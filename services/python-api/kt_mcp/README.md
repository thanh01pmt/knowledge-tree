# 🌳 Knowledge Tree MCP Hub Documentation

Tài liệu này tổng hợp chi tiết về bộ công cụ **Knowledge Tree MCP Sub-Server (`kt`)** và hệ thống Multi-MCP Hub trong thư mục `kt_mcp/`.

---

## 📌 Tổng Quan Sub-Server `kt` (Knowledge Tree Operations)

Sub-server **`kt`** đóng vai trò là lõi xử lý tự động hoá toàn bộ quy trình xây dựng, kiểm định và đồng bộ Knowledge Tree cho các dự án con.

- **Namespace Tool**: `kt_*`
- **Mục tiêu**: Cung cấp bộ công cụ chuẩn hoá cho bất kỳ AI Agent nào (Pi, Cursor, Claude Desktop, Antigravity,...) gọi trực tiếp.

---

## 🛠️ Danh Sách Công Cụ (Tools) Của `kt` Server (29 Tools)

### Validation & Audit (5 tools)

### 1. `kt_validate_tree`
* **Mô tả**: Kiểm tra tính toàn vẹn tham chiếu (referential integrity) giữa 6 tầng dữ liệu (`fields` → `subjects` → `categories` → `topics` → `concepts` → `learning-objectives`).
* **Tham số (Arguments)**:
  - `project_name` (`str`, bắt buộc): Tên slug dự án (ví dụ: `"roadmap_sh_graphql"`, `"swift-associate"`).
  - `fix` (`bool`, tùy chọn, mặc định `False`): Nếu `True`, tự động chuẩn hoá các cell lỗi format an toàn (`DUPLICATE_REF_IN_CELL`, `SEPARATOR_FORMAT`) và sinh báo cáo đề xuất sửa lỗi (`proposed_fixes.md`).
* **Kết quả trả về**: Mã trạng thái (`PASSED`/`FAILED`), số lượng lỗi/cảnh báo và báo cáo Markdown chi tiết.

---

### 2. `kt_detect_gaps`
* **Mô tả**: Phân tích và phát hiện **3 dạng lỗ hổng tri thức** trong cây của dự án:
  1. *Missing LO Coverage*: Các `concept` chưa được phủ bởi bất kỳ `learning-objective` nào.
  2. *Shallow CIOs*: Các `CIO` cạn kiệt thông tin, thiếu độ sâu lý thuyết Anderson & Krathwohl.
  3. *Master Candidates*: Các `concept` hoặc `LO` mới tiềm năng cần đề xuất đưa vào Master Tree.
* **Tham số**:
  - `project_name` (`str`, bắt buộc): Tên slug dự án.
* **Kết quả trả về**: Báo cáo Markdown phân tích chi tiết lỗ hổng (`gap_analysis_report.md`).

---

### 3. `kt_audit_coverage`
* **Mô tả**: Thực hiện đối chiếu ngược (Reverse Coverage Audit) giữa các `learning-objectives` đã sinh ra với tài liệu nguồn (syllabus / PDF / raw roadmap) trong thư mục `projects/<project>/context/`.
* **Tham số**:
  - `project_name` (`str`, bắt buộc): Tên slug dự án.
* **Kết quả trả về**: Báo cáo Markdown chỉ số độ phủ (Coverage Score %) và danh sách các phần bài học bị bỏ sót.

---

### 4. `kt_sync_supabase`
* **Mô tả**: Đồng bộ dữ liệu từ 6 file TSV đầu ra (`output/*.tsv`) của dự án lên cơ sở dữ liệu Supabase Cloud theo thứ tự phụ thuộc nghiêm ngặt (upsert by code).
* **Tham số**:
  - `project_name` (`str`, bắt buộc): Tên slug dự án.
* **Kết quả trả về**: Nhật ký kết quả đồng bộ từng bảng (`fields`, `subjects`, `categories`, `topics`, `concepts`, `learning_objectives`).

---

### 5. `kt_scaffold_project`
* **Mô tả**: Khởi tạo cấu trúc thư mục dự án mới (`projects/<project_name>/`) với đầy đủ các thư mục con `context/`, `.work/`, `.tree-validator/`, `output/` và file header TSV chuẩn.
* **Tham số**:
  - `project_name` (`str`, bắt buộc): Tên dự án mới (slug dạng kebab-case/snake_case, chỉ gồm chữ thường, số, gạch ngang/gạch dưới).
* **Kết quả trả về**: Thông báo tạo cấu trúc thư mục thành công.

---

