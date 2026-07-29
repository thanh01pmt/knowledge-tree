#!/usr/bin/env python3
"""
sync_to_supabase.py — Đồng bộ dữ liệu 6 file TSV của dự án lên Supabase tuân thủ nghiêm ngặt tính phụ thuộc (Dependency Order).

Thứ tự phụ thuộc (Top-Down Order):
1. fields (Tầng cao nhất)
2. subjects (Phụ thuộc fields)
3. categories (Phụ thuộc subjects)
4. topics (Phụ thuộc categories)
5. concepts (Phụ thuộc topics)
6. learning_objectives (Phụ thuộc concepts & phân tầng parent_lo_code: UNIVERSAL -> CONCEPTUAL_IMPL -> SPECIFIC_IMPL)
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
                    os.environ[k.strip()] = v.strip().strip("'\"")

def sync_project_to_supabase(slug: str, repo_root: Path):
    load_env(repo_root)

    url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SERVICE_ROLE_KEY")
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL và SERVICE_ROLE_KEY phải được set trong .env hoặc environment variables.")
        sys.exit(1)

    supabase = create_client(url, service_key)

    out_dir = repo_root / "projects" / slug / "output"
    if not out_dir.is_dir():
        print(f"❌ Error: Output directory '{out_dir}' does not exist.")
        sys.exit(1)

    # 1. BẮT BUỘC THỨ TỰ ĐỒNG BỘ TOP-DOWN
    # Bao gồm cả learning_objective_prerequisites ở cuối cùng (Phase E)
    tables_config = [
        ("fields.tsv", "fields", ["field_codes"]),
        ("subjects.tsv", "subjects", ["field_codes"]),
        ("categories.tsv", "categories", ["subject_codes", "field_codes"]),
        ("topics.tsv", "topics", ["category_codes", "subject_codes", "field_codes"]),
        ("concepts.tsv", "concepts", ["topic_codes", "category_codes", "subject_codes", "field_codes", "prerequisite_concept_codes"]),
        ("learning-objectives.tsv", "learning_objectives", ["concept_codes", "topic_codes", "category_codes", "subject_codes", "field_codes"]),
        ("lo_prerequisites.tsv", "learning_objective_prerequisites", [])
    ]

    print(f"==================================================")
    print(f"🚀 SYNCING PROJECT '{slug}' TO SUPABASE (STRICT DEPENDENCY ORDER)")
    print(f"==================================================")

    for tsv_name, table_name, array_fields in tables_config:
        tsv_path = out_dir / tsv_name
        if not tsv_path.is_file():
            print(f"⚠️ Warning: File {tsv_name} not found, skipping...")
            continue

        with open(tsv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            rows = list(reader)

        if table_name == "learning_objective_prerequisites":
            # Batch upsert (chunk of 200) to avoid per-row round-trip latency
            # and reduce risk of partial sync on large prerequisite graphs.
            batch_payloads = []
            skipped = 0
            for r in rows:
                target_code = r.get("learning_objective_code", "").strip()
                prereq_code = r.get("prerequisite_lo_code", "").strip()
                if not target_code or not prereq_code:
                    skipped += 1
                    continue
                batch_payloads.append({
                    "learning_objective_code": target_code,
                    "prerequisite_lo_code": prereq_code,
                    "rationale": r.get("rationale", "").strip(),
                    "source_layer": r.get("source_layer", "L3-LLM").strip() or "L3-LLM",
                })
                if len(batch_payloads) >= 200:
                    supabase.table(table_name).upsert(
                        batch_payloads,
                        on_conflict="learning_objective_code,prerequisite_lo_code"
                    ).execute()
                    batch_payloads = []
            if batch_payloads:
                supabase.table(table_name).upsert(
                    batch_payloads,
                    on_conflict="learning_objective_code,prerequisite_lo_code"
                ).execute()
            synced_count = len(rows) - skipped
            print(f"  • {table_name:<20}: {synced_count} synced (Upserted in batches of 200, {skipped} skipped)")
            continue

        # For normal tables - OPTIMIZED: fetch only codes we need using 'in' query
        # Collect all codes from the TSV first
        tsv_codes = [r.get("code", "").strip() for r in rows if r.get("code", "").strip()]
        
        # Đối với learning_objectives: sắp xếp theo thứ tự phụ thuộc parent_lo_code (UNIVERSAL -> CONCEPTUAL_IMPL -> SPECIFIC_IMPL)
        if table_name == "learning_objectives":
            type_priority = {"UNIVERSAL": 0, "CONCEPTUAL_IMPL": 1, "SPECIFIC_IMPL": 2}
            rows.sort(key=lambda x: type_priority.get(x.get("lo_type", "UNIVERSAL").strip(), 99))

        # Fetch existing records for ONLY the codes we have in TSV (batched for PostgREST limits)
        code_to_id = {}
        if tsv_codes:
            # PostgREST has a limit on 'in' query size (~1000 items per query)
            # Batch the codes to avoid URL length limits
            BATCH_SIZE = 500
            for i in range(0, len(tsv_codes), BATCH_SIZE):
                batch_codes = tsv_codes[i:i + BATCH_SIZE]
                try:
                    page = supabase.table(table_name).select("id, code").in_("code", batch_codes).execute()
                    for r in page.data:
                        if r.get("code"):
                            code_to_id[r["code"]] = r["id"]
                except Exception as e:
                    print(f"  ⚠️ Warning: Failed to fetch existing codes for {table_name} batch {i//BATCH_SIZE}: {e}", file=sys.stderr)

        synced_count = 0
        updated_count = 0
        inserted_count = 0

        for r in rows:
            code = r.get("code", "").strip()
            if not code:
                continue

            payload = {
                "code": code,
                "name": r.get("name", "").strip(),
                "description": r.get("description", "").strip(),
                "organization_code": "DEFAULT_ORG"
            }

            for af in array_fields:
                if af in r:
                    vals = [v.strip() for v in r[af].replace(";", ",").split(",") if v.strip()]
                    payload[af] = vals

            if table_name == "learning_objectives":
                payload["lo_type"] = r.get("lo_type", "UNIVERSAL").strip()
                p_code = r.get("parent_lo_code", "").strip()
                payload["parent_lo_code"] = p_code if p_code and p_code.upper() != "NULL" else None
                if r.get("bloom_level", "").strip():
                    payload["bloom_level"] = r["bloom_level"].strip()
                if r.get("knowledge_dimension", "").strip():
                    payload["knowledge_dimension"] = r["knowledge_dimension"].strip()
                if r.get("assessment_approach", "").strip():
                    payload["assessment_approach"] = r["assessment_approach"].strip()

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

        print(f"  • {table_name:<20}: {synced_count} synced (Updated {updated_count}, Inserted {inserted_count})")

    print(f"==================================================")
    print(f"🎉 DEPENDENCY-AWARE SYNC COMPLETED FOR '{slug}'!")
    print(f"==================================================")

def load_status(repo_root: Path) -> dict:
    status_file = repo_root / "status.yaml"
    if not status_file.is_file():
        return {}
    import yaml  # type: ignore
    with open(status_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def main():
    parser = argparse.ArgumentParser(description="Sync project TSV files to Supabase database with dependency ordering")
    parser.add_argument("--project", type=str, help="Project slug")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    slug = args.project
    if not slug:
        status = load_status(repo_root)
        slug = status.get("active_project")
        if not slug:
            print("❌ Error: No project specified and active_project not set in status.yaml")
            sys.exit(1)

    sync_project_to_supabase(slug, repo_root)

if __name__ == "__main__":
    main()
