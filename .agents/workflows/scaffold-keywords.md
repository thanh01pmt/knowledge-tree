---
description: Scaffold keyword extraction workspace — tạo .work/kw/, ghi target-context và source refs.
---

# Workflow: Scaffold Keywords

> Tạo workspace cho ATE pipeline. Bước đầu tiên trước khi chạy `/extract-terms`.

**Command:** `/scaffold-keywords <target-context> --source <path>`
**Owner:** `scaffolder`

## Contract

1. Nhận `target-context` (chuỗi mô tả chủ đề mục tiêu) và `--source` (path đến file/thư mục nguồn).
2. Xác định active project từ `status.yaml`.
3. Chạy `chunk_source.py` để cắt tài liệu nguồn và tạo `chunks.json`:
   ```bash
   python3 .agents/skills/keyword-extractor/scripts/chunk_source.py \
     --source <path> \
     --target-context "<target-context>"
   ```
4. Xác nhận với user:
   - Số chunks đã tạo
   - Danh sách file nguồn đã xử lý
   - Target context đã ghi vào `config.json`
5. Hướng dẫn bước tiếp theo: `/extract-terms`

## Expected Output

```
projects/<project>/.work/kw/
├── config.json     # {"target_context": "...", "source": "..."}
└── chunks.json     # [{chunk_id, heading_trail, text, source_file}, ...]
```

## Notes

- Hỗ trợ: PDF (pdfplumber), MD, TXT
- Nếu `--source` là thư mục, xử lý tất cả file `.pdf`/`.md`/`.txt` bên trong
- Dependency: `pip install pdfplumber`
