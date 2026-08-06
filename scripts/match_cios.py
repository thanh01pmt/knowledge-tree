#!/usr/bin/env python3
"""
STEP 4: Match resolved concepts to CIOs from Master Tree and Projects

Reads:
- resolved_concepts.json (from STEP 3)
- reuse_inventory.json (from STEP 0)
- projects/*/output/learning-objectives.tsv

Outputs:
- matched_cios.json: List of CIOs that match resolved concepts
"""

import json
import csv
from pathlib import Path

def load_cios_from_projects(projects_dir: Path) -> dict:
    """Load all CIOs from project output files."""
    cios = {}
    
    for project_dir in projects_dir.glob('*'):
        if not project_dir.is_dir():
            continue
            
        lo_file = project_dir / 'output' / 'learning-objectives.tsv'
        if not lo_file.exists():
            continue
            
        with open(lo_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                if row.get('lo_type') == 'CONCEPTUAL_IMPL':
                    code = row.get('code')
                    if code:
                        cios[code] = {
                            'code': code,
                            'name': row.get('name', ''),
                            'description': row.get('description', ''),
                            'bloom_level': row.get('bloom_level', ''),
                            'knowledge_dimension': row.get('knowledge_dimension', ''),
                            'concept_codes': row.get('concept_codes', ''),
                            'project': project_dir.name,
                        }
    
    return cios

def derive_ulos(matched_cios: list) -> list:
    """Derive ULO (Universal Learning Objective) codes from matched CIOs.

    Each matched concept gets a ULO at the UNIVERSAL tier:
      - code: ULO-<CONCEPT>-01
      - lo_type: UNIVERSAL
      - concept_codes: [CONCEPT]
      - parent_lo_code: (empty — ULO is the top of the derivation chain)
    Deduplicates by concept so each concept yields exactly one ULO.
    """
    seen_concepts = set()
    ulos = []

    for match in matched_cios:
        concept = match.get('concept_code', '')
        if not concept or concept in seen_concepts:
            continue
        seen_concepts.add(concept)

        ulos.append({
            'code': f"ULO-{concept}-01",
            'name': f"Understand {concept}",
            'description': (
                f"Người học có khả năng hiểu nguyên lý phổ quát của {concept} "
                f"và vai trò của nó trong thiết kế giải pháp phần mềm."
            ),
            'lo_type': 'UNIVERSAL',
            'parent_lo_code': '',
            'concept_codes': [concept],
            'bloom_level': 'UNDERSTAND',
            'knowledge_dimension': 'CONCEPTUAL',
            'assessment_approach': 'concept-check',
        })

    return ulos


def main():
    import argparse
    parser = argparse.ArgumentParser(description='STEP 4: Match resolved concepts to CIOs')
    parser.add_argument('--resolved-concepts', type=Path, default=Path('/tmp/resolved_concepts.json'),
                       help='Path to resolved_concepts.json from STEP 3')
    parser.add_argument('--reuse-inventory', type=Path, default=Path('/tmp/reuse_inventory.json'),
                       help='Path to reuse_inventory.json from STEP 0')
    parser.add_argument('--projects-dir', type=Path, default=Path('projects'),
                       help='Directory containing project outputs')
    parser.add_argument('--output', type=Path, default=Path('/tmp/matched_cios.json'),
                       help='Output matched_cios.json path')
    args = parser.parse_args()

    # Load inputs
    resolved_path = args.resolved_concepts
    inventory_path = args.reuse_inventory
    
    with open(resolved_path) as f:
        resolved = json.load(f)
    
    with open(inventory_path) as f:
        inventory = json.load(f)
    
    # Load CIOs from projects
    projects_dir = args.projects_dir
    cios = load_cios_from_projects(projects_dir)
    
    print(f"[*] Found {len(cios)} CIOs in projects")
    
    # Match CIOs to resolved concepts
    matched_cios = []
    reused_cios = []
    
    # Track seen CIO codes to avoid duplicate matches
    seen_matches = set()
    
    for item in resolved.get('resolved', []):
        # Extract concept codes: prefer 'concept_codes' list, fallback to matches[].code
        concept_codes = item.get('concept_codes', [])
        if not concept_codes:
            concept_codes = [m.get('code') for m in item.get('matches', []) if m.get('code')]
        
        keyword = item.get('keyword', '')
        
        for concept_code in concept_codes:
            if not concept_code:
                continue
            
            # Find CIOs that reference this concept in their concept_codes field
            for cio_code, cio_data in cios.items():
                if concept_code in cio_data.get('concept_codes', ''):
                    match_key = (concept_code, cio_code)
                    if match_key in seen_matches:
                        continue
                    seen_matches.add(match_key)
                    
                    match_info = {
                        'keyword': keyword,
                        'concept_code': concept_code,
                        'concept_name': cio_data.get('concept_codes', ''),
                        'cio_code': cio_code,
                        'cio_name': cio_data.get('name', ''),
                        'project': cio_data.get('project', ''),
                    }
                    matched_cios.append(match_info)
                    reused_cios.append(cio_code)
                    print(f"  ✓ {concept_code} → {cio_code} (from {cio_data.get('project')})")
    
    print(f"\n[*] Matched {len(matched_cios)} CIOs to resolved concepts")
    print(f"[*] Reused {len(set(reused_cios))} unique CIOs")

    # Derive ULOs from matched concepts (UNIVERSAL tier)
    derived_ulos = derive_ulos(matched_cios)
    print(f"[*] Derived {len(derived_ulos)} ULOs from matched concepts")

    # Save output
    output = {
        'matched_cios': matched_cios,
        'derived_ulos': derived_ulos,
        'reused_cios': list(set(reused_cios)),
        'summary': {
            'total_matched': len(matched_cios),
            'unique_reused': len(set(reused_cios)),
            'derived_ulo_count': len(derived_ulos),
            'source': 'local_projects'
        }
    }
    
    output_path = args.output
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✓ Saved to {output_path}")

if __name__ == '__main__':
    main()
