#!/usr/bin/env python3
"""
STEP 0.5: Tech Stack Proposal & Architecture Detection.

Dựa trên mô tả yêu cầu (goal), LLM:
1. Research + đề xuất 2-3 tech stack options (kèm trade-off)
2. User chọn (hoặc --tech-stack nếu đã rõ)
3. Từ tech stack → suy ra kiến trúc (components + roles: ui/backend/device)

Output: tech_stack_proposal.json
{
  "goal": "...",
  "options": [
    {"option_id": 1, "title": "...", "tech_stack": [...], "tradeoffs": "...", "architecture": {...}}
  ],
  "selected_option": 1,
  "architecture": {
    "project_type": "app_with_device",
    "components": [
      {"name": "iOS App", "role": "ui", "tech": ["Swift", "SwiftUI"]},
      {"name": "ESP32 Firmware", "role": "device", "tech": ["C++", "Arduino"]}
    ],
    "communication": "REST + MQTT"
  }
}

Usage:
    python scripts/propose_tech_stack.py \
        --goal "Học SwiftUI để điều khiển ESP32 qua WiFi" \
        --tech-stack "Swift,SwiftUI,ESP32" \
        --output /tmp/tech_stack_proposal.json
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
    from llm_call import llm_chat_json, LLMCallError, get_llm_client
    from openai import OpenAI
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / '.env')


def _get_client():
    """Trả (client, model) qua provider layer (deepseek | ollama-cloud | ollama)."""
    client, _provider, model = get_llm_client()
    return client, model


def propose_options(goal: str, tech_stack: List[str]) -> List[Dict]:
    """LLM đề xuất 2-3 tech stack options từ goal."""
    if not _LLM_AVAILABLE:
        return _fallback_options(goal, tech_stack)

    try:
        client, model = _get_client()

        system = (
            "Bạn là kiến trúc sư phần mềm + cố vấn học tập. "
            "Phân tích yêu cầu học tập, đề xuất 2-3 tech stack options khả thi "
            "(từ đơn giản đến đầy đủ), kèm trade-off rõ ràng. "
            "Với mỗi option, suy ra kiến trúc: components (ui/backend/device), "
            "giao thức giao tiếp, project_type. "
            "Trả JSON đúng schema."
        )
        user = f"""Yêu cầu: '{goal}'
Tech stack gợi ý (nếu có): {', '.join(tech_stack) if tech_stack else 'chưa xác định'}

Trả JSON:
{{
  "options": [
    {{
      "option_id": 1,
      "title": "Tên option",
      "tech_stack": ["Swift", "SwiftUI"],
      "tradeoffs": "Mô tả ưu/nhược",
      "architecture": {{
        "project_type": "app | app_with_device | cli | library | api_service | web",
        "components": [
          {{"name": "iOS App", "role": "ui", "tech": ["Swift", "SwiftUI"]}},
          {{"name": "ESP32 Firmware", "role": "device", "tech": ["C++", "Arduino"]}}
        ],
        "communication": "REST + MQTT"
      }}
    }}
  ]
}}"""
        res = llm_chat_json(client, model, system, user, temperature=0.3)
        return res.get('options', [])
    except Exception as e:
        print(f"[WARN] Tech stack proposal LLM failed ({e}), fallback", file=sys.stderr)
        return _fallback_options(goal, tech_stack)


def _fallback_options(goal: str, tech_stack: List[str]) -> List[Dict]:
    """Fallback: dùng tech stack đã cho hoặc heuristic."""
    if tech_stack:
        return [{
            'option_id': 1,
            'title': f'Dự án với {", ".join(tech_stack)}',
            'tech_stack': tech_stack,
            'tradeoffs': 'Tech stack do user cung cấp',
            'architecture': _infer_architecture(tech_stack),
        }]
    return [{
        'option_id': 1,
        'title': f'Dự án: {goal[:50]}',
        'tech_stack': ['Python'],
        'tradeoffs': 'Fallback heuristic — chưa có LLM',
        'architecture': {'project_type': 'app', 'components': [], 'communication': ''},
    }]


def _infer_architecture(tech_stack: List[str]) -> Dict:
    """Heuristic suy ra kiến trúc từ tech stack (fallback khi LLM unavailable)."""
    joined = ' '.join(tech_stack).lower()
    components = []
    roles = []

    # UI frameworks
    ui_techs = [t for t in tech_stack if t.lower() in ['swiftui', 'react', 'vue', 'flutter', 'tkinter', 'html', 'swift']]
    if ui_techs:
        components.append({'name': 'UI App', 'role': 'ui', 'tech': ui_techs})
        roles.append('ui')
    # Backend
    backend_techs = [t for t in tech_stack if t.lower() in ['node', 'fastapi', 'flask', 'django', 'express', 'go']]
    if backend_techs:
        components.append({'name': 'Backend', 'role': 'backend', 'tech': backend_techs})
        roles.append('backend')
    # Device/embedded
    device_techs = [t for t in tech_stack if t.lower() in ['esp32', 'arduino', 'c++', 'embedded', 'raspberry']]
    if device_techs:
        components.append({'name': 'Device Firmware', 'role': 'device', 'tech': device_techs})
        roles.append('device')

    if 'ui' in roles and 'device' in roles:
        ptype = 'app_with_device'
    elif 'ui' in roles and 'backend' in roles:
        ptype = 'web'
    elif 'ui' in roles:
        ptype = 'app'
    elif 'backend' in roles:
        ptype = 'api_service'
    else:
        ptype = 'library'

    return {
        'project_type': ptype,
        'components': components,
        'communication': 'REST + MQTT' if 'device' in roles else 'HTTP',
    }


def main():
    parser = argparse.ArgumentParser(description='STEP 0.5: Tech Stack Proposal & Architecture Detection')
    parser.add_argument('--goal', required=True, help='Mô tả yêu cầu học tập')
    parser.add_argument('--tech-stack', default='', help='Tech stack đã biết (comma-separated, optional)')
    parser.add_argument('--select-option', type=int, default=1, help='Option user chọn (default: 1)')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    tech_stack = [t.strip() for t in args.tech_stack.split(',') if t.strip()]

    # 1. LLM đề xuất options
    options = propose_options(args.goal, tech_stack)
    print(f"[*] Đề xuất {len(options)} tech stack options")

    # 2. User chọn (hoặc default)
    selected = None
    for opt in options:
        if opt.get('option_id') == args.select_option:
            selected = opt
            break
    if not selected and options:
        selected = options[0]
    if not selected:
        print("[ERROR] Không có option nào")
        return 1

    print(f"[✓] Chọn option {selected.get('option_id')}: {selected.get('title')}")
    print(f"    Tech stack: {', '.join(selected.get('tech_stack', []))}")
    arch = selected.get('architecture', {})
    print(f"    Project type: {arch.get('project_type')}")
    for comp in arch.get('components', []):
        print(f"    - {comp.get('name')} ({comp.get('role')}): {', '.join(comp.get('tech', []))}")

    # 3. Output
    result = {
        'goal': args.goal,
        'options': options,
        'selected_option': selected.get('option_id'),
        'selected_title': selected.get('title'),
        'tech_stack': selected.get('tech_stack', []),
        'architecture': arch,
    }
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[✓] Saved to {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
