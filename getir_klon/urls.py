from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# En temiz yöntem: views dosyasını bir bütün olarak çağırıyoruz
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- ANASAYFA ---
    path('', views.index, name='index'),
    
    # --- RESTORAN & YEMEK DETAYLARI ---
    # Restoran detay sayfası
    path('restoran/<int:id>/', views.restoran_detay, name='restoran_detay'),
    # Yemek detay sayfası
    path('yemek/<int:id>/', views.yemek_detay, name='yemek_detay'),
    
    # --- İŞLEMLER (ARAMA, SİPARİŞ, ŞİKAYET) ---
    # Restoranı Ara Butonu için (Senin istediğin kısım)
    path('restoran-ara/<int:id>/', views.restoran_ara, name='restoran_ara'),
    # Sipariş Onay Sayfası
    path('siparis/<int:restoran_id>/<int:yemek_id>/', views.siparis_onay, name='siparis_onay'),
    # Şikayet Etme Sayfası
    path('sikayet/<int:id>/', views.sikayet_et, name='sikayet_et'),
    
    # --- KURUMSAL ---
    # Restoran Başvurusu (Partner)
    path('partner/', views.partner, name='partner'),
    
    # --- KULLANICI GİRİŞ/ÇIKIŞ ---
    path('giris/', views.giris_yap, name='giris'),
    path('kayit/', views.kayit_ol, name='kayit'),
    path('cikis/', views.cikis_yap, name='cikis'),
]

# Resimlerin düzgün çalışması için gerekli ayar (Çok Önemli!)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)