#!/usr/bin/env python3
"""
Sub-MCP Server: Knowledge Tree Operations (kt)
"""
import re
import sys
import subprocess
from pathlib import Path
from fastmcp import FastMCP

# Paths
SERVER_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SERVER_DIR.parent.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"

kt_mcp = FastMCP("KnowledgeTreeOps")

# Safe project slug: lowercase letters, digits, hyphens, underscores only.
# Prevents path traversal (../, /, ..) in MCP tool calls.
SAFE_SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*$')


def _validate_project_name(project_name: str) -> str:
    """Validate project_name to prevent path traversal and injection.
    Returns the slug if safe, raises ValueError otherwise."""
    if not project_name or not SAFE_SLUG_RE.match(project_name):
        raise ValueError(
            f"Invalid project_name '{project_name}'. "
            "Only lowercase letters, digits, hyphens, and underscores are allowed."
        )
    if ".." in project_name or "/" in project_name or "\\" in project_name:
        raise ValueError(f"project_name '{project_name}' contains path traversal characters.")
    return project_name


def _run_script(script_path: Path, project_name: str, extra_args: list = None,
                timeout: int = 300) -> str:
    """Run a skill script with validation, timeout, and error handling.
    Default timeout 300s (5 min) prevents hung subprocesses.
    Returns a string that includes exit code prefix for error propagation."""
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"
    if not script_path.exists():
        return f"Error: Cannot find {script_path.name} at {script_path}"
    cmd = [sys.executable, str(script_path), "--project", project_name] + (extra_args or [])
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=timeout)
        output = res.stdout or res.stderr
        # Propagate exit code so caller (LLM agent) knows if the tool failed.
        # Non-zero exit = script failed (e.g., LLM call error, validation error).
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED — do not trust TSV files written by this run.")
        return output
    except subprocess.TimeoutExpired:
        return f"❌ Error: {script_path.name} timed out after {timeout}s for project '{project_name}'."

@kt_mcp.tool
def validate_tree(project_name: str, fix: bool = False) -> str:
    """
    Kiểm tra tính toàn vẹn tham chiếu (referential integrity) của Knowledge Tree trong một dự án.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
        fix: Nếu True, tự động sửa các lỗi format an toàn và đề xuất phương án sửa lỗi.
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "validate_tree.py"
    extra = ["--fix"] if fix else []
    output = _run_script(script_path, project_name, extra_args=extra, timeout=120)

    reports_dir = ROOT_DIR / "projects" / project_name / ".tree-validator" / "reports"
    report_content = ""
    if reports_dir.is_dir():
        candidates = sorted(reports_dir.glob("*/validation_report.md"), reverse=True)
        if candidates:
            report_content = "\n\n--- BÁO CÁO CHI TIẾT ---\n" + candidates[0].read_text(encoding="utf-8")

    return f"{output}{report_content}"

@kt_mcp.tool
def detect_gaps(project_name: str) -> str:
    """
    Phát hiện 4 dạng lỗ hổng tri thức: Missing LO coverage (A), Shallow CIOs (B), Master Candidates (C), và Marr test violations (D).

    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "detect_gaps.py"
    output = _run_script(script_path, project_name, timeout=120)

    reports_dir = ROOT_DIR / "projects" / project_name / ".tree-validator" / "reports"
    if reports_dir.is_dir():
        candidates = sorted(reports_dir.glob("*/gap_report.md"), reverse=True)
        if candidates:
            return candidates[0].read_text(encoding="utf-8")

    return output

@kt_mcp.tool
def audit_coverage(project_name: str) -> str:
    """
    Thực hiện kiểm tra đối chiếu ngược độ phủ syllabus (Reverse Coverage Audit) với tài liệu nguồn context.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "audit_coverage.py"
    output = _run_script(script_path, project_name, timeout=120)

    # Also return the full coverage report if available (previously only stdout)
    reports_dir = ROOT_DIR / "projects" / project_name / ".tree-validator" / "reports"
    if reports_dir.is_dir():
        candidates = sorted(reports_dir.glob("*/coverage_report.md"), reverse=True)
        if candidates:
            report_content = "\n\n--- BÁO CÁO CHI TIẾT ---\n" + candidates[0].read_text(encoding="utf-8")
            return f"{output}{report_content}"

    return output

@kt_mcp.tool
def sync_supabase(project_name: str) -> str:
    """
    Đồng bộ 6 file TSV của dự án (fields, subjects, categories, topics, concepts, learning-objectives) lên Supabase DB.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
    """
    script_path = SKILLS_DIR / "supabase-sync" / "scripts" / "sync_to_supabase.py"
    return _run_script(script_path, project_name, timeout=600)

@kt_mcp.tool
def scaffold_project(project_name: str) -> str:
    """
    Khởi tạo cấu trúc dự án mới và các header TSV đầu ra trong thư mục projects/<project_name>/.
    
    Args:
        project_name: Tên dự án mới (slug dạng kebab-case/snake_case, chỉ gồm chữ thường, số, gạch ngang/gạch dưới)
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "scaffold_tree.py"
    if not script_path.exists():
        return f"Error: Cannot find scaffold_tree.py at {script_path}"

    # scaffold_tree.py takes positional arg (not --project)
    cmd = [sys.executable, str(script_path), project_name]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=60)
        return res.stdout or res.stderr
    except subprocess.TimeoutExpired:
        return f"❌ Error: scaffold_tree.py timed out after 60s."

@kt_mcp.tool
def map_prerequisites(project_name: str, dry_run: bool = False, no_verify: bool = False,
                      reuse_concept_dag: bool = False) -> str:
    """
    Sinh DAG tiền đề (prerequisite) giữa các Learning Objectives theo phương pháp 4-Bước ADR-0005:
    Domain Partitioning → Concept DAG per-domain (LLM) → ULO Derivation → LLM Verify (phép thử ngược).
    
    Output: lo_prerequisites.tsv (có source_layer, justification, counterfactual_test)
            concepts.tsv (thêm cột prerequisite_concept_codes)
            .work/concept_dag.tsv (concept-level DAG audit trail)
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        dry_run: Nếu True, in candidate DAG ra stdout, không ghi TSV
        no_verify: Nếu True, bỏ Bước 4 (LLM verify — chỉ chạy Bước 1+2+3)
        reuse_concept_dag: Nếu True, dùng .work/concept_dag.tsv có sẵn, skip Bước 2 (tiết kiệm LLM calls)
    """
    script_path = SKILLS_DIR / "learning-objective-generator" / "scripts" / "llm_map_prerequisites.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_map_prerequisites.py at {script_path}"

    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    cmd = [sys.executable, str(script_path), "--project", project_name]
    if dry_run:
        cmd.append("--dry-run")
    if no_verify:
        cmd.append("--no-verify")
    if reuse_concept_dag:
        cmd.append("--reuse-concept-dag")

    try:
        # LLM calls can be slow — 30 min timeout
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=1800)
        return res.stdout or res.stderr
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_map_prerequisites.py timed out after 1800s for project '{project_name}'."
