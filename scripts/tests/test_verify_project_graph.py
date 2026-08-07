#!/usr/bin/env python3
"""
Unit tests for scripts/verify_project_graph.py (Phase B2).

Runs 3 test cases without LLM calls:
- Ca 1: Valid graph -> verified preserved with evidence, hallucinations empty.
- Ca 2: Hallucinated file 'FakeService.swift' -> moved to hallucinations, removed from verified.
- Ca 3: Mismatched platform ('esp32' claimed for ContentView.swift) -> corrected to 'app' + warning.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Add repository root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.verify_project_graph import verify_project_graph


def get_base_graph_fixture():
    return {
        "schema_version": 1,
        "project": {
            "name": "smart-bulb-controller",
            "project_type": "multi_target",
            "platforms": ["app", "esp32"]
        },
        "product": {
            "purpose": "Smart bulb controller",
            "features": [
                {
                    "id": "F1",
                    "name": "App UI & Service",
                    "description": "Control bulb from iOS App",
                    "files": ["ContentView.swift", "HTTPBulbService.swift"],
                    "platform": "app"
                },
                {
                    "id": "F2",
                    "name": "ESP32 Firmware",
                    "description": "Arduino firmware for WS2812 LED strip",
                    "files": ["smart_bulb.ino"],
                    "platform": "esp32"
                }
            ],
            "user_journeys": [
                {"name": "Control Bulb", "feature_ids": ["F1", "F2"]}
            ]
        },
        "architecture": {
            "layers": [
                {"name": "presentation", "component_names": ["ContentView"]},
                {"name": "service", "component_names": ["HTTPBulbService"]}
            ],
            "services": [
                {"name": "HTTPBulbService", "file": "HTTPBulbService.swift", "responsibility": "HTTP REST API"}
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
                    "name": "Basic Control",
                    "goal": "Turn bulb on and off",
                    "feature_ids": ["F1", "F2"],
                    "files": ["ContentView.swift", "HTTPBulbService.swift", "smart_bulb.ino"],
                    "acceptance": "Bulb turns on/off",
                    "depends_on": []
                }
            ]
        }
    }


def test_ca1_valid_graph(repo_dir: Path):
    print("Running Ca 1: Valid graph...")
    graph_data = get_base_graph_fixture()
    verified, hallucinations = verify_project_graph(graph_data, repo_dir)

    # Assertions
    features = verified["product"]["features"]
    assert len(features) == 2, f"Expected 2 features, got {len(features)}"
    assert features[0]["files"] == ["ContentView.swift", "HTTPBulbService.swift"]
    assert features[1]["files"] == ["smart_bulb.ino"]

    # Evidence assertions
    f1_evidence = features[0]["evidence"]
    assert "SwiftUI" in f1_evidence["imports"], f"Missing SwiftUI import in F1 evidence: {f1_evidence['imports']}"
    assert "Foundation" in f1_evidence["imports"], f"Missing Foundation import in F1 evidence: {f1_evidence['imports']}"
    assert "@State" in f1_evidence["property_wrappers"], f"Missing @State in F1 evidence: {f1_evidence['property_wrappers']}"
    assert "ContentView" in f1_evidence["type_usages"], f"Missing ContentView in F1 type_usages"

    f2_evidence = features[1]["evidence"]
    assert "WiFi.h" in f2_evidence["imports"], f"Missing WiFi.h in F2 evidence: {f2_evidence['imports']}"
    assert "handleGetState" in f2_evidence["api_calls"], f"Missing handleGetState in F2 api_calls"

    # Hallucinations check
    assert len(hallucinations["missing_files"]) == 0, f"Expected 0 missing files, got {hallucinations['missing_files']}"
    assert len(hallucinations["invalid_symbols"]) == 0, f"Expected 0 invalid symbols, got {hallucinations['invalid_symbols']}"
    print("  Ca 1 PASSED!")


def test_ca2_hallucinated_file(repo_dir: Path):
    print("Running Ca 2: Hallucinated file 'FakeService.swift'...")
    graph_data = get_base_graph_fixture()
    graph_data["product"]["features"][0]["files"].append("FakeService.swift")
    graph_data["decomposition"]["milestones"][0]["files"].append("FakeService.swift")

    verified, hallucinations = verify_project_graph(graph_data, repo_dir)

    # Assertions
    f1_files = verified["product"]["features"][0]["files"]
    assert "FakeService.swift" not in f1_files, "FakeService.swift should be removed from verified features"
    assert f1_files == ["ContentView.swift", "HTTPBulbService.swift"]

    m1_files = verified["decomposition"]["milestones"][0]["files"]
    assert "FakeService.swift" not in m1_files, "FakeService.swift should be removed from verified milestones"

    assert "FakeService.swift" in hallucinations["missing_files"], f"FakeService.swift should be in missing_files: {hallucinations['missing_files']}"
    print("  Ca 2 PASSED!")


def test_ca3_mismatched_platform(repo_dir: Path):
    print("Running Ca 3: Mismatched platform ('esp32' claimed for ContentView.swift)...")
    graph_data = get_base_graph_fixture()
    graph_data["product"]["features"][0]["platform"] = "esp32"  # Incorrect claim by LLM

    verified, hallucinations = verify_project_graph(graph_data, repo_dir)

    # Assertions
    f1 = verified["product"]["features"][0]
    assert f1["platform"] == "app", f"Platform should be corrected to 'app', got '{f1['platform']}'"
    assert len(verified["warnings"]) > 0, "Expected warnings for platform correction"
    assert any("corrected from 'esp32' to 'app'" in w for w in verified["warnings"]), f"Warning message mismatch: {verified['warnings']}"
    print("  Ca 3 PASSED!")


def test_ca4_fuzzy_friendly_name_passes(repo_dir: Path):
    print("Running Ca 4: Friendly-name symbols ('WebServer','PubSubClient') must PASS fuzzy match...")
    graph_data = get_base_graph_fixture()
    # Real symbols exist in smart_bulb.ino as #include <WebServer.h> etc.
    graph_data["architecture"]["layers"] = [
        {"name": "firmware", "component_names": ["WebServer", "PubSubClient", "Adafruit_NeoPixel", "WiFiClient"]},
    ]
    graph_data["architecture"]["services"] = [
        {"name": "WebServer", "file": "smart_bulb.ino", "responsibility": "REST endpoint on ESP32"},
    ]

    verified, hallucinations = verify_project_graph(graph_data, repo_dir)

    comps = verified["architecture"]["layers"][0]["component_names"]
    for c in ["WebServer", "PubSubClient", "Adafruit_NeoPixel", "WiFiClient"]:
        assert c in comps, f"Real friendly symbol '{c}' must survive fuzzy match, got comps={comps}"
    svc_names = [s["name"] for s in verified["architecture"]["services"]]
    assert "WebServer" in svc_names, f"Service 'WebServer' must pass fuzzy match, got {svc_names}"
    assert "WebServer" not in hallucinations.get("invalid_symbols", []), "WebServer wrongly flagged as hallucination"
    print("  Ca 4 PASSED!")


def test_ca5_genuine_fake_symbol_still_fails(repo_dir: Path):
    print("Running Ca 5: Genuinely absent symbol must STILL be flagged...")
    graph_data = get_base_graph_fixture()
    graph_data["architecture"]["layers"] = [
        {"name": "firmware", "component_names": ["BluetoothStack", "ZigbeeCoordinator"]},
    ]

    verified, hallucinations = verify_project_graph(graph_data, repo_dir)

    comps = verified["architecture"]["layers"][0]["component_names"]
    assert "BluetoothStack" not in comps, f"Fake symbol 'BluetoothStack' must be removed, got {comps}"
    assert "ZigbeeCoordinator" not in comps, f"Fake symbol 'ZigbeeCoordinator' must be removed, got {comps}"
    inv = hallucinations.get("invalid_symbols", [])
    assert any("BluetoothStack" in str(x) for x in inv) or any(h.get("component") == "BluetoothStack" for h in hallucinations.get("hallucinations", [])), f"BluetoothStack must be in hallucinations, got {hallucinations}"
    print("  Ca 5 PASSED!")


def test_cli_execution(repo_dir: Path):
    print("Running CLI execution smoke test...")
    graph_data = get_base_graph_fixture()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        graph_json = tmp_path / "input_graph.json"
        verified_json = tmp_path / "verified_graph.json"
        hallucinations_json = tmp_path / "hallucinations.json"

        with open(graph_json, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2)

        script_path = Path(__file__).parent.parent / "verify_project_graph.py"

        cmd = [
            sys.executable,
            str(script_path),
            "--project-graph", str(graph_json),
            "--repo-dir", str(repo_dir),
            "--output", str(verified_json),
            "--hallucinations-output", str(hallucinations_json)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"CLI process exited with non-zero code {result.returncode}:\nStdout: {result.stdout}\nStderr: {result.stderr}"

        assert verified_json.is_file(), "CLI failed to output verified_graph.json"
        assert hallucinations_json.is_file(), "CLI failed to output hallucinations.json"

        with open(verified_json, "r", encoding="utf-8") as f:
            v_data = json.load(f)

        assert "evidence" in v_data["product"]["features"][0], "Verified JSON missing evidence field"
        print("  CLI execution smoke test PASSED!")


def main():
    repo_dir = Path(__file__).parent / "fixtures" / "smart-bulb-repo"
    assert repo_dir.is_dir(), f"Fixture repo directory not found: {repo_dir}"

    print(f"Testing verify_project_graph against fixture repo: {repo_dir}")
    test_ca1_valid_graph(repo_dir)
    test_ca2_hallucinated_file(repo_dir)
    test_ca3_mismatched_platform(repo_dir)
    test_ca4_fuzzy_friendly_name_passes(repo_dir)
    test_ca5_genuine_fake_symbol_still_fails(repo_dir)
    test_cli_execution(repo_dir)

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! (Exit code 0)")


if __name__ == "__main__":
    main()
