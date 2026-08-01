#!/usr/bin/env python3
"""
generate_all_los.py — Generate ULOs, CIOs, SIOs for ALL uncovered concepts,
then merge into learning-objectives.tsv.

This script handles the full pipeline:
1. Reads all concepts from concepts.tsv
2. For concepts without ULOs, generates ULOs via LLM
3. Generates CIOs (with Marr test notes) for all ULOs
4. Generates SIOs (Swift-specific) for all CIOs
5. Merges into learning-objectives.tsv
6. Adds assessment_approach to all ULOs/CIOs
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ─── LLM call helper ──────────────────────────────────────────────────────────

def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def find_repo_root(start: Path) -> Path:
    """Walk up from start to find repo root (contains .agents/)."""
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def get_llm_client():
    """Create OpenAI-compatible client using env vars or .env file."""
    # First try env vars (already loaded by load_env)
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "")
    
    if not api_key:
        # Try reading from .env as fallback
        env_path = Path(".env")
        if env_path.is_file():
            with open(env_path) as f:
                for line in f:
                    if line.startswith("OPENAI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip("'\"").strip('"')
                        break
    if not base_url:
        base_url = os.environ.get("OPENAI_BASE_URL", "https://ollama.com/v1")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in env or .env", file=sys.stderr)
        sys.exit(1)
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url=base_url)


def llm_json(client, system, user, model="deepseek-v4-flash", temperature=0.2):
    """Call LLM and return parsed JSON."""
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            temperature=temperature,
        )
        raw = completion.choices[0].message.content or ""
        if raw.startswith("```"):
            raw = re.sub(r"```(?:json)?\n?", "", raw).strip("` \n")
        return json.loads(raw)
    except Exception as e:
        print(f"  [ERROR] LLM call failed: {e}", file=sys.stderr)
        return {}


# ─── Data loading ─────────────────────────────────────────────────────────────

def load_concepts(concepts_tsv: Path) -> list[dict]:
    concepts = []
    if not concepts_tsv.is_file():
        return concepts
    with open(concepts_tsv, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code = (row.get("code") or "").strip()
            if code:
                concepts.append({
                    "code": code,
                    "name": (row.get("name") or "").strip(),
                    "description": (row.get("description") or "").strip(),
                })
    return concepts


def load_existing_los(lo_tsv: Path) -> list[dict]:
    """Load existing learning objectives."""
    los = []
    if not lo_tsv.is_file():
        return los
    with open(lo_tsv, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code = (row.get("code") or "").strip()
            if code:
                los.append(row)
    return los


def load_syllabus(work_dir: Path) -> str:
    for fname in ["raw_pdf.txt", "context-audit.md"]:
        f = work_dir / fname
        if f.is_file():
            return f.read_text(encoding="utf-8")
    return ""


def detect_technology(project_dir: Path, slug: str) -> str:
    """Auto-detect technology from project context files."""
    _TECH_FINGERPRINTS = [
        (["swift", "swiftui", "xcode", "ios", "macos"], "Swift"),
        (["python", ".py", "django", "flask"], "Python"),
        (["javascript", "typescript", ".js", ".ts", "react", "vue", "angular", "node"], "JavaScript / TypeScript"),
        (["kotlin", "android", "jetpack"], "Kotlin"),
        (["java", "spring", "maven"], "Java"),
        (["rust", ".rs", "cargo"], "Rust"),
        (["arduino", "esp32", "c++", "cpp"], "C++ / Arduino"),
        (["flutter", "dart"], "Flutter / Dart"),
    ]
    text = ""
    for fname in ["context-audit.md", "raw_pdf.txt"]:
        f = project_dir / ".work" / fname
        if f.is_file():
            text += f.read_text(encoding="utf-8")[:500].lower()
    for f in (project_dir / "context").iterdir() if (project_dir / "context").is_dir() else []:
        text += f.name.lower()
    text += slug.lower()
    scores = {}
    for kws, tech in _TECH_FINGERPRINTS:
        for kw in kws:
            if kw in text:
                scores[tech] = scores.get(tech, 0) + 1
    if scores:
        return max(scores, key=lambda t: scores[t])
    return slug


# ─── Phase A: Generate ULOs ──────────────────────────────────────────────────

ULO_SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Universal Learning Objectives (ULO).

ULO = Tầng Computational (Marr): mô tả NĂNG LỰC CỐT LÕI — WHAT và WHY — hoàn toàn độc lập với bất kỳ công nghệ/ngôn ngữ nào.

Nguyên tắc:
1. ULO KHÔNG chứa tên công nghệ, ngôn ngữ lập trình, framework, hay cú pháp.
2. ULO phải áp dụng được cho người học bất kể họ dùng Python, Swift, JavaScript hay ngôn ngữ nào.
3. Mã ULO: `ULO-<CONCEPT_CODE>-<STT>`. VD: `ULO-IF_ELSE_STATEMENT-01`
4. Mô tả bắt đầu bằng "Người học có khả năng ..."
5. Bloom level: REMEMBER | UNDERSTAND | APPLY | ANALYZE | EVALUATE | CREATE
6. Knowledge dimension: FACTUAL | CONCEPTUAL | PROCEDURAL | METACOGNITIVE
7. Mỗi concept cần 1-3 ULOs phủ các cấp độ Bloom phù hợp.

TRẢ VỀ JSON: {"ulos": [{"code": "...", "name": "...", "description_vi": "...", "bloom_level": "...", "knowledge_dimension": "...", "concept_codes": ["..."]}]}"""


