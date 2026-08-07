#!/usr/bin/env python3
"""
STEP 8.8: Generate JIT Knowledge Graph from a real repository.

Design (docs/ideas/2026-08-06-jit-knowledge-graph.md):
- Phase = bước xây dựng sản phẩm (setup, data model, core logic, config, UI, test)
- 1 luồng chính Start → End duy nhất
- Mỗi implement chỉ nối với kiến thức TỐI THIỂU cần cho nó (JIT)
- Keyword = chú thích dưới node (note), không tạo nhánh giả
- Mỗi phase 1 màu, kết thúc bằng implement cụ thể

Usage:
    python scripts/generate_jit_graph.py \
        --repo-dir /path/to/repo \
        --output jit_graph.json

Output: jit_graph.json (dạng roadmap.sh: nodes + edges + position)
"""

import ast
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ============================================================================
# CONSTRUCT → KNOWLEDGE MAPPING (per language)
# ============================================================================

# Python constructs → minimal knowledge needed
PY_CONSTRUCT_KNOWLEDGE = {
    # Foundation (Phase 1)
    'setup_python': ('Cài đặt Python', 'install, terminal, PATH'),
    'run_script': ('Chạy script đầu tiên', 'python main.py, print, input'),
    'create_project': ('Tạo thư mục dự án', 'main.py, config.py, requirements.txt'),
    'git_init': ('Git init & commit', 'git init, add, commit, .gitignore'),
    'import': ('Module & import', 'import, from...import, __name__'),
    'assign': ('Biến & kiểu dữ liệu', 'int, str, bool, list, dict'),
    'if': ('If/Else', 'điều kiện, so sánh'),
    'for': ('Vòng lặp', 'for, range, duyệt collection'),
    'f_string': ('F-string', 'f"...{var}", format'),
    'type_hint': ('Type hints', 'List[str], Optional, -> Ret'),
    # Data (Phase 2)
    'list_comp': ('List comprehension', '[x for x in list if ...]'),
    'asdict()': ('Dataclass', '@dataclass, asdict, field'),
    'dumps()': ('JSON', 'json.dumps, indent'),
    'loads()': ('JSON', 'json.loads, parse'),
    'Path()': ('Path & file I/O', 'Path, read_text, write_text, exists'),
    'read_text()': ('Path & file I/O', 'Path, read_text, write_text, exists'),
    'write_text()': ('Path & file I/O', 'Path, read_text, write_text, exists'),
    'exists()': ('Path & file I/O', 'Path, read_text, write_text, exists'),
    'lower()': ('String methods', 'lower, split, strip'),
    'split()': ('String methods', 'lower, split, strip'),
    # AI (Phase 3)
    'getenv()': ('Env vars', 'os.getenv, default, .env'),
    # UI (Phase 5)
    'Tk()': ('Tkinter basics', 'Tk, mainloop'),
    'Entry()': ('Tkinter widgets', 'Entry, Button, Text, pack'),
    'Button()': ('Tkinter widgets', 'Entry, Button, Text, pack'),
    'Text()': ('Tkinter widgets', 'Entry, Button, Text, pack'),
    'pack()': ('Tkinter layout', 'pack, grid, padding'),
    'title()': ('Tkinter basics', 'Tk, mainloop'),
    'get()': ('Event handler', 'button command, callback, đọc input'),
    'insert()': ('Event handler', 'button command, callback, render kết quả'),
    'delete()': ('Event handler', 'button command, callback, render kết quả'),
    # Test (Phase 6)
    'try_except': ('Error handling', 'try/except, raise, validate'),
}

# Swift constructs → minimal knowledge needed
SWIFT_CONSTRUCT_KNOWLEDGE = {
    'import': ('Module & import', 'import Foundation, import UIKit'),
    'class': ('Class & struct', 'class, struct, protocol, enum'),
    'struct': ('Class & struct', 'class, struct, protocol, enum'),
    'enum': ('Enum & associated values', 'enum, case, associated values'),
    'protocol': ('Protocol & delegate', 'protocol, delegate, extension'),
    'var': ('Biến & kiểu dữ liệu', 'var, let, Int, String, Bool'),
    'let': ('Biến & kiểu dữ liệu', 'var, let, Int, String, Bool'),
    'func': ('Hàm', 'func, return, tham số, default value'),
    'guard': ('Guard & early return', 'guard let, else, early return'),
    'if': ('If/Else', 'điều kiện, so sánh'),
    'for': ('Vòng lặp', 'for, in, duyệt collection'),
    'switch': ('Switch', 'switch, case, pattern matching'),
    'try': ('Error handling', 'try, catch, throws, do'),
    'catch': ('Error handling', 'try, catch, throws, do'),
    'async': ('Async/await', 'async, await, Task'),
    'await': ('Async/await', 'async, await, Task'),
    'closure': ('Closure', 'closure, trailing closure, capture list'),
    'optional': ('Optional & unwrap', '?, !, guard let, if let'),
    'map': ('Higher-order functions', 'map, filter, reduce, compactMap'),
    'filter': ('Higher-order functions', 'map, filter, reduce, compactMap'),
    'reduce': ('Higher-order functions', 'map, filter, reduce, compactMap'),
    'JSONDecoder': ('JSON Codable', 'Codable, JSONDecoder, decode'),
    'JSONEncoder': ('JSON Codable', 'Codable, JSONEncoder, encode'),
    'Codable': ('JSON Codable', 'Codable, JSONDecoder, decode'),
    'URLSession': ('URLSession & API', 'URLSession, dataTask, async/await'),
    'dataTask': ('URLSession & API', 'URLSession, dataTask, async/await'),
    'UserDefaults': ('UserDefaults', 'set, object, standard'),
    'ObservableObject': ('ObservableObject', '@Published, @StateObject, Combine'),
    '@Published': ('ObservableObject', '@Published, @StateObject, Combine'),
    'View': ('SwiftUI View', 'View, body, some View'),
    'body': ('SwiftUI View', 'View, body, some View'),
    'NavigationView': ('SwiftUI navigation', 'NavigationView, NavigationLink'),
    'List': ('SwiftUI List', 'List, ForEach, Section'),
    'ForEach': ('SwiftUI List', 'List, ForEach, Section'),
    'Button': ('SwiftUI Button', 'Button, action, label'),
    'TextField': ('SwiftUI TextField', 'TextField, @State, binding'),
    '@State': ('SwiftUI state', '@State, @Binding, @Environment'),
    '@Binding': ('SwiftUI state', '@State, @Binding, @Environment'),
    'UIKit': ('UIKit basics', 'UIViewController, UIView, UITableView'),
    'UIViewController': ('UIKit basics', 'UIViewController, UIView, UITableView'),
    'UITableView': ('UIKit basics', 'UIViewController, UIView, UITableView'),
    'UICollectionView': ('UIKit collection', 'UICollectionView, UICollectionViewCell'),
    'DispatchQueue': ('Concurrency', 'DispatchQueue, main, async'),
    'Task': ('Concurrency', 'Task, async/await, MainActor'),
    'MainActor': ('Concurrency', 'Task, async/await, MainActor'),
    'Combine': ('Combine', 'Publisher, Subscriber, sink'),
    'sink': ('Combine', 'Publisher, Subscriber, sink'),
    'deinit': ('Memory management', 'ARC, retain cycle, weak'),
    'weak': ('Memory management', 'ARC, retain cycle, weak'),
    'unowned': ('Memory management', 'ARC, retain cycle, weak'),
    'extension': ('Extension', 'extension, protocol conformance'),
    'generic': ('Generics', 'T, where, associatedtype'),
    'associatedtype': ('Generics', 'T, where, associatedtype'),
    'actor': ('Actor', 'actor, isolated, Sendable'),
    'Sendable': ('Actor', 'actor, isolated, Sendable'),
}

