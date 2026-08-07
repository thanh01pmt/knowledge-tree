#!/usr/bin/env python3
"""
STEP 9: Validate roadmap after generation - post-generation validation

Validates the final roadmap structure and completeness before rendering.

Usage:
    python scripts/validate_roadmap.py \
        --roadmap-file /tmp/roadmap.json \
        --sios-file /tmp/resolved_sios.json \
        --concepts-file /tmp/resolved_concepts.json \
        --output /tmp/validation_report.json

Validation checks:
1. Roadmap structure completeness (all phases, milestones, LOs)
2. SIO coverage (all SIOs have assignments)
3. Concept completeness (all concepts have ULO/CIO/SIO chain)
4. Prerequisite DAG validity (no cycles, all references valid)
5. Code snippet availability (at least some SIOs have code examples)
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict


def validate_roadmap_structure(roadmap: Dict) -> Dict:
    """Validate basic roadmap structure."""
    issues = []
    
    # Check required top-level keys
    required_keys = ['project_brief', 'phases', 'total_milestones', 'total_concepts']
    for key in required_keys:
        if key not in roadmap:
            issues.append(f"Missing required key: {key}")
    
    # Check phases
    phases = roadmap.get('phases', [])
    if not phases:
        issues.append("No phases defined in roadmap")
    
    for i, phase in enumerate(phases):
        if 'phase_id' not in phase:
            issues.append(f"Phase {i} missing phase_id")
        if 'title' not in phase:
            issues.append(f"Phase {i} missing title")
        if 'milestones' not in phase:
            issues.append(f"Phase {i} missing milestones")
        
        # Check milestones
        milestones = phase.get('milestones', [])
        for j, milestone in enumerate(milestones):
            if 'concept_code' not in milestone:
                issues.append(f"Phase {i}, Milestone {j} missing concept_code")
            if 'learning_objectives' not in milestone:
                issues.append(f"Phase {i}, Milestone {j} missing learning_objectives")
    
    return {
        'status': 'PASS' if not issues else 'FAIL',
        'issues': issues,
        'phase_count': len(phases),
        'total_milestones': sum(len(p.get('milestones', [])) for p in phases)
    }


def validate_sio_coverage(roadmap: Dict, resolved_sios: List[Dict]) -> Dict:
    """Validate SIO coverage theo ADR GENERATE-first (docs/ideas/2026-08-07).

    GENERATE-first: SIOs sinh trực tiếp trong roadmap (jit_los) gắn keyword
    dự án — KHÔNG còn REUSE/ADAPT từ resolved_sios. Coverage đo = tỷ lệ
    concept có ít nhất 1 SIO trong roadmap (mọi concept phải có thực hành).
    """
    issues = []
    
    # Mọi concept trong roadmap phải có ≥1 SIO (thực hành)
    concept_sio_count = {}
    for phase in roadmap.get('phases', []):
        for milestone in phase.get('milestones', []):
            concept = milestone.get('concept_code', '')
            sio_count = sum(1 for lo in milestone.get('learning_objectives', [])
                            if lo.get('lo_type') == 'SPECIFIC_IMPL')
            concept_sio_count[concept] = sio_count
    
    total_concepts = max(len(concept_sio_count), 1)
    covered = sum(1 for n in concept_sio_count.values() if n > 0)
    coverage = covered / total_concepts
    
    if coverage < 1.0:
        missing = [c for c, n in concept_sio_count.items() if n == 0]
        issues.append(f"{len(missing)} concepts thiếu SIO: {missing[:5]}")
    
    return {
        'status': 'PASS' if coverage >= 0.8 else 'WARN',
        'issues': issues,
        'coverage': round(coverage, 2),
        'roadmap_sio_count': sum(concept_sio_count.values()),
        'concepts_with_sio': covered,
        'resolved_sio_count': len(resolved_sios)  # giữ field cho tương thích
    }


def validate_semantic_keywords(roadmap: Dict, repo_dir: str, project_keywords: List[Dict]) -> Dict:
    """SEMANTIC GATE: mỗi SIO keyword phải TỒN TẠI trong code thật của dự án.

    Chặn lỗi ngữ nghĩa mà structural check bỏ qua (VD: 'forEach' không có
    trong smart-bulb-controller nhưng vẫn vào roadmap qua REUSE). Kiểm:
    1. Keyword có trong keywords.json của dự án (đã extract từ code)
    2. Hoặc keyword xuất hiện trực tiếp trong source files (grep)
    """
    issues = []
    # Gom keyword đã extract từ dự án
    extracted = {k.get('keyword', '').lower() for k in project_keywords if k.get('keyword')}

    # Gom keyword trong roadmap SIOs
    roadmap_kws = set()
    for phase in roadmap.get('phases', []):
        for milestone in phase.get('milestones', []):
            for lo in milestone.get('learning_objectives', []):
                if lo.get('lo_type') == 'SPECIFIC_IMPL' and lo.get('keyword'):
                    roadmap_kws.add((lo.get('keyword', '').lower(), lo.get('keyword'), milestone.get('concept_code', '')))

    # Tìm keyword không có trong dự án
    missing = []
    for kw_lower, kw_orig, concept in sorted(roadmap_kws):
        if kw_lower in extracted:
            continue
        # Fallback: grep trực tiếp trong source files
        if repo_dir and Path(repo_dir).exists():
            found = False
            for ext in ('*.swift', '*.py', '*.ino', '*.cpp', '*.h', '*.js', '*.ts'):
                for f in Path(repo_dir).rglob(ext):
                    try:
                        if kw_orig.lower() in f.read_text(errors='ignore').lower():
                            found = True
                            break
                    except OSError:
                        continue
                if found:
                    break
            if found:
                continue
        missing.append((kw_orig, concept))

    if missing:
        for kw, concept in missing:
            issues.append(f"SIO keyword '{kw}' ({concept}) KHÔNG có trong code dự án — SIO không gắn thực hành thật")

    status = 'PASS' if not missing else 'FAIL'
    return {
        'status': status,
        'issues': issues,
        'checked_count': len(roadmap_kws),
        'missing_keywords': [k for k, _ in missing],
    }


def validate_concept_completeness(roadmap: Dict, resolved_concepts: List[Dict]) -> Dict:
    """Validate concept chain completeness (ULO -> CIO -> SIO)."""
    issues = []
    
    # Collect all concept codes from roadmap
    roadmap_concepts = set()
    concept_lo_counts = defaultdict(lambda: {'ULO': 0, 'CIO': 0, 'SIO': 0})
    
    for phase in roadmap.get('phases', []):
        for milestone in phase.get('milestones', []):
            concept_code = milestone.get('concept_code')
            if concept_code:
                roadmap_concepts.add(concept_code)
                for lo in milestone.get('learning_objectives', []):
                    lo_type = lo.get('lo_type')
                    if lo_type in ['UNIVERSAL', 'CONCEPTUAL_IMPL', 'SPECIFIC_IMPL']:
                        type_key = {'UNIVERSAL': 'ULO', 'CONCEPTUAL_IMPL': 'CIO', 'SPECIFIC_IMPL': 'SIO'}[lo_type]
                        concept_lo_counts[concept_code][type_key] += 1
    
    # Check concept completeness
    # Count UNIQUE incomplete concepts (a concept missing both ULO and CIO
    # should count once, not twice)
    incomplete_concepts = set()
    incomplete_details = []
    for concept, counts in concept_lo_counts.items():
        missing = []
        if counts['ULO'] == 0:
            missing.append('ULO')
        if counts['CIO'] == 0:
            missing.append('CIO')
        if counts['SIO'] == 0:
            missing.append('SIO')
        if missing:
            incomplete_concepts.add(concept)
            incomplete_details.append(f"{concept} missing {'/'.join(missing)}")
    
    if incomplete_details:
        issues.append(f"{len(incomplete_concepts)} incomplete concept chains: {incomplete_details[:5]}")
    
    # Check resolved concepts are in roadmap
    resolved_concept_codes = {c.get('concept_code') for c in resolved_concepts if c.get('concept_code')}
    missing_concepts = resolved_concept_codes - roadmap_concepts
    if missing_concepts:
        issues.append(f"{len(missing_concepts)} resolved concepts not in roadmap: {list(missing_concepts)[:5]}")
    
    # Completeness never negative: clamp to [0, 1]
    complete_count = max(0, len(roadmap_concepts) - len(incomplete_concepts))
    completeness = complete_count / max(len(roadmap_concepts), 1)
    
    return {
        'status': 'PASS' if completeness >= 0.9 else 'WARN',
        'issues': issues,
        'completeness': round(completeness, 2),
        'roadmap_concept_count': len(roadmap_concepts),
        'incomplete_concept_count': len(incomplete_concepts)
    }


def validate_prerequisite_dag(roadmap: Dict) -> Dict:
    """Validate prerequisite DAG (no cycles, valid references)."""
    issues = []
    
    # Build DAG from milestones
    dag = defaultdict(set)
    all_concepts = set()
    
    for phase in roadmap.get('phases', []):
        for milestone in phase.get('milestones', []):
            concept = milestone.get('concept_code')
            if concept:
                all_concepts.add(concept)
                prereqs = milestone.get('prerequisites', [])
                for prereq in prereqs:
                    dag[concept].add(prereq)
    
    # Check for cycles using DFS
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in dag.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    visited = set()
    has_cycles = False
    for node in all_concepts:
        if node not in visited:
            if has_cycle(node, visited, set()):
                has_cycles = True
                issues.append("Cycle detected in prerequisite DAG")
                break
    
    # Check for invalid references
    invalid_refs = []
    for concept, prereqs in dag.items():
        for prereq in prereqs:
            if prereq not in all_concepts:
                invalid_refs.append(f"{concept} -> {prereq}")
    
    if invalid_refs:
        issues.append(f"{len(invalid_refs)} invalid prerequisite references: {invalid_refs[:5]}")
    
    return {
        'status': 'PASS' if not has_cycles and not invalid_refs else 'FAIL',
        'issues': issues,
        'has_cycles': has_cycles,
        'invalid_ref_count': len(invalid_refs),
        'concept_count': len(all_concepts),
        'edge_count': sum(len(prereqs) for prereqs in dag.values())
    }


def validate_code_snippets(roadmap: Dict, code_snippets: Dict) -> Dict:
    """Validate code snippet availability."""
    issues = []
    
    # Collect SIO codes that need code snippets
    sio_needing_code = set()
    for phase in roadmap.get('phases', []):
        for milestone in phase.get('milestones', []):
            for lo in milestone.get('learning_objectives', []):
                if lo.get('lo_type') == 'SPECIFIC_IMPL':
                    sio_needing_code.add(lo.get('code'))
    
    # Check which SIOs have code snippets
    matched_snippets = code_snippets.get('matched_snippets', {})
    sio_with_code = {code for code, snippets in matched_snippets.items() if snippets}
    
    coverage = len(sio_with_code & sio_needing_code) / max(len(sio_needing_code), 1)
    
    if coverage < 0.3:
        issues.append(f"Low code snippet coverage: {coverage:.0%} (recommend >= 30%)")
    
    return {
        'status': 'PASS' if coverage >= 0.3 else 'WARN',
        'issues': issues,
        'coverage': round(coverage, 2),
        'sio_needing_code': len(sio_needing_code),
        'sio_with_code': len(sio_with_code)
    }


def main():
    parser = argparse.ArgumentParser(description='Validate roadmap after generation')
    parser.add_argument('--roadmap-file', type=Path, required=True,
                       help='Path to roadmap.json')
    parser.add_argument('--sios-file', type=Path, required=True,
                       help='Path to resolved_sios.json from STEP 5')
    parser.add_argument('--concepts-file', type=Path, required=True,
                       help='Path to resolved_concepts.json from STEP 3')
    parser.add_argument('--code-snippets-file', type=Path,
                       help='Path to code_snippets.json from STEP 8.5 (optional)')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output validation report JSON')
    parser.add_argument('--keywords-file', type=Path,
                       help='Path to keywords.json from STEP 1-2 (semantic gate)')
    parser.add_argument('--repo-dir', type=str, default='',
                       help='Project repo dir (semantic gate: grep keyword in source)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.roadmap_file.exists():
        print(f"[ERROR] Roadmap file not found: {args.roadmap_file}")
        return 1
    
    if not args.sios_file.exists():
        print(f"[ERROR] SIOs file not found: {args.sios_file}")
        return 1
    
    if not args.concepts_file.exists():
        print(f"[ERROR] Concepts file not found: {args.concepts_file}")
        return 1
    
    # Load data
    with open(args.roadmap_file, 'r', encoding='utf-8') as f:
        roadmap = json.load(f)
    
    with open(args.sios_file, 'r', encoding='utf-8') as f:
        sios_data = json.load(f)
    resolved_sios = sios_data.get('resolved_sios', [])
    
    with open(args.concepts_file, 'r', encoding='utf-8') as f:
        concepts_data = json.load(f)
    resolved_concepts = concepts_data.get('resolved_concepts', [])
    
    code_snippets = {}
    if args.code_snippets_file and args.code_snippets_file.exists():
        with open(args.code_snippets_file, 'r', encoding='utf-8') as f:
            code_snippets = json.load(f)
    
    # Run validations
    print("[*] Validating roadmap structure...")
    structure_result = validate_roadmap_structure(roadmap)
    print(f"    {structure_result['status']}: {structure_result['phase_count']} phases, {structure_result['total_milestones']} milestones")
    
    print("[*] Validating SIO coverage...")
    sio_result = validate_sio_coverage(roadmap, resolved_sios)
    print(f"    {sio_result['status']}: {sio_result['coverage']:.0%} coverage")
    
    print("[*] Validating concept completeness...")
    concept_result = validate_concept_completeness(roadmap, resolved_concepts)
    print(f"    {concept_result['status']}: {concept_result['completeness']:.0%} completeness")
    
    print("[*] Validating prerequisite DAG...")
    dag_result = validate_prerequisite_dag(roadmap)
    print(f"    {dag_result['status']}: {dag_result['concept_count']} concepts, {dag_result['edge_count']} edges")
    
    # Semantic gate: SIO keyword phải tồn tại trong code dự án
    semantic_result = None
    if args.keywords_file and args.keywords_file.exists():
        with open(args.keywords_file, 'r', encoding='utf-8') as f:
            kw_data = json.load(f)
        project_keywords = kw_data.get('keywords', kw_data if isinstance(kw_data, list) else [])
        print("[*] Validating semantic keywords (phải tồn tại trong code dự án)...")
        semantic_result = validate_semantic_keywords(roadmap, args.repo_dir, project_keywords)
        if semantic_result['issues']:
            for iss in semantic_result['issues']:
                print(f"    ⚠ {iss}")
        print(f"    {semantic_result['status']}: {semantic_result['checked_count']} keywords checked")
    else:
        print("[!] Bỏ qua semantic gate (thiếu --keywords-file)")
    
    if code_snippets:
        print("[*] Validating code snippets...")
        snippets_result = validate_code_snippets(roadmap, code_snippets)
        print(f"    {snippets_result['status']}: {snippets_result['coverage']:.0%} coverage")
    else:
        snippets_result = None
    
    # Determine overall status
    all_results = [structure_result, sio_result, concept_result, dag_result]
    if snippets_result:
        all_results.append(snippets_result)
    if semantic_result:
        all_results.append(semantic_result)
    
    if any(r['status'] == 'FAIL' for r in all_results):
        overall_status = 'FAIL'
    elif any(r['status'] == 'WARN' for r in all_results):
        overall_status = 'WARN'
    else:
        overall_status = 'PASS'
    
    # Save report
    report = {
        'overall_status': overall_status,
        'validations': {
            'structure': structure_result,
            'sio_coverage': sio_result,
            'concept_completeness': concept_result,
            'prerequisite_dag': dag_result
        }
    }
    
    if snippets_result:
        report['validations']['code_snippets'] = snippets_result
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SUMMARY] Overall status: {overall_status}")
    print(f"[SUCCESS] Validation report saved to {args.output}")
    
    return 0 if overall_status != 'FAIL' else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
