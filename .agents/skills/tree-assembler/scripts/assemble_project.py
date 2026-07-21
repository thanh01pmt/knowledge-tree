import json
import csv
from pathlib import Path
import sys

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()

def build_project(slug):
    repo = find_repo_root(Path.cwd())
    out_dir = repo / "projects" / slug / "output"
    master_json = repo / ".agents/skills/taxonomy-mapper/resources/master_tree.json"
    lo_tsv = out_dir / "learning-objectives.tsv"
    
    with open(master_json, 'r', encoding='utf-8') as f:
        master = json.load(f)
        
    levels = ['fields', 'subjects', 'categories', 'topics', 'concepts']
    code_to_lvl = {}
    code_to_row = {}
    for lvl in levels:
        for row in master.get(lvl, []):
            code = row['code']
            code_to_lvl[code] = lvl
            code_to_row[code] = dict(row) # copy
            
    parent_keys = {
        'concepts': 'topic_codes',
        'topics': 'category_codes',
        'categories': 'subject_codes',
        'subjects': 'field_codes',
        'fields': None
    }

    def collect_ancestors(code, result):
        row = code_to_row.get(code)
        if not row:
            return
        actual_lvl = code_to_lvl[code]
        if actual_lvl not in result:
            result[actual_lvl] = {}
        if code in result[actual_lvl]:
            return
        result[actual_lvl][code] = row

        pkey = parent_keys.get(actual_lvl)
        if pkey and row.get(pkey):
            p_codes = [c.strip() for c in row[pkey].replace(';', ',').split(',') if c.strip()]
            for pc in p_codes:
                if pc in code_to_lvl:
                    collect_ancestors(pc, result)

    # Read concepts from learning-objectives.tsv if present
    target_concepts = set()
    if lo_tsv.is_file():
        with open(lo_tsv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for r in reader:
                c_str = r.get('concept_codes', '')
                for c in c_str.replace(';', ',').split(','):
                    c = c.strip()
                    if c:
                        target_concepts.add(c)
                        
    result = {}
    for c in target_concepts:
        collect_ancestors(c, result)

    # Sanitize parent references so each level ONLY references codes present in the level directly above it
    level_codes = {lvl: set(result.get(lvl, {}).keys()) for lvl in levels}
    
    # Clean subjects -> field_codes
    for s_code, row in result.get('subjects', {}).items():
        fc = [c.strip() for c in row.get('field_codes', '').replace(';', ',').split(',') if c.strip() in level_codes['fields']]
        row['field_codes'] = ', '.join(fc) if fc else 'ASE'

    # Clean categories -> subject_codes
    for c_code, row in result.get('categories', {}).items():
        sc = [c.strip() for c in row.get('subject_codes', '').replace(';', ',').split(',') if c.strip() in level_codes['subjects']]
        row['subject_codes'] = ', '.join(sc) if sc else list(level_codes['subjects'])[0]

    # Clean topics -> category_codes
    for t_code, row in result.get('topics', {}).items():
        cc = [c.strip() for c in row.get('category_codes', '').replace(';', ',').split(',') if c.strip() in level_codes['categories']]
        row['category_codes'] = ', '.join(cc) if cc else list(level_codes['categories'])[0]

    # Clean concepts -> topic_codes
    for c_code, row in result.get('concepts', {}).items():
        tc = [c.strip() for c in row.get('topic_codes', '').replace(';', ',').split(',') if c.strip() in level_codes['topics']]
        row['topic_codes'] = ', '.join(tc) if tc else list(level_codes['topics'])[0]

    # Write TSVs for fields, subjects, categories, topics, concepts
    headers_map = {
        "fields": ["code", "name", "description", "display_order", "keywords", "cs2023_ka_mapping", "metadata"],
        "subjects": ["code", "name", "description", "field_codes", "keywords", "cs2023_ka_mapping", "metadata"],
        "categories": ["code", "name", "description", "subject_codes", "keywords", "cs2023_ka_mapping", "metadata"],
        "topics": ["code", "name", "description", "category_codes", "keywords", "cs2023_ka_mapping", "metadata"],
        "concepts": ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    }
    
    for lvl, keys in headers_map.items():
        rows = list(result.get(lvl, {}).values())
        with open(out_dir / f"{lvl}.tsv", 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(keys)
            for r in rows:
                writer.writerow([r.get(k, "") for k in keys])
                
    print(f"Successfully assembled 100% clean tree hierarchy for '{slug}'!")

if __name__ == "__main__":
    build_project(sys.argv[1] if len(sys.argv) > 1 else "swift-associate")
