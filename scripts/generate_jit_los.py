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
SKILL_LLM_PATH = REPO_ROOT / ".agents" / "skills" / "keyword-extractor" / "scripts"
if str(SKILL_LLM_PATH) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM_PATH))

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
    """Concepts that already have CIO/SIO coverage."""
    covered = set()
    for match in matched_cios.get('matched_cios', []):
        covered.add(match.get('concept_code', ''))
    for group in resolved_sios.get('resolved_sios', []):
        covered.add(group.get('concept_code', ''))
    return {c for c in covered if c}


def collect_resolved_concepts(resolved_concepts: dict) -> Dict[str, dict]:
    """Map concept_code -> concept info từ resolved + proposed concepts.

    - resolved: concept đã có trong Master Tree (match embedding)
    - proposed: concept CHƯA có — cần JIT generation nội bộ (cuối dự án mới sync ngược)
    """
    concepts = {}
    # Resolved concepts (đã match Master Tree)
    for item in resolved_concepts.get('resolved', []):
        for code in item.get('concept_codes', []):
            if code:
                concepts[code] = {
                    'keyword': item.get('keyword', ''),
                    'matches': item.get('matches', []),
                    'is_proposed': False,
                }
    # Proposed concepts (chưa có trong Master Tree — JIT nội bộ)
    # Chỉ JIT cho keywords là KIẾN THỨC thật (import, property_wrapper, error_handling, docstring)
    # Bỏ tên class/function tự đặt (type_declaration, function_signature) — không phải concept
    JIT_SOURCES = {'import', 'property_wrapper', 'error_handling', 'docstring', 'readme', 'config', 'escalated'}
    for item in resolved_concepts.get('proposed', []):
        source = item.get('source', '')
        if source and source not in JIT_SOURCES:
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


def generate_ulo(concept_code: str, description: str) -> dict:
    """Generate ULO (UNIVERSAL tier) from concept description.

    Uses LLM to write a natural, context-aware description; falls back to
    the concept description (or template) if LLM unavailable.
    """
    # Try LLM first for a natural description
    llm_desc = _llm_generate(
        "Bạn là chuyên gia sư phạm. Viết 1 câu mô tả ULO (Universal Learning Objective) "
        "bắt đầu bằng 'Người học có khả năng hiểu' cho khái niệm sau. "
        "QUAN TRỌNG: dùng tên khái niệm tự nhiên bằng tiếng Việt, KHÔNG chèn mã code "
        "(tên viết hoa như GENERATIVE_CONTENT_APPLICATION) vào câu văn. "
        "Giữ nguyên thuật ngữ tiếng Anh như 'Generative AI', 'generative content' (không dịch sang tiếng Việt). "
        "Trả về JSON: {\"description\": \"...\"}",
        f"Khái niệm: {concept_code}. Mô tả: {description}"
    )
    if llm_desc:
        final_desc = llm_desc
    elif description:
        final_desc = f"Người học có khả năng hiểu: {description}"
    else:
        final_desc = (
            f"Người học có khả năng hiểu nguyên lý phổ quát của {concept_code} "
            f"và vai trò của nó trong thiết kế giải pháp phần mềm."
        )

    return {
        'code': f"ULO-{concept_code}-01",
        'name': f"Understand {concept_code}",
        'description': final_desc,
        'lo_type': 'UNIVERSAL',
        'parent_lo_code': '',
        'concept_codes': [concept_code],
        'bloom_level': 'UNDERSTAND',
        'knowledge_dimension': 'CONCEPTUAL',
        'assessment_approach': 'concept-check',
    }


def generate_cio(concept_code: str, description: str) -> dict:
    """Generate CIO (CONCEPTUAL_IMPL tier) from concept description.

    Uses LLM for a natural, tech-agnostic description; falls back to template.
    """
    llm_desc = _llm_generate(
        "Bạn là chuyên gia sư phạm. Viết 1 câu mô tả CIO (Conceptual Implementation Objective) "
        "bắt đầu bằng 'Người học có khả năng thiết kế' cho khái niệm sau, "
        "KHÔNG nhắc tên công nghệ cụ thể, KHÔNG chèn mã code vào câu văn. "
        "Giữ nguyên thuật ngữ tiếng Anh như 'Generative AI', 'generative content' (không dịch sang tiếng Việt). "
        "Trả về JSON: {\"description\": \"...\"}",
        f"Khái niệm: {concept_code}. Mô tả: {description}"
    )
    if llm_desc:
        final_desc = llm_desc
    elif description:
        final_desc = f"Người học có khả năng thiết kế quy trình xử lý cho {concept_code}: {description[:200]}"
    else:
        final_desc = (
            f"Người học có khả năng thiết kế quy trình xử lý cho {concept_code}: "
            f"phân tích yêu cầu, lựa chọn phương pháp, và đánh giá kết quả."
        )

    return {
        'code': f"CIO-{concept_code}-01",
        'name': f"Apply {concept_code} Concepts",
        'description': final_desc,
        'lo_type': 'CONCEPTUAL_IMPL',
        'parent_lo_code': f"ULO-{concept_code}-01",
        'concept_codes': [concept_code],
        'bloom_level': 'APPLY',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-lab',
    }


