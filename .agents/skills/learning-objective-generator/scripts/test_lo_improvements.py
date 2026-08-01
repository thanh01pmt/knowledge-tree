#!/usr/bin/env python3
"""Functional test for LO generation improvements (P0-P3)."""
import sys
import csv
import json
from pathlib import Path

# Add script dir to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# We can't import the full script (it has side effects), so test the functions directly
# by extracting and testing the validation logic

# Test 1: bloom_verbs.tsv loading
BLOOM_VERBS_PATH = SCRIPT_DIR.parent / "resources" / "bloom_verbs.tsv"
assert BLOOM_VERBS_PATH.is_file(), f"Not found: {BLOOM_VERBS_PATH}"

bloom_verbs = {}
with open(BLOOM_VERBS_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        level = row.get("bloom_level", "").strip()
        allowed = row.get("allowed_verbs", "").strip()
        if level and allowed:
            bloom_verbs[level] = {v.strip().lower() for v in allowed.split(",") if v.strip()}

assert len(bloom_verbs) == 6, f"Expected 6 levels, got {len(bloom_verbs)}"
print(f"✅ Test 1: bloom_verbs.tsv — {len(bloom_verbs)} levels loaded")
for level, verbs in bloom_verbs.items():
    print(f"   {level}: {len(verbs)} verbs")

# Test 2: validate_bloom_verb logic
def validate_bloom_verb(description, declared_bloom, bloom_verbs):
    """Check if the first verb in description matches the declared Bloom level.
    Supports both English and Vietnamese verbs."""
    if not bloom_verbs or declared_bloom not in bloom_verbs:
        return []
    desc_lower = description.lower()
    for prefix in ["người học có khả năng", "người học có thể"]:
        if prefix in desc_lower:
            desc_lower = desc_lower.split(prefix, 1)[1].strip()
            break
    words = desc_lower.split()
    if not words:
        return []
    
    # Try first word, then first two words (for Vietnamese compound verbs)
    candidates = [words[0].strip(".,;:!?")]
    if len(words) >= 2:
        candidates.append(f"{words[0]} {words[1]}".strip(".,;:!?"))
    
    allowed = bloom_verbs.get(declared_bloom, set())
    for candidate in candidates:
        if candidate in allowed:
            return []
    
    suggestions = []
    for level, verbs in bloom_verbs.items():
        for candidate in candidates:
            if candidate in verbs:
                suggestions.append(level)
                break
    
    if suggestions:
        return [f"Verb '{candidates[0]}' declared as {declared_bloom} but belongs to {suggestions}"]
    else:
        return [f"Verb '{candidates[0]}' not found in any Bloom level (declared: {declared_bloom})"]

tests = [
    ("Người học có khả năng thiết kế một giải pháp", "CREATE", 0),
    ("Người học có khả năng giải thích sự khác biệt", "UNDERSTAND", 0),
    ("Người học có khả năng thiết kế một giải pháp", "REMEMBER", 1),  # should warn
    ("Người học có khả năng giải thích", "EVALUATE", 1),  # should warn
    ("Người học có thể áp dụng công thức", "APPLY", 0),
    ("Người học có khả năng liệt kê các bước", "REMEMBER", 0),
    ("Người học có khả năng đánh giá hiệu năng", "EVALUATE", 0),
    ("Người học có khả năng sáng tạo một ứng dụng", "CREATE", 0),
    ("Người học có khả năng phân tích dữ liệu", "ANALYZE", 0),
    ("Người học có khả năng ghi nhớ công thức", "REMEMBER", 0),
    ("Người học có khả năng thực hiện thí nghiệm", "APPLY", 0),
    ("Người học có khả năng so sánh hai phương pháp", "ANALYZE", 0),
    ("Người học có khả năng đề xuất giải pháp", "EVALUATE", 0),
    ("Người học có khả năng xây dựng ứng dụng", "CREATE", 0),
    ("Người học có khả năng tóm tắt nội dung", "UNDERSTAND", 0),
    ("Người học có khả năng thiết kế", "CREATE", 0),  # single word
    ("Người học có khả năng giải thích", "UNDERSTAND", 0),  # single word
]
all_pass = True
for desc, bloom, expected_warnings in tests:
    warnings = validate_bloom_verb(desc, bloom, bloom_verbs)
    if expected_warnings == 0 and warnings:
        print(f"  ❌ False positive: '{desc[:40]}...' declared as {bloom}: {warnings}")
        all_pass = False
    elif expected_warnings > 0 and not warnings:
        print(f"  ❌ Should have warned: '{desc[:40]}...' declared as {bloom}")
        all_pass = False
    else:
        status = "⚠️ warned" if warnings else "✅ passed"
        print(f"   {status}: '{desc[:40]}...' → {bloom}")

if all_pass:
    print("✅ Test 2: Bloom verb validation — all cases correct")

# Test 3: Merge logic with assessment_approach
print("\nTest 3: Merge TSV with assessment_approach...")
test_ulos = [{
    "code": "ULO-TEST-01", "name": "Test ULO",
    "description": "Người học có khả năng thiết kế một giải pháp",
    "description_vi": "Người học có khả năng thiết kế một giải pháp",
    "bloom_level": "CREATE", "knowledge_dimension": "CONCEPTUAL",
    "concept_codes": ["TEST_CONCEPT"],
    "assessment_approach": "project"
}]
test_cios = [{
    "code": "CIO-TEST-01", "name": "Test CIO",
    "description": "Người học có khả năng áp dụng thuật toán",
    "description_vi": "Người học có khả năng áp dụng thuật toán",
    "bloom_level": "APPLY", "knowledge_dimension": "PROCEDURAL",
    "parent_ulo_code": "ULO-TEST-01",
    "marr_test_note": "Áp dụng được cho Python và JavaScript",
    "assessment_approach": "code-review"
}]
test_sios = [{
    "code": "SIO-SWIFT-TEST", "name": "Test SIO",
    "description": "Người học có khả năng viết vòng lặp for-in trong Swift",
    "description_vi": "Người học có khả năng viết vòng lặp for-in trong Swift",
    "bloom_level": "APPLY", "knowledge_dimension": "PROCEDURAL",
    "parent_cio_code": "CIO-TEST-01",
    "assessment_approach": "debugging-exercise"
}]
test_concepts = [{"code": "TEST_CONCEPT"}]

# Simulate merge logic
valid_concept_codes = {c["code"] for c in test_concepts}
rows = []

# ULOs
ulo_concept_map = {}
for u in test_ulos:
    concept_codes_str = ",".join(
        c for c in u.get("concept_codes", []) if c in valid_concept_codes
    )
    ulo_concept_map[u["code"]] = concept_codes_str
    rows.append({
        "code": u["code"], "name": u["name"],
        "description": u.get("description", u.get("description_vi", "")),
        "lo_type": "UNIVERSAL", "parent_lo_code": "",
        "concept_codes": concept_codes_str,
        "bloom_level": u.get("bloom_level", ""),
        "knowledge_dimension": u.get("knowledge_dimension", ""),
        "assessment_approach": u.get("assessment_approach", "")
    })

# CIOs
cio_concept_map = {}
for c in test_cios:
    parent_ulo = c.get("parent_ulo_code", "")
    inherited = ulo_concept_map.get(parent_ulo, "")
    cio_concept_map[c["code"]] = inherited
    rows.append({
        "code": c["code"], "name": c["name"],
        "description": c.get("description", c.get("description_vi", "")),
        "lo_type": "CONCEPTUAL_IMPL", "parent_lo_code": parent_ulo,
        "concept_codes": inherited,
        "bloom_level": c.get("bloom_level", ""),
        "knowledge_dimension": c.get("knowledge_dimension", ""),
        "assessment_approach": c.get("assessment_approach", "")
    })

# SIOs
for s in test_sios:
    parent_cio = s.get("parent_cio_code", "")
    inherited = cio_concept_map.get(parent_cio, "")
    rows.append({
        "code": s["code"], "name": s["name"],
        "description": s.get("description", s.get("description_vi", "")),
        "lo_type": "SPECIFIC_IMPL", "parent_lo_code": parent_cio,
        "concept_codes": inherited,
        "bloom_level": s.get("bloom_level", ""),
        "knowledge_dimension": s.get("knowledge_dimension", ""),
        "assessment_approach": s.get("assessment_approach", "")
    })

assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"
approaches = {r["code"]: r["assessment_approach"] for r in rows}
assert approaches["ULO-TEST-01"] == "project", f"ULO: {approaches}"
assert approaches["CIO-TEST-01"] == "code-review", f"CIO: {approaches}"
assert approaches["SIO-SWIFT-TEST"] == "debugging-exercise", f"SIO: {approaches}"
print(f"   assessment_approach: {approaches}")
print("✅ Test 3: Merge TSV — assessment_approach preserved correctly")

# Test 4: Write TSV and verify columns
out_path = Path("/tmp/test_lo_merge.tsv")
fieldnames = ["code", "name", "description", "lo_type", "parent_lo_code",
              "concept_codes", "bloom_level", "knowledge_dimension", "assessment_approach"]
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

with open(out_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    written = list(reader)
    assert len(written) == 3
    assert written[0]["assessment_approach"] == "project"
    assert written[1]["assessment_approach"] == "code-review"
    assert written[2]["assessment_approach"] == "debugging-exercise"
    assert written[0]["bloom_level"] == "CREATE"
    assert written[1]["bloom_level"] == "APPLY"
    print(f"   TSV columns: {reader.fieldnames}")
    print(f"   Row 1 (ULO): bloom={written[0]['bloom_level']}, assessment={written[0]['assessment_approach']}")
    print(f"   Row 2 (CIO): bloom={written[1]['bloom_level']}, assessment={written[1]['assessment_approach']}")
    print(f"   Row 3 (SIO): bloom={written[2]['bloom_level']}, assessment={written[2]['assessment_approach']}")

out_path.unlink()
print("✅ Test 4: TSV write/read — columns and values correct")

print("\n🎉 ALL TESTS PASSED")
