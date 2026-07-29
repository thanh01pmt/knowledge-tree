# Taxonomy Mapping Plan: Swift Associate

Dựa trên bảng LO dự kiến tại `context-audit.md`, dưới đây là kế hoạch sử dụng và mở rộng Master Knowledge Tree.

## 1. Domain: Planning, Design & Security
**Phân tích LO:** Cần các Concept về Design Lifecycle, Accessibility, Security.
- **Field:** `HCC`, `IDC`
- **Subject:** `UI_UX_DESIGN`, `DIGITAL_CITIZENSHIP`
- **Category:** `UI_UX_PROCESS`, `DIGITAL_CITIZENSHIP`
- **Topic & Concept Mappings:**
  - **ULO-DESIGN-CYCLE** -> **Concept:** `USER_CENTERED_DESIGN`, `WIREFRAMING`, `PROTOTYPING` (Có sẵn)
  - **ULO-SEC-PRIVACY** -> **Concept:** `DIGITAL_IDENTITY`, `DIGITAL_FOOTPRINT`, `PASSWORD_STRENGTH_CONCEPT` (Có sẵn)
  - **ULO-ACCESSIBILITY** -> **Concept:** `WCAG_PRINCIPLES`, `SCREEN_READERS` (Có sẵn)
  - **ULO-SENSITIVE_DATA** -> **Concept:** `DIGITAL_IDENTITY`, `DIGITAL_FOOTPRINT`, `PASSWORD_STRENGTH_CONCEPT` (Có sẵn)
  - **ULO-SECURITY_CHALLENGES** -> **Concept:** `MALWARE_TYPES_CONCEPT`, `PHISHING_IDENTIFICATION`, `CROSS_ORIGIN_SECURITY` (Có sẵn)
  - **ULO-LEGAL_ETHICAL_SOCIOECONOMIC_IMPACTS** -> **Concept:** `ALGORITHMIC_BIAS_SOCIETY`, `AI_BIAS` (Có sẵn)

## 2. Domain: Xcode Project Navigation
**Phân tích LO:** Cần môi trường IDE, quản lý Assets, cấu hình giao diện.
- **Category:** `DEVELOPMENT_ENVIRONMENT` (Có sẵn - Subject: `SW_LIFECYCLE`)
- **Topic:** `IDE_NAVIGATION` (Có sẵn)
- **Concept:** `PROJECT_ASSETS_MANAGEMENT` (Có sẵn)

## 2.5. Domain: Swift Language Usage - Additional Concepts
**Phân tích LO:** Additional concepts from LO file mapped to Master Tree concepts
  - **Concepts for ULO-VARIABLES_AND_CONSTANTS:** `PRIMITIVE_TYPE_DECLARATION`, `REFERENCE_TYPE_DECLARATION` (Có sẵn)
  - **Concepts for ULO-NAMING_CONVENTIONS:** `PRIMITIVE_TYPE_DECLARATION`, `REFERENCE_TYPE_DECLARATION` (Có sẵn)
  - **Concepts for ULO-OPERATORS:** `PRIMITIVE_TYPE_DECLARATION` (Có sẵn)
  - **Concepts for ULO-STRUCTURE_TYPE:** `CLASS_DEFINITION`, `OBJECT_INSTANTIATION` (Có sẵn)
  - **Concepts for ULO-OBJECT_INSTANTIATION:** `OBJECT_INSTANTIATION`, `CLASS_DEFINITION` (Có sẵn)
  - **Concepts for ULO-OBJECT_PROPERTIES:** `OBJECT_PROPERTIES` (Có sẵn)
  - **Concepts for ULO-FUNCTIONS_AND_PROCEDURES:** `FIRST_CLASS_FUNCTIONS_CONCEPT` (Có sẵn)
  - **Concepts for ULO-IMPERATIVE_PROGRAMMING:** (Category: `SW_PARADIGMS`) (Có sẵn)
  - **Concepts for ULO-RETURN_VALUES_AND_SCOPE:** `RETURN_VALUES` (Có sẵn)
  - **Concepts for ULO-TYPE_SYSTEM:** `PRIMITIVE_TYPE_DECLARATION`, `REFERENCE_TYPE_DECLARATION` (Có sẵn)
  - **Concepts for ULO-DATA_TYPES:** `PRIMITIVE_TYPE_DECLARATION`, `REFERENCE_TYPE_DECLARATION` (Có sẵn)
  - **Concepts for ULO-CONTROL_FLOW:** (Category: `CONTROL_FLOW`) (Có sẵn)
  - **Concepts for ULO-CONDITIONAL_STATEMENTS:** `IF_ELSE_STATEMENT`, `SWITCH_CASE` (Có sẵn)
  - **Concepts for ULO-LOOP_STRUCTURES:** `FOR_LOOP`, `WHILE_LOOP` (Có sẵn)
  - **Concepts for ULO-ARRAYS:** `ARRAY_OPERATIONS` (Có sẵn)
  - **Concepts for ULO-DEBUGGING:** `BREAKPOINTS`, `LOGIC_ERRORS` (Có sẵn)

