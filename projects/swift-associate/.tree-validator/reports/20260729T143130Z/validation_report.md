# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-29T14:31:30.305315+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 807 (588 lỗi, 219 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 10 |
| topics | 13 |
| concepts | 15 |
| learning_objectives | 445 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 294 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 294 |
| `LO_MISSING_ASSESSMENT_APPROACH` | ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc) | 203 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 7 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 7 |
| `LO_UNUSUAL_BLOOM_KD_COMBO` | Kết hợp Bloom Level + Knowledge Dimension ít phổ biến sư phạm | 1 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (294) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-DESIGN_CYCLE-01` | concept_codes | 'DESIGN_CYCLE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | concept_codes | 'SENSITIVE_DATA' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ACCESSIBILITY-04` | concept_codes | 'ACCESSIBILITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | concept_codes | 'IMPERATIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | concept_codes | 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OPERATORS-03` | concept_codes | 'OPERATORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | concept_codes | 'STRUCTURE_TYPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ARRAYS-03` | concept_codes | 'ARRAYS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | concept_codes | 'LOOP_STRUCTURES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | concept_codes | 'CONDITIONAL_STATEMENTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | concept_codes | 'VARIABLES_AND_CONSTANTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | concept_codes | 'NAMING_CONVENTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_CONTROLS-03` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SYNTAX_ERRORS-02` | concept_codes | 'SYNTAX_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RUNTIME_ERRORS-02` | concept_codes | 'RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | concept_codes | 'ERROR_MESSAGES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SHAPE-03` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COLOR-02` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA_TYPES-01` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA_TYPES-02` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DATA_TYPES-03` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL_FLOW-01` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL_FLOW-02` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONTROL_FLOW-03` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING-01` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING-02` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DEBUGGING-03` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-01` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-02` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-03` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-01` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-03` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-01` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-02` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-03` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | concept_codes | 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-USE_STEP_INTO_AND` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEBUGGING-USE_5_WHYS_ON` | concept_codes | 'DEBUGGING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | concept_codes | 'OBJECT_INSTANTIATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | concept_codes | 'OBJECT_PROPERTIES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | concept_codes | 'RETURN_VALUES_AND_SCOPE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_2` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE_2` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE_2` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT_2` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY_2` | concept_codes | 'SECURITY_CHALLENGES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_UIKIT_VIEW_COMPONENTS` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TAP_INTERACTION_FLOW_IN_SWIFTUI` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TEXT_INPUT_INTERACTION_FLOW_IN_SWIFTUI` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_SWIFTUI_STRUCT` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_UIKIT_UIVIEW_SUBCLASS` | concept_codes | 'VIEW_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_INTEGER_VALUES_TO_INT_TYPE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_STRING_VALUES_TO_STRING_TYPE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_MEMORY_SIZE_OF_INTEGER_TYPES` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_STORAGE_OF_FLOAT_AND_DOUBLE` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS_2` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING_2` | concept_codes | 'DATA_TYPES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_SEQUENCE_BRANCH_AND_LOOP_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_IF_ELSE_AND_SWITCH_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT_2` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT_2` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT_2` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CHECK_EXHAUSTIVENESS_OF_SWITCH_CASES_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-VERIFY_LOOP_TERMINATION_CONDITION_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DETECT_INFINITE_LOOP_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DETECT_NON_EXHAUSTIVE_SWITCH_IN_SWIFT` | concept_codes | 'CONTROL_FLOW' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_DATA_TYPES_BY_STORAGE_AND_RANGE` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_COLLECTION_TYPES_BY_STORAGE_AND_RANGE` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_STATIC_TYPING_IN_SWIFT_VIA_TYPE_ANNOTATION_AND_INFERENCE` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_STATIC_VS_DYNAMIC_TYPING_IN_SWIFT` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_THE_STEPS_OF_STATIC_TYPE_CHECKING_IN_SWIFT` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_SWIFT_TYPE_INFERENCE_TO_DETERMINE_EXPRESSION_TYPE` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_TYPE_INFERENCE_IN_FUNCTION_AND_CLOSURE_CONTEXT` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_2` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SUGGEST_WAYS_TO_FIX_TYPE_ERRORS_BASED_ON_SWIFT_ERROR_MESSAGES` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SIMULATE_SWIFT_TYPE_FLOW_TO_DETECT_ERRORS` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE_SWIFT_TYPE_FLOW_IN_COMPLEX_PROGRAMS` | concept_codes | 'TYPE_SYSTEM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_3` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_CONTRAST_IN_SWIFTUI_DESIGN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_SYMMETRIC_BALANCE_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_ASYMMETRIC_BALANCE_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-USE_GOLDEN_RATIO_GRID` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CALCULATE_GOLDEN_RATIO_LAYOUT` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-GROUP_RELATED_ELEMENTS_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-USE_PADDING_AND_OVERLAY` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_COLOR_PALETTES_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_WHITESPACE_IMPACT_ON` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_WHITESPACE_LEVELS_IN` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_3` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_VISUAL_LAYOUT_WITH` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_DESIGN_PROXIMITY_USING` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_DESIGN_CONSISTENCY_USING` | concept_codes | 'VISUAL_DESIGN' không tồn tại trong bảng cha. |
| ... | ... | ... | (+388 dòng nữa) |

### `LO_CONCEPT_NOT_IN_PROJECT` (294) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-DESIGN_CYCLE-01` | concept_codes | concept_code 'DESIGN_CYCLE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | concept_codes | concept_code 'SENSITIVE_DATA' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ACCESSIBILITY-04` | concept_codes | concept_code 'ACCESSIBILITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | concept_codes | concept_code 'IMPERATIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | concept_codes | concept_code 'FUNCTIONS_AND_PROCEDURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OPERATORS-03` | concept_codes | concept_code 'OPERATORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | concept_codes | concept_code 'STRUCTURE_TYPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ARRAYS-03` | concept_codes | concept_code 'ARRAYS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | concept_codes | concept_code 'LOOP_STRUCTURES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | concept_codes | concept_code 'CONDITIONAL_STATEMENTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | concept_codes | concept_code 'VARIABLES_AND_CONSTANTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | concept_codes | concept_code 'NAMING_CONVENTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_CONTROLS-03` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SYNTAX_ERRORS-02` | concept_codes | concept_code 'SYNTAX_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RUNTIME_ERRORS-02` | concept_codes | concept_code 'RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | concept_codes | concept_code 'ERROR_MESSAGES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SHAPE-03` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-COLOR-02` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DATA_TYPES-01` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DATA_TYPES-02` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DATA_TYPES-03` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTROL_FLOW-01` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTROL_FLOW-02` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONTROL_FLOW-03` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DEBUGGING-01` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DEBUGGING-02` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DEBUGGING-03` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-01` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-02` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-03` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-01` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-03` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-01` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-02` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-03` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | concept_codes | concept_code 'IMPLICIT_EXPLICIT_ANIMATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-USE_STEP_INTO_AND` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEBUGGING-USE_5_WHYS_ON` | concept_codes | concept_code 'DEBUGGING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | concept_codes | concept_code 'OBJECT_INSTANTIATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | concept_codes | concept_code 'OBJECT_PROPERTIES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | concept_codes | concept_code 'RETURN_VALUES_AND_SCOPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_2` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE_2` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE_2` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT_2` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY_2` | concept_codes | concept_code 'SECURITY_CHALLENGES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_UIKIT_VIEW_COMPONENTS` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TAP_INTERACTION_FLOW_IN_SWIFTUI` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TEXT_INPUT_INTERACTION_FLOW_IN_SWIFTUI` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_SWIFTUI_STRUCT` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_UIKIT_UIVIEW_SUBCLASS` | concept_codes | concept_code 'VIEW_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_INTEGER_VALUES_TO_INT_TYPE` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_STRING_VALUES_TO_STRING_TYPE` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_MEMORY_SIZE_OF_INTEGER_TYPES` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_STORAGE_OF_FLOAT_AND_DOUBLE` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS_2` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING_2` | concept_codes | concept_code 'DATA_TYPES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_SEQUENCE_BRANCH_AND_LOOP_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_IF_ELSE_AND_SWITCH_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT_2` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT_2` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT_2` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CHECK_EXHAUSTIVENESS_OF_SWITCH_CASES_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-VERIFY_LOOP_TERMINATION_CONDITION_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DETECT_INFINITE_LOOP_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DETECT_NON_EXHAUSTIVE_SWITCH_IN_SWIFT` | concept_codes | concept_code 'CONTROL_FLOW' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_DATA_TYPES_BY_STORAGE_AND_RANGE` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_COLLECTION_TYPES_BY_STORAGE_AND_RANGE` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_STATIC_TYPING_IN_SWIFT_VIA_TYPE_ANNOTATION_AND_INFERENCE` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_STATIC_VS_DYNAMIC_TYPING_IN_SWIFT` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_THE_STEPS_OF_STATIC_TYPE_CHECKING_IN_SWIFT` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_SWIFT_TYPE_INFERENCE_TO_DETERMINE_EXPRESSION_TYPE` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_TYPE_INFERENCE_IN_FUNCTION_AND_CLOSURE_CONTEXT` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_2` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SUGGEST_WAYS_TO_FIX_TYPE_ERRORS_BASED_ON_SWIFT_ERROR_MESSAGES` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SIMULATE_SWIFT_TYPE_FLOW_TO_DETECT_ERRORS` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE_SWIFT_TYPE_FLOW_IN_COMPLEX_PROGRAMS` | concept_codes | concept_code 'TYPE_SYSTEM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_3` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EVALUATE_CONTRAST_IN_SWIFTUI_DESIGN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_SYMMETRIC_BALANCE_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_ASYMMETRIC_BALANCE_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-USE_GOLDEN_RATIO_GRID` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CALCULATE_GOLDEN_RATIO_LAYOUT` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-GROUP_RELATED_ELEMENTS_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-USE_PADDING_AND_OVERLAY` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_COLOR_PALETTES_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EVALUATE_WHITESPACE_IMPACT_ON` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_WHITESPACE_LEVELS_IN` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_3` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_VISUAL_LAYOUT_WITH` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_DESIGN_PROXIMITY_USING` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EVALUATE_DESIGN_CONSISTENCY_USING` | concept_codes | concept_code 'VISUAL_DESIGN' không tồn tại trong concepts.tsv của project. |
| ... | ... | ... | (+388 dòng nữa) |

