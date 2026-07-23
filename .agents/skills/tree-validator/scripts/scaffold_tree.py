#!/usr/bin/env python3
"""
scaffold_tree.py — Tạo cấu trúc thư mục và file TSV trống cho project mới.
"""

import argparse
import csv
from pathlib import Path

HEADERS = {
    "fields.tsv": ["code", "name", "description", "display_order", "keywords", "cs2023_ka_mapping", "metadata"],
    "subjects.tsv": ["code", "name", "description", "field_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "categories.tsv": ["code", "name", "description", "subject_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "topics.tsv": ["code", "name", "description", "category_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "concepts.tsv": ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "learning-objectives.tsv": ["code", "name", "description", "lo_type", "knowledge_dimension_code", "suggested_bloom_levels", "parent_lo_code", "concept_codes"]
}

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
    repo_root = find_repo_root(Path.cwd())
    project_dir = repo_root / "projects" / slug
    
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
            
    update_status_yaml(repo_root, slug)
    print(f"\nProject '{slug}' scaffolded successfully and set as active_project in status.yaml.")

if __name__ == "__main__":
    main()
