#!/usr/bin/env python3
"""
3_escalate_to_concepts.py — Phân tích đồ thị, lọc khái niệm trung tính qua LLM và xuất concepts.tsv.
"""

import argparse
import asyncio
import csv
import json
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import List

try:
    from openai import AsyncOpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] pip install openai pydantic", file=sys.stderr)
    sys.exit(1)

class Concept(BaseModel):
    code: str = Field(description="Mã Concept (UPPER_SNAKE_CASE, ví dụ DATABASE_ORM)")
    name: str = Field(description="Tên khái niệm (Trung tính 100%)")
    description: str = Field(description="Định nghĩa khái quát (Trung tính 100%)")
    keywords: str = Field(description="Các từ khóa liên quan, cách nhau bằng dấu phẩy")

class ConceptList(BaseModel):
    concepts: List[Concept]

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

def load_master_data(repo_root: Path):
    """Đọc master_tree.json để lấy danh sách domain cấp cao (fields, subjects, categories, topics) VÀ danh sách Concepts."""
    master_file = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree.json"
    if not master_file.exists():
        return "", "[]"
    try:
        with open(master_file, "r", encoding="utf-8") as f:
            master = json.load(f)
        
        # Load high-level domains
        names = set()
        for level in ["fields", "subjects", "categories", "topics"]:
            for item in master.get(level, []):
                if "name" in item:
                    names.add(item["name"])
        
        # Load master concepts
        master_concepts = []
        for c in master.get("concepts", []):
            master_concepts.append({
                "code": c.get("code", ""),
                "name": c.get("name", ""),
                "description": c.get("description", ""),
                "keywords": c.get("keywords", "")
            })
            
        return ", ".join(sorted(names)), json.dumps(master_concepts, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Lỗi đọc master_tree.json: {e}")
        return "", "[]"

async def evaluate_concepts(client: AsyncOpenAI, candidates: list, domain_names: str, master_concepts_str: str) -> list:
    """Gửi danh sách ứng viên cho LLM để lọc trung tính."""
    
    prompt = f"""Bạn là một chuyên gia thiết kế Ontology Sư phạm (Pedagogical Ontology).
Dưới đây là danh sách các Khái niệm (Nodes) được trích xuất từ tài liệu.

Quy tắc TỐI THƯỢNG 1 (Technology-Agnostic): BẮT BUỘC khái niệm phải 100% TRUNG TÍNH. 
KHÔNG ĐƯỢC CHỨA tên công nghệ, ngôn ngữ lập trình, hay framework cụ thể (như Swift, Python, Docker, SwiftUI).
Ví dụ: "View" thì được chấp nhận, "SwiftUI View" thì bị loại bỏ. "Protocol" thì được, "Swift Protocol" thì loại.

Quy tắc TỐI THƯỢNG 2 (Scope Resolution): Concept là cấp độ chi tiết (hạt nhân). 
KHÔNG ĐƯỢC tạo ra các Concept có tên hoặc phạm vi (scope) trùng lặp với các Domain cấp cao (Fields, Subjects, Categories, Topics) đã có trong Master Tree.
Danh sách các Domain cấp cao (cấm trùng lặp):
[{domain_names}]

Quy tắc TỐI THƯỢNG 3 (Pedagogical Depth & Clustering): Khái niệm BẮT BUỘC phải có ĐỘ SÂU SƯ PHẠM.
- CHẤP NHẬN: Các nguyên lý, cấu trúc dữ liệu, mô hình, cơ chế cốt lõi.
- GỘP (CLUSTERING): Nếu có nhiều ứng viên là các thành phần nhỏ của cùng một họ (Ví dụ: Button, Slider, TextField, Toggle), KHÔNG ĐƯỢC tạo từng Concept riêng lẻ cho mỗi cái. Hãy GỘP chúng lại thành một Concept lớn (Ví dụ: `INTERACTIVE_COMPONENTS` hoặc `UI_CONTROLS`) và đẩy các từ khóa con vào 'keywords'.
- LOẠI BỎ (REJECT): Các danh từ chung chung, các bước thực hành quá nhỏ không có lý thuyết.

Quy tắc TỐI THƯỢNG 4 (Entity Resolution - Ưu tiên Master Tree):
Dưới đây là danh sách các Master Concepts ĐÃ TỒN TẠI trong hệ thống (dạng JSON):
{master_concepts_str}

Trước khi sinh ra một Concept mới, BẮT BUỘC phải đối chiếu ý nghĩa của nó với Danh sách Master Concepts ở trên. 
- Nếu khái niệm ứng viên có ý nghĩa tương đương, HOẶC là tập con nằm trọn trong phạm vi của một Master Concept (Ví dụ: Asset thuộc về PROJECT_ASSETS_MANAGEMENT), bạn BẮT BUỘC phải TÁI SỬ DỤNG nguyên xi 'code', 'name', và 'description' của Master Concept đó. ĐỐI VỚI TRƯỜNG 'keywords', bạn phải NỐI (merge) các keywords cũ đang có trong Master Concept với các keywords mới trích xuất được.
- CHỈ tạo Concept mới (dạng UPPER_SNAKE_CASE) khi hoàn toàn không có Master Concept nào phù hợp. Tuyệt đối không tạo mới nếu có thể ép nó vào làm tập con.

Quy tắc TỐI THƯỢNG 5 (Ngôn ngữ):
TẤT CẢ 'name' và 'description' của Concept MỚI BẮT BUỘC phải được viết bằng TIẾNG VIỆT (văn phong học thuật, chuẩn mực).

Nhiệm vụ:
1. Lọc và gộp các khái niệm đảm bảo Trung tính (Quy tắc 1), Chi tiết (Quy tắc 2), và Sư phạm/Clustering (Quy tắc 3).
2. Tái sử dụng Master Concept tối đa (Quy tắc 4). Nếu tạo mới, sinh ra 'code' UPPER_SNAKE_CASE.
3. Đảm bảo ngôn ngữ TIẾNG VIỆT (Quy tắc 5).
4. Gom các từ khóa gốc vào trường 'keywords' (phân tách bằng dấu phẩy).

Danh sách ứng viên:
{json.dumps(candidates, ensure_ascii=False, indent=2)}

Trả về dữ liệu dưới định dạng JSON tuân thủ schema quy định.
Schema JSON mẫu:
{{
  "concepts": [
    {{"code": "...", "name": "...", "description": "...", "keywords": "..."}}
  ]
}}
"""

    print("[PROCESS] Đang gọi LLM để đánh giá sự trung tính và chống trùng lặp domain...")
    try:
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
        data = json.loads(content)
        if "concepts" not in data:
            print("[WARN] Dữ liệu trả về không chứa mảng 'concepts'.")
            return []
        
        validated = ConceptList.model_validate(data)
        return validated.concepts
    except Exception as e:
        print(f"[ERROR] Quá trình LLM thất bại: {e}")
        return []

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Tên project (slug)")
    parser.add_argument("--top-n", type=int, default=100, help="Số lượng Node có kết nối cao nhất để đánh giá")
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    for _ in range(20):
        if (repo_root / ".agents").is_dir():
            break
        if repo_root.parent == repo_root:
            repo_root = Path.cwd()
            break
        repo_root = repo_root.parent

    load_env(repo_root)

    out_dir = repo_root / "projects" / args.project / "output"
    graph_file = out_dir / "keyword_graph.json"
    concepts_file = out_dir / "concepts.tsv"
    
    if not graph_file.exists():
        print(f"[ERROR] Không tìm thấy đồ thị: {graph_file}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(graph_file, "r", encoding="utf-8") as f:
            graph_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Không thể đọc {graph_file}: {e}")
        sys.exit(1)
        
    # Chỉ lấy các Node có type là "conceptual" hoặc "procedural" để đưa lên làm Concept
    # Bỏ qua "factual" (quá vụn vặt), "action" (động từ), và "metacognitive"
    allowed_types = {"conceptual", "procedural"}
    nodes = {n["id"]: n for n in graph_data.get("nodes", []) if n.get("type") in allowed_types}
    edges = graph_data.get("edges", [])
    
    print(f"[INFO] Tổng số Conceptual/Procedural Nodes hợp lệ trong Graph: {len(nodes)}")
    if not nodes:
        print("[WARN] Không có Node (conceptual/procedural) nào để xử lý.")
        sys.exit(0)

    # Tính Degree (Số lượng kết nối) cho mỗi Node
    degree = defaultdict(int)
    for e in edges:
        degree[e["source"]] += e.get("weight", 1)
        degree[e["target"]] += e.get("weight", 1)
        
    # Sắp xếp Nodes theo Degree giảm dần
    sorted_nodes = sorted(nodes.values(), key=lambda x: degree[x["id"]], reverse=True)
    
    # Lấy Top N
    top_candidates = sorted_nodes[:args.top_n]
    print(f"[INFO] Tổng số Nodes trong Graph: {len(nodes)}")
    print(f"[INFO] Lấy Top {len(top_candidates)} Nodes có độ liên kết cao nhất làm ứng viên Concept.")
    
    # Chuẩn bị dữ liệu gửi LLM
    llm_payload = [
        {"id": n["id"], "label": n["label"], "definition": n["definition"]}
        for n in top_candidates
    ]
    
    domain_names, master_concepts_str = load_master_data(repo_root)
    client = get_client()
    approved_concepts = await evaluate_concepts(client, llm_payload, domain_names, master_concepts_str)
    
    if not approved_concepts:
        print("[WARN] LLM không trả về Concept nào hợp lệ.")
        sys.exit(0)
        
    print(f"[SUCCESS] LLM đã duyệt và trả về {len(approved_concepts)} Concepts trung tính.")
    
    # Ghi ra TSV
    headers = ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"]
    
    with open(concepts_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(headers)
        
        for c in approved_concepts:
            row = [
                c.code,
                c.name,
                c.description,
                "", # topic_codes (trống)
                c.keywords,
                "", # cs2023_ka_mapping (trống)
                "{}" # metadata (trống)
            ]
            writer.writerow(row)
            
    print(f"[SUCCESS] Đã lưu vào {concepts_file.relative_to(repo_root)}")

if __name__ == "__main__":
    asyncio.run(main())
