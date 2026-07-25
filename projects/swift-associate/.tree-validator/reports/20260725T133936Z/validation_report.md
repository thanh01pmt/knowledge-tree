# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-25T13:39:36.099485+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 361 (300 lỗi, 61 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 12 |
| topics | 16 |
| concepts | 24 |
| learning_objectives | 274 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 132 |
| `LO_BROKEN_PARENT_REF` | parent_lo_code trỏ tới 1 LO không tồn tại | 132 |
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 55 |
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 18 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 18 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 4 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 2 |

## ❌ Lỗi (ERROR) — cần sửa

### `EMPTY_PARENT_REF` (132) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_UIKIT_VIEW_COMPONENTS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TAP_INTERACTION_FLOW_IN_SWIFTUI` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TEXT_INPUT_INTERACTION_FLOW_IN_SWIFTUI` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_SWIFTUI_STRUCT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_UIKIT_UIVIEW_SUBCLASS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_INTEGER_VALUES_TO_INT_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_STRING_VALUES_TO_STRING_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_MEMORY_SIZE_OF_INTEGER_TYPES` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_STORAGE_OF_FLOAT_AND_DOUBLE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_SEQUENCE_BRANCH_AND_LOOP_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_IF_ELSE_AND_SWITCH_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CHECK_EXHAUSTIVENESS_OF_SWITCH_CASES_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-VERIFY_LOOP_TERMINATION_CONDITION_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DETECT_INFINITE_LOOP_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DETECT_NON_EXHAUSTIVE_SWITCH_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_DATA_TYPES_BY_STORAGE_AND_RANGE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_COLLECTION_TYPES_BY_STORAGE_AND_RANGE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_STATIC_TYPING_IN_SWIFT_VIA_TYPE_ANNOTATION_AND_INFERENCE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_STATIC_VS_DYNAMIC_TYPING_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_THE_STEPS_OF_STATIC_TYPE_CHECKING_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_SWIFT_TYPE_INFERENCE_TO_DETERMINE_EXPRESSION_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_TYPE_INFERENCE_IN_FUNCTION_AND_CLOSURE_CONTEXT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-SUGGEST_WAYS_TO_FIX_TYPE_ERRORS_BASED_ON_SWIFT_ERROR_MESSAGES` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-SIMULATE_SWIFT_TYPE_FLOW_TO_DETECT_ERRORS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_SWIFT_TYPE_FLOW_IN_COMPLEX_PROGRAMS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_3` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_CONTRAST_IN_SWIFTUI_DESIGN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_SYMMETRIC_BALANCE_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_ASYMMETRIC_BALANCE_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_GOLDEN_RATIO_GRID` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CALCULATE_GOLDEN_RATIO_LAYOUT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-GROUP_RELATED_ELEMENTS_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_PADDING_AND_OVERLAY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_COLOR_PALETTES_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_WHITESPACE_IMPACT_ON` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_WHITESPACE_LEVELS_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_3` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_VISUAL_LAYOUT_WITH` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_DESIGN_PROXIMITY_USING` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_DESIGN_CONSISTENCY_USING` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_BY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_USING` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_SECURITY_CHALLENGE_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DETECT_KEYCHAIN_STORAGE_VULNERABILITIES` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SQL` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_PLAINTEXT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_SEVERITY_OF_SECURITY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SEVERITY_OF_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_5_WHYS_TECHNIQUE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_FISHBONE_DIAGRAM_TO` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CONSTRUCT_CAUSE_EFFECT_CHAIN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODEL_ATTACK_CHAIN_FOR` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_DEBUGGING_WORKFLOW_USING` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-SET_CONDITIONAL_BREAKPOINT_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_BREAKPOINT_ACTION_TO` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_PRINT_WITH_LEVEL_PREFIX` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_OS_LOG_WITH_LOG_LEVELS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_STEP_INTO_AND_STEP_OUT_IN_XCODE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_STEP_INTO_AND_STEP_OUT_IN_XCODE_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-INSERT_PRINT_AT_MIDPOINT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_ASSERT_OR_PRECONDITION_AT_MIDPOINT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_5_WHYS_ON_SWIFT_LOG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMBINE_CONDITIONAL_BREAKPOINT_WITH_5_WHYS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_HOW_INITIALIZER_PARAMETERS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_BETWEEN_LABELED_AND` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CALL_A_SWIFT_CLASS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-INITIALIZE_A_SWIFT_STRUCT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CREATE_A_SWIFT_OBJECT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_DEFAULT_PROPERTY_VALUES` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_DIRECT_INITIALIZATION_VIA` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_ADVANTAGES_OF_FACTORY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_HOW_DEPENDENCY_INJECTION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_CONSTRUCTOR_INJECTION_VS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IMPLEMENT_EVENT_DRIVEN_PATTERN_IN_SWIFT_USING_SWIFTUIS_ONTAPGESTURE_AND_ONCHANGE_MODIFIERS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IMPLEMENT_EVENT_DRIVEN_PATTERN_IN_SWIFT_USING_SWIFTUIS_ONTAPGESTURE_AND_ONCHANGE_MODIFIERS_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_EVENT_FLOW_FROM_USER_ACTION_TO_HANDLER_INVOCATION_IN_SWIFT_USING_UIAPPLICATION_AND_UIRESPONDER_CHAIN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-TRACE_EVENT_FLOW_IN_SWIFTUI_USING_THE_VIEW_HIERARCHY_AND_ONRECEIVE_MODIFIER` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-REGISTER_CALLBACK_TO_UIBUTTONS_TOUCHUPINSIDE_EVENT_IN_SWIFT_USING_ADDTARGET_ACTION_FOR` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-REGISTER_CALLBACK_TO_SWIFTUI_BUTTONS_ACTION_CLOSURE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_EVENT_PROPAGATION_IN_SWIFTUI_USING_ALLOWSHITTESTING_AND_CONTENTSHAPE_TO_CONTROL_TOUCH_DELIVERY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_EVENT_PROPAGATION_IN_SWIFTUI_USING_ALLOWSHITTESTING_AND_CONTENTSHAPE_TO_CONTROL_TOUCH_DELIVERY_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN_TOUCHUPINSIDE_ON_A_SINGLE_UIBUTTON_IN_SWIFT_USING_SEPARATE_IBACTION_METHODS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-HANDLE_MULTIPLE_EVENTS_TAP_LONGPRESS_ON_A_SINGLE_SWIFTUI_VIEW_USING_SIMULTANEOUSGESTURE_AND_HIGHPRIORITYGESTURE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_PROPERTY_AS_KEY_VALUE_PAIR_USING_SWIFT_SYNTAX` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_STORED_AND_COMPUTED_PROPERTIES_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_PROPERTY_OBSERVERS_TO_MANAGE_STATE_CHANGES_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_COMPUTED_PROPERTY_TO_PROVIDE_READ_ONLY_OR_DERIVED_STATE_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ACCESS_AND_UPDATE_STORED_PROPERTY_VIA_INSTANCE_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_SUBSCRIPT_TO_ACCESS_AND_UPDATE_KEY_VALUE_STATE_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DEFINE_CUSTOM_GETTER_AND_SETTER_FOR_COMPUTED_PROPERTY_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_ACCESS_CONTROL_TO_RESTRICT_PROPERTY_WRITE_ACCESS_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_RETURN_STATEMENT_SYNTAX_IN_SWIFT_FUNCTIONS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_RETURN_TYPES_IN_SWIFT_VOID_OPTIONAL_TUPLE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_LOCAL_AND_GLOBAL_VARIABLES_IN_SWIFT_BASED_ON_DECLARATION_POSITION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_VARIABLE_SCOPE_WITHIN_SWIFT_CODE_BLOCKS_USING_BRACES` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EXPLAIN_LOCAL_VARIABLE_SCOPE_AND_RETURN_VALUE_MECHANISM_IN_SWIFT_FUNCTIONS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-EXPLAIN_THE_FLOW_OF_RETURN_VALUE_FROM_A_SWIFT_FUNCTION_TO_THE_CALLER` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_VARIABLE_ACCESS_RULES_BASED_ON_SCOPE_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_VARIABLE_SHADOWING_IN_SWIFT_AND_ITS_EFFECT_ON_DATA_ACCESS` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WRITE_A_SWIFT_FUNCTION_WITH_MULTIPLE_RETURN_STATEMENTS_IN_CONDITIONAL_BRANCHES` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WRITE_A_SWIFT_FUNCTION_WITH_MULTIPLE_RETURN_STATEMENTS_IN_CONDITIONAL_BRANCHES_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESIGN_A_SWIFT_FUNCTION_WITH_SIDE_EFFECTS_ON_GLOBAL_STATE_AND_RETURN_VALUE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DESIGN_A_SWIFT_FUNCTION_WITH_SIDE_EFFECTS_ON_GLOBAL_STATE_AND_RETURN_VALUE_2` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-USE_RETURN_VALUE_AS_DIRECT_ARGUMENT_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ASSIGN_RETURN_VALUE_TO_CONSTANT_AND_USE_IN_SUBSEQUENT_EXPRESSION_IN_SWIFT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |

