#!/usr/bin/env python3
"""
Trend Collector - Phase 1
Discovers emerging trends via auto_stem_discovery (last30days, Exa, Crawl4AI)
and creates research items for high-priority trends.
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_collector import BaseCollector, ResearchMetadata, ResearchSource, ResearchStatus


class TrendCollector(BaseCollector):
    """Collects emerging trends using auto_stem_discovery.py"""
    
    def __init__(self, repo_root: Optional[Path] = None):
        super().__init__(ResearchSource.TRENDS, repo_root)
        self.discovery_script = self.repo_root / ".agents" / "skills" / "knowledge-researcher" / "scripts" / "auto_stem_discovery.py"
        self.queue_file = self.repo_root / ".work" / "research_queue.json"
    
    def _run_discovery(self) -> Dict[str, Any]:
        """Run auto_stem_discovery.py to update research queue"""
        if not self.discovery_script.exists():
            return {"error": f"Discovery script not found: {self.discovery_script}"}
        
        try:
            print(f"  Running auto_stem_discovery.py --deep...")
            cmd = [
                sys.executable, str(self.discovery_script),
                "--deep", "--out-dir", ".work"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=str(self.repo_root))
            
            if result.returncode == 0:
                print(f"  ✅ Discovery complete")
                return {"success": True, "output": result.stdout}
            else:
                print(f"  ❌ Discovery failed: {result.stderr}")
                return {"error": result.stderr, "success": False}
        except subprocess.TimeoutExpired:
            return {"error": "Discovery timed out", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _load_queue(self) -> List[Dict[str, Any]]:
        """Load research queue from auto_stem_discovery"""
        if not self.queue_file.exists():
            return []
        
        try:
            return json.loads(self.queue_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ⚠️ Failed to load queue: {e}")
            return []
    
    def _run_crosswalk_for_trend(self, trend_topic: str) -> Optional[Path]:
        """Run curriculum crosswalk for a specific trend topic"""
        crosswalk_script = self.repo_root / ".agents" / "skills" / "knowledge-researcher" / "scripts" / "curriculum_crosswalk.py"
        
        if not crosswalk_script.exists():
            return None
        
        safe_slug = trend_topic.lower().replace(" ", "-").replace("/", "-")[:50]
        output_dir = self.research_dir / f"crosswalk_{safe_slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            cmd = [
                sys.executable, str(crosswalk_script),
                "--reference", "ACM_CS2023",
                "--compare", "NGSS", "CSTA", "UNESCO_ICT", "OECD_PISA",
                "--out-dir", str(output_dir)
            ]
            
            print(f"    Crosswalking trend: {trend_topic}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(self.repo_root))
            
            if result.returncode == 0:
                print(f"    ✅ Crosswalk complete")
                return output_dir
            else:
                print(f"    ⚠️ Crosswalk failed: {result.stderr[:100]}")
                return None
        except Exception as e:
            print(f"    ⚠️ Crosswalk error: {e}")
            return None
    
    def _generate_trend_context(self, trend: Dict[str, Any], crosswalk_dir: Optional[Path]) -> str:
        """Generate structured context.md for a trend"""
        lines = [
            f"# Trend Research: {trend.get('topic', 'Unknown')}",
            f"",
            f"**Topic:** {trend.get('topic', 'Unknown')}",
            f"**Source:** {trend.get('source', 'auto_stem_discovery')}",
            f"**Query:** {trend.get('query', 'N/A')}",
            f"**Discovered:** {trend.get('discovered_at', datetime.now(timezone.utc).isoformat())}",
            f"**Priority Score:** {trend.get('priority_score', 'N/A')}",
            f"",
            f"---",
            f"",
            f"## Scoring Breakdown",
            f"- **Foundation Score:** {trend.get('foundation_score', 'N/A')}/10",
            f"- **Trend Velocity:** {trend.get('trend_velocity', 'N/A')}/10",
            f"- **Educational Fit:** {trend.get('educational_fit', 'N/A')}/10",
            f"- **Gap Bonus:** {trend.get('gap_bonus', 'N/A')}",
            f"",
            f"---",
            f"",
            f"## Evidence",
            f"",
            trend.get('evidence', 'No evidence available'),
            f"",
            f"---",
            f"",
        ]
        
        if crosswalk_dir:
            lines.extend([
                f"## Curriculum Crosswalk (ACM_CS2023 vs NGSS/CSTA/UNESCO/OECD)",
                f"",
                f"**Crosswalk Directory:** {crosswalk_dir}",
                f"",
                f"---",
                f"",
            ])
        
        lines.extend([
            f"## Notes for LLM Processing",
            f"- This is an emerging trend in STEM/CS education",
            f"- Analyze how this trend maps to Master Tree concepts",
            f"- Identify missing concepts, topics, or categories",
            f"- Consider technology-agnostic framing (Marr T6)",
            f"- Propose new Concepts/Topics for project creation",
            f"- Check crosswalk results for curriculum alignment opportunities",
        ])
        
        return '\n'.join(lines)
    
    def collect(self) -> List[ResearchMetadata]:
        """Run discovery and create research items for high-priority trends"""
        new_items = []
        
        # Run discovery to update queue
        discovery_result = self._run_discovery()
        
        if not discovery_result.get("success"):
            print(f"  Discovery failed: {discovery_result.get('error', 'Unknown')}")
            return new_items
        
        # Load updated queue
        queue = self._load_queue()
        
        if not queue:
            print("  Queue is empty")
            return new_items
        
        # Filter high-priority items (priority_score >= 7.0)
        high_priority = [item for item in queue if item.get('priority_score', 0) >= 7.0]
        
        # Also include framework monitor items
        framework_items = [item for item in queue if item.get('source') == 'framework_monitor']
        
        candidates = high_priority + framework_items
        
        # Limit to top 5 to avoid overwhelming
        candidates = sorted(candidates, key=lambda x: x.get('priority_score', 0), reverse=True)[:5]
        
        print(f"  Found {len(candidates)} high-priority trends (from {len(queue)} total)")
        
        for trend in candidates:
            topic = trend.get('topic', 'unknown')
            item_id = self._generate_item_id(f"trend-{topic}")
            
            if self.is_processed(item_id):
                continue
            
            # Create item directory
            item_dir = self._create_item_dir(item_id)
            
            # Run crosswalk for this trend
            crosswalk_dir = self._run_crosswalk_for_trend(topic)
            
            # Generate context.md
            context_md = self._generate_trend_context(trend, crosswalk_dir)
            (item_dir / "context.md").write_text(context_md, encoding='utf-8')
            
            # Save trend data
            (item_dir / "trend_data.json").write_text(json.dumps(trend, indent=2, ensure_ascii=False), encoding='utf-8')
            
            if crosswalk_dir:
                (item_dir / "crosswalk_reference.txt").write_text(str(crosswalk_dir), encoding='utf-8')
            
            # Create metadata
            metadata = ResearchMetadata(
                id=item_id,
                source=ResearchSource.TRENDS,
                title=f"Trend: {topic}",
                context_path=str(item_dir.relative_to(self.repo_root)),
                priority="high" if trend.get('priority_score', 0) >= 8.0 else "medium",
                status=ResearchStatus.PENDING,
                extra={
                    "topic": topic,
                    "source": trend.get('source', 'auto_stem_discovery'),
                    "priority_score": trend.get('priority_score', 0),
                    "foundation_score": trend.get('foundation_score', 0),
                    "trend_velocity": trend.get('trend_velocity', 0),
                    "educational_fit": trend.get('educational_fit', 0),
                    "evidence": trend.get('evidence', '')[:200],
                    "crosswalk_dir": str(crosswalk_dir) if crosswalk_dir else None
                }
            )
            
            self._save_metadata(metadata)
            new_items.append(metadata)
            
            print(f"    Created trend item: {item_id} (score: {trend.get('priority_score', 0)})")
        
        return new_items


if __name__ == "__main__":
    collector = TrendCollector()
    result = collector.run()
    print(json.dumps(result, indent=2, ensure_ascii=False))