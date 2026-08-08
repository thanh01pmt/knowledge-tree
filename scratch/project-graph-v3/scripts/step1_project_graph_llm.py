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
    "feature":       ("A", "features (Feature Graph): product capabilities, priority, status"),
    "capability":    ("A", "capabilities: bridge Feature → Task (purpose/depends_on/produces)"),
    "architecture":  ("A", "architecture (Architecture Graph): pattern/confidence/nodes/edges — FACT vs INFERENCE"),
    "experience":    ("B", "experience (Experience/UI Graph): screens/components/ui_states/navigation"),
    "data":          ("B", "data_integration (Data & Integration Graph): data_flows/models/integrations/persistence"),
    "implementation": ("C", "implementation (Implementation Graph): tasks/task_dependencies — each task with intent/outcome/source_evidence"),
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
        "\nADDITIONAL (essential):\n"
        "- feature.api_usage[]: API/framework methods the feature uses (e.g. ChatClient.connectUser, queryChannels).\n"
        "- task.keywords[]: API/framework/property wrapper the task uses (e.g. '@State', 'ChatClient').\n"
        "- task.effort: workload estimate (concepts_count, files_touched, estimated_minutes).\n"
    ),
    "full": (
        "\nADDITIONAL (full):\n"
        "- feature.api_usage[]: API/framework methods the feature uses.\n"
        "- task.keywords[]: API/framework/property wrapper the task uses.\n"
        "- task.concurrency[]: async mechanisms used (Task, DispatchQueue, async/await).\n"
        "- task.effort: workload estimate.\n"
        "- screen.keywords[]: framework/property wrapper the screen uses.\n"
        "- implementation.missing_gaps[]: code that is MISSING (error handling/test/hardcoded) — the roadmap teaches it as follow-up work.\n"
        "- implementation.tech_debt[]: tech debt signals (large files, deeply nested logic) — Polish phase.\n"
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
    "You are a software architect analyzing source code into a canonical Project Graph.\n"
    "The Project Graph is a canonical representation: it describes 'how the project should be built', "
    "NOT an AST, NOT a Knowledge Tree, NOT a roadmap.\n"
    "RULES:\n"
    "1. The app the learner will build IS EXACTLY the provided files (not external SDKs/libs).\n"
    "2. Every inferred fact must have evidence: file exists, symbol present in file. NEVER invent files/symbols.\n"
    "3. Keep FACT vs INFERENCE separate: file/symbol/keyword = OBSERVED; architecture/pattern = INFERRED "
    "with confidence + evidence.\n"
    "4. Boundary: DO NOT put bloom levels, quizzes, mastery, lesson sequences, or teaching content into the Project Graph.\n"
    "5. A task is an ACTION that can be performed ('Implement search query state'), NOT 'Learn State'. "
    "Each task has intent (WHY) + outcome (WHAT changes after the task).\n"
    "6. Return JSON matching the schema exactly. Fill only fields you have code evidence for.\n"
    "7. END-USER PERSPECTIVE (product domain): goals/users/requirements must be described from the "
    "END USER's perspective of using the app — 'User can sign in', 'User can view the channel list', "
    "'User can send a message'. NEVER describe repo/artifacts (e.g. 'Provide a demo app', 'Serve as "
    "reference implementation', 'preview SDK features'). User = the actor using the app; goals = the "
    "actions they can perform.\n"
    "8. SCAFFOLD (FOUNDATION): besides analyzing the existing code, identify the PROJECT INITIALIZATION "
    "step the learner needs — creating the project from the platform template (Xcode/SwiftUI template, "
    "generated file structure: AppDelegate, ContentView, Assets...), first successful build, getting "
    "familiar with the tooling. This step comes BEFORE the code exists — derive it from tech_stack + "
    "repo structure, not from file contents.\n"
    "9. project_type (identity domain) is REQUIRED: one of "
    "['mobile_app', 'web_app', 'cli_tool', 'library_sdk', 'desktop_app', 'backend_service', "
    "'fullstack_app', 'game', 'design_tool', 'ai_agent', 'plugin_extension', 'data_pipeline', 'other']. "
    "Always fill it; never leave it null/empty.\n"
    "10. completion_level (product domain, per requirement) is REQUIRED for EVERY requirement: "
    "one of ['base', 'mvp', 'extend', 'polish'] — base = foundation needed first, mvp = core "
    "functionality works, extend = add more, polish = finalize/refactor.\n"
    "11. Architecture confidence: a node/pattern with REAL structural evidence (directories named "
    "ViewModel/, Model/, View/; files whose names indicate their role) must have INFERRED confidence ≥ 0.7. "
    "Only use low confidence (0.3-0.5) for guesses without evidence.\n"
    "12. development_stages (product domain) is REQUIRED — a cross-feature NARRATIVE of growth.\n"
    "Describe how this app evolves through STAGES from minimal to complete, where each stage is a "
    "RUNNABLE product milestone (incremental walking skeleton).\n"
    "IMPORTANT — order by LEARNING LOGIC (Reigeluth elaboration: easy/quick-feedback first, "
    "heavy configuration later), NOT by completion_level:\n"
    "  - STAGE 1 = PURE FOUNDATION (M2 scaffold): get familiar with the IDE/platform (Xcode, simulator), "
    "get familiar with the LANGUAGE (Swift basic syntax), set up the project from the template, build and "
    "run the default template, quick wins (edit a few demo Texts and see the result). "
    "Stage 1 MUST NOT contain project-specific features (NO app WelcomeView, NO SecureTextField "
    "component, NO app navigation) — only platform/template basics.\n"
    "  - From stage 2 onward, work on the project's UI/features (WelcomeView, forms, components) — "
    "simple first (runnable screens, fake/temporary data), complex later.\n"
    "  - Heavy backend/config (Firebase configure, singletons, API keys) must NOT be front-loaded — "
    "push them down until after a working UI exists.\n"
    "  - Each stage: product_state (what the user can do), need (features/tasks to implement), "
    "learn (knowledge needed), validation (how to know it is done).\n"
    "  - The final stage = the complete product as it exists in the current repo.\n"
    "CROSS-FEATURE ADDITIVE VALUE: each stage must clearly describe the value it ADDS to the overall "
    "product (e.g. the auth stage adds 'the user has their own identity' on top of the existing UI, "
    "not as an isolated feature). The product after each stage = previous product + new layer.\n"
    "NON-LINEARITY: allow/anticipate TEMPORARY SCAFFOLDS for fast testing — intermediate solutions "
    "NOT present in the final architecture (mock data, temporary local storage instead of Firebase, "
    "hardcoded tokens, temporary navigation instead of auth gate). Note in need as 'temporarily use X "
    "to test Y' and state which stage replaces it with the real solution (e.g. 'temporarily store the "
    "session with UserDefaults for fast testing, replaced by FirebaseAuth in stage 3').\n"
    "Generate 4-6 stages, each tied to REAL features/tasks in the graph.\n"
    "13. LANGUAGE: write ALL generated text — goals, purposes, requirements, feature descriptions, "
    "task actions, intents, outcomes, source notes, and stage narratives — IN ENGLISH. "
    "Keep technical identifiers (class names, APIs) verbatim.\n"
)

