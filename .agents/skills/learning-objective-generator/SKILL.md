---
name: learning-objective-generator
description: Extract and generate structured Learning Objectives (ULO, CIO, SIO) from raw syllabus and context text using LLM scripts.
---

# Learning Objective Generator

> **Goal:** Generate `learning-objectives.tsv` by extracting LOs from the project's syllabus material. Must run AFTER `/build-tree` so that valid concept codes are available for grounding.

## Model Sư Phạm — Abstraction Axis

| Tầng | Bản chất (Tri-Level Hypothesis [T6]) | Ràng buộc & Phép thử | Mã định danh |
|---|---|---|---|
| **ULO** | **Computational Level**: Năng lực cốt lõi, WHAT/WHY | Ưu tiên chọn động từ Bloom cấp cao (**Evaluate/Create**); `parent_lo_code = ""` | `ULO-<FEATURE_SLUG>` |
| **CIO** | **Algorithmic Level**: Biểu diễn thủ tục, **language-neutral** | **BẮT BUỘC Phép thử Marr 2-Ngôn-ngữ** (map thử sang $\ge 2$ công cụ, không dính token-order); mỗi CIO $\ge 2$ SIO con | `CIO-<FEATURE_SLUG>` |
| **SIO** | **Implementational Level**: Cụ thể công nghệ | Tên công nghệ PHẢI có trong `name`/`description` | `SIO-<TECH_PREFIX>-<FEATURE_SLUG>` |

> ⚠️ Công nghệ cụ thể (Swift, Python, SQL...) **do context quy định**, không phải hardcode. Script tự động detect từ `context/`, `context-audit.md`, `raw_pdf.txt`.

## SIO Cross-Referencing & Naming Conventions

1. **Cấu trúc Mã SIO:** `SIO-<TECH_PREFIX>-<FEATURE_SLUG>` (dạng `UPPER_SNAKE_CASE`).
   - Ví dụ: `SIO-JS-OBJECT-LITERAL-METHODS`, `SIO-SWIFT-DICTIONARY-LITERAL-METHODS`, `SIO-PY-DICT-KEYS-VALUES-GET`.
2. **Đối chiếu Mẫu SIO Đa Công nghệ (Cross-Technology Pattern Reference):**
   - Tầng **Concept / ULO / CIO** là **100% Trung tính** và dùng chung cho mọi dự án.
   - Khi xây dựng SIO cho một công nghệ mới (ví dụ: Swift), Agent **CẦN TRA CỨU & ĐỐI CHIẾU** các SIO sẵn có từ các dự án khác (JS, Python...) kết nối cùng mã CIO/Concept để kế thừa cấu trúc và chuyển đổi tên/từ khóa tương đương cho công nghệ mới.

## Format Bắt Buộc

- **Description:** `"Người học có khả năng [verb] [object]..."` (tiếng Việt, 1-3 câu)
- **parent_lo_code:** ULO → `""`; CIO → ULO code; SIO → CIO code
- **lo_type:** ULO → `UNIVERSAL`; CIO → `CONCEPTUAL_IMPL`; SIO → `SPECIFIC_IMPL`
- **knowledge_dimension_code:** `FACTUAL`, `CONCEPTUAL`, `PROCEDURAL`, hoặc `METACOGNITIVE` (xác định theo loại đối tượng tri thức [T1])
- **suggested_bloom_levels:** Cấp độ Bloom gợi ý (ví dụ: `REMEMBER,UNDERSTAND`, `APPLY`, `CREATE`)


## Prerequisite

1. `/build-tree` đã chạy → `concepts.tsv` tồn tại (LLM cần danh sách valid concept codes)
2. `context/` có file syllabus (PDF, DOCX...) hoặc `.work/context-audit.md` có nội dung

## Inputs

- `projects/<project>/context/` — file syllabus gốc (PDF, DOCX...)
- `projects/<project>/.work/raw_pdf.txt` hoặc `.work/context-audit.md` — text syllabus
- `projects/<project>/output/concepts.tsv` — valid concept codes (grounding)

## Outputs

- `projects/<project>/output/learning-objectives.tsv`

## Script

```bash
# Chạy tự động (detect technology từ context):
python3 .agents/skills/learning-objective-generator/scripts/llm_extract_lo.py --project <slug>

# Override technology nếu cần:
python3 .agents/skills/learning-objective-generator/scripts/llm_extract_lo.py --project <slug> --technology "Python"
```

## Technology Detection Logic

Script `llm_extract_lo.py` tự suy technology theo thứ tự ưu tiên:
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
