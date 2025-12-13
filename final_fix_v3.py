
import os

file_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the correctly formatted cuisine list block
    clean_cuisine_block = """<div class="cuisine-list">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="catAll" {% if not secili_kategoriler %}checked{% endif %} onclick="selectCategory('')">
                                <label class="form-check-label fw-bold" for="catAll">Tümü</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Burger" id="catBurger" {% if 'Burger' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catBurger">Burger</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Döner" id="catDoner" {% if 'Döner' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catDoner">Döner</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Pizza" id="catPizza" {% if 'Pizza' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catPizza">Pizza</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Kebap" id="catKebap" {% if 'Kebap' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catKebap">Kebap & Türk Mutfağı</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Tavuk" id="catTavuk" {% if 'Tavuk' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catTavuk">Tavuk Dünyası</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Tatlı" id="catTatli" {% if 'Tatlı' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catTatli">Tatlı & Pastane</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Pide" id="catPide" {% if 'Pide' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catPide">Pide & Lahmacun</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Çiğ Köfte" id="catCigkofte" {% if 'Çiğ Köfte' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catCigkofte">Çiğ Köfte</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Uzak Doğu" id="catUzak" {% if 'Uzak Doğu' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catUzak">Uzak Doğu</label>
                            </div>
                        </div>"""

    # We need to find the existing cuisine-list block and replace it.
    # Since the content might be messy with split lines, regex or finding start/end markers is best.
    
    start_marker = '<div class="cuisine-list">'
    end_marker = '</form>' # The form closes right after
    
    start_idx = content.find(start_marker)
    if start_idx != -1:
        end_idx = content.find(end_marker, start_idx)
        if end_idx != -1:
            # Construct new content
            # Preserve content before start_marker
            prefix = content[:start_idx]
            # Preserve content after end_marker (inclusive of end_marker?) No, we replace up to end_marker
            suffix = content[end_idx:]
            
            new_content = prefix + clean_cuisine_block + "\n                        " + suffix
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully matched and replaced cuisine-list block.")
        else:
            print("Could not find end marker for cuisine block.")
    else:
        print("Could not find start marker for cuisine block.")

else:
    print("index_v2.html not found.")
