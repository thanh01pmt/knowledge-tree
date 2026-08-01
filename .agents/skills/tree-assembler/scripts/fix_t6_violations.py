#!/usr/bin/env python3
"""
fix_t6_violations.py — Fix T6 (Technology-Agnostic Neutrality) violations in Master TSV.

Renames tech-specific concepts to tech-agnostic names and sanitizes
description/keywords fields to remove concrete technology names.
"""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(repo_root / ".agents/skills/tree-validator/scripts"))
from master_tree_parser import parse_master_tsv


def fix_t6_violations(tsv_path: Path):
    print(f"🔧 Fixing T6 violations in {tsv_path}...")
    content = tsv_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    current_level = None
    headers = []

    # ── Concept renames (tech-specific → tech-agnostic) ──────────────────────
    CONCEPT_RENAME = {
        "ARDUINO_BASICS": "MICROCONTROLLER_PROGRAMMING_BASICS",
        "RASPBERRY_PI_BASICS": "SINGLE_BOARD_COMPUTER_BASICS",
        "FRONTEND_FRAMEWORKS": "FRONTEND_FRAMEWORK_CONCEPTS",
        "BACKEND_FRAMEWORKS": "BACKEND_FRAMEWORK_CONCEPTS",
    }

    # ── Topic renames ────────────────────────────────────────────────────────
    TOPIC_RENAME = {
        "JAVASCRIPT_DOM": "DOM_MANIPULATION",
        "MCU_PLATFORMS": "MICROCONTROLLER_PLATFORMS",
    }

    # ── Keywords/description sanitization rules ──────────────────────────────
    # (field_name, level, code) -> {field: replacement_text}
    # Empty string = remove the token entirely
    SANITIZE = {
        # subjects
        ("keywords", "subjects", "PHYSICAL_COMPUTING"): {"keywords": "embedded systems, microcontrollers, robotics, sensors, actuators"},
        ("keywords", "subjects", "WEB_DEV"): {"keywords": "frontend, backend, full-stack, web architecture, HTTP, APIs"},

        # categories
        ("keywords", "categories", "MICROCONTROLLERS"): {"keywords": "embedded systems, microcontrollers, GPIO, interrupts, RTOS"},
        ("description", "categories", "MICROCONTROLLERS"): {"description": "Covers microcontroller architectures, peripherals, and embedded programming concepts."},
        ("keywords", "categories", "FRONTEND_DEV"): {"keywords": "frontend, user interface, DOM, CSS, accessibility, performance"},
        ("description", "categories", "FRONTEND_DEV"): {"description": "Covers client-side web development concepts including markup, styling, scripting, and user interaction."},
        ("keywords", "categories", "WEB_FRAMEWORKS"): {"keywords": "web frameworks, MVC, component-based, server-side rendering, SPA"},
        ("description", "categories", "WEB_FRAMEWORKS"): {"description": "Covers architectural patterns and concepts in web application frameworks."},
        ("keywords", "categories", "GAME_SCRIPTING"): {"keywords": "game scripting, game logic, scripting languages, game engines"},

        # topics
        ("description", "topics", "MCU_PLATFORMS"): {"description": "Covers common microcontroller platforms, their architectures, peripherals, and development ecosystems."},
        ("keywords", "topics", "MCU_PLATFORMS"): {"keywords": "microcontrollers, AVR, ARM Cortex-M, ESP, STM32, development boards"},
        ("name", "topics", "JAVASCRIPT_DOM"): {"name": "DOM Manipulation"},
        ("description", "topics", "JAVASCRIPT_DOM"): {"description": "Covers Document Object Model manipulation, event handling, and dynamic content updates."},
        ("keywords", "topics", "JAVASCRIPT_DOM"): {"keywords": "DOM, events, selectors, manipulation, browser APIs"},
        ("description", "topics", "SERVER_SIDE_LOGIC"): {"description": "Covers server-side programming concepts: request handling, routing, middleware, authentication, database integration."},
        ("keywords", "topics", "SERVER_SIDE_LOGIC"): {"keywords": "server-side, routing, middleware, authentication, REST, GraphQL, databases"},
        ("keywords", "topics", "STRUCTURED_DATA_STORAGE"): {"keywords": "data serialization, JSON, Protocol Buffers, Avro, schema evolution"},

        # concepts
        ("name", "concepts", "ARDUINO_BASICS"): {"name": "Microcontroller Programming Basics"},
        ("description", "concepts", "ARDUINO_BASICS"): {"description": "Covers fundamental microcontroller programming: GPIO, timers, interrupts, serial communication, and basic I/O."},
        ("keywords", "concepts", "ARDUINO_BASICS"): {"keywords": "microcontroller, GPIO, timers, interrupts, UART, I2C, SPI, embedded C"},
        ("name", "concepts", "RASPBERRY_PI_BASICS"): {"name": "Single Board Computer Basics"},
        ("description", "concepts", "RASPBERRY_PI_BASICS"): {"description": "Covers single-board computer fundamentals: Linux on ARM, GPIO, peripheral interfaces, headless setup, and IoT gateway patterns."},
        ("keywords", "concepts", "RASPBERRY_PI_BASICS"): {"keywords": "SBC, ARM Linux, GPIO, headless, IoT gateway, embedded Linux"},
        ("description", "concepts", "FRONTEND_FRAMEWORKS"): {"description": "Covers frontend framework concepts: component lifecycle, state management, virtual DOM, reactivity, composition patterns."},
        ("keywords", "concepts", "FRONTEND_FRAMEWORKS"): {"keywords": "components, state, props, lifecycle, reactivity, virtual DOM, composition"},
        ("description", "concepts", "BACKEND_FRAMEWORKS"): {"description": "Covers backend framework concepts: routing, controllers, middleware, ORM, dependency injection, API design patterns."},
        ("keywords", "concepts", "BACKEND_FRAMEWORKS"): {"keywords": "routing, controllers, middleware, ORM, DI, REST, GraphQL, authentication"},
        ("description", "concepts", "DOM_MANIPULATION"): {"description": "Covers DOM manipulation techniques: element selection, traversal, modification, event delegation, and performance considerations."},
        ("keywords", "concepts", "DOM_MANIPULATION"): {"keywords": "DOM, selectors, traversal, events, delegation, performance, shadow DOM"},
        ("description", "concepts", "JSON_SERIALIZATION"): {"description": "Covers structured data serialization concepts: schema definition, encoding/decoding, validation, versioning, and interoperability."},
        ("keywords", "concepts", "JSON_SERIALIZATION"): {"keywords": "serialization, JSON, schema, encoding, decoding, validation, interoperability"},
    }

    # Also update references when code renamed
    CODE_RENAME_MAP = {**CONCEPT_RENAME, **TOPIC_RENAME}

    for line in lines:
        s = line.strip()

        # Detect table boundaries
        if s.startswith("Bảng 1:"):
            current_level = "fields"
            new_lines.append(line)
            continue
        elif s.startswith("Bảng 2:"):
            current_level = "subjects"
            new_lines.append(line)
            continue
        elif s.startswith("Bảng 3:"):
            current_level = "categories"
            headers = []
            new_lines.append(line)
            continue
        elif s.startswith("Bảng 4:"):
            current_level = "topics"
            headers = []
            new_lines.append(line)
            continue
        elif s.startswith("Bảng 5:"):
            current_level = "concepts"
            headers = []
            new_lines.append(line)
            continue
        elif s.startswith("Bảng 6:"):
            current_level = "learning_objectives"
            headers = []
            new_lines.append(line)
            continue

        # Parse header row
        parts = line.split("\t")
        if parts[0] == "code":
            headers = [h.strip() for h in parts]
            new_lines.append(line)
            continue

        # Process data rows
        if headers and len(parts) >= 2 and parts[0].strip():
            row_dict = {h: parts[i].strip() if i < len(parts) else "" for i, h in enumerate(headers)}
            original_code = row_dict["code"]

            # Apply sanitization
            sanitize_key = None
            for field in ["name", "description", "keywords"]:
                key = (field, current_level, original_code)
                if key in SANITIZE:
                    sanitize_key = key
                    break

            if sanitize_key:
                field, _, _ = sanitize_key
                replacements = SANITIZE[sanitize_key]
                for f, new_val in replacements.items():
                    if f in row_dict:
                        row_dict[f] = new_val

            # Apply code renames
            if original_code in CODE_RENAME_MAP:
                new_code = CODE_RENAME_MAP[original_code]
                row_dict["code"] = new_code
                print(f"  📝 Renamed {current_level}: {original_code} → {new_code}")

            # Update references in other columns (category_codes, topic_codes, etc.)
            for h in headers:
                if h in row_dict and h.endswith("_codes"):
                    val = row_dict[h]
                    for old_c, new_c in CODE_RENAME_MAP.items():
                        # Replace whole word matches
                        val = val.replace(f",{old_c},", f",{new_c},")
                        val = val.replace(f"{old_c},", f"{new_c},")
                        val = val.replace(f",{old_c}", f",{new_c}")
                        if val == old_c:
                            val = new_c
                    row_dict[h] = val

            # Also update field_codes, subject_codes, etc. in concepts/topics
            for h in ["field_codes", "subject_codes", "category_codes", "topic_codes", "prerequisite_concept_codes"]:
                if h in row_dict:
                    val = row_dict[h]
                    for old_c, new_c in CODE_RENAME_MAP.items():
                        val = val.replace(f",{old_c},", f",{new_c},")
                        val = val.replace(f"{old_c},", f"{new_c},")
                        val = val.replace(f",{old_c}", f",{new_c}")
                        if val == old_c:
                            val = new_c
                    row_dict[h] = val

            new_line = "\t".join([row_dict.get(h, "") for h in headers])
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    final_content = "\n".join(new_lines)
    tsv_path.write_text(final_content, encoding="utf-8")
    print(f"✅ Fixed T6 violations in {tsv_path}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else repo_root / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
    fix_t6_violations(target)