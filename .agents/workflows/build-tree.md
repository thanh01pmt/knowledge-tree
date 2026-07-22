---
description: Run this workflow to assemble the final project TSV files based on an approved mapping plan.
---

# Workflow: Build Tree

> Run this workflow to assemble the final project taxonomy TSV files (fields → concepts) based on an approved mapping plan. NOTE: Learning Objectives (`learning-objectives.tsv`) are generated separately via `/generate-los`, which must run AFTER this workflow.

**Command:** `/build-tree`
**Owner:** `@tree-assembler`

## Contract

1. Verify that `projects/<project>/.work/mapping-plan.md` has been explicitly approved by the user.
2. Read the master data from `.agents/skills/taxonomy-mapper/resources/master_tree.json`.
3. Filter the master data to extract ONLY the rows selected in the mapping plan.
4. Write the exact rows (with all columns like `keywords`, `cs2023_ka_mapping`, `metadata`) to 5 project TSV files: `fields.tsv`, `subjects.tsv`, `categories.tsv`, `topics.tsv`, `concepts.tsv`.
5. Ensure referential integrity (children must have parents at every level).
6. Run `/validate-tree` to confirm no BROKEN_REFERENCE or ORPHAN errors exist.
7. After this workflow completes, run `/generate-los` to generate `learning-objectives.tsv` grounded in the concepts just built.

