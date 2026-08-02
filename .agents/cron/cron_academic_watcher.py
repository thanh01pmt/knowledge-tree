#!/usr/bin/env python3
import os
import shutil
import time
import subprocess
from pathlib import Path
import re
import datetime

INPUTS_DIR = Path("inputs/academic")
PROCESSED_FILE = INPUTS_DIR / ".processed"
PROJECTS_DIR = Path("projects")

def get_processed_files():
    if not PROCESSED_FILE.exists():
        return set()
    return set(PROCESSED_FILE.read_text(encoding="utf-8").splitlines())

def mark_processed(filename):
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(filename + "\n")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def main():
    if not INPUTS_DIR.exists():
        INPUTS_DIR.mkdir(parents=True)
    
    processed = get_processed_files()
    
    # Supported formats
    extensions = {'.pdf', '.md', '.txt', '.csv'}
    
    new_files_found = False
    for filepath in INPUTS_DIR.iterdir():
        if filepath.is_file() and filepath.suffix.lower() in extensions:
            if filepath.name not in processed:
                new_files_found = True
                print(f"Found new academic input: {filepath.name}")
                
                # Create a project slug
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                base_slug = slugify(filepath.stem)
                project_slug = f"academic-{base_slug}-{timestamp}"
                
                print(f"Scaffolding project: {project_slug}")
                # Run scaffold_tree.py
                scaffold_script = Path(".agents/skills/tree-validator/scripts/scaffold_tree.py")
                subprocess.run([sys.executable, str(scaffold_script), project_slug], check=True)
                
                # Copy file to project context
                context_dir = PROJECTS_DIR / project_slug / "context"
                shutil.copy2(filepath, context_dir / filepath.name)
                
                # Mark as processed
                mark_processed(filepath.name)
                
                print(f"✅ Success! Data moved to {context_dir}")
                print(f"👉 Next steps: User must run `/set-project {project_slug}` then `/run-pipeline` to align this syllabus.")
                print("-" * 40)
                
    if not new_files_found:
        print("No new academic files found.")

if __name__ == "__main__":
    import sys
    main()
