#!/usr/bin/env python3
"""
detect_gaps.py — Gap Detection Tool cho Knowledge Tree.

Phát hiện 4 loại gap:
  Gap A (CONCEPT_WITHOUT_LO):  Concept trong project chưa có LO nào trỏ đến.
  Gap B (CIO_SHALLOW):         CIO có ít hơn 2 SIO con → phân rã chưa đủ sâu.
  Gap D (MARR_VIOLATION):      CIO vi phạm Phép thử Marr 2-Ngôn-ngữ (chứa tên công nghệ/cú pháp ngôn ngữ cụ thể).
  Gap C (MASTER_CANDIDATE):    Concept từ master_tree.json liên quan đến syllabus
                               nhưng chưa được đưa vào project taxonomy.

Chạy: python3 detect_gaps.py --project <slug>
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─── Helpers ─────────────────────────────────────────────────────────────────

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


def load_tsv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def split_codes(value: str) -> list[str]:
    if not value:
        return []
    return [c.strip() for c in value.replace(";", ",").split(",") if c.strip()]


def load_syllabus_text(work_dir: Path) -> str:
    """Load raw syllabus text for keyword matching."""
    for fname in ("raw_pdf.txt", "context-audit.md"):
        p = work_dir / fname
        if p.is_file():
            return p.read_text(encoding="utf-8").lower()
    return ""


STOP_WORDS = {
    "and", "the", "for", "with", "use", "using", "create", "summarize",
    "assess", "differentiate", "select", "appropriate", "actions", "when",
    "how", "are", "from", "that", "this", "will", "have", "not", "but",
    "can", "its", "also", "into", "such", "each", "than", "more", "over",
}


def keyword_score(concept: dict, syllabus_text: str) -> tuple[float, list[str]]:
    """Score a master concept's relevance to syllabus text. Returns (score, hits)."""
    name_words = [w.lower() for w in re.findall(r"[a-zA-Z]{3,}", concept.get("name", ""))]
    kw_words = [k.strip().lower() for k in concept.get("keywords", "").split(",") if k.strip()]
    desc_words = [w.lower() for w in re.findall(r"[a-zA-Z]{4,}", concept.get("description", ""))]

    score = 0.0
    hits = []

    for kw in kw_words:
        if len(kw) > 3 and kw not in STOP_WORDS and kw in syllabus_text:
            score += 1.5
            hits.append(kw)

    for w in name_words:
        if len(w) > 3 and w not in STOP_WORDS and w in syllabus_text:
            score += 0.8
            if w not in hits:
                hits.append(w)

    for w in desc_words[:10]:
        if w not in STOP_WORDS and w in syllabus_text:
            score += 0.3

    return round(score, 2), hits[:6]


# ─── Gap A: Concepts without LOs ─────────────────────────────────────────────

def detect_concept_without_lo(
    project_concepts: list[dict],
    project_los: list[dict],
) -> list[dict]:
    """Return concepts that no LO points to."""
    covered = set()
    for lo in project_los:
        for c in split_codes(lo.get("concept_codes", "")):
            covered.add(c)

    gaps = []
    for concept in project_concepts:
        code = (concept.get("code") or "").strip()
        if code and code not in covered:
            gaps.append({
                "code": code,
                "name": concept.get("name", ""),
                "topic_codes": concept.get("topic_codes", ""),
            })
    return gaps


# ─── Gap B: CIOs with fewer than 2 SIOs ──────────────────────────────────────

def detect_shallow_cios(project_los: list[dict], min_sios: int = 2) -> list[dict]:
    """Return CIOs with fewer than min_sios SIO children.
    N:N aware: a SIO with comma-separated parents counts toward each parent CIO."""
    cios = {r["code"]: r for r in project_los if r.get("lo_type") == "CONCEPTUAL_IMPL" and r.get("code")}
    sios = [r for r in project_los if r.get("lo_type") == "SPECIFIC_IMPL"]

    cio_sio_count: dict[str, int] = {c: 0 for c in cios}
    for sio in sios:
        # N:N: split comma-separated parents so multi-parent SIOs count for each CIO.
        for parent in split_codes(sio.get("parent_lo_code", "")):
            if parent in cio_sio_count:
                cio_sio_count[parent] += 1

    shallow = []
    for cio_code, count in cio_sio_count.items():
        if count < min_sios:
            shallow.append({
                "code": cio_code,
                "name": cios[cio_code].get("name", ""),
                "sio_count": count,
                "parent_ulo": (cios[cio_code].get("parent_lo_code") or "").strip(),
            })
    return shallow


