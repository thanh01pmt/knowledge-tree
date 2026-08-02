# Agentic Cron Definitions

File này lưu trữ cấu hình các **Agentic Cron** (Tác vụ ngầm đánh thức AI) cho hệ thống Knowledge Tree.

Do các lệnh `/schedule` được lưu trong bộ nhớ tạm của phiên IDE, nếu bạn khởi động lại IDE hoặc mở một phiên mới và muốn khôi phục lại toàn bộ Agentic Cron, bạn chỉ cần copy-paste các lệnh dưới đây vào khung chat:

---

## Kiến trúc 3 Cron (Phase 1 + Phase 2)

### **Cron 1: Auto-Heal** — *Guardian (bảo vệ Master Tree)*
- **Schedule**: `0 */6 * * *` (mỗi 6 tiếng)
- **Chức năng**: Quick validate Master Tree (T6, referential integrity) + LLM auto-fix
- **Output**: `projects/INBOX.md` tag `[AUTO_HEAL]`

```text
/schedule CronExpression="0 */6 * * *" Prompt="[Cron 1 - Auto-Heal] Thức dậy và chạy lệnh 'python3 .agents/cron/cron_auto_heal.py'. Nếu script báo lỗi Master Tree, hãy đọc log lỗi, tự động sửa file TSV, sau đó ghi báo cáo vào file 'projects/INBOX.md' với tag [AUTO_HEAL]. Nếu không có lỗi, ghi trạng thái '[x] Master Tree Healthy' vào 'projects/INBOX.md'. Cuối cùng, thực hiện 'git add .', 'git commit -m \"chore(cron): Auto-heal check & fix\"' và 'git push origin main'."
```

---

### **Cron 2: Collectors** — *Research & Context Collection (Phase 1)*
- **Schedule**: Multi-schedule trong 1 script
  - Academic: `*/15 * * * *` (15 phút) — watch `inputs/academic/`
  - Standards: `0 3 * * 0` (CN 3am) — crosswalk 5 frameworks
  - Trends: `0 2 * * 0` (CN 2am) — auto_stem_discovery
- **Chức năng**: Thu thập, tổ chức context → ghi vào `.work/research/<source>/<item_id>/`
- **Output**: `projects/INBOX.md` tag `[COLLECTORS]` + summary file

```text
/schedule CronExpression="*/15 * * * *" Prompt="[Cron 2 - Collectors Academic] Thức dậy và chạy lệnh 'python3 .agents/cron/collectors/run_collectors.py --source academic --schedule 15m'. Ghi kết quả tóm tắt vào 'projects/INBOX.md' với tag [COLLECTORS_ACADEMIC]. Commit & push."

/schedule CronExpression="0 3 * * 0" Prompt="[Cron 2 - Collectors Standards] Thức dậy và chạy lệnh 'python3 .agents/cron/collectors/run_collectors.py --source standards --schedule weekly'. Ghi kết quả tóm tắt vào 'projects/INBOX.md' với tag [COLLECTORS_STANDARDS]. Commit & push."

/schedule CronExpression="0 2 * * 0" Prompt="[Cron 2 - Collectors Trends] Thức dậy và chạy lệnh 'python3 .agents/cron/collectors/run_collectors.py --source trends --schedule weekly'. Ghi kết quả tóm tắt vào 'projects/INBOX.md' với tag [COLLECTORS_TRENDS]. Commit & push."
```

---

### **Cron 3: Processor** — *LLM Analysis & Pipeline Execution (Phase 2)*
- **Schedule**: `0 */6 * * *` (mỗi 6 tiếng) — sau khi collectors chạy
- **Chức năng**: 
  1. Scan `.work/research/**/metadata.json` tìm items `status: "pending"`
  2. LLM đọc context + Master Tree → phân tích gaps
  3. Mỗi gap = scaffold project → chạy `run-autonomous-pipeline` (10 bước, Agent-as-Judge)
  4. Cập nhật status, ghi INBOX
- **Output**: `projects/INBOX.md` tag `[PROCESSOR]` + project TSVs

