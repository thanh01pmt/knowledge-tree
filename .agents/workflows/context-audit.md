---
description: Run this workflow to establish the project context from source files (PDFs, syllabi, etc.).
---

# Workflow: Context Audit

> Run this workflow to establish the project context from source files (PDFs, syllabi, etc.).

**Command:** `/context-audit`
**Owner:** `@context-analyzer`

## Contract

1. Read all files in `projects/<project>/context/`.
2. Extract the syllabus and high-level knowledge domains that need to be covered.
3. Save the findings to `projects/<project>/.work/context-audit.md`.

Do NOT attempt to map to the Master Tree yet. Just understand what is required.
