#!/usr/bin/env python3
"""
Integration test for taxonomy mapping improvements (P0, P1, P2, P4).
Tests core logic of each script without requiring API calls.
"""
import sys
import json
import csv
import re
from pathlib import Path

REPO_ROOT = Path("/opt/data/my-projects/knowledge-tree")
PASS = 0
FAIL = 0

# Add script directories to path
sys.path.insert(0, str(REPO_ROOT / ".agents/skills/taxonomy-mapper/scripts"))
sys.path.insert(0, str(REPO_ROOT / ".agents/skills/tree-assembler/scripts"))

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name} — {detail}")

# ═══════════════════════════════════════════════════════════════════════════════
# P0 — extract_document_hierarchy.py: heading extraction logic
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*60)
print("P0: extract_document_hierarchy.py — Heading Extraction")
print("="*60)

# Test markdown heading extraction
from extract_document_hierarchy import (
    extract_headings_from_markdown, extract_headings_from_text,
    detect_source_type, DocNode, annotate_tree
)

md_text = """# Computer Science
## Programming Fundamentals
### Variables and Data Types
Variables store values in memory.
### Control Flow
Loops and conditionals.
## Networks
### TCP/IP
Transmission Control Protocol.
"""
tree = extract_headings_from_markdown(md_text)
test("Markdown: top-level count", len(tree) == 1, f"got {len(tree)}")
test("Markdown: CS has 2 children", len(tree[0].children) == 2, f"got {len(tree[0].children)}")
test("Markdown: Variables is H3", tree[0].children[0].children[0].level == 3)
test("Markdown: content captured", "Variables store" in tree[0].children[0].children[0].content[0])

# Test text heading extraction (numbered sections)
txt_text = """1. Computer Science
1.1 Programming Fundamentals
1.1.1 Variables and Data Types
Variables store values in memory.
1.1.2 Control Flow
Loops and conditionals.
1.2 Networks
1.2.1 TCP/IP
Transmission Control Protocol.
"""
tree2 = extract_headings_from_text(txt_text)
test("Text: top-level count", len(tree2) == 1, f"got {len(tree2)}")
test("Text: CS has 2 children", len(tree2[0].children) == 2, f"got {len(tree2[0].children)}")
test("Text: section ref captured", "Section 1.1.1" in tree2[0].children[0].children[0].source_ref)

# Test source type detection
test("Source type: .md", detect_source_type(Path("test.md")) == "markdown")
test("Source type: .pdf", detect_source_type(Path("test.pdf")) == "pdf")
test("Source type: .txt", detect_source_type(Path("test.txt")) == "text")

# Test DocNode to_dict
node = DocNode(1, "Test Heading", "p.5")
node.content.append("Some content")
d = node.to_dict()
test("DocNode: level", d["level"] == 1)
test("DocNode: text", d["text"] == "Test Heading")
test("DocNode: source_ref", d["source_ref"] == "p.5")
test("DocNode: content", "Some content" in d["content"])

# Test annotate_tree
from extract_document_hierarchy import annotate_tree
test_tree = [DocNode(1, "Programming", "p.1")]
test_classifications = [{"text": "Programming", "assigned_level": "subject", "confidence": 0.9, "reasoning": "Major discipline"}]
annotated = annotate_tree(test_tree, test_classifications)
test("Annotate: level assigned", annotated[0]["assigned_level"] == "subject")
test("Annotate: confidence", annotated[0]["confidence"] == 0.9)

# ═══════════════════════════════════════════════════════════════════════════════
# P1 — semantic_search_master.py: cosine similarity + search logic
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*60)
print("P1: semantic_search_master.py — Search Logic")
print("="*60)

from semantic_search_master import cosine_similarity, search_level

# Test cosine_similarity
a = [1.0, 0.0, 0.0]
b = [1.0, 0.0, 0.0]
c = [0.0, 1.0, 0.0]
test("Cosine: identical", abs(cosine_similarity(a, b) - 1.0) < 0.001)
test("Cosine: orthogonal", abs(cosine_similarity(a, c) - 0.0) < 0.001)
test("Cosine: empty", cosine_similarity([], []) == 0.0)
test("Cosine: zero vector", cosine_similarity([0, 0], [1, 0]) == 0.0)

# Test search_level with mock embeddings
mock_embeddings = {
    "concepts": {
        "DEFINITE_ITERATION": {"name": "Definite Iteration", "embedding": [1.0, 0.0, 0.0]},
        "COLLECTION_TRAVERSAL": {"name": "Collection Traversal", "embedding": [0.9, 0.1, 0.0]},
        "MEMORY_MANAGEMENT": {"name": "Memory Management", "embedding": [0.0, 0.0, 1.0]},
    }
}
query_emb = [1.0, 0.0, 0.0]
results = search_level(query_emb, mock_embeddings, "concepts", top_k=2)
test("Search: top result", results[0]["code"] == "DEFINITE_ITERATION", f"got {results[0]['code']}")
test("Search: top score ~1.0", abs(results[0]["score"] - 1.0) < 0.01)
test("Search: returns 2 results", len(results) == 2, f"got {len(results)}")
# Test threshold filtering
results_high_thresh = search_level(query_emb, mock_embeddings, "concepts", top_k=5, threshold=0.95)
results_low_thresh = search_level(query_emb, mock_embeddings, "concepts", top_k=5, threshold=0.0)
test("Search: threshold filters", len(results_high_thresh) < len(results_low_thresh),
     f"high={len(results_high_thresh)} low={len(results_low_thresh)}")

