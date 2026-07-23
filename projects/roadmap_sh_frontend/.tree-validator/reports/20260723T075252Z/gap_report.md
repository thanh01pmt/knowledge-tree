# Gap Detection Report

- **Project:** `roadmap_sh_frontend`
- **Generated:** 2026-07-23T07:52:52.514814+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

**2 concept(s) không có LO:**

| Code | Name | Parent Topic |
|---|---|---|
| `ERROR_MESSAGES` | Interpreting Error Messages | `DEBUGGING_TECH` |
| `TROUBLESHOOTING_METHODOLOGY` | Systematic Troubleshooting | `NET_LAYERS` |

**→ Action:** Thêm ít nhất 1 ULO + 1 CIO + 2 SIO cho mỗi concept trên.
---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

**16 CIO(s) có < 2 SIO:**

| CIO Code | CIO Name | SIO Count | Parent ULO |
|---|---|---|---|
| `CIO-CLIENT-SERVER-FLOW` | Analyze Client Server Request Response Cycle | ⚠️ 1 | `ULO-INTERNET-ARCHITECTURE` |
| `CIO-HTTP-HEADER-STATUS` | Understand HTTP Headers and Status Codes | ⚠️ 1 | `ULO-HTTP-SPECIFICATION` |
| `CIO-DNS-RECORD-TYPES` | Configure DNS Record Types | ⚠️ 1 | `ULO-DOMAIN-NAME-SYSTEM` |
| `CIO-CDN-EDGE-DELIVERY` | Utilize CDN and Edge Networks | ⚠️ 1 | `ULO-WEB-HOSTING-DEPL` |
| `CIO-CRITICAL-RENDER-PATH` | Analyze Critical Rendering Path | ⚠️ 1 | `ULO-BROWSER-RENDERING` |
| `CIO-BOX-SIZING-STRATEGY` | Apply Box Sizing and Spacing | ⚠️ 1 | `ULO-UI-BOX-MODEL` |
| `CIO-GRID-CONTAINER-ALIGN` | Align Items with Flexbox and Grid | ⚠️ 1 | `ULO-FLEX-GRID-LAYOUT` |
| `CIO-MEDIA-QUERIES-BREAK` | Implement Breakpoints and Fluid Layout | ⚠️ 1 | `ULO-RESPONSIVE-DESIGN` |
| `CIO-LOCKFILE-VERSIONING` | Manage Semantic Versioning and Lockfiles | ⚠️ 1 | `ULO-PACKAGE-MANAGEMENT` |
| `CIO-TREE-SHAKING-BUNDLING` | Optimize Bundle Size with Tree Shaking | ⚠️ 1 | `ULO-MODULE-BUNDLING` |
| `CIO-STATIC-LINT-RULES` | Enforce Lint Rules and Code Style | ⚠️ 1 | `ULO-CODE-STATIC-ANALYSIS` |
| `CIO-PR-PULL-REQUEST-FLOW` | Manage Code Review via Pull Requests | ⚠️ 1 | `ULO-VCS-PLATFORMS` |
| `CIO-COMPONENT-STATE-PROPS` | Manage Component State and Props | ⚠️ 1 | `ULO-FRONTEND-FRAMEWORKS` |
| `CIO-UNIT-E2E-STRATEGY` | Implement Unit and End to End Tests | ⚠️ 1 | `ULO-AUTOMATED-TESTING` |
| `CIO-CORS-POLICY-HEADERS` | Configure CORS Headers and Preflight | ⚠️ 1 | `ULO-CROSS-ORIGIN-SEC` |
| `CIO-TOKEN-SESSION-AUTH` | Implement Token and Session Auth | ⚠️ 1 | `ULO-WEB-AUTH-STRATEGIES` |

**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.
---

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

✅ **Không tìm thấy master concept nào có score ≥ 2.0 chưa được chọn.**
