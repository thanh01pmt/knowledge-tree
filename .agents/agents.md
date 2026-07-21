# Knowledge Tree Team

## Workflow Index

| Command | Owner | Primary result |
|---|---|---|
| `/init <project>` | scaffolder | Scaffold project TSV files (updates status.yaml) |
| `/set-project` | coordinator | Update active_project in status.yaml |
| `/context-audit` | @context-analyzer | Read project syllabus/PDFs |
| `/map-taxonomy` | @taxonomy-mapper | Cross-reference syllabus with Master TSV -> mapping-plan.md |
| `/build-tree` | @tree-assembler | Apply mapping-plan.md to project TSV files |
| `/validate-tree` | @tree-validator | Run `validate_tree.py` for structural referential integrity |
| `/audit-coverage` | @tree-validator | Run `audit_coverage.py` to cross-reference LO output against source PDF |

## @context-analyzer
- Goal: Extract syllabus and knowledge domains from `projects/<project>/context/` source files.
- Skill: `project-context-loader`

## @taxonomy-mapper
- Goal: Map the extracted domains to exact codes in `KnowledgeTree v2.2.tsv`.
- Handover: `.work/mapping-plan.md`
- Skill: `taxonomy-mapper`

## @tree-assembler
- Goal: Wait for user approval, then physically build the 6 TSV files.
- Skill: `tree-assembler`

## @tree-validator
- Goal: Run validation script (`validate_tree.py`) & reverse coverage audit (`audit_coverage.py`) to ensure 100% referential integrity and 100% syllabus coverage.
- Skill: `tree-validator`
