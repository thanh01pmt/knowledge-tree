# Mapping Plan — App Development with Swift Associate

_Generated: 2026-08-02_  
_Project: swift-associate_  
_Source: Apple Associate - Objective Domains_0125.pdf_

---

## 📋 Overview

| Metric | Count |
|--------|-------|
| ATE Concept Candidates | 62 (41 matched, 21 Gap D) |
| PDF Objective Domains | 5 main domains, ~30 objectives |
| Master Tree Concepts Available | 271 |

---

## 1. ATE-Matched Concepts (from `/escalate-concepts`)

*All 41 matched concepts with `match_confidence >= 0.80` — ready to use `matched_master_code` directly.*

| Proposed Code | Master Code | Name (VI) | Confidence | Source |
|---|---|---|---|---|
| `DECLARATIVE_UI_PARADIGM` | `DECLARATIVE_UI_PARADIGM` | Xây dựng giao diện người dùng theo kiểu khai báo | 1.00 | ATE |
| `UI_MODIFIERS` | `UI_MODIFIERS_CONCEPT` | Áp dụng các hàm biến đổi giao diện | 0.95 | ATE |
| `STATE_PROPERTY_WRAPPER` | `LOCAL_VIEW_STATE` | Quản lý trạng thái cục bộ bằng property wrapper | 0.90 | ATE |
| `CROSS_ORIGIN_SECURITY` | `CROSS_ORIGIN_SECURITY` | Cơ chế bảo mật cross-origin (CORS) | 1.00 | ATE |
| `IDENTIFIER_NAMING_RULES` | `PRIMITIVE_TYPE_DECLARATION` | Quy tắc đặt tên định danh | 0.70 | ATE [VERIFY] |
| `TYPE_INFERENCE` | `REFERENCE_TYPE_DECLARATION` | Kiểu suy diễn | 0.70 | ATE [VERIFY] |
| `CONDITIONAL_LOGIC_IF_ELSE` | `IF_ELSE_STATEMENT` | Cấu trúc điều khiển rẽ nhánh if-else | 1.00 | ATE |
| `CONDITIONAL_LOGIC_SWITCH` | `SWITCH_CASE` | Cấu trúc chọn nhiều nhánh switch-case | 1.00 | ATE |
| `ITERATION_FOR_LOOP` | `FOR_LOOP` | Vòng lặp for | 1.00 | ATE |
| `ITERATION_WHILE_LOOP` | `WHILE_LOOP` | Vòng lặp while | 1.00 | ATE |
| `LOOP_CONTROL_FLOW` | `FOR_LOOP` | Điều khiển luồng vòng lặp | 0.60 | ATE [VERIFY] |
| `ARRAY_OPERATIONS` | `ARRAY_OPERATIONS` | Thao tác cơ bản trên mảng | 1.00 | ATE |
| `LIST_COLLECTIONS` | `LIST_OPERATIONS` | Danh sách/dynamic array | 1.00 | ATE |
| `PRIMITIVE_TYPES` | `PRIMITIVE_TYPE_DECLARATION` | Kiểu dữ liệu nguyên thủy | 1.00 | ATE |
| `REFERENCE_TYPES` | `REFERENCE_TYPE_DECLARATION` | Kiểu dữ liệu tham chiếu | 1.00 | ATE |
| `CONSTANTS_VARIABLES` | `PRIMITIVE_TYPE_DECLARATION` | Hằng số vs biến | 0.80 | ATE [VERIFY] |
| `OOP_CLASS_DEFINITION` | `CLASS_DEFINITION` | Định nghĩa lớp | 1.00 | ATE |
| `OOP_OBJECT_INSTANTIATION` | `OBJECT_INSTANTIATION` | Tạo thể hiện từ lớp | 1.00 | ATE |
| `OOP_INHERITANCE` | `INHERITANCE_SYNTAX` | Kế thừa | 1.00 | ATE |
| `OOP_ENCAPSULATION` | `ACCESS_MODIFIERS` | Đóng gói | 1.00 | ATE |
| `ERROR_HANDLING_SYNTAX` | `SYNTAX_ERRORS` | Lỗi cú pháp | 1.00 | ATE |
| `ERROR_HANDLING_RUNTIME` | `RUNTIME_ERRORS` | Lỗi runtime | 1.00 | ATE |
| `ERROR_HANDLING_LOGIC` | `LOGIC_ERRORS` | Lỗi logic | 1.00 | ATE |
| `DEBUGGING_TECHNIQUES` | `BREAKPOINTS` | Kỹ thuật gỡ lỗi | 1.00 | ATE |
| `ERROR_INTERPRETATION` | `ERROR_MESSAGES_CONCEPT` | Đọc và hiểu thông báo lỗi | 1.00 | ATE |
| `EVENT_DRIVEN_PROGRAMMING` | `EVENT_BASED_PROGRAMMING` | Mô hình lập trình hướng sự kiện | 1.00 | ATE |
| `ASYNCHRONOUS_PROGRAMMING` | `ASYNCHRONOUS_PROG_CONCEPT` | Lập trình bất đồng bộ | 1.00 | ATE |
| `FIRST_CLASS_FUNCTIONS` | `FIRST_CLASS_FUNCTIONS_CONCEPT` | Hàm first-class citizen | 1.00 | ATE |
| `FUNCTION_SYNTAX` | `PRIMITIVE_TYPE_DECLARATION` | Cú pháp hàm | 0.60 | ATE [VERIFY] |
| `PROPERTY_WRAPPER` | `STATE_PROPERTY_WRAPPER` | Property wrapper generic | 0.90 | ATE |
| `DATA_BINDING_TWO_WAY` | `TWO_WAY_BINDING` | Two-way data binding | 1.00 | ATE |
| `STATE_MANAGEMENT_PATTERNS` | `LOCAL_VIEW_STATE` | Mẫu quản lý trạng thái | 0.80 | ATE [VERIFY] |
| `UI_STACK_LAYOUT` | `LEVEL_LAYOUT` | Stack-based layout | 0.70 | ATE [VERIFY] |
| `UI_ANIMATION_TRANSITIONS` | `IMPLICIT_EXPLICIT_ANIMATION` | Animation & chuyển cảnh | 1.00 | ATE |
| `UI_ACCESSIBILITY` | `WCAG_PRINCIPLES` | Truy cập | 1.00 | ATE |
| `UI_COLOR_THEORY` | `COLOR_THEORY` | Màu sắc | 1.00 | ATE |
| `UI_TYPOGRAPHY` | `TYPOGRAPHY_AND_VISUAL_HIERARCHY` | Typography | 1.00 | ATE |
| `UI_COMPOSITION_PRINCIPLES` | `COMPOSITION_PRINCIPLES` | Nguyên tắc bố cục | 1.00 | ATE |
| `USER_CENTERED_DESIGN` | `USER_CENTERED_DESIGN` | Thiết kế lấy người dùng làm trung tâm | 1.00 | ATE |
| `WIREFRAMING_PROTOTYPING` | `WIREFRAMING` | Wireframe & Prototype | 1.00 | ATE |
| `DESIGN_THINKING_PROCESS` | `DESIGN_THINKING_PROCESS` | Design Thinking 5 bước | 1.00 | ATE |
| `DIGITAL_CITIZENSHIP` | `DIGITAL_FOOTPRINT` | Công dân số | 1.00 | ATE |
| `CYBERSECURITY_BASICS` | `PHISHING_IDENTIFICATION` | An ninh mạng cơ bản | 1.00 | ATE |
| `AI_ETHICS_BIAS` | `AI_BIAS` | Đạo đức AI | 1.00 | ATE |
| `IMPACT_OF_COMPUTING` | `ALGORITHMIC_BIAS_SOCIETY` | Tác động của điện toán | 0.80 | ATE [VERIFY] |
| `COPYRIGHT_LICENSING` | `COPYRIGHT_CREATIVE_COMMONS` | Bản quyền & licensing | 1.00 | ATE |
| `INFORMATION_CREDIBILITY` | `INFORMATION_CREDIBILITY` | Đánh giá độ tin cậy thông tin | 1.00 | ATE |
| `IDE_NAVIGATION_TOOLING` | `PROJECT_ASSETS_MANAGEMENT` | IDE tooling | 0.60 | ATE [VERIFY] |
| `SOURCE_CONTROL_GIT` | `VERSION_CONTROL_WORKFLOW` | Version control: Git | 1.00 | ATE |

