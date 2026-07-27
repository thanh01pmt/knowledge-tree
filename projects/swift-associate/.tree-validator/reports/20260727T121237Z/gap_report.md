# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-27T12:12:37.079686+00:00

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

**49 CIO(s) vi phạm tính Trung tính (Marr Test):**

| CIO Code | CIO Name | Detected Keywords / Patterns |
|---|---|---|
| `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` | Distinguish Sequence, Branch, and Loop in Swift | `swift` |
| `CIO-CONTROL_FLOW-DESCRIBE_EXECUTION_ORDER_OF` | Describe Execution Order of if-else in Swift | `swift` |
| `CIO-CONTROL_FLOW-TRACE_VARIABLE_VALUES_THROUGH` | Trace Variable Values Through if-else Branches in Swift | `swift` |
| `CIO-CONTROL_FLOW-TRACE_EXECUTION_PATH_OF` | Trace execution path of if-else in Swift | `swift` |
| `CIO-CONTROL_FLOW-CHECK_EXHAUSTIVENESS_OF_SWITCH` | Check exhaustiveness of switch cases in Swift | `swift` |
| `CIO-CONTROL_FLOW-DETECT_INFINITE_LOOP_IN` | Detect infinite loop in Swift | `swift` |
| `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` | Classify Integer Values to Int Type | `swift` |
| `CIO-DATA_TYPES-COMPARE_MEMORY_SIZE_OF` | Compare Memory Size of Integer Types | `swift` |
| `CIO-DATA_TYPES-CHOOSE_SWIFT_DATA_TYPE` | Choose Swift Data Type Based on Value Range | `swift` |
| `CIO-DATA_TYPES-CONVERT_DATA_TYPES_USING` | Convert Data Types Using Swift Initializers | `swift` |
| `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` | Execute Sequential Debugging Process on Swift Code in Xcode | `swift` |
| `CIO-DEBUGGING-SET_CONDITIONAL_BREAKPOINT_IN` | Set Conditional Breakpoint in Xcode to Inspect Swift Variable State | `swift` |
| `CIO-DEBUGGING-USE_PRINT_WITH_LEVEL` | Sử dụng hàm print với tiền tố cấp độ để ghi log trong Swift | `swift` |
| `CIO-DEBUGGING-USE_STEP_INTO_AND` | Sử dụng lệnh Step Over trong Xcode debugger để thực thi từng dòng Swift | `swift` |
| `CIO-DEBUGGING-INSERT_PRINT_AT_MIDPOINT` | Chèn câu lệnh print tại điểm giữa mã Swift để loại trừ nhị phân | `swift` |
| `CIO-DEBUGGING-USE_5_WHYS_ON` | Đặt chuỗi câu hỏi Tại sao dựa trên log Swift để truy vết nguyên nhân gốc rễ | `swift` |
| `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` | Implement event-driven pattern in Swift using @IBAction and UIControl events | `swift` |
| `CIO-EVENT_HANDLERS_CONCEPT-TRACE_EVENT_FLOW_FROM` | Trace event flow from user action to handler invocation in Swift using UIApplication and UIResponder chain | `swift` |
| `CIO-EVENT_HANDLERS_CONCEPT-REGISTER_CALLBACK_TO_UIBUTTONS` | Register callback to UIButton's touchUpInside event in Swift using addTarget(_:action:for:) | `swift` |
| `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN` | Handle multiple events (touchDown, touchUpInside) on a single UIButton in Swift using separate @IBAction methods | `swift` |
| `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` | Mô tả quy trình cấp phát bộ nhớ và khởi tạo đối tượng class trong Swift | `swift` |
| `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_INITIALIZER_PARAMETERS` | Analyze How Initializer Parameters Affect Object State in Swift | `swift` |
| `CIO-OBJECT_INSTANTIATION-CALL_A_SWIFT_CLASS` | Call a Swift Class Initializer with Appropriate Arguments | `swift` |
| `CIO-OBJECT_INSTANTIATION-CREATE_A_SWIFT_OBJECT` | Create a Swift Object Using a No-Argument Initializer | `swift` |
| `CIO-OBJECT_INSTANTIATION-COMPARE_DIRECT_INITIALIZATION_VIA` | Compare Direct Initialization via Swift Initializer vs. Static Factory Method | `swift` |
| `CIO-OBJECT_INSTANTIATION-ANALYZE_HOW_DEPENDENCY_INJECTION` | Analyze How Dependency Injection in Swift Enables Object Creation Without Knowing Dependency Details | `swift` |
| `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` | Identify Property as Key-Value Pair Using Swift Syntax | `swift` |
| `CIO-OBJECT_PROPERTIES-APPLY_PROPERTY_OBSERVERS_TO` | Apply Property Observers to Manage State Changes in Swift | `swift` |
| `CIO-OBJECT_PROPERTIES-ACCESS_AND_UPDATE_STORED` | Access and Update Stored Property via Instance in Swift | `swift` |
| `CIO-OBJECT_PROPERTIES-DEFINE_CUSTOM_GETTER_AND` | Define Custom Getter and Setter for Computed Property in Swift | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` | Identify Return Statement Syntax in Swift Functions | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-DISTINGUISH_LOCAL_AND_GLOBAL` | Distinguish local and global variables in Swift based on declaration position | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-EXPLAIN_LOCAL_VARIABLE_SCOPE` | Explain local variable scope and return value mechanism in Swift functions | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES` | Describe variable access rules based on scope in Swift | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-WRITE_A_SWIFT_FUNCTION` | Write a Swift function that uses local variables and returns a value | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-DESIGN_A_SWIFT_FUNCTION` | Design a Swift function using both global and local variables with controlled data flow | `swift` |
| `CIO-RETURN_VALUES_AND_SCOPE-USE_RETURN_VALUE_AS` | Use Return Value as Direct Argument in Swift | `swift` |
| `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` | Classify security challenges in Swift apps by origin (network, input, code) | `swift` |
| `CIO-SECURITY_CHALLENGES-USE_SWIFT_SPECIFIC_CHECKLIST` | Use Swift-specific checklist to identify SQL injection in Swift code | `swift` |
| `CIO-SECURITY_CHALLENGES-ANALYZE_IMPACT_OF_SWIFT` | Analyze impact of Swift data leakage on confidentiality and integrity | `swift` |
| `CIO-SECURITY_CHALLENGES-EVALUATE_SEVERITY_OF_SECURITY` | Evaluate Severity of Security Impact Using Predefined Criteria in Swift | `swift` |
| `CIO-SECURITY_CHALLENGES-APPLY_5_WHYS_TECHNIQUE` | Apply 5 Whys Technique to Identify Root Cause of Swift Security Incident | `swift` |
| `CIO-SECURITY_CHALLENGES-CONSTRUCT_CAUSE_EFFECT_CHAIN` | Construct Cause-Effect Chain from Swift Security Incident | `swift` |
| `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` | Classify Swift data types by storage and range | `swift` |
| `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN` | Identify static typing in Swift via type annotation and inference | `swift` |
| `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI` | Phân tích quá trình kiểm tra kiểu tĩnh trong Swift | `swift` |
| `CIO-TYPE_SYSTEM-APPLY_SWIFT_TYPE_INFERENCE` | Áp dụng suy luận kiểu Swift để xác định kiểu biểu thức | `swift` |
| `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI_2` | Phân tích thông báo lỗi kiểu Swift để tìm nguyên nhân | `swift` |
| `CIO-TYPE_SYSTEM-SIMULATE_SWIFT_TYPE_FLOW` | Mô phỏng luồng kiểu Swift để phát hiện lỗi | `swift` |

**→ Action:** Viết lại mô tả/tên CIO thành khái niệm/thủ tục trung tính 100% độc lập ngôn ngữ, hoặc chuyển xuống tầng SIO.
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