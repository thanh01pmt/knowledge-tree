#!/usr/bin/env python3
"""
STEP 1 — LLM Project Graph (canonical v3, 8 domain).

Chia 3 LLM calls theo cụm domain (tránh 1 call khổng lồ):
  Call A: 01 Identity + 02 Product + 03 Feature + 04 Architecture
  Call B: 05 Experience/UI + 06 Data & Integration
  Call C: 07 Implementation (Capability/Task/Dependency) + 08 Validation

Input: merged source (### FILE: <path> headers) từ STEP 0 + goal + tech_stack
Output: project_graph_raw.json (schema v3)

Usage:
  python step1_project_graph_llm.py \
    --source-file /tmp/merged.txt \
    --goal "Xây app chat iOS dùng StreamChat SDK" \
    --tech-stack "Swift,SwiftUI,StreamChat" \
    --output /tmp/project_graph_raw.json
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]  # scripts → project-graph-v3 → scratch → repo root
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

# Load schema v3 để nhúng vào prompt (chuẩn hoá — Agent không tự nghĩ schema)
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "project_graph.schema.v3.json"
SCHEMA = json.load(open(SCHEMA_PATH, encoding="utf-8"))

# ============ DOMAIN GROUPS (bật/tắt từng phần) ============

# Domain → call nào chạy + mô tả ngắn cho prompt
CALL_GROUPS = {
    "identity":      ("A", "project (Identity): id/name/purpose/platform/tech_stack/source"),
    "product":       ("A", "product (Product Graph): goals/users/journeys/requirements"),
    "feature":       ("A", "features (Feature Graph): capability của sản phẩm, priority, status"),
    "capability":    ("A", "capabilities: cầu nối Feature → Task (purpose/depends_on/produces)"),
    "architecture":  ("A", "architecture (Architecture Graph): pattern/confidence/nodes/edges — FACT vs INFERENCE"),
    "experience":    ("B", "experience (Experience/UI Graph): screens/components/ui_states/navigation"),
    "data":          ("B", "data_integration (Data & Integration Graph): data_flows/models/integrations/persistence"),
    "implementation": ("C", "implementation (Implementation Graph): tasks/task_dependencies — mỗi task kèm intent/outcome/source_evidence"),
    "validation":    ("C", "validation (Validation Graph): validations/quality_requirements"),
}
ALL_DOMAINS = list(CALL_GROUPS.keys())

# ============ PROFILES (bật theo nhóm) ============
# lite: phân tích nhanh sản phẩm + features (1 call)
# essential: + kiến trúc + implementation cốt lõi (task có keywords/effort)
# full: tất cả domain + chi tiết (concurrency, missing_gaps, tech_debt, state machine)
PROFILES = {
    "lite": ["product", "feature"],
    "essential": ["identity", "product", "feature", "capability", "architecture", "implementation"],
    "full": ALL_DOMAINS,
}
PROFILE_EXTRA_INSTRUCTIONS = {
    "lite": "",
    "essential": (
        "\nBỔ SUNG (essential):\n"
        "- feature.api_usage[]: API/framework methods feature dùng (VD: ChatClient.connectUser, queryChannels).\n"
        "- task.keywords[]: API/framework/property wrapper task dùng (VD: '@State', 'ChatClient').\n"
        "- task.effort: ước lượng độ nặng (concepts_count, files_touched, estimated_minutes).\n"
    ),
    "full": (
        "\nBỔ SUNG (full):\n"
        "- feature.api_usage[]: API/framework methods feature dùng.\n"
        "- task.keywords[]: API/framework/property wrapper task dùng.\n"
        "- task.concurrency[]: cơ chế async dùng (Task, DispatchQueue, async/await).\n"
        "- task.effort: ước lượng độ nặng.\n"
        "- screen.keywords[]: framework/property wrapper screen dùng.\n"
        "- implementation.missing_gaps[]: điều code THIẾU (missing error handling/test/hardcoded) — roadmap dạy bổ sung.\n"
        "- implementation.tech_debt[]: tech debt signals (file lớn, logic lồng sâu) — Polish.\n"
        "- validation.quality_requirements: accessibility/security/localization (B2/B3/B6).\n"
    ),
}

# Flag domain → schema property key
FLAG_TO_SCHEMA_KEY = {
    "identity": "project", "product": "product", "feature": "features",
    "capability": "capabilities", "architecture": "architecture",
    "experience": "experience", "data": "data_integration",
    "implementation": "implementation", "validation": "validation",
}

# Schema subset theo domain (giảm prompt khi lite)
def schema_subset(domains: list) -> str:
    """Cắt schema chỉ giữ các property được bật."""
    props = SCHEMA.get("properties", {})
    keys = [FLAG_TO_SCHEMA_KEY[d] for d in domains if d in FLAG_TO_SCHEMA_KEY and FLAG_TO_SCHEMA_KEY[d] in props]
    subset = {
        "$schema": SCHEMA.get("$schema"),
        "type": "object",
        "required": ["schema_version"] + keys,
        "properties": {k: props[k] for k in keys},
    }
    # Thêm definitions.edges nếu có domain dùng nó
    if "architecture" in domains or "implementation" in domains:
        subset["definitions"] = {"edges": SCHEMA.get("definitions", {}).get("edges", {})}
    return json.dumps(subset, ensure_ascii=False)


# ============ PROMPT BUILDERS ============

BASE_SYSTEM = (
    "Bạn là kiến trúc sư phần mềm phân tích source code thành Project Graph chuẩn hóa.\n"
    "Project Graph là canonical representation: mô tả 'project cần được xây dựng như thế nào', "
    "KHÔNG phải AST, KHÔNG phải Knowledge Tree, KHÔNG phải roadmap.\n"
    "NGUYÊN TẮC:\n"
    "1. App người dùng sẽ xây CHÍNH LÀ các files được cung cấp (không phải SDK/lib bên ngoài).\n"
    "2. Mỗi thông tin suy ra phải có evidence: file tồn tại, symbol có trong file. CẤM bịa file/symbol.\n"
    "3. FACT vs INFERENCE tách bạch: file/symbol/keyword = OBSERVED; architecture/pattern = INFERRED "
    "kèm confidence + evidence.\n"
    "4. Boundary: KHÔNG đưa bloom level, quiz, mastery, lesson sequence, teaching content vào Project Graph.\n"
    "5. Task là ACTION có thể thực hiện ('Implement search query state'), KHÔNG phải 'Learn State'. "
    "Mỗi task có intent (WHY) + outcome (WHAT thay đổi sau task).\n"
    "6. Trả JSON ĐÚNG schema. Chỉ điền các field bạn có bằng chứng từ code.\n"
    "7. GÓC NHÌN END-USER (product domain): goals/users/requirements phải mô tả từ góc nhìn "
    "NGƯỜI DÙNG CUỐI dùng app — 'User có thể đăng nhập', 'User có thể xem danh sách channel', "
    "'User có thể gửi tin nhắn'. CẤM mô tả repo/artifact (VD 'Provide a demo app', 'Serve as "
    "reference implementation', 'preview SDK features'). User = actor dùng app, goals = hành động "
    "họ làm được.\n"
    "8. SCAFFOLD (NỀN TẢNG): ngoài việc phân tích code hiện có, phải xác định bước KHỞI TẠO dự án "
    "mà người học cần — tạo project từ template của nền tảng (Xcode/SwiftUI template, cấu trúc file "
    "sinh sẵn: AppDelegate, ContentView, Assets...), build chạy được đầu tiên, làm quen công cụ. "
    "Đây là bước TRƯỚC khi code tồn tại — phân tích từ tech_stack + cấu trúc repo, không phải từ "
    "nội dung file.\n"
)

def _file_context(source_text: str, max_chars: int) -> str:
    """Cắt source theo giới hạn ký tự, giữ header # FILE:."""
    if len(source_text) <= max_chars:
        return source_text
    return source_text[:max_chars] + "\n... (TRUNCATED — còn lại không đưa vào prompt này)"

