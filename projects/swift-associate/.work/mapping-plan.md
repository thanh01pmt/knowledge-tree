# Taxonomy Mapping Plan: Swift Associate

Dựa trên bảng LO dự kiến tại `context-audit.md`, dưới đây là kế hoạch sử dụng và mở rộng Master Knowledge Tree.

## 1. Domain: Planning, Design & Security
**Phân tích LO:** Cần các Concept về Design Lifecycle, Accessibility, Security.
- **Field:** `HCC`, `IDC`
- **Subject:** `UI_UX_DESIGN`, `DIGITAL_CITIZENSHIP`
- **Category:** `DESIGN_ACCESSIBILITY`, `SECURITY_PRIVACY`
- **Topic & Concept Mappings:**
  - `ULO-DESIGN-CYCLE` -> **Concept:** `USER_CENTERED_DESIGN` (Có sẵn)
  - `ULO-SEC-PRIVACY` -> **Concept:** `DIGITAL_IDENTITY` (Có sẵn, có thể dùng tạm, hoặc đề xuất mới `DATA_PRIVACY`)

## 2. Domain: Xcode Project Navigation
**Phân tích LO:** Cần môi trường IDE, quản lý Assets, cấu hình giao diện.
- **[NEW NODE PROPOSAL] Category:** `DEVELOPMENT_ENVIRONMENT`
  - **Parent:** `SW_LIFECYCLE`
  - **Reason:** Master Tree chưa có Category nào nhóm các công cụ IDE chuyên dụng.
- **[NEW NODE PROPOSAL] Topic:** `IDE_NAVIGATION`
  - **Parent:** `DEVELOPMENT_ENVIRONMENT`
- **[NEW NODE PROPOSAL] Concept:** `PROJECT_ASSETS_MANAGEMENT`
  - **Parent:** `IDE_NAVIGATION`
  - **Reason:** Để chứa các LO như `CIO-XCODE-NAV`, `SIO-XCODE-ASSETS`.

## 3. Domain: Swift Language Usage
**Phân tích LO:** Variables, Loops, Functions, Arrays, Conditionals, State Management.
- **Field:** `ASE`
- **Subject:** `PROG_FUNDAMENTALS`
- **Category & Topic Mappings:** Hoàn toàn tái sử dụng được Master Tree vì đây là nền tảng lập trình cơ bản.
  - **Concepts:** `PRIMITIVE_TYPE_DECLARATION`, `REFERENCE_TYPE_DECLARATION`, `FIRST_CLASS_FUNCTIONS`, `ARRAY_OPERATIONS`, `FOR_LOOP`, `WHILE_LOOP`, `IF_ELSE_STATEMENT`, `SWITCH_CASE`, `TWO_WAY_BINDING`, `LOCAL_VIEW_STATE`

## 4. Domain: View Building with SwiftUI
**Phân tích LO:** Declarative UI, Modifiers, State Management.
- **Field:** `MET`
- **Subject:** `NATIVE_APP_DEV`
- **Category:** `UI_BUILDING_BLOCKS`, `LAYOUT_COMPOSITION`, `STATE_DATA_FLOW` (Có sẵn).
- **[NEW NODE PROPOSAL] Concept:** `DECLARATIVE_UI_PARADIGM`
  - **Parent:** `UI_BUILDING_BLOCKS` (Topic: `UI_COMPONENTS`)
  - **Reason:** Phục vụ `ULO-DECLARATIVE-UI`.
- **[NEW NODE PROPOSAL] Concept:** `UI_MODIFIERS`
  - **Parent:** `UI_BUILDING_BLOCKS`
  - **Reason:** Phục vụ `SIO-SWIFTUI-MODIFIERS`.
- **[NEW NODE PROPOSAL] Concept:** `STATE_PROPERTY_WRAPPER`
  - **Parent:** `STATE_DATA_FLOW` (Topic: `LOCAL_STATE`)
  - **Reason:** Đón các LO như `CIO-SWIFTUI-STATE`, `SIO-SWIFTUI-STATE-DECL`.

## 5. Domain: Debugging
**Phân tích LO:** Lỗi cú pháp vs Runtime, đọc log.
- **Field:** `ASE`
- **Subject:** `SW_LIFECYCLE`
- **Category:** `SOFTWARE_TESTING` (hoặc đề xuất mới)
- **[NEW NODE PROPOSAL] Topic:** `DEBUGGING_TECHNIQUES`
  - **Parent:** `SOFTWARE_TESTING`
- **[NEW NODE PROPOSAL] Concept:** `SYNTAX_VS_RUNTIME_ERRORS`
  - **Parent:** `DEBUGGING_TECHNIQUES`
  - **Reason:** Để chứa `CIO-SWIFT-ERRORS`.
- **Concept:** `ERROR_MESSAGES`

---
*Ghi chú (Approval Gate):* 
- Human cần xem xét và phê duyệt các mã `[NEW NODE PROPOSAL]` này.
- Sau khi được phê duyệt, Agent `@tree-assembler` sẽ bổ sung chúng vào `mlo-knowlege-tree.tsv` trước khi xuất ra 6 file TSV cuối cùng của dự án.
