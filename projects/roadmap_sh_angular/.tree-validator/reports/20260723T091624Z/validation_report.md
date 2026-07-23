# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T09:16:24.797904+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 14 (14 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 1 |
| subjects | 1 |
| categories | 1 |
| topics | 20 |
| concepts | 20 |
| learning_objectives | 108 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 7 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 7 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (7) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-ANGULAR-VIEWPROVIDER-CONTENTCHILD` | concept_codes | 'CONTENT_PROLECTION_VIEWCHILD' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ANGULAR-RXJS-FILTERING-COMBINATION` | concept_codes | 'RXJS_REACTIVE_PROGRAMMING' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ANGULAR-ZONELESS-APPS-AOT` | concept_codes | 'SIGNALS_REACTIVE_STATE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ANGULAR-CLI-SETUP-BUILD-DEPLOY` | concept_codes | 'ANGULAR_CLI_SCHEMATICS_BUILD' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ANGULAR-CREATING-USING-LIBRARIES` | concept_codes | 'ANGULAR_MODULES_VS_STANDALONE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ANGULAR-ANALOGJS-META-FRAMEWORK` | concept_codes | 'ANGULAR_SSR_HYDRATION_UNIVERSAL' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-ANGULAR-LOCALIZE-MULTIPLE-LOCALES` | concept_codes | 'CUSTOM_PIPES_DATA_TRANSFORM' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (7) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-ANGULAR-VIEWPROVIDER-CONTENTCHILD` | concept_codes | concept_code 'CONTENT_PROLECTION_VIEWCHILD' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-ANGULAR-RXJS-FILTERING-COMBINATION` | concept_codes | concept_code 'RXJS_REACTIVE_PROGRAMMING' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-ANGULAR-ZONELESS-APPS-AOT` | concept_codes | concept_code 'SIGNALS_REACTIVE_STATE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-ANGULAR-CLI-SETUP-BUILD-DEPLOY` | concept_codes | concept_code 'ANGULAR_CLI_SCHEMATICS_BUILD' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-ANGULAR-CREATING-USING-LIBRARIES` | concept_codes | concept_code 'ANGULAR_MODULES_VS_STANDALONE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-ANGULAR-ANALOGJS-META-FRAMEWORK` | concept_codes | concept_code 'ANGULAR_SSR_HYDRATION_UNIVERSAL' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-ANGULAR-LOCALIZE-MULTIPLE-LOCALES` | concept_codes | concept_code 'CUSTOM_PIPES_DATA_TRANSFORM' không tồn tại trong concepts.tsv của project. |

## ⚠️ Cảnh báo (WARNING)

_Không có._
