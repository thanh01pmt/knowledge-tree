# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-01T13:38:41.636260+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 93 (0 lỗi, 93 cảnh báo)

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
| `LO_MISSING_ASSESSMENT_APPROACH` | ULO/CIO thiếu assessment_approach (Rule 7: đánh giá trực tiếp bắt buộc) | 23 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

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
