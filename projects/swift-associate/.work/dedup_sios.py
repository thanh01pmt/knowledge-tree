import json, re
from pathlib import Path
from collections import defaultdict

hlo_dir = Path("projects/swift-associate/.work/hlo")
out_dir = Path("projects/swift-associate/output")

with open(hlo_dir / "sios.json") as f: sios = json.load(f)
with open(hlo_dir / "ulos.json") as f: ulos = json.load(f)
with open(hlo_dir / "cios.json") as f: cios = json.load(f)

# Find duplicates by code
counts = defaultdict(list)
for i, s in enumerate(sios):
    counts[s["code"]].append(i)

dedup_count = 0
for code, indices in counts.items():
    if len(indices) > 1:
        for j, idx in enumerate(indices[1:], 2):
            new_code = f"{code}_{j}"
            sios[idx]["code"] = new_code
            dedup_count += 1

print(f"Deduped {dedup_count} SIO codes")
print(f"All codes unique: {len(set(s['code'] for s in sios)) == len(sios)}")

with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

import sys
sys.path.append(".agents/skills/learning-objective-generator/scripts")
import llm_generate_hierarchical_lo as gen_lo
with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]
gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Done! Rebuilt learning-objectives.tsv")
