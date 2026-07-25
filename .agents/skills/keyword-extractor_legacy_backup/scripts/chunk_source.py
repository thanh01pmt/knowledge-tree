#!/usr/bin/env python3
"""
chunk_source.py — Bước 1: Cắt tài liệu nguồn theo ranh giới ngữ nghĩa.

Hỗ trợ: PDF (pdfplumber), Markdown (.md), Plain Text (.txt)
Output: .work/kw/chunks.json — mảng {chunk_id, heading_trail, text, char_start, char_end}

Logic:
- PDF: tách theo trang, sau đó detect heading bằng heuristic (ALL_CAPS dòng ngắn / kích cỡ font)
- Markdown: tách theo heading boundaries (# / ## / ###)
- Plain text: tách theo blank-line paragraphs
- Overlap: 20% giữa các chunk liền kề (tránh bỏ sót term vắt qua ranh giới)
- Gắn heading_trail vào metadata từng chunk để LLM ở bước sau có ngữ cảnh đủ
"""

import argparse
import json
import os
import re
import sys
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


# ─── PDF chunking ─────────────────────────────────────────────────────────────

def _is_heading_line(line: str) -> bool:
    """Heuristic: dòng ngắn (<= 80 ký tự), không kết thúc bằng dấu câu thông thường."""
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False
    if stripped[-1] in ".,:;!?":
        return False
    # Ưu tiên dòng có vẻ là title (nhiều chữ hoa hoặc chỉ 1-8 từ)
    words = stripped.split()
    if len(words) <= 8:
        return True
    return False


def chunk_pdf(pdf_path: Path, overlap_ratio: float = 0.2) -> list[dict]:
    try:
        import pdfplumber
    except ImportError:
        print("[ERROR] pdfplumber chưa cài. Chạy: pip install pdfplumber", file=sys.stderr)
        sys.exit(1)

    chunks = []
    heading_trail: list[str] = []
    current_lines: list[str] = []
    chunk_id = 0

    def flush_chunk(trail: list[str], lines: list[str], cid: int) -> dict:
        return {
            "chunk_id": f"chunk_{cid:04d}",
            "heading_trail": " > ".join(trail) if trail else "(no heading)",
            "text": "\n".join(lines).strip(),
        }

    with pdfplumber.open(pdf_path) as pdf:
        all_lines: list[str] = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            all_lines.extend(text.split("\n"))

    # Tính overlap window size (số dòng)
    window: list[str] = []

    for raw_line in all_lines:
        line = raw_line.rstrip()
        if not line:
            continue

        if _is_heading_line(line) and len(current_lines) > 3:
            # Flush chunk hiện tại
            if current_lines:
                chunks.append(flush_chunk(heading_trail, current_lines, chunk_id))
                chunk_id += 1
                # Overlap: giữ lại 20% dòng cuối của chunk trước
                overlap_n = max(1, int(len(current_lines) * overlap_ratio))
                current_lines = current_lines[-overlap_n:]

            # Update heading trail (depth 3 max)
            heading_trail = heading_trail[:2] + [line.strip()]
            current_lines.append(line)
        else:
            current_lines.append(line)

    # Flush chunk cuối
    if current_lines:
        chunks.append(flush_chunk(heading_trail, current_lines, chunk_id))

    return [c for c in chunks if len(c["text"]) > 20]


# ─── Markdown chunking ────────────────────────────────────────────────────────

def chunk_markdown(md_path: Path, overlap_ratio: float = 0.2) -> list[dict]:
    text = md_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    chunks = []
    heading_trail: list[str] = []
    current_lines: list[str] = []
    chunk_id = 0

    heading_re = re.compile(r"^(#{1,3})\s+(.+)")

    def flush(trail, cur_lines, cid):
        return {
            "chunk_id": f"chunk_{cid:04d}",
            "heading_trail": " > ".join(trail) if trail else "(no heading)",
            "text": "\n".join(cur_lines).strip(),
        }

    for line in lines:
        m = heading_re.match(line)
        if m and len(current_lines) > 2:
            if current_lines:
                chunks.append(flush(heading_trail, current_lines, chunk_id))
                chunk_id += 1
                overlap_n = max(1, int(len(current_lines) * overlap_ratio))
                current_lines = current_lines[-overlap_n:]

            depth = len(m.group(1))
            title = m.group(2).strip()
            if depth == 1:
                heading_trail = [title]
            elif depth == 2:
                heading_trail = heading_trail[:1] + [title]
            else:
                heading_trail = heading_trail[:2] + [title]
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        chunks.append(flush(heading_trail, current_lines, chunk_id))

    return [c for c in chunks if len(c["text"].strip()) > 20]


