---
name: tree-validator
description: Kiểm tra tính toàn vẹn tham chiếu của knowledge tree và thực hiện kiểm tra đối chiếu ngược độ phủ syllabus (Reverse Coverage Audit) với tài liệu nguồn context.
---

## Cấu trúc repo

```
repo-root/
├── projects/
│   └── <project-slug>/
│       ├── output/
│       │   ├── fields.tsv
│       │   ├── subjects.tsv
│       │   ├── categories.tsv
│       │   ├── topics.tsv
│       │   ├── concepts.tsv
│       │   └── learning-objectives.tsv
│       └── .tree-validator/            # tự scaffold bởi script, không cần tạo tay
│           └── reports/<timestamp>/{validation_report.md, coverage_report.md}
├── .agents/
│   └── skills/tree-validator/scripts/
│       ├── validate_tree.py            # Kiểm tra toàn vẹn tham chiếu
│       └── audit_coverage.py           # Kiểm tra đối chiếu ngược độ phủ syllabus
└── status.yaml                          # active_project + trạng thái lần chạy gần nhất
```

## Quy tắc Kiểm tra N:N (Many-to-Many Referential Integrity)

Cây Tri thức hỗ trợ quan hệ **N:N (Đa - Đa)** trên cả 5 tầng (hỗ trợ phân cách dấu phẩy `,` tại `field_codes`, `subject_codes`, `category_codes`, `topic_codes`, `concept_codes`). 

`validate_tree.py` tự động kiểm tra rằng **mỗi mã cha trong danh sách phân cách bằng dấu phẩy** đều phải tồn tại ở bảng cha tương ứng.

## Quy trình kiểm tra & nghiệm thu

1. **Kiểm tra tính toàn vẹn tham chiếu (`/validate-tree`)**:
   - Chạy `python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <slug> --fix`
   - Đảm bảo 100% không có `BROKEN_REFERENCE`, `ORPHAN_NODE`, hay lỗi format.

2. **Kiểm tra đối chiếu ngược độ phủ Syllabus (`/audit-coverage`)**:
   - Chạy `python3 .agents/skills/tree-validator/scripts/audit_coverage.py --project <slug>`
   - Đảm bảo 100% các mục trong syllabus nguồn (`projects/<slug>/context/` hoặc PDF) đều được phủ bởi các mã LO.
   - Xuất báo cáo tại `projects/<slug>/.tree-validator/reports/<timestamp>/coverage_report.md`.
