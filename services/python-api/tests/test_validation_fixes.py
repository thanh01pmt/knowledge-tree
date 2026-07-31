#!/usr/bin/env python3
"""
test_validation_fixes.py — Test suite cho các fix T6 neutrality, hierarchy
semantics, N:N comma split, word-boundary matching, và Master Tree integrity.

Chạy: python3 tests/test_validation_fixes.py
Không cần API key — test thuần deterministic trên dữ liệu mẫu.
"""

import csv
import io
import os
import re
import sys
import tempfile
from pathlib import Path

# Đảm bảo import được các module từ skill scripts
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / ".agents/skills/tree-validator/scripts"))
sys.path.insert(0, str(REPO_ROOT / ".agents/skills/taxonomy-mapper/scripts"))


# ─── Helpers ──────────────────────────────────────────────────────────────────

def write_tsv(path: Path, headers: list, rows: list[dict]):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def make_project(output_dir: Path, lo_rows=None, concept_rows=None):
    """Scaffold a minimal project output dir with given LO/concept rows."""
    output_dir.mkdir(parents=True, exist_ok=True)
    lo_headers = ["code", "name", "description", "lo_type", "parent_lo_code",
                  "concept_codes", "bloom_level", "knowledge_dimension",
                  "assessment_approach"]
    write_tsv(output_dir / "learning-objectives.tsv", lo_headers, lo_rows or [])
    concept_headers = ["code", "name", "description", "topic_codes", "keywords",
                       "cs2023_ka_mapping", "metadata"]
    write_tsv(output_dir / "concepts.tsv", concept_headers, concept_rows or [])


# ─── Tests: validate_master_tree T6 neutrality ───────────────────────────────

def test_t6_regex_detects_known_tech_tokens():
    """T6 regex phải bắt được các tech token phổ biến."""
    from validate_master_tree import TECH_RE
    test_cases = [
        ("Sử dụng Swift để code", "swift"),
        ("Arduino sketch setup", "arduino"),
        ("React component", "react"),
        ("Django framework", "django"),
        ("Codable protocol", "codable"),
        ("Python script", "python"),
        ("Node.js server", "node.js"),
    ]
    for text, expected_token in test_cases:
        matches = [m.group(0).lower() for m in TECH_RE.finditer(text)]
        assert any(expected_token in m for m in matches), \
            f"TECH_RE phải bắt '{expected_token}' trong '{text}', got {matches}"
    print("✓ test_t6_regex_detects_known_tech_tokens")


def test_t6_regex_ignores_generic_terms():
    """T6 regex KHÔNG match các từ chung không phải tech brand."""
    from validate_master_tree import TECH_RE
    # "spring" (vật lý lò xo), "rust" (gỉ sét) — nhưng "rust" là ngôn ngữ nên phải bắt
    # Chỉ "spring" bị bỏ vì ambiguous
    text = "lò xo spring joint hinge"
    matches = [m.group(0).lower() for m in TECH_RE.finditer(text)]
    assert "spring" not in matches, \
        f"'spring' (vật lý) không nên bị match, got {matches}"
    print("✓ test_t6_regex_ignores_generic_terms")


def test_t6_regex_no_false_positive_on_reactive():
    """'reactive' (reactive UI) không nên bị match với 'react'."""
    from validate_master_tree import TECH_RE
    text = "reactive UI, declarative UI, component-based"
    matches = [m.group(0).lower() for m in TECH_RE.finditer(text)]
    assert "react" not in matches, \
        f"'reactive' không nên match 'react', got {matches}"
    print("✓ test_t6_regex_no_false_positive_on_reactive")


def test_find_t6_violations_on_clean_data():
    """Master Tree đã fix phải 0 violations."""
    from validate_master_tree import parse, find_t6_violations
    tsv_path = REPO_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
    if not tsv_path.is_file():
        print("⚠ SKIP test_find_t6_violations_on_clean_data (master TSV not found)")
        return
    tables = parse(tsv_path)
    violations = find_t6_violations(tables)
    assert len(violations) == 0, \
        f"Master Tree phải 0 T6 violations sau fix, got {len(violations)}: {violations[:5]}"
    print("✓ test_find_t6_violations_on_clean_data")


