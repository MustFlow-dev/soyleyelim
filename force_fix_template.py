
import os

file_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_fixed.html'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the bad block and the good block
    bad_block = """                        <div class="mb-4">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortRec" value="onerilen"
                                    {% if sort_order=='onerilen' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortRec">Önerilen</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" {%
                                    if sort_order=='puan' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortPoint">Puana Göre</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortTime" value="teslimat"
                                    {% if sort_order=='teslimat' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortTime">Teslimat Süresine Göre</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortDiscount"
                                    value="indirim" {% if sort_order=='indirim' %}checked{% endif %}
                                    onchange="this.form.submit()">
                                <label class="form-check-label" for="sortDiscount">İndirimli Olanlar</label>
                            </div>
                        </div>"""

    good_block = """                        <div class="mb-4">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortRec" value="onerilen" 
                                    {% if sort_order == 'onerilen' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortRec">Önerilen</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" 
                                    {% if sort_order == 'puan' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortPoint">Puana Göre</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortTime" value="teslimat" 
                                    {% if sort_order == 'teslimat' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortTime">Teslimat Süresine Göre</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortDiscount" 
                                    value="indirim" {% if sort_order == 'indirim' %}checked{% endif %} 
                                    onchange="this.form.submit()">
                                <label class="form-check-label" for="sortDiscount">İndirimli Olanlar</label>
                            </div>
                        </div>"""
    
    # Try direct replacement
    if bad_block in content:
        new_content = content.replace(bad_block, good_block)
        print("Found exact block match. Replacing.")
    else:
        # Fallback: Replace individual lines if block doesn't match (e.g. whitespace diffs)
        print("Block match failed. Trying iterative replacement.")
        new_content = content
        replacements = [
            ("sort_order=='onerilen'", "sort_order == 'onerilen'"),
            ("sort_order=='puan'", "sort_order == 'puan'"),
            ("sort_order=='teslimat'", "sort_order == 'teslimat'"),
            ("sort_order=='indirim'", "sort_order == 'indirim'"),
            ('value="puan" {%\n                                    if', 'value="puan" {% if') # Fixing split tag
        ]
        for old, new in replacements:
            new_content = new_content.replace(old, new)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated index_fixed.html")
    else:
        print("No changes made. Content might already be correct or matching failed.")

else:
    print(f"File not found: {file_path}")
