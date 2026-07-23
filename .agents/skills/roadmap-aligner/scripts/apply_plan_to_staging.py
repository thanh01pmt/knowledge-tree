#!/usr/bin/env python3
"""
apply_plan_to_staging.py — Apply approved Knowledge Tree Plan using N:N Reusable Topology
to general-context/mlo-knowlege-tree.tsv (Staging working copy).

Cleanly maps 15 new concepts to EXISTING Categories/Topics using N:N relationships,
avoiding creation of redundant Categories or Topics!
"""

import sys
import json
import re
import shutil
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent

def find_project_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(20):
        if (cur / ".agents").is_dir():
            return cur
        if cur.parent == cur:
            break
    return start.resolve().parent.parent.parent.parent

PROJECT_ROOT = find_project_root(SCRIPT_DIR)
MASTER_TSV_PATH = PROJECT_ROOT / ".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv"
STAGING_TSV_PATH = PROJECT_ROOT / "general-context" / "mlo-knowlege-tree.tsv"
VERSION_HISTORY_PATH = PROJECT_ROOT / "general-context" / "version_history.json"
DEFAULT_PLAN_PATH = PROJECT_ROOT / ".work" / "frontend_knowledge_tree_plan.md"

def reset_staging_from_master():
    """Reset staging TSV directly from Master TSV to remove previous redundant nodes"""
    if MASTER_TSV_PATH.exists():
        STAGING_TSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MASTER_TSV_PATH, STAGING_TSV_PATH)
        print(f"🔄 Reset Staging TSV clean state from Master Tree at {STAGING_TSV_PATH}")

