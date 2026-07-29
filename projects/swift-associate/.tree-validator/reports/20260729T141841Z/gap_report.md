# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-29T14:18:41.828765+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**

---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

✅ **Tất cả CIOs đều có ít nhất 2 SIO con.**

---

## Gap D — Marr's Test Violated CIOs (`MARR_VIOLATION`)

> CIO chứa từ khóa công nghệ, cú pháp hoặc cấu trúc ngôn ngữ cụ thể — vi phạm Phép thử Marr 2-Ngôn-ngữ.

✅ **Tất cả CIOs đều đạt Phép thử Marr (100% Trung tính).**

---

## Gap E — Marr Test Note Quality (`MARR_NOTE_QUALITY`)

> CIO có marr_test_note nhưng note không đủ chất lượng (thiếu note, hoặc nhắc < 2 ngôn ngữ).
> Theo T6: CIO bắt buộc phải pass Marr 2-Language Test — note phải chứng minh mapping ≥ 2 ngôn ngữ.

**116 CIO(s) có vấn đề với marr_test_note:**

| CIO Code | CIO Name | Issue | Detail |
|---|---|---|---|
| `CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT` | Truy cập phần tử mảng bằng chỉ số | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-ZERO_BASED_INDEX` | Hiểu chỉ số bắt đầu từ 0 | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-SEQUENTIAL_ARRAY_TRAVERSAL` | Duyệt mảng tuần tự | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-MODIFY_ARRAY_ELEMENT` | Sửa đổi phần tử mảng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE` | Vai trò của trạng thái cục bộ trong đồng bộ giao diện | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOCAL_VIEW_STATE-CONTROL_UI_PROPERTIES` | Điều khiển thuộc tính giao diện bằng trạng thái cục bộ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOCAL_VIEW_STATE-UPDATE_LOCAL_STATE` | Cập nhật trạng thái cục bộ từ tương tác người dùng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOCAL_VIEW_STATE-TRACE_LOCAL_STATE_LIFECYCLE` | Trace local state lifecycle | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-LOCAL_VIEW_STATE-DETERMINE_LOCAL_STATE_SCOPE` | Determine local state scope | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER` | Explain state-triggered re-rendering | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING` | Describe state wrapper decoupling role | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-INITIALIZE_UPDATE_MUTABLE_STATE` | Initialize and update mutable state | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT` | Bind state to UI element and observe changes | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS` | Compare ownership and sharing semantics of state wrappers | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER` | Evaluate appropriate wrapper based on data source and view hierarchy | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP` | Recognize condition-controlled loop pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-CONDITION_FIRST_REPETITION` | Condition-first repetition pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-LOOP_TERMINATION_CONDITION` | Loop termination via condition falsification | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-DYNAMIC_CONDITION_REPETITION` | Dynamic condition repetition with mutable control variable | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-SENTINEL_CONTROLLED_REPETITION` | Sentinel-controlled repetition pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION` | Asset type categorization pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_CATALOG_HIERARCHICAL` | Asset catalog hierarchical organization pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_ADDITION_REFERENCE` | Asset addition and reference pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-COLOR_ASSET_DEFINITION` | Color asset definition and usage pattern | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME` | Phân biệt lỗi cú pháp và lỗi runtime dựa trên định nghĩa | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-SYNTAX_RUNTIME_CAUSES` | Giải thích nguyên nhân gây ra lỗi cú pháp và lỗi runtime | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-CLASSIFY_ERROR_DETECTION` | Phân loại ví dụ lỗi dựa trên thời điểm phát hiện | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-IDENTIFY_ERROR_TYPE` | Xác định loại lỗi từ mã nguồn dựa trên dấu hiệu nhận biết | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-ANALYZE_ERROR_MESSAGES` | Phân tích thông báo lỗi để phân loại lỗi | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX` | Nhận diện cú pháp khai báo kiểu tham chiếu | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-COMPARE_REFERENCE_VALUE` | So sánh hành vi gán và sao chép giữa kiểu tham chiếu và kiểu giá trị | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-ANALYZE_REFERENCE_IMPACT` | Phân tích tác động của tham chiếu đến bộ nhớ và hiệu năng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL` | Khai báo biến tham chiếu với khởi tạo đối tượng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-REFERENCE_TYPE_DECLARATION-DECLARE_REFERENCE_NULL_2` | Khai báo biến tham chiếu với giá trị null hoặc nil | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL` | Phân biệt dựa trên cơ chế kích hoạt | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-DISTINGUISH_TIME_CONTROL_2` | Phân biệt dựa trên mức độ kiểm soát thời gian và chi tiết | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES` | Áp dụng implicit animation bằng cách gắn bộ mô tả animation vào view | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-WRAP_STATE_CHANGES_2` | Áp dụng implicit animation bằng cách bao bọc thay đổi trạng thái trong ngữ cảnh animation | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY` | Phân tích ưu nhược điểm dựa trên mức độ kiểm soát và độ phức tạp | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-ANALYZE_PERFORMANCE_REUSABILITY_2` | Phân tích ưu nhược điểm dựa trên hiệu suất và khả năng tái sử dụng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX` | Đánh giá lựa chọn dựa trên yêu cầu về hiệu suất và độ phức tạp | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-IMPLICIT_EXPLICIT_ANIMATION-EVALUATE_CUSTOMIZABILITY_UX_2` | Đánh giá lựa chọn dựa trên khả năng tùy chỉnh và trải nghiệm người dùng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE` | Mô tả trạng thái mong muốn | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE` | So sánh luồng điều khiển khai báo và mệnh lệnh | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW` | Xây dựng cấu trúc view phân cấp | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-ATTACH_STATE_VIEW` | Gắn trạng thái vào view | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY` | Phân tích quản lý trạng thái | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2` | Phân tích khả năng tái sử dụng và bảo trì | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE` | Đánh giá hiệu suất | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY` | Đánh giá khả năng mở rộng | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` | Liệt kê và phân loại UI Modifier | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS-ORDER_AFFECTS_DISPLAY` | Thứ tự áp dụng modifier ảnh hưởng đến kết quả hiển thị | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS-COMBINE_MODIFIERS` | Kết hợp các modifier để tạo hiệu ứng tổng hợp | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS-SELECT_BY_LAYOUT` | Lựa chọn modifier dựa trên yêu cầu bố cục | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS-ORDER_FOR_EFFECT` | Sắp xếp thứ tự modifier để đạt hiệu quả mong muốn | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | Distinguish Sequence, Branch, and Loop in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | Describe Execution Order of if-else in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | Trace Variable Values Through if-else Branches in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | Trace execution path of if-else in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | Check exhaustiveness of switch cases in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | Detect infinite loop in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | Classify Integer Values to Int Type | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | Compare Memory Size of Integer Types | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | Choose ngôn ngữ Data Type Based on Value Range | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | Convert Data Types Using ngôn ngữ Initializers | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | Execute Sequential Debugging Process on ngôn ngữ Code in Xcode | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | Set Conditional Breakpoint in Xcode to Inspect ngôn ngữ Variable State | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | Sử dụng hàm print với tiền tố cấp độ để ghi log trong ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DEBUGGING-USE_STEP_INTO_AND` | Sử dụng lệnh Step Over trong Xcode debugger để thực thi từng dòng ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | Chèn câu lệnh print tại điểm giữa mã ngôn ngữ để loại trừ nhị phân | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DEBUGGING-USE_5_WHYS_ON` | Đặt chuỗi câu hỏi Tại sao dựa trên log ngôn ngữ để truy vết nguyên nhân gốc rễ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | Implement event-driven pattern in ngôn ngữ using @IBAction and UIControl events | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | Trace event flow from user action to handler invocation in ngôn ngữ using UIApplication and UIResponder chain | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | Register callback to UIButton's touchUpInside event in ngôn ngữ using addTarget(_:action:for:) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-ANALYZE_EVENT_PROPAGATION_IN` | Analyze event propagation in UIKit using hitTest(_:with:) and touchesBegan(_:with:) to prevent propagation | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | Handle multiple events (touchDown, touchUpInside) on a single UIButton in ngôn ngữ using separate @IBAction methods | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | Mô tả quy trình cấp phát bộ nhớ và khởi tạo đối tượng class trong ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | Analyze How Initializer Parameters Affect Object State in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | Call a ngôn ngữ Class Initializer with Appropriate Arguments | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | Create a ngôn ngữ Object Using a No-Argument Initializer | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | Compare Direct Initialization via ngôn ngữ Initializer vs. Static Factory Method | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | Analyze How Dependency Injection in ngôn ngữ Enables Object Creation Without Knowing Dependency Details | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | Identify Property as Key-Value Pair Using ngôn ngữ Syntax | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | Apply Property Observers to Manage State Changes in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | Access and Update Stored Property via Instance in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | Define Custom Getter and Setter for Computed Property in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | Identify Return Statement Syntax in ngôn ngữ Functions | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | Distinguish local and global variables in ngôn ngữ based on declaration position | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | Explain local variable scope and return value mechanism in ngôn ngữ functions | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | Describe variable access rules based on scope in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | Write a ngôn ngữ function that uses local variables and returns a value | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | Design a ngôn ngữ function using both global and local variables with controlled data flow | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | Use Return Value as Direct Argument in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | Classify security challenges in ngôn ngữ apps by origin (network, input, code) | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | Use ngôn ngữ-specific checklist to identify SQL injection in ngôn ngữ code | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | Analyze impact of ngôn ngữ data leakage on confidentiality and integrity | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | Evaluate Severity of Security Impact Using Predefined Criteria in ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | Apply 5 Whys Technique to Identify Root Cause of ngôn ngữ Security Incident | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | Construct Cause-Effect Chain from ngôn ngữ Security Incident | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | Classify ngôn ngữ data types by storage and range | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | Identify static typing in ngôn ngữ via type annotation and inference | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | Phân tích quá trình kiểm tra kiểu tĩnh trong ngôn ngữ | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | Áp dụng suy luận kiểu ngôn ngữ để xác định kiểu biểu thức | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | Phân tích thông báo lỗi kiểu ngôn ngữ để tìm nguyên nhân | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | Mô phỏng luồng kiểu ngôn ngữ để phát hiện lỗi | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` | Classify framework UI khai báo View Components | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_CONCEPT-ANALYZE_TAP_INTERACTION_FLOW` | Analyze Tap Interaction Flow in framework UI khai báo | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VIEW_CONCEPT-MODEL_VIEW_AS_SWIFTUI` | Model View as framework UI khai báo Struct | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-ANALYZE_CONTRAST_IN_SWIFTUI` | Phân tích tương phản trong giao diện framework UI khai báo | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-APPLY_SYMMETRIC_BALANCE_IN` | Apply symmetric balance in framework UI khai báo layout | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-USE_GOLDEN_RATIO_GRID` | Use golden ratio grid in framework UI khai báo with LazyVGrid | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN` | Group related elements in framework UI khai báo using containers and spacing | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-ANALYZE_COLOR_PALETTE_PSYCHOLOGY` | Analyze color palette psychology in framework UI khai báo | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-EVALUATE_WHITESPACE_IMPACT_ON` | Evaluate whitespace impact on readability in framework UI khai báo | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-APPLY_VISUAL_EVALUATION_CRITERIA` | Apply visual evaluation criteria to analyze framework UI khai báo layout | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-VISUAL_DESIGN-COMPARE_SWIFTUI_DESIGN_AGAINST` | Compare framework UI khai báo design against proximity principle | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |

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