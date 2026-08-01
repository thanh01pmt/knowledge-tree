#!/usr/bin/env python3
"""
detect_master_gaps.py — Detect syllabus domains missing from Master Tree.

For each unmapped syllabus domain, semantic search the entire Master Tree.
If top-3 similarity < threshold, propose new Category or Topic node.

Usage:
  python3 detect_master_gaps.py --project <slug>
  python3 detect_master_gaps.py --hints structured_hints.json --master master_tree.json

Integration:
  Runs after /build-tree (optional).
  Output: master_gap_report.md — list of domains not covered by Master Tree.
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


def load_json(path: Path) -> dict:
    if not path.is_file():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def embed_text(text: str, client, model: str = "text-embedding-3-small") -> list[float]:
    try:
        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}", file=sys.stderr)
        return []


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def extract_domains_from_hints(hints: dict) -> list[dict]:
    """Extract unmapped domains from structured_hints.json hierarchy."""
    domains = []
    
    def walk(nodes: list[dict], parent_level: str = "root"):
        for node in nodes:
            level = node.get("assigned_level", "concept")
            text = node.get("text", "")
            confidence = node.get("confidence", 0.5)
            children = node.get("children", [])
            
            # Only consider Category/Topic level nodes as potential gaps
            if level in ("category", "topic") and confidence >= 0.6:
                domains.append({
                    "text": text,
                    "level": level,
                    "confidence": confidence,
                    "reasoning": node.get("reasoning", ""),
                    "child_count": len(children),
                })
            
            walk(children, level)
    
    walk(hints.get("hierarchy", []))
    return domains


def search_master(domain_text: str, embeddings: dict, client, top_k: int = 3) -> list[dict]:
    """Search Master Tree for a domain. Returns top matches."""
    query_emb = embed_text(domain_text, client)
    if not query_emb:
        return []
    
    results = []
    for level in ["concepts", "topics", "categories"]:
        items = embeddings.get(level, {})
        scored = []
        for code, data in items.items():
            emb = data.get("embedding", [])
            if not emb:
                continue
            score = cosine_similarity(query_emb, emb)
            scored.append({
                "code": code,
                "name": data.get("name", code),
                "level": level,
                "score": round(score, 4),
            })
        scored.sort(key=lambda x: -x["score"])
        results.extend(scored[:top_k])
    
    results.sort(key=lambda x: -x["score"])
    return results[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Detect Master Tree gaps from syllabus domains")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--hints", help="Path to structured_hints.json")
    parser.add_argument("--master", help="Path to master_tree.json")
    parser.add_argument("--embeddings", help="Path to master_tree_embeddings.json")
    parser.add_argument("--threshold", type=float, default=0.60,
                        help="Similarity threshold for gap detection (default: 0.60)")
    parser.add_argument("--output", help="Output path for gap report")
    args = parser.parse_args()
    
    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)
    
    # Resolve paths
    if args.hints:
        hints_path = Path(args.hints)
    elif args.project:
        hints_path = repo_root / "projects" / args.project / ".work" / "structured_hints.json"
    else:
        print("[ERROR] --project or --hints required", file=sys.stderr)
        sys.exit(1)
    
    if args.embeddings:
        emb_path = Path(args.embeddings)
    else:
        emb_path = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree_embeddings.json"
    
    if args.master:
        master_path = Path(args.master)
    else:
        master_path = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree.json"
    
    # Load data
    print(f"[*] Loading hints from {hints_path}...")
    hints = load_json(hints_path)
    
    print(f"[*] Loading embeddings from {emb_path}...")
    embeddings = load_json(emb_path)
    
    master = load_json(master_path)
    
    # Extract domains from hints
    domains = extract_domains_from_hints(hints)
    print(f"[*] Found {len(domains)} domains to check")
    
    # Embed and search
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    from openai import OpenAI
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    
    gaps = []
    covered = []
    
    for domain in domains:
        text = domain["text"]
        matches = search_master(text, embeddings, client)
        
        if matches and matches[0]["score"] >= args.threshold:
            covered.append({"domain": text, "best_match": matches[0]})
        else:
            gaps.append({
                "domain": text,
                "level": domain["level"],
                "confidence": domain["confidence"],
                "reasoning": domain["reasoning"],
                "best_matches": matches,
            })
    
    # Generate report
    report_lines = [
        "# Master Tree Gap Detection Report",
        f"\n_Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        f"**Threshold:** {args.threshold}\n",
        f"**Domains checked:** {len(domains)}\n",
        f"**Covered:** {len(covered)} | **Gaps:** {len(gaps)}\n",
        "---\n",
    ]
    
    if gaps:
        report_lines.append("## 🚩 Gaps — Domains Missing from Master Tree\n")
        for g in gaps:
            report_lines.append(f"### {g['domain']}")
            report_lines.append(f"- **Suggested level:** {g['level']}")
            report_lines.append(f"- **Confidence:** {g['confidence']}")
            report_lines.append(f"- **Reasoning:** {g['reasoning']}")
            if g['best_matches']:
                report_lines.append(f"- **Best Master Tree match:** {g['best_matches'][0]['code']} (score: {g['best_matches'][0]['score']})")
                report_lines.append(f"  → Below threshold ({args.threshold}) — consider [NEW NODE PROPOSAL]")
            else:
                report_lines.append(f"  → No match found — strong candidate for [NEW NODE PROPOSAL]")
            report_lines.append("")
    
    if covered:
        report_lines.append("## ✅ Covered — Domains Found in Master Tree\n")
        report_lines.append("| Domain | Best Match | Score |")
        report_lines.append("|--------|-----------|-------|")
        for c in covered:
            report_lines.append(f"| {c['domain']} | `{c['best_match']['code']}` | {c['best_match']['score']} |")
        report_lines.append("")
    
    report_lines.append("---\n")
    report_lines.append("### Recommendations\n")
    
    if gaps:
        report_lines.append(f"- {len(gaps)} gap(s) detected. Review each and create [NEW NODE PROPOSAL] in mapping-plan.md.")
        report_lines.append("- Consider adding new Categories or Topics to Master Tree via /crawl-roadmap workflow.")
    else:
        report_lines.append("- No gaps detected. Master Tree coverage is adequate for this syllabus.")
    
    report = "\n".join(report_lines)
    
    # Write output
    if args.output:
        out_path = Path(args.output)
    elif args.project:
        out_path = repo_root / "projects" / args.project / ".work" / "master_gap_report.md"
    else:
        out_path = Path("master_gap_report.md")
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    
    print(f"\n[✓] Gap report → {out_path}")
    print(f"    Covered: {len(covered)} | Gaps: {len(gaps)}")
    
    # Print gaps to stdout
    if gaps:
        print(f"\n{'='*60}")
        print(f"GAPS DETECTED ({len(gaps)})")
        print(f"{'='*60}")
        for g in gaps:
            print(f"  🚩 {g['domain']} (suggested: {g['level']})")
            if g['best_matches']:
                print(f"     Closest: {g['best_matches'][0]['code']} ({g['best_matches'][0]['score']})")


if __name__ == "__main__":
    main()
