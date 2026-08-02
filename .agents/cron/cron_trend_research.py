#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
from pathlib import Path
import re
import json

SEED_SCOPES = [
    "AI Agent Frameworks",
    "Frontend UI Libraries",
    "Cloud Native Deployment",
    "LLM Orchestration",
    "Serverless Databases"
]

STATE_FILE = Path(".agents/cron/.trend_state.json")
PROJECTS_DIR = Path("projects")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def get_next_topic():
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        last_idx = state.get("last_index", -1)
    else:
        last_idx = -1
        
    next_idx = (last_idx + 1) % len(SEED_SCOPES)
    topic = SEED_SCOPES[next_idx]
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_index": next_idx, "last_topic": topic}, f)
        
    return topic

def main():
    topic = get_next_topic()
    print(f"[{datetime.datetime.now()}] Starting Trend Research Cron for topic: {topic}")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    base_slug = slugify(topic)
    project_slug = f"trend-{base_slug}-{timestamp}"
    
    print(f"Scaffolding project: {project_slug}")
    scaffold_script = Path(".agents/skills/tree-validator/scripts/scaffold_tree.py")
    subprocess.run([sys.executable, str(scaffold_script), project_slug], check=True)
    
    context_dir = PROJECTS_DIR / project_slug / "context"
    report_path = context_dir / "trend_report.md"
    
    print(f"Running last30days for topic: '{topic}'...")
    # Using keyless for safety in automated environments.
    last30days_cmd = [
        sys.executable,
        ".agents/skills/last30days/scripts/last30days.py",
        topic,
        "--web-backend", "keyless",
        "--days", "30",
        "--emit", "md",
        "--output", str(report_path)
    ]
    
    try:
        # We run it and let it output to the report path
        subprocess.run(last30days_cmd, check=True)
        print(f"✅ Success! Trend report generated at {report_path}")
        print(f"👉 Next steps: User must run `/set-project {project_slug}` then `/run-pipeline` to filter and extract standard concepts.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run last30days: {e}")

if __name__ == "__main__":
    main()
