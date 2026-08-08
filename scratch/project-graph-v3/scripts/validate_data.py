#!/usr/bin/env python3
"""
validate_data.py — Validator DỮ LIỆU chất lượng (chạy nhanh, không LLM).

Phát hiện lỗi dữ liệu agent sinh mà test_schema (cấu trúc) bỏ sót:
- Task thiếu mapping concept (→ UI hiện 'Concept t7')
- LO thiếu concept_code (mất traceability)
- Task không có keywords (STEP 1 sinh thiếu)
- Milestone/phase rỗng, task không có LO
- Prerequisite DAG cycle (Gagné)
- ZPD task nhảy cóc

Usage:
  python validate_data.py --project-graph output/project_graph_standardized.json \
      --roadmap output/roadmap.json
Exit code: 0 = PASS, 1 = có lỗi (in chi tiết).
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def check_tasks_mapping(pg: dict) -> list:
    """Task thiếu knowledge_mapping → LO mất concept (lỗi 'Concept t7')."""
    ms = pg.get("knowledge_mapping", {}).get("mappings", [])
    tasks = pg.get("implementation", {}).get("tasks", [])
    mapped_ids = {m["node_id"].split(":", 1)[1]
                  for m in ms if m.get("node_id", "").startswith("task:")}
    missing = [t["id"] for t in tasks if t["id"] not in mapped_ids]
    return [f"❌ Task thiếu mapping concept: {m}" for m in missing]


def check_task_keywords(pg: dict) -> list:
    """Task không có keywords — STEP 1 sinh thiếu (không có gì để map)."""
    tasks = pg.get("implementation", {}).get("tasks", [])
    return [f"❌ Task {t['id']} không có keywords: {t.get('action', '')[:40]}"
            for t in tasks if not t.get("keywords")]


def check_lo_concept(roadmap: dict) -> list:
    """LO thiếu concept_code → mất traceability (không biết dạy concept gì)."""
    issues = []
    n_lo = n_missing = 0
    for ph in roadmap.get("phases", []):
        for m in ph.get("milestones", []):
            for lo in m.get("los", []):
                n_lo += 1
                if not lo.get("concept_code"):
                    n_missing += 1
                    if n_missing <= 5:
                        issues.append(f"❌ LO thiếu concept_code: task {m['task']['id']} — "
                                      f"{lo.get('description', '')[:45]}")
    if n_missing > 5:
        issues.append(f"❌ ... và {n_missing - 5} LO nữa thiếu concept_code")
    if n_lo:
        pct = n_missing / n_lo * 100
        if pct > 5:
            issues.append(f"⚠️ {pct:.0f}% LO ({n_missing}/{n_lo}) thiếu concept_code (ngưỡng 5%)")
    return issues


def check_lo_assessment(roadmap: dict) -> list:
    """LO thiếu assessment — Biggs constructive alignment đổ vỡ."""
    n_lo = n_missing = 0
    for ph in roadmap.get("phases", []):
        for m in ph.get("milestones", []):
            for lo in m.get("los", []):
                n_lo += 1
                if not lo.get("assessment"):
                    n_missing += 1
    if n_lo and n_missing / n_lo > 0.05:
        return [f"❌ {n_missing}/{n_lo} LO thiếu assessment (Biggs — ngưỡng 5%)"]
    return []


def check_phases(roadmap: dict) -> list:
    """Phase rỗng / milestone không LO."""
    issues = []
    for ph in roadmap.get("phases", []):
        if not ph.get("milestones"):
            issues.append(f"❌ Phase {ph.get('phase')} RỖNG (không milestone)")
            continue
        for m in ph["milestones"]:
            if not m.get("los"):
                issues.append(f"❌ Milestone {m['task']['id']} không có LO (phase {ph.get('phase')})")
    return issues


def check_dag_cycle(pg: dict) -> list:
    """Gagné prerequisite DAG có cycle không (A requires B, B requires A)."""
    edges = pg.get("curriculum", {}).get("concept_prerequisites", [])
    adj = defaultdict(list)
    for e in edges:
        # requires có thể là string (implementation hiện tại) HOẶC list
        # (schema cũ trong curriculum-graph-design-B.md) — chuẩn hoá cả 2 để
        # tránh TypeError: unhashable type: 'list' khi DFS dùng làm dict key.
        reqs = e["requires"] if isinstance(e["requires"], list) else [e["requires"]]
        for r in reqs:
            adj[e["concept_code"]].append(r)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycle = []

    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                cycle.append(f"❌ DAG cycle: {u} ↔ {v}")
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for u in list(adj):
        if color[u] == WHITE:
            dfs(u)
    return cycle[:3]


def check_zpd(roadmap: dict) -> list:
    """ZPD task nhảy cóc (nhiều concept mới, không nối kiến thức cũ)."""
    cur = roadmap.get("curriculum", {})
    zpd = cur.get("zpd_checks", [])
    bad = [f"⚠️ ZPD: task {c['task_id']} — {c['verdict']} ({c['issues'][0][:45] if c.get('issues') else ''})"
           for c in zpd if c.get("verdict") != "OK"]
    return bad[:5]


def main():
    parser = argparse.ArgumentParser(description="validate_data.py — validator chất lượng dữ liệu agent")
    parser.add_argument("--project-graph", required=True, type=Path)
    parser.add_argument("--roadmap", type=Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    pg = json.load(open(args.project_graph, encoding="utf-8"))
    roadmap = json.load(open(args.roadmap, encoding="utf-8")) if args.roadmap else None

    all_issues = []
    all_issues += check_tasks_mapping(pg)
    all_issues += check_task_keywords(pg)
    if roadmap:
        all_issues += check_lo_concept(roadmap)
        all_issues += check_lo_assessment(roadmap)
        all_issues += check_phases(roadmap)
        all_issues += check_zpd(roadmap)
    all_issues += check_dag_cycle(pg)

    if all_issues:
        print(f"[FAIL] {len(all_issues)} vấn đề dữ liệu:")
        for issue in all_issues:
            print(f"  {issue}")
        return 1

    n_tasks = len(pg.get("implementation", {}).get("tasks", []))
    n_ms = len(pg.get("knowledge_mapping", {}).get("mappings", []))
    n_lo = (sum(len(m.get("los", [])) for ph in roadmap["phases"] for m in ph["milestones"])
            if roadmap else 0)
    print(f"[PASS] {n_tasks} tasks | {n_ms} mappings | {n_lo} LOs — dữ liệu sạch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
