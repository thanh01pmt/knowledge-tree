#!/usr/bin/env python3
"""
llm_verify_and_dedup.py — Bước 4+5: LLM dedup biến thể + omission-check loop.

Input:  .work/kw/candidates_filtered.json + chunks.json + config.json
Output: .work/kw/keywords_verified.json
        .work/kw/verify-report.md  ← điểm duyệt người

Pipeline:
  Phase A — Dedup & Canonicalize:
    LLM nhóm các biến thể thành canonical form + aliases
    (VD: "ESP32-S3" / "ESP32 S3" / "esp32s3" → canonical: "ESP32-S3", aliases: [...])

  Phase B — Omission Check Loop (tối đa 2 vòng):
    Per-chunk: "chunk này có thuật ngữ liên quan chủ đề chưa có trong danh sách không?"
    Model thấy TOÀN BỘ danh sách hiện có + chunk gốc trong cùng 1 lượt gọi
    Dừng sớm nếu vòng nào Δ = 0 (không term mới)
    Term thêm từ omission-check → first_extraction_method = "omission_check"

  Sau phase B: mini-dedup để gộp term mới với list cũ nếu trùng
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] Cài đặt: pip install openai pydantic", file=sys.stderr)
    sys.exit(1)


# ─── Models ───────────────────────────────────────────────────────────────────

class CanonicalGroup(BaseModel):
    canonical: str = Field(description="Dạng chuẩn hóa của thuật ngữ (thường là dạng phổ biến nhất / đúng nhất)")
    aliases: list[str] = Field(description="Các biến thể/alias, KHÔNG bao gồm canonical")
    category: str = Field(description="hardware | software | protocol | concept | tool | other")


class DedupResponse(BaseModel):
    groups: list[CanonicalGroup]


class OmissionTerm(BaseModel):
    term: str = Field(description="Thuật ngữ mới chưa có trong danh sách")
    category: str = Field(description="hardware | software | protocol | concept | tool | other")


class OmissionResponse(BaseModel):
    new_terms: list[OmissionTerm] = Field(
        description="Danh sách thuật ngữ liên quan chưa có trong danh sách hiện tại. Để trống nếu không tìm thấy."
    )


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


# ─── Phase A: Dedup ───────────────────────────────────────────────────────────

DEDUP_SYSTEM = """Bạn là chuyên gia chuẩn hóa thuật ngữ kỹ thuật.
Nhóm các biến thể/alias của cùng một thuật ngữ thành một canonical form.

Quy tắc:
- Chọn dạng CANONICAL phổ biến/đúng nhất (VD: "ESP32-S3" không phải "esp32s3")
- KHÔNG gộp các thuật ngữ khác nghĩa dù embedding gần nhau (VD: "I2C" và "SPI" là khác nhau)
- Mỗi term trong input phải xuất hiện ĐÚNG MỘT LẦN trong output (là canonical HOẶC alias)
- Nếu term hoàn toàn độc lập, tạo group riêng với aliases = []"""


def dedup_candidates(client: OpenAI, candidates: list[dict], model: str, batch_size: int = 80) -> list[dict]:
    """Phase A: Gộp biến thể. Xử lý theo batch nếu list dài."""
    all_groups: list[dict] = []
    terms = [c["term"] for c in candidates]

    # Map term → candidate để giữ metadata
    term_to_meta: dict[str, dict] = {c["term"].lower().strip(): c for c in candidates}

    print(f"  [A] Dedup {len(terms)} terms theo batch_size={batch_size} ...")

    for batch_start in range(0, len(terms), batch_size):
        batch_terms = terms[batch_start:batch_start + batch_size]
        term_list_str = "\n".join(f"- {t}" for t in batch_terms)
        user_prompt = f"Danh sách thuật ngữ cần nhóm:\n{term_list_str}"

        try:
            completion = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": DEDUP_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=DedupResponse,
                temperature=0.0,
            )
            result = completion.choices[0].message.parsed
            if result is None:
                continue

            for g in result.groups:
                canonical_key = g.canonical.lower().strip()
                meta = term_to_meta.get(canonical_key, {})
                # Merge source_chunks từ tất cả aliases
                all_source_chunks = list(meta.get("source_chunks", []))
                for alias in g.aliases:
                    alias_meta = term_to_meta.get(alias.lower().strip(), {})
                    for sc in alias_meta.get("source_chunks", []):
                        if sc not in all_source_chunks:
                            all_source_chunks.append(sc)

                # first_extraction_method: ưu tiên "statistical" nếu có alias từ statistical
                method = meta.get("first_extraction_method", "llm")
                for alias in g.aliases:
                    alias_meta = term_to_meta.get(alias.lower().strip(), {})
                    if alias_meta.get("first_extraction_method") == "statistical":
                        method = "statistical"
                        break

                all_groups.append({
                    "term": g.canonical,
                    "aliases": g.aliases,
                    "category": g.category or meta.get("category", "other"),
                    "relevance_score": meta.get("relevance_score", 0.0),
                    "source_chunks": all_source_chunks,
                    "first_extraction_method": method,
                })

        except Exception as e:
            print(f"    [WARN] Dedup batch {batch_start}: {e}", file=sys.stderr)
            # Fallback: giữ nguyên từng term
            for t in batch_terms:
                meta = term_to_meta.get(t.lower().strip(), {"term": t})
                all_groups.append({
                    "term": t,
                    "aliases": [],
                    "category": meta.get("category", "other"),
                    "relevance_score": meta.get("relevance_score", 0.0),
                    "source_chunks": meta.get("source_chunks", []),
                    "first_extraction_method": meta.get("first_extraction_method", "unknown"),
                })

    return all_groups


# ─── Phase B: Omission Check ─────────────────────────────────────────────────

OMISSION_SYSTEM = """Bạn là người kiểm tra độ đầy đủ của danh sách thuật ngữ chuyên ngành.
Nhiệm vụ DUY NHẤT: Tìm các thuật ngữ liên quan đến chủ đề mục tiêu TRONG ĐOẠN VĂN mà CHƯA CÓ trong danh sách hiện tại.

