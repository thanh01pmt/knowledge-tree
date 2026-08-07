#!/usr/bin/env python3
"""
STEP 5.5: JIT generation — generate ULO/CIO/SIO for concepts without coverage.

When a concept resolves (STEP 3) but has no CIO/SIO in the Master Tree or
existing projects (Gap D), this script generates the missing LO chain:

  ULO (UNIVERSAL)      — from concept description (tech-agnostic)
  CIO (CONCEPTUAL_IMPL) — from concept description + Bloom level
  SIO (SPECIFIC_IMPL)   — from project keywords + concept (tech-specific)

Generated LOs go to quarantine for Agent-as-Judge review before staging.

Reads:
- resolved_concepts.json (from STEP 3)
- matched_cios.json (from STEP 4)
- resolved_sios.json (from STEP 5)
- keywords.json (from STEP 1-2, for SIO context)

Outputs:
- jit_los.json: {generated: [ULO/CIO/SIO entries], concepts_covered: [...]}
"""

import json
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

# LLM support (optional — falls back to template if unavailable)
REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
SKILL_LLM_PATH = REPO_ROOT / ".agents" / "skills" / "keyword-extractor" / "scripts"
if str(SKILL_LLM_PATH) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM_PATH))

import lo_quality

try:
    from llm_call import llm_chat_json, LLMCallError, get_llm_client, resolve_provider
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False


def _get_llm():
    """Return (client, model) or (None, None) if LLM unavailable.

    Provider qua llm_call.resolve_provider():
    - LLM_PROVIDER=deepseek      → https://api.deepseek.com, deepseek-v4-flash
    - LLM_PROVIDER=ollama-cloud  → https://api.ollama.ai/v1, deepseek-v4-flash:cloud
    - LLM_PROVIDER=ollama        → http://127.0.0.1:11434/v1 (local)
    - Không set LLM_PROVIDER     → auto (cloud nếu có SAAS_OLLAMA_CLOUD_API_KEY)
    """
    if not _LLM_AVAILABLE:
        return None, None
    try:
        client, provider, model = get_llm_client()
        if client is None:
            return None, None
        if os.environ.get("VERBOSE_LLM"):
            print(f"  [LLM] provider={provider} model={model}", file=sys.stderr)
        return client, model
    except Exception:
        return None, None


def _llm_generate(system: str, user: str) -> str:
    """Call LLM, return text or empty string on failure."""
    client, model = _get_llm()
    if not client:
        return ""
    try:
        result = llm_chat_json(client, model, system, user, temperature=0.4)
        return result.get("description", "")
    except Exception:
        return ""


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_covered_concepts(matched_cios: dict, resolved_sios: dict) -> set:
    """Concepts co SIO THAT — chi concept nay duoc coi la 'covered'.

    GENERATE-first: resolved_sios luon GENERATE (0 sios). Concept co CIO matched
    nhung khong SIO → KHONG covered → JIT sinh du ULO+CIO+SIO. Truoc day cover
    tu matched_cios (CIO) lam HTTP_PROTOCOL/EXCEPTION_HANDLING mat SIO.
    """
    covered = set()
    # Chi concept co SIO thuc (REUSE sios) moi covered
    for group in resolved_sios.get('resolved_sios', []):
        if group.get('action') == 'REUSE' and group.get('sios'):
            covered.add(group.get('concept_code', ''))
        elif group.get('action') in ('ADAPT', 'TEMPLATE') and group.get('source_sio'):
            covered.add(group.get('concept_code', ''))
    return {c for c in covered if c}


