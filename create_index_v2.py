
import os
import re

source_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index.html'
dest_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html'

def fix_content(content):
    # Fix 1: Add spaces around == in sort_order checks
    # Pattern: sort_order=='value' -> sort_order == 'value'
    content = re.sub(r"sort_order=='([^']+)'", r"sort_order == '\1'", content)
    
    # Fix 2: Fix split tags (specifically checked{% endif %})
    # This handles cases where {% is on one line and if ... is on the next
    # Regex to find {% followed by whitespace/newlines then if
    content = re.sub(r"\{%\s+\n\s+if", "{% if", content)
    
    # Also fix specific split lines in cuisine list if they exist like:
    # <input ... {%
    #    if ... %}
    # We want to join them.
    # A generic approach: find any `{%` that is part of an `if` tag inside an input and ensure single line? 
    # Actually, the specific error in cuisine list was the split `if` tag.
    # Let's fix lines like:
    # width: 100% ... {%
    # if ...
    
    # Let's target the known pattern in cuisine filters:
    # id="cat..." {%\n if ... %}
    content = re.sub(r'id="([^"]+)"\s+\{%\s*\n\s+if', r'id="\1" {% if', content)
    
    # Also fix the sort inputs just in case
    content = re.sub(r'value="([^"]+)"\s+\{%\s*\n\s+if', r'value="\1" {% if', content)

    # Clean up multiple spaces inside the tags created by join
    content = re.sub(r"\{%\s+if", "{% if", content)


    # Fix 3: Hide Banner for authenticated users
    # Find the banner div text
    banner_start = '<!-- Sticky Promo Banner (Forced Visible on Homepage) -->'
    if banner_start in content:
        # Check if already wrapped (unlikely in original index.html but possible)
        if '{% if not user.is_authenticated %}' not in content:
             content = content.replace(banner_start, banner_start + '\n    {% if not user.is_authenticated %}')
             
             # Find the end of the banner. It ends with a </div> which closes the main wrapper?
             # Looking at previous view_file, the banner ends before </body>?
             # No, it's a specific block.
             # Let's assume the banner block logic from previous attempts.
             # It ends with: "document.getElementById('sticky-promo-bar-index').remove()"></button> ... </div> ... </div>
             # Use a robust replacement if possible.
             
             # Replacing the END of the banner is harder automatically without strict parsing.
             # However, we know the banner HTML structure.
             
             # Let's look for the closing of that specific component.
             # It ends with `...document.getElementById('sticky-promo-bar-index').remove()"></button>`
             # followed by two closing divs.
             
             # We can find the closing div of the `sticky-promo-bar-index` ID?
             # Actually, simpler manual patching of the banner block if valid.
             pass 

    return content

# Read source
with open(source_path, 'r', encoding='utf-8') as f:
    raw_content = f.read()

# Apply Fixes
fixed_content = fix_content(raw_content)

# Specific Banner Injection (Manual String replace to be safe)
# Identify unique strings for start and end of banner
banner_id_str = '<div id="sticky-promo-bar-index"'
if "{% if not user.is_authenticated %}" not in fixed_content:
    if banner_id_str in fixed_content:
        # Inject start
        fixed_content = fixed_content.replace(banner_id_str, "{% if not user.is_authenticated %}\n    " + banner_id_str)
        
        # Inject end. The banner ends with the closing div of the sticky bar.
        # The sticky bar has: <div class="container...> ... </div> </div>
        # It's safer to rely on the fact that it is likely right before </body> or <script> tags for bootstrap.
        # Based on file view, it is near the end.
        
        # Let's find the closing tag.
        # We can look for the button with the remove() call.
        remove_call = "document.getElementById('sticky-promo-bar-index').remove()"
        idx = fixed_content.find(remove_call)
        if idx != -1:
            # Find the next </div> (closes button container), then next </div> (closes container), then next </div> (closes main bar)
            # This is risky. 
            pass

# RETHINKING BANNER: Use the known full block replacement if possible.
# I will overwrite the whole file with known good content if I can trust I have it.
# But `index.html` might have changes I don't see.

# BETTER PLAN: Just fix the SYNTAX errors violently.
# 1. `sort_order=='...` -> `sort_order == '...`
# 2. Join lines for the split tags.

final_content = re.sub(r"sort_order=='([^']+)'", r"sort_order == '\1'", raw_content)

# Fix split tags using a loop to be robust
lines = final_content.splitlines()
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    if stripped.endswith("{%") or stripped.endswith("{%"): # Split tag start
        # Check next line
        if i + 1 < len(lines) and "if " in lines[i+1] and "%}" in lines[i+1]:
            # Merge
            joined = line.rstrip() + " " + lines[i+1].lstrip()
            # Remove the split marker if it was just whitespace
            new_lines.append(joined)
            i += 2
            continue
    
    # Also handle the case where `{%` is alone on a line or at end of line
    # Specifically for the radio/checkbox inputs seen in diffs
    # input ... {%
    # if ... %}
    
    # Use Regex on the full string for the split tags, it's safer than line iteration
    # Pattern: {% \n whitespace if
    
    new_lines.append(line)
    i += 1

# Re-join to string for regex
final_content_str = "\n".join(new_lines)

# Regex fix for split tags:
# Matches `{%` followed by optional whitespace/newlines followed by `if`
final_content_str = re.sub(r"\{%\s*\n\s*if", "{% if", final_content_str)

# One more pass for `==` just in case
final_content_str = re.sub(r"sort_order=='([^']+)'", r"sort_order == '\1'", final_content_str)

# Banner Fix (Simple append if not present)
if "{% if not user.is_authenticated %}" not in final_content_str:
     # Locate the banner start
     start_marker = '<!-- Sticky Promo Banner (Forced Visible on Homepage) -->'
     if start_marker in final_content_str:
         final_content_str = final_content_str.replace(start_marker, "{% if not user.is_authenticated %}\n" + start_marker)
         # We need to close it. The banner is the last HTML element before scripts.
         # Locate script src bootstrap
         end_marker = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>'
         if end_marker in final_content_str:
             final_content_str = final_content_str.replace(end_marker, "{% endif %}\n    " + end_marker)

with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(final_content_str)

print("Created index_v2.html with all fixes.")
