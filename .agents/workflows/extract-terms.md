---
description: Chạy pipeline trích xuất candidate — YAKE statistical + LLM candidate-gen → embedding filter, ra candidates_filtered.md để xem trước.
---

# Workflow: Extract Terms

> Chạy 3 scripts để sinh và lọc candidate terms từ các chunks đã tạo ở `/scaffold-keywords`.

**Command:** `/extract-terms`
**Owner:** `@keyword-extractor`

## Prerequisites

- `.work/kw/chunks.json` tồn tại (chạy `/scaffold-keywords` trước)
- `OPENAI_API_KEY` trong `.env`
- Dependencies: `pip install yake openai pydantic`

## Contract

Chạy tuần tự 3 scripts:

### Step 1 — Statistical Candidates (YAKE)
```bash
python3 .agents/skills/keyword-extractor/scripts/gen_statistical_candidates.py
```
Output: `.work/kw/candidates_statistical.json`

### Step 2 — LLM Candidates
```bash
python3 .agents/skills/keyword-extractor/scripts/llm_gen_candidates.py
```
Output: `.work/kw/candidates_llm.json`
- Gọi 1 lượt/chunk với prompt "liệt kê MỌI thuật ngữ, đừng tự curate"
- Chi phí: ~$0.001–0.005 / 10 chunks với gpt-4o-mini

### Step 3 — Filter by Relevance
```bash
python3 .agents/skills/keyword-extractor/scripts/filter_by_relevance.py
```
Output: `.work/kw/candidates_filtered.json` + `.work/kw/candidates_filtered.md`
- Union 2 candidate lists, embed cosine similarity với target-context
- Ngưỡng lỏng (default 0.25) — ưu tiên recall

## Expected Output

```
.work/kw/
├── candidates_statistical.json
├── candidates_llm.json
├── candidates_filtered.json
└── candidates_filtered.md   ← xem trước kết quả
```

## After This Step

Xem `candidates_filtered.md`. Nếu coverage đủ, chạy `/verify-terms`.
