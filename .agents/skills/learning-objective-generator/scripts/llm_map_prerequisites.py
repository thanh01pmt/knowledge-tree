#!/usr/bin/env python3
"""
llm_map_prerequisites.py (v3) — Phase E: Prerequisite Mapping theo ADR-0005
Domain-Partitioned Concept DAG + LLM Verify.

4 Bước:
  Bước 1 — Domain Partitioning (deterministic): chia concepts theo topic
  Bước 2 — Concept-Level DAG per-domain (LLM có constraint justification)
  Bước 4 — ULO-Level Derivation (deterministic từ concept DAG + L1 Bloom)
  Bước 5 — Phép thử ngược (LLM verify từng link → drop false positives)
  Bước 6 — Export TSV cho Human Review

Outputs:
  output/lo_prerequisites.tsv  (có source_layer, justification, counterfactual_test)
  output/.work/concept_dag.tsv  (concept-level DAG per-topic)
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ─── env / client ──────────────────────────────────────────────────────────
def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()

def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))

def load_status(repo_root: Path) -> dict:
    res = {}
    sf = repo_root / "status.yaml"
    if sf.is_file():
        for line in sf.read_text(encoding="utf-8").splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                res[k.strip()] = v.strip().strip("'\"")
    return res

def get_client():
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY không tìm thấy.", file=sys.stderr)
        sys.exit(1)
    base_url = os.environ.get("OPENAI_BASE_URL") or None
    try:
        import httpx
        http_client = httpx.Client(transport=httpx.HTTPTransport())
        return OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
    except Exception:
        return OpenAI(api_key=api_key, base_url=base_url)

def llm_json(client, model, system, user, temperature=0.1):
    """Gọi LLM trả JSON. Parse robust."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    raw = (completion.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"```(?:json)?\n?", "", raw).strip("` \n")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r'\{[\s\S]*\}', raw)
        return json.loads(m.group()) if m else {}

# ─── Bloom ordering (giữ từ ADR-0004 L1) ───────────────────────────────────
BLOOM_ORDER = {
    "Remember": 1, "Remembering": 1,
    "Understand": 2, "Understanding": 2,
    "Apply": 3, "Applying": 3,
    "Analyze": 4, "Analyzing": 4,
    "Evaluate": 5, "Evaluating": 5,
    "Create": 6, "Creating": 6,
}

def bloom_rank(level: str) -> int:
    if not level:
        return 0
    for k, v in BLOOM_ORDER.items():
        if k.lower() in level.lower():
            return v
    return 0

# =====================================================================
# Bước 1 — Domain Partitioning (Deterministic)
# =====================================================================
def partition_concepts_by_topic(concepts: list[dict]) -> dict[str, list[dict]]:
    """Chia concepts theo topic_codes. Concept multi-topic → xuất hiện trong nhiều topic."""
    by_topic = defaultdict(list)
    for c in concepts:
        for t in (c.get("topic_codes") or "").split(","):
            t = t.strip()
            if t:
                by_topic[t].append(c)
    return dict(by_topic)

# =====================================================================
# Bước 2 — Concept-Level DAG per-domain (LLM có constraint)
# =====================================================================
STEP2_SYSTEM = """Bạn là một Chuyên gia Thiết kế Curriculum am hiểu về Prerequisite Sequencing.

Nhiệm vụ: Xây dựng DAG tiên đề (prerequisite) giữa các CONCEPT trong cùng 1 domain/topic.

MỖI link BẮT BUỘC justify theo 1 trong 2 mẫu (KHÔNG được dùng mẫu khác):
  1. "Tool dependency": B sử dụng A như công cụ/khái niệm nền (VD: Loop dùng biến đếm → Variables là prereq của Loop)
  2. "Conceptual foundation": B mở rộng/kế thừa A (VD: while-loop extends control-flow)

CẤM các mẫu justification mơ hồ:
  - "liên quan", "cùng domain", "thường học trước"
  - "giúp hiểu tốt hơn", "có liên hệ"
Chỉ tạo link khi THỰC SỰ cần thiết: sinh viên chưa học A thì KHÔNG THỂ hiểu/làm được B.

Trả về JSON:
{
  "links": [
    {
      "prereq_concept": "CONCEPT_A_CODE",
      "target_concept": "CONCEPT_B_CODE",
      "justification": "Tool dependency | Conceptual foundation: ...",
      "counterfactual_test": "NO - sinh viên không biết A thì không thể B vì..."
    }
  ]
}

Quy tắc counterfactual_test:
  - "NO" = A là prereq bắt buộc (giữ link)
  - "YES" = A không phải prereq (sẽ bị drop)
"""

