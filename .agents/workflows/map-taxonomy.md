---
description: Run this workflow to map the syllabus to the Master Knowledge Tree.
---

# Workflow: Map Taxonomy

> Map syllabus domains to the Master Knowledge Tree. Pipeline tự động extract cấu trúc tài liệu nguồn và semantic search Master Tree trước khi agent mapping thủ công.

**Command:** `/map-taxonomy`
**Owner:** `@taxonomy-mapper`

## Prerequisites

- `/context-audit` đã chạy → `.work/context-audit.md` tồn tại
- (Optional) `/escalate-concepts` đã chạy → `output/concept_candidates.tsv` có thể có

## Step 0 — Document Hierarchy Extraction (tự động)

Chạy script extract cấu trúc phân cấp từ tài liệu nguồn (PDF/MD/TXT/DOCX), không phụ thuộc loại tài liệu:

```bash
python3 .agents/skills/taxonomy-mapper/scripts/extract_document_hierarchy.py --project <slug>
```

Output: `.work/structured_hints.json` — cây phân cấp với mỗi node đã được LLM phân loại tầng Master Tree (Field/Subject/Category/Topic/Concept).

**Cơ chế:**
1. Detect source type (PDF/MD/TXT/DOCX)
2. Extract heading tree từ document structure (H1→H2→H3→paragraph)
3. LLM classify mỗi node vào tầng Master Tree phù hợp — dựa trên NỘI DUNG, không dựa trên heading level
4. Ghi `structured_hints.json` làm primary signal cho agent mapping

## Step 1 — Load ATE Concept Hints (nếu có)

Kiểm tra `projects/<project>/output/concept_candidates.tsv` tồn tại không.

Nếu có, đọc và phân thành 2 nhóm:
- **Matched** (`is_new_concept=False`, `match_confidence >= 0.80`): dùng `matched_master_code` trực tiếp, đánh dấu `[ATE-MATCHED]`
- **Low-confidence** (`0.70 ≤ match_confidence < 0.80`): đưa vào plan với flag `[VERIFY]`
- **Gap D** (`is_new_concept=True`): đề xuất `[NEW NODE PROPOSAL]`

## Step 2 — Semantic Search Master Tree

Với mỗi domain/item chưa được ATE cover, dùng semantic search để tìm top-5 concept/topic/category gần nhất:

```bash
python3 .agents/skills/taxonomy-mapper/scripts/semantic_search_master.py \
  --query "Use for-in loops to iterate over arrays" \
  --top-k 5
```

Dùng `master_tree_embeddings.json` (đã có sẵn) để tính cosine similarity. Kết quả có evidence-based scores, loại bỏ guess work.

## Step 3 — Assemble `mapping-plan.md`

Tổ chức theo cấu trúc rõ ràng, ưu tiên:
1. **ATE-Matched Concepts** (từ concept_candidates.tsv)
2. **Structured Hints** (từ structured_hints.json — hierarchy từ tài liệu gốc)
3. **Semantic Search Results** (từ semantic_search_master.py)
4. **Additional Taxonomy** (search Master Tree thủ công cho phần còn lại)

```markdown
## ATE-Matched Concepts (from /escalate-concepts)
- CONCEPT_CODE_1  ← matched_master_code, confidence=0.92

## Structured Hints (from document hierarchy)
### Category: CATEGORY_NAME
- Topic: TOPIC_NAME → Concept: CONCEPT_CODE_1, CONCEPT_CODE_2

## [VERIFY] Low-Confidence Matches
- CONCEPT_CODE_3  ← confidence=0.74 — cần xác nhận

## Gap D — New Node Proposals
### [NEW NODE PROPOSAL] PROPOSED_CODE
- Name: ...
- Parent codes: TOPIC_CODE_1, TOPIC_CODE_2

## Additional Taxonomy (from context-audit search)
```

## Step 4 — STOP for Approval

Không ghi bất kỳ project TSV nào. Đề xuất `mapping-plan.md` cho người dùng duyệt, rồi chạy `/build-tree`.

## After Approval

```bash
# /build-tree sẽ đọc mapping-plan.md và ghi 5 TSV files
```
