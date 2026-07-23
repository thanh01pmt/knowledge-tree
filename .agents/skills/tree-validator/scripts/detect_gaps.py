#!/usr/bin/env python3
"""
detect_gaps.py — Gap Detection Tool cho Knowledge Tree.

Phát hiện 3 loại gap:
  Gap A (CONCEPT_WITHOUT_LO):  Concept trong project chưa có LO nào trỏ đến.
  Gap B (CIO_SHALLOW):         CIO có ít hơn 2 SIO con → phân rã chưa đủ sâu.
  Gap C (MASTER_CANDIDATE):    Concept từ master_tree.json liên quan đến syllabus
                                nhưng chưa được đưa vào project taxonomy.

Chạy: python3 detect_gaps.py --project <slug>
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─── Helpers ─────────────────────────────────────────────────────────────────

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_status(repo_root: Path) -> dict:
    status_file = repo_root / "status.yaml"
    res = {}
    if status_file.is_file():
        with open(status_file, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line and not line.strip().startswith("#"):
                    k, v = line.split(":", 1)
                    res[k.strip()] = v.strip().strip("'\"")
    return res


def load_tsv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def split_codes(value: str) -> list[str]:
    if not value:
        return []
    return [c.strip() for c in value.replace(";", ",").split(",") if c.strip()]


def load_syllabus_text(work_dir: Path) -> str:
    """Load raw syllabus text for keyword matching."""
    for fname in ("raw_pdf.txt", "context-audit.md"):
        p = work_dir / fname
        if p.is_file():
            return p.read_text(encoding="utf-8").lower()
    return ""


STOP_WORDS = {
    "and", "the", "for", "with", "use", "using", "create", "summarize",
    "assess", "differentiate", "select", "appropriate", "actions", "when",
    "how", "are", "from", "that", "this", "will", "have", "not", "but",
    "can", "its", "also", "into", "such", "each", "than", "more", "over",
}


def keyword_score(concept: dict, syllabus_text: str) -> tuple[float, list[str]]:
    """Score a master concept's relevance to syllabus text. Returns (score, hits)."""
    name_words = [w.lower() for w in re.findall(r"[a-zA-Z]{3,}", concept.get("name", ""))]
    kw_words = [k.strip().lower() for k in concept.get("keywords", "").split(",") if k.strip()]
    desc_words = [w.lower() for w in re.findall(r"[a-zA-Z]{4,}", concept.get("description", ""))]

    score = 0.0
    hits = []

    for kw in kw_words:
        if len(kw) > 3 and kw not in STOP_WORDS and kw in syllabus_text:
            score += 1.5
            hits.append(kw)

    for w in name_words:
        if len(w) > 3 and w not in STOP_WORDS and w in syllabus_text:
            score += 0.8
            if w not in hits:
                hits.append(w)

    for w in desc_words[:10]:
        if w not in STOP_WORDS and w in syllabus_text:
            score += 0.3

    return round(score, 2), hits[:6]


# ─── Gap A: Concepts without LOs ─────────────────────────────────────────────

def detect_concept_without_lo(
    project_concepts: list[dict],
    project_los: list[dict],
) -> list[dict]:
    """Return concepts that no LO points to."""
    covered = set()
    for lo in project_los:
        for c in split_codes(lo.get("concept_codes", "")):
            covered.add(c)

    gaps = []
    for concept in project_concepts:
        code = (concept.get("code") or "").strip()
        if code and code not in covered:
            gaps.append({
                "code": code,
                "name": concept.get("name", ""),
                "topic_codes": concept.get("topic_codes", ""),
            })
    return gaps


# ─── Gap B: CIOs with fewer than 2 SIOs ──────────────────────────────────────

def detect_shallow_cios(project_los: list[dict], min_sios: int = 2) -> list[dict]:
    """Return CIOs with fewer than min_sios SIO children."""
    cios = {r["code"]: r for r in project_los if r.get("lo_type") == "CONCEPTUAL_IMPL" and r.get("code")}
    sios = [r for r in project_los if r.get("lo_type") == "SPECIFIC_IMPL"]

    cio_sio_count: dict[str, int] = {c: 0 for c in cios}
    for sio in sios:
        parent = (sio.get("parent_lo_code") or "").strip()
        if parent in cio_sio_count:
            cio_sio_count[parent] += 1

    shallow = []
    for cio_code, count in cio_sio_count.items():
        if count < min_sios:
            shallow.append({
                "code": cio_code,
                "name": cios[cio_code].get("name", ""),
                "sio_count": count,
                "parent_ulo": (cios[cio_code].get("parent_lo_code") or "").strip(),
            })
    return shallow


