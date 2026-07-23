## Description of Changes

Briefly summarize the changes made in this Pull Request.

---

## Type of Change

- [ ] Data fix / Taxonomy update in Master Tree (`mlo-knowlege-tree.tsv`)
- [ ] Script fix / feature enhancement (`validate_tree.py`, `assemble_project.py`, etc.)
- [ ] Workflow / Agent rule update (`AGENTS.md`, `RULES.md`)
- [ ] New project creation (`projects/<slug>/`)
- [ ] Documentation update

---

## Validation Checklist

Before submitting this PR, please check that all the following gates pass:

- [ ] **Master Tree Gate**: `python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv general-context/mlo-knowlege-tree.tsv` passes with `0 error(s)`.
- [ ] **Skill Copy Sync**: `python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv .agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` passes with `0 error(s)`.
- [ ] **JSON Rebuilt**: Ran `python3 .agents/skills/taxonomy-mapper/scripts/parse_master_tree.py` if TSVs were modified.
- [ ] **Project Tree Gate**: `python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug>` passes with `[PASS] 0 lỗi`.
- [ ] **Coverage Audit**: `python3 .agents/skills/tree-validator/scripts/audit_coverage.py` achieves $\ge 90\%$ score.