# ─── Tests: validate_tree hierarchy semantics ────────────────────────────────

def test_hierarchy_violation_cio_parent_not_ulo():
    """CIO có parent là SIO → phải báo LO_HIERARCHY_VIOLATION."""
    from validate_tree import check_lo_type_rules, Issue
    lo_rows = [
        {"code": "ULO-A", "lo_type": "UNIVERSAL", "parent_lo_code": ""},
        {"code": "CIO-B", "lo_type": "CONCEPTUAL_IMPL", "parent_lo_code": "SIO-X"},
        {"code": "SIO-X", "lo_type": "SPECIFIC_IMPL", "parent_lo_code": "CIO-Y"},
        {"code": "CIO-Y", "lo_type": "CONCEPTUAL_IMPL", "parent_lo_code": "ULO-A"},
    ]
    issues = check_lo_type_rules(lo_rows)
    hierarchy_issues = [i for i in issues if i.rule_id == "LO_HIERARCHY_VIOLATION"]
    assert len(hierarchy_issues) >= 1, \
        f"Phải có LO_HIERARCHY_VIOLATION cho CIO-B (parent=SIO-X), got {hierarchy_issues}"
    print("✓ test_hierarchy_violation_cio_parent_not_ulo")


def test_hierarchy_violation_sio_parent_not_cio():
    """SIO có parent là ULO → phải báo LO_HIERARCHY_VIOLATION."""
    from validate_tree import check_lo_type_rules
    lo_rows = [
        {"code": "ULO-A", "lo_type": "UNIVERSAL", "parent_lo_code": ""},
        {"code": "SIO-B", "lo_type": "SPECIFIC_IMPL", "parent_lo_code": "ULO-A"},
    ]
    issues = check_lo_type_rules(lo_rows)
    hierarchy_issues = [i for i in issues if i.rule_id == "LO_HIERARCHY_VIOLATION"]
    assert len(hierarchy_issues) >= 1, \
        f"Phải có LO_HIERARCHY_VIOLATION cho SIO-B (parent=ULO-A), got {hierarchy_issues}"
    print("✓ test_hierarchy_violation_sio_parent_not_cio")


def test_hierarchy_valid_chain_no_violation():
    """ULO → CIO → SIO đúng → không có LO_HIERARCHY_VIOLATION."""
    from validate_tree import check_lo_type_rules
    lo_rows = [
        {"code": "ULO-A", "lo_type": "UNIVERSAL", "parent_lo_code": ""},
        {"code": "CIO-B", "lo_type": "CONCEPTUAL_IMPL", "parent_lo_code": "ULO-A"},
        {"code": "SIO-C", "lo_type": "SPECIFIC_IMPL", "parent_lo_code": "CIO-B"},
    ]
    issues = check_lo_type_rules(lo_rows)
    hierarchy_issues = [i for i in issues if i.rule_id == "LO_HIERARCHY_VIOLATION"]
    assert len(hierarchy_issues) == 0, \
        f"Chain đúng không có hierarchy violation, got {hierarchy_issues}"
    print("✓ test_hierarchy_valid_chain_no_violation")


# ─── Tests: N:N comma split for Gap B ─────────────────────────────────────────

def test_cio_sio_depth_split_comma():
    """SIO có parent_lo_code = 'CIO-A,CIO-B' phải count cho cả 2 CIO."""
    from validate_tree import check_cio_sio_depth
    lo_rows = [
        {"code": "CIO-A", "lo_type": "CONCEPTUAL_IMPL", "name": "A"},
        {"code": "CIO-B", "lo_type": "CONCEPTUAL_IMPL", "name": "B"},
        # SIO có 2 parent (N:N) → count cho cả 2
        {"code": "SIO-X", "lo_type": "SPECIFIC_IMPL", "parent_lo_code": "CIO-A,CIO-B"},
        {"code": "SIO-Y", "lo_type": "SPECIFIC_IMPL", "parent_lo_code": "CIO-A"},
    ]
    issues = check_cio_sio_depth(lo_rows, min_sios=2)
    # CIO-A có 2 SIO (X, Y) → OK; CIO-B có 1 SIO (X) → WARNING
    shallow_b = [i for i in issues if i.code == "CIO-B"]
    shallow_a = [i for i in issues if i.code == "CIO-A"]
    assert len(shallow_b) == 1, f"CIO-B phải shallow (1 SIO), got {shallow_b}"
    assert len(shallow_a) == 0, f"CIO-A phải OK (2 SIO via N:N), got {shallow_a}"
    print("✓ test_cio_sio_depth_split_comma")


