---
description: Run this workflow to generate hierarchical Learning Objectives (ULO → CIO → SIO) from the project syllabus. Replaces legacy /generate-los (1-shot). Must be run AFTER /build-tree so valid concept codes are available.
---

# Workflow: Generate Hierarchical Learning Objectives (3-Phase HITL)

> **Phased Approach**: ULOs (Phase A) → CIOs with Marr Test (Phase B) → SIOs + Merge (Phase C). Each phase has a Human-in-the-Loop checkpoint.

**Commands:** `/generate-ulos` → `/generate-cios` → `/generate-sios` → `/map-prerequisites`
**Owner:** `@tree-assembler`

## Prerequisites

- `/build-tree` completed: `projects/<project>/output/concepts.tsv` exists and non-empty
- `.work/raw_pdf.txt` or `.work/context-audit.md` contains source syllabus text

---

## Phase A: Generate ULOs (Universal Learning Objectives)

**Command:** `/generate-ulos`

**Script:**
```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase ulos --project <slug>
```

**Output:**
```
.work/hlo/
├── ulos.json          ← data
└── ulos_preview.md    ← summary table + descriptions
```

**HITL Checkpoint:** Review `ulos_preview.md`
- [ ] Technology-agnostic? (no Swift, React, Python, etc.)
- [ ] Bloom level: Evaluate / Create priority?
- [ ] Coverage: all key concepts have ULOs?
- [ ] Count: reasonable (not too many trivial ULOs)?

✅ Approve → proceed to `/generate-cios`

---

## Phase B: Generate CIOs (Conceptual Implementation Objectives)

**Command:** `/generate-cios`

**Script:**
```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase cios --project <slug>
```

**Output:**
```
.work/hlo/
├── cios.json          ← data (includes marr_test_note)
└── cios_preview.md    ← summary table with Marr Test Note column
```

**HITL Checkpoint (Strict - Marr 2-Language Test):** Review `cios_preview.md`
- [ ] `marr_test_note` mentions ≥2 distinct languages/tools?
- [ ] CIO description has NO technology-specific syntax/keywords?
- [ ] Each ULO has ≥1 CIO covering different approaches?
- ⚠️ **FAIL** if Marr test note empty or mentions only 1 language → rewrite CIO

✅ Approve → proceed to `/generate-sios`

---

## Phase C: Generate SIOs & Merge to TSV

**Command:** `/generate-sios`

**Scripts:**
```bash
# Step 1: Generate SIOs (technology-specific)
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase sios --project <slug> [--technology "Swift / SwiftUI"]

# Step 2: Merge ULO+CIO+SIO → learning-objectives.tsv
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase merge --project <slug>
```

**Output:**
```
.work/hlo/
└── sios.json

output/
└── learning-objectives.tsv  ← final 8-column TSV
```

---

## Phase E: Map Prerequisites (ADR-0005)

**Command:** `/map-prerequisites`

**Script:**
```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase prerequisites --project <slug>
```

**Output:**
```
output/
├── lo_prerequisites.tsv        ← LO prerequisite pairs
└── concepts.tsv (updated)      ← prerequisite_concept_codes added
```

---

## Validation (Run After Phase C/E)

```bash
python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug>
python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <slug>
python3 .agents/skills/tree-validator/scripts/detect_gaps.py --project <slug>
```

---

## Legacy `/generate-los` (Deprecated)

Old 1-shot script at `.agents/skills/learning-objective-generator/scripts/llm_extract_lo.py`.
Use only for quick prototypes — lacks Marr Test, Bloom priority, and HITL checkpoints.