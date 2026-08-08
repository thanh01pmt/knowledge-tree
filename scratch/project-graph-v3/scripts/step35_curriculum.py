#!/usr/bin/env python3
"""
STEP 3.5 — Curriculum Graph (tầng giữa Project Graph và Roadmap).

Bám lý thuyết giáo dục (xem docs/curriculum-graph-design-B.md):
- Gagné: concept prerequisite DAG — task chỉ vào khi concept tiên quyết đã xuất hiện.
- Bruner: spiral curriculum — bloom cap tăng theo số lần concept được gặp.
- Reigeluth: walking skeleton — epitome (FOUNDATION) trước, elaborate sau.
- Vygotsky: ZPD check — mỗi task có ≥1 concept quen (known) + ≤ K concept mới (new).
- Sweller: intrinsic load gate — quá nhiều concept mới/task → flag tách task.
- Bloom: mastery gates giữa phase — assessment phải pass mới qua phase sau.

Output: curriculum section (thêm vào project graph):
{
  "curriculum": {
    "concept_prerequisites": [{"concept_code", "requires", "source", "confidence"}],
    "concept_sequence": [{"concept_code", "first_seen_task", "encounters", "bloom_cap"}],
    "walking_skeleton": {"epitome", "elaborations"},
    "zpd_checks": [{"task_id", "new_concepts", "known_concepts", "verdict"}],
    "mastery_gates": [{"phase", "criteria", "next_phase"}]
  }
}

Usage:
  python step35_curriculum.py \
      --project-graph output/project_graph_standardized.json \
      --lo-prerequisites ../../projects/master-tree/output/lo_prerequisites.tsv \
      --output output/project_graph_curriculum.json
"""
import argparse
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))

try:
    from llm_call import llm_chat_json, get_llm_client
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

# Ngưỡng cognitive load (Sweller) — concept MỚI tối đa/task
MAX_NEW_CONCEPTS_PER_TASK = 2


def _concept_descriptions(pg: dict, master_path: Path) -> dict:
    """Nạp mô tả concept: ưu tiên master tree (Bảng 5), fallback từ mappings."""
    desc = {}
    if master_path and master_path.is_file():
        try:
            with open(master_path, encoding="utf-8-sig") as f:
                for line in f:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) >= 3 and parts[0] and parts[0] != "code" and "Bảng" not in parts[0]:
                        desc[parts[0]] = parts[2][:120]
        except Exception:
            pass
    # Fallback: keyword từ knowledge_mapping
    for m in pg.get("knowledge_mapping", {}).get("mappings", []):
        c = m.get("concept_code") or (m.get("concepts") or [None])[0]
        if c and c not in desc and m.get("keyword"):
            desc[c] = m["keyword"][:120]
    return desc