---

## 2. Structured Hints (from PDF Objective Domains)

*Extracted from PDF document structure: 5 main domains with hierarchical objectives.*

### Domain 1: Planning and Design
| Objective | Text | Suggested Master Concepts |
|---|---|---|
| 1.1 | Summarize the design cycle (Brainstorm, plan, prototype, evaluate) | `DESIGN_THINKING_PROCESS`, `WIREFRAMING_PROTOTYPING` |
| 1.2 | Summarize how sensitive data can be protected and compromised | `CYBERSECURITY_BASICS`, `DIGITAL_CITIZENSHIP`, `COPYRIGHT_LICENSING` |
| 1.2.1 | Sharing personal and application information | `DIGITAL_CITIZENSHIP`, `IMPACT_OF_COMPUTING` |
| 1.2.2 | Security challenges | `CYBERSECURITY_BASICS` |
| 1.2.3 | Legal, ethical and socioeconomic impacts | `IMPACT_OF_COMPUTING`, `AI_ETHICS_BIAS`, `COPYRIGHT_LICENSING` |
| 1.3 | Assess a visual design with accessibility in mind | `UI_ACCESSIBILITY`, `UI_COMPOSITION_PRINCIPLES`, `USER_CENTERED_DESIGN` |

### Domain 2: Xcode Project Navigation
| Objective | Text | Suggested Master Concepts |
|---|---|---|
| 2.1 | Differentiate between basic file types | `IDE_NAVIGATION_TOOLING`, `PROJECT_ASSETS_MANAGEMENT` |
| 2.2 | After asset imported, recognize available assets | `PROJECT_ASSETS_MANAGEMENT` |
| 2.3 | Import and/or use an asset | `PROJECT_ASSETS_MANAGEMENT` |
| 2.4 | Select appropriate actions to configure UI areas | `UI_MODIFIERS`, `UI_CONTAINER_VIEWS`, `UI_NAVIGATION` |

