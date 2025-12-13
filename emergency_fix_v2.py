
import os
import re

file_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Read {len(content)} bytes.")
    
    # 1. Fix sort_order spacing
    # Matches sort_order=='value' or sort_order =='value' etc.
    # Replaces with sort_order == 'value'
    new_content, count = re.subn(r"sort_order\s*==\s*'([^']+)'", r"sort_order == '\1'", content)
    print(f"Fixed {count} instances of sort_order spacing.")
    
    # 2. Fix split {% if ... %tags
    # Specifically looking for {% at end of line, followed by if on next line
    # Regex: \{% \s* \n \s* if
    new_content, count2 = re.subn(r"\{%\s*\n\s*if", "{% if", new_content)
    print(f"Fixed {count2} split tags.")
    
    # 3. Specifically target the input lines if regex 2 missed them due to context
    # Example: value="puan" {% \n if ...
    new_content = re.sub(r'value="([^"]+)"\s+\{%\s*\n\s+if', r'value="\1" {% if', new_content)
    
    # 4. Target the cuisine specific ones
    new_content = re.sub(r'id="([^"]+)"\s+\{%\s*\n\s+if', r'id="\1" {% if', new_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully corrected index_v2.html")
    
    # Verify
    if "sort_order=='onerilen'" in new_content:
        print("ERROR: sort_order=='onerilen' still present!")
    else:
        print("VERIFIED: sort_order=='onerilen' is gone.")
        
else:
    print("File not found.")
