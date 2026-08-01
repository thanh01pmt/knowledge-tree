# Implementation Plan: Taxonomy Mapping Improvements (P0-P4)

**Date**: 2026-08-01
**ADR**: ADR-0007
**Priority**: P0 > P1 > P2 > P3 > P4

---

## P0 — Document Hierarchy Extractor

**File**: `.agents/skills/taxonomy-mapper/scripts/extract_document_hierarchy.py`
**Dependencies**: `pdfplumber`, `python-docx` (optional)
**Estimated**: ~200 lines

### Implementation

```python
# 1. detect_source_type(path) -> "pdf" | "md" | "txt" | "docx"
# 2. extract_headings(source) -> list of {level, text, children}
#    - PDF: pdfplumber, detect heading by font size / bold
#    - MD: regex heading levels
#    - TXT: detect numbering (1., 1.1) or blank-line grouping
#    - DOCX: python-docx heading styles
# 3. llm_classify_levels(tree, syllabus_text) -> annotated tree
#    - Prompt: assign Master Tree level (Field/Subject/Category/Topic/Concept)
#    - Based on content, NOT heading level
# 4. Output: structured_hints.json
```

### Prompt design

```
System: You are a taxonomy classifier. Given a document heading and its content,
determine which Knowledge Tree level it maps to.

Rules:
- Field: Broadest domain (e.g., "Computer Science", "Data Science")
- Subject: Major sub-discipline (e.g., "Programming", "Networks")
- Category: Group of related topics (e.g., "Control Flow", "Data Structures")
- Topic: Specific skill area (e.g., "Loops", "Arrays")
- Concept: Atomic knowledge unit (e.g., "Definite Iteration", "Array Traversal")

Base your decision on the CONTENT, not the heading level.
A H2 about "Variables" might be a Topic, while a H2 about "Computer Architecture" might be a Subject.
```

---

## P1 — Semantic Search Master Tree

**File**: `.agents/skills/taxonomy-mapper/scripts/semantic_search_master.py`
**Dependencies**: `numpy` (for cosine similarity)
**Estimated**: ~100 lines

### Implementation

```python
# 1. Load master_tree_embeddings.json (already exists)
# 2. embed(query) -> vector (using OpenAI embeddings API)
# 3. cosine_similarity(query_emb, master_embeddings[level]) -> scores
# 4. Return top-k matches per level (concepts, topics, categories)
# 5. Output: search_results.json
```

### Integration

Agent `/map-taxonomy` calls:
```bash
python3 semantic_search_master.py --query "Use for-in loops to iterate over arrays" --top-k 5
```

Returns:
```json
{
  "concepts": [
    {"code": "DEFINITE_ITERATION", "name": "Definite Iteration", "score": 0.92},
    {"code": "COLLECTION_TRAVERSAL", "name": "Collection Traversal", "score": 0.85}
  ],
  "topics": [
    {"code": "ITERATION_PATTERNS", "name": "Iteration Patterns", "score": 0.88}
  ]
}
```

---

## P2 — Multi-level Coherence Validation

**File**: `.agents/skills/tree-assembler/scripts/validate_taxonomy_coherence.py`
**Estimated**: ~80 lines

### Checks

1. **CS2023 KA coherence**: Concepts in same topic should have related KA codes
2. **Parent-child validity**: All parent references must exist in Master Tree
3. **Hierarchy depth**: concept → topic → category → subject → field chain must be valid

---

## P3 — CS2023 KA Coherence Signal

**Cải tiến trong**: `assemble_project.py` (thêm function)
**Estimated**: ~50 lines

### Logic

```python
def check_ka_coherence(concept_code, topic_code, master_tree):
    concept_ka = master_tree.concepts[concept_code].cs2023_ka_mapping
    topic_ka = master_tree.topics[topic_code].cs2023_ka_mapping
    if concept_ka and topic_ka and not set(concept_ka) & set(topic_ka):
        return Warning(f"Concept {concept_code} KA ({concept_ka}) disjoint from topic {topic_code} KA ({topic_ka})")
    return None
```

---

## P4 — Master Gap Detection

**File**: `.agents/skills/taxonomy-mapper/scripts/detect_master_gaps.py`
**Estimated**: ~120 lines

### Logic

```python
# For each unmapped syllabus domain:
# 1. Embed domain name
# 2. Search all Master Tree concepts
# 3. If top-3 similarity < 0.60 → Gap
# 4. Propose [NEW CATEGORY PROPOSAL] or [NEW TOPIC PROPOSAL]
```

---

## Timeline

| Step | What | Depends on |
|------|------|------------|
| 1 | P0: extract_document_hierarchy.py | — |
| 2 | P1: semantic_search_master.py | master_tree_embeddings.json (exists) |
| 3 | Update map-taxonomy.md workflow | P0, P1 |
| 4 | Update taxonomy-mapper/SKILL.md | P0, P1 |
| 5 | P2: validate_taxonomy_coherence.py | — |
| 6 | P3: integrate into assemble_project.py | — |
| 7 | P4: detect_master_gaps.py | — |
| 8 | Update build-tree.md workflow | P2, P3 |
| 9 | Test all scripts | All |

---

## Files to create/modify

### New files
- `.agents/skills/taxonomy-mapper/scripts/extract_document_hierarchy.py` (P0)
- `.agents/skills/taxonomy-mapper/scripts/semantic_search_master.py` (P1)
- `.agents/skills/tree-assembler/scripts/validate_taxonomy_coherence.py` (P2)
- `.agents/skills/taxonomy-mapper/scripts/detect_master_gaps.py` (P4)

### Modified files
- `.agents/skills/tree-assembler/scripts/assemble_project.py` (P3)
- `.agents/workflows/map-taxonomy.md` (P0, P1 integration)
- `.agents/workflows/build-tree.md` (P2, P3 integration)
- `.agents/skills/taxonomy-mapper/SKILL.md` (new scripts)
