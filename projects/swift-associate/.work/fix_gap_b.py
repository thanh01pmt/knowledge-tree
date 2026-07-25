import sys
import json
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

with open(hlo_dir / "cios.json", "r") as f:
    cios = json.load(f)

# The missing ones
missing_codes = [
    "CIO-VISUAL_DESIGN-04-01", "CIO-VISUAL_DESIGN-04-02", 
    "CIO-SECURITY_CHALLENGES-01-01", "CIO-SECURITY_CHALLENGES-01-02", "CIO-SECURITY_CHALLENGES-02-01"
]

missing_cios = [c for c in cios if c["code"] in missing_codes]
if not missing_cios:
    print("No missing cios found!")
    sys.exit(0)

matrix = ""
tech = "Swift"
keywords_text = ""
new_sios = gen_lo.generate_sios(client, missing_cios, tech, matrix, keywords_text, model, hlo_dir, batch_size=5)

for s in new_sios:
    if "code" in s and isinstance(s["code"], str):
        s["code"] = s["code"].upper()

with open(hlo_dir / "sios.json", "r") as f: sios = json.load(f)
existing_sio_codes = {s["code"] for s in sios}
sios.extend([s for s in new_sios if s["code"] not in existing_sio_codes])
with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

with open(hlo_dir / "ulos.json", "r") as f: ulos = json.load(f)
with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]

gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Done fixing Gap B!")
