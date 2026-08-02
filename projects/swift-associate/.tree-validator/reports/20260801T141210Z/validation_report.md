# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-01T14:12:10.271611+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 93 (52 lỗi, 41 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 10 |
| categories | 19 |
| topics | 30 |
| concepts | 44 |
| learning_objectives | 547 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 41 |
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 26 |
| `LO_TYPE_PARENT_MISMATCH` | lo_type=UNIVERSAL phải có parent_lo_code=NULL và ngược lại | 26 |

## ❌ Lỗi (ERROR) — cần sửa

### `EMPTY_PARENT_REF` (26) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-REFERENCE_IMAGE_BY_NAME` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-REFERENCE_COLOR_BY_NAME` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_FOR_IN` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_ENUMERATED` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_IN_PLACE_CONDITION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_WITH_MAP` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_COUNTER` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_BOOLEAN_FLAG` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_USER_INPUT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_FUNCTION_RESULT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DECLARE_STATE_PROPERTY` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-READ_ERROR_MESSAGE_TYPE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-LOCATE_ERROR_CAUSE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |

### `LO_TYPE_PARENT_MISMATCH` (26) — lo_type=UNIVERSAL phải có parent_lo_code=NULL và ngược lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-REFERENCE_IMAGE_BY_NAME` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-REFERENCE_COLOR_BY_NAME` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_FOR_IN` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ITERATE_ARRAY_ENUMERATED` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_IN_PLACE_CONDITION` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-MODIFY_ARRAY_WITH_MAP` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_COUNTER` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_BOOLEAN_FLAG` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_USER_INPUT` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-WHILE_LOOP_FUNCTION_RESULT` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-DECLARE_STATE_PROPERTY` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-READ_ERROR_MESSAGE_TYPE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |
| learning_objectives | `SIO-SWIFT-LOCATE_ERROR_CAUSE` | parent_lo_code | lo_type=SPECIFIC_IMPL nhưng parent_lo_code=NULL (cần có parent). |

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (41) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | - | CIO 'Phân loại tài nguyên dự án theo loại' (CIO-PROJECT_ASSETS_MANAGEMENT-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | - | CIO 'Thêm tài nguyên vào cấu trúc dự án' (CIO-PROJECT_ASSETS_MANAGEMENT-03-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | - | CIO 'Tham chiếu tài nguyên bằng tên định danh' (CIO-PROJECT_ASSETS_MANAGEMENT-03-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-01` | - | CIO 'Duyệt mảng và truy cập từng phần tử' (CIO-ARRAY_OPERATIONS-03-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ARRAY_OPERATIONS-03-02` | - | CIO 'Sửa đổi mảng tại chỗ dựa trên điều kiện' (CIO-ARRAY_OPERATIONS-03-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-03-01` | - | CIO 'Lặp với điều kiện kiểm tra trước' (CIO-WHILE_LOOP-03-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-WHILE_LOOP-03-02` | - | CIO 'Lặp với điều kiện phụ thuộc đầu vào' (CIO-WHILE_LOOP-03-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | - | CIO 'So sánh khai báo và mệnh lệnh trong xây dựng giao diện' (CIO-DECLARATIVE_UI_PARADIGM-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | - | CIO 'Áp dụng modifier theo chuỗi để tạo kiểu giao diện' (CIO-UI_MODIFIERS_CONCEPT-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | - | CIO 'Gắn hàm xử lý sự kiện tương tác' (CIO-EVENT_HANDLERS_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | - | CIO 'Khai báo và cập nhật biến trạng thái có giám sát' (CIO-STATE_PROPERTY_WRAPPER-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | - | CIO 'Phân loại lỗi dựa trên thời điểm phát hiện' (CIO-SYNTAX_VS_RUNTIME_ERRORS-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-ERROR_MESSAGES_CONCEPT-02` | - | CIO 'Giải thích thông báo lỗi dựa trên cấu trúc' (CIO-ERROR_MESSAGES_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | - | CIO 'So sánh dựa trên vector lây nhiễm và hành vi sau lây nhiễm' (CIO-MALWARE_TYPES_CONCEPT-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | - | CIO 'Phân loại theo mục tiêu tấn công và mức độ ảnh hưởng' (CIO-MALWARE_TYPES_CONCEPT-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-01` | - | CIO 'Sử dụng cấu trúc rẽ nhánh dựa trên giá trị của biểu thức' (CIO-SWITCH_CASE-01) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-02` | - | CIO 'Sử dụng cấu trúc rẽ nhánh với trường hợp mặc định và nhiều giá trị' (CIO-SWITCH_CASE-02) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-03` | - | CIO 'Phân tích hành vi fall-through và break' (CIO-SWITCH_CASE-03) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-04` | - | CIO 'Phân tích xử lý trường hợp không khớp (default)' (CIO-SWITCH_CASE-04) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-01-DUP2` | - | CIO 'So sánh chiến lược giảm thiểu thiên vị theo tiêu chí' (CIO-AI_BIAS-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-02-DUP2` | - | CIO 'Đề xuất chiến lược dựa trên phân tích bối cảnh' (CIO-AI_BIAS-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-02` | - | CIO 'Nhận diện lỗi cú pháp qua mẫu cấu trúc' (CIO-SYNTAX_ERRORS-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-03` | - | CIO 'Xác định vị trí lỗi dựa trên thông báo lỗi' (CIO-SYNTAX_ERRORS-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-04` | - | CIO 'Sửa lỗi cú pháp bằng cách điều chỉnh cấu trúc' (CIO-SYNTAX_ERRORS-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-05` | - | CIO 'Áp dụng quy trình sửa lỗi từng bước' (CIO-SYNTAX_ERRORS-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-06` | - | CIO 'Phân tích nguyên nhân gốc rễ của lỗi cú pháp phức tạp' (CIO-SYNTAX_ERRORS-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-07` | - | CIO 'So sánh lỗi cú pháp với lỗi logic để xác định bản chất' (CIO-SYNTAX_ERRORS-07) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | - | CIO 'Đồng bộ hóa dữ liệu giữa nguồn và giao diện theo cả hai hướng' (CIO-TWO_WAY_BINDING-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | - | CIO 'Khai báo liên kết hai chiều giữa thuộc tính và biến' (CIO-TWO_WAY_BINDING-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-03` | - | CIO 'So sánh luồng dữ liệu một chiều và hai chiều' (CIO-TWO_WAY_BINDING-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-04` | - | CIO 'Xác định tác động của liên kết hai chiều đến hiệu suất' (CIO-TWO_WAY_BINDING-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01-DUP2` | - | CIO 'Phân tích overhead của đồng bộ dữ liệu hai chiều' (CIO-TWO_WAY_BINDING-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02-DUP2` | - | CIO 'So sánh chi phí cập nhật giữa binding một chiều và hai chiều' (CIO-TWO_WAY_BINDING-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | - | CIO 'Cấu hình quy tắc cho phép truy cập dựa trên nguồn gốc' (CIO-CROSS_ORIGIN_SECURITY-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | - | CIO 'Kiểm tra nguồn gốc yêu cầu và áp dụng chính sách động' (CIO-CROSS_ORIGIN_SECURITY-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | - | CIO 'Mô tả đặc điểm của hàm như một giá trị có thể gán, truyền và trả về' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | - | CIO 'So sánh hàm với các kiểu dữ liệu khác về khả năng thao tác' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | - | CIO 'Sử dụng hàm nhận hàm khác làm đối số để thực hiện thao tác trên từng phần tử' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | - | CIO 'Xây dựng pipeline xử lý dữ liệu bằng cách kết hợp các hàm biến đổi' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | - | CIO 'Tạo hàm bao bọc nhận một hàm và trả về hàm mới với hành vi mở rộng' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | - | CIO 'Thiết kế hàm nhận hàm xử lý và áp dụng nó trong một ngữ cảnh cụ thể' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
