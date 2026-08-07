#!/usr/bin/env python3
"""
STEP 3.5: Keyword → Concept Escalation (LLM abstraction) cho pipeline v3.

Vấn đề: resolve_concepts.py (STEP 3) dùng embedding trực tiếp keyword → concept.
Keyword là tên thư viện cụ thể (ArduinoJson.h, PubSubClient.h) → embedding match tệ
(0.25 → MECHATRONICS thay vì JSON_SERIALIZATION).

Giải pháp: LLM abstraction — keyword cụ thể → concept trung tính (technology-agnostic),
rồi match Master Tree với threshold cao (0.80). Concept không match → Gap D candidate.

Input:
  keywords.json           (từ STEP 1-2 extract_project_keywords.py)
  resolved_concepts.json  (từ STEP 3 resolve_concepts.py — các proposed concepts)

Output:
  escalated_concepts.json — concept trung tính + matched/new
  {
    "escalated": [
      {"concept_code": "JSON_SERIALIZATION", "concept_name": "...", "status": "matched",
       "keywords": ["ArduinoJson.h"], "score": 0.85},
      {"concept_code": "WIRELESS_NETWORKING", "concept_name": "...", "status": "new",
       "keywords": ["WiFi.h"], "score": 0.0}
    ]
  }

Usage:
    python scripts/escalate_concepts_v3.py \
        --keywords /tmp/pipeline/keywords.json \
        --resolved-concepts /tmp/pipeline/resolved_concepts.json \
        --output /tmp/pipeline/escalated_concepts.json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(SKILL_LLM) not in sys.path:
    sys.path.insert(0, str(SKILL_LLM))

try:
    from llm_call import llm_chat_json, LLMCallError
    from openai import OpenAI
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / '.env')

# Keywords KHÔNG phải kiến thức (tên class/function tự đặt) — bỏ qua
NOISE_KEYWORDS = {
    'type_declaration', 'function_signature', 'property_wrapper',
}
# Keywords là kiến thức thật — cần escalate
REAL_SOURCES = {'import', 'error_handling', 'docstring', 'readme', 'config'}


def load_keywords(keywords_json: dict) -> List[Dict]:
    """Load keywords từ keywords.json (STEP 1-2)."""
    result = []
    for kw in keywords_json.get('keywords', []):
        if not isinstance(kw, dict):
            continue
        source = kw.get('source', '')
        # Bỏ tên class/function tự đặt — không phải concept
        if source in NOISE_KEYWORDS:
            continue
        result.append({
            'keyword': kw.get('keyword', ''),
            'source': source,
            'weight': kw.get('weight', 1.0),
        })
    return result


def load_master_concepts(tsv_path: Path) -> Dict[str, Dict]:
    """Load concepts từ Master Tree TSV (Bảng 5)."""
    concepts = {}
    in_concepts = False
    headers = None
    with open(tsv_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('Bảng 5:'):
                in_concepts = True
                headers = None
                continue
            if not in_concepts or not line or line.startswith('Bảng'):
                continue
            parts = line.split('\t')
            if headers is None:
                headers = parts
                continue
            row = dict(zip(headers, parts))
            if row.get('code'):
                concepts[row['code']] = {
                    'name': row.get('name', ''),
                    'description': row.get('description', ''),
                    'keywords': row.get('keywords', ''),
                }
    return concepts


def escalate_keywords(keywords: List[Dict], master_concepts: Dict) -> List[Dict]:
    """LLM abstraction: keyword cụ thể → concept trung tính, match Master Tree."""
    if not _LLM_AVAILABLE:
        return _fallback_escalate(keywords, master_concepts)

    try:
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY') or os.getenv('SAAS_OLLAMA_CLOUD_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL'),
        )
        model = os.getenv('ATE_MODEL', 'deepseek-v4-flash:cloud')

        # Master concepts — gửi TOÀN BỘ dạng compact (code + name) cho LLM match
        master_sample = [
            {'code': c, 'name': info['name']}
            for c, info in master_concepts.items()
        ]

        kw_list = [k['keyword'] for k in keywords if k['keyword']]
        system = (
            "Bạn là chuyên gia phân loại tri thức. "
            "Nhận danh sách keywords (tên thư viện, API, công nghệ cụ thể). "
            "Với mỗi keyword, xác định concept trung tính (technology-agnostic) nó thuộc về. "
            "QUAN TRONG: Uu tien CHON concept da co trong Master Tree (danh sach ben duoi) "
            "neu keyword la bieu hien cua concept do. "
            "Chi tao concept MOI (status=new) khi that su khong co concept nao trong Master Tree cover. "
            "Trả JSON đúng schema."
        )
        user = f"""Keywords cần escalate:
{json.dumps(kw_list, ensure_ascii=False)}

