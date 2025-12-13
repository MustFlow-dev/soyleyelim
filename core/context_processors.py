from .views import _get_cart

def sepet_bilgisi(request):
    """
    Tüm şablonlarda sepet bilgisini (ürün sayısı vb.) erişilebilir kılar.
    """
    try:
        sepet = _get_cart(request)
        # Sepetteki toplam ürün sayısı (her bir ürünün adeti toplanarak)
        sepet_ogeleri = sepet.sepeturun_set.all()
        toplam_adet = sum(item.adet for item in sepet_ogeleri)
        toplam_tutar = sepet.toplam_tutar()
        
        return {
            'global_sepet_adet': toplam_adet,
            'global_sepet_tutar': toplam_tutar,
            'global_sepet_ogeleri': sepet_ogeleri,
            'global_sepet': sepet
        }
    except:
        return {
            'global_sepet_adet': 0,
            'global_sepet_tutar': 0,
            'global_sepet_ogeleri': [],
            'global_sepet': None
        }
