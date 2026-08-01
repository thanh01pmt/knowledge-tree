---
name: keyword-extractor
description: Vét cạn thuật ngữ chuyên ngành (Automatic Term Extraction) từ tài liệu nguồn theo một chủ đề mục tiêu cho trước. Dùng pipeline lai: YAKE statistical + LLM candidate-gen → embedding filter → LLM dedup + omission-check loop. Output tương thích làm input cho /context-audit.
---

# Keyword Extractor (ATE Pipeline)

> **Goal:** Trích xuất kiệt tất cả thuật ngữ liên quan đến `target_context` từ tài liệu nguồn (PDF/MD/TXT). Tối ưu cho **recall** — không bỏ sót, kể cả thuật ngữ chỉ xuất hiện 1 lần — sau đó dedup và kiểm tra omission để đảm bảo độ đầy đủ.

---

## Vì sao pipeline nhiều tầng

Single-pass (RAKE/YAKE/LLM 1 lần) không đủ vì hai nguồn lỗi khác nhau:

- **Statistical (YAKE):** đánh giá thấp thuật ngữ hiếm (tần suất 1).
- **LLM 1 lượt trên tài liệu dài:** attention suy giảm giữa tài liệu → bỏ sót phần giữa.

Pipeline này kết hợp cả hai track, filter domain-relevance rồi mới dedup + omission-check.

---

## Quality Rules (Bắt Buộc)

1. **Recall-First Filtering** — Ngưỡng cosine ở `filter_by_relevance.py` PHẢI lỏng (default `≥ 0.25`). Precision được xử lý ở `llm_verify_and_dedup.py`. Loại sớm không phục hồi được ở bước sau.
2. **No Self-Curating Prompts** — Prompt LLM candidate-gen PHẢI tường minh: _"liệt kê MỌI thuật ngữ, kể cả xuất hiện 1 lần, KHÔNG lọc theo mức độ quan trọng."_
3. **Omission-Check In-Context** — Không tách omission-check thành lượt gọi riêng biệt. Model PHẢI thấy toàn bộ danh sách hiện có + chunk gốc trong CÙNG 1 lượt gọi.
4. **Source Traceability** — Mọi term trong output PHẢI mang `source_chunks` (chunk_id nguồn) và `first_extraction_method` (statistical / llm / omission_check).
5. **Omission Loop Limit** — Tối đa 2 vòng lặp omission-check. Dừng sớm nếu vòng nào Δ = 0 (không term mới).

---

## Inputs

- `target_context` — Chuỗi mô tả chủ đề mục tiêu (VD: `"Lập trình Arduino cho ESP32-S3 làm sản phẩm IoT"`)
- Source files: PDF, MD, hoặc TXT trong `projects/<project>/context/` hoặc path tùy ý
- `OPENAI_API_KEY` trong `.env` (cho LLM + embedding scripts)

## Outputs

| File                                   | Mô tả                                                    |
| -------------------------------------- | -------------------------------------------------------- |
| `.work/kw/chunks.json`                 | Chunks với heading_trail                                 |
| `.work/kw/candidates_statistical.json` | YAKE candidates                                          |
| `.work/kw/candidates_llm.json`         | LLM candidates                                           |
| `.work/kw/candidates_filtered.json`    | Union filtered by embedding cosine                       |
| `.work/kw/candidates_filtered.md`      | Preview markdown cho agent xem nhanh                     |
| `.work/kw/keywords_verified.json`      | Sau dedup + omission-check                               |
| `.work/kw/verify-report.md`            | **Điểm duyệt người**: trước/sau, delta từ omission-check |
| `output/keywords.tsv`                  | Output cuối (6 cột: term, aliases, relevance_score, source_chunks, first_extraction_method, category)                                      |
| `output/keywords.json`                 | Output cuối dạng JSON                                    |

---

## Scripts

