#!/usr/bin/env python3
"""
check_master_sync.py — Kiểm tra đồng bộ (và kéo dữ liệu mới) giữa Master TSV và Supabase.

Các chức năng:
1. Đọc dữ liệu từ file Master TSV nội bộ.
2. Tải dữ liệu các bảng (fields, subjects, categories, topics, concepts) từ Supabase.
3. So sánh:
   - Thiếu trên DB (Chỉ có ở TSV)
   - Thiếu trên TSV (Chỉ có ở DB)
   - Lệch thông tin (Tên, mô tả, quan hệ cha-con...)
4. Hỗ trợ --sync-down: Ghi đè file TSV bằng dữ liệu từ Supabase, giữ nguyên định dạng header gốc.
"""

import argparse
import os
import sys
from pathlib import Path

# Thêm path để import master_tree_parser
script_dir = Path(__file__).resolve().parent
validator_dir = script_dir.parent.parent / "tree-validator" / "scripts"
if validator_dir.is_dir() and str(validator_dir) not in sys.path:
    sys.path.insert(0, str(validator_dir))

try:
    from master_tree_parser import parse_master_tsv, SECTIONS, SKIP_PREFIXES, get_default_master_tsv_path
except ImportError:
    print("❌ Error: Cannot import master_tree_parser. Make sure it's in .agents/skills/tree-validator/scripts/")
    sys.exit(1)

from supabase import create_client

def load_env(repo_root: Path):
    env_path = repo_root / ".env"
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

def dicts_are_equal(d1, d2, ignore_keys=None):
    if ignore_keys is None:
        ignore_keys = {"id", "organization_code", "created_at", "updated_at", "created_by"}
    k1 = set(d1.keys()) - ignore_keys
    all_keys = k1
    for k in all_keys:
        v1 = str(d1.get(k, "")).strip()
        
        # Handle array fields from Supabase vs comma-separated from TSV
        v2_raw = d2.get(k, "")
        if v2_raw is None:
            v2 = ""
        elif isinstance(v2_raw, list):
            v2 = ",".join([str(x).strip() for x in v2_raw if str(x).strip()])
        else:
            v2 = str(v2_raw).strip()
            
        if v1 != v2:
            return False, k, v1, v2
    return True, None, None, None

