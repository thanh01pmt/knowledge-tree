import os
import sys
from pathlib import Path
from supabase import create_client

def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

repo_root = Path.cwd()
for _ in range(5):
    if (repo_root / ".agents").is_dir():
        break
    repo_root = repo_root.parent
load_env(repo_root)

url = os.environ.get("SUPABASE_URL")
service_key = os.environ.get("SERVICE_ROLE_KEY")
supabase = create_client(url, service_key)

tables = [
    "activities", "activity",
    "activity_learning_objectives", "lesson_activities"
]

for table in tables:
    try:
        res = supabase.table(table).select("*").limit(1).execute()
        if res.data:
            cols = list(res.data[0].keys())
            print(f"✅ Table '{table}' exists. Columns ({len(cols)}):")
            print("  " + ", ".join(cols))
        else:
            print(f"✅ Table '{table}' exists but is EMPTY.")
    except Exception as e:
        print(f"❌ Table '{table}' DOES NOT EXIST: {e}")