# ─── Plain text chunking ──────────────────────────────────────────────────────

def chunk_plaintext(txt_path: Path, max_chars: int = 1200, overlap_ratio: float = 0.2) -> list[dict]:
    text = txt_path.read_text(encoding="utf-8")
    # Tách theo đoạn văn (blank line)
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    chunk_id = 0
    current: list[str] = []
    current_len = 0

    def flush(paras, cid):
        body = "\n\n".join(paras)
        return {
            "chunk_id": f"chunk_{cid:04d}",
            "heading_trail": "(plain text)",
            "text": body,
        }

    for para in paragraphs:
        if current_len + len(para) > max_chars and current:
            chunks.append(flush(current, chunk_id))
            chunk_id += 1
            overlap_n = max(1, int(len(current) * overlap_ratio))
            current = current[-overlap_n:]
            current_len = sum(len(p) for p in current)

        current.append(para)
        current_len += len(para)

    if current:
        chunks.append(flush(current, chunk_id))

    return chunks


# ─── Main ─────────────────────────────────────────────────────────────────────

def chunk_source(source_path: Path, target_context: str, work_dir: Path) -> list[dict]:
    suffix = source_path.suffix.lower()

    if suffix == ".pdf":
        chunks = chunk_pdf(source_path)
    elif suffix == ".md":
        chunks = chunk_markdown(source_path)
    elif suffix in (".txt", ".text"):
        chunks = chunk_plaintext(source_path)
    else:
        print(f"[WARN] Định dạng không nhận ra: {suffix}. Thử đọc như plain text.")
        chunks = chunk_plaintext(source_path)

    # Thêm metadata chung
    for c in chunks:
        c["source_file"] = source_path.name
        c["target_context"] = target_context

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Chunk source file for ATE pipeline")
    parser.add_argument("--source", required=True, help="Path đến file nguồn (PDF/MD/TXT) hoặc thư mục")
    parser.add_argument("--target-context", required=True, help="Mô tả chủ đề mục tiêu")
    parser.add_argument("--project", help="Project slug (để tìm .work/kw/ tự động)")
    parser.add_argument("--work-dir", help="Override thư mục .work/kw/")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).parent)

    # Resolve work_dir
    if args.work_dir:
        work_dir = Path(args.work_dir)
    elif args.project:
        work_dir = repo_root / "projects" / args.project / ".work" / "kw"
    else:
        # Tìm active project từ status.yaml
        status_file = repo_root / "status.yaml"
        active_project = ""
        if status_file.is_file():
            for line in status_file.read_text().splitlines():
                if line.startswith("active_project"):
                    active_project = line.split(":", 1)[1].strip().strip("'\"")
        if active_project:
            work_dir = repo_root / "projects" / active_project / ".work" / "kw"
        else:
            work_dir = repo_root / ".work" / "kw"

    work_dir.mkdir(parents=True, exist_ok=True)

    source_path = Path(args.source)
    all_chunks: list[dict] = []

    if source_path.is_dir():
        # Xử lý tất cả file trong thư mục
        supported = [".pdf", ".md", ".txt", ".text"]
        files = [f for f in sorted(source_path.iterdir()) if f.suffix.lower() in supported]
        if not files:
            print(f"[WARN] Không tìm thấy file hỗ trợ trong: {source_path}")
        for f in files:
            print(f"[*] Chunking {f.name} ...")
            chunks = chunk_source(f, args.target_context, work_dir)
            # Re-number để tránh trùng chunk_id giữa các file
            offset = len(all_chunks)
            for c in chunks:
                num = int(c["chunk_id"].split("_")[1]) + offset
                c["chunk_id"] = f"chunk_{num:04d}"
            all_chunks.extend(chunks)
    elif source_path.is_file():
        print(f"[*] Chunking {source_path.name} ...")
        all_chunks = chunk_source(source_path, args.target_context, work_dir)
    else:
        print(f"[ERROR] Không tìm thấy: {source_path}", file=sys.stderr)
        sys.exit(1)

    # Ghi output
    out_path = work_dir / "chunks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    # Ghi target_context config để các script sau dùng lại
    config = {"target_context": args.target_context, "source": str(source_path)}
    with open(work_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(all_chunks)} chunks → {out_path}")


if __name__ == "__main__":
    main()
