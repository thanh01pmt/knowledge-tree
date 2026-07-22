#!/usr/bin/env python3
"""
gen_real_los.py — Reference Implementation: Swift Associate Learning Objectives.

Cấu trúc đúng theo Abstraction Axis:
  ULO  = Năng lực cốt lõi, KHÔNG phụ thuộc ngôn ngữ.
  CIO  = Pattern/approach, language-NEUTRAL (không có tên Swift trong name).
  SIO  = Kỹ năng Swift cụ thể, đo lường được, gắn với syntax/API.

Format description: "Người học có khả năng [verb] [object]..."

Dùng script này để tái tạo learning-objectives.tsv cho swift-associate thủ công.
Dùng llm_extract_lo.py để tự động sinh LO cho project mới.
"""

import argparse
import csv
import sys
from pathlib import Path

los: list[list[str]] = []


def lo(code: str, name: str, desc: str, lo_type: str, parent: str, concepts: str):
    """Add a Learning Objective to the list."""
    los.append([code, name, desc, lo_type, parent, concepts])


# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN 1: Planning & Design
# ═══════════════════════════════════════════════════════════════════════════════

lo("ULO-USER-CENTERED-DESIGN",
   "Understand User-Centered Design",
   "Người học có khả năng giải thích quy trình thiết kế lấy người dùng làm trung tâm và lý do tại sao nó đảm bảo sản phẩm đáp ứng đúng nhu cầu thực tế.",
   "UNIVERSAL", "", "USER_CENTERED_DESIGN")

# CIO: Design Cycle (pattern, language-neutral)
lo("CIO-APPLY-DESIGN-CYCLE",
   "Apply the Iterative Design Cycle",
   "Người học có khả năng áp dụng chu trình thiết kế lặp (Brainstorm → Plan → Prototype → Evaluate) để phát triển một sản phẩm từ ý tưởng đến nguyên mẫu.",
   "CONCEPTUAL_IMPL", "ULO-USER-CENTERED-DESIGN", "USER_CENTERED_DESIGN")

lo("SIO-SWIFT-BRAINSTORM",
   "Brainstorm and define app problem in Swift context",
   "Người học có khả năng lên ý tưởng và viết câu định nghĩa vấn đề rõ ràng cho một ứng dụng iOS cần phát triển.",
   "SPECIFIC_IMPL", "CIO-APPLY-DESIGN-CYCLE", "USER_CENTERED_DESIGN")

lo("SIO-SWIFT-PLAN-STRUCTURE",
   "Plan the structure and user flow of an iOS app",
   "Người học có khả năng phác thảo cấu trúc màn hình và luồng người dùng cho một ứng dụng iOS ở giai đoạn lập kế hoạch.",
   "SPECIFIC_IMPL", "CIO-APPLY-DESIGN-CYCLE", "USER_CENTERED_DESIGN")

lo("SIO-SWIFT-PROTOTYPE",
   "Create a low-fidelity prototype for an iOS app",
   "Người học có khả năng tạo nguyên mẫu giao diện đơn giản (low-fidelity) đại diện cho các màn hình chính của ứng dụng.",
   "SPECIFIC_IMPL", "CIO-APPLY-DESIGN-CYCLE", "USER_CENTERED_DESIGN")

lo("SIO-SWIFT-EVALUATE-DESIGN",
   "Evaluate a prototype against user feedback criteria",
   "Người học có khả năng đánh giá một nguyên mẫu dựa trên phản hồi người dùng và xác định các điểm cần cải tiến.",
   "SPECIFIC_IMPL", "CIO-APPLY-DESIGN-CYCLE", "USER_CENTERED_DESIGN")

# CIO: Accessibility assessment (pattern, neutral)
lo("CIO-ASSESS-ACCESSIBILITY",
   "Evaluate Visual Designs for Accessibility",
   "Người học có khả năng đánh giá một thiết kế trực quan theo các tiêu chuẩn tiếp cận (accessibility) để đảm bảo tính bao hàm.",
   "CONCEPTUAL_IMPL", "ULO-USER-CENTERED-DESIGN", "USER_CENTERED_DESIGN")

lo("SIO-SWIFT-COLOR-CONTRAST",
   "Evaluate color contrast for iOS accessibility guidelines",
   "Người học có khả năng kiểm tra độ tương phản màu sắc của một giao diện iOS theo ngưỡng tỷ lệ tương phản tối thiểu (4.5:1 cho văn bản nhỏ).",
   "SPECIFIC_IMPL", "CIO-ASSESS-ACCESSIBILITY", "USER_CENTERED_DESIGN")

lo("SIO-SWIFT-FONT-READABILITY",
   "Assess font size and Dynamic Type readability in iOS",
   "Người học có khả năng đánh giá cỡ chữ và khả năng đọc của giao diện iOS, bao gồm việc hỗ trợ Dynamic Type cho người có nhu cầu đặc biệt.",
   "SPECIFIC_IMPL", "CIO-ASSESS-ACCESSIBILITY", "USER_CENTERED_DESIGN")

# ──────────────────────────────────────────────────────────────────────────────

lo("ULO-DATA-PRIVACY-SECURITY",
   "Understand Data Privacy and Security",
   "Người học có khả năng giải thích tại sao việc bảo vệ dữ liệu cá nhân là quan trọng và mô tả các nguy cơ khi dữ liệu bị lộ.",
   "UNIVERSAL", "", "DIGITAL_IDENTITY")

lo("CIO-PROTECT-USER-DATA",
   "Protect Sensitive User Data in an Application",
   "Người học có khả năng xác định các chiến lược bảo vệ thông tin cá nhân trong một ứng dụng phần mềm.",
   "CONCEPTUAL_IMPL", "ULO-DATA-PRIVACY-SECURITY", "DIGITAL_IDENTITY")

lo("SIO-SWIFT-EVALUATE-INFO-SHARING",
   "Evaluate risks of sharing personal information in an iOS app",
   "Người học có khả năng phân tích tình huống chia sẻ thông tin cá nhân trong ứng dụng iOS và đánh giá mức độ rủi ro tương ứng.",
   "SPECIFIC_IMPL", "CIO-PROTECT-USER-DATA", "DIGITAL_IDENTITY")

lo("SIO-SWIFT-IDENTIFY-SECURITY-CHALLENGES",
   "Identify common security challenges in mobile apps",
   "Người học có khả năng nhận diện ít nhất ba thách thức bảo mật phổ biến trong ứng dụng iOS (VD: lưu trữ không mã hóa, kết nối không an toàn).",
   "SPECIFIC_IMPL", "CIO-PROTECT-USER-DATA", "DIGITAL_IDENTITY")

lo("CIO-ASSESS-BREACH-IMPACTS",
   "Assess Socioeconomic Impacts of Data Breaches",
   "Người học có khả năng phân tích hậu quả pháp lý, đạo đức và kinh tế xã hội khi dữ liệu bị xâm phạm.",
   "CONCEPTUAL_IMPL", "ULO-DATA-PRIVACY-SECURITY", "DIGITAL_IDENTITY")

lo("SIO-SWIFT-LEGAL-ETHICAL-IMPACTS",
   "Assess legal and ethical consequences of a data breach scenario",
   "Người học có khả năng phân tích một tình huống rò rỉ dữ liệu cụ thể và trình bày các hệ quả pháp lý, đạo đức và kinh tế xã hội liên quan.",
   "SPECIFIC_IMPL", "CIO-ASSESS-BREACH-IMPACTS", "DIGITAL_IDENTITY")

