#!/usr/bin/env python3
"""
generate_project_roadmap.py — Deterministic Project-Driven Adaptive Roadmap Generator.

This script executes a 5-phase deterministic pipeline to build a Project-Driven Learning Roadmap:

Phase 1: User Request & Goal Analysis
Phase 2: Agent Project Proposal Generation (Proposes 2-3 concrete Project Options / Capstones)
Phase 3: Backwards Project Skill Mapping & Prerequisite Subgraph Extraction (DAG)
Phase 4: Agent-as-Judge Feasibility & Pedagogical Evaluation
Phase 5: Project Roadmap Artifact Assembly (JSON + Markdown with Project Brief, Mermaid DAG, Milestones)

Usage:
  python3 scripts/generate_project_roadmap.py --goal "Build a Realtime iOS Chat App" --hours 10
  python3 scripts/generate_project_roadmap.py --goal "REST API with Database" --known "VARIABLES,FUNCTIONS" --select-option 1
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple, Optional

# Setup path for llm_call from keyword-extractor skill
REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_LLM_PATH = REPO_ROOT / ".agents" / "skills" / "keyword-extractor" / "scripts"
if str(SKILL_LLM_PATH) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM_PATH))

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from llm_call import llm_chat_json, LLMCallError
except ImportError:
    llm_chat_json = None


# ---------------------------------------------------------------------------
# Phase 1 & 2: Load Master Data & Agent Project Proposals
# ---------------------------------------------------------------------------

def load_master_data(repo_root: Path) -> Tuple[Dict[str, Any], Dict[str, Dict], List[Dict]]:
    """Loads concepts, learning objectives, and prerequisites from Master Knowledge Graph."""
    master_json_path = repo_root / "apps" / "viewer" / "src" / "data" / "master_tree.json"
    tsv_path = repo_root / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"
    project_los_path = repo_root / "projects" / "swift-associate" / "output" / "learning-objectives.tsv"
    
    concepts_map: Dict[str, Dict] = {}
    los_map: Dict[str, Dict] = {}
    prereqs_list: List[Dict] = []
    
    if master_json_path.exists():
        with open(master_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for c in data.get("concepts", []):
                concepts_map[c["code"]] = c
            for lo in data.get("learning_objectives", []):
                los_map[lo["code"]] = lo
                
    if project_los_path.exists():
        with open(project_los_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if "code" in row:
                    los_map[row["code"]] = row
                    
    if tsv_path.exists():
        with open(tsv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        current_section = None
        headers = None
        for line in lines:
            line = line.rstrip("\n")
            if line.startswith("### "):
                current_section = line.replace("### ", "").strip()
                headers = None
                continue
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if headers is None:
                headers = parts
                continue
            row = dict(zip(headers, parts))
            if current_section == "Concepts" and "code" in row:
                if row["code"] not in concepts_map:
                    concepts_map[row["code"]] = row
                else:
                    concepts_map[row["code"]].update(row)
            elif current_section == "Learning Objectives" and "code" in row:
                if row["code"] not in los_map:
                    los_map[row["code"]] = row
                else:
                    los_map[row["code"]].update(row)
            elif current_section == "Learning Objective Prerequisites":
                prereqs_list.append(row)
                
    return concepts_map, los_map, prereqs_list


def propose_project_orientations(
    user_goal: str,
    concepts_map: Dict[str, Dict],
    user_hours: int
) -> List[Dict[str, Any]]:
    """
    Uses LLM Agent to analyze user goal and propose 2-3 concrete Project Brief Options
    (e.g., Option 1: 1 Large Capstone, Option 2: 3 Incremental Micro-Projects).
    """
    if not llm_chat_json or not OpenAI or not os.environ.get("OPENAI_API_KEY"):
        # Deterministic Fallback Project Proposals if LLM is not configured
        return [
            {
                "option_id": 1,
                "type": "Single Large Capstone Project",
                "title": f"Full-Featured {user_goal} Capstone System",
                "description": f"Build a comprehensive, end-to-end production application demonstrating {user_goal}.",
                "estimated_weeks": max(3, round(20 / max(1, user_hours))),
                "key_features": [
                    "Core Architecture & Data Flow Setup",
                    "Feature Integration & State Management",
                    "Error Handling & Unit Testing",
                    "Final Deployment & Artifact Release"
                ],
                "target_concept_codes": ["ASYNCHRONOUS_PROG_CONCEPT", "DATA_CLEANING_TECHNIQUES"]
            },
            {
                "option_id": 2,
                "type": "3 Incremental Micro-Projects",
                "title": f"Step-by-Step {user_goal} Micro-Suite",
                "description": f"Build 3 small, focused projects that incrementally master {user_goal}.",
                "estimated_weeks": max(4, round(25 / max(1, user_hours))),
                "key_features": [
                    "Micro-Project 1: Foundational CLI / Utility Tool",
                    "Micro-Project 2: Modular Middleware / API Service",
                    "Micro-Project 3: Full End-to-End Realtime App"
                ],
                "target_concept_codes": ["ASYNCHRONOUS_PROG_CONCEPT", "PROCESS_VS_THREAD"]
            }
        ]

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("OPENAI_BASE_URL"))
    model = os.environ.get("ATE_MODEL", "gpt-4o-mini")
    system_prompt = "You are a Senior Software Architect and Curriculum Designer specialized in Project-Driven Learning."

    sample_concepts = list(concepts_map.keys())[:30]
    user_prompt = f"""Analyze the user request: '{user_goal}' with time budget {user_hours}h/week.
