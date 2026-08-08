#!/usr/bin/env python3
"""
STEP 4 — Task-aware Roadmap: Project Graph (canonical v3) → roadmap.json.

Compile Project Graph + knowledge_mapping thành roadmap task-aware:
  1. Mỗi task → tập concepts (từ knowledge_mapping, giữ node_id; scaffold → [] )
  2. Sắp xếp task theo LOGIC HỌC TẬP stage-aware (learning_order.py — narrative
     development_stages, KHÔNG phải dependency compile-time)
  3. Phase = development stage (6 stages thay vì 4 phases hardcode); gaps/debt → POLISH
  4. JIT sinh LO per-task (LLM) — dùng intent + outcome + keywords + concepts
  5. Gắn validation làm assessment

Input: project_graph_curriculum.json (STEP 3.5)
Output: roadmap.json (phases → milestones → tasks → LOs)

Usage:
  python step4_roadmap.py \
      --project-graph output/project_graph_curriculum.json \
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

# Stage-aware learning order (dùng chung với STEP 3.5 — một nguồn thứ tự duy nhất)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_order import (
    learning_task_order, honored_learning_deps,
    stage_index as learning_stage_index,
)

# Mọi degradation LLM được ghi lại và đẩy vào roadmap output (KHÔNG nuốt âm thầm)
WARNINGS: List[str] = []

# Concept dạy MVVM pattern — gắn deterministic cho task ViewModel (audit E.5:
# MVVM_PATTERN chỉ xuất hiện ở polish, không có ở MVP dù roadmap toàn MVVM).
MVVM_PATTERN = "MVVM_PATTERN"


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

    # 2. Qua location file (debt có) — tìm task node có source_evidence chứa file đó.
    # Location có thể nối NHIỀU file ('Talky/View/LoginxView.swift and Talky/View/RegisterxView.swift')
    # — phải tách trước khi match, nếu không mọi task đều miss (concepts = []).
    loc = gap_or_debt.get("location", "")
    if loc and impl_tasks:
        loc_files = [f.strip() for f in re.split(r"\s*(?:and|,)\s*", loc) if f.strip()]
        matched_task_ids = {
            t.get("id") for t in impl_tasks
            for f in loc_files
            if f in (t.get("source_evidence", []) or []) or f in (t.get("modifies", []) or [])
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

    # 0. Đã là feature id (F-XXX / F_XXX / F9) → giữ nguyên.
    # LLM gán thẳng feature id cho task.capability_id theo 2 convention: 'F-CORE'
    # (có dấu) và 'F9' (số — STEP 1 v3). Capability ids thật là C1..C11, không
    # trùng F\d nên match an toàn.
    if re.match(r"^F[-_]?\d", task_cap_id):
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


def build_roadmap_structure(pg: Dict) -> Dict:
    """Xây roadmap structure (không LLM): phases → milestones(task) → concepts.

    Phase = development_stage (LLM narrative, đã lưu task_stage_mapping từ STEP 3.5)
    — KHÔNG nén 6 stages → 4 phases hardcode (audit 2026-08-08: MVP 17 task +
    POLISH 17 task, EXTEND 1 task). Thứ tự task = learning_order (stage → need[]
    → journey) — backend không còn đứng trước UI.
    """
    mappings = pg.get("knowledge_mapping", {}).get("mappings", [])
    tasks = pg.get("implementation", {}).get("tasks", [])
    features = pg.get("features", [])
    caps = pg.get("capabilities", [])
    stages = pg.get("product", {}).get("development_stages", [])
    stage_assignments = pg.get("curriculum", {}).get("task_stage_mapping", {})

    # M4 — line-level trace: file → [ref] (file#L<line>) từ STEP 2 evidence.
    # Đính vào milestone để viewer/LO giữ được truy xuất nguồn (không rơi rớt).
    ref_by_file: Dict[str, List[str]] = defaultdict(list)
    for ent in pg.get("evidence", {}).get("entries", []):
        src = ent.get("source") or {}
        if src.get("ref"):
            ref_by_file[src.get("file", "")].append(src["ref"])

    # task → feature (qua capability; F-XXX là feature id dùng thẳng) — cho
    # scaffold detection + concept fallback (task không có task-node MAPPED)
    cap_feat = {c.get("id", ""): c.get("feature_id", "") for c in caps}
    task_to_feature = {}
    for t in tasks:
        norm_id = normalize_capability_id(t.get("capability_id", ""), caps)
        fid = norm_id if re.match(r"^F[-_]?\d", norm_id) else cap_feat.get(norm_id, "")
        task_to_feature[t.get("id", "")] = fid

    # Thứ tự học tập stage-aware (thay topo-sort theo dependency compile-time).
    ordered = learning_task_order(pg, stage_assignments, stages, tasks)
    # Learning-deps nhất quán narrative — milestone giữ field này để viewer/validator
    # thấy ràng buộc học tập (task object giữ nguyên depends_on gốc — code-dep).
    honored_deps = honored_learning_deps(pg, stage_assignments, stages, tasks)

    phases: Dict[str, List] = defaultdict(list)
    for i, t in enumerate(ordered):
        st_idx = learning_stage_index(t.get("id", ""), stage_assignments, stages)
        phase = stages[st_idx].get("stage", f"Stage {st_idx+1}") if st_idx < len(stages) else "POLISH"
        action_lower = (t.get("action", "") or "").lower()
        feat_id = task_to_feature.get(t.get("id", ""))

        concepts = task_concepts(t, mappings)
        # Scaffold (stage 1 = nền tảng thuần / marker khởi tạo): KHÔNG fallback
        # concept từ feature node (audit C.1 — T01 bị gán SHARED_OBSERVABLE_STATE
        # + API_INTEGRATION từ feature F9 catch-all dù chưa có state/API nào).
        SCAFFOLD_MARKERS = ("scaffold", "khởi tạo", "tạo project", "create project",
                            "project setup", "setup project", "xcode project")
        is_scaffold = st_idx == 0 or any(m in action_lower for m in SCAFFOLD_MARKERS)
        if not concepts and not is_scaffold and feat_id:
            # Task không có task-node MAPPED nhưng không phải scaffold → anchor
            # ngữ nghĩa từ feature node (giữ traceability LO → concept).
            for m in mappings:
                if m.get("node_id") == f"feature:{feat_id}" and m.get("status") == "MAPPED":
                    for c in m.get("concepts", []):
                        if c and c not in concepts:
                            concepts.append(c)
        # MVVM: task ViewModel dạy MVVM pattern (audit E.5) — từ MVP, không phải
        # chỉ polish. Deterministic — không cần LLM map lại.
        if "viewmodel" in action_lower and MVVM_PATTERN not in concepts:
            concepts.append(MVVM_PATTERN)

        phases[phase].append({
            "task": t,
            "concepts": concepts,
            # Dep compile-time được lọc thành learning-deps nhất quán narrative —
            # milestone giữ field này để viewer/validator thấy ràng buộc học tập
            # (task object giữ nguyên depends_on gốc).
            "learning_dependencies": honored_deps.get(t.get("id", ""), []),
            "order": i,
            "scaffold": is_scaffold,
            # M4 — line-level trace (file#L<line>) từ STEP 2 evidence
            "evidence_refs": [r for f in (t.get("source_evidence") or [])
                              for r in ref_by_file.get(f, [])],
        })

    # POLISH tasks tự sinh từ missing_gaps + tech_debt (chất lượng — KHÔNG chứa
    # feature thật; feature thật đã nằm ở stage của chúng: Profile S5, Push S6).
    polish_extra = []
    order_base = len(ordered)
    for idx, g in enumerate(pg.get("implementation", {}).get("missing_gaps", [])):
        polish_extra.append({
            "task": {
                "id": f"polish-gap-{idx+1}",
                "capability_id": "",
                # KHÔNG truncate — dữ liệu giữ nguyên nội dung gap (trước cắt 100
                # ký tự làm mất ý: 'đưa lên server/proxy' bị cắt bỏ)
                "action": f"Fix: {g.get('gap', '')}",
                "intent": f"Improve quality: {g.get('gap', '')}",
                "outcome": {"user_visible": g.get('suggested_lo', '')},
                "keywords": [],
                "source_evidence": [g.get('location', '')] if g.get('location') else [],
            },
            "concepts": polish_concepts(g, mappings, features, tasks),
            "learning_dependencies": [],
            "order": order_base + idx,
            "scaffold": False,
            "evidence_refs": [r for f in ([g.get("location", "")] if g.get("location") else [])
                              for r in ref_by_file.get(f, [])],
        })
    n_gaps = len(polish_extra)
    for idx, d in enumerate(pg.get("implementation", {}).get("tech_debt", [])):
        polish_extra.append({
            "task": {
                "id": f"polish-debt-{idx+1}",
                "capability_id": "",
                "action": f"Refactor: {d.get('issue', '')}",
                "intent": f"Giảm tech debt: {d.get('issue', '')}",
                "outcome": {"user_visible": d.get('suggested_phase', 'POLISH')},
                "keywords": [],
                "source_evidence": [d.get('location', '')] if d.get('location') else [],
            },
            "concepts": polish_concepts(d, mappings, features, tasks),
            "learning_dependencies": [],
            "order": order_base + n_gaps + idx,
            "scaffold": False,
            "evidence_refs": [r for f in ([d.get("location", "")] if d.get("location") else [])
                              for r in ref_by_file.get(f, [])],
        })
    phases.setdefault("POLISH", []).extend(polish_extra)

    # Gagné guard (cross-phase, safety net): learning-dependency KHÔNG được nằm
    # sau task của nó. Với thứ tự stage-aware, learning deps luôn ở stage sớm hơn
    # hoặc cùng stage (đã lọc code-deps trỏ stage sau) → guard chỉ phòng hồi quy.
    phase_order = {s.get("stage", f"Stage {i+1}"): i for i, s in enumerate(stages)}
    phase_order["POLISH"] = len(stages)
    ms_by_id = {m["task"]["id"]: (ph, m) for ph, ms in phases.items() for m in ms}
    changed = True
    while changed:
        changed = False
        for ph, ms in list(phases.items()):
            for m in list(ms):
                tid = m["task"]["id"]
                for dep in m.get("learning_dependencies", []):
                    ditem = ms_by_id.get(dep)
                    if not ditem:
                        continue
                    dph, dm = ditem
                    if phase_order.get(dph, 9) > phase_order.get(ph, 9):
                        phases[ph].append(dm)
                        phases[dph].remove(dm)
                        ms_by_id[dep] = (ph, dm)
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break

    result = {"schema_version": 3, "phases": []}
    for phase_name in sorted(phases.keys(), key=lambda p: phase_order.get(p, 9)):
        # Scaffold/setup task luôn đầu phase (tạo project trước khi code)
        items = sorted(phases[phase_name], key=lambda x: (
            0 if x.get("scaffold") else 1,
            x["order"]
        ))
        if not items:
            continue  # phase rỗng sau Gagné guard promotes — không emit
        result["phases"].append({
            "phase": phase_name,
            "milestones": items,
        })
    return result


def _anchor_lo_concepts(los: List[Dict], concepts: List[str]) -> List[Dict]:
    """LO không concept (LLM bỏ trống cho LO thực hành chung, VD 'build WelcomeView')
    → anchor concept đầu của milestone — giữ traceability LO→concept (validator/UI
    không mất, viewer đã fallback concepts[0] — roadmap tự nhất quán).
    Milestone scaffold (concepts=[]) giữ nguyên trống (audit C.1)."""
    anchor = concepts[0] if concepts else None
    if not anchor:
        return los
    for lo in los:
        if not lo.get("concept_code"):
            lo["concept_code"] = anchor
    return los


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
        "You are a pedagogy expert. Generate Learning Objectives (LOs) for ONE implementation task "
        "in a learn-by-building roadmap.\n"
        "Each LO: sentence starts with 'Learners will be able to', with bloom_level (UNDERSTAND/APPLY/ANALYZE/CREATE) "
        "and lo_type (UNIVERSAL/CONCEPTUAL_IMPL/SPECIFIC_IMPL).\n"
        "Attach LOs to the GIVEN concept (concept_code); do NOT create new concepts.\n"
        "BLOOM BY TASK TYPE (REQUIRED): pure UI task → APPLY is primary (max 1 UNDERSTAND, NO "
        "ANALYZE); logic/service task → max 1 ANALYZE + APPLY; new-concept/scaffold task → "
        "UNDERSTAND primary + APPLY; refactor/polish/gap task → ANALYZE + CREATE primary, no UNDERSTAND "
        "except for new concepts. Each task: max 1 ANALYZE, min 1 APPLY.\n"
        "Write all LO descriptions IN ENGLISH.\n"
        "Return JSON: {\"los\": [{\"description\": \"...\", \"bloom_level\": \"...\", "
        "\"lo_type\": \"...\", \"concept_code\": \"...\", \"keyword\": \"...\"}]}"
    )
    user = (
        f"TASK: {task.get('action', '')}\n"
        f"INTENT (WHY): {task.get('intent', '')}\n"
        f"OUTCOME: {task.get('outcome', {}).get('user_visible', '')}\n"
        f"KEYWORDS: {task.get('keywords', [])}\n"
        f"CONCEPTS (choose concept_code from here): {concepts}\n"
        f"ACCEPTANCE: {task.get('acceptance', [])}\n"
        f"VALIDATION: {[v.get('criteria', []) for v in val]}\n"
        f"EFFORT: {task.get('effort', {})}\n"
        "Generate 2-4 LOs covering the concept and the practice of the task."
    )
    try:
        client, _p, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
        los = res.get("los", [])
        return _anchor_lo_concepts([{"task_id": task.get("id"), **lo} for lo in los], concepts)
    except Exception as e:
        print(f"[WARN] LLM fail task {task.get('id')}: {e}", file=sys.stderr)
        WARNINGS.append(f"generate_task_lo fail ({task.get('id')}): {e} — LO fallback")
        return [{"task_id": task.get("id"), "concepts": concepts,
                 "lo": f"[fallback] {task.get('action', '')}"}]


def attach_assessments(roadmap_structure: dict) -> dict:
    """Biggs constructive alignment: gắn assessment vào MỖI LO từ task.acceptance.

    Assessment = cách kiểm tra LO đó đạt chưa. Nguồn: task.acceptance (tiêu chí
    chấp nhận) + outcome.user_visible. Nếu task không có acceptance → dùng action
    làm assessment gần đúng.

    Bloom-aware (audit F.2): UNDERSTAND LO → khung "Explain:" (kiểm tra hiểu),
    APPLY/ANALYZE/CREATE → acceptance criteria (kiểm tra làm được). KHÔNG dùng
    outcome là tên phase ("POLISH") làm assessment — polish task không có
    acceptance sẽ fallback action.
    """
    PHASE_LIKE = {"POLISH", "MVP", "EXTEND", "FOUNDATION"}
    for phase in roadmap_structure.get("phases", []):
        for m in phase.get("milestones", []):
            t = m.get("task", {})
            acc = t.get("acceptance") or []
            acc_str = "; ".join(str(a) for a in acc) if acc else ""
            outcome = (t.get("outcome") or {}).get("user_visible", "")
            if outcome.strip().upper() in PHASE_LIKE:
                outcome = ""  # polish task outcome rác — dùng action
            for lo in m.get("los", []):
                if not lo.get("assessment"):
                    base = acc_str or outcome or t.get("action", "")
                    if not base:
                        lo["assessment"] = f"Complete task {t.get('id', '')}"
                        continue
                    if (lo.get("bloom_level") or "").upper() == "UNDERSTAND":
                        # Kiểm tra hiểu (không phải làm) — acceptance là bối cảnh
                        lo["assessment"] = f"Explain: {base}"[:220]
                    else:
                        lo["assessment"] = base[:220]
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
        "You are a pedagogy expert. Generate Learning Objectives (LOs) for MULTIPLE implementation tasks "
        "in a learn-by-building roadmap.\n"
        "Each task: generate 2-4 LOs — each sentence starts with 'Learners will be able to', with bloom_level "
        "(UNDERSTAND/APPLY/ANALYZE/CREATE) and lo_type (UNIVERSAL/CONCEPTUAL_IMPL/SPECIFIC_IMPL).\n"
        "Attach LOs to the concept_code GIVEN for each task; do NOT create new concepts.\n"
        "BLOOM BY TASK TYPE (REQUIRED — do NOT inflate ANALYZE):\n"
        "  - Pure UI/view task (Implement XView, render, display): APPLY is primary, max 1 UNDERSTAND "
        "if there is a new SwiftUI concept. NO ANALYZE.\n"
        "  - Logic/service task (ViewModel, manager, data layer, realtime sync): ANALYZE is appropriate for "
        "1 LO (analyze the data flow), the rest APPLY.\n"
        "  - New-concept task (scaffold, entry point, platform setup): UNDERSTAND is primary (understand "
        "why it is needed), plus APPLY for the hands-on step.\n"
        "  - Refactor/polish/gap task: ANALYZE (evaluate the current code) + CREATE (design the new "
        "solution) are primary, NO UNDERSTAND unless explaining a new concept.\n"
        "Each task MUST NOT have more than 1 ANALYZE (except polish/refactor). "
        "Every task must have at least 1 APPLY.\n"
        "BLOOM CAP (Bruner spiral — MUST obey, do not exceed): if a task lists "
        "BLOOM_CAPS, each concept must generate LOs with bloom_level ≤ cap (UNDERSTAND < APPLY < "
        "ANALYZE < CREATE). A concept seen for the first time may only be UNDERSTAND/APPLY — NEVER "
        "ANALYZE/CREATE for a completely new concept.\n"
        "Return JSON: {\"results\": {\"<TASK_ID>\": {\"los\": [{\"description\": \"...\", "
        "\"bloom_level\": \"...\", \"lo_type\": \"...\", \"concept_code\": \"...\", "
        "\"keyword\": \"...\"}]}}}\n"
        "If a task has no concept, leave concept_code empty.\n"
        "Write all LO descriptions IN ENGLISH (keep technical terms verbatim)."
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
        "Generate LOs for the following tasks (2-4 LOs each):\n\n" + "\n".join(user_items)
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
            out[tid] = _anchor_lo_concepts([{"task_id": tid, **lo} for lo in los],
                                           t.get("_concepts", []))
        return out
    except Exception as e:
        print(f"[WARN] Batch LLM fail ({e}) → fallback per-task", file=sys.stderr)
        WARNINGS.append(f"generate_tasks_lo_batch fail: {e} — fallback per-task")
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
    if WARNINGS:
        roadmap["pipeline_warnings"] = list(WARNINGS)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Roadmap → {args.output}")
    for phase in roadmap["phases"]:
        n = len(phase["milestones"])
        n_lo = sum(len(m.get("los", [])) for m in phase["milestones"])
        print(f"    {phase['phase']}: {n} tasks, {n_lo} LOs")
    if WARNINGS:
        print(f"    ⚠ {len(WARNINGS)} LLM degradation warning(s) — xem pipeline_warnings trong output:")
        for w in WARNINGS:
            print(f"      - {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
