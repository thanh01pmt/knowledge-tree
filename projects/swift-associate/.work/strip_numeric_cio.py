import json
import re
from pathlib import Path

hlo_dir = Path("projects/swift-associate/.work/hlo")
out_dir = Path("projects/swift-associate/output")

with open(hlo_dir / "cios.json") as f: cios = json.load(f)
with open(hlo_dir / "sios.json") as f: sios = json.load(f)
with open(hlo_dir / "ulos.json") as f: ulos = json.load(f)

# Build mapping: old -> new (strip -NN- from CIO codes)
cio_mapping = {}
for c in cios:
    old = c["code"]
    new = re.sub(r"^(CIO-[^-]+-)\d{2,}-(.+)$", r"\1\2", old)
    if new != old:
        cio_mapping[old] = new

# Handle duplicates: if 2 CIOs have same new code, keep distinct by appending counter
seen = {}
for old, new in cio_mapping.items():
    if new in seen.values():
        # Find all that map to same new
        pass  # Just detect, let's check

# Apply to CIOs
for c in cios:
    if c["code"] in cio_mapping:
        c["code"] = cio_mapping[c["code"]]

# Apply to SIOs parent_cio_code and parent_lo_code  
for s in sios:
    pcc = s.get("parent_cio_code", "")
    if pcc in cio_mapping:
        s["parent_cio_code"] = cio_mapping[pcc]
    plo = s.get("parent_lo_code", "")
    if plo:
        new_parts = []
        for p in plo.replace(";", ",").split(","):
            p = p.strip()
            new_parts.append(cio_mapping.get(p, p))
        s["parent_lo_code"] = ", ".join(new_parts)

# Check for duplicate codes
codes = [c["code"] for c in cios]
dupes = [c for c in codes if codes.count(c) > 1]
if dupes:
    print(f"WARNING: Duplicate codes after migration: {set(dupes)}")
else:
    print(f"No duplicates. OK.")

print(f"Renamed {len(cio_mapping)} CIO codes")
print("Sample codes after fix:")
for c in cios[:5]:
    print(f"  {c['code']}")

with open(hlo_dir / "cios.json", "w") as f: json.dump(cios, f, indent=2, ensure_ascii=False)
with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

import sys
sys.path.append(".agents/skills/learning-objective-generator/scripts")
import llm_generate_hierarchical_lo as gen_lo
with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]
gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Done! Rebuilt learning-objectives.tsv")
