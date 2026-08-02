# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-08-02T16:49:23.394491+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 423 (374 lỗi, 49 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 5 |
| subjects | 12 |
| categories | 25 |
| topics | 36 |
| concepts | 39 |
| learning_objectives | 547 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 187 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 187 |
| `CIO_INSUFFICIENT_SIO` | CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm | 28 |
| `LO_CONCEPT_UNCOVERED` | Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage) | 10 |
| `ORPHAN_NODE` | Node không được node nào ở tầng dưới tham chiếu tới | 10 |
| `LO_DESCRIPTION_PREFIX` | Mô tả LO không bắt đầu bằng 'Người học có khả năng' | 1 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (187) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_TRANSITIONS-01` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-VIEW_TRANSITIONS-02` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-MALWARE_TYPES_CONCEPT-01` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-MALWARE_TYPES_CONCEPT-02` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_BOX_MODEL_LAYOUT-01` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_BOX_MODEL_LAYOUT-02` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-UI_BOX_MODEL_LAYOUT-03` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SCREEN_READERS-01` | concept_codes | 'SCREEN_READERS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-SCREEN_READERS-02` | concept_codes | 'SCREEN_READERS' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PASSWORD_STRENGTH_CONCEPT-01` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PASSWORD_STRENGTH_CONCEPT-02` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PASSWORD_STRENGTH_CONCEPT-03` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROTOTYPING-01` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROTOTYPING-02` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-PROTOTYPING-03` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DIGITAL_IDENTITY-01` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DIGITAL_IDENTITY-02` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-DIGITAL_IDENTITY-03` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FLEXBOX_GRID_LAYOUT-01` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FLEXBOX_GRID_LAYOUT-02` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-FLEXBOX_GRID_LAYOUT-03` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CROSS_ORIGIN_SECURITY-01` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CROSS_ORIGIN_SECURITY-02` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `ULO-CROSS_ORIGIN_SECURITY-03` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-01` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-02` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-03` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-04` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-01` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-02` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-03` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-04` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-05` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-06` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-01` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-02` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-03` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-04` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-05` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-06` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROTOTYPING-01` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROTOTYPING-02` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROTOTYPING-02-01` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROTOTYPING-02-02` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROTOTYPING-03-01` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-PROTOTYPING-03-02` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-01` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-02` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-03` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-04` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-05` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-06` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-01` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-02` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-03` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-04` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-05` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-06` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-03` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-04` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-REFERENCE_IMAGE_BY_NAME` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-REFERENCE_COLOR_BY_NAME` | concept_codes | 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` | concept_codes | 'DECLARATIVE_UI_PARADIGM' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` | concept_codes | 'UI_MODIFIERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` | concept_codes | 'EVENT_HANDLERS_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DECLARE_STATE_PROPERTY` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` | concept_codes | 'STATE_PROPERTY_WRAPPER' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` | concept_codes | 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_TRANSITION_PURPOSE` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_TRANSITION_TYPE` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TRANSITION_SPEED` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TRANSITION_SMOOTHNESS` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_TRANSITION_FOR_NAVIGATION` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_TRANSITION_FOR_ALERT` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CREATE_FADE_TRANSITION` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CREATE_SLIDE_TRANSITION` | concept_codes | 'VIEW_TRANSITIONS' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SIMULATE_WORM_SPREAD` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_WORM_VIRUS` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_MALWARE_BY_TARGET` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SIMULATE_RANSOMWARE_ENCRYPTION` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_INFECTION_VECTOR_EMAIL` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRACE_POST_INFECTION_BEHAVIOR` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_MALWARE_BY_IMPACT` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SCORE_MALWARE_SEVERITY` | concept_codes | 'MALWARE_TYPES_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_PADDING_EFFECT` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_BORDER_EFFECT` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_CONTENT_BOX` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_BORDER_BOX` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CALCULATE_ACCUMULATED_SIZE` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CALCULATE_STACK_SIZE` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CALCULATE_BORDER_BOX_FRAME` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CALCULATE_FIXED_SIZE` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_SPACING_COLLAPSE` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_NESTED_PADDING` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_OVERLAP_PADDING` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_OVERLAP_BORDER` | concept_codes | 'UI_BOX_MODEL_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-LIST_CRITERIA_BY_CATEGORY` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CATEGORIZE_CRITERIA_WITH_ENUM` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-PRIORITIZE_CRITERIA_WITH_DICTIONARY` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-PRIORITIZE_WITH_ENUM_COMPARABLE` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-GENERATE_RANDOM_PASSWORD` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-GENERATE_PASSWORD_WITH_REQUIRED_TYPES` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRANSFORM_PASSPHRASE` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-TRANSFORM_WITH_RULESET` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SCORE_PASSWORD` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SCORE_WITH_WEIGHTED_CRITERIA` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_WITH_COMMON_PASSWORDS` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_WITH_PATTERNS` | concept_codes | 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_PROTOTYPE_FIDELITY_PURPOSE` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_PROTOTYPE_FIDELITY_BY_GOAL` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_PROTOTYPE_FIDELITY_FEATURES` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONTRAST_PROTOTYPE_FIDELITY_UX` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-BUILD_INTERACTION_FLOW` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONNECT_VIEWS_WITH_BINDING` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SIMULATE_UI_FEEDBACK` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ADD_STATE_CHANGES_WITH_ANIMATION` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_USER_FEEDBACK` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_UX_ISSUES_FROM_FEEDBACK` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ADJUST_PROTOTYPE_BASED_ON_CRITERIA` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-PRIORITIZE_CHANGES_IN_PROTOTYPE` | concept_codes | 'PROTOTYPING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-MODEL_DIGITAL_IDENTITY` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ENUM_IDENTITY_COMPONENTS` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_IDENTITY_INFO` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SWITCH_IDENTITY_CLASSIFICATION` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CAREER_OPPORTUNITY` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CORRELATION_ANALYSIS` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-RISK_ASSESSMENT_ENUM` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-INCONSISTENCY_DETECTION` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STRATEGY_COMPARISON_PROTOCOL` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-STRATEGY_ITERATION` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EFFECTIVENESS_SCORE` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-GOAL_MAPPING` | concept_codes | 'DIGITAL_IDENTITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_1D_2D_LAYOUT` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_1D_2D_BEHAVIOR` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_LAYOUT_FOR_NAV` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SELECT_LAYOUT_FOR_GRID` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ALIGN_ITEMS_HSTACK` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONFIGURE_GRID_ALIGNMENT` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DISTRIBUTE_SPACE_HSTACK` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-USE_FRAME_FOR_SIZING` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-NEST_HSTACK_IN_GRID` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-NEST_VSTACK_IN_HGRID` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_NESTED_LAYOUT` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DECOMPOSE_COMPLEX_LAYOUT` | concept_codes | 'FLEXBOX_GRID_LAYOUT' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_SAME_ORIGIN_POLICY` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EXPLAIN_CORS_BLOCKING` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CSRF_THREAT` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_XSS_THREAT` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-CONFIGURE_CORS_HEADERS` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-SET_ALLOWED_ORIGINS` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-VALIDATE_ORIGIN_HEADER` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-APPLY_DYNAMIC_CORS` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ASSESS_RESOURCE_SENSITIVITY` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-EVALUATE_TRUST_LEVEL` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-COMPARE_ATTACK_SCENARIOS` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-SWIFT-ANALYZE_OVERLY_PERMISSIVE_CORS` | concept_codes | 'CROSS_ORIGIN_SECURITY' không tồn tại trong bảng cha. |
| ... | ... | ... | (+174 dòng nữa) |

