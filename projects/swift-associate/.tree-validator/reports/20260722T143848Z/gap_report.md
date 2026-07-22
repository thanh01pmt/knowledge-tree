# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-22T14:38:48.098289+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**

---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

**2 CIO(s) có < 2 SIO:**

| CIO Code | CIO Name | SIO Count | Parent ULO |
|---|---|---|---|
| `CIO-ITERATE-OVER-COLLECTION` | Traverse Every Element of a Collection Using a Loop | ⚠️ 1 | `ULO-DEFINITE-ITERATION` |
| `CIO-EVALUATE-MODIFIER-ORDER` | Predict How Modifier Order Affects Rendered Output | ⚠️ 1 | `ULO-VIEW-STYLING` |

**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.
---

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

**6 candidate(s) từ Master Tree:**

| Score | Code | Name | Matching Keywords |
|---|---|---|---|
| 7.3 | `OBJECT_PROPERTIES` | Object Properties/Attributes | `properties`, `state`, `object` |
| 5.2 | `POLYGON_MESH` | Polygonal Mesh (Vertex, Edge, Face) | `edge`, `face` |
| 4.1 | `OBJECT_INSTANTIATION` | Object Instantiation | `object`, `instance` |
| 2.6 | `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `explicit` |
| 2.3 | `STACK_OPERATIONS` | Stack Operations (Push/Pop) | `stack` |
| 2.3 | `USER_PERSONAS` | Creating User Personas | `persona`, `user` |

**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`.