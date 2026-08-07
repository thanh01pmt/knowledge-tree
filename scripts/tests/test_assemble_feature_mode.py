#!/usr/bin/env python3
"""
test_assemble_feature_mode.py — Unit & Integration tests for scripts/assemble_roadmap.py
testing legacy vertical mode and new project-graph feature mode.

Runs 3 test cases without external dependencies:
- Ca 1 (regression): Legacy flow with bulb9 fixtures -> 12 milestones, 3 phases (matches roadmap_final.json).
- Ca 2 (feature mode): Inline project graph (F1, F2 -> M1 MVP) + concept map (F1 -> HTTP_PROTOCOL, F2 -> FOR_LOOP)
  + bulb9 fixtures -> 1 milestone named M1 with LOs of both concepts, phase 1, ULO+CIO+SIO for each concept.
- Ca 3: Run without --project-graph -> output identical to Ca 1 (shape + total milestones).
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Add repository root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

SCRIPT_DIR = Path(__file__).parent.parent
FIXTURE_DIR = SCRIPT_DIR / "tests" / "fixtures" / "bulb9"
ASSEMBLE_SCRIPT = SCRIPT_DIR / "assemble_roadmap.py"

MATCHED_CIOS = FIXTURE_DIR / "matched_cios.json"
RESOLVED_SIOS = FIXTURE_DIR / "resolved_sios.json"
PREREQUISITES = FIXTURE_DIR / "prerequisites.json"
JIT_LOS = FIXTURE_DIR / "jit_los.json"
ROADMAP_FINAL = FIXTURE_DIR / "roadmap_final.json"


def test_ca1_regression():
    print("Running Ca 1 (regression test)...")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp_out:
        out_path = Path(tmp_out.name)

    cmd = [
        sys.executable,
        str(ASSEMBLE_SCRIPT),
        "--matched-cios", str(MATCHED_CIOS),
        "--resolved-sios", str(RESOLVED_SIOS),
        "--prerequisites", str(PREREQUISITES),
        "--jit-los", str(JIT_LOS),
        "--vertical",
        "--output", str(out_path),
        "--goal", "Học Swift và SwiftUI...",
        "--tech-stack", "Swift, SwiftUI, URLSession, ESP32"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Script failed with code {res.returncode}: {res.stderr}"

    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(ROADMAP_FINAL, "r", encoding="utf-8") as f:
        expected = json.load(f)

    assert "project_brief" in data
    assert "phases" in data
    assert "total_milestones" in data
    assert "total_concepts" in data

    assert data["total_milestones"] == 12, f"Expected 12 milestones, got {data['total_milestones']}"
    assert len(data["phases"]) == 3, f"Expected 3 phases, got {len(data['phases'])}"
    assert data["total_milestones"] == expected["total_milestones"]
    assert len(data["phases"]) == len(expected["phases"])

    out_path.unlink(missing_ok=True)
    print("  Ca 1 PASSED!")


def test_ca2_feature_mode():
    print("Running Ca 2 (feature mode test)...")
    graph_data = {
        "schema_version": 1,
        "product": {
            "features": [
                {"id": "F1", "name": "HTTP Service"},
                {"id": "F2", "name": "Loop Logic"}
            ]
        },
        "decomposition": {
            "milestones": [
                {
                    "id": "M1",
                    "name": "M1",
                    "phase": "MVP",
                    "feature_ids": ["F1", "F2"]
                }
            ]
        }
    }

    concept_map_data = {
        "schema_version": 1,
        "feature_concepts": {
            "F1": ["HTTP_PROTOCOL"],
            "F2": ["FOR_LOOP"]
        },
        "milestone_concepts": {
            "M1": ["HTTP_PROTOCOL", "FOR_LOOP"]
        }
    }

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f_graph, \
         tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f_cmap, \
         tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f_out:

        graph_path = Path(f_graph.name)
        cmap_path = Path(f_cmap.name)
        out_path = Path(f_out.name)

        json.dump(graph_data, f_graph)
        f_graph.flush()
        json.dump(concept_map_data, f_cmap)
        f_cmap.flush()

    cmd = [
        sys.executable,
        str(ASSEMBLE_SCRIPT),
        "--matched-cios", str(MATCHED_CIOS),
        "--resolved-sios", str(RESOLVED_SIOS),
        "--prerequisites", str(PREREQUISITES),
        "--jit-los", str(JIT_LOS),
        "--project-graph", str(graph_path),
        "--concept-map", str(cmap_path),
        "--output", str(out_path),
        "--goal", "Test Feature Mode",
        "--tech-stack", "Swift, ESP32"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Script failed with code {res.returncode}: {res.stderr}"

    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "phases" in data
    assert len(data["phases"]) == 1, f"Expected 1 phase, got {len(data['phases'])}"
    phase = data["phases"][0]
    assert phase["phase_id"] == 1, f"Expected phase_id 1, got {phase['phase_id']}"
    assert phase["title"] == "MVP"

    assert len(phase["milestones"]) == 1, f"Expected 1 milestone, got {len(phase['milestones'])}"
    milestone = phase["milestones"][0]
    assert milestone["name"] == "M1" or milestone["id"] == "M1"

    los = milestone["learning_objectives"]
    concepts_in_milestone = {lo.get("concept") for lo in los}
    assert "HTTP_PROTOCOL" in concepts_in_milestone, f"Missing HTTP_PROTOCOL in {concepts_in_milestone}"
    assert "FOR_LOOP" in concepts_in_milestone, f"Missing FOR_LOOP in {concepts_in_milestone}"

    lo_types_per_concept = {}
    for lo in los:
        c = lo.get("concept")
        if c not in lo_types_per_concept:
            lo_types_per_concept[c] = set()
        lo_types_per_concept[c].add(lo.get("lo_type"))

    for c in ["HTTP_PROTOCOL", "FOR_LOOP"]:
        types = lo_types_per_concept.get(c, set())
        assert "UNIVERSAL" in types, f"Concept {c} missing UNIVERSAL (ULO)"
        assert "CONCEPTUAL_IMPL" in types, f"Concept {c} missing CONCEPTUAL_IMPL (CIO)"
        assert "SPECIFIC_IMPL" in types, f"Concept {c} missing SPECIFIC_IMPL (SIO)"

    graph_path.unlink(missing_ok=True)
    cmap_path.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)
    print("  Ca 2 PASSED!")


def test_ca3_no_project_graph():
    print("Running Ca 3 (no project-graph flag test)...")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f_out1, \
         tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f_out2:
        out1_path = Path(f_out1.name)
        out2_path = Path(f_out2.name)

    cmd1 = [
        sys.executable,
        str(ASSEMBLE_SCRIPT),
        "--matched-cios", str(MATCHED_CIOS),
        "--resolved-sios", str(RESOLVED_SIOS),
        "--prerequisites", str(PREREQUISITES),
        "--jit-los", str(JIT_LOS),
        "--vertical",
        "--output", str(out1_path)
    ]
    res1 = subprocess.run(cmd1, capture_output=True, text=True)
    assert res1.returncode == 0, f"Ca 3 baseline failed: {res1.stderr}"

    cmd2 = [
        sys.executable,
        str(ASSEMBLE_SCRIPT),
        "--matched-cios", str(MATCHED_CIOS),
        "--resolved-sios", str(RESOLVED_SIOS),
        "--prerequisites", str(PREREQUISITES),
        "--jit-los", str(JIT_LOS),
        "--vertical",
        "--output", str(out2_path)
    ]
    res2 = subprocess.run(cmd2, capture_output=True, text=True)
    assert res2.returncode == 0, f"Ca 3 run failed: {res2.stderr}"

    with open(out1_path, "r", encoding="utf-8") as f:
        data1 = json.load(f)
    with open(out2_path, "r", encoding="utf-8") as f:
        data2 = json.load(f)

    assert data1["total_milestones"] == data2["total_milestones"] == 12
    assert len(data1["phases"]) == len(data2["phases"]) == 3
    assert data1 == data2

    out1_path.unlink(missing_ok=True)
    out2_path.unlink(missing_ok=True)
    print("  Ca 3 PASSED!")


def main():
    print("Executing test_assemble_feature_mode.py...")
    test_ca1_regression()
    test_ca2_feature_mode()
    test_ca3_no_project_graph()
    print("\nALL TESTS IN test_assemble_feature_mode.py PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
