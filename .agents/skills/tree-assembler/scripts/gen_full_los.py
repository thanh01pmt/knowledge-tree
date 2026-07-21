import csv

# We construct the 97 LOs manually (via script) for the swift-associate project
los = []

def add_lo(code, name, desc, lo_type, parent, concepts):
    los.append([code, name, desc, lo_type, parent, concepts])

# Domain 1: Planning and Design
add_lo("ULO-DESIGN", "Understand App Design Cycle", "Hiểu quy trình thiết kế phần mềm.", "UNIVERSAL", "", "USER_CENTERED_DESIGN")
add_lo("CIO-DESIGN-CYCLE", "Summarize Design Cycle", "Nắm vững các bước trong thiết kế app.", "CONCEPTUAL_IMPL", "ULO-DESIGN", "USER_CENTERED_DESIGN")
add_lo("SIO-DESIGN-BRAINSTORM", "Brainstorm Ideas", "Lên ý tưởng cho ứng dụng.", "SPECIFIC_IMPL", "CIO-DESIGN-CYCLE", "USER_CENTERED_DESIGN")
add_lo("SIO-DESIGN-PLAN", "Plan Application", "Lập kế hoạch phát triển.", "SPECIFIC_IMPL", "CIO-DESIGN-CYCLE", "USER_CENTERED_DESIGN")
add_lo("SIO-DESIGN-PROTO", "Prototype UI", "Tạo nguyên mẫu giao diện.", "SPECIFIC_IMPL", "CIO-DESIGN-CYCLE", "USER_CENTERED_DESIGN")
add_lo("SIO-DESIGN-EVAL", "Evaluate Design", "Đánh giá thiết kế.", "SPECIFIC_IMPL", "CIO-DESIGN-CYCLE", "USER_CENTERED_DESIGN")

add_lo("ULO-SEC-PRIVACY", "Understand Security & Privacy", "Hiểu tầm quan trọng của bảo mật.", "UNIVERSAL", "", "DIGITAL_IDENTITY")
add_lo("CIO-DATA-PROTECT", "Summarize Data Protection", "Bảo vệ thông tin nhạy cảm.", "CONCEPTUAL_IMPL", "ULO-SEC-PRIVACY", "DIGITAL_IDENTITY")
add_lo("SIO-DATA-SHARE", "Sharing Information", "Hậu quả của việc chia sẻ thông tin cá nhân.", "SPECIFIC_IMPL", "CIO-DATA-PROTECT", "DIGITAL_IDENTITY")
add_lo("SIO-DATA-SEC-CHAL", "Security Challenges", "Nhận diện thách thức bảo mật.", "SPECIFIC_IMPL", "CIO-DATA-PROTECT", "DIGITAL_IDENTITY")
add_lo("SIO-DATA-IMPACTS", "Legal and Ethical Impacts", "Tác động kinh tế xã hội và đạo đức.", "SPECIFIC_IMPL", "CIO-DATA-PROTECT", "DIGITAL_IDENTITY")
add_lo("CIO-ACCESSIBILITY", "Assess Visual Design Accessibility", "Đánh giá thiết kế dựa trên tiêu chuẩn tiếp cận.", "CONCEPTUAL_IMPL", "ULO-DESIGN", "USER_CENTERED_DESIGN")

# Domain 2: Xcode Project Navigation
add_lo("ULO-DEV-ENV", "Navigate IDE", "Quản lý môi trường IDE.", "UNIVERSAL", "", "PROJECT_ASSETS_MANAGEMENT")
add_lo("CIO-XCODE-FILES", "Differentiate File Types", "Phân biệt các loại file cơ bản trong Xcode.", "CONCEPTUAL_IMPL", "ULO-DEV-ENV", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-SWIFT-FILE", "Identify .swift", "Nhận diện file mã nguồn.", "SPECIFIC_IMPL", "CIO-XCODE-FILES", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-ASSET-FILE", "Identify .xcassets", "Nhận diện file tài nguyên.", "SPECIFIC_IMPL", "CIO-XCODE-FILES", "PROJECT_ASSETS_MANAGEMENT")

