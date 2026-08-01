#!/usr/bin/env python3
"""
semantic_search_master.py — Semantic search against Master Tree using embeddings.

Uses pre-computed master_tree_embeddings.json for fast cosine similarity search.
Returns top-k matches per Master Tree level (concepts, topics, categories).

Usage:
  python3 semantic_search_master.py --query "Use for-in loops to iterate over arrays"
  python3 semantic_search_master.py --query "Variables and constants" --top-k 10 --level concepts

Integration:
  Agent /map-taxonomy calls this script for each syllabus item.
  Results provide evidence-based matching scores instead of guesswork.
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
    """Load master_tree_embeddings.json."""
    if not emb_path.is_file():
        print(f"[ERROR] Embeddings not found: {emb_path}", file=sys.stderr)
        sys.exit(1)
    with open(emb_path, "r", encoding="utf-8") as f:
        return json.load(f)


def embed_text(text: str, client, model: str = "text-embedding-3-small") -> list[float]:
    """Embed text using OpenAI-compatible API."""
    try:
        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}", file=sys.stderr)
        return []


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


def search_level(
    query_emb: list[float],
    embeddings: dict,
    level: str,
    top_k: int = 5,
    threshold: float = 0.0,
) -> list[dict]:
    """Search within a single Master Tree level."""
    items = embeddings.get(level, {})
    scored = []
    for code, data in items.items():
        emb = data.get("embedding", [])
        if not emb:
            continue
        score = cosine_similarity(query_emb, emb)
        if score >= threshold:
            scored.append({
                "code": code,
                "name": data.get("name", code),
                "score": round(score, 4),
            })
    scored.sort(key=lambda x: -x["score"])
    return scored[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Semantic search against Master Tree")
    parser.add_argument("--query", required=True, help="Search query (syllabus item, concept name, etc.)")
    parser.add_argument("--top-k", type=int, default=5, help="Max results per level")
    parser.add_argument("--threshold", type=float, default=0.0, help="Minimum similarity threshold")
    parser.add_argument("--level", choices=["concepts", "topics", "categories", "all"], default="all",
                        help="Master Tree level to search (default: all)")
    parser.add_argument("--embeddings", help="Path to master_tree_embeddings.json (default: auto-detect)")
    parser.add_argument("--output", help="Output path for search results JSON")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)

    # Resolve embeddings path
    if args.embeddings:
        emb_path = Path(args.embeddings)
    else:
        emb_path = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree_embeddings.json"
    
    print(f"[*] Loading embeddings from {emb_path}...")
    embeddings = load_embeddings(emb_path)
    print(f"    concepts: {len(embeddings.get('concepts', {}))}")
    print(f"    topics: {len(embeddings.get('topics', {}))}")
    print(f"    categories: {len(embeddings.get('categories', {}))}")

    # Embed query
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    from openai import OpenAI
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    
    print(f"[*] Embedding query: '{args.query[:60]}...'")
    query_emb = embed_text(args.query, client)
    if not query_emb:
        sys.exit(1)

    # Search
    levels_to_search = ["concepts", "topics", "categories"] if args.level == "all" else [args.level]
    
    results = {}
    for level in levels_to_search:
        matches = search_level(query_emb, embeddings, level, args.top_k, args.threshold)
        results[level] = matches
        print(f"\n  {level.upper()} (top {args.top_k}):")
        for m in matches:
            print(f"    {m['code']:45s} {m['score']:.4f}  {m['name'][:50]}")

    # Output
    output = {
        "query": args.query,
        "results": results,
    }
    
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"\n[✓] Results → {out_path}")
    
    # Return JSON to stdout for agent consumption
    print("\n---JSON---")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
