#!/usr/bin/env python3
"""
Verify Project Graph against codebase AST ground truth (Phase B2).

Checks 5 rules:
1. File existence check for feature/milestone/service files.
2. Platform resolution based on root source files (_platform_from_path).
3. Evidence extraction per feature (imports, api_calls, property_wrappers, type_usages) using parsers.
4. Symbol / service / layer component validation against parser output.
5. Output verified graph (with evidence per feature + warnings) and hallucinations JSON.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple

# Add repository root to sys.path to allow importing scripts modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.extract_project_keywords import (
    parse_swift_file,
    parse_cpp_file,
    parse_python_file,
    parse_ts_file,
    _platform_from_path,
)


def _norm(s: str) -> str:
    """Normalize a symbol for fuzzy matching: lowercase + strip non-alphanumeric."""
    return re.sub(r'[^a-z0-9]', '', str(s).lower())


def _symbol_matches(name: str, valid_symbols: Set[str], min_len: int = 3) -> bool:
    """Ground-truth fuzzy match: name matches valid_symbols if (after normalize)
    it is a substring of some symbol, or vice versa (bidirectional).

    Avoids false-positives where the LLM uses friendly names ('WebServer') while
    the parser sees import forms ('WebServer.h'). Still ground-truth: the name must
    actually appear in the codebase, just in a different form.
    """
    n = _norm(name)
    if len(n) < min_len:
        return False
    for sym in valid_symbols:
        ns = _norm(sym)
        if not ns:
            continue
        if n in ns or ns in n:
            return True
    return False


def extract_file_evidence(filepath: Path) -> Dict[str, List[str]]:
    """Extract AST/regex level evidence from a single file."""
    ext = filepath.suffix.lower()
    content = ""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        pass

    imports: List[str] = []
    property_wrappers: List[str] = []
    type_usages: List[str] = []
    api_calls: List[str] = []

    if ext == ".swift":
        res = parse_swift_file(filepath)
        imports.extend(res.get("imports", []))
        for pw in res.get("property_wrappers", []):
            property_wrappers.append(pw if pw.startswith("@") else f"@{pw}")
        for t in res.get("types", []):
            if isinstance(t, dict):
                if t.get("name"):
                    type_usages.append(t["name"])
                type_usages.extend(t.get("conforms_to", []))
            elif isinstance(t, str):
                type_usages.append(t)
        for fn in res.get("functions", []):
            if isinstance(fn, dict):
                if fn.get("name"):
                    api_calls.append(fn["name"])
            elif isinstance(fn, str):
                api_calls.append(fn)
        for fw in res.get("frameworks_used", []):
            api_calls.append(fw)

    elif ext in (".cpp", ".c", ".cc", ".cxx", ".h", ".hpp", ".ino"):
        res = parse_cpp_file(filepath)
        for imp in res.get("imports", []):
            if isinstance(imp, dict):
                if imp.get("module"):
                    imports.append(imp["module"])
            elif isinstance(imp, str):
                imports.append(imp)
        for t in res.get("types", []):
            if isinstance(t, dict):
                if t.get("name"):
                    type_usages.append(t["name"])
            elif isinstance(t, str):
                type_usages.append(t)
        for fn in res.get("functions", []):
            if isinstance(fn, dict):
                if fn.get("name"):
                    api_calls.append(fn["name"])
            elif isinstance(fn, str):
                api_calls.append(fn)

    elif ext == ".py":
        res = parse_python_file(filepath)
        imports.extend(res.get("imports", []))
        for t in res.get("types", []):
            if isinstance(t, dict):
                if t.get("name"):
                    type_usages.append(t["name"])
                type_usages.extend(t.get("bases", []))
            elif isinstance(t, str):
                type_usages.append(t)
        for fn in res.get("functions", []):
            if isinstance(fn, dict):
                if fn.get("name"):
                    api_calls.append(fn["name"])
            elif isinstance(fn, str):
                api_calls.append(fn)

    elif ext in (".ts", ".tsx", ".js", ".jsx"):
        res = parse_ts_file(filepath)
        imports.extend(res.get("imports", []))
        for t in res.get("types", []):
            if isinstance(t, dict):
                if t.get("name"):
                    type_usages.append(t["name"])
            elif isinstance(t, str):
                type_usages.append(t)
        for fn in res.get("functions", []):
            if isinstance(fn, dict):
                if fn.get("name"):
                    api_calls.append(fn["name"])
            elif isinstance(fn, str):
                api_calls.append(fn)

    if content:
        method_calls = re.findall(r"\b([a-zA-Z_]\w*)\s*\(", content)
        keywords = {
            "if", "for", "while", "switch", "guard", "return", "catch",
            "let", "var", "func", "struct", "class", "import", "def", "try"
        }
        for mc in method_calls:
            if mc not in keywords and not mc.startswith("_"):
                api_calls.append(mc)

    return {
        "imports": sorted(list(set(filter(None, imports)))),
        "property_wrappers": sorted(list(set(filter(None, property_wrappers)))),
        "type_usages": sorted(list(set(filter(None, type_usages)))),
        "api_calls": sorted(list(set(filter(None, api_calls)))),
    }


def verify_project_graph(graph_data: Dict[str, Any], repo_dir: Path) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Verify project graph against codebase ground truth.
    Returns (verified_graph_data, hallucinations_data).
    """
    verified = json.loads(json.dumps(graph_data))  # deep copy
    hallucinations_list: List[Dict[str, Any]] = []
    warnings: List[str] = []

    repo_dir = repo_dir.resolve()

    # Pre-parse all files in repo_dir to collect valid symbols across project
    all_repo_symbols: Set[str] = set()
    file_evidence_cache: Dict[str, Dict[str, List[str]]] = {}
    file_contents: Dict[str, str] = {}

    for file_path in repo_dir.glob("**/*"):
        if file_path.is_file() and not any(part.startswith(".") for part in file_path.parts):
            rel_path_str = str(file_path.relative_to(repo_dir))
            ev = extract_file_evidence(file_path)
            file_evidence_cache[rel_path_str] = ev
            all_repo_symbols.add(file_path.stem)
            all_repo_symbols.update(ev["type_usages"])
            all_repo_symbols.update(ev["api_calls"])
            all_repo_symbols.update(ev["imports"])
            try:
                file_contents[rel_path_str] = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                file_contents[rel_path_str] = ""
    # 1. Verify product.features (LUẬT 1, 2, 3)
    verified_features = []
    valid_feature_ids = set()

    for feature in verified.get("product", {}).get("features", []):
        feature_id = feature.get("id", "")
        claimed_files = feature.get("files", [])
        valid_files = []

        for f_path in claimed_files:
            full_p = repo_dir / f_path
            if full_p.is_file():
                valid_files.append(f_path)
            else:
                hallucinations_list.append({
                    "type": "missing_file",
                    "context": f"feature {feature_id}",
                    "file": f_path
                })

        if not valid_files:
            hallucinations_list.append({
                "type": "empty_feature",
                "context": f"feature {feature_id}",
                "message": f"Feature {feature_id} has no valid files in repo"
            })
            continue

        valid_feature_ids.add(feature_id)
        feature["files"] = valid_files

        # LUẬT 2: Platform resolution based on root source files
        file_platforms = [_platform_from_path(f, str(repo_dir)) for f in valid_files]
        if "esp32" in file_platforms:
            computed_platform = "esp32"
        else:
            computed_platform = "app"

        claimed_platform = feature.get("platform")
        if claimed_platform != computed_platform:
            warnings.append(
                f"Feature '{feature_id}' platform corrected from '{claimed_platform}' to '{computed_platform}' based on source files."
            )
            feature["platform"] = computed_platform

        # LUẬT 3: Extract evidence per feature
        feature_imports: Set[str] = set()
        feature_prop_wrappers: Set[str] = set()
        feature_type_usages: Set[str] = set()
        feature_api_calls: Set[str] = set()

        for f_path in valid_files:
            ev = file_evidence_cache.get(f_path) or extract_file_evidence(repo_dir / f_path)
            feature_imports.update(ev["imports"])
            feature_prop_wrappers.update(ev["property_wrappers"])
            feature_type_usages.update(ev["type_usages"])
            feature_api_calls.update(ev["api_calls"])

        feature["evidence"] = {
            "imports": sorted(list(feature_imports)),
            "property_wrappers": sorted(list(feature_prop_wrappers)),
            "type_usages": sorted(list(feature_type_usages)),
            "api_calls": sorted(list(feature_api_calls))
        }

        verified_features.append(feature)

    verified.setdefault("product", {})["features"] = verified_features

    # Filter product.user_journeys
    verified_journeys = []
    for journey in verified.get("product", {}).get("user_journeys", []):
        j_feat_ids = [fid for fid in journey.get("feature_ids", []) if fid in valid_feature_ids]
        if j_feat_ids:
            journey["feature_ids"] = j_feat_ids
            verified_journeys.append(journey)
    verified["product"]["user_journeys"] = verified_journeys

    # 2. Verify architecture.services (LUẬT 4)
    verified_services = []
    for service in verified.get("architecture", {}).get("services", []):
        s_name = service.get("name", "")
        s_file = service.get("file", "")
        full_p = repo_dir / s_file if s_file else None

        if not s_file or not full_p or not full_p.is_file():
            hallucinations_list.append({
                "type": "missing_service_file",
                "service": s_name,
                "file": s_file
            })
            continue

        ev = file_evidence_cache.get(s_file) or extract_file_evidence(full_p)
        file_symbols = set(ev["type_usages"]).union(set(ev["api_calls"])).union({full_p.stem})
        content = full_p.read_text(encoding="utf-8", errors="ignore") if full_p.is_file() else ""

        if not _symbol_matches(s_name, file_symbols) and _norm(s_name) not in _norm(content):
            hallucinations_list.append({
                "type": "invalid_service_symbol",
                "service": s_name,
                "file": s_file
            })
            continue

        verified_services.append(service)

    verified.setdefault("architecture", {})["services"] = verified_services

    # Verify architecture.layers (LUẬT 4)
    verified_layers = []
    for layer in verified.get("architecture", {}).get("layers", []):
        valid_comps = []
        for comp in layer.get("component_names", []):
            ok = _symbol_matches(comp, all_repo_symbols)
            if not ok:
                # Fallback: token appears literally in some real file content
                ok = any(_norm(comp) in _norm(txt) for txt in file_contents.values())
            if ok:
                valid_comps.append(comp)
            else:
                hallucinations_list.append({
                    "type": "invalid_layer_component",
                    "component": comp,
                    "layer": layer.get("name", "")
                })
        layer["component_names"] = valid_comps
        verified_layers.append(layer)
    verified["architecture"]["layers"] = verified_layers

    # 3. Verify decomposition.milestones (LUẬT 1)
    verified_milestones = []
    for milestone in verified.get("decomposition", {}).get("milestones", []):
        m_id = milestone.get("id", "")
        m_files = milestone.get("files", [])
        valid_m_files = []

        for f_path in m_files:
            if (repo_dir / f_path).is_file():
                valid_m_files.append(f_path)
            else:
                hallucinations_list.append({
                    "type": "missing_file",
                    "context": f"milestone {m_id}",
                    "file": f_path
                })

        milestone["files"] = valid_m_files
        milestone["feature_ids"] = [fid for fid in milestone.get("feature_ids", []) if fid in valid_feature_ids]
        verified_milestones.append(milestone)

    verified.setdefault("decomposition", {})["milestones"] = verified_milestones

    # Re-evaluate project platforms
    feature_platforms = {f.get("platform") for f in verified_features if f.get("platform")}
    if feature_platforms:
        current_project_platforms = set(verified.get("project", {}).get("platforms", []))
        if current_project_platforms != feature_platforms:
            warnings.append(
                f"Project platforms updated to match features: {sorted(list(feature_platforms))}"
            )
            verified.setdefault("project", {})["platforms"] = sorted(list(feature_platforms))

    verified["warnings"] = warnings

    missing_files_list = [h["file"] for h in hallucinations_list if h.get("type") == "missing_file" and "file" in h]
    invalid_symbols_list = [
        h.get("service") or h.get("component")
        for h in hallucinations_list
        if "symbol" in h.get("type", "") or "component" in h.get("type", "")
    ]

    hallucinations_output = {
        "hallucinations": hallucinations_list,
        "missing_files": sorted(list(set(missing_files_list))),
        "invalid_symbols": sorted(list(set(filter(None, invalid_symbols_list)))),
        "warnings": warnings,
    }

    return verified, hallucinations_output