def collect_resolved_concepts(resolved_concepts: dict) -> Dict[str, dict]:
    """Map concept_code -> concept info từ resolved + proposed concepts.

    - resolved: concept đã có trong Master Tree (match embedding)
    - proposed: concept CHƯA có — cần JIT generation nội bộ (cuối dự án mới sync ngược)
    """
    # Nguồn keyword là KIẾN THỨC THẬT (dùng làm keyword thực hành):
    #   import (Foundation, SwiftUI), property_wrapper (@State),
    #   error_handling (throws, try!), docstring/readme/config, escalated
    # Bỏ TÊN DO DEV ĐẶT (function_signature: loop/getState — không phải keyword
    # ngôn ngữ; type_declaration: HTTPBulbService — tên class tự viết).
    KEYWORD_SOURCES = {'import', 'property_wrapper', 'error_handling', 'docstring', 'readme', 'config', 'escalated', 'framework_usage'}

    concepts = {}
    # Resolved concepts (đã match Master Tree)
    # Keyword nguồn dev-đặt (function_signature: loop/getState, type_declaration:
    # HTTPBulbService) KHÔNG phải keyword thực hành — xóa để infer từ SIO name
    for item in resolved_concepts.get('resolved', []):
        source = item.get('source', '')
        kw = item.get('keyword', '')
        if source and source not in KEYWORD_SOURCES:
            kw = ''  # giữ concept, bỏ keyword sai nguồn
        for code in item.get('concept_codes', []):
            if code:
                # Lấy description từ match ĐÚNG code (không lấy matches[0] vì có
                # thể là embedding sai nghĩa) — tránh fallback template generic
                desc = ''
                for m in item.get('matches', []):
                    if m.get('code') == code:
                        desc = m.get('description', '')
                        break
                concepts[code] = {
                    'keyword': kw,
                    'matches': item.get('matches', []),
                    'is_proposed': False,
                    'description': desc,
                }
    # Proposed concepts (chưa có trong Master Tree — JIT nội bộ)
    # Chỉ JIT cho keywords là KIẾN THỨC thật — cùng KEYWORD_SOURCES
    for item in resolved_concepts.get('proposed', []):
        source = item.get('source', '')
        if source and source not in KEYWORD_SOURCES:
            continue
        keyword = item.get('keyword', '') or item.get('proposed_name', '') or item.get('name', '')
        if not keyword:
            continue
        # Nếu có concept_code (từ STEP 3.5 escalated) — dùng trực tiếp (concept trung tính)
        code = item.get('concept_code', '')
        if not code:
            # Fallback: tạo concept_code tạm từ keyword (UPPER_SNAKE)
            code = re.sub(r'[^A-Z0-9]+', '_', keyword.upper()).strip('_')
        if not code:
            continue
        concepts[code] = {
            'keyword': keyword,
            'matches': [],
            'is_proposed': True,
            'proposed_name': item.get('proposed_name', '') or item.get('name', '') or keyword,
            'description': item.get('reason', '') or item.get('description', ''),
        }
    return concepts


def get_concept_description(concept_code: str, reuse_inventory: dict) -> str:
    """Get concept description from master tree (hoặc fallback từ proposed)."""
    # Nếu concept là proposed (từ collect_resolved_concepts), dùng keyword làm description
    # (description thật sẽ do LLM sinh trong generate_ulo/cio/sio)
    concepts = reuse_inventory.get('master_tree', {}).get('concepts', {})
    data = concepts.get(concept_code, {})
    return data.get('description', '')


def get_concept_name(concept_code: str, reuse_inventory: dict) -> str:
    """Get the natural-language concept name from master tree.

    e.g. GENERATIVE_CONTENT_APPLICATION -> 'Generative Content Application'
    """
    # FOR_LOOP hiển thị là "Definite Iteration" (lặp với số lần xác định) —
    # khái niệm chuẩn hơn "Loop"; for/while/forEach là keyword/SIO cụ thể
    if concept_code == 'FOR_LOOP':
        return 'Definite Iteration'
    concepts = reuse_inventory.get('master_tree', {}).get('concepts', {})
    data = concepts.get(concept_code, {})
    name = data.get('name', '')
    if name:
        return name
    # Fallback: humanize the code
    return concept_code.replace('_', ' ').title()


def get_project_context(keywords_data: dict) -> str:
    """Build a natural-language project description from docstrings/README.

    Prefers high-signal sources (docstring, readme_description) which carry
    real domain intent, instead of raw code identifiers.
    """
    for kw in keywords_data.get('keywords', []):
        if kw.get('source') in ('readme_description', 'docstring'):
            text = kw.get('keyword', '').strip()
            if len(text) > 15:
                return text
    return ''


