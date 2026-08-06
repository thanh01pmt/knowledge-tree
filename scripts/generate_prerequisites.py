#!/usr/bin/env python3
"""
STEP 4.5: Generate prerequisite DAG for the resolved roadmap.

Reads:
- matched_cios.json (from STEP 4, includes derived_ulos)
- resolved_sios.json (from STEP 5)
- reuse_inventory.json (from STEP 0, includes master_tree.prerequisites
  and concepts with prerequisite_concept_codes)

Outputs:
- prerequisites.json: list of {learning_objective_code, prerequisite_lo_code,
  source_layer, rationale}

Logic:
1. Reuse existing Master Tree prerequisites that reference resolved LOs.
2. Derive concept-level prerequisites: if concept A requires concept B
   (prerequisite_concept_codes), then every LO of A depends on the ULO of B.
3. Enforce hierarchy: SIO -> CIO -> ULO (a SIO depends on its parent CIO,
   a CIO depends on its parent ULO).
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_resolved_codes(matched_cios: dict, resolved_sios: dict) -> Dict[str, str]:
    """Collect all LO codes in the roadmap with their concept.

    Returns {lo_code: concept_code}.
    """
    codes = {}

    # Derived ULOs
    for ulo in matched_cios.get('derived_ulos', []):
        code = ulo.get('code', '')
        concepts = ulo.get('concept_codes', [])
        if code:
            codes[code] = concepts[0] if concepts else ''

    # Matched CIOs
    for match in matched_cios.get('matched_cios', []):
        cio_code = match.get('cio_code', '')
        concept = match.get('concept_code', '')
        if cio_code:
            codes[cio_code] = concept

    # Resolved SIOs (REUSE 'sios' + ADAPT 'source_sio')
    for group in resolved_sios.get('resolved_sios', []):
        concept = group.get('concept_code', '')
        sio_list = group.get('sios', [])
        if not sio_list and group.get('source_sio'):
            sio_list = [group['source_sio']]
        for sio in sio_list:
            code = sio.get('code', '')
            if code:
                codes[code] = concept

    return codes


def build_concept_prereqs(concepts: dict) -> Dict[str, List[str]]:
    """Build {concept: [prerequisite_concepts]} from master tree concepts."""
    prereqs = {}
    for code, data in concepts.items():
        raw = data.get('prerequisite_concept_codes', '')
        if isinstance(raw, str) and raw.strip():
            prereqs[code] = [c.strip() for c in raw.split(',') if c.strip()]
    return prereqs


def generate_prerequisites(
    matched_cios: dict,
    resolved_sios: dict,
    master_tree: dict,
) -> List[dict]:
    """Generate the prerequisite DAG for the resolved roadmap."""
    lo_to_concept = collect_resolved_codes(matched_cios, resolved_sios)
    all_codes = set(lo_to_concept.keys())

    # Concept-level prerequisites from master tree
    concepts = master_tree.get('concepts', {})
    concept_prereqs = build_concept_prereqs(concepts)

    # Existing master tree prerequisites (reuse those touching our codes)
    existing = master_tree.get('prerequisites', [])
    edges = []
    seen = set()

    def add_edge(target: str, prereq: str, source_layer: str, rationale: str):
        if target == prereq or not target or not prereq:
            return
        key = (target, prereq)
        if key in seen:
            return
        seen.add(key)
        edges.append({
            'learning_objective_code': target,
            'prerequisite_lo_code': prereq,
            'source_layer': source_layer,
            'rationale': rationale,
        })

    # 1. Reuse existing master tree prerequisites
    for p in existing:
        target = p.get('learning_objective_code', '')
        prereq = p.get('prerequisite_lo_code', '')
        if target in all_codes and prereq in all_codes:
            add_edge(target, prereq,
                     p.get('source_layer', 'L3-LLM'),
                     p.get('rationale', 'Reused from Master Tree'))

    # 2. Concept-level prerequisites: LO of A depends on ULO of B
    for lo_code, concept in lo_to_concept.items():
        if not concept:
            continue
        for prereq_concept in concept_prereqs.get(concept, []):
            # Find the ULO of the prerequisite concept
            prereq_ulo = f"ULO-{prereq_concept}-01"
            if prereq_ulo in all_codes:
                add_edge(lo_code, prereq_ulo, 'L2-CONCEPT',
                         f"{concept} requires {prereq_concept}")

    # 3. Hierarchy: SIO -> CIO -> ULO
    # Build parent map from CIO codes (normalized) to ULO codes
    cio_to_ulo = {}
    for match in matched_cios.get('matched_cios', []):
        cio_code = match.get('cio_code', '')
        concept = match.get('concept_code', '')
        if cio_code and concept:
            cio_to_ulo[cio_code] = f"ULO-{concept}-01"

    # SIO parent CIO lookup from resolved_sios
    sio_to_cio = {}
    for group in resolved_sios.get('resolved_sios', []):
        cio_code = group.get('cio_code', '')
        sio_list = group.get('sios', [])
        if not sio_list and group.get('source_sio'):
            sio_list = [group['source_sio']]
        for sio in sio_list:
            code = sio.get('code', '')
            if code:
                sio_to_cio[code] = cio_code

    # SIO -> CIO
    for sio_code, cio_code in sio_to_cio.items():
        if cio_code in all_codes:
            add_edge(sio_code, cio_code, 'L1-HIERARCHY',
                     'SIO is a specific implementation of its parent CIO')

    # CIO -> ULO
    for cio_code, ulo_code in cio_to_ulo.items():
        if cio_code in all_codes and ulo_code in all_codes:
            add_edge(cio_code, ulo_code, 'L1-HIERARCHY',
                     'CIO is a conceptual implementation of its parent ULO')

    return edges


def main():
    parser = argparse.ArgumentParser(description='STEP 4.5: Generate prerequisite DAG')
    parser.add_argument('--matched-cios', type=Path, required=True,
                       help='Path to matched_cios.json from STEP 4')
    parser.add_argument('--resolved-sios', type=Path, required=True,
                       help='Path to resolved_sios.json from STEP 5')
    parser.add_argument('--reuse-inventory', type=Path, required=True,
                       help='Path to reuse_inventory.json from STEP 0')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output prerequisites.json path')
    args = parser.parse_args()

    matched_cios = load_json(args.matched_cios)
    resolved_sios = load_json(args.resolved_sios)
    inventory = load_json(args.reuse_inventory)

    master_tree = inventory.get('master_tree', {})
    print(f"[*] Master Tree: {len(master_tree.get('concepts', {}))} concepts, "
          f"{len(master_tree.get('prerequisites', []))} prereqs")

    edges = generate_prerequisites(matched_cios, resolved_sios, master_tree)

    # Count by source layer
    layers = {}
    for e in edges:
        layer = e['source_layer']
        layers[layer] = layers.get(layer, 0) + 1

    print(f"[*] Generated {len(edges)} prerequisite edges")
    for layer, count in sorted(layers.items()):
        print(f"    {layer}: {count}")

    output = {
        'prerequisites': edges,
        'summary': {
            'total_edges': len(edges),
            'by_source_layer': layers,
        }
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {args.output}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