```
.agents/skills/keyword-extractor/scripts/
├── chunk_source.py              # ❌ LLM  — cắt nguồn theo heading, PDF/MD/TXT
├── gen_statistical_candidates.py # ❌ LLM  — YAKE trên từng chunk
├── llm_gen_candidates.py        # ✅ LLM  — liệt kê vét cạn per-chunk
├── filter_by_relevance.py       # ⚠️ embed — cosine vs target-context (lỏng)
├── llm_verify_and_dedup.py      # ✅ LLM  — dedup biến thể + omission loop
├── export_keywords.py           # ❌ LLM  — ghi TSV/JSON output cuối
└── llm_escalate_concepts.py     # ✅ LLM  — keyword → concept trung tính + match Master Tree
```

---

## Workflow Commands

| Command                                       | Owner                | LLM? | Kết quả                                                             |
| --------------------------------------------- | -------------------- | ---- | ------------------------------------------------------------------- |
| `/scaffold-keywords <target> --source <path>` | scaffolder           | ❌   | Tạo `.work/kw/`, ghi config                                         |
| `/extract-terms`                              | `@keyword-extractor` | ✅   | `candidates_filtered.md`                                            |
| `/verify-terms`                               | `@keyword-extractor` | ✅   | `verify-report.md` ← **điểm duyệt**                                 |
| `/finalize-keywords`                          | `@keyword-extractor` | ❌   | `output/keywords.tsv` + inject vào context-audit                    |
| `/escalate-concepts`                          | `@keyword-extractor` | ✅   | `concept_candidates.tsv` + `concept_escalation.md` ← **điểm duyệt** |

---

## Tích hợp với `/context-audit`

Sau `/finalize-keywords`, agent sẽ:

1. Copy `output/keywords.tsv` vào `projects/<project>/context/keywords.tsv`
2. Cập nhật `projects/<project>/.work/context-audit.md` thêm section **`## ATE Keywords`** chứa danh sách term đã vét cạn
3. `@context-analyzer` khi chạy `/context-audit` sẽ kiểm tra sự tồn tại của `keywords.tsv` và tích hợp vào domain breakdown

---

## Run Sequence

```bash
# Bước 1: Scaffold (không cần API key)
# /scaffold-keywords "Arduino ESP32-S3 IoT" --source projects/<slug>/context/

# Bước 2: Extract (cần OPENAI_API_KEY)
# /extract-terms

# Bước 3: Verify + duyệt verify-report.md
# /verify-terms

# Bước 4: Finalize (inject vào context-audit)
# /finalize-keywords
```

## Dependencies

```bash
pip install pdfplumber yake numpy openai pydantic
```

---

## Alternative/Experimental Pipeline: GraphRAG

> ⚠️ Pipeline dưới đây là thử nghiệm (experimental), không được dùng trong workflow chuẩn (`/run-pipeline`). Giữ lại để tham khảo.

Skill này sử dụng mô hình LLM-Native GraphRAG để quét toàn bộ tài liệu dự án, trích xuất các Thực thể (Nodes) và Mối quan hệ (Edges), sau đó lọc ra các Khái niệm trung tính (Concepts).

### Output Files (GraphRAG)

1. `.work/kw/chunks_graph/*.json`: Các đồ thị cục bộ của từng chunk.
2. `output/keyword_graph.json`: Đồ thị toàn cục đã gộp (Flat JSON array nodes/edges tối ưu cho Postgres).
3. `output/concepts.tsv`: Bảng concepts (Trung tính 100%) lấy từ các Node có kết nối cao nhất.

### Scripts (GraphRAG)

```bash
# Phase 1: Trích xuất Đồ thị từ Chunk
python3 .agents/skills/keyword-extractor/scripts/1_extract_graph_chunks.py --project <project_slug>

# Phase 2: Gộp & Xây dựng Đồ thị Toàn cục
python3 .agents/skills/keyword-extractor/scripts/2_merge_and_build_graph.py --project <project_slug>

# Phase 3: Lọc & Đẩy lên thành Concepts
python3 .agents/skills/keyword-extractor/scripts/3_escalate_to_concepts.py --project <project_slug> --top-n 100
```

### Chú ý (Quy chuẩn T6)

- File `keyword_graph.json` lưu giữ _tất cả_ các khái niệm (kể cả chứa công nghệ như Swift, Python).
- File `concepts.tsv` chỉ lưu giữ các khái niệm TRUNG TÍNH (Technology-Agnostic). Bước 3 sẽ tự động gọi LLM để lọc các Node và ép chuẩn trung tính.
