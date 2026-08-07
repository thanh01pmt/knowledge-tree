#!/usr/bin/env python3
"""
STEP 6: Agent-as-Judge - Evaluate proposed concepts, SIOs, and prerequisites

This script validates the outputs from STEP 3-5 before they are applied to staging.

Evaluators:
1. concepts_evaluator - Validate proposed concepts from STEP 3
2. sios_evaluator - Validate resolved SIOs from STEP 5
3. prerequisites_evaluator - Validate prerequisite graph coherence

Usage:
    python scripts/agent_as_judge.py \
        --concepts /tmp/resolved_concepts.json \
        --sios /tmp/resolved_sios.json \
        --prerequisites /tmp/prerequisites.json \
        --output /tmp/judgment.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

sys.path.insert(0, str(Path(__file__).parent))
import lo_quality

def evaluate_concepts(concepts_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate proposed concepts from STEP 3.
    
    Checks:
    - Each proposed concept has required fields
    - Concept codes follow naming convention
    - No duplicate concepts
    """
    issues = []
    warnings = []
    
    proposed = concepts_data.get("proposed", [])
    resolved = concepts_data.get("resolved", [])
    
    print(f"[*] Evaluating {len(proposed)} proposed concepts...")
    
    # Check proposed concepts
    # At STEP 6, proposals are raw: they have keyword/source/best_match/reason
    # A 'code' field only appears after the concept is generated (STEP 7+)
    seen_keywords = set()
    seen_codes = set()
    for concept in proposed:
        keyword = concept.get("keyword", "")
        code = concept.get("code", "")
        proposed_code = concept.get("proposed_code", "")  # semantic_cluster format
        
        # Require at least one identifier: keyword | code | proposed_code
        if not keyword and not code and not proposed_code:
            issues.append(f"Proposed concept missing 'keyword'/'code'/'proposed_code': {concept}")
            continue
        
        # Use proposed_code as the code if present (semantic_cluster proposals)
        if not code and proposed_code:
            code = proposed_code
        
        # If code exists, validate naming convention
        if code:
            if not code.isupper() or " " in code:
                warnings.append(f"Proposed concept code '{code}' doesn't follow UPPER_SNAKE_CASE convention")
            if code in seen_codes:
                issues.append(f"Duplicate concept code: {code}")
            seen_codes.add(code)
        
        # Check keyword duplicates
        if keyword:
            if keyword in seen_keywords:
                warnings.append(f"Duplicate proposed keyword: {keyword}")
            seen_keywords.add(keyword)
        
        # Check that proposal has a reason or best_match for traceability
        if not concept.get("reason") and not concept.get("best_match"):
            warnings.append(f"Proposed concept '{keyword or code}' missing reason/best_match traceability")
    
    # Check resolved concepts
    print(f"[*] Evaluating {len(resolved)} resolved concepts...")
    for resolved_item in resolved:
        keyword = resolved_item.get("keyword", "")
        matches = resolved_item.get("matches", [])
        
        if not matches:
            warnings.append(f"Resolved keyword '{keyword}' has no matches (threshold too high?)")
    
    result = {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
        "summary": {
            "proposed_count": len(proposed),
            "resolved_count": len(resolved),
            "issue_count": len(issues),
            "warning_count": len(warnings)
        }
    }
    
    print(f"  Status: {result['status']}")
    if issues:
        print(f"  Issues: {len(issues)}")
        for issue in issues[:3]:
            print(f"    - {issue}")
    if warnings:
        print(f"  Warnings: {len(warnings)}")
        for warning in warnings[:3]:
            print(f"    - {warning}")
    
    return result