def parse_existing_tsv(tsv_path: Path):
    """Read lines of TSV and track existing codes per section"""
    lines = []
    existing_codes = {
        "fields": set(),
        "subjects": set(),
        "categories": set(),
        "topics": set(),
        "concepts": set()
    }
    section_indices = {}

    if not tsv_path.exists():
        reset_staging_from_master()

    current_section = None
    with open(tsv_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            lines.append(line)
            line_str = line.strip()
            if not line_str:
                continue

            if line_str.startswith("Bảng 1"):
                current_section = "fields"
                section_indices["fields"] = idx
                continue
            elif line_str.startswith("Bảng 2"):
                current_section = "subjects"
                section_indices["subjects"] = idx
                continue
            elif line_str.startswith("Bảng 3"):
                current_section = "categories"
                section_indices["categories"] = idx
                continue
            elif line_str.startswith("Bảng 4"):
                current_section = "topics"
                section_indices["topics"] = idx
                continue
            elif line_str.startswith("Bảng 5"):
                current_section = "concepts"
                section_indices["concepts"] = idx
                continue

            if line_str.startswith("Đây là") or line_str.startswith("Mỗi Field") or line_str.startswith("code\t"):
                continue

            parts = line.rstrip("\r\n").split("\t")
            code = parts[0].strip()
            if code and current_section:
                existing_codes[current_section].add(code)

    return lines, existing_codes, section_indices

def merge_nodes_to_staging(nodes_to_add: dict):
    # Reset staging to clean master state first
    reset_staging_from_master()
    lines, existing_codes, section_indices = parse_existing_tsv(STAGING_TSV_PATH)

    added_count = {"categories": 0, "topics": 0, "concepts": 0}
    updated_keyword_count = 0
    updated_parent_count = 0

    new_concept_lines = []

    # Update N:N Subject linkages on EXISTING Categories
    for cat_update in nodes_to_add.get("category_updates", []):
        c_code = cat_update["code"]
        sub_to_add = cat_update.get("subject_codes", "")
        if c_code in existing_codes["categories"]:
            for idx, line in enumerate(lines):
                if line.startswith(f"{c_code}\t"):
                    parts = line.rstrip("\r\n").split("\t")
                    while len(parts) < 7:
                        parts.append("")
                    existing_subs = set(s.strip() for s in parts[3].split(",") if s.strip())
                    new_subs = set(s.strip() for s in sub_to_add.split(",") if s.strip())
                    parts[3] = ", ".join(sorted(existing_subs.union(new_subs)))
                    lines[idx] = "\t".join(parts) + "\n"
                    updated_parent_count += 1
                    break

    # Process Concepts
    for conc in nodes_to_add.get("concepts", []):
        code = conc["code"]
        if code not in existing_codes["concepts"]:
            row_str = f"{code}\t{conc['name']}\t{conc.get('desc', '')}\t{conc.get('topic_code', 'APP_PROTOCOLS')}\t{conc.get('keywords', '')}\t\t{conc.get('metadata', '{\"icon\": \"code\"}')}\n"
            new_concept_lines.append(row_str)
            existing_codes["concepts"].add(code)
            added_count["concepts"] += 1
        else:
            kw_to_add = conc.get("keywords", "")
            topic_to_add = conc.get("topic_code", "")
            for idx, line in enumerate(lines):
                if line.startswith(f"{code}\t"):
                    parts = line.rstrip("\r\n").split("\t")
                    while len(parts) < 7:
                        parts.append("")
                    
                    if topic_to_add:
                        existing_parents = set(p.strip() for p in parts[3].split(",") if p.strip())
                        new_parents = set(p.strip() for p in topic_to_add.split(",") if p.strip())
                        parts[3] = ", ".join(sorted(existing_parents.union(new_parents)))

                    if kw_to_add:
                        existing_kws = set(k.strip() for k in parts[4].split(",") if k.strip())
                        new_kws = set(k.strip() for k in kw_to_add.split(",") if k.strip())
                        parts[4] = ", ".join(sorted(existing_kws.union(new_kws)))
                        updated_keyword_count += 1

                    lines[idx] = "\t".join(parts) + "\n"
                    break

    final_lines = list(lines)
    if new_concept_lines:
        final_lines.extend(new_concept_lines)

    STAGING_TSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STAGING_TSV_PATH, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print(f"✅ Successfully updated Staging Knowledge Tree TSV ({STAGING_TSV_PATH}) via N:N Reuse:")
    print(f"  - New Categories added: {added_count['categories']} (Lean & Clean!)")
    print(f"  - New Topics added: {added_count['topics']} (Lean & Clean!)")
    print(f"  - New Concepts added: {added_count['concepts']}")
    print(f"  - N:N Parent Category updates: {updated_parent_count}")
    print(f"  - Concept Keywords updated: {updated_keyword_count}")

    if VERSION_HISTORY_PATH.exists():
        with open(VERSION_HISTORY_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)

        cur_ver = history.get("current_version", "v2.2.0-staging.0")
        parts = cur_ver.split("-staging.")
        base_ver = parts[0]
        stg_num = int(parts[1]) + 1 if len(parts) > 1 else 1
        new_stg_ver = f"{base_ver}-staging.{stg_num}"

        history["current_version"] = new_stg_ver
        history["last_updated"] = datetime.now().isoformat()
        history["versions"].append({
            "version": new_stg_ver,
            "timestamp": datetime.now().isoformat(),
            "description": f"Applied N:N Reusable Topology: +{added_count['concepts']} concepts mapped to existing Master Categories/Topics"
        })

        with open(VERSION_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"🏷️ Staging version bumped to: {new_stg_ver}")

def main():
    # Clean N:N Package: Reuse existing Categories & Topics, insert only pure Concepts!
    clean_nn_package = {
        "category_updates": [
            {"code": "NETWORK_PROTOCOLS", "subject_codes": "NETWORKING, WEB_DEV"},
            {"code": "NETWORK_SECURITY", "subject_codes": "NETWORKING, WEB_DEV"},
            {"code": "TESTING_DEBUGGING", "subject_codes": "SW_LIFECYCLE, WEB_DEV"},
            {"code": "DEVELOPMENT_ENVIRONMENT", "subject_codes": "SW_LIFECYCLE, WEB_DEV"}
        ],
        "concepts": [
            {"code": "INTERNET_FUNDAMENTALS", "name": "Internet Architecture & Protocols", "desc": "Nguyên tắc hoạt động của Internet và mô hình Client-Server.", "topic_code": "APP_PROTOCOLS, NET_LAYERS", "keywords": "IP, packet routing, client-server"},
            {"code": "HTTP_PROTOCOL", "name": "HTTP Protocol & Specification", "desc": "Giao thức truyền tải siêu văn bản HTTP/1.1, HTTP/2, HTTP/3.", "topic_code": "APP_PROTOCOLS", "keywords": "headers, status codes, REST"},
            {"code": "DOMAIN_NAME_SYSTEM", "name": "Domain Name System (DNS)", "desc": "Hệ thống phân giải tên miền DNS.", "topic_code": "APP_PROTOCOLS", "keywords": "A record, CNAME, NS"},
            {"code": "WEB_HOSTING", "name": "Web Hosting & Infrastructure", "desc": "Hạ tầng lưu trữ và phân phối ứng dụng web.", "topic_code": "APP_PROTOCOLS, CLOUD_COMPUTING", "keywords": "CDN, static hosting, edge"},
            {"code": "WEB_BROWSER_ENGINES", "name": "Web Browser Architecture & Engines", "desc": "Kiến trúc trình duyệt web và cơ chế render.", "topic_code": "APP_PROTOCOLS, FRONTEND_DEV", "keywords": "DOM tree, CSSOM, reflow, repaint"},
            {"code": "UI_BOX_MODEL_LAYOUT", "name": "UI Box Model Layout System", "desc": "Mô hình bố cục khung khối UI trừu tượng (Margin, Border, Padding).", "topic_code": "LAYOUT_COMPOSITION, FRONTEND_DEV", "keywords": "box-sizing, margin, padding, border"},
            {"code": "FLEXBOX_GRID_LAYOUT", "name": "Flexible & Grid Layout Systems", "desc": "Hệ thống dàn trang linh hoạt và dạng lưới.", "topic_code": "LAYOUT_COMPOSITION, FRONTEND_DEV", "keywords": "flexbox, css grid, alignment"},
            {"code": "RESPONSIVE_DESIGN", "name": "Responsive Web Design Principles", "desc": "Nguyên lý thiết kế ứng dụng web đáp ứng đa màn hình.", "topic_code": "LAYOUT_COMPOSITION, GRAPHIC_DESIGN_PRINCIPLES", "keywords": "media queries, breakpoints, fluid"},
            {"code": "PACKAGE_MANAGEMENT", "name": "Package & Dependency Management", "desc": "Nguyên lý và công cụ quản lý thư viện phụ thuộc.", "topic_code": "DEVELOPMENT_ENVIRONMENT, VERSION_CONTROL", "keywords": "npm, yarn, pnpm, pip, conda, uv"},
            {"code": "MODULE_BUNDLERS", "name": "Module Bundlers & Build Tools", "desc": "Công cụ đóng gói module và biên dịch tài nguyên.", "topic_code": "DEVELOPMENT_ENVIRONMENT", "keywords": "Vite, Webpack, Rollup, Parcel, esbuild"},
            {"code": "CODE_LINTING_FORMATTING", "name": "Code Formatting & Static Analysis", "desc": "Công cụ linter và định dạng mã nguồn tự động.", "topic_code": "DEVELOPMENT_ENVIRONMENT, TROUBLESHOOTING_METHODOLOGY", "keywords": "ESLint, Prettier"},
            {"code": "VCS_HOSTING", "name": "Version Control Hosting Platforms", "desc": "Nền tảng lưu trữ và quản lý mã nguồn lưu vết.", "topic_code": "VERSION_CONTROL, DEVELOPMENT_ENVIRONMENT", "keywords": "GitHub, GitLab, Bitbucket"},
            {"code": "FRONTEND_FRAMEWORKS", "name": "UI Component Frameworks & Libraries", "desc": "Các framework và thư viện giao diện theo mô hình component.", "topic_code": "WEB_FRAMEWORKS, FRONTEND_DEV", "keywords": "React, Vue.js, Angular, Svelte, Solid JS"},
            {"code": "AUTOMATED_TESTING_TOOLS", "name": "Automated Testing Frameworks & Tools", "desc": "Khung kiểm thử tự động unit test và end-to-end.", "topic_code": "TESTING_DEBUGGING, ERROR_MESSAGES", "keywords": "Jest, Vitest, Cypress, Playwright"},
            {"code": "CROSS_ORIGIN_SECURITY", "name": "Cross-Origin Security & Policies", "desc": "Cơ chế bảo mật truy cập tài nguyên chia sẻ cross-origin.", "topic_code": "NETWORK_SECURITY, APP_PROTOCOLS", "keywords": "CORS, Same-Origin Policy"},
            {"code": "WEB_AUTHENTICATION_STRATEGIES", "name": "Web Authentication & Authorization", "desc": "Các chiến lược xác thực và phân quyền người dùng web.", "topic_code": "NETWORK_SECURITY, APP_PROTOCOLS", "keywords": "JWT, OAuth, Session Cookies, WebAuthn"}
        ]
    }

    merge_nodes_to_staging(clean_nn_package)

if __name__ == "__main__":
    main()
