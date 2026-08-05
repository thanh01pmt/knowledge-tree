#!/usr/bin/env python3
"""
STEP 5: Resolve SIOs via cross-tech reuse through CIO bridge

Logic:
1. For each matched CIO from STEP 4
2. Find sibling SIOs (same CIO parent, different tech)
3. Compute keyword similarity
4. Decide: REUSE (same tech) / ADAPT (cross-tech, high similarity) / GENERATE (low similarity)

Reads:
- matched_cios.json (from STEP 4)
- projects/*/output/learning-objectives.tsv

Outputs:
- resolved_sios.json: SIOs to reuse/adapt/generate
"""

import json
import csv
from pathlib import Path
from difflib import SequenceMatcher


def normalize_cio_code(cio_code: str) -> str:
    """
    Normalize CIO code to base form (first 3 parts):
    - Format 1 (master-tree): CIO-LOCAL_VIEW_STATE-01-EXPLAIN_MECHANISM -> CIO-LOCAL_VIEW_STATE-01
    - Format 2 (swift-associate): CIO-USER_CENTERED_DESIGN-01 -> CIO-USER_CENTERED_DESIGN-01
    Always returns CIO-CONCEPT-NUM format.
    """
    parts = cio_code.split('-')
    if len(parts) >= 3:
        # Always keep first 3 parts: CIO-CONCEPT-NUM
        return '-'.join(parts[:3])
    return cio_code


def load_sios_from_projects(projects_dir: Path) -> list:
    """Load all SIOs from project output files."""
    sios = []
    
    for project_dir in projects_dir.glob('*'):
        if not project_dir.is_dir():
            continue
        
        lo_file = project_dir / 'output' / 'learning-objectives.tsv'
        if not lo_file.exists():
            continue
        
        with open(lo_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                if row.get('lo_type') == 'SPECIFIC_IMPL':
                    sios.append({
                        'code': row.get('code'),
                        'name': row.get('name'),
                        'description': row.get('description'),
                        'parent_lo_code': row.get('parent_lo_code'),
                        'project': project_dir.name
                    })
    
    return sios


def extract_tech_from_sio_code(sio_code: str) -> str:
    """Extract tech stack from SIO code (e.g., 'SIO-REACT-LOCAL_VIEW_STATE-01' -> 'REACT')."""
    parts = sio_code.split('-')
    if len(parts) >= 2:
        return parts[1]
    return 'UNKNOWN'


def keyword_similarity(text1: str, text2: str) -> float:
    """Compute keyword similarity with text normalization."""
    import re
    # Normalize: lowercase, replace underscores and hyphens with spaces
    text1_norm = re.sub(r'[_-]', ' ', text1.lower())
    text2_norm = re.sub(r'[_-]', ' ', text2.lower())
    
    words1 = set(text1_norm.split())
    words2 = set(text2_norm.split())
    
    intersection = words1 & words2
    union = words1 | words2
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)