def evaluate_sios(sios_data: Dict[str, Any], target_tech: str) -> Dict[str, Any]:
    """
    Evaluate resolved SIOs from STEP 5.
    
    Checks:
    - REUSE actions have valid SIOs and correct tech
    - ADAPT actions have valid source SIOs
    - GENERATE actions have reasons
    - No duplicate SIOs within same CIO (cross-CIO duplicates are allowed)
    """
    issues = []
    warnings = []
    
    resolved = sios_data.get("resolved_sios", [])
    
    print(f"[*] Evaluating {len(resolved)} resolved SIOs...")
    
    action_counts = {"REUSE": 0, "ADAPT": 0, "GENERATE": 0}
    
    for sio_resolution in resolved:
        cio_code = sio_resolution.get("cio_code", "")
        action = sio_resolution.get("action", "")
        
        action_counts[action] = action_counts.get(action, 0) + 1
        
        if action == "REUSE":
            # Check reused SIOs
            sios = sio_resolution.get("sios", [])
            tech = sio_resolution.get("tech", "")
            
            if not sios:
                issues.append(f"REUSE action for {cio_code} has no SIOs")
                continue
            
            if tech != target_tech:
                issues.append(f"REUSE action for {cio_code} has wrong tech: {tech} (expected {target_tech})")
            
            # Check for duplicates within this CIO only (cross-CIO duplicates are OK)
            codes_in_this_cio = set()
            for sio in sios:
                code = sio.get("code", "")
                if code in codes_in_this_cio:
                    issues.append(f"Duplicate SIO code within {cio_code}: {code}")
                codes_in_this_cio.add(code)
        
        elif action == "ADAPT":
            # Check adapted SIOs
            source_sio = sio_resolution.get("source_sio", {})
            source_tech = sio_resolution.get("source_tech", "")
            similarity = sio_resolution.get("similarity", 0.0)
            
            if not source_sio:
                issues.append(f"ADAPT action for {cio_code} has no source_sio")
                continue
            
            if not source_tech:
                warnings.append(f"ADAPT action for {cio_code} missing source_tech")
            
            if similarity < 0.3:
                warnings.append(f"ADAPT action for {cio_code} has low similarity: {similarity:.2f}")
        
        elif action == "GENERATE":
            # Check generated SIOs (minimal validation)
            reason = sio_resolution.get("reason", "")
            if not reason:
                warnings.append(f"GENERATE action for {cio_code} missing reason")
    
    result = {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
        "summary": {
            "total_sios": len(resolved),
            "action_counts": action_counts,
            "issue_count": len(issues),
            "warning_count": len(warnings)
        }
    }
    
    print(f"  Status: {result['status']}")
    print(f"  Actions: {action_counts}")
    if issues:
        print(f"  Issues: {len(issues)}")
        for issue in issues[:3]:
            print(f"    - {issue}")
    if warnings:
        print(f"  Warnings: {len(warnings)}")
        for warning in warnings[:3]:
            print(f"    - {warning}")
    
    return result


