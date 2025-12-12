from django.db import models

class Restoran(models.Model):
    isim = models.CharField(max_length=100, verbose_name="Restoran Adı")
    aciklama = models.TextField(blank=True, verbose_name="Kısa Açıklama", help_text="Örn: En lezzetli hamburgerlerin adresi.")
    telefon = models.CharField(max_length=20, verbose_name="Sipariş Hattı", help_text="Müşterilerin arayacağı numara (Örn: 0212...)")
    resim_linki = models.CharField(max_length=500, blank=True, verbose_name="Kapak Fotoğrafı (Link)", help_text="Google'dan kopyaladığınız resim adresini buraya yapıştırın.")

    class Meta:
        verbose_name = "Restoran"
        verbose_name_plural = "Restoranlar"

    def __str__(self):
        return self.isim

class Yemek(models.Model):
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE, verbose_name="Hangi Restoran?")
    isim = models.CharField(max_length=100, verbose_name="Yemek Adı")
    fiyat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Fiyat (₺)")
    icerik = models.TextField(blank=True, verbose_name="İçindekiler / Not", help_text="Örn: Soğan, turşu, özel sos...")
    
    # --- YENİ EKLEDİĞİMİZ ALAN ---
    resim = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Yemek Fotoğrafı (Link)",
        help_text="Yemeğin fotoğraf linkini buraya yapıştırın."
    )

    class Meta:
        verbose_name = "Yemek"
        verbose_name_plural = "Yemek Menüsü"
    
    def __str__(self):
        return self.isim
    
    # Dosyanın en altına ekle:

class Sikayet(models.Model):
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE, verbose_name="Şikayet Edilen Restoran")
    ad_soyad = models.CharField(max_length=100, verbose_name="Müşteri Adı", blank=True, default="Anonim")
    konu = models.CharField(max_length=100, verbose_name="Şikayet Konusu", choices=[
        ('teslimat', 'Teslimat Çok Geç Kaldı'),
        ('lezzet', 'Yemek Soğuk/Lezzetsiz'),
        ('davranis', 'Kurye Davranışı'),
        ('diger', 'Diğer Sebepler')
    ])
    mesaj = models.TextField(verbose_name="Şikayet Detayı")
    tarih = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")

    class Meta:
        verbose_name = "Şikayet"
        verbose_name_plural = "Gelen Şikayetler"
        ordering = ['-tarih'] # En yeni şikayet en üstte

    def __str__(self):
        return f"{self.restoran.isim} - {self.konu}"
    
    # Dosyanın en altına ekle:

class Secenek(models.Model):
    yemek = models.ForeignKey(Yemek, on_delete=models.CASCADE, related_name='secenekler')
    isim = models.CharField(max_length=100, verbose_name="Seçenek Adı", help_text="Örn: Ekstra Peynir, Acı Sos")
    fiyat = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Ekstra Fiyat")

    def __str__(self):
        return f"{self.isim} (+{self.fiyat} TL)"
    
    # Mevcut kodların altına ekle:

class RestoranBasvuru(models.Model):
    restoran_adi = models.CharField(max_length=100)
    yetkili_adi = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    email = models.EmailField()
    sehir = models.CharField(max_length=50)
    kvkk_onayi = models.BooleanField(default=False)
    basvuru_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restoran_adi} - {self.yetkili_adi}"

    class Meta:
        verbose_name = "Restoran Başvurusu"
        verbose_name_plural = "Restoran Başvuruları"

# --- SEPET MODELLERİ ---

from django.contrib.auth.models import User

class Sepet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı")
    session_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Oturum ID")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    
    def toplam_tutar(self):
        # Sepetteki tüm ürünlerin fiyatını toplar
        toplam = 0
        for urun in self.sepeturun_set.all():
            toplam += urun.toplam_fiyat()
        return toplam

    class Meta:
        verbose_name = "Sepet"
        verbose_name_plural = "Sepetler"

    def __str__(self):
        return f"Sepet {self.id} - {self.user if self.user else self.session_id}"

class SepetUrun(models.Model):
    sepet = models.ForeignKey(Sepet, on_delete=models.CASCADE, verbose_name="Sepet")
    yemek = models.ForeignKey(Yemek, on_delete=models.CASCADE, verbose_name="Yemek")
    adet = models.PositiveIntegerField(default=1, verbose_name="Adet")
    # Fiyat değişirse sipariş anındaki fiyatı tutmak için eklenebilir ama şimdilik modelden çekelim.
    
    def toplam_fiyat(self):
        return self.yemek.fiyat * self.adet

    class Meta:
        verbose_name = "Sepet Ürünü"
        verbose_name_plural = "Sepetteki Ürünler"
    
    def __str__(self):
        return f"{self.yemek.isim} ({self.adet})"

# --- SİPARİŞ MODELLERİ ---