def _schema_section(domains: list = None) -> str:
    """Nhúng schema (hoặc subset theo domain được bật) vào prompt."""
    if domains is None or set(domains) == set(ALL_DOMAINS):
        return json.dumps(SCHEMA, ensure_ascii=False, indent=1)
    return schema_subset(domains)

def build_call_a(source_text: str, goal: str, tech_stack: str, max_chars: int = 60000,
                 domains: list = None,
                 profile_extra: str = "") -> tuple:
    """Call A: Identity + Product + Feature + Architecture (theo domains bật)."""
    domains = domains or ["identity", "product", "feature", "capability", "architecture"]
    domain_desc = "; ".join(CALL_GROUPS[d][1] for d in domains if d in CALL_GROUPS)
    system = BASE_SYSTEM + (
        f"\n\nNHIỆM VỤ NÀY: Phân tích các domain: {domain_desc}.\n"
        "Trả JSON theo schema — chỉ điền các field của domain được yêu cầu, các domain khác để rỗng ([] / {} như schema).\n"
        + profile_extra + "\n"
    )
    user = (
        f"GOAL: {goal}\nTECH_STACK: {tech_stack}\n\n"
        f"SOURCE CODE (files có header '# FILE: <path>'):\n\n"
        f"{_file_context(source_text, max_chars)}\n\n"
        f"SCHEMA (điền đúng, chỉ các domain được yêu cầu):\n{_schema_section(domains)}"
    )
    return system, user

