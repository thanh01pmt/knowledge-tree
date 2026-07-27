#!/usr/bin/env python3
"""
test_llm_error_handling.py — Test suite cho LLM error handling improvements.

Test:
- llm_call.py: error classification, retry logic, JSON parse
- Fail-fast semantics: LLM failure → exit nonzero, không ghi TSV rỗng
- Audit trail: failures được ghi ra file
- MCP: exit code propagation qua _run_script

Chạy: python3 tests/test_llm_error_handling.py
Không cần API key — test thuần deterministic với mock.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_SCRIPTS = REPO_ROOT / ".agents/skills/keyword-extractor/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from llm_call import (
    LLMCallError, _classify_error, llm_chat_json,
    llm_embed, llm_embed_single, _retry_with_backoff
)


# ─── Tests: error classification ─────────────────────────────────────────────

def test_classify_auth_error():
    """Auth errors must be classified as fatal (not retryable)."""
    e = Exception("Invalid API key provided")
    etype, retryable = _classify_error(e)
    assert etype == "auth", f"Expected 'auth', got '{etype}'"
    assert not retryable, "Auth error must NOT be retryable"
    print("✓ test_classify_auth_error")


def test_classify_rate_limit():
    """Rate limit errors must be retryable."""
    e = Exception("Rate limit exceeded: 429 Too Many Requests")
    etype, retryable = _classify_error(e)
    assert etype == "rate_limit", f"Expected 'rate_limit', got '{etype}'"
    assert retryable, "Rate limit must be retryable"
    print("✓ test_classify_rate_limit")


def test_classify_timeout():
    """Timeout errors must be retryable."""
    e = Exception("Request timed out: read timeout after 60s")
    etype, retryable = _classify_error(e)
    assert etype == "timeout", f"Expected 'timeout', got '{etype}'"
    assert retryable, "Timeout must be retryable"
    print("✓ test_classify_timeout")


def test_classify_network_error():
    """Network errors must be retryable."""
    e = Exception("Connection refused: could not connect to host")
    etype, retryable = _classify_error(e)
    assert etype == "network", f"Expected 'network', got '{etype}'"
    assert retryable, "Network error must be retryable"
    print("✓ test_classify_network_error")


def test_classify_model_not_found():
    """Model not found must be fatal."""
    e = Exception("The model 'gpt-999' does not exist")
    etype, retryable = _classify_error(e)
    assert etype == "model_not_found", f"Expected 'model_not_found', got '{etype}'"
    assert not retryable, "Model not found must NOT be retryable"
    print("✓ test_classify_model_not_found")


def test_classify_api_error():
    """5xx server errors must be retryable."""
    e = Exception("503 Service Unavailable")
    etype, retryable = _classify_error(e)
    assert etype == "api_error", f"Expected 'api_error', got '{etype}'"
    assert retryable, "5xx must be retryable"
    print("✓ test_classify_api_error")


# ─── Tests: LLMCallError attributes ───────────────────────────────────────────

def test_llm_call_error_attributes():
    """LLMCallError must carry error_type and retryable."""
    e = LLMCallError("test error", error_type="auth", retryable=False)
    assert e.error_type == "auth"
    assert e.retryable == False
    assert "auth" in str(e)
    print("✓ test_llm_call_error_attributes")


# ─── Tests: llm_chat_json with mock ───────────────────────────────────────────

def test_llm_chat_json_success():
    """llm_chat_json must parse valid JSON response."""
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '{"result": "ok"}'
    mock_client.chat.completions.create.return_value = mock_completion

    result = llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=0)
    assert result == {"result": "ok"}, f"Expected parsed dict, got {result}"
    print("✓ test_llm_chat_json_success")


def test_llm_chat_json_markdown_fence():
    """llm_chat_json must strip markdown code fences."""
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '```json\n{"key": "value"}\n```'
    mock_client.chat.completions.create.return_value = mock_completion

    result = llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=0)
    assert result == {"key": "value"}, f"Expected parsed dict, got {result}"
    print("✓ test_llm_chat_json_markdown_fence")


def test_llm_chat_json_trailing_comma():
    """llm_chat_json must fix trailing commas in JSON."""
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '{"items": [1, 2, 3,],}'
    mock_client.chat.completions.create.return_value = mock_completion

    result = llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=0)
    assert "items" in result, f"Expected items key, got {result}"
    print("✓ test_llm_chat_json_trailing_comma")


def test_llm_chat_json_empty_response():
    """llm_chat_json must raise LLMCallError on empty response."""
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = ""
    mock_client.chat.completions.create.return_value = mock_completion

    try:
        llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=0)
        assert False, "Should have raised LLMCallError"
    except LLMCallError as e:
        assert e.error_type == "empty_response"
    print("✓ test_llm_chat_json_empty_response")


def test_llm_chat_json_non_json_response():
    """llm_chat_json must raise LLMCallError on non-JSON response."""
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "Sorry, I cannot help with that."
    mock_client.chat.completions.create.return_value = mock_completion

    try:
        llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=0)
        assert False, "Should have raised LLMCallError"
    except LLMCallError as e:
        assert e.error_type == "json_parse"
    print("✓ test_llm_chat_json_non_json_response")


def test_llm_chat_json_auth_error_no_retry():
    """llm_chat_json must raise immediately on auth error (no retry)."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("401 Unauthorized: Invalid API key")

    try:
        llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=3)
        assert False, "Should have raised LLMCallError"
    except LLMCallError as e:
        assert e.error_type == "auth"
        assert e.retryable == False
    # Must NOT have retried (auth = fatal)
    assert mock_client.chat.completions.create.call_count == 1, \
        "Auth error must not retry"
    print("✓ test_llm_chat_json_auth_error_no_retry")


