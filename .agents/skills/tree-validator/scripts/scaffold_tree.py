#!/usr/bin/env python3
"""
scaffold_tree.py — Tạo cấu trúc thư mục và file TSV trống cho project mới.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

HEADERS = {
    "fields.tsv": ["code", "name", "description", "display_order", "keywords", "cs2023_ka_mapping", "metadata", "sequence_order"],
    "subjects.tsv": ["code", "name", "description", "field_codes", "keywords", "cs2023_ka_mapping", "metadata", "sequence_order"],
    "categories.tsv": ["code", "name", "description", "subject_codes", "keywords", "cs2023_ka_mapping", "metadata", "sequence_order"],
    "topics.tsv": ["code", "name", "description", "category_codes", "keywords", "cs2023_ka_mapping", "metadata", "sequence_order"],
    "concepts.tsv": ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata", "sequence_order"],
    "learning-objectives.tsv": ["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes", "bloom_level", "knowledge_dimension", "assessment_approach"]
}

# Safe project slug: lowercase letters, digits, hyphens, underscores only.
# Prevents path traversal (../, /, ..) and command injection.
SAFE_SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*$')


def validate_slug(slug: str) -> str:
    """Validate project slug against path traversal and unsafe characters.
    Returns the slug if safe, raises ValueError otherwise."""
    if not slug:
        raise ValueError("Project slug cannot be empty.")
    if not SAFE_SLUG_RE.match(slug):
        raise ValueError(
            f"Invalid project slug '{slug}'. "
            "Only lowercase letters, digits, hyphens, and underscores are allowed "
            "(must start with a letter or digit). No path separators or '..'."
        )
    if ".." in slug or "/" in slug or "\\" in slug:
        raise ValueError(f"Project slug '{slug}' contains path traversal characters.")
    return slug

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()

def update_status_yaml(repo_root: Path, slug: str):
    status_path = repo_root / "status.yaml"
    
    lines = []
    if status_path.exists():
        lines = status_path.read_text(encoding="utf-8").splitlines()
    
    new_lines = []
    found = False
    for line in lines:
        if line.startswith("active_project:"):
            new_lines.append(f"active_project: {slug}")
            found = True
        else:
            new_lines.append(line)
            
    if not found:
        new_lines.append(f"active_project: {slug}")
        
    status_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Tạo cấu trúc taxonomy trống cho project mới.")
    parser.add_argument("project", help="Tên (slug) của project cần tạo")
    args = parser.parse_args()

    slug = args.project
    try:
        validate_slug(slug)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    repo_root = find_repo_root(Path.cwd())
    project_dir = repo_root / "projects" / slug

    # Defense-in-depth: verify resolved path stays inside repo
    project_dir_resolved = project_dir.resolve()
    repo_root_resolved = repo_root.resolve()
    if not project_dir_resolved.is_relative_to(repo_root_resolved):
        print(f"❌ Error: Resolved project path escapes repository root.")
        sys.exit(1)
    
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "context").mkdir(exist_ok=True)
    (project_dir / ".work").mkdir(exist_ok=True)
    output_dir = project_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    for filename, headers in HEADERS.items():
        filepath = output_dir / filename
        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                writer.writerow(headers)
            print(f"Created: {filepath.relative_to(repo_root)}")
        else:
            print(f"Skipped (exists): {filepath.relative_to(repo_root)}")
            
    # Create project_meta.yaml
    meta_path = project_dir / "project_meta.yaml"
    if not meta_path.exists():
        import datetime
        now = datetime.datetime.utcnow().isoformat() + "Z"
        # Determine type based on slug
        proj_type = "cron_trend_research" if "trend" in slug else "cron_academic_alignment" if "academic" in slug else "standard_project"
        meta_content = f"""type: "{proj_type}"
status: 
  generated: false
  merged_to_master: false
  synced_to_supabase: false
timestamps:
  created_at: {now}
  merged_at: null
  synced_at: null
reports:
  diff_changelog: "output/changelog.md"
"""
        meta_path.write_text(meta_content, encoding="utf-8")
        print(f"Created: {meta_path.relative_to(repo_root)}")

    update_status_yaml(repo_root, slug)
    print(f"\nProject '{slug}' scaffolded successfully and set as active_project in status.yaml.")

if __name__ == "__main__":
    main()
