# Academic Practices Applied — Pipeline v3 (Project Graph → Curriculum Graph → Roadmap)

> Ngày: 2026-08-08 | Nguồn: `scratch/project-graph-v3/`
> Tài liệu này tổng hợp **toàn bộ practice sư phạm/học thuật đã áp dụng** vào pipeline
> sinh roadmap học-by-building — mỗi practice gắn lý thuyết, cơ chế code, và bằng chứng đo được.

---

## 1. Tổng quan: 6 lý thuyết nền tảng → 6 cơ chế

| Lý thuyết | Cơ chế trong pipeline | Nơi triển khai |
|---|---|---|
| **Gagné** — Learning Hierarchies (học tích lũy, prerequisite) | Concept prerequisite DAG + LLM-as-judge lọc hub noise | `step35_curriculum.py::build_concept_dag` + `llm_judge_edges` |
| **Bruner** — Spiral Curriculum (khái niệm quay lại sâu hơn) | Bloom cap per concept encounter (lần 1 UNDERSTAND/APPLY, lần 2+ ANALYZE/CREATE) | `compute_concept_sequence` + prompt STEP 4 |
| **Reigeluth** — Elaboration Theory (epitome → elaborate) | Walking skeleton + `development_stages` narrative (6 giai đoạn) | STEP 1 `development_stages` + STEP 4 phase |
| **Vygotsky** — ZPD + Scaffolding | ZPD check: mỗi task có known concept (cầu nối) + giới hạn new concept | `zpd_check` |
| **Sweller** — Cognitive Load Theory | Intrinsic load gate: ≤ 2 concept mới/task → quá tải đề xuất tách | `zpd_check` (MAX_NEW_CONCEPTS_PER_TASK=2) |
| **Bloom** — Mastery Learning | Mastery gates giữa phase (acceptance criteria → gate) | `mastery_gates` |
| **Biggs** — Constructive Alignment | Mỗi LO gắn assessment từ task.acceptance (LO ↔ Assessment ↔ Activity) | `step4_roadmap.py::attach_assessments` |

---

## 2. Chi tiết từng practice + bằng chứng (Talky — SwiftUI chat app)

### 2.1 Gagné: Concept prerequisite DAG + LLM-as-judge

**Vấn đề ban đầu:** Master tree `lo_prerequisites.tsv` có 811 edges nhưng **810/811 là trong cùng concept** (Bloom progression), **0 cross-concept** — không có dữ liệu prerequisite giữa các concept khác nhau.

**Cơ chế (2 vòng):**
```
1. build_concept_dag(): DAG thô từ task_dependencies + knowledge_mapping
   (concept A ở task X, concept B ở task Y, X depends_on Y → A requires B)
   → 46 edges (23 cấu trúc conf 0.8 + 23 hub conf 0.5)
2. llm_judge_edges(): LLM xem concept description + task context
   → giữ 6/46, loại 40 (hub noise — "API_INTEGRATION requires mọi thứ" không phải prereq thật)
3. llm_generate_cross_concepts(): LLM sinh cross-concept còn thiếu (3 edges)
   → verify code (B dạy task trước A) → giữ 3
4. judge vòng 2: giữ 0/3 (đều noise) — loại hết
```

**Kết quả:** 6 edges sạch, **0 hub flag, 0 cần review người** — auto 100% qua LLM-as-judge.

**Bằng chứng edges giữ:** `SHARED_OBSERVABLE_STATE requires PUBLISHER_SUBSCRIBER_MODEL` (0.7), `UI_MODIFIERS_CONCEPT requires DECLARATIVE_UI_PARADIGM` (0.9), `TWO_WAY_BINDING requires DECLARATIVE_UI_PARADIGM` (0.8) — mọi edge có `judge_rationale`.

### 2.2 Bruner: Spiral Curriculum — Bloom cap per encounter

**Vấn đề:** LLM sinh LO bơm ANALYZE bừa bãi (28/102 LO) — task UI thuần cũng ANALYZE.

**Cơ chế:**
- `compute_concept_sequence`: đếm số lần concept xuất hiện theo thứ tự task → encounter 1 → cap UNDERSTAND, 2 → APPLY, 3+ → ANALYZE
- Prompt STEP 4 nhận `BLOOM_CAPS` → "concept gặp lần đầu chỉ UNDERSTAND/APPLY, KHÔNG ANALYZE/CREATE"