def get_keyword_platforms(keywords_data: dict) -> dict:
    """Map keyword -> platform (app/esp32) tu keywords.json.

    Multi-codebase project (Swift app + ESP32 firmware): keyword sinh tu file
    nao thi platform do. SIO se sinh dung platform (Swift vs Arduino).
    """
    kw_to_platform = {}
    for kw in keywords_data.get('keywords', []):
        k = kw.get('keyword', '')
        if k:
            kw_to_platform[k] = kw.get('platform', 'app')
    return kw_to_platform


def generate_ulo(concept_code: str, description: str, concept_name: str = '') -> dict:
    """Generate ULO (UNIVERSAL tier) from concept description.

    Uses LLM to write a natural, context-aware description; falls back to
    lo_quality.build_lo_desc if LLM unavailable.
    """
    name_hint = concept_name or concept_code
    # Try LLM first for a natural description
    llm_desc = _llm_generate(
        "Bạn là chuyên gia sư phạm. Viết 1 câu mô tả ULO (Universal Learning Objective) "
        "bắt đầu bằng 'Người học có khả năng hiểu' cho khái niệm sau. "
        f"Dùng đúng tên khái niệm '{name_hint}' (không dùng mã code, không dùng tên khác). "
        "QUAN TRỌNG: dùng tên khái niệm tự nhiên bằng tiếng Việt, KHÔNG chèn mã code "
        "(tên viết hoa như GENERATIVE_CONTENT_APPLICATION) vào câu văn. "
        "CẤM: cấu trúc 'Tên khái niệm: Mô tả' (dấu hai chấm sau tên) và mọi sự lặp từ 'hiểu' hai lần — "
        "viết một câu liền mạch, cụ thể vào vai trò/đặc điểm của khái niệm trong dự án, không chung chung "
        "(ví dụ nói rõ nó giải quyết vấn đề gì, không phải 'và vai trò của nó'). "
        "Giữ nguyên thuật ngữ tiếng Anh chuyên ngành (không dịch sang tiếng Việt) nếu là khái niệm kỹ thuật quốc tế, ví dụ như tên gốc của khái niệm đang xét. "
        "Trả về JSON: {\"description\": \"...\"}",
        f"Khái niệm: {name_hint}. Mô tả: {description}"
    )
    if llm_desc:
        llm_desc = lo_quality.clean_llm_description(llm_desc, name_hint)

    if llm_desc:
        final_desc = llm_desc
        needs_review = False
    else:
        final_desc, needs_review = lo_quality.build_lo_desc(
            'ULO', concept_code, name_hint, description
        )

    return {
        'code': f"ULO-{concept_code}-01",
        'name': f"Understand {concept_code}",
        'description': final_desc,
        'needs_review': needs_review,
        'lo_type': 'UNIVERSAL',
        'parent_lo_code': '',
        'concept_codes': [concept_code],
        'bloom_level': 'UNDERSTAND',
        'knowledge_dimension': 'CONCEPTUAL',
        'assessment_approach': 'concept-check',
    }


def generate_cio(concept_code: str, description: str) -> dict:
    """Generate CIO (CONCEPTUAL_IMPL tier) from concept description.

    Uses LLM for a natural, tech-agnostic description; falls back to lo_quality.build_lo_desc.
    """
    llm_desc = _llm_generate(
        "Bạn là chuyên gia sư phạm. Viết 1 câu mô tả CIO (Conceptual Implementation Objective) "
        "bắt đầu bằng 'Người học có khả năng thiết kế' cho khái niệm sau, "
        "KHÔNG nhắc tên công nghệ cụ thể, KHÔNG chèn mã code vào câu văn. "
        "Giữ nguyên thuật ngữ tiếng Anh chuyên ngành (không dịch sang tiếng Việt) nếu là khái niệm kỹ thuật quốc tế, ví dụ như tên gốc của khái niệm đang xét. "
        "Trả về JSON: {\"description\": \"...\"}",
        f"Khái niệm: {concept_code}. Mô tả: {description}"
    )
    if llm_desc:
        llm_desc = lo_quality.clean_llm_description(llm_desc, concept_code)

    if llm_desc:
        final_desc = llm_desc
        needs_review = False
    else:
        final_desc, needs_review = lo_quality.build_lo_desc(
            'CIO', concept_code, concept_code, description
        )

    return {
        'code': f"CIO-{concept_code}-01",
        'name': f"Apply {concept_code} Concepts",
        'description': final_desc,
        'needs_review': needs_review,
        'lo_type': 'CONCEPTUAL_IMPL',
        'parent_lo_code': f"ULO-{concept_code}-01",
        'concept_codes': [concept_code],
        'bloom_level': 'APPLY',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-lab',
    }


