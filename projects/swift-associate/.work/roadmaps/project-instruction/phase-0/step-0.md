# 📖 PHASE 0 INSTRUCTION: WEBSOCKET TRANSPORT LAYER

> **Tài Liệu Hướng Dẫn Giảng Dạy & Thi Công Kỹ Thuật Chi Tiết Theo Từng Bước**  
> **Mã Dự án:** `PROJ-STREAM-CHAT` | **Target Product:** `Stream Chat Swift (Production Realtime Messaging)`  
> **Tech Stack:** `Swift, SwiftUI, Combine, URLSessionWebSocketTask, CoreData` | **Calibrated Focus Window:** **45m / Task**  
> **Reference Anchors:**  
> - 📍 `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md#L15]`  
> - 📖 `[DOC: project-ref/docs/swift/manifest.json]`  
> - 🧪 `[PROOF: project-ref/proof-of-functionality/stream_chat_swift__production_realtime_messaging_/build.log]`

---

## 🎯 1. TỔNG QUAN PHASE & MỤC TIÊU SƯ PHẠM
- **Hành động Kỹ thuật Lõi:** `Implement a WebSocket client using URLSessionWebSocketTask with automatic reconnection, ping/pong keep-alive, and message serialization/deserialization.`
- **Kiến thức Tiên quyết:** *Swift concurrency (async/await), URLSession, WebSocket protocol basics, JSON encoding/decoding.*
- **Mức độ Nhận thức Bloom:**
  - `UNIVERSAL (ULO)`: Hiểu nguyên lý cốt lõi.
  - `CONCEPTUAL_IMPL (CIO)`: Thiết kế quy trình thuật toán.
  - `SPECIFIC_IMPL (SIO)`: Viết mã nguồn trực tiếp và pass Tests.

---

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
Tạo thư mục và file cho Phase 0 theo cấu trúc dự án chuẩn.

---

## 💻 3. THỰC THI MÃ NGUỒN CHÍNH THỨC
Thực hiện: **Implement a WebSocket client using URLSessionWebSocketTask with automatic reconnection, ping/pong keep-alive, and message serialization/deserialization.**  
Tham chiếu mã nguồn mẫu từ: `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md]`

---

## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Xử lý lỗi kết nối, dữ liệu không hợp lệ, race conditions.
- Luôn bọc I/O trong error handling (try-catch / Result type / do-catch).

---

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
Viết unit test cho các chức năng cốt lõi của Phase 0.

---

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG

| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| Import/module not found | File chưa nằm trong đúng thư mục target | Kiểm tra cấu trúc project & build config |
| Runtime crash on async call | Missing await hoặc error handler | Thêm error handling wrapper |
| State không update UI | State mutation trên wrong thread | Dispatch về main thread |

---

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ (45 phút/task)

- [ ] **TASK_0_1** (⏱️ 45m): Read & Understand: *Swift concurrency (async/await), URLSession, WebSocket protocol basics, JSON encoding/decoding.*
  - 🎯 *Target LO:* `ULO-PROCESS_VS_THREAD-1`
  - 📦 *Deliverable:* Architecture Cheatsheet
- [ ] **TASK_0_2** (⏱️ 45m): Hands-on: Implement a WebSocket client using URLSessionWebSocketTask with automatic reconnection, ping/pong keep-alive, and message serialization/deserialization.
  - 🎯 *Target LO:* `SIO-PROCESS_VS_THREAD-1`
  - 📦 *Deliverable:* Working Code Module
- [ ] **TASK_0_3** (⏱️ 45m): Unit Test & Verify
  - 🎯 *Target LO:* `CIO-PROCESS_VS_THREAD-1`
  - 📦 *Deliverable:* Passing Tests & Git Commit

---

## 🏁 8. DEFINITION OF DONE & GATE CHECKPOINT

- [ ] ✅ Code module hoạt động hoàn chỉnh.
- [ ] ✅ Hoàn thành 100% Micro-Tasks.
- [ ] ⛔ **GATE 0 AUDIT:** Pass unit tests & AI code review. *(Nếu rớt: 15 phút Remediation Micro-Sprint)*.
