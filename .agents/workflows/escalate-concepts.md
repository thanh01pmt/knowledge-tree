---
description: Abstraction từ keywords công nghệ-cụ thể lên concepts trung tính, sau đó match với Master Tree để phát hiện Gap D candidates.
---

# Workflow: Escalate Concepts

> Chuyển `output/keywords.tsv` (tech-specific) lên `output/concept_candidates.tsv` (technology-agnostic concepts), đối chiếu với Master Tree.

**Command:** `/escalate-concepts`
**Owner:** `@keyword-extractor`

## Prerequisites

- `output/keywords.tsv` tồn tại (chạy `/finalize-keywords` trước)
- `services/python-api/general-context/mlo-knowlege-tree.tsv` có trong repo (Master Tree)
- `OPENAI_API_KEY` trong `.env` (hoặc `SAAS_OLLAMA_CLOUD_API_KEY` cho Ollama Cloud)

## Tại sao cần bước này

Keywords là **Implementational** (tầng SIO):
- `let` trong JS = khai báo biến
- `let` trong Swift = khai báo hằng số
- `const` trong JS = khai báo hằng số

Knowledge Tree cần **Concepts trung tính** (tầng Computational):
- "Khai báo biến", "Khai báo hằng số", "Kiểu tham trị", "Giao tiếp mạng"...

Bước này thực hiện abstraction + đối chiếu Master Tree để tránh tạo concept trùng.

## Contract

Chạy 1 script với 3 phase:

```bash
python3 .agents/skills/keyword-extractor/scripts/llm_escalate_concepts.py
```

### Phase 1 — LLM Abstraction
- Input: `output/keywords.tsv` (grouped by category)
- LLM: "Các khái niệm trung tính nào ẩn đằng sau các keywords này?"
- Ràng buộc: concept PHẢI pass **Marr 2-Language Test** (áp dụng được ≥ 2 công nghệ)
- Mapping N:N: nhiều keywords → 1 concept; 1 keyword → nhiều concepts
- Model: **gpt-4o** (cần reasoning tốt cho abstraction)

### Phase 2 — Master Tree Matching (embedding cosine)
- Embed proposed concepts + Master Tree concepts
- Cosine ≥ 0.80 → `matched_master_code` (conservative threshold)
- Project `output/concepts.tsv` được check trước (nếu đã build-tree)
- Master Tree embeddings được **cache** tại `.work/kw/master_embed_cache.json`

### Phase 3 — Gap Detection
- Concept không match → `is_new_concept = True` → **Gap D candidate**
- Ghi `concept_escalation.md` với 3 section: Matched / New / Ambiguous

## Expected Output

```
projects/<project>/
├── output/
│   ├── concept_candidates.tsv   ← 8 cột: concept_name, description_vi, matched_master_code, ...
│   └── concept_candidates.json  ← JSON cho downstream
└── .work/kw/
    ├── concept_escalation.md    ← ĐỌC TRƯỚC KHI /map-taxonomy
    └── master_embed_cache.json  ← cache tự động
```

### TSV Columns

| Cột | Ý nghĩa |
|-----|---------|
| `concept_name` | Tên concept trung tính (EN) |
| `description_vi` | Mô tả tiếng Việt |
| `matched_master_code` | Code trong Master Tree (trống nếu mới) |
| `matched_master_name` | Tên trong Master Tree |
| `match_confidence` | Cosine similarity score |
| `match_source` | `master` / `project` / `` |
| `is_new_concept` | `True` / `False` |
| `supporting_keywords` | Pipe-separated keywords minh họa concept |

## Human Review Point ← QUAN TRỌNG

Đọc `.work/kw/concept_escalation.md` và kiểm tra:
- [ ] Concepts có thực sự technology-agnostic không? (không chứa tên ngôn ngữ)
- [ ] Gap D concepts có thực sự missing khỏi Master Tree không?
- [ ] Match confidence có hợp lý không? (quá thấp → có thể false positive)

## After This Step

```
/map-taxonomy
```
`@taxonomy-mapper` sẽ đọc `output/concept_candidates.tsv` làm **concept hints**,
thay vì phải suy luận từ đầu từ `context-audit.md`.

## Notes

- Dùng `--match-threshold 0.75` nếu muốn match permissive hơn
- Dùng `--llm-model gpt-4o-mini` để giảm chi phí (chấp nhận abstraction kém chính xác hơn)
- Gap D concepts → có thể add vào Master Tree qua `/validate-master-tree` → PR riêng
