#!/usr/bin/env python3
"""
Convert STEP 4 roadmap (task-aware) → format viewer (jit-bulb-v3.json):
  roadmap.json → {project_brief, phases:[{phase_id,title,description,milestones}],
                  total_milestones, total_concepts}
  milestone: {id, name, concept_code, learning_objectives:[{code,lo_type,description,
              bloom_level,keyword,platform,...}]}

Usage:
  python convert_to_viewer.py \
      --roadmap output/roadmap.json \
      --output /path/to/roadmaps/stream-chat-demoapp.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Phase = development_stage (audit 2026-08-08: step4 không còn nén 6 stages → 4
# phases). phase_id = stage index (0-based); POLISH (gaps/debts) = phase 6+.
POLISH_PHASE_ID = 6


def _phase_id(phase_name: str) -> int:
    m = re.match(r"Stage\s+(\d+)", phase_name or "")
    if m:
        return int(m.group(1)) - 1
    return POLISH_PHASE_ID


def _phase_title(phase_name: str) -> str:
    m = re.match(r"Stage\s+\d+\s*[-—]\s*(.+)", phase_name or "")
    if m:
        return m.group(1).strip()
    return "Polish" if phase_name == "POLISH" else (phase_name or "Phase")


def convert(roadmap: dict) -> dict:
    phases_out = []
    concept_counter = 0
    lo_counter = 0
    all_concepts = set()

    # Stage narrative → description cho phase (product_state của stage đó)
    stage_desc = {}
    for s in roadmap.get("development_stages", []):
        stage_desc[s.get("stage", "")] = s.get("product_state", "")

    for phase in roadmap.get("phases", []):
        phase_name = phase.get("phase", "POLISH")
        phase_id = _phase_id(phase_name)

        milestones_out = []
        for m in phase.get("milestones", []):
            task = m.get("task", {})
            task_id = task.get("id", "T")
            # KHÔNG truncate action — renderer tự wrap dòng (trước cắt 60 ký tự
            # làm mất chữ: 'mật khẩu' → 'mật k')
            task_name = task.get("action", task_id)

            los_out = []
            for lo in m.get("los", []):
                lo_counter += 1
                # Scaffold (audit C.1 + v2 #6): milestone không concept → KHÔNG
                # fallback task_id làm concept (trước đây viewer hiện 'Concept T01'
                # — task ID trá hình concept). concept = "" (renderer tự fallback).
                concept = lo.get("concept_code") or (m.get("concepts") or [""])[0]
                all_concepts.add(concept) if concept else None
                lo_type = lo.get("lo_type", "SPECIFIC_IMPL")
                prefix = {"UNIVERSAL": "ULO", "CONCEPTUAL_IMPL": "CIO", "SPECIFIC_IMPL": "SIO"}.get(
                    lo_type, "LO")
                los_out.append({
                    "code": f"{prefix}-{concept}-{lo_counter:02d}" if concept
                            else f"{prefix}-{lo_counter:02d}",
                    "lo_type": lo_type,
                    "concept": concept,
                    "name": f"{prefix}: {task_name}",
                    "description": lo.get("description", ""),
                    # Biggs constructive alignment — assessment thật từ roadmap
                    "assessment": lo.get("assessment")
                        or ("code-review" if lo_type == "SPECIFIC_IMPL" else "concept-check"),
                    "bloom_level": (lo.get("bloom_level") or "understand").lower(),
                    "knowledge_dimension": "PROCEDURAL",
                    "keyword": lo.get("keyword", ""),
                    "platform": lo.get("platform", "app"),
                    "task_id": lo.get("task_id", task_id),
                })

            # Milestone dùng concepts THẬT của task (KHÔNG phải task_id — task
            # không phải concept). Renderer dùng field này làm nhãn concept.
            # LƯU Ý: los_out dùng key "concept" (đã transform), KHÔNG phải
            # "concept_code" (key của LO thô trong roadmap) — fallback đọc đúng key.
            milestone_concepts = m.get("concepts") or list({
                lo.get("concept") for lo in los_out if lo.get("concept")
            })
            milestones_out.append({
                "id": task_id,
                "name": task_name,
                "concepts": milestone_concepts,
                # Scaffold: concept_code = "" (không có concept thật — renderer
                # fallback milestone.name thay vì task ID trá hình concept).
                "concept_code": milestone_concepts[0] if milestone_concepts
                                else ("" if m.get("scaffold") else task_id),
                # M4 — line-level trace (file#L<line>) từ STEP 2 evidence, do
                # step4_roadmap.py đính vào milestone (nếu có).
                "evidence_refs": m.get("evidence_refs", []),
                "learning_objectives": los_out,
            })
            concept_counter += 1

        phases_out.append({
            "phase_id": phase_id,
            "title": _phase_title(phase_name),
            "description": stage_desc.get(phase_name)
                or f"{phase_name}: {len(milestones_out)} tasks",
            "milestones": milestones_out,
        })

    project = roadmap.get("project", {})
    return {
        "project_brief": {
            # M1 — không hardcode template project cũ (StreamChat). Code/tiêu đề
            # đều lấy từ roadmap; fallback trung tính, không nhắc SDK/repo.
            "project_code": (project.get("name") or "PROJECT").upper().replace(" ", "_"),
            "title": project.get("name", "Learn-by-building project"),
            "goal": project.get("purpose", ""),
            "tech_stack": project.get("tech_stack", {}),
        },
        "development_stages": roadmap.get("development_stages", []),
        "phases": phases_out,
        "total_milestones": concept_counter,
        "total_concepts": len(all_concepts),
        "lo_count": lo_counter,
    }


def main():
    parser = argparse.ArgumentParser(description="Convert STEP 4 roadmap → viewer format")
    parser.add_argument("--roadmap", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    roadmap = json.load(open(args.roadmap, encoding="utf-8"))
    result = convert(roadmap)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[✓] Converted → {args.output}")
    print(f"    {result['total_milestones']} milestones | {result['total_concepts']} concepts | {result['lo_count']} LOs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
