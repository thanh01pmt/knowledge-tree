# Gap Detection Report

- **Project:** `roadmap_sh_backend`
- **Generated:** 2026-07-23T08:41:05.324897+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

**4 concept(s) không có LO:**

| Code | Name | Parent Topic |
|---|---|---|
| `HTTP_PROTOCOL` | HTTP Protocol & Specification | `BACKEND_ARCHITECTURE` |
| `BACKEND_AUTHENTICATION` | Backend Auth & Security | `BACKEND_ARCHITECTURE` |
| `CACHING_STRATEGIES` | Caching & Performance Optimization | `BACKEND_ARCHITECTURE` |
| `SYSTEM_DESIGN_SCALABILITY` | System Design & Microservices | `BACKEND_ARCHITECTURE` |

**→ Action:** Thêm ít nhất 1 ULO + 1 CIO + 2 SIO cho mỗi concept trên.
---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

✅ **Tất cả CIOs đều có ít nhất 2 SIO con.**

---

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

✅ **Không tìm thấy master concept nào có score ≥ 2.0 chưa được chọn.**
