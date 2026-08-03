# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-02T18:42:19.447218+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 933 (460 lỗi, 473 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 6 |
| subjects | 25 |
| categories | 82 |
| topics | 137 |
| concepts | 270 |
| learning_objectives | 2212 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 302 |
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 227 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 227 |
| `LO_MISSING_ASSESSMENT_APPROACH` | ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc) | 139 |
| `CODE_FORMAT` | Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$ | 32 |
| `MISSING_SEQUENCE_ORDER` | Thiếu cột sequence_order (Doc Chương 2.4: bảng N:N cần thứ tự sư phạm) | 5 |
| `DUPLICATE_CODE` | Code bị trùng trong cùng 1 file | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (227) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-UI_CONTROLS-01` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_CONTROLS-02` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_CONTROLS-03` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTAINER_VIEWS-01` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTAINER_VIEWS-02` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STRUCTURE_TYPE-01` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STRUCTURE_TYPE-02` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_HIERARCHY-01` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_HIERARCHY-03` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-01` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-02` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA_TYPES-01` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA_TYPES-02` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA_TYPES-03` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LOOP_STRUCTURES-01` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LOOP_STRUCTURES-02` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LOOP_STRUCTURES-04` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL_FLOW-01` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL_FLOW-02` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL_FLOW-03` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-01` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-02` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-04` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-01` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-02` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ARRAYS-01` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ARRAYS-02` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ARRAYS-03` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-01` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-03` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SHAPE-01` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SHAPE-02` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SHAPE-03` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COLOR-01` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COLOR-02` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ACCESSIBILITY-01` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ACCESSIBILITY-02` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ACCESSIBILITY-03` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ACCESSIBILITY-04` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-02` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-03` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS-01` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS-02` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS-03` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS-04` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SENSITIVE_DATA-01` | concept_codes | 'SENSITIVE_DATA' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | concept_codes | 'SENSITIVE_DATA' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SENSITIVE_DATA-03` | concept_codes | 'SENSITIVE_DATA' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DESIGN_CYCLE-01` | concept_codes | 'DESIGN_CYCLE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DESIGN_CYCLE-02` | concept_codes | 'DESIGN_CYCLE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DESIGN_CYCLE-03` | concept_codes | 'DESIGN_CYCLE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-01` | concept_codes | 'NAMING_CONVENTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-02` | concept_codes | 'NAMING_CONVENTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | concept_codes | 'NAMING_CONVENTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING-01` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING-02` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING-03` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-02` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-01` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-03` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-01` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-02` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-04` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-GRAPH_THEORY-01` | concept_codes | 'GRAPH_THEORY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_CONTROLS-DESIGN_INTERACTION_PATTERN` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_CONTROLS-EVALUATE_USABILITY` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_CONCEPT-DESIGN_INTERACTION_PATTERN` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_CONCEPT-EVALUATE_USABILITY` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTAINER_VIEWS-DESIGN_INTERACTION_PATTERN` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTAINER_VIEWS-EVALUATE_USABILITY` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-STRUCTURE_TYPE-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-STRUCTURE_TYPE-REFACTOR_IMPLEMENTATION` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_HIERARCHY-DESIGN_INTERACTION_PATTERN` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_HIERARCHY-EVALUATE_USABILITY` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VARIABLES_AND_CONSTANTS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VARIABLES_AND_CONSTANTS-REFACTOR_IMPLEMENTATION` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DATA_TYPES-DESIGN_DATA_PIPELINE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DATA_TYPES-VALIDATE_DATA_QUALITY` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-LOOP_STRUCTURES-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-LOOP_STRUCTURES-REFACTOR_IMPLEMENTATION` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-DESIGN_INTERACTION_PATTERN` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-EVALUATE_USABILITY` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONDITIONAL_STATEMENTS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONDITIONAL_STATEMENTS-REFACTOR_IMPLEMENTATION` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FUNCTIONS_AND_PROCEDURES-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FUNCTIONS_AND_PROCEDURES-REFACTOR_IMPLEMENTATION` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-ARRAYS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-ARRAYS-REFACTOR_IMPLEMENTATION` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-REFACTOR_IMPLEMENTATION` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPERATIVE_PROGRAMMING-DESIGN_IMPLEMENTATION` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPERATIVE_PROGRAMMING-ANALYZE_IMPLEMENTATION` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SHAPE-DESIGN_IMPLEMENTATION` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SHAPE-ANALYZE_IMPLEMENTATION` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-COLOR-DESIGN_RENDERING_PIPELINE` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-COLOR-OPTIMIZE_VISUAL_QUALITY` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-ACCESSIBILITY-DESIGN` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-ACCESSIBILITY-ASSESS` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-DESIGN_INTERACTION_PATTERN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-EVALUATE_USABILITY` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-DESIGN_IMPLEMENTATION` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-ANALYZE_IMPLEMENTATION` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OPERATORS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OPERATORS-REFACTOR_IMPLEMENTATION` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-DESIGN_SECURITY_CONTROL` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ASSESS_VULNERABILITY` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SENSITIVE_DATA-DESIGN_IMPLEMENTATION` | concept_codes | 'SENSITIVE_DATA' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SENSITIVE_DATA-ANALYZE_IMPLEMENTATION` | concept_codes | 'SENSITIVE_DATA' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DESIGN_CYCLE-DESIGN_INTERACTION_PATTERN` | concept_codes | 'DESIGN_CYCLE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DESIGN_CYCLE-EVALUATE_USABILITY` | concept_codes | 'DESIGN_CYCLE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-NAMING_CONVENTIONS-DESIGN_IMPLEMENTATION` | concept_codes | 'NAMING_CONVENTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-NAMING_CONVENTIONS-ANALYZE_IMPLEMENTATION` | concept_codes | 'NAMING_CONVENTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-REFACTOR_IMPLEMENTATION` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-DESIGN_INTERACTION_PATTERN` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-EVALUATE_USABILITY` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-DESIGN_IMPLEMENTATION` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ANALYZE_IMPLEMENTATION` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-DESIGN_INTERACTION_PATTERN` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_USABILITY` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESIGN_INTERACTION_PATTERN` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_USABILITY` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_IMPLEMENTATION` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-ANALYZE_IMPLEMENTATION` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-REFACTOR_IMPLEMENTATION` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-GRAPH_THEORY-DESIGN` | concept_codes | 'GRAPH_THEORY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-GRAPH_THEORY-ASSESS` | concept_codes | 'GRAPH_THEORY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-UI_CONTROLS-PROTOTYPE_WITH_STREAMLIT` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-UI_CONTROLS-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VIEW_CONCEPT-PROTOTYPE_WITH_STREAMLIT` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VIEW_CONCEPT-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-CONTAINER_VIEWS-PROTOTYPE_WITH_STREAMLIT` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-CONTAINER_VIEWS-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-STRUCTURE_TYPE-IMPLEMENT_PATTERN` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-STRUCTURE_TYPE-REFACTOR_WITH_AST` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VIEW_HIERARCHY-PROTOTYPE_WITH_STREAMLIT` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VIEW_HIERARCHY-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VARIABLES_AND_CONSTANTS-IMPLEMENT_PATTERN` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VARIABLES_AND_CONSTANTS-REFACTOR_WITH_AST` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-DATA_TYPES-BUILD_DATA_PIPELINE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-DATA_TYPES-VALIDATE_WITH_GREAT_EXPECTATIONS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-LOOP_STRUCTURES-IMPLEMENT_PATTERN` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-LOOP_STRUCTURES-REFACTOR_WITH_AST` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-CONTROL_FLOW-PROTOTYPE_WITH_STREAMLIT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-CONTROL_FLOW-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-CONDITIONAL_STATEMENTS-IMPLEMENT_PATTERN` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-CONDITIONAL_STATEMENTS-REFACTOR_WITH_AST` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-FUNCTIONS_AND_PROCEDURES-IMPLEMENT_PATTERN` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-FUNCTIONS_AND_PROCEDURES-REFACTOR_WITH_AST` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-ARRAYS-IMPLEMENT_PATTERN` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-ARRAYS-REFACTOR_WITH_AST` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-TYPE_SYSTEM-IMPLEMENT_PATTERN` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-TYPE_SYSTEM-REFACTOR_WITH_AST` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-IMPERATIVE_PROGRAMMING-IMPLEMENT_SOLUTION` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-IMPERATIVE_PROGRAMMING-TEST_WITH_PYTEST` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-SHAPE-IMPLEMENT_SOLUTION` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-SHAPE-TEST_WITH_PYTEST` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-COLOR-RENDER_WITH_OPENGL/MODERNGL` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-COLOR-PROCESS_IMAGE_WITH_OPENCV` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-ACCESSIBILITY-IMPLEMENT_GOVERNANCE_CHECKLIST` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-ACCESSIBILITY-GENERATE_COMPLIANCE_REPORT` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VISUAL_DESIGN-PROTOTYPE_WITH_STREAMLIT` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-VISUAL_DESIGN-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-PYTHON-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-IMPLEMENT_SOLUTION` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| ... | ... | ... | (+260 dòng nữa) |