# C++/Arduino constructs → minimal knowledge needed
CPP_CONSTRUCT_KNOWLEDGE = {
    'include': ('Include & libraries', '#include, Arduino.h, Adafruit_NeoPixel'),
    'setup': ('Arduino setup', 'setup(), pinMode, Serial.begin'),
    'loop': ('Arduino loop', 'loop(), delay, millis'),
    'WiFi': ('WiFi connection', 'WiFi.begin, WiFi.status, WL_CONNECTED'),
    'WebServer': ('HTTP server', 'WebServer, server.on, server.send'),
    'server.on': ('HTTP routes', 'server.on, HTTP_GET, HTTP_POST'),
    'ArduinoJson': ('JSON parsing', 'StaticJsonDocument, deserializeJson, serializeJson'),
    'deserializeJson': ('JSON parsing', 'StaticJsonDocument, deserializeJson, serializeJson'),
    'serializeJson': ('JSON parsing', 'StaticJsonDocument, deserializeJson, serializeJson'),
    'PubSubClient': ('MQTT client', 'PubSubClient, setServer, setCallback, publish'),
    'mqttClient': ('MQTT client', 'PubSubClient, setServer, setCallback, publish'),
    'Adafruit_NeoPixel': ('LED strip', 'Adafruit_NeoPixel, setPixelColor, show'),
    'strip': ('LED strip', 'Adafruit_NeoPixel, setPixelColor, show'),
    'setPixelColor': ('LED strip', 'Adafruit_NeoPixel, setPixelColor, show'),
    'show': ('LED strip', 'Adafruit_NeoPixel, setPixelColor, show'),
    'delay': ('Timing', 'delay, millis, non-blocking'),
    'millis': ('Timing', 'delay, millis, non-blocking'),
    'String': ('String handling', 'String, concat, indexOf'),
    'uint8_t': ('Data types', 'uint8_t, uint16_t, int, byte'),
    'if': ('If/Else', 'điều kiện, so sánh'),
    'for': ('Vòng lặp', 'for, duyệt collection'),
    'while': ('Vòng lặp', 'while, điều kiện'),
    'switch': ('Switch', 'switch, case, break'),
    'void': ('Hàm', 'void, return, tham số'),
    'bool': ('Data types', 'bool, true, false'),
}

# Python builtins that are NOT knowledge (noise)
PY_NOISE = {
    'print', 'len', 'range', 'str', 'int', 'list', 'dict', 'set', 'tuple',
    'self', 'super', 'isinstance', 'type', 'id', 'repr', 'format', 'sorted',
    'enumerate', 'zip', 'map', 'filter', 'sum', 'min', 'max', 'abs', 'round',
    'open', 'input', 'bool', 'float', 'object', 'property', 'staticmethod',
    'classmethod', 'hasattr', 'getattr', 'setattr', 'delattr', 'vars',
}

# ============================================================================
# PHASE MAPPING — VERTICAL SLICING (docs/ideas/2026-08-07-vertical-slicing-roadmap.md)
# ============================================================================
# Phase chia theo MỨC ĐỘ HOÀN THIỆN SẢN PHẨM, không theo tầng công nghệ:
#   P0 NỀN TẢNG   — làm quen công cụ, ngôn ngữ, thiết lập dự án
#   P1 MVP        — sản phẩm CHẠY ĐƯỢC từ đầu (UI + logic + data tối giản)
#   P2 MỞ RỘNG    — thật hóa: API thật, file persistence, lọc
#   P3 HOÀN THIỆN — độ chắc: error handling, validation, test, polish

PHASE_COLORS = {
    0: '#6b6b76',  # gray — NỀN TẢNG
    1: '#0e7c6b',  # teal — MVP
    2: '#2b78e4',  # blue — MỞ RỘNG
    3: '#8e44ad',  # purple — HOÀN THIỆN
}

PHASE_NAMES = {
    0: 'NỀN TẢNG',
    1: 'MVP',
    2: 'MỞ RỘNG',
    3: 'HOÀN THIỆN',
}

# ============================================================================
# PROJECT TYPE DETECTION (docs/ideas/2026-08-07-vertical-slicing-roadmap.md §7.4)
# ============================================================================
# "Thấy sản phẩm" khác nhau theo loại dự án:
#   APP      — UI tối giản + logic chạy
#   CLI      — chạy được command
#   LIBRARY  — public API + 1 use case
#   API_SVC  — 1 endpoint + health check

PROJECT_TYPES = {
    'app': 'App có UI',
    'cli': 'CLI tool',
    'library': 'Library/SDK',
    'api_service': 'API service',
}


def detect_project_type(repo_dir: Path) -> str:
    """Detect loại dự án từ cấu trúc repo.

    Heuristic:
    - Có main.py / AppDelegate / @main / __main__ → app
    - Có Package.swift / setup.py / pyproject.toml (chỉ exports) → library
    - Có main.py + argparse/click/typer → cli
    - Có app.py / server.py / main.py + FastAPI/Flask/Django → api_service
    """
    files = list(repo_dir.rglob('*')) if repo_dir.exists() else []
    names = {f.name for f in files if f.is_file()}
    paths = {str(f) for f in files if f.is_file()}

    has_main = any(n in names for n in ['main.py', 'app.py', 'server.py', 'index.js', 'index.ts'])
    # SwiftUI app: file có @main
    if not has_main:
        for f in files:
            if f.is_file() and f.suffix == '.swift':
                try:
                    src = f.read_text(encoding='utf-8', errors='ignore')[:2000]
                    if '@main' in src:
                        has_main = True
                        break
                except Exception:
                    pass
    has_package = any(n in names for n in ['Package.swift', 'setup.py', 'pyproject.toml', 'package.json', 'Cargo.toml'])
    has_cli = any(n in names for n in ['cli.py', 'cli.js', 'main.go'])

    # API framework detection
    api_frameworks = ['fastapi', 'flask', 'django', 'express', 'gin', 'actix']
    has_api = False
    for f in files:
        if f.is_file() and f.suffix in ('.py', '.js', '.ts', '.go'):
            try:
                src = f.read_text(encoding='utf-8', errors='ignore')[:2000]
                if any(fw in src.lower() for fw in api_frameworks):
                    has_api = True
                    break
            except Exception:
                pass

    if has_api:
        return 'api_service'
    if has_cli:
        return 'cli'
    if has_main:
        return 'app'
    if has_package:
        return 'library'
    # Không có entry point (main) → library (thư viện thuần)
    return 'library'

# Constructs báo hiệu external I/O (file persistence) → P2
FILE_IO_CONSTRUCTS = {'Path()', 'read_text()', 'write_text()', 'exists()', 'open()',
                      'JSONDecoder', 'JSONEncoder', 'UserDefaults', 'URLSession', 'dataTask'}

# Constructs báo hiệu error handling / validation → P3
ROBUSTNESS_CONSTRUCTS = {'try_except', 'assert', 'validate', 'try', 'catch', 'throws'}

