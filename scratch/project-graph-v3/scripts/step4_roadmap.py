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
import re
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


def polish_concepts(gap_or_debt: Dict, mappings: List[Dict], features: List[Dict],
                    impl_tasks: List[Dict] = None) -> List[str]:
    """Map concept cho polish tasks (gap/debt) — chúng không có node riêng trong knowledge_mapping.

    Chiến lược:
    1. gap: feature_id → concepts của feature node (nếu feature đã MAPPED), fallback screen node
    2. debt: location file → task nào có source_evidence chứa file đó → concepts của task node
    3. Fallback: tìm node khác (task/feature/screen) có keyword trùng từ nội dung text
    """
    concepts = []

    # 1. Qua feature_id (gap có) — feature node + screen node tương ứng
    fid = gap_or_debt.get("feature_id", "")
    if fid:
        for m in mappings:
            if m.get("node_id") == f"feature:{fid}" and m.get("status") == "MAPPED":
                for c in m.get("concepts", []):
                    if c and c not in concepts:
                        concepts.append(c)
        # Fallback: feature không có node → tìm screen node khớp tên feature
        if not concepts:
            # F-RECENT → screen_recent_chat (bỏ prefix F-, lowercase, -/→ _)
            stem = fid.lower().replace("f-", "").replace("-", "_").replace("_", "")
            for m in mappings:
                nid = m.get("node_id", "")
                if nid.startswith("screen:"):
                    screen_stem = nid.replace("screen:", "").replace("_", "")
                    if stem in screen_stem and m.get("status") == "MAPPED":
                        for c in m.get("concepts", []):
                            if c and c not in concepts:
                                concepts.append(c)

    # 2. Qua location file (debt có) — tìm task node có source_evidence chứa file
    loc = gap_or_debt.get("location", "")
    if loc and impl_tasks:
        matched_task_ids = {
            t.get("id") for t in impl_tasks
            if loc in (t.get("source_evidence", []) or []) or loc in (t.get("modifies", []) or [])
        }
        for tid in matched_task_ids:
            for m in mappings:
                if m.get("node_id") == f"task:{tid}" and m.get("status") == "MAPPED":
                    for c in m.get("concepts", []):
                        if c and c not in concepts:
                            concepts.append(c)

    # 3. Fallback: keyword overlap với text gap/debt
    if not concepts:
        text = f"{gap_or_debt.get('gap', '')} {gap_or_debt.get('issue', '')} {gap_or_debt.get('suggested_lo', '')}".lower()
        for m in mappings:
            if m.get("status") != "MAPPED":
                continue
            kw = (m.get("keyword") or "").lower()
            if kw and kw in text:
                for c in m.get("concepts", []):
                    if c and c not in concepts:
                        concepts.append(c)

    return concepts[:3]  # giới hạn 3 concept/polish task


def normalize_capability_id(task_cap_id: str, capabilities: List[Dict]) -> str:
    """Map task.capability_id → capability.id.

    STEP 1 Call C sinh task.capability_id với 2 convention lẫn lộn:
    - Feature id trực tiếp: 'F-CORE', 'F-AUTH' (dùng thẳng — feature là cha)
    - Capability id: 'cap_bootstrap', 'CAP-CHANNEL-BROWSING', 'channel-list'
    Hàm chuẩn hoá: trả capability.id nếu khớp; F-XXX giữ nguyên (feature id).
    """
    if not task_cap_id:
        return ""

    # 0. Đã là feature id (F-XXX) → giữ nguyên
    if re.match(r"^F[-_]", task_cap_id):
        return task_cap_id

    norm = task_cap_id.replace("-", "_").replace(" ", "_").upper()
    # 1. Exact match sau normalize (cap_xxx / CAP-XXX / CAP_XXX)
    for cap in capabilities:
        if cap.get("id", "").replace("-", "_").upper() == norm:
            return cap["id"]
        if cap.get("id", "") == norm or cap.get("id", "") == f"CAP_{norm}":
            return cap["id"]
    # 2. Map thủ công các capability_id phổ biến (nền tảng — không phụ thuộc project).
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
            if cap.get("id", "") == target or cap.get("id", "").replace("-", "_") == target:
                return cap["id"]
    # 3. Token overlap với purpose (nhiều token trùng → gần nhau)
    toks = set(norm.split("_"))
    best, best_score = "", 0
    for cap in capabilities:
        cap_text = (cap.get("id", "") + " " + cap.get("purpose", "")).upper().replace("-", "_")
        score = sum(1 for t in toks if t and len(t) > 3 and t in cap_text)
        if score > best_score:
            best, best_score = cap["id"], score
    return best if best_score > 0 else ""


