# /detect-gaps Workflow

## Mục đích

Phát hiện 3 loại gap trong Knowledge Tree của project hiện tại:

| Gap | Ký hiệu | Ý nghĩa |
|---|---|---|
| **A** | `CONCEPT_WITHOUT_LO` | Concept trong `concepts.tsv` chưa có LO nào trỏ đến |
| **B** | `CIO_SHALLOW` | CIO có < 2 SIO con — phân rã chưa đủ sâu |
| **C** | `MASTER_CANDIDATE` | Concept từ `master_tree.json` liên quan đến syllabus nhưng chưa được chọn vào project |

## Khi nào dùng

- Sau khi `/generate-los` hoàn thành, trước khi `/sync-supabase`
- Khi muốn kiểm tra độ đầy đủ của Learning Objectives
- Khi thêm concept mới vào project và muốn đảm bảo coverage

## Prerequisites

- `projects/<project>/output/concepts.tsv` — phải tồn tại (chạy `/build-tree` trước)
- `projects/<project>/output/learning-objectives.tsv` — phải tồn tại (chạy `/generate-los` trước)

## Skill

Đọc và làm theo: `.agents/skills/tree-validator/SKILL.md`

## Lệnh thực thi

```bash
python3 .agents/skills/tree-validator/scripts/detect_gaps.py --project <slug>
```

**Options:**
- `--project <slug>` — Project slug (bỏ qua để dùng `active_project` từ `status.yaml`)
- `--min-score <float>` — Ngưỡng score cho Master Candidate (default: 2.0)
- `--top-n <int>` — Số lượng candidate tối đa (default: 20)

## Output

| File | Mô tả |
|---|---|
| `projects/<slug>/.tree-validator/reports/<stamp>/gap_report.md` | Report chính thức |
| `projects/<slug>/.work/gap_report.md` | Working copy để agent đọc |

## Contract

- **Gap A = 0:** Tất cả concepts có ít nhất 1 LO
- **Gap B = 0:** Tất cả CIOs có ít nhất 2 SIO con
- **Gap C:** Thông tin tham khảo — không phải lỗi, nhưng nên xem xét

## Hành động tiếp theo

| Kết quả | Hành động |
|---|---|
| Gap A > 0 | Bổ sung LO cho concepts thiếu, chạy lại `/generate-los` hoặc thêm thủ công |
| Gap B > 0 | Mở rộng SIO cho CIO thiếu, cập nhật `learning-objectives.tsv` |
| Gap C > 0 | Xem xét bổ sung vào `mapping-plan.md`, chạy lại `/build-tree` nếu cần |
| Tất cả pass | Tiến hành `/validate-tree` rồi `/sync-supabase` |
