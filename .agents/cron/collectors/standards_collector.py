#!/usr/bin/env python3
"""
Standards Collector - Phase 1
Crosswalks Master Tree against 5 frameworks (NGSS, CSTA, CS2023, UNESCO, OECD)
to identify gaps and create research items for each gap.
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


class StandardsCollector(BaseCollector):
    """Collects gaps from crosswalking Master Tree against standard frameworks"""
    
    FRAMEWORKS = {
        "NGSS": {
            "name": "Next Generation Science Standards",
            "focus": ["science", "engineering", "crosscutting concepts", "practices"],
            "url": "https://www.nextgenscience.org/"
        },
        "CSTA": {
            "name": "CSTA K-12 Computer Science Standards",
            "focus": ["computing systems", "networks", "data", "algorithms", "impacts"],
            "url": "https://csteachers.org/page/standards"
        },
        "ACM_CS2023": {
            "name": "ACM/IEEE CS2023 Computer Science Curricula",
            "focus": ["AR", "OS", "NC", "AL", "SDF", "FPL", "SE", "DM", "MSF", "AI", "GIT", "SPD", "HCI", "SEP"],
            "url": "https://csed.acm.org/"
        },
        "UNESCO_ICT": {
            "name": "UNESCO ICT Competency Framework for Teachers",
            "focus": ["technology literacy", "knowledge deepening", "knowledge creation"],
            "url": "https://unesdoc.unesco.org/ark:/48223/pf0000265721"
        },
        "OECD_PISA": {
            "name": "OECD PISA 2025/2028 Frameworks",
            "focus": ["creative thinking", "digital literacy", "global competence"],
            "url": "https://www.oecd.org/pisa/"
        }
    }
    
    def __init__(self, repo_root: Optional[Path] = None):
        super().__init__(ResearchSource.STANDARDS, repo_root)
        self.master_tree_path = self.repo_root / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"
        self.crosswalk_script = self.repo_root / ".agents" / "skills" / "knowledge-researcher" / "scripts" / "curriculum_crosswalk.py"
    
    def _load_master_concepts(self) -> List[Dict[str, Any]]:
        """Load Master Tree concepts for gap detection"""
        concepts = []
        if not self.master_tree_path.exists():
            return concepts
        
        try:
            lines = self.master_tree_path.read_text(encoding="utf-8").splitlines()
            headers = None
            in_data_section = False
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith("Bảng") or line.startswith("Mỗi") or line.startswith("Đây là") or line.startswith("Các") or (line.startswith("|") and "code" not in line):
                    continue
                
                if line.startswith("code\t") and ("name" in line or "name\t" in line):
                    headers = line.split("\t")
                    in_data_section = True
                    continue
                
                if in_data_section and headers and line and "\t" in line:
                    parts = line.split("\t")
                    if len(parts) >= len(headers):
                        concept = dict(zip(headers, parts))
                        code = concept.get("code", "").strip()
                        if code:
                            concepts.append(concept)
        except Exception as e:
            print(f"  ⚠️ Failed to load Master Tree: {e}")
        
        return concepts
    
    def _run_crosswalk(self, framework: str) -> Optional[Path]:
        """Run curriculum_crosswalk.py for a framework"""
        if not self.crosswalk_script.exists():
            print(f"  ⚠️ Crosswalk script not found: {self.crosswalk_script}")
            return None
        
        output_dir = self.research_dir / f"crosswalk_{framework.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Run crosswalk with this framework as reference
            other_frameworks = [f for f in self.FRAMEWORKS.keys() if f != framework]
            
            cmd = [
                sys.executable, str(self.crosswalk_script),
                "--reference", framework,
                "--compare"] + other_frameworks + [
                "--out-dir", str(output_dir)
            ]
            
            print(f"  Running crosswalk: {framework} vs {', '.join(other_frameworks)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(self.repo_root))
            
            if result.returncode == 0:
                print(f"  ✅ Crosswalk complete: {output_dir}")
                return output_dir
            else:
                print(f"  ❌ Crosswalk failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"  ❌ Crosswalk timeout for {framework}")
            return None
        except Exception as e:
            print(f"  ❌ Crosswalk error for {framework}: {e}")
            return None
    
    def _parse_crosswalk_gaps(self, crosswalk_dir: Path, framework: str) -> List[Dict[str, Any]]:
        """Parse crosswalk output to extract gaps"""
        gaps = []
        
        # Look for crosswalk document
        crosswalk_docs = list(crosswalk_dir.glob("crosswalk_document_*.md"))
        if not crosswalk_docs:
            return gaps
        
        doc_path = crosswalk_docs[0]
        content = doc_path.read_text(encoding="utf-8")
        
        # Simple parsing: look for "Gap" or "Missing" or "Divergence" sections
        # This is a simplified parser - could be enhanced
        lines = content.splitlines()
        in_gap_section = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ["gap", "missing", "divergence", "unique to"]):
                in_gap_section = True
            elif line.startswith("## ") and in_gap_section:
                in_gap_section = False
            
            if in_gap_section and line.strip().startswith("-"):
                # Extract gap description
                gap_text = line.strip()[1:].strip()
                if len(gap_text) > 10:
                    gaps.append({
                        "framework": framework,
                        "description": gap_text[:200],
                        "source_doc": str(doc_path),
                        "detected_at": datetime.now(timezone.utc).isoformat()
                    })
        
        # Also check convergence CSV for quantitative gaps
        convergence_files = list(crosswalk_dir.glob("crosswalk_convergence_*.csv"))
        if convergence_files:
            try:
                import pandas as pd
                # Use proper CSV parsing with quoting
                df = pd.read_csv(convergence_files[0], quotechar='"', escapechar='\\')
                # Look for rows with "divergence" or "unique_to_reference" issue_type
                if 'issue_type' in df.columns:
                    divergence_rows = df[df['issue_type'].isin(['divergence', 'unique_to_reference', 'missing_in_comparison'])]
                    for _, row in divergence_rows.iterrows():
                        gaps.append({
                            "framework": framework,
                            "description": f"{row.get('lt_name', row.get('theme', 'Unknown'))}: {row.get('issue_type', 'gap')}",
                            "theme": row.get('lt_name', row.get('theme', '')),
                            "band": row.get('band', ''),
                            "source_doc": str(convergence_files[0]),
                            "detected_at": datetime.now(timezone.utc).isoformat()
                        })
            except Exception as e:
                print(f"  ⚠️ Failed to parse convergence CSV: {e}")
                # Fallback: manual CSV parsing
                try:
                    import csv
                    with open(convergence_files[0], 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            issue_type = row.get('issue_type', '')
                            if issue_type in ['divergence', 'unique_to_reference', 'missing_in_comparison']:
                                gaps.append({
                                    "framework": framework,
                                    "description": f"{row.get('lt_name', row.get('theme', 'Unknown'))}: {issue_type}",
                                    "theme": row.get('lt_name', row.get('theme', '')),
                                    "band": row.get('band', ''),
                                    "source_doc": str(convergence_files[0]),
                                    "detected_at": datetime.now(timezone.utc).isoformat()
                                })
                except Exception as e2:
                    print(f"  ⚠️ Fallback CSV parse also failed: {e2}")
        
        return gaps
    
    def _generate_gap_context(self, gap: Dict[str, Any], framework: str) -> str:
        """Generate structured context.md for a gap"""
        lines = [
            f"# Standards Gap: {framework} - {gap.get('theme', 'General')}",
            f"",
            f"**Framework:** {self.FRAMEWORKS[framework]['name']} ({framework})",
            f"**Detected:** {gap.get('detected_at', datetime.now(timezone.utc).isoformat())}",
            f"**Gap Type:** {gap.get('description', 'Missing concept/coverage')}",
            f"**Theme:** {gap.get('theme', 'N/A')}",
            f"**Band:** {gap.get('band', 'N/A')}",
            f"",
            f"---",
            f"",
            f"## Gap Description",
            f"",
            gap.get('description', 'No description available'),
            f"",
            f"---",
            f"",
            f"## Reference",
            f"- Crosswalk Document: {gap.get('source_doc', 'N/A')}",
            f"- Framework URL: {self.FRAMEWORKS[framework]['url']}",
            f"",
            f"---",
            f"",
            f"## Notes for LLM Processing",
            f"- This gap was identified by crosswalking Master Tree against {framework} and other frameworks",
            f"- Analyze what concepts/topics from {framework} are missing or misaligned in Master Tree",
            f"- Propose specific new Concepts, Topics, or Categories to add",
            f"- Ensure technology-agnostic naming (Marr T6 compliance)",
            f"- Map to CS2023 KAs where applicable",
        ]
        return '\n'.join(lines)
    
    def collect(self) -> List[ResearchMetadata]:
        """Run crosswalk for all frameworks and create gap research items"""
        new_items = []
        master_concepts = self._load_master_concepts()
        
        print(f"  Loaded {len(master_concepts)} Master Tree concepts")
        
        if not master_concepts:
            print("  ⚠️ No Master Tree concepts loaded, skipping crosswalk")
            return new_items
        
        # Run crosswalk for each framework (or just ACM_CS2023 as reference)
        # For efficiency, run with ACM_CS2023 as reference vs all others
        reference_framework = "ACM_CS2023"
        crosswalk_dir = self._run_crosswalk(reference_framework)
        
        if not crosswalk_dir:
            print(f"  ❌ Crosswalk failed for {reference_framework}")
            return new_items
        
        # Parse gaps from crosswalk
        gaps = self._parse_crosswalk_gaps(crosswalk_dir, reference_framework)
        
        # Also check for missing CS2023 KAs directly
        cs2023_gaps = self._check_cs2023_ka_coverage(master_concepts)
        gaps.extend(cs2023_gaps)
        
        print(f"  Found {len(gaps)} gaps from crosswalk")
        
        for i, gap in enumerate(gaps):
            # Generate item ID
            framework = gap.get('framework', reference_framework)
            theme = gap.get('theme', f'gap-{i}')
            item_id = self._generate_item_id(f"{framework}-{theme}")
            
            if self.is_processed(item_id):
                continue
            
            # Create item directory
            item_dir = self._create_item_dir(item_id)
            
            # Generate context.md
            context_md = self._generate_gap_context(gap, framework)
            (item_dir / "context.md").write_text(context_md, encoding='utf-8')
            
            # Save crosswalk reference
            (item_dir / "crosswalk_reference.txt").write_text(str(crosswalk_dir), encoding='utf-8')
            
            # Determine priority
            priority = "high" if framework == "ACM_CS2023" else "medium"
            
            # Create metadata
            metadata = ResearchMetadata(
                id=item_id,
                source=ResearchSource.STANDARDS,
                title=f"Standards Gap: {framework} - {theme}",
                context_path=str(item_dir.relative_to(self.repo_root)),
                priority=priority,
                status=ResearchStatus.PENDING,
                extra={
                    "framework": framework,
                    "theme": gap.get('theme', ''),
                    "band": gap.get('band', ''),
                    "gap_type": "missing_concept",
                    "crosswalk_dir": str(crosswalk_dir),
                    "description": gap.get('description', '')[:200]
                }
            )
            
            self._save_metadata(metadata)
            new_items.append(metadata)
            
            print(f"    Created gap item: {item_id}")
        
        return new_items
    
    def _check_cs2023_ka_coverage(self, concepts: List[Dict]) -> List[Dict[str, Any]]:
        """Check CS2023 Knowledge Areas coverage"""
        all_kas = ["AR", "OS", "NC", "AL", "SDF", "FPL", "SE", "DM", "MSF", "AI", "GIT", "SPD", "HCI", "SEP"]
        ka_counts = {ka: 0 for ka in all_kas}
        
        for concept in concepts:
            ka_mapping = concept.get("cs2023_ka_mapping", "").strip()
            if ka_mapping:
                for ka in ka_mapping.split(","):
                    ka = ka.strip()
                    if ka in ka_counts:
                        ka_counts[ka] += 1
        
        gaps = []
        for ka, count in ka_counts.items():
            if count == 0:
                gaps.append({
                    "framework": "ACM_CS2023",
                    "theme": f"KA_{ka}_MISSING",
                    "description": f"CS2023 Knowledge Area {ka} has 0 concepts mapped",
                    "ka": ka,
                    "detected_at": datetime.now(timezone.utc).isoformat()
                })
        
        return gaps


if __name__ == "__main__":
    collector = StandardsCollector()
    result = collector.run()
    print(json.dumps(result, indent=2, ensure_ascii=False))