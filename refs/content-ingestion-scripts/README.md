# ⚙️ Reference: Content Ingestion & Structuring Scripts

Thư mục này chứa các script tự động hóa quy trình phân rã và nạp nội dung bài học:

- **`import-activities-from-tsv.ts`**: Script TypeScript nạp dữ liệu Hoạt động từ file TSV lên Supabase và tự động gọi RPC `upsert_master_activity_with_los` để gắn mã LOs.
- **`import-reading-resources.js`**: Script nạp bài đọc Markdown (có Frontmatter) vào bảng `learning_resources` và nối N:N với `learning_objectives`.
- **`rewrite-curriculum-from-lessons.js`**: Tự động chuẩn hóa mã phân cấp Curriculum theo dạng `[COURSE]_U[INDEX]_M[INDEX]_L[INDEX]`.
- **`split-reading-parts.js`**: Tự động phân rã các file tài liệu/PDF dài thành các Micro-Reading Parts nguyên tử, slugify mã in hoa và đính kèm Frontmatter LO.
