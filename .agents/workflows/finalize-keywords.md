---
description: Sau khi duyệt verify-report.md, ghi output/keywords.tsv và inject vào context-audit để /context-audit dùng.
---

# Workflow: Finalize Keywords

> Export keywords cuối cùng và tích hợp vào `/context-audit` pipeline.

**Command:** `/finalize-keywords`
**Owner:** `@keyword-extractor`

## Prerequisites

- `.work/kw/keywords_verified.json` tồn tại (chạy `/verify-terms` trước)
- Đã đọc và duyệt `verify-report.md`

## Contract

Chạy export script:

```bash
python3 .agents/skills/keyword-extractor/scripts/export_keywords.py
```

### Script làm gì:

1. **Ghi `output/keywords.tsv`** — 6 cột:
   `term | aliases | relevance_score | source_chunks | first_extraction_method | category`

2. **Ghi `output/keywords.json`** — format đầy đủ cho downstream use

3. **Copy sang `context/keywords.tsv`** — để `@context-analyzer` dùng khi chạy `/context-audit`

4. **Inject section `## ATE Keywords`** vào `.work/context-audit.md` (nếu đã tồn tại):
   - Thêm bảng top-80 terms theo relevance_score
   - Ghi metadata: target_context, timestamp, số terms

## Integration với `/context-audit`

Sau bước này, khi `@context-analyzer` chạy `/context-audit`:
- Tự động đọc `context/keywords.tsv` nếu tồn tại
- Tích hợp danh sách ATE terms vào domain breakdown
- Không cần extract lại từ PDF — đã có từ ATE pipeline

## Expected Output

```
projects/<project>/
├── output/
│   ├── keywords.tsv      ← output cuối, 6 cột
│   └── keywords.json     ← JSON cho downstream
├── context/
│   └── keywords.tsv      ← copy cho @context-analyzer
└── .work/
    └── context-audit.md  ← đã có section ## ATE Keywords (nếu tồn tại)
```

## After This Step

```
→ /escalate-concepts  (recommended)
   Abstraction keywords → concept trung tính + match Master Tree
   → Sinh concept_candidates.tsv + phát hiện Gap D
   → Làm hints cho /map-taxonomy

→ /context-audit   (nếu bỏ qua /escalate-concepts)
   @context-analyzer đọc keywords.tsv và tích hợp vào domain breakdown
```
