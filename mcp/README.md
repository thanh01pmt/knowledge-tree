# 🌳 Knowledge Tree MCP Hub Documentation

Tài liệu này tổng hợp chi tiết về bộ công cụ **Knowledge Tree MCP Sub-Server (`kt`)** và hệ thống Multi-MCP Hub trong thư mục `mcp/`.

---

## 📌 Tổng Quan Sub-Server `kt` (Knowledge Tree Operations)

Sub-server **`kt`** đóng vai trò là lõi xử lý tự động hoá toàn bộ quy trình xây dựng, kiểm định và đồng bộ Knowledge Tree cho các dự án con.

- **Namespace Tool**: `kt_*`
- **Mục tiêu**: Cung cấp bộ công cụ chuẩn hoá cho bất kỳ AI Agent nào (Pi, Cursor, Claude Desktop, Antigravity,...) gọi trực tiếp.

---

## 🛠️ Danh Sách Công Cụ (Tools) Của `kt` Server

### 1. `kt_validate_tree`
* **Mô tả**: Kiểm tra tính toàn vẹn tham chiếu (referential integrity) giữa 6 tầng dữ liệu (`fields` $\rightarrow$ `subjects` $\rightarrow$ `categories` $\rightarrow$ `topics` $\rightarrow$ `concepts` $\rightarrow$ `learning-objectives`).
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
  - `project_name` (`str`, bắt buộc): Tên dự án mới cần khởi tạo.
* **Kết quả trả về**: Thông báo tạo cấu trúc thư mục thành công.

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
        "mcp/main.py"
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
- `skills://{skill_name}` (Resource): Đọc tài liệu hướng dẫn kỹ năng `SKILL.md`.
- `guide_workflow` (Prompt): Cung cấp hướng dẫn quy trình từng bước cho Agent.
