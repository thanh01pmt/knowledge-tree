# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-25T12:19:12.903267+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 128 (36 lỗi, 92 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 11 |
| topics | 15 |
| concepts | 36 |
| learning_objectives | 217 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `CODE_FORMAT` | Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$ | 54 |
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 36 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 26 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 11 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `EMPTY_PARENT_REF` (36) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `UI_CONTROLS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `VIEW_CONCEPT` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `VIEW_HIERARCHY` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `CONTAINER_VIEWS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `STRUCTURE_TYPE` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `VARIABLES_AND_CONSTANTS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `DATA_TYPES` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `LOOP_STRUCTURES` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `CONTROL_FLOW` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `CONDITIONAL_STATEMENTS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `FUNCTIONS_AND_PROCEDURES` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `ARRAYS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `TYPE_SYSTEM` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `IMPERATIVE_PROGRAMMING` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `SHAPE` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `COLOR` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `ACCESSIBILITY` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `VISUAL_DESIGN` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `OPERATORS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `SECURITY_CHALLENGES` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `SENSITIVE_DATA` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `DESIGN_CYCLE` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `NAMING_CONVENTIONS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `DEBUGGING` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `UI_MODIFIERS_CONCEPT` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `PROJECT_ASSETS_MANAGEMENT` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `OBJECT_INSTANTIATION` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `STATE_PROPERTY_WRAPPER` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `EVENT_HANDLERS_CONCEPT` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `OBJECT_PROPERTIES` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `DECLARATIVE_UI_PARADIGM` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `SYNTAX_ERRORS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `RUNTIME_ERRORS` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `ERROR_MESSAGES_CONCEPT` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |
| concepts | `RETURN_VALUES_AND_SCOPE` | topic_codes | Cột 'topic_codes' rỗng — node không có cha. |

## ⚠️ Cảnh báo (WARNING)

### `CODE_FORMAT` (54) — Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-define-function-parameters` | - | Code 'SIO-SWIFT-define-function-parameters' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-pass-arguments` | - | Code 'SIO-SWIFT-pass-arguments' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-assign-return-value` | - | Code 'SIO-SWIFT-assign-return-value' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-combine-return-values` | - | Code 'SIO-SWIFT-combine-return-values' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-build-comparison-expression` | - | Code 'SIO-SWIFT-build-comparison-expression' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-use-comparison-in-condition` | - | Code 'SIO-SWIFT-use-comparison-in-condition' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-use-parentheses-precedence` | - | Code 'SIO-SWIFT-use-parentheses-precedence' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-evaluate-parenthesized-expression` | - | Code 'SIO-SWIFT-evaluate-parenthesized-expression' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-combine-logical-operators` | - | Code 'SIO-SWIFT-combine-logical-operators' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-evaluate-logical-expression` | - | Code 'SIO-SWIFT-evaluate-logical-expression' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-define-struct-properties` | - | Code 'SIO-SWIFT-define-struct-properties' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-identify-property-types` | - | Code 'SIO-SWIFT-identify-property-types' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-insert-element-at-end` | - | Code 'SIO-SWIFT-insert-element-at-end' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-insert-element-at-index` | - | Code 'SIO-SWIFT-insert-element-at-index' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-remove-element-by-index` | - | Code 'SIO-SWIFT-remove-element-by-index' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-remove-element-by-condition` | - | Code 'SIO-SWIFT-remove-element-by-condition' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-for-loop-closed-range` | - | Code 'SIO-SWIFT-for-loop-closed-range' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-for-loop-stride` | - | Code 'SIO-SWIFT-for-loop-stride' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-state-management-comparison` | - | Code 'SIO-SWIFT-state-management-comparison' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-choose-state-paradigm` | - | Code 'SIO-SWIFT-choose-state-paradigm' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-static-ui-declaration` | - | Code 'SIO-SWIFT-static-ui-declaration' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-static-ui-composition` | - | Code 'SIO-SWIFT-static-ui-composition' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-reactive-ui-state` | - | Code 'SIO-SWIFT-reactive-ui-state' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-reactive-ui-binding` | - | Code 'SIO-SWIFT-reactive-ui-binding' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-arrange-children-autosizing` | - | Code 'SIO-SWIFT-arrange-children-autosizing' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-control-spacing-autosizing` | - | Code 'SIO-SWIFT-control-spacing-autosizing' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-nest-containers-adaptive` | - | Code 'SIO-SWIFT-nest-containers-adaptive' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-layout-priority-nesting` | - | Code 'SIO-SWIFT-layout-priority-nesting' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-analyze-rendering-order` | - | Code 'SIO-SWIFT-analyze-rendering-order' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-zstack-ordering` | - | Code 'SIO-SWIFT-zstack-ordering' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-hit-testing-explanation` | - | Code 'SIO-SWIFT-hit-testing-explanation' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-hit-testing-prediction` | - | Code 'SIO-SWIFT-hit-testing-prediction' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-attach-tap-gesture` | - | Code 'SIO-SWIFT-attach-tap-gesture' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-attach-slider-action` | - | Code 'SIO-SWIFT-attach-slider-action' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-textfield-state-binding` | - | Code 'SIO-SWIFT-textfield-state-binding' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-slider-state-update` | - | Code 'SIO-SWIFT-slider-state-update' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-set-multiple-controls-1` | - | Code 'SIO-SWIFT-set-multiple-controls-1' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-set-multiple-controls-2` | - | Code 'SIO-SWIFT-set-multiple-controls-2' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-reactive-state-binding-1` | - | Code 'SIO-SWIFT-reactive-state-binding-1' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-reactive-state-binding-2` | - | Code 'SIO-SWIFT-reactive-state-binding-2' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-syntax-error-analysis-1` | - | Code 'SIO-SWIFT-syntax-error-analysis-1' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-syntax-error-analysis-2` | - | Code 'SIO-SWIFT-syntax-error-analysis-2' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-runtime-error-diagnosis-1` | - | Code 'SIO-SWIFT-runtime-error-diagnosis-1' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-runtime-error-diagnosis-2` | - | Code 'SIO-SWIFT-runtime-error-diagnosis-2' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-error-message-structure-1` | - | Code 'SIO-SWIFT-error-message-structure-1' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-error-message-structure-2` | - | Code 'SIO-SWIFT-error-message-structure-2' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-error-cause-inference-1` | - | Code 'SIO-SWIFT-error-cause-inference-1' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-error-cause-inference-2` | - | Code 'SIO-SWIFT-error-cause-inference-2' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-combine-shapes-stack` | - | Code 'SIO-SWIFT-combine-shapes-stack' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-combine-shapes-overlay` | - | Code 'SIO-SWIFT-combine-shapes-overlay' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-analyze-hsl-components` | - | Code 'SIO-SWIFT-analyze-hsl-components' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-analyze-hsv-modifiers` | - | Code 'SIO-SWIFT-analyze-hsv-modifiers' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-explain-color-interaction-hsl` | - | Code 'SIO-SWIFT-explain-color-interaction-hsl' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `SIO-SWIFT-explain-color-interaction-comparison` | - | Code 'SIO-SWIFT-explain-color-interaction-comparison' không khớp định dạng ^[A-Z0-9_-]+$. |

