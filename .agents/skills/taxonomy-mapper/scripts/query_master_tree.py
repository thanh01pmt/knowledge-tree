#!/usr/bin/env python3
"""
query_master_tree.py — Công cụ tìm kiếm trên Master Knowledge Tree.

Hỗ trợ tìm kiếm mờ (fuzzy search) theo tên, mã, và từ khóa (keywords).
Hỗ trợ lọc theo cấp độ (level) và mã cha (parent).
"""

import argparse
import json
import re
from pathlib import Path

def normalize_text(text):
    if not text:
        return ""
    return text.lower().strip()

def calculate_score(query, code, name, keywords):
    """Tính điểm khớp đơn giản: 
    - Khớp chính xác code: 100
    - Khớp chính xác name: 90
    - Từ khóa nằm trong keywords: 80
    - Chứa trong name: 50
    """
    q = normalize_text(query)
    c = normalize_text(code)
    n = normalize_text(name)
    k = normalize_text(keywords)
    
    if not q:
        return 1

    if q == c:
        return 100
    if q == n:
        return 90
    if q in k.split(','):
        return 80
    if q in n:
        return 50
    if q in k:
        return 30
        
    # Thử tách từ
    q_words = q.split()
    matched_words = sum(1 for w in q_words if w in n or w in k)
    if matched_words > 0:
        return matched_words * 10
        
    return 0

def get_parent_field(level):
    mapping = {
        'subjects': 'field_codes',
        'categories': 'subject_codes',
        'topics': 'category_codes',
        'concepts': 'topic_codes',
        'learning_objectives': 'concept_codes'
    }
    return mapping.get(level)

def main():
    parser = argparse.ArgumentParser(description="Tìm kiếm node trong Master Tree.")
    parser.add_argument("--query", type=str, default="", help="Từ khóa tìm kiếm (tên, mã, keyword).")
    parser.add_argument("--level", type=str, choices=["fields", "subjects", "categories", "topics", "concepts"], help="Giới hạn tìm kiếm ở 1 cấp độ cụ thể.")
    parser.add_argument("--parent", type=str, default="", help="Mã của node cha (để lọc dạng Top-Down).")
    parser.add_argument("--limit", type=int, default=5, help="Số kết quả trả về tối đa.")
    parser.add_argument("--tree-file", type=str, default=".agents/skills/taxonomy-mapper/resources/master_tree.json")
    args = parser.parse_args()

    tree_path = Path(args.tree_file).resolve()
    if not tree_path.exists():
        print(f"Lỗi: Không tìm thấy file JSON tại {tree_path}")
        print("Hãy chạy script parse_master_tree.py trước!")
        exit(1)

    with open(tree_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    
    levels_to_search = [args.level] if args.level else ["fields", "subjects", "categories", "topics", "concepts"]

    for lvl in levels_to_search:
        rows = data.get(lvl, [])
        parent_field = get_parent_field(lvl)
        
        for row in rows:
            # Lọc theo parent
            if args.parent and parent_field:
                parents_str = row.get(parent_field, "")
                if args.parent not in [p.strip() for p in parents_str.replace(";", ",").replace("|", ",").split(",")]:
                    continue
            elif args.parent and not parent_field: # Fields don't have parents
                continue
                
            code = row.get("code", "")
            name = row.get("name", "")
            keywords = row.get("keywords", "")
            
            score = calculate_score(args.query, code, name, keywords)
            
            if score > 0 or not args.query:
                results.append({
                    "level": lvl,
                    "code": code,
                    "name": name,
                    "description": row.get("description", ""),
                    "score": score
                })

    # Sắp xếp theo score giảm dần
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:args.limit]

    if not results:
        print("Không tìm thấy kết quả phù hợp.")
        return

    print(f"Top {len(results)} kết quả phù hợp nhất:")
    print("-" * 60)
    for res in results:
        print(f"[{res['level'].upper()}] Mã: {res['code']}")
        print(f"Tên: {res['name']}")
        print(f"Mô tả: {res['description']}")
        print("-" * 60)

if __name__ == "__main__":
    main()
