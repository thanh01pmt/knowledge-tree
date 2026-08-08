#!/usr/bin/env python3
"""
llm_project_graph.py — DemoApp-first LLM Project Graph Extraction & Verification Pipeline.

Pipeline:
1. [STEP A - code] collect_target_files: detect DemoApp/Example/App/Examples -> files
2. [STEP B - code] build_sdk_api_index: scan public symbols in SDK core & check usage in demo app
3. [STEP C - 1 LLM call] project graph: extract features, files, api_usage, keywords
4. [STEP D - code verify] ground-truth verification: remove invalid files, APIs, keywords -> hallucinations
5. [STEP E - 1 LLM call] concept map: escalate keywords/apis to neutral concepts + evidence files join

Outputs verified project graph JSON (schema version 2).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / '.env')

SKIP_DIRS = {
    "node_modules", ".build", "Pods", ".git", ".venv", "venv",
    "__pycache__", "build", "dist", ".idea", ".vscode"
}

SKIP_NAME_MARKERS = {
    "test", "demo", "sample", "example", "playground", "fixture",
    "docc", "docs", "readme", "integration", "mock", "stub"
}

ALLOWED_EXTENSIONS = {".swift", ".py", ".ts", ".js", ".ino", ".cpp", ".c", ".h"}
APP_DIR_CANDIDATES = ["DemoApp", "Example", "App", "Examples"]

PUBLIC_SYMBOL_REGEX = re.compile(
    r'\bpublic\s+(?:final\s+|open\s+)?(?:class|struct|enum|protocol|func|var|let)\s+(\w+)'
)
EXPORT_SYMBOL_REGEX = re.compile(
    r'\bexport\s+(?:default\s+)?(?:class|interface|type|enum|function|const|let|var)\s+(\w+)'
)


def _is_skip_dir(name: str, check_markers: bool = True) -> bool:
    """True if directory name should be skipped."""
    if name in SKIP_DIRS:
        return True
    if check_markers:
        lowered = name.lower()
        return any(marker in lowered for marker in SKIP_NAME_MARKERS)
    return False


def collect_target_files(
    repo_dir: Path,
    target: str = 'auto',
    max_files: int = 70,
    max_chars: int = 120000
) -> Tuple[List[Path], Dict[str, str]]:
    """
    STEP A: Collect target files based on target selection logic.
    Returns (collected_paths, file_contents_map).
    file_contents_map keys are relative paths to repo_dir.
    """
    repo_dir = repo_dir.resolve()
    if not repo_dir.exists():
        raise FileNotFoundError(f"repo_dir does not exist: {repo_dir}")

    target_files: List[Path] = []

    # 1. Search for app directory candidates if target is auto or demo_app
    if target in ('auto', 'demo_app'):
        for cand in APP_DIR_CANDIDATES:
            cand_low = cand.lower()
            matching_dirs: List[Path] = []
            for root, dirs, _ in os.walk(repo_dir):
                # Filter out skip dirs
                dirs[:] = [d for d in dirs if not _is_skip_dir(d, check_markers=False)]
                root_path = Path(root)
                for d in dirs:
                    if d.lower() == cand_low or cand_low in d.lower():
                        matching_dirs.append(root_path / d)

            if matching_dirs:
                # Collect files inside matching app directories
                cand_files: List[Path] = []
                for mdir in matching_dirs:
                    for path in mdir.rglob("*"):
                        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
                            rel_parts = path.relative_to(repo_dir).parts
                            if not any(_is_skip_dir(part, check_markers=False) for part in rel_parts[:-1]):
                                cand_files.append(path)
                if cand_files:
                    target_files = cand_files
                    break

    # 2. Validation & Fallback logic
    if not target_files:
        if target == 'demo_app':
            raise RuntimeError(
                f"[ERROR] Target 'demo_app' specified but no DemoApp/Example/App/Examples "
                f"directory containing source files was found in {repo_dir}"
            )
        # target == 'auto' fallback or target == 'sdk_core'
        collected: List[Path] = []
        for path in repo_dir.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(repo_dir).parts
            if any(_is_skip_dir(part, check_markers=True) for part in rel_parts[:-1]):
                continue
            if path.suffix.lower() in ALLOWED_EXTENSIONS:
                collected.append(path)
        target_files = collected

    # 3. Sort files by size descending (and rel path ascending for stability)
    target_files.sort(key=lambda p: (-p.stat().st_size, str(p.relative_to(repo_dir))))

    # 4. Cap at max_files and max_chars
    target_files = target_files[:max_files]

    file_contents_map: Dict[str, str] = {}
    collected_paths: List[Path] = []
    total_chars = 0

    for path in target_files:
        rel_str = str(path.relative_to(repo_dir))
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        if total_chars + len(content) > max_chars:
            rem = max_chars - total_chars
            if rem > 100:
                content = content[:rem]
                file_contents_map[rel_str] = content
                collected_paths.append(path)
            break
        else:
            file_contents_map[rel_str] = content
            collected_paths.append(path)
            total_chars += len(content)

    return collected_paths, file_contents_map


def build_sdk_api_index(
    repo_dir: Path,
    target_files: List[Path],
    file_contents_map: Dict[str, str]
) -> Dict[str, Any]:
    """
    STEP B: Scan public symbols in SDK core files and check usage in target files.
    """
    repo_dir = repo_dir.resolve()
    target_set = {p.resolve() for p in target_files}

    # Search for SDK core files (outside target files, inside Sources/lib/src or repo root)
    sdk_files: List[Path] = []
    for path in repo_dir.rglob("*"):
        if not path.is_file() or path.resolve() in target_set:
            continue
        rel_parts = path.relative_to(repo_dir).parts
        if any(_is_skip_dir(part, check_markers=True) for part in rel_parts[:-1]):
            continue
        if path.suffix.lower() in ALLOWED_EXTENSIONS:
            sdk_files.append(path)

    # If no separate SDK files, scan all target files or repo files
    if not sdk_files:
        sdk_files = target_files

    # Extract public/export symbols
    symbols_map: Dict[str, str] = {}  # name -> kind

    for path in sdk_files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # Swift / general public regex
        for match in PUBLIC_SYMBOL_REGEX.finditer(text):
            full_stmt = match.group(0)
            sym_name = match.group(1)
            # Find kind (class, struct, enum, protocol, func, var, let)
            kind = "symbol"
            for k in ["class", "struct", "enum", "protocol", "func", "var", "let"]:
                if f" {k} " in f" {full_stmt} ":
                    kind = k
                    break
            symbols_map[sym_name] = kind

        # TS/JS export regex
        for match in EXPORT_SYMBOL_REGEX.finditer(text):
            full_stmt = match.group(0)
            sym_name = match.group(1)
            kind = "symbol"
            for k in ["class", "interface", "type", "enum", "function", "const", "let", "var"]:
                if f" {k} " in f" {full_stmt} ":
                    kind = k
                    break
            symbols_map[sym_name] = kind

    # Check usage in target files
    combined_target_text = "\n".join(file_contents_map.values())
    sdk_apis: List[Dict[str, Any]] = []
    used_count = 0

    for sym_name, kind in symbols_map.items():
        is_used = bool(re.search(r'\b' + re.escape(sym_name) + r'\b', combined_target_text))
        if is_used:
            used_count += 1
        sdk_apis.append({
            "name": sym_name,
            "kind": kind,
            "used_in_demo": is_used
        })

    # Sort APIs: used_in_demo first, then name ascending
    sdk_apis.sort(key=lambda x: (not x["used_in_demo"], x["name"]))

    return {
        "sdk_apis": sdk_apis,
        "used_in_demo": used_count
    }


def extract_project_graph_llm(
    goal: str,
    tech_stack: str,
    sdk_api_index: Dict[str, Any],
    file_contents_map: Dict[str, str]
) -> Dict[str, Any]:
    """
    STEP C: Call LLM to extract Project Graph.
    """
    if not _LLM_AVAILABLE:
        raise RuntimeError("LLM client modules unavailable")

    client, provider, model = get_llm_client()
    if not client:
        raise RuntimeError("Could not initialize LLM client. Check API key/provider settings.")

    used_sdk_apis = [
        api["name"] for api in sdk_api_index.get("sdk_apis", [])
        if api.get("used_in_demo")
    ][:2000]

    system_prompt = (
        "Bạn là kiến trúc sư phần mềm. App người dùng sẽ xây CHÍNH LÀ các files được cung cấp (không phải SDK/lib). "
        "Phân tích chúng thành Project Graph. Mỗi feature kèm: files[] (đường dẫn đúng), api_usage[] (chỉ từ SDK API index đã cho), "
        "keywords[] (thuật ngữ/language feature thật trong files). CẤM bịa file/api. "
        "CẤM tham chiếu nội bộ SDK/lib trừ khi nó xuất hiện trong files đã cho."
    )

    files_text_blocks = []
    for rel_path, content in file_contents_map.items():
        files_text_blocks.append(f"### FILE: {rel_path}\n{content}")
    all_files_str = "\n\n".join(files_text_blocks)

    user_prompt = f"""\
