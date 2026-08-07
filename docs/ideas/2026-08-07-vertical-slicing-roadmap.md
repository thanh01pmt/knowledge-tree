# Vertical Slicing Roadmap — Phase theo mức độ hoàn thiện sản phẩm

> **Ngày:** 2026-08-07  
> **Trạng thái:** ✅ Ý tưởng đã ghi nhận (bởi Human) — chưa implement  
> **Liên kết:** [`2026-08-06-action-roadmap.md`](./2026-08-06-action-roadmap.md) · [`2026-08-06-jit-knowledge-graph.md`](./2026-08-06-jit-knowledge-graph.md)

---

## 1. Vấn đề với cách chia phase hiện tại (Horizontal Layering)

Roadmap hiện tại chia phase theo **tầng công nghệ**:

```
P1: THIẾT LẬP (chỉ setup)
P2: DATA MODEL (data xong A-Z)
P3: AI CORE (AI xong A-Z)
P4: CẤU HÌNH
P5: UI (UI cuối cùng)
```

**Vấn đề:**
- Mỗi phase hoàn thiện 1 tầng từ A-Z, các phase sau không đụng vào tầng đó nữa
- **UI chỉ xuất hiện ở phase cuối** — học viên không "thấy" sản phẩm cho tới khi gần xong
- Mất động lực: học 4-5 phase mới thấy kết quả
- Không phản ánh cách dev thực tế làm việc (dev không làm hết data rồi mới làm UI)

---

## 2. Ý tưởng mới: Vertical Slicing

Phase chia theo **mức độ hoàn thiện sản phẩm** (product completeness), không theo tầng công nghệ.

### 2.1 So sánh

```
HORIZONTAL (cũ — bỏ)                          VERTICAL (mới — áp dụng)
─────────────────────────────                ─────────────────────────────
P1: THIẾT LẬP (chỉ setup)                    P0: NỀN TẢNG — làm quen công cụ
P2: DATA MODEL (data xong A-Z)                  ├─ Cài đặt Python, IDE, terminal
P3: AI CORE (AI xong A-Z)                       ├─ Cú pháp cơ bản (biến, if, for)
P4: CẤU HÌNH                                    ├─ Chạy script đầu tiên
P5: UI (UI cuối cùng)                           └─ Git init, cấu trúc dự án
                                             P1: MVP — sản phẩm CHẠY ĐƯỢC từ đầu
P1-P4: chưa thấy sản phẩm                        ├─ UI tối giản (1 ô nhập + 1 nút)
P5: mới thấy UI → học viên chán                 ├─ Logic đơn giản (3 câu hỏi mẫu)
                                                 └─ Data tạm (không lưu)
                                             P2: MỞ RỘNG — thêm chức năng
                                                 ├─ Lưu/đọc question bank
                                                 ├─ Gọi LLM thật
                                                 └─ UI đầy đủ hơn
                                             P3: HOÀN THIỆN — độ chắc
                                                 ├─ Error handling, retry
                                                 ├─ Test, edge cases
                                                 └─ Polish UI
```

### 2.2 Nguyên tắc

1. **Mỗi phase = 1 bước tiến thấy được của sản phẩm** (foundation → walking skeleton → meat → polish)
2. **P0 (Nền tảng)**: làm quen công cụ + ngôn ngữ ở mức đơn giản nhất + thiết lập dự án — chưa cần sản phẩm
3. **P1 (MVP) luôn có UI** (dù tối giản) — học viên "thấy" sản phẩm ngay từ đầu
4. **Phase sau mở rộng chức năng**, không làm lại từ đầu
5. **Cùng concept có thể xuất hiện ở nhiều phase** với mức nhận thức khác nhau

---

## 3. Bloom Level dọc theo roadmap (điểm mấu chốt)

Cùng concept (ví dụ JSON) xuất hiện nhiều lần với độ sâu tăng dần:

