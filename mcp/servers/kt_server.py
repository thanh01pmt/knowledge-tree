#!/usr/bin/env python3
"""
Sub-MCP Server: Knowledge Tree Operations (kt)
"""
import sys
import subprocess
from pathlib import Path
from fastmcp import FastMCP

# Paths
SERVER_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SERVER_DIR.parent.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"

kt_mcp = FastMCP("KnowledgeTreeOps")

@kt_mcp.tool
def validate_tree(project_name: str, fix: bool = False) -> str:
    """
    Kiểm tra tính toàn vẹn tham chiếu (referential integrity) của Knowledge Tree trong một dự án.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
        fix: Nếu True, tự động sửa các lỗi format an toàn và đề xuất phương án sửa lỗi.
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "validate_tree.py"
    if not script_path.exists():
        return f"Error: Cannot find validate_tree.py at {script_path}"
    
    cmd = [sys.executable, str(script_path), "--project", project_name, "--repo-root", str(ROOT_DIR)]
    if fix:
        cmd.append("--fix")
        
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    
    report_path = ROOT_DIR / "projects" / project_name / ".tree-validator" / "report" / "validation_report.md"
    report_content = ""
    if report_path.exists():
        report_content = "\n\n--- BÁO CÁO CHI TIẾT ---\n" + report_path.read_text(encoding="utf-8")
        
    output = res.stdout or res.stderr
    return f"Status Code: {res.returncode}\n{output}{report_content}"

@kt_mcp.tool
def detect_gaps(project_name: str) -> str:
    """
    Phát hiện 3 dạng lỗ hổng tri thức: Missing LO coverage, Shallow CIOs, và Master Candidates.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "detect_gaps.py"
    if not script_path.exists():
        return f"Error: Cannot find detect_gaps.py at {script_path}"
        
    cmd = [sys.executable, str(script_path), "--project", project_name, "--repo-root", str(ROOT_DIR)]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    
    report_path = ROOT_DIR / "projects" / project_name / ".tree-validator" / "gap_analysis_report.md"
    if report_path.exists():
        return report_path.read_text(encoding="utf-8")
        
    return res.stdout or res.stderr

@kt_mcp.tool
def audit_coverage(project_name: str) -> str:
    """
    Thực hiện kiểm tra đối chiếu ngược độ phủ syllabus (Reverse Coverage Audit) với tài liệu nguồn context.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "audit_coverage.py"
    if not script_path.exists():
        return f"Error: Cannot find audit_coverage.py at {script_path}"
        
    cmd = [sys.executable, str(script_path), "--project", project_name, "--repo-root", str(ROOT_DIR)]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    return res.stdout or res.stderr

@kt_mcp.tool
def sync_supabase(project_name: str) -> str:
    """
    Đồng bộ 6 file TSV của dự án (fields, subjects, categories, topics, concepts, learning-objectives) lên Supabase DB.
    
    Args:
        project_name: Tên dự án (ví dụ: 'roadmap_sh_graphql')
    """
    script_path = SKILLS_DIR / "supabase-sync" / "scripts" / "sync_to_supabase.py"
    if not script_path.exists():
        return f"Error: Cannot find sync_to_supabase.py at {script_path}"
        
    cmd = [sys.executable, str(script_path), "--project", project_name, "--repo-root", str(ROOT_DIR)]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    return res.stdout or res.stderr

@kt_mcp.tool
def scaffold_project(project_name: str) -> str:
    """
    Khởi tạo cấu trúc dự án mới và các header TSV đầu ra trong thư mục projects/<project_name>/.
    
    Args:
        project_name: Tên dự án mới (slug dạng kebab-case/snake_case)
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "scaffold_tree.py"
    if not script_path.exists():
        return f"Error: Cannot find scaffold_tree.py at {script_path}"
        
    cmd = [sys.executable, str(script_path), "--project", project_name, "--repo-root", str(ROOT_DIR)]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    return res.stdout or res.stderr
