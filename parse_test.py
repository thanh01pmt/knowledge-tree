import csv
with open('.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv', 'r') as f:
    for i, line in enumerate(f):
        if line.startswith('Bảng'):
            print(f"Line {i}: {line.strip()}")
