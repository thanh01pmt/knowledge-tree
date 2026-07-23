#!/usr/bin/env python3
"""
tree_diff.py — Compare Staging Knowledge Tree (general-context/) vs Master Knowledge Tree (.agents/skills/...)
Outputs structural diff across Fields, Subjects, Categories, Topics, and Concepts.
"""

import sys
import json
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

def find_project_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
    return start.resolve().parent.parent.parent.parent

PROJECT_ROOT = find_project_root(SCRIPT_DIR)
MASTER_TSV_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
STAGING_TSV_PATH = PROJECT_ROOT / "general-context" / "mlo-knowlege-tree.tsv"
DIFF_REPORT_PATH = PROJECT_ROOT / ".work" / "tree_diff_report.md"

def ensure_staging_exists():
    """If staging TSV does not exist, copy from Master TSV"""
    if not STAGING_TSV_PATH.exists() and MASTER_TSV_PATH.exists():
        STAGING_TSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MASTER_TSV_PATH, STAGING_TSV_PATH)
        print(f"ℹ️ Auto-initialized staging TSV from Master Tree at {STAGING_TSV_PATH}")

def parse_sections(tsv_path: Path) -> dict:
    """Parse TSV into section dictionary keyed by section name (fields, subjects, categories, topics, concepts)"""
    sections = {
        "fields": {},
        "subjects": {},
        "categories": {},
        "topics": {},
        "concepts": {}
    }
    
    if not tsv_path.exists():
        return sections

    current_section = None
    with open(tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("Bảng 1"):
                current_section = "fields"
                continue
            elif line_str.startswith("Bảng 2"):
                current_section = "subjects"
                continue
            elif line_str.startswith("Bảng 3"):
                current_section = "categories"
                continue
            elif line_str.startswith("Bảng 4"):
                current_section = "topics"
                continue
            elif line_str.startswith("Bảng 5"):
                current_section = "concepts"
                continue

            if line_str.startswith("Đây là") or line_str.startswith("Mỗi Field") or line_str.startswith("code\t"):
                continue

            parts = line.rstrip("\r\n").split("\t")
            code = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else ""

            if code and current_section in sections:
                sections[current_section][code] = {
                    "code": code,
                    "name": name,
                    "raw_parts": parts
                }

    return sections

def diff_trees():
    ensure_staging_exists()
    
    master_sections = parse_sections(MASTER_TSV_PATH)
    staging_sections = parse_sections(STAGING_TSV_PATH)

    diff_summary = {}
    total_added = 0
    total_modified = 0
    total_removed = 0

    for section_name in ["fields", "subjects", "categories", "topics", "concepts"]:
        m_dict = master_sections[section_name]
        s_dict = staging_sections[section_name]

        m_codes = set(m_dict.keys())
        s_codes = set(s_dict.keys())

        added_codes = s_codes - m_codes
        removed_codes = m_codes - s_codes
        common_codes = m_codes.intersection(s_codes)

        modified_codes = []
        for c in common_codes:
            if m_dict[c]["raw_parts"] != s_dict[c]["raw_parts"]:
                modified_codes.append(c)

        diff_summary[section_name] = {
            "added": [s_dict[c] for c in added_codes],
            "modified": [{"code": c, "master": m_dict[c], "staging": s_dict[c]} for c in modified_codes],
            "removed": [m_dict[c] for c in removed_codes]
        }

        total_added += len(added_codes)
        total_modified += len(modified_codes)
        total_removed += len(removed_codes)

    DIFF_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DIFF_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Knowledge Tree Staging Diff Report\n\n")
        f.write(f"- **Staging Path:** `general-context/mlo-knowlege-tree.tsv`\n")
        f.write(f"- **Master Path:** `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv`\n")
        f.write(f"- **Total Added Nodes:** `{total_added}`\n")
        f.write(f"- **Total Modified Nodes:** `{total_modified}`\n")
        f.write(f"- **Total Removed Nodes:** `{total_removed}`\n\n")

        for sec in ["fields", "subjects", "categories", "topics", "concepts"]:
            sec_diff = diff_summary[sec]
            f.write(f"## 📊 Section: {sec.upper()}\n\n")

            if sec_diff["added"]:
                f.write("### 🟢 Added Nodes\n")
                for item in sec_diff["added"]:
                    f.write(f"- `{item['code']}`: **{item['name']}**\n")
                f.write("\n")

            if sec_diff["modified"]:
                f.write("### 🟡 Modified Nodes\n")
                for item in sec_diff["modified"]:
                    f.write(f"- `{item['code']}`:\n")
                    f.write(f"  - Master: `{item['master']['name']}`\n")
                    f.write(f"  - Staging: `{item['staging']['name']}`\n")
                f.write("\n")

            if sec_diff["removed"]:
                f.write("### 🔴 Removed Nodes\n")
                for item in sec_diff["removed"]:
                    f.write(f"- `{item['code']}`: **{item['name']}**\n")
                f.write("\n")

            if not sec_diff["added"] and not sec_diff["modified"] and not sec_diff["removed"]:
                f.write("*(No differences in this section)*\n\n")

    print(f"📊 Tree Diff Completed:")
    print(f"  - Added: {total_added}")
    print(f"  - Modified: {total_modified}")
    print(f"  - Removed: {total_removed}")
    print(f"📄 Diff report saved to: {DIFF_REPORT_PATH}")

if __name__ == "__main__":
    diff_trees()
