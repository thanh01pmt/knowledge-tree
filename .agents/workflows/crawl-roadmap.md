---
description: Run this workflow to crawl external roadmaps (e.g. roadmap.sh) and align/enrich the Master Knowledge Tree.
---

# Workflow: Crawl Roadmap

> Run this workflow to crawl online roadmaps using Crawl4AI and align missing topics into the Master Knowledge Tree.

**Command:** `/crawl-roadmap <URL>`
**Owner:** `@roadmap-aligner`

## Contract

1. Load environment credentials (`CRAWL4AI_URL`, `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`) from `.env`.
2. Run the alignment script:
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/crawl_roadmap_align.py <URL>
   ```
3. Read the generated alignment report at `.work/roadmap_alignment_report.md`.
4. Review matched topics and missing candidate concepts with the user.
5. Present proposed new concept codes for user approval before modifying `mlo-knowlege-tree.tsv`.