# ─── Gap D: CIOs violating Marr's Representation-Independent test ─────────────
#
# TECH_KEYWORDS: concrete language/framework/brand names that MUST NOT appear
# in a CIO (which is supposed to be language-neutral per T6). Matched as whole
# words, case-insensitive. Ambiguous tokens (e.g. "spring" the season, "r" the
# letter) are intentionally omitted to avoid false positives.
TECH_KEYWORDS = {
    # languages
    "python", "swift", "javascript", "typescript", "java", "golang", "rust",
    "ruby", "php", "kotlin", "scala", "perl", "lua", "haskell", "dart",
    "c++", "cpp", "c#", "csharp", "objective-c", "objc",
    # frameworks / libraries
    "react", "vue", "vue.js", "angular", "svelte", "solidjs", "solid js",
    "django", "flask", "express", "rails", "laravel", "nextjs", "next.js",
    "nuxt", "gatsby", "tailwind", "bootstrap",
    # platforms / vendors
    "arduino", "raspberry pi", "esp32", "esp8266", "node.js", "nodejs",
    "docker", "kubernetes", "k8s",
    # specific syntax tokens (unambiguous)
    "codable", "getelementbyid", "innerhtml", "console.log",
    "printf", "scanf", "std::", "malloc",
}

SYNTAX_PATTERNS = [
    (r'(?:\bc\+\+|\bcpp\b)', "c++"),
    (r'(?:\bc#|\bcsharp\b)', "c#"),
    (r'\bclass\s+\w+\s*\(\s*\w+\s*\)', "syntax: class Child(Parent)"),
    (r'\bdef\s+\w+', "syntax: def function"),
    (r'\bfunc\s+\w+', "syntax: func function"),
    (r'\bfn\s+\w+', "syntax: fn function"),
    (r'\bimport\s+\w+', "syntax: import statement"),
    (r'\bfrom\s+\w+\s+import\b', "syntax: from ... import"),
    (r'\bconsole\.log\b', "syntax: console.log"),
    (r'\bstd::', "syntax: std:: namespace"),
    (r'\bmalloc\s*\(', "syntax: malloc call"),
    (r'\bprintf\s*\(', "syntax: printf call"),
    (r'\bawait\s+\w+', "syntax: await expression"),
    (r'\basync\s+function\b', "syntax: async function"),
    (r'=>\s*\{', "syntax: arrow function body"),
    (r'\bpublic\s+static\s+void\s+main\b', "syntax: Java main"),
    (r'\bprintln!\s*\(', "syntax: Rust println! macro"),
]

def detect_non_neutral_cios(project_los: list[dict]) -> list[dict]:
    """Return CIOs containing technology/syntax-specific tokens violating Marr's test."""
    cios = [r for r in project_los if r.get("lo_type") == "CONCEPTUAL_IMPL"]
    violations = []
    for cio in cios:
        text = (cio.get("name", "") + " " + cio.get("description", "")).lower()
        found_kw = []
        for kw in TECH_KEYWORDS:
            # Use word-boundary regex for reliable matching (handles c++, c#, etc.)
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                found_kw.append(kw)

        for pattern, label in SYNTAX_PATTERNS:
            if re.search(pattern, text):
                if label not in found_kw:
                    found_kw.append(label)

        if found_kw:
            violations.append({
                "code": cio.get("code", ""),
                "name": cio.get("name", ""),
                "keywords": found_kw
            })
    return violations


