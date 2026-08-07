#!/usr/bin/env python3
"""
Chuyển roadmap.json (pipeline v3, learning-objectives format) → viewer format.

Pipeline v3 xuất roadmap.json (phases + milestones + learning_objectives).
Viewer (ActionRoadmapWeb) cần format: nodes + edges (2-column card).

Script này convert: mỗi milestone (concept) → 1 implement card
(2-column: Implementation | Knowledge), grouped theo phase vertical.

Output: roadmap-viewer.json — thả vào apps/viewer/public/roadmaps/ là hiện.

Usage:
    python scripts/convert_roadmap_to_viewer.py \
        --roadmap /tmp/pipeline-bulb8/roadmap.json \
        --output apps/viewer/public/roadmaps/jit-bulb-v3.json
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List

# Phase colors (khớp ActionRoadmapWeb)
PHASE_COLORS = {
    0: '#6b6b76', 1: '#0e7c6b', 2: '#2b78e4', 3: '#8e44ad',
}
PHASE_NAMES = {
    0: 'NỀN TẢNG', 1: 'MVP', 2: 'MỞ RỘNG', 3: 'HOÀN THIỆN',
}

# Bloom level theo lo_type
LO_TYPE_BLOOM = {
    'UNIVERSAL': 'remember',
    'CONCEPTUAL_IMPL': 'understand',
    'SPECIFIC_IMPL': 'apply',
}


def convert(roadmap: dict) -> dict:
    """Convert roadmap.json → viewer format (nodes + edges)."""
    nodes = []
    edges = []
    node_id = 0
    prev_node = None

    def add_node(label, note, phase, node_type, extra=None):
        nonlocal node_id
        nid = f"n{node_id}"
        node_id += 1
        data = {
            'label': label,
            'note': note,
            'phase': phase,
            'nodeType': node_type,
            'color': PHASE_COLORS.get(phase, '#333'),
        }
        if extra:
            data.update(extra)
        nodes.append({
            'id': nid,
            'type': 'topic' if node_type == 'knowledge' else 'subtopic',
            'data': data,
            'position': {'x': 0, 'y': len(nodes) * 100},
        })
        return nid

    # START
    start_id = add_node('START', '', 0, 'start')
    prev_node = start_id

    for phase in roadmap.get('phases', []):
        pid = phase.get('phase_id', 1)
        ptitle = phase.get('title', PHASE_NAMES.get(pid, f'Phase {pid}'))

        # Phase header
        header_id = add_node(f'PHASE {pid} — {ptitle}', '', pid, 'phase')
        edges.append({'source': prev_node, 'target': header_id})
        prev_node = header_id

        for milestone in phase.get('milestones', []):
            concept = milestone.get('concept_code', 'UNSPECIFIED')
            los = milestone.get('learning_objectives', [])

            # Nhóm LOs theo lo_type
            ulos = [lo for lo in los if lo.get('lo_type') == 'UNIVERSAL']
            cios = [lo for lo in los if lo.get('lo_type') == 'CONCEPTUAL_IMPL']
            sios = [lo for lo in los if lo.get('lo_type') == 'SPECIFIC_IMPL']

            # Knowledge items = ULO/CIO/SIO descriptions
            knowledge_items = []
            for lo in ulos[:2]:
                knowledge_items.append({
                    'label': lo.get('name', ''),
                    'note': lo.get('description', '')[:60],
                    'bloom_level': 'remember',
                })
            for lo in cios[:2]:
                knowledge_items.append({
                    'label': lo.get('name', ''),
                    'note': lo.get('description', '')[:60],
                    'bloom_level': 'understand',
                })
            for lo in sios[:2]:
                knowledge_items.append({
                    'label': lo.get('name', ''),
                    'note': lo.get('description', '')[:60],
                    'bloom_level': 'apply',
                })

            # Implement card = concept
            imp_label = f'Triển khai {concept.lower().replace("_", " ")}'
            imp_note = f'{len(los)} mục tiêu học tập'
            iid = add_node(imp_label, imp_note, pid, 'implement')

            # Knowledge nodes (trước implement)
            for k in knowledge_items:
                kid = add_node(k['label'], k['note'], pid, 'knowledge',
                               {'bloom_level': k['bloom_level']})
                edges.append({'source': prev_node, 'target': kid})
                prev_node = kid

            edges.append({'source': prev_node, 'target': iid})
            prev_node = iid

    # END
    end_id = add_node('END', '', 0, 'end')
    edges.append({'source': prev_node, 'target': end_id})

    return {
        'project_brief': {
            'project_code': 'V3_ROADMAP',
            'title': roadmap.get('project_brief', {}).get('goal', 'Roadmap')[:60],
            'description': 'Roadmap từ pipeline v3 (learning objectives)',
        },
        'nodes': nodes,
        'edges': edges,
    }


def main():
    parser = argparse.ArgumentParser(description='Convert roadmap.json → viewer format')
    parser.add_argument('--roadmap', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    roadmap = json.loads(args.roadmap.read_text(encoding='utf-8'))
    result = convert(roadmap)

    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[✓] Converted: {len(result['nodes'])} nodes, {len(result['edges'])} edges")
    print(f"    Saved to {args.output}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
