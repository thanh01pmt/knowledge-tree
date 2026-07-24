# 💡 Chiến Lược & Định Hướng Mở Rộng Hệ Thống Knowledge Tree

Tài liệu này lưu trữ các ý tưởng brainstorm định hướng phát triển và mở rộng hệ sinh thái **Knowledge Tree** & **Multi-MCP Hub** trong tương lai.

---

## 🏗️ Tổng Quan Hiện Trạng Hệ Thống
Hệ thống hiện tại đã đạt được các cột mốc nền tảng:
- **Chuẩn hóa Sư phạm**: Anderson-Krathwohl Taxonomy + Marr's 2-Language Tri-Level Test cho CIOs + Mô hình quan hệ N:N giữa Concepts, ULOs, CIOs, SIOs.
- **Multi-MCP Hub Production Server**: FastMCP v3 Server Composition (`mount()`) công khai tại `https://kt-mcp.orchable.xyz/mcp`.
- **Tự động hóa CI/CD & Cloud Infrastructure**: Chạy Docker Container trên Oracle Cloud VM với GitHub Actions CI/CD (nhánh `stable`).

---

## 🚀 4 Hướng Mở Rộng Chiến Lược

### 1. 🤖 Tầng Sinh Nội Dung & Đánh Giá Tự Động (AI-Native Learning Engine)

Tận dụng cấu trúc tri thức đã chuẩn hóa để phát triển các Sub-MCP Tools tự động tạo tài liệu học tập & đánh giá:

* **`kt_generate_quiz` (Trình tạo Đề thi / Trắc nghiệm chuẩn Bloom)**:
  - Dựa vào mã ULO/CIO, tự động gọi LLM sinh câu hỏi trắc nghiệm hoặc bài tập lập trình.
  - Phân loại rõ nét theo 4 Knowledge Dimensions (`FACTUAL`, `CONCEPTUAL`, `PROCEDURAL`, `METACOGNITIVE`).
  - Kiểm tra trực tiếp khả năng hiểu bản chất (Relational Understanding - Skemp).
* **`kt_generate_micro_lesson` (Trình sinh Bài học Siêu ngắn)**:
  - Tự động sinh Flashcard hoặc micro-lesson (đọc trong 3 phút) bám sát các tiêu chí SIO (`lo_type: SPECIFIC_IMPL`) cho ngôn ngữ/công cụ cụ thể (Python, Swift, GraphQL,...).

---

### 2. 🔌 Bổ Sung Các Sub-MCP Server Mới Vào Hub (`mcp/servers/`)

Mở rộng danh sách Sub-Server trong `https://kt-mcp.orchable.xyz/mcp` để phục vụ nhiều tác vụ chuyên biệt hơn:

* **`crawler` Server (`mcp/servers/crawler_server.py`)**:
  - `crawler_crawl_roadmap(url)`: Tự động cào và phân tích đồ thị tri thức từ roadmap.sh, Coursera, Khan Academy.
  - `crawler_parse_pdf_syllabus(file)`: Đọc và tự động phân tích khung chương trình học từ PDF/Docx của trường đại học.
* **`tracing` Server (Hệ thống Theo dõi Năng lực Học viên)**:
  - `tracing_calculate_mastery(user_id, concept_code)`: Áp dụng thuật toán **Bayesian Knowledge Tracing (BKT)** hoặc **IRT** để đo lường mức độ thành thục của người học trên đồ thị tri thức.
  - `tracing_recommend_next_lo(user_id)`: Đề xuất bài học tối ưu tiếp theo (Next Best Learning Objective) dựa trên lỗ hổng tri thức.
* **`governance` Server (Quản trị Master Tree)**:
  - `gov_propose_master_merge`: Tự động tạo **GitHub PR** khi một dự án con phát hiện các Node tri thức mới đạt chuẩn cần đưa vào Master Tree (`mlo-knowlege-tree.tsv`).

---

### 3. 🎨 Visualizer & Interactive UI (Giao diện Trực quan hóa Đồ thị)

* **Tận dụng FastMCP v3 Generative UI / Prefab Apps**:
  - Tận dụng tính năng `@mcp.tool(app=True)` của FastMCP v3 để trả về giao diện UI tương tác (React Flow / D3.js) trực tiếp trong cửa sổ chat của AI Agent.
  - Người học hoặc Giáo viên gọi tool `kt_visualize_tree` sẽ xem được Sơ đồ Đồ thị DAG Tri thức trực quan ngay lập tức.
* **Knowledge Tree Visual Dashboard (Next.js + Supabase)**:
  - Xây dựng Web App cho phép Giáo viên kéo-thả (Drag & Drop) chỉnh sửa liên kết N:N giữa **Concept $\leftrightarrow$ ULO $\leftrightarrow$ CIO $\leftrightarrow$ SIO** trực tiếp trên giao diện đồ họa.

---

### 4. 🔒 Enterprise Security, Auth & Metrics

* **Phân quyền người dùng (Role-Based Access Control - RBAC)**:
  - Tích hợp `fastmcp.auth` với OAuth/JWT token:
    - **Guest / Student**: Chỉ được gọi các Tool đọc public (`sys_*`, `kt_generate_quiz`).
    - **Teacher / Admin**: Được gọi các Tool chỉnh sửa/đồng bộ DB (`kt_sync_supabase`, `kt_scaffold_project`).
* **OpenTelemetry (OTEL) Observability**:
  - Đo lường tần suất tra cứu các Node tri thức, theo dõi lộ trình học tập nào được quan tâm nhiều nhất.
