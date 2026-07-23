#!/usr/bin/env python3
"""
sync_back_master.py — Reverse Sync approved Staging Knowledge Tree back to Official Master Tree in skill resources.
Re-generates master_tree.json and bumps release version history.
"""

import sys
import shutil
import json
import re
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
STAGING_TSV_PATH = PROJECT_ROOT / "general-context" / "mlo-knowlege-tree.tsv"
MASTER_TSV_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
MASTER_JSON_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/master_tree.json"
VERSION_HISTORY_PATH = PROJECT_ROOT / "general-context" / "version_history.json"

def parse_tsv_to_master_json(tsv_path: Path) -> dict:
    """Parse TSV file into JSON format expected by master_tree.json"""
    data = {
        "fields": [],
        "subjects": [],
        "categories": [],
        "topics": [],
        "concepts": []
    }

    current_section = None
    with open(tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("Bảng 1"):
                current_section = "fields"
                continue
            elif line_str.startswith("Bảng 2"):
                current_section = "subjects"
                continue
            elif line_str.startswith("Bảng 3"):
                current_section = "categories"
                continue
            elif line_str.startswith("Bảng 4"):
                current_section = "topics"
                continue
            elif line_str.startswith("Bảng 5"):
                current_section = "concepts"
                continue

            if line_str.startswith("Đây là") or line_str.startswith("Mỗi Field") or line_str.startswith("code\t"):
                continue

            parts = line.rstrip("\r\n").split("\t")
            if len(parts) >= 2:
                code = parts[0].strip()
                name = parts[1].strip()
                desc = parts[2].strip() if len(parts) > 2 else ""
                
                item = {
                    "code": code,
                    "name": name,
                    "description": desc
                }
                if len(parts) > 3:
                    raw_parents = parts[3].strip()
                    item["parent_or_relation"] = raw_parents
                    item["parent_codes"] = [p.strip() for p in raw_parents.split(",") if p.strip()]
                if len(parts) > 4:
                    item["keywords"] = parts[4].strip()
                if len(parts) > 6:
                    item["metadata"] = parts[6].strip()

                if current_section in data:
                    data[current_section].append(item)


    return data

def main():
    if not STAGING_TSV_PATH.exists():
        print(f"❌ Staging TSV not found at {STAGING_TSV_PATH}")
        sys.exit(1)

    print(f"🔄 Syncing Staging copy back to Official Master Tree resource...")
    MASTER_TSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(STAGING_TSV_PATH, MASTER_TSV_PATH)
    print(f"✅ Updated Official Master TSV: {MASTER_TSV_PATH}")

    # Regenerate master_tree.json
    master_json_data = parse_tsv_to_master_json(STAGING_TSV_PATH)
    MASTER_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(master_json_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Regenerated Master JSON: {MASTER_JSON_PATH}")

    # Update version history
    if VERSION_HISTORY_PATH.exists():
        with open(VERSION_HISTORY_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)

        old_ver = history.get("current_version", "v2.2.0")
        ver_match = re.search(r"v(\d+)\.(\d+)\.(\d+)", old_ver)
        if ver_match:
            major, minor, patch = map(int, ver_match.groups())
            new_ver = f"v{major}.{minor + 1}.0"
        else:
            new_ver = "v2.3.0"

        history["current_version"] = new_ver
        history["base_master_version"] = new_ver
        history["last_updated"] = datetime.now().isoformat()
        history["versions"].append({
            "version": new_ver,
            "timestamp": datetime.now().isoformat(),
            "description": f"Approved reverse sync from general-context staging to official Master Knowledge Tree {new_ver}"
        })

        with open(VERSION_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"✅ Bumped Master Version to {new_ver} in {VERSION_HISTORY_PATH}")

    print("\n🎉 Reverse Sync Completed Successfully!")

if __name__ == "__main__":
    main()