### Domain 3: Swift Language Usage
| Objective | Text | Suggested Master Concepts |
|---|---|---|
| 3.1 | Write, call, evaluate execution of functions | `FUNCTION_SYNTAX`, `FIRST_CLASS_FUNCTIONS` |
| 3.1.1 | Evaluate argument labels, parameters, returns | `FUNCTION_SYNTAX`, `IDENTIFIER_NAMING_RULES` |
| 3.2 | Calculate results using operators | `ARITHMETIC_OPS` |
| 3.3 | Create and evaluate structures | `OOP_CLASS_DEFINITION`, `STRUCT_VALUE_SEMANTICS` |
| 3.3.1 | Declare properties of a structure | `OOP_CLASS_DEFINITION`, `PRIMITIVE_TYPES`, `REFERENCE_TYPES` |
| 3.3.2 | Initialize properties of a structure | `OOP_OBJECT_INSTANTIATION`, `CONSTANTS_VARIABLES` |
| 3.3.3 | Define methods | `OOP_CLASS_DEFINITION`, `FUNCTION_SYNTAX` |
| 3.3.4 | Create an instance of a structure | `OOP_OBJECT_INSTANTIATION` |
| 3.3.5 | Use an instance of a structure | `OOP_OBJECT_INSTANTIATION`, `OBJECT_PROPERTIES` |
| 3.4 | Create and manipulate arrays | `ARRAY_OPERATIONS`, `LIST_COLLECTIONS` |
| 3.4.1 | Declare/initialize array with values | `ARRAY_OPERATIONS`, `CONSTANTS_VARIABLES` |
| 3.4.2 | Identify/modify array element using index | `ARRAY_OPERATIONS` |
| 3.4.3 | Use/evaluate array properties and methods | `ARRAY_OPERATIONS`, `LIST_COLLECTIONS` |
| 3.5 | Demonstrate how to control flow of execution | `CONDITIONAL_LOGIC_IF_ELSE`, `CONDITIONAL_LOGIC_SWITCH`, `ITERATION_FOR_LOOP`, `ITERATION_WHILE_LOOP`, `LOOP_CONTROL_FLOW` |
| 3.5.1 | Create, analyze, predict loop structures and results | `LOOP_CONTROL_FLOW`, `ITERATION_FOR_LOOP`, `ITERATION_WHILE_LOOP` |
| 3.5.2 | Create and interpret outcome of conditional statements | `CONDITIONAL_LOGIC_IF_ELSE`, `CONDITIONAL_LOGIC_SWITCH` |
| 3.6 | Declare/evaluate constants and variables of different data types | `CONSTANTS_VARIABLES`, `PRIMITIVE_TYPES`, `REFERENCE_TYPES`, `TYPE_INFERENCE` |
| 3.6.1 | Differentiate between constants and variables | `CONSTANTS_VARIABLES` |
| 3.6.2 | Apply type inference | `TYPE_INFERENCE` |
| 3.6.3 | Use explicit typing | `TYPE_INFERENCE`, `IDENTIFIER_NAMING_RULES` |
| 3.7 | Use appropriate naming syntax | `IDENTIFIER_NAMING_RULES` |
| 3.7.1 | Use appropriate camel casing | `IDENTIFIER_NAMING_RULES` |
| 3.7.2 | Apply Swift identifier rules | `IDENTIFIER_NAMING_RULES` |

