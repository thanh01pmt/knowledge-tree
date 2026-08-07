#!/usr/bin/env python3
"""
roadmap_discovery.py — STEP 0 of Unified Roadmap Generation Pipeline

Scans Master Tree (from Supabase) and existing projects to build a reuse inventory.
This is the first step before generating a roadmap.

Usage:
    python scripts/roadmap_discovery.py --goal "Build iOS app with SwiftUI" --tech-stack "Swift,SwiftUI,Combine"
    python scripts/roadmap_discovery.py --goal "Build web app" --tech-stack "TypeScript,React,Node" --output reuse_inventory.json
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Suppress urllib3 warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

# Supabase client
try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


def find_repo_root() -> Path:
    """Find repository root by looking for .agents directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".agents").is_dir():
            return current
        current = current.parent
    raise RuntimeError("Could not find repository root")


def load_env(repo_root: Path):
    """Load environment variables from .env file."""
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("\"'")


def load_from_supabase(supabase) -> Dict:
    """
    Load Master Tree data from Supabase.
    
    Returns:
        Dict with concepts, ulos, cios, sios, prerequisites
    """
    # Query concepts
    concepts_response = supabase.table("concepts").select("*").execute()
    concepts = {c["code"]: c for c in concepts_response.data} if concepts_response.data else {}
    
    # Query learning objectives
    los_response = supabase.table("learning_objectives").select("*").execute()
    los = los_response.data if los_response.data else []
    
    # Categorize LOs by type
    ulos = [lo for lo in los if lo.get("lo_type") == "UNIVERSAL"]
    cios = [lo for lo in los if lo.get("lo_type") == "CONCEPTUAL_IMPL"]
    sios = [lo for lo in los if lo.get("lo_type") == "SPECIFIC_IMPL"]
    
    # Query prerequisites
    prereqs_response = supabase.table("learning_objective_prerequisites").select("*").execute()
    prereqs = prereqs_response.data if prereqs_response.data else []
    
    return {
        "concepts": concepts,
        "ulos": ulos,
        "cios": cios,
        "sios": sios,
        "prerequisites": prereqs,
    }


