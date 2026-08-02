# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-08-01T17:52:56.441836+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**

---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

**28 CIO(s) có < 2 SIO:**

| CIO Code | CIO Name | SIO Count | Parent ULO |
|---|---|---|---|
| `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | So sánh dựa trên vector lây nhiễm và hành vi sau lây nhiễm (malware, worm, ransomware, security, virus) | ❌ 0 | `ULO-MALWARE_TYPES_CONCEPT-02` |
| `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | Phân loại theo mục tiêu tấn công và mức độ ảnh hưởng (malware, worm, ransomware, security, virus) | ❌ 0 | `ULO-MALWARE_TYPES_CONCEPT-02` |
| `CIO-SWITCH_CASE-01` | Sử dụng cấu trúc rẽ nhánh dựa trên giá trị của biểu thức (branching, switch-case, multi-way, selection) | ⚠️ 1 | `ULO-SWITCH_CASE-01` |
| `CIO-SWITCH_CASE-02` | Sử dụng cấu trúc rẽ nhánh với trường hợp mặc định và nhiều giá trị (branching, switch-case, multi-way, selection) | ⚠️ 1 | `ULO-SWITCH_CASE-01` |
| `CIO-SWITCH_CASE-03` | Phân tích hành vi fall-through và break (branching, switch-case, multi-way, selection) | ⚠️ 1 | `ULO-SWITCH_CASE-02` |
| `CIO-SWITCH_CASE-04` | Phân tích xử lý trường hợp không khớp (default) (branching, switch-case, multi-way, selection) | ⚠️ 1 | `ULO-SWITCH_CASE-02` |
| `CIO-AI_BIAS-01-DUP2` | So sánh chiến lược giảm thiểu thiên vị theo tiêu chí (training data, fairness, AI bias, ethics) | ❌ 0 | `ULO-AI_BIAS-03` |
| `CIO-AI_BIAS-02-DUP2` | Đề xuất chiến lược dựa trên phân tích bối cảnh (training data, fairness, AI bias, ethics) | ❌ 0 | `ULO-AI_BIAS-03` |
| `CIO-SYNTAX_ERRORS-02` | Nhận diện lỗi cú pháp qua mẫu cấu trúc (compiler error, syntax error, parsing) | ❌ 0 | `ULO-SYNTAX_ERRORS-01` |
| `CIO-SYNTAX_ERRORS-03` | Xác định vị trí lỗi dựa trên thông báo lỗi (compiler error, syntax error, parsing) | ❌ 0 | `ULO-SYNTAX_ERRORS-01` |
| `CIO-SYNTAX_ERRORS-04` | Sửa lỗi cú pháp bằng cách điều chỉnh cấu trúc (compiler error, syntax error, parsing) | ❌ 0 | `ULO-SYNTAX_ERRORS-02` |
| `CIO-SYNTAX_ERRORS-05` | Áp dụng quy trình sửa lỗi từng bước (compiler error, syntax error, parsing) | ❌ 0 | `ULO-SYNTAX_ERRORS-02` |
| `CIO-SYNTAX_ERRORS-06` | Phân tích nguyên nhân gốc rễ của lỗi cú pháp phức tạp (compiler error, syntax error, parsing) | ❌ 0 | `ULO-SYNTAX_ERRORS-03` |
| `CIO-SYNTAX_ERRORS-07` | So sánh lỗi cú pháp với lỗi logic để xác định bản chất (compiler error, syntax error, parsing) | ❌ 0 | `ULO-SYNTAX_ERRORS-03` |
| `CIO-TWO_WAY_BINDING-01` | Đồng bộ hóa dữ liệu giữa nguồn và giao diện theo cả hai hướng (two-way binding, data binding, sync) | ❌ 0 | `ULO-TWO_WAY_BINDING-01` |
| `CIO-TWO_WAY_BINDING-02` | Khai báo liên kết hai chiều giữa thuộc tính và biến (two-way binding, data binding, sync) | ❌ 0 | `ULO-TWO_WAY_BINDING-01` |
| `CIO-TWO_WAY_BINDING-03` | So sánh luồng dữ liệu một chiều và hai chiều (two-way binding, data binding, sync) | ❌ 0 | `ULO-TWO_WAY_BINDING-02` |
| `CIO-TWO_WAY_BINDING-04` | Xác định tác động của liên kết hai chiều đến hiệu suất (two-way binding, data binding, sync) | ❌ 0 | `ULO-TWO_WAY_BINDING-03` |
| `CIO-TWO_WAY_BINDING-01-DUP2` | Phân tích overhead của đồng bộ dữ liệu hai chiều (two-way binding, data binding, sync) | ❌ 0 | `ULO-TWO_WAY_BINDING-03` |
| `CIO-TWO_WAY_BINDING-02-DUP2` | So sánh chi phí cập nhật giữa binding một chiều và hai chiều (two-way binding, data binding, sync) | ❌ 0 | `ULO-TWO_WAY_BINDING-03` |
| `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | Cấu hình quy tắc cho phép truy cập dựa trên nguồn gốc (security, same-origin, cross-origin, CORS) | ❌ 0 | `ULO-CROSS_ORIGIN_SECURITY-02` |
| `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | Kiểm tra nguồn gốc yêu cầu và áp dụng chính sách động (security, same-origin, cross-origin, CORS) | ❌ 0 | `ULO-CROSS_ORIGIN_SECURITY-02` |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | Mô tả đặc điểm của hàm như một giá trị có thể gán, truyền và trả về (lambda, closure, higher-order function, first-class) | ❌ 0 | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | So sánh hàm với các kiểu dữ liệu khác về khả năng thao tác (lambda, closure, higher-order function, first-class) | ❌ 0 | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | Sử dụng hàm nhận hàm khác làm đối số để thực hiện thao tác trên từng phần tử (lambda, closure, higher-order function, first-class) | ❌ 0 | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | Xây dựng pipeline xử lý dữ liệu bằng cách kết hợp các hàm biến đổi (lambda, closure, higher-order function, first-class) | ❌ 0 | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | Tạo hàm bao bọc nhận một hàm và trả về hàm mới với hành vi mở rộng (lambda, closure, higher-order function, first-class) | ❌ 0 | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | Thiết kế hàm nhận hàm xử lý và áp dụng nó trong một ngữ cảnh cụ thể (lambda, closure, higher-order function, first-class) | ❌ 0 | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` |

**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.
---

## Gap D — Marr's Test Violated CIOs (`MARR_VIOLATION`)

> CIO chứa từ khóa công nghệ, cú pháp hoặc cấu trúc ngôn ngữ cụ thể — vi phạm Phép thử Marr 2-Ngôn-ngữ.

**4 CIO(s) vi phạm tính Trung tính (Marr Test):**

| CIO Code | CIO Name | Detected Keywords / Patterns |
|---|---|---|
| `CIO-PRIMITIVE_TYPE_DECLARATION-01` | Phân tích kiểu dữ liệu từ giá trị (int, boolean, data type, primitive type, declaration) | `swift` |
| `CIO-PRIMITIVE_TYPE_DECLARATION-02` | So sánh đặc điểm lưu trữ kiểu (int, boolean, data type, primitive type, declaration) | `swift` |
| `CIO-PRIMITIVE_TYPE_DECLARATION-03` | Chọn kiểu dữ liệu theo yêu cầu (int, boolean, data type, primitive type, declaration) | `swift` |
| `CIO-PRIMITIVE_TYPE_DECLARATION-04` | Khai báo biến phù hợp bài toán (int, boolean, data type, primitive type, declaration) | `swift` |

**→ Action:** Viết lại mô tả/tên CIO thành khái niệm/thủ tục trung tính 100% độc lập ngôn ngữ, hoặc chuyển xuống tầng SIO.
---

## Gap E — Marr Test Note Quality (`MARR_NOTE_QUALITY`)

> CIO có marr_test_note nhưng note không đủ chất lượng (thiếu note, hoặc nhắc < 2 ngôn ngữ).
> Theo T6: CIO bắt buộc phải pass Marr 2-Language Test — note phải chứng minh mapping ≥ 2 ngôn ngữ.

**163 CIO(s) có vấn đề với marr_test_note:**

| CIO Code | CIO Name | Issue | Detail |
|---|---|---|---|
| `CIO-PROJECT_ASSETS_MANAGEMENT-01` | Phân loại tài nguyên dự án theo loại (asset, file type, project navigation, Xcode, import) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | Thêm tài nguyên vào cấu trúc dự án (asset, file type, project navigation, Xcode, import) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | Tham chiếu tài nguyên bằng tên định danh (asset, file type, project navigation, Xcode, import) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-03-01` | Duyệt mảng và truy cập từng phần tử (index, traverse, element, modify, array) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-03-02` | Sửa đổi mảng tại chỗ dựa trên điều kiện (index, traverse, element, modify, array) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-03-01` | Lặp với điều kiện kiểm tra trước (iteration, looping, condition, while loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-03-02` | Lặp với điều kiện phụ thuộc đầu vào (iteration, looping, condition, while loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-03` | So sánh khai báo và mệnh lệnh trong xây dựng giao diện (declarative, SwiftUI, imperative, UIKit) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS_CONCEPT-03` | Áp dụng modifier theo chuỗi để tạo kiểu giao diện (foregroundColor, frame, font, resizable, background) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-02` | Gắn hàm xử lý sự kiện tương tác (listener, callback, event, event handler) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-02` | Khai báo và cập nhật biến trạng thái có giám sát (state management, property wrapper, @State, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | Phân loại lỗi dựa trên thời điểm phát hiện (compile-time, error type, syntax error, runtime error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ERROR_MESSAGES_CONCEPT-02` | Giải thích thông báo lỗi dựa trên cấu trúc (stack trace, error message, error handling, debugging) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IF_ELSE_STATEMENT-01` | Phân tích điều kiện đơn (branching, conditional, if-else, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IF_ELSE_STATEMENT-02` | Phân tích điều kiện kết hợp (branching, conditional, if-else, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IF_ELSE_STATEMENT-03` | Áp dụng rẽ nhánh cơ bản (branching, conditional, if-else, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IF_ELSE_STATEMENT-04` | Áp dụng rẽ nhánh lồng nhau (branching, conditional, if-else, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PRIMITIVE_TYPE_DECLARATION-01` | Phân tích kiểu dữ liệu từ giá trị (int, boolean, data type, primitive type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PRIMITIVE_TYPE_DECLARATION-02` | So sánh đặc điểm lưu trữ kiểu (int, boolean, data type, primitive type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PRIMITIVE_TYPE_DECLARATION-03` | Chọn kiểu dữ liệu theo yêu cầu (int, boolean, data type, primitive type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PRIMITIVE_TYPE_DECLARATION-04` | Khai báo biến phù hợp bài toán (int, boolean, data type, primitive type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_FOOTPRINT-01` | Phân tích dấu chân số từ hoạt động (digital footprint, privacy, online, personal information) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_FOOTPRINT-02` | Đánh giá mức độ ảnh hưởng (digital footprint, privacy, online, personal information) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_FOOTPRINT-03` | Nhận diện rủi ro từ hành vi (digital footprint, privacy, online, personal information) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_FOOTPRINT-04` | So sánh mức độ nguy hiểm (digital footprint, privacy, online, personal information) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_TRANSITIONS-01` | Phân loại hiệu ứng chuyển tiếp (animation, fade, transition, slide) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_TRANSITIONS-02` | Phân tích tác động UX (animation, fade, transition, slide) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_TRANSITIONS-03` | Lựa chọn hiệu ứng theo ngữ cảnh (animation, fade, transition, slide) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_TRANSITIONS-04` | Tạo chuyển tiếp liên tục (animation, fade, transition, slide) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RUNTIME_ERRORS-01` | Phân loại lỗi runtime dựa trên nguyên nhân gốc (exception, crash, runtime error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RUNTIME_ERRORS-02` | Nhận diện dấu hiệu lỗi runtime từ thông báo lỗi (exception, crash, runtime error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RUNTIME_ERRORS-03` | Sử dụng cơ chế bắt và xử lý ngoại lệ (exception, crash, runtime error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RUNTIME_ERRORS-04` | Kiểm tra điều kiện trước khi thực thi để ngăn lỗi (exception, crash, runtime error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WCAG_PRINCIPLES-01` | Phân tích bốn nguyên tắc POUR và ý nghĩa của chúng trong thiết kế giao diện (WCAG, robust, understandable, perceivable, accessibility) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WCAG_PRINCIPLES-02` | Đánh giá giao diện dựa trên tiêu chí Perceivable (POUR, WCAG, robust, understandable, accessibility) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WCAG_PRINCIPLES-03` | Đánh giá giao diện dựa trên tiêu chí Operable (POUR, WCAG, robust, understandable, perceivable) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ALGORITHMIC_BIAS_SOCIETY-01` | Phân tích thành kiến từ dữ liệu huấn luyện (societal impact, algorithmic bias, fairness, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ALGORITHMIC_BIAS_SOCIETY-02` | Phân tích thành kiến từ quyết định thiết kế thuật toán (societal impact, algorithmic bias, fairness, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ALGORITHMIC_BIAS_SOCIETY-03` | Phân tích tác động của thành kiến thuật toán đến các nhóm xã hội (societal impact, algorithmic bias, fairness, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PHISHING_IDENTIFICATION-01` | Phân tích các đặc điểm của email lừa đảo dựa trên nội dung và ngữ cảnh (security, scam, phishing, social engineering) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PHISHING_IDENTIFICATION-02` | Thực hiện quy trình xác minh thông điệp qua nhiều kênh (security, scam, phishing, social engineering) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FOR_LOOP-01` | Phân tích cấu trúc lặp với biến đếm (iteration, for loop, looping, repetition) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FOR_LOOP-02` | Áp dụng lặp với bước nhảy tùy chỉnh (iteration, for loop, looping, repetition) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FOR_LOOP-03` | Áp dụng lặp để duyệt tập hợp (iteration, for loop, looping, repetition) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FOR_LOOP-04` | Áp dụng lặp lồng để xử lý ma trận (iteration, for loop, looping, repetition) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WIREFRAMING-01` | Phân tích mục đích của wireframe trong quy trình thiết kế (sketch, layout, structure) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WIREFRAMING-02` | Áp dụng kỹ thuật phân chia bố cục bằng khung lưới (sketch, layout, structure, wireframe) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WIREFRAMING-03` | Áp dụng ký hiệu tiêu chuẩn cho các thành phần tương tác (sketch, layout, structure, wireframe) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOGIC_ERRORS-01` | Phân tích sự khác biệt giữa kết quả mong đợi và thực tế (incorrect output, bug, logical error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOGIC_ERRORS-02` | Nhận diện lỗi logic qua kiểm tra điều kiện biên (incorrect output, bug, logical error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOGIC_ERRORS-03` | Truy vết luồng thực thi để xác định nguyên nhân lỗi (incorrect output, bug, logical error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOGIC_ERRORS-04` | Phân tích điều kiện và vòng lặp để tìm lỗi logic (incorrect output, bug, logical error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOGIC_ERRORS-05` | Điều chỉnh điều kiện để sửa lỗi logic (incorrect output, bug, logical error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOGIC_ERRORS-06` | Thay đổi thứ tự thực thi để sửa lỗi logic (incorrect output, bug, logical error) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-MALWARE_TYPES_CONCEPT-01` | Phân biệt malware dựa trên cơ chế lây lan (worm, ransomware, security, virus) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-MALWARE_TYPES_CONCEPT-02` | Phân biệt malware dựa trên mục tiêu tấn công (worm, ransomware, security, virus) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | So sánh dựa trên vector lây nhiễm và hành vi sau lây nhiễm (malware, worm, ransomware, security, virus) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | Phân loại theo mục tiêu tấn công và mức độ ảnh hưởng (malware, worm, ransomware, security, virus) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-01` | Phân biệt dựa trên nguồn gốc thay đổi trạng thái (withAnimation, explicit animation, implicit animation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-02` | Phân biệt dựa trên mức độ kiểm soát và tùy chỉnh (withAnimation, explicit animation, implicit animation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-03` | Lựa chọn dựa trên tính chất thay đổi thuộc tính (withAnimation, explicit animation, implicit animation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-04` | Lựa chọn dựa trên yêu cầu về hiệu suất và tùy chỉnh (withAnimation, explicit animation, implicit animation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_BOX_MODEL_LAYOUT-01` | Phân tích ảnh hưởng của từng thành phần đến kích thước tổng thể (box model, layout, padding, margin, border) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_BOX_MODEL_LAYOUT-02` | So sánh các chế độ box-sizing (box model, layout, padding, margin, border) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_BOX_MODEL_LAYOUT-03` | Tính toán kích thước dựa trên công thức cộng dồn (box model, layout, padding, margin, border) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_BOX_MODEL_LAYOUT-04` | Tính toán kích thước với chế độ border-box (box model, layout, padding, margin) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_BOX_MODEL_LAYOUT-05` | Phân tích nguyên nhân khoảng cách bất thường do margin collapsing (box model, layout, padding, border) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_BOX_MODEL_LAYOUT-06` | Phân tích sự chồng lấn do không tính border/padding (box model, layout, margin) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SWITCH_CASE-01` | Sử dụng cấu trúc rẽ nhánh dựa trên giá trị của biểu thức (branching, switch-case, multi-way, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SWITCH_CASE-02` | Sử dụng cấu trúc rẽ nhánh với trường hợp mặc định và nhiều giá trị (branching, switch-case, multi-way, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SWITCH_CASE-03` | Phân tích hành vi fall-through và break (branching, switch-case, multi-way, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SWITCH_CASE-04` | Phân tích xử lý trường hợp không khớp (default) (branching, switch-case, multi-way, selection) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CLASS_DEFINITION-01` | Xác định thuộc tính và hành vi cốt lõi (definition, class, OOP, attributes, methods) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CLASS_DEFINITION-02` | Tổ chức đóng gói và trách nhiệm (definition, class, OOP, attributes, methods) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-01` | So sánh hành vi lưu trữ và truyền dữ liệu (string, object, reference type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-02` | Khởi tạo biến tham chiếu bằng gán đối tượng (string, object, reference type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-03` | Truy cập và thay đổi dữ liệu qua tham chiếu (string, object, reference type, declaration) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-USER_CENTERED_DESIGN-01` | Phân tích trình tự và mối quan hệ giữa các giai đoạn UCD (user-centered, brainstorm, plan, evaluate, design cycle) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-USER_CENTERED_DESIGN-02` | Lựa chọn phương pháp thu thập thông tin người dùng phù hợp (UCD, user-centered, brainstorm, plan, evaluate) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-USER_CENTERED_DESIGN-03` | Đánh giá sản phẩm dựa trên tiêu chí UCD (user-centered, brainstorm, plan, evaluate, design cycle) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-AI_BIAS-01` | Phân loại thiên vị theo giai đoạn phát triển AI (training data, fairness, AI bias, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-AI_BIAS-02` | Xác định điểm tiềm ẩn thiên vị trong pipeline AI (training data, fairness, AI bias, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-AI_BIAS-01-DUP2` | So sánh chiến lược giảm thiểu thiên vị theo tiêu chí (training data, fairness, AI bias, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-AI_BIAS-02-DUP2` | Đề xuất chiến lược dựa trên phân tích bối cảnh (training data, fairness, AI bias, ethics) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-01` | Phân loại lỗi cú pháp dựa trên thông báo lỗi (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-02` | Nhận diện lỗi cú pháp qua mẫu cấu trúc (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-03` | Xác định vị trí lỗi dựa trên thông báo lỗi (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-04` | Sửa lỗi cú pháp bằng cách điều chỉnh cấu trúc (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-05` | Áp dụng quy trình sửa lỗi từng bước (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-06` | Phân tích nguyên nhân gốc rễ của lỗi cú pháp phức tạp (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_ERRORS-07` | So sánh lỗi cú pháp với lỗi logic để xác định bản chất (compiler error, syntax error, parsing) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PASSWORD_STRENGTH_CONCEPT-01` | Liệt kê tiêu chí mật khẩu mạnh theo danh mục (security, strong password, authentication, password) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PASSWORD_STRENGTH_CONCEPT-02` | Phân loại tiêu chí theo mức độ ưu tiên (security, strong password, authentication, password) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PASSWORD_STRENGTH_CONCEPT-03` | Tạo mật khẩu mạnh bằng phương pháp kết hợp ngẫu nhiên (security, strong password, authentication, password) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PASSWORD_STRENGTH_CONCEPT-04` | Áp dụng quy tắc biến đổi từ cụm từ dễ nhớ (security, strong password, authentication, password) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PASSWORD_STRENGTH_CONCEPT-05` | Đánh giá độ mạnh mật khẩu dựa trên thang điểm (security, strong password, authentication, password) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PASSWORD_STRENGTH_CONCEPT-06` | So sánh mật khẩu với danh sách mật khẩu yếu phổ biến (security, strong password, authentication, password) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROTOTYPING-01` | Phân biệt mức độ chi tiết prototype dựa trên mục đích (mockup, interactive, test) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROTOTYPING-02` | So sánh đặc điểm của các mức độ chi tiết prototype (mockup, interactive, test) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROTOTYPING-02-01` | Xây dựng luồng tương tác giữa các màn hình (mockup, interactive, test, prototype) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROTOTYPING-02-02` | Mô phỏng phản hồi của giao diện khi người dùng tương tác (mockup, interactive, test, prototype) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROTOTYPING-03-01` | Phân tích phản hồi người dùng để xác định vấn đề (mockup, interactive, test, prototype) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROTOTYPING-03-02` | Điều chỉnh prototype dựa trên tiêu chí đánh giá (mockup, interactive, test) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-BREAKPOINTS-01-01` | Đặt điểm dừng tại vị trí nghi ngờ lỗi (debugger, debugging, IDE, breakpoint) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-BREAKPOINTS-01-02` | Kích hoạt và vô hiệu hóa điểm dừng (debugger, debugging, IDE, breakpoint) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-BREAKPOINTS-02-01` | Thiết lập điểm dừng chỉ khi biểu thức điều kiện đúng (debugger, debugging, IDE, breakpoint) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-BREAKPOINTS-02-02` | Sử dụng điểm dừng đếm số lần (debugger, debugging, IDE, breakpoint) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-BREAKPOINTS-03-01` | Theo dõi luồng thực thi bằng các bước đơn (debugger, debugging, IDE, breakpoint) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-BREAKPOINTS-03-02` | Phân tích call stack để xác định đường đi của chương trình (debugger, debugging, IDE, breakpoint) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-01-01` | Truy cập thuộc tính bằng tên (object, properties, attributes, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-01-02` | Kiểm tra sự tồn tại của thuộc tính (object, properties, attributes, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-02-01` | Phân loại thành phần của đối tượng dựa trên hành vi (object, properties, attributes, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-02-02` | So sánh cách gọi thuộc tính và phương thức (object, properties, attributes, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-03-01` | Gán giá trị mới cho thuộc tính (object, properties, attributes, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-03-02` | Cập nhật thuộc tính dựa trên giá trị hiện tại (object, properties, attributes, state) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COMPOSITION_PRINCIPLES-01` | Phân chia lưới 3x3 và đặt yếu tố chính (rule of thirds, composition, layout, balance) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COMPOSITION_PRINCIPLES-02` | Tạo điểm nhấn bằng cách đặt chủ thể lệch tâm (rule of thirds, composition, layout, balance) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COMPOSITION_PRINCIPLES-03` | Phân tích đường dẫn thị giác từ điểm vào đến điểm kết thúc (rule of thirds, composition, layout, balance) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COMPOSITION_PRINCIPLES-04` | Nhận diện đường dẫn thị giác dựa trên độ tương phản và kích thước (rule of thirds, composition, layout, balance) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COMPOSITION_PRINCIPLES-05` | Đánh giá cân bằng đối xứng và bất đối xứng (rule of thirds, composition, layout, balance) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COMPOSITION_PRINCIPLES-06` | Phân tích cân bằng dựa trên màu sắc và kích thước (rule of thirds, composition, layout, balance) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_BASED_PROGRAMMING-01` | Liệt kê các sự kiện từ tương tác người dùng và hệ thống (event-driven, asynchronous, event loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_BASED_PROGRAMMING-02` | Phân loại sự kiện theo nguồn gốc và thời điểm (event-driven, asynchronous, event loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_BASED_PROGRAMMING-03` | Đăng ký hàm xử lý cho một sự kiện cụ thể (event-driven, asynchronous, event loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_BASED_PROGRAMMING-04` | Viết hàm xử lý sự kiện với tham số sự kiện (event-driven, asynchronous, event loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_BASED_PROGRAMMING-05` | Phân tích thứ tự thực thi khi nhiều sự kiện xảy ra đồng thời (event-driven, asynchronous, event loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_BASED_PROGRAMMING-06` | Dự đoán luồng thực thi khi có sự kiện lồng nhau (event-driven, asynchronous, event loop) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TWO_WAY_BINDING-01` | Đồng bộ hóa dữ liệu giữa nguồn và giao diện theo cả hai hướng (two-way binding, data binding, sync) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TWO_WAY_BINDING-02` | Khai báo liên kết hai chiều giữa thuộc tính và biến (two-way binding, data binding, sync) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TWO_WAY_BINDING-03` | So sánh luồng dữ liệu một chiều và hai chiều (two-way binding, data binding, sync) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TWO_WAY_BINDING-04` | Xác định tác động của liên kết hai chiều đến hiệu suất (two-way binding, data binding, sync) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TWO_WAY_BINDING-01-DUP2` | Phân tích overhead của đồng bộ dữ liệu hai chiều (two-way binding, data binding, sync) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TWO_WAY_BINDING-02-DUP2` | So sánh chi phí cập nhật giữa binding một chiều và hai chiều (two-way binding, data binding, sync) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_IDENTITY-01` | Mô hình hóa các thành phần của danh tính số (digital identity, online profile, reputation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_IDENTITY-02` | Phân loại các loại thông tin trong danh tính số (digital identity, online profile, reputation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_IDENTITY-03` | Phân tích mối quan hệ giữa quản lý danh tính và cơ hội nghề nghiệp (digital identity, online profile, reputation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_IDENTITY-04` | Đánh giá rủi ro từ việc quản lý danh tính không nhất quán (digital identity, online profile, reputation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_IDENTITY-05` | So sánh các chiến lược quản lý hình ảnh trên các nền tảng (digital identity, online profile, reputation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DIGITAL_IDENTITY-06` | Phân tích hiệu quả của chiến lược dựa trên mục tiêu (digital identity, online profile, reputation) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FLEXBOX_GRID_LAYOUT-01` | Phân biệt hệ thống bố cục một chiều và hai chiều (flex, grid, layout, alignment) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FLEXBOX_GRID_LAYOUT-02` | Xác định trường hợp sử dụng phù hợp cho mỗi hệ thống (flex, grid, layout, alignment) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FLEXBOX_GRID_LAYOUT-03` | Sử dụng các thuộc tính điều chỉnh trục chính và trục chéo (flex, grid, layout, alignment) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FLEXBOX_GRID_LAYOUT-04` | Phân bố không gian giữa các phần tử con (flex, grid, layout, alignment) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FLEXBOX_GRID_LAYOUT-05` | Kết hợp hệ thống một chiều và hai chiều trong cùng một bố cục (flex, grid, layout, alignment) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FLEXBOX_GRID_LAYOUT-06` | Phân tích cấu trúc lồng nhau để đạt được bố cục mong muốn (flex, grid, layout, alignment) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CROSS_ORIGIN_SECURITY-01` | Mô tả cơ chế hạn chế truy cập giữa các nguồn gốc khác nhau (security, same-origin, cross-origin, CORS) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CROSS_ORIGIN_SECURITY-02` | Phân tích lý do bảo mật đằng sau chính sách cùng nguồn gốc (security, same-origin, cross-origin, CORS) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | Cấu hình quy tắc cho phép truy cập dựa trên nguồn gốc (security, same-origin, cross-origin, CORS) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | Kiểm tra nguồn gốc yêu cầu và áp dụng chính sách động (security, same-origin, cross-origin, CORS) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CROSS_ORIGIN_SECURITY-03` | Phân tích ma trận rủi ro dựa trên độ nhạy tài nguyên và mức độ tin cậy nguồn gốc (security, same-origin, cross-origin, CORS) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CROSS_ORIGIN_SECURITY-04` | So sánh kịch bản tấn công tiềm ẩn khi cấu hình CORS quá rộng (security, same-origin, cross-origin) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COLOR_THEORY-01` | Phân loại mô hình màu theo không gian màu và ứng dụng (color, palette, visual design, CMYK, RGB) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COLOR_THEORY-02` | So sánh đặc điểm của các mô hình màu phổ biến (color, palette, visual design, CMYK, RGB) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COLOR_THEORY-03` | Lựa chọn màu sắc dựa trên vòng tròn màu và quy tắc hài hòa (color, palette, visual design, CMYK, RGB) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COLOR_THEORY-04` | Xây dựng bảng màu bằng cách kết hợp các màu theo tỷ lệ và độ tương phản (color, palette, visual design, CMYK, RGB) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COLOR_THEORY-05` | Đánh giá cảm xúc gợi lên từ màu sắc dựa trên bối cảnh văn hóa và ngữ cảnh sử dụng (color, palette, visual design, CMYK, RGB) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-COLOR_THEORY-06` | So sánh hiệu ứng của các bảng màu khác nhau lên hành vi người dùng (color, palette, visual design, CMYK, RGB) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | Mô tả đặc điểm của hàm như một giá trị có thể gán, truyền và trả về (lambda, closure, higher-order function, first-class) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | So sánh hàm với các kiểu dữ liệu khác về khả năng thao tác (lambda, closure, higher-order function, first-class) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | Sử dụng hàm nhận hàm khác làm đối số để thực hiện thao tác trên từng phần tử (lambda, closure, higher-order function, first-class) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | Xây dựng pipeline xử lý dữ liệu bằng cách kết hợp các hàm biến đổi (lambda, closure, higher-order function, first-class) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | Tạo hàm bao bọc nhận một hàm và trả về hàm mới với hành vi mở rộng (lambda, closure, higher-order function, first-class) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | Thiết kế hàm nhận hàm xử lý và áp dụng nó trong một ngữ cảnh cụ thể (lambda, closure, higher-order function, first-class) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |

**→ Action:** Bổ sung/sửa marr_test_note để nhắc rõ ràng ≥ 2 ngôn ngữ khác nhau (ví dụ: 'Áp dụng được cho Python vì... và Swift vì...').
---

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

**4 candidate(s) từ Master Tree:**

| Score | Code | Name | Matching Keywords |
|---|---|---|---|
| 5.2 | `POLYGON_MESH` | Polygonal Mesh (Vertex, Edge, Face) | `edge`, `face` |
| 2.3 | `ARDUINO_BASICS` | Microcontroller Sketch Structure | `loop`, `structure` |
| 2.3 | `STACK_OPERATIONS` | Stack Operations (Push/Pop) | `stack` |
| 2.3 | `USER_PERSONAS` | Creating User Personas | `persona`, `user` |

**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`.