def generate_sio(concept_code: str, concept_name: str, description: str,
                 project_context: str, target_tech: str, keyword: str = '',
                 platform: str = 'app') -> dict:
    """Generate SIO (SPECIFIC_IMPL tier) from concept + project context.

    Uses LLM to write a natural description grounded in the project's real
    domain intent (docstring/README) + concept keyword (thực hành cụ thể).
    SIO name dùng TÊN THỰC HÀNH (For Loop / @State...) — không dùng tên khái niệm
    trừu tượng (Definite Iteration) làm tên implement.
    platform: app (Swift) | esp32 (Arduino) — phân biệt codebase thật.
    """
    # Platform: esp32 → code prefix 'ESP32', hiển thị 'ESP32/Arduino'
    platform_label = 'ESP32/Arduino' if platform == 'esp32' else target_tech
    code_prefix = 'ESP32' if platform == 'esp32' else target_tech
    # Tên thực hành: FOR_LOOP → 'For Loop' (không phải 'Definite Iteration')
    if concept_code == 'FOR_LOOP':
        concept_name = 'For Loop'
        if not keyword:
            keyword = 'for'
    name_hint = concept_name or concept_code
    kw_hint = (f"Khái niệm này trong dự án xuất hiện qua keyword/tên gọi: '{keyword}' "
               f"thuộc codebase {platform_label}. " if keyword
               else f"Khái niệm này thuộc codebase {platform_label}. ")
    llm_desc = _llm_generate(
        f"Bạn là chuyên gia sư phạm. Viết 1 câu mô tả SIO (Specific Implementation Objective) "
        f"bắt đầu bằng 'Người học có khả năng triển khai' cho khái niệm '{concept_name}' "
        f"trong ngôn ngữ {target_tech}, gắn với mục đích dự án: '{project_context}'. "
        f"{kw_hint}"
        f"QUAN TRỌNG: mô tả phải GẮN VỚI THỰC HÀNH CỤ THỂ trong dự án — nêu rõ keyword/tên "
        f"API/framework người học sẽ dùng (như tên framework, property wrapper, từ khóa ngôn ngữ), "
        f"KHÔNG viết lý thuyết trừu tượng chung chung. "
        f"QUAN TRỌNG: dùng tên khái niệm và mô tả tự nhiên bằng tiếng Việt, "
        f"KHÔNG chèn tên biến/class/function do lập trình viên tự đặt (code identifiers) vào câu văn. "
        f"Giữ nguyên thuật ngữ tiếng Anh chuyên ngành quốc tế (không dịch sang tiếng Việt) "
        f"nếu là khái niệm kỹ thuật; viết tự nhiên theo đúng tên khái niệm '{concept_name}'. "
        f"Trả về JSON: {{\"description\": \"...\"}}",
        f"Khái niệm: {concept_name}. Mô tả khái niệm: {description}"
    )
    if llm_desc:
        llm_desc = lo_quality.clean_llm_description(llm_desc, name_hint)

    if llm_desc:
        final_desc = llm_desc
        needs_review = False
    else:
        final_desc, needs_review = lo_quality.build_lo_desc(
            'SIO', concept_code, name_hint, description, keyword=keyword, platform=platform
        )

    return {
        'code': f"SIO-{code_prefix}-{concept_code}-01",
        'name': f"{platform_label}: Implement {concept_name}",
        'description': final_desc,
        'needs_review': needs_review,
        'lo_type': 'SPECIFIC_IMPL',
        'parent_lo_code': f"CIO-{concept_code}-01",
        'concept_codes': [concept_code],
        'keyword': keyword,  # keyword thực hành của concept trong project
        'platform': platform,  # app (Swift) | esp32 (Arduino)
        'bloom_level': 'CREATE',  # SIO = thực hành hoàn thiện (Phase 3, vertical slicing)
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-review',
    }