### 6. `kt_query_master_tree`
* **Mô tả**: Tìm kiếm/filter Master Knowledge Tree (mlo-knowlege-tree.tsv) — fuzzy search, level filter, parent filter.
* **Tham số**:
  - `query` (`str`, tùy chọn, mặc định `""`): Từ khóa tìm kiếm (tên, mã, keywords, description).
  - `level` (`str`, tùy chọn): `"fields"` \| `"subjects"` \| `"categories"` \| `"topics"` \| `"concepts"` \| `""` (tất cả).
  - `parent` (`str`, tùy chọn): Mã node cha để lọc top-down.
  - `limit` (`int`, tùy chọn, mặc định `20`, max `100`): Số kết quả tối đa.
  - `include_keywords` (`bool`, tùy chọn, mặc định `true`): Trả về cột keywords.
  - `include_description` (`bool`, tùy chọn, mặc định `true`): Trả về cột description.
* **Kết quả**: JSON `{ "results": [{level, code, name, keywords?, description?, score}, ...], "total": N }`

---

### 7. `kt_query_master_tree_semantic`
* **Mô tả**: Tìm kiếm ngữ nghĩa (semantic search) trên Master Knowledge Tree dùng **Ollama (nomic-embed-text, 768-dim)**. Hiểu ngữ cảnh, đồng nghĩa, đa ngôn ngữ (EN/VI). Thích hợp cho truy vấn tự nhiên như "thuật toán tìm kiếm nhị phân", "kiến trúc CPU", "cách sắp xếp mảng". Model chạy local trên VM qua Ollama container (không phụ thuộc HF Hub).
* **Tham số**:
  - `query` (`str`, bắt buộc): Câu truy vấn tự nhiên (tiếng Anh hoặc tiếng Việt).
  - `level` (`str`, tùy chọn): `"fields"` \| `"subjects"` \| `"categories"` \| `"topics"` \| `"concepts"` \| `"learning_objectives"` \| `""` (tất cả).
  - `limit` (`int`, tùy chọn, mặc định `10`, max `50`): Số kết quả tối đa.
  - `threshold` (`float`, tùy chọn, mặc định `0.35`): Ngưỡng cosine similarity (0.0-1.0). Thấp hơn = nhiều kết quả hơn.
* **Kết quả**: JSON `{ "results": [{level, code, name, keywords, description, similarity}, ...], "total": N }`

---

### Hierarchical LO Generation Pipeline (6 tools)

### 6. `kt_build_taxonomy`
* **Mô tả**: Build 5 taxonomy TSV files từ approved mapping plan.
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 7. `kt_generate_ulos`
* **Mô tả**: Phase A — Generate ULOs (Bloom Evaluate/Create, tech-agnostic) → `ulos_preview.md` (HITL checkpoint)
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 8. `kt_generate_cios`
* **Mô tả**: Phase B — Generate CIOs + Marr 2-Language Test → `cios_preview.md` (HITL checkpoint)
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 9. `kt_generate_sios`
* **Mô tả**: Phase C — Generate tech-specific SIOs
* **Tham số**: `project_name` (`str`, bắt buộc), `technology` (`str`, tùy chọn, ví dụ: `"Swift / SwiftUI"`)

---

### 10. `kt_merge_los`
* **Mô tả**: Merge ULO+CIO+SIO → `learning-objectives.tsv`
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 11. `kt_map_prerequisites`
* **Mô tả**: Phase E (ADR-0005) — 4-step prerequisite mapping → `lo_prerequisites.tsv` + updated `concepts.tsv`
* **Tham số**: `project_name` (`str`, bắt buộc), `dry_run` (`bool`), `no_verify` (`bool`), `reuse_concept_dag` (`bool`)

---

### Context & Taxonomy (2 tools)

### 12. `kt_context_audit`
* **Mô tả**: Phân tích syllabus + ATE keywords → `.work/context-audit.md`
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 13. `kt_map_taxonomy`
* **Mô tả**: Cross-reference syllabus with Master Tree → `.work/mapping-plan.md` (HITL checkpoint)
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### ATE Pipeline (5 tools)

### 14. `kt_scaffold_keywords`
* **Mô tả**: Tạo workspace ATE keyword extraction
* **Tham số**: `topic` (`str`, bắt buộc), `source_path` (`str`, bắt buộc), `project_name` (`str`, tùy chọn)

---

### 15. `kt_extract_terms`
* **Mô tả**: YAKE + LLM candidate generation → embedding filter → candidates
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 16. `kt_verify_terms`
* **Mô tả**: LLM dedup + omission check loop → `verify-report.md` (HITL checkpoint)
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 17. `kt_finalize_keywords`
* **Mô tả**: Export `keywords.tsv` + inject into context audit
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 18. `kt_escalate_concepts`
* **Mô tả**: Keywords → neutral concepts + Master Tree match → concept candidates (Gap D)
* **Tham số**: `project_name` (`str`, bắt buộc), `match_threshold` (`float`, tùy chọn)

---

### Roadmap Aligner (5 tools)

### 19. `kt_crawl_roadmap`
* **Mô tả**: Scaffold project + crawl roadmap.sh graph JSON
* **Tham số**: `url` (`str`, bắt buộc), `project_name` (`str`, tùy chọn)

---

