# CIO Preview — Marr Test Results

_Generated: 2026-07-29 22:11 | 13 CIOs_

> Kiểm tra cột **Marr Test** — nếu trống hoặc chỉ nhắc 1 ngôn ngữ → CIO cần viết lại

| Code | Name | Parent ULO | Bloom | Dimension | Marr Test Note |
|------|------|-----------|-------|-----------|----------------|
| `CIO-PROJECT_ASSETS_MANAGEMENT-01` | Phân loại tài nguyên dự án theo loại | `ULO-PROJECT_ASSETS_MANAGEMENT-01` (Nhận biết các loại tài nguyên trong dự án) | UNDERSTAND | CONCEPTUAL | Marr test: Mô tả này khớp với cả Swift (Asset Catalog phân loại theo loại) và Ja |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | Thêm tài nguyên vào cấu trúc dự án | `ULO-PROJECT_ASSETS_MANAGEMENT-03` (Thêm và sử dụng tài nguyên trong dự án) | APPLY | PROCEDURAL | Marr test: Swift: thêm file vào Assets.xcassets; JavaScript: thêm file vào thư m |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | Tham chiếu tài nguyên bằng tên định danh | `ULO-PROJECT_ASSETS_MANAGEMENT-03` (Thêm và sử dụng tài nguyên trong dự án) | APPLY | PROCEDURAL | Marr test: Swift: Image('ten_hinh'); JavaScript: <img src='ten_hinh.png'>. Cả ha |
| `CIO-ARRAY_OPERATIONS-03-01` | Duyệt mảng và truy cập từng phần tử | `ULO-ARRAY_OPERATIONS-03` (Apply array traversal and modification) | APPLY | PROCEDURAL | Marr test: Swift: for (index, value) in array.enumerated(); JavaScript: array.fo |
| `CIO-ARRAY_OPERATIONS-03-02` | Sửa đổi mảng tại chỗ dựa trên điều kiện | `ULO-ARRAY_OPERATIONS-03` (Apply array traversal and modification) | APPLY | PROCEDURAL | Marr test: Swift: array[index] = newValue; JavaScript: array[index] = newValue.  |
| `CIO-WHILE_LOOP-03-01` | Lặp với điều kiện kiểm tra trước | `ULO-WHILE_LOOP-03` (Apply while loops for dynamic repetition) | APPLY | PROCEDURAL | Marr test: Swift: while condition { }; JavaScript: while (condition) { }. Cả hai |
| `CIO-WHILE_LOOP-03-02` | Lặp với điều kiện phụ thuộc đầu vào | `ULO-WHILE_LOOP-03` (Apply while loops for dynamic repetition) | APPLY | PROCEDURAL | Marr test: Swift: while userInput != 'quit' { ... }; JavaScript: while (data.len |
| `CIO-DECLARATIVE_UI_PARADIGM-03` | So sánh khai báo và mệnh lệnh trong xây dựng giao diện | `ULO-DECLARATIVE_UI_PARADIGM-03` (Phân tích sự khác biệt giữa khai báo và mệnh lệnh) | ANALYZE | CONCEPTUAL | Marr test: SwiftUI (declarative) vs UIKit (imperative); React (declarative) vs j |
| `CIO-UI_MODIFIERS_CONCEPT-03` | Áp dụng modifier theo chuỗi để tạo kiểu giao diện | `ULO-UI_MODIFIERS_CONCEPT-03` (Áp dụng UI Modifier để xây dựng giao diện) | APPLY | PROCEDURAL | Marr test: SwiftUI: Text('Hello').font(.title).padding(); Flutter: Container(dec |
| `CIO-EVENT_HANDLERS_CONCEPT-02` | Gắn hàm xử lý sự kiện tương tác | `ULO-EVENT_HANDLERS_CONCEPT-02` (Gắn event handler vào thành phần giao diện) | APPLY | PROCEDURAL | Marr test: SwiftUI: .onTapGesture { ... }; JavaScript: element.addEventListener( |
| `CIO-STATE_PROPERTY_WRAPPER-02` | Khai báo và cập nhật biến trạng thái có giám sát | `ULO-STATE_PROPERTY_WRAPPER-02` (Sử dụng @State để theo dõi và cập nhật trạng thái) | APPLY | PROCEDURAL | Marr test: SwiftUI: @State var count = 0; count += 1; React: const [count, setCo |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | Phân loại lỗi dựa trên thời điểm phát hiện | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` (Analyze code to classify errors) | ANALYZE | CONCEPTUAL | Marr test: Swift: lỗi cú pháp như thiếu dấu ngoặc (compile-time), runtime như in |
| `CIO-ERROR_MESSAGES_CONCEPT-02` | Giải thích thông báo lỗi dựa trên cấu trúc | `ULO-ERROR_MESSAGES_CONCEPT-02` (Giải thích thông báo lỗi) | UNDERSTAND | CONCEPTUAL | Marr test: Swift: 'Fatal error: Index out of range' -> hiểu là truy cập mảng ngo |

## Descriptions & Marr Tests

### `CIO-PROJECT_ASSETS_MANAGEMENT-01` ← `ULO-PROJECT_ASSETS_MANAGEMENT-01`
**Phân loại tài nguyên dự án theo loại**
> Người học có khả năng phân loại các tệp tài nguyên (hình ảnh, màu sắc, biểu tượng, font chữ) dựa trên thuộc tính loại (type) của chúng trong cấu trúc dự án.

**Marr Test:** Marr test: Mô tả này khớp với cả Swift (Asset Catalog phân loại theo loại) và JavaScript (thư mục assets phân loại theo loại file). Cả hai đều dùng khái niệm 'loại tài nguyên' mà không phụ thuộc cú pháp cụ thể.

### `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` ← `ULO-PROJECT_ASSETS_MANAGEMENT-03`
**Thêm tài nguyên vào cấu trúc dự án**
> Người học có khả năng thêm một tệp tài nguyên mới (hình ảnh, màu sắc) vào cấu trúc thư mục hoặc danh mục tài nguyên của dự án, đảm bảo tài nguyên có tên định danh duy nhất.

**Marr Test:** Marr test: Swift: thêm file vào Assets.xcassets; JavaScript: thêm file vào thư mục images/. Cả hai đều có bước đặt tên và đưa vào đúng vị trí. Mô tả trung tính, không gắn cú pháp.

### `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` ← `ULO-PROJECT_ASSETS_MANAGEMENT-03`
**Tham chiếu tài nguyên bằng tên định danh**
> Người học có khả năng tham chiếu một tài nguyên đã thêm vào dự án thông qua tên định danh của nó trong mã nguồn để sử dụng trong giao diện.

**Marr Test:** Marr test: Swift: Image('ten_hinh'); JavaScript: <img src='ten_hinh.png'>. Cả hai đều dùng tên file/asset để tham chiếu. Mô tả không chứa cú pháp cụ thể.

### `CIO-ARRAY_OPERATIONS-03-01` ← `ULO-ARRAY_OPERATIONS-03`
**Duyệt mảng và truy cập từng phần tử**
> Người học có khả năng duyệt qua từng phần tử của mảng, truy cập giá trị và chỉ số (nếu cần) để thực hiện một thao tác trên mỗi phần tử.

**Marr Test:** Marr test: Swift: for (index, value) in array.enumerated(); JavaScript: array.forEach((value, index) => ...). Cả hai đều có pattern lặp với chỉ số và giá trị. Mô tả trung tính.

### `CIO-ARRAY_OPERATIONS-03-02` ← `ULO-ARRAY_OPERATIONS-03`
**Sửa đổi mảng tại chỗ dựa trên điều kiện**
> Người học có khả năng thay đổi giá trị của các phần tử trong mảng dựa trên một điều kiện kiểm tra, bằng cách gán lại giá trị mới cho phần tử tại chỉ số tương ứng.

**Marr Test:** Marr test: Swift: array[index] = newValue; JavaScript: array[index] = newValue. Cả hai đều dùng chỉ số để gán. Mô tả không chứa cú pháp cụ thể.

### `CIO-WHILE_LOOP-03-01` ← `ULO-WHILE_LOOP-03`
**Lặp với điều kiện kiểm tra trước**
> Người học có khả năng lặp lại một khối lệnh cho đến khi một điều kiện động (phụ thuộc vào dữ liệu hoặc trạng thái) trở thành sai, với điều kiện được kiểm tra trước mỗi lần lặp.

**Marr Test:** Marr test: Swift: while condition { }; JavaScript: while (condition) { }. Cả hai đều có cấu trúc kiểm tra điều kiện trước. Mô tả trung tính.

### `CIO-WHILE_LOOP-03-02` ← `ULO-WHILE_LOOP-03`
**Lặp với điều kiện phụ thuộc đầu vào**
> Người học có khả năng xây dựng vòng lặp while mà điều kiện lặp phụ thuộc vào giá trị đầu vào hoặc kết quả tính toán trong thân vòng lặp, cho phép số lần lặp không xác định trước.

**Marr Test:** Marr test: Swift: while userInput != 'quit' { ... }; JavaScript: while (data.length > 0) { ... }. Cả hai đều dùng điều kiện động. Mô tả không gắn cú pháp.

### `CIO-DECLARATIVE_UI_PARADIGM-03` ← `ULO-DECLARATIVE_UI_PARADIGM-03`
**So sánh khai báo và mệnh lệnh trong xây dựng giao diện**
> Người học có khả năng phân tích sự khác biệt giữa hai cách tiếp cận: khai báo (mô tả trạng thái giao diện mong muốn) và mệnh lệnh (liệt kê các bước thay đổi giao diện), chỉ ra ưu nhược điểm của mỗi cách.

**Marr Test:** Marr test: SwiftUI (declarative) vs UIKit (imperative); React (declarative) vs jQuery (imperative). Cả hai cặp đều thể hiện cùng pattern: mô tả what vs how. Mô tả trung tính.

### `CIO-UI_MODIFIERS_CONCEPT-03` ← `ULO-UI_MODIFIERS_CONCEPT-03`
**Áp dụng modifier theo chuỗi để tạo kiểu giao diện**
> Người học có khả năng áp dụng một chuỗi các modifier lên một thành phần giao diện, mỗi modifier thay đổi một thuộc tính (kích thước, màu sắc, căn chỉnh) và trả về thành phần đã biến đổi.

**Marr Test:** Marr test: SwiftUI: Text('Hello').font(.title).padding(); Flutter: Container(decoration: BoxDecoration(...)); CSS: .class { font-size: 20px; padding: 10px; }. Cả ba đều dùng pattern modifier chain hoặc thuộc tính. Mô tả trung tính.

### `CIO-EVENT_HANDLERS_CONCEPT-02` ← `ULO-EVENT_HANDLERS_CONCEPT-02`
**Gắn hàm xử lý sự kiện tương tác**
> Người học có khả năng đăng ký một hàm (callback) để được thực thi khi một sự kiện tương tác cụ thể (nhấn, gõ phím, cử chỉ) xảy ra trên một thành phần giao diện.

**Marr Test:** Marr test: SwiftUI: .onTapGesture { ... }; JavaScript: element.addEventListener('click', handler). Cả hai đều gắn callback vào sự kiện. Mô tả trung tính.

### `CIO-STATE_PROPERTY_WRAPPER-02` ← `ULO-STATE_PROPERTY_WRAPPER-02`
**Khai báo và cập nhật biến trạng thái có giám sát**
> Người học có khả năng khai báo một biến trạng thái với giá trị khởi tạo, và cập nhật giá trị của biến đó để kích hoạt việc render lại giao diện tự động.

**Marr Test:** Marr test: SwiftUI: @State var count = 0; count += 1; React: const [count, setCount] = useState(0); setCount(count+1). Cả hai đều có biến đặc biệt khi thay đổi sẽ cập nhật UI. Mô tả trung tính.

### `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` ← `ULO-SYNTAX_VS_RUNTIME_ERRORS-03`
**Phân loại lỗi dựa trên thời điểm phát hiện**
> Người học có khả năng phân tích mã nguồn để xác định lỗi thuộc loại cú pháp (vi phạm quy tắc ngôn ngữ, phát hiện khi biên dịch) hay runtime (xảy ra khi thực thi chương trình).

**Marr Test:** Marr test: Swift: lỗi cú pháp như thiếu dấu ngoặc (compile-time), runtime như index out of range; JavaScript: SyntaxError (parse-time), TypeError (runtime). Cả hai đều phân loại dựa trên thời điểm. Mô tả trung tính.

### `CIO-ERROR_MESSAGES_CONCEPT-02` ← `ULO-ERROR_MESSAGES_CONCEPT-02`
**Giải thích thông báo lỗi dựa trên cấu trúc**
> Người học có khả năng đọc thông báo lỗi, xác định loại lỗi, nguyên nhân gốc rễ và vị trí xảy ra lỗi dựa trên các từ khóa và ngữ cảnh được cung cấp trong thông báo.

**Marr Test:** Marr test: Swift: 'Fatal error: Index out of range' -> hiểu là truy cập mảng ngoài phạm vi; JavaScript: 'Cannot read property x of undefined' -> hiểu là đối tượng undefined. Cả hai đều phân tích cấu trúc thông báo. Mô tả trung tính.