# Constructs báo hiệu UI (entry point "thấy sản phẩm") → P1
UI_CONSTRUCTS = {'Tk()', 'Entry()', 'Button()', 'Text()', 'pack()', 'mainloop()', 'title()',
                 'get()', 'insert()', 'delete()', 'View', 'body', 'NavigationView', 'List',
                 'ForEach', 'TextField', '@State', '@Binding', 'UIKit', 'UIViewController',
                 'UITableView', 'UICollectionView'}


def assign_phase(imp: dict) -> int:
    """Assign phase theo mức độ hoàn thiện sản phẩm (vertical slicing).

    P0: setup/scaffold — không có logic sản phẩm
    P1: MVP — core flow (UI, orchestration, data model, JSON)
    P2: MỞ RỘNG — external I/O (file persistence, API call, network)
    P3: HOÀN THIỆN — error handling, validation, test
    """
    name = imp['name'].lower()
    constructs = set(imp.get('constructs', []))

    # P0: setup/scaffold — chỉ exact match, không bắt setUp (test) / setup (UI)
    if name in ('scaffold', 'bootstrap') or 'setup_python' in constructs:
        return 0

    # CLI entry point (main) → P1 MVP — "thấy sản phẩm" = chạy được command
    if name == 'main' and 'argparse' in str(imp.get('constructs', [])):
        return 1

    # MOCK (giả lập) → P1 MVP — mock là sản phẩm chạy được, thật hóa ở P2
    if detect_mock(imp):
        return 1

    # P3: error handling, validation, test
    # Lưu ý: 'try' trong Swift có thể là try! (force unwrap) — không phải error handling
    if 'try_except' in constructs or 'catch' in constructs or 'throws' in constructs:
        return 3
    if 'validate' in name or 'test' in name or 'assert' in name:
        return 3

    # P2: external I/O — file persistence, network, API
    if FILE_IO_CONSTRUCTS & constructs:
        return 2
    # P2: API call functions (call_*, fetch_*, request_*, *_api, http, client, connect)
    if any(k in name for k in ['call_', 'fetch', 'request', '_api', 'http', 'client', 'connect', 'send', 'upload', 'download']):
        return 2

    # P1: MVP — core flow (UI, orchestration, data model, JSON)
    return 1



# Dấu hiệu mock: comment "simplified/in production/mock" + trả literal cứng
MOCK_SIGNALS = ['simplified', 'in production', 'mock', 'fake', 'placeholder', 'stub', 'hardcoded']


def detect_mock(imp: dict) -> bool:
    """Detect nếu implement là mock (giả lập, chưa gọi thật).

    Dấu hiệu:
    1. Comment chứa "simplified", "in production", "mock", "stub"...
    2. Body trả literal cứng (JSON/dict/list) mà không gọi external
    """
    desc = (imp.get('description', '') or '').lower()
    src = (imp.get('source', '') or '').lower()
    if any(sig in desc for sig in MOCK_SIGNALS):
        return True
    # Comment trong source: "simplified", "in production", "mock"...
    if any(sig in src for sig in MOCK_SIGNALS):
        return True
    # Function trả literal cứng (dumps/loads với data tĩnh) + không gọi external
    constructs = set(imp.get('constructs', []))
    calls = set(imp.get('calls', []))
    has_literal = 'dumps' in constructs or 'loads' in constructs
    has_external = bool(FILE_IO_CONSTRUCTS & constructs) or bool(calls)
    if has_literal and not has_external:
        return True
    return False


def propagate_phases(implements: List[dict]) -> None:
    """Call graph propagation: implement gọi function có file I/O → nâng lên P2.

    UI (entry point "thấy sản phẩm") luôn giữ P1 (MVP) — không bị nâng.
    Implement gọi MOCK (giả lập) cũng giữ P1 — vì mock là MVP, thật hóa ở P2.

    Ví dụ: filter_by_topic gọi load() (file I/O) → filter_by_topic nên P2.
    Nhưng generate_questions gọi _call_llm (MOCK) → giữ P1 (MVP chạy được).
    """
    # Build name → phase map (function-level)
    name_phase = {}
    mock_names = set()
    for imp in implements:
        name_phase[imp['name']] = imp['phase']
        if detect_mock(imp):
            mock_names.add(imp['name'])

    # Iterate until stable (max 3 passes)
    for _ in range(3):
        changed = False
        for imp in implements:
            if imp['phase'] >= 2:
                continue
            # UI/CLI entry point → giữ P1 (MVP), không nâng
            if UI_CONSTRUCTS & set(imp.get('constructs', [])):
                continue
            if imp['name'] == 'main':
                continue
            # Nếu gọi function nào đó ở P2 (file I/O) → nâng lên P2
            for callee in imp.get('calls', []):
                # Gọi mock → giữ P1 (mock là MVP, chưa thật hóa)
                if callee in mock_names:
                    continue
                if name_phase.get(callee, 0) >= 2:
                    imp['phase'] = 2
                    imp['phase_label'] = PHASE_NAMES[2]
                    changed = True
                    break
        if not changed:
            break


# ============================================================================
# FEATURE CLUSTERING (docs/ideas/2026-08-07-vertical-slicing-roadmap.md §7.1)
# ============================================================================
# Hybrid: tự động detect (call graph → connected components) + config override.
# Feature = nhóm implements cùng 1 chức năng (UI + logic + data).


def build_call_graph(implements: List[dict]) -> Dict[str, Set[str]]:
    """Build call graph: {function_name: set of called function names}."""
    graph = {}
    for imp in implements:
        graph[imp['name']] = set(imp.get('calls', []))
    return graph


def cluster_features(implements: List[dict], config: dict = None) -> Tuple[Dict[str, int], Dict[int, str]]:
    """Gán feature_id cho mỗi implement + feature names.

    Tự động: connected components trên call graph (implements gọi nhau = 1 feature).
    Override: config {'feature_name': ['impl1', 'impl2', ...]} — ghi đè auto.

    Returns: (feature_id_map, feature_names) — feature_names: {id: tên feature}
    """
    # 1. Config override (nếu có)
    if config and config.get('features'):
        feature_id = {}
        feature_names = {}
        for fid, (fname, impls) in enumerate(config['features'].items()):
            feature_names[fid] = fname
            for name in impls:
                feature_id[name] = fid
        return feature_id, feature_names

    # 2. Auto: connected components trên call graph
    graph = build_call_graph(implements)
    # Union-find
    parent = {imp['name']: imp['name'] for imp in implements}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # Union implements gọi nhau
    for imp in implements:
        for callee in imp.get('calls', []):
            if callee in parent:
                union(imp['name'], callee)

    # Gán feature_id theo root
    feature_ids = {}
    root_to_id = {}
    next_id = 0
    for imp in implements:
        root = find(imp['name'])
        if root not in root_to_id:
            root_to_id[root] = next_id
            next_id += 1
        feature_ids[imp['name']] = root_to_id[root]

    # Feature names từ root implement (tên có ý nghĩa nhất)
    feature_names = {}
    for root, fid in root_to_id.items():
        feature_names[fid] = readable_name(root)
    return feature_ids, feature_names


# ============================================================================
# BLOOM LEVEL — LLM EVALUATION (docs/ideas/2026-08-07-vertical-slicing-roadmap.md §7.3)
# ============================================================================
# LLM đánh giá bloom_level cho từng knowledge item (chính xác hơn heuristic).
# Fallback: heuristic theo phase khi LLM unavailable.

