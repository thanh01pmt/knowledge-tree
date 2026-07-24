# 📚 Knowledge Tree Reference Materials (`refs/`)

Thư mục `refs/` lưu trữ các tài nguyên tham chiếu cốt lõi được trích xuất từ codebase **`qms-monorepo`** (`packages/learnwell-platform`) để làm căn cứ phát triển, đối chiếu và mở rộng hệ thống **Knowledge Tree**.

---

## 📂 Cấu Trúc Các Thư Mục Tham Chiếu

| Thư Mục | Vai Trò & Danh Sách File Trích Về |
| :--- | :--- |
| **[`database-schemas/`](./database-schemas/)** | **Cơ sở Dữ liệu & RPCs**: <br>- `public_schema.sql`: Schema DDL 69 bảng Postgres Supabase. <br>- `RPCs.md`: Tài liệu 20+ Stored Procedures PL/pgSQL. <br>- `SUPABASE.md`: Tổng quan kiến trúc CSDL. |
| **[`validation-scripts/`](./validation-scripts/)** | **Script Kiểm Định Integrity**: <br>- `validate_knowledge_tree.py`: Quét toàn vẹn Cây 6 tầng. <br>- `validate-lo-codes.js`: Kiểm tra liên kết Activity $\leftrightarrow$ LO. <br>- `dedup_learning_objectives_codes.py`: Khử trùng mã LO. <br>- `normalize-curriculum-tsv.js`: Format TSV JSON columns. <br>- `compare-lo-codes.js`: So sánh LO giữa các phiên bản. |
| **[`content-ingestion-scripts/`](./content-ingestion-scripts/)** | **Script Phân Rã & Import Nội Dung**: <br>- `import-activities-from-tsv.ts`: Nạp Activity và nối LO qua RPC. <br>- `import-reading-resources.js`: Nạp bài đọc Markdown & gắn LO. <br>- `rewrite-curriculum-from-lessons.js`: Chuẩn hóa mã `COURSE_U01_M01`. <br>- `split-reading-parts.js`: Cắt tài liệu dài thành Micro-Lesson. |
| **[`architecture-docs/`](./architecture-docs/)** | **Nền Tảng Sư Phạm & Kiến Trúc**: <br>- `Kiến Trúc và Lộ Trình Phát Triển Hệ Thống LearnWell.md`: Thiết kế tổng thể. <br>- `Tính phù hợp và phổ quát của mô hình phân loại kiến thức học tập.md`: Lý luận sư phạm & AI Graph Embeddings. |
