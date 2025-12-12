from django.core.management.base import BaseCommand
from core.models import Restoran, Yemek
import random

class Command(BaseCommand):
    help = 'Populates the database with 10 dummy restaurants and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Restoran.objects.all().delete()
        
        # Data for 10 Restaurants
        restaurants_data = [
            {
                "isim": "Burger King",
                "aciklama": "Ateş seni çağırıyor! En lezzetli burgerler burada.",
                "resim": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&q=80",
                "kategori": "Burger"
            },
            {
                "isim": "Domino's Pizza",
                "aciklama": "30 dakikada kapında, yoksa bedava!",
                "resim": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=800&q=80",
                "kategori": "Pizza"
            },
            {
                "isim": "Hasan Usta Kebap",
                "aciklama": "Adana'nın gerçek lezzeti. Acılı, zırh kıyması.",
                "resim": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80",
                "kategori": "Kebap"
            },
            {
                "isim": "Starbucks",
                "aciklama": "Dünyanın en iyi kahveleri ve eşsiz tatlıları.",
                "resim": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80",
                "kategori": "Tatlı & içecek"
            },
            {
                "isim": "KFC",
                "aciklama": "Parmak yedirten lezzet. 11 baharatlı gizli tarif.",
                "resim": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=800&q=80",
                "kategori": "Tavuk"
            },
            {
                "isim": "Komagene Çiğ Köfte",
                "aciklama": "Etsiz çiğ köftenin tek adresi. Her 15'inde %50 bedava.",
                "resim": "https://i.nefisyemektarifleri.com/2023/12/06/etsiz-cig-kofte-tarifi-nasil-yapilir.jpg", # Manual link for cig kofte
                "kategori": "Çiğ Köfte"
            },
            {
                "isim": "Sultanahmet Köftecisi",
                "aciklama": "Tarihi lezzet. 1920'den beri değişmeyen tat.",
                "resim": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800&q=80",
                "kategori": "Köfte"
            },
            {
                "isim": "Mado",
                "aciklama": "Gerçek Maraş dondurması ve sütlü tatlılar.",
                "resim": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&q=80",
                "kategori": "Tatlı"
            },
            {
                "isim": "Dönerci Ali Usta",
                "aciklama": "Odun ateşinde yaprak döner. Yanında bol köpüklü ayran.",
                "resim": "https://images.unsplash.com/photo-1662116886364-77ae38d21c43?w=800&q=80",
                "kategori": "Döner"
            },
            {
                "isim": "Sushi Co",
                "aciklama": "Uzakdoğu mutfağının en iyileri. Sushi, noodle ve daha fazlası.",
                "resim": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&q=80",
                "kategori": "Uzak Doğu"
            }
        ]

        products_map = {
            "Burger": [
                ("Whopper", 180, "Alevde ızgara dana eti, büyük boy susamlı ekmek."),
                ("Steakhouse", 210, "Özel soslu, çıtır soğanlı premium lezzet."),
                ("Chicken Royale", 150, "Uzun tavuk fileto, mayonez ve taze marul.")
            ],
            "Pizza": [
                ("Karışık Pizza", 220, "Sucuk, salam, sosis, mantar, mısır."),
                ("Pepperoni", 240, "Bol mozzarella ve baharatlı pepperoni."),
                ("Margarita", 190, "Domates sosu ve mozzarella peyniri.")
            ],
            "Kebap": [
                ("Adana Kebap", 280, "Zırh kıyması, özel baharatlar, yanında közlenmiş domates."),
                ("Urfa Kebap", 270, "Acısız zırh kıyması, lavaş ekmeği ile."),
                ("Beyti Sarma", 320, "Lavaşa sarılı kebap, sarımsaklı yoğurt ve salça sosu.")
            ],
            "Tatlı & içecek": [
                ("White Chocolate Mocha", 120, "Beyaz çikolata ve espresso."),
                ("Cheesecake", 110, "Frambuazlı veya limonlu seçenekleriyle."),
                ("Filtre Kahve", 70, "Günün kahvesi, taze demlenmiş.")
            ],
            "Tavuk": [
                ("Kova Menü", 350, "10 parça çıtır tavuk, 4 kanat, 2 patates."),
                ("Zinger Burger", 160, "Acılı çıtır tavuk but fileto."),
                ("Twister Dürüm", 140, "Lavaş içinde çıtır tavuk parçaları.")
            ],
            "Çiğ Köfte": [
                ("Mega Dürüm", 80, "200gr çiğ köfte, bol yeşillik, nar ekşisi."),
                ("Sushi Çiğ Köfte", 100, "Özel kesim, lokmalık sunum."),
                ("Aile Boyu Paket", 300, "1kg çiğ köfte, yeşillik, soslar.")
            ],
            "Köfte": [
                ("Izgara Köfte Porsiyon", 240, "6 adet klasik köfte, piyaz ve pilav ile."),
                ("Piyaz", 90, "Haşlanmış fasulye, soğan, özel sos."),
                ("İrmik Helvası", 70, "Sıcak üzeri fıstıklı.")
            ],
            "Tatlı": [
                ("Maraş Dondurması (Top)", 40, "Sade, çikolatalı, fıstıklı."),
                ("Baklava (Porsiyon)", 180, "3 dilim fıstıklı baklava."),
                ("Kazandibi", 110, "Yanık kıvamında eşsiz lezzet.")
            ],
            "Döner": [
                ("İskender", 340, "Tereyağlı, domates soslu, yoğurtlu efsane."),
                ("Pilav Üstü Döner", 300, "Tereyağlı pilav ve yaprak döner."),
                ("Tombik Döner", 200, "Gobit ekmek arası bol döner.")
            ],
            "Uzak Doğu": [
                ("California Roll", 220, "Yengeç, avokado, salatalık."),
                ("Noodle Tavuklu", 200, "Sebzeli ve tavuklu noodle."),
                ("Miso Çorbası", 90, "Geleneksel Japon soya çorbası.")
            ]
        }
        
        # Fallback for unknown categories
        default_products = [
            ("Günün Menüsü", 200, "Şefin özel seçimi."),
            ("İçecek", 40, "330ml kutu içecek."),
            ("Tatlı", 90, "Günün tatlısı.")
        ]

        for r_data in restaurants_data:
            restoran = Restoran.objects.create(
                isim=r_data["isim"],
                aciklama=r_data["aciklama"],
                telefon="0212 555 44 33",
                resim_linki=r_data["resim"]
            )
            
            # Add Products
            cat = r_data.get("kategori", "Genel")
            products = products_map.get(cat, default_products)
            
            for p_name, p_price, p_desc in products:
                # Use query param for random distinct images
                img_url = f"https://source.unsplash.com/random/400x300/?{p_name.split()[0]},food"
                # Alternative simpler images if unsplash random redirects weirdly
                # But for now let's trust it or use a solid placeholder service
                img_url = f"https://loremflickr.com/400/300/food?random={random.randint(1,1000)}"

                Yemek.objects.create(
                    restoran=restoran,
                    isim=p_name,
                    fiyat=p_price,
                    icerik=p_desc,
                    resim=img_url
                )
            
            self.stdout.write(f'Created {restoran.isim}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with 10 restaurants'))
