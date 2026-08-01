#!/usr/bin/env python3
"""
sync_master_to_supabase.py — Đồng bộ Master Knowledge Tree TSV lên Supabase (One-way: TSV → DB).

Đây là tool CHÍNH THỨC để cập nhật Master Tree trên Supabase.
Chỉ chạy sau khi:
1. validate_master_tree PASS (Gate §7)
2. Human approve merge proposal (HITL Gate §4)
3. Staging TSV đã được merge vào Master TSV

KHÔNG bao giờ dùng check_master_sync.py --sync-down cho Master Tree!
"""

import argparse
import csv
import os
import sys
from pathlib import Path

# Sanitize NO_PROXY to prevent httpx InvalidURL parsing error on IPv6 addresses like ::1
os.environ.pop("NO_PROXY", None)
os.environ.pop("no_proxy", None)

from supabase import create_client


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("\"'")


def parse_master_tsv(tsv_path: Path) -> dict:
    """Parse the multi-table Master TSV using shared parser logic."""
    SECTIONS = {
        "Bảng 1": "fields",
        "Bảng 2": "subjects",
        "Bảng 3": "categories",
        "Bảng 4": "topics",
        "Bảng 5": "concepts",
        "Bảng 6": "learning_objectives",
    }
    SKIP_PREFIXES = (
        "Đây là", "Mỗi Field", "Các Subject", "Các Category", "Các Topic", "Các Concept",
    )
    data = {k: [] for k in SECTIONS.values()}
    current_level = None
    headers = []

    text = tsv_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue

        hit = next((k for k in SECTIONS if s.startswith(k)), None)
        if hit:
            current_level = SECTIONS[hit]
            headers = []
            continue

        if not current_level or s.startswith(SKIP_PREFIXES):
            continue

        parts = line.rstrip("\n").split("\t")
        if parts[0] == "code":
            headers = [h.strip() for h in parts]
            continue

        if headers and parts[0].strip():
            row_dict = {}
            for i, header in enumerate(headers):
                val = parts[i].strip() if i < len(parts) else ""
                row_dict[header] = val
            data[current_level].append(row_dict)

    return data


def sync_master_to_supabase(tsv_path: Path, dry_run: bool = False):
    repo_root = find_repo_root(tsv_path)
    load_env(repo_root)

    url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SUPABASE_SECRET_KEY")  # Use secret key for admin operations
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL và SUPABASE_SECRET_KEY phải được set trong .env")
        sys.exit(1)

    supabase = create_client(url, service_key)

    print(f"📄 Đang đọc Master TSV: {tsv_path}")
    master_data = parse_master_tsv(tsv_path)

    # Master tables in dependency order
    tables_config = [
        ("fields", ["keywords"], ["display_order"]),  # skip display_order - not in Supabase schema
        ("subjects", ["field_codes"], []),
        ("categories", ["subject_codes", "field_codes"], []),
        ("topics", ["category_codes", "subject_codes", "field_codes"], []),
        ("concepts", ["topic_codes", "category_codes", "subject_codes", "field_codes", "prerequisite_concept_codes"], []),
        # learning_objectives is NOT in Master TSV (project-specific)
    ]

    print(f"\n{'🔍 DRY RUN' if dry_run else '🚀 SYNCING'} MASTER TREE TO SUPABASE")
    print(f"==================================================")

    total_synced = 0
    for table_name, array_fields, skip_fields in tables_config:
        rows = master_data.get(table_name, [])
        print(f"\n  📋 {table_name.upper()}: {len(rows)} rows")

        if dry_run:
            for r in rows[:3]:
                code = r.get("code", "")
                name = r.get("name", "")[:50]
                print(f"     → {code}: {name}")
            if len(rows) > 3:
                print(f"     ... (+{len(rows)-3} more)")
            total_synced += len(rows)
            continue

        # Fetch existing codes for upsert optimization
        tsv_codes = [r.get("code", "").strip() for r in rows if r.get("code", "").strip()]
        code_to_id = {}
        if tsv_codes:
            BATCH_SIZE = 500
            for i in range(0, len(tsv_codes), BATCH_SIZE):
                batch_codes = tsv_codes[i:i + BATCH_SIZE]
                try:
                    page = supabase.table(table_name).select("id, code").in_("code", batch_codes).execute()
                    for r in page.data:
                        if r.get("code"):
                            code_to_id[r["code"]] = r["id"]
                except Exception as e:
                    print(f"     ⚠️ Warning: Failed to fetch existing codes for {table_name} batch {i//BATCH_SIZE}: {e}")

        synced_count = 0
        updated_count = 0
        inserted_count = 0

        for r in rows:
            code = r.get("code", "").strip()
            if not code:
                continue

            payload = {"organization_code": "DEFAULT_ORG"}

            for k, v in r.items():
                if not k:
                    continue
                k = k.strip()
                if k in array_fields or k in skip_fields:
                    continue

                val = v.strip() if v else ""

                if val == "":
                    if k in ["name", "description"]:
                        payload[k] = ""
                    continue

                payload[k] = val

            payload["code"] = code

            for af in array_fields:
                if af in r:
                    val_str = r[af].strip()
                    if val_str:
                        vals = [v.strip() for v in val_str.replace(";", ",").split(",") if v.strip()]
                        payload[af] = vals
                    else:
                        payload[af] = []

            if code in code_to_id:
                payload["id"] = code_to_id[code]
                supabase.table(table_name).upsert(payload).execute()
                updated_count += 1
            else:
                res = supabase.table(table_name).insert(payload).execute()
                if res.data:
                    code_to_id[code] = res.data[0]["id"]
                    inserted_count += 1
            synced_count += 1

        print(f"     ✅ {synced_count} synced (Updated {updated_count}, Inserted {inserted_count})")
        total_synced += synced_count

    print(f"\n==================================================")
    if dry_run:
        print(f"🔍 DRY RUN COMPLETE: {total_synced} rows would be synced")
    else:
        print(f"🎉 MASTER TREE SYNC COMPLETED: {total_synced} rows synced!")
    print(f"==================================================")


def main():
    parser = argparse.ArgumentParser(
        description="Sync Master Knowledge Tree TSV to Supabase (One-way: TSV → DB)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (safe preview)
  python sync_master_to_supabase.py --tsv .agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv --dry-run

  # Actual sync (requires human approval per Gate §4)
  python sync_master_to_supabase.py --tsv .agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv

⚠️  WARNING: This REPLACES Master Tree data in Supabase.
    Only run after: validate_master_tree PASS + HITL Gate §4 approval.
    NEVER use check_master_sync.py --sync-down for Master Tree!
"""
    )
    parser.add_argument("--tsv", type=str, default=".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv",
                        help="Path to Master TSV file")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing to DB")
    args = parser.parse_args()

    tsv_path = Path(args.tsv)
    if not tsv_path.is_file():
        print(f"❌ File không tồn tại: {tsv_path}")
        sys.exit(1)

    if not args.dry_run:
        confirm = input("\n⚠️  THIS WILL REPLACE MASTER TREE DATA IN SUPABASE. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Đã hủy.")
            sys.exit(0)

    sync_master_to_supabase(tsv_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()