**Bằng chứng:** 0 vi phạm bloom cap (hậu kiểm đếm LO concept-mới mà ANALYZE/CREATE = 0). Spiral thật:
```
MEDIA_PICKER_API: T-IMAGE-PICKER(UNDERSTAND) → polish-gap-4(ANALYZE→CREATE)
KEY_VALUE_PERSISTENCE: T-PUSH-MANAGER(UNDERSTAND) → polish-gap-1(ANALYZE→CREATE)
ASYNC_PATTERNS: T-NOTIFICATION-MANAGER(APPLY) → polish-debt-1(CREATE)
```

### 2.3 Reigeluth: Elaboration Theory — development_stages narrative

**Vấn đề:** Phase = completion_level công thức → Firebase dồn lên FOUNDATION (vì REQ-SCAFFOLD LLM nhét Firebase vào base requirement).

**Cơ chế:** STEP 1 LLM sinh `development_stages` — 6 giai đoạn narrative cross-feature, mỗi giai đoạn:
- `product_state`: người dùng làm được gì (end-user, không mô tả repo)
- `need`: features/tasks triển khai
- `learn`: kiến thức học để làm được
- `cross_feature_value`: giá trị BỒI ĐẮP vào sản phẩm tổng thể (additive)
- `temporary_approach`: scaffold TẠM phi tuyến để test nhanh (non-linearity)
- `validation`: cách biết hoàn thành

**Phi tuyến (non-linearity) — điểm quan trọng:** dù App dùng Firebase cho session, giai đoạn test nhanh có thể thêm local storage tạm. Ví dụ LLM sinh:
```
🔧 Tạm dùng UID user cố định/hardcode để test realtime, giai đoạn 4 thay bằng NewChatView chọn user thật
🔧 Hardcode serverKey FCM trong source để test push nhanh; production nên chuyển lên Cloud Functions
```

**Sắp xếp theo logic HỌC TẬP (Reigeluth), không completion_level:**
- Giai đoạn 1 = NỀN TẢNG THUẦN (M2): làm quen Xcode IDE, Swift cơ bản, template, build chạy — **CẤM chức năng dự án** (WelcomeView/form/component/navigation)
- Giai đoạn 2 = UI + Firebase/Auth
- Giai đoạn 3-4 = chat realtime + new chat
- Giai đoạn 5-6 = profile/push + polish

### 2.4 Vygotsky: ZPD check

**Cơ chế:** mỗi task tính `new_concepts` (chưa gặp) vs `known_concepts` (đã gặp task trước):
- `OK` — có cầu nối kiến thức cũ → mới
- `NO_ZPD_BRIDGE` — ≥ 2 concepts và 0 known (nhảy cóc)
- `TOO_MANY_NEW` — > 2 concept mới (kết hợp Sweller)

**Điều chỉnh thực nghiệm quan trọng:** bản đầu flag mọi task 0 known (6/32) — **false positive**. Bài học: **1 concept mới = đúng ZPD** ("just beyond current capability"), chỉ nhiều concept mới đồng thời mới là vấn đề. Sau sửa: 32/32 OK.

### 2.5 Sweller: Cognitive Load Theory

**Cơ chế:** `MAX_NEW_CONCEPTS_PER_TASK = 2` — task có > 2 concept mới → TOO_MANY_NEW + đề xuất tách task. Lý do: nhiều khái niệm mới đồng thời vượt working memory giới hạn.

**Bằng chứng:** Talky 0 task TOO_MANY_NEW (STEP 1 sinh task đủ nhỏ — mỗi task 0-3 concepts).

### 2.6 Bloom: Mastery Learning — gates giữa phase

**Cơ chế:** `mastery_gates()` — giữa mỗi phase, gate = acceptance criteria của tasks trong phase (formative assessment).

**Quyết định thiết kế:** gate **gợi ý redo, không hard-block** — khác biệt quan trọng giữa tự học (không teacher) và lớp học truyền thống. Tránh frustration.

### 2.7 Biggs: Constructive Alignment

**Vấn đề:** 0/100 LO có assessment — LO không kế thừa task.acceptance.

**Cơ chế:** `attach_assessments()` — mỗi LO gắn assessment từ task.acceptance + outcome.user_visible. Vòng khép kín: LO dạy gì → task làm gì → gate đánh gì, là một.

**Kết quả:** 93/93 → 104/104 LO có assessment thật (không phải "concept-check" default).

---

## 3. Practice về CHẤT LƯỢNG DỮ LIỆU (agent sinh — không phải lý thuyết sư phạm nhưng quyết định chất lượng)