def _build_lo_triplet(concept_code: str, name_hint: str, description: str,
                      keyword: str, platform: str, code_prefix: str,
                      raw_ulo: str, raw_cio: str, raw_sio: str) -> List[dict]:
    """Build [ulo, cio, sio] dicts from raw LLM strings; per-field fallback
    via lo_quality.build_lo_desc when a field is missing/empty."""
    # ULO
    if raw_ulo:
        cleaned_ulo = lo_quality.clean_llm_description(str(raw_ulo), name_hint)
        if cleaned_ulo:
            ulo_desc, ulo_needs_review = cleaned_ulo, False
        else:
            ulo_desc, ulo_needs_review = lo_quality.build_lo_desc('ULO', concept_code, name_hint, description)
    else:
        ulo_desc, ulo_needs_review = lo_quality.build_lo_desc('ULO', concept_code, name_hint, description)

    # CIO
    if raw_cio:
        cleaned_cio = lo_quality.clean_llm_description(str(raw_cio), name_hint)
        if cleaned_cio:
            cio_desc, cio_needs_review = cleaned_cio, False
        else:
            cio_desc, cio_needs_review = lo_quality.build_lo_desc('CIO', concept_code, name_hint, description)
    else:
        cio_desc, cio_needs_review = lo_quality.build_lo_desc('CIO', concept_code, name_hint, description)

    # SIO
    if raw_sio:
        cleaned_sio = lo_quality.clean_llm_description(str(raw_sio), name_hint)
        if cleaned_sio:
            sio_desc, sio_needs_review = cleaned_sio, False
        else:
            sio_desc, sio_needs_review = lo_quality.build_lo_desc(
                'SIO', concept_code, name_hint, description, keyword=keyword, platform=platform
            )
    else:
        sio_desc, sio_needs_review = lo_quality.build_lo_desc(
            'SIO', concept_code, name_hint, description, keyword=keyword, platform=platform
        )

    platform_label = 'ESP32/Arduino' if platform == 'esp32' else code_prefix
    ulo = {
        'code': f"ULO-{concept_code}-01",
        'name': f"Understand {concept_code}",
        'description': ulo_desc,
        'needs_review': ulo_needs_review,
        'lo_type': 'UNIVERSAL',
        'parent_lo_code': '',
        'concept_codes': [concept_code],
        'bloom_level': 'UNDERSTAND',
        'knowledge_dimension': 'CONCEPTUAL',
        'assessment_approach': 'concept-check',
    }

    cio = {
        'code': f"CIO-{concept_code}-01",
        'name': f"Apply {concept_code} Concepts",
        'description': cio_desc,
        'needs_review': cio_needs_review,
        'lo_type': 'CONCEPTUAL_IMPL',
        'parent_lo_code': f"ULO-{concept_code}-01",
        'concept_codes': [concept_code],
        'bloom_level': 'APPLY',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-lab',
    }

    sio = {
        'code': f"SIO-{code_prefix}-{concept_code}-01",
        'name': f"{platform_label}: Implement {name_hint}",
        'description': sio_desc,
        'needs_review': sio_needs_review,
        'lo_type': 'SPECIFIC_IMPL',
        'parent_lo_code': f"CIO-{concept_code}-01",
        'concept_codes': [concept_code],
        'keyword': keyword,
        'platform': platform,
        'bloom_level': 'CREATE',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-review',
    }

    return [ulo, cio, sio]
