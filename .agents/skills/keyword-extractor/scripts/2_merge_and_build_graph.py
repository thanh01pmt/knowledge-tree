#!/usr/bin/env python3
"""
2_merge_and_build_graph.py — Gộp các đồ thị cục bộ thành đồ thị toàn cục.
Tối ưu hóa: Canonical hóa ID dựa trên Label để chống trùng lặp, tính Weight cho Edges.

Input:  .work/kw/chunks_graph/*.json
Output: output/keyword_graph.json
"""

import argparse
import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

def make_canonical_id(label: str) -> str:
    """Biến đổi label thành ID chuẩn (kebab-case) để gộp."""
    s = str(label).lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s\-]+', '-', s)
    return s.strip('-')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Tên project (slug)")
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    for _ in range(20):
        if (repo_root / ".agents").is_dir():
            break
        if repo_root.parent == repo_root:
            repo_root = Path.cwd()
            break
        repo_root = repo_root.parent

    work_dir = repo_root / "projects" / args.project / ".work" / "kw"
    chunks_dir = work_dir / "chunks_graph"
    
    if not chunks_dir.exists():
        print(f"[ERROR] Không tìm thấy thư mục {chunks_dir}", file=sys.stderr)
        sys.exit(1)
        
    out_dir = repo_root / "projects" / args.project / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "keyword_graph.json"
    
    global_nodes = {}
    global_edges = defaultdict(int) # key: (source, target, relation), value: weight
    
    chunk_files = list(chunks_dir.glob("*.json"))
    print(f"[INFO] Tìm thấy {len(chunk_files)} file đồ thị cục bộ.")
    
    for fpath in chunk_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])
            
            # Map original ID to Canonical ID for this chunk
            id_map = {}
            for n in nodes:
                orig_id = n.get("id")
                label = n.get("label", orig_id)
                can_id = make_canonical_id(label)
                id_map[orig_id] = can_id
                
                # Cập nhật Node
                if can_id not in global_nodes:
                    global_nodes[can_id] = {
                        "id": can_id,
                        "label": label,
                        "type": n.get("type", "concept"),
                        "definition": n.get("definition", "")
                    }
                else:
                    # Có thể giữ định nghĩa dài hơn nếu bị trùng
                    existing_def = global_nodes[can_id]["definition"]
                    new_def = n.get("definition", "")
                    if len(new_def) > len(existing_def):
                        global_nodes[can_id]["definition"] = new_def
                        
            # Cập nhật Edge
            for e in edges:
                orig_src = e.get("source")
                orig_tgt = e.get("target")
                relation = e.get("relation", "related_to")
                
                can_src = id_map.get(orig_src)
                can_tgt = id_map.get(orig_tgt)
                
                if can_src and can_tgt:
                    edge_key = (can_src, can_tgt, relation)
                    global_edges[edge_key] += 1
                    
        except Exception as e:
            print(f"[WARN] Lỗi đọc file {fpath.name}: {e}")
            
    # Serialize
    final_nodes = list(global_nodes.values())
    final_edges = [
        {
            "source": src,
            "target": tgt,
            "relation": rel,
            "weight": weight
        }
        for (src, tgt, rel), weight in global_edges.items()
    ]
    
    out_data = {
        "nodes": final_nodes,
        "edges": final_edges
    }
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Đã gộp thành công vào {out_file.relative_to(repo_root)}")
    print(f"Tổng Nodes: {len(final_nodes)}")
    print(f"Tổng Edges: {len(final_edges)}")

if __name__ == "__main__":
    main()
