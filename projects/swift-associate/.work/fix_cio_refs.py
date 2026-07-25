#!/usr/bin/env python3
"""
Fix inconsistent CIO codes: create new semantic CIOs for all broken SIO parent refs,
update sios.json and learning-objectives.tsv accordingly.
"""
import json, re, copy

BASE = "projects/swift-associate"
ULOS_PATH = f"{BASE}/.work/hlo/ulos.json"
CIOS_PATH = f"{BASE}/.work/hlo/cios.json"
SIOS_PATH = f"{BASE}/.work/hlo/sios.json"
TSV_PATH  = f"{BASE}/output/learning-objectives.tsv"

with open(ULOS_PATH) as f: ulos = json.load(f)
with open(CIOS_PATH) as f: cios = json.load(f)
with open(SIOS_PATH) as f: sios = json.load(f)

ulo_codes = {u['code'] for u in ulos}
cio_codes = {c['code'] for c in cios}

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: group SIOs by broken parent CIO ref
# ─────────────────────────────────────────────────────────────────────────────
groups: dict[str, list] = {}
for s in sios:
    p = s.get('parent_cio_code', '')
    if p and p not in cio_codes:
        groups.setdefault(p, []).append(s)

print(f"Found {len(groups)} broken CIO refs covering {sum(len(v) for v in groups.values())} SIOs")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: parse old CIO code -> concept + ulo_num
# Handles both  CIO-CONCEPT-NN-MM  and  CIO-CONCEPT_NN-MM  patterns
# ─────────────────────────────────────────────────────────────────────────────
def parse_old_cio(code: str):
    """Return (concept, ulo_num) from old numeric CIO code."""
    rest = code[4:]  # strip 'CIO-'
    # e.g. CONTROL_FLOW-01-01  or  DEBUGGING_02-01  or  OBJECT_PROPERTIES-03-1
    # Split by '-' right-to-left to find numeric suffix
    parts = rest.split('-')
    # Walk backwards to find all-numeric tokens (may be '01','1','02' etc.)
    num_parts = []
    concept_parts = []
    for p in reversed(parts):
        if re.match(r'^\d+$', p) and len(num_parts) < 2:
            num_parts.insert(0, p)
        else:
            concept_parts.insert(0, p)
    concept = '-'.join(concept_parts)
    # ulo_num is the first numeric token (e.g. '01')
    ulo_num = num_parts[0].zfill(2) if num_parts else '01'
    # Fix DEBUGGING_ edge case: DEBUGGING_02 -> concept=DEBUGGING, ulo_num=02
    m = re.match(r'^([A-Z_]+?)_(\d+)$', concept)
    if m:
        concept = m.group(1)
        ulo_num = m.group(2).zfill(2)
    return concept, ulo_num

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: derive semantic slug from first SIO's action keywords
# ─────────────────────────────────────────────────────────────────────────────
def derive_slug(sio_list: list, concept: str) -> str:
    first = sio_list[0]
    code = first['code'].replace('SIO-SWIFT-', '')
    # Remove concept prefix if it exists in SIO code
    code = re.sub(rf'^{re.escape(concept)}_', '', code)
    parts = code.split('_')
    # Take first 4 meaningful tokens
    slug = '_'.join(parts[:4])
    return slug

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: build remap + create new CIO objects
# ─────────────────────────────────────────────────────────────────────────────
bloom_up = {
    'Create': 'Evaluate', 'Evaluate': 'Analyze', 'Analyze': 'Apply',
    'Apply': 'Understand', 'Understand': 'Remember', 'Remember': 'Remember'
}

remap: dict[str, str] = {}   # old_code -> new_code
new_cios: list = []
used_new_codes: set = set(cio_codes)

for old_code in sorted(groups.keys()):
    sio_list = groups[old_code]
    concept, ulo_num = parse_old_cio(old_code)

    # Find parent ULO
    ulo_candidate = f'ULO-{concept}-{ulo_num}'
    if ulo_candidate not in ulo_codes:
        # Fallback: find any ULO with this concept
        candidates = [u['code'] for u in ulos if concept in u['code']]
        ulo_candidate = candidates[0] if candidates else ulo_candidate

    slug = derive_slug(sio_list, concept)
    new_code = f'CIO-{concept}-{slug}'

    # Ensure uniqueness
    suffix = 2
    base_new = new_code
    while new_code in used_new_codes:
        new_code = f'{base_new}_{suffix}'
        suffix += 1
    used_new_codes.add(new_code)
    remap[old_code] = new_code

    first = sio_list[0]
    sio_bloom = first.get('bloom_level', 'Understand')
    cio_bloom = bloom_up.get(sio_bloom, sio_bloom)

    new_cios.append({
        'code': new_code,
        'name': first.get('name', f'CIO: {slug.replace("_"," ").title()}'),
        'description_vi': first.get('description_vi', '')[:200],
        'bloom_level': cio_bloom,
        'knowledge_dimension': first.get('knowledge_dimension', 'Procedural Knowledge'),
        'parent_ulo_code': ulo_candidate,
        'marr_test_note': f'Auto-generated from {old_code}. Verify Marr 2-language test independently.'
    })

print(f"\n=== REMAP ({len(remap)} entries) ===")
for old, new in sorted(remap.items()):
    print(f"  {old} -> {new}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: write updated files
# ─────────────────────────────────────────────────────────────────────────────
# 5a. Append new CIOs to cios.json
cios.extend(new_cios)
with open(CIOS_PATH, 'w', encoding='utf-8') as f:
    json.dump(cios, f, ensure_ascii=False, indent=2)
print(f"\n[OK] cios.json: added {len(new_cios)} new CIOs (total: {len(cios)})")

# 5b. Update sios.json parent_cio_code refs
sio_fix_count = 0
for s in sios:
    old = s.get('parent_cio_code', '')
    if old in remap:
        s['parent_cio_code'] = remap[old]
        sio_fix_count += 1

with open(SIOS_PATH, 'w', encoding='utf-8') as f:
    json.dump(sios, f, ensure_ascii=False, indent=2)
print(f"[OK] sios.json: fixed {sio_fix_count} SIO parent refs")

# 5c. Update learning-objectives.tsv
with open(TSV_PATH, encoding='utf-8') as f:
    tsv = f.read()

tsv_count = 0
for old, new in remap.items():
    if old in tsv:
        tsv_count += tsv.count(old)
        tsv = tsv.replace(old, new)

with open(TSV_PATH, 'w', encoding='utf-8') as f:
    f.write(tsv)
print(f"[OK] learning-objectives.tsv: fixed {tsv_count} occurrences")

print("\nDone. Run validate_tree.py to verify.")
