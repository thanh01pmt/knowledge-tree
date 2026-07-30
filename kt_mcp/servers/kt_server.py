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


@kt_mcp.tool
def validate_master_tree() -> str:
    """
    Kiểm tra tính toàn vẹn tham chiếu và phát hiện collision trong Master Knowledge Tree (mlo-knowlege-tree.tsv).
    
    BẮT BUỘC phải PASS trước khi /map-taxonomy hoặc /build-tree đọc từ Master Tree (Gate §7).
    """
    script_path = SKILLS_DIR / "tree-validator" / "scripts" / "validate_master_tree.py"
    if not script_path.exists():
        return f"Error: Cannot find validate_master_tree.py at {script_path}"

    cmd = [sys.executable, str(script_path)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output
    except subprocess.TimeoutExpired:
        return f"❌ Error: validate_master_tree.py timed out after 120s."


@kt_mcp.tool
def query_master_tree(
    query: str = "",
    level: str = "",
    parent: str = "",
    limit: int = 20,
    include_keywords: bool = True,
    include_description: bool = True
) -> str:
    """
    Tìm kiếm/filter Master Knowledge Tree (mlo-knowlege-tree.tsv) qua MCP.
    
    Args:
        query: Từ khóa tìm kiếm mờ (tên, mã, keywords, description). Rỗng = trả về tất cả (theo limit).
        level: Giới hạn cấp độ. Rỗng = search tất cả 5 cấp. Chọn: "fields", "subjects", "categories", "topics", "concepts".
        parent: Lọc theo mã node cha (ví dụ: "PROGRAMMING_FUNDAMENTALS").
        limit: Số kết quả tối đa (mặc định 20, max 100).
        include_keywords: Trả về cột keywords.
        include_description: Trả về cột description.
    
    Returns:
        JSON string: { "results": [ {level, code, name, keywords?, description?, score}, ... ], "total": N }
    """
    import json
    import re
    import unicodedata
    from pathlib import Path
    
    # Validate limit
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 1
    
    # Validate level
    valid_levels = {"fields", "subjects", "categories", "topics", "concepts", ""}
    if level and level not in valid_levels:
        return json.dumps({"error": f"Invalid level: {level}. Valid: {list(valid_levels)}"}, ensure_ascii=False)
    
    # Load master_tree.json
    tree_path = SKILLS_DIR / "taxonomy-mapper" / "resources" / "master_tree.json"
    if not tree_path.exists():
        return json.dumps({"error": "master_tree.json not found. Run parse_master_tree.py first."}, ensure_ascii=False)
    
    try:
        with open(tree_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return json.dumps({"error": f"Failed to load master_tree.json: {e}"}, ensure_ascii=False)
    
    # Scoring logic (reused from query_master_tree.py)
    def strip_diacritics(text: str) -> str:
        if not text:
            return ""
        nfkd = unicodedata.normalize("NFKD", text)
        return "".join(c for c in nfkd if not unicodedata.combining(c))
    
    def normalize_text(text):
        return strip_diacritics(text).lower().strip()
    
    def word_boundary_match(needle: str, haystack: str) -> bool:
        if not needle or not haystack:
            return False
        pattern = r"\b" + re.escape(needle) + r"\b"
        return re.search(pattern, haystack) is not None
    
    def calculate_score(q, code, name, keywords, description=""):
        q = normalize_text(q)
        c = normalize_text(code)
        n = normalize_text(name)
        k = normalize_text(keywords)
        d = normalize_text(description)
        if not q:
            return 1
        if q == c:
            return 100
        if q == n:
            return 90
        # keyword exact match (word-boundary on comma-separated list)
        if any(word_boundary_match(q, kw.strip()) for kw in k.split(",")):
            return 80
        if word_boundary_match(q, n):
            return 50
        if word_boundary_match(q, k):
            return 30
        if word_boundary_match(q, d):
            return 20
        # multi-word query: count matched words
        q_words = q.split()
        if len(q_words) > 1:
            matched_words = 0
            for w in q_words:
                if (word_boundary_match(w, n)
                        or word_boundary_match(w, k)
                        or word_boundary_match(w, d)):
                    matched_words += 1
            if matched_words > 0:
                return matched_words * 10
        return 0
    
    def get_parent_field(lvl):
        return {
            'subjects': 'field_codes',
            'categories': 'subject_codes',
            'topics': 'category_codes',
            'concepts': 'topic_codes'
        }.get(lvl)
    
    levels_to_search = [level] if level else ["fields", "subjects", "categories", "topics", "concepts"]
    results = []
    
    for lvl in levels_to_search:
        rows = data.get(lvl, [])
        parent_field = get_parent_field(lvl)
        for row in rows:
            # Filter by parent
            if parent and parent_field:
                parents_str = row.get(parent_field, "")
                if parent not in [p.strip() for p in parents_str.replace(";", ",").replace("|", ",").split(",")]:
                    continue
            elif parent and not parent_field:  # Fields don't have parents
                continue
            
            code = row.get("code", "")
            name = row.get("name", "")
            keywords = row.get("keywords", "")
            description = row.get("description", "")
            
            score = calculate_score(query, code, name, keywords, description)
            if score > 0 or not query:
                res = {"level": lvl, "code": code, "name": name, "score": score}
                if include_keywords:
                    res["keywords"] = keywords
                if include_description:
                    res["description"] = description
                results.append(res)
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:limit]
    
    return json.dumps({"results": results, "total": len(results)}, ensure_ascii=False)


@kt_mcp.tool
def build_taxonomy(project_name: str, source: str = "mapping-plan") -> str:
    """
    Xây dựng 5 file TSV phân loại (fields, subjects, categories, topics, concepts) từ mapping-plan.md đã duyệt.
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        source: Nguồn dữ liệu - 'mapping-plan' (khuyến nghị) hoặc 'lo-tsv' (tương thích ngược)
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    if source not in ("mapping-plan", "lo-tsv"):
        return f"❌ Error: source must be 'mapping-plan' or 'lo-tsv', got '{source}'"

    script_path = SKILLS_DIR / "tree-assembler" / "scripts" / "assemble_project.py"
    if not script_path.exists():
        return f"Error: Cannot find assemble_project.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--source", source]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output
    except subprocess.TimeoutExpired:
        return f"❌ Error: assemble_project.py timed out after 120s for project '{project_name}'."


# ─── ATE Pipeline Tools (Keyword Extraction) ──────────────────────────────────

@kt_mcp.tool
def scaffold_keywords(project_name: str, target_context: str, source: str) -> str:
    """
    Khởi tạo workspace ATE: cắt tài liệu nguồn (PDF/MD/TXT) thành chunks, ghi config.json.
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        target_context: Mô tả chủ đề mục tiêu (VD: "Lập trình Swift iOS cơ bản")
        source: Đường dẫn đến file/thư mục nguồn (VD: "projects/swift-associate/context/")
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "keyword-extractor" / "scripts" / "chunk_source.py"
    if not script_path.exists():
        return f"Error: Cannot find chunk_source.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--target-context", target_context, "--source", source]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output
    except subprocess.TimeoutExpired:
        return f"❌ Error: chunk_source.py timed out after 120s for project '{project_name}'."


