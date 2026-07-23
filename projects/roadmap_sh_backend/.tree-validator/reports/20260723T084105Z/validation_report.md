# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T08:41:05.283256+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 10 (1 lỗi, 9 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 1 |
| subjects | 1 |
| categories | 1 |
| topics | 1 |
| concepts | 7 |
| learning_objectives | 12 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 5 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 4 |
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `EMPTY_PARENT_REF` (1) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| topics | `BACKEND_ARCHITECTURE` | category_codes | Cột 'category_codes' rỗng — node không có cha. |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (5) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `BACKEND_ENGINEERING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `BACKEND_AUTHENTICATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `CACHING_STRATEGIES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `HTTP_PROTOCOL` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SYSTEM_DESIGN_SCALABILITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_CONCEPT_UNCOVERED` (4) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `HTTP_PROTOCOL` | - | Concept 'HTTP Protocol & Specification' (HTTP_PROTOCOL) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `BACKEND_AUTHENTICATION` | - | Concept 'Backend Auth & Security' (BACKEND_AUTHENTICATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `CACHING_STRATEGIES` | - | Concept 'Caching & Performance Optimization' (CACHING_STRATEGIES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `SYSTEM_DESIGN_SCALABILITY` | - | Concept 'System Design & Microservices' (SYSTEM_DESIGN_SCALABILITY) không có LO nào trỏ đến trong learning-objectives.tsv. |
