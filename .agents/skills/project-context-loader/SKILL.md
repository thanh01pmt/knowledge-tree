---
name: project-context-loader
description: Inventory, read, interpret, and summarize every resource in the active project's context directory to establish the exact domains and syllabus.
---

# Project Context Loader

> **Goal:** You are the `@context-analyzer`. Read all source materials provided by the teacher (e.g. syllabus PDF, exam guide) in `projects/<project>/context/`, extract the core topics and knowledge domains, and write a summary.

## Inputs
- Active project name (from `status.yaml`)
- Any files inside `projects/<project>/context/`

## Outputs
- `.work/context-audit.md` inside the project's folder.

## Process
1. Locate the context resources for the current active project in `projects/<project>/context/`.
2. Inventory all files (PDF, DOCX, etc.).
3. Extract the text using appropriate tools or scripts.
4. **Pedagogical Breakdown:** For each extracted topic/domain, you MUST break it down into detailed Learning Objective descriptions following the ULO, CIO, SIO model:
   - **ULO (Universal Learning Objective):** The agnostic, conceptual capability.
   - **CIO (Conceptual Implementation Objective):** The technology-specific application of the concept.
   - **SIO (Specific Implementation Objective):** The granular, actionable, testable skill.
5. Create a `context-audit.md` in `projects/<project>/.work/` that lists the domains AND their detailed ULO/CIO/SIO breakdowns. This ensures the intent is fully fleshed out before any Master Tree mapping is attempted.

## Handoff
Once `context-audit.md` is written, you are done. The `@taxonomy-mapper` will use your output to map these domains into the formal Knowledge Tree.
