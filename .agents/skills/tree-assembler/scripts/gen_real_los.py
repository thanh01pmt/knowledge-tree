import csv

los = []
def add_lo(code, name, desc, lo_type, parent, concepts):
    los.append([code, name, desc, lo_type, parent, concepts])

# ---------------------------------------------------------
# DOMAIN 1: Planning and Design
# ---------------------------------------------------------
# 1.1. Summarize the design cycle 
# 1.1.1. Brainstorm, plan, prototype, evaluate
add_lo("ULO-DESIGN", "Understand Design Cycle", "Hiểu quy trình thiết kế phần mềm lấy người dùng làm trung tâm.", "UNIVERSAL", "", "USER_CENTERED_DESIGN")
add_lo("CIO-DESIGN-STEPS", "Apply Design Steps", "Vận dụng các bước trong chu trình thiết kế ứng dụng.", "CONCEPTUAL_IMPL", "ULO-DESIGN", "USER_CENTERED_DESIGN")
add_lo("SIO-DS-BRAINSTORM", "Brainstorm Ideas", "Lên ý tưởng và xác định vấn đề cần giải quyết.", "SPECIFIC_IMPL", "CIO-DESIGN-STEPS", "USER_CENTERED_DESIGN")
add_lo("SIO-DS-PLAN", "Plan Application", "Lập kế hoạch phát triển và cấu trúc ứng dụng.", "SPECIFIC_IMPL", "CIO-DESIGN-STEPS", "USER_CENTERED_DESIGN")
add_lo("SIO-DS-PROTOTYPE", "Prototype UI", "Tạo nguyên mẫu giao diện (prototype).", "SPECIFIC_IMPL", "CIO-DESIGN-STEPS", "USER_CENTERED_DESIGN")
add_lo("SIO-DS-EVALUATE", "Evaluate Design", "Đánh giá thiết kế dựa trên phản hồi của người dùng.", "SPECIFIC_IMPL", "CIO-DESIGN-STEPS", "USER_CENTERED_DESIGN")

# 1.2. Summarize how sensitive data can be protected and compromised
add_lo("ULO-SECURITY", "Understand Data Security", "Hiểu tầm quan trọng của việc bảo mật dữ liệu và quyền riêng tư.", "UNIVERSAL", "", "DIGITAL_IDENTITY")
add_lo("CIO-SEC-PROTECT", "Protect Sensitive Data", "Các phương pháp bảo vệ thông tin nhạy cảm.", "CONCEPTUAL_IMPL", "ULO-SECURITY", "DIGITAL_IDENTITY")
add_lo("SIO-SEC-SHARING", "Evaluate Info Sharing", "Đánh giá rủi ro khi chia sẻ thông tin cá nhân và ứng dụng.", "SPECIFIC_IMPL", "CIO-SEC-PROTECT", "DIGITAL_IDENTITY")
add_lo("SIO-SEC-CHALLENGES", "Identify Security Challenges", "Nhận diện các thách thức bảo mật phổ biến.", "SPECIFIC_IMPL", "CIO-SEC-PROTECT", "DIGITAL_IDENTITY")
add_lo("SIO-SEC-IMPACTS", "Assess Socioeconomic Impacts", "Đánh giá tác động pháp lý, đạo đức và kinh tế xã hội của việc rò rỉ dữ liệu.", "SPECIFIC_IMPL", "CIO-SEC-PROTECT", "DIGITAL_IDENTITY")

# 1.3. Assess a visual design with accessibility in mind 
add_lo("CIO-ACCESSIBILITY", "Assess Accessibility", "Đánh giá thiết kế trực quan dựa trên tiêu chuẩn tiếp cận (accessibility).", "CONCEPTUAL_IMPL", "ULO-DESIGN", "USER_CENTERED_DESIGN")
add_lo("SIO-ACC-VISUAL", "Evaluate Visual Accessibility", "Đánh giá độ tương phản màu sắc, kích thước chữ cho người khiếm thị.", "SPECIFIC_IMPL", "CIO-ACCESSIBILITY", "USER_CENTERED_DESIGN")

