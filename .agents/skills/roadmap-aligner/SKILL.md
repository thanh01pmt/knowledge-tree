---
name: roadmap-aligner
description: Crawl online roadmaps (e.g. roadmap.sh) via Crawl4AI server and align/enrich the Master Knowledge Tree TSV.
---

# Roadmap Aligner

> **Goal:** You are the `@roadmap-aligner`. Your job is to crawl external technical roadmaps (such as `https://roadmap.sh/...`) using the Crawl4AI Server (authenticated via Cloudflare Access Service Tokens), extract structured topics and concepts, and perform gap analysis against `mlo-knowlege-tree.tsv`.

## Inputs
- Roadmap URL (e.g. `https://roadmap.sh/python-data-analysis`)
- Environment variables: `CRAWL4AI_URL`, `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET` (from `.env` or `.env.local`)
- Master Knowledge Tree: `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv`

## Outputs
- `.work/roadmap_alignment_report.md` (Alignment and Gap Analysis Report)

## Process
1. Read `CRAWL4AI_URL` and Cloudflare Access tokens from `.env` / `.env.local`.
2. Execute the python alignment script:
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/crawl_roadmap_align.py <ROADMAP_URL>
   ```
3. Read the generated report at `.work/roadmap_alignment_report.md`.
4. Review matched topics and missing candidates (gaps) with the user.
5. If requested by the user, propose new `UPPER_SNAKE_CASE` codes and descriptions for missing candidates to be merged into `mlo-knowlege-tree.tsv`.
