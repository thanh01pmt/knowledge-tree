#!/usr/bin/env python3
"""
extract_project_graph.py — Extract Product/Architecture Graph from source code (Phase B1)

Usage:
    python scripts/extract_project_graph.py --repo-dir path/to/repo --output output.json [--tech-stack "SwiftUI, ESP32"] [--max-files 8] [--max-chars 20000]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    from openai import OpenAI
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / '.env')

SKIP_DIRS = {
    "node_modules", ".build", "Pods", ".git", ".venv", "venv",
    "__pycache__", "build", "dist", ".idea", ".vscode"
}
# Directory-name substrings that indicate non-core code (tests, demos, samples).
# Matched case-insensitively against each path part so that real repos with
# large test/demo folders don't dominate the "biggest files" selection.
SKIP_NAME_MARKERS = {
    "test", "demo", "sample", "example", "playground", "fixture",
    "docc", "docs", "readme", "integration", "mock", "stub"
}


def _is_skip_dir(name: str) -> bool:
    """True if a directory name should be skipped (core-code extraction)."""
    if name in SKIP_DIRS:
        return True
    lowered = name.lower()
    return any(marker in lowered for marker in SKIP_NAME_MARKERS)

ALLOWED_EXTENSIONS = {".swift", ".py", ".ino", ".cpp", ".h", ".js", ".ts"}

SCHEMA_SPEC = {
    "schema_version": 1,
    "project": {
        "name": "str",
        "project_type": "app|cli|library|api_service|firmware|multi_target",
        "platforms": ["app", "esp32"]
    },
    "product": {
        "purpose": "str",
        "features": [{
            "id": "F1",
            "name": "str",
            "description": "str",
            "files": ["str"],
            "platform": "app|esp32"
        }],
        "user_journeys": [{
            "name": "str",
            "feature_ids": ["str"]
        }]
    },
    "architecture": {
        "layers": [{
            "name": "str",
            "component_names": ["str"]
        }],
        "services": [{
            "name": "str",
            "file": "str",
            "responsibility": "str"
        }],
        "state_management": "str",
        "communication": [{
            "from": "str",
            "to": "str",
            "protocol": "HTTP|MQTT|WiFi|..."
        }]
    },
    "decomposition": {
        "milestones": [{
            "id": "M1",
            "phase": "MVP|EXTEND|POLISH",
            "name": "str",
            "goal": "str",
            "feature_ids": ["str"],
            "files": ["str"],
            "acceptance": "str",
            "depends_on": ["str"]
        }]
    }
}


def collect_repo_files(repo_dir: Path, max_files: int = 8) -> List[Path]:
    """
    Walk repo_dir, collect source files (.swift, .py, .ino, .cpp, .h, .js, .ts).
    Skip directories like node_modules, .build, Pods, .git, etc.
    Prioritize .swift and .ino files, then sort by file size descending.
    Returns up to max_files paths.
    """
    repo_dir = repo_dir.resolve()
    collected: List[Tuple[int, int, str, Path]] = []

    for path in repo_dir.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(repo_dir).parts
        if any(_is_skip_dir(part) for part in rel_parts[:-1]):
            continue
        ext = path.suffix.lower()
        if ext in ALLOWED_EXTENSIONS:
            # Priority: .swift and .ino first (score 2), others 1
            priority_score = 2 if ext in {".swift", ".ino"} else 1
            size = path.stat().st_size
            rel_str = str(path.relative_to(repo_dir))
            collected.append((priority_score, size, rel_str, path))

    # Sort descending by priority_score, then size, then relative path
    collected.sort(key=lambda item: (-item[0], -item[1], item[2]))
    return [path for _, _, _, path in collected[:max_files]]


def load_and_cap_file_contents(repo_dir: Path, file_paths: List[Path], max_chars: int = 20000) -> str:
    """
    Read contents of file_paths, format with file headers, and cap total string to max_chars.
    """
    repo_dir = repo_dir.resolve()
    chunks: List[str] = []
    current_chars = 0

    for path in file_paths:
        if current_chars >= max_chars:
            break
        try:
            rel_path = path.relative_to(repo_dir)
        except ValueError:
            rel_path = path.name

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        header = f"=== File: {rel_path} ===\n"
        content_block = header + text + "\n\n"

        if current_chars + len(content_block) > max_chars:
            remaining = max_chars - current_chars
            chunks.append(content_block[:remaining])
            current_chars = max_chars
            break
        else:
            chunks.append(content_block)
            current_chars += len(content_block)

    return "".join(chunks)


def validate_shape(data: Any) -> bool:
    """
    Validate that data contains required top-level keys and structure for Project Graph:
    keys: project, product, architecture, decomposition
    features in product must be a list
    milestones in decomposition must be a list
    """
    if not isinstance(data, dict):
        return False

    required_keys = {"project", "product", "architecture", "decomposition"}
    if not required_keys.issubset(data.keys()):
        return False

    project = data.get("project")
    if not isinstance(project, dict):
        return False
    if not {"name", "project_type", "platforms"}.issubset(project.keys()):
        return False

    product = data.get("product")
    if not isinstance(product, dict):
        return False
    if "features" not in product or not isinstance(product.get("features"), list):
        return False

    architecture = data.get("architecture")
    if not isinstance(architecture, dict):
        return False
    if not {"layers", "services", "state_management", "communication"}.issubset(architecture.keys()):
        return False

    decomposition = data.get("decomposition")
    if not isinstance(decomposition, dict):
        return False
    if "milestones" not in decomposition or not isinstance(decomposition.get("milestones"), list):
        return False

    return True


def build_prompt(file_contents: str, tech_stack: str = "") -> Tuple[str, str]:
    """
    Build system and user prompts for LLM.
    MUST NOT include Knowledge Tree or pedagogical concepts.
    """
    system_prompt = (
        "Bạn là kiến trúc sư phần mềm. Phân tích source code thành Product/Architecture Graph theo schema JSON. "
        "CẤM bịa file/symbol/tính năng không thấy trong code. "
        "KHÔNG tham chiếu danh mục kiến thức bên ngoài nào. "
        "Trả JSON đúng schema.\n"
        "QUAN TRỌNG về file:\n"
        "1. Mỗi feature (F1, F2...) phải liệt kê ĐÚNG tất cả source files thực hiện chức năng đó. "
        "Một feature thường dùng NHIỀU files (không bao giờ chỉ 1 file trừ khi repo thật sự nhỏ).\n"
        "2. Một file có thể xuất hiện trong NHIỀU features nếu nó phục vụ nhiều chức năng — đó là bình thường.\n"
        "3. Mọi file quan trọng đã đọc phải xuất hiện trong ít nhất 1 feature — không bỏ sót file.\n"
        "4. CẤM đặt tất cả features vào cùng 1 file khi có nhiều file khác nhau.\n"
        "5. decomposition.milestones[].files = union của feature_ids[].files."
    )

    schema_str = json.dumps(SCHEMA_SPEC, indent=2, ensure_ascii=False)

    user_parts = [
        "Hãy phân tích source code bên dưới và trả về JSON Product/Architecture Graph theo đúng JSON Schema sau:\n",
        f"```json\n{schema_str}\n```\n"
    ]

    if tech_stack:
        user_parts.append(f"Tech Stack gợi ý: {tech_stack}\n")

    user_parts.append("Source Code Files:\n")
    user_parts.append(file_contents)
    user_parts.append("\nTrả về JSON hợp lệ theo đúng schema trên.")

    user_prompt = "\n".join(user_parts)
    return system_prompt, user_prompt


def main():
    parser = argparse.ArgumentParser(description="Extract Product Graph from repository source code.")
    parser.add_argument("--repo-dir", required=True, type=Path, help="Path to repository root")
    parser.add_argument("--output", required=True, type=Path, help="Path to write output JSON")
    parser.add_argument("--tech-stack", default="", type=str, help="Optional tech stack description")
    parser.add_argument("--max-files", default=8, type=int, help="Maximum number of files to process (default: 8)")
    parser.add_argument("--max-chars", default=20000, type=int, help="Maximum total characters of code content (default: 20000)")

    args = parser.parse_args()

    repo_dir: Path = args.repo_dir
    output_path: Path = args.output

    if not repo_dir.exists() or not repo_dir.is_dir():
        print(f"[ERROR] repo-dir does not exist or is not a directory: {repo_dir}", file=sys.stderr)
        sys.exit(1)

    # 1. Collect files
    file_paths = collect_repo_files(repo_dir, max_files=args.max_files)
    if not file_paths:
        print(f"[ERROR] No matching source code files found in {repo_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Selected {len(file_paths)} files from {repo_dir}: {[f.name for f in file_paths]}")

    # 2. Read and cap contents
    file_contents = load_and_cap_file_contents(repo_dir, file_paths, max_chars=args.max_chars)
    if not file_contents.strip():
        print(f"[ERROR] Empty file contents after loading and capping.", file=sys.stderr)
        sys.exit(1)

    # 3. Check LLM availability
    if not _LLM_AVAILABLE:
        print("[ERROR] LLM client / dependencies not available", file=sys.stderr)
        sys.exit(1)

    client, provider, model = get_llm_client()
    if not client:
        print("[ERROR] Could not initialize LLM client. Check environment / API keys.", file=sys.stderr)
        sys.exit(1)

    system_prompt, user_prompt = build_prompt(file_contents, tech_stack=args.tech_stack)

    # 4. Call LLM with JSON mode and max_retries=1
    print(f"[INFO] Calling LLM ({provider} / {model})...")
    try:
        result = llm_chat_json(
            client=client,
            model=model,
            system=system_prompt,
            user=user_prompt,
            temperature=0.2,
            max_retries=1
        )
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Validate shape
    if not validate_shape(result):
        print("[ERROR] LLM response failed shape validation", file=sys.stderr)
        sys.exit(1)

    result.setdefault("schema_version", 1)

    # 6. Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[SUCCESS] Wrote project graph to {output_path}")


if __name__ == "__main__":
    main()