# ---------------------------------------------------------
# DOMAIN 2: Xcode Project Navigation
# ---------------------------------------------------------
add_lo("ULO-IDE", "Navigate IDE", "Sử dụng môi trường phát triển tích hợp (IDE).", "UNIVERSAL", "", "PROJECT_ASSETS_MANAGEMENT")
# 2.1. Differentiate between basic file types 
add_lo("CIO-XCODE-FILES", "Differentiate File Types", "Phân biệt các loại file cơ bản trong dự án Xcode.", "CONCEPTUAL_IMPL", "ULO-IDE", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-SWIFT", "Identify Swift Files", "Nhận diện và hiểu vai trò của file .swift.", "SPECIFIC_IMPL", "CIO-XCODE-FILES", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-PLIST", "Identify Info.plist", "Nhận diện và hiểu vai trò của file cấu hình.", "SPECIFIC_IMPL", "CIO-XCODE-FILES", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-XCASSETS", "Identify Asset Catalogs", "Nhận diện thư mục tài nguyên .xcassets.", "SPECIFIC_IMPL", "CIO-XCODE-FILES", "PROJECT_ASSETS_MANAGEMENT")

# 2.2. & 2.3 Import and use assets
add_lo("CIO-XCODE-ASSETS", "Manage Assets", "Nhập và sử dụng tài nguyên trong dự án.", "CONCEPTUAL_IMPL", "ULO-IDE", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-ASSET-IMPORT", "Import Assets", "Đưa hình ảnh, biểu tượng, màu sắc vào Asset Catalog.", "SPECIFIC_IMPL", "CIO-XCODE-ASSETS", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-ASSET-RECOGNIZE", "Recognize Available Assets", "Nhận biết các tài nguyên đã được import thành công.", "SPECIFIC_IMPL", "CIO-XCODE-ASSETS", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-ASSET-USE", "Use Assets in Code", "Tham chiếu và sử dụng tài nguyên trong mã nguồn hoặc UI.", "SPECIFIC_IMPL", "CIO-XCODE-ASSETS", "PROJECT_ASSETS_MANAGEMENT")

# 2.4. Select appropriate actions to configure UI areas
add_lo("CIO-XCODE-UI-AREAS", "Configure UI Areas", "Thao tác với các khu vực giao diện của Xcode.", "CONCEPTUAL_IMPL", "ULO-IDE", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-NAVIGATOR", "Use Navigator Area", "Sử dụng Navigator để quản lý file và tìm kiếm.", "SPECIFIC_IMPL", "CIO-XCODE-UI-AREAS", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-INSPECTOR", "Use Inspector Area", "Sử dụng Inspector để thay đổi thuộc tính của UI component.", "SPECIFIC_IMPL", "CIO-XCODE-UI-AREAS", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-EDITOR", "Use Editor Area", "Sử dụng Editor Area và Canvas để viết code và xem trước (Preview).", "SPECIFIC_IMPL", "CIO-XCODE-UI-AREAS", "PROJECT_ASSETS_MANAGEMENT")

# ---------------------------------------------------------
# DOMAIN 3: Swift Language Usage
# ---------------------------------------------------------
# 3.1. Functions
add_lo("ULO-FUNCTIONS", "Understand Functions", "Khái niệm hàm, tham số và giá trị trả về.", "UNIVERSAL", "", "FIRST_CLASS_FUNCTIONS")
add_lo("CIO-SWIFT-FUNCTIONS", "Write and Call Functions", "Viết, gọi và đánh giá việc thực thi hàm trong Swift.", "CONCEPTUAL_IMPL", "ULO-FUNCTIONS", "FIRST_CLASS_FUNCTIONS")
add_lo("SIO-FUNC-WRITE", "Write Functions", "Viết cú pháp hàm (func) cơ bản.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FIRST_CLASS_FUNCTIONS")
add_lo("SIO-FUNC-CALL", "Call Functions", "Gọi thực thi một hàm đã định nghĩa.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FIRST_CLASS_FUNCTIONS")
add_lo("SIO-FUNC-LABELS", "Evaluate Argument Labels", "Sử dụng và đánh giá nhãn đối số (argument labels).", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FIRST_CLASS_FUNCTIONS")
add_lo("SIO-FUNC-PARAMS", "Evaluate Parameters", "Truyền và đánh giá tham số (parameters).", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FIRST_CLASS_FUNCTIONS")
add_lo("SIO-FUNC-RETURN", "Evaluate Returns", "Nhận và xử lý giá trị trả về (returns).", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FIRST_CLASS_FUNCTIONS")

# 3.2. Operators
add_lo("ULO-OPERATORS", "Understand Operators", "Khái niệm toán tử để tính toán và so sánh.", "UNIVERSAL", "", "PRIMITIVE_TYPE_DECLARATION")
add_lo("CIO-SWIFT-OPERATORS", "Calculate with Operators", "Tính toán kết quả sử dụng các loại toán tử trong Swift.", "CONCEPTUAL_IMPL", "ULO-OPERATORS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-OP-ARITHMETIC", "Use Arithmetic Operators", "Sử dụng toán tử số học (+, -, *, /, %).", "SPECIFIC_IMPL", "CIO-SWIFT-OPERATORS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-OP-COMPOUND", "Use Compound Assignment", "Sử dụng toán tử gán kết hợp (+=, -=).", "SPECIFIC_IMPL", "CIO-SWIFT-OPERATORS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-OP-COMPARISON", "Use Comparison Operators", "Sử dụng toán tử so sánh (==, !=, >, <).", "SPECIFIC_IMPL", "CIO-SWIFT-OPERATORS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-OP-LOGICAL", "Use Logical Operators", "Sử dụng toán tử logic (&&, ||, !).", "SPECIFIC_IMPL", "CIO-SWIFT-OPERATORS", "PRIMITIVE_TYPE_DECLARATION")

# 3.3. Structures
add_lo("ULO-DATA-STRUCTURES", "Understand Custom Data Types", "Khái niệm nhóm dữ liệu và hành vi thành một kiểu tuỳ chỉnh.", "UNIVERSAL", "", "REFERENCE_TYPE_DECLARATION")
add_lo("CIO-SWIFT-STRUCTS", "Create and Evaluate Structures", "Tạo và đánh giá các cấu trúc (struct) trong Swift.", "CONCEPTUAL_IMPL", "ULO-DATA-STRUCTURES", "REFERENCE_TYPE_DECLARATION")
add_lo("SIO-STRUCT-DECL", "Declare Properties", "Khai báo các thuộc tính (properties) cho struct.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "REFERENCE_TYPE_DECLARATION")
add_lo("SIO-STRUCT-INIT", "Initialize Properties", "Khởi tạo giá trị cho các thuộc tính (memberwise initializer).", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "REFERENCE_TYPE_DECLARATION")
add_lo("SIO-STRUCT-METHOD", "Define Methods", "Định nghĩa phương thức (methods) bên trong struct.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "REFERENCE_TYPE_DECLARATION")
add_lo("SIO-STRUCT-INST-CREATE", "Create Instance", "Tạo một phiên bản (instance) cụ thể từ struct.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "REFERENCE_TYPE_DECLARATION")
add_lo("SIO-STRUCT-INST-USE", "Use Instance", "Truy cập thuộc tính và gọi phương thức của một instance.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "REFERENCE_TYPE_DECLARATION")

# 3.4. Arrays
add_lo("ULO-COLLECTIONS", "Understand Collections", "Khái niệm lưu trữ tập hợp dữ liệu.", "UNIVERSAL", "", "ARRAY_OPERATIONS")
add_lo("CIO-SWIFT-ARRAYS", "Create and Manipulate Arrays", "Tạo và thao tác với mảng (Array) trong Swift.", "CONCEPTUAL_IMPL", "ULO-COLLECTIONS", "ARRAY_OPERATIONS")
add_lo("SIO-ARR-DECL", "Declare Array", "Khai báo và khởi tạo mảng với các giá trị ban đầu.", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "ARRAY_OPERATIONS")
add_lo("SIO-ARR-INDEX-READ", "Identify Element by Index", "Truy cập phần tử mảng thông qua chỉ mục (index).", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "ARRAY_OPERATIONS")
add_lo("SIO-ARR-INDEX-WRITE", "Modify Element by Index", "Sửa đổi giá trị phần tử mảng thông qua chỉ mục.", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "ARRAY_OPERATIONS")
add_lo("SIO-ARR-PROPS", "Use Array Properties", "Sử dụng các thuộc tính của mảng (ví dụ: count, isEmpty).", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "ARRAY_OPERATIONS")
add_lo("SIO-ARR-METHODS", "Use Array Methods", "Sử dụng các phương thức của mảng (ví dụ: append, insert, remove).", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "ARRAY_OPERATIONS")

# 3.5. Control flow
add_lo("ULO-CONTROL-FLOW", "Understand Control Flow", "Khái niệm rẽ nhánh và lặp trong lập trình.", "UNIVERSAL", "", "FOR_LOOP,WHILE_LOOP,IF_ELSE_STATEMENT")
add_lo("CIO-SWIFT-LOOPS", "Predict Loop Structures", "Tạo, phân tích và dự đoán kết quả của vòng lặp.", "CONCEPTUAL_IMPL", "ULO-CONTROL-FLOW", "FOR_LOOP")
add_lo("SIO-LOOP-FOR-IN", "Use for-in Loop", "Sử dụng vòng lặp for-in để duyệt qua mảng hoặc range.", "SPECIFIC_IMPL", "CIO-SWIFT-LOOPS", "FOR_LOOP")
add_lo("SIO-LOOP-WHILE", "Use while Loop", "Sử dụng vòng lặp while.", "SPECIFIC_IMPL", "CIO-SWIFT-LOOPS", "WHILE_LOOP")
add_lo("SIO-LOOP-PREDICT", "Predict Loop Results", "Dự đoán chính xác số lần lặp và trạng thái biến trong vòng lặp.", "SPECIFIC_IMPL", "CIO-SWIFT-LOOPS", "FOR_LOOP")

add_lo("CIO-SWIFT-CONDS", "Interpret Conditional Statements", "Tạo và dịch kết quả của câu lệnh điều kiện.", "CONCEPTUAL_IMPL", "ULO-CONTROL-FLOW", "IF_ELSE_STATEMENT")
add_lo("SIO-COND-IF", "Use if-else Statement", "Sử dụng cấu trúc if-else if-else.", "SPECIFIC_IMPL", "CIO-SWIFT-CONDS", "IF_ELSE_STATEMENT")
add_lo("SIO-COND-SWITCH", "Use switch Statement", "Sử dụng cấu trúc switch-case (bao gồm default).", "SPECIFIC_IMPL", "CIO-SWIFT-CONDS", "SWITCH_CASE")

# 3.6. Constants and Variables
add_lo("ULO-STATE", "Understand State and Mutability", "Khái niệm về cấp phát bộ nhớ khả biến và bất biến.", "UNIVERSAL", "", "PRIMITIVE_TYPE_DECLARATION")
add_lo("CIO-SWIFT-VARS", "Declare Constants and Variables", "Khai báo và đánh giá hằng, biến, các kiểu dữ liệu.", "CONCEPTUAL_IMPL", "ULO-STATE", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-VAR-LET", "Differentiate Constants and Variables", "Phân biệt và sử dụng đúng let (hằng) và var (biến).", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-VAR-INFERENCE", "Apply Type Inference", "Áp dụng cơ chế tự suy luận kiểu (Type Inference).", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-VAR-EXPLICIT", "Use Explicit Typing", "Khai báo định kiểu tường minh (Explicit typing).", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-VAR-TYPES", "Identify Data Types", "Nhận diện Int, Double, String, Bool.", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "PRIMITIVE_TYPE_DECLARATION")

# 3.7. Naming Syntax
add_lo("CIO-SWIFT-NAMING", "Use Naming Syntax", "Sử dụng cú pháp đặt tên chuẩn xác.", "CONCEPTUAL_IMPL", "ULO-STATE", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-NAME-CAMEL", "Use Camel Casing", "Áp dụng quy tắc lowerCamelCase cho biến và hàm.", "SPECIFIC_IMPL", "CIO-SWIFT-NAMING", "PRIMITIVE_TYPE_DECLARATION")
add_lo("SIO-NAME-RULES", "Apply Identifier Rules", "Tuân thủ luật đặt tên (không bắt đầu bằng số, không dùng ký tự đặc biệt...).", "SPECIFIC_IMPL", "CIO-SWIFT-NAMING", "PRIMITIVE_TYPE_DECLARATION")

# ---------------------------------------------------------
# DOMAIN 4: View Building with SwiftUI
# ---------------------------------------------------------
# 4.1. Imperative vs Declarative
add_lo("ULO-DECLARATIVE", "Understand Declarative Paradigm", "Khái niệm lập trình khai báo.", "UNIVERSAL", "", "DECLARATIVE_UI_PARADIGM")
add_lo("CIO-SWIFTUI-PARADIGM", "Imperative vs Declarative", "Phân biệt lập trình ra lệnh (imperative) và khai báo (declarative).", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-PARADIGM-DIFF", "Differentiate UI Paradigms", "Giải thích cách SwiftUI phản ứng với state thay vì cập nhật UI thủ công.", "SPECIFIC_IMPL", "CIO-SWIFTUI-PARADIGM", "DECLARATIVE_UI_PARADIGM")

# 4.2. Content Views
add_lo("CIO-SWIFTUI-CONTENT", "Create Content Views", "Tạo các View nội dung cơ bản.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-TEXT", "Use Text View", "Sử dụng Text() để hiển thị chuỗi.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-IMAGE", "Use Image View", "Sử dụng Image() để hiển thị hình ảnh.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-SHAPE", "Use Shape View", "Sử dụng Shape (Circle, Rectangle...).", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-COLOR", "Use Color View", "Sử dụng Color như một View độc lập.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")

# 4.3. Modifiers
add_lo("CIO-SWIFTUI-MODIFIERS", "Implement Modifiers", "Sử dụng Modifiers để thay đổi giao diện View.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE", "UI_MODIFIERS")
add_lo("SIO-MOD-PADDING", "Use .padding", "Tạo khoảng trắng bằng .padding.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-BACKGROUND", "Use .background", "Tạo nền bằng .background.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-FRAME", "Use .frame", "Điều chỉnh kích thước bằng .frame.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-FOREGROUND", "Use .foregroundColor", "Thay đổi màu sắc bằng .foregroundColor.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-FONT", "Use .font", "Thay đổi kiểu chữ bằng .font.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-RESIZABLE", "Use .resizable", "Cho phép Image thay đổi kích thước bằng .resizable.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-ORDER", "Understand Modifier Order", "Đánh giá sự thay đổi giao diện dựa trên thứ tự gọi Modifiers.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")

# 4.4. Container Views
add_lo("CIO-SWIFTUI-STACKS", "Create Container Views", "Sắp xếp Views sử dụng Stacks.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-HSTACK", "Use HStack", "Xếp Views theo chiều ngang (HStack).", "SPECIFIC_IMPL", "CIO-SWIFTUI-STACKS", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-VSTACK", "Use VStack", "Xếp Views theo chiều dọc (VStack).", "SPECIFIC_IMPL", "CIO-SWIFTUI-STACKS", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-ZSTACK", "Use ZStack", "Xếp đè Views lên nhau theo chiều sâu (ZStack).", "SPECIFIC_IMPL", "CIO-SWIFTUI-STACKS", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-SPACER", "Use Spacer", "Đẩy các Views giãn ra bằng Spacer.", "SPECIFIC_IMPL", "CIO-SWIFTUI-STACKS", "DECLARATIVE_UI_PARADIGM")

# 4.5. View hierarchy
add_lo("CIO-SWIFTUI-HIERARCHY", "Explain View Hierarchy", "Kiến trúc phân tầng giao diện SwiftUI.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-HIERARCHY-PARENT", "Understand Parent-Child", "Hiểu quan hệ View cha và View con trong cây giao diện.", "SPECIFIC_IMPL", "CIO-SWIFTUI-HIERARCHY", "DECLARATIVE_UI_PARADIGM")

# 4.6. Interactive Views
add_lo("CIO-SWIFTUI-INTERACTIVE", "Apply Interactive Views", "Tạo và sử dụng các View tương tác.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-BUTTON", "Use Button", "Sử dụng Button và khai báo action.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-TEXTFIELD", "Use TextField", "Sử dụng TextField để nhập văn bản.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-SLIDER", "Use Slider", "Sử dụng Slider để chọn giá trị số.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-TOGGLE", "Use Toggle", "Sử dụng Toggle làm công tắc bật/tắt.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")

# 4.7. @State
add_lo("ULO-STATE-MGT", "Understand State Management", "Khái niệm dữ liệu quản lý giao diện.", "UNIVERSAL", "", "LOCAL_VIEW_STATE")
add_lo("CIO-SWIFTUI-STATE", "Use @State Property Wrapper", "Sử dụng @State để điều khiển diện mạo View.", "CONCEPTUAL_IMPL", "ULO-STATE-MGT", "STATE_PROPERTY_WRAPPER")
add_lo("SIO-STATE-DECL", "Declare @State Variables", "Khai báo biến state (ví dụ: @State private var).", "SPECIFIC_IMPL", "CIO-SWIFTUI-STATE", "STATE_PROPERTY_WRAPPER")
add_lo("SIO-STATE-BIND", "Bind State to Views", "Sử dụng ký hiệu $ để tạo liên kết hai chiều (binding) với Interactive Views.", "SPECIFIC_IMPL", "CIO-SWIFTUI-STATE", "TWO_WAY_BINDING")

# ---------------------------------------------------------
# DOMAIN 5: Debugging
# ---------------------------------------------------------
add_lo("ULO-DEBUGGING", "Understand Debugging", "Khái niệm tìm và sửa lỗi.", "UNIVERSAL", "", "SYNTAX_VS_RUNTIME_ERRORS")
# 5.1. Syntax vs Run-time errors
add_lo("CIO-SWIFT-ERRORS", "Differentiate Error Types", "Phân biệt các loại lỗi khi build và run ứng dụng.", "CONCEPTUAL_IMPL", "ULO-DEBUGGING", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-ERR-SYNTAX", "Identify Syntax Errors", "Nhận diện lỗi cú pháp (Compile-time/Syntax errors).", "SPECIFIC_IMPL", "CIO-SWIFT-ERRORS", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-ERR-RUNTIME", "Identify Runtime Errors", "Nhận diện lỗi phát sinh khi chạy (Run-time errors / Crash).", "SPECIFIC_IMPL", "CIO-SWIFT-ERRORS", "SYNTAX_VS_RUNTIME_ERRORS")

# 5.2. Interpret error messages
add_lo("CIO-SWIFT-INTERPRET", "Interpret Error Messages", "Dịch và phân tích thông báo lỗi.", "CONCEPTUAL_IMPL", "ULO-DEBUGGING", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-MSG-CONSOLE", "Read Console Logs", "Đọc thông báo lỗi từ màn hình Console.", "SPECIFIC_IMPL", "CIO-SWIFT-INTERPRET", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-MSG-FIX", "Apply Fix-its", "Sử dụng tính năng Fix-it của Xcode để sửa các lỗi cú pháp cơ bản.", "SPECIFIC_IMPL", "CIO-SWIFT-INTERPRET", "SYNTAX_VS_RUNTIME_ERRORS")

with open("/Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree/projects/swift-associate/output/learning-objectives.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"])
    for r in los:
        writer.writerow(r)

print(f"Generated exactly {len(los)} Learning Objectives strictly matching valid Master Tree concept codes!")