def build_concept_dag_per_topic(client, model, topic_code: str, concepts: list[dict]) -> list[dict]:
    """Gọi LLM build DAG cho 1 topic."""
    concept_lines = []
    for c in concepts:
        concept_lines.append(
            f"- {c['code']}: {c.get('name','')} — {c.get('description','')[:150]}"
        )
    concepts_text = "\n".join(concept_lines)

    user_prompt = f"""=== DOMAIN/TOPIC: {topic_code} ===
Concepts trong domain này ({len(concepts)} concepts):
{concepts_text}

Hãy xây dựng DAG tiên đề giữa các concepts trên theo quy tắc đã nêu.

HƯỚNG DẪN: Hãy tích cực tìm các quan hệ tiên đề thật sự. Trong 1 domain kỹ thuật, thường có 30-60% cặp concept có quan hệ tiên đề. Đừng quá thận trọng — nếu B thực sự cần A làm nền, hãy tạo link.

Nhớ: chỉ link khi THỰC SỰ bắt buộc (sinh viên chưa học A thì KHÔNG THỂ hiểu/làm B), nhưng đừng skip link chỉ vì "có thể học song song".
"""
    data = llm_json(client, model, STEP2_SYSTEM, user_prompt, temperature=0.2)
    valid_codes = {c["code"] for c in concepts}
    links = []
    for lk in data.get("links", []):
        pre = (lk.get("prereq_concept") or "").strip()
        tgt = (lk.get("target_concept") or "").strip()
        just = (lk.get("justification") or "").strip()
        test = (lk.get("counterfactual_test") or "").strip()
        if pre in valid_codes and tgt in valid_codes and pre != tgt:
            links.append({
                "topic_code": topic_code,
                "prereq_concept": pre,
                "target_concept": tgt,
                "justification": just,
                "counterfactual_test": test,
            })
    return links

def derive_concept_dag(client, model, by_topic: dict[str, list[dict]], runs: int = 2) -> list[dict]:
    """Bước 2: chạy LLM cho từng topic, gộp kết quả qua N runs (union).
    Link được giữ nếu xuất hiện ở ≥ ceil(runs/2) runs (majority vote)."""
    from collections import Counter
    all_runs = []  # list of dict[(pre,tgt)] -> link
    for run_idx in range(runs):
        print(f"  --- Run {run_idx+1}/{runs} ---")
        run_links = {}
        for topic_code, concepts in by_topic.items():
            if len(concepts) < 2:
                continue
            print(f"  [B2] Topic {topic_code} ({len(concepts)} concepts)...", end=" ", flush=True)
            links = build_concept_dag_per_topic(client, model, topic_code, concepts)
            new_count = 0
            for l in links:
                key = (l["prereq_concept"], l["target_concept"])
                if key not in run_links:
                    run_links[key] = l
                    new_count += 1
            print(f"{len(links)} links ({new_count} new)")
        all_runs.append(run_links)
    # Majority vote: giữ link nếu xuất hiện ở >= ceil(runs/2) runs
    threshold = (runs + 1) // 2  # runs=2 → 1 (union), runs=3 → 2 (majority)
    link_counter = Counter()
    link_data = {}
    for run in all_runs:
        for key, l in run.items():
            link_counter[key] += 1
            link_data[key] = l
    final_links = []
    for key, cnt in link_counter.items():
        if cnt >= threshold:
            l = link_data[key]
            l["confidence_runs"] = f"{cnt}/{runs}"
            final_links.append(l)
    return final_links

