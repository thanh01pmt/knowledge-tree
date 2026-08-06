#!/usr/bin/env python3
"""
Update master_tree_embeddings.json with embeddings for new concepts.

Adds embedding vectors for concepts that exist in the Master Tree TSV but
are missing from the embeddings file. Uses the same model
(paraphrase-multilingual-MiniLM-L12-v2) and text format as the original
generation, so dimensions stay consistent (384).

Usage:
    python scripts/update_embeddings.py \
        --tsv services/python-api/general-context/mlo-knowlege-tree.tsv \
        --embeddings .agents/skills/taxonomy-mapper/resources/master_tree_embeddings.json
"""

import argparse
import json
import re
from pathlib import Path


def parse_concepts_from_tsv(tsv_path: Path) -> dict:
    """Parse concepts section (Bảng 5) from Master Tree TSV."""
    concepts = {}
    in_concepts = False
    headers = None

    with open(tsv_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('Bảng 5:'):
                in_concepts = True
                headers = None
                continue
            if not in_concepts or not line or line.startswith('Bảng'):
                continue
            parts = line.split('\t')
            if headers is None:
                headers = parts
                continue
            row = dict(zip(headers, parts))
            if 'code' in row and row['code']:
                concepts[row['code']] = row
    return concepts


def build_text(node: dict) -> str:
    """Build the same text format used in the original embeddings."""
    parts = [node.get('name', '')]
    if node.get('keywords'):
        parts.append(node['keywords'])
    if node.get('description'):
        parts.append(node['description'])
    return '. '.join(p for p in parts if p)


def main():
    parser = argparse.ArgumentParser(description='Update embeddings for new concepts')
    parser.add_argument('--tsv', type=Path, required=True,
                       help='Path to Master Tree TSV')
    parser.add_argument('--embeddings', type=Path, required=True,
                       help='Path to master_tree_embeddings.json')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be added without writing')
    args = parser.parse_args()

    # Load embeddings file
    with open(args.embeddings, 'r', encoding='utf-8') as f:
        emb_data = json.load(f)

    model_name = emb_data.get('model', 'paraphrase-multilingual-MiniLM-L12-v2')
    existing = {n['code'] for n in emb_data.get('nodes', [])}

    # Parse concepts from TSV
    concepts = parse_concepts_from_tsv(args.tsv)
    missing = {code: data for code, data in concepts.items() if code not in existing}

    print(f"[*] Model: {model_name} | Existing nodes: {len(existing)}")
    print(f"[*] Concepts in TSV: {len(concepts)} | Missing from embeddings: {len(missing)}")

    if not missing:
        print("[✓] No missing concepts — embeddings up to date")
        return 0

    for code in sorted(missing):
        print(f"  - {code}")

    if args.dry_run:
        print("[DRY-RUN] No changes written")
        return 0

    # Load SentenceTransformer
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)

    # Add embeddings for missing concepts
    added = 0
    for code, data in sorted(missing.items()):
        text = build_text(data)
        emb = model.encode(text, normalize_embeddings=True).tolist()
        emb_data['nodes'].append({
            'level': 'concepts',
            'code': code,
            'name': data.get('name', ''),
            'keywords': data.get('keywords', ''),
            'description': data.get('description', ''),
            'text': text,
            'embedding': emb,
        })
        added += 1

    # Write back
    with open(args.embeddings, 'w', encoding='utf-8') as f:
        json.dump(emb_data, f, ensure_ascii=False)

    print(f"[✓] Added {added} embeddings. Total nodes: {len(emb_data['nodes'])}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
