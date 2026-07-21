# Workflow: Audit Coverage (Đối chiếu ngược độ phủ Syllabus)

> Run this workflow to perform a reverse cross-referencing audit between the generated project TSV files (specifically `learning-objectives.tsv`) and the source context files (`context/` syllabus or PDF).

**Command:** `/audit-coverage`
**Owner:** `@tree-validator`

## Contract
1. Run `python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <project>`.
2. Extract all Objective Domains / Syllabus topics from the source PDF / context files.
3. Cross-reference each syllabus item against `learning-objectives.tsv` to verify coverage.
4. Generate a detailed markdown report at `projects/<project>/.tree-validator/reports/<timestamp>/coverage_report.md` and `.work/coverage_audit.md`.
5. Report the Coverage Score (%), missing items (gaps), and coverage status (`PASS` if >= 95%, `FAIL` otherwise) to the user.