def llm_judge_edges(pg: dict, edges: list, master_path: Path) -> list:
    """LLM-as-judge: đánh giá từng prerequisite edge — giữ hay loại.

    Mỗi edge: concept_code requires X. Judge nhìn mô tả concept + task context
    → trả keep/reject + confidence + rationale. Giải quyết hub noise tự động.
    """
    if not _LLM_AVAILABLE or not edges:
        return edges

    desc = _concept_descriptions(pg, master_path)
    # Task context: task nào dạy concept nào (cho judge đối chiếu thực tế)
    task_conc = {}
    for m in pg.get("knowledge_mapping", {}).get("mappings", []):
        nid = m.get("node_id", "")
        if nid.startswith("task:") and m.get("status") == "MAPPED":
            task_conc[m.get("node_id").split(":", 1)[1]] = m.get("concepts", [])

    edge_lines = []
    for i, e in enumerate(edges):
        edge_lines.append(
            f"{i}. {e['concept_code']} requires {e['requires']}"
            f"  [source={e.get('source','')}, conf={e.get('confidence')}]"
        )

    system = (
        "Bạn là chuyên gia giáo dục + kiến trúc sư phần mềm. Đánh giá từng cạnh "
        "prerequisite trong concept DAG của một roadmap học-by-building.\n"
        "'A requires B' nghĩa: học viên PHẢI hiểu concept B trước khi học A.\n"
        "Tiêu chí giữ (keep):\n"
        "1. B là nền tảng/tiền đề logic của A (VD: biết data binding trước khi dùng "
        "ObservableObject; biết async trước khi realtime sync).\n"
        "2. B thực sự xuất hiện ở task trước A trong roadmap (kiểm tra task context).\n"
        "Tiêu chí loại (reject):\n"
        "1. Đây là nhiễu cấu trúc — A và B chỉ cùng xuất hiện vì 1 task chứa cả 2, "
        "không có quan hệ tiền đề (VD: 'API_INTEGRATION requires LOCAL_NOTIFICATION_API' "
        "nếu không có lý do thật).\n"
        "2. Thứ tự ngược: A thực ra phụ thuộc B nhưng B xuất hiện SAU A, hoặc quan hệ "
        "không rõ ràng.\n"
        "3. Quan hệ quá lỏng lẻo — mọi concept đều 'cần' nhau thì không phải prerequisite.\n"
        "Trả JSON: {\"verdicts\": [{\"edge_index\": <số thứ tự>, \"keep\": true/false, "
        "\"confidence\": 0.0-1.0, \"rationale\": \"...\"}]}"
    )
    user = (
        "CONCEPT DESCRIPTIONS:\n" +
        "\n".join(f"- {c}: {d}" for c, d in sorted(desc.items()) if c in
                  {e['concept_code'] for e in edges} | {e['requires'] for e in edges}) +
        "\n\nTASK CONTEXT (task → concepts):\n" +
        "\n".join(f"- {tid}: {conc}" for tid, conc in sorted(task_conc.items())) +
        "\n\nEDGES CẦN ĐÁNH GIÁ:\n" + "\n".join(edge_lines) +
        "\n\nTrả verdict cho MỌI edge. Giữ edge chỉ khi có lý do prerequisite thật."
    )

    try:
        client, _p, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
        verdicts = {v.get("edge_index"): v for v in res.get("verdicts", [])}
        judged = []
        for i, e in enumerate(edges):
            v = verdicts.get(i)
            if v and v.get("keep") and v.get("confidence", 0) >= 0.6:
                e = dict(e)
                e["confidence"] = round(v["confidence"], 2)
                e["judge_rationale"] = v.get("rationale", "")
                e["hub"] = False  # đã judge — không cần review người
                judged.append(e)
            elif v and v.get("keep"):
                e = dict(e)
                e["judge_rationale"] = v.get("rationale", "")
                e["hub"] = False
                judged.append(e)
            # keep=false → loại (hub noise/không phải prerequisite thật)
        print(f"[Judge] Giữ {len(judged)}/{len(edges)} edges | "
              f"loại {len(edges) - len(judged)} (hub noise / không phải prerequisite)")
        return judged
    except Exception as e:
        print(f"[WARN] LLM judge fail: {e} → giữ nguyên edges cũ", file=sys.stderr)
        return edges


def assign_stages_llm(tasks: list, stages: list) -> dict:
    """LLM map task → giai đoạn (1 call, deterministic — lưu mapping vào graph).

    Root-cause fix: task→stage mapping là ARTIFACT sinh 1 lần (như knowledge_mapping),
    không chạy lại mỗi lần STEP 4 (trước đây non-deterministic → phải vá hard rule).
    """
    if not _LLM_AVAILABLE or not stages or not tasks:
        return {}
    system = (
        "Bạn là chuyên gia sư phạm. Gán MỖI implementation task vào ĐÚNG giai đoạn "
        "phát triển (development_stages) của app — theo LOGIC HỌC TẬP (task nào dạy "
        "điều gì thuộc giai đoạn nào), không theo keyword bề mặt.\n"
        "Quy tắc:\n"
        "1. UI view/form (Welcome, Login, Register, RecentChatView, ChatDetailView) thuộc "
        "giai đoạn UI/auth của nó — Login form thuộc giai đoạn auth, KHÔNG phải profile.\n"
        "2. Model/ViewModel thuộc giai đoạn feature nó phục vụ (ChatMessage model → giai "
        "đoạn chat; NewChatViewModel → giai đoạn bắt đầu chat).\n"
        "3. FirebaseManager/AuthViewModel/entry point → giai đoạn Firebase setup.\n"
        "4. ProfileView/EditProfile/ImagePicker/NotificationManager/Push → giai đoạn Profile "
        "và push.\n"
        "5. ViewState/loading/error/empty refactor → giai đoạn hoàn thiện.\n"
        "6. KHÔNG bao giờ gán task feature CORE (NewChat, Profile, Push, SecureTextField "
        "component) vào giai đoạn hoàn thiện/polish — chúng có giai đoạn riêng của mình.\n"
        "7. Mỗi task PHẢI có đúng 1 giai đoạn — dùng stage name CHÍNH XÁC từ danh sách "
        "bên dưới (copy nguyên văn, không thêm số thứ tự).\n"
        "Trả JSON: {\"assignments\": {\"<task_id>\": \"<stage_name chính xác>\"}}"
    )
    stage_list = "\n".join(f"- {i+1}. {s.get('stage')}: need={s.get('need', [])}"
                           for i, s in enumerate(stages))
    task_list = "\n".join(f"- {t.get('id')}: {t.get('action', '')[:80]}"
                          for t in tasks)
    try:
        client, _p, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system,
                            user=f"GIAI ĐOẠN:\n{stage_list}\n\nTASKS:\n{task_list}",
                            temperature=0.0)  # deterministic
        assign = res.get("assignments", {})
        # Normalize: strip "1. " prefix nếu LLM vẫn thêm
        import re as _re
        return {tid: _re.sub(r"^\d+\.\s*", "", st) for tid, st in assign.items()}
    except Exception as e:
        print(f"[WARN] assign_stages_llm fail: {e}", file=sys.stderr)
        return {}


