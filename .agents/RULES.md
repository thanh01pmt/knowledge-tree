# Shared Workflow Rules

> Cross-cutting rules referenced by every skill and workflow in Knowledge Tree.
> Read once per project and cite the section; do not paraphrase the rule itself.

## 1. Context Gate
Before any workflow that **writes** project artifacts (like `/map-taxonomy` or `/build-tree`), you must understand the project context.
- Read PDF/Syllabus files in `projects/<project>/context/`.
- Khởi đầu luôn dùng `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` làm chân lý. Bạn CÓ THỂ đề xuất thêm mã (code) mới vào Master Tree nếu không tìm thấy mã phù hợp, nhưng **tuyệt đối không được tự ý ghi** mà phải thông qua phê duyệt của Human.

## 2. Mock-Mode Prohibition
⛔ Never run scripts with `--mock` or bypass actual execution.

## 3. Final Artifacts and Working State
The final output for any project is exactly these 6 validated TSV files inside `projects/<project>/output/`:
- `fields.tsv`
- `subjects.tsv`
- `categories.tsv`
- `topics.tsv`
- `concepts.tsv`
- `learning-objectives.tsv`

Intermediate files like mapping plans must be saved in `projects/<project>/.work/`.

## 4. Approval Gate
Before writing the final TSV files (e.g. running `/build-tree`), you MUST show the proposed mapping plan (`projects/<project>/.work/mapping-plan.md`) to the user. Do NOT write the TSVs without explicit user approval.

## 5. Security Boundary
- Read master data from `.agents/skills/taxonomy-mapper/resources/`.
- Read project data from `projects/<project>/context/`.
- Write ONLY to `projects/<project>/output/*.tsv` and `projects/<project>/.work/`. (Sửa đổi thư mục `resources/` của skill chỉ khi được User cho phép rõ ràng).
- Active project is tracked in `status.yaml`.

## 6. Reverse Coverage Gate (Đối chiếu ngược độ phủ Syllabus)
Sau khi tạo xong `learning-objectives.tsv` và hoàn tất `/build-tree`, BẮT BUỘC phải thực hiện kiểm tra đối chiếu ngược (`/audit-coverage` hoặc chạy `audit_coverage.py`) giữa dữ liệu `learning-objectives.tsv` vừa sinh ra với tài liệu nguồn trong `projects/<project>/context/`.
- Đảm bảo 100% mục trong syllabus nguồn đều có ít nhất 1 mã LO đảm nhiệm.
- Phát hiện các khoảng trống (gaps) hoặc dư thừa để xuất báo cáo `coverage_report.md`.

## 7. Master Tree Integrity Gate
Master Tree Integrity Gate — before `/map-taxonomy` or `/build-tree` reads from the Master Tree, `/validate-master-tree` (or `validate_master_tree.py`) must have PASSed since the tree was last modified.