class Siparis(models.Model):
    DURUM_SECENEKLERI = [
        ('hazirlaniyor', 'Hazırlanıyor'),
        ('yolda', 'Yolda'),
        ('teslim_edildi', 'Teslim Edildi'),
        ('iptal', 'İptal Edildi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı")
    ad_soyad = models.CharField(max_length=100, verbose_name="Ad Soyad")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Teslimat Adresi")
    adres_tarifi = models.TextField(blank=True, verbose_name="Adres Tarifi")
    
    toplam_tutar = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Toplam Tutar")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='hazirlaniyor', verbose_name="Sipariş Durumu")

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        ordering = ['-olusturma_tarihi']

    def __str__(self):
        return f"Sipariş #{self.id} - {self.ad_soyad}"

class SiparisUrun(models.Model):
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE, verbose_name="Sipariş")
    yemek = models.ForeignKey(Yemek, on_delete=models.CASCADE, verbose_name="Yemek")
    adet = models.PositiveIntegerField(verbose_name="Adet")
    fiyat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Birim Fiyat (TL)")
    
    def toplam_tutar(self):
        return self.adet * self.fiyat

    class Meta:
        verbose_name = "Sipariş Ürünü"
        verbose_name_plural = "Sipariş Ürünleri"

    def __str__(self):
        return f"{self.yemek.isim} x {self.adet}"


class Yorum(models.Model):
    siparis = models.OneToOneField(Siparis, on_delete=models.CASCADE, verbose_name="Sipariş")
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE, related_name='yorumlar', verbose_name="Restoran")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    puan = models.PositiveIntegerField(default=5, verbose_name="Puan (1-5)")
    yorum = models.TextField(verbose_name="Yorumunuz")
    tarih = models.DateTimeField(auto_now_add=True, verbose_name="Yorum Tarihi")

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ['-tarih']

    def __str__(self):
        return f"{self.user.username} - {self.restoran.isim} ({self.puan})"

# --- CANLI DESTEK MODELLERİ ---

class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True, verbose_name="Oturum ID")
    customer_name = models.CharField(max_length=100, blank=True, verbose_name="Müşteri Adı", default="Ziyaretçi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = "Sohbet Oturumu"
        verbose_name_plural = "Sohbet Oturumları"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.customer_name} ({self.session_id[:8]})"
    
    @property
    def unread_count_for_admin(self):
        return self.chatmessage_set.filter(sender='user', is_read=False).count()

class ChatMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, verbose_name="Oturum")
    sender = models.CharField(max_length=10, choices=[('user', 'Kullanıcı'), ('admin', 'Admin')], verbose_name="Gönderen")
    message = models.TextField(verbose_name="Mesaj")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Zaman")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}"

# --- YENİ ÖZELLİKLER (FAVORİLER & KUPONLAR) ---

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE, verbose_name="Restoran")
    tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoriler"
        unique_together = ('user', 'restoran') # Aynı restoranı bir daha favorileyemesin

    def __str__(self):
        return f"{self.user.username} - {self.restoran.isim}"

class Kupon(models.Model):
    kod = models.CharField(max_length=50, unique=True, verbose_name="Kupon Kodu")
    indirim_yuzdesi = models.PositiveIntegerField(verbose_name="İndirim Yüzdesi (%)", help_text="Örn: 10 yazarsanız %10 indirim yapar.")
    min_sepet_tutari = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Min. Sepet Tutarı")
    aktif = models.BooleanField(default=True, verbose_name="Aktif mi?")
    
    def __str__(self):
        return f"{self.kod} (%{self.indirim_yuzdesi})"

    class Meta:
        verbose_name = "Kupon"
        verbose_name_plural = "Kuponlar"

# --- YENİ EKLENEN MODELLER: KULLANICI PROFİLİ VE KARTLAR ---

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Kullanıcı")
    telefon = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    adres = models.TextField(blank=True, verbose_name="Varsayılan Adres")
    dogum_tarihi = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")

    def __str__(self):
        return f"{self.user.username} Profili"

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class SavedCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    kart_adi = models.CharField(max_length=50, verbose_name="Kartın Adı", help_text="Örn: İş Bankası Maaş")
    kart_sahibi = models.CharField(max_length=100, verbose_name="Kart Sahibi")
    kart_numarasi = models.CharField(max_length=20, verbose_name="Kart Numarası (Maskelenmiş)")
    son_kullanma_ay = models.CharField(max_length=2, verbose_name="Ay")
    son_kullanma_yil = models.CharField(max_length=4, verbose_name="Yıl")
    
    # Gerçek uygulamada kart numarası asla böyle saklanmaz, token saklanır.
    # Bu basit bir demo olduğu için sadece son 4 haneyi göstereceğiz.
    
    def __str__(self):
        return f"{self.kart_adi} - {self.user.username}"

    class Meta:
        verbose_name = "Kayıtlı Kart"
        verbose_name_plural = "Kayıtlı Kartlar"
