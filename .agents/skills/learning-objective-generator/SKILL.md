---
name: learning-objective-generator
description: Extract and generate structured Learning Objectives (ULO, CIO, SIO) from raw syllabus and context text using LLM scripts.
---

# Learning Objective Generator

> **Goal:** Extract structured Learning Objectives following the 3-tier hierarchy (Universal LO -> Conceptual Implementation LO -> Specific Implementation LO) from raw syllabus material in `projects/<project>/context/`.

## Inputs
- Raw context text or PDF in `projects/<project>/context/`
- Active project slug from `status.yaml`

## Outputs
- Structured LO definitions in `.work/context-audit.md` or `projects/<project>/output/learning-objectives.tsv`.

## Scripts
- `.agents/skills/learning-objective-generator/scripts/llm_extract_lo.py`
