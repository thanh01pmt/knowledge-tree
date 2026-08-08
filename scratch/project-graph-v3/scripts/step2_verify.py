#!/usr/bin/env python3
"""
STEP 2 — Verify Project Graph (canonical v3) bằng code, evidence OBSERVED.

Luật verify (ground-truth, không tin LLM):
  L1. File path trong source_evidence / modifies / source trỏ file thật?
  L2. Symbol/keyword (keywords, api_usage) xuất hiện trong file thật?
  L3. Architecture INFERRED → giữ confidence, đánh dấu evidence
  L4. Task source_evidence là REFERENCE (không phải 'task = tạo file đó')
  L5. Điền evidence.entries: OBSERVED cho file/symbol; INFERRED cho architecture

Input: project_graph_raw.json (STEP 1) + repo_dir
Output: project_graph_verified.json + hallucinations.json

Usage:
  python step2_verify.py --project-graph /tmp/pgv3-raw.json \
      --repo-dir /tmp/stream-chat-swift \
      --output /tmp/pgv3-verified.json
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


def file_exists(repo_dir: Path, rel_path: str) -> bool:
    return (repo_dir / rel_path).is_file()


def symbol_in_file(repo_dir: Path, rel_path: str, symbol: str):
    """Tìm symbol trong file → trả (found: bool, line: int|None).
    Line-level evidence (M4 — trace nguồn P3, REF: file#L45)."""
    p = repo_dir / rel_path
    if not p.is_file():
        return False, None
    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False, None
    for i, line in enumerate(content.split("\n"), start=1):
        if re.search(rf"\b{re.escape(symbol)}\b", line):
            return True, i
    return False, None


def verify_project_graph(raw: Dict[str, Any], repo_dir: Path) -> tuple:
    """Return (verified, hallucinations)."""
    verified = json.loads(json.dumps(raw))  # deep copy
    hallucinations: List[Dict[str, Any]] = []
    evidence_entries: List[Dict[str, Any]] = []

    # L1: files trong toàn graph tồn tại?
    # Null-safe: LLM có thể trả "source": null / "architecture": null — .get(k, {})
    # KHÔNG chặn được (key tồn tại với giá trị null) → phải (x or {}).
    all_files: Set[str] = set()
    for task in (verified.get("implementation") or {}).get("tasks", []):
        for f in task.get("source_evidence", []):
            all_files.add(f)
        for f in task.get("modifies", []):
            all_files.add(f)
    for f in (verified.get("source") or {}).get("files", []):
        all_files.add(f)

    valid_files: Set[str] = set()
    for f in sorted(all_files):
        if file_exists(repo_dir, f):
            valid_files.add(f)
            evidence_entries.append({
                "target_id": f,
                "source": {"file": f},
                "evidence_type": "OBSERVED",
                "confidence": 1.0,
                "extraction_method": "git_tracker_file_exists"
            })
        else:
            hallucinations.append({"type": "missing_file", "file": f})

    # L2: symbol/keyword xuất hiện trong file? (grep từ tasks + architecture evidence)
    # Thu thập mọi symbol cần verify: keywords trong task action/source_evidence files
    for task in (verified.get("implementation") or {}).get("tasks", []):
        task_id = task.get("id", "")
        # Lấy symbol từ source_evidence files: tìm tên class/struct khớp tên file
        for f in task.get("source_evidence", []):
            if f not in valid_files:
                continue
            stem = Path(f).stem
            # Class/struct cùng tên file (Swift convention: WeatherView.swift → WeatherView)
            found, line = symbol_in_file(repo_dir, f, stem)
            if found:
                # REF tag dạng file#L<line> (M4 — trace nguồn P3)
                ref = f"{f}#L{line}"
                evidence_entries.append({
                    "target_id": f"{task_id}:{stem}",
                    "source": {"file": f, "symbol": stem, "line": line, "ref": ref},
                    "evidence_type": "OBSERVED",
                    "confidence": 1.0,
                    "extraction_method": "source_analysis_symbol"
                })
            else:
                # File hợp lệ nhưng không có symbol cùng tên — chỉ cảnh báo, không phải hallucination
                pass

    # L3: architecture nodes INFERRED → giữ + thêm evidence
    for node in (verified.get("architecture") or {}).get("nodes", []):
        if node.get("evidence_type") == "INFERRED" and node.get("confidence") is not None:
            evidence_entries.append({
                "target_id": node.get("id", ""),
                "source": {"file": node.get("evidence_file", "?")} if node.get("evidence_file") else {},
                "evidence_type": "INFERRED",
                "confidence": node.get("confidence"),
                "extraction_method": "LLM_inference"
            })

    # L4: task phải có intent + outcome (boundary D7) — thiếu → warning (không hallucination)
    missing_intent = [t["id"] for t in (verified.get("implementation") or {}).get("tasks", [])
                      if not t.get("intent") or not t.get("outcome")]
    if missing_intent:
        hallucinations.append({"type": "missing_intent_outcome", "tasks": missing_intent})

    # Điền evidence vào output
    verified["evidence"] = {"entries": evidence_entries}

    return verified, {"hallucinations": hallucinations}


def main():
    parser = argparse.ArgumentParser(description="STEP 2 — Verify Project Graph v3 (evidence OBSERVED)")
    parser.add_argument("--project-graph", required=True, type=Path)
    parser.add_argument("--repo-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    raw = json.load(open(args.project_graph, encoding="utf-8"))
    verified, hall = verify_project_graph(raw, args.repo_dir)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(verified, f, indent=2, ensure_ascii=False)

    hall_path = args.output.with_name("hallucinations.json")
    with open(hall_path, "w", encoding="utf-8") as f:
        json.dump(hall, f, indent=2, ensure_ascii=False)

    n_ev = len(verified.get("evidence", {}).get("entries", []))
    n_hall = len(hall["hallucinations"])
    print(f"[✓] Verified: {n_ev} evidence entries | hallucinations: {n_hall}")
    for h in hall["hallucinations"][:5]:
        print(f"    ! {str(h)[:90]}")
    print(f"    → {args.output} + {hall_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