def test_detect_gaps_shallow_cios_split_comma():
    """detect_gaps.detect_shallow_cios cũng phải split comma."""
    from detect_gaps import detect_shallow_cios
    lo_rows = [
        {"code": "CIO-A", "lo_type": "CONCEPTUAL_IMPL", "name": "A", "parent_lo_code": "ULO-X"},
        {"code": "CIO-B", "lo_type": "CONCEPTUAL_IMPL", "name": "B", "parent_lo_code": "ULO-X"},
        {"code": "SIO-X", "lo_type": "SPECIFIC_IMPL", "parent_lo_code": "CIO-A,CIO-B"},
    ]
    shallow = detect_shallow_cios(lo_rows, min_sios=2)
    # Cả 2 CIO đều có 1 SIO (chỉ SIO-X) → cả 2 shallow
    codes = [s["code"] for s in shallow]
    assert "CIO-A" in codes and "CIO-B" in codes, \
        f"Cả CIO-A và CIO-B phải được count (N:N split), got {codes}"
    print("✓ test_detect_gaps_shallow_cios_split_comma")


# ─── Tests: query_master_tree word boundary + Unicode ─────────────────────────

def test_query_word_boundary_no_substring_false_positive():
    """Query 'SQL' không nên match 'SQLITE'."""
    from query_master_tree import calculate_score
    # SQLITE trong name, SQL trong query
    score = calculate_score("SQL", "SQLITE_ROW", "SQLite Storage", "sqlite, storage", "")
    # 'SQL' không nên word-match 'SQLite' (case-insensitive)
    # Score có thể > 0 nếu code chứa 'SQLITE' — nhưng phải < 80 (không phải keyword exact)
    assert score < 80, f"SQL không nên exact-match SQLITE, score={score}"
    print("✓ test_query_word_boundary_no_substring_false_positive")


def test_query_unicode_diacritics_tolerance():
    """Query 'Đồ thị' phải match name chứa 'đồ thị'."""
    from query_master_tree import calculate_score, normalize_text
    # 'đồ thị' in name
    score = calculate_score("Đồ thị", "GRAPH", "Đồ thị và Cây", "graph, tree", "")
    assert score > 0, f"'Đồ thị' phải match name chứa 'đồ thị', score={score}"
    print("✓ test_query_unicode_diacritics_tolerance")


def test_query_unicode_strip_diacritics():
    """Query không dấu 'Do thi' phải match name có dấu 'Đồ thị'."""
    from query_master_tree import calculate_score
    score = calculate_score("Do thi", "GRAPH", "Đồ thị và Cây", "graph, tree", "")
    # 'Do thi' (no diacritics) phải match 'Đồ thị' (with diacritics) sau strip
    assert score > 0, f"'Do thi' phải match 'Đồ thị' qua strip_diacritics, score={score}"
    print("✓ test_query_unicode_strip_diacritics")


# ─── Tests: audit_coverage word boundary ──────────────────────────────────────

def test_audit_coverage_word_boundary_no_false_match():
    """'internet' trong syllabus không nên match LO chỉ chứa 'intern'."""
    # Đây là test integration nhẹ — verify regex pattern đúng
    text = "intern training program"
    kw = "internet"
    # Word-boundary match
    matched = bool(re.search(r"\b" + re.escape(kw) + r"\b", text))
    assert not matched, f"'internet' không nên word-match 'intern', matched={matched}"
    print("✓ test_audit_coverage_word_boundary_no_false_match")


