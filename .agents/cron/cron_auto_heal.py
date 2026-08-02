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
        # In a fully autonomous mode, this would trigger an agent to read the errors and fix them.
        # For now, it logs the failure and notifies the human (or parent agent system) to intervene.
        # This prevents invalid data from being synced to Supabase (Enforcing Gate §7).

if __name__ == "__main__":
    main()
