# Progress Report: Project Graph v3 (DemoApp-first) — Sandbox `scratch/project-graph-v3`

> **Ngày:** 2026-08-08
> **Phạm vi:** Thiết kế lại Project Graph theo canonical 8-domain model, DemoApp-first, LLM semantics (bỏ embedding resolve).
> **Vị trí:** `scratch/project-graph-v3/` — sandbox cô lập, KHÔNG đụng `scripts/` production.
> **Trạng thái:** 🟢 STEP 0→4 hoàn tất — task-aware roadmap: MVP 11 tasks/38 LOs + EXTEND 1/3. Toàn pipeline v3 đã chứng minh end-to-end.

---

## 1. Bối cảnh & Quyết định thiết kế (đã chốt với Human)

| # | Quyết định | Lý do / Bằng chứng |
|---|---|---|
| D1 | **DemoApp-first**: app learner xây = DemoApp, không phải SDK Core | stream-chat 830 files SDK ≈ 1M tokens, sai đối tượng; DemoApp 70 files ≈ 107k tokens vừa context |
| D2 | **SDK Core chỉ giữ public API dùng trong DemoApp** | 285/989 symbols; index bằng code (regex), không LLM |
| D3 | **Bỏ embedding resolve** — dùng LLM semantics | `Combine` embedding sim 0.04 fail; escalated LLM map đúng Combine→ASYNC_PATTERNS |
| D4 | **Bỏ SDK API index** — verify bằng grep code thật | Không index được n thư viện ngoài; symbol phải tồn tại trong file |
| D5 | **Project Graph = canonical 8 domain** (tham khảo tài liệu Human cung cấp) | Identity/Product/Feature/Architecture/Experience/Data/Implementation/Validation + Knowledge Mapping + Evidence |
| D6 | **FACT vs INFERENCE tách bạch** — file/symbol/keyword = OBSERVED; architecture = INFERRED kèm confidence + evidence | Chống "bịa architecture" |
| D7 | **Intent + Outcome trên task** — WHY → WHAT → HOW | Roadmap không thành danh sách "tạo file, tạo class" |
| D8 | **Project Graph không chứa**: teaching content, bloom, quiz, mastery, lesson sequence | Boundary rõ — thuộc Knowledge/Learner/Curriculum Graph |
| D9 | **STEP E standardize**: 1 LLM call map keyword → 295 concepts (code+name+desc, ~12k tokens); Gap D → đề xuất concept mới + topic/category | Thay step_3 (embedding) + step_3_5 (escalate rời) |
| D10 | **Pipeline mới = 4-5 LLM calls** (STEP C + E + JIT batch) vs cũ ~20+ calls | 7 phút vs 27 phút (đo thật v4) |

## 2. Kiến trúc mục tiêu

```
REPO
  │
  ▼
STEP 0 — Collect & Filter (code)          ← git_tracker (mở rộng)
  Output: tree map (scan-dir) + merged files per type
  │
  ▼
STEP 1 — LLM Project Graph (LLM #1)
  Input: merged source (### FILE: path) + goal + tech-stack
  Output: project_graph_raw.json (8 domain canonical)
  │
  ▼
STEP 2 — Verify (code, evidence OBSERVED)
  Output: project_graph_verified.json + hallucinations[]
  │
  ▼
STEP 3 — Standardize Concepts (LLM #2)
  Input: keywords/api_usage (verified) + 295 concepts tree
  Output: concept_map.json (matched + gap_d_proposals)
  │
  ▼
STEP 4 — JIT + Assemble + Judge
  Output: roadmap.json
```

## 3. Đã hoàn thành

### 3.1 Mở rộng `git_tracker.py` (tham khảo từ qms-monorepo)

**Copy**: `qms-monorepo/packages/learnwell-platform/git_tracker.py` (1765 dòng, bản đầy đủ có dependency analysis) → `scratch/project-graph-v3/scripts/git_tracker.py`.