lo("SIO-SWIFT-DATA-PROTECTION-BEST-PRACTICES",
   "Summarize data protection best practices for iOS developers",
   "Người học có khả năng tóm tắt các biện pháp bảo vệ dữ liệu tốt nhất mà một nhà phát triển iOS cần tuân thủ.",
   "SPECIFIC_IMPL", "CIO-ASSESS-BREACH-IMPACTS", "DIGITAL_IDENTITY")


# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN 2: Xcode Project Navigation
# ═══════════════════════════════════════════════════════════════════════════════

lo("ULO-IDE-NAVIGATION",
   "Understand IDE Structure and Navigation",
   "Người học có khả năng giải thích mục đích của môi trường phát triển tích hợp (IDE) và điều hướng hiệu quả trong không gian làm việc của nó.",
   "UNIVERSAL", "", "PROJECT_ASSETS_MANAGEMENT")

lo("CIO-CATEGORIZE-PROJECT-FILES",
   "Categorize File Types Within a Software Project",
   "Người học có khả năng phân biệt các loại file khác nhau trong một dự án phần mềm và giải thích vai trò của từng loại.",
   "CONCEPTUAL_IMPL", "ULO-IDE-NAVIGATION", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-SWIFT-FILE",
   "Identify the role of .swift source files in Xcode",
   "Người học có khả năng nhận diện file .swift là file mã nguồn Swift và giải thích rằng đây là nơi viết logic và giao diện ứng dụng.",
   "SPECIFIC_IMPL", "CIO-CATEGORIZE-PROJECT-FILES", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-PLIST-FILE",
   "Identify the role of Info.plist in an Xcode project",
   "Người học có khả năng giải thích rằng Info.plist chứa metadata cấu hình ứng dụng (tên, permissions, bundle ID) và biết cách đọc các key-value trong file này.",
   "SPECIFIC_IMPL", "CIO-CATEGORIZE-PROJECT-FILES", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-XCASSETS-FILE",
   "Identify and use .xcassets Asset Catalog in Xcode",
   "Người học có khả năng nhận diện thư mục .xcassets là kho lưu trữ tài nguyên có cấu trúc và biết cách mở nó trong Xcode.",
   "SPECIFIC_IMPL", "CIO-CATEGORIZE-PROJECT-FILES", "PROJECT_ASSETS_MANAGEMENT")

lo("CIO-MANAGE-PROJECT-ASSETS",
   "Import and Organize Project Assets",
   "Người học có khả năng đưa tài nguyên bên ngoài vào một dự án phần mềm và tổ chức chúng theo cách có thể tái sử dụng trong code.",
   "CONCEPTUAL_IMPL", "ULO-IDE-NAVIGATION", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-IMPORT-ASSET",
   "Import images and icons into the Xcode Asset Catalog",
   "Người học có khả năng kéo thả hình ảnh và biểu tượng vào đúng slot (1x, 2x, 3x) trong Asset Catalog của Xcode.",
   "SPECIFIC_IMPL", "CIO-MANAGE-PROJECT-ASSETS", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-REFERENCE-ASSET",
   "Reference an Asset Catalog item in a SwiftUI view",
   "Người học có khả năng sử dụng Image(\"asset-name\") trong SwiftUI để tham chiếu đến tài nguyên đã được import vào Asset Catalog.",
   "SPECIFIC_IMPL", "CIO-MANAGE-PROJECT-ASSETS", "PROJECT_ASSETS_MANAGEMENT")

lo("CIO-CONFIGURE-IDE-WORKSPACE",
   "Configure and Navigate IDE Workspace Areas",
   "Người học có khả năng nhận biết và sử dụng các vùng làm việc chính của một IDE để tối ưu hóa quy trình phát triển.",
   "CONCEPTUAL_IMPL", "ULO-IDE-NAVIGATION", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-NAVIGATOR",
   "Use the Xcode Navigator area to manage files and search",
   "Người học có khả năng sử dụng Navigator (vùng trái) của Xcode để duyệt cấu trúc dự án, tìm file, và thực hiện tìm kiếm trong toàn bộ project.",
   "SPECIFIC_IMPL", "CIO-CONFIGURE-IDE-WORKSPACE", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-INSPECTOR",
   "Use the Xcode Inspector area to modify UI attributes",
   "Người học có khả năng sử dụng Inspector (vùng phải) của Xcode để xem và chỉnh sửa thuộc tính của UI component đang được chọn.",
   "SPECIFIC_IMPL", "CIO-CONFIGURE-IDE-WORKSPACE", "PROJECT_ASSETS_MANAGEMENT")

lo("SIO-XCODE-EDITOR-CANVAS",
   "Use the Xcode Editor and Canvas for coding and live preview",
   "Người học có khả năng viết mã nguồn Swift trong Editor Area và xem trước UI thời gian thực trên Canvas (Preview) của Xcode.",
   "SPECIFIC_IMPL", "CIO-CONFIGURE-IDE-WORKSPACE", "PROJECT_ASSETS_MANAGEMENT")


# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN 3: Swift Language Fundamentals
# ═══════════════════════════════════════════════════════════════════════════════

# ── Functions ──────────────────────────────────────────────────────────────────

lo("ULO-PARAMETERIZED-SUBROUTINE",
   "Understand Parameterized Subroutines",
   "Người học có khả năng giải thích khái niệm hàm (subroutine) với tham số và giá trị trả về, và mô tả tại sao hàm giúp tổ chức code tái sử dụng được.",
   "UNIVERSAL", "", "FIRST_CLASS_FUNCTIONS")

lo("CIO-DEFINE-SUBROUTINE",
   "Define a Named Subroutine with Parameters and Return Value",
   "Người học có khả năng định nghĩa một subroutine có tên, nhận tham số đầu vào và trả về một kết quả.",
   "CONCEPTUAL_IMPL", "ULO-PARAMETERIZED-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-FUNC-DEFINE",
   "Write a Swift function with typed parameters and return type",
   "Người học có khả năng viết cú pháp hàm Swift đầy đủ với từ khóa func, danh sách tham số có kiểu, và kiểu trả về sau dấu ->.",
   "SPECIFIC_IMPL", "CIO-DEFINE-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-FUNC-VOID",
   "Write a Swift function with no return value",
   "Người học có khả năng viết một hàm Swift không trả về giá trị (kiểu trả về ngầm định là Void) và giải thích khi nào nên dùng.",
   "SPECIFIC_IMPL", "CIO-DEFINE-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-ARG-LABELS",
   "Declare argument labels and parameter names in Swift",
   "Người học có khả năng khai báo hàm Swift với argument label khác tên parameter (VD: func move(to destination: Point)) và giải thích sự khác biệt giữa hai tên này.",
   "SPECIFIC_IMPL", "CIO-DEFINE-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("CIO-INVOKE-SUBROUTINE",
   "Invoke a Subroutine and Use Its Return Value",
   "Người học có khả năng gọi thực thi một subroutine với đúng đối số và xử lý giá trị mà subroutine trả về.",
   "CONCEPTUAL_IMPL", "ULO-PARAMETERIZED-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-FUNC-CALL",
   "Call a Swift function with correct argument syntax",
   "Người học có khả năng gọi hàm Swift với đúng argument labels và kiểu dữ liệu tương ứng cho mỗi tham số.",
   "SPECIFIC_IMPL", "CIO-INVOKE-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-FUNC-RETURN-CAPTURE",
   "Capture and use the return value of a Swift function",
   "Người học có khả năng lưu giá trị trả về của hàm Swift vào một biến/hằng và sử dụng nó trong biểu thức tiếp theo.",
   "SPECIFIC_IMPL", "CIO-INVOKE-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("CIO-TRACE-SUBROUTINE-EXECUTION",
   "Trace Subroutine Execution to Predict Output",
   "Người học có khả năng theo dõi luồng thực thi của một subroutine từng bước để dự đoán chính xác kết quả đầu ra.",
   "CONCEPTUAL_IMPL", "ULO-PARAMETERIZED-SUBROUTINE", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-TRACE-FUNC-CALL",
   "Trace parameter passing in a Swift function call",
   "Người học có khả năng theo dõi giá trị của từng tham số qua các bước thực thi hàm Swift và dự đoán giá trị trả về.",
   "SPECIFIC_IMPL", "CIO-TRACE-SUBROUTINE-EXECUTION", "FIRST_CLASS_FUNCTIONS")

