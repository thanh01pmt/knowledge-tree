#!/usr/bin/env python3
"""
STEP 0b — Tree Advisor: LLM đọc tree map → quyết định file types cần collect.

Lý do: người học/xác định tech stack từ TREE (không phải hardcode). LLM nhìn
cây thư mục → đánh giá techstack THẬT của project → trả các extension cần
collect nội dung (bỏ assets/config/build rác).

Input: project_structure.txt (tree map từ git_tracker --initial-scan)
Output: file_types_profile.json
  {
    "tech_stack": ["Swift", "SwiftUI", "Firebase"],
    "extensions": [".swift"],
    "include_dirs": ["Talky"],
    "exclude_dirs": ["Assets.xcassets", "*.colorset"],
    "reasoning": "..."
  }

Usage:
  python step0b_tree_advisor.py \
      --tree output/talky-step0/project_structure.txt \
      --goal "Xây app chat iOS SwiftUI" \
      --output output/talky-step0/file_types_profile.json
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False


def main():
    parser = argparse.ArgumentParser(description="STEP 0b — Tree Advisor: LLM chọn file types từ tree")
    parser.add_argument("--tree", required=True, type=Path, help="project_structure.txt từ git_tracker")
    parser.add_argument("--goal", default="", help="Goal của learner (để LLM đối chiếu tech stack)")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.tree.is_file():
        print(f"❌ Tree file không tồn tại: {args.tree}", file=sys.stderr)
        sys.exit(1)

    tree = args.tree.read_text(encoding="utf-8", errors="ignore")
    # Cắt tree nếu quá lớn (chỉ cần cấu trúc, không cần toàn bộ)
    if len(tree) > 30000:
        tree = tree[:30000] + "\n... (truncated — cấu trúc đủ để đánh giá)"

    if not _LLM_AVAILABLE:
        print("❌ LLM không available", file=sys.stderr)
        sys.exit(1)

    system = (
        "You are a software project structure analyst.\n"
        "Look at the TREE MAP of a project (directory + file tree) and determine:\n"
        "1. The ACTUAL tech_stack of the project (language, framework, libraries) — cross-check against the learner goal if provided.\n"
        "2. extensions: the CODE file extensions whose content should be collected (e.g. ['.swift'], ['.ts','.tsx'], ['.py']). "
        "EXCLUDE build/config/asset files (e.g. .json Contents, .png, .plist, .xcassets).\n"
        "3. include_dirs: the main code directories (e.g. 'Talky', 'src').\n"
        "4. exclude_dirs: directories NOT needed (assets, build, node_modules, *.colorset...).\n"
        "Return JSON: {\"tech_stack\": [], \"extensions\": [], \"include_dirs\": [], "
        "\"exclude_dirs\": [], \"reasoning\": \"...\"}"
    )
    user = (
        f"LEARNER GOAL: {args.goal or '(none)'}\n\n"
        f"PROJECT TREE MAP:\n{tree}\n\n"
        "Return JSON matching the schema above. extensions must be real code file extensions (with a leading dot)."
    )

    try:
        client, _provider, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
    except Exception as e:
        print(f"❌ LLM fail: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate output tối thiểu
    if not res.get("extensions"):
        print(f"❌ LLM không trả extensions: {res}", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)

    print(f"[✓] Tree Advisor: tech_stack={res.get('tech_stack')} | "
          f"extensions={res.get('extensions')} | include={res.get('include_dirs')}")
    print(f"    exclude={res.get('exclude_dirs')}")
    print(f"    → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
