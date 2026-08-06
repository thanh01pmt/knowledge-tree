# JIT Knowledge Graph — Thiết kế chi tiết

> **Ngày:** 2026-08-06
> **Trạng thái:** ✅ Đã duyệt cấu trúc (bởi Human)
> **Liên kết:** [`2026-08-05-unified-roadmap-generation-architecture.md`](./2026-08-05-unified-roadmap-generation-architecture.md) · [`2026-08-06-pipeline-v3-implementation.md`](../progress/2026-08-06-pipeline-v3-implementation.md)

---

## 1. Vấn đề

Roadmap hiện tại (Pipeline v3, STEP 8.7) sinh graph theo **topological sort toàn bộ ULO → CIO → SIO** — người học phải học mọi kiến thức trước khi tới implement, kể cả kiến thức không cần cho dự án. Kết quả:

- Roadmap dài, chứa kiến thức dư thừa ("plugin system", "DI container" cho 1 app quiz đơn giản)
- Không phản ánh quá trình **xây dựng sản phẩm thực** (phase theo bước làm)
- Người mới không biết bắt đầu từ đâu, học gì tối thiểu để làm được bước tiếp theo

**Mục tiêu:** Graph theo hướng **JIT Knowledge** — mỗi implement chỉ nối với kiến thức tối thiểu cần để triển khai nó, không học dư. Cấu trúc theo **Phase = bước xây dựng sản phẩm**, 1 luồng chính Start → End duy nhất.

---

## 2. Nguyên tắc thiết kế cốt lõi

### 2.1 JIT Knowledge (Just-In-Time)

> Kiến thức trước mỗi implement chỉ **vừa đủ** để triển khai implement đó. Không tìm hiểu dư.

| Implement | Kiến thức tối thiểu | Không học dư |
|---|---|---|
| `QuestionBank` | dataclass + JSON + Path + list comp | ❌ SQL, ❌ OOP nâng cao |
| `_build_prompt` | f-string | ❌ chain-of-thought, ❌ few-shot |
| `_call_llm` | HTTP/API + error handling | ❌ streaming, ❌ function calling |
| `_parse_response` | JSON parse | ❌ schema nâng cao |
| `QuizApp` | tkinter widget + class + module | ❌ animation, ❌ custom components |

### 2.2 Phase = bước xây dựng sản phẩm

Không tách tầng (Tầng 0/1/2...) như bản cũ. Mỗi **Phase** = 1 bước xây dựng sản phẩm thực:

- Phase 1: Thiết lập dự án
- Phase 2: Data model & persistence
- Phase 3: Generative AI core
- Phase 4: Cấu hình
- Phase 5: Desktop UI
- Phase 6: Kiểm thử & chạy

### 2.3 1 luồng chính duy nhất

- **1 Start, 1 End** duy nhất cho toàn graph (không Start/End riêng mỗi phase)
- Mỗi phase có **đúng 1 luồng chính** (mũi tên dọc) đi xuyên qua
- **Nhánh cụt** (mũi tên ngang) chỉ xuất hiện khi có **nhánh thật** (kiến thức tùy chọn, alternative) — không dùng để ghi keyword
- **Keyword** ghi ngay dưới node như **chú thích làm rõ nghĩa**
- Mỗi phase kết thúc bằng **implement cụ thể**

### 2.4 Màu theo phase

Khi render, mỗi phase có 1 màu riêng để phân biệt vùng kiến thức.

---

## 3. Cấu trúc node & edge

### 3.1 Node

| Loại | Ý nghĩa | Ví dụ |
|---|---|---|
| **Knowledge node** | Kiến thức tối thiểu cần học | `<Biến & kiểu dữ liệu>`, `<JSON>`, `<tkinter>` |
| **Implement node** | Function/class thực trong repo | `[IMPLEMENT QuestionBank]`, `[IMPLEMENT _call_llm]` |
| **Test/Run node** | Kiểm thử & chạy | `[TEST QuestionBank]`, `[RUN python main.py]` |