## ⚠️ Cảnh báo (WARNING)

### `LO_MISSING_ASSESSMENT_APPROACH` (203) — ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-DESIGN_CYCLE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ACCESSIBILITY-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OPERATORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAYS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_CONTROLS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_ERRORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RUNTIME_ERRORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SHAPE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-COLOR-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DATA_TYPES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DATA_TYPES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DATA_TYPES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTROL_FLOW-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTROL_FLOW-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-CONTROL_FLOW-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DEBUGGING-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DEBUGGING-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DEBUGGING-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_PROPERTIES-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_PROPERTIES-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-OBJECT_PROPERTIES-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-04` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ZERO_BASED_INDEX` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-SEQUENTIAL_ARRAY_TRAVERSAL` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-MODIFY_ARRAY_ELEMENT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-CONTROL_UI_PROPERTIES` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-UPDATE_LOCAL_STATE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-TRACE_LOCAL_STATE_LIFECYCLE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-DETERMINE_LOCAL_STATE_SCOPE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-INITIALIZE_UPDATE_MUTABLE_STATE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-DYNAMIC_CONDITION_REPETITION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-SENTINEL_CONTROLLED_REPETITION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_CATALOG_HIERARCHICAL` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_ADDITION_REFERENCE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-COLOR_ASSET_DEFINITION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-SYNTAX_RUNTIME_CAUSES` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-CLASSIFY_ERROR_DETECTION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-IDENTIFY_ERROR_TYPE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-ANALYZE_ERROR_MESSAGES` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-COMPARE_REFERENCE_VALUE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-ANALYZE_REFERENCE_IMPACT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ATTACH_STATE_VIEW` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DEBUGGING-USE_STEP_INTO_AND` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DEBUGGING-USE_5_WHYS_ON` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| ... | ... | ... | (+19 dòng nữa) |

