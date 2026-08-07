#!/usr/bin/env python3
"""
B3: Map Project Graph (verified) to Knowledge Graph concepts via resolve_concepts & escalate_concepts_v3.

Usage:
  python scripts/map_project_graph.py \
    --project-graph project_graph_verified.json \
    --repo-dir /path/to/repo \
    --reuse-inventory reuse_inventory.json \
    --goal "Goal description" \
    --output concept_map.json
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def extract_keywords_from_graph(verified_graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract keywords list from verified graph evidence for resolve_concepts.py.

    Each evidence token -> {
        keyword,
        source: 'graph_evidence',
        platform: feature.platform,
        weight: 1.0,
        context: 'feature <id>'
    }
    Deduplicated per (keyword, platform), preserving first occurrence.
    """
    keywords: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str]] = set()

    features = verified_graph.get("product", {}).get("features", [])
    for feat in features:
        fid = feat.get("id", "")
        platform = feat.get("platform", "unknown")
        evidence = feat.get("evidence", {})

        categories = ["imports", "api_calls", "property_wrappers", "type_usages"]
        for cat in categories:
            items = evidence.get(cat, [])
            if isinstance(items, list):
                for token in items:
                    if token and isinstance(token, str):
                        key = (token, platform)
                        if key not in seen:
                            seen.add(key)
                            keywords.append({
                                "keyword": token,
                                "source": "graph_evidence",
                                "platform": platform,
                                "weight": 1.0,
                                "context": f"feature {fid}"
                            })

    return keywords


def build_concept_map(
    verified_graph: Dict[str, Any],
    resolved_data: Dict[str, Any],
    escalated_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Join verified graph evidence keywords with resolved/escalated concepts.

    Output format:
    {
      "schema_version": 1,
      "feature_concepts": {"F1": ["HTTP_PROTOCOL", "WEB_SERVER"]},
      "milestone_concepts": {"M1": ["HTTP_PROTOCOL", "WEB_SERVER", "FOR_LOOP"]},
      "concepts": ["FOR_LOOP", "HTTP_PROTOCOL"],
      "keyword_evidence": {"URLSession": ["HTTP_PROTOCOL"]}
    }
    """
    # 1. Map keyword -> list of concept codes
    kw_to_concepts: Dict[str, List[str]] = {}

    for item in resolved_data.get("resolved", []):
        kw = item.get("keyword")
        codes = item.get("concept_codes", [])
        if kw and codes:
            if kw not in kw_to_concepts:
                kw_to_concepts[kw] = []
            for c in codes:
                if c not in kw_to_concepts[kw]:
                    kw_to_concepts[kw].append(c)

    if escalated_data:
        for item in escalated_data.get("escalated", []):
            kw = item.get("keyword")
            raw_code = item.get("concept_code") or item.get("concept_codes")
            if kw and raw_code:
                codes = raw_code if isinstance(raw_code, list) else [raw_code]
                if kw not in kw_to_concepts:
                    kw_to_concepts[kw] = []
                for c in codes:
                    if c not in kw_to_concepts[kw]:
                        kw_to_concepts[kw].append(c)

    # 2. Map feature_id -> sorted unique concept codes
    feature_concepts: Dict[str, List[str]] = {}
    features = verified_graph.get("product", {}).get("features", [])

    for feat in features:
        fid = feat.get("id", "")
        if not fid:
            continue
        feat_concepts_set: Set[str] = set()
        evidence = feat.get("evidence", {})
        for cat_list in evidence.values():
            if isinstance(cat_list, list):
                for token in cat_list:
                    if token in kw_to_concepts:
                        for c in kw_to_concepts[token]:
                            feat_concepts_set.add(c)
        feature_concepts[fid] = sorted(list(feat_concepts_set))

    # 3. Map milestone_id -> sorted unique concept codes (union of features in milestone)
    milestone_concepts: Dict[str, List[str]] = {}
    milestones = verified_graph.get("decomposition", {}).get("milestones", [])

    for milestone in milestones:
        mid = milestone.get("id", "")
        if not mid:
            continue
        m_fids = milestone.get("feature_ids", [])
        m_concepts_set: Set[str] = set()
        for fid in m_fids:
            for c in feature_concepts.get(fid, []):
                m_concepts_set.add(c)
        milestone_concepts[mid] = sorted(list(m_concepts_set))

    # 4. Overall union of all concepts
    all_concepts = sorted(list({c for c_list in feature_concepts.values() for c in c_list}))

    # 5. keyword_evidence: map evidence keywords to concept codes
    keyword_evidence: Dict[str, List[str]] = {}
    for feat in features:
        evidence = feat.get("evidence", {})
        for cat_list in evidence.values():
            if isinstance(cat_list, list):
                for token in cat_list:
                    if token in kw_to_concepts and kw_to_concepts[token]:
                        keyword_evidence[token] = kw_to_concepts[token]

    return {
        "schema_version": 1,
        "feature_concepts": feature_concepts,
        "milestone_concepts": milestone_concepts,
        "concepts": all_concepts,
        "keyword_evidence": keyword_evidence,
    }


def main():
    parser = argparse.ArgumentParser(description="B3: Map Project Graph to Knowledge Graph concepts")
    parser.add_argument("--project-graph", required=True, type=Path, help="Verified project graph JSON file")
    parser.add_argument("--repo-dir", required=True, type=Path, help="Repository directory path")
    parser.add_argument("--reuse-inventory", type=Path, help="Reuse inventory JSON from STEP 0")
    parser.add_argument("--goal", required=True, help="User goal / application description")
    parser.add_argument("--output", required=True, type=Path, help="Output concept_map.json path")
    args = parser.parse_args()

    project_graph_path: Path = args.project_graph.resolve()
    repo_dir_path: Path = args.repo_dir.resolve()
    output_path: Path = args.output.resolve()

    if not project_graph_path.is_file():
        print(f"[ERROR] Project graph file not found: {project_graph_path}", file=sys.stderr)
        sys.exit(1)

    with open(project_graph_path, "r", encoding="utf-8") as f:
        verified_graph = json.load(f)

    # Inventory handling
    inv_path: Optional[Path] = args.reuse_inventory
    inv_file_to_use: Path
    temp_inv_dir = None

    if inv_path and inv_path.is_file():
        inv_file_to_use = inv_path.resolve()
    else:
        if inv_path:
            print(f"[WARNING] Reuse inventory file '{inv_path}' not found. Operating with empty inventory.", file=sys.stderr)
        else:
            print("[WARNING] No reuse inventory provided. Operating with empty inventory.", file=sys.stderr)

        temp_inv_dir = tempfile.TemporaryDirectory()
        temp_inv_file = Path(temp_inv_dir.name) / "empty_inventory.json"
        with open(temp_inv_file, "w", encoding="utf-8") as f:
            json.dump({"master_tree": {"concepts": {}}}, f)
        inv_file_to_use = temp_inv_file

    keywords_list = extract_keywords_from_graph(verified_graph)
    print(f"[*] Extracted {len(keywords_list)} evidence keywords from verified project graph.")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_kw_path = temp_dir_path / "keywords.json"
        temp_resolved_path = temp_dir_path / "resolved_concepts.json"
        temp_escalated_path = temp_dir_path / "escalated_concepts.json"

        # Write temp keywords.json
        kw_data = {
            "repo_dir": str(repo_dir_path),
            "primary_language": "multi",
            "languages": {},
            "source_context": {},
            "keywords": keywords_list
        }
        with open(temp_kw_path, "w", encoding="utf-8") as f:
            json.dump(kw_data, f, indent=2, ensure_ascii=False)

        scripts_dir = Path(__file__).parent.resolve()
        resolve_script = scripts_dir / "resolve_concepts.py"
        escalate_script = scripts_dir / "escalate_concepts_v3.py"

        # Call resolve_concepts.py
        print("[*] Running resolve_concepts.py...")
        cmd_resolve = [
            sys.executable,
            str(resolve_script),
            "--keywords", str(temp_kw_path),
            "--reuse-inventory", str(inv_file_to_use),
            "--goal", args.goal,
            "--output", str(temp_resolved_path),
        ]
        res_resolve = subprocess.run(cmd_resolve, capture_output=True, text=True)
        if res_resolve.returncode != 0:
            print(f"[ERROR] resolve_concepts.py failed (exit code {res_resolve.returncode}):\n{res_resolve.stderr}", file=sys.stderr)
            if temp_inv_dir:
                temp_inv_dir.cleanup()
            sys.exit(1)

        # Call escalate_concepts_v3.py
        print("[*] Running escalate_concepts_v3.py...")
        cmd_escalate = [
            sys.executable,
            str(escalate_script),
            "--keywords", str(temp_kw_path),
            "--resolved-concepts", str(temp_resolved_path),
            "--output", str(temp_escalated_path),
        ]
        res_escalate = subprocess.run(cmd_escalate, capture_output=True, text=True)
        if res_escalate.returncode != 0:
            print(f"[ERROR] escalate_concepts_v3.py failed (exit code {res_escalate.returncode}):\n{res_escalate.stderr}", file=sys.stderr)
            if temp_inv_dir:
                temp_inv_dir.cleanup()
            sys.exit(1)

        # Load resolved and escalated outputs
        with open(temp_resolved_path, "r", encoding="utf-8") as f:
            resolved_data = json.load(f)

        escalated_data = None
        if temp_escalated_path.is_file():
            with open(temp_escalated_path, "r", encoding="utf-8") as f:
                escalated_data = json.load(f)

        concept_map = build_concept_map(verified_graph, resolved_data, escalated_data)

    if temp_inv_dir:
        temp_inv_dir.cleanup()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(concept_map, f, indent=2, ensure_ascii=False)

    print(f"[✓] Concept map saved to {output_path}")
    print(f"    Features: {len(concept_map['feature_concepts'])}, "
          f"Milestones: {len(concept_map['milestone_concepts'])}, "
          f"Total concepts: {len(concept_map['concepts'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
