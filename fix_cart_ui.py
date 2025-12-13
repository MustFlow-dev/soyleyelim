
import os
import re

files_to_fix = [
    r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\base.html',
    r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\index_v2.html',
    r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\templates\\core\\yemek_detay.html'
]

# Replacement configurations
# 1. Correct Item Name and Image
# Old: item.urun.isim -> item.yemek.isim
# Old: item.urun.resim.url -> item.yemek.resim (because it's CharField)
# Old: item.urun.resim -> item.yemek.resim (for check)

def fix_item_fields(content):
    content = content.replace('item.urun.isim', 'item.yemek.isim')
    content = content.replace('item.urun.resim.url', 'item.yemek.resim')
    content = content.replace('item.urun.resim', 'item.yemek.resim')
    
    # 2. Quantity Controls
    # Target: <div class="quantity-control ..."> ... <span ...>{{ item.adet }} adet</span> ... </div>
    # We want to replace the whole quantity control div or inner part.
    
    # Let's find the quantity control block using regex to be safe
    # It looks roughly like:
    # <div class="quantity-control bg-light rounded-pill px-2 py-1 d-flex align-items-center">
    #     <span class="text-dark fw-bold small">{{ item.adet }} adet</span>
    # </div>
    
    # New content:
    new_quantity_control = """
                                <div class="quantity-control bg-light rounded-pill px-2 py-1 d-flex align-items-center bg-white border">
                                    <button class="btn btn-sm btn-link text-decoration-none p-0 text-muted" onclick="updateCartItem({{ item.id }}, 'decrease')">
                                        <i class="fas fa-minus small"></i>
                                    </button>
                                    <span class="text-dark fw-bold small mx-2" id="q-{{ item.id }}">{{ item.adet }}</span>
                                    <button class="btn btn-sm btn-link text-decoration-none p-0 text-orange" onclick="updateCartItem({{ item.id }}, 'increase')" style="color: #ff6b00;">
                                        <i class="fas fa-plus small"></i>
                                    </button>
                                </div>
    """
    
    # We use a regex to find the old block.
    # Pattern: <div class="quantity-control[^>]*>.*?{{ item.adet }} adet.*?</div>
    # Note: re.DOTALL is needed.
    
    pattern = re.compile(r'<div class="quantity-control[^>]*>.*?{{ item\.adet }} adet.*?</div>', re.DOTALL)
    
    # Only replace if we haven't already added buttons (look for updateCartItem)
    if 'updateCartItem' not in content:
        content = pattern.sub(new_quantity_control.strip(), content)
        print("Updated quantity controls.")
    else:
        print("Quantity controls already updated.")

    return content

# 3. Add JavaScript
js_code = """
    <script>
        function updateCartItem(itemId, action) {
            fetch('/api/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    'item_id': itemId,
                    'action': action
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update Quantity Display
                    const qSpan = document.getElementById('q-' + itemId);
                    if (qSpan) {
                         if (data.new_quantity > 0) {
                            qSpan.innerText = data.new_quantity;
                         } else {
                            // Item removed, reload page or remove element
                            // Checking if it was the last item?
                            location.reload(); 
                         }
                    } else {
                        // If span not found (maybe reload needed)
                         location.reload();
                    }
                    
                    // Update Total Price (id needed for total price span)
                    // We need to add ID to total price span in the template first
                    const totalSpan = document.getElementById('cart-total-price');
                    if (totalSpan) {
                        totalSpan.innerText = data.cart_total + ' ₺';
                    } else {
                        // If we didn't add id yet, good fallback is reload on total change or just reload for simplicity
                        // But let's try to update text content if we can find it
                         location.reload(); 
                    }
                } else {
                    alert('Hata: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
"""

def add_js_and_ids(content):
    # Add ID to total price span
    # Old: <span class="fs-4 fw-bold text-dark">{{ global_sepet_tutar }} ₺</span>
    # New: <span class="fs-4 fw-bold text-dark" id="cart-total-price">{{ global_sepet_tutar }} ₺</span>
    if 'id="cart-total-price"' not in content:
        content = content.replace(
            '{{ global_sepet_tutar }} ₺</span>', 
            '<span id="cart-total-price">{{ global_sepet_tutar }} ₺</span>'
        ).replace('<span class="fs-4 fw-bold text-dark"><span id="cart-total-price">', '<span class="fs-4 fw-bold text-dark" id="cart-total-price">')
        # Clean up double spans if replaced awkwardly
        content = content.replace('<span class="fs-4 fw-bold text-dark"><span id="cart-total-price">', '<span class="fs-4 fw-bold text-dark" id="cart-total-price">')
    
    # Append JS before end of body/offcanvas
    if 'function updateCartItem' not in content:
        if '</body>' in content:
            content = content.replace('</body>', js_code + '\n</body>')
            print("Added JS code.")
    
    return content

for path in files_to_fix:
    if os.path.exists(path):
        print(f"Processing {path}...")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = fix_item_fields(content)
        content = add_js_and_ids(content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")
    else:
        print(f"File not found: {path}")

