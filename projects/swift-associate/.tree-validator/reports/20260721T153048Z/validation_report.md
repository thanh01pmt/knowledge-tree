# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-21T15:30:48.221521+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 17 (13 lỗi, 4 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 3 |
| subjects | 4 |
| categories | 5 |
| topics | 7 |
| concepts | 9 |
| learning_objectives | 15 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 13 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 4 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (13) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `STATE_DATA_FLOW` | subject_codes | 'ASE' không tồn tại trong bảng cha. |
| categories | `STATE_DATA_FLOW` | subject_codes | 'DECLARATIVE_UI' không tồn tại trong bảng cha. |
| categories | `UI_BUILDING_BLOCKS` | subject_codes | 'HCC' không tồn tại trong bảng cha. |
| topics | `DIGITAL_INTERACTION` | category_codes | 'DIGITAL_LITERACY' không tồn tại trong bảng cha. |
| concepts | `USER_CENTERED_DESIGN` | topic_codes | 'UI_UX_PROCESS' không tồn tại trong bảng cha. |
| concepts | `DIGITAL_IDENTITY` | topic_codes | 'DATA_PRIVACY_USER' không tồn tại trong bảng cha. |
| concepts | `STATE_PROPERTY_WRAPPER` | topic_codes | 'LOCAL_VIEW_STATE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEV-ENV` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-NAV` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROG-STATE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROG-STATE` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-VARS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-LET` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (4) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `DECLARATIVE_UI_PARADIGM` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DIGITAL_IDENTITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `UI_MODIFIERS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `WHILE_LOOP` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