def resolve_sios_for_cio(cio_code: str, target_tech: str, all_sios: list) -> dict:
    """Resolve SIOs for a given CIO and target tech stack."""
    # Normalize CIO code to handle different formats
    normalized_cio = normalize_cio_code(cio_code)
    
    # Find sibling SIOs
    siblings = []
    for sio in all_sios:
        sio_parent = sio.get('parent_lo_code', '')
        normalized_parent = normalize_cio_code(sio_parent)
        
        if normalized_parent == normalized_cio:
            siblings.append(sio)
    
    if not siblings:
        return {
            'cio_code': cio_code,
            'normalized_cio': normalized_cio,
            'action': 'GENERATE',
            'reason': 'No sibling SIOs found',
            'siblings_count': 0
        }
    
    # Group by tech
    by_tech = {}
    for sio in siblings:
        tech = extract_tech_from_sio_code(sio['code'])
        if tech not in by_tech:
            by_tech[tech] = []
        by_tech[tech].append(sio)
    
    # Check if target tech exists
    if target_tech in by_tech:
        return {
            'cio_code': cio_code,
            'normalized_cio': normalized_cio,
            'action': 'REUSE',
            'sios': by_tech[target_tech],
            'tech': target_tech,
            'siblings_count': len(siblings)
        }
    
    # Find best cross-tech match
    # Prioritize ADAPT over GENERATE when cross-tech siblings exist
    best_match = None
    best_score = 0.0
    
    # Extract concept name from normalized_cio for better similarity
    concept_name = normalized_cio.split('-')[1] if '-' in normalized_cio else normalized_cio
    
    for tech, tech_sios in by_tech.items():
        if tech == target_tech:
            continue  # Skip target tech (already handled above)
        for sio in tech_sios:
            # Compare concept name with SIO name for better matching
            score = keyword_similarity(concept_name, sio['name'])
            if score > best_score:
                best_score = score
                best_match = {'sio': sio, 'tech': tech, 'score': score}
    
    # If any cross-tech sibling exists, prefer ADAPT over GENERATE
    # Lower threshold from 0.6 to 0.1 to favor adaptation
    if best_match and best_score >= 0.1:
        return {
            'cio_code': cio_code,
            'normalized_cio': normalized_cio,
            'action': 'ADAPT',
            'source_sio': best_match['sio'],
            'source_tech': best_match['tech'],
            'target_tech': target_tech,
            'similarity': best_score,
            'siblings_count': len(siblings)
        }
        if best_score >= 0.6:
            return {
                'cio_code': cio_code,
                'normalized_cio': normalized_cio,
                'action': 'ADAPT',
                'source_sio': best_match['sio'],
                'source_tech': best_match['tech'],
                'target_tech': target_tech,
                'similarity': best_score,
                'siblings_count': len(siblings)
            }
        elif best_score >= 0.3:
            return {
                'cio_code': cio_code,
                'normalized_cio': normalized_cio,
                'action': 'TEMPLATE',
                'source_sio': best_match['sio'],
                'source_tech': best_match['tech'],
                'target_tech': target_tech,
                'similarity': best_score,
                'siblings_count': len(siblings)
            }
    
    return {
        'cio_code': cio_code,
        'normalized_cio': normalized_cio,
        'action': 'GENERATE',
        'reason': f'Low similarity with siblings (best: {best_score:.2f})',
        'siblings_count': len(siblings),
        'available_techs': list(by_tech.keys())
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='STEP 5: Resolve SIOs via cross-tech reuse through CIO bridge')
    parser.add_argument('--matched-cios', type=Path, default=Path('/tmp/matched_cios.json'),
                       help='Path to matched_cios.json from STEP 4')
    parser.add_argument('--target-tech', type=str, default='SWIFT',
                       help='Target tech stack (e.g., SWIFT, PYTHON, REACT)')
    parser.add_argument('--projects-dir', type=Path, default=Path('projects'),
                       help='Directory containing project outputs')
    parser.add_argument('--output', type=Path, default=Path('/tmp/resolved_sios.json'),
                       help='Output resolved_sios.json path')
    args = parser.parse_args()

    # Load inputs
    matched_cios_path = args.matched_cios
    
    with open(matched_cios_path) as f:
        matched_cios = json.load(f)
    
    # Target tech stack
    target_tech = args.target_tech.upper()
    
    # Load all SIOs from projects
    projects_dir = args.projects_dir
    all_sios = load_sios_from_projects(projects_dir)
    
    print(f"[*] Found {len(all_sios)} SIOs in projects")
    print(f"[*] Target tech: {target_tech}")
    
    # Resolve SIOs for each matched CIO
    resolved = []
    
    for match in matched_cios.get('matched_cios', []):
        cio_code = match['cio_code']
        concept_code = match['concept_code']
        
        print(f"\n[*] Resolving SIOs for {cio_code}...")
        
        result = resolve_sios_for_cio(cio_code, target_tech, all_sios)
        result['concept_code'] = concept_code
        
        if result['action'] == 'REUSE':
            print(f"  ✓ REUSE: {len(result['sios'])} SIOs from {result['tech']}")
        elif result['action'] == 'ADAPT':
            print(f"  → ADAPT from {result['source_tech']} (similarity: {result['similarity']:.2f})")
        elif result['action'] == 'TEMPLATE':
            print(f"  → TEMPLATE from {result['source_tech']} (similarity: {result['similarity']:.2f})")
        else:
            reason = result.get('reason', 'N/A')
            siblings = result.get('siblings_count', 0)
            print(f"  ✗ GENERATE: {reason} (siblings: {siblings})")
        
        resolved.append(result)
    
    # Summary
    actions = {}
    for r in resolved:
        action = r['action']
        actions[action] = actions.get(action, 0) + 1
    
    print(f"\n[*] Summary:")
    for action, count in sorted(actions.items()):
        print(f"  {action}: {count}")
    
    # Save output
    output = {
        'resolved_sios': resolved,
        'summary': {
            'total_cios': len(resolved),
            'actions': actions,
            'target_tech': target_tech
        }
    }
    
    output_path = args.output
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Saved to {output_path}")


if __name__ == '__main__':
    main()
