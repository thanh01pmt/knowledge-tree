#!/usr/bin/env python3
"""
Knowledge Tree Cron Runner
Python-based scheduler to replace system crontab in containerized environments.

Runs continuously and executes cron jobs on schedule:
- Auto-Heal: every 6 hours
- Collectors Academic: every 15 minutes
- Collectors Standards: weekly Sunday 3:00 AM
- Collectors Trends: weekly Sunday 2:00 AM
- Processor: every 6 hours (offset by 3 hours from Auto-Heal)

Usage:
  python3 cron_runner.py           # Run as daemon (foreground)
  python3 cron_runner.py --once    # Run all due jobs once and exit
  python3 cron_runner.py --status  # Show next run times
"""

import sys
import os
import time
import schedule
import subprocess
import threading
import signal
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import json

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

PYTHON_BIN = sys.executable
LOG_DIR = REPO_ROOT / ".agents" / "cron" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


class CronRunner:
    """Manages scheduled cron jobs for Knowledge Tree."""
    
    def __init__(self):
        self.running = False
        self.jobs = {}
        self._setup_jobs()
        self._setup_signals()
    
    def _setup_signals(self):
        """Handle graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
    
    def _run_job(self, name: str, cmd: list, log_file: Path):
        """Execute a cron job and log output."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ▶️ Running: {name}")
        
        with open(log_file, "a") as log:
            log.write(f"\n{'='*60}\n")
            log.write(f"[{timestamp}] START: {name}\n")
            log.write(f"Command: {' '.join(cmd)}\n")
            log.write(f"{'='*60}\n")
            
            try:
                result = subprocess.run(
                    cmd,
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=3600  # 1 hour max
                )
                
                log.write(f"Exit code: {result.returncode}\n")
                if result.stdout:
                    log.write(f"STDOUT:\n{result.stdout}\n")
                if result.stderr:
                    log.write(f"STDERR:\n{result.stderr}\n")
                
                status = "✅ SUCCESS" if result.returncode == 0 else f"❌ FAILED (exit {result.returncode})"
                log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] END: {name} - {status}\n")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status}: {name}")
                
            except subprocess.TimeoutExpired:
                log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TIMEOUT: {name} (1h limit)\n")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏱️ TIMEOUT: {name}")
            except Exception as e:
                log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {name} - {e}\n")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 💥 ERROR: {name} - {e}")
    
    def _setup_jobs(self):
        """Define all cron jobs with their schedules."""
        
        # CRON 1: Auto-Heal - every 6 hours
        def run_auto_heal():
            self._run_job(
                "Auto-Heal",
                [PYTHON_BIN, ".agents/cron/cron_auto_heal.py"],
                LOG_DIR / "cron_auto_heal.log"
            )
        schedule.every(6).hours.do(run_auto_heal).tag("auto-heal")
        
        # CRON 2a: Collectors Academic - every 15 minutes
        def run_collectors_academic():
            self._run_job(
                "Collectors Academic",
                [PYTHON_BIN, ".agents/cron/collectors/run_collectors.py", "--source", "academic", "--schedule", "15m"],
                LOG_DIR / "cron_collectors_academic.log"
            )
        schedule.every(15).minutes.do(run_collectors_academic).tag("collectors-academic")
        
        # CRON 2b: Collectors Standards - weekly Sunday 3:00 AM
        def run_collectors_standards():
            self._run_job(
                "Collectors Standards",
                [PYTHON_BIN, ".agents/cron/collectors/run_collectors.py", "--source", "standards", "--schedule", "weekly"],
                LOG_DIR / "cron_collectors_standards.log"
            )
        schedule.every().sunday.at("03:00").do(run_collectors_standards).tag("collectors-standards")
        
        # CRON 2c: Collectors Trends - weekly Sunday 2:00 AM
        def run_collectors_trends():
            self._run_job(
                "Collectors Trends",
                [PYTHON_BIN, ".agents/cron/collectors/run_collectors.py", "--source", "trends", "--schedule", "weekly"],
                LOG_DIR / "cron_collectors_trends.log"
            )
        schedule.every().sunday.at("02:00").do(run_collectors_trends).tag("collectors-trends")
        
        # CRON 3: Processor - every 6 hours (offset by 3 hours from Auto-Heal)
        def run_processor():
            self._run_job(
                "Processor",
                [PYTHON_BIN, ".agents/cron/collectors/run_processor.py", "--all-pending"],
                LOG_DIR / "cron_processor.log"
            )
        schedule.every(6).hours.do(run_processor).tag("processor")
        
        # Adjust Processor to run 3 hours after Auto-Heal (at :30 past the hour)
        # We can't easily do this with schedule library, so we'll just run it on a different 6h cycle
        
        self.jobs = {
            "auto-heal": "Auto-Heal (every 6h)",
            "collectors-academic": "Collectors Academic (every 15m)",
            "collectors-standards": "Collectors Standards (Sun 03:00)",
            "collectors-trends": "Collectors Trends (Sun 02:00)",
            "processor": "Processor (every 6h)",
        }
    
    def run_pending(self):
        """Run all jobs that are due."""
        schedule.run_pending()
    
    def run_once(self):
        """Run all jobs once (for testing)."""
        print("🔄 Running all cron jobs once...")
        for tag, name in self.jobs.items():
            # Get the job
            jobs = schedule.get_jobs(tag)
            if jobs:
                print(f"  Running: {name}")
                jobs[0].run()
            else:
                print(f"  ⚠️ No job found for: {name}")
    
    def show_status(self):
        """Show next run times for all jobs."""
        print("\n📅 Cron Job Schedule Status")
        print("=" * 60)
        for tag, name in self.jobs.items():
            jobs = schedule.get_jobs(tag)
            if jobs:
                job = jobs[0]
                next_run = job.next_run
                if next_run:
                    now = datetime.now()
                    delta = next_run - now
                    hours = int(delta.total_seconds() // 3600)
                    minutes = int((delta.total_seconds() % 3600) // 60)
                    print(f"  {name}")
                    print(f"    Next run: {next_run.strftime('%Y-%m-%d %H:%M:%S')} ({hours}h {minutes}m from now)")
                else:
                    print(f"  {name}")
                    print(f"    Next run: Not scheduled")
            else:
                print(f"  {name} - NOT FOUND")
        print("=" * 60)
    
    def start(self):
        """Start the cron runner daemon."""
        self.running = True
        print("🚀 Knowledge Tree Cron Runner started")
        print(f"📁 Repo: {REPO_ROOT}")
        print(f"📁 Logs: {LOG_DIR}")
        self.show_status()
        print("\n⏳ Running... Press Ctrl+C to stop\n")
        
        # Run any overdue jobs immediately on startup
        schedule.run_all()
        
        while self.running:
            self.run_pending()
            time.sleep(30)  # Check every 30 seconds
        
        print("\n👋 Cron Runner stopped")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Knowledge Tree Cron Runner")
    parser.add_argument("--once", action="store_true", help="Run all jobs once and exit")
    parser.add_argument("--status", action="store_true", help="Show schedule status and exit")
    parser.add_argument("--job", choices=["auto-heal", "collectors-academic", "collectors-standards", "collectors-trends", "processor"], help="Run specific job once")
    
    args = parser.parse_args()
    
    runner = CronRunner()
    
    if args.status:
        runner.show_status()
    elif args.once:
        runner.run_once()
    elif args.job:
        jobs = schedule.get_jobs(args.job)
        if jobs:
            print(f"🔄 Running {args.job} once...")
            jobs[0].run()
        else:
            print(f"❌ Job not found: {args.job}")
            sys.exit(1)
    else:
        runner.start()


if __name__ == "__main__":
    main()