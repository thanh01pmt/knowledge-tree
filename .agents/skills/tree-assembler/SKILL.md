---
name: tree-assembler
description: Build the 6 final TSV project files by applying the approved mapping plan against the Master Knowledge Tree.
---

# Tree Assembler

> **Goal:** You are the `@tree-assembler`. Your job has two phases:
> 1. **Build taxonomy** (fields → concepts) from an approved `mapping-plan.md`.
> 2. **Sync** the validated TSV files to Supabase via `/sync-supabase`.
>
> ⚠️ `learning-objectives.tsv` is generated separately via the `/generate-los` workflow using the `learning-objective-generator` skill. It MUST be generated AFTER the taxonomy TSVs are built, so that valid concept codes can be used for grounding.

## Inputs
- `.work/mapping-plan.md` (Must be explicitly approved by the user)
- `.agents/skills/taxonomy-mapper/resources/master_tree.json`
- The existing output TSV files in `projects/<project>/output/`

## Outputs
- `projects/<project>/output/fields.tsv`
- `projects/<project>/output/subjects.tsv`
- `projects/<project>/output/categories.tsv`
- `projects/<project>/output/topics.tsv`
- `projects/<project>/output/concepts.tsv`
- *(Learning Objectives are NOT produced here — see `/generate-los`)*

## Process
1. Verify the teacher has approved the mapping plan.
2. Extract the exact list of `code`s needed for each taxonomy level from `mapping-plan.md`.
3. Look up those codes in `master_tree.json` to get all columns (`name`, `description`, `keywords`, `cs2023_ka_mapping`, `metadata`).
4. Write the rows to the 5 taxonomy TSV files.
5. Ensure referential integrity at every level (children must have parents).

## Scripts
- `assemble_project.py --project <slug> --source mapping-plan` → builds taxonomy from mapping-plan (**recommended**).
- `assemble_project.py --project <slug> --source lo-tsv` → builds taxonomy from LO concept_codes (backward-compat).
- `gen_real_los.py --project <slug>` → **Reference implementation only** for `swift-associate`. Use `llm_extract_lo.py` for new projects.