def task_phase_from_stages(task: Dict, stages: list) -> str:
    """M4-narrative: phase task từ development_stages (LLM narrative — đúng logic
    học tập: UI trước, backend sau) thay vì completion_level công thức.

    Map bằng keyword overlap giữa task.action và stage.need/product_state.
    Task không khớp stage nào → '' (dùng fallback completion_level).
    """
    if not stages:
        return ""
    action = (task.get("action", "") + " " + task.get("intent", "")).lower()
    # Token hữu ích từ action (bỏ từ chung)
    STOP = {"implement", "với", "và", "của", "trong", "cho", "theo", "để",
            "các", "một", "không", "có", "được", "sau", "khi", "từ"}
    toks = {t for t in action.replace("-", " ").replace("/", " ").split() if len(t) > 2 and t not in STOP}

    best_stage, best_score = "", 0
    for i, s in enumerate(stages):
        text = " ".join(s.get("need", []) + [s.get("product_state", "")]).lower()
        score = sum(1 for t in toks if t in text)
        if score > best_score:
            best_stage, best_score = s.get("stage", f"stage-{i+1}"), score
    return best_stage if best_score >= 2 else ""


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


def topo_sort_tasks(tasks: List[Dict], dependencies: List[Dict],
                    task_journey_rank: dict = None) -> List[Dict]:
    """Sắp xếp task theo dependency (DEPENDS_ON/BLOCKED_BY trước task phụ thuộc).

    task_journey_rank: {task_id: journey_rank} — task thuộc user journey sớm hơn
    (VD J1 Welcome → J2 Login → J3 Chat) được ưu tiên trước khi cùng dependency.
    """
    task_map = {t["id"]: t for t in tasks}
    dep_map: Dict[str, Set[str]] = defaultdict(set)  # task → tasks nó phụ thuộc
    # Ưu tiên task.depends_on (field trên task — sinh cùng task, tin cậy hơn
    # edge list riêng mà STEP 1 có thể viết ngược ý from/to).
    for t in tasks:
        for dep in t.get("depends_on", []) or []:
            if dep in task_map and dep != t["id"]:
                dep_map[t["id"]].add(dep)
    # Bổ sung từ edge list — CHỈ edge nào KHÔNG mâu thuẫn: nếu task đã có dep khác
    # với cùng "ý", edge chỉ thêm dep chưa có. Edge ngược (task A "cần" B mà B
    # thực ra cần A theo task.depends_on) bị bỏ qua.
    task_dep_fields = {t["id"]: set(t.get("depends_on", []) or []) for t in tasks}
    for d in dependencies:
        frm, to = d.get("from", ""), d.get("to", "")
        if frm in task_map and to in task_map and frm != to:
            # Bỏ edge nếu nó ngược với depends_on field: to cần frm theo field
            if to in task_dep_fields.get(frm, set()):
                continue
            # Bỏ edge nếu frm thực sự phụ thuộc to nhưng field của frm không có
            # (edge riêng chỉ dùng khi field không nhắc) — thêm dep an toàn
            dep_map[frm].add(to)

    journey_rank = task_journey_rank or {}

    def sort_key(tid):
        # Journey sớm (rank nhỏ) lên trước — user journey thắng dependency
        # (Welcome J1 trước Login J2 dù code Login dùng AuthVM).
        # Cùng journey → giữ thứ tự id ổn định.
        return (journey_rank.get(tid, 999), tid)

    result, visited, visiting = [], set(), set()

    def dfs(tid):
        if tid in visited:
            return
        if tid in visiting:
            return  # cycle — bỏ
        visiting.add(tid)
        # Dep trong CÙNG journey: phải trước. Dep khác journey: journey rank quyết.
        for dep in sorted(dep_map.get(tid, []), key=sort_key):
            if journey_rank.get(dep, 999) == journey_rank.get(tid, 999) or \
               journey_rank.get(dep, 999) < journey_rank.get(tid, 999):
                dfs(dep)
            # dep ở journey SAU task hiện tại (code dep ngược journey) → bỏ qua,
            # để sort_key xếp task theo journey đúng
        visiting.discard(tid)
        visited.add(tid)
        result.append(tid)

    for t in sorted(task_map.keys(), key=sort_key):
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

    # User journey rank: J1 < J2 < ... — task thuộc feature journey sớm hơn lên trước
    # (Welcome/Login J1-J2 trước RecentChat/Chat J3-J5)
    JOURNEY_RANK = {"J1": 1, "J2": 2, "J3": 3, "J4": 4, "J5": 5, "J6": 6, "J7": 7, "J8": 8, "J9": 9, "J10": 10}
    feat_journey = {}
    for f in features:
        jids = f.get("journey_ids", [])
        if f.get("id", "") == "F-CORE":
            feat_journey[f.get("id", "")] = 0  # setup/scaffold trước mọi journey
        else:
            feat_journey[f.get("id", "")] = min((JOURNEY_RANK.get(j, 99) for j in jids), default=99)
    # task → feature (qua capability; F-XXX là feature id dùng thẳng)
    task_to_feature = {}
    for t in tasks:
        norm_id = normalize_capability_id(t.get("capability_id", ""), caps)
        if re.match(r"^F[-_]", norm_id):
            fid = norm_id
        else:
            fid = cap_feat.get(norm_id, "")
        task_to_feature[t.get("id", "")] = fid
    task_journey_rank = {
        tid: feat_journey.get(fid, 99) for tid, fid in task_to_feature.items()
    }

    # Foundation tasks: setup/lifecycle/entry-point — NHẬN DIỆN từ action (không phụ thuộc feature priority)
    FOUNDATION_SIGNALS = ["appdelegate", "entry point", "@main", "diagnostics", "configure sentry",
                          "configure third-party", "initial setup", "setup"]

    ordered = topo_sort_tasks(tasks, deps, task_journey_rank=task_journey_rank)

    # M4-narrative: task→stage mapping ĐÃ LƯU từ STEP 3.5 (deterministic — không
    # gọi LLM lại). Stage idx → phase: 0→FOUNDATION, 1→MVP, 2-3→EXTEND, 4+→POLISH.
    stages = pg.get("product", {}).get("development_stages", [])
    stage_assignments = pg.get("curriculum", {}).get("task_stage_mapping", {})

    phases: Dict[str, List] = defaultdict(list)
    for i, t in enumerate(ordered):
        cap_id = normalize_capability_id(t.get("capability_id", ""), caps)
        feat_id = cap_feat.get(cap_id, "")
        priority = feat_priority.get(feat_id, "core")
        action_lower = (t.get("action", "") or "").lower()

        stage_phase = stage_assignments.get(t.get("id", ""))
        if stage_phase:
            # LLM có thể trả "1. Giai đoạn 1 — ..." — strip số prefix
            import re as _re
            norm_phase = _re.sub(r"^\d+\.\s*", "", stage_phase)
            stage_idx = next((i for i, s in enumerate(stages)
                              if s.get("stage") == norm_phase), -1)
            if stage_idx == 0:
                phase = "FOUNDATION"
            elif stage_idx == 1:
                phase = "MVP"
            elif stage_idx in (2, 3):
                phase = "EXTEND"
            else:
                phase = "POLISH"
        else:
            # Fallback: completion_level → FOUNDATION signal → priority
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
            "concepts": polish_concepts(g, mappings, features, tasks),
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
            "concepts": polish_concepts(d, mappings, features, tasks),
            "order": order_base + n_gaps + idx,
        })
    phases["POLISH"].extend(polish_extra)

    result = {"schema_version": 3, "phases": []}
    for phase_name in sorted(phases.keys(), key=lambda p: PHASE_ORDER.get(p, 9)):
        # Scaffold/setup task luôn đầu phase (tạo project trước khi code)
        items = sorted(phases[phase_name], key=lambda x: (
            0 if "scaffold" in x["task"].get("action", "").lower() else 1,
            x["order"]
        ))
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
        "BLOOM THEO LOẠI TASK (BẮT BUỘC): task thuần UI → APPLY chính (tối đa 1 UNDERSTAND, KHÔNG "
        "ANALYZE); task logic/service → ANALYZE tối đa 1 + APPLY; task khái niệm mới/scaffold → "
        "UNDERSTAND chính + APPLY; task refactor/polish/gap → ANALYZE + CREATE chính, không UNDERSTAND "
        "trừ khái niệm mới. Mỗi task tối đa 1 ANALYZE, tối thiểu 1 APPLY.\n"
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


