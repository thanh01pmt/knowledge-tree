#!/usr/bin/env python3
"""
extract_document_hierarchy.py — Extract hierarchical structure from any source document.

Source-type agnostic: handles PDF, MD, TXT, DOCX.
Output: structured_hints.json — a hierarchy tree with each node classified
to a Master Tree level (Field/Subject/Category/Topic/Concept) by LLM.

Usage:
  python3 extract_document_hierarchy.py --project <slug>
  python3 extract_document_hierarchy.py --source <path> --output <path>

Integration:
  Runs after /context-audit, before /map-taxonomy.
  Agent reads structured_hints.json as primary mapping signal.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional


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


# ─── Source Type Detection ────────────────────────────────────────────────────

def detect_source_type(path: Path) -> str:
    """Detect source type by extension and content inspection."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return "pdf"
    elif ext == ".md":
        return "markdown"
    elif ext == ".txt":
        return "text"
    elif ext == ".docx":
        return "docx"
    # Fallback: try to read first few bytes
    try:
        head = path.read_bytes()[:100]
        if head.startswith(b"%PDF"):
            return "pdf"
        if b"PK" in head[:4]:  # DOCX is ZIP-based
            return "docx"
    except Exception:
        pass
    return "text"


# ─── Heading Extraction ──────────────────────────────────────────────────────

class DocNode:
    """A node in the document hierarchy tree."""
    def __init__(self, level: int, text: str, source_ref: str = ""):
        self.level = level          # 0=root, 1=H1, 2=H2, 3=H3, ...
        self.text = text.strip()
        self.source_ref = source_ref  # e.g. "page 5, Section 2.1"
        self.children: list["DocNode"] = []
        self.content: list[str] = []  # paragraph text under this heading

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "text": self.text,
            "source_ref": self.source_ref,
            "content": self.content[:3],  # first 3 paragraphs as context
            "children": [c.to_dict() for c in self.children],
        }


def extract_headings_from_markdown(text: str) -> list[DocNode]:
    """Parse markdown headings (##, ###, etc.) into a tree."""
    lines = text.splitlines()
    root = DocNode(0, "(root)")
    stack = [root]
    
    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            text_content = heading_match.group(2).strip()
            node = DocNode(level, text_content)
            # Find parent in stack
            while stack and stack[-1].level >= level:
                stack.pop()
            if stack:
                stack[-1].children.append(node)
            stack.append(node)
        elif stack and stack[-1].level > 0:
            # Accumulate content under current heading
            stripped = line.strip()
            if stripped and not stripped.startswith("```"):
                stack[-1].content.append(stripped[:200])
    
    return root.children


def extract_headings_from_text(text: str) -> list[DocNode]:
    """Parse plain text using section numbering (1., 1.1, 1.1.1) or blank-line grouping."""
    lines = text.splitlines()
    root = DocNode(0, "(root)")
    stack = [root]
    
    # Pattern: "1. Title" or "1.1 Title" or "1.1.1 Title"
    num_pattern = re.compile(r"^(\d+(?:\.\d+)*)[.\s]+(.+)$")
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        num_match = num_pattern.match(stripped)
        if num_match:
            numbering = num_match.group(1)
            level = len(numbering.split("."))
            text_content = num_match.group(2).strip()
            node = DocNode(level, text_content, f"Section {numbering}")
            while stack and stack[-1].level >= level:
                stack.pop()
            if stack:
                stack[-1].children.append(node)
            stack.append(node)
        elif stack and stack[-1].level > 0:
            stack[-1].content.append(stripped[:200])
    
    return root.children


