# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-25T13:40:40.799737+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 97 (36 lỗi, 61 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 12 |
| topics | 16 |
| concepts | 24 |
| learning_objectives | 335 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 55 |
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 18 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 18 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 4 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 2 |

## ❌ Lỗi (ERROR) — cần sửa

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
