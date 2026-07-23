#!/usr/bin/env python3
"""
validate_tree.py — Kiểm tra & (tuỳ chọn) tự sửa lỗi Knowledge Tree

Cây: fields > subjects > categories > topics > concepts > learning-objectives
(N:N qua cột "<parent>_codes"; learning-objectives có thêm parent_lo_code N:1
và lo_type).

Chế độ chạy
-----------
1) Ad-hoc (không gắn với project nào, tương thích ngược với v1):
   python3 validate_tree.py --data-dir /path/to/tsv --output-dir /path/to/reports

2) Theo project trong repo (đọc/scaffold theo cấu trúc projects/<slug>/.tree-validator/):
   python3 validate_tree.py --project <slug> [--repo-root .]
   python3 validate_tree.py                       # lấy project từ status.yaml ở repo root

Thêm --fix để: (a) tự chuẩn hoá các cell lỗi format an toàn (DUPLICATE_REF_IN_CELL,
SEPARATOR_FORMAT) và ghi đè file (có backup), (b) sinh đề xuất sửa cho
BROKEN_REFERENCE / LO_TYPE_PARENT_MISMATCH vào proposed_fixes.json/.md — KHÔNG
tự ghi đè các đề xuất này, chờ người/agent duyệt.

Exit code: 0 nếu không còn ERROR sau khi fix (hoặc không --fix mà vốn đã PASS),
1 nếu còn ERROR.
"""

import argparse
import csv
import difflib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

LEVELS = [
    {"name": "fields", "file": "fields.tsv", "parent_field": None, "parent_level": None, "has_metadata": True},
    {"name": "subjects", "file": "subjects.tsv", "parent_field": "field_codes", "parent_level": "fields", "has_metadata": True},
    {"name": "categories", "file": "categories.tsv", "parent_field": "subject_codes", "parent_level": "subjects", "has_metadata": True},
    {"name": "topics", "file": "topics.tsv", "parent_field": "category_codes", "parent_level": "categories", "has_metadata": True},
    {"name": "concepts", "file": "concepts.tsv", "parent_field": "topic_codes", "parent_level": "topics", "has_metadata": True},
]
LO_LEVEL = {"name": "learning_objectives", "file": "learning-objectives.tsv",
            "parent_field": "concept_codes", "parent_level": "concepts", "has_metadata": False}
ALL_LEVELS = LEVELS + [LO_LEVEL]

CODE_FORMAT_RE = re.compile(r'^[A-Z0-9_\-]+$')
ALLOWED_LO_TYPES = {"UNIVERSAL", "CONCEPTUAL_IMPL", "SPECIFIC_IMPL"}
ALLOWED_KNOWLEDGE_DIMENSIONS = {"FACTUAL", "CONCEPTUAL", "PROCEDURAL", "METACOGNITIVE", "", "NULL"}
NULL_TOKEN = "NULL"

SAFE_FIX_RULES = {"DUPLICATE_REF_IN_CELL", "SEPARATOR_FORMAT"}
PROPOSE_FIX_RULES = {"BROKEN_REFERENCE", "LO_TYPE_PARENT_MISMATCH"}

RULE_DESCRIPTIONS = {
    "DUPLICATE_CODE": "Code bị trùng trong cùng 1 file",
    "EMPTY_REQUIRED_FIELD": "Thiếu giá trị bắt buộc (code/name)",
    "INVALID_METADATA_JSON": "Cột metadata không phải JSON hợp lệ",
    "BROKEN_REFERENCE": "Tham chiếu tới code không tồn tại ở bảng cha",
    "EMPTY_PARENT_REF": "Không có tham chiếu nào tới bảng cha (node lơ lửng)",
    "DUPLICATE_REF_IN_CELL": "Cùng 1 code cha xuất hiện lặp lại trong 1 cell",
    "LO_CYCLE": "Có chu trình (cycle) trong chuỗi parent_lo_code",
    "LO_SELF_REFERENCE": "parent_lo_code trỏ về chính nó",
    "LO_BROKEN_PARENT_REF": "parent_lo_code trỏ tới 1 LO không tồn tại",
    "LO_TYPE_PARENT_MISMATCH": "lo_type=UNIVERSAL phải có parent_lo_code=NULL và ngược lại",
    "LO_TYPE_UNKNOWN": "lo_type không nằm trong tập giá trị cho phép",
    "LO_CONCEPT_NOT_IN_PROJECT": "concept_codes của LO chứa code không tồn tại trong concepts.tsv của project",
    "LO_CONCEPT_UNCOVERED": "Concept trong concepts.tsv không được LO nào trỏ đến (thiếu coverage)",
    "CIO_INSUFFICIENT_SIO": "CIO có ít hơn 2 SIO con — phân rã chưa đủ sâu theo mô hình sư phạm",
    "ORPHAN_NODE": "Node không được node nào ở tầng dưới tham chiếu tới",
    "CODE_FORMAT": "Code không khớp định dạng chuẩn ^[A-Z0-9_-]+$",
    "SEPARATOR_FORMAT": "Cách phân tách code trong cell không chuẩn (thừa space / dùng ; hoặc |)",
    "INCONSISTENT_LINE_ENDINGS": "File dùng line-ending khác với đa số các file còn lại",
    "MISSING_FILE": "Không tìm thấy file dữ liệu",
}


