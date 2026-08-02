#!/usr/bin/env python3
"""
cron_trend_research.py — Trend Research Cron (Updated)

This cron now delegates to the full auto_stem_discovery.py implementation
which manages a priority research queue with Foundation×Velocity×Fit scoring.
After updating the queue, it runs CS2023 crosswalk for top trend topics.
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

def main():
    print(f"[{datetime.datetime.now()}] Starting Trend Research Cron (delegating to auto_stem_discovery.py)...")

    # Run the full trend discovery with queue management
    discovery_script = Path(".agents/skills/knowledge-researcher/scripts/auto_stem_discovery.py")
    
    if not discovery_script.exists():
        print(f"❌ auto_stem_discovery.py not found at {discovery_script}")
        sys.exit(1)

    # Run with --deep to execute all trend queries
    cmd = [sys.executable, str(discovery_script), "--deep", "--out-dir", ".work"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=str(Path.cwd()))
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("❌ auto_stem_discovery.py timed out")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to run auto_stem_discovery.py: {e}")
        sys.exit(1)

    # After queue update, run CS2023 crosswalk for top 3 topics
    print(f"\n[*] Running CS2023 crosswalk for top 3 trend topics...")
    crosswalk_script = Path(".agents/skills/knowledge-researcher/scripts/curriculum_crosswalk.py")
    work_dir = Path(".work")
    queue_file = work_dir / "research_queue.json"
    
    if crosswalk_script.exists() and queue_file.exists():
        import json
        try:
            queue = json.loads(queue_file.read_text(encoding="utf-8"))
            for item in queue[:3]:
                topic = item['topic']
                print(f"    Crosswalking: {topic}")
                safe_slug = topic.lower().replace(" ", "-").replace("/", "-")[:50]
                out_dir = work_dir / "crosswalk" / safe_slug
                out_dir.mkdir(parents=True, exist_ok=True)
                
                try:
                    subprocess.run([
                        sys.executable, str(crosswalk_script),
                        "--reference", "ACM_CS2023",
                        "--compare", "NGSS", "CSTA", "UNESCO_ICT", "OECD_PISA",
                        "--out-dir", str(out_dir)
                    ], check=False, timeout=300, cwd=str(Path.cwd()))
                except subprocess.TimeoutExpired:
                    print(f"    ⚠️ Crosswalk timeout for {topic}")
                except Exception as e:
                    print(f"    ⚠️ Crosswalk error for {topic}: {e}")
        except Exception as e:
            print(f"    ⚠️ Failed to load queue for crosswalk: {e}")
    else:
        print(f"    ⚠️ Crosswalk script or queue not found, skipping")

if __name__ == "__main__":
    main()