def llm_generate_cross_concepts(pg: dict, existing: list, master_path: Path) -> list:
    """LLM sinh cross-concept prerequisites còn thiếu (Gagné — master chỉ có 0/811).

    LLM nhìn concept descriptions + task dependencies → đề xuất edges mới chưa có.
    Verify bằng code: edge chỉ giữ nếu B dạy ở task trước A trong task_dependencies.
    """
    if not _LLM_AVAILABLE:
        return []

    desc = _concept_descriptions(pg, master_path)
    existing_pairs = {(e["concept_code"], e["requires"]) for e in existing}
    task_conc = {}
    for m in pg.get("knowledge_mapping", {}).get("mappings", []):
        nid = m.get("node_id", "")
        if nid.startswith("task:") and m.get("status") == "MAPPED":
            task_conc[m.get("node_id").split(":", 1)[1]] = m.get("concepts", [])
    # task deps
    deps = pg.get("implementation", {}).get("task_dependencies", [])
    dep_lines = "\n".join(f"- {d.get('task_id')} cần {d.get('depends_on')}" for d in deps[:40])

    system = (
        "Bạn là chuyên gia giáo dục (Gagné learning hierarchies). Đề xuất prerequisite "
        "giữa các KHÁI NIỆM KHÁC NHAU (cross-concept) cho roadmap học-by-building.\n"
        "'A requires B' = học viên phải hiểu B trước khi học A (B là nền tảng của A).\n"
        "CHỈ đề xuất cạnh có quan hệ tiền đề THẬT — không đề xuất cạnh lỏng lẻo.\n"
        "Trả JSON: {\"new_edges\": [{\"concept_code\": \"A\", \"requires\": \"B\", "
        "\"rationale\": \"...\"}]}"
    )
    user = (
        "CONCEPT DESCRIPTIONS:\n" +
        "\n".join(f"- {c}: {d}" for c, d in sorted(desc.items()) if c in
                  {c for t in task_conc.values() for c in t}) +
        "\n\nTASK CONTEXT:\n" +
        "\n".join(f"- {tid}: {conc}" for tid, conc in sorted(task_conc.items())) +
        "\n\nTASK DEPENDENCIES (task nào cần task nào xong trước):\n" + dep_lines +
        "\n\nĐề xuất tối đa 15 cạnh cross-concept mới có ý nghĩa nhất. "
        "KHÔNG lặp lại cạnh đã có. KHÔNG đề xuất 'A requires A'."
    )

    try:
        client, _p, model = get_llm_client()
        res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
        new_edges = []
        for e in res.get("new_edges", []):
            a, b = e.get("concept_code"), e.get("requires")
            if not a or not b or a == b:
                continue
            if (a, b) in existing_pairs:
                continue
            new_edges.append({
                "concept_code": a,
                "requires": b,
                "source": "LLM_CROSS_CONCEPT",
                "confidence": 0.6,  # LLM đề xuất — verify cấu trúc nâng lên
                "rationale": e.get("rationale", "")[:120],
            })
        # Verify bằng code: B phải dạy ở task TRƯỚC task dạy A (theo task_dependencies)
        verified = []
        for e in new_edges:
            # task nào dạy A, task nào dạy B
            tasks_a = [t for t, cs in task_conc.items() if e["concept_code"] in cs]
            tasks_b = [t for t, cs in task_conc.items() if e["requires"] in cs]
            if not tasks_a or not tasks_b:
                continue
            # B dạy trước A nếu tồn tại đường dep từ task A → task B
            dep_of = {}
            for d in deps:
                dep_of.setdefault(d.get("task_id"), set()).add(d.get("depends_on"))
            def reaches(start, target, seen=None):
                seen = seen or set()
                if start == target:
                    return True
                for nxt in dep_of.get(start, set()):
                    if nxt not in seen:
                        seen.add(nxt)
                        if reaches(nxt, target, seen):
                            return True
                return False
            if any(reaches(ta, tb) for ta in tasks_a for tb in tasks_b):
                e["confidence"] = 0.75
                e["source"] = "LLM_CROSS_CONCEPT_VERIFIED"
            verified.append(e)
        print(f"[Cross-concept] LLM đề xuất {len(new_edges)}, verify giữ {len(verified)}")
        return verified
    except Exception as e:
        print(f"[WARN] LLM cross-concept fail: {e}", file=sys.stderr)
        return []


