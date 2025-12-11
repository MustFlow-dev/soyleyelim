from django.contrib import admin
from django.utils.html import format_html
from .models import Restoran, Yemek, Secenek, Sikayet, RestoranBasvuru

# --- 1. RESTORAN YÖNETİMİ ---
@admin.register(Restoran)
class RestoranAdmin(admin.ModelAdmin):
    list_display = ('isim', 'aciklama_kisalt', 'resim_goster')
    search_fields = ('isim',)

    def aciklama_kisalt(self, obj):
        if obj.aciklama:
            return obj.aciklama[:50] + "..."
        return "-"
    aciklama_kisalt.short_description = "Açıklama"

    def resim_goster(self, obj):
        # Restoran logosu link mi dosya mı kontrolü
        if obj.resim_linki:
            resim_yolu = obj.resim_linki
            if hasattr(obj.resim_linki, 'url'):
                resim_yolu = obj.resim_linki.url
            return format_html('<img src="{}" style="height: 30px; border-radius: 5px;" />', resim_yolu)
        return "-"
    resim_goster.short_description = "Logo"


# --- 2. YEMEK VE SEÇENEKLERİ ---
class SecenekInline(admin.TabularInline):
    model = Secenek
    extra = 1

@admin.register(Yemek)
class YemekAdmin(admin.ModelAdmin):
    list_display = ('yemek_resmi_goster', 'isim', 'restoran', 'fiyat')
    list_filter = ('restoran',)
    search_fields = ('isim',)
    inlines = [SecenekInline]

    # --- HATA DÜZELTİLEN KISIM BURASI ---
    def yemek_resmi_goster(self, obj):
        if obj.resim:
            # Eğer resim bir dosya ise .url özelliğini al, değilse (yazıysa) direkt kendisini al
            resim_yolu = obj.resim.url if hasattr(obj.resim, 'url') else obj.resim
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 10px; object-fit: cover;" />', resim_yolu)
        return "-"
    yemek_resmi_goster.short_description = "Görsel"


# --- 3. BAŞVURU YÖNETİMİ ---
@admin.register(RestoranBasvuru)
class BasvuruAdmin(admin.ModelAdmin):
    list_display = ('restoran_adi', 'yetkili_adi', 'telefon', 'sehir', 'basvuru_tarihi')
    list_filter = ('sehir', 'basvuru_tarihi')
    search_fields = ('restoran_adi', 'yetkili_adi', 'telefon')
    ordering = ('-basvuru_tarihi',)


# --- 4. ŞİKAYET YÖNETİMİ ---
@admin.register(Sikayet)
class SikayetAdmin(admin.ModelAdmin):
    # Eğer modelinde bu alanlar yoksa hata almamak için şimdilik 'pass' geçiyoruz
    pass