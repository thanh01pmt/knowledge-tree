#!/usr/bin/env python3
"""validate_master_tree.py — referential integrity + cross-level collision +
"level-skip" checks for the Master Knowledge Tree itself."""

import argparse
import sys
from pathlib import Path

SECTIONS = {
    "Bảng 1": "fields",
    "Bảng 2": "subjects",
    "Bảng 3": "categories",
    "Bảng 4": "topics",
    "Bảng 5": "concepts",
}


def parse(tsv_path: Path):
    tables = {v: [] for v in SECTIONS.values()}
    section, headers = None, []
    for line in tsv_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s:
            continue
        hit = next((k for k in SECTIONS if s.startswith(k)), None)
        if hit:
            section, headers = SECTIONS[hit], []
            continue
        if not section or s.startswith(("Đây là", "Mỗi Field", "Các Subject", "Các Category", "Các Topic", "Các Concept")):
            continue
        parts = line.rstrip("\n").split("\t")
        if parts[0] == "code":
            headers = [h.strip() for h in parts]
            continue
        if headers and parts[0].strip():
            tables[section].append(dict(zip(headers, parts)))
    return tables


def split(v):
    return [c.strip() for c in (v or "").replace(";", ",").replace("|", ",").split(",") if c.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", default="general-context/mlo-knowlege-tree.tsv")
    args = ap.parse_args()
    tsv_path = Path(args.tsv)
    if not tsv_path.is_file():
        print(f"❌ File not found: {tsv_path}")
        sys.exit(1)

    tables = parse(tsv_path)

    order = ["fields", "subjects", "categories", "topics", "concepts"]
    parent_field = {
        "subjects": "field_codes",
        "categories": "subject_codes",
        "topics": "category_codes",
        "concepts": "topic_codes",
    }
    parent_level = {
        "subjects": "fields",
        "categories": "subjects",
        "topics": "categories",
        "concepts": "topics",
    }
    grandparent_level = {"topics": "subjects", "concepts": "categories"}
    codes = {lvl: {r["code"].strip() for r in tables[lvl]} for lvl in order}

    errors, warnings = [], []
    owner = {}
    for lvl in order:
        for row in tables[lvl]:
            c = row["code"].strip()
            if c in owner and owner[c] != lvl:
                errors.append(f"[CROSS_LEVEL_COLLISION] '{c}' is both a {owner[c][:-1]} and a {lvl[:-1]}")
            owner[c] = lvl

    for lvl in order[1:]:
        pf, plvl, glvl = parent_field[lvl], parent_level[lvl], grandparent_level.get(lvl)
        for row in tables[lvl]:
            code = row["code"].strip()
            refs = split(row.get(pf, ""))
            if not refs:
                warnings.append(f"[EMPTY_PARENT] {lvl}/{code} has no {pf}")
            for r in refs:
                if r not in codes[plvl]:
                    if glvl and r in codes[glvl]:
                        errors.append(
                            f"[LEVEL_SKIP] {lvl}/{code}: '{r}' is a {glvl[:-1]} (grandparent), not a {plvl[:-1]}. Did you mean a {plvl[:-1]} named '{code}'?"
                        )
                    else:
                        errors.append(f"[BROKEN_REFERENCE] {lvl}/{code}: '{r}' not in {plvl}")

    print(f"Checking {tsv_path}:")
    print(f"❌ {len(errors)} error(s), ⚠️ {len(warnings)} warning(s)")
    for e in errors:
        print(f"  • {e}")
    for w in warnings:
        print(f"  • {w}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
