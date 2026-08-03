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
import json
import os
import sys
from pathlib import Path

# Sanitize NO_PROXY to prevent httpx InvalidURL parsing error on IPv6 addresses like ::1
os.environ.pop("NO_PROXY", None)
os.environ.pop("no_proxy", None)

from supabase import create_client
import yaml


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
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("\"'")


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
        ("keywords.tsv", "keywords", ["concept_codes"]),
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
            # Special handling for prerequisites
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
            BATCH_SIZE = 100  # Reduced from 500 to avoid PostgREST URL length limits
            # Keywords table uses 'code' as primary key, not 'id'
            select_fields = "code" if table_name == "keywords" else "id, code"
            for i in range(0, len(tsv_codes), BATCH_SIZE):
                batch_codes = tsv_codes[i:i + BATCH_SIZE]
                try:
                    page = supabase.table(table_name).select(select_fields).in_("code", batch_codes).execute()
                    for r in page.data:
                        if r.get("code"):
                            # For keywords table, use code as the key since there's no id
                            key_value = r["code"] if table_name == "keywords" else r["id"]
                            code_to_id[r["code"]] = key_value
                except Exception as e:
                    print(f"  ⚠️ Warning: Failed to fetch existing codes for {table_name} batch {i//BATCH_SIZE}: {e}", file=sys.stderr)

        synced_count = 0
        updated_count = 0
        inserted_count = 0

        for r in rows:
            code = r.get("code", "").strip()
            if not code:
                continue

            if table_name == "learning_objectives":
                # Map TSV columns to Supabase schema
                payload = {"organization_code": "DEFAULT_ORG"}
                
                # Direct field mappings (string to string)
                direct_fields = ["name", "description", "lo_type", "cs2023_ka_mapping"]
                for field in direct_fields:
                    val = r.get(field, "").strip()
                    if val:
                        payload[field] = val
                
                # code is required
                payload["code"] = code
                
                # lo_type default
                if not payload.get("lo_type"):
                    payload["lo_type"] = "UNIVERSAL"
                
                # Array fields from TSV (comma/semicolon separated)
                array_fields_map = {
                    "bloom_level": "bloom_level_codes",
                    "knowledge_dimension": "context_codes",
                    "keywords": "keywords",
                    "concept_codes": "concept_codes",
                    "topic_codes": "topic_codes",
                    "category_codes": "category_codes",
                    "subject_codes": "subject_codes",
                    "field_codes": "field_codes",
                    "cs2023_ka_mapping": "cs2023_ka_mapping",
                }
                for tsv_field, sb_field in array_fields_map.items():
                    val = r.get(tsv_field, "").strip()
                    if val:
                        vals = [v.strip() for v in val.replace(";", ",").split(",") if v.strip()]
                        payload[sb_field] = vals
                    else:
                        payload[sb_field] = []
                
                # parent_lo_code (nullable)
                p_code = r.get("parent_lo_code", "").strip()
                if p_code and p_code.upper() != "NULL":
                    payload["parent_lo_code"] = p_code
                
                # metadata as JSON object
                meta = {}
                assessment = r.get("assessment_approach", "").strip()
                if assessment:
                    meta["assessment_approach"] = assessment
                sequence = r.get("sequence_order", "").strip()
                if sequence:
                    meta["sequence_order"] = sequence
                meta_val = r.get("metadata", "").strip()
                if meta_val:
                    try:
                        extra = json.loads(meta_val)
                        meta.update(extra)
                    except:
                        meta["extra"] = meta_val
                if meta:
                    payload["metadata"] = meta
                
                # Ensure required array fields exist
                for field in ["bloom_level_codes", "context_codes", "keywords", "concept_codes", 
                              "topic_codes", "category_codes", "subject_codes", "field_codes", 
                              "cs2023_ka_mapping"]:
                    if field not in payload:
                        payload[field] = []

            elif table_name == "keywords":
                # Keywords table has minimal schema: code, name, description, metadata, concept_codes
                payload = {
                    "code": code,
                    "name": r.get("name", "").strip(),
                    "description": r.get("description", "").strip(),
                }
                # Handle metadata if present
                meta_val = r.get("metadata", "").strip()
                if meta_val:
                    try:
                        payload["metadata"] = json.loads(meta_val)
                    except:
                        payload["metadata"] = {"raw": meta_val}

                # Handle concept_codes array
                concept_codes = r.get("concept_codes", "").strip()
                if concept_codes:
                    payload["concept_codes"] = [c.strip() for c in concept_codes.replace(";", ",").split(",") if c.strip()]

            else:
                # For other tables (fields, subjects, categories, topics, concepts)
                # Direct column mapping - only include columns that exist in both TSV and Supabase
                payload = {}
                direct_fields = [
                    "name", "description", "keywords", "cs2023_ka_mapping", "metadata",
                    "field_codes", "subject_codes", "category_codes", "topic_codes", "prerequisite_concept_codes"
                ]
                for col in direct_fields:
                    val = r.get(col, "").strip()
                    if val:
                        if col in array_fields:
                            vals = [v.strip() for v in val.replace(";", ",").split(",") if v.strip()]
                            payload[col] = vals
                        else:
                            payload[col] = val

                payload["code"] = code

            try:
                if code in code_to_id:
                    supabase.table(table_name).update(payload).eq("code", code).execute()
                    updated_count += 1
                else:
                    res = supabase.table(table_name).insert(payload).execute()
                    if res.data:
                        code_to_id[code] = res.data[0]["id"]
                    inserted_count += 1
            except Exception as e:
                print(f"  ⚠️  Failed to sync {table_name}/{code}: {e}", file=sys.stderr)

            synced_count += 1

        print(f"  • {table_name:<20}: {synced_count} synced (Updated {updated_count}, Inserted {inserted_count})")

    print(f"==================================================")
    print(f"🎉 DEPENDENCY-AWARE SYNC COMPLETED FOR '{slug}'!")
    print(f"==================================================")


def load_status(repo_root: Path) -> dict:
    status_file = repo_root / "status.yaml"
    if status_file.is_file():
        with open(status_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def main():
    parser = argparse.ArgumentParser(description="Sync project TSV files to Supabase database with dependency ordering")
    parser.add_argument("--project", help="Project slug (default: from status.yaml)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())

    slug = args.project
    if not slug:
        status = load_status(repo_root)
        slug = status.get("active_project")
        if not slug:
            print("❌ Error: Không có project. Truyền --project hoặc set active_project trong status.yaml.")
            sys.exit(1)

    sync_project_to_supabase(slug, repo_root)


if __name__ == "__main__":
    main()