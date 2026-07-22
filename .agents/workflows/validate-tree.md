---
description: Run this workflow to validate the integrity of the project's Knowledge Tree.
---

# Workflow: Validate Tree

> Run this workflow to validate the integrity of the project's Knowledge Tree.

**Command:** `/validate-tree`
**Owner:** `@tree-validator`

## Contract

1. Run `python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <project> --fix`.
2. Report the results to the user.
3. If there are ERRORs, help the user resolve them.
