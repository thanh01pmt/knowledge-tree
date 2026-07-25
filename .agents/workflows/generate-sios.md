---
description: Phase C của Hierarchical LO Generation — sinh SIOs (Specific Implementation Objectives) từ CIOs đã duyệt, gắn với công nghệ cụ thể của project. Sau đó merge toàn bộ vào learning-objectives.tsv.
---

# Workflow: Generate SIOs

> Phase C: Sinh SIO từ CIOs đã duyệt. SIO = kỹ năng cụ thể gắn technology. Sau đó merge ULO+CIO+SIO vào `learning-objectives.tsv`.

**Command:** `/generate-sios`
**Owner:** `@tree-assembler`

## Prerequisites

- `/generate-cios` đã xong → `.work/hlo/cios.json` tồn tại
- CIOs đã xem xét Marr Test

## Contract

### Step 1: Sinh SIOs

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase sios --project <slug>
# Override technology nếu cần:
# --technology "Swift / SwiftUI"
```

- Mỗi CIO → ≥ 2 SIOs (diễn đạt 2 scenario/cách dùng khác nhau)
- SIO BẮT BUỘC nhắc tên technology trong code, name, description
- Có thể nhắc cú pháp API/keyword cụ thể của technology

### Step 2: Merge → TSV

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase merge --project <slug>
```

Ghi toàn bộ ULO+CIO+SIO vào `output/learning-objectives.tsv` (8 cột: code, name, description, lo_type, parent_lo_code, concept_codes, bloom_level, knowledge_dimension).

## Expected Output

```
.work/hlo/
└── sios.json                          ← data

output/
└── learning-objectives.tsv            ← final output
```

## After This Step

```bash
# Validate referential integrity
python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug>

# Check coverage ≥ 95%
python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <slug>

# Detect gaps (CIO thiếu SIO, Concept thiếu LO)
python3 .agents/skills/tree-validator/scripts/detect_gaps.py --project <slug>
```

## Notes

- Nếu `/generate-los` (old 1-shot) đã chạy trước và tạo `learning-objectives.tsv`, script này sẽ **ghi đè** — backup nếu cần
- Dùng `--phase all` để chạy toàn bộ pipeline tự động (không có human review checkpoints)
