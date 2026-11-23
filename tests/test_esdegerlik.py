"""Eşdeğerlik Bölümleme testleri (EP-01 – EP-24)"""
import pytest

from conftest import kayit_verisi, mesajlar


# ---------- Kayıt ----------

def test_ep01_gecerli_kayit(client):
    yanit = client.post("/kayit", data=kayit_verisi())
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/giris")
    assert "Kayıt başarılı! Giriş yapabilirsiniz." in mesajlar(client.get("/giris"))


@pytest.mark.parametrize("degisen, beklenen_mesaj", [
    pytest.param({"kullanici_adi": "ab"}, "Kullanıcı adı 3-15 karakter olmalıdır.", id="EP-02"),
    pytest.param({"kullanici_adi": "a" * 20}, "Kullanıcı adı 3-15 karakter olmalıdır.", id="EP-03"),
    pytest.param({"kullanici_adi": "ali"}, "Bu kullanıcı adı zaten alınmış.", id="EP-04"),
    pytest.param({"kullanici_adi": ""}, "Tüm alanlar doldurulmalıdır.", id="EP-05"),
    pytest.param({"email": "mehmettest.com"}, "Geçerli bir e-posta adresi giriniz.", id="EP-06"),
    pytest.param({"email": "mehmet@"}, "Geçerli bir e-posta adresi giriniz.", id="EP-07"),
    pytest.param({"email": "ali@test.com"}, "Bu e-posta zaten kayıtlı.", id="EP-08"),
    pytest.param({"email": "ALI@test.com"}, "Bu e-posta zaten kayıtlı.", id="EP-09"),
    pytest.param({"sifre": "oyun1", "sifre_tekrar": "oyun1"}, "Şifre 8-20 karakter olmalıdır.", id="EP-10"),
    pytest.param({"sifre": "a" * 25, "sifre_tekrar": "a" * 25}, "Şifre 8-20 karakter olmalıdır.", id="EP-11"),
    pytest.param({"sifre_tekrar": "baska12345"}, "Şifreler eşleşmiyor.", id="EP-12"),
    pytest.param({"yas": "10"}, "Yaş 13 ile 99 arasında olmalıdır.", id="EP-13"),
    pytest.param({"yas": "120"}, "Yaş 13 ile 99 arasında olmalıdır.", id="EP-14"),
    pytest.param({"yas": "yirmi"}, "Yaş bir sayı olmalıdır.", id="EP-15"),
])
def test_gecersiz_kayit(client, degisen, beklenen_mesaj):
    yanit = client.post("/kayit", data=kayit_verisi(**degisen))
    assert yanit.status_code == 400
    assert beklenen_mesaj in mesajlar(yanit)


# ---------- Giriş ----------

def test_ep16_gecerli_giris(client):
    yanit = client.post("/giris", data={"kullanici_adi": "ali", "sifre": "oyun12345"})
    assert yanit.status_code == 302
    assert yanit.headers["Location"].endswith("/oyunlar")
    assert "Giriş başarılı. Hoş geldin, ali!" in mesajlar(client.get("/oyunlar"))


@pytest.mark.parametrize("kullanici_adi, sifre, beklenen_kod, beklenen_mesaj", [
    pytest.param("ali", "yanlis123", 401, "Kullanıcı adı veya şifre hatalı.", id="EP-17"),
    pytest.param("yokkisi", "oyun12345", 401, "Kullanıcı adı veya şifre hatalı.", id="EP-18"),
    pytest.param("ali", "", 400, "Kullanıcı adı ve şifre boş bırakılamaz.", id="EP-19"),
])
def test_gecersiz_giris(client, kullanici_adi, sifre, beklenen_kod, beklenen_mesaj):
    yanit = client.post("/giris", data={"kullanici_adi": kullanici_adi, "sifre": sifre})
    assert yanit.status_code == beklenen_kod
    assert beklenen_mesaj in mesajlar(yanit)


# ---------- Sepet ----------

def test_ep20_gecerli_adet(girisli_client):
    yanit = girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": "3"})
    assert yanit.status_code == 302
    sepet = girisli_client.get("/sepet").text
    assert "Minecraft" in sepet
    assert "1800 TL" in sepet  # 3 x 600 TL


@pytest.mark.parametrize("adet, beklenen_mesaj", [
    pytest.param("-2", "Adet 1 ile 5 arasında olmalıdır.", id="EP-21"),
    pytest.param("10", "Adet 1 ile 5 arasında olmalıdır.", id="EP-22"),
    pytest.param("iki", "Adet bir sayı olmalıdır.", id="EP-23"),
    pytest.param("", "Adet boş bırakılamaz.", id="EP-24"),
])
def test_gecersiz_adet(girisli_client, adet, beklenen_mesaj):
    yanit = girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": adet})
    assert yanit.status_code == 400
    assert beklenen_mesaj in mesajlar(yanit)