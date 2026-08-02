#!/usr/bin/env python3
"""
Academic Collector - Phase 1
Watches inputs/academic/ for new PDF/MD/TXT files and creates research items.
"""

import os
import sys
import json
import shutil
import subprocess
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_collector import BaseCollector, ResearchMetadata, ResearchSource, ResearchStatus


class AcademicCollector(BaseCollector):
    """Collects academic syllabus documents from inputs/academic/"""
    
    def __init__(self, repo_root: Optional[Path] = None):
        super().__init__(ResearchSource.ACADEMIC, repo_root)
        self.inputs_dir = self.repo_root / "inputs" / "academic"
        self.inputs_dir.mkdir(parents=True, exist_ok=True)
        
        # Supported file extensions
        self.supported_extensions = {'.pdf', '.md', '.txt', '.csv', '.docx'}
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using pdftotext or pymupdf"""
        try:
            import fitz  # pymupdf
            doc = fitz.open(str(pdf_path))
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except ImportError:
            # Fallback to pdftotext
            try:
                result = subprocess.run(
                    ['pdftotext', str(pdf_path), '-'],
                    capture_output=True, text=True, timeout=60
                )
                return result.stdout
            except:
                return f"[PDF content extraction failed - install pymupdf or pdftotext: {pdf_path.name}]"
        except Exception as e:
            return f"[PDF extraction error: {e}]"
    
    def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from various file types"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self._extract_text_from_pdf(file_path)
        elif suffix in ['.md', '.txt', '.csv']:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        elif suffix == '.docx':
            try:
                import docx
                doc = docx.Document(str(file_path))
                return '\n'.join([p.text for p in doc.paragraphs])
            except:
                return f"[DOCX extraction failed - install python-docx: {file_path.name}]"
        else:
            return f"[Unsupported file type: {suffix}]"
    
    def _generate_context_markdown(self, file_path: Path, content: str, metadata: dict) -> str:
        """Generate structured context.md for the research item"""
        lines = [
            f"# Academic Syllabus: {file_path.stem}",
            f"",
            f"**Source File:** {file_path.name}",
            f"**Collected:** {datetime.now(timezone.utc).isoformat()}",
            f"**File Type:** {file_path.suffix}",
            f"**Domain:** {metadata.get('domain', 'unknown')}",
            f"**Priority:** {metadata.get('priority', 'medium')}",
            f"",
            f"---",
            f"",
            f"## Extracted Content",
            f"",
            content[:50000],  # Limit size
            f"",
            f"---",
            f"",
            f"## Notes for LLM Processing",
            f"- This is an academic syllabus/document from an educational institution",
            f"- Extract: learning objectives, topics, concepts, competencies",
            f"- Map to Master Tree concepts (NGSS, CSTA, CS2023, etc.)",
            f"- Identify gaps for new project creation",
        ]
        return '\n'.join(lines)
    
    def _extract_domain_from_filename(self, filename: str) -> str:
        """Extract domain hint from filename"""
        name = filename.lower()
        domains = {
            'swift': 'swift-programming',
            'python': 'python-programming', 
            'javascript': 'javascript-programming',
            'java': 'java-programming',
            'cs': 'computer-science',
            'algorithm': 'algorithms',
            'data-structure': 'data-structures',
            'web': 'web-development',
            'mobile': 'mobile-development',
            'ai': 'artificial-intelligence',
            'ml': 'machine-learning',
            'security': 'cybersecurity',
            'network': 'networking',
            'database': 'databases',
        }
        for key, domain in domains.items():
            if key in name:
                return domain
        return 'general-computing'
    
    def collect(self) -> List[ResearchMetadata]:
        """Scan inputs/academic/ for new files and create research items"""
        new_items = []
        
        if not self.inputs_dir.exists():
            print(f"  Inputs directory not found: {self.inputs_dir}")
            return new_items
        
        for file_path in self.inputs_dir.iterdir():
            if not file_path.is_file():
                continue
            
            if file_path.suffix.lower() not in self.supported_extensions:
                continue
            
            # Generate item ID
            item_id = self._generate_item_id(file_path.stem)
            
            # Skip if already processed
            if self.is_processed(item_id):
                continue
            
            print(f"  Found new academic input: {file_path.name}")
            
            # Extract content
            content = self._extract_text_from_file(file_path)
            
            # Determine domain and priority
            domain = self._extract_domain_from_filename(file_path.name)
            priority = 'high' if file_path.suffix.lower() == '.pdf' else 'medium'
            
            # Create item directory
            item_dir = self._create_item_dir(item_id)
            
            # Copy original file
            raw_file = item_dir / f"raw{file_path.suffix}"
            shutil.copy2(file_path, raw_file)
            
            # Generate context.md
            context_md = self._generate_context_markdown(file_path, content, {
                'domain': domain,
                'priority': priority
            })
            (item_dir / "context.md").write_text(context_md, encoding='utf-8')
            
            # Create metadata
            metadata = ResearchMetadata(
                id=item_id,
                source=ResearchSource.ACADEMIC,
                title=f"Academic: {file_path.stem}",
                context_path=str(item_dir.relative_to(self.repo_root)),
                priority=priority,
                status=ResearchStatus.PENDING,
                extra={
                    'original_file': file_path.name,
                    'file_type': file_path.suffix.lower(),
                    'domain': domain,
                    'raw_file': raw_file.name,
                    'content_length': len(content)
                }
            )
            
            self._save_metadata(metadata)
            new_items.append(metadata)
            
            print(f"    Created research item: {item_id}")
        
        return new_items


if __name__ == "__main__":
    collector = AcademicCollector()
    result = collector.run()
    print(json.dumps(result, indent=2, ensure_ascii=False))