@kt_mcp.tool
def extract_terms(project_name: str) -> str:
    """
    Chạy pipeline trích xuất candidate terms: YAKE statistical + LLM candidate-gen → embedding filter.
    
    Output: .work/kw/candidates_filtered.json + .work/kw/candidates_filtered.md
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    scripts = [
        ("gen_statistical_candidates.py", "YAKE statistical extraction"),
        ("llm_gen_candidates.py", "LLM candidate generation"),
        ("filter_by_relevance.py", "Embedding cosine filter"),
    ]

    results = []
    for script_name, desc in scripts:
        script_path = SKILLS_DIR / "keyword-extractor" / "scripts" / script_name
        if not script_path.exists():
            return f"Error: Cannot find {script_name} at {script_path}"

        cmd = [sys.executable, str(script_path), "--project", project_name]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=300)
            output = res.stdout or res.stderr
            if res.returncode != 0:
                stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
                stderr_summary = "\n".join(stderr_tail)
                return (f"❌ {desc} FAILED (exit code {res.returncode}).\n"
                        f"--- stdout ---\n{output}\n"
                        f"--- stderr (last lines) ---\n{stderr_summary}\n"
                        f"⚠️ Pipeline stopped at {script_name}.")
            results.append(f"✅ {desc}: {output.strip()[:200]}")
        except subprocess.TimeoutExpired:
            return f"❌ Error: {script_name} timed out after 300s for project '{project_name}'."

    return "\n".join(results) + "\n\n→ Xem .work/kw/candidates_filtered.md, rồi chạy /verify-terms"


@kt_mcp.tool
def verify_terms(project_name: str, max_rounds: int = 2, dedup_batch: int = 30) -> str:
    """
    LLM dedup biến thể + vòng lặp omission-check (tối đa 2 vòng).
    
    Output: .work/kw/keywords_verified.json + .work/kw/verify-report.md (điểm duyệt người)
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        max_rounds: Số vòng omission-check tối đa (default: 2)
        dedup_batch: Kích thước batch dedup (default: 30)
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "keyword-extractor" / "scripts" / "llm_verify_and_dedup.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_verify_and_dedup.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--max-rounds", str(max_rounds), "--dedup-batch", str(dedup_batch)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=600)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Đọc .work/kw/verify-report.md để duyệt, rồi chạy /finalize-keywords"
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_verify_and_dedup.py timed out after 600s for project '{project_name}'."


