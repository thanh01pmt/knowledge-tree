---
description: Run this workflow to map the syllabus to the Master Knowledge Tree.
---

# Workflow: Map Taxonomy

> Run this workflow to map the syllabus to the Master Knowledge Tree.

**Command:** `/map-taxonomy`
**Owner:** `@taxonomy-mapper`

## Contract

1. Read the output of `/context-audit` (`projects/<project>/.work/context-audit.md`).
2. Read the master tree from `.agents/skills/taxonomy-mapper/resources/master_tree.json` (or use the TSV).
3. Cross-reference the required domains with the master tree.
4. Select the exact `fields`, `subjects`, `categories`, `topics`, and `concepts` that apply.
5. Generate a plan at `projects/<project>/.work/mapping-plan.md`.
6. STOP and ask the user to approve the `mapping-plan.md`. Do NOT proceed to write TSV files.
