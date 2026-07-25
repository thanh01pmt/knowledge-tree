import csv, json, re, sys
from pathlib import Path
from collections import defaultdict

sys.path.append(".agents/skills/learning-objective-generator/scripts")
import llm_generate_hierarchical_lo as gen_lo

out_dir = Path("projects/swift-associate/output")
hlo_dir = Path("projects/swift-associate/.work/hlo")

with open(hlo_dir / "cios.json") as f: cios = json.load(f)
with open(hlo_dir / "ulos.json") as f: ulos = json.load(f)
with open(hlo_dir / "sios.json") as f: sios = json.load(f)

# Current CIO codes
current_cio_codes = {c["code"] for c in cios}

# Get all broken parent_cio_code from sios.json
# These are the old codes like CIO-CONTROL_FLOW-01-01
broken_refs = set()
for s in sios:
    pc = s.get("parent_cio_code", "")
    if pc and pc not in current_cio_codes:
        broken_refs.add(pc)

print(f"Broken parent_cio_code refs in sios.json: {len(broken_refs)}")

# Build reverse map: concept -> list of CIO codes in order
concept_to_cios = defaultdict(list)
for c in cios:
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", c["code"])
    if m:
        concept_to_cios[m.group(1)].append(c["code"])

# Build old->new mapping
# Old pattern: CIO-<CONCEPT>-<ULO_IDX>-<CIO_IDX>
# We map the CIO_IDX (1-indexed) within that CONCEPT to the current CIO list
old_to_new = {}
for old_code in broken_refs:
    # Try CIO-CONCEPT-NN-NN
    m = re.match(r"CIO-([A-Z][A-Z0-9_0-9]+)-(\d+)-(\d+)$", old_code)
    if m:
        concept = m.group(1)
        ulo_idx = int(m.group(2))
        cio_idx = int(m.group(3)) - 1  # 0-indexed
        
        # Total offset: first (ulo_idx-1) * avg_per_ulo CIOs, + cio_idx
        # But we don't know the original ULO grouping...
        # Better approach: treat total sequential order
        # Old scheme: ULO-1: CIOs 01-01, 01-02 | ULO-2: CIOs 02-01, 02-02
        # Calculate sequential index: (ulo_idx-1)*2 + cio_idx  
        candidates = concept_to_cios.get(concept, [])
        if candidates:
            # Try to estimate sequential position
            # Each ULO had typically 1-2 CIOs, so sequential_idx ≈ (ulo_idx-1)*2 + cio_idx
            sequential_idx = (ulo_idx - 1) * 2 + cio_idx
            if sequential_idx < len(candidates):
                new_code = candidates[sequential_idx]
            else:
                new_code = candidates[min(cio_idx, len(candidates)-1)]
            old_to_new[old_code] = new_code
            continue
    
    # Try CIO-CONCEPT-NN-1/2/3 (single digit suffix)
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-(\d+)-(\d)$", old_code)
    if m:
        concept = m.group(1)
        ulo_idx = int(m.group(2))
        cio_idx = int(m.group(3)) - 1
        candidates = concept_to_cios.get(concept, [])
        if candidates:
            sequential_idx = (ulo_idx - 1) * 2 + cio_idx
            new_code = candidates[min(sequential_idx, len(candidates)-1)]
            old_to_new[old_code] = new_code
            continue
    
    # Fallback: map to first CIO of that concept
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", old_code)
    if m:
        concept = m.group(1)
        candidates = concept_to_cios.get(concept, [])
        if candidates:
            old_to_new[old_code] = candidates[0]
            print(f"  Fallback: {old_code} -> {candidates[0]}")

print(f"Built mapping for {len(old_to_new)}/{len(broken_refs)} broken refs")

# Apply mapping to sios.json
fixed_count = 0
for s in sios:
    pc = s.get("parent_cio_code", "")
    if pc and pc in old_to_new:
        s["parent_cio_code"] = old_to_new[pc]
        fixed_count += 1

print(f"Fixed {fixed_count} parent_cio_code in sios.json")
with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

# Rebuild TSV
with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
    concepts = [line.strip().split("\t") for line in f.readlines()[1:]]
gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
print("Rebuilt learning-objectives.tsv")

# Re-run concept_codes fix
with open(out_dir / "learning-objectives.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    rows = list(reader)

cio_concept = {}
for c in cios:
    m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", c["code"])
    if m:
        cio_concept[c["code"]] = m.group(1)

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
        m = re.match(r"CIO-([A-Z][A-Z0-9_]+)-", code)
        if m:
            row["concept_codes"] = m.group(1)
            filled += 1
    elif lo_type == "SPECIFIC_IMPL":
        plo = row.get("parent_lo_code", "").strip()
        parts = [p.strip() for p in plo.replace(";", ",").split(",") if p.strip()]
        concepts = []
        for pc in parts:
            c = cio_concept.get(pc, "")
            if c and c not in concepts:
                concepts.append(c)
        if concepts:
            row["concept_codes"] = ", ".join(concepts)
            filled += 1

print(f"Filled concept_codes for {filled} LOs")

with open(out_dir / "learning-objectives.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print("Done!")
