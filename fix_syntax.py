import re
import os

file_path = r'c:\Users\cagat\Desktop\Phyton\soyleyelim\core\templates\core\index.html'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix specific sort_order cases
    new_content = content.replace("sort_order=='onerilen'", "sort_order == 'onerilen'")
    new_content = new_content.replace("sort_order=='puan'", "sort_order == 'puan'")
    new_content = new_content.replace("sort_order=='teslimat'", "sort_order == 'teslimat'")
    new_content = new_content.replace("sort_order=='indirim'", "sort_order == 'indirim'")
    
    # Generic fix for other cases (e.g. key=='Value')
    # Regex: (\w+)==([\'"]) -> \1 == \2
    new_content = re.sub(r'(\b\w+)==([\'"])', r'\1 == \2', new_content)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed syntax errors in index.html")
    else:
        print("No changes needed or already fixed.")
else:
    print("File not found.")
