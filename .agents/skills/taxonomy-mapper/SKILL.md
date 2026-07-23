---
name: taxonomy-mapper
description: Cross-reference extracted project syllabus with the Master Knowledge Tree to establish a formal taxonomy mapping plan.
---

# Taxonomy Mapper

> **Goal:** You are the `@taxonomy-mapper`. Your job is to take the raw, unstructured syllabus topics from `/context-audit` and map them exactly to the codes defined in the Master Knowledge Tree using N:N Multi-parent Topology.

## Inputs
- `.work/context-audit.md` (What needs to be taught/tested)
- `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` (or the parsed JSON in `.agents/skills/taxonomy-mapper/resources/master_tree.json`)

## Outputs
- `.work/mapping-plan.md`

## Process & N:N Topology Rules
1. Read the required knowledge domains from the context audit.
2. Search the Master Tree to find the most appropriate `fields`, `subjects`, `categories`, `topics`, and `concepts`.
3. **N:N Graph Reuse Principle:**
   - Always prefer REUSING existing Categories and Topics across the entire Master Tree before proposing new ones.
   - All levels support **Many-to-Many (N:N)** relationships via comma-separated codes (`field_codes`, `subject_codes`, `category_codes`, `topic_codes`).
   - If an existing Category/Topic belongs to another Subject, append the target Subject code to its parent list separated by commas `,` (e.g. `subject_codes: NETWORKING, WEB_DEV`).
4. Create a Markdown file (`mapping-plan.md`) that explicitly lists which `code`s will be included.
   - For existing codes: Just list them.
   - For NEW Concept proposals: Mark clearly with `[NEW NODE PROPOSAL]`, provide `UPPER_SNAKE_CASE` code (must be a NOUN PHRASE), Name, Description, and its comma-separated parent codes.
5. Organize the plan hierarchically for review.
6. **STOP:** You do not write any project TSVs directly. You propose the plan for user/teacher approval. Upon approval, apply to staging via `.agents/skills/roadmap-aligner/scripts/apply_plan_to_staging.py`.
