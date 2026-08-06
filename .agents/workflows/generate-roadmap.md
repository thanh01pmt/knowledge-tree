---
description: Generate adaptive learning roadmap from user goal + tech stack + project repo, using Master Tree (Supabase) + cross-tech SIO reuse + JIT expansion + Agent-as-Judge.
---

# Workflow: Generate Adaptive Roadmap

> **Command:** `/generate-roadmap <goal> --tech-stack <stack> [--repo-url <url> | --repo-dir <path>] [--output-dir <path>] [--skip-steps <steps>]`
> **Owner:** `@roadmap-generator`
> **Skill:** `roadmap-generator`

---

## Mô tả

Sinh lộ trình học tập cá nhân hóa từ mục tiêu người học + tech stack + repository dự án thực tế. Pipeline 11 steps tự động, dựa trên Master Tree (Supabase) làm single source of truth cho ULO/CIO, cross-tech SIO reuse qua CIO bridge, JIT expansion cho concepts chưa có coverage, và Agent-as-Judge validation.

## Input

| Tham số | Bắt buộc | Mô tả |
|---|---|---|
| `goal` | ✅ | Mục tiêu học tập (VD: "Học Python để làm dự án AI Generative cơ bản") |
| `--tech-stack` | ✅ | Comma-separated (VD: "Python,OpenAI,JSON") — item đầu = target tech |
| `--repo-url` | ⚠️ | GitHub URL (tự clone) — hoặc `--repo-dir` |
| `--repo-dir` | ⚠️ | Local repo path — hoặc `--repo-url` |
| `--output-dir` | ✅ | Nơi lưu artifacts |
| `--skip-steps` | ❌ | Bỏ qua steps (VD: `step_7` để không sync Supabase) |
| `--resume` | ❌ | Resume từ checkpoint |

## Pipeline (11 steps)

```
STEP 0    Discovery → reuse_inventory.json
STEP 1-2  Keyword extraction → keywords.json
STEP 3    Concept resolution → resolved_concepts.json
STEP 4    CIO matching + ULO derivation → matched_cios.json
STEP 4.5  Prerequisites DAG → prerequisites.json
STEP 5    SIO resolution (REUSE/ADAPT/GENERATE) → resolved_sios.json
STEP 5.5  JIT generation (ULO/CIO/SIO cho concepts mới) → jit_los.json
STEP 6    Agent-as-Judge → judgment.json
STEP 7    Apply staging → Supabase (dry-run default)
STEP 8.5  Code snippets → code_snippets.json
STEP 8.6  Instruction generation → instruction/
STEP 9    Validation → validation_report.json
```

## Cách chạy

### Full pipeline với local repo

```bash
python scripts/generate_roadmap_v3.py \
  --goal "Học Python để làm dự án AI Generative cơ bản" \
  --tech-stack "Python,OpenAI,JSON" \
  --repo-dir /path/to/project \
  --output-dir /tmp/roadmap-output
```

### Với GitHub repo

```bash
python scripts/generate_roadmap_v3.py \
  --goal "Build iOS chat app with SwiftUI" \
  --tech-stack "Swift,SwiftUI,Combine" \
  --repo-url https://github.com/user/repo \
  --output-dir /tmp/out
```

### Skip staging sync (không ghi Supabase)

```bash
python scripts/generate_roadmap_v3.py \
  --goal "..." --tech-stack "..." --repo-dir ... \
  --output-dir /tmp/out --skip-steps step_7
```

## Output

```
/tmp/roadmap-output/
├── pipeline_summary.json        # Tóm tắt toàn bộ
├── reuse_inventory.json         # STEP 0
├── keywords.json                # STEP 1-2
├── resolved_concepts.json       # STEP 3
├── matched_cios.json            # STEP 4
├── prerequisites.json           # STEP 4.5
├── resolved_sios.json           # STEP 5
├── jit_los.json                 # STEP 5.5
├── judgment.json                # STEP 6
├── code_snippets.json           # STEP 8.5
├── instruction/                 # STEP 8.6 — instruction markdown per concept
├── roadmap.json                 # STEP 9
└── validation_report.json       # STEP 9
```

## Lưu ý

- **STEP 7 (Supabase sync)** mặc định dry-run — cần phê duyệt người dùng trước khi upsert thật (AGENTS.md §8)
- **Master Tree Gap D**: nếu pipeline phát hiện concepts mới (proposed), cần duyệt + thêm vào staging Master Tree trước khi chạy lại
- **JIT generation** (STEP 5.5) tự sinh ULO/CIO/SIO cho concepts chưa có coverage — output vào `jit_los.json` chờ judge review