```text
/schedule CronExpression="0 */6 * * *" Prompt="[Cron 3 - Processor] Thức dậy và chạy lệnh 'python3 .agents/cron/collectors/run_processor.py --limit 10 --all-pending'. Script sẽ: (1) Quét tất cả research items pending trong .work/research/, (2) Với mỗi item: LLM phân tích gap so với Master Tree, (3) Mỗi gap = scaffold project mới + chạy pipeline tự động (run-autonomous-pipeline), (4) Ghi kết quả vào 'projects/INBOX.md' với tag [PROCESSOR]. Nếu pipeline thất bại, ghi lỗi chi tiết. Commit & push."
```

---

## Tóm tắt 3 Cron

| Cron | Phase | Schedule | Chức năng chính | Output INBOX tag |
|------|-------|----------|-----------------|------------------|
| **1. Auto-Heal** | - | 6h | Validate + auto-fix Master Tree | `[AUTO_HEAL]` |
| **2. Collectors** | 1 | 15m / CN 2am / CN 3am | Research → context packages | `[COLLECTORS_*]` |
| **3. Processor** | 2 | 6h | LLM gaps → projects → pipeline | `[PROCESSOR]` |

---

## Luồng dữ liệu

```
inputs/academic/          5 Frameworks          Domain List + Exa
      │                       │                      │
      ▼                       ▼                      ▼
┌─────────────────────────────────────────────────────────┐
│                 CRON 2: COLLECTORS                       │
│  AcademicCollector | StandardsCollector | TrendCollector │
│  → .work/research/academic/  standards/  trends/        │
│  → context.md + metadata.json (status: pending)         │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                 CRON 3: PROCESSOR                        │
│  Scan pending → LLM analyze gaps → Scaffold projects    │
│  → run-autonomous-pipeline (10 steps, Agent-as-Judge)   │
│  → projects/<slug>/output/ (6 TSV)                      │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│              HUMAN VERIFICATION                          │
│  Verify 6 TSV → /sync-supabase (Gate §8)                │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│              MASTER TREE (T6 Compliant)                  │
└─────────────────────────────────────────────────────────┘
```

---

## INBOX.md Format

Mọi cron đều ghi vào `projects/INBOX.md` với format:

```markdown
# 📥 Agentic Cron Inbox (Needs Review)

## [AUTO_HEAL] 2026-08-02 06:00 — Check Complete
- Status: Master Tree Healthy
- T6 Compliance: 100%
- Referential Integrity: OK

## [COLLECTORS_STANDARDS] 2026-08-02 03:00 — Collection Complete
- Collected: 12 gap items
- Pending: 8 items
- Frameworks: ACM_CS2023, NGSS, CSTA, UNESCO_ICT, OECD_PISA

## [COLLECTORS_TRENDS] 2026-08-02 02:00 — Collection Complete
- Collected: 5 trend items
- Pending: 3 items (score >= 7.0)
- Top: AI Agents in Education (9.1), Quantum K-12 (8.8)

## [PROCESSOR] 2026-08-02 06:00 — Processing Complete
- Processed: 5 research items
- Projects created: 7
- gap-acm_cs2023-spd-20260802060000: ✅ Pipeline SUCCESS
- gap-trend-ai_agents-20260802060001: ✅ Pipeline SUCCESS
- gap-trend-quantum-20260802060002: ❌ Pipeline FAILED (see logs)
```

---

## Human Action Required

| Cron | Khi nào human act? | Action |
|------|-------------------|--------|
| **Auto-Heal** | Chỉ khi FAIL | Review fix suggestions, chỉnh TSV, push |
| **Collectors** | Không cần (chỉ collect) | — |
| **Processor** | Mỗi project success | **Verify 6 TSV** → `/sync-supabase` (Gate §8) |
| **Processor** | Mỗi project fail | Đọc log, fix context/collection, re-trigger |

---

## Manual Triggers

```bash
# Chạy collector cụ thể
python3 .agents/cron/collectors/run_collectors.py --source academic --schedule manual
python3 .agents/cron/collectors/run_collectors.py --source standards --schedule manual
python3 .agents/cron/collectors/run_collectors.py --source trends --schedule manual

# Chạy processor cho tất cả pending
python3 .agents/cron/collectors/run_processor.py --all-pending

# Chạy processor cho source cụ thể
python3 .agents/cron/collectors/run_processor.py --source standards --limit 5
```