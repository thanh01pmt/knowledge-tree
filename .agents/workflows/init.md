---
description: Run this workflow to scaffold a new project directory structure and output TSV headers.
---

# Workflow: Init Project

> Run this workflow to scaffold a new project directory structure and output TSV headers.

**Command:** `/init <project>`
**Owner:** `scaffolder`

## Contract

1. Run `python3 .agents/skills/tree-validator/scripts/scaffold_tree.py <project>`.
2. Create `projects/<project>/` directory structure: `context/`, `.work/`, `output/`.
3. Scaffold 6 empty TSV files with correct headers inside `projects/<project>/output/`.
4. Update `active_project: <project>` in `status.yaml`.
5. Report success to the user.
