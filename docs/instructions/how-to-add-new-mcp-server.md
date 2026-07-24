# 📖 Hướng Dẫn Bổ Sung MCP Sub-Server Mới Vào Multi-MCP Hub

Tài liệu này hướng dẫn chi tiết cách bổ sung một **MCP Sub-Server mới** (ví dụ: `analytics`, `crawler`, `git_manager`,...) vào hệ thống **Multi-MCP Hub** hiện tại của dự án `knowledge-tree`.

---

## 🏗️ 1. Tổng Quan Kiến Trúc Multi-MCP Hub

Hệ thống sử dụng mô hình **FastMCP Server Composition (`mount()`)**:

```tree
knowledge-tree/
├── mcp/
│   ├── main.py                  # Entrypoint chính (Hub gom tất cả sub-servers)
│   └── servers/                 # Thư mục chứa các Sub-MCP Servers độc lập
│       ├── kt_server.py         # Sub-Server #1: Knowledge Tree Tools (kt_*)
│       ├── system_server.py     # Sub-Server #2: System Tools & Resources (sys_*)
│       └── <domain>_server.py   # Sub-Server Mới Của Bạn (<namespace>_*)
```

- **Tất cả các Sub-Server** đều chạy chung trong **1 container Docker duy nhất** tại cổng `8888` (endpoint `/mcp`).
- Mỗi Sub-Server được gán 1 **`namespace`** riêng để tự động tiền tố hoá tên Tool (tránh đụng độ tên giữa các server).

---

## 🚀 2. Quy Trình 3 Bước Thêm MCP Server Mới

### Bước 1: Tạo File Sub-Server Mới
Tạo một file Python mới trong thư mục [mcp/servers/](file:///Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree/mcp/servers/), ví dụ: `mcp/servers/analytics_server.py`:

```python
#!/usr/bin/env python3
"""
Sub-MCP Server: Analytics & Metrics (analytics)
"""
from fastmcp import FastMCP

# 1. Khởi tạo FastMCP sub-instance
analytics_mcp = FastMCP("AnalyticsOps")

# 2. Định nghĩa các Tools
@analytics_mcp.tool
def get_project_stats(project_name: str) -> str:
    """Trả về thống kê số lượng LOs, Concepts, Topics của một dự án."""
    # Logic thống kê của bạn ở đây...
    return f"Stats for {project_name}: 120 LOs, 45 Concepts."

# 3. Định nghĩa Resources (Nếu cần)
@analytics_mcp.resource("analytics://summary")
def get_global_analytics_summary() -> str:
    """Tài nguyên thống kê tổng quan toàn hệ thống."""
    return "Global Summary: 15 Active Projects."

# 4. Định nghĩa Prompts (Nếu cần)
@analytics_mcp.prompt
def suggest_analytics_queries() -> str:
    """Prompt mẫu gợi ý truy vấn phân tích."""
    return "Hãy phân tích độ phủ tri thức của dự án roadmap_sh_graphql."
```

---

### Bước 2: Đăng Ký (Mount) Vào Hub Chính (`mcp/main.py`)
Mở file [mcp/main.py](file:///Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree/mcp/main.py) và thêm 2 dòng để import & mount sub-server mới:

```python
# 1. Import sub-server mới từ mcp/servers/
from servers.analytics_server import analytics_mcp

# 2. Mount vào Hub với namespace mong muốn (ví dụ: 'analytics')
hub.mount(analytics_mcp, namespace="analytics")
```

*(Sau bước này, các Tool của `analytics_mcp` sẽ tự động mang tiền tố `analytics_`, ví dụ: `analytics_get_project_stats`)*.

---

### Bước 3: Deploy & Kiểm Trụ

#### A. Chạy thử nghiệm Local:
```bash
uv run python mcp/main.py --help
```

#### B. Synchronize & Deploy lên Oracle Cloud VM:
1. Sync mã nguồn mới lên máy chủ từ máy local:
   ```bash
   rsync -avz -e "ssh -i /path/to/ssh-key.key" --exclude='.git' --exclude='.venv' /path/to/knowledge-tree/ ubuntu@140.245.127.64:/home/ubuntu/knowledge-tree/
   ```

2. Khởi chạy lại Docker Container trên VM:
   ```bash
   ssh -i /path/to/ssh-key.key ubuntu@140.245.127.64 "cd /home/ubuntu/knowledge-tree && docker compose up -d --build"
   ```

3. Kiểm tra thông tin Health Endpoint:
   ```bash
   curl http://localhost:8888/health
   ```
   **Kết quả mong đợi**:
   ```json
   {
     "status": "healthy",
     "service": "Multi-MCP Hub Server",
     "version": "0.2.0",
     "mounted_servers": ["kt", "sys", "analytics"]
   }
   ```

---

## 🤖 3. Sử Dụng Phía Agent / Client (Cursor, Pi, Claude Desktop)

Không cần thay đổi bất kỳ URL cấu hình nào trên Client! File `.mcp.json` vẫn giữ nguyên:

```json
{
  "mcpServers": {
    "knowledge-tree-hub": {
      "url": "http://localhost:8888/mcp"
    }
  }
}
```

Agent sẽ tự động nhận diện và liệt kê thêm bộ công cụ `analytics_*` bên cạnh `kt_*` và `sys_*`.

---

## 📌 Các Quy Tắc Cần Nhớ (Best Practices)
1. **Đặt tên Namespace ngắn gọn**: Nên dùng dạng kebab-case hoặc snake_case ngắn gọn (ví dụ: `kt`, `db`, `sys`, `git`, `ai`).
2. **Pydantic / Type Hints**: Luôn chỉ định kiểu dữ liệu (`project_name: str`, `fix: bool = False`) và viết docstring đầy đủ cho từng `@mcp.tool`. AI Agent sẽ đọc docstring này làm chỉ dẫn sử dụng tool.
3. **Thư viện phụ**: Nếu sub-server mới cần thêm thư viện Python bên ngoài, hãy nhớ thêm vào file [pyproject.toml](file:///Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree/pyproject.toml) trước khi deploy Docker.