# ─── Gap D: CIOs violating Marr's Representation-Independent test ─────────────

TECH_KEYWORDS = {
    "python", "swift", "javascript", "typescript", "java", "golang", "c++",
    "class", "def", "func", "function", "var", "let", "struct", "import", "enum"
}

def detect_non_neutral_cios(project_los: list[dict]) -> list[dict]:
    """Return CIOs containing technology/syntax-specific tokens violating Marr's test."""
    cios = [r for r in project_los if r.get("lo_type") == "CONCEPTUAL_IMPL"]
    violations = []
    for cio in cios:
        text = (cio.get("name", "") + " " + cio.get("description", "")).lower()
        found_kw = [kw for kw in TECH_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', text)]
        if found_kw:
            violations.append({
                "code": cio.get("code", ""),
                "name": cio.get("name", ""),
                "keywords": found_kw
            })
    return violations


# ─── Gap C: Master Tree Candidates ───────────────────────────────────────────

def detect_master_candidates(
    master_concepts: list[dict],
    project_concept_codes: set[str],
    syllabus_text: str,
    min_score: float = 2.0,
    top_n: int = 20,
) -> list[dict]:
    """Return master concepts not in project but relevant to syllabus."""
    candidates = []
    for concept in master_concepts:
        code = (concept.get("code") or "").strip()
        if not code or code in project_concept_codes:
            continue
        score, hits = keyword_score(concept, syllabus_text)
        if score >= min_score:
            candidates.append({
                "code": code,
                "name": concept.get("name", ""),
                "description": concept.get("description", ""),
                "topic_codes": concept.get("topic_codes", ""),
                "score": score,
                "matching_keywords": hits,
            })

    candidates.sort(key=lambda x: -x["score"])
    return candidates[:top_n]


# ─── Report Rendering ─────────────────────────────────────────────────────────

def render_report(
    slug: str,
    gap_a: list[dict],
    gap_b: list[dict],
    gap_c: list[dict],
    min_score: float,
) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Gap Detection Report",
        "",
        f"- **Project:** `{slug}`",
        f"- **Generated:** {now}",
        "",
        "---",
        "",
        "## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)",
        "",
        f"> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.",
        "",
    ]

    if gap_a:
        lines += [
            f"**{len(gap_a)} concept(s) không có LO:**",
            "",
            "| Code | Name | Parent Topic |",
            "|---|---|---|",
        ]
        for g in gap_a:
            lines.append(f"| `{g['code']}` | {g['name']} | `{g['topic_codes']}` |")
        lines.append("")
        lines.append("**→ Action:** Thêm ít nhất 1 ULO + 1 CIO + 2 SIO cho mỗi concept trên.")
    else:
        lines += ["✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**", ""]

    lines += [
        "---",
        "",
        "## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)",
        "",
        "> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.",
        "",
    ]

    if gap_b:
        lines += [
            f"**{len(gap_b)} CIO(s) có < 2 SIO:**",
            "",
            "| CIO Code | CIO Name | SIO Count | Parent ULO |",
            "|---|---|---|---|",
        ]
        for g in gap_b:
            sio_display = f"{'⚠️ ' if g['sio_count'] == 1 else '❌ '}{g['sio_count']}"
            lines.append(f"| `{g['code']}` | {g['name']} | {sio_display} | `{g['parent_ulo']}` |")
        lines.append("")
        lines.append("**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.")
    else:
        lines += ["✅ **Tất cả CIOs đều có ít nhất 2 SIO con.**", ""]

    lines += [
        "---",
        "",
        "## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)",
        "",
        f"> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ {min_score}).",
        "> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.",
        "",
    ]

    if gap_c:
        lines += [
            f"**{len(gap_c)} candidate(s) từ Master Tree:**",
            "",
            "| Score | Code | Name | Matching Keywords |",
            "|---|---|---|---|",
        ]
        for g in gap_c:
            kws = ", ".join(f"`{k}`" for k in g["matching_keywords"])
            lines.append(f"| {g['score']} | `{g['code']}` | {g['name']} | {kws} |")
        lines.append("")
        lines.append(
            "**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`."
        )
    else:
        lines += [f"✅ **Không tìm thấy master concept nào có score ≥ {min_score} chưa được chọn.**", ""]

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Detect 3 types of gaps in the project Knowledge Tree."
    )
    parser.add_argument("--project", type=str, help="Project slug")
    parser.add_argument(
        "--min-score", type=float, default=2.0,
        help="Minimum keyword score for Master Candidate detection (default: 2.0)"
    )
    parser.add_argument(
        "--top-n", type=int, default=20,
        help="Max number of master candidates to report (default: 20)"
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())

    slug = args.project
    if not slug:
        st = load_status(repo_root)
        slug = st.get("active_project")
        if not slug:
            print("❌ Error: Không có project. Truyền --project hoặc set active_project trong status.yaml.")
            sys.exit(1)

    project_dir = repo_root / "projects" / slug
    out_dir = project_dir / "output"
    work_dir = project_dir / ".work"
    master_json = repo_root / ".agents/skills/taxonomy-mapper/resources/master_tree.json"

    # Load data
    project_concepts = load_tsv(out_dir / "concepts.tsv")
    project_los = load_tsv(out_dir / "learning-objectives.tsv")

    if not project_concepts:
        print(f"⚠️  concepts.tsv không tìm thấy. Chạy /build-tree trước.")
    if not project_los:
        print(f"⚠️  learning-objectives.tsv không tìm thấy. Chạy /generate-los trước.")

    master_concepts = []
    if master_json.is_file():
        with open(master_json, "r", encoding="utf-8") as f:
            master = json.load(f)
        master_concepts = master.get("concepts", [])

    syllabus_text = load_syllabus_text(work_dir)
    if not syllabus_text:
        print("⚠️  Syllabus text không tìm thấy. Gap C sẽ không có kết quả.")

    project_concept_codes = {(r.get("code") or "").strip() for r in project_concepts}

    # Detect gaps
    gap_a = detect_concept_without_lo(project_concepts, project_los)
    gap_b = detect_shallow_cios(project_los, min_sios=2)
    gap_d = detect_non_neutral_cios(project_los)
    gap_c = detect_master_candidates(
        master_concepts, project_concept_codes, syllabus_text,
        min_score=args.min_score, top_n=args.top_n
    )

    # Print summary
    print(f"\n{'='*54}")
    print(f"🔍 GAP DETECTION RESULTS for '{slug}'")
    print(f"{'='*54}")
    status_a = "❌" if gap_a else "✅"
    status_b = "⚠️ " if gap_b else "✅"
    status_d = "❌" if gap_d else "✅"
    status_c = "ℹ️ " if gap_c else "✅"
    print(f"  {status_a} Gap A (Concepts without LO):       {len(gap_a)}")
    if gap_a:
        for g in gap_a:
            print(f"       • {g['code']}: {g['name']}")
    print(f"  {status_b} Gap B (Shallow CIOs < 2 SIO):      {len(gap_b)}")
    if gap_b:
        for g in gap_b:
            print(f"       • {g['code']} ({g['sio_count']} SIO)")
    print(f"  {status_d} Gap D (Marr Test Violated CIOs): {len(gap_d)}")
    if gap_d:
        for g in gap_d:
            print(f"       • {g['code']}: contains {', '.join(g['keywords'])}")
    print(f"  {status_c} Gap C (Master Candidates):         {len(gap_c)}")

    if gap_c:
        for g in gap_c[:5]:
            print(f"       • [{g['score']}] {g['code']}: {g['name']}")
        if len(gap_c) > 5:
            print(f"       ... và {len(gap_c) - 5} candidate(s) khác (xem report)")
    print(f"{'='*54}")

    # Write reports
    report_content = render_report(slug, gap_a, gap_b, gap_c, args.min_score)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_dir = project_dir / ".tree-validator" / "reports" / stamp
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "gap_report.md"
    work_copy = work_dir / "gap_report.md"
    report_path.write_text(report_content, encoding="utf-8")
    work_dir.mkdir(parents=True, exist_ok=True)
    work_copy.write_text(report_content, encoding="utf-8")

    print(f"\n  • Report: {report_path.relative_to(repo_root)}")
    print(f"  • Work copy: {work_copy.relative_to(repo_root)}")
    print(f"{'='*54}\n")


if __name__ == "__main__":
    main()
