# Progress Report: Project Graph v3 — Curriculum-Aware Roadmap (LLM-as-Judge)

> **Ngày:** 2026-08-08 (cập nhật buổi chiều — sau `project-graph-v3-demoapp-first-sandbox.md`)
> **Phạm vi:** Curriculum Graph tầng (6 lý thuyết sư phạm) + LLM-as-judge auto + deterministic mapping + narrative development_stages
> **Vị trí:** `scratch/project-graph-v3/` — sandbox cô lập
> **Trạng thái:** 🟢 **HOÀN TẤT** — Talky (SwiftUI chat app) chạy end-to-end, roadmap curriculum-aware trên UI, `validate_data.py` PASS.

---

## 1. Bối cảnh chuỗi làm việc

Buổi sáng: hoàn tất STEP 0→4 cơ bản (task-aware roadmap, 8-domain graph, DemoApp-first) — ghi ở file progress trước.
Buổi chiều (file này): **phản biện sư phạm từ Human** dẫn đến 3 mảng lớn:

1. **"Sắp xếp bằng công thức hay context?"** → Firebase dồn lên FOUNDATION vì completion_level công thức → thay bằng `development_stages` narrative do LLM sinh
2. **"Cross-feature phát triển thế nào?"** → STEP 1 sinh 6 giai đoạn (product_state/need/learn/additive/temporary/validation)
3. **"Liệu phải sửa root cause hay vá triệu chứng?"** → task→stage mapping thành artifact lưu 1 lần (deterministic), bỏ hard rule

## 2. Gì đã làm (theo thứ tự)

### 2.1 Curriculum Graph tầng (B) — 6 lý thuyết → 6 cơ chế

| Lý thuyết | Cơ chế | Bằng chứng Talky |
|---|---|---|
| Gagné | Concept prerequisite DAG + judge 2 vòng | 46 edges thô → **6 sạch**, 0 hub, auto 100% |
| Bruner | Bloom cap per encounter | **0 vi phạm**; spiral thật (UNDERSTAND→CREATE) |
| Reigeluth | development_stages narrative | 6 giai đoạn (epitome → elaborate) |
| Vygotsky | ZPD check | 32/32 OK (sau sửa false positive: 1 concept mới = ZPD hợp lệ) |
| Sweller | ≤2 concept mới/task | 0 TOO_MANY_NEW |
| Bloom | Mastery gates | 3 gates (criteria từ acceptance) |
| Biggs | assessment per LO | 104/104 LO có assessment thật |

### 2.2 LLM-as-judge (auto 100%, 0 review người)

- `llm_judge_edges()`: lọc hub noise (46→6 edges, mọi edge có rationale)
- `llm_generate_cross_concepts()`: sinh cross-concept prereq (master 0/811) + verify code + judge vòng 2 (0/3 lọt)
- **Bài học:** judge bắt được "API_INTEGRATION requires X" là noise dù X hợp lý

### 2.3 Deterministic task→stage mapping (fix root cause)

- Trước: assign_stages_llm chạy trong STEP 4 → non-deterministic (scaffold lúc FOUNDATION lúc MVP) → phải vá hard rule
- Sau: mapping **lưu vào graph ở STEP 3.5**, STEP 4 đọc thuần — verified 2 lần chạy cùng kết quả, bỏ hard rule

### 2.4 Fix dữ liệu (agent sinh)

- `setdefault` mất node_id → t7 (ChatMessage model) 0 mapping → UI "Concept t7". Fix: `node_ids` set → **183 mappings, 0 task thiếu**
- Truncate cứng `[:60]` cắt "mật khẩu"→"mật k", polish action 187→100 — **bỏ toàn bộ truncate ở dữ liệu**
- `validate_data.py` (mới): validator 1 giây không LLM — task thiếu mapping, LO thiếu concept/assessment, phase rỗng, DAG cycle, ZPD

### 2.5 FOUNDATION = nền tảng thuần (M2) — feedback Human

- Trước: FOUNDATION chứa SecureTextField/WelcomeView (chức năng dự án)
- Sau: giai đoạn 1 = **làm quen Xcode IDE, Swift cơ bản, template, build chạy** — CẤM chức năng dự án; prompt STEP 1 rule 12 + assign_stages_llm rule 1 enforce
- FOUNDATION chỉ t1 (scaffold); MVP: SecureTextField/Firebase/AuthVM/Login/Register

### 2.6 UI fixes (browser-verified)

- Hover popup: fixed + clamp viewport + hiện gần item (4 lần sửa — root: absolute tràn scroll container; clamp đưa popup xa item)
- "Concept Concept" → task_id fallback; "mật k" → bỏ truncate
- Banner lộ trình: absolute overlay + collapsible (mặc định thu gọn 37px)
- Keyword trùng (7 items/3 LO): renderer gom toàn cục → LO task-local

## 3. Kết quả cuối (Talky)

```
[PASS] validate_data.py — 22 tasks | 183 mappings | 104 LOs — dữ liệu sạch
Roadmap: FOUNDATION(t1) → MVP(7) → EXTEND(9) → POLISH(16) | 6 development_stages
Viewer: 33 milestones | 16 concepts | 104 LOs | banner narrative collapsible
```

**Phases theo narrative (không completion_level):**
| Phase | Tasks | Ý nghĩa học tập |
|---|---|---|
| NỀN TẢNG | t1 scaffold | Làm quen IDE/Swift/template/build |
| MVP | SecureTextField, FirebaseManager, AuthVM, Login/Register, entry | UI đơn giản → backend → auth |
| MỞ RỘNG | models, RecentChat, ChatDetail, NewChat | Chat realtime + bắt đầu chat |
| HOÀN THIỆN | Profile/Push, ViewState, gaps/debts | Cá nhân hóa + chất lượng |

## 4. Chi phí LLM (đo thật, profile full)

**13 calls | ~70.8k input | ~175k output | ~23 phút** (chi tiết bảng ở `docs/ideas/academic-practices-applied.md` §6)

## 5. Docs sinh trong phiên

| File | Nội dung |
|---|---|
| `docs/ideas/academic-practices-applied.md` | **MỚI** — toàn bộ practice học thuật + dữ liệu + UI đã áp dụng, kèm bằng chứng |
| `docs/curriculum-graph-design-B.md` | Thiết kế Curriculum Graph (6 lý thuyết → 6 cơ chế) |
| `docs/pedagogy-theory-application.md` | Áp dụng lý thuyết — verified trên Talky |
| `docs/reconciliation-vs-main-docs.md` | Đối chiếu M1-M4 với docs main |

## 6. Còn lại / đề xuất

- [ ] Re-run full pipeline với prompt mới (STEP 1 development_stages chuẩn M2) — hiện sửa data tay + prompt, chưa re-run STEP 1
- [ ] Curriculum Graph cho project khác (test tính tổng quát — smart-bulb)
- [ ] Viewer: hiển thị mastery gates (data có, UI chưa)
- [ ] `assign_stages_llm` LLM map task→stage vẫn cần 1 call — có thể thay bằng rule nếu đủ ổn định

## 7. Commits

`f2aa3c1` development_stages + deterministic mapping · `6d304c3` hover popup · `e65c628` CONCEPT placeholder + popup fixed · `26ebff7` banner collapsible · `901c681` FOUNDATION nền tảng thuần
