# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-21T16:35:12.846925+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 10 (10 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 3 |
| subjects | 4 |
| categories | 8 |
| topics | 13 |
| concepts | 17 |
| learning_objectives | 109 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 10 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (10) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `STATE_DATA_FLOW` | subject_codes | 'DECLARATIVE_UI' không tồn tại trong bảng cha. |
| categories | `STATE_DATA_FLOW` | subject_codes | 'ASE' không tồn tại trong bảng cha. |
| categories | `UI_BUILDING_BLOCKS` | subject_codes | 'HCC' không tồn tại trong bảng cha. |
| topics | `DIGITAL_INTERACTION` | category_codes | 'DIGITAL_LITERACY' không tồn tại trong bảng cha. |
| concepts | `USER_CENTERED_DESIGN` | topic_codes | 'UI_UX_PROCESS' không tồn tại trong bảng cha. |
| concepts | `DIGITAL_IDENTITY` | topic_codes | 'DATA_PRIVACY_USER' không tồn tại trong bảng cha. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | topic_codes | 'VARIABLES_DATA_TYPES' không tồn tại trong bảng cha. |
| concepts | `REFERENCE_TYPE_DECLARATION` | topic_codes | 'VARIABLES_DATA_TYPES' không tồn tại trong bảng cha. |
| concepts | `FIRST_CLASS_FUNCTIONS` | topic_codes | 'FUNCTIONAL_PROG' không tồn tại trong bảng cha. |
| concepts | `STATE_PROPERTY_WRAPPER` | topic_codes | 'LOCAL_VIEW_STATE' không tồn tại trong bảng cha. |

## ⚠️ Cảnh báo (WARNING)

_Không có._
