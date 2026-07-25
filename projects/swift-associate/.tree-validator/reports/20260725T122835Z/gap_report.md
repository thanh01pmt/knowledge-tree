# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-25T12:28:35.100042+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

**11 concept(s) không có LO:**

| Code | Name | Parent Topic |
|---|---|---|
| `VIEW_CONCEPT` | Khái Niệm View | `UI_CONTROLS` |
| `DATA_TYPES` | Kiểu Dữ Liệu | `PRIMITIVE_TYPES` |
| `CONTROL_FLOW` | Luồng Điều Khiển | `CONDITIONAL_LOGIC` |
| `TYPE_SYSTEM` | Hệ Thống Kiểu | `PRIMITIVE_TYPES` |
| `VISUAL_DESIGN` | Thiết Kế Trực Quan | `IDE_NAVIGATION` |
| `SECURITY_CHALLENGES` | Thách Thức Bảo Mật | `IDE_NAVIGATION` |
| `DEBUGGING` | Gỡ Lỗi | `DEBUGGING_TECHNIQUES` |
| `OBJECT_INSTANTIATION` | Object Instantiation | `IDE_NAVIGATION` |
| `EVENT_HANDLERS_CONCEPT` | Events and Event Handling | `IDE_NAVIGATION` |
| `OBJECT_PROPERTIES` | Object Properties/Attributes | `IDE_NAVIGATION` |
| `RETURN_VALUES_AND_SCOPE` | Return Values and Scope | `IDE_NAVIGATION` |

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

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

**9 candidate(s) từ Master Tree:**

| Score | Code | Name | Matching Keywords |
|---|---|---|---|
| 5.6 | `ARRAY_OPERATIONS` | Array Operations | `array`, `index`, `access` |
| 5.5 | `LOCAL_VIEW_STATE` | Local View State | `state`, `@state`, `view` |
| 5.2 | `POLYGON_MESH` | Polygonal Mesh (Vertex, Edge, Face) | `edge`, `face` |
| 3.4 | `WHILE_LOOP` | While Loop | `condition`, `while`, `loop` |
| 3.1 | `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `error`, `syntax`, `errors` |
| 2.9 | `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `object`, `types` |
| 2.6 | `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `explicit` |
| 2.3 | `STACK_OPERATIONS` | Stack Operations (Push/Pop) | `stack` |
| 2.3 | `USER_PERSONAS` | Creating User Personas | `persona`, `user` |

**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`.