def test_llm_chat_json_retry_on_rate_limit():
    """llm_chat_json must retry on rate limit error."""
    mock_client = MagicMock()
    # First call: rate limit, second call: success
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '{"ok": true}'
    mock_client.chat.completions.create.side_effect = [
        Exception("429 Rate limit exceeded"),
        mock_completion,
    ]

    with patch("llm_call.time.sleep") as mock_sleep:
        result = llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=3)
    assert result == {"ok": True}
    assert mock_client.chat.completions.create.call_count == 2, "Should retry once"
    mock_sleep.assert_called_once()
    print("✓ test_llm_chat_json_retry_on_rate_limit")


def test_llm_chat_json_retry_exhaustion():
    """llm_chat_json must raise after max retries."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("503 Service Unavailable")

    with patch("llm_call.time.sleep"):
        try:
            llm_chat_json(mock_client, "test-model", "sys", "user", max_retries=2)
            assert False, "Should have raised LLMCallError"
        except LLMCallError as e:
            assert e.error_type in ("api_error", "retry_exhausted")
    # Should have tried max_retries + 1 = 3 times
    assert mock_client.chat.completions.create.call_count == 3
    print("✓ test_llm_chat_json_retry_exhaustion")


# ─── Tests: llm_embed ─────────────────────────────────────────────────────────

def test_llm_embed_success():
    """llm_embed must return embeddings for all texts."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_item = MagicMock()
    mock_item.embedding = [0.1, 0.2, 0.3]
    mock_response.data = [mock_item, mock_item]
    mock_client.embeddings.create.return_value = mock_response

    result = llm_embed(mock_client, ["text1", "text2"], model="test", max_retries=0)
    assert len(result) == 2
    assert result[0] == [0.1, 0.2, 0.3]
    print("✓ test_llm_embed_success")


def test_llm_embed_failure():
    """llm_embed must raise LLMCallError on API failure."""
    mock_client = MagicMock()
    mock_client.embeddings.create.side_effect = Exception("401 Unauthorized")

    try:
        llm_embed(mock_client, ["text1"], model="test", max_retries=0)
        assert False, "Should have raised LLMCallError"
    except LLMCallError as e:
        assert e.error_type == "auth"
    print("✓ test_llm_embed_failure")


# ─── Tests: MCP exit code propagation ─────────────────────────────────────────

def test_mcp_run_script_exit_code_propagation():
    """_run_script must report non-zero exit code as failure."""
    sys.path.insert(0, str(REPO_ROOT / "kt_mcp"))
    sys.path.insert(0, str(REPO_ROOT))
    from servers.kt_server import _run_script

    # Create a temp script that exits 1
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, dir="/tmp") as f:
        f.write("import sys; print('error occurred'); sys.exit(1)")
        temp_script = Path(f.name)

    try:
        result = _run_script(temp_script, "test-valid-project", timeout=10)
        assert "FAILED" in result or "exited with code 1" in result, \
            f"Non-zero exit must be reported as failure, got: {result[:200]}"
        assert "INCOMPLETE" in result or "CORRUPTED" in result, \
            f"Must warn about data integrity, got: {result[:200]}"
    finally:
        temp_script.unlink()
    print("✓ test_mcp_run_script_exit_code_propagation")


def test_mcp_run_script_success():
    """_run_script must return clean output on exit 0."""
    sys.path.insert(0, str(REPO_ROOT / "kt_mcp"))
    sys.path.insert(0, str(REPO_ROOT))
    from servers.kt_server import _run_script

    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, dir="/tmp") as f:
        f.write("print('all good')")
        temp_script = Path(f.name)

    try:
        result = _run_script(temp_script, "test-valid-project", timeout=10)
        assert "all good" in result
        assert "FAILED" not in result
    finally:
        temp_script.unlink()
    print("✓ test_mcp_run_script_success")


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_all():
    tests = [
        test_classify_auth_error,
        test_classify_rate_limit,
        test_classify_timeout,
        test_classify_network_error,
        test_classify_model_not_found,
        test_classify_api_error,
        test_llm_call_error_attributes,
        test_llm_chat_json_success,
        test_llm_chat_json_markdown_fence,
        test_llm_chat_json_trailing_comma,
        test_llm_chat_json_empty_response,
        test_llm_chat_json_non_json_response,
        test_llm_chat_json_auth_error_no_retry,
        test_llm_chat_json_retry_on_rate_limit,
        test_llm_chat_json_retry_exhaustion,
        test_llm_embed_success,
        test_llm_embed_failure,
        test_mcp_run_script_exit_code_propagation,
        test_mcp_run_script_success,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"✗ {t.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    print(f"\n{'='*50}")
    print(f"LLM Error Handling Tests: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'='*50}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())