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
    code: str = Field(description="Ma Concept (UPPER_SNAKE_CASE, vi du DATABASE_ORM)")
    name: str = Field(description="Ten khai niem (Trung tinh 100%)")
    description: str = Field(description="Dinh nghia khai quat (Trung tinh 100%)")
    keywords: str = Field(description="Cac tu khoa lien quan, cach nhau bang dau phay")

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
    """Doc master_tree.json de lay danh sach domain cap cao VA danh sach Concepts + lookup."""
    master_file = repo_root / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "master_tree.json"
    if not master_file.exists():
        return "", "[]", {}
    try:
        with open(master_file, "r", encoding="utf-8") as f:
            master = json.load(f)
        
        names = set()
        for level in ["fields", "subjects", "categories", "topics"]:
            for item in master.get(level, []):
                if "name" in item:
                    names.add(item["name"])
        
        master_concepts = []
        master_lookup = {}
        for c in master.get("concepts", []):
            master_concepts.append({
                "code": c.get("code", ""),
                "name": c.get("name", ""),
                "description": c.get("description", ""),
                "keywords": c.get("keywords", "")
            })
            master_lookup[c.get("code", "")] = {
                "cs2023_ka_mapping": c.get("cs2023_ka_mapping", ""),
                "metadata": c.get("metadata", "{}"),
            }
            
        return ", ".join(sorted(names)), json.dumps(master_concepts, ensure_ascii=False), master_lookup
    except Exception as e:
        print(f"[WARN] Loi doc master_tree.json: {e}")
        return "", "[]", {}