Master Tree concepts (code, name, keywords) - CHON TU DAY neu co:
{json.dumps(master_sample, ensure_ascii=False)[:12000]}

Trả JSON:
{{
  "escalated": [
    {{
      "keyword": "ArduinoJson.h",
      "concept_code": "JSON_SERIALIZATION",
      "concept_name": "JSON Serialization/Deserialization",
      "status": "matched",
      "score": 0.85,
      "reason": "ArduinoJson la thu vien JSON cho C++ - thuoc concept JSON Serialization"
    }},
    {{
      "keyword": "WiFi.h",
      "concept_code": "PHYSICAL_MEDIA_CONCEPT",
      "concept_name": "Physical Media & Wireless",
      "status": "matched",
      "score": 0.8,
      "reason": "WiFi.h la thu vien wireless - thuoc concept Physical Media & Wireless"
    }}
  ]
}}"""
        res = llm_chat_json(client, model, system, user, temperature=0.1)
        return res.get('escalated', [])
    except Exception as e:
        print(f"[WARN] LLM escalate failed ({e}), fallback", file=sys.stderr)
        return _fallback_escalate(keywords, master_concepts)


def _fallback_escalate(keywords: List[Dict], master_concepts: Dict) -> List[Dict]:
    """Fallback: keyword → concept code từ tên (không lý tưởng, chỉ khi LLM unavailable)."""
    result = []
    for kw in keywords:
        keyword = kw.get('keyword', '')
        if not keyword:
            continue
        # Tạo code tạm từ keyword
        code = ''.join(c for c in keyword.upper() if c.isalnum() or c == '_')[:40]
        result.append({
            'keyword': keyword,
            'concept_code': code,
            'concept_name': keyword,
            'status': 'new',
            'score': 0.0,
            'reason': 'Fallback heuristic — LLM unavailable',
        })
    return result


def main():
    parser = argparse.ArgumentParser(description='STEP 3.5: Keyword → Concept Escalation (LLM)')
    parser.add_argument('--keywords', type=Path, required=True, help='keywords.json từ STEP 1-2')
    parser.add_argument('--resolved-concepts', type=Path, required=True, help='resolved_concepts.json từ STEP 3')
    parser.add_argument('--master-tsv', type=Path, default=None,
                        help='Master Tree TSV (default: services/.../mlo-knowlege-tree.tsv)')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    # Load inputs
    keywords_data = json.loads(args.keywords.read_text(encoding='utf-8'))
    resolved_data = json.loads(args.resolved_concepts.read_text(encoding='utf-8'))

    keywords = load_keywords(keywords_data)
    print(f"[*] Keywords (kiến thức thật): {len(keywords)}")

    # Master Tree
    master_tsv = args.master_tsv or (REPO_ROOT / 'services' / 'python-api' / 'general-context' / 'mlo-knowlege-tree.tsv')
    master_concepts = load_master_concepts(master_tsv)
    print(f"[*] Master Tree concepts: {len(master_concepts)}")

    # LLM escalate
    escalated = escalate_keywords(keywords, master_concepts)
    print(f"[*] Escalated: {len(escalated)} concepts")

    # Stats
    n_matched = sum(1 for e in escalated if e.get('status') == 'matched')
    n_new = sum(1 for e in escalated if e.get('status') == 'new')
    print(f"    Matched: {n_matched} | New (Gap D): {n_new}")

    # Output
    output = {
        'escalated': escalated,
        'summary': {
            'total_keywords': len(keywords),
            'matched': n_matched,
            'new_concepts': n_new,
        },
    }
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"[✓] Saved to {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
