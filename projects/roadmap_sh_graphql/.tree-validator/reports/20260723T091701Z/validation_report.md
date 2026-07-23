# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T09:17:01.194289+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 6 (6 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 1 |
| subjects | 1 |
| categories | 1 |
| topics | 16 |
| concepts | 16 |
| learning_objectives | 84 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 3 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 3 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (3) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-GRAPHQL-SYNC-ASYNC-PRODUCING-RESULT` | concept_codes | 'RESOLVER_EXECUTION_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-GRAPHQL-AUTHORIZATION-BATCHING` | concept_codes | 'GRAPHQL_SECURITY_RATE_LIMITING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-GRAPHQL-MERCURIUS-GRAPHENE-SERVERS` | concept_codes | 'APOLLO_SERVER_ENGINE' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (3) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-GRAPHQL-SYNC-ASYNC-PRODUCING-RESULT` | concept_codes | concept_code 'RESOLVER_EXECUTION_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-GRAPHQL-AUTHORIZATION-BATCHING` | concept_codes | concept_code 'GRAPHQL_SECURITY_RATE_LIMITING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-GRAPHQL-MERCURIUS-GRAPHENE-SERVERS` | concept_codes | concept_code 'APOLLO_SERVER_ENGINE' không tồn tại trong concepts.tsv của project. |

## ⚠️ Cảnh báo (WARNING)

_Không có._
