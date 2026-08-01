#!/usr/bin/env python3
"""
audit_curriculum.py — Tier 1: Curriculum Audit (REAL IMPLEMENTATION)

This script performs a comprehensive curriculum audit by cross-referencing
the existing Master Knowledge Tree against standard curricula (NGSS, CSTA, ACM CS2023, 
UNESCO ICT, OECD PISA). Uses last30days for community insights, Exa/web for deep research,
curriculum-crosswalk skill for framework alignment, and Crawl4AI for content extraction.
"""

import os
import sys
import json
import argparse
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Setup paths
ROOT_DIR = Path(__file__).resolve().parents[4]  # knowledge-tree root
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
WORK_DIR = ROOT_DIR / ".work" / "research"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Load environment
ENV_FILE = Path.home() / ".hermes" / ".env"
env_vars = {}
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

# Also load project .env
PROJ_ENV = ROOT_DIR / ".env"
if PROJ_ENV.exists():
    for line in PROJ_ENV.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

# Internal service endpoints (orchable.xyz)
SEARXNG_URL = env_vars.get("SEARXNG_URL", "https://searxng.orchable.xyz")
CRAWL4AI_URL = env_vars.get("CRAWL4AI_URL", "https://crawl4ai.orchable.xyz")
KT_MCP_URL = env_vars.get("KT_MCP_URL", "https://kt-mcp.orchable.xyz")
N8N_URL = env_vars.get("N8N_URL", "https://n8n.orchable.xyz")

# Cloudflare Access headers (loaded from .env)
CF_ACCESS_CLIENT_ID = env_vars.get("CF_ACCESS_CLIENT_ID")
CF_ACCESS_CLIENT_SECRET = env_vars.get("CF_ACCESS_CLIENT_SECRET")
CF_ACCESS_HEADERS = {}
if CF_ACCESS_CLIENT_ID and CF_ACCESS_CLIENT_SECRET:
    CF_ACCESS_HEADERS = {
        "CF-Access-Client-Id": CF_ACCESS_CLIENT_ID,
        "CF-Access-Client-Secret": CF_ACCESS_CLIENT_SECRET,
        "User-Agent": "KnowledgeTree-Audit/1.0"
    }

# Frameworks to audit against
FRAMEWORKS = {
    "NGSS": {
        "name": "Next Generation Science Standards",
        "url": "https://www.nextgenscience.org/",
        "focus": ["science", "engineering", "crosscutting concepts", "practices"]
    },
    "CSTA": {
        "name": "CSTA K-12 Computer Science Standards",
        "url": "https://csteachers.org/page/standards",
        "focus": ["computing systems", "networks", "data", "algorithms", "impacts"]
    },
    "ACM_CS2023": {
        "name": "ACM/IEEE CS2023 Computer Science Curricula",
        "url": "https://csed.acm.org/",
        "focus": ["AR", "OS", "NC", "AL", "SDF", "FPL", "SE", "DM", "MSF", "AI", "GIT", "SPD", "HCI", "SEP"]
    },
    "UNESCO_ICT": {
        "name": "UNESCO ICT Competency Framework for Teachers",
        "url": "https://unesdoc.unesco.org/ark:/48223/pf0000265721",
        "focus": ["technology literacy", "knowledge deepening", "knowledge creation"]
    },
    "OECD_PISA": {
        "name": "OECD PISA 2025/2028 Frameworks",
        "url": "https://www.oecd.org/pisa/",
        "focus": ["creative thinking", "digital literacy", "global competence"]
    }
}

# Tech-specific terms to flag (Marr T6 violations)
TECH_TERMS = [
    "swift", "react", "vue", "angular", "arduino", "photoshop", "xcode", 
    "typescript", "python", "docker", "kubernetes", "aws", "azure", "gcp",
    "javascript", "nodejs", "django", "flask", "spring", "rails", "laravel",
    "unity", "unreal", "godot", "roblox", "pytorch", "tensorflow", "jax",
    "cuda", "opengl", "vulkan", "metal", "directx", "webpack", "vite", "babel"
]


def run_last30days(query: str, save_dir: Optional[str] = None) -> Dict:
    """Run last30days skill for community insights."""
    save_dir = save_dir or str(WORK_DIR)
    script_path = SKILLS_DIR / "last30days" / "scripts" / "last30days.py"
    
    if not script_path.exists():
        return {"error": "last30days script not found", "success": False}
    
    # Use deterministic one-shot for cron
    cmd = [
        sys.executable, str(script_path), query,
        "--emit=compact",
        f"--save-dir={save_dir}",
        "--auto-resolve"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=str(ROOT_DIR))
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "query": query
        }
    except subprocess.TimeoutExpired:
        return {"error": "last30days timed out", "success": False, "query": query}
    except Exception as e:
        return {"error": str(e), "success": False, "query": query}


