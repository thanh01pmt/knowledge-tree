# Gap Detection Report

- **Project:** `swift-associate`
- **Generated:** 2026-07-25T12:47:05.029037+00:00

---

## Gap A — Concepts Without Any LO (`CONCEPT_WITHOUT_LO`)

> Các concept trong `concepts.tsv` không có LO nào trỏ đến. Cần bổ sung LO để đảm bảo độ phủ.

✅ **Tất cả concepts đều có ít nhất 1 LO trỏ đến.**

---

## Gap B — Shallow CIOs (`CIO_INSUFFICIENT_SIO`)

> CIO có ít hơn 2 SIO con → phân rã chưa đủ chi tiết theo mô hình sư phạm.

**56 CIO(s) có < 2 SIO:**

| CIO Code | CIO Name | SIO Count | Parent ULO |
|---|---|---|---|
| `CIO-VIEW_CONCEPT-01-01` | Classify UI components based on view criteria | ❌ 0 | `ULO-VIEW_CONCEPT-01` |
| `CIO-VIEW_CONCEPT-02-01` | Analyze interaction flow between user and view | ❌ 0 | `ULO-VIEW_CONCEPT-02` |
| `CIO-VIEW_CONCEPT-03-01` | Model view as an encapsulated unit of visual and behavioral properties | ❌ 0 | `ULO-VIEW_CONCEPT-03` |
| `CIO-DATA_TYPES-01-01` | Classify values into basic data types | ❌ 0 | `ULO-DATA_TYPES-01` |
| `CIO-DATA_TYPES-02-01` | Compare storage characteristics of basic data types | ❌ 0 | `ULO-DATA_TYPES-02` |
| `CIO-CONTROL_FLOW-02-02` | Xác định đường đi thực thi dựa trên điều kiện đầu vào | ❌ 0 | `ULO-CONTROL_FLOW-02` |
| `CIO-CONTROL_FLOW-03-01` | Kiểm tra tính đầy đủ của các nhánh rẽ và điều kiện dừng vòng lặp | ❌ 0 | `ULO-CONTROL_FLOW-03` |
| `CIO-CONTROL_FLOW-03-02` | Phát hiện lỗi logic như vòng lặp vô hạn hoặc nhánh không bao phủ | ❌ 0 | `ULO-CONTROL_FLOW-03` |
| `CIO-TYPE_SYSTEM-01-01` | Phân loại kiểu dữ liệu dựa trên đặc điểm lưu trữ và phạm vi | ❌ 0 | `ULO-TYPE_SYSTEM-01` |
| `CIO-TYPE_SYSTEM-01-02` | Nhận diện kiểu tĩnh và kiểu động dựa trên thời điểm kiểm tra | ❌ 0 | `ULO-TYPE_SYSTEM-01` |
| `CIO-TYPE_SYSTEM-02-01` | Phân tích quá trình kiểm tra kiểu tĩnh | ❌ 0 | `ULO-TYPE_SYSTEM-02` |
| `CIO-TYPE_SYSTEM-02-02` | Áp dụng suy luận kiểu để suy ra kiểu của biểu thức | ❌ 0 | `ULO-TYPE_SYSTEM-02` |
| `CIO-TYPE_SYSTEM-03-01` | Phân tích thông báo lỗi kiểu để xác định nguyên nhân gốc rễ | ❌ 0 | `ULO-TYPE_SYSTEM-03` |
| `CIO-TYPE_SYSTEM-03-02` | Xác định lỗi kiểu bằng cách mô phỏng luồng kiểu trong chương trình | ❌ 0 | `ULO-TYPE_SYSTEM-03` |
| `CIO-VISUAL_DESIGN-01-01` | Phân tích tác động của nguyên tắc tương phản đến khả năng đọc và thu hút sự chú ý | ❌ 0 | `ULO-VISUAL_DESIGN-01` |
| `CIO-VISUAL_DESIGN-01-02` | Áp dụng nguyên tắc cân bằng để phân bố trọng lượng thị giác trong bố cục | ❌ 0 | `ULO-VISUAL_DESIGN-01` |
| `CIO-VISUAL_DESIGN-02-01` | Tạo bố cục lưới dựa trên tỷ lệ vàng để đạt được sự hài hòa | ❌ 0 | `ULO-VISUAL_DESIGN-02` |
| `CIO-VISUAL_DESIGN-02-02` | Sắp xếp các thành phần giao diện theo nguyên tắc gần nhau để nhóm thông tin liên quan | ❌ 0 | `ULO-VISUAL_DESIGN-02` |
| `CIO-VISUAL_DESIGN-03-01` | Phân tích hiệu quả của bảng màu dựa trên tâm lý học màu sắc | ❌ 0 | `ULO-VISUAL_DESIGN-03` |
| `CIO-VISUAL_DESIGN-03-02` | Đánh giá tác động của khoảng trắng đến khả năng đọc và tập trung | ❌ 0 | `ULO-VISUAL_DESIGN-03` |
| `CIO-VISUAL_DESIGN-04-01` | Apply visual evaluation criteria to analyze interface design | ❌ 0 | `ULO-VISUAL_DESIGN-04` |
| `CIO-VISUAL_DESIGN-04-02` | Compare design against standard design principles to identify strengths and weaknesses | ❌ 0 | `ULO-VISUAL_DESIGN-04` |
| `CIO-SECURITY_CHALLENGES-01-01` | Classify security challenges based on origin and impact | ❌ 0 | `ULO-SECURITY_CHALLENGES-01` |
| `CIO-SECURITY_CHALLENGES-01-02` | Use a checklist of indicators to identify the type of security challenge | ❌ 0 | `ULO-SECURITY_CHALLENGES-01` |
| `CIO-SECURITY_CHALLENGES-02-01` | Analyze the impact of a security challenge on integrity, confidentiality, and availability | ❌ 0 | `ULO-SECURITY_CHALLENGES-02` |
| `CIO-SECURITY_CHALLENGES-02-02` | Evaluate the severity of impact based on predefined criteria | ❌ 0 | `ULO-SECURITY_CHALLENGES-02` |
| `CIO-SECURITY_CHALLENGES-03-01` | Apply root cause analysis to identify the origin of a security incident | ❌ 0 | `ULO-SECURITY_CHALLENGES-03` |
| `CIO-SECURITY_CHALLENGES-03-02` | Construct a cause-effect chain from a security incident | ❌ 0 | `ULO-SECURITY_CHALLENGES-03` |
| `CIO-DEBUGGING-01-01` | Execute a sequential debugging process consisting of reproduce, isolate, fix, and test | ❌ 0 | `ULO-DEBUGGING-01` |
| `CIO-DEBUGGING_02-01` | Thiết lập điểm dừng có điều kiện để kiểm tra trạng thái | ❌ 0 | `ULO-DEBUGGING-02` |
| `CIO-DEBUGGING_02-02` | Sử dụng nhật ký (logging) có cấp độ để theo dõi hành vi | ❌ 0 | `ULO-DEBUGGING-02` |
| `CIO-DEBUGGING_02-03` | Thực thi từng bước (step-through) để quan sát luồng điều khiển | ❌ 0 | `ULO-DEBUGGING-02` |
| `CIO-DEBUGGING_03-01` | Áp dụng phương pháp loại trừ nhị phân trên mã nguồn | ❌ 0 | `ULO-DEBUGGING-03` |
| `CIO-DEBUGGING_03-02` | Truy vết nguyên nhân gốc rễ bằng kỹ thuật 5 Whys | ❌ 0 | `ULO-DEBUGGING-03` |
| `CIO-OBJECT_INSTANTIATION_01-01` | Mô tả quy trình cấp phát bộ nhớ và khởi tạo đối tượng | ❌ 0 | `ULO-OBJECT_INSTANTIATION-01` |
| `CIO-OBJECT_INSTANTIATION_01-02` | Phân tích vai trò của tham số trong khởi tạo đối tượng | ❌ 0 | `ULO-OBJECT_INSTANTIATION-01` |
| `CIO-OBJECT_INSTANTIATION_02-01` | Gọi hàm tạo với tham số phù hợp để khởi tạo đối tượng | ❌ 0 | `ULO-OBJECT_INSTANTIATION-02` |
| `CIO-OBJECT_INSTANTIATION_02-02` | Sử dụng giá trị mặc định và khởi tạo không tham số | ❌ 0 | `ULO-OBJECT_INSTANTIATION-02` |
| `CIO-OBJECT_INSTANTIATION_03-01` | So sánh khởi tạo trực tiếp và phương thức factory | ❌ 0 | `ULO-OBJECT_INSTANTIATION-03` |
| `CIO-OBJECT_INSTANTIATION_03-02` | Phân tích dependency injection như một cách tạo đối tượng | ❌ 0 | `ULO-OBJECT_INSTANTIATION-03` |
| `CIO-EVENT_HANDLERS_CONCEPT-01-01` | Event-Driven Programming Pattern | ❌ 0 | `ULO-EVENT_HANDLERS_CONCEPT-01` |
| `CIO-EVENT_HANDLERS_CONCEPT-01-02` | Event Flow and Handler Invocation | ❌ 0 | `ULO-EVENT_HANDLERS_CONCEPT-01` |
| `CIO-EVENT_HANDLERS_CONCEPT-02-01` | Registering Callback to UI Element Event | ❌ 0 | `ULO-EVENT_HANDLERS_CONCEPT-02` |
| `CIO-EVENT_HANDLERS_CONCEPT-03-01` | Event Propagation and Prevention | ❌ 0 | `ULO-EVENT_HANDLERS_CONCEPT-03` |
| `CIO-EVENT_HANDLERS_CONCEPT-03-02` | Handling Multiple Events on Same Element | ❌ 0 | `ULO-EVENT_HANDLERS_CONCEPT-03` |
| `CIO-OBJECT_PROPERTIES-01-01` | Identifying Object Properties as Key-Value Pairs | ❌ 0 | `ULO-OBJECT_PROPERTIES-01` |
| `CIO-OBJECT_PROPERTIES-02-01` | Using Properties to Manage Object State | ❌ 0 | `ULO-OBJECT_PROPERTIES-02` |
| `CIO-OBJECT_PROPERTIES-03-1` | Truy xuất và cập nhật trạng thái thực thể qua trường dữ liệu | ❌ 0 | `ULO-OBJECT_PROPERTIES-03` |
| `CIO-OBJECT_PROPERTIES-03-2` | Kiểm soát truy cập trạng thái thực thể qua phương thức truy cập | ❌ 0 | `ULO-OBJECT_PROPERTIES-03` |
| `CIO-RETURN_VALUES_AND_SCOPE-01-1` | Nhận diện cấu trúc kết thúc và trả về kết quả | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-01` |
| `CIO-RETURN_VALUES_AND_SCOPE-01-2` | Phân biệt phạm vi biến dựa trên vị trí khai báo | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-01` |
| `CIO-RETURN_VALUES_AND_SCOPE-02-1` | Giải thích phạm vi biến và cơ chế trả về giá trị | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-02` |
| `CIO-RETURN_VALUES_AND_SCOPE-02-2` | Mô tả mối quan hệ giữa phạm vi biến và khả năng truy cập dữ liệu | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-02` |
| `CIO-RETURN_VALUES_AND_SCOPE-03-1` | Viết hàm có sử dụng return và quản lý phạm vi biến | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-03` |
| `CIO-RETURN_VALUES_AND_SCOPE-03-2` | Thiết kế hàm với biến cục bộ và toàn cục, kiểm soát luồng dữ liệu ra ngoài | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-03` |
| `CIO-RETURN_VALUES_AND_SCOPE-03-3` | Sử dụng giá trị trả về làm đầu vào cho xử lý khác, quản lý phạm vi | ❌ 0 | `ULO-RETURN_VALUES_AND_SCOPE-03` |

