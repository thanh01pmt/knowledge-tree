# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-01T14:11:30.586398+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 284 (86 lỗi, 198 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 10 |
| categories | 19 |
| topics | 30 |
| concepts | 44 |
| learning_objectives | 547 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `LO_DESCRIPTION_PREFIX` | Mô tả LO không bắt đầu bằng 'Người học có khả năng' | 150 |
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 39 |
| `LO_TYPE_PARENT_MISMATCH` | lo_type=UNIVERSAL phải có parent_lo_code=NULL và ngược lại | 39 |
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 33 |
| `LO_INVALID_KNOWLEDGE_DIMENSION` | knowledge_dimension không thuộc tập giá trị cho phép | 15 |
| `DUPLICATE_CODE` | Code bị trùng trong cùng 1 file | 8 |

## ❌ Lỗi (ERROR) — cần sửa

### `EMPTY_PARENT_REF` (39) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-01` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-02` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-WHILE_LOOP-03-01` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-WHILE_LOOP-03-02` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `CIO-ERROR_MESSAGES_CONCEPT-02` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-REFERENCE_IMAGE_BY_NAME` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-REFERENCE_COLOR_BY_NAME` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_FOR_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_ENUMERATED` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_IN_PLACE_CONDITION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_WITH_MAP` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_COUNTER` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_BOOLEAN_FLAG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_USER_INPUT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_FUNCTION_RESULT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DECLARE_STATE_PROPERTY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-READ_ERROR_MESSAGE_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-LOCATE_ERROR_CAUSE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |

### `LO_TYPE_PARENT_MISMATCH` (39) — lo_type=UNIVERSAL phải có parent_lo_code=NULL và ngược lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-01` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-02` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-WHILE_LOOP-03-01` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-WHILE_LOOP-03-02` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `CIO-ERROR_MESSAGES_CONCEPT-02` | parent_lo_code | lo_type=CONCEPTUAL_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-REFERENCE_IMAGE_BY_NAME` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-REFERENCE_COLOR_BY_NAME` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_FOR_IN` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_ENUMERATED` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_IN_PLACE_CONDITION` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_WITH_MAP` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_COUNTER` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_BOOLEAN_FLAG` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_USER_INPUT` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_FUNCTION_RESULT` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-DECLARE_STATE_PROPERTY` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-READ_ERROR_MESSAGE_TYPE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-LOCATE_ERROR_CAUSE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |

### `DUPLICATE_CODE` (8) — Code bị trùng trong cùng 1 file

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01` | - | Code 'CIO-MALWARE_TYPES_CONCEPT-01' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02` | - | Code 'CIO-MALWARE_TYPES_CONCEPT-02' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-AI_BIAS-01` | - | Code 'CIO-AI_BIAS-01' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-AI_BIAS-02` | - | Code 'CIO-AI_BIAS-02' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | - | Code 'CIO-TWO_WAY_BINDING-01' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | - | Code 'CIO-TWO_WAY_BINDING-02' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01` | - | Code 'CIO-CROSS_ORIGIN_SECURITY-01' xuất hiện 2 lần trong file. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02` | - | Code 'CIO-CROSS_ORIGIN_SECURITY-02' xuất hiện 2 lần trong file. |

## ⚠️ Cảnh báo (WARNING)

