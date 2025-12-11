from django.contrib import admin
from core import views
from django.urls import path
# Bütün görünümleri (view) tek seferde, hatasız çağırıyoruz:
from core.views import (
    index, restoran_detay, giris_yap, kayit_ol, cikis_yap, 
    siparis_onay, sikayet_et, yemek_detay  # <--- YENİ EKLENDİ
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    
    # Restoran ve Menü
    path('restoran/<int:id>/', restoran_detay, name='restoran_detay'),
    
    # Kullanıcı İşlemleri
    path('giris/', giris_yap, name='giris'),
    path('kayit/', kayit_ol, name='kayit'),
    path('cikis/', cikis_yap, name='cikis'),
    
    # Sipariş ve Şikayet (YENİLER)
    path('siparis-onay/<int:restoran_id>/<int:yemek_id>/', siparis_onay, name='siparis_onay'),
    path('sikayet-et/<int:restoran_id>/', sikayet_et, name='sikayet_et'),
    path('yemek/<int:yemek_id>/', yemek_detay, name='yemek_detay'),
    path('restoran-ara/<int:restoran_id>/', views.restoran_ara, name='restoran_ara'),
]
