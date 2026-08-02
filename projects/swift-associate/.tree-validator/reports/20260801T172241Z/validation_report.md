# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-01T17:22:41.672285+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 29 (0 lỗi, 29 cảnh báo)

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
| `LO_DESCRIPTION_PREFIX` | Mô tả LO không bắt đầu bằng 'Người học có khả năng' | 1 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (28) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | - | CIO 'So sánh dựa trên vector lây nhiễm và hành vi sau lây nhiễm (malware, worm, ransomware, security, virus)' (CIO-MALWARE_TYPES_CONCEPT-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | - | CIO 'Phân loại theo mục tiêu tấn công và mức độ ảnh hưởng (malware, worm, ransomware, security, virus)' (CIO-MALWARE_TYPES_CONCEPT-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-01` | - | CIO 'Sử dụng cấu trúc rẽ nhánh dựa trên giá trị của biểu thức (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-01) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-02` | - | CIO 'Sử dụng cấu trúc rẽ nhánh với trường hợp mặc định và nhiều giá trị (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-02) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-03` | - | CIO 'Phân tích hành vi fall-through và break (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-03) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-04` | - | CIO 'Phân tích xử lý trường hợp không khớp (default) (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-04) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-01-DUP2` | - | CIO 'So sánh chiến lược giảm thiểu thiên vị theo tiêu chí (training data, fairness, AI bias, ethics)' (CIO-AI_BIAS-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-02-DUP2` | - | CIO 'Đề xuất chiến lược dựa trên phân tích bối cảnh (training data, fairness, AI bias, ethics)' (CIO-AI_BIAS-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-02` | - | CIO 'Nhận diện lỗi cú pháp qua mẫu cấu trúc (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-03` | - | CIO 'Xác định vị trí lỗi dựa trên thông báo lỗi (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-04` | - | CIO 'Sửa lỗi cú pháp bằng cách điều chỉnh cấu trúc (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-05` | - | CIO 'Áp dụng quy trình sửa lỗi từng bước (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-06` | - | CIO 'Phân tích nguyên nhân gốc rễ của lỗi cú pháp phức tạp (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-07` | - | CIO 'So sánh lỗi cú pháp với lỗi logic để xác định bản chất (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-07) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | - | CIO 'Đồng bộ hóa dữ liệu giữa nguồn và giao diện theo cả hai hướng (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | - | CIO 'Khai báo liên kết hai chiều giữa thuộc tính và biến (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-03` | - | CIO 'So sánh luồng dữ liệu một chiều và hai chiều (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-04` | - | CIO 'Xác định tác động của liên kết hai chiều đến hiệu suất (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01-DUP2` | - | CIO 'Phân tích overhead của đồng bộ dữ liệu hai chiều (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02-DUP2` | - | CIO 'So sánh chi phí cập nhật giữa binding một chiều và hai chiều (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | - | CIO 'Cấu hình quy tắc cho phép truy cập dựa trên nguồn gốc (security, same-origin, cross-origin, CORS)' (CIO-CROSS_ORIGIN_SECURITY-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | - | CIO 'Kiểm tra nguồn gốc yêu cầu và áp dụng chính sách động (security, same-origin, cross-origin, CORS)' (CIO-CROSS_ORIGIN_SECURITY-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | - | CIO 'Mô tả đặc điểm của hàm như một giá trị có thể gán, truyền và trả về (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | - | CIO 'So sánh hàm với các kiểu dữ liệu khác về khả năng thao tác (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | - | CIO 'Sử dụng hàm nhận hàm khác làm đối số để thực hiện thao tác trên từng phần tử (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | - | CIO 'Xây dựng pipeline xử lý dữ liệu bằng cách kết hợp các hàm biến đổi (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | - | CIO 'Tạo hàm bao bọc nhận một hàm và trả về hàm mới với hành vi mở rộng (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | - | CIO 'Thiết kế hàm nhận hàm xử lý và áp dụng nó trong một ngữ cảnh cụ thể (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |

### `LO_DESCRIPTION_PREFIX` (1) — Mô tả LO không bắt đầu bằng 'Người học có khả năng'

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-LOGIC_ERRORS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