Mục tiêu ứng dụng: {goal}
Công nghệ: {tech_stack}

Danh sách SDK API đã lọc (used_in_demo):
{json.dumps(used_sdk_apis, ensure_ascii=False)}

Mã nguồn các file:
{all_files_str}

Hãy phân tích mã nguồn trên và trả về kết quả JSON theo đúng schema sau:
{{
  "schema_version": 2,
  "project": {{"name": "...", "project_type": "app", "platforms": ["ios"]}},
  "product": {{
    "purpose": "...",
    "features": [
      {{
        "id": "F1",
        "name": "Tên Feature",
        "description": "Mô tả feature",
        "files": ["đường/dẫn/file.swift"],
        "api_usage": ["ChatClient"],
        "keywords": ["@State", "NavigationStack"],
        "platform": "ios"
      }}
    ],
    "user_journeys": [{{"name": "...", "feature_ids": ["F1"]}}]
  }},
  "architecture": {{"layers": [], "services": [], "state_management": "..."}},
  "decomposition": {{"milestones": [{{"id": "M1", "phase": "MVP", "name": "...", "goal": "...", "feature_ids": ["F1"]}}]}}
}}
"""

    result = llm_chat_json(
        client=client,
        model=model,
        system=system_prompt,
        user=user_prompt,
        temperature=0.1,
        max_retries=1
    )

    return result


def verify_project_graph(
    project_graph: Dict[str, Any],
    repo_dir: Path,
    sdk_api_index: Dict[str, Any],
    file_contents_map: Dict[str, str]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    STEP D: Ground-truth verification of project graph against code and SDK API index.
    Removes invalid files, APIs, keywords and logs hallucinations.
    """
    repo_dir = repo_dir.resolve()
    sdk_api_names = {api["name"] for api in sdk_api_index.get("sdk_apis", [])}

    hallucinations: List[Dict[str, Any]] = []

    features = project_graph.get("product", {}).get("features", [])
    for feature in features:
        fid = feature.get("id", "F_UNK")

        # 1. Verify files[]
        valid_files = []
        for f in feature.get("files", []):
            f_path = repo_dir / f
            if f_path.exists() or f in file_contents_map:
                valid_files.append(f)
            else:
                hallucinations.append({
                    "type": "file",
                    "item": f,
                    "feature_id": fid,
                    "reason": f"File '{f}' does not exist in repository"
                })
        feature["files"] = valid_files

        # 2. Verify api_usage[]
        valid_apis = []
        for api in feature.get("api_usage", []):
            if not sdk_api_names or api in sdk_api_names:
                valid_apis.append(api)
            else:
                hallucinations.append({
                    "type": "api",
                    "item": api,
                    "feature_id": fid,
                    "reason": f"API '{api}' not found in SDK API index"
                })
        feature["api_usage"] = valid_apis

        # 3. Verify keywords[]
        valid_kws = []
        for kw in feature.get("keywords", []):
            kw_low = kw.lower()
            # Check in feature's files
            found = False
            for f in valid_files:
                c = file_contents_map.get(f, "")
                if kw_low in c.lower():
                    found = True
                    break
            if not found:
                # Check in any target file
                found = any(kw_low in c.lower() for c in file_contents_map.values())

            if found:
                valid_kws.append(kw)
            else:
                hallucinations.append({
                    "type": "keyword",
                    "item": kw,
                    "feature_id": fid,
                    "reason": f"Keyword '{kw}' not found in target files"
                })
        feature["keywords"] = valid_kws

    return project_graph, hallucinations


