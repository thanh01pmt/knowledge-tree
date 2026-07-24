#!/usr/bin/env python3
"""
Sub-MCP Server: System Status & Resources (sys)
"""
from pathlib import Path
from fastmcp import FastMCP

SERVER_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SERVER_DIR.parent.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"

sys_mcp = FastMCP("SystemOps")

@sys_mcp.tool
def get_system_status() -> str:
    """Trả về thông tin trạng thái hoạt động của hệ thống Knowledge Tree."""
    status_file = ROOT_DIR / "status.yaml"
    if status_file.exists():
        return f"=== STATUS.YAML ===\n{status_file.read_text(encoding='utf-8')}"
    return "Status file not found."

@sys_mcp.resource("skills://{skill_name}")
def get_skill_doc(skill_name: str) -> str:
    """Đọc tài liệu hướng dẫn SKILL.md của một skill trong dự án."""
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    return f"Skill '{skill_name}' không tồn tại tại {skill_file}"

@sys_mcp.resource("project://{project_name}/status")
def get_project_status(project_name: str) -> str:
    """Đọc thông tin trạng thái dự án hiện tại từ status.yaml ở repo root."""
    status_file = ROOT_DIR / "status.yaml"
    if status_file.exists():
        return status_file.read_text(encoding="utf-8")
    return "Chưa có file status.yaml."

@sys_mcp.prompt
def guide_workflow(step_name: str, project_name: str) -> str:
    """
    Cung cấp hướng dẫn quy trình từng bước cho Agent theo chuẩn Pipeline.
    """
    guides = {
        "init": f"Thao tác khởi tạo dự án '{project_name}'. Hãy gọi tool 'kt_scaffold_project(project_name=\"{project_name}\")'.",
        "context-audit": f"Đọc toàn bộ tài liệu nguồn trong projects/{project_name}/context/ và trích xuất danh sách chủ đề tri thức.",
        "map-taxonomy": f"Đối chiếu danh sách chủ đề với Master Knowledge Tree trong general-context/ và tạo file mapping-plan.md tại projects/{project_name}/.work/.",
        "build-tree": f"Dựa trên mapping-plan.md đã duyệt, xây dựng 6 file TSV đầu ra trong projects/{project_name}/output/.",
        "validate-tree": f"Gọi tool 'kt_validate_tree(project_name=\"{project_name}\")' để kiểm tra tính hợp lệ và tự động khắc phục các lỗi tham chiếu.",
        "sync-supabase": f"Gọi tool 'kt_sync_supabase(project_name=\"{project_name}\")' để đồng bộ dữ liệu TSV lên cơ sở dữ liệu Supabase Cloud."
    }
    return guides.get(step_name, f"Không tìm thấy hướng dẫn cho bước '{step_name}'. Các bước khả thi: {list(guides.keys())}")
