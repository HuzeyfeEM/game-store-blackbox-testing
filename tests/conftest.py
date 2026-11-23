import os
import re
import sys

import pytest

# Proje klasörünü Python'un arama yoluna ekle (app.py'yi bulabilmek için)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as uygulama


def mesajlar(yanit):
    """Sayfadaki hata/bilgi mesajlarını liste olarak döndürür."""
    return re.findall(r'<div class="mesaj">(.*?)</div>', yanit.text)


def kayit_verisi(**degisen):
    """Geçerli varsayılan kayıt verisini döndürür. Sadece verilen alanlar değişir."""
    veri = {
        "kullanici_adi": "mehmet",
        "email": "mehmet@test.com",
        "sifre": "oyun12345",
        "sifre_tekrar": "oyun12345",
        "yas": "20",
    }
    veri.update(degisen)
    return veri


@pytest.fixture
def client():
    """ÖK-1: Uygulama temiz başlar ve 'ali' kullanıcısı kayıtlıdır."""
    uygulama.kullanicilar.clear()
    uygulama.basarisiz_denemeler.clear()
    uygulama.app.config["TESTING"] = True

    with uygulama.app.test_client() as c:
        c.post("/kayit", data=kayit_verisi(kullanici_adi="ali", email="ali@test.com"))
        c.get("/giris")  # "Kayıt başarılı" mesajını ekrandan temizler
        yield c


@pytest.fixture
def girisli_client(client):
    """ÖK-2: ÖK-1 + 'ali' ile giriş yapılmış, sepet boş."""
    client.post("/giris", data={"kullanici_adi": "ali", "sifre": "oyun12345"})
    client.get("/oyunlar")  # "Giriş başarılı" mesajını temizler
    return client