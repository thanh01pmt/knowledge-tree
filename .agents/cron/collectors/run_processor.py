#!/usr/bin/env python3
"""
Run Processor - Phase 2 Entry Point
Scans pending research items, uses LLM to analyze gaps vs Master Tree,
creates projects and runs autonomous pipeline for each gap.

This replaces the direct cron-to-pipeline approach with a two-phase model:
Phase 1 (Collectors): Research & organize context → .work/research/
Phase 2 (Processor): LLM reads context → finds gaps → creates projects → runs pipeline
"""

import sys
import json
import subprocess
import os
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

# Load environment variables (same pattern as other scripts)
ENV_FILE = Path.home() / ".hermes" / ".env"
env_vars = {}
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

# Also load project .env
PROJ_ENV = Path(__file__).resolve().parents[3] / ".env"
if PROJ_ENV.exists():
    for line in PROJ_ENV.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_collector import ResearchMetadata, ResearchStatus, discover_pending_items, ResearchSource


def git_commit_push(message: str):
    """Commit and push changes to git."""
    try:
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print(f"✅ Git commit & push: {message}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git commit/push failed: {e}")


class ResearchProcessor:
    """Phase 2: Process pending research items → create projects → run pipeline"""
    
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or self._find_repo_root()
        self.inbox_path = self.repo_root / "projects" / "INBOX.md"
        self.inbox_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Pipeline script
        self.pipeline_script = self.repo_root / ".agents" / "skills" / "knowledge-researcher" / "scripts" / "run_autonomous_pipeline.py"
        
        # Check if we have the autonomous pipeline script
        if not self.pipeline_script.exists():
            # Try alternative locations
            alt_paths = [
                self.repo_root / "run_autonomous_pipeline.py",
                self.repo_root / ".agents" / "scripts" / "run_autonomous_pipeline.py",
            ]
            for p in alt_paths:
                if p.exists():
                    self.pipeline_script = p
                    break
    
    def _find_repo_root(self) -> Path:
        cur = Path.cwd().resolve()
        for _ in range(20):
            if (cur / ".agents").is_dir():
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent
        return Path.cwd().resolve()
    
    def _load_master_tree_context(self) -> str:
        """Load Master Tree summary for LLM context"""
        master_tree_path = self.repo_root / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"
        
        if not master_tree_path.exists():
            return "Master Tree not found."
        
        try:
            lines = master_tree_path.read_text(encoding="utf-8").splitlines()
            
            # Extract stats
            fields = subjects = categories = topics = concepts = 0
            in_data = False
            
            for line in lines:
                line = line.strip()
                if line.startswith("Bảng 1") or "Fields" in line and "code" in line.lower():
                    fields = sum(1 for l in lines if l.startswith("FLD-"))
                elif line.startswith("Bảng 2") or "Subjects" in line and "code" in line.lower():
                    subjects = sum(1 for l in lines if l.startswith("SUB-"))
                elif line.startswith("Bảng 3") or "Categories" in line and "code" in line.lower():
                    categories = sum(1 for l in lines if l.startswith("CAT-"))
                elif line.startswith("Bảng 4") or "Topics" in line and "code" in line.lower():
                    topics = sum(1 for l in lines if l.startswith("TOP-"))
                elif line.startswith("Bảng 5") or "Concepts" in line and "code" in line.lower():
                    concepts = sum(1 for l in lines if l.startswith("CON-"))
            
            return f"""Master Tree Summary:
- Fields: {fields}
- Subjects: {subjects}
- Categories: {categories}
- Topics: {topics}
- Concepts: {concepts}
Total nodes: {fields + subjects + categories + topics + concepts}

Key Principle: 100% Technology-Agnostic (Marr T6) - No specific tech names in Fields/Subjects/Categories/Topics/Concepts.
"""
        except Exception as e:
            return f"Error loading Master Tree: {e}"
    
    def _analyze_gaps_with_llm(self, research_item: ResearchMetadata, master_context: str) -> List[Dict[str, Any]]:
        """Use LLM to analyze research context and identify gaps vs Master Tree"""
        
        # Read research context
        context_path = self.repo_root / research_item.context_path / "context.md"
        if not context_path.exists():
            return []
        
        context_content = context_path.read_text(encoding="utf-8")
        
        # Build prompt
        prompt = f"""You are a Knowledge Tree Architect. Analyze the research context below and identify specific gaps in the Master Tree.

MASTER TREE CONTEXT:
{master_context}

RESEARCH ITEM:
Source: {research_item.source.value}
Title: {research_item.title}
Priority: {research_item.priority}
Context:
{context_content[:8000]}

TASK: Identify 1-3 SPECIFIC gaps where this research reveals missing concepts, topics, or categories in the Master Tree.

For EACH gap, provide:
1. gap_type: "missing_concept" | "missing_topic" | "missing_category" | "alignment_issue"
2. suggested_code: Proposed code (e.g., "CON-PARALLEL_COMPUTING", "TOP-AI_ETHICS")
3. suggested_name: Technology-agnostic name (Marr T6 compliant)
4. suggested_description: Brief description
5. cs2023_ka: Relevant CS2023 Knowledge Area(s) if applicable
6. parent_suggestion: Suggested parent Topic/Category code
7. confidence: 0-100
8. rationale: Why this gap exists based on the research

OUTPUT FORMAT: JSON array of gap objects only. No extra text.
"""
        
        # Call LLM via available interface
        try:
            # Use OpenAI-compatible API - prefer Ollama Cloud if available
            import requests
            import json
            
            # Check for Ollama Cloud first (ATE_MODEL=deepseek-v4-flash:cloud)
            model = env_vars.get("ATE_MODEL", "deepseek-v4-flash:cloud")
            openai_key = env_vars.get("SAAS_OLLAMA_CLOUD_API_KEY") or env_vars.get("OPENAI_API_KEY", "ollama")
            
            # Determine base URL: prefer cloud if API key available
            if env_vars.get("SAAS_OLLAMA_CLOUD_API_KEY"):
                # Ollama Cloud API endpoint
                openai_base = "https://api.ollama.ai/v1"
            else:
                # Fallback to local Ollama
                openai_base = env_vars.get("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
            
            print(f"  🔄 Calling LLM: {model} via {openai_base}")
            
            response = requests.post(
                f"{openai_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a Knowledge Tree Architect. Output only valid JSON array of gap objects."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 4000
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                # Parse JSON from response
                try:
                    gaps = json.loads(content)
                    if isinstance(gaps, list) and len(gaps) > 0:
                        print(f"  ✅ LLM gap analysis: {len(gaps)} gaps identified")
                        return gaps
                except json.JSONDecodeError:
                    print(f"  ⚠️ LLM returned non-JSON, using fallback")
            else:
                print(f"  ⚠️ LLM API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"  ⚠️ LLM analysis failed: {e}")
        
        # LLM failed — do NOT fabricate gaps (§9: No Metric Gaming)
        print(f"  ❌ LLM analysis failed — marking item as FAILED (no fallback)")
        return []
    
    def _scaffold_project(self, gap: Dict[str, Any], research_item: ResearchMetadata) -> Optional[str]:
        """Scaffold a new project for the gap"""
        # Generate project slug
        slug_base = gap.get('suggested_code', 'GAP').replace('CON-', '').replace('TOP-', '').replace('CAT-', '').lower()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        slug = f"gap-{slug_base}-{timestamp}"
        
        project_dir = self.repo_root / "projects" / slug
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create context directory
        context_dir = project_dir / "context"
        context_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy research context to project context
        research_context_dir = self.repo_root / research_item.context_path
        for file in research_context_dir.glob("*"):
            if file.is_file():
                import shutil
                shutil.copy2(file, context_dir / file.name)
        
        # Create project spec
        spec = {
            "project_slug": slug,
            "source_research": research_item.id,
            "source_type": research_item.source.value,
            "gap_analysis": gap,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "scaffolded"
        }
        (context_dir / "project_spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # Create a summary context file for the pipeline
        summary = f"""# Project: {slug}

**Source Research:** {research_item.id} ({research_item.source.value})
**Gap Type:** {gap.get('gap_type', 'unknown')}
**Suggested Code:** {gap.get('suggested_code', 'N/A')}
**Suggested Name:** {gap.get('suggested_name', 'N/A')}
**CS2023 KA:** {gap.get('cs2023_ka', 'N/A')}
**Parent Suggestion:** {gap.get('parent_suggestion', 'N/A')}
**Confidence:** {gap.get('confidence', 0)}%
**Rationale:** {gap.get('rationale', 'N/A')}

## Research Context
See context.md and other files in this directory.
"""
        (context_dir / "gap_summary.md").write_text(summary, encoding='utf-8')
        
        return slug
    
    def _run_pipeline(self, slug: str) -> Dict[str, Any]:
        """Run autonomous pipeline for an academic project.
        
        This delegates to the actual pipeline scripts. If the scripts
        are not available or fail, it reports failure honestly.
        """
        project_dir = self.repo_root / "projects" / slug
        context_dir = project_dir / "context"
        
        if not context_dir.exists():
            return {"error": f"Project context not found: {context_dir}", "success": False}
        
        # Update status.yaml with active project
        status_file = self.repo_root / "status.yaml"
        try:
            if status_file.exists():
                status = yaml.safe_load(status_file.read_text()) or {}
            else:
                status = {}
            status["active_project"] = slug
            status_file.write_text(yaml.dump(status, allow_unicode=True))
        except Exception as e:
            print(f"  ⚠️ Failed to update status.yaml: {e}")
        
        # Try running the assemble script as a first real step
        assemble_script = self.repo_root / ".agents" / "skills" / "tree-assembler" / "scripts" / "assemble_project.py"
        if assemble_script.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(assemble_script), "--project", slug],
                    capture_output=True, text=True, timeout=300,
                    cwd=str(self.repo_root)
                )
                if result.returncode == 0:
                    print(f"  ✅ Pipeline assemble step succeeded for {slug}")
                    return {"success": True, "output": result.stdout[-500:] if result.stdout else "OK"}
                else:
                    return {"error": f"Assemble failed: {result.stderr[-300:]}", "success": False}
            except subprocess.TimeoutExpired:
                return {"error": "Pipeline timed out", "success": False}
            except Exception as e:
                return {"error": str(e), "success": False}
        
        # No pipeline script available — mark for Agent processing
        return {"error": "Pipeline scripts not found — needs Agent execution", "success": False}
    
    def _write_staging_proposals(self, item: 'ResearchMetadata', gaps: List[Dict[str, Any]]):
        """Write gaps to staging_proposals.tsv for Human review.
        
        Standards and Trends gaps are NOT projects — they are proposals
        to add/modify nodes in the Master Tree. Human reviews and decides.
        """
        staging_file = self.repo_root / ".work" / "staging_proposals.tsv"
        staging_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write header if new file
        if not staging_file.exists():
            header = "source\tresearch_id\tgap_type\tsuggested_code\tsuggested_name\tsuggested_description\tcs2023_ka\tparent_suggestion\tconfidence\trationale\tstatus\n"
            staging_file.write_text(header, encoding='utf-8')
        
        # Append gaps
        with open(staging_file, 'a', encoding='utf-8') as f:
            for gap in gaps:
                row = '\t'.join([
                    item.source.value,
                    item.id,
                    gap.get('gap_type', ''),
                    gap.get('suggested_code', ''),
                    gap.get('suggested_name', ''),
                    gap.get('suggested_description', ''),
                    gap.get('cs2023_ka', ''),
                    gap.get('parent_suggestion', ''),
                    str(gap.get('confidence', 0)),
                    gap.get('rationale', ''),
                    'pending_review'
                ])
                f.write(row + '\n')
        
        print(f"  📋 Wrote {len(gaps)} proposals to staging_proposals.tsv")
    
    def _update_inbox(self, message: str):
        """Append message to INBOX.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n## [{timestamp}] {message}\n"
        
        if self.inbox_path.exists():
            content = self.inbox_path.read_text(encoding='utf-8')
        else:
            content = "# 📥 Agentic Cron Inbox (Needs Review)\n"
        
        content += entry
        self.inbox_path.write_text(content, encoding='utf-8')
    
    def process(self, limit: int = None, source_filter: ResearchSource = None) -> Dict[str, Any]:
        """Process pending research items.
        
        Routing logic:
        - ACADEMIC: Has a full syllabus → scaffold project + run pipeline
        - STANDARDS/TRENDS: Gap proposals → write to staging_proposals.tsv (Human reviews)
        """
        print(f"\n{'='*60}")
        print(f"PROCESSOR: Scanning pending research items...")
        print(f"{'='*60}")
        
        # Discover pending items
        pending = discover_pending_items(self.repo_root)
        
        if source_filter:
            pending = [p for p in pending if p.source == source_filter]
        
        if limit:
            pending = pending[:limit]
        
        print(f"Found {len(pending)} pending items")
        
        if not pending:
            return {"processed": 0, "projects_created": 0, "proposals_written": 0,
                    "timestamp": datetime.now(timezone.utc).isoformat()}
        
        # Load Master Tree context
        master_context = self._load_master_tree_context()
        
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "processed": 0,
            "projects_created": 0,
            "proposals_written": 0,
            "items": []
        }
        
        for item in pending:
            print(f"\n  Processing: {item.id} ({item.source.value})")
            
            # Update status to processing
            item.status = ResearchStatus.PROCESSING
            item.save(self.repo_root / item.context_path / "metadata.json")
            
            # ── Route by source type ──
            if item.source == ResearchSource.ACADEMIC:
                # Academic items have a full syllabus → create project + run pipeline
                result = self._process_academic(item, master_context)
                if result.get("project_slug"):
                    results["projects_created"] += 1
                    tag = "ACADEMIC"
                    self._update_inbox(
                        f"[{tag}] Project {result['project_slug']} created from {item.id} "
                        f"- Pipeline: {'SUCCESS' if result.get('success') else 'FAILED'}"
                    )
            else:
                # Standards/Trends → analyze gaps and write to staging proposals
                result = self._process_staging(item, master_context)
                results["proposals_written"] += result.get("proposals_count", 0)
                if result.get("proposals_count", 0) > 0:
                    tag = item.source.value.upper()
                    self._update_inbox(
                        f"[{tag}] {result['proposals_count']} gap proposals written to "
                        f"staging_proposals.tsv from {item.id}"
                    )
            
            results["processed"] += 1
            results["items"].append({
                "research_id": item.id,
                "source": item.source.value,
                "result": result
            })
        
        print(f"\n{'='*60}")
        print(f"PROCESSOR SUMMARY: {results['processed']} processed, "
              f"{results['projects_created']} projects, "
              f"{results['proposals_written']} staging proposals")
        print(f"{'='*60}")
        
        return results
    
    def _process_academic(self, item: 'ResearchMetadata', master_context: str) -> Dict[str, Any]:
        """Process an academic item: scaffold project + run pipeline."""
        # For academic items, use the research context directly as project context
        slug = self._scaffold_project(
            {"gap_type": "academic_syllabus",
             "suggested_code": item.extra.get('domain', 'general-computing'),
             "suggested_name": item.title,
             "suggested_description": item.title},
            item
        )
        if not slug:
            item.status = ResearchStatus.FAILED
            item.error_message = "Failed to scaffold project"
            item.save(self.repo_root / item.context_path / "metadata.json")
            return {"success": False, "error": "Scaffold failed"}
        
        pipeline_result = self._run_pipeline(slug)
        
        item.status = ResearchStatus.PROCESSED if pipeline_result.get("success") else ResearchStatus.FAILED
        item.processed_at = datetime.now(timezone.utc).isoformat()
        item.project_slug = slug
        item.error_message = pipeline_result.get("error")
        item.save(self.repo_root / item.context_path / "metadata.json")
        
        return {"success": pipeline_result.get("success", False), "project_slug": slug}
    
    def _process_staging(self, item: 'ResearchMetadata', master_context: str) -> Dict[str, Any]:
        """Process standards/trends item: LLM analyzes gaps → staging_proposals.tsv."""
        gaps = self._analyze_gaps_with_llm(item, master_context)
        
        if not gaps:
            item.status = ResearchStatus.SKIPPED
            item.error_message = "No gaps identified by LLM"
            item.save(self.repo_root / item.context_path / "metadata.json")
            return {"proposals_count": 0}
        
        # Write to staging file — Human will review
        self._write_staging_proposals(item, gaps)
        
        item.status = ResearchStatus.PROCESSED
        item.processed_at = datetime.now(timezone.utc).isoformat()
        item.save(self.repo_root / item.context_path / "metadata.json")
        
        return {"proposals_count": len(gaps)}


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Process pending research items → create projects → run pipeline")
    parser.add_argument("--limit", type=int, help="Limit number of items to process")
    parser.add_argument("--source", choices=["academic", "standards", "trends"], 
                        help="Filter by source")
    parser.add_argument("--repo-root", type=Path, help="Repository root path")
    parser.add_argument("--all-pending", action="store_true", help="Process all pending (no limit)")
    
    args = parser.parse_args()
    
    # Determine repo root
    repo_root = args.repo_root or Path.cwd().resolve()
    if not (repo_root / ".agents").exists():
        for p in [repo_root] + list(repo_root.parents):
            if (p / ".agents").exists():
                repo_root = p
                break
    
    print(f"Repository root: {repo_root}")
    
    # Determine source filter
    source_filter = None
    if args.source:
        from base_collector import ResearchSource
        source_filter = ResearchSource(args.source)
    
    # Determine limit
    limit = None if args.all_pending else (args.limit or 10)
    
    # Run processor
    processor = ResearchProcessor(repo_root)
    results = processor.process(limit=limit, source_filter=source_filter)
    
    # Save summary
    summary_dir = repo_root / ".work" / "research" / "processor_summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = summary_dir / f"processor_{timestamp}.json"
    summary_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n📄 Summary saved: {summary_file}")
    
    # Git commit & push if projects were created
    projects_created = results.get("projects_created", 0)
    if projects_created > 0:
        git_commit_push(f"feat(processor): {projects_created} projects created from research gaps")
    
    # Exit code: 0 = script ran successfully (cron-friendly)
    # Pipeline failures are logged in INBOX.md, not treated as script crash
    failed_count = sum(1 for r in results.get("pipeline_results", []) if not r.get("success", False))
    total_count = len(results.get("pipeline_results", []))
    if failed_count > 0:
        print(f"⚠️ {failed_count}/{total_count} pipelines failed (see INBOX.md)")
    print(f"✅ Processor completed: {projects_created} projects created")
    sys.exit(0)


if __name__ == "__main__":
    main()