import re

path = r"c:\Users\cagat\Desktop\Phyton\soyleyelim\core\templates\core\index_v2.html"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Missing spaces around == (and handling if they are split across lines)
# We look for: sort_order=='something'
# Pattern: sort_order\s*==\s*'([^']+)'
content = re.sub(r"sort_order\s*==\s*'([^']+)'", r"sort_order == '\1'", content)

# Fix 2: Split {% if ... %} tags
# Example: {% if sort_order == 'puan' \n %} -> {% if sort_order == 'puan' %}
# We want to merge lines inside {% ... %} if they are split.
# A safe way for these specific known cases:

# Case A: Split `{%` and `if`
# No, usually it's `{% if condition` ... newline ... `%}`
# Or `{%` newline `if ... %}` (like lines 921-922: `{% \n if ... }`)

# Let's fix specific known blocks by replacing the whole messy string with clean string.

replacements = [
    # 1. onerilen
    (r"""<input class="form-check-input" type="radio" name="sort" id="sortRec" value="onerilen"
                                    {% if sort_order=='onerilen' %}checked{% endif %} onchange="this.form.submit()">""",
     r"""<input class="form-check-input" type="radio" name="sort" id="sortRec" value="onerilen" {% if sort_order == 'onerilen' %}checked{% endif %} onchange="this.form.submit()">"""),
     
     # 2. puan (split)
    (r"""<input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" {%
                                    if sort_order=='puan' %}checked{% endif %} onchange="this.form.submit()">""",
     r"""<input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" {% if sort_order == 'puan' %}checked{% endif %} onchange="this.form.submit()">"""),
     
     (r"""<input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" {%
                                    if sort_order == 'puan' %}checked{% endif %} onchange="this.form.submit()">""",
     r"""<input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" {% if sort_order == 'puan' %}checked{% endif %} onchange="this.form.submit()">"""),

     # 3. teslimat
    (r"""<input class="form-check-input" type="radio" name="sort" id="sortTime" value="teslimat"
                                    {% if sort_order=='teslimat' %}checked{% endif %} onchange="this.form.submit()">""",
     r"""<input class="form-check-input" type="radio" name="sort" id="sortTime" value="teslimat" {% if sort_order == 'teslimat' %}checked{% endif %} onchange="this.form.submit()">"""),
     
     # 4. indirim
    (r"""<input class="form-check-input" type="radio" name="sort" id="sortDiscount"
                                    value="indirim" {% if sort_order=='indirim' %}checked{% endif %}
                                    onchange="this.form.submit()">""",
     r"""<input class="form-check-input" type="radio" name="sort" id="sortDiscount" value="indirim" {% if sort_order == 'indirim' %}checked{% endif %} onchange="this.form.submit()">"""),

     # 5. catAll (split)
     (r"""<input class="form-check-input" type="checkbox" id="catAll" {% if not secili_kategoriler
                                    %}checked{% endif %} onclick="selectCategory('')">""",
      r"""<input class="form-check-input" type="checkbox" id="catAll" {% if not secili_kategoriler %}checked{% endif %} onclick="selectCategory('')">"""),

     # 6. Pide (split)
     (r"""<input class="form-check-input" type="checkbox" name="cat" value="Pide" id="catPide" {%
                                    if 'Pide' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">""",
      r"""<input class="form-check-input" type="checkbox" name="cat" value="Pide" id="catPide" {% if 'Pide' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">"""),
      
     # 7. Çiğ Köfte (split) - from previous logs, might exist
     (r"""<input class="form-check-input" type="checkbox" name="cat" value="Çiğ Köfte"
                                    id="catCigkofte" {% if 'Çiğ Köfte' in secili_kategoriler %}checked{% endif %}
                                    onchange="this.form.submit()">""",
      r"""<input class="form-check-input" type="checkbox" name="cat" value="Çiğ Köfte" id="catCigkofte" {% if 'Çiğ Köfte' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">"""),
      
      # 8. Uzak Doğu (split)
      (r"""<input class="form-check-input" type="checkbox" name="cat" value="Uzak Doğu"
                                    id="catUzak" {% if 'Uzak Doğu' in secili_kategoriler %}checked{% endif %}
                                    onchange="this.form.submit()">""",
       r"""<input class="form-check-input" type="checkbox" name="cat" value="Uzak Doğu" id="catUzak" {% if 'Uzak Doğu' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">"""),
]

# Normalize content to unix line endings for easier matching if needed, but stick to direct replacement
# We will use re.sub with exact strings, escaping if needed.
# Since these are exact multiline strings, string.replace should work if indentation matches EXACTLY.
# The indentation in the file looks like spaces.

for old, new in replacements:
    # Try exact match first
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:20]}...")
    else:
        # Try normalizing whitespace
        old_norm = re.sub(r'\s+', ' ', old).strip()
        # Find where this normalized version exists in content (also normalized)? Hard.
        # Let's try to just use Regex for the parts that are resistant.
        pass

# Fallback REGEX for general cleanup of split tokens
# Pattern: {% \n if ... %} -> {% if ... %}
content = re.sub(r'\{%\s*\n\s*if', '{% if', content)
content = re.sub(r'\{%\s+if', '{% if', content)

# Fix remaining sort_order=='xxx'
content = re.sub(r"sort_order=='([^']+)'", r"sort_order == '\1'", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Comprehensive fix applied.")
