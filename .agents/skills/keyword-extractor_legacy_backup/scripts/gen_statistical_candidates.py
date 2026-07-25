#!/usr/bin/env python3
"""
gen_statistical_candidates.py — Bước 2a: YAKE statistical candidate generation.

Input:  .work/kw/chunks.json
Output: .work/kw/candidates_statistical.json

Logic:
- Chạy YAKE trên từng chunk, KHÔNG áp ngưỡng high → mục tiêu recall
- Extract noun-phrases và multi-word terms (n=1..4)
- Dedup nhẹ ở mức string (lowercase) trước khi ghi — dedup ngữ nghĩa để sau ở llm_verify
- Không gọi LLM, không cần API key
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_work_dir(args, repo_root: Path) -> Path:
    if args.work_dir:
        return Path(args.work_dir)
    if args.project:
        return repo_root / "projects" / args.project / ".work" / "kw"
    # Đọc active project từ status.yaml
    status_file = repo_root / "status.yaml"
    if status_file.is_file():
        for line in status_file.read_text().splitlines():
            if line.startswith("active_project"):
                slug = line.split(":", 1)[1].strip().strip("'\"")
                if slug:
                    return repo_root / "projects" / slug / ".work" / "kw"
    return repo_root / ".work" / "kw"


def run_yake_on_chunk(text: str, lang: str = "en", max_ngram: int = 4, top_n: int = 200) -> list[dict]:
    """
    Chạy YAKE. Trả về danh sách {term, score} — score thấp = quan trọng hơn trong YAKE.
    top_n cao (200) để recall cao; dedup chính xác để sau ở LLM.
    """
    try:
        import yake
    except ImportError:
        print("[ERROR] yake chưa cài. Chạy: pip install yake", file=sys.stderr)
        sys.exit(1)

    # YAKE: deduplication_threshold cao (0.9) để giữ nhiều term hơn
    kw_extractor = yake.KeywordExtractor(
        lan=lang,
        n=max_ngram,
        dedupLim=0.9,
        top=top_n,
        features=None,
    )
    try:
        keywords = kw_extractor.extract_keywords(text)
    except Exception:
        keywords = []

    return [{"term": kw, "score": round(score, 6)} for kw, score in keywords]


def normalize_term(term: str) -> str:
    """Normalize nhẹ để dedup surface-level (lowercase, strip, collapse spaces)."""
    return re.sub(r"\s+", " ", term.strip().lower())


def main():
    parser = argparse.ArgumentParser(description="YAKE statistical candidate generation")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--work-dir", help="Override .work/kw/ path")
    parser.add_argument("--lang", default="en", help="Language cho YAKE (default: en)")
    parser.add_argument("--max-ngram", type=int, default=4, help="Max n-gram size (default: 4)")
    parser.add_argument("--top-n", type=int, default=200, help="Top-N per chunk (default: 200, mục tiêu recall)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    work_dir = load_work_dir(args, repo_root)

    chunks_path = work_dir / "chunks.json"
    if not chunks_path.is_file():
        print(f"[ERROR] Không tìm thấy chunks.json tại: {chunks_path}", file=sys.stderr)
        print("Hãy chạy chunk_source.py trước.", file=sys.stderr)
        sys.exit(1)

    with open(chunks_path, encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"[*] Chạy YAKE trên {len(chunks)} chunks (lang={args.lang}, max_ngram={args.max_ngram}, top_n={args.top_n}) ...")

    # term_normalized → best_score, source_chunks, original_forms
    term_map: dict[str, dict] = {}

    for chunk in chunks:
        chunk_id = chunk["chunk_id"]
        text = chunk.get("text", "")
        if not text.strip():
            continue

        candidates = run_yake_on_chunk(text, lang=args.lang, max_ngram=args.max_ngram, top_n=args.top_n)

        for c in candidates:
            norm = normalize_term(c["term"])
            if len(norm) < 2:
                continue  # bỏ single-char

            if norm not in term_map:
                term_map[norm] = {
                    "term_normalized": norm,
                    "term_original": c["term"],
                    "best_score": c["score"],
                    "source_chunks": [chunk_id],
                    "first_extraction_method": "statistical",
                }
            else:
                entry = term_map[norm]
                # YAKE: score thấp hơn = tốt hơn
                if c["score"] < entry["best_score"]:
                    entry["best_score"] = c["score"]
                    entry["term_original"] = c["term"]
                if chunk_id not in entry["source_chunks"]:
                    entry["source_chunks"].append(chunk_id)

    candidates_out = sorted(term_map.values(), key=lambda x: x["best_score"])

    out_path = work_dir / "candidates_statistical.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(candidates_out, f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(candidates_out)} statistical candidates → {out_path}")


if __name__ == "__main__":
    main()
