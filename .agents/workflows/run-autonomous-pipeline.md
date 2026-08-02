---
description: Run this workflow to execute the entire Knowledge Tree pipeline autonomously end-to-end without human intervention. Used primarily by Agentic Crons.
---

# Workflow: Autonomous End-to-End Pipeline

> This workflow executes the complete Knowledge Tree generation pipeline from a scaffolded project to the final TSV files, utilizing `agent_as_judge.py` to bypass human approval gates.

**Command:** `/run-autonomous-pipeline`
**Owner:** `@coordinator`

## Prerequisites
- A project has been scaffolded (e.g., via `cron_academic_watcher.py` or `cron_trend_research.py`).
- The cron script output tells you the **project slug**. Capture it from the script's stdout (e.g. `Scaffolding project: academic-xxx-20260801`).
- Set the active project: update `status.yaml` with `active_project: <slug>`.

## ⚠️ STRICT RULES FOR AUTONOMOUS EXECUTION
1. Do NOT stop to ask the user for permission at any step.
2. Execute all steps sequentially in one go.
3. Use `agent_as_judge.py` to evaluate your own outputs at key checkpoints.
4. If ANY step fails after 3 retries, STOP the pipeline, write a failure report to `projects/INBOX.md`, commit, and push. Do NOT leave the pipeline in a half-done state without notification.

---

## Step 1: Context Audit
1. Read the source materials in `projects/<slug>/context/`.
2. Generate `.work/context-audit.md` summarizing the domains and syllabus.

## Step 2: Taxonomy Mapping
1. Run document hierarchy extraction:
   ```bash
   python3 .agents/skills/taxonomy-mapper/scripts/extract_document_hierarchy.py --project <slug>
   ```
2. Based on `structured_hints.json` and `context-audit.md`, draft the mapping plan.
3. Save it to `projects/<slug>/.work/mapping-plan.md`.

## Step 3: Agent-as-Judge — Mapping Plan (Replaces HITL Gate §4)
1. Execute the independent judge script:
   ```bash
   python3 .agents/skills/taxonomy-mapper/scripts/agent_as_judge.py \
     --artifact projects/<slug>/.work/mapping-plan.md \
     --stage mapping_plan
   ```
2. If the script exits with error, read the feedback, correct `mapping-plan.md`, and re-run (max 3 retries).
3. On success: `mapping-plan-approved.md` is created. Use THIS file for the next step.

## Step 4: Build Tree
```bash
python3 .agents/skills/tree-assembler/scripts/build_tree.py \
  --project <slug> \
  --plan projects/<slug>/.work/mapping-plan-approved.md
```

## Step 5: Generate ULOs + Judge Checkpoint
1. Generate ULOs:
   ```bash
   python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
     --phase ulos --project <slug>
   ```
2. **Judge checkpoint** — evaluate ULO quality:
   ```bash
   python3 .agents/skills/taxonomy-mapper/scripts/agent_as_judge.py \
     --artifact projects/<slug>/.work/phase_ulos.json \
     --stage ulo
   ```
3. If Judge rejects: read feedback, fix `phase_ulos.json`, re-run judge (max 3 retries).

## Step 6: Generate CIOs + Judge Checkpoint
1. Generate CIOs:
   ```bash
   python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
     --phase cios --project <slug>
   ```
2. **Judge checkpoint** — evaluate CIO quality (Marr 2-Language Test):
   ```bash
   python3 .agents/skills/taxonomy-mapper/scripts/agent_as_judge.py \
     --artifact projects/<slug>/.work/phase_cios.json \
     --stage cio
   ```
3. If Judge rejects: read feedback, fix `phase_cios.json`, re-run judge (max 3 retries).

## Step 7: Generate SIOs + Merge
SIOs are technology-specific (T6 does NOT apply), so no Judge checkpoint needed.
```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase sios --project <slug>
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase merge --project <slug>
```

## Step 8: Map Prerequisites
```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_map_prerequisites.py \
  --project <slug>
```

## Step 9: Integrity & Coverage Validation
1. Validate tree:
   ```bash
   python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug>
   ```
2. Audit coverage:
   ```bash
   python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <slug>
   ```
3. If validation fails: attempt auto-fix (max 2 iterations), then re-validate. If still failing after fixes, report failure to INBOX.

## Step 10: Finalize & Notify
1. Append a **success or failure** message to `projects/INBOX.md`:
   - **On success:** "✅ Project `<slug>` hoàn tất. 6 file TSV đã sẵn sàng trong `projects/<slug>/output/`. Mời duyệt và ra lệnh `/sync-supabase`."
   - **On failure:** "❌ Project `<slug>` gặp lỗi tại Step X. Chi tiết: [lỗi]. Cần can thiệp thủ công."
2. Commit and push:
   ```bash
   git add . && git commit -m "feat(automation): End-to-end generation for <slug>" && git push origin main
   ```
3. END OF WORKFLOW.
