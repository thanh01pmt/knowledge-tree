#!/usr/bin/env python3
"""
Sub-MCP Server: Knowledge Researcher (Tier 1 & Tier 2)
"""
import sys
import subprocess
from pathlib import Path
from fastmcp import FastMCP

# Paths
SERVER_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SERVER_DIR.parent.parent.parent.parent.parent # Navigate to knowledge-tree root
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"

research_mcp = FastMCP("KnowledgeResearcher")

def _run_research_script(script_path: Path, extra_args: list = None, timeout: int = 300) -> str:
    if not script_path.exists():
        return f"Error: Cannot find {script_path.name} at {script_path}"
    
    cmd = [sys.executable, str(script_path)] + (extra_args or [])
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR), timeout=timeout)
        output = res.stdout or res.stderr
        if res.returncode != 0:
            return f"❌ Script failed (Code {res.returncode}):\n{output}"
        return output
    except subprocess.TimeoutExpired:
        return f"❌ Error: {script_path.name} timed out after {timeout}s."

@research_mcp.tool
def audit_curriculum(framework: str = "ACM CS2023") -> str:
    """
    Tier 1: Curriculum Audit. 
    Cross-references the existing Master Knowledge Tree against standard curricula (e.g., NGSS, ACM).
    Returns a report of foundational gaps.
    
    Args:
        framework: The standard curriculum to audit against (e.g., "ACM CS2023")
    """
    script_path = SKILLS_DIR / "knowledge-researcher" / "scripts" / "audit_curriculum.py"
    output = _run_research_script(script_path, extra_args=["--curriculum", framework], timeout=300)
    
    # Check if a gap report was generated and append it
    gap_file = ROOT_DIR / ".work" / "research" / "foundational_gaps.md"
    if gap_file.exists():
        output += f"\n\n--- FOUNDATIONAL GAPS REPORT ---\n{gap_file.read_text(encoding='utf-8')}"
        
    return output

@research_mcp.tool
def watch_trends(query: str = "emerging technologies in STEM education") -> str:
    """
    Tier 2: Trend Watcher.
    Performs periodic scans for emerging trends in STEM education that are not present 
    in the Master Knowledge Tree. Updates a priority queue of research topics.
    
    Args:
        query: Broad query to search for trends
    """
    script_path = SKILLS_DIR / "knowledge-researcher" / "scripts" / "auto_stem_discovery.py"
    output = _run_research_script(script_path, extra_args=["--query", query], timeout=300)
    
    queue_file = ROOT_DIR / ".work" / "research_queue.json"
    if queue_file.exists():
        output += f"\n\n--- RESEARCH QUEUE STATUS ---\n{queue_file.read_text(encoding='utf-8')}"
        
    return output
