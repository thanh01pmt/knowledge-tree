---
description: Run this workflow to assemble the final project TSV files based on an approved mapping plan.
---

# Workflow: Build Tree

> Run this workflow to assemble the final project taxonomy TSV files (fields → concepts) based on an approved mapping plan. NOTE: Learning Objectives (`learning-objectives.tsv`) are generated separately via the hierarchical pipeline (`/generate-ulos` → `/generate-cios` → `/generate-sios`), which must run AFTER this workflow.

**Command:** `/build-tree`
**Owner:** `@tree-assembler`
**Script:** `.agents/skills/tree-assembler/scripts/assemble_project.py`

## Contract

1. Verify that `projects/<project>/.work/mapping-plan.md` has been explicitly approved by the user.
2. Read the master data from `.agents/skills/taxonomy-mapper/resources/master_tree.json`.
3. Filter the master data to extract ONLY the rows selected in the mapping plan.
4. Write the exact rows (with all columns like `keywords`, `cs2023_ka_mapping`, `metadata`) to 5 project TSV files: `fields.tsv`, `subjects.tsv`, `categories.tsv`, `topics.tsv`, `concepts.tsv`.
5. Ensure referential integrity (children must have parents at every level).

## Step 6 — Taxonomy Coherence Validation (tự động)

Sau khi build, chạy validation để phát hiện mapping issues:

```bash
python3 .agents/skills/tree-assembler/scripts/validate_taxonomy_coherence.py --project <slug>
```

**Các check:**
- **KA Coherence**: Concept trong cùng topic có CS2023 KA codes gần nhau không?
- **Parent-child validity**: Mọi parent reference có tồn tại trong Master Tree không?
- **Hierarchy depth**: Chuỗi concept → topic → category → subject → field có hợp lệ không?

Cảnh báo ghi vào `.work/taxonomy_warnings.json` — không block, chỉ warning.

## Step 7 — Validate

```bash
/validate-tree
```

Confirm no BROKEN_REFERENCE or ORPHAN errors exist.

## Step 8 — (Optional) Master Gap Detection

```bash
python3 .agents/skills/taxonomy-mapper/scripts/detect_master_gaps.py --project <slug>
```

Phát hiện syllabus domains không có trong Master Tree. Output: `.work/master_gap_report.md`.

## After This Workflow

```bash
# Generate learning objectives grounded in the concepts just built
/generate-ulos
/generate-cios
/generate-sios
```
