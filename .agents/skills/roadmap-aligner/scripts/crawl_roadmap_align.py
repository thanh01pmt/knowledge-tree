#!/usr/bin/env python3
"""
Crawl & Align Roadmap Script with 2-Step Decision Framework & Tri-Layer Strategy:
- Layer 1: Crawl4AI (Roadmap SVG crawling & Sequence/Prerequisite Graph Extraction)
- Layer 2: SearXNG (Independent web verification & multi-source reference search)
- Layer 3: Context7 API (Official technical library docs & description extraction)

Decision Framework:
- Step 1: Concrete Tool Check -> Map tool (pip, npm, venv, VS Code) as Keyword/Metadata under an Abstract Concept (create concept if missing).
- Step 2: Abstract Concept Check -> Promote items satisfying abstract criteria directly as new Concept proposals in Master Tree.
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
STAGING_TSV_PATH = PROJECT_ROOT / "general-context" / "mlo-knowlege-tree.tsv"
ORIGINAL_MASTER_TSV_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
MASTER_TSV_PATH = STAGING_TSV_PATH if STAGING_TSV_PATH.exists() else ORIGINAL_MASTER_TSV_PATH
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

def discover_and_download_roadmap_json(target_url: str, dest_path: Path) -> bool:
    """
    Auto-discover and download the exact roadmap JSON payload for ANY roadmap.sh URL.
    Strategies:
    1. Direct slug endpoint: https://roadmap.sh/<slug>.json
    2. HTML inspection: parse script tags / embedded React state for JSON URL or raw data.
    """
    parsed = urllib.parse.urlparse(target_url)
    slug = parsed.path.strip("/").split("/")[-1]
    if slug.endswith(".json"):
        slug = slug[:-5]
    if not slug:
        slug = "frontend"
        
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Strategy 1: Direct endpoint https://roadmap.sh/<slug>.json
    direct_json_url = f"https://roadmap.sh/{slug}.json"
    print(f"🔍 [JSON Discovery Engine] Strategy 1: Trying endpoint {direct_json_url}...")
    try:
        req = urllib.request.Request(direct_json_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            obj = json.loads(content.decode("utf-8"))
            if "nodes" in obj:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                dest_path.write_bytes(content)
                print(f"✅ [JSON Discovery Engine] Discovered & saved JSON for '{slug}' -> {dest_path} ({len(content)} bytes)")
                return True
    except Exception as e:
        print(f"ℹ️ Strategy 1 missed: {e}")

    # Strategy 2: HTML discovery
    print(f"🔍 [JSON Discovery Engine] Strategy 2: Inspecting HTML at {target_url}...")
    try:
        req = urllib.request.Request(target_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8")
            
        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script"):
            src = script.get("src", "")
            if src.endswith(".json") and "roadmap" in src:
                full_url = urllib.parse.urljoin(target_url, src)
                try:
                    r = urllib.request.Request(full_url, headers=headers)
                    with urllib.request.urlopen(r) as res:
                        content = res.read()
                        obj = json.loads(content.decode("utf-8"))
                        if "nodes" in obj:
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            dest_path.write_bytes(content)
                            print(f"✅ Discovered JSON from script src: {full_url}")
                            return True
                except Exception:
                    pass
            
            stext = script.string or ""
            if "nodes" in stext and "edges" in stext:
                m = re.search(r"(\{\"_id\":.*\"nodes\":\[.*\]\})", stext)
                if m:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    dest_path.write_text(m.group(1), encoding="utf-8")
                    print(f"✅ Discovered embedded script JSON for '{slug}'")
                    return True
    except Exception as e:
        print(f"⚠️ Strategy 2 failed: {e}")

    return False

def extract_roadmap_from_json(json_path: Path) -> list[dict]:
    """Extract structured topics, subtopics, and exact graph edges from a single roadmap.sh JSON payload."""
    if not json_path.exists():
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = {n["id"]: n for n in data.get("nodes", [])}
    edges = data.get("edges", [])

    node_labels = {}
    for nid, n in nodes.items():
        data_obj = n.get("data", {})
        label = data_obj.get("label") or n.get("label") or f"[{n.get('type', '')}]"
        node_labels[nid] = label

    # Build adjacency parent map from edges
    parent_map = {}
    for e in edges:
        src_id = e.get("source")
        tgt_id = e.get("target")
        if src_id in nodes and tgt_id in nodes:
            src_lbl = node_labels.get(src_id, "")
            tgt_lbl = node_labels.get(tgt_id, "")
            if src_lbl and tgt_lbl:
                parent_map.setdefault(tgt_lbl, []).append(src_lbl)

    structured_topics = []
    idx = 1
    for nid, n in nodes.items():
        ntype = n.get("type", "")
        if ntype in ["topic", "subtopic", "button", "section"]:
            name = node_labels.get(nid, "").strip()
            if not name or len(name) < 2 or name.startswith("[") or "Continue Learning" in name:
                continue
            parents = parent_map.get(name, [])
            prereq = ", ".join(parents) if parents else "ROOT (Start)"
            structured_topics.append({
                "order": idx,
                "name": name,
                "type": ntype.upper(),
                "prerequisite": prereq
            })
            idx += 1

    return structured_topics

def extract_roadmap_topics_with_sequence(html: str) -> list[dict]:
    """Extract topic names along with sequence index and prerequisite flow from SVG"""
    soup = BeautifulSoup(html, "html.parser")
    raw_topics = []
    
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
        if combined and combined not in raw_topics and len(combined) > 1:
            if not any(ign.lower() in combined.lower() for ign in ignore_texts):
                raw_topics.append(combined)
                
    structured_topics = []
    prev_name = None
    for idx, name in enumerate(raw_topics, start=1):
        item = {
            "order": idx,
            "name": name,
            "prerequisite": prev_name if prev_name else "ROOT (Start)"
        }
        structured_topics.append(item)
        prev_name = name

    return structured_topics

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

# ── 2-STEP DECISION FRAMEWORK FOR CANDIDATE EVALUATION ────────────────────────
CONCRETE_TOOL_MAP = {
    # Package Managers & Build Tools
    "pip": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    "npm": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    "yarn": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    "pnpm": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    "conda": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    "uv": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    "cargo": ("PACKAGE_MANAGEMENT", "Package & Dependency Management"),
    
    # Virtual Environments & Containers
    "virtualenv / venv": ("VIRTUAL_ENVIRONMENTS", "Virtual Environment Management"),
    "virtualenv": ("VIRTUAL_ENVIRONMENTS", "Virtual Environment Management"),
    "venv": ("VIRTUAL_ENVIRONMENTS", "Virtual Environment Management"),
    "Docker": ("CONTAINERIZATION", "Containerization & Isolation"),
    
    # IDEs & Editor Setup
    "VS Code": ("DEVELOPMENT_ENVIRONMENTS", "Integrated Development Environments (IDEs)"),
    "JupyterLab": ("DEVELOPMENT_ENVIRONMENTS", "Integrated Development Environments (IDEs)"),
    "Google Colab": ("DEVELOPMENT_ENVIRONMENTS", "Integrated Development Environments (IDEs)"),
    "IDEs": ("DEVELOPMENT_ENVIRONMENTS", "Integrated Development Environments (IDEs)"),
    "Environment Setup": ("DEVELOPMENT_ENVIRONMENTS", "Integrated Development Environments (IDEs)"),
    
    # VCS Hosting Platforms
    "GitHub": ("VCS_HOSTING", "Version Control Hosting Platforms"),
    "GitLab": ("VCS_HOSTING", "Version Control Hosting Platforms"),
    "Bitbucket": ("VCS_HOSTING", "Version Control Hosting Platforms"),
    
    # Frontend Frameworks & Libraries (Specific Tool Implementations)
    "React": ("FRONTEND_FRAMEWORKS", "Frontend UI Frameworks & Component Libraries"),
    "Vue.js": ("FRONTEND_FRAMEWORKS", "Frontend UI Frameworks & Component Libraries"),
    "Angular": ("FRONTEND_FRAMEWORKS", "Frontend UI Frameworks & Component Libraries"),
    "Svelte": ("FRONTEND_FRAMEWORKS", "Frontend UI Frameworks & Component Libraries"),
    "Solid JS": ("FRONTEND_FRAMEWORKS", "Frontend UI Frameworks & Component Libraries"),
    "Preact": ("FRONTEND_FRAMEWORKS", "Frontend UI Frameworks & Component Libraries"),
    
    # CSS Preprocessors & Frameworks
    "Tailwind CSS": ("CSS_FRAMEWORKS", "CSS Frameworks & Styling Tools"),
    "Bootstrap": ("CSS_FRAMEWORKS", "CSS Frameworks & Styling Tools"),
    "Sass": ("CSS_PREPROCESSORS", "CSS Preprocessors & Extensions"),
    "PostCSS": ("CSS_PREPROCESSORS", "CSS Preprocessors & Extensions"),
    
    # Build & Bundling Tools
    "Vite": ("MODULE_BUNDLERS", "Module Bundlers & Build Tools"),
    "Webpack": ("MODULE_BUNDLERS", "Module Bundlers & Build Tools"),
    "Rollup": ("MODULE_BUNDLERS", "Module Bundlers & Build Tools"),
    "Parcel": ("MODULE_BUNDLERS", "Module Bundlers & Build Tools"),
    "esbuild": ("MODULE_BUNDLERS", "Module Bundlers & Build Tools"),
    
    # Testing & Linting Tools
    "ESLint": ("CODE_LINTING_FORMATTING", "Code Linting & Formatting Tools"),
    "Prettier": ("CODE_LINTING_FORMATTING", "Code Linting & Formatting Tools"),
    "Jest": ("AUTOMATED_TESTING_TOOLS", "Automated Testing Frameworks & Tools"),
    "Vitest": ("AUTOMATED_TESTING_TOOLS", "Automated Testing Frameworks & Tools"),
    "Cypress": ("AUTOMATED_TESTING_TOOLS", "Automated Testing Frameworks & Tools"),
    "Playwright": ("AUTOMATED_TESTING_TOOLS", "Automated Testing Frameworks & Tools"),

    # Type Systems & TypeScript
    "TypeScript": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification"),
    "Type Checkers": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification"),
    "tsconfig.json": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification"),
    "Compiler Options": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification")
}


def evaluate_candidate_item(name: str, master_concepts: list[dict]):
    """
    Step 1: Check if item is a concrete tool -> Map to abstract parent concept as Keyword/Metadata.
    Step 2: If abstract -> Promote to Concept Proposal.
    """
    name_clean = name.strip()
    
    # Step 1: Concrete tool evaluation
    if name_clean in CONCRETE_TOOL_MAP:
        target_code, target_name = CONCRETE_TOOL_MAP[name_clean]
        # Check if abstract concept already exists in master tree
        existing = next((c for c in master_concepts if c["code"] == target_code), None)
        return {
            "type": "CONCRETE_TOOL_MAPPING",
            "item": name_clean,
            "target_concept_code": target_code,
            "target_concept_name": target_name,
            "concept_exists": existing is not None,
            "action": f"Map '{name_clean}' as Keyword under Concept '{target_code}' ({'Exists' if existing else 'Create New Abstract Concept'})"
        }
    
    # Step 2: Abstract Concept promotion & Noun Phrase Normalization
    # 2a. Clean question sentences and verbs into Noun Phrases
    cleaned_name = name_clean
    
    # Custom Abstraction & Noun Phrase Mappings
    CONCEPT_NOUN_MAP = {
        "How does the internet work?": ("INTERNET_FUNDAMENTALS", "Internet Fundamentals & Architecture"),
        "What is HTTP?": ("HTTP_PROTOCOL", "HTTP Protocol & Specification"),
        "What is Domain Name?": ("DOMAIN_NAME_SYSTEM", "Domain Name System (DNS)"),
        "What is hosting?": ("WEB_HOSTING", "Web Hosting & Infrastructure"),
        "DNS and how it works?": ("DOMAIN_NAME_SYSTEM", "Domain Name System (DNS)"),
        "Browsers and how they work?": ("WEB_BROWSER_ENGINES", "Web Browser Architecture & Engines"),
        "CSS Box Model": ("UI_BOX_MODEL_LAYOUT", "UI Box Model Layout System"),
        "Box Model": ("UI_BOX_MODEL_LAYOUT", "UI Box Model Layout System"),
        "APIs with requests": ("HTTP_API_CLIENTS", "HTTP API Clients & Requests"),
        "Introduction to TypeScript": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification"),
        "TypeScript vs JavaScript": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification"),
        "TS and JS Interoperability": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification"),
        "Installation and Configuration": ("TYPE_SYSTEMS_TYPESCRIPT", "Type Systems & TypeScript Specification")
    }

    if cleaned_name in CONCEPT_NOUN_MAP:
        proposed_code, clean_title = CONCEPT_NOUN_MAP[cleaned_name]
        return {
            "type": "ABSTRACT_CONCEPT_PROPOSAL",
            "item": name_clean,
            "proposed_code": proposed_code,
            "action": f"Promote '{name_clean}' as Noun Concept Code '{proposed_code}' ({clean_title}) to Master Tree"
        }

    # Strip question patterns: "How does...", "What is...", "how it works?", "Learn a..."
    cleaned_name = re.sub(r"^(What is|How does|How|Learn a|Learn)\s+", "", cleaned_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r"\s+and how it works\??$", "", cleaned_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r"\s+and how they work\??$", "", cleaned_name, flags=re.IGNORECASE)
    cleaned_name = cleaned_name.strip("? ")

    # Convert normalized name to UPPER_SNAKE_CASE noun code proposal
    proposed_code = re.sub(r"[^A-Za-z0-9]+", "_", cleaned_name).strip("_").upper()
    return {
        "type": "ABSTRACT_CONCEPT_PROPOSAL",
        "item": name_clean,
        "proposed_code": proposed_code,
        "action": f"Promote '{name_clean}' as Noun Concept Code '{proposed_code}' to Master Tree"
    }


def align_topics(roadmap_topics: list[dict], master_concepts: list[dict], master_topics: list[dict]):
    """Align extracted roadmap topics with existing master concepts & topics preserving sequence"""
    matched = []
    missing = []

    concept_map = {c["name"].lower(): c for c in master_concepts}
    topic_map = {t["name"].lower(): t for t in master_topics}

    for rt_obj in roadmap_topics:
        rt = rt_obj["name"]
        rt_clean = rt.lower().strip()
        
        # 1. Exact match by name
        matched_concept = concept_map.get(rt_clean)
        matched_topic = topic_map.get(rt_clean)
        
        if matched_concept:
            matched.append({
                "order": rt_obj["order"],
                "roadmap_name": rt,
                "prerequisite": rt_obj["prerequisite"],
                "match_type": "Exact (Concept)",
                "code": matched_concept["code"],
                "matched_name": matched_concept["name"]
            })
        elif matched_topic:
            matched.append({
                "order": rt_obj["order"],
                "roadmap_name": rt,
                "prerequisite": rt_obj["prerequisite"],
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
                    "order": rt_obj["order"],
                    "roadmap_name": rt,
                    "prerequisite": rt_obj["prerequisite"],
                    "match_type": f"Fuzzy ({item_type} - {int(best_score*100)}%)",
                    "code": item["code"],
                    "matched_name": item["name"]
                })
            else:
                missing.append(rt_obj)

    return matched, missing

# ── LAYER 2: SEARXNG ─────────────────────────────────────────────────────────
def verify_candidates_with_searxng(candidates: list[dict], env: dict, max_verify: int = 15) -> list[dict]:
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

    for cand_obj in candidates[:max_verify]:
        candidate = cand_obj["name"]
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
                        "order": cand_obj["order"],
                        "candidate": candidate,
                        "prerequisite": cand_obj["prerequisite"],
                        "verified": True,
                        "confidence": "High (Verified)",
                        "title": top_ref.get("title", ""),
                        "url": top_ref.get("url", ""),
                        "snippet": top_ref.get("content", "")[:150]
                    })
                else:
                    verified_results.append({
                        "order": cand_obj["order"],
                        "candidate": candidate,
                        "prerequisite": cand_obj["prerequisite"],
                        "verified": False,
                        "confidence": "SearXNG Standby",
                        "title": "N/A",
                        "url": "",
                        "snippet": "No response from search engine upstream."
                    })
        except Exception as e:
            verified_results.append({
                "order": cand_obj["order"],
                "candidate": candidate,
                "prerequisite": cand_obj["prerequisite"],
                "verified": False,
                "confidence": "Error",
                "title": "",
                "url": "",
                "snippet": str(e)
            })

    return verified_results

# ── LAYER 3: CONTEXT7 API ───────────────────────────────────────────────────
def enrich_candidates_with_context7(candidates: list[dict], env: dict, max_enrich: int = 15) -> list[dict]:
    """Fetch official library docs & descriptions using Context7 API"""
    ctx7_key = env.get("CONTEXT7_API_KEY", "")
    headers = {"User-Agent": "Mozilla/5.0"}
    if ctx7_key:
        headers["Authorization"] = f"Bearer {ctx7_key}"

    enriched = []
    print(f"📚 [Layer 3 - Context7] Extracting official docs for top {min(len(candidates), max_enrich)} candidate libraries...")

    for cand_obj in candidates[:max_enrich]:
        candidate = cand_obj["name"]
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
    target_url = "https://roadmap.sh/frontend"
    project_slug = "roadmap_sh_frontend"

    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    
    for i, arg in enumerate(sys.argv):
        if arg == "--project" and i + 1 < len(sys.argv):
            project_slug = sys.argv[i + 1]
        elif i == 2 and not arg.startswith("--"):
            project_slug = arg

    env = load_env()
    
    # Layer 1 Execution
    json_path = None
    if project_slug:
        parsed_slug = urllib.parse.urlparse(target_url).path.strip("/").split("/")[-1] or "frontend"
        dest_json = PROJECT_ROOT / "projects" / project_slug / "context" / f"{parsed_slug}.json"
        
        if not dest_json.exists():
            discover_and_download_roadmap_json(target_url, dest_json)
            
        if dest_json.exists():
            json_path = dest_json

    if json_path and json_path.exists():
        print(f"📊 [JSON Graph Engine] Parsing graph structure directly from {json_path.name}...")
        structured_topics = extract_roadmap_from_json(json_path)
    else:
        html = fetch_roadmap(target_url, env)
        structured_topics = extract_roadmap_topics_with_sequence(html)
    
    print(f"✅ Extracted {len(structured_topics)} structured topics & graph relations from {target_url}")
    
    # Save into project context if project_slug is defined
    if project_slug:
        project_context_dir = PROJECT_ROOT / "projects" / project_slug / "context"
        project_context_dir.mkdir(parents=True, exist_ok=True)
        
        raw_json_path = project_context_dir / "raw_roadmap.json"
        with open(raw_json_path, "w", encoding="utf-8") as f:
            json.dump({
                "url": target_url,
                "topics_count": len(structured_topics),
                "topics": structured_topics
            }, f, indent=2, ensure_ascii=False)
            
        syllabus_md_path = project_context_dir / "syllabus.md"
        with open(syllabus_md_path, "w", encoding="utf-8") as f:
            f.write(f"# Syllabus: {target_url}\n\n")
            f.write(f"Source URL: {target_url}\n\n")
            f.write("## Sequence & Topics Graph\n\n")
            for t in structured_topics:
                f.write(f"{t['order']}. **{t['name']}** (Prerequisite: `{t['prerequisite']}`)\n")
        print(f"📁 Saved project context files to: {project_context_dir}")

    concepts, topics, categories = parse_master_tsv(MASTER_TSV_PATH)
    print(f"📊 Master Tree loaded: {len(concepts)} concepts, {len(topics)} topics, {len(categories)} categories")
    
    matched, missing = align_topics(structured_topics, concepts, topics)
    print(f"\n🎯 ALIGNMENT RESULTS:")
    print(f"  - Matched items: {len(matched)}")
    print(f"  - Missing candidate items (Gaps): {len(missing)}")

    # Apply 2-Step Decision Framework to missing candidates
    decision_evaluated = []
    for item_obj in missing:
        eval_res = evaluate_candidate_item(item_obj["name"], concepts)
        eval_res["order"] = item_obj["order"]
        eval_res["prerequisite"] = item_obj["prerequisite"]
        decision_evaluated.append(eval_res)

    # Layer 2 Execution (SearXNG Independent Verification)
    searxng_results = verify_candidates_with_searxng(missing, env, max_verify=15)
    
    # Layer 3 Execution (Context7 Official Library Docs Enrichment)
    context7_results = enrich_candidates_with_context7(missing, env, max_enrich=15)
    
    report_path = PROJECT_ROOT / ".work" / "roadmap_alignment_report.md"
    if project_slug:
        report_path = PROJECT_ROOT / "projects" / project_slug / ".work" / "roadmap_alignment_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Tri-Layer Alignment & 2-Step Decision Framework Report\n\n")
        f.write(f"- **Target Roadmap:** {target_url}\n")
        f.write(f"- **Project Slug:** {project_slug}\n")
        f.write(f"- **Total Topics Crawled (Layer 1 - Crawl4AI):** {len(structured_topics)}\n")
        f.write(f"- **Matched with Master Tree:** {len(matched)}\n")
        f.write(f"- **Missing Candidates (Gaps):** {len(missing)}\n\n")
        
        f.write("## 🟢 Matched Topics with Sequence & Prerequisite Context\n\n")
        f.write("| Order | Roadmap Topic | Prerequisite Node (Trước) | Match Type | Master Code | Master Name |\n")
        f.write("|---|---|---|---|---|---| \n")
        for m in matched:
            f.write(f"| {m['order']} | **{m['roadmap_name']}** | `{m['prerequisite']}` | {m['match_type']} | `{m['code']}` | {m['matched_name']} |\n")
            
        f.write("\n## ⚖️ 2-Step Decision Framework: Candidate Item Classification\n\n")
        f.write("### 🛠️ 1. Concrete Tools / Technology-Specific Items (Map as Keywords to Abstract Concept)\n\n")
        f.write("| Order | Concrete Tool | Target Abstract Concept Code | Target Concept Name | Status | Action Plan |\n")
        f.write("|---|---|---|---|---|---|\n")
        tool_items = [d for d in decision_evaluated if d["type"] == "CONCRETE_TOOL_MAPPING"]
        for t in tool_items:
            status_str = "Concept Exists" if t["concept_exists"] else "Create Abstract Concept"
            f.write(f"| {t['order']} | **{t['item']}** | `{t['target_concept_code']}` | {t['target_concept_name']} | `{status_str}` | {t['action']} |\n")

        f.write("\n### 📐 2. Abstract Concepts (Promote directly to Master Tree)\n\n")
        f.write("| Order | Candidate Item | Proposed Concept Code | Action Plan |\n")
        f.write("|---|---|---|---|\n")
        abstract_items = [d for d in decision_evaluated if d["type"] == "ABSTRACT_CONCEPT_PROPOSAL"]
        for a in abstract_items[:20]:
            f.write(f"| {a['order']} | **{a['item']}** | `{a['proposed_code']}` | {a['action']} |\n")
        if len(abstract_items) > 20:
            f.write(f"| ... *and {len(abstract_items)-20} more abstract concept proposals* | | |\n")


        f.write("\n## 🔎 Layer 2: SearXNG Independent Multi-Source Verification\n\n")
        f.write("| Order | Candidate Topic | Prerequisite Node (Trước) | Status | Reference Source | Snippet / Description |\n")
        f.write("|---|---|---|---|---|---|\n")
        for v in searxng_results:
            ref_link = f"[{v['title'][:30]}]({v['url']})" if v['url'] else "N/A"
            f.write(f"| {v['order']} | **{v['candidate']}** | `{v['prerequisite']}` | `{v['confidence']}` | {ref_link} | {v['snippet']} |\n")

        f.write("\n## 📚 Layer 3: Context7 Official Library Documentation & Description\n\n")
        f.write("| Candidate Concept | Context7 Library ID | Official Description |\n")
        f.write("|---|---|---|\n")
        for c in context7_results:
            f.write(f"| **{c['candidate']}** | `{c['library_id']}` | {c['description']} |\n")

    print(f"\n📄 Tri-Layer 2-Step Decision report generated successfully at: {report_path}")

if __name__ == "__main__":
    main()

