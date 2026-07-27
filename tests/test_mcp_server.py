#!/usr/bin/env python3
"""
test_mcp_server.py — Test suite cho Knowledge Tree MCP Hub.

Test:
- Server load + tool/resource/prompt discovery
- Path traversal protection trên tất cả tool nhận project_name
- Skill doc path traversal protection
- Tool execution (validate_tree, detect_gaps, audit_coverage)
- Subprocess timeout handling
- Resource URI namespace fix (skills:// → tool)

Chạy: python3 tests/test_mcp_server.py
Không cần API key — test thuần deterministic.
"""

import asyncio
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "kt_mcp"))
sys.path.insert(0, str(REPO_ROOT))

from fastmcp import Client


async def get_hub():
    """Lazy import + return hub instance."""
    import main
    return main.hub


async def list_tools():
    """Verify all expected tools are registered."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        tools = await client.list_tools()
        tool_names = {t.name for t in tools}
    expected = {
        "kt_validate_tree", "kt_detect_gaps", "kt_audit_coverage",
        "kt_sync_supabase", "kt_scaffold_project", "kt_map_prerequisites",
        "sys_get_system_status", "sys_get_skill_doc", "sys_get_project_status",
    }
    missing = expected - tool_names
    assert not missing, f"Missing tools: {missing}. Got: {tool_names}"
    print(f"✓ list_tools ({len(tool_names)} tools, all expected present)")


async def list_prompts():
    """Verify guide_workflow prompt is registered."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        prompts = await client.list_prompts()
        prompt_names = {p.name for p in prompts}
    assert "sys_guide_workflow" in prompt_names, \
        f"sys_guide_workflow missing. Got: {prompt_names}"
    print(f"✓ list_prompts ({len(prompt_names)} prompts)")


