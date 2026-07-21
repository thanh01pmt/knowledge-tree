# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-21T15:48:32.086741+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 52 (52 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 3 |
| subjects | 4 |
| categories | 5 |
| topics | 7 |
| concepts | 9 |
| learning_objectives | 103 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 52 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (52) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `STATE_DATA_FLOW` | subject_codes | 'DECLARATIVE_UI' không tồn tại trong bảng cha. |
| categories | `STATE_DATA_FLOW` | subject_codes | 'ASE' không tồn tại trong bảng cha. |
| categories | `UI_BUILDING_BLOCKS` | subject_codes | 'HCC' không tồn tại trong bảng cha. |
| topics | `DIGITAL_INTERACTION` | category_codes | 'DIGITAL_LITERACY' không tồn tại trong bảng cha. |
| concepts | `USER_CENTERED_DESIGN` | topic_codes | 'UI_UX_PROCESS' không tồn tại trong bảng cha. |
| concepts | `DIGITAL_IDENTITY` | topic_codes | 'DATA_PRIVACY_USER' không tồn tại trong bảng cha. |
| concepts | `STATE_PROPERTY_WRAPPER` | topic_codes | 'LOCAL_VIEW_STATE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEV-ENV` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-FILES` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-SWIFT-FILE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-ASSET-FILE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-ASSETS` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ASSETS-RECOGNIZE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ASSETS-IMPORT` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ASSETS-USE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-UI` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-NAVIGATOR` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-INSPECTOR` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FUNCTIONS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-FUNCTIONS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-WRITE` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-CALL` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-LABELS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-PARAMS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-RETURNS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-OPERATORS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-OP-ARITHMETIC` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-OP-LOGICAL` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CUSTOM-TYPES` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-STRUCTS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-DECL_PROP` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-INIT` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-METHODS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-INST_CREATE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-INST_USE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COLLECTIONS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-ARRAYS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARRAY-DECL` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARRAY-INIT` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARRAY-INDEX` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARRAY-MOD_INDEX` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARRAY-PROPS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARRAY-METHODS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROG-STATE` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-VARS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-DIFF` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-INFER` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-EXPLICIT` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-NAMING` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-NAME-CAMEL` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-NAME-RULES` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |

## ⚠️ Cảnh báo (WARNING)

_Không có._
