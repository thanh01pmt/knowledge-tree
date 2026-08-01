---
description: Run this workflow to perform a reverse cross-referencing audit between the generated project TSV files (specifically `learning-objectives.tsv`) and the source context files (`context/` syllabus or PDF). Required Gate §6.
---

# Workflow: Audit Coverage (Đối chiếu ngược độ phủ Syllabus)

> Reverse coverage audit: every syllabus item must have ≥1 LO covering it. Target: ≥95% coverage score.

**Command:** `/audit-coverage`
**Owner:** `@tree-validator`
**Script:** `.agents/skills/tree-validator/scripts/audit_coverage.py`

## Prerequisites

- `/validate-tree` must PASS (0 errors) — Gate §3
- `learning-objectives.tsv` exists in project output
- Source syllabus in `projects/<project>/context/`

## Contract

```bash
python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <slug>
```

## Process

1. Parse syllabus items from `context/` (PDF text, markdown, or structured syllabus)
2. Cross-reference each syllabus item against `learning-objectives.tsv` descriptions
3. Compute coverage score: `covered_items / total_syllabus_items × 100%`
4. Generate detailed report

## Expected Output

```
projects/<project>/.tree-validator/reports/<timestamp>/
└── coverage_report.md      # Human-readable with gap table

projects/<project>/.work/
└── coverage_audit.md       # Copy for quick access
```

## Gate §6 — Reverse Coverage Gate

- **PASS**: Coverage Score ≥ 95%
- **FAIL**: Coverage Score < 95% → Run `/detect-gaps` and address missing LOs

## Report Sections

| Section | Description |
|---|---|
| **Syllabus → LO Mapping** | Each syllabus item + covering LO codes |
| **Missing / Gap Items** | Syllabus items with NO covering LO |
| **Concept Coverage** | Concepts in project with/without LOs |
| **Coverage Score** | Percentage + PASS/FAIL status |

## After Audit

```bash
# If gaps found:
/detect-gaps

# If PASS and validation PASS:
/sync-supabase  (requires Gate §8 HITL approval)
```