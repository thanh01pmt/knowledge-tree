import os
import json
import csv
import sys
from pathlib import Path
from pydantic import BaseModel, Field

# Thư viện để parse dữ liệu (Yêu cầu: pip install openai pydantic)
try:
    from openai import OpenAI
except ImportError:
    print("Vui lòng cài đặt: pip install openai pydantic")
    sys.exit(1)

class LearningObjective(BaseModel):
    code: str = Field(description="Mã LO (VD: ULO-DESIGN, CIO-SWIFT-VARS, SIO-LET)")
    name: str = Field(description="Tên ngắn gọn của mục tiêu")
    description: str = Field(description="Mô tả chi tiết năng lực đạt được")
    lo_type: str = Field(description="Một trong các giá trị: UNIVERSAL, CONCEPTUAL_IMPL, SPECIFIC_IMPL")
    parent_lo_code: str = Field(description="Mã của LO cấp cha. ULO thì để trống. CIO trỏ về ULO. SIO trỏ về CIO.")
    concept_codes: str = Field(description="Từ khóa của Master Tree (VD: FOR_LOOP, VARIABLES, DATA_TYPES, USER_CENTERED_DESIGN)")

class LOExtractionResponse(BaseModel):
    learning_objectives: list[LearningObjective] = Field(description="Danh sách toàn bộ các LO phân rã từ tài liệu.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python llm_extract_lo.py <project_slug>")
        sys.exit(1)
        
    slug = sys.argv[1]
    
    # 1. Tìm thư mục chứa raw_pdf.txt
    project_dir = Path.cwd() / "projects" / slug
    raw_text_path = project_dir / ".work" / "raw_pdf.txt"
    output_tsv = project_dir / "output" / "learning-objectives.tsv"
    
    if not raw_text_path.exists():
        print(f"Error: {raw_text_path} không tồn tại.")
        sys.exit(1)
        
    text_content = raw_text_path.read_text(encoding="utf-8")
    
    # 2. Khởi tạo LLM Client (Sử dụng OpenAI chuẩn, có thể đổi base_url sang Gemini/OpenRouter)
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Vui lòng set biến môi trường OPENAI_API_KEY hoặc GEMINI_API_KEY.")
        sys.exit(1)
        
    # Cấu hình Client. Nếu dùng Gemini qua chuẩn OpenAI, thêm base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    print(f"[*] Đang gửi dữ liệu ({len(text_content)} ký tự) lên LLM để phân rã ULO -> CIO -> SIO...")
    
    system_prompt = """
    Bạn là một chuyên gia thiết kế chương trình học (Curriculum Designer) và Kiến trúc sư Taxonomy.
    Nhiệm vụ của bạn là đọc nội dung Syllabus (Objective Domains) và phân rã TẤT CẢ các bullet points thành hệ thống Learning Objectives (LO) đa tầng.
    
    Quy tắc phân rã bắt buộc:
    1. Cấp 1 (UNIVERSAL): ULO - Khái niệm cốt lõi, không phụ thuộc công nghệ. (parent_lo_code = "")
    2. Cấp 2 (CONCEPTUAL_IMPL): CIO - Cách hiện thực khái niệm bằng công nghệ cụ thể. (parent_lo_code trỏ về ULO tương ứng).
    3. Cấp 3 (SPECIFIC_IMPL): SIO - Kỹ năng chi tiết cực nhỏ, đo lường được. (parent_lo_code trỏ về CIO tương ứng).
    
    Quy tắc concept_codes: 
    Hãy đoán các keyword chuẩn hóa liên quan nhất (ví dụ: FOR_LOOP, VARIABLES, DATA_TYPES, USER_CENTERED_DESIGN, FUNCTIONS_METHODS, DECLARATIVE_UI_MODEL).
    
    Yêu cầu: Phân rã đầy đủ không bỏ sót bất kỳ dòng nào trong tài liệu. 1 gạch đầu dòng trong PDF có thể sinh ra từ 3 đến 5 LO (1 ULO, 1 CIO, nhiều SIO).
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06", # Hoặc gemini-2.5-pro nếu dùng base_url gemini
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Tài liệu Syllabus:\n{text_content}"}
        ],
        response_format=LOExtractionResponse,
    )

    result = completion.choices[0].message.parsed
    los = result.learning_objectives
    
    print(f"[*] LLM đã trích xuất thành công {len(los)} Learning Objectives!")
    
    # 3. Ghi ra file TSV
    with open(output_tsv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"])
        for lo in los:
            writer.writerow([lo.code, lo.name, lo.description, lo.lo_type, lo.parent_lo_code, lo.concept_codes])
            
    print(f"[*] Đã ghi đè thành công vào {output_tsv}")

if __name__ == "__main__":
    main()
