from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from .models import Restoran, Yemek, RestoranBasvuru, Siparis, SiparisUrun, Sepet, SepetUrun, Yorum 
from .forms import RegisterForm 

# --- ANASAYFA ---
# --- ANASAYFA ---
def index(request):
    restoranlar = Restoran.objects.all().distinct()

    # --- FİLTRELEME ---
    # 1. Kategoriler (Sidebar'dan veya Üst Menüden)
    # URL'de ?cat=Burger&cat=Pizza gibi gelebilir (getlist)
    secili_kategoriler = request.GET.getlist('cat')
    if secili_kategoriler and 'Tümü' not in secili_kategoriler:
        # Seçili kategorilerden herhangi birini içeren restoranları getir
        query = Q()
        for k in secili_kategoriler:
            query |= Q(isim__icontains=k) | Q(aciklama__icontains=k) | Q(yemek__isim__icontains=k)
        restoranlar = restoranlar.filter(query).distinct()

    # 2. Arama (Sidebar Mutfak Arama)
    mutfak_ara = request.GET.get('mutfak_q')
    if mutfak_ara:
        restoranlar = restoranlar.filter(
            Q(isim__icontains=mutfak_ara) | 
            Q(aciklama__icontains=mutfak_ara)
        ).distinct()

    # --- SIRALAMA ---
    sort_order = request.GET.get('sort', 'onerilen')
    
    if sort_order == 'puan':
        # Yorum puan ortalamasına göre azalan
        restoranlar = restoranlar.annotate(avg_puan=Avg('yorum__puan')).order_by('-avg_puan')
    elif sort_order == 'teslimat':
        # Veritabanında teslimat süresi yok, ID'ye göre tersten (yeni eklenenler hızlı gibi :D)
        restoranlar = restoranlar.order_by('-id')
    elif sort_order == 'indirim':
        # Açıklamasında 'indirim' geçenleri öne al
        restoranlar = restoranlar.filter(aciklama__icontains='indirim')
    # onerilen ise varsayılan sıralama kalır

    # Favorileri al
    favori_ids = []
    if request.user.is_authenticated:
        favori_ids = Favori.objects.filter(user=request.user).values_list('restoran_id', flat=True)

    context = {
        'restoranlar': restoranlar,
        'favori_ids': list(favori_ids),
        'secili_kategoriler': secili_kategoriler,
        'sort_order': sort_order
    }
    return render(request, 'core/index_v2.html', context)

# ... (rest of the file until sepet_detay) ...

def sepet_detay(request):
    sepet = _get_cart(request)
    sepet_urunleri = SepetUrun.objects.filter(sepet=sepet)
    
    ara_toplam = sepet.toplam_tutar()
    
    # Kupon Kontrolü
    indirim_tutari = 0
    odenecek_tutar = ara_toplam
    kupon_kod = request.session.get('kupon_kod')
    kupon_indirim = request.session.get('kupon_indirim')
    
    if kupon_kod and kupon_indirim:
        indirim_tutari = (ara_toplam * kupon_indirim) / 100
        odenecek_tutar = ara_toplam - indirim_tutari
    
    context = {
        'sepet': sepet,
        'sepet_urunleri': sepet_urunleri,
        'toplam_tutar': ara_toplam, # Eski değişken uyumluluğu için (artık 'ara_toplam')
        'ara_toplam': ara_toplam,
        'indirim_tutari': indirim_tutari,
        'odenecek_tutar': odenecek_tutar,
        'kupon_kod': kupon_kod,
        'kupon_indirim': kupon_indirim
    }
    return render(request, 'core/sepet.html', context)

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
    if request.method == 'POST':
        email = request.POST.get('username') # Login formunda name='username' kalsa da placeholder 'E-posta' olacak
        sifre = request.POST.get('password')
        
        if email:
            email = email.strip() # Boşlukları temizle
        
        print(f"DEBUG: Login attempt for email: '{email}'")

        # Email ile giriş yapılıyor
        try:
            # Login attempt check (Case insensitive lookup)
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj:
                print(f"DEBUG: User found: {user_obj.username} (ID: {user_obj.id})")
                user = authenticate(request, username=user_obj.username, password=sifre)
                print(f"DEBUG: Authenticate result: {user}")
            else:
                print("DEBUG: User not found with this email.")
                user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Hoşgeldin {user.first_name}! 👋")
                return redirect('index')
            else:
                messages.error(request, "E-posta adresi veya şifre hatalı.")
        except Exception as e:
             print(f"DEBUG: Exception in login: {e}")
             messages.error(request, "Bir hata oluştu.")
            
    return render(request, 'core/giris.html')

