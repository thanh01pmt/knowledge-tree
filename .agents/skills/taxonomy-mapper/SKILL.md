---
name: taxonomy-mapper
description: Cross-reference extracted project syllabus with the Master Knowledge Tree to establish a formal taxonomy mapping plan.
---

# Taxonomy Mapper

> **Goal:** You are the `@taxonomy-mapper`. Your job is to take the raw, unstructured syllabus topics from `/context-audit` and map them exactly to the codes defined in the Master Knowledge Tree.

## Inputs
- `.work/context-audit.md` (What needs to be taught/tested)
- `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` (or the parsed JSON in `.agents/resources/master_tree.json`)

## Outputs
- `.work/mapping-plan.md`

## Process
1. Read the required knowledge domains from the context audit.
2. Search the Master Tree to find the most appropriate `fields`, `subjects`, `categories`, `topics`, and `concepts`.
3. Evaluate if you need to reuse an existing code or propose a new one based on the "Tiêu chí Dùng lại vs Tạo mới" in AGENT.md.
4. Create a Markdown file (`mapping-plan.md`) that explicitly lists which `code`s will be included.
   - For existing codes: Just list them.
   - For NEW codes: Mark them clearly with `[NEW NODE PROPOSAL]`, provide the proposed `UPPER_SNAKE_CASE` code, Name, Description, and its exact Parent code. Justify why an existing code couldn't be used.
5. Organize the plan hierarchically so the teacher can easily review it.
6. **STOP:** You do not write any TSV files (neither the project TSVs nor the Master TSV). You only propose the plan. The teacher must approve this plan. If approved, you may be instructed to update the Master Tree TSV before `/build-tree` runs.
