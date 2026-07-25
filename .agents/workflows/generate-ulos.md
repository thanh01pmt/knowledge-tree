---
description: Phase A của Hierarchical LO Generation — sinh ULOs (Universal Learning Objectives) từ concepts, ưu tiên Bloom Evaluate/Create. Điểm duyệt người trước khi sinh CIO.
---

# Workflow: Generate ULOs

> Phase A: Sinh ULO từ concepts đã build. ULO = năng lực cốt lõi, hoàn toàn technology-agnostic, ưu tiên Bloom cấp cao.

**Command:** `/generate-ulos`
**Owner:** `@tree-assembler`

## Prerequisites

- `/build-tree` đã xong → `output/concepts.tsv` tồn tại
- `.work/raw_pdf.txt` hoặc `.work/context-audit.md` có nội dung

## Contract

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase ulos --project <slug>
```

### Sinh gì

- Mỗi concept → 1-3 ULOs
- Bloom level ưu tiên: **Evaluate / Create** (tránh "lực hút" về Remember/Understand)
- ULO KHÔNG chứa tên công nghệ
- `concept_codes` chỉ dùng codes từ `concepts.tsv`

## Expected Output

```
.work/hlo/
├── ulos.json          ← data
└── ulos_preview.md    ← bảng tóm tắt + descriptions
```

## Human Review Point ← DUYỆT TRƯỚC KHI /generate-cios

Đọc `.work/hlo/ulos_preview.md` và kiểm tra:
- [ ] ULOs có thực sự technology-agnostic không?
- [ ] Bloom level có đủ cao (Evaluate/Create) không?
- [ ] Coverage đủ cho tất cả concepts quan trọng không?
- [ ] Số ULO hợp lý (không quá nhiều ULO trivial)?

Có thể sửa `ulos.json` trực tiếp trước khi chạy bước tiếp theo.

## After This Step

```
/generate-cios
```
