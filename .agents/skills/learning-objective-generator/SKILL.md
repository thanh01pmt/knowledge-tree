---
name: learning-objective-generator
description: Extract and generate structured Learning Objectives (ULO, CIO, SIO) from raw syllabus and context text using LLM scripts.
---

# Learning Objective Generator

> **Goal:** Generate `learning-objectives.tsv` by extracting LOs from the project's syllabus material. Must run AFTER `/build-tree` so that valid concept codes are available for grounding.

## Model Sư Phạm — Abstraction Axis

| Tầng | Bản chất | Ràng buộc |
|---|---|---|
| **ULO** | Năng lực cốt lõi, độc lập với ngôn ngữ/công cụ | KHÔNG đề cập tên công nghệ; `parent_lo_code = ""` |
| **CIO** | Pattern/approach cụ thể hơn, vẫn **language-neutral** | KHÔNG có tên công nghệ trong `name`; mỗi CIO ≥ 2 SIO con |
| **SIO** | Gắn với **công nghệ cụ thể của project** (đọc từ context) | Tên công nghệ PHẢI có trong `name`/`description` |

> ⚠️ Công nghệ cụ thể (Swift, Python, SQL...) **do context quy định**, không phải hardcode. Script tự động detect từ `context/`, `context-audit.md`, `raw_pdf.txt`.

## Format Bắt Buộc

- **Description:** `"Người học có khả năng [verb] [object]..."` (tiếng Việt, 1-3 câu)
- **parent_lo_code:** ULO → `""`; CIO → ULO code; SIO → CIO code

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
python3 .agents/skills/tree-validator/scripts/detect_gaps.py --project <slug>
```
