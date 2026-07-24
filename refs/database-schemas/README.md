# 🗄️ Reference: Database Schemas & RPC Documentation

Thư mục này chứa các sơ đồ cơ sở dữ liệu Postgres và tài liệu chi tiết các hàm RPC của hệ thống Supabase Cloud:

- **`public_schema.sql`**: Schema DDL PostgreSQL hoàn chỉnh của 69 bảng dữ liệu (bao gồm 6 bảng Knowledge Tree, 13 bảng Curriculum, bảng `learning_objective_prerequisites` và `student_mastery`).
- **`RPCs.md`**: Tài liệu kỹ thuật chi tiết về 20+ Stored Procedures (RPCs) được viết bằng PL/pgSQL để thực thi các tác vụ phức tạp (như `update_mastery_after_submission`, `upsert_master_activity_with_los`, `get_content_performance_summary`).
- **`SUPABASE.md`**: Tổng quan kiến trúc CSDL Supabase, quy tắc RLS (Row Level Security), phân quyền người dùng và chiến lược index.