### Domain 4: View Building with SwiftUI
| Objective | Text | Suggested Master Concepts |
|---|---|---|
| 4.1 | Differentiate between imperative and declarative programming | `DECLARATIVE_UI_PARADIGM` |
| 4.2 | Create Content Views using Text, Image, Shape, Color | `UI_CONTAINER_VIEWS`, `UI_TYPOGRAPHY`, `UI_COLOR_THEORY` |
| 4.3 | Implement Modifiers (.padding, .background, .frame, .foregroundColor, .font, .resizable) | `UI_MODIFIERS` |
| 4.4 | Create Container Views (HStack, VStack, ZStack, Spacer) and arrange Views | `UI_STACK_LAYOUT`, `UI_CONTAINER_VIEWS`, `UI_BOX_MODEL_LAYOUT`, `FLEXBOX_GRID_LAYOUT` |
| 4.5 | Explain the View hierarchy produced by a program | `UI_STACK_LAYOUT`, `UI_CONTAINER_VIEWS`, `STATE_MANAGEMENT_PATTERNS` |
| 4.6 | Create/apply Interactive Views (Button, TextField, Slider, Toggle) | `UI_CONTAINER_VIEWS`, `EVENT_DRIVEN_PROGRAMMING`, `DATA_BINDING_TWO_WAY` |
| 4.7 | Use @State Property Wrapper to control appearance of a View | `STATE_PROPERTY_WRAPPER`, `PROPERTY_WRAPPER`, `STATE_MANAGEMENT_PATTERNS` |

### Domain 5: Debugging
| Objective | Text | Suggested Master Concepts |
|---|---|---|
| 5.1 | Differentiate between syntax and run-time errors | `SYNTAX_VS_RUNTIME_ERRORS`, `ERROR_HANDLING_SYNTAX`, `ERROR_HANDLING_RUNTIME` |
| 5.2 | Interpret error messages | `ERROR_INTERPRETATION`, `DEBUGGING_TECHNIQUES` |

---

## 3. [VERIFY] Low-Confidence Matches (0.60 ≤ confidence < 0.80)

| Proposed Code | Master Code | Confidence | Issue |
|---|---|---|---|
| `IDENTIFIER_NAMING_RULES` | `PRIMITIVE_TYPE_DECLARATION` | 0.70 | Master concept is about declaration, not naming conventions |
| `TYPE_INFERENCE` | `REFERENCE_TYPE_DECLARATION` | 0.70 | Master concept is about declaration, not inference |
| `LOOP_CONTROL_FLOW` | `FOR_LOOP` | 0.60 | Too broad, needs separate concept |
| `CONSTANTS_VARIABLES` | `PRIMITIVE_TYPE_DECLARATION` | 0.80 | Borderline — semantics different from declaration |
| `FUNCTION_SYNTAX` | `PRIMITIVE_TYPE_DECLARATION` | 0.60 | Function syntax ≠ variable declaration |
| `UI_STACK_LAYOUT` | `LEVEL_LAYOUT` | 0.70 | LEVEL_LAYOUT is game-specific, not general UI stack |
| `STATE_MANAGEMENT_PATTERNS` | `LOCAL_VIEW_STATE` | 0.80 | Master has local/shared separate, no unified pattern |
| `IMPACT_OF_COMPUTING` | `ALGORITHMIC_BIAS_SOCIETY` | 0.80 | Bias is subset, not full computing impact |
| `IDE_NAVIGATION_TOOLING` | `PROJECT_ASSETS_MANAGEMENT` | 0.60 | Different concern: navigation vs assets |