# =====================================================================
# Bước 4 — ULO-Level Derivation (Deterministic)
# =====================================================================
def derive_layer1_bloom(los: list[dict]) -> list[dict]:
    """L1-BLOOM: CIO trong cùng ULO + SIO trong cùng CIO, theo bloom level."""
    links = []
    by_parent_cio = defaultdict(list)
    for lo in los:
        if lo["lo_type"] == "CONCEPTUAL_IMPL":
            by_parent_cio[lo["parent_lo_code"]].append(lo)
    for ulo_code, cios in by_parent_cio.items():
        cios_sorted = sorted(cios, key=lambda c: bloom_rank(c.get("bloom_level", "")))
        for prev, curr in zip(cios_sorted, cios_sorted[1:]):
            if bloom_rank(prev.get("bloom_level", "")) != bloom_rank(curr.get("bloom_level", "")):
                links.append({
                    "learning_objective_code": curr["code"],
                    "prerequisite_lo_code": prev["code"],
                    "rationale": f"CIO {prev.get('bloom_level','?')} → {curr.get('bloom_level','?')} trong cùng ULO {ulo_code}",
                    "source_layer": "L1-BLOOM-CIO",
                    "justification": "Bloom ordering trong cùng parent ULO",
                    "counterfactual_test": "NO — CIO cấp thấp là nền bắt buộc của CIO cấp cao",
                })
    by_parent_sio = defaultdict(list)
    for lo in los:
        if lo["lo_type"] == "SPECIFIC_IMPL":
            by_parent_sio[lo["parent_lo_code"]].append(lo)
    for cio_code, sios in by_parent_sio.items():
        sios_sorted = sorted(sios, key=lambda s: bloom_rank(s.get("bloom_level", "")))
        for prev, curr in zip(sios_sorted, sios_sorted[1:]):
            if bloom_rank(prev.get("bloom_level", "")) != bloom_rank(curr.get("bloom_level", "")):
                links.append({
                    "learning_objective_code": curr["code"],
                    "prerequisite_lo_code": prev["code"],
                    "rationale": f"SIO {prev.get('bloom_level','?')} → {curr.get('bloom_level','?')} trong cùng CIO {cio_code}",
                    "source_layer": "L1-BLOOM-SIO",
                    "justification": "Bloom ordering trong cùng parent CIO",
                    "counterfactual_test": "NO — SIO cấp thấp là nền bắt buộc của SIO cấp cao",
                })
    return links

def derive_ulo_from_concept_dag(concept_dag: list[dict], ulos: list[dict]) -> list[dict]:
    """Bước 4: concept DAG → ULO DAG. ULO representative = bloom thấp nhất."""
    concept_to_ulos = defaultdict(list)
    for u in ulos:
        for c in (u.get("concept_codes") or "").split(","):
            c = c.strip()
            if c:
                concept_to_ulos[c].append(u)
    ulo_by_code = {u["code"]: u for u in ulos}

    def representative_ulo(concept_code: str) -> str | None:
        ulos_for_c = concept_to_ulos.get(concept_code, [])
        if not ulos_for_c:
            return None
        return sorted(ulos_for_c, key=lambda u: bloom_rank(u.get("bloom_level", "")))[0]["code"]

    links = []
    for edge in concept_dag:
        pre_ulo = representative_ulo(edge["prereq_concept"])
        tgt_ulo = representative_ulo(edge["target_concept"])
        if not pre_ulo or not tgt_ulo or pre_ulo == tgt_ulo:
            continue
        links.append({
            "learning_objective_code": tgt_ulo,
            "prerequisite_lo_code": pre_ulo,
            "rationale": edge["justification"][:200],
            "source_layer": "L4-CONCEPT-DAG",
            "justification": edge["justification"],
            "counterfactual_test": edge["counterfactual_test"],
        })
    return links

# =====================================================================
# Bước 5 — Phép thử ngược (LLM verify từng link)
# =====================================================================
STEP5_SYSTEM = """Bạn là một evaluator xác minh tính hợp lệ của liên kết tiền đề (prerequisite).

Bạn nhận được 1 link: A là tiền đề của B.
Câu hỏi kiểm tra: "Sinh viên đã hiểu mọi concept TRỪ A. Có thể hiểu/làm được B không?"

Quy tắc:
- "NO" = A là prereq BẮT BUỘC (giữ link). Sinh viên thiếu A thì KHÔNG THỂ hiểu/làm B.
- "YES" = A KHÔNG phải prereq (drop link). Sinh viên vẫn hiểu/làm B mà không cần A.
- "PARTIAL" = A giúp hiểu B nhưng không bắt buộc → drop.

QUAN TRỌNG — đừng quá khắt khe:
- KHÔNG yêu cầu description của B phải nhắc đích danh A. Description thường viết ngắn, không liệt kê mọi nền tảng.
- Ví dụ: B="Container views" description chỉ nói "sắp xếp view con". KHÔNG nhắc "view" đích danh, nhưng RÕ RÀNG cần hiểu View trước. → verdict NO (giữ).
- Phép thử thật: "Sinh viên chưa học A, có THỰC SỰ hiểu/làm được B không?" — dùng kiến thức sư phạm, không match keyword trong description.
- Nếu A là khái niệm nền tảng hiển nhiên (VD: View → Container Views, Data Types → Variables) → verdict NO.

CẢNH BÁO justification bịa:
- Đọc name + description. Nếu justification nói "B sử dụng A" nhưng A và B hoàn toàn khác domain/không liên quan thực sự → verdict YES.
- Ví dụ: A="Object Properties" (thuộc tính đối tượng), B="Visual Design" (cân bằng, tương phản). → verdict YES (drop, justification bịa).

Trả về JSON:
{"verdict": "NO" | "YES" | "PARTIAL", "reason": "lý do ngắn 1 câu"}
"""