### `LO_CONCEPT_NOT_IN_PROJECT` (227) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-UI_CONTROLS-01` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_CONTROLS-02` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_CONTROLS-03` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTAINER_VIEWS-01` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTAINER_VIEWS-02` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STRUCTURE_TYPE-01` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STRUCTURE_TYPE-02` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_HIERARCHY-01` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_HIERARCHY-03` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-01` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-02` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DATA_TYPES-01` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DATA_TYPES-02` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DATA_TYPES-03` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LOOP_STRUCTURES-01` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LOOP_STRUCTURES-02` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LOOP_STRUCTURES-04` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTROL_FLOW-01` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTROL_FLOW-02` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTROL_FLOW-03` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-01` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-02` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-04` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-01` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-02` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ARRAYS-01` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ARRAYS-02` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ARRAYS-03` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-01` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-03` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SHAPE-01` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SHAPE-02` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SHAPE-03` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-COLOR-01` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-COLOR-02` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ACCESSIBILITY-01` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ACCESSIBILITY-02` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ACCESSIBILITY-03` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ACCESSIBILITY-04` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-02` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-03` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OPERATORS-01` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OPERATORS-02` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OPERATORS-03` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OPERATORS-04` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SENSITIVE_DATA-01` | concept_codes | concept_code 'SENSITIVE_DATA' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | concept_codes | concept_code 'SENSITIVE_DATA' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SENSITIVE_DATA-03` | concept_codes | concept_code 'SENSITIVE_DATA' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DESIGN_CYCLE-01` | concept_codes | concept_code 'DESIGN_CYCLE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DESIGN_CYCLE-02` | concept_codes | concept_code 'DESIGN_CYCLE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DESIGN_CYCLE-03` | concept_codes | concept_code 'DESIGN_CYCLE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-01` | concept_codes | concept_code 'NAMING_CONVENTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-02` | concept_codes | concept_code 'NAMING_CONVENTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | concept_codes | concept_code 'NAMING_CONVENTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DEBUGGING-01` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DEBUGGING-02` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DEBUGGING-03` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-02` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-01` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-03` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-01` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-02` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-04` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-GRAPH_THEORY-01` | concept_codes | concept_code 'GRAPH_THEORY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_CONTROLS-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_CONTROLS-EVALUATE_USABILITY` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_CONCEPT-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_CONCEPT-EVALUATE_USABILITY` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTAINER_VIEWS-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTAINER_VIEWS-EVALUATE_USABILITY` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-STRUCTURE_TYPE-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-STRUCTURE_TYPE-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_HIERARCHY-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_HIERARCHY-EVALUATE_USABILITY` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VARIABLES_AND_CONSTANTS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VARIABLES_AND_CONSTANTS-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DATA_TYPES-DESIGN_DATA_PIPELINE` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DATA_TYPES-VALIDATE_DATA_QUALITY` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-LOOP_STRUCTURES-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-LOOP_STRUCTURES-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-EVALUATE_USABILITY` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONDITIONAL_STATEMENTS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONDITIONAL_STATEMENTS-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FUNCTIONS_AND_PROCEDURES-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FUNCTIONS_AND_PROCEDURES-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-ARRAYS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-ARRAYS-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPERATIVE_PROGRAMMING-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPERATIVE_PROGRAMMING-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SHAPE-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SHAPE-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-COLOR-DESIGN_RENDERING_PIPELINE` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-COLOR-OPTIMIZE_VISUAL_QUALITY` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-ACCESSIBILITY-DESIGN` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-ACCESSIBILITY-ASSESS` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-EVALUATE_USABILITY` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OPERATORS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OPERATORS-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-DESIGN_SECURITY_CONTROL` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ASSESS_VULNERABILITY` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SENSITIVE_DATA-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'SENSITIVE_DATA' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SENSITIVE_DATA-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'SENSITIVE_DATA' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DESIGN_CYCLE-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'DESIGN_CYCLE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DESIGN_CYCLE-EVALUATE_USABILITY` | concept_codes | concept_code 'DESIGN_CYCLE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-NAMING_CONVENTIONS-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'NAMING_CONVENTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-NAMING_CONVENTIONS-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'NAMING_CONVENTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-EVALUATE_USABILITY` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_USABILITY` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESIGN_INTERACTION_PATTERN` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_USABILITY` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_IMPLEMENTATION` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-ANALYZE_IMPLEMENTATION` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-DESIGN_IMPLEMENTATION_PATTERN` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-REFACTOR_IMPLEMENTATION` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-GRAPH_THEORY-DESIGN` | concept_codes | concept_code 'GRAPH_THEORY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-GRAPH_THEORY-ASSESS` | concept_codes | concept_code 'GRAPH_THEORY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-UI_CONTROLS-PROTOTYPE_WITH_STREAMLIT` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-UI_CONTROLS-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VIEW_CONCEPT-PROTOTYPE_WITH_STREAMLIT` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VIEW_CONCEPT-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-CONTAINER_VIEWS-PROTOTYPE_WITH_STREAMLIT` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-CONTAINER_VIEWS-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-STRUCTURE_TYPE-IMPLEMENT_PATTERN` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-STRUCTURE_TYPE-REFACTOR_WITH_AST` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VIEW_HIERARCHY-PROTOTYPE_WITH_STREAMLIT` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VIEW_HIERARCHY-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VARIABLES_AND_CONSTANTS-IMPLEMENT_PATTERN` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VARIABLES_AND_CONSTANTS-REFACTOR_WITH_AST` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-DATA_TYPES-BUILD_DATA_PIPELINE` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-DATA_TYPES-VALIDATE_WITH_GREAT_EXPECTATIONS` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-LOOP_STRUCTURES-IMPLEMENT_PATTERN` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-LOOP_STRUCTURES-REFACTOR_WITH_AST` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-CONTROL_FLOW-PROTOTYPE_WITH_STREAMLIT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-CONTROL_FLOW-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-CONDITIONAL_STATEMENTS-IMPLEMENT_PATTERN` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-CONDITIONAL_STATEMENTS-REFACTOR_WITH_AST` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-FUNCTIONS_AND_PROCEDURES-IMPLEMENT_PATTERN` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-FUNCTIONS_AND_PROCEDURES-REFACTOR_WITH_AST` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-ARRAYS-IMPLEMENT_PATTERN` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-ARRAYS-REFACTOR_WITH_AST` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-TYPE_SYSTEM-IMPLEMENT_PATTERN` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-TYPE_SYSTEM-REFACTOR_WITH_AST` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-IMPERATIVE_PROGRAMMING-IMPLEMENT_SOLUTION` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-IMPERATIVE_PROGRAMMING-TEST_WITH_PYTEST` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-SHAPE-IMPLEMENT_SOLUTION` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-SHAPE-TEST_WITH_PYTEST` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-COLOR-RENDER_WITH_OPENGL/MODERNGL` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-COLOR-PROCESS_IMAGE_WITH_OPENCV` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-ACCESSIBILITY-IMPLEMENT_GOVERNANCE_CHECKLIST` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-ACCESSIBILITY-GENERATE_COMPLIANCE_REPORT` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VISUAL_DESIGN-PROTOTYPE_WITH_STREAMLIT` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-VISUAL_DESIGN-TEST_ACCESSIBILITY_WITH_AXE` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-PYTHON-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-IMPLEMENT_SOLUTION` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| ... | ... | ... | (+260 dòng nữa) |

