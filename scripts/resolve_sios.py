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




# Tech-specific keywords — nếu SIO mô tả chứa, không ADAPT được sang tech khác
_FOREIGN_TECH_KEYWORDS = [
    'mypy', 'pyright', 'ruff', 'pylint', 'flake8', 'black', 'isort',  # Python tooling
    'pip', 'pypi', 'poetry', 'venv', 'virtualenv',  # Python packaging
    'cmmi', 'iso 42001', 'iso42001', 'nis ', 'threat modeling',  # Rác governance
    'governance framework', 'compliance', 'policy and', 'risk assessment', 'maturity',  # Rác governance
    'numpy', 'pandas', 'requests', 'fastapi', 'flask', 'django',  # Python libs
    'react', 'vue', 'angular', 'jsx', 'tsx',  # JS frameworks
    'npm', 'yarn', 'pnpm', 'node_modules',  # JS packaging
]


def _contains_foreign_tech_keywords(sio: dict, target_tech: str) -> bool:
    """Check if SIO description contains tech-specific keywords of OTHER techs.

    If yes, cannot safely 'adapt' keyword to target tech — must GENERATE new.
    """
    desc = (sio.get('description', '') or '').lower()
    name = (sio.get('name', '') or '').lower()
    text = desc + ' ' + name
    for kw in _FOREIGN_TECH_KEYWORDS:
        if kw in text:
            return True
    return False

def resolve_sios_for_cio(cio_code: str, target_tech: str, all_sios: list) -> dict:
    """Resolve SIOs for a given CIO and target tech stack.

    ADR: BỎ REUSE/ADAPT cross-project (GENERATE-first).
    Master Tree SIOs sinh từ project khác (stream-chat-swift, swift-associate...)
    — 'generic Swift SIOs' không gắn keyword dự án đích (VD forEach không có
    trong smart-bulb-controller). Reuse dễ lỗi → luôn GENERATE, JIT sinh SIO
    gắn keyword thật của project, sau đó đánh giá loại/cập nhật.
    """
    # Normalize CIO code to handle different formats
    normalized_cio = normalize_cio_code(cio_code)
    
    # ADR (GENERATE-first): không REUSE/ADAPT SIO cross-project — JIT sinh mới
    # gắn keyword thật của dự án. Tránh SIO 'generic Swift' (forEach, stride...)
    # không tồn tại trong code dự án đích.
    return {
        'cio_code': cio_code,
        'normalized_cio': normalized_cio,
        'action': 'GENERATE',
        'reason': 'GENERATE-first (ADR): bỏ REUSE cross-project, JIT sinh SIO gắn keyword dự án',
        'siblings_count': 0
    }
    

def _goal_tokens(goal: str) -> set:
    """Extract meaningful tokens from the user goal."""
    import re
    tokens = set()
    for word in re.findall(r'[a-zA-Z0-9]+', goal.lower()):
        if word not in _DOMAIN_STOPWORDS and len(word) > 2:
            tokens.add(word)
    return tokens


def _sio_domain_score(sio: dict, goal_tokens: set) -> float:
    """Score how relevant an SIO is to the user goal.

    Overlap ratio between SIO description tokens and goal tokens.
    Returns 0.0 if no overlap (generic SIO unrelated to the project).
    """
    if not goal_tokens:
        return 1.0  # no goal -> keep all
    import re
    desc = (sio.get('name', '') + ' ' + sio.get('description', '')).lower()
    desc_tokens = set(re.findall(r'[a-zA-Z0-9]+', desc))
    overlap = desc_tokens & goal_tokens
    return len(overlap) / len(goal_tokens)


def filter_sios_by_domain(sio_list: list, goal_tokens: set, min_score: float = 0.0) -> list:
    """Annotate SIOs with domain relevance score.

    Keeps all SIOs (min_score=0) but tags each with domain_score so the
    roadmap can surface relevance. SIOs with score 0 are generic (e.g.
    'plugin system', 'DI container') and may be de-prioritized downstream.
    """
    kept = []
    for sio in sio_list:
        sio = dict(sio)
        sio['domain_score'] = round(_sio_domain_score(sio, goal_tokens), 3)
        kept.append(sio)
    return kept


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
    parser.add_argument('--goal', type=str, default='',
                       help='User learning goal (for domain relevance filtering)')
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
            # Annotate SIOs with domain relevance to the user goal
            goal_tokens = _goal_tokens(args.goal)
            result['sios'] = filter_sios_by_domain(result['sios'], goal_tokens)
            result['siblings_count'] = len(result['sios'])
            print(f"  ✓ REUSE: {len(result['sios'])} SIOs from {result['tech']} "
                  f"(domain-annotated)")
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
