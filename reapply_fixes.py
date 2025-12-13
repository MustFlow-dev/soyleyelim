
import os
import re

file_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix sort_order spacing
    new_content = re.sub(r"sort_order=='([^']+)'", r"sort_order == '\1'", content)
    
    # 2. Fix split {% if ... %} tags
    # This handles {% at end of line
    new_content = re.sub(r"\{%\s*\n\s*if", "{% if", new_content)
    
    # 3. Ensure cuisine list inputs are clean (just in case they reverted too)
    # The clean block pattern from final_fix_v3.py is safest if we can match it.
    # But regex replacement for split check tags is good too.
    new_content = re.sub(r'id="([^"]+)"\s+\{%\s*\n\s+if', r'id="\1" {% if', new_content)
    new_content = re.sub(r'value="([^"]+)"\s+\{%\s*\n\s+if', r'value="\1" {% if', new_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Re-applied syntax fixes to index_v2.html")
else:
    print("File not found")