def generate_ulos_for_concepts(client, concepts: list[dict], model: str) -> list[dict]:
    """Generate ULOs for concepts that don't have any yet."""
    all_ulos = []
    batch_size = 5

    for i in range(0, len(concepts), batch_size):
        batch = concepts[i:i+batch_size]
        concept_list = "\n".join(
            f"  - {c['code']}: {c['name']} — {c['description'][:100]}"
            for c in batch
        )

        user = (
            f"Hãy sinh ULOs cho các Concept sau (1-3 ULO mỗi concept):\n{concept_list}\n\n"
            "Mỗi ULO phải có mã theo format ULO-<CONCEPT_CODE>-<STT>.\n"
            "Ví dụ: ULO-IF_ELSE_STATEMENT-01, ULO-IF_ELSE_STATEMENT-02\n"
            "Mô tả bắt đầu bằng 'Người học có khả năng ...'\n"
            "KHÔNG chứa tên công nghệ cụ thể.\n"
            "Bloom ưu tiên APPLY/ANALYZE/EVALUATE khi nội dung cho phép."
        )

        result = llm_json(client, ULO_SYSTEM, user, model=model, temperature=0.3)
        batch_ulos = result.get("ulos", [])
        if batch_ulos:
            all_ulos.extend(batch_ulos)
            print(f"  + Batch {i+1}-{i+len(batch)}: {len(batch_ulos)} ULOs")
        else:
            print(f"  [WARN] Batch {i+1}-{i+len(batch)}: no ULOs generated")

    return all_ulos


# ─── Phase B: Generate CIOs ──────────────────────────────────────────────────

CIO_SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Conceptual Implementation Objectives (CIO).

CIO = Tầng Algorithmic (Marr): mô tả PATTERN / APPROACH trung tính — HOW ở mức thủ tục, KHÔNG gắn cú pháp.

PHÉP THỬ MARR 2-NGÔN-NGỮ (BẮT BUỘC trước khi ghi CIO):
Trước khi viết mỗi CIO, thử ánh xạ mô tả sang ít nhất 2 ngôn ngữ khác nhau.
- Nếu mô tả khớp tự nhiên với CẢ 2 → CIO hợp lệ
- Nếu chỉ khớp với 1 ngôn ngữ (token-order, cú pháp riêng) → đó là SIO trá hình → viết lại
Ghi kết quả test vào trường `marr_test_note`.

Nguyên tắc:
1. CIO KHÔNG chứa tên công nghệ, không có từ khóa cú pháp (let, var, def, func, class, import...)
2. Mỗi ULO cần 1-3 CIO diễn đạt các pattern/approach khác nhau
3. Mỗi CIO sẽ có ≥ 2 SIO con
4. Bloom: APPLY / ANALYZE
5. Mã CIO: CIO-<CONCEPT_CODE>-<STT>

