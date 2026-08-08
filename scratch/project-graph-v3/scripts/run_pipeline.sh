#!/usr/bin/env bash
# run_pipeline.sh — Chạy toàn bộ pipeline project-graph-v3 (Talky) và xuất viewer
# JSON thẳng tới apps/viewer/public/roadmaps/talky-swiftui.json — NƠI UI ĐỌC.
#
# Đảm bảo MỌI lần chạy sau đều hiện trên UI: bước cuối convert_to_viewer ghi
# đúng file mà RoadmapViewer.jsx fetch (`/roadmaps/talky-swiftui.json`).
#
# Usage:
#   bash run_pipeline.sh            # chạy full (LLM ~25 phút)
#   bash run_pipeline.sh --skip-jit # test cấu trúc nhanh (không sinh LO bằng LLM)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$SCRIPT_DIR/../output"

# Inputs (có thể override bằng env)
SCAN_DIR="${SCAN_DIR:-/tmp/pgv3-talky-scan}"
REPO_DIR="${REPO_DIR:-/private/tmp/repocand-Talky}"
SOURCE="${SOURCE:-$SCAN_DIR/swift_files.txt}"
GOAL="${GOAL:-Build a realtime chat app for iOS with SwiftUI and Firebase — users sign up/sign in, send realtime messages, edit profile, receive push notifications}"
TECH_STACK="${TECH_STACK:-Swift,SwiftUI,Firebase}"
EMBEDDINGS="$REPO_ROOT/.agents/skills/taxonomy-mapper/resources/master_tree_embeddings.json"
LO_PREREQ="$REPO_ROOT/projects/master-tree/output/lo_prerequisites.tsv"
# Viewer JSON — file UI fetch (RoadmapViewer.jsx: TOPIC_ROADMAPS = ['jit-bulb-v3','talky-swiftui'])
VIEWER_JSON="$REPO_ROOT/apps/viewer/public/roadmaps/talky-swiftui.json"

SKIP_JIT=""
if [[ "${1:-}" == "--skip-jit" ]]; then
  SKIP_JIT="--skip-jit"
fi

cd "$SCRIPT_DIR"

echo "=== STEP 0b: Tree Advisor ==="
python3 step0b_tree_advisor.py \
  --tree "$SCAN_DIR/project_structure.txt" \
  --goal "$GOAL" \
  --output "$OUT/talky-step0/file_types_profile.json"

echo "=== STEP 1: Project Graph LLM ==="
python3 step1_project_graph_llm.py \
  --source-file "$SOURCE" \
  --goal "$GOAL" \
  --tech-stack "$TECH_STACK" \
  --output "$OUT/project_graph_raw.json" \
  --profile full

echo "=== STEP 2: Verify (code) ==="
python3 step2_verify.py \
  --project-graph "$OUT/project_graph_raw.json" \
  --repo-dir "$REPO_DIR" \
  --output "$OUT/project_graph_verified.json"

echo "=== STEP 3: Standardize concepts ==="
python3 step3_standardize.py \
  --project-graph "$OUT/project_graph_verified.json" \
  --repo-dir "$REPO_DIR" \
  --embeddings "$EMBEDDINGS" \
  --output "$OUT/project_graph_standardized.json"

echo "=== STEP 3.5: Curriculum Graph ==="
python3 step35_curriculum.py \
  --project-graph "$OUT/project_graph_standardized.json" \
  --lo-prerequisites "$LO_PREREQ" \
  --output "$OUT/project_graph_curriculum.json"

echo "=== STEP 4: Roadmap ==="
python3 step4_roadmap.py \
  --project-graph "$OUT/project_graph_curriculum.json" \
  --output "$OUT/roadmap.json" \
  $SKIP_JIT

echo "=== Gate: validate_data (bắt buộc PASS) ==="
python3 validate_data.py \
  --project-graph "$OUT/project_graph_curriculum.json" \
  --roadmap "$OUT/roadmap.json"

echo "=== Convert → viewer: $VIEWER_JSON ==="
python3 convert_to_viewer.py \
  --roadmap "$OUT/roadmap.json" \
  --output "$VIEWER_JSON"

echo "[✓] Pipeline xong — UI đọc $VIEWER_JSON (mở viewer: cd apps/viewer && npm run dev)"