# ═══════════════════════════════════════════════════════════════════════════════
# P2 — validate_taxonomy_coherence.py: validation logic
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*60)
print("P2: validate_taxonomy_coherence.py — Validation Logic")
print("="*60)

from validate_taxonomy_coherence import (
    build_lookup, extract_codes_from_mapping_plan, validate_coherence
)

# Mock master tree
mock_master = {
    "fields": [{"code": "CSN", "name": "Computing Systems", "cs2023_ka_mapping": "AR,OS"}],
    "subjects": [{"code": "PROG", "name": "Programming", "field_codes": "CSN", "cs2023_ka_mapping": "SDF"}],
    "categories": [{"code": "CTRL_FLOW", "name": "Control Flow", "subject_codes": "PROG", "cs2023_ka_mapping": "SDF"}],
    "topics": [{"code": "LOOPS", "name": "Loops", "category_codes": "CTRL_FLOW", "cs2023_ka_mapping": "SDF"}],
    "concepts": [
        {"code": "DEF_ITER", "name": "Definite Iteration", "topic_codes": "LOOPS", "cs2023_ka_mapping": "SDF"},
        {"code": "COND_BRANCH", "name": "Conditional Branching", "topic_codes": "LOOPS", "cs2023_ka_mapping": "SDF"},
        {"code": "MEM_MGMT", "name": "Memory Management", "topic_codes": "LOOPS", "cs2023_ka_mapping": "OS"},  # KA mismatch!
    ]
}

lookup = build_lookup(mock_master)
test("Lookup: concept found", lookup["DEF_ITER"]["level"] == "concepts")
test("Lookup: field found", lookup["CSN"]["level"] == "fields")
test("Lookup: non-existent", "NONEXISTENT" not in lookup)

# Test extract_codes_from_mapping_plan
plan_content = """## ATE-Matched Concepts
- `DEF_ITER` ← matched
- `COND_BRANCH` ← matched

## Gap D
### [NEW NODE PROPOSAL] `NEW_CONCEPT`
"""
plan_path = Path("/tmp/test_mapping_plan.md")
plan_path.write_text(plan_content)
codes = extract_codes_from_mapping_plan(plan_path)
test("Extract codes: count", len(codes) == 3, f"got {codes}")
test("Extract codes: DEF_ITER", "DEF_ITER" in codes)
test("Extract codes: NEW_CONCEPT", "NEW_CONCEPT" in codes)
plan_path.unlink()

# Test validate_coherence
warnings = validate_coherence({"DEF_ITER", "COND_BRANCH", "MEM_MGMT"}, mock_master, lookup)
ka_warnings = [w for w in warnings if w["type"] == "KA_MISMATCH"]
test("Coherence: KA mismatch detected", len(ka_warnings) == 1, f"got {len(ka_warnings)}")
test("Coherence: MEM_MGMT flagged", ka_warnings[0]["code"] == "MEM_MGMT")
test("Coherence: no broken refs", len([w for w in warnings if w["type"] == "BROKEN_PARENT_REF"]) == 0)

# Test with broken reference
mock_master_broken = {
    "fields": [{"code": "CSN", "name": "CSN"}],
    "subjects": [],
    "categories": [],
    "topics": [],
    "concepts": [{"code": "BAD_CONCEPT", "name": "Bad", "topic_codes": "NONEXISTENT_TOPIC"}]
}
lookup_broken = build_lookup(mock_master_broken)
warnings_broken = validate_coherence({"BAD_CONCEPT"}, mock_master_broken, lookup_broken)
broken_refs = [w for w in warnings_broken if w["type"] == "BROKEN_PARENT_REF"]
test("Coherence: broken ref detected", len(broken_refs) == 1, f"got {len(broken_refs)}")

# ═══════════════════════════════════════════════════════════════════════════════
# P4 — detect_master_gaps.py: domain extraction + gap detection logic
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*60)
print("P4: detect_master_gaps.py — Gap Detection Logic")
print("="*60)

from detect_master_gaps import extract_domains_from_hints

# Mock structured_hints.json
mock_hints = {
    "source": "test.md",
    "source_type": "markdown",
    "hierarchy": [
        {
            "text": "Programming",
            "assigned_level": "subject",
            "confidence": 0.9,
            "children": [
                {
                    "text": "Variables",
                    "assigned_level": "topic",
                    "confidence": 0.85,
                    "reasoning": "Core programming concept",
                    "children": [
                        {"text": "Type Systems", "assigned_level": "concept", "confidence": 0.8, "children": []}
                    ]
                },
                {
                    "text": "Quantum Computing",
                    "assigned_level": "topic",
                    "confidence": 0.7,
                    "reasoning": "Emerging topic",
                    "children": []
                }
            ]
        }
    ]
}

domains = extract_domains_from_hints(mock_hints)
test("Gaps: 2 domains extracted", len(domains) == 2, f"got {len(domains)}")
test("Gaps: Variables is topic", domains[0]["level"] == "topic")
test("Gaps: Quantum Computing extracted", domains[1]["text"] == "Quantum Computing")
test("Gaps: child_count tracked", domains[0]["child_count"] == 1)

# Test with empty hierarchy
empty_hints = {"hierarchy": []}
test("Gaps: empty hierarchy", len(extract_domains_from_hints(empty_hints)) == 0)

# Test with no hierarchy key
test("Gaps: missing key", len(extract_domains_from_hints({})) == 0)

# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*60)
print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS+FAIL} total")
print("="*60)

if FAIL > 0:
    sys.exit(1)
else:
    print("🎉 ALL TESTS PASSED")
