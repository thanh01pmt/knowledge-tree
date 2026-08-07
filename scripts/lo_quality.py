"""lo_quality.py - Utility module for Learning Objective (LO) quality inspection and description standardisation.
"""

import re
from typing import Tuple, List, Set

# 1. TEMPLATE CIO VERBS (12 verbs from Master Tree template pattern)
TEMPLATE_CIO_VERBS: Set[str] = {
    'EXPLAIN_MECHANISM',
    'INTERPRET_PARAMETERS',
    'DECOMPOSE_TRADEOFFS',
    'COMPARE_ALTERNATIVES',
    'IDENTIFY_COMPONENTS',
    'RECALL_DEFINITIONS',
    'IMPLEMENT_PATTERN',
    'ADAPT_TO_CONTEXT',
    'ASSESS_QUALITY',
    'CRITIQUE_DESIGN',
    'DESIGN_SOLUTION',
    'INNOVATE_EXTENSION',
}

# 2. TEMPLATE DESC SIGNALS (Union deduplicated from assemble_roadmap, generate_jit_los, agent_as_judge)
TEMPLATE_DESC_SIGNALS: List[str] = [
    'ngưỡng',
    'vật lý/logic',
    'mô hình tham chiếu',
    'chỉ số trong',
    'nguyên lý phổ quát',
    'hiểu:',
    'vai trò của nó trong thiết kế',
    'định lượng đánh đổi',
    'tiêu chuẩn ngành',
    'benchmark',
    'nợ kỹ thuật',
    'tối ưu hóa đột phá',
    'tích hợp cross-cutting',
    'điều kiện biên',
    'so sánh nhiều phương pháp/kiến trúc cho',
    'phân rã',
    'cơ chế hoạt động nội tại',
    'hiểu ',
    'người học có khả năng hiểu:',
    'hiểu: hiểu',
    'và vai trò của nó',
    'và cách vận dụng nó',
]

# Layer-specific subsets for is_template_description filtering
ULO_TEMPLATE_SIGNALS: List[str] = [
    'nguyên lý phổ quát',
    'vai trò của nó trong thiết kế',
    'hiểu:',
    'hiểu ',
    'người học có khả năng hiểu:',
    'hiểu: hiểu',
    'và vai trò của nó',
    'và cách vận dụng nó',
]

CIO_TEMPLATE_SIGNALS: List[str] = [
    'ngưỡng',
    'vật lý/logic',
    'mô hình tham chiếu',
    'chỉ số trong',
]

# 3. GENERIC SIO KEYWORDS (15 generic words)
GENERIC_KEYWORDS: Set[str] = {
    'loop', 'state', 'server', 'http', 'api', 'app', 'data', 'error',
    'handler', 'service', 'model', 'view', 'config', 'file', 'function',
}

# 4. FORBIDDEN STRINGS (Never allowed in build_lo_desc output)
FORBIDDEN_STRINGS: List[str] = [
    'nguyên lý phổ quát',
    'và cách vận dụng nó',
    'vai trò của nó trong thiết kế',
]


def is_template_cio_code(cio_code: str) -> bool:
    """True nếu cio_code kết thúc bằng -NN-<VERB> thuộc TEMPLATE_CIO_VERBS."""
    if not cio_code:
        return False
    cio_upper = cio_code.upper()
    for verb in TEMPLATE_CIO_VERBS:
        if cio_upper.endswith(f'-{verb}'):
            return True
    return False


def is_template_description(desc: str, layer: str = '') -> bool:
    """True nếu desc.lower() chứa signal template.
    layer='ULO': chỉ check ULO-relevant signals
    layer='CIO': chỉ check CIO-relevant signals
    layer='': check toàn bộ TEMPLATE_DESC_SIGNALS
    """
    if not desc:
        return False
    d = desc.lower()
    layer_norm = layer.upper() if layer else ''
    if layer_norm == 'ULO':
        signals = ULO_TEMPLATE_SIGNALS
    elif layer_norm == 'CIO':
        signals = CIO_TEMPLATE_SIGNALS
    else:
        signals = TEMPLATE_DESC_SIGNALS
    return any(sig in d for sig in signals)


