#!/usr/bin/env python3
"""Fix missing cs2023_ka_mapping and metadata for concepts created by ATE pipeline."""
import csv
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


import argparse

FIX_MAP = {
    "UI_MODIFIERS_CONCEPT": {
        "cs2023_ka_mapping": "HCI",
        "metadata": '{"icon": "paint-brush"}',
    },
    "PROJECT_ASSETS_MANAGEMENT": {
        "cs2023_ka_mapping": "SDF",
        "metadata": '{"icon": "folder-open"}',
    },
    "UI_BOX_MODEL_LAYOUT": {
        "cs2023_ka_mapping": "HCI, GIT",
        "metadata": '{"icon": "code"}',
    },
    "STATE_PROPERTY_WRAPPER": {
        "cs2023_ka_mapping": "HCI, SDF",
        "metadata": '{"icon": "dot-circle"}',
    },
    "DECLARATIVE_UI_PARADIGM": {
        "cs2023_ka_mapping": "HCI, FPL",
        "metadata": '{"icon": "code"}',
    },
    "SYNTAX_VS_RUNTIME_ERRORS": {
        "cs2023_ka_mapping": "SDF, SE",
        "metadata": '{"icon": "exclamation-triangle"}',
    },
    "FLEXBOX_GRID_LAYOUT": {
        "cs2023_ka_mapping": "HCI, GIT",
        "metadata": '{"icon": "code"}',
    },
    "CROSS_ORIGIN_SECURITY": {
        "cs2023_ka_mapping": "SEC",
        "metadata": '{"icon": "code"}',
    },
}

def main():
    parser = argparse.ArgumentParser(description="Fix cs2023_ka_mapping and metadata")
    parser.add_argument("--project", default="swift-associate", help="Project slug")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    concepts_tsv = repo_root / "projects" / args.project / "output" / "concepts.tsv"
    if not concepts_tsv.is_file():
        print(f"⚠️ {concepts_tsv} not found, skipping...")
        return

    rows = []
    with open(concepts_tsv, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        for row in reader:
            code = row.get("code", "").strip()
            if code in FIX_MAP:
                fix = FIX_MAP[code]
                if not row.get("cs2023_ka_mapping", "").strip():
                    row["cs2023_ka_mapping"] = fix["cs2023_ka_mapping"]
                if not row.get("metadata", "").strip():
                    row["metadata"] = fix["metadata"]
            rows.append(row)

    with open(concepts_tsv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Fixed cs2023_ka_mapping and metadata for ATE-created concepts in {args.project}")


if __name__ == "__main__":
    main()