QUAN TRỌNG:
- Chỉ thêm term thực sự LIÊN QUAN đến chủ đề mục tiêu
- KHÔNG thêm lại những gì đã có trong danh sách (kể cả alias)
- Nếu không tìm thấy gì mới, trả về new_terms = []
- Kiểm tra kỹ CẢ aliases, đừng thêm alias của term đã có"""


def build_current_terms_str(verified: list[dict]) -> str:
    """Tạo chuỗi danh sách term hiện có (gồm cả aliases) để nhét vào prompt."""
    lines = []
    for v in verified:
        aliases_str = f" (aliases: {', '.join(v['aliases'])})" if v.get("aliases") else ""
        lines.append(f"- {v['term']}{aliases_str}")
    return "\n".join(lines)


def omission_check_chunk(
    client: OpenAI,
    chunk: dict,
    target_context: str,
    current_terms_str: str,
    model: str,
) -> list[dict]:
    """Kiểm tra 1 chunk — trả về danh sách term mới (nếu có)."""
    user_prompt = f"""Chủ đề mục tiêu: "{target_context}"

Đoạn văn (heading: {chunk.get('heading_trail', '?')}):
---
{chunk['text']}
---

Danh sách thuật ngữ ĐÃ CÓ (bao gồm cả aliases):
{current_terms_str}

