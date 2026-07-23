---
name: roadmap-aligner
description: Crawl online roadmaps (e.g. roadmap.sh) via Crawl4AI server, verify via SearXNG & Context7 API, capture prerequisite graph metadata, and align/enrich the Master Knowledge Tree TSV.
---

# Roadmap Aligner Skill

> **Goal:** You are the `@roadmap-aligner`. Your job is to crawl external technical roadmaps (such as `https://roadmap.sh/...`), extract sequence-ordered topics and prerequisite graph metadata, perform independent verification via SearXNG and Context7 API, and execute a **2-step decision framework** to align new concepts into `mlo-knowlege-tree.tsv`.

---

## 🏗️ Tri-Layer Architecture

1. **Layer 1: Crawl4AI Server (`CRAWL4AI_URL`)**
   - Crawl roadmap SVG/HTML structure using Cloudflare Access Service Tokens (`CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`).
   - Extract raw topics, sequence order (`Order #`), and prerequisite flow (`Prerequisite Node`).
2. **Layer 2: SearXNG Engine (`SEARXNG_URL`)**
   - Perform independent multi-source verification and retrieve reference links/snippets for unverified topics.
3. **Layer 3: Context7 API (`CONTEXT7_API_KEY`)**
   - Query official library documentation, official descriptions, and exact library IDs for extracted tools and frameworks.

---

## ⚖️ 2-Step Decision Framework & Noun Phrase Rule

When evaluating candidate items extracted from a roadmap:

### 🛠️ Step 1: Concrete Tool Evaluation
- **Condition:** Item is a concrete tool, technology, or platform (e.g. `pip`, `npm`, `yarn`, `pnpm`, `conda`, `uv`, `venv`, `VS Code`, `JupyterLab`, `Google Colab`, `GitHub`, `React`, `Vue.js`, `Vite`, `ESLint`).
- **Action:** **DO NOT** make it a standalone Concept! Map it into the `keywords` / `metadata` column of its parent **Abstract Concept** (e.g. `PACKAGE_MANAGEMENT`, `VIRTUAL_ENVIRONMENTS`, `DEVELOPMENT_ENVIRONMENTS`, `VCS_HOSTING`, `FRONTEND_FRAMEWORKS`, `MODULE_BUNDLERS`).

### 📐 Step 2: Abstract Concept Promotion & Noun Phrase Rule
- **Condition:** Item represents an abstract, technology-agnostic knowledge concept (e.g. *List Comprehensions*, *Data Cleaning*, *Web Security*, *Box Model Layout*).
- **Rule (MUST BE NOUN PHRASE):** Concept codes **MUST BE NOUNS OR NOUN PHRASES** (e.g. `INTERNET_FUNDAMENTALS`, `HTTP_PROTOCOL`, `DOMAIN_NAME_SYSTEM`, `UI_BOX_MODEL_LAYOUT`). Never use question sentences like `HOW_DOES_THE_INTERNET_WORK` or `WHAT_IS_HTTP`.
- **Action:** Promote directly as a new `[CONCEPT PROPOSAL]` in `mlo-knowlege-tree.tsv`.

---

## 🔄 Two-Pass Workflow (Script + Agent)

1. **Pass 1: Script Execution (Automation Engine)**
   - Run python script:
     ```bash
     python3 .agents/skills/roadmap-aligner/scripts/crawl_roadmap_align.py <ROADMAP_URL>
     ```
   - Script outputs draft report at `.work/roadmap_alignment_report.md`.

2. **Pass 2: Agent Semantic Refinement (Semantic Engine)**
   - Agent reads `.work/roadmap_alignment_report.md`.
   - Agent performs second-pass semantic evaluation:
     - Validates Noun Phrase formatting for all proposed Concept codes.
     - Ensures cross-platform abstraction (e.g. elevating `CSS Box Model` $\rightarrow$ `UI_BOX_MODEL_LAYOUT`).
     - Verifies parent hierarchy propagation (`Concept` $\rightarrow$ `Topic` $\rightarrow$ `Category` $\rightarrow$ `Subject` $\rightarrow$ `Field`).

3. **Pass 3: Human Approval**
   - Present final `.work/mapping-plan.md` to user/teacher for approval before updating `mlo-knowlege-tree.tsv` and executing `/build-tree`.
