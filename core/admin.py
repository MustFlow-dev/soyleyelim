from django.contrib import admin
from django.utils.html import format_html
from .models import Restoran, Yemek, Secenek, Sikayet # Secenek'i ekledik

# --- YENİ KISIM: Seçenekleri Yemeğin İçine Göm ---
class SecenekInline(admin.TabularInline):
    model = Secenek
    extra = 1 # Varsayılan olarak 1 tane boş satır göster

class YemekAdmin(admin.ModelAdmin):
    list_display = ('yemek_resmi_goster', 'isim', 'restoran', 'fiyat')
    list_filter = ('restoran',)
    search_fields = ('isim',)
    readonly_fields = ('yemek_resmi_buyuk',)
    
    # Inline yapıyı buraya ekliyoruz
    inlines = [SecenekInline] 

    fieldsets = (
        ('Yemek Bilgisi', {'fields': ('restoran', 'isim', 'fiyat', 'icerik')}),
        ('Görsel', {'fields': ('resim', 'yemek_resmi_buyuk')}),
    )
    
    # ... (Geri kalan resim fonksiyonları aynen kalsın) ...
    def yemek_resmi_goster(self, obj):
        if obj.resim:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 10px; object-fit: cover;" />', obj.resim)
        return "-"
    
    def yemek_resmi_buyuk(self, obj):
        if obj.resim:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 10px;" />', obj.resim)
        return "-"

# Diğerleri aynı kalsın
admin.site.register(Restoran) # (RestoranAdmin varsa parantez içine yaz)
admin.site.register(Yemek, YemekAdmin)
admin.site.register(Sikayet)