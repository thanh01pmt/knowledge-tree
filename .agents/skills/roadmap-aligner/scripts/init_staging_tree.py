#!/usr/bin/env python3
"""
init_staging_tree.py — Initialize staging working copy of Master Knowledge Tree in general-context/
"""

import shutil
import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent

def find_project_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
    return start.resolve().parent.parent.parent.parent

PROJECT_ROOT = find_project_root(SCRIPT_DIR)
MASTER_TSV_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
STAGING_DIR = PROJECT_ROOT / "general-context"
STAGING_TSV_PATH = STAGING_DIR / "mlo-knowlege-tree.tsv"
VERSION_HISTORY_PATH = STAGING_DIR / "version_history.json"

def main():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    if not MASTER_TSV_PATH.exists():
        print(f"❌ Original Master TSV not found at {MASTER_TSV_PATH}")
        return

    # Copy master TSV to staging working copy if missing or requested
    shutil.copy2(MASTER_TSV_PATH, STAGING_TSV_PATH)
    print(f"✅ Copied Master Tree TSV to Staging: {STAGING_TSV_PATH}")

    # Initialize version history if not present
    if not VERSION_HISTORY_PATH.exists():
        history = {
            "current_version": "v2.2.0-staging.0",
            "base_master_version": "v2.2.0",
            "last_updated": datetime.now().isoformat(),
            "versions": [
                {
                    "version": "v2.2.0-staging.0",
                    "timestamp": datetime.now().isoformat(),
                    "description": "Initialized staging working copy from Master Knowledge Tree v2.2.0"
                }
            ]
        }
        with open(VERSION_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"✅ Initialized version history at {VERSION_HISTORY_PATH}")
    else:
        print(f"ℹ️ Version history already exists at {VERSION_HISTORY_PATH}")

if __name__ == "__main__":
    main()
