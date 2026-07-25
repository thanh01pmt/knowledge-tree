#!/usr/bin/env python3
"""
llm_generate_hierarchical_lo.py — Sinh Learning Objectives theo 3 phase phân cấp.

Thay vì sinh toàn bộ ULO+CIO+SIO trong 1 lượt (black box), script này cho phép:
  Phase A: /generate-ulos  — Sinh ULOs từ concepts, ưu tiên Bloom Evaluate/Create
  Phase B: /generate-cios  — Sinh CIOs từ ULOs đã duyệt, enforce Marr 2-Language Test
  Phase C: /generate-sios  — Sinh SIOs từ CIOs đã duyệt, gắn với technology cụ thể

Mỗi phase ghi file JSON trung gian để người dùng xem/duyệt trước khi phase tiếp theo.
Phase C merge toàn bộ vào learning-objectives.tsv.

Cách dùng:
  python3 llm_generate_hierarchical_lo.py --phase ulos --project <slug>
  python3 llm_generate_hierarchical_lo.py --phase cios --project <slug>
  python3 llm_generate_hierarchical_lo.py --phase sios --project <slug>
  python3 llm_generate_hierarchical_lo.py --phase merge --project <slug>  # merge → TSV

Hoặc dùng workflow commands: /generate-ulos, /generate-cios, /generate-sios
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] Cài đặt: pip install openai pydantic", file=sys.stderr)
    sys.exit(1)


# ─── Pydantic Models ──────────────────────────────────────────────────────────

class ULO(BaseModel):
    code: str = Field(description=(
        "Mã ULO: 'ULO-<CONCEPT-SLUG>' dạng UPPER-KEBAB-CASE. "
        "VD: ULO-DEFINITE-ITERATION. KHÔNG chứa tên công nghệ."
    ))
    name: str = Field(description=(
        "Tên năng lực cốt lõi, tiếng Anh, tối đa 8 từ, verb infinitive. "
        "KHÔNG chứa tên công nghệ hay ngôn ngữ lập trình."
    ))
    description_vi: str = Field(description=(
        "Mô tả bằng tiếng Việt, bắt đầu 'Người học có khả năng...'. "
        "Mô tả năng lực UNIVERSAL — áp dụng được bất kể công nghệ."
    ))
    bloom_level: str = Field(description=(
        "Cấp độ Bloom: REMEMBER | UNDERSTAND | APPLY | ANALYZE | EVALUATE | CREATE. "
        "Ưu tiên EVALUATE hoặc CREATE khi nội dung cho phép."
    ))
    knowledge_dimension: str = Field(description=(
        "FACTUAL | CONCEPTUAL | PROCEDURAL | METACOGNITIVE"
    ))
    concept_codes: list[str] = Field(description=(
        "Danh sách concept codes hợp lệ từ concepts.tsv của project. "
        "CHỈ dùng codes đã được cung cấp, không tự bịa."
    ))


class ULOBatch(BaseModel):
    ulos: list[ULO]


class CIO(BaseModel):
    code: str = Field(description=(
        "Mã CIO: 'CIO-<PATTERN-SLUG>' dạng UPPER-KEBAB-CASE. "
        "VD: CIO-ITERATE-COLLECTION. KHÔNG chứa tên công nghệ."
    ))
    name: str = Field(description=(
        "Tên pattern/approach, tiếng Anh. Verb + Object. "
        "KHÔNG chứa tên công nghệ hay cú pháp ngôn ngữ cụ thể."
    ))
    description_vi: str = Field(description=(
        "Mô tả bằng tiếng Việt, bắt đầu 'Người học có khả năng...'. "
        "Mô tả PATTERN TRUNG TÍNH — không nhắc tên ngôn ngữ/framework."
    ))
    parent_ulo_code: str = Field(description="Code ULO cha (phải là ULO code tồn tại trong input)")
    marr_test_note: str = Field(description=(
        "Ghi chú kiểm tra Marr: 'Áp dụng được cho [ngôn ngữ A] vì [...] và [ngôn ngữ B] vì [...]'. "
        "BẮT BUỘC map thử sang ≥ 2 ngôn ngữ/công cụ TRƯỚC khi ghi CIO này."
    ))
    bloom_level: str = Field(description="APPLY | ANALYZE | EVALUATE — CIO thường ở Apply/Analyze")
    knowledge_dimension: str = Field(description="CONCEPTUAL | PROCEDURAL | METACOGNITIVE")


class CIOBatch(BaseModel):
    cios: list[CIO]


class SIO(BaseModel):
    code: str = Field(description=(
        "Mã SIO: 'SIO-<TECH>-<SKILL-SLUG>' dạng UPPER-KEBAB-CASE. "
        "VD: SIO-SWIFT-FOR-IN-ARRAY. PHẢI chứa tên công nghệ."
    ))
    name: str = Field(description=(
        "Tên kỹ năng cụ thể, tiếng Anh. PHẢI nhắc tên công nghệ. "
        "VD: 'Traverse a Swift Array using for-in'"
    ))
    description_vi: str = Field(description=(
        "Mô tả bằng tiếng Việt, bắt đầu 'Người học có khả năng...'. "
        "PHẢI nhắc tên công nghệ và có thể nhắc cú pháp/API cụ thể."
    ))
    parent_cio_code: str = Field(description="Code CIO cha (phải là CIO code tồn tại trong input)")
    bloom_level: str = Field(description="APPLY | CREATE — SIO thường ở Apply")
    knowledge_dimension: str = Field(description="PROCEDURAL")


class SIOBatch(BaseModel):
    sios: list[SIO]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def get_project_dirs(repo_root: Path, slug: str):
    project_dir = repo_root / "projects" / slug
    work_dir = project_dir / ".work"
    out_dir = project_dir / "output"
    hlo_dir = work_dir / "hlo"  # hierarchical LO workspace
    hlo_dir.mkdir(parents=True, exist_ok=True)
    return project_dir, work_dir, out_dir, hlo_dir


def load_concepts(concepts_tsv: Path) -> list[dict]:
    if not concepts_tsv.is_file():
        return []
    concepts = []
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


def load_syllabus(work_dir: Path) -> str:
    for fname in ["raw_pdf.txt", "context-audit.md"]:
        f = work_dir / fname
        if f.is_file():
            return f.read_text(encoding="utf-8")
    return ""


def detect_technology(project_dir: Path, slug: str) -> str:
    _TECH_FINGERPRINTS = [
        (["swift", "swiftui", "xcode", "ios", "macos"], "Swift"),
        (["python", ".py", "django", "flask"], "Python"),
        (["javascript", "typescript", ".js", ".ts", "react", "vue", "angular", "node"], "JavaScript / TypeScript"),
        (["kotlin", "android", "jetpack"], "Kotlin"),
        (["java", "spring", "maven"], "Java"),
        (["rust", ".rs", "cargo"], "Rust"),
        (["arduino", "esp32", "c++", "cpp"], "C++ / Arduino"),
        (["flutter", "dart"], "Flutter / Dart"),
        (["angular"], "Angular"),
        (["react", "reactjs"], "React"),
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


# ─── Phase A: Generate ULOs ───────────────────────────────────────────────────

ULO_SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Universal Learning Objectives (ULO).

ULO = Tầng Computational (Marr): mô tả NĂNG LỰC CỐT LÕI — WHAT và WHY — hoàn toàn độc lập với bất kỳ công nghệ/ngôn ngữ nào.

Nguyên tắc:
1. ULO KHÔNG chứa tên công nghệ, ngôn ngữ lập trình, framework, hay cú pháp
2. ULO phải áp dụng được cho người học bất kể họ dùng Python, Swift, JavaScript hay ngôn ngữ nào
3. Ưu tiên động từ Bloom CẤP CAO: Evaluate / Create / Analyze — tránh "lực hút" về Remember/Understand
4. 1 concept → 1-3 ULO (tùy độ phức tạp). Không sinh quá nhiều ULO trivial
5. Mỗi ULO là gốc của cây LO; CIO và SIO sẽ được sinh SAU từ mỗi ULO"""