def build_call_b(source_text: str, goal: str, tech_stack: str, features_summary: str, max_chars: int = 40000,
                 domains: list = None,
                 profile_extra: str = "") -> tuple:
    """Call B: Experience/UI + Data & Integration (theo domains bật)."""
    domains = domains or ["experience", "data"]
    domain_desc = "; ".join(CALL_GROUPS[d][1] for d in domains if d in CALL_GROUPS)
    system = BASE_SYSTEM + (
        f"\n\nNHIỆM VỤ NÀY: Phân tích các domain: {domain_desc}.\n"
        "Dựa trên features đã xác định (đưa trong user prompt) — gắn UI/data vào features đó.\n"
        "Trả JSON theo schema — chỉ điền domain được yêu cầu, các domain khác để rỗng.\n"
        + profile_extra + "\n"
    )
    user = (
        f"GOAL: {goal}\nTECH_STACK: {tech_stack}\n\n"
        f"FEATURES (đã xác định ở call trước):\n{features_summary}\n\n"
        f"SOURCE CODE:\n\n{_file_context(source_text, max_chars)}\n\n"
        f"SCHEMA:\n{_schema_section(domains)}"
    )
    return system, user

def build_call_c(source_text: str, goal: str, features_summary: str, arch_summary: str, max_chars: int = 60000,
                 domains: list = None,
                 profile_extra: str = "") -> tuple:
    """Call C: Implementation + Validation (theo domains bật)."""
    domains = domains or ["implementation", "validation"]
    domain_desc = "; ".join(CALL_GROUPS[d][1] for d in domains if d in CALL_GROUPS)
    system = BASE_SYSTEM + (
        f"\n\nNHIỆM VỤ NÀY: Phân tích các domain: {domain_desc}.\n"
        "Mỗi task: action = hành động cụ thể, intent = WHY, outcome = WHAT thay đổi, "
        "source_evidence = file thật minh hoạ (KHÔNG phải 'task = tạo file đó').\n"
        "Trả JSON theo schema — chỉ điền domain được yêu cầu, các domain khác để rỗng.\n"
        + profile_extra + "\n"
    )
    user = (
        f"GOAL: {goal}\n\n"
        f"FEATURES:\n{features_summary}\n\n"
        f"ARCHITECTURE:\n{arch_summary}\n\n"
        f"SOURCE CODE:\n\n{_file_context(source_text, max_chars)}\n\n"
        f"SCHEMA:\n{_schema_section(domains)}"
    )
    return system, user

# ============ LLM CALL ============

def _llm_json(system: str, user: str, retries: int = 1) -> dict:
    if not _LLM_AVAILABLE:
        raise RuntimeError("LLM không available (llm_call import fail)")
    client, _provider, model = get_llm_client()
    last_err = None
    for attempt in range(retries + 1):
        try:
            res = llm_chat_json(client=client, model=model, system=system, user=user, temperature=0.1)
            if isinstance(res, dict):
                return res
        except Exception as e:
            last_err = e
    raise RuntimeError(f"LLM JSON call fail sau {retries+1} lần: {last_err}")


def merge_domains(a: dict, b: dict, c: dict, domains: list = None) -> dict:
    """Gộp 3 kết quả domain thành 1 project graph hoàn chỉnh (bỏ domain không bật)."""
    domains = domains or ALL_DOMAINS
    result = {
        "schema_version": 3,
        "project": a.get("project", {}) if "identity" in domains else {},
        "product": a.get("product", {}) if "product" in domains else {},
        "features": a.get("features", []) if "feature" in domains else [],
        "capabilities": a.get("capabilities", []) if "capability" in domains else [],
        "architecture": a.get("architecture", {}) if "architecture" in domains else {},
        "experience": b.get("experience", {}) if "experience" in domains else {},
        "data_integration": b.get("data_integration", {}) if "data" in domains else {},
        "implementation": c.get("implementation", {}) if "implementation" in domains else {},
        "validation": c.get("validation", {}) if "validation" in domains else {},
        "evidence": {},  # STEP 2 (verify) sẽ điền — không phải LLM
        "knowledge_mapping": {},  # STEP 3 (standardize) sẽ điền
    }
    return result