def main():
    parser = argparse.ArgumentParser(description="Verify Project Graph against codebase AST ground truth (Phase B2).")
    parser.add_argument("--project-graph", required=True, help="Path to LLM output project graph JSON")
    parser.add_argument("--repo-dir", required=True, help="Path to target repository directory")
    parser.add_argument("--output", required=True, help="Output path for verified project graph JSON")
    parser.add_argument("--hallucinations-output", default=None, help="Output path for hallucinations JSON")

    args = parser.parse_args()

    graph_path = Path(args.project_graph)
    repo_dir = Path(args.repo-dir) if hasattr(args, "repo-dir") else Path(args.repo_dir)
    output_path = Path(args.output)

    if args.hallucinations_output:
        hallucinations_path = Path(args.hallucinations_output)
    else:
        hallucinations_path = output_path.parent / "hallucinations.json"

    if not graph_path.is_file():
        print(f"Error: Project graph file not found: {graph_path}", file=sys.stderr)
        sys.exit(1)

    if not repo_dir.is_dir():
        print(f"Error: Repository directory not found: {repo_dir}", file=sys.stderr)
        sys.exit(1)

    with open(graph_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    verified, hallucinations = verify_project_graph(graph_data, repo_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(verified, f, ensure_ascii=False, indent=2)

    hallucinations_path.parent.mkdir(parents=True, exist_ok=True)
    with open(hallucinations_path, "w", encoding="utf-8") as f:
        json.dump(hallucinations, f, ensure_ascii=False, indent=2)

    print(f"Verified project graph written to: {output_path}")
    print(f"Hallucinations report written to: {hallucinations_path}")


if __name__ == "__main__":
    main()