@kt_mcp.tool
def finalize_keywords(project_name: str, no_inject: bool = False) -> str:
    """
    Export keywords cuối cùng (keywords.tsv, keywords.json) và inject vào context-audit.md.
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        no_inject: Nếu True, không inject vào context-audit.md
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "keyword-extractor" / "scripts" / "export_keywords.py"
    if not script_path.exists():
        return f"Error: Cannot find export_keywords.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name]
    if no_inject:
        cmd.append("--no-inject")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Chạy /escalate-concepts (khuyến nghị) hoặc /context-audit"
    except subprocess.TimeoutExpired:
        return f"❌ Error: export_keywords.py timed out after 120s for project '{project_name}'."


@kt_mcp.tool
def escalate_concepts(project_name: str, match_threshold: float = 0.80, llm_model: str = "gpt-4o") -> str:
    """
    Abstraction keywords → concept trung tính + match Master Tree (Gap D detection).
    
    Output: output/concept_candidates.tsv + .work/kw/concept_escalation.md (điểm duyệt người)
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        match_threshold: Ngưỡng cosine để match Master Tree (default: 0.80 — conservative)
        llm_model: Model LLM cho abstraction (default: gpt-4o)
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "keyword-extractor" / "scripts" / "llm_escalate_concepts.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_escalate_concepts.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--match-threshold", str(match_threshold), "--llm-model", llm_model]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=600)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Đọc .work/kw/concept_escalation.md để duyệt Gap D concepts, rồi chạy /map-taxonomy"
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_escalate_concepts.py timed out after 600s for project '{project_name}'."


# ─── Hierarchical LO Generation Tools (ULO → CIO → SIO) ─────────────────────────

@kt_mcp.tool
def generate_ulos(project_name: str, model: str = "gpt-4o", batch_size: int = 10, no_master_append: bool = False) -> str:
    """
    Phase A: Sinh/Filter ULOs từ Master Bank (ưu tiên Bloom Evaluate/Create).
    
    Output: .work/hlo/ulos.json + .work/hlo/ulos_preview.md (điểm duyệt người)
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        model: OpenAI model (default: gpt-4o)
        batch_size: Số concepts mỗi LLM call (default: 10)
        no_master_append: Nếu True, không ghi ULO mới vào master bank
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "learning-objective-generator" / "scripts" / "llm_generate_hierarchical_lo.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_generate_hierarchical_lo.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--phase", "ulos", "--model", model, "--batch-size", str(batch_size)]
    if no_master_append:
        cmd.append("--no-master-append")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=600)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Đọc .work/hlo/ulos_preview.md để duyệt ULOs, rồi chạy /generate-cios"
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_generate_hierarchical_lo.py (ulos phase) timed out after 600s for project '{project_name}'."


@kt_mcp.tool
def generate_cios(project_name: str, model: str = "gpt-4o", batch_size: int = 10) -> str:
    """
    Phase B: Sinh CIOs từ ULOs đã duyệt, enforce Marr 2-Language Test per CIO.
    
    Output: .work/hlo/cios.json + .work/hlo/cios_preview.md (điểm duyệt người - kiểm tra Marr Test)
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        model: OpenAI model (default: gpt-4o)
        batch_size: Số ULOs mỗi LLM call (default: 10)
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "learning-objective-generator" / "scripts" / "llm_generate_hierarchical_lo.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_generate_hierarchical_lo.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--phase", "cios", "--model", model, "--batch-size", str(batch_size)]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=600)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Đọc .work/hlo/cios_preview.md (kiểm tra marr_test_note), duyệt, rồi chạy /generate-sios"
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_generate_hierarchical_lo.py (cios phase) timed out after 600s for project '{project_name}'."


