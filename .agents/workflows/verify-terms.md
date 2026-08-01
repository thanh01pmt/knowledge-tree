---
description: Dedup biến thể + vòng lặp omission-check (tối đa 2 vòng) → verify-report.md — điểm duyệt người trước khi finalize.
---

# Workflow: Verify Terms

> LLM dedup biến thể và kiểm tra bỏ sót. Tạo `verify-report.md` để người duyệt trước khi export.

**Command:** `/verify-terms`
**Owner:** `@keyword-extractor`

## Prerequisites

- `.work/kw/candidates_filtered.json` tồn tại (chạy `/extract-terms` trước)
- `.work/kw/chunks.json` tồn tại
- `OPENAI_API_KEY` trong `.env` (hoặc `SAAS_OLLAMA_CLOUD_API_KEY` cho Ollama Cloud)

## Contract

Chạy 1 script với 2 phase:

```bash
python3 .agents/skills/keyword-extractor/scripts/llm_verify_and_dedup.py
```

### Phase A — Dedup & Canonicalize
- LLM nhóm biến thể thành canonical form + aliases
- VD: `"ESP32-S3"` / `"ESP32 S3"` / `"esp32s3"` → canonical: `"ESP32-S3"`, aliases: `["ESP32 S3", "esp32s3"]`
- **Không gộp thuật ngữ khác nghĩa** (I2C ≠ SPI dù embedding gần)

### Phase B — Omission Check Loop (≤ 2 vòng)
- Per-chunk: model thấy **toàn bộ danh sách hiện có + chunk gốc** trong cùng 1 lượt gọi
- Hỏi: "có thuật ngữ liên quan chưa có trong danh sách không?"
- Dừng sớm nếu vòng nào Δ = 0
- Term mới → `first_extraction_method = "omission_check"`

## Expected Output

```
.work/kw/
├── keywords_verified.json
└── verify-report.md   ← ĐỌC TRƯỚC KHI CHẠY /finalize-keywords
```

## Human Review Point ← QUAN TRỌNG

Đọc `verify-report.md` và kiểm tra:
- [ ] Số term thêm từ omission-check có hợp lý không?
- [ ] Danh sách canonical có phủ đủ 3 lớp HW/SW/Protocol chưa?
- [ ] Có canonical nào bị gộp nhầm không?

Nếu OK → chạy `/finalize-keywords`.
