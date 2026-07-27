# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-27T13:07:47.266346+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 891 (0 lỗi, 891 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 12 |
| topics | 16 |
| concepts | 42 |
| learning_objectives | 445 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `LO_INVALID_KNOWLEDGE_DIMENSION` | knowledge_dimension không thuộc tập giá trị cho phép | 445 |
| `LO_INVALID_BLOOM_LEVEL` | bloom_level không thuộc tập giá trị cho phép | 445 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `LO_INVALID_KNOWLEDGE_DIMENSION` (445) — knowledge_dimension không thuộc tập giá trị cho phép

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-DESIGN_CYCLE-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-ACCESSIBILITY-04` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OPERATORS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-ARRAYS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-UI_CONTROLS-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SYNTAX_ERRORS-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-RUNTIME_ERRORS-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SHAPE-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-COLOR-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DATA_TYPES-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DATA_TYPES-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DATA_TYPES-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-CONTROL_FLOW-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-CONTROL_FLOW-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-CONTROL_FLOW-03` | knowledge_dimension | knowledge_dimension='Metacognitive' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DEBUGGING-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DEBUGGING-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DEBUGGING-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-WHILE_LOOP-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-WHILE_LOOP-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-ARRAY_OPERATIONS-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-ARRAY_OPERATIONS-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-ARRAY_OPERATIONS-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-01` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-04` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-WHILE_LOOP-02` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ZERO_BASED_INDEX` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-SEQUENTIAL_ARRAY_TRAVERSAL` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-MODIFY_ARRAY_ELEMENT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-CONTROL_UI_PROPERTIES` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-UPDATE_LOCAL_STATE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-TRACE_LOCAL_STATE_LIFECYCLE` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-DETERMINE_LOCAL_STATE_SCOPE` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-INITIALIZE_UPDATE_MUTABLE_STATE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-WHILE_LOOP-DYNAMIC_CONDITION_REPETITION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-WHILE_LOOP-SENTINEL_CONTROLLED_REPETITION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_CATALOG_HIERARCHICAL` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_ADDITION_REFERENCE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-COLOR_ASSET_DEFINITION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-SYNTAX_RUNTIME_CAUSES` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-CLASSIFY_ERROR_DETECTION` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-IDENTIFY_ERROR_TYPE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-ANALYZE_ERROR_MESSAGES` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-COMPARE_REFERENCE_VALUE` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-ANALYZE_REFERENCE_IMPACT` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL_2` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | knowledge_dimension | knowledge_dimension='Metacognitive' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | knowledge_dimension | knowledge_dimension='Metacognitive' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ATTACH_STATE_VIEW` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE` | knowledge_dimension | knowledge_dimension='Metacognitive' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY` | knowledge_dimension | knowledge_dimension='Metacognitive' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | knowledge_dimension | knowledge_dimension='Factual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | knowledge_dimension | knowledge_dimension='Conceptual' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DEBUGGING-USE_STEP_INTO_AND` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-DEBUGGING-USE_5_WHYS_ON` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | knowledge_dimension | knowledge_dimension='Procedural' không thuộc ['', 'CONCEPTUAL', 'FACTUAL', 'METACOGNITIVE', 'NULL', 'PROCEDURAL']. |
| ... | ... | ... | (+245 dòng nữa) |

### `LO_INVALID_BLOOM_LEVEL` (445) — bloom_level không thuộc tập giá trị cho phép

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-DESIGN_CYCLE-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SENSITIVE_DATA-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-ACCESSIBILITY-04` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-IMPERATIVE_PROGRAMMING-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-FUNCTIONS_AND_PROCEDURES-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OPERATORS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-STRUCTURE_TYPE-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-ARRAYS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-LOOP_STRUCTURES-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-CONDITIONAL_STATEMENTS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VARIABLES_AND_CONSTANTS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-NAMING_CONVENTIONS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-02` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-CONTAINER_VIEWS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VIEW_HIERARCHY-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-UI_CONTROLS-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SYNTAX_ERRORS-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-RUNTIME_ERRORS-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-ERROR_MESSAGES_CONCEPT-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SHAPE-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-COLOR-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VIEW_CONCEPT-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VIEW_CONCEPT-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VIEW_CONCEPT-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DATA_TYPES-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DATA_TYPES-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DATA_TYPES-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-CONTROL_FLOW-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-CONTROL_FLOW-02` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-CONTROL_FLOW-03` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-TYPE_SYSTEM-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-TYPE_SYSTEM-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-TYPE_SYSTEM-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VISUAL_DESIGN-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VISUAL_DESIGN-02` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VISUAL_DESIGN-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-VISUAL_DESIGN-04` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SECURITY_CHALLENGES-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DEBUGGING-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DEBUGGING-02` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DEBUGGING-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-02` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OBJECT_INSTANTIATION-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-03` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-OBJECT_PROPERTIES-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-01` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-RETURN_VALUES_AND_SCOPE-03` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-WHILE_LOOP-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-WHILE_LOOP-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-ARRAY_OPERATIONS-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-ARRAY_OPERATIONS-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-ARRAY_OPERATIONS-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-LOCAL_VIEW_STATE-01` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-04` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-REFERENCE_TYPE_DECLARATION-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-WHILE_LOOP-02` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-ZERO_BASED_INDEX` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-SEQUENTIAL_ARRAY_TRAVERSAL` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-MODIFY_ARRAY_ELEMENT` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-CONTROL_UI_PROPERTIES` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-UPDATE_LOCAL_STATE` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-TRACE_LOCAL_STATE_LIFECYCLE` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-LOCAL_VIEW_STATE-DETERMINE_LOCAL_STATE_SCOPE` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-INITIALIZE_UPDATE_MUTABLE_STATE` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-WHILE_LOOP-DYNAMIC_CONDITION_REPETITION` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-WHILE_LOOP-SENTINEL_CONTROLLED_REPETITION` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_CATALOG_HIERARCHICAL` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_ADDITION_REFERENCE` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-COLOR_ASSET_DEFINITION` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-SYNTAX_RUNTIME_CAUSES` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-CLASSIFY_ERROR_DETECTION` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-IDENTIFY_ERROR_TYPE` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-ANALYZE_ERROR_MESSAGES` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-COMPARE_REFERENCE_VALUE` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-ANALYZE_REFERENCE_IMPACT` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL_2` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ATTACH_STATE_VIEW` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY` | bloom_level | bloom_level='Evaluate' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | bloom_level | bloom_level='Remember' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DEBUGGING-USE_STEP_INTO_AND` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-DEBUGGING-USE_5_WHYS_ON` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | bloom_level | bloom_level='Understand' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN` | bloom_level | bloom_level='Apply' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| learning_objectives | `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | bloom_level | bloom_level='Analyze' không thuộc ['', 'ANALYZE', 'APPLY', 'CREATE', 'EVALUATE', 'REMEMBER', 'UNDERSTAND']. |
| ... | ... | ... | (+245 dòng nữa) |

### `INCONSISTENT_LINE_ENDINGS` (1) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `concepts.tsv` | - | File dùng line-ending CRLF, khác đa số các file khác (LF). |