def verify_link(client, model, lo_map: dict, link: dict) -> str:
    """Trả về verdict NO/YES/PARTIAL."""
    pre = lo_map.get(link["prerequisite_lo_code"], {})
    tgt = lo_map.get(link["learning_objective_code"], {})
    user_prompt = f"""Link đang xét:
A (prereq) = {link['prerequisite_lo_code']}
  name: {pre.get('name','')}
  description: {pre.get('description','')[:300]}
  bloom: {pre.get('bloom_level','')}
  concepts: {pre.get('concept_codes','')}

B (target) = {link['learning_objective_code']}
  name: {tgt.get('name','')}
  description: {tgt.get('description','')[:300]}
  bloom: {tgt.get('bloom_level','')}
  concepts: {tgt.get('concept_codes','')}

Justification đã có: {link.get('justification','')}

Câu hỏi: "Sinh viên đã hiểu mọi concept TRỪ A. Có thể hiểu/làm được B không?"
Hãy đọc kỹ description của A và B. Nếu justification mô tả sai nội dung B (không khớp description) → verdict YES (drop).
"""
    data = llm_json(client, model, STEP5_SYSTEM, user_prompt, temperature=0.0)
    verdict = (data.get("verdict") or "").upper().strip()
    reason = (data.get("reason") or "").strip()
    if verdict not in ("NO", "YES", "PARTIAL"):
        # Fallback: parse text
        if "no" in verdict.lower():
            verdict = "NO"
        elif "yes" in verdict.lower():
            verdict = "YES"
        else:
            verdict = "PARTIAL"
    return f"{verdict} — {reason}"

def verify_links_batch(client, model, lo_map: dict, links: list[dict]) -> list[dict]:
    """Bước 5: verify từng link (chỉ L4-CONCEPT-DAG, L1 đã chắc chắn)."""
    to_verify = [l for l in links if l["source_layer"] == "L4-CONCEPT-DAG"]
    print(f"\n[Bước 5] Verify {len(to_verify)} links L4-CONCEPT-DAG...")
    kept = []
    dropped = []
    for i, l in enumerate(to_verify):
        if i % 10 == 0:
            print(f"  [{i}/{len(to_verify)}]...", flush=True)
        verdict = verify_link(client, model, lo_map, l)
        l["counterfactual_test"] = verdict
        if verdict.startswith("NO"):
            l["source_layer"] = "L5-VERIFIED"
            kept.append(l)
        else:
            dropped.append(l)
    print(f"  → Kept {len(kept)}, Dropped {len(dropped)} (YES/PARTIAL)")
    # L1-BLOOM links luôn giữ
    l1_links = [l for l in links if l["source_layer"].startswith("L1")]
    return l1_links + kept, dropped

