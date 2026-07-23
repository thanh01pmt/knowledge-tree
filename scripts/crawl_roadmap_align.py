#!/usr/bin/env python3
"""
Crawl & Align Roadmap Script (v2)
Crawls roadmap.sh via Crawl4AI Server (protected by Cloudflare Access)
and aligns extracted topics/concepts with mlo-knowlege-tree.tsv.
"""

import os
import sys
import json
import re
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

# Root path configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
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

    print(f"🔄 Crawling roadmap via Crawl4AI: {url}...")
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
    """Parse concepts and topics from mlo-knowlege-tree.tsv accurately"""
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

            # Skip header description lines or column headers
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

def main():
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://roadmap.sh/python-data-analysis"
    env = load_env()
    
    html = fetch_roadmap(target_url, env)
    roadmap_topics = extract_roadmap_topics(html)
    
    print(f"\n✅ Extracted {len(roadmap_topics)} topics from {target_url}")
    
    concepts, topics, categories = parse_master_tsv(MASTER_TSV_PATH)
    print(f"📊 Master Tree loaded: {len(concepts)} concepts, {len(topics)} topics, {len(categories)} categories")
    
    matched, missing = align_topics(roadmap_topics, concepts, topics)
    
    print(f"\n🎯 ALIGNMENT RESULTS:")
    print(f"  - Matched items: {len(matched)}")
    print(f"  - Missing candidate items (Gaps): {len(missing)}")
    
    report_path = PROJECT_ROOT / ".work" / "roadmap_alignment_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Roadmap Alignment Report\n\n")
        f.write(f"- **Target Roadmap:** {target_url}\n")
        f.write(f"- **Total Topics Crawled:** {len(roadmap_topics)}\n")
        f.write(f"- **Matched with Master Tree:** {len(matched)}\n")
        f.write(f"- **Missing Candidates (Gaps to Supplement):** {len(missing)}\n\n")
        
        f.write("## 🟢 Matched Topics\n\n")
        f.write("| Roadmap Topic | Match Type | Master Code | Master Name |\n")
        f.write("|---|---|---|---|\n")
        for m in matched:
            f.write(f"| {m['roadmap_name']} | {m['match_type']} | `{m['code']}` | {m['matched_name']} |\n")
            
        f.write("\n## 🔴 Missing Candidates (Suggestions to Supplement)\n\n")
        f.write("These topics were found on the roadmap but are currently missing from `mlo-knowlege-tree.tsv`:\n\n")
        for item in missing:
            f.write(f"- [ ] {item}\n")

    print(f"\n📄 Report generated at: {report_path}")

if __name__ == "__main__":
    main()
