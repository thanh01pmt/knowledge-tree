import re
import shutil
from pathlib import Path

def update_master_tsv(tsv_path):
    # Backup
    shutil.copy(tsv_path, str(tsv_path) + ".bak")
    
    with open(tsv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # We need to insert rows in respective tables.
    # Find table start indices
    tables = {}
    for i, line in enumerate(lines):
        if line.startswith("Bảng 3: Nhóm chủ đề (categories)"):
            tables['categories'] = i
        elif line.startswith("Bảng 4: Chủ đề con (topics)"):
            tables['topics'] = i
        elif line.startswith("Bảng 5: Khái niệm (concepts)"):
            tables['concepts'] = i
            
    def insert_before(section_next, row):
        nonlocal lines
        # Find next section or end
        idx = len(lines)
        if section_next in tables:
            idx = tables[section_next] - 1
        # find the last non-empty line before idx
        while idx > 0 and lines[idx-1].strip() == "":
            idx -= 1
        lines.insert(idx, row + "\n")
        # Update indices after idx
        for k in tables:
            if tables[k] >= idx:
                tables[k] += 1
                
    # Add DEVELOPMENT_ENVIRONMENT to categories
    insert_before('topics', 'DEVELOPMENT_ENVIRONMENT\tDevelopment Environment & Tools\tKỹ năng sử dụng môi trường phát triển tích hợp (IDE), quản lý file, assets, và điều hướng dự án.\tSW_LIFECYCLE\tIDE, tools\t\t{"icon": "tools"}')
    
    # Add IDE_NAVIGATION to topics
    insert_before('concepts', 'IDE_NAVIGATION\tIDE Navigation\tĐiều hướng và quản lý cấu trúc file, assets trong dự án.\tDEVELOPMENT_ENVIRONMENT\tIDE, file, assets\t\t')
    
    # Add DEBUGGING_TECHNIQUES to topics
    insert_before('concepts', 'DEBUGGING_TECHNIQUES\tDebugging Techniques\tKỹ thuật và công cụ dùng để gỡ lỗi.\tTESTING_DEBUGGING\tdebug\t\t')
    
    # Add Concepts (End of file is fine for concepts)
    lines.append('PROJECT_ASSETS_MANAGEMENT\tProject Assets Management\tQuản lý tài nguyên hình ảnh, màu sắc trong IDE.\tIDE_NAVIGATION\tassets\t\t\n')
    lines.append('DECLARATIVE_UI_PARADIGM\tDeclarative UI Paradigm\tXây dựng giao diện kiểu khai báo.\tUI_CONTROLS\tdeclarative\t\t\n')
    lines.append('UI_MODIFIERS\tUI Modifiers\tÁp dụng các hàm thay đổi giao diện.\tUI_MODIFIERS\tmodifier\t\t\n')
    lines.append('STATE_PROPERTY_WRAPPER\tState Property Wrapper\tTheo dõi trạng thái bằng property wrapper.\tLOCAL_VIEW_STATE\tstate\t\t\n')
    lines.append('SYNTAX_VS_RUNTIME_ERRORS\tSyntax vs Runtime Errors\tPhân biệt các loại lỗi trong quá trình dev.\tERROR_MESSAGES,DEBUGGING_TECHNIQUES\terror\t\t\n')
    
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
if __name__ == "__main__":
    import sys
    update_master_tsv(sys.argv[1])