**Recommendation:** Create new concepts for all [VERIFY] items (promote to Gap D).

---

## 4. Gap D — New Node Proposals (21 + 9 promoted = 30 total)

### HIGH Priority (Core Curriculum Gaps)

| Proposed Code | Name (VI) | Parent Topic(s) | CS2023 KA | Rationale |
|---|---|---|---|---|
| `UI_BOX_MODEL_LAYOUT` | UI Box Model Layout System | `STACK_LAYOUT`, `GRID_LAYOUT`, `ADAPTIVE_LAYOUT` | HCI, GIT | Foundation for all layout systems |
| `FLEXBOX_GRID_LAYOUT` | Flexible & Grid Layout Systems | `GRID_LAYOUT`, `STACK_LAYOUT`, `ADAPTIVE_LAYOUT` | HCI, GIT | Modern responsive layout distinct from Stack |
| `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `IDE_NAVIGATION` | SDF | IDE asset workflow missing |
| `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `ERROR_MESSAGES`, `EXCEPTION_HANDLING` | SDF, SE | Pedagogically critical for beginners |
| `OOP_PROTOCOLS_INTERFACES` | Protocols & Interfaces | `CLASSES_OBJECTS`, `API_DESIGN` | SDF, FPL | Core to Swift POP |
| `STRUCT_VALUE_SEMANTICS` | Struct Value Semantics | `CLASSES_OBJECTS`, `REFERENCE_TYPES` | SDF, FPL | Fundamental value vs reference distinction |
| `UI_NAVIGATION` | UI Navigation | `IDE_NAVIGATION`, `HIERARCHICAL_NAVIGATION` | HCI | Core app architecture |
| `PROPERTY_WRAPPER` | Property Wrapper Pattern | `STATE_MANAGEMENT`, `OBSERVABLE_MODEL` | HCI, SDF | Generalizable decorator/aspect pattern |
| `STATE_MANAGEMENT_PATTERNS` | State Management Patterns | `STATE_MANAGEMENT`, `OBSERVABLE_MODEL` | HCI, SDF | Unifies local/shared/environment |
| `IMPACT_OF_COMPUTING` | Impact of Computing on Society | `USER_RESEARCH`, `DIGITAL_INTERACTION` | SEP | Broad SEP concept (bias is subset) |
| `DIGITAL_CITIZENSHIP` | Digital Citizenship | `PRIVACY_SETTINGS`, `DIGITAL_INTERACTION` | SEP | Comprehensive digital literacy |

### MEDIUM Priority

| Proposed Code | Name (VI) | Parent Topic(s) | CS2023 KA | Rationale |
|---|---|---|---|---|
| `CLOSURES_CAPTURE` | Closures & Capture Semantics | `FIRST_CLASS_FUNCTIONS` | FPL | Distinct from first-class functions |
| `UI_CONTAINER_VIEWS` | UI Container Views | `UI_CONTROLS`, `STACK_LAYOUT` | HCI | Group, Section, Form, List, ScrollView |
| `FUNCTION_SYNTAX` | Function Syntax & Semantics | `FUNC_SYNTAX`, `RETURN_VALUES` | SDF, FPL | Params, labels, return type, body |
| `LOOP_CONTROL_FLOW` | Loop Control Flow | `ITERATION_LOOPS`, `CONDITIONAL_LOGIC` | SDF | Break, continue, conditions |
| `CONSTANTS_VARIABLES` | Constants vs Variables Semantics | `PRIMITIVE_TYPES`, `REFERENCE_TYPES`, `VAR_CONSTANTS` | SDF | let/const vs var, scope, lifetime |
| `TYPE_INFERENCE` | Type Inference | `PRIMITIVE_TYPES`, `REFERENCE_TYPES`, `VAR_CONSTANTS`, `FUNC_SYNTAX` | SDF | Compiler deduces type from init |
| `IDENTIFIER_NAMING_RULES` | Identifier Naming Rules | `PRIMITIVE_TYPES`, `VAR_CONSTANTS` | SDF | camelCase, PascalCase, reserved |
| `APP_LIFECYCLE` | Application Lifecycle | `MEDIA_SERVICES`, `APP_DEPLOYMENT` | HCI, SDF | Launch, foreground, background, termination |
| `IDE_NAVIGATION_TOOLING` | IDE Navigation & Tooling | `IDE_NAVIGATION` | SDF | Navigator, debugger, refactoring |