| Phase | Mức độ | Bloom | Ví dụ JSON |
|-------|--------|-------|------------|
| P0 (Nền tảng) | Nền tảng | Remember | Biến, kiểu dữ liệu, cú pháp cơ bản |
| P1 (MVP) | Nông | Understand | Đọc/parse JSON đơn giản |
| P2 (Mở rộng) | Trung bình | Apply | Ghi JSON file, asdict |
| P3 (Hoàn thiện) | Sâu | Create | Validate schema, xử lý lỗi, custom encoder |

→ Knowledge item cần field `bloom_level` (hoặc `depth`): `understand | apply | create`

**Hệ quả:** Kiến thức ở Phase 1 và Phase 4 dù cùng concept nhưng khác learning objective là hoàn toàn hợp lệ — không phải trùng lặp.

---

## 4. Cấu trúc phase mới (ví dụ AI Quiz Generator)

```
P0 (Nền tảng ~1h):  Làm quen công cụ & ngôn ngữ
  ├─ Cài đặt Python, IDE, terminal, PATH
  ├─ Cú pháp cơ bản: biến, if/else, vòng lặp, hàm
  ├─ Chạy script đầu tiên (print, input)
  └─ Git init, cấu trúc thư mục dự án, .gitignore

P1 (MVP ~1.5h):  Sản phẩm chạy được
  ├─ Tính năng tạo question (dataclass đơn giản)
  ├─ Tính năng generate (3 câu hỏi mẫu, không LLM)
  └─ Tính năng hiển thị UI (1 ô nhập + 1 nút + text area)

P2 (Mở rộng ~2h): Thêm chức năng
  ├─ Tính năng gọi LLM thật (API call)
  ├─ Tính năng lưu question bank (JSON file)
  └─ Tính năng lọc theo topic

P3 (Hoàn thiện ~1.5h): Độ chắc
  ├─ Tính năng xử lý lỗi (try/except, retry)
  ├─ Tính năng kiểm thử (unit test)
  └─ Tính năng polish UI (layout, message)
```

---

## 5. Generator: Feature Graph thay vì PHASE_BY_FILE

### 5.1 Cũ (bỏ)

`PHASE_BY_FILE` — detect phase từ filename:
```python
PHASE_BY_FILE = [
    (('model', 'storage', 'db'), 2, 'DATA MODEL'),
    (('generator', 'ai', 'llm'), 3, 'AI CORE'),
    (('main', 'ui', 'view'), 5, 'UI'),
]
```

### 5.2 Mới (áp dụng)

**Feature Graph:**
1. Parse call graph (function A gọi function B)
2. Nhóm thành **feature clusters** (chức năng hoàn chỉnh: UI → logic → data)
3. Phase 1 = chọn feature đơn giản nhất, đường đi ngắn nhất xuyên các tầng
4. Phase N+1 = feature kế tiếp, phụ thuộc phase trước

```
Call graph:  main.generate → generator.generate_questions → _build_prompt
                                                          → _call_llm
                                                          → _parse_response
                                                          → bank.save

Feature cluster 1 (MVP):  main.generate → generator.generate_questions (mock) → UI
Feature cluster 2 (Mở rộng): _call_llm thật + bank.save/load
Feature cluster 3 (Hoàn thiện): error handling + test
```

---

## 6. Tác động kỹ thuật

| Thành phần | Thay đổi |
|-----------|----------|
| `PHASE_BY_FILE` | Bỏ — thay bằng feature graph |
| `detect_phase` | Bỏ — phase từ feature clustering |
| Knowledge item | Thêm `bloom_level` |
| Phase names | `NỀN TẢNG` / `MVP` / `MỞ RỘNG` / `HOÀN THIỆN` (hoặc tùy dự án) |
| UI renderer | Không đổi (vẫn 2-column card, vertical flow) |
| `generate_jit_graph.py` | Rewrite phase detection logic |

---


---

## 6.5 Phân tích project thực: AI Quiz Generator (2026-08-07)

### 6.5.1 Call Graph (từ AST parse)

