import sys
import json
import csv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.append(".agents/skills/learning-objective-generator/scripts")
import llm_generate_hierarchical_lo as gen_lo
from openai import OpenAI

client = OpenAI()
model = "deepseek-v4-flash:cloud"

# Load Master Tree
master_json_path = Path(".agents/skills/taxonomy-mapper/resources/master_tree.json")
with open(master_json_path, "r", encoding="utf-8") as f:
    master = json.load(f)

# Load code to row mapping
code_to_lvl = {}
code_to_row = {}
for lvl in ["fields", "subjects", "categories", "topics", "concepts"]:
    for row in master.get(lvl, []):
        code_to_lvl[row["code"]] = lvl
        code_to_row[row["code"]] = row

gap_c_codes = [
    "ARRAY_OPERATIONS",
    "LOCAL_VIEW_STATE",
    "POLYGON_MESH",
    "STATE_PROPERTY_WRAPPER",
    "WHILE_LOOP",
    "PROJECT_ASSETS_MANAGEMENT",
    "SYNTAX_VS_RUNTIME_ERRORS",
    "REFERENCE_TYPE_DECLARATION",
    "IMPLICIT_EXPLICIT_ANIMATION",
    "STACK_OPERATIONS",
    "USER_PERSONAS",
    "DECLARATIVE_UI_PARADIGM",
    "UI_MODIFIERS_CONCEPT"
]

# We will drop POLYGON_MESH (3D), USER_PERSONAS (UX), STACK_OPERATIONS (advanced DS not usually in Associate) 
# and keep the ones highly relevant to Swift Associate.
relevant_codes = [
    "ARRAY_OPERATIONS",
    "LOCAL_VIEW_STATE",
    "STATE_PROPERTY_WRAPPER",
    "WHILE_LOOP",
    "PROJECT_ASSETS_MANAGEMENT",
    "SYNTAX_VS_RUNTIME_ERRORS",
    "REFERENCE_TYPE_DECLARATION",
    "IMPLICIT_EXPLICIT_ANIMATION",
    "DECLARATIVE_UI_PARADIGM",
    "UI_MODIFIERS_CONCEPT"
]

def collect_ancestors(code, result):
    row = code_to_row.get(code)
    if not row: return
    actual_lvl = code_to_lvl[code]
    result.setdefault(actual_lvl, {})
    if code in result[actual_lvl]: return
    result[actual_lvl][code] = dict(row)

    parent_keys = {
        "concepts": "topic_codes",
        "topics": "category_codes",
        "categories": "subject_codes",
        "subjects": "field_codes"
    }
    pkey = parent_keys.get(actual_lvl)
    if pkey and row.get(pkey):
        p_codes = [c.strip() for c in row[pkey].replace(";", ",").split(",") if c.strip()]
        for pc in p_codes:
            collect_ancestors(pc, result)

# Collect all items for the new concepts
new_items = {}
for code in relevant_codes:
    collect_ancestors(code, new_items)

# Append to project TSVs
out_dir = Path("projects/swift-associate/output")
levels = ["fields", "subjects", "categories", "topics", "concepts"]
for lvl in levels:
    tsv_path = out_dir / f"{lvl}.tsv"
    existing_codes = set()
    rows = []
    if tsv_path.exists():
        with open(tsv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            fieldnames = reader.fieldnames
            rows = list(reader)
            existing_codes = {r["code"] for r in rows}
    
    # Add new items
    added = False
    for code, row in new_items.get(lvl, {}).items():
        if code not in existing_codes:
            # Ensure row has all fieldnames, default to empty
            clean_row = {k: row.get(k, "") for k in fieldnames}
            rows.append(clean_row)
            added = True
            print(f"Added {lvl[:-1]}: {code}")

    if added:
        with open(tsv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

# Generate LOs for the new concepts
hlo_dir = Path("projects/swift-associate/.work/hlo")
with open(out_dir / "concepts.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]

missing_concepts = [{"code": c[0], "name": c[1], "description": c[2]} for c in concepts if c[0] in relevant_codes]

print(f"Generating LOs for {len(missing_concepts)} new Master concepts")

master_ulos_db = gen_lo.load_master_ulos()
to_generate_master = [c for c in missing_concepts if c["code"] not in master_ulos_db]

if to_generate_master:
    gen_lo.generate_master_ulos_for_missing_concepts(client, to_generate_master, model)
    master_ulos_db = gen_lo.load_master_ulos()

new_ulos = []
for c in missing_concepts:
    if c["code"] in master_ulos_db:
        new_ulos.extend(master_ulos_db[c["code"]])

print(f"Selected {len(new_ulos)} ULOs")
new_cios = gen_lo.generate_cios(client, new_ulos, "", model, hlo_dir, batch_size=5)
new_sios = gen_lo.generate_sios(client, new_cios, "Swift", "", "", model, hlo_dir, batch_size=5)

for s in new_sios:
    if "code" in s and isinstance(s["code"], str):
        s["code"] = s["code"].upper()

with open(hlo_dir / "ulos.json", "r") as f: ulos = json.load(f)
with open(hlo_dir / "cios.json", "r") as f: cios = json.load(f)
with open(hlo_dir / "sios.json", "r") as f: sios = json.load(f)

existing_ulo_codes = {u["code"] for u in ulos}
existing_cio_codes = {c["code"] for c in cios}
existing_sio_codes = {s["code"] for s in sios}

ulos.extend([u for u in new_ulos if u["code"] not in existing_ulo_codes])
cios.extend([c for c in new_cios if c["code"] not in existing_cio_codes])
sios.extend([s for s in new_sios if s["code"] not in existing_sio_codes])

with open(hlo_dir / "ulos.json", "w") as f: json.dump(ulos, f, indent=2, ensure_ascii=False)
with open(hlo_dir / "cios.json", "w") as f: json.dump(cios, f, indent=2, ensure_ascii=False)
with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Done fixing Gap C!")
