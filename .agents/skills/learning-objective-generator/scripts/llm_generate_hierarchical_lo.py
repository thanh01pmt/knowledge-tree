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

# ─── Shared LLM error handling ────────────────────────────────────────────────
# Import from keyword-extractor skill (sibling directory)
_SKILL_SCRIPTS = Path(__file__).resolve().parents[1].parent / "keyword-extractor" / "scripts"
if str(_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILL_SCRIPTS))
try:
    from llm_call import llm_chat_json as _llm_chat_json, LLMCallError as _LLMCallError
    _HAS_LLM_CALL = True
except ImportError:
    _HAS_LLM_CALL = False

# Global tracker for LLM failures across all phases — written to audit trail
_LLM_FAILURES: list[dict] = []


def _safe_llm_json(client, model, system, user, temperature=0.2, batch_label=""):
    """Call LLM with retry. On failure, track in _LLM_FAILURES and return {}.
    Caller must check _LLM_FAILURES before writing final output."""
    if _HAS_LLM_CALL:
        try:
            return _llm_chat_json(client, model, system, user, temperature=temperature)
        except _LLMCallError as e:
            _LLM_FAILURES.append({
                "batch": batch_label,
                "error": str(e),
                "error_type": e.error_type,
            })
            print(f"  [FAIL] {batch_label}: {e}", file=sys.stderr)
            return {}
    else:
        # Fallback: direct call without retry (legacy behavior)
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
            _LLM_FAILURES.append({"batch": batch_label, "error": str(e), "error_type": "unknown"})
            print(f"  [FAIL] {batch_label}: {e}", file=sys.stderr)
            return {}

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


def load_classified_phrases(out_dir: Path) -> list[dict]:
    f = out_dir / "classified_action_phrases.json"
    if f.is_file():
        with open(f, encoding="utf-8") as file:
            return json.load(file)
    return []


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


