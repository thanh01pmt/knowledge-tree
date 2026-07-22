#!/usr/bin/env python3
"""
llm_extract_lo.py — Trích xuất Learning Objectives từ syllabus sử dụng LLM.

Model sư phạm (Abstraction Axis):
  ULO — Năng lực cốt lõi, độc lập với ngôn ngữ/công cụ cụ thể.
  CIO — Pattern/approach cụ thể hơn, nhưng vẫn language-neutral.
  SIO — Gắn với công nghệ cụ thể của PROJECT (súy từ context), trực tiếp đo lường được.
        Công nghệ cụ thể là gì (Swift, Python, SQL...) do context của project quy định.

Format description bắt buộc: "Người học có khả năng [verb] [object] [context]..."

Yêu cầu: pip install openai pydantic
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from pydantic import BaseModel, Field

try:
    from openai import OpenAI
except ImportError:
    print("Vui lòng cài đặt: pip install openai pydantic")
    sys.exit(1)


# ─── Models ──────────────────────────────────────────────────────────────────

class LearningObjective(BaseModel):
    code: str = Field(description=(
        "Mã LO duy nhất, UPPER-CASE với dấu gạch ngang. "
        "ULO: 'ULO-<CONCEPT>' (VD: ULO-DEFINITE-ITERATION). "
        "CIO: 'CIO-<PATTERN>' (VD: CIO-ITERATE-COLLECTION). "
        "SIO: 'SIO-<TECH>-<SKILL>' (VD: SIO-SWIFT-FOR-IN-ARRAY). "
        "Code phải DUY NHẤT trong toàn bộ output."
    ))
    name: str = Field(description=(
        "Tên mục tiêu bằng tiếng Anh, tối đa 8 từ, dùng verb infinitive. "
        "ULO/CIO: KHÔNG được chứa tên công nghệ (không có Swift, Python, Xcode). "
        "SIO: NÊN chứa tên công nghệ (VD: 'Write a Swift for loop with range')."
    ))
    description: str = Field(description=(
        "Mô tả năng lực bằng tiếng Việt. "
        "BẮT BUỘC bắt đầu: 'Người học có khả năng [verb] [object]...'. "
        "Câu mô tả phải hoàn chỉnh, chính xác về mặt sư phạm (1-3 câu)."
    ))
    lo_type: str = Field(description="Một trong: UNIVERSAL | CONCEPTUAL_IMPL | SPECIFIC_IMPL")
    parent_lo_code: str = Field(description=(
        "UNIVERSAL: để trống hoặc 'NULL'. "
        "CONCEPTUAL_IMPL: phải trỏ về một UNIVERSAL code trong cùng output. "
        "SPECIFIC_IMPL: phải trỏ về một CONCEPTUAL_IMPL code trong cùng output."
    ))
    concept_codes: str = Field(description=(
        "Một hoặc nhiều concept code phân cách bằng dấu phẩy. "
        "CHỈ được dùng các code trong danh sách hợp lệ được cung cấp."
    ))


class LOExtractionResponse(BaseModel):
    learning_objectives: list[LearningObjective] = Field(
        description="Danh sách đầy đủ tất cả LO được phân rã từ tài liệu."
    )


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


def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def load_valid_concepts(concepts_tsv: Path) -> list[dict]:
    """Load concepts from project's concepts.tsv for grounding."""
    if not concepts_tsv.is_file():
        return []
    concepts = []
    with open(concepts_tsv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code = (row.get("code") or "").strip()
            name = (row.get("name") or "").strip()
            desc = (row.get("description") or "").strip()
            if code:
                concepts.append({"code": code, "name": name, "description": desc})
    return concepts


def load_syllabus_text(work_dir: Path) -> str:
    """Load syllabus from raw_pdf.txt, fallback to context-audit.md."""
    raw_pdf = work_dir / "raw_pdf.txt"
    context_audit = work_dir / "context-audit.md"
    if raw_pdf.is_file():
        return raw_pdf.read_text(encoding="utf-8")
    if context_audit.is_file():
        print("[*] raw_pdf.txt không tìm thấy, dùng context-audit.md làm fallback.")
        return context_audit.read_text(encoding="utf-8")
    return ""


# Known technology fingerprints (keyword → canonical name)
_TECH_FINGERPRINTS: list[tuple[list[str], str]] = [
    (["swiftui", "swift", "xcode", ".swift", "ios", "macos", "apple"], "Swift / SwiftUI"),
    (["python", ".py", "django", "flask", "pandas", "numpy"], "Python"),
    (["kotlin", ".kt", "android", "jetpack", "compose"], "Kotlin / Jetpack Compose"),
    (["java", ".java", "spring", "maven", "gradle"], "Java"),
    (["javascript", "typescript", ".js", ".ts", "react", "vue", "angular", "node"], "JavaScript / TypeScript"),
    (["sql", "postgresql", "mysql", "sqlite", ".sql"], "SQL"),
    (["rust", ".rs", "cargo"], "Rust"),
    (["c#", "csharp", ".cs", "dotnet", "unity", "asp.net"], "C# / .NET"),
    (["c++", "cpp", ".cpp", ".h"], "C++"),
    (["flutter", "dart", ".dart"], "Flutter / Dart"),
    (["html", "css", ".html", ".css"], "HTML / CSS"),
]


def extract_technology_from_context(project_dir: Path, slug: str, status: dict) -> str:
    """
    Súy luận tên công nghệ cụ thể của project từ nhiều nguồn:
      1. status.yaml (key 'technology')
      2. Tên file/thư mục trong context/
      3. context-audit.md (keyword scan đầu file)
      4. raw_pdf.txt (keyword scan đầu file)
      5. Project slug (fallback cuối)
    """
    # Guầu 1: status.yaml có key 'technology' được set thủ công
    if status.get("technology"):
        return status["technology"].strip()

    scores: dict[str, float] = {}

    def _add_score(text: str, weight: float = 1.0):
        text_lower = text.lower()
        for keywords, tech_name in _TECH_FINGERPRINTS:
            for kw in keywords:
                if kw in text_lower:
                    scores[tech_name] = scores.get(tech_name, 0) + weight
                    break  # chỉ tính 1 lần mỗi fingerprint group

    # Guầu 2: Tên file trong context/
    context_dir = project_dir / "context"
    if context_dir.is_dir():
        for f in context_dir.iterdir():
            _add_score(f.name, weight=3.0)

    # Guầu 3: context-audit.md (đầu 80 dòng — gỳn nhưng có tech keywords cao)
    context_audit = project_dir / ".work" / "context-audit.md"
    if context_audit.is_file():
        head = "\n".join(context_audit.read_text(encoding="utf-8").splitlines()[:80])
        _add_score(head, weight=2.0)

    # Guầu 4: raw_pdf.txt (đầu 100 dòng)
    raw_pdf = project_dir / ".work" / "raw_pdf.txt"
    if raw_pdf.is_file():
        head = "\n".join(raw_pdf.read_text(encoding="utf-8").splitlines()[:100])
        _add_score(head, weight=1.5)

    # Guầu 5: Project slug
    _add_score(slug, weight=1.0)

    if scores:
        best_tech = max(scores, key=lambda t: scores[t])
        print(f"[*] Detected technology: '{best_tech}' (scores: {dict(sorted(scores.items(), key=lambda x: -x[1])[:3])})")
        return best_tech

    # Họp fallback nếu không detect được
    print(f"[!] Không thể detect technology từ context. Dùng --technology để chỉ định thủ công.")
    return slug


def validate_concept_codes(los: list[LearningObjective], valid_codes: set[str]) -> list[str]:
    """Validate all concept_codes in generated LOs. Return list of error messages."""
    errors = []
    if not valid_codes:
        return errors
    for lo in los:
        codes = [c.strip() for c in lo.concept_codes.replace(";", ",").split(",") if c.strip()]
        for c in codes:
            if c not in valid_codes:
                errors.append(
                    f"  • [{lo.lo_type}] {lo.code}: concept_code '{c}' không tồn tại trong project concepts.tsv"
                )
    return errors


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Trích xuất Learning Objectives từ syllabus sử dụng LLM. "
            "Model sư phạm: ULO (language-agnostic) → CIO (pattern, neutral) → SIO (technology-specific)."
        )
    )
    parser.add_argument(
        "--project", type=str,
        help="Project slug (nếu bỏ qua, đọc active_project từ status.yaml)"
    )
    parser.add_argument(
        "--technology", type=str, default=None,
        help="Override: tên công nghệ cụ thể cho SIO (VD: 'Swift', 'Python'). "
             "Nếu bỏ qua, tự động súy từ context của project."
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)

    # Resolve project slug
    slug = args.project
    status = load_status(repo_root)
    if not slug:
        slug = status.get("active_project")
        if not slug:
            print("❌ Error: Không tìm thấy project. Truyền --project <slug> hoặc set active_project trong status.yaml.")
            sys.exit(1)

    project_dir = repo_root / "projects" / slug
    work_dir = project_dir / ".work"
    out_dir = project_dir / "output"
    output_tsv = out_dir / "learning-objectives.tsv"
    concepts_tsv = out_dir / "concepts.tsv"

    # Detect technology from context (or use --technology override)
    technology = args.technology
    if not technology:
        technology = extract_technology_from_context(project_dir, slug, status)

    # Load valid concepts for grounding
    valid_concepts = load_valid_concepts(concepts_tsv)
    valid_codes = {c["code"] for c in valid_concepts}
    if not valid_concepts:
        print(f"⚠️  Warning: concepts.tsv không tìm thấy tại {concepts_tsv}.")
        print("   Hãy chạy /build-tree trước. LLM sẽ không được grounding.")
    else:
        print(f"[*] Loaded {len(valid_concepts)} valid concept codes.")

    # Load syllabus
    text_content = load_syllabus_text(work_dir)
    if not text_content.strip():
        print(f"❌ Error: Không tìm thấy syllabus text trong {work_dir}")
        sys.exit(1)
    print(f"[*] Đọc syllabus ({len(text_content)} ký tự).")

    # Setup LLM client
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: Set biến môi trường OPENAI_API_KEY hoặc GEMINI_API_KEY.")
        sys.exit(1)
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    client = OpenAI(api_key=api_key, base_url=base_url)

    # Build grounded concept list for prompt
    if valid_concepts:
        concept_list_str = "\n".join(
            f"  - {c['code']}: {c['name']} — {c['description'][:80]}"
            for c in valid_concepts
        )
        grounding_block = f"""
DANH SÁCH CONCEPT CODES HỢP LỆ (chỉ được dùng các mã dưới đây, không được tự bịa):
{concept_list_str}
"""
    else:
        grounding_block = (
            "Lưu ý: Không có danh sách concept_codes cố định. "
            "Dùng mã UPPER_SNAKE_CASE mô tả đúng khái niệm."
        )

    system_prompt = f"""Bạn là một Chuyên gia Thiết kế Chương trình học (Curriculum Designer) chuyên xây dựng hệ thống Learning Objectives phân tầng.

Nhiệm vụ: Đọc tài liệu Syllabus và phân rã TẤT CẢ các mục thành hệ thống LO 3 tầng theo trục trừu tượng hóa (Abstraction Axis).

════════════════════════════════════════════
KIẾN TRÚC 3 TẦNG (ABSTRACTION AXIS)
════════════════════════════════════════════

Tầng 1 — UNIVERSAL (ULO):
  • Mô tả năng lực CỐT LÕI, trừu tượng, KHÔNG phụ thuộc ngôn ngữ hay công cụ.
  • Trả lời: "Về bản chất, người học cần hiểu/làm được GÌ với khái niệm này?"
  • Tên: KHÔNG chứa tên công nghệ ({technology}).
  • parent_lo_code = "" (rỗng).
  • Mỗi ULO là gốc của một cụm LO liên quan.

Tầng 2 — CONCEPTUAL_IMPL (CIO):
  • Mô tả một PATTERN hoặc APPROACH cụ thể để hiện thực ULO.
  • Vẫn language-neutral — KHÔNG nhắc tên công nghệ cụ thể ({technology}) trong name.
  • Trả lời: "Theo pattern/cách tiếp cận nào người học có thể đạt ULO này?"
  • Tên: Verb + Object (VD: "Iterate Over a Collection", "Define a Named Function").
  • parent_lo_code → trỏ về ULO tương ứng.
  • Mỗi CIO phải có ÍT NHẤT 2 SIO con.

Tầng 3 — SPECIFIC_IMPL (SIO):
  • Mô tả kỹ năng CỤ THỂ, gắn với công nghệ {technology}, đo lường được trực tiếp.
  • PHẢI nhắc tên công nghệ {technology} trong name và/hoặc description.
  • Gắn với syntax, API, hoặc công cụ cụ thể của {technology}.
  • parent_lo_code → trỏ về CIO tương ứng.

════════════════════════════════════════════
FORMAT BẮT BUỘC
════════════════════════════════════════════

Description: "Người học có khả năng [verb] [object] [context]..." (tiếng Việt, 1-3 câu)
Code ULO: "ULO-<CONCEPT>" (VD: ULO-DEFINITE-ITERATION)
Code CIO: "CIO-<PATTERN>" (VD: CIO-ITERATE-COLLECTION)
Code SIO: "SIO-{technology.upper()}-<SKILL>" (VD: SIO-SWIFT-FOR-IN-ARRAY)

════════════════════════════════════════════
VÍ DỤ THAM KHẢO (Concept: FOR_LOOP)
════════════════════════════════════════════

ULO-DEFINITE-ITERATION | Understand Definite Iteration | UNIVERSAL | "" | FOR_LOOP
→ "Người học có khả năng giải thích và áp dụng khái niệm lặp lại một khối hành động
   một số lần xác định trước để giải quyết các bài toán có cấu trúc lặp lại."

CIO-ITERATE-COLLECTION | Traverse Elements of a Collection | CONCEPTUAL_IMPL | ULO-DEFINITE-ITERATION | FOR_LOOP
→ "Người học có khả năng sử dụng vòng lặp xác định để truy cập tuần tự từng phần tử
   trong một cấu trúc dữ liệu tập hợp."

SIO-SWIFT-FOR-IN-ARRAY | Traverse a {technology} Array using for-in | SPECIFIC_IMPL | CIO-ITERATE-COLLECTION | FOR_LOOP
→ "Người học có khả năng viết vòng lặp for item in myArray trong {technology} để
   duyệt qua từng phần tử và thực hiện một thao tác trên mỗi phần tử."

SIO-SWIFT-FOR-IN-RANGE | Use a {technology} for-in loop with a numeric range | SPECIFIC_IMPL | CIO-ITERATE-COLLECTION | FOR_LOOP
→ "Người học có khả năng sử dụng for i in 1...10 và 1..<10 trong {technology} để
   lặp qua một dãy số với bước nhảy mặc định."

════════════════════════════════════════════
QUY TẮC ĐỘ PHỦ
════════════════════════════════════════════

• Phân rã ĐẦY ĐỦ tất cả mục trong syllabus, không bỏ sót.
• Mỗi bullet/mục sinh ít nhất: 1 ULO + 1 CIO + 2 SIO.
• Mỗi CIO phải có ÍT NHẤT 2 SIO con.
• Code phải DUY NHẤT trong toàn bộ output.
• parent_lo_code phải trỏ đến code ĐANG TỒN TẠI trong output (không bịa code).
• UNIVERSAL luôn có parent_lo_code rỗng.

{grounding_block}
"""

    print(f"[*] Đang gửi dữ liệu lên LLM (technology: {technology})...")
    model = os.getenv("LO_EXTRACT_MODEL", "gpt-4o-2024-08-06")
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Tài liệu Syllabus ({technology}):\n{text_content}"}
        ],
        response_format=LOExtractionResponse,
    )

    result = completion.choices[0].message.parsed
    los = result.learning_objectives
    print(f"[*] LLM trích xuất {len(los)} Learning Objectives.")

    # Post-processing: validate concept_codes
    errors = validate_concept_codes(los, valid_codes)
    if errors:
        print(f"\n⚠️  {len(errors)} LO có concept_codes không hợp lệ:")
        for e in errors:
            print(e)
        print("\n[!] Các LO lỗi vẫn được ghi vào TSV nhưng sẽ bị báo ERROR khi /validate-tree.\n")
    else:
        print("[✓] Tất cả concept_codes hợp lệ.")

    # Sort: UNIVERSAL → CONCEPTUAL_IMPL → SPECIFIC_IMPL
    type_priority = {"UNIVERSAL": 0, "CONCEPTUAL_IMPL": 1, "SPECIFIC_IMPL": 2}
    los.sort(key=lambda x: type_priority.get(x.lo_type, 99))

    # Write TSV
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(output_tsv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"])
        for lo in los:
            parent = lo.parent_lo_code.strip()
            if lo.lo_type == "UNIVERSAL":
                parent = ""
            writer.writerow([lo.code, lo.name, lo.description, lo.lo_type, parent, lo.concept_codes])

    print(f"[✓] Đã ghi {len(los)} LO vào {output_tsv.relative_to(repo_root)}")
    print("[→] Tiếp theo: chạy /validate-tree để kiểm tra referential integrity.")


if __name__ == "__main__":
    main()
