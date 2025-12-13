
import os
import re

base_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\base.html'
index_v2_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html'

offcanvas_html = """
    <!-- Cart Offcanvas Sidebar Global -->
    <div class="offcanvas offcanvas-end rounded-start-4 border-0 shadow-lg" tabindex="-1" id="cartOffcanvas"
        aria-labelledby="cartOffcanvasLabel" style="width: 400px; background-color: #fcfcfc;">
        <div class="offcanvas-header border-bottom bg-white py-3">
            <h5 class="offcanvas-title fw-bold text-dark" id="cartOffcanvasLabel">
                <i class="fas fa-shopping-basket me-2" style="color: #ff6b00;"></i>Sepetim
            </h5>
            <button type="button" class="btn-close text-reset shadow-none" data-bs-dismiss="offcanvas"
                aria-label="Close"></button>
        </div>
        <div class="offcanvas-body p-0 d-flex flex-column h-100">
            {% if global_sepet_adet > 0 %}
            <div class="flex-grow-1 overflow-auto p-3">
                {% for item in global_sepet_ogeleri %}
                <div class="card mb-3 border-0 shadow-sm rounded-3 overflow-hidden animate__animated animate__fadeInUp">
                    <div class="card-body p-3 d-flex align-items-center">
                        <div class="bg-light rounded-3 d-flex align-items-center justify-content-center me-3"
                            style="width: 64px; height: 64px; flex-shrink: 0;">
                            {% if item.urun.resim %}
                            <img src="{{ item.urun.resim.url }}" alt="{{ item.urun.isim }}" class="img-fluid rounded-3"
                                style="width: 100%; height: 100%; object-fit: cover;">
                            {% else %}
                            <i class="fas fa-utensils text-secondary fa-lg"></i>
                            {% endif %}
                        </div>

                        <div class="flex-grow-1">
                            <h6 class="fw-bold mb-1 text-dark text-truncate" style="max-width: 160px;">{{ item.urun.isim }}</h6>
                            <div class="d-flex align-items-center justify-content-between">
                                <span class="fw-bold small" style="color: #ff6b00;">{{ item.toplam_fiyat }} ₺</span>
                                <div class="quantity-control bg-light rounded-pill px-2 py-1 d-flex align-items-center">
                                    <span class="text-dark fw-bold small">{{ item.adet }} adet</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div class="border-top bg-white p-4 shadow-top z-index-10">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="text-muted small fw-bold text-uppercase">Toplam Tutar</span>
                    <span class="fs-4 fw-bold text-dark">{{ global_sepet_tutar }} ₺</span>
                </div>
                <a href="{% url 'sepet_detay' %}" class="btn w-100 py-3 rounded-pill fw-bold shadow-sm hover-elevate text-white" style="background-color: #ff6b00; border-color: #ff6b00;">
                    Sepeti Onayla <i class="fas fa-arrow-right ms-2"></i>
                </a>
            </div>

            {% else %}
            <div class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center p-4">
                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center mb-4 heart-beat-anim"
                    style="width: 120px; height: 120px;">
                    <i class="fas fa-shopping-basket fa-4x opacity-50" style="color: #ff6b00;"></i>
                </div>
                <h5 class="fw-bold text-dark mb-2">Sepetiniz Boş</h5>
                <p class="text-muted small mb-4" style="max-width: 250px;">
                    Lezzetli yiyecekler sizi bekliyor! Hemen restoranları keşfetmeye başlayın.
                </p>
                <button type="button" class="btn rounded-pill px-4 py-2 fw-medium"
                    data-bs-dismiss="offcanvas" style="color: #ff6b00; border-color: #ff6b00;">
                    Alışverişe Başla
                </button>
            </div>
            {% endif %}
        </div>
    </div>

    <style>
        .hover-elevate { transition: transform 0.2s, box-shadow 0.2s; }
        .hover-elevate:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255, 107, 0, 0.3) !important; }
        .shadow-top { box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05); }
        @keyframes heartBeat { 0% { transform: scale(1); } 14% { transform: scale(1.1); } 28% { transform: scale(1); } 42% { transform: scale(1.1); } 70% { transform: scale(1); } }
        .heart-beat-anim:hover { animation: heartBeat 1.3s ease-in-out infinite; }
    </style>
"""

# ----------------- MODIFY BASE.HTML -----------------
with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

# 1. Update Cart Button in Base
base_content = base_content.replace(
    'href="{% url \'sepet_detay\' %}"', 
    'href="javascript:void(0)" data-bs-toggle="offcanvas" data-bs-target="#cartOffcanvas" aria-controls="cartOffcanvas"'
)

# 2. Append Offcanvas HTML before end of body
if '<!-- Cart Offcanvas Sidebar Global -->' not in base_content:
    if '</body>' in base_content:
        base_content = base_content.replace('</body>', offcanvas_html + '\n</body>')
    else:
        print("Warning: </body> not found in base.html")

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_content)
print("Updated base.html")

# ----------------- CLEAN INDEX_V2.HTML -----------------
# We need to remove the offcanvas from index_v2 since it's now in base.
with open(index_v2_path, 'r', encoding='utf-8') as f:
    v2_content = f.read()

# Remove the previously added offcanvas block
start_marker = '<!-- Cart Offcanvas Sidebar -->'
end_marker = '<!-- Live Support Integration -->'

start_idx = v2_content.find(start_marker)
# Find the next marker or just rely on the structure
# The previous script inserted it before '<!-- Live Support Integration -->'
# So we can remove everything between start_marker and '<!-- Live Support Integration -->'
if start_idx != -1:
    end_idx = v2_content.find(end_marker, start_idx)
    if end_idx != -1:
        # Keep end_marker
        v2_content = v2_content[:start_idx] + v2_content[end_idx:]
        
        with open(index_v2_path, 'w', encoding='utf-8') as f:
            f.write(v2_content)
        print("Cleaned index_v2.html")
    else:
        print("Could not find end marker in index_v2.html")
else:
    print("Could not find start marker in index_v2.html (maybe already clean?)")
