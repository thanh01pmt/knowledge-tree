#!/usr/bin/env python3
"""fix_master_tsv.py — Comprehensive Master Knowledge Tree Data Fixer."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(repo_root / ".agents/skills/taxonomy-mapper/scripts"))
from parse_master_tree import parse_master_tsv


def fix_tsv(tsv_path: Path):
    print(f"Applying data fixes to {tsv_path}...")
    content = tsv_path.read_text(encoding="utf-8")

    # 1. Typos and invalid subject refs in Categories
    content = content.replace("SW_PARADIGIMS", "SW_PARADIGMS")
    content = content.replace("NATIVE_APP_DEV, HCC", "NATIVE_APP_DEV, HCI")
    content = content.replace("NATIVE_APP_DEV,HCC", "NATIVE_APP_DEV, HCI")
    content = content.replace("DECLARATIVE_UI, NATIVE_APP_DEV, ASE", "NATIVE_APP_DEV, SW_PARADIGMS")
    content = content.replace("DECLARATIVE_UI,MOBILE_DEV", "MOBILE_DEV")
    content = content.replace("DECLARATIVE_UI, MOBILE_DEV", "MOBILE_DEV")
    content = content.replace("NATIVE_APP_DEV, DAI", "NATIVE_APP_DEV, DATA_MGMT")

    # 2. Rename Category codes that collide with Topic codes
    # GRAPHIC_DESIGN_PRINCIPLES (cat) -> GRAPHIC_DESIGN_CAT
    # DIGITAL_INTERACTION (cat) -> DIGITAL_INTERACTION_CAT
    # COLLABORATION_TOOLS (cat) -> COLLABORATION_TOOLS_CAT

    lines = content.splitlines()
    new_lines = []
    current_level = None
    headers = []

    # First pass: load topic codes and category codes
    tsv_path.write_text(content, encoding="utf-8")
    tables = parse_master_tsv(tsv_path)
    topic_codes = {t["code"] for t in tables["topics"]}

    CONCEPT_RENAME = {
        "STATIC_MEMBERS": "STATIC_MEMBERS_CONCEPT",
        "FIRST_CLASS_FUNCTIONS": "FIRST_CLASS_FUNCTIONS_CONCEPT",
        "IMMUTABILITY": "IMMUTABILITY_CONCEPT",
        "ASYNCHRONOUS_PROG": "ASYNCHRONOUS_PROG_CONCEPT",
        "ROUTERS_SWITCHES": "ROUTERS_SWITCHES_CONCEPT",
        "PHYSICAL_MEDIA": "PHYSICAL_MEDIA_CONCEPT",
        "NETWORK_TOPOLOGIES": "NETWORK_TOPOLOGIES_CONCEPT",
        "IOT_PROTOCOLS_MQTT": "IOT_PROTOCOLS_MQTT_CONCEPT",
        "BASIC_MECHANISMS": "BASIC_MECHANISMS_CONCEPT",
        "BASIC_ELECTRONIC_COMPONENTS": "BASIC_ELECTRONIC_COMPONENTS_CONCEPT",
        "CIRCUIT_PRINCIPLES": "CIRCUIT_PRINCIPLES_CONCEPT",
        "PASSWORD_STRENGTH": "PASSWORD_STRENGTH_CONCEPT",
        "EVENT_HANDLERS": "EVENT_HANDLERS_CONCEPT",
        "MALWARE_TYPES": "MALWARE_TYPES_CONCEPT",
        "PHYSICS_CONSTRAINTS": "PHYSICS_CONSTRAINTS_CONCEPT",
        "UI_MODIFIERS": "UI_MODIFIERS_CONCEPT",
        "TROUBLESHOOTING_METHODOLOGY": "TROUBLESHOOTING_METHODOLOGY_CONCEPT",
        "ERROR_MESSAGES": "ERROR_MESSAGES_CONCEPT",
    }

    CONCEPT_EXPLICIT_TOPIC = {
        "MVVM_PATTERN": "OBSERVABLE_MODEL",
        "OBJECT_PROPERTIES": "CLASSES_OBJECTS",
        "SIMULATION_MODELING": "ALGO_STRATEGIES",
        "SHARED_EDITING_ETIQUETTE": "COLLABORATION_TOOLS",
        "INFORMATION_CREDIBILITY": "DIGITAL_INTERACTION",
        "DATA_DISTRIBUTIONS": "ALGO_ANALYSIS",
        "STATE_PROPERTY_WRAPPER": "STATE_MANAGEMENT",
        "API_INTEGRATION": "API_DESIGN",
        "RESPONSIVE_DESIGN": "ADAPTIVE_LAYOUT",
        "CLOUD_MODELS_IAAS_PAAS_SAAS": "SERVER_SIDE_LOGIC",
        "CLOUD_DEPLOYMENT_MODELS": "APP_DEPLOYMENT",
        "VIRTUALIZATION": "OS_PROCESS_MGMT",
        "MAPREDUCE_CONCEPT": "ALGO_STRATEGIES",
        "CAP_THEOREM": "SERVER_SIDE_LOGIC",
        "REGRESSION_CLASSIFICATION": "SUPERVISED_LEARNING",
        "CLUSTERING_ALGORITHMS": "UNSUPERVISED_LEARNING",
        "NEURAL_NETWORKS_BASICS": "SUPERVISED_LEARNING",
        "AI_HISTORY_MILESTONES": "SUPERVISED_LEARNING",
        "TYPES_OF_AI": "SUPERVISED_LEARNING",
        "AI_BIAS": "USER_RESEARCH",
        "ALGORITHMIC_BIAS_SOCIETY": "USER_RESEARCH",
        "IOT_SECURITY_THREATS": "NETWORK_ATTACKS",
        "IOT_SAFETY_RISKS": "NETWORK_ATTACKS",
        "USER_CENTERED_DESIGN": "USER_RESEARCH",
        "AFFORDANCES_SIGNIFIERS": "UI_UX_HEURISTICS",
        "FEEDBACK_AND_RESPONSE": "UI_UX_HEURISTICS",
        "DIGITAL_IDENTITY": "PRIVACY_SETTINGS",
        "DIGITAL_FOOTPRINT": "PRIVACY_SETTINGS",
        "CYBERBULLYING": "DIGITAL_INTERACTION",
        "COPYRIGHT_CREATIVE_COMMONS": "DIGITAL_INTERACTION",
        "DIGITAL_DIVIDE": "DIGITAL_INTERACTION",
        "IMAGE_WARPING": "RASTER_GRAPHICS_CONCEPTS",
        "IMAGE_RETOUCHING": "RASTER_GRAPHICS_CONCEPTS",
        "IMAGE_COMPOSITING": "RASTER_GRAPHICS_CONCEPTS",
        "PRIMITIVE_TYPE_DECLARATION": "PRIMITIVE_TYPES",
        "REFERENCE_TYPE_DECLARATION": "REFERENCE_TYPES",
        "AI_VS_ML": "SUPERVISED_LEARNING",
        "USABILITY_TESTING": "USER_RESEARCH",
        "LOGIC_ERRORS": "DEBUGGING_TECH",
        "SYNTAX_ERRORS": "ERROR_MESSAGES",
        "RUNTIME_ERRORS": "EXCEPTION_HANDLING",
        "DATABASE_NORMALIZATION": "RELATIONAL_DB",
        "STATISTICAL_MEASURES": "ALGO_ANALYSIS",
        "PROBABILITY_BASICS": "ALGO_ANALYSIS",
        "TWO_FACTOR_AUTH": "PASSWORD_STRENGTH",
        "APP_EXTENSION_MODEL": "MEDIA_SERVICES",
        "JSON_SERIALIZATION": "STRUCTURED_DATA_STORAGE",
        "COLLISION_DETECTION": "PHYSICS_CONSTRAINTS",
        "WEB_HOSTING": "APP_DEPLOYMENT",
        "WEB_BROWSER_ENGINES": "HTML_CSS",
        "UI_BOX_MODEL_LAYOUT": "STACK_LAYOUT",
        "FLEXBOX_GRID_LAYOUT": "GRID_LAYOUT",
        "PACKAGE_MANAGEMENT": "IDE_NAVIGATION",
        "MODULE_BUNDLERS": "IDE_NAVIGATION",
        "CODE_LINTING_FORMATTING": "IDE_NAVIGATION",
        "VCS_HOSTING": "GIT_BASICS",
        "AUTOMATED_TESTING_TOOLS": "UNIT_INTEGRATION_TESTING",
        "CROSS_ORIGIN_SECURITY": "FIREWALLS_IDS",
        "WEB_AUTHENTICATION_STRATEGIES": "ENCRYPTION_PROTOCOLS",
        "ABSTRACTION_LAYERS": "ALGO_STRATEGIES",
        "PROBLEM_DECOMPOSITION": "ALGO_STRATEGIES",
        "CREATIONAL_PATTERNS": "CLASSES_OBJECTS",
        "STRUCTURAL_PATTERNS": "CLASSES_OBJECTS",
        "BEHAVIORAL_PATTERNS": "CLASSES_OBJECTS",
        "AGILE_PRINCIPLES": "AGILE_SCRUM",
        "SCRUM_ROLES_EVENTS": "AGILE_SCRUM",
        "VERSION_CONTROL_WORKFLOW": "GIT_BASICS",
        "FRONTEND_FRAMEWORKS": "HTML_CSS",
        "BACKEND_FRAMEWORKS": "SERVER_SIDE_LOGIC",
        "RELATIONAL_VS_NONRELATIONAL": "RELATIONAL_DB",
        "DATA_EXPLORATION_EDA": "DATA_VIS_TOOLS",
        "DATA_CLEANING_TECHNIQUES": "DATA_VIS_TOOLS",
        "CHART_TYPES": "DATA_VIS_TOOLS",
    }

    TOPIC_EXPLICIT_CAT = {
        "APP_PROTOCOLS": "NETWORK_PROTOCOLS",
        "EDGE_FOG_CLOUD": "CLOUD_COMPUTING",
        "DIGITAL_INTERACTION": "DIGITAL_INTERACTION_CAT",
        "COLLABORATION_TOOLS": "COLLABORATION_TOOLS_CAT",
        "GRAPHIC_DESIGN_PRINCIPLES": "GRAPHIC_DESIGN_CAT",
        "APP_DEPLOYMENT": "DEVELOPMENT_ENVIRONMENT",
        "AI_ASSISTED_CODING": "AI_APPLICATIONS",
    }

    for line in lines:
        s = line.strip()
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

        parts = line.split("\t")
        if parts[0] == "code":
            headers = [h.strip() for h in parts]
            new_lines.append(line)
            continue

        if headers and len(parts) >= 2 and parts[0].strip():
            row_dict = {h: parts[i].strip() if i < len(parts) else "" for i, h in enumerate(headers)}
            code = row_dict["code"]

            if current_level == "categories":
                if code == "GRAPHIC_DESIGN_PRINCIPLES":
                    row_dict["code"] = "GRAPHIC_DESIGN_CAT"
                elif code == "DIGITAL_INTERACTION":
                    row_dict["code"] = "DIGITAL_INTERACTION_CAT"
                elif code == "COLLABORATION_TOOLS":
                    row_dict["code"] = "COLLABORATION_TOOLS_CAT"

            elif current_level == "topics":
                if code in TOPIC_EXPLICIT_CAT:
                    row_dict["category_codes"] = TOPIC_EXPLICIT_CAT[code]
                else:
                    cat_refs = row_dict.get("category_codes", "")
                    cat_refs = cat_refs.replace("GRAPHIC_DESIGN_PRINCIPLES", "GRAPHIC_DESIGN_CAT")
                    cat_refs = cat_refs.replace("DIGITAL_INTERACTION", "DIGITAL_INTERACTION_CAT")
                    cat_refs = cat_refs.replace("COLLABORATION_TOOLS", "COLLABORATION_TOOLS_CAT")
                    row_dict["category_codes"] = cat_refs

            elif current_level == "concepts":
                # Rename colliding concept codes
                original_code = code
                if code in CONCEPT_RENAME:
                    row_dict["code"] = CONCEPT_RENAME[code]

                if original_code in CONCEPT_EXPLICIT_TOPIC:
                    row_dict["topic_codes"] = CONCEPT_EXPLICIT_TOPIC[original_code]
                elif original_code in CONCEPT_RENAME:
                    row_dict["topic_codes"] = original_code
                else:
                    tc_refs = row_dict.get("topic_codes", "")
                    tc_refs = tc_refs.replace("GRAPHIC_DESIGN_PRINCIPLES", "GRAPHIC_DESIGN_PRINCIPLES")
                    tc_refs = tc_refs.replace("DIGITAL_INTERACTION", "DIGITAL_INTERACTION")
                    tc_refs = tc_refs.replace("COLLABORATION_TOOLS", "COLLABORATION_TOOLS")
                    row_dict["topic_codes"] = tc_refs

            new_line = "\t".join([row_dict.get(h, "") for h in headers])
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    final_content = "\n".join(new_lines)
    tsv_path.write_text(final_content, encoding="utf-8")
    print(f"✓ Cleaned and fixed {tsv_path}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else repo_root / "general-context/mlo-knowlege-tree.tsv"
    fix_tsv(target)
