#!/usr/bin/env bash
# setup_crontab.sh - Cài đặt các Cron Jobs tự động cho Knowledge Tree
# Chạy lệnh này để nạp lịch trình vào crontab của hệ thống macOS/Linux.

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$DIR")"
PYTHON_BIN="$(which python3)"

# Xóa các cron cũ của Knowledge Tree (nếu có) để tránh trùng lặp
crontab -l | grep -v "knowledge-tree/.agents/cron" > /tmp/current_cron
echo "" >> /tmp/current_cron

# Định nghĩa các Cron Jobs
# 1. Auto-Heal (Cron 1): Chạy mỗi 6 tiếng một lần (00:00, 06:00, 12:00, 18:00)
echo "0 */6 * * * cd $REPO_ROOT && $PYTHON_BIN .agents/cron/cron_auto_heal.py >> .agents/cron/logs/cron_auto_heal.log 2>&1" >> /tmp/current_cron

# 2. Academic Watcher (Cron 2): Quét thư mục inputs/academic/ mỗi 15 phút
echo "*/15 * * * * cd $REPO_ROOT && $PYTHON_BIN .agents/cron/cron_academic_watcher.py >> .agents/cron/logs/cron_academic_watcher.log 2>&1" >> /tmp/current_cron

# 3. Trend Research (Cron 3): Chạy mỗi tuần 1 lần vào 02:00 sáng Chủ Nhật
echo "0 2 * * 0 cd $REPO_ROOT && $PYTHON_BIN .agents/cron/cron_trend_research.py >> .agents/cron/logs/cron_trend_research.log 2>&1" >> /tmp/current_cron

# Cài đặt crontab mới
crontab /tmp/current_cron
rm /tmp/current_cron

echo "✅ Đã cài đặt thành công 3 Cron Jobs cho Knowledge Tree!"
echo "Bạn có thể kiểm tra danh sách bằng lệnh: crontab -l"