### `LO_DESCRIPTION_PREFIX` (150) — Mô tả LO không bắt đầu bằng 'Người học có khả năng'

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-IF_ELSE_STATEMENT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IF_ELSE_STATEMENT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IF_ELSE_STATEMENT-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IF_ELSE_STATEMENT-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PRIMITIVE_TYPE_DECLARATION-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PRIMITIVE_TYPE_DECLARATION-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PRIMITIVE_TYPE_DECLARATION-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PRIMITIVE_TYPE_DECLARATION-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_FOOTPRINT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_FOOTPRINT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_FOOTPRINT-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_FOOTPRINT-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-RUNTIME_ERRORS-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-RUNTIME_ERRORS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-RUNTIME_ERRORS-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-RUNTIME_ERRORS-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-WCAG_PRINCIPLES-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-WCAG_PRINCIPLES-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-WCAG_PRINCIPLES-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-ALGORITHMIC_BIAS_SOCIETY-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-ALGORITHMIC_BIAS_SOCIETY-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-ALGORITHMIC_BIAS_SOCIETY-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PHISHING_IDENTIFICATION-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PHISHING_IDENTIFICATION-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FOR_LOOP-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FOR_LOOP-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FOR_LOOP-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FOR_LOOP-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-WIREFRAMING-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-WIREFRAMING-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-WIREFRAMING-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-LOGIC_ERRORS-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-LOGIC_ERRORS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-LOGIC_ERRORS-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-LOGIC_ERRORS-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-LOGIC_ERRORS-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-LOGIC_ERRORS-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SWITCH_CASE-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SWITCH_CASE-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SWITCH_CASE-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SWITCH_CASE-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CLASS_DEFINITION-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CLASS_DEFINITION-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-USER_CENTERED_DESIGN-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-USER_CENTERED_DESIGN-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-USER_CENTERED_DESIGN-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-AI_BIAS-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-AI_BIAS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-AI_BIAS-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-AI_BIAS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-SYNTAX_ERRORS-07` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PROTOTYPING-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PROTOTYPING-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PROTOTYPING-02-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PROTOTYPING-02-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PROTOTYPING-03-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-PROTOTYPING-03-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-BREAKPOINTS-01-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-BREAKPOINTS-01-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-BREAKPOINTS-02-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-BREAKPOINTS-02-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-BREAKPOINTS-03-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-BREAKPOINTS-03-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-01-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-01-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-02-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-02-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-03-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-03-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-TWO_WAY_BINDING-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-TWO_WAY_BINDING-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COLOR_THEORY-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COLOR_THEORY-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COLOR_THEORY-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COLOR_THEORY-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COLOR_THEORY-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-COLOR_THEORY-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |

### `CIO_INSUFFICIENT_SIO` (33) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | - | CIO 'Phân loại tài nguyên dự án theo loại' (CIO-PROJECT_ASSETS_MANAGEMENT-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | - | CIO 'Thêm tài nguyên vào cấu trúc dự án' (CIO-PROJECT_ASSETS_MANAGEMENT-03-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | - | CIO 'Tham chiếu tài nguyên bằng tên định danh' (CIO-PROJECT_ASSETS_MANAGEMENT-03-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-01` | - | CIO 'Duyệt mảng và truy cập từng phần tử' (CIO-ARRAY_OPERATIONS-03-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-02` | - | CIO 'Sửa đổi mảng tại chỗ dựa trên điều kiện' (CIO-ARRAY_OPERATIONS-03-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-03-01` | - | CIO 'Lặp với điều kiện kiểm tra trước' (CIO-WHILE_LOOP-03-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-03-02` | - | CIO 'Lặp với điều kiện phụ thuộc đầu vào' (CIO-WHILE_LOOP-03-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | - | CIO 'So sánh khai báo và mệnh lệnh trong xây dựng giao diện' (CIO-DECLARATIVE_UI_PARADIGM-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | - | CIO 'Áp dụng modifier theo chuỗi để tạo kiểu giao diện' (CIO-UI_MODIFIERS_CONCEPT-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | - | CIO 'Gắn hàm xử lý sự kiện tương tác' (CIO-EVENT_HANDLERS_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | - | CIO 'Khai báo và cập nhật biến trạng thái có giám sát' (CIO-STATE_PROPERTY_WRAPPER-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | - | CIO 'Phân loại lỗi dựa trên thời điểm phát hiện' (CIO-SYNTAX_VS_RUNTIME_ERRORS-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ERROR_MESSAGES_CONCEPT-02` | - | CIO 'Giải thích thông báo lỗi dựa trên cấu trúc' (CIO-ERROR_MESSAGES_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-01` | - | CIO 'Sử dụng cấu trúc rẽ nhánh dựa trên giá trị của biểu thức' (CIO-SWITCH_CASE-01) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-02` | - | CIO 'Sử dụng cấu trúc rẽ nhánh với trường hợp mặc định và nhiều giá trị' (CIO-SWITCH_CASE-02) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-03` | - | CIO 'Phân tích hành vi fall-through và break' (CIO-SWITCH_CASE-03) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-04` | - | CIO 'Phân tích xử lý trường hợp không khớp (default)' (CIO-SWITCH_CASE-04) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-02` | - | CIO 'Nhận diện lỗi cú pháp qua mẫu cấu trúc' (CIO-SYNTAX_ERRORS-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-03` | - | CIO 'Xác định vị trí lỗi dựa trên thông báo lỗi' (CIO-SYNTAX_ERRORS-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-04` | - | CIO 'Sửa lỗi cú pháp bằng cách điều chỉnh cấu trúc' (CIO-SYNTAX_ERRORS-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-05` | - | CIO 'Áp dụng quy trình sửa lỗi từng bước' (CIO-SYNTAX_ERRORS-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-06` | - | CIO 'Phân tích nguyên nhân gốc rễ của lỗi cú pháp phức tạp' (CIO-SYNTAX_ERRORS-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-07` | - | CIO 'So sánh lỗi cú pháp với lỗi logic để xác định bản chất' (CIO-SYNTAX_ERRORS-07) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | - | CIO 'Phân tích overhead của đồng bộ dữ liệu hai chiều' (CIO-TWO_WAY_BINDING-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | - | CIO 'So sánh chi phí cập nhật giữa binding một chiều và hai chiều' (CIO-TWO_WAY_BINDING-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-03` | - | CIO 'So sánh luồng dữ liệu một chiều và hai chiều' (CIO-TWO_WAY_BINDING-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-04` | - | CIO 'Xác định tác động của liên kết hai chiều đến hiệu suất' (CIO-TWO_WAY_BINDING-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | - | CIO 'Mô tả đặc điểm của hàm như một giá trị có thể gán, truyền và trả về' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | - | CIO 'So sánh hàm với các kiểu dữ liệu khác về khả năng thao tác' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | - | CIO 'Sử dụng hàm nhận hàm khác làm đối số để thực hiện thao tác trên từng phần tử' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | - | CIO 'Xây dựng pipeline xử lý dữ liệu bằng cách kết hợp các hàm biến đổi' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | - | CIO 'Tạo hàm bao bọc nhận một hàm và trả về hàm mới với hành vi mở rộng' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | - | CIO 'Thiết kế hàm nhận hàm xử lý và áp dụng nó trong một ngữ cảnh cụ thể' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |

### `LO_INVALID_KNOWLEDGE_DIMENSION` (15) — knowledge_dimension không thuộc tập giá trị cho phép

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-FOR_LOOP-01` | knowledge_dimension | knowledge_dimension='Conceptual Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-FOR_LOOP-02` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-FOR_LOOP-03` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-FOR_LOOP-04` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-WIREFRAMING-01` | knowledge_dimension | knowledge_dimension='Conceptual Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-WIREFRAMING-02` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-WIREFRAMING-03` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-LOGIC_ERRORS-01` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-LOGIC_ERRORS-02` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-LOGIC_ERRORS-03` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-LOGIC_ERRORS-04` | knowledge_dimension | knowledge_dimension='Conceptual Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-LOGIC_ERRORS-05` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-LOGIC_ERRORS-06` | knowledge_dimension | knowledge_dimension='Procedural Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01` | knowledge_dimension | knowledge_dimension='Conceptual Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02` | knowledge_dimension | knowledge_dimension='Conceptual Knowledge' không thuộc ['', 'CONCEPTUAL', 'Conceptual', 'FACTUAL', 'Factual', 'METACOGNITIVE', 'Metacognitive', 'NULL', 'PROCEDURAL', 'Procedural']. |