lo("SIO-SWIFT-PREDICT-FUNC-OUTPUT",
   "Predict the output of a Swift function given specific inputs",
   "Người học có khả năng đọc định nghĩa hàm Swift và dự đoán chính xác giá trị trả về khi biết trước các đối số đầu vào.",
   "SPECIFIC_IMPL", "CIO-TRACE-SUBROUTINE-EXECUTION", "FIRST_CLASS_FUNCTIONS")

# ── Operators ──────────────────────────────────────────────────────────────────

lo("ULO-ARITHMETIC-LOGIC-OPS",
   "Understand Arithmetic and Logical Operations",
   "Người học có khả năng mô tả các loại toán tử cơ bản (số học, so sánh, logic) và giải thích vai trò của chúng trong xây dựng biểu thức và điều kiện.",
   "UNIVERSAL", "", "PRIMITIVE_TYPE_DECLARATION")

lo("CIO-COMPUTE-ARITHMETIC",
   "Perform Arithmetic Computations Using Operators",
   "Người học có khả năng xây dựng biểu thức số học để tính toán kết quả, bao gồm việc kết hợp nhiều toán tử theo đúng thứ tự ưu tiên.",
   "CONCEPTUAL_IMPL", "ULO-ARITHMETIC-LOGIC-OPS", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-ARITHMETIC-OPS",
   "Use Swift arithmetic operators in expressions",
   "Người học có khả năng viết biểu thức Swift sử dụng các toán tử số học: cộng (+), trừ (-), nhân (*), chia (/), và chia lấy dư (%).",
   "SPECIFIC_IMPL", "CIO-COMPUTE-ARITHMETIC", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-COMPOUND-ASSIGN",
   "Use Swift compound assignment operators",
   "Người học có khả năng sử dụng các toán tử gán kết hợp Swift (+=, -=, *=, /=) để cập nhật giá trị biến một cách ngắn gọn.",
   "SPECIFIC_IMPL", "CIO-COMPUTE-ARITHMETIC", "PRIMITIVE_TYPE_DECLARATION")

lo("CIO-EVALUATE-BOOLEAN-EXPR",
   "Evaluate Boolean Expressions Using Comparison and Logical Operators",
   "Người học có khả năng xây dựng và đánh giá các biểu thức boolean phức hợp bằng cách kết hợp toán tử so sánh và logic.",
   "CONCEPTUAL_IMPL", "ULO-ARITHMETIC-LOGIC-OPS", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-COMPARISON-OPS",
   "Use Swift comparison operators to form boolean conditions",
   "Người học có khả năng viết điều kiện Swift sử dụng toán tử so sánh: bằng (==), khác (!=), lớn hơn (>), nhỏ hơn (<), >= và <=.",
   "SPECIFIC_IMPL", "CIO-EVALUATE-BOOLEAN-EXPR", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-LOGICAL-OPS",
   "Combine boolean conditions using Swift logical operators",
   "Người học có khả năng kết hợp nhiều điều kiện boolean trong Swift bằng toán tử logic: AND (&&), OR (||), và NOT (!).",
   "SPECIFIC_IMPL", "CIO-EVALUATE-BOOLEAN-EXPR", "PRIMITIVE_TYPE_DECLARATION")

# ── Structures ──────────────────────────────────────────────────────────────────

lo("ULO-COMPOSITE-DATA-TYPE",
   "Understand Composite Custom Data Types",
   "Người học có khả năng giải thích khái niệm nhóm các dữ liệu liên quan và hành vi vào một kiểu dữ liệu tùy chỉnh (composite type) và mô tả lợi ích của cách tiếp cận này.",
   "UNIVERSAL", "", "REFERENCE_TYPE_DECLARATION")

lo("CIO-DEFINE-COMPOSITE-TYPE",
   "Define a Composite Type Grouping Properties and Methods",
   "Người học có khả năng định nghĩa một kiểu dữ liệu tùy chỉnh bao gồm các thuộc tính lưu trữ dữ liệu và các phương thức mô tả hành vi.",
   "CONCEPTUAL_IMPL", "ULO-COMPOSITE-DATA-TYPE", "REFERENCE_TYPE_DECLARATION")

lo("SIO-SWIFT-STRUCT-DEFINE",
   "Declare a Swift struct with stored properties",
   "Người học có khả năng khai báo một struct Swift bằng từ khóa struct, định nghĩa các thuộc tính lưu trữ (stored properties) với kiểu dữ liệu rõ ràng.",
   "SPECIFIC_IMPL", "CIO-DEFINE-COMPOSITE-TYPE", "REFERENCE_TYPE_DECLARATION")

lo("SIO-SWIFT-STRUCT-METHODS",
   "Define instance methods inside a Swift struct",
   "Người học có khả năng định nghĩa phương thức (method) bên trong một Swift struct, đọc thuộc tính của struct từ bên trong phương thức đó.",
   "SPECIFIC_IMPL", "CIO-DEFINE-COMPOSITE-TYPE", "REFERENCE_TYPE_DECLARATION")

lo("CIO-INSTANTIATE-COMPOSITE-TYPE",
   "Create and Use Instances of a Composite Data Type",
   "Người học có khả năng tạo một thể hiện (instance) cụ thể từ kiểu dữ liệu tùy chỉnh và truy cập các thành phần của nó.",
   "CONCEPTUAL_IMPL", "ULO-COMPOSITE-DATA-TYPE", "REFERENCE_TYPE_DECLARATION")

lo("SIO-SWIFT-STRUCT-INIT",
   "Create a Swift struct instance using memberwise initializer",
   "Người học có khả năng tạo một instance Swift struct bằng cú pháp memberwise initializer tự động (StructName(prop1: val1, prop2: val2)).",
   "SPECIFIC_IMPL", "CIO-INSTANTIATE-COMPOSITE-TYPE", "REFERENCE_TYPE_DECLARATION")

lo("SIO-SWIFT-STRUCT-ACCESS",
   "Access properties and call methods of a Swift struct instance",
   "Người học có khả năng sử dụng dot notation (instance.property, instance.method()) để truy cập thuộc tính và gọi phương thức trên một struct instance Swift.",
   "SPECIFIC_IMPL", "CIO-INSTANTIATE-COMPOSITE-TYPE", "REFERENCE_TYPE_DECLARATION")

