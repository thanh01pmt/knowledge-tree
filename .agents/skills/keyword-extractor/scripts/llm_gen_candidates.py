#!/usr/bin/env python3
"""
llm_gen_candidates.py — Bước 2b: LLM candidate generation per-chunk.

Input:  .work/kw/chunks.json + target_context (từ config.json)
Output: .work/kw/candidates_llm.json

Prompt nguyên tắc:
- Tường minh "liệt kê MỌI thuật ngữ, kể cả xuất hiện 1 lần"
- "KHÔNG lọc theo mức độ quan trọng" — chặn xu hướng tự-curate của LLM
- Structured output (Pydantic) để parse stable
- Tái sử dụng find_repo_root() / load_env() pattern từ llm_extract_lo.py
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] Cài đặt: pip install openai pydantic", file=sys.stderr)
    sys.exit(1)


# ─── Models ───────────────────────────────────────────────────────────────────

class CandidateTerm(BaseModel):
    term: str = Field(description=(
        "Thuật ngữ nguyên văn như xuất hiện trong chunk. "
        "Có thể là từ đơn, cụm từ, tên viết tắt, tên riêng, hoặc tên công nghệ."
    ))
    category: str = Field(description=(
        "Phân loại nhanh: 'hardware' | 'software' | 'protocol' | 'concept' | 'tool' | 'other'"
    ))


class ChunkCandidates(BaseModel):
    chunk_id: str
    terms: list[CandidateTerm]


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


# ─── LLM call ─────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Bạn là chuyên gia trích xuất thuật ngữ chuyên ngành (Automatic Term Extraction).
Nhiệm vụ: Liệt kê TẤT CẢ thuật ngữ/tên riêng/viết tắt xuất hiện trong đoạn văn cho trước có liên quan đến chủ đề mục tiêu.

QUAN TRỌNG:
- KHÔNG lọc theo mức độ quan trọng hay tần suất.
- KHÔNG chỉ lấy những thứ "nổi bật nhất" — liệt kê KỂ CẢ thuật ngữ chỉ xuất hiện 1 lần.
- Bao gồm: tên chip, tên thư viện, giao thức, viết tắt kỹ thuật, tên API, tên hàm/lệnh nếu liên quan chủ đề.
- Giữ nguyên viết hoa/viết thường như trong văn bản gốc."""


def extract_terms_for_chunk(
    client: OpenAI,
    chunk: dict,
    target_context: str,
    model: str = "gpt-4o-mini",
) -> list[dict]:
    """Gọi LLM để trích xuất term từ 1 chunk. Trả về list dict."""

    user_prompt = f"""Chủ đề mục tiêu: "{target_context}"

Ngữ cảnh heading: {chunk.get('heading_trail', '(không có)')}

Đoạn văn:
---
{chunk['text']}
---

Liệt kê MỌI thuật ngữ liên quan đến chủ đề mục tiêu có trong đoạn văn trên."""

    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format=ChunkCandidates,
            temperature=0.1,
        )
        result = completion.choices[0].message.parsed
        if result is None:
            return []
        return [
            {
                "term": t.term.strip(),
                "category": t.category,
                "source_chunks": [chunk["chunk_id"]],
                "first_extraction_method": "llm",
            }
            for t in result.terms
            if t.term.strip()
        ]
    except Exception as e:
        print(f"  [WARN] chunk {chunk['chunk_id']}: {e}", file=sys.stderr)
        return []


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LLM candidate generation for ATE pipeline")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--work-dir", help="Override .work/kw/ path")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model (default: gpt-4o-mini)")
    parser.add_argument("--target-context", help="Override target_context từ config.json")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)
    work_dir = load_work_dir(args, repo_root)

    # Load chunks
    chunks_path = work_dir / "chunks.json"
    if not chunks_path.is_file():
        print(f"[ERROR] Không tìm thấy chunks.json: {chunks_path}", file=sys.stderr)
        sys.exit(1)
    with open(chunks_path, encoding="utf-8") as f:
        chunks = json.load(f)

    # Load config (target_context)
    config_path = work_dir / "config.json"
    config = {}
    if config_path.is_file():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

    target_context = args.target_context or config.get("target_context", "")
    if not target_context:
        print("[ERROR] Cần cung cấp --target-context hoặc chạy scaffold-keywords trước.", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY không tìm thấy. Thêm vào .env hoặc export.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"[*] LLM candidate gen: {len(chunks)} chunks, target='{target_context}', model={args.model}")

    # term_lower → merged entry
    term_map: dict[str, dict] = {}

    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}/{len(chunks)}] {chunk['chunk_id']} ({len(chunk.get('text',''))} chars) ...", end=" ")
        terms = extract_terms_for_chunk(client, chunk, target_context, model=args.model)
        for t in terms:
            key = t["term"].lower().strip()
            if len(key) < 2:
                continue
            if key not in term_map:
                term_map[key] = {
                    "term": t["term"],
                    "term_normalized": key,
                    "category": t["category"],
                    "source_chunks": t["source_chunks"],
                    "first_extraction_method": "llm",
                }
            else:
                entry = term_map[key]
                for sc in t["source_chunks"]:
                    if sc not in entry["source_chunks"]:
                        entry["source_chunks"].append(sc)
        print(f"{len(terms)} terms")

    candidates_out = list(term_map.values())

    out_path = work_dir / "candidates_llm.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(candidates_out, f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(candidates_out)} LLM candidates → {out_path}")


if __name__ == "__main__":
    main()
