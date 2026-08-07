#!/usr/bin/env python3
"""
Test PipelineOrchestrator Step Wiring (Phase B4 integration)

Verifies that step_1_3_extract_project_graph, step_1_4_verify_project_graph,
and step_3_6_map_concepts are properly wired into generate_roadmap_v3.py.
"""

import ast
import inspect
import sys
import tempfile
from pathlib import Path

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(scripts_dir))

from generate_roadmap_v3 import PipelineOrchestrator


def test_step_methods_exist():
    print("Running Test 1: Assert 3 new step methods exist and are callable...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        fixture_repo = Path(__file__).parent / "fixtures" / "smart-bulb-repo"

        orchestrator = PipelineOrchestrator(
            goal="Build Smart Bulb iOS App",
            tech_stack="Swift,SwiftUI",
            output_dir=tmp_path,
            repo_dir=fixture_repo,
        )

        target_methods = [
            "step_1_3_extract_project_graph",
            "step_1_4_verify_project_graph",
            "step_3_6_map_concepts",
        ]

        for method_name in target_methods:
            assert hasattr(orchestrator, method_name), f"Missing method {method_name} in PipelineOrchestrator"
            method = getattr(orchestrator, method_name)
            assert callable(method), f"Method {method_name} is not callable"
            print(f"  ✓ Method '{method_name}' exists and is callable.")

    print("  Test 1 PASSED!")


def test_steps_list_order():
    print("Running Test 2: Assert steps list order in run_pipeline source...")
    file_path = scripts_dir / "generate_roadmap_v3.py"
    src = file_path.read_text(encoding="utf-8")
    tree = ast.parse(src)

    step_ids = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "run_pipeline":
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name) and target.id == "steps":
                            if isinstance(stmt.value, ast.List):
                                for elt in stmt.value.elts:
                                    if isinstance(elt, ast.Tuple) and len(elt.elts) >= 1:
                                        first = elt.elts[0]
                                        if isinstance(first, ast.Constant):
                                            step_ids.append(first.value)
                                        elif isinstance(first, ast.Str):
                                            step_ids.append(first.s)

    print(f"  Extracted step IDs: {step_ids}")

    required_steps = ["step_1_3", "step_1_4", "step_3_6"]
    for s in required_steps:
        assert s in step_ids, f"Step '{s}' missing from run_pipeline steps list"

    idx_1_2 = step_ids.index("step_1_2")
    idx_1_3 = step_ids.index("step_1_3")
    idx_1_4 = step_ids.index("step_1_4")
    idx_3 = step_ids.index("step_3")
    idx_3_5 = step_ids.index("step_3_5")
    idx_3_6 = step_ids.index("step_3_6")
    idx_4 = step_ids.index("step_4")

    # Assert 1_3 before 1_4, 1_4 before 3, 3_5 before 3_6, 3_6 before 4
    assert idx_1_2 < idx_1_3, f"step_1_3 ({idx_1_3}) should be after step_1_2 ({idx_1_2})"
    assert idx_1_3 < idx_1_4, f"step_1_4 ({idx_1_4}) should be after step_1_3 ({idx_1_3})"
    assert idx_1_4 < idx_3, f"step_1_4 ({idx_1_4}) should be before step_3 ({idx_3})"
    assert idx_3_5 < idx_3_6, f"step_3_6 ({idx_3_6}) should be after step_3_5 ({idx_3_5})"
    assert idx_3_6 < idx_4, f"step_3_6 ({idx_3_6}) should be before step_4 ({idx_4})"

    print("  Test 2 PASSED!")


def test_step_8_7_artifact_references():
    print("Running Test 3: Assert step_8_7 references project_graph_verified and concept_map...")
    src = inspect.getsource(PipelineOrchestrator.step_8_7_assemble_roadmap)
    assert "project_graph_verified" in src, "step_8_7 source does not reference 'project_graph_verified'"
    assert "concept_map" in src, "step_8_7 source does not reference 'concept_map'"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        orchestrator = PipelineOrchestrator(
            goal="Test Goal",
            tech_stack="Swift",
            output_dir=tmp_path,
        )

        # Check default paths for artifacts in orchestrator._artifact
        pg_v = orchestrator._artifact("project_graph_verified", "project_graph_verified.json")
        c_m = orchestrator._artifact("concept_map", "concept_map.json")

        assert pg_v.name == "project_graph_verified.json"
        assert c_m.name == "concept_map.json"

        # Mocking artifacts presence in state
        orchestrator._complete("step_1_4", project_graph_verified=pg_v)
        orchestrator._complete("step_3_6", concept_map=c_m)

        assert orchestrator.state["artifacts"]["project_graph_verified"] == str(pg_v)
        assert orchestrator.state["artifacts"]["concept_map"] == str(c_m)

    print("  Test 3 PASSED!")


def main():
    print("=" * 60)
    print("RUNNING ORCHESTRATOR STEPS INTEGRATION TESTS (Phase B4)")
    print("=" * 60)

    test_step_methods_exist()
    test_steps_list_order()
    test_step_8_7_artifact_references()

    print("\nALL ORCHESTRATOR STEP WIRING TESTS PASSED SUCCESSFULLY! (Exit 0)")
    sys.exit(0)


if __name__ == "__main__":
    main()