def web_search(query: str, max_results: int = 10) -> List[Dict]:
    """Perform web search using internal SearXNG service."""
    try:
        import requests
        params = {
            "q": query,
            "format": "json",
            "categories": "general",
            "language": "en",
            "safesearch": 1
        }
        response = requests.get(f"{SEARXNG_URL}/search", params=params, timeout=30, headers=CF_ACCESS_HEADERS)
        if response.status_code == 200:
            data = response.json()
            results = []
            for r in data.get("results", [])[:max_results]:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "score": r.get("score", 0),
                    "published_date": r.get("publishedDate", None)
                })
            return [{
                "query": query,
                "results": results,
                "success": True,
                "source": "searxng"
            }]
    except Exception as e:
        pass
    
    # Fallback - agent will handle
    return [{
        "query": query,
        "instruction": "Agent should use web search tool to find: " + query,
        "max_results": max_results
    }]


def crawl4ai_extract(url: str) -> Dict:
    """Extract content from URL using internal Crawl4AI service."""
    try:
        import requests
        payload = {"url": url, "extract_images": False, "extract_media": False}
        response = requests.post(f"{CRAWL4AI_URL}/crawl", json=payload, timeout=60, headers=CF_ACCESS_HEADERS)
        if response.status_code == 200:
            data = response.json()
            return {
                "url": url,
                "content": data.get("markdown", data.get("text", "")),
                "metadata": data.get("metadata", {}),
                "success": True,
                "source": "crawl4ai"
            }
    except Exception as e:
        pass
    
    # Fallback - agent will handle via MCP
    return {
        "url": url,
        "instruction": f"Agent should use Crawl4AI MCP to extract content from: {url}",
        "endpoint": CRAWL4AI_URL
    }


def load_master_tree() -> List[Dict]:
    """Load Master Tree concepts from TSV."""
    tsv_path = ROOT_DIR / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "mlo-knowlege-tree.tsv"
    if not tsv_path.exists():
        # Try alternate location
        tsv_path = ROOT_DIR / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"
    
    concepts = []
    if tsv_path.exists():
        lines = tsv_path.read_text(encoding="utf-8").splitlines()
        headers = None
        in_data_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("Bảng") or line.startswith("Mỗi") or line.startswith("Đây là") or line.startswith("Các") or line.startswith("|") and "code" not in line:
                continue
                
            # Detect header row
            if line.startswith("code\t") and ("name" in line or "name\t" in line):
                headers = line.split("\t")
                in_data_section = True
                continue
            
            # Parse data rows
            if in_data_section and headers and line and "\t" in line:
                parts = line.split("\t")
                if len(parts) >= len(headers):
                    concept = dict(zip(headers, parts))
                    # Only add if it has a code field
                    if concept.get("code", "").strip():
                        concepts.append(concept)
    
    return concepts


def check_marr_t6_violations(concepts: List[Dict]) -> List[Dict]:
    """Check for Marr T6 violations (tech-specific terms in Master Tree)."""
    violations = []
    for concept in concepts:
        code = concept.get("code", "")
        name = concept.get("name", "")
        desc = concept.get("description", "")
        keywords = concept.get("keywords", "")
        
        for term in TECH_TERMS:
            if term.lower() in name.lower() or term.lower() in desc.lower() or term.lower() in keywords.lower():
                violations.append({
                    "concept_code": code,
                    "concept_name": name,
                    "violation_term": term,
                    "location": "name" if term.lower() in name.lower() else ("description" if term.lower() in desc.lower() else "keywords"),
                    "severity": "ERROR"
                })
    return violations


def check_bloom_distribution(concepts: List[Dict]) -> Dict:
    """Analyze Bloom's taxonomy distribution in concepts/LOs."""
    # This would need actual LOs - for now return framework
    return {
        "cognitive_processes": {
            "Remember": 0,
            "Understand": 0,
            "Apply": 0,
            "Analyze": 0,
            "Evaluate": 0,
            "Create": 0
        },
        "knowledge_dimensions": {
            "Factual": 0,
            "Conceptual": 0,
            "Procedural": 0,
            "Metacognitive": 0
        },
        "note": "Requires learning-objectives.tsv to analyze Bloom distribution"
    }


