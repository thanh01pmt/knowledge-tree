# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-21T16:33:13.817845+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 87 (85 lỗi, 2 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 3 |
| subjects | 4 |
| categories | 5 |
| topics | 7 |
| concepts | 9 |
| learning_objectives | 109 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 85 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 2 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (85) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| categories | `STATE_DATA_FLOW` | subject_codes | 'ASE' không tồn tại trong bảng cha. |
| categories | `STATE_DATA_FLOW` | subject_codes | 'DECLARATIVE_UI' không tồn tại trong bảng cha. |
| categories | `UI_BUILDING_BLOCKS` | subject_codes | 'HCC' không tồn tại trong bảng cha. |
| topics | `DIGITAL_INTERACTION` | category_codes | 'DIGITAL_LITERACY' không tồn tại trong bảng cha. |
| concepts | `USER_CENTERED_DESIGN` | topic_codes | 'UI_UX_PROCESS' không tồn tại trong bảng cha. |
| concepts | `DIGITAL_IDENTITY` | topic_codes | 'DATA_PRIVACY_USER' không tồn tại trong bảng cha. |
| concepts | `STATE_PROPERTY_WRAPPER` | topic_codes | 'LOCAL_VIEW_STATE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IDE` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-FILES` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-SWIFT` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-PLIST` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-XCASSETS` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-ASSETS` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ASSET-IMPORT` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ASSET-RECOGNIZE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ASSET-USE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-XCODE-UI-AREAS` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-NAVIGATOR` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-INSPECTOR` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-XCODE-EDITOR` | concept_codes | 'IDE_NAVIGATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FUNCTIONS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-FUNCTIONS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-WRITE` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-CALL` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-LABELS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-PARAMS` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-FUNC-RETURN` | concept_codes | 'FUNCTIONS_METHODS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-OPERATORS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-OP-ARITHMETIC` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-OP-COMPOUND` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-OP-COMPARISON` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-OP-LOGICAL` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA-STRUCTURES` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-STRUCTS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-DECL` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-INIT` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-METHOD` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-INST-CREATE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STRUCT-INST-USE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COLLECTIONS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-ARRAYS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARR-DECL` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARR-INDEX-READ` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARR-INDEX-WRITE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARR-PROPS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ARR-METHODS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL-FLOW` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-CONDS` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-COND-IF` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-COND-SWITCH` | concept_codes | 'SWITCH_CASE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STATE` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-VARS` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-LET` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-INFERENCE` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-EXPLICIT` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VAR-TYPES` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-NAMING` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-NAME-CAMEL` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-NAME-RULES` | concept_codes | 'VARIABLES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DECLARATIVE` | concept_codes | 'DECLARATIVE_UI_MODEL' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFTUI-PARADIGM` | concept_codes | 'DECLARATIVE_UI_MODEL' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PARADIGM-DIFF` | concept_codes | 'DECLARATIVE_UI_MODEL' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFTUI-CONTENT` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VIEW-TEXT` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VIEW-IMAGE` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VIEW-SHAPE` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VIEW-COLOR` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFTUI-STACKS` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STACK-HSTACK` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STACK-VSTACK` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STACK-ZSTACK` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STACK-SPACER` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFTUI-HIERARCHY` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-HIERARCHY-PARENT` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFTUI-INTERACTIVE` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-INT-BUTTON` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-INT-TEXTFIELD` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-INT-SLIDER` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-INT-TOGGLE` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-STATE-BIND` | concept_codes | 'DATA_BINDING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING` | concept_codes | 'DEBUGGING_TECHNIQUES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SWIFT-INTERPRET` | concept_codes | 'ERROR_MESSAGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-MSG-CONSOLE` | concept_codes | 'ERROR_MESSAGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-MSG-FIX` | concept_codes | 'ERROR_MESSAGES' không tồn tại trong bảng cha. |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (2) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `DECLARATIVE_UI_PARADIGM` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `STATE_PROPERTY_WRAPPER` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
