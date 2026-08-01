#!/usr/bin/env python3
"""
auto_stem_discovery.py — Tier 2: Trend Watcher

This script performs periodic scans for emerging trends in STEM education
that are not present in the Master Knowledge Tree. It manages a priority queue
of research topics.
"""

import os
import sys
import json
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Tier 2: STEM Trend Discovery")
    parser.add_argument("--query", default="emerging technologies in STEM education", help="Broad query to search for trends")
    parser.add_argument("--out-dir", default=".work", help="Output directory for queue")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    queue_file = os.path.join(args.out_dir, "research_queue.json")

    print(f"[*] Starting Trend Watcher with query: '{args.query}'")
    print("[*] (Simulation) Calling Exa / last30days APIs...")
    print("[*] (Simulation) Found new topic: 'Quantum Machine Learning in Education'")
    
    # Load existing queue
    queue = []
    if os.path.exists(queue_file):
        with open(queue_file, "r", encoding="utf-8") as f:
            queue = json.load(f)
            
    # Add new item if not exists
    topic = "Quantum Machine Learning"
    if not any(item["topic"] == topic for item in queue):
        queue.append({
            "topic": topic,
            "foundation_score": 6,
            "trend_velocity": 9,
            "educational_fit": 5,
            "priority_score": (6 * 0.5) + (9 * 0.3) + (5 * 0.2),
            "status": "pending",
            "discovered_at": datetime.now().isoformat()
        })
        
    # Sort queue by priority descending
    queue.sort(key=lambda x: x["priority_score"], reverse=True)
    
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

    print(f"[+] Trend Watcher complete. Queue updated: {queue_file}")
    if queue:
        top_topic = queue[0]
        print(f"[!] Top priority topic: {top_topic['topic']} (Score: {top_topic['priority_score']:.1f})")
        print(f"    Run `/research-trend '{top_topic['topic']}'` to execute.")

if __name__ == "__main__":
    main()