def run_pipeline(source_file: Path, goal: str, tech_stack: str, output_path: Path,
                 max_chars_a: int = 60000, max_chars_b: int = 40000, max_chars_c: int = 60000,
                 include_domains: list = None, profile: str = None) -> dict:
    """Chỉ chạy các call có domain được bật (--include hoặc --profile). Bỏ call không cần → tiết kiệm LLM."""
    if profile:
        include_domains = PROFILES.get(profile, include_domains)
    domains = include_domains or ALL_DOMAINS
    profile_extra = PROFILE_EXTRA_INSTRUCTIONS.get(profile or "full", "")
    group_a = [d for d in domains if CALL_GROUPS.get(d, ("", ""))[0] == "A"]
    group_b = [d for d in domains if CALL_GROUPS.get(d, ("", ""))[0] == "B"]
    group_c = [d for d in domains if CALL_GROUPS.get(d, ("", ""))[0] == "C"]

    source_text = source_file.read_text(encoding="utf-8", errors="ignore")
    print(f"[*] Source: {source_file} ({len(source_text):,} chars) | domains: {domains}")

    res_a, res_b, res_c = {}, {}, {}

    if group_a:
        print(f"[*] Call A: {group_a}...")
        sys_a, user_a = build_call_a(source_text, goal, tech_stack, max_chars_a, domains=group_a, profile_extra=profile_extra)
        res_a = _llm_json(sys_a, user_a)

    # Tóm tắt features cho call B/C (nếu có data)
    features_summary = json.dumps(res_a.get("features", []), ensure_ascii=False)[:8000]
    arch_summary = json.dumps(res_a.get("architecture", {}), ensure_ascii=False)[:4000]

    if group_b:
        print(f"[*] Call B: {group_b}...")
        sys_b, user_b = build_call_b(source_text, goal, tech_stack, features_summary, max_chars_b, domains=group_b, profile_extra=profile_extra)
        res_b = _llm_json(sys_b, user_b)

    if group_c:
        print(f"[*] Call C: {group_c}...")
        sys_c, user_c = build_call_c(source_text, goal, features_summary, arch_summary, max_chars_c, domains=group_c, profile_extra=profile_extra)
        res_c = _llm_json(sys_c, user_c)

    # Merge (bỏ domain không bật)
    result = merge_domains(res_a, res_b, res_c, domains)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    n_features = len(result["features"])
    n_tasks = len(result["implementation"].get("tasks", []))
    print(f"[✓] Project Graph raw: {n_features} features, {n_tasks} tasks → {output_path}")
    return result


def main():
    parser = argparse.ArgumentParser(description="STEP 1 — LLM Project Graph (canonical v3, 3 calls)")
    parser.add_argument("--source-file", required=True, type=Path, help="Merged source từ STEP 0")
    parser.add_argument("--goal", default="", help="Application goal")
    parser.add_argument("--tech-stack", default="", help="Technologies (comma-separated)")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile", default=None, choices=["lite", "essential", "full"],
                        help="(PROFILE) lite: product+feature (1 call) | essential: +architecture+implementation | full: tất cả")
    parser.add_argument("--include", default=None,
                        help="(BẬT/TẮT DOMAIN) Chỉ phân tích các domain, comma-separated. "
                             "VD: --include product,feature (lite) | --include implementation "
                             "| bỏ qua = tất cả. Domain: " + ",".join(ALL_DOMAINS))
    args = parser.parse_args()

    include_domains = None
    if args.include:
        include_domains = [d.strip() for d in args.include.split(",") if d.strip()]
        invalid = [d for d in include_domains if d not in ALL_DOMAINS]
        if invalid:
            parser.error(f"--include có domain không hợp lệ: {invalid}. Hợp lệ: {ALL_DOMAINS}")

    if not args.source_file.is_file():
        print(f"❌ Source file không tồn tại: {args.source_file}", file=sys.stderr)
        sys.exit(1)

    try:
        run_pipeline(args.source_file, args.goal, args.tech_stack, args.output,
                     include_domains=include_domains, profile=args.profile)
    except Exception as e:
        print(f"❌ STEP 1 fail: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
