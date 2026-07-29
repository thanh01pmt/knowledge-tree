# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-29T15:12:32.373980+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 154 (61 lỗi, 93 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 10 |
| categories | 19 |
| topics | 30 |
| concepts | 44 |
| learning_objectives | 49 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 35 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 35 |
| `LO_PREREQ_BROKEN_PREREQ` | prerequisite_lo_code trong prerequisites không tồn tại | 31 |
| `LO_PREREQ_BROKEN_TARGET` | learning_objective_code trong prerequisites không tồn tại | 30 |
| `LO_MISSING_ASSESSMENT_APPROACH` | ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc) | 23 |

## ❌ Lỗi (ERROR) — cần sửa

### `LO_PREREQ_BROKEN_PREREQ` (31) — prerequisite_lo_code trong prerequisites không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objective_prerequisites | `CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION` | - | prerequisite_lo_code 'CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | - | prerequisite_lo_code 'CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-DEBUGGING-USE_STEP_INTO_AND` | - | prerequisite_lo_code 'CIO-DEBUGGING-USE_STEP_INTO_AND' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | - | prerequisite_lo_code 'CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | - | prerequisite_lo_code 'CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | - | prerequisite_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | - | prerequisite_lo_code 'CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | - | prerequisite_lo_code 'CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `SIO-SWIFT-IDENTIFY_WHILE_LOOP_STRUCTURE` | - | prerequisite_lo_code 'SIO-SWIFT-IDENTIFY_WHILE_LOOP_STRUCTURE' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `SIO-SWIFT-COMPARE_WHILE_AND_REPEAT_WHILE` | - | prerequisite_lo_code 'SIO-SWIFT-COMPARE_WHILE_AND_REPEAT_WHILE' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `SIO-SWIFT-PREVENT_INFINITE_LOOP_WHILE` | - | prerequisite_lo_code 'SIO-SWIFT-PREVENT_INFINITE_LOOP_WHILE' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_CONCEPT-01` | - | prerequisite_lo_code 'ULO-VIEW_CONCEPT-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_CONCEPT-01` | - | prerequisite_lo_code 'ULO-VIEW_CONCEPT-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_CONCEPT-01` | - | prerequisite_lo_code 'ULO-VIEW_CONCEPT-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_CONCEPT-01` | - | prerequisite_lo_code 'ULO-VIEW_CONCEPT-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_CONCEPT-01` | - | prerequisite_lo_code 'ULO-VIEW_CONCEPT-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_CONCEPT-01` | - | prerequisite_lo_code 'ULO-VIEW_CONCEPT-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-DECLARATIVE_UI_PARADIGM-01` | - | prerequisite_lo_code 'ULO-DECLARATIVE_UI_PARADIGM-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_HIERARCHY-02` | - | prerequisite_lo_code 'ULO-VIEW_HIERARCHY-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-DATA_TYPES-01` | - | prerequisite_lo_code 'ULO-DATA_TYPES-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-DATA_TYPES-01` | - | prerequisite_lo_code 'ULO-DATA_TYPES-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-DATA_TYPES-01` | - | prerequisite_lo_code 'ULO-DATA_TYPES-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-IMPERATIVE_PROGRAMMING-02` | - | prerequisite_lo_code 'ULO-IMPERATIVE_PROGRAMMING-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-CONTROL_FLOW-01` | - | prerequisite_lo_code 'ULO-CONTROL_FLOW-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-RUNTIME_ERRORS-02` | - | prerequisite_lo_code 'ULO-RUNTIME_ERRORS-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-SYNTAX_ERRORS-02` | - | prerequisite_lo_code 'ULO-SYNTAX_ERRORS-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-RUNTIME_ERRORS-02` | - | prerequisite_lo_code 'ULO-RUNTIME_ERRORS-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-ARRAYS-03` | - | prerequisite_lo_code 'ULO-ARRAYS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-STATE_PROPERTY_WRAPPER-01` | - | prerequisite_lo_code 'ULO-STATE_PROPERTY_WRAPPER-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-REFERENCE_TYPE_DECLARATION-03` | - | prerequisite_lo_code 'ULO-REFERENCE_TYPE_DECLARATION-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-LOOP_STRUCTURES-03` | - | prerequisite_lo_code 'ULO-LOOP_STRUCTURES-03' không tồn tại trong learning-objectives.tsv |

