#!/usr/bin/env python3
"""
STEP 8.5: Extract code snippets from repository for instruction generation.

Parses source files using AST, extracts relevant code snippets for each SIO,
and outputs a structured JSON for instruction generation.

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
from pathlib import Path
from typing import Dict, List, Optional


class CodeExtractor(ast.NodeVisitor):
    """AST visitor to extract code snippets."""
    
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


def extract_snippets_from_file(file_path: Path) -> List[Dict]:
    """Extract code snippets from a single Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source, filename=str(file_path))
        extractor = CodeExtractor()
        extractor.set_source(source)
        extractor.visit(tree)
        
        # Add file path to all snippets
        for snippet in extractor.snippets:
            snippet['file'] = str(file_path)
        
        return extractor.snippets
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"[WARN] Failed to parse {file_path}: {e}")
        return []


def extract_all_snippets(repo_dir: Path) -> List[Dict]:
    """Extract code snippets from all Python files in repository."""
    all_snippets = []
    
    for py_file in repo_dir.rglob('*.py'):
        # Skip common non-source directories
        if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'node_modules', 'venv', '.venv']):
            continue
        
        snippets = extract_snippets_from_file(py_file)
        all_snippets.extend(snippets)
    
    return all_snippets


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
    import sys
    sys.exit(main())
