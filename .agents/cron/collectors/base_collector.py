#!/usr/bin/env python3
"""
Base Collector Framework for Knowledge Tree
Phase 1: Collect & Organize Context

All collectors inherit from BaseCollector and produce structured context packages
in .work/research/<source>/<item_id>/
"""

import os
import json
import hashlib
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum


class ResearchStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ResearchSource(str, Enum):
    ACADEMIC = "academic"
    STANDARDS = "standards"
    TRENDS = "trends"


@dataclass
class ResearchMetadata:
    """Unified metadata schema for all research items"""
    id: str
    source: ResearchSource
    title: str
    context_path: str
    priority: str  # high, medium, low
    status: ResearchStatus = ResearchStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    processed_at: Optional[str] = None
    project_slug: Optional[str] = None
    error_message: Optional[str] = None
    
    # Source-specific fields (flexible)
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ResearchMetadata':
        data = json.loads(json_str)
        # Convert enum strings back to enums
        data['source'] = ResearchSource(data['source'])
        data['status'] = ResearchStatus(data['status'])
        return cls(**data)
    
    def save(self, path: Path):
        path.write_text(self.to_json(), encoding='utf-8')
    
    @classmethod
    def load(cls, path: Path) -> 'ResearchMetadata':
        return cls.from_json(path.read_text(encoding='utf-8'))


class BaseCollector(ABC):
    """Abstract base class for all collectors"""
    
    def __init__(self, source: ResearchSource, repo_root: Optional[Path] = None):
        self.source = source
        self.repo_root = repo_root or self._find_repo_root()
        self.research_dir = self.repo_root / ".work" / "research" / source.value
        self.research_dir.mkdir(parents=True, exist_ok=True)
        self.processed_log = self.repo_root / ".work" / "research" / f"{source.value}_processed.json"
        self._load_processed_log()
    
    def _find_repo_root(self) -> Path:
        cur = Path.cwd().resolve()
        for _ in range(20):
            if (cur / ".agents").is_dir():
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent
        return Path.cwd().resolve()
    
    def _load_processed_log(self):
        if self.processed_log.exists():
            try:
                self.processed_items = set(json.loads(self.processed_log.read_text()))
            except:
                self.processed_items = set()
        else:
            self.processed_items = set()
    
    def _save_processed_log(self):
        self.processed_log.write_text(json.dumps(list(self.processed_items)), encoding='utf-8')
    
    def _generate_item_id(self, title: str, extra_key: str = "") -> str:
        """Generate deterministic ID from title + extra_key (content-addressable).
        
        The same title+extra_key will ALWAYS produce the same ID,
        so re-running a collector won't create duplicate items.
        """
        content = f"{self.source.value}:{title}:{extra_key}"
        hash_suffix = hashlib.md5(content.encode()).hexdigest()[:8]
        base = title.lower().replace(" ", "-").replace("/", "-")[:40]
        return f"{base}-{hash_suffix}"
    
    def _create_item_dir(self, item_id: str) -> Path:
        """Create directory structure for a research item"""
        item_dir = self.research_dir / item_id
        item_dir.mkdir(parents=True, exist_ok=True)
        return item_dir
    
    def _save_metadata(self, metadata: ResearchMetadata):
        """Save metadata.json in item directory"""
        metadata_path = self.research_dir / metadata.id / "metadata.json"
        metadata_path.write_text(metadata.to_json(), encoding='utf-8')
    
    def _load_metadata(self, item_id: str) -> Optional[ResearchMetadata]:
        """Load metadata.json from item directory"""
        metadata_path = self.research_dir / item_id / "metadata.json"
        if metadata_path.exists():
            return ResearchMetadata.load(metadata_path)
        return None
    
    def is_processed(self, item_id: str) -> bool:
        """Check if item was already processed"""
        return item_id in self.processed_items
    
    def mark_processed(self, item_id: str, project_slug: Optional[str] = None):
        """Mark item as processed"""
        self.processed_items.add(item_id)
        metadata = self._load_metadata(item_id)
        if metadata:
            metadata.status = ResearchStatus.PROCESSED
            metadata.processed_at = datetime.now(timezone.utc).isoformat()
            if project_slug:
                metadata.project_slug = project_slug
            self._save_metadata(metadata)
        self._save_processed_log()
    
    def mark_failed(self, item_id: str, error: str):
        """Mark item as failed"""
        metadata = self._load_metadata(item_id)
        if metadata:
            metadata.status = ResearchStatus.FAILED
            metadata.error_message = error
            self._save_metadata(metadata)
    
    @abstractmethod
    def collect(self) -> List[ResearchMetadata]:
        """
        Main collection logic.
        Returns list of ResearchMetadata for newly collected items.
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """Run collector and return summary"""
        print(f"[{datetime.now()}] Starting {self.source.value} collector...")
        
        try:
            new_items = self.collect()
            
            # Filter out already processed
            pending_items = [item for item in new_items if not self.is_processed(item.id)]
            
            print(f"  Collected: {len(new_items)} items")
            print(f"  Pending: {len(pending_items)} items")
            
            return {
                "source": self.source.value,
                "collected": len(new_items),
                "pending": len(pending_items),
                "items": [item.id for item in pending_items],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            print(f"  ❌ Collector failed: {e}")
            return {
                "source": self.source.value,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


def discover_pending_items(repo_root: Optional[Path] = None) -> List[ResearchMetadata]:
    """Discover all pending research items across all sources"""
    root = repo_root or Path.cwd().resolve()
    research_root = root / ".work" / "research"
    
    pending = []
    for source_dir in research_root.iterdir():
        if not source_dir.is_dir() or source_dir.name.endswith("_processed.json"):
            continue
        
        for item_dir in source_dir.iterdir():
            if not item_dir.is_dir():
                continue
            
            metadata_path = item_dir / "metadata.json"
            if metadata_path.exists():
                try:
                    metadata = ResearchMetadata.load(metadata_path)
                    if metadata.status == ResearchStatus.PENDING:
                        pending.append(metadata)
                except Exception as e:
                    print(f"  ⚠️ Failed to load {metadata_path}: {e}")
    
    return pending