def detect_marr_test_note_quality(project_los: list[dict]) -> list[dict]:
    """Check CIOs for Marr 2-Language Test note quality (Gap E).
    Each CIO must have a marr_test_note mentioning ≥2 distinct languages."""
    # Common programming language names to detect in marr_test_note
    LANGUAGE_PATTERNS = [
        r'\bpython\b', r'\bswift\b', r'\bjavascript\b', r'\btypescript\b', r'\bjava\b',
        r'\bgolang\b', r'\bgo\b', r'\brust\b', r'\bruby\b', r'\bphp\b', r'\bkotlin\b',
        r'\bscala\b', r'\bperl\b', r'\blua\b', r'\bhaskell\b', r'\bdart\b',
        r'\bc\+\+\b', r'\bcpp\b', r'\bc#\b', r'\bcsharp\b', r'\bobjective-c\b', r'\bobjc\b',
        r'\bc\b(?![a-z])',  # C language (not followed by letter)
    ]
    
    LANGUAGE_RE = re.compile('|'.join(LANGUAGE_PATTERNS), re.IGNORECASE)
    
    cios = [r for r in project_los if r.get("lo_type") == "CONCEPTUAL_IMPL"]
    issues = []
    for cio in cios:
        note = (cio.get("marr_test_note") or "").strip()
        code = cio.get("code", "")
        name = cio.get("name", "")
        
        if not note:
            issues.append({
                "code": code,
                "name": name,
                "issue": "MISSING_MARR_NOTE",
                "detail": "CIO thiếu trường marr_test_note (bắt buộc theo Marr 2-Language Test [T6])"
            })
            continue
        
        # Find language mentions in the note
        found_langs = set()
        for match in LANGUAGE_RE.finditer(note):
            found_langs.add(match.group(0).lower())
        
        # Normalize some aliases
        lang_map = {
            'go': 'golang',
            'c++': 'cpp',
            'c#': 'csharp',
            'objc': 'objective-c',
            'c': 'c',
        }
        normalized_langs = {lang_map.get(l, l) for l in found_langs}
        
        if len(normalized_langs) < 2:
            issues.append({
                "code": code,
                "name": name,
                "issue": "INSUFFICIENT_LANGUAGES_IN_MARR_NOTE",
                "detail": f"marr_test_note chỉ nhắc đến {len(normalized_langs)} ngôn ngữ ({', '.join(normalized_langs) if normalized_langs else 'không có'}), cần ≥ 2. Note: {note[:100]}"
            })
    return issues


# ─── Gap C: Master Tree Candidates ───────────────────────────────────────────

def detect_master_candidates(
    master_concepts: list[dict],
    project_concept_codes: set[str],
    syllabus_text: str,
    min_score: float = 2.0,
    top_n: int = 20,
) -> list[dict]:
    """Return master concepts not in project but relevant to syllabus."""
    candidates = []
    for concept in master_concepts:
        code = (concept.get("code") or "").strip()
        if not code or code in project_concept_codes:
            continue
        score, hits = keyword_score(concept, syllabus_text)
        if score >= min_score:
            candidates.append({
                "code": code,
                "name": concept.get("name", ""),
                "description": concept.get("description", ""),
                "topic_codes": concept.get("topic_codes", ""),
                "score": score,
                "matching_keywords": hits,
            })

    candidates.sort(key=lambda x: -x["score"])
    return candidates[:top_n]


# ─── Report Rendering ─────────────────────────────────────────────────────────