# ── Arrays ──────────────────────────────────────────────────────────────────────

lo("ULO-ORDERED-COLLECTION",
   "Understand Ordered Indexed Collections",
   "Người học có khả năng giải thích khái niệm tập hợp có thứ tự với chỉ mục (indexed collection) và mô tả các tình huống nên dùng cấu trúc dữ liệu này.",
   "UNIVERSAL", "", "ARRAY_OPERATIONS")

lo("CIO-DECLARE-ORDERED-COLLECTION",
   "Declare and Initialize an Ordered Collection",
   "Người học có khả năng khai báo và khởi tạo một tập hợp có thứ tự với kiểu phần tử xác định và các giá trị ban đầu.",
   "CONCEPTUAL_IMPL", "ULO-ORDERED-COLLECTION", "ARRAY_OPERATIONS")

lo("SIO-SWIFT-ARRAY-DECLARE",
   "Declare a typed Swift Array with initial values",
   "Người học có khả năng khai báo một Swift Array với kiểu phần tử tường minh (VD: [Int], [String]) và danh sách giá trị ban đầu trong dấu ngoặc vuông.",
   "SPECIFIC_IMPL", "CIO-DECLARE-ORDERED-COLLECTION", "ARRAY_OPERATIONS")

lo("SIO-SWIFT-ARRAY-EMPTY",
   "Declare an empty Swift Array and append elements",
   "Người học có khả năng khởi tạo một Swift Array rỗng và sử dụng phương thức append(_:) để thêm phần tử vào cuối mảng.",
   "SPECIFIC_IMPL", "CIO-DECLARE-ORDERED-COLLECTION", "ARRAY_OPERATIONS")

lo("CIO-ACCESS-MODIFY-COLLECTION",
   "Access and Modify Elements of an Ordered Collection",
   "Người học có khả năng đọc và thay đổi các phần tử trong tập hợp có thứ tự thông qua chỉ mục (index) và các phương thức tích hợp.",
   "CONCEPTUAL_IMPL", "ULO-ORDERED-COLLECTION", "ARRAY_OPERATIONS")

lo("SIO-SWIFT-ARRAY-READ-INDEX",
   "Read an element from a Swift Array by index",
   "Người học có khả năng truy cập giá trị của phần tử tại vị trí index cụ thể trong Swift Array bằng cú pháp array[index] (zero-based).",
   "SPECIFIC_IMPL", "CIO-ACCESS-MODIFY-COLLECTION", "ARRAY_OPERATIONS")

lo("SIO-SWIFT-ARRAY-WRITE-INDEX",
   "Modify an element in a Swift Array by index",
   "Người học có khả năng thay đổi giá trị phần tử tại vị trí index trong một Swift Array có thể biến đổi (var) bằng cú pháp gán array[index] = newValue.",
   "SPECIFIC_IMPL", "CIO-ACCESS-MODIFY-COLLECTION", "ARRAY_OPERATIONS")

lo("SIO-SWIFT-ARRAY-PROPERTIES",
   "Use Swift Array properties to inspect the collection",
   "Người học có khả năng sử dụng thuộc tính count để lấy số phần tử và isEmpty để kiểm tra mảng rỗng trong Swift Array.",
   "SPECIFIC_IMPL", "CIO-ACCESS-MODIFY-COLLECTION", "ARRAY_OPERATIONS")

lo("SIO-SWIFT-ARRAY-METHODS",
   "Use Swift Array mutation methods",
   "Người học có khả năng sử dụng các phương thức biến đổi Swift Array: append(_:) thêm cuối, insert(_:at:) thêm vào vị trí, remove(at:) xóa phần tử theo index.",
   "SPECIFIC_IMPL", "CIO-ACCESS-MODIFY-COLLECTION", "ARRAY_OPERATIONS")

# ── For Loop ──────────────────────────────────────────────────────────────────

lo("ULO-DEFINITE-ITERATION",
   "Understand Definite Iteration",
   "Người học có khả năng giải thích và áp dụng khái niệm lặp lại một khối hành động một số lần biết trước để giải quyết các bài toán có cấu trúc lặp lại.",
   "UNIVERSAL", "", "FOR_LOOP")

lo("CIO-ITERATE-OVER-COLLECTION",
   "Traverse Every Element of a Collection Using a Loop",
   "Người học có khả năng sử dụng vòng lặp xác định để truy cập tuần tự từng phần tử trong một cấu trúc dữ liệu tập hợp.",
   "CONCEPTUAL_IMPL", "ULO-DEFINITE-ITERATION", "FOR_LOOP")

lo("SIO-SWIFT-FOR-IN-ARRAY",
   "Traverse a Swift Array using a for-in loop",
   "Người học có khả năng viết vòng lặp for item in myArray trong Swift để duyệt qua từng phần tử và thực hiện thao tác xử lý trên mỗi phần tử.",
   "SPECIFIC_IMPL", "CIO-ITERATE-OVER-COLLECTION", "FOR_LOOP, ARRAY_OPERATIONS")

lo("SIO-SWIFT-FOR-IN-STRING",
   "Traverse a Swift String character by character using for-in",
   "Người học có khả năng viết vòng lặp for char in myString trong Swift để xử lý từng ký tự của một chuỗi.",
   "SPECIFIC_IMPL", "CIO-ITERATE-OVER-COLLECTION", "FOR_LOOP")

lo("CIO-ITERATE-NUMERIC-RANGE",
   "Iterate Over a Numeric Range",
   "Người học có khả năng sử dụng vòng lặp xác định để lặp qua một dãy số với điểm bắt đầu, điểm kết thúc xác định.",
   "CONCEPTUAL_IMPL", "ULO-DEFINITE-ITERATION", "FOR_LOOP")

lo("SIO-SWIFT-FOR-IN-RANGE",
   "Use a Swift for-in loop with a numeric range",
   "Người học có khả năng viết vòng lặp Swift sử dụng closed range (1...10) và half-open range (1..<10) để lặp qua dãy số nguyên.",
   "SPECIFIC_IMPL", "CIO-ITERATE-NUMERIC-RANGE", "FOR_LOOP")

lo("SIO-SWIFT-RANGE-FORMS",
   "Distinguish closed and half-open range operators in Swift",
   "Người học có khả năng phân biệt toán tử ... (closed, bao gồm điểm cuối) và ..< (half-open, không bao gồm điểm cuối) trong vòng lặp Swift.",
   "SPECIFIC_IMPL", "CIO-ITERATE-NUMERIC-RANGE", "FOR_LOOP")

lo("CIO-PREDICT-LOOP-OUTCOME",
   "Trace and Predict the Outcome of a Definite Loop",
   "Người học có khả năng theo dõi từng bước lặp của một vòng lặp xác định để dự đoán chính xác trạng thái cuối cùng của các biến.",
   "CONCEPTUAL_IMPL", "ULO-DEFINITE-ITERATION", "FOR_LOOP")

lo("SIO-SWIFT-TRACE-FOR-LOOP",
   "Trace a Swift for-in loop to predict variable state",
   "Người học có khả năng theo dõi từng bước lặp của vòng lặp for-in Swift, ghi chép giá trị biến sau mỗi vòng, và dự đoán trạng thái cuối cùng.",
   "SPECIFIC_IMPL", "CIO-PREDICT-LOOP-OUTCOME", "FOR_LOOP")