def generate_concept_los(concept_code: str, concept_name: str, description: str,
                         project_context: str, target_tech: str, keyword: str = '',
                         platform: str = 'app') -> List[dict]:
    """Generate ULO, CIO, and SIO in a single LLM call for a concept.

    Returns [ulo_dict, cio_dict, sio_dict]. Falls back per-field via lo_quality.build_lo_desc.
    """
    if concept_code == 'FOR_LOOP':
        concept_name = 'For Loop'
        if not keyword:
            keyword = 'for'
    name_hint = concept_name or concept_code
    platform_label = 'ESP32/Arduino' if platform == 'esp32' else target_tech
    code_prefix = 'ESP32' if platform == 'esp32' else target_tech

    kw_hint = (f"Khái niệm này trong dự án xuất hiện qua keyword/tên gọi: '{keyword}' "
               f"thuộc codebase {platform_label}." if keyword
               else f"Khái niệm này thuộc codebase {platform_label}.")

    system_prompt = (
        "Bạn là chuyên gia sư phạm. Hãy viết 3 câu mô tả mục tiêu học tập (LO) cho 1 khái niệm kỹ thuật theo 3 tầng (ULO, CIO, SIO):\n"
        "- ULO (Universal Learning Objective): bắt đầu bằng 'Người học có khả năng hiểu', nêu rõ đặc điểm/bản chất của khái niệm trong ngữ cảnh dự án.\n"
        "- CIO (Conceptual Implementation Objective): bắt đầu bằng 'Người học có khả năng thiết kế', mô tả giải pháp kiến trúc/mô hình (KHÔNG nhắc tên công nghệ cụ thể).\n"
        "- SIO (Specific Implementation Objective): bắt đầu bằng 'Người học có khả năng triển khai', mô tả thực hành cụ thể gắn với keyword, platform và mục đích dự án.\n"
        "QUAN TRỌNG:\n"
        "1. CẤM cấu trúc 'Tên: Mô tả' (dấu hai chấm sau tên) ở tất cả các tầng.\n"
        "2. CẤM lặp từ 'hiểu' hai lần trong câu ULO.\n"
        "3. CẤM dùng các cụm từ template chung chung như 'và vai trò của nó', 'và cách vận dụng nó'.\n"
        "4. Dùng đúng tên khái niệm tự nhiên bằng tiếng Việt/tiếng Anh chuyên ngành, KHÔNG chèn mã code/identifier biến vào câu văn.\n"
        "Trả về JSON dạng: {\"ulo\": \"...\", \"cio\": \"...\", \"sio\": \"...\"}"
    )

    user_prompt = (
        f"Khái niệm: {name_hint}\n"
        f"Mô tả khái niệm: {description}\n"
        f"Dự án / Ngữ cảnh: {project_context}\n"
        f"Target Tech: {target_tech}\n"
        f"Codebase / Platform: {platform_label}\n"
        f"{kw_hint}"
    )

    llm_raw = _llm_generate(system_prompt, user_prompt)
    parsed = None
    if llm_raw:
        raw_text = llm_raw.strip()
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()
        try:
            parsed = json.loads(raw_text)
        except Exception:
            parsed = None

    raw_ulo = parsed.get('ulo', '') if isinstance(parsed, dict) and parsed.get('ulo') else ''
    raw_cio = parsed.get('cio', '') if isinstance(parsed, dict) and parsed.get('cio') else ''
    raw_sio = parsed.get('sio', '') if isinstance(parsed, dict) and parsed.get('sio') else ''

    return _build_lo_triplet(
        concept_code, name_hint, description, keyword, platform, code_prefix,
        raw_ulo, raw_cio, raw_sio
    )