import sys as _sys
REPO_ROOT = Path(__file__).resolve().parents[1]
_SKILL_LLM = REPO_ROOT / '.agents' / 'skills' / 'keyword-extractor' / 'scripts'
if str(_SKILL_LLM) not in _sys.path:
    _sys.path.insert(0, str(_SKILL_LLM))

try:
    from llm_call import llm_chat_json, LLMCallError
    from openai import OpenAI
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

# Bloom levels (Anderson & Krathwohl)
BLOOM_LEVELS = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']


def evaluate_bloom_llm(knowledge_items: List[dict], project_type: str = 'app') -> List[dict]:
    """LLM đánh giá bloom_level cho từng knowledge item.

    Input: list knowledge items (label + note + phase)
    Output: list với bloom_level gán bởi LLM
    Fallback: heuristic theo phase nếu LLM unavailable/fail.
    """
    if not _LLM_AVAILABLE:
        return _evaluate_bloom_heuristic(knowledge_items)

    try:
        import os
        from dotenv import load_dotenv
        load_dotenv(REPO_ROOT / '.env')
        api_key = os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return _evaluate_bloom_heuristic(knowledge_items)

        client = OpenAI(api_key=api_key, base_url=os.getenv('OPENAI_BASE_URL'))
        model = os.getenv('ATE_MODEL', 'deepseek-v4-flash:cloud')

        # Batch: gửi tất cả knowledge items 1 lần
        items_desc = '\n'.join(
            f"- {k['label']} ({k.get('note', '')}) [phase {k.get('phase', 1)}]"
            for k in knowledge_items
        )
        system = (
            "Bạn là chuyên gia giáo dục (Bloom's Taxonomy). "
            "Đánh giá mức độ nhận thức cần thiết cho mỗi kiến thức trong roadmap học lập trình. "
            f"Project type: {PROJECT_TYPES.get(project_type, project_type)}. "
            'Trả JSON: {"items": [{"label": "...", "bloom_level": "understand"}]}'
        )
        user = "Đánh giá bloom_level (1 trong: " + ', '.join(BLOOM_LEVELS) + ") cho:\n" + items_desc

        result = llm_chat_json(client, model, system, user, temperature=0.1)
        llm_map = {}
        for item in result.get('items', []):
            label = item.get('label', '')
            bloom = item.get('bloom_level', '')
            if label and bloom in BLOOM_LEVELS:
                llm_map[label] = bloom

        # Gán bloom từ LLM, fallback heuristic cho items thiếu
        for k in knowledge_items:
            if k['label'] in llm_map:
                k['bloom_level'] = llm_map[k['label']]
            else:
                k['bloom_level'] = _heuristic_bloom(k)
        return knowledge_items
    except Exception as e:
        print(f"[WARN] LLM bloom evaluation failed ({e}), fallback heuristic")
        return _evaluate_bloom_heuristic(knowledge_items)


def _evaluate_bloom_heuristic(knowledge_items: List[dict]) -> List[dict]:
    """Fallback: bloom theo phase (P0 remember, P1 understand, P2 apply, P3 create)."""
    for k in knowledge_items:
        k['bloom_level'] = _heuristic_bloom(k)
    return knowledge_items


def _heuristic_bloom(k: dict) -> str:
    """Heuristic bloom từ phase + constructs."""
    phase = k.get('phase', 1)
    return PHASE_BLOOM.get(phase, 'understand')


# ============================================================================
# AST ANALYSIS
# ============================================================================


def build_description(node, parent_class: str = '') -> str:
    """Build a natural, informative description from name, params, fields, and constructs.

    Ưu tiên: docstring > heuristic giàu ngữ cảnh (class cha + constructs).
    """
    name = node.name
    # Class: describe from fields + methods
    if isinstance(node, ast.ClassDef):
        fields = []
        methods = []
        for sub in node.body:
            if isinstance(sub, ast.AnnAssign) and isinstance(sub.target, ast.Name):
                fields.append(sub.target.id)
            elif isinstance(sub, ast.FunctionDef) and not (sub.name.startswith('__') and sub.name.endswith('__')):
                methods.append(sub.name)
        parts = []
        if fields:
            parts.append(f"các trường: {', '.join(fields)}")
        if methods:
            parts.append(f"phương thức: {', '.join(methods)}")
        if parts:
            return f"Định nghĩa class {name} với {'; '.join(parts)}"
        return f"Định nghĩa class {name}"

    # Function: verb + object + purpose from constructs
    args = []
    if node.args.args:
        args = [a.arg for a in node.args.args if a.arg != 'self']
    arg_str = ', '.join(args) if args else ''

    # Collect constructs for purpose inference
    constructs = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            if isinstance(sub.func, ast.Attribute):
                constructs.add(sub.func.attr)
            elif isinstance(sub.func, ast.Name):
                constructs.add(sub.func.id)
        elif isinstance(sub, ast.JoinedStr):
            constructs.add('f_string')
        elif isinstance(sub, ast.ListComp):
            constructs.add('list_comp')
        elif isinstance(sub, ast.Try):
            constructs.add('try_except')

    # Verb mapping
    verbs = {
        'save': 'Lưu dữ liệu', 'load': 'Đọc dữ liệu', 'get': 'Lấy dữ liệu',
        'set': 'Thiết lập', 'create': 'Tạo', 'build': 'Xây dựng',
        'generate': 'Sinh', 'parse': 'Phân tích', 'filter': 'Lọc',
        'call': 'Gọi', 'init': 'Khởi tạo', 'setup': 'Thiết lập',
        'run': 'Chạy', 'main': 'Khởi chạy', 'delete': 'Xóa',
        'insert': 'Chèn', 'update': 'Cập nhật', 'validate': 'Kiểm tra',
        'convert': 'Chuyển đổi', 'format': 'Định dạng',
        'filter_by': 'Lọc', 'setup_': 'Thiết lập', 'build_': 'Xây dựng',
        'parse_': 'Phân tích', 'call_': 'Gọi', 'generate_': 'Sinh',
        'create_': 'Tạo', 'init_': 'Khởi tạo',
    }
    verb = 'Xử lý'
    matched_key = None
    stripped_name = name.lstrip('_')
    multi_verbs = ['filter_by', 'setup_', 'build_', 'parse_', 'call_', 'generate_', 'create_', 'init_']
    for key in multi_verbs:
        if stripped_name.startswith(key):
            verb = verbs.get(key.rstrip('_'), 'Xử lý')
            matched_key = key
            break
    if not matched_key:
        for key, v in verbs.items():
            if stripped_name.startswith(key) or stripped_name == key:
                verb = v
                matched_key = key
                break

    clean = stripped_name
    if matched_key and clean.startswith(matched_key):
        clean = clean[len(matched_key):]
    clean = clean.replace('_', ' ').strip()

    # Purpose inference — ưu tiên theo tên hàm, sau đó constructs
    purpose = ''
    if 'call' in stripped_name or 'fetch' in stripped_name or 'request' in stripped_name:
        purpose = 'gọi API bên ngoài'
    elif 'generate' in stripped_name:
        purpose = 'sinh câu hỏi trắc nghiệm'
    elif 'save' in stripped_name:
        purpose = 'lưu dữ liệu ra file'
    elif 'load' in stripped_name:
        purpose = 'đọc dữ liệu từ file'
    elif 'filter' in stripped_name:
        purpose = 'lọc theo điều kiện'
    elif 'parse' in stripped_name:
        purpose = 'chuyển JSON thành đối tượng'
    elif 'setup' in stripped_name:
        purpose = 'dựng giao diện người dùng'
    elif 'generate_questions' in constructs or 'generate' in constructs:
        purpose = 'sinh câu hỏi trắc nghiệm'
    elif 'save' in constructs:
        purpose = 'lưu kết quả'
    elif 'load' in constructs:
        purpose = 'đọc dữ liệu đã lưu'
    elif 'insert' in constructs or 'delete' in constructs:
        purpose = 'cập nhật giao diện hiển thị'
    elif 'get' in constructs:
        purpose = 'đọc input từ người dùng'
    elif 'dumps' in constructs or 'loads' in constructs:
        purpose = 'xử lý dữ liệu JSON'
    elif 'write_text' in constructs or 'read_text' in constructs:
        purpose = 'đọc/ghi file'
    elif 'f_string' in constructs:
        purpose = 'tạo chuỗi template'

    # Build description — tránh lặp verb (vd: "Sinh — sinh câu hỏi")
    purpose_verb = purpose.split(' ')[0] if purpose else ''
    verb_repeats = purpose_verb and (purpose_verb.lower() in verb.lower() or verb.lower() in purpose_verb.lower())

    if verb_repeats:
        # Purpose đã chứa verb → dùng purpose làm mô tả chính
        base = purpose
        if arg_str:
            base += f" với tham số: {arg_str}"
    else:
        if not clean:
            base = verb
        else:
            base = f"{verb} {clean}"
        if arg_str:
            base += f" với tham số: {arg_str}"
        if purpose:
            base += f" — {purpose}"
    if parent_class:
        base += f" (thuộc {parent_class})"
    return base


