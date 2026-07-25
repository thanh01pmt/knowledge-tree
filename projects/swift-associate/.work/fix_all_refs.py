import csv, json, re, sys
from pathlib import Path

sys.path.append(".agents/skills/learning-objective-generator/scripts")
import llm_generate_hierarchical_lo as gen_lo

out_dir = Path("projects/swift-associate/output")
hlo_dir = Path("projects/swift-associate/.work/hlo")

# Load raw JSON (source of truth)
with open(hlo_dir / "ulos.json") as f: ulos = json.load(f)
with open(hlo_dir / "cios.json") as f: cios = json.load(f)
with open(hlo_dir / "sios.json") as f: sios = json.load(f)

# Step 1: Find CIOs whose parent_ulo_code is NOT in ulos.json
ulo_codes = {u["code"] for u in ulos}
missing_ulo_codes = set()
for c in cios:
    pulo = c.get("parent_ulo_code", "")
    if pulo and pulo not in ulo_codes:
        missing_ulo_codes.add(pulo)

print(f"Missing ULOs referenced by CIOs: {len(missing_ulo_codes)}")

# Step 2: Build synthetic ULOs for missing codes (same pattern as existing ULOs)
# Pattern: ULO-<CONCEPT>-NN -> extract concept, create a minimal ULO
# We'll load from master_ulos.json if possible, else construct minimally
master_ulos_path = Path(".agents/skills/learning-objective-generator/scripts/master_ulos.json")
master_ulos_db = {}
if master_ulos_path.exists():
    with open(master_ulos_path) as f:
        master_ulos_db = json.load(f)
    print(f"Loaded {len(master_ulos_db)} master ULO groups")

new_ulos = []
for missing_code in missing_ulo_codes:
    # Check if it's already in master_ulos
    m = re.match(r"ULO-([A-Z][A-Z0-9_]+)-(\d+)$", missing_code)
    if not m:
        print(f"  WARNING: unexpected ULO code pattern: {missing_code}")
        continue
    concept = m.group(1)
    if concept in master_ulos_db:
        # Pull the right ULO from the master DB
        for u in master_ulos_db[concept]:
            if u.get("code") == missing_code:
                new_ulos.append(u)
                break
        else:
            # Not found by exact code, create minimal placeholder
            new_ulos.append({
                "code": missing_code,
                "name": f"Understand {concept.replace('_', ' ').title()}",
                "description": f"Người học có khả năng hiểu và áp dụng {concept.replace('_', ' ').lower()}.",
                "lo_type": "UNIVERSAL",
                "parent_lo_code": "",
                "concept_codes": concept,
                "bloom_level": "UNDERSTAND",
                "knowledge_dimension": "CONCEPTUAL"
            })
    else:
        new_ulos.append({
            "code": missing_code,
            "name": f"Understand {concept.replace('_', ' ').title()}",
            "description": f"Người học có khả năng hiểu và áp dụng {concept.replace('_', ' ').lower()}.",
            "lo_type": "UNIVERSAL",
            "parent_lo_code": "",
            "concept_codes": concept,
            "bloom_level": "UNDERSTAND",
            "knowledge_dimension": "CONCEPTUAL"
        })

print(f"Adding {len(new_ulos)} synthetic ULOs")

# Add new ULOs to ulos list
existing_ulo_codes = {u["code"] for u in ulos}
for u in new_ulos:
    if u["code"] not in existing_ulo_codes:
        ulos.append(u)

# Save updated ulos
with open(hlo_dir / "ulos.json", "w") as f: json.dump(ulos, f, indent=2, ensure_ascii=False)

# Step 3: Rebuild TSV - this will now include all ULOs
with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]
gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Rebuilt learning-objectives.tsv")

# Step 4: Now fix concept_codes for SIOs (parent_cio_code match)
# Build CIO code -> concept map
cio_concept = {}
for c in cios:
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", c["code"])
    if m:
        cio_concept[c["code"]] = m.group(1)

# Build ULO code -> concept_codes
ulo_cc = {}
for u in ulos:
    cc = u.get("concept_codes", "")
    if isinstance(cc, list): cc = ", ".join(cc)
    ulo_cc[u["code"]] = cc

with open(out_dir / "learning-objectives.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    rows = list(reader)

filled = 0
for row in rows:
    code = row.get("code", "")
    lo_type = row.get("lo_type", "")
    if row.get("concept_codes", "").strip():
        continue

    if lo_type == "UNIVERSAL":
        m = re.match(r"ULO-([A-Z][A-Z0-9_]+)-\d+$", code)
        if m:
            row["concept_codes"] = m.group(1)
            filled += 1

    elif lo_type == "CONCEPTUAL_IMPL":
        # Extract concept from CIO code pattern: CIO-<CONCEPT>-<SLUG>
        m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", code)
        if m:
            row["concept_codes"] = m.group(1)
            filled += 1
        else:
            # Fallback: parent ULO
            pulo = row.get("parent_lo_code", "").strip()
            cc = ulo_cc.get(pulo, "")
            if cc:
                row["concept_codes"] = cc
                filled += 1

    elif lo_type == "SPECIFIC_IMPL":
        # Extract concept from parent CIO code pattern
        parent_cio = row.get("parent_lo_code", "").strip()
        parts = [p.strip() for p in parent_cio.replace(";",",").split(",") if p.strip()]
        concepts_set = []
        for pc in parts:
            c = cio_concept.get(pc, "")
            if c and c not in concepts_set:
                concepts_set.append(c)
        if concepts_set:
            row["concept_codes"] = ", ".join(concepts_set)
            filled += 1

print(f"Filled concept_codes for {filled} more LOs")

with open(out_dir / "learning-objectives.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print("Done!")