def _file_context(source_text: str, max_chars: int) -> str:
    """Cut source to the char limit, keeping the # FILE: headers."""
    if len(source_text) <= max_chars:
        return source_text
    return source_text[:max_chars] + "\n... (TRUNCATED — the rest is not included in this prompt)"

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
        f"\n\nTHIS TASK: Analyze the domains: {domain_desc}.\n"
        "Return JSON matching the schema — fill only the fields of the requested domains; leave the other domains empty ([] / {} as in the schema).\n"
        + profile_extra + "\n"
    )
    user = (
        f"GOAL: {goal}\nTECH_STACK: {tech_stack}\n\n"
        f"SOURCE CODE (files have '# FILE: <path>' headers):\n\n"
        f"{_file_context(source_text, max_chars)}\n\n"
        f"SCHEMA (fill exactly, only the requested domains):\n{_schema_section(domains)}"
    )
    return system, user

def build_call_b(source_text: str, goal: str, tech_stack: str, features_summary: str, max_chars: int = 40000,
                 domains: list = None,
                 profile_extra: str = "") -> tuple:
    """Call B: Experience/UI + Data & Integration (theo domains bật)."""
    domains = domains or ["experience", "data"]
    domain_desc = "; ".join(CALL_GROUPS[d][1] for d in domains if d in CALL_GROUPS)
    system = BASE_SYSTEM + (
        f"\n\nTHIS TASK: Analyze the domains: {domain_desc}.\n"
        "Base on the features already identified (provided in the user prompt) — attach UI/data to those features.\n"
        "Return JSON matching the schema — fill only the requested domains; leave the others empty.\n"
        + profile_extra + "\n"
    )
    user = (
        f"GOAL: {goal}\nTECH_STACK: {tech_stack}\n\n"
        f"FEATURES (identified in the previous call):\n{features_summary}\n\n"
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
        f"\n\nTHIS TASK: Analyze the domains: {domain_desc}.\n"
        "Each task: action = a concrete action, intent = WHY, outcome = WHAT changes, "
        "source_evidence = the list of EXACT FILE PATHS taken from the '# FILE: <path>' headers in SOURCE CODE. "
        "REQUIRED: every source_evidence entry must be a path identical to a header (e.g. 'Talky/ViewModel/AuthViewModel.swift'), "
        "NO descriptive text, NO file contents, NO 'task = create file'. "
        "If a task involves multiple files, list every path. "
        "If a task has no file yet (e.g. a scaffold task), leave it empty [].\n"
        "Return JSON matching the schema — fill only the requested domains; leave the others empty.\n"
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


def _trim_json(obj, max_chars: int) -> str:
    """Serialize obj → JSON hợp lệ, ≤ max_chars.

    KHÔNG cắt chuỗi theo chỉ số ký tự thô ([:N] — vỡ cú pháp JSON + mất chữ giữa
    từ; bài học §3.3 academic-practices-applied.md). Cắt theo CẤU TRÚC:
      1. Bỏ field mô tả dài (description/rationale/...) — ít giá trị cross-reference
      2. Co chuỗi còn lại theo biên từ với '…'
      3. Bỏ phần tử cuối (list) / key cuối (dict) tới khi vừa budget
    Luôn trả về JSON parse được (trường hợp biên: hơi quá budget nhưng không vỡ).
    """
    def _len(x) -> int:
        return len(json.dumps(x, ensure_ascii=False))

    s = json.dumps(obj, ensure_ascii=False)
    if len(s) <= max_chars:
        return s

    HEAVY = {"description", "rationale", "acceptance", "details",
             "outcome", "evidence", "purpose", "product_state"}

    def drop_heavy(x):
        if isinstance(x, dict):
            return {k: drop_heavy(v) for k, v in x.items() if k not in HEAVY}
        if isinstance(x, list):
            return [drop_heavy(i) for i in x]
        return x

    def shrink_strings(x, budget):
        if isinstance(x, str) and len(x) > budget:
            cut = x[:budget]
            cut = cut.rsplit(" ", 1)[0] if " " in cut else cut
            return cut + "…"
        if isinstance(x, dict):
            return {k: shrink_strings(v, budget) for k, v in x.items()}
        if isinstance(x, list):
            return [shrink_strings(i, budget) for i in x]
        return x

    def drop_tail(x):
        while _len(x) > max_chars:
            if isinstance(x, list):
                if len(x) <= 1:
                    break
                x = x[:-1]
            elif isinstance(x, dict):
                if not x:
                    break
                x = {k: v for k, v in list(x.items())[:-1]}
            else:
                break
        return x

    # Bước 1: bỏ field mô tả dài
    light = drop_heavy(obj)
    if _len(light) <= max_chars:
        return json.dumps(light, ensure_ascii=False)
    # Bước 2: co chuỗi dài theo biên từ
    shrunk = shrink_strings(light, max(64, max_chars // 4))
    if _len(shrunk) <= max_chars:
        return json.dumps(shrunk, ensure_ascii=False)
    # Bước 3: bỏ phần tử cuối
    return json.dumps(drop_tail(shrunk), ensure_ascii=False)


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

    # Tóm tắt features cho call B/C (nếu có data) — trim theo CẤU TRÚC, không cắt
    # giữa chuỗi: giữ JSON hợp lệ cho prompt LLM (xem _trim_json).
    features_summary = _trim_json(res_a.get("features", []), 8000)
    arch_summary = _trim_json(res_a.get("architecture", {}), 4000)

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
