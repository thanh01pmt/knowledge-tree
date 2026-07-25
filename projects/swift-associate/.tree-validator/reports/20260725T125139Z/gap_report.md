# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-25T12:51:39.951594+00:00

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
| `CIO-VISUAL_DESIGN-04-01` | Apply visual evaluation criteria to analyze visual layout | ❌ 0 | `ULO-VISUAL_DESIGN-04` |
| `CIO-VISUAL_DESIGN-04-02` | Compare design against standard design principles to identify strengths and weaknesses | ❌ 0 | `ULO-VISUAL_DESIGN-04` |
| `CIO-SECURITY_CHALLENGES-01-01` | Classify security challenges based on origin and impact | ❌ 0 | `ULO-SECURITY_CHALLENGES-01` |
| `CIO-SECURITY_CHALLENGES-01-02` | Use a checklist of indicators to identify the type of security challenge | ❌ 0 | `ULO-SECURITY_CHALLENGES-01` |
| `CIO-SECURITY_CHALLENGES-02-01` | Analyze the impact of a security challenge on integrity, confidentiality, and availability | ❌ 0 | `ULO-SECURITY_CHALLENGES-02` |

**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.
---

## Gap D — Marr's Test Violated CIOs (`MARR_VIOLATION`)

> CIO chứa từ khóa công nghệ, cú pháp hoặc cấu trúc ngôn ngữ cụ thể — vi phạm Phép thử Marr 2-Ngôn-ngữ.

✅ **Tất cả CIOs đều đạt Phép thử Marr (100% Trung tính).**

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