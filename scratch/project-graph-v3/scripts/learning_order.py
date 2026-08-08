#!/usr/bin/env python3
"""learning_order.py — Stage-aware learning order (dùng chung STEP 3.5 + STEP 4).

Thay thế topo-sort theo task_dependencies thuần bằng ordering theo LOGIC HỌC TẬP
(đúng narrative development_stages mà STEP 1 sinh ra):

    primary:    stage index  (curriculum.task_stage_mapping — LLM narrative, artifact)
    secondary:  vị trí task trong need[] của stage (thứ tự tác giả biên soạn)
    tertiary:   journey rank của feature task thuộc (tie-break)
    tie-break:  thứ tự ban đầu trong graph

Dependency từ STEP 1 là CODE-DEPENDENCY (compile-time: WelcomeView NavigationLink
cần LoginView, ChatDetail cần PushNotificationManager...) — KHÔNG được dùng để
sắp xếp học tập. Chỉ dep NHẤT QUÁN với narrative (dep ở stage sớm hơn, hoặc cùng
stage nhưng đứng trước trong need[]) được giữ làm LEARNING-DEPENDENCY và dùng làm
ràng buộc phụ trong stage (Kahn tie-break). Dep ngược narrative bị bỏ khỏi thứ tự
(giữ nguyên trên task object — dữ liệu gốc không đổi, chỉ không lái thứ tự).

Audit 2026-08-08 (Talky roadmap): stage narrative đúng nhưng step4 nén 6 stages →
4 phases hardcode + Gagné guard kéo ngược → MVP 17 task + POLISH 17 task. Module
này là root-cause fix: phase = stage, thứ tự = narrative.
"""
import re
from collections import defaultdict

# Token chung — không có giá trị phân biệt khi match task ↔ need
# LƯU Ý: KHÔNG stop 'implement'/'create'/'build' — chúng xuất hiện ở CẢ action
# task và need item, đếm như token khớp giúp task qua ngưỡng (T07 'login screen'
# ↔ item 'Implement login/register UI' cần 'implement'+'login' = 2).
STOP = {
    "with", "and", "the", "using", "into", "from", "that", "this",
    "for", "view", "app", "screen", "form", "add", "make", "use", "get",
    "set", "new", "real", "mock", "data", "file", "show",
    "với", "và", "của", "trong", "cho", "theo", "để", "các", "một", "không",
    "có", "được", "sau", "khi", "từ", "của", "thì", "là", "bằng",
}

JOURNEY_RANK = {f"J{i}": i for i in range(1, 11)}
JOURNEY_RANK["F-CORE"] = 0  # setup/scaffold feature → trước mọi journey

INF = 1_000_000


def tokens(text: str) -> set:
    """Token lowercase theo biên không-phải-chữ-số (login/register → login, register)."""
    return set(re.findall(r"[a-z0-9]+", (text or "").lower())) - STOP


def identifiers(text: str) -> set:
    """CamelCase/identifier tokens (WelcomeView, SecureTextField...) — tín hiệu phân biệt mạnh."""
    return set(re.findall(r"[A-Za-z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)+", text or ""))


def _need_score(task: dict, need: str) -> int:
    """Độ khớp task ↔ 1 need item của stage.

    - token overlap EXACT (đã tách theo biên ký tự: 'login/register' → login, register)
    - +2 cho mỗi identifier (CamelCase) trùng trong ACTION (KHÔNG dùng source_evidence
      — file evidence là code-dep, làm login screen khớp nhầm need 'WelcomeView'
      chỉ vì cùng file LoginxView.swift)
    """
    action = f"{task.get('action', '')} {task.get('intent', '')}"
    toks_t = tokens(action)
    toks_n = tokens(need)
    score = len(toks_t & toks_n)

    ids_t = identifiers(action)
    ids_n = identifiers(need)
    score += 2 * len(ids_t & ids_n)
    return score


def need_position(task: dict, stage: dict) -> int:
    """Vị trí task trong need[] của stage (authored learning order).

    Không khớp need nào (score < 2) → INF (xếp sau mọi task khớp trong stage).
    """
    best, best_score = INF, 0
    for i, need in enumerate(stage.get("need", []) or []):
        s = _need_score(task, need)
        if s > best_score:
            best, best_score = i, s
    return best if best_score >= 2 else INF


