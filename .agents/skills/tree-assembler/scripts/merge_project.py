#!/usr/bin/env python3
import sys
import csv
import argparse
from pathlib import Path
import datetime
import yaml

def load_master_sections(master_path):
    sections = {
        "fields": [],
        "subjects": [],
        "categories": [],
        "topics": [],
        "concepts": []
    }
    master_codes = set()
    
    if not master_path.exists():
        return sections, master_codes
        
    current_section = None
    with open(master_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith("Bảng 1: Lĩnh vực"):
                current_section = "fields"
            elif line_str.startswith("Bảng 2: Chủ đề (subjects)"):
                current_section = "subjects"
            elif line_str.startswith("Bảng 3: Hạng mục"):
                current_section = "categories"
            elif line_str.startswith("Bảng 4: Chủ đề con"):
                current_section = "topics"
            elif line_str.startswith("Bảng 5: Khái niệm"):
                current_section = "concepts"
                
            if current_section:
                sections[current_section].append(line)
                parts = line.split('\t')
                if len(parts) > 0 and parts[0].strip() and not parts[0].startswith("Bảng") and not parts[0].startswith("code") and not parts[0].startswith("Đây là"):
                    master_codes.add(parts[0].strip())
                    
    return sections, master_codes

def get_new_rows_from_tsv(tsv_path, master_codes):
    new_rows = []
    if not tsv_path.exists():
        return new_rows
        
    with open(tsv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None) # skip header
        for row in reader:
            if not row or not row[0].strip():
                continue
            code = row[0].strip()
            if code not in master_codes:
                new_rows.append(row)
                master_codes.add(code)
    return new_rows

def write_master(master_path, sections):
    with open(master_path, "w", encoding="utf-8", newline="") as f:
        for section in ["fields", "subjects", "categories", "topics", "concepts"]:
            for line in sections[section]:
                f.write(line if line.endswith('\n') else line + '\n')

def format_row(row):
    return "\t".join(row) + "\n"

def merge_project(project_slug):
    repo_root = Path.cwd()
    project_dir = repo_root / "projects" / project_slug
    output_dir = project_dir / "output"
    meta_path = project_dir / "project_meta.yaml"
    master_path = repo_root / "services/python-api/general-context/mlo-knowlege-tree.tsv"

    if not project_dir.exists():
        print(f"Error: Project '{project_slug}' not found.")
        sys.exit(1)

    sections, master_codes = load_master_sections(master_path)
    
    file_to_section = {
        "fields.tsv": "fields",
        "subjects.tsv": "subjects",
        "categories.tsv": "categories",
        "topics.tsv": "topics",
        "concepts.tsv": "concepts"
    }
    
    total_new = 0
    changelog_lines = [f"# Merge Changelog for {project_slug}", "", f"Merged at: {datetime.datetime.utcnow().isoformat()}Z", ""]
    
    for tsv_name, section_key in file_to_section.items():
        proj_tsv = output_dir / tsv_name
        new_rows = get_new_rows_from_tsv(proj_tsv, master_codes)
        
        if new_rows:
            changelog_lines.append(f"## Added to {section_key}")
            for r in new_rows:
                # Add to the appropriate section in master
                sections[section_key].append(format_row(r))
                changelog_lines.append(f"- **{r[0]}**: {r[1]}")
                total_new += 1
            changelog_lines.append("")
            
            # Ensure there's a blank line at the end of the section
            sections[section_key].append("\t\t\t\t\t\t\n")

    if total_new > 0:
        write_master(master_path, sections)
        changelog_path = output_dir / "changelog.md"
        changelog_path.write_text("\n".join(changelog_lines), encoding="utf-8")
        print(f"Merged {total_new} new nodes. Changelog written to {changelog_path}")
    else:
        print("No new nodes to merge. Everything is already in Master Tree.")
        
    # Update project_meta.yaml
    if meta_path.exists():
        meta_data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        if "status" in meta_data:
            meta_data["status"]["merged_to_master"] = True
        if "timestamps" in meta_data:
            meta_data["timestamps"]["merged_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        meta_path.write_text(yaml.dump(meta_data, sort_keys=False), encoding="utf-8")
        print(f"Updated {meta_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="Project slug to merge")
    args = parser.parse_args()
    merge_project(args.project)
