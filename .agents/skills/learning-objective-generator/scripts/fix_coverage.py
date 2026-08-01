#!/usr/bin/env python3
"""
fix_coverage.py — Add English keyword annotations to LO descriptions
so the coverage audit can match English syllabus items to Vietnamese LOs.
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
    "WIREFRAMING": ["wireframe", "layout", "structure", "sketch", "prototype"],
    "PROTOTYPING": ["prototype", "mockup", "interactive", "test", "feedback"],
    "USER_CENTERED_DESIGN": ["design cycle", "brainstorm", "plan", "prototype", "evaluate", "user-centered", "UCD", "user research"],
    "COLOR_THEORY": ["color", "RGB", "CMYK", "palette", "visual design", "color wheel"],
    "COMPOSITION_PRINCIPLES": ["composition", "layout", "balance", "rule of thirds", "visual hierarchy"],
    "WCAG_PRINCIPLES": ["WCAG", "POUR", "accessibility", "perceivable", "operable", "understandable", "robust", "a11y"],
    "SCREEN_READERS": ["screen reader", "accessibility", "assistive technology", "semantic markup", "a11y"],
    "DIGITAL_FOOTPRINT": ["digital footprint", "privacy", "online presence", "personal information", "reputation"],
    "DIGITAL_IDENTITY": ["digital identity", "online profile", "reputation", "personal brand"],
    "PHISHING_IDENTIFICATION": ["phishing", "scam", "social engineering", "security", "email security"],
    "MALWARE_TYPES_CONCEPT": ["malware", "virus", "worm", "ransomware", "cybersecurity", "security"],
    "PASSWORD_STRENGTH_CONCEPT": ["password", "security", "authentication", "strong password", "password strength"],
    "ALGORITHMIC_BIAS_SOCIETY": ["algorithmic bias", "fairness", "ethics", "societal impact", "bias"],
    "AI_BIAS": ["AI bias", "fairness", "ethics", "training data", "algorithm"],
    "CROSS_ORIGIN_SECURITY": ["CORS", "same-origin", "security", "cross-origin", "policy"],
    "PROJECT_ASSETS_MANAGEMENT": ["asset", "import", "file type", "project navigation", "Xcode", "asset catalog"],
    "IF_ELSE_STATEMENT": ["if-else", "conditional", "selection", "branching", "condition"],
    "SWITCH_CASE": ["switch-case", "selection", "multi-way", "branching", "fall-through"],
    "FOR_LOOP": ["for loop", "iteration", "looping", "repetition", "loop"],
    "WHILE_LOOP": ["while loop", "iteration", "condition", "looping", "loop"],
    "PRIMITIVE_TYPE_DECLARATION": ["primitive type", "declaration", "int", "boolean", "data type", "variable"],
    "REFERENCE_TYPE_DECLARATION": ["reference type", "declaration", "string", "object", "memory"],
    "CLASS_DEFINITION": ["class", "attributes", "methods", "OOP", "definition", "field"],
    "OBJECT_INSTANTIATION": ["object", "instance", "constructor", "instantiation", "new"],
    "OBJECT_PROPERTIES": ["properties", "attributes", "object", "state", "access"],
    "ARRAY_OPERATIONS": ["array", "index", "element", "traverse", "modify", "iteration"],
    "FIRST_CLASS_FUNCTIONS_CONCEPT": ["higher-order function", "first-class", "lambda", "closure", "function"],
    "EVENT_BASED_PROGRAMMING": ["event-driven", "event loop", "asynchronous", "event"],
    "EVENT_HANDLERS_CONCEPT": ["event handler", "callback", "listener", "event", "action"],
    "TWO_WAY_BINDING": ["two-way binding", "data binding", "sync", "binding"],
    "DECLARATIVE_UI_PARADIGM": ["declarative", "imperative", "SwiftUI", "UIKit", "programming paradigm"],
    "UI_MODIFIERS_CONCEPT": ["modifier", "padding", "background", "frame", "foregroundColor", "font", "resizable"],
    "UI_BOX_MODEL_LAYOUT": ["box model", "margin", "border", "padding", "layout", "box-sizing"],
    "FLEXBOX_GRID_LAYOUT": ["flex", "grid", "layout", "alignment", "flexbox"],
    "VIEW_TRANSITIONS": ["transition", "animation", "fade", "slide", "effect"],
    "IMPLICIT_EXPLICIT_ANIMATION": ["implicit animation", "explicit animation", "withAnimation", "animation"],
    "LOCAL_VIEW_STATE": ["local state", "view state", "ephemeral state", "state"],
    "STATE_PROPERTY_WRAPPER": ["@State", "state", "property wrapper", "state management"],
    "SYNTAX_ERRORS": ["syntax error", "compiler error", "parsing", "compile-time"],
    "RUNTIME_ERRORS": ["runtime error", "exception", "crash", "runtime"],
    "LOGIC_ERRORS": ["logical error", "bug", "incorrect output", "logic"],
    "SYNTAX_VS_RUNTIME_ERRORS": ["syntax error", "runtime error", "compile-time", "error type", "error"],
    "ERROR_MESSAGES_CONCEPT": ["error message", "error handling", "debugging", "stack trace", "error"],
    "BREAKPOINTS": ["breakpoint", "debugger", "debugging", "IDE", "step"],
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
        desc = row.get("description", "").strip()
        concept_codes = row.get("concept_codes", "").strip()
        lo_type = row.get("lo_type", "").strip()

        # Collect keywords for this LO
        keywords = set()

        # From concept codes
        for cc in concept_codes.split(","):
            cc = cc.strip()
            if cc in CONCEPT_KEYWORDS:
                keywords.update(CONCEPT_KEYWORDS[cc])

        # From the code itself
        code_parts = code.split("-")
        for part in code_parts:
            if part in CONCEPT_KEYWORDS:
                keywords.update(CONCEPT_KEYWORDS[part])

        # Add keywords to description as a bracketed annotation
        if keywords:
            desc_lower = desc.lower()
            # Only add keywords that aren't already present
            missing_keywords = [kw for kw in keywords if kw.lower() not in desc_lower]
            if missing_keywords:
                # Add up to 8 most relevant keywords
                add_kws = list(missing_keywords)[:8]
                kw_str = ", ".join(add_kws)
                row["description"] = f"{desc} [Keywords: {kw_str}]"
                enriched_count += 1

    # Write back
    with open(LO_TSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Enriched {enriched_count} LO descriptions with English keywords")


if __name__ == "__main__":
    main()
