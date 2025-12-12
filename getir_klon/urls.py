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
    path('biz-kimiz/', views.biz_kimiz, name='biz_kimiz'),
    path('kullanim-kosullari/', views.kullanim_kosullari, name='kullanim_kosullari'),
    path('kvkk/', views.kvkk, name='kvkk'),
    path('cerez-politikasi/', views.cerez_politikasi, name='cerez_politikasi'),
    
    # --- KULLANICI GİRİŞ/ÇIKIŞ ---
    path('giris/', views.giris_yap, name='giris'),
    path('kayit/', views.kayit_ol, name='kayit'),
    path('cikis/', views.cikis_yap, name='cikis'),
    # ... (User auth URLs)
    
    # --- SEPET İŞLEMLERİ ---
    path('sepet/', views.sepet_detay, name='sepet_detay'),
    path('sepet/ekle/<int:yemek_id>/', views.sepete_ekle, name='sepete_ekle'),
    path('sepet/azalt/<int:sepet_urun_id>/', views.sepet_adet_azalt, name='sepet_adet_azalt'),
    path('sepet/sil/<int:sepet_urun_id>/', views.sepetten_cikar, name='sepetten_cikar'),
    path('sepet/bosalt/', views.sepeti_bosalt, name='sepeti_bosalt'),
    
    # --- SİPARİŞ ONAY VE TAKİP ---
    path('siparis/tamamla/', views.siparis_olustur, name='siparis_olustur'),
    path('siparis/takip/<int:id>/', views.siparis_takip, name='siparis_takip'),
    path('siparis/iletisim/<int:id>/', views.restoran_iletisim, name='restoran_iletisim'),
    path('siparis/odeme/<int:id>/', views.odeme_sayfasi, name='odeme_sayfasi'),
    # --- CANLI DESTEK ---
    path('api/chat/send/', views.chat_api_send_message, name='chat_send'),
    path('api/chat/get/', views.chat_api_get_messages, name='chat_get'),
    path('custom-admin/chat/', views.admin_chat_dashboard, name='admin_chat_dashboard'),
    path('custom-admin/chat/<str:session_id>/', views.admin_chat_detail, name='admin_chat_detail'),
    path('siparislerim/', views.siparislerim, name='siparislerim'),
    path('siparis/yorum-yap/<int:siparis_id>/', views.yorum_yap, name='yorum_yap'),
    
    # --- YENİ ÖZELLİKLER ---
    path('favori-toggle/<int:restoran_id>/', views.favori_toggle, name='favori_toggle'),
    path('favorilerim/', views.favorilerim, name='favorilerim'),
    path('sepet/kupon-uygula/', views.kupon_uygula, name='kupon_uygula'),
    
    # --- YENİ ÖZELLİKLER ---
    path('favori-toggle/<int:restoran_id>/', views.favori_toggle, name='favori_toggle'),
    path('favorilerim/', views.favorilerim, name='favorilerim'),
    path('sepet/kupon-uygula/', views.kupon_uygula, name='kupon_uygula'),

    # --- KULLANICI PROFİLİ VE KARTLAR ---
    path('kullanici-bilgileri/', views.kullanici_bilgileri, name='kullanici_bilgileri'),
    path('kayitli-kartlarim/', views.kayitli_kartlarim, name='kayitli_kartlarim'),
    path('kart-ekle/', views.kart_ekle, name='kart_ekle'),
    path('kart-sil/<int:id>/', views.kart_sil, name='kart_sil'),
]



# Resimlerin düzgün çalışması için gerekli ayar (Çok Önemli!)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)