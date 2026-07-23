# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T09:15:06.920483+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 5 (5 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 1 |
| subjects | 1 |
| categories | 1 |
| topics | 18 |
| concepts | 18 |
| learning_objectives | 96 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 2 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 2 |
| `LO_BROKEN_PARENT_REF` | parent_lo_code trỏ tới 1 LO không tồn tại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (2) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-REACT-APOLLO-GRAPHQL-CLIENT` | concept_codes | 'ASYNC_DATA_FETCHING_TANSTACK' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-REACT-VITEST-CYPRESS-PLAYWRIGHT` | concept_codes | 'TESTING_REACT_COMPONENTS' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (2) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-REACT-APOLLO-GRAPHQL-CLIENT` | concept_codes | concept_code 'ASYNC_DATA_FETCHING_TANSTACK' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-REACT-VITEST-CYPRESS-PLAYWRIGHT` | concept_codes | concept_code 'TESTING_REACT_COMPONENTS' không tồn tại trong concepts.tsv của project. |

### `LO_BROKEN_PARENT_REF` (1) — parent_lo_code trỏ tới 1 LO không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-REACT-APOLLO-GRAPHQL-CLIENT` | parent_lo_code | parent_lo_code 'CIO-SERVER-STATE-CACHING' không tồn tại. |

## ⚠️ Cảnh báo (WARNING)

_Không có._