### LOW Priority (SIO-level / Tech-specific)

| Proposed Code | Name (VI) | Note |
|---|---|---|
| `PLATFORM_SDK_IOS` | iOS/macOS Platform SDK | Apple-specific → SIO layer only |

---

## 5. Additional Taxonomy (from Context Audit + Master Search)

*Concepts already in Master Tree needed for full coverage but not in ATE candidates.*

| Master Code | Name | Domain | Why Needed |
|---|---|---|---|
| `ARITHMETIC_OPS` | Arithmetic Operations | 3.2 Calculate operators | Swift Language Usage |
| `COMPARISON_LOGICAL_OPS` | Comparison & Logical Operations | 3.2, 3.5.2 conditions | Swift Language Usage |
| `VAR_CONSTANTS` | Variables & Constants | 3.6, 3.6.1 | Swift Language Usage |
| `OBJECT_PROPERTIES` | Object Properties/Attributes | 3.3.1, 3.3.5 | Swift Language Usage |
| `INHERITANCE_POLY` | Inheritance & Polymorphism | 3.3 structures don't inherit, but concept exists | Future OOP |
| `ENCAPSULATION_ABSTRACTION` | Encapsulation & Abstraction | 3.3, access modifiers | Swift Language Usage |
| `DATA_BINDING` | Data Binding (general) | 4.6, 4.7 | SwiftUI binding |
| `GESTURE_HANDLING` | Gesture Handling | 4.6 Interactive Views | SwiftUI interaction |
| `MODAL_PRESENTATION` | Modal Presentation | 4.6 sheets, alerts | UI_NAVIGATION |
| `HIERARCHICAL_NAVIGATION` | Hierarchical Navigation | 4.5, 4.6 | UI_NAVIGATION |
| `RENDERING_CONCEPTS` | Rendering Concepts | 4.5 View hierarchy | UI rendering pipeline |

---

## 6. Proposed Topic Mapping for New Concepts

| New Concept | Primary Topic | Secondary Topics |
|---|---|---|
| `UI_BOX_MODEL_LAYOUT` | `STACK_LAYOUT` | `GRID_LAYOUT`, `ADAPTIVE_LAYOUT` |
| `FLEXBOX_GRID_LAYOUT` | `GRID_LAYOUT` | `STACK_LAYOUT`, `ADAPTIVE_LAYOUT` |
| `PROJECT_ASSETS_MANAGEMENT` | `IDE_NAVIGATION` | — |
| `SYNTAX_VS_RUNTIME_ERRORS` | `ERROR_MESSAGES` | `EXCEPTION_HANDLING` |
| `OOP_PROTOCOLS_INTERFACES` | `CLASSES_OBJECTS` | `API_DESIGN` |
| `STRUCT_VALUE_SEMANTICS` | `CLASSES_OBJECTS` | `REFERENCE_TYPES` |
| `UI_NAVIGATION` | `IDE_NAVIGATION` | `HIERARCHICAL_NAVIGATION` |
| `PROPERTY_WRAPPER` | `STATE_MANAGEMENT` | `OBSERVABLE_MODEL` |
| `STATE_MANAGEMENT_PATTERNS` | `STATE_MANAGEMENT` | `OBSERVABLE_MODEL` |
| `IMPACT_OF_COMPUTING` | `USER_RESEARCH` | `DIGITAL_INTERACTION` |
| `DIGITAL_CITIZENSHIP` | `PRIVACY_SETTINGS` | `DIGITAL_INTERACTION` |
| `CLOSURES_CAPTURE` | `FIRST_CLASS_FUNCTIONS` | — |
| `UI_CONTAINER_VIEWS` | `UI_CONTROLS` | `STACK_LAYOUT` |
| `FUNCTION_SYNTAX` | `FUNC_SYNTAX` | `RETURN_VALUES` |
| `LOOP_CONTROL_FLOW` | `ITERATION_LOOPS` | `CONDITIONAL_LOGIC` |
| `CONSTANTS_VARIABLES` | `VAR_CONSTANTS` | `PRIMITIVE_TYPES`, `REFERENCE_TYPES` |
| `TYPE_INFERENCE` | `PRIMITIVE_TYPES` | `REFERENCE_TYPES`, `VAR_CONSTANTS`, `FUNC_SYNTAX` |
| `IDENTIFIER_NAMING_RULES` | `PRIMITIVE_TYPES` | `VAR_CONSTANTS` |
| `APP_LIFECYCLE` | `MEDIA_SERVICES` | `APP_DEPLOYMENT` |
| `IDE_NAVIGATION_TOOLING` | `IDE_NAVIGATION` | — |

