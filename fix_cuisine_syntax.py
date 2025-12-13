
import os

file_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_fixed.html'

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will construct a new content by replacing the entire cuisine-list block
    # This is more robust than finding exact bad strings if they vary
    
    # Identify the start and end of the cuisine-list block
    start_marker = '<div class="cuisine-list">'
    end_marker = '</form>' # The form closes right after the list
    
    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)
    
    if start_index != -1 and end_index != -1:
        prefix = content[:start_index]
        suffix = content[end_index:]
        
        # New clean block
        new_block = """<div class="cuisine-list">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="catAll" {% if not secili_kategoriler %}checked{% endif %} onclick="selectCategory('')">
                                <label class="form-check-label fw-bold" for="catAll">Tümü</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Burger" id="catBurger" 
                                    {% if 'Burger' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catBurger">Burger</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Döner" id="catDoner" 
                                    {% if 'Döner' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catDoner">Döner</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Pizza" id="catPizza" 
                                    {% if 'Pizza' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catPizza">Pizza</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Kebap" id="catKebap" 
                                    {% if 'Kebap' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catKebap">Kebap & Türk Mutfağı</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Tavuk" id="catTavuk" 
                                    {% if 'Tavuk' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catTavuk">Tavuk Dünyası</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Tatlı" id="catTatli" 
                                    {% if 'Tatlı' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catTatli">Tatlı & Pastane</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Pide" id="catPide" 
                                    {% if 'Pide' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catPide">Pide & Lahmacun</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Çiğ Köfte" id="catCigkofte" 
                                    {% if 'Çiğ Köfte' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catCigkofte">Çiğ Köfte</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" name="cat" value="Uzak Doğu" id="catUzak" 
                                    {% if 'Uzak Doğu' in secili_kategoriler %}checked{% endif %} onchange="this.form.submit()">
                                <label class="form-check-label" for="catUzak">Uzak Doğu</label>
                            </div>
                        </div>
                        """
        
        new_content = prefix + new_block + suffix
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully replaced cuisine-list block in index_fixed.html")
        
    else:
        print("Could not find cuisine-list block markers")

else:
    print(f"File not found: {file_path}")
