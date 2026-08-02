#!/usr/bin/env python3
"""
Run Collectors - Phase 1 Entry Point
Multi-schedule entry point for all collectors.

Usage:
  python run_collectors.py --all                    # Run all collectors
  python run_collectors.py --source academic        # Run academic only
  python run_collectors.py --source standards       # Run standards only
  python run_collectors.py --source trends          # Run trends only
  python run_collectors.py --schedule 6h            # Run with 6h schedule filter
"""

import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_collector import ResearchSource, discover_pending_items
from academic_collector import AcademicCollector
from standards_collector import StandardsCollector
from trend_collector import TrendCollector


def get_collector(source: ResearchSource, repo_root: Path):
    """Get collector instance by source"""
    collectors = {
        ResearchSource.ACADEMIC: AcademicCollector,
        ResearchSource.STANDARDS: StandardsCollector,
        ResearchSource.TRENDS: TrendCollector,
    }
    if source not in collectors:
        raise ValueError(f"Unknown source: {source}")
    return collectors[source](repo_root)


def run_collectors(sources: List[ResearchSource], repo_root: Path, schedule: str = None) -> Dict[str, Any]:
    """Run specified collectors"""
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "schedule": schedule,
        "sources": [s.value for s in sources],
        "results": {}
    }
    
    for source in sources:
        print(f"\n{'='*60}")
        print(f"Running {source.value} collector...")
        print(f"{'='*60}")
        
        collector = get_collector(source, repo_root)
        result = collector.run()
        results["results"][source.value] = result
        
        # Summary
        if "error" in result:
            print(f"  ❌ {source.value}: {result['error']}")
        else:
            print(f"  ✅ {source.value}: {result.get('collected', 0)} collected, {result.get('pending', 0)} pending")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Run Knowledge Tree Collectors")
    parser.add_argument("--all", action="store_true", help="Run all collectors")
    parser.add_argument("--source", choices=["academic", "standards", "trends"], 
                        help="Run specific collector")
    parser.add_argument("--schedule", choices=["15m", "6h", "weekly"], 
                        help="Schedule filter for logging")
    parser.add_argument("--repo-root", type=Path, help="Repository root path")
    
    args = parser.parse_args()
    
    # Determine repo root
    repo_root = args.repo_root or Path.cwd().resolve()
    # Verify it's the right repo
    if not (repo_root / ".agents").exists():
        # Try to find repo root
        for p in [repo_root] + list(repo_root.parents):
            if (p / ".agents").exists():
                repo_root = p
                break
    
    print(f"Repository root: {repo_root}")
    
    # Determine sources to run
    if args.all:
        sources = list(ResearchSource)
    elif args.source:
        sources = [ResearchSource(args.source)]
    else:
        # Default: run all
        sources = list(ResearchSource)
    
    # Run collectors
    results = run_collectors(sources, repo_root, args.schedule)
    
    # Save summary
    summary_dir = repo_root / ".work" / "research" / "collection_summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    schedule_suffix = f"_{args.schedule}" if args.schedule else ""
    summary_file = summary_dir / f"collection_{timestamp}{schedule_suffix}.json"
    
    summary_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n📄 Summary saved: {summary_file}")
    
    # Print overall summary
    total_collected = sum(r.get("collected", 0) for r in results["results"].values() if isinstance(r, dict))
    total_pending = sum(r.get("pending", 0) for r in results["results"].values() if isinstance(r, dict))
    
    print(f"\n{'='*60}")
    print(f"COLLECTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total collected: {total_collected}")
    print(f"Total pending: {total_pending}")
    print(f"Schedule: {args.schedule or 'manual'}")
    
    # Note: Collectors write to .work/research/ (not git-tracked)
    # Git commit happens in Processor phase when projects are created
    # and in Auto-Heal phase when INBOX.md is updated
    
    # Exit with error if any collector failed
    failed = any("error" in r for r in results["results"].values() if isinstance(r, dict))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()