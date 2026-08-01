#!/usr/bin/env python3
"""
fix_validation_errors.py — Fix validation errors in learning-objectives.tsv.

Fixes:
1. LO_DESCRIPTION_PREFIX: Descriptions not starting with "Người học có khả năng"
2. LO_INVALID_KNOWLEDGE_DIMENSION: Invalid dimension values
3. EMPTY_PARENT_REF / LO_TYPE_PARENT_MISMATCH: Only for LOs where parent
   can be determined from existing data (no synthetic generation)

NOTE: Does NOT auto-generate synthetic parent references or DUP suffixes
(per AGENTS.md §9 — No Metric Gaming). Reports issues for manual review.
"""

import csv
import re
import sys
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


REPO_ROOT = find_repo_root(Path(__file__).resolve())
PROJECT = "swift-associate"
LO_TSV = REPO_ROOT / "projects" / PROJECT / "output" / "learning-objectives.tsv"
CONCEPTS_TSV = REPO_ROOT / "projects" / PROJECT / "output" / "concepts.tsv"

VALID_KNOWLEDGE_DIMS = {"FACTUAL", "CONCEPTUAL", "PROCEDURAL", "METACOGNITIVE"}


def fix_description_prefix(desc: str) -> str:
    desc = desc.strip()
    if not desc or desc.startswith("Người học có khả năng"):
        return desc
    if desc[0].isupper():
        desc = desc[0].lower() + desc[1:]
    return f"Người học có khả năng {desc}"


def fix_knowledge_dimension(dim: str) -> str:
    d = dim.strip().upper()
    mapping = {
        "CONCEPTUAL": "CONCEPTUAL",
        "PROCEDURAL": "PROCEDURAL",
        "FACTUAL": "FACTUAL",
        "METACOGNITIVE": "METACOGNITIVE",
        "CONCEPTUAL_IMPL": "CONCEPTUAL",
        "SPECIFIC_IMPL": "PROCEDURAL",
        "UNIVERSAL": "CONCEPTUAL",
        "": "CONCEPTUAL",
    }
    return mapping.get(d, "CONCEPTUAL")


def main():
    # Load concepts
    concepts = {}
    with open(CONCEPTS_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code = (row.get("code") or "").strip()
            if code:
                concepts[code] = row
    valid_concept_codes = set(concepts.keys())

    # Load LOs
    los = []
    with open(LO_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            los.append(row)

    print(f"[*] Loaded {len(los)} LOs, {len(valid_concept_codes)} concepts")

    # Build parent-child maps from existing data only
    ulo_concept_map = {}
    for lo in los:
        if lo.get("lo_type") == "UNIVERSAL":
            ulo_concept_map[lo["code"]] = lo.get("concept_codes", "")

    cio_parent_map = {}
    for lo in los:
        if lo.get("lo_type") == "CONCEPTUAL_IMPL":
            parent = lo.get("parent_lo_code", "").strip()
            if parent:
                cio_parent_map[lo["code"]] = parent

    fixed_prefix = 0
    fixed_dimension = 0
    fixed_parent_ref = 0
    fixed_type_mismatch = 0
    needs_review = []  # Issues that need manual review (§9 compliance)

    for lo in los:
        code = lo["code"]
        lo_type = lo.get("lo_type", "")
        parent = lo.get("parent_lo_code", "").strip()
        concept_codes = lo.get("concept_codes", "").strip()
        desc = lo.get("description", "").strip()
        dim = lo.get("knowledge_dimension", "").strip()

        # Fix 1: LO_DESCRIPTION_PREFIX
        if desc and not desc.startswith("Người học có khả năng"):
            lo["description"] = fix_description_prefix(desc)
            fixed_prefix += 1

        # Fix 2: LO_INVALID_KNOWLEDGE_DIMENSION
        if dim and dim.upper() not in VALID_KNOWLEDGE_DIMS:
            lo["knowledge_dimension"] = fix_knowledge_dimension(dim)
            fixed_dimension += 1
        elif not dim:
            lo["knowledge_dimension"] = "CONCEPTUAL"
            fixed_dimension += 1

        # Fix 3: EMPTY_PARENT_REF — only fix if parent data exists
        if not concept_codes:
            if lo_type == "UNIVERSAL":
                m = re.match(r"ULO-(.+?)-\d+$", code)
                if m:
                    cc = m.group(1)
                    if cc in valid_concept_codes:
                        lo["concept_codes"] = cc
                        fixed_parent_ref += 1
            elif lo_type == "CONCEPTUAL_IMPL":
                if parent and parent in ulo_concept_map:
                    inherited = ulo_concept_map[parent]
                    if inherited:
                        lo["concept_codes"] = inherited
                        fixed_parent_ref += 1
                else:
                    m = re.match(r"CIO-(.+?)-\d", code)
                    if m:
                        cc = m.group(1)
                        if cc in valid_concept_codes:
                            lo["concept_codes"] = cc
                            fixed_parent_ref += 1
            elif lo_type == "SPECIFIC_IMPL":
                if parent and parent in cio_parent_map:
                    parent_ulo = cio_parent_map[parent]
                    if parent_ulo in ulo_concept_map:
                        inherited = ulo_concept_map[parent_ulo]
                        if inherited:
                            lo["concept_codes"] = inherited
                            fixed_parent_ref += 1

        # Fix 4: LO_TYPE_PARENT_MISMATCH — only if parent can be found
        if lo_type == "CONCEPTUAL_IMPL" and not parent:
            m = re.match(r"CIO-(.+?)-\d", code)
            if m:
                cc = m.group(1)
                found = False
                for ulo_code, ulo_cc in ulo_concept_map.items():
                    if cc in ulo_cc:
                        lo["parent_lo_code"] = ulo_code
                        fixed_type_mismatch += 1
                        found = True
                        break
                if not found:
                    needs_review.append(f"  [REVIEW] {code}: cannot determine parent ULO for concept '{cc}'")

    # Backup
    backup = LO_TSV.with_suffix(".tsv.bak2")
    LO_TSV.rename(backup)
    print(f"[*] Backup saved to {backup}")

    # Write fixed TSV
    fieldnames = [
        "code", "name", "description", "lo_type", "parent_lo_code",
        "concept_codes", "bloom_level", "knowledge_dimension", "assessment_approach"
    ]
    with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(los)

    print(f"\n{'='*60}")
    print("FIX SUMMARY")
    print(f"{'='*60}")
    print(f"  LO_DESCRIPTION_PREFIX:      {fixed_prefix}")
    print(f"  LO_INVALID_KNOWLEDGE_DIM:   {fixed_dimension}")
    print(f"  EMPTY_PARENT_REF:           {fixed_parent_ref}")
    print(f"  LO_TYPE_PARENT_MISMATCH:    {fixed_type_mismatch}")
    print(f"\n  Total LOs written: {len(los)}")
    if needs_review:
        print(f"\n⚠️  {len(needs_review)} issue(s) need manual review (§9):")
        for r in needs_review:
            print(r)
    print(f"\n→ Run validate_tree.py to verify")


if __name__ == "__main__":
    main()
