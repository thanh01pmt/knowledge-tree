#!/usr/bin/env python3
"""
STEP 8.7: Assemble final roadmap from resolved artifacts.

Reads:
- resolved_sios.json (from STEP 5)
- matched_cios.json (from STEP 4, includes derived_ulos)
- prerequisites.json (from STEP 4.5)
- jit_los.json (from STEP 5.5, optional)
- instruction/ (from STEP 8.6, optional)

Performs:
1. Build LO inventory (ULO/CIO/SIO per concept)
2. Topological sort on prerequisite DAG (Kahn's algorithm, layered)
3. Group into phases by layer
4. Attach rationale + assessment + instruction reference per LO

Outputs:
- roadmap.json: {project_brief, phases[], total_milestones, total_concepts}
"""

import json
import argparse
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Set, Tuple


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Dấu hiệu template máy móc (Master Tree sinh data thối — 2160 CIOs từ 12-verb pattern)
# 1. Pattern code: CIO-XXX-NN-VERB (VD: CIO-FOR_LOOP-02-EXPLAIN_MECHANISM)
#    → 12 verb máy móc áp cho 70-270 concepts mỗi cái, không phải content thật
# 2. Description chứa cụm generic (fallback nếu code pattern bị đổi dạng)
_TEMPLATE_CIO_VERBS = {
    'EXPLAIN_MECHANISM', 'INTERPRET_PARAMETERS', 'DECOMPOSE_TRADEOFFS',
    'COMPARE_ALTERNATIVES', 'IDENTIFY_COMPONENTS', 'RECALL_DEFINITIONS',
    'IMPLEMENT_PATTERN', 'ADAPT_TO_CONTEXT', 'ASSESS_QUALITY',
    'CRITIQUE_DESIGN', 'DESIGN_SOLUTION', 'INNOVATE_EXTENSION',
}
_TEMPLATE_DESC_SIGNALS = [
    'ngưỡng', 'vật lý/logic', 'mô hình tham chiếu', 'chỉ số trong',
    'nguyên lý phổ quát', 'hiểu:', 'vai trò của nó trong thiết kế',
    'định lượng đánh đổi', 'tiêu chuẩn ngành', 'benchmark', 'nợ kỹ thuật',
    'tối ưu hóa đột phá', 'tích hợp cross-cutting', 'điều kiện biên',
    'so sánh nhiều phương pháp/kiến trúc cho', 'phân rã', 'cơ chế hoạt động nội tại',
]


def infer_keyword_from_sio(sio: dict) -> str:
    """Trích keyword thực hành từ SIO name khi SIO không có field keyword.

    Ưu tiên token đặc thù (camelCase, @property, ký tự đặc biệt) thay vì
    cả câu. VD:
      'Use a for-in loop with a Range in Swift' → 'for-in'
      'Swift: Use @StateObject for Reference Type State' → '@StateObject'
      'Configure Custom HTTP Request Headers' → 'HTTP Request Headers'
    """
    kw = (sio.get('keyword') or '').strip()
    if kw:
        return kw
    name = sio.get('name', '') or ''
    name = re.sub(r'^SWIFT:\s*|^Swift:\s*', '', name)
    # Token đặc thù: @Property, camelCase, ký tự đặc biệt (for-in, forEach, _)
    tokens = re.findall(r'@[\w.]+|[a-z]+[A-Z][\w]*|[\w]+-[\w]+|_[\w]*', name)
    if tokens:
        # Ưu tiên token có @ hoặc camelCase hoặc ký tự đặc biệt
        special = [t for t in tokens if '@' in t or '-' in t or '_' in t or (t != t.lower() and t != t.upper())]
        if special:
            return special[0]
        return tokens[0]
    # Fallback: bỏ động từ mở đầu, lấy phần còn lại cắt ngắn
    name = re.sub(r'^(Use|Using|Configure|Implement|Apply|Understand|Traverse|Iterate|Declare|Mutate)\s+', '', name)
    return name.strip(' .,;')[:40]


def is_template_cio_code(cio_code: str) -> bool:
    """True nếu code CIO theo pattern 12-verb template (VD: -02-EXPLAIN_MECHANISM)."""
    if not cio_code:
        return False
    for verb in _TEMPLATE_CIO_VERBS:
        if cio_code.endswith(f'-{verb}'):
            return True
    return False


def is_template_description(desc: str) -> bool:
    """True nếu description là template máy móc (data thối), không đưa vào roadmap."""
    if not desc:
        return False
    d = desc.lower()
    return any(sig in d for sig in _TEMPLATE_DESC_SIGNALS)


