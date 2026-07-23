# Báo cáo kiểm tra Knowledge Tree

- **Thời gian chạy:** 2026-07-23T09:15:43.936391+00:00
- **Kết quả:** ❌ FAIL
- **Tổng số issue:** 14 (14 lỗi, 0 cảnh báo)

## Số lượng node theo tầng

| Tầng | Số node |
|---|---|
| fields | 1 |
| subjects | 1 |
| categories | 1 |
| topics | 16 |
| concepts | 16 |
| learning_objectives | 89 |

## Tổng hợp theo rule

| Rule | Mô tả | Số lượng |
|---|---|---|
| `BROKEN_REFERENCE` | Tham chiếu tới code không tồn tại ở bảng cha | 7 |
| `LO_CONCEPT_NOT_IN_PROJECT` | concept_codes của LO chứa code không tồn tại trong concepts.tsv của project | 7 |

## ❌ Lỗi (ERROR) — cần sửa

### `BROKEN_REFERENCE` (7) — Tham chiếu tới code không tồn tại ở bảng cha

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-VUE-WATCHERS-VUEUSE-UTILITIES` | concept_codes | 'COMPOSITION_REACTIVITY_API' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VUE-FORMKIT-VUELIDATE-RULES` | concept_codes | 'VUE_FORM_VALIDATION_RULES' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VUE-QUASAR-VITEPRESS-SSG` | concept_codes | 'NUXTJS_SSR_FULLSTACK' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VUE-VITEST-CYPRESS-PLAYWRIGHT` | concept_codes | 'VUE_TESTING_UTILS_VITEST' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VUE-APOLLO-TANSTACK-QUERY` | concept_codes | 'PINIA_CENTRALIZED_STORE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VUE-CAPACITOR-MOBILE-DEPLOY` | concept_codes | 'VUE_TELEPORT_KEEPALIVE' không tồn tại trong bảng cha. |
| learning_objectives | `SIO-VUE-DEVTOOLS-DEBUGGING` | concept_codes | 'COMPOSITION_REACTIVITY_API' không tồn tại trong bảng cha. |

### `LO_CONCEPT_NOT_IN_PROJECT` (7) — concept_codes của LO chứa code không tồn tại trong concepts.tsv của project

| Tầng | Code | Cột | Chi tiết |
|---|---|---|---|
| learning_objectives | `SIO-VUE-WATCHERS-VUEUSE-UTILITIES` | concept_codes | concept_code 'COMPOSITION_REACTIVITY_API' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-VUE-FORMKIT-VUELIDATE-RULES` | concept_codes | concept_code 'VUE_FORM_VALIDATION_RULES' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-VUE-QUASAR-VITEPRESS-SSG` | concept_codes | concept_code 'NUXTJS_SSR_FULLSTACK' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-VUE-VITEST-CYPRESS-PLAYWRIGHT` | concept_codes | concept_code 'VUE_TESTING_UTILS_VITEST' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-VUE-APOLLO-TANSTACK-QUERY` | concept_codes | concept_code 'PINIA_CENTRALIZED_STORE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-VUE-CAPACITOR-MOBILE-DEPLOY` | concept_codes | concept_code 'VUE_TELEPORT_KEEPALIVE' không tồn tại trong concepts.tsv của project. |
| learning_objectives | `SIO-VUE-DEVTOOLS-DEBUGGING` | concept_codes | concept_code 'COMPOSITION_REACTIVITY_API' không tồn tại trong concepts.tsv của project. |

## ⚠️ Cảnh báo (WARNING)

_Không có._
