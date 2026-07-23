#!/usr/bin/env python3
"""
assemble_project.py — Build 5 taxonomy TSV files (fields → concepts) from master_tree.json.

Hai chế độ hoạt động:
  --source mapping-plan  (MẶC ĐỊNH): Đọc concept codes từ mapping-plan.md để build taxonomy.
                                      Đây là thứ tự ĐÚNG: build taxonomy trước, generate LO sau.
  --source lo-tsv        (tương thích ngược): Đọc concept_codes từ learning-objectives.tsv,
                                               rồi build taxonomy ngược từ LO.

Lưu ý: Chỉ build 5 file (fields, subjects, categories, topics, concepts).
        File learning-objectives.tsv được sinh riêng bởi /generate-los (llm_extract_lo.py).
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_status(repo_root: Path) -> dict:
    status_file = repo_root / "status.yaml"
    res = {}
    if status_file.is_file():
        with open(status_file, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line and not line.strip().startswith("#"):
                    k, v = line.split(":", 1)
                    res[k.strip()] = v.strip().strip("'\"")
    return res


def extract_codes_from_mapping_plan(plan_path: Path) -> set:
    """Parse concept codes from mapping-plan.md.
    Recognises lines containing backtick-quoted UPPER_SNAKE_CASE tokens."""
    if not plan_path.is_file():
        print(f"❌ Error: mapping-plan.md không tìm thấy tại {plan_path}")
        sys.exit(1)

    content = plan_path.read_text(encoding="utf-8")
    # Match all `CODE_LIKE_THIS` tokens (UPPER_SNAKE_CASE or UPPER-WITH-DASH)
    codes = set(re.findall(r"`([A-Z][A-Z0-9_\-]{2,})`", content))
    return codes


def extract_codes_from_lo_tsv(lo_tsv: Path) -> set:
    """Parse concept_codes column from learning-objectives.tsv."""
    if not lo_tsv.is_file():
        print(f"⚠️ Warning: learning-objectives.tsv không tìm thấy tại {lo_tsv}. Taxonomy sẽ rỗng.")
        return set()

    target_concepts = set()
    with open(lo_tsv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            c_str = r.get("concept_codes", "")
            for c in c_str.replace(";", ",").split(","):
                c = c.strip()
                if c:
                    target_concepts.add(c)
    return target_concepts


def build_lookup_tables(master: dict) -> tuple[dict, dict, dict]:
    """Build code → level and code → row lookup tables from master_tree.json."""
    levels = ["fields", "subjects", "categories", "topics", "concepts"]
    code_to_lvl, code_to_row = {}, {}
    collisions = []
    for lvl in levels:
        for row in master.get(lvl, []):
            code = row["code"]
            if code in code_to_lvl and code_to_lvl[code] != lvl:
                collisions.append((code, code_to_lvl[code], lvl))
            code_to_lvl[code] = lvl
            code_to_row[code] = dict(row)
    if collisions:
        print("❌ Codes reused across multiple Master Tree levels:")
        for code, lvl1, lvl2 in collisions:
            print(f"   • '{code}' is both a {lvl1[:-1]} and a {lvl2[:-1]}")
        sys.exit(1)
    return levels, code_to_lvl, code_to_row


def collect_ancestors(code: str, code_to_lvl: dict, code_to_row: dict, result: dict):
    """Recursively collect a code and all its ancestors into result dict."""
    parent_keys = {
        "concepts": "topic_codes",
        "topics": "category_codes",
        "categories": "subject_codes",
        "subjects": "field_codes",
        "fields": None,
    }
    row = code_to_row.get(code)
    if not row:
        return
    actual_lvl = code_to_lvl[code]
    result.setdefault(actual_lvl, {})
    if code in result[actual_lvl]:
        return
    result[actual_lvl][code] = row

    pkey = parent_keys.get(actual_lvl)
    if pkey and row.get(pkey):
        p_codes = [c.strip() for c in row[pkey].replace(";", ",").split(",") if c.strip()]
        for pc in p_codes:
            if pc in code_to_lvl:
                collect_ancestors(pc, code_to_lvl, code_to_row, result)


def sanitize_parent_refs(result: dict, levels: list):
    """Trim cross-level parent references to only valid codes at each level."""
    level_codes = {lvl: set(result.get(lvl, {}).keys()) for lvl in levels}
    dropped = []

    def clean(rows_dict, parent_field, parent_lvl, level_name):
        for code, row in list(rows_dict.items()):
            valid = [c.strip() for c in row.get(parent_field, "").replace(";", ",").split(",")
                     if c.strip() in level_codes[parent_lvl]]
            if valid:
                row[parent_field] = ", ".join(valid)
            else:
                dropped.append((level_name, code, row.get(parent_field, "")))
                del rows_dict[code]

    if result.get("subjects"):
        clean(result["subjects"], "field_codes", "fields", "subjects")
    if result.get("categories"):
        clean(result["categories"], "subject_codes", "subjects", "categories")
    if result.get("topics"):
        clean(result["topics"], "category_codes", "categories", "topics")
    if result.get("concepts"):
        clean(result["concepts"], "topic_codes", "topics", "concepts")

    if dropped:
        print("⚠️  Rows dropped for lacking any valid parent (fix the Master Tree or mapping-plan):")
        for level_name, code, raw in dropped:
            print(f"   • {level_name}/{code} (had: '{raw}')")


HEADERS_MAP = {
    "fields":     ["code", "name", "description", "display_order", "keywords", "cs2023_ka_mapping", "metadata"],
    "subjects":   ["code", "name", "description", "field_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "categories": ["code", "name", "description", "subject_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "topics":     ["code", "name", "description", "category_codes", "keywords", "cs2023_ka_mapping", "metadata"],
    "concepts":   ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"],
}


def write_tsvs(result: dict, out_dir: Path, levels: list):
    out_dir.mkdir(parents=True, exist_ok=True)
    for lvl in levels:
        keys = HEADERS_MAP[lvl]
        rows = list(result.get(lvl, {}).values())
        with open(out_dir / f"{lvl}.tsv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(keys)
            for r in rows:
                writer.writerow([r.get(k, "") for k in keys])
        print(f"  ✓ {lvl}.tsv — {len(rows)} rows")


def main():
    parser = argparse.ArgumentParser(description="Assemble taxonomy TSV files from master_tree.json")
    parser.add_argument("--project", type=str, help="Project slug")
    parser.add_argument(
        "--source",
        choices=["mapping-plan", "lo-tsv"],
        default="mapping-plan",
        help="Source to determine which concept codes to include. Default: mapping-plan (recommended)."
    )
    args = parser.parse_args()

    repo = find_repo_root(Path.cwd())

    slug = args.project
    if not slug:
        status = load_status(repo)
        slug = status.get("active_project")
        if not slug:
            print("❌ Error: Không có project. Truyền --project hoặc set active_project trong status.yaml.")
            sys.exit(1)

    out_dir = repo / "projects" / slug / "output"
    work_dir = repo / "projects" / slug / ".work"
    master_json = repo / ".agents/skills/taxonomy-mapper/resources/master_tree.json"

    if not master_json.is_file():
        print(f"❌ Error: master_tree.json không tìm thấy tại {master_json}.")
        print("   Hãy chạy parse_master_tree.py trước.")
        sys.exit(1)

    with open(master_json, "r", encoding="utf-8") as f:
        master = json.load(f)

    levels, code_to_lvl, code_to_row = build_lookup_tables(master)

    # Determine target concept codes
    if args.source == "mapping-plan":
        plan_path = work_dir / "mapping-plan.md"
        print(f"[*] Mode: mapping-plan — đọc concept codes từ {plan_path.name}")
        target_codes = extract_codes_from_mapping_plan(plan_path)
        # Filter to only concept-level codes
        concept_codes = {c for c in target_codes if code_to_lvl.get(c) == "concepts"}
        # Also allow topics/categories to be explicitly targeted
        non_concept = target_codes - concept_codes
        print(f"[*] Tìm thấy {len(concept_codes)} concept codes, {len(non_concept)} codes cấp khác trong mapping-plan.")
    else:
        lo_tsv = out_dir / "learning-objectives.tsv"
        print(f"[*] Mode: lo-tsv — đọc concept codes từ {lo_tsv.name} (backward-compatible)")
        concept_codes = extract_codes_from_lo_tsv(lo_tsv)

    if not concept_codes:
        print("⚠️  Warning: Không tìm thấy concept codes hợp lệ. Output TSVs sẽ rỗng.")

    # Collect ancestors for all target codes
    result: dict = {}
    for c in concept_codes:
        collect_ancestors(c, code_to_lvl, code_to_row, result)

    sanitize_parent_refs(result, levels)

    print(f"\n[*] Building taxonomy TSVs for project '{slug}'...")
    write_tsvs(result, out_dir, levels)
    print(f"\n[✓] Taxonomy assembled for '{slug}'!")
    print("[→] Tiếp theo: chạy /generate-los để sinh learning-objectives.tsv.")


if __name__ == "__main__":
    main()
