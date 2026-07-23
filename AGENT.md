# Hướng dẫn dành cho AI Agent (Knowledge Tree)

Chào mừng Agent! Khi bạn hoạt động trong không gian làm việc này (`knowledge-tree`), bạn là một phần của hệ thống sản xuất nội dung tự động dựa trên quy trình **Agentic Pipeline**.

Mục tiêu tối thượng của bạn là xây dựng hệ thống phân cấp tri thức (fields > subjects > categories > topics > concepts) cho các dự án một cách cực kỳ chuẩn xác, bằng cách đối chiếu thông tin với "Nguồn chân lý" (Master Truth).

---

## 🎯 Quy tắc Kiến trúc & Biên soạn Nội dung Bắt buộc (Must-Follow Rules)

### 1. Quy chuẩn Trung tính 100% (Technology-Agnostic / Neutral Rules)
- **Field / Subject / Category / Topic Layer**: 100% Trung tính, không chứa tên công nghệ hay ngôn ngữ lập trình cụ thể.
- **Concept Layer**: **100% TRUNG TÍNH (Mã, Tên, Mô tả)**. Concept đại diện cho khái niệm khoa học máy tính trừu tượng nguyên thủy. **CẤM CHỨA** tên ngôn ngữ/công nghệ (ví dụ: Không dùng `TYPESCRIPT_PRIMITIVES`, `REACT_COMPONENTS`, `DOCKER_CONTAINERS` mà phải chuyển thành `PRIMITIVE_TYPE_ANNOTATIONS`, `COMPONENT_BASED_UI`, `CONTAINER_VIRTUALIZATION_FUNDAMENTALS`).
- **ULO (Universal Learning Objective - `lo_type: UNIVERSAL`)**: **100% TRUNG TÍNH (Mã, Tên, Mô tả)**. Không chứa tên công nghệ cụ thể (ví dụ: `ULO-PRIMITIVE-TYPES-INFERENCE`).
- **CIO (Conceptual Implementation Objective - `lo_type: CONCEPTUAL_IMPL`)**: **100% TRUNG TÍNH (Mã, Tên, Mô tả)**. Định nghĩa năng lực thiết kế/phân tích khái niệm trung tính (ví dụ: `CIO-TYPE-ANNOTATIONS-INFERENCE`).
- **SIO (Specific Implementation Objective - `lo_type: SPECIFIC_IMPL`)**: **TẦNG DUY NHẤT CHỨA CÔNG NGHỆ CỤ THỂ**. SIO mô tả kỹ năng thao tác thực hành trực tiếp với thư viện, công cụ, framework (ví dụ: `SIO-TS-PRIMITIVE-ANNOTATE`, `SIO-REACT-USESTATE-STATE-UPDATE`, `SIO-DOCKER-MULTI-STAGE-BUILD`).

### 2. Mô hình Quan hệ N:N (Many-to-Many Relationships)
- Quan hệ giữa **Concept $\leftrightarrow$ ULO**, **ULO $\leftrightarrow$ CIO**, và **CIO $\leftrightarrow$ SIO** là quan hệ **N:N (Many-to-Many)**.
- Một LO có thể phụ trách nhiều Concepts (phân tách bởi dấu phẩy trong cột `concept_codes`).
- Một LO con có thể thuộc về nhiều LO cha (phân tách bởi dấu phẩy trong cột `parent_lo_code`).

### 3. Tiền tố Câu Mô tả LO Chuẩn hóa
- **100% tất cả các câu mô tả (`description`) trong tệp `learning-objectives.tsv`** (ở cả 3 tầng ULO, CIO, SIO) **BẮT BUỘC** phải bắt đầu bằng cụm từ chuẩn hóa: **`"Người học có khả năng ..."`**.

### 4. Quy mô & Độ phủ Tri thức Cạn kệt ($\ge 80 - 120$ LOs)
- Quy mô của từng roadmap/syllabus rất lớn, do đó **không được tạo dữ liệu hời kẹt, sơ khai** (dưới 80 LOs).
- Mọi dự án phải trích xuất cạn kệt 100% các chủ đề, công cụ, thư viện trong `context/*.json` và `context/*.pdf` với quy mô trung bình **$\ge 80 - 120$ LOs**.
- Bắt buộc phải chạy kiểm tra và đạt **PASS cả 2 script**:
  1. `validate_tree.py`: Referential Integrity (**`[PASS] 0 lỗi`**).
  2. `audit_coverage.py`: Reverse Coverage Audit (**`Coverage Score ≥ 90%`**).

### 5. Cấm Sử dụng Script Thế Chuỗi Tự động Thô ráp (No Dumb Find-and-Replace)
- Tuyệt đối **KHÔNG DÙNG** các script find-and-replace regex cơ học để đổi tên công nghệ thành tên trung tính (gây hiện tượng lặp từ và chắp vá ngữ nghĩa ngớ ngẩn như *"Server Runtime Engine Asynchronous Runtime Engine"*).
- Mọi câu mô tả ULO/CIO/Concept bắt buộc phải được biên soạn ngữ nghĩa tự nhiên, mạch lạc.

### 6. Không Tạo Script Rác ở Thư mục Root
- Không tạo các file script Python tạm thời tại thư mục gốc workspace (`/`). All system automation scripts belong strictly inside `.agents/skills/`.

---

## 🛠️ Tiêu chí Mã hóa & Phân tích Cấp độ Mục tiêu (LO Tree)

1. **Dùng lại mã cũ (Tái sử dụng):**
   - Khi chủ đề trong syllabus là một từ đồng nghĩa, hoặc là một trường hợp cụ thể nằm trong phạm vi của một Concept/Topic đã có trong Master Tree (`general-context/mlo-knowlege-tree.tsv`).
   - Khi độ phủ (overlap) về mặt ý nghĩa đạt trên 70%.

2. **Tạo mã mới (Mở rộng Master Tree):**
   - Mã mới bắt buộc phải tuân theo chuẩn `UPPER_SNAKE_CASE` và chỉ ra rõ node cha.

3. **Cấu trúc LO 3 tầng (ULO -> CIO -> SIO):**
   - **ULO (`lo_type: UNIVERSAL`):** Cột `parent_lo_code` để trống (NULL). Gắn với `concept_codes` trung tính.
   - **CIO (`lo_type: CONCEPTUAL_IMPL`):** Cột `parent_lo_code` chứa mã ULO.
   - **SIO (`lo_type: SPECIFIC_IMPL`):** Cột `parent_lo_code` chứa mã CIO. Tầng thực thi công nghệ cụ thể.

---

## 📋 Thao tác Workflow & Đóng gói Dự án

1. **Khởi tạo:** `python3 .agents/skills/tree-validator/scripts/scaffold_tree.py <project-slug>`
2. **Phân tích Context:** Đọc cạn kệt `projects/<project-slug>/context/`.
3. **Lập Kế hoạch Mapping:** Lưu tại `.work/mapping-plan.md` và chờ phê duyệt.
4. **Đóng gói TSV:** Sau khi được duyệt, ghi 6 file TSV vào `projects/<project-slug>/output/`.
5. **Nghiệm thu:** Chạy `validate_tree.py` và `audit_coverage.py` để đảm bảo **PASS 100%**.
