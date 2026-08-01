#!/usr/bin/env python3
"""Fix the 26 old SIOs that lost parent_lo_code and concept_codes during merge."""
import csv
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

# Map old SIO codes -> (parent_cio, concept_code)
SIO_PARENT_MAP = {
    "SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE": ("CIO-PROJECT_ASSETS_MANAGEMENT-01", "PROJECT_ASSETS_MANAGEMENT"),
    "SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION": ("CIO-PROJECT_ASSETS_MANAGEMENT-01", "PROJECT_ASSETS_MANAGEMENT"),
    "SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG": ("CIO-PROJECT_ASSETS_MANAGEMENT-03-01", "PROJECT_ASSETS_MANAGEMENT"),
    "SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG": ("CIO-PROJECT_ASSETS_MANAGEMENT-03-01", "PROJECT_ASSETS_MANAGEMENT"),
    "SIO-SWIFT-REFERENCE_IMAGE_BY_NAME": ("CIO-PROJECT_ASSETS_MANAGEMENT-03-02", "PROJECT_ASSETS_MANAGEMENT"),
    "SIO-SWIFT-REFERENCE_COLOR_BY_NAME": ("CIO-PROJECT_ASSETS_MANAGEMENT-03-02", "PROJECT_ASSETS_MANAGEMENT"),
    "SIO-SWIFT-ITERATE_ARRAY_FOR_IN": ("CIO-ARRAY_OPERATIONS-03-01", "ARRAY_OPERATIONS"),
    "SIO-SWIFT-ITERATE_ARRAY_ENUMERATED": ("CIO-ARRAY_OPERATIONS-03-01", "ARRAY_OPERATIONS"),
    "SIO-SWIFT-MODIFY_ARRAY_IN_PLACE_CONDITION": ("CIO-ARRAY_OPERATIONS-03-02", "ARRAY_OPERATIONS"),
    "SIO-SWIFT-MODIFY_ARRAY_WITH_MAP": ("CIO-ARRAY_OPERATIONS-03-02", "ARRAY_OPERATIONS"),
    "SIO-SWIFT-WHILE_LOOP_COUNTER": ("CIO-WHILE_LOOP-03-01", "WHILE_LOOP"),
    "SIO-SWIFT-WHILE_LOOP_BOOLEAN_FLAG": ("CIO-WHILE_LOOP-03-01", "WHILE_LOOP"),
    "SIO-SWIFT-WHILE_LOOP_USER_INPUT": ("CIO-WHILE_LOOP-03-02", "WHILE_LOOP"),
    "SIO-SWIFT-WHILE_LOOP_FUNCTION_RESULT": ("CIO-WHILE_LOOP-03-02", "WHILE_LOOP"),
    "SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE": ("CIO-DECLARATIVE_UI_PARADIGM-03", "DECLARATIVE_UI_PARADIGM"),
    "SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI": ("CIO-DECLARATIVE_UI_PARADIGM-03", "DECLARATIVE_UI_PARADIGM"),
    "SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT": ("CIO-UI_MODIFIERS_CONCEPT-03", "UI_MODIFIERS_CONCEPT"),
    "SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE": ("CIO-UI_MODIFIERS_CONCEPT-03", "UI_MODIFIERS_CONCEPT"),
    "SIO-SWIFT-ATTACH_ACTION_TO_BUTTON": ("CIO-EVENT_HANDLERS_CONCEPT-02", "EVENT_HANDLERS_CONCEPT"),
    "SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE": ("CIO-EVENT_HANDLERS_CONCEPT-02", "EVENT_HANDLERS_CONCEPT"),
    "SIO-SWIFT-DECLARE_STATE_PROPERTY": ("CIO-STATE_PROPERTY_WRAPPER-02", "STATE_PROPERTY_WRAPPER"),
    "SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION": ("CIO-STATE_PROPERTY_WRAPPER-02", "STATE_PROPERTY_WRAPPER"),
    "SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME": ("CIO-SYNTAX_VS_RUNTIME_ERRORS-03", "SYNTAX_VS_RUNTIME_ERRORS"),
    "SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE": ("CIO-SYNTAX_VS_RUNTIME_ERRORS-03", "SYNTAX_VS_RUNTIME_ERRORS"),
    "SIO-SWIFT-READ_ERROR_MESSAGE_TYPE": ("CIO-ERROR_MESSAGES_CONCEPT-02", "ERROR_MESSAGES_CONCEPT"),
    "SIO-SWIFT-LOCATE_ERROR_CAUSE": ("CIO-ERROR_MESSAGES_CONCEPT-02", "ERROR_MESSAGES_CONCEPT"),
}

# Read all rows
rows = []
with open(LO_TSV, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

fixed_count = 0
for row in rows:
    code = row.get("code", "").strip()
    if code in SIO_PARENT_MAP:
        parent_cio, concept_code = SIO_PARENT_MAP[code]
        old_parent = row.get("parent_lo_code", "").strip()
        old_concept = row.get("concept_codes", "").strip()
        if not old_parent or not old_concept:
            row["parent_lo_code"] = parent_cio
            row["concept_codes"] = concept_code
            fixed_count += 1
            print(f"  Fixed {code}: parent={old_parent}->{parent_cio}, concept={old_concept}->{concept_code}")

# Write back
with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(f"\n[✓] Fixed {fixed_count} SIOs")
