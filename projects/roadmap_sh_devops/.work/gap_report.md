# Gap Detection Report

- **Project:** `roadmap_sh_devops`
- **Generated:** 2026-07-23T08:41:06.044421+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

**1 concept(s) không có LO:**

| Code | Name | Parent Topic |
|---|---|---|
| `SYSTEM_MONITORING_LOGGING` | System Monitoring & Observability | `DEVOPS_PRACTICES` |

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