def generate_ulos(
    client: OpenAI,
    concepts: list[dict],
    syllabus: str,
    model: str,
    work_dir: Path,
    hlo_dir: Path,
) -> list[dict]:
    concept_list = "\n".join(
        f"  - {c['code']}: {c['name']} — {c['description'][:80]}"
        for c in concepts
    )
    user_prompt = (
        f"Project concepts (valid codes — CHỈ dùng các mã này cho concept_codes):\n{concept_list}\n\n"
        f"Syllabus / Context:\n{syllabus[:6000]}\n\n"
        "Sinh danh sách ULO đầy đủ cho project này. Ưu tiên Bloom Evaluate/Create."
    )

    print("[A] Generating ULOs ...")
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": ULO_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        response_format=ULOBatch,
        temperature=0.3,
    )
    result = completion.choices[0].message.parsed
    ulos = [u.model_dump() for u in result.ulos] if result else []

    # Validate concept codes
    valid_codes = {c["code"] for c in concepts}
    for u in ulos:
        u["concept_codes"] = [c for c in u["concept_codes"] if c in valid_codes]

    out_path = hlo_dir / "ulos.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ulos, f, ensure_ascii=False, indent=2)

    # Preview markdown
    _write_ulo_preview(hlo_dir / "ulos_preview.md", ulos)

    print(f"[✓] {len(ulos)} ULOs → {out_path}")
    print(f"[✓] Preview → {hlo_dir / 'ulos_preview.md'}")
    print(f"\n→ Xem ulos_preview.md, duyệt, rồi chạy /generate-cios")
    return ulos


