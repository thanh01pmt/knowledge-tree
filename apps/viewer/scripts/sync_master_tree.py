#!/usr/bin/env python3
"""
Sync Master Tree TSV + Keywords TSV → Viewer JSON
Run after any Master Tree update to keep the 3D viewer data fresh.
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

# Paths
TSV_PATH = Path(__file__).parent.parent.parent.parent / "services/python-api/general-context/mlo-knowlege-tree.tsv"
KEYWORDS_TSV_PATH = Path(__file__).parent.parent.parent.parent / "services/python-api/general-context/keywords.tsv"
OUTPUT_PATH = Path(__file__).parent.parent / "src/data/master_tree.json"

def parse_master_tsv():
    """Parse the master TSV into structured data."""
    with open(TSV_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sections = {}
    current_section = None
    headers = None
    
    for line in lines:
        line = line.rstrip('\n')
        
        if line.startswith('Bảng ') or line.startswith('# Table:'):
            current_section = line
            sections[current_section] = []
            headers = None
            continue
            
        if current_section and line.startswith('code\t'):
            headers = line.split('\t')
            continue
            
        if current_section and line.strip() and not line.startswith('#') and headers:
            values = line.split('\t')
            if len(values) == len(headers):
                sections[current_section].append(dict(zip(headers, values)))
    
    table_map = {
        'Bảng 1: Lĩnh vực': 'fields',
        'Bảng 2: Chủ đề': 'subjects',
        'Bảng 3: Danh mục': 'categories',
        'Bảng 4: Chủ đề': 'topics',
        'Bảng 5: Khái niệm': 'concepts',
    }
    
    result = {}
    for viet_name, eng_name in table_map.items():
        result[eng_name] = sections.get(viet_name, [])
    
    return result

def parse_keywords():
    """Parse keywords TSV."""
    with open(KEYWORDS_TSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return list(reader)

def parse_metadata(metadata_str):
    """Parse metadata JSON string safely."""
    if not metadata_str:
        return {}
    try:
        return json.loads(metadata_str)
    except:
        return {}

def build_master_tree():
    """Build the complete master tree JSON for the viewer."""
    print("📖 Parsing Master Tree TSV...")
    tables = parse_master_tsv()
    
    print("🔑 Parsing Keywords TSV...")
    keywords = parse_keywords()
    
    # Build keyword index by concept
    keyword_by_concept = defaultdict(list)
    for kw in keywords:
        try:
            concept_codes = json.loads(kw['concept_codes']) if kw['concept_codes'] else []
        except:
            concept_codes = []
        kw_obj = {
            'code': kw['code'],
            'name': kw['name'],
            'description': kw['description'],
            'metadata': parse_metadata(kw['metadata']),
        }
        for cc in concept_codes:
            keyword_by_concept[cc].append(kw_obj)
    
    # Attach keywords to concepts
    for concept in tables['concepts']:
        cc = concept['code']
        concept['keywords'] = keyword_by_concept.get(cc, [])
    
    # Parse metadata for all levels
    for level in ['fields', 'subjects', 'categories', 'topics', 'concepts']:
        for item in tables[level]:
            item['metadata'] = parse_metadata(item.get('metadata', ''))
            # Parse keywords string to array
            kw_raw = item.get('keywords', '')
            if isinstance(kw_raw, str) and kw_raw:
                item['keywords_list'] = [k.strip() for k in kw_raw.split(',') if k.strip()]
            elif isinstance(kw_raw, list):
                item['keywords_list'] = kw_raw
            else:
                item['keywords_list'] = []
    
    # Keywords also get parsed metadata
    for kw in keywords:
        kw['metadata'] = parse_metadata(kw.get('metadata', ''))
    
    # Add keywords array at root level for easy access
    tables['keywords'] = keywords
    
    # Add empty learning_objectives array (populated from project-specific data if needed)
    tables['learning_objectives'] = []
    
    # Add sync metadata
    tables['_sync_metadata'] = {
        'source_tsv': str(TSV_PATH),
        'keywords_tsv': str(KEYWORDS_TSV_PATH),
        'keywords_count': len(keywords),
        'concepts_count': len(tables['concepts']),
        'fields_count': len(tables['fields']),
        'subjects_count': len(tables['subjects']),
        'categories_count': len(tables['categories']),
        'topics_count': len(tables['topics']),
        'concepts_with_keywords': sum(1 for c in tables['concepts'] if c.get('keywords')),
        'total_keyword_links': sum(len(c.get('keywords', [])) for c in tables['concepts']),
    }
    
    # Write output
    print(f"💾 Writing to {OUTPUT_PATH}...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(tables, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Sync complete!")
    print(f"   Fields: {len(tables['fields'])}")
    print(f"   Subjects: {len(tables['subjects'])}")
    print(f"   Categories: {len(tables['categories'])}")
    print(f"   Topics: {len(tables['topics'])}")
    print(f"   Concepts: {len(tables['concepts'])}")
    print(f"   Keywords (root): {len(keywords)}")
    print(f"   Concepts with keywords: {tables['_sync_metadata']['concepts_with_keywords']}")
    print(f"   Total keyword→concept links: {tables['_sync_metadata']['total_keyword_links']}")
    
    return tables

if __name__ == '__main__':
    build_master_tree()