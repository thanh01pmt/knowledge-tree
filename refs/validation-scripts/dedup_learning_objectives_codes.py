import csv
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'docs', 'examples', 'knowledge-tree')
LO_PATH = os.path.join(BASE, 'learning-objectives-ltasw.tsv')

def dedup_codes(path: str):
    rows = []
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        headers = reader.fieldnames or []
        for row in reader:
            rows.append(row)
    seen = {}
    mapping = {}
    for row in rows:
        code = (row.get('code') or '').strip()
        if not code:
            continue
        count = seen.get(code, 0)
        if count == 0:
            seen[code] = 1
        else:
            seen[code] = count + 1
            suffix = seen[code]
            new_code = f"{code}_{suffix}"
            # ensure uniqueness even if existing codes include suffixes
            while new_code in seen or any(r.get('code') == new_code for r in rows):
                suffix += 1
                new_code = f"{code}_{suffix}"
            mapping[code, count] = new_code
            row['code'] = new_code
    # write back
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter='\t')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    os.replace(tmp_path, path)

if __name__ == '__main__':
    dedup_codes(LO_PATH)