def is_generic_keyword(kw: str) -> bool:
    """True nếu kw thuộc GENERIC_KEYWORDS (case-insensitive)."""
    if not kw:
        return False
    return kw.strip().lower() in GENERIC_KEYWORDS


def clean_llm_description(desc: str, concept_name: str) -> str:
    """Làm sạch description sinh ra từ LLM.
    - Bỏ markdown fence (```...```)
    - Bỏ prefix '<name>: ' hoặc '<name> - '
    - Dedupe từ 'hiểu' lặp ('hiểu X: Hiểu...' → nối mượt)
    - Strip khoảng trắng thừa
    """
    if not desc:
        return ""

    s = desc.strip()

    # Strip markdown fence
    if s.startswith("```"):
        lines = s.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            lines = lines[1:-1]
            s = "\n".join(lines).strip()
        else:
            s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
            s = re.sub(r"\n?```$", "", s).strip()

    if not s:
        return ""

    cname = concept_name.strip() if concept_name else ""

    if cname:
        # 1. Handle repeated 'hiểu' pattern: 'hiểu X: Hiểu...' or 'Hiểu X: hiểu...'
        dup_pattern = re.compile(
            r'^(?:hiểu|Hiểu)\s+' + re.escape(cname) + r':\s*(?:hiểu|Hiểu)\s+',
            re.IGNORECASE
        )
        if dup_pattern.match(s):
            s = dup_pattern.sub("Hiểu ", s)

        # 2. Handle prefix "<concept_name>: " or "<concept_name> - " or "<concept_name>:"
        prefix_pattern = re.compile(
            r'^' + re.escape(cname) + r'\s*[:\-]\s*',
            re.IGNORECASE
        )
        if prefix_pattern.match(s):
            s = prefix_pattern.sub("", s)

    # 3. Dedupe 'Hiểu: Hiểu' or 'hiểu: hiểu'
    s = re.sub(r'^(?:hiểu|Hiểu):\s*(?:hiểu|Hiểu)\s+', 'Hiểu ', s)

    return s.strip()


def build_lo_desc(
    layer: str,
    concept_code: str,
    concept_name: str,
    source_desc: str,
    keyword: str = '',
    platform: str = ''
) -> Tuple[str, bool]:
    """Tạo description chuẩn hóa cho LO theo layer (ULO/CIO/SIO).
    Returns (description, needs_review)
    """
    cname = concept_name.strip() if concept_name else concept_code.strip()
    layer_norm = layer.upper() if layer else 'ULO'

    cleaned = clean_llm_description(source_desc, cname)

    # Check if cleaned source has content and is NOT a template / forbidden description
    is_valid = bool(cleaned) and not any(f in cleaned.lower() for f in FORBIDDEN_STRINGS)

    if is_valid:
        # Build description using cleaned source
        # Avoid duplicating prefix if cleaned already starts with standard prefix
        if layer_norm == 'ULO':
            action = "hiểu"
        elif layer_norm == 'CIO':
            action = "thiết kế"
        else:  # SIO
            action = "triển khai"

        prefix = f"Người học có khả năng {action} {cname}: "
        if cleaned.lower().startswith(prefix.lower()):
            final_desc = cleaned
        else:
            final_desc = f"{prefix}{cleaned}"
        return final_desc, False

    # Fallback to minimal honest sentence when source_desc is empty or invalid
    needs_review = True
    if layer_norm == 'ULO':
        final_desc = f"Người học có khả năng hiểu {cname} trong ngữ cảnh dự án."
    elif layer_norm == 'CIO':
        final_desc = f"Người học có khả năng vận dụng {cname} ở mức mô hình trong dự án."
    else:  # SIO
        kw_part = f" dùng '{keyword.strip()}'" if keyword and keyword.strip() else ""
        plat_part = f" trong {platform.strip()}" if platform and platform.strip() else ""
        if not plat_part and not kw_part:
            plat_part = " trong dự án"
        final_desc = f"Người học có khả năng triển khai {cname}{kw_part}{plat_part}."

    return final_desc, needs_review