### `LO_BROKEN_PARENT_REF` (132) — parent_lo_code trỏ tới 1 LO không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_2` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_SWIFTUI_DESIGN_AGAINST_CONSISTENCY_PRINCIPLE_2` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE_2` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_SPECIFIC_CHECKLIST_TO_IDENTIFY_INSECURE_NETWORK_REQUESTS_IN_SWIFT_2` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SWIFT_DENIAL_OF_SERVICE_ON_AVAILABILITY_2` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | parent_lo_code | parent_lo_code 'CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_UIKIT_VIEW_COMPONENTS` | parent_lo_code | parent_lo_code 'CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TAP_INTERACTION_FLOW_IN_SWIFTUI` | parent_lo_code | parent_lo_code 'CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TEXT_INPUT_INTERACTION_FLOW_IN_SWIFTUI` | parent_lo_code | parent_lo_code 'CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW' không tồn tại. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_SWIFTUI_STRUCT` | parent_lo_code | parent_lo_code 'CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI' không tồn tại. |
| learning_objectives | `SIO-SWIFT-MODEL_VIEW_AS_UIKIT_UIVIEW_SUBCLASS` | parent_lo_code | parent_lo_code 'CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_INTEGER_VALUES_TO_INT_TYPE` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_STRING_VALUES_TO_STRING_TYPE` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_MEMORY_SIZE_OF_INTEGER_TYPES` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_STORAGE_OF_FLOAT_AND_DOUBLE` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CHOOSE_SWIFT_DATA_TYPE_BASED_ON_REQUIRED_OPERATIONS_2` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CONVERT_DATA_TYPES_USING_SWIFT_TYPE_CASTING_2` | parent_lo_code | parent_lo_code 'CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_SEQUENCE_BRANCH_AND_LOOP_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_IF_ELSE_AND_SWITCH_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_EXECUTION_ORDER_OF_SWITCH_IN_SWIFT_2` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_VARIABLE_VALUES_THROUGH_FOR_IN_LOOP_IN_SWIFT_2` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_EXECUTION_PATH_OF_SWITCH_IN_SWIFT_2` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CHECK_EXHAUSTIVENESS_OF_SWITCH_CASES_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH' không tồn tại. |
| learning_objectives | `SIO-SWIFT-VERIFY_LOOP_TERMINATION_CONDITION_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DETECT_INFINITE_LOOP_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DETECT_NON_EXHAUSTIVE_SWITCH_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_DATA_TYPES_BY_STORAGE_AND_RANGE` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SWIFT_COLLECTION_TYPES_BY_STORAGE_AND_RANGE` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_STATIC_TYPING_IN_SWIFT_VIA_TYPE_ANNOTATION_AND_INFERENCE` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_STATIC_VS_DYNAMIC_TYPING_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_THE_STEPS_OF_STATIC_TYPE_CHECKING_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_SWIFT_TYPE_INFERENCE_TO_DETERMINE_EXPRESSION_TYPE` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_SWIFT_TYPE_INFERENCE_IN_FUNCTION_AND_CLOSURE_CONTEXT` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_2` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2' không tồn tại. |
| learning_objectives | `SIO-SWIFT-SUGGEST_WAYS_TO_FIX_TYPE_ERRORS_BASED_ON_SWIFT_ERROR_MESSAGES` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2' không tồn tại. |
| learning_objectives | `SIO-SWIFT-SIMULATE_SWIFT_TYPE_FLOW_TO_DETECT_ERRORS` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_SWIFT_TYPE_FLOW_IN_COMPLEX_PROGRAMS` | parent_lo_code | parent_lo_code 'CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CONTRAST_IN_SWIFTUI_INTERFACE_3` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EVALUATE_CONTRAST_IN_SWIFTUI_DESIGN` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_SYMMETRIC_BALANCE_IN` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_ASYMMETRIC_BALANCE_IN` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_GOLDEN_RATIO_GRID` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CALCULATE_GOLDEN_RATIO_LAYOUT` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID' không tồn tại. |
| learning_objectives | `SIO-SWIFT-GROUP_RELATED_ELEMENTS_IN` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_PADDING_AND_OVERLAY` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_COLOR_PALETTES_IN` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EVALUATE_WHITESPACE_IMPACT_ON` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_WHITESPACE_LEVELS_IN` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_VISUAL_EVALUATION_CRITERIA_3` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_VISUAL_LAYOUT_WITH` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_DESIGN_PROXIMITY_USING` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EVALUATE_DESIGN_CONSISTENCY_USING` | parent_lo_code | parent_lo_code 'CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_BY` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_USING` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_SECURITY_CHALLENGE_TYPE` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DETECT_KEYCHAIN_STORAGE_VULNERABILITIES` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_SQL` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_IMPACT_OF_PLAINTEXT` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EVALUATE_SEVERITY_OF_SECURITY` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_SEVERITY_OF_SWIFT` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_5_WHYS_TECHNIQUE` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_FISHBONE_DIAGRAM_TO` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CONSTRUCT_CAUSE_EFFECT_CHAIN` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-MODEL_ATTACK_CHAIN_FOR` | parent_lo_code | parent_lo_code 'CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_DEBUGGING_WORKFLOW_USING` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-SET_CONDITIONAL_BREAKPOINT_IN` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_BREAKPOINT_ACTION_TO` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_PRINT_WITH_LEVEL_PREFIX` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-USE_PRINT_WITH_LEVEL' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_OS_LOG_WITH_LOG_LEVELS` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-USE_PRINT_WITH_LEVEL' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_STEP_INTO_AND_STEP_OUT_IN_XCODE` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-USE_STEP_INTO_AND' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_STEP_INTO_AND_STEP_OUT_IN_XCODE_2` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-USE_STEP_INTO_AND' không tồn tại. |
| learning_objectives | `SIO-SWIFT-INSERT_PRINT_AT_MIDPOINT` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_ASSERT_OR_PRECONDITION_AT_MIDPOINT` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_5_WHYS_ON_SWIFT_LOG` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-USE_5_WHYS_ON' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMBINE_CONDITIONAL_BREAKPOINT_WITH_5_WHYS` | parent_lo_code | parent_lo_code 'CIO-DEBUGGING-USE_5_WHYS_ON' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION_2` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_HOW_INITIALIZER_PARAMETERS` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_BETWEEN_LABELED_AND` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CALL_A_SWIFT_CLASS` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-INITIALIZE_A_SWIFT_STRUCT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-CREATE_A_SWIFT_OBJECT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_DEFAULT_PROPERTY_VALUES` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_DIRECT_INITIALIZATION_VIA` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_ADVANTAGES_OF_FACTORY` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_HOW_DEPENDENCY_INJECTION` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-COMPARE_CONSTRUCTOR_INJECTION_VS` | parent_lo_code | parent_lo_code 'CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IMPLEMENT_EVENT_DRIVEN_PATTERN_IN_SWIFT_USING_SWIFTUIS_ONTAPGESTURE_AND_ONCHANGE_MODIFIERS` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IMPLEMENT_EVENT_DRIVEN_PATTERN_IN_SWIFT_USING_SWIFTUIS_ONTAPGESTURE_AND_ONCHANGE_MODIFIERS_2` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_EVENT_FLOW_FROM_USER_ACTION_TO_HANDLER_INVOCATION_IN_SWIFT_USING_UIAPPLICATION_AND_UIRESPONDER_CHAIN` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM' không tồn tại. |
| learning_objectives | `SIO-SWIFT-TRACE_EVENT_FLOW_IN_SWIFTUI_USING_THE_VIEW_HIERARCHY_AND_ONRECEIVE_MODIFIER` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM' không tồn tại. |
| learning_objectives | `SIO-SWIFT-REGISTER_CALLBACK_TO_UIBUTTONS_TOUCHUPINSIDE_EVENT_IN_SWIFT_USING_ADDTARGET_ACTION_FOR` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-REGISTER_CALLBACK_TO_SWIFTUI_BUTTONS_ACTION_CLOSURE` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_EVENT_PROPAGATION_IN_SWIFTUI_USING_ALLOWSHITTESTING_AND_CONTENTSHAPE_TO_CONTROL_TOUCH_DELIVERY` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ANALYZE_EVENT_PROPAGATION_IN_SWIFTUI_USING_ALLOWSHITTESTING_AND_CONTENTSHAPE_TO_CONTROL_TOUCH_DELIVERY_2` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN_TOUCHUPINSIDE_ON_A_SINGLE_UIBUTTON_IN_SWIFT_USING_SEPARATE_IBACTION_METHODS` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-HANDLE_MULTIPLE_EVENTS_TAP_LONGPRESS_ON_A_SINGLE_SWIFTUI_VIEW_USING_SIMULTANEOUSGESTURE_AND_HIGHPRIORITYGESTURE` | parent_lo_code | parent_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_PROPERTY_AS_KEY_VALUE_PAIR_USING_SWIFT_SYNTAX` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_STORED_AND_COMPUTED_PROPERTIES_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY' không tồn tại. |
| learning_objectives | `SIO-SWIFT-APPLY_PROPERTY_OBSERVERS_TO_MANAGE_STATE_CHANGES_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_COMPUTED_PROPERTY_TO_PROVIDE_READ_ONLY_OR_DERIVED_STATE_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ACCESS_AND_UPDATE_STORED_PROPERTY_VIA_INSTANCE_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_SUBSCRIPT_TO_ACCESS_AND_UPDATE_KEY_VALUE_STATE_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DEFINE_CUSTOM_GETTER_AND_SETTER_FOR_COMPUTED_PROPERTY_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_ACCESS_CONTROL_TO_RESTRICT_PROPERTY_WRITE_ACCESS_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_RETURN_STATEMENT_SYNTAX_IN_SWIFT_FUNCTIONS` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_RETURN_TYPES_IN_SWIFT_VOID_OPTIONAL_TUPLE` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_LOCAL_AND_GLOBAL_VARIABLES_IN_SWIFT_BASED_ON_DECLARATION_POSITION` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL' không tồn tại. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_VARIABLE_SCOPE_WITHIN_SWIFT_CODE_BLOCKS_USING_BRACES` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EXPLAIN_LOCAL_VARIABLE_SCOPE_AND_RETURN_VALUE_MECHANISM_IN_SWIFT_FUNCTIONS` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-EXPLAIN_THE_FLOW_OF_RETURN_VALUE_FROM_A_SWIFT_FUNCTION_TO_THE_CALLER` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_VARIABLE_ACCESS_RULES_BASED_ON_SCOPE_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_VARIABLE_SHADOWING_IN_SWIFT_AND_ITS_EFFECT_ON_DATA_ACCESS` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES' không tồn tại. |
| learning_objectives | `SIO-SWIFT-WRITE_A_SWIFT_FUNCTION_WITH_MULTIPLE_RETURN_STATEMENTS_IN_CONDITIONAL_BRANCHES` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-WRITE_A_SWIFT_FUNCTION_WITH_MULTIPLE_RETURN_STATEMENTS_IN_CONDITIONAL_BRANCHES_2` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESIGN_A_SWIFT_FUNCTION_WITH_SIDE_EFFECTS_ON_GLOBAL_STATE_AND_RETURN_VALUE` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-DESIGN_A_SWIFT_FUNCTION_WITH_SIDE_EFFECTS_ON_GLOBAL_STATE_AND_RETURN_VALUE_2` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION' không tồn tại. |
| learning_objectives | `SIO-SWIFT-USE_RETURN_VALUE_AS_DIRECT_ARGUMENT_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS' không tồn tại. |
| learning_objectives | `SIO-SWIFT-ASSIGN_RETURN_VALUE_TO_CONSTANT_AND_USE_IN_SUBSEQUENT_EXPRESSION_IN_SWIFT` | parent_lo_code | parent_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS' không tồn tại. |

