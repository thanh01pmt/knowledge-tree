---
name: supabase-sync
description: Đồng bộ dữ liệu 6 file TSV của dự án (fields, subjects, categories, topics, concepts, learning-objectives) lên cơ sở dữ liệu Supabase theo thứ tự phụ thuộc nghiêm ngặt và cơ chế ghi đè (upsert by code).
---

# Supabase Sync Skill

> **Goal:** Synchronize validated project output TSVs in `projects/<project>/output/` into Supabase database tables while strictly maintaining referential dependency order and preserving original row UUIDs.

## Inputs
- Active project name (from `status.yaml` or CLI `--project <slug>`)
- The 6 validated output TSV files in `projects/<project>/output/`
- Connection credentials in `.env` (`SUPABASE_URL` and `SERVICE_ROLE_KEY`)

## Outputs
- Updated database records in Supabase Cloud (`fields`, `subjects`, `categories`, `topics`, `concepts`, `learning_objectives`).

## Dependency Rules (Thứ tự phụ thuộc)
1. **Top-Down Table Order:**
   `fields` ➔ `subjects` ➔ `categories` ➔ `topics` ➔ `concepts` ➔ `learning_objectives`
2. **LO Parent Ordering:**
   In `learning_objectives`, `UNIVERSAL` nodes are written before `CONCEPTUAL_IMPL`, which are written before `SPECIFIC_IMPL`.
3. **Upsert Semantics:**
   Look up existing UUID `id` by `code`. If `code` exists, upsert using `id` to update data in-place without breaking relational keys. If missing, insert as new record.
4. **Non-destructive Upsert Policy (No Automatic Deletes):**
   `sync_to_supabase.py` uses `.upsert()` / `.insert()` exclusively. It **does NOT** execute `.delete()` on records that are removed from local TSV files. This behavior is intentional to prevent accidental cascade deletion of student progress tracking and historical mastery metrics (`student_mastery`). If a record must be purged from Supabase, it must be deleted via explicit SQL migration or direct admin database query.

## Scripts
- `.agents/skills/supabase-sync/scripts/sync_to_supabase.py`
