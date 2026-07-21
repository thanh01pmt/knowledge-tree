import os
import csv
import json
import argparse

def parse_master_tsv(tsv_path):
    """Parses the multi-table Master TSV into a dictionary of lists."""
    with open(tsv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = {
        'fields': [],
        'subjects': [],
        'categories': [],
        'topics': [],
        'concepts': [],
        'learning_objectives': []
    }

    current_level = None
    headers = []

    for raw_line in lines:
        line = raw_line.strip('\n')
        # Detect table boundaries by looking at 'Bảng X:'
        if line.startswith('Bảng 1:'):
            current_level = 'fields'
            continue
        elif line.startswith('Bảng 2:'):
            current_level = 'subjects'
            continue
        elif line.startswith('Bảng 3:'):
            current_level = 'categories'
            continue
        elif line.startswith('Bảng 4:'):
            current_level = 'topics'
            continue
        elif line.startswith('Bảng 5:'):
            current_level = 'concepts'
            continue
        elif line.startswith('Bảng 6:'):
            current_level = 'learning_objectives'
            continue

        if not current_level:
            continue

        # Skip empty lines or descriptions
        if not line or line.startswith('Đây là') or line.startswith('Mỗi') or line.startswith('Các'):
            continue

        parts = line.split('\t')
        
        # Detect headers
        if parts[0] == 'code':
            headers = [h.strip() for h in parts]
            continue
            
        if headers and len(parts) >= 2 and parts[0]:
            # This is a data row
            row_dict = {}
            for i, header in enumerate(headers):
                val = parts[i].strip() if i < len(parts) else ""
                row_dict[header] = val
            data[current_level].append(row_dict)

    return data

def main():
    parser = argparse.ArgumentParser(description="Parse Master TSV into JSON")
    parser.add_argument('--input', type=str, default=".agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv")
    parser.add_argument('--output', type=str, default=".agents/skills/taxonomy-mapper/resources/master_tree.json")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    data = parse_master_tsv(args.input)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully parsed Master TSV and saved to {args.output}")
    print("Node counts:")
    for k, v in data.items():
        print(f"  {k}: {len(v)}")

if __name__ == "__main__":
    main()