### `LO_PREREQ_BROKEN_TARGET` (30) — learning_objective_code trong prerequisites không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objective_prerequisites | `CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION` | - | learning_objective_code 'CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | - | learning_objective_code 'CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | - | learning_objective_code 'CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | - | learning_objective_code 'CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | - | learning_objective_code 'CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | - | learning_objective_code 'CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | - | learning_objective_code 'CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON` | - | learning_objective_code 'CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `SIO-SWIFT-WRITE_WHILE_LOOP_BASIC` | - | learning_objective_code 'SIO-SWIFT-WRITE_WHILE_LOOP_BASIC' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `SIO-SWIFT-IMPLEMENT_CONDITION_FIRST_WHILE` | - | learning_objective_code 'SIO-SWIFT-IMPLEMENT_CONDITION_FIRST_WHILE' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `SIO-SWIFT-ANALYZE_WHILE_LOOP_TERMINATION` | - | learning_objective_code 'SIO-SWIFT-ANALYZE_WHILE_LOOP_TERMINATION' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-DECLARATIVE_UI_PARADIGM-01` | - | learning_objective_code 'ULO-DECLARATIVE_UI_PARADIGM-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-ACCESSIBILITY-04` | - | learning_objective_code 'ULO-ACCESSIBILITY-04' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-CONTAINER_VIEWS-03` | - | learning_objective_code 'ULO-CONTAINER_VIEWS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VIEW_HIERARCHY-02` | - | learning_objective_code 'ULO-VIEW_HIERARCHY-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-UI_CONTROLS-03` | - | learning_objective_code 'ULO-UI_CONTROLS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-SHAPE-03` | - | learning_objective_code 'ULO-SHAPE-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-CONTAINER_VIEWS-03` | - | learning_objective_code 'ULO-CONTAINER_VIEWS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-CONTAINER_VIEWS-03` | - | learning_objective_code 'ULO-CONTAINER_VIEWS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-TYPE_SYSTEM-01` | - | learning_objective_code 'ULO-TYPE_SYSTEM-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-VARIABLES_AND_CONSTANTS-03` | - | learning_objective_code 'ULO-VARIABLES_AND_CONSTANTS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-OPERATORS-03` | - | learning_objective_code 'ULO-OPERATORS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-CONTROL_FLOW-01` | - | learning_objective_code 'ULO-CONTROL_FLOW-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-CONDITIONAL_STATEMENTS-03` | - | learning_objective_code 'ULO-CONDITIONAL_STATEMENTS-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | - | learning_objective_code 'ULO-SYNTAX_VS_RUNTIME_ERRORS-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | - | learning_objective_code 'ULO-SYNTAX_VS_RUNTIME_ERRORS-02' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-ARRAY_OPERATIONS-01` | - | learning_objective_code 'ULO-ARRAY_OPERATIONS-01' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-LOCAL_VIEW_STATE-03` | - | learning_objective_code 'ULO-LOCAL_VIEW_STATE-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-STRUCTURE_TYPE-03` | - | learning_objective_code 'ULO-STRUCTURE_TYPE-03' không tồn tại trong learning-objectives.tsv |
| learning_objective_prerequisites | `ULO-WHILE_LOOP-01` | - | learning_objective_code 'ULO-WHILE_LOOP-01' không tồn tại trong learning-objectives.tsv |

## ⚠️ Cảnh báo (WARNING)

