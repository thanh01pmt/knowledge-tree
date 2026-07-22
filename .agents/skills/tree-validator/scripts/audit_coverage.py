#!/usr/bin/env python3
"""
audit_coverage.py — Reverse Cross-Referencing Audit Tool
Đối chiếu ngược kết quả learning-objectives.tsv với tài liệu nguồn trong projects/<slug>/context/ hoặc .work/raw_pdf.txt.
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

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

def parse_pdf_sections(raw_pdf_path: Path) -> list:
    """Parses exact Objective Domains items from raw_pdf.txt dynamically."""
    sections = []
    if not raw_pdf_path.is_file():
        return sections

    with open(raw_pdf_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    current_domain = "General"

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue

        # Match objective numbers like '1.1.', '1.1.1.', '2.1.', '3.4.1.'
        match_obj = re.match(r"^(\d+\.\d+(\.\d+)?)\.?\s*(.*)", line_s)
        if match_obj:
            code_num = match_obj.group(1)
            title = match_obj.group(3)
            if title and len(title) > 3:
                sections.append({
                    "domain": current_domain,
                    "code": code_num,
                    "title": title
                })
        else:
            # Treat short unpunctuated non-page lines as dynamic domain headers
            if len(line_s) < 60 and not line_s.endswith(".") and not line_s.startswith("Page "):
                current_domain = line_s.replace(" (Continued)", "")

    return sections

def parse_context_audit(audit_path: Path) -> list:
    """Fallback: extracts topics/objectives from context-audit.md if raw_pdf.txt is missing."""
    sections = []
    if not audit_path.is_file():
        return sections

    with open(audit_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    current_domain = "General"
    item_counter = 1

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue

        if line_s.startswith(("#", "##", "###", "####")):
            header_text = line_s.lstrip("#").strip()
            if header_text.lower() not in ["context audit", "overview", "summary", "handoff", "inputs", "outputs"]:
                current_domain = header_text
            continue

        m_bullet = re.match(r"^[\*\-\+]\s*(.*)", line_s)
        m_num = re.match(r"^(\d+(\.\d+)*)\.?\s*(.*)", line_s)

        if m_bullet:
            title = m_bullet.group(1).strip()
            if len(title) > 5 and not title.startswith(("Goal:", "Inputs:", "Outputs:", "Process:")):
                sections.append({
                    "domain": current_domain,
                    "code": f"AUDIT-{item_counter}",
                    "title": title
                })
                item_counter += 1
        elif m_num:
            code_num = m_num.group(1)
            title = m_num.group(3).strip()
            if len(title) > 3:
                sections.append({
                    "domain": current_domain,
                    "code": code_num,
                    "title": title
                })
                item_counter += 1

    return sections

def audit_project_coverage(slug: str, repo_root: Path):
    proj_dir = repo_root / "projects" / slug
    work_dir = proj_dir / ".work"
    out_dir = proj_dir / "output"
    raw_pdf = work_dir / "raw_pdf.txt"
    context_audit = work_dir / "context-audit.md"
    lo_tsv = out_dir / "learning-objectives.tsv"

    if not lo_tsv.is_file():
        print(f"❌ Error: {lo_tsv} does not exist. Run /build-tree or assemble tree first.")
        sys.exit(1)

    # 1. Load LOs
    los = []
    with open(lo_tsv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            los.append(r)

    # 1b. Load project concepts (for Dimension 2 audit)
    project_concepts = []
    concepts_tsv = out_dir / "concepts.tsv"
    if concepts_tsv.is_file():
        with open(concepts_tsv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for r in reader:
                project_concepts.append(r)

    # 2. Extract sections from PDF or context-audit.md
    sections = parse_pdf_sections(raw_pdf)

    if not sections:
        sections = parse_context_audit(context_audit)

    if not sections:
        print(f"⚠️ Warning: No syllabus items found in {raw_pdf} or {context_audit}.")
        return

    # 3. Perform matching between Syllabus Sections and LOs
    lo_full_text = [
        f"{r['code']} {r['name']} {r['description']} {r.get('concept_codes','')}".lower()
        for r in los
    ]

    matched_sections = []
    missing_sections = []

    for sec in sections:
        keywords = [w.lower() for w in re.findall(r"\b[a-zA-Z]{3,}\b", sec["title"])]
        stop_words = {"and", "the", "for", "with", "use", "using", "create", "summarize", "assess", "differentiate", "select", "appropriate", "actions", "when", "how", "are"}
        keywords = [k for k in keywords if k not in stop_words]

        matches = []
        if keywords:
            for idx, text in enumerate(lo_full_text):
                matched_count = sum(1 for kw in keywords if kw in text)
                if matched_count >= 1:
                    matches.append(los[idx]["code"])

        if matches:
            matched_sections.append({
                "section": sec,
                "matched_los": list(dict.fromkeys(matches))[:4] # dedupe top 4
            })
        else:
            missing_sections.append(sec)

    total_sections = len(sections)
    covered_sections = len(matched_sections)
    coverage_score = round((covered_sections / total_sections) * 100, 2)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_dir = proj_dir / ".tree-validator" / "reports" / timestamp
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "coverage_report.md"

    # Save Markdown Report
    report_lines = [
        f"# Báo cáo Đối chiếu Ngược Độ Phủ Syllabus (Reverse Coverage Audit)",
        f"",
        f"- **Dự án:** `{slug}`",
        f"- **Thời gian kiểm tra:** {datetime.now(timezone.utc).isoformat()}",
        f"- **Tổng số mục Syllabus:** {total_sections}",
        f"- **Số mục đã phủ trong LO:** {covered_sections}",
        f"- **Số mục còn thiếu (Gaps):** {len(missing_sections)}",
        f"- **Độ phủ Syllabus (Coverage Score):** **{coverage_score}%**",
        f"- **Trạng thái:** {'✅ PASS' if coverage_score >= 95.0 else '⚠️ WARN / FAIL'}",
        f"",
        f"## Bảng đối chiếu đầy đủ (Syllabus vs Learning Objectives)",
        "| Domain | Mã Syllabus | Nội dung Syllabus | LOs phụ trách |",
        "|---|---|---|---|",
    ]

    for item in matched_sections:
        sec = item["section"]
        los_str = ", ".join([f"`{c}`" for c in item["matched_los"]])
        report_lines.append(f"| {sec['domain']} | `{sec['code']}` | {sec['title']} | {los_str} |")

    if missing_sections:
        report_lines.extend([
            "",
            "## ❌ Chi tiết các mục thiếu (Missing / Gap Items)",
            "| Domain | Mã | Nội dung Syllabus |",
            "|---|---|---|",
        ])
        for m in missing_sections:
            report_lines.append(f"| {m['domain']} | `{m['code']}` | {m['title']} |")
    else:
        report_lines.extend([
            "",
            "🎉 **Tất cả các mục trong Syllabus gốc đều đã được phủ đầy đủ 100%!**"
        ])

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    # ── Dimension 2: Concept Coverage ────────────────────────────────────────
    concept_covered: list[dict] = []
    concept_uncovered: list[dict] = []

    if project_concepts:
        lo_concept_coverage: dict[str, list[str]] = {}
        for lo in los:
            codes = [c.strip() for c in lo.get("concept_codes", "").replace(";", ",").split(",") if c.strip()]
            for c in codes:
                lo_concept_coverage.setdefault(c, []).append(lo["code"])

        for concept in project_concepts:
            code = (concept.get("code") or "").strip()
            if code:
                lo_list = lo_concept_coverage.get(code, [])
                entry = {"concept": concept, "code": code, "lo_codes": lo_list}
                if lo_list:
                    concept_covered.append(entry)
                else:
                    concept_uncovered.append(entry)

    # Append Dimension 2 to report
    d2_lines: list[str] = [
        "",
        "---",
        "",
        "## Chiều 2 — Concept Coverage (Concept → LO)",
        "",
        f"- **Tổng số Concepts:** {len(project_concepts)}",
        f"- **Concepts có LO:** {len(concept_covered)}",
        f"- **Concepts chưa có LO:** {len(concept_uncovered)}",
        "",
    ]
    if concept_uncovered:
        d2_lines += [
            "### ⚠️ Concepts chưa được phủ bởi LO nào",
            "",
            "| Code | Name |",
            "|---|---|",
        ]
        for e in concept_uncovered:
            d2_lines.append(f"| `{e['code']}` | {e['concept'].get('name','')} |")
        d2_lines.append("")
        d2_lines.append("**→ Action:** Thêm LO cho các concepts trên. Chạy `/detect-gaps` để có plan chi tiết.")
    else:
        d2_lines.append("✅ **Tất cả concepts đều có ít nhất 1 LO.**")

    d2_lines += [
        "",
        "### Bảng Concept → LOs",
        "",
        "| Concept | Name | LOs phụ trách |",
        "|---|---|---|",
    ]
    for e in concept_covered:
        lo_str = ", ".join(f"`{c}`" for c in e["lo_codes"][:4])
        if len(e["lo_codes"]) > 4:
            lo_str += f" ... (+{len(e['lo_codes'])-4} more)"
        d2_lines.append(f"| `{e['code']}` | {e['concept'].get('name','')} | {lo_str} |")

    full_report_lines = report_lines + d2_lines

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(full_report_lines))

    with open(work_dir / "coverage_audit.md", "w", encoding="utf-8") as f:
        f.write("\n".join(full_report_lines))

    print(f"==================================================")
    print(f"📊 REVERSE COVERAGE AUDIT RESULTS for '{slug}'")
    print(f"==================================================")
    print(f"  • Total Syllabus Items : {total_sections}")
    print(f"  • Covered Items        : {covered_sections}")
    print(f"  • Missing / Gaps       : {len(missing_sections)}")
    print(f"  • Coverage Score       : {coverage_score}%")
    print(f"  • Status               : {'PASS' if coverage_score >= 95.0 else 'FAIL'}")
    print(f"  • Report Path          : {report_file}")
    print(f"==================================================")

def main():
    parser = argparse.ArgumentParser(description="Audit Syllabus Coverage against Learning Objectives")
    parser.add_argument("--project", type=str, help="Project slug")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    slug = args.project
    if not slug:
        st = load_status(repo_root)
        slug = st.get("active_project", "swift-associate")

    audit_project_coverage(slug, repo_root)

if __name__ == "__main__":
    main()