# ==== Phân loại dep cùng-stage: navigation (bỏ) vs learning (giữ) ====
# Audit v2 (2026-08-08): trong stage, dep VIEW→VIEW là navigation/compile-time
# (WelcomeView 'navigates to' Login; RecentChatView 'presents' NewChat) — learner
# build view trước với placeholder. Dep tới COMPONENT (SecureTextField, ImagePicker
# 'reusable component') là learning thật (form cần component có sẵn) → GIỮ.
NAV_REASON = re.compile(r"navigat|present|link|open|launch", re.I)
# \bpush\b KHÔNG khớp 'PushNotificationManager' (không có word boundary) — an toàn.
COMPONENT_SIGNALS = ("component", "reusable", "wrapper", "picker", "util", "helper")
WIRING_SIGNALS = ("wire", "appdelegate", "delegate", "root app", "@main")


def _is_component_task(task: dict) -> bool:
    return any(sig in (task.get("action", "") or "").lower() for sig in COMPONENT_SIGNALS)


def _is_wiring_task(task: dict) -> bool:
    """Integration capstone (AppDelegate, root wiring) — xếp SAU mọi dep cùng stage."""
    action = (task.get("action", "") or "").lower()
    return any(sig in action for sig in WIRING_SIGNALS)


def _dep_reasons(pg: dict) -> dict:
    """(from, to) → reason từ task_dependencies (edge có reason LLM viết)."""
    out = {}
    for d in pg.get("implementation", {}).get("task_dependencies", []):
        out[(d.get("from", ""), d.get("to", ""))] = d.get("reason", "")
    return out


def _same_stage_honored(task: dict, tasks_by_id: dict, stage_mapping: dict, stages: list,
                        dep_reasons: dict) -> set:
    """Dep cùng-stage được TÔN TRỌNG trong thứ tự học của task.

    Quy tắc (audit v2):
    - task WIRING → giữ MỌI dep cùng-stage (wire cần mọi manager có sẵn: T22 sau T20/T21)
    - dep thường → giữ TRỪ KHI reason là navigation/presentation tới SCREEN (không
      phải component): WelcomeView 'navigates to' Login/Register → bỏ; EditProfile
      'presents ImagePicker' (component reusable) → giữ.
    """
    tid = task.get("id", "")
    st = stage_index(tid, stage_mapping, stages)
    honored = set()
    for dep in task.get("depends_on", []) or []:
        if stage_index(dep, stage_mapping, stages) != st:
            continue
        if _is_wiring_task(task):
            honored.add(dep)
            continue
        reason = dep_reasons.get((tid, dep), "")
        dep_task = tasks_by_id.get(dep, {})
        if NAV_REASON.search(reason) and not _is_component_task(dep_task):
            continue  # navigation tới screen — placeholder được, không phải prerequisite
        honored.add(dep)
    return honored


def stage_index(task_id: str, stage_mapping: dict, stages: list) -> int:
    """Index của stage task thuộc (theo task_stage_mapping — LLM narrative).

    Task không có mapping → len(stages) (xếp sau mọi stage thật).
    """
    name = (stage_mapping or {}).get(task_id)
    if name:
        for i, s in enumerate(stages):
            if s.get("stage") == name:
                return i
    return len(stages)


def _journey_ranks(pg: dict) -> dict:
    """task_id → journey rank của feature task thuộc (0 = F-CORE, 99 = không rõ)."""
    cap_feat = {c.get("id", ""): c.get("feature_id", "") for c in pg.get("capabilities", [])}
    feat_journey = {}
    for f in pg.get("features", []):
        jids = f.get("journey_ids", []) or []
        feat_journey[f.get("id", "")] = (
            0 if f.get("id") == "F-CORE"
            else min((JOURNEY_RANK.get(j, 99) for j in jids), default=99)
        )
    ranks = {}
    for t in pg.get("implementation", {}).get("tasks", []):
        cid = t.get("capability_id", "")
        fid = cid if re.match(r"^F[-_]?\d", cid) else cap_feat.get(cid, "")
        ranks[t["id"]] = feat_journey.get(fid, 99)
    return ranks


def learning_dependencies(task: dict, stage_mapping: dict, stages: list) -> list:
    """LEARNING-DEPENDENCY của task: dep ở stage sớm hơn HOẶC cùng stage.

    Dep trỏ tới stage SAU (code-dep compile-time: View trỏ tới logic chưa học) bị
    loại khỏi ràng buộc học tập — learner xây mock trước, wire thật ở stage sau.
    """
    tid = task.get("id", "")
    st = stage_index(tid, stage_mapping, stages)
    out = []
    for dep in task.get("depends_on", []) or []:
        if stage_index(dep, stage_mapping, stages) <= st:
            out.append(dep)
    return out


