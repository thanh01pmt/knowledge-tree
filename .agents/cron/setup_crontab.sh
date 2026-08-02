#!/usr/bin/env bash
# setup_crontab.sh - Cài đặt các Cron Jobs tự động cho Knowledge Tree
# Chạy lệnh này để nạp lịch trình vào crontab của hệ thống macOS/Linux.
# Kiến trúc mới: 3 Cron (Auto-Heal, Collectors, Processor)

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$DIR")"
PYTHON_BIN="$(which python3)"

# Tạo thư mục logs nếu chưa có
mkdir -p "$REPO_ROOT/.agents/cron/logs"

# Xóa các cron cũ của Knowledge Tree (nếu có) để tránh trùng lặp
crontab -l | grep -v "knowledge-tree/.agents/cron" > /tmp/current_cron
echo "" >> /tmp/current_cron

# ============================================
# CRON 1: Auto-Heal (mỗi 6 tiếng)
# Quick validate Master Tree + LLM auto-fix T6/ref errors
# ============================================
echo "0 */6 * * * cd $REPO_ROOT && $PYTHON_BIN .agents/cron/cron_auto_heal.py >> .agents/cron/logs/cron_auto_heal.log 2>&1" >> /tmp/current_cron

# ============================================
# CRON 2: Collectors - Phase 1: Research & Context Collection
# Multi-schedule: Academic (15m), Standards (CN 3am), Trends (CN 2am)
# ============================================

# 2a. Academic Collector - mỗi 15 phút
echo "*/15 * * * * cd $REPO_ROOT && $PYTHON_BIN .agents/cron/collectors/run_collectors.py --source academic --schedule 15m >> .agents/cron/logs/cron_collectors_academic.log 2>&1" >> /tmp/current_cron

# 2b. Standards Collector - Chủ Nhật 3:00 sáng (crosswalk 5 frameworks)
echo "0 3 * * 0 cd $REPO_ROOT && $PYTHON_BIN .agents/cron/collectors/run_collectors.py --source standards --schedule weekly >> .agents/cron/logs/cron_collectors_standards.log 2>&1" >> /tmp/current_cron

# 2c. Trends Collector - Chủ Nhật 2:00 sáng (auto_stem_discovery)
echo "0 2 * * 0 cd $REPO_ROOT && $PYTHON_BIN .agents/cron/collectors/run_collectors.py --source trends --schedule weekly >> .agents/cron/logs/cron_collectors_trends.log 2>&1" >> /tmp/current_cron

# ============================================
# CRON 3: Processor - Phase 2: LLM Analysis & Pipeline Execution
# Mỗi 6 tiếng (sau khi collectors chạy) - quét pending items, chạy pipeline
# ============================================
echo "0 */6 * * * cd $REPO_ROOT && $PYTHON_BIN .agents/cron/collectors/run_processor.py --all-pending >> .agents/cron/logs/cron_processor.log 2>&1" >> /tmp/current_cron

# Cài đặt crontab mới
crontab /tmp/current_cron
rm /tmp/current_cron

echo "✅ Đã cài đặt thành công 3 Cron Jobs cho Knowledge Tree (Kiến trúc mới)!"
echo ""
echo "📋 Danh sách Cron:"
echo "  1. Auto-Heal:        0 */6 * * *     (mỗi 6h)        - Validate + auto-fix Master Tree"
echo "  2. Collectors Academic: */15 * * * * (15 phút)       - Watch inputs/academic/"
echo "  3. Collectors Standards: 0 3 * * 0   (CN 3am)        - Crosswalk 5 frameworks"
echo "  4. Collectors Trends:   0 2 * * 0   (CN 2am)        - auto_stem_discovery"
echo "  5. Processor:        0 */6 * * *     (mỗi 6h)        - LLM gaps → projects → pipeline"
echo ""
echo "🔍 Kiểm tra: crontab -l"
echo "📁 Logs:     $REPO_ROOT/.agents/cron/logs/"
echo "📥 INBOX:    $REPO_ROOT/projects/INBOX.md"