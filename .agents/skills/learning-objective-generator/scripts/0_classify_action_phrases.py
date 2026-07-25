import sys
import os
import argparse
import json
import asyncio
import csv
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Setup client
load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "ollama"),
    base_url=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
)

PROMPT_TEMPLATE = """Bạn là một chuyên gia Kiến trúc chương trình học (Curriculum Architect).
Nhiệm vụ của bạn là đọc một danh sách các "Mục tiêu hành động" (Action Phrases) và danh sách các "Khái niệm" (Concepts).
Hãy thực hiện 2 việc cho MỖI Action Phrase:
1. Phân loại nó vào 1 trong 3 tầng Learning Objective:
   - "ULO" (Universal Learning Objective): Các mục tiêu vĩ mô, nguyên lý cốt lõi, không phụ thuộc công nghệ.
   - "CIO" (Conceptual Implementation Objective): Thuật toán, logic, hoặc cách giải quyết vấn đề bằng code một cách tổng quát.
   - "SIO" (Specific Implementation Objective): Cực kỳ cụ thể, gắn chặt với công nghệ, thư viện, hoặc cú pháp cụ thể (VD: @State, VStack, HStack, SwiftUI).
2. Khớp nối (Map) nó với MỘT `concept_code` phù hợp nhất từ danh sách Concepts.

DANH SÁCH CONCEPTS:
{concepts_text}

DANH SÁCH ACTION PHRASES CẦN XỬ LÝ:
{phrases_text}

Trả về dữ liệu dưới định dạng JSON tuân thủ schema quy định.
Schema JSON:
{{
  "classified_phrases": [
    {{
      "id": "1.3",
      "verb": "Assess",
      "phrase": "Assess a visual design with accessibility in mind",
      "cognitive_level": "Evaluating",
      "lo_type": "ULO",
      "mapped_concept_code": "ACCESSIBILITY"
    }}
  ]
}}
"""

async def process_phrases(phrases_file, concepts_file, out_file):
    # Load concepts
    concepts = []
    with open(concepts_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            concepts.append({
                "code": row["code"],
                "name": row["name"],
                "description": row["description"]
            })
    
    concepts_text = ""
    for c in concepts:
        concepts_text += f"- {c['code']}: {c['name']} ({c['description']})\n"
        
    # Load phrases
    with open(phrases_file, "r", encoding="utf-8") as f:
        phrases = json.load(f)
        
    phrases_text = json.dumps(phrases, ensure_ascii=False, indent=2)
    
    prompt = PROMPT_TEMPLATE.format(concepts_text=concepts_text, phrases_text=phrases_text)
    
    print(f"[PROCESS] Đang gọi LLM phân loại {len(phrases)} Action Phrases...")
    try:
        response = await client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "deepseek-v4-flash:cloud"),
            messages=[
                {"role": "system", "content": "You are a precise JSON data extraction assistant. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        result = json.loads(response.choices[0].message.content)
        classified_phrases = result.get("classified_phrases", [])
        
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(classified_phrases, f, ensure_ascii=False, indent=2)
            
        print(f"\\n[SUCCESS] Hoàn thành! Đã phân loại được {len(classified_phrases)} phrases.")
        print(f"[INFO] Đã lưu vào: {out_file}")
    except Exception as e:
        print(f"[ERROR] Lỗi khi xử lý LLM: {e}")

def main():
    parser = argparse.ArgumentParser(description="Classify and Map Action Phrases.")
    parser.add_argument("--project", required=True, help="Tên project (vd: swift-associate)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    while not (repo_root / ".agents").exists() and repo_root.parent != repo_root:
        repo_root = repo_root.parent

    out_dir = repo_root / "projects" / args.project / "output"
    
    phrases_file = out_dir / "action_phrases.json"
    concepts_file = out_dir / "concepts.tsv"
    out_file = out_dir / "classified_action_phrases.json"
    
    if not phrases_file.exists():
        print(f"[ERROR] Không tìm thấy file {phrases_file}")
        sys.exit(1)
        
    if not concepts_file.exists():
        print(f"[ERROR] Không tìm thấy file {concepts_file}")
        sys.exit(1)
        
    asyncio.run(process_phrases(phrases_file, concepts_file, out_file))

if __name__ == "__main__":
    main()