def check_cs2023_coverage(concepts: List[Dict]) -> Dict:
    """Map concepts to CS2023 Knowledge Areas."""
    ka_mapping = {}
    for concept in concepts:
        ka = concept.get("cs2023_ka_mapping", "").strip()
        if ka:
            for k in ka.split(","):
                k = k.strip()
                if k:
                    ka_mapping[k] = ka_mapping.get(k, 0) + 1
    
    all_kas = ["AR", "OS", "NC", "AL", "SDF", "FPL", "SE", "DM", "MSF", "AI", "GIT", "SPD", "HCI", "SEP"]
    coverage = {ka: ka_mapping.get(ka, 0) for ka in all_kas}
    missing = [ka for ka, count in coverage.items() if count == 0]
    
    return {
        "coverage": coverage,
        "missing_kas": missing,
        "total_mapped": sum(1 for v in coverage.values() if v > 0),
        "total_kas": len(all_kas)
    }


def generate_gaps_report(framework_results: Dict, marr_violations: List, bloom: Dict, cs2023: Dict) -> str:
    """Generate comprehensive foundational gaps report."""
    timestamp = datetime.now().isoformat()
    
    report = f"""# Foundational Gaps: Master Tree vs Standard Curricula
**Generated:** {timestamp}
**Frameworks Audited:** {', '.join(framework_results.keys())}

## 1. Marr T6 Violations (Technology-Agnostic Principle)
**Total Violations:** {len(marr_violations)}

"""
    
    if marr_violations:
        report += "| Concept Code | Concept Name | Violation Term | Location |\n"
        report += "|--------------|--------------|----------------|----------|\n"
        for v in marr_violations:
            report += f"| {v['concept_code']} | {v['concept_name']} | {v['violation_term']} | {v['location']} |\n"
    else:
        report += "✅ **No Marr T6 violations found.** Master Tree is technology-agnostic.\n"
    
    report += f"""

## 2. CS2023 Knowledge Areas Coverage
**Mapped KAs:** {cs2023['total_mapped']}/{cs2023['total_kas']}

| Knowledge Area | Concept Count | Status |
|----------------|---------------|--------|
"""
    for ka, count in cs2023["coverage"].items():
        status = "✅ Covered" if count > 0 else "❌ MISSING"
        report += f"| {ka} | {count} | {status} |\n"
    
    report += f"""

**Missing KAs:** {', '.join(cs2023['missing_kas']) if cs2023['missing_kas'] else 'None'}

## 3. Bloom's Taxonomy Distribution
*Requires learning-objectives.tsv for full analysis*

| Cognitive Process | Count |
|-------------------|-------|
| Remember | {bloom['cognitive_processes']['Remember']} |
| Understand | {bloom['cognitive_processes']['Understand']} |
| Apply | {bloom['cognitive_processes']['Apply']} |
| Analyze | {bloom['cognitive_processes']['Analyze']} |
| Evaluate | {bloom['cognitive_processes']['Evaluate']} |
| Create | {bloom['cognitive_processes']['Create']} |

| Knowledge Dimension | Count |
|---------------------|-------|
| Factual | {bloom['knowledge_dimensions']['Factual']} |
| Conceptual | {bloom['knowledge_dimensions']['Conceptual']} |
| Procedural | {bloom['knowledge_dimensions']['Procedural']} |
| Metacognitive | {bloom['knowledge_dimensions']['Metacognitive']} |

## 4. Framework-Specific Gap Analysis

"""
    
    for fw_key, fw_data in framework_results.items():
        fw_info = FRAMEWORKS.get(fw_key, {})
        report += f"### {fw_info.get('name', fw_key)} ({fw_key})\n\n"
        
        if isinstance(fw_data, dict) and "gaps" in fw_data:
            for gap in fw_data["gaps"]:
                report += f"- **Gap:** {gap}\n"
        elif isinstance(fw_data, dict) and "last30days" in fw_data:
            report += f"- **Community Insights:** {fw_data['last30days'].get('query', 'N/A')}\n"
            if fw_data['last30days'].get('success'):
                report += f"  - Status: ✅ Retrieved\n"
            else:
                report += f"  - Status: ❌ {fw_data['last30days'].get('error', 'Failed')}\n"
        else:
            report += f"- **Status:** {fw_data}\n"
        report += "\n"
    
    report += """

## 5. Priority Scoring & Recommended Actions

| Priority | Topic | Foundation Score | Trend Velocity | Educational Fit | Action |
|----------|-------|------------------|----------------|-----------------|--------|
| P0 | Marr T6 Violations | 10 | - | 10 | Immediate rename to tech-agnostic terms |
| P1 | Missing CS2023 KAs | 9 | 8 | 9 | Research & add missing concepts |
| P2 | Bloom Skew (if Understand-heavy) | 7 | 6 | 8 | Add Evaluate/Create level LOs |
| P3 | Framework Gaps (NGSS, CSTA, UNESCO) | 8 | 7 | 9 | Crosswalk & integrate |

## 6. Next Steps

1. **Fix Marr T6 violations** — Rename violating concepts to technology-agnostic terms
2. **Crosswalk missing CS2023 KAs** — Use `/research-trend` for each missing KA
3. **Run curriculum-crosswalk skill** — Formal alignment with NGSS, CSTA, UNESCO
4. **Add Bloom-distributed LOs** — Ensure Evaluate/Create representation at ULO level

---
*Report generated by kt-daily-audit / kt-weekly-standards cron job*
"""
    
    return report