def analyze_file(file_path: Path) -> List[dict]:
    """Parse a Python file, return implement nodes with their constructs."""
    try:
        src = file_path.read_text(encoding='utf-8')
        tree = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"[WARN] Cannot parse {file_path}: {e}")
        return []

    implements = []

    # Track parent class for methods
    parent_class = ''
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Class itself is an implement
            implements.append(_analyze_impl(node, file_path, ''))
            parent_class = node.name
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef) and not (sub.name.startswith('__') and sub.name.endswith('__')):
                    implements.append(_analyze_impl(sub, file_path, parent_class))
        elif isinstance(node, ast.FunctionDef) and not (node.name.startswith('__') and node.name.endswith('__')):
            # Top-level function (not inside class)
            if not _is_inside_class(node, tree):
                implements.append(_analyze_impl(node, file_path, ''))

    return implements


def _is_inside_class(node, tree) -> bool:
    """Check if a function node is inside a class body."""
    for cls in ast.walk(tree):
        if isinstance(cls, ast.ClassDef):
            for sub in cls.body:
                if sub is node:
                    return True
    return False


def _analyze_impl(node, file_path: Path, parent_class: str) -> dict:
    """Analyze a single function/class node into an implement dict."""
    constructs = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            if isinstance(sub.func, ast.Attribute):
                constructs.add(f'{sub.func.attr}()')
            elif isinstance(sub.func, ast.Name):
                constructs.add(f'{sub.func.id}()')
        elif isinstance(sub, ast.AnnAssign):
            constructs.add('type_hint')
        elif isinstance(sub, ast.JoinedStr):
            constructs.add('f_string')
        elif isinstance(sub, ast.ListComp):
            constructs.add('list_comp')
        elif isinstance(sub, ast.Try):
            constructs.add('try_except')
        elif isinstance(sub, ast.If):
            constructs.add('if')
        elif isinstance(sub, ast.For):
            constructs.add('for')
        elif isinstance(sub, (ast.Import, ast.ImportFrom)):
            constructs.add('import')
        elif isinstance(sub, ast.Assign):
            constructs.add('assign')

    # Filter noise
    constructs = {c for c in constructs if c not in PY_NOISE}

    # Track function calls (for phase propagation via call graph)
    calls = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            if isinstance(sub.func, ast.Name):
                calls.add(sub.func.id)
            elif isinstance(sub.func, ast.Attribute):
                calls.add(sub.func.attr)

    # Build description: docstring > heuristic
    description = ''
    if ast.get_docstring(node):
        doc = ast.get_docstring(node).strip()
        description = doc.split('\n')[0].strip()
    else:
        description = build_description(node, parent_class)

    # Capture source text (for mock detection — comment signals)
    try:
        src_text = ast.get_source_segment(open(file_path, encoding='utf-8').read(), node) or ''
    except Exception:
        src_text = ''

    imp = {
        'name': node.name,
        'kind': 'class' if isinstance(node, ast.ClassDef) else 'function',
        'file': str(file_path),
        'constructs': sorted(constructs),
        'calls': sorted(calls),
        'description': description,
        'source': src_text,
    }
    # Assign phase theo mức độ hoàn thiện sản phẩm (vertical slicing)
    imp['phase'] = assign_phase(imp)
    imp['phase_label'] = PHASE_NAMES[imp['phase']]
    return imp


# ============================================================================
# SWIFT ANALYSIS (regex-based, tương tự instruction_code_extractor.py)
# ============================================================================

import re as _re

# Swift declaration patterns
SWIFT_TYPE_RE = _re.compile(
    r'^[ \t]*(?:(?:public|private|internal|open|fileprivate|final|indirect)\s+)*'
    r'(class|struct|enum|protocol)\s+(\w+)',
    _re.MULTILINE
)
SWIFT_FUNC_RE = _re.compile(
    r'^[ \t]*(?:(?:public|private|internal|open|fileprivate|static|class|final)\s+)*'
    r'func\s+(\w+)\s*\(',
    _re.MULTILINE
)