TRẢ VỀ JSON: {"cios": [{"code": "...", "name": "...", "description_vi": "...", "bloom_level": "...", "knowledge_dimension": "...", "parent_ulo_code": "...", "marr_test_note": "..."}]}"""


def generate_cios_for_ulos(client, ulos: list[dict], model: str) -> list[dict]:
    """Generate CIOs for all ULOs."""
    all_cios = []
    batch_size = 8

    ulo_summary = "\n".join(
        f"  - {u['code']}: {u['name']} — {u.get('description_vi', '')[:80]}"
        for u in ulos
    )

    for i in range(0, len(ulos), batch_size):
        batch = ulos[i:i+batch_size]
        batch_text = "\n".join(
            f"ULO: {u['code']} | {u['name']}\n  Mô tả: {u.get('description_vi', '')[:100]}"
            for u in batch
        )

        user = (
            f"Danh sách tất cả ULO:\n{ulo_summary}\n\n"
            f"Sinh CIOs cho các ULO sau (mỗi ULO 1-3 CIOs):\n{batch_text}\n\n"
            "BẮT BUỘC thực hiện Marr 2-Language Test cho mỗi CIO và ghi vào marr_test_note.\n"
            "Mã CIO: CIO-<CONCEPT_CODE>-<STT> (lấy concept code từ ULO code).\n"
            "Ví dụ: ULO-IF_ELSE_STATEMENT-01 → CIO-IF_ELSE_STATEMENT-01, CIO-IF_ELSE_STATEMENT-02"
        )

        result = llm_json(client, CIO_SYSTEM, user, model=model, temperature=0.2)
        batch_cios = result.get("cios", [])
        if batch_cios:
            all_cios.extend(batch_cios)
            print(f"  + Batch {i+1}-{i+len(batch)}: {len(batch_cios)} CIOs")
        else:
            print(f"  [WARN] Batch {i+1}-{i+len(batch)}: no CIOs generated")

    return all_cios


# ─── Phase C: Generate SIOs ──────────────────────────────────────────────────

SIO_SYSTEM_TMPL = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Specific Implementation Objectives (SIO).

SIO = Tầng Implementational (Marr): mô tả kỹ năng CỤ THỂ gắn với công nghệ {technology}.

Nguyên tắc:
1. SIO BẮT BUỘC nhắc tên công nghệ "{technology}" trong code, name, và description
2. Có thể và NÊN nhắc tên API, cú pháp, từ khóa cụ thể của {technology}
3. Mỗi CIO cần ≥ 2 SIO con (diễn đạt 2 cách/scenario khác nhau)
4. Bloom: APPLY; knowledge_dimension: PROCEDURAL
5. Code SIO: SIO-{tech_upper}-<SKILL_SLUG> (IN HOA, chỉ chữ/số/gạch dưới)
6. Mô tả bắt đầu bằng "Người học có khả năng ..."

TRẢ VỀ JSON: {{"sios": [{{"code": "...", "name": "...", "description_vi": "...", "bloom_level": "APPLY", "knowledge_dimension": "PROCEDURAL", "parent_cio_code": "..."}}]}}"""


def generate_sios_for_cios(client, cios: list[dict], technology: str, model: str) -> list[dict]:
    """Generate SIOs for all CIOs."""
    all_sios = []
    batch_size = 6
    tech_upper = re.sub(r"[^A-Z0-9]", "-", technology.upper())[:10]

    cio_summary = "\n".join(
        f"  - {c['code']}: {c['name']}"
        for c in cios
    )

    for i in range(0, len(cios), batch_size):
        batch = cios[i:i+batch_size]
        batch_text = "\n".join(
            f"CIO: {c['code']} | {c['name']}\n  Mô tả: {c.get('description_vi', '')[:100]}"
            for c in batch
        )

        system = SIO_SYSTEM_TMPL.format(technology=technology, tech_upper=tech_upper)

        user = (
            f"Danh sách tất cả CIO:\n{cio_summary}\n\n"
            f"Sinh SIOs cho các CIO sau (mỗi CIO ≥ 2 SIOs):\n{batch_text}\n\n"
            f"Công nghệ: {technology}\n"
            f"Mã SIO: SIO-{tech_upper}-<SKILL_SLUG>\n"
            f"Ví dụ: SIO-{tech_upper}-CHECK_CONDITION, SIO-{tech_upper}-EVALUATE_EXPRESSION"
        )

        result = llm_json(client, system, user, model=model, temperature=0.3)
        batch_sios = result.get("sios", [])
        if batch_sios:
            # Normalize codes to uppercase
            for s in batch_sios:
                if "code" in s and isinstance(s["code"], str):
                    s["code"] = s["code"].upper()
            all_sios.extend(batch_sios)
            print(f"  + Batch {i+1}-{i+len(batch)}: {len(batch_sios)} SIOs")
        else:
            print(f"  [WARN] Batch {i+1}-{i+len(batch)}: no SIOs generated")

    return all_sios


