# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T08:41:05.717271+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 4 (1 lỗi, 3 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 1 |
| subjects | 1 |
| categories | 1 |
| topics | 1 |
| concepts | 3 |
| learning_objectives | 8 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 2 |
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 1 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `EMPTY_PARENT_REF` (1) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| topics | `ANGULAR_FRAMEWORK` | category_codes | Cột 'category_codes' rỗng — node không có cha. |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (2) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `FRONTEND_ENGINEERING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ANGULAR_SERVICES_ROUTING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_CONCEPT_UNCOVERED` (1) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `ANGULAR_SERVICES_ROUTING` | - | Concept 'Angular Services & Routing' (ANGULAR_SERVICES_ROUTING) không có LO nào trỏ đến trong learning-objectives.tsv. |
