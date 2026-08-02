# Báo cáo Đối chiếu Ngược Độ Phủ Syllabus (Reverse Coverage Audit)

- **Dự án:** `swift-associate`
- **Thời gian kiểm tra:** 2026-08-02T17:14:37.436729+00:00
- **Tổng số mục Syllabus:** 43
- **Số mục đã phủ trong LO:** 13
- **Số mục còn thiếu (Gaps):** 30
- **Độ phủ Syllabus (Coverage Score):** **30.23%**
- **Trạng thái:** ⚠️ WARN / FAIL

## Bảng đối chiếu đầy đủ (Syllabus vs Learning Objectives)
| Domain | Mã Syllabus | Nội dung Syllabus | LOs phụ trách |
|---|---|---|---|
| Planning and Design | `1.1` | Summarize the design cycle | `CIO-DESIGN_THINKING_PROCESS-01`, `CIO-TWO_WAY_BINDING-01`, `SIO-SWIFT-REFERENCE_TYPE_DECLARATION-02` |
| Swift Language Usage | `3.1` | Write, call and/or evaluate the execution of functions | `CIO-BREAKPOINTS-01` |
| and returns | `3.3` | Create and evaluate structures | `CIO-FOR_LOOP-01` |
| and returns | `3.3.3` | Define methods | `ULO-CLASS_DEFINITION-01`, `SIO-SWIFT-LIST_OPERATIONS-01` |
| Swift Language Usage | `3.4.2` | Identify and/or modify an array element using its index | `ULO-ARRAY_OPERATIONS-01`, `ULO-FOR_LOOP-01`, `CIO-ARRAY_OPERATIONS-01`, `SIO-SWIFT-FOR_LOOP-01` |
| Swift Language Usage | `3.4.3` | Use and/or evaluate array properties and/or methods | `ULO-CLASS_DEFINITION-01`, `SIO-SWIFT-LIST_OPERATIONS-01` |
| Swift Language Usage | `3.5` | Demonstrate how to control the flow of execution | `ULO-LOGIC_ERRORS-01`, `CIO-ASYNCHRONOUS_PROG_CONCEPT-01`, `SIO-SWIFT-FOR_LOOP-02` |
| Swift Language Usage | `3.5.1` | Create, analyze and predict loop structures | `CIO-FOR_LOOP-01` |
| different data types | `3.7` | .2. Apply Swift identifier rules | `SIO-SWIFT-COPYRIGHT_CREATIVE_COMMONS-01`, `SIO-SWIFT-SYNTAX_ERRORS-01` |
| View Building with SwiftUI | `4.1` | Differentiate between imperative and declarative | `CIO-IMPLICIT_EXPLICIT_ANIMATION-01` |
| but not limited to, Button, TextField, Slider, and Toggle | `4.7` | . Use @State Property Wrapper to control the | `SIO-SWIFT-CLASS_DEFINITION-02` |
| Debugging | `5.1` | Differentiate between syntax and run-time errors when | `ULO-SYNTAX_ERRORS-01` |
| building and running an app | `5.2` | Interpret error messages | `ULO-ERROR_MESSAGES_CONCEPT-01` |

## ❌ Chi tiết các mục thiếu (Missing / Gap Items)
| Domain | Mã | Nội dung Syllabus |
|---|---|---|
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
| Swift Language Usage | `3.1.1` | Evaluate the use of argument labels, parameters |
| and returns | `3.2` | Calculate the results when using various operators |
| and returns | `3.3.1` | Declare the properties of a structure |
| and returns | `3.3.2` | Initialize the properties of a structure |
| and returns | `3.3.4` | Create an instance of a structure |
| and returns | `3.3.5` | Use an instance of a structure |
| Swift Language Usage | `3.4` | Create and manipulate arrays |
| Swift Language Usage | `3.4.1` | Declare and/or initialize an array with values |
| and their results | `3.5.2` | Create and interpret the outcome of conditional |
| statements | `3.6` | Declare and/or evaluate constants and variables of |
| different data types | `3.6.1` | Differentiate between constants and variables |
| different data types | `3.6.2` | Apply type inference |
| different data types | `3.6.3` | Use explicit typing |
| different data types | `3.7` | . Use the appropriate naming syntax |
| different data types | `3.7` | .1. Use appropriate camel casing |
| programming | `4.2` | Create Content Views using Text, Image, Shape, |
| and/or Color | `4.3` | Implement Modifiers including, but not limited to, |
| and .resizable | `4.4` | Create Container Views (HStack, VStack, ZStack, Spacer) |
| and arrange Views inside of Stack Views | `4.5` | Explain the View hierarchy produced by a program |
| and arrange Views inside of Stack Views | `4.6` | Create and/or apply Interactive Views including, |

