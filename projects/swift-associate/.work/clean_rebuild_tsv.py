#!/usr/bin/env python3
"""
Clean JSON files (strip newlines in fields) and rebuild learning-objectives.tsv cleanly.
"""
import json, re

BASE = "projects/swift-associate"
ULOS_PATH = f"{BASE}/.work/hlo/ulos.json"
CIOS_PATH = f"{BASE}/.work/hlo/cios.json"
SIOS_PATH = f"{BASE}/.work/hlo/sios.json"
CONCEPTS_PATH = f"{BASE}/output/concepts.tsv"
TSV_PATH  = f"{BASE}/output/learning-objectives.tsv"

# Load concepts
with open(CONCEPTS_PATH, encoding='utf-8') as f:
    concept_lines = f.readlines()
valid_concepts = {l.split('\t')[0].strip() for l in concept_lines[1:] if l.strip()}
print(f"Valid concepts in project: {len(valid_concepts)}")

# Concept alias map if needed
concept_alias = {
    'UI_MODIFIERS': 'UI_MODIFIERS_CONCEPT',
}

def sanitize_obj(obj):
    """Recursively strip raw newlines from string fields."""
    if isinstance(obj, dict):
        return {k: sanitize_obj(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_obj(x) for x in obj]
    elif isinstance(obj, str):
        return obj.replace('\r', '').replace('\n', ' ').strip()
    return obj

# 1. Clean JSONs
with open(ULOS_PATH) as f: ulos = sanitize_obj(json.load(f))
with open(CIOS_PATH) as f: cios = sanitize_obj(json.load(f))
with open(SIOS_PATH) as f: sios = sanitize_obj(json.load(f))

# Save sanitized JSONs back
with open(ULOS_PATH, 'w', encoding='utf-8') as f: json.dump(ulos, f, ensure_ascii=False, indent=2)
with open(CIOS_PATH, 'w', encoding='utf-8') as f: json.dump(cios, f, ensure_ascii=False, indent=2)
with open(SIOS_PATH, 'w', encoding='utf-8') as f: json.dump(sios, f, ensure_ascii=False, indent=2)

print("[OK] Sanitized ulos.json, cios.json, sios.json (removed embedded newlines)")

ulo_map = {u['code']: u for u in ulos}
cio_map = {c['code']: c for c in cios}

def get_concept_for_cio(cio_code):
    cio = cio_map.get(cio_code)
    if not cio:
        parts = cio_code.split('-')
        c = parts[1] if len(parts) > 1 else ''
        return concept_alias.get(c, c)
    parent_ulo = cio.get('parent_ulo_code', '')
    ulo = ulo_map.get(parent_ulo)
    if ulo:
        cc = ulo.get('concept_codes', '')
        if isinstance(cc, list):
            res = cc[0] if cc else ''
        else:
            res = str(cc).strip("[]'\"")
        return concept_alias.get(res, res)
    # Fallback to code
    parts = cio_code.split('-')
    c = parts[1] if len(parts) > 1 else ''
    return concept_alias.get(c, c)

def norm_bloom(b):
    mapping = {
        'REMEMBER':'Remember','UNDERSTAND':'Understand','APPLY':'Apply',
        'ANALYZE':'Analyze','EVALUATE':'Evaluate','CREATE':'Create',
    }
    return mapping.get(b.upper(), b.capitalize())

def norm_kd(kd):
    kd = kd.strip()
    mapping = {
        'FACTUAL':'Factual','CONCEPTUAL':'Conceptual','PROCEDURAL':'Procedural',
        'METACOGNITIVE':'Metacognitive',
        'Factual Knowledge':'Factual','Conceptual Knowledge':'Conceptual',
        'Procedural Knowledge':'Procedural','Metacognitive Knowledge':'Metacognitive',
    }
    return mapping.get(kd, kd)

# Rebuild TSV completely from clean JSON sources
tsv_rows = []
HEADER = "code\tname\tdescription\tlo_type\tparent_lo_code\tconcept_codes\tbloom_level\tknowledge_dimension\tassessment_approach"

# 1. ULOs
for u in ulos:
    cc = u.get('concept_codes', '')
    if isinstance(cc, list): cc = ','.join(cc)
    cc = concept_alias.get(cc, cc)
    tsv_rows.append('\t'.join([
        u['code'],
        u.get('name', ''),
        u.get('description_vi', u.get('description', '')),
        'UNIVERSAL',
        '',
        cc,
        norm_bloom(u.get('bloom_level', 'Understand')),
        norm_kd(u.get('knowledge_dimension', 'Conceptual')),
        '',
    ]))

# 2. CIOs
for c in cios:
    cc = get_concept_for_cio(c['code'])
    tsv_rows.append('\t'.join([
        c['code'],
        c.get('name', ''),
        c.get('description_vi', c.get('description', '')),
        'CONCEPTUAL_IMPL',
        c.get('parent_ulo_code', ''),
        cc,
        norm_bloom(c.get('bloom_level', 'Understand')),
        norm_kd(c.get('knowledge_dimension', 'Procedural')),
        '',
    ]))

# 3. SIOs
for s in sios:
    parent_cio = s.get('parent_cio_code', '')
    cc = get_concept_for_cio(parent_cio)
    tsv_rows.append('\t'.join([
        s['code'],
        s.get('name', ''),
        s.get('description_vi', s.get('description', '')),
        'SPECIFIC_IMPL',
        parent_cio,
        cc,
        norm_bloom(s.get('bloom_level', 'Apply')),
        norm_kd(s.get('knowledge_dimension', 'Procedural')),
        '',
    ]))

with open(TSV_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(HEADER + '\n')
    for r in tsv_rows:
        f.write(r + '\n')

print(f"[OK] Rebuilt learning-objectives.tsv cleanly: {len(tsv_rows)} rows")