def render_report(
    slug: str,
    gap_a: list[dict],
    gap_b: list[dict],
    gap_d: list[dict],
    gap_e: list[dict],  # New: Gap E - Marr Test Note Quality
    gap_c: list[dict],
    min_score: float,
) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Gap Detection Report",
        "",
        f"- **Project:** `{slug}`",
        f"- **Generated:** {now}",
        "",
        "---",
        "",
        "## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)",
        "",
        f"> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.",
        "",
    ]

    if gap_a:
        lines += [
            f"**{len(gap_a)} concept(s) không có LO:**",
            "",
            "| Code | Name | Parent Topic |",
            "|---|---|---|",
        ]
        for g in gap_a:
            lines.append(f"| `{g['code']}` | {g['name']} | `{g['topic_codes']}` |")
        lines.append("")
        lines.append("**→ Action:** Thêm ít nhất 1 ULO + 1 CIO + 2 SIO cho mỗi concept trên.")
    else:
        lines += ["✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**", ""]

    lines += [
        "---",
        "",
        "## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)",
        "",
        "> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.",
        "",
    ]

    if gap_b:
        lines += [
            f"**{len(gap_b)} CIO(s) có < 2 SIO:**",
            "",
            "| CIO Code | CIO Name | SIO Count | Parent ULO |",
            "|---|---|---|---|",
        ]
        for g in gap_b:
            sio_display = f"{'⚠️ ' if g['sio_count'] == 1 else '❌ '}{g['sio_count']}"
            lines.append(f"| `{g['code']}` | {g['name']} | {sio_display} | `{g['parent_ulo']}` |")
        lines.append("")
        lines.append("**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.")
    else:
        lines += ["✅ **Tất cả CIOs đều có ít nhất 2 SIO con.**", ""]

    lines += [
        "---",
        "",
        "## Gap D — Marr's Test Violated CIOs (`MARR_VIOLATION`)",
        "",
        "> CIO chứa từ khóa công nghệ, cú pháp hoặc cấu trúc ngôn ngữ cụ thể — vi phạm Phép thử Marr 2-Ngôn-ngữ.",
        "",
    ]

    if gap_d:
        lines += [
            f"**{len(gap_d)} CIO(s) vi phạm tính Trung tính (Marr Test):**",
            "",
            "| CIO Code | CIO Name | Detected Keywords / Patterns |",
            "|---|---|---|",
        ]
        for g in gap_d:
            kws = ", ".join(f"`{k}`" for k in g["keywords"])
            lines.append(f"| `{g['code']}` | {g['name']} | {kws} |")
        lines.append("")
        lines.append("**→ Action:** Viết lại mô tả/tên CIO thành khái niệm/thủ tục trung tính 100% độc lập ngôn ngữ, hoặc chuyển xuống tầng SIO.")
    else:
        lines += ["✅ **Tất cả CIOs đều đạt Phép thử Marr (100% Trung tính).**", ""]

    lines += [
        "---",
        "",
        "## Gap E — Marr Test Note Quality (`MARR_NOTE_QUALITY`)",
        "",
        "> CIO có marr_test_note nhưng note không đủ chất lượng (thiếu note, hoặc nhắc < 2 ngôn ngữ).",
        "> Theo T6: CIO bắt buộc phải pass Marr 2-Language Test — note phải chứng minh mapping ≥ 2 ngôn ngữ.",
        "",
    ]

    if gap_e:
        lines += [
            f"**{len(gap_e)} CIO(s) có vấn đề với marr_test_note:**",
            "",
            "| CIO Code | CIO Name | Issue | Detail |",
            "|---|---|---|---|",
        ]
        for g in gap_e:
            lines.append(f"| `{g['code']}` | {g['name']} | {g['issue']} | {g['detail'][:120]} |")
        lines.append("")
        lines.append("**→ Action:** Bổ sung/sửa marr_test_note để nhắc rõ ràng ≥ 2 ngôn ngữ khác nhau (ví dụ: 'Áp dụng được cho Python vì... và Swift vì...').")
    else:
        lines += ["✅ **Tất cả CIOs đều có marr_test_note đạt chuẩn (≥ 2 ngôn ngữ).**", ""]

    lines += [
        "---",
        "",
        "## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)",
        "",
        f"> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ {min_score}).",
        "> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.",
        "",
    ]

    if gap_c:
        lines += [
            f"**{len(gap_c)} candidate(s) từ Master Tree:**",
            "",
            "| Score | Code | Name | Matching Keywords |",
            "|---|---|---|---|",
        ]
        for g in gap_c:
            kws = ", ".join(f"`{k}`" for k in g["matching_keywords"])
            lines.append(f"| {g['score']} | `{g['code']}` | {g['name']} | {kws} |")
        lines.append("")
        lines.append(
            "**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`."
        )
    else:
        lines += [f"✅ **Không tìm thấy master concept nào có score ≥ {min_score} chưa được chọn.**", ""]

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Detect 4 types of gaps in the project Knowledge Tree."
    )
    parser.add_argument("--project", type=str, help="Project slug")
    parser.add_argument(
        "--min-score", type=float, default=2.0,
        help="Minimum keyword score for Master Candidate detection (default: 2.0)"
    )
    parser.add_argument(
        "--top-n", type=int, default=20,
        help="Max number of master candidates to report (default: 20)"
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())

    slug = args.project
    if not slug:
        st = load_status(repo_root)
        slug = st.get("active_project")
        if not slug:
            print("❌ Error: Không có project. Truyền --project hoặc set active_project trong status.yaml.")
            sys.exit(1)

    project_dir = repo_root / "projects" / slug
    out_dir = project_dir / "output"
    work_dir = project_dir / ".work"
    master_json = repo_root / ".agents/skills/taxonomy-mapper/resources/master_tree.json"

    # Load data
    project_concepts = load_tsv(out_dir / "concepts.tsv")
    project_los = load_tsv(out_dir / "learning-objectives.tsv")

    if not project_concepts:
        print(f"⚠️  concepts.tsv không tìm thấy. Chạy /build-tree trước.")
    if not project_los:
        print(f"⚠️  learning-objectives.tsv không tìm thấy. Chạy /generate-los trước.")

    master_concepts = []
    if master_json.is_file():
        with open(master_json, "r", encoding="utf-8") as f:
            master = json.load(f)
        master_concepts = master.get("concepts", [])

    syllabus_text = load_syllabus_text(work_dir)
    if not syllabus_text:
        print("⚠️  Syllabus text không tìm thấy. Gap C sẽ không có kết quả.")

    project_concept_codes = {(r.get("code") or "").strip() for r in project_concepts}

    # Detect gaps
    gap_a = detect_concept_without_lo(project_concepts, project_los)
    gap_b = detect_shallow_cios(project_los, min_sios=2)
    gap_d = detect_non_neutral_cios(project_los)
    gap_e = detect_marr_test_note_quality(project_los)  # New: Marr test note quality
    gap_c = detect_master_candidates(
        master_concepts, project_concept_codes, syllabus_text,
        min_score=args.min_score, top_n=args.top_n
    )

    # Print summary
    print(f"\n{'='*54}")
    print(f"🔍 GAP DETECTION RESULTS for '{slug}'")
    print(f"{'='*54}")
    status_a = "❌" if gap_a else "✅"
    status_b = "⚠️ " if gap_b else "✅"
    status_d = "❌" if gap_d else "✅"
    status_e = "⚠️ " if gap_e else "✅"
    status_c = "ℹ️ " if gap_c else "✅"
    print(f"  {status_a} Gap A (Concepts without LO):       {len(gap_a)}")
    if gap_a:
        for g in gap_a:
            print(f"       • {g['code']}: {g['name']}")
    print(f"  {status_b} Gap B (Shallow CIOs < 2 SIO):      {len(gap_b)}")
    if gap_b:
        for g in gap_b:
            print(f"       • {g['code']} ({g['sio_count']} SIO)")
    print(f"  {status_d} Gap D (Marr Test Violated CIOs): {len(gap_d)}")
    if gap_d:
        for g in gap_d:
            print(f"       • {g['code']}: contains {', '.join(g['keywords'])}")
    print(f"  {status_e} Gap E (Marr Test Note Quality):    {len(gap_e)}")
    if gap_e:
        for g in gap_e:
            print(f"       • {g['code']}: {g['issue']} - {g['detail'][:80]}")
    print(f"  {status_c} Gap C (Master Candidates):         {len(gap_c)}")

    if gap_c:
        for g in gap_c[:5]:
            print(f"       • [{g['score']}] {g['code']}: {g['name']}")
        if len(gap_c) > 5:
            print(f"       ... và {len(gap_c) - 5} candidate(s) khác (xem report)")
    print(f"{'='*54}")

    # Write reports
    report_content = render_report(slug, gap_a, gap_b, gap_d, gap_e, gap_c, args.min_score)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_dir = project_dir / ".tree-validator" / "reports" / stamp
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "gap_report.md"
    work_copy = work_dir / "gap_report.md"
    report_path.write_text(report_content, encoding="utf-8")
    work_dir.mkdir(parents=True, exist_ok=True)
    work_copy.write_text(report_content, encoding="utf-8")

    print(f"\n  • Report: {report_path.relative_to(repo_root)}")
    print(f"  • Work copy: {work_copy.relative_to(repo_root)}")
    print(f"{'='*54}\n")


if __name__ == "__main__":
    main()
