# validate-master-tree

Run this workflow to validate referential integrity, cross-level collisions, empty parents, and level skips for the Master Knowledge Tree TSV.

## Steps

1. Run the `validate_master_tree.py` script against the Master Tree TSV:
   ```bash
   python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv general-context/mlo-knowlege-tree.tsv
   ```

2. Also check the official skill copy in `taxonomy-mapper`:
   ```bash
   python3 .agents/skills/tree-validator/scripts/validate_master_tree.py --tsv .agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv
   ```

3. Ensure both reports show `0 error(s)`. If errors are reported, fix the underlying data in `general-context/mlo-knowlege-tree.tsv`, synchronize to `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv`, and re-parse:
   ```bash
   python3 .agents/skills/taxonomy-mapper/scripts/parse_master_tree.py
   ```
