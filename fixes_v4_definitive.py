
import os
import re

file_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html'

def get_clean_sort_block():
    return """                        <div class="mb-4">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortRec" value="onerilen" {% if sort_order == 'onerilen' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortRec">Önerilen</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortPoint" value="puan" {% if sort_order == 'puan' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortPoint">Puana Göre</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortTime" value="teslimat" {% if sort_order == 'teslimat' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortTime">Teslimat Süresine Göre</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" name="sort" id="sortDiscount" value="indirim" {% if sort_order == 'indirim' %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="sortDiscount">İndirimli Olanlar</label>
                            </div>
                        </div>"""

def get_clean_cuisine_block():
    return """                        <div class="cuisine-list">
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

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # FIX 1: Replace SORT section
    # Use markers to find the block. 
    # Start: <div class="mb-4"> (inside the filter form, first one)
    # End: <hr class="text-muted opacity-25"> 
    # This is a bit risky if multiple mb-4 exists.
    # Let's rely on finding the radio inputs block via regex 'start' and 'end' patterns.
    
    # Locate the "Sırala" title, then the div after it.
    sort_title_idx = content.find('Sırala</h5>')
    if sort_title_idx != -1:
        # Find following div start
        sort_start_idx = content.find('<div class="mb-4">', sort_title_idx)
        if sort_start_idx != -1:
            # Find the end of this div? Or the separator <hr>
            sort_end_idx = content.find('<hr class="text-muted opacity-25">', sort_start_idx)
            if sort_end_idx != -1:
                # Replace the content between sort_start_idx and sort_end_idx (excluding <hr>, including div)
                # But we need to include the closing </div> of that mb-4 block. 
                # The clean block has opening and closing div.
                # So we replace from sort_start_idx to sort_end_idx.
                # Just need to check if there is an extra whitespace or something.
                
                # Careful: The search finds the start of <hr>. The text to replace ends right before <hr>.
                prefix = content[:sort_start_idx]
                suffix = content[sort_end_idx:]
                content = prefix + get_clean_sort_block() + "\n\n                        " + suffix
                print("Replaced Sort Block")

    # FIX 2: Replace CUISINE section
    # Marker: <div class="cuisine-list"> ... </form>
    cuisine_start_idx = content.find('<div class="cuisine-list">')
    if cuisine_start_idx != -1:
        cuisine_end_idx = content.find('</form>', cuisine_start_idx)
        if cuisine_end_idx != -1:
             prefix = content[:cuisine_start_idx]
             suffix = content[cuisine_end_idx:]
             content = prefix + get_clean_cuisine_block() + "\n                    " + suffix
             print("Replaced Cuisine Block")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Corrections applied to index_v2.html")

else:
    print("File not found")
