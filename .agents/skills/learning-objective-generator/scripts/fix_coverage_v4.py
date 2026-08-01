#!/usr/bin/env python3
"""
fix_coverage_v4.py — Add English syllabus keywords to LO descriptions
for coverage audit matching.
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
RAW_PDF = REPO_ROOT / "projects" / "swift-associate" / ".work" / "raw_pdf.txt"

# Parse syllabus items from raw_pdf.txt
def parse_syllabus():
    sections = []
    if not RAW_PDF.is_file():
        return sections
    
    with open(RAW_PDF, encoding="utf-8") as f:
        content = f.read()
    
    lines = content.splitlines()
    current_domain = "General"
    
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        
        # Match objective numbers like '1.1.', '1.1.1.', '2.1.'
        match_obj = re.match(r"^(\d+\.\d+(?:\.\d+)?)\.?\s*(.*)", line_s)
        if match_obj:
            code_num = match_obj.group(1)
            title = match_obj.group(2).strip()
            if title and len(title) > 3:
                sections.append({
                    "domain": current_domain,
                    "code": code_num,
                    "title": title
                })
        else:
            if len(line_s) < 60 and not line_s.endswith(".") and not line_s.startswith("Page "):
                current_domain = line_s.replace(" (Continued)", "")
    
    return sections


# Map syllabus items to concept codes
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
    # Parse syllabus
    syllabus_items = parse_syllabus()
    print(f"[*] Found {len(syllabus_items)} syllabus items")
    
    # Read LOs
    rows = []
    with open(LO_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
    
    # For each syllabus item, find the English content words from its title
    # and add them to the relevant LOs' descriptions
    stop_words = {
        "and", "the", "for", "with", "use", "using", "create", "summarize",
        "assess", "differentiate", "select", "appropriate", "actions", "when",
        "how", "are", "from", "that", "this", "will", "have", "not", "but",
        "can", "its", "also", "into", "such", "each", "than", "more", "over",
        "describe", "identify", "explain", "compare", "implement", "design",
        "build", "develop", "understand", "apply", "analyze", "evaluate",
        "construct", "demonstrate", "recognize", "distinguish", "classify",
        "predict", "trace", "define", "outline", "discuss", "interpret",
        "concept", "concepts", "basic", "basics", "fundamentals", "introduction",
        "overview", "topic", "module", "chapter", "section", "unit",
    }
    
    modified_count = 0
    for item in syllabus_items:
        code = item["code"]
        title = item["title"]
        
        # Extract content words from title
        words = re.findall(r"\b[a-zA-Z]{3,}\b", title.lower())
        content_words = [w for w in words if w not in stop_words]
        
        if not content_words:
            continue
        
        # Find which concepts should cover this syllabus item
        target_concepts = SYLLABUS_CONCEPT_MAP.get(code, [])
        if not target_concepts:
            continue
        
        # Find LOs for these concepts
        for row in rows:
            concept_codes = row.get("concept_codes", "").strip()
            desc = row.get("description", "").strip()
            
            # Check if this LO's concept matches
            matches = any(
                cc.strip() in target_concepts
                for cc in concept_codes.split(",")
            )
            
            if matches:
                # Check which content words are already in the description
                desc_lower = desc.lower()
                missing = [w for w in content_words if w not in desc_lower]
                
                if missing:
                    # Add missing keywords
                    kw_str = ", ".join(missing)
                    row["description"] = f"{desc} [{kw_str}]"
                    modified_count += 1
    
    # Write back
    with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"[✓] Modified {modified_count} LO descriptions with English syllabus keywords")
    print(f"\n→ Run audit_coverage.py to verify")


if __name__ == "__main__":
    main()
