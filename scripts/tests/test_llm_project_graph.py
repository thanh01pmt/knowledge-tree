#!/usr/bin/env python3
"""
test_llm_project_graph.py — Unit tests for scripts/llm_project_graph.py.
No LLM calls required (pure code tests with mocks).
"""

import os
import sys
import tempfile
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import llm_project_graph as lpg


def test_ca1_collect_target_files_fallback():
    print("Running Test Ca 1: collect_target_files on smart-bulb-repo fallback...")
    fixture_repo = Path(__file__).resolve().parent / "fixtures" / "smart-bulb-repo"
    assert fixture_repo.exists(), f"Fixture directory {fixture_repo} does not exist"

    paths, file_map = lpg.collect_target_files(fixture_repo, target="auto")
    assert len(paths) == 3, f"Expected 3 files in smart-bulb-repo fallback, got {len(paths)}"

    file_names = {p.name for p in paths}
    expected_names = {"smart_bulb.ino", "HTTPBulbService.swift", "ContentView.swift"}
    assert file_names == expected_names, f"Expected {expected_names}, got {file_names}"
    print("  ✓ Ca 1 PASSED!")


def test_ca2_build_sdk_api_index():
    print("Running Test Ca 2: build_sdk_api_index with temp SDK & App fixture...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sources_dir = tmp_path / "Sources"
        app_dir = tmp_path / "DemoApp"
        sources_dir.mkdir()
        app_dir.mkdir()

        # SDK File with public class and public func
        sdk_file = sources_dir / "ChatSDK.swift"
        sdk_file.write_text(
            "public class ChatClient {\n"
            "    public func connect() {}\n"
            "}\n"
            "public class UnusedSDKClient {}\n",
            encoding="utf-8"
        )

        # App File using ChatClient but NOT UnusedSDKClient
        app_file = app_dir / "MainView.swift"
        app_file.write_text(
            "import ChatSDK\n"
            "let client = ChatClient()\n"
            "client.connect()\n",
            encoding="utf-8"
        )

        target_paths, file_map = lpg.collect_target_files(tmp_path, target="demo_app")
        assert len(target_paths) == 1, f"Expected 1 app file, got {len(target_paths)}"

        sdk_index = lpg.build_sdk_api_index(tmp_path, target_paths, file_map)
        apis = {item["name"]: item["used_in_demo"] for item in sdk_index.get("sdk_apis", [])}

        assert "ChatClient" in apis, "ChatClient missing from sdk_apis"
        assert apis["ChatClient"] is True, "ChatClient used_in_demo should be True"

        assert "UnusedSDKClient" in apis, "UnusedSDKClient missing from sdk_apis"
        assert apis["UnusedSDKClient"] is False, "UnusedSDKClient used_in_demo should be False"

        assert sdk_index.get("used_in_demo") >= 1, "used_in_demo count should be >= 1"

    print("  ✓ Ca 2 PASSED!")


def test_ca3_verify_project_graph():
    print("Running Test Ca 3: verify_project_graph ground-truth filtering...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        real_file = tmp_path / "RealApp.swift"
        real_file.write_text("struct ContentView {\n    var body: @State int = 0\n    let client = ChatClient()\n}", encoding="utf-8")

        file_contents = {"RealApp.swift": real_file.read_text(encoding="utf-8")}

        sdk_api_index = {
            "sdk_apis": [
                {"name": "ChatClient", "kind": "class", "used_in_demo": True}
            ],
            "used_in_demo": 1
        }

        mock_llm_graph = {
            "product": {
                "features": [
                    {
                        "id": "F1",
                        "name": "Chat View",
                        "files": ["RealApp.swift", "FakeApp.swift"],
                        "api_usage": ["ChatClient", "FakeAPI"],
                        "keywords": ["@State", "FakeKeywordThatDoesNotExistAnywhere"]
                    }
                ]
            }
        }

        verified, hallucinations = lpg.verify_project_graph(mock_llm_graph, tmp_path, sdk_api_index, file_contents)
        f1 = verified["product"]["features"][0]

        # Assert fake items removed
        assert "FakeApp.swift" not in f1["files"], "FakeApp.swift should be removed"
        assert "RealApp.swift" in f1["files"], "RealApp.swift should be kept"

        assert "FakeAPI" not in f1["api_usage"], "FakeAPI should be removed"
        assert "ChatClient" in f1["api_usage"], "ChatClient should be kept"

        assert "FakeKeywordThatDoesNotExistAnywhere" not in f1["keywords"], "FakeKeyword should be removed"
        assert "@State" in f1["keywords"], "@State should be kept"

        # Assert hallucinations recorded
        h_types = {h["type"] for h in hallucinations}
        assert "file" in h_types, "File hallucination should be recorded"
        assert "api" in h_types, "API hallucination should be recorded"
        assert "keyword" in h_types, "Keyword hallucination should be recorded"

    print("  ✓ Ca 3 PASSED!")


def test_ca4_concept_map_join():
    print("Running Test Ca 4: concept map join with evidence_files...")
    mock_verified_graph = {
        "product": {
            "features": [
                {
                    "id": "F1",
                    "name": "Chat Feature",
                    "files": ["DemoApp/ChatView.swift", "DemoApp/Helpers.swift"],
                    "api_usage": ["ChatClient"],
                    "keywords": ["NavigationStack"]
                }
            ]
        }
    }

    file_contents = {
        "DemoApp/ChatView.swift": "import ChatSDK\nstruct ChatView {\n    let client = ChatClient()\n}",
        "DemoApp/Helpers.swift": "struct NavHelper {\n    // NavigationStack usage\n}"
    }

    mock_concept_map_override = {
        "ChatClient": {"concept_code": "CHAT_CLIENT_API", "concept_name": "Chat Client API"},
        "NavigationStack": {"concept_code": "NAVIGATION_STACK", "concept_name": "Navigation Stack"}
    }

    fc = lpg.escalate_and_map_concepts(mock_verified_graph, file_contents, concept_map_override=mock_concept_map_override)

    assert "F1" in fc, "Feature F1 missing from feature_concepts"
    f1_concepts = fc["F1"]
    assert len(f1_concepts) == 2, f"Expected 2 concept entries for F1, got {len(f1_concepts)}"

    chat_client_entry = next((c for c in f1_concepts if c["keyword"] == "ChatClient"), None)
    assert chat_client_entry is not None, "ChatClient entry missing"
    assert chat_client_entry["concept_code"] == "CHAT_CLIENT_API"
    assert chat_client_entry["evidence_files"] == ["DemoApp/ChatView.swift"], f"Evidence files error: {chat_client_entry['evidence_files']}"

    nav_entry = next((c for c in f1_concepts if c["keyword"] == "NavigationStack"), None)
    assert nav_entry is not None, "NavigationStack entry missing"
    assert nav_entry["concept_code"] == "NAVIGATION_STACK"
    assert nav_entry["evidence_files"] == ["DemoApp/Helpers.swift"], f"Evidence files error: {nav_entry['evidence_files']}"

    print("  ✓ Ca 4 PASSED!")


def main():
    print("=" * 60)
    print("Running unit tests for scripts/llm_project_graph.py...")
    print("=" * 60)

    test_ca1_collect_target_files_fallback()
    test_ca2_build_sdk_api_index()
    test_ca3_verify_project_graph()
    test_ca4_concept_map_join()

    print("\n✅ All unit tests in test_llm_project_graph.py PASSED!")
    sys.exit(0)


if __name__ == "__main__":
    main()
