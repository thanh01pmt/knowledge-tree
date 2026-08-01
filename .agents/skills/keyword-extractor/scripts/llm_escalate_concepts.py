#!/usr/bin/env python3
"""
llm_escalate_concepts.py — Keyword → Concept Escalation.

Input:  output/keywords.tsv  (từ /finalize-keywords)
        general-context/mlo-knowlege-tree.tsv  (Master Tree — concepts section)
        [optional] output/concepts.tsv của project hiện tại

Output: output/concept_candidates.tsv
        .work/kw/concept_escalation.md  ← human review point

Pipeline 3 phase:
  Phase 1 — Abstraction (LLM):
    Group keywords theo concept trung tính (technology-agnostic).
    Ràng buộc: concept name/description KHÔNG chứa tên công nghệ cụ thể.
    Mapping là N:N: 1 keyword có thể thuộc nhiều concept; nhiều keywords → 1 concept.

  Phase 2 — Master Tree Matching (embedding cosine):
    Embed từng proposed concept + tất cả Master Tree concepts (batch, cache).
    Cosine >= threshold (default 0.80) → matched_master_code.
    Threshold cao (conservative) để tránh false-positive match.

  Phase 3 — Gap Detection:
    Concept không match → is_new_concept = True → Gap D candidate.
    Ghi vào concept_escalation.md với phân loại matched / new / ambiguous.
"""

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] Cài đặt: pip install openai pydantic", file=sys.stderr)
    sys.exit(1)


# ─── Models ───────────────────────────────────────────────────────────────────

class ConceptGroup(BaseModel):
    concept_name: str = Field(description=(
        "Tên khái niệm trung tính (technology-agnostic), tiếng Anh, danh từ/cụm danh từ ngắn gọn. "
        "TUYỆT ĐỐI KHÔNG chứa tên ngôn ngữ lập trình hay công nghệ cụ thể (Python, Swift, JS, Arduino...)."
    ))
    description_vi: str = Field(description=(
        "Mô tả ngắn bằng tiếng Việt (1-2 câu). "
        "Phải là khái niệm trung tính, áp dụng được cho ≥ 2 ngôn ngữ/công nghệ khác nhau."
    ))
    supporting_keywords: list[str] = Field(description=(
        "Danh sách keyword (từ input) là biểu hiện cụ thể của concept này. "
        "Mỗi keyword chỉ cần xuất hiện ở đây nếu nó thực sự minh họa cho concept này."
    ))