### `LO_CONCEPT_UNCOVERED` (7) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `SWITCH_CASE` | - | Concept 'Switch-Case Statement' (SWITCH_CASE) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DIGITAL_IDENTITY` | - | Concept 'Digital Identity Management' (DIGITAL_IDENTITY) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `FOR_LOOP` | - | Concept 'For Loop' (FOR_LOOP) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `USER_CENTERED_DESIGN` | - | Concept 'User-Centered Design Process' (USER_CENTERED_DESIGN) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `IF_ELSE_STATEMENT` | - | Concept 'If-Else Statement' (IF_ELSE_STATEMENT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | - | Concept 'Declaring Primitive Types' (PRIMITIVE_TYPE_DECLARATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `TWO_WAY_BINDING` | - | Concept 'Two-Way Data Binding' (TWO_WAY_BINDING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| ... | ... | ... | (+19 dòng nữa) |

### `ORPHAN_NODE` (7) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `DIGITAL_IDENTITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `FOR_LOOP` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `IF_ELSE_STATEMENT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SWITCH_CASE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TWO_WAY_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `USER_CENTERED_DESIGN` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| ... | ... | ... | (+19 dòng nữa) |

### `LO_UNUSUAL_BLOOM_KD_COMBO` (1) — Kết hợp Bloom Level + Knowledge Dimension ít phổ biến sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-IDENTIFY_WHILE_LOOP_STRUCTURE` | bloom_level,knowledge_dimension | Kết hợp bloom_level=REMEMBER + knowledge_dimension=PROCEDURAL ít phổ biến sư phạm (Anderson & Krathwohl). |
| ... | ... | ... | (+19 dòng nữa) |

### `INCONSISTENT_LINE_ENDINGS` (1) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `learning-objectives.tsv` | - | File dùng line-ending LF, khác đa số các file khác (CRLF). |
| ... | ... | ... | (+19 dòng nữa) |
