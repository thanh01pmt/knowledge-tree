#!/usr/bin/env python3
"""
STEP 1-2: Extract project keywords using AST-level analysis.

This script:
1. Analyzes repo structure (file tree, LOC, entry points)
2. Parses source files to extract:
   - Import statements → framework keywords
   - Type declarations (class/struct/enum/protocol) → domain concepts
   - Function signatures → business logic
   - Property wrappers → state management patterns
   - Error handling patterns → reliability concerns
3. Outputs structured keywords with source, weight, and context

Usage:
    python scripts/extract_project_keywords.py --repo-url https://github.com/user/repo
    python scripts/extract_project_keywords.py --repo-dir /path/to/repo
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set

# Import analyze_repo_structure
sys.path.insert(0, str(Path(__file__).parent.parent / ".agents/skills/github-research/scripts"))
import analyze_repo_structure


# ============================================================================
# SWIFT PARSING
# ============================================================================

def parse_swift_file(filepath: Path) -> Dict:
    """Parse Swift file to extract AST-level information."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {}
    
    result = {
        'imports': [],
        'types': [],
        'functions': [],
        'property_wrappers': [],
        'error_handling': [],
    }
    
    # Extract imports
    import_pattern = r'^import\s+(\w+)'
    result['imports'] = re.findall(import_pattern, content, re.MULTILINE)
    
    # Extract type declarations
    type_pattern = r'\b(class|struct|enum|protocol)\s+(\w+)(?:\s*:\s*([^\{]+))?'
    for match in re.finditer(type_pattern, content):
        kind = match.group(1)
        name = match.group(2)
        conforms = match.group(3) or ""
        protocols = [p.strip() for p in conforms.split(',') if p.strip()]
        
        result['types'].append({
            'kind': kind,
            'name': name,
            'conforms_to': protocols,
            'file': str(filepath.name),
        })
    
    # Extract function signatures
    func_pattern = r'\bfunc\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([^\{]+))?'
    for match in re.finditer(func_pattern, content):
        name = match.group(1)
        params = match.group(2)
        returns = (match.group(3) or "").strip()
        
        # Skip private/internal helpers (simple heuristic)
        if name.startswith('_'):
            continue
        
        result['functions'].append({
            'name': name,
            'params': params.strip(),
            'returns': returns,
            'file': str(filepath.name),
        })
    
    # Extract property wrappers
    wrapper_pattern = r'@(State|Binding|ObservedObject|StateObject|Published|Environment|EnvironmentObject|AppStorage|SceneStorage|FocusState|Observable)\b'
    result['property_wrappers'] = list(set(re.findall(wrapper_pattern, content)))
    
    # Extract error handling patterns
    if 'do {' in content or 'do{' in content:
        result['error_handling'].append('do-catch')
    if 'throws' in content:
        result['error_handling'].append('throws')
    if 'Result<' in content:
        result['error_handling'].append('Result type')
    if 'try?' in content:
        result['error_handling'].append('try?')
    if 'try!' in content:
        result['error_handling'].append('try!')
    
    return result


def parse_swift_project(repo_dir: Path) -> Dict:
    """Parse all Swift files in project."""
    swift_files = list(repo_dir.rglob('*.swift'))
    
    all_imports = []
    all_types = []
    all_functions = []
    all_wrappers = []
    all_error_patterns = []
    
    for swift_file in swift_files:
        # Skip test files and generated files
        if 'Test' in str(swift_file) or 'Tests' in str(swift_file):
            continue
        if '.build' in str(swift_file) or 'Derived' in str(swift_file):
            continue
        
        parsed = parse_swift_file(swift_file)
        all_imports.extend(parsed['imports'])
        all_types.extend(parsed['types'])
        all_functions.extend(parsed['functions'])
        all_wrappers.extend(parsed['property_wrappers'])
        all_error_patterns.extend(parsed['error_handling'])
    
    # Deduplicate and count
    from collections import Counter
    import_counts = Counter(all_imports)
    wrapper_counts = Counter(all_wrappers)
    error_counts = Counter(all_error_patterns)
    
    return {
        'imports': [
            {'module': mod, 'count': count}
            for mod, count in import_counts.most_common(20)
        ],
        'types': all_types[:100],  # Limit to top 100
        'functions': all_functions[:100],  # Limit to top 100
        'property_wrappers': [
            {'wrapper': w, 'count': count}
            for w, count in wrapper_counts.most_common(10)
        ],
        'error_handling_patterns': [
            {'pattern': p, 'count': count}
            for p, count in error_counts.most_common(10)
        ],
    }