Mỗi node có:
- `label`: tên ngắn
- `note`: keyword chú thích làm rõ nghĩa (hiển thị dưới label)
- `phase`: phase thuộc về (quyết định màu)
- `type`: knowledge | implement | test | run

### 3.2 Edge

- **1 luồng chính**: edge dọc nối các node theo thứ tự học/làm
- **Nhánh cụt**: edge ngang tới node tùy chọn (chỉ khi có nhánh thật)

---

## 4. Biểu đồ mẫu ASCII (đã duyệt)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  JIT KNOWLEDGE GRAPH — 1 luồng chính Start → End                          │
│  ██ Phase 1 ██ Phase 2 ██ Phase 3 ██ Phase 4 ██ Phase 5 ██ Phase 6       │
│  (chú thích dưới node = keyword làm rõ nghĩa)                              │
└─────────────────────────────────────────────────────────────────────────────┘

  START
    │
    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PHASE 1 — THIẾT LẬP DỰ ÁN                                             │
  └───────────────────────────────────────────────────────────────────────┘
    │
    ▼
  <Cài Python>
    (install, terminal, PATH)
    │
    ▼
  <Chạy script đầu tiên>
    (python main.py, print, input)
    │
    ▼
  <Tạo thư mục dự án>
    (main.py, config.py, question_bank.py, quiz_generator.py, requirements.txt)
    │
    ▼
  <Git init & commit>
    (git init, add, commit, .gitignore)
    │
    ▼
  [IMPLEMENT scaffold]
    (cấu trúc file + git repo sạch)
    │
    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PHASE 2 — DATA MODEL & PERSISTENCE (question_bank.py)                 │
  └───────────────────────────────────────────────────────────────────────┘
    │
    ▼
  <Biến & kiểu dữ liệu>
    (int, str, bool, list, dict)
    │
    ▼
  <List & dict>
    (truy cập, thêm, xóa phần tử)
    │
    ▼
  <Class & object>
    (thuộc tính, phương thức, self, __init__)
    │
    ▼
  <dataclass>
    (@dataclass, asdict, type hints)
    │
    ▼
  <JSON>
    (json.dumps, json.loads, indent)
    │
    ▼
  <Path & file I/O>
    (Path, read_text, write_text, exists)
    │
    ▼
  [IMPLEMENT Question]
    (model 4 trường: question, options, correct_index, explanation)
    │
    ▼
  [IMPLEMENT QuestionBank]
    (save, load, storage_path)
    │
    ▼
  <List comprehension>
    ([x for x in list if ...])
    │
    ▼
  [IMPLEMENT filter_by_topic]
    (lọc câu hỏi theo chủ đề)
    │
    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PHASE 3 — GENERATIVE AI CORE (quiz_generator.py)                      │
  └───────────────────────────────────────────────────────────────────────┘
    │
    ▼
  <Hàm>
    (def, return, tham số, default value)
    │
    ▼
  <f-string>
    (f"...{var}", format)
    │
    ▼
  <env vars>
    (os.getenv, default)
    │
    ▼
  [IMPLEMENT generate_questions]
    (orchestrate: prompt → LLM → parse)
    │
    ▼
  <LLM API call>
    (auth, token, timeout, retry)
    │
    ▼
  [IMPLEMENT _call_llm]
    (gọi model, trả response)
    │
    ▼
  <JSON parse & validate>
    (json.loads, kiểm tra cấu trúc, xử lý lỗi)
    │
    ▼
  [IMPLEMENT _parse_response]
    (response → List[Question])
    │
    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PHASE 4 — CẤU HÌNH (config.py)                                        │
  └───────────────────────────────────────────────────────────────────────┘
    │
    ▼
  <Class constants>
    (API_KEY, MODEL, DEFAULT_QUESTIONS, SUPPORTED_TOPICS)
    │
    ▼
  [IMPLEMENT Config]
    (đọc env, expose hằng số)
    │
    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PHASE 5 — DESKTOP UI (main.py)                                        │
  └───────────────────────────────────────────────────────────────────────┘
    │
    ▼
  <tkinter basics>
    (Tk, Entry, Button, Text, pack, mainloop)
    │
    ▼
  [IMPLEMENT QuizApp.__init__]
    (khởi tạo generator + bank + UI)
    │
    ▼
  [IMPLEMENT QuizApp.setup_ui]
    (window, input, button, result area)
    │
    ▼
  <Event handler>
    (button command, callback)
    │
    ▼
  [IMPLEMENT QuizApp.generate]
    (đọc topic → sinh câu hỏi → lưu → render)
    │
    ▼
  <if __name__ == "__main__">
    (entry point)
    │
    ▼
  [IMPLEMENT main entry]
    (Tk() + mainloop())
    │
    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PHASE 6 — KIỂM THỬ & CHẠY                                             │
  └───────────────────────────────────────────────────────────────────────┘
    │
    ▼
  <unittest/pytest basics>
    (TestCase, assertEqual, setUp)
    │
    ▼
  <Mock LLM>
    (giả lập API response)
    │
    ▼
  [TEST QuestionBank round-trip]
    (save → load → so sánh)
    │
    ▼
  [TEST _parse_response]
    (JSON hợp lệ + JSON lỗi)
    │
    ▼
  [RUN python main.py]
    (nhập topic → sinh câu hỏi → lưu questions.json)
    │
    ▼
  END
