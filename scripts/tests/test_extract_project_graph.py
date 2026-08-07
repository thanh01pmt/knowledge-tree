#!/usr/bin/env python3
"""
test_extract_project_graph.py — Unit tests for scripts/extract_project_graph.py

Runs standalone with python scripts/tests/test_extract_project_graph.py (no pytest dependency).
"""

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from extract_project_graph import (
    collect_repo_files,
    load_and_cap_file_contents,
    validate_shape,
    build_prompt,
)


def test_collect_repo_files():
    print("[TEST] test_collect_repo_files...")
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Create dummy files
        f_swift = root / "MainView.swift"
        f_swift.write_text("import SwiftUI\n" + "x" * 100)

        f_ino = root / "firmware.ino"
        f_ino.write_text("void setup() {}\n" + "y" * 200)

        f_py = root / "script.py"
        f_py.write_text("print('hello')\n" + "z" * 500)

        f_txt = root / "readme.txt"
        f_txt.write_text("Documentation")

        # Ignored dirs
        node_modules = root / "node_modules"
        node_modules.mkdir()
        (node_modules / "pkg.js").write_text("console.log('pkg')")

        build_dir = root / ".build"
        build_dir.mkdir()
        (build_dir / "Build.swift").write_text("swift code")

        # Test collecting files max_files=2
        collected = collect_repo_files(root, max_files=2)
        assert len(collected) == 2, f"Expected 2 files, got {len(collected)}"

        names = {p.name for p in collected}
        # .swift and .ino should be prioritized over .py
        assert "MainView.swift" in names or "firmware.ino" in names, f"Expected swift/ino, got {names}"
        assert "pkg.js" not in names, "node_modules should be ignored"
        assert "Build.swift" not in names, ".build directory should be ignored"
        assert "readme.txt" not in names, ".txt extension should be ignored"

        # Test collecting all files
        all_collected = collect_repo_files(root, max_files=10)
        assert len(all_collected) == 3, f"Expected 3 valid files, got {len(all_collected)}"

    print("  -> PASSED")


def test_load_and_cap_file_contents():
    print("[TEST] test_load_and_cap_file_contents...")
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        f1 = root / "a.swift"
        f1.write_text("Line 1\nLine 2\nLine 3\n")

        f2 = root / "b.py"
        f2.write_text("print('a')\nprint('b')\n")

        # Test capping chars
        res = load_and_cap_file_contents(root, [f1, f2], max_chars=30)
        assert len(res) <= 30, f"Expected len <= 30, got {len(res)}"
        assert "=== File: a.swift ===" in res, "Header for file 1 should be included"

        # Test reading full content
        res_full = load_and_cap_file_contents(root, [f1, f2], max_chars=1000)
        assert "=== File: a.swift ===" in res_full
        assert "=== File: b.py ===" in res_full
        assert "Line 1" in res_full
        assert "print('a')" in res_full

    print("  -> PASSED")


def test_validate_shape():
    print("[TEST] test_validate_shape...")

    # (a) Valid dictionary with all required keys
    valid_data = {
        "schema_version": 1,
        "project": {
            "name": "smart-bulb-controller",
            "project_type": "multi_target",
            "platforms": ["app", "esp32"]
        },
        "product": {
            "purpose": "Control smart bulb via WiFi",
            "features": [
                {
                    "id": "F1",
                    "name": "Toggle Light",
                    "description": "User can turn light on/off",
                    "files": ["SmartBulb/ContentView.swift"],
                    "platform": "app"
                }
            ],
            "user_journeys": [
                {"name": "Connect and Control", "feature_ids": ["F1"]}
            ]
        },
        "architecture": {
            "layers": [
                {"name": "presentation", "component_names": ["ContentView"]}
            ],
            "services": [
                {"name": "HTTPBulbService", "file": "HTTPBulbService.swift", "responsibility": "Send HTTP requests"}
            ],
            "state_management": "@State",
            "communication": [
                {"from": "app", "to": "esp32", "protocol": "HTTP"}
            ]
        },
        "decomposition": {
            "milestones": [
                {
                    "id": "M1",
                    "phase": "MVP",
                    "name": "Basic On/Off",
                    "goal": "Turn bulb on and off",
                    "feature_ids": ["F1"],
                    "files": ["ContentView.swift"],
                    "acceptance": "App toggles bulb status",
                    "depends_on": []
                }
            ]
        }
    }
    assert validate_shape(valid_data) is True, "Valid dictionary should pass validate_shape"

    # (b) Missing 'decomposition' key -> fail
    invalid_data_missing_decomp = {
        "schema_version": 1,
        "project": {"name": "test", "project_type": "app", "platforms": ["app"]},
        "product": {"purpose": "test", "features": [], "user_journeys": []},
        "architecture": {"layers": [], "services": [], "state_management": None, "communication": []}
    }
    assert validate_shape(invalid_data_missing_decomp) is False, "Missing decomposition should fail"

    # (c) Features is not a list -> fail
    invalid_data_features = {
        "schema_version": 1,
        "project": {"name": "test", "project_type": "app", "platforms": ["app"]},
        "product": {"purpose": "test", "features": "invalid_string_not_list", "user_journeys": []},
        "architecture": {"layers": [], "services": [], "state_management": None, "communication": []},
        "decomposition": {"milestones": []}
    }
    assert validate_shape(invalid_data_features) is False, "Non-list features should fail"

    # (d) Non-dict input -> fail
    assert validate_shape("not a dict") is False, "String input should fail"
    assert validate_shape(None) is False, "None input should fail"

    print("  -> PASSED")


def test_build_prompt():
    print("[TEST] test_build_prompt...")
    system, user = build_prompt("code content sample", tech_stack="SwiftUI + ESP32")

    # Prompt MUST NOT reference Knowledge Tree or pedagogical concepts
    assert "knowledge tree" not in system.lower(), "System prompt must not mention Knowledge Tree"
    assert "knowledge tree" not in user.lower(), "User prompt must not mention Knowledge Tree"
    assert "concept sư phạm" not in system.lower(), "System prompt must not mention concept sư phạm"
    assert "concept sư phạm" not in user.lower(), "User prompt must not mention concept sư phạm"

    assert "SwiftUI + ESP32" in user, "User prompt should include tech stack"
    assert "code content sample" in user, "User prompt should include file contents"

    print("  -> PASSED")


def test_smart_bulb_fixture_file_selection():
    print("[TEST] test_smart_bulb_fixture_file_selection...")
    fixture_dir = REPO_ROOT / "scripts" / "tests" / "fixtures" / "smart-bulb-repo"
    assert fixture_dir.exists(), f"Fixture dir missing at {fixture_dir}"

    collected = collect_repo_files(fixture_dir, max_files=8)
    assert len(collected) == 3, f"Expected 3 files in smart-bulb-repo, got {len(collected)}"

    file_names = {p.name for p in collected}
    expected_files = {"smart_bulb.ino", "HTTPBulbService.swift", "ContentView.swift"}
    assert file_names == expected_files, f"Expected {expected_files}, got {file_names}"

    contents = load_and_cap_file_contents(fixture_dir, collected, max_chars=20000)
    assert "=== File: ContentView.swift ===" in contents or "=== File: SmartBulb/ContentView.swift ===" in contents
    assert "=== File: smart_bulb.ino ===" in contents

    print("  -> PASSED")


def main():
    test_collect_repo_files()
    test_load_and_cap_file_contents()
    test_validate_shape()
    test_build_prompt()
    test_smart_bulb_fixture_file_selection()
    print("\n[ALL TESTS PASSED SUCCESSFULLY]")


if __name__ == "__main__":
    main()
