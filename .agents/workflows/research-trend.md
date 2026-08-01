---
description: Tự động nghiên cứu xu hướng công nghệ bằng last30days, Exa và Crawl4AI, sau đó trích xuất khái niệm mới và đề xuất cập nhật vào Master Tree thông qua quy trình phê duyệt Staging.
---

# Workflow: Research Technology Trend & Expand Knowledge Tree

> **Rule:** Bất kỳ kiến thức mới nào được khám phá từ Internet đều phải trải qua Phép thử Marr 2-Ngôn-ngữ (nếu là CIO) và tuân thủ tuyệt đối quy tắc **100% Trung tính** cho các Concept, Topic. Hệ thống không ghi đè trực tiếp mà phải thông qua Staging Diff Report để người dùng phê duyệt (HITL).

**Command:** `/research-trend "<Topic/Keyword>"`  
**Owner:** `@knowledge-researcher`

---

## 🔄 5-Phase Automated Research Pipeline

### Giai đoạn 1: Discovery (Khám phá & Lắng nghe Xu hướng)

1. **Lắng nghe Mạng xã hội & Cộng đồng Dev**:
   - Sử dụng **`last30days`** skill để quét X, Reddit, Hacker News, GitHub về `<Topic/Keyword>` trong 30 ngày qua.
   - Báo cáo tóm tắt những khái niệm thực tế mà cộng đồng đang quan tâm nhất.
2. **Deep Tech Search**:
   - Sử dụng **Exa MCP** để tìm kiếm các bài viết sâu, tài liệu chính thức, và whitepaper liên quan đến từ khóa.

### Giai đoạn 2: Extraction (Đọc hiểu & Trích xuất)

3. **Cào & Phân tích nội dung**:
   - Sử dụng **Crawl4AI MCP** để tải nội dung chi tiết từ các URL chất lượng nhất tìm được ở Giai đoạn 1.
4. **Trích xuất Thuật ngữ & Khái niệm**:
   - Chạy kịch bản LLM (tương tự quy trình ATE) để bóc tách các *Thuật ngữ (Keywords)* và *Khái niệm (Concepts)* mới.
   - Lưu trữ tạm thời danh sách vào `.work/research/<topic>_candidates.md`.

### Giai đoạn 3: Mapping & Gap Detection (Đối chiếu Master Tree)

5. **Lọc và Tái sử dụng (N:N Reuse)**:
   - Đối chiếu danh sách Concept mới với Master Tree hiện tại (`.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv`).
   - Loại bỏ trùng lặp. Nếu khái niệm mới có thể ghép vào Category/Topic hiện tại, thực hiện ghép N:N.
   - Những khái niệm thực sự mới (Gap D) sẽ được chuẩn bị để đưa vào Staging.
6. **Kiểm tra Trung tính & Cú pháp Danh từ**:
   - Chuyển đổi mọi concept sang định dạng Noun Phrase và trung tính công nghệ.

### Giai đoạn 4: Proposal & HITL (Đề xuất & Phê duyệt)

7. **Lập Báo cáo Khác biệt (Diff Report)**:
   - Chạy script so sánh (tương tự `tree_diff.py`) để sinh ra báo cáo `.work/research_diff_report.md`.
   - Báo cáo phải thể hiện rõ: [NEW CONCEPT], [MODIFIED TOPIC], và danh sách các ULO/CIO dự kiến (nếu có sinh kèm).
8. **🛑 HITL Checkpoint: Phê duyệt Merge**:
   - Hệ thống dừng lại và yêu cầu người dùng xem xét file `research_diff_report.md`.

### Giai đoạn 5: Merge & Sync (Hợp nhất)

9. **Merge vào Master Tree**:
   - Sau khi người dùng phê duyệt, chạy script `sync_back_master.py` (của `@roadmap-aligner`) hoặc tương đương để hợp nhất các thay đổi vào Master Tree.
10. **Sinh Learning Objectives bổ sung**:
    - Tự động kích hoạt `@tree-assembler` để chạy `/generate-ulos` và `/generate-cios` (có Phép thử Marr) cho các khái niệm mới được bổ sung.
