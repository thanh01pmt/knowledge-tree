---
description: Run this workflow to generate Learning Objectives from the project syllabus, grounded in the concepts already built for the project.
---

# Workflow: Generate Learning Objectives

> Run this workflow to generate `learning-objectives.tsv` from the project syllabus. Must be run AFTER `/build-tree` so that valid concept codes are available for grounding.

**Command:** `/generate-los`
**Owner:** `@tree-assembler`

## Prerequisites
- `/build-tree` must have completed successfully: `projects/<project>/output/concepts.tsv` must exist and be non-empty.

## Contract
1. Read the active project from `status.yaml` (or use `--project <slug>`).
2. Read the valid concept codes from `projects/<project>/output/concepts.tsv`.
3. Read the raw syllabus text from `projects/<project>/.work/raw_pdf.txt` OR `projects/<project>/.work/context-audit.md` as fallback.
4. Inject the valid concept codes into the LLM system prompt so the model ONLY uses codes that exist in the project taxonomy.
5. Run `python3 .agents/skills/learning-objective-generator/scripts/llm_extract_lo.py --project <slug>`.
6. Validate that all `concept_codes` in the generated LOs exist in `concepts.tsv`.
7. Write the output to `projects/<project>/output/learning-objectives.tsv`.
8. Run `/validate-tree` to ensure referential integrity.
