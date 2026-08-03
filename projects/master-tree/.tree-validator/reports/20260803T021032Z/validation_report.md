# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-03T02:10:32.067247+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 5 (5 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 6 |
| subjects | 25 |
| categories | 82 |
| topics | 137 |
| concepts | 269 |
| learning_objectives | 7560 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `MISSING_SEQUENCE_ORDER` | Thiếu cột sequence_order (Doc Chương 2.4: bảng N:N cần thứ tự sư phạm) | 5 |

## ❌ Lỗi (ERROR) — cần sửa

### `MISSING_SEQUENCE_ORDER` (5) — Thiếu cột sequence_order (Doc Chương 2.4: bảng N:N cần thứ tự sư phạm)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| fields | `-` | sequence_order | File fields.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| subjects | `-` | sequence_order | File subjects.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| categories | `-` | sequence_order | File categories.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| topics | `-` | sequence_order | File topics.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| concepts | `-` | sequence_order | File concepts.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |

## ⚠️ Cảnh báo (WARNING)

_Không có._
