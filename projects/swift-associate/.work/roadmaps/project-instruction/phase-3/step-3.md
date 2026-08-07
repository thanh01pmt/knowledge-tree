# 📖 PHASE 3 INSTRUCTION: SWIFTUI VIEW COMPONENTS & REACTIONS

> **Tài Liệu Hướng Dẫn Giảng Dạy & Thi Công Kỹ Thuật Chi Tiết Theo Từng Bước**  
> **Mã Dự án:** `PROJ-STREAM-CHAT` | **Target Product:** `Stream Chat Swift (Production Realtime Messaging)`  
> **Tech Stack:** `Swift, SwiftUI, Combine, URLSessionWebSocketTask, CoreData` | **Calibrated Focus Window:** **45m / Task**  
> **Reference Anchors:**  
> - 📍 `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md#L135]`  
> - 📖 `[DOC: project-ref/docs/swift/manifest.json]`  
> - 🧪 `[PROOF: project-ref/proof-of-functionality/stream_chat_swift__production_realtime_messaging_/build.log]`

---

## 🎯 1. TỔNG QUAN PHASE & MỤC TIÊU SƯ PHẠM
- **Hành động Kỹ thuật Lõi:** `Create reusable SwiftUI views for chat bubbles, reaction overlays, typing indicators, and message input field, binding them to the Combine state stream and CoreData store.`
- **Kiến thức Tiên quyết:** *SwiftUI (View, @State, @ObservedObject, @EnvironmentObject), view composition, animation, and state-driven UI updates.*
- **Mức độ Nhận thức Bloom:**
  - `UNIVERSAL (ULO)`: Hiểu nguyên lý cốt lõi.
  - `CONCEPTUAL_IMPL (CIO)`: Thiết kế quy trình thuật toán.
  - `SPECIFIC_IMPL (SIO)`: Viết mã nguồn trực tiếp và pass Tests.

---

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
Tạo thư mục và file cho Phase 3 theo cấu trúc dự án chuẩn.

---

## 💻 3. THỰC THI MÃ NGUỒN CHÍNH THỨC
Thực hiện: **Create reusable SwiftUI views for chat bubbles, reaction overlays, typing indicators, and message input field, binding them to the Combine state stream and CoreData store.**  
Tham chiếu mã nguồn mẫu từ: `[REF: project-ref/repos/stream_chat_swift__production_realtime_messaging_/notes.md]`

---

## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Xử lý lỗi kết nối, dữ liệu không hợp lệ, race conditions.
- Luôn bọc I/O trong error handling (try-catch / Result type / do-catch).

---

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
Viết unit test cho các chức năng cốt lõi của Phase 3.

---

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG

| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| Import/module not found | File chưa nằm trong đúng thư mục target | Kiểm tra cấu trúc project & build config |
| Runtime crash on async call | Missing await hoặc error handler | Thêm error handling wrapper |
| State không update UI | State mutation trên wrong thread | Dispatch về main thread |

---

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ (45 phút/task)

- [ ] **TASK_3_1** (⏱️ 45m): Read & Understand: *SwiftUI (View, @State, @ObservedObject, @EnvironmentObject), view composition, animation, and state-driven UI updates.*
  - 🎯 *Target LO:* `ULO-STRUCTURAL_PATTERNS-4`
  - 📦 *Deliverable:* Architecture Cheatsheet
- [ ] **TASK_3_2** (⏱️ 45m): Hands-on: Create reusable SwiftUI views for chat bubbles, reaction overlays, typing indicators, and message input field, binding them to the Combine state stream and CoreData store.
  - 🎯 *Target LO:* `SIO-STRUCTURAL_PATTERNS-4`
  - 📦 *Deliverable:* Working Code Module
- [ ] **TASK_3_3** (⏱️ 45m): Unit Test & Verify
  - 🎯 *Target LO:* `CIO-STRUCTURAL_PATTERNS-4`
  - 📦 *Deliverable:* Passing Tests & Git Commit

---

## 🏁 8. DEFINITION OF DONE & GATE CHECKPOINT

- [ ] ✅ Code module hoạt động hoàn chỉnh.
- [ ] ✅ Hoàn thành 100% Micro-Tasks.
- [ ] ⛔ **GATE 3 AUDIT:** Pass unit tests & AI code review. *(Nếu rớt: 15 phút Remediation Micro-Sprint)*.
