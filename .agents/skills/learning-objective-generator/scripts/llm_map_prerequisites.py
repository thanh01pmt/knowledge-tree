#!/usr/bin/env python3
"""
llm_map_prerequisites.py — Phase E: Curriculum DAG Mapping
Đọc toàn bộ file learning-objectives.tsv đã hoàn chỉnh và bối cảnh DAG từ roadmap.sh
để suy luận và sinh ra các liên kết tiền đề giữa các Learning Objectives.
Kết quả xuất ra file output/lo_prerequisites.tsv chuẩn v2.3.
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
    from pydantic import BaseModel, Field
except ImportError:
    print("[ERROR] Cài đặt: pip install openai pydantic", file=sys.stderr)
    sys.exit(1)


# ─── Pydantic Models ──────────────────────────────────────────────────────────

class PrerequisiteLink(BaseModel):
    learning_objective_code: str = Field(description="Mã LO đích (Target LO code)")
    prerequisite_lo_code: str = Field(description="Mã LO tiền đề (LO bắt buộc phải học trước)")
    rationale: str = Field(description="Lý do ngắn gọn tại sao lại có liên kết này dựa trên DAG context")

class PrerequisiteBatch(BaseModel):
    links: list[PrerequisiteLink]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()

def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))

def load_status(repo_root: Path) -> dict:
    status_file = repo_root / "status.yaml"
    res = {}
    if status_file.is_file():
        for line in status_file.read_text(encoding="utf-8").splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                res[k.strip()] = v.strip().strip("'\"")
    return res


# ─── LLM Generation ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Bạn là một Chuyên gia Thiết kế Curriculum (Curriculum Designer) am hiểu về Sequence & Sequencing.

Nhiệm vụ: Nhìn vào danh sách Learning Objectives (ULO, CIO, SIO) đã hoàn chỉnh và bối cảnh Đồ thị Tiền đề (Prerequisite DAG Context) từ nguồn syllabus. 
Hãy thiết lập các liên kết tiền đề giữa các Learning Objectives (Target LO -> Prerequisite LO).

Nguyên tắc:
1. learning_objective_code và prerequisite_lo_code PHẢI LÀ MÃ TỒN TẠI trong danh sách LO cung cấp. KHÔNG được bịa mã.
2. Nếu trong bối cảnh DAG, Concept B bắt buộc học sau Concept A -> Các LO (ULO/CIO/SIO) của Concept B có thể phụ thuộc vào các LO tương ứng của Concept A.
3. Không cần link mọi thứ vào nhau, chỉ link những gì thực sự mang tính TIỀN ĐỀ BẮT BUỘC (Prerequisite).
4. SIO có thể phụ thuộc vào SIO. ULO phụ thuộc vào ULO. CIO phụ thuộc vào CIO.
5. Không tạo vòng lặp (Cyclic dependency)."""


def map_prerequisites(client: OpenAI, los: list[dict], dag_context: str, model: str) -> list[dict]:
    # Tóm tắt danh sách LO (chỉ lấy thông tin quan trọng để tránh quá tải token)
    lo_summary = []
    for lo in los:
        t = lo.get("lo_type", "UNKNOWN")
        c = lo.get("code", "")
        n = lo.get("name", "")
        desc = lo.get("description", "")[:100]
        lo_summary.append(f"[{t}] {c}: {n} - {desc}")
    
    lo_text = "\n".join(lo_summary)
    
    user_prompt = f"""
===== DANH SÁCH HỌC PHẦN (LEARNING OBJECTIVES) =====
{lo_text}

===== BỐI CẢNH ĐỒ THỊ TIỀN ĐỀ TỪ NGUỒN (DAG CONTEXT) =====
{dag_context[:8000]}

Dựa vào bối cảnh DAG trên, hãy suy luận và trích xuất danh sách các liên kết tiền đề giữa các Learning Objectives.
"""

    print(f"[*] Đang phân tích đồ thị tiền đề (Model: {model})...")
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=PrerequisiteBatch,
        temperature=0.1,
    )
    result = completion.choices[0].message.parsed
    return [link.model_dump() for link in result.links] if result else []


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase E: Cấu hình Curriculum DAG (Prerequisite Mapping)")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)

    slug = args.project
    if not slug:
        status = load_status(repo_root)
        slug = status.get("active_project")
        if not slug:
            print("[ERROR] Không tìm thấy project. Dùng --project hoặc set active_project.", file=sys.stderr)
            sys.exit(1)

    project_dir = repo_root / "projects" / slug
    work_dir = project_dir / ".work"
    out_dir = project_dir / "output"
    
    lo_tsv_path = out_dir / "learning-objectives.tsv"
    dag_path = work_dir / "roadmap_dag_context.json"
    audit_path = work_dir / "context-audit.md"
    
    if not lo_tsv_path.is_file():
        print(f"[ERROR] Không tìm thấy {lo_tsv_path}. Phải chạy /generate-sios --merge trước.", file=sys.stderr)
        sys.exit(1)

    # Đọc danh sách LO
    los = []
    with open(lo_tsv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            los.append(row)
            
    print(f"[*] Đã load {len(los)} Learning Objectives.")

    # Đọc DAG Context
    dag_context = ""
    if dag_path.is_file():
        print(f"[*] Đã load roadmap DAG context.")
        with open(dag_path, encoding="utf-8") as f:
            try:
                dag_json = json.load(f)
                dag_lines = [f"Node: {d.get('name')} | Prerequisite: {d.get('prerequisite')}" for d in dag_json]
                dag_context = "\n".join(dag_lines)
            except json.JSONDecodeError:
                dag_context = dag_path.read_text(encoding="utf-8")
    elif audit_path.is_file():
        print(f"[*] Không có roadmap DAG json. Dùng context-audit.md làm fallback.")
        dag_context = audit_path.read_text(encoding="utf-8")
    else:
        print("[WARN] Không tìm thấy source bối cảnh nào. LLM sẽ tự suy luận hoàn toàn.")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY không tìm thấy.", file=sys.stderr)
        sys.exit(1)
    try:
        import httpx
        http_client = httpx.Client(transport=httpx.HTTPTransport())
        base_url = os.environ.get("OPENAI_BASE_URL") or None
        client = OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
    except Exception as e:
        client = OpenAI(api_key=api_key)

    links = map_prerequisites(client, los, dag_context, args.model)
    
    # Lọc bỏ các mã không hợp lệ (ảo giác của LLM)
    valid_codes = {lo["code"] for lo in los}
    valid_links = []
    for link in links:
        if link["learning_objective_code"] in valid_codes and link["prerequisite_lo_code"] in valid_codes:
            valid_links.append(link)
        else:
            print(f"[WARN] Drop invalid link: {link['learning_objective_code']} -> {link['prerequisite_lo_code']}")
            
    # Ghi TSV
    out_tsv = out_dir / "lo_prerequisites.tsv"
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_tsv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["learning_objective_code", "prerequisite_lo_code", "rationale"], delimiter="\t")
        writer.writeheader()
        writer.writerows(valid_links)
        
    print(f"[✓] Đã sinh {len(valid_links)} liên kết tiền đề -> {out_tsv.relative_to(repo_root)}")
    print(f"    (Có thể xem chi tiết trong file TSV bao gồm cột rationale để kiểm tra)")

if __name__ == "__main__":
    main()
