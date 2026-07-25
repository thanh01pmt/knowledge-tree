# Báo cáo Đối chiếu Ngược Độ Phủ Syllabus (Reverse Coverage Audit)

- **Dự án:** `swift-associate`
- **Thời gian kiểm tra:** 2026-07-25T12:20:19.833504+00:00
- **Tổng số mục Syllabus:** 43
- **Số mục đã phủ trong LO:** 21
- **Số mục còn thiếu (Gaps):** 22
- **Độ phủ Syllabus (Coverage Score):** **48.84%**
- **Trạng thái:** ⚠️ WARN / FAIL

## Bảng đối chiếu đầy đủ (Syllabus vs Learning Objectives)
| Domain | Mã Syllabus | Nội dung Syllabus | LOs phụ trách |
|---|---|---|---|
| Planning and Design | `1.1` | Summarize the design cycle | `ULO-DESIGN_CYCLE-01`, `CIO-DESIGN_CYCLE-01`, `CIO-DESIGN_CYCLE-02`, `SIO-SWIFT-DESIGN-CYCLE-IDENTIFY-PHASES` |
| Planning and Design | `1.1.1` | Brainstorm, plan, prototype, evaluate | `SIO-SWIFT-DESIGN-CYCLE-IDENTIFY-PHASES`, `SIO-SWIFT-DESIGN-CYCLE-PLAN-PROJECT` |
| Planning and Design | `1.2` | Summarize how sensitive data can be protected and | `ULO-SENSITIVE_DATA-02`, `CIO-SENSITIVE_DATA-01`, `CIO-SENSITIVE_DATA-02`, `SIO-SWIFT-SENSITIVE-DATA-IDENTIFY` |
| compromised | `1.2.3` | Legal, ethical and socioeconomic impacts | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01`, `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01-01`, `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01-02`, `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01-03` |
| and returns | `3.3.1` | Declare the properties of a structure | `SIO-SWIFT-define-struct-properties` |
| and returns | `3.3.2` | Initialize the properties of a structure | `SIO-SWIFT-define-struct-properties` |
| Swift Language Usage | `3.4.2` | Identify and/or modify an array element using its index | `SIO-SWIFT-insert-element-at-end`, `SIO-SWIFT-insert-element-at-index`, `SIO-SWIFT-remove-element-by-index`, `SIO-SWIFT-remove-element-by-condition` |
| Swift Language Usage | `3.5` | Demonstrate how to control the flow of execution | `SIO-SWIFT-TRACE-CONTROL-FLOW` |
| Swift Language Usage | `3.5.1` | Create, analyze and predict loop structures | `ULO-LOOP_STRUCTURES-03`, `CIO-LOOPS-01`, `CIO-LOOPS-02`, `CIO-LOOPS-03` |
| statements | `3.6` | Declare and/or evaluate constants and variables of | `ULO-VARIABLES_AND_CONSTANTS-03`, `CIO-VARIABLES-01`, `CIO-VARIABLES-02`, `SIO-SWIFT-VARIABLE-DECLARE-01` |
| different data types | `3.6.1` | Differentiate between constants and variables | `ULO-VARIABLES_AND_CONSTANTS-03`, `CIO-VARIABLES-01`, `CIO-VARIABLES-02`, `SIO-SWIFT-VARIABLE-DECLARE-01` |
| different data types | `3.6.2` | Apply type inference | `SIO-SWIFT-assign-return-value`, `SIO-SWIFT-VARIABLE-DECLARE-02` |
| different data types | `3.7` | .2. Apply Swift identifier rules | `SIO-SWIFT-ASSET-ADD-IMAGE`, `SIO-SWIFT-ASSET-ADD-COLOR` |
| programming | `4.2` | Create Content Views using Text, Image, Shape, | `SIO-SWIFT-static-ui-declaration`, `SIO-SWIFT-static-ui-composition`, `SIO-SWIFT-MODIFY-APPEARANCE-COLOR-FONT` |
| and/or Color | `4.3` | Implement Modifiers including, but not limited to, | `SIO-SWIFT-MODIFY-APPEARANCE-COLOR-FONT` |
| and .resizable | `4.4` | Create Container Views (HStack, VStack, ZStack, Spacer) | `ULO-CONTAINER_VIEWS-03`, `CIO-CONTAINER_VIEWS-01`, `CIO-CONTAINER_VIEWS-02`, `CIO-CONTAINER_VIEWS-03` |
| and arrange Views inside of Stack Views | `4.5` | Explain the View hierarchy produced by a program | `ULO-VIEW_HIERARCHY-02`, `CIO-VIEW_HIERARCHY-01`, `CIO-VIEW_HIERARCHY-02`, `SIO-SWIFT-analyze-rendering-order` |
| and arrange Views inside of Stack Views | `4.6` | Create and/or apply Interactive Views including, | `ULO-CONTAINER_VIEWS-03` |
| but not limited to, Button, TextField, Slider, and Toggle | `4.7` | . Use @State Property Wrapper to control the | `ULO-STATE_PROPERTY_WRAPPER-02`, `CIO-UI_CONTROLS-02`, `CIO-STATE_PROPERTY_WRAPPER-01`, `SIO-SWIFT-reactive-ui-state` |
| Debugging | `5.1` | Differentiate between syntax and run-time errors when | `ULO-SYNTAX_ERRORS-02`, `ULO-RUNTIME_ERRORS-02`, `CIO-SYNTAX_ERRORS-01`, `CIO-RUNTIME_ERRORS-01` |
| building and running an app | `5.2` | Interpret error messages | `ULO-ERROR_MESSAGES_CONCEPT-02`, `CIO-ERROR_MESSAGES_CONCEPT-02-01`, `CIO-ERROR_MESSAGES_CONCEPT-02-02`, `CIO-ERROR_MESSAGES_CONCEPT-02-03` |

## ❌ Chi tiết các mục thiếu (Missing / Gap Items)
| Domain | Mã | Nội dung Syllabus |
|---|---|---|
| compromised | `1.2.1` | Sharing personal and application information |
| compromised | `1.2.2` | Security challenges |
| compromised | `1.3` | Assess a visual design with accessibility in mind |
| XCode Project Navigation | `2.1` | Differentiate between basic file types |
| XCode Project Navigation | `2.2` | After an asset has been imported, recognize available |
| assets and how they are used in a project | `2.3` | Import and/or use an asset |
| assets and how they are used in a project | `2.4` | Select the appropriate actions to configure |
| Swift Language Usage | `3.1` | Write, call and/or evaluate the execution of functions |
| Swift Language Usage | `3.1.1` | Evaluate the use of argument labels, parameters |
| and returns | `3.2` | Calculate the results when using various operators |
| and returns | `3.3` | Create and evaluate structures |
| and returns | `3.3.3` | Define methods |
| and returns | `3.3.4` | Create an instance of a structure |
| and returns | `3.3.5` | Use an instance of a structure |
| Swift Language Usage | `3.4` | Create and manipulate arrays |
| Swift Language Usage | `3.4.1` | Declare and/or initialize an array with values |
| Swift Language Usage | `3.4.3` | Use and/or evaluate array properties and/or methods |
| and their results | `3.5.2` | Create and interpret the outcome of conditional |
| different data types | `3.6.3` | Use explicit typing |
| different data types | `3.7` | . Use the appropriate naming syntax |
| different data types | `3.7` | .1. Use appropriate camel casing |
| View Building with SwiftUI | `4.1` | Differentiate between imperative and declarative |

---

## Chiều 2 — Concept Coverage (Concept → LO)

- **Tổng số Concepts:** 36
- **Concepts có LO:** 25
- **Concepts chưa có LO:** 11

### ⚠️ Concepts chưa được phủ bởi LO nào

| Code | Name |
|---|---|
| `VIEW_CONCEPT` | Khái Niệm View |
| `DATA_TYPES` | Kiểu Dữ Liệu |
| `CONTROL_FLOW` | Luồng Điều Khiển |
| `TYPE_SYSTEM` | Hệ Thống Kiểu |
| `VISUAL_DESIGN` | Thiết Kế Trực Quan |
| `SECURITY_CHALLENGES` | Thách Thức Bảo Mật |
| `DEBUGGING` | Gỡ Lỗi |
| `OBJECT_INSTANTIATION` | Object Instantiation |
| `EVENT_HANDLERS_CONCEPT` | Events and Event Handling |
| `OBJECT_PROPERTIES` | Object Properties/Attributes |
| `RETURN_VALUES_AND_SCOPE` | Return Values and Scope |

**→ Action:** Thêm LO cho các concepts trên. Chạy `/detect-gaps` để có plan chi tiết.

### Bảng Concept → LOs

| Concept | Name | LOs phụ trách |
|---|---|---|
| `UI_CONTROLS` | Các Thành Phần Tương Tác | `ULO-UI_CONTROLS-03`, `CIO-UI_CONTROLS-01`, `CIO-UI_CONTROLS-02`, `CIO-UI_CONTROLS-03` ... (+6 more) |
| `VIEW_HIERARCHY` | Phân Cấp View | `ULO-VIEW_HIERARCHY-02`, `CIO-VIEW_HIERARCHY-01`, `CIO-VIEW_HIERARCHY-02`, `SIO-SWIFT-analyze-rendering-order` ... (+3 more) |
| `CONTAINER_VIEWS` | Các View Chứa | `ULO-CONTAINER_VIEWS-03`, `CIO-CONTAINER_VIEWS-01`, `CIO-CONTAINER_VIEWS-02`, `CIO-CONTAINER_VIEWS-03` ... (+6 more) |
| `STRUCTURE_TYPE` | Kiểu Cấu Trúc | `ULO-STRUCTURE_TYPE-03`, `CIO-STRUCTURE_TYPE-01`, `CIO-STRUCTURE_TYPE-02`, `CIO-STRUCTURE_TYPE-03` ... (+6 more) |
| `VARIABLES_AND_CONSTANTS` | Biến và Hằng Số | `ULO-VARIABLES_AND_CONSTANTS-03`, `CIO-VARIABLES-01`, `CIO-VARIABLES-02`, `SIO-SWIFT-VARIABLE-DECLARE-01` ... (+3 more) |
| `LOOP_STRUCTURES` | Cấu Trúc Lặp | `ULO-LOOP_STRUCTURES-03`, `CIO-LOOPS-01`, `CIO-LOOPS-02`, `CIO-LOOPS-03` ... (+6 more) |
| `CONDITIONAL_STATEMENTS` | Câu Lệnh Điều Kiện | `ULO-CONDITIONAL_STATEMENTS-03`, `CIO-CONDITIONAL-01`, `CIO-CONDITIONAL-02`, `SIO-SWIFT-CONDITIONAL-01-01` ... (+3 more) |
| `FUNCTIONS_AND_PROCEDURES` | Hàm và Phương Thức | `ULO-FUNCTIONS_AND_PROCEDURES-03`, `CIO-FUNC_DECOMP-01`, `CIO-FUNC_PARAM-01`, `CIO-FUNC_RETURN-01` ... (+6 more) |
| `ARRAYS` | Mảng | `ULO-ARRAYS-03`, `CIO-ARRAYS-01`, `CIO-ARRAYS-02`, `CIO-ARRAYS-03` ... (+6 more) |
| `IMPERATIVE_PROGRAMMING` | Lập Trình Mệnh Lệnh | `ULO-IMPERATIVE_PROGRAMMING-02`, `CIO-IMP_STATE-01`, `CIO-IMP_STATE-02`, `SIO-SWIFT-TRACE-VARIABLE-CHANGES` ... (+3 more) |
| `SHAPE` | Hình Dạng | `ULO-SHAPE-03`, `CIO-SHAPE-03-01`, `CIO-SHAPE-03-02`, `CIO-SHAPE-03-03` ... (+6 more) |
| `COLOR` | Màu Sắc | `ULO-COLOR-02`, `CIO-COLOR-02-01`, `CIO-COLOR-02-02`, `SIO-SWIFT-analyze-hsl-components` ... (+3 more) |
| `ACCESSIBILITY` | Khả Năng Tiếp Cận | `ULO-ACCESSIBILITY-04`, `CIO-ACCESSIBILITY-01`, `CIO-ACCESSIBILITY-02`, `SIO-SWIFT-WCAG-CONTRAST-EVALUATION` ... (+3 more) |
| `LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS` | Tác Động Pháp Lý, Đạo Đức và Kinh Tế Xã Hội | `ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01`, `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01-01`, `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01-02`, `CIO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS-01-03` ... (+6 more) |
| `OPERATORS` | Toán Tử | `ULO-OPERATORS-03`, `CIO-OP_EXPR-01`, `CIO-OP_PRECEDENCE-01`, `CIO-OP_LOGICAL-01` ... (+6 more) |
| `SENSITIVE_DATA` | Dữ Liệu Nhạy Cảm | `ULO-SENSITIVE_DATA-02`, `CIO-SENSITIVE_DATA-01`, `CIO-SENSITIVE_DATA-02`, `SIO-SWIFT-SENSITIVE-DATA-IDENTIFY` ... (+3 more) |
| `DESIGN_CYCLE` | Chu Kỳ Thiết Kế | `ULO-DESIGN_CYCLE-01`, `CIO-DESIGN_CYCLE-01`, `CIO-DESIGN_CYCLE-02`, `SIO-SWIFT-DESIGN-CYCLE-IDENTIFY-PHASES` ... (+3 more) |
| `NAMING_CONVENTIONS` | Quy Ước Đặt Tên | `ULO-NAMING_CONVENTIONS-03`, `CIO-NAMING-01`, `CIO-NAMING-02`, `SIO-SWIFT-NAMING-01-01` ... (+3 more) |
| `UI_MODIFIERS_CONCEPT` | UI Modifiers | `ULO-UI_MODIFIERS_CONCEPT-03`, `CIO-UI_MODIFIERS_CONCEPT-03-01`, `CIO-UI_MODIFIERS_CONCEPT-03-02`, `SIO-SWIFT-MODIFY-APPEARANCE-COLOR-FONT` ... (+3 more) |
| `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `ULO-PROJECT_ASSETS_MANAGEMENT-02`, `ULO-PROJECT_ASSETS_MANAGEMENT-01`, `ULO-PROJECT_ASSETS_MANAGEMENT-03`, `CIO-PAM-02-01` ... (+17 more) |
| `STATE_PROPERTY_WRAPPER` | State Property Wrapper | `ULO-STATE_PROPERTY_WRAPPER-02`, `CIO-STATE_PROPERTY_WRAPPER-01`, `SIO-SWIFT-reactive-state-binding-1`, `SIO-SWIFT-reactive-state-binding-2` |
| `DECLARATIVE_UI_PARADIGM` | Declarative UI Paradigm | `ULO-DECLARATIVE_UI_PARADIGM-03`, `ULO-DECLARATIVE_UI_PARADIGM-02`, `CIO-DECLARATIVE_UI_PARADIGM-03-01`, `CIO-DECLARATIVE_UI_PARADIGM-03-02` ... (+10 more) |
| `SYNTAX_ERRORS` | Syntax Errors | `ULO-SYNTAX_ERRORS-02`, `CIO-SYNTAX_ERRORS-01`, `SIO-SWIFT-syntax-error-analysis-1`, `SIO-SWIFT-syntax-error-analysis-2` |
| `RUNTIME_ERRORS` | Runtime Errors | `ULO-RUNTIME_ERRORS-02`, `CIO-RUNTIME_ERRORS-01`, `SIO-SWIFT-runtime-error-diagnosis-1`, `SIO-SWIFT-runtime-error-diagnosis-2` |
| `ERROR_MESSAGES_CONCEPT` | Interpreting Error Messages | `ULO-ERROR_MESSAGES_CONCEPT-02`, `CIO-ERROR_MESSAGES_CONCEPT-02-01`, `CIO-ERROR_MESSAGES_CONCEPT-02-02`, `CIO-ERROR_MESSAGES_CONCEPT-02-03` ... (+6 more) |