# ============================================================================
# TYPESCRIPT/JAVASCRIPT PARSING
# ============================================================================

def parse_ts_file(filepath: Path) -> Dict:
    """Parse TypeScript/JavaScript file."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {}
    
    result = {
        'imports': [],
        'types': [],
        'functions': [],
        'error_handling': [],
    }
    
    # Extract imports
    import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
    result['imports'] = re.findall(import_pattern, content)
    
    # Extract type/interface declarations
    type_pattern = r'\b(interface|type|class|enum)\s+(\w+)'
    for match in re.finditer(type_pattern, content):
        kind = match.group(1)
        name = match.group(2)
        result['types'].append({
            'kind': kind,
            'name': name,
            'file': str(filepath.name),
        })
    
    # Extract function declarations
    func_pattern = r'\bfunction\s+(\w+)\s*\(([^)]*)\)'
    for match in re.finditer(func_pattern, content):
        name = match.group(1)
        params = match.group(2)
        result['functions'].append({
            'name': name,
            'params': params.strip(),
            'file': str(filepath.name),
        })
    
    # Arrow functions
    arrow_pattern = r'\bconst\s+(\w+)\s*=\s*\([^)]*\)\s*(?::\s*\w+)?\s*=>'
    for match in re.finditer(arrow_pattern, content):
        name = match.group(1)
        result['functions'].append({
            'name': name,
            'params': '',
            'file': str(filepath.name),
        })
    
    # Error handling
    if 'try {' in content or 'try{' in content:
        result['error_handling'].append('try-catch')
    if 'Promise' in content:
        result['error_handling'].append('Promise')
    if '.catch(' in content:
        result['error_handling'].append('.catch()')
    
    return result


def parse_ts_project(repo_dir: Path) -> Dict:
    """Parse all TypeScript/JavaScript files."""
    ts_files = list(repo_dir.rglob('*.ts')) + list(repo_dir.rglob('*.tsx')) + list(repo_dir.rglob('*.js')) + list(repo_dir.rglob('*.jsx'))
    
    all_imports = []
    all_types = []
    all_functions = []
    all_error_patterns = []
    
    for ts_file in ts_files:
        # Skip node_modules and build artifacts
        if 'node_modules' in str(ts_file) or 'dist' in str(ts_file) or '.next' in str(ts_file):
            continue
        
        parsed = parse_ts_file(ts_file)
        all_imports.extend(parsed['imports'])
        all_types.extend(parsed['types'])
        all_functions.extend(parsed['functions'])
        all_error_patterns.extend(parsed['error_handling'])
    
    # Deduplicate and count
    from collections import Counter
    import_counts = Counter(all_imports)
    error_counts = Counter(all_error_patterns)
    
    return {
        'imports': [
            {'module': mod, 'count': count}
            for mod, count in import_counts.most_common(20)
        ],
        'types': all_types[:100],
        'functions': all_functions[:100],
        'error_handling_patterns': [
            {'pattern': p, 'count': count}
            for p, count in error_counts.most_common(10)
        ],
    }


# ============================================================================
# PYTHON PARSING
# ============================================================================

def parse_python_file(filepath: Path) -> Dict:
    """Parse Python file."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {}
    
    result = {
        'imports': [],
        'types': [],
        'functions': [],
        'error_handling': [],
    }
    
    # Extract imports
    import_pattern = r'^(?:import|from)\s+(\w+)'
    result['imports'] = re.findall(import_pattern, content, re.MULTILINE)
    
    # Extract class declarations
    class_pattern = r'\bclass\s+(\w+)(?:\s*\(([^)]+)\))?'
    for match in re.finditer(class_pattern, content):
        name = match.group(1)
        bases = match.group(2) or ""
        result['types'].append({
            'kind': 'class',
            'name': name,
            'bases': [b.strip() for b in bases.split(',') if b.strip()],
            'file': str(filepath.name),
        })
    
    # Extract function declarations
    func_pattern = r'\bdef\s+(\w+)\s*\(([^)]*)\)'
    for match in re.finditer(func_pattern, content):
        name = match.group(1)
        params = match.group(2)
        # Skip private/dunder methods
        if name.startswith('_'):
            continue
        result['functions'].append({
            'name': name,
            'params': params.strip(),
            'file': str(filepath.name),
        })
    
    # Error handling
    if 'try:' in content:
        result['error_handling'].append('try-except')
    if 'raise' in content:
        result['error_handling'].append('raise')
    
    return result