### `LO_CONCEPT_NOT_IN_PROJECT` (187) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROJECT_ASSETS_MANAGEMENT-03` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_MODIFIERS_CONCEPT-03` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-STATE_PROPERTY_WRAPPER-02` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_TRANSITIONS-01` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-VIEW_TRANSITIONS-02` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-MALWARE_TYPES_CONCEPT-01` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-MALWARE_TYPES_CONCEPT-02` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_BOX_MODEL_LAYOUT-01` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_BOX_MODEL_LAYOUT-02` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-UI_BOX_MODEL_LAYOUT-03` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SCREEN_READERS-01` | concept_codes | concept_code 'SCREEN_READERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-SCREEN_READERS-02` | concept_codes | concept_code 'SCREEN_READERS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PASSWORD_STRENGTH_CONCEPT-01` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PASSWORD_STRENGTH_CONCEPT-02` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PASSWORD_STRENGTH_CONCEPT-03` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROTOTYPING-01` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROTOTYPING-02` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-PROTOTYPING-03` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DIGITAL_IDENTITY-01` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DIGITAL_IDENTITY-02` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-DIGITAL_IDENTITY-03` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FLEXBOX_GRID_LAYOUT-01` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FLEXBOX_GRID_LAYOUT-02` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-FLEXBOX_GRID_LAYOUT-03` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CROSS_ORIGIN_SECURITY-01` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CROSS_ORIGIN_SECURITY-02` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `ULO-CROSS_ORIGIN_SECURITY-03` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-01` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-01` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROJECT_ASSETS_MANAGEMENT-03-02` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DECLARATIVE_UI_PARADIGM-03` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_MODIFIERS_CONCEPT-03` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-EVENT_HANDLERS_CONCEPT-02` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-STATE_PROPERTY_WRAPPER-02` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-SYNTAX_VS_RUNTIME_ERRORS-03` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-01` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-02` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-03` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-VIEW_TRANSITIONS-04` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-01` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-02` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-03` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-04` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-05` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-UI_BOX_MODEL_LAYOUT-06` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-01` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-02` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-03` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-04` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-05` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PASSWORD_STRENGTH_CONCEPT-06` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROTOTYPING-01` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROTOTYPING-02` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROTOTYPING-02-01` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROTOTYPING-02-02` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROTOTYPING-03-01` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-PROTOTYPING-03-02` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-01` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-02` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-03` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-04` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-05` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-DIGITAL_IDENTITY-06` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-01` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-02` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-03` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-04` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-05` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-FLEXBOX_GRID_LAYOUT-06` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-03` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-04` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ASSET_BY_TYPE` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_ASSET_TYPE_BY_EXTENSION` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ADD_IMAGE_TO_ASSET_CATALOG` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ADD_COLOR_SET_TO_ASSET_CATALOG` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-REFERENCE_IMAGE_BY_NAME` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-REFERENCE_COLOR_BY_NAME` | concept_codes | concept_code 'PROJECT_ASSETS_MANAGEMENT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_DECLARATIVE_IMPERATIVE` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONVERT_UIKIT_TO_SWIFTUI` | concept_codes | concept_code 'DECLARATIVE_UI_PARADIGM' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_TEXT` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_MODIFIER_CHAIN_IMAGE` | concept_codes | concept_code 'UI_MODIFIERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_BUTTON` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ATTACH_ACTION_TO_TOGGLE` | concept_codes | concept_code 'EVENT_HANDLERS_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DECLARE_STATE_PROPERTY` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-UPDATE_STATE_VIA_INTERACTION` | concept_codes | concept_code 'STATE_PROPERTY_WRAPPER' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DIFFERENTIATE_SYNTAX_RUNTIME` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_ERROR_FROM_CODE` | concept_codes | concept_code 'SYNTAX_VS_RUNTIME_ERRORS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_TRANSITION_PURPOSE` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_TRANSITION_TYPE` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TRANSITION_SPEED` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_TRANSITION_SMOOTHNESS` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_TRANSITION_FOR_NAVIGATION` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_TRANSITION_FOR_ALERT` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CREATE_FADE_TRANSITION` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CREATE_SLIDE_TRANSITION` | concept_codes | concept_code 'VIEW_TRANSITIONS' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SIMULATE_WORM_SPREAD` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_WORM_VIRUS` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_MALWARE_BY_TARGET` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SIMULATE_RANSOMWARE_ENCRYPTION` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_INFECTION_VECTOR_EMAIL` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRACE_POST_INFECTION_BEHAVIOR` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_MALWARE_BY_IMPACT` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SCORE_MALWARE_SEVERITY` | concept_codes | concept_code 'MALWARE_TYPES_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_PADDING_EFFECT` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_BORDER_EFFECT` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_CONTENT_BOX` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_BORDER_BOX` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CALCULATE_ACCUMULATED_SIZE` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CALCULATE_STACK_SIZE` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CALCULATE_BORDER_BOX_FRAME` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CALCULATE_FIXED_SIZE` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_SPACING_COLLAPSE` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_NESTED_PADDING` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_OVERLAP_PADDING` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_OVERLAP_BORDER` | concept_codes | concept_code 'UI_BOX_MODEL_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-LIST_CRITERIA_BY_CATEGORY` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CATEGORIZE_CRITERIA_WITH_ENUM` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-PRIORITIZE_CRITERIA_WITH_DICTIONARY` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-PRIORITIZE_WITH_ENUM_COMPARABLE` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-GENERATE_RANDOM_PASSWORD` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-GENERATE_PASSWORD_WITH_REQUIRED_TYPES` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRANSFORM_PASSPHRASE` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-TRANSFORM_WITH_RULESET` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SCORE_PASSWORD` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SCORE_WITH_WEIGHTED_CRITERIA` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_WITH_COMMON_PASSWORDS` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_WITH_PATTERNS` | concept_codes | concept_code 'PASSWORD_STRENGTH_CONCEPT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_PROTOTYPE_FIDELITY_PURPOSE` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_PROTOTYPE_FIDELITY_BY_GOAL` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_PROTOTYPE_FIDELITY_FEATURES` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONTRAST_PROTOTYPE_FIDELITY_UX` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-BUILD_INTERACTION_FLOW` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONNECT_VIEWS_WITH_BINDING` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SIMULATE_UI_FEEDBACK` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ADD_STATE_CHANGES_WITH_ANIMATION` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_USER_FEEDBACK` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-IDENTIFY_UX_ISSUES_FROM_FEEDBACK` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ADJUST_PROTOTYPE_BASED_ON_CRITERIA` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-PRIORITIZE_CHANGES_IN_PROTOTYPE` | concept_codes | concept_code 'PROTOTYPING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-MODEL_DIGITAL_IDENTITY` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ENUM_IDENTITY_COMPONENTS` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CLASSIFY_IDENTITY_INFO` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SWITCH_IDENTITY_CLASSIFICATION` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CAREER_OPPORTUNITY` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CORRELATION_ANALYSIS` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-RISK_ASSESSMENT_ENUM` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-INCONSISTENCY_DETECTION` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STRATEGY_COMPARISON_PROTOCOL` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-STRATEGY_ITERATION` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EFFECTIVENESS_SCORE` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-GOAL_MAPPING` | concept_codes | concept_code 'DIGITAL_IDENTITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DISTINGUISH_1D_2D_LAYOUT` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_1D_2D_BEHAVIOR` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_LAYOUT_FOR_NAV` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SELECT_LAYOUT_FOR_GRID` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ALIGN_ITEMS_HSTACK` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONFIGURE_GRID_ALIGNMENT` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DISTRIBUTE_SPACE_HSTACK` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-USE_FRAME_FOR_SIZING` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-NEST_HSTACK_IN_GRID` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-NEST_VSTACK_IN_HGRID` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_NESTED_LAYOUT` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DECOMPOSE_COMPLEX_LAYOUT` | concept_codes | concept_code 'FLEXBOX_GRID_LAYOUT' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-DESCRIBE_SAME_ORIGIN_POLICY` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EXPLAIN_CORS_BLOCKING` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_CSRF_THREAT` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_XSS_THREAT` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-CONFIGURE_CORS_HEADERS` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-SET_ALLOWED_ORIGINS` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-VALIDATE_ORIGIN_HEADER` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-APPLY_DYNAMIC_CORS` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ASSESS_RESOURCE_SENSITIVITY` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-EVALUATE_TRUST_LEVEL` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-COMPARE_ATTACK_SCENARIOS` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-SWIFT-ANALYZE_OVERLY_PERMISSIVE_CORS` | concept_codes | concept_code 'CROSS_ORIGIN_SECURITY' không tồn tại trong concepts.tsv của project. |
| ... | ... | ... | (+174 dòng nữa) |

