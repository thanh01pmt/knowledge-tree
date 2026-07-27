#!/usr/bin/env python3
"""
filter_by_relevance.py — Bước 3: Lọc candidates theo domain-relevance bằng embedding cosine.

Input:  .work/kw/candidates_statistical.json + candidates_llm.json + config.json
Output: .work/kw/candidates_filtered.json
        .work/kw/candidates_filtered.md  (preview)

Logic:
- Union 2 candidate lists (statistical + LLM), dedup by term_normalized
- Embed target_context + từng term candidate bằng embedding model
  (default: nomic-embed-text:latest qua Ollama, cấu hình qua env ATE_EMBED_MODEL)
- Giữ lại theo cosine similarity >= threshold (default 0.25 — lỏng, ưu tiên recall)
- Precision được xử lý ở bước sau (llm_verify_and_dedup)
- Batch embed để giảm số API calls
"""

import argparse
import json
import math
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("[ERROR] Cài đặt: pip install openai", file=sys.stderr)
    sys.exit(1)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def create_openai_client() -> OpenAI:
    """Tạo OpenAI client, ưu tiên OPENAI_BASE_URL nếu có (Ollama compat)."""
    api_key = os.environ.get("OPENAI_API_KEY", "ollama")
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    if not api_key or api_key == "ollama":
        print("[ERROR] OPENAI_API_KEY hoặc OPENAI_BASE_URL chưa cấu hình.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def load_work_dir(args, repo_root: Path) -> Path:
    if args.work_dir:
        return Path(args.work_dir)
    if args.project:
        return repo_root / "projects" / args.project / ".work" / "kw"
    status_file = repo_root / "status.yaml"
    if status_file.is_file():
        for line in status_file.read_text().splitlines():
            if line.startswith("active_project"):
                slug = line.split(":", 1)[1].strip().strip("'\"")
                if slug:
                    return repo_root / "projects" / slug / ".work" / "kw"
    return repo_root / ".work" / "kw"


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def batch_embed(client: OpenAI, texts: list[str], model: str = "text-embedding-3-small", batch_size: int = 100) -> list[list[float]]:
    """Embed texts in batches. Returns list of embedding vectors.
    Raises LLMCallError on failure (does NOT return partial results)."""
    import sys as _sys
    from pathlib import Path as _Path
    _skill_scripts = _Path(__file__).resolve().parent
    if str(_skill_scripts) not in _sys.path:
        _sys.path.insert(0, str(_skill_scripts))
    from llm_call import llm_embed as _llm_embed
    return _llm_embed(client, texts, model=model, batch_size=batch_size)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Filter candidates by embedding cosine similarity")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--work-dir", help="Override .work/kw/ path")
    parser.add_argument("--threshold", type=float, default=0.25,
                        help="Cosine threshold (default: 0.25 — lỏng, ưu tiên recall)")
    parser.add_argument("--embed-model", default=None,
                        help="Embedding model (default: ATE_EMBED_MODEL env hoặc nomic-embed-text:latest)")
    parser.add_argument("--target-context", help="Override target_context từ config.json")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)
    if not args.embed_model:
        args.embed_model = os.environ.get("ATE_EMBED_MODEL", "nomic-embed-text:latest")
    work_dir = load_work_dir(args, repo_root)

    # Load config
    config_path = work_dir / "config.json"
    config = {}
    if config_path.is_file():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

    target_context = args.target_context or config.get("target_context", "")
    if not target_context:
        print("[ERROR] Cần target_context. Chạy scaffold-keywords trước.", file=sys.stderr)
        sys.exit(1)

    # Load candidates từ cả 2 sources
    def load_candidates(path: Path) -> list[dict]:
        if not path.is_file():
            return []
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    stat_candidates = load_candidates(work_dir / "candidates_statistical.json")
    llm_candidates = load_candidates(work_dir / "candidates_llm.json")

    print(f"[*] Statistical: {len(stat_candidates)} | LLM: {len(llm_candidates)}")

    # Union + dedup by term_normalized
    merged: dict[str, dict] = {}

    for c in stat_candidates:
        key = c.get("term_normalized") or c.get("term", "").lower().strip()
        if key not in merged:
            merged[key] = {
                "term": c.get("term_original") or c.get("term", ""),
                "term_normalized": key,
                "category": c.get("category", "unknown"),
                "source_chunks": list(c.get("source_chunks", [])),
                "first_extraction_method": "statistical",
                "yake_score": c.get("best_score"),
            }

    for c in llm_candidates:
        key = c.get("term_normalized") or c.get("term", "").lower().strip()
        if key not in merged:
            merged[key] = {
                "term": c.get("term", ""),
                "term_normalized": key,
                "category": c.get("category", "unknown"),
                "source_chunks": list(c.get("source_chunks", [])),
                "first_extraction_method": "llm",
                "yake_score": None,
            }
        else:
            # Đã có từ statistical — bổ sung source_chunks và update method
            entry = merged[key]
            for sc in c.get("source_chunks", []):
                if sc not in entry["source_chunks"]:
                    entry["source_chunks"].append(sc)
            # Nếu cả 2 source tìm thấy → ghi nhận
            if entry["first_extraction_method"] == "statistical":
                entry["confirmed_by_llm"] = True

    all_candidates = list(merged.values())
    print(f"[*] Union sau dedup surface-level: {len(all_candidates)} candidates")

    client = create_openai_client()

    # Embed target_context
    print(f"[*] Embedding target_context: '{target_context}' ...")
    import sys as _sys
    from pathlib import Path as _Path
    _skill_scripts = _Path(__file__).resolve().parent
    if str(_skill_scripts) not in _sys.path:
        _sys.path.insert(0, str(_skill_scripts))
    from llm_call import llm_embed_single as _llm_embed_single, LLMCallError as _LLMCallError
    try:
        target_emb = _llm_embed_single(client, target_context, model=args.embed_model)
    except _LLMCallError as e:
        print(f"[FATAL] Embedding target_context failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Batch embed tất cả candidates
    terms_to_embed = [c["term"] for c in all_candidates]
    print(f"[*] Embedding {len(terms_to_embed)} candidates (batch) ...")
    try:
        embeddings = batch_embed(client, terms_to_embed, model=args.embed_model)
    except _LLMCallError as e:
        print(f"[FATAL] Embedding candidates failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Tính cosine similarity + filter
    filtered = []
    for c, emb in zip(all_candidates, embeddings):
        score = cosine_similarity(target_emb, emb)
        c["relevance_score"] = round(score, 4)
        if score >= args.threshold:
            filtered.append(c)

    # Sort by relevance_score desc
    filtered.sort(key=lambda x: x["relevance_score"], reverse=True)

    out_path = work_dir / "candidates_filtered.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    # Generate preview markdown
    md_lines = [
        f"# Candidates Filtered — {target_context}",
        f"\n**Threshold:** {args.threshold} | **Total:** {len(filtered)} / {len(all_candidates)} candidates\n",
        "| Term | Category | Score | Method | Chunks |",
        "|------|----------|-------|--------|--------|",
    ]
    for c in filtered[:100]:  # Preview top 100
        aliases = ""
        md_lines.append(
            f"| {c['term']} | {c.get('category','?')} | {c['relevance_score']:.3f} | "
            f"{c['first_extraction_method']} | {', '.join(c['source_chunks'][:3])} |"
        )
    if len(filtered) > 100:
        md_lines.append(f"\n*... và {len(filtered) - 100} term khác (xem candidates_filtered.json)*")

    md_path = work_dir / "candidates_filtered.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[✓] {len(filtered)} candidates qua lọc (ngưỡng={args.threshold}) → {out_path}")
    print(f"[✓] Preview → {md_path}")


if __name__ == "__main__":
    main()
