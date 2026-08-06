#!/usr/bin/env python3
"""
STEP 8.6: Generate instruction markdown from resolved SIOs + code snippets.

Reads:
- resolved_sios.json (from STEP 5)
- code_snippets.json (from STEP 8.5)
- prerequisites.json (from STEP 4.5, optional)
- matched_cios.json (from STEP 4, optional — for CIO descriptions)

Outputs:
- instruction/ directory with one markdown file per concept milestone.

Each instruction file follows the 8-section structure:
  1. Overview & pedagogical goals
  2. File/directory setup
  3. Code execution (with real snippets from repo)
  4. Error handling
  5. Test scripts
  6. Common errors & debugging (phase-specific)
  7. Atomic task checklist
  8. Definition of done
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_sios_by_concept(resolved_sios: dict) -> Dict[str, List[dict]]:
    """Group SIOs by concept code."""
    by_concept = {}
    for group in resolved_sios.get('resolved_sios', []):
        concept = group.get('concept_code', '')
        action = group.get('action', 'UNKNOWN')
        sio_list = group.get('sios', [])
        if not sio_list and group.get('source_sio'):
            sio_list = [group['source_sio']]
        for sio in sio_list:
            entry = {
                'code': sio.get('code', ''),
                'name': sio.get('name', ''),
                'description': sio.get('description', ''),
                'action': action,
                'source_tech': group.get('source_tech', ''),
                'target_tech': group.get('target_tech', ''),
            }
            by_concept.setdefault(concept, []).append(entry)
    return by_concept


def collect_snippets_by_sio(code_snippets: dict) -> Dict[str, List[dict]]:
    """Map SIO code -> list of matched snippets."""
    return code_snippets.get('matched_snippets', {})


def collect_prereqs_by_sio(prerequisites: dict) -> Dict[str, List[str]]:
    """Map SIO code -> list of prerequisite LO codes."""
    prereqs = {}
    for edge in prerequisites.get('prerequisites', []):
        target = edge.get('learning_objective_code', '')
        prereq = edge.get('prerequisite_lo_code', '')
        if target:
            prereqs.setdefault(target, []).append(prereq)
    return prereqs


def render_section_3_code(snippets: List[dict]) -> str:
    """Render code execution section with real snippets."""
    if not snippets:
        return (
            "> ⚠️ Không có code snippet thực từ repository cho SIO này. "
            "Tham khảo tài liệu chính thức của framework/API tương ứng.\n"
        )

    lines = []
    for i, snip in enumerate(snippets[:3], 1):
        lines.append(f"**Snippet {i}** — `{snip.get('name', '')}` "
                     f"({snip.get('type', '')}, {snip.get('file', '')}):")
        lines.append("```")
        lines.append(snip.get('code', ''))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def render_section_6_debug(sio: dict) -> str:
    """Render phase-specific debug table based on SIO name/description."""
    text = (sio.get('name', '') + ' ' + sio.get('description', '')).lower()

    # Heuristic: pick relevant error categories from SIO content
    rows = []
    if any(k in text for k in ['state', 'binding', 'observable', 'publish']):
        rows.append(("State không cập nhật UI",
                     "Mutation state trên background thread / thiếu @MainActor",
                     "Dispatch về main thread hoặc dùng @MainActor"))
    if any(k in text for k in ['network', 'socket', 'connect', 'fetch', 'request']):
        rows.append(("Network timeout / connection lost",
                     "Thiếu retry/backoff, timeout quá ngắn",
                     "Thêm exponential backoff + timeout handling"))
    if any(k in text for k in ['data', 'decode', 'parse', 'json', 'serialize']):
        rows.append(("Decode/parse lỗi",
                     "Schema mismatch giữa client và server",
                     "Kiểm tra Codable/JSON schema, thêm error mapping"))
    if any(k in text for k in ['memory', 'leak', 'retain', 'closure', 'weak']):
        rows.append(("Retain cycle / memory leak",
                     "Closure capture strong self",
                     "Dùng [weak self] trong capture list"))
    if any(k in text for k in ['async', 'await', 'concurrent', 'task']):
        rows.append(("Race condition / data race",
                     "Shared mutable state truy cập đồng thời",
                     "Dùng actor / serial queue / lock"))
    if not rows:
        rows.append(("Compile error",
                     "Type mismatch / unresolved identifier",
                     "Đọc compiler message, fix type annotation"))

    lines = ["| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |",
             "| :--- | :--- | :--- |"]
    for err, cause, fix in rows:
        lines.append(f"| {err} | {cause} | {fix} |")
    return "\n".join(lines)


def render_instruction(concept: str, sios: List[dict],
                       snippets_by_sio: Dict[str, List[dict]],
                       prereqs_by_sio: Dict[str, List[str]],
                       target_tech: str) -> str:
    """Render a full instruction markdown for one concept milestone."""
    lines = []
    lines.append(f"# 📖 INSTRUCTION: {concept}")
    lines.append("")
    lines.append(f"> **Target Tech:** `{target_tech}` | **Concept:** `{concept}`")
    lines.append("")

    # 1. Overview
    lines.append("## 🎯 1. TỔNG QUAN & MỤC TIÊU SƯ PHẠM")
    lines.append(f"- **Concept:** `{concept}` — {len(sios)} SIO(s) cần thực hiện")
    lines.append("- **Mức độ nhận thức:** ULO (hiểu) → CIO (thiết kế) → SIO (viết code + pass tests)")
    lines.append("")

    # 2. Setup
    lines.append("## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC")
    lines.append(f"- Tạo module/file cho concept `{concept}` theo cấu trúc dự án hiện tại.")
    lines.append("")

    # 3. Code execution
    lines.append("## 💻 3. THỰC THI MÃ NGUỒN")
    for sio in sios:
        lines.append(f"### {sio['code']} — {sio['name']}")
        if sio.get('action') == 'ADAPT':
            lines.append(f"> 🔄 ADAPT từ `{sio.get('source_tech')}` → `{sio.get('target_tech')}`: "
                         f"giữ cấu trúc, thay tech-specific tokens.")
        lines.append(f"**Mô tả:** {sio.get('description', '')}")
        lines.append("")
        snippets = snippets_by_sio.get(sio['code'], [])
        lines.append(render_section_3_code(snippets))
        lines.append("")

    # 4. Error handling
    lines.append("## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ")
    lines.append("- Luôn bọc I/O trong error handling (do-catch / Result type / try-catch).")
    lines.append("- Xử lý edge cases: dữ liệu rỗng, null/nil, timeout, mất kết nối.")
    lines.append("")

    # 5. Tests
    lines.append("## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG")
    lines.append(f"- Viết unit test cho từng SIO của concept `{concept}`.")
    lines.append("- Test happy path + error path + edge cases.")
    lines.append("")

    # 6. Debug table (phase-specific)
    lines.append("## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG")
    for sio in sios:
        lines.append(f"**{sio['code']}:**")
        lines.append(render_section_6_debug(sio))
        lines.append("")

    # 7. Atomic tasks
    lines.append("## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ")
    for i, sio in enumerate(sios, 1):
        prereqs = prereqs_by_sio.get(sio['code'], [])
        prereq_str = f" (prereq: {', '.join(prereqs)})" if prereqs else ""
        lines.append(f"- [ ] **TASK_{i}** — `{sio['code']}`: {sio['name']}{prereq_str}")
    lines.append("")

    # 8. DoD
    lines.append("## 🏁 8. DEFINITION OF DONE")
    lines.append("- [ ] Code module hoạt động hoàn chỉnh.")
    lines.append("- [ ] Unit tests pass.")
    lines.append("- [ ] Git commit với message rõ ràng.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='STEP 8.6: Generate instruction markdown')
    parser.add_argument('--resolved-sios', type=Path, required=True,
                       help='Path to resolved_sios.json from STEP 5')
    parser.add_argument('--code-snippets', type=Path, required=True,
                       help='Path to code_snippets.json from STEP 8.5')
    parser.add_argument('--prerequisites', type=Path,
                       help='Path to prerequisites.json from STEP 4.5 (optional)')
    parser.add_argument('--jit-los', type=Path,
                       help='Path to jit_los.json from STEP 5.5 (optional)')
    parser.add_argument('--target-tech', type=str, default='SWIFT',
                       help='Target tech stack')
    parser.add_argument('--output-dir', type=Path, required=True,
                       help='Output directory for instruction files')
    args = parser.parse_args()

    resolved_sios = load_json(args.resolved_sios)
    code_snippets = load_json(args.code_snippets)

    prereqs_by_sio = {}
    if args.prerequisites and args.prerequisites.exists():
        prereqs_by_sio = collect_prereqs_by_sio(load_json(args.prerequisites))

    by_concept = collect_sios_by_concept(resolved_sios)
    snippets_by_sio = collect_snippets_by_sio(code_snippets)

    # Merge JIT-generated SIOs (STEP 5.5) into by_concept
    if args.jit_los and args.jit_los.exists():
        jit_data = load_json(args.jit_los)
        for lo in jit_data.get('generated', []):
            if lo.get('lo_type') != 'SPECIFIC_IMPL':
                continue
            concept = (lo.get('concept_codes') or [''])[0]
            if not concept:
                continue
            by_concept.setdefault(concept, []).append({
                'code': lo.get('code', ''),
                'name': lo.get('name', ''),
                'description': lo.get('description', ''),
                'action': 'JIT_GENERATED',
                'source_tech': '',
                'target_tech': args.target_tech,
            })
        print(f"[*] Merged JIT SIOs into instruction generation")

    print(f"[*] Found {len(by_concept)} concepts with SIOs")

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    total_files = 0
    for concept, sios in sorted(by_concept.items()):
        md = render_instruction(
            concept, sios, snippets_by_sio, prereqs_by_sio, args.target_tech
        )
        # Sanitize filename
        safe = concept.lower().replace(' ', '_')
        file_path = out_dir / f"instruction-{safe}.md"
        file_path.write_text(md, encoding='utf-8')
        total_files += 1
        print(f"  ✓ {file_path.name} ({len(sios)} SIOs)")

    print(f"\n[SUCCESS] Generated {total_files} instruction files in {out_dir}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
