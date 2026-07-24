---
description: Run this workflow to establish the project context from source files (PDFs, syllabi, etc.).
---

# Workflow: Context Audit

> Run this workflow to establish the project context from source files (PDFs, syllabi, etc.).

**Command:** `/context-audit`
**Owner:** `@context-analyzer`

## Contract

1. Read all files in `projects/<project>/context/`.
2. **ATE Keywords Check**: Nếu `projects/<project>/context/keywords.tsv` tồn tại (được tạo bởi `/finalize-keywords`):
   - Đọc file này và tích hợp danh sách thuật ngữ vào domain breakdown
   - Ghi section `## ATE Keywords` vào `context-audit.md` (nếu chưa có)
   - Không cần tự extract thuật ngữ từ PDF — đã có từ ATE pipeline
3. Extract the syllabus and high-level knowledge domains that need to be covered.
4. Save the findings to `projects/<project>/.work/context-audit.md`.

Do NOT attempt to map to the Master Tree yet. Just understand what is required.

## Optional Pre-step: ATE Pipeline

Để đảm bảo không bỏ sót thuật ngữ, có thể chạy ATE pipeline trước `/context-audit`:

```
/scaffold-keywords "<chủ đề>" --source projects/<project>/context/
/extract-terms
/verify-terms      ← đọc verify-report.md trước
/finalize-keywords ← tự động inject vào context-audit.md
/context-audit     ← @context-analyzer đọc keywords.tsv đã có
```