def extract_headings_from_pdf(path: Path) -> list[DocNode]:
    """Extract headings from PDF using pdfplumber font size detection."""
    try:
        import pdfplumber
    except ImportError:
        print("[WARN] pdfplumber not installed. Falling back to text extraction.", file=sys.stderr)
        return extract_headings_from_text(path.read_text(encoding="utf-8", errors="replace"))
    
    root = DocNode(0, "(root)")
    stack = [root]
    
    with pdfplumber.open(path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            lines = text.splitlines()
            
            # Try to detect headings by font size (pdfplumber chars)
            try:
                chars = page.chars
                # Group chars by y-position (same line)
                lines_with_size: list[tuple[float, str]] = []
                if chars:
                    y_positions = sorted(set(c["top"] for c in chars))
                    for y in y_positions:
                        line_chars = [c for c in chars if abs(c["top"] - y) < 3]
                        if line_chars:
                            avg_size = sum(c.get("size", 10) for c in line_chars) / len(line_chars)
                            line_text = "".join(c["text"] for c in line_chars).strip()
                            if line_text:
                                lines_with_size.append((avg_size, line_text))
                
                # Find the most common font size (body text)
                if lines_with_size:
                    sizes = [s for s, _ in lines_with_size]
                    from collections import Counter
                    body_size = Counter(sizes).most_common(1)[0][0]
                    
                    for size, line_text in lines_with_size:
                        if size > body_size * 1.15 and len(line_text) < 100:
                            # This is likely a heading
                            level = 1
                            if size > body_size * 1.4:
                                level = 1
                            elif size > body_size * 1.25:
                                level = 2
                            else:
                                level = 3
                            node = DocNode(level, line_text, f"p.{page_num}")
                            while stack and stack[-1].level >= level:
                                stack.pop()
                            if stack:
                                stack[-1].children.append(node)
                            stack.append(node)
                        elif stack and stack[-1].level > 0:
                            stack[-1].content.append(line_text[:200])
            except Exception:
                # Fallback: use text-based heading detection
                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    # Heuristic: short, bold-like lines are headings
                    if len(stripped) < 80 and stripped.isupper() and not stripped.endswith("."):
                        node = DocNode(2, stripped, f"p.{page_num}")
                        while stack and stack[-1].level >= 2:
                            stack.pop()
                        if stack:
                            stack[-1].children.append(node)
                        stack.append(node)
                    elif stack and stack[-1].level > 0:
                        stack[-1].content.append(stripped[:200])
    
    return root.children


def extract_headings(path: Path) -> list[DocNode]:
    """Extract heading tree from any source document."""
    source_type = detect_source_type(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    
    if source_type == "pdf":
        return extract_headings_from_pdf(path)
    elif source_type == "markdown":
        return extract_headings_from_markdown(text)
    elif source_type == "text":
        # Try markdown first, fallback to numbered sections
        headings = extract_headings_from_markdown(text)
        if not headings:
            headings = extract_headings_from_text(text)
        return headings
    else:
        return extract_headings_from_text(text)


# ─── LLM Classification ──────────────────────────────────────────────────────

CLASSIFY_SYSTEM = """Bạn là Chuyên gia Phân loại Taxonomy cho Knowledge Tree.

Nhiệm vụ: Với mỗi heading trong tài liệu nguồn, xác định nó tương ứng với tầng nào 
trong Knowledge Tree.

Các tầng:
- **Field**: Lĩnh vực rộng nhất (VD: "Computer Science", "Data Science", "Business")
- **Subject**: Chuyên ngành chính (VD: "Programming", "Networks", "Databases")
- **Category**: Nhóm chủ đề liên quan (VD: "Control Flow", "Data Structures", "UI Design")
- **Topic**: Kỹ năng cụ thể (VD: "Loops", "Arrays", "Functions")
- **Concept**: Đơn vị tri thức nguyên tử (VD: "Definite Iteration", "Array Traversal")

QUY TẮC:
1. Dựa vào NỘI DUNG, không dựa vào heading level (H1/H2/H3).
2. Một H2 về "Variables" có thể là Topic, trong khi H2 về "Computer Architecture" có thể là Subject.
3. Nếu không chắc chắn, chọn tầng thấp hơn (Topic > Category > Subject).
4. Trả về JSON array, mỗi phần tử có: text, assigned_level, confidence, reasoning.

Định dạng JSON trả về:
{
  "classifications": [
    {
      "text": "Variables and Constants",
      "assigned_level": "topic",
      "confidence": 0.9,
      "reasoning": "Mô tả kỹ năng cụ thể về khai báo và sử dụng biến"
    }
  ]
}"""


def classify_nodes_llm(nodes: list[DocNode], syllabus_text: str, client, model: str) -> list[dict]:
    """Classify each node to a Master Tree level using LLM."""
    # Flatten nodes for classification
    flat_nodes = []
    
    def flatten(nodes_list: list[DocNode], depth: int = 0):
        for node in nodes_list:
            context = " ".join(node.content[:2])[:150]
            flat_nodes.append({
                "text": node.text,
                "heading_level": node.level,
                "depth": depth,
                "context": context,
                "source_ref": node.source_ref,
            })
            flatten(node.children, depth + 1)
    
    flatten(nodes)
    
    if not flat_nodes:
        return []
    
    # Batch classify (up to 20 nodes per call to avoid token limits)
    batch_size = 20
    all_classifications = []
    
    for i in range(0, len(flat_nodes), batch_size):
        batch = flat_nodes[i:i+batch_size]
        nodes_text = "\n---\n".join(
            f"Heading: {n['text']}\nLevel: H{n['heading_level']}\nContext: {n['context']}"
            for n in batch
        )
        
        user_prompt = (
            f"Tài liệu nguồn (tóm tắt):\n{syllabus_text[:2000]}\n\n"
            f"Danh sách headings cần phân loại:\n{nodes_text}\n\n"
            "Với mỗi heading, xác định tầng Master Tree phù hợp (field/subject/category/topic/concept)."
        )
        
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": CLASSIFY_SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            result = json.loads(completion.choices[0].message.content)
            batch_classifications = result.get("classifications", [])
            all_classifications.extend(batch_classifications)
            print(f"  Classified batch {i+1}-{min(i+batch_size, len(flat_nodes))}: {len(batch_classifications)} nodes")
        except Exception as e:
            print(f"  [WARN] Classification batch {i} failed: {e}", file=sys.stderr)
    
    return all_classifications


def annotate_tree(nodes: list[DocNode], classifications: list[dict]) -> list[dict]:
    """Merge LLM classifications back into the tree structure."""
    class_map = {c["text"].strip().lower(): c for c in classifications}
    
    def annotate(nodes_list: list[DocNode]) -> list[dict]:
        result = []
        for node in nodes_list:
            key = node.text.lower()
            cls = class_map.get(key, {})
            result.append({
                "text": node.text,
                "source_ref": node.source_ref,
                "assigned_level": cls.get("assigned_level", "concept"),
                "confidence": cls.get("confidence", 0.5),
                "reasoning": cls.get("reasoning", ""),
                "children": annotate(node.children),
            })
        return result
    
    return annotate(nodes)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Extract document hierarchy for taxonomy mapping")
    parser.add_argument("--project", help="Project slug (reads from projects/<slug>/context/)")
    parser.add_argument("--source", help="Direct path to source document")
    parser.add_argument("--output", help="Output path for structured_hints.json")
    parser.add_argument("--model", default="deepseek-v4-flash:cloud", help="LLM model for classification")
    args = parser.parse_args()
    
    repo_root = find_repo_root(Path.cwd())
    load_env(repo_root)
    
    # Resolve source path
    source_path = None
    if args.source:
        source_path = Path(args.source)
    elif args.project:
        context_dir = repo_root / "projects" / args.project / "context"
        if context_dir.is_dir():
            # Find the most likely source document
            for ext in ["*.pdf", "*.md", "*.txt", "*.docx"]:
                files = sorted(context_dir.glob(ext))
                if files:
                    source_path = files[0]
                    break
            if not source_path:
                # Try .work/raw_pdf.txt
                raw = repo_root / "projects" / args.project / ".work" / "raw_pdf.txt"
                if raw.is_file():
                    source_path = raw
    else:
        print("[ERROR] --project or --source required", file=sys.stderr)
        sys.exit(1)
    
    if not source_path or not source_path.is_file():
        print(f"[ERROR] Source not found: {source_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"[*] Source: {source_path} ({detect_source_type(source_path)})")
    
    # Step 1: Extract heading tree
    print("[1] Extracting document hierarchy...")
    tree = extract_headings(source_path)
    print(f"    → {len(tree)} top-level sections")
    
    # Count total nodes
    def count_nodes(nodes):
        return sum(1 + count_nodes(n.children) for n in nodes)
    total_nodes = count_nodes(tree)
    print(f"    → {total_nodes} total nodes in tree")
    
    # Step 2: Classify by LLM
    print("[2] Classifying nodes to Master Tree levels...")
    syllabus_text = source_path.read_text(encoding="utf-8", errors="replace")[:5000]
    
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[WARN] OPENAI_API_KEY not set. Using heuristic classification.", file=sys.stderr)
        # Fallback: heuristic based on heading level
        classifications = []
        def heuristic_classify(nodes, depth=0):
            for node in nodes:
                level_map = {0: "field", 1: "subject", 2: "category", 3: "topic", 4: "concept"}
                assigned = level_map.get(min(depth, 4), "concept")
                classifications.append({
                    "text": node.text,
                    "assigned_level": assigned,
                    "confidence": 0.5,
                    "reasoning": "Heuristic fallback (no LLM)"
                })
                heuristic_classify(node.children, depth + 1)
        heuristic_classify(tree)
    else:
        from openai import OpenAI
        base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
        client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        classifications = classify_nodes_llm(tree, syllabus_text, client, args.model)
    
    # Step 3: Annotate tree
    print("[3] Annotating tree with classifications...")
    annotated = annotate_tree(tree, classifications)
    
    # Step 4: Write output
    output = {
        "source": str(source_path),
        "source_type": detect_source_type(source_path),
        "total_nodes": total_nodes,
        "hierarchy": annotated,
    }
    
    if args.output:
        out_path = Path(args.output)
    elif args.project:
        work_dir = repo_root / "projects" / args.project / ".work"
        out_path = work_dir / "structured_hints.json"
    else:
        out_path = Path("structured_hints.json")
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n[✓] Structured hints → {out_path}")
    
    # Summary
    level_counts = {}
    def count_levels(nodes):
        for node in nodes:
            lvl = node.get("assigned_level", "unknown")
            level_counts[lvl] = level_counts.get(lvl, 0) + 1
            count_levels(node.get("children", []))
    count_levels(annotated)
    print(f"\n    Level distribution:")
    for lvl in ["field", "subject", "category", "topic", "concept"]:
        if lvl in level_counts:
            print(f"      {lvl}: {level_counts[lvl]}")
    
    print(f"\n→ Agent /map-taxonomy: đọc {out_path} làm primary mapping signal")


if __name__ == "__main__":
    main()
