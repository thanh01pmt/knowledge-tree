# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-08-01T13:38:21.986047+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

**35 concept(s) không có LO:**

| Code | Name | Parent Topic |
|---|---|---|
| `IF_ELSE_STATEMENT` | If-Else Statement | `CONDITIONAL_LOGIC` |
| `PRIMITIVE_TYPE_DECLARATION` | Declaring Primitive Types | `PRIMITIVE_TYPES` |
| `DIGITAL_FOOTPRINT` | Digital Footprint | `PRIVACY_SETTINGS` |
| `VIEW_TRANSITIONS` | View Transitions | `UI_ANIMATION` |
| `RUNTIME_ERRORS` | Runtime Errors | `EXCEPTION_HANDLING` |
| `WCAG_PRINCIPLES` | WCAG Principles (POUR) | `WCAG_STANDARDS` |
| `ALGORITHMIC_BIAS_SOCIETY` | Algorithmic Bias in Society | `USER_RESEARCH` |
| `PHISHING_IDENTIFICATION` | Identifying Phishing Attempts | `PHISHING_SCAMS` |
| `FOR_LOOP` | For Loop | `ITERATION_LOOPS` |
| `WIREFRAMING` | Wireframing | `WIREFRAMING_PROTOTYPING` |
| `LOGIC_ERRORS` | Logical Errors | `DEBUGGING_TECH` |
| `MALWARE_TYPES_CONCEPT` | Malware Types | `MALWARE_TYPES` |
| `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `UI_ANIMATION` |
| `UI_BOX_MODEL_LAYOUT` | UI Box Model Layout System | `STACK_LAYOUT` |
| `SWITCH_CASE` | Switch-Case Statement | `CONDITIONAL_LOGIC` |
| `SCREEN_READERS` | Screen Readers | `ASSISTIVE_TECH` |
| `LOCAL_VIEW_STATE` | Local View State | `STATE_MANAGEMENT` |
| `OBJECT_INSTANTIATION` | Object Instantiation | `CLASSES_OBJECTS` |
| `CLASS_DEFINITION` | Class Definition | `CLASSES_OBJECTS` |
| `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `REFERENCE_TYPES` |
| `USER_CENTERED_DESIGN` | User-Centered Design Process | `USER_RESEARCH` |
| `AI_BIAS` | Bias in AI | `USER_RESEARCH` |
| `SYNTAX_ERRORS` | Syntax Errors | `ERROR_MESSAGES` |
| `PASSWORD_STRENGTH_CONCEPT` | Strong Passwords | `PASSWORD_STRENGTH` |
| `PROTOTYPING` | Prototyping | `WIREFRAMING_PROTOTYPING` |
| `BREAKPOINTS` | Using Breakpoints | `DEBUGGING_TECH` |
| `OBJECT_PROPERTIES` | Object Properties/Attributes | `CLASSES_OBJECTS` |
| `COMPOSITION_PRINCIPLES` | Composition Principles | `GRAPHIC_DESIGN_PRINCIPLES` |
| `EVENT_BASED_PROGRAMMING` | Event-Based Programming Model | `EVENT_HANDLERS` |
| `TWO_WAY_BINDING` | Two-Way Data Binding | `DATA_BINDING` |
| `DIGITAL_IDENTITY` | Digital Identity Management | `PRIVACY_SETTINGS` |
| `FLEXBOX_GRID_LAYOUT` | Flexible & Grid Layout Systems | `GRID_LAYOUT` |
| `CROSS_ORIGIN_SECURITY` | Cross-Origin Security & Policies | `FIREWALLS_IDS` |
| `COLOR_THEORY` | Color Theory | `GRAPHIC_DESIGN_PRINCIPLES` |
| `FIRST_CLASS_FUNCTIONS_CONCEPT` | First-Class & Higher-Order Functions | `FIRST_CLASS_FUNCTIONS` |

**→ Action:** Thêm ít nhất 1 ULO + 1 CIO + 2 SIO cho mỗi concept trên.
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

**13 CIO(s) có vấn đề với marr_test_note:**

| CIO Code | CIO Name | Issue | Detail |
|---|---|---|---|
| `CIO-PROJECT_ASSETS_MANAGEMENT-01` | Phân loại tài nguyên dự án theo loại | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | Thêm tài nguyên vào cấu trúc dự án | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | Tham chiếu tài nguyên bằng tên định danh | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-03-01` | Duyệt mảng và truy cập từng phần tử | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ARRAY_OPERATIONS-03-02` | Sửa đổi mảng tại chỗ dựa trên điều kiện | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-03-01` | Lặp với điều kiện kiểm tra trước | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-WHILE_LOOP-03-02` | Lặp với điều kiện phụ thuộc đầu vào | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-DECLARATIVE_UI_PARADIGM-03` | So sánh khai báo và mệnh lệnh trong xây dựng giao diện | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-UI_MODIFIERS_CONCEPT-03` | Áp dụng modifier theo chuỗi để tạo kiểu giao diện | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-EVENT_HANDLERS_CONCEPT-02` | Gắn hàm xử lý sự kiện tương tác | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-STATE_PROPERTY_WRAPPER-02` | Khai báo và cập nhật biến trạng thái có giám sát | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | Phân loại lỗi dựa trên thời điểm phát hiện | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |
| `CIO-ERROR_MESSAGES_CONCEPT-02` | Giải thích thông báo lỗi dựa trên cấu trúc | MISSING_MARR_NOTE | CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6]) |

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