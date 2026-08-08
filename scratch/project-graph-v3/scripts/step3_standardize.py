#!/usr/bin/env python3
"""
STEP 3 — Standardize Concepts: đối chiếu keywords từ Project Graph với concept chuẩn (Knowledge Tree).

Input:
  - project_graph_verified.json (STEP 2)
  - Concept bank: master_tree_embeddings.json (295 concepts, code|name|description)
  - repo_dir (để extract keyword thật từ code)

LLM xử lý MỖI keyword:
  - Match được concept chuẩn (ngữ nghĩa) → MAPPED
  - Không match → UNMAPPED_CONCEPT + đề xuất topic/category (Gap D)

Output: project_graph_standardized.json (điền knowledge_mapping.mappings[])

Usage:
  python step3_standardize.py \
      --project-graph output/project_graph_verified.json \
      --repo-dir /tmp/stream-chat-swift \
      --embeddings ../../.agents/skills/taxonomy-mapper/resources/master_tree_embeddings.json \
      --output output/project_graph_standardized.json
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

# Import Swift parser (từ production scripts — tái sử dụng, không viết lại)
try:
    sys.path.insert(0, str(REPO_ROOT / 'scripts'))
    from extract_project_keywords import parse_swift_file
    _HAS_PARSER = True
except ImportError:
    _HAS_PARSER = False


# ============ KEYWORD EXTRACTION (code, không LLM) ============

def collect_keywords(project_graph: Dict[str, Any], repo_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Thu thập keyword THẬT từ project graph:
    1. PER-NODE keywords (A1): task.keywords[] + feature.api_usage[] + screen.keywords[]
       — gắn node_id để giữ quan hệ task → keyword → concept
    2. imports/framework calls từ code (bổ sung)
    3. evidence OBSERVED
    """
    keywords: Dict[str, Dict[str, Any]] = {}

    # 0. Per-node keywords từ STEP 1 (A1/A2) — GIỮ QUAN HỆ node.
    # LƯU Ý: 1 keyword (VD 'Codable') xuất hiện ở NHIỀU task (t5, t6, t7) —
    # phải giữ node_id của TẤT CẢ, không setdefault (setdefault gán cho task
    # đầu tiên → các task sau mất mapping → UI hiện 'Concept t7').
    for t in project_graph.get("implementation", {}).get("tasks", []):
        node_id = f"task:{t.get('id', '')}"
        for kw in t.get("keywords", []):
            entry = keywords.setdefault(kw, {"source": "task_keyword",
                                             "evidence": {"file": (t.get("source_evidence") or [""])[0]},
                                             "node_ids": set()})
            entry["node_ids"].add(node_id)
    for f in project_graph.get("features", []):
        node_id = f"feature:{f.get('id', '')}"
        for kw in f.get("api_usage", []):
            # api_usage có thể là 'UserDefaults.currentUserId' — lấy token đầu
            base_kw = kw.split(".")[0] if isinstance(kw, str) else kw
            entry = keywords.setdefault(base_kw, {"source": "feature_api_usage",
                                                  "evidence": {},
                                                  "node_ids": set()})
            entry["node_ids"].add(node_id)
    for s in project_graph.get("experience", {}).get("screens", []):
        node_id = f"screen:{s.get('id', '')}"
        for kw in s.get("keywords", []):
            entry = keywords.setdefault(kw, {"source": "screen_keyword",
                                             "evidence": {},
                                             "node_ids": set()})
            entry["node_ids"].add(node_id)

    # 1. Symbols OBSERVED từ evidence (đã verify tồn tại)
    for e in project_graph.get("evidence", {}).get("entries", []):
        sym = e.get("source", {}).get("symbol")
        if sym and e.get("evidence_type") == "OBSERVED":
            keywords[sym] = {"source": "observed", "evidence": e.get("source", {})}

    # 2. Imports + framework calls từ code DemoApp (parse từng file)
    if _HAS_PARSER:
        app_dirs = ["DemoApp", "Example", "App", "app"]
        scan_roots = [repo_dir / d for d in app_dirs if (repo_dir / d).is_dir()]
        if not scan_roots:
            scan_roots = [repo_dir]  # fallback: toàn repo
        for root in scan_roots:
            for f in root.rglob("*.swift"):
                try:
                    res = parse_swift_file(f)
                except Exception:
                    continue
                for imp in res.get("imports", []):
                    keywords.setdefault(imp, {"source": "import", "evidence": {"file": str(f)}})
                for fw in res.get("frameworks_used", []):
                    keywords.setdefault(fw, {"source": "framework_usage", "evidence": {"file": str(f)}})
                for pw in res.get("property_wrappers", []):
                    kw = pw if pw.startswith("@") else f"@{pw}"
                    keywords.setdefault(kw, {"source": "property_wrapper", "evidence": {"file": str(f)}})

    # 3. Framework calls phổ biến (grep code thật — đã chứng minh ChatClient ×8 files)
    common_calls = ["ChatClient", "ChatChannel", "ChatMessage", "URLSession", "UserNotifications",
                    "@State", "@StateObject", "@ObservedObject", "@Binding", "JSONDecoder",
                    "Combine", "Task", "Timer", "DispatchQueue"]
    for root in scan_roots:
        for f in root.rglob("*.swift"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for call in common_calls:
                if call in content:
                    keywords.setdefault(call, {"source": "framework_usage", "evidence": {"file": str(f)}})

    return keywords


# ============ CONCEPT BANK ============

def load_concept_bank(embeddings_path: Path) -> List[Dict[str, str]]:
    """295 concepts từ master_tree_embeddings.json (code|name|description)."""
    data = json.load(open(embeddings_path, encoding="utf-8"))
    concepts = []
    for n in data.get("nodes", []):
        if n.get("level") == "concepts":
            concepts.append({
                "code": n.get("code", ""),
                "name": n.get("name", ""),
                "description": n.get("description", "")[:150],
            })
    return concepts


# ============ STEP 3 LLM ============

def standardize_keywords(keywords: Dict[str, Dict[str, Any]],
                         concept_bank: List[Dict[str, str]]) -> Dict[str, Any]:
    """1 LLM call: map keyword → concept chuẩn. Gap D → đề xuất concept mới."""
    if not _LLM_AVAILABLE:
        raise RuntimeError("LLM không available")

    keyword_list = sorted(keywords.keys())
    bank_str = "\n".join(
        f"{c['code']} | {c['name']} | {c['description'][:100]}" for c in concept_bank
    )

    system = (
        "Bạn là chuyên gia phân loại tri thức. Với mỗi keyword/API/thư viện từ dự án, "
        "xác định concept trung tính nó thuộc về trong Knowledge Tree.\n"
        "QUY TẮC:\n"
        "1. ƯU TIÊN chọn concept CÓ SẴN trong CONCEPT_BANK nếu keyword là biểu hiện của concept đó "
        "(dựa trên ngữ nghĩa, không phải khớp chữ).\n"
        "2. Chỉ khi KHÔNG concept nào trong bank cover, trả status=unmapped + đề xuất concept mới "
        "(code UPPER_SNAKE_CASE, KHÔNG kết thúc _CONCEPT, KHÔNG chứa tên công nghệ cụ thể) "
        "kèm suggested_topic + suggested_category hợp lý.\n"
        "3. VD: ChatClient → API_INTEGRATION, @State → LOCAL_VIEW_STATE, "
        "UserNotifications → LOCAL_NOTIFICATION_API, UIKit → FRONTEND_FRAMEWORKS.\n"
        "Trả JSON: {\"mappings\": [{\"keyword\": \"...\", \"status\": \"mapped|unmapped\", "
        "\"concept_code\": \"...\", \"concept_name\": \"...\", "
        "\"suggested_topic\": \"...\", \"suggested_category\": \"...\", \"reason\": \"...\"}]}"
    )
    user = (
        f"KEYWORDS cần map ({len(keyword_list)}):\n" + "\n".join(f"- {k}" for k in keyword_list) +
        f"\n\nCONCEPT_BANK ({len(concept_bank)} concepts):\n{bank_str}"
    )

    client, _provider, model = get_llm_client()
    res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
    return res


def apply_mappings(project_graph: Dict[str, Any], keywords: Dict[str, Dict[str, Any]],
                   llm_result: Dict[str, Any]) -> Dict[str, Any]:
    """Điền knowledge_mapping.mappings[] vào project graph."""
    result = json.loads(json.dumps(project_graph))
    mappings = llm_result.get("mappings", [])

    knowledge_mappings = []
    for m in mappings:
        kw = m.get("keyword", "")
        info = keywords.get(kw, {})
        status = "MAPPED" if m.get("status") == "mapped" else "UNMAPPED_CONCEPT"
        # 1 keyword → NHIỀU node (t5/t6/t7 cùng 'Codable') → 1 mapping per node,
        # giữ quan hệ task → keyword → concept cho MỌI task, không chỉ task đầu.
        node_ids = info.get("node_ids") or ({info.get("node_id", "")} if info.get("node_id") else set())
        if not node_ids:
            node_ids = {""}
        for nid in sorted(node_ids):
            entry = {
                "project_node": kw,
                "node_id": nid,  # task/feature/screen cụ thể
                "keywords": [kw],
                "concepts": [m.get("concept_code", "")] if m.get("concept_code") else [],
                "status": status,
                "evidence": info.get("evidence", {}),
            }
            if status == "UNMAPPED_CONCEPT":
                entry["suggested_concept"] = {
                    "code": m.get("concept_code", ""),
                    "name": m.get("concept_name", ""),
                    "topic": m.get("suggested_topic", ""),
                    "category": m.get("suggested_category", ""),
                    "reason": m.get("reason", ""),
                }
            knowledge_mappings.append(entry)

    result["knowledge_mapping"] = {"mappings": knowledge_mappings}
    return result


def main():
    parser = argparse.ArgumentParser(description="STEP 3 — Standardize Concepts (LLM đối chiếu concept chuẩn)")
    parser.add_argument("--project-graph", required=True, type=Path)
    parser.add_argument("--repo-dir", required=True, type=Path)
    parser.add_argument("--embeddings", required=True, type=Path, help="master_tree_embeddings.json")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    pg = json.load(open(args.project_graph, encoding="utf-8"))
    bank = load_concept_bank(args.embeddings)
    print(f"[*] Concept bank: {len(bank)} concepts")

    keywords = collect_keywords(pg, args.repo_dir)
    print(f"[*] Keywords từ project graph + code: {len(keywords)}")
    print(f"    {sorted(keywords.keys())[:15]}...")

    llm_res = standardize_keywords(keywords, bank)
    result = apply_mappings(pg, keywords, llm_res)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    mappings = result["knowledge_mapping"]["mappings"]
    mapped = [m for m in mappings if m["status"] == "MAPPED"]
    unmapped = [m for m in mappings if m["status"] == "UNMAPPED_CONCEPT"]
    print(f"[✓] Standardized: {len(mappings)} mappings | {len(mapped)} MAPPED | {len(unmapped)} UNMAPPED (Gap D)")
    for m in mapped[:5]:
        print(f"    ✓ {m['keywords'][0]} → {m['concepts']}")
    for m in unmapped[:5]:
        print(f"    ? {m['keywords'][0]} → đề xuất {m.get('suggested_concept', {}).get('code')}")
    print(f"    → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
