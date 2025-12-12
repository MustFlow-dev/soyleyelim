from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Restoran, Yemek, RestoranBasvuru, Siparis, SiparisUrun, Sepet, SepetUrun, Yorum 

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
    
    # Yorumları getir
    yorumlar = Yorum.objects.filter(restoran=restoran).order_by('-tarih')
    
    # Ortalama puanı hesapla
    ortalama_puan = yorumlar.aggregate(Avg('puan'))['puan__avg']
    if ortalama_puan:
        ortalama_puan = round(ortalama_puan, 1)
    
    context = {
        'restoran': restoran,
        'yemekler': yemekler,
        'yorumlar': yorumlar,
        'ortalama_puan': ortalama_puan,
        'yorum_sayisi': yorumlar.count()
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

# --- SEPET İŞLEMLERİ ---

from .models import Sepet, SepetUrun
import uuid

def _get_cart(request):
    """
    Kullanıcının sepetini getirir veya oluşturur.
    Kullanıcı giriş yapmışsa user ile, yapmamışsa session_id ile eşleştirir.
    """
    if request.user.is_authenticated:
        # Kullanıcı giriş yaptıysa sepeti user ile al
        sepet, created = Sepet.objects.get_or_create(user=request.user)
    else:
        # Anonim kullanıcı işlemleri
        session_id = request.session.get('cart_session_id')
        if not session_id:
            # Session ID yoksa oluştur
            session_id = str(uuid.uuid4())
            request.session['cart_session_id'] = session_id
        
        sepet, created = Sepet.objects.get_or_create(session_id=session_id)
    return sepet

def sepete_ekle(request, yemek_id):
    yemek = get_object_or_404(Yemek, id=yemek_id)
    sepet = _get_cart(request)
    
    # Ürün zaten sepette varsa adeti arttır
    sepet_urun, created = SepetUrun.objects.get_or_create(sepet=sepet, yemek=yemek)
    
    if not created:
        sepet_urun.adet += 1
        sepet_urun.save()
        messages.success(request, f"{yemek.isim} sepetinize eklendi. (Adet: {sepet_urun.adet})")
    else:
        messages.success(request, f"{yemek.isim} sepetinize eklendi.")
    
    # Geldiği sayfaya geri dön (HTTP_REFERER header'ından)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('restoran_detay', id=yemek.restoran.id)

def sepet_detay(request):
    sepet = _get_cart(request)
    sepet_urunleri = SepetUrun.objects.filter(sepet=sepet)
    
    context = {
        'sepet': sepet,
        'sepet_urunleri': sepet_urunleri,
        'toplam_tutar': sepet.toplam_tutar()
    }
    return render(request, 'core/sepet.html', context)

def sepetten_cikar(request, sepet_urun_id):
    sepet_urun = get_object_or_404(SepetUrun, id=sepet_urun_id)
    
    # Güvenlik kontrolü: Kullanıcı sadece kendi sepetindeki ürünü silebilir mi?
    # Basit bir kontrol ekleyelim:
    current_cart = _get_cart(request)
    if sepet_urun.sepet != current_cart:
        messages.error(request, "Bu işlemi yapmaya yetkiniz yok.")
        return redirect('sepet_detay')

    yemek_isim = sepet_urun.yemek.isim
    sepet_urun.delete()
    messages.info(request, f"{yemek_isim} sepetten çıkarıldı.")
    return redirect('sepet_detay')

def sepeti_bosalt(request):
    sepet = _get_cart(request)
    sepet.sepeturun_set.all().delete()
    messages.info(request, "Sepetiniz boşaltıldı.")
    return redirect('sepet_detay')

# --- SİPARİŞ İŞLEMLERİ ---

from .models import Siparis, SiparisUrun

def siparis_olustur(request):
    sepet = _get_cart(request)
    sepet_urunleri = SepetUrun.objects.filter(sepet=sepet)
    
    if not sepet_urunleri.exists():
        messages.warning(request, "Sepetiniz boş, sipariş oluşturamazsınız.")
        return redirect('index')

    if request.method == 'POST':
        # Form verilerini al
        ad_soyad = request.POST.get('ad_soyad')
        telefon = request.POST.get('telefon')
        adres = request.POST.get('adres')
        adres_tarifi = request.POST.get('adres_tarifi', '')

        # Sipariş Kaydı Oluştur
        siparis = Siparis.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ad_soyad=ad_soyad,
            telefon=telefon,
            adres=adres,
            adres_tarifi=adres_tarifi,
            toplam_tutar=sepet.toplam_tutar()
        )

        # Sepetteki ürünleri Sipariş Ürünlerine dönüştür
        for urun in sepet_urunleri:
            SiparisUrun.objects.create(
                siparis=siparis,
                yemek=urun.yemek,
                adet=urun.adet,
                fiyat=urun.yemek.fiyat # O anki fiyatı kaydediyoruz
            )

        # Sepeti Temizle
        sepet_urunleri.delete()
        
        # Başarılı -> Takip Sayfasına Git
        # messages.success(request, "Siparişiniz başarıyla alındı!")
        return redirect('siparis_takip', id=siparis.id)

    # GET isteği ise özet bilgi ve form sayfasını göster
    context = {
        'sepet': sepet,
        'sepet_urunleri': sepet_urunleri,
        'toplam_tutar': sepet.toplam_tutar()
    }
    return render(request, 'core/siparis_olustur.html', context)