```

### Dạng chuỗi ngắn (1 luồng duy nhất)

```
START
→ [P1] <Cài Python> → <Chạy script> → <Tạo thư mục> → <Git> → [scaffold]
→ [P2] <Biến & kiểu> → <List/dict> → <Class> → <dataclass> → <JSON> → <Path> → [Question] → [QuestionBank] → <list comp> → [filter_by_topic]
→ [P3] <Hàm> → <f-string> → <env vars> → [generate_questions] → <LLM API> → [_call_llm] → <JSON parse> → [_parse_response]
→ [P4] <Class constants> → [Config]
→ [P5] <tkinter> → [__init__] → [setup_ui] → <event> → [generate] → <__main__> → [entry]
→ [P6] <unittest> → <mock> → [TEST QuestionBank] → [TEST parse] → [RUN]
→ END
```

---

## 5. Cách map kiến thức → implement (phần lõi)

```
Với mỗi function/class trong repo (AST parse):
  1. Detect constructs dùng bên trong (json.dumps, os.getenv, tk.Entry, f-string...)
  2. Map constructs → kiến thức tối thiểu (từ Master Tree concepts)
  3. Tạo edge: <kiến thức> → [implement]
```

Ví dụ `_call_llm`:
```
AST detect: json.dumps, os.getenv, str.split, self.model
    │
    ▼