```
main.py::QuizApp (UI)
  ├─ __init__ → QuizGenerator(), QuestionBank(), setup_ui()
  ├─ setup_ui → Entry, Button, Text, pack, title
  └─ generate → get() → generate_questions() → save() → insert() (render)
                    │
quiz_generator.py::QuizGenerator (AI logic)
  ├─ generate_questions → _build_prompt() → _call_llm() → _parse_response()
  │                          │              │              │
  │                          │              └─ MOCK!      └─ loads() → Question()
  │                          └─ f-string      (trả JSON giả)
  │
question_bank.py::QuestionBank (data)
  ├─ save → asdict, dumps, write_text
  ├─ load → exists, loads, read_text
  └─ filter_by_topic → load, lower
```

### 6.5.2 Phát hiện quan trọng: `_call_llm` là MOCK

```python
def _call_llm(self, prompt: str) -> str:
    # Simplified: in production this calls the LLM API
    return json.dumps([...])  # ← trả JSON GIẢ, không gọi API thật
```

→ Sản phẩm **đã chạy được end-to-end với mock**. Đây là chìa khóa cho vertical slicing:
chia phase theo mức "thật hóa" dần (mock → API thật → độ chắc).

### 6.5.3 Feature Clusters (4 phase)

```
P0 (NỀN TẢNG ~1h) — làm quen công cụ & ngôn ngữ
  ├─ Cài đặt Python, IDE, terminal, PATH
  ├─ Cú pháp cơ bản: biến, if/else, vòng lặp, hàm
  ├─ Chạy script đầu tiên (print, input)
  └─ Git init, cấu trúc thư mục, .gitignore
  📚 Remember: biến, kiểu dữ liệu, cú pháp

P1 (MVP ~1.5h) — sản phẩm CHẠY ĐƯỢC
  ├─ Tính năng tạo question (dataclass)
  ├─ Tính năng generate (dùng _call_llm MOCK → 3 câu hỏi mẫu)
  └─ Tính năng hiển thị UI (1 ô nhập + 1 nút + text area)
  📚 Understand: JSON parse, dataclass, tkinter basics, f-string

P2 (MỞ RỘNG ~2h) — thật hóa
  ├─ Tính năng gọi LLM thật (thay mock bằng HTTP + error handling)
  ├─ Tính năng lưu question bank (JSON file: save/load)
  └─ Tính năng lọc theo topic (list comprehension)
  📚 Apply: HTTP request, Path I/O, JSON write, list comp

P3 (HOÀN THIỆN ~1.5h) — độ chắc
  ├─ Tính năng xử lý lỗi (try/except, retry, validate schema)
  ├─ Tính năng kiểm thử (unittest: round-trip, parse lỗi)
  └─ Tính năng polish UI (message, layout)
  📚 Create: error handling, schema validation, unittest
```

### 6.5.4 Bloom level dọc theo roadmap

| Concept | P0 (Nền tảng) | P1 (MVP) | P2 (Mở rộng) | P3 (Hoàn thiện) |
|---------|--------------|----------|--------------|-----------------|
| **Cú pháp** | Remember — biến, if, for | — | — | — |
| **JSON** | — | Understand — parse đơn giản | Apply — ghi file, asdict | Create — validate schema |
| **dataclass** | — | Understand — khai báo | Apply — asdict round-trip | — |
| **Error handling** | — | — | Apply — try/except cơ bản | Create — retry, validate |
| **UI (tkinter)** | — | Understand — widget cơ bản | Apply — layout đầy đủ | Create — polish, message |

### 6.5.5 So sánh cũ vs mới

| | Cũ (horizontal) | Mới (vertical 4 phase) |
|---|---|---|
| P0 | — | **Nền tảng: làm quen công cụ, ngôn ngữ, setup** |
| P1 | THIẾT LẬP (chỉ setup) | **MVP: thấy sản phẩm chạy ngay** |
| P2 | DATA MODEL (data A-Z) | **Mở rộng: LLM thật + lưu** |
| P3 | AI CORE (AI A-Z) | **Hoàn thiện: error + test** |
| P4-5 | CẤU HÌNH, UI (cuối mới thấy) | — |