def generate_concept_los_batch(concepts_info: List[dict], project_context: str,
                              target_tech: str, batch_size: int = 10) -> List[dict]:
    """Generate ULO+CIO+SIO for multiple concepts in ONE LLM call.

    concepts_info: [{concept_code, concept_name, description, keyword, platform}]
    Returns flat list of all LO dicts across all concepts.
    Falls back per-concept via generate_concept_los if batch parse fails.
    """
    if len(concepts_info) <= 1:
        results = []
        for info in concepts_info:
            results.extend(generate_concept_los(
                info['concept_code'], info['concept_name'], info['description'],
                project_context, target_tech,
                keyword=info.get('keyword', ''), platform=info.get('platform', 'app')
            ))
        return results

    system_prompt = (
        "Bạn là chuyên gia sư phạm. Viết BẰNG TIẾNG VIỆT (giữ nguyên thuật ngữ kỹ thuật tiếng Anh). Sinh 3 câu mô tả mục tiêu học tập cho MỖI concept "
        "trong danh sách, theo 3 tầng:\n"
        "- ULO: bắt đầu bằng 'Người học có khả năng hiểu', nêu đặc điểm/bản chất khái niệm.\n"
        "- CIO: bắt đầu bằng 'Người học có khả năng thiết kế', mô tả giải pháp mô hình.\n"
        "- SIO: bắt đầu bằng 'Người học có khả năng triển khai', gắn keyword + platform cụ thể.\n"
        "QUAN TRỌNG:\n"
        "1. CẤM cấu trúc 'Tên: Mô tả'.\n"
        "2. CẤM lặp từ 'hiểu' hai lần trong ULO.\n"
        "3. CẤM template chung chung ('và vai trò của nó', 'và cách vận dụng nó').\n"
        "4. Giữ thuật ngữ tiếng Anh chuyên ngành, KHÔNG chèn identifier/mã code.\n"
        "Trả JSON: {\"results\": {\"<CONCEPT_CODE>\": {\"ulo\": \"...\", \"cio\": \"...\", \"sio\": \"...\"}}}"
    )

    user_items = []
    for info in concepts_info:
        code = info['concept_code']
        name = info['concept_name'] or code
        if code == 'FOR_LOOP':
            name = 'For Loop'
        platform_label = 'ESP32/Arduino' if info.get('platform') == 'esp32' else target_tech
        kw = info.get('keyword', '')
        kw_part = f" keyword '{kw}'," if kw else ''
        user_items.append(
            f"- {code}: {name} — {info.get('description', '')[:100]}{kw_part} platform={platform_label}"
        )

    user_prompt = (
        f"Dự án: {project_context[:200]}\n"
        f"Target tech: {target_tech}\n\n"
        "Concepts:\n" + "\n".join(user_items)
    )

    llm_raw = _llm_generate(system_prompt, user_prompt)
    parsed = None
    if llm_raw:
        raw_text = llm_raw.strip()
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()
        try:
            parsed = json.loads(raw_text)
        except Exception:
            parsed = None

    results_data = parsed.get('results', {}) if isinstance(parsed, dict) else {}

    all_los = []
    for info in concepts_info:
        code = info['concept_code']
        name = info['concept_name'] or code
        if code == 'FOR_LOOP':
            name = 'For Loop'
        platform = info.get('platform', 'app')
        keyword = info.get('keyword', '')
        code_prefix = 'ESP32' if platform == 'esp32' else target_tech

        lo_data = results_data.get(code, {}) if isinstance(results_data, dict) else {}
        raw_ulo = lo_data.get('ulo', '') if isinstance(lo_data, dict) else ''
        raw_cio = lo_data.get('cio', '') if isinstance(lo_data, dict) else ''
        raw_sio = lo_data.get('sio', '') if isinstance(lo_data, dict) else ''

        triplet = _build_lo_triplet(
            code, name, info.get('description', ''), keyword, platform, code_prefix,
            raw_ulo, raw_cio, raw_sio
        )
        all_los.extend(triplet)

    return all_los