def siparis_takip(request, id):
    siparis = get_object_or_404(Siparis, id=id)
    siparis_urunleri = SiparisUrun.objects.filter(siparis=siparis)
    
    # Restoran bilgisini al (ilk üründen)
    restoran = None
    if siparis_urunleri.exists():
        restoran = siparis_urunleri.first().yemek.restoran

    context = {
        'siparis': siparis,
        'siparis_urunleri': siparis_urunleri,
        'restoran': restoran
    }
    return render(request, 'core/siparis_takip.html', context)

def restoran_iletisim(request, id):
    siparis = get_object_or_404(Siparis, id=id)
    # Siparişten restorana ulaşmamız lazım. Şimdilik ilk ürünün restoranını alıyoruz.
    # Gerçek senaryoda Sipariş modelinde restoran FK olması daha doğru olurdu.
    siparis_urun = SiparisUrun.objects.filter(siparis=siparis).first()
    restoran = siparis_urun.yemek.restoran if siparis_urun else None
    
    return render(request, 'core/restoran_iletisim.html', {'restoran': restoran})

def odeme_sayfasi(request, id):
    siparis = get_object_or_404(Siparis, id=id)
    if request.method == 'POST':
        # Ödeme işlemi burada yapılır (Simülasyon)
        messages.success(request, 'Siparişiniz başarıyla oluşturuldu! Lezzet yola çıkıyor. 🛵')
        return redirect('index')

    return render(request, 'core/odeme.html', {'siparis': siparis})




@login_required
def siparislerim(request):
    siparisler = Siparis.objects.filter(user=request.user).order_by('-olusturma_tarihi')
    return render(request, 'core/siparislerim.html', {'siparisler': siparisler})

@login_required
def yorum_yap(request, siparis_id):
    if request.method == 'POST':
        siparis = get_object_or_404(Siparis, id=siparis_id, user=request.user)
        
        # Sadece teslim edilen siparişlere yorum yapılabilir
        if siparis.durum != 'teslim_edildi':
            messages.error(request, 'Sadece teslim edilen siparişleri değerlendirebilirsiniz.')
            return redirect('siparislerim')

        # Daha önce yorum yapılmış mı?
        if hasattr(siparis, 'yorum'):
            messages.warning(request, 'Bu sipariş için zaten yorum yaptınız.')
            return redirect('siparislerim')

        puan = request.POST.get('puan')
        yorum_metni = request.POST.get('yorum')
        restoran = siparis.siparisurun_set.first().yemek.restoran

        Yorum.objects.create(
            siparis=siparis,
            restoran=restoran,
            user=request.user,
            puan=puan,
            yorum=yorum_metni
        )
        
        messages.success(request, 'Değerlendirmeniz için teşekkürler!')
        return redirect('siparislerim')
    
    return redirect('index')