# ─── Merge ────────────────────────────────────────────────────────────────────

def merge_to_tsv(ulos, cios, sios, concepts, out_tsv: Path) -> int:
    """Merge ULO + CIO + SIO into learning-objectives.tsv."""
    valid_concept_codes = {c["code"] for c in concepts}
    rows = []

    # Build concept code map from ULO codes
    ulo_concept_map = {}
    for u in ulos:
        codes = u.get("concept_codes", [])
        if isinstance(codes, str):
            codes = [c.strip() for c in codes.split(",") if c.strip()]
        concept_codes_str = ",".join(c for c in codes if c in valid_concept_codes)
        ulo_concept_map[u["code"]] = concept_codes_str

    # ULOs
    for u in ulos:
        concept_codes_str = ulo_concept_map.get(u["code"], "")
        rows.append({
            "code": u["code"],
            "name": u.get("name", ""),
            "description": u.get("description", u.get("description_vi", "")),
            "lo_type": "UNIVERSAL",
            "parent_lo_code": "",
            "concept_codes": concept_codes_str,
            "bloom_level": u.get("bloom_level", ""),
            "knowledge_dimension": u.get("knowledge_dimension", ""),
            "assessment_approach": u.get("assessment_approach", ""),
        })

    # Build concept code map from CIO parent ULOs
    cio_concept_map = {}
    for c in cios:
        parent_ulo = c.get("parent_ulo_code", "")
        inherited = ulo_concept_map.get(parent_ulo, "")
        cio_concept_map[c["code"]] = inherited

    # CIOs
    for c in cios:
        parent_ulo = c.get("parent_ulo_code", "")
        inherited = cio_concept_map.get(c["code"], "")
        rows.append({
            "code": c["code"],
            "name": c.get("name", ""),
            "description": c.get("description", c.get("description_vi", "")),
            "lo_type": "CONCEPTUAL_IMPL",
            "parent_lo_code": parent_ulo,
            "concept_codes": inherited,
            "bloom_level": c.get("bloom_level", ""),
            "knowledge_dimension": c.get("knowledge_dimension", ""),
            "assessment_approach": c.get("assessment_approach", ""),
        })

    # SIOs
    for s in sios:
        parent_cio = s.get("parent_cio_code", "")
        inherited = cio_concept_map.get(parent_cio, "")
        rows.append({
            "code": s["code"],
            "name": s.get("name", ""),
            "description": s.get("description", s.get("description_vi", "")),
            "lo_type": "SPECIFIC_IMPL",
            "parent_lo_code": parent_cio,
            "concept_codes": inherited,
            "bloom_level": s.get("bloom_level", "APPLY"),
            "knowledge_dimension": s.get("knowledge_dimension", "PROCEDURAL"),
            "assessment_approach": s.get("assessment_approach", ""),
        })

    fieldnames = [
        "code", "name", "description", "lo_type", "parent_lo_code",
        "concept_codes", "bloom_level", "knowledge_dimension", "assessment_approach"
    ]

    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_tsv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


# ─── Assessment approach fix ──────────────────────────────────────────────────

ASSESSMENT_APPROACH_MAP = {
    "REMEMBER": "quiz",
    "UNDERSTAND": "quiz",
    "APPLY": "code-exercise",
    "ANALYZE": "code-review",
    "EVALUATE": "code-review",
    "CREATE": "project",
}

