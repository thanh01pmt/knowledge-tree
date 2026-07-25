import csv, json, re
from pathlib import Path

out_dir = Path("projects/swift-associate/output")
hlo_dir = Path("projects/swift-associate/.work/hlo")

with open(hlo_dir / "ulos.json") as f: ulos_raw = json.load(f)
with open(hlo_dir / "cios.json") as f: cios_raw = json.load(f)

# Build lookup: ULO code -> concept_codes (from hlo/ulos.json)
ulo_cc = {}
for u in ulos_raw:
    cc = u.get("concept_codes", [])
    if isinstance(cc, list): cc = ", ".join(cc)
    ulo_cc[u["code"]] = cc

# Build lookup: CIO code -> concept from CIO pattern "CIO-<CONCEPT_CODE>-<SLUG>"
cio_concept = {}
cio_parent_ulo = {}
for c in cios_raw:
    code = c["code"]
    # Extract concept: everything between CIO- and the last -SLUG
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-[A-Z]", code)
    if m:
        cio_concept[code] = m.group(1)
    cio_parent_ulo[code] = c.get("parent_ulo_code", "")

# Read TSV
with open(out_dir / "learning-objectives.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    rows = list(reader)

fixed = 0
for row in rows:
    code = row.get("code", "")
    lo_type = row.get("lo_type", "")
    if row.get("concept_codes", "").strip():
        continue  # Already filled

    if lo_type == "UNIVERSAL":
        # Extract concept from ULO pattern: ULO-<CONCEPT>-NN
        m = re.match(r"ULO-([A-Z][A-Z0-9_]+)-\d+$", code)
        if m:
            row["concept_codes"] = m.group(1)
            fixed += 1

    elif lo_type == "CONCEPTUAL_IMPL":
        # 1. Try from parent ULO concept_codes
        parent_ulo = row.get("parent_lo_code", "").strip()
        cc = ulo_cc.get(parent_ulo, "")
        if not cc:
            # 2. Try from CIO code pattern: CIO-<CONCEPT>-SLUG
            concept = cio_concept.get(code, "")
            if concept:
                cc = concept
        if cc:
            row["concept_codes"] = cc
            fixed += 1

    elif lo_type == "SPECIFIC_IMPL":
        # SIO: get concept from parent CIO code pattern
        parent_cio = row.get("parent_lo_code", "").strip()
        parts = [p.strip() for p in parent_cio.replace(";", ",").split(",") if p.strip()]
        concepts = []
        for pc in parts:
            c = cio_concept.get(pc, "")
            if c: concepts.append(c)
            else:
                # Try parent_ulo of CIO
                pulo = cio_parent_ulo.get(pc, "")
                cc = ulo_cc.get(pulo, "")
                if cc: concepts.append(cc)
        if concepts:
            row["concept_codes"] = ", ".join(dict.fromkeys(concepts))
            fixed += 1

print(f"Filled concept_codes for {fixed} LOs")

with open(out_dir / "learning-objectives.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print("Done!")
