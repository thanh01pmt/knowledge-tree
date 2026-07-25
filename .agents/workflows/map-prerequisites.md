---
description: Phase E của Hierarchical LO Generation — Nối các liên kết tiền đề (Prerequisites) giữa các LO hoàn chỉnh, dựa trên bối cảnh Curriculum DAG.
---

# Workflow: Map Prerequisites

> Phase E: Nhìn toàn cảnh `learning-objectives.tsv` và `roadmap_dag_context.json` để nối các dây tiền đề (Prerequisites) giữa các LO (ULO $\leftrightarrow$ ULO, SIO $\leftrightarrow$ SIO). Xuất ra `lo_prerequisites.tsv`.

**Command:** `/map-prerequisites`
**Owner:** `@tree-assembler`

## Prerequisites

- `/generate-sios` (hoặc Phase Merge) đã hoàn tất → `output/learning-objectives.tsv` tồn tại.
- Nên có `.work/roadmap_dag_context.json` hoặc `.work/context-audit.md` (làm bối cảnh).

## Contract

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_map_prerequisites.py \
  --project <slug>
```

### Quá trình thực hiện
- Lấy danh sách toàn bộ LO đã duyệt.
- Lấy DAG Context (Ví dụ: Concept JS phụ thuộc HTML).
- LLM suy luận các liên kết bắt buộc.
- Lọc bỏ ảo giác (mã LO không tồn tại).

## Expected Output

```
output/
└── lo_prerequisites.tsv            ← final output (Target LO, Prereq LO, Rationale)
```

## After This Step

```bash
# Sync 7 tables to Supabase
/sync-supabase
```
