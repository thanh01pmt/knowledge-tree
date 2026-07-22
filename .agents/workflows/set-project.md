---
description: Run this workflow to update the active project.
---

# Workflow: Set Project

> Run this workflow to update the active project.

**Command:** `/set-project <project>`
**Owner:** `coordinator`

## Contract

1. Verify that `projects/<project>` exists.
2. Update `status.yaml` to set `active_project: <project>`.
3. Report success.