def _write_ulo_preview(path: Path, ulos: list[dict]) -> None:
    lines = [
        "# ULO Preview",
        f"\n_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {len(ulos)} ULOs_\n",
        "| Code | Name | Bloom | Dimension | Concepts |",
        "|------|------|-------|-----------|---------|",
    ]
    for u in ulos:
        codes = ", ".join(u.get("concept_codes", []))
        lines.append(
            f"| `{u['code']}` | {u['name']} | {u['bloom_level']} | "
            f"{u['knowledge_dimension']} | {codes} |"
        )
    lines += ["", "## Descriptions", ""]
    for u in ulos:
        lines.append(f"### `{u['code']}` — {u['name']}")
        lines.append(f"> {u['description_vi']}\n")
    path.write_text("\n".join(lines), encoding="utf-8")


# ─── Phase B: Generate CIOs ───────────────────────────────────────────────────

CIO_SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Conceptual Implementation Objectives (CIO).

CIO = Tầng Algorithmic (Marr): mô tả PATTERN / APPROACH trung tính — HOW ở mức thủ tục, KHÔNG gắn cú pháp.

PHÉP THỬ MARR 2-NGÔN-NGỮ (BẮT BUỘC trước khi ghi CIO):
Trước khi viết mỗi CIO, thử ánh xạ mô tả sang ít nhất 2 ngôn ngữ khác nhau.
- Nếu mô tả khớp tự nhiên với CẢ 2 → CIO hợp lệ
- Nếu chỉ khớp với 1 ngôn ngữ (token-order, cú pháp riêng) → đó là SIO trá hình → viết lại
Ghi kết quả test vào trường `marr_test_note`.

