---
name: roadmap-aligner
description: Crawl online roadmaps (e.g. roadmap.sh) via Crawl4AI server, verify via SearXNG & Context7 API, capture prerequisite graph metadata, and align/enrich the Master Knowledge Tree TSV.
---

# Roadmap Aligner Skill

> **Goal:** You are the `@roadmap-aligner`. Your job is to crawl external technical roadmaps (such as `https://roadmap.sh/...`), extract sequence-ordered topics and prerequisite graph metadata, perform independent verification via SearXNG and Context7 API, and execute a **2-step decision framework with N:N Reuse Topology** to align new concepts into the Staging Knowledge Tree in `general-context/`.

---

## 🏛️ Staging, Diff & Versioning Architecture

To protect the official skill resource from unverified edits, all enrichment works operate on a **Staging Working Copy**:

- **Staging Location:** `general-context/mlo-knowlege-tree.tsv`
- **Official Master Location:** `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv`
- **Version Tracking:** `general-context/version_history.json`

### 🛠️ Staging Management Tools

1. **Initialize Staging Working Copy:**
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/init_staging_tree.py
   ```
2. **Apply Approved Plan to Staging Tree:**
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/apply_plan_to_staging.py
   ```
3. **Compare Staging vs Official Master (Diff Mechanism):**
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/tree_diff.py
   ```
   *Generates `.work/tree_diff_report.md` showing added, modified, and removed nodes across all 5 tables.*

4. **Reverse Sync back to Official Master (Sync-back on User Approval):**
   ```bash
   python3 .agents/skills/roadmap-aligner/scripts/sync_back_master.py
   ```
   *Copies approved `general-context/mlo-knowlege-tree.tsv` to skill resources, regenerates `master_tree.json`, and bumps the release version tag (e.g., `v2.2.0` $\rightarrow$ `v2.3.0`).*

---

## 🔗 MANDATORY RULE: N:N Graph Reuse First Topology

> **CRITICAL RULE:** All 5 tiers in the Knowledge Tree support **Many-to-Many (N:N)** relationships via comma-separated codes (`field_codes`, `subject_codes`, `category_codes`, `topic_codes`).

1. **Category & Topic Reuse Principle:**
   - **DO NOT** propose creating a new Category or Topic if an equivalent concept already exists anywhere in the Master Tree!
   - **Action:** Perform a full-breadth scan across all 82 Categories and 130 Topics. Reuse existing nodes and append the target Subject code into `subject_codes` or `category_codes` separated by commas `,` (e.g., `subject_codes: NETWORKING, WEB_DEV` for `NETWORK_SECURITY`).

2. **Concept Insertion Principle:**
   - Insert new Abstract Concepts directly under existing Topics/Categories by assigning multiple parent codes if necessary (e.g. `topic_code: APP_PROTOCOLS, CLOUD_COMPUTING`).
   - Only propose a NEW Category or Topic when the domain is 100% novel and cannot be represented by any existing node in the Master Tree.

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
- **Action:** Promote directly as a new `[CONCEPT PROPOSAL]` in `general-context/mlo-knowlege-tree.tsv`.

---

## 🔄 Two-Pass Workflow (Script + Agent)

1. **Pass 1: Script Execution (Automation Engine)**
   - Run python script:
     ```bash
     python3 .agents/skills/roadmap-aligner/scripts/crawl_roadmap_align.py <ROADMAP_URL>
     ```
   - Script outputs draft report at `.work/roadmap_alignment_report.md`.

2. **Pass 2: Agent N:N Semantic Audit (Semantic Engine)**
   - Agent reads `.work/roadmap_alignment_report.md`.
   - Agent performs mandatory N:N Audit across all 82 Categories and 130 Topics:
     - Enforces N:N reuse on existing Categories/Topics. Eliminates redundant Category/Topic proposals.
     - Validates Noun Phrase formatting for all proposed Concept codes.
     - Ensures cross-platform abstraction (e.g. elevating `CSS Box Model` $\rightarrow$ `UI_BOX_MODEL_LAYOUT`).
     - Maps new Concepts into existing Master Tree nodes via comma-separated N:N relation codes.

3. **Pass 3: Human Approval & Reverse Sync**
   - Present `tree_diff.py` report to user/teacher for approval.
   - Upon approval, execute `python3 .agents/skills/roadmap-aligner/scripts/sync_back_master.py` to sync back to official skill resources and bump version.