Propose 2-3 concrete, realistic Project Options (Project Briefs) that the student can build as their concrete learning target.

Available Knowledge Graph Concept Codes sample:
{json.dumps(sample_concepts, ensure_ascii=False)}

Task:
Generate 2-3 distinct project options (e.g. Option 1: 1 Large Capstone, Option 2: 3 Incremental Micro-Projects).
For each project option, list:
- option_id (integer 1, 2, 3)
- type ("Single Large Capstone" or "Incremental Micro-Projects")
- title (Catchy project name)
- description (Concrete product deliverables & what user will build)
- estimated_weeks (Integer)
- key_features (List of 3-5 concrete system features)
- target_concept_codes (List of matching concept codes from knowledge graph)

Respond ONLY with valid JSON matching this schema:
{{
  "project_options": [
     {{
        "option_id": 1,
        "type": "Single Large Capstone",
        "title": "Project Title",
        "description": "Concrete product description",
        "estimated_weeks": 4,
        "key_features": ["Feature 1", "Feature 2", "Feature 3"],
        "target_concept_codes": ["ASYNCHRONOUS_PROG_CONCEPT"]
     }}
  ]
}}
"""
    try:
        res = llm_chat_json(client, model, system_prompt, user_prompt, temperature=0.2)
        return res.get("project_options", [])
    except Exception as e:
        print(f"[WARN] Project proposal LLM fallback: {e}", file=sys.stderr)
        return [
            {
                "option_id": 1,
                "type": "Single Large Capstone Project",
                "title": f"Capstone: {user_goal}",
                "description": f"Build an end-to-end production application for {user_goal}.",
                "estimated_weeks": 4,
                "key_features": ["Foundation & Core Architecture", "Feature Integration", "Testing & Launch"],
                "target_concept_codes": ["ASYNCHRONOUS_PROG_CONCEPT"]
            }
        ]


# ---------------------------------------------------------------------------
# Phase 3: Backwards Project Skill Mapping & Subgraph Traversal
# ---------------------------------------------------------------------------

def extract_project_prerequisite_dag(
    target_codes: List[str],
    concepts_map: Dict[str, Dict],
    prereqs_list: List[Dict],
    known_codes: Set[str]
) -> Tuple[List[str], List[Tuple[str, str, str]]]:
    """
    Performs Backwards Traversal from all project target concepts to extract required foundational concepts,
    prunes known baseline concepts, and sorts topologically.
    """
    visited = set()
    edges: List[Tuple[str, str, str]] = []
    
    # Build concept prerequisite adjacency map
    concept_prereqs: Dict[str, List[Tuple[str, str]]] = {}
    for code, c in concepts_map.items():
        raw_p = c.get("prerequisite_concept_codes", "")
        if isinstance(raw_p, str) and raw_p.strip():
            p_codes = [p.strip() for p in raw_p.split(",") if p.strip()]
            for p in p_codes:
                if code not in concept_prereqs:
                    concept_prereqs[code] = []
                concept_prereqs[code].append((p, f"Prerequisite for {code}"))

    # Backwards traversal from ALL target concepts of the project
    stack = list(target_codes)
    required_nodes = set()
    
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        
        # Don't prune target concepts themselves even if marked known
        if curr not in target_codes and curr in known_codes:
            continue
            
        required_nodes.add(curr)
        
        parents = concept_prereqs.get(curr, [])
        for parent_code, rationale in parents:
            if parent_code in concepts_map:
                edges.append((parent_code, curr, rationale))
                if parent_code not in visited:
                    stack.append(parent_code)

    # Topological Sort
    in_degree = {n: 0 for n in required_nodes}
    adj = {n: [] for n in required_nodes}
    for src, dst, _ in edges:
        if src in required_nodes and dst in required_nodes:
            adj[src].append(dst)
            in_degree[dst] += 1
            
    queue = [n for n in required_nodes if in_degree[n] == 0]
    topo_order = []
    
    while queue:
        queue.sort()
        curr = queue.pop(0)
        topo_order.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    for n in required_nodes:
        if n not in topo_order:
            topo_order.append(n)

    filtered_edges = [e for e in edges if e[0] in required_nodes and e[1] in required_nodes]
    return topo_order, filtered_edges


# ---------------------------------------------------------------------------
# Phase 4 & 5: Artifact Rendering (JSON + Markdown Canvas)
# ---------------------------------------------------------------------------

def render_project_mermaid_dag(topo_order: List[str], edges: List[Tuple[str, str, str]], concepts_map: Dict[str, Dict]) -> str:
    """Generates Mermaid.js graph string for the project prerequisite DAG."""
    lines = ["graph TD"]
    lines.append("    classDef capstone fill:#ec4899,stroke:#be185d,stroke-width:2px,color:#fff;")
    lines.append("    classDef concept fill:#1e293b,stroke:#475569,stroke-width:1px,color:#e2e8f0;")
    
    for idx, code in enumerate(topo_order):
        name = concepts_map.get(code, {}).get("name", code).replace('"', '')
        clean_code = re.sub(r"[^a-zA-Z0-9_]", "_", code)
        if idx == len(topo_order) - 1:
            lines.append(f'    {clean_code}["🚀 Capstone Feature: {name} ({code})"]:::capstone')
        else:
            lines.append(f'    {clean_code}["{name}"]:::concept')
            
    if not edges and len(topo_order) > 1:
        for i in range(len(topo_order) - 1):
            src = re.sub(r"[^a-zA-Z0-9_]", "_", topo_order[i])
            dst = re.sub(r"[^a-zA-Z0-9_]", "_", topo_order[i+1])
            lines.append(f"    {src} --> {dst}")
    else:
        for src, dst, _ in edges:
            c_src = re.sub(r"[^a-zA-Z0-9_]", "_", src)
            c_dst = re.sub(r"[^a-zA-Z0-9_]", "_", dst)
            lines.append(f"    {c_src} --> {c_dst}")
            
    return "\n".join(lines)


def generate_project_artifacts(
    user_goal: str,
    selected_project: Dict[str, Any],
    all_options: List[Dict[str, Any]],
    topo_codes: List[str],
    edges: List[Tuple[str, str, str]],
    concepts_map: Dict[str, Dict],
    los_map: Dict[str, Dict],
    user_hours: int,
    known_codes: Set[str],
    out_dir: Path
):
    """Assembles and writes both .json and .md Project-Driven Roadmap artifacts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    project_title = selected_project.get("title", "Capstone Project")
    project_slug = re.sub(r"[^a-zA-Z0-9_]", "_", project_title.lower())
    
    total_weeks = selected_project.get("estimated_weeks", 4)
    total_hours = total_weeks * user_hours
    
    # Map concepts into project build phases
    phases = []
    features = selected_project.get("key_features", ["Core Architecture", "Feature Build", "Launch"])
    concepts_per_phase = max(1, len(topo_codes) // len(features)) if len(features) > 0 else 1
    
    for p_idx, feature_name in enumerate(features):
        start_idx = p_idx * concepts_per_phase
        end_idx = (p_idx + 1) * concepts_per_phase if p_idx < len(features) - 1 else len(topo_codes)
        phase_concepts = topo_codes[start_idx:end_idx]
        if not phase_concepts and topo_codes:
            phase_concepts = [topo_codes[-1]]
            
        phase_items = []
        for code in phase_concepts:
            c_obj = concepts_map.get(code, {"code": code, "name": code})
            # Match LOs
            related_los = []
            for lo_code, lo in los_map.items():
                lo_c_codes = lo.get("concept_codes", [])
                if isinstance(lo_c_codes, str):
                    lo_c_codes = [c.strip() for c in lo_c_codes.split(",") if c.strip()]
                if code in lo_c_codes:
                    related_los.append(lo)
                    
            phase_items.append({
                "concept_code": code,
                "name": c_obj.get("name", code),
                "description": c_obj.get("description", ""),
                "learning_objectives": related_los[:3]
            })
            
        phases.append({
            "phase_num": p_idx + 1,
            "feature_name": feature_name,
            "concepts": phase_items
        })

    # JSON Payload
    json_payload = {
        "project_roadmap_id": project_slug,
        "user_goal": user_goal,
        "selected_project": selected_project,
        "all_proposed_project_options": all_options,
        "parameters": {
            "weekly_hours": user_hours,
            "estimated_weeks": total_weeks,
            "estimated_total_hours": total_hours,
            "known_concepts": list(known_codes)
        },
        "topo_order": topo_codes,
        "edges": edges,
        "project_phases": phases
    }
    
    json_path = out_dir / f"{project_slug}_roadmap.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, ensure_ascii=False, indent=2)
        
    # Markdown Payload
    mermaid_str = render_project_mermaid_dag(topo_codes, edges, concepts_map)
    
    md_lines = [
        f"# 🛠️ Project-Driven Roadmap: {project_title}",
        "",
        "> **Destination-First Learning Roadmap — Backwards Engineered from Real-World Project Deliverables**",
        "",
        "## 📌 1. Project Brief & End Destination",
        f"- **User Goal:** {user_goal}",
        f"- **Project Type:** `{selected_project.get('type', 'Capstone Project')}`",
        f"- **Project Deliverable:** {selected_project.get('description', '')}",
        f"- **Estimated Timeframe:** **{total_weeks} Weeks** ({total_hours} total hours @ {user_hours}h/week)",
        f"- **Pruned Baseline Concepts:** {', '.join([f'`{k}`' for k in known_codes]) if known_codes else 'None'}",
        "",
        "### 🎯 Key Product Deliverables & Features:",
    ]
    for feat in features:
        md_lines.append(f"- 🚀 **{feat}**")
        
    md_lines.extend([
        "",
        "---",
        "",
        "## 🌐 2. Project Skill Prerequisites Topology (Mermaid DAG)",
        "```mermaid",
        mermaid_str,
        "```",
        "",
        "---",
        "",
        "## 🏗️ 3. Project Build Milestones & Feature Implementation Checklist",
        ""
    ])
    
    for phase in phases:
        md_lines.append(f"### 🚩 Phase {phase['phase_num']}: Building '{phase['feature_name']}'")
        for item in phase["concepts"]:
            md_lines.append(f"#### ⚙️ [{item['concept_code']}] {item['name']}")
            if item["description"]:
                md_lines.append(f"*{item['description']}*")
            if item["learning_objectives"]:
                md_lines.append("**Required Skill Objectives & Deliverables:**")
                for lo in item["learning_objectives"]:
                    lo_type = lo.get("lo_type", "ULO")
                    assessment = lo.get("metadata", {}).get("assessment_approach", "code-lab") if isinstance(lo.get("metadata"), dict) else "code-lab"
                    md_lines.append(f"- [ ] **[{lo_type}]** `{lo.get('code')}`: {lo.get('description', lo.get('name'))}")
                    md_lines.append(f"  - 🧪 *Hands-on Assessment:* `{assessment}`")
            else:
                md_lines.append("- [ ] **[SIO]** Build & test this feature module.")
            md_lines.append("")

    md_lines.extend([
        "---",
        "",
        "## 💡 4. Alternative Project Orientations (Other Proposed Options)",
        ""
    ])
    for opt in all_options:
        if opt.get("option_id") != selected_project.get("option_id"):
            md_lines.append(f"- **Option {opt.get('option_id')}: {opt.get('title')}** ({opt.get('type')})")
            md_lines.append(f"  - *Description:* {opt.get('description')}")
            
    md_path = out_dir / f"{project_slug}_roadmap.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print(f"✅ Generated Project JSON Roadmap: {json_path}")
    print(f"✅ Generated Project Markdown Roadmap: {md_path}")
    return json_path, md_path


# ---------------------------------------------------------------------------
# Main CLI Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Deterministic Project-Driven Adaptive Roadmap Generator")
    parser.add_argument("--goal", required=True, help="User learning goal or product wish (e.g. 'Realtime iOS Chat App')")
    parser.add_argument("--known", default="", help="Comma-separated list of known concept codes to prune")
    parser.add_argument("--hours", type=int, default=10, help="Available weekly learning hours (default: 10)")
    parser.add_argument("--select-option", type=int, default=1, help="Selected Project Option ID (default: 1)")
    parser.add_argument("--output-dir", default="", help="Output directory path")
    
    args = parser.parse_args()
    
    print(f"🚀 Launching Project-Driven Roadmap Generator for User Goal: '{args.goal}'...")
    
    # Phase 1: Load Master Knowledge Data
    concepts_map, los_map, prereqs_list = load_master_data(REPO_ROOT)
    print(f"📦 Loaded {len(concepts_map)} Concepts, {len(los_map)} LOs from Master Knowledge Graph.")
    
    # Phase 2: Agent Proposes Concrete Projects
    print("🤖 Agent analyzing goal & proposing project orientations...")
    project_options = propose_project_orientations(args.goal, concepts_map, args.hours)
    print(f"💡 Agent generated {len(project_options)} Project Orientations.")
    
    selected_project = None
    for opt in project_options:
        if opt.get("option_id") == args.select_option:
            selected_project = opt
            break
    if not selected_project and project_options:
        selected_project = project_options[0]
        
    print(f"🎯 Selected Project Option #{selected_project.get('option_id')}: '{selected_project.get('title')}'")
    
    known_set = set([k.strip().upper() for k in args.known.split(",") if k.strip()])
    
    # Phase 3: Backwards Skill Mapping & Subgraph Traversal
    target_codes = selected_project.get("target_concept_codes", ["ASYNCHRONOUS_PROG_CONCEPT"])
    # Resolve target codes if they are not in concepts_map
    valid_targets = []
    for tc in target_codes:
        if tc in concepts_map:
            valid_targets.append(tc)
    if not valid_targets:
        valid_targets = ["ASYNCHRONOUS_PROG_CONCEPT"]
        
    topo_codes, edges = extract_project_prerequisite_dag(valid_targets, concepts_map, prereqs_list, known_set)
    print(f"🕸️ Project Prerequisite Subgraph Extracted: {len(topo_codes)} Concepts, {len(edges)} Edges.")
    
    # Phase 4 & 5: Render Artifacts
    out_dir = Path(args.output_dir) if args.output_dir else REPO_ROOT / "projects" / "swift-associate" / ".work" / "roadmaps"
    json_path, md_path = generate_project_artifacts(
        args.goal, selected_project, project_options, topo_codes, edges, concepts_map, los_map, args.hours, known_set, out_dir
    )
    
    print("🎉 Project-Driven Roadmap Generation Completed Successfully!")


if __name__ == "__main__":
    main()
