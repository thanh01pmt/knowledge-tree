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

# Python builtins that are NOT knowledge (noise)
PY_NOISE = {
    'print', 'len', 'range', 'str', 'int', 'list', 'dict', 'set', 'tuple',
    'self', 'super', 'isinstance', 'type', 'id', 'repr', 'format', 'sorted',
    'enumerate', 'zip', 'map', 'filter', 'sum', 'min', 'max', 'abs', 'round',
    'open', 'input', 'bool', 'float', 'object', 'property', 'staticmethod',
    'classmethod', 'hasattr', 'getattr', 'setattr', 'delattr', 'vars',
}

# ============================================================================
# FILE → PHASE MAPPING
# ============================================================================

# Default phase mapping by filename patterns
PHASE_BY_FILE = [
    (('setup', 'scaffold', 'init', 'env', 'docker', 'makefile', 'requirements'), 1, 'THIẾT LẬP DỰ ÁN'),
    (('model', 'models', 'storage', 'db', 'database', 'persist', 'repository', 'schema', 'bank', 'question', 'entity', 'domain'), 2, 'DATA MODEL & PERSISTENCE'),
    (('generator', 'service', 'core', 'logic', 'engine', 'ai', 'llm', 'prompt', 'agent'), 3, 'CORE LOGIC (AI/DOMAIN)'),
    (('config', 'settings', 'constant', 'env'), 4, 'CẤU HÌNH'),
    (('main', 'app', 'ui', 'view', 'window', 'screen', 'controller'), 5, 'UI'),
    (('test', 'tests', 'spec', 'run', 'benchmark'), 6, 'KIỂM THỬ & CHẠY'),
]

PHASE_COLORS = {
    1: '#2b78e4',  # blue
    2: '#27ae60',  # green
    3: '#8e44ad',  # purple
    4: '#f39c12',  # orange
    5: '#e74c3c',  # red
    6: '#16a085',  # teal
}

PHASE_NAMES = {
    1: 'THIẾT LẬP DỰ ÁN',
    2: 'DATA MODEL & PERSISTENCE',
    3: 'CORE LOGIC (AI/DOMAIN)',
    4: 'CẤU HÌNH',
    5: 'UI',
    6: 'KIỂM THỬ & CHẠY',
}


def detect_phase(file_path: Path, constructs: Set[str] = None) -> Tuple[int, str]:
    """Detect phase from filename, fallback to constructs."""
    name = file_path.stem.lower()
    # Exact filename matches take priority (main.py is always UI entry)
    if name in ('main', 'app', 'ui', 'window', 'view', 'screen'):
        return 5, PHASE_NAMES[5]
    if name in ('config', 'settings', 'constants'):
        return 4, PHASE_NAMES[4]
    if name.startswith('test') or name.endswith('_test') or name.endswith('_spec'):
        return 6, PHASE_NAMES[6]
    for patterns, phase, label in PHASE_BY_FILE:
        if any(p in name for p in patterns):
            return phase, label

    # Fallback: detect from constructs (content-based)
    if constructs:
        # UI constructs → phase 5
        if any(c in constructs for c in ['Tk()', 'Entry()', 'Button()', 'Text()', 'pack()', 'mainloop()']):
            return 5, PHASE_NAMES[5]
        # Data constructs → phase 2
        if any(c in constructs for c in ['asdict()', 'dumps()', 'loads()', 'Path()', 'read_text()', 'write_text()']):
            return 2, PHASE_NAMES[2]
        # Config constructs → phase 4
        if 'getenv()' in constructs and 'import' in constructs:
            return 4, PHASE_NAMES[4]
        # Test constructs → phase 6
        if any(c in constructs for c in ['assertEqual()', 'assertTrue()', 'setUp()', 'mock()']):
            return 6, PHASE_NAMES[6]

    return 3, PHASE_NAMES[3]  # default: core logic


# ============================================================================
# AST ANALYSIS
# ============================================================================


def build_description(node) -> str:
    """Build a natural description from name, params, and fields."""
    name = node.name
    # Class: describe from fields
    if isinstance(node, ast.ClassDef):
        fields = []
        for sub in node.body:
            if isinstance(sub, ast.AnnAssign) and isinstance(sub.target, ast.Name):
                fields.append(sub.target.id)
        if fields:
            return f"Định nghĩa {name} với các trường: {', '.join(fields)}"
        return f"Định nghĩa class {name}"
    # Function: describe from name + params
    args = []
    if node.args.args:
        args = [a.arg for a in node.args.args if a.arg != 'self']
    arg_str = ', '.join(args) if args else ''
    # Verb mapping from function name
    verbs = {
        'save': 'Lưu dữ liệu',
        'load': 'Đọc dữ liệu',
        'get': 'Lấy dữ liệu',
        'set': 'Thiết lập',
        'create': 'Tạo',
        'build': 'Xây dựng',
        'generate': 'Sinh',
        'parse': 'Phân tích',
        'filter': 'Lọc',
        'call': 'Gọi',
        'init': 'Khởi tạo',
        'setup': 'Thiết lập',
        'run': 'Chạy',
        'main': 'Khởi chạy',
        'delete': 'Xóa',
        'insert': 'Chèn',
        'update': 'Cập nhật',
        'validate': 'Kiểm tra',
        'convert': 'Chuyển đổi',
        'format': 'Định dạng',
        'filter_by': 'Lọc',
        'setup_': 'Thiết lập',
        'build_': 'Xây dựng',
        'parse_': 'Phân tích',
        'call_': 'Gọi',
        'generate_': 'Sinh',
        'create_': 'Tạo',
        'init_': 'Khởi tạo',
    }
    verb = 'Xử lý'
    matched_key = None
    # Strip leading underscores for verb matching (e.g. _build_prompt -> build_prompt)
    stripped_name = name.lstrip('_')
    # Match multi-word verbs first (filter_by, setup_, build_, parse_, call_)
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
    # Remove the matched verb prefix from the name to avoid repetition
    clean = stripped_name
    if matched_key and clean.startswith(matched_key):
        clean = clean[len(matched_key):]
    clean = clean.replace('_', ' ').strip()
    if not clean:
        # No remainder after verb -> just the verb (e.g. "Lưu dữ liệu")
        if arg_str:
            return f"{verb} với tham số: {arg_str}"
        return verb
    if arg_str:
        return f"{verb} {clean} với tham số: {arg_str}"
    return f"{verb} {clean}"