@kt_mcp.tool
def generate_sios(project_name: str, technology: str = "", model: str = "gpt-4o", batch_size: int = 8) -> str:
    """
    Phase C: Sinh SIOs (tech-specific) từ CIOs đã duyệt.
    
    Output: .work/hlo/sios.json (sau khi merge sẽ thành learning-objectives.tsv)
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        technology: Override technology detection (VD: "Swift", "Python", "JavaScript")
        model: OpenAI model (default: gpt-4o)
        batch_size: Số CIOs mỗi LLM call (default: 8)
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "learning-objective-generator" / "scripts" / "llm_generate_hierarchical_lo.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_generate_hierarchical_lo.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--phase", "sios", "--model", model, "--batch-size", str(batch_size)]
    if technology:
        cmd.extend(["--technology", technology])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=600)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Chạy /merge-los để ghi learning-objectives.tsv"
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_generate_hierarchical_lo.py (sios phase) timed out after 600s for project '{project_name}'."


@kt_mcp.tool
def merge_los(project_name: str) -> str:
    """
    Phase D: Merge ULO + CIO + SIO → learning-objectives.tsv.
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "learning-objective-generator" / "scripts" / "llm_generate_hierarchical_lo.py"
    if not script_path.exists():
        return f"Error: Cannot find llm_generate_hierarchical_lo.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--phase", "merge"]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Chạy /validate-tree và /audit-coverage"
    except subprocess.TimeoutExpired:
        return f"❌ Error: llm_generate_hierarchical_lo.py (merge phase) timed out after 120s for project '{project_name}'."


# ─── Roadmap Aligner Tools (External Knowledge Ingestion) ──────────────────────

@kt_mcp.tool
def crawl_roadmap(project_name: str, roadmap_url: str) -> str:
    """
    Crawl roadmap.sh URL via Crawl4AI, verify via SearXNG + Context7, produce alignment report.
    
    Output: .work/roadmap_alignment_report.md
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
        roadmap_url: URL roadmap.sh (VD: "https://roadmap.sh/backend")
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "roadmap-aligner" / "scripts" / "crawl_roadmap_align.py"
    if not script_path.exists():
        return f"Error: Cannot find crawl_roadmap_align.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name, "--url", roadmap_url]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=600)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Đọc .work/roadmap_alignment_report.md, duyệt, rồi chạy /init-staging-tree"
    except subprocess.TimeoutExpired:
        return f"❌ Error: crawl_roadmap_align.py timed out after 600s for project '{project_name}'."


@kt_mcp.tool
def init_staging_tree() -> str:
    """
    Khởi tạo staging working copy của Master Tree tại general-context/mlo-knowlege-tree.tsv.
    
    Copy từ .agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv
    """
    script_path = SKILLS_DIR / "roadmap-aligner" / "scripts" / "init_staging_tree.py"
    if not script_path.exists():
        return f"Error: Cannot find init_staging_tree.py at {script_path}"

    cmd = [sys.executable, str(script_path)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=60)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Staging tree ready. Chạy /apply-staging-plan sau khi có alignment plan"
    except subprocess.TimeoutExpired:
        return f"❌ Error: init_staging_tree.py timed out after 60s."


@kt_mcp.tool
def apply_staging_plan(project_name: str) -> str:
    """
    Áp dụng alignment plan đã duyệt vào staging tree (general-context/mlo-knowlege-tree.tsv).
    
    Args:
        project_name: Tên dự án (ví dụ: 'swift-associate')
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    script_path = SKILLS_DIR / "roadmap-aligner" / "scripts" / "apply_plan_to_staging.py"
    if not script_path.exists():
        return f"Error: Cannot find apply_plan_to_staging.py at {script_path}"

    cmd = [sys.executable, str(script_path), "--project", project_name]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Chạy /diff-staging để xem diff, rồi /sync-master-back (cần phê duyệt)"
    except subprocess.TimeoutExpired:
        return f"❌ Error: apply_plan_to_staging.py timed out after 120s for project '{project_name}'."


@kt_mcp.tool
def diff_staging() -> str:
    """
    So sánh staging tree (general-context/) với official master (.agents/skills/taxonomy-mapper/resources/).
    
    Output: .work/tree_diff_report.md showing added/modified/removed nodes across 5 tables.
    """
    script_path = SKILLS_DIR / "roadmap-aligner" / "scripts" / "tree_diff.py"
    if not script_path.exists():
        return f"Error: Cannot find tree_diff.py at {script_path}"

    cmd = [sys.executable, str(script_path)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=60)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Đọc .work/tree_diff_report.md, duyệt, rồi chạy /sync-master-back"
    except subprocess.TimeoutExpired:
        return f"❌ Error: tree_diff.py timed out after 60s."


