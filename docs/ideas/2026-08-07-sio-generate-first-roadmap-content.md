# SIO GENERATE-First & Roadmap Content Design — Quyết định thiết kế

> **Ngày:** 2026-08-07
> **Phạm vi:** Pipeline roadmap (pipeline v3), TopicRoadmapRenderer, resolve_sios, generate_jit_los
> **Bối cảnh:** Test trên smart-bulb-controller (Swift/ESP32) phát hiện hàng loạt lỗi content sai lệch dự án.

---

## 1. ADR: SIO GENERATE-First — bỏ REUSE/ADAPT cross-project

### Vấn đề
Master Tree SIOs sinh từ project khác (`stream-chat-swift`, `swift-associate`, ...) — là
"generic Swift SIOs" **không gắn với dự án đích**. Ví dụ thực tế:

- Dự án `smart-bulb-controller` dùng `for (int i...)` (C-style) + `while WiFi.status()`
- SIO REUSE lấy từ `swift-associate`: *"Use forEach vs for-in for Side Effects"*
- **`forEach` không tồn tại trong code dự án bulb** → SIO sai, gây hiểu nhầm người học

`resolve_sios.filter_sios_by_domain` chỉ **annotate** `domain_score` (min_score=0 giữ hết),
**không loại** SIO không liên quan, và chỉ dùng `goal_tokens` — không đối chiếu
`keywords.json` / AST thật của dự án.

### Quyết định
**Bỏ hẳn hướng REUSE/ADAPT cross-project.** Mọi SIO đi qua GENERATE (JIT sinh mới):

```
resolve_sios_for_cio() → luôn trả {action: 'GENERATE'}
  ↓
generate_jit_los.generate_sio() — sinh SIO gắn keyword THẬT của dự án
  ↓
Sau đó mới đánh giá loại bỏ / cập nhật
```

- Không tìm sibling SIO, không group by tech, không similarity ADAPT
- `generate_sio` nhận `keyword` từ `collect_resolved_concepts` (keyword nguồn thật:
  import/property_wrapper/error_handling — **bỏ function_signature/type_declaration**
  vì là tên do dev đặt, không phải keyword ngôn ngữ)

### Hệ quả
- Roadmap chỉ có SIO gắn keyword thực tế xuất hiện trong code dự án
- Chi phí LLM tăng (mỗi concept sinh SIO mới) nhưng đảm bảo đúng content
- `JIT_SOURCES` / `KEYWORD_SOURCES` = `{import, property_wrapper, error_handling, docstring, readme, config, escalated}`

---

## 2. 1 Concept = 1 Milestone duy nhất (sửa vertical slicing)

### Vấn đề
`group_vertical_phases` tách LO theo bloom: ULO→P1, CIO→P2, SIO→P3 → **cùng concept
bị rải 3 phase, mỗi phase chỉ 1 tầng**. Card P1 chỉ "Concept" (ULO), card P3 chỉ
"Keyword" (SIO) — thiếu bên này/bên kia. Đây là horizontal layering mà chính
`2026-08-07-vertical-slicing-roadmap.md` phê phán.

### Quyết định
**1 concept = 1 milestone duy nhất chứa ĐỦ ULO + CIO + SIO.** Phase gán theo
bước tiến FLOW (thứ tự concept trong layer), không theo bloom:

```
group_vertical_phases():
  by_concept[concept] = [mọi LO của concept, xuyên phase]
  concept_order = thứ tự concept theo layer (dependency flow)
  chia đều concepts vào P1..P3 theo thứ tự flow
```

Ví dụ bulb: P1 (MVP) = Core Libraries, Exception Handling, Definite Iteration;
P2 (MỞ RỘNG) = Http Protocol, Local View State, Web Auth; P3 (HOÀN THIỆN) = Web Server.

---

## 3. Cột phải: "Concept X" + "Keyword Y" (không tách ULO/CIO/SIO riêng)

