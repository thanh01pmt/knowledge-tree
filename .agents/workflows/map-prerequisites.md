---
description: Phase E (ADR-0005) — Sinh DAG tiền đề giữa các LO qua 4-Bước: Domain Partitioning → Concept DAG (LLM) → ULO Derivation → LLM Verify.
---

# Workflow: Map Prerequisites

> Phase E: Sinh `lo_prerequisites.tsv` và cập nhật `concepts.tsv` (cột `prerequisite_concept_codes`) qua kiến trúc 4-Bước ADR-0005.

**Command:** `/map-prerequisites`
**Owner:** `@tree-assembler`
**ADR:** [ADR-0005: Domain-Partitioned Concept DAG + LLM Verify](docs/adr/adr-0005-domain-partitioned-concept-dag-prerequisite-mapping.md)
**Supersedes:** ADR-0004 (3-Layer Structural → Syllabus Structure → LLM Gap-fill)

## Prerequisites

- `/generate-sios` (hoặc Phase Merge) đã hoàn tất → `output/learning-objectives.tsv` tồn tại.
- `output/concepts.tsv` tồn tại (để Domain Partitioning).
- `output/classified_action_phrases.json` tồn tại (từ `/escalate-concepts` — dùng làm context nhưng không bắt buộc).

## Contract

```bash
python3 .agents/skills/learning-objective-generator/scripts/llm_map_prerequisites.py \
  --project <slug> \
  [--dry-run] [--no-verify] [--reuse-concept-dag]
```

### Flags

| Flag | Mô tả |
|---|---|
| `--dry-run` | In candidate DAG + verify results ra stdout, KHÔNG ghi TSV. Dùng để review trước khi ghi. |
| `--no-verify` | Bỏ Bước 5 (LLM verify). Chỉ chạy Bước 1+2+4. Nhanh hơn nhưng không filter false positives. |
| `--reuse-concept-dag` | Dùng `.work/concept_dag.tsv` có sẵn, skip Bước 2 (LLM Concept DAG). Tiết kiệm ~10 phút LLM calls khi re-run chỉ để verify/ghi. |

### 4 Bước (ADR-0005)

1. **Bước 1 — Domain Partitioning** (0% LLM, 100% deterministic): chia concepts theo `topic_codes`. Prereq chỉ tìm trong cùng topic. Giảm search space n×n → nhiều cặp nhỏ.
2. **Bước 2 — Concept-Level DAG per-domain** (LLM có constraint): với mỗi topic (~10-15 concepts), LLM build DAG. Mỗi link BẮT BUỘC justify theo 1 trong 2 mẫu:
   - **Tool dependency**: "B sử dụng A làm công cụ/khái niệm nền"
   - **Conceptual foundation**: "B mở rộng/kế thừa A"
   - Chạy 2 lần + majority vote (union) để giảm non-determinism.
3. **Bước 4 — ULO-Level Derivation** (deterministic): concept DAG → ULO DAG. ULO representative = bloom thấp nhất. Giữ L1-BLOOM (CIO/SIO trong cùng parent).
4. **Bước 5 — Phép thử ngược** (LLM verify từng link): với mỗi link A→B, LLM trả lời *"Sinh viên đã hiểu mọi concept TRỪ A. Có thể hiểu/làm B không?"*
   - "NO" → GIỮ (A là prereq bắt buộc)
   - "YES"/"PARTIAL" → DROP (A không phải prereq bắt buộc)

### Output Files

```
output/
├── lo_prerequisites.tsv       ← final output (6 cột: target, prereq, rationale, source_layer, justification, counterfactual_test)
├── concepts.tsv               ← updated (thêm cột prerequisite_concept_codes)
└── .work/
    └── concept_dag.tsv        ← concept-level DAG audit trail (có confidence_runs 2/2)
```

### Source Layers

| source_layer | Ý nghĩa |
|---|---|
| `L1-BLOOM-CIO` | CIO trong cùng ULO, chain theo Bloom level (deterministic) |
| `L1-BLOOM-SIO` | SIO trong cùng CIO, chain theo Bloom level (deterministic) |
| `L4-CONCEPT-DAG` | ULO link từ concept DAG (chưa verify) |
| `L5-VERIFIED` | ULO link đã pass phép thử ngược Bước 5 |

### Cycle Detection

Sau khi merge tất cả links, chạy Kahn topological sort để đảm bảo **acyclic**. Nếu phát hiện cycle, drop edge theo priority: L5-VERIFIED > L4-CONCEPT-DAG > L1-BLOOM (giữ deterministic, drop LLM first).

## After This Step

```bash
# 1. Validate structural integrity
/validate-tree

# 2. Sync 7 tables to Supabase (bao gồm lo_prerequisites + concepts mới)
/sync-supabase
```

## Acceptance Criteria

Script được coi là PASS khi:
1. Acyclic (Kahn topological sort).
2. Tổng links sau verify ∈ **[20, 60]**.
3. ≥95% L5-VERIFIED links có justification thuộc 1 trong 2 mẫu (tool dependency / conceptual foundation).
4. `validate_tree.py` PASS.
5. Coverage: ≥25% ULO có ≥1 prereq link.

## Notes

- **Thời gian chạy**: ~10-25 phút (2 runs Bước 2 + verify từng link). Dùng `--reuse-concept-dag` cho re-run nhanh hơn.
- **LLM model**: mặc định `deepseek-v4-flash:cloud`, override qua `--model`.
- **Human Review (Bước 6)**: TSV có cột `justification` + `counterfactual_test` để human review sau.