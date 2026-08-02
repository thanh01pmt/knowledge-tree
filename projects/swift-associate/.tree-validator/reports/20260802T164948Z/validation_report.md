# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-02T16:49:48.063238+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 42 (3 lỗi, 39 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 5 |
| subjects | 12 |
| categories | 25 |
| topics | 36 |
| concepts | 39 |
| learning_objectives | 0 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 39 |
| `MISSING_FILE` | Không tìm thấy file dữ liệu | 1 |
| `LO_PREREQ_BROKEN_TARGET` | learning_objective_code trong prerequisites không tồn tại | 1 |
| `LO_PREREQ_BROKEN_PREREQ` | prerequisite_lo_code trong prerequisites không tồn tại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `MISSING_FILE` (1) — Không tìm thấy file dữ liệu

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `-` | - | Không tìm thấy file learning-objectives.tsv |

### `LO_PREREQ_BROKEN_TARGET` (1) — learning_objective_code trong prerequisites không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objective_prerequisites | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | - | learning_objective_code 'ULO-SYNTAX_VS_RUNTIME_ERRORS-03' không tồn tại trong learning-objectives.tsv |

### `LO_PREREQ_BROKEN_PREREQ` (1) — prerequisite_lo_code trong prerequisites không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objective_prerequisites | `ULO-ERROR_MESSAGES_CONCEPT-02` | - | prerequisite_lo_code 'ULO-ERROR_MESSAGES_CONCEPT-02' không tồn tại trong learning-objectives.tsv |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (39) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `ACCESS_MODIFIERS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `AI_BIAS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ALGORITHMIC_BIAS_SOCIETY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ARRAY_OPERATIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ASYNCHRONOUS_PROG_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `BREAKPOINTS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `CLASS_DEFINITION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `COLOR_THEORY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `COMPOSITION_PRINCIPLES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `COPYRIGHT_CREATIVE_COMMONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DESIGN_THINKING_PROCESS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DIGITAL_FOOTPRINT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ERROR_MESSAGES_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `EVENT_BASED_PROGRAMMING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `FIRST_CLASS_FUNCTIONS_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `FOR_LOOP` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `IF_ELSE_STATEMENT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `IMPLICIT_EXPLICIT_ANIMATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `INFORMATION_CREDIBILITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `INHERITANCE_SYNTAX` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LEVEL_LAYOUT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LIST_OPERATIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LOCAL_VIEW_STATE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LOGIC_ERRORS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_INSTANTIATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_PROPERTIES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PHISHING_IDENTIFICATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `PRIMITIVE_TYPE_DECLARATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `REFERENCE_TYPE_DECLARATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `RUNTIME_ERRORS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SWITCH_CASE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SYNTAX_ERRORS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TWO_WAY_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TYPOGRAPHY_AND_VISUAL_HIERARCHY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `USER_CENTERED_DESIGN` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VERSION_CONTROL_WORKFLOW` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `WCAG_PRINCIPLES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `WHILE_LOOP` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `WIREFRAMING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