### Nguyên tắc (ý định người dùng)
> "Để làm implement đó, user cần hiểu **concept** gì, có khả năng vận dụng
> **keyword** gì để triển khai thực tế."

### Hiển thị
| Tầng | Cột phải | Hover |
|---|---|---|
| ULO + CIO (cùng concept) | **1 item "Concept <Tên>"** — gom, không tách | Hiện đủ ULO + CIO (mỗi cái kèm bloom + desc) |
| SIO | **1 item "Keyword <kw>"** | Hiện SIO (name + desc + bloom) |

- Bloom tag đa cấp cho concept: `understand · apply` (gom các bloom khác nhau)
- Dùng **tên tự nhiên** (humanizeCode: `LOCAL_VIEW_STATE` → "Local View State"),
  không hiển thị mã code
- Dedup keyword trùng (VD 3× "for-in" → 1)

---

## 4. Khái niệm chuẩn: Definite Iteration (không phải "For Loop" hay "Loop")

### Quyết định
- **ULO** gắn khái niệm **"Definite Iteration"** (lặp với số lần xác định) — chuẩn
  sư phạm hơn "Loop"; phân biệt với Indefinite Iteration (while, số lần không xác định)
- **SIO** dùng tên thực hành: **"For Loop"** + keyword **`for`** (từ khóa ngôn ngữ thật)
  — KHÔNG dùng tên khái niệm trừu tượng làm tên implement

### Trước → Sau (FOR_LOOP)
```
Trước: ULO "hiểu vòng lặp for" | SIO "Implement Definite Iteration" | kw="definite iteration"
Sau:   ULO "hiểu Definite Iteration" | SIO "Implement For Loop" | kw="for"
```

### Keyword generic bị loại
`loop` (tên hàm Arduino `loop()`) là function_signature — không phải keyword ngôn ngữ.
`_GENERIC_SIO_KEYWORDS = {loop, state, server, http, api, app, data, error, handler,
service, model, view, config, file, function}` → thay bằng keyword thật trích từ
SIO name (`for`, `@State`, `forEach`...).

---

## 5. Lọc Template CIOs 12-Verb (Master Tree data thối)

Master Tree có **2160 CIOs sinh từ đúng 12-verb pattern máy móc** (mỗi verb áp 70-270
concepts): `EXPLAIN_MECHANISM ×270, INTERPRET_PARAMETERS ×270, DECOMPOSE_TRADEOFFS ×268,
COMPARE_ALTERNATIVES ×268, IDENTIFY_COMPONENTS ×200, RECALL_DEFINITIONS ×200,
IMPLEMENT_PATTERN ×200, ADAPT_TO_CONTEXT ×200, ASSESS_QUALITY ×72, CRITIQUE_DESIGN ×72,
DESIGN_SOLUTION ×70, INNOVATE_EXTENSION ×70`.

Mô tả generic ("phân rã X thành yếu tố quyết định và định lượng đánh đổi", "đánh giá
theo tiêu chuẩn ngành, benchmark") — không nói gì đặc thù concept.

### Fix
`is_template_cio_code()` — filter CIO code kết thúc `-NN-VERB` (12 verb) khỏi roadmap.
Phân tích trước đó bỏ sót vì dùng chính bộ signals thiếu pattern (circular check).

---

## 6. Bài học quy trình (phòng lỗi tái diễn)

1. **Kiểm bằng con mắt phê bình, không bằng chính bộ lọc mình viết** — scan bằng
   `_TEMPLATE_DESC_SIGNALS` thiếu pattern → báo "0 issues" giả
2. **Mọi content phải gắn keyword thực hành dự án** — không lý thuyết trừu tượng;
   verify SIO keyword tồn tại trong code thật (grep AST / keywords.json)
3. **Nhìn data gốc, không vá renderer** — lỗi cấu trúc sửa ở pipeline (assemble),
   không che ở UI
