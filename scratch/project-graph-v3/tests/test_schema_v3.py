#!/usr/bin/env python3
"""Test cho Project Graph v3 schema + canonical constraints."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "schemas" / "project_graph.schema.v3.json"
EXAMPLE_PATH = HERE.parent / "schemas" / "project_graph.example.weather.json"


def load(name: str, path: Path) -> dict:
    if not path.is_file():
        print(f"❌ Thiếu file {name}: {path}")
        sys.exit(1)
    return json.load(open(path, encoding="utf-8"))


def main():
    from jsonschema import Draft7Validator

    schema = load("schema", SCHEMA_PATH)
    example = load("example", EXAMPLE_PATH)

    # 1. Schema hợp lệ Draft-07
    Draft7Validator.check_schema(schema)
    print("  ✓ Schema hợp lệ Draft-07")

    # 2. Example khớp schema
    v = Draft7Validator(schema)
    errors = sorted(v.iter_errors(example), key=lambda e: list(e.path))
    assert not errors, f"Example lỗi schema: {[e.message for e in errors[:3]]}"
    print(f"  ✓ Example weather khớp schema ({len(errors)} errors)")

    # 3. Canonical constraints (không nằm trong JSON Schema thuần)
    # 3a. Không chứa nội dung giảng dạy (boundary D8)
    forbidden_teaching_keys = {"bloom_level", "quiz", "lesson_sequence", "mastery"}
    def walk_forbidden(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.lower() in forbidden_teaching_keys:
                    return f"{path}.{k}"
                r = walk_forbidden(v, f"{path}.{k}")
                if r: return r
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                r = walk_forbidden(v, f"{path}[{i}]")
                if r: return r
        return None
    forbidden = walk_forbidden(example)
    assert forbidden is None, f"Project Graph chứa nội dung giảng dạy: {forbidden}"
    print("  ✓ Không chứa bloom/quiz/mastery (boundary D8)")

    # 3b. Task phải có intent + outcome (D7 — WHY→WHAT→HOW)
    for task in example["implementation"]["tasks"]:
        assert task.get("intent"), f"Task {task['id']} thiếu intent"
        assert task.get("outcome"), f"Task {task['id']} thiếu outcome"
    print("  ✓ Mọi task có intent + outcome (D7)")

    # 3c. Architecture INFERRED phải có confidence + evidence (D6)
    for node in example["architecture"]["nodes"]:
        if node.get("evidence_type") == "INFERRED":
            assert node.get("confidence") is not None, f"Node {node['id']} INFERRED thiếu confidence"
    print("  ✓ INFERRED nodes có confidence (D6)")

    # 3d. Edge types thuộc canonical set (không 'related_to')
    edge_enum = schema["definitions"]["edges"]["items"]["properties"]["type"]["enum"]
    assert "related_to" not in edge_enum, "Cấm edge generic 'related_to'"
    print(f"  ✓ {len(edge_enum)} canonical edge types, không 'related_to'")

    print("\nALL PROJECT GRAPH V3 SCHEMA TESTS PASSED!")


if __name__ == "__main__":
    main()
