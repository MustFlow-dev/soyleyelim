import os
import re

path = r"c:\Users\cagat\Desktop\Phyton\soyleyelim\core\templates\core\index_v2.html"

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Read {len(content)} characters.")

    # Fix split tag at 951 (catAll)
    content = re.sub(r'id="catAll" {% if not secili_kategoriler\s*%\}checked{% endif %}', 'id="catAll" {% if not secili_kategoriler %}checked{% endif %}', content)

    # Fix split tag at 992 (Pide)
    content = re.sub(r'id="catPide" {%\s*if \'Pide\' in secili_kategoriler %\}checked{% endif %}', 'id="catPide" {% if \'Pide\' in secili_kategoriler %}checked{% endif %}', content)

    # Fix split tag at 998 (Cigkofte)
    content = re.sub(r'id="catCigkofte" {%\s*if \'Çiğ Köfte\' in secili_kategoriler %\}checked{% endif %}', 'id="catCigkofte" {% if \'Çiğ Köfte\' in secili_kategoriler %}checked{% endif %}', content)
    
    # Fix split tag at 1004 (Uzak Dogu)
    content = re.sub(r'id="catUzak" {%\s*if \'Uzak Doğu\' in secili_kategoriler %\}checked{% endif %}', 'id="catUzak" {% if \'Uzak Doğu\' in secili_kategoriler %}checked{% endif %}', content)

    # Also general fix for any remaining split tags like value="..." {% newline if ...
    content = re.sub(r'\{%\s*\n\s+if', '{% if', content)
    content = re.sub(r'\n\s*%\}checked', '%}checked', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("File saved successfully with new fixes.")

except Exception as e:
    print(f"Error: {e}")
