#!/usr/bin/env python3
"""
validate_taxonomy_coherence.py — Validate taxonomy mapping coherence.

Checks:
1. CS2023 KA coherence: concepts in same topic should have related KA codes
2. Parent-child validity: all parent references must exist in Master Tree
3. Hierarchy depth: concept → topic → category → subject → field chain must be valid

Usage:
  python3 validate_taxonomy_coherence.py --project <slug>
  python3 validate_taxonomy_coherence.py --mapping mapping-plan.md --master master_tree.json

Integration:
  Runs after /build-tree, before /validate-tree.
  Outputs warnings to .work/taxonomy_warnings.json — non-blocking.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_master_tree(path: Path) -> dict:
    if not path.is_file():
        print(f"[ERROR] Master tree not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_codes_from_mapping_plan(plan_path: Path) -> set:
    """Parse concept codes from mapping-plan.md."""
    if not plan_path.is_file():
        return set()
    content = plan_path.read_text(encoding="utf-8")
    codes = set(re.findall(r"`([A-Z][A-Z0-9_\-]{2,})`", content))
    return codes


def build_lookup(master: dict) -> dict:
    """Build code → {level, row} lookup."""
    lookup = {}
    for level in ["fields", "subjects", "categories", "topics", "concepts"]:
        for row in master.get(level, []):
            code = row.get("code", "")
            if code:
                lookup[code] = {"level": level, "row": row}
    return lookup


def validate_coherence(
    concept_codes: set,
    master: dict,
    lookup: dict,
) -> list[dict]:
    """Validate taxonomy coherence. Returns list of warnings."""
    warnings = []
    
    # Build topic → concepts mapping
    topic_concepts: dict[str, list[str]] = {}
    for code in concept_codes:
        entry = lookup.get(code)
        if not entry or entry["level"] != "concepts":
            continue
        row = entry["row"]
        topic_codes_str = row.get("topic_codes", "")
        for tc in topic_codes_str.replace(";", ",").split(","):
            tc = tc.strip()
            if tc:
                topic_concepts.setdefault(tc, []).append(code)
    
    # Check 1: CS2023 KA coherence within each topic
    for topic_code, concepts in topic_concepts.items():
        topic_entry = lookup.get(topic_code)
        if not topic_entry:
            continue
        topic_ka_str = topic_entry["row"].get("cs2023_ka_mapping", "")
        topic_ka = set(t.strip() for t in topic_ka_str.split(",") if t.strip())
        
        if not topic_ka:
            continue
        
        for concept_code in concepts:
            concept_entry = lookup.get(concept_code)
            if not concept_entry:
                continue
            concept_ka_str = concept_entry["row"].get("cs2023_ka_mapping", "")
            concept_ka = set(t.strip() for t in concept_ka_str.split(",") if t.strip())
            
            if concept_ka and topic_ka and not (concept_ka & topic_ka):
                warnings.append({
                    "type": "KA_MISMATCH",
                    "severity": "WARNING",
                    "message": f"Concept {concept_code} KA ({','.join(concept_ka)}) disjoint from topic {topic_code} KA ({','.join(topic_ka)})",
                    "code": concept_code,
                    "parent_code": topic_code,
                })
    
    # Check 2: Parent-child validity
    for code in concept_codes:
        entry = lookup.get(code)
        if not entry:
            warnings.append({
                "type": "MISSING_CODE",
                "severity": "ERROR",
                "message": f"Code {code} not found in Master Tree",
                "code": code,
            })
            continue
        
        row = entry["row"]
        for parent_field in ["topic_codes", "category_codes", "subject_codes", "field_codes"]:
            parents_str = row.get(parent_field, "")
            for pc in parents_str.replace(";", ",").split(","):
                pc = pc.strip()
                if pc and pc not in lookup:
                    warnings.append({
                        "type": "BROKEN_PARENT_REF",
                        "severity": "ERROR",
                        "message": f"{entry['level'][:-1]} {code} references non-existent {parent_field[:-5]} {pc}",
                        "code": code,
                        "parent_code": pc,
                    })
    
    # Check 3: Hierarchy depth
    for code in concept_codes:
        entry = lookup.get(code)
        if not entry or entry["level"] != "concepts":
            continue
        row = entry["row"]
        # concept → topic → category → subject → field
        chain = []
        current = code
        current_level = "concepts"
        parent_key_map = {
            "concepts": "topic_codes",
            "topics": "category_codes",
            "categories": "subject_codes",
            "subjects": "field_codes",
        }
        
        while current_level in parent_key_map:
            entry = lookup.get(current)
            if not entry:
                break
            parents_str = entry["row"].get(parent_key_map[current_level], "")
            parents = [p.strip() for p in parents_str.replace(";", ",").split(",") if p.strip()]
            if parents:
                current = parents[0]
                current_level = lookup.get(current, {}).get("level", "")
                chain.append(current)
            else:
                break
        
        if len(chain) < 2:
            warnings.append({
                "type": "SHALLOW_HIERARCHY",
                "severity": "INFO",
                "message": f"Concept {code} has shallow hierarchy ({len(chain)} levels above)",
                "code": code,
            })
    
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Validate taxonomy mapping coherence")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--mapping", help="Path to mapping-plan.md")
    parser.add_argument("--master", help="Path to master_tree.json")
    parser.add_argument("--output", help="Output path for warnings JSON")
    args = parser.parse_args()
    
    repo_root = find_repo_root(Path.cwd())
    
    # Resolve paths
    if args.master:
        master_path = Path(args.master)
    else:
        master_path = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree.json"
    
    master = load_master_tree(master_path)
    lookup = build_lookup(master)
    
    if args.mapping:
        plan_path = Path(args.mapping)
    elif args.project:
        plan_path = repo_root / "projects" / args.project / ".work" / "mapping-plan.md"
    else:
        print("[ERROR] --project or --mapping required", file=sys.stderr)
        sys.exit(1)
    
    concept_codes = extract_codes_from_mapping_plan(plan_path)
    print(f"[*] Found {len(concept_codes)} concept codes in mapping plan")
    
    warnings = validate_coherence(concept_codes, master, lookup)
    
    # Print summary
    errors = [w for w in warnings if w["severity"] == "ERROR"]
    warns = [w for w in warnings if w["severity"] == "WARNING"]
    infos = [w for w in warnings if w["severity"] == "INFO"]
    
    print(f"\n{'='*60}")
    print(f"Coherence Validation Results")
    print(f"{'='*60}")
    print(f"  Errors:   {len(errors)}")
    print(f"  Warnings: {len(warns)}")
    print(f"  Info:     {len(infos)}")
    print(f"{'='*60}")
    
    for w in warnings:
        icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}.get(w["severity"], "•")
        print(f"  {icon} [{w['type']}] {w['message']}")
    
    # Write output
    if args.output:
        out_path = Path(args.output)
    elif args.project:
        out_path = repo_root / "projects" / args.project / ".work" / "taxonomy_warnings.json"
    else:
        out_path = Path("taxonomy_warnings.json")
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(warnings, f, ensure_ascii=False, indent=2)
    print(f"\n[✓] Warnings → {out_path}")
    
    # Exit code: 0 if no errors, 1 if errors found
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