def main():
    parser = argparse.ArgumentParser(description="Kiểm tra đồng bộ Master TSV và Supabase")
    parser.add_argument("--sync-down", action="store_true", help="Cập nhật TSV local dựa trên dữ liệu từ Supabase")
    parser.add_argument("--tsv", type=str, default=str(get_default_master_tsv_path()), help="Đường dẫn đến file TSV")
    args = parser.parse_args()

    tsv_path = Path(args.tsv)
    if not tsv_path.is_file():
        print(f"❌ File không tồn tại: {tsv_path}")
        sys.exit(1)

    repo_root = tsv_path.parent
    for _ in range(5):
        if (repo_root / ".agents").is_dir():
            break
        repo_root = repo_root.parent

    load_env(repo_root)
    url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SERVICE_ROLE_KEY")
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL và SERVICE_ROLE_KEY phải được set trong .env")
        sys.exit(1)

    supabase = create_client(url, service_key)

    # 1. Parse local TSV
    print(f"📄 Đang đọc file TSV: {tsv_path.name}...")
    local_data = parse_master_tsv(tsv_path)

    # 2. Fetch from DB
    print("☁️ Đang lấy dữ liệu từ Supabase...")
    db_data = {k: [] for k in local_data.keys()}
    table_names = ["fields", "subjects", "categories", "topics", "concepts"]
    
    for table in table_names:
        try:
            # Fetch all rows for the master tables. Master data is usually < 10k rows.
            # PostgREST max is 1000 by default, we loop if needed or just use limit(10000)
            res = supabase.table(table).select("*").limit(10000).execute()
            db_data[table] = res.data
        except Exception as e:
            print(f"❌ Lỗi khi lấy dữ liệu bảng {table}: {e}")
            sys.exit(1)

    # 3. Compare
    print("\n🔍 ĐANG KIỂM TRA ĐỒNG BỘ...\n")
    
    missing_in_db = []
    missing_in_tsv = []
    mismatches = []
    
    db_dicts = {}
    for table in table_names:
        db_dicts[table] = {row["code"]: row for row in db_data[table] if row.get("code")}

    for table in table_names:
        local_codes = set()
        for l_row in local_data[table]:
            code = l_row.get("code", "").strip()
            if not code: continue
            local_codes.add(code)
            
            if code not in db_dicts[table]:
                missing_in_db.append((table, code))
            else:
                db_row = db_dicts[table][code]
                eq, bad_key, v_local, v_db = dicts_are_equal(l_row, db_row)
                if not eq:
                    mismatches.append((table, code, bad_key, v_local, v_db))
                    
        for db_code in db_dicts[table].keys():
            if db_code not in local_codes:
                missing_in_tsv.append((table, db_code))

    # Print Report
    if missing_in_db:
        print(f"⚠️  THIẾU TRÊN SUPABASE ({len(missing_in_db)}):")
        for t, c in missing_in_db:
            print(f"   - {t}: {c}")
        print()
        
    if missing_in_tsv:
        print(f"⚠️  THIẾU TRONG TSV LOCAL / THỪA TRÊN DB ({len(missing_in_tsv)}):")
        for t, c in missing_in_tsv:
            print(f"   - {t}: {c}")
        print()
        
    if mismatches:
        print(f"⚠️  LỆCH THÔNG TIN ({len(mismatches)}):")
        for t, c, k, v_l, v_db in mismatches:
            print(f"   - {t}/{c} lệch '{k}':")
            print(f"     + Local TSV: {v_l}")
            print(f"     + Supabase : {v_db}")
        print()
        
    if not missing_in_db and not missing_in_tsv and not mismatches:
        print("✅ ĐỒNG BỘ HOÀN TOÀN! Không có sự chênh lệch nào.")
    
    # 4. Sync Down
    if args.sync_down:
        if not missing_in_tsv and not mismatches and not missing_in_db:
            print("\n✅ Không có gì để sync-down.")
            sys.exit(0)
            
        print("\n===========================================")
        print("⚠️ CHUẨN BỊ GHI ĐÈ FILE TSV (SYNC-DOWN)")
        print("===========================================")
        confirm = input("Bạn có chắc chắn muốn cập nhật file local TSV bằng dữ liệu từ Supabase? (y/N): ")
        if confirm.lower() != 'y':
            print("Đã hủy quá trình sync-down.")
            sys.exit(0)
            
        print("Đang tiến hành ghi đè file TSV...")
        
        # Đọc lại nguyên file để bảo tồn các header và khoảng trắng
        with open(tsv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        out_lines = []
        current_level = None
        headers = []
        processed_codes_in_level = set()
        
        def append_missing_db_rows_for_level(level_name, current_headers, out_buf, processed):
            if not level_name or not current_headers: return
            for code, db_row in db_dicts[level_name].items():
                if code not in processed:
                    row_vals = []
                    for h in current_headers:
                        v = db_row.get(h, "")
                        if isinstance(v, list):
                            v = ",".join([str(x) for x in v if str(x)])
                        row_vals.append(str(v).replace("\\n", " "))
                    out_buf.append("\t".join(row_vals) + "\n")
        
        for line in lines:
            s = line.strip()
            
            # Đổi bảng
            hit = next((k for k in SECTIONS if s.startswith(k)), None)
            if hit:
                # Flush the missing db rows for previous table before switching
                if current_level and headers:
                    append_missing_db_rows_for_level(current_level, headers, out_lines, processed_codes_in_level)
                    
                current_level = SECTIONS[hit]
                headers = []
                processed_codes_in_level = set()
                out_lines.append(line)
                continue
                
            if not current_level or s.startswith(SKIP_PREFIXES) or not s:
                out_lines.append(line)
                continue
                
            parts = line.rstrip("\n").split("\t")
            if parts[0] == "code":
                headers = [h.strip() for h in parts]
                out_lines.append(line)
                continue
                
            if headers and parts[0].strip():
                code = parts[0].strip()
                if code in db_dicts[current_level]:
                    # Build row from DB
                    db_row = db_dicts[current_level][code]
                    row_vals = []
                    for h in headers:
                        v = db_row.get(h, "")
                        if isinstance(v, list):
                            v = ",".join([str(x) for x in v if str(x)])
                        row_vals.append(str(v).replace("\\n", " "))
                    out_lines.append("\t".join(row_vals) + "\n")
                    processed_codes_in_level.add(code)
                else:
                    # In TSV but not in DB -> we drop it (or keep it?)
                    # Since we are syncing DOWN from truth (DB), we drop it.
                    # We simply do NOT append it to out_lines.
                    print(f"🗑️ Đã xóa '{code}' khỏi TSV vì không tồn tại trên Supabase.")
            else:
                out_lines.append(line)
                
        # Flush last table
        if current_level and headers:
            append_missing_db_rows_for_level(current_level, headers, out_lines, processed_codes_in_level)
            
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.writelines(out_lines)
            
        print("✅ Đã cập nhật xong Master TSV!")

if __name__ == "__main__":
    main()
