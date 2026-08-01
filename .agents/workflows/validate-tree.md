---
description: Run this workflow to validate the referential integrity of the project's Knowledge Tree. Must PASS (0 errors) before proceeding to coverage audit or sync.
---

# Workflow: Validate Tree

> Validates all 6 TSV files in `projects/<project>/output/` for referential integrity. Must PASS 100% (0 errors) before coverage audit or database sync.

**Command:** `/validate-tree`
**Owner:** `@tree-validator`
**Script:** `.agents/skills/tree-validator/scripts/validate_tree.py`

## Prerequisites

- Project output TSVs exist: `fields.tsv`, `subjects.tsv`, `categories.tsv`, `topics.tsv`, `concepts.tsv`, `learning-objectives.tsv`

## Contract

```bash
python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug>
```

## Validation Rules (Must Pass 100%)

| Rule | Severity | Description |
|---|---|---|
| `BROKEN_REFERENCE` | ERROR | Child references parent code that doesn't exist |
| `ORPHAN_NODE` | WARNING | Node not referenced by any child (expected for Master Tree reuse) |
| `DUPLICATE_CODE` | ERROR | Duplicate code within same TSV |
| `EMPTY_REQUIRED_FIELD` | ERROR | Required column empty |
| `LO_CONCEPT_UNCOVERED` | WARNING | Concept in concepts.tsv has no LO referencing it |
| `LO_MISSING_ASSESSMENT_APPROACH` | WARNING | ULO/CIO missing `assessment_approach` (Rule 7) |

## Expected Output

```
projects/<project>/.tree-validator/reports/<timestamp>/
├── validation_report.md     # Human-readable summary
└── validation_report.json   # Machine-readable details
```

## Gates

- **Gate §3 (Final Artifacts)**: Must PASS before `/sync-supabase`
- **Gate §9 (No Metric Gaming)**: Fix root cause, never write dummy scripts to force PASS

## After Validation

```bash
# Next: Coverage audit
/audit-coverage

# Then: Gap detection
/detect-gaps
```

## Legacy `--fix` Flag

The `--fix` flag is deprecated. All fixes must be done via explicit repair scripts in `.work/` or by editing source TSVs directly.