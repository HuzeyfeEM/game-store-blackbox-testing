"""Durum Geçiş testleri (ST-01 – ST-12)"""
from conftest import mesajlar

import app as uygulama

DOGRU = {"kullanici_adi": "ali", "sifre": "oyun12345"}
YANLIS = {"kullanici_adi": "ali", "sifre": "yanlis123"}


def test_st01_basarili_giris(client):
    # S0 --T3--> S1
    yanit = client.post("/giris", data=DOGRU)
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/oyunlar")


def test_st02_tek_yanlis_giris(client):
    # S0 --T1--> S0
    yanit = client.post("/giris", data=YANLIS)
    assert yanit.status_code == 401
    assert "Kullanıcı adı veya şifre hatalı." in mesajlar(yanit)


def test_st03_uc_yanlis_giris_hesabi_kilitler(client):
    # S0 --T1--> S0 --T1--> S0 --T2--> S3 --T5--> S3
    for _ in range(3):
        assert client.post("/giris", data=YANLIS).status_code == 401
    yanit = client.post("/giris", data=DOGRU)
    assert yanit.status_code == 403
    assert "Hesabınız kilitlendi. Çok fazla hatalı deneme yapıldı." in mesajlar(yanit)


def test_st04_basarili_giris_sayaci_sifirlar(client):
    # 2 yanlış + doğru giriş → sayaç sıfırlanır
    client.post("/giris", data=YANLIS)
    client.post("/giris", data=YANLIS)
    assert client.post("/giris", data=DOGRU).status_code == 302

    # Yeni gizli pencere = yeni oturum
    with uygulama.app.test_client() as yeni_pencere:
        yeni_pencere.post("/giris", data=YANLIS)
        yanit = yeni_pencere.post("/giris", data=YANLIS)
        assert yanit.status_code == 401  # 403 olmamalı (kilitli değil)


def test_st05_ziyaretci_oyunlar_sayfasina_giremez(client):
    # S0 --T4--> S0
    yanit = client.get("/oyunlar")
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/giris")
    assert "Bu sayfayı görmek için giriş yapmalısınız." in mesajlar(client.get("/giris"))


def test_st06_ziyaretci_sepete_giremez(client):
    # S0 --T4--> S0
    yanit = client.get("/sepet")
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/giris")
    assert "Sepeti görmek için giriş yapmalısınız." in mesajlar(client.get("/giris"))


def test_st07_girisli_kullanici_giris_sayfasina_gidemez(girisli_client):
    # S1'de kalır
    yanit = girisli_client.get("/giris")
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/oyunlar")


def test_st08_sepete_ekle_ve_satin_al(girisli_client):
    # S1 --T6--> S2 --T9--> S1
    girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": "2"})
    assert "Minecraft" in girisli_client.get("/sepet").text  # S2

    yanit = girisli_client.post("/satin-al")
    assert yanit.status_code == 302
    assert "Satın alma başarılı! Teşekkür ederiz." in mesajlar(girisli_client.get("/oyunlar"))
    assert "Sepetiniz boş." in girisli_client.get("/sepet").text  # S1


def test_st09_bos_sepetle_satin_alma(girisli_client):
    # S1 --T7--> S1
    yanit = girisli_client.post("/satin-al")
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/sepet")
    assert "Sepetiniz boş." in mesajlar(girisli_client.get("/sepet"))


def test_st10_cikistan_sonra_korumali_sayfa(girisli_client):
    # S1 --T10--> S4 --T11--> S0
    girisli_client.get("/cikis")
    yanit = girisli_client.get("/oyunlar")
    assert yanit.status_code == 302, "Çıkış yapılmasına rağmen oyunlar sayfası açıldı"
    assert yanit.headers["Location"].endswith("/giris")


def test_st11_cikistan_sonra_giris_sayfasi_acilir(girisli_client):
    # S1 --T10--> S4: giriş formu görünmeli
    girisli_client.get("/cikis")
    yanit = girisli_client.get("/giris")
    assert yanit.status_code == 200, "Çıkıştan sonra giriş sayfası yerine başka sayfaya yönlendirildi"
    assert "Giriş Yap" in yanit.text


def test_st12_cikistan_sonra_tekrar_giris(girisli_client):
    # S1 --T10--> S4 --T12--> S1
    girisli_client.get("/cikis")
    yanit = girisli_client.post("/giris", data=DOGRU)
    assert yanit.status_code == 302
    assert "Giriş başarılı. Hoş geldin, ali!" in mesajlar(girisli_client.get("/oyunlar"))