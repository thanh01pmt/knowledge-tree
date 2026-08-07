# 📖 PHASE 5 INSTRUCTION: PERFORMANCE & PRODUCTION READINESS

> **Tài Liệu Hướng Dẫn Giảng Dạy & Thi Công Kỹ Thuật Chi Tiết Theo Từng Bước**  
> **Mã Dự án:** `PROJ-STREAM-CHAT` | **Target Product:** `Stream Chat Swift (Production Realtime Messaging)`  
> **Tech Stack:** `Swift, SwiftUI, Combine, URLSessionWebSocketTask, CoreData` | **Calibrated Focus Window:** **45m / Task**  
> **Reference Anchors:**  
> - 📍 `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md#L215]`  
> - 📖 `[DOC: project-ref/docs/swift/manifest.json]`  
> - 🧪 `[PROOF: project-ref/proof-of-functionality/stream_chat_swift__production_realtime_messaging_/build.log]`

---

## 🎯 1. TỔNG QUAN PHASE & MỤC TIÊU SƯ PHẠM
- **Hành động Kỹ thuật Lõi:** `Optimize WebSocket reconnection backoff, reduce memory footprint of CoreData cache, profile Combine subscriptions, and add logging/monitoring for production deployment.`
- **Kiến thức Tiên quyết:** *Instruments for profiling, memory management in Swift, production deployment considerations (crash reporting, analytics).*
- **Mức độ Nhận thức Bloom:**
  - `UNIVERSAL (ULO)`: Hiểu nguyên lý cốt lõi.
  - `CONCEPTUAL_IMPL (CIO)`: Thiết kế quy trình thuật toán.
  - `SPECIFIC_IMPL (SIO)`: Viết mã nguồn trực tiếp và pass Tests.

---

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
Tạo thư mục và file cho Phase 5 theo cấu trúc dự án chuẩn.

---

## 💻 3. THỰC THI MÃ NGUỒN CHÍNH THỨC
Thực hiện: **Optimize WebSocket reconnection backoff, reduce memory footprint of CoreData cache, profile Combine subscriptions, and add logging/monitoring for production deployment.**  
Tham chiếu mã nguồn mẫu từ: `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md]`

---

## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Xử lý lỗi kết nối, dữ liệu không hợp lệ, race conditions.
- Luôn bọc I/O trong error handling (try-catch / Result type / do-catch).

---

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
Viết unit test cho các chức năng cốt lõi của Phase 5.

---

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG

| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| Import/module not found | File chưa nằm trong đúng thư mục target | Kiểm tra cấu trúc project & build config |
| Runtime crash on async call | Missing await hoặc error handler | Thêm error handling wrapper |
| State không update UI | State mutation trên wrong thread | Dispatch về main thread |

---

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ (45 phút/task)

- [ ] **TASK_5_1** (⏱️ 45m): Read & Understand: *Instruments for profiling, memory management in Swift, production deployment considerations (crash reporting, analytics).*
  - 🎯 *Target LO:* `ULO-PROCESS_VS_THREAD-6`
  - 📦 *Deliverable:* Architecture Cheatsheet
- [ ] **TASK_5_2** (⏱️ 45m): Hands-on: Optimize WebSocket reconnection backoff, reduce memory footprint of CoreData cache, profile Combine subscriptions, and add logging/monitoring for production deployment.
  - 🎯 *Target LO:* `SIO-PROCESS_VS_THREAD-6`
  - 📦 *Deliverable:* Working Code Module
- [ ] **TASK_5_3** (⏱️ 45m): Unit Test & Verify
  - 🎯 *Target LO:* `CIO-PROCESS_VS_THREAD-6`
  - 📦 *Deliverable:* Passing Tests & Git Commit

---

## 🏁 8. DEFINITION OF DONE & GATE CHECKPOINT

- [ ] ✅ Code module hoạt động hoàn chỉnh.
- [ ] ✅ Hoàn thành 100% Micro-Tasks.
- [ ] ⛔ **GATE 5 AUDIT:** Pass unit tests & AI code review. *(Nếu rớt: 15 phút Remediation Micro-Sprint)*.