### `BROKEN_REFERENCE` (18) — Tham chiếu tới code không tồn tại ở bảng cha

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
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | concept_codes | 'CONTAINER_VIEWS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | concept_codes | 'VIEW_HIERARCHY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_CONTROLS-03` | concept_codes | 'UI_CONTROLS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | concept_codes | 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SHAPE-03` | concept_codes | 'SHAPE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COLOR-02` | concept_codes | 'COLOR' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (18) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

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
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | concept_codes | concept_code 'CONTAINER_VIEWS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | concept_codes | concept_code 'VIEW_HIERARCHY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_CONTROLS-03` | concept_codes | concept_code 'UI_CONTROLS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | concept_codes | concept_code 'LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SHAPE-03` | concept_codes | concept_code 'SHAPE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-COLOR-02` | concept_codes | concept_code 'COLOR' không tồn tại trong concepts.tsv của project. |

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (55) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT` | - | CIO 'Truy cập phần tử mảng bằng chỉ số' (CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ZERO_BASED_INDEX` | - | CIO 'Hiểu chỉ số bắt đầu từ 0' (CIO-ARRAY_OPERATIONS-ZERO_BASED_INDEX) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-SEQUENTIAL_ARRAY_TRAVERSAL` | - | CIO 'Duyệt mảng tuần tự' (CIO-ARRAY_OPERATIONS-SEQUENTIAL_ARRAY_TRAVERSAL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-MODIFY_ARRAY_ELEMENT` | - | CIO 'Sửa đổi phần tử mảng' (CIO-ARRAY_OPERATIONS-MODIFY_ARRAY_ELEMENT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE` | - | CIO 'Vai trò của trạng thái cục bộ trong đồng bộ giao diện' (CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-CONTROL_UI_PROPERTIES` | - | CIO 'Điều khiển thuộc tính giao diện bằng trạng thái cục bộ' (CIO-LOCAL_VIEW_STATE-CONTROL_UI_PROPERTIES) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-UPDATE_LOCAL_STATE` | - | CIO 'Cập nhật trạng thái cục bộ từ tương tác người dùng' (CIO-LOCAL_VIEW_STATE-UPDATE_LOCAL_STATE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-TRACE_LOCAL_STATE_LIFECYCLE` | - | CIO 'Trace local state lifecycle' (CIO-LOCAL_VIEW_STATE-TRACE_LOCAL_STATE_LIFECYCLE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-DETERMINE_LOCAL_STATE_SCOPE` | - | CIO 'Determine local state scope' (CIO-LOCAL_VIEW_STATE-DETERMINE_LOCAL_STATE_SCOPE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER` | - | CIO 'Explain state-triggered re-rendering' (CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING` | - | CIO 'Describe state wrapper decoupling role' (CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-INITIALIZE_UPDATE_MUTABLE_STATE` | - | CIO 'Initialize and update mutable state' (CIO-STATE_PROPERTY_WRAPPER-INITIALIZE_UPDATE_MUTABLE_STATE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT` | - | CIO 'Bind state to UI element and observe changes' (CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS` | - | CIO 'Compare ownership and sharing semantics of state wrappers' (CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER` | - | CIO 'Evaluate appropriate wrapper based on data source and view hierarchy' (CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP` | - | CIO 'Recognize condition-controlled loop pattern' (CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION` | - | CIO 'Condition-first repetition pattern' (CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION` | - | CIO 'Loop termination via condition falsification' (CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-DYNAMIC_CONDITION_REPETITION` | - | CIO 'Dynamic condition repetition with mutable control variable' (CIO-WHILE_LOOP-DYNAMIC_CONDITION_REPETITION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-SENTINEL_CONTROLLED_REPETITION` | - | CIO 'Sentinel-controlled repetition pattern' (CIO-WHILE_LOOP-SENTINEL_CONTROLLED_REPETITION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION` | - | CIO 'Asset type categorization pattern' (CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_CATALOG_HIERARCHICAL` | - | CIO 'Asset catalog hierarchical organization pattern' (CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_CATALOG_HIERARCHICAL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_ADDITION_REFERENCE` | - | CIO 'Asset addition and reference pattern' (CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_ADDITION_REFERENCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-COLOR_ASSET_DEFINITION` | - | CIO 'Color asset definition and usage pattern' (CIO-PROJECT_ASSETS_MANAGEMENT-COLOR_ASSET_DEFINITION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME` | - | CIO 'Phân biệt lỗi cú pháp và lỗi runtime dựa trên định nghĩa' (CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-SYNTAX_RUNTIME_CAUSES` | - | CIO 'Giải thích nguyên nhân gây ra lỗi cú pháp và lỗi runtime' (CIO-SYNTAX_VS_RUNTIME_ERRORS-SYNTAX_RUNTIME_CAUSES) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-CLASSIFY_ERROR_DETECTION` | - | CIO 'Phân loại ví dụ lỗi dựa trên thời điểm phát hiện' (CIO-SYNTAX_VS_RUNTIME_ERRORS-CLASSIFY_ERROR_DETECTION) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-IDENTIFY_ERROR_TYPE` | - | CIO 'Xác định loại lỗi từ mã nguồn dựa trên dấu hiệu nhận biết' (CIO-SYNTAX_VS_RUNTIME_ERRORS-IDENTIFY_ERROR_TYPE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-ANALYZE_ERROR_MESSAGES` | - | CIO 'Phân tích thông báo lỗi để phân loại lỗi' (CIO-SYNTAX_VS_RUNTIME_ERRORS-ANALYZE_ERROR_MESSAGES) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX` | - | CIO 'Nhận diện cú pháp khai báo kiểu tham chiếu' (CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-COMPARE_REFERENCE_VALUE` | - | CIO 'So sánh hành vi gán và sao chép giữa kiểu tham chiếu và kiểu giá trị' (CIO-REFERENCE_TYPE_DECLARATION-COMPARE_REFERENCE_VALUE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-ANALYZE_REFERENCE_IMPACT` | - | CIO 'Phân tích tác động của tham chiếu đến bộ nhớ và hiệu năng' (CIO-REFERENCE_TYPE_DECLARATION-ANALYZE_REFERENCE_IMPACT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL` | - | CIO 'Khai báo biến tham chiếu với khởi tạo đối tượng' (CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL_2` | - | CIO 'Khai báo biến tham chiếu với giá trị null hoặc nil' (CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL_2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | - | CIO 'Phân biệt dựa trên cơ chế kích hoạt' (CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | - | CIO 'Phân biệt dựa trên mức độ kiểm soát thời gian và chi tiết' (CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | - | CIO 'Áp dụng implicit animation bằng cách gắn bộ mô tả animation vào view' (CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | - | CIO 'Áp dụng implicit animation bằng cách bao bọc thay đổi trạng thái trong ngữ cảnh animation' (CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | - | CIO 'Phân tích ưu nhược điểm dựa trên mức độ kiểm soát và độ phức tạp' (CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | - | CIO 'Phân tích ưu nhược điểm dựa trên hiệu suất và khả năng tái sử dụng' (CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | - | CIO 'Đánh giá lựa chọn dựa trên yêu cầu về hiệu suất và độ phức tạp' (CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | - | CIO 'Đánh giá lựa chọn dựa trên khả năng tùy chỉnh và trải nghiệm người dùng' (CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE` | - | CIO 'Mô tả trạng thái mong muốn' (CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE` | - | CIO 'So sánh luồng điều khiển khai báo và mệnh lệnh' (CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW` | - | CIO 'Xây dựng cấu trúc view phân cấp' (CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ATTACH_STATE_VIEW` | - | CIO 'Gắn trạng thái vào view' (CIO-DECLARATIVE_UI_PARADIGM-ATTACH_STATE_VIEW) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY` | - | CIO 'Phân tích quản lý trạng thái' (CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2` | - | CIO 'Phân tích khả năng tái sử dụng và bảo trì' (CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE` | - | CIO 'Đánh giá hiệu suất' (CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY` | - | CIO 'Đánh giá khả năng mở rộng' (CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | - | CIO 'Liệt kê và phân loại UI Modifier' (CIO-UI_MODIFIERS-LIST_AND_CLASSIFY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | - | CIO 'Thứ tự áp dụng modifier ảnh hưởng đến kết quả hiển thị' (CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | - | CIO 'Kết hợp các modifier để tạo hiệu ứng tổng hợp' (CIO-UI_MODIFIERS-COMBINE_MODIFIERS) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | - | CIO 'Lựa chọn modifier dựa trên yêu cầu bố cục' (CIO-UI_MODIFIERS-SELECT_BY_LAYOUT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | - | CIO 'Sắp xếp thứ tự modifier để đạt hiệu quả mong muốn' (CIO-UI_MODIFIERS-ORDER_FOR_EFFECT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |

### `ORPHAN_NODE` (4) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| topics | `DATA_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `FIRST_CLASS_FUNCTIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `PRIVACY_SETTINGS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `USER_RESEARCH` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `INCONSISTENT_LINE_ENDINGS` (2) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `fields.tsv` | - | File dùng line-ending CRLF, khác đa số các file khác (LF). |
| _file | `subjects.tsv` | - | File dùng line-ending CRLF, khác đa số các file khác (LF). |