add_lo("CIO-XCODE-ASSETS", "Manage Assets", "Nhập và sử dụng tài nguyên.", "CONCEPTUAL_IMPL", "ULO-DEV-ENV", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-ASSETS-RECOGNIZE", "Recognize Assets", "Nhận biết tài nguyên đã import.", "SPECIFIC_IMPL", "CIO-XCODE-ASSETS", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-ASSETS-IMPORT", "Import Assets", "Đưa hình ảnh/màu sắc vào dự án.", "SPECIFIC_IMPL", "CIO-XCODE-ASSETS", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-ASSETS-USE", "Use Assets", "Gọi tài nguyên trong code/UI.", "SPECIFIC_IMPL", "CIO-XCODE-ASSETS", "PROJECT_ASSETS_MANAGEMENT")

add_lo("CIO-XCODE-UI", "Configure UI Areas", "Thao tác với các khu vực giao diện Xcode.", "CONCEPTUAL_IMPL", "ULO-DEV-ENV", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-NAVIGATOR", "Use Navigator", "Sử dụng thanh Navigator.", "SPECIFIC_IMPL", "CIO-XCODE-UI", "PROJECT_ASSETS_MANAGEMENT")
add_lo("SIO-XCODE-INSPECTOR", "Use Inspector", "Sử dụng thanh Inspector.", "SPECIFIC_IMPL", "CIO-XCODE-UI", "PROJECT_ASSETS_MANAGEMENT")

# Domain 3: Swift Language Usage
add_lo("ULO-FUNCTIONS", "Understand Functions", "Hiểu khái niệm hàm số trong lập trình.", "UNIVERSAL", "", "FUNCTIONS_METHODS")
add_lo("CIO-SWIFT-FUNCTIONS", "Use Swift Functions", "Viết và gọi hàm Swift.", "CONCEPTUAL_IMPL", "ULO-FUNCTIONS", "FUNCTIONS_METHODS")
add_lo("SIO-FUNC-WRITE", "Write Functions", "Tự viết hàm.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FUNCTIONS_METHODS")
add_lo("SIO-FUNC-CALL", "Call Functions", "Thực thi hàm.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FUNCTIONS_METHODS")
add_lo("SIO-FUNC-LABELS", "Argument Labels", "Sử dụng tham số và nhãn biến.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FUNCTIONS_METHODS")
add_lo("SIO-FUNC-PARAMS", "Evaluate Parameters", "Đánh giá tham số truyền vào.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FUNCTIONS_METHODS")
add_lo("SIO-FUNC-RETURNS", "Evaluate Returns", "Đánh giá giá trị trả về.", "SPECIFIC_IMPL", "CIO-SWIFT-FUNCTIONS", "FUNCTIONS_METHODS")

add_lo("ULO-OPERATORS", "Understand Operators", "Toán tử cơ bản.", "UNIVERSAL", "", "VARIABLES")
add_lo("CIO-SWIFT-OPERATORS", "Calculate with Operators", "Sử dụng toán tử toán học và logic.", "CONCEPTUAL_IMPL", "ULO-OPERATORS", "VARIABLES")
add_lo("SIO-OP-ARITHMETIC", "Arithmetic Operators", "+ - * /", "SPECIFIC_IMPL", "CIO-SWIFT-OPERATORS", "VARIABLES")
add_lo("SIO-OP-LOGICAL", "Logical Operators", "&& || !", "SPECIFIC_IMPL", "CIO-SWIFT-OPERATORS", "VARIABLES")

add_lo("ULO-CUSTOM-TYPES", "Understand Custom Data Types", "Hiểu cấu trúc dữ liệu tuỳ chỉnh.", "UNIVERSAL", "", "DATA_TYPES")
add_lo("CIO-SWIFT-STRUCTS", "Create and Evaluate Structures", "Tạo và xử lý struct.", "CONCEPTUAL_IMPL", "ULO-CUSTOM-TYPES", "DATA_TYPES")
add_lo("SIO-STRUCT-DECL_PROP", "Declare Properties", "Khai báo thuộc tính.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "DATA_TYPES")
add_lo("SIO-STRUCT-INIT", "Initialize Properties", "Khởi tạo struct.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "DATA_TYPES")
add_lo("SIO-STRUCT-METHODS", "Define Methods", "Định nghĩa phương thức.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "DATA_TYPES")
add_lo("SIO-STRUCT-INST_CREATE", "Create Instance", "Tạo một instance của struct.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "DATA_TYPES")
add_lo("SIO-STRUCT-INST_USE", "Use Instance", "Sử dụng instance.", "SPECIFIC_IMPL", "CIO-SWIFT-STRUCTS", "DATA_TYPES")

add_lo("ULO-COLLECTIONS", "Understand Data Collections", "Mảng và danh sách.", "UNIVERSAL", "", "DATA_TYPES")
add_lo("CIO-SWIFT-ARRAYS", "Manipulate Arrays", "Thao tác với mảng Swift.", "CONCEPTUAL_IMPL", "ULO-COLLECTIONS", "DATA_TYPES")
add_lo("SIO-ARRAY-DECL", "Declare Arrays", "Khai báo mảng.", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "DATA_TYPES")
add_lo("SIO-ARRAY-INIT", "Initialize Arrays", "Khởi tạo giá trị mảng.", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "DATA_TYPES")
add_lo("SIO-ARRAY-INDEX", "Identify by Index", "Truy xuất phần tử qua index.", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "DATA_TYPES")
add_lo("SIO-ARRAY-MOD_INDEX", "Modify by Index", "Thay đổi giá trị tại index.", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "DATA_TYPES")
add_lo("SIO-ARRAY-PROPS", "Use Array Properties", "Dùng thuộc tính (count, isEmpty).", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "DATA_TYPES")
add_lo("SIO-ARRAY-METHODS", "Use Array Methods", "Dùng phương thức (append, remove).", "SPECIFIC_IMPL", "CIO-SWIFT-ARRAYS", "DATA_TYPES")

add_lo("ULO-CONTROL-FLOW", "Understand Control Flow", "Điều khiển luồng chương trình.", "UNIVERSAL", "", "FOR_LOOP,WHILE_LOOP")
add_lo("CIO-SWIFT-LOOPS", "Control Loop Structures", "Vòng lặp trong Swift.", "CONCEPTUAL_IMPL", "ULO-CONTROL-FLOW", "FOR_LOOP")
add_lo("SIO-LOOP-CREATE", "Create Loops", "Viết vòng lặp.", "SPECIFIC_IMPL", "CIO-SWIFT-LOOPS", "FOR_LOOP")
add_lo("SIO-LOOP-ANALYZE", "Analyze Loops", "Phân tích vòng lặp.", "SPECIFIC_IMPL", "CIO-SWIFT-LOOPS", "FOR_LOOP")
add_lo("SIO-LOOP-PREDICT", "Predict Loop Results", "Dự đoán kết quả lặp.", "SPECIFIC_IMPL", "CIO-SWIFT-LOOPS", "FOR_LOOP")

add_lo("CIO-SWIFT-CONDS", "Use Conditional Statements", "Lệnh rẽ nhánh (if, switch).", "CONCEPTUAL_IMPL", "ULO-CONTROL-FLOW", "FOR_LOOP") # For now map to loops/flow
add_lo("SIO-COND-CREATE", "Create Conditionals", "Viết if-else/switch.", "SPECIFIC_IMPL", "CIO-SWIFT-CONDS", "FOR_LOOP")
add_lo("SIO-COND-INTERPRET", "Interpret Outcomes", "Dịch mã lệnh điều kiện.", "SPECIFIC_IMPL", "CIO-SWIFT-CONDS", "FOR_LOOP")

add_lo("ULO-PROG-STATE", "Understand Variables", "Biến và hằng.", "UNIVERSAL", "", "VARIABLES")
add_lo("CIO-SWIFT-VARS", "Declare Constants and Variables", "Khai báo let, var.", "CONCEPTUAL_IMPL", "ULO-PROG-STATE", "VARIABLES")
add_lo("SIO-VAR-DIFF", "Differentiate Let and Var", "Phân biệt biến và hằng.", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "VARIABLES")
add_lo("SIO-VAR-INFER", "Type Inference", "Sử dụng suy luận kiểu.", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "VARIABLES")
add_lo("SIO-VAR-EXPLICIT", "Explicit Typing", "Định kiểu tường minh.", "SPECIFIC_IMPL", "CIO-SWIFT-VARS", "VARIABLES")

add_lo("CIO-SWIFT-NAMING", "Use Naming Syntax", "Cú pháp đặt tên.", "CONCEPTUAL_IMPL", "ULO-PROG-STATE", "VARIABLES")
add_lo("SIO-NAME-CAMEL", "Camel Casing", "Quy tắc camelCase.", "SPECIFIC_IMPL", "CIO-SWIFT-NAMING", "VARIABLES")
add_lo("SIO-NAME-RULES", "Identifier Rules", "Quy tắc đặt tên biến.", "SPECIFIC_IMPL", "CIO-SWIFT-NAMING", "VARIABLES")

# Domain 4: View Building with SwiftUI
add_lo("ULO-DECLARATIVE-UI", "Understand Declarative UI", "Giao diện khai báo.", "UNIVERSAL", "", "DECLARATIVE_UI_PARADIGM")
add_lo("CIO-SWIFTUI-PARADIGM", "Imperative vs Declarative", "So sánh.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-UI-DIFF", "Differentiate Paradigms", "Hiểu sự khác biệt UI truyền thống và SwiftUI.", "SPECIFIC_IMPL", "CIO-SWIFTUI-PARADIGM", "DECLARATIVE_UI_PARADIGM")

add_lo("CIO-SWIFTUI-CONTENT", "Create Content Views", "Tạo view nội dung.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-TEXT", "Use Text View", "Tạo Text.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-IMAGE", "Use Image View", "Tạo Image.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-SHAPE", "Use Shape View", "Tạo Hình học.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-VIEW-COLOR", "Use Color View", "Tạo màu sắc nền.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTENT", "DECLARATIVE_UI_PARADIGM")

add_lo("CIO-SWIFTUI-MODIFIERS", "Implement Modifiers", "Sử dụng Modifier.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "UI_MODIFIERS")
add_lo("SIO-MOD-PADDING", ".padding Modifier", "Đệm khoảng trắng.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-BACKGROUND", ".background Modifier", "Tạo nền.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-FRAME", ".frame Modifier", "Đổi kích thước.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-FORECOLOR", ".foregroundColor", "Đổi màu chữ.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-FONT", ".font Modifier", "Đổi kiểu chữ.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")
add_lo("SIO-MOD-RESIZE", ".resizable Modifier", "Hình ảnh thay đổi kích cỡ.", "SPECIFIC_IMPL", "CIO-SWIFTUI-MODIFIERS", "UI_MODIFIERS")

add_lo("CIO-SWIFTUI-CONTAINERS", "Create Container Views", "Sắp xếp View trong Stack.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-HSTACK", "Use HStack", "Xếp ngang.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTAINERS", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-VSTACK", "Use VStack", "Xếp dọc.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTAINERS", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-ZSTACK", "Use ZStack", "Xếp đè.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTAINERS", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-STACK-SPACER", "Use Spacer", "Đẩy view.", "SPECIFIC_IMPL", "CIO-SWIFTUI-CONTAINERS", "DECLARATIVE_UI_PARADIGM")

add_lo("CIO-SWIFTUI-HIERARCHY", "Explain View Hierarchy", "Kiến trúc phân tầng của UI.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-HIERARCHY-EXPLAIN", "Explain View Tree", "Giải thích cây giao diện.", "SPECIFIC_IMPL", "CIO-SWIFTUI-HIERARCHY", "DECLARATIVE_UI_PARADIGM")

add_lo("CIO-SWIFTUI-INTERACTIVE", "Interactive Views", "Tạo giao diện tương tác.", "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-BUTTON", "Use Button", "Nút bấm.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-TEXTFIELD", "Use TextField", "Ô nhập liệu.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-SLIDER", "Use Slider", "Thanh trượt.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")
add_lo("SIO-INT-TOGGLE", "Use Toggle", "Công tắc bật tắt.", "SPECIFIC_IMPL", "CIO-SWIFTUI-INTERACTIVE", "DECLARATIVE_UI_PARADIGM")

add_lo("ULO-STATE-DATA-DRIVEN", "Understand Data-Driven UI", "Quản lý state UI", "UNIVERSAL", "", "LOCAL_VIEW_STATE")
add_lo("CIO-SWIFTUI-STATE", "Use @State Property Wrapper", "Dùng @State", "CONCEPTUAL_IMPL", "ULO-STATE-DATA-DRIVEN", "STATE_PROPERTY_WRAPPER")
add_lo("SIO-SWIFTUI-STATE-DECL", "Declare @State", "Khai báo @State", "SPECIFIC_IMPL", "CIO-SWIFTUI-STATE", "STATE_PROPERTY_WRAPPER")
add_lo("SIO-SWIFTUI-STATE-BIND", "Bind State Variables", "Dùng ký hiệu $", "SPECIFIC_IMPL", "CIO-SWIFTUI-STATE", "STATE_PROPERTY_WRAPPER")

# Domain 5: Debugging
add_lo("ULO-DEBUGGING", "Understand Debugging", "Khái niệm tìm lỗi", "UNIVERSAL", "", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("CIO-SWIFT-ERRORS", "Differentiate Errors", "Phân biệt cú pháp vs runtime", "CONCEPTUAL_IMPL", "ULO-DEBUGGING", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-ERR-SYNTAX", "Identify Syntax Errors", "Phát hiện lỗi cú pháp.", "SPECIFIC_IMPL", "CIO-SWIFT-ERRORS", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-ERR-RUNTIME", "Identify Runtime Errors", "Phát hiện lỗi khi chạy.", "SPECIFIC_IMPL", "CIO-SWIFT-ERRORS", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("CIO-SWIFT-INTERPRET", "Interpret Error Messages", "Phân tích thông báo lỗi.", "CONCEPTUAL_IMPL", "ULO-DEBUGGING", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-MSG-READ", "Read Error Logs", "Đọc log Xcode.", "SPECIFIC_IMPL", "CIO-SWIFT-INTERPRET", "SYNTAX_VS_RUNTIME_ERRORS")
add_lo("SIO-MSG-FIX", "Fix From Message", "Sửa lỗi dựa trên gợi ý.", "SPECIFIC_IMPL", "CIO-SWIFT-INTERPRET", "SYNTAX_VS_RUNTIME_ERRORS")


with open("/Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree/projects/swift-associate/output/learning-objectives.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"])
    for r in los:
        writer.writerow(r)
        
print(f"Generated {len(los)} Learning Objectives!")
