#!/usr/bin/env python3
"""
query_master_tree.py — Công cụ tìm kiếm trên Master Knowledge Tree.

Hỗ trợ tìm kiếm mờ (fuzzy search) theo tên, mã, và từ khóa (keywords).
Hỗ trợ lọc theo cấp độ (level) và mã cha (parent).
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


def strip_diacritics(text: str) -> str:
    """Normalize Vietnamese/Unicode diacritics to ASCII base for tolerant matching.
    E.g. 'Đồ thị' -> 'Do thi'. Keeps the original-folded equivalence class so
    that queries with or without accents match data with or without accents."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_text(text):
    if not text:
        return ""
    return strip_diacritics(text).lower().strip()


def word_boundary_match(needle: str, haystack: str) -> bool:
    """Whole-word match using word boundaries. Avoids 'SQL' matching 'SQLITE'
    or 'C' matching every word containing 'c'."""
    if not needle or not haystack:
        return False
    pattern = r"\b" + re.escape(needle) + r"\b"
    return re.search(pattern, haystack) is not None


def calculate_score(query, code, name, keywords, description=""):
    """Tính điểm khớp đơn giản:
    - Khớp chính xác code: 100
    - Khớp chính xác name: 90
    - Từ khóa nằm trong keywords (word-boundary): 80
    - Chứa trong name (word-boundary): 50
    - Chứa trong keywords (word-boundary): 30
    - Chứa trong description (word-boundary): 20
    """
    q = normalize_text(query)
    c = normalize_text(code)
    n = normalize_text(name)
    k = normalize_text(keywords)
    d = normalize_text(description)

    if not q:
        return 1

    if q == c:
        return 100
    if q == n:
        return 90
    # keyword exact match (word-boundary on comma-separated list)
    if any(word_boundary_match(q, kw.strip()) for kw in k.split(",")):
        return 80
    if word_boundary_match(q, n):
        return 50
    if word_boundary_match(q, k):
        return 30
    if word_boundary_match(q, d):
        return 20

    # Thử tách từ — multi-word query: count how many query words appear in
    # name/keywords/description with word boundaries.
    q_words = q.split()
    if len(q_words) > 1:
        matched_words = 0
        for w in q_words:
            if (word_boundary_match(w, n)
                    or word_boundary_match(w, k)
                    or word_boundary_match(w, d)):
                matched_words += 1
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
    repo_root = find_repo_root(Path.cwd())
    parser = argparse.ArgumentParser(description="Tìm kiếm node trong Master Tree.")
    parser.add_argument("--query", type=str, default="", help="Từ khóa tìm kiếm (tên, mã, keyword).")
    parser.add_argument("--level", type=str, choices=["fields", "subjects", "categories", "topics", "concepts"], help="Giới hạn tìm kiếm ở 1 cấp độ cụ thể.")
    parser.add_argument("--parent", type=str, default="", help="Mã của node cha (để lọc dạng Top-Down).")
    parser.add_argument("--limit", type=int, default=5, help="Số kết quả trả về tối đa.")
    parser.add_argument("--tree-file", type=str, default=str(repo_root / ".agents/skills/taxonomy-mapper/resources/master_tree.json"))
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
            description = row.get("description", "")

            score = calculate_score(args.query, code, name, keywords, description)
            
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
