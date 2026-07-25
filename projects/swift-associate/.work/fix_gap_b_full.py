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

with open(hlo_dir / "cios.json", "r") as f: cios = json.load(f)
with open(hlo_dir / "sios.json", "r") as f: sios = json.load(f)

# Fix Marr test violations directly in cios.json
for c in cios:
    if c["code"] == "CIO-VISUAL_DESIGN-04-01":
        c["name"] = c["name"].replace("interface design", "visual layout")
        c["description_vi"] = c["description_vi"].replace("giao diện", "bố cục trực quan")
    if c["code"] == "CIO-OBJECT_INSTANTIATION_03-01":
        c["description_vi"] = c["description_vi"].replace("class method", "type method")

with open(hlo_dir / "cios.json", "w") as f: json.dump(cios, f, indent=2, ensure_ascii=False)

sio_parents = set()
for s in sios:
    parent = s.get("parent_lo_code", "")
    if parent:
        for code in parent.replace(";", ",").replace("|", ",").split(","):
            sio_parents.add(code.strip())

missing_cios = [c for c in cios if c["code"] not in sio_parents]

if missing_cios:
    print(f"Found {len(missing_cios)} CIOs without SIOs. Generating...")
    new_sios = gen_lo.generate_sios(client, missing_cios, "Swift", "", "", model, hlo_dir, batch_size=5)
    for s in new_sios:
        if "code" in s and isinstance(s["code"], str):
            s["code"] = s["code"].upper()
    sios.extend(new_sios)
    with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)
else:
    print("No missing CIOs found!")

with open(hlo_dir / "ulos.json", "r") as f: ulos = json.load(f)
with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]

gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Done fixing Gap B and D!")