**→ Action:** Mỗi CIO cần ít nhất 2 SIO để phân rã đủ chi tiết thực hành.
---

## Gap D — Marr's Test Violated CIOs (`MARR_VIOLATION`)

> CIO chứa từ khóa công nghệ, cú pháp hoặc cấu trúc ngôn ngữ cụ thể — vi phạm Phép thử Marr 2-Ngôn-ngữ.

**2 CIO(s) vi phạm tính Trung tính (Marr Test):**

| CIO Code | CIO Name | Detected Keywords / Patterns |
|---|---|---|
| `CIO-VISUAL_DESIGN-04-01` | Apply visual evaluation criteria to analyze interface design | `interface` |
| `CIO-OBJECT_INSTANTIATION_03-01` | So sánh khởi tạo trực tiếp và phương thức factory | `class` |

**→ Action:** Viết lại mô tả/tên CIO thành khái niệm/thủ tục trung tính 100% độc lập ngôn ngữ, hoặc chuyển xuống tầng SIO.
---

## Gap C — Master Tree Candidates (`MASTER_CANDIDATE`)

> Concepts từ `master_tree.json` **chưa có trong project** nhưng keyword-match với syllabus (score ≥ 2.0).
> Xem xét bổ sung vào `mapping-plan.md` nếu liên quan.