Map: <env vars> + <JSON> + <string methods> → [IMPLEMENT _call_llm]
```

### Nguồn kiến thức tối thiểu

- **Option A (đã chọn):** Map từ Master Tree concepts — tái dùng, không tốn LLM, nhất quán
- Option B: LLM sinh kiến thức theo từng implement — tự nhiên hơn, tốn LLM

### Tầng nền tảng ngôn ngữ

- **Option A (đã chọn):** Bộ kiến thức nền thủ công per-language (biến, hàm, class...) — deterministic, không phụ thuộc LLM
- Option B: LLM sinh từ code

---

## 6. Output format (dạng roadmap.sh)

```json
{
  "nodes": [
    {
      "id": "k1",
      "type": "topic",
      "data": {
        "label": "Biến & kiểu dữ liệu",
        "note": "int, str, bool, list, dict",
        "phase": 2,
        "nodeType": "knowledge"
      },
      "position": {"x": 0, "y": 0}
    },
    {
      "id": "i1",
      "type": "subtopic",
      "data": {
        "label": "IMPLEMENT QuestionBank",
        "note": "save, load, storage_path",
        "phase": 2,
        "nodeType": "implement"
      },
      "position": {"x": 300, "y": 200}
    }
  ],
  "edges": [
    {"source": "k1", "target": "i1", "data": {"edgeStyle": "solid"}}
  ]
}
```

- `phase` quyết định **màu** khi render
- `nodeType` phân biệt knowledge / implement / test / run
- Render bằng `RoadmapShRendererV2.jsx` (đã có trong `apps/viewer/`)

---

## 7. Các quyết định thiết kế (đã chốt)

| # | Quyết định | Lựa chọn | Lý do |
|---|---|---|---|
| 1 | Nguồn kiến thức tối thiểu | **Master Tree concepts** | Tái dùng, không tốn LLM, nhất quán |
| 2 | Tầng nền tảng ngôn ngữ | **Thủ công per-language** | Deterministic, không phụ thuộc LLM |
| 3 | Implement node | **Mỗi function/class = 1 node** | Đúng JIT, chi tiết |
| 4 | Render | **JSON → viewer** | Tận dụng renderer có sẵn |
| 5 | Kiến thức dư | **Chỉ giữ kiến thức có edge tới implement** | Đúng triết lý JIT |
| 6 | Cấu trúc phase | **Phase = bước xây dựng sản phẩm** | Phản ánh quá trình làm thật |
| 7 | Luồng | **1 Start → 1 End duy nhất** | Dễ theo dõi, không rối |
| 8 | Keyword | **Chú thích dưới node** | Làm rõ nghĩa, không tạo nhánh giả |
| 9 | Nhánh cụt | **Chỉ khi có nhánh thật** | Không dùng để ghi keyword |
| 10 | Màu | **Mỗi phase 1 màu** | Phân biệt vùng kiến thức |
| 11 | Kết thúc phase | **Bằng implement cụ thể** | Deliverable rõ ràng |

---

## 8. Script đề xuất: `generate_jit_graph.py`

### Input / Output

```
Input:  repo_dir (code thực) + reuse_inventory (Master Tree concepts)
Output: jit_graph.json (dạng frontend.json: nodes + edges + position)
        → render bằng RoadmapShRendererV2.jsx
```

### Pipeline

```
1. Parse repo → mỗi function/class = 1 implement node
2. Phân tích AST → detect constructs dùng trong mỗi function
3. Map constructs → kiến thức tối thiểu (từ Master Tree concepts)
4. Group implement theo phase (file/module → phase)
5. Sinh chuỗi kiến thức → implement trong mỗi phase
6. Xuất jit_graph.json (nodes có phase/color, edges 1 luồng chính)
```

### Phase mapping (mặc định per-language)

| Phase | Nội dung | File thường chứa |
|---|---|---|
| 1 | Thiết lập dự án | scaffold, git, env |
| 2 | Data model & persistence | models, storage, db |
| 3 | Core logic (AI/domain) | generator, service |
| 4 | Cấu hình | config, settings |
| 5 | UI | main, app, views |
| 6 | Kiểm thử & chạy | tests, run |

---

## 9. Khác biệt so với Pipeline v3 hiện tại

| Tiêu chí | Pipeline v3 (STEP 8.7) | JIT Knowledge Graph |
|---|---|---|
| **Cấu trúc** | Topo sort toàn bộ ULO→CIO→SIO | Phase theo bước xây dựng sản phẩm |
| **Kiến thức** | Học mọi thứ trước khi implement | Chỉ học tối thiểu cho từng implement |
| **Luồng** | Nhiều nhánh | 1 luồng chính Start→End |
| **Phase** | Layer nhận thức (ULO/CIO/SIO) | Bước xây dựng (setup, model, AI, UI...) |
| **Keyword** | Trong description | Chú thích dưới node |
| **Màu** | Không | Mỗi phase 1 màu |
| **Mục đích** | Curriculum coverage | Hướng dẫn làm sản phẩm thực |

---

## 10. Next steps

1. ✅ Ghi thiết kế này vào `docs/ideas/` (file hiện tại)
2. Tạo `generate_jit_graph.py` theo đúng cấu trúc đã duyệt
3. Test với AI Quiz Generator repo
4. Render trong viewer (RoadmapShRendererV2)
5. (Tùy chọn) Tích hợp vào Pipeline v3 như STEP 8.8