## 3. Domain: Swift Language Usage
**Phân tích LO:** Variables, Loops, Functions, Arrays, Conditionals, State Management.
- **Field:** `ASE`
- **Subject:** `PROG_FUNDAMENTALS`
- **Category & Topic Mappings:** Hoàn toàn tái sử dụng được Master Tree vì đây là nền tảng lập trình cơ bản.
  - **Category:** `VARIABLES_DATA_TYPES` (Có sẵn)
    - **Topic:** `PRIMITIVE_TYPES` -> **Concept:** `PRIMITIVE_TYPE_DECLARATION` (Có sẵn)
    - **Topic:** `REFERENCE_TYPES` -> **Concept:** `REFERENCE_TYPE_DECLARATION` (Có sẵn)
  - **Category:** `CONTROL_FLOW` (Có sẵn)
    - **Topic:** `CONDITIONAL_LOGIC` -> **Concept:** `IF_ELSE_STATEMENT`, `SWITCH_CASE` (Có sẵn)
    - **Topic:** `ITERATION_LOOPS` -> **Concept:** `FOR_LOOP`, `WHILE_LOOP` (Có sẵn)
  - **Category:** `DATA_STRUCTURES_BASIC` (Có sẵn)
    - **Topic:** `ARRAYS` -> **Concept:** `ARRAY_OPERATIONS` (Có sẵn)
  - **Category:** `FUNCTIONS_PROCEDURES` (Có sẵn)
    - **Topic:** `FUNC_SYNTAX` -> **Concept:** `FIRST_CLASS_FUNCTIONS_CONCEPT` (Có sẵn)
    - **Topic:** `RETURN_VALUES` -> **Concept:** `RETURN_VALUES` (Có sẵn)
  - **Category:** `TESTING_DEBUGGING` (Có sẵn)
    - **Topic:** `DEBUGGING_TECH` -> **Concept:** `BREAKPOINTS`, `LOGIC_ERRORS` (Có sẵn)
  - **Category:** `SW_PARADIGMS` (Có sẵn) - cho Imperative Programming context
  - **Category:** `STATE_DATA_FLOW` (Có sẵn)
    - **Topic:** `STATE_MANAGEMENT` -> **Concept:** `LOCAL_VIEW_STATE`, `STATE_PROPERTY_WRAPPER` (Có sẵn)
    - **Topic:** `DATA_BINDING` -> **Concept:** `TWO_WAY_BINDING` (Có sẵn)

## 4. Domain: View Building with SwiftUI
**Phân tích LO:** Declarative UI, Modifiers, State Management.
- **Field:** `MET`
- **Subject:** `NATIVE_APP_DEV`
- **Category:** `UI_BUILDING_BLOCKS`, `LAYOUT_COMPOSITION`, `STATE_DATA_FLOW` (Có sẵn).
- **Topic & Concept Mappings:**
  - **Concepts for ULO-DECLARATIVE-UI:** `DECLARATIVE_UI_PARADIGM` (Có sẵn, Topic: `UI_CONTROLS`)
  - **Concepts for ULO-UI-MODIFIERS:** `UI_MODIFIERS_CONCEPT` (Có sẵn, Topic: `UI_MODIFIERS`)
  - **Concepts for ULO-VIEW-CONCEPT:** `DECLARATIVE_UI_PARADIGM` (Có sẵn)
  - **Concepts for ULO-VIEW-HIERARCHY:** `UI_BOX_MODEL_LAYOUT`, `FLEXBOX_GRID_LAYOUT` (Có sẵn, Topic: `STACK_LAYOUT`, `GRID_LAYOUT`)
  - **Concepts for ULO-VISUAL-DESIGN:** `COLOR_THEORY`, `COMPOSITION_PRINCIPLES` (Có sẵn, Topic: `GRAPHIC_DESIGN_PRINCIPLES`)
  - **Concepts for ULO-COLOR:** `COLOR_THEORY` (Có sẵn)
  - **Concepts for ULO-SHAPE:** `COLOR_THEORY`, `COMPOSITION_PRINCIPLES` (Có sẵn)

## 5. Domain: Debugging
**Phân tích LO:** Lỗi cú pháp vs Runtime, đọc log.
- **Field:** `ASE`
- **Subject:** `SW_LIFECYCLE`
- **Category:** `TESTING_DEBUGGING` (Có sẵn)
- **Topic:** `DEBUGGING_TECH` (Có sẵn)
- **Concept Mappings:**
  - **Concepts for ULO-SYNTAX_ERRORS:** `SYNTAX_ERRORS` (Có sẵn, Topic: `ERROR_MESSAGES`)
  - **Concepts for ULO-RUNTIME_ERRORS:** `RUNTIME_ERRORS` (Có sẵn, Topic: `EXCEPTION_HANDLING`)
  - **Concepts for ULO-ERROR_MESSAGES:** `ERROR_MESSAGES_CONCEPT` (Có sẵn)
  - **Concepts for ULO-SYNTAX_VS_RUNTIME:** `SYNTAX_VS_RUNTIME_ERRORS` (Có sẵn)

## 6. Domain: Event Handling & Animation
**Phân tích LO:** Event-driven patterns, Animations.
- **Category:** `INTERACTION_EFFECTS` (Có sẵn)
- **Topic:** `UI_ANIMATION` (Có sẵn)
- **Concept Mappings:**
  - **ULO-IMPLICIT_EXPLICIT_ANIMATION** -> **Concept:** `IMPLICIT_EXPLICIT_ANIMATION`, `VIEW_TRANSITIONS` (Có sẵn)
  - **ULO-EVENT_HANDLERS** -> **Concept:** `EVENT_HANDLERS_CONCEPT`, `EVENT_BASED_PROGRAMMING` (Có sẵn, Topic: `EVENT_HANDLERS`)

---

*Ghi chú (Approval Gate):* 
- Tất cả concept codes trên đều **đã có sẵn trong Master Tree** (không cần `[NEW NODE PROPOSAL]`).
- Human chỉ cần xem xét và phê duyệt việc sử dụng mapping này.
- Sau khi được phê duyệt, Agent `@tree-assembler` sẽ dùng mapping này để xuất ra 6 file TSV cuối cùng của dự án.