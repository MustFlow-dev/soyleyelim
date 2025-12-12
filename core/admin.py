from django.contrib import admin
from django.utils.html import format_html
from .models import Restoran, Yemek, Secenek, Sikayet, RestoranBasvuru, Siparis, SiparisUrun, Sepet, SepetUrun, Yorum

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
    pass


# --- 5. SİPARİŞ ve SEPET YÖNETİMİ ---
from .models import Sepet, SepetUrun, Siparis, SiparisUrun

class SiparisUrunInline(admin.TabularInline):
    model = SiparisUrun
    extra = 0
    can_delete = False

@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_soyad', 'telefon', 'toplam_tutar', 'durum', 'olusturma_tarihi')
    list_editable = ('durum',)
    list_filter = ('durum', 'olusturma_tarihi')
    search_fields = ('ad_soyad', 'telefon', 'adres')
    inlines = [SiparisUrunInline]

class SepetUrunInline(admin.TabularInline):
    model = SepetUrun
    extra = 0

@admin.register(Sepet)
class SepetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'olusturma_tarihi')
    inlines = [SepetUrunInline]

@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restoran', 'puan', 'tarih')
    list_filter = ('puan', 'tarih')
    search_fields = ('user__username', 'restoran__isim', 'yorum')