@kt_mcp.tool
def sync_master_back() -> str:
    """
    Gate §8 Protected: Sync approved staging tree back to official master resource.
    
    - Copies general-context/mlo-knowlege-tree.tsv → .agents/skills/taxonomy-mapper/resources/
    - Regenerates master_tree.json
    - Bumps version tag (e.g., v2.2.0 → v2.3.0)
    - CẤM TUYỆT ĐỐI tự động chạy — phải có phê duyệt trực tiếp từ người dùng.
    """
    script_path = SKILLS_DIR / "roadmap-aligner" / "scripts" / "sync_back_master.py"
    if not script_path.exists():
        return f"Error: Cannot find sync_back_master.py at {script_path}"

    cmd = [sys.executable, str(script_path)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=120)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            stderr_tail = res.stderr.strip().split("\n")[-3:] if res.stderr else []
            stderr_summary = "\n".join(stderr_tail)
            return (f"❌ Script exited with code {res.returncode} (FAILED).\n"
                    f"--- stdout ---\n{output}\n"
                    f"--- stderr (last lines) ---\n{stderr_summary}\n"
                    f"⚠️ Output may be INCOMPLETE or CORRUPTED.")
        return output + "\n\n→ Master Tree updated. Chạy /validate-master-tree để confirm."
    except subprocess.TimeoutExpired:
        return f"❌ Error: sync_back_master.py timed out after 120s."


# ─── Workflow Orchestration Tools ──────────────────────────────────────────────

