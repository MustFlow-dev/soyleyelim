from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Restoran, Yemek, RestoranBasvuru 

# --- ANASAYFA ---
def index(request):
    restoranlar = Restoran.objects.all()
    context = {
        'restoranlar': restoranlar
    }
    return render(request, 'core/index.html', context)

# --- RESTORAN DETAY ---
def restoran_detay(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    yemekler = Yemek.objects.filter(restoran=restoran)
    
    context = {
        'restoran': restoran,
        'yemekler': yemekler
    }
    return render(request, 'core/detay.html', context)

# --- YEMEK DETAY ---
def yemek_detay(request, id):
    yemek = get_object_or_404(Yemek, id=id)
    restoran = yemek.restoran
    
    context = {
        'yemek': yemek,
        'restoran': restoran
    }
    return render(request, 'core/yemek_detay.html', context)

# --- SİPARİŞ ONAY ---
def siparis_onay(request, restoran_id, yemek_id):
    restoran = get_object_or_404(Restoran, id=restoran_id)
    yemek = get_object_or_404(Yemek, id=yemek_id)
    
    # Ekstra malzemeler ve fiyat hesaplama mantığı (Basit Hali)
    toplam_fiyat = yemek.fiyat
    
    context = {
        'restoran': restoran,
        'yemek': yemek,
        'toplam_fiyat': toplam_fiyat
    }
    return render(request, 'core/siparis_onay.html', context)

# --- ŞİKAYET ET ---
def sikayet_et(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    
    if request.method == 'POST':
        # Buraya şikayet kaydetme kodları gelecek
        # Örn: Sikayet.objects.create(...)
        messages.success(request, 'Şikayetiniz başarıyla iletildi.')
        return render(request, 'core/sikayet_et.html', {'restoran': restoran, 'basarili': True})
        
    return render(request, 'core/sikayet_et.html', {'restoran': restoran})

# --- PARTNER (RESTORAN BAŞVURUSU) ---
def partner(request):
    if request.method == 'POST':
        # Formdan verileri al
        restoran_adi = request.POST.get('restoran_adi')
        yetkili_adi = request.POST.get('yetkili_adi')
        telefon = request.POST.get('telefon')
        email = request.POST.get('email')
        sehir = request.POST.get('sehir')
        kvkk = request.POST.get('kvkk') == 'on' # Checkbox işaretli mi?

        # Veritabanına kaydet
        yeni_basvuru = RestoranBasvuru(
            restoran_adi=restoran_adi,
            yetkili_adi=yetkili_adi,
            telefon=telefon,
            email=email,
            sehir=sehir,
            kvkk_onayi=kvkk
        )
        yeni_basvuru.save()

        # Başarı mesajı ver ve sayfayı yenile
        messages.success(request, 'Başvurunuz başarıyla alındı! Ekibimiz en kısa sürede size ulaşacak.')
        return redirect('partner')

    return render(request, 'core/partner.html')

# --- KULLANICI İŞLEMLERİ (GİRİŞ/ÇIKIŞ) ---
def giris_yap(request):
    # Giriş kodların buradaysa kalabilir (Şu an sadece template render ediyor)
    return render(request, 'core/giris.html')

def kayit_ol(request):
    # Kayıt kodların buradaysa kalabilir (Şu an sadece template render ediyor)
    return render(request, 'core/kayit.html')

def cikis_yap(request):
    logout(request)
    return redirect('index')

# --- RESTORAN ARAMA (DÜZELTİLDİ) ---
# --- RESTORAN ARAMA (İLETİŞİM SAYFASI) ---
def restoran_ara(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    
    # Redirect yerine render kullanıyoruz.
    # 'core/iletisim.html' senin az önce attığın HTML dosyasının adı olmalı.
    return render(request, 'core/iletisim.html', {'restoran': restoran})