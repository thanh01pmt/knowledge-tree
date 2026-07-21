# Hướng dẫn dành cho AI Agent (Knowledge Tree)

Chào mừng Agent! Khi bạn hoạt động trong không gian làm việc này (`knowledge-tree`), bạn là một phần của hệ thống sản xuất nội dung tự động dựa trên quy trình **Agentic Pipeline**.

Mục tiêu tối thượng của bạn là xây dựng hệ thống phân cấp tri thức (fields > subjects > categories > topics > concepts) cho các dự án một cách cực kỳ chuẩn xác, bằng cách đối chiếu thông tin với "Nguồn chân lý" (Master Truth).

## Quy tắc bắt buộc (Must-Follow)

1. **Tuân thủ Workflow:** Không bao giờ làm tắt. Bạn CHỈ thực hiện các tác vụ thông qua Slash Commands (vd: `/context-audit`, `/map-taxonomy`). Đọc mô tả chi tiết của từng lệnh trong `.agents/workflows/`.
2. **Context Gate (Nguyên tắc Đầu vào):** 
   - Khởi đầu luôn dùng `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` làm chân lý.
   - Bạn được phép **đề xuất thêm mã (code) mới** vào Master Tree nếu cần thiết, nhưng phải tuân thủ nghiêm ngặt **Tiêu chí tạo mã mới** (xem bên dưới) và phải được Human xác nhận trước khi cập nhật file TSV Master.

## Tiêu chí: Dùng lại mã cũ vs. Tạo mã mới

1. **Dùng lại mã cũ (Tái sử dụng):**
   - Khi chủ đề trong syllabus là một từ đồng nghĩa, hoặc là một trường hợp cụ thể (instance) nằm trọn vẹn trong phạm vi của một Concept/Topic đã có.
   - Khi độ phủ (overlap) về mặt ý nghĩa đạt trên 70%. (Ví dụ: Syllabus ghi "Hàm và thủ tục", Master Tree có `FUNCTIONS` -> Dùng lại `FUNCTIONS`).
2. **Tạo mã mới (Mở rộng Master Tree):**
   - Khi chủ đề là một công nghệ, framework, hoặc khái niệm cốt lõi hoàn toàn mới chưa từng tồn tại trong Master Tree.
   - Khi việc nhét ép chủ đề này vào một mã cũ sẽ làm méo mó định nghĩa ban đầu của mã cũ.
   - Mã mới bắt buộc phải tuân theo chuẩn `UPPER_SNAKE_CASE` và phải chỉ ra rõ nó thuộc về node cha nào.
3. **Phân tích Cấp độ Mục tiêu (ULO - CIO - SIO):**
   Trước khi tiến hành mapping, mọi intent/yêu cầu từ syllabus phải được chẻ nhỏ thành 3 tầng. Lưu ý rằng 3 tầng này tương ứng chính xác với cột `lo_type` trong file `learning-objectives.tsv`:
   - **ULO (Universal Learning Objective - `lo_type: UNIVERSAL`):** Mục tiêu phổ quát. (Vd: "Hiểu vòng lặp xác định"). -> Gắn với `concept_codes` tương ứng (vd: `FOR_LOOP`). Cột `parent_lo_code` để trống (NULL).
   - **CIO (Conceptual Implementation Objective - `lo_type: CONCEPTUAL_IMPL`):** Cách hiện thực hóa khái niệm phổ quát. (Vd: "Dùng vòng lặp for-in trong Swift"). -> Gắn vào `parent_lo_code` là mã ULO ở trên.
   - **SIO (Specific Implementation Objective - `lo_type: SPECIFIC_IMPL`):** Kỹ năng thao tác cực kỳ chi tiết (Vd: "Viết vòng lặp for-in duyệt mảng string"). -> Gắn vào `parent_lo_code` là mã CIO ở trên.
   *Chỉ khi thiết kế bảng LO theo cấu trúc Tree (ULO -> CIO -> SIO) và nối nó vào Concept Codes, bạn mới nhìn thấy những khoảng trống (gap) thực sự trong Master Tree. Từ đó mới quyết định việc có nên tạo Concept/Topic mới hay không.*

4. **Approval Gate (Nguyên tắc Phê duyệt):** 
   - Trạng thái kế hoạch phải được lưu ở `.work/mapping-plan.md`. 
   - Không được phép ghi/thay đổi bất kỳ dữ liệu nào vào thư mục `output/` (nơi chứa 6 file TSV) nếu User chưa xác nhận "Approve" (Đồng ý) kế hoạch mapping.
4. **File is State:** 
   - Đừng cố ghi nhớ mọi thứ trong bộ nhớ ngữ cảnh (context window) của bạn. 
   - Sử dụng ổ đĩa. Đọc tài liệu từ `projects/<project-slug>/context/`. Ghi nháp vào `.work/`. Lưu thành phẩm vào `output/`.

## Danh sách kỹ năng (Skills)

Nếu bạn không chắc chắn phải làm gì với một Slash Command, hãy đọc `SKILL.md` tương ứng trong thư mục `.agents/skills/`:
- **`project-context-loader`**: Kỹ năng đọc hiểu các định dạng file PDF/DOCX trong `context/`.
- **`taxonomy-mapper`**: Kỹ năng tra cứu và so khớp vào cây Master TSV/JSON.
- **`tree-assembler`**: Kỹ năng trích xuất metadata từ Master TSV và ghi vào 6 file TSV của dự án.
- **`tree-validator`**: Kỹ năng chạy script `validate_tree.py` để bắt lỗi tham chiếu (Orphan Node, Broken Reference, v.v.).

## Các thao tác thường dùng

Nếu người dùng yêu cầu phân tích một dự án mới (ví dụ: `swift-associate`):
1. **Kiểm tra trạng thái:** Đọc `status.yaml` xem dự án đang active là gì. Dùng lệnh `cat status.yaml` hoặc đọc trực tiếp.
2. **Khởi tạo:** Nếu cấu trúc chưa có, chạy `python3 .agents/skills/tree-validator/scripts/scaffold_tree.py <project-slug>`.
3. **Phân tích:** Chuyển vai trò sang `@context-analyzer` và đọc thư mục `context/`.
4. **Lập bản đồ:** Chuyển vai trò sang `@taxonomy-mapper` và đề xuất bản đồ. Dừng lại chờ lệnh.
5. **Đóng gói:** Chỉ sau khi được duyệt, chuyển vai trò sang `@tree-assembler` để sinh TSV vào `output/`.

*Hãy tuân thủ các quy tắc trên để giữ cho cây tri thức luôn sạch sẽ, toàn vẹn và không có lỗi!*
