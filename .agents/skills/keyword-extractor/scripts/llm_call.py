"""
llm_call.py — Shared LLM call helper with retry, error classification, and
fail-fast semantics for Knowledge Tree skill scripts.

Design principles (per AGENTS.md §9, §10):
- NEVER swallow LLM errors silently. Always classify and surface them.
- Distinguish retryable (network, rate limit, timeout) from fatal (auth, model
  not found) errors.
- On fatal error or retry exhaustion: raise LLMCallError so caller can decide
  whether to abort the whole pipeline (fail-fast) or skip the batch with an
  explicit audit trail.
- Never overwrite good data with empty data when LLM fails — caller is
  responsible for checking the return value and aborting before writing TSVs.

Usage:
    from llm_call import llm_chat_json, llm_embed, LLMCallError

    try:
        result = llm_chat_json(client, model, system, user, temperature=0.2)
    except LLMCallError as e:
        print(f"[FATAL] LLM failed: {e}", file=sys.stderr)
        sys.exit(1)

    # For batch operations where partial failure is acceptable but must be tracked:
    failures = []
    for item in batch:
        try:
            r = llm_chat_json(client, model, system, user.format(item=item))
            results.append(r)
        except LLMCallError as e:
            failures.append({"item": item, "error": str(e)})
            continue
    if failures:
        # Write audit trail so downstream knows data is incomplete
        with open(work_dir / "llm_failures.json", "w") as f:
            json.dump(failures, f, indent=2)
        print(f"[WARN] {len(failures)} batch items failed LLM call", file=sys.stderr)
"""

import json
import re
import time
from typing import Any, Optional


class LLMCallError(Exception):
    """Raised when an LLM call fails after retries or encounters a fatal error.

    Attributes:
        error_type: 'auth' | 'rate_limit' | 'timeout' | 'network' |
                    'model_not_found' | 'json_parse' | 'empty_response' |
                    'api_error' | 'unknown'
        retryable: whether the error is retryable
        original: the original exception (if any)
    """

    def __init__(self, message: str, error_type: str = "unknown",
                 retryable: bool = False, original: Optional[Exception] = None):
        super().__init__(message)
        self.error_type = error_type
        self.retryable = retryable
        self.original = original

    def __str__(self):
        return f"[{self.error_type}] {super().__str__()}"


def _classify_error(e: Exception) -> tuple[str, bool]:
    """Classify an OpenAI/API exception into (error_type, retryable).
    Returns (type, retryable)."""
    msg = str(e).lower()
    exc_type = type(e).__name__.lower()

    # Auth / API key issues — fatal, not retryable
    if any(k in msg for k in ["api key", "unauthorized", "forbidden",
                               "authentication", "401", "403"]):
        return "auth", False

    # Rate limit — retryable with backoff
    if any(k in msg for k in ["rate limit", "429", "too many requests",
                               "rate_limit"]):
        return "rate_limit", True

    # Timeout — retryable
    if any(k in msg for k in ["timeout", "timed out", "read timeout"]):
        return "timeout", True

    # Network — retryable
    if any(k in msg for k in ["connection", "network", "unreachable",
                               "refused", "reset", "dns", "resolve"]):
        return "network", True

    # Model not found — fatal
    if any(k in msg for k in ["model not found", "does not exist",
                               "not available", "invalid model"]):
        return "model_not_found", False

    # Bad request / invalid input — fatal
    if any(k in msg for k in ["bad request", "400", "invalid"]):
        return "bad_request", False

    # API server error — retryable
    if any(k in msg for k in ["500", "502", "503", "504", "server error",
                               "internal error", "service unavailable"]):
        return "api_error", True

    # Fallback
    return "unknown", False