# Swift constructs to detect (keywords + API calls)
SWIFT_CONSTRUCT_RE = {
    'import': _re.compile(r'\bimport\s+\w+'),
    'class': _re.compile(r'\bclass\s+\w+'),
    'struct': _re.compile(r'\bstruct\s+\w+'),
    'enum': _re.compile(r'\benum\s+\w+'),
    'protocol': _re.compile(r'\bprotocol\s+\w+'),
    'var': _re.compile(r'\bvar\s+\w+'),
    'let': _re.compile(r'\blet\s+\w+'),
    'func': _re.compile(r'\bfunc\s+\w+'),
    'guard': _re.compile(r'\bguard\s+'),
    'if': _re.compile(r'\bif\s+'),
    'for': _re.compile(r'\bfor\s+'),
    'switch': _re.compile(r'\bswitch\s+'),
    'try': _re.compile(r'\btry\s*[?!]?'),
    'catch': _re.compile(r'\bcatch\s*'),
    'async': _re.compile(r'\basync\s+'),
    'await': _re.compile(r'\bawait\s+'),
    'optional': _re.compile(r'\b\w+\?\b'),
    'map': _re.compile(r'\.map\s*\('),
    'filter': _re.compile(r'\.filter\s*\('),
    'reduce': _re.compile(r'\.reduce\s*\('),
    'JSONDecoder': _re.compile(r'\bJSONDecoder\b'),
    'JSONEncoder': _re.compile(r'\bJSONEncoder\b'),
    'Codable': _re.compile(r'\bCodable\b'),
    'URLSession': _re.compile(r'\bURLSession\b'),
    'dataTask': _re.compile(r'\.dataTask\s*\('),
    'UserDefaults': _re.compile(r'\bUserDefaults\b'),
    'ObservableObject': _re.compile(r'\bObservableObject\b'),
    '@Published': _re.compile(r'@Published'),
    'View': _re.compile(r'\bView\b'),
    'body': _re.compile(r'\bvar\s+body\s*:'),
    'NavigationView': _re.compile(r'\bNavigationView\b'),
    'List': _re.compile(r'\bList\s*\('),
    'ForEach': _re.compile(r'\bForEach\s*\('),
    'Button': _re.compile(r'\bButton\s*\('),
    'TextField': _re.compile(r'\bTextField\s*\('),
    '@State': _re.compile(r'@State'),
    '@Binding': _re.compile(r'@Binding'),
    'UIKit': _re.compile(r'\bUIKit\b'),
    'UIViewController': _re.compile(r'\bUIViewController\b'),
    'UITableView': _re.compile(r'\bUITableView\b'),
    'UICollectionView': _re.compile(r'\bUICollectionView\b'),
    'DispatchQueue': _re.compile(r'\bDispatchQueue\b'),
    'Task': _re.compile(r'\bTask\s*\{'),
    'MainActor': _re.compile(r'\bMainActor\b'),
    'Combine': _re.compile(r'\bCombine\b'),
    'sink': _re.compile(r'\.sink\s*\('),
    'deinit': _re.compile(r'\bdeinit\b'),
    'weak': _re.compile(r'\bweak\s+'),
    'unowned': _re.compile(r'\bunowned\s+'),
    'extension': _re.compile(r'\bextension\s+\w+'),
    'generic': _re.compile(r'<\w+(?:,\s*\w+)*>'),
    'associatedtype': _re.compile(r'\bassociatedtype\b'),
    'actor': _re.compile(r'\bactor\s+\w+'),
    'Sendable': _re.compile(r'\bSendable\b'),
}


def analyze_swift_file(file_path: Path) -> List[dict]:
    """Parse Swift file: extract types + functions with constructs."""
    try:
        src = file_path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError) as e:
        print(f"[WARN] Cannot read {file_path}: {e}")
        return []

    implements = []
    lines = src.split('\n')

    # Detect types (class/struct/enum/protocol)
    for m in SWIFT_TYPE_RE.finditer(src):
        kind = m.group(1)
        name = m.group(2)
        start_line = src[:m.start()].count('\n')
        end_line = _find_swift_block_end(lines, start_line)
        block = '\n'.join(lines[start_line:end_line + 1])
        constructs = _detect_swift_constructs(block)
        description = _swift_description(kind, name, block)
        imp = {
            'name': name,
            'kind': 'class',
            'file': str(file_path),
            'constructs': sorted(constructs),
            'calls': [],
            'description': description,
        }
        imp['phase'] = assign_phase(imp)
        imp['phase_label'] = PHASE_NAMES[imp['phase']]
        implements.append(imp)

    # Detect functions (top-level + methods) — skip private/internal (noise)
    for m in SWIFT_FUNC_RE.finditer(src):
        name = m.group(1)
        # Skip test helpers, private/internal, and common noise
        if name in ('setUp', 'tearDown', 'setUpWithError', 'tearDownWithError'):
            continue
        if name.startswith('_') or name.startswith('test'):
            continue
        start_line = src[:m.start()].count('\n')
        end_line = _find_swift_block_end(lines, start_line)
        block = '\n'.join(lines[start_line:end_line + 1])
        constructs = _detect_swift_constructs(block)
        description = _swift_description('func', name, block)
        imp = {
            'name': name,
            'kind': 'function',
            'file': str(file_path),
            'constructs': sorted(constructs),
            'calls': [],
            'description': description,
        }
        imp['phase'] = assign_phase(imp)
        imp['phase_label'] = PHASE_NAMES[imp['phase']]
        implements.append(imp)

    return implements


def _find_swift_block_end(lines: List[str], start_line: int) -> int:
    """Find matching closing brace for a declaration."""
    depth = 0
    i = start_line
    while i < len(lines):
        for ch in lines[i]:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return start_line


def _detect_swift_constructs(block: str) -> Set[str]:
    """Detect Swift constructs in a code block."""
    constructs = set()
    for key, pattern in SWIFT_CONSTRUCT_RE.items():
        if pattern.search(block):
            constructs.add(key)
    return constructs


def _swift_description(kind: str, name: str, block: str) -> str:
    """Build description for Swift type/function."""
    if kind in ('class', 'struct', 'enum', 'protocol'):
        methods = SWIFT_FUNC_RE.findall(block)
        if methods:
            return f"Định nghĩa {kind} {name} với phương thức: {', '.join(methods[:6])}"
        return f"Định nghĩa {kind} {name}"
    verbs = {
        'load': 'Đọc dữ liệu', 'save': 'Lưu dữ liệu', 'fetch': 'Tải dữ liệu',
        'send': 'Gửi dữ liệu', 'get': 'Lấy dữ liệu', 'set': 'Thiết lập',
        'create': 'Tạo', 'build': 'Xây dựng', 'update': 'Cập nhật',
        'delete': 'Xóa', 'handle': 'Xử lý', 'configure': 'Cấu hình',
        'setup': 'Thiết lập', 'init': 'Khởi tạo', 'connect': 'Kết nối',
        'disconnect': 'Ngắt kết nối', 'subscribe': 'Đăng ký', 'publish': 'Phát hành',
    }
    verb = 'Xử lý'
    matched = None
    for key, v in verbs.items():
        if name.startswith(key):
            verb = v
            matched = key
            break
    clean = name
    if matched and clean.startswith(matched):
        clean = clean[len(matched):]
    clean = clean.replace('_', ' ').strip()
    if not clean:
        return verb
    return f"{verb} {clean}"


# ============================================================================
# C++/ARDUINO ANALYSIS (regex-based)
# ============================================================================

CPP_TYPE_RE = _re.compile(
    r'^[ \t]*(?:(?:public|private|protected|static|inline|virtual|final)\s+)*'
    r'(class|struct|enum)\s+(\w+)',
    _re.MULTILINE
)
CPP_FUNC_RE = _re.compile(
    r'^[ \t]*(?:(?:static|inline|virtual|const|unsigned|signed|long|short|int|float|double|char|bool|void|String|uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t)\s+)+'
    r'(\w+)\s*\(',
    _re.MULTILINE
)

