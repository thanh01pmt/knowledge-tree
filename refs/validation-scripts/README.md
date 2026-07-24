# 🧹 Reference: Validation & Integrity Scripts

Thư mục này chứa các script kiểm định tính toàn vẹn cấu trúc và liên kết dữ liệu:

- **`validate_knowledge_tree.py`**: Kiểm tra toàn vẹn tham chiếu 6 tầng Cây tri thức (`fields` $\rightarrow$ `subjects` $\rightarrow$ `categories` $\rightarrow$ `topics` $\rightarrow$ `concepts` $\rightarrow$ `learning-objectives`), ràng buộc `lo_type` và `parent_lo_code`.
- **`validate-lo-codes.js`**: Kiểm tra liên kết giữa Curriculum TSV (`activities_json`) với `learning-objectives.tsv` để phát hiện mã LO mồ côi hoặc sai định dạng.
- **`dedup_learning_objectives_codes.py`**: Phát hiện và khử trùng lặp mã LO.
- **`normalize-curriculum-tsv.js`**: Chuẩn hóa định dạng TSV, xử lý ký tự tab/line break trong cột JSON.
- **`compare-lo-codes.js`**: So sánh danh sách LO giữa các phiên bản để phát hiện breaking changes.
