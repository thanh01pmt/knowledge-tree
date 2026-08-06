#!/usr/bin/env python3
"""
STEP 7: Sync quarantine TSVs to Supabase Learning Objectives table.

Reads quarantine TSVs (ulos, cios, sios) approved by agent_as_judge,
validates schema, and upserts them into Supabase learning_objectives table.

Usage:
    python scripts/apply_to_staging.py \
        --quarantine-dir /tmp/quarantine \
        --dry-run

Input:
    - /tmp/quarantine/ulos.tsv
    - /tmp/quarantine/cios.tsv
    - /tmp/quarantine/sios.tsv

Output:
    - Upserts into Supabase learning_objectives table
"""

import os
import sys
import csv
import json
import argparse
from pathlib import Path
from typing import List, Dict

# Suppress urllib3 IPv6 warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

from supabase import create_client, Client


def load_env():
    """Load Supabase credentials from .env file."""
    env_path = Path('.env')
    if not env_path.exists():
        print("[ERROR] .env file not found")
        sys.exit(1)
    
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


def load_quarantine_tsv(file_path: Path) -> List[Dict]:
    """Load TSV file into list of dictionaries."""
    if not file_path.exists():
        print(f"[WARN] File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return list(reader)


def validate_schema(rows: List[Dict], required_fields: List[str], lo_type: str) -> bool:
    """Validate that all rows have required fields."""
    if not rows:
        return True
    
    for i, row in enumerate(rows):
        for field in required_fields:
            if field not in row or not row[field]:
                print(f"[ERROR] {lo_type} row {i} missing field '{field}'")
                return False
    return True


def _map_lo_to_supabase(row: Dict) -> Dict:
    """Map a TSV learning-objective row to the Supabase schema.

    Supabase learning_objectives columns (from live schema):
      code, name, description, lo_type, parent_lo_code,
      bloom_level_codes[], context_codes[], keywords[],
      concept_codes[], topic_codes[], category_codes[],
      subject_codes[], field_codes[], cs2023_ka_mapping[],
      metadata (JSONB), organization_code
    """
    payload = {"organization_code": "DEFAULT_ORG"}

    # Direct string fields
    for field in ("name", "description", "lo_type"):
        val = row.get(field, "").strip()
        if val:
            payload[field] = val

    # code is required
    payload["code"] = row.get("code", "").strip()

    # lo_type default
    if not payload.get("lo_type"):
        payload["lo_type"] = "UNIVERSAL"

    # Array fields (TSV comma/semicolon separated -> Supabase arrays)
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
        val = row.get(tsv_field, "").strip()
        if val:
            vals = [v.strip() for v in val.replace(";", ",").split(",") if v.strip()]
            payload[sb_field] = vals
        else:
            payload[sb_field] = []

    # parent_lo_code (nullable)
    p_code = row.get("parent_lo_code", "").strip()
    if p_code and p_code.upper() != "NULL":
        payload["parent_lo_code"] = p_code

    # metadata as JSON object (assessment_approach, sequence_order, ...)
    meta = {}
    assessment = row.get("assessment_approach", "").strip()
    if assessment:
        meta["assessment_approach"] = assessment
    sequence = row.get("sequence_order", "").strip()
    if sequence:
        meta["sequence_order"] = sequence
    meta_val = row.get("metadata", "").strip()
    if meta_val:
        try:
            extra = json.loads(meta_val)
            meta.update(extra)
        except Exception:
            meta["extra"] = meta_val
    if meta:
        payload["metadata"] = meta

    return payload


def sync_to_supabase(supabase: Client, rows: List[Dict], lo_type: str, dry_run: bool = False) -> int:
    """Sync rows to Supabase learning_objectives table.

    Returns number of rows upserted.
    """
    if not rows:
        print(f"[SKIP] No {lo_type} to sync")
        return 0

    # Map TSV rows to Supabase schema
    payloads = [_map_lo_to_supabase(r) for r in rows]

    if dry_run:
        print(f"[DRY-RUN] Would sync {len(payloads)} {lo_type} to Supabase")
        return len(payloads)

    # Upsert rows (update on conflict by code)
    try:
        result = supabase.table('learning_objectives').upsert(
            payloads,
            on_conflict='code'
        ).execute()

        synced = len(result.data)
        print(f"[SYNC] Upserted {synced} {lo_type} to Supabase")
        return synced
    except Exception as e:
        print(f"[ERROR] Failed to sync {lo_type}: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(description='Sync quarantine TSVs to Supabase')
    parser.add_argument('--quarantine-dir', type=Path, required=True,
                       help='Directory containing quarantine TSVs')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be synced without actually syncing')
    
    args = parser.parse_args()
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SERVICE_ROLE_KEY')
    load_env()
    
    # Initialize Supabase client
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SERVICE_ROLE_KEY')
    
    if not supabase_url or not supabase_key:
        print("[ERROR] SUPABASE_URL or SERVICE_ROLE_KEY not found in .env")
        sys.exit(1)
    
    supabase = create_client(supabase_url, supabase_key)
    
    # Define schema for each LO type
    schemas = {
        'ulos': {
            'required': ['code', 'name', 'description', 'lo_type', 'concept_codes'],
            'file': 'ulos.tsv'
        },
        'cios': {
            'required': ['code', 'name', 'description', 'lo_type', 'parent_lo_code', 'concept_codes'],
            'file': 'cios.tsv'
        },
        'sios': {
            'required': ['code', 'name', 'description', 'lo_type', 'parent_lo_code', 'concept_codes'],
            'file': 'sios.tsv'
        }
    }
    
    # Sync each LO type
    total_synced = 0
    for lo_type, schema in schemas.items():
        file_path = args.quarantine_dir / schema['file']
        rows = load_quarantine_tsv(file_path)
        
        if not rows:
            continue
        
        # Validate schema
        if not validate_schema(rows, schema['required'], lo_type.upper()):
            print(f"[ERROR] Schema validation failed for {lo_type}")
            continue
        
        # Sync to Supabase
        synced = sync_to_supabase(supabase, rows, lo_type.upper(), args.dry_run)
        total_synced += synced
    
    print(f"\n[SUMMARY] Total LOs synced: {total_synced}")
    
    if total_synced > 0 and not args.dry_run:
        print(f"[SUCCESS] Supabase learning_objectives table updated")
        return 0
    elif args.dry_run:
        print(f"[DRY-RUN] No changes made")
        return 0
    else:
        print(f"[INFO] No changes made")
        return 0


if __name__ == '__main__':
    sys.exit(main())