### `ORPHAN_NODE` (26) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| topics | `ARRAYS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `CONDITIONAL_LOGIC` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `DATA_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `DEBUGGING_TECHNIQUES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `ERROR_MESSAGES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `FIRST_CLASS_FUNCTIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `IDE_NAVIGATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `ITERATION_LOOPS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `PRIMITIVE_TYPES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `PRIVACY_SETTINGS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `REFERENCE_TYPES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `STATE_MANAGEMENT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `UI_CONTROLS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `UI_MODIFIERS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `USER_RESEARCH` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `CONTROL_FLOW` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DATA_TYPES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DEBUGGING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `EVENT_HANDLERS_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_INSTANTIATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_PROPERTIES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `RETURN_VALUES_AND_SCOPE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SECURITY_CHALLENGES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TYPE_SYSTEM` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VIEW_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VISUAL_DESIGN` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_CONCEPT_UNCOVERED` (11) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `VIEW_CONCEPT` | - | Concept 'Khái Niệm View' (VIEW_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DATA_TYPES` | - | Concept 'Kiểu Dữ Liệu' (DATA_TYPES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `CONTROL_FLOW` | - | Concept 'Luồng Điều Khiển' (CONTROL_FLOW) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `TYPE_SYSTEM` | - | Concept 'Hệ Thống Kiểu' (TYPE_SYSTEM) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `VISUAL_DESIGN` | - | Concept 'Thiết Kế Trực Quan' (VISUAL_DESIGN) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `SECURITY_CHALLENGES` | - | Concept 'Thách Thức Bảo Mật' (SECURITY_CHALLENGES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DEBUGGING` | - | Concept 'Gỡ Lỗi' (DEBUGGING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `OBJECT_INSTANTIATION` | - | Concept 'Object Instantiation' (OBJECT_INSTANTIATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `EVENT_HANDLERS_CONCEPT` | - | Concept 'Events and Event Handling' (EVENT_HANDLERS_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `OBJECT_PROPERTIES` | - | Concept 'Object Properties/Attributes' (OBJECT_PROPERTIES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `RETURN_VALUES_AND_SCOPE` | - | Concept 'Return Values and Scope' (RETURN_VALUES_AND_SCOPE) không có LO nào trỏ đến trong learning-objectives.tsv. |

### `INCONSISTENT_LINE_ENDINGS` (1) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `concepts.tsv` | - | File dùng line-ending LF, khác đa số các file khác (CRLF). |