## 7. Câu hỏi mở — ĐÃ QUYẾT ĐỊNH (2026-08-07)

1. **Feature clustering: HYBRID** ✅
   - Tự động detect (call graph → community detection)
   - Cho phép override bằng config file

2. **Phase names: CỐ ĐỊNH** ✅
   - Luôn `NỀN TẢNG` / `MVP` / `MỞ RỘNG` / `HOÀN THIỆN`
   - Nhất quán, dễ hiểu, không phụ thuộc LLM

3. **Bloom level: LLM ĐÁNH GIÁ** ✅
   - LLM đánh giá từng knowledge item (không heuristic theo phase)
   - Chính xác hơn, phản ánh bản chất kiến thức
   - Fallback: heuristic theo phase khi LLM unavailable

4. **MVP + UI: THEO PHÂN LOẠI DỰ ÁN** ✅
   - App có UI → MVP cần UI tối giản
   - CLI tool → MVP = chạy được command
   - Library/SDK → MVP = public API + 1 use case
   - API service → MVP = 1 endpoint + health check
   - Cần project-type detection (có main/@main/__main__? → app; Package.swift/setup.py? → library)

---

## 8. Trạng thái

- [x] Ý tưởng ghi nhận (2026-08-07)
- [x] Bổ sung phase NỀN TẢNG (P0) — làm quen công cụ & ngôn ngữ (2026-08-07)
- [x] Phân tích project thực: AI Quiz Generator call graph + feature clusters (2026-08-07)
- [x] Backup logic cũ: `backup/2026-08-07-vertical-slicing-before/` (13 files + README)
- [x] **G1**: Implement feature graph trong generator (assign_phase + propagation + mock detection + Swift parser)
- [x] **G2**: Thêm `bloom_level` vào knowledge (PHASE_BLOOM + dedup theo label+bloom)
- [x] Cập nhật phase names: NỀN TẢNG / MVP / MỞ RỘNG / HOÀN THIỆN
- [x] Test AI Quiz Generator: P0(1) P1(10) P2(4) — MVP chạy được với mock, P2 thật hóa
- [x] Quyết định câu hỏi mở (mục 7): hybrid clustering, cố định phase names, LLM bloom, theo project type
- [x] G3: Viewer phase names polish (đã xong trong G1)
- [x] G4: assemble_roadmap.py (pipeline v3) — --vertical flag opt-in
- [x] G5: project-type detection + feature clustering (hybrid) + LLM bloom evaluation
- [x] G6: Viewer hiển thị feature grouping (feature badge trên card)
- [x] G7: Test 3 project types — CLI (todo), Library (string utils), API (notes)
  - Detect đúng: cli / library / api_service
  - CLI: P1 main (entry) + P2 file I/O
  - Library/API: toàn P1 (MVP = API surface)
  - Feature clustering: library/API 6 features độc lập, CLI 1 cluster (override bằng config)

## 9. THAY ĐỔI (2026-08-07, sau khi test smart-bulb-controller) — 1 concept = 1 milestone

> ⚠️ **Sửa đổi quan trọng** — xem `2026-08-07-sio-generate-first-roadmap-content.md` §2.

**Vấn đề phát hiện:** `group_vertical_phases` tách LO theo bloom (ULO→P1, CIO→P2,
SIO→P3) khiến **cùng concept bị rải 3 phase, mỗi phase chỉ 1 tầng** — card P1 chỉ
"Concept", card P3 chỉ "Keyword". Đây vô tình tái tạo horizontal layering mà doc này
phê phán ở mục 1.

**Quyết định mới:** 1 concept = **1 milestone duy nhất** chứa đủ ULO+CIO+SIO.
Phase gán theo **bước tiến FLOW** (thứ tự concept theo dependency layer), KHÔNG theo
bloom. Cột phải card: "Concept <Tên>" (gom ULO+CIO) + "Keyword <kw>" (SIO).

Chi tiết triển khai: `assemble_roadmap.group_vertical_phases` — gom by_concept trước,
chia đều vào P1..P3 theo concept_order (flow).
