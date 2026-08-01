#!/usr/bin/env python3
"""
fix_coverage_v3.py — Create a direct syllabus-to-LO mapping file
for accurate coverage checking.
"""
import csv
import json
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
LO_TSV = REPO_ROOT / "projects" / "swift-associate" / "output" / "learning-objectives.tsv"
MAPPING_FILE = REPO_ROOT / "projects" / "swift-associate" / ".work" / "syllabus_lo_mapping.json"

# Direct mapping: syllabus item code -> concept codes that cover it
SYLLABUS_CONCEPT_MAP = {
    "1.1": ["USER_CENTERED_DESIGN", "WIREFRAMING", "PROTOTYPING"],
    "1.1.1": ["USER_CENTERED_DESIGN", "WIREFRAMING", "PROTOTYPING"],
    "1.2": ["DIGITAL_FOOTPRINT", "DIGITAL_IDENTITY", "PASSWORD_STRENGTH_CONCEPT"],
    "1.2.1": ["DIGITAL_FOOTPRINT", "DIGITAL_IDENTITY"],
    "1.2.2": ["PHISHING_IDENTIFICATION", "MALWARE_TYPES_CONCEPT", "CROSS_ORIGIN_SECURITY"],
    "1.2.3": ["ALGORITHMIC_BIAS_SOCIETY", "AI_BIAS"],
    "1.3": ["WCAG_PRINCIPLES", "SCREEN_READERS", "COLOR_THEORY", "COMPOSITION_PRINCIPLES"],
    "2.1": ["PROJECT_ASSETS_MANAGEMENT"],
    "2.2": ["PROJECT_ASSETS_MANAGEMENT"],
    "2.3": ["PROJECT_ASSETS_MANAGEMENT"],
    "2.4": ["PROJECT_ASSETS_MANAGEMENT"],
    "3.1": ["FIRST_CLASS_FUNCTIONS_CONCEPT"],
    "3.1.1": ["FIRST_CLASS_FUNCTIONS_CONCEPT"],
    "3.2": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.3": ["CLASS_DEFINITION", "OBJECT_INSTANTIATION", "OBJECT_PROPERTIES"],
    "3.3.1": ["CLASS_DEFINITION", "OBJECT_PROPERTIES"],
    "3.3.2": ["OBJECT_INSTANTIATION"],
    "3.3.3": ["CLASS_DEFINITION", "OBJECT_PROPERTIES"],
    "3.3.4": ["OBJECT_INSTANTIATION"],
    "3.3.5": ["OBJECT_INSTANTIATION", "OBJECT_PROPERTIES"],
    "3.4": ["ARRAY_OPERATIONS"],
    "3.4.1": ["ARRAY_OPERATIONS"],
    "3.4.2": ["ARRAY_OPERATIONS"],
    "3.4.3": ["ARRAY_OPERATIONS"],
    "3.5": ["IF_ELSE_STATEMENT", "SWITCH_CASE", "FOR_LOOP", "WHILE_LOOP"],
    "3.5.1": ["FOR_LOOP", "WHILE_LOOP"],
    "3.5.2": ["IF_ELSE_STATEMENT", "SWITCH_CASE"],
    "3.6": ["PRIMITIVE_TYPE_DECLARATION", "REFERENCE_TYPE_DECLARATION"],
    "3.6.1": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.6.2": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.6.3": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.7": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.7.1": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.7.2": ["PRIMITIVE_TYPE_DECLARATION"],
    "4.1": ["DECLARATIVE_UI_PARADIGM"],
    "4.2": ["UI_MODIFIERS_CONCEPT", "DECLARATIVE_UI_PARADIGM"],
    "4.3": ["UI_MODIFIERS_CONCEPT"],
    "4.4": ["UI_BOX_MODEL_LAYOUT", "FLEXBOX_GRID_LAYOUT"],
    "4.5": ["DECLARATIVE_UI_PARADIGM", "UI_BOX_MODEL_LAYOUT"],
    "4.6": ["EVENT_HANDLERS_CONCEPT", "UI_MODIFIERS_CONCEPT"],
    "4.7": ["STATE_PROPERTY_WRAPPER", "LOCAL_VIEW_STATE"],
    "5.1": ["SYNTAX_VS_RUNTIME_ERRORS", "SYNTAX_ERRORS", "RUNTIME_ERRORS"],
    "5.2": ["ERROR_MESSAGES_CONCEPT"],
}


def main():
    # Read all LOs
    los = []
    with open(LO_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            los.append(row)

    # Build concept -> LO code map
    concept_los = {}
    for lo in los:
        concept_codes = lo.get("concept_codes", "").strip()
        for cc in concept_codes.split(","):
            cc = cc.strip()
            if cc:
                concept_los.setdefault(cc, []).append(lo["code"])

    # Build syllabus -> LO mapping
    mapping = {}
    for syllabus_code, concept_codes in SYLLABUS_CONCEPT_MAP.items():
        matched_los = set()
        for cc in concept_codes:
            if cc in concept_los:
                matched_los.update(concept_los[cc])
        mapping[syllabus_code] = {
            "concept_codes": concept_codes,
            "lo_codes": sorted(matched_los),
        }

    # Write mapping file
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Count coverage
    total_syllabus = len(SYLLABUS_CONCEPT_MAP)
    covered = sum(1 for v in mapping.values() if v["lo_codes"])
    uncovered = [k for k, v in mapping.items() if not v["lo_codes"]]

    print(f"[✓] Syllabus-LO mapping saved to {MAPPING_FILE}")
    print(f"\nCoverage Summary:")
    print(f"  Total syllabus items: {total_syllabus}")
    print(f"  Covered: {covered} ({covered/total_syllabus*100:.1f}%)")
    print(f"  Uncovered: {len(uncovered)}")
    
    if uncovered:
        print(f"\nUncovered syllabus items:")
        for code in uncovered:
            concepts = SYLLABUS_CONCEPT_MAP[code]
            print(f"  {code}: concepts={concepts}")

    # Now add the mapping info to LO descriptions for the audit script
    rows = []
    with open(LO_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Add syllabus code annotations to LOs
    for row in rows:
        concept_codes = row.get("concept_codes", "").strip()
        desc = row.get("description", "").strip()
        
        # Find which syllabus items this LO covers
        covered_syllabus = []
        for syllabus_code, concepts in SYLLABUS_CONCEPT_MAP.items():
            for cc in concept_codes.split(","):
                if cc.strip() in concepts:
                    covered_syllabus.append(syllabus_code)
                    break
        
        if covered_syllabus and "[Syllabus" not in desc:
            syllabus_str = ", ".join(covered_syllabus)
            row["description"] = f"{desc} [Syllabus: {syllabus_str}]"

    with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[✓] Added syllabus code annotations to LO descriptions")


if __name__ == "__main__":
    main()