def load_assessment_matrix(repo_root: Path) -> str:
    matrix_path = repo_root / ".agents" / "skills" / "learning-objective-generator" / "resources" / "approaches.tsv"
    if not matrix_path.is_file():
        return ""
    
    lines = ["## ASSESSMENT MATRIX (PRAGMATIC APPROACHES)"]
    lines.append("Bạn có thể tham khảo bảng approach dưới đây để chọn động từ (Verb) và cách viết `description_vi` (dựa trên `example_vi`) cho phù hợp nhất với Cognitive Level và Knowledge Dimension.")
    lines.append("LƯU Ý: KHÔNG CẦN TRẢ VỀ CỘT APPROACH CODE TRONG KẾT QUẢ JSON. CHỈ DÙNG ĐỂ ĐỊNH HƯỚNG VĂN PHONG.")
    lines.append("GIẢI THÍCH ĐỘ KHÓ (difficulty):")
    lines.append("  E (Easy): Remembering, hoặc Understanding cơ bản.")
    lines.append("  M (Medium): Phần lớn Understanding, Applying tiêu chuẩn.")
    lines.append("  H (Hard): Analyzing, Evaluating, Creating, hoặc Applying phức tạp.")
    lines.append("GIẢI THÍCH NGỮ CẢNH (suggestContext):")
    lines.append("  A: Lý thuyết/Trừu tượng, B: Ví dụ Cụ thể/Riêng, C: Hiện tượng Tự nhiên/Quan sát, D: Ứng dụng Công nghệ/Kỹ thuật, E: Thí nghiệm/Điều tra, F: Vấn đề Thực tế/Xã hội, G: Diễn giải Dữ liệu/Mô hình hóa, H: Lịch sử/Phát triển Khoa học, I: Liên ngành, J: Giả định/So sánh.")
    lines.append("")
    lines.append("code | name | bloom | question_type | example_vi")
    
    try:
        with open(matrix_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                lines.append(f"{row['code']} | {row['name']} | {row['bloom_level_code']} | {row['question_type_code']} | {row['example_vi']}")
    except Exception as e:
        print(f"[WARNING] Could not load approaches.tsv: {e}")
        return ""
        
    return "\n".join(lines)


MASTER_ULO_PATH = Path(".agents/skills/learning-objective-generator/resources/master_learning_objectives.tsv")

def load_master_ulos() -> dict[str, list[dict]]:
    """Loads all Master ULOs, grouped by concept code."""
    master_ulos = {}
    if not MASTER_ULO_PATH.is_file():
        return master_ulos
    try:
        with open(MASTER_ULO_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row.get("lo_type") == "UNIVERSAL":
                    concepts = [c.strip() for c in row.get("concept_codes", "").split(",") if c.strip()]
                    row["concept_codes"] = concepts
                    for c in concepts:
                        master_ulos.setdefault(c, []).append(row)
    except Exception as e:
        print(f"[WARNING] Could not load master ULOs: {e}")
    return master_ulos

def append_master_ulos(ulos: list[dict]):
    """Appends new Master ULOs to the master TSV (requires explicit user approval)."""
    master_path = MASTER_ULO_PATH
    print(f"\n⚠️  {len(ulos)} ULO mới sẽ được thêm vào {master_path}")
    print("   (AGENTS.md §5: Sửa resources/ chỉ khi được User cho phép rõ ràng)")
    confirm = input("   Tiếp tục? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("   ⏭️  Bỏ qua ghi master ULO bank.")
        return

    file_exists = master_path.is_file()
    fieldnames = ["code", "name", "description", "lo_type", "parent_lo_code",
                  "concept_codes", "bloom_level", "knowledge_dimension"]
    
    with open(master_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        if not file_exists or master_path.stat().st_size == 0:
            writer.writeheader()
        
        for u in ulos:
            writer.writerow({
                "code": u["code"],
                "name": u["name"],
                "description": u.get("description_vi", ""),
                "lo_type": "UNIVERSAL",
                "parent_lo_code": "",
                "concept_codes": ",".join(u.get("concept_codes", [])),
                "bloom_level": u.get("bloom_level", ""),
                "knowledge_dimension": u.get("knowledge_dimension", ""),
            })

# ─── Master Generation Prompts ───────────────────────────────────────────────

MASTER_ULO_SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Universal Learning Objectives (ULO) cho Master Knowledge Tree.

Nhiệm vụ của bạn: Với mỗi Concept được cung cấp, hãy sinh ra MỘT PHỔ (SPECTRUM) gồm 2-4 ULO phủ đều các bậc nhận thức Bloom phù hợp nhất với bản chất của Concept đó.
TUYỆT ĐỐI KHÔNG phụ thuộc vào bất kỳ giáo trình cụ thể nào. Bạn đang xây dựng Ngân hàng Tri thức gốc.

Nguyên tắc:
1. ULO KHÔNG chứa tên công nghệ, ngôn ngữ lập trình cụ thể (Python, Swift...).
2. [QUAN TRỌNG] Mã ULO PHẢI tuân theo cú pháp: `ULO-<CONCEPT_CODE>-<STT>`. Ví dụ: `ULO-LOOP_STRUCTURES-01`.
3. Bản chất Concept quyết định phổ Bloom:
   - Factual Concept (dữ kiện, thuật ngữ): Chỉ cần Remember, Understand.
   - Procedural Concept (cách làm, thuật toán): Cần Remember, Understand, Apply, có thể Analyze.
   - Conceptual (lý thuyết, kiến trúc): Cần Understand, Analyze, Evaluate.

QUAN TRỌNG: TRẢ VỀ JSON theo định dạng chuẩn."""

# ─── Curriculum Filter Prompts ───────────────────────────────────────────────

FILTER_ULO_SYSTEM = """Bạn là Chuyên gia Thiết kế Giáo trình (Curriculum Designer).
Nhiệm vụ của bạn: Từ Ngân hàng Master ULOs (Sở hữu tri thức), hãy CHỌN LỌC (SELECT) ra các ULO phù hợp nhất để đưa vào Khóa học cụ thể (Áp dụng tri thức).

Nguyên tắc lọc:
1. [BẤT BIẾN] TUYỆT ĐỐI KHÔNG sửa đổi nội dung, tên, hay mã của Master ULO. Phải giữ nguyên văn (immutable) để đảm bảo tính toàn vẹn dữ liệu. Bê y nguyên object JSON của ULO được chọn.
2. Dựa vào `Syllabus Action Phrases` (nếu có) để chọn ULO có mức Bloom khớp với trần nhận thức của giáo trình. Ví dụ: Nếu giáo trình yêu cầu "Recognize" (Remember), hãy chọn Master ULO bậc Remember, vứt bỏ các ULO bậc Apply/Analyze.
3. Dựa vào `Project Context` (đối tượng học viên, thời lượng) để quyết định số lượng ULO. Nếu khóa cơ bản, ưu tiên các ULO bậc thấp.
4. Nếu một Concept không có Syllabus Action Phrase đi kèm, hãy tự chọn 1-2 Master ULO phù hợp nhất với bối cảnh chung của khóa học.

QUAN TRỌNG: TRẢ VỀ JSON."""

# ─── Phase A: Generate/Filter ULOs ────────────────────────────────────────────

ULO_SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum chuyên viết Universal Learning Objectives (ULO).

ULO = Tầng Computational (Marr): mô tả NĂNG LỰC CỐT LÕI — WHAT và WHY — hoàn toàn độc lập với bất kỳ công nghệ/ngôn ngữ nào.

Nguyên tắc:
1. ULO KHÔNG chứa tên công nghệ, ngôn ngữ lập trình, framework, hay cú pháp.
2. ULO phải áp dụng được cho người học bất kể họ dùng Python, Swift, JavaScript hay ngôn ngữ nào.
3. [QUAN TRỌNG VỀ CODE] Mã ULO PHẢI tuân theo cú pháp: `ULO-<CONCEPT_CODE>-<STT>`. Ví dụ, nếu concept có mã là `LOOP_STRUCTURES`, thì ULO sinh ra phải có mã là `ULO-LOOP_STRUCTURES-01`.
4. [QUAN TRỌNG] "Trần nhận thức" (Cognitive Ceiling):
   - User sẽ cung cấp các Syllabus Action Phrases bắt buộc cho một số Concept.
   - Nếu Concept có Syllabus Phrase (VD: "Assess a visual design" -> Evaluate), bạn PHẢI biến nó thành ULO chính của Concept đó. Không đẻ thêm ULO bậc Create vô lý.
   - Nếu Syllabus Phrase ở mức thấp (VD: "Recognize", "List"), thì Năng lực cốt lõi của Concept đó chỉ ở mức thấp. Không cố ép sinh ULO ở mức Analyze/Evaluate.
5. [QUAN TRỌNG VỀ ĐỘNG TỪ TRẮC NGHIỆM] Ánh xạ động từ thực dụng:
   - Nếu Syllabus Action Phrase dùng các động từ kém thực dụng (khó đo lường bằng trắc nghiệm) như "Summarize" (Tóm tắt), "Understand" (Hiểu), "Know" (Biết)...
   - Bạn ĐƯỢC PHÉP tự động đổi sang các động từ thực dụng, dễ đo lường hơn thuộc CÙNG cấp độ Bloom trong tên và mô tả ULO. 
   - VD: "Summarize" có thể đổi thành "Explain" (Giải thích), "Identify" (Nhận diện), "Differentiate" (Phân biệt), hoặc "Interpret" (Diễn giải). Mục tiêu là mô tả hành vi làm bài cụ thể của người học.
6. "Đắp khoảng trống" (Gap-filling) linh hoạt:
   - KHÔNG ép mỗi Concept phải có 3 ULO hay đủ 6 bậc Bloom.
   - Nếu một Concept quá hiển nhiên, 1 ULO là đủ.
   - Chỉ sinh thêm ULO mới nếu thực sự cần thiết để hoàn thiện lộ trình sư phạm cho Concept đó.
   
QUAN TRỌNG: Bạn PHẢI trả về ĐÚNG ĐỊNH DẠNG JSON. TUYỆT ĐỐI KHÔNG giải thích, KHÔNG có markdown, KHÔNG bắt đầu bằng 'Dưới đây là...'. CHỈ TRẢ VỀ JSON."""


def generate_master_ulos_for_missing_concepts(
    client: OpenAI,
    missing_concepts: list[dict],
    model: str,
    no_master_append: bool = False,
) -> list[dict]:
    print(f"[*] Phân tích và sinh Master ULOs cho {len(missing_concepts)} concept mới...")
    new_master_ulos = []
    
    # Process in small batches so LLM doesn't hallucinate
    batch_size = 5
    for i in range(0, len(missing_concepts), batch_size):
        batch = missing_concepts[i:i+batch_size]
        concept_list = "\n".join(f"  - {c['code']}: {c['name']} — {c['description'][:80]}" for c in batch)
        
        user_prompt = (
            f"Hãy sinh phổ ULO (Spectrum of ULOs) cho các Concept sau:\n{concept_list}\n\n"
            "ĐỊNH DẠNG JSON TRẢ VỀ (Bắt buộc phải khớp chính xác):\n"
            "{\n"
            '  "ulos": [\n'
            "    {\n"
            '      "code": "ULO-<CONCEPT_CODE>-<STT>",\n'
            '      "name": "...",\n'
            '      "description_vi": "Người học có khả năng...",\n'
            '      "bloom_level": "...",\n'
            '      "knowledge_dimension": "...",\n'
            '      "concept_codes": ["CODE1"]\n'
            "    }\n"
            "  ]\n"
            "}"
        )
        
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": MASTER_ULO_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            result_json = json.loads(completion.choices[0].message.content)
            new_master_ulos.extend(result_json.get("ulos", []))
            print(f"  + Batch {i+1}-{i+len(batch)}: {len(result_json.get('ulos', []))} ULOs")
        except Exception as e:
            print(f"  [ERROR] Master Generation Failed for batch {i}: {e}")
            
    # Save back to master
    if new_master_ulos and not no_master_append:
        append_master_ulos(new_master_ulos)
    elif new_master_ulos and no_master_append:
        print(f"  ⏭️  --no-master-append: bỏ qua ghi {len(new_master_ulos)} ULO vào master bank.")
    return new_master_ulos


def filter_ulos(
    client: OpenAI,
    concepts: list[dict],
    syllabus: str,
    classified_phrases: list[dict],
    assessment_matrix_text: str,
    model: str,
    work_dir: Path,
    hlo_dir: Path,
    no_master_append: bool = False,
) -> list[dict]:
    # 1. Load Master ULOs
    master_ulos_db = load_master_ulos()
    
    # 2. Check for missing concepts in Master
    missing_concepts = []
    for c in concepts:
        if c["code"] not in master_ulos_db:
            missing_concepts.append(c)
            
    # 3. Generate Master ULOs for missing ones
    if missing_concepts:
        new_ulos = generate_master_ulos_for_missing_concepts(client, missing_concepts, model, no_master_append)
        # Reload DB to get the newly appended ULOs
        master_ulos_db = load_master_ulos()
        
    # 4. Gather available Master ULOs for this project's concepts
    available_ulos = []
    for c in concepts:
        if c["code"] in master_ulos_db:
            available_ulos.extend(master_ulos_db[c["code"]])
            
    # Remove duplicates if any
    seen_codes = set()
    unique_available_ulos = []
    for u in available_ulos:
        if u["code"] not in seen_codes:
            unique_available_ulos.append(u)
            seen_codes.add(u["code"])

    available_ulos_text = "DANH SÁCH MASTER ULOS CÓ SẴN (CHỈ CHỌN TỪ ĐÂY, KHÔNG SỬA ĐỔI):\n"
    for u in unique_available_ulos:
        available_ulos_text += f"- {u['code']} | Bloom: {u.get('bloom_level')} | Dim: {u.get('knowledge_dimension')} | Name: {u['name']}\n"
    
    ulo_phrases_text = ""
    ulo_phrases = [p for p in classified_phrases if p.get("lo_type") == "ULO"]
    if ulo_phrases:
        ulo_phrases_text = "CÁC ACTION PHRASES BẮT BUỘC (SYLLABUS ANCHORS):\n"
        for p in ulo_phrases:
            ulo_phrases_text += f"  - Concept: {p['mapped_concept_code']} | Verb: {p['verb']} ({p['cognitive_level']}) | Phrase: {p['phrase']}\n"
            
    user_prompt = (
        f"Project Syllabus / Context:\n{syllabus[:6000]}\n\n"
        f"{ulo_phrases_text}\n"
        f"{available_ulos_text}\n\n"
        "Nhiệm vụ: CHỌN LỌC các ULO phù hợp nhất từ danh sách Master ULOs để đưa vào Project này.\n"
        "ĐỊNH DẠNG JSON TRẢ VỀ (Bắt buộc phải chứa chính xác các object ULO đã chọn, y nguyên nội dung gốc):\n"
        "{\n"
        '  "ulos": [\n'
        "    {\n"
        '      "code": "ULO-...",\n'
        '      "name": "...",\n'
        '      "description_vi": "Người học có khả năng...",\n'
        '      "bloom_level": "...",\n'
        '      "knowledge_dimension": "...",\n'
        '      "concept_codes": ["CODE1"]\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    print("[A] Filtering ULOs from Master Bank ...")
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": FILTER_ULO_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,  # Temperature 0 for strict selection
    )
    try:
        result_json = json.loads(completion.choices[0].message.content)
        ulos = result_json.get("ulos", [])
    except Exception as e:
        print(f"[ERROR] JSON parse failed: {e}")
        ulos = []

    # Validation: Ensure selected ULOs exist in unique_available_ulos and are strictly immutable
    master_dict = {u["code"]: u for u in unique_available_ulos}
    final_ulos = []
    for u in ulos:
        if u["code"] in master_dict:
            # Overwrite with the exact master object to prevent any hallucinated modifications by LLM
            final_ulos.append(master_dict[u["code"]])
        else:
            print(f"[WARNING] LLM tried to select/invent an unknown ULO: {u['code']}")

    out_path = hlo_dir / "ulos.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final_ulos, f, ensure_ascii=False, indent=2)

    # Preview markdown
    _write_ulo_preview(hlo_dir / "ulos_preview.md", final_ulos)

    print(f"[✓] {len(final_ulos)} ULOs Filtered → {out_path}")
    print(f"[✓] Preview → {hlo_dir / 'ulos_preview.md'}")
    print(f"\n→ Xem ulos_preview.md, duyệt, rồi chạy /generate-cios")
    return final_ulos


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
        lines.append(f"> {u.get('description', u.get('description_vi', ''))}\n")
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
    assessment_matrix_text: str,
    model: str,
    hlo_dir: Path,
    batch_size: int = 10,
) -> list[dict]:
    all_cios = []

    ulo_summary = "\n".join(
        f"  - {u['code']}: {u['name']} — {u.get('description', u.get('description_vi', ''))[:80]}"
        for u in ulos
    )

    print(f"[B] Generating CIOs for {len(ulos)} ULOs (batch_size={batch_size}) ...")

    for i in range(0, len(ulos), batch_size):
        batch = ulos[i : i + batch_size]
        batch_text = "\n".join(
            f"ULO: {u['code']} | {u['name']}\n  Mô tả: {u.get('description', u.get('description_vi', ''))}"
            for u in batch
        )

        user_prompt = (
            f"Danh sách tất cả ULO trong project (để tham chiếu parent codes):\n{ulo_summary}\n\n"
            f"Syllabus Context (Assessment Matrix):\n{assessment_matrix_text}\n\n"
            f"Sinh CIOs cho các ULO sau:\n{batch_text}\n\n"
            "Với mỗi ULO, sinh 1-3 CIO. BẮT BUỘC thực hiện Marr 2-Language Test cho mỗi CIO.\n\n"
            "ĐỊNH DẠNG JSON TRẢ VỀ:\n"
            "QUAN TRỌNG: TRONG CÁC GIÁ TRỊ CHUỖI NHƯ marr_test_note, KHÔNG SỬ DỤNG DẤU NGOẶC KÉP (\") BÊN TRONG HOẶC PHẢI ESCAPE CHÚNG BẰNG BACKSLASH (\\\"). NẾU KHÔNG SẼ GÂY LỖI JSON!\n"
            "{\n"
            '  "cios": [\n'
            "    {\n"
            '      "code": "CIO-<CONCEPT_CODE>-<STT>",\n'
            '      "name": "...",\n'
            '      "description_vi": "Người học có khả năng...",\n'
            '      "bloom_level": "...",\n'
            '      "knowledge_dimension": "...",\n'
            '      "parent_ulo_code": "ULO-...",\n'
            '      "marr_test_note": "Lập luận Marr 2-Language test ở đây. Tránh dùng dấu ngoặc kép bên trong chuỗi này."\n'
            "    }\n"
            "  ]\n"
            "}"
        )

        try:
            result_json = _safe_llm_json(
                client, model, CIO_SYSTEM, user_prompt,
                temperature=0.2, batch_label=f"CIO batch {i+1}-{min(i+batch_size, len(ulos))}"
            )
            batch_cios = result_json.get("cios", []) if result_json else []
            if batch_cios:
                # Validate parent codes — surface hallucinations instead of
                # silently rebinding to batch[0] (§10 Bảo tồn & Minh bạch).
                valid_ulo_codes = {u["code"] for u in ulos}
                for c in batch_cios:
                    if c.get("parent_ulo_code") not in valid_ulo_codes:
                        original = c.get("parent_ulo_code", "")
                        c["parent_ulo_code"] = batch[0]["code"]  # fallback
                        c["_parent_fallback"] = original  # audit trail
                        print(f"  [WARN] CIO {c.get('code','?')} hallucinated parent "
                              f"'{original}' → rebound to '{batch[0]['code']}' "
                              f"(REVIEW NEEDED — fix in cios.json before /generate-sios)",
                              file=sys.stderr)
                all_cios.extend(batch_cios)
                print(f"  Batch {i+1}-{min(i+batch_size, len(ulos))}: +{len(batch_cios)} CIOs")
            elif not result_json:
                print(f"  Batch {i+1}: [SKIPPED] LLM call failed — no CIOs generated", file=sys.stderr)
        except Exception as e:
            print(f"  [WARN] Batch {i}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

    out_path = hlo_dir / "cios.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_cios, f, ensure_ascii=False, indent=2)

    # Write LLM failure audit trail (§10 Bảo tồn & Minh bạch)
    if _LLM_FAILURES:
        failures_path = hlo_dir / "llm_failures.json"
        with open(failures_path, "w", encoding="utf-8") as f:
            json.dump(_LLM_FAILURES, f, ensure_ascii=False, indent=2)
        print(f"\n[⚠️] {len(_LLM_FAILURES)} LLM call(s) failed during CIO generation", file=sys.stderr)
        print(f"  Audit trail: {failures_path}", file=sys.stderr)
        print(f"  CIO count may be INCOMPLETE — review before /generate-sios", file=sys.stderr)

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
        "| Code | Name | Parent ULO | Bloom | Dimension | Marr Test Note |",
        "|------|------|-----------|-------|-----------|----------------|",
    ]
    for c in cios:
        ulo_name = ulo_map.get(c["parent_ulo_code"], "?")
        marr = c.get("marr_test_note", "")[:80]
        lines.append(
            f"| `{c['code']}` | {c['name']} | `{c['parent_ulo_code']}` ({ulo_name}) | "
            f"{c['bloom_level']} | {c['knowledge_dimension']} | {marr} |"
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
5. Code SIO format: SIO-{tech_upper}-<SKILL_SLUG> (BẮT BUỘC IN HOA TOÀN BỘ, chỉ dùng chữ, số, gạch ngang/dưới. Ví dụ: SIO-SWIFT-DEFINE_FUNC)"""


def generate_sios(
    client: OpenAI,
    cios: list[dict],
    technology: str,
    assessment_matrix_text: str,
    keywords_text: str,
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
        
        keywords_section = ""
        if keywords_text:
            keywords_section = f"TỪ KHÓA ĐẶC THÙ (ATE Extracted Keywords):\nSử dụng các từ khóa sau để làm cho SIO gắn chặt với {technology}:\n{keywords_text}\n\n"

        user_prompt = (
            f"Danh sách tất cả CIO trong project (để tham chiếu parent codes):\n{cio_summary}\n\n"
            f"Assessment Matrix Reference:\n{assessment_matrix_text}\n\n"
            f"{keywords_section}"
            f"Sinh SIOs cho các CIO sau (mỗi CIO ≥ 2 SIOs):\n{batch_text}\n\n"
            "ĐỊNH DẠNG JSON TRẢ VỀ:\n"
            "{\n"
            '  "sios": [\n'
            "    {\n"
            '      "code": "SIO-...",\n'
            '      "name": "...",\n'
            '      "description_vi": "Người học có khả năng...",\n'
            '      "bloom_level": "...",\n'
            '      "knowledge_dimension": "...",\n'
            '      "parent_cio_code": "CIO-..."\n'
            "    }\n"
            "  ]\n"
            "}"
        )

        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            raw_content = completion.choices[0].message.content
            if raw_content.startswith("```json"):
                raw_content = raw_content.strip("` \n")
                if raw_content.startswith("json"):
                    raw_content = raw_content[4:].strip()
            elif raw_content.startswith("```"):
                raw_content = raw_content.strip("` \n")
            
            try:
                result_json = json.loads(raw_content)
            except json.JSONDecodeError:
                clean_content = raw_content.replace("\\", "\\\\")
                result_json = json.loads(clean_content)
            batch_sios = result_json.get("sios", [])
            
            if batch_sios:
                valid_cio_codes = {c["code"] for c in cios}
                for s in batch_sios:
                    if s["parent_cio_code"] not in valid_cio_codes:
                        s["parent_cio_code"] = batch[0]["code"]
                    if "code" in s and isinstance(s["code"], str):
                        s["code"] = s["code"].upper()
                all_sios.extend(batch_sios)
                print(f"  Batch {i+1}-{min(i+batch_size, len(cios))}: +{len(batch_sios)} SIOs")
        except Exception as e:
            print(f"  [WARN] Batch {i}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

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
    ulo_concept_map = {} # Maps ULO code to its concept_codes_str
    for u in ulos:
        concept_codes_str = ",".join(
            c for c in u.get("concept_codes", []) if c in valid_concept_codes
        )
        ulo_concept_map[u["code"]] = concept_codes_str
        rows.append({
            "code": u["code"],
            "name": u["name"],
            "description": u.get("description", u.get("description_vi", "")),
            "lo_type": "UNIVERSAL",
            "parent_lo_code": "",
            "concept_codes": concept_codes_str,
            "bloom_level": u.get("bloom_level", ""),
            "knowledge_dimension": u.get("knowledge_dimension", ""),
            "assessment_approach": u.get("assessment_approach", "")
        })

    # CIOs
    cio_concept_map = {} # Maps CIO code to its concept_codes_str
    for c in cios:
        parent_ulo = c.get("parent_ulo_code", "")
        inherited_concept_codes = ulo_concept_map.get(parent_ulo, "")
        cio_concept_map[c["code"]] = inherited_concept_codes
        
        rows.append({
            "code": c["code"],
            "name": c["name"],
            "description": c.get("description", c.get("description_vi", "")),
            "lo_type": "CONCEPTUAL_IMPL",
            "parent_lo_code": parent_ulo,
            "concept_codes": inherited_concept_codes,
            "bloom_level": c.get("bloom_level", ""),
            "knowledge_dimension": c.get("knowledge_dimension", ""),
            "assessment_approach": c.get("assessment_approach", "")
        })

    # SIOs
    for s in sios:
        parent_cio = s.get("parent_cio_code", "")
        inherited_concept_codes = cio_concept_map.get(parent_cio, "")
        
        rows.append({
            "code": s["code"],
            "name": s["name"],
            "description": s.get("description", s.get("description_vi", "")),
            "lo_type": "SPECIFIC_IMPL",
            "parent_lo_code": parent_cio,
            "concept_codes": inherited_concept_codes,
            "bloom_level": s.get("bloom_level", ""),
            "knowledge_dimension": s.get("knowledge_dimension", ""),
            "assessment_approach": s.get("assessment_approach", "")
        })

    fieldnames = ["code", "name", "description", "lo_type", "parent_lo_code",
                  "concept_codes", "bloom_level", "knowledge_dimension", "assessment_approach"]

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
    parser.add_argument("--no-master-append", action="store_true",
                        help="Skip appending new ULOs to master ULO bank (resources/)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    load_env(repo_root)
    os.chdir(repo_root)  # Anchor relative paths (e.g. MASTER_ULO_PATH) to repo root

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
    base_url = os.environ.get("OPENAI_BASE_URL")
    client = OpenAI(api_key=api_key, base_url=base_url)

    concepts = load_concepts(out_dir / "concepts.tsv")
    if not concepts and args.phase != "merge":
        print(f"[WARN] concepts.tsv không tìm thấy. Chạy /build-tree trước.", file=sys.stderr)

    technology = args.technology or detect_technology(project_dir, slug)
    assessment_matrix_text = load_assessment_matrix(repo_root)
    print(f"[*] Project: {slug} | Technology: {technology} | Phase: {args.phase}")

    if args.phase in ("ulos", "all"):
        syllabus = load_syllabus(work_dir)
        classified_phrases = load_classified_phrases(out_dir)
        ulos = filter_ulos(
            client, concepts, syllabus, classified_phrases,
            assessment_matrix_text, args.model, work_dir, hlo_dir,
            no_master_append=args.no_master_append,
        )
        if args.phase != "all":
            return

    if args.phase in ("cios", "all"):
        ulo_path = hlo_dir / "ulos.json"
        if not ulo_path.is_file():
            print("[ERROR] ulos.json không tìm thấy. Chạy --phase ulos trước.", file=sys.stderr)
            sys.exit(1)
        with open(ulo_path, encoding="utf-8") as f:
            ulos = json.load(f)
        cios = generate_cios(client, ulos, assessment_matrix_text, args.model, hlo_dir, args.batch_size)
        if args.phase != "all":
            return

    if args.phase in ("sios", "all"):
        cio_path = hlo_dir / "cios.json"
        if not cio_path.is_file():
            print("[ERROR] cios.json không tìm thấy. Chạy --phase cios trước.", file=sys.stderr)
            sys.exit(1)
        with open(cio_path, encoding="utf-8") as f:
            cios = json.load(f)
            
        # Extract keywords if available
        keywords_text = ""
        kw_path = project_dir / "context" / "keywords.tsv"
        if not kw_path.is_file():
            kw_path = out_dir / "keywords.tsv"
        
        if kw_path.is_file():
            try:
                import pandas as pd
                df = pd.read_csv(kw_path, sep="\t")
                if "term" in df.columns:
                    terms = df["term"].dropna().tolist()
                    keywords_text = ", ".join(terms)
                    print(f"[*] Loaded {len(terms)} keywords from {kw_path.name}")
            except Exception as e:
                print(f"[WARN] Failed to load keywords.tsv: {e}")

        sios = generate_sios(
            client, cios, technology, assessment_matrix_text, 
            keywords_text, args.model, hlo_dir, args.batch_size
        )
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