lo("SIO-SWIFT-LOOP-ITERATION-COUNT",
   "Calculate the iteration count of a Swift for-in loop",
   "Người học có khả năng tính chính xác số lần lặp của một vòng lặp for-in Swift với closed range hoặc half-open range cho trước.",
   "SPECIFIC_IMPL", "CIO-PREDICT-LOOP-OUTCOME", "FOR_LOOP")

# ── While Loop ──────────────────────────────────────────────────────────────────

lo("ULO-INDEFINITE-ITERATION",
   "Understand Indefinite Iteration",
   "Người học có khả năng giải thích khái niệm lặp lại một khối hành động cho đến khi điều kiện dừng được thỏa mãn, và phân biệt với vòng lặp xác định.",
   "UNIVERSAL", "", "WHILE_LOOP")

lo("CIO-LOOP-WHILE-CONDITION",
   "Repeat a Block of Code While a Condition Holds",
   "Người học có khả năng xây dựng vòng lặp lặp lại một khối code chừng nào điều kiện boolean vẫn đúng.",
   "CONCEPTUAL_IMPL", "ULO-INDEFINITE-ITERATION", "WHILE_LOOP")

lo("SIO-SWIFT-WHILE-LOOP",
   "Write a Swift while loop with a continuation condition",
   "Người học có khả năng viết cú pháp vòng lặp while trong Swift với điều kiện tiếp tục phù hợp và thân vòng lặp thực hiện cập nhật trạng thái để đảm bảo hội tụ.",
   "SPECIFIC_IMPL", "CIO-LOOP-WHILE-CONDITION", "WHILE_LOOP")

lo("SIO-SWIFT-WHILE-TERMINATION",
   "Design a Swift while loop condition to prevent infinite loops",
   "Người học có khả năng xác định điều kiện dừng phù hợp cho vòng lặp while Swift và giải thích tại sao biến điều kiện phải được cập nhật trong thân vòng lặp.",
   "SPECIFIC_IMPL", "CIO-LOOP-WHILE-CONDITION", "WHILE_LOOP")

# ── Conditionals ──────────────────────────────────────────────────────────────

lo("ULO-CONDITIONAL-EXECUTION",
   "Understand Conditional Execution",
   "Người học có khả năng giải thích khái niệm rẽ nhánh chương trình dựa trên điều kiện và mô tả cách máy tính lựa chọn đường thực thi phù hợp.",
   "UNIVERSAL", "", "IF_ELSE_STATEMENT")

lo("CIO-BRANCH-ON-CONDITION",
   "Select Code Paths Based on a Boolean Condition",
   "Người học có khả năng xây dựng cấu trúc rẽ nhánh để thực thi các khối code khác nhau dựa trên giá trị của điều kiện boolean.",
   "CONCEPTUAL_IMPL", "ULO-CONDITIONAL-EXECUTION", "IF_ELSE_STATEMENT")

lo("SIO-SWIFT-IF-ELSE",
   "Write a Swift if / else if / else chain",
   "Người học có khả năng viết cấu trúc if / else if / else trong Swift để xử lý nhiều nhánh điều kiện loại trừ lẫn nhau.",
   "SPECIFIC_IMPL", "CIO-BRANCH-ON-CONDITION", "IF_ELSE_STATEMENT")

lo("SIO-SWIFT-SWITCH-CASE",
   "Write a Swift switch statement with case branches",
   "Người học có khả năng viết câu lệnh switch trong Swift với các nhánh case cụ thể và nhánh default, tuân thủ yêu cầu exhaustiveness của Swift.",
   "SPECIFIC_IMPL", "CIO-BRANCH-ON-CONDITION", "SWITCH_CASE")

lo("CIO-TRACE-CONDITIONAL-LOGIC",
   "Trace Conditional Logic to Predict Execution Path",
   "Người học có khả năng đọc cấu trúc điều kiện và theo dõi luồng thực thi để xác định nhánh nào sẽ chạy với các giá trị đầu vào cụ thể.",
   "CONCEPTUAL_IMPL", "ULO-CONDITIONAL-EXECUTION", "IF_ELSE_STATEMENT")

lo("SIO-SWIFT-TRACE-IF-CHAIN",
   "Trace a Swift if-else chain given specific input values",
   "Người học có khả năng theo dõi một chuỗi if/else if/else Swift với các giá trị đầu vào cụ thể và xác định chính xác nhánh nào được thực thi.",
   "SPECIFIC_IMPL", "CIO-TRACE-CONDITIONAL-LOGIC", "IF_ELSE_STATEMENT")

lo("SIO-SWIFT-TRACE-SWITCH",
   "Trace a Swift switch statement to determine matching case",
   "Người học có khả năng đánh giá câu lệnh switch Swift với một giá trị cho trước và xác định chính xác case nào khớp và được thực thi.",
   "SPECIFIC_IMPL", "CIO-TRACE-CONDITIONAL-LOGIC", "SWITCH_CASE")

# ── Variables & Constants ──────────────────────────────────────────────────────

lo("ULO-MUTABLE-IMMUTABLE-STATE",
   "Understand Mutable and Immutable State",
   "Người học có khả năng giải thích sự khác biệt giữa giá trị có thể thay đổi (mutable) và không thể thay đổi (immutable), và mô tả lợi ích của tính bất biến trong lập trình.",
   "UNIVERSAL", "", "PRIMITIVE_TYPE_DECLARATION")

lo("CIO-DECLARE-VALUE-BINDING",
   "Declare a Named Value Binding with Appropriate Mutability",
   "Người học có khả năng khai báo tên ràng buộc với giá trị, chọn đúng giữa biến đổi được và bất biến tùy theo nhu cầu sử dụng.",
   "CONCEPTUAL_IMPL", "ULO-MUTABLE-IMMUTABLE-STATE", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-LET-CONSTANT",
   "Declare an immutable constant in Swift using let",
   "Người học có khả năng khai báo hằng số Swift bằng từ khóa let, gán giá trị một lần duy nhất, và giải thích tại sao nên ưu tiên let hơn var khi giá trị không thay đổi.",
   "SPECIFIC_IMPL", "CIO-DECLARE-VALUE-BINDING", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-VAR-VARIABLE",
   "Declare a mutable variable in Swift using var",
   "Người học có khả năng khai báo biến Swift bằng từ khóa var và thực hiện gán lại giá trị mới cho biến sau khi đã khai báo.",
   "SPECIFIC_IMPL", "CIO-DECLARE-VALUE-BINDING", "PRIMITIVE_TYPE_DECLARATION")

lo("CIO-APPLY-TYPE-SYSTEM",
   "Apply Static Type System to Variable Declarations",
   "Người học có khả năng làm việc với hệ thống kiểu tĩnh của ngôn ngữ: suy luận kiểu tự động hoặc khai báo kiểu tường minh.",
   "CONCEPTUAL_IMPL", "ULO-MUTABLE-IMMUTABLE-STATE", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-TYPE-INFERENCE",
   "Use Swift type inference to omit explicit type annotation",
   "Người học có khả năng dựa vào cơ chế type inference của Swift để viết khai báo ngắn gọn (VD: let name = \"Alice\") và giải thích rằng Swift tự suy kiểu String.",
   "SPECIFIC_IMPL", "CIO-APPLY-TYPE-SYSTEM", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-EXPLICIT-TYPE",
   "Write explicit type annotations for Swift declarations",
   "Người học có khả năng thêm chú thích kiểu tường minh (VD: var count: Int = 0) cho khai báo Swift và nhận biết 4 kiểu nguyên thủy cơ bản: Int, Double, String, Bool.",
   "SPECIFIC_IMPL", "CIO-APPLY-TYPE-SYSTEM", "PRIMITIVE_TYPE_DECLARATION")

