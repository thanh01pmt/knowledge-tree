#!/usr/bin/env python3
"""
Rebuild learning-objectives.tsv from JSON sources:
1. Insert missing CIO rows (61 new CIOs not yet in TSV)
2. Fill concept_codes for all SIO rows (inherit from parent CIO)
3. Fix bloom_level format (APPLY -> Apply) for SIO rows
"""
import json, re

BASE = "projects/swift-associate"
ULOS_PATH = f"{BASE}/.work/hlo/ulos.json"
CIOS_PATH = f"{BASE}/.work/hlo/cios.json"
SIOS_PATH = f"{BASE}/.work/hlo/sios.json"
TSV_PATH  = f"{BASE}/output/learning-objectives.tsv"

with open(ULOS_PATH) as f: ulos = json.load(f)
with open(CIOS_PATH) as f: cios = json.load(f)
with open(SIOS_PATH) as f: sios = json.load(f)

# ─────────────────────────────────────────────────────────────────────────────
# Build lookup maps
# ─────────────────────────────────────────────────────────────────────────────
ulo_map = {u['code']: u for u in ulos}
cio_map = {c['code']: c for c in cios}
sio_map = {s['code']: s for s in sios}

# Build concept_codes per CIO: inherit from parent ULO's concept_codes
def get_concept_from_cio(cio_code):
    """Return concept_codes string for a CIO based on its parent ULO."""
    cio = cio_map.get(cio_code)
    if not cio:
        return ''
    ulo_code = cio.get('parent_ulo_code','')
    ulo = ulo_map.get(ulo_code)
    if ulo:
        cc = ulo.get('concept_codes','')
        if isinstance(cc, list):
            return ','.join(cc)
        return str(cc).strip("[]'\"")
    # Fallback: extract concept from CIO code itself
    parts = cio_code.split('-')
    return parts[1] if len(parts) > 1 else ''

# Capitalize bloom level
def norm_bloom(b):
    mapping = {
        'REMEMBER':'Remember','UNDERSTAND':'Understand','APPLY':'Apply',
        'ANALYZE':'Analyze','EVALUATE':'Evaluate','CREATE':'Create',
    }
    return mapping.get(b.upper(), b.capitalize())

# Normalize knowledge dimension
def norm_kd(kd):
    kd = kd.strip()
    mapping = {
        'FACTUAL':'Factual','CONCEPTUAL':'Conceptual','PROCEDURAL':'Procedural',
        'METACOGNITIVE':'Metacognitive',
        'Factual Knowledge':'Factual','Conceptual Knowledge':'Conceptual',
        'Procedural Knowledge':'Procedural','Metacognitive Knowledge':'Metacognitive',
    }
    return mapping.get(kd, kd)

# ─────────────────────────────────────────────────────────────────────────────
# Read existing TSV
# ─────────────────────────────────────────────────────────────────────────────
with open(TSV_PATH, encoding='utf-8') as f:
    raw_lines = f.readlines()

header = raw_lines[0]
# Parse into dicts keyed by code
tsv_rows: dict[str, dict] = {}
tsv_order: list[str] = []  # preserve insertion order

COLS = ['code','name','description','lo_type','parent_lo_code','concept_codes','bloom_level','knowledge_dimension','assessment_approach']

for line in raw_lines[1:]:
    parts = line.rstrip('\n').split('\t')
    # Pad to 9 cols
    while len(parts) < 9:
        parts.append('')
    row = dict(zip(COLS, parts))
    code = row['code']
    if code:
        tsv_rows[code] = row
        tsv_order.append(code)

print(f"Existing TSV rows: {len(tsv_rows)}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Insert missing CIO rows
# ─────────────────────────────────────────────────────────────────────────────
inserted_cios = 0
for cio in cios:
    code = cio['code']
    if code not in tsv_rows:
        concept_codes = get_concept_from_cio(code)
        row = {
            'code': code,
            'name': cio.get('name',''),
            'description': cio.get('description_vi',''),
            'lo_type': 'CONCEPTUAL_IMPL',
            'parent_lo_code': cio.get('parent_ulo_code',''),
            'concept_codes': concept_codes,
            'bloom_level': norm_bloom(cio.get('bloom_level','Understand')),
            'knowledge_dimension': norm_kd(cio.get('knowledge_dimension','Procedural')),
            'assessment_approach': '',
        }
        tsv_rows[code] = row
        # Insert after its parent ULO in order
        parent = cio.get('parent_ulo_code','')
        if parent in tsv_order:
            idx = tsv_order.index(parent) + 1
            tsv_order.insert(idx, code)
        else:
            tsv_order.append(code)
        inserted_cios += 1

print(f"Inserted {inserted_cios} new CIO rows")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Fix concept_codes for all SIO rows + CIO rows
# ─────────────────────────────────────────────────────────────────────────────
fixed_sio_concept = 0
fixed_cio_concept = 0
fixed_bloom = 0
fixed_kd = 0

for code, row in tsv_rows.items():
    # Fix concept_codes for SIOs (inherit from parent CIO)
    if code.startswith('SIO-') and not row.get('concept_codes','').strip():
        parent_cio = row.get('parent_lo_code','')
        cc = get_concept_from_cio(parent_cio)
        if cc:
            row['concept_codes'] = cc
            fixed_sio_concept += 1

    # Fix concept_codes for CIOs that are empty
    if code.startswith('CIO-') and not row.get('concept_codes','').strip():
        cc = get_concept_from_cio(code)
        if cc:
            row['concept_codes'] = cc
            fixed_cio_concept += 1

    # Fix bloom_level format
    bl = row.get('bloom_level','')
    normed = norm_bloom(bl)
    if bl != normed:
        row['bloom_level'] = normed
        fixed_bloom += 1

    # Fix knowledge_dimension format
    kd = row.get('knowledge_dimension','')
    normed_kd = norm_kd(kd)
    if kd != normed_kd:
        row['knowledge_dimension'] = normed_kd
        fixed_kd += 1

print(f"Fixed {fixed_sio_concept} SIO concept_codes")
print(f"Fixed {fixed_cio_concept} CIO concept_codes")
print(f"Fixed {fixed_bloom} bloom_level formats")
print(f"Fixed {fixed_kd} knowledge_dimension formats")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Write output
# ─────────────────────────────────────────────────────────────────────────────
with open(TSV_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(header.rstrip('\n') + '\n')
    for code in tsv_order:
        if code not in tsv_rows:
            continue
        row = tsv_rows[code]
        line = '\t'.join([
            row.get('code',''),
            row.get('name',''),
            row.get('description',''),
            row.get('lo_type',''),
            row.get('parent_lo_code',''),
            row.get('concept_codes',''),
            row.get('bloom_level',''),
            row.get('knowledge_dimension',''),
            row.get('assessment_approach',''),
        ])
        f.write(line + '\n')

print(f"\n[OK] TSV rebuilt: {len(tsv_order)} rows total")
print("Run validate_tree.py to verify.")
