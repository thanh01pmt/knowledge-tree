---
description: Run this workflow to validate referential integrity, cross-level collisions, empty parents, and level skips for the Master Knowledge Tree TSV. Gate §7: Must PASS before reading Master Tree for any project workflow.
---

# Workflow: Validate Master Tree

> Validates the Master Knowledge Tree TSV (`services/python-api/general-context/mlo-knowlege-tree.tsv`) for referential integrity and collision detection. **Must PASS before `/map-taxonomy` or `/build-tree`** (Gate §7).

**Command:** `/validate-master-tree`
**Owner:** `@tree-validator`
**Script:** `.agents/skills/tree-validator/scripts/validate_master_tree.py`

## Prerequisites

- Master Tree TSV at `services/python-api/general-context/mlo-knowlege-tree.tsv`
- Skills copy at `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` (auto-synced after parse)

## Contract

```bash
# Validate main copy
python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv services/python-api/general-context/mlo-knowlege-tree.tsv

# Validate skills copy (should match after parse_master_tree.py)
python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv .agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv
```

## Validation Rules (Must PASS 100%)

| Rule | Severity | Description |
|------|----------|-------------|
| `BROKEN_REFERENCE` | ERROR | Child references parent code that doesn't exist |
| `CROSS_LEVEL_COLLISION` | ERROR | Same code used at different hierarchy levels |
| `EMPTY_PARENT` | WARNING | Node has empty parent code but is not a root |
| `LEVEL_SKIP` | ERROR | Child skips hierarchy level (e.g., field → topic) |
| `T6_VIOLATION` | ERROR | Technology name found in technology-agnostic tier |

## Expected Output

Script prints results to stdout. Example:
```
Checking services/python-api/general-context/mlo-knowlege-tree.tsv:
❌ 0 error(s), ⚠️ 0 warning(s)
```

## Gates

- **Gate §7 (Master Tree Integrity)**: Must PASS before `/map-taxonomy` reads Master Tree
- **Gate §9 (No Metric Gaming)**: Fix root cause, never write dummy scripts to force PASS

## After Validation (If PASS)

```bash
# Parse Master Tree to skills cache (auto-syncs resources)
python3 .agents/skills/taxonomy-mapper/scripts/parse_master_tree.py

# Proceed to project workflow
/map-taxonomy
/build-tree
```

## If Errors Found

1. Fix `services/python-api/general-context/mlo-knowlege-tree.tsv` directly
2. Re-run validation
3. Re-parse: `python3 .agents/skills/taxonomy-mapper/scripts/parse_master_tree.py`