def evaluate_prerequisites(prereqs_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate prerequisite graph from STEP 4.
    
    Checks:
    - No circular dependencies
    - All source/target codes exist
    - Prerequisites are acyclic (DAG)
    """
    issues = []
    warnings = []
    
    prerequisites = prereqs_data.get("prerequisites", [])
    all_codes = set(prereqs_data.get("all_codes", []))
    
    print(f"[*] Evaluating {len(prerequisites)} prerequisites...")
    
    # Build adjacency list for cycle detection
    graph = {}
    for prereq in prerequisites:
        source = prereq.get("source_code", "")
        target = prereq.get("target_code", "")
        
        # Check codes exist
        if source not in all_codes:
            warnings.append(f"Prerequisite source '{source}' not in all_codes")
        if target not in all_codes:
            warnings.append(f"Prerequisite target '{target}' not in all_codes")
        
        # Build graph
        if source not in graph:
            graph[source] = []
        graph[source].append(target)
    
    # Detect cycles using DFS
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    visited = set()
    has_cycles = False
    for node in graph:
        if node not in visited:
            if has_cycle(node, visited, set()):
                has_cycles = True
                issues.append(f"Cycle detected involving node: {node}")
                break
    
    if not has_cycles:
        print(f"  ✓ No circular dependencies detected")
    
    result = {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
        "summary": {
            "prerequisite_count": len(prerequisites),
            "unique_codes": len(all_codes),
            "has_cycles": has_cycles,
            "issue_count": len(issues),
            "warning_count": len(warnings)
        }
    }
    
    print(f"  Status: {result['status']}")
    if issues:
        print(f"  Issues: {len(issues)}")
        for issue in issues[:3]:
            print(f"    - {issue}")
    if warnings:
        print(f"  Warnings: {len(warnings)}")
        for warning in warnings[:3]:
            print(f"    - {warning}")
    
    return result


def evaluate_roadmap(roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    POST-ROADMAP evaluation — Judge roadmap HOÀN CHỈNH (sau khi assemble).

    Kiểm ngữ nghĩa (structural validator bỏ qua):
    1. Mỗi concept card có ĐỦ Concept (ULO/CIO) + Keyword (SIO)? — không card
       nào chỉ có 1 bên (lỗi horizontal slicing đã gặp)
    2. Mỗi SIO keyword là keyword THỰC HÀNH, không phải tên concept lọt
       (VD 'http protocol' từ SIO name — sai, phải là URLSession)
    3. Bloom đúng tầng: ULO=understand, CIO=apply, SIO=create
    4. Không template máy móc (ngưỡng/mô hình tham chiếu/nguyên lý phổ quát)
    5. Platform (app/esp32) nhất quán: SIO code prefix khớp platform field
    """
    issues = []
    warnings = []

    CONCEPT_NAME_SIGNALS = ['http protocol', 'definite iteration']  # tên concept lọt làm keyword

    total_cards = 0
    for phase in roadmap_data.get('phases', []):
        for milestone in phase.get('milestones', []):
            total_cards += 1
            los = milestone.get('learning_objectives', [])
            ulos = [lo for lo in los if lo.get('lo_type') == 'UNIVERSAL']
            cios = [lo for lo in los if lo.get('lo_type') == 'CONCEPTUAL_IMPL']
            sios = [lo for lo in los if lo.get('lo_type') == 'SPECIFIC_IMPL']

            # 1. Đủ Concept + Keyword?
            if not ulos and not cios:
                issues.append(f"[{milestone.get('concept_code')}] Card thiếu Concept (ULO/CIO)")
            if not sios:
                issues.append(f"[{milestone.get('concept_code')}] Card thiếu Keyword (SIO) — không thực hành")

            # 2. Keyword thực hành, không phải tên concept
            for sio in sios:
                kw = (sio.get('keyword') or '').strip()
                if kw and kw.lower() in CONCEPT_NAME_SIGNALS:
                    issues.append(f"[{milestone.get('concept_code')}] Keyword '{kw}' là tên concept lọt — cần keyword code thật")

            # 3. Bloom đúng tầng
            for lo in los:
                bloom = (lo.get('bloom_level') or '').lower()
                lt = lo.get('lo_type', '')
                if lt == 'UNIVERSAL' and bloom not in ('understand', 'remember'):
                    warnings.append(f"[{milestone.get('concept_code')}] ULO bloom '{bloom}' (mong đợi understand)")
                if lt == 'SPECIFIC_IMPL' and bloom not in ('create', 'apply'):
                    warnings.append(f"[{milestone.get('concept_code')}] SIO bloom '{bloom}' (mong đợi create)")

            # 4. Không template
            for lo in los:
                desc = lo.get('description') or ''
                if lo_quality.is_template_description(desc):
                    issues.append(f"[{milestone.get('concept_code')}] Mô tả template máy móc: {lo.get('code')}")

            # 5. Check needs_review
            for lo in los:
                if lo.get('needs_review') is True:
                    warnings.append(f"[{milestone.get('concept_code')}] LO {lo.get('code')} đánh dấu needs_review — mô tả thiếu nguyên liệu")

            # 5. Platform nhất quán
            for sio in sios:
                platform = sio.get('platform') or ''
                code = sio.get('code') or ''
                if platform == 'esp32' and not code.startswith('SIO-ESP32'):
                    issues.append(f"[{milestone.get('concept_code')}] platform=esp32 nhưng code '{code}' không prefix ESP32")
                if platform == 'app' and not code.startswith('SIO-SWIFT') and 'SWIFT' not in code:
                    warnings.append(f"[{milestone.get('concept_code')}] platform=app nhưng code '{code}' không prefix SWIFT")

    status = 'FAIL' if issues else ('WARN' if warnings else 'PASS')
    return {
        'status': status,
        'issues': issues,
        'warnings': warnings,
        'cards_checked': total_cards,
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="STEP 6: Agent-as-Judge validation")
    parser.add_argument("--concepts", help="Path to resolved_concepts.json from STEP 3")
    parser.add_argument("--sios", help="Path to resolved_sios.json from STEP 5")
    parser.add_argument("--prerequisites", help="Path to prerequisites.json from STEP 4")
    parser.add_argument("--target-tech", default="SWIFT", help="Target tech stack (default: SWIFT)")
    parser.add_argument("--roadmap", help="Path to roadmap.json (POST-ROADMAP evaluation)")
    parser.add_argument("--output", default="/tmp/judgment.json", help="Output judgment file")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("STEP 6: Agent-as-Judge Validation")
    print("=" * 70)
    
    judgment = {
        "evaluators": {},
        "overall_status": "PASS"
    }
    
    # Evaluate concepts
    if args.concepts:
        concepts_path = Path(args.concepts)
        if concepts_path.exists():
            with open(concepts_path) as f:
                concepts_data = json.load(f)
            judgment["evaluators"]["concepts"] = evaluate_concepts(concepts_data)
            if judgment["evaluators"]["concepts"]["status"] == "FAIL":
                judgment["overall_status"] = "FAIL"
        else:
            print(f"[!] Concepts file not found: {args.concepts}")
    
    # Evaluate SIOs
    if args.sios:
        sios_path = Path(args.sios)
        if sios_path.exists():
            with open(sios_path) as f:
                sios_data = json.load(f)
            judgment["evaluators"]["sios"] = evaluate_sios(sios_data, args.target_tech)
            if judgment["evaluators"]["sios"]["status"] == "FAIL":
                judgment["overall_status"] = "FAIL"
        else:
            print(f"[!] SIOs file not found: {args.sios}")
    
    # Evaluate roadmap (POST-ROADMAP — sau khi assemble xong)
    if args.roadmap:
        roadmap_path = Path(args.roadmap)
        if roadmap_path.exists():
            with open(roadmap_path) as f:
                roadmap_data = json.load(f)
            judgment["evaluators"]["roadmap"] = evaluate_roadmap(roadmap_data)
            if judgment["evaluators"]["roadmap"]["status"] == "FAIL":
                judgment["overall_status"] = "FAIL"
            print(f"[Roadmap] {judgment['evaluators']['roadmap']['status']}: "
                  f"{judgment['evaluators']['roadmap']['cards_checked']} cards checked")
            for iss in judgment["evaluators"]["roadmap"].get("issues", []):
                print(f"    ✗ {iss}")
            for warn in judgment["evaluators"]["roadmap"].get("warnings", []):
                print(f"    ! {warn}")
        else:
            print(f"[!] Roadmap file not found: {args.roadmap}")
    
    # Evaluate prerequisites
    if args.prerequisites:
        prereqs_path = Path(args.prerequisites)
        if prereqs_path.exists():
            with open(prereqs_path) as f:
                prereqs_data = json.load(f)
            judgment["evaluators"]["prerequisites"] = evaluate_prerequisites(prereqs_data)
            if judgment["evaluators"]["prerequisites"]["status"] == "FAIL":
                judgment["overall_status"] = "FAIL"
        else:
            print(f"[!] Prerequisites file not found: {args.prerequisites}")
    
    # Save judgment
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(judgment, f, indent=2)
    
    print("\n" + "=" * 70)
    print(f"Overall Status: {judgment['overall_status']}")
    print(f"Judgment saved to: {output_path}")
    print("=" * 70)
    
    # Exit with error code if failed
    if judgment["overall_status"] == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
