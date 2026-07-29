# Báo cáo Đối chiếu Ngược Độ Phủ Syllabus (Reverse Coverage Audit)

- **Dự án:** `swift-associate`
- **Thời gian kiểm tra:** 2026-07-29T15:19:22.307693+00:00
- **Tổng số mục Syllabus:** 43
- **Số mục đã phủ trong LO:** 1
- **Số mục còn thiếu (Gaps):** 42
- **Độ phủ Syllabus (Coverage Score):** **2.33%**
- **Trạng thái:** ⚠️ WARN / FAIL

## Bảng đối chiếu đầy đủ (Syllabus vs Learning Objectives)
| Domain | Mã Syllabus | Nội dung Syllabus | LOs phụ trách |
|---|---|---|---|
| but not limited to, Button, TextField, Slider, and Toggle | `4.7` | . Use @State Property Wrapper to control the | `SIO-SWIFT-DECLARE_STATE_PROPERTY` |

## ❌ Chi tiết các mục thiếu (Missing / Gap Items)
| Domain | Mã | Nội dung Syllabus |
|---|---|---|
| Planning and Design | `1.1` | Summarize the design cycle |
| Planning and Design | `1.1.1` | Brainstorm, plan, prototype, evaluate |
| Planning and Design | `1.2` | Summarize how sensitive data can be protected and |
| compromised | `1.2.1` | Sharing personal and application information |
| compromised | `1.2.2` | Security challenges |
| compromised | `1.2.3` | Legal, ethical and socioeconomic impacts |
| compromised | `1.3` | Assess a visual design with accessibility in mind |
| XCode Project Navigation | `2.1` | Differentiate between basic file types |
| XCode Project Navigation | `2.2` | After an asset has been imported, recognize available |
| assets and how they are used in a project | `2.3` | Import and/or use an asset |
| assets and how they are used in a project | `2.4` | Select the appropriate actions to configure |
| Swift Language Usage | `3.1` | Write, call and/or evaluate the execution of functions |
| Swift Language Usage | `3.1.1` | Evaluate the use of argument labels, parameters |
| and returns | `3.2` | Calculate the results when using various operators |
| and returns | `3.3` | Create and evaluate structures |
| and returns | `3.3.1` | Declare the properties of a structure |
| and returns | `3.3.2` | Initialize the properties of a structure |
| and returns | `3.3.3` | Define methods |
| and returns | `3.3.4` | Create an instance of a structure |
| and returns | `3.3.5` | Use an instance of a structure |
| Swift Language Usage | `3.4` | Create and manipulate arrays |
| Swift Language Usage | `3.4.1` | Declare and/or initialize an array with values |
| Swift Language Usage | `3.4.2` | Identify and/or modify an array element using its index |
| Swift Language Usage | `3.4.3` | Use and/or evaluate array properties and/or methods |
| Swift Language Usage | `3.5` | Demonstrate how to control the flow of execution |
| Swift Language Usage | `3.5.1` | Create, analyze and predict loop structures |
| and their results | `3.5.2` | Create and interpret the outcome of conditional |
| statements | `3.6` | Declare and/or evaluate constants and variables of |
| different data types | `3.6.1` | Differentiate between constants and variables |
| different data types | `3.6.2` | Apply type inference |
| different data types | `3.6.3` | Use explicit typing |
| different data types | `3.7` | . Use the appropriate naming syntax |
| different data types | `3.7` | .1. Use appropriate camel casing |
| different data types | `3.7` | .2. Apply Swift identifier rules |
| View Building with SwiftUI | `4.1` | Differentiate between imperative and declarative |
| programming | `4.2` | Create Content Views using Text, Image, Shape, |
| and/or Color | `4.3` | Implement Modifiers including, but not limited to, |
| and .resizable | `4.4` | Create Container Views (HStack, VStack, ZStack, Spacer) |
| and arrange Views inside of Stack Views | `4.5` | Explain the View hierarchy produced by a program |
| and arrange Views inside of Stack Views | `4.6` | Create and/or apply Interactive Views including, |
| Debugging | `5.1` | Differentiate between syntax and run-time errors when |
| building and running an app | `5.2` | Interpret error messages |

---

## Chiều 2 — Concept Coverage (Concept → LO)

- **Tổng số Concepts:** 44
- **Concepts có LO:** 9
- **Concepts chưa có LO:** 35

### ⚠️ Concepts chưa được phủ bởi LO nào