Nguyên tắc:
1. CIO KHÔNG chứa tên công nghệ, không có từ khóa cú pháp (let, var, def, func, class, import...)
2. Mỗi ULO cần 1-3 CIO diễn đạt các pattern/approach khác nhau để đạt ULO đó
3. Mỗi CIO sẽ có ≥ 2 SIO con (được sinh ở bước sau)
4. Bloom ở CIO thường là APPLY / ANALYZE"""


def generate_cios(
    client: OpenAI,
    ulos: list[dict],
    model: str,
    hlo_dir: Path,
    batch_size: int = 10,
) -> list[dict]:
    all_cios = []

    ulo_summary = "\n".join(
        f"  - {u['code']}: {u['name']} — {u.get('description_vi', '')[:80]}"
        for u in ulos
    )

    print(f"[B] Generating CIOs for {len(ulos)} ULOs (batch_size={batch_size}) ...")

    for i in range(0, len(ulos), batch_size):
        batch = ulos[i : i + batch_size]
        batch_text = "\n".join(
            f"ULO: {u['code']} | {u['name']}\n  Mô tả: {u.get('description_vi', '')}"
            for u in batch
        )

        user_prompt = (
            f"Danh sách tất cả ULO trong project (để tham chiếu parent codes):\n{ulo_summary}\n\n"
            f"Sinh CIOs cho các ULO sau:\n{batch_text}\n\n"
            "Với mỗi ULO, sinh 1-3 CIO. BẮT BUỘC thực hiện Marr 2-Language Test cho mỗi CIO."
        )

        try:
            completion = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": CIO_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=CIOBatch,
                temperature=0.2,
            )
            result = completion.choices[0].message.parsed
            if result:
                batch_cios = [c.model_dump() for c in result.cios]
                # Validate parent codes
                valid_ulo_codes = {u["code"] for u in ulos}
                for c in batch_cios:
                    if c["parent_ulo_code"] not in valid_ulo_codes:
                        c["parent_ulo_code"] = batch[0]["code"]  # fallback
                all_cios.extend(batch_cios)
                print(f"  Batch {i+1}-{min(i+batch_size, len(ulos))}: +{len(batch_cios)} CIOs")
        except Exception as e:
            print(f"  [WARN] Batch {i}: {e}", file=sys.stderr)

    out_path = hlo_dir / "cios.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_cios, f, ensure_ascii=False, indent=2)

    _write_cio_preview(hlo_dir / "cios_preview.md", all_cios, ulos)

    print(f"[✓] {len(all_cios)} CIOs → {out_path}")
    print(f"[✓] Preview → {hlo_dir / 'cios_preview.md'}")
    print(f"\n→ Xem cios_preview.md (kiểm tra marr_test_note), rồi chạy /generate-sios")
    return all_cios


def _write_cio_preview(path: Path, cios: list[dict], ulos: list[dict]) -> None:
    ulo_map = {u["code"]: u["name"] for u in ulos}
    lines = [
        "# CIO Preview — Marr Test Results",
        f"\n_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {len(cios)} CIOs_\n",
        "> Kiểm tra cột **Marr Test** — nếu trống hoặc chỉ nhắc 1 ngôn ngữ → CIO cần viết lại\n",
        "| Code | Name | Parent ULO | Bloom | Marr Test Note |",
        "|------|------|-----------|-------|----------------|",
    ]
    for c in cios:
        ulo_name = ulo_map.get(c["parent_ulo_code"], "?")
        marr = c.get("marr_test_note", "")[:80]
        lines.append(
            f"| `{c['code']}` | {c['name']} | `{c['parent_ulo_code']}` ({ulo_name}) | "
            f"{c['bloom_level']} | {marr} |"
        )
    lines += ["", "## Descriptions & Marr Tests", ""]
    for c in cios:
        lines.append(f"### `{c['code']}` ← `{c['parent_ulo_code']}`")
        lines.append(f"**{c['name']}**")
        lines.append(f"> {c.get('description_vi', '')}")
        lines.append(f"\n**Marr Test:** {c.get('marr_test_note', '_(chưa ghi)_')}\n")
    path.write_text("\n".join(lines), encoding="utf-8")


# ─── Phase C: Generate SIOs ───────────────────────────────────────────────────

SIO_SYSTEM_TMPL = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Specific Implementation Objectives (SIO).

SIO = Tầng Implementational (Marr): mô tả kỹ năng CỤ THỂ gắn với công nghệ {technology}.

Nguyên tắc:
1. SIO BẮT BUỘC nhắc tên công nghệ "{technology}" trong code, name, và description
2. Có thể và NÊN nhắc tên API, cú pháp, từ khóa cụ thể của {technology}
3. Mỗi CIO cần ≥ 2 SIO con (diễn đạt 2 cách/scenario khác nhau)
4. Bloom ở SIO thường là APPLY; knowledge_dimension = PROCEDURAL
5. Code SIO format: SIO-{tech_upper}-<SKILL-SLUG>"""


