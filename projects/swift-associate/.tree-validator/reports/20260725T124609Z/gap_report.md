# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-25T12:46:09.916613+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**

---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

**5 CIO(s) có < 2 SIO:**

| CIO Code | CIO Name | SIO Count | Parent ULO |
|---|---|---|---|
| `CIO-DATA_TYPES-03-01` | Chọn kiểu dữ liệu dựa trên miền giá trị và phép toán | ❌ 0 | `ULO-DATA_TYPES-03` |
| `CIO-DATA_TYPES-03-02` | Chuyển đổi kiểu dữ liệu bằng ánh xạ giá trị | ❌ 0 | `ULO-DATA_TYPES-03` |
| `CIO-CONTROL_FLOW-01-01` | Phân biệt ba cấu trúc luồng điều khiển cơ bản | ❌ 0 | `ULO-CONTROL_FLOW-01` |
| `CIO-CONTROL_FLOW-01-02` | Mô tả thứ tự thực thi dựa trên điều kiện | ❌ 0 | `ULO-CONTROL_FLOW-01` |
| `CIO-CONTROL_FLOW-02-01` | Theo dõi giá trị biến và thứ tự thực thi qua các nhánh | ❌ 0 | `ULO-CONTROL_FLOW-02` |

**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.
---

## Gap D — Marr's Test Violated CIOs (`MARR_VIOLATION`)

> CIO chứa từ khóa công nghệ, cú pháp hoặc cấu trúc ngôn ngữ cụ thể — vi phạm Phép thử Marr 2-Ngôn-ngữ.

**2 CIO(s) vi phạm tính Trung tính (Marr Test):**

| CIO Code | CIO Name | Detected Keywords / Patterns |
|---|---|---|
| `CIO-VISUAL_DESIGN-04-01` | Apply visual evaluation criteria to analyze interface design | `interface` |
| `CIO-OBJECT_INSTANTIATION_03-01` | So sánh khởi tạo trực tiếp và phương thức factory | `class` |

**→ Action:** Viết lại mô tả/tên CIO thành khái niệm/thủ tục trung tính 100% độc lập ngôn ngữ, hoặc chuyển xuống tầng SIO.
---

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

**13 candidate(s) từ Master Tree:**

| Score | Code | Name | Matching Keywords |
|---|---|---|---|
| 5.6 | `ARRAY_OPERATIONS` | Array Operations | `array`, `index`, `access` |
| 5.5 | `LOCAL_VIEW_STATE` | Local View State | `state`, `@state`, `view` |
| 5.2 | `POLYGON_MESH` | Polygonal Mesh (Vertex, Edge, Face) | `edge`, `face` |
| 4.5 | `STATE_PROPERTY_WRAPPER` | State Property Wrapper | `state`, `property`, `wrapper` |
| 3.4 | `WHILE_LOOP` | While Loop | `condition`, `while`, `loop` |
| 3.1 | `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `assets`, `project` |
| 3.1 | `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `error`, `syntax`, `errors` |
| 2.9 | `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `object`, `types` |
| 2.6 | `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `explicit` |
| 2.3 | `STACK_OPERATIONS` | Stack Operations (Push/Pop) | `stack` |
| 2.3 | `USER_PERSONAS` | Creating User Personas | `persona`, `user` |
| 2.3 | `DECLARATIVE_UI_PARADIGM` | Declarative UI Paradigm | `declarative` |
| 2.3 | `UI_MODIFIERS_CONCEPT` | UI Modifiers | `modifier`, `modifiers` |

**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`.