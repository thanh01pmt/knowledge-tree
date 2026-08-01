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

load_env(Path.cwd())
url = os.environ.get("SUPABASE_URL")
service_key = os.environ.get("SERVICE_ROLE_KEY")
supabase = create_client(url, service_key)

for table in ["keywords", "keyword"]:
    try:
        res = supabase.table(table).select("*").limit(1).execute()
        print(f"✅ Table '{table}' exists!")
        if res.data:
            print("Fields:", list(res.data[0].keys()))
        else:
            print("Table is empty, but we can't get schema easily via REST without data.")
    except Exception as e:
        print(f"❌ Table '{table}' check failed (likely does not exist): {e}")

