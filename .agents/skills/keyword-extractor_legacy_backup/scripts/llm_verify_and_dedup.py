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


def create_openai_client() -> OpenAI:
    """Tạo OpenAI client với timeout 60s, ưu tiên OPENAI_BASE_URL nếu có (Ollama compat)."""
    api_key = os.environ.get("OPENAI_API_KEY", "ollama")
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)
    if not api_key or api_key == "ollama":
        print("[ERROR] OPENAI_API_KEY hoặc OPENAI_BASE_URL chưa cấu hình.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, timeout=60.0)


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



DEDUP_SYSTEM = """Bạn là chuyên gia chuẩn hóa thuật ngữ kỹ thuật.
Nhóm các biến thể/alias của cùng một thuật ngữ thành một canonical form.

Quy tắc:
- Chọn dạng CANONICAL phổ biến/đúng nhất (VD: "ESP32-S3" không phải "esp32s3")
- KHÔNG gộp các thuật ngữ khác nghĩa dù embedding gần nhau (VD: "I2C" và "SPI" là khác nhau)
- Mỗi term trong input phải xuất hiện ĐÚNG MỘT LẦN trong output (là canonical HOẶC alias)
- Nếu term hoàn toàn độc lập, tạo group riêng với aliases = []

TRẢ LỜI BUỘC PHẢI LÀ JSON theo đúng schema (không thêm text giải thích):
{"groups": [{"canonical": "<term>", "aliases": ["<alias1>"], "category": "<hardware|software|protocol|concept|tool|other>"}]}"""


def parse_dedup_json(raw: str) -> list[dict]:
    """Parse JSON dedup response, hỗ trợ cả response gệ lệch."""
    import re
    text = raw.strip()
    fence = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if fence:
        text = fence.group(1).strip()
    obj = re.search(r'\{[\s\S]*\}', text)
    if not obj:
        return []
    try:
        data = json.loads(obj.group(0))
        return data.get("groups", [])
    except json.JSONDecodeError:
        return []


def dedup_candidates(client: OpenAI, candidates: list[dict], model: str, batch_size: int = 80) -> list[dict]:
    """Phase A: Gộp biến thể. Xử lý theo batch nếu list dài."""
    all_groups: list[dict] = []
    terms = [c["term"] for c in candidates]

    # Map term → candidate để giữ metadata
    term_to_meta: dict[str, dict] = {c["term"].lower().strip(): c for c in candidates}

    total_batches = (len(terms) + batch_size - 1) // batch_size
    print(f"  [A] Dedup {len(terms)} terms theo batch_size={batch_size} ({total_batches} batches) ...", flush=True)

    for batch_start in range(0, len(terms), batch_size):
        batch_num = (batch_start // batch_size) + 1
        batch_terms = terms[batch_start:batch_start + batch_size]
        print(f"    Batch [{batch_num}/{total_batches}] ({len(batch_terms)} terms) đang xử lý...", flush=True)
        term_list_str = "\n".join(f"- {t}" for t in batch_terms)
        user_prompt = f"Danh sách thuật ngữ cần nhóm:\n{term_list_str}"

        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": DEDUP_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
            )
            raw = completion.choices[0].message.content or ""
            groups = parse_dedup_json(raw)

            for g in groups:
                canonical = g.get("canonical", "").strip()
                if not canonical:
                    continue
                aliases = [a for a in g.get("aliases", []) if isinstance(a, str)]
                canonical_key = canonical.lower().strip()
                meta = term_to_meta.get(canonical_key, {})
                # Merge source_chunks từ tất cả aliases
                all_source_chunks = list(meta.get("source_chunks", []))
                for alias in aliases:
                    alias_meta = term_to_meta.get(alias.lower().strip(), {})
                    for sc in alias_meta.get("source_chunks", []):
                        if sc not in all_source_chunks:
                            all_source_chunks.append(sc)

                # first_extraction_method: ưu tiên "statistical" nếu có alias từ statistical
                method = meta.get("first_extraction_method", "llm")
                for alias in aliases:
                    alias_meta = term_to_meta.get(alias.lower().strip(), {})
                    if alias_meta.get("first_extraction_method") == "statistical":
                        method = "statistical"
                        break

                all_groups.append({
                    "term": canonical,
                    "aliases": aliases,
                    "category": g.get("category") or meta.get("category", "other"),
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


# ─── Phase B: Omission Check ───────────────────────────────────────────────────────────

OMISSION_SYSTEM = """Bạn là người kiểm tra độ đầy đủ của danh sách thuật ngữ chuyên ngành.
Nhiệm vụ DUY NHẤT: Tìm các thuật ngữ liên quan đến chủ đề mục tiêu TRONG ĐOẠN VĂN mà CHƯA CÓ trong danh sách hiện tại.

QUAN TRỌNG:
- Chỉ thêm term thực sự LIÊN QUAN đến chủ đề mục tiêu
- KHÔNG thêm lại những gì đã có trong danh sách (kể cả alias)
- Nếu không tìm thấy gì mới, trả về new_terms rỗng
- Kiểm tra kỹ CẢ aliases, đừng thêm alias của term đã có

TRẢ LỜI BUỘC PHẢI LÀ JSON theo đúng schema (không thêm text giải thích):
{"new_terms": [{"term": "<thuật ngữ mới>", "category": "<hardware|software|protocol|concept|tool|other>"}]}"""


def parse_omission_json(raw: str) -> list[dict]:
    """Parse JSON omission response."""
    import re
    text = raw.strip()
    fence = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if fence:
        text = fence.group(1).strip()
    obj = re.search(r'\{[\s\S]*\}', text)
    if not obj:
        return []
    try:
        data = json.loads(obj.group(0))
        return [
            {"term": t.get("term", "").strip(), "category": t.get("category", "other")}
            for t in data.get("new_terms", [])
            if isinstance(t, dict) and t.get("term", "").strip()
        ]
    except json.JSONDecodeError:
        return []


def build_current_terms_str(verified: list[dict]) -> str:
    """Tạo chuỗi danh sách term hiện có dạng compact để tối ưu kích thước prompt."""
    terms_list = []
    for v in verified:
        terms_list.append(v["term"])
        if v.get("aliases"):
            terms_list.extend(v["aliases"])
    return ", ".join(terms_list)


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

Hãy trả về JSON với các thuật ngữ chưa có trong danh sách (hoặc new_terms rỗng nếu không có)."""

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": OMISSION_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        raw = completion.choices[0].message.content or ""
        new_items = parse_omission_json(raw)
        return [
            {
                "term": t["term"],
                "aliases": [],
                "category": t["category"],
                "relevance_score": 0.0,
                "source_chunks": [chunk["chunk_id"]],
                "first_extraction_method": "omission_check",
            }
            for t in new_items
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
    parser.add_argument("--model", default=None, help="LLM model (default: ATE_MODEL env hoặc deepseek-v4-flash:cloud)")
    parser.add_argument("--max-rounds", type=int, default=2, help="Max omission-check rounds (default: 2)")
    parser.add_argument("--dedup-batch", type=int, default=30, help="Dedup batch size (default: 30)")
    parser.add_argument("--target-context", help="Override target_context")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)
    if not args.model:
        args.model = os.environ.get("ATE_MODEL", "deepseek-v4-flash:cloud")
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

    client = create_openai_client()
    n_before_dedup = len(candidates)

    # ── Phase A: Dedup ────────────────────────────────────────────────────────
    print(f"\n=== Phase A: Dedup & Canonicalize ({n_before_dedup} candidates) ===", flush=True)
    canonical_cache_path = work_dir / "candidates_canonical.json"
    if canonical_cache_path.is_file():
        with open(canonical_cache_path, encoding="utf-8") as f:
            verified = json.load(f)
        print(f"  [CACHE] Đã load {len(verified)} canonical terms từ candidates_canonical.json", flush=True)
    else:
        verified = dedup_candidates(client, candidates, model=args.model, batch_size=args.dedup_batch)
        with open(canonical_cache_path, "w", encoding="utf-8") as f:
            json.dump(verified, f, ensure_ascii=False, indent=2)
        print(f"  → {len(verified)} canonical terms sau dedup (đã lưu cache)", flush=True)

    # ── Phase B: Omission Check ───────────────────────────────────────────────
    print(f"\n=== Phase B: Omission Check (max {args.max_rounds} rounds) ===", flush=True)
    omission_rounds = []

    for round_num in range(1, args.max_rounds + 1):
        print(f"\n  Round {round_num}/{args.max_rounds}:", flush=True)
        current_terms_str = build_current_terms_str(verified)
        round_new_terms: list[dict] = []

        for i, chunk in enumerate(chunks):
            print(f"    [Round {round_num}] Đang check chunk_{i:04d} ({chunk['chunk_id']})...", flush=True)
            new_terms = omission_check_chunk(
                client, chunk, target_context, current_terms_str, model=args.model
            )
            if new_terms:
                print(f"      ↳ +{len(new_terms)} terms mới: {[t['term'] for t in new_terms]}", flush=True)
                # Merge vào verified ngay để vòng tiếp theo thấy
                verified.extend(new_terms)
                round_new_terms.extend(new_terms)
                # Update current_terms_str cho chunk tiếp trong cùng round
                current_terms_str = build_current_terms_str(verified)

        delta = len(round_new_terms)
        omission_rounds.append({"round": round_num, "delta": delta, "new_terms": round_new_terms})
        print(f"  Round {round_num}: +{delta} terms", flush=True)

        if delta == 0:
            print(f"  → Không có term mới. Dừng sớm sau round {round_num}.", flush=True)
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