### 20. `kt_init_staging_tree`
* **Mô tả**: Initialize staging tree from roadmap DAG
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 21. `kt_apply_staging_plan`
* **Mô tả**: Apply approved staging changes to local project
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 22. `kt_diff_staging`
* **Mô tả**: Diff staging tree against Master Tree
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### 23. `kt_sync_master_back`
* **Mô tả**: Push approved changes to Master Tree (Gate §8 protected — HITL required)
* **Tham số**: `project_name` (`str`, bắt buộc)

---

### Workflow Orchestration (2 tools)

### 24. `kt_run_pipeline_step`
* **Mô tả**: Execute a single pipeline step with status tracking
* **Tham số**: `project_name` (`str`), `step_name` (`str`), `params` (`object`)

---

### 25. `kt_get_pipeline_status`
* **Mô tả**: Get current pipeline execution status
* **Tham số**: `project_name` (`str`)

---

### System Introspection (2 tools - `sys` server)

### 26. `sys_get_system_status`
* **Mô tả**: Read `status.yaml` for overall repo state
* **Tham số**: none

---

### 27. `sys_get_skill_metadata`
* **Mô tả**: Read SKILL.md for a specific skill
* **Tham số**: `skill_name` (`str`, bắt buộc)

---

### Autonomous Research (2 tools - `research` server)

### 28. `research_audit_curriculum`
* **Mô tả**: Kích hoạt **Tier 1 (Curriculum Audit)**. Cross-reference Master Tree với các framework chuẩn (NGSS, ACM) để tìm ra các lỗ hổng nền tảng (Foundational Gaps).
* **Tham số**: `framework` (`str`, tùy chọn, mặc định `"ACM CS2023"`)
* **Kết quả**: Trả về báo cáo Foundational Gaps Report.

---

### 29. `research_watch_trends`
* **Mô tả**: Kích hoạt **Tier 2 (Trend Watcher)**. Quét các nguồn dữ liệu mạng ngầm và deep tech để tìm kiếm các xu hướng học máy / công nghệ mới (emerging tech).
* **Tham số**: `query` (`str`, tùy chọn, mặc định `"emerging technologies in STEM education"`)
* **Kết quả**: Trả về danh sách Hàng đợi nghiên cứu (`research_queue.json`).

---

## 📋 HITL Resources (9 Resource Templates — `sys` server)

| Resource URI Template | Artifact Description |
|---|---|
| `project://sys/{project}/work/context-audit` | Context audit markdown (Checkpoint 3) |
| `project://sys/{project}/work/mapping-plan` | Taxonomy mapping plan (Checkpoint 4) |
| `project://sys/{project}/work/hlo/ulos_preview` | ULOs preview table (Checkpoint 5) |
| `project://sys/{project}/work/hlo/cios_preview` | CIOs preview + Marr Test (Checkpoint 6) |
| `project://sys/{project}/work/hlo/sios_preview` | SIOs preview |
| `project://sys/{project}/work/concept_escalation` | Concept escalation report (Gap D) |
| `project://sys/{project}/work/verify-report` | ATE keyword verification report (Checkpoint 1) |
| `project://sys/{project}/work/gap_report` | Gap detection report |
| `project://sys/{project}/work/coverage_audit` | Coverage audit report |

---

## 💬 Prompt (1 prompt — `sys` server)

### `guide_workflow`
* **Mô tả**: Cung cấp hướng dẫn quy trình từng bước cho Agent (slash command workflow guidance).
* **Tham số**: `step` (`str`, tùy chọn) — tên bước cụ thể để xem hướng dẫn chi tiết.

---

## 💻 Mẫu Cấu Hình Cho AI Client (`.mcp.json`)

```json
{
  "mcpServers": {
    "knowledge-tree": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp>=3.0.0",
        "--with", "supabase>=2.0.0",
        "--with", "pandas>=2.0.0",
        "kt_mcp/main.py"
      ],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

---

## 🌐 Các Server Khác Cùng Chạy Trong Hub

Ngoài `kt`, Hub còn chứa sub-server **`sys` (SystemOps)**:
- `sys_get_system_status`: Đọc file `status.yaml` để biết trạng thái tổng thể toàn repo.
- `sys_get_skill_metadata`: Đọc tài liệu hướng dẫn `SKILL.md` của một skill (thay thế resource `skills://` cũ).
- `sys_get_project_status`: Đọc thông tin trạng thái dự án từ `status.yaml` (thay thế resource `project://status` cũ).
- `guide_workflow` (Prompt): Cung cấp hướng dẫn quy trình từng bước cho Agent.
- **9 HITL Resource Templates**: `project://sys/{project}/work/{artifact}`

> **Lưu ý bảo mật**: Tất cả tool nhận `project_name` đều validate slug (chỉ chấp nhận chữ thường, số, gạch ngang, gạch dưới) để ngăn path traversal. Các subprocess gọi script có timeout (120s-1800s tùy tool) để tránh hung process.