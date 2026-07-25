import sys
import json
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.append(".agents/skills/learning-objective-generator/scripts")
import llm_generate_hierarchical_lo as gen_lo
from openai import OpenAI

client = OpenAI()
model = "deepseek-v4-flash:cloud"

hlo_dir = Path("projects/swift-associate/.work/hlo")
out_dir = Path("projects/swift-associate/output")

# Restore backups first to be safe
shutil.copy(hlo_dir / "ulos_backup.json", hlo_dir / "ulos.json")
shutil.copy(hlo_dir / "cios_backup.json", hlo_dir / "cios.json")
shutil.copy(hlo_dir / "sios_backup.json", hlo_dir / "sios.json")

missing_codes = [
    "VIEW_CONCEPT", "DATA_TYPES", "CONTROL_FLOW", "TYPE_SYSTEM",
    "VISUAL_DESIGN", "SECURITY_CHALLENGES", "DEBUGGING", 
    "OBJECT_INSTANTIATION", "EVENT_HANDLERS_CONCEPT", 
    "OBJECT_PROPERTIES", "RETURN_VALUES_AND_SCOPE"
]

with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]
missing_concepts = [{"code": c[0], "name": c[1], "description": c[2]} for c in concepts if c[0] in missing_codes]

master_ulos_db = gen_lo.load_master_ulos()
to_generate_master = [c for c in missing_concepts if c["code"] not in master_ulos_db]

if to_generate_master:
    gen_lo.generate_master_ulos_for_missing_concepts(client, to_generate_master, model)
    master_ulos_db = gen_lo.load_master_ulos()

new_ulos = []
for c in missing_concepts:
    if c["code"] in master_ulos_db:
        new_ulos.extend(master_ulos_db[c["code"]])

print(f"Selected {len(new_ulos)} new ULOs")

matrix = ""
tech = "Swift"
keywords_text = ""

# Temporarily copy backups so functions don't overwrite them
new_cios = gen_lo.generate_cios(client, new_ulos, matrix, model, hlo_dir, batch_size=5)

new_sios = gen_lo.generate_sios(client, new_cios, tech, matrix, keywords_text, model, hlo_dir, batch_size=5)

for s in new_sios:
    if "code" in s and isinstance(s["code"], str):
        s["code"] = s["code"].upper()

# Reload original files from backups
with open(hlo_dir / "ulos_backup.json", "r") as f: ulos = json.load(f)
with open(hlo_dir / "cios_backup.json", "r") as f: cios = json.load(f)
with open(hlo_dir / "sios_backup.json", "r") as f: sios = json.load(f)

existing_ulo_codes = {u["code"] for u in ulos}
existing_cio_codes = {c["code"] for c in cios}
existing_sio_codes = {s["code"] for s in sios}

ulos.extend([u for u in new_ulos if u["code"] not in existing_ulo_codes])
cios.extend([c for c in new_cios if c["code"] not in existing_cio_codes])
sios.extend([s for s in new_sios if s["code"] not in existing_sio_codes])

with open(hlo_dir / "ulos.json", "w") as f: json.dump(ulos, f, indent=2, ensure_ascii=False)
with open(hlo_dir / "cios.json", "w") as f: json.dump(cios, f, indent=2, ensure_ascii=False)
with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

print("Running merge...")
gen_lo.merge_to_tsv(ulos, cios, sios, missing_concepts + [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Done filling gap A!")
