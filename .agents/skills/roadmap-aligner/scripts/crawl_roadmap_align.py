#!/usr/bin/env python3
"""
Crawl & Align Roadmap Script with Tri-Layer Strategy:
- Layer 1: Crawl4AI (Roadmap SVG crawling & Gap Identification)
- Layer 2: SearXNG (Independent web verification & multi-source reference search)
- Layer 3: Context7 API (Official technical library docs & description extraction)
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

# Root path configuration
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
MASTER_TSV_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
DOTENV_PATH = PROJECT_ROOT / ".env"
DOTENV_LOCAL_PATH = PROJECT_ROOT / ".env.local"

def load_env():
    """Load environment variables from .env and .env.local"""
    env_vars = {}
    for p in [DOTENV_PATH, DOTENV_LOCAL_PATH]:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip().strip("'\"")
    return env_vars

# ── LAYER 1: CRAWL4AI ────────────────────────────────────────────────────────
def fetch_roadmap(url: str, env: dict) -> str:
    """Crawl roadmap URL using Crawl4AI server with CF Access headers"""
    crawl4ai_url = env.get("CRAWL4AI_URL", "https://crawl4ai.orchable.xyz")
    cf_id = env.get("CF_ACCESS_CLIENT_ID", "")
    cf_secret = env.get("CF_ACCESS_CLIENT_SECRET", "")

    headers = {
        "CF-Access-Client-Id": cf_id,
        "CF-Access-Client-Secret": cf_secret,
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    payload = {
        "urls": [url],
        "crawler_config": {
            "delay_before_return_html": 3.0,
            "wait_for": "css:svg"
        }
    }

    req = urllib.request.Request(
        f"{crawl4ai_url}/crawl",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    print(f"🌐 [Layer 1 - Crawl4AI] Crawling roadmap: {url}...")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        results = res.get("results", [])
        if not results or not results[0].get("success"):
            raise RuntimeError(f"Crawl failed: {res}")
        return results[0]["html"]

def extract_roadmap_topics(html: str) -> list[str]:
    """Extract topic names from SVG text elements"""
    soup = BeautifulSoup(html, "html.parser")
    topics = []
    
    ignore_texts = {
        "We value your privacy", "Consent Preferences", "Necessary cookies",
        "Feedback Wanted", "All Roadmaps", "Prefer us on Google", "Weekly Newsletter",
        "Personalize", "Roadmap", "Download", "AI TutorAI", "Share", "Star"
    }

    for text_tag in soup.find_all("text"):
        tspan_list = text_tag.find_all("tspan")
        if tspan_list:
            combined = " ".join([t.get_text(strip=True) for t in tspan_list if t.get_text(strip=True)])
        else:
            combined = text_tag.get_text(strip=True)
        
        combined = combined.strip()
        if combined and combined not in topics and len(combined) > 1:
            if not any(ign.lower() in combined.lower() for ign in ignore_texts):
                topics.append(combined)
                
    return topics

def parse_master_tsv(tsv_path: Path):
    """Parse concepts, topics, and categories from mlo-knowlege-tree.tsv"""
    concepts = []
    topics = []
    categories = []
    
    if not tsv_path.exists():
        print(f"⚠️ Master TSV not found at {tsv_path}")
        return concepts, topics, categories

    with open(tsv_path, "r", encoding="utf-8") as f:
        current_section = None
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("Bảng 1"):
                current_section = "fields"
                continue
            elif line_str.startswith("Bảng 2"):
                current_section = "subjects"
                continue
            elif line_str.startswith("Bảng 3"):
                current_section = "categories"
                continue
            elif line_str.startswith("Bảng 4"):
                current_section = "topics"
                continue
            elif line_str.startswith("Bảng 5"):
                current_section = "concepts"
                continue

            if line_str.startswith("Đây là") or line_str.startswith("Mỗi Field") or line_str.startswith("code\t"):
                continue

            parts = line.rstrip("\r\n").split("\t")
            code = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else ""

            if not code or not name:
                continue

            if current_section == "concepts":
                concepts.append({
                    "code": code,
                    "name": name,
                    "topic_code": parts[3].strip() if len(parts) > 3 else ""
                })
            elif current_section == "topics":
                topics.append({
                    "code": code,
                    "name": name,
                    "category_code": parts[3].strip() if len(parts) > 3 else ""
                })
            elif current_section == "categories":
                categories.append({
                    "code": code,
                    "name": name,
                    "subject_codes": parts[3].strip() if len(parts) > 3 else ""
                })
                
    return concepts, topics, categories

def align_topics(roadmap_topics: list[str], master_concepts: list[dict], master_topics: list[dict]):
    """Align extracted roadmap topics with existing master concepts & topics"""
    matched = []
    missing = []

    concept_map = {c["name"].lower(): c for c in master_concepts}
    topic_map = {t["name"].lower(): t for t in master_topics}

    for rt in roadmap_topics:
        rt_clean = rt.lower().strip()
        
        # 1. Exact match by name
        matched_concept = concept_map.get(rt_clean)
        matched_topic = topic_map.get(rt_clean)
        
        if matched_concept:
            matched.append({
                "roadmap_name": rt,
                "match_type": "Exact (Concept)",
                "code": matched_concept["code"],
                "matched_name": matched_concept["name"]
            })
        elif matched_topic:
            matched.append({
                "roadmap_name": rt,
                "match_type": "Exact (Topic)",
                "code": matched_topic["code"],
                "matched_name": matched_topic["name"]
            })
        else:
            # 2. Token overlap / Keyword match
            rt_tokens = set(re.findall(r"\w+", rt_clean))
            best_match = None
            best_score = 0.0
            
            all_items = [(c, "Concept") for c in master_concepts] + [(t, "Topic") for t in master_topics]
            for item, item_type in all_items:
                name_tokens = set(re.findall(r"\w+", item["name"].lower()))
                if not name_tokens:
                    continue
                intersection = rt_tokens.intersection(name_tokens)
                score = len(intersection) / max(len(rt_tokens), len(name_tokens))
                
                if score > best_score and score >= 0.5:
                    best_score = score
                    best_match = (item, item_type)
            
            if best_match:
                item, item_type = best_match
                matched.append({
                    "roadmap_name": rt,
                    "match_type": f"Fuzzy ({item_type} - {int(best_score*100)}%)",
                    "code": item["code"],
                    "matched_name": item["name"]
                })
            else:
                missing.append(rt)

    return matched, missing

# ── LAYER 2: SEARXNG ─────────────────────────────────────────────────────────
def verify_candidates_with_searxng(candidates: list[str], env: dict, max_verify: int = 15) -> list[dict]:
    """Independently verify missing candidates using SearXNG metasearch API"""
    searxng_url = env.get("SEARXNG_URL", "https://searxng.orchable.xyz")
    cf_id = env.get("CF_ACCESS_CLIENT_ID", "")
    cf_secret = env.get("CF_ACCESS_CLIENT_SECRET", "")

    headers = {
        "CF-Access-Client-Id": cf_id,
        "CF-Access-Client-Secret": cf_secret,
        "User-Agent": "Mozilla/5.0"
    }

    verified_results = []
    print(f"🔎 [Layer 2 - SearXNG] Independently verifying top {min(len(candidates), max_verify)} candidates...")

    for candidate in candidates[:max_verify]:
        query = candidate
        url = f"{searxng_url}/search?" + urllib.parse.urlencode({
            "q": query,
            "format": "json"
        })

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results = data.get("results", [])
                
                if results:
                    top_ref = results[0]
                    verified_results.append({
                        "candidate": candidate,
                        "verified": True,
                        "confidence": "High (Verified)",
                        "title": top_ref.get("title", ""),
                        "url": top_ref.get("url", ""),
                        "snippet": top_ref.get("content", "")[:150]
                    })
                else:
                    verified_results.append({
                        "candidate": candidate,
                        "verified": False,
                        "confidence": "SearXNG Standby",
                        "title": "N/A",
                        "url": "",
                        "snippet": "No response from search engine upstream."
                    })
        except Exception as e:
            verified_results.append({
                "candidate": candidate,
                "verified": False,
                "confidence": "Error",
                "title": "",
                "url": "",
                "snippet": str(e)
            })

    return verified_results

# ── LAYER 3: CONTEXT7 API ───────────────────────────────────────────────────
def enrich_candidates_with_context7(candidates: list[str], env: dict, max_enrich: int = 15) -> list[dict]:
    """Fetch official library docs & descriptions using Context7 API"""
    ctx7_key = env.get("CONTEXT7_API_KEY", "")
    headers = {"User-Agent": "Mozilla/5.0"}
    if ctx7_key:
        headers["Authorization"] = f"Bearer {ctx7_key}"

    enriched = []
    print(f"📚 [Layer 3 - Context7] Extracting official docs for top {min(len(candidates), max_enrich)} candidate libraries...")

    for candidate in candidates[:max_enrich]:
        url = "https://context7.com/api/v1/search?" + urllib.parse.urlencode({"query": candidate})
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results = data.get("results", [])
                if results:
                    top = results[0]
                    enriched.append({
                        "candidate": candidate,
                        "library_id": top.get("id", ""),
                        "title": top.get("title", ""),
                        "description": top.get("description", "")
                    })
                else:
                    enriched.append({
                        "candidate": candidate,
                        "library_id": "N/A",
                        "title": candidate,
                        "description": "General concept / No dedicated Context7 library"
                    })
        except Exception as e:
            enriched.append({
                "candidate": candidate,
                "library_id": "Error",
                "title": candidate,
                "description": str(e)
            })

    return enriched

def main():
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://roadmap.sh/python-data-analysis"
    env = load_env()
    
    # Layer 1 Execution
    html = fetch_roadmap(target_url, env)
    roadmap_topics = extract_roadmap_topics(html)
    print(f"✅ Extracted {len(roadmap_topics)} topics from {target_url}")
    
    concepts, topics, categories = parse_master_tsv(MASTER_TSV_PATH)
    print(f"📊 Master Tree loaded: {len(concepts)} concepts, {len(topics)} topics, {len(categories)} categories")
    
    matched, missing = align_topics(roadmap_topics, concepts, topics)
    print(f"\n🎯 ALIGNMENT RESULTS:")
    print(f"  - Matched items: {len(matched)}")
    print(f"  - Missing candidate items (Gaps): {len(missing)}")

    # Layer 2 Execution (SearXNG Independent Verification)
    searxng_results = verify_candidates_with_searxng(missing, env, max_verify=15)
    
    # Layer 3 Execution (Context7 Official Library Docs Enrichment)
    context7_results = enrich_candidates_with_context7(missing, env, max_enrich=15)
    
    report_path = PROJECT_ROOT / ".work" / "roadmap_alignment_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Tri-Layer Roadmap Alignment & Enrichment Report\n\n")
        f.write(f"- **Target Roadmap:** {target_url}\n")
        f.write(f"- **Total Topics Crawled (Layer 1 - Crawl4AI):** {len(roadmap_topics)}\n")
        f.write(f"- **Matched with Master Tree:** {len(matched)}\n")
        f.write(f"- **Missing Candidates (Gaps):** {len(missing)}\n\n")
        
        f.write("## 🟢 Matched Topics\n\n")
        f.write("| Roadmap Topic | Match Type | Master Code | Master Name |\n")
        f.write("|---|---|---|---|\n")
        for m in matched:
            f.write(f"| {m['roadmap_name']} | {m['match_type']} | `{m['code']}` | {m['matched_name']} |\n")

            
        f.write("\n## 🔎 Layer 2: SearXNG Independent Multi-Source Verification\n\n")
        f.write("| Candidate Topic | Status | Reference Source | Snippet / Description |\n")
        f.write("|---|---|---|---|\n")
        for v in searxng_results:
            ref_link = f"[{v['title'][:30]}]({v['url']})" if v['url'] else "N/A"
            f.write(f"| **{v['candidate']}** | `{v['confidence']}` | {ref_link} | {v['snippet']} |\n")

        f.write("\n## 📚 Layer 3: Context7 Official Library Documentation & Description\n\n")
        f.write("| Candidate Concept | Context7 Library ID | Official Description |\n")
        f.write("|---|---|---|\n")
        for c in context7_results:
            f.write(f"| **{c['candidate']}** | `{c['library_id']}` | {c['description']} |\n")

        f.write("\n## 🔴 All Missing Candidates (Suggestions to Supplement)\n\n")
        for item in missing:
            f.write(f"- [ ] {item}\n")

    print(f"\n📄 Tri-Layer report generated successfully at: {report_path}")

if __name__ == "__main__":
    main()
