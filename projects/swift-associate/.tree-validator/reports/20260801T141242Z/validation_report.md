# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-01T14:12:42.662513+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 28 (0 lỗi, 28 cảnh báo)

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
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 28 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (28) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
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
