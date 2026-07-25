#!/usr/bin/env python3
"""
export_keywords.py — Bước 6: Ghi output cuối + tích hợp vào /context-audit.

Input:  .work/kw/keywords_verified.json + config.json
Output: output/keywords.tsv
        output/keywords.json
        projects/<project>/context/keywords.tsv  ← copy để context-audit dùng
        (cập nhật .work/context-audit.md nếu tồn tại)

TSV columns: term, aliases, relevance_score, source_chunks, first_extraction_method
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
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


def load_work_dir(args, repo_root: Path) -> Path:
    if args.work_dir:
        return Path(args.work_dir)
    if args.project:
        return repo_root / "projects" / args.project / ".work" / "kw"
    status_file = repo_root / "status.yaml"
    if status_file.is_file():
        for line in status_file.read_text().splitlines():
            if line.startswith("active_project"):
                slug = line.split(":", 1)[1].strip().strip("'\"")
                if slug:
                    return repo_root / "projects" / slug / ".work" / "kw"
    return repo_root / ".work" / "kw"


def get_active_project(args, repo_root: Path) -> str:
    if args.project:
        return args.project
    status_file = repo_root / "status.yaml"
    if status_file.is_file():
        for line in status_file.read_text().splitlines():
            if line.startswith("active_project"):
                return line.split(":", 1)[1].strip().strip("'\"")
    return ""


def write_tsv(keywords: list[dict], out_path: Path) -> None:
    fieldnames = ["term", "aliases", "relevance_score", "source_chunks", "first_extraction_method", "category"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for kw in keywords:
            writer.writerow({
                "term": kw.get("term", ""),
                "aliases": "|".join(kw.get("aliases", [])),
                "relevance_score": kw.get("relevance_score", ""),
                "source_chunks": "|".join(kw.get("source_chunks", [])),
                "first_extraction_method": kw.get("first_extraction_method", ""),
                "category": kw.get("category", ""),
            })


def inject_into_context_audit(
    context_audit_path: Path,
    keywords: list[dict],
    target_context: str,
    keywords_tsv_path: Path,
) -> None:
    """Thêm section ## ATE Keywords vào context-audit.md."""
    if not context_audit_path.is_file():
        return

    existing = context_audit_path.read_text(encoding="utf-8")

    # Nếu đã có section ATE Keywords → replace
    ATE_MARKER = "## ATE Keywords"
    ate_section_lines = [
        "",
        ATE_MARKER,
        "",
        f"> Trích xuất bằng ATE Pipeline từ: `{target_context}`",
        f"> Thời điểm: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> File đầy đủ: `{keywords_tsv_path.name}` (xem `output/keywords.tsv`)",
        "",
        f"**Tổng cộng: {len(keywords)} thuật ngữ đã vét cạn và kiểm tra omission.**",
        "",
        "| Term | Aliases | Category | Method |",
        "|------|---------|----------|--------|",
    ]
    for kw in sorted(keywords, key=lambda x: x.get("relevance_score", 0), reverse=True)[:80]:
        aliases = ", ".join(kw.get("aliases", []))
        ate_section_lines.append(
            f"| {kw['term']} | {aliases} | {kw.get('category','?')} | {kw.get('first_extraction_method','?')} |"
        )
    if len(keywords) > 80:
        ate_section_lines.append(f"\n*... và {len(keywords) - 80} term khác (xem keywords.tsv)*")

    ate_section = "\n".join(ate_section_lines)

    if ATE_MARKER in existing:
        # Replace từ ATE_MARKER đến hết file (hoặc đến section header tiếp theo)
        idx = existing.index(ATE_MARKER)
        # Tìm heading tiếp theo sau ATE_MARKER
        next_heading_idx = existing.find("\n## ", idx + len(ATE_MARKER))
        if next_heading_idx != -1:
            new_content = existing[:idx] + ate_section + "\n" + existing[next_heading_idx:]
        else:
            new_content = existing[:idx] + ate_section
    else:
        new_content = existing.rstrip() + "\n\n" + ate_section

    context_audit_path.write_text(new_content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Export final keywords + integrate with context-audit")
    parser.add_argument("--project", help="Project slug")
    parser.add_argument("--work-dir", help="Override .work/kw/ path")
    parser.add_argument("--no-inject", action="store_true", help="Không inject vào context-audit.md")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)
    work_dir = load_work_dir(args, repo_root)
    project = get_active_project(args, repo_root)

    # Load verified keywords
    verified_path = work_dir / "keywords_verified.json"
    if not verified_path.is_file():
        print(f"[ERROR] Không tìm thấy keywords_verified.json: {verified_path}", file=sys.stderr)
        print("Hãy chạy llm_verify_and_dedup.py trước.", file=sys.stderr)
        sys.exit(1)
    with open(verified_path, encoding="utf-8") as f:
        keywords = json.load(f)

    # Load config
    config = {}
    config_path = work_dir / "config.json"
    if config_path.is_file():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    target_context = config.get("target_context", "")

    # Sort by relevance_score desc
    keywords.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    # Resolve output dir
    if project:
        out_dir = repo_root / "projects" / project / "output"
        context_dir = repo_root / "projects" / project / "context"
        work_project_dir = repo_root / "projects" / project / ".work"
    else:
        out_dir = repo_root / "output"
        context_dir = None
        work_project_dir = None

    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ghi output/keywords.tsv
    tsv_path = out_dir / "keywords.tsv"
    write_tsv(keywords, tsv_path)
    print(f"[✓] output/keywords.tsv → {tsv_path} ({len(keywords)} terms)")

    # 2. Ghi output/keywords.json
    json_path = out_dir / "keywords.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    print(f"[✓] output/keywords.json → {json_path}")

    # 3. Copy vào context/ để context-audit dùng
    if context_dir and not args.no_inject:
        context_dir.mkdir(parents=True, exist_ok=True)
        context_kw_path = context_dir / "keywords.tsv"
        write_tsv(keywords, context_kw_path)
        print(f"[✓] context/keywords.tsv → {context_kw_path}")

        # 4. Inject vào context-audit.md
        if work_project_dir:
            context_audit_md = work_project_dir / "context-audit.md"
            if context_audit_md.is_file():
                inject_into_context_audit(context_audit_md, keywords, target_context, tsv_path)
                print(f"[✓] Đã inject ATE Keywords section → {context_audit_md}")
            else:
                print(f"[INFO] context-audit.md chưa tồn tại ({context_audit_md}). "
                      "Sẽ inject khi /context-audit chạy lần sau.")

    print(f"\n[✓] Finalized! {len(keywords)} keywords export xong.")
    if not args.no_inject and context_dir:
        print(f"\n→ Bước tiếp theo: chạy /context-audit để tích hợp keywords vào domain breakdown.")
    else:
        print(f"\n→ Output sẵn sàng tại: {out_dir}")


if __name__ == "__main__":
    main()