def analyze_file(file_path: Path) -> List[dict]:
    """Parse a Python file, return implement nodes with their constructs."""
    try:
        src = file_path.read_text(encoding='utf-8')
        tree = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"[WARN] Cannot parse {file_path}: {e}")
        return []

    implements = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('__') and node.name.endswith('__'):
                continue  # skip dunder

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

            # Detect phase from filename + constructs
            phase, phase_label = detect_phase(file_path, constructs)

            # Build description: docstring > heuristic from name/params/fields
            description = ''
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and ast.get_docstring(node):
                doc = ast.get_docstring(node).strip()
                description = doc.split('\n')[0].strip()
            else:
                description = build_description(node)

            implements.append({
                'name': node.name,
                'kind': 'class' if isinstance(node, ast.ClassDef) else 'function',
                'file': str(file_path),
                'phase': phase,
                'phase_label': phase_label,
                'constructs': sorted(constructs),
                'description': description,
            })

    return implements


# ============================================================================
# KNOWLEDGE MAPPING
# ============================================================================

def map_constructs_to_knowledge(constructs: List[str]) -> List[dict]:
    """Map constructs to minimal knowledge nodes (deduplicated, ordered)."""
    knowledge = []
    seen = set()
    for c in constructs:
        if c in PY_CONSTRUCT_KNOWLEDGE:
            label, note = PY_CONSTRUCT_KNOWLEDGE[c]
            if label not in seen:
                seen.add(label)
                knowledge.append({'label': label, 'note': note})
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


def build_graph(implements: List[dict]) -> dict:
    """Build JIT knowledge graph: 1 main flow Start → End, phases colored."""
    nodes = []
    edges = []
    node_id = 0
    prev_node = None

    def add_node(label, note, phase, node_type, x, y):
        nonlocal node_id
        nid = f"n{node_id}"
        node_id += 1
        nodes.append({
            'id': nid,
            'type': 'topic' if node_type == 'knowledge' else 'subtopic',
            'data': {
                'label': label,
                'note': note,
                'phase': phase,
                'nodeType': node_type,
                'color': PHASE_COLORS.get(phase, '#333'),
            },
            'position': {'x': x, 'y': y},
        })
        return nid

    # Group implements by phase (preserve order)
    by_phase = {}
    for imp in implements:
        by_phase.setdefault(imp['phase'], []).append(imp)

    # Phase 1 (THIẾT LẬP) is always present — foundation phase
    if 1 not in by_phase:
        by_phase[1] = [{
            'name': 'scaffold',
            'kind': 'function',
            'file': '',
            'phase': 1,
            'phase_label': 'THIẾT LẬP DỰ ÁN',
            'constructs': ['setup_python', 'run_script', 'create_project', 'git_init'],
            'description': 'Tạo cấu trúc thư mục dự án, khởi tạo môi trường và git repo sạch.',
        }]

    # START node
    start_id = add_node('START', '', 0, 'start', 0, 0)
    prev_node = start_id
    y = 0

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
            knowledge = map_constructs_to_knowledge(imp['constructs'])

            # Knowledge nodes (main flow)
            for k in knowledge:
                kid = add_node(k['label'], k['note'], phase, 'knowledge', 0, y)
                edges.append({'source': prev_node, 'target': kid, 'data': {'edgeStyle': 'solid'}})
                prev_node = kid
                y += 100

            # Implement node (phase ends with implement)
            if imp['kind'] == 'class':
                imp_label = f'Tính năng tạo {imp["name"].lower()}'
            else:
                imp_label = f'Tính năng {readable_name(imp["name"])}'
            imp_note = imp.get('description', '') or f'({imp["file"].split("/")[-1]})'
            iid = add_node(imp_label, imp_note, phase, 'implement', 0, y)
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
    args = parser.parse_args()

    if not args.repo_dir.exists():
        print(f"[ERROR] Repo not found: {args.repo_dir}")
        return 1

    # Collect all Python files
    py_files = sorted(args.repo_dir.rglob('*.py'))
    if not py_files:
        print(f"[ERROR] No Python files in {args.repo_dir}")
        return 1

    print(f"[*] Analyzing {len(py_files)} Python files...")

    all_implements = []
    for f in py_files:
        if any(skip in str(f) for skip in ['__pycache__', '.venv', 'venv', 'node_modules']):
            continue
        implements = analyze_file(f)
        all_implements.extend(implements)

    print(f"[*] Found {len(all_implements)} implements (functions/classes)")

    # Build graph
    graph = build_graph(all_implements)

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