def generate_sios(
    client: OpenAI,
    cios: list[dict],
    technology: str,
    model: str,
    hlo_dir: Path,
    batch_size: int = 8,
) -> list[dict]:
    all_sios = []
    tech_upper = re.sub(r"[^A-Z0-9]", "-", technology.upper())[:10]

    cio_summary = "\n".join(
        f"  - {c['code']}: {c['name']}"
        for c in cios
    )

    print(f"[C] Generating SIOs for {len(cios)} CIOs (technology: {technology}) ...")

    for i in range(0, len(cios), batch_size):
        batch = cios[i : i + batch_size]
        batch_text = "\n".join(
            f"CIO: {c['code']} | {c['name']}\n  Mô tả: {c.get('description_vi', '')[:100]}"
            for c in batch
        )

        system = SIO_SYSTEM_TMPL.format(technology=technology, tech_upper=tech_upper)
        user_prompt = (
            f"Danh sách tất cả CIO trong project (để tham chiếu parent codes):\n{cio_summary}\n\n"
            f"Sinh SIOs cho các CIO sau (mỗi CIO ≥ 2 SIOs):\n{batch_text}"
        )

        try:
            completion = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=SIOBatch,
                temperature=0.3,
            )
            result = completion.choices[0].message.parsed
            if result:
                batch_sios = [s.model_dump() for s in result.sios]
                valid_cio_codes = {c["code"] for c in cios}
                for s in batch_sios:
                    if s["parent_cio_code"] not in valid_cio_codes:
                        s["parent_cio_code"] = batch[0]["code"]
                all_sios.extend(batch_sios)
                print(f"  Batch {i+1}-{min(i+batch_size, len(cios))}: +{len(batch_sios)} SIOs")
        except Exception as e:
            print(f"  [WARN] Batch {i}: {e}", file=sys.stderr)

    out_path = hlo_dir / "sios.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_sios, f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(all_sios)} SIOs → {out_path}")
    print(f"\n→ Chạy /generate-sios --merge để ghi learning-objectives.tsv")
    return all_sios


# ─── Phase D: Merge → TSV ────────────────────────────────────────────────────

