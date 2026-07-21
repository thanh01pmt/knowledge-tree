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
    """Parses exact Objective Domains items from raw_pdf.txt."""
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

        # Domain headers like 'Planning and Design', 'XCode Project Navigation', 'Swift Language Usage', 'View Building with SwiftUI', 'Debugging'
        if line_s in [
            "Planning and Design",
            "XCode Project Navigation",
            "Swift Language Usage",
            "Swift Language Usage (Continued)",
            "View Building with SwiftUI",
            "Debugging"
        ]:
            current_domain = line_s.replace(" (Continued)", "")
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

    return sections

def audit_project_coverage(slug: str, repo_root: Path):
    proj_dir = repo_root / "projects" / slug
    work_dir = proj_dir / ".work"
    out_dir = proj_dir / "output"
    raw_pdf = work_dir / "raw_pdf.txt"
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

    # 2. Extract sections from PDF
    sections = parse_pdf_sections(raw_pdf)

    # Fallback to context-audit if raw_pdf not found/parsed
    if not sections:
        sections = [
            {"domain": "Planning and Design", "code": "1.1", "title": "Design cycle (brainstorm, plan, prototype, evaluate)"},
            {"domain": "Planning and Design", "code": "1.2", "title": "Protect sensitive data and security challenges"},
            {"domain": "Planning and Design", "code": "1.3", "title": "Visual design with accessibility in mind"},
            {"domain": "Xcode Project Navigation", "code": "2.1", "title": "Differentiate basic file types"},
            {"domain": "Xcode Project Navigation", "code": "2.2", "title": "Import and use assets"},
            {"domain": "Xcode Project Navigation", "code": "2.4", "title": "Configure UI areas"},
            {"domain": "Swift Language Usage", "code": "3.1", "title": "Functions execution and argument labels"},
            {"domain": "Swift Language Usage", "code": "3.2", "title": "Calculate results with operators"},
            {"domain": "Swift Language Usage", "code": "3.3", "title": "Create and evaluate structures"},
            {"domain": "Swift Language Usage", "code": "3.4", "title": "Create and manipulate arrays"},
            {"domain": "Swift Language Usage", "code": "3.5", "title": "Control flow loops and conditionals"},
            {"domain": "Swift Language Usage", "code": "3.6", "title": "Constants, variables, and data types"},
            {"domain": "Swift Language Usage", "code": "3.7", "title": "Naming syntax and identifier rules"},
            {"domain": "View Building with SwiftUI", "code": "4.1", "title": "Imperative vs declarative programming"},
            {"domain": "View Building with SwiftUI", "code": "4.2", "title": "Create Content Views (Text, Image, Shape, Color)"},
            {"domain": "View Building with SwiftUI", "code": "4.3", "title": "Implement Modifiers"},
            {"domain": "View Building with SwiftUI", "code": "4.4", "title": "Create Container Views (Stacks)"},
            {"domain": "View Building with SwiftUI", "code": "4.5", "title": "View hierarchy"},
            {"domain": "View Building with SwiftUI", "code": "4.6", "title": "Interactive Views"},
            {"domain": "View Building with SwiftUI", "code": "4.7", "title": "@State Property Wrapper"},
            {"domain": "Debugging", "code": "5.1", "title": "Syntax vs run-time errors"},
            {"domain": "Debugging", "code": "5.2", "title": "Interpret error messages"}
        ]

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

    with open(work_dir / "coverage_audit.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

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
