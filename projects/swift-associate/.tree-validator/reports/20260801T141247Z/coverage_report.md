# Báo cáo Đối chiếu Ngược Độ Phủ Syllabus (Reverse Coverage Audit)

- **Dự án:** `swift-associate`
- **Thời gian kiểm tra:** 2026-08-01T14:12:47.777766+00:00
- **Tổng số mục Syllabus:** 43
- **Số mục đã phủ trong LO:** 9
- **Số mục còn thiếu (Gaps):** 34
- **Độ phủ Syllabus (Coverage Score):** **20.93%**
- **Trạng thái:** ⚠️ WARN / FAIL

## Bảng đối chiếu đầy đủ (Syllabus vs Learning Objectives)
| Domain | Mã Syllabus | Nội dung Syllabus | LOs phụ trách |
|---|---|---|---|
| and returns | `3.3.3` | Define methods | `ULO-OBJECT_PROPERTIES-02`, `SIO-SWIFT-DEFINE_CLASS_METHODS` |
| Swift Language Usage | `3.4.2` | Identify and/or modify an array element using its index | `SIO-SWIFT-CLASSIFY_RUNTIME_ERROR_INDEX` |
| Swift Language Usage | `3.4.3` | Use and/or evaluate array properties and/or methods | `ULO-OBJECT_PROPERTIES-02` |
| different data types | `3.6.2` | Apply type inference | `SIO-SWIFT-MAP_VALUE_TO_TYPE` |
| different data types | `3.7` | .2. Apply Swift identifier rules | `SIO-SWIFT-TRANSFORM_WITH_RULESET` |
| programming | `4.2` | Create Content Views using Text, Image, Shape, | `SIO-SWIFT-TEXT_SHAPE_WIREFRAME`, `SIO-SWIFT-CREATE_3X3_GRID_WITH_GRID` |
| and .resizable | `4.4` | Create Container Views (HStack, VStack, ZStack, Spacer) | `SIO-SWIFT-CALCULATE_STACK_SIZE`, `SIO-SWIFT-ANALYZE_SPACING_COLLAPSE`, `SIO-SWIFT-SIMULATE_3X3_GRID_WITH_STACKS`, `SIO-SWIFT-CREATE_VISUAL_PATH_WITH_HIERARCHY` |
| and arrange Views inside of Stack Views | `4.5` | Explain the View hierarchy produced by a program | `SIO-SWIFT-CREATE_VISUAL_PATH_WITH_HIERARCHY` |
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
| and returns | `3.3.4` | Create an instance of a structure |
| and returns | `3.3.5` | Use an instance of a structure |
| Swift Language Usage | `3.4` | Create and manipulate arrays |
| Swift Language Usage | `3.4.1` | Declare and/or initialize an array with values |
| Swift Language Usage | `3.5` | Demonstrate how to control the flow of execution |
| Swift Language Usage | `3.5.1` | Create, analyze and predict loop structures |
| and their results | `3.5.2` | Create and interpret the outcome of conditional |
| statements | `3.6` | Declare and/or evaluate constants and variables of |
| different data types | `3.6.1` | Differentiate between constants and variables |
| different data types | `3.6.3` | Use explicit typing |
| different data types | `3.7` | . Use the appropriate naming syntax |
| different data types | `3.7` | .1. Use appropriate camel casing |
| View Building with SwiftUI | `4.1` | Differentiate between imperative and declarative |
| and/or Color | `4.3` | Implement Modifiers including, but not limited to, |
| and arrange Views inside of Stack Views | `4.6` | Create and/or apply Interactive Views including, |
| Debugging | `5.1` | Differentiate between syntax and run-time errors when |
| building and running an app | `5.2` | Interpret error messages |

---

## Chiều 2 — Concept Coverage (Concept → LO)

- **Tổng số Concepts:** 44
- **Concepts có LO:** 44
- **Concepts chưa có LO:** 0

✅ **Tất cả concepts đều có ít nhất 1 LO.**

### Bảng Concept → LOs

