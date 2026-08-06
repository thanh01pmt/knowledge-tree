# Gap D Proposal — AI Generative Application Concepts

> **Ngày:** 2026-08-06
> **Nguồn phát hiện:** Pipeline v3 test với use case "AI Quiz Generator" (Python + OpenAI)
> **Vấn đề:** Master Tree có topic `GENERATIVE_AI_MODELS` + concepts lý thuyết (Transformer, LLM Principles, RAG) nhưng **thiếu concepts ứng dụng LLM thực tế** — khiến keywords như "Generative AI logic", "Generate questions using LLM" chỉ match `IF_ELSE_STATEMENT` (0.50) / `SQL_SELECT` (0.49).

---

## 1. Concepts đề xuất (5 concepts mới)

### HIGH priority — cần thiết cho mọi dự án LLM application

| # | Code | Name (EN) | Description | Topic Codes | Keywords | CS2023 |
|---|------|-----------|-------------|-------------|----------|--------|
| 1 | `PROMPT_ENGINEERING` | Prompt Engineering | Thiết kế prompt hiệu quả cho LLM: system prompt, few-shot examples, chain-of-thought, temperature/top-p tuning, prompt templates và đánh giá chất lượng prompt. | `GENERATIVE_AI_MODELS` | prompt engineering, system prompt, few-shot, chain-of-thought, temperature, prompt template | AI |
| 2 | `LLM_API_INTEGRATION` | LLM API Integration | Tích hợp LLM qua API: authentication, request/response lifecycle, token limits, rate limiting, retry/backoff, streaming responses và error handling. | `GENERATIVE_AI_MODELS` | LLM API, OpenAI, token limit, rate limit, streaming, retry, API integration | AI, SE |
| 3 | `STRUCTURED_OUTPUT_PARSING` | Structured Output Parsing | Ép LLM trả về output có cấu trúc (JSON, schema validation): response format, JSON mode, function calling, validation và retry khi parse lỗi. | `GENERATIVE_AI_MODELS` | structured output, JSON mode, function calling, schema validation, response parsing | AI, SDF |

### MEDIUM priority — cần cho app desktop + persistence

| # | Code | Name (EN) | Description | Topic Codes | Keywords | CS2023 |
|---|------|-----------|-------------|-------------|----------|--------|
| 4 | `GENERATIVE_CONTENT_APPLICATION` | Generative Content Application | Xây dựng ứng dụng sinh nội dung: content generation pipeline, user input → prompt → LLM → validated output, domain-specific generation (quiz, summary, translation). | `GENERATIVE_AI_MODELS` | content generation, quiz generation, generation pipeline, LLM application | AI, HCI |
| 5 | `LOCAL_JSON_PERSISTENCE` | Local JSON Persistence | Lưu trữ và truy xuất dữ liệu cục bộ dạng JSON: dataclass serialization, file I/O, query/filter theo điều kiện, atomic write và backup. | `DATA_MGMT` | JSON persistence, dataclass, serialization, file storage, local database | DM, SDF |

---

## 2. Lý do cần thêm

### 2.1 Gap thực tế (từ test pipeline)

| Keyword từ repo | Best match hiện tại | Score | Đúng domain? |
|---|---|---|---|
| "Generative AI logic for creating quiz questions" | `IF_ELSE_STATEMENT` | 0.50 | ❌ |
| "Generate multiple-choice questions for a topic using LLM" | `SQL_SELECT` | 0.49 | ❌ |
| "AI Quiz Generator" | `TYPES_OF_AI` | 0.53 | ❌ |
| "Desktop app that generates multiple-choice quiz questions" | `AUTOMATED_TESTING_TOOLS` | 0.47 | ❌ |

→ Không concept nào match đúng → 29 concepts rời rạc bị propose (noise).

### 2.2 Sau khi thêm 5 concepts, kỳ vọng

| Keyword | Concept match mới | Kỳ vọng score |
|---|---|---|
| "Generative AI logic for creating quiz questions" | `GENERATIVE_CONTENT_APPLICATION` | ≥ 0.55 |
| "Generate multiple-choice questions for a topic using LLM" | `PROMPT_ENGINEERING` / `LLM_API_INTEGRATION` | ≥ 0.55 |
| `_call_llm` | `LLM_API_INTEGRATION` | ≥ 0.55 |
| `_build_prompt` | `PROMPT_ENGINEERING` | ≥ 0.55 |
| `_parse_response` | `STRUCTURED_OUTPUT_PARSING` | ≥ 0.55 |
| `save` / `load` / `QuestionBank` | `LOCAL_JSON_PERSISTENCE` | ≥ 0.55 |

---

## 3. Cách merge (theo AGENTS.md §1, §5)

1. **Bạn duyệt proposal này** (approve/reject/modify từng concept)
2. Tôi thêm vào **staging** `services/python-api/general-context/mlo-knowlege-tree.tsv` (working copy)
3. Chạy `validate_master_tree.py` → xác nhận không DUPLICATE_CODE / BROKEN_REFERENCE
4. Chạy lại pipeline AI Quiz Generator → verify roadmap match đúng domain
5. (Tùy chọn) `sync_back_master.py` → promote vào official Master Tree

---

## 4. Rủi ro & lưu ý

- **Trùng lặp:** Đã kiểm tra — `PROMPT_ENGINEERING`, `LLM_API_INTEGRATION`, `STRUCTURED_OUTPUT_PARSING`, `GENERATIVE_CONTENT_APPLICATION`, `LOCAL_JSON_PERSISTENCE` **không tồn tại** trong Master Tree hiện tại
- **T6 neutrality:** Tất cả concepts trên đều tech-agnostic (không nhắc OpenAI cụ thể trong description chính thức — "LLM API" là khái niệm chung)
- **Topic parent:** `GENERATIVE_AI_MODELS` đã tồn tại (line 252), `DATA_MGMT` đã tồn tại — không cần tạo topic mới