### `MISSING_SEQUENCE_ORDER` (5) — Thiếu cột sequence_order (Doc Chương 2.4: bảng N:N cần thứ tự sư phạm)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| fields | `-` | sequence_order | File fields.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| subjects | `-` | sequence_order | File subjects.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| categories | `-` | sequence_order | File categories.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| topics | `-` | sequence_order | File topics.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| concepts | `-` | sequence_order | File concepts.tsv thiếu cột 'sequence_order' (Doc Chương 2.4: tất cả bảng N:N cần sequence_order). |
| ... | ... | ... | (+260 dòng nữa) |

### `DUPLICATE_CODE` (1) — Code bị trùng trong cùng 1 file

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-PROPOSITIONAL_LOGIC-01` | - | Code 'ULO-PROPOSITIONAL_LOGIC-01' xuất hiện 2 lần trong file. |
| ... | ... | ... | (+260 dòng nữa) |

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (302) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-UI_CONTROLS-EVALUATE_USABILITY` | - | CIO 'Identify common UI control types - Evaluate Usability' (CIO-UI_CONTROLS-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-VIEW_CONCEPT-EVALUATE_USABILITY` | - | CIO 'Define the concept of a view in UI development - Evaluate Usability' (CIO-VIEW_CONCEPT-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CONTAINER_VIEWS-EVALUATE_USABILITY` | - | CIO 'Recognize common container view types - Evaluate Usability' (CIO-CONTAINER_VIEWS-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STRUCTURE_TYPE-REFACTOR_IMPLEMENTATION` | - | CIO 'Recall the syntax for defining a structure type - Refactor Implementation' (CIO-STRUCTURE_TYPE-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-VIEW_HIERARCHY-EVALUATE_USABILITY` | - | CIO 'Identify the parent-child relationships in a view hierarchy - Evaluate Usability' (CIO-VIEW_HIERARCHY-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-VARIABLES_AND_CONSTANTS-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember Variables and Constants - Refactor Implementation' (CIO-VARIABLES_AND_CONSTANTS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DATA_TYPES-VALIDATE_DATA_QUALITY` | - | CIO 'Remember Basic Data Types - Validate Data Quality' (CIO-DATA_TYPES-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOOP_STRUCTURES-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember Loop Syntax - Refactor Implementation' (CIO-LOOP_STRUCTURES-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CONTROL_FLOW-EVALUATE_USABILITY` | - | CIO 'Understand Control Flow Concept - Evaluate Usability' (CIO-CONTROL_FLOW-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CONDITIONAL_STATEMENTS-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember Conditional Syntax - Refactor Implementation' (CIO-CONDITIONAL_STATEMENTS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FUNCTIONS_AND_PROCEDURES-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết khái niệm hàm và thủ tục - Refactor Implementation' (CIO-FUNCTIONS_AND_PROCEDURES-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAYS-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết khái niệm mảng và chỉ số - Refactor Implementation' (CIO-ARRAYS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TYPE_SYSTEM-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết các kiểu dữ liệu cơ bản và phân loại - Refactor Implementation' (CIO-TYPE_SYSTEM-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPERATIVE_PROGRAMMING-ANALYZE_IMPLEMENTATION` | - | CIO 'Nhận biết các câu lệnh cơ bản trong lập trình mệnh lệnh - Analyze Implementation' (CIO-IMPERATIVE_PROGRAMMING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SHAPE-ANALYZE_IMPLEMENTATION` | - | CIO 'Nhận biết khái niệm hình dạng và các loại cơ bản - Analyze Implementation' (CIO-SHAPE-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COLOR-OPTIMIZE_VISUAL_QUALITY` | - | CIO 'Nhận biết các mô hình màu phổ biến - Optimize Visual Quality' (CIO-COLOR-OPTIMIZE_VISUAL_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ACCESSIBILITY-ASSESS` | - | CIO 'Hiểu các nguyên tắc thiết kế tiếp cận - Assess' (CIO-ACCESSIBILITY-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-VISUAL_DESIGN-EVALUATE_USABILITY` | - | CIO 'Hiểu các nguyên tắc thiết kế trực quan - Evaluate Usability' (CIO-VISUAL_DESIGN-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-ANALYZE_IMPLEMENTATION` | - | CIO 'Hiểu các khái niệm pháp lý, đạo đức và kinh tế xã hội - Analyze Implementation' (CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-OPERATORS-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết các loại toán tử và ký hiệu - Refactor Implementation' (CIO-OPERATORS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ASSESS_VULNERABILITY` | - | CIO 'Nhận diện các thách thức bảo mật phổ biến - Assess Vulnerability' (CIO-SECURITY_CHALLENGES-ASSESS_VULNERABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SENSITIVE_DATA-ANALYZE_IMPLEMENTATION` | - | CIO 'Nhận diện các loại dữ liệu nhạy cảm - Analyze Implementation' (CIO-SENSITIVE_DATA-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DESIGN_CYCLE-EVALUATE_USABILITY` | - | CIO 'Mô tả các giai đoạn của chu kỳ thiết kế - Evaluate Usability' (CIO-DESIGN_CYCLE-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NAMING_CONVENTIONS-ANALYZE_IMPLEMENTATION` | - | CIO 'Nhận diện các quy ước đặt tên phổ biến trong lập trình - Analyze Implementation' (CIO-NAMING_CONVENTIONS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DEBUGGING-REFACTOR_IMPLEMENTATION` | - | CIO 'Mô tả quy trình gỡ lỗi cơ bản - Refactor Implementation' (CIO-DEBUGGING-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-EVALUATE_USABILITY` | - | CIO 'Nhận diện các UI Modifier phổ biến - Evaluate Usability' (CIO-UI_MODIFIERS_CONCEPT-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ANALYZE_IMPLEMENTATION` | - | CIO 'Nhận biết các loại tài nguyên trong dự án - Analyze Implementation' (CIO-PROJECT_ASSETS_MANAGEMENT-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-REFACTOR_IMPLEMENTATION` | - | CIO 'Hiểu quá trình tạo đối tượng từ lớp - Refactor Implementation' (CIO-OBJECT_INSTANTIATION-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_USABILITY` | - | CIO 'Hiểu mục đích và cơ chế của @State - Evaluate Usability' (CIO-STATE_PROPERTY_WRAPPER-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_IMPLEMENTATION` | - | CIO 'Hiểu mô hình xử lý sự kiện trong lập trình giao diện - Analyze Implementation' (CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết thuộc tính đối tượng - Refactor Implementation' (CIO-OBJECT_PROPERTIES-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_USABILITY` | - | CIO 'Giải thích mô hình giao diện khai báo - Evaluate Usability' (CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết lỗi cú pháp - Refactor Implementation' (CIO-SYNTAX_ERRORS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-RUNTIME_ERRORS-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết lỗi runtime - Refactor Implementation' (CIO-RUNTIME_ERRORS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ERROR_MESSAGES_CONCEPT-REFACTOR_IMPLEMENTATION` | - | CIO 'Nhận biết thành phần thông báo lỗi - Refactor Implementation' (CIO-ERROR_MESSAGES_CONCEPT-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-ANALYZE_IMPLEMENTATION` | - | CIO 'Nhận diện cú pháp return và phạm vi biến - Analyze Implementation' (CIO-RETURN_VALUES_AND_SCOPE-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember array element access syntax - Refactor Implementation' (CIO-ARRAY_OPERATIONS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-EVALUATE_USABILITY` | - | CIO 'Understand purpose of local view state - Evaluate Usability' (CIO-LOCAL_VIEW_STATE-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember while loop syntax - Refactor Implementation' (CIO-WHILE_LOOP-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember definitions of syntax and runtime errors - Refactor Implementation' (CIO-SYNTAX_VS_RUNTIME_ERRORS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-REFACTOR_IMPLEMENTATION` | - | CIO 'Remember syntax for declaring reference types - Refactor Implementation' (CIO-REFERENCE_TYPE_DECLARATION-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_USABILITY` | - | CIO 'Phân biệt implicit và explicit animation - Evaluate Usability' (CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROPOSITIONAL_LOGIC-ASSESS` | - | CIO 'Evaluate Boolean Expression - Assess' (CIO-PROPOSITIONAL_LOGIC-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GRAPH_THEORY-ASSESS` | - | CIO 'Analyze Graph Connections - Assess' (CIO-GRAPH_THEORY-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GRAPH_MODELS-ASSESS` | - | CIO 'Analyze Graph Connections - Assess' (CIO-GRAPH_MODELS-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PARAMETERIZED_QUANTUM_CIRCUITS-OPTIMIZE_PARAMETERS` | - | CIO 'Create Quantum Neural Network - Optimize Parameters' (CIO-PARAMETERIZED_QUANTUM_CIRCUITS-OPTIMIZE_PARAMETERS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-2D_3D_TRANSFORMATIONS_MATH-ANALYZE_COMPLEXITY` | - | CIO '2D/3D Geometric Transformations - Analyze Complexity' (CIO-2D_3D_TRANSFORMATIONS_MATH-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ABSTRACTION_LAYERS-ANALYZE_IMPLEMENTATION` | - | CIO 'Layers of Abstraction - Analyze Implementation' (CIO-ABSTRACTION_LAYERS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ACCESS_MODIFIERS-ANALYZE_IMPLEMENTATION` | - | CIO 'Access Modifiers - Analyze Implementation' (CIO-ACCESS_MODIFIERS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ADJUSTMENT_LAYERS-ANALYZE_IMPLEMENTATION` | - | CIO 'Non-Destructive Adjustment Layers - Analyze Implementation' (CIO-ADJUSTMENT_LAYERS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AFFORDANCES_SIGNIFIERS-ANALYZE_IMPLEMENTATION` | - | CIO 'Affordances and Signifiers - Analyze Implementation' (CIO-AFFORDANCES_SIGNIFIERS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AGENTIC_WORKFLOW_ORCHESTRATION-EVALUATE_MODEL` | - | CIO 'Agentic Workflow Orchestration - Evaluate Model' (CIO-AGENTIC_WORKFLOW_ORCHESTRATION-EVALUATE_MODEL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AGENT_MEMORY_SYSTEMS-PROGRAM_INTERFACE` | - | CIO 'Agent Memory Systems - Program Interface' (CIO-AGENT_MEMORY_SYSTEMS-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AGILE_PRINCIPLES-CONFIGURE_PROTOCOL` | - | CIO 'Agile Principles - Configure Protocol' (CIO-AGILE_PRINCIPLES-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AIOT_DATA_PIPELINE-VALIDATE_DATA_QUALITY` | - | CIO 'AIoT Edge Data Pipeline - Validate Data Quality' (CIO-AIOT_DATA_PIPELINE-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_ARTIFACT_VERIFICATION_AND_EVALUATION-ASSESS` | - | CIO 'AI Artifact Verification & Auditing - Assess' (CIO-AI_ARTIFACT_VERIFICATION_AND_EVALUATION-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-ASSESS` | - | CIO 'Bias in AI - Assess' (CIO-AI_BIAS-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_GOVERNANCE_AND_RED_TEAMING-ASSESS` | - | CIO 'AI Governance & Active Red-Teaming - Assess' (CIO-AI_GOVERNANCE_AND_RED_TEAMING-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_HISTORY_MILESTONES-EVALUATE_MODEL` | - | CIO 'History and Milestones of AI - Evaluate Model' (CIO-AI_HISTORY_MILESTONES-EVALUATE_MODEL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_VS_ML-EVALUATE_MODEL` | - | CIO 'AI vs. ML vs. Deep Learning - Evaluate Model' (CIO-AI_VS_ML-EVALUATE_MODEL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ALGORITHMIC_BIAS_SOCIETY-ASSESS` | - | CIO 'Algorithmic Bias in Society - Assess' (CIO-ALGORITHMIC_BIAS_SOCIETY-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ALGORITHMIC_GENERATIVE_ART-ANALYZE_COMPLEXITY` | - | CIO 'Algorithmic and Generative Art - Analyze Complexity' (CIO-ALGORITHMIC_GENERATIVE_ART-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-API_INTEGRATION-IMPLEMENT_API_CONTRACT` | - | CIO 'API Integration - Implement API Contract' (CIO-API_INTEGRATION-IMPLEMENT_API_CONTRACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-APP_EXTENSION_MODEL-ANALYZE_IMPLEMENTATION` | - | CIO 'App Extension Model - Analyze Implementation' (CIO-APP_EXTENSION_MODEL-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARDUINO_BASICS-ANALYZE_IMPLEMENTATION` | - | CIO 'microcontroller Basics - Analyze Implementation' (CIO-ARDUINO_BASICS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ASYNCHRONOUS_PROG_CONCEPT-REFACTOR_IMPLEMENTATION` | - | CIO 'Asynchronous Programming - Refactor Implementation' (CIO-ASYNCHRONOUS_PROG_CONCEPT-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AUTONOMOUS_DRONE_NAVIGATION-PROGRAM_INTERFACE` | - | CIO 'Autonomous Vehicle and Drone Navigation - Program Interface' (CIO-AUTONOMOUS_DRONE_NAVIGATION-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BACKEND_FRAMEWORKS-IMPLEMENT_API_CONTRACT` | - | CIO 'Backend Frameworks - Implement API Contract' (CIO-BACKEND_FRAMEWORKS-IMPLEMENT_API_CONTRACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BASIC_ELECTRONIC_COMPONENTS_CONCEPT-ANALYZE_IMPLEMENTATION` | - | CIO 'Basic Electronic Components - Analyze Implementation' (CIO-BASIC_ELECTRONIC_COMPONENTS_CONCEPT-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BASIC_MECHANISMS_CONCEPT-ANALYZE_IMPLEMENTATION` | - | CIO 'Basic Mechanisms - Analyze Implementation' (CIO-BASIC_MECHANISMS_CONCEPT-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BATTERY_MANAGEMENT_ALGORITHMS-ANALYZE_COMPLEXITY` | - | CIO 'Battery Management System (BMS) Health Algorithms - Analyze Complexity' (CIO-BATTERY_MANAGEMENT_ALGORITHMS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BEHAVIORAL_PATTERNS-ASSESS` | - | CIO 'Behavioral Design Patterns - Assess' (CIO-BEHAVIORAL_PATTERNS-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BIG_O_NOTATION-ANALYZE_IMPLEMENTATION` | - | CIO 'Big O Notation - Analyze Implementation' (CIO-BIG_O_NOTATION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BIOINFORMATICS_GENOMIC_ANALYSIS-ANALYZE_COMPLEXITY` | - | CIO 'Bioinformatics and Genomic Sequence Analysis - Analyze Complexity' (CIO-BIOINFORMATICS_GENOMIC_ANALYSIS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BOOLEAN_OPERATIONS_3D-OPTIMIZE_VISUAL_QUALITY` | - | CIO '3D Boolean Operations - Optimize Visual Quality' (CIO-BOOLEAN_OPERATIONS_3D-OPTIMIZE_VISUAL_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BREAKPOINTS-ANALYZE_IMPLEMENTATION` | - | CIO 'Using Breakpoints - Analyze Implementation' (CIO-BREAKPOINTS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BUBBLE_INSERTION_SORT-ANALYZE_COMPLEXITY` | - | CIO 'Bubble Sort & Insertion Sort - Analyze Complexity' (CIO-BUBBLE_INSERTION_SORT-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CACHE_HIERARCHY-ANALYZE_IMPLEMENTATION` | - | CIO 'Cache Hierarchy - Analyze Implementation' (CIO-CACHE_HIERARCHY-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CAP_THEOREM-ANALYZE_IMPLEMENTATION` | - | CIO 'CAP Theorem - Analyze Implementation' (CIO-CAP_THEOREM-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CARBON_FOOTPRINT_ACCOUNTING_SOFTWARE-ASSESS` | - | CIO 'Carbon Accounting and Life-Cycle Assessment Software - Assess' (CIO-CARBON_FOOTPRINT_ACCOUNTING_SOFTWARE-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CHART_TYPES-REFACTOR_IMPLEMENTATION` | - | CIO 'Choosing Appropriate Chart Types - Refactor Implementation' (CIO-CHART_TYPES-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CIRCUIT_PRINCIPLES_CONCEPT-CONFIGURE_PROTOCOL` | - | CIO 'Basic Circuit Principles - Configure Protocol' (CIO-CIRCUIT_PRINCIPLES_CONCEPT-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CLASS_DEFINITION-REFACTOR_IMPLEMENTATION` | - | CIO 'Class Definition - Refactor Implementation' (CIO-CLASS_DEFINITION-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CLOSED_LOOP_NEUROSTIMULATION-REFACTOR_IMPLEMENTATION` | - | CIO 'Closed-Loop Neurostimulation and Bio-Prosthetics - Refactor Implementation' (CIO-CLOSED_LOOP_NEUROSTIMULATION-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CLOUD_DEPLOYMENT_MODELS-IMPLEMENT_API_CONTRACT` | - | CIO 'Cloud Deployment Models - Implement API Contract' (CIO-CLOUD_DEPLOYMENT_MODELS-IMPLEMENT_API_CONTRACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CLOUD_MODELS_IAAS_PAAS_SAAS-IMPLEMENT_API_CONTRACT` | - | CIO 'Cloud Service Models - Implement API Contract' (CIO-CLOUD_MODELS_IAAS_PAAS_SAAS-IMPLEMENT_API_CONTRACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CLUSTERING_ALGORITHMS-ANALYZE_COMPLEXITY` | - | CIO 'Clustering Algorithms - Analyze Complexity' (CIO-CLUSTERING_ALGORITHMS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COLLABORATIVE_PLATFORMS-ANALYZE_IMPLEMENTATION` | - | CIO 'Collaborative Platforms - Analyze Implementation' (CIO-COLLABORATIVE_PLATFORMS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COLLISION_DETECTION-OPTIMIZE_PERFORMANCE` | - | CIO 'Collision Detection - Optimize Performance' (CIO-COLLISION_DETECTION-OPTIMIZE_PERFORMANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COLOR_THEORY-OPTIMIZE_VISUAL_QUALITY` | - | CIO 'Color Theory - Optimize Visual Quality' (CIO-COLOR_THEORY-OPTIMIZE_VISUAL_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COLOR_THEORY_AND_PALETTE_DESIGN-EVALUATE_USABILITY` | - | CIO 'Color Theory and Digital Palette Systems - Evaluate Usability' (CIO-COLOR_THEORY_AND_PALETTE_DESIGN-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COMBINATORICS-PROVE_CORRECTNESS` | - | CIO 'Combinatorics - Prove Correctness' (CIO-COMBINATORICS-PROVE_CORRECTNESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COMPOSITION_PRINCIPLES-CONFIGURE_PROTOCOL` | - | CIO 'Composition Principles - Configure Protocol' (CIO-COMPOSITION_PRINCIPLES-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COMPUTATIONAL_GENETICS_MODELS-ANALYZE_COMPLEXITY` | - | CIO 'Computational Genetics and Evolutionary Models - Analyze Complexity' (CIO-COMPUTATIONAL_GENETICS_MODELS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COMPUTER_VISION_FEATURE_EXTRACTION-ANALYZE_IMPLEMENTATION` | - | CIO 'Computer Vision Feature Extraction and Segmentation - Analyze Implementation' (CIO-COMPUTER_VISION_FEATURE_EXTRACTION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COMPUTE_IN_MEMORY_ACCELERATION-PROGRAM_INTERFACE` | - | CIO 'Compute-in-Memory Edge Acceleration - Program Interface' (CIO-COMPUTE_IN_MEMORY_ACCELERATION-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COPYRIGHT_CREATIVE_COMMONS-EVALUATE_COMPLIANCE` | - | CIO 'Copyright & Creative Commons - Evaluate Compliance' (CIO-COPYRIGHT_CREATIVE_COMMONS-EVALUATE_COMPLIANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CORE_DATA_ORM-VALIDATE_DATA_QUALITY` | - | CIO 'Core Data (ORM) - Validate Data Quality' (CIO-CORE_DATA_ORM-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CPU_ARCHITECTURE-PROGRAM_INTERFACE` | - | CIO 'CPU Architecture - Program Interface' (CIO-CPU_ARCHITECTURE-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CREATIONAL_PATTERNS-ASSESS` | - | CIO 'Creational Design Patterns - Assess' (CIO-CREATIONAL_PATTERNS-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSSCUTTING_SCIENCE_CONCEPTS-ANALYZE_IMPLEMENTATION` | - | CIO 'Crosscutting Concepts in Science and Systems - Analyze Implementation' (CIO-CROSSCUTTING_SCIENCE_CONCEPTS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CSS_SELECTORS-IMPLEMENT_API_CONTRACT` | - | CIO 'CSS Selectors - Implement API Contract' (CIO-CSS_SELECTORS-IMPLEMENT_API_CONTRACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CYBERBULLYING-EVALUATE_COMPLIANCE` | - | CIO 'Cyberbullying and Response - Evaluate Compliance' (CIO-CYBERBULLYING-EVALUATE_COMPLIANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DATABASE_NORMALIZATION-VALIDATE_DATA_QUALITY` | - | CIO 'Database Normalization - Validate Data Quality' (CIO-DATABASE_NORMALIZATION-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DATA_CLEANING_TECHNIQUES-VALIDATE_DATA_QUALITY` | - | CIO 'Data Cleaning Techniques - Validate Data Quality' (CIO-DATA_CLEANING_TECHNIQUES-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DATA_DISTRIBUTIONS-VALIDATE_DATA_QUALITY` | - | CIO 'Basic Data Distributions - Validate Data Quality' (CIO-DATA_DISTRIBUTIONS-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DATA_EXPLORATION_EDA-VALIDATE_DATA_QUALITY` | - | CIO 'Exploratory Data Analysis (EDA) - Validate Data Quality' (CIO-DATA_EXPLORATION_EDA-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DATA_LITERACY_DIKW_MODEL-VALIDATE_DATA_QUALITY` | - | CIO 'Data Literacy & DIKW Pyramid - Validate Data Quality' (CIO-DATA_LITERACY_DIKW_MODEL-VALIDATE_DATA_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECENTRALIZED_LEDGER_CONSENSUS-CONFIGURE_PROTOCOL_STACK` | - | CIO 'Decentralized Ledger Cryptographic Consensus - Configure Protocol Stack' (CIO-DECENTRALIZED_LEDGER_CONSENSUS-CONFIGURE_PROTOCOL_STACK) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DESIGN_THINKING_PROCESS-ASSESS` | - | CIO 'Design Thinking & Human-Centered Innovation - Assess' (CIO-DESIGN_THINKING_PROCESS-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIGITAL_ANALOG_IO-REFACTOR_IMPLEMENTATION` | - | CIO 'Digital vs. Analog I/O Pins - Refactor Implementation' (CIO-DIGITAL_ANALOG_IO-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIGITAL_DIVIDE-REFACTOR_IMPLEMENTATION` | - | CIO 'The Digital Divide - Refactor Implementation' (CIO-DIGITAL_DIVIDE-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIGITAL_FILTERING_AND_SAMPLING-REFACTOR_IMPLEMENTATION` | - | CIO 'Digital Filtering and Nyquist Sampling Theorem - Refactor Implementation' (CIO-DIGITAL_FILTERING_AND_SAMPLING-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIGITAL_FOOTPRINT-REFACTOR_IMPLEMENTATION` | - | CIO 'Digital Footprint - Refactor Implementation' (CIO-DIGITAL_FOOTPRINT-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-REFACTOR_IMPLEMENTATION` | - | CIO 'Digital Identity Management - Refactor Implementation' (CIO-DIGITAL_IDENTITY-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIGITAL_TWIN_SIMULATION-ANALYZE_COMPLEXITY` | - | CIO 'Digital Twin Simulation and Telemetry Sync - Analyze Complexity' (CIO-DIGITAL_TWIN_SIMULATION-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DIVIDE_CONQUER-ANALYZE_COMPLEXITY` | - | CIO 'Divide and Conquer - Analyze Complexity' (CIO-DIVIDE_CONQUER-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DMA_CONCEPT-ANALYZE_IMPLEMENTATION` | - | CIO 'Direct Memory Access (DMA) - Analyze Implementation' (CIO-DMA_CONCEPT-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DNS_LOOKUP-CONFIGURE_PROTOCOL` | - | CIO 'DNS Lookup Process - Configure Protocol' (CIO-DNS_LOOKUP-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DOM_MANIPULATION-CONFIGURE_PROTOCOL` | - | CIO 'DOM Manipulation - Configure Protocol' (CIO-DOM_MANIPULATION-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DRAG_GESTURE-EVALUATE_USABILITY` | - | CIO 'Drag Gesture - Evaluate Usability' (CIO-DRAG_GESTURE-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DURABLE_AGENT_STATE_MANAGEMENT-EVALUATE_USABILITY` | - | CIO 'Durable Agent State Management - Evaluate Usability' (CIO-DURABLE_AGENT_STATE_MANAGEMENT-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DYNAMIC_PROGRAMMING-ANALYZE_COMPLEXITY` | - | CIO 'Dynamic Programming - Analyze Complexity' (CIO-DYNAMIC_PROGRAMMING-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-EDGE_MODEL_QUANTIZATION-CONFIGURE_PROTOCOL_STACK` | - | CIO 'Edge Model Quantization and Compression - Configure Protocol Stack' (CIO-EDGE_MODEL_QUANTIZATION-CONFIGURE_PROTOCOL_STACK) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ENGINEERING_DESIGN_CYCLE-ASSESS` | - | CIO 'Engineering Design Cycle and Prototyping - Assess' (CIO-ENGINEERING_DESIGN_CYCLE-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ETHICAL_AI_AND_BIAS_AWARENESS-ASSESS` | - | CIO 'Ethical AI and Algorithmic Bias Awareness - Assess' (CIO-ETHICAL_AI_AND_BIAS_AWARENESS-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-EVENT_BASED_PROGRAMMING-ANALYZE_IMPLEMENTATION` | - | CIO 'Event-Based Programming Model - Analyze Implementation' (CIO-EVENT_BASED_PROGRAMMING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FEEDBACK_AND_RESPONSE-ANALYZE_IMPLEMENTATION` | - | CIO 'Feedback and System Response - Analyze Implementation' (CIO-FEEDBACK_AND_RESPONSE-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FETCH_DECODE_EXECUTE-ANALYZE_IMPLEMENTATION` | - | CIO 'Fetch-Decode-Execute Cycle - Analyze Implementation' (CIO-FETCH_DECODE_EXECUTE-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FILE_ALLOCATION-ANALYZE_IMPLEMENTATION` | - | CIO 'File Allocation Methods - Analyze Implementation' (CIO-FILE_ALLOCATION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-REFACTOR_IMPLEMENTATION` | - | CIO 'First-Class & Higher-Order Functions - Refactor Implementation' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FORMAL_PROGRAM_VERIFICATION-ASSESS` | - | CIO 'Formal Program Verification and Model Checking - Assess' (CIO-FORMAL_PROGRAM_VERIFICATION-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FOR_LOOP-REFACTOR_IMPLEMENTATION` | - | CIO 'For Loop - Refactor Implementation' (CIO-FOR_LOOP-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FOURIER_TRANSFORM_SIGNAL_ANALYSIS-ANALYZE_COMPLEXITY` | - | CIO 'Fourier Transform and Frequency Analysis - Analyze Complexity' (CIO-FOURIER_TRANSFORM_SIGNAL_ANALYSIS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FRONTEND_FRAMEWORKS-IMPLEMENT_API_CONTRACT` | - | CIO 'Frontend Frameworks/Libraries - Implement API Contract' (CIO-FRONTEND_FRAMEWORKS-IMPLEMENT_API_CONTRACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GAME_LOOP-REFACTOR_IMPLEMENTATION` | - | CIO 'Game Loop - Refactor Implementation' (CIO-GAME_LOOP-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GRADIENT_DESCENT_OPTIMIZATION-ASSESS` | - | CIO 'Gradient Descent and Convex Optimization - Assess' (CIO-GRADIENT_DESCENT_OPTIMIZATION-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GRAPH_BASED_AGENTIC_WORKFLOW-ANALYZE_COMPLEXITY` | - | CIO 'Graph-Based Agentic Workflow - Analyze Complexity' (CIO-GRAPH_BASED_AGENTIC_WORKFLOW-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GREEDY_ALGORITHMS-ANALYZE_COMPLEXITY` | - | CIO 'Greedy Algorithms - Analyze Complexity' (CIO-GREEDY_ALGORITHMS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-HDD_VS_SSD-ANALYZE_IMPLEMENTATION` | - | CIO 'HDD vs. SSD - Analyze Implementation' (CIO-HDD_VS_SSD-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-HTML_STRUCTURE-EVALUATE_MODEL` | - | CIO 'HTML Document Structure - Evaluate Model' (CIO-HTML_STRUCTURE-EVALUATE_MODEL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-HTTP_METHODS-CONFIGURE_PROTOCOL` | - | CIO 'HTTP Methods (GET, POST) - Configure Protocol' (CIO-HTTP_METHODS-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-HYBRID_VECTOR_SPARSE_SEARCH-ANALYZE_COMPLEXITY` | - | CIO 'Hybrid Vector and Sparse Search - Analyze Complexity' (CIO-HYBRID_VECTOR_SPARSE_SEARCH-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IDENTITY_AND_ACCESS_MANAGEMENT-EVALUATE_COMPLIANCE` | - | CIO 'Identity and Access Management - Evaluate Compliance' (CIO-IDENTITY_AND_ACCESS_MANAGEMENT-EVALUATE_COMPLIANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IF_ELSE_STATEMENT-EVALUATE_USABILITY` | - | CIO 'If-Else Statement - Evaluate Usability' (CIO-IF_ELSE_STATEMENT-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMAGE_COMPOSITING-ANALYZE_IMPLEMENTATION` | - | CIO 'Image Compositing - Analyze Implementation' (CIO-IMAGE_COMPOSITING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMAGE_RETOUCHING-ANALYZE_IMPLEMENTATION` | - | CIO 'Image Retouching Techniques - Analyze Implementation' (CIO-IMAGE_RETOUCHING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMAGE_WARPING-ANALYZE_IMPLEMENTATION` | - | CIO 'Mesh and Liquify Warping - Analyze Implementation' (CIO-IMAGE_WARPING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMMUTABILITY_CONCEPT-REFACTOR_IMPLEMENTATION` | - | CIO 'Immutability and Pure Functions - Refactor Implementation' (CIO-IMMUTABILITY_CONCEPT-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-INCLUSIVE_DESIGN_ACCESSIBILITY_WCAG-ASSESS` | - | CIO 'Inclusive Design and Accessibility Standards - Assess' (CIO-INCLUSIVE_DESIGN_ACCESSIBILITY_WCAG-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-INFORMATION_CREDIBILITY-ASSESS` | - | CIO 'Assessing Information Credibility - Assess' (CIO-INFORMATION_CREDIBILITY-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-INFORMATION_ENTROPY_METRICS-PROVE_CORRECTNESS` | - | CIO 'Information Entropy and Mutual Information - Prove Correctness' (CIO-INFORMATION_ENTROPY_METRICS-PROVE_CORRECTNESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-INHERITANCE_SYNTAX-REFACTOR_IMPLEMENTATION` | - | CIO 'Inheritance Syntax - Refactor Implementation' (CIO-INHERITANCE_SYNTAX-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IOT_PROTOCOLS_MQTT_CONCEPT-CONFIGURE_PROTOCOL` | - | CIO 'IoT Messaging Protocols (MQTT) - Configure Protocol' (CIO-IOT_PROTOCOLS_MQTT_CONCEPT-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IOT_SAFETY_RISKS-CONFIGURE_PROTOCOL_STACK` | - | CIO 'IoT Safety Risks - Configure Protocol Stack' (CIO-IOT_SAFETY_RISKS-CONFIGURE_PROTOCOL_STACK) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IOT_SECURITY_THREATS-ASSESS_VULNERABILITY` | - | CIO 'Common IoT Security Threats - Assess Vulnerability' (CIO-IOT_SECURITY_THREATS-ASSESS_VULNERABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IO_METHODS_POLLING_INTERRUPT-PROGRAM_INTERFACE` | - | CIO 'I/O Methods: Polling vs. Interrupt - Program Interface' (CIO-IO_METHODS_POLLING_INTERRUPT-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IPV4_VS_IPV6-CONFIGURE_PROTOCOL` | - | CIO 'IPv4 vs. IPv6 - Configure Protocol' (CIO-IPV4_VS_IPV6-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-JSON_SERIALIZATION-ANALYZE_IMPLEMENTATION` | - | CIO 'JSON Serialization/Deserialization - Analyze Implementation' (CIO-JSON_SERIALIZATION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-KEYFRAME_ANIMATION-EVALUATE_USABILITY` | - | CIO 'Keyframe Animation - Evaluate Usability' (CIO-KEYFRAME_ANIMATION-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-KEY_VALUE_PERSISTENCE-ANALYZE_IMPLEMENTATION` | - | CIO 'Key-Value Persistence - Analyze Implementation' (CIO-KEY_VALUE_PERSISTENCE-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-KNOWLEDGE_GRAPH_RETRIEVAL_AUGMENTATION-ANALYZE_COMPLEXITY` | - | CIO 'Knowledge Graph-Augmented Retrieval - Analyze Complexity' (CIO-KNOWLEDGE_GRAPH_RETRIEVAL_AUGMENTATION-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LARGE_LANGUAGE_MODEL_CONCEPTS-ANALYZE_IMPLEMENTATION` | - | CIO 'Large Language Model Principles - Analyze Implementation' (CIO-LARGE_LANGUAGE_MODEL_CONCEPTS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LAYER_BLEND_MODES-ANALYZE_IMPLEMENTATION` | - | CIO 'Layer Blending Modes - Analyze Implementation' (CIO-LAYER_BLEND_MODES-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LAYER_MASKING-ANALYZE_IMPLEMENTATION` | - | CIO 'Layer Masking - Analyze Implementation' (CIO-LAYER_MASKING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LAYOUT_GRID_AND_COMPOSITION_RULES-EVALUATE_USABILITY` | - | CIO 'Layout Grid and Compositional Rules - Evaluate Usability' (CIO-LAYOUT_GRID_AND_COMPOSITION_RULES-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LEADERBOARD_SYSTEM-OPTIMIZE_PERFORMANCE` | - | CIO 'Leaderboard/Scoring System - Optimize Performance' (CIO-LEADERBOARD_SYSTEM-OPTIMIZE_PERFORMANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LEVEL_LAYOUT-ASSESS` | - | CIO 'Level Layout Design - Assess' (CIO-LEVEL_LAYOUT-ASSESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LIGHTING_AND_SHADOWS-ANALYZE_IMPLEMENTATION` | - | CIO 'Lighting and Shadows - Analyze Implementation' (CIO-LIGHTING_AND_SHADOWS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LIGHT_MOTION_SENSORS-PROGRAM_INTERFACE` | - | CIO 'Reading Light/Motion Sensors - Program Interface' (CIO-LIGHT_MOTION_SENSORS-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LINEAR_BINARY_SEARCH-ANALYZE_COMPLEXITY` | - | CIO 'Linear vs. Binary Search - Analyze Complexity' (CIO-LINEAR_BINARY_SEARCH-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LIST_OPERATIONS-REFACTOR_IMPLEMENTATION` | - | CIO 'List Operations - Refactor Implementation' (CIO-LIST_OPERATIONS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_NOTIFICATION_API-ANALYZE_IMPLEMENTATION` | - | CIO 'Local Notification API - Analyze Implementation' (CIO-LOCAL_NOTIFICATION_API-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCATION_SERVICES_API-ANALYZE_IMPLEMENTATION` | - | CIO 'Location Services API - Analyze Implementation' (CIO-LOCATION_SERVICES_API-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOGIC_ERRORS-REFACTOR_IMPLEMENTATION` | - | CIO 'Logical Errors - Refactor Implementation' (CIO-LOGIC_ERRORS-REFACTOR_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOGIC_GATES-PROVE_CORRECTNESS` | - | CIO 'Logic Gates (AND, OR, NOT) - Prove Correctness' (CIO-LOGIC_GATES-PROVE_CORRECTNESS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-ASSESS_VULNERABILITY` | - | CIO 'Malware Types - Assess Vulnerability' (CIO-MALWARE_TYPES_CONCEPT-ASSESS_VULNERABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MAPREDUCE_CONCEPT-ANALYZE_COMPLEXITY` | - | CIO 'MapReduce Concept - Analyze Complexity' (CIO-MAPREDUCE_CONCEPT-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MAP_INTEGRATION-ANALYZE_IMPLEMENTATION` | - | CIO 'Map Integration - Analyze Implementation' (CIO-MAP_INTEGRATION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MARITIME_UNDERWATER_ROBOTICS-PROGRAM_INTERFACE` | - | CIO 'Autonomous Underwater Robotics and Acoustic Sensing - Program Interface' (CIO-MARITIME_UNDERWATER_ROBOTICS-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MATERIAL_AND_TEXTURE-OPTIMIZE_VISUAL_QUALITY` | - | CIO 'Material and Texture Mapping - Optimize Visual Quality' (CIO-MATERIAL_AND_TEXTURE-OPTIMIZE_VISUAL_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MECHATRONICS_SYSTEMS_DIAGNOSTICS-ANALYZE_IMPLEMENTATION` | - | CIO 'Mechatronics and Control Systems Diagnostics - Analyze Implementation' (CIO-MECHATRONICS_SYSTEMS_DIAGNOSTICS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MEDIA_PICKER_API-ANALYZE_IMPLEMENTATION` | - | CIO 'Media Picker API - Analyze Implementation' (CIO-MEDIA_PICKER_API-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MEDICAL_IMAGE_DICOM_SEGMENTATION-ANALYZE_IMPLEMENTATION` | - | CIO 'Medical Image DICOM Segmentation and Analytics - Analyze Implementation' (CIO-MEDICAL_IMAGE_DICOM_SEGMENTATION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MEMORY_TYPES-PROGRAM_INTERFACE` | - | CIO 'Memory Types - Program Interface' (CIO-MEMORY_TYPES-PROGRAM_INTERFACE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MESH_EXTRUSION-OPTIMIZE_VISUAL_QUALITY` | - | CIO 'Mesh Extrusion - Optimize Visual Quality' (CIO-MESH_EXTRUSION-OPTIMIZE_VISUAL_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-METHOD_OVERRIDING-ANALYZE_IMPLEMENTATION` | - | CIO 'Method Overriding - Analyze Implementation' (CIO-METHOD_OVERRIDING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MODEL_CONTEXT_PROTOCOL_STANDARD-CONFIGURE_PROTOCOL` | - | CIO 'Model Context Protocol Standard - Configure Protocol' (CIO-MODEL_CONTEXT_PROTOCOL_STANDARD-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MOLECULAR_DYNAMICS_MODELING-ANALYZE_COMPLEXITY` | - | CIO 'Molecular Dynamics and Materials Computing - Analyze Complexity' (CIO-MOLECULAR_DYNAMICS_MODELING-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MOTOR_CONTROL-EVALUATE_USABILITY` | - | CIO 'DC Motor and Servo Control - Evaluate Usability' (CIO-MOTOR_CONTROL-EVALUATE_USABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MULTI_AGENT_COOPERATION-ANALYZE_IMPLEMENTATION` | - | CIO 'Multi-Agent Cooperation Dynamics - Analyze Implementation' (CIO-MULTI_AGENT_COOPERATION-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MULTI_SENSOR_FUSION_ALGORITHMS-ANALYZE_COMPLEXITY` | - | CIO 'Multi-Sensor Fusion and State Estimation - Analyze Complexity' (CIO-MULTI_SENSOR_FUSION_ALGORITHMS-ANALYZE_COMPLEXITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MVVM_PATTERN-ANALYZE_IMPLEMENTATION` | - | CIO 'MVVM Architectural Pattern - Analyze Implementation' (CIO-MVVM_PATTERN-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NATURAL_LANGUAGE_PARSING-ANALYZE_IMPLEMENTATION` | - | CIO 'Natural Language Parsing and Machine Translation - Analyze Implementation' (CIO-NATURAL_LANGUAGE_PARSING-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NETIQUETTE-EVALUATE_COMPLIANCE` | - | CIO 'Netiquette (Online Etiquette) - Evaluate Compliance' (CIO-NETIQUETTE-EVALUATE_COMPLIANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NETWORK_TOPOLOGIES_CONCEPT-CONFIGURE_PROTOCOL` | - | CIO 'Network Topologies - Configure Protocol' (CIO-NETWORK_TOPOLOGIES_CONCEPT-CONFIGURE_PROTOCOL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NEURAL_NETWORKS_BASICS-EVALUATE_MODEL` | - | CIO 'Neural Networks Basics - Evaluate Model' (CIO-NEURAL_NETWORKS_BASICS-EVALUATE_MODEL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NEURAL_SIGNAL_DECODING_BCI-EVALUATE_MODEL` | - | CIO 'Neural Signal Decoding for Brain-Computer Interfaces - Evaluate Model' (CIO-NEURAL_SIGNAL_DECODING_BCI-EVALUATE_MODEL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-NEUROMORPHIC_COMPUTING_SPIKING_NEURONS-ANALYZE_IMPLEMENTATION` | - | CIO 'Neuromorphic Computing and Spiking Neurons - Analyze Implementation' (CIO-NEUROMORPHIC_COMPUTING_SPIKING_NEURONS-ANALYZE_IMPLEMENTATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ORBITAL_MECHANICS_SATELLITE_MESH-OPTIMIZE_VISUAL_QUALITY` | - | CIO 'Orbital Mechanics and Inter-Satellite Mesh Networks - Optimize Visual Quality' (CIO-ORBITAL_MECHANICS_SATELLITE_MESH-OPTIMIZE_VISUAL_QUALITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| ... | ... | ... | (+273 dòng nữa) |

### `LO_MISSING_ASSESSMENT_APPROACH` (139) — ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-UI_CONTROLS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_CONTROLS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_CONTROLS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTAINER_VIEWS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTAINER_VIEWS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STRUCTURE_TYPE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STRUCTURE_TYPE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_HIERARCHY-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_HIERARCHY-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DATA_TYPES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DATA_TYPES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DATA_TYPES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOOP_STRUCTURES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOOP_STRUCTURES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOOP_STRUCTURES-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTROL_FLOW-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTROL_FLOW-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTROL_FLOW-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAYS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAYS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAYS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SHAPE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SHAPE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SHAPE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-COLOR-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-COLOR-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ACCESSIBILITY-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ACCESSIBILITY-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ACCESSIBILITY-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ACCESSIBILITY-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OPERATORS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OPERATORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OPERATORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OPERATORS-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SENSITIVE_DATA-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SENSITIVE_DATA-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DESIGN_CYCLE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DESIGN_CYCLE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DESIGN_CYCLE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-NAMING_CONVENTIONS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-NAMING_CONVENTIONS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DEBUGGING-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DEBUGGING-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DEBUGGING-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_PROPERTIES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_PROPERTIES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_PROPERTIES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_ERRORS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_ERRORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_ERRORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RUNTIME_ERRORS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RUNTIME_ERRORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RUNTIME_ERRORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RUNTIME_ERRORS-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROPOSITIONAL_LOGIC-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-GRAPH_THEORY-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROPOSITIONAL_LOGIC-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-GRAPH_MODELS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PARAMETERIZED_QUANTUM_CIRCUITS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| ... | ... | ... | (+273 dòng nữa) |

### `CODE_FORMAT` (32) — Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-PYTHON-COLOR-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-COLOR-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-AGENT_MEMORY_SYSTEMS-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-AGENT_MEMORY_SYSTEMS-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-AUTONOMOUS_DRONE_NAVIGATION-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-AUTONOMOUS_DRONE_NAVIGATION-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-BOOLEAN_OPERATIONS_3D-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-BOOLEAN_OPERATIONS_3D-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-COLOR_THEORY-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-COLOR_THEORY-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-COMBINATORICS-COMPUTE_WITH_NUMPY/SYMPY` | - | Code 'SIO-PYTHON-COMBINATORICS-COMPUTE_WITH_NUMPY/SYMPY' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-COMPUTE_IN_MEMORY_ACCELERATION-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-COMPUTE_IN_MEMORY_ACCELERATION-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-CPU_ARCHITECTURE-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-CPU_ARCHITECTURE-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-INFORMATION_ENTROPY_METRICS-COMPUTE_WITH_NUMPY/SYMPY` | - | Code 'SIO-PYTHON-INFORMATION_ENTROPY_METRICS-COMPUTE_WITH_NUMPY/SYMPY' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-IO_METHODS_POLLING_INTERRUPT-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-IO_METHODS_POLLING_INTERRUPT-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-LIGHT_MOTION_SENSORS-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-LIGHT_MOTION_SENSORS-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-LOGIC_GATES-COMPUTE_WITH_NUMPY/SYMPY` | - | Code 'SIO-PYTHON-LOGIC_GATES-COMPUTE_WITH_NUMPY/SYMPY' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-MARITIME_UNDERWATER_ROBOTICS-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-MARITIME_UNDERWATER_ROBOTICS-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-MATERIAL_AND_TEXTURE-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-MATERIAL_AND_TEXTURE-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-MEMORY_TYPES-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-MEMORY_TYPES-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-MESH_EXTRUSION-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-MESH_EXTRUSION-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-ORBITAL_MECHANICS_SATELLITE_MESH-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-ORBITAL_MECHANICS_SATELLITE_MESH-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-POLYGON_MESH-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-POLYGON_MESH-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-PROBABILITY_BASICS-COMPUTE_WITH_NUMPY/SYMPY` | - | Code 'SIO-PYTHON-PROBABILITY_BASICS-COMPUTE_WITH_NUMPY/SYMPY' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-PROBLEM_DECOMPOSITION-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-PROBLEM_DECOMPOSITION-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-PROBLEM_DECOMPOSITION_CONCEPT-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-PROBLEM_DECOMPOSITION_CONCEPT-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-PWM-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-PWM-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-ROBOTIC_ACTUATION_CONTROL-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-ROBOTIC_ACTUATION_CONTROL-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-ROBOTIC_PATH_PLANNING-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-ROBOTIC_PATH_PLANNING-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-SET_THEORY-COMPUTE_WITH_NUMPY/SYMPY` | - | Code 'SIO-PYTHON-SET_THEORY-COMPUTE_WITH_NUMPY/SYMPY' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-SINGULAR_VALUE_DECOMPOSITION-RENDER_WITH_OPENGL/MODERNGL` | - | Code 'SIO-PYTHON-SINGULAR_VALUE_DECOMPOSITION-RENDER_WITH_OPENGL/MODERNGL' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-SPATIAL_AUDIO_AND_HAPTICS-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-SPATIAL_AUDIO_AND_HAPTICS-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-SWARM_ROBOTICS_FORMATION_CONTROL-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-SWARM_ROBOTICS_FORMATION_CONTROL-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-TEMP_HUMIDITY_SENSORS-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-TEMP_HUMIDITY_SENSORS-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-UAV_FLIGHT_DYNAMICS_AND_CONTROL-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-UAV_FLIGHT_DYNAMICS_AND_CONTROL-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-VIRTUAL_MEMORY-CONTROL_GPIO_WITH_RPI.GPIO` | - | Code 'SIO-PYTHON-VIRTUAL_MEMORY-CONTROL_GPIO_WITH_RPI.GPIO' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-PYTHON-WEARABLE_PHYSIOLOGICAL_MONITORING-COMPUTE_WITH_NUMPY/SYMPY` | - | Code 'SIO-PYTHON-WEARABLE_PHYSIOLOGICAL_MONITORING-COMPUTE_WITH_NUMPY/SYMPY' không khớp định dạng ^[A-Z0-9_-]+$. |
| ... | ... | ... | (+273 dòng nữa) |
