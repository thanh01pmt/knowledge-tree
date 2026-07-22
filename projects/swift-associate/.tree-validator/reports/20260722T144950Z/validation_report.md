# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-22T14:49:50.595832+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 110 (106 lỗi, 4 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 7 |
| categories | 8 |
| topics | 7 |
| concepts | 11 |
| learning_objectives | 141 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 53 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 53 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 4 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (53) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-PARAMETERIZED-SUBROUTINE` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEFINE-SUBROUTINE` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-FUNC-DEFINE` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-FUNC-VOID` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARG-LABELS` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-INVOKE-SUBROUTINE` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-FUNC-CALL` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-FUNC-RETURN-CAPTURE` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TRACE-SUBROUTINE-EXECUTION` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE-FUNC-CALL` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-PREDICT-FUNC-OUTPUT` | concept_codes | 'FIRST_CLASS_FUNCTIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ARITHMETIC-LOGIC-OPS` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-COMPUTE-ARITHMETIC` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARITHMETIC-OPS` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPOUND-ASSIGN` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVALUATE-BOOLEAN-EXPR` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARISON-OPS` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-LOGICAL-OPS` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-COMPOSITE-DATA-TYPE` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DEFINE-COMPOSITE-TYPE` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STRUCT-DEFINE` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STRUCT-METHODS` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-INSTANTIATE-COMPOSITE-TYPE` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STRUCT-INIT` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STRUCT-ACCESS` | concept_codes | 'REFERENCE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-ORDERED-COLLECTION` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DECLARE-ORDERED-COLLECTION` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARRAY-DECLARE` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARRAY-EMPTY` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-ACCESS-MODIFY-COLLECTION` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARRAY-READ-INDEX` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARRAY-WRITE-INDEX` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARRAY-PROPERTIES` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ARRAY-METHODS` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-FOR-IN-ARRAY` | concept_codes | 'ARRAY_OPERATIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CONDITIONAL-EXECUTION` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-BRANCH-ON-CONDITION` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-IF-ELSE` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SWITCH-CASE` | concept_codes | 'SWITCH_CASE' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-TRACE-CONDITIONAL-LOGIC` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE-IF-CHAIN` | concept_codes | 'IF_ELSE_STATEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE-SWITCH` | concept_codes | 'SWITCH_CASE' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-MUTABLE-IMMUTABLE-STATE` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DECLARE-VALUE-BINDING` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-LET-CONSTANT` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-VAR-VARIABLE` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-APPLY-TYPE-SYSTEM` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TYPE-INFERENCE` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EXPLICIT-TYPE` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-APPLY-NAMING-CONVENTIONS` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CAMELCASE` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ID-RULES` | concept_codes | 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STATE-TWO-WAY-BIND` | concept_codes | 'TWO_WAY_BINDING' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (53) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-PARAMETERIZED-SUBROUTINE` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEFINE-SUBROUTINE` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-FUNC-DEFINE` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-FUNC-VOID` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARG-LABELS` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-INVOKE-SUBROUTINE` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-FUNC-CALL` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-FUNC-RETURN-CAPTURE` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TRACE-SUBROUTINE-EXECUTION` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE-FUNC-CALL` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-PREDICT-FUNC-OUTPUT` | concept_codes | concept_code 'FIRST_CLASS_FUNCTIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ARITHMETIC-LOGIC-OPS` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-COMPUTE-ARITHMETIC` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARITHMETIC-OPS` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPOUND-ASSIGN` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVALUATE-BOOLEAN-EXPR` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARISON-OPS` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-LOGICAL-OPS` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-COMPOSITE-DATA-TYPE` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DEFINE-COMPOSITE-TYPE` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STRUCT-DEFINE` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STRUCT-METHODS` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-INSTANTIATE-COMPOSITE-TYPE` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STRUCT-INIT` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STRUCT-ACCESS` | concept_codes | concept_code 'REFERENCE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-ORDERED-COLLECTION` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DECLARE-ORDERED-COLLECTION` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARRAY-DECLARE` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARRAY-EMPTY` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-ACCESS-MODIFY-COLLECTION` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARRAY-READ-INDEX` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARRAY-WRITE-INDEX` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARRAY-PROPERTIES` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ARRAY-METHODS` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-FOR-IN-ARRAY` | concept_codes | concept_code 'ARRAY_OPERATIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CONDITIONAL-EXECUTION` | concept_codes | concept_code 'IF_ELSE_STATEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-BRANCH-ON-CONDITION` | concept_codes | concept_code 'IF_ELSE_STATEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-IF-ELSE` | concept_codes | concept_code 'IF_ELSE_STATEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SWITCH-CASE` | concept_codes | concept_code 'SWITCH_CASE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-TRACE-CONDITIONAL-LOGIC` | concept_codes | concept_code 'IF_ELSE_STATEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE-IF-CHAIN` | concept_codes | concept_code 'IF_ELSE_STATEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE-SWITCH` | concept_codes | concept_code 'SWITCH_CASE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-MUTABLE-IMMUTABLE-STATE` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DECLARE-VALUE-BINDING` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-LET-CONSTANT` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-VAR-VARIABLE` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-APPLY-TYPE-SYSTEM` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TYPE-INFERENCE` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EXPLICIT-TYPE` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-APPLY-NAMING-CONVENTIONS` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CAMELCASE` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ID-RULES` | concept_codes | concept_code 'PRIMITIVE_TYPE_DECLARATION' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STATE-TWO-WAY-BIND` | concept_codes | concept_code 'TWO_WAY_BINDING' không tồn tại trong concepts.tsv của project. |

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (4) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| subjects | `DIGITAL_LITERACY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `DATA_PRIVACY_USER` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `TROUBLESHOOTING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `UI_UX_PROCESS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