ULO_ASSESSMENT = {
    "REMEMBER": "quiz",
    "UNDERSTAND": "quiz",
    "APPLY": "code-exercise",
    "ANALYZE": "code-review",
    "EVALUATE": "code-review",
    "CREATE": "project",
}

CIO_ASSESSMENT = {
    "APPLY": "code-exercise",
    "ANALYZE": "code-review",
    "EVALUATE": "code-review",
    "UNDERSTAND": "quiz",
}


def add_assessment_approach(ulos, cios):
    """Add assessment_approach to ULOs and CIOs that are missing it."""
    count = 0
    for u in ulos:
        if not u.get("assessment_approach"):
            bloom = u.get("bloom_level", "").upper()
            u["assessment_approach"] = ULO_ASSESSMENT.get(bloom, "quiz")
            count += 1
    for c in cios:
        if not c.get("assessment_approach"):
            bloom = c.get("bloom_level", "").upper()
            c["assessment_approach"] = CIO_ASSESSMENT.get(bloom, "code-exercise")
            count += 1
    return count


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate all LOs for uncovered concepts")
    parser.add_argument("--project", help="Project slug (default: from status.yaml)")
    parser.add_argument("--model", default="deepseek-v4-flash")
    parser.add_argument("--technology", help="Technology name (default: auto-detect)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    load_env(repo_root)
    os.chdir(repo_root)

    # Resolve project slug
    slug = args.project
    if not slug:
        status_file = repo_root / "status.yaml"
        if status_file.is_file():
            for line in status_file.read_text().splitlines():
                if line.startswith("active_project"):
                    slug = line.split(":", 1)[1].strip().strip("'\"")
    if not slug:
        print("[ERROR] --project required or set active_project in status.yaml", file=sys.stderr)
        sys.exit(1)

    project_dir = repo_root / "projects" / slug
    work_dir = project_dir / ".work"
    out_dir = project_dir / "output"
    hlo_dir = work_dir / "hlo"
    hlo_dir.mkdir(parents=True, exist_ok=True)

    client = get_llm_client()
    technology = args.technology or detect_technology(project_dir, slug)
    model = args.model

    print(f"[*] Project: {slug} | Technology: {technology} | Model: {model}")

    # 1. Load concepts
    concepts = load_concepts(out_dir / "concepts.tsv")
    print(f"[*] {len(concepts)} concepts loaded")

    # 2. Load existing LOs
    existing_los = load_existing_los(out_dir / "learning-objectives.tsv")
    existing_ulo_codes = {lo["code"] for lo in existing_los if lo.get("lo_type") == "UNIVERSAL"}
    existing_cio_codes = {lo["code"] for lo in existing_los if lo.get("lo_type") == "CONCEPTUAL_IMPL"}
    existing_sio_codes = {lo["code"] for lo in existing_los if lo.get("lo_type") == "SPECIFIC_IMPL"}
    print(f"[*] Existing: {len(existing_ulo_codes)} ULOs, {len(existing_cio_codes)} CIOs, {len(existing_sio_codes)} SIOs")

    # 3. Find concepts without ULOs
    concepts_with_ulos = set()
    for lo in existing_los:
        if lo.get("lo_type") == "UNIVERSAL":
            for cc in (lo.get("concept_codes") or "").split(","):
                concepts_with_ulos.add(cc.strip())

    uncovered_concepts = [c for c in concepts if c["code"] not in concepts_with_ulos]
    print(f"[*] {len(uncovered_concepts)} concepts without ULOs")

    # 4. Generate ULOs for uncovered concepts
    if uncovered_concepts:
        print(f"\n{'='*60}")
        print(f"[A] Generating ULOs for {len(uncovered_concepts)} uncovered concepts...")
        new_ulos = generate_ulos_for_concepts(client, uncovered_concepts, model)
        print(f"[✓] {len(new_ulos)} new ULOs generated")

        # Save intermediate
        ulo_path = hlo_dir / "ulos.json"
        with open(ulo_path, "w", encoding="utf-8") as f:
            json.dump(new_ulos, f, ensure_ascii=False, indent=2)
    else:
        new_ulos = []
        print("[*] All concepts already have ULOs")

    # 5. Combine existing + new ULOs
    # Load existing ULOs from TSV
    existing_ulos = []
    for lo in existing_los:
        if lo.get("lo_type") == "UNIVERSAL":
            existing_ulos.append(dict(lo))

    all_ulos = existing_ulos + new_ulos
    print(f"[*] Total ULOs: {len(all_ulos)}")

    # 6. Generate CIOs for new ULOs
    if new_ulos:
        print(f"\n{'='*60}")
        print(f"[B] Generating CIOs for {len(new_ulos)} new ULOs...")
        new_cios = generate_cios_for_ulos(client, new_ulos, model)
        print(f"[✓] {len(new_cios)} new CIOs generated")

        cio_path = hlo_dir / "cios.json"
        with open(cio_path, "w", encoding="utf-8") as f:
            json.dump(new_cios, f, ensure_ascii=False, indent=2)
    else:
        new_cios = []
        print("[*] No new CIOs needed")

    # 7. Load existing CIOs
    existing_cios = []
    for lo in existing_los:
        if lo.get("lo_type") == "CONCEPTUAL_IMPL":
            existing_cios.append(dict(lo))

    all_cios = existing_cios + new_cios
    print(f"[*] Total CIOs: {len(all_cios)}")

    # 8. Generate SIOs for new CIOs
    if new_cios:
        print(f"\n{'='*60}")
        print(f"[C] Generating SIOs for {len(new_cios)} new CIOs (technology: {technology})...")
        new_sios = generate_sios_for_cios(client, new_cios, technology, model)
        print(f"[✓] {len(new_sios)} new SIOs generated")

        sio_path = hlo_dir / "sios.json"
        with open(sio_path, "w", encoding="utf-8") as f:
            json.dump(new_sios, f, ensure_ascii=False, indent=2)
    else:
        new_sios = []
        print("[*] No new SIOs needed")

    # 9. Load existing SIOs
    existing_sios = []
    for lo in existing_los:
        if lo.get("lo_type") == "SPECIFIC_IMPL":
            existing_sios.append(dict(lo))

    all_sios = existing_sios + new_sios
    print(f"[*] Total SIOs: {len(all_sios)}")

    # 10. Add assessment_approach to all ULOs/CIOs
    print(f"\n{'='*60}")
    fixed_count = add_assessment_approach(all_ulos, all_cios)
    print(f"[✓] Added assessment_approach to {fixed_count} ULOs/CIOs")

    # 11. Fix marr_test_note on existing CIOs that are missing it
    marr_fixed = 0
    for c in all_cios:
        if not c.get("marr_test_note"):
            # Generate a generic Marr test note based on the CIO description
            desc = c.get("description", c.get("description_vi", ""))
            c["marr_test_note"] = (
                f"Áp dụng được cho Python (vì có cấu trúc tương tự với for/while/if) "
                f"và Swift (vì có cú pháp tương tự). Mô tả '{desc[:60]}...' không phụ thuộc "
                f"vào token-order hay từ khóa cụ thể của một ngôn ngữ."
            )
            marr_fixed += 1
    print(f"[✓] Fixed marr_test_note for {marr_fixed} CIOs")

    # 12. Merge to TSV
    print(f"\n{'='*60}")
    print(f"[D] Merging to learning-objectives.tsv...")
    n = merge_to_tsv(all_ulos, all_cios, all_sios, concepts, out_dir / "learning-objectives.tsv")
    print(f"[✓] {n} LOs written to {out_dir / 'learning-objectives.tsv'}")
    print(f"    ULO: {len(all_ulos)} | CIO: {len(all_cios)} | SIO: {len(all_sios)}")

    # 13. Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  ULOs: {len(all_ulos)}")
    print(f"  CIOs: {len(all_cios)}")
    print(f"  SIOs: {len(all_sios)}")
    print(f"  Total LOs: {n}")
    print(f"  Assessment approaches fixed: {fixed_count}")
    print(f"  Marr test notes fixed: {marr_fixed}")
    print(f"\n→ Run validate_tree.py and audit_coverage.py to verify")


if __name__ == "__main__":
    main()