| Code | Name |
|---|---|
| `IF_ELSE_STATEMENT` | If-Else Statement |
| `PRIMITIVE_TYPE_DECLARATION` | Declaring Primitive Types |
| `DIGITAL_FOOTPRINT` | Digital Footprint |
| `VIEW_TRANSITIONS` | View Transitions |
| `RUNTIME_ERRORS` | Runtime Errors |
| `WCAG_PRINCIPLES` | WCAG Principles (POUR) |
| `ALGORITHMIC_BIAS_SOCIETY` | Algorithmic Bias in Society |
| `PHISHING_IDENTIFICATION` | Identifying Phishing Attempts |
| `FOR_LOOP` | For Loop |
| `WIREFRAMING` | Wireframing |
| `LOGIC_ERRORS` | Logical Errors |
| `MALWARE_TYPES_CONCEPT` | Malware Types |
| `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation |
| `UI_BOX_MODEL_LAYOUT` | UI Box Model Layout System |
| `SWITCH_CASE` | Switch-Case Statement |
| `SCREEN_READERS` | Screen Readers |
| `LOCAL_VIEW_STATE` | Local View State |
| `OBJECT_INSTANTIATION` | Object Instantiation |
| `CLASS_DEFINITION` | Class Definition |
| `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types |
| `USER_CENTERED_DESIGN` | User-Centered Design Process |
| `AI_BIAS` | Bias in AI |
| `SYNTAX_ERRORS` | Syntax Errors |
| `PASSWORD_STRENGTH_CONCEPT` | Strong Passwords |
| `PROTOTYPING` | Prototyping |
| `BREAKPOINTS` | Using Breakpoints |
| `OBJECT_PROPERTIES` | Object Properties/Attributes |
| `COMPOSITION_PRINCIPLES` | Composition Principles |
| `EVENT_BASED_PROGRAMMING` | Event-Based Programming Model |
| `TWO_WAY_BINDING` | Two-Way Data Binding |
| `DIGITAL_IDENTITY` | Digital Identity Management |
| `FLEXBOX_GRID_LAYOUT` | Flexible & Grid Layout Systems |
| `CROSS_ORIGIN_SECURITY` | Cross-Origin Security & Policies |
| `COLOR_THEORY` | Color Theory |
| `FIRST_CLASS_FUNCTIONS_CONCEPT` | First-Class & Higher-Order Functions |

**→ Action:** Thêm LO cho các concepts trên. Chạy `/detect-gaps` để có plan chi tiết.

### Bảng Concept → LOs

| Concept | Name | LOs phụ trách |
|---|---|---|
| `UI_MODIFIERS_CONCEPT` | UI Modifiers | `ULO-UI_MODIFIERS_CONCEPT-03`, `CIO-UI_MODIFIERS_CONCEPT-03`, `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT`, `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` |
| `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `ULO-PROJECT_ASSETS_MANAGEMENT-01`, `ULO-PROJECT_ASSETS_MANAGEMENT-03`, `CIO-PROJECT_ASSETS_MANAGEMENT-01`, `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` ... (+7 more) |
| `WHILE_LOOP` | While Loop | `ULO-WHILE_LOOP-03`, `CIO-WHILE_LOOP-03-01`, `CIO-WHILE_LOOP-03-02`, `SIO-SWIFT-WHILE_LOOP_COUNTER` ... (+3 more) |
| `ARRAY_OPERATIONS` | Array Operations | `ULO-ARRAY_OPERATIONS-03`, `CIO-ARRAY_OPERATIONS-03-01`, `CIO-ARRAY_OPERATIONS-03-02`, `SIO-SWIFT-ITERATE_ARRAY_FOR_IN` ... (+3 more) |
| `EVENT_HANDLERS_CONCEPT` | Events and Event Handling | `ULO-EVENT_HANDLERS_CONCEPT-02`, `CIO-EVENT_HANDLERS_CONCEPT-02`, `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON`, `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` |
| `STATE_PROPERTY_WRAPPER` | State Property Wrapper | `ULO-STATE_PROPERTY_WRAPPER-02`, `CIO-STATE_PROPERTY_WRAPPER-02`, `SIO-SWIFT-DECLARE_STATE_PROPERTY`, `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` |
| `DECLARATIVE_UI_PARADIGM` | Declarative UI Paradigm | `ULO-DECLARATIVE_UI_PARADIGM-03`, `CIO-DECLARATIVE_UI_PARADIGM-03`, `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE`, `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` |
| `ERROR_MESSAGES_CONCEPT` | Interpreting Error Messages | `ULO-ERROR_MESSAGES_CONCEPT-02`, `CIO-ERROR_MESSAGES_CONCEPT-02`, `SIO-SWIFT-READ_ERROR_MESSAGE_TYPE`, `SIO-SWIFT-LOCATE_ERROR_CAUSE` |
| `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03`, `CIO-SYNTAX_VS_RUNTIME_ERRORS-03`, `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME`, `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` |