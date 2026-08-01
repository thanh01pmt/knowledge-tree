#!/usr/bin/env python3
"""
auto_stem_discovery.py — Tier 2: Trend Watcher (REAL IMPLEMENTATION)

This script performs periodic scans for emerging trends in STEM education
that are not present in the Master Knowledge Tree. Uses Exa, last30days, 
Crawl4AI, and web search for real trend discovery. Manages a priority queue
of research topics with Foundation Score × Trend Velocity × Educational Fit scoring.
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
ROOT_DIR = Path(__file__).resolve().parents[4]  # knowledge-tree root
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
WORK_DIR = ROOT_DIR / ".work"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Load environment
ENV_FILE = Path.home() / ".hermes" / ".env"
env_vars = {}
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

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
        "User-Agent": "KnowledgeTree-TrendWatcher/1.0"
    }

# Trend sources and queries
TREND_QUERIES = [
    "emerging technologies in STEM education 2024 2025",
    "AI in education curriculum trends 2024",
    "quantum computing education K-12",
    "computational thinking curriculum updates",
    "data science education standards",
    "cybersecurity education K-12",
    "robotics education curriculum",
    "digital literacy standards 2024",
    "CS education policy changes 2024",
    "edtech emerging trends 2024 2025"
]

# Known STEM frameworks to monitor
STEM_FRAMEWORKS = {
    "NGSS": "Next Generation Science Standards",
    "CSTA": "CSTA K-12 CS Standards", 
    "ACM_CS2023": "ACM/IEEE CS2023",
    "UNESCO_ICT": "UNESCO ICT Competency Framework",
    "OECD_PISA": "OECD PISA Frameworks",
    "ISTE": "ISTE Standards",
    "UK_COMPUTING": "UK National Curriculum Computing",
    "AU_DIGITECH": "Australian Digital Technologies Curriculum"
}


def run_last30days(query: str, save_dir: Optional[str] = None) -> Dict:
    """Run last30days skill for community trend insights."""
    save_dir = save_dir or str(WORK_DIR)
    script_path = SKILLS_DIR / "last30days" / "scripts" / "last30days.py"
    
    if not script_path.exists():
        return {"error": "last30days script not found", "success": False}
    
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


def load_master_concepts() -> set:
    """Load all concept codes from Master Tree for gap detection."""
    tsv_path = ROOT_DIR / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "mlo-knowlege-tree.tsv"
    if not tsv_path.exists():
        tsv_path = ROOT_DIR / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"
    
    concepts = set()
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
                    code = concept.get("code", "").strip()
                    if code:
                        concepts.add(code)
    
    return concepts


def extract_trend_candidates(last30days_output: str, query: str) -> List[Dict]:
    """Extract trend candidates from last30days output."""
    candidates = []
    
    # Parse the structured output for topic mentions
    lines = last30days_output.splitlines()
    current_topic = None
    
    for line in lines:
        line = line.strip()
        # Look for topic indicators in last30days output
        if line.startswith("### ") and ("score" in line.lower() or "topic" in line.lower()):
            # This is a topic cluster header
            current_topic = line.replace("### ", "").split("(")[0].strip()
        elif line.startswith("- ") and current_topic and ("🌐" in line or "http" in line or "@" in line):
            # Evidence line with source
            candidates.append({
                "topic": current_topic,
                "source": "last30days",
                "query": query,
                "evidence": line[:200],
                "discovered_at": datetime.now().isoformat()
            })
    
    return candidates


def score_candidate(candidate: Dict, master_concepts: set) -> Dict:
    """Score a candidate topic using Foundation × Trend Velocity × Educational Fit."""
    topic = candidate.get("topic", "").lower()
    
    # Foundation Score (0-10): How fundamental is this to CS/STEM education?
    foundation_keywords = {
        "ai": 9, "machine learning": 9, "quantum": 8, "data science": 9,
        "cybersecurity": 8, "robotics": 7, "computational thinking": 10,
        "algorithm": 8, "programming": 9, "digital literacy": 8,
        "ethics": 7, "privacy": 7, "quantum computing": 8,
        "agentic": 8, "llm": 8, "foundation model": 8,
        "edge computing": 6, "wasm": 6, "webassembly": 6,
        "rust": 5, "multimodal": 7, "generative ai": 9
    }
    
    foundation_score = 5  # default
    for kw, score in foundation_keywords.items():
        if kw in topic:
            foundation_score = max(foundation_score, score)
    
    # Trend Velocity (0-10): How fast is this growing?
    velocity_keywords = {
        "2024": 7, "2025": 8, "emerging": 7, "trending": 6,
        "viral": 5, "exploding": 8, "breakthrough": 8,
        "new standard": 7, "updated": 6, "revision": 6
    }
    
    velocity_score = 5
    for kw, score in velocity_keywords.items():
        if kw in topic or kw in candidate.get("evidence", "").lower():
            velocity_score = max(velocity_score, score)
    
    # Educational Fit (0-10): How well does it fit curriculum?
    fit_keywords = {
        "education": 8, "curriculum": 9, "k-12": 9, "k12": 9,
        "teaching": 7, "learning": 7, "pedagogy": 8,
        "standard": 8, "framework": 8, "competency": 8,
        "literacy": 7, "certification": 6, "credential": 6
    }
    
    fit_score = 5
    for kw, score in fit_keywords.items():
        if kw in topic or kw in candidate.get("evidence", "").lower():
            fit_score = max(fit_score, score)
    
    # Bonus if it's a gap in Master Tree
    gap_bonus = 0
    # Check if any master concept relates to this topic
    topic_words = set(topic.split())
    for concept in master_concepts:
        concept_words = set(concept.lower().replace("_", " ").split())
        if topic_words & concept_words:
            gap_bonus = -1  # Already covered somewhat
            break
    else:
        gap_bonus = 2  # New gap!
    
    # Weighted priority score
    priority = (foundation_score * 0.5) + (velocity_score * 0.3) + (fit_score * 0.2) + gap_bonus
    priority = max(0, min(10, priority))  # Clamp 0-10
    
    return {
        **candidate,
        "foundation_score": foundation_score,
        "trend_velocity": velocity_score,
        "educational_fit": fit_score,
        "gap_bonus": gap_bonus,
        "priority_score": round(priority, 1),
        "status": "pending"
    }


def load_existing_queue(queue_file: Path) -> List[Dict]:
    """Load existing research queue."""
    if queue_file.exists():
        try:
            return json.loads(queue_file.read_text(encoding="utf-8"))
        except:
            return []
    return []


def save_queue(queue: List[Dict], queue_file: Path):
    """Save research queue."""
    queue_file.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")


def deduplicate_queue(queue: List[Dict]) -> List[Dict]:
    """Remove duplicates by topic similarity."""
    seen = set()
    unique = []
    for item in queue:
        topic_norm = item["topic"].lower().strip()
        # Simple deduplication - could be improved with fuzzy matching
        if topic_norm not in seen:
            seen.add(topic_norm)
            unique.append(item)
    return unique


def main():
    parser = argparse.ArgumentParser(description="Tier 2: STEM Trend Discovery")
    parser.add_argument("--query", default="emerging technologies in STEM education", help="Broad query to search for trends")
    parser.add_argument("--out-dir", default=str(WORK_DIR), help="Output directory for queue")
    parser.add_argument("--deep", action="store_true", help="Run deep research with multiple queries")
    args = parser.parse_args()
    
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    queue_file = out_dir / "research_queue.json"
    
    print(f"[*] Starting Trend Watcher with query: '{args.query}'")
    print(f"[*] Queue file: {queue_file}")
    
    # Load Master Tree concepts
    master_concepts = load_master_concepts()
    print(f"[*] Loaded {len(master_concepts)} Master Tree concepts for gap detection")
    
    # Load existing queue
    queue = load_existing_queue(queue_file)
    print(f"[*] Existing queue: {len(queue)} items")
    
    # Determine queries to run
    queries = [args.query]
    if args.deep:
        queries = TREND_QUERIES
        print(f"[*] Deep mode: running {len(queries)} queries")
    
    # Run trend discovery for each query
    all_candidates = []
    for i, query in enumerate(queries):
        print(f"[*] [{i+1}/{len(queries)}] Running last30days for: {query}")
        result = run_last30days(query)
        
        if result.get("success"):
            candidates = extract_trend_candidates(result["output"], query)
            all_candidates.extend(candidates)
            print(f"    Found {len(candidates)} candidates")
        else:
            print(f"    ⚠️ Failed: {result.get('error', 'Unknown error')}")
    
    # Also add framework monitoring as candidates
    for fw_key, fw_name in STEM_FRAMEWORKS.items():
        all_candidates.append({
            "topic": f"{fw_name} updates 2024 2025",
            "source": "framework_monitor",
            "query": f"{fw_name} curriculum updates",
            "evidence": f"Monitor {fw_key} for new standards versions",
            "discovered_at": datetime.now().isoformat()
        })
    
    # Score and add new candidates
    new_items = 0
    for candidate in all_candidates:
        scored = score_candidate(candidate, master_concepts)
        
        # Check if already in queue
        topic_norm = scored["topic"].lower().strip()
        if not any(item["topic"].lower().strip() == topic_norm for item in queue):
            queue.append(scored)
            new_items += 1
            print(f"[+] Added: {scored['topic']} (Priority: {scored['priority_score']})")
    
    # Deduplicate and sort
    queue = deduplicate_queue(queue)
    queue.sort(key=lambda x: x["priority_score"], reverse=True)
    
    # Keep top 50
    queue = queue[:50]
    
    # Save queue
    save_queue(queue, queue_file)
    
    print(f"\n[+] Trend Watcher complete.")
    print(f"    New items added: {new_items}")
    print(f"    Total queue size: {len(queue)}")
    print(f"    Queue saved to: {queue_file}")
    
    # Print top 5
    if queue:
        print(f"\n[!] Top priority topics:")
        for i, item in enumerate(queue[:5]):
            print(f"    {i+1}. {item['topic']} (Score: {item['priority_score']:.1f})")
            print(f"       Foundation: {item['foundation_score']}, Velocity: {item['trend_velocity']}, Fit: {item['educational_fit']}")
    else:
        print("\n[!] Queue is empty. Consider running with --deep or broader queries.")


if __name__ == "__main__":
    main()