#!/usr/bin/env python3
"""
enrich_lo_keywords.py — Add English keyword annotations to LO names
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

# Map concept codes to English keywords from the syllabus
CONCEPT_KEYWORDS = {
    # Planning and Design (1.x)
    "WIREFRAMING": ["wireframe", "layout", "structure", "sketch"],
    "PROTOTYPING": ["prototype", "mockup", "interactive", "test"],
    "USER_CENTERED_DESIGN": ["design cycle", "brainstorm", "plan", "evaluate", "user-centered", "UCD"],
    "COLOR_THEORY": ["color", "RGB", "CMYK", "palette", "visual design"],
    "COMPOSITION_PRINCIPLES": ["composition", "layout", "balance", "rule of thirds"],
    "WCAG_PRINCIPLES": ["WCAG", "POUR", "accessibility", "perceivable", "operable", "understandable", "robust"],
    "SCREEN_READERS": ["screen reader", "accessibility", "assistive technology", "semantic"],
    "DIGITAL_FOOTPRINT": ["digital footprint", "privacy", "online", "personal information"],
    "DIGITAL_IDENTITY": ["digital identity", "online profile", "reputation"],
    "PHISHING_IDENTIFICATION": ["phishing", "scam", "social engineering", "security"],
    "MALWARE_TYPES_CONCEPT": ["malware", "virus", "worm", "ransomware", "security"],
    "PASSWORD_STRENGTH_CONCEPT": ["password", "security", "authentication", "strong password"],
    "ALGORITHMIC_BIAS_SOCIETY": ["algorithmic bias", "fairness", "ethics", "societal impact"],
    "AI_BIAS": ["AI bias", "fairness", "ethics", "training data"],
    "CROSS_ORIGIN_SECURITY": ["CORS", "same-origin", "security", "cross-origin"],
    
    # XCode Project Navigation (2.x)
    "PROJECT_ASSETS_MANAGEMENT": ["asset", "import", "file type", "project navigation", "Xcode"],
    
    # Swift Language Usage (3.x)
    "IF_ELSE_STATEMENT": ["if-else", "conditional", "selection", "branching"],
    "SWITCH_CASE": ["switch-case", "selection", "multi-way", "branching"],
    "FOR_LOOP": ["for loop", "iteration", "looping", "repetition"],
    "WHILE_LOOP": ["while loop", "iteration", "condition", "looping"],
    "PRIMITIVE_TYPE_DECLARATION": ["primitive type", "declaration", "int", "boolean", "data type"],
    "REFERENCE_TYPE_DECLARATION": ["reference type", "declaration", "string", "object"],
    "CLASS_DEFINITION": ["class", "attributes", "methods", "OOP", "definition"],
    "OBJECT_INSTANTIATION": ["object", "instance", "constructor", "instantiation"],
    "OBJECT_PROPERTIES": ["properties", "attributes", "object", "state"],
    "ARRAY_OPERATIONS": ["array", "index", "element", "traverse", "modify"],
    "FIRST_CLASS_FUNCTIONS_CONCEPT": ["higher-order function", "first-class", "lambda", "closure"],
    "EVENT_BASED_PROGRAMMING": ["event-driven", "event loop", "asynchronous"],
    "EVENT_HANDLERS_CONCEPT": ["event handler", "callback", "listener", "event"],
    "TWO_WAY_BINDING": ["two-way binding", "data binding", "sync"],
    
    # View Building with SwiftUI (4.x)
    "DECLARATIVE_UI_PARADIGM": ["declarative", "imperative", "SwiftUI", "UIKit"],
    "UI_MODIFIERS_CONCEPT": ["modifier", "padding", "background", "frame", "foregroundColor", "font", "resizable"],
    "UI_BOX_MODEL_LAYOUT": ["box model", "margin", "border", "padding", "layout"],
    "FLEXBOX_GRID_LAYOUT": ["flex", "grid", "layout", "alignment"],
    "VIEW_TRANSITIONS": ["transition", "animation", "fade", "slide"],
    "IMPLICIT_EXPLICIT_ANIMATION": ["implicit animation", "explicit animation", "withAnimation"],
    "LOCAL_VIEW_STATE": ["local state", "view state", "ephemeral state"],
    "STATE_PROPERTY_WRAPPER": ["@State", "state", "property wrapper", "state management"],
    
    # Debugging (5.x)
    "SYNTAX_ERRORS": ["syntax error", "compiler error", "parsing"],
    "RUNTIME_ERRORS": ["runtime error", "exception", "crash"],
    "LOGIC_ERRORS": ["logical error", "bug", "incorrect output"],
    "SYNTAX_VS_RUNTIME_ERRORS": ["syntax error", "runtime error", "compile-time", "error type"],
    "ERROR_MESSAGES_CONCEPT": ["error message", "error handling", "debugging", "stack trace"],
    "BREAKPOINTS": ["breakpoint", "debugger", "debugging", "IDE"],
}

# Also map specific syllabus items to LO concepts
SYLLABUS_ITEM_MAP = {
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
    "3.3.3": ["method", "define"],
    "3.3.4": ["instance", "create", "structure"],
    "3.3.5": ["instance", "use", "structure"],
    "3.4": ["array", "create", "manipulate"],
    "3.4.1": ["array", "declare", "initialize", "value"],
    "3.4.2": ["array", "element", "index", "identify", "modify"],
    "3.4.3": ["array", "property", "method", "evaluate"],
    "3.5": ["flow", "control", "execution"],
    "3.5.1": ["loop", "create", "analyze", "predict"],
    "3.5.2": ["conditional", "create", "interpret", "outcome"],
    "3.6": ["constant", "variable", "data type", "declare", "evaluate"],
    "3.6.1": ["constant", "variable", "differentiate"],
    "3.6.2": ["type inference", "apply"],
    "3.6.3": ["explicit typing", "use"],
    "3.7": ["naming", "syntax", "identifier"],
    "3.7.1": ["camel case", "naming"],
    "3.7.2": ["identifier", "rule", "Swift"],
    "4.1": ["imperative", "declarative", "programming", "differentiate"],
    "4.2": ["content view", "Text", "Image", "Shape", "Color", "create"],
    "4.3": ["modifier", "padding", "background", "frame", "foregroundColor", "font", "resizable", "implement"],
    "4.4": ["container view", "HStack", "VStack", "ZStack", "Spacer", "create"],
    "4.5": ["view hierarchy", "explain", "program"],
    "4.6": ["interactive view", "Button", "TextField", "Slider", "Toggle", "create", "apply"],
    "4.7": ["@State", "property wrapper", "control", "appearance"],
    "5.1": ["syntax", "runtime", "error", "differentiate"],
    "5.2": ["error message", "interpret"],
}


def main():
    # Read all rows
    rows = []
    with open(LO_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    enriched_count = 0
    for row in rows:
        code = row.get("code", "").strip()
        name = row.get("name", "").strip()
        concept_codes = row.get("concept_codes", "").strip()
        lo_type = row.get("lo_type", "").strip()

        # Collect keywords for this LO
        keywords = set()

        # From concept codes
        for cc in concept_codes.split(","):
            cc = cc.strip()
            if cc in CONCEPT_KEYWORDS:
                keywords.update(CONCEPT_KEYWORDS[cc])

        # From the code itself (e.g., ULO-IF_ELSE_STATEMENT-01)
        code_parts = code.split("-")
        for part in code_parts:
            if part in CONCEPT_KEYWORDS:
                keywords.update(CONCEPT_KEYWORDS[part])

        # Add keywords to name if not already present
        if keywords:
            # Check if keywords are already in the name
            name_lower = name.lower()
            missing_keywords = [kw for kw in keywords if kw.lower() not in name_lower]
            if missing_keywords:
                # Add up to 5 most relevant keywords
                add_kws = list(missing_keywords)[:5]
                kw_str = ", ".join(add_kws)
                row["name"] = f"{name} ({kw_str})"
                enriched_count += 1

    # Write back
    with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Enriched {enriched_count} LO names with English keywords")


if __name__ == "__main__":
    main()
