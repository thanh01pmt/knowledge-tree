# Knowledge Tree Team

## Workflow Index

| Command | Owner | Primary result |
|---|---|---|
| `/init <project>` | scaffolder | Scaffold project TSV files (updates status.yaml) |
| `/set-project` | coordinator | Update active_project in status.yaml |
| `/context-audit` | @context-analyzer | Read project syllabus/PDFs |
| `/map-taxonomy` | @taxonomy-mapper | Cross-reference syllabus with Master TSV -> mapping-plan.md |
| `/build-tree` | @tree-assembler | Apply mapping-plan.md to build 5 taxonomy TSVs (fields → concepts) |
| `/generate-los` | @tree-assembler | Generate `learning-objectives.tsv` via LLM, grounded in project concept codes |
| `/detect-gaps` | @tree-validator | Run `detect_gaps.py` to find 3 gap types: missing LO coverage, shallow CIOs, master candidates |
| `/validate-tree` | @tree-validator | Run `validate_tree.py` for structural referential integrity |
| `/audit-coverage` | @tree-validator | Run `audit_coverage.py` to cross-reference LO output against source PDF |
| `/sync-supabase` | @tree-assembler | Run `sync_to_supabase.py` to push TSVs into Supabase Cloud DB |

## scaffolder
- Goal: Scaffold project directory structure, 6 output TSV headers, and set active project in `status.yaml`.
- Script: `.agents/skills/tree-validator/scripts/scaffold_tree.py`

## @context-analyzer
- Goal: Extract syllabus and knowledge domains from `projects/<project>/context/` source files.
- Skill: `project-context-loader`

## @taxonomy-mapper
- Goal: Map the extracted domains to exact codes in `KnowledgeTree v2.2.tsv`.
- Handover: `.work/mapping-plan.md`
- Skill: `taxonomy-mapper`

## @tree-assembler
- Goal: (1) Build 5 taxonomy TSVs from approved mapping-plan. (2) Generate learning-objectives.tsv via /generate-los after build-tree. (3) Sync to Supabase via /sync-supabase.
- Skill: `tree-assembler`, `learning-objective-generator`, `supabase-sync`

## @tree-validator
- Goal: Run validation script (`validate_tree.py`) & reverse coverage audit (`audit_coverage.py`) to ensure 100% referential integrity and 100% syllabus coverage.
- Skill: `tree-validator`
