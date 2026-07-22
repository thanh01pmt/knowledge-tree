---
description: Run this workflow to assemble the final project TSV files based on an approved mapping plan.
---

# Workflow: Build Tree

> Run this workflow to assemble the final project TSV files based on an approved mapping plan.

**Command:** `/build-tree`
**Owner:** `@tree-assembler`

## Contract

1. Verify that `projects/<project>/.work/mapping-plan.md` has been explicitly approved by the user.
2. Read the master data from `.agents/skills/taxonomy-mapper/resources/master_tree.json`.
3. Filter the master data to extract ONLY the rows selected in the mapping plan.
4. Write the exact rows (with all columns like metadata, cs2023_ka_mapping) to the project's 6 TSV files.
5. Ensure referential integrity (children must have parents).
