#!/usr/bin/env python3
"""
Unified Roadmap Generation Orchestrator v3

Coordinates the entire roadmap generation pipeline by calling individual step scripts.
Each step is a standalone script that can be tested independently.

Pipeline steps:
  STEP 0:   roadmap_discovery.py        — scan Master Tree + projects → reuse_inventory.json
  STEP 1-2: extract_project_keywords.py — AST-level keyword extraction → keywords.json
  STEP 3:   resolve_concepts.py         — keyword → concept resolution → resolved_concepts.json
  STEP 4:   match_cios.py               — concept → CIO matching → matched_cios.json
  STEP 5:   resolve_sios.py             — cross-tech SIO resolution → resolved_sios.json
  STEP 6:   agent_as_judge.py           — validation gate → judgment.json
  STEP 7:   apply_to_staging.py         — sync approved LOs to Supabase (optional)
  STEP 8.5: instruction_code_extractor.py — code snippets for instructions → code_snippets.json
  STEP 9:   validate_roadmap.py         — post-generation validation → validation_report.json

Usage:
  python scripts/generate_roadmap_v3.py \
    --goal "Build iOS fitness tracker with SwiftUI and HealthKit" \
    --tech-stack "Swift,SwiftUI,HealthKit,CoreData" \
    --repo-url https://github.com/user/repo \
    --output-dir /tmp/roadmap-output
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class PipelineOrchestrator:
    """Orchestrates the roadmap generation pipeline."""

    def __init__(self, goal: str, tech_stack: str, output_dir: Path,
                 repo_url: str = None, repo_dir: Path = None,
                 skip_steps: List[str] = None, resume: bool = False):
        self.goal = goal
        self.tech_stack = tech_stack
        self.output_dir = output_dir
        self.repo_url = repo_url
        self.repo_dir = repo_dir
        self.skip_steps = skip_steps or []
        self.resume = resume

        # Target tech = first item of tech stack, uppercased
        self.target_tech = tech_stack.split(',')[0].strip().upper()

        # Setup directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir = self.output_dir / "quarantine"
        self.quarantine_dir.mkdir(exist_ok=True)

        # State file for resume capability
        self.state_file = self.output_dir / "pipeline_state.json"
        self.state = self._load_state()

        # Script paths
        self.repo_root = Path(__file__).resolve().parents[1]
        self.scripts_dir = self.repo_root / "scripts"

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def _load_state(self) -> Dict:
        if self.resume and self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"completed_steps": [], "artifacts": {}}

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _artifact(self, name: str, default: str) -> Path:
        return Path(self.state["artifacts"].get(name, self.output_dir / default))

    # ------------------------------------------------------------------
    # Script runner
    # ------------------------------------------------------------------

    def _run_script(self, script_name: str, args: List[str], cwd: Path = None) -> bool:
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False

        cmd = [sys.executable, str(script_path)] + args

        print(f"\n{'='*70}")
        print(f"🚀 {script_name} {' '.join(args)}")
        print('='*70)

        try:
            result = subprocess.run(cmd, cwd=cwd or self.repo_root)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Script failed with exit code {e.returncode}")
            return False

    def _skip_or_run(self, step_id: str) -> bool:
        if step_id in self.skip_steps:
            print(f"⏭️  Skipping {step_id}")
            return True
        if self.resume and step_id in self.state["completed_steps"]:
            print(f"✅ {step_id} already completed (resume)")
            return True
        return False

    def _complete(self, step_id: str, **artifacts):
        if step_id not in self.state["completed_steps"]:
            self.state["completed_steps"].append(step_id)
        for name, path in artifacts.items():
            self.state["artifacts"][name] = str(path)
        self._save_state()

    # ------------------------------------------------------------------
    # Pipeline steps
    # ------------------------------------------------------------------

    def step_0_discover(self) -> bool:
        """STEP 0: Discover existing projects and Master Tree."""
        if self._skip_or_run("step_0"):
            return True

        print("\n📋 STEP 0: Discovering Master Tree and existing projects...")
        out = self.output_dir / "reuse_inventory.json"

        success = self._run_script("roadmap_discovery.py", [
            "--goal", self.goal,
            "--tech-stack", self.tech_stack,
            "--output", str(out),
        ])

        if success:
            self._complete("step_0", inventory=out)
        return success

    def step_1_2_extract_keywords(self) -> bool:
        """STEP 1-2: Extract keywords from project repository."""
        if self._skip_or_run("step_1_2"):
            return True

        print("\n📋 STEP 1-2: Extracting keywords from project repository...")
        out = self.output_dir / "keywords.json"

        args = []
        if self.repo_dir:
            args += ["--repo-dir", str(self.repo_dir)]
        elif self.repo_url:
            args += ["--repo-url", self.repo_url]
        else:
            print("⚠️  No --repo-url or --repo-dir provided, skipping STEP 1-2")
            return True

        args += ["--output", str(out)]

        success = self._run_script("extract_project_keywords.py", args)
        if success:
            self._complete("step_1_2", keywords=out)
        return success

    def step_3_resolve_concepts(self) -> bool:
        """STEP 3: Resolve keywords to Master Tree concepts."""
        if self._skip_or_run("step_3"):
            return True

        print("\n📋 STEP 3: Resolving keywords to concepts...")
        keywords_file = self._artifact("keywords", "keywords.json")
        if not keywords_file.exists():
            print(f"⚠️  Keywords file not found ({keywords_file}), skipping STEP 3")
            return True

        out = self.output_dir / "resolved_concepts.json"

        success = self._run_script("resolve_concepts.py", [
            "--keywords", str(keywords_file),
            "--reuse-inventory", str(self._artifact("inventory", "reuse_inventory.json")),
            "--goal", self.goal,
            "--output", str(out),
        ])

        if success:
            self._complete("step_3", resolved_concepts=out)
        return success

    def step_4_match_cios(self) -> bool:
        """STEP 4: Match concepts to CIOs."""
        if self._skip_or_run("step_4"):
            return True

        print("\n📋 STEP 4: Matching concepts to CIOs...")
        resolved_file = self._artifact("resolved_concepts", "resolved_concepts.json")
        if not resolved_file.exists():
            print(f"⚠️  Resolved concepts not found ({resolved_file}), skipping STEP 4")
            return True

        out = self.output_dir / "matched_cios.json"

        success = self._run_script("match_cios.py", [
            "--resolved-concepts", str(resolved_file),
            "--reuse-inventory", str(self._artifact("inventory", "reuse_inventory.json")),
            "--projects-dir", str(self.repo_root / "projects"),
            "--output", str(out),
        ])

        if success:
            self._complete("step_4", matched_cios=out)
        return success

    def step_5_resolve_sios(self) -> bool:
        """STEP 5: Resolve SIOs (REUSE/ADAPT/GENERATE)."""
        if self._skip_or_run("step_5"):
            return True

        print("\n📋 STEP 5: Resolving SIOs via cross-tech CIO bridge...")
        matched_file = self._artifact("matched_cios", "matched_cios.json")
        if not matched_file.exists():
            print(f"⚠️  Matched CIOs not found ({matched_file}), skipping STEP 5")
            return True

        out = self.output_dir / "resolved_sios.json"

        success = self._run_script("resolve_sios.py", [
            "--matched-cios", str(matched_file),
            "--target-tech", self.target_tech,
            "--projects-dir", str(self.repo_root / "projects"),
            "--output", str(out),
        ])

        if success:
            self._complete("step_5", resolved_sios=out)
        return success

    def step_6_agent_judge(self) -> bool:
        """STEP 6: Agent-as-Judge validation gate."""
        if self._skip_or_run("step_6"):
            return True

        print("\n📋 STEP 6: Running Agent-as-Judge validation...")
        out = self.output_dir / "judgment.json"

        args = [
            "--concepts", str(self._artifact("resolved_concepts", "resolved_concepts.json")),
            "--sios", str(self._artifact("resolved_sios", "resolved_sios.json")),
            "--target-tech", self.target_tech,
            "--output", str(out),
        ]

        success = self._run_script("agent_as_judge.py", args)

        if success:
            self._complete("step_6", judgment=out)

            # Report judgment
            with open(out, 'r') as f:
                judgment = json.load(f)
            status = judgment.get("overall_status", "UNKNOWN")
            print(f"\n🔒 Judge verdict: {status}")
            if status == "FAIL":
                print("❌ Agent-as-Judge rejected. Pipeline continues but review required.")
        return success

    def step_7_apply_staging(self) -> bool:
        """STEP 7: Apply quarantine to staging (Supabase)."""
        if self._skip_or_run("step_7"):
            return True

        print("\n📋 STEP 7: Applying quarantine to staging...")

        # Check quarantine has content
        tsv_files = list(self.quarantine_dir.glob("*.tsv"))
        if not tsv_files:
            print("ℹ️  No quarantine TSVs to apply, skipping")
            return True

        # Dry-run by default to avoid unintended Supabase writes
        return self._run_script("apply_to_staging.py", [
            "--quarantine-dir", str(self.quarantine_dir),
            "--dry-run",
        ])

    def step_8_5_extract_snippets(self) -> bool:
        """STEP 8.5: Extract code snippets for instruction generation."""
        if self._skip_or_run("step_8_5"):
            return True

        print("\n📋 STEP 8.5: Extracting code snippets...")
        sios_file = self._artifact("resolved_sios", "resolved_sios.json")
        if not sios_file.exists():
            print("⚠️  Resolved SIOs not found, skipping STEP 8.5")
            return True

        # Need a local repo dir
        repo_dir = self.repo_dir
        if not repo_dir:
            print("⚠️  No --repo-dir provided, skipping STEP 8.5")
            return True

        out = self.output_dir / "code_snippets.json"

        success = self._run_script("instruction_code_extractor.py", [
            "--repo-dir", str(repo_dir),
            "--sios-file", str(sios_file),
            "--output", str(out),
        ])

        if success:
            self._complete("step_8_5", code_snippets=out)
        return success

    def step_9_validate(self) -> bool:
        """STEP 9: Post-generation validation."""
        if self._skip_or_run("step_9"):
            return True

        print("\n📋 STEP 9: Running post-generation validation...")

        # Build a roadmap skeleton from resolved artifacts for validation
        roadmap_file = self.output_dir / "roadmap.json"
        self._build_roadmap_skeleton(roadmap_file)

        args = [
            "--roadmap-file", str(roadmap_file),
            "--sios-file", str(self._artifact("resolved_sios", "resolved_sios.json")),
            "--concepts-file", str(self._artifact("resolved_concepts", "resolved_concepts.json")),
            "--output", str(self.output_dir / "validation_report.json"),
        ]

        snippets_file = self._artifact("code_snippets", "code_snippets.json")
        if snippets_file.exists():
            args += ["--code-snippets-file", str(snippets_file)]

        success = self._run_script("validate_roadmap.py", args)
        if success:
            self._complete("step_9", validation_report=self.output_dir / "validation_report.json")
        return success

    def _build_roadmap_skeleton(self, roadmap_file: Path):
        """Build a minimal roadmap.json from resolved artifacts for validation.

        Maps each resolved concept to a milestone with its LO chain.
        """
        resolved_file = self._artifact("resolved_concepts", "resolved_concepts.json")
        sios_file = self._artifact("resolved_sios", "resolved_sios.json")

        milestones = []
        seen_concepts = set()

        # From resolved concepts
        if resolved_file.exists():
            with open(resolved_file, 'r') as f:
                resolved = json.load(f)
            for item in resolved.get("resolved", []):
                code = item.get("concept_code") or (item.get("matches") or [{}])[0].get("code")
                if code and code not in seen_concepts:
                    seen_concepts.add(code)
                    milestones.append({
                        "concept_code": code,
                        "prerequisites": [],
                        "learning_objectives": [],
                    })

        # Attach LOs from resolved SIOs
        if sios_file.exists():
            with open(sios_file, 'r') as f:
                sios_data = json.load(f)

            for milestone in milestones:
                concept = milestone["concept_code"]
                for group in sios_data.get("resolved_sios", []):
                    # Match by normalized CIO containing concept code
                    normalized = group.get("normalized_cio", "")
                    if concept in normalized:
                        for sio in group.get("sios", []):
                            milestone["learning_objectives"].append({
                                "code": sio.get("code", ""),
                                "lo_type": "SPECIFIC_IMPL",
                                "name": sio.get("name", ""),
                            })

        roadmap = {
            "project_brief": {
                "goal": self.goal,
                "tech_stack": [t.strip() for t in self.tech_stack.split(",")],
            },
            "phases": [{
                "phase_id": 1,
                "title": "Phase 1: Core Skills",
                "milestones": milestones,
            }],
            "total_milestones": len(milestones),
            "total_concepts": len(seen_concepts),
        }

        with open(roadmap_file, 'w') as f:
            json.dump(roadmap, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Pipeline runner
    # ------------------------------------------------------------------

    def run_pipeline(self) -> bool:
        print("="*70)
        print("🚀 UNIFIED ROADMAP GENERATION PIPELINE v3")
        print("="*70)
        print(f"Goal:        {self.goal}")
        print(f"Tech stack:  {self.tech_stack}")
        print(f"Target tech: {self.target_tech}")
        print(f"Output:      {self.output_dir}")
        if self.skip_steps:
            print(f"Skip:        {', '.join(self.skip_steps)}")
        if self.resume:
            print(f"Resume:      from {self.state_file}")
        print("="*70)

        start = datetime.now()

        steps = [
            ("step_0", self.step_0_discover),
            ("step_1_2", self.step_1_2_extract_keywords),
            ("step_3", self.step_3_resolve_concepts),
            ("step_4", self.step_4_match_cios),
            ("step_5", self.step_5_resolve_sios),
            ("step_6", self.step_6_agent_judge),
            ("step_7", self.step_7_apply_staging),
            ("step_8_5", self.step_8_5_extract_snippets),
            ("step_9", self.step_9_validate),
        ]

        for step_id, step_fn in steps:
            self.state["current_step"] = step_id
            self._save_state()
            if not step_fn():
                print(f"\n❌ Pipeline failed at {step_id}")
                return False

        duration = (datetime.now() - start).total_seconds()
        self._generate_summary(duration)

        print("\n" + "="*70)
        print(f"✅ PIPELINE COMPLETED in {duration:.1f}s")
        print(f"📁 Output: {self.output_dir}")
        print("="*70)
        return True

    def _generate_summary(self, duration: float):
        summary = {
            "goal": self.goal,
            "tech_stack": self.tech_stack,
            "target_tech": self.target_tech,
            "completed_at": datetime.now().isoformat(),
            "duration_seconds": round(duration, 1),
            "completed_steps": self.state["completed_steps"],
            "artifacts": self.state["artifacts"],
        }
        summary_file = self.output_dir / "pipeline_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Unified Roadmap Generation Pipeline v3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline with a GitHub repo
  python scripts/generate_roadmap_v3.py \\
    --goal "Build iOS fitness tracker with SwiftUI and HealthKit" \\
    --tech-stack "Swift,SwiftUI,HealthKit,CoreData" \\
    --repo-url https://github.com/user/repo \\
    --output-dir /tmp/roadmap-output

  # With local repo, skip staging sync
  python scripts/generate_roadmap_v3.py \\
    --goal "Learn SwiftUI" \\
    --tech-stack "Swift,SwiftUI" \\
    --repo-dir ./projects/swift-associate \\
    --output-dir /tmp/out \\
    --skip-steps step_7
        """
    )

    parser.add_argument("--goal", required=True, help="Learning goal description")
    parser.add_argument("--tech-stack", required=True,
                       help="Comma-separated tech stack (first item = target tech)")
    parser.add_argument("--repo-url", help="GitHub repository URL to analyze")
    parser.add_argument("--repo-dir", type=Path, help="Local repository directory (instead of cloning)")
    parser.add_argument("--output-dir", required=True, type=Path,
                       help="Output directory for pipeline artifacts")
    parser.add_argument("--skip-steps", nargs="*", default=[],
                       help="Steps to skip (step_0 step_7 ...)")
    parser.add_argument("--resume", action="store_true",
                       help="Resume from last checkpoint")

    args = parser.parse_args()

    orchestrator = PipelineOrchestrator(
        goal=args.goal,
        tech_stack=args.tech_stack,
        output_dir=args.output_dir,
        repo_url=args.repo_url,
        repo_dir=args.repo_dir,
        skip_steps=args.skip_steps,
        resume=args.resume,
    )

    sys.exit(0 if orchestrator.run_pipeline() else 1)


if __name__ == "__main__":
    main()
