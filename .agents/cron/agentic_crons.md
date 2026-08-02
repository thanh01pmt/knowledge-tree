# Agentic Cron Definitions

File này lưu trữ cấu hình các **Agentic Cron** (Tác vụ ngầm đánh thức AI) cho hệ thống Knowledge Tree.

Do các lệnh `/schedule` được lưu trong bộ nhớ tạm của phiên IDE, nếu bạn khởi động lại IDE hoặc mở một phiên mới và muốn khôi phục lại toàn bộ Agentic Cron, bạn chỉ cần copy-paste các lệnh dưới đây vào khung chat:

### Cron 1: Auto-Heal (Mỗi 6 tiếng)
```text
/schedule CronExpression="0 */6 * * *" Prompt="[Cron 1 - Auto-Heal] Thức dậy và chạy lệnh 'python3 .agents/cron/cron_auto_heal.py'. Nếu script báo lỗi Master Tree, hãy đọc log lỗi, tự động sửa file TSV, sau đó ghi báo cáo vào file 'projects/INBOX.md'. Nếu không có lỗi, ghi trạng thái '[x] Master Tree Healthy' vào 'projects/INBOX.md'. Cuối cùng, thực hiện 'git add .', 'git commit -m \"chore(cron): Auto-heal check & fix\"' và 'git push origin main'."
```

### Cron 2: Academic Watcher (Mỗi 15 phút)
```text
/schedule CronExpression="*/15 * * * *" Prompt="[Cron 2 - Academic Watcher] Thức dậy và chạy lệnh 'python3 .agents/cron/cron_academic_watcher.py'. Nếu script báo có file mới và đã dựng Project thành công, hãy cập nhật phần Pending Approvals trong file 'projects/INBOX.md' để nhắc Người dùng (Tony) chạy '/run-pipeline'. Cuối cùng, nếu có thay đổi, thực hiện 'git add .', 'git commit -m \"chore(cron): Scaffold new academic project\"' và 'git push origin main'."
```

### Cron 3: Trend Research (Sáng Chủ Nhật)
```text
/schedule CronExpression="0 2 * * 0" Prompt="[Cron 3 - Trend Research] Thức dậy và chạy lệnh 'python3 .agents/cron/cron_trend_research.py'. Khi script chạy xong last30days và dựng Project mới, hãy cập nhật phần Pending Approvals trong file 'projects/INBOX.md' để Người dùng (Tony) vào duyệt và chạy '/run-pipeline'. Cuối cùng, thực hiện 'git add .', 'git commit -m \"chore(cron): Scaffold trend research project\"' và 'git push origin main'."
```