# =====================================================================
# Cycle detection (Kahn topological)
# =====================================================================
def break_cycles(links: list[dict]) -> tuple[list[dict], list[dict]]:
    from collections import defaultdict, deque
    priority = {"L5-VERIFIED": 0, "L4-CONCEPT-DAG": 1,
                "L1-BLOOM-CIO": 2, "L1-BLOOM-SIO": 2}
    remaining = list(links)
    dropped = []
    def kahn_detect(adj):
        all_nodes = set()
        for tgt, pres in adj.items():
            all_nodes.add(tgt); all_nodes.update(pres)
        indeg = {n: 0 for n in all_nodes}
        for tgt, pres in adj.items():
            for p in pres: indeg[tgt] += 1
        q = deque([n for n in all_nodes if indeg[n] == 0])
        visited = set()
        while q:
            n = q.popleft(); visited.add(n)
            for tgt, pres in adj.items():
                if n in pres:
                    indeg[tgt] -= 1
                    if indeg[tgt] == 0 and tgt not in visited:
                        q.append(tgt)
        return all_nodes - visited
    for _ in range(500):
        adj = defaultdict(set)
        for l in remaining:
            adj[l["learning_objective_code"]].add(l["prerequisite_lo_code"])
        cycle_nodes = kahn_detect(adj)
        if not cycle_nodes:
            break
        candidate = []
        for idx, l in enumerate(remaining):
            if (l["learning_objective_code"] in cycle_nodes
                    and l["prerequisite_lo_code"] in cycle_nodes):
                candidate.append((priority.get(l["source_layer"], 9), idx, l))
        if not candidate:
            break
        candidate.sort(key=lambda x: -x[0])
        _, idx, drop = candidate[0]
        dropped.append(drop)
        remaining.pop(idx)
    return remaining, dropped

# =====================================================================
# Concept prereq (cho concepts.tsv)
# =====================================================================
def build_concept_prereqs(links: list[dict], ulos: list[dict]) -> dict:
    ulo_to_concepts = {}
    for u in ulos:
        cs = [c.strip() for c in (u.get("concept_codes") or "").split(",") if c.strip()]
        ulo_to_concepts[u["code"]] = cs
    result = defaultdict(set)
    for l in links:
        for tgt_c in ulo_to_concepts.get(l["learning_objective_code"], []):
            for pre_c in ulo_to_concepts.get(l["prerequisite_lo_code"], []):
                if tgt_c != pre_c:
                    result[tgt_c].add(pre_c)
    return {k: sorted(v) for k, v in result.items()}