@kt_mcp.tool
def run_pipeline_step(project_name: str, step: str) -> str:
    """
    Thực thi một bước trong pipeline 13 bước với kiểm tra pre/post condition.
    
    Các bước hợp lệ:
    - init: Khởi tạo project (kt_scaffold_project)
    - context-audit: Phân tích ngữ cảnh (agent-driven, cần PDF trong context/)
    - map-taxonomy: Map taxonomy (agent-driven, đọc context-audit.md + concept_candidates.tsv)
    - build-tree: Xây dựng taxonomy TSV (kt_build_taxonomy)
    - generate-ulos: Sinh ULOs (kt_generate_ulos)
    - generate-cios: Sinh CIOs + Marr Test (kt_generate_cios)
    - generate-sios: Sinh SIOs (kt_generate_sios)
    - merge-los: Merge thành learning-objectives.tsv (kt_merge_los)
    - map-prerequisites: Sinh lo_prerequisites.tsv (kt_map_prerequisites)
    - validate-tree: Kiểm tra toàn vẹn (kt_validate_tree)
    - audit-coverage: Kiểm tra độ phủ syllabus (kt_audit_coverage)
    - detect-gaps: Phát hiện 4 loại gap (kt_detect_gaps)
    - sync-supabase: Đồng bộ lên Supabase (kt_sync_supabase) — Gate §8 protected
    
    Args:
        project_name: Tên dự án
        step: Tên bước pipeline
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    step_map = {
        "init": lambda: scaffold_project(project_name),
        "context-audit": lambda: f"[AGENT-DRIVEN] Hãy đọc projects/{project_name}/context/ và ghi .work/context-audit.md. Xem hướng dẫn: sys_guide_workflow(step_name='context-audit', project_name='{project_name}')",
        "map-taxonomy": lambda: f"[AGENT-DRIVEN] Hãy đọc .work/context-audit.md và output/concept_candidates.tsv, ghi .work/mapping-plan.md. Xem hướng dẫn: sys_guide_workflow(step_name='map-taxonomy', project_name='{project_name}')",
        "build-tree": lambda: build_taxonomy(project_name, "mapping-plan"),
        "generate-ulos": lambda: generate_ulos(project_name),
        "generate-cios": lambda: generate_cios(project_name),
        "generate-sios": lambda: generate_sios(project_name),
        "merge-los": lambda: merge_los(project_name),
        "map-prerequisites": lambda: map_prerequisites(project_name),
        "validate-tree": lambda: validate_tree(project_name, fix=True),
        "audit-coverage": lambda: audit_coverage(project_name),
        "detect-gaps": lambda: detect_gaps(project_name),
        "sync-supabase": lambda: sync_supabase(project_name),
    }

    if step not in step_map:
        return f"❌ Unknown step '{step}'. Valid steps: {list(step_map.keys())}"

    # Pre-condition checks
    pre_checks = {
        "build-tree": f"⚠️ Kiểm tra: .work/mapping-plan.md phải tồn tại và đã được duyệt.",
        "generate-ulos": f"⚠️ Kiểm tra: concepts.tsv phải tồn tại (chạy /build-tree trước).",
        "generate-cios": f"⚠️ Kiểm tra: .work/hlo/ulos.json phải tồn tại (chạy /generate-ulos trước).",
        "generate-sios": f"⚠️ Kiểm tra: .work/hlo/cios.json phải tồn tại (chạy /generate-cios trước).",
        "merge-los": f"⚠️ Kiểm tra: ulos.json, cios.json, sios.json phải tồn tại.",
        "map-prerequisites": f"⚠️ Kiểm tra: learning-objectives.tsv phải tồn tại (chạy /merge-los trước).",
        "validate-tree": f"⚠️ Kiểm tra: 6 TSV files phải tồn tại trong output/.",
        "sync-supabase": f"⚠️ GATE §8: CẤM TUYỆT ĐỐI tự động chạy. Phải có phê duyệt trực tiếp từ người dùng!",
    }

    if step in pre_checks:
        return f"{pre_checks[step]}\n\n---\n\n" + step_map[step]()

    return step_map[step]()


@kt_mcp.tool
def get_pipeline_status(project_name: str) -> str:
    """
    Trả về trạng thái pipeline: bước nào đã complete, bước nào đang pending HITL gate.
    
    Args:
        project_name: Tên dự án
    """
    try:
        _validate_project_name(project_name)
    except ValueError as e:
        return f"❌ Error: {e}"

    project_dir = ROOT_DIR / "projects" / project_name
    work_dir = project_dir / ".work"
    out_dir = project_dir / "output"
    hlo_dir = work_dir / "hlo"
    kw_dir = work_dir / "kw"
    tv_reports = project_dir / ".tree-validator" / "reports"

    status = {
        "init": (out_dir / "fields.tsv").exists(),
        "context-audit": (work_dir / "context-audit.md").exists(),
        "concept-candidates": (out_dir / "concept_candidates.tsv").exists(),
        "map-taxonomy": (work_dir / "mapping-plan.md").exists(),
        "build-tree": (out_dir / "concepts.tsv").exists(),
        "generate-ulos": (hlo_dir / "ulos.json").exists(),
        "generate-cios": (hlo_dir / "cios.json").exists(),
        "generate-sios": (hlo_dir / "sios.json").exists(),
        "merge-los": (out_dir / "learning-objectives.tsv").exists(),
        "map-prerequisites": (out_dir / "lo_prerequisites.tsv").exists(),
        "validate-tree": any(tv_reports.glob("*/validation_report.md")) if tv_reports.exists() else False,
        "audit-coverage": any(tv_reports.glob("*/coverage_report.md")) if tv_reports.exists() else False,
        "detect-gaps": any(tv_reports.glob("*/gap_report.md")) if tv_reports.exists() else False,
    }

    lines = [f"# Pipeline Status: {project_name}", ""]
    for step, done in status.items():
        mark = "✅" if done else "⏳"
        lines.append(f"{mark} {step}")
    
    # HITL Gates status
    lines += ["", "## HITL Gates", ""]
    gates = [
        ("Checkpoint 1: Verify Terms", kw_dir / "verify-report.md"),
        ("Checkpoint 2: Approve Concepts (Gap D)", out_dir / "concept_candidates.tsv"),
        ("Checkpoint 3: Confirm Context Audit", work_dir / "context-audit.md"),
        ("Checkpoint 4: Approve Mapping Plan", work_dir / "mapping-plan.md"),
        ("Checkpoint 5: Approve ULOs", hlo_dir / "ulos_preview.md"),
        ("Checkpoint 6: Approve CIOs (Marr Test)", hlo_dir / "cios_preview.md"),
        ("Checkpoint 7: Approve Supabase Sync", project_dir / "output" / "learning-objectives.tsv"),
    ]
    for gate_name, artifact in gates:
        mark = "✅" if artifact.exists() else "🛑"
        lines.append(f"{mark} {gate_name} — artifact: {artifact}")

    return "\n".join(lines)
