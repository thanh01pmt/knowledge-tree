# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-22T14:38:48.052662+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 7 (0 lỗi, 7 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 8 |
| categories | 11 |
| topics | 12 |
| concepts | 18 |
| learning_objectives | 139 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 5 |
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 2 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (5) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| subjects | `DIGITAL_LITERACY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `DATA_PRIVACY_USER` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `FUNCTIONAL_PROG` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `TROUBLESHOOTING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| categories | `UI_UX_PROCESS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `CIO_INSUFFICIENT_SIO` (2) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-ITERATE-OVER-COLLECTION` | - | CIO 'Traverse Every Element of a Collection Using a Loop' (CIO-ITERATE-OVER-COLLECTION) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-EVALUATE-MODIFIER-ORDER` | - | CIO 'Predict How Modifier Order Affects Rendered Output' (CIO-EVALUATE-MODIFIER-ORDER) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
