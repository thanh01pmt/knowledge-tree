# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T07:52:50.216560+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 30 (0 lỗi, 30 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 8 |
| categories | 10 |
| topics | 4 |
| concepts | 18 |
| learning_objectives | 48 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 16 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 11 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 2 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 1 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (16) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-CLIENT-SERVER-FLOW` | - | CIO 'Analyze Client Server Request Response Cycle' (CIO-CLIENT-SERVER-FLOW) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-HTTP-HEADER-STATUS` | - | CIO 'Understand HTTP Headers and Status Codes' (CIO-HTTP-HEADER-STATUS) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DNS-RECORD-TYPES` | - | CIO 'Configure DNS Record Types' (CIO-DNS-RECORD-TYPES) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CDN-EDGE-DELIVERY` | - | CIO 'Utilize CDN and Edge Networks' (CIO-CDN-EDGE-DELIVERY) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CRITICAL-RENDER-PATH` | - | CIO 'Analyze Critical Rendering Path' (CIO-CRITICAL-RENDER-PATH) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-BOX-SIZING-STRATEGY` | - | CIO 'Apply Box Sizing and Spacing' (CIO-BOX-SIZING-STRATEGY) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-GRID-CONTAINER-ALIGN` | - | CIO 'Align Items with Flexbox and Grid' (CIO-GRID-CONTAINER-ALIGN) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MEDIA-QUERIES-BREAK` | - | CIO 'Implement Breakpoints and Fluid Layout' (CIO-MEDIA-QUERIES-BREAK) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-LOCKFILE-VERSIONING` | - | CIO 'Manage Semantic Versioning and Lockfiles' (CIO-LOCKFILE-VERSIONING) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TREE-SHAKING-BUNDLING` | - | CIO 'Optimize Bundle Size with Tree Shaking' (CIO-TREE-SHAKING-BUNDLING) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-STATIC-LINT-RULES` | - | CIO 'Enforce Lint Rules and Code Style' (CIO-STATIC-LINT-RULES) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-PR-PULL-REQUEST-FLOW` | - | CIO 'Manage Code Review via Pull Requests' (CIO-PR-PULL-REQUEST-FLOW) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-COMPONENT-STATE-PROPS` | - | CIO 'Manage Component State and Props' (CIO-COMPONENT-STATE-PROPS) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-UNIT-E2E-STRATEGY` | - | CIO 'Implement Unit and End to End Tests' (CIO-UNIT-E2E-STRATEGY) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CORS-POLICY-HEADERS` | - | CIO 'Configure CORS Headers and Preflight' (CIO-CORS-POLICY-HEADERS) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TOKEN-SESSION-AUTH` | - | CIO 'Implement Token and Session Auth' (CIO-TOKEN-SESSION-AUTH) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |

### `ORPHAN_NODE` (11) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| subjects | `HCI` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| subjects | `UI_UX_DESIGN` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `DEVELOPMENT_ENVIRONMENT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `FRONTEND_DEV` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `LAYOUT_COMPOSITION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `NETWORK_SECURITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `TROUBLESHOOTING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `VERSION_CONTROL` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `WEB_FRAMEWORKS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ERROR_MESSAGES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TROUBLESHOOTING_METHODOLOGY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_CONCEPT_UNCOVERED` (2) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `ERROR_MESSAGES` | - | Concept 'Interpreting Error Messages' (ERROR_MESSAGES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `TROUBLESHOOTING_METHODOLOGY` | - | Concept 'Systematic Troubleshooting' (TROUBLESHOOTING_METHODOLOGY) không có LO nào trỏ đến trong learning-objectives.tsv. |

### `INCONSISTENT_LINE_ENDINGS` (1) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `learning-objectives.tsv` | - | File dùng line-ending LF, khác đa số các file khác (CRLF). |
