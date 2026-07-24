# 🔄 Hướng Dẫn Cấu Hình CI/CD Tự Động Deploy Với GitHub Actions

Tài liệu này hướng dẫn thiết lập **GitHub Actions** để tự động đồng bộ mã nguồn và khởi chạy lại Container Multi-MCP Server trên **Oracle Cloud VM** mỗi khi nhánh `main` (hoặc `stable`) được push/merge code.

---

## 🛠️ 1. File Workflow Được Tạo Sẵn

File workflow nằm tại:
👉 [.github/workflows/deploy.yml](file:///Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree/.github/workflows/deploy.yml)

### Cơ chế hoạt động:
1. Khi có sự kiện `push` lên nhánh `main` hoặc `stable`.
2. GitHub Runner khởi tạo, checkout mã nguồn mới nhất.
3. Dùng SSH Key tự động kết nối bảo mật tới máy chủ Oracle VM (`ubuntu@140.245.127.64`).
4. Thực thi lệnh cập nhật repo (`git reset --hard origin/main`), tự động rebuild Docker Image và khởi chạy container (`docker compose up -d --build`).
5. Kiểm tra tính khả dụng của endpoint `http://localhost:8888/health`.

---

## 🔑 2. Cấu Hình Repository Secrets Trên GitHub

Để GitHub Actions kết nối được vào Oracle VM, bạn cần thêm **3 Secrets** vào GitHub Repository của bạn:

### Các bước thực hiện:
1. Truy cập vào GitHub Repository của bạn (`https://github.com/thanh01pmt/knowledge-tree`).
2. Vào **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions**.
3. Bấm **New repository secret** và thêm lần lượt 3 biến sau:

| Tên Secret (Name) | Giá Trị (Value) |
| :--- | :--- |
| **`ORACLE_HOST`** | `140.245.127.64` |
| **`ORACLE_USER`** | `ubuntu` |
| **`ORACLE_SSH_KEY`** | Paste toàn bộ nội dung file SSH Private Key (`ssh-key-2026-05-29.key`) bao gồm cả phần `-----BEGIN OPENSSH PRIVATE KEY-----` và `-----END OPENSSH PRIVATE KEY-----`. |

---

## 🧪 3. Kiểm Tra Tiến Trình Deployment

1. Mỗi khi push code lên nhánh `main`:
   ```bash
   git add .
   git commit -m "feat: add new mcp sub-server"
   git push origin main
   ```
2. Vào tab **Actions** trên GitHub Repo để xem tiến trình build thực tế:
   - Runner sẽ kích hoạt job `Build & Deploy to Remote Oracle VM`.
   - Nếu thành công, bạn sẽ thấy thông báo: `✅ Deployment Completed Successfully!`.
