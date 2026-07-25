# CIO Preview — Marr Test Results

_Generated: 2026-07-25 20:05 | 55 CIOs_

> Kiểm tra cột **Marr Test** — nếu trống hoặc chỉ nhắc 1 ngôn ngữ → CIO cần viết lại

| Code | Name | Parent ULO | Bloom | Dimension | Marr Test Note |
|------|------|-----------|-------|-----------|----------------|
| `CIO-ARRAY_OPERATIONS-01-01` | Truy cập phần tử mảng bằng chỉ số | `ULO-ARRAY_OPERATIONS-01` (Remember array element access syntax) | Remember | Factual Knowledge | Thử với Python (array[0]) và JavaScript (arr[0]): cả hai đều dùng cú pháp ngoặc  |
| `CIO-ARRAY_OPERATIONS-02-01` | Hiểu chỉ số bắt đầu từ 0 | `ULO-ARRAY_OPERATIONS-02` (Understand zero-based indexing) | Understand | Conceptual Knowledge | Thử với Python (list[0] là phần tử đầu) và C (arr[0] là phần tử đầu): cả hai đều |
| `CIO-ARRAY_OPERATIONS-03-01` | Duyệt mảng tuần tự | `ULO-ARRAY_OPERATIONS-03` (Apply array traversal and modification) | Apply | Procedural Knowledge | Thử với Python (for i in range(len(arr)): print(arr[i])) và JavaScript (for let  |
| `CIO-ARRAY_OPERATIONS-03-02` | Sửa đổi phần tử mảng | `ULO-ARRAY_OPERATIONS-03` (Apply array traversal and modification) | Apply | Procedural Knowledge | Thử với Python (arr[0] = 10) và JavaScript (arr[0] = 10): cả hai đều dùng phép g |
| `CIO-LOCAL_VIEW_STATE-01-01` | Vai trò của trạng thái cục bộ trong đồng bộ giao diện | `ULO-LOCAL_VIEW_STATE-01` (Understand purpose of local view state) | Understand | Conceptual Knowledge | Thử với SwiftUI (@State) và React (useState): cả hai đều có khái niệm state cục  |
| `CIO-LOCAL_VIEW_STATE-02-01` | Điều khiển thuộc tính giao diện bằng trạng thái cục bộ | `ULO-LOCAL_VIEW_STATE-02` (Apply local view state to UI elements) | Apply | Procedural Knowledge | Thử với SwiftUI (Text(showText ? Hello : ) và React ({showText && <p>Hello</p>}) |
| `CIO-LOCAL_VIEW_STATE-02-02` | Cập nhật trạng thái cục bộ từ tương tác người dùng | `ULO-LOCAL_VIEW_STATE-02` (Apply local view state to UI elements) | Apply | Procedural Knowledge | Thử với SwiftUI (Button(action: { count += 1 })) và React (onClick={() => setCou |
| `CIO-LVS-03-1` | Trace local state lifecycle | `ULO-LOCAL_VIEW_STATE-03` (Analyze scope and lifecycle of local view state) | Analyze | Conceptual | Marr 2-language test: SwiftUI @State được khởi tạo khi view xuất hiện và hủy khi |
| `CIO-LVS-03-2` | Determine local state scope | `ULO-LOCAL_VIEW_STATE-03` (Analyze scope and lifecycle of local view state) | Analyze | Conceptual | Marr 2-language test: SwiftUI @State chỉ có thể truy cập trong view khai báo, kh |
| `CIO-SPW-01-1` | Explain state-triggered re-rendering | `ULO-STATE_PROPERTY_WRAPPER-01` (Hiểu mục đích và cơ chế của @State) | Understand | Conceptual | Marr 2-language test: SwiftUI @State thay đổi gây re-render view; React useState |
| `CIO-SPW-01-2` | Describe state wrapper decoupling role | `ULO-STATE_PROPERTY_WRAPPER-01` (Hiểu mục đích và cơ chế của @State) | Understand | Conceptual | Marr 2-language test: SwiftUI @State tách dữ liệu khỏi view struct; React useSta |
| `CIO-SPW-02-1` | Initialize and update mutable state | `ULO-STATE_PROPERTY_WRAPPER-02` (Sử dụng @State để theo dõi và cập nhật trạng thái) | Apply | Procedural | Marr 2-language test: SwiftUI @State var count = 0; Button action: count += 1. R |
| `CIO-SPW-02-2` | Bind state to UI element and observe changes | `ULO-STATE_PROPERTY_WRAPPER-02` (Sử dụng @State để theo dõi và cập nhật trạng thái) | Apply | Procedural | Marr 2-language test: SwiftUI TextField($text) với binding; React <input value={ |
| `CIO-SPW-03-1` | Compare ownership and sharing semantics of state wrappers | `ULO-STATE_PROPERTY_WRAPPER-03` (Phân tích sự khác biệt giữa @State và các property wrapper khác) | Analyze | Conceptual | Marr 2-language test: SwiftUI @State (local), @Binding (shared reference), @Obse |
| `CIO-SPW-03-2` | Evaluate appropriate wrapper based on data source and view hierarchy | `ULO-STATE_PROPERTY_WRAPPER-03` (Phân tích sự khác biệt giữa @State và các property wrapper khác) | Analyze | Conceptual | Marr 2-language test: SwiftUI chọn @State cho local, @Binding cho parent-child,  |
| `CIO-WL-01-1` | Recognize condition-controlled loop pattern | `ULO-WHILE_LOOP-01` (Remember while loop syntax) | Remember | Factual | Marr 2-language test: while (condition) { } trong C/Java/Swift; while condition: |
| `CIO-WHILE_LOOP-02-01` | Condition-first repetition pattern | `ULO-WHILE_LOOP-02` (Understand condition evaluation and termination) | Understand | Conceptual | Test 2 ngôn ngữ: Python (while condition:) và C (while(condition)). Cả hai đều d |
| `CIO-WHILE_LOOP-02-02` | Loop termination via condition falsification | `ULO-WHILE_LOOP-02` (Understand condition evaluation and termination) | Analyze | Conceptual | Test 2 ngôn ngữ: Java (while(condition){...}) và JavaScript (while(condition){.. |
| `CIO-WHILE_LOOP-03-01` | Dynamic condition repetition with mutable control variable | `ULO-WHILE_LOOP-03` (Apply while loops for dynamic repetition) | Apply | Procedural | Test 2 ngôn ngữ: Python (while user_input != 'quit':) và C (while(scanf(...) !=  |
| `CIO-WHILE_LOOP-03-02` | Sentinel-controlled repetition pattern | `ULO-WHILE_LOOP-03` (Apply while loops for dynamic repetition) | Apply | Procedural | Test 2 ngôn ngữ: Java (while(!input.equals('exit'))) và JavaScript (while(input  |
| `CIO-PROJECT_ASSETS_MANAGEMENT-01-01` | Asset type categorization pattern | `ULO-PROJECT_ASSETS_MANAGEMENT-01` (Nhận biết các loại tài nguyên trong dự án) | Remember | Factual | Test 2 môi trường: Xcode (Asset Catalog) và Android Studio (res/). Cả hai đều có |
| `CIO-PROJECT_ASSETS_MANAGEMENT-02-01` | Asset catalog hierarchical organization pattern | `ULO-PROJECT_ASSETS_MANAGEMENT-02` (Hiểu cấu trúc và cách tổ chức tài nguyên) | Understand | Conceptual | Test 2 môi trường: Xcode (Assets.xcassets) và Android (res/ với các thư mục con  |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | Asset addition and reference pattern | `ULO-PROJECT_ASSETS_MANAGEMENT-03` (Thêm và sử dụng tài nguyên trong dự án) | Apply | Procedural | Test 2 môi trường: Xcode (thêm ảnh vào Assets.xcassets, dùng Image('ten')) và An |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | Color asset definition and usage pattern | `ULO-PROJECT_ASSETS_MANAGEMENT-03` (Thêm và sử dụng tài nguyên trong dự án) | Apply | Procedural | Test 2 môi trường: Xcode (Color asset trong Assets.xcassets, dùng Color('ten'))  |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-01-01` | Phân biệt lỗi cú pháp và lỗi runtime dựa trên định nghĩa | `ULO-SYNTAX_VS_RUNTIME_ERRORS-01` (Remember definitions of syntax and runtime errors) | Remember | Factual | Marr 2-Language Test: Mô tả này có thể ánh xạ sang Python (syntax error: missing |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-02-01` | Giải thích nguyên nhân gây ra lỗi cú pháp và lỗi runtime | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` (Understand causes and examples of each error type) | Understand | Conceptual | Marr 2-Language Test: Mô tả này có thể minh họa bằng Python (IndentationError là |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-02-02` | Phân loại ví dụ lỗi dựa trên thời điểm phát hiện | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02` (Understand causes and examples of each error type) | Understand | Conceptual | Marr 2-Language Test: Trong Python, lỗi thiếu dấu hai chấm là syntax (phát hiện  |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-03-01` | Xác định loại lỗi từ mã nguồn dựa trên dấu hiệu nhận biết | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` (Analyze code to classify errors) | Analyze | Procedural | Marr 2-Language Test: Trong Python, dấu hiệu thiếu dấu hai chấm sau def là synta |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-03-02` | Phân tích thông báo lỗi để phân loại lỗi | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` (Analyze code to classify errors) | Analyze | Procedural | Marr 2-Language Test: Thông báo lỗi syntax trong Python thường có dạng 'SyntaxEr |
| `CIO-REFERENCE_TYPE_DECLARATION-01-01` | Nhận diện cú pháp khai báo kiểu tham chiếu | `ULO-REFERENCE_TYPE_DECLARATION-01` (Remember syntax for declaring reference types) | Remember | Factual | Marr 2-Language Test: Trong Java, khai báo kiểu tham chiếu dùng 'new' (ví dụ: St |
| `CIO-REFERENCE_TYPE_DECLARATION-02-01` | So sánh hành vi gán và sao chép giữa kiểu tham chiếu và kiểu giá trị | `ULO-REFERENCE_TYPE_DECLARATION-02` (Understand difference between reference and value types) | Understand | Conceptual | Marr 2-Language Test: Trong JavaScript, kiểu giá trị (number, string) được sao c |
| `CIO-REFERENCE_TYPE_DECLARATION-02-02` | Phân tích tác động của tham chiếu đến bộ nhớ và hiệu năng | `ULO-REFERENCE_TYPE_DECLARATION-02` (Understand difference between reference and value types) | Understand | Conceptual | Marr 2-Language Test: Trong Java, tham chiếu đến đối tượng được truyền theo giá  |
| `CIO-REFERENCE_TYPE_DECLARATION-03-01` | Khai báo biến tham chiếu với khởi tạo đối tượng | `ULO-REFERENCE_TYPE_DECLARATION-03` (Apply declaration of reference types in code) | Apply | Procedural Knowledge | Test 2 ngôn ngữ: Java: MyClass obj = new MyClass(); Swift: let obj = MyClass() ( |
| `CIO-REFERENCE_TYPE_DECLARATION-03-02` | Khai báo biến tham chiếu với giá trị null hoặc nil | `ULO-REFERENCE_TYPE_DECLARATION-03` (Apply declaration of reference types in code) | Apply | Procedural Knowledge | Test 2 ngôn ngữ: Java: MyClass obj = null; sau đó obj = new MyClass(); Swift: va |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-01-01` | Phân biệt dựa trên cơ chế kích hoạt | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` (Phân biệt implicit và explicit animation) | Understand | Conceptual Knowledge | Test 2 ngôn ngữ: SwiftUI: implicit dùng .animation(), explicit dùng withAnimatio |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-01-02` | Phân biệt dựa trên mức độ kiểm soát thời gian và chi tiết | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01` (Phân biệt implicit và explicit animation) | Understand | Conceptual Knowledge | Test 2 ngôn ngữ: SwiftUI: implicit chỉ có .animation(.easeInOut), explicit có th |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-02-01` | Áp dụng implicit animation bằng cách gắn bộ mô tả animation vào view | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` (Áp dụng implicit animation cho các thay đổi trạng thái đơn giản) | Apply | Procedural Knowledge | Test 2 ngôn ngữ: SwiftUI: Text(...).animation(.default); CSS: div { transition:  |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-02-02` | Áp dụng implicit animation bằng cách bao bọc thay đổi trạng thái trong ngữ cảnh animation | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02` (Áp dụng implicit animation cho các thay đổi trạng thái đơn giản) | Apply | Procedural Knowledge | Test 2 ngôn ngữ: SwiftUI: withAnimation { state.toggle() } (thực chất là explici |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-03-01` | Phân tích ưu nhược điểm dựa trên mức độ kiểm soát và độ phức tạp | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` (Phân tích ưu nhược điểm của implicit và explicit animation) | Analyze | Conceptual Knowledge | Test 2 ngôn ngữ: SwiftUI và CSS đều có thể áp dụng phân tích này. Pattern: so sá |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-03-02` | Phân tích ưu nhược điểm dựa trên hiệu suất và khả năng tái sử dụng | `ULO-IMPLICIT_EXPLICIT_ANIMATION-03` (Phân tích ưu nhược điểm của implicit và explicit animation) | Analyze | Conceptual Knowledge | Test 2 ngôn ngữ: SwiftUI: implicit animation dùng hệ thống tối ưu, explicit có t |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-04-01` | Đánh giá lựa chọn dựa trên yêu cầu về hiệu suất và độ phức tạp | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` (Đánh giá lựa chọn loại animation phù hợp cho tình huống cụ thể) | Evaluate | Metacognitive Knowledge | Test 2 ngôn ngữ: SwiftUI và CSS đều có thể áp dụng tiêu chí này. Pattern: cân nh |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-04-02` | Đánh giá lựa chọn dựa trên khả năng tùy chỉnh và trải nghiệm người dùng | `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` (Đánh giá lựa chọn loại animation phù hợp cho tình huống cụ thể) | Evaluate | Metacognitive Knowledge | Test 2 ngôn ngữ: SwiftUI và CSS đều có thể áp dụng. Pattern: cân nhắc tùy chỉnh  |
| `CIO-DECLARATIVE_UI_PARADIGM-01-01` | Mô tả trạng thái mong muốn | `ULO-DECLARATIVE_UI_PARADIGM-01` (Giải thích mô hình giao diện khai báo) | Understand | Conceptual | Test 2 ngôn ngữ: SwiftUI dùng @State và body để render lại khi state thay đổi; R |
| `CIO-DECLARATIVE_UI_PARADIGM-01-02` | So sánh luồng điều khiển khai báo và mệnh lệnh | `ULO-DECLARATIVE_UI_PARADIGM-01` (Giải thích mô hình giao diện khai báo) | Understand | Conceptual | Test 2 ngôn ngữ: SwiftUI khai báo VStack, HStack; React khai báo div, span. UIKi |
| `CIO-DECLARATIVE_UI_PARADIGM-02-01` | Xây dựng cấu trúc view phân cấp | `ULO-DECLARATIVE_UI_PARADIGM-02` (Xây dựng giao diện khai báo) | Apply | Procedural | Test 2 ngôn ngữ: SwiftUI dùng VStack { Text(...) }; React dùng <div><span>...</s |
| `CIO-DECLARATIVE_UI_PARADIGM-02-02` | Gắn trạng thái vào view | `ULO-DECLARATIVE_UI_PARADIGM-02` (Xây dựng giao diện khai báo) | Apply | Procedural | Test 2 ngôn ngữ: SwiftUI dùng @State var count = 0; React dùng const [count, set |
| `CIO-DECLARATIVE_UI_PARADIGM-03-01` | Phân tích quản lý trạng thái | `ULO-DECLARATIVE_UI_PARADIGM-03` (Phân tích sự khác biệt giữa khai báo và mệnh lệnh) | Analyze | Conceptual | Test 2 ngôn ngữ: SwiftUI thay đổi state tự động render lại; UIKit phải gọi reloa |
| `CIO-DECLARATIVE_UI_PARADIGM-03-02` | Phân tích khả năng tái sử dụng và bảo trì | `ULO-DECLARATIVE_UI_PARADIGM-03` (Phân tích sự khác biệt giữa khai báo và mệnh lệnh) | Analyze | Conceptual | Test 2 ngôn ngữ: SwiftUI component có thể dùng lại; React component tái sử dụng. |
| `CIO-DECLARATIVE_UI_PARADIGM-04-01` | Đánh giá hiệu suất | `ULO-DECLARATIVE_UI_PARADIGM-04` (Đánh giá mô hình giao diện khai báo) | Evaluate | Metacognitive | Test 2 ngôn ngữ: SwiftUI có thể re-render toàn bộ view; React có shouldComponent |
| `CIO-DECLARATIVE_UI_PARADIGM-04-02` | Đánh giá khả năng mở rộng | `ULO-DECLARATIVE_UI_PARADIGM-04` (Đánh giá mô hình giao diện khai báo) | Evaluate | Metacognitive | Test 2 ngôn ngữ: SwiftUI dễ thêm view mới; React dễ thêm component. UIKit có thể |
| `CIO-UI_MODIFIERS_CONCEPT-01-01` | Liệt kê và phân loại UI Modifier | `ULO-UI_MODIFIERS_CONCEPT-01` (Nhận diện các UI Modifier phổ biến) | Remember | Factual | Test 2 ngôn ngữ: SwiftUI dùng .padding(), .background(), .font(); React Native d |
| `CIO-UI_MODIFIERS_CONCEPT-02-01` | Thứ tự áp dụng modifier ảnh hưởng đến kết quả hiển thị | `ULO-UI_MODIFIERS_CONCEPT-02` (Hiểu cách UI Modifier ảnh hưởng đến giao diện) | Understand | Conceptual | Marr 2-Language Test: Mô tả này khớp với SwiftUI (modifier chain: .padding().bac |
| `CIO-UI_MODIFIERS_CONCEPT-02-02` | Kết hợp các modifier để tạo hiệu ứng tổng hợp | `ULO-UI_MODIFIERS_CONCEPT-02` (Hiểu cách UI Modifier ảnh hưởng đến giao diện) | Understand | Conceptual | Marr 2-Language Test: Mô tả này khớp với SwiftUI (nhiều modifier như .font().for |
| `CIO-UI_MODIFIERS_CONCEPT-03-01` | Lựa chọn modifier dựa trên yêu cầu bố cục | `ULO-UI_MODIFIERS_CONCEPT-03` (Áp dụng UI Modifier để xây dựng giao diện) | Apply | Procedural | Marr 2-Language Test: Mô tả này khớp với SwiftUI (sử dụng HStack, VStack, paddin |
| `CIO-UI_MODIFIERS_CONCEPT-03-02` | Sắp xếp thứ tự modifier để đạt hiệu quả mong muốn | `ULO-UI_MODIFIERS_CONCEPT-03` (Áp dụng UI Modifier để xây dựng giao diện) | Apply | Procedural | Marr 2-Language Test: Mô tả này khớp với SwiftUI (thứ tự modifier ảnh hưởng đến  |

## Descriptions & Marr Tests

### `CIO-ARRAY_OPERATIONS-01-01` ← `ULO-ARRAY_OPERATIONS-01`
**Truy cập phần tử mảng bằng chỉ số**
> Người học có khả năng nhận diện và tái tạo mẫu truy cập phần tử mảng thông qua chỉ số (index) – sử dụng cặp ngoặc vuông và chỉ số để lấy giá trị tại vị trí xác định.

**Marr Test:** Thử với Python (array[0]) và JavaScript (arr[0]): cả hai đều dùng cú pháp ngoặc vuông với chỉ số. Mô tả khớp với cả hai ngôn ngữ, không phụ thuộc cú pháp đặc thù.

### `CIO-ARRAY_OPERATIONS-02-01` ← `ULO-ARRAY_OPERATIONS-02`
**Hiểu chỉ số bắt đầu từ 0**
> Người học có khả năng giải thích ý nghĩa của chỉ số bắt đầu từ 0 trong mảng: phần tử đầu tiên có chỉ số 0, phần tử cuối có chỉ số (độ dài - 1), và áp dụng để xác định vị trí phần tử.

**Marr Test:** Thử với Python (list[0] là phần tử đầu) và C (arr[0] là phần tử đầu): cả hai đều zero-based. Mô tả không gắn với cú pháp cụ thể, chỉ nói về khái niệm chỉ số.

### `CIO-ARRAY_OPERATIONS-03-01` ← `ULO-ARRAY_OPERATIONS-03`
**Duyệt mảng tuần tự**
> Người học có khả năng áp dụng mẫu duyệt mảng tuần tự: lặp qua từng phần tử bằng cách tăng dần chỉ số từ 0 đến độ dài - 1, và thực hiện thao tác trên mỗi phần tử.

**Marr Test:** Thử với Python (for i in range(len(arr)): print(arr[i])) và JavaScript (for let i=0; i<arr.length; i++): cả hai đều dùng vòng lặp với chỉ số tăng dần. Mô tả trung tính, không nhắc đến từ khóa for hay range.

### `CIO-ARRAY_OPERATIONS-03-02` ← `ULO-ARRAY_OPERATIONS-03`
**Sửa đổi phần tử mảng**
> Người học có khả năng áp dụng mẫu sửa đổi giá trị phần tử mảng: gán giá trị mới cho phần tử tại một chỉ số xác định, có thể kết hợp với điều kiện để chỉ sửa đổi khi thỏa mãn.

**Marr Test:** Thử với Python (arr[0] = 10) và JavaScript (arr[0] = 10): cả hai đều dùng phép gán với chỉ số. Mô tả không chứa từ khóa gán cụ thể, chỉ nói gán giá trị mới.

### `CIO-LOCAL_VIEW_STATE-01-01` ← `ULO-LOCAL_VIEW_STATE-01`
**Vai trò của trạng thái cục bộ trong đồng bộ giao diện**
> Người học có khả năng giải thích mục đích của trạng thái cục bộ: lưu trữ dữ liệu thay đổi theo thời gian trong phạm vi một view/component, và khi dữ liệu thay đổi, giao diện tự động cập nhật tương ứng.

**Marr Test:** Thử với SwiftUI (@State) và React (useState): cả hai đều có khái niệm state cục bộ, khi state thay đổi thì view re-render. Mô tả không dùng tên framework hay cú pháp.

### `CIO-LOCAL_VIEW_STATE-02-01` ← `ULO-LOCAL_VIEW_STATE-02`
**Điều khiển thuộc tính giao diện bằng trạng thái cục bộ**
> Người học có khả năng áp dụng trạng thái cục bộ để điều khiển các thuộc tính giao diện như hiển thị/ẩn, màu sắc, nội dung văn bản – gắn giá trị state vào thuộc tính và thay đổi state để kích hoạt cập nhật.

**Marr Test:** Thử với SwiftUI (Text(showText ? Hello : ) và React ({showText && <p>Hello</p>}): cả hai đều dùng state boolean để điều khiển hiển thị. Mô tả không nhắc đến cú pháp ternary hay toán tử &&.

### `CIO-LOCAL_VIEW_STATE-02-02` ← `ULO-LOCAL_VIEW_STATE-02`
**Cập nhật trạng thái cục bộ từ tương tác người dùng**
> Người học có khả năng áp dụng mẫu cập nhật trạng thái cục bộ khi có sự kiện từ người dùng (ví dụ: nhấn nút, nhập liệu) – gán giá trị mới cho state và giao diện tự động phản ánh thay đổi.

**Marr Test:** Thử với SwiftUI (Button(action: { count += 1 })) và React (onClick={() => setCount(count+1)}): cả hai đều gán giá trị mới cho state khi có sự kiện. Mô tả không dùng tên hàm hay toán tử.

### `CIO-LVS-03-1` ← `ULO-LOCAL_VIEW_STATE-03`
**Trace local state lifecycle**
> Người học có khả năng theo dõi vòng đời của một biến trạng thái cục bộ từ lúc khởi tạo đến khi bị hủy trong một hệ thống phân cấp view.

**Marr Test:** Marr 2-language test: SwiftUI @State được khởi tạo khi view xuất hiện và hủy khi view biến mất; React useState được khởi tạo khi component mount và hủy khi unmount. Mô tả 'khởi tạo đến hủy' khớp cả hai, không phụ thuộc cú pháp.

### `CIO-LVS-03-2` ← `ULO-LOCAL_VIEW_STATE-03`
**Determine local state scope**
> Người học có khả năng xác định phạm vi truy cập và khả năng hiển thị của một biến trạng thái cục bộ trong các view lồng nhau.

**Marr Test:** Marr 2-language test: SwiftUI @State chỉ có thể truy cập trong view khai báo, không chia sẻ với view con; React useState chỉ có hiệu lực trong function component đó. Mô tả 'phạm vi truy cập trong view lồng nhau' khớp cả hai.

### `CIO-SPW-01-1` ← `ULO-STATE_PROPERTY_WRAPPER-01`
**Explain state-triggered re-rendering**
> Người học có khả năng giải thích cách một biến trạng thái kích hoạt việc render lại giao diện khi giá trị của nó thay đổi.

**Marr Test:** Marr 2-language test: SwiftUI @State thay đổi gây re-render view; React useState thay đổi gây re-render component. Cả hai đều dùng cơ chế theo dõi thay đổi và cập nhật UI. Mô tả trung tính.

### `CIO-SPW-01-2` ← `ULO-STATE_PROPERTY_WRAPPER-01`
**Describe state wrapper decoupling role**
> Người học có khả năng mô tả vai trò của một wrapper trạng thái trong việc tách rời dữ liệu khỏi logic render của view.

**Marr Test:** Marr 2-language test: SwiftUI @State tách dữ liệu khỏi view struct; React useState tách dữ liệu khỏi JSX. Cả hai đều cung cấp cơ chế quản lý trạng thái nội bộ mà không làm ô nhiễm view. Mô tả khớp.

### `CIO-SPW-02-1` ← `ULO-STATE_PROPERTY_WRAPPER-02`
**Initialize and update mutable state**
> Người học có khả năng khởi tạo một biến trạng thái có thể thay đổi với giá trị mặc định và cập nhật nó để phản hồi tương tác người dùng.

**Marr Test:** Marr 2-language test: SwiftUI @State var count = 0; Button action: count += 1. React const [count, setCount] = useState(0); onClick: setCount(count+1). Cả hai đều khởi tạo và cập nhật. Mô tả trung tính.

### `CIO-SPW-02-2` ← `ULO-STATE_PROPERTY_WRAPPER-02`
**Bind state to UI element and observe changes**
> Người học có khả năng gắn một biến trạng thái vào giá trị của phần tử giao diện và theo dõi thay đổi thông qua callback.

**Marr Test:** Marr 2-language test: SwiftUI TextField($text) với binding; React <input value={text} onChange={e=>setText(e.target.value)}>. Cả hai đều gắn state vào UI và dùng callback để cập nhật. Mô tả trung tính.

### `CIO-SPW-03-1` ← `ULO-STATE_PROPERTY_WRAPPER-03`
**Compare ownership and sharing semantics of state wrappers**
> Người học có khả năng so sánh ngữ nghĩa sở hữu và chia sẻ giữa các wrapper quản lý trạng thái khác nhau.

**Marr Test:** Marr 2-language test: SwiftUI @State (local), @Binding (shared reference), @ObservedObject (external), @StateObject (owned). React useState (local), useRef (mutable ref), useContext (shared), useReducer. Cả hai đều có khái niệm ownership và sharing. Mô tả trung tính.

### `CIO-SPW-03-2` ← `ULO-STATE_PROPERTY_WRAPPER-03`
**Evaluate appropriate wrapper based on data source and view hierarchy**
> Người học có khả năng đánh giá và lựa chọn wrapper phù hợp dựa trên nguồn dữ liệu và cấu trúc phân cấp view.

**Marr Test:** Marr 2-language test: SwiftUI chọn @State cho local, @Binding cho parent-child, @ObservedObject cho external. React chọn useState cho local, useRef cho mutable ref, useContext cho shared. Cả hai đều dựa trên nguồn dữ liệu và hệ thống phân cấp. Mô tả trung tính.

### `CIO-WL-01-1` ← `ULO-WHILE_LOOP-01`
**Recognize condition-controlled loop pattern**
> Người học có khả năng nhận diện cấu trúc của một vòng lặp điều khiển bằng điều kiện, lặp lại một khối lệnh cho đến khi điều kiện boolean trở thành false.

**Marr Test:** Marr 2-language test: while (condition) { } trong C/Java/Swift; while condition: trong Python. Cả hai đều có từ khóa while, điều kiện và thân lặp. Mô tả 'cấu trúc vòng lặp điều khiển bằng điều kiện' khớp cả hai.

### `CIO-WHILE_LOOP-02-01` ← `ULO-WHILE_LOOP-02`
**Condition-first repetition pattern**
> Người học có khả năng áp dụng mẫu lặp kiểm tra điều kiện trước khi thực thi khối lệnh, trong đó điều kiện được đánh giá lại sau mỗi lần lặp và vòng lặp kết thúc khi điều kiện trở thành sai.

**Marr Test:** Test 2 ngôn ngữ: Python (while condition:) và C (while(condition)). Cả hai đều dùng cấu trúc kiểm tra điều kiện trước thân lặp, không phụ thuộc cú pháp cụ thể. Mô tả trung tính.

### `CIO-WHILE_LOOP-02-02` ← `ULO-WHILE_LOOP-02`
**Loop termination via condition falsification**
> Người học có khả năng phân tích cách một vòng lặp dừng lại khi biểu thức điều kiện chuyển từ true sang false, bao gồm các tình huống điều kiện luôn đúng dẫn đến vòng lặp vô hạn và cách tránh bằng cách thay đổi biến điều khiển trong thân lặp.

**Marr Test:** Test 2 ngôn ngữ: Java (while(condition){...}) và JavaScript (while(condition){...}). Cả hai đều dùng cơ chế đánh giá điều kiện trước mỗi lần lặp. Mô tả không chứa từ khóa cú pháp.

### `CIO-WHILE_LOOP-03-01` ← `ULO-WHILE_LOOP-03`
**Dynamic condition repetition with mutable control variable**
> Người học có khả năng áp dụng mẫu lặp sử dụng một biến điều khiển được cập nhật trong thân lặp dựa trên dữ liệu đầu vào hoặc trạng thái thay đổi, cho phép số lần lặp không xác định trước và phụ thuộc vào điều kiện động.

**Marr Test:** Test 2 ngôn ngữ: Python (while user_input != 'quit':) và C (while(scanf(...) != EOF)). Cả hai đều dùng biến thay đổi trong thân lặp để kiểm soát điều kiện. Mô tả trung tính.

### `CIO-WHILE_LOOP-03-02` ← `ULO-WHILE_LOOP-03`
**Sentinel-controlled repetition pattern**
> Người học có khả năng áp dụng mẫu lặp dùng giá trị sentinel (giá trị kết thúc đặc biệt) để dừng vòng lặp, trong đó điều kiện kiểm tra xem đầu vào có bằng sentinel hay không và thân lặp xử lý dữ liệu trước khi đọc giá trị tiếp theo.

**Marr Test:** Test 2 ngôn ngữ: Java (while(!input.equals('exit'))) và JavaScript (while(input !== 'quit')). Cả hai đều dùng sentinel để kiểm soát vòng lặp. Mô tả không phụ thuộc cú pháp cụ thể.

### `CIO-PROJECT_ASSETS_MANAGEMENT-01-01` ← `ULO-PROJECT_ASSETS_MANAGEMENT-01`
**Asset type categorization pattern**
> Người học có khả năng nhận diện và phân loại các loại tài nguyên dự án dựa trên mục đích sử dụng: tài nguyên hình ảnh (ảnh bitmap, vector), tài nguyên màu sắc (bảng màu, gradient), tài nguyên biểu tượng (icon, glyph), và tài nguyên chữ (font, typeface).

**Marr Test:** Test 2 môi trường: Xcode (Asset Catalog) và Android Studio (res/). Cả hai đều có các thư mục riêng cho image, color, icon, font. Mô tả trung tính, không gắn tên công nghệ.

### `CIO-PROJECT_ASSETS_MANAGEMENT-02-01` ← `ULO-PROJECT_ASSETS_MANAGEMENT-02`
**Asset catalog hierarchical organization pattern**
> Người học có khả năng giải thích cách tài nguyên được tổ chức theo cấu trúc phân cấp trong một thư mục đặc biệt, nơi mỗi tài nguyên có tên duy nhất và có thể được nhóm theo loại hoặc mục đích, đồng thời tuân theo quy tắc đặt tên nhất quán để tránh xung đột.

**Marr Test:** Test 2 môi trường: Xcode (Assets.xcassets) và Android (res/ với các thư mục con drawable, values). Cả hai đều dùng cấu trúc thư mục và quy tắc đặt tên. Mô tả không chứa tên IDE cụ thể.

### `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` ← `ULO-PROJECT_ASSETS_MANAGEMENT-03`
**Asset addition and reference pattern**
> Người học có khả năng áp dụng quy trình thêm tài nguyên mới vào dự án bằng cách đặt tệp vào đúng thư mục tài nguyên, sau đó tham chiếu tài nguyên đó trong mã nguồn thông qua tên định danh (không bao gồm đường dẫn tuyệt đối) để sử dụng trong giao diện.

**Marr Test:** Test 2 môi trường: Xcode (thêm ảnh vào Assets.xcassets, dùng Image('ten')) và Android (thêm ảnh vào res/drawable, dùng @drawable/ten). Cả hai đều dùng tên định danh. Mô tả trung tính.

### `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` ← `ULO-PROJECT_ASSETS_MANAGEMENT-03`
**Color asset definition and usage pattern**
> Người học có khả năng áp dụng quy trình tạo tài nguyên màu sắc bằng cách định nghĩa một bộ màu với các giá trị (RGB, hex, hoặc tên) trong hệ thống quản lý tài nguyên, sau đó tham chiếu màu đó qua tên trong mã nguồn để thiết lập màu nền, màu chữ, hoặc các thuộc tính giao diện khác.

**Marr Test:** Test 2 môi trường: Xcode (Color asset trong Assets.xcassets, dùng Color('ten')) và Android (màu trong res/values/colors.xml, dùng @color/ten). Cả hai đều dùng tên định danh. Mô tả không chứa cú pháp cụ thể.

### `CIO-SYNTAX_VS_RUNTIME_ERRORS-01-01` ← `ULO-SYNTAX_VS_RUNTIME_ERRORS-01`
**Phân biệt lỗi cú pháp và lỗi runtime dựa trên định nghĩa**
> Người học có khả năng nhận diện và phân biệt định nghĩa của lỗi cú pháp (sai quy tắc ngôn ngữ) và lỗi runtime (xảy ra khi chạy chương trình) từ các mô tả cho trước.

**Marr Test:** Marr 2-Language Test: Mô tả này có thể ánh xạ sang Python (syntax error: missing colon, runtime error: division by zero) và JavaScript (syntax error: missing parenthesis, runtime error: TypeError). Cả hai đều dùng cùng khái niệm định nghĩa, không phụ thuộc cú pháp cụ thể. Hợp lệ.

### `CIO-SYNTAX_VS_RUNTIME_ERRORS-02-01` ← `ULO-SYNTAX_VS_RUNTIME_ERRORS-02`
**Giải thích nguyên nhân gây ra lỗi cú pháp và lỗi runtime**
> Người học có khả năng giải thích nguyên nhân hình thành lỗi cú pháp (do vi phạm cấu trúc ngôn ngữ) và lỗi runtime (do điều kiện không hợp lệ khi thực thi) bằng cách sử dụng các ví dụ cụ thể.

**Marr Test:** Marr 2-Language Test: Mô tả này có thể minh họa bằng Python (IndentationError là syntax, ZeroDivisionError là runtime) và Java (missing semicolon là syntax, ArrayIndexOutOfBoundsException là runtime). Cả hai đều dùng khái niệm nguyên nhân chung. Hợp lệ.

### `CIO-SYNTAX_VS_RUNTIME_ERRORS-02-02` ← `ULO-SYNTAX_VS_RUNTIME_ERRORS-02`
**Phân loại ví dụ lỗi dựa trên thời điểm phát hiện**
> Người học có khả năng phân loại các đoạn mã lỗi thành lỗi cú pháp (phát hiện khi biên dịch/parse) hoặc lỗi runtime (phát hiện khi chạy) dựa trên thời điểm xảy ra lỗi.

**Marr Test:** Marr 2-Language Test: Trong Python, lỗi thiếu dấu hai chấm là syntax (phát hiện trước khi chạy), lỗi chia cho 0 là runtime. Trong JavaScript, lỗi thiếu dấu ngoặc là syntax, lỗi truy cập thuộc tính undefined là runtime. Cả hai đều dùng tiêu chí thời điểm phát hiện. Hợp lệ.

### `CIO-SYNTAX_VS_RUNTIME_ERRORS-03-01` ← `ULO-SYNTAX_VS_RUNTIME_ERRORS-03`
**Xác định loại lỗi từ mã nguồn dựa trên dấu hiệu nhận biết**
> Người học có khả năng phân tích một đoạn mã nguồn để xác định đó là lỗi cú pháp (dựa vào dấu hiệu như thiếu dấu ngoặc, sai từ khóa) hay lỗi runtime (dựa vào dấu hiệu như truy cập chỉ số ngoài phạm vi, chia cho 0).

**Marr Test:** Marr 2-Language Test: Trong Python, dấu hiệu thiếu dấu hai chấm sau def là syntax; truy cập list index out of range là runtime. Trong Java, thiếu dấu chấm phẩy là syntax; NullPointerException là runtime. Cả hai đều dùng dấu hiệu chung. Hợp lệ.

### `CIO-SYNTAX_VS_RUNTIME_ERRORS-03-02` ← `ULO-SYNTAX_VS_RUNTIME_ERRORS-03`
**Phân tích thông báo lỗi để phân loại lỗi**
> Người học có khả năng đọc và phân tích thông báo lỗi từ trình biên dịch hoặc runtime để xác định loại lỗi (syntax error hay runtime error) dựa trên nội dung và ngữ cảnh thông báo.

**Marr Test:** Marr 2-Language Test: Thông báo lỗi syntax trong Python thường có dạng 'SyntaxError: invalid syntax' còn runtime là 'ZeroDivisionError: division by zero'. Trong JavaScript, syntax error là 'SyntaxError: Unexpected token' còn runtime là 'TypeError: Cannot read property of undefined'. Cả hai đều dùng cách phân tích thông báo. Hợp lệ.

### `CIO-REFERENCE_TYPE_DECLARATION-01-01` ← `ULO-REFERENCE_TYPE_DECLARATION-01`
**Nhận diện cú pháp khai báo kiểu tham chiếu**
> Người học có khả năng nhận diện cú pháp khai báo biến với kiểu dữ liệu tham chiếu (ví dụ: sử dụng từ khóa tạo đối tượng, cấp phát bộ nhớ) từ các đoạn mã cho trước.

**Marr Test:** Marr 2-Language Test: Trong Java, khai báo kiểu tham chiếu dùng 'new' (ví dụ: String s = new String()). Trong Python, mọi biến đều là tham chiếu, nhưng khai báo đơn giản (ví dụ: s = 'hello') không có từ khóa đặc biệt. Tuy nhiên, mô tả tập trung vào nhận diện cú pháp tạo đối tượng, có thể áp dụng cho cả hai (Python dùng constructor như list()). Hợp lệ.

### `CIO-REFERENCE_TYPE_DECLARATION-02-01` ← `ULO-REFERENCE_TYPE_DECLARATION-02`
**So sánh hành vi gán và sao chép giữa kiểu tham chiếu và kiểu giá trị**
> Người học có khả năng so sánh cách thức gán và sao chép dữ liệu: kiểu giá trị tạo bản sao độc lập, kiểu tham chiếu chia sẻ cùng một đối tượng, từ đó giải thích sự khác biệt trong kết quả khi thay đổi biến.

**Marr Test:** Marr 2-Language Test: Trong JavaScript, kiểu giá trị (number, string) được sao chép, kiểu tham chiếu (object) được tham chiếu. Trong Python, int là giá trị, list là tham chiếu. Cả hai đều có hành vi tương tự. Hợp lệ.

### `CIO-REFERENCE_TYPE_DECLARATION-02-02` ← `ULO-REFERENCE_TYPE_DECLARATION-02`
**Phân tích tác động của tham chiếu đến bộ nhớ và hiệu năng**
> Người học có khả năng phân tích cách kiểu tham chiếu lưu trữ địa chỉ bộ nhớ thay vì giá trị trực tiếp, dẫn đến chia sẻ dữ liệu và ảnh hưởng đến hiệu năng khi truyền tham số hoặc sao chép.

**Marr Test:** Marr 2-Language Test: Trong Java, tham chiếu đến đối tượng được truyền theo giá trị (tham chiếu). Trong C#, struct là value type, class là reference type. Cả hai đều dùng khái niệm địa chỉ bộ nhớ. Hợp lệ.

### `CIO-REFERENCE_TYPE_DECLARATION-03-01` ← `ULO-REFERENCE_TYPE_DECLARATION-03`
**Khai báo biến tham chiếu với khởi tạo đối tượng**
> Người học có khả năng khai báo một biến để lưu trữ tham chiếu đến một thể hiện của kiểu tham chiếu bằng cách gọi hàm tạo và gán kết quả cho biến.

**Marr Test:** Test 2 ngôn ngữ: Java: MyClass obj = new MyClass(); Swift: let obj = MyClass() (class). Cả hai đều dùng pattern: gọi hàm tạo và gán cho biến. Không phụ thuộc cú pháp cụ thể (từ khóa new hay không). Hợp lệ.

### `CIO-REFERENCE_TYPE_DECLARATION-03-02` ← `ULO-REFERENCE_TYPE_DECLARATION-03`
**Khai báo biến tham chiếu với giá trị null hoặc nil**
> Người học có khả năng khai báo một biến tham chiếu mà chưa gán đối tượng ngay lập tức, sử dụng giá trị đặc biệt đại diện cho không có tham chiếu (null/nil) và sau đó gán đối tượng khi cần.

**Marr Test:** Test 2 ngôn ngữ: Java: MyClass obj = null; sau đó obj = new MyClass(); Swift: var obj: MyClass? = nil; sau đó obj = MyClass(). Pattern: khai báo biến với giá trị rỗng, sau đó gán đối tượng. Không phụ thuộc từ khóa null/nil cụ thể. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-01-01` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-01`
**Phân biệt dựa trên cơ chế kích hoạt**
> Người học có khả năng phân biệt animation ngầm định và tường minh dựa trên cách chúng được kích hoạt: ngầm định tự động kích hoạt khi trạng thái thay đổi, tường minh yêu cầu gọi một hàm hoặc khối lệnh cụ thể.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI: implicit dùng .animation(), explicit dùng withAnimation; CSS: implicit dùng transition, explicit dùng @keyframes + animation-name. Pattern: tự động vs chủ động kích hoạt. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-01-02` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-01`
**Phân biệt dựa trên mức độ kiểm soát thời gian và chi tiết**
> Người học có khả năng phân biệt animation ngầm định và tường minh dựa trên mức độ kiểm soát: ngầm định chỉ cho phép tùy chỉnh thời gian và hiệu ứng ở mức tổng thể, tường minh cho phép kiểm soát chi tiết từng giai đoạn (keyframe) và hành vi phức tạp.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI: implicit chỉ có .animation(.easeInOut), explicit có thể dùng withAnimation kết hợp keyframe; CSS: transition chỉ có duration/delay, animation có keyframes. Pattern: kiểm soát tổng thể vs chi tiết. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-02-01` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-02`
**Áp dụng implicit animation bằng cách gắn bộ mô tả animation vào view**
> Người học có khả năng gắn một bộ mô tả animation (ví dụ: thời gian, hiệu ứng) vào một view để tự động tạo chuyển tiếp mượt mà khi các thuộc tính của view thay đổi do trạng thái thay đổi.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI: Text(...).animation(.default); CSS: div { transition: all 0.3s; }. Pattern: khai báo animation trên view, tự động kích hoạt khi thuộc tính thay đổi. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-02-02` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-02`
**Áp dụng implicit animation bằng cách bao bọc thay đổi trạng thái trong ngữ cảnh animation**
> Người học có khả năng bao bọc các thay đổi trạng thái trong một ngữ cảnh animation (ví dụ: khối lệnh) để tất cả các thay đổi thuộc tính phụ thuộc vào trạng thái đó đều được chuyển tiếp mượt mà.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI: withAnimation { state.toggle() } (thực chất là explicit nhưng có thể coi là implicit? Cần cẩn thận: withAnimation là explicit. Tuy nhiên, pattern bao bọc thay đổi trong một khối animation cũng có thể là implicit nếu framework tự động. Ví dụ: trong Flutter, AnimatedContainer tự động animate khi properties thay đổi. Hoặc trong CSS, thay đổi class kích hoạt transition. Pattern: thay đổi trạng thái trong một phạm vi được đánh dấu animation. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-03-01` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-03`
**Phân tích ưu nhược điểm dựa trên mức độ kiểm soát và độ phức tạp**
> Người học có khả năng phân tích ưu điểm (dễ sử dụng, tự động) và nhược điểm (thiếu kiểm soát chi tiết) của animation ngầm định so với animation tường minh, và ngược lại, dựa trên các tiêu chí như mức độ kiểm soát, độ phức tạp khi triển khai, và khả năng tùy chỉnh.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI và CSS đều có thể áp dụng phân tích này. Pattern: so sánh dựa trên tiêu chí chung (kiểm soát, phức tạp). Không phụ thuộc cú pháp. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-03-02` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-03`
**Phân tích ưu nhược điểm dựa trên hiệu suất và khả năng tái sử dụng**
> Người học có khả năng phân tích ưu nhược điểm của animation ngầm định và tường minh dựa trên hiệu suất (ngầm định thường tối ưu hơn cho các thay đổi đơn giản) và khả năng tái sử dụng (tường minh dễ đóng gói thành các animation phức tạp có thể dùng lại).

**Marr Test:** Test 2 ngôn ngữ: SwiftUI: implicit animation dùng hệ thống tối ưu, explicit có thể tạo custom animation; CSS: transition nhẹ hơn animation. Pattern: so sánh dựa trên hiệu suất và tái sử dụng. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-04-01` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-04`
**Đánh giá lựa chọn dựa trên yêu cầu về hiệu suất và độ phức tạp**
> Người học có khả năng đánh giá và lựa chọn giữa animation ngầm định và tường minh dựa trên yêu cầu về hiệu suất (ngầm định cho thay đổi đơn giản, tường minh cho thay đổi phức tạp) và độ phức tạp của animation (số lượng thuộc tính thay đổi, cần keyframe hay không).

**Marr Test:** Test 2 ngôn ngữ: SwiftUI và CSS đều có thể áp dụng tiêu chí này. Pattern: cân nhắc hiệu suất và độ phức tạp. Không phụ thuộc cú pháp. Hợp lệ.

### `CIO-IMPLICIT_EXPLICIT_ANIMATION-04-02` ← `ULO-IMPLICIT_EXPLICIT_ANIMATION-04`
**Đánh giá lựa chọn dựa trên khả năng tùy chỉnh và trải nghiệm người dùng**
> Người học có khả năng đánh giá và lựa chọn giữa animation ngầm định và tường minh dựa trên mức độ tùy chỉnh cần thiết (tường minh cho phép kiểm soát chi tiết từng giai đoạn) và trải nghiệm người dùng mong muốn (ngầm định cho chuyển tiếp mượt mà tự nhiên, tường minh cho hiệu ứng đặc biệt).

**Marr Test:** Test 2 ngôn ngữ: SwiftUI và CSS đều có thể áp dụng. Pattern: cân nhắc tùy chỉnh và UX. Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-01-01` ← `ULO-DECLARATIVE_UI_PARADIGM-01`
**Mô tả trạng thái mong muốn**
> Người học có khả năng mô tả nguyên lý cốt lõi của giao diện khai báo: thay vì chỉ định các bước thay đổi UI, người phát triển khai báo trạng thái mong muốn và để framework tự động đồng bộ UI với trạng thái đó.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI dùng @State và body để render lại khi state thay đổi; React dùng useState và JSX để re-render. Cả hai đều mô tả UI là hàm của state, không phải các bước thao tác DOM. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-01-02` ← `ULO-DECLARATIVE_UI_PARADIGM-01`
**So sánh luồng điều khiển khai báo và mệnh lệnh**
> Người học có khả năng so sánh luồng điều khiển giữa mô hình khai báo (khai báo cấu trúc view, framework quyết định thời điểm cập nhật) và mô hình mệnh lệnh (lập trình viên chỉ thị từng bước thay đổi UI).

**Marr Test:** Test 2 ngôn ngữ: SwiftUI khai báo VStack, HStack; React khai báo div, span. UIKit yêu cầu addSubview, setFrame; jQuery yêu cầu .append(), .css(). Cả hai declarative đều dùng cấu trúc tĩnh, imperative dùng lệnh tuần tự. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-02-01` ← `ULO-DECLARATIVE_UI_PARADIGM-02`
**Xây dựng cấu trúc view phân cấp**
> Người học có khả năng xây dựng giao diện bằng cách lồng ghép các thành phần khai báo theo hệ thống phân cấp cha-con, tạo ra cây view hoàn chỉnh.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI dùng VStack { Text(...) }; React dùng <div><span>...</span></div>. Cả hai đều lồng các thành phần để tạo bố cục. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-02-02` ← `ULO-DECLARATIVE_UI_PARADIGM-02`
**Gắn trạng thái vào view**
> Người học có khả năng gắn trạng thái cục bộ vào view thông qua cơ chế khai báo (property wrapper, hook) để UI tự động cập nhật khi trạng thái thay đổi.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI dùng @State var count = 0; React dùng const [count, setCount] = useState(0). Cả hai đều khai báo state và binding để UI phản ứng. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-03-01` ← `ULO-DECLARATIVE_UI_PARADIGM-03`
**Phân tích quản lý trạng thái**
> Người học có khả năng phân tích sự khác biệt trong quản lý trạng thái: declarative có trạng thái tập trung và UI là hàm của trạng thái; imperative có trạng thái phân tán và UI được cập nhật thủ công.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI thay đổi state tự động render lại; UIKit phải gọi reloadData. React state thay đổi tự động re-render; jQuery phải thao tác DOM. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-03-02` ← `ULO-DECLARATIVE_UI_PARADIGM-03`
**Phân tích khả năng tái sử dụng và bảo trì**
> Người học có khả năng phân tích khả năng tái sử dụng và bảo trì: declarative dễ dàng tái sử dụng component nhờ tính module; imperative thường dễ gây side-effect và khó bảo trì hơn.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI component có thể dùng lại; React component tái sử dụng. UIKit view khó tái sử dụng hơn do phải kế thừa và delegate. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-04-01` ← `ULO-DECLARATIVE_UI_PARADIGM-04`
**Đánh giá hiệu suất**
> Người học có khả năng đánh giá mô hình khai báo dựa trên tiêu chí hiệu suất: declarative có thể gây re-render không cần thiết nếu không tối ưu; imperative kiểm soát tốt hơn nhưng dễ dư thừa code.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI có thể re-render toàn bộ view; React có shouldComponentUpdate. Imperative như UIKit chỉ cập nhật phần cần. -> Hợp lệ.

### `CIO-DECLARATIVE_UI_PARADIGM-04-02` ← `ULO-DECLARATIVE_UI_PARADIGM-04`
**Đánh giá khả năng mở rộng**
> Người học có khả năng đánh giá mô hình khai báo dựa trên khả năng mở rộng: declarative dễ mở rộng nhờ tính module và tách biệt; imperative có thể phức tạp khi quy mô lớn.

**Marr Test:** Test 2 ngôn ngữ: SwiftUI dễ thêm view mới; React dễ thêm component. UIKit có thể khó maintain khi nhiều màn hình. -> Hợp lệ.

### `CIO-UI_MODIFIERS_CONCEPT-01-01` ← `ULO-UI_MODIFIERS_CONCEPT-01`
**Liệt kê và phân loại UI Modifier**
> Người học có khả năng liệt kê các UI Modifier phổ biến và phân loại chúng theo chức năng: bố cục (padding, frame), kiểu dáng (background, foregroundColor, font), tương tác (onTapGesture).

**Marr Test:** Test 2 ngôn ngữ: SwiftUI dùng .padding(), .background(), .font(); React Native dùng style={{padding: 10, backgroundColor: 'red', fontSize: 16}}. Cả hai đều có khái niệm modifier/style để thay đổi thuộc tính. -> Hợp lệ.

### `CIO-UI_MODIFIERS_CONCEPT-02-01` ← `ULO-UI_MODIFIERS_CONCEPT-02`
**Thứ tự áp dụng modifier ảnh hưởng đến kết quả hiển thị**
> Người học có khả năng giải thích rằng thứ tự áp dụng các modifier lên một view ảnh hưởng đến kết quả cuối cùng, vì mỗi modifier thay đổi layout hoặc appearance dựa trên trạng thái hiện tại của view sau modifier trước đó.

**Marr Test:** Marr 2-Language Test: Mô tả này khớp với SwiftUI (modifier chain: .padding().background() khác .background().padding()) và Flutter (wrapping widgets: Padding( child: Container(...)) khác Container( padding: ...)). Cả hai đều có khái niệm thứ tự ảnh hưởng đến kết quả. Không chứa cú pháp cụ thể.

### `CIO-UI_MODIFIERS_CONCEPT-02-02` ← `ULO-UI_MODIFIERS_CONCEPT-02`
**Kết hợp các modifier để tạo hiệu ứng tổng hợp**
> Người học có khả năng giải thích cách kết hợp nhiều modifier để tạo ra hiệu ứng hiển thị tổng hợp, trong đó mỗi modifier đóng góp một phần vào thuộc tính cuối cùng của view (ví dụ: kích thước, màu sắc, khoảng cách, hình dạng).

**Marr Test:** Marr 2-Language Test: Mô tả này khớp với SwiftUI (nhiều modifier như .font().foregroundColor().padding()) và React Native (style object với nhiều thuộc tính như fontSize, color, padding). Cả hai đều có khái niệm kết hợp các thuộc tính. Không chứa cú pháp cụ thể.

### `CIO-UI_MODIFIERS_CONCEPT-03-01` ← `ULO-UI_MODIFIERS_CONCEPT-03`
**Lựa chọn modifier dựa trên yêu cầu bố cục**
> Người học có khả năng xác định các modifier cần thiết để đạt được bố cục mong muốn bằng cách phân tích yêu cầu về khoảng cách, căn chỉnh, kích thước và sắp xếp các thành phần.

**Marr Test:** Marr 2-Language Test: Mô tả này khớp với SwiftUI (sử dụng HStack, VStack, padding, alignment) và Flutter (sử dụng Row, Column, Padding, Align). Cả hai đều có khái niệm lựa chọn widget/modifier dựa trên bố cục. Không chứa cú pháp cụ thể.

### `CIO-UI_MODIFIERS_CONCEPT-03-02` ← `ULO-UI_MODIFIERS_CONCEPT-03`
**Sắp xếp thứ tự modifier để đạt hiệu quả mong muốn**
> Người học có khả năng sắp xếp các modifier theo thứ tự logic để tránh xung đột và đạt được kết quả chính xác, dựa trên hiểu biết về cách mỗi modifier tương tác với trạng thái hiện tại của view.

**Marr Test:** Marr 2-Language Test: Mô tả này khớp với SwiftUI (thứ tự modifier ảnh hưởng đến layout) và CSS (thứ tự khai báo thuộc tính không ảnh hưởng nhưng thứ tự lớp và specificity ảnh hưởng). Cả hai đều có khái niệm thứ tự ảnh hưởng đến kết quả. Không chứa cú pháp cụ thể.