def kayit_ol(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Kayıt olunca otomatik giriş yap
            messages.success(request, "Aramıza hoşgeldin! İlk siparişine özel teslimat bizden. 🛵")
            return redirect('index')
    else:
        form = RegisterForm()
        
    return render(request, 'core/kayit.html', {'form': form})

def cikis_yap(request):
    logout(request)
    return redirect('index')

# --- RESTORAN ARAMA (DÜZELTİLDİ) ---
# --- RESTORAN ARAMA (İLETİŞİM SAYFASI) ---
def restoran_ara(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    return render(request, 'core/iletisim.html', {'restoran': restoran})

# --- GENEL ARAMA (YENİ) ---
def global_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        # İsimde VEYA (yemek isminde) geçen restoranlar
        results = Restoran.objects.filter(
            Q(isim__icontains=query) | 
            Q(yemek__isim__icontains=query)
        ).distinct()
    
    return render(request, 'core/search_results.html', {'results': results, 'query': query})

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
    
    ara_toplam = sepet.toplam_tutar()
    
    # Kupon Kontrolü
    indirim_tutari = 0
    odenecek_tutar = ara_toplam
    kupon_kod = request.session.get('kupon_kod')
    kupon_indirim = request.session.get('kupon_indirim')
    
    if kupon_kod and kupon_indirim:
        indirim_tutari = (ara_toplam * kupon_indirim) / 100
        odenecek_tutar = ara_toplam - indirim_tutari
    
    context = {
        'sepet': sepet,
        'sepet_urunleri': sepet_urunleri,
        'toplam_tutar': ara_toplam, 
        'ara_toplam': ara_toplam,
        'indirim_tutari': indirim_tutari,
        'odenecek_tutar': odenecek_tutar,
        'kupon_kod': kupon_kod,
        'kupon_indirim': kupon_indirim
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

def sepet_adet_azalt(request, sepet_urun_id):
    sepet_urun = get_object_or_404(SepetUrun, id=sepet_urun_id)
    current_cart = _get_cart(request)
    
    if sepet_urun.sepet != current_cart:
         messages.error(request, "Bu işlemi yapmaya yetkiniz yok.")
         return redirect('sepet_detay')
         
    if sepet_urun.adet > 1:
        sepet_urun.adet -= 1
        sepet_urun.save()
        messages.success(request, f"{sepet_urun.yemek.isim} adeti azaltıldı.")
    else:
        sepet_urun.delete()
        messages.info(request, f"{sepet_urun.yemek.isim} sepetten çıkarıldı.")
        
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

    # GET Request: Show Checkout Form
    ara_toplam = sepet.toplam_tutar()
    odenecek_tutar = ara_toplam
    
    # Check for coupon
    kupon_indirim = request.session.get('kupon_indirim')
    if kupon_indirim:
        indirim_tutari = (ara_toplam * kupon_indirim) / 100
        odenecek_tutar = ara_toplam - indirim_tutari

    context = {
        'sepet_urunleri': sepet_urunleri,
        'toplam_tutar': odenecek_tutar
    }
    return render(request, 'core/siparis_olustur.html', context)

def siparis_takip(request, id):
    siparis = get_object_or_404(Siparis, id=id)
    siparis_urunleri = SiparisUrun.objects.filter(siparis=siparis)
    
    # Progress Bar Logic
    progress_width = 0
    step1_class = "btn-secondary"
    step2_class = "btn-secondary"
    step3_class = "btn-secondary"

    if siparis.durum == 'hazirlaniyor':
        progress_width = 15
        step1_class = "btn-success"
    elif siparis.durum == 'yolda':
        progress_width = 65
        step1_class = "btn-success"
        step2_class = "btn-success"
    elif siparis.durum == 'teslim_edildi':
        progress_width = 100
        step1_class = "btn-success"
        step2_class = "btn-success"
        step3_class = "btn-success"
    
    # Restoran bilgisini al (ilk üründen)
    restoran = None
    if siparis_urunleri.exists():
        restoran = siparis_urunleri.first().yemek.restoran

    context = {
        'siparis': siparis,
        'siparis_urunleri': siparis_urunleri,
        'restoran': restoran,
        'progress_width': progress_width,
        'step1_class': step1_class,
        'step2_class': step2_class,
        'step3_class': step3_class
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

def biz_kimiz(request):
    return render(request, 'core/biz_kimiz.html')

def kullanim_kosullari(request):
    return render(request, 'core/kullanim_kosullari.html')

def kvkk(request):
    return render(request, 'core/kvkk.html')

def cerez_politikasi(request):
    return render(request, 'core/cerez_politikasi.html')

# --- CANLI DESTEK API & VIEWS ---
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage
from django.contrib.admin.views.decorators import staff_member_required

def get_or_create_chat_session(request):
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    
    chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
    return chat_session

@csrf_exempt
def chat_api_send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_text = data.get('message')
        sender = data.get('sender', 'user') # 'user' or 'admin' (admin logic will be separate usually)

        # Güvenlik: Admin mesajı sadece admin oturumundan atılabilir
        if sender == 'admin' and not request.user.is_staff:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        # Eğer admin panelinden geliyorsa session_id'yi post datasından al
        if sender == 'admin':
            session_id = data.get('session_id')
            chat_session = get_object_or_404(ChatSession, session_id=session_id)
        else:
            chat_session = get_or_create_chat_session(request)

        ChatMessage.objects.create(
            chat_session=chat_session,
            sender=sender,
            message=message_text,
            is_read=(sender=='admin') # Admin atınca user okumamış sayılır, user atınca admin okumamış sayılır
        )
        
        if sender == 'user' and chat_session.customer_name == "Ziyaretçi":
             # Belki ileride isim sorarız, şimdilik ID'nin bir kısmı
             pass

        # --- OTOMATİK YANIT SİSTEMİ (BOT) ---
        if sender == 'user':
            msg_lower = message_text.lower()
            bot_reply = None
            
            if 'merhaba' in msg_lower or 'selam' in msg_lower:
                bot_reply = "Merhabalar! Size nasıl yardımcı olabilirim?"
            elif 'sipariş' in msg_lower or 'yemek' in msg_lower:
                bot_reply = "Siparişinizle ilgili bir sorun mu yaşıyorsunuz? Lütfen sipariş numaranızı belirtin."
            elif 'indirim' in msg_lower or 'kampanya' in msg_lower:
                bot_reply = "Güncel kampanyalarımıza ana sayfadaki slider alanından ulaşabilirsiniz. Çok özel fırsatlar sizi bekliyor! 🍔"
            elif 'kurye' in msg_lower or 'iş' in msg_lower:
                bot_reply = "Kurye başvurusu için 'Söyleyelim Kurye' sayfamızı ziyaret edebilirsiniz."
            elif 'canlı' in msg_lower or 'temsilci' in msg_lower:
                bot_reply = "Anlaşıldı. Sizi hemen ilgili birimimize aktarıyorum, lütfen hatta kalın... 🎧"
            
            # Eğer bir auto-reply varsa kaydet
            if bot_reply:
                ChatMessage.objects.create(
                    chat_session=chat_session,
                    sender='admin', # Bot mesajı admin gibi görünsün
                    message=bot_reply,
                    is_read=True
                )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def chat_api_get_messages(request):
    # Admin panelinden istek geliyorsa session_id parametresi beklenir
    if request.user.is_staff and request.GET.get('session_id'):
         session_id = request.GET.get('session_id')
         chat_session = get_object_or_404(ChatSession, session_id=session_id)
    else:
        chat_session = get_or_create_chat_session(request)

    # Okunmamış mesajları getir (Poll için)
    # Basitlik adına son 50 mesajı gönderiyoruz
    messages_qs = ChatMessage.objects.filter(chat_session=chat_session).order_by('timestamp')
    messages_data = [{
        'sender': msg.sender,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%H:%M')
    } for msg in messages_qs]

    return JsonResponse({'messages': messages_data})

@staff_member_required
def admin_chat_dashboard(request):
    # Sadece aktif ve mesajı olan oturumları gösterelim
    sessions = ChatSession.objects.filter(is_active=True).order_by('-updated_at')
    return render(request, 'core/admin_chat_dashboard.html', {'sessions': sessions})

@staff_member_required
def admin_chat_detail(request, session_id):
    chat_session = get_object_or_404(ChatSession, session_id=session_id)
    
    # Admin açtığında kullanıcının mesajlarını okundu yap
    chat_session.chatmessage_set.filter(sender='user', is_read=False).update(is_read=True)
    
    return render(request, 'core/admin_chat_detail.html', {'chat_session': chat_session})

# --- YENİ ÖZELLİK VIEWS (FAVORİ & KUPON) ---
from .models import Favori, Kupon
from django.db import IntegrityError

@login_required
def favori_toggle(request, restoran_id):
    restoran = get_object_or_404(Restoran, id=restoran_id)
    favori, created = Favori.objects.get_or_create(user=request.user, restoran=restoran)
    
    if not created:
        # Zaten varsa sil (Toggle mantığı)
        favori.delete()
        mesaj = "Favorilerden çıkarıldı."
        durum = "removed"
    else:
        mesaj = "Favorilere eklendi."
        durum = "added"
    
    # AJAX isteği geldiyse JSON dön, yoksa önceki sayfaya dön
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         return JsonResponse({'status': durum, 'message': mesaj})
         
    messages.success(request, f"{restoran.isim} {mesaj}")
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def favorilerim(request):
    favoriler = Favori.objects.filter(user=request.user).select_related('restoran')
    # Sadece restoran objelerini listeye çevirelim
    restoranlar = [f.restoran for f in favoriler]
    return render(request, 'core/favorilerim.html', {'restoranlar': restoranlar})

def kupon_uygula(request):
    if request.method == 'POST':
        kod = request.POST.get('kod')
        sepet = _get_cart(request)
        toplam = sepet.toplam_tutar()
        
        try:
            kupon = Kupon.objects.get(kod=kod, aktif=True)
            if toplam >= kupon.min_sepet_tutari:
                request.session['kupon_kod'] = kupon.kod
                request.session['kupon_indirim'] = kupon.indirim_yuzdesi
                messages.success(request, f"Tebrikler! %{kupon.indirim_yuzdesi} indirim uygulandı.")
            else:
                messages.warning(request, f"Bu kupon için minimum sepet tutarı {kupon.min_sepet_tutari} TL olmalıdır.")
        except Kupon.DoesNotExist:
            messages.error(request, "Geçersiz veya süresi dolmuş kupon kodu.")
            
    return redirect('sepet_detay')

# --- YENİ ÖZELLİK VIEWS (FAVORİ & KUPON) ---
from .models import Favori, Kupon
from django.db import IntegrityError

@login_required
def favori_toggle(request, restoran_id):
    restoran = get_object_or_404(Restoran, id=restoran_id)
    favori, created = Favori.objects.get_or_create(user=request.user, restoran=restoran)
    
    if not created:
        # Zaten varsa sil (Toggle mantığı)
        favori.delete()
        mesaj = "Favorilerden çıkarıldı."
        durum = "removed"
    else:
        mesaj = "Favorilere eklendi."
        durum = "added"
    
    # AJAX isteği geldiyse JSON dön, yoksa önceki sayfaya dön
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         return JsonResponse({'status': durum, 'message': mesaj})
         
    messages.success(request, f"{restoran.isim} {mesaj}")
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def favorilerim(request):
    favoriler = Favori.objects.filter(user=request.user).select_related('restoran')
    # Sadece restoran objelerini listeye çevirelim
    restoranlar = [f.restoran for f in favoriler]
    return render(request, 'core/favorilerim.html', {'restoranlar': restoranlar})

def kupon_uygula(request):
    if request.method == 'POST':
        kod = request.POST.get('kod')
        sepet = _get_cart(request)
        toplam = sepet.toplam_tutar()
        
        try:
            kupon = Kupon.objects.get(kod=kod, aktif=True)
            if toplam >= kupon.min_sepet_tutari:
                request.session['kupon_kod'] = kupon.kod
                request.session['kupon_indirim'] = kupon.indirim_yuzdesi
                messages.success(request, f"Tebrikler! %{kupon.indirim_yuzdesi} indirim uygulandı.")
            else:
                messages.warning(request, f"Bu kupon için minimum sepet tutarı {kupon.min_sepet_tutari} TL olmalıdır.")
        except Kupon.DoesNotExist:
            messages.error(request, "Geçersiz veya süresi dolmuş kupon kodu.")
            
    return redirect('sepet_detay')

# --- KULLANICI PROFİLİ VE KART İŞLEMLERİ ---
from .models import UserProfile, SavedCard

@login_required
def kullanici_bilgileri(request):
    # Profil yoksa oluştur (Signal çalışmazsa diye fallback)
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Form verilerini al
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telefon = request.POST.get('telefon')
        adres = request.POST.get('adres')
        
        # User modelini güncelle
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        # Profil modelini güncelle
        profile.telefon = telefon
        profile.adres = adres
        profile.save()
        
        messages.success(request, 'Bilgileriniz başarıyla güncellendi.')
        return redirect('kullanici_bilgileri')
        
    return render(request, 'core/kullanici_bilgileri.html')

@login_required
def kayitli_kartlarim(request):
    kartlar = SavedCard.objects.filter(user=request.user)
    return render(request, 'core/kayitli_kartlarim.html', {'kartlar': kartlar})

@login_required
def kart_ekle(request):
    if request.method == 'POST':
        kart_adi = request.POST.get('kart_adi')
        kart_sahibi = request.POST.get('kart_sahibi')
        kart_numarasi = request.POST.get('kart_numarasi') # Demo: Maskeleme yapılacak
        ay = request.POST.get('ay')
        yil = request.POST.get('yil')
        
        # Basit maskeleme (Son 4 hane hariç yıldızla)
        masked_num = "**** **** **** " + kart_numarasi[-4:] if len(kart_numarasi) >= 16 else kart_numarasi
        
        SavedCard.objects.create(
            user=request.user,
            kart_adi=kart_adi,
            kart_sahibi=kart_sahibi,
            kart_numarasi=masked_num,
            son_kullanma_ay=ay,
            son_kullanma_yil=yil
        )
        
        messages.success(request, 'Kartınız başarıyla eklendi.')
        return redirect('kayitli_kartlarim')
    return redirect('kayitli_kartlarim')

@login_required
def kart_sil(request, id):
    kart = get_object_or_404(SavedCard, id=id, user=request.user)
    kart.delete()
    messages.info(request, 'Kart silindi.')
    return redirect('kayitli_kartlarim')


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