## ⚠️ Cảnh báo (WARNING)

### `CIO_INSUFFICIENT_SIO` (28) — CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-01-DUP2` | - | CIO 'So sánh dựa trên vector lây nhiễm và hành vi sau lây nhiễm (malware, worm, ransomware, security, virus)' (CIO-MALWARE_TYPES_CONCEPT-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-MALWARE_TYPES_CONCEPT-02-DUP2` | - | CIO 'Phân loại theo mục tiêu tấn công và mức độ ảnh hưởng (malware, worm, ransomware, security, virus)' (CIO-MALWARE_TYPES_CONCEPT-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-01` | - | CIO 'Sử dụng cấu trúc rẽ nhánh dựa trên giá trị của biểu thức (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-01) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-02` | - | CIO 'Sử dụng cấu trúc rẽ nhánh với trường hợp mặc định và nhiều giá trị (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-02) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-03` | - | CIO 'Phân tích hành vi fall-through và break (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-03) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SWITCH_CASE-04` | - | CIO 'Phân tích xử lý trường hợp không khớp (default) (branching, switch-case, multi-way, selection)' (CIO-SWITCH_CASE-04) chỉ có 1 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-01-DUP2` | - | CIO 'So sánh chiến lược giảm thiểu thiên vị theo tiêu chí (training data, fairness, AI bias, ethics)' (CIO-AI_BIAS-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-AI_BIAS-02-DUP2` | - | CIO 'Đề xuất chiến lược dựa trên phân tích bối cảnh (training data, fairness, AI bias, ethics)' (CIO-AI_BIAS-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-02` | - | CIO 'Nhận diện lỗi cú pháp qua mẫu cấu trúc (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-03` | - | CIO 'Xác định vị trí lỗi dựa trên thông báo lỗi (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-04` | - | CIO 'Sửa lỗi cú pháp bằng cách điều chỉnh cấu trúc (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-05` | - | CIO 'Áp dụng quy trình sửa lỗi từng bước (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-06` | - | CIO 'Phân tích nguyên nhân gốc rễ của lỗi cú pháp phức tạp (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-SYNTAX_ERRORS-07` | - | CIO 'So sánh lỗi cú pháp với lỗi logic để xác định bản chất (compiler error, syntax error, parsing)' (CIO-SYNTAX_ERRORS-07) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01` | - | CIO 'Đồng bộ hóa dữ liệu giữa nguồn và giao diện theo cả hai hướng (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02` | - | CIO 'Khai báo liên kết hai chiều giữa thuộc tính và biến (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-03` | - | CIO 'So sánh luồng dữ liệu một chiều và hai chiều (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-04` | - | CIO 'Xác định tác động của liên kết hai chiều đến hiệu suất (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-01-DUP2` | - | CIO 'Phân tích overhead của đồng bộ dữ liệu hai chiều (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-TWO_WAY_BINDING-02-DUP2` | - | CIO 'So sánh chi phí cập nhật giữa binding một chiều và hai chiều (two-way binding, data binding, sync)' (CIO-TWO_WAY_BINDING-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-01-DUP2` | - | CIO 'Cấu hình quy tắc cho phép truy cập dựa trên nguồn gốc (security, same-origin, cross-origin, CORS)' (CIO-CROSS_ORIGIN_SECURITY-01-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-CROSS_ORIGIN_SECURITY-02-DUP2` | - | CIO 'Kiểm tra nguồn gốc yêu cầu và áp dụng chính sách động (security, same-origin, cross-origin, CORS)' (CIO-CROSS_ORIGIN_SECURITY-02-DUP2) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01` | - | CIO 'Mô tả đặc điểm của hàm như một giá trị có thể gán, truyền và trả về (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-01) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02` | - | CIO 'So sánh hàm với các kiểu dữ liệu khác về khả năng thao tác (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-02) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03` | - | CIO 'Sử dụng hàm nhận hàm khác làm đối số để thực hiện thao tác trên từng phần tử (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-03) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04` | - | CIO 'Xây dựng pipeline xử lý dữ liệu bằng cách kết hợp các hàm biến đổi (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-04) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05` | - | CIO 'Tạo hàm bao bọc nhận một hàm và trả về hàm mới với hành vi mở rộng (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-05) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |
| learning_objectives | `CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06` | - | CIO 'Thiết kế hàm nhận hàm xử lý và áp dụng nó trong một ngữ cảnh cụ thể (lambda, closure, higher-order function, first-class)' (CIO-FIRST_CLASS_FUNCTIONS_CONCEPT-06) chỉ có 0 SIO con (yêu cầu ≥ 2). Phân rã chưa đủ chi tiết thực hành. |