def parse_python_project(repo_dir: Path) -> Dict:
    """Parse all Python files."""
    py_files = list(repo_dir.rglob('*.py'))
    
    all_imports = []
    all_types = []
    all_functions = []
    all_error_patterns = []
    
    for py_file in py_files:
        # Skip venv, __pycache__, tests
        if any(skip in str(py_file) for skip in ['venv', '__pycache__', 'test_', 'tests/']):
            continue
        
        parsed = parse_python_file(py_file)
        all_imports.extend(parsed['imports'])
        all_types.extend(parsed['types'])
        all_functions.extend(parsed['functions'])
        all_error_patterns.extend(parsed['error_handling'])
    
    # Deduplicate and count
    from collections import Counter
    import_counts = Counter(all_imports)
    error_counts = Counter(all_error_patterns)
    
    return {
        'imports': [
            {'module': mod, 'count': count}
            for mod, count in import_counts.most_common(20)
        ],
        'types': all_types[:100],
        'functions': all_functions[:100],
        'error_handling_patterns': [
            {'pattern': p, 'count': count}
            for p, count in error_counts.most_common(10)
        ],
    }


# ============================================================================
# KEYWORD EXTRACTION
# ============================================================================

def extract_keywords(source_context: Dict, basic_analysis: Dict, repo_dir: str) -> List[Dict]:
    """Extract structured keywords from source context and basic analysis."""
    keywords = []
    
    # Source 1: Import statements → framework keywords
    for imp in source_context.get('imports', []):
        module = imp['module']
        count = imp['count']
        keywords.append({
            'keyword': module,
            'source': 'import',
            'weight': 1.0 + (count - 1) * 0.1,  # Higher weight for frequently used
            'context': f'Imported {count} times',
        })
    
    # Source 2: Type declarations → domain concepts
    for type_decl in source_context.get('types', []):
        name = type_decl['name']
        kind = type_decl['kind']
        
        # Skip generic/framework types
        if name in {'View', 'Model', 'ViewModel', 'Controller', 'Service', 'Manager'}:
            continue
        
        keywords.append({
            'keyword': name,
            'source': 'type_declaration',
            'weight': 1.5,
            'context': f'{kind} declaration',
        })
    
    # Source 3: Function signatures → business logic
    for func in source_context.get('functions', []):
        name = func['name']
        
        # Skip generic helpers
        if name in {'init', 'setup', 'configure', 'initialize'}:
            continue
        
        keywords.append({
            'keyword': name,
            'source': 'function_signature',
            'weight': 1.2,
            'context': 'Function signature',
        })
    
    # Source 4: Property wrappers → state management patterns
    for wrapper in source_context.get('property_wrappers', []):
        wrapper_name = wrapper['wrapper']
        count = wrapper['count']
        keywords.append({
            'keyword': f'@{wrapper_name}',
            'source': 'property_wrapper',
            'weight': 2.0,
            'context': f'Used {count} times',
        })
    
    # Source 5: Error handling patterns → reliability concerns
    for error in source_context.get('error_handling_patterns', []):
        pattern = error['pattern']
        count = error['count']
        keywords.append({
            'keyword': pattern,
            'source': 'error_handling',
            'weight': 1.3,
            'context': f'Used {count} times',
        })
    
    # Source 6: README sections → design intent
    readme_path = Path(repo_dir) / 'README.md'
    if readme_path.exists():
        try:
            readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')
            # Extract section headers
            headers = re.findall(r'^#+\s+(.+)$', readme_content, re.MULTILINE)
            for header in headers[:10]:
                keywords.append({
                    'keyword': header.strip(),
                    'source': 'readme',
                    'weight': 0.9,
                    'context': 'README section',
                })
        except Exception:
            pass
    
    # Source 7: Config files → platform constraints
    for config in basic_analysis.get('config_files', []):
        filename = Path(config).name
        keywords.append({
            'keyword': filename,
            'source': 'config',
            'weight': 0.8,
            'context': 'Configuration file',
        })
    
    # Deduplicate by keyword
    seen = set()
    unique_keywords = []
    for kw in keywords:
        key = kw['keyword'].lower()
        if key not in seen:
            seen.add(key)
            unique_keywords.append(kw)
    
    return unique_keywords