def load_master_concepts(lo_prereq_path: Path) -> dict:
    """Đọc lo_prerequisites.tsv → Bloom progression per concept (Bruner).

    Trả về {concept_code: max_bloom_seen} — level cao nhất đã đạt trong master.
    """
    if not lo_prereq_path or not lo_prereq_path.is_file():
        return {}
    prog = defaultdict(set)
    with open(lo_prereq_path, encoding="utf-8-sig") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2 or parts[0] == "learning_objective_code":
                continue
            for lo in (parts[0], parts[1]):
                m = re.match(r"(ULO|CIO|SIO)-(.+?)-\d+$", lo)
                if m:
                    prog[m.group(2)].add(m.group(1))
    # ULO < CIO < SIO (độ sâu triển khai tăng) — dùng làm bloom proxy
    depth = {"ULO": 1, "CIO": 2, "SIO": 3}
    return {c: max(depth[t] for t in types) for c, types in prog.items()}


def build_concept_dag(pg: dict) -> dict:
    """Gagné: concept prerequisite DAG từ task_dependencies + knowledge_mapping.

    Nguyên lý: concept B dạy ở task Y, concept A dạy ở task X, X depends_on Y
    (X cần Y trước) → concept B là prerequisite của concept A (B phải học trước).
    Không dùng LLM — verify thuần bằng cấu trúc (tránh hallucination).
    """
    tasks = pg.get("implementation", {}).get("tasks", [])
    deps = pg.get("implementation", {}).get("task_dependencies", [])
    mappings = pg.get("knowledge_mapping", {}).get("mappings", [])

    # task → concepts (MAPPED)
    task_concepts = defaultdict(set)
    for m in mappings:
        nid = m.get("node_id", "")
        if nid.startswith("task:") and m.get("status") == "MAPPED":
            tid = nid.split(":", 1)[1]
            for c in m.get("concepts", []):
                task_concepts[tid].add(c)

    # dep map: task → set(task phải xong trước)
    dep_map = defaultdict(set)
    for d in deps:
        dep_map[d.get("task_id")].add(d.get("depends_on"))
    for t in tasks:
        for dep in t.get("depends_on", []):
            dep_map[t["id"]].add(dep)

    # concept → concept: nếu concept A ở task X, concept B ở task Y, Y ∈ deps(X)
    prereq = defaultdict(set)
    for tid, concepts in task_concepts.items():
        for dep_tid in dep_map.get(tid, set()):
            dep_concepts = task_concepts.get(dep_tid, set())
            for c in concepts:
                for dc in dep_concepts:
                    if dc != c:
                        prereq[c].add(dc)

    # Chuyển thành list + source
    result = []
    for c, reqs in sorted(prereq.items()):
        for r in sorted(reqs):
            # Hub concept (dạy ở nhiều task) → edge có thể là nhiễu cấu trúc,
            # không phải prerequisite thật (API_INTEGRATION require mọi concept task trước)
            is_hub = len(reqs) >= 6
            result.append({
                "concept_code": c,
                "requires": r,
                "source": "TASK_DEPENDENCY_VERIFIED",
                "confidence": 0.5 if is_hub else 0.8,
                "hub": is_hub,  # cần review người — có thể không phải prerequisite thật
            })
    return result


