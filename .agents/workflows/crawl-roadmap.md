---
description: Run this workflow to crawl external roadmaps (e.g. roadmap.sh), scaffold a dedicated project, execute standard build pipeline, and merge new nodes into General Context.
---

# Workflow: Crawl Roadmap & Project Alignment Pipeline

> **Rule:** Khi crawl dữ liệu từ bất kỳ nguồn bên ngoài nào (như `roadmap.sh`), hệ thống sẽ **khởi tạo 1 project độc lập** trong `projects/<project_name>`, triển khai đầy đủ quy trình xây dựng & kiểm định 6 bảng TSV cho project đó trước, sau đó mới đề xuất merge node mới vào `general-context/mlo-knowlege-tree.tsv`.

**Command:** `/crawl-roadmap <URL> [project_name]`  
**Owner:** `@roadmap-aligner` & `@tree-assembler`

---

## 🔄 3-Phase Workflow Contract

### Giai đoạn 1: Khởi tạo Project & Cào dữ liệu Nguồn (Project Setup & Crawl)

1. **Xác định Tên Project**: Tự động chuyển đổi URL thành tên project (ví dụ: `https://roadmap.sh/frontend` $\rightarrow$ `roadmap_sh_frontend`), hoặc sử dụng `project_name` do người dùng chỉ định.
2. **Scaffold Project**:
   ```bash
   python3 .agents/skills/tree-validator/scripts/scaffold_tree.py <project_name>
   ```
   *Cập nhật `active_project` trong `status.yaml` và tạo cấu trúc `projects/<project_name>/context/` và `output/`.*
3. **Cào & Lưu Context**:
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/crawl_roadmap_align.py <URL> --project <project_name>
   ```
   *Lưu dữ liệu cào thô và file `syllabus.md` vào `projects/<project_name>/context/`.*

---

### Giai đoạn 2: Quy trình Chuẩn của Project (Standard Project Pipeline)

4. **Context Audit (`/context-audit`)**: Trích xuất chủ đề và kiến thức miền từ `projects/<project_name>/context/`.
5. **Taxonomy Mapping (`/map-taxonomy`)**: Đối chiếu context với Master Tree và lập kế hoạch `projects/<project_name>/.work/mapping-plan.md`.
6. **Build Tree (`/build-tree`)**: Dựng 5 file taxonomy TSVs trong `projects/<project_name>/output/` (`fields.tsv`, `subjects.tsv`, `categories.tsv`, `topics.tsv`, `concepts.tsv`).
7. **Generate Learning Objectives (`/generate-los`)**: Sinh file `learning-objectives.tsv` (chuẩn ULO, CIO, SIO) grounded theo concept codes của project.
8. **Validate & Audit (`/validate-tree`)**: Run `validate_tree.py` & `audit_coverage.py` đảm bảo referential integrity 100% PASS và phủ 100% syllabus.
9. *(Tùy chọn)* **Sync Supabase (`/sync-supabase`)**: Đồng bộ 6 file TSV của project lên cơ sở dữ liệu Supabase.

---

### Giai đoạn 3: Đề xuất & Merge vào General Context (Master Merge Proposal)

10. **So sánh Diff với General Context**:
    ```bash
    python3 .agents/skills/roadmap-aligner/scripts/tree_diff.py --project <project_name>
    ```
    *So sánh 6 bảng TSV của project với `general-context/mlo-knowlege-tree.tsv`.*
11. **Lập Đề xuất Merge (N:N Reuse Topology)**:
    - Báo cáo chi tiết các Fields, Subjects, Categories, Topics, Concepts, và LOs mới được phát hiện từ project.
    - Áp dụng nguyên tắc N:N Reuse: Ưu tiên gắn ghép vào Category/Topic hiện có thay vì tạo Category/Topic trùng lặp.
12. **Phê duyệt & Sync Back**:
    - Trình báo cáo cho người dùng phê duyệt.
    - Sau khi phê duyệt, thực hiện merge vào `general-context/mlo-knowlege-tree.tsv` và nâng phiên bản trong `general-context/version_history.json`.