def to_upper_snake(term: str) -> str:
    """Helper to convert string term to UPPER_SNAKE_CASE."""
    s = re.sub(r'^[^\w]+', '', term)  # strip leading @ or # etc
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    s = re.sub(r'[^\w]+', '_', s)
    res = s.upper().strip('_')
    return res if res else "CONCEPT"


def escalate_and_map_concepts(
    project_graph: Dict[str, Any],
    file_contents_map: Dict[str, str],
    concept_map_override: Optional[Dict[str, Dict[str, str]]] = None,
    available_concepts: Optional[List[str]] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    STEP E: Escalate keywords/api_usage to neutral concepts and join evidence files.
    Ưu tiên map vào concept ĐÃ CÓ (available_concepts — cùng vocabulary JIT/resolved).
    Chỉ tạo concept mới khi không có concept nào cover keyword.
    """
    all_terms: Set[str] = set()
    features = project_graph.get("product", {}).get("features", [])
    for feature in features:
        all_terms.update(feature.get("api_usage", []))
        all_terms.update(feature.get("keywords", []))

    if not all_terms:
        return {}

    term_list = sorted(list(all_terms))
    llm_results: Dict[str, Dict[str, str]] = {}

    if concept_map_override is not None:
        llm_results = concept_map_override
    else:
        if _LLM_AVAILABLE:
            try:
                client, provider, model = get_llm_client()
                # Danh sách concepts có sẵn (từ resolved_concepts — vocabulary JIT dùng).
                # LLM PHẢI chọn từ đây trước; chỉ tạo concept mới khi thật sự thiếu.
                concept_bank = ", ".join(sorted(available_concepts or [])) or "(rỗng)"
                system_prompt = (
                    "Bạn là chuyên gia phân loại tri thức. Với mỗi keyword/API cụ thể, "
                    "xác định concept trung tính nó thuộc về.\n"
                    f"QUY TẮC:\n"
                    "1. ƯU TIÊN chọn concept ĐÃ CÓ trong danh sách CONCEPT_BANK bên dưới nếu keyword là biểu hiện của concept đó.\n"
                    f"2. CHỈ tạo concept MỚI (UPPER_SNAKE_CASE, KHÔNG kết thúc _CONCEPT, KHÔNG chứa tên công nghệ cụ thể) khi KHÔNG concept nào trong bank cover.\n"
                    "3. CONCEPT_BANK: " + concept_bank[:12000] + "\n"
                    "VD: ChatClient → CHAT_CLIENT_API (hoặc API_INTEGRATION nếu có trong bank), "
                    "@State → LOCAL_VIEW_STATE, URLSession → HTTP_PROTOCOL.\n"
                    "Trả JSON: {\"results\": {\"<keyword>\": {\"concept_code\": \"...\", \"concept_name\": \"...\"}}}"
                )
                user_prompt = (
                    f"Phân loại danh sách keyword/API sau thành concept trung tính (UPPER_SNAKE_CASE):\n"
                    + "\n".join(term_list)
                    + "\n\nTrả về JSON dạng: {\"results\": {\"<keyword>\": {\"concept_code\": \"...\", \"concept_name\": \"...\"}}}"
                )
                res = llm_chat_json(
                    client=client,
                    model=model,
                    system=system_prompt,
                    user=user_prompt,
                    temperature=0.1,
                    max_retries=1
                )
                llm_results = res.get("results", {})
            except Exception as e:
                print(f"[WARN] Concept escalation LLM failed ({e}), using fallback UPPER_SNAKE", file=sys.stderr)

    # Join results into feature_concepts
    feature_concepts: Dict[str, List[Dict[str, Any]]] = {}

    for feature in features:
        fid = feature.get("id", "F_UNK")
        feature_files = feature.get("files", [])
        terms = feature.get("api_usage", []) + feature.get("keywords", [])

        c_items: List[Dict[str, Any]] = []
        seen: Set[str] = set()

        for kw in terms:
            info = llm_results.get(kw, {})
            c_code = info.get("concept_code") or to_upper_snake(kw)
            c_name = info.get("concept_name") or kw

            if c_code in seen:
                continue
            seen.add(c_code)

            # Find evidence_files containing kw
            kw_low = kw.lower()
            ev_files = []
            for f in feature_files:
                c = file_contents_map.get(f, "")
                if kw_low in c.lower():
                    ev_files.append(f)
            if not ev_files:
                ev_files = list(feature_files)

            c_items.append({
                "concept_code": c_code,
                "concept_name": c_name,
                "keyword": kw,
                "evidence_files": ev_files
            })

        feature_concepts[fid] = c_items

    return feature_concepts


def run_pipeline(
    repo_dir: Path,
    output_path: Path,
    goal: str = "",
    tech_stack: str = "",
    target: str = "auto",
    max_files: int = 70,
    max_chars: int = 120000,
    resolved_concepts: Optional[Path] = None,
    escalated_concepts: Optional[Path] = None
) -> Dict[str, Any]:
    """Execute full 5-step pipeline and write output."""
    repo_dir = repo_dir.resolve()

    # STEP A: Collect target files
    target_files, file_contents_map = collect_target_files(
        repo_dir=repo_dir,
        target=target,
        max_files=max_files,
        max_chars=max_chars
    )
    if not target_files:
        raise RuntimeError(f"No source files collected from {repo_dir}")

    # STEP B: Build SDK API Index
    sdk_api_index = build_sdk_api_index(
        repo_dir=repo_dir,
        target_files=target_files,
        file_contents_map=file_contents_map
    )

    # STEP C: Project Graph extraction via LLM
    raw_graph = extract_project_graph_llm(
        goal=goal,
        tech_stack=tech_stack,
        sdk_api_index=sdk_api_index,
        file_contents_map=file_contents_map
    )

    # STEP D: Verify project graph
    verified_graph, hallucinations = verify_project_graph(
        project_graph=raw_graph,
        repo_dir=repo_dir,
        sdk_api_index=sdk_api_index,
        file_contents_map=file_contents_map
    )

    # STEP E: Escalate concepts & map evidence
    # available_concepts: từ resolved_concepts (nếu có) — cùng vocabulary JIT,
    # để feature_concepts khớp concept codes mà JIT sinh LOs (overlap > 0).
    available_concepts = None
    if resolved_concepts and resolved_concepts.is_file():
        try:
            with open(resolved_concepts, "r", encoding="utf-8") as f:
                rc = json.load(f)
            available_concepts = []
            for item in rc.get("resolved", []):
                available_concepts.extend(item.get("concept_codes", []))
            for item in rc.get("proposed", []):
                c = item.get("concept_code") or item.get("concept_codes")
                if isinstance(c, list):
                    available_concepts.extend(c)
                elif c:
                    available_concepts.append(c)
            # Gộp escalated_concepts (step_3_5) — JIT vocabulary = resolved + escalated
            if escalated_concepts and escalated_concepts.is_file():
                with open(escalated_concepts, "r", encoding="utf-8") as f:
                    ec = json.load(f)
                for item in ec.get("escalated", []):
                    c = item.get("concept_code")
                    if c:
                        available_concepts.append(c)
            available_concepts = sorted(set(filter(None, available_concepts)))
            print(f"[*] STEP E dùng {len(available_concepts)} concepts có sẵn (resolved + escalated)")
        except Exception as e:
            print(f"[WARN] Không đọc được resolved_concepts cho concept bank: {e}", file=sys.stderr)

    feature_concepts = escalate_and_map_concepts(
        project_graph=verified_graph,
        file_contents_map=file_contents_map,
        available_concepts=available_concepts
    )

    # Assemble final contract JSON
    final_output = {
        "schema_version": 2,
        "project_graph": verified_graph,
        "sdk_api_index": sdk_api_index,
        "feature_concepts": feature_concepts,
        "hallucinations": hallucinations
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully wrote DemoApp-first project graph to {output_path}")
    return final_output


def main():
    parser = argparse.ArgumentParser(description="DemoApp-first LLM Project Graph Pipeline")
    parser.add_argument("--repo-dir", required=True, type=Path, help="Path to project repository")
    parser.add_argument("--goal", default="", help="Application goal/purpose")
    parser.add_argument("--tech-stack", default="", help="Technologies used")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    parser.add_argument("--target", choices=["auto", "demo_app", "sdk_core"], default="auto", help="Target scanning strategy")
    parser.add_argument("--max-files", type=int, default=70, help="Max files limit")
    parser.add_argument("--max-chars", type=int, default=120000, help="Max total chars limit")
    parser.add_argument("--resolved-concepts", type=Path,
                        help="Optional: resolved_concepts.json — dùng làm concept bank cho STEP E (khớp vocabulary JIT)")
    parser.add_argument("--escalated-concepts", type=Path,
                        help="Optional: escalated_concepts.json — gộp vào concept bank (JIT vocabulary = resolved + escalated)")

    args = parser.parse_args()

    try:
        run_pipeline(
            repo_dir=args.repo_dir,
            output_path=args.output,
            goal=args.goal,
            tech_stack=args.tech_stack,
            target=args.target,
            max_files=args.max_files,
            max_chars=args.max_chars,
            resolved_concepts=args.resolved_concepts,
            escalated_concepts=args.escalated_concepts
        )
    except Exception as e:
        print(f"❌ Error running llm_project_graph: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