def main():
    parser = argparse.ArgumentParser(description='STEP 5.5: JIT generate LOs for uncovered concepts')
    parser.add_argument('--resolved-concepts', type=Path, required=True)
    parser.add_argument('--escalated-concepts', type=Path, default=None,
                        help='Optional: escalated_concepts.json từ STEP 3.5 (concept trung tính)')
    parser.add_argument('--matched-cios', type=Path, required=True)
    parser.add_argument('--resolved-sios', type=Path, required=True)
    parser.add_argument('--keywords', type=Path, required=True)
    parser.add_argument('--reuse-inventory', type=Path, required=True)
    parser.add_argument('--target-tech', type=str, default='SWIFT')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    resolved_concepts = load_json(args.resolved_concepts)
    # Nếu có escalated_concepts (STEP 3.5) — THAY proposed raw bằng concept trung tính
    if args.escalated_concepts and args.escalated_concepts.exists():
        escalated = load_json(args.escalated_concepts)
        # Giữ escalated concepts: status=new (Gap D) VÀ status=matched (concept
        # hợp lệ đã match Master Tree — có keyword thật: SwiftUI, ArduinoJson.h...)
        # Trước đây chỉ giữ 'new' → 5 concepts matched bị mất (FRONTEND_FRAMEWORKS,
        # JSON_SERIALIZATION, DIGITAL_ANALOG_IO, IOT_MESSAGING_PROTOCOLS, MEDIUM_TYPES)
        escalated_proposed = []
        for item in escalated.get('escalated', []):
            code = item.get('concept_code', '')
            if code and item.get('status') in ('new', 'matched'):
                escalated_proposed.append({
                    'keyword': item.get('keyword', ''),
                    'proposed_name': item.get('concept_name', code),
                    'concept_code': code,
                    'source': 'escalated',
                    'reason': item.get('reason', ''),
                })
        resolved_concepts['proposed'] = escalated_proposed
        print(f"[*] Dùng escalated concepts từ STEP 3.5 ({len(escalated_proposed)} concepts: new + matched)")
    matched_cios = load_json(args.matched_cios)
    resolved_sios = load_json(args.resolved_sios)
    keywords_data = load_json(args.keywords)
    inventory = load_json(args.reuse_inventory)

    # Concepts already covered
    covered = collect_covered_concepts(matched_cios, resolved_sios)
    # Concepts resolved from STEP 3
    resolved = collect_resolved_concepts(resolved_concepts)

    # TEMPLATE DETECTION: concepts covered nhưng ULO/CIO là template máy móc
    # → đưa vào JIT để regenerate (LLM sinh desc tự nhiên)
    for code in list(covered):
        # Kiểm tra ULO template (derived_ulos)
        ulo_template = False
        for lo in matched_cios.get('derived_ulos', []):
            if lo.get('concept_codes') and code in lo.get('concept_codes', []):
                desc = lo.get('description', '')
                if lo_quality.is_template_description(desc, layer='ULO'):
                    ulo_template = True
                break
        # Kiểm tra CIO template (matched_cios) — data Master Tree thối (gen_real_los.py)
        cio_template = False
        for match in matched_cios.get('matched_cios', []):
            if match.get('concept_code') == code:
                cio_desc = match.get('cio_description', '')
                if lo_quality.is_template_description(cio_desc, layer='CIO'):
                    cio_template = True
                    break
        if ulo_template or cio_template:
            covered.discard(code)
            # Thêm vào resolved để JIT regenerate
            if code not in resolved:
                resolved[code] = {
                    'keyword': code,
                    'matches': [],
                    'is_proposed': True,
                    'proposed_name': code.replace('_', ' ').title(),
                }
            why = 'ULO' if ulo_template else 'CIO'
            print(f"  → Template detected ({why}): {code} — regenerate qua JIT")

    # Concepts needing JIT generation
    uncovered = {c: info for c, info in resolved.items() if c not in covered}
    print(f"[*] Resolved concepts: {len(resolved)} | Covered: {len(covered)} | Uncovered: {len(uncovered)}")

    if not uncovered:
        print("[✓] All resolved concepts have coverage — no JIT generation needed")
        output = {'generated': [], 'concepts_covered': sorted(covered)}
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        return 0

    # Build natural-language project context (docstring/README, not code ids)
    project_context = get_project_context(keywords_data)
    kw_platforms = get_keyword_platforms(keywords_data)

    # Build concepts_info with description/platform resolution
    concepts_info = []
    for concept_code, info in sorted(uncovered.items()):
        description = info.get('description') or get_concept_description(concept_code, inventory)
        concept_name = get_concept_name(concept_code, inventory)
        kw = info.get('keyword', '')
        platform = kw_platforms.get(kw, '')
        if not platform and concept_code == 'FOR_LOOP':
            platform = 'esp32'
        if not platform:
            platform = 'app'
        concepts_info.append({
            'concept_code': concept_code,
            'concept_name': concept_name,
            'description': description,
            'keyword': kw,
            'platform': platform,
        })

    # Batch generation: 10 concepts per LLM call (tested: ~3.1s/concept, 3.9k output)
    BATCH_SIZE = 10
    generated = []
    n_batches = (len(concepts_info) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(n_batches):
        chunk = concepts_info[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        names = ", ".join(c['concept_name'] for c in chunk)
        print(f"  -> Batch {i+1}/{n_batches}: {len(chunk)} concepts ({names[:80]}...)")
        batch_los = generate_concept_los_batch(
            chunk, project_context, args.target_tech, batch_size=BATCH_SIZE
        )
        generated.extend(batch_los)

    print(f"[*] Generated {len(generated)} LOs ({len(uncovered)} concepts × 3 tiers)")

    output = {
        'generated': generated,
        'concepts_covered': sorted(covered),
        'concepts_generated': sorted(uncovered.keys()),
        'summary': {
            'generated_count': len(generated),
            'concepts_generated': len(uncovered),
            'target_tech': args.target_tech,
        }
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {args.output}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
