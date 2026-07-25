---
description: Run this workflow to map the syllabus to the Master Knowledge Tree.
---

# Workflow: Map Taxonomy

> Map syllabus domains to the Master Knowledge Tree. Nếu `/escalate-concepts` đã chạy, taxonomy mapper sẽ dùng `concept_candidates.tsv` làm mapping hints — không cần search lại Master Tree cho phần đã biết.

**Command:** `/map-taxonomy`
**Owner:** `@taxonomy-mapper`

## Contract

1. Đọc `projects/<project>/.work/context-audit.md` (required).
2. **ATE Hints Check**: Kiểm tra `projects/<project>/output/concept_candidates.tsv`:
   - Nếu tồn tại → đọc, phân loại Matched / Low-confidence / Gap D
   - Matched (`confidence ≥ 0.80`) → dùng `matched_master_code` trực tiếp, đánh dấu `[ATE-MATCHED]`
   - Low-confidence (`0.70–0.80`) → đưa vào plan với flag `[VERIFY]`
   - Gap D → đề xuất `[NEW NODE PROPOSAL]`
3. Với phần còn lại (chưa được ATE cover): search Master Tree từ `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv`
4. Áp dụng **N:N Graph Reuse Principle**: ưu tiên reuse Category/Topic có sẵn.
5. Tạo `projects/<project>/.work/mapping-plan.md` theo cấu trúc:
   - `## ATE-Matched Concepts`
   - `## [VERIFY] Low-Confidence Matches`
   - `## Gap D — New Node Proposals`
   - `## Additional Taxonomy (from context-audit search)`
6. **STOP**: Không ghi TSV. Đề xuất `mapping-plan.md` cho người dùng duyệt.

## After Approval

```bash
# /build-tree sẽ đọc mapping-plan.md và ghi 5 TSV files
```
