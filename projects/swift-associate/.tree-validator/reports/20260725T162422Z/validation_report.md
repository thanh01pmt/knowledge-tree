# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-25T16:24:22.395194+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 1 (0 lỗi, 1 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 12 |
| topics | 16 |
| concepts | 42 |
| learning_objectives | 445 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `INCONSISTENT_LINE_ENDINGS` (1) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `concepts.tsv` | - | File dùng line-ending CRLF, khác đa số các file khác (LF). |
