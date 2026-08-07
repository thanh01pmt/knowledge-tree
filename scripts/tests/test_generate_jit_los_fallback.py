#!/usr/bin/env python3
"""test_generate_jit_los_fallback.py - Unit tests for fallback logic in scripts/generate_jit_los.py.
"""

import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_jit_los

# Mock _llm_generate to return None so fallback path is executed without calling LLM
generate_jit_los._llm_generate = lambda *a, **k: None


def test_case_1():
    print("Testing Case 1: generate_ulo with valid concept description...")
    res = generate_jit_los.generate_ulo('LED_CONTROL', 'dùng NeoPixel để điều khiển LED', 'Led Control')
    assert 'NeoPixel' in res['description'], f"Expected 'NeoPixel' in description, got: {res['description']}"
    assert res['needs_review'] is False, f"Expected needs_review=False, got: {res['needs_review']}"
    print("  ✓ Case 1 passed")


def test_case_2():
    print("Testing Case 2: generate_ulo with empty description...")
    res = generate_jit_los.generate_ulo('WEB_SERVER', '', 'Web Server')
    assert res['needs_review'] is True, f"Expected needs_review=True, got: {res['needs_review']}"
    desc = res['description']
    assert 'nguyên lý phổ quát' not in desc, f"Description contains forbidden phrase 'nguyên lý phổ quát': {desc}"
    assert 'và cách vận dụng nó' not in desc, f"Description contains forbidden phrase 'và cách vận dụng nó': {desc}"
    print("  ✓ Case 2 passed")


def test_case_3():
    print("Testing Case 3: generate_sio for esp32 platform...")
    res = generate_jit_los.generate_sio(
        'FOR_LOOP', 'For Loop', 'dùng vòng lặp for', 'app IoT', 'SWIFT',
        keyword='for', platform='esp32'
    )
    assert 'for' in res['description'], f"Expected 'for' in description, got: {res['description']}"
    assert res['needs_review'] is False, f"Expected needs_review=False, got: {res['needs_review']}"
    assert res['lo_type'] == 'SPECIFIC_IMPL', f"Expected lo_type='SPECIFIC_IMPL', got: {res['lo_type']}"
    assert res['code'].startswith('SIO-ESP32-'), f"Expected code to start with 'SIO-ESP32-', got: {res['code']}"
    print("  ✓ Case 3 passed")


def test_case_4():
    print("Testing Case 4: generate_cio with empty description...")
    res = generate_jit_los.generate_cio('HTTP_PROTOCOL', '')
    assert res['needs_review'] is True, f"Expected needs_review=True, got: {res['needs_review']}"
    assert res['bloom_level'] == 'APPLY', f"Expected bloom_level='APPLY', got: {res['bloom_level']}"
    print("  ✓ Case 4 passed")


if __name__ == '__main__':
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    print("\nAll JIT fallback tests passed successfully!")
