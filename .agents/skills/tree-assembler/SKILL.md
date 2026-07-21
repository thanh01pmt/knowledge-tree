---
name: tree-assembler
description: Build the 6 final TSV project files by applying the approved mapping plan against the Master Knowledge Tree.
---

# Tree Assembler

> **Goal:** You are the `@tree-assembler`. After the teacher has approved the `mapping-plan.md`, your job is to extract the full data rows from the Master Tree and write them into the project's TSV files.

## Inputs
- `.work/mapping-plan.md` (Must be explicitly approved by the user)
- `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` (or JSON version)
- The existing empty TSV files in `projects/<project>/`

## Outputs
- `projects/<project>/output/fields.tsv`
- `projects/<project>/output/subjects.tsv`
- `projects/<project>/output/categories.tsv`
- `projects/<project>/output/topics.tsv`
- `projects/<project>/output/concepts.tsv`
- `projects/<project>/output/learning-objectives.tsv`

## Process
1. Verify that the teacher has approved the mapping plan.
2. Extract the exact list of `code`s needed for each level.
3. Look up those codes in the Master Tree to get all columns (`name`, `description`, `keywords`, etc.).
4. Overwrite (or intelligently merge if they are not empty) the project TSV files with the newly extracted rows.
5. Make sure the headers remain intact (`code \t name \t description ...`).
6. Ensure referential integrity (e.g. if you pull a concept, make sure its parent topic is also pulled into the topics TSV).