**So sánh 3 bản tham khảo**: root `qms-monorepo/git_tracker.py` = learnwell (36 methods, 0 khác); quiz-kit (958 dòng) = bản rút gọn thiếu dependency analysis.

**Mở rộng đã làm** (2 args mới):

| Arg | Công dụng | Verified trên stream-chat DemoApp |
|---|---|---|
| `--file-types '{"swift":[".swift"],...}'` | Map extension → loại, thay hardcode TS/JS | `swift_files.txt` = 70 files |
| `--scan-dir DemoApp` | Giới hạn scan/tree chỉ trong thư mục con | 91 files (0 SDK Core), tree chỉ `DemoApp/` |

**Lệnh STEP 0 chuẩn**:
```bash
python scripts/git_tracker.py \
    --project-path /tmp/stream-chat-swift \
    --file-types '{"swift":[".swift"],"python":[".py"],"c_cpp":[".c",".cpp",".ino"]}' \
    --scan-dir DemoApp \
    --initial-scan
```

**Output**: `project_structure.txt` (tree DemoApp) + `<type>_files.txt` (swift/config/markdown/assets/other) + `metadata.json` (commit + hashes).

### 3.2 Backup & an toàn

- Git tag `backup-2026-08-07-before-llm-pg` → commit `438ed09` (trước mọi thay đổi LLM project graph)
- Production `scripts/` giữ nguyên — sandbox tách riêng, commit riêng

## 4. Đang làm / Chưa làm

| Bước | Trạng thái |
|---|---|
| STEP 0 — git_tracker mở rộng | ✅ Hoàn tất (committed) |
| Schema v3 (8 domain canonical) | ✅ `schemas/project_graph.schema.v3.json` + example + tests (Draft-07, D6/D7/D8) |
| STEP 1 — LLM Project Graph (3 calls theo cụm domain) | ✅ + `--profile lite/essential/full` + `--include` + fields A1/A2/A4/C1/C2/C3 |
| STEP 2 — Verify evidence OBSERVED | ✅ `scripts/step2_verify.py` — 21 evidence, 0 hallucination |
| STEP 3 — Standardize (LLM #2, concept bank) | ✅ per-node: 76 mappings (50 MAPPED + 26 Gap D), 53 giữ node_id + `merge_project_graphs.py` |
| STEP 4 — Task-aware Roadmap | ✅ `scripts/step4_roadmap.py` — topo sort, phase theo priority, LO per-task (41 LOs) |
| Test trên smart-bulb + stream-chat | ⬜ |

## 5. Bài học rút ra (từ v4 — pipeline cũ chạy thật)

1. **STEP E concept bank phải = resolved + escalated** (39 concepts), không chỉ resolved (21) → nếu thiếu, LLM bịa concept ngoài bank, milestone rỗng (M1/M2 chỉ còn 1 ULO lọt).
2. **JIT vocabulary = resolved + escalated merged** — collect_resolved_concepts phải nhận escalated đúng cách.
3. **Assemble phải unwrap format mới** `{"project_graph": {...}}` — format cũ mong đợi `{decomposition:...}` trực tiếp.
4. **embedding sai nghĩa tên dev đặt** (`OptionsSelectorViewController`→CSS_SELECTORS 0.59, `UserAnnotation`→USER_PERSONAS) → chính là lý do bỏ embedding, dùng LLM semantics (D3).
5. **Tree có 16 cặp topic/concept trùng** (`ERROR_MSG_PARSING`, `ELECTRONIC_ELEMENTS`...) — di chứng rename, cần chuẩn hóa khi map (D9).

## 6. Files

```
scratch/project-graph-v3/
├── scripts/git_tracker.py       # ✅ Mở rộng --file-types + --scan-dir (committed)
├── schemas/                     # ⬜ project_graph.schema.v3.json
├── tests/                       # ⬜
├── output/                      # ⬜
└── docs/                        # ⬜ (progress này nằm ở docs/progress/ toàn cục)
```
