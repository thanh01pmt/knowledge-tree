#!/usr/bin/env python3
"""
FastMCP v3 Server for Knowledge Tree Operations
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

# Base Directories
MCP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = MCP_DIR.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"

mcp = FastMCP("Knowledge Tree MCP Server")

# ---------------------------------------------------------------------------
# Custom Routes (Health check)
# ---------------------------------------------------------------------------
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({
        "status": "healthy",
        "service": "Knowledge Tree FastMCP Server",
        "version": "0.1.0"
    })

# ---------------------------------------------------------------------------
# MCP Tools (Functions)
# ---------------------------------------------------------------------------
@mcp.tool
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

@mcp.tool
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

@mcp.tool
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

@mcp.tool
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

@mcp.tool
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

# ---------------------------------------------------------------------------
# MCP Resources
# ---------------------------------------------------------------------------
@mcp.resource("skills://{skill_name}")
def get_skill_doc(skill_name: str) -> str:
    """Đọc tài liệu hướng dẫn SKILL.md của một skill trong dự án."""
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    return f"Skill '{skill_name}' không tồn tại tại {skill_file}"

@mcp.resource("project://{project_name}/status")
def get_project_status(project_name: str) -> str:
    """Đọc thông tin trạng thái dự án hiện tại từ status.yaml ở repo root."""
    status_file = ROOT_DIR / "status.yaml"
    if status_file.exists():
        return status_file.read_text(encoding="utf-8")
    return "Chưa có file status.yaml."

# ---------------------------------------------------------------------------
# MCP Prompts
# ---------------------------------------------------------------------------
@mcp.prompt
def guide_workflow(step_name: str, project_name: str) -> str:
    """
    Cung cấp hướng dẫn quy trình từng bước cho Agent theo chuẩn Pipeline.
    
    Args:
        step_name: Tên bước (như 'init', 'context-audit', 'map-taxonomy', 'build-tree', 'validate-tree', 'sync-supabase')
        project_name: Tên dự án đang làm việc
    """
    guides = {
        "init": f"Thao tác khởi tạo dự án '{project_name}'. Hãy gọi tool 'scaffold_project(project_name=\"{project_name}\")'.",
        "context-audit": f"Đọc toàn bộ tài liệu nguồn trong projects/{project_name}/context/ và trích xuất danh sách chủ đề tri thức.",
        "map-taxonomy": f"Đối chiếu danh sách chủ đề với Master Knowledge Tree trong general-context/ và tạo file mapping-plan.md tại projects/{project_name}/.work/.",
        "build-tree": f"Dựa trên mapping-plan.md đã duyệt, xây dựng 6 file TSV đầu ra trong projects/{project_name}/output/.",
        "validate-tree": f"Gọi tool 'validate_tree(project_name=\"{project_name}\")' để kiểm tra tính hợp lệ và tự động khắc phục các lỗi tham chiếu.",
        "sync-supabase": f"Gọi tool 'sync_supabase(project_name=\"{project_name}\")' để đồng bộ dữ liệu TSV lên cơ sở dữ liệu Supabase Cloud."
    }
    return guides.get(step_name, f"Không tìm thấy hướng dẫn cho bước '{step_name}'. Các bước khả thi: {list(guides.keys())}")

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Check transport environment variable
    transport = os.getenv("FASTMCP_TRANSPORT", "stdio").lower()
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", "8000"))
    
    if transport in ("http", "sse", "streamable-http"):
        print(f"🚀 Running FastMCP Server via {transport.upper()} on {host}:{port}")
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run()