lo("CIO-APPLY-NAMING-CONVENTIONS",
   "Apply Consistent Naming Conventions for Identifiers",
   "Người học có khả năng đặt tên cho các định danh (biến, hằng, hàm) theo quy ước nhất quán và dễ đọc.",
   "CONCEPTUAL_IMPL", "ULO-MUTABLE-IMMUTABLE-STATE", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-CAMELCASE",
   "Apply lowerCamelCase naming for Swift identifiers",
   "Người học có khả năng đặt tên biến, hằng và hàm Swift theo chuẩn lowerCamelCase (VD: myVariableName, calculateTotal) và giải thích lý do của quy ước này.",
   "SPECIFIC_IMPL", "CIO-APPLY-NAMING-CONVENTIONS", "PRIMITIVE_TYPE_DECLARATION")

lo("SIO-SWIFT-ID-RULES",
   "Follow Swift identifier formation rules",
   "Người học có khả năng áp dụng đúng các quy tắc tạo tên định danh Swift: không bắt đầu bằng chữ số, không dùng ký tự đặc biệt (trừ _), và phân biệt hoa/thường.",
   "SPECIFIC_IMPL", "CIO-APPLY-NAMING-CONVENTIONS", "PRIMITIVE_TYPE_DECLARATION")


# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN 4: View Building with SwiftUI
# ═══════════════════════════════════════════════════════════════════════════════

lo("ULO-DECLARATIVE-UI",
   "Understand Declarative UI Programming",
   "Người học có khả năng giải thích mô hình lập trình khai báo (declarative) và phân biệt nó với mô hình mệnh lệnh (imperative) trong xây dựng giao diện người dùng.",
   "UNIVERSAL", "", "DECLARATIVE_UI_PARADIGM")

lo("CIO-DISTINGUISH-UI-PARADIGMS",
   "Distinguish Imperative and Declarative UI Construction",
   "Người học có khả năng so sánh hai cách tiếp cận xây dựng UI: mệnh lệnh (mô tả HOW) và khai báo (mô tả WHAT), và nhận ra ưu điểm của từng cách.",
   "CONCEPTUAL_IMPL", "ULO-DECLARATIVE-UI", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-DECLARATIVE-VS-IMPERATIVE",
   "Explain how SwiftUI's declarative model differs from UIKit",
   "Người học có khả năng mô tả sự khác biệt giữa cách SwiftUI khai báo UI qua body property và cách UIKit thao tác UI trực tiếp bằng các lời gọi hàm.",
   "SPECIFIC_IMPL", "CIO-DISTINGUISH-UI-PARADIGMS", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-STATE-DRIVEN-UPDATE",
   "Describe how SwiftUI re-renders views in response to state changes",
   "Người học có khả năng giải thích rằng SwiftUI tự động so sánh view tree trước và sau khi state thay đổi, rồi chỉ render lại phần giao diện cần thiết.",
   "SPECIFIC_IMPL", "CIO-DISTINGUISH-UI-PARADIGMS", "DECLARATIVE_UI_PARADIGM")

lo("ULO-VIEW-COMPOSITION",
   "Understand Composing Visual Content Views",
   "Người học có khả năng giải thích khái niệm xây dựng giao diện bằng cách kết hợp (compose) các thành phần hiển thị nhỏ hơn thành UI hoàn chỉnh.",
   "UNIVERSAL", "", "DECLARATIVE_UI_PARADIGM")

lo("CIO-DISPLAY-CONTENT-VIEWS",
   "Display Textual and Visual Content Using Views",
   "Người học có khả năng sử dụng các thành phần hiển thị nội dung cơ bản để trình bày văn bản, hình ảnh, và hình học trong UI.",
   "CONCEPTUAL_IMPL", "ULO-VIEW-COMPOSITION", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-TEXT-VIEW",
   "Use SwiftUI Text() to display a string",
   "Người học có khả năng sử dụng view Text(\"Hello\") trong SwiftUI để hiển thị một chuỗi văn bản trên màn hình.",
   "SPECIFIC_IMPL", "CIO-DISPLAY-CONTENT-VIEWS", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-IMAGE-VIEW",
   "Use SwiftUI Image() to display an asset or system icon",
   "Người học có khả năng sử dụng Image(\"asset-name\") và Image(systemName: \"icon\") trong SwiftUI để hiển thị hình ảnh từ Asset Catalog hoặc SF Symbols.",
   "SPECIFIC_IMPL", "CIO-DISPLAY-CONTENT-VIEWS", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-SHAPE-VIEW",
   "Use SwiftUI Shape views for geometric elements",
   "Người học có khả năng sử dụng các Shape view SwiftUI như Circle(), Rectangle(), và RoundedRectangle() để vẽ các hình học trong giao diện.",
   "SPECIFIC_IMPL", "CIO-DISPLAY-CONTENT-VIEWS", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-COLOR-VIEW",
   "Use SwiftUI Color as a standalone view",
   "Người học có khả năng sử dụng Color.blue, Color.red, và các màu tùy chỉnh trong SwiftUI như một view độc lập để lấp đầy không gian.",
   "SPECIFIC_IMPL", "CIO-DISPLAY-CONTENT-VIEWS", "DECLARATIVE_UI_PARADIGM")

lo("ULO-VIEW-STYLING",
   "Understand View Appearance Modification",
   "Người học có khả năng giải thích cơ chế modifier chain trong lập trình khai báo: mỗi modifier bao bọc view và trả về view mới đã được biến đổi.",
   "UNIVERSAL", "", "UI_MODIFIERS")

lo("CIO-APPLY-VIEW-MODIFIERS",
   "Modify View Appearance by Chaining Modifier Methods",
   "Người học có khả năng áp dụng các modifier vào view để thay đổi giao diện: khoảng cách, màu sắc, kích thước, font chữ.",
   "CONCEPTUAL_IMPL", "ULO-VIEW-STYLING", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-PADDING",
   "Apply .padding() to add spacing around a SwiftUI view",
   "Người học có khả năng gắn modifier .padding() và .padding(_:) vào view SwiftUI để tạo khoảng trắng đều hoặc có hướng cụ thể.",
   "SPECIFIC_IMPL", "CIO-APPLY-VIEW-MODIFIERS", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-BACKGROUND",
   "Apply .background() to set a SwiftUI view background",
   "Người học có khả năng sử dụng modifier .background(Color.blue) hoặc .background(Image(...)) để đặt nền cho một view SwiftUI.",
   "SPECIFIC_IMPL", "CIO-APPLY-VIEW-MODIFIERS", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-FRAME",
   "Apply .frame() to constrain a SwiftUI view's dimensions",
   "Người học có khả năng sử dụng modifier .frame(width:height:) và .frame(maxWidth: .infinity) để kiểm soát kích thước và căn chỉnh của view SwiftUI.",
   "SPECIFIC_IMPL", "CIO-APPLY-VIEW-MODIFIERS", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-FOREGROUND-COLOR",
   "Apply .foregroundColor() to change text or icon color in SwiftUI",
   "Người học có khả năng sử dụng modifier .foregroundColor(.red) để thay đổi màu chữ hoặc biểu tượng trong SwiftUI view.",
   "SPECIFIC_IMPL", "CIO-APPLY-VIEW-MODIFIERS", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-FONT",
   "Apply .font() to set SwiftUI text typography",
   "Người học có khả năng sử dụng modifier .font(.title), .font(.body), và .font(.system(size:)) để thiết lập kiểu chữ cho Text view trong SwiftUI.",
   "SPECIFIC_IMPL", "CIO-APPLY-VIEW-MODIFIERS", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-RESIZABLE",
   "Apply .resizable() to allow SwiftUI Image scaling",
   "Người học có khả năng gắn modifier .resizable() và .scaledToFit() / .scaledToFill() vào SwiftUI Image để kiểm soát cách hình ảnh co giãn.",
   "SPECIFIC_IMPL", "CIO-APPLY-VIEW-MODIFIERS", "UI_MODIFIERS")

