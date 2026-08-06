#!/usr/bin/env python3
"""
STEP 3: Resolve project keywords to Master Tree concepts.

Multi-label concept resolution:
- Each keyword → top-K concepts (default K=3)
- High confidence (≥0.80) → REUSE existing concepts
- Low confidence (<0.80) → PROPOSE new concepts
- Pre-filter by field relevance from user goal

Usage:
  python scripts/resolve_concepts.py \
    --keywords keywords.json \
    --reuse-inventory reuse_inventory.json \
    --goal "Build iOS fitness tracker with SwiftUI and HealthKit" \
    --output resolved_concepts.json
"""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def load_embeddings(emb_path: Path) -> dict[str, Any]:
    """Load master_tree_embeddings.json and organize by level."""
    if not emb_path.is_file():
        print(f"[ERROR] Embeddings not found: {emb_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(emb_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    # Organize nodes by level
    organized = {
        "fields": {},
        "subjects": {},
        "categories": {},
        "topics": {},
        "concepts": {},
    }
    
    nodes = raw_data.get("nodes", [])
    for node in nodes:
        level = node.get("level", "")
        code = node.get("code", "")
        if level in organized and code:
            organized[level][code] = node
    
    print(f"[*] Loaded embeddings: {len(nodes)} nodes")
    for level, items in organized.items():
        print(f"    {level}: {len(items)} items")
    
    return organized


_ST_MODEL = None  # lazy-loaded SentenceTransformer singleton


def embed_text(text: str, client=None, model: str = "paraphrase-multilingual-MiniLM-L12-v2") -> list[float]:
    """Embed text using SentenceTransformer (must match embeddings file dim).

    Uses the same model that generated master_tree_embeddings.json
    (paraphrase-multilingual-MiniLM-L12-v2, 384-dim). Falls back to empty
    list on failure so the caller can use keyword-overlap matching.
    """
    global _ST_MODEL
    try:
        if _ST_MODEL is None:
            from sentence_transformers import SentenceTransformer
            _ST_MODEL = SentenceTransformer(model)
        emb = _ST_MODEL.encode(text, normalize_embeddings=True)
        return emb.tolist()
    except Exception as e:
        print(f"[ERROR] Embedding failed ({e}), using keyword overlap fallback", file=sys.stderr)
        return []


def keyword_overlap_score(query: str, keywords: str, description: str) -> float:
    """Calculate keyword overlap score between query and concept metadata."""
    query_terms = set(query.lower().split())
    concept_terms = set(keywords.lower().split() + description.lower().split())
    
    if not query_terms or not concept_terms:
        return 0.0
    
    overlap = query_terms & concept_terms
    score = len(overlap) / len(query_terms)
    return min(score, 1.0)
def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def infer_fields_from_goal(goal: str) -> list[str]:
    """Infer relevant field codes from user goal using keyword matching."""
    goal_lower = goal.lower()
    
    # Keyword → field mapping
    field_keywords = {
        "ASE": ["algorithm", "software", "programming", "code", "develop", "build", "app", "application"],
        "DAI": ["data", "database", "storage", "query", "sql", "analytics", "statistics"],
        "CSN": ["network", "protocol", "server", "client", "api", "http", "tcp", "ip"],
        "HCI": ["user", "interface", "ui", "ux", "interaction", "accessibility", "design"],
        "SEF": ["security", "encryption", "authentication", "authorization", "privacy"],
        "MTH": ["math", "calculus", "linear algebra", "probability", "statistics"],
        "SYS": ["system", "os", "operating", "kernel", "process", "thread", "memory"],
        "ART": ["ai", "artificial intelligence", "machine learning", "ml", "neural", "deep learning"],
        "GAM": ["game", "graphics", "rendering", "3d", "2d", "animation", "physics"],
        "WEB": ["web", "html", "css", "javascript", "react", "vue", "frontend", "backend"],
        "MOB": ["mobile", "ios", "android", "swift", "kotlin", "flutter", "react native"],
        "DEV": ["devops", "ci/cd", "docker", "kubernetes", "deployment", "monitoring"],
    }
    
    matched_fields = []
    for field_code, keywords in field_keywords.items():
        if any(kw in goal_lower for kw in keywords):
            matched_fields.append(field_code)
    
    # Default to ASE if nothing matched
    if not matched_fields:
        matched_fields = ["ASE"]
    
    return matched_fields


def search_concepts(
    query_emb: list[float],
    query_text: str,
    embeddings: dict,
    top_k: int = 5,
    threshold: float = 0.0,
) -> list[dict]:
    """Search concepts using cosine similarity or keyword overlap fallback."""
    items = embeddings.get("concepts", {})
    scored = []
    
    # Determine search mode
    use_embedding = bool(query_emb)
    
    for code, data in items.items():
        if use_embedding:
            emb = data.get("embedding", [])
            if not emb:
                continue
            score = cosine_similarity(query_emb, emb)
        else:
            # Fallback to keyword overlap
            keywords = data.get("keywords", "")
            description = data.get("description", "")
            score = keyword_overlap_score(query_text, keywords, description)
        
        if score >= threshold:
            scored.append({
                "code": code,
                "name": data.get("name", code),
                "description": data.get("description", ""),
                "keywords": data.get("keywords", ""),
                "score": round(score, 4),
                "method": "embedding" if use_embedding else "keyword_overlap",
            })
    scored.sort(key=lambda x: -x["score"])
    return scored[:top_k]


def resolve_concepts(
    keywords: list[dict],
    reuse_inventory: dict,
    goal: str,
    embeddings: dict,
    client,
    top_k: int = 3,
    threshold: float = 0.55,
) -> dict:
    """Resolve keywords to concepts with multi-label matching."""
    
    master_tree = reuse_inventory.get("master_tree", {})
    concepts = master_tree.get("concepts", {})
    
    # Infer relevant fields from goal
    relevant_fields = infer_fields_from_goal(goal)
    print(f"[*] Inferred relevant fields: {relevant_fields}")
    
    resolved = []
    proposed = []
    
    for kw_data in keywords:
        keyword = kw_data.get("keyword", "")
        source = kw_data.get("source", "unknown")
        
        print(f"[*] Resolving: '{keyword}' (from {source})...")
        
        # Try embedding, fallback to keyword overlap if fails
        query_emb = embed_text(keyword, client)
        if not query_emb:
            print(f"    [!] Embedding failed, using keyword overlap fallback")
        
        # Search concepts (auto-fallback if query_emb is empty)
        matches = search_concepts(query_emb, keyword, embeddings, top_k=top_k, threshold=0.0)
        
        if not matches:
            print(f"    [!] No matches found")
            proposed.append({
                "keyword": keyword,
                "source": source,
                "reason": "No matches in Master Tree",
            })
            continue
        
        # Filter by field relevance
        field_filtered = []
        for match in matches:
            code = match["code"]
            concept_data = concepts.get(code, {})
            concept_fields = concept_data.get("field_codes", "")
            
            # Check if any relevant field matches
            if any(f in concept_fields for f in relevant_fields):
                field_filtered.append(match)
        
        if not field_filtered:
            # If no field match, use top match anyway
            field_filtered = matches[:1]
        
        # Check confidence threshold
        top_match = field_filtered[0]
        if top_match["score"] >= threshold:
            # High confidence → REUSE
            resolved.append({
                "keyword": keyword,
                "source": source,
                "concept_codes": [m["code"] for m in field_filtered if m["score"] >= threshold],
                "matches": field_filtered,
            })
            print(f"    ✓ REUSE: {[m['code'] for m in field_filtered if m['score'] >= threshold]}")
        else:
            # Low confidence → PROPOSE
            proposed.append({
                "keyword": keyword,
                "source": source,
                "best_match": top_match,
                "reason": f"Low confidence ({top_match['score']:.2f} < {threshold})",
            })
            print(f"    ? PROPOSE: best match {top_match['code']} ({top_match['score']:.2f})")
    
    return {
        "resolved": resolved,
        "proposed": proposed,
        "summary": {
            "total_keywords": len(keywords),
            "resolved_count": len(resolved),
            "proposed_count": len(proposed),
            "threshold": threshold,
            "relevant_fields": relevant_fields,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="STEP 3: Resolve keywords to Master Tree concepts")
    parser.add_argument("--keywords", required=True, help="Input keywords JSON from STEP 1-2")
    parser.add_argument("--reuse-inventory", required=True, help="Reuse inventory JSON from STEP 0")
    parser.add_argument("--goal", required=True, help="User goal/learning objective")
    parser.add_argument("--top-k", type=int, default=3, help="Max concepts per keyword (default: 3)")
    parser.add_argument("--threshold", type=float, default=0.55,
                       help="Confidence threshold for REUSE. Default 0.55 tuned for "
                            "paraphrase-multilingual-MiniLM-L12-v2 (higher for OpenAI "
                            "text-embedding-3-small)")
    parser.add_argument("--embeddings", help="Path to master_tree_embeddings.json (default: auto-detect)")
    parser.add_argument("--output", required=True, help="Output resolved concepts JSON")
    args = parser.parse_args()
    
    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)
    
    # Load inputs
    with open(args.keywords, "r", encoding="utf-8") as f:
        keywords_data = json.load(f)
    
    with open(args.reuse_inventory, "r", encoding="utf-8") as f:
        reuse_inventory = json.load(f)
    
    # Load embeddings
    if args.embeddings:
        emb_path = Path(args.embeddings)
    else:
        emb_path = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree_embeddings.json"
    
    embeddings = load_embeddings(emb_path)
    
    # Setup embedding engine (SentenceTransformer matches embeddings file dim)
    # client param kept for signature compatibility; embed_text uses ST model.
    client = None
    
    # Extract keywords list
    keywords_list = keywords_data.get("keywords", [])
    print(f"\n[*] Resolving {len(keywords_list)} keywords...")
    
    # Resolve concepts
    result = resolve_concepts(
        keywords=keywords_list,
        reuse_inventory=reuse_inventory,
        goal=args.goal,
        embeddings=embeddings,
        client=client,
        top_k=args.top_k,
        threshold=args.threshold,
    )
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n[✓] Resolved concepts → {output_path}")
    print(f"    Resolved: {result['summary']['resolved_count']}")
    print(f"    Proposed: {result['summary']['proposed_count']}")


if __name__ == "__main__":
    main()