# ============================================================================
# MAIN
# ============================================================================

def clone_repo(repo_url: str, target_dir: Path) -> Path:
    """Clone repository to target directory."""
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_dir = target_dir / repo_name
    
    if repo_dir.exists():
        print(f"Repository already exists at {repo_dir}", file=sys.stderr)
        return repo_dir
    
    print(f"Cloning {repo_url} to {repo_dir}...", file=sys.stderr)
    subprocess.run(
        ['git', 'clone', '--depth', '1', repo_url, str(repo_dir)],
        check=True,
        capture_output=True,
    )
    return repo_dir


def main():
    parser = argparse.ArgumentParser(description='Extract project keywords using AST-level analysis')
    parser.add_argument('--repo-url', help='GitHub repository URL to clone')
    parser.add_argument('--repo-dir', help='Local repository directory (if already cloned)')
    parser.add_argument('--output', required=True, help='Output JSON file')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress output')
    
    args = parser.parse_args()
    
    # Determine repo directory
    if args.repo_dir:
        repo_dir = Path(args.repo_dir)
        if not repo_dir.exists():
            print(f"Error: Repository directory not found: {repo_dir}", file=sys.stderr)
            sys.exit(1)
    elif args.repo_url:
        temp_dir = Path('/tmp/roadmap-repos')
        temp_dir.mkdir(exist_ok=True)
        repo_dir = clone_repo(args.repo_url, temp_dir)
    else:
        print("Error: Must provide --repo-url or --repo-dir", file=sys.stderr)
        sys.exit(1)
    
    # Step 1: Basic analysis
    if not args.quiet:
        print(f"[STEP 1] Analyzing repository structure...", file=sys.stderr)
    
    basic_analysis = analyze_repo_structure.analyze(str(repo_dir), repo_dir.name)
    
    # Determine primary language
    languages = basic_analysis.get('languages', {})
    primary_lang = max(languages.keys(), key=lambda k: languages[k]) if languages else 'unknown'
    
    if not args.quiet:
        print(f"  Primary language: {primary_lang}", file=sys.stderr)
    
    # Step 2: AST-level parsing
    if not args.quiet:
        print(f"[STEP 2] Parsing source files...", file=sys.stderr)
    
    if primary_lang == 'Swift':
        source_context = parse_swift_project(repo_dir)
    elif primary_lang in {'TypeScript', 'JavaScript'}:
        source_context = parse_ts_project(repo_dir)
    elif primary_lang == 'Python':
        source_context = parse_python_project(repo_dir)
    else:
        print(f"  Warning: No parser for language '{primary_lang}'", file=sys.stderr)
        source_context = {'imports': [], 'types': [], 'functions': [], 'property_wrappers': [], 'error_handling_patterns': []}
    
    # Step 3: Keyword extraction
    if not args.quiet:
        print(f"[STEP 3] Extracting keywords...", file=sys.stderr)
    
    keywords = extract_keywords(source_context, basic_analysis, str(repo_dir))
    
    # Build output
    output = {
        'repo_dir': str(repo_dir),
        'primary_language': primary_lang,
        'languages': languages,
        'source_context': source_context,
        'keywords': keywords,
    }
    
    # Write output
    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    if not args.quiet:
        print(f"[DONE] Extracted {len(keywords)} keywords", file=sys.stderr)
        print(f"  Imports: {len(source_context['imports'])}", file=sys.stderr)
        print(f"  Types: {len(source_context['types'])}", file=sys.stderr)
        print(f"  Functions: {len(source_context['functions'])}", file=sys.stderr)
        if source_context.get('property_wrappers'):
            print(f"  Property wrappers: {len(source_context['property_wrappers'])}", file=sys.stderr)
        if source_context.get('error_handling_patterns'):
            print(f"  Error patterns: {len(source_context['error_handling_patterns'])}", file=sys.stderr)
        print(f"Output written to {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