def _retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
):
    """Execute func with exponential backoff retry.

    Retryable errors: network, timeout, rate_limit, api_error.
    Fatal errors: auth, model_not_found, bad_request — raise immediately.
    """
    last_error: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except LLMCallError as e:
            if not e.retryable or attempt == max_retries:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            print(f"  [RETRY] {e.error_type} — retry {attempt+1}/{max_retries} "
                  f"after {delay:.1f}s", flush=True)
            time.sleep(delay)
            last_error = e
        except Exception as e:
            error_type, retryable = _classify_error(e)
            if not retryable or attempt == max_retries:
                raise LLMCallError(str(e), error_type, retryable, original=e)
            delay = min(base_delay * (2 ** attempt), max_delay)
            print(f"  [RETRY] {error_type} — retry {attempt+1}/{max_retries} "
                  f"after {delay:.1f}s", flush=True)
            time.sleep(delay)
            last_error = e
    # Should not reach here, but just in case
    raise LLMCallError(f"Retry exhausted: {last_error}", "retry_exhausted", False)


def llm_chat_json(
    client,
    model: str,
    system: str,
    user: str,
    temperature: float = 0.2,
    max_retries: int = 3,
) -> dict:
    """Call LLM chat completion and parse JSON response.

    Returns parsed dict. Raises LLMCallError on failure.

    Handles:
    - Network/rate-limit/timeout errors with retry + exponential backoff
    - JSON parse failures (tries to extract JSON from markdown fences, fix
      trailing commas)
    - Empty responses
    - Auth/model errors (fatal, no retry)
    """
    def _call():
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
            )
        except Exception as e:
            error_type, retryable = _classify_error(e)
            raise LLMCallError(str(e), error_type, retryable, original=e)

        raw = (completion.choices[0].message.content or "").strip()
        if not raw:
            raise LLMCallError("LLM returned empty response", "empty_response", False)

        # Strip markdown code fences
        if raw.startswith("```"):
            raw = re.sub(r"```(?:json)?\n?", "", raw).strip("` \n")

        # Try direct parse
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Try extracting first JSON object
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
            # Fix trailing commas
            try:
                fixed = re.sub(r",\s*([}\]])", r"\1", m.group())
                return json.loads(fixed)
            except json.JSONDecodeError:
                pass

        raise LLMCallError(
            f"LLM returned non-JSON response. Raw snippet: {raw[:200]}",
            "json_parse", False
        )

    return _retry_with_backoff(_call, max_retries=max_retries)


def llm_chat_text(
    client,
    model: str,
    system: str,
    user: str,
    temperature: float = 0.2,
    max_retries: int = 3,
) -> str:
    """Call LLM chat completion and return raw text response.

    Returns text string. Raises LLMCallError on failure.
    """
    def _call():
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
            )
        except Exception as e:
            error_type, retryable = _classify_error(e)
            raise LLMCallError(str(e), error_type, retryable, original=e)

        raw = (completion.choices[0].message.content or "").strip()
        if not raw:
            raise LLMCallError("LLM returned empty response", "empty_response", False)
        return raw

    return _retry_with_backoff(_call, max_retries=max_retries)


def llm_embed(
    client,
    texts: list[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
    max_retries: int = 3,
) -> list[list[float]]:
    """Embed texts in batches. Returns list of embedding vectors.

    Raises LLMCallError on failure. Does NOT return partial results —
    either all embeddings succeed or the whole call fails.
    """
    def _embed_batch(batch: list[str]) -> list[list[float]]:
        try:
            response = client.embeddings.create(input=batch, model=model)
        except Exception as e:
            error_type, retryable = _classify_error(e)
            raise LLMCallError(str(e), error_type, retryable, original=e)
        return [item.embedding for item in response.data]

    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        embs = _retry_with_backoff(lambda b=batch: _embed_batch(b), max_retries=max_retries)
        all_embeddings.extend(embs)
    return all_embeddings


def llm_embed_single(
    client,
    text: str,
    model: str = "text-embedding-3-small",
    max_retries: int = 3,
) -> list[float]:
    """Embed a single text. Returns one embedding vector.

    Raises LLMCallError on failure.
    """
    def _call():
        try:
            response = client.embeddings.create(input=[text], model=model)
        except Exception as e:
            error_type, retryable = _classify_error(e)
            raise LLMCallError(str(e), error_type, retryable, original=e)
        if not response.data:
            raise LLMCallError("Embedding API returned no data", "empty_response", False)
        return response.data[0].embedding

    return _retry_with_backoff(_call, max_retries=max_retries)