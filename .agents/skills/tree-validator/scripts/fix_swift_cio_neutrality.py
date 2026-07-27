#!/usr/bin/env python3
"""
fix_swift_cio_neutrality.py — Rewrite CIO name/description in swift-associate
project to be technology-agnostic (T6 compliance).

Quy tắc:
- CIO = tầng Algorithmic (Marr) → KHÔNG chứa tên công nghệ.
- Thay "Swift" → "ngôn ngữ" (hoặc bỏ nếu context đã rõ).
- Thay "SwiftUI" → "framework UI khai báo" (lần đầu), "framework" (lần sau).
- Giữ nguyên code, lo_type, parent_lo_code, concept_codes, bloom_level,
  knowledge_dimension, assessment_approach.
- KHÔNG sửa ULO (đã trung tính) hay SIO (SIO được phép chứa tech).

Backup: tạo .bak.<date> trước khi ghi đè.
"""

import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
LO_PATH = REPO_ROOT / "projects/swift-associate/output/learning-objectives.tsv"


def neutralize_text(text: str) -> str:
    """Replace Swift/SwiftUI tokens with neutral equivalents."""
    if not text:
        return text
    # SwiftUI → "framework UI khai báo" (first occurrence) / "framework" (later)
    # Order matters: SwiftUI first (more specific), then Swift.
    text = re.sub(r'\bSwiftUI\b', 'framework UI khai báo', text, flags=re.IGNORECASE)
    # "Swift" standalone → "ngôn ngữ" (language-agnostic)
    # But avoid touching "SwiftUI" already replaced, and avoid "Swift's" possessive edge.
    text = re.sub(r'\bSwift\b(?!UI)', 'ngôn ngữ', text, flags=re.IGNORECASE)
    # Clean up double-spaces from replacements
    text = re.sub(r'\s{2,}', ' ', text)
    # Fix capitalization at sentence start: lowercase "ngôn ngữ" mid-sentence is fine,
    # but if it starts a sentence after ". " then capitalize.
    text = re.sub(r'\. ngôn ngữ', '. Ngôn ngữ', text)
    return text.strip()


def main():
    if not LO_PATH.is_file():
        print(f"❌ Not found: {LO_PATH}")
        return 1

    # Backup
    bak = LO_PATH.with_suffix(f".tsv.bak.{datetime.now().strftime('%Y%m%d')}")
    shutil.copy2(LO_PATH, bak)
    print(f"Backup → {bak.name}")

    with open(LO_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for r in rows:
        if r.get("lo_type") != "CONCEPTUAL_IMPL":
            continue
        name = r.get("name", "")
        desc = r.get("description", "")
        new_name = neutralize_text(name)
        new_desc = neutralize_text(desc)
        if new_name != name or new_desc != desc:
            r["name"] = new_name
            r["description"] = new_desc
            changed += 1

    with open(LO_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Neutralized {changed} CIO rows (Swift/SwiftUI → ngôn ngữ/framework)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())