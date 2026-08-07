#!/usr/bin/env python3
"""test_jit_batch.py - Unit tests for batch concept LO generation in scripts/generate_jit_los.py.
"""

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_jit_los
import lo_quality


def test_case_1():
    print("Testing Case 1: mock returning valid JSON with ulo, cio, sio...")
    mock_json = json.dumps({
        "ulo": "Người học có khả năng hiểu mô hình quản lý bộ nhớ trong dự án.",
        "cio": "Người học có khả năng thiết kế giải pháp bộ nhớ tối ưu.",
        "sio": "Người học có khả năng triển khai Swift ARC với keyword 'weak' trong ứng dụng."
    })
    generate_jit_los._llm_generate = lambda system, user: mock_json

    los = generate_jit_los.generate_concept_los(
        'MEMORY_MANAGEMENT', 'Memory Management', 'quản lý bộ nhớ',
        'App iOS', 'SWIFT', keyword='weak', platform='app'
    )
    assert len(los) == 3, f"Expected 3 LOs, got {len(los)}"
    ulo, cio, sio = los

    assert ulo['code'] == 'ULO-MEMORY_MANAGEMENT-01'
    assert ulo['bloom_level'] == 'UNDERSTAND'
    assert ulo['lo_type'] == 'UNIVERSAL'
    assert ulo['needs_review'] is False, f"Expected ULO needs_review=False, got {ulo['needs_review']}"

    assert cio['code'] == 'CIO-MEMORY_MANAGEMENT-01'
    assert cio['bloom_level'] == 'APPLY'
    assert cio['lo_type'] == 'CONCEPTUAL_IMPL'
    assert cio['needs_review'] is False, f"Expected CIO needs_review=False, got {cio['needs_review']}"

    assert sio['code'] == 'SIO-SWIFT-MEMORY_MANAGEMENT-01'
    assert sio['bloom_level'] == 'CREATE'
    assert sio['lo_type'] == 'SPECIFIC_IMPL'
    assert sio['needs_review'] is False, f"Expected SIO needs_review=False, got {sio['needs_review']}"
    assert sio['platform'] == 'app'
    assert sio['keyword'] == 'weak'
    print("  ✓ Case 1 passed")


def test_case_2():
    print("Testing Case 2: mock returning None (LLM failure)...")
    generate_jit_los._llm_generate = lambda system, user: None

    los = generate_jit_los.generate_concept_los(
        'CACHE_POLICY', 'Cache Policy', '',
        'App iOS', 'SWIFT', keyword='', platform='app'
    )
    assert len(los) == 3
    for lo in los:
        assert lo['needs_review'] is True, f"Expected needs_review=True for {lo['code']}, got {lo['needs_review']}"
        desc = lo['description'].lower()
        for forbidden in lo_quality.FORBIDDEN_STRINGS:
            assert forbidden not in desc, f"Forbidden phrase '{forbidden}' found in description: {desc}"
    print("  ✓ Case 2 passed")


def test_case_3():
    print("Testing Case 3: mock returning JSON missing 'sio' field...")
    mock_json = json.dumps({
        "ulo": "Người học có khả năng hiểu nguyên lý bộ nhớ đệm.",
        "cio": "Người học có khả năng thiết kế cơ chế lưu trữ đệm."
    })
    generate_jit_los._llm_generate = lambda system, user: mock_json

    los = generate_jit_los.generate_concept_los(
        'CACHE_POLICY', 'Cache Policy', '',
        'App iOS', 'SWIFT', keyword='', platform='app'
    )
    assert len(los) == 3
    ulo, cio, sio = los

    assert ulo['needs_review'] is False, f"Expected ULO needs_review=False, got {ulo['needs_review']}"
    assert cio['needs_review'] is False, f"Expected CIO needs_review=False, got {cio['needs_review']}"
    assert sio['needs_review'] is True, f"Expected SIO fallback needs_review=True, got {sio['needs_review']}"
    print("  ✓ Case 3 passed")


def test_case_4():
    print("Testing Case 4: mock returning invalid JSON ('không phải json')...")
    generate_jit_los._llm_generate = lambda system, user: "không phải json"

    los = generate_jit_los.generate_concept_los(
        'ASYNC_TASK', 'Async Task', '',
        'App iOS', 'SWIFT', keyword='', platform='app'
    )
    assert len(los) == 3
    for lo in los:
        assert lo['needs_review'] is True, f"Expected needs_review=True for {lo['code']}, got {lo['needs_review']}"
    print("  ✓ Case 4 passed")


def test_case_5():
    print("Testing Case 5: FOR_LOOP without keyword...")
    generate_jit_los._llm_generate = lambda system, user: None

    los = generate_jit_los.generate_concept_los(
        'FOR_LOOP', 'Definite Iteration', 'vòng lặp xác định',
        'IoT App', 'SWIFT', keyword='', platform='esp32'
    )
    assert len(los) == 3
    sio = los[2]

    assert sio['keyword'] == 'for', f"Expected keyword 'for', got '{sio['keyword']}'"
    assert 'For Loop' in sio['name'], f"Expected 'For Loop' in SIO name, got '{sio['name']}'"
    print("  ✓ Case 5 passed")


if __name__ == '__main__':
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    print("\nAll JIT batch tests passed successfully!")
