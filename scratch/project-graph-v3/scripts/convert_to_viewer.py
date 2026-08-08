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
import sys
from pathlib import Path

PHASE_TITLES = {"FOUNDATION": "Foundation", "MVP": "MVP", "EXTEND": "Extend", "POLISH": "Polish"}


def convert(roadmap: dict) -> dict:
    phases_out = []
    concept_counter = 0
    lo_counter = 0
    all_concepts = set()

    for phase in roadmap.get("phases", []):
        phase_name = phase.get("phase", "MVP")
        phase_id = {"FOUNDATION": 0, "MVP": 1, "EXTEND": 2, "POLISH": 3}.get(phase_name, 1)

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
                concept = lo.get("concept_code") or (m.get("concepts") or [task_id])[0]
                all_concepts.add(concept)
                lo_type = lo.get("lo_type", "SPECIFIC_IMPL")
                prefix = {"UNIVERSAL": "ULO", "CONCEPTUAL_IMPL": "CIO", "SPECIFIC_IMPL": "SIO"}.get(
                    lo_type, "LO")
                los_out.append({
                    "code": f"{prefix}-{concept}-{lo_counter:02d}",
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
                "concept_code": milestone_concepts[0] if milestone_concepts else task_id,
                # M4 — line-level trace (file#L<line>) từ STEP 2 evidence, do
                # step4_roadmap.py đính vào milestone (nếu có).
                "evidence_refs": m.get("evidence_refs", []),
                "learning_objectives": los_out,
            })
            concept_counter += 1

        phases_out.append({
            "phase_id": phase_id,
            "title": PHASE_TITLES.get(phase_name, phase_name),
            "description": f"{phase_name}: {len(milestones_out)} tasks",
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