| Concept | Name | LOs phụ trách |
|---|---|---|
| `IF_ELSE_STATEMENT` | If-Else Statement | `ULO-IF_ELSE_STATEMENT-01`, `ULO-IF_ELSE_STATEMENT-02`, `CIO-IF_ELSE_STATEMENT-01`, `CIO-IF_ELSE_STATEMENT-02` ... (+10 more) |
| `PRIMITIVE_TYPE_DECLARATION` | Declaring Primitive Types | `ULO-PRIMITIVE_TYPE_DECLARATION-01`, `ULO-PRIMITIVE_TYPE_DECLARATION-02`, `CIO-PRIMITIVE_TYPE_DECLARATION-01`, `CIO-PRIMITIVE_TYPE_DECLARATION-02` ... (+10 more) |
| `DIGITAL_FOOTPRINT` | Digital Footprint | `ULO-DIGITAL_FOOTPRINT-01`, `ULO-DIGITAL_FOOTPRINT-02`, `CIO-DIGITAL_FOOTPRINT-01`, `CIO-DIGITAL_FOOTPRINT-02` ... (+10 more) |
| `VIEW_TRANSITIONS` | View Transitions | `ULO-VIEW_TRANSITIONS-01`, `ULO-VIEW_TRANSITIONS-02`, `CIO-VIEW_TRANSITIONS-01`, `CIO-VIEW_TRANSITIONS-02` ... (+10 more) |
| `RUNTIME_ERRORS` | Runtime Errors | `ULO-RUNTIME_ERRORS-01`, `ULO-RUNTIME_ERRORS-02`, `CIO-RUNTIME_ERRORS-01`, `CIO-RUNTIME_ERRORS-02` ... (+10 more) |
| `WCAG_PRINCIPLES` | WCAG Principles (POUR) | `ULO-WCAG_PRINCIPLES-01`, `ULO-WCAG_PRINCIPLES-02`, `CIO-WCAG_PRINCIPLES-01`, `CIO-WCAG_PRINCIPLES-02` ... (+7 more) |
| `ALGORITHMIC_BIAS_SOCIETY` | Algorithmic Bias in Society | `ULO-ALGORITHMIC_BIAS_SOCIETY-01`, `ULO-ALGORITHMIC_BIAS_SOCIETY-02`, `CIO-ALGORITHMIC_BIAS_SOCIETY-01`, `CIO-ALGORITHMIC_BIAS_SOCIETY-02` ... (+7 more) |
| `PHISHING_IDENTIFICATION` | Identifying Phishing Attempts | `ULO-PHISHING_IDENTIFICATION-01`, `ULO-PHISHING_IDENTIFICATION-02`, `CIO-PHISHING_IDENTIFICATION-01`, `CIO-PHISHING_IDENTIFICATION-02` ... (+4 more) |
| `UI_MODIFIERS_CONCEPT` | UI Modifiers | `ULO-UI_MODIFIERS_CONCEPT-03`, `CIO-UI_MODIFIERS_CONCEPT-03`, `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT`, `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` |
| `FOR_LOOP` | For Loop | `ULO-FOR_LOOP-01`, `ULO-FOR_LOOP-02`, `CIO-FOR_LOOP-01`, `CIO-FOR_LOOP-02` ... (+10 more) |
| `WIREFRAMING` | Wireframing | `ULO-WIREFRAMING-01`, `ULO-WIREFRAMING-02`, `CIO-WIREFRAMING-01`, `CIO-WIREFRAMING-02` ... (+7 more) |
| `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `ULO-PROJECT_ASSETS_MANAGEMENT-01`, `ULO-PROJECT_ASSETS_MANAGEMENT-03`, `CIO-PROJECT_ASSETS_MANAGEMENT-01`, `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` ... (+7 more) |
| `WHILE_LOOP` | While Loop | `ULO-WHILE_LOOP-03`, `CIO-WHILE_LOOP-03-01`, `CIO-WHILE_LOOP-03-02`, `SIO-SWIFT-WHILE_LOOP_COUNTER` ... (+3 more) |
| `LOGIC_ERRORS` | Logical Errors | `ULO-LOGIC_ERRORS-01`, `ULO-LOGIC_ERRORS-02`, `ULO-LOGIC_ERRORS-03`, `CIO-LOGIC_ERRORS-01` ... (+17 more) |
| `MALWARE_TYPES_CONCEPT` | Malware Types | `ULO-MALWARE_TYPES_CONCEPT-01`, `ULO-MALWARE_TYPES_CONCEPT-02`, `CIO-MALWARE_TYPES_CONCEPT-01`, `CIO-MALWARE_TYPES_CONCEPT-02` ... (+10 more) |
| `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01`, `ULO-IMPLICIT_EXPLICIT_ANIMATION-02`, `CIO-IMPLICIT_EXPLICIT_ANIMATION-01`, `CIO-IMPLICIT_EXPLICIT_ANIMATION-02` ... (+10 more) |
| `UI_BOX_MODEL_LAYOUT` | UI Box Model Layout System | `ULO-UI_BOX_MODEL_LAYOUT-01`, `ULO-UI_BOX_MODEL_LAYOUT-02`, `ULO-UI_BOX_MODEL_LAYOUT-03`, `CIO-UI_BOX_MODEL_LAYOUT-01` ... (+17 more) |
| `SWITCH_CASE` | Switch-Case Statement | `ULO-SWITCH_CASE-01`, `ULO-SWITCH_CASE-02`, `CIO-SWITCH_CASE-01`, `CIO-SWITCH_CASE-02` ... (+6 more) |
| `ARRAY_OPERATIONS` | Array Operations | `ULO-ARRAY_OPERATIONS-03`, `CIO-ARRAY_OPERATIONS-03-01`, `CIO-ARRAY_OPERATIONS-03-02`, `SIO-SWIFT-ITERATE_ARRAY_FOR_IN` ... (+3 more) |
| `SCREEN_READERS` | Screen Readers | `ULO-SCREEN_READERS-01`, `ULO-SCREEN_READERS-02` |
| `LOCAL_VIEW_STATE` | Local View State | `ULO-LOCAL_VIEW_STATE-01`, `ULO-LOCAL_VIEW_STATE-02` |
| `EVENT_HANDLERS_CONCEPT` | Events and Event Handling | `ULO-EVENT_HANDLERS_CONCEPT-02`, `CIO-EVENT_HANDLERS_CONCEPT-02`, `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON`, `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` |
| `OBJECT_INSTANTIATION` | Object Instantiation | `ULO-OBJECT_INSTANTIATION-01`, `ULO-OBJECT_INSTANTIATION-02` |
| `CLASS_DEFINITION` | Class Definition | `ULO-CLASS_DEFINITION-01`, `ULO-CLASS_DEFINITION-02`, `ULO-CLASS_DEFINITION-03`, `CIO-CLASS_DEFINITION-01` ... (+5 more) |
| `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `ULO-REFERENCE_TYPE_DECLARATION-01`, `ULO-REFERENCE_TYPE_DECLARATION-02`, `CIO-REFERENCE_TYPE_DECLARATION-01`, `CIO-REFERENCE_TYPE_DECLARATION-02` ... (+7 more) |
| `USER_CENTERED_DESIGN` | User-Centered Design Process | `ULO-USER_CENTERED_DESIGN-01`, `ULO-USER_CENTERED_DESIGN-02`, `ULO-USER_CENTERED_DESIGN-03`, `CIO-USER_CENTERED_DESIGN-01` ... (+8 more) |
| `AI_BIAS` | Bias in AI | `ULO-AI_BIAS-01`, `ULO-AI_BIAS-02`, `ULO-AI_BIAS-03`, `CIO-AI_BIAS-01` ... (+11 more) |
| `SYNTAX_ERRORS` | Syntax Errors | `ULO-SYNTAX_ERRORS-01`, `ULO-SYNTAX_ERRORS-02`, `ULO-SYNTAX_ERRORS-03`, `CIO-SYNTAX_ERRORS-01` ... (+8 more) |
| `PASSWORD_STRENGTH_CONCEPT` | Strong Passwords | `ULO-PASSWORD_STRENGTH_CONCEPT-01`, `ULO-PASSWORD_STRENGTH_CONCEPT-02`, `ULO-PASSWORD_STRENGTH_CONCEPT-03`, `CIO-PASSWORD_STRENGTH_CONCEPT-01` ... (+17 more) |
| `PROTOTYPING` | Prototyping | `ULO-PROTOTYPING-01`, `ULO-PROTOTYPING-02`, `ULO-PROTOTYPING-03`, `CIO-PROTOTYPING-01` ... (+17 more) |
| `STATE_PROPERTY_WRAPPER` | State Property Wrapper | `ULO-STATE_PROPERTY_WRAPPER-02`, `CIO-STATE_PROPERTY_WRAPPER-02`, `SIO-SWIFT-DECLARE_STATE_PROPERTY`, `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` |
| `BREAKPOINTS` | Using Breakpoints | `ULO-BREAKPOINTS-01`, `ULO-BREAKPOINTS-02`, `ULO-BREAKPOINTS-03`, `CIO-BREAKPOINTS-01-01` ... (+17 more) |
| `OBJECT_PROPERTIES` | Object Properties/Attributes | `ULO-OBJECT_PROPERTIES-01`, `ULO-OBJECT_PROPERTIES-02`, `ULO-OBJECT_PROPERTIES-03`, `CIO-OBJECT_PROPERTIES-01-01` ... (+17 more) |
| `COMPOSITION_PRINCIPLES` | Composition Principles | `ULO-COMPOSITION_PRINCIPLES-01`, `ULO-COMPOSITION_PRINCIPLES-02`, `ULO-COMPOSITION_PRINCIPLES-03`, `CIO-COMPOSITION_PRINCIPLES-01` ... (+17 more) |
| `DECLARATIVE_UI_PARADIGM` | Declarative UI Paradigm | `ULO-DECLARATIVE_UI_PARADIGM-03`, `CIO-DECLARATIVE_UI_PARADIGM-03`, `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE`, `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` |
| `ERROR_MESSAGES_CONCEPT` | Interpreting Error Messages | `ULO-ERROR_MESSAGES_CONCEPT-02`, `CIO-ERROR_MESSAGES_CONCEPT-02`, `SIO-SWIFT-READ_ERROR_MESSAGE_TYPE`, `SIO-SWIFT-LOCATE_ERROR_CAUSE` |
| `EVENT_BASED_PROGRAMMING` | Event-Based Programming Model | `ULO-EVENT_BASED_PROGRAMMING-01`, `ULO-EVENT_BASED_PROGRAMMING-02`, `ULO-EVENT_BASED_PROGRAMMING-03`, `CIO-EVENT_BASED_PROGRAMMING-01` ... (+17 more) |
| `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03`, `CIO-SYNTAX_VS_RUNTIME_ERRORS-03`, `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME`, `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` |
| `TWO_WAY_BINDING` | Two-Way Data Binding | `ULO-TWO_WAY_BINDING-01`, `ULO-TWO_WAY_BINDING-02`, `ULO-TWO_WAY_BINDING-03`, `CIO-TWO_WAY_BINDING-01` ... (+5 more) |
| `DIGITAL_IDENTITY` | Digital Identity Management | `ULO-DIGITAL_IDENTITY-01`, `ULO-DIGITAL_IDENTITY-02`, `ULO-DIGITAL_IDENTITY-03`, `CIO-DIGITAL_IDENTITY-01` ... (+17 more) |
| `FLEXBOX_GRID_LAYOUT` | Flexible & Grid Layout Systems | `ULO-FLEXBOX_GRID_LAYOUT-01`, `ULO-FLEXBOX_GRID_LAYOUT-02`, `ULO-FLEXBOX_GRID_LAYOUT-03`, `CIO-FLEXBOX_GRID_LAYOUT-01` ... (+17 more) |
| `CROSS_ORIGIN_SECURITY` | Cross-Origin Security & Policies | `ULO-CROSS_ORIGIN_SECURITY-01`, `ULO-CROSS_ORIGIN_SECURITY-02`, `ULO-CROSS_ORIGIN_SECURITY-03`, `CIO-CROSS_ORIGIN_SECURITY-01` ... (+17 more) |
| `COLOR_THEORY` | Color Theory | `ULO-COLOR_THEORY-01`, `ULO-COLOR_THEORY-02`, `ULO-COLOR_THEORY-03`, `CIO-COLOR_THEORY-01` ... (+17 more) |
| `FIRST_CLASS_FUNCTIONS_CONCEPT` | First-Class & Higher-Order Functions | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-01`, `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-02`, `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-03`, `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` ... (+5 more) |