lo("CIO-EVALUATE-MODIFIER-ORDER",
   "Predict How Modifier Order Affects Rendered Output",
   "Người học có khả năng phân tích thứ tự áp dụng modifier trong chuỗi modifier và dự đoán sự khác biệt về giao diện kết quả.",
   "CONCEPTUAL_IMPL", "ULO-VIEW-STYLING", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-ORDER-PREDICT",
   "Trace SwiftUI modifier order to predict visual differences",
   "Người học có khả năng so sánh hai đoạn code SwiftUI với modifier cùng loại nhưng khác thứ tự (.padding().background() vs .background().padding()) và dự đoán chính xác sự khác biệt trên màn hình.",
   "SPECIFIC_IMPL", "CIO-EVALUATE-MODIFIER-ORDER", "UI_MODIFIERS")

lo("SIO-SWIFT-MOD-ORDER-BACKGROUND-PADDING",
   "Explain why modifier order matters: .background() vs .padding() first",
   "Người học có khả năng giải thích bằng lời tại sao việc đặt .background() trước hay sau .padding() tạo ra hai kết quả hiển thị khác nhau trong SwiftUI, dựa trên cơ chế wrapper chain.",
   "SPECIFIC_IMPL", "CIO-EVALUATE-MODIFIER-ORDER", "UI_MODIFIERS")

lo("ULO-LAYOUT-COMPOSITION",
   "Understand Layout and View Tree Composition",
   "Người học có khả năng giải thích cách các view được tổ chức thành cấu trúc cây phân cấp (view tree) và cách các container layout điều phối vị trí của view con.",
   "UNIVERSAL", "", "DECLARATIVE_UI_PARADIGM")

lo("CIO-ARRANGE-VIEWS-IN-CONTAINER",
   "Position Multiple Views Using Layout Containers",
   "Người học có khả năng sử dụng các container layout để sắp xếp nhiều view con theo chiều ngang, dọc, hoặc theo chiều sâu (overlay).",
   "CONCEPTUAL_IMPL", "ULO-LAYOUT-COMPOSITION", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-HSTACK",
   "Arrange sibling views horizontally using SwiftUI HStack",
   "Người học có khả năng sử dụng HStack { } trong SwiftUI để sắp xếp các view con theo chiều ngang và điều chỉnh alignment và spacing.",
   "SPECIFIC_IMPL", "CIO-ARRANGE-VIEWS-IN-CONTAINER", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-VSTACK",
   "Arrange sibling views vertically using SwiftUI VStack",
   "Người học có khả năng sử dụng VStack { } trong SwiftUI để xếp các view con theo chiều dọc và cấu hình alignment và spacing.",
   "SPECIFIC_IMPL", "CIO-ARRANGE-VIEWS-IN-CONTAINER", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-ZSTACK",
   "Layer views on top of each other using SwiftUI ZStack",
   "Người học có khả năng sử dụng ZStack { } trong SwiftUI để chồng nhiều view lên nhau theo trục Z (độ sâu) và điều chỉnh alignment.",
   "SPECIFIC_IMPL", "CIO-ARRANGE-VIEWS-IN-CONTAINER", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-SPACER",
   "Use SwiftUI Spacer to distribute remaining space",
   "Người học có khả năng sử dụng Spacer() bên trong HStack hoặc VStack để đẩy các view ra xa nhau hoặc về phía cạnh của container.",
   "SPECIFIC_IMPL", "CIO-ARRANGE-VIEWS-IN-CONTAINER", "DECLARATIVE_UI_PARADIGM")

lo("CIO-DESCRIBE-VIEW-HIERARCHY",
   "Describe the Parent-Child View Tree Structure",
   "Người học có khả năng phân tích cây view của một giao diện SwiftUI và giải thích mối quan hệ cha-con giữa các view.",
   "CONCEPTUAL_IMPL", "ULO-LAYOUT-COMPOSITION", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-VIEW-TREE-MAP",
   "Map a SwiftUI view body to its parent-child view tree",
   "Người học có khả năng đọc code SwiftUI và vẽ sơ đồ cây view thể hiện chính xác quan hệ cha-con giữa tất cả các view trong body.",
   "SPECIFIC_IMPL", "CIO-DESCRIBE-VIEW-HIERARCHY", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-PARENT-CHILD-INHERIT",
   "Explain how parent views influence child view layout in SwiftUI",
   "Người học có khả năng giải thích cách view cha đề xuất kích thước cho view con và cách view con báo cáo kích thước thực tế của nó lại.",
   "SPECIFIC_IMPL", "CIO-DESCRIBE-VIEW-HIERARCHY", "DECLARATIVE_UI_PARADIGM")

lo("ULO-INTERACTIVE-CONTROLS",
   "Understand Interactive UI Controls",
   "Người học có khả năng giải thích vai trò của các control tương tác trong giao diện người dùng và mô tả cơ chế xử lý sự kiện người dùng.",
   "UNIVERSAL", "", "DECLARATIVE_UI_PARADIGM")

lo("CIO-IMPLEMENT-INTERACTIVE-CONTROL",
   "Add a User Interaction Control to a UI",
   "Người học có khả năng tích hợp control tương tác vào giao diện, kết nối nó với dữ liệu trạng thái và xác định hành động phản hồi.",
   "CONCEPTUAL_IMPL", "ULO-INTERACTIVE-CONTROLS", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-BUTTON",
   "Create a SwiftUI Button with an action closure",
   "Người học có khả năng tạo SwiftUI Button với label tùy chỉnh và closure action chứa code thực thi khi người dùng nhấn nút.",
   "SPECIFIC_IMPL", "CIO-IMPLEMENT-INTERACTIVE-CONTROL", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-TEXTFIELD",
   "Create a SwiftUI TextField bound to a string state variable",
   "Người học có khả năng tạo SwiftUI TextField với placeholder text và binding ($stateName) đến một @State String variable.",
   "SPECIFIC_IMPL", "CIO-IMPLEMENT-INTERACTIVE-CONTROL", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-SLIDER",
   "Create a SwiftUI Slider bound to a numeric state variable",
   "Người học có khả năng tạo SwiftUI Slider với range xác định (value: $stateVar, in: 0...100) để người dùng chọn giá trị số.",
   "SPECIFIC_IMPL", "CIO-IMPLEMENT-INTERACTIVE-CONTROL", "DECLARATIVE_UI_PARADIGM")