def merge_to_tsv(
    ulos: list[dict],
    cios: list[dict],
    sios: list[dict],
    concepts: list[dict],
    out_tsv: Path,
) -> int:
    """Merge ULO + CIO + SIO vào learning-objectives.tsv."""
    valid_concept_codes = {c["code"] for c in concepts}
    rows = []

    # ULOs
    for u in ulos:
        concept_codes_str = ",".join(
            c for c in u.get("concept_codes", []) if c in valid_concept_codes
        )
        rows.append({
            "code": u["code"],
            "name": u["name"],
            "description": u.get("description_vi", ""),
            "lo_type": "UNIVERSAL",
            "parent_lo_code": "",
            "concept_codes": concept_codes_str,
            "bloom_level": u.get("bloom_level", ""),
            "knowledge_dimension": u.get("knowledge_dimension", ""),
        })

    # CIOs
    for c in cios:
        rows.append({
            "code": c["code"],
            "name": c["name"],
            "description": c.get("description_vi", ""),
            "lo_type": "CONCEPTUAL_IMPL",
            "parent_lo_code": c.get("parent_ulo_code", ""),
            "concept_codes": "",
            "bloom_level": c.get("bloom_level", ""),
            "knowledge_dimension": c.get("knowledge_dimension", ""),
        })

    # SIOs
    for s in sios:
        rows.append({
            "code": s["code"],
            "name": s["name"],
            "description": s.get("description_vi", ""),
            "lo_type": "SPECIFIC_IMPL",
            "parent_lo_code": s.get("parent_cio_code", ""),
            "concept_codes": "",
            "bloom_level": s.get("bloom_level", ""),
            "knowledge_dimension": s.get("knowledge_dimension", ""),
        })

    fieldnames = ["code", "name", "description", "lo_type", "parent_lo_code",
                  "concept_codes", "bloom_level", "knowledge_dimension"]

    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_tsv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Hierarchical LO generation: ULO → CIO → SIO")
    parser.add_argument("--phase", choices=["ulos", "cios", "sios", "merge", "all"],
                        required=True, help="Phase to run")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--technology", help="Override technology detection")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)

    # Resolve project
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

    project_dir, work_dir, out_dir, hlo_dir = get_project_dirs(repo_root, slug)

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY không tìm thấy.", file=sys.stderr)
        sys.exit(1)
    client = OpenAI(api_key=api_key)

    concepts = load_concepts(out_dir / "concepts.tsv")
    if not concepts and args.phase != "merge":
        print(f"[WARN] concepts.tsv không tìm thấy. Chạy /build-tree trước.", file=sys.stderr)

    technology = args.technology or detect_technology(project_dir, slug)
    print(f"[*] Project: {slug} | Technology: {technology} | Phase: {args.phase}")

    if args.phase in ("ulos", "all"):
        syllabus = load_syllabus(work_dir)
        generate_ulos(client, concepts, syllabus, model=args.model,
                      work_dir=work_dir, hlo_dir=hlo_dir)
        if args.phase != "all":
            return

    if args.phase in ("cios", "all"):
        ulo_path = hlo_dir / "ulos.json"
        if not ulo_path.is_file():
            print("[ERROR] ulos.json không tìm thấy. Chạy --phase ulos trước.", file=sys.stderr)
            sys.exit(1)
        with open(ulo_path, encoding="utf-8") as f:
            ulos = json.load(f)
        generate_cios(client, ulos, model=args.model, hlo_dir=hlo_dir,
                      batch_size=args.batch_size)
        if args.phase != "all":
            return

    if args.phase in ("sios", "all"):
        cio_path = hlo_dir / "cios.json"
        if not cio_path.is_file():
            print("[ERROR] cios.json không tìm thấy. Chạy --phase cios trước.", file=sys.stderr)
            sys.exit(1)
        with open(cio_path, encoding="utf-8") as f:
            cios = json.load(f)
        generate_sios(client, cios, technology=technology, model=args.model,
                      hlo_dir=hlo_dir, batch_size=args.batch_size)
        if args.phase != "all":
            return

    if args.phase in ("merge", "all"):
        for fname, label in [("ulos.json", "ULOs"), ("cios.json", "CIOs"), ("sios.json", "SIOs")]:
            if not (hlo_dir / fname).is_file():
                print(f"[ERROR] {fname} không tìm thấy. Chạy các phase trước.", file=sys.stderr)
                sys.exit(1)

        with open(hlo_dir / "ulos.json", encoding="utf-8") as f:
            ulos = json.load(f)
        with open(hlo_dir / "cios.json", encoding="utf-8") as f:
            cios = json.load(f)
        with open(hlo_dir / "sios.json", encoding="utf-8") as f:
            sios = json.load(f)

        n = merge_to_tsv(ulos, cios, sios, concepts, out_dir / "learning-objectives.tsv")
        print(f"[✓] {n} LOs → {out_dir / 'learning-objectives.tsv'}")
        print(f"    ULO: {len(ulos)} | CIO: {len(cios)} | SIO: {len(sios)}")
        print(f"\n→ Chạy /validate-tree và /audit-coverage")


if __name__ == "__main__":
    main()
