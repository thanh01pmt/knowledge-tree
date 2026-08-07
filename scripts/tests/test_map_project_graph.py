#!/usr/bin/env python3
"""
Unit tests for scripts/map_project_graph.py (pure join logic, no subprocess / network).
"""
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.map_project_graph import extract_keywords_from_graph, build_concept_map


def test_keyword_extraction():
    print("Running test_keyword_extraction...")
    verified_graph = {
        "product": {
            "features": [
                {
                    "id": "F1",
                    "platform": "app",
                    "evidence": {
                        "imports": ["URLSession", "SwiftUI"],
                        "api_calls": ["fetchData"]
                    }
                },
                {
                    "id": "F2",
                    "platform": "app",
                    "evidence": {
                        "imports": ["URLSession", "WiFi.h"]
                    }
                },
                {
                    "id": "F3",
                    "platform": "esp32",
                    "evidence": {
                        "imports": ["URLSession"]
                    }
                }
            ]
        }
    }

    kw_list = extract_keywords_from_graph(verified_graph)

    # Assert shape
    for kw_item in kw_list:
        assert "keyword" in kw_item
        assert kw_item["source"] == "graph_evidence"
        assert "platform" in kw_item
        assert kw_item["weight"] == 1.0
        assert kw_item["context"].startswith("feature ")

    # Deduplication check:
    # URLSession (app) from F1 should be kept once.
    # URLSession (app) from F2 skipped.
    # URLSession (esp32) from F3 kept because platform differs.
    tokens_and_platforms = [(k["keyword"], k["platform"]) for k in kw_list]
    assert tokens_and_platforms == [
        ("URLSession", "app"),
        ("SwiftUI", "app"),
        ("fetchData", "app"),
        ("WiFi.h", "app"),
        ("URLSession", "esp32"),
    ]
    print("  test_keyword_extraction PASSED!")


def test_ca1_valid_join():
    print("Running Ca 1: Valid join...")
    verified_graph = {
        "schema_version": 1,
        "product": {
            "features": [
                {
                    "id": "F1",
                    "name": "App Feature",
                    "platform": "app",
                    "evidence": {
                        "imports": ["URLSession", "SwiftUI"]
                    }
                },
                {
                    "id": "F2",
                    "name": "ESP32 Firmware",
                    "platform": "esp32",
                    "evidence": {
                        "imports": ["WiFi.h"]
                    }
                }
            ]
        },
        "decomposition": {
            "milestones": [
                {
                    "id": "M1",
                    "name": "Integration Milestone",
                    "feature_ids": ["F1", "F2"]
                }
            ]
        }
    }

    resolved_fake = {
        "resolved": [
            {"keyword": "URLSession", "concept_codes": ["HTTP_PROTOCOL"]},
            {"keyword": "WiFi.h", "concept_codes": ["MEDIUM_TYPES"]}
        ]
    }

    concept_map = build_concept_map(verified_graph, resolved_fake)

    # Assert schema version
    assert concept_map["schema_version"] == 1

    # Assert feature_concepts
    assert concept_map["feature_concepts"]["F1"] == ["HTTP_PROTOCOL"]
    assert concept_map["feature_concepts"]["F2"] == ["MEDIUM_TYPES"]

    # Assert milestone_concepts (union of F1 + F2)
    assert concept_map["milestone_concepts"]["M1"] == ["HTTP_PROTOCOL", "MEDIUM_TYPES"]

    # Assert total union of concepts
    assert concept_map["concepts"] == ["HTTP_PROTOCOL", "MEDIUM_TYPES"]

    # Assert keyword_evidence
    assert concept_map["keyword_evidence"]["URLSession"] == ["HTTP_PROTOCOL"]
    assert concept_map["keyword_evidence"]["WiFi.h"] == ["MEDIUM_TYPES"]
    assert "SwiftUI" not in concept_map["keyword_evidence"]

    print("  Ca 1 PASSED!")


def test_ca2_unresolved_token():
    print("Running Ca 2: Evidence token not in resolved (no fabrication)...")
    verified_graph = {
        "schema_version": 1,
        "product": {
            "features": [
                {
                    "id": "F1",
                    "name": "Custom Feature",
                    "platform": "app",
                    "evidence": {
                        "imports": ["UnknownHeader.h", "CustomLib"]
                    }
                }
            ]
        },
        "decomposition": {
            "milestones": [
                {
                    "id": "M1",
                    "name": "Standalone Milestone",
                    "feature_ids": ["F1"]
                }
            ]
        }
    }

    resolved_fake = {
        "resolved": [
            # Neither UnknownHeader.h nor CustomLib is resolved
        ]
    }

    concept_map = build_concept_map(verified_graph, resolved_fake)

    # feature_concepts and milestone_concepts should be empty
    assert concept_map["feature_concepts"]["F1"] == []
    assert concept_map["milestone_concepts"]["M1"] == []
    assert concept_map["concepts"] == []

    # Evidence tokens without concept resolution should not be in keyword_evidence
    assert "UnknownHeader.h" not in concept_map["keyword_evidence"]
    assert "CustomLib" not in concept_map["keyword_evidence"]

    print("  Ca 2 PASSED!")


def test_escalated_concepts_join():
    print("Running test_escalated_concepts_join...")
    verified_graph = {
        "product": {
            "features": [
                {
                    "id": "F1",
                    "platform": "app",
                    "evidence": {
                        "imports": ["Foundation", "Task"]
                    }
                }
            ]
        },
        "decomposition": {
            "milestones": [
                {
                    "id": "M1",
                    "feature_ids": ["F1"]
                }
            ]
        }
    }

    resolved_fake = {
        "resolved": [
            {"keyword": "Foundation", "concept_codes": ["STANDARD_LIBRARY"]}
        ]
    }

    escalated_fake = {
        "escalated": [
            {"keyword": "Task", "concept_code": "ASYNC_PATTERNS"}
        ]
    }

    concept_map = build_concept_map(verified_graph, resolved_fake, escalated_fake)

    assert concept_map["feature_concepts"]["F1"] == ["ASYNC_PATTERNS", "STANDARD_LIBRARY"]
    assert concept_map["milestone_concepts"]["M1"] == ["ASYNC_PATTERNS", "STANDARD_LIBRARY"]
    assert concept_map["concepts"] == ["ASYNC_PATTERNS", "STANDARD_LIBRARY"]
    assert concept_map["keyword_evidence"]["Foundation"] == ["STANDARD_LIBRARY"]
    assert concept_map["keyword_evidence"]["Task"] == ["ASYNC_PATTERNS"]

    print("  test_escalated_concepts_join PASSED!")


def main():
    print("=== Running test_map_project_graph.py ===")
    test_keyword_extraction()
    test_ca1_valid_join()
    test_ca2_unresolved_token()
    test_escalated_concepts_join()
    print("=== ALL TESTS PASSED ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
