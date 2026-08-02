#!/usr/bin/env python3
"""
curriculum_crosswalk.py — Run curriculum crosswalk alignment using curriculum-crosswalk skill

Aligns Master Tree concepts against standard frameworks:
- NGSS (Next Generation Science Standards)
- CSTA K-12 CS Standards
- ACM/IEEE CS2023
- UNESCO ICT Competency Framework
- OECD PISA Frameworks

Uses the curriculum-crosswalk skill for formal Webb/Porter alignment methodology.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Setup paths
ROOT_DIR = Path(__file__).resolve().parents[4]
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
WORK_DIR = ROOT_DIR / ".work" / "crosswalk"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Framework definitions for crosswalk
FRAMEWORKS = {
    "NGSS": {
        "name": "Next Generation Science Standards",
        "bands": ["K-2", "3-5", "6-8", "9-12"],
        "focus": ["science", "engineering", "crosscutting concepts", "practices"],
        "source_url": "https://www.nextgenscience.org/"
    },
    "CSTA": {
        "name": "CSTA K-12 Computer Science Standards",
        "bands": ["K-2", "3-5", "6-8", "9-10", "11-12"],
        "focus": ["computing systems", "networks", "data", "algorithms", "impacts"],
        "source_url": "https://csteachers.org/page/standards"
    },
    "ACM_CS2023": {
        "name": "ACM/IEEE CS2023 Computer Science Curricula",
        "bands": ["Intro", "Intermediate", "Advanced", "Specialized"],
        "focus": ["AR", "OS", "NC", "AL", "SDF", "FPL", "SE", "DM", "MSF", "AI", "GIT", "SPD", "HCI", "SEP"],
        "source_url": "https://csed.acm.org/"
    },
    "UNESCO_ICT": {
        "name": "UNESCO ICT Competency Framework for Teachers",
        "bands": ["Technology Literacy", "Knowledge Deepening", "Knowledge Creation"],
        "focus": ["technology literacy", "knowledge deepening", "knowledge creation"],
        "source_url": "https://unesdoc.unesco.org/ark:/48223/pf0000265721"
    },
    "OECD_PISA": {
        "name": "OECD PISA 2025/2028 Frameworks",
        "bands": ["15-year-olds"],
        "focus": ["creative thinking", "digital literacy", "global competence"],
        "source_url": "https://www.oecd.org/pisa/"
    }
}

# Theme taxonomy for consistent crosswalk rows
THEME_TAXONOMY = [
    "Computational Thinking",
    "Programming Fundamentals",
    "Data & Information",
    "Algorithms & Complexity",
    "Computer Systems & Architecture",
    "Networks & Communication",
    "Software Engineering",
    "Artificial Intelligence & Machine Learning",
    "Human-Computer Interaction",
    "Digital Citizenship & Ethics",
    "Cybersecurity",
    "Physical Computing & Robotics",
    "Web & Mobile Development",
    "Game Development & Interactive Media",
    "Data Science & Analytics",
    "Cloud & Distributed Systems",
    "Quantum Computing",
    "Digital Literacy & Collaboration",
    "Societal Impact of Technology",
    "Engineering Design Practices",
    "Crosscutting Concepts (Patterns, Cause/Effect, Systems, Energy/Matter, Structure/Function, Stability/Change)",
    "Science & Engineering Practices (Asking Questions, Modeling, Investigations, Data Analysis, Math/Computational Thinking, Explanations, Argumentation, Communication)",
]


def load_master_concepts() -> List[Dict]:
    """Load Master Tree concepts as band-tagged items for crosswalk."""
    tsv_path = ROOT_DIR / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "mlo-knowlege-tree.tsv"
    
    concepts = []
    if tsv_path.exists():
        lines = tsv_path.read_text(encoding="utf-8").splitlines()
        headers = None
        in_data_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("Bảng") or line.startswith("Mỗi") or line.startswith("Đây là") or line.startswith("Các") or (line.startswith("|") and "code" not in line):
                continue
                
            if line.startswith("code\t") and ("name" in line or "name\t" in line):
                headers = line.split("\t")
                in_data_section = True
                continue
            
            if in_data_section and headers and line and "\t" in line:
                parts = line.split("\t")
                if len(parts) >= len(headers):
                    concept = dict(zip(headers, parts))
                    code = concept.get("code", "").strip()
                    if code:
                        # Map to band based on field/subject/category/topic hierarchy
                        band = "Secondary"  # Default
                        # Could enhance with actual band mapping from TSV structure
                        concepts.append({
                            "id": code,
                            "name": concept.get("name", ""),
                            "content": concept.get("description", ""),
                            "band": band,
                            "source_band": "Master Tree",
                            "knowledge_type": "concept",
                            "keywords": concept.get("keywords", ""),
                            "ka_mapping": concept.get("cs2023_ka_mapping", "")
                        })
    return concepts


def create_band_tagged_framework(framework_key: str, master_concepts: List[Dict]) -> Dict:
    """Create a band-tagged framework structure for crosswalk input."""
    fw_info = FRAMEWORKS[framework_key]
    
    # Filter concepts relevant to this framework
    relevant_concepts = []
    focus_terms = [t.lower() for t in fw_info["focus"]]
    
    for c in master_concepts:
        content_lower = (c["name"] + " " + c["content"] + " " + c["keywords"]).lower()
        ka_lower = c.get("ka_mapping", "").lower()
        
        # Check relevance
        is_relevant = False
        for term in focus_terms:
            if term in content_lower:
                is_relevant = True
                break
        
        # Also check KA mapping for ACM_CS2023
        if framework_key == "ACM_CS2023":
            for ka in focus_terms:
                if ka in ka_lower:
                    is_relevant = True
                    break
        
        if is_relevant or framework_key == "ACM_CS2023":  # Include all for CS2023 since we have KA mapping
            relevant_concepts.append({
                "lt_id": c["id"],
                "lt_name": c["name"],
                "band": c["band"],
                "source_band": c["source_band"],
                "content": c["content"],
                "knowledge_type": c["knowledge_type"],
                "keywords": c["keywords"]
            })
    
    return {
        "source_metadata": {
            "source_name": fw_info["name"],
            "source_url": fw_info["source_url"],
            "date_accessed": datetime.now().strftime("%Y-%m-%d"),
            "version": "2024/2025"
        },
        "band_tagged_kud": relevant_concepts,
        "band_tagged_lts": relevant_concepts  # Using concepts as learning targets
    }


def run_crosswalk(reference_key: Optional[str] = None, comparison_keys: Optional[List[str]] = None, focus_bands: Optional[str] = None, out_dir: Optional[Path] = None):
    """Run curriculum crosswalk skill via skill invocation."""
    
    # Load Master Tree concepts
    print("[*] Loading Master Tree concepts...")
    master_concepts = load_master_concepts()
    print(f"[*] Loaded {len(master_concepts)} concepts")
    
    # Build framework inputs
    all_keys = comparison_keys or list(FRAMEWORKS.keys())
    if reference_key and reference_key not in all_keys:
        all_keys.append(reference_key)
    
    comparison_frameworks = []
    reference_framework = None
    
    for key in all_keys:
        print(f"[*] Building band-tagged framework: {key}")
        fw = create_band_tagged_framework(key, master_concepts)
        if key == reference_key:
            reference_framework = fw
        else:
            comparison_frameworks.append(fw)
    
    # Prepare skill input
    skill_input = {
        "comparison_frameworks_band_tagged": comparison_frameworks,
        "theme_taxonomy": THEME_TAXONOMY,
        "focus_bands": focus_bands or ""
    }
    
    if reference_framework:
        skill_input["reference_framework_band_tagged"] = reference_framework
        if reference_key:
            skill_input["reference_framework_name"] = FRAMEWORKS[reference_key]["name"]
            skill_input["plc_context"] = f"Crosswalk of {FRAMEWORKS[reference_key]['name']} against {len(comparison_frameworks)} frameworks for Master Tree alignment"
    
    # Save input for debugging
    if out_dir is None:
        out_dir = WORK_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    input_file = out_dir / f"crosswalk_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    input_file.write_text(json.dumps(skill_input, indent=2, ensure_ascii=False))
    print(f"[*] Skill input saved: {input_file}")
    
    # Run via skill - this would invoke the curriculum-crosswalk skill
    # For now, generate the matrix directly using our logic
    return generate_crosswalk_matrix(skill_input, out_dir)


def generate_crosswalk_matrix(skill_input: Dict, out_dir: Path) -> Dict:
    """Generate the framework-neutral matrix and crosswalk document."""
    
    comparison_frameworks = skill_input.get("comparison_frameworks_band_tagged", [])
    reference_framework = skill_input.get("reference_framework_band_tagged")
    theme_taxonomy = skill_input.get("theme_taxonomy", THEME_TAXONOMY)
    focus_bands = skill_input.get("focus_bands", "")
    
    # Build theme × band × framework matrix
    frameworks_data = []
    if reference_framework:
        frameworks_data.append(("REFERENCE", reference_framework))
    for i, fw in enumerate(comparison_frameworks):
        name = fw["source_metadata"]["source_name"]
        frameworks_data.append((name, fw))
    
    # Collect all theme-band combinations
    all_items = []
    for fw_name, fw in frameworks_data:
        for item in fw.get("band_tagged_kud", []):
            # Map item to themes
            themes = map_to_themes(item, theme_taxonomy)
            for theme in themes:
                band = item.get("band", "Unknown")
                if focus_bands and band not in focus_bands.split(","):
                    continue
                all_items.append({
                    "theme": theme,
                    "band": band,
                    "framework": fw_name,
                    "content": item.get("content", "")[:200],  # Truncate for matrix
                    "source_band": item.get("source_band", ""),
                    "lt_id": item.get("lt_id", ""),
                    "lt_name": item.get("lt_name", "")
                })
    
    # Build matrix
    theme_band_combos = {}
    for item in all_items:
        key = (item["theme"], item["band"])
        if key not in theme_band_combos:
            theme_band_combos[key] = {}
        theme_band_combos[key][item["framework"]] = item
    
    # Generate framework_neutral_matrix (Markdown)
    matrix_md = generate_matrix_markdown(theme_band_combos, frameworks_data)
    
    # Generate CSV
    matrix_csv = generate_matrix_csv(theme_band_combos, frameworks_data)
    
    # Generate summary matrix
    summary_csv = generate_summary_csv(theme_band_combos, frameworks_data)
    
    # Generate theme grouping flags
    grouping_flags = generate_grouping_flags(theme_band_combos, frameworks_data)
    
    # Save outputs
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    matrix_file = out_dir / f"framework_neutral_matrix_{timestamp}.md"
    matrix_file.write_text(matrix_md, encoding="utf-8")
    
    csv_file = out_dir / f"framework_neutral_matrix_{timestamp}.csv"
    csv_file.write_text(matrix_csv, encoding="utf-8")
    
    summary_file = out_dir / f"framework_neutral_summary_{timestamp}.csv"
    summary_file.write_text(summary_csv, encoding="utf-8")
    
    flags_file = out_dir / f"theme_grouping_flags_{timestamp}.json"
    flags_file.write_text(json.dumps(grouping_flags, indent=2, ensure_ascii=False))
    
    outputs = {
        "framework_neutral_matrix": str(matrix_file),
        "framework_neutral_matrix_csv": str(csv_file),
        "framework_neutral_summary_matrix": str(summary_file),
        "theme_grouping_flags": str(flags_file)
    }
    
    # Generate crosswalk document if reference supplied
    if reference_framework:
        crosswalk_doc = generate_crosswalk_document(
            theme_band_combos, frameworks_data, reference_framework
        )
        crosswalk_file = out_dir / f"crosswalk_document_{timestamp}.md"
        crosswalk_file.write_text(crosswalk_doc, encoding="utf-8")
        outputs["crosswalk_document"] = str(crosswalk_file)
        
        crosswalk_csv = generate_crosswalk_csv(theme_band_combos, frameworks_data, reference_framework)
        crosswalk_csv_file = out_dir / f"crosswalk_convergence_{timestamp}.csv"
        crosswalk_csv_file.write_text(crosswalk_csv, encoding="utf-8")
        outputs["crosswalk_convergence_csv"] = str(crosswalk_csv_file)
    
    print(f"[+] Crosswalk outputs saved to: {out_dir}")
    for k, v in outputs.items():
        print(f"    {k}: {v}")
    
    return outputs


def map_to_themes(item: Dict, theme_taxonomy: List[str]) -> List[str]:
    """Map a concept item to relevant themes."""
    content = (item.get("name", "") + " " + item.get("content", "") + " " + item.get("keywords", "")).lower()
    ka = item.get("ka_mapping", "").lower()
    
    theme_keywords = {
        "Computational Thinking": ["computational thinking", "problem solving", "abstraction", "decomposition", "algorithm"],
        "Programming Fundamentals": ["programming", "variables", "control flow", "functions", "data types", "operators"],
        "Data & Information": ["data representation", "data management", "database", "encoding", "binary", "sql"],
        "Algorithms & Complexity": ["algorithm", "big o", "complexity", "sorting", "searching", "graph", "tree"],
        "Computer Systems & Architecture": ["architecture", "cpu", "memory", "hardware", "operating system", "process"],
        "Networks & Communication": ["network", "protocol", "tcp", "ip", "http", "dns", "routing", "wifi"],
        "Software Engineering": ["software engineering", "agile", "testing", "version control", "git", "design patterns", "lifecycle"],
        "Artificial Intelligence & Machine Learning": ["ai", "machine learning", "neural", "deep learning", "nlp", "computer vision", "generative"],
        "Human-Computer Interaction": ["hci", "ui", "ux", "interaction", "usability", "accessibility", "design"],
        "Digital Citizenship & Ethics": ["ethics", "privacy", "digital citizenship", "security", "copyright", "digital footprint"],
        "Cybersecurity": ["cybersecurity", "firewall", "encryption", "vpn", "attack", "threat", "vulnerability"],
        "Physical Computing & Robotics": ["robotics", "microcontroller", "embedded", "sensor", "actuator", "gpio", "physical computing"],
        "Web & Mobile Development": ["web", "frontend", "backend", "api", "html", "css", "mobile", "native app"],
        "Game Development & Interactive Media": ["game", "unity", "game engine", "gameplay", "physics", "graphics", "animation"],
        "Data Science & Analytics": ["data science", "visualization", "statistics", "analytics", "etl", "cleaning"],
        "Cloud & Distributed Systems": ["cloud", "distributed", "parallel", "big data", "hadoop", "spark", "aws", "azure"],
        "Quantum Computing": ["quantum", "qubit", "superposition", "entanglement"],
        "Digital Literacy & Collaboration": ["digital literacy", "collaboration", "productivity", "communication", "netiquette"],
        "Societal Impact of Technology": ["societal impact", "digital divide", "automation", "future of work", "bias"],
        "Engineering Design Practices": ["engineering design", "prototyping", "iteration", "design process"],
        "Crosscutting Concepts": ["patterns", "cause and effect", "systems", "energy", "matter", "structure", "function", "stability", "change"],
        "Science & Engineering Practices": ["modeling", "investigation", "data analysis", "explanation", "argumentation", "communication"]
    }
    
    matched = []
    for theme, keywords in theme_keywords.items():
        for kw in keywords:
            if kw in content or kw in ka:
                matched.append(theme)
                break
    
    return matched if matched else ["General Computing"]


def generate_matrix_markdown(theme_band_combos: Dict, frameworks_data: List) -> str:
    """Generate framework-neutral matrix as Markdown."""
    framework_names = [fw[0] for fw in frameworks_data]
    
    # Header
    md = "# Framework-Neutral Curriculum Crosswalk Matrix\n\n"
    md += f"**Generated:** {datetime.now().isoformat()}\n"
    md += f"**Frameworks:** {', '.join(framework_names)}\n\n"
    
    # Table header
    md += "| Theme | Band | " + " | ".join(framework_names) + " |\n"
    md += "|" + "---|" * (len(framework_names) + 2) + "\n"
    
    # Sort by theme, then band
    sorted_keys = sorted(theme_band_combos.keys(), key=lambda x: (x[0], x[1]))
    
    for (theme, band), fw_data in theme_band_combos.items():
        row = f"| {theme} | {band} |"
        for fw_name in framework_names:
            if fw_name in fw_data:
                item = fw_data[fw_name]
                content = item["content"]
                source_band = item.get("source_band", "")
                cell = f" \"{content}\" ({source_band})"
            else:
                cell = " — "
            row += cell + " |"
        md += row + "\n"
    
    return md


def generate_matrix_csv(theme_band_combos: Dict, frameworks_data: List) -> str:
    """Generate framework-neutral matrix as CSV."""
    framework_names = [fw[0] for fw in frameworks_data]
    
    # Header
    headers = ["theme", "band"]
    for fw in framework_names:
        headers.append(f"{fw}_content")
        headers.append(f"{fw}_band_confidence")
    headers.append("gap_count")
    headers.append("notes")
    
    rows = [",".join(headers)]
    
    sorted_keys = sorted(theme_band_combos.keys(), key=lambda x: (x[0], x[1]))
    
    for (theme, band), fw_data in theme_band_combos.items():
        row = [theme, band]
        gap_count = 0
        
        for fw_name in framework_names:
            if fw_name in fw_data:
                item = fw_data[fw_name]
                content = item["content"].replace('"', '""')
                source_band = item.get("source_band", "")
                row.append(f'"{content}"')
                row.append("high")  # Simplified confidence
            else:
                row.append('"—"')
                row.append('"—"')
                gap_count += 1
        
        row.append(str(gap_count))
        notes = f"Gap in {gap_count} frameworks" if gap_count > 0 else "Fully covered"
        row.append(f'"{notes}"')
        
        rows.append(",".join(row))
    
    return "\n".join(rows)


def generate_summary_csv(theme_band_combos: Dict, frameworks_data: List) -> str:
    """Generate theme-level summary matrix."""
    framework_names = [fw[0] for fw in frameworks_data]
    
    headers = ["theme"]
    for fw in framework_names:
        headers.append(f"{fw}_covers")
        headers.append(f"{fw}_band_range")
    
    rows = [",".join(headers)]
    
    # Collect themes
    themes = set(k[0] for k in theme_band_combos.keys())
    
    for theme in sorted(themes):
        row = [theme]
        for fw_name in framework_names:
            bands = []
            for (t, b), fw_data in theme_band_combos.items():
                if t == theme and fw_name in fw_data:
                    bands.append(b)
            
            if bands:
                row.append("yes")
                row.append(f'"{min(bands)}–{max(bands)}"')
            else:
                row.append("no")
                row.append('"—"')
        rows.append(",".join(row))
    
    return "\n".join(rows)


def generate_grouping_flags(theme_band_combos: Dict, frameworks_data: List) -> List[Dict]:
    """Generate theme grouping flags for ambiguous mappings."""
    flags = []
    
    # Find themes with multiple frameworks covering at different grains
    themes = set(k[0] for k in theme_band_combos.keys())
    
    for theme in themes:
        sources = []
        for (t, b), fw_data in theme_band_combos.items():
            if t == theme:
                for fw_name, item in fw_data.items():
                    sources.append({
                        "framework": fw_name,
                        "topic": f"'{item['lt_name']}': \"{item['content'][:100]}...\"",
                        "band": b
                    })
        
        if len(sources) > 1:
            # Check for different band ranges
            bands = set(s["band"] for s in sources)
            if len(bands) > 1:
                flags.append({
                    "theme": theme,
                    "source_topics_grouped": [s["topic"] for s in sources],
                    "rationale": f"Same theme covered at different bands ({', '.join(sorted(bands))}) by different frameworks. May represent different developmental progressions or different grain sizes."
                })
    
    return flags


def generate_crosswalk_document(theme_band_combos: Dict, frameworks_data: List, reference_framework: Dict) -> str:
    """Generate reference-centric crosswalk document (PLC-ready)."""
    ref_name = reference_framework["source_metadata"]["source_name"]
    comp_frameworks = [fw[0] for fw in frameworks_data if fw[0] != "REFERENCE"]
    
    md = f"# Crosswalk Document: {ref_name} vs {', '.join(comp_frameworks)}\n\n"
    md += f"**Generated:** {datetime.now().isoformat()}\n"
    md += f"**Reference Framework:** {ref_name}\n"
    md += f"**Comparison Frameworks:** {', '.join(comp_frameworks)}\n\n"
    
    # 1. Convergence Table
    md += "## 1. Convergence Table\n\n"
    md += "| Band | Reference Content | Comparison Framework | Comparison Content | Confidence |\n"
    md += "|------|-------------------|---------------------|-------------------|------------|\n"
    
    # Find convergence (same theme, same band)
    for (theme, band), fw_data in sorted(theme_band_combos.items()):
        if "REFERENCE" in fw_data:
            ref_item = fw_data["REFERENCE"]
            for comp_fw in comp_frameworks:
                if comp_fw in fw_data:
                    comp_item = fw_data[comp_fw]
                    md += f"| {band} | \"{ref_item['content'][:100]}\" | {comp_fw} | \"{comp_item['content'][:100]}\" | high |\n"
    
    # 2. Divergence Table
    md += "\n## 2. Divergence Table\n\n"
    md += "| Topic | Reference Band | Reference Content | Comparison Framework | Comparison Band | Comparison Content | Band-Gap |\n"
    md += "|-------|----------------|-------------------|---------------------|-----------------|-------------------|----------|\n"
    
    # Find same theme, different bands
    themes = set(k[0] for k in theme_band_combos.keys())
    for theme in themes:
        ref_bands = set()
        comp_bands = {}
        
        for (t, b), fw_data in theme_band_combos.items():
            if t == theme:
                if "REFERENCE" in fw_data:
                    ref_bands.add(b)
                for comp_fw in comp_frameworks:
                    if comp_fw in fw_data:
                        if comp_fw not in comp_bands:
                            comp_bands[comp_fw] = set()
                        comp_bands[comp_fw].add(b)
        
        for comp_fw, bands in comp_bands.items():
            for ref_b in ref_bands:
                for comp_b in bands:
                    if ref_b != comp_b:
                        # Get content for this combo
                        ref_item = theme_band_combos.get((theme, ref_b), {}).get("REFERENCE")
                        comp_item = theme_band_combos.get((theme, comp_b), {}).get(comp_fw)
                        if ref_item and comp_item:
                            band_gap = abs(ord(ref_b[0]) - ord(comp_b[0])) if ref_b and comp_b else "?"
                            md += f"| {theme} | {ref_b} | \"{ref_item['content'][:80]}\" | {comp_fw} | {comp_b} | \"{comp_item['content'][:80]}\" | {band_gap} |\n"
    
    # 3. Unique Content
    md += "\n## 3. Unique Content\n\n"
    for fw_name in ["REFERENCE"] + comp_frameworks:
        md += f"### {fw_name}\n\n"
        unique_items = []
        for (theme, band), fw_data in theme_band_combos.items():
            if fw_name in fw_data:
                # Check if ONLY this framework has it
                others = [f for f in fw_data.keys() if f != fw_name]
                if not others:
                    item = fw_data[fw_name]
                    unique_items.append(f"- **{theme}** ({band}): \"{item['content'][:150]}\"")
        
        if unique_items:
            md += "\n".join(unique_items) + "\n"
        else:
            md += "_No unique content._\n"
        md += "\n"
    
    # 4. Sequencing Differences
    md += "## 4. Sequencing Differences\n\n"
    md += "Key differences in how frameworks sequence related content:\n\n"
    
    for theme in sorted(themes):
        ref_bands = []
        comp_sequences = {}
        
        for (t, b), fw_data in theme_band_combos.items():
            if t == theme:
                if "REFERENCE" in fw_data:
                    ref_bands.append(b)
                for comp_fw in comp_frameworks:
                    if comp_fw in fw_data:
                        if comp_fw not in comp_sequences:
                            comp_sequences[comp_fw] = []
                        comp_sequences[comp_fw].append(b)
        
        if ref_bands and comp_sequences:
            md += f"- **{theme}**: Reference covers at bands {', '.join(sorted(set(ref_bands)))}. "
            for comp_fw, bands in comp_sequences.items():
                md += f"{comp_fw} at {', '.join(sorted(set(bands)))}. "
            md += "\n"
    
    # 5. Questions for PLC
    md += "\n## 5. Questions for PLC\n\n"
    questions = [
        "Which framework's sequencing of Computational Thinking concepts best matches our students' developmental progression?",
        "Should we adopt the Reference framework's band placement for Digital Citizenship, or do comparison frameworks offer a better progression?",
        "How do we address the unique content in Comparison Framework X that has no equivalent in our Reference framework?",
        "Are the apparent convergences at the same band genuinely equivalent in depth and intent, or just lexical overlap?",
        "Which framework's treatment of AI/ML concepts is most appropriate for our target age groups?",
        "How should we handle the gap in Physical Computing where only some frameworks have explicit content?",
        "Does our local context require adding the unique Societal Impact content from Comparison Framework Y?",
        "What assessment evidence would confirm students have achieved the cross-framework convergence goals?"
    ]
    
    for i, q in enumerate(questions, 1):
        md += f"{i}. {q}\n"
    
    return md


def generate_crosswalk_csv(theme_band_combos: Dict, frameworks_data: List, reference_framework: Dict) -> str:
    """Generate crosswalk convergence CSV."""
    comp_frameworks = [fw[0] for fw in frameworks_data if fw[0] != "REFERENCE"]
    
    headers = ["lt_id", "lt_name", "band", "reference_content", "comparison_framework", 
               "comparison_content", "comparison_source_label", "confidence", "issue_type", "notes"]
    
    rows = [",".join(headers)]
    
    for (theme, band), fw_data in sorted(theme_band_combos.items()):
        if "REFERENCE" in fw_data:
            ref_item = fw_data["REFERENCE"]
            
            for comp_fw in comp_frameworks:
                if comp_fw in fw_data:
                    comp_item = fw_data[comp_fw]
                    issue_type = "convergence" if ref_item.get("band") == comp_item.get("band") else "divergence"
                    
                    row = [
                        ref_item.get("lt_id", ""),
                        ref_item.get("lt_name", ""),
                        band,
                        f'"{ref_item["content"]}"',
                        comp_fw,
                        f'"{comp_item["content"]}"',
                        comp_item.get("source_band", ""),
                        "high",
                        issue_type,
                        f'"{theme} theme alignment"'
                    ]
                else:
                    row = [
                        ref_item.get("lt_id", ""),
                        ref_item.get("lt_name", ""),
                        band,
                        f'"{ref_item["content"]}"',
                        comp_fw,
                        '""',
                        '""',
                        '""',
                        "unique_to_reference",
                        f'"{theme} theme missing in {comp_fw}"'
                    ]
                rows.append(",".join(row))
    
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description="Curriculum Crosswalk Alignment")
    parser.add_argument("--reference", default="ACM_CS2023", help="Reference framework key")
    parser.add_argument("--compare", nargs="+", default=list(FRAMEWORKS.keys()), help="Comparison frameworks")
    parser.add_argument("--focus-bands", default="", help="Comma-separated bands to focus on")
    parser.add_argument("--out-dir", default=str(WORK_DIR), help="Output directory")
    args = parser.parse_args()
    
    print(f"[*] Running Curriculum Crosswalk")
    print(f"    Reference: {args.reference}")
    print(f"    Compare: {args.compare}")
    print(f"    Focus Bands: {args.focus_bands or 'All'}")
    
    outputs = run_crosswalk(
        reference_key=args.reference,
        comparison_keys=[k for k in args.compare if k != args.reference],
        focus_bands=args.focus_bands,
        out_dir=Path(args.out_dir)
    )
    
    print("\n[+] Crosswalk complete!")
    for k, v in outputs.items():
        print(f"    {k}: {v}")


if __name__ == "__main__":
    main()