### `LO_CONCEPT_UNCOVERED` (35) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `IF_ELSE_STATEMENT` | - | Concept 'If-Else Statement' (IF_ELSE_STATEMENT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | - | Concept 'Declaring Primitive Types' (PRIMITIVE_TYPE_DECLARATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DIGITAL_FOOTPRINT` | - | Concept 'Digital Footprint' (DIGITAL_FOOTPRINT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `VIEW_TRANSITIONS` | - | Concept 'View Transitions' (VIEW_TRANSITIONS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `RUNTIME_ERRORS` | - | Concept 'Runtime Errors' (RUNTIME_ERRORS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `WCAG_PRINCIPLES` | - | Concept 'WCAG Principles (POUR)' (WCAG_PRINCIPLES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `ALGORITHMIC_BIAS_SOCIETY` | - | Concept 'Algorithmic Bias in Society' (ALGORITHMIC_BIAS_SOCIETY) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `PHISHING_IDENTIFICATION` | - | Concept 'Identifying Phishing Attempts' (PHISHING_IDENTIFICATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `FOR_LOOP` | - | Concept 'For Loop' (FOR_LOOP) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `WIREFRAMING` | - | Concept 'Wireframing' (WIREFRAMING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `LOGIC_ERRORS` | - | Concept 'Logical Errors' (LOGIC_ERRORS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `MALWARE_TYPES_CONCEPT` | - | Concept 'Malware Types' (MALWARE_TYPES_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `IMPLICIT_EXPLICIT_ANIMATION` | - | Concept 'Implicit vs. Explicit Animation' (IMPLICIT_EXPLICIT_ANIMATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `UI_BOX_MODEL_LAYOUT` | - | Concept 'UI Box Model Layout System' (UI_BOX_MODEL_LAYOUT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `SWITCH_CASE` | - | Concept 'Switch-Case Statement' (SWITCH_CASE) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `SCREEN_READERS` | - | Concept 'Screen Readers' (SCREEN_READERS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `LOCAL_VIEW_STATE` | - | Concept 'Local View State' (LOCAL_VIEW_STATE) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `OBJECT_INSTANTIATION` | - | Concept 'Object Instantiation' (OBJECT_INSTANTIATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `CLASS_DEFINITION` | - | Concept 'Class Definition' (CLASS_DEFINITION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `REFERENCE_TYPE_DECLARATION` | - | Concept 'Declaring Reference Types' (REFERENCE_TYPE_DECLARATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `USER_CENTERED_DESIGN` | - | Concept 'User-Centered Design Process' (USER_CENTERED_DESIGN) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `AI_BIAS` | - | Concept 'Bias in AI' (AI_BIAS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `SYNTAX_ERRORS` | - | Concept 'Syntax Errors' (SYNTAX_ERRORS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `PASSWORD_STRENGTH_CONCEPT` | - | Concept 'Strong Passwords' (PASSWORD_STRENGTH_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `PROTOTYPING` | - | Concept 'Prototyping' (PROTOTYPING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `BREAKPOINTS` | - | Concept 'Using Breakpoints' (BREAKPOINTS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `OBJECT_PROPERTIES` | - | Concept 'Object Properties/Attributes' (OBJECT_PROPERTIES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `COMPOSITION_PRINCIPLES` | - | Concept 'Composition Principles' (COMPOSITION_PRINCIPLES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `EVENT_BASED_PROGRAMMING` | - | Concept 'Event-Based Programming Model' (EVENT_BASED_PROGRAMMING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `TWO_WAY_BINDING` | - | Concept 'Two-Way Data Binding' (TWO_WAY_BINDING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DIGITAL_IDENTITY` | - | Concept 'Digital Identity Management' (DIGITAL_IDENTITY) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `FLEXBOX_GRID_LAYOUT` | - | Concept 'Flexible & Grid Layout Systems' (FLEXBOX_GRID_LAYOUT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `CROSS_ORIGIN_SECURITY` | - | Concept 'Cross-Origin Security & Policies' (CROSS_ORIGIN_SECURITY) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `COLOR_THEORY` | - | Concept 'Color Theory' (COLOR_THEORY) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `FIRST_CLASS_FUNCTIONS_CONCEPT` | - | Concept 'First-Class & Higher-Order Functions' (FIRST_CLASS_FUNCTIONS_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |

### `ORPHAN_NODE` (35) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `AI_BIAS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ALGORITHMIC_BIAS_SOCIETY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `BREAKPOINTS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `CLASS_DEFINITION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `COLOR_THEORY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `COMPOSITION_PRINCIPLES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `CROSS_ORIGIN_SECURITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DIGITAL_FOOTPRINT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DIGITAL_IDENTITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `EVENT_BASED_PROGRAMMING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `FIRST_CLASS_FUNCTIONS_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `FLEXBOX_GRID_LAYOUT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `FOR_LOOP` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `IF_ELSE_STATEMENT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `IMPLICIT_EXPLICIT_ANIMATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LOCAL_VIEW_STATE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LOGIC_ERRORS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `MALWARE_TYPES_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_INSTANTIATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_PROPERTIES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PASSWORD_STRENGTH_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PHISHING_IDENTIFICATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PROTOTYPING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `REFERENCE_TYPE_DECLARATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `RUNTIME_ERRORS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SCREEN_READERS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SWITCH_CASE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SYNTAX_ERRORS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TWO_WAY_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `UI_BOX_MODEL_LAYOUT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `USER_CENTERED_DESIGN` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VIEW_TRANSITIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `WCAG_PRINCIPLES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `WIREFRAMING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_MISSING_ASSESSMENT_APPROACH` (23) — ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ARRAY_OPERATIONS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-WHILE_LOOP-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | assessment_approach | lo_type=UNIVERSAL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-01` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-02` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-03-01` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-WHILE_LOOP-03-02` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
| learning_objectives | `CIO-ERROR_MESSAGES_CONCEPT-02` | assessment_approach | lo_type=CONCEPTUAL_IMPL thiếu assessment_approach (Rule 7: Direct Assessment Coverage). |
