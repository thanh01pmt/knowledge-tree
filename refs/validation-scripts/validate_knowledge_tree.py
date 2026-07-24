import csv
import os
import sys
import argparse
import json

BASE = os.path.join(os.path.dirname(__file__), '..', 'docs', 'examples', 'knowledge-tree')
FILES = {
    'fields': os.path.join(BASE, 'fields.tsv'),
    'subjects': os.path.join(BASE, 'subjects.tsv'),
    'categories': os.path.join(BASE, 'categories.tsv'),
    'topics': os.path.join(BASE, 'topics.tsv'),
    'concepts': os.path.join(BASE, 'concepts.tsv'),
    'learning_objectives': os.path.join(BASE, 'learning-objectives-ltasw.tsv'),
}

def read_tsv(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            rows.append((row, reader.line_num))
    return rows

def parse_codes(value):
    if not value:
        return []
    parts = [p.strip() for p in value.split(',')]
    return [p for p in parts if p]

fields_rows = read_tsv(FILES['fields'])
subjects_rows = read_tsv(FILES['subjects'])
categories_rows = read_tsv(FILES['categories'])
topics_rows = read_tsv(FILES['topics'])
concepts_rows = read_tsv(FILES['concepts'])
learning_rows = read_tsv(FILES['learning_objectives'])

fields_codes = set(r['code'] for r, _ in fields_rows)
subjects_codes = set(r['code'] for r, _ in subjects_rows)
categories_codes = set(r['code'] for r, _ in categories_rows)
topics_codes = set(r['code'] for r, _ in topics_rows)
concepts_codes = set(r['code'] for r, _ in concepts_rows)
lo_codes = set(r['code'] for r, _ in learning_rows)
lo_types_by_code = {}
lo_lines_by_code = {}
for r, line in learning_rows:
    code = (r.get('code') or '').strip()
    lo_types_by_code[code] = (r.get('lo_type') or '').strip()
    lo_lines_by_code.setdefault(code, []).append(line)

errors = []

def add_error(file, line, entity_code, column, bad_value, expected_level, error_type):
    errors.append({'file': file, 'line': line, 'code': entity_code, 'column': column, 'value': bad_value, 'expected': expected_level, 'error_type': error_type})

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true', help='Output JSON report')
parser.add_argument('--lo-only', action='store_true', help='Validate only Learning Objectives')
args = parser.parse_args()

if not args.lo_only:
    for r, line in subjects_rows:
        for c in parse_codes(r.get('field_codes', '')):
            if c not in fields_codes:
                add_error(FILES['subjects'], line, r.get('code', ''), 'field_codes', c, 'fields', 'missing_field')

if not args.lo_only:
    for r, line in categories_rows:
        for c in parse_codes(r.get('subject_codes', '')):
            if c not in subjects_codes:
                add_error(FILES['categories'], line, r.get('code', ''), 'subject_codes', c, 'subjects', 'missing_subject')

if not args.lo_only:
    for r, line in topics_rows:
        for c in parse_codes(r.get('category_codes', '')):
            if c not in categories_codes:
                add_error(FILES['topics'], line, r.get('code', ''), 'category_codes', c, 'categories', 'missing_category')

if not args.lo_only:
    for r, line in concepts_rows:
        for c in parse_codes(r.get('topic_codes', '')):
            if c not in topics_codes:
                add_error(FILES['concepts'], line, r.get('code', ''), 'topic_codes', c, 'topics', 'missing_topic')

# learning objectives → concepts and parent link
for r, line in learning_rows:
    lo_code = (r.get('code') or '').strip()
    lo_type = (r.get('lo_type') or '').strip()
    lo_name = (r.get('name') or '').strip()
    if not lo_code:
        add_error(FILES['learning_objectives'], line, '(empty)', 'code', '(empty)', 'non_empty', 'missing_required')
    if not lo_name:
        add_error(FILES['learning_objectives'], line, lo_code or '(unknown)', 'name', '(empty)', 'non_empty', 'missing_required')
    if lo_type not in ('UNIVERSAL', 'CONCEPTUAL_IMPL', 'SPECIFIC_IMPL'):
        add_error(FILES['learning_objectives'], line, lo_code, 'lo_type', lo_type or '(empty)', 'UNIVERSAL|CONCEPTUAL_IMPL|SPECIFIC_IMPL', 'invalid_lo_type')
    for c in parse_codes(r.get('concept_codes', '')):
        if c not in concepts_codes:
            add_error(FILES['learning_objectives'], line, r.get('code', ''), 'concept_codes', c, 'concepts', 'missing_concept')
    parent = r.get('parent_lo_code', '').strip()
    if parent and parent.upper() != 'NULL' and parent not in lo_codes:
        add_error(FILES['learning_objectives'], line, lo_code, 'parent_lo_code', parent, 'missing_parent', 'missing_parent')
    code = r.get('code', '').strip()
    lo_type = r.get('lo_type', '').strip()
    prefix = 'UNKNOWN'
    if code.startswith('ULO-'):
        prefix = 'ULO'
    elif code.startswith('CIO-'):
        prefix = 'CIO'
    elif code.startswith('SIO-'):
        prefix = 'SIO'
    elif code.upper().startswith('ULO_'):
        prefix = 'ULO'
    elif code.upper().startswith('CIO_'):
        prefix = 'CIO'
    elif code.upper().startswith('SIO_'):
        prefix = 'SIO'
    expected_type = ''
    if prefix == 'ULO':
        expected_type = 'UNIVERSAL'
    elif prefix == 'CIO':
        expected_type = 'CONCEPTUAL_IMPL'
    elif prefix == 'SIO':
        expected_type = 'SPECIFIC_IMPL'
    if expected_type and lo_type and lo_type != expected_type:
        add_error(FILES['learning_objectives'], line, code, 'lo_type', lo_type, expected_type, 'prefix_type_mismatch')
    if prefix == 'ULO':
        if parent and parent.upper() != 'NULL':
            add_error(FILES['learning_objectives'], line, code, 'parent_lo_code', parent, 'NULL', 'ulo_must_have_null_parent')
    elif prefix == 'CIO':
        if parent and parent.upper() != 'NULL' and not (parent.startswith('ULO-') or parent.upper().startswith('ULO_') or parent.upper().startswith('ULO')):
            add_error(FILES['learning_objectives'], line, code, 'parent_lo_code', parent, 'ULO-*', 'cio_parent_prefix_mismatch')
        elif parent and parent.upper() != 'NULL':
            # parent exists? check type
            ptype = lo_types_by_code.get(parent, '')
            if ptype and ptype != 'UNIVERSAL':
                add_error(FILES['learning_objectives'], line, code, 'parent_lo_type', ptype, 'UNIVERSAL', 'cio_parent_type_mismatch')
    elif prefix == 'SIO':
        if parent and parent.upper() != 'NULL' and not (parent.startswith('CIO-') or parent.upper().startswith('CIO_') or parent.upper().startswith('CIO')):
            add_error(FILES['learning_objectives'], line, code, 'parent_lo_code', parent, 'CIO-*', 'sio_parent_prefix_mismatch')
        elif parent and parent.upper() != 'NULL':
            ptype = lo_types_by_code.get(parent, '')
            if ptype and ptype != 'CONCEPTUAL_IMPL':
                add_error(FILES['learning_objectives'], line, code, 'parent_lo_type', ptype, 'CONCEPTUAL_IMPL', 'sio_parent_type_mismatch')

# duplicate LO codes check
from collections import Counter
lo_code_counts = Counter((r.get('code') or '').strip() for r, _ in learning_rows)
for code, cnt in lo_code_counts.items():
    if code and cnt > 1:
        lines = ','.join(str(x) for x in lo_lines_by_code.get(code, []))
        add_error(FILES['learning_objectives'], lo_lines_by_code.get(code, [0])[0], code, 'code', f'duplicated {cnt} times at lines {lines}', 'unique', 'duplicate_code')

def rel(path):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    try:
        return os.path.relpath(path, root)
    except Exception:
        return path

by_level = {'subjects': 0, 'categories': 0, 'topics': 0, 'concepts': 0, 'learning_objectives': 0}
for e in errors:
    base = os.path.basename(e['file'])
    if base == 'subjects.tsv':
        by_level['subjects'] += 1
    elif base == 'categories.tsv':
        by_level['categories'] += 1
    elif base == 'topics.tsv':
        by_level['topics'] += 1
    elif base == 'concepts.tsv':
        by_level['concepts'] += 1
    elif base == 'learning-objectives-ltasw.tsv':
        by_level['learning_objectives'] += 1

type_counts = {}
for e in errors:
    type_counts[e['error_type']] = type_counts.get(e['error_type'], 0) + 1

# Suggestions (non-mutating)
suggestions = []
used_codes = set(lo_codes)
for e in errors:
    if e['error_type'] == 'duplicate_code':
        code = e['code']
        lines = lo_lines_by_code.get(code, [])
        for i, ln in enumerate(lines[1:], start=2):  # keep first occurrence, suggest for duplicates
            suffix = i
            new_code = f"{code}_{suffix}"
            while new_code in used_codes:
                suffix += 1
                new_code = f"{code}_{suffix}"
            suggestions.append({'type': 'rename_code', 'code': code, 'line': ln, 'suggested_code': new_code, 'reason': 'ensure unique code'})
            used_codes.add(new_code)
    elif e['error_type'] == 'missing_parent':
        child_code = e['code']
        parent_code = e['value']
        etype = 'add_parent_LO'
        child_prefix = 'UNKNOWN'
        if child_code.startswith('CIO-') or child_code.upper().startswith('CIO_'):
            child_prefix = 'CIO'
        elif child_code.startswith('SIO-') or child_code.upper().startswith('SIO_'):
            child_prefix = 'SIO'
        expected_parent_type = 'UNIVERSAL' if child_prefix == 'CIO' else ('CONCEPTUAL_IMPL' if child_prefix == 'SIO' else 'UNIVERSAL')
        suggestions.append({'type': etype, 'code': child_code, 'parent_code': parent_code, 'expected_parent_lo_type': expected_parent_type})
    elif e['error_type'] in ('prefix_type_mismatch', 'ulo_must_have_null_parent', 'cio_parent_prefix_mismatch', 'cio_parent_type_mismatch', 'sio_parent_prefix_mismatch', 'sio_parent_type_mismatch'):
        suggestions.append({'type': 'fix_relationship', 'code': e['code'], 'column': e['column'], 'value': e['value'], 'expected': e['expected'], 'error_type': e['error_type']})

if args.json:
    out = {
        'base': rel(BASE),
        'summary': {
            'errors': len(errors),
            'subjects': by_level['subjects'],
            'categories': by_level['categories'],
            'topics': by_level['topics'],
            'concepts': by_level['concepts'],
            'learning_objectives': by_level['learning_objectives'],
            'error_types': type_counts,
        },
        'details': [{
            'file': rel(e['file']),
            'line': e['line'],
            'code': e['code'],
            'column': e['column'],
            'value': e['value'],
            'expected': e['expected'],
            'error_type': e['error_type'],
        } for e in errors]
    }
    out['suggestions'] = suggestions
    print(json.dumps(out, ensure_ascii=False))
else:
    print('Knowledge Tree Validation')
    print('Base:', rel(BASE))
    print('Errors:', len(errors))
    print('Subjects:', by_level['subjects'])
    print('Categories:', by_level['categories'])
    print('Topics:', by_level['topics'])
    print('Concepts:', by_level['concepts'])
    print('LearningObjectives:', by_level['learning_objectives'])
    if errors:
        print('Error Types:')
        for k in sorted(type_counts.keys()):
            print(f"  {k}: {type_counts[k]}")
        print('Details:')
        for e in errors:
            print(f"{rel(e['file'])}:{e['line']} | {e['code']} | {e['column']} invalid '{e['value']}' (expected {e['expected']})")
        if suggestions:
            print('Suggestions:')
            for s in suggestions:
                if s['type'] == 'rename_code':
                    print(f"  line {s['line']}: rename '{s['code']}' to '{s['suggested_code']}'")
                elif s['type'] == 'add_parent_LO':
                    print(f"  code {s['code']}: add parent LO '{s['parent_code']}' with lo_type '{s['expected_parent_lo_type']}'")
                elif s['type'] == 'fix_relationship':
                    print(f"  code {s['code']}: fix {s['column']} '{s['value']}' to match '{s['expected']}' [{s['error_type']}]")

sys.exit(1 if errors else 0)