### 3.1 Deterministic mapping — root cause fix

**Vấn đề:** `task_stage_mapping` sinh bên trong STEP 4 → chạy lại mỗi lần → non-deterministic → phải vá hard rule "scaffold luôn FOUNDATION".

**Fix root cause:** mapping là **artifact sinh 1 lần, lưu vào graph** (như knowledge_mapping). STEP 4 đọc thuần. Verified: 2 lần chạy cùng kết quả.

### 3.2 setdefault mất node_id (lỗi 'Concept t7')

**Vấn đề:** keyword "Codable" xuất hiện ở t5/t6/t7, `setdefault` chỉ giữ node task đầu → t7 mất mapping → UI hiện "Concept t7".

**Fix:** `node_ids` SET per keyword → 1 mapping per node. Kết quả: 106→183 mappings, 0 task thiếu.

### 3.3 Truncate cố định ký tự = phá dữ liệu

**Vấn đề:** `[:60]` cắt "mật khẩu" → "mật k" (giữa từ); polish task action cắt 187→100 mất ý.

**Nguyên tắc:** truncate theo từ/câu (ellipsis), chỉ khi UI cần — **không bao giờ trong dữ liệu/API**. Đã bỏ toàn bộ truncate cứng ở output.

### 3.4 Validator nhanh (không LLM)

`validate_data.py` — 1 giây, bắt: task thiếu mapping, LO thiếu concept_code/assessment, phase rỗng, DAG cycle, ZPD vi phạm. **Phát hiện lỗi trước khi lên UI** (thay vì user thấy "Concept t7").

### 3.5 FACT vs INFERENCE (từ design v3)

- file/symbol/keyword = OBSERVED (verify bằng code tồn tại)
- architecture/pattern = INFERRED kèm confidence (≥ 0.7 khi có bằng chứng cấu trúc)

---

## 4. Practice UI/trình bày (lessons learned)

| Vấn đề | Root cause | Fix |
|---|---|---|
| "Concept Concept" | converter fallback literal "CONCEPT" | fallback = task_id |
| Hover popup cắt nội dung | `position: absolute; left:100%` tràn scroll container | `position: fixed` + clamp viewport + maxHeight 70vh |
| Popup "mất" dù còn chỗ | clamp đưa popup lên đầu màn hình (xa item đang nhìn) | popup hiện GẦN item (dưới/trên) |
| "mật k" | converter `[:60]` | bỏ truncate |
| Lộ trình phát triển chiếm chỗ | banner maxHeight 30% chèn giữa header/roadmap | absolute overlay + collapsible (mặc định thu gọn) |
| Keyword trùng (7 items cho 3 LO) | renderer gom LO theo concept toàn cục | dùng LO của task hiện tại |

---

## 5. Pipeline tổng thể (cách các practice ghép lại)

```
STEP 0b  Tree Advisor (LLM chọn file types từ tree — bỏ asset rác 47%)
STEP 1   Project Graph LLM (3 calls) — development_stages narrative (Reigeluth)
STEP 2   Verify (code — OBSERVED/INFERRED, 0 hallucination)
STEP 3   Standardize (LLM keyword→concept, node_ids set — deterministic)
STEP 3.5 Curriculum Graph:
         - Gagné DAG + judge 2 vòng (auto lọc hub noise)
         - Bruner spiral (bloom cap per encounter)
         - ZPD + Sweller checks
         - Bloom mastery gates
         - task_stage_mapping (lưu artifact — deterministic)
STEP 4   Roadmap (đọc mapping đã lưu, sinh LO với bloom caps + assessment Biggs)
validate_data.py (1 giây — gate chất lượng)
convert_to_viewer.py → UI
```

## 6. Chi phí LLM (đo thật, profile full)

| Giai đoạn | Calls | Input | Output | Thời gian |
|---|---|---|---|---|
| STEP 0b Tree Advisor | 1 | ~1.3k | ~7.3k | ~9s |
| STEP 1 (3 calls) | 3 | ~38k | ~45k | ~567s |
| STEP 3 | 1 | 16.4k | 21.8k | 130s |
| STEP 3.5 (judge×2 + cross + assign) | 4 | 6.2k | 45.5k | 291s |
| STEP 4 (batch-10 LO) | 4 | 8.9k | 55.3k | 368s |
| **Tổng** | **13** | **~70.8k** | **~175k** | **~23 phút** |

Cache: input lặp (source code) → prefix cache ấm giữa các call cùng profile.
