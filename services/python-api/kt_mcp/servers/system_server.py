#!/usr/bin/env python3
"""
Sub-MCP Server: System Status & Resources (sys)
"""
import re
from pathlib import Path
from fastmcp import FastMCP

SERVER_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SERVER_DIR.parent.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"

sys_mcp = FastMCP("SystemOps")

# Safe project slug for resource URIs (prevents path traversal via resource read).
SAFE_SLUG_RE = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$')


def _validate_slug(slug: str) -> str:
    """Validate a slug used in resource URIs to prevent path traversal."""
    if not slug or not SAFE_SLUG_RE.match(slug):
        raise ValueError(f"Invalid slug '{slug}'")
    if ".." in slug or "/" in slug or "\\" in slug:
        raise ValueError(f"Slug '{slug}' contains path traversal characters.")
    return slug


@sys_mcp.tool
def get_system_status() -> str:
    """Trả về thông tin trạng thái hoạt động của hệ thống Knowledge Tree."""
    status_file = ROOT_DIR / "status.yaml"
    if status_file.exists():
        return f"=== STATUS.YAML ===\n{status_file.read_text(encoding='utf-8')}"
    return "Status file not found."

@sys_mcp.tool
def get_skill_doc(skill_name: str) -> str:
    """
    Đọc tài liệu hướng dẫn SKILL.md của một skill trong dự án.

    Args:
        skill_name: Tên skill (ví dụ: 'tree-validator', 'taxonomy-mapper')
    """
    try:
        _validate_slug(skill_name)
    except ValueError as e:
        return f"❌ Error: {e}"
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    # Defense-in-depth: verify resolved path stays inside SKILLS_DIR
    if not skill_file.resolve().is_relative_to(SKILLS_DIR.resolve()):
        return f"❌ Error: Resolved skill path escapes skills directory."
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    return f"Skill '{skill_name}' không tồn tại tại {skill_file}"

@sys_mcp.tool
def get_project_status(project_name: str) -> str:
    """
    Đọc thông tin trạng thái dự án hiện tại từ status.yaml ở repo root.

    Args:
        project_name: Tên dự án (slug, chỉ để tham chiếu — status.yaml ở repo root)
    """
    try:
        _validate_slug(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"
    status_file = ROOT_DIR / "status.yaml"
    if status_file.exists():
        return status_file.read_text(encoding="utf-8")
    return "Chưa có file status.yaml."

@sys_mcp.prompt
def guide_workflow(step_name: str, project_name: str) -> str:
    """
    Cung cấp hướng dẫn quy trình từng bước cho Agent theo chuẩn Pipeline.
    """
    # Sanitize project_name to prevent prompt injection in generated text.
    try:
        _validate_slug(project_name)
        safe_name = project_name
    except ValueError:
        safe_name = "<invalid-project-name>"
    guides = {
        "init": f"Thao tác khởi tạo dự án '{safe_name}'. Hãy gọi tool 'kt_scaffold_project(project_name=\"{safe_name}\")'.",
        "context-audit": f"Đọc toàn bộ tài liệu nguồn trong projects/{safe_name}/context/ và trích xuất danh sách chủ đề tri thức.",
        "map-taxonomy": f"Đối chiếu danh sách chủ đề với Master Knowledge Tree trong .agents/skills/taxonomy-mapper/resources/ và tạo file mapping-plan.md tại projects/{safe_name}/.work/.",
        "build-tree": f"Dựa trên mapping-plan.md đã duyệt, xây dựng 6 file TSV đầu ra trong projects/{safe_name}/output/.",
        "validate-tree": f"Gọi tool 'kt_validate_tree(project_name=\"{safe_name}\")' để kiểm tra tính hợp lệ và tự động khắc phục các lỗi tham chiếu.",
        "sync-supabase": f"Gọi tool 'kt_sync_supabase(project_name=\"{safe_name}\")' để đồng bộ dữ liệu TSV lên cơ sở dữ liệu Supabase Cloud."
    }
    return guides.get(step_name, f"Không tìm thấy hướng dẫn cho bước '{step_name}'. Các bước khả thi: {list(guides.keys())}")


# ─── HITL Artifact Resources (Read-Only) ──────────────────────────────────────

# These resources expose intermediate files that require human review at HITL checkpoints.
# URI pattern: project://{project_name}/work/{artifact_name}

HITL_ARTIFACTS = {
    "verify-report": ".work/kw/verify-report.md",                    # Checkpoint 1: ATE term verification
    "concept-escalation": ".work/kw/concept_escalation.md",          # Checkpoint 2: New concept proposals (Gap D)
    "context-audit": ".work/context-audit.md",                       # Checkpoint 3: Domain/syllabus analysis
    "mapping-plan": ".work/mapping-plan.md",                         # Checkpoint 4: Taxonomy mapping proposal
    "ulos-preview": ".work/hlo/ulos_preview.md",                     # Checkpoint 5: ULO review
    "cios-preview": ".work/hlo/cios_preview.md",                     # Checkpoint 6: CIO Marr Test review
    "validation-report": ".tree-validator/reports/latest/validation_report.md",  # Checkpoint 7: Post-validation
    "coverage-report": ".tree-validator/reports/latest/coverage_report.md",      # Coverage audit
    "gap-report": ".tree-validator/reports/latest/gap_report.md",                # Gap detection
}


def _get_latest_report_dir(project_name: str) -> Path | None:
    """Find the latest timestamped report directory for a project."""
    reports_dir = ROOT_DIR / "projects" / project_name / ".tree-validator" / "reports"
    if not reports_dir.is_dir():
        return None
    candidates = sorted(reports_dir.iterdir(), reverse=True)
    return candidates[0] if candidates else None


for artifact_name, artifact_path_template in HITL_ARTIFACTS.items():
    # Capture variables in closure
    name = artifact_name
    template = artifact_path_template

    if "latest" in template:
        # Dynamic path: resolve latest timestamped directory at read time
        @sys_mcp.resource(f"project://{{project_name}}/work/{name}")
        def _make_latest_resource(project_name: str, _name=name, _template=template):
            try:
                _validate_slug(project_name)
            except ValueError as e:
                return f"❌ Error: {e}"
            latest_dir = _get_latest_report_dir(project_name)
            if not latest_dir:
                return f"❌ No validation reports found for project '{project_name}'."
            # Resolve the actual file path
            if "validation_report" in _template:
                target = latest_dir / "validation_report.md"
            elif "coverage_report" in _template:
                target = latest_dir / "coverage_report.md"
            elif "gap_report" in _template:
                target = latest_dir / "gap_report.md"
            else:
                target = latest_dir / "validation_report.md"
            if target.is_file():
                return target.read_text(encoding="utf-8")
            return f"❌ Report file not found: {target}"
    else:
        # Static path under project/.work/
        @sys_mcp.resource(f"project://{{project_name}}/work/{name}")
        def _make_static_resource(project_name: str, _name=name, _template=template):
            try:
                _validate_slug(project_name)
            except ValueError as e:
                return f"❌ Error: {e}"
            target = ROOT_DIR / "projects" / project_name / _template
            if target.is_file():
                return target.read_text(encoding="utf-8")
            return f"❌ Artifact not found: {target} (run the corresponding pipeline step first)"
