import sys
import os
import argparse
import json
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Setup client
load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "ollama"),
    base_url=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
)

PROMPT_TEMPLATE = """Bạn là một chuyên gia Sư phạm (Pedagogical Expert) và Thiết kế Khung chương trình (Curriculum Designer).
Nhiệm vụ của bạn là đọc đoạn văn bản (được trích xuất từ tài liệu giáo trình) và tìm ra tất cả các "Mục tiêu học tập" (Learning Objectives).

ĐẶC ĐIỂM NHẬN DẠNG MỤC TIÊU HỌC TẬP:
- Thường bắt đầu bằng một số hiệu (VD: 1.1, 2.3).
- LUÔN LUÔN bắt đầu bằng một trong các Động từ Bloom (Bloom's Taxonomy Verbs) dưới đây:
  + Remembering: Identify, Recognize, Define, List, Recall, State, Label, Match
  + Understanding: Explain, Interpret, Summarize, Classify, Compare, Infer, Paraphrase, Describe
  + Applying: Apply, Calculate, Compute, Use, Solve, Demonstrate, Implement, Execute, Determine
  + Analyzing: Analyze, Differentiate, Distinguish, Contrast, Organize, Structure, Attribute, Deconstruct, Outline, Relate
  + Evaluating: Evaluate, Judge, Critique, Justify, Recommend, Assess, Defend, Prioritize
  + Creating: Design, Construct, Develop, Formulate, Propose, Combine

YÊU CẦU XỬ LÝ:
1. Văn bản PDF có thể bị dính chữ (Ví dụ: "1.1. Summarize the design cycle 3.1. Write, call..."). Bạn BẮT BUỘC phải ngắt chúng thành các câu riêng biệt hợp lý.
2. Với mỗi câu tìm được, trích xuất:
   - "id": Số hiệu của mục tiêu (ví dụ: "1.1", "3.2"). Nếu không có số hiệu thì để trống "".
   - "verb": Động từ Bloom bắt đầu câu (ví dụ: "Summarize", "Differentiate").
   - "phrase": Toàn bộ câu hoàn chỉnh (bắt đầu từ động từ, KHÔNG bao gồm số hiệu).
   - "cognitive_level": Cấp độ nhận thức tương ứng với động từ đó (Remembering, Understanding, Applying, Analyzing, Evaluating, Creating).

CHỈ TRÍCH XUẤT CÁC CÂU LÀ MỤC TIÊU HỌC TẬP (Bắt đầu bằng động từ). Đừng bịa ra mục tiêu nếu văn bản không có.

Văn bản:
{text}

Trả về dữ liệu dưới định dạng JSON tuân thủ schema quy định.
Schema JSON:
{{
  "action_phrases": [
    {{"id": "1.1", "verb": "Summarize", "phrase": "Summarize the design cycle", "cognitive_level": "Understanding"}}
  ]
}}
"""

async def extract_action_phrases_from_chunk(chunk):
    text = chunk.get("text", "").strip()
    if not text:
        return []
        
    prompt = PROMPT_TEMPLATE.format(text=text)
    
    print(f"[PROCESS] Đang xử lý chunk {chunk.get('id')}...")
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
        phrases = result.get("action_phrases", [])
        print(f"[DONE] {chunk.get('id')} - Tìm thấy {len(phrases)} phrases.")
        return phrases
    except Exception as e:
        print(f"[ERROR] Lỗi khi xử lý {chunk.get('id')}: {e}")
        return []

async def process_all_chunks(chunks_file, out_file):
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"[INFO] Tổng số chunks cần quét: {len(chunks)}")
    
    # Run concurrently (batching is recommended if too many chunks, but chunks are usually ~10-20)
    tasks = [extract_action_phrases_from_chunk(chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    
    all_phrases = []
    for r in results:
        all_phrases.extend(r)
        
    # Deduplicate (sometimes chunks overlap)
    unique_phrases = []
    seen = set()
    for p in all_phrases:
        identifier = f"{p.get('id', '')}-{p.get('verb', '')}-{p.get('phrase', '')}"
        if identifier not in seen:
            seen.add(identifier)
            unique_phrases.append(p)
            
    # Sort by ID
    def parse_id(item):
        id_str = item.get("id", "")
        if not id_str:
            return [999]
        parts = id_str.split('.')
        try:
            return [int(p) for p in parts if p.isdigit()]
        except:
            return [999]
            
    unique_phrases.sort(key=parse_id)
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(unique_phrases, f, ensure_ascii=False, indent=2)
        
    print(f"\\n[SUCCESS] Hoàn thành! Đã trích xuất được {len(unique_phrases)} Action Phrases.")
    print(f"[INFO] Đã lưu vào: {out_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract Action Phrases (LOs) from chunks using LLM.")
    parser.add_argument("--project", required=True, help="Tên project (vd: swift-associate)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    while not (repo_root / ".agents").exists() and repo_root.parent != repo_root:
        repo_root = repo_root.parent

    kw_dir = repo_root / "projects" / args.project / ".work" / "kw"
    out_dir = repo_root / "projects" / args.project / "output"
    
    chunks_file = kw_dir / "chunks.json"
    out_file = out_dir / "action_phrases.json"
    
    if not chunks_file.exists():
        print(f"[ERROR] Không tìm thấy file {chunks_file}")
        sys.exit(1)
        
    asyncio.run(process_all_chunks(chunks_file, out_file))

if __name__ == "__main__":
    main()