async def evaluate_concepts(client: AsyncOpenAI, candidates: list, domain_names: str, master_concepts_str: str) -> list:
    """Gui danh sach ung vien cho LLM de loc trung tinh."""
    prompt = f"""Ban la mot chuyen gia thiet ke Ontology Su pham (Pedagogical Ontology).
Duoi day la danh sach cac Khai niem (Nodes) duoc trich xuat tu tai lieu.

Quy tac TOI THUONG 1 (Technology-Agnostic): BAT BUOC khai niem phai 100% TRUNG TINH.
KHONG DUOC CHUA ten cong nghe, ngon ngu lap trinh, hay framework cu the (nhu Swift, Python, Docker, SwiftUI).
Vi du: "View" thi duoc chap nhan, "SwiftUI View" thi bi loai bo. "Protocol" thi duoc, "Swift Protocol" thi loai.

Quy tac TOI THUONG 2 (Scope Resolution): Concept la cap do chi tiet (hat nhan).
KHONG DUOC tao ra cac Concept co ten hoac pham vi (scope) trung lap voi cac Domain cap cao (Fields, Subjects, Categories, Topics) da co trong Master Tree.
Danh sach cac Domain cap cao (cam trung lap):
[{domain_names}]

Quy tac TOI THUONG 3 (Pedagogical Depth & Clustering): Khai niem BAT BUOC phai co DO SAU SU PHAM.
- CHAP NHAN: Cac nguyen ly, cau truc du lieu, mo hinh, co che cot loi.
- GOP (CLUSTERING): Neu co nhieu ung vien la cac thanh phan nho cua cung mot ho, KHONG DUOC tao tung Concept rieng le cho moi cai. Hay GOP chung lai thanh mot Concept lon va day cac tu khoa con vao 'keywords'.
- LOAI BO (REJECT): Cac danh tu chung chung, cac buoc thuc hanh qua nho khong co ly thuyet.

Quy tac TOI THUONG 4 (Entity Resolution - Uu tien Master Tree):
Duoi day la danh sach cac Master Concepts DA TON TAI trong he thong (dang JSON):
{master_concepts_str}

Truoc khi sinh ra mot Concept moi, BAT BUOC phai doi chieu y nghia cua no voi Danh sach Master Concepts o tren.
- Neu khai niem ung vien co y nghia tuong duong, HOAC la tap con nam tron trong pham vi cua mot Master Concept, ban BAT BUOC phai TAI SU DUNG nguyen xi 'code', 'name', va 'description' cua Master Concept do. DOI VOI TRUONG 'keywords', ban phai NOI (merge) cac keywords cu dang co trong Master Concept voi cac keywords moi trich xuat duoc.
- CHI tao Concept moi (dang UPPER_SNAKE_CASE) khi hoan toan khong co Master Concept nao phu hop. Tuyet doi khong tao moi neu co the ep no vao lam tap con.

Quy tac TOI THUONG 5 (Ngon ngu):
TAT CA 'name' va 'description' cua Concept MOI BAT BUOC phai duoc viet bang TIENG VIET (van phong hoc thuat, chuan muc).

Nhiem vu:
1. Loc va gop cac khai niem dam bao Trung tinh (Quy tac 1), Chi tiet (Quy tac 2), va Su pham/Clustering (Quy tac 3).
2. Tai su dung Master Concept toi da (Quy tac 4). Neu tao moi, sinh ra 'code' UPPER_SNAKE_CASE.
3. Dam bao ngon ngu TIENG VIET (Quy tac 5).
4. Gom cac tu khoa goc vao truong 'keywords' (phan tach bang dau phay).

Danh sach ung vien:
{json.dumps(candidates, ensure_ascii=False, indent=2)}

Tra ve du lieu duoi dinh dang JSON tuan thu schema quy dinh.
Schema JSON mau:
{{
  "concepts": [
    {{"code": "...", "name": "...", "description": "...", "keywords": "..."}}
  ]
}}
"""

    print("[PROCESS] Dang goi LLM de danh gia su trung tinh va chong trung lap domain...")
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
            print("[WARN] Du lieu tra ve khong chua mang 'concepts'.")
            return []
        
        validated = ConceptList.model_validate(data)
        return validated.concepts
    except Exception as e:
        print(f"[ERROR] Qua trinh LLM that bai: {e}")
        return []

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Ten project (slug)")
    parser.add_argument("--top-n", type=int, default=100, help="So luong Node co ket noi cao nhat de danh gia")
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
        print(f"[ERROR] Khong tim thay do thi: {graph_file}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(graph_file, "r", encoding="utf-8") as f:
            graph_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Khong the doc {graph_file}: {e}")
        sys.exit(1)
        
    allowed_types = {"conceptual", "procedural"}
    nodes = {n["id"]: n for n in graph_data.get("nodes", []) if n.get("type") in allowed_types}
    edges = graph_data.get("edges", [])
    
    print(f"[INFO] Tong so Conceptual/Procedural Nodes hop le trong Graph: {len(nodes)}")
    if not nodes:
        print("[WARN] Khong co Node (conceptual/procedural) nao de xu ly.")
        sys.exit(0)

    degree = defaultdict(int)
    for e in edges:
        degree[e["source"]] += e.get("weight", 1)
        degree[e["target"]] += e.get("weight", 1)
        
    sorted_nodes = sorted(nodes.values(), key=lambda x: degree[x["id"]], reverse=True)
    top_candidates = sorted_nodes[:args.top_n]
    print(f"[INFO] Tong so Nodes trong Graph: {len(nodes)}")
    print(f"[INFO] Lay Top {len(top_candidates)} Nodes co do lien ket cao nhat lam ung vien Concept.")
    
    llm_payload = [
        {"id": n["id"], "label": n["label"], "definition": n["definition"]}
        for n in top_candidates
    ]
    
    domain_names, master_concepts_str, master_lookup = load_master_data(repo_root)
    client = get_client()
    approved_concepts = await evaluate_concepts(client, llm_payload, domain_names, master_concepts_str)
    
    if not approved_concepts:
        print("[WARN] LLM khong tra ve Concept nao hop le.")
        sys.exit(0)
        
    print(f"[SUCCESS] LLM da duyet va tra ve {len(approved_concepts)} Concepts trung tinh.")
    
    # Ghi ra TSV
    headers = ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"]
    
    with open(concepts_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(headers)
        
        for c in approved_concepts:
            # Lookup cs2023_ka_mapping and metadata from Master Tree if available
            master_info = master_lookup.get(c.code, {})
            row = [
                c.code,
                c.name,
                c.description,
                "", # topic_codes (trong)
                c.keywords,
                master_info.get("cs2023_ka_mapping", ""), # tu Master Tree neu co
                master_info.get("metadata", "{}"),         # tu Master Tree neu co
            ]
            writer.writerow(row)
            
    print(f"[SUCCESS] Da luu vao {concepts_file.relative_to(repo_root)}")

if __name__ == "__main__":
    asyncio.run(main())
