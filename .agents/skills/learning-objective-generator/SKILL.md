---
name: learning-objective-generator
description: Extract and generate structured Learning Objectives (ULO, CIO, SIO) from raw syllabus and context text using LLM scripts.
---

# Learning Objective Generator

> **Goal:** Generate `learning-objectives.tsv` by extracting LOs from the project's syllabus material. Must run AFTER `/build-tree` so that valid concept codes are available for grounding.

## Model Sư Phạm — Abstraction Axis

| Tầng    | Bản chất (Tri-Level Hypothesis [T6])                           | Ràng buộc & Phép thử                                                                                                  | Mã định danh                       |
| ------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **ULO** | **Computational Level**: Năng lực cốt lõi, WHAT/WHY            | Ưu tiên chọn động từ Bloom cấp cao (**Evaluate/Create**); `parent_lo_code = ""`                                       | `ULO-<FEATURE_SLUG>`               |
| **CIO** | **Algorithmic Level**: Biểu diễn thủ tục, **language-neutral** | **BẮT BUỘC Phép thử Marr 2-Ngôn-ngữ** (map thử sang $\ge 2$ công cụ, không dính token-order); mỗi CIO $\ge 2$ SIO con | `CIO-<FEATURE_SLUG>`               |
| **SIO** | **Implementational Level**: Cụ thể công nghệ                   | Tên công nghệ PHẢI có trong `name`/`description`                                                                      | `SIO-<TECH_PREFIX>-<FEATURE_SLUG>` |

> ⚠️ Công nghệ cụ thể (Swift, Python, SQL...) **do context quy định**, không phải hardcode. Script tự động detect từ `context/`, `context-audit.md`, `raw_pdf.txt`.

## SIO Cross-Referencing & Naming Conventions

1. **Cấu trúc Mã SIO:** `SIO-<TECH_PREFIX>-<FEATURE_SLUG>` (dạng `UPPER_SNAKE_CASE`).
   - Ví dụ: `SIO-JS-OBJECT-LITERAL-METHODS`, `SIO-SWIFT-DICTIONARY-LITERAL-METHODS`, `SIO-PY-DICT-KEYS-VALUES-GET`.
2. **Đối chiếu Mẫu SIO Đa Công nghệ (Cross-Technology Pattern Reference):**
   - Tầng **Concept / ULO / CIO** là **100% Trung tính** và dùng chung cho mọi dự án.
   - Khi xây dựng SIO cho một công nghệ mới (ví dụ: Swift), Agent **CẦN TRA CỨU & ĐỐI CHIẾU** các SIO sẵn có từ các dự án khác (JS, Python...) kết nối cùng mã CIO/Concept để kế thừa cấu trúc và chuyển đổi tên/từ khóa tương đương cho công nghệ mới.

## Format Bắt Buộc

File `learning-objectives.tsv` gồm **9 cột** (tab-separated):

| Cột                   | Mô tả                                                                          |
| --------------------- | ------------------------------------------------------------------------------ |
| `code`                | Mã định danh (VD: `ULO-DATA-TYPES`, `CIO-ARRAY-TRAVERSAL`, `SIO-JS-ARRAY-MAP`) |
| `name`                | Tên ngắn gọn                                                                   |
| `description`         | `"Người học có khả năng [verb] [object]..."` (tiếng Việt, 1-3 câu)             |
| `lo_type`             | ULO → `UNIVERSAL`; CIO → `CONCEPTUAL_IMPL`; SIO → `SPECIFIC_IMPL`              |
| `parent_lo_code`      | ULO → `""`; CIO → ULO code(s); SIO → CIO code(s). Phân cách `,` cho N:N        |
| `concept_codes`       | Danh sách mã concept liên kết (phân cách `,`)                                  |
| `bloom_level`         | Cấp độ Bloom (VD: `REMEMBER`, `UNDERSTAND`, `APPLY`, `EVALUATE`, `CREATE`)     |
| `knowledge_dimension` | `FACTUAL`, `CONCEPTUAL`, `PROCEDURAL`, hoặc `METACOGNITIVE` [T1]               |
| `assessment_approach` | Phương pháp đánh giá trực tiếp (VD: `project`, `quiz`, `code-review`)          |

## Prerequisite

1. `/build-tree` đã chạy → `concepts.tsv` tồn tại (LLM cần danh sách valid concept codes)
2. `context/` có file syllabus (PDF, DOCX...) hoặc `.work/context-audit.md` có nội dung

## Inputs

- `projects/<project>/context/` — file syllabus gốc (PDF, DOCX...)
- `projects/<project>/.work/raw_pdf.txt` hoặc `.work/context-audit.md` — text syllabus
- `projects/<project>/output/concepts.tsv` — valid concept codes (grounding)

## Outputs

- `projects/<project>/output/learning-objectives.tsv`

## Scripts

### Primary: `llm_generate_hierarchical_lo.py` (Hierarchical 4-Phase)

Script chính, sinh LO theo 3 tầng riêng biệt rồi merge. Mỗi phase tương ứng một workflow command:

| Phase        | Command                   | Mô tả                                                                                |
| ------------ | ------------------------- | ------------------------------------------------------------------------------------ |
| **A** — ULOs | `/generate-ulos`          | Sinh Universal LOs từ concepts. Bloom ưu tiên Evaluate/Create. **Điểm duyệt người.** |
| **B** — CIOs | `/generate-cios`          | Sinh Conceptual Impl LOs với **Marr 2-Language Test** per-CIO. **Điểm duyệt người.** |
| **C** — SIOs | `/generate-sios`          | Sinh Specific Impl LOs (tech-specific) + merge ra `learning-objectives.tsv`          |
| **merge**    | _(tự động trong Phase C)_ | Gộp ULO + CIO + SIO thành file TSV cuối                                              |

```bash
# Phase A: Sinh ULOs
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py --project <slug> --phase ulos

# Phase B: Sinh CIOs (kèm Marr Test)
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py --project <slug> --phase cios

# Phase C: Sinh SIOs + merge
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py --project <slug> --phase sios
```

### `llm_map_prerequisites.py` (Phase E — ADR-0005)

Sinh `lo_prerequisites.tsv` và cập nhật `concepts.tsv` (cột `prerequisite_concept_codes`) theo quy trình 4 bước: Domain Partitioning → Concept DAG (LLM) → ULO Derivation → LLM Verify.

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_map_prerequisites.py --project <slug>
```

### Legacy 1-shot: `llm_extract_lo.py`

> ⚠️ Legacy/fast path. Sinh toàn bộ LO trong 1 lần gọi LLM, không phân tách phase. Không khuyến nghị cho project mới — dùng `llm_generate_hierarchical_lo.py` thay thế.

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_extract_lo.py --project <slug>

# Override technology nếu cần:
python3 .agents/skills/learning-objective-generator/scripts/llm_extract_lo.py --project <slug> --technology "Python"
```

**Technology Detection Logic** (áp dụng cho cả 2 script):

1. `status.yaml` key `technology` (nếu được set thủ công)
2. Tên file trong `context/` (weight cao nhất — VD: "Apple_Associate.pdf" → Swift)
3. Keyword scan `context-audit.md` (80 dòng đầu)
4. Keyword scan `raw_pdf.txt` (100 dòng đầu)
5. Project slug (fallback cuối cùng)

## Validation sau khi generate

```bash
python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug>
python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <slug>
```