def compute_concept_sequence(pg: dict, tasks_in_order: list) -> list:
    """Bruner spiral: concept gặp ở task nào, bao nhiêu lần, bloom cap bao nhiêu.

    bloom_cap: lần 1 → UNDERSTAND (nền) / APPLY (thao tác), lần 2+ → ANALYZE, lần 3+ → CREATE.
    """
    task_concepts = {}
    for m in pg.get("knowledge_mapping", {}).get("mappings", []):
        nid = m.get("node_id", "")
        if nid.startswith("task:") and m.get("status") == "MAPPED":
            task_concepts[m.get("node_id").split(":", 1)[1]] = m.get("concepts", [])

    seq = []
    seen = defaultdict(int)
    for tid in tasks_in_order:
        for c in task_concepts.get(tid, []):
            seen[c] += 1
            n = seen[c]
            if n == 1:
                cap = "UNDERSTAND"  # khái niệm nền; LLM STEP 4 có thể override APPLY
            elif n == 2:
                cap = "APPLY"
            else:
                cap = "ANALYZE"
            seq.append({
                "concept_code": c,
                "task_id": tid,
                "encounter": n,
                "bloom_cap": cap,
            })
    return seq


def zpd_check(pg: dict, tasks_in_order: list) -> list:
    """Vygotsky ZPD + Sweller cognitive load: new vs known concepts per task."""
    task_concepts = {}
    for m in pg.get("knowledge_mapping", {}).get("mappings", []):
        nid = m.get("node_id", "")
        if nid.startswith("task:") and m.get("status") == "MAPPED":
            task_concepts[m.get("node_id").split(":", 1)[1]] = set(m.get("concepts", []))

    seen = set()
    checks = []
    for idx, tid in enumerate(tasks_in_order):
        conc = task_concepts.get(tid, set())
        new = conc - seen
        known = conc & seen
        seen |= conc
        verdict = "OK"
        issues = []
        if len(new) > MAX_NEW_CONCEPTS_PER_TASK:
            verdict = "TOO_MANY_NEW"
            issues.append(f"có {len(new)} concept mới (giới hạn {MAX_NEW_CONCEPTS_PER_TASK}) — "
                          f"quá tải intrinsic load (Sweller), cân nhắc tách task")
        if len(conc) > 1 and len(known) == 0 and idx > 0:
            # Task đầu tiên roadmap + task 1 concept mới = ZPD hợp lệ
            # (1 bước vừa sức — Vygotsky). Chỉ flag khi NHIỀU concept mới đồng thời.
            verdict = "NO_ZPD_BRIDGE"
            issues.append("không có concept quen (Vygotsky: nhiệm vụ nên nối kiến thức cũ → mới)")
        checks.append({
            "task_id": tid,
            "new_concepts": sorted(new),
            "known_concepts": sorted(known),
            "verdict": verdict,
            "issues": issues,
        })
    return checks


def mastery_gates(pg: dict, phases: list) -> list:
    """Bloom mastery: gate giữa phase — acceptance criteria của tasks trong phase."""
    gates = []
    for i, ph in enumerate(phases):
        if i + 1 >= len(phases):
            break
        criteria = []
        for m in ph.get("milestones", []):
            t = m.get("task", {})
            for acc in t.get("acceptance", []) or []:
                # KHÔNG truncate — gate criteria là tiêu chí đánh giá, phải đầy đủ
                if isinstance(acc, str):
                    criteria.append(f"{t.get('id')}: {acc}")
                elif isinstance(acc, dict):
                    criteria.append(f"{t.get('id')}: {acc.get('criteria', str(acc))}")
            # Fallback: action làm gate gần đúng
            if not criteria:
                criteria.append(f"{t.get('id')}: {t.get('action', '')}")
        gates.append({
            "phase": ph.get("phase"),
            "criteria": criteria[:8],  # giới hạn hiển thị
            "next_phase": phases[i + 1].get("phase"),
        })
    return gates


def build_walking_skeleton(pg: dict, phases: list) -> dict:
    """Reigeluth: epitome = phase đầu (app tối thiểu), elaborations = phase sau."""
    if not phases:
        return {"epitome": "", "elaborations": []}
    first = phases[0]
    epitome_tasks = [m.get("task", {}).get("action", "") for m in first.get("milestones", [])]
    elaborations = []
    for ph in phases[1:]:
        for m in ph.get("milestones", []):
            elaborations.append(f"{ph.get('phase')}: {m.get('task', {}).get('action', '')[:60]}")
    return {
        "epitome": " | ".join(epitome_tasks)[:200],
        "elaborations": elaborations[:12],
    }