def update_concepts_tsv(concepts_path: Path, concept_prereqs: dict):
    rows = []
    fieldnames = None
    with open(concepts_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)
    if "prerequisite_concept_codes" not in fieldnames:
        fieldnames.append("prerequisite_concept_codes")
    for row in rows:
        prereqs = concept_prereqs.get(row["code"], [])
        row["prerequisite_concept_codes"] = ",".join(prereqs)
    with open(concepts_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

# =====================================================================
# Main
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="Phase E v3 (ADR-0005): Domain-Partitioned Concept DAG + LLM Verify")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--model", default="deepseek-v4-flash:cloud", help="LLM model")
    parser.add_argument("--dry-run", action="store_true", help="In candidate DAG, không ghi TSV")
    parser.add_argument("--no-verify", action="store_true", help="Bỏ Bước 5 (verify)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)
    slug = args.project or load_status(repo_root).get("active_project")
    if not slug:
        print("[ERROR] Cần --project hoặc active_project.", file=sys.stderr)
        sys.exit(1)

    project_dir = repo_root / "projects" / slug
    out_dir = project_dir / "output"
    work_dir = project_dir / ".work"

    lo_tsv = out_dir / "learning-objectives.tsv"
    concepts_tsv = out_dir / "concepts.tsv"

    # Load
    los = []
    with open(lo_tsv, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            los.append(row)
    ulos = [l for l in los if l["lo_type"] == "UNIVERSAL"]
    lo_map = {l["code"]: l for l in los}
    print(f"[*] Load {len(los)} LOs ({len(ulos)} ULOs).")

    concepts = []
    with open(concepts_tsv, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            concepts.append(row)
    print(f"[*] Load {len(concepts)} concepts.")

    client = get_client()

    # ── Bước 1: Domain Partitioning ──
    print("\n[Bước 1] Domain Partitioning...")
    by_topic = partition_concepts_by_topic(concepts)
    topics_with_multiple = {t: cs for t, cs in by_topic.items() if len(cs) >= 2}
    print(f"  → {len(by_topic)} topics, {len(topics_with_multiple)} có ≥2 concepts (sẽ chạy LLM)")

    # ── Bước 2: Concept-Level DAG per-domain ──
    print("\n[Bước 2] Concept-Level DAG per-domain (LLM)...")
    concept_dag = derive_concept_dag(client, args.model, by_topic)
    print(f"  → {len(concept_dag)} concept-level links (trước verify)")

    # Lưu concept_dag.tsv vào .work
    work_dir.mkdir(parents=True, exist_ok=True)
    concept_dag_path = work_dir / "concept_dag.tsv"
    with open(concept_dag_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["topic_code", "prereq_concept", "target_concept", "justification", "counterfactual_test", "confidence_runs"], delimiter="\t")
        w.writeheader()
        for l in concept_dag:
            w.writerow({k: l.get(k, "") for k in ["topic_code","prereq_concept","target_concept","justification","counterfactual_test","confidence_runs"]})
    print(f"  → Lưu {concept_dag_path.relative_to(repo_root)}")

    # ── Bước 4: ULO-Level Derivation ──
    print("\n[Bước 4] ULO-Level Derivation (deterministic từ concept DAG)...")
    l1_links = derive_layer1_bloom(los)
    l4_links = derive_ulo_from_concept_dag(concept_dag, ulos)
    print(f"  L1-BLOOM: {len(l1_links)} links")
    print(f"  L4-CONCEPT-DAG: {len(l4_links)} links")
    all_links = l1_links + l4_links

    # ── Bước 5: Phép thử ngược (LLM verify) ──
    dropped_verify = []
    if not args.no_verify:
        all_links, dropped_verify = verify_links_batch(client, args.model, lo_map, all_links)
    else:
        print("\n[Bước 5] SKIP (--no-verify)")

    # ── Cycle break ──
    print("\n[Cycle] Kahn topological...")
    kept, dropped_cycle = break_cycles(all_links)
    if dropped_cycle:
        print(f"  Dropped {len(dropped_cycle)} links gây cycle:")
        for d in dropped_cycle:
            print(f"    - {d['prerequisite_lo_code']} -> {d['learning_objective_code']}")
    print(f"  Final: {len(kept)} acyclic links")

    # Stats
    from collections import Counter
    by_source = Counter(l["source_layer"] for l in kept)
    print("\n[Phân bổ source_layer]:")
    for src, cnt in sorted(by_source.items()):
        print(f"  {src:<25} {cnt:>4}")

    ulos_covered = ({l["learning_objective_code"] for l in kept if l["learning_objective_code"].startswith("ULO-")}
                    | {l["prerequisite_lo_code"] for l in kept if l["prerequisite_lo_code"].startswith("ULO-")})
    print(f"\n[Coverage ULO] {len(ulos_covered)}/{len(ulos)} ({100*len(ulos_covered)/max(len(ulos),1):.0f}%)")

    if args.dry_run:
        print("\n========== DRY-RUN — KHÔNG ghi TSV ==========")
        print("\n--- Concept DAG (Bước 2) ---")
        for l in concept_dag[:30]:
            print(f"  {l['prereq_concept']:<28} → {l['target_concept']:<28}  [{l['topic_code']}]")
            print(f"    justification: {l['justification'][:90]}")
        if len(concept_dag) > 30:
            print(f"  ... ({len(concept_dag)-30} links nữa)")
        print("\n--- Final ULO links (sau verify + cycle-break) ---")
        for l in kept:
            print(f"  {l['prerequisite_lo_code']:<28} → {l['learning_objective_code']:<28}  [{l['source_layer']}]  {l['rationale'][:60]}")
        if dropped_verify:
            print(f"\n--- DROPPED by verify ({len(dropped_verify)}) ---")
            for l in dropped_verify:
                print(f"  {l['prerequisite_lo_code']:<28} → {l['learning_objective_code']:<28}  {l.get('counterfactual_test','')[:60]}")
        print("\n[Dry-run] Để ghi TSV, chạy lại không có --dry-run")
        return

    # ── Ghi TSV ──
    out_tsv = out_dir / "lo_prerequisites.tsv"
    fieldnames = ["learning_objective_code", "prerequisite_lo_code", "rationale", "source_layer", "justification", "counterfactual_test"]
    with open(out_tsv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        for l in kept:
            row = {k: l.get(k, "") for k in fieldnames}
            w.writerow(row)
    print(f"\n[✓] Ghi {len(kept)} links -> {out_tsv.relative_to(repo_root)}")

    concept_prereqs = build_concept_prereqs(kept, ulos)
    update_concepts_tsv(concepts_tsv, concept_prereqs)
    print(f"[✓] Cập nhật {len(concept_prereqs)} concepts với prereq -> {concepts_tsv.relative_to(repo_root)}")

if __name__ == "__main__":
    main()