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