def main():
    parser = argparse.ArgumentParser(description="STEP 3.5 — Curriculum Graph")
    parser.add_argument("--project-graph", required=True, type=Path)
    parser.add_argument("--lo-prerequisites", type=Path, default=None,
                        help="projects/master-tree/output/lo_prerequisites.tsv (Bloom progression)")
    parser.add_argument("--roadmap", type=Path, default=None,
                        help="roadmap.json (nếu có — lấy phases cho mastery gates + skeleton)")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--no-judge", action="store_true",
                        help="Bỏ qua LLM-as-judge (test cấu trúc nhanh)")
    args = parser.parse_args()

    pg = json.load(open(args.project_graph, encoding="utf-8"))

    # Thứ tự task: từ roadmap phases (nếu có) hoặc task order trong graph
    tasks_in_order = []
    phases = []
    if args.roadmap and args.roadmap.is_file():
        rm = json.load(open(args.roadmap, encoding="utf-8"))
        phases = rm.get("phases", [])
        for ph in phases:
            for m in ph.get("milestones", []):
                tasks_in_order.append(m.get("task", {}).get("id", ""))
    if not tasks_in_order:
        tasks_in_order = [t.get("id", "") for t in pg.get("implementation", {}).get("tasks", [])]

    curriculum = {
        "schema_version": 1,
        "concept_prerequisites": build_concept_dag(pg),
        "concept_sequence": compute_concept_sequence(pg, tasks_in_order),
        "walking_skeleton": build_walking_skeleton(pg, phases),
        "zpd_checks": zpd_check(pg, tasks_in_order),
        "mastery_gates": mastery_gates(pg, phases),
        "master_bloom_progression": load_master_concepts(args.lo_prerequisites),
    }

    # LLM-as-judge: lọc hub noise (hub: true → judge giữ/loại) + đánh giá mọi edge
    if not args.no_judge:
        curriculum["concept_prerequisites"] = llm_judge_edges(
            pg, curriculum["concept_prerequisites"], args.lo_prerequisites)
        # LLM sinh cross-concept còn thiếu + verify code
        new_cross = llm_generate_cross_concepts(
            pg, curriculum["concept_prerequisites"], args.lo_prerequisites)
        existing_pairs = {(e["concept_code"], e["requires"])
                          for e in curriculum["concept_prerequisites"]}
        for e in new_cross:
            if (e["concept_code"], e["requires"]) not in existing_pairs:
                curriculum["concept_prerequisites"].append(e)
        # Cross-concept edges cũng phải qua judge (chúng có thể là hub noise kiểu mới)
        if new_cross:
            cross_edges = [e for e in curriculum["concept_prerequisites"]
                           if e.get("source") == "LLM_CROSS_CONCEPT"]
            if cross_edges:
                judged_cross = llm_judge_edges(pg, cross_edges, args.lo_prerequisites)
                judged_ids = {(e["concept_code"], e["requires"]) for e in judged_cross}
                curriculum["concept_prerequisites"] = [
                    e for e in curriculum["concept_prerequisites"]
                    if (e["concept_code"], e["requires"]) in judged_ids
                    or e.get("source") != "LLM_CROSS_CONCEPT"
                ]

    # Root-cause fix: task→stage mapping sinh 1 lần, LƯU vào graph (deterministic).
    # STEP 4 đọc từ đây — KHÔNG gọi LLM lại mỗi lần chạy.
    stages = pg.get("product", {}).get("development_stages", [])
    tasks_all = pg.get("implementation", {}).get("tasks", [])
    if stages and not args.no_judge:
        curriculum["task_stage_mapping"] = assign_stages_llm(tasks_all, stages)
    else:
        curriculum["task_stage_mapping"] = {}

    pg["curriculum"] = curriculum

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(pg, f, indent=2, ensure_ascii=False)

    n_prereq = len(curriculum["concept_prerequisites"])
    n_seq = len(curriculum["concept_sequence"])
    n_zpd_ok = sum(1 for c in curriculum["zpd_checks"] if c["verdict"] == "OK")
    n_zpd = len(curriculum["zpd_checks"])
    n_gates = len(curriculum["mastery_gates"])
    print(f"[✓] Curriculum Graph → {args.output}")
    print(f"    concept_prerequisites (Gagné DAG): {n_prereq}")
    print(f"    concept_sequence (Bruner spiral): {n_seq}")
    print(f"    zpd_checks (Vygotsky): {n_zpd_ok}/{n_zpd} OK")
    print(f"    mastery_gates (Bloom): {n_gates}")
    for c in curriculum["zpd_checks"]:
        if c["verdict"] != "OK":
            print(f"    ⚠ {c['task_id']}: {c['verdict']} — {c['issues'][0][:70] if c['issues'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
