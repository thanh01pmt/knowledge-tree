# Báo cáo Đối chiếu Ngược Độ Phủ Syllabus (Reverse Coverage Audit)

- **Dự án:** `swift-associate`
- **Thời gian kiểm tra:** 2026-07-27T12:05:35.036661+00:00
- **Tổng số mục Syllabus:** 43
- **Số mục đã phủ trong LO:** 15
- **Số mục còn thiếu (Gaps):** 28
- **Độ phủ Syllabus (Coverage Score):** **34.88%**
- **Trạng thái:** ⚠️ WARN / FAIL

## Bảng đối chiếu đầy đủ (Syllabus vs Learning Objectives)
| Domain | Mã Syllabus | Nội dung Syllabus | LOs phụ trách |
|---|---|---|---|
| compromised | `1.2.2` | Security challenges | `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN`, `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE`, `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_IN_SWIFT_APPS_BY_IMPACT_DATA_BREACH_DENIAL_OF_SERVICE_2`, `SIO-SWIFT-CLASSIFY_SECURITY_CHALLENGES_BY` |
| compromised | `1.3` | Assess a visual design with accessibility in mind | `SIO-SWIFT-ANALYZE_VISUAL_LAYOUT_WITH` |
| Swift Language Usage | `3.1.1` | Evaluate the use of argument labels, parameters | `SIO-SWIFT-DISTINGUISH_BETWEEN_LABELED_AND` |
| and returns | `3.3.3` | Define methods | `CIO-EVENT_HANDLERS_CONCEPT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN`, `SIO-SWIFT-ANALYZE_ADVANTAGES_OF_FACTORY`, `SIO-SWIFT-HANDLE_MULTIPLE_EVENTS_TOUCHDOWN_TOUCHUPINSIDE_ON_A_SINGLE_UIBUTTON_IN_SWIFT_USING_SEPARATE_IBACTION_METHODS` |
| Swift Language Usage | `3.4.1` | Declare and/or initialize an array with values | `SIO-SWIFT-USE_DEFAULT_PROPERTY_VALUES` |
| Swift Language Usage | `3.4.2` | Identify and/or modify an array element using its index | `SIO-SWIFT-USE_SUBSCRIPT_TO_ACCESS_AND_UPDATE_KEY_VALUE_STATE_IN_SWIFT`, `SIO-SWIFT-ACCESS_ARRAY_ELEMENT_BY_INDEX`, `SIO-SWIFT-HANDLE_OUT_OF_BOUNDS_ACCESS`, `SIO-SWIFT-TRAVERSE_ARRAY_WITH_FOR_IN_INDEX` |
| Swift Language Usage | `3.5` | Demonstrate how to control the flow of execution | `ULO-CONTROL_FLOW-01`, `ULO-CONTROL_FLOW-02`, `ULO-CONTROL_FLOW-03` |
| different data types | `3.6.2` | Apply type inference | `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO`, `CIO-TYPE_SYSTEM-IDENTIFY_STATIC_TYPING_IN`, `CIO-TYPE_SYSTEM-ANALYZE_CONTRAST_IN_SWIFTUI`, `SIO-SWIFT-CLASSIFY_INTEGER_VALUES_TO_INT_TYPE` |
| different data types | `3.7` | .2. Apply Swift identifier rules | `CIO-RETURN_VALUES_AND_SCOPE-DESCRIBE_VARIABLE_ACCESS_RULES`, `SIO-SWIFT-DESCRIBE_VARIABLE_ACCESS_RULES_BASED_ON_SCOPE_IN_SWIFT`, `SIO-SWIFT-ANALYZE_COMPILER_ERROR_MESSAGE` |
| View Building with SwiftUI | `4.1` | Differentiate between imperative and declarative | `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY`, `CIO-DECLARATIVE_UI_PARADIGM-ANALYZE_REUSABILITY_MAINTAINABILITY_2`, `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_PERFORMANCE`, `CIO-DECLARATIVE_UI_PARADIGM-EVALUATE_SCALABILITY` |
| programming | `4.2` | Create Content Views using Text, Image, Shape, | `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS`, `SIO-SWIFT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS`, `SIO-SWIFT-USE_COLOR_ASSET_IN_VIEW` |
| and .resizable | `4.4` | Create Container Views (HStack, VStack, ZStack, Spacer) | `ULO-CONTAINER_VIEWS-03`, `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS`, `CIO-VISUAL_DESIGN-GROUP_RELATED_ELEMENTS_IN`, `SIO-SWIFT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` |
| and arrange Views inside of Stack Views | `4.5` | Explain the View hierarchy produced by a program | `ULO-VIEW_HIERARCHY-02`, `CIO-STATE_PROPERTY_WRAPPER-EVALUATE_APPROPRIATE_WRAPPER`, `SIO-SWIFT-TRACE_EVENT_FLOW_IN_SWIFTUI_USING_THE_VIEW_HIERARCHY_AND_ONRECEIVE_MODIFIER`, `SIO-SWIFT-EVALUATE_STATE_VS_STATEOBJECT_WRAPPER` |
| but not limited to, Button, TextField, Slider, and Toggle | `4.7` | . Use @State Property Wrapper to control the | `ULO-STATE_PROPERTY_WRAPPER-01`, `ULO-STATE_PROPERTY_WRAPPER-03`, `CIO-STATE_PROPERTY_WRAPPER-STATE_WRAPPER_DECOUPLING`, `CIO-STATE_PROPERTY_WRAPPER-OWNERSHIP_SHARING_SEMANTICS` |
| Debugging | `5.1` | Differentiate between syntax and run-time errors when | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02`, `ULO-SYNTAX_VS_RUNTIME_ERRORS-01`, `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` |

## ❌ Chi tiết các mục thiếu (Missing / Gap Items)
| Domain | Mã | Nội dung Syllabus |
|---|---|---|
| Planning and Design | `1.1` | Summarize the design cycle |
| Planning and Design | `1.1.1` | Brainstorm, plan, prototype, evaluate |
| Planning and Design | `1.2` | Summarize how sensitive data can be protected and |
| compromised | `1.2.1` | Sharing personal and application information |
| compromised | `1.2.3` | Legal, ethical and socioeconomic impacts |
| XCode Project Navigation | `2.1` | Differentiate between basic file types |
| XCode Project Navigation | `2.2` | After an asset has been imported, recognize available |
| assets and how they are used in a project | `2.3` | Import and/or use an asset |
| assets and how they are used in a project | `2.4` | Select the appropriate actions to configure |
| Swift Language Usage | `3.1` | Write, call and/or evaluate the execution of functions |
| and returns | `3.2` | Calculate the results when using various operators |
| and returns | `3.3` | Create and evaluate structures |
| and returns | `3.3.1` | Declare the properties of a structure |
| and returns | `3.3.2` | Initialize the properties of a structure |
| and returns | `3.3.4` | Create an instance of a structure |
| and returns | `3.3.5` | Use an instance of a structure |
| Swift Language Usage | `3.4` | Create and manipulate arrays |
| Swift Language Usage | `3.4.3` | Use and/or evaluate array properties and/or methods |
| Swift Language Usage | `3.5.1` | Create, analyze and predict loop structures |
| and their results | `3.5.2` | Create and interpret the outcome of conditional |
| statements | `3.6` | Declare and/or evaluate constants and variables of |
| different data types | `3.6.1` | Differentiate between constants and variables |
| different data types | `3.6.3` | Use explicit typing |
| different data types | `3.7` | . Use the appropriate naming syntax |
| different data types | `3.7` | .1. Use appropriate camel casing |
| and/or Color | `4.3` | Implement Modifiers including, but not limited to, |
| and arrange Views inside of Stack Views | `4.6` | Create and/or apply Interactive Views including, |
| building and running an app | `5.2` | Interpret error messages |

---

## Chiều 2 — Concept Coverage (Concept → LO)

- **Tổng số Concepts:** 42
- **Concepts có LO:** 42
- **Concepts chưa có LO:** 0

✅ **Tất cả concepts đều có ít nhất 1 LO.**

### Bảng Concept → LOs

| Concept | Name | LOs phụ trách |
|---|---|---|
| `VIEW_CONCEPT` | Khái Niệm View | `ULO-VIEW_CONCEPT-01`, `ULO-VIEW_CONCEPT-02`, `ULO-VIEW_CONCEPT-03`, `CIO-VIEW_CONCEPT-CLASSIFY_SWIFTUI_VIEW_COMPONENTS` ... (+8 more) |
| `DATA_TYPES` | Kiểu Dữ Liệu | `ULO-DATA_TYPES-01`, `ULO-DATA_TYPES-02`, `ULO-DATA_TYPES-03`, `CIO-DATA_TYPES-CLASSIFY_INTEGER_VALUES_TO` ... (+11 more) |
| `CONTROL_FLOW` | Luồng Điều Khiển | `ULO-CONTROL_FLOW-01`, `ULO-CONTROL_FLOW-02`, `ULO-CONTROL_FLOW-03`, `CIO-CONTROL_FLOW-DISTINGUISH_SEQUENCE_BRANCH_AND` ... (+17 more) |
| `TYPE_SYSTEM` | Hệ Thống Kiểu | `ULO-TYPE_SYSTEM-01`, `ULO-TYPE_SYSTEM-02`, `ULO-TYPE_SYSTEM-03`, `CIO-TYPE_SYSTEM-CLASSIFY_SWIFT_DATA_TYPES` ... (+17 more) |
| `VISUAL_DESIGN` | Thiết Kế Trực Quan | `ULO-VISUAL_DESIGN-01`, `ULO-VISUAL_DESIGN-02`, `ULO-VISUAL_DESIGN-03`, `ULO-VISUAL_DESIGN-04` ... (+28 more) |
| `SECURITY_CHALLENGES` | Thách Thức Bảo Mật | `ULO-SECURITY_CHALLENGES-01`, `ULO-SECURITY_CHALLENGES-02`, `ULO-SECURITY_CHALLENGES-03`, `CIO-SECURITY_CHALLENGES-CLASSIFY_SECURITY_CHALLENGES_IN` ... (+23 more) |
| `DEBUGGING` | Gỡ Lỗi | `ULO-DEBUGGING-01`, `ULO-DEBUGGING-02`, `ULO-DEBUGGING-03`, `CIO-DEBUGGING-EXECUTE_SEQUENTIAL_DEBUGGING_PROCESS` ... (+17 more) |
| `OBJECT_INSTANTIATION` | Object Instantiation | `ULO-OBJECT_INSTANTIATION-01`, `ULO-OBJECT_INSTANTIATION-02`, `ULO-OBJECT_INSTANTIATION-03`, `CIO-OBJECT_INSTANTIATION-DESCRIBE_STRUCT_MEMBERWISE_INITIALIZATION` ... (+17 more) |
| `EVENT_HANDLERS_CONCEPT` | Events and Event Handling | `ULO-EVENT_HANDLERS_CONCEPT-01`, `ULO-EVENT_HANDLERS_CONCEPT-02`, `ULO-EVENT_HANDLERS_CONCEPT-03`, `CIO-EVENT_HANDLERS_CONCEPT-IMPLEMENT_EVENT_DRIVEN_PATTERN` ... (+14 more) |
| `OBJECT_PROPERTIES` | Object Properties/Attributes | `ULO-OBJECT_PROPERTIES-01`, `ULO-OBJECT_PROPERTIES-02`, `ULO-OBJECT_PROPERTIES-03`, `CIO-OBJECT_PROPERTIES-IDENTIFY_PROPERTY_AS_KEY` ... (+11 more) |
| `SYNTAX_ERRORS` | Syntax Errors | `ULO-SYNTAX_ERRORS-02` |
| `RUNTIME_ERRORS` | Runtime Errors | `ULO-RUNTIME_ERRORS-02` |
| `ERROR_MESSAGES_CONCEPT` | Interpreting Error Messages | `ULO-ERROR_MESSAGES_CONCEPT-02` |
| `RETURN_VALUES_AND_SCOPE` | Return Values and Scope | `ULO-RETURN_VALUES_AND_SCOPE-01`, `ULO-RETURN_VALUES_AND_SCOPE-02`, `ULO-RETURN_VALUES_AND_SCOPE-03`, `CIO-RETURN_VALUES_AND_SCOPE-IDENTIFY_RETURN_STATEMENT_SYNTAX` ... (+20 more) |
| `ARRAY_OPERATIONS` | Array Operations | `ULO-ARRAY_OPERATIONS-01`, `ULO-ARRAY_OPERATIONS-02`, `ULO-ARRAY_OPERATIONS-03`, `CIO-ARRAY_OPERATIONS-ACCESS_ARRAY_ELEMENT` ... (+11 more) |
| `LOCAL_VIEW_STATE` | Local View State | `ULO-LOCAL_VIEW_STATE-03`, `ULO-LOCAL_VIEW_STATE-02`, `ULO-LOCAL_VIEW_STATE-01`, `CIO-LOCAL_VIEW_STATE-LOCAL_STATE_SYNC_ROLE` ... (+14 more) |
| `STATE_PROPERTY_WRAPPER` | State Property Wrapper | `ULO-STATE_PROPERTY_WRAPPER-02`, `ULO-STATE_PROPERTY_WRAPPER-01`, `ULO-STATE_PROPERTY_WRAPPER-03`, `CIO-STATE_PROPERTY_WRAPPER-STATE_TRIGGERED_RERENDER` ... (+17 more) |
| `WHILE_LOOP` | While Loop | `ULO-WHILE_LOOP-01`, `ULO-WHILE_LOOP-03`, `ULO-WHILE_LOOP-02`, `CIO-WHILE_LOOP-CONDITION_CONTROLLED_LOOP` ... (+14 more) |
| `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `ULO-PROJECT_ASSETS_MANAGEMENT-02`, `ULO-PROJECT_ASSETS_MANAGEMENT-01`, `ULO-PROJECT_ASSETS_MANAGEMENT-03`, `CIO-PROJECT_ASSETS_MANAGEMENT-ASSET_TYPE_CATEGORIZATION` ... (+11 more) |
| `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `ULO-SYNTAX_VS_RUNTIME_ERRORS-02`, `ULO-SYNTAX_VS_RUNTIME_ERRORS-01`, `ULO-SYNTAX_VS_RUNTIME_ERRORS-03`, `CIO-SYNTAX_VS_RUNTIME_ERRORS-DISTINGUISH_SYNTAX_RUNTIME` ... (+14 more) |
| `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `ULO-REFERENCE_TYPE_DECLARATION-03`, `ULO-REFERENCE_TYPE_DECLARATION-01`, `ULO-REFERENCE_TYPE_DECLARATION-02`, `CIO-REFERENCE_TYPE_DECLARATION-IDENTIFY_REFERENCE_SYNTAX` ... (+14 more) |
| `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `ULO-IMPLICIT_EXPLICIT_ANIMATION-02`, `ULO-IMPLICIT_EXPLICIT_ANIMATION-03`, `ULO-IMPLICIT_EXPLICIT_ANIMATION-01`, `ULO-IMPLICIT_EXPLICIT_ANIMATION-04` ... (+24 more) |
| `DECLARATIVE_UI_PARADIGM` | Declarative UI Paradigm | `ULO-DECLARATIVE_UI_PARADIGM-03`, `ULO-DECLARATIVE_UI_PARADIGM-02`, `ULO-DECLARATIVE_UI_PARADIGM-01`, `ULO-DECLARATIVE_UI_PARADIGM-04` ... (+24 more) |
| `UI_MODIFIERS_CONCEPT` | UI Modifiers | `ULO-UI_MODIFIERS_CONCEPT-03`, `ULO-UI_MODIFIERS_CONCEPT-02`, `ULO-UI_MODIFIERS_CONCEPT-01`, `CIO-UI_MODIFIERS-LIST_AND_CLASSIFY` ... (+14 more) |
| `DESIGN_CYCLE` | Chu Kỳ Thiết Kế | `ULO-DESIGN_CYCLE-01` |
| `SENSITIVE_DATA` | Dữ Liệu Nhạy Cảm | `ULO-SENSITIVE_DATA-02` |
| `ACCESSIBILITY` | Khả Năng Tiếp Cận | `ULO-ACCESSIBILITY-04` |
| `IMPERATIVE_PROGRAMMING` | Lập Trình Mệnh Lệnh | `ULO-IMPERATIVE_PROGRAMMING-02` |
| `FUNCTIONS_AND_PROCEDURES` | Hàm và Thủ Tục | `ULO-FUNCTIONS_AND_PROCEDURES-03` |
| `OPERATORS` | Toán Tử | `ULO-OPERATORS-03` |
| `STRUCTURE_TYPE` | Kiểu Cấu Trúc | `ULO-STRUCTURE_TYPE-03` |
| `ARRAYS` | Mảng | `ULO-ARRAYS-03` |
| `LOOP_STRUCTURES` | Cấu Trúc Vòng Lặp | `ULO-LOOP_STRUCTURES-03` |
| `CONDITIONAL_STATEMENTS` | Câu Lệnh Điều Kiện | `ULO-CONDITIONAL_STATEMENTS-03` |
| `VARIABLES_AND_CONSTANTS` | Biến và Hằng | `ULO-VARIABLES_AND_CONSTANTS-03` |
| `NAMING_CONVENTIONS` | Quy Ước Đặt Tên | `ULO-NAMING_CONVENTIONS-03` |
| `CONTAINER_VIEWS` | Container View | `ULO-CONTAINER_VIEWS-03` |
| `VIEW_HIERARCHY` | Phân Cấp View | `ULO-VIEW_HIERARCHY-02` |
| `UI_CONTROLS` | Điều Khiển Giao Diện | `ULO-UI_CONTROLS-03` |
| `LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS` | Tác Động Pháp Lý Đạo Đức Kinh Tế Xã Hội | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01` |
| `SHAPE` | Hình Dạng | `ULO-SHAPE-03` |
| `COLOR` | Màu Sắc | `ULO-COLOR-02` |