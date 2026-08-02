#!/usr/bin/env python3
import sys
import subprocess
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
model = os.getenv("ATE_MODEL", "gpt-4o")

# Add shared paths
repo_root = Path.cwd()
while not (repo_root / ".agents").exists() and repo_root != repo_root.parent:
    repo_root = repo_root.parent
sys.path.append(str(repo_root / ".agents/skills/keyword-extractor/scripts"))
from llm_call import llm_chat_json

sys.path.append(str(repo_root / ".agents/skills/tree-validator/scripts"))
from master_tree_parser import parse_master_tsv, SECTIONS

MASTER_TSV = repo_root / "services/python-api/general-context/mlo-knowlege-tree.tsv"
VALIDATOR_SCRIPT = repo_root / ".agents/skills/tree-validator/scripts/validate_master_tree.py"

SYSTEM_PROMPT = """You are an expert taxonomy engineer. 
Your task is to fix errors in a Master Knowledge Tree TSV file based on validation errors.
You will receive:
1. The error log (containing BROKEN_REFERENCE, LEVEL_SKIP, CROSS_LEVEL_COLLISION, T6_VIOLATION, EMPTY_PARENT).
2. The relevant row data that needs fixing (JSON format).

Return a JSON array of patch objects to fix the errors. Each patch object MUST have:
{
  "action": "update" or "rename",
  "level": "fields" | "subjects" | "categories" | "topics" | "concepts",
  "code": "<The original code of the row>",
  "field": "<The field to update. Required if action is update>",
  "new_value": "<The new value. Required if action is update>",
  "new_code": "<The new code. Required if action is rename>"
}

Guidelines for fixing:
- T6_VIOLATION: Rewrite the offending field (name, description, keywords) to be technology-neutral. If the code itself contains a tech name (e.g. REACT_JS), output an action="rename" to change it (e.g. COMPONENT_UI).
- BROKEN_REFERENCE / LEVEL_SKIP: Provide the correct parent code in the respective parent field (e.g., category_codes).
- EMPTY_PARENT: Infer the most logical parent code from the name/description and update the parent field.
- For "update", the `new_value` will completely replace the current value of the field.
"""

def get_validation_errors():
    try:
        subprocess.run([sys.executable, str(VALIDATOR_SCRIPT)], capture_output=True, text=True, check=True)
        return False, "", ""
    except subprocess.CalledProcessError as e:
        return True, e.stdout, e.stderr

def apply_patches(patches, tables):
    # Prepare a cascade mapping if there are renames
    code_renames = {}
    for p in patches:
        if p.get("action") == "rename":
            code_renames[p["code"]] = p["new_code"]
    
    # 1. Apply updates and basic renames
    for p in patches:
        level = p.get("level")
        code = p.get("code")
        action = p.get("action")
        
        if level not in tables: continue
        
        for row in tables[level]:
            if row["code"] == code:
                if action == "update":
                    field = p["field"]
                    row[field] = p["new_value"]
                    print(f"  📝 [UPDATE] {level}/{code}: {field} -> {p['new_value']}")
                elif action == "rename":
                    new_code = p["new_code"]
                    row["code"] = new_code
                    print(f"  📝 [RENAME] {level}: {code} -> {new_code}")

    # 2. Cascade Renames
    if code_renames:
        for section_name in SECTIONS.values():
            for row in tables[section_name]:
                for field in ["field_codes", "subject_codes", "category_codes", "topic_codes", "prerequisite_concept_codes"]:
                    if field in row:
                        val = row[field]
                        for old_c, new_c in code_renames.items():
                            val = val.replace(f",{old_c},", f",{new_c},")
                            val = val.replace(f"{old_c},", f"{new_c},")
                            val = val.replace(f",{old_c}", f",{new_c}")
                            if val == old_c:
                                val = new_c
                        row[field] = val

def write_tsv(tables):
    lines = []
    for level, section_name in SECTIONS.items():
        lines.append(f"{level}\n")
        if not tables[section_name]:
            continue
        headers = list(tables[section_name][0].keys())
        lines.append("\t".join(headers) + "\n")
        for row in tables[section_name]:
            lines.append("\t".join(row.get(h, "") for h in headers) + "\n")
        lines.append("\n")
    
    with open(MASTER_TSV, "w", encoding="utf-8") as f:
        f.writelines(lines)

def heal_once(attempt):
    print(f"[{attempt}/3] Running validation...")
    has_error, stdout, stderr = get_validation_errors()
    
    if not has_error:
        print("✅ Validation passed. Tree is healthy.")
        return True
        
    print("❌ Validation failed. Analyzing errors...")
    
    # Extract affected codes from stdout
    affected_codes = set()
    for line in stdout.splitlines():
        if "[T6_VIOLATION]" in line or "[BROKEN_REFERENCE]" in line or "[LEVEL_SKIP]" in line or "[EMPTY_PARENT]" in line or "[CROSS_LEVEL_COLLISION]" in line:
            # Extract code (e.g. concepts/MY_CODE:)
            parts = line.split(":")
            if len(parts) > 1:
                prefix = parts[0].strip().split()[-1] # concepts/MY_CODE
                if "/" in prefix:
                    affected_codes.add(prefix.split("/")[1])
    
    if not affected_codes:
        print("⚠️ Could not parse affected codes. Manual intervention required.")
        return False
        
    tables = parse_master_tsv(MASTER_TSV)
    
    # Build context
    context = []
    valid_codes = {}
    for section_name in SECTIONS.values():
        valid_codes[section_name] = [row["code"] for row in tables[section_name]]
        for row in tables[section_name]:
            if row["code"] in affected_codes:
                context.append({"level": section_name, "row": row})
                
    prompt = f"Validation Errors:\n{stdout}\n\nAffected Rows:\n{json.dumps(context, indent=2)}\n\nValid Codes per Level:\n{json.dumps(valid_codes, indent=2)}\n\nPlease provide JSON patches to fix these errors."
    
    print(f"🤖 Calling LLM to heal {len(affected_codes)} affected codes...")
    response = llm_chat_json(client, model, SYSTEM_PROMPT, prompt, max_retries=2)
    
    if not response:
        print("❌ LLM failed to return valid JSON.")
        return False
        
    print(f"🩹 Applying {len(response)} patches...")
    apply_patches(response, tables)
    write_tsv(tables)
    
    return False

def main():
    print("🏥 Starting Auto-Heal Protocol...")
    for attempt in range(1, 4):
        if heal_once(attempt):
            sys.exit(0)
            
    print("❌ Auto-Heal exhausted 3 retries and failed.")
    sys.exit(1)

if __name__ == "__main__":
    main()
