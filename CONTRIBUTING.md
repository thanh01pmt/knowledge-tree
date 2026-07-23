# Contributing to Knowledge Tree

Thank you for your interest in contributing to the **Universal Agentic Knowledge Tree Pipeline**! We welcome contributions from developers, educators, curriculum designers, and domain experts.

---

## 📜 Principles & Core Rules

Before contributing, please familiarize yourself with our core architectural constraints:

1. **100% Technology-Agnostic Master Tree**: All Fields, Subjects, Categories, Topics, Concepts, ULOs, and CIOs **must remain neutral**. Never mention specific languages, frameworks, or tools (e.g., Python, React, Docker) above the SIO (`SPECIFIC_IMPL`) layer.
2. **Marr's Tri-Level Test**: Conceptual Objectives (CIOs) must be representation-independent. Before submitting a new CIO, test mapping its description against $\ge 2$ different programming languages/tools.
3. **Master Tree Validation Gate**: Any PR that modifies `general-context/mlo-knowlege-tree.tsv` or `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` **must pass** `validate_master_tree.py` with 0 errors.

---

## 🛠️ How to Contribute

### 1. Proposing Taxonomy Changes (Master Tree)
- If you find a missing domain or concept, open an issue using the **Taxonomy Node Proposal** template.
- Specify the proposed node's code (`UPPER_SNAKE_CASE`), name, description, parent codes, and keywords.
- Avoid duplicate nodes — check existing nodes in `general-context/mlo-knowlege-tree.tsv` first.

### 2. Creating or Updating Project Trees
- Scaffold new projects via `/init <project-slug>`.
- Keep intermediate plans in `projects/<project-slug>/.work/`.
- Ensure output TSVs in `projects/<project-slug>/output/` pass `validate_tree.py` and `audit_coverage.py`.

### 3. Submitting Pull Requests
1. **Fork** the repository and create a feature branch (`git checkout -b feature/add-swift-taxonomy`).
2. Run validation tools locally:
   ```bash
   python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv general-context/mlo-knowlege-tree.tsv
   python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <active-project>
   ```
3. Commit your changes following clean commit message conventions (`feat: add geospatial concepts to master tree`).
4. Push to your fork and submit a **Pull Request** against the `main` branch.

---

## 🧪 Local Testing & Verification

Before submitting a PR, ensure all local validation checks pass:

```bash
# 1. Validate Master Tree referential integrity
python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv general-context/mlo-knowlege-tree.tsv

# 2. Parse Master Tree into JSON
python3 .agents/skills/taxonomy-mapper/scripts/parse_master_tree.py

# 3. Validate project output TSVs
python3 .agents/skills/tree-validator/scripts/validate_tree.py --project <active-project>
```

---

## 🤝 Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the repository maintainers.

Thank you for helping build a standardized, open knowledge tree for education!
