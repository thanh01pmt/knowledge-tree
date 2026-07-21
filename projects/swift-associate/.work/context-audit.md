# Context Audit: Swift Associate
**Source:** `projects/swift-associate/context/Apple Associate - Objective Domains_0125.pdf`

## Yêu cầu
Thực hiện phân rã các chủ đề trong Syllabus thành các bản ghi dự kiến cho `learning-objectives.tsv` (cấu trúc ULO -> CIO -> SIO). Từ đó xác định chính xác các `concept_codes` cần thiết.

---

### Domain 1: Planning, Design & Security
*Nội dung:* Design cycle (Brainstorm, plan, prototype, evaluate), Security challenges, privacy, Accessibility.

| code | name | description | lo_type | parent_lo_code | concept_codes (Master Tree) |
|---|---|---|---|---|---|
| `ULO-DESIGN-CYCLE` | Understand App Design Cycle | Hiểu quy trình thiết kế phần mềm từ lên ý tưởng đến đánh giá. | `UNIVERSAL` | `NULL` | Cần tìm: *Design Process, Software Lifecycle* |
| `CIO-APP-DESIGN` | Apply App Design Cycle | Vận dụng các bước brainstorm, plan, prototype, evaluate để thiết kế app. | `CONCEPTUAL_IMPL` | `ULO-DESIGN-CYCLE` | Cần tìm: *Prototyping, UI/UX* |
| `SIO-APP-EVALUATE` | Evaluate Visual Design | Đánh giá thiết kế giao diện dựa trên tiêu chí Accessibility. | `SPECIFIC_IMPL` | `CIO-APP-DESIGN` | Cần tìm: *Accessibility* |
| `ULO-SEC-PRIVACY` | Understand Security & Privacy | Hiểu tầm quan trọng của bảo mật dữ liệu và quyền riêng tư. | `UNIVERSAL` | `NULL` | Cần tìm: *Security, Privacy* |

---

### Domain 2: Xcode Project Navigation
*Nội dung:* Basic file types, Recognize/Import/Use assets, UI configuration actions.

| code | name | description | lo_type | parent_lo_code | concept_codes (Master Tree) |
|---|---|---|---|---|---|
| `ULO-DEV-ENV` | Navigate Development Environment | Hiểu cách sử dụng môi trường phát triển tích hợp (IDE) để quản lý dự án. | `UNIVERSAL` | `NULL` | Cần tìm: *IDE, Tools* |
| `CIO-XCODE-NAV` | Navigate Xcode Project | Điều hướng và quản lý cấu trúc file, assets trong dự án Xcode. | `CONCEPTUAL_IMPL` | `ULO-DEV-ENV` | Cần tìm: *Assets Management, IDE* |
| `SIO-XCODE-ASSETS` | Import and Use Assets | Nhập và sử dụng tài nguyên (hình ảnh, màu sắc) qua `.xcassets`. | `SPECIFIC_IMPL` | `CIO-XCODE-NAV` | Cần tìm: *Assets* |
| `SIO-XCODE-UI-CONF` | Configure UI in Xcode | Sử dụng Inspector và Navigator để cấu hình giao diện. | `SPECIFIC_IMPL` | `CIO-XCODE-NAV` | Cần tìm: *Interface Builder/Config* |

---

### Domain 3: Swift Language Usage
*Nội dung:* Functions, Operators, Structures, Arrays, Control flow (Loops, Conditionals), Variables & Constants.

| code | name | description | lo_type | parent_lo_code | concept_codes (Master Tree) |
|---|---|---|---|---|---|
| `ULO-PROG-STATE` | Understand Variables and Data Types | Hiểu cấp phát bộ nhớ và định kiểu dữ liệu. | `UNIVERSAL` | `NULL` | Cần tìm: *Variables, Data Types* |
| `CIO-SWIFT-VARS` | Declare Swift Variables/Constants | Khai báo `var` và `let`, sử dụng Type inference. | `CONCEPTUAL_IMPL` | `ULO-PROG-STATE` | Cần tìm: *Variables, Data Types* |
| `SIO-SWIFT-LET` | Declare Constant with type inference | Viết `let name = "Apple"`. | `SPECIFIC_IMPL` | `CIO-SWIFT-VARS` | Cần tìm: *Variables* |
| `ULO-ITERATION` | Understand Definite Iteration | Hiểu vòng lặp xác định để thực thi lệnh nhiều lần. | `UNIVERSAL` | `NULL` | Cần tìm: *Loops, Iteration* |
| `CIO-SWIFT-FOR-IN` | Use for-in loop in Swift | Sử dụng `for-in` duyệt Collection. | `CONCEPTUAL_IMPL` | `ULO-ITERATION` | Cần tìm: *Loops* |

---

### Domain 4: View Building with SwiftUI
*Nội dung:* Content Views, Modifiers, Container Views, View Hierarchy, Interactive Views, @State.

| code | name | description | lo_type | parent_lo_code | concept_codes (Master Tree) |
|---|---|---|---|---|---|
| `ULO-DECLARATIVE-UI` | Understand Declarative UI | Nắm bắt mô hình lập trình giao diện khai báo. | `UNIVERSAL` | `NULL` | Cần tìm: *Declarative UI, UI Building* |
| `CIO-SWIFTUI-VIEWS` | Compose Views in SwiftUI | Kết hợp Content Views và Container Views (VStack, HStack). | `CONCEPTUAL_IMPL` | `ULO-DECLARATIVE-UI` | Cần tìm: *Layout, UI Components* |
| `SIO-SWIFTUI-MODIFIERS` | Apply Modifiers | Áp dụng `.padding`, `.background` để tuỳ chỉnh giao diện. | `SPECIFIC_IMPL` | `CIO-SWIFTUI-VIEWS` | Cần tìm: *UI Modifiers* |
| `ULO-STATE-DATA-DRIVEN`| Understand Data-Driven UI | Quản lý trạng thái và tự động cập nhật giao diện. | `UNIVERSAL` | `NULL` | Cần tìm: *State Management* |
| `CIO-SWIFTUI-STATE` | Use @State Property Wrapper | Sử dụng `@State` để theo dõi trạng thái cục bộ. | `CONCEPTUAL_IMPL` | `ULO-STATE-DATA-DRIVEN` | Cần tìm: *State, Property Wrapper* |

---

### Domain 5: Debugging
*Nội dung:* Syntax vs run-time errors, Interpret error messages.

| code | name | description | lo_type | parent_lo_code | concept_codes (Master Tree) |
|---|---|---|---|---|---|
| `ULO-DEBUGGING` | Understand Debugging | Khái niệm tìm và sửa lỗi phần mềm. | `UNIVERSAL` | `NULL` | Cần tìm: *Debugging, Testing* |
| `CIO-SWIFT-ERRORS` | Differentiate Error Types | Phân biệt lỗi cú pháp và lỗi runtime trong Xcode. | `CONCEPTUAL_IMPL` | `ULO-DEBUGGING` | Cần tìm: *Errors, Exceptions* |
| `SIO-SWIFT-INTERPRET`| Interpret Error Messages | Đọc hiểu log và thông báo lỗi. | `SPECIFIC_IMPL` | `CIO-SWIFT-ERRORS` | Cần tìm: *Debugging* |
