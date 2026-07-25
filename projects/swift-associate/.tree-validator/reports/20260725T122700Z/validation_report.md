# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-25T12:27:00.439936+00:00
- **Kết quả:** ✅ PASS
- **Tổng số issue:** 33 (0 lỗi, 33 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 11 |
| topics | 15 |
| concepts | 36 |
| learning_objectives | 217 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 20 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 11 |
| `INCONSISTENT_LINE_ENDINGS` | File dùng line-ending khác với đa số các file còn lại | 2 |

## ❌ Lỗi (ERROR) — cần sửa

_Không có._

## ⚠️ Cảnh báo (WARNING)

### `ORPHAN_NODE` (20) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| topics | `ARRAYS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `DATA_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `ERROR_MESSAGES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `FIRST_CLASS_FUNCTIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `ITERATION_LOOPS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `REFERENCE_TYPES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `STATE_MANAGEMENT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `UI_MODIFIERS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| topics | `USER_RESEARCH` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `CONTROL_FLOW` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DATA_TYPES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DEBUGGING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `EVENT_HANDLERS_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_INSTANTIATION` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `OBJECT_PROPERTIES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `RETURN_VALUES_AND_SCOPE` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `SECURITY_CHALLENGES` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TYPE_SYSTEM` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VIEW_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VISUAL_DESIGN` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_CONCEPT_UNCOVERED` (11) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `VIEW_CONCEPT` | - | Concept 'Khái Niệm View' (VIEW_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DATA_TYPES` | - | Concept 'Kiểu Dữ Liệu' (DATA_TYPES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `CONTROL_FLOW` | - | Concept 'Luồng Điều Khiển' (CONTROL_FLOW) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `TYPE_SYSTEM` | - | Concept 'Hệ Thống Kiểu' (TYPE_SYSTEM) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `VISUAL_DESIGN` | - | Concept 'Thiết Kế Trực Quan' (VISUAL_DESIGN) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `SECURITY_CHALLENGES` | - | Concept 'Thách Thức Bảo Mật' (SECURITY_CHALLENGES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DEBUGGING` | - | Concept 'Gỡ Lỗi' (DEBUGGING) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `OBJECT_INSTANTIATION` | - | Concept 'Object Instantiation' (OBJECT_INSTANTIATION) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `EVENT_HANDLERS_CONCEPT` | - | Concept 'Events and Event Handling' (EVENT_HANDLERS_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `OBJECT_PROPERTIES` | - | Concept 'Object Properties/Attributes' (OBJECT_PROPERTIES) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `RETURN_VALUES_AND_SCOPE` | - | Concept 'Return Values and Scope' (RETURN_VALUES_AND_SCOPE) không có LO nào trỏ đến trong learning-objectives.tsv. |

### `INCONSISTENT_LINE_ENDINGS` (2) — File dùng line-ending khác với đa số các file còn lại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| _file | `concepts.tsv` | - | File dùng line-ending LF, khác đa số các file khác (CRLF). |
| _file | `learning-objectives.tsv` | - | File dùng line-ending LF, khác đa số các file khác (CRLF). |