Có thuật ngữ nào liên quan đến chủ đề mục tiêu trong đoạn văn trên mà CHƯA có trong danh sách không?"""

    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": OMISSION_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            response_format=OmissionResponse,
            temperature=0.0,
        )
        result = completion.choices[0].message.parsed
        if result is None or not result.new_terms:
            return []
        return [
            {
                "term": t.term.strip(),
                "aliases": [],
                "category": t.category,
                "relevance_score": 0.0,
                "source_chunks": [chunk["chunk_id"]],
                "first_extraction_method": "omission_check",
            }
            for t in result.new_terms
            if t.term.strip()
        ]
    except Exception as e:
        print(f"    [WARN] omission chunk {chunk['chunk_id']}: {e}", file=sys.stderr)
        return []


# ─── Report ───────────────────────────────────────────────────────────────────

def write_verify_report(
    work_dir: Path,
    target_context: str,
    n_before_dedup: int,
    verified: list[dict],
    omission_rounds: list[dict],
) -> None:
    """Tạo verify-report.md — điểm duyệt người."""
    n_after = len(verified)
    n_from_omission = sum(
        1 for v in verified if v.get("first_extraction_method") == "omission_check"
    )
    n_statistical = sum(1 for v in verified if v.get("first_extraction_method") == "statistical")
    n_llm = sum(1 for v in verified if v.get("first_extraction_method") == "llm")

    lines = [
        f"# Verify Report — {target_context}",
        f"\n_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        "## Summary",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Trước dedup | {n_before_dedup} candidates |",
        f"| Sau dedup & canonicalize | {n_after} terms |",
        f"| Thêm từ omission-check | **{n_from_omission}** terms |",
        f"| method=statistical | {n_statistical} |",
        f"| method=llm | {n_llm} |",
        f"| method=omission_check | {n_from_omission} |",
        "",
        "## Omission Check Rounds",
    ]

    for i, rnd in enumerate(omission_rounds):
        lines.append(f"\n### Round {i+1}: +{rnd['delta']} terms")
        if rnd["new_terms"]:
            for t in rnd["new_terms"]:
                lines.append(f"- `{t['term']}` ({t.get('category','?')}) ← {', '.join(t['source_chunks'][:2])}")
        else:
            lines.append("_(không có term mới — dừng sớm)_")

    lines += [
        "",
        "## Final Keyword List (Preview top 50)",
        "| Term | Aliases | Category | Score | Method |",
        "|------|---------|----------|-------|--------|",
    ]
    for v in sorted(verified, key=lambda x: x.get("relevance_score", 0), reverse=True)[:50]:
        aliases = ", ".join(v.get("aliases", []))
        lines.append(
            f"| {v['term']} | {aliases} | {v.get('category','?')} | "
            f"{v.get('relevance_score', 0):.3f} | {v.get('first_extraction_method','?')} |"
        )
    if len(verified) > 50:
        lines.append(f"\n*... và {len(verified) - 50} term khác (xem keywords_verified.json)*")

    lines += [
        "",
        "---",
        "> **Hành động tiếp theo:** Xem xét danh sách trên. Nếu ổn, chạy `/finalize-keywords` để ghi output.",
    ]

    (work_dir / "verify-report.md").write_text("\n".join(lines), encoding="utf-8")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LLM verify, dedup, and omission-check")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--work-dir", help="Override .work/kw/ path")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model")
    parser.add_argument("--max-rounds", type=int, default=2, help="Max omission-check rounds (default: 2)")
    parser.add_argument("--dedup-batch", type=int, default=80, help="Dedup batch size (default: 80)")
    parser.add_argument("--target-context", help="Override target_context")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)
    work_dir = load_work_dir(args, repo_root)

    # Load data
    config = {}
    config_path = work_dir / "config.json"
    if config_path.is_file():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

    target_context = args.target_context or config.get("target_context", "")
    if not target_context:
        print("[ERROR] Cần target_context.", file=sys.stderr)
        sys.exit(1)

    filtered_path = work_dir / "candidates_filtered.json"
    if not filtered_path.is_file():
        print(f"[ERROR] Không tìm thấy candidates_filtered.json: {filtered_path}", file=sys.stderr)
        sys.exit(1)
    with open(filtered_path, encoding="utf-8") as f:
        candidates = json.load(f)

    chunks_path = work_dir / "chunks.json"
    if not chunks_path.is_file():
        print(f"[ERROR] Không tìm thấy chunks.json: {chunks_path}", file=sys.stderr)
        sys.exit(1)
    with open(chunks_path, encoding="utf-8") as f:
        chunks = json.load(f)

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY không tìm thấy.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    n_before_dedup = len(candidates)

    # ── Phase A: Dedup ────────────────────────────────────────────────────────
    print(f"\n=== Phase A: Dedup & Canonicalize ({n_before_dedup} candidates) ===")
    verified = dedup_candidates(client, candidates, model=args.model, batch_size=args.dedup_batch)
    print(f"  → {len(verified)} canonical terms sau dedup")

    # ── Phase B: Omission Check ───────────────────────────────────────────────
    print(f"\n=== Phase B: Omission Check (max {args.max_rounds} rounds) ===")
    omission_rounds = []

    for round_num in range(1, args.max_rounds + 1):
        print(f"\n  Round {round_num}/{args.max_rounds}:")
        current_terms_str = build_current_terms_str(verified)
        round_new_terms: list[dict] = []

        for i, chunk in enumerate(chunks):
            new_terms = omission_check_chunk(
                client, chunk, target_context, current_terms_str, model=args.model
            )
            if new_terms:
                print(f"    chunk_{i:04d}: +{len(new_terms)} terms: {[t['term'] for t in new_terms]}")
                # Merge vào verified ngay để vòng tiếp theo thấy
                verified.extend(new_terms)
                round_new_terms.extend(new_terms)
                # Update current_terms_str cho chunk tiếp trong cùng round
                current_terms_str = build_current_terms_str(verified)

        delta = len(round_new_terms)
        omission_rounds.append({"round": round_num, "delta": delta, "new_terms": round_new_terms})
        print(f"  Round {round_num}: +{delta} terms")

        if delta == 0:
            print(f"  → Không có term mới. Dừng sớm sau round {round_num}.")
            break

    # ── Ghi output ────────────────────────────────────────────────────────────
    out_path = work_dir / "keywords_verified.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(verified, f, ensure_ascii=False, indent=2)

    write_verify_report(work_dir, target_context, n_before_dedup, verified, omission_rounds)

    total_omission = sum(r["delta"] for r in omission_rounds)
    print(f"\n[✓] {len(verified)} keywords verified → {out_path}")
    print(f"[✓] Thêm từ omission-check: {total_omission} terms")
    print(f"[✓] verify-report.md → {work_dir / 'verify-report.md'}")
    print(f"\n→ Xem verify-report.md, rồi chạy /finalize-keywords")


if __name__ == "__main__":
    main()
