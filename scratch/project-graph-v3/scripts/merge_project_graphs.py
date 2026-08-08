#!/usr/bin/env python3
"""
Merge nhiều partial Project Graph (chạy --include tách nhóm) thành 1 graph hoàn chỉnh.

Vì sao cần: --include chỉ chạy 1 nhóm domain (VD: A+B hoặc C), output thiếu domain khác.
Script này gộp N partial graphs theo domain key — phần nào có data thì giữ, phần rỗng bỏ qua.

Usage:
  python merge_project_graphs.py \
      --inputs output/partial_ab.json output/partial_c.json \
      --output output/project_graph_raw.json
  # hoặc dạng key=value để kiểm soát thứ tự ưu tiên:
  python merge_project_graphs.py \
      --inputs ab=output/partial_ab.json c=output/partial_c.json \
      --output output/project_graph_raw.json
"""
import argparse
import json
import sys
from pathlib import Path

# Domain key → schema property key (khớp FLAG_TO_SCHEMA_KEY trong step1)
DOMAIN_KEYS = {
    "project": "project", "product": "product", "features": "features",
    "capabilities": "capabilities", "architecture": "architecture",
    "experience": "experience", "data_integration": "data_integration",
    "implementation": "implementation", "validation": "validation",
}


def is_empty(value) -> bool:
    """True nếu value 'rỗng' (không có data — domain không được bật)."""
    if isinstance(value, dict):
        return not value
    if isinstance(value, list):
        return not value
    return value is None or value == ""


def merge_graphs(graphs: list) -> dict:
    """Gộp nhiều graphs. Domain nào có data ở graph sau → giữ; rỗng → lấy graph trước."""
    result = {
        "schema_version": 3,
        "project": {}, "product": {}, "features": [], "capabilities": [],
        "architecture": {}, "experience": {}, "data_integration": {},
        "implementation": {}, "validation": {},
        "evidence": {}, "knowledge_mapping": {},
    }

    # Gộp theo thứ tự — graph sau ghi đè domain KHÔNG rỗng của nó
    for g in graphs:
        for key in DOMAIN_KEYS:
            val = g.get(key)
            if not is_empty(val):
                result[key] = val

    return result


def main():
    parser = argparse.ArgumentParser(description="Merge partial Project Graphs (--include tách nhóm)")
    parser.add_argument("--inputs", nargs="+", required=True,
                        help="Các file graph cần gộp. Dạng: path.json hoặc label=path.json "
                             "(label không quan trọng, chỉ cần thứ tự).")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    graphs = []
    for item in args.inputs:
        path = item.split("=", 1)[-1] if "=" in item else item
        p = Path(path)
        if not p.is_file():
            print(f"❌ Không tìm thấy: {p}", file=sys.stderr)
            sys.exit(1)
        g = json.load(open(p, encoding="utf-8"))
        graphs.append(g)
        print(f"[*] Load: {p} → features={len(g.get('features', []))}, "
              f"tasks={len(g.get('implementation', {}).get('tasks', []))}")

    result = merge_graphs(graphs)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    filled = [k for k in DOMAIN_KEYS if not is_empty(result.get(k))]
    print(f"[✓] Merged → {args.output}")
    print(f"    Domain có data: {filled}")
    print(f"    features: {len(result['features'])} | tasks: {len(result['implementation'].get('tasks', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