lo("SIO-SWIFT-TOGGLE",
   "Create a SwiftUI Toggle bound to a boolean state variable",
   "Người học có khả năng tạo SwiftUI Toggle với label và binding ($boolState) để hiển thị công tắc bật/tắt gắn với trạng thái boolean.",
   "SPECIFIC_IMPL", "CIO-IMPLEMENT-INTERACTIVE-CONTROL", "DECLARATIVE_UI_PARADIGM")

lo("ULO-DATA-DRIVEN-UI",
   "Understand Data-Driven UI with Reactive State",
   "Người học có khả năng giải thích khái niệm UI phản ứng (reactive): khi dữ liệu (state) thay đổi, giao diện tự động cập nhật để phản ánh trạng thái mới.",
   "UNIVERSAL", "", "LOCAL_VIEW_STATE")

lo("CIO-MANAGE-LOCAL-REACTIVE-STATE",
   "Declare and Use Reactive Local State in a View",
   "Người học có khả năng khai báo biến trạng thái phản ứng cục bộ trong một view và kết nối nó với các control tương tác để tạo UI động.",
   "CONCEPTUAL_IMPL", "ULO-DATA-DRIVEN-UI", "STATE_PROPERTY_WRAPPER")

lo("SIO-SWIFT-STATE-DECLARE",
   "Declare a @State property wrapper variable in a SwiftUI view",
   "Người học có khả năng khai báo @State private var trong SwiftUI struct, chọn đúng kiểu dữ liệu, và giải thích tại sao @State là cần thiết để SwiftUI theo dõi thay đổi.",
   "SPECIFIC_IMPL", "CIO-MANAGE-LOCAL-REACTIVE-STATE", "STATE_PROPERTY_WRAPPER")

lo("SIO-SWIFT-STATE-TWO-WAY-BIND",
   "Use $ prefix to create a two-way Binding to a @State variable",
   "Người học có khả năng sử dụng ký hiệu $ (VD: $myState) trong SwiftUI để truyền Binding hai chiều vào các control như TextField và Toggle.",
   "SPECIFIC_IMPL", "CIO-MANAGE-LOCAL-REACTIVE-STATE", "TWO_WAY_BINDING")


# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN 5: Debugging
# ═══════════════════════════════════════════════════════════════════════════════

lo("ULO-DEBUGGING-FUNDAMENTALS",
   "Understand Software Debugging Fundamentals",
   "Người học có khả năng giải thích quy trình tìm và sửa lỗi phần mềm (debugging) và mô tả các loại lỗi khác nhau có thể xảy ra trong vòng đời phát triển.",
   "UNIVERSAL", "", "SYNTAX_VS_RUNTIME_ERRORS")

lo("CIO-CLASSIFY-ERROR-TYPES",
   "Classify Programming Errors by Detection Phase",
   "Người học có khả năng phân loại lỗi lập trình theo giai đoạn phát hiện: lỗi cú pháp (compile-time) và lỗi thực thi (runtime).",
   "CONCEPTUAL_IMPL", "ULO-DEBUGGING-FUNDAMENTALS", "SYNTAX_VS_RUNTIME_ERRORS")

lo("SIO-SWIFT-SYNTAX-ERROR",
   "Identify a compile-time syntax error in Swift/Xcode",
   "Người học có khả năng nhận diện lỗi cú pháp trong mã Swift (thiếu dấu ngoặc, sai tên keyword...) qua thông báo lỗi màu đỏ xuất hiện ngay trong Xcode editor.",
   "SPECIFIC_IMPL", "CIO-CLASSIFY-ERROR-TYPES", "SYNTAX_VS_RUNTIME_ERRORS")

lo("SIO-SWIFT-RUNTIME-ERROR",
   "Identify a runtime error (crash) in a Swift application",
   "Người học có khả năng phân biệt lỗi runtime (ứng dụng crash khi chạy) với lỗi compile-time và giải thích các nguyên nhân phổ biến như index out of bounds.",
   "SPECIFIC_IMPL", "CIO-CLASSIFY-ERROR-TYPES", "SYNTAX_VS_RUNTIME_ERRORS")

lo("CIO-INTERPRET-ERROR-FEEDBACK",
   "Read and Interpret Error Feedback to Locate and Fix Faults",
   "Người học có khả năng đọc thông báo lỗi từ môi trường phát triển, định vị nguồn gốc lỗi, và áp dụng các bước sửa lỗi phù hợp.",
   "CONCEPTUAL_IMPL", "ULO-DEBUGGING-FUNDAMENTALS", "ERROR_MESSAGES")

lo("SIO-XCODE-READ-CONSOLE-ERRORS",
   "Read and interpret error messages in the Xcode console",
   "Người học có khả năng đọc output trong Xcode Debug Console, nhận diện thông báo lỗi và stack trace để xác định dòng code gây ra crash.",
   "SPECIFIC_IMPL", "CIO-INTERPRET-ERROR-FEEDBACK", "ERROR_MESSAGES")

lo("SIO-XCODE-APPLY-FIXIT",
   "Apply Xcode Fix-it suggestions to correct compile-time errors",
   "Người học có khả năng sử dụng tính năng Fix-it của Xcode: click vào gợi ý sửa lỗi tự động để áp dụng chỉnh sửa cú pháp đơn giản.",
   "SPECIFIC_IMPL", "CIO-INTERPRET-ERROR-FEEDBACK", "ERROR_MESSAGES")

lo("SIO-XCODE-ERROR-LINE-IDENTIFY",
   "Identify error type and line number from an Xcode error message",
   "Người học có khả năng đọc một thông báo lỗi Xcode và trích xuất: loại lỗi (error/warning), số dòng, tên file, và mô tả ngắn gọn của vấn đề.",
   "SPECIFIC_IMPL", "CIO-INTERPRET-ERROR-FEEDBACK", "SYNTAX_VS_RUNTIME_ERRORS")


# ═══════════════════════════════════════════════════════════════════════════════
# Output
# ═══════════════════════════════════════════════════════════════════════════════

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def load_status(repo_root: Path) -> dict:
    status_file = repo_root / "status.yaml"
    res = {}
    if status_file.is_file():
        with open(status_file, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line and not line.strip().startswith("#"):
                    k, v = line.split(":", 1)
                    res[k.strip()] = v.strip().strip("'\"")
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="[Reference Implementation] Generate structured LOs for swift-associate."
    )
    parser.add_argument(
        "--project", type=str,
        help="Project slug (default: reads active_project from status.yaml)"
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    slug = args.project
    if not slug:
        status = load_status(repo_root)
        slug = status.get("active_project")
        if not slug:
            print("❌ Error: Không có project. Truyền --project hoặc set active_project trong status.yaml.")
            sys.exit(1)

    output_tsv = repo_root / "projects" / slug / "output" / "learning-objectives.tsv"
    output_tsv.parent.mkdir(parents=True, exist_ok=True)

    with open(output_tsv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"])
        for r in los:
            writer.writerow(r)

    # Summary
    ulos = sum(1 for r in los if r[3] == "UNIVERSAL")
    cios = sum(1 for r in los if r[3] == "CONCEPTUAL_IMPL")
    sios = sum(1 for r in los if r[3] == "SPECIFIC_IMPL")
    print(f"[✓] Generated {len(los)} Learning Objectives ({ulos} ULO, {cios} CIO, {sios} SIO)")
    print(f"    → {output_tsv.relative_to(repo_root)}")
    print("[!] CIO names: language-neutral (no Swift). SIO names: Swift-specific.")
