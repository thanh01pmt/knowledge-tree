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


def sync_to_supabase(supabase: Client, rows: List[Dict], lo_type: str, dry_run: bool = False) -> int:
    """Sync rows to Supabase learning_objectives table.
    
    Returns number of rows upserted.
    """
    if not rows:
        print(f"[SKIP] No {lo_type} to sync")
        return 0
    
    if dry_run:
        print(f"[DRY-RUN] Would sync {len(rows)} {lo_type} to Supabase")
        return len(rows)
    
    # Upsert rows (update on conflict by code)
    try:
        result = supabase.table('learning_objectives').upsert(
            rows,
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
