---
description: Run this workflow to sync the validated project TSV output files into Supabase. Gate §8: Human approval REQUIRED before execution.
---

# Workflow: Sync to Supabase

> Sync 6 validated TSV files to Supabase Cloud DB. **Gate §8: Human approval REQUIRED** — no auto-sync.

**Command:** `/sync-supabase`
**Owner:** `@tree-assembler`
**Skill:** `supabase-sync`

## Prerequisites (All Gates Must Pass)

- [ ] `/validate-tree` → **PASS** (0 errors) — Gate §3
- [ ] `/audit-coverage` → **PASS** (≥95%) — Gate §6
- [ ] `/detect-gaps` → **Reviewed** (no critical gaps)
- [ ] **Gate §8 HITL**: Explicit user approval to push to cloud

## Contract

```bash
python3 .agents/skills/supabase-sync/scripts/sync_to_supabase.py --project <slug>
```

## Sync Order (Dependency-Aware)

| Order | Table | Foreign Keys |
|-------|-------|-------------|
| 1 | `fields` | — |
| 2 | `subjects` | `field_codes` |
| 3 | `categories` | `subject_codes` |
| 4 | `topics` | `category_codes` |
| 5 | `concepts` | `topic_codes`, `prerequisite_concept_codes` |
| 6 | `keywords` | `concept_codes` |
| 7 | `learning_objectives` | `concept_codes`, `parent_lo_code` |
| 8 | `learning_objective_prerequisites` | `learning_objective_code`, `prerequisite_lo_code` |

**Mechanism**: Upsert by `code` (PK). Existing `id` preserved on update.

## Expected Output

```
📊 Supabase Sync Report — <project>
┌──────────────────────┬───────┬─────────┬──────────┐
│ Table                │ Total │ Updated │ Inserted │
├──────────────────────┼───────┼─────────┼──────────┤
│ fields               │ N     │ 0       │ N        │
│ subjects             │ N     │ 0       │ N        │
│ categories           │ N     │ 0       │ N        │
│ topics               │ N     │ 0       │ N        │
│ concepts             │ N     │ 0       │ N        │
│ keywords             │ N     │ 0       │ N        │
│ learning_objectives  │ N     │ 0       │ N        │
│ lo_prerequisites     │ N     │ 0       │ N        │
└──────────────────────┴───────┴─────────┴──────────┘
✅ Sync complete — N records processed
```

## Gate §8 — Security Boundary

> **CẤM TUYỆT ĐỐI** tự động thực thi `/sync-supabase` hoặc đẩy dữ liệu lên DB/Cloud nếu **chưa nhận được phê duyệt trực tiếp từ người dùng**. Bao gồm cả thao tác "restore" — không chỉ cập nhật mới.

- Must receive explicit: "Yes, sync to Supabase" or similar
- Applies to initial sync, updates, AND restores
- No `--auto-approve` or `--force` flags

## Post-Sync

- Update `status.yaml` with sync timestamp
- Verify in Supabase Dashboard: Table Editor → row counts match