#!/usr/bin/env python3
"""
STEP 8.5: Extract code snippets from repository for instruction generation.

Parses source files (Python AST, Swift regex, TypeScript/JavaScript regex),
extracts relevant code snippets for each SIO, and outputs a structured JSON
for instruction generation.

Usage:
    python scripts/instruction_code_extractor.py \
        --repo-dir /tmp/repo \
        --sios-file /tmp/resolved_sios.json \
        --output /tmp/code_snippets.json

Input:
    - Repository directory with source code
    - resolved_sios.json from STEP 5

Output:
    - code_snippets.json with extracted snippets per SIO
"""

import ast
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional
import sys


# ============================================================================
# PYTHON PARSER (AST-based)
# ============================================================================

class CodeExtractor(ast.NodeVisitor):
    """AST visitor to extract code snippets from Python."""

    def __init__(self):
        self.snippets = []
        self.current_class = None
        self.source_lines = []

    def set_source(self, source: str):
        """Set source code for line extraction."""
        self.source_lines = source.splitlines()

    def get_snippet(self, node: ast.AST, context_lines: int = 3) -> str:
        """Extract code snippet with surrounding context."""
        start_line = max(0, node.lineno - 1 - context_lines)
        end_line = min(len(self.source_lines), node.end_lineno + context_lines)
        return '\n'.join(self.source_lines[start_line:end_line])

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Extract function definitions."""
        snippet = {
            'type': 'function',
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'code': self.get_snippet(node, context_lines=2),
            'docstring': ast.get_docstring(node),
            'args': [arg.arg for arg in node.args.args],
            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
        }
        if self.current_class:
            snippet['class'] = self.current_class
        self.snippets.append(snippet)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Extract async function definitions."""
        snippet = {
            'type': 'async_function',
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'code': self.get_snippet(node, context_lines=2),
            'docstring': ast.get_docstring(node),
            'args': [arg.arg for arg in node.args.args],
            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
        }
        if self.current_class:
            snippet['class'] = self.current_class
        self.snippets.append(snippet)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Extract class definitions."""
        old_class = self.current_class
        self.current_class = node.name

        snippet = {
            'type': 'class',
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'code': self.get_snippet(node, context_lines=3),
            'docstring': ast.get_docstring(node),
            'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
        }
        self.snippets.append(snippet)
        self.generic_visit(node)
        self.current_class = old_class


def extract_python_snippets(source: str, file_path: Path) -> List[Dict]:
    """Extract code snippets from Python source."""
    try:
        tree = ast.parse(source, filename=str(file_path))
        extractor = CodeExtractor()
        extractor.set_source(source)
        extractor.visit(tree)
        for snippet in extractor.snippets:
            snippet['file'] = str(file_path)
        return extractor.snippets
    except SyntaxError as e:
        print(f"[WARN] Failed to parse {file_path}: {e}")
        return []


# ============================================================================
# GENERIC REGEX-BASED PARSER (Swift / TypeScript / JavaScript)
# ============================================================================

# Declaration patterns per language
# Each pattern: (regex, kind, name_group) — captures the declaration header.
LANG_PATTERNS = {
    'swift': {
        # `class Name: Protocol {`, `struct Name {`, `enum Name {`, `protocol Name {`
        'type': re.compile(
            r'^[ \t]*(?:(?:public|private|internal|open|fileprivate|final|indirect)\s+)*'
            r'(class|struct|enum|protocol)\s+(\w+)',
            re.MULTILINE
        ),
        # `func name(args) -> Ret {`, `func name(args) async throws -> Ret {`
        'function': re.compile(
            r'^[ \t]*(?:(?:public|private|internal|open|fileprivate|static|class|final)\s+)*'
            r'func\s+(\w+)\s*\(',
            re.MULTILINE
        ),
    },
    'javascript': {
        # `class Name {`, `class Name extends Base {`
        'type': re.compile(
            r'^[ \t]*(?:export\s+|default\s+|abstract\s+)*class\s+(\w+)',
            re.MULTILINE
        ),
        # `function name(args) {`, `async function name(args) {`
        'function': re.compile(
            r'^[ \t]*(?:export\s+|default\s+|async\s+)*function\s+(\w+)\s*\(',
            re.MULTILINE
        ),
        # Class methods: `name(args) {`, `async name(args) {`, `static name(args) {`
        # Excludes control-flow keywords and closure assignments
        'method': re.compile(
            r'^[ \t]*(?!if\b|for\b|while\b|switch\b|catch\b|return\b|const\b|let\b|var\b|function\b|class\b|import\b|export\b|throw\b|new\b|break\b|continue\b)'
            r'(?:async\s+|static\s+|get\s+|set\s+)*(\w+)\s*\(',
            re.MULTILINE
        ),
    },
    'cpp': {
        # `class Name {`, `struct Name {`, `enum Name {`
        'type': re.compile(
            r'^[ \t]*(?:(?:public|private|protected|static|inline|virtual|final)\s+)*'
            r'(class|struct|enum)\s+(\w+)',
            re.MULTILINE
        ),
        # `void setup() {`, `void loop() {`, `int handleX() {`, `void handleY() {`
        'function': re.compile(
            r'^[ \t]*(?:(?:static|inline|virtual|const|unsigned|signed|long|short|int|float|double|char|bool|void|String|uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t)\s+)+'
            r'(\w+)\s*\(',
            re.MULTILINE
        ),
    },
    'typescript': {
        # `class Name {`, `interface Name {`, `enum Name {`, `type Name = ...`
        'type': re.compile(
            r'^[ \t]*(?:export\s+|default\s+|abstract\s+)*(?:class|interface|enum)\s+(\w+)',
            re.MULTILINE
        ),
        # `function name(args) {`, `async function name(args) {`
        'function': re.compile(
            r'^[ \t]*(?:export\s+|default\s+|async\s+)*function\s+(\w+)\s*\(',
            re.MULTILINE
        ),
        # Class methods + interface method signatures: `name(args): Ret {`
        'method': re.compile(
            r'^[ \t]*(?!if\b|for\b|while\b|switch\b|catch\b|return\b|const\b|let\b|var\b|function\b|class\b|interface\b|enum\b|import\b|export\b|throw\b|new\b|break\b|continue\b)'
            r'(?:async\s+|static\s+|get\s+|set\s+|readonly\s+|public\s+|private\s+|protected\s+)*(\w+)\s*\(',
            re.MULTILINE
        ),
    },
}


def _find_block_end(lines: List[str], start_line: int) -> int:
    """Given a declaration start line, return the matching closing brace line.

    Tracks brace depth ignoring braces inside string literals (simple heuristic).
    """
    depth = 0
    i = start_line
    in_string = None  # None | single | double | backtick
    while i < len(lines):
        line = lines[i]
        j = 0
        while j < len(line):
            ch = line[j]
            if in_string:
                # Handle escapes
                if ch == '\\' and j + 1 < len(line):
                    j += 2
                    continue
                if (in_string == 'single' and ch == "'") or \
                   (in_string == 'double' and ch == '"') or \
                   (in_string == 'backtick' and ch == '`'):
                    in_string = None
                j += 1
                continue
            if ch in ('"', "'", '`'):
                in_string = 'single' if ch == "'" else ('double' if ch == '"' else 'backtick')
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i
            j += 1
        i += 1
    return start_line  # fallback: no closing brace found


def _generic_extract_snippets(source: str, file_path: Path, lang: str) -> List[Dict]:
    """Extract function/type snippets using regex + brace counting."""
    patterns = LANG_PATTERNS.get(lang)
    if not patterns:
        return []

    lines = source.splitlines()
    snippets = []
    seen = set()  # (kind, name, start_line) to avoid duplicates

    for kind in ('type', 'function', 'method'):
        pattern = patterns.get(kind)
        if not pattern:
            continue
        for match in pattern.finditer(source):
            name = match.group(1)
            # Compute line number (0-indexed) of the match
            line_start = source.count('\n', 0, match.start())
            if line_start >= len(lines):
                continue

            # For methods, only keep declarations (line ends with '{' or '}'
            # i.e. a block), not bare function calls like `clearTimeout(timer);`
            decl_line = lines[line_start].strip()
            if kind == 'method' and not (decl_line.endswith('{') or decl_line.endswith('}')):
                continue

            key = (kind, name, line_start)
            if key in seen:
                continue
            seen.add(key)

            line_end = _find_block_end(lines, line_start)
            if line_end < line_start:
                continue

            # Extract declaration + body (with 1 line context padding)
            ctx_start = max(0, line_start - 1)
            ctx_end = min(len(lines), line_end + 1)
            code = '\n'.join(lines[ctx_start:ctx_end])

            snippet = {
                'type': kind,
                'name': name,
                'line_start': line_start + 1,  # 1-indexed for consistency
                'line_end': line_end + 1,
                'code': code,
                'docstring': None,  # not extracted for regex path
                'file': str(file_path),
            }
            snippets.append(snippet)

    return snippets


# ============================================================================
# FILE DISPATCH
# ============================================================================

# Skip directories that are never source code
SKIP_DIR_PARTS = {
    '__pycache__', '.git', 'node_modules', 'venv', '.venv', 'dist', 'build',
    '.build', '.next', '.nuxt', 'Pods', 'DerivedData', '.swiftpm',
    'assets', 'fonts', 'images', 'Pods', 'xcuserdata', '.git-annex',
}

# Extension → parser dispatch
EXT_LANG_MAP = {
    '.py': 'python',
    '.swift': 'swift',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.mjs': 'javascript',
    '.cjs': 'javascript',
    '.ino': 'cpp',
    '.cpp': 'cpp',
    '.h': 'cpp',
    '.c': 'cpp',
}


def _should_skip(path: Path) -> bool:
    """Return True if the file path should be skipped."""
    for part in path.parts:
        if part in SKIP_DIR_PARTS:
            return True
    return False


def extract_snippets_from_file(file_path: Path) -> List[Dict]:
    """Extract code snippets from a single source file (dispatch by extension)."""
    ext = file_path.suffix.lower()
    lang = EXT_LANG_MAP.get(ext)
    if not lang:
        return []

    try:
        source = file_path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return []

    if lang == 'python':
        return extract_python_snippets(source, file_path)
    return _generic_extract_snippets(source, file_path, lang)


def extract_all_snippets(repo_dir: Path) -> List[Dict]:
    """Extract code snippets from all supported source files in repository."""
    all_snippets = []

    for file_path in repo_dir.rglob('*'):
        if not file_path.is_file():
            continue
        if _should_skip(file_path):
            continue

        snippets = extract_snippets_from_file(file_path)
        all_snippets.extend(snippets)

    return all_snippets


# ============================================================================
# SIO FLATTENING & MATCHING
# ============================================================================

def flatten_sios(resolved_sios: List[Dict]) -> List[Dict]:
    """Flatten nested SIO structure from resolved_sios.json into simple list."""
    flattened = []

    for sio_group in resolved_sios:
        action = sio_group.get('action', 'UNKNOWN')
        cio_code = sio_group.get('cio_code', '')

        # Handle REUSE action - has 'sios' list
        if action == 'REUSE' and 'sios' in sio_group:
            for sio in sio_group['sios']:
                flattened.append({
                    'code': sio.get('code', ''),
                    'name': sio.get('name', ''),
                    'concept_codes': sio.get('concept_codes', ''),
                    'action': action,
                    'cio_code': cio_code
                })

        # Handle ADAPT action - has 'source_sio'
        elif action == 'ADAPT' and 'source_sio' in sio_group:
            source = sio_group['source_sio']
            flattened.append({
                'code': source.get('code', ''),
                'name': source.get('name', ''),
                'concept_codes': source.get('concept_codes', ''),
                'action': action,
                'cio_code': cio_code
            })

        # Handle GENERATE action - no existing SIO
        elif action == 'GENERATE':
            # Add placeholder for GENERATE
            flattened.append({
                'code': f"NEW-{cio_code}",
                'name': f"New SIO for {cio_code}",
                'concept_codes': '',
                'action': action,
                'cio_code': cio_code
            })

    return flattened


def match_snippets_to_sios(snippets: List[Dict], sios: List[Dict]) -> Dict[str, List[Dict]]:
    """Match code snippets to SIOs based on concept codes and keywords."""
    matched = {}

    for sio in sios:
        sio_code = sio.get('code', '')
        sio_name = sio.get('name', '').lower()
        concept_codes = sio.get('concept_codes', '').split(',')

        # Extract keywords from SIO name
        keywords = set(word.lower() for word in sio_name.split() if len(word) > 3)

        matching_snippets = []

        for snippet in snippets:
            # Check if snippet matches by name or keywords
            snippet_name = snippet.get('name', '').lower()
            snippet_code = snippet.get('code', '').lower()

            # Score based on keyword overlap
            score = 0

            # Check name match
            if any(kw in snippet_name for kw in keywords):
                score += 2

            # Check code content match
            if any(kw in snippet_code for kw in keywords):
                score += 1

            # Check concept code match
            if any(cc.strip().lower() in snippet_code for cc in concept_codes if cc.strip()):
                score += 1

            if score > 0:
                snippet_copy = snippet.copy()
                snippet_copy['match_score'] = score
                matching_snippets.append(snippet_copy)

        # Sort by score and take top 5
        matching_snippets.sort(key=lambda x: x['match_score'], reverse=True)
        matched[sio_code] = matching_snippets[:5]

    return matched


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Extract code snippets from repository')
    parser.add_argument('--repo-dir', type=Path, required=True,
                       help='Repository directory to extract snippets from')
    parser.add_argument('--sios-file', type=Path, required=True,
                       help='Path to resolved_sios.json from STEP 5')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output JSON file for code snippets')

    args = parser.parse_args()

    # Validate inputs
    if not args.repo_dir.exists():
        print(f"[ERROR] Repository directory not found: {args.repo_dir}")
        return 1

    if not args.sios_file.exists():
        print(f"[ERROR] SIOs file not found: {args.sios_file}")
        return 1

    # Load SIOs
    with open(args.sios_file, 'r', encoding='utf-8') as f:
        sios_data = json.load(f)

    resolved_sios = sios_data.get('resolved_sios', [])
    print(f"[*] Loaded {len(resolved_sios)} SIO groups")

    # Flatten nested SIO structure
    sios = flatten_sios(resolved_sios)
    print(f"[*] Flattened to {len(sios)} individual SIOs")

    # Extract snippets
    print(f"[*] Extracting code snippets from {args.repo_dir}")
    snippets = extract_all_snippets(args.repo_dir)
    print(f"[*] Extracted {len(snippets)} snippets")

    # Match snippets to SIOs
    print("[*] Matching snippets to SIOs")
    matched = match_snippets_to_sios(snippets, sios)

    # Calculate statistics
    total_matched = sum(len(snips) for snips in matched.values())
    sios_with_snippets = sum(1 for snips in matched.values() if snips)

    print(f"[*] Matched {total_matched} snippets to {sios_with_snippets}/{len(sios)} SIOs")

    # Save output
    output = {
        'repository': str(args.repo_dir),
        'total_snippets': len(snippets),
        'total_matched': total_matched,
        'sios_with_snippets': sios_with_snippets,
        'matched_snippets': matched
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Code snippets saved to {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())