def honored_learning_deps(pg: dict, stage_mapping: dict, stages: list, tasks: list) -> dict:
    """task_id → [dep được TÔN TRỌNG trong thứ tự học] — cùng logic với learning_task_order.

    Dep hợp lệ: stage sớm hơn (prerequisite đã học) HOẶC cùng stage được
    _same_stage_honored() duyệt (bỏ navigation tới screen, giữ component/dep thật,
    wiring giữ mọi dep). Dep ngược là code-dep — loại khỏi ràng buộc học tập.
    """
    tasks = list(tasks)
    tasks_by_id = {t["id"]: t for t in tasks}
    stage_of = {t["id"]: stage_index(t["id"], stage_mapping, stages) for t in tasks}
    dep_reasons = _dep_reasons(pg)

    out = {}
    for t in tasks:
        st = stage_of[t["id"]]
        same_honored = _same_stage_honored(t, tasks_by_id, stage_mapping, stages, dep_reasons)
        out[t["id"]] = [
            d for d in (t.get("depends_on", []) or [])
            if stage_of.get(d, INF) < st or d in same_honored
        ]
    return out


def learning_task_order(pg: dict, stage_mapping: dict, stages: list, tasks: list) -> list:
    """Thứ tự học tập: (stage_idx, need_pos, journey_rank, idx) + Kahn cùng-stage.

    Kahn: dep cùng-stage được tôn trọng theo _same_stage_honored() — navigation
    tới screen bị bỏ (WelcomeView trước Login), component/dep thật giữ (ImagePicker
    trước EditProfile, models trước ViewModel), wiring giữ mọi dep (T20→T21→T22).
    Cross-stage dep tự thoả (stage sớm emit trước).
    """
    tasks = list(tasks)
    tasks_by_id = {t["id"]: t for t in tasks}
    stage_of = {t["id"]: stage_index(t["id"], stage_mapping, stages) for t in tasks}
    journey = _journey_ranks(pg)
    idx = {t["id"]: i for i, t in enumerate(tasks)}
    dep_reasons = _dep_reasons(pg)

    by_stage = defaultdict(list)
    for t in tasks:
        by_stage[stage_of[t["id"]]].append(t)

    ordered: list = []
    for st in sorted(by_stage):
        group = by_stage[st]
        stage = stages[st] if st < len(stages) else None
        pos = {t["id"]: need_position(t, stage) if stage else INF for t in group}
        # INF tasks (không khớp need nào) → neo sau same-stage deps có pos thật
        # (VD T08 registration không khớp need 'login/register' chính xác → xếp
        # sau T16 SecureTextField, trước RecentChatView).
        for t in group:
            if pos[t["id"]] == INF:
                same = [d for d in (t.get("depends_on", []) or [])
                        if stage_of.get(d) == st and pos.get(d, INF) < INF]
                if same:
                    pos[t["id"]] = max(pos[d] for d in same) + 0.5

        # Kahn tie-break (pos, journey, idx) với dep cùng-stage thật (nav bỏ)
        honored = {t["id"]: _same_stage_honored(t, tasks_by_id, stage_mapping, stages, dep_reasons)
                   for t in group}

        remaining = {t["id"] for t in group}
        emitted: list = []
        while remaining:
            ready = [tid for tid in remaining
                     if not (honored.get(tid, set()) & remaining)]
            if not ready:  # cycle an toàn (không nên xảy ra — pos đã phi mâu thuẫn)
                ready = [min(remaining, key=lambda x: (pos.get(x, INF), journey.get(x, 99), idx.get(x, 0)))]
            ready.sort(key=lambda x: (pos.get(x, INF), journey.get(x, 99), idx.get(x, 0)))
            tid = ready[0]
            remaining.discard(tid)
            emitted.append(tid)

        ordered.extend(next(t for t in group if t["id"] == tid) for tid in emitted)
    return ordered