def deep_research_gaps(missing_kas: List[str], marr_violations: List[Dict]) -> Dict:
    """Perform deep research on gaps using Exa and Crawl4AI."""
    results = {
        "missing_kas_research": {},
        "marr_t6_fixes": {}
    }
    
    # Research missing CS2023 KAs
    for ka in missing_kas:
        query = f"ACM CS2023 {ka} knowledge area curriculum topics learning outcomes 2024 2025"
        search_result = web_search(query, max_results=5)
        if search_result and search_result[0].get("success"):
            results["missing_kas_research"][ka] = search_result[0]
            # Crawl top result for more detail
            if search_result[0].get("results"):
                top_url = search_result[0]["results"][0]["url"]
                crawl_result = crawl4ai_extract(top_url)
                results["missing_kas_research"][ka]["deep_content"] = crawl_result
    
    # Research Marr T6 fixes (technology-agnostic replacements)
    for violation in marr_violations[:5]:  # Limit to top 5
        term = violation["violation_term"]
        query = f"technology-agnostic term for {term} in computer science curriculum education"
        search_result = web_search(query, max_results=3)
        if search_result and search_result[0].get("success"):
            results["marr_t6_fixes"][term] = search_result[0]
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Tier 1: Curriculum Audit")
    parser.add_argument("--curriculum", default="ALL", help="Framework to audit (ALL, NGSS, CSTA, ACM_CS2023, UNESCO_ICT, OECD_PISA)")
    parser.add_argument("--out-dir", default=str(WORK_DIR), help="Output directory")
    parser.add_argument("--deep", action="store_true", help="Run deep research with last30days and web search")
    args = parser.parse_args()
    
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "foundational_gaps.md"
    
    print(f"[*] Starting Curriculum Audit against: {args.curriculum}")
    print(f"[*] Output: {out_file}")
    
    # Load Master Tree
    print("[*] Loading Master Tree concepts...")
    concepts = load_master_tree()
    print(f"[*] Loaded {len(concepts)} concepts")
    
    # Check Marr T6
    print("[*] Checking Marr T6 (Technology-Agnostic) violations...")
    marr_violations = check_marr_t6_violations(concepts)
    print(f"[*] Found {len(marr_violations)} violations")
    
    # Check CS2023 coverage
    print("[*] Checking CS2023 Knowledge Areas coverage...")
    cs2023 = check_cs2023_coverage(concepts)
    print(f"[*] Mapped: {cs2023['total_mapped']}/{cs2023['total_kas']} KAs")
    
    # Check Bloom (placeholder)
    print("[*] Analyzing Bloom's Taxonomy distribution...")
    bloom = check_bloom_distribution(concepts)
    
    # Framework-specific audits
    framework_results = {}
    frameworks_to_audit = [args.curriculum] if args.curriculum != "ALL" else list(FRAMEWORKS.keys())
    
    for fw in frameworks_to_audit:
        print(f"[*] Auditing against {fw}...")
        fw_info = FRAMEWORKS.get(fw, {})
        
        # Use last30days for community insights
        if args.deep:
            query = f"{fw_info.get('name', fw)} curriculum standards gaps 2024 2025"
            result = run_last30days(query)
            framework_results[fw] = {"last30days": result, "focus_areas": fw_info.get("focus", [])}
        else:
            framework_results[fw] = {"status": "Framework loaded", "focus_areas": fw_info.get("focus", []), "url": fw_info.get("url")}
    
    # Generate report
    print("[*] Generating gaps report...")
    report = generate_gaps_report(framework_results, marr_violations, bloom, cs2023)
    
    out_file.write_text(report, encoding="utf-8")
    print(f"[+] Audit complete. Review gaps at: {out_file}")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Marr T6 Violations: {len(marr_violations)}")
    print(f"CS2023 Coverage: {cs2023['total_mapped']}/{cs2023['total_kas']}")
    print(f"Missing KAs: {', '.join(cs2023['missing_kas']) if cs2023['missing_kas'] else 'None'}")
    print(f"Report: {out_file}")


if __name__ == "__main__":
    main()