# C++ constructs to detect
CPP_CONSTRUCT_RE = {
    'include': _re.compile(r'#include\s*<[^>]+>'),
    'setup': _re.compile(r'\bvoid\s+setup\s*\('),
    'loop': _re.compile(r'\bvoid\s+loop\s*\('),
    'WiFi': _re.compile(r'\bWiFi\b'),
    'WebServer': _re.compile(r'\bWebServer\b'),
    'server.on': _re.compile(r'\.on\s*\('),
    'ArduinoJson': _re.compile(r'\bArduinoJson\b'),
    'deserializeJson': _re.compile(r'\bdeserializeJson\b'),
    'serializeJson': _re.compile(r'\bserializeJson\b'),
    'PubSubClient': _re.compile(r'\bPubSubClient\b'),
    'mqttClient': _re.compile(r'\bmqttClient\b'),
    'Adafruit_NeoPixel': _re.compile(r'\bAdafruit_NeoPixel\b'),
    'strip': _re.compile(r'\bstrip\b'),
    'setPixelColor': _re.compile(r'\.setPixelColor\s*\('),
    'show': _re.compile(r'\.show\s*\('),
    'delay': _re.compile(r'\bdelay\s*\('),
    'millis': _re.compile(r'\bmillis\s*\('),
    'String': _re.compile(r'\bString\b'),
    'uint8_t': _re.compile(r'\buint8_t\b'),
    'if': _re.compile(r'\bif\s*\('),
    'for': _re.compile(r'\bfor\s*\('),
    'while': _re.compile(r'\bwhile\s*\('),
    'switch': _re.compile(r'\bswitch\s*\('),
    'void': _re.compile(r'\bvoid\s+\w+'),
    'bool': _re.compile(r'\bbool\b'),
}


def analyze_cpp_file(file_path: Path) -> List[dict]:
    """Parse C++/Arduino file: extract types + functions with constructs."""
    try:
        src = file_path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError) as e:
        print(f"[WARN] Cannot read {file_path}: {e}")
        return []

    implements = []
    lines = src.split('\n')

    # Detect types
    for m in CPP_TYPE_RE.finditer(src):
        kind = m.group(1)
        name = m.group(2)
        start_line = src[:m.start()].count('\n')
        end_line = _find_swift_block_end(lines, start_line)
        block = '\n'.join(lines[start_line:end_line + 1])
        constructs = _detect_cpp_constructs(block)
        description = _cpp_description(kind, name, block)
        imp = {
            'name': name,
            'kind': 'class',
            'file': str(file_path),
            'constructs': sorted(constructs),
            'calls': [],
            'description': description,
        }
        imp['phase'] = assign_phase(imp)
        imp['phase_label'] = PHASE_NAMES[imp['phase']]
        implements.append(imp)

    # Detect functions
    for m in CPP_FUNC_RE.finditer(src):
        name = m.group(1)
        # Skip common noise
        if name in ('if', 'for', 'while', 'switch', 'return', 'sizeof'):
            continue
        start_line = src[:m.start()].count('\n')
        end_line = _find_swift_block_end(lines, start_line)
        block = '\n'.join(lines[start_line:end_line + 1])
        constructs = _detect_cpp_constructs(block)
        description = _cpp_description('func', name, block)
        imp = {
            'name': name,
            'kind': 'function',
            'file': str(file_path),
            'constructs': sorted(constructs),
            'calls': [],
            'description': description,
        }
        imp['phase'] = assign_phase(imp)
        imp['phase_label'] = PHASE_NAMES[imp['phase']]
        implements.append(imp)

    return implements


def _detect_cpp_constructs(block: str) -> Set[str]:
    """Detect C++ constructs in a code block."""
    constructs = set()
    for key, pattern in CPP_CONSTRUCT_RE.items():
        if pattern.search(block):
            constructs.add(key)
    return constructs


def _cpp_description(kind: str, name: str, block: str) -> str:
    """Build description for C++ type/function."""
    if kind in ('class', 'struct', 'enum'):
        methods = CPP_FUNC_RE.findall(block)
        if methods:
            return f"Định nghĩa {kind} {name} với phương thức: {', '.join(methods[:6])}"
        return f"Định nghĩa {kind} {name}"
    # Function
    verbs = {
        'setup': 'Khởi tạo', 'loop': 'Vòng lặp chính', 'handle': 'Xử lý',
        'publish': 'Phát hành', 'update': 'Cập nhật', 'connect': 'Kết nối',
        'get': 'Lấy dữ liệu', 'set': 'Thiết lập', 'send': 'Gửi dữ liệu',
    }
    verb = 'Xử lý'
    matched = None
    for key, v in verbs.items():
        if name.startswith(key):
            verb = v
            matched = key
            break
    clean = name
    if matched and clean.startswith(matched):
        clean = clean[len(matched):]
    clean = clean.replace('_', ' ').strip()
    if not clean:
        return verb
    return f"{verb} {clean}"


# ============================================================================
# KNOWLEDGE MAPPING
# ============================================================================

# Bloom level theo phase (vertical slicing — docs/ideas/2026-08-07-vertical-slicing-roadmap.md)
# Cùng concept có thể xuất hiện ở nhiều phase với mức nhận thức khác nhau:
#   P0 NỀN TẢNG   → remember
#   P1 MVP        → understand
#   P2 MỞ RỘNG    → apply
#   P3 HOÀN THIỆN → create
PHASE_BLOOM = {
    0: 'remember',
    1: 'understand',
    2: 'apply',
    3: 'create',
}


def map_constructs_to_knowledge(constructs: List[str], phase: int = 1) -> List[dict]:
    """Map constructs to minimal knowledge nodes (deduplicated, ordered).

    Mỗi knowledge item mang bloom_level theo phase — cùng label ở phase khác
    (mức nhận thức khác) là kiến thức MỚI, không phải trùng lặp.
    """
    knowledge = []
    seen = set()
    bloom = PHASE_BLOOM.get(phase, 'understand')
    for c in constructs:
        if c in PY_CONSTRUCT_KNOWLEDGE:
            label, note = PY_CONSTRUCT_KNOWLEDGE[c]
        elif c in SWIFT_CONSTRUCT_KNOWLEDGE:
            label, note = SWIFT_CONSTRUCT_KNOWLEDGE[c]
        elif c in CPP_CONSTRUCT_KNOWLEDGE:
            label, note = CPP_CONSTRUCT_KNOWLEDGE[c]
        else:
            continue
        # Dedup key = (label, bloom_level) — cùng label khác mức = mới
        key = (label, bloom)
        if key not in seen:
            seen.add(key)
            knowledge.append({'label': label, 'note': note, 'bloom_level': bloom})
    return knowledge


# ============================================================================
# GRAPH BUILDING
# ============================================================================


def readable_name(name: str) -> str:
    """Convert snake_case function name to readable form.
    filter_by_topic -> filter theo topic
    generate_questions -> generate questions
    _build_prompt -> build prompt
    """
    clean = name.lstrip('_')
    # Handle "by" as "theo"
    clean = clean.replace('_by_', ' theo ')
    # Handle remaining underscores as spaces
    clean = clean.replace('_', ' ')
    return clean.strip()


