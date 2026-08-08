#!/usr/bin/env python3
"""
STEP 4 — Task-aware Roadmap: Project Graph (canonical v3) → roadmap.json.

Compile Project Graph + knowledge_mapping thành roadmap task-aware:
  1. Mỗi task → tập concepts (từ knowledge_mapping, giữ node_id)
  2. Sắp xếp task theo task_dependencies (topo sort)
  3. Chia phase theo feature.priority (core→MVP, supporting→EXTEND, optional/polish→POLISH)
  4. JIT sinh LO per-task (LLM) — dùng intent + outcome + keywords + concepts
  5. Gắn validation làm assessment

Input: project_graph_standardized.json (STEP 3)
Output: roadmap.json (phases → milestones → tasks → LOs)

Usage:
  python step4_roadmap.py \
      --project-graph output/project_graph_standardized.json \
      --output output/roadmap.json \
      [--skip-jit]   # bỏ qua LLM (test cấu trúc), dùng desc mô tả sẵn
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False


# Phase theo feature priority
PRIORITY_PHASE = {
    "core": "MVP",
    "supporting": "EXTEND",
    "optional": "POLISH",
    "polish": "POLISH",
}
PHASE_ORDER = {"FOUNDATION": 0, "MVP": 1, "EXTEND": 2, "POLISH": 3}


def task_concepts(task: Dict, mappings: List[Dict]) -> List[str]:
    """Concepts của task từ knowledge_mapping (giữ node_id)."""
    node_id = f"task:{task.get('id', '')}"
    concepts = []
    for m in mappings:
        if m.get("node_id") == node_id and m.get("status") == "MAPPED":
            for c in m.get("concepts", []):
                if c and c not in concepts:
                    concepts.append(c)
    return concepts


def normalize_capability_id(task_cap_id: str, capabilities: List[Dict]) -> str:
    """Map task.capability_id (VD 'channel-list') → capability.id (VD 'CAP-CHANNEL-BROWSING')
    qua token chung (snake → UPPER + prefix CAP-). STEP 1 có thể sinh 2 convention id khác nhau
    giữa Call A (capabilities) và Call C (tasks) — chuẩn hoá ở đây."""
    norm = task_cap_id.replace("-", "_").replace(" ", "_").upper()
    # 0. Exact match sau normalize
    for cap in capabilities:
        if cap.get("id", "") == norm or cap.get("id", "") == f"CAP_{norm}":
            return cap["id"]
    # 1. Map thủ công các capability_id phổ biến (nền tảng — không phụ thuộc project).
    # Key UPPERCASE (norm), value format CAP-XXX (dash — khớp caps id thật).
    COMMON = {
        "APP_LIFECYCLE": "CAP-LOGIN", "SESSION_AUTH": "CAP-LOGIN",
        "SESSION_CONTROL": "CAP-LOGIN", "UI_UTILS": "CAP-LOGIN",
        "STATE_MANAGEMENT": "CAP-SESSION-ACTIONS", "SESSION_PERSISTENCE": "CAP-SESSION-ACTIONS",
        "CHANNEL_LIST": "CAP-CHANNEL-BROWSING", "MESSAGE_THREAD": "CAP-MESSAGING",
        "MESSAGE_CUSTOMIZATION": "CAP-MESSAGING", "IMAGE_HANDLING": "CAP-MESSAGING",
        "PUSH_NOTIFICATIONS": "CAP-PUSH", "USER_MANAGEMENT": "CAP-PROFILE",
        "OBSERVABILITY": "CAP-DEVMODE", "DEVMODE": "CAP-DEVMODE",
        "ACCESSIBILITY": "CAP-ACCESSIBILITY",
    }
    if norm in COMMON:
        target = COMMON[norm]
        for cap in capabilities:
            if cap.get("id", "") == target:
                return cap["id"]
        cap_id = COMMON[norm]
        for cap in capabilities:
            if cap.get("id", "").replace("-", "_") == cap_id:
                return cap["id"]
    # 2. Token overlap với purpose (nhiều token trùng → gần nhau)
    toks = set(norm.split("_"))
    best, best_score = "", 0
    for cap in capabilities:
        cap_text = (cap.get("id", "") + " " + cap.get("purpose", "")).upper().replace("-", "_")
        score = sum(1 for t in toks if t and len(t) > 3 and t in cap_text)
        if score > best_score:
            best, best_score = cap["id"], score
    return best if best_score > 0 else ""


def task_phase_from_requirements(task: Dict, requirements: List[Dict]) -> str:
    """M3 (cross-feature): phase từ completion_level của requirement mà task thực hiện.
    Ưu tiên: mọi requirement của task cùng completion_level → dùng level đó.
    Khác level → lấy level cao nhất (task hoàn thành nhiều mức).
    Không có requirement_ids → fallback '' (dùng feature.priority)."""
    req_ids = task.get("requirement_ids", [])
    if not req_ids:
        return ""
    levels = []
    for r in requirements:
        if r.get("id") in req_ids and r.get("completion_level"):
            levels.append(r["completion_level"])
    if not levels:
        return ""
    # Mức cao nhất (polish > extend > mvp > base)
    order = {"base": 0, "mvp": 1, "extend": 2, "polish": 3}
    best = max(levels, key=lambda l: order.get(l, 1))
    return best


def task_phase(task: Dict, features_by_capability: Dict[str, str]) -> str:
    """Phase từ feature.priority của capability task thuộc."""
    cap_id = task.get("capability_id", "")
    feat_id = features_by_capability.get(cap_id, "")
    # fallback: không có → MVP
    return PRIORITY_PHASE.get(feat_id, "MVP")


def topo_sort_tasks(tasks: List[Dict], dependencies: List[Dict]) -> List[Dict]:
    """Sắp xếp task theo dependency (DEPENDS_ON/BLOCKED_BY trước task phụ thuộc)."""
    task_map = {t["id"]: t for t in tasks}
    dep_map: Dict[str, Set[str]] = defaultdict(set)  # task → tasks nó phụ thuộc
    for d in dependencies:
        frm, to = d.get("from", ""), d.get("to", "")
        if frm in task_map and to in task_map:
            dep_map[frm].add(to)  # frm cần to trước

    result, visited, visiting = [], set(), set()

    def dfs(tid):
        if tid in visited:
            return
        if tid in visiting:
            return  # cycle — bỏ
        visiting.add(tid)
        for dep in sorted(dep_map.get(tid, [])):
            dfs(dep)
        visiting.discard(tid)
        visited.add(tid)
        result.append(tid)

    for t in sorted(task_map.keys()):
        dfs(t)
    return [task_map[tid] for tid in result]


def build_roadmap_structure(pg: Dict) -> Dict:
    """Xây roadmap structure (không LLM): phases → milestones(task) → concepts."""
    mappings = pg.get("knowledge_mapping", {}).get("mappings", [])
    tasks = pg.get("implementation", {}).get("tasks", [])
    deps = pg.get("implementation", {}).get("task_dependencies", [])
    features = pg.get("features", [])
    caps = pg.get("capabilities", [])
    requirements = pg.get("product", {}).get("requirements", [])

    # feature.priority theo capability (chuẩn hoá id nếu lệch convention)
    cap_feat = {c.get("id", ""): c.get("feature_id", "") for c in caps}
    feat_priority = {f.get("id", ""): f.get("priority", "core") for f in features}

    # Foundation tasks: setup/lifecycle/entry-point — NHẬN DIỆN từ action (không phụ thuộc feature priority)
    FOUNDATION_SIGNALS = ["appdelegate", "entry point", "@main", "diagnostics", "configure sentry",
                          "configure third-party", "initial setup", "setup"]

    ordered = topo_sort_tasks(tasks, deps)

    phases: Dict[str, List] = defaultdict(list)
    for i, t in enumerate(ordered):
        cap_id = normalize_capability_id(t.get("capability_id", ""), caps)
        feat_id = cap_feat.get(cap_id, "")
        priority = feat_priority.get(feat_id, "core")
        action_lower = (t.get("action", "") or "").lower()

        # M3 (cross-feature): ưu tiên completion_level từ requirement,
        # rồi FOUNDATION signal (scaffold), rồi feature.priority (fallback)
        completion = task_phase_from_requirements(t, requirements)
        if completion:
            phase = {"base": "FOUNDATION", "mvp": "MVP",
                     "extend": "EXTEND", "polish": "POLISH"}.get(completion, "MVP")
        elif any(sig in action_lower for sig in FOUNDATION_SIGNALS):
            phase = "FOUNDATION"
        else:
            phase = PRIORITY_PHASE.get(priority, "MVP")

        concepts = task_concepts(t, mappings)
        phases[phase].append({
            "task": t,
            "concepts": concepts,
            "order": i,
        })

    # POLISH tasks tự sinh từ missing_gaps + tech_debt (feature F6 + quality)
    polish_extra = []
    order_base = len(ordered)
    for idx, g in enumerate(pg.get("implementation", {}).get("missing_gaps", [])):
        polish_extra.append({
            "task": {
                "id": f"polish-gap-{idx+1}",
                "capability_id": "",
                "action": f"Khắc phục: {g.get('gap', '')[:100]}",
                "intent": f"Cải thiện chất lượng: {g.get('gap', '')[:80]}",
                "outcome": {"user_visible": g.get('suggested_lo', '')},
                "keywords": [],
                "source_evidence": [g.get('location', '')] if g.get('location') else [],
            },
            "concepts": [],
            "order": order_base + idx,
        })
    n_gaps = len(polish_extra)
    for idx, d in enumerate(pg.get("implementation", {}).get("tech_debt", [])):
        polish_extra.append({
            "task": {
                "id": f"polish-debt-{idx+1}",
                "capability_id": "",
                "action": f"Refactor: {d.get('issue', '')[:100]}",
                "intent": f"Giảm tech debt: {d.get('issue', '')[:80]}",
                "outcome": {"user_visible": d.get('suggested_phase', 'POLISH')},
                "keywords": [],
                "source_evidence": [d.get('location', '')] if d.get('location') else [],
            },
            "concepts": [],
            "order": order_base + n_gaps + idx,
        })
    phases["POLISH"].extend(polish_extra)

    result = {"schema_version": 3, "phases": []}
    for phase_name in sorted(phases.keys(), key=lambda p: PHASE_ORDER.get(p, 9)):
        items = sorted(phases[phase_name], key=lambda x: x["order"])
        result["phases"].append({
            "phase": phase_name,
            "milestones": items,
        })
    return result


def generate_task_lo(task: Dict, concepts: List[str], validations: List[Dict]) -> List[Dict]:
    """Sinh LO cho 1 task (LLM) — intent/outcome/keywords/concepts làm context."""
    if not _LLM_AVAILABLE:
        return [{
            "task_id": task.get("id"),
            "concepts": concepts,
            "lo": f"[no-llm] {task.get('action', '')}",
        }]

    val = [v for v in validations if v.get("target") == task.get("id", "")]
    system = (
        "Bạn là chuyên gia sư phạm. Sinh Learning Objectives (LO) cho MỘT implementation task "
        "trong roadmap học-by-building.\n"
        "Mỗi LO: câu bắt đầu 'Người học có khả năng', kèm bloom_level (UNDERSTAND/APPLY/ANALYZE/CREATE) "
        "và lo_type (UNIVERSAL/CONCEPTUAL_IMPL/SPECIFIC_IMPL).\n"
        "Gắn LO vào CONCEPT đã cho (concept_code), KHÔNG tạo concept mới.\n"
        "Trả JSON: {\"los\": [{\"description\": \"...\", \"bloom_level\": \"...\", "
        "\"lo_type\": \"...\", \"concept_code\": \"...\", \"keyword\": \"...\"}]}"
    )
    user = (
        f"TASK: {task.get('action', '')}\n"
        f"INTENT (WHY): {task.get('intent', '')}\n"
        f"OUTCOME: {task.get('outcome', {}).get('user_visible', '')}\n"
        f"KEYWORDS: {task.get('keywords', [])}\n"
        f"CONCEPTS (chọn concept_code từ đây): {concepts}\n"
        f"ACCEPTANCE: {task.get('acceptance', [])}\n"
        f"VALIDATION: {[v.get('criteria', []) for v in val]}\n"
        f"EFFORT: {task.get('effort', {})}\n"
        "Sinh 2-4 LO bao phủ khái niệm + thực hành của task."
    )
    try:
        client, _p, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
        los = res.get("los", [])
        return [{"task_id": task.get("id"), **lo} for lo in los]
    except Exception as e:
        print(f"[WARN] LLM fail task {task.get('id')}: {e}", file=sys.stderr)
        return [{"task_id": task.get("id"), "concepts": concepts,
                 "lo": f"[fallback] {task.get('action', '')}"}]


def main():
    parser = argparse.ArgumentParser(description="STEP 4 — Task-aware Roadmap")
    parser.add_argument("--project-graph", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--skip-jit", action="store_true", help="Bỏ qua LLM (test cấu trúc)")
    args = parser.parse_args()

    pg = json.load(open(args.project_graph, encoding="utf-8"))
    structure = build_roadmap_structure(pg)

    validations = pg.get("validation", {}).get("validations", [])
    if args.skip_jit:
        for phase in structure["phases"]:
            for m in phase["milestones"]:
                m["los"] = [{"task_id": m["task"]["id"], "concepts": m["concepts"],
                             "lo": f"[skip-jit] {m['task']['action']}"}]
    else:
        for phase in structure["phases"]:
            for m in phase["milestones"]:
                print(f"[*] Sinh LO: {m['task']['id']} ({m['task']['action'][:40]}...)")
                m["los"] = generate_task_lo(m["task"], m["concepts"], validations)

    # Đóng gói output
    roadmap = {
        "project": pg.get("project", {}),
        "phases": structure["phases"],
        "total_tasks": sum(len(p["milestones"]) for p in structure["phases"]),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Roadmap → {args.output}")
    for phase in roadmap["phases"]:
        n = len(phase["milestones"])
        n_lo = sum(len(m.get("los", [])) for m in phase["milestones"])
        print(f"    {phase['phase']}: {n} tasks, {n_lo} LOs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