class EscalationResponse(BaseModel):
    concepts: list[ConceptGroup] = Field(
        description="Danh sách các concept trung tính được abstracted từ keywords. "
                    "Đảm bảo mỗi keyword quan trọng xuất hiện trong ít nhất 1 concept."
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


def get_active_project(args, repo_root: Path) -> str:
    if args.project:
        return args.project
    status_file = repo_root / "status.yaml"
    if status_file.is_file():
        for line in status_file.read_text().splitlines():
            if line.startswith("active_project"):
                return line.split(":", 1)[1].strip().strip("'\"")
    return ""


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def batch_embed(
    client: OpenAI,
    texts: list[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
) -> list[list[float]]:
    """Embed texts in batches with retry + error handling.
    Raises LLMCallError on failure."""
    import sys as _sys
    from pathlib import Path as _Path
    _skill_scripts = _Path(__file__).resolve().parent
    if str(_skill_scripts) not in _sys.path:
        _sys.path.insert(0, str(_skill_scripts))
    from llm_call import llm_embed as _llm_embed
    return _llm_embed(client, texts, model=model, batch_size=batch_size)


# ─── Load keywords ────────────────────────────────────────────────────────────

def load_keywords_tsv(keywords_tsv: Path) -> list[dict]:
    """Load output/keywords.tsv, trả về list dict."""
    if not keywords_tsv.is_file():
        return []
    keywords = []
    with open(keywords_tsv, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("term", "").strip():
                keywords.append({
                    "term": row["term"].strip(),
                    "aliases": [a.strip() for a in row.get("aliases", "").split("|") if a.strip()],
                    "category": row.get("category", "other").strip(),
                    "relevance_score": float(row.get("relevance_score", 0) or 0),
                    "first_extraction_method": row.get("first_extraction_method", "").strip(),
                })
    return keywords


# ─── Load Master Tree concepts ────────────────────────────────────────────────

def load_master_concepts(master_tsv: Path) -> list[dict]:
    """
    Đọc concepts từ mlo-knowlege-tree.tsv.
    Concepts bắt đầu sau dòng header "code\tname\tdescription\ttopic_codes\t..."
    (section cuối cùng trong file).
    """
    if not master_tsv.is_file():
        print(f"[WARN] Master Tree TSV không tìm thấy: {master_tsv}", file=sys.stderr)
        return []

    concepts = []
    in_concept_section = False

    with open(master_tsv, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        concept_header_seen = 0
        for row in reader:
            if not row or not row[0].strip():
                continue
            # Tìm header row của section concepts (có cột topic_codes)
            if row[0].strip() == "code" and len(row) >= 4 and "topic_codes" in row:
                concept_header_seen += 1
                in_concept_section = True
                continue
            if not in_concept_section:
                continue
            # Dừng nếu gặp header section mới
            if row[0].strip() == "code":
                in_concept_section = False
                continue

            code = row[0].strip()
            if not code:
                continue

            name = row[1].strip() if len(row) > 1 else ""
            description = row[2].strip() if len(row) > 2 else ""
            topic_codes = row[3].strip() if len(row) > 3 else ""
            keywords_str = row[4].strip() if len(row) > 4 else ""

            # Tạo rich text để embed: name + description + keywords
            embed_text = f"{name}. {description}. Keywords: {keywords_str}".strip()

            concepts.append({
                "code": code,
                "name": name,
                "description": description,
                "topic_codes": topic_codes,
                "keywords": keywords_str,
                "embed_text": embed_text,
            })

    return concepts


def load_project_concepts(project_concepts_tsv: Path) -> list[dict]:
    """Load output/concepts.tsv của project (nếu đã build-tree trước)."""
    if not project_concepts_tsv.is_file():
        return []
    concepts = []
    with open(project_concepts_tsv, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code = (row.get("code") or "").strip()
            name = (row.get("name") or "").strip()
            description = (row.get("description") or "").strip()
            if code and name:
                embed_text = f"{name}. {description}".strip()
                concepts.append({
                    "code": code,
                    "name": name,
                    "description": description,
                    "embed_text": embed_text,
                    "source": "project",
                })
    return concepts


# ─── Phase 1: LLM Abstraction ────────────────────────────────────────────────

ABSTRACTION_SYSTEM = """Bạn là chuyên gia thiết kế curriculum và taxonomy tri thức (Knowledge Engineering).

Nhiệm vụ: Từ danh sách keyword công nghệ-cụ thể, xác định các **khái niệm trung tính** (technology-agnostic concepts) ẩn đằng sau.

Nguyên tắc bắt buộc:
1. **Concept PHẢI technology-agnostic**: concept_name và description_vi TUYỆT ĐỐI không chứa tên công nghệ/ngôn ngữ cụ thể (Python, Swift, JavaScript, Arduino, ESP32, MQTT...).
   - ❌ Sai: "Khai báo biến trong Swift"
   - ✅ Đúng: "Khai báo biến"

2. **Marr Test**: Concept phải áp dụng được cho ít nhất 2 ngôn ngữ/công nghệ khác nhau. Nếu chỉ khớp với 1 ngôn ngữ → đó là SIO (implementation detail), không phải concept.

3. **Mapping N:N được phép**:
   - Nhiều keyword → 1 concept: `let` (JS), `var` (Python), `int x` (C) → concept "Khai báo biến"
   - 1 keyword → nhiều concept: `class` → "Định nghĩa Kiểu" VÀ "Đóng gói"

4. **Granularity phù hợp**: Không quá rộng ("Lập trình") cũng không quá hẹp ("Vòng lặp for với bước tăng 2").
   Ưu tiên granularity ở cấp "topic" trong một curriculum (VD: "Kiểu dữ liệu nguyên thủy", "Cấu trúc điều kiện", "Kết nối mạng không dây").

5. **Đủ phủ**: Đảm bảo mỗi keyword quan trọng (relevance_score cao) có mặt trong ít nhất 1 supporting_keywords."""


def escalate_keywords_to_concepts(
    client: OpenAI,
    keywords: list[dict],
    target_context: str,
    model: str = "gpt-4o",
    batch_size: int = 60,
) -> list[dict]:
    """Phase 1: LLM abstraction. Trả về list concept dicts."""
    all_concepts: list[dict] = []

    # Sort by relevance_score desc, ưu tiên terms quan trọng nhất vào batch đầu
    sorted_kws = sorted(keywords, key=lambda x: x.get("relevance_score", 0), reverse=True)

    for batch_start in range(0, len(sorted_kws), batch_size):
        batch = sorted_kws[batch_start : batch_start + batch_size]

        # Format input cho LLM: nhóm theo category để dễ đọc
        by_category: dict[str, list[str]] = {}
        for kw in batch:
            cat = kw.get("category", "other")
            by_category.setdefault(cat, []).append(kw["term"])

        kw_text_parts = []
        for cat, terms in sorted(by_category.items()):
            kw_text_parts.append(f"**{cat.upper()}**: {', '.join(terms)}")
        kw_text = "\n".join(kw_text_parts)

        user_prompt = (
            f'Chủ đề tài liệu: "{target_context}"\n\n'
            f"Danh sách keyword công nghệ-cụ thể:\n{kw_text}\n\n"
            "Hãy xác định các concept trung tính ẩn đằng sau các keywords trên."
        )

        print(f"  [1] Batch {batch_start+1}–{min(batch_start+batch_size, len(sorted_kws))}: "
              f"abstraction ({len(batch)} keywords) ...")

        try:
            completion = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": ABSTRACTION_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=EscalationResponse,
                temperature=0.2,
            )
            result = completion.choices[0].message.parsed
            if result is None:
                print(f"    [WARN] Batch {batch_start}: LLM returned None (parsed=False)",
                      file=sys.stderr)
                continue

            for cg in result.concepts:
                if not cg.concept_name.strip():
                    continue
                all_concepts.append({
                    "concept_name": cg.concept_name.strip(),
                    "description_vi": cg.description_vi.strip(),
                    "supporting_keywords": cg.supporting_keywords,
                })

        except Exception as e:
            # Classify error — retryable vs fatal
            import sys as _sys
            from pathlib import Path as _Path
            _skill_scripts = _Path(__file__).resolve().parent
            if str(_skill_scripts) not in _sys.path:
                _sys.path.insert(0, str(_skill_scripts))
            from llm_call import _classify_error
            error_type, retryable = _classify_error(e)
            print(f"    [FAIL] Abstraction batch {batch_start}: [{error_type}] {e}",
                  file=sys.stderr)
            if not retryable:
                # Fatal error (auth, model_not_found) — abort entire pipeline
                print(f"    [FATAL] Non-retryable error — aborting abstraction.", file=sys.stderr)
                raise

    # Dedup nhẹ bằng concept_name_lower
    seen: set[str] = set()
    deduped: list[dict] = []
    for c in all_concepts:
        key = c["concept_name"].lower().strip()
        if key not in seen:
            seen.add(key)
            deduped.append(c)
        else:
            # Gộp supporting_keywords vào entry đã có
            for existing in deduped:
                if existing["concept_name"].lower().strip() == key:
                    for kw in c["supporting_keywords"]:
                        if kw not in existing["supporting_keywords"]:
                            existing["supporting_keywords"].append(kw)
                    break

    return deduped


# ─── Phase 2: Master Tree Matching ───────────────────────────────────────────

def match_against_master(
    client: OpenAI,
    proposed_concepts: list[dict],
    master_concepts: list[dict],
    project_concepts: list[dict],
    match_threshold: float,
    embed_model: str,
    cache_path: Path,
) -> list[dict]:
    """
    Phase 2: Embed + cosine match.
    Thử project concepts trước, rồi master concepts.
    """
    if not master_concepts and not project_concepts:
        print("  [2] Không có Master Tree concepts để match. Bỏ qua Phase 2.")
        for c in proposed_concepts:
            c.update({
                "matched_master_code": "",
                "matched_master_name": "",
                "match_confidence": 0.0,
                "match_source": "",
                "is_new_concept": True,
            })
        return proposed_concepts

    all_reference_concepts = project_concepts + master_concepts
    ref_texts = [c["embed_text"] for c in all_reference_concepts]

    # Cache embeddings để tránh re-embed Master Tree mỗi lần chạy
    cache: dict[str, list[float]] = {}
    if cache_path.is_file():
        try:
            with open(cache_path, encoding="utf-8") as f:
                cache = json.load(f)
            print(f"  [2] Loaded {len(cache)} cached master embeddings")
        except Exception:
            cache = {}

    # Embed reference concepts (từ cache hoặc API)
    ref_embeddings: list[list[float]] = []
    to_embed_indices: list[int] = []
    to_embed_texts: list[str] = []

    for i, text in enumerate(ref_texts):
        key = hashlib.sha256(text.encode()).hexdigest()[:32]
        if key in cache:
            ref_embeddings.append(cache[key])
        else:
            ref_embeddings.append([])  # placeholder
            to_embed_indices.append(i)
            to_embed_texts.append(text)

    if to_embed_texts:
        print(f"  [2] Embedding {len(to_embed_texts)} new reference concepts ...")
        new_embeddings = batch_embed(client, to_embed_texts, model=embed_model)
        for idx, emb in zip(to_embed_indices, new_embeddings):
            ref_embeddings[idx] = emb
            key = hashlib.sha256(ref_texts[idx].encode()).hexdigest()[:32]
            cache[key] = emb

        # Update cache
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f)

    # Embed proposed concepts
    proposed_texts = [
        f"{c['concept_name']}. {c['description_vi']}"
        for c in proposed_concepts
    ]
    print(f"  [2] Embedding {len(proposed_texts)} proposed concepts ...")
    proposed_embeddings = batch_embed(client, proposed_texts, model=embed_model)

    # Match
    for c, p_emb in zip(proposed_concepts, proposed_embeddings):
        best_score = 0.0
        best_ref = None

        for ref_c, r_emb in zip(all_reference_concepts, ref_embeddings):
            if not r_emb:
                continue
            score = cosine_similarity(p_emb, r_emb)
            if score > best_score:
                best_score = score
                best_ref = ref_c

        if best_ref and best_score >= match_threshold:
            c["matched_master_code"] = best_ref["code"]
            c["matched_master_name"] = best_ref["name"]
            c["match_confidence"] = round(best_score, 4)
            c["match_source"] = best_ref.get("source", "master")
            c["is_new_concept"] = False
        else:
            c["matched_master_code"] = ""
            c["matched_master_name"] = ""
            c["match_confidence"] = round(best_score, 4) if best_ref else 0.0
            c["match_source"] = ""
            c["is_new_concept"] = True

    return proposed_concepts


# ─── Phase 3: Report ──────────────────────────────────────────────────────────

def write_escalation_report(
    report_path: Path,
    concepts: list[dict],
    target_context: str,
    match_threshold: float,
) -> None:
    matched = [c for c in concepts if not c["is_new_concept"]]
    new_concepts = [c for c in concepts if c["is_new_concept"]]
    ambiguous = [
        c for c in concepts
        if not c["is_new_concept"] and c["match_confidence"] < match_threshold + 0.05
    ]

    lines = [
        f"# Concept Escalation Report — {target_context}",
        f"\n_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        f"_Match threshold: {match_threshold}_\n",

        "## Summary",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Tổng concept đề xuất | {len(concepts)} |",
        f"| Matched Master Tree | **{len(matched)}** |",
        f"| **Concept mới (Gap D)** | **{len(new_concepts)}** |",
        f"| Cần xem thêm (low confidence) | {len(ambiguous)} |",
        "",

        "## ✅ Matched — có trong Master Tree",
        "| Concept đề xuất | Master Code | Master Name | Confidence | Keywords |",
        "|-----------------|-------------|-------------|-----------|----------|",
    ]
    for c in sorted(matched, key=lambda x: x["match_confidence"], reverse=True):
        kws = ", ".join(c.get("supporting_keywords", [])[:5])
        lines.append(
            f"| {c['concept_name']} | `{c['matched_master_code']}` | "
            f"{c['matched_master_name']} | {c['match_confidence']:.3f} | {kws} |"
        )

    if new_concepts:
        lines += [
            "",
            "## 🆕 Concept Mới (Gap D — chưa có trong Master Tree)",
            "> Những concept này là ứng viên để bổ sung vào Master Knowledge Tree.",
            "| Concept đề xuất | Mô tả | Keywords |",
            "|-----------------|-------|----------|",
        ]
        for c in new_concepts:
            kws = ", ".join(c.get("supporting_keywords", [])[:5])
            lines.append(
                f"| **{c['concept_name']}** | {c['description_vi']} | {kws} |"
            )

    if ambiguous:
        lines += [
            "",
            f"## ⚠️ Cần Xem Lại (confidence < {match_threshold + 0.05:.2f})",
            "| Concept đề xuất | Best Match | Confidence |",
            "|-----------------|------------|-----------|",
        ]
        for c in ambiguous:
            lines.append(
                f"| {c['concept_name']} | {c['matched_master_name']} ({c['matched_master_code']}) "
                f"| {c['match_confidence']:.3f} |"
            )

    lines += [
        "",
        "## Keyword → Concept Map (đầy đủ)",
        "| Keyword | Concept(s) |",
        "|---------|------------|",
    ]
    # Build reverse map: keyword → list[concept_name]
    kw_to_concepts: dict[str, list[str]] = {}
    for c in concepts:
        for kw in c.get("supporting_keywords", []):
            kw_to_concepts.setdefault(kw.lower(), []).append(c["concept_name"])
    for kw, concept_names in sorted(kw_to_concepts.items()):
        lines.append(f"| `{kw}` | {', '.join(concept_names)} |")

    lines += [
        "",
        "---",
        "> **Hành động tiếp theo:**",
        "> - Nếu OK → chạy `/map-taxonomy` (sẽ đọc `output/concept_candidates.tsv` làm hints)",
        "> - Với Gap D concepts → cân nhắc thêm vào Master Tree trước khi `/map-taxonomy`",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_concept_candidates_tsv(out_path: Path, concepts: list[dict]) -> None:
    fieldnames = [
        "concept_name", "description_vi", "matched_master_code",
        "matched_master_name", "match_confidence", "match_source",
        "is_new_concept", "supporting_keywords",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for c in concepts:
            writer.writerow({
                **c,
                "supporting_keywords": "|".join(c.get("supporting_keywords", [])),
                "is_new_concept": str(c.get("is_new_concept", True)),
            })


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Escalate keywords → technology-agnostic concepts + match Master Tree"
    )
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--work-dir", help="Override .work/kw/ path")
    parser.add_argument(
        "--master-tsv",
        help="Path đến Master Tree TSV (default: general-context/mlo-knowlege-tree.tsv)",
    )
    parser.add_argument(
        "--match-threshold",
        type=float,
        default=0.80,
        help="Cosine threshold để match Master Tree (default: 0.80 — conservative)",
    )
    parser.add_argument(
        "--embed-model",
        default="text-embedding-3-small",
        help="OpenAI embedding model",
    )
    parser.add_argument(
        "--llm-model",
        default="gpt-4o",
        help="OpenAI LLM model cho abstraction (default: gpt-4o — cần reasoning tốt)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=60,
        help="Số keywords mỗi LLM call (default: 60)",
    )
    parser.add_argument("--target-context", help="Override target_context từ config.json")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)

    work_dir = load_work_dir(args, repo_root)
    project = get_active_project(args, repo_root)

    # Resolve paths
    if project:
        out_dir = repo_root / "projects" / project / "output"
        project_concepts_tsv = out_dir / "concepts.tsv"
    else:
        out_dir = repo_root / "output"
        project_concepts_tsv = Path("/nonexistent")

    master_tsv_path = Path(args.master_tsv) if args.master_tsv else (
        repo_root / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"
    )
    embed_cache_path = work_dir / "master_embed_cache.json"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load target_context
    config = {}
    config_path = work_dir / "config.json"
    if config_path.is_file():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    target_context = args.target_context or config.get("target_context", "")
    if not target_context:
        print("[ERROR] Cần target_context. Chạy /scaffold-keywords trước.", file=sys.stderr)
        sys.exit(1)

    # Load keywords
    keywords_tsv = out_dir / "keywords.tsv"
    if not keywords_tsv.is_file():
        print(f"[ERROR] Không tìm thấy keywords.tsv: {keywords_tsv}", file=sys.stderr)
        print("Chạy /finalize-keywords trước.", file=sys.stderr)
        sys.exit(1)
    keywords = load_keywords_tsv(keywords_tsv)
    print(f"[*] Loaded {len(keywords)} keywords từ {keywords_tsv}")

    # Load Master Tree concepts
    master_concepts = load_master_concepts(master_tsv_path)
    print(f"[*] Loaded {len(master_concepts)} Master Tree concepts từ {master_tsv_path.name}")

    # Load project concepts (optional — nếu đã build-tree)
    project_concepts = load_project_concepts(project_concepts_tsv)
    if project_concepts:
        print(f"[*] Loaded {len(project_concepts)} project concepts từ {project_concepts_tsv.name}")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY không tìm thấy.", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    # ── Phase 1: Abstraction ──────────────────────────────────────────────────
    print(f"\n=== Phase 1: LLM Abstraction ({len(keywords)} keywords → concepts) ===")
    proposed_concepts = escalate_keywords_to_concepts(
        client, keywords, target_context,
        model=args.llm_model,
        batch_size=args.batch_size,
    )
    print(f"  → {len(proposed_concepts)} concept candidates sau abstraction")

    # ── Phase 2: Master Tree Matching ─────────────────────────────────────────
    print(f"\n=== Phase 2: Master Tree Matching (threshold={args.match_threshold}) ===")
    matched_concepts = match_against_master(
        client, proposed_concepts,
        master_concepts, project_concepts,
        match_threshold=args.match_threshold,
        embed_model=args.embed_model,
        cache_path=embed_cache_path,
    )

    n_matched = sum(1 for c in matched_concepts if not c["is_new_concept"])
    n_new = sum(1 for c in matched_concepts if c["is_new_concept"])
    print(f"  → Matched: {n_matched} | New (Gap D): {n_new}")

    # ── Phase 3: Output ───────────────────────────────────────────────────────
    print(f"\n=== Phase 3: Writing Output ===")

    # TSV output
    tsv_out = out_dir / "concept_candidates.tsv"
    write_concept_candidates_tsv(tsv_out, matched_concepts)
    print(f"[✓] concept_candidates.tsv → {tsv_out}")

    # JSON output (cho downstream use)
    json_out = out_dir / "concept_candidates.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(matched_concepts, f, ensure_ascii=False, indent=2)
    print(f"[✓] concept_candidates.json → {json_out}")

    # Human review report
    report_path = work_dir / "concept_escalation.md"
    write_escalation_report(report_path, matched_concepts, target_context, args.match_threshold)
    print(f"[✓] concept_escalation.md → {report_path}")

    print(f"\n{'='*60}")
    print(f"Tổng: {len(matched_concepts)} concepts | Matched: {n_matched} | Gap D: {n_new}")
    print(f"\n→ Đọc .work/kw/concept_escalation.md để review trước khi /map-taxonomy")


if __name__ == "__main__":
    main()
