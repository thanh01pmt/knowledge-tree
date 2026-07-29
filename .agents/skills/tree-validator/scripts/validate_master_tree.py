#!/usr/bin/env python3
"""validate_master_tree.py — referential integrity + cross-level collision +
"level-skip" checks for the Master Knowledge Tree itself.

Also enforces T6 (Technology-Agnostic Neutrality) on Fields/Subjects/Categories/
Topics/Concepts: name + description + keywords MUST NOT contain concrete
technology/language names (Python, Swift, React, ...). SIO-specific content
belongs only in project-level SPECIFIC_IMPL rows, never in the Master Tree.
"""

import argparse
import re
import sys
from pathlib import Path

# Import shared parser
from master_tree_parser import (
    parse_master_tsv,
    SECTIONS,
    find_repo_root,
)

# T6 — concrete tech tokens forbidden in Master Tree (any tier).
# Matched as whole words (case-insensitive). Brand/platform names only;
# generic terms like "web", "database", "embedded" are allowed.
# IMPORTANT: tokens are pre-escaped for regex; matching uses word boundaries
# and is case-insensitive. Tokens that would match common English words
# (e.g. "spring" the season, "r" the letter) are intentionally OMITTED to
# avoid false positives — those are too ambiguous without context.
TECH_TOKENS = [
    # languages
    r"python", r"swift", r"javascript", r"typescript", r"java\b", r"golang", r"rust",
    r"ruby", r"php", r"kotlin", r"scala", r"perl", r"lua", r"haskell", r"dart",
    r"c\+\+", r"cpp", r"c#", r"csharp", r"objective-?c", r"objc",
    # frameworks / libraries (specific brand names only)
    r"react\b", r"vue\.js", r"vue\b", r"angular", r"svelte", r"solidjs", r"solid js",
    r"django", r"flask", r"express\b", r"rails\b", r"laravel",
    r"nextjs", r"next\.js", r"nuxt", r"gatsby", r"tailwind", r"bootstrap",
    # platforms / vendors
    r"arduino", r"raspberry pi", r"esp32", r"esp8266", r"node\.js", r"nodejs",
    r"docker", r"kubernetes", r"k8s",
    # specific syntax tokens (unambiguous)
    r"codable", r"getelementbyid", r"innerhtml", r"console\.log",
    r"printf", r"scanf", r"std::", r"malloc",
]

TECH_RE = re.compile(
    r"\b(?:%s)\b" % "|".join(TECH_TOKENS),
    re.IGNORECASE,
)


def find_t6_violations(tables):
    """Return list of (level, code, field, token) for any Master Tree row
    whose name/description/keywords contains a concrete technology token."""
    violations = []
    for lvl in ("fields", "subjects", "categories", "topics", "concepts"):
        for row in tables.get(lvl, []):
            code = (row.get("code") or "").strip()
            for field in ("name", "description", "keywords"):
                val = (row.get(field) or "")
                for m in TECH_RE.finditer(val):
                    violations.append((lvl, code, field, m.group(0)))
    return violations


def split(v):
    return [c.strip() for c in (v or "").replace(";", ",").replace("|", ",").split(",") if c.strip()]


def main():
    repo_root = find_repo_root(Path.cwd())
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", default=str(repo_root / "general-context/mlo-knowlege-tree.tsv"))
    args = ap.parse_args()
    tsv_path = Path(args.tsv)
    if not tsv_path.is_file():
        print(f"❌ File not found: {tsv_path}")
        sys.exit(1)

    tables = parse_master_tsv(tsv_path)

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

    # T6 neutrality audit (always runs — independent of referential errors)
    t6_violations = find_t6_violations(tables)
    if t6_violations:
        print(f"🚫 {len(t6_violations)} T6 neutrality violation(s):")
        for lvl, code, field, token in t6_violations:
            msg = f"  • [T6_VIOLATION] {lvl}/{code}: '{token}' appears in {field}"
            print(msg)
            errors.append(msg)

    for e in errors:
        if not e.startswith("  •"):
            print(f"  • {e}")
    for w in warnings:
        print(f"  • {w}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()