---

## ✅ Concept Codes for Build Tree (backtick-quoted for parser)

### Master Tree Concepts to Include (41 ATE-matched + 11 Additional = 52)

```
DECLARATIVE_UI_PARADIGM
UI_MODIFIERS_CONCEPT
LOCAL_VIEW_STATE
CROSS_ORIGIN_SECURITY
IF_ELSE_STATEMENT
SWITCH_CASE
FOR_LOOP
WHILE_LOOP
ARRAY_OPERATIONS
LIST_OPERATIONS
PRIMITIVE_TYPE_DECLARATION
REFERENCE_TYPE_DECLARATION
CLASS_DEFINITION
OBJECT_INSTANTIATION
INHERITANCE_SYNTAX
ACCESS_MODIFIERS
SYNTAX_ERRORS
RUNTIME_ERRORS
LOGIC_ERRORS
BREAKPOINTS
ERROR_MESSAGES_CONCEPT
EVENT_BASED_PROGRAMMING
ASYNCHRONOUS_PROG_CONCEPT
FIRST_CLASS_FUNCTIONS_CONCEPT
TWO_WAY_BINDING
IMPLICIT_EXPLICIT_ANIMATION
WCAG_PRINCIPLES
COLOR_THEORY
TYPOGRAPHY_AND_VISUAL_HIERARCHY
COMPOSITION_PRINCIPLES
USER_CENTERED_DESIGN
WIREFRAMING
DESIGN_THINKING_PROCESS
DIGITAL_FOOTPRINT
PHISHING_IDENTIFICATION
AI_BIAS
COPYRIGHT_CREATIVE_COMMONS
INFORMATION_CREDIBILITY
VERSION_CONTROL_WORKFLOW
ARITHMETIC_OPS
COMPARISON_LOGICAL_OPS
VAR_CONSTANTS
OBJECT_PROPERTIES
INHERITANCE_POLY
ENCAPSULATION_ABSTRACTION
DATA_BINDING
GESTURE_HANDLING
MODAL_PRESENTATION
HIERARCHICAL_NAVIGATION
RENDERING_CONCEPTS
```

### New Concepts to Add (Gap D — 20 HIGH+MEDIUM, excluding PLATFORM_SDK_IOS)

```
UI_BOX_MODEL_LAYOUT
FLEXBOX_GRID_LAYOUT
PROJECT_ASSETS_MANAGEMENT
SYNTAX_VS_RUNTIME_ERRORS
OOP_PROTOCOLS_INTERFACES
STRUCT_VALUE_SEMANTICS
UI_NAVIGATION
PROPERTY_WRAPPER
STATE_MANAGEMENT_PATTERNS
IMPACT_OF_COMPUTING
DIGITAL_CITIZENSHIP
CLOSURES_CAPTURE
UI_CONTAINER_VIEWS
FUNCTION_SYNTAX
LOOP_CONTROL_FLOW
CONSTANTS_VARIABLES
TYPE_INFERENCE
IDENTIFIER_NAMING_RULES
APP_LIFECYCLE
IDE_NAVIGATION_TOOLING
```

---

## Next Step

Upon approval, run `/build-tree` to generate:
- `projects/swift-associate/output/fields.tsv`
- `projects/swift-associate/output/subjects.tsv`
- `projects/swift-associate/output/categories.tsv`
- `projects/swift-associate/output/topics.tsv`
- `projects/swift-associate/output/concepts.tsv`
- `projects/swift-associate/output/learning-objectives.tsv`