def assign_stages_by_matching(tasks: list, stages: list) -> dict:
    """Fallback DETERMINISTIC (không LLM): task → stage theo _need_score.

    Dùng khi chạy --no-judge trên graph CHƯA có task_stage_mapping artifact
    (audit v2 #7 — trước đây mapping rỗng → mọi task rơi vào POLISH). Khớp với
    toàn bộ text stage (need + product_state + learn), chọn stage điểm cao nhất;
    task không khớp stage nào (score < 2) → bỏ trống (vẫn để POLISH fallback).
    """
    mapping = {}
    for t in tasks:
        best, best_score = None, 0
        for s in stages:
            # Điểm = need item khớp NHẤT của stage (per-item — concatenate cả stage
            # làm T07/T08 khớp nhầm stage auth vì cùng từ 'register/login').
            items = (s.get("need", []) or []) + [s.get("product_state", "")]
            score = max((_need_score(t, n) for n in items), default=0)
            if score > best_score:
                best, best_score = s.get("stage"), score
        if best and best_score >= 2:
            mapping[t["id"]] = best
    return mapping


def correct_stage_assignments(pg: dict, stage_mapping: dict, stages: list) -> dict:
    """Hiệu chỉnh deterministic task_stage_mapping (audit v2 #3).

    Task có MỌI dep ở stage sớm hơn NHƯNG có dependent (task khác liệt kê nó
    trong depends_on) ở stage sớm hơn → utility dùng chung bị xếp sai stage sau
    (VD T04 ViewState → Stage 6 Push dù AuthViewModel Stage 3 cần nó). Kéo về
    stage ngay sau dep muộn nhất của nó (T04: sau T01 → Stage 2). Task có dep
    cùng/sau stage (feature-wired, VD T21 push cần T20) không bị đụng.
    """
    if not stage_mapping:
        return dict(stage_mapping)
    tasks = pg.get("implementation", {}).get("tasks", [])
    task_stage = {t["id"]: stage_index(t["id"], stage_mapping, stages) for t in tasks}
    dependents = defaultdict(list)
    for t in tasks:
        for d in t.get("depends_on", []) or []:
            dependents[d].append(t["id"])

    mapping = dict(stage_mapping)
    tasks_by_id = {t["id"]: t for t in tasks}
    dep_reasons = _dep_reasons(pg)
    for t in tasks:
        st = task_stage[t["id"]]
        if st == 0 or st >= len(stages):
            continue
        deps = [d for d in (t.get("depends_on", []) or []) if d in task_stage]
        if not deps:
            continue
        # có dep cùng stage hoặc sau → feature-wired (VD T21 cần T20 cùng S6) → giữ
        if any(task_stage[d] >= st for d in deps):
            continue
        # Dependent CHỈ tính nếu không phải navigation-tới-screen (VD T13 'links to
        # ProfileView' — code-dep, không chứng minh T17 là utility dùng chung).
        earlier_dependents = [
            task_stage[y] for y in dependents.get(t["id"], [])
            if task_stage.get(y, 99) < st
            and not (NAV_REASON.search(dep_reasons.get((y, t["id"]), ""))
                     and not _is_component_task(t))
        ]
        if not earlier_dependents:
            continue
        new_stage = max(1, max(task_stage[d] for d in deps) + 1)
        if new_stage < st:
            mapping[t["id"]] = stages[new_stage].get("stage", stages[new_stage])
            task_stage[t["id"]] = new_stage
    return mapping


def stage_phases(pg: dict, stage_mapping: dict, stages: list, tasks: list) -> list:
    """Phases stage-based (nhẹ — cho mastery_gates/walking_skeleton ở STEP 3.5).

    Mỗi development_stage → 1 phase; missing_gaps + tech_debt → phase POLISH cuối.
    STEP 4 dựng milestones đầy đủ (concepts/evidence) từ cùng thứ tự này.
    """
    ordered = learning_task_order(pg, stage_mapping, stages, tasks)
    phases = []
    for st, stage in enumerate(stages):
        items = [{"task": t} for t in ordered
                 if stage_index(t["id"], stage_mapping, stages) == st]
        if items:
            phases.append({"phase": stage.get("stage", f"Stage {st+1}"), "milestones": items})
    polish = [
        {"task": {"id": f"polish-gap-{i+1}"}} for i in range(len(pg.get("implementation", {}).get("missing_gaps", [])))
    ] + [
        {"task": {"id": f"polish-debt-{i+1}"}} for i in range(len(pg.get("implementation", {}).get("tech_debt", [])))
    ]
    if polish:
        phases.append({"phase": "POLISH", "milestones": polish})
    return phases