def generate_sio(concept_code: str, concept_name: str, description: str,
                 project_context: str, target_tech: str) -> dict:
    """Generate SIO (SPECIFIC_IMPL tier) from concept + project context.

    Uses LLM to write a natural description grounded in the project's real
    domain intent (docstring/README), NOT raw code identifiers.
    """
    llm_desc = _llm_generate(
        f"Bạn là chuyên gia sư phạm. Viết 1 câu mô tả SIO (Specific Implementation Objective) "
        f"bắt đầu bằng 'Người học có khả năng triển khai' cho khái niệm '{concept_name}' "
        f"trong ngôn ngữ {target_tech}, gắn với mục đích dự án: '{project_context}'. "
        f"QUAN TRỌNG: dùng tên khái niệm và mô tả tự nhiên bằng tiếng Việt, "
        f"KHÔNG chèn tên biến/class/function (code identifiers) vào câu văn. "
        f"Giữ nguyên thuật ngữ tiếng Anh như 'Generative AI', 'generative content' "
        f"(không dịch sang tiếng Việt, không dùng 'sinh học'). "
        f"Trả về JSON: {{\"description\": \"...\"}}",
        f"Khái niệm: {concept_name}. Mô tả khái niệm: {description}"
    )
    if llm_desc:
        final_desc = llm_desc
    else:
        final_desc = (
            f"Người học có khả năng triển khai {concept_name} trong {target_tech} "
            f"phục vụ {project_context if project_context else 'mục đích của dự án'}: "
            f"{description[:150] if description else 'viết code, xử lý lỗi, và kiểm thử.'}"
        )

    return {
        'code': f"SIO-{target_tech}-{concept_code}-01",
        'name': f"{target_tech}: Implement {concept_name}",
        'description': final_desc,
        'lo_type': 'SPECIFIC_IMPL',
        'parent_lo_code': f"CIO-{concept_code}-01",
        'concept_codes': [concept_code],
        'bloom_level': 'APPLY',
        'knowledge_dimension': 'PROCEDURAL',
        'assessment_approach': 'code-review',
    }


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
        # Chỉ giữ escalated concepts (concept trung tính), bỏ proposed raw (tên thư viện)
        escalated_proposed = []
        for item in escalated.get('escalated', []):
            code = item.get('concept_code', '')
            if code and item.get('status') == 'new':
                escalated_proposed.append({
                    'keyword': item.get('keyword', ''),
                    'proposed_name': item.get('concept_name', code),
                    'concept_code': code,
                    'source': 'escalated',
                })
        resolved_concepts['proposed'] = escalated_proposed
        print(f"[*] Dùng escalated concepts từ STEP 3.5 ({len(escalated_proposed)} Gap D concepts)")
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
    # Dấu hiệu template ULO: "nguyên lý phổ quát", "hiểu:", concept code thô
    # Dấu hiệu template CIO: "ngưỡng", "vật lý/logic", "mô hình tham chiếu", "chỉ số" (gen_real_los.py)
    ULO_TEMPLATE_SIGNALS = ['nguyên lý phổ quát', 'vai trò của nó trong thiết kế', 'hiểu:', 'hiểu ', 'người học có khả năng hiểu:']
    CIO_TEMPLATE_SIGNALS = ['ngưỡng', 'vật lý/logic', 'mô hình tham chiếu', 'chỉ số trong']
    for code in list(covered):
        # Kiểm tra ULO template (derived_ulos)
        ulo_template = False
        for lo in matched_cios.get('derived_ulos', []):
            if lo.get('concept_codes') and code in lo.get('concept_codes', []):
                desc = lo.get('description', '').lower()
                if any(sig in desc for sig in ULO_TEMPLATE_SIGNALS):
                    raw_code = code.lower()
                    if (raw_code in desc or desc.startswith('người học có khả năng hiểu nguyên lý')
                            or ' hiểu: ' in desc or desc.startswith('người học có khả năng hiểu:')):
                        ulo_template = True
                break
        # Kiểm tra CIO template (matched_cios) — data Master Tree thối (gen_real_los.py)
        cio_template = False
        for match in matched_cios.get('matched_cios', []):
            if match.get('concept_code') == code:
                cio_desc = match.get('cio_description', '').lower()
                if any(sig in cio_desc for sig in CIO_TEMPLATE_SIGNALS):
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

    generated = []
    for concept_code, info in sorted(uncovered.items()):
        description = get_concept_description(concept_code, inventory)
        concept_name = get_concept_name(concept_code, inventory)
        print(f"  → Generating LOs for {concept_name}")

        ulo = generate_ulo(concept_code, description)
        cio = generate_cio(concept_code, description)
        sio = generate_sio(concept_code, concept_name, description,
                           project_context, args.target_tech)

        generated.extend([ulo, cio, sio])

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
