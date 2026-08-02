#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
from pathlib import Path

def main():
    print(f"[{datetime.datetime.now()}] Starting Auto-Heal Cron...")
    
    validate_script = Path(".agents/skills/tree-validator/scripts/validate_master_tree.py")
    
    try:
        result = subprocess.run(
            [sys.executable, str(validate_script)], 
            capture_output=True, text=True, check=True
        )
        print("✅ Master Tree is healthy. No anomalies found.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Master Tree validation failed. Anomalies detected!")
        print("--- ERROR LOG ---")
        print(e.stdout)
        print(e.stderr)
        print("-----------------")
        print("👉 Next steps: Initiating Auto-Heal Protocol...")
        auto_heal_script = Path(".agents/skills/tree-validator/scripts/llm_auto_heal_master_tree.py")
        try:
            subprocess.run([sys.executable, str(auto_heal_script)], check=True)
            print("✅ Auto-Heal Protocol completed successfully.")
        except subprocess.CalledProcessError:
            print("❌ Auto-Heal Protocol failed to resolve all issues.")
            sys.exit(1)

if __name__ == "__main__":
    main()