def build_graph(implements: List[dict], project_type: str = 'app', feature_names: dict = None,
                use_llm_bloom: bool = True) -> dict:
    """Build JIT knowledge graph: 1 main flow Start → End, phases colored.

    project_type quyết định "thấy sản phẩm" ở MVP:
    - app: UI entry point
    - cli: command chạy được
    - library: public API
    - api_service: endpoint
    """
    nodes = []
    edges = []
    node_id = 0
    prev_node = None

    def add_node(label, note, phase, node_type, x, y, extra=None):
        nonlocal node_id
        nid = f"n{node_id}"
        node_id += 1
        data = {
            'label': label,
            'note': note,
            'phase': phase,
            'nodeType': node_type,
            'color': PHASE_COLORS.get(phase, '#333'),
        }
        if extra:
            data.update(extra)
        nodes.append({
            'id': nid,
            'type': 'topic' if node_type == 'knowledge' else 'subtopic',
            'data': data,
            'position': {'x': x, 'y': y},
        })
        return nid

    # Group implements by phase (preserve order)
    by_phase = {}
    for imp in implements:
        by_phase.setdefault(imp['phase'], []).append(imp)

    # P0 (NỀN TẢNG) luôn có mặt — phase nền tảng, không phụ thuộc repo
    if 0 not in by_phase:
        by_phase[0] = [{
            'name': 'scaffold',
            'kind': 'function',
            'file': '',
            'phase': 0,
            'phase_label': 'NỀN TẢNG',
            'constructs': ['setup_python', 'run_script', 'create_project', 'git_init'],
            'description': 'Cài đặt Python, làm quen cú pháp cơ bản, chạy script đầu tiên, khởi tạo git repo sạch.',
        }]

    # START node
    start_id = add_node('START', '', 0, 'start', 0, 0)
    prev_node = start_id
    y = 0

    # Collect all knowledge items (for LLM bloom evaluation)
    all_knowledge = []
    for phase in sorted(by_phase.keys()):
        for imp in by_phase[phase]:
            for k in map_constructs_to_knowledge(imp['constructs'], imp['phase']):
                k['phase'] = phase
                all_knowledge.append(k)

    # LLM đánh giá bloom_level (hoặc heuristic theo phase nếu --no-llm-bloom)
    if use_llm_bloom:
        all_knowledge = evaluate_bloom_llm(all_knowledge, project_type)
    else:
        all_knowledge = _evaluate_bloom_heuristic(all_knowledge)
    bloom_by_label = {k['label']: k['bloom_level'] for k in all_knowledge}

    # Sort phases
    for phase in sorted(by_phase.keys()):
        phase_impls = by_phase[phase]
        phase_label = phase_impls[0]['phase_label']

        # Phase header node
        header_id = add_node(f'PHASE {phase} — {phase_label}', '', phase, 'phase', 0, y)
        edges.append({'source': prev_node, 'target': header_id, 'data': {'edgeStyle': 'solid'}})
        prev_node = header_id
        y += 100

        # For each implement: knowledge nodes → implement node
        for imp in phase_impls:
            knowledge = map_constructs_to_knowledge(imp['constructs'], imp['phase'])
            # Gán bloom từ LLM evaluation
            for k in knowledge:
                k['bloom_level'] = bloom_by_label.get(k['label'], k.get('bloom_level', 'understand'))

            # Knowledge nodes (main flow)
            for k in knowledge:
                kid = add_node(k['label'], k['note'], phase, 'knowledge', 0, y, {'bloom_level': k.get('bloom_level', 'understand')})
                edges.append({'source': prev_node, 'target': kid, 'data': {'edgeStyle': 'solid'}})
                prev_node = kid
                y += 100

            # Implement node (phase ends with implement)
            if imp['kind'] == 'class':
                imp_label = f'Tính năng tạo {imp["name"].lower()}'
            else:
                imp_label = f'Tính năng {readable_name(imp["name"])}'
            imp_note = imp.get('description', '') or f'({imp["file"].split("/")[-1]})'
            iid = add_node(imp_label, imp_note, phase, 'implement', 0, y,
                           {'feature_id': imp.get('feature_id', 0)})
            edges.append({'source': prev_node, 'target': iid, 'data': {'edgeStyle': 'solid'}})
            prev_node = iid
            y += 100

    # END node
    end_id = add_node('END', '', 0, 'end', 0, y)
    edges.append({'source': prev_node, 'target': end_id, 'data': {'edgeStyle': 'solid'}})

    return {
        'project_brief': {
            'project_code': 'JIT_GRAPH',
            'title': 'JIT Knowledge Graph',
            'description': 'Just-in-time knowledge graph: minimal knowledge per implement',
            'project_type': project_type,
            'features': feature_names or {},
        },
        'title': {'card': 'JIT Knowledge Graph', 'page': 'JIT Knowledge Graph'},
        'nodes': nodes,
        'edges': edges,
        'dimensions': {'height': y + 100, 'width': 600},
        'type': 'role',
        'status': 'published',
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='STEP 8.8: Generate JIT Knowledge Graph')
    parser.add_argument('--repo-dir', type=Path, required=True,
                       help='Repository directory to analyze')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output jit_graph.json path')
    parser.add_argument('--feature-config', type=Path, default=None,
                       help='Optional: JSON config override feature clustering '
                            '{"features": {"Tên feature": ["impl1", "impl2"]}}')
    parser.add_argument('--no-llm-bloom', action='store_true',
                       help='Bỏ qua LLM bloom evaluation, dùng heuristic theo phase (nhanh hơn)')
    args = parser.parse_args()

    if not args.repo_dir.exists():
        print(f"[ERROR] Repo not found: {args.repo_dir}")
        return 1

    # Collect source files (Python + Swift + C++)
    py_files = sorted(args.repo_dir.rglob('*.py'))
    swift_files = sorted(args.repo_dir.rglob('*.swift'))
    cpp_files = sorted(args.repo_dir.rglob('*.ino')) + sorted(args.repo_dir.rglob('*.cpp'))
    if not py_files and not swift_files and not cpp_files:
        print(f"[ERROR] No Python/Swift/C++ files in {args.repo_dir}")
        return 1

    # Detect project type (app/cli/library/api_service)
    project_type = detect_project_type(args.repo_dir)
    print(f"[*] Project type: {PROJECT_TYPES.get(project_type, project_type)}")

    print(f"[*] Analyzing {len(py_files)} Python + {len(swift_files)} Swift + {len(cpp_files)} C++ files...")

    all_implements = []
    skip_dirs = ['__pycache__', '.venv', 'venv', 'node_modules', '.build', 'Pods', 'DerivedData', '.swiftpm']
    for f in py_files:
        if any(skip in str(f) for skip in skip_dirs):
            continue
        all_implements.extend(analyze_file(f))
    for f in swift_files:
        if any(skip in str(f) for skip in skip_dirs):
            continue
        all_implements.extend(analyze_swift_file(f))
    for f in cpp_files:
        if any(skip in str(f) for skip in skip_dirs):
            continue
        all_implements.extend(analyze_cpp_file(f))

    print(f"[*] Found {len(all_implements)} implements (functions/classes)")

    # Call graph propagation: implement gọi function file I/O → P2
    propagate_phases(all_implements)

    # Feature clustering (hybrid: auto + config override)
    feature_config = None
    if args.feature_config and args.feature_config.exists():
        import json as _json
        feature_config = _json.loads(args.feature_config.read_text(encoding='utf-8'))
    feature_ids, feature_names = cluster_features(all_implements, feature_config)
    n_features = len(set(feature_ids.values()))
    print(f"[*] Features: {n_features} clusters")
    for imp in all_implements:
        imp['feature_id'] = feature_ids.get(imp['name'], 0)
        imp['feature_name'] = feature_names.get(imp['feature_id'], f'Feature {imp["feature_id"]}')

    # Build graph
    graph = build_graph(all_implements, project_type, feature_names, use_llm_bloom=not args.no_llm_bloom)

    # Save
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    # Summary
    phases = {}
    for n in graph['nodes']:
        p = n['data'].get('phase')
        if p:
            phases[p] = phases.get(p, 0) + 1

    print(f"[✓] Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    print(f"    Phases: {dict(sorted(phases.items()))}")
    print(f"    Saved to {args.output}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