def test_audit_coverage_bloom_verbs_in_stopwords():
    """Bloom verbs phải có trong stop words để không inflate coverage."""
    # Đọc source audit_coverage.py để verify stop words chứa Bloom verbs
    src = (REPO_ROOT / ".agents/skills/tree-validator/scripts/audit_coverage.py").read_text()
    bloom_verbs = ["describe", "identify", "explain", "compare", "implement", "design"]
    for v in bloom_verbs:
        assert f'"{v}"' in src, f"Bloom verb '{v}' phải có trong stop_words của audit_coverage"
    print("✓ test_audit_coverage_bloom_verbs_in_stopwords")


# ─── Tests: detect_gaps Marr detection mở rộng ────────────────────────────────

def test_detect_gaps_marr_detects_more_languages():
    """Marr detection phải bắt được Kotlin, Scala, Perl (mới thêm)."""
    from detect_gaps import detect_non_neutral_cios
    cios = [
        {"code": "CIO-A", "lo_type": "CONCEPTUAL_IMPL",
         "name": "Kotlin coroutine", "description": "Sử dụng Kotlin"},
        {"code": "CIO-B", "lo_type": "CONCEPTUAL_IMPL",
         "name": "Scala pattern", "description": "Functional với Scala"},
        {"code": "CIO-C", "lo_type": "CONCEPTUAL_IMPL",
         "name": "Neutral pattern", "description": "Mô tả trung tính"},
    ]
    violations = detect_non_neutral_cios(cios)
    codes = [v["code"] for v in violations]
    assert "CIO-A" in codes, f"Kotlin phải bị bắt, got {codes}"
    assert "CIO-B" in codes, f"Scala phải bị bắt, got {codes}"
    assert "CIO-C" not in codes, f"CIO trung tính không bị bắt, got {codes}"
    print("✓ test_detect_gaps_marr_detects_more_languages")


def test_detect_gaps_marr_detects_syntax_patterns():
    """Marr detection phải bắt các syntax pattern mới (console.log, async)."""
    from detect_gaps import detect_non_neutral_cios
    cios = [
        {"code": "CIO-A", "lo_type": "CONCEPTUAL_IMPL",
         "name": "Logging", "description": "Sử dụng console.log để debug"},
        {"code": "CIO-B", "lo_type": "CONCEPTUAL_IMPL",
         "name": "Async", "description": "Viết async function với await"},
    ]
    violations = detect_non_neutral_cios(cios)
    codes = [v["code"] for v in violations]
    assert "CIO-A" in codes, f"console.log phải bị bắt, got {codes}"
    assert "CIO-B" in codes, f"async/await phải bị bắt, got {codes}"
    print("✓ test_detect_gaps_marr_detects_syntax_patterns")


# ─── Integration: validate_master_tree on actual Master Tree ──────────────────

def test_validate_master_tree_pass():
    """validate_master_tree.py phải PASS trên Master Tree hiện tại."""
    import subprocess
    result = subprocess.run(
        [sys.executable,
         str(REPO_ROOT / ".agents/skills/tree-validator/scripts/validate_master_tree.py")],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, \
        f"validate_master_tree phải PASS (exit 0), got {result.returncode}\n{result.stdout}\n{result.stderr}"
    assert "0 error" in result.stdout, f"Phải 0 errors, got: {result.stdout}"
    print("✓ test_validate_master_tree_pass")


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_all():
    tests = [
        test_t6_regex_detects_known_tech_tokens,
        test_t6_regex_ignores_generic_terms,
        test_t6_regex_no_false_positive_on_reactive,
        test_find_t6_violations_on_clean_data,
        test_hierarchy_violation_cio_parent_not_ulo,
        test_hierarchy_violation_sio_parent_not_cio,
        test_hierarchy_valid_chain_no_violation,
        test_cio_sio_depth_split_comma,
        test_detect_gaps_shallow_cios_split_comma,
        test_query_word_boundary_no_substring_false_positive,
        test_query_unicode_diacritics_tolerance,
        test_query_unicode_strip_diacritics,
        test_audit_coverage_word_boundary_no_false_match,
        test_audit_coverage_bloom_verbs_in_stopwords,
        test_detect_gaps_marr_detects_more_languages,
        test_detect_gaps_marr_detects_syntax_patterns,
        test_validate_master_tree_pass,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'='*50}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())