**13 candidate(s) từ Master Tree:**

| Score | Code | Name | Matching Keywords |
|---|---|---|---|
| 5.6 | `ARRAY_OPERATIONS` | Array Operations | `array`, `index`, `access` |
| 5.5 | `LOCAL_VIEW_STATE` | Local View State | `state`, `@state`, `view` |
| 5.2 | `POLYGON_MESH` | Polygonal Mesh (Vertex, Edge, Face) | `edge`, `face` |
| 4.5 | `STATE_PROPERTY_WRAPPER` | State Property Wrapper | `state`, `property`, `wrapper` |
| 3.4 | `WHILE_LOOP` | While Loop | `condition`, `while`, `loop` |
| 3.1 | `PROJECT_ASSETS_MANAGEMENT` | Project Assets Management | `assets`, `project` |
| 3.1 | `SYNTAX_VS_RUNTIME_ERRORS` | Syntax vs Runtime Errors | `error`, `syntax`, `errors` |
| 2.9 | `REFERENCE_TYPE_DECLARATION` | Declaring Reference Types | `object`, `types` |
| 2.6 | `IMPLICIT_EXPLICIT_ANIMATION` | Implicit vs. Explicit Animation | `explicit` |
| 2.3 | `STACK_OPERATIONS` | Stack Operations (Push/Pop) | `stack` |
| 2.3 | `USER_PERSONAS` | Creating User Personas | `persona`, `user` |
| 2.3 | `DECLARATIVE_UI_PARADIGM` | Declarative UI Paradigm | `declarative` |
| 2.3 | `UI_MODIFIERS_CONCEPT` | UI Modifiers | `modifier`, `modifiers` |

**→ Action:** Nếu concept liên quan, bổ sung vào `mapping-plan.md` và chạy lại `/build-tree`.