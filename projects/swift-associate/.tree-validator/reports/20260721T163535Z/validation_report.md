# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-21T16:35:35.254183+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 19 (13 lỗi, 6 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 8 |
| categories | 11 |
| topics | 12 |
| concepts | 18 |
| learning_objectives | 109 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 13 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 6 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (13) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `STATE_DATA_FLOW` | subject_codes | 'DECLARATIVE_UI' không tồn tại trong bảng cha. |
| categories | `STATE_DATA_FLOW` | subject_codes | 'ASE' không tồn tại trong bảng cha. |
| categories | `UI_BUILDING_BLOCKS` | subject_codes | 'HCC' không tồn tại trong bảng cha. |
| topics | `DIGITAL_INTERACTION` | category_codes | 'DIGITAL_LITERACY' không tồn tại trong bảng cha. |
| concepts | `SYNTAX_VS_RUNTIME_ERRORS` | topic_codes | 'ERROR_MESSAGES' không tồn tại trong bảng cha. |
| concepts | `ERROR_MESSAGES` | topic_codes | 'TROUBLESHOOTING' không tồn tại trong bảng cha. |
| concepts | `DIGITAL_IDENTITY` | topic_codes | 'DATA_PRIVACY_USER' không tồn tại trong bảng cha. |
| concepts | `USER_CENTERED_DESIGN` | topic_codes | 'UI_UX_PROCESS' không tồn tại trong bảng cha. |
| concepts | `FIRST_CLASS_FUNCTIONS` | topic_codes | 'FUNCTIONAL_PROG' không tồn tại trong bảng cha. |
| concepts | `REFERENCE_TYPE_DECLARATION` | topic_codes | 'VARIABLES_DATA_TYPES' không tồn tại trong bảng cha. |
| concepts | `UI_MODIFIERS` | topic_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | topic_codes | 'VARIABLES_DATA_TYPES' không tồn tại trong bảng cha. |
| concepts | `STATE_PROPERTY_WRAPPER` | topic_codes | 'LOCAL_VIEW_STATE' không tồn tại trong bảng cha. |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (6) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| subjects | `DIGITAL_LITERACY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `DATA_PRIVACY_USER` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `FUNCTIONAL_PROG` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `TROUBLESHOOTING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `UI_UX_PROCESS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ERROR_MESSAGES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
