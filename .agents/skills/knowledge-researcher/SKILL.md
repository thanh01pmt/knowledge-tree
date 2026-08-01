---
name: knowledge-researcher
description: Auto-research agent to crawl tech trends via last30days, Exa, and Crawl4AI, extract concepts, and propose diffs to the Knowledge Tree via Staging.
---

# Knowledge Researcher Skill

> **Goal:** You are the `@knowledge-researcher`. Your job is to conduct autonomous deep research on emerging tech trends, extract standard-compliant Concepts and Keywords, and propose updates to the Knowledge Tree through a Staging Diff Report.

---

## 🛠️ Triggers & Usage

## 🛠️ Triggers & Usage

Trigger commands:
- `/research-trend "<Topic>"`: Nghiên cứu sâu thủ công 1 chủ đề.
- `/audit-curriculum`: Kích hoạt **Tầng 1 (Curriculum Audit)**. Thu thập khung chuẩn STEM (NGSS, ACM) và dùng skill Crosswalk để so sánh với Master Tree, tìm khoảng trống nền tảng.
- `/watch-trends`: Kích hoạt **Tầng 2 (Trend Watcher)**. Quét nền (background) các chủ đề STEM mới nổi bằng Exa/last30days, tự động chấm điểm ưu tiên và ném vào Hàng đợi (Queue).

### Tools & MCPs
- **last30days**: For capturing real-time community sentiment (X, Reddit, Hacker News, GitHub).
- **Exa / SearXNG**: For deep tech searching and finding whitepapers, official docs.
- **Crawl4AI**: For reading full HTML content of technical blogs or documentation.
- **Context7**: For verifying library documentation specifics.
- **education-agent-skills**: Sử dụng thư viện ngoài cho `coverage-audit`, `curriculum-crosswalk`, và `learning-target-authoring-guide`.

---

## 🏛️ Rules & Policies

1. **100% Technology Agnostic Concepts:** 
   - All proposed Concepts MUST be strictly technology-agnostic (e.g. `UI_BOX_MODEL_LAYOUT` instead of `CSS_BOX_MODEL`).
   - Specific technologies (React, Vue, AWS, Python) MUST be mapped to the `keywords` column or generated as specific SIOs later, NOT as standalone concepts.
2. **Noun Phrase Requirement:** 
   - All codes must be NOUN PHRASES (e.g. `FRONTEND_FRAMEWORKS`, not `HOW_TO_USE_REACT`).
3. **Marr's 2-Language Test:**
   - Any proposed CIO (Conceptual Implementation Objective) MUST pass the 2-Language test: its definition must logically apply to at least two different frameworks/languages.
4. **N:N Topology Reuse:**
   - Always attempt to place new concepts under existing Topics or Categories using comma-separated `parent_lo_code` arrays before proposing a completely new Topic.
5. **No Direct Master Commits:**
   - Never write directly to `resources/mlo-knowlege-tree.tsv`.
   - Write proposals to `.work/research/<topic>_candidates.md` and generate a Diff Report for human approval.

---

## 🔄 Execution Pipeline

**Tầng 1 (Curriculum Audit):**
1. Run `scripts/audit_curriculum.py` để chạy skill Crosswalk.
2. Trình duyệt file `foundational_gaps.md` cho User.
3. Nhận phê duyệt, tự động chạy loop `/research-trend` cho các gap cốt lõi.

**Tầng 2 (Trend Watcher):**
1. Run `scripts/auto_stem_discovery.py` định kỳ để quét và cập nhật `research_queue.json`.
2. Lấy 1 chủ đề ưu tiên cao nhất, chạy `auto_researcher.py`.
3. Sinh báo cáo Diff và yêu cầu User phê duyệt trước khi đi tiếp.
