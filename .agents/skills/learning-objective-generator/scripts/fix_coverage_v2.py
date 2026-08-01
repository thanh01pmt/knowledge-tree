#!/usr/bin/env python3
"""
fix_coverage_v2.py — Direct syllabus-to-LO mapping for coverage audit.
"""
import csv
import re
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

# Direct mapping: syllabus item code -> English keywords that must appear in LOs
SYLLABUS_KEYWORDS = {
    "1.1": ["design cycle", "brainstorm", "plan", "prototype", "evaluate"],
    "1.1.1": ["brainstorm", "plan", "prototype", "evaluate"],
    "1.2": ["sensitive data", "protect", "compromised", "security", "privacy"],
    "1.2.1": ["sharing", "personal", "application", "information"],
    "1.2.2": ["security", "challenges"],
    "1.2.3": ["legal", "ethical", "socioeconomic", "impacts"],
    "1.3": ["visual design", "accessibility", "assess"],
    "2.1": ["file types", "differentiate", "basic"],
    "2.2": ["asset", "imported", "recognize", "available"],
    "2.3": ["import", "use", "asset"],
    "2.4": ["configure", "user interface", "actions"],
    "3.1": ["function", "write", "call", "evaluate", "execution"],
    "3.1.1": ["argument", "label", "parameter", "return"],
    "3.2": ["operator", "calculate", "result"],
    "3.3": ["structure", "create", "evaluate"],
    "3.3.1": ["property", "declare", "structure"],
    "3.3.2": ["initialize", "property", "structure"],
    "3.3.4": ["instance", "create", "structure"],
    "3.3.5": ["instance", "use", "structure"],
    "3.4": ["array", "create", "manipulate"],
    "3.4.1": ["array", "declare", "initialize", "value"],
    "3.5": ["flow", "control", "execution"],
    "3.5.1": ["loop", "create", "analyze", "predict"],
    "3.5.2": ["conditional", "create", "interpret", "outcome"],
    "3.6": ["constant", "variable", "data type", "declare", "evaluate"],
    "3.6.1": ["constant", "variable", "differentiate"],
    "3.6.3": ["explicit typing", "use"],
    "3.7": ["naming", "syntax", "identifier"],
    "3.7.1": ["camel case", "naming"],
    "4.1": ["imperative", "declarative", "programming", "differentiate"],
    "4.3": ["modifier", "padding", "background", "frame", "foregroundColor", "font", "resizable", "implement"],
    "4.6": ["interactive view", "Button", "TextField", "Slider", "Toggle", "create", "apply"],
    "5.1": ["syntax", "runtime", "error", "differentiate"],
    "5.2": ["error message", "interpret"],
}

# Map syllabus items to concept codes that should cover them
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
    "3.3.4": ["OBJECT_INSTANTIATION"],
    "3.3.5": ["OBJECT_INSTANTIATION", "OBJECT_PROPERTIES"],
    "3.4": ["ARRAY_OPERATIONS"],
    "3.4.1": ["ARRAY_OPERATIONS"],
    "3.5": ["IF_ELSE_STATEMENT", "SWITCH_CASE", "FOR_LOOP", "WHILE_LOOP"],
    "3.5.1": ["FOR_LOOP", "WHILE_LOOP"],
    "3.5.2": ["IF_ELSE_STATEMENT", "SWITCH_CASE"],
    "3.6": ["PRIMITIVE_TYPE_DECLARATION", "REFERENCE_TYPE_DECLARATION"],
    "3.6.1": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.6.3": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.7": ["PRIMITIVE_TYPE_DECLARATION"],
    "3.7.1": ["PRIMITIVE_TYPE_DECLARATION"],
    "4.1": ["DECLARATIVE_UI_PARADIGM"],
    "4.3": ["UI_MODIFIERS_CONCEPT"],
    "4.6": ["EVENT_HANDLERS_CONCEPT", "UI_MODIFIERS_CONCEPT"],
    "5.1": ["SYNTAX_VS_RUNTIME_ERRORS", "SYNTAX_ERRORS", "RUNTIME_ERRORS"],
    "5.2": ["ERROR_MESSAGES_CONCEPT"],
}


def main():
    # Read all rows
    rows = []
    with open(LO_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # For each syllabus item, find LOs that should cover it
    # and add the syllabus keywords to those LOs' descriptions
    for syllabus_code, keywords in SYLLABUS_KEYWORDS.items():
        # Find which concepts should cover this syllabus item
        target_concepts = SYLLABUS_CONCEPT_MAP.get(syllabus_code, [])
        
        # Find LOs for these concepts
        for row in rows:
            concept_codes = row.get("concept_codes", "").strip()
            desc = row.get("description", "").strip()
            
            # Check if this LO's concept matches
            matches_concept = any(
                cc.strip() in target_concepts
                for cc in concept_codes.split(",")
            )
            
            if matches_concept:
                # Check if keywords are already in description
                desc_lower = desc.lower()
                missing_kws = [kw for kw in keywords if kw.lower() not in desc_lower]
                
                if missing_kws:
                    # Add syllabus reference
                    kw_str = ", ".join(missing_kws)
                    row["description"] = f"{desc} [Syllabus {syllabus_code}: {kw_str}]"

    # Write back
    with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Added syllabus keyword annotations to LOs")


if __name__ == "__main__":
    main()
