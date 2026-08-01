#!/usr/bin/env python3
"""master_tree_parser.py — Shared parser for Master Knowledge Tree TSV.

Single source of truth for parsing the multi-table Master TSV format.
Used by: validate_master_tree.py, parse_master_tree.py, fix_master_tsv.py,
crawl_roadmap_align.py, and other scripts that need Master Tree data.
"""

import argparse
from pathlib import Path
from typing import Dict, List, Any


SECTIONS = {
    "Bảng 1": "fields",
    "Bảng 2": "subjects",
    "Bảng 3": "categories",
    "Bảng 4": "topics",
    "Bảng 5": "concepts",
    "Bảng 6": "learning_objectives",
}

# Lines to skip within table sections
SKIP_PREFIXES = (
    "Đây là",
    "Mỗi Field",
    "Các Subject",
    "Các Category",
    "Các Topic",
    "Các Concept",
)


def parse_master_tsv(tsv_path: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Parse the multi-table Master TSV into a dict of lists of row dicts.

    Returns dict with keys: fields, subjects, categories, topics, concepts,
    learning_objectives. Each value is a list of dicts mapping column headers
    to cell values.
    """
    data = {k: [] for k in SECTIONS.values()}
    current_level = None
    headers = []

    text = tsv_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue

        # Detect table boundaries
        hit = next((k for k in SECTIONS if s.startswith(k)), None)
        if hit:
            current_level = SECTIONS[hit]
            headers = []
            continue

        if not current_level or s.startswith(SKIP_PREFIXES):
            continue

        parts = line.rstrip("\n").split("\t")
        if parts[0] == "code":
            headers = [h.strip() for h in parts]
            continue

        if headers and parts[0].strip():
            row_dict = {}
            for i, header in enumerate(headers):
                val = parts[i].strip() if i < len(parts) else ""
                row_dict[header] = val
            data[current_level].append(row_dict)

    return data


def find_repo_root(start: Path) -> Path:
    """Find repository root by locating .agents directory."""
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def get_default_master_tsv_path() -> Path:
    """Return the default Master TSV path (source of truth)."""
    return find_repo_root(Path.cwd()) / "services/python-api/general-context/mlo-knowlege-tree.tsv"


if __name__ == "__main__":
    import json
    import sys

    ap = argparse.ArgumentParser(description="Parse Master TSV and output JSON")
    ap.add_argument("--input", type=str, default=str(get_default_master_tsv_path()))
    ap.add_argument("--output", type=str, default="master_tree.json")
    args = ap.parse_args()

    data = parse_master_tsv(Path(args.input))
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully parsed Master TSV and saved to {args.output}")
    print("Node counts:")
    for k, v in data.items():
        print(f"  {k}: {len(v)}")