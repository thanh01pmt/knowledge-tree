# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-25T14:38:38.714753+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 47 (32 lỗi, 15 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 4 |
| subjects | 9 |
| categories | 12 |
| topics | 16 |
| concepts | 42 |
| learning_objectives | 443 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 12 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 12 |
| `LO_TYPE_UNKNOWN` | lo_type không nằm trong tập giá trị cho phép | 6 |
| `CODE_FORMAT` | Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$ | 4 |
| `EMPTY_PARENT_REF` | Không có tham chiếu nào tới bảng cha (node lơ lửng) | 4 |
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 4 |
| `EMPTY_REQUIRED_FIELD` | Thiếu giá trị bắt buộc (code/name) | 2 |
| `LO_BROKEN_PARENT_REF` | parent_lo_code trỏ tới 1 LO không tồn tại | 2 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (12) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `.onChange(of: name) { newValue in print("Name changed to \(newValue)") }` | concept_codes | 'PROCEDURAL' không tồn tại trong bảng cha. |
| learning_objectives | `.onChange(of: isOn) { newValue in print("Toggle is now \(newValue ? "ON" : "OFF")") }` | concept_codes | 'PROCEDURAL' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_LAYOUT_MODIFIERS` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_STYLE_INTERACTION_MODIFIERS` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ORDER_PADDING_BEFORE_BACKGROUND` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ORDER_FONT_BEFORE_FOREGROUND` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMBINE_LAYOUT_MODIFIERS` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMBINE_APPEARANCE_MODIFIERS` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_PADDING_AND_ALIGNMENT` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_FRAME_AND_SIZE` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ORDER_PADDING_BACKGROUND` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ORDER_FRAME_CLIPPED` | concept_codes | 'UI_MODIFIERS' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (12) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `.onChange(of: name) { newValue in print("Name changed to \(newValue)") }` | concept_codes | concept_code 'PROCEDURAL' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `.onChange(of: isOn) { newValue in print("Toggle is now \(newValue ? "ON" : "OFF")") }` | concept_codes | concept_code 'PROCEDURAL' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_LAYOUT_MODIFIERS` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_STYLE_INTERACTION_MODIFIERS` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ORDER_PADDING_BEFORE_BACKGROUND` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ORDER_FONT_BEFORE_FOREGROUND` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMBINE_LAYOUT_MODIFIERS` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMBINE_APPEARANCE_MODIFIERS` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_PADDING_AND_ALIGNMENT` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_FRAME_AND_SIZE` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ORDER_PADDING_BACKGROUND` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ORDER_FRAME_CLIPPED` | concept_codes | concept_code 'UI_MODIFIERS' không tồn tại trong concepts.tsv của project. |

### `EMPTY_PARENT_REF` (4) — Không có tham chiếu nào tới bảng cha (node lơ lửng)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-BIND_STATE_TEXTFIELD_ONCHANGE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `TextField("Enter name", text: $name)` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `SIO-SWIFT-BIND_STATE_TOGGLE_ONCHANGE` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |
| learning_objectives | `Toggle("Enable", isOn: $isOn)` | concept_codes | Cột 'concept_codes' rỗng — node không có cha. |

### `EMPTY_REQUIRED_FIELD` (2) — Thiếu giá trị bắt buộc (code/name)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `TextField("Enter name", text: $name)` | name | Cột 'name' bị rỗng. |
| learning_objectives | `Toggle("Enable", isOn: $isOn)` | name | Cột 'name' bị rỗng. |

### `LO_BROKEN_PARENT_REF` (2) — parent_lo_code trỏ tới 1 LO không tồn tại

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `.onChange(of: name) { newValue in print("Name changed to \(newValue)") }` | parent_lo_code | parent_lo_code 'Apply' không tồn tại. |
| learning_objectives | `.onChange(of: isOn) { newValue in print("Toggle is now \(newValue ? "ON" : "OFF")") }` | parent_lo_code | parent_lo_code 'Apply' không tồn tại. |

## ⚠️ Cảnh báo (WARNING)

### `LO_TYPE_UNKNOWN` (6) — lo_type không nằm trong tập giá trị cho phép

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-SWIFT-BIND_STATE_TEXTFIELD_ONCHANGE` | lo_type | lo_type='' không thuộc ['CONCEPTUAL_IMPL', 'SPECIFIC_IMPL', 'UNIVERSAL']. |
| learning_objectives | `TextField("Enter name", text: $name)` | lo_type | lo_type='' không thuộc ['CONCEPTUAL_IMPL', 'SPECIFIC_IMPL', 'UNIVERSAL']. |
| learning_objectives | `.onChange(of: name) { newValue in print("Name changed to \(newValue)") }` | lo_type | lo_type='STATE_PROPERTY_WRAPPER' không thuộc ['CONCEPTUAL_IMPL', 'SPECIFIC_IMPL', 'UNIVERSAL']. |
| learning_objectives | `SIO-SWIFT-BIND_STATE_TOGGLE_ONCHANGE` | lo_type | lo_type='' không thuộc ['CONCEPTUAL_IMPL', 'SPECIFIC_IMPL', 'UNIVERSAL']. |
| learning_objectives | `Toggle("Enable", isOn: $isOn)` | lo_type | lo_type='' không thuộc ['CONCEPTUAL_IMPL', 'SPECIFIC_IMPL', 'UNIVERSAL']. |
| learning_objectives | `.onChange(of: isOn) { newValue in print("Toggle is now \(newValue ? "ON" : "OFF")") }` | lo_type | lo_type='STATE_PROPERTY_WRAPPER' không thuộc ['CONCEPTUAL_IMPL', 'SPECIFIC_IMPL', 'UNIVERSAL']. |

### `CODE_FORMAT` (4) — Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `TextField("Enter name", text: $name)` | - | Code 'TextField("Enter name", text: $name)' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `.onChange(of: name) { newValue in print("Name changed to \(newValue)") }` | - | Code '.onChange(of: name) { newValue in print("Name changed to \(newValue)") }' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `Toggle("Enable", isOn: $isOn)` | - | Code 'Toggle("Enable", isOn: $isOn)' không khớp định dạng ^[A-Z0-9_-]+$. |
| learning_objectives | `.onChange(of: isOn) { newValue in print("Toggle is now \(newValue ? "ON" : "OFF")") }` | - | Code '.onChange(of: isOn) { newValue in print("Toggle is now \(newValue ? "ON" : "OFF")") }' không khớp định dạng ^[A-Z0-9_-]+$. |

### `CIO_INSUFFICIENT_SIO` (4) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT` | - | CIO 'Bind state to UI element and observe changes' (CIO-STATE_PROPERTY_WRAPPER-BIND_STATE_UI_ELEMENT) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE` | - | CIO 'Mô tả trạng thái mong muốn' (CIO-DECLARATIVE_UI_PARADIGM-DESCRIBE_DESIRED_STATE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE` | - | CIO 'So sánh luồng điều khiển khai báo và mệnh lệnh' (CIO-DECLARATIVE_UI_PARADIGM-COMPARE_DECLARATIVE_IMPERATIVE) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW` | - | CIO 'Xây dựng cấu trúc view phân cấp' (CIO-DECLARATIVE_UI_PARADIGM-BUILD_HIERARCHICAL_VIEW) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |

### `ORPHAN_NODE` (1) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| topics | `DATA_BINDING` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
