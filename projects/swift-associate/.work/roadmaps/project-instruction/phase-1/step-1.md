# 📖 PHASE 1 INSTRUCTION: COMBINE STATE BINDING & EVENT STREAM

> **Tài Liệu Hướng Dẫn Giảng Dạy & Thi Công Kỹ Thuật Chi Tiết Theo Từng Bước**  
> **Mã Dự án:** `PROJ-STREAM-CHAT` | **Target Product:** `Stream Chat Swift (Production Realtime Messaging)`  
> **Tech Stack:** `Swift, SwiftUI, Combine, URLSessionWebSocketTask, CoreData` | **Calibrated Focus Window:** **45m / Task**  
> **Reference Anchors:**  
> - 📍 `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md#L55]`  
> - 📖 `[DOC: project-ref/docs/swift/manifest.json]`  
> - 🧪 `[PROOF: project-ref/proof-of-functionality/stream_chat_swift__production_realtime_messaging_/build.log]`

---

## 🎯 1. TỔNG QUAN PHASE & MỤC TIÊU SƯ PHẠM
- **Hành động Kỹ thuật Lõi:** `Build a Combine-based event stream that transforms raw WebSocket messages into typed chat events (new message, typing indicator, reactions) and exposes them as publishers for UI binding.`
- **Kiến thức Tiên quyết:** *Combine framework (Publishers, Subscribers, Subjects, Operators), reactive programming patterns, error handling in Combine.*
- **Mức độ Nhận thức Bloom:**
  - `UNIVERSAL (ULO)`: Hiểu nguyên lý cốt lõi.
  - `CONCEPTUAL_IMPL (CIO)`: Thiết kế quy trình thuật toán.
  - `SPECIFIC_IMPL (SIO)`: Viết mã nguồn trực tiếp và pass Tests.

---

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
Tạo thư mục và file cho Phase 1 theo cấu trúc dự án chuẩn.

---

## 💻 3. THỰC THI MÃ NGUỒN CHÍNH THỨC
Thực hiện: **Build a Combine-based event stream that transforms raw WebSocket messages into typed chat events (new message, typing indicator, reactions) and exposes them as publishers for UI binding.**  
Tham chiếu mã nguồn mẫu từ: `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md]`

---

## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Xử lý lỗi kết nối, dữ liệu không hợp lệ, race conditions.
- Luôn bọc I/O trong error handling (try-catch / Result type / do-catch).

---

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
Viết unit test cho các chức năng cốt lõi của Phase 1.

---

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG

| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| Import/module not found | File chưa nằm trong đúng thư mục target | Kiểm tra cấu trúc project & build config |
| Runtime crash on async call | Missing await hoặc error handler | Thêm error handling wrapper |
| State không update UI | State mutation trên wrong thread | Dispatch về main thread |

---

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ (45 phút/task)

- [ ] **TASK_1_1** (⏱️ 45m): Read & Understand: *Combine framework (Publishers, Subscribers, Subjects, Operators), reactive programming patterns, error handling in Combine.*
  - 🎯 *Target LO:* `ULO-BEHAVIORAL_PATTERNS-2`
  - 📦 *Deliverable:* Architecture Cheatsheet
- [ ] **TASK_1_2** (⏱️ 45m): Hands-on: Build a Combine-based event stream that transforms raw WebSocket messages into typed chat events (new message, typing indicator, reactions) and exposes them as publishers for UI binding.
  - 🎯 *Target LO:* `SIO-BEHAVIORAL_PATTERNS-2`
  - 📦 *Deliverable:* Working Code Module
- [ ] **TASK_1_3** (⏱️ 45m): Unit Test & Verify
  - 🎯 *Target LO:* `CIO-BEHAVIORAL_PATTERNS-2`
  - 📦 *Deliverable:* Passing Tests & Git Commit

---

## 🏁 8. DEFINITION OF DONE & GATE CHECKPOINT

- [ ] ✅ Code module hoạt động hoàn chỉnh.
- [ ] ✅ Hoàn thành 100% Micro-Tasks.
- [ ] ⛔ **GATE 1 AUDIT:** Pass unit tests & AI code review. *(Nếu rớt: 15 phút Remediation Micro-Sprint)*.