@dataclass
class Issue:
    severity: str
    rule_id: str
    level: str
    code: str
    message: str
    field: Optional[str] = None
    ref: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_tsv_rows(path: Path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        rows = list(reader)
    return fieldnames, rows


def write_tsv_rows(path: Path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def split_codes_raw(value: str):
    if value is None:
        return []
    normalized = value.replace(";", ",").replace("|", ",")
    return [c.strip() for c in normalized.split(",")]


def split_codes(value: str):
    return [c for c in split_codes_raw(value) if c]


def now_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# status.yaml — parser/writer tối giản (không phụ thuộc PyYAML).
# Chỉ hỗ trợ đúng schema phẳng dùng trong skill này: scalar keys + 1 list of
# scalars/objects đơn giản. Nếu môi trường có PyYAML, ưu tiên dùng PyYAML để
# an toàn hơn với các status.yaml phức tạp hơn.
# ---------------------------------------------------------------------------

try:
    import yaml  # type: ignore
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False


def read_status_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if _HAS_YAML:
        return yaml.safe_load(text) or {}
    # fallback: parser tối giản cho key: value phẳng (bỏ qua list/nested)
    data = {}
    for line in text.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or line.lstrip().startswith("-"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        if key.startswith(" "):
            continue  # bỏ qua nested — cần PyYAML cho trường hợp phức tạp
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if val == "" or val.lower() == "null":
            val = None
        data[key] = val
    return data


def write_status_yaml(path: Path, data: dict):
    if _HAS_YAML:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return
    # fallback writer tối giản — chỉ hỗ trợ scalar + list[str]
    lines = []
    for k, v in data.items():
        if v is None:
            lines.append(f"{k}: null")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        elif isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        else:
            lines.append(f'{k}: "{v}"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Project / repo resolution
# ---------------------------------------------------------------------------

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()  # fallback: không tìm thấy .agents, dùng thư mục start


def resolve_data_dir(args) -> tuple[Path, Optional[Path], Optional[str]]:
    """Trả về (data_dir, project_dir_or_None, project_slug_or_None)."""
    if args.data_dir:
        return Path(args.data_dir).resolve(), None, None

    repo_root = Path(args.repo_root).resolve() if args.repo_root else find_repo_root(Path.cwd())
    status_path = repo_root / "status.yaml"

    slug = args.project
    if not slug:
        status = read_status_yaml(status_path)
        slug = status.get("active_project")
        if not slug:
            print(f"Lỗi: không có --project và không tìm thấy 'active_project' trong {status_path}",
                  file=sys.stderr)
            sys.exit(2)

    project_dir = repo_root / "projects" / slug
    if not project_dir.is_dir():
        print(f"Lỗi: không tìm thấy thư mục project '{slug}' tại {project_dir}", file=sys.stderr)
        sys.exit(2)
    data_dir = project_dir / "output"
    return data_dir, project_dir, slug


def scaffold_project_artifacts(project_dir: Path, need_fix_dirs: bool = False) -> dict:
    base = project_dir / ".tree-validator"
    stamp = now_stamp()
    paths = {
        "base": base,
        "report_dir": base / "reports" / stamp,
        "fix_dir": base / "fixes" / stamp,
        "backup_dir": base / "backups" / stamp,
        "stamp": stamp,
    }
    paths["report_dir"].mkdir(parents=True, exist_ok=True)
    if need_fix_dirs:
        paths["fix_dir"].mkdir(parents=True, exist_ok=True)
        # backup_dir chỉ tạo thật sự nếu có file bị ghi đè (xem apply_safe_fixes)
    return paths


# ---------------------------------------------------------------------------
# Checks (giống v1) — trả về list[Issue]
# ---------------------------------------------------------------------------

def check_duplicate_codes(level_name, rows):
    issues = []
    seen = {}
    for r in rows:
        c = (r.get("code") or "").strip()
        seen[c] = seen.get(c, 0) + 1
    for c, n in seen.items():
        if n > 1:
            issues.append(Issue("ERROR", "DUPLICATE_CODE", level_name, c,
                                 f"Code '{c}' xuất hiện {n} lần trong file."))
    return issues


def check_empty_required(level_name, rows, required_cols=("code", "name")):
    issues = []
    for r in rows:
        code = (r.get("code") or "").strip() or "<EMPTY_CODE>"
        for col in required_cols:
            if not (r.get(col) or "").strip():
                issues.append(Issue("ERROR", "EMPTY_REQUIRED_FIELD", level_name, code,
                                     f"Cột '{col}' bị rỗng.", field=col))
    return issues


def check_metadata_json(level_name, rows):
    issues = []
    for r in rows:
        code = (r.get("code") or "").strip()
        raw = r.get("metadata")
        if raw is None or raw.strip() == "":
            continue
        try:
            json.loads(raw)
        except Exception as e:
            issues.append(Issue("ERROR", "INVALID_METADATA_JSON", level_name, code,
                                 f"metadata không parse được: {e}", field="metadata"))
    return issues


def check_code_format(level_name, rows):
    issues = []
    for r in rows:
        code = (r.get("code") or "").strip()
        if code and not CODE_FORMAT_RE.match(code):
            issues.append(Issue("WARNING", "CODE_FORMAT", level_name, code,
                                 f"Code '{code}' không khớp định dạng ^[A-Z0-9_-]+$."))
    return issues


def check_referential_integrity(level_name, rows, parent_field, parent_codes_set):
    issues = []
    for r in rows:
        code = (r.get("code") or "").strip()
        raw = r.get(parent_field, "") or ""
        pieces_raw_no_norm = [c.strip() for c in raw.split(",")]
        pieces = split_codes(raw)

        if not pieces:
            issues.append(Issue("ERROR", "EMPTY_PARENT_REF", level_name, code,
                                 f"Cột '{parent_field}' rỗng — node không có cha.", field=parent_field))
            continue

        dup = {p for p in pieces if pieces.count(p) > 1}
        for d in dup:
            issues.append(Issue("ERROR", "DUPLICATE_REF_IN_CELL", level_name, code,
                                 f"'{d}' xuất hiện lặp lại trong cột '{parent_field}'.",
                                 field=parent_field, ref=d))

        for p in set(pieces):
            if p not in parent_codes_set:
                issues.append(Issue("ERROR", "BROKEN_REFERENCE", level_name, code,
                                     f"'{p}' không tồn tại trong bảng cha.",
                                     field=parent_field, ref=p))

        if "" in pieces_raw_no_norm and len(pieces_raw_no_norm) > 1:
            issues.append(Issue("WARNING", "SEPARATOR_FORMAT", level_name, code,
                                 f"Cột '{parent_field}' có dấu phẩy thừa/rỗng giữa các phần tử.",
                                 field=parent_field))
        if any(ch in raw for ch in (";", "|")):
            issues.append(Issue("WARNING", "SEPARATOR_FORMAT", level_name, code,
                                 f"Cột '{parent_field}' chứa ký tự phân tách lạ (';' hoặc '|').",
                                 field=parent_field))
    return issues


def check_orphans(level_name, own_codes_set, referenced_codes_set):
    return [Issue("WARNING", "ORPHAN_NODE", level_name, c,
                   "Không có node nào ở tầng dưới tham chiếu tới node này.")
            for c in sorted(own_codes_set - referenced_codes_set)]


def check_lo_parent_and_cycles(lo_rows, lo_codes_set):
    issues = []
    parent_map = {(r.get("code") or "").strip(): (r.get("parent_lo_code") or "").strip() for r in lo_rows}

    for code, parent in parent_map.items():
        if not parent or parent == NULL_TOKEN:
            continue
        if parent == code:
            issues.append(Issue("ERROR", "LO_SELF_REFERENCE", "learning_objectives", code,
                                 "parent_lo_code trỏ về chính nó.", field="parent_lo_code", ref=parent))
        elif parent not in lo_codes_set:
            issues.append(Issue("ERROR", "LO_BROKEN_PARENT_REF", "learning_objectives", code,
                                 f"parent_lo_code '{parent}' không tồn tại.", field="parent_lo_code", ref=parent))

    state = {}
    reported = set()

    def walk(start):
        path = []
        cur = start
        while True:
            if state.get(cur) == 1:
                return
            if cur in path:
                idx = path.index(cur)
                cycle_nodes = path[idx:]
                for n in cycle_nodes:
                    if n not in reported:
                        reported.add(n)
                        issues.append(Issue("ERROR", "LO_CYCLE", "learning_objectives", n,
                                             "Nằm trong chu trình parent_lo_code: "
                                             + " -> ".join(cycle_nodes + [cycle_nodes[0]]),
                                             field="parent_lo_code"))
                for n in cycle_nodes:
                    state[n] = 1
                return
            path.append(cur)
            nxt = parent_map.get(cur, "")
            if not nxt or nxt == NULL_TOKEN or nxt not in lo_codes_set or nxt == cur:
                for n in path:
                    state[n] = 1
                return
            cur = nxt

    for code in lo_codes_set:
        if code not in state:
            walk(code)
    return issues


def check_lo_type_rules(lo_rows):
    issues = []
    for r in lo_rows:
        code = (r.get("code") or "").strip()
        lo_type = (r.get("lo_type") or "").strip()
        parent = (r.get("parent_lo_code") or "").strip()

        if lo_type not in ALLOWED_LO_TYPES:
            issues.append(Issue("WARNING", "LO_TYPE_UNKNOWN", "learning_objectives", code,
                                 f"lo_type='{lo_type}' không thuộc {sorted(ALLOWED_LO_TYPES)}.", field="lo_type"))
            continue

        is_null_parent = parent in ("", NULL_TOKEN)
        if lo_type == "UNIVERSAL" and not is_null_parent:
            issues.append(Issue("ERROR", "LO_TYPE_PARENT_MISMATCH", "learning_objectives", code,
                                 "lo_type=UNIVERSAL nhưng parent_lo_code khác NULL.", field="parent_lo_code"))
        if lo_type != "UNIVERSAL" and is_null_parent:
            issues.append(Issue("ERROR", "LO_TYPE_PARENT_MISMATCH", "learning_objectives", code,
                                 f"lo_type={lo_type} nhưng parent_lo_code=NULL (cần có parent).",
                                 field="parent_lo_code"))
    return issues


def check_lo_concept_codes(lo_rows, project_concept_codes: set):
    """ERROR if any concept_code in a LO does not exist in the project's concepts.tsv.
    Only runs when project_concept_codes is non-empty (i.e. concepts.tsv has been built)."""
    issues = []
    if not project_concept_codes:
        return issues  # concepts.tsv rỗng → bỏ qua (có thể chưa build-tree)
    for r in lo_rows:
        code = (r.get("code") or "").strip()
        raw = r.get("concept_codes", "") or ""
        pieces = split_codes(raw)
        for p in pieces:
            if p not in project_concept_codes:
                issues.append(Issue(
                    "ERROR", "LO_CONCEPT_NOT_IN_PROJECT", "learning_objectives", code,
                    f"concept_code '{p}' không tồn tại trong concepts.tsv của project.",
                    field="concept_codes", ref=p
                ))
    return issues


def check_concept_lo_coverage(concept_rows, lo_rows):
    """WARNING if a concept in concepts.tsv has no LO pointing to it.
    Only runs when both concepts and LOs are non-empty."""
    issues = []
    if not concept_rows or not lo_rows:
        return issues

    covered: set[str] = set()
    for r in lo_rows:
        raw = r.get("concept_codes", "") or ""
        for c in raw.replace(";", ",").split(","):
            c = c.strip()
            if c:
                covered.add(c)

    for concept in concept_rows:
        code = (concept.get("code") or "").strip()
        name = (concept.get("name") or "").strip()
        if code and code not in covered:
            issues.append(Issue(
                "WARNING", "LO_CONCEPT_UNCOVERED", "concepts", code,
                f"Concept '{name}' ({code}) không có LO nào trỏ đến trong learning-objectives.tsv."
            ))
    return issues


def check_cio_sio_depth(lo_rows, min_sios: int = 2):
    """WARNING if a CIO has fewer than min_sios SPECIFIC_IMPL children.
    Each CIO should have at least 2 SIOs to ensure adequate instructional depth."""
    issues = []
    cios = {r["code"]: r for r in lo_rows if r.get("lo_type") == "CONCEPTUAL_IMPL" and r.get("code")}
    if not cios:
        return issues

    cio_sio_count: dict[str, int] = {c: 0 for c in cios}
    for r in lo_rows:
        if r.get("lo_type") == "SPECIFIC_IMPL":
            parent = (r.get("parent_lo_code") or "").strip()
            if parent in cio_sio_count:
                cio_sio_count[parent] += 1

    for cio_code, count in cio_sio_count.items():
        if count < min_sios:
            cio_name = (cios[cio_code].get("name") or "").strip()
            issues.append(Issue(
                "WARNING", "CIO_INSUFFICIENT_SIO", "learning_objectives", cio_code,
                f"CIO '{cio_name}' ({cio_code}) chỉ có {count} SIO con "
                f"(yêu cầu ≥ {min_sios}). Phân rã chưa đủ chi tiết thực hành."
            ))
    return issues


def check_line_endings(data_dir: Path, filenames):
    issues = []
    styles = {}
    for fn in filenames:
        p = data_dir / fn
        if not p.exists():
            continue
        raw = p.read_bytes()
        crlf = raw.count(b"\r\n")
        lf_only = raw.count(b"\n") - crlf
        styles[fn] = "CRLF" if crlf > lf_only else "LF"
    if not styles:
        return issues
    majority = max(set(styles.values()), key=list(styles.values()).count)
    for fn, style in styles.items():
        if style != majority:
            issues.append(Issue("WARNING", "INCONSISTENT_LINE_ENDINGS", "_file", fn,
                                 f"File dùng line-ending {style}, khác đa số các file khác ({majority})."))
    return issues


# ---------------------------------------------------------------------------
# Pipeline: load + validate
# ---------------------------------------------------------------------------

def load_all(data_dir: Path):
    issues = []
    tables = {}       # level_name -> rows (list[dict])
    fieldnames_map = {}  # level_name -> fieldnames list (thứ tự cột gốc)
    code_sets = {}

    for lvl in ALL_LEVELS:
        path = data_dir / lvl["file"]
        if not path.exists():
            issues.append(Issue("ERROR", "MISSING_FILE", lvl["name"], "-", f"Không tìm thấy file {lvl['file']}"))
            tables[lvl["name"]] = []
            fieldnames_map[lvl["name"]] = []
            code_sets[lvl["name"]] = set()
            continue
        fieldnames, rows = load_tsv_rows(path)
        tables[lvl["name"]] = rows
        fieldnames_map[lvl["name"]] = fieldnames
        code_sets[lvl["name"]] = {(r.get("code") or "").strip() for r in rows if (r.get("code") or "").strip()}

    return tables, fieldnames_map, code_sets, issues


def run_checks(data_dir: Path, tables, code_sets):
    issues = []
    for lvl in LEVELS:
        name, rows = lvl["name"], tables[lvl["name"]]
        issues += check_duplicate_codes(name, rows)
        issues += check_empty_required(name, rows)
        if lvl["has_metadata"]:
            issues += check_metadata_json(name, rows)
        issues += check_code_format(name, rows)

    lo_rows = tables[LO_LEVEL["name"]]
    issues += check_duplicate_codes(LO_LEVEL["name"], lo_rows)
    issues += check_empty_required(LO_LEVEL["name"], lo_rows)
    issues += check_code_format(LO_LEVEL["name"], lo_rows)

    for lvl in LEVELS:
        if lvl["parent_field"] is None:
            continue
        issues += check_referential_integrity(lvl["name"], tables[lvl["name"]], lvl["parent_field"],
                                               code_sets[lvl["parent_level"]])
    issues += check_referential_integrity(LO_LEVEL["name"], lo_rows, LO_LEVEL["parent_field"],
                                           code_sets[LO_LEVEL["parent_level"]])

    issues += check_lo_parent_and_cycles(lo_rows, code_sets[LO_LEVEL["name"]])
    issues += check_lo_type_rules(lo_rows)
    issues += check_lo_concept_codes(lo_rows, code_sets.get("concepts", set()))
    issues += check_concept_lo_coverage(tables.get("concepts", []), lo_rows)
    issues += check_cio_sio_depth(lo_rows, min_sios=2)

    for i in range(len(ALL_LEVELS) - 1):
        parent_lvl, child_lvl = ALL_LEVELS[i], ALL_LEVELS[i + 1]
        referenced = set()
        for r in tables[child_lvl["name"]]:
            referenced |= set(split_codes(r.get(child_lvl["parent_field"], "")))
        issues += check_orphans(parent_lvl["name"], code_sets[parent_lvl["name"]], referenced)

    issues += check_line_endings(data_dir, [lvl["file"] for lvl in ALL_LEVELS])
    return issues


# ---------------------------------------------------------------------------
# Safe auto-fix: chuẩn hoá cell (dedupe + separator) — không đổi ý nghĩa dữ liệu
# ---------------------------------------------------------------------------

def apply_safe_fixes(data_dir: Path, tables, fieldnames_map, issues, backup_dir: Path):
    """Chuẩn hoá các cell bị SEPARATOR_FORMAT / DUPLICATE_REF_IN_CELL.
    Trả về (applied_fix_records, changed_files)."""
    targets = {}  # (level_name, code, field) -> True, cần chuẩn hoá
    for i in issues:
        if i.rule_id in SAFE_FIX_RULES:
            targets[(i.level, i.code, i.field)] = True

    applied = []
    changed_levels = set()

    level_by_name = {lvl["name"]: lvl for lvl in ALL_LEVELS}

    for (level_name, code, field), _ in targets.items():
        lvl = level_by_name.get(level_name)
        if lvl is None or field is None:
            continue
        for row in tables[level_name]:
            if (row.get("code") or "").strip() != code:
                continue
            old_val = row.get(field, "") or ""
            pieces = split_codes(old_val)  # đã: normalize separator, trim, drop empty
            # dedupe giữ thứ tự xuất hiện đầu tiên
            deduped = list(dict.fromkeys(pieces))
            new_val = ", ".join(deduped)
            if new_val != old_val:
                row[field] = new_val
                applied.append({
                    "level": level_name, "code": code, "field": field,
                    "old_value": old_val, "new_value": new_val,
                })
                changed_levels.add(level_name)

    # ghi backup + ghi đè file cho các level bị thay đổi
    for level_name in changed_levels:
        lvl = level_by_name[level_name]
        path = data_dir / lvl["file"]
        if path.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            (backup_dir / lvl["file"]).write_bytes(path.read_bytes())
        write_tsv_rows(path, fieldnames_map[level_name], tables[level_name])

    return applied, changed_levels


# ---------------------------------------------------------------------------
# Proposed fixes (cần suy luận) — KHÔNG ghi đè file, chỉ đề xuất
# ---------------------------------------------------------------------------

def propose_fixes(issues, code_sets):
    proposals = []

    for i in issues:
        if i.rule_id == "BROKEN_REFERENCE":
            level_by_name = {lvl["name"]: lvl for lvl in ALL_LEVELS}
            lvl = level_by_name.get(i.level)
            parent_codes = code_sets.get(lvl["parent_level"], set()) if lvl else set()
            matches = difflib.get_close_matches(i.ref, sorted(parent_codes), n=3, cutoff=0.6)
            suggestions = []
            for m in matches:
                ratio = difflib.SequenceMatcher(None, i.ref, m).ratio()
                suggestions.append({"suggested_value": m, "confidence": round(ratio, 3)})
            proposals.append({
                "rule_id": i.rule_id, "level": i.level, "code": i.code, "field": i.field,
                "broken_ref": i.ref,
                "suggestions": suggestions if suggestions else None,
                "note": None if suggestions else "Không tìm thấy code nào đủ giống — cần bổ sung thủ công.",
                "status": "pending_review",
            })

        elif i.rule_id == "LO_TYPE_PARENT_MISMATCH":
            proposals.append({
                "rule_id": i.rule_id, "level": i.level, "code": i.code,
                "options": [
                    {"change_field": "parent_lo_code", "new_value": "NULL",
                     "rationale": "Giữ lo_type hiện tại là UNIVERSAL, xoá parent."},
                    {"change_field": "lo_type", "new_value": "CONCEPTUAL_IMPL hoặc SPECIFIC_IMPL",
                     "rationale": "Giữ parent_lo_code hiện tại, đổi lo_type cho khớp."},
                ] if i.message.startswith("lo_type=UNIVERSAL") else [
                    {"change_field": "lo_type", "new_value": "UNIVERSAL",
                     "rationale": "Giữ parent_lo_code=NULL, đổi lo_type thành UNIVERSAL."},
                    {"change_field": "parent_lo_code", "new_value": "<cần chọn 1 LO cha phù hợp>",
                     "rationale": "Giữ lo_type hiện tại, gán 1 parent_lo_code hợp lệ."},
                ],
                "status": "pending_review",
            })
    return proposals


def render_proposed_fixes_md(proposals):
    lines = ["# Đề xuất sửa lỗi (chờ duyệt)", ""]
    if not proposals:
        lines.append("_Không có đề xuất nào._")
        return "\n".join(lines)
    for p in proposals:
        lines.append(f"## `{p['rule_id']}` — {p['level']} / `{p['code']}`")
        if "broken_ref" in p:
            lines.append(f"- Tham chiếu gãy: `{p['broken_ref']}` (cột `{p['field']}`)")
            if p["suggestions"]:
                lines.append("- Gợi ý:")
                for s in p["suggestions"]:
                    lines.append(f"  - `{s['suggested_value']}` (độ giống: {s['confidence']})")
            else:
                lines.append(f"- {p['note']}")
        if "options" in p:
            lines.append("- Phương án:")
            for o in p["options"]:
                lines.append(f"  - Đổi `{o['change_field']}` → `{o['new_value']}` — {o['rationale']}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report rendering (giữ như v1)
# ---------------------------------------------------------------------------

def build_summary(issues, tables):
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]
    by_rule, by_level = {}, {}
    for i in issues:
        by_rule[i.rule_id] = by_rule.get(i.rule_id, 0) + 1
        by_level.setdefault(i.level, {"ERROR": 0, "WARNING": 0})
        by_level[i.level][i.severity] += 1
    return {
        "status": "FAIL" if errors else "PASS",
        "total_issues": len(issues), "errors": len(errors), "warnings": len(warnings),
        "by_rule": by_rule, "by_level": by_level,
        "node_counts": {name: len(rows) for name, rows in tables.items()},
    }


def render_json(issues, tables, generated_at, extra=None):
    payload = {
        "generated_at": generated_at,
        "summary": build_summary(issues, tables),
        "rule_descriptions": RULE_DESCRIPTIONS,
        "issues": [i.to_dict() for i in issues],
    }
    if extra:
        payload.update(extra)
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_markdown(issues, tables, generated_at):
    summary = build_summary(issues, tables)
    lines = ["# Báo cáo kiểm tra Knowledge Tree", "",
             f"- **Thời gian chạy:** {generated_at}",
             f"- **Kết quả:** {'✅ PASS' if summary['status'] == 'PASS' else '❌ FAIL'}",
             f"- **Tổng số issue:** {summary['total_issues']} ({summary['errors']} lỗi, {summary['warnings']} cảnh báo)",
             ""]
    lines += ["## Số lượng node theo tầng", "", "| Tầng | Số node |", "|---|---|"]
    lines += [f"| {n} | {c} |" for n, c in summary["node_counts"].items()]
    lines.append("")
    lines += ["## Tổng hợp theo rule", "", "| Rule | Mô tả | Số lượng |", "|---|---|---|"]
    for rule_id, count in sorted(summary["by_rule"].items(), key=lambda x: -x[1]):
        lines.append(f"| `{rule_id}` | {RULE_DESCRIPTIONS.get(rule_id, '')} | {count} |")
    lines.append("")
    for severity, title in (("ERROR", "## ❌ Lỗi (ERROR) — cần sửa"), ("WARNING", "## ⚠️ Cảnh báo (WARNING)")):
        group = [i for i in issues if i.severity == severity]
        lines.append(title)
        lines.append("")
        if not group:
            lines += ["_Không có._", ""]
            continue
        by_rule = {}
        for i in group:
            by_rule.setdefault(i.rule_id, []).append(i)
        for rule_id, items in sorted(by_rule.items(), key=lambda x: -len(x[1])):
            lines.append(f"### `{rule_id}` ({len(items)}) — {RULE_DESCRIPTIONS.get(rule_id, '')}")
            lines += ["", "| Tầng | Code | Cột | Chi tiết |", "|---|---|---|---|"]
            for i in items[:200]:
                lines.append(f"| {i.level} | `{i.code}` | {i.field or '-'} | {i.message} |")
            if len(items) > 200:
                lines.append(f"| ... | ... | ... | (+{len(items) - 200} dòng nữa) |")
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Kiểm tra / sửa lỗi Knowledge Tree (TSV).")
    ap.add_argument("--repo-root", default=None, help="Gốc repo (mặc định: tự tìm thư mục chứa .agents/)")
    ap.add_argument("--project", default=None, help="Project slug (mặc định: đọc active_project trong status.yaml)")
    ap.add_argument("--data-dir", default=None, help="Dùng trực tiếp 1 thư mục TSV, bỏ qua project/status.yaml")
    ap.add_argument("--output-dir", default=None, help="Chỉ dùng cùng --data-dir; nơi xuất report ad-hoc")
    ap.add_argument("--fix", action="store_true", help="Áp dụng auto-fix an toàn + sinh đề xuất fix cần duyệt")
    ap.add_argument("--fail-on", choices=["error", "warning", "none"], default="error")
    args = ap.parse_args()

    data_dir, project_dir, slug = resolve_data_dir(args)
    generated_at = now_iso()

    tables, fieldnames_map, code_sets, load_issues = load_all(data_dir)
    issues = load_issues + run_checks(data_dir, tables, code_sets)

    applied_fixes, proposals = [], []

    if args.fix and project_dir is not None:
        artifact_paths = scaffold_project_artifacts(project_dir, need_fix_dirs=True)
        applied_fixes, changed_levels = apply_safe_fixes(
            data_dir, tables, fieldnames_map, issues, artifact_paths["backup_dir"])
        if applied_fixes:
            # re-validate sau khi fix để số liệu report phản ánh đúng trạng thái mới
            tables, fieldnames_map, code_sets, load_issues = load_all(data_dir)
            issues = load_issues + run_checks(data_dir, tables, code_sets)
        proposals = propose_fixes(issues, code_sets)

        (artifact_paths["fix_dir"] / "applied_fixes.json").write_text(
            json.dumps(applied_fixes, ensure_ascii=False, indent=2), encoding="utf-8")
        (artifact_paths["fix_dir"] / "proposed_fixes.json").write_text(
            json.dumps(proposals, ensure_ascii=False, indent=2), encoding="utf-8")
        (artifact_paths["fix_dir"] / "proposed_fixes.md").write_text(
            render_proposed_fixes_md(proposals), encoding="utf-8")

        report_dir = artifact_paths["report_dir"]
    elif project_dir is not None:
        artifact_paths = scaffold_project_artifacts(project_dir)
        report_dir = artifact_paths["report_dir"]
    else:
        report_dir = Path(args.output_dir).resolve() if args.output_dir else data_dir
        report_dir.mkdir(parents=True, exist_ok=True)

    json_report = render_json(issues, tables, generated_at)
    md_report = render_markdown(issues, tables, generated_at)
    (report_dir / "validation_report.json").write_text(json_report, encoding="utf-8")
    (report_dir / "validation_report.md").write_text(md_report, encoding="utf-8")

    summary = build_summary(issues, tables)

    if project_dir is not None:
        no_fix_issue_count = len([i for i in issues if i.severity == "ERROR"
                                   and i.rule_id not in SAFE_FIX_RULES | PROPOSE_FIX_RULES])
        repo_root = project_dir.parent.parent
        status_path = repo_root / "status.yaml"
        status = read_status_yaml(status_path)
        status["active_project"] = slug
        status["last_validated_at"] = generated_at
        status["last_validation_status"] = summary["status"]
        status["last_report_path"] = str((report_dir / "validation_report.md").relative_to(repo_root))
        status["pending_manual_fixes"] = no_fix_issue_count
        status["pending_proposed_fixes"] = len(proposals)
        if args.fix:
            status["proposed_fixes_path"] = str(
                (artifact_paths["fix_dir"] / "proposed_fixes.md").relative_to(repo_root))
        status_path.parent.mkdir(parents=True, exist_ok=True)
        write_status_yaml(status_path, status)

    print(f"[{summary['status']}] {summary['errors']} lỗi, {summary['warnings']} cảnh báo"
          + (f" | auto-fixed: {len(applied_fixes)} cell | đề xuất chờ duyệt: {len(proposals)}"
             if args.fix else "")
          + f" — report tại {report_dir}")

    if args.fail_on == "error" and summary["errors"] > 0:
        sys.exit(1)
    if args.fail_on == "warning" and summary["total_issues"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
