import csv, json, re
from pathlib import Path

out_dir = Path("projects/swift-associate/output")
hlo_dir = Path("projects/swift-associate/.work/hlo")

with open(hlo_dir / "cios.json") as f: cios = json.load(f)

# All current CIO codes
current_cio_codes = {c["code"] for c in cios}

# Build a mapping from old_style (CIO-CONCEPT-NN-SLUG / CIO-CONCEPT-NN-NN) to new code
# Strategy: for each old code referenced by SIOs, find the CIO with
# matching CONCEPT and matching numeric index among that CONCEPT's CIOs
#
# Old: CIO-VISUAL_DESIGN-04-01  -> VISUAL_DESIGN concept, was 1st under ULO-04
# New: CIO-VISUAL_DESIGN-EVALUATE_VISUAL_CRITERIA (or similar)
# 
# We'll build a fallback: CIO-CONCEPT-NN-NN -> any CIO with same CONCEPT (first match)
# For same concept, order by appearance in cios list

concept_to_cio = {}
for c in cios:
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", c["code"])
    if m:
        concept = m.group(1)
        concept_to_cio.setdefault(concept, []).append(c["code"])

print("Current CIO concepts:", list(concept_to_cio.keys())[:10])

# Build old->new mapping for broken SIO parent refs
# Old pattern: CIO-CONCEPT-NN-NN or CIO-CONCEPT-NN-SLUG
def find_new_cio(old_code):
    if old_code in current_cio_codes:
        return old_code
    # Try to extract concept and index from old code
    # Pattern: CIO-<CONCEPT>-<NN1>-<NN2>  or  CIO-<CONCEPT>-<NN1>-<SLUG>
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-(\d+)-(\d+|[A-Z_]+)", old_code)
    if m:
        concept = m.group(1)
        idx = int(m.group(2)) - 1  # 1-indexed -> 0-indexed
        if concept in concept_to_cio:
            candidates = concept_to_cio[concept]
            if idx < len(candidates):
                return candidates[idx]
            return candidates[0]  # fallback to first
    return None

# Read TSV
with open(out_dir / "learning-objectives.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    rows = list(reader)

all_codes = {r["code"] for r in rows}

fixed = 0
unfixable = []
for row in rows:
    plo = row.get("parent_lo_code", "").strip()
    if not plo: continue
    parts = [p.strip() for p in plo.replace(";", ",").split(",") if p.strip()]
    new_parts = []
    changed = False
    for p in parts:
        if p in all_codes:
            new_parts.append(p)
        else:
            new_p = find_new_cio(p)
            if new_p:
                new_parts.append(new_p)
                changed = True
            else:
                new_parts.append(p)
                unfixable.append((row["code"], p))
    if changed:
        row["parent_lo_code"] = ", ".join(new_parts)
        fixed += 1

print(f"Fixed parent_lo_code for {fixed} LOs")
if unfixable:
    print(f"Unfixable broken refs ({len(unfixable)}):")
    for child, parent in unfixable[:10]:
        print(f"  {child} -> {parent}")

with open(out_dir / "learning-objectives.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print("Done!")
