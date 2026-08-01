# ADR-0007: Document Hierarchy Extractor & Semantic Taxonomy Mapping

**Status**: Accepted
**Date**: 2026-08-01
**Deciders**: thanh01pmt, Hermes Agent

## Context

Pipeline hiện tại cho taxonomy mapping có 3 bước rời rạc:

```
/context-audit  →  context-audit.md (markdown tự do, agent đọc thủ công)
/escalate-concepts → concept_candidates.tsv (chỉ chạm tới concept, không chạm category/topic)
/map-taxonomy   →  agent search Master Tree thủ công → mapping-plan.md
```

### Vấn đề

1. **Mất cấu trúc tài liệu gốc**: Syllabus, tài liệu kỹ thuật, roadmap.sh đều có hierarchy riêng (heading levels, section numbering, table of contents) nhưng pipeline không extract được. Agent phải guess concept nào thuộc topic nào.

2. **Không có semantic search**: Agent search Master Tree bằng cách đọc TSV/JSON thủ công — dễ bỏ sót, phụ thuộc keyword matching của LLM.

3. **Không có coherence validation**: Sau khi map, không có check nào đảm bảo concept A thuộc topic X là hợp lý, hoặc các concept trong cùng topic có coherent không.

4. **Không có gap detection**: Không phát hiện được syllabus có domain X nhưng Master Tree không có concept nào phù hợp.

### Source types cần hỗ trợ

| Loại | Ví dụ | Heading structure |
|------|-------|-------------------|
| Syllabus học thuật | Apple Associate Guide | Chương → Bài → Mục rõ ràng |
| Tài liệu kỹ thuật | AWS docs, MDN | H1→H2→H3→paragraph |
| Roadmap | roadmap.sh | Markdown headings |
| Blog / Documentation | Blog posts | Lỏng lẻo, có thể không có heading |
| PDF scan | Thiếu outline | Font size, numbering detection |

## Decision

Bổ sung 5 cải tiến vào pipeline taxonomy mapping, triển khai theo thứ tự ưu tiên:

### P0 — Document Hierarchy Extractor (thay thế "Syllabus Structure Parser")

**File mới**: `.agents/skills/taxonomy-mapper/scripts/extract_document_hierarchy.py`

**Cơ chế**: Script duy nhất, source-type agnostic, extract cây phân cấp từ bất kỳ tài liệu nào:

1. **Extract document tree**: Dùng pdfplumber (PDF heading bằng font size/bold), markdown heading levels, TXT numbering detection, DOCX styles
2. **LLM classify Master Tree level**: Với mỗi node trong cây, LLM xác định tầng Master Tree phù hợp (Field/Subject/Category/Topic/Concept) dựa trên nội dung — không dựa trên heading level cứng
3. **Output**: `structured_hints.json` — cây phân cấp đã gán nhãn, kèm evidence trích dẫn

**Không giả định input là syllabus.** Xử lý mọi loại tài liệu kỹ thuật.

### P1 — Semantic Search Master Tree

**File mới**: `.agents/skills/taxonomy-mapper/scripts/semantic_search_master.py`

**Cơ chế**: Dùng `master_tree_embeddings.json` (3.8MB, đã có sẵn) để tìm top-5 concept/topic/category gần nhất cho mỗi syllabus item. Trả về evidence-based matching scores.

### P2 — Multi-level Coherence Validation

**Cải tiến**: `assemble_project.py` (hoặc script mới `validate_taxonomy_coherence.py`)

**Cơ chế**: Kiểm tra:
- CS2023 KA codes của các concept trong cùng topic có coherent không
- Parent-child references có hợp lệ không
- Hierarchy depth có đúng không (concept → topic → category → subject → field)

### P3 — CS2023 KA Coherence Signal

**Cải tiến**: Trong `assemble_project.py`

**Cơ chế**: Khi agent đề xuất concept cho topic, kiểm tra KA code match với topic/category cha. Cảnh báo nếu concept có KA code hoàn toàn khác biệt.

### P4 — Master Gap Detection

**File mới**: `.agents/skills/taxonomy-mapper/scripts/detect_master_gaps.py`

**Cơ chế**: Với mỗi syllabus domain chưa được map, semantic search toàn bộ Master Tree. Nếu top-3 similarity < threshold (0.60) → Gap: Master Tree thiếu domain này. Đề xuất node mới ở cấp Category hoặc Topic.

## Consequences

### Tích hợp vào pipeline

```
/context-audit
  ↓ context-audit.md (giữ nguyên)
  ↓
[extract_document_hierarchy.py]  ← P0 MỚI
  ↓ structured_hints.json
  ↓
[escalate-concepts]  (giữ nguyên)
  ↓ concept_candidates.tsv
  ↓
/map-taxonomy  ← agent dùng structured_hints.json + semantic_search_master.py
  ↓ mapping-plan.md
  ↓
/build-tree  ← thêm coherence validation (P2, P3)
  ↓ 5 taxonomy TSVs
  ↓
[detect_master_gaps.py]  ← P4 MỚI (optional, chạy sau build-tree)
  ↓ master_gap_report.md
```

### Workflow changes

- `map-taxonomy.md`: Thêm bước load `structured_hints.json` trước khi search Master Tree
- `build-tree.md`: Thêm coherence validation step
- `taxonomy-mapper/SKILL.md`: Thêm scripts mới

### No schema changes

Không thay đổi database schema, TSV format, hay Master Tree structure. Tất cả đều là scripts + prompt engineering.

## Related

- ADR-0006: Source of Truth for Master Knowledge Tree
- AGENTS.md §1 (Context Gate), §4 (Approval Gate), §7 (Master Tree Integrity Gate)