---

## Chiều 2 — Concept Coverage (Concept → LO)

- **Tổng số Concepts:** 39
- **Concepts có LO:** 39
- **Concepts chưa có LO:** 0

✅ **Tất cả concepts đều có ít nhất 1 LO.**

### Bảng Concept → LOs

| Concept | Name | LOs phụ trách |
|---|---|---|
| `USER_CENTERED_DESIGN` | User-Centered Design Process | `ULO-USER_CENTERED_DESIGN-01`, `CIO-USER_CENTERED_DESIGN-01`, `SIO-SWIFT-USER_CENTERED_DESIGN-01`, `SIO-SWIFT-USER_CENTERED_DESIGN-02` |
| `LIST_OPERATIONS` | List Operations | `ULO-LIST_OPERATIONS-01`, `CIO-LIST_OPERATIONS-01`, `SIO-SWIFT-LIST_OPERATIONS-01`, `SIO-SWIFT-LIST_OPERATIONS-02` |
| `PRIMITIVE_TYPE_DECLARATION` | Declaring Primitive Types | `ULO-PRIMITIVE_TYPE_DECLARATION-01`, `CIO-PRIMITIVE_TYPE_DECLARATION-01`, `SIO-SWIFT-PRIMITIVE_TYPE_DECLARATION-01`, `SIO-SWIFT-PRIMITIVE_TYPE_DECLARATION-02` |
| `COPYRIGHT_CREATIVE_COMMONS` | Copyright & Creative Commons | `ULO-COPYRIGHT_CREATIVE_COMMONS-01`, `CIO-COPYRIGHT_CREATIVE_COMMONS-01`, `SIO-SWIFT-COPYRIGHT_CREATIVE_COMMONS-01` |
| `DESIGN_THINKING_PROCESS` | Design Thinking & Human-Centered Innovation | `ULO-DESIGN_THINKING_PROCESS-01`, `CIO-DESIGN_THINKING_PROCESS-01`, `SIO-SWIFT-DESIGN_THINKING_PROCESS-01`, `SIO-SWIFT-DESIGN_THINKING_PROCESS-02` |
| `ERROR_MESSAGES_CONCEPT` | Interpreting Error Messages | `ULO-ERROR_MESSAGES_CONCEPT-01`, `CIO-ERROR_MESSAGES_CONCEPT-01`, `SIO-SWIFT-ERROR_MESSAGES_CONCEPT-01`, `SIO-SWIFT-ERROR_MESSAGES_CONCEPT-02` |
| `AI_BIAS` | Bias in AI | `ULO-AI_BIAS-01`, `CIO-AI_BIAS-01`, `SIO-SWIFT-AI_BIAS-01` |
| `RUNTIME_ERRORS` | Runtime Errors | `ULO-RUNTIME_ERRORS-01`, `CIO-RUNTIME_ERRORS-01`, `SIO-SWIFT-RUNTIME_ERRORS-01`, `SIO-SWIFT-RUNTIME_ERRORS-02` |
| `ASYNCHRONOUS_PROG_CONCEPT` | Asynchronous Programming | `ULO-ASYNCHRONOUS_PROG_CONCEPT-01`, `CIO-ASYNCHRONOUS_PROG_CONCEPT-01`, `SIO-SWIFT-ASYNCHRONOUS_PROG_CONCEPT-01`, `SIO-SWIFT-ASYNCHRONOUS_PROG_CONCEPT-02` |
| `IF_ELSE_STATEMENT` | If-Else Statement | `ULO-IF_ELSE_STATEMENT-01`, `CIO-IF_ELSE_STATEMENT-01`, `SIO-SWIFT-IF_ELSE_STATEMENT-01`, `SIO-SWIFT-IF_ELSE_STATEMENT-02` |
| `ARRAY_OPERATIONS` | Array Operations | `ULO-ARRAY_OPERATIONS-01`, `CIO-ARRAY_OPERATIONS-01`, `SIO-SWIFT-ARRAY_OPERATIONS-01`, `SIO-SWIFT-ARRAY_OPERATIONS-02` |
| `COLOR_THEORY` | Color Theory | `ULO-COLOR_THEORY-01`, `CIO-COLOR_THEORY-01`, `SIO-SWIFT-COLOR_THEORY-01`, `SIO-SWIFT-COLOR_THEORY-02` |
| `INHERITANCE_SYNTAX` | Inheritance Syntax | `ULO-INHERITANCE_SYNTAX-01`, `CIO-INHERITANCE_SYNTAX-01`, `SIO-SWIFT-INHERITANCE_SYNTAX-01`, `SIO-SWIFT-INHERITANCE_SYNTAX-02` |
| `WCAG_PRINCIPLES` | WCAG Principles (POUR) | `ULO-WCAG_PRINCIPLES-01`, `CIO-WCAG_PRINCIPLES-01`, `SIO-SWIFT-WCAG_PRINCIPLES-01`, `SIO-SWIFT-WCAG_PRINCIPLES-02` |
| `DIGITAL_FOOTPRINT` | Digital Footprint | `ULO-DIGITAL_FOOTPRINT-01`, `CIO-DIGITAL_FOOTPRINT-01`, `SIO-SWIFT-DIGITAL_FOOTPRINT-01` |
| `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `ULO-IMPLICIT_EXPLICIT_ANIMATION-01`, `CIO-IMPLICIT_EXPLICIT_ANIMATION-01`, `SIO-SWIFT-IMPLICIT_EXPLICIT_ANIMATION-01`, `SIO-SWIFT-IMPLICIT_EXPLICIT_ANIMATION-02` |
| `PHISHING_IDENTIFICATION` | Identifying Phishing Attempts | `ULO-PHISHING_IDENTIFICATION-01`, `CIO-PHISHING_IDENTIFICATION-01`, `SIO-SWIFT-PHISHING_IDENTIFICATION-01` |
| `CLASS_DEFINITION` | Class Definition | `ULO-CLASS_DEFINITION-01`, `CIO-CLASS_DEFINITION-01`, `SIO-SWIFT-CLASS_DEFINITION-01`, `SIO-SWIFT-CLASS_DEFINITION-02` |
| `FIRST_CLASS_FUNCTIONS_CONCEPT` | First-Class & Higher-Order Functions | `ULO-FIRST_CLASS_FUNCTIONS_CONCEPT-01`, `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01`, `SIO-SWIFT-FIRST_CLASS_FUNCTIONS_CONCEPT-01`, `SIO-SWIFT-FIRST_CLASS_FUNCTIONS_CONCEPT-02` |
| `LEVEL_LAYOUT` | Level Layout Design | `ULO-LEVEL_LAYOUT-01`, `CIO-LEVEL_LAYOUT-01`, `SIO-SWIFT-LEVEL_LAYOUT-01` |
| `FOR_LOOP` | For Loop | `ULO-FOR_LOOP-01`, `CIO-FOR_LOOP-01`, `SIO-SWIFT-FOR_LOOP-01`, `SIO-SWIFT-FOR_LOOP-02` |
| `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `ULO-REFERENCE_TYPE_DECLARATION-01`, `CIO-REFERENCE_TYPE_DECLARATION-01`, `SIO-SWIFT-REFERENCE_TYPE_DECLARATION-01`, `SIO-SWIFT-REFERENCE_TYPE_DECLARATION-02` |
| `ACCESS_MODIFIERS` | Access Modifiers | `ULO-ACCESS_MODIFIERS-01`, `CIO-ACCESS_MODIFIERS-01`, `SIO-SWIFT-ACCESS_MODIFIERS-01` |
| `SWITCH_CASE` | Switch-Case Statement | `ULO-SWITCH_CASE-01`, `CIO-SWITCH_CASE-01`, `SIO-SWIFT-SWITCH_CASE-01`, `SIO-SWIFT-SWITCH_CASE-02` |
| `COMPOSITION_PRINCIPLES` | Composition Principles | `ULO-COMPOSITION_PRINCIPLES-01`, `CIO-COMPOSITION_PRINCIPLES-01`, `SIO-SWIFT-COMPOSITION_PRINCIPLES-01`, `SIO-SWIFT-COMPOSITION_PRINCIPLES-02` |
| `ALGORITHMIC_BIAS_SOCIETY` | Algorithmic Bias in Society | `ULO-ALGORITHMIC_BIAS_SOCIETY-01`, `CIO-ALGORITHMIC_BIAS_SOCIETY-01`, `SIO-SWIFT-ALGORITHMIC_BIAS_SOCIETY-01` |
| `OBJECT_INSTANTIATION` | Object Instantiation | `ULO-OBJECT_INSTANTIATION-01`, `CIO-OBJECT_INSTANTIATION-01`, `SIO-SWIFT-OBJECT_INSTANTIATION-01`, `SIO-SWIFT-OBJECT_INSTANTIATION-02` |
| `EVENT_BASED_PROGRAMMING` | Event-Based Programming Model | `ULO-EVENT_BASED_PROGRAMMING-01`, `CIO-EVENT_BASED_PROGRAMMING-01`, `SIO-SWIFT-EVENT_BASED_PROGRAMMING-01`, `SIO-SWIFT-EVENT_BASED_PROGRAMMING-02` |
| `SYNTAX_ERRORS` | Syntax Errors | `ULO-SYNTAX_ERRORS-01`, `CIO-SYNTAX_ERRORS-01`, `SIO-SWIFT-SYNTAX_ERRORS-01` |
| `TYPOGRAPHY_AND_VISUAL_HIERARCHY` | Typography and Visual Hierarchy Systems | `ULO-TYPOGRAPHY_AND_VISUAL_HIERARCHY-01`, `CIO-TYPOGRAPHY_AND_VISUAL_HIERARCHY-01`, `SIO-SWIFT-TYPOGRAPHY_AND_VISUAL_HIERARCHY-01`, `SIO-SWIFT-TYPOGRAPHY_AND_VISUAL_HIERARCHY-02` |
| `TWO_WAY_BINDING` | Two-Way Data Binding | `ULO-TWO_WAY_BINDING-01`, `CIO-TWO_WAY_BINDING-01`, `SIO-SWIFT-TWO_WAY_BINDING-01`, `SIO-SWIFT-TWO_WAY_BINDING-02` |
| `BREAKPOINTS` | Using Breakpoints | `ULO-BREAKPOINTS-01`, `CIO-BREAKPOINTS-01`, `SIO-SWIFT-BREAKPOINTS-01`, `SIO-SWIFT-BREAKPOINTS-02` |
| `VERSION_CONTROL_WORKFLOW` | Version Control Workflow | `ULO-VERSION_CONTROL_WORKFLOW-01`, `CIO-VERSION_CONTROL_WORKFLOW-01`, `SIO-SWIFT-VERSION_CONTROL_WORKFLOW-01`, `SIO-SWIFT-VERSION_CONTROL_WORKFLOW-02` |
| `LOCAL_VIEW_STATE` | Local View State | `ULO-LOCAL_VIEW_STATE-01`, `CIO-LOCAL_VIEW_STATE-01`, `SIO-SWIFT-LOCAL_VIEW_STATE-01`, `SIO-SWIFT-LOCAL_VIEW_STATE-02` |
| `WIREFRAMING` | Wireframing | `ULO-WIREFRAMING-01`, `CIO-WIREFRAMING-01`, `SIO-SWIFT-WIREFRAMING-01`, `SIO-SWIFT-WIREFRAMING-02` |
| `LOGIC_ERRORS` | Logical Errors | `ULO-LOGIC_ERRORS-01`, `CIO-LOGIC_ERRORS-01`, `SIO-SWIFT-LOGIC_ERRORS-01`, `SIO-SWIFT-LOGIC_ERRORS-02` |
| `WHILE_LOOP` | While Loop | `ULO-WHILE_LOOP-01`, `CIO-WHILE_LOOP-01`, `SIO-SWIFT-WHILE_LOOP-01`, `SIO-SWIFT-WHILE_LOOP-02` |
| `OBJECT_PROPERTIES` | Object Properties/Attributes | `ULO-OBJECT_PROPERTIES-01`, `CIO-OBJECT_PROPERTIES-01`, `SIO-SWIFT-OBJECT_PROPERTIES-01`, `SIO-SWIFT-OBJECT_PROPERTIES-02` |
| `INFORMATION_CREDIBILITY` | Assessing Information Credibility | `ULO-INFORMATION_CREDIBILITY-01`, `CIO-INFORMATION_CREDIBILITY-01`, `SIO-SWIFT-INFORMATION_CREDIBILITY-01` |