#!/usr/bin/env python3
"""
parse_master_tree.py — Parse Master TSV into JSON for taxonomy-mapper.

Delegates to shared master_tree_parser.py (tree-validator) to avoid code duplication.
"""
import json
import argparse
from pathlib import Path

# Import shared parser from tree-validator
import sys
_script_dir = Path(__file__).resolve().parent
_validator_dir = _script_dir.parent.parent / "tree-validator" / "scripts"
if _validator_dir.is_dir() and str(_validator_dir) not in sys.path:
    sys.path.insert(0, str(_validator_dir))

from master_tree_parser import parse_master_tsv, find_repo_root, get_default_master_tsv_path


def main():
    repo_root = find_repo_root(Path.cwd())
    parser = argparse.ArgumentParser(description="Parse Master TSV into JSON")
    parser.add_argument('--input', type=str, default=str(
        repo_root / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
    ))
    parser.add_argument('--output', type=str, default=str(
        repo_root / ".agents/skills/taxonomy-mapper/resources/master_tree.json"
    ))
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    data = parse_master_tsv(Path(args.input))

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully parsed Master TSV and saved to {args.output}")
    print("Node counts:")
    for k, v in data.items():
        print(f"  {k}: {len(v)}")


if __name__ == "__main__":
    main()