### `LO_CONCEPT_UNCOVERED` (10) — Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `LIST_OPERATIONS` | - | Concept 'List Operations' (LIST_OPERATIONS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `COPYRIGHT_CREATIVE_COMMONS` | - | Concept 'Copyright & Creative Commons' (COPYRIGHT_CREATIVE_COMMONS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `DESIGN_THINKING_PROCESS` | - | Concept 'Design Thinking & Human-Centered Innovation' (DESIGN_THINKING_PROCESS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `ASYNCHRONOUS_PROG_CONCEPT` | - | Concept 'Asynchronous Programming' (ASYNCHRONOUS_PROG_CONCEPT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `INHERITANCE_SYNTAX` | - | Concept 'Inheritance Syntax' (INHERITANCE_SYNTAX) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `LEVEL_LAYOUT` | - | Concept 'Level Layout Design' (LEVEL_LAYOUT) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `ACCESS_MODIFIERS` | - | Concept 'Access Modifiers' (ACCESS_MODIFIERS) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `TYPOGRAPHY_AND_VISUAL_HIERARCHY` | - | Concept 'Typography and Visual Hierarchy Systems' (TYPOGRAPHY_AND_VISUAL_HIERARCHY) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `VERSION_CONTROL_WORKFLOW` | - | Concept 'Version Control Workflow' (VERSION_CONTROL_WORKFLOW) không có LO nào trỏ đến trong learning-objectives.tsv. |
| concepts | `INFORMATION_CREDIBILITY` | - | Concept 'Assessing Information Credibility' (INFORMATION_CREDIBILITY) không có LO nào trỏ đến trong learning-objectives.tsv. |

### `ORPHAN_NODE` (10) — Node không được node nào ở tầng dưới tham chiếu tới

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| concepts | `ACCESS_MODIFIERS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `ASYNCHRONOUS_PROG_CONCEPT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `COPYRIGHT_CREATIVE_COMMONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `DESIGN_THINKING_PROCESS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `INFORMATION_CREDIBILITY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `INHERITANCE_SYNTAX` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LEVEL_LAYOUT` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `LIST_OPERATIONS` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `TYPOGRAPHY_AND_VISUAL_HIERARCHY` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |
| concepts | `VERSION_CONTROL_WORKFLOW` | - | Không có node nào ở tầng dưới tham chiếu tới node này. |

### `LO_DESCRIPTION_PREFIX` (1) — Mô tả LO không bắt đầu bằng 'Người học có khả năng'

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `ULO-LOGIC_ERRORS-02` | description | Mô tả không bắt đầu bằng 'Người học có khả năng...'. |
