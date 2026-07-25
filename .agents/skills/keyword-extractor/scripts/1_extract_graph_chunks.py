#!/usr/bin/env python3
"""
1_extract_graph_chunks.py — Trích xuất Graph (Nodes & Edges) từ từng chunk văn bản.
Sử dụng LLM (DeepSeek-V4-Flash) thông qua Async OpenAI Client.

Input:  .work/kw/chunks.json (từ bước chunk_source.py)
Output: .work/kw/chunks_graph/chunk_xxxx.json
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List

try:
    from openai import AsyncOpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] pip install openai pydantic", file=sys.stderr)
    sys.exit(1)

# --- Schema định dạng output (GraphRAG) ---
class Node(BaseModel):
    id: str = Field(description="Mã định danh duy nhất (kebab-case hoặc snake_case)")
    label: str = Field(description="Tên khái niệm gốc (giữ nguyên case phổ biến nhất)")
    type: str = Field(description="Loại: concept, tool, framework, language, other")
    definition: str = Field(description="Định nghĩa hoặc mô tả ngắn gọn dựa trên ngữ cảnh")

class Edge(BaseModel):
    source: str = Field(description="Node ID nguồn")
    target: str = Field(description="Node ID đích")
    relation: str = Field(description="Mối quan hệ (ví dụ: contains, implements, is_a, related_to)")

class GraphChunk(BaseModel):
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)

# --- Helpers ---
def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))

def get_client() -> AsyncOpenAI:
    api_key = os.environ.get("OPENAI_API_KEY", "ollama")
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
    if base_url:
        return AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=120.0)
    return AsyncOpenAI(api_key=api_key, timeout=120.0)

async def process_chunk(client: AsyncOpenAI, chunk: dict, out_dir: Path, semaphore: asyncio.Semaphore):
    chunk_id = chunk["chunk_id"]
    out_file = out_dir / f"{chunk_id}.json"
    
    if out_file.exists():
        print(f"[SKIP] {chunk_id} đã được xử lý.")
        return
        
    prompt = f"""Bạn là một chuyên gia bóc tách Đồ thị Tri thức (Knowledge Graph Ontology) và Thiết kế Sư phạm (Pedagogical Design).
Hãy phân tích đoạn văn bản sau và trích xuất các Thực thể (Nodes) và các Mối quan hệ (Edges) giữa chúng.

YÊU CẦU PHÂN LOẠI NODE NGHIÊM NGẶT (Dựa theo thang Bloom):
Bạn BẮT BUỘC phải phân loại Node thành đúng 5 loại (`type`) sau đây:
1. "type": "factual" (Dữ kiện): Các danh từ riêng, tên gọi, công cụ cụ thể mang tính thuộc lòng (Ví dụ: `Swift`, `Xcode`, `Apple`, `iOS`).
2. "type": "conceptual" (Khái niệm): Các khái niệm lập trình, nguyên lý, cấu trúc dữ liệu, thành phần UI (Ví dụ: `Variables`, `Array`, `Loop Structures`, `UI Modifiers`, `Button`, `View Hierarchy`).
3. "type": "procedural" (Quy trình): Các kỹ thuật, phương pháp, vòng đời (Ví dụ: `Design Cycle`, `Prototyping`, `Unit Testing`).
4. "type": "metacognitive" (Siêu nhận thức): Các chiến lược học tập, nhận thức (ít gặp).
5. "type": "action" (Động từ): Các hành động, kỹ năng nhận thức (Ví dụ: `Create`, `Evaluate`, `Import`, `Differentiate`). Động từ cực kỳ hữu ích để sinh LOs.

YÊU CẦU VỀ EDGE:
Xây dựng mối quan hệ giữa các Node, đặc biệt là quan hệ giữa `action` và các loại kiến thức (Ví dụ: Nguồn: `Import` -> Đích: `Asset` -> Quan hệ: `acts_on`).

Trích xuất cạn kiệt, không bỏ sót khái niệm hay kỹ năng chuyên ngành nào.
Trả về dữ liệu dưới định dạng JSON tuân thủ schema quy định.

Schema JSON mẫu:
{{
  "nodes": [
    {{"id": "node_1", "label": "Structure", "type": "conceptual", "definition": "A Swift structure type."}},
    {{"id": "node_2", "label": "Evaluate", "type": "action", "definition": "To assess the execution of functions."}},
    {{"id": "node_3", "label": "Swift", "type": "factual", "definition": "Apple's programming language."}}
  ],
  "edges": [
    {{"source": "node_2", "target": "node_1", "relation": "acts_on"}}
  ]
}}

Ngữ cảnh (Heading): {chunk.get('heading_trail', '')}
Văn bản:
{chunk.get('text', '')}
"""
    
    async with semaphore:
        print(f"[PROCESS] Đang xử lý {chunk_id}...")
        try:
            # Sử dụng mô hình từ biến môi trường LLM_MODEL hoặc mặc định là deepseek
            # DeepSeek/OpenAI compat endpoints hỗ trợ JSON object
            response = await client.chat.completions.create(
                model=os.environ.get("LLM_MODEL", "deepseek-v4-flash:cloud"),
                messages=[
                    {"role": "system", "content": "You are a precise JSON data extraction assistant. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            # Validate json
            data = json.loads(content)
            # Lấy trường nodes/edges nếu nó nằm trong wrapper nào đó, nhưng theo prompt thì nằm ngay ở root
            if "nodes" not in data:
                print(f"[WARN] {chunk_id}: Dữ liệu không chứa mảng 'nodes'. Đã bỏ qua.")
                return

            validated = GraphChunk.model_validate(data)
            
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(validated.model_dump(), f, ensure_ascii=False, indent=2)
            print(f"[DONE] {chunk_id} - {len(validated.nodes)} nodes, {len(validated.edges)} edges.")
            
        except Exception as e:
            print(f"[ERROR] {chunk_id}: {e}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Tên project (slug)")
    args = parser.parse_args()

    # Tìm repo_root bằng cách dò ngược từ cwd
    cur = Path.cwd().resolve()
    repo_root = cur
    for _ in range(20):
        if (cur / ".agents").is_dir():
            repo_root = cur
            break
        if cur.parent == cur:
            break
        cur = cur.parent

    load_env(repo_root)

    work_dir = repo_root / "projects" / args.project / ".work" / "kw"
    chunks_file = work_dir / "chunks.json"
    
    if not chunks_file.exists():
        print(f"[ERROR] Không tìm thấy file {chunks_file}", file=sys.stderr)
        sys.exit(1)
        
    out_dir = work_dir / "chunks_graph"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    client = get_client()
    semaphore = asyncio.Semaphore(10) # Xử lý tối đa 10 chunk đồng thời
    
    tasks = [process_chunk(client, chunk, out_dir, semaphore) for chunk in chunks]
    await asyncio.gather(*tasks)
    
    print("\n[SUCCESS] Hoàn thành trích xuất Graph cho tất cả chunks.")

if __name__ == "__main__":
    asyncio.run(main())
