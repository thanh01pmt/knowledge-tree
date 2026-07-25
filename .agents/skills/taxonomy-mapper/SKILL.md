---
name: taxonomy-mapper
description: Cross-reference extracted project syllabus with the Master Knowledge Tree to establish a formal taxonomy mapping plan.
---

# Taxonomy Mapper

> **Goal:** You are the `@taxonomy-mapper`. Take the raw syllabus topics from `/context-audit` and map them to the Master Knowledge Tree using N:N Multi-parent Topology. If `concept_candidates.tsv` exists (from `/escalate-concepts`), use those pre-computed `matched_master_code` hints as the **primary mapping signal** — do NOT re-derive what ATE has already resolved.

## Inputs

| File | Required | Role |
|------|----------|------|
| `.work/context-audit.md` | ✅ | Domain breakdown, knowledge scope |
| `output/concept_candidates.tsv` | 🔵 optional | **Pre-computed concept→Master mapping** từ ATE pipeline (`/escalate-concepts`) |

## Outputs
- `.work/mapping-plan.md`

## Process

### Step 1 — Load ATE Concept Hints (nếu có)

Kiểm tra `projects/<project>/output/concept_candidates.tsv` tồn tại không.

Nếu có, đọc và phân thành 2 nhóm:
- **Matched** (`is_new_concept=False`, `match_confidence >= 0.80`): `matched_master_code` đã biết → đưa thẳng vào plan, đánh dấu `[ATE-MATCHED]`. **Không cần search lại Master Tree.**
- **Low-confidence** (`0.70 ≤ match_confidence < 0.80`): đưa vào plan với flag `[VERIFY]` để người duyệt xác nhận.
- **Gap D** (`is_new_concept=True`): chưa có code → đề xuất `[NEW NODE PROPOSAL]`.

Mapping từ ATE **thay thế** việc phải search/suy luận từ Master Tree cho những concept đã có sẵn.
Chỉ thực hiện fresh search cho các domain trong `context-audit.md` **chưa** xuất hiện trong `concept_candidates.tsv`.

### Step 2 — Taxonomy Search (cho phần còn lại)

Với các domain trong `context-audit.md` chưa được ATE cover:
1. Đọc master tree từ `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` (hoặc `master_tree.json`)
2. Tìm `fields`, `subjects`, `categories`, `topics`, `concepts` phù hợp
3. **N:N Graph Reuse Principle:** Ưu tiên REUSE Category/Topic có sẵn thay vì tạo mới

### Step 3 — Assemble `mapping-plan.md`

Tổ chức theo cấu trúc rõ ràng:

```markdown
## ATE-Matched Concepts (from /escalate-concepts)
- CONCEPT_CODE_1  ← matched_master_code, confidence=0.92
- CONCEPT_CODE_2  ← matched_master_code, confidence=0.85

## [VERIFY] Low-Confidence Matches
- CONCEPT_CODE_3  ← matched_master_code, confidence=0.74 — cần xác nhận

## Gap D — New Node Proposals (from /escalate-concepts)
### [NEW NODE PROPOSAL] PROPOSED_CODE
- Name: ...
- Description: ...
- Parent codes: TOPIC_CODE_1, TOPIC_CODE_2

## Additional Taxonomy (from context-audit search)
<!-- Codes tìm thấy qua search Master Tree -->
```

Với code hiện có: chỉ liệt kê.
Với `[NEW NODE PROPOSAL]`: ghi đủ `UPPER_SNAKE_CASE` code (noun phrase), Name, Description, parent codes.

### Step 4 — STOP for Approval

Không ghi bất kỳ project TSV nào. Đề xuất `mapping-plan.md` cho người dùng duyệt, rồi chạy `/build-tree`.

## Rules

- `match_confidence >= 0.80` → trust & use directly (no re-derivation)
- `0.70 ≤ match_confidence < 0.80` → flag `[VERIFY]`
- Gap D concepts → always `[NEW NODE PROPOSAL]`
- *Note: `apply_plan_to_staging.py` chỉ dùng trong `/crawl-roadmap` workflow.*
