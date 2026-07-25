---
description: Phase B của Hierarchical LO Generation — sinh CIOs (Conceptual Implementation Objectives) từ ULOs đã duyệt. Mỗi CIO bắt buộc có Marr 2-Language Test note. Điểm duyệt người trước khi sinh SIO.
---

# Workflow: Generate CIOs

> Phase B: Sinh CIO từ ULOs đã duyệt. CIO = pattern/approach trung tính (Algorithmic Level). Mỗi CIO BẮT BUỘC pass Marr 2-Language Test.

**Command:** `/generate-cios`
**Owner:** `@tree-assembler`

## Prerequisites

- `/generate-ulos` đã xong → `.work/hlo/ulos.json` tồn tại
- ULOs đã được xem xét/duyệt

## Contract

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py \
  --phase cios --project <slug>
```

### Sinh gì

- Mỗi ULO → 1-3 CIOs (các pattern/approach khác nhau để đạt ULO đó)
- CIO KHÔNG chứa tên công nghệ hay cú pháp ngôn ngữ
- **Marr 2-Language Test tích hợp trong prompt**: LLM phải map thử CIO sang ≥ 2 ngôn ngữ và ghi vào `marr_test_note`
- Mỗi CIO sẽ có ≥ 2 SIO con (được sinh ở bước sau)

## Expected Output

```
.work/hlo/
├── cios.json          ← data (có trường marr_test_note)
└── cios_preview.md    ← bảng với cột Marr Test Note
```

## Human Review Point ← DUYỆT TRƯỚC KHI /generate-sios

Đọc `.work/hlo/cios_preview.md` và đặc biệt kiểm tra cột **Marr Test**:
- [ ] `marr_test_note` có nhắc tên ≥ 2 ngôn ngữ/công cụ khác nhau không?
- [ ] CIO description có chứa tên công nghệ hay cú pháp không? (nếu có → SIO trá hình → xóa/viết lại)
- [ ] Mỗi ULO có đủ CIO cover các approach khác nhau không?

> ⚠️ CIO với `marr_test_note` trống hoặc chỉ nhắc 1 ngôn ngữ = **vi phạm Marr Test** → phải sửa trước khi tiếp tục.

## After This Step

```
/generate-sios
```
