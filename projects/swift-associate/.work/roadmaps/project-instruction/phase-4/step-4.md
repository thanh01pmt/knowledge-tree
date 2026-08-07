# 📖 PHASE 4 INSTRUCTION: INTEGRATION & TESTING

> **Tài Liệu Hướng Dẫn Giảng Dạy & Thi Công Kỹ Thuật Chi Tiết Theo Từng Bước**  
> **Mã Dự án:** `PROJ-STREAM-CHAT` | **Target Product:** `Stream Chat Swift (Production Realtime Messaging)`  
> **Tech Stack:** `Swift, SwiftUI, Combine, URLSessionWebSocketTask, CoreData` | **Calibrated Focus Window:** **45m / Task**  
> **Reference Anchors:**  
> - 📍 `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md#L175]`  
> - 📖 `[DOC: project-ref/docs/swift/manifest.json]`  
> - 🧪 `[PROOF: project-ref/proof-of-functionality/stream_chat_swift__production_realtime_messaging_/build.log]`

---

## 🎯 1. TỔNG QUAN PHASE & MỤC TIÊU SƯ PHẠM
- **Hành động Kỹ thuật Lõi:** `Integrate all layers (transport, state, persistence, UI) into a cohesive chat client, write unit tests for Combine pipelines and CoreData operations, and UI tests for SwiftUI views.`
- **Kiến thức Tiên quyết:** *XCTest framework, mocking network and CoreData, testing Combine publishers, UI testing with XCUITest.*
- **Mức độ Nhận thức Bloom:**
  - `UNIVERSAL (ULO)`: Hiểu nguyên lý cốt lõi.
  - `CONCEPTUAL_IMPL (CIO)`: Thiết kế quy trình thuật toán.
  - `SPECIFIC_IMPL (SIO)`: Viết mã nguồn trực tiếp và pass Tests.

---

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
Tạo thư mục và file cho Phase 4 theo cấu trúc dự án chuẩn.

---

## 💻 3. THỰC THI MÃ NGUỒN CHÍNH THỨC
Thực hiện: **Integrate all layers (transport, state, persistence, UI) into a cohesive chat client, write unit tests for Combine pipelines and CoreData operations, and UI tests for SwiftUI views.**  
Tham chiếu mã nguồn mẫu từ: `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md]`

---

## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Xử lý lỗi kết nối, dữ liệu không hợp lệ, race conditions.
- Luôn bọc I/O trong error handling (try-catch / Result type / do-catch).

---

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
Viết unit test cho các chức năng cốt lõi của Phase 4.

---

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG

| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| Import/module not found | File chưa nằm trong đúng thư mục target | Kiểm tra cấu trúc project & build config |
| Runtime crash on async call | Missing await hoặc error handler | Thêm error handling wrapper |
| State không update UI | State mutation trên wrong thread | Dispatch về main thread |

---

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ (45 phút/task)

- [ ] **TASK_4_1** (⏱️ 45m): Read & Understand: *XCTest framework, mocking network and CoreData, testing Combine publishers, UI testing with XCUITest.*
  - 🎯 *Target LO:* `ULO-PROCESS_VS_THREAD-5`
  - 📦 *Deliverable:* Architecture Cheatsheet
- [ ] **TASK_4_2** (⏱️ 45m): Hands-on: Integrate all layers (transport, state, persistence, UI) into a cohesive chat client, write unit tests for Combine pipelines and CoreData operations, and UI tests for SwiftUI views.
  - 🎯 *Target LO:* `SIO-PROCESS_VS_THREAD-5`
  - 📦 *Deliverable:* Working Code Module
- [ ] **TASK_4_3** (⏱️ 45m): Unit Test & Verify
  - 🎯 *Target LO:* `CIO-PROCESS_VS_THREAD-5`
  - 📦 *Deliverable:* Passing Tests & Git Commit

---

## 🏁 8. DEFINITION OF DONE & GATE CHECKPOINT

- [ ] ✅ Code module hoạt động hoàn chỉnh.
- [ ] ✅ Hoàn thành 100% Micro-Tasks.
- [ ] ⛔ **GATE 4 AUDIT:** Pass unit tests & AI code review. *(Nếu rớt: 15 phút Remediation Micro-Sprint)*.
