---
name: roadmap-generator
description: Generate adaptive learning roadmaps from a user goal + tech stack + project repository, using Master Tree (Supabase) as source of truth for ULO/CIO, cross-tech SIO reuse via CIO bridge, JIT expansion for uncovered concepts, and Agent-as-Judge validation.
---

# Roadmap Generator Skill

> **Goal:** Bạn là `@roadmap-generator`. Nhiệm vụ của bạn là sinh lộ trình học tập cá nhân hóa từ mục tiêu người học + tech stack + repository dự án thực tế, dựa trên Master Tree (Supabase) làm single source of truth cho ULO/CIO, tái sử dụng SIO cross-tech qua CIO bridge, JIT expansion cho concepts chưa có coverage, và Agent-as-Judge validation.

---

## 🏛️ Kiến trúc Pipeline (11 steps)

```
STEP 0    roadmap_discovery.py        — scan Master Tree (Supabase) + projects → reuse_inventory.json
STEP 1-2  extract_project_keywords.py — AST-level keyword extraction → keywords.json
STEP 3    resolve_concepts.py         — keyword → concept resolution (embedding + source thresholds) → resolved_concepts.json
STEP 4    match_cios.py               — concept → CIO matching + ULO derivation → matched_cios.json
STEP 4.5  generate_prerequisites.py   — prerequisite DAG (reuse master + concept + hierarchy) → prerequisites.json
STEP 5    resolve_sios.py             — cross-tech SIO resolution (REUSE/ADAPT/GENERATE) → resolved_sios.json
STEP 5.5  generate_jit_los.py         — JIT generate ULO/CIO/SIO cho concepts chưa có coverage → jit_los.json
STEP 6    agent_as_judge.py           — validation gate (concepts/SIOs/prerequisites) → judgment.json
STEP 7    apply_to_staging.py         — sync quarantine TSVs lên Supabase (dry-run default) → staging
STEP 8.5  instruction_code_extractor.py — extract code snippets từ repo → code_snippets.json
STEP 8.6  generate_instruction.py     — sinh instruction markdown (8-section, real code) → instruction/
STEP 9    validate_roadmap.py         — post-generation validation → validation_report.json
```

## 🚀 Cách chạy

### Full pipeline

```bash
python scripts/generate_roadmap_v3.py \
  --goal "Học Python để làm dự án AI Generative cơ bản" \
  --tech-stack "Python,OpenAI,JSON" \
  --repo-dir /path/to/project \
  --output-dir /tmp/roadmap-output
```

### Với GitHub repo (tự clone)

```bash
python scripts/generate_roadmap_v3.py \
  --goal "..." \
  --tech-stack "Swift,SwiftUI,Combine" \
  --repo-url https://github.com/user/repo \
  --output-dir /tmp/out
```

### Resume / skip steps

```bash
python scripts/generate_roadmap_v3.py \
  --goal "..." --tech-stack "..." --repo-dir ... \
  --output-dir /tmp/out --resume          # resume từ checkpoint
  --skip-steps step_7                     # bỏ qua staging sync
```

## ⚙️ Chạy từng step riêng (debug)

```bash
# STEP 0
python scripts/roadmap_discovery.py --goal "..." --tech-stack "Swift,SwiftUI" --output /tmp/inv.json

# STEP 1-2
python scripts/extract_project_keywords.py --repo-dir /path/to/repo --output /tmp/kw.json

# STEP 3
python scripts/resolve_concepts.py --keywords /tmp/kw.json --reuse-inventory /tmp/inv.json --goal "..." --output /tmp/rc.json

# STEP 4
python scripts/match_cios.py --resolved-concepts /tmp/rc.json --reuse-inventory /tmp/inv.json --output /tmp/mc.json

# STEP 4.5
python scripts/generate_prerequisites.py --matched-cios /tmp/mc.json --resolved-sios /tmp/rs.json --reuse-inventory /tmp/inv.json --output /tmp/prereqs.json

# STEP 5
python scripts/resolve_sios.py --matched-cios /tmp/mc.json --target-tech SWIFT --output /tmp/rs.json

# STEP 5.5
python scripts/generate_jit_los.py --resolved-concepts /tmp/rc.json --matched-cios /tmp/mc.json --resolved-sios /tmp/rs.json --keywords /tmp/kw.json --reuse-inventory /tmp/inv.json --target-tech SWIFT --output /tmp/jit.json

# STEP 6
python scripts/agent_as_judge.py --concepts /tmp/rc.json --sios /tmp/rs.json --target-tech SWIFT --output /tmp/judgment.json

# STEP 8.5
python scripts/instruction_code_extractor.py --repo-dir /path/to/repo --sios-file /tmp/rs.json --output /tmp/snippets.json

# STEP 8.6
python scripts/generate_instruction.py --resolved-sios /tmp/rs.json --code-snippets /tmp/snippets.json --target-tech SWIFT --output-dir /tmp/instruction --prerequisites /tmp/prereqs.json --jit-los /tmp/jit.json

# STEP 9
python scripts/validate_roadmap.py --roadmap-file /tmp/roadmap.json --sios-file /tmp/rs.json --concepts-file /tmp/rc.json --output /tmp/validation.json
```

## 🧠 Nguyên tắc thiết kế (bắt buộc)

1. **Master Tree (Supabase) là single source of truth cho ULO/CIO** — đọc, không sinh lại (trừ khi concept mới)
2. **Chỉ SIO là tầng sinh mới per-project** — gắn với tech stack cụ thể
3. **Mọi tầng đều có thể thiếu** — Master Tree đang xây → JIT expansion (STEP 5.5) sinh ULO/CIO/SIO cho concepts chưa có coverage
4. **Cross-tech SIO reuse qua CIO bridge** — cùng CIO parent, khác tech → ADAPT (threshold ≥0.6 ADAPT, 0.3-0.6 TEMPLATE, <0.3 GENERATE)
5. **Judge gate tự động** — Agent-as-Judge cho phép merge nếu pass, không cần human blocking
6. **Source-based thresholds** — docstring/README (0.45) là high-signal domain intent, imports/error_handling (0.60) là noisy
7. **Semantic clustering cho proposals** — gom keywords cùng domain thành 1 concept proposal (anchor = docstring/README), loại noise

## 📁 Output structure

```
/tmp/roadmap-output/
├── pipeline_state.json          # Checkpoint state
├── pipeline_summary.json        # Summary report
├── reuse_inventory.json         # STEP 0
├── keywords.json                # STEP 1-2
├── resolved_concepts.json       # STEP 3
├── matched_cios.json            # STEP 4 (+ derived_ulos)
├── prerequisites.json           # STEP 4.5
├── resolved_sios.json           # STEP 5
├── jit_los.json                 # STEP 5.5
├── judgment.json                # STEP 6
├── quarantine/                  # STEP 7
├── code_snippets.json           # STEP 8.5
├── instruction/                 # STEP 8.6
├── roadmap.json                 # STEP 9 (skeleton)
└── validation_report.json       # STEP 9
```

## 🔗 Liên kết

- **Thiết kế:** `docs/ideas/2026-08-05-unified-roadmap-generation-architecture.md`
- **Progress:** `docs/progress/2026-08-06-pipeline-v3-implementation.md`
- **Master Tree:** `services/python-api/general-context/mlo-knowlege-tree.tsv`
- **Supabase:** `SUPABASE_URL` trong `.env`