def attach_assessments(roadmap_structure: dict) -> dict:
    """Biggs constructive alignment: gắn assessment vào MỖI LO từ task.acceptance.

    Assessment = cách kiểm tra LO đó đạt chưa. Nguồn: task.acceptance (tiêu chí
    chấp nhận) + outcome.user_visible. Nếu task không có acceptance → dùng action
    làm assessment gần đúng.
    """
    for phase in roadmap_structure.get("phases", []):
        for m in phase.get("milestones", []):
            t = m.get("task", {})
            acc = t.get("acceptance") or []
            acc_str = "; ".join(str(a) for a in acc) if acc else ""
            outcome = (t.get("outcome") or {}).get("user_visible", "")
            for lo in m.get("los", []):
                if not lo.get("assessment"):
                    base = acc_str or outcome or t.get("action", "")
                    # Nối bloom vào assessment cho phù hợp (áp dụng/đánh giá)
                    lo["assessment"] = base[:200] if base else f"Hoàn thành task {t.get('id', '')}"
    return roadmap_structure


def generate_tasks_lo_batch(tasks: List[Dict], validations: List[Dict],
                            batch_size: int = 10,
                            bloom_caps: dict = None) -> Dict[str, List[Dict]]:
    """Sinh LO cho NHIỀU task trong 1 LLM call (batch-10 JIT).

    bloom_caps: {task_id: {concept_code: bloom_cap}} — từ Curriculum Graph
    (Bruner spiral). LLM KHÔNG được vượt cap cho concept đó.
    """
    if len(tasks) <= 1:
        return {t["id"]: generate_task_lo(t, t.get("_concepts", []), validations)
                for t in tasks}

    system = (
        "Bạn là chuyên gia sư phạm. Sinh Learning Objectives (LO) cho NHIỀU implementation task "
        "trong roadmap học-by-building.\n"
        "Mỗi task: sinh 2-4 LO — câu bắt đầu 'Người học có khả năng', kèm bloom_level "
        "(UNDERSTAND/APPLY/ANALYZE/CREATE) và lo_type (UNIVERSAL/CONCEPTUAL_IMPL/SPECIFIC_IMPL).\n"
        "Gắn LO vào concept_code ĐÃ CHO ở mỗi task, KHÔNG tạo concept mới.\n"
        "BLOOM THEO LOẠI TASK (BẮT BUỘC — KHÔNG bơm ANALYZE bừa bãi):\n"
        "  - Task thuần UI/view (Implement XView, render, hiển thị): APPLY là chính, tối đa 1 UNDERSTAND "
        "nếu có khái niệm SwiftUI mới. KHÔNG ANALYZE.\n"
        "  - Task logic/service (ViewModel, manager, data layer, realtime sync): ANALYZE hợp lý cho "
        "1 LO (phân tích luồng dữ liệu), còn lại APPLY.\n"
        "  - Task khái niệm mới (scaffold, entry point, setup nền tảng): UNDERSTAND là chính (hiểu "
        "vì sao cần), kèm APPLY cho thao tác.\n"
        "  - Task refactor/polish/gap: ANALYZE (đánh giá code hiện tại) + CREATE (thiết kế giải pháp "
        "mới) là chính, KHÔNG UNDERSTAND trừ khi giải thích khái niệm mới.\n"
        "Mỗi task KHÔNG được có quá 1 ANALYZE (trừ polish/refactor). "
        "Tối thiểu 1 APPLY cho task nào cũng có.\n"
        "BLOOM CAP (Bruner spiral — BẮT BUỘC tuân thủ, không vượt): nếu task có ghi "
        "BLOOM_CAPS, mỗi concept phải sinh LO có bloom_level ≤ cap (UNDERSTAND < APPLY < "
        "ANALYZE < CREATE). Concept gặp lần đầu chỉ được UNDERSTAND/APPLY — KHÔNG được "
        "ANALYZE/CREATE cho khái niệm hoàn toàn mới.\n"
        "Trả JSON: {\"results\": {\"<TASK_ID>\": {\"los\": [{\"description\": \"...\", "
        "\"bloom_level\": \"...\", \"lo_type\": \"...\", \"concept_code\": \"...\", "
        "\"keyword\": \"...\"}]}}}\n"
        "Nếu task không có concept, concept_code để rỗng.\n"
        "Viết BẰNG TIẾNG VIỆT (giữ thuật ngữ kỹ thuật tiếng Anh)."
    )

    user_items = []
    for t in tasks:
        concepts = t.get("_concepts", [])
        caps = bloom_caps or {}
        task_caps = caps.get(t["id"], {})
        caps_str = ", ".join(f"{c}:{cap}" for c, cap in task_caps.items()) or "KHÔNG GIỚI HẠN"
        user_items.append(
            f"- TASK {t['id']}: {t.get('action', '')}\n"
            f"    INTENT: {t.get('intent', '')}\n"
            f"    OUTCOME: {t.get('outcome', {}).get('user_visible', '')}\n"
            f"    KEYWORDS: {t.get('keywords', [])}\n"
            f"    CONCEPTS: {concepts}\n"
            f"    BLOOM_CAPS: {caps_str}\n"
            f"    ACCEPTANCE: {t.get('acceptance', [])}\n"
            f"    EFFORT: {t.get('effort', {})}"
        )

    user = (
        "Sinh LO cho các task sau (mỗi task 2-4 LO):\n\n" + "\n".join(user_items)
    )

    try:
        client, _p, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
        results = res.get("results", {})
        out = {}
        for t in tasks:
            tid = t["id"]
            los = results.get(tid, {}).get("los", [])
            if not los:
                raise ValueError(f"Batch thiếu LO cho {tid}")
            out[tid] = [{"task_id": tid, **lo} for lo in los]
        return out
    except Exception as e:
        print(f"[WARN] Batch LLM fail ({e}) → fallback per-task", file=sys.stderr)
        return {t["id"]: generate_task_lo(t, t.get("_concepts", []), validations)
                for t in tasks}


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
        # Curriculum Graph (Bruner spiral): bloom cap per concept per task
        # {task_id: {concept_code: cap}} — concept gặp lần 1 → UNDERSTAND/APPLY
        bloom_caps = {}
        curriculum = pg.get("curriculum", {})
        for seq in curriculum.get("concept_sequence", []):
            bloom_caps.setdefault(seq.get("task_id"), {})[seq.get("concept_code")] = seq.get("bloom_cap")

        # Batch-10 JIT: gộp tasks theo chunk 10 → 1 LLM call/chunk (thay vì per-task)
        all_milestones = [m for phase in structure["phases"] for m in phase["milestones"]]
        # Gắn concepts tạm vào task để batch dùng
        for m in all_milestones:
            m["task"]["_concepts"] = m["concepts"]
        BATCH_SIZE = 10
        for i in range(0, len(all_milestones), BATCH_SIZE):
            chunk = all_milestones[i:i + BATCH_SIZE]
            chunk_tasks = [m["task"] for m in chunk]
            print(f"[*] Sinh LO batch {i // BATCH_SIZE + 1}/{(len(all_milestones) + BATCH_SIZE - 1) // BATCH_SIZE}: "
                  f"{len(chunk_tasks)} tasks ({', '.join(t['id'] for t in chunk_tasks)})")
            batch_los = generate_tasks_lo_batch(chunk_tasks, validations, batch_size=BATCH_SIZE,
                                                bloom_caps=bloom_caps)
            for m in chunk:
                m["los"] = batch_los.get(m["task"]["id"], [])

        # Dọn field tạm
        for m in all_milestones:
            m["task"].pop("_concepts", None)

    # Biggs: gắn assessment vào mỗi LO (constructive alignment)
    structure = attach_assessments(structure)

    # Đóng gói output
    roadmap = {
        "project": pg.get("project", {}),
        "curriculum": pg.get("curriculum", {}),
        "development_stages": pg.get("product", {}).get("development_stages", []),
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