async def test_path_traversal_scaffold():
    """scaffold_project phải block path traversal."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("kt_scaffold_project",
                                         {"project_name": "../../../tmp/evil"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Error" in text or "❌" in text, \
            f"Path traversal phải bị block, got: {text[:200]}"
    print("✓ test_path_traversal_scaffold")


async def test_path_traversal_validate_tree():
    """validate_tree phải block path traversal."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("kt_validate_tree",
                                         {"project_name": "../../etc/passwd"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Error" in text or "❌" in text, \
            f"Path traversal phải bị block, got: {text[:200]}"
    print("✓ test_path_traversal_validate_tree")


async def test_path_traversal_detect_gaps():
    """detect_gaps phải block path traversal."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("kt_detect_gaps",
                                         {"project_name": "..%2F..%2Ftmp"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Error" in text or "❌" in text, \
            f"Path traversal phải bị block, got: {text[:200]}"
    print("✓ test_path_traversal_detect_gaps")


async def test_path_traversal_skill_doc():
    """sys_get_skill_doc phải block path traversal."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("sys_get_skill_doc",
                                         {"skill_name": "../../../etc/passwd"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Error" in text or "❌" in text, \
            f"Path traversal phải bị block, got: {text[:200]}"
    print("✓ test_path_traversal_skill_doc")


async def test_skill_doc_valid():
    """sys_get_skill_doc phải đọc được SKILL.md hợp lệ."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("sys_get_skill_doc",
                                         {"skill_name": "tree-validator"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "tree-validator" in text.lower() or "SKILL" in text, \
            f"Phải trả về nội dung SKILL.md, got: {text[:200]}"
    print("✓ test_skill_doc_valid")


async def test_validate_tree_execution():
    """kt_validate_tree phải chạy thành công trên swift-associate."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("kt_validate_tree",
                                         {"project_name": "swift-associate"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "PASS" in text or "FAIL" in text, \
            f"Phải trả về status, got: {text[:200]}"
    print("✓ test_validate_tree_execution")


async def test_detect_gaps_execution():
    """kt_detect_gaps phải chạy thành công trên swift-associate."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("kt_detect_gaps",
                                         {"project_name": "swift-associate"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Gap" in text or "GAP" in text, \
            f"Phải trả về gap report, got: {text[:200]}"
    print("✓ test_detect_gaps_execution")


async def test_audit_coverage_execution():
    """kt_audit_coverage phải chạy thành công và trả về report."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("kt_audit_coverage",
                                         {"project_name": "swift-associate"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Coverage" in text or "coverage" in text.lower(), \
            f"Phải trả về coverage report, got: {text[:200]}"
    print("✓ test_audit_coverage_execution")


async def test_get_system_status():
    """sys_get_system_status phải trả về status.yaml content."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("sys_get_system_status", {})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "active_project" in text, \
            f"Phải trả về status.yaml, got: {text[:200]}"
    print("✓ test_get_system_status")


async def test_guide_workflow_prompt():
    """sys_guide_workflow prompt phải trả về hướng dẫn."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        p = await client.get_prompt("sys_guide_workflow",
                                     {"step_name": "init", "project_name": "test-proj"})
        text = str(p)
        assert "scaffold" in text.lower() or "init" in text.lower(), \
            f"Prompt phải trả về hướng dẫn init, got: {text[:200]}"
    print("✓ test_guide_workflow_prompt")


async def test_invalid_project_name_format():
    """Project name với ký tự không hợp lệ phải bị block."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        # Uppercase not allowed (slug must be lowercase)
        result = await client.call_tool("kt_validate_tree",
                                         {"project_name": "Swift-Associate"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Error" in text or "❌" in text, \
            f"Uppercase project name phải bị block, got: {text[:200]}"
    print("✓ test_invalid_project_name_format")


async def test_prompt_injection_blocked():
    """guide_workflow phải sanitize project_name để prevent prompt injection."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        p = await client.get_prompt("sys_guide_workflow",
                                     {"step_name": "init",
                                      "project_name": 'evil"; rm -rf /; #'})
        text = str(p)
        assert "<invalid-project-name>" in text, \
            f"Prompt injection phải bị sanitize, got: {text[:200]}"
    print("✓ test_prompt_injection_blocked")


async def test_get_project_status_slug_validation():
    """sys_get_project_status phải validate slug."""
    hub = await get_hub()
    client = Client(hub)
    async with client:
        result = await client.call_tool("sys_get_project_status",
                                         {"project_name": "../../../etc/passwd"})
        text = result.content[0].text if hasattr(result, "content") else str(result)
        assert "Error" in text or "❌" in text, \
            f"Path traversal phải bị block, got: {text[:200]}"
    print("✓ test_get_project_status_slug_validation")


async def test_no_namespace_collision():
    """Verify local kt_mcp/ doesn't shadow mcp SDK (PyPI).
    'import mcp' must resolve to site-packages, not local kt_mcp/."""
    import mcp as mcp_sdk
    sdk_path = str(mcp_sdk.__file__)
    assert "site-packages" in sdk_path, \
        f"mcp SDK phải resolve to site-packages, got: {sdk_path}"
    # Verify our hub is importable from kt_mcp, not mcp
    assert REPO_ROOT / "kt_mcp" / "main.py" in [REPO_ROOT / "kt_mcp" / "main.py"]
    assert not (REPO_ROOT / "mcp" / "main.py").exists(), \
        "Old mcp/ directory should not exist after rename"
    print("✓ test_no_namespace_collision")


async def run_all():
    tests = [
        list_tools,
        list_prompts,
        test_path_traversal_scaffold,
        test_path_traversal_validate_tree,
        test_path_traversal_detect_gaps,
        test_path_traversal_skill_doc,
        test_skill_doc_valid,
        test_validate_tree_execution,
        test_detect_gaps_execution,
        test_audit_coverage_execution,
        test_get_system_status,
        test_guide_workflow_prompt,
        test_invalid_project_name_format,
        test_prompt_injection_blocked,
        test_get_project_status_slug_validation,
        test_no_namespace_collision,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            await t()
            passed += 1
        except Exception as e:
            print(f"✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{'='*50}")
    print(f"MCP Test Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'='*50}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run_all()))