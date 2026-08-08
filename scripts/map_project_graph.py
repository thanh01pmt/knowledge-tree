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


def build_concept_file_index(repo_dir: Path, kw_to_concepts: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Ground-truth: concept → ALL source files where its keywords appear.

    Scans the repo with the same parser the pipeline uses (verify_project_graph
    extract_file_evidence), so we do NOT rely on the LLM's feature→file claims
    (which collapse to a single file on large repos). Every file containing an
    evidence token that maps to a concept associates that concept with the file.
    """
    import sys as _sys
    _here = Path(__file__).resolve().parent
    if str(_here) not in _sys.path:
        _sys.path.insert(0, str(_here))
    from verify_project_graph import extract_file_evidence

    concept_files: Dict[str, Set[str]] = {}

    SKIP_PARTS = {"node_modules", ".build", "Pods", ".git", ".venv", "venv",
                  "__pycache__", "build", "dist", "Tests", "tests", "TestTools",
                  "DemoApp", "Examples", "Integration", "Sample", "Samples"}
    ALLOWED_EXT = {".swift", ".py", ".ino", ".cpp", ".c", ".cc", ".cxx",
                   ".h", ".hpp", ".js", ".jsx", ".ts", ".tsx"}

    for path in repo_dir.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(repo_dir).parts
        if any(p in SKIP_PARTS for p in rel_parts[:-1]):
            continue
        if path.suffix.lower() not in ALLOWED_EXT:
            continue
        try:
            ev = extract_file_evidence(path)
        except Exception:
            continue
        rel = str(path.relative_to(repo_dir))
        # Chỉ dùng category có từ vựng khớp resolved keywords (imports, framework usage)
        tokens = set(ev.get("imports", []))
        tokens.update(ev.get("property_wrappers", []))
        tokens.update(ev.get("framework_usage", []))
        for tok in tokens:
            for code in kw_to_concepts.get(tok, []):
                concept_files.setdefault(code, set()).add(rel)

    return {c: sorted(fs) for c, fs in concept_files.items()}


def build_concept_map(
    verified_graph: Dict[str, Any],
    resolved_data: Dict[str, Any],
    escalated_data: Optional[Dict[str, Any]] = None,
    repo_dir: Optional[Path] = None,
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

    # 2. Map feature_id -> sorted unique concept codes.
    # Dùng kw_to_concepts TOÀN CỤC (keyword → concept từ resolved/escalated) —
    # KHÔNG giới hạn trong evidence của từng feature, vì evidence bị ràng buộc
    # bởi feature→file claim của LLM (thoái hóa thành 1 file trên repo lớn).
    # Mỗi feature gom concepts của MỌI keyword nó chạm tới (imports + property wrappers).
    feature_concepts: Dict[str, List[str]] = {}
    features = verified_graph.get("product", {}).get("features", [])

    for feat in features:
        fid = feat.get("id", "")
        if not fid:
            continue
        feat_concepts_set: Set[str] = set()
        evidence = feat.get("evidence", {})
        # Ưu tiên imports + property_wrappers + framework_usage — từ vựng khớp resolved keywords
        for cat in ("imports", "property_wrappers", "framework_usage"):
            for token in evidence.get(cat, []):
                for c in kw_to_concepts.get(token, []):
                    feat_concepts_set.add(c)
        # Fallback: các category khác nếu feature không có imports rõ
        if not feat_concepts_set:
            for cat_list in evidence.values():
                if isinstance(cat_list, list):
                    for token in cat_list:
                        for c in kw_to_concepts.get(token, []):
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

    concept_files: Dict[str, List[str]] = {}
    if repo_dir is not None:
        concept_files = build_concept_file_index(repo_dir, kw_to_concepts)

    return {
        "schema_version": 1,
        "feature_concepts": feature_concepts,
        "milestone_concepts": milestone_concepts,
        "concepts": all_concepts,
        "keyword_evidence": keyword_evidence,
        "concept_files": concept_files,
    }


def main():
    parser = argparse.ArgumentParser(description="B3: Map Project Graph to Knowledge Graph concepts")
    parser.add_argument("--project-graph", required=True, type=Path, help="Verified project graph JSON file")
    parser.add_argument("--repo-dir", required=True, type=Path, help="Repository directory path")
    parser.add_argument("--reuse-inventory", type=Path, help="Reuse inventory JSON from STEP 0")
    parser.add_argument("--goal", required=True, help="User goal / application description")
    parser.add_argument("--resolved-concepts", type=Path,
                        help="Optional: existing resolved_concepts.json to reuse (skip internal resolve)")
    parser.add_argument("--escalated-concepts", type=Path,
                        help="Optional: existing escalated_concepts.json to reuse (skip internal escalate)")
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
    keywords_list = extract_keywords_from_graph(verified_graph)
    print(f"[*] Extracted {len(keywords_list)} evidence keywords from verified project graph.")

    resolved_data: Dict[str, Any]
    escalated_data: Optional[Dict[str, Any]] = None

    # Reuse path: join graph evidence against the pipeline's existing
    # resolved/escalated concepts so the concept vocabulary matches what
    # JIT generates LOs for (avoids a disjoint re-resolve).
    if args.resolved_concepts and args.resolved_concepts.is_file():
        print(f"[*] Reusing resolved concepts from {args.resolved_concepts}")
        with open(args.resolved_concepts, "r", encoding="utf-8") as f:
            resolved_data = json.load(f)
        if args.escalated_concepts and args.escalated_concepts.is_file():
            print(f"[*] Reusing escalated concepts from {args.escalated_concepts}")
            with open(args.escalated_concepts, "r", encoding="utf-8") as f:
                escalated_data = json.load(f)
        concept_map = build_concept_map(verified_graph, resolved_data, escalated_data, repo_dir=repo_dir_path)
    else:
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
                sys.exit(1)

            # Load resolved and escalated outputs
            with open(temp_resolved_path, "r", encoding="utf-8") as f:
                resolved_data = json.load(f)

            if temp_escalated_path.is_file():
                with open(temp_escalated_path, "r", encoding="utf-8") as f:
                    escalated_data = json.load(f)

            concept_map = build_concept_map(verified_graph, resolved_data, escalated_data, repo_dir=repo_dir_path)

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
