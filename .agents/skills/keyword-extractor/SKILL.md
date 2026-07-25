---
name: keyword-extractor
description: "Trích xuất Keyword Graph và Concepts từ tài liệu sử dụng LLM-Native GraphRAG architecture."
---

# Keyword Extractor (GraphRAG Pipeline)

Skill này sử dụng mô hình LLM-Native GraphRAG (VD: DeepSeek-v4-flash) để quét toàn bộ tài liệu dự án, trích xuất các Thực thể (Nodes) và Mối quan hệ (Edges), sau đó lọc ra các Khái niệm trung tính (Concepts) để lưu vào cơ sở dữ liệu.

## Output Files
1. `.work/kw/chunks_graph/*.json`: Các đồ thị cục bộ của từng chunk.
2. `output/keyword_graph.json`: Đồ thị toàn cục đã gộp (Flat JSON array nodes/edges tối ưu cho Postgres).
3. `output/concepts.tsv`: Bảng concepts (Trung tính 100%) lấy từ các Node có kết nối cao nhất.

## Các lệnh thực thi (Commands)

### 1. Trích xuất Đồ thị từ Chunk (Phase 1)
```bash
# Phụ thuộc vào file .work/kw/chunks.json đã được sinh ra trước đó
python3 .agents/skills/keyword-extractor/scripts/1_extract_graph_chunks.py --project <project_slug>
```

### 2. Gộp & Xây dựng Đồ thị Toàn cục (Phase 2)
```bash
python3 .agents/skills/keyword-extractor/scripts/2_merge_and_build_graph.py --project <project_slug>
```

### 3. Lọc & Đẩy lên thành Concepts (Phase 3)
```bash
python3 .agents/skills/keyword-extractor/scripts/3_escalate_to_concepts.py --project <project_slug> --top-n 100
```

## Chú ý quan trọng (Quy chuẩn T6)
- File `keyword_graph.json` lưu giữ *tất cả* các khái niệm (kể cả chứa công nghệ như Swift, Python).
- File `concepts.tsv` chỉ lưu giữ các khái niệm TRUNG TÍNH (Technology-Agnostic). Bước 3 sẽ tự động gọi LLM để lọc các Node và ép chuẩn trung tính. Không bao giờ đưa các Node có tính công nghệ vào `concepts.tsv`.
