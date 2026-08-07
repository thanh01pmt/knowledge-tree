# Backup — Trước khi chuyển sang Vertical Slicing

> **Ngày backup:** 2026-08-07
> **Lý do:** Chuyển đổi triết lý chia phase từ **Horizontal Layering** (tầng công nghệ) sang **Vertical Slicing** (mức độ hoàn thiện sản phẩm). Đây là thay đổi lớn, cần backup toàn bộ logic cũ để có thể rollback.

---

## 1. Lý do backup

Theo idea [`docs/ideas/2026-08-07-vertical-slicing-roadmap.md`](../../docs/ideas/2026-08-07-vertical-slicing-roadmap.md):

- **Cũ (Horizontal):** Phase chia theo tầng công nghệ (DATA MODEL, AI CORE, UI...) — mỗi tầng hoàn thiện A-Z, UI chỉ xuất hiện cuối cùng
- **Mới (Vertical):** Phase chia theo mức độ hoàn thiện sản phẩm (NỀN TẢNG → MVP → MỞ RỘNG → HOÀN THIỆN) — mỗi phase là 1 bước tiến thấy được

Thay đổi này ảnh hưởng đến:
1. `generate_jit_graph.py` — logic detect phase (`PHASE_BY_FILE` → feature graph)
2. `assemble_roadmap.py` (STEP 8.7) — nhóm phase theo topological layer → có thể đổi
3. Viewer components — hiển thị phase names
4. Knowledge mapping — thêm `bloom_level`

## 2. Files backup

### Scripts (scripts/)

| File | Vai trò | Trạng thái backup |
|------|---------|-------------------|
| `generate_roadmap_v3.py` | Orchestrator pipeline 11 steps | ✅ |
| `roadmap_discovery.py` | STEP 0: scan Master Tree + projects | ✅ |
| `assemble_roadmap.py` | STEP 8.7: topo sort + phases + metadata | ✅ |
| `generate_jit_graph.py` | JIT graph cho viewer (dùng `PHASE_BY_FILE`) | ✅ |
| `generate_jit_los.py` | STEP 5.5: JIT ULO/CIO/SIO | ✅ |
| `generate_adaptive_roadmap.py` | Adaptive roadmap (5-phase) | ✅ |
| `generate_project_roadmap.py` | Project roadmap (5-phase, backwards mapping) | ✅ |
| `generate_project_driven_roadmap.py` | Project-driven roadmap v4.2 | ✅ |
| `validate_roadmap.py` | STEP 9: post-generation validation | ✅ |

### Viewer (apps/viewer/src/components/)

| File | Vai trò | Trạng thái backup |
|------|---------|-------------------|
| `ActionRoadmapWeb.jsx` | Web interactive renderer (2-column card) | ✅ |
| `ActionRoadmapWeb.css` | CSS design tokens | ✅ |
| `RoadmapViewer.jsx` | Wrapper chọn roadmap type | ✅ |
| `RoadmapViewer.css` | CSS viewer header/layout | ✅ |

## 3. Cách rollback

```bash
# Restore scripts
cp backup/2026-08-07-vertical-slicing-before/generate_jit_graph.py scripts/
cp backup/2026-08-07-vertical-slicing-before/assemble_roadmap.py scripts/
cp backup/2026-08-07-vertical-slicing-before/generate_roadmap_v3.py scripts/
# ... (tương tự cho các file khác)

# Restore viewer
cp backup/2026-08-07-vertical-slicing-before/ActionRoadmapWeb.jsx apps/viewer/src/components/
cp backup/2026-08-07-vertical-slicing-before/ActionRoadmapWeb.css apps/viewer/src/components/
cp backup/2026-08-07-vertical-slicing-before/RoadmapViewer.jsx apps/viewer/src/components/
cp backup/2026-08-07-vertical-slicing-before/RoadmapViewer.css apps/viewer/src/components/
```

## 4. Tài liệu liên quan

| File | Mô tả |
|------|-------|
| `docs/ideas/2026-08-07-vertical-slicing-roadmap.md` | Idea mới (vertical slicing) |
| `docs/ideas/2026-08-06-action-roadmap.md` | Action Roadmap design (tiền thân) |
| `docs/ideas/2026-08-06-jit-knowledge-graph.md` | JIT graph design |

## 5. Ghi chú

- Backup này chụp trạng thái **trước khi** bắt đầu implement vertical slicing
- Sau khi implement xong, nếu cần rollback → dùng lệnh ở mục 3
- Không xóa thư mục backup này cho tới khi vertical slicing ổn định trên production
