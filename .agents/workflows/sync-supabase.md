---
description: Run this workflow to sync the validated project TSV output files (`projects/<project>/output/*.tsv`) into the corresponding tables in the Supabase database.
---

# Workflow: Sync to Supabase

> Run this workflow to sync the validated project TSV output files (`projects/<project>/output/*.tsv`) into the corresponding tables in the Supabase database.

**Command:** `/sync-supabase`
**Owner:** `@tree-assembler`

## Contract

1. Read the 6 validated TSV output files from `projects/<project>/output/`.
2. Connect to the active Supabase project database via API / Service Role Key.
3. For each table (`fields`, `subjects`, `categories`, `topics`, `concepts`, `learning_objectives`):
   - Match by `code`. If a record with the same `code` exists, fetch its `id` and **overwrite (UPSERT)** the data.
   - If the `code` does not exist, **INSERT** a new record.
4. Report the sync statistics (Total, Updated, Inserted count per table) to the user.
