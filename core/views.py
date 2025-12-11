from django.shortcuts import render, redirect, get_object_or_404
from .models import Restoran, Yemek, Secenek, Sikayet
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# --- ANA SAYFA ---
def index(request):
    # Tüm restoranları veritabanından çek
    restoranlar = Restoran.objects.all()
    context = {
        'restoranlar': restoranlar
    }
    return render(request, 'core/index.html', context)

# --- RESTORAN MENÜ SAYFASI ---
def restoran_detay(request, id):
    secilen_restoran = get_object_or_404(Restoran, id=id)
    yemekler = Yemek.objects.filter(restoran=secilen_restoran)
    
    return render(request, 'core/detay.html', {
        'restoran': secilen_restoran, 
        'yemekler': yemekler
    })

# --- SİPARİŞ ONAY VE HESAPLAMA ---
def siparis_onay(request, restoran_id, yemek_id):
    secilen_restoran = get_object_or_404(Restoran, id=restoran_id)
    secilen_yemek = get_object_or_404(Yemek, id=yemek_id)
    
    # Kullanıcının seçtiği ekstra malzemelerin ID'lerini alıyoruz (HTML formundan 'ekstra' adıyla gelir)
    secilen_ekstra_idler = request.GET.getlist('ekstra') 
    
    # Veritabanından bu ekstraları bul
    secilen_ekstralar = Secenek.objects.filter(id__in=secilen_ekstra_idler)
    
    # Toplam fiyatı hesapla (Yemek Fiyatı + Seçilen Ekstralar)
    ekstra_toplam = sum(ekstra.fiyat for ekstra in secilen_ekstralar)
    genel_toplam = secilen_yemek.fiyat + ekstra_toplam

    return render(request, 'core/siparis_onay.html', {
        'restoran': secilen_restoran, 
        'yemek': secilen_yemek,
        'ekstralar': secilen_ekstralar, # Fişte göstermek için sayfaya gönderiyoruz
        'toplam_fiyat': genel_toplam
    })

# --- ŞİKAYET ETME ---
def sikayet_et(request, restoran_id):
    secilen_restoran = get_object_or_404(Restoran, id=restoran_id)
    basarili = False # Form gönderilince True olacak

    if request.method == 'POST':
        # Formdan gelen verileri al
        ad = request.POST.get('ad_soyad')
        konu = request.POST.get('konu')
        mesaj = request.POST.get('mesaj')
        
        # Veritabanına kaydet
        Sikayet.objects.create(
            restoran=secilen_restoran,
            ad_soyad=ad,
            konu=konu,
            mesaj=mesaj
        )
        basarili = True # Başarılı mesajını tetikle

    return render(request, 'core/sikayet_et.html', {
        'restoran': secilen_restoran,
        'basarili': basarili
    })

# --- KULLANICI İŞLEMLERİ (Giriş/Çıkış/Kayıt) ---

def kayit_ol(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Kayıt olunca direkt giriş yap
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'core/kayit.html', {'form': form})

def giris_yap(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/giris.html', {'form': form})

def cikis_yap(request):
    logout(request)
    return redirect('index')
# Dosyanın en altına ekle:

def yemek_detay(request, yemek_id):
    secilen_yemek = get_object_or_404(Yemek, id=yemek_id)
    secilen_restoran = secilen_yemek.restoran 
    
    return render(request, 'core/yemek_detay.html', {
        'yemek': secilen_yemek,
        'restoran': secilen_restoran
    })