
import os

views_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\core\\views.py'
urls_path = r'c:\\Users\\cagat\\Desktop\\Phyton\\soyleyelim\\Soyleyelim\\urls.py'

# 1. Update core/views.py
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

# Add imports if missing
if 'import json' not in views_content:
    views_content = "import json\n" + views_content
if 'from django.http import JsonResponse' not in views_content:
    views_content = "from django.http import JsonResponse\n" + views_content

# Add update_cart_item function if not exists
api_code = """
def update_cart_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            action = data.get('action') # 'increase' or 'decrease'

            sepet_urun = get_object_or_404(SepetUrun, id=item_id)
            sepet = _get_cart(request)
            
            # Security check
            if sepet_urun.sepet != sepet:
                 return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

            if action == 'increase':
                sepet_urun.adet += 1
                sepet_urun.save()
            elif action == 'decrease':
                if sepet_urun.adet > 1:
                    sepet_urun.adet -= 1
                    sepet_urun.save()
                else:
                    sepet_urun.delete()

            # Recalculate totals
            sepet_toplam = sepet.toplam_tutar()
            item_toplam = sepet_urun.toplam_fiyat() if sepet_urun.id else 0
            
            return JsonResponse({
                'status': 'success', 
                'new_quantity': sepet_urun.adet if sepet_urun.id else 0,
                'item_total': item_toplam,
                'cart_total': sepet_toplam
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error'}, status=400)
"""

if 'def update_cart_item(request):' not in views_content:
    views_content += "\n" + api_code
    print("Added update_cart_item to views.py")
else:
    print("update_cart_item already in views.py")

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)


# 2. Update Soyleyelim/urls.py
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

url_pattern = "path('api/cart/update/', views.update_cart_item, name='api_cart_update'),"

if 'api/cart/update/' not in urls_content:
    # Insert before the closing ]
    if 'urlpatterns = [' in urls_content:
        # Find the last ]
        last_bracket_index = urls_content.rfind(']')
        if last_bracket_index != -1:
            urls_content = urls_content[:last_bracket_index] + "    " + url_pattern + "\n" + urls_content[last_bracket_index:]
            print("Added URL pattern to urls.py")
else:
    print("URL pattern already in urls.py")

with open(urls_path, 'w', encoding='utf-8') as f:
    f.write(urls_content)
