#!/usr/bin/env python3
"""
STEP 5.5: JIT generation — generate ULO/CIO/SIO for concepts without coverage.

When a concept resolves (STEP 3) but has no CIO/SIO in the Master Tree or
existing projects (Gap D), this script generates the missing LO chain:

  ULO (UNIVERSAL)      — from concept description (tech-agnostic)
  CIO (CONCEPTUAL_IMPL) — from concept description + Bloom level
  SIO (SPECIFIC_IMPL)   — from project keywords + concept (tech-specific)

Generated LOs go to quarantine for Agent-as-Judge review before staging.

Reads:
- resolved_concepts.json (from STEP 3)
- matched_cios.json (from STEP 4)
- resolved_sios.json (from STEP 5)
- keywords.json (from STEP 1-2, for SIO context)

Outputs:
- jit_los.json: {generated: [ULO/CIO/SIO entries], concepts_covered: [...]}
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_covered_concepts(matched_cios: dict, resolved_sios: dict) -> set:
    """Concepts that already have CIO/SIO coverage."""
    covered = set()
    for match in matched_cios.get('matched_cios', []):
        covered.add(match.get('concept_code', ''))
    for group in resolved_sios.get('resolved_sios', []):
        covered.add(group.get('concept_code', ''))
    return {c for c in covered if c}


def collect_resolved_concepts(resolved_concepts: dict) -> Dict[str, dict]:
    """Map concept_code -> concept info from resolved_concepts.json."""
    concepts = {}
    for item in resolved_concepts.get('resolved', []):
        for code in item.get('concept_codes', []):
            if code:
                concepts[code] = {
                    'keyword': item.get('keyword', ''),
                    'matches': item.get('matches', []),
                }
    return concepts


def get_concept_description(concept_code: str, reuse_inventory: dict) -> str:
    """Get concept description from master tree."""
    concepts = reuse_inventory.get('master_tree', {}).get('concepts', {})
    data = concepts.get(concept_code, {})
    return data.get('description', '')


def generate_ulo(concept_code: str, description: str) -> dict:
    """Generate ULO (UNIVERSAL tier) from concept description."""
    return {
        'code': f"ULO-{concept_code}-01",
        'name': f"Understand {concept_code}",
        'description': (
            f"Người học có khả năng hiểu nguyên lý phổ quát của {concept_code}: "
            f"{description[:200] if description else 'khái niệm và vai trò trong thiết kế giải pháp phần mềm.'}"
        ),
        'lo_type': 'UNIVERSAL',
        'parent_lo_code': '',
        'concept_codes': [concept_code],
        'bloom_level': 'UNDERSTAND',
        'knowledge_dimension': 'CONCEPTUAL',
        'assessment_approach': 'concept-check',
    }


def generate_cio(concept_code: str, description: str) -> dict:
    """Generate CIO (CONCEPTUAL_IMPL tier) from concept description."""
    return {
        'code': f"CIO-{concept_code}-01",
        'name': f"Apply {concept_code} Concepts",
        'description': (
            f"Người học có khả năng thiết kế quy trình xử lý cho {concept_code}: "
            f"{description[:200] if description else 'phân tích yêu cầu, lựa chọn phương pháp, và đánh giá kết quả.'}"
        ),
        'lo_type': 'CONCEPTUAL_IMPL',
        'parent_lo_code': f"ULO-{concept_code}-01",
        'concept_codes': [concept_code],
        'bloom_level': 'APPLY',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-lab',
    }


def generate_sio(concept_code: str, description: str, keywords: List[str], target_tech: str) -> dict:
    """Generate SIO (SPECIFIC_IMPL tier) from concept + project keywords."""
    # Pick relevant keywords as context (exclude the concept code itself)
    context = [k for k in keywords if k.lower() not in concept_code.lower()][:3]
    context_str = ', '.join(context) if context else 'project context'

    return {
        'code': f"SIO-{target_tech}-{concept_code}-01",
        'name': f"{target_tech}: Implement {concept_code}",
        'description': (
            f"Người học có khả năng triển khai {concept_code} trong {target_tech} "
            f"cho {context_str}: {description[:150] if description else 'viết code, xử lý lỗi, và kiểm thử.'}"
        ),
        'lo_type': 'SPECIFIC_IMPL',
        'parent_lo_code': f"CIO-{concept_code}-01",
        'concept_codes': [concept_code],
        'bloom_level': 'APPLY',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-review',
    }


def main():
    parser = argparse.ArgumentParser(description='STEP 5.5: JIT generate LOs for uncovered concepts')
    parser.add_argument('--resolved-concepts', type=Path, required=True)
    parser.add_argument('--matched-cios', type=Path, required=True)
    parser.add_argument('--resolved-sios', type=Path, required=True)
    parser.add_argument('--keywords', type=Path, required=True)
    parser.add_argument('--reuse-inventory', type=Path, required=True)
    parser.add_argument('--target-tech', type=str, default='SWIFT')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    resolved_concepts = load_json(args.resolved_concepts)
    matched_cios = load_json(args.matched_cios)
    resolved_sios = load_json(args.resolved_sios)
    keywords_data = load_json(args.keywords)
    inventory = load_json(args.reuse_inventory)

    # Concepts already covered
    covered = collect_covered_concepts(matched_cios, resolved_sios)
    # Concepts resolved from STEP 3
    resolved = collect_resolved_concepts(resolved_concepts)

    # Concepts needing JIT generation
    uncovered = {c: info for c, info in resolved.items() if c not in covered}
    print(f"[*] Resolved concepts: {len(resolved)} | Covered: {len(covered)} | Uncovered: {len(uncovered)}")

    if not uncovered:
        print("[✓] All resolved concepts have coverage — no JIT generation needed")
        output = {'generated': [], 'concepts_covered': sorted(covered)}
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        return 0

    # Collect project keywords for SIO context
    keywords = [k.get('keyword', '') for k in keywords_data.get('keywords', [])]

    generated = []
    for concept_code, info in sorted(uncovered.items()):
        description = get_concept_description(concept_code, inventory)
        print(f"  → Generating LOs for {concept_code}")

        ulo = generate_ulo(concept_code, description)
        cio = generate_cio(concept_code, description)
        sio = generate_sio(concept_code, description, keywords, args.target_tech)

        generated.extend([ulo, cio, sio])

    print(f"[*] Generated {len(generated)} LOs ({len(uncovered)} concepts × 3 tiers)")

    output = {
        'generated': generated,
        'concepts_covered': sorted(covered),
        'concepts_generated': sorted(uncovered.keys()),
        'summary': {
            'generated_count': len(generated),
            'concepts_generated': len(uncovered),
            'target_tech': args.target_tech,
        }
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {args.output}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