def load_project_context(project_dir: Path) -> Tuple[Dict[str, Dict], List[Dict]]:
    """
    Load concepts and learning objectives from a project's output TSV files.
    
    Returns:
        concepts: Dict mapping concept code -> concept data
        learning_objectives: List of LO data
    """
    concepts = {}
    los = []
    
    # Load concepts
    concepts_file = project_dir / "output" / "concepts.tsv"
    if concepts_file.exists():
        with open(concepts_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                code = row.get("code", "")
                if code:
                    concepts[code] = row
    
    # Load learning objectives
    lo_file = project_dir / "output" / "learning-objectives.tsv"
    if lo_file.exists():
        with open(lo_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                los.append(row)
    
    return concepts, los


def scan_projects(projects_dir: Path) -> Dict[str, Dict]:
    """
    Scan all projects and extract their SIOs, tech stack, and concept codes.
    
    Returns:
        Dict mapping project slug -> project data
    """
    projects = {}
    
    if not projects_dir.exists():
        return projects
    
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        
        # Skip hidden directories
        if project_dir.name.startswith("."):
            continue
        
        concepts, los = load_project_context(project_dir)
        
        if not los:
            continue
        
        # Extract SIOs
        sios = [lo for lo in los if lo.get("lo_type") == "SPECIFIC_IMPL"]
        
        # Extract tech stack from SIO codes (format: SIO-TECH-CONCEPT-NUM)
        # Blacklist common non-tech terms that appear in SIO codes
        tech_blacklist = {
            'UN', 'CONCEPT', 'DEBUG', 'LTASW', 'CORE', 'BASIC', 'ADVANCED',
            'TEST', 'DOC', 'UTIL', 'HELPER', 'COMMON', 'BASE', 'MAIN'
        }
        
        tech_stack = set()
        for sio in sios:
            code = sio.get("code", "")
            parts = code.split("-")
            if len(parts) >= 3 and parts[0] == "SIO":
                tech = parts[1].upper()
                # Filter out blacklisted terms and very short terms
                if tech not in tech_blacklist and len(tech) > 2:
                    tech_stack.add(tech)
        
        # Extract concept codes
        concept_codes = set()
        for lo in los:
            codes = lo.get("concept_codes", "")
            if codes:
                for code in codes.split(","):
                    concept_codes.add(code.strip())
        
        # Extract keywords from LO names
        keywords = set()
        for lo in los:
            name = lo.get("name", "").lower()
            # Simple tokenization
            for word in name.replace("-", " ").replace("_", " ").split():
                if len(word) > 3:
                    keywords.add(word)
        
        projects[project_dir.name] = {
            "slug": project_dir.name,
            "path": str(project_dir),
            "concepts": concepts,
            "sios": sios,
            "tech_stack": list(tech_stack),
            "concept_codes": list(concept_codes),
            "keywords": list(keywords),
        }
    
    return projects


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def overlap_ratio(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute overlap ratio: |intersection| / |set_a|."""
    if not set_a:
        return 0.0
    intersection = set_a & set_b
    return len(intersection) / len(set_a)


def score_project_similarity(
    target_tech: Set[str],
    target_keywords: Set[str],
    target_concepts: Set[str],
    project_data: Dict
) -> float:
    """
    Score similarity between target and existing project.
    
    Weights:
        - Tech stack: 0.5 (Jaccard)
        - Keywords: 0.3 (overlap ratio)
        - Concept codes: 0.2 (overlap ratio)
    """
    proj_tech = set(project_data.get("tech_stack", []))
    proj_keywords = set(project_data.get("keywords", []))
    proj_concepts = set(project_data.get("concept_codes", []))
    
    tech_score = jaccard_similarity(target_tech, proj_tech)
    keyword_score = overlap_ratio(target_keywords, proj_keywords)
    concept_score = overlap_ratio(target_concepts, proj_concepts)
    
    return 0.5 * tech_score + 0.3 * keyword_score + 0.2 * concept_score


def build_reuse_inventory(
    goal: str,
    tech_stack: List[str],
    master_tree: Dict,
    projects: Dict[str, Dict]
) -> Dict:
    """
    Build reuse inventory by scoring projects against target.
    
    Returns:
        Inventory dict with master tree, scored projects, and reuse summary.
    """
    target_tech = set(tech_stack)
    
    # Extract keywords and concepts from goal (simple tokenization)
    target_keywords = set()
    for word in goal.lower().replace("-", " ").replace("_", " ").split():
        if len(word) > 3:
            target_keywords.add(word)
    
    target_concepts = set()  # Will be populated in later steps
    
    # Score all projects
    scored_projects = []
    for slug, data in projects.items():
        score = score_project_similarity(
            target_tech, target_keywords, target_concepts, data
        )
        if score > 0.0:  # Only include projects with some similarity
            reuse_level = "high" if score >= 0.7 else ("partial" if score >= 0.4 else "low")
            scored_projects.append({
                "slug": slug,
                "score": round(score, 3),
                "reuse_level": reuse_level,
                "tech_stack": data["tech_stack"],
                "sio_count": len(data["sios"]),
                "concept_count": len(data["concept_codes"]),
            })
    
    # Sort by score descending
    scored_projects.sort(key=lambda x: x["score"], reverse=True)
    
    # Extract master tree summary
    master_concepts = master_tree.get("concepts", {})
    master_ulos = master_tree.get("ulos", [])
    master_cios = master_tree.get("cios", [])
    master_sios = master_tree.get("sios", [])
    master_prereqs = master_tree.get("prerequisites", [])
    
    return {
        "goal": goal,
        "tech_stack": tech_stack,
        "timestamp": datetime.now(UTC).isoformat(),
        "master_tree": {
            "concept_count": len(master_concepts),
            "ulo_count": len(master_ulos),
            "cio_count": len(master_cios),
            "sio_count": len(master_sios),
            "prereq_count": len(master_prereqs),
            "concepts": master_concepts,
            "ulos": master_ulos,
            "cios": master_cios,
            "sios": master_sios,
            "prerequisites": master_prereqs,
        },
        "scored_projects": scored_projects,
        "reuse_summary": {
            "tier1_master_available": len(master_concepts) > 0,
            "tier2_high_reuse": len([p for p in scored_projects if p["reuse_level"] == "high"]),
            "tier2_partial_reuse": len([p for p in scored_projects if p["reuse_level"] == "partial"]),
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="STEP 0: Build reuse inventory from Master Tree (Supabase) and existing projects"
    )
    parser.add_argument("--goal", required=True, help="Learning goal description")
    parser.add_argument("--tech-stack", required=True, help="Comma-separated tech stack")
    parser.add_argument("--output", help="Output JSON file path (optional)")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    parser.add_argument("--fallback-tsv", action="store_true", help="Use TSV files instead of Supabase")
    
    args = parser.parse_args()
    
    repo_root = find_repo_root()
    projects_dir = repo_root / "projects"
    
    if not args.quiet:
        print(f"[STEP 0] Scanning projects in {projects_dir}...", file=sys.stderr)
    
    # Scan existing projects
    projects = scan_projects(projects_dir)
    
    if not args.quiet:
        print(f"[STEP 0] Found {len(projects)} projects with learning objectives", file=sys.stderr)
    
    # Load Master Tree
    master_tree = {
        "concepts": {},
        "ulos": [],
        "cios": [],
        "sios": [],
        "prerequisites": [],
    }
    
    # Try Supabase first (unless fallback requested)
    if not args.fallback_tsv and SUPABASE_AVAILABLE:
        load_env(repo_root)
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SERVICE_ROLE_KEY")
        
        if supabase_url and supabase_key:
            try:
                if not args.quiet:
                    print(f"[STEP 0] Loading Master Tree from Supabase...", file=sys.stderr)
                
                supabase = create_client(supabase_url, supabase_key)
                master_tree = load_from_supabase(supabase)
                
                if not args.quiet:
                    print(f"[STEP 0] ✓ Loaded from Supabase", file=sys.stderr)
            except Exception as e:
                if not args.quiet:
                    print(f"[STEP 0] ⚠ Supabase failed: {e}", file=sys.stderr)
                    print(f"[STEP 0] Falling back to TSV files...", file=sys.stderr)
    
    # Fallback to TSV if Supabase not available or failed
    if not master_tree["concepts"]:
        master_tree_project = projects_dir / "master-tree"
        if master_tree_project.exists():
            concepts, los = load_project_context(master_tree_project)
            ulos = [lo for lo in los if lo.get("lo_type") == "UNIVERSAL"]
            cios = [lo for lo in los if lo.get("lo_type") == "CONCEPTUAL_IMPL"]
            sios = [lo for lo in los if lo.get("lo_type") == "SPECIFIC_IMPL"]
            
            # Load prerequisites
            prereqs_file = master_tree_project / "output" / "lo_prerequisites.tsv"
            prereqs = []
            if prereqs_file.exists():
                with open(prereqs_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f, delimiter="\t")
                    prereqs = list(reader)
            
            master_tree = {
                "concepts": concepts,
                "ulos": ulos,
                "cios": cios,
                "sios": sios,
                "prerequisites": prereqs,
            }
            
            if not args.quiet:
                print(f"[STEP 0] ✓ Loaded from TSV files", file=sys.stderr)
    
    if not args.quiet:
        mc = len(master_tree["concepts"])
        mu = len(master_tree["ulos"])
        mci = len(master_tree["cios"])
        ms = len(master_tree["sios"])
        mp = len(master_tree["prerequisites"])
        print(f"[STEP 0] Master Tree: {mc} concepts, {mu} ULOs, {mci} CIOs, {ms} SIOs, {mp} prereqs", file=sys.stderr)
    
    # Parse tech stack
    tech_stack = [t.strip() for t in args.tech_stack.split(",")]
    
    # Build inventory
    inventory = build_reuse_inventory(
        goal=args.goal,
        tech_stack=tech_stack,
        master_tree=master_tree,
        projects=projects
    )
    
    # Output
    output_json = json.dumps(inventory, indent=2, ensure_ascii=False)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output_json, encoding="utf-8")
        if not args.quiet:
            print(f"[STEP 0] Wrote inventory to {output_path}", file=sys.stderr)
    else:
        print(output_json)
    
    # Print summary
    if not args.quiet:
        summary = inventory["reuse_summary"]
        print(f"\n[STEP 0] Reuse Summary:", file=sys.stderr)
        print(f"  Tier 1 (Master Tree): {'✓' if summary['tier1_master_available'] else '✗'}", file=sys.stderr)
        print(f"  Tier 2 High Reuse (≥0.7): {summary['tier2_high_reuse']} projects", file=sys.stderr)
        print(f"  Tier 2 Partial Reuse (0.4-0.7): {summary['tier2_partial_reuse']} projects", file=sys.stderr)
        
        if inventory["scored_projects"]:
            print(f"\n[STEP 0] Top 3 Similar Projects:", file=sys.stderr)
            for proj in inventory["scored_projects"][:3]:
                print(f"  {proj['slug']}: score={proj['score']}, level={proj['reuse_level']}, tech={proj['tech_stack']}", file=sys.stderr)


if __name__ == "__main__":
    main()