def collect_los(matched_cios: dict, resolved_sios: dict, jit_los: dict) -> Dict[str, dict]:
    """Build {lo_code: {code, lo_type, concept, name, description, assessment}}."""
    los = {}

    # ULOs (derived in STEP 4)
    for ulo in matched_cios.get('derived_ulos', []):
        code = ulo.get('code', '')
        if code and not is_template_description(ulo.get('description', '')):
            los[code] = {
                'code': code,
                'lo_type': 'UNIVERSAL',
                'concept': (ulo.get('concept_codes') or [''])[0],
                'name': ulo.get('name', ''),
                'description': ulo.get('description', ''),
                'assessment': ulo.get('assessment_approach', 'concept-check'),
                'bloom_level': (ulo.get('bloom_level') or 'understand').lower(),
                'knowledge_dimension': ulo.get('knowledge_dimension') or 'CONCEPTUAL',
            }

    # CIOs (matched in STEP 4) — bỏ template data thối từ Master Tree
    for match in matched_cios.get('matched_cios', []):
        code = match.get('cio_code', '')
        if code and not is_template_description(match.get('cio_description', '')) \
                and not is_template_cio_code(code):
            los[code] = {
                'code': code,
                'lo_type': 'CONCEPTUAL_IMPL',
                'concept': match.get('concept_code', ''),
                'name': match.get('cio_name', ''),
                'description': match.get('cio_description', ''),
                'assessment': 'code-lab',
                'bloom_level': (match.get('bloom_level') or 'apply').lower(),
                'knowledge_dimension': match.get('knowledge_dimension') or 'PROCEDURAL',
            }

    # SIOs (resolved in STEP 5: REUSE 'sios' + ADAPT 'source_sio')
    seen_sio_codes = set()
    seen_sio_names = set()
    for group in resolved_sios.get('resolved_sios', []):
        concept = group.get('concept_code', '')
        sio_list = group.get('sios', [])
        if not sio_list and group.get('source_sio'):
            sio_list = [group['source_sio']]
        for sio in sio_list:
            code = sio.get('code', '')
            if not code or code in seen_sio_codes:
                continue  # trùng code (REUSE lặp) — bỏ
            seen_sio_codes.add(code)
            name = sio.get('name', '') or code
            if name in seen_sio_names:
                continue  # trùng tên (Master Tree 2 SIO cùng tên) — giữ 1
            seen_sio_names.add(name)
            if not is_template_description(sio.get('description', '')):
                los[code] = {
                    'code': code,
                    'lo_type': 'SPECIFIC_IMPL',
                    'concept': concept,
                    'name': sio.get('name', ''),
                    'description': sio.get('description', ''),
                    'assessment': 'code-review',
                    'bloom_level': (sio.get('bloom_level') or 'create').lower(),
                    'knowledge_dimension': sio.get('knowledge_dimension') or 'PROCEDURAL',
                    'keyword': infer_keyword_from_sio(sio),
                }

    # JIT-generated LOs (STEP 5.5)
    for lo in jit_los.get('generated', []):
        code = lo.get('code', '')
        if code:
            los[code] = {
                'code': code,
                'lo_type': lo.get('lo_type', ''),
                'concept': (lo.get('concept_codes') or [''])[0],
                'name': lo.get('name', ''),
                'description': lo.get('description', ''),
                'assessment': lo.get('assessment_approach', 'code-review'),
                'bloom_level': (lo.get('bloom_level') or 'understand').lower(),
                'knowledge_dimension': lo.get('knowledge_dimension') or 'CONCEPTUAL',
                'keyword': lo.get('keyword', '') or '',
            }

    return los


def build_dag(prerequisites: dict, los: Dict[str, dict]) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
    """Build prerequisite DAG: {lo_code: [prereq_codes]} + {lo_code: rationale}."""
    dag = defaultdict(list)
    rationale = {}
    for edge in prerequisites.get('prerequisites', []):
        target = edge.get('learning_objective_code', '')
        prereq = edge.get('prerequisite_lo_code', '')
        if target in los and prereq in los and target != prereq:
            dag[target].append(prereq)
            rationale[(prereq, target)] = edge.get('rationale', '')
    return dag, rationale


def topo_layers(dag: Dict[str, List[str]], los: Dict[str, dict]) -> List[List[str]]:
    """Kahn's algorithm with layering. Returns list of layers (each = list of LO codes)."""
    in_degree = {code: 0 for code in los}
    forward = defaultdict(list)  # prereq -> dependents

    for target, prereqs in dag.items():
        for prereq in prereqs:
            if prereq in in_degree:
                in_degree[target] += 1
                forward[prereq].append(target)

    # Nodes with no prerequisites start first
    queue = deque([c for c in los if in_degree[c] == 0])
    layers = []
    processed = set()

    while queue:
        layer = list(queue)
        layers.append(layer)
        next_queue = deque()
        for node in layer:
            processed.add(node)
            for dependent in forward[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0 and dependent not in processed:
                    next_queue.append(dependent)
        queue = next_queue

    # Any remaining nodes (cycles) — append as final layer
    remaining = [c for c in los if c not in processed]
    if remaining:
        layers.append(remaining)

    return layers


def group_by_concept(layers: List[List[str]], los: Dict[str, dict]) -> List[dict]:
    """Group LO codes by concept within each layer, preserving order."""
    phases = []
    for layer_idx, layer in enumerate(layers):
        # Group layer LOs by concept
        by_concept = defaultdict(list)
        for code in layer:
            concept = los[code]['concept'] or 'UNSPECIFIED'
            by_concept[concept].append(code)

        milestones = []
        for concept, codes in sorted(by_concept.items()):
            milestones.append({
                'concept_code': concept,
                'learning_objectives': [los[c] for c in codes],
            })

        phases.append({
            'phase_id': layer_idx + 1,
            'title': f"Phase {layer_idx + 1}: Foundation" if layer_idx == 0 else f"Phase {layer_idx + 1}",
            'milestones': milestones,
        })
    return phases


# ============================================================================
# VERTICAL SLICING PHASES (docs/ideas/2026-08-07-vertical-slicing-roadmap.md)
# ============================================================================
# Phase theo MỨC ĐỘ HOÀN THIỆN SẢN PHẨM, không theo topological layer:
#   P0 NỀN TẢNG   — ULO nền tảng (remember/understand)
#   P1 MVP        — ULO/CIO cốt lõi (understand/apply) — sản phẩm chạy được
#   P2 MỞ RỘNG    — CIO/SIO thật hóa (apply) — I/O, API, persistence
#   P3 HOÀN THIỆN — SIO robustness (create) — error handling, test, polish

VERTICAL_PHASES = [
    {'id': 0, 'title': 'NỀN TẢNG', 'desc': 'Làm quen công cụ, ngôn ngữ, thiết lập dự án'},
    {'id': 1, 'title': 'MVP', 'desc': 'Sản phẩm chạy được từ đầu (UI + logic + data tối giản)'},
    {'id': 2, 'title': 'MỞ RỘNG', 'desc': 'Thật hóa: API thật, file persistence, lọc'},
    {'id': 3, 'title': 'HOÀN THIỆN', 'desc': 'Độ chắc: error handling, validation, test, polish'},
]

# Bloom level theo lo_type (heuristic — có thể override bằng data)
LO_TYPE_BLOOM = {
    'UNIVERSAL': 'understand',
    'CONCEPTUAL_IMPL': 'apply',
    'SPECIFIC_IMPL': 'create',
}


def vertical_phase_for_lo(lo: dict) -> int:
    """Assign vertical phase cho 1 LO dựa trên lo_type + bloom_level."""
    lo_type = lo.get('lo_type', '')
    bloom = (lo.get('bloom_level', '') or LO_TYPE_BLOOM.get(lo_type, 'understand')).lower()

    # P3: create (SIO robustness)
    if bloom == 'create':
        return 3
    # P2: apply (CIO/SIO thật hóa)
    if bloom == 'apply':
        return 2
    # P1: understand (ULO/CIO cốt lõi)
    if bloom == 'understand':
        return 1
    # P0: remember (nền tảng)
    return 0


def group_vertical_phases(layers: List[List[str]], los: Dict[str, dict]) -> List[dict]:
    """Group LOs vào 4 phase vertical (NỀN TẢNG → MVP → MỞ RỘNG → HOÀN THIỆN).

    Giữ nguyên topological order bên trong mỗi phase (dependency vẫn đúng),
    chỉ đổi cách nhóm phase từ "layer" sang "mức hoàn thiện sản phẩm".
    """
    # Gán phase cho từng LO
    lo_phase = {}
    for layer in layers:
        for code in layer:
            lo_phase[code] = vertical_phase_for_lo(los[code])

    # Gom theo phase, giữ thứ tự layer (dependency order)
    phases = []
    for p in VERTICAL_PHASES:
        p_codes = [c for layer in layers for c in layer if lo_phase.get(c) == p['id']]
        if not p_codes:
            continue
        # Group theo concept trong phase
        by_concept = defaultdict(list)
        for code in p_codes:
            concept = los[code]['concept'] or 'UNSPECIFIED'
            by_concept[concept].append(code)
        milestones = []
        for concept, codes in sorted(by_concept.items()):
            milestones.append({
                'concept_code': concept,
                'learning_objectives': [los[c] for c in codes],
            })
        phases.append({
            'phase_id': p['id'],
            'title': p['title'],
            'description': p['desc'],
            'milestones': milestones,
        })
    return phases


def attach_metadata(phases: List[dict], rationale: Dict[Tuple[str, str], str],
                     instruction_dir: Path) -> List[dict]:
    """Attach rationale + instruction reference to each LO."""
    for phase in phases:
        for milestone in phase['milestones']:
            concept = milestone['concept_code']
            # Instruction file for this concept
            safe = concept.lower().replace(' ', '_')
            instr_file = instruction_dir / f"instruction-{safe}.md"
            instr_ref = str(instr_file) if instr_file.exists() else None

            for lo in milestone['learning_objectives']:
                code = lo['code']
                # Rationale: find edges where this LO is the target
                lo_rationale = [
                    rationale.get((p, code), '')
                    for p in dag.get(code, [])
                    if rationale.get((p, code))
                ]
                lo['rationale'] = lo_rationale
                lo['instruction_ref'] = instr_ref
    return phases


def main():
    parser = argparse.ArgumentParser(description='STEP 8.7: Assemble final roadmap')
    parser.add_argument('--matched-cios', type=Path, required=True)
    parser.add_argument('--resolved-sios', type=Path, required=True)
    parser.add_argument('--prerequisites', type=Path, required=True)
    parser.add_argument('--jit-los', type=Path, help='Optional: jit_los.json from STEP 5.5')
    parser.add_argument('--instruction-dir', type=Path, help='Optional: instruction/ from STEP 8.6')
    parser.add_argument('--goal', type=str, default='')
    parser.add_argument('--tech-stack', type=str, default='')
    parser.add_argument('--vertical', action='store_true',
                       help='Dùng vertical slicing phases (NỀN TẢNG/MVP/MỞ RỘNG/HOÀN THIỆN) thay vì topological layers')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    matched_cios = load_json(args.matched_cios)
    resolved_sios = load_json(args.resolved_sios)
    prerequisites = load_json(args.prerequisites)
    jit_los = load_json(args.jit_los) if args.jit_los and args.jit_los.exists() else {'generated': []}

    # 1. Build LO inventory
    los = collect_los(matched_cios, resolved_sios, jit_los)
    print(f"[*] LO inventory: {len(los)} LOs")

    # 2. Build DAG
    global dag
    dag, rationale = build_dag(prerequisites, los)
    print(f"[*] Prerequisite edges: {sum(len(v) for v in dag.values())}")

    # 3. Topological sort with layering
    layers = topo_layers(dag, los)
    print(f"[*] Topological layers: {len(layers)}")
    for i, layer in enumerate(layers):
        print(f"    Layer {i+1}: {len(layer)} LOs")

    # 4. Group into phases — vertical slicing (nếu --vertical) hoặc topological layers
    if args.vertical:
        phases = group_vertical_phases(layers, los)
        print(f"[*] Vertical phases: {len(phases)}")
        for p in phases:
            print(f"    {p['title']}: {sum(len(m['learning_objectives']) for m in p['milestones'])} LOs")
    else:
        phases = group_by_concept(layers, los)

    # 5. Attach rationale + instruction refs
    if args.instruction_dir and args.instruction_dir.exists():
        phases = attach_metadata(phases, rationale, args.instruction_dir)

    # 6. Build roadmap
    roadmap = {
        'project_brief': {
            'goal': args.goal,
            'tech_stack': [t.strip() for t in args.tech_stack.split(',')] if args.tech_stack else [],
        },
        'phases': phases,
        'total_milestones': sum(len(p['milestones']) for p in phases),
        'total_concepts': len({m['concept_code'] for p in phases for m in p['milestones']}),
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(roadmap, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Roadmap assembled: {roadmap['total_milestones']} milestones, "
          f"{roadmap['total_concepts']} concepts, {len(phases)} phases")
    print(f"    Saved to {args.output}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
