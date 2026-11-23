"""Sınır Değer Analizi testleri (BVA-01 – BVA-26)"""
import pytest

from conftest import kayit_verisi, mesajlar

AD_HATASI = "Kullanıcı adı 3-15 karakter olmalıdır."
SIFRE_HATASI = "Şifre 8-20 karakter olmalıdır."
YAS_HATASI = "Yaş 13 ile 99 arasında olmalıdır."
ADET_HATASI = "Adet 1 ile 5 arasında olmalıdır."


# ---------- Kayıt: kullanıcı adı, şifre, yaş ----------
# hata_mesaji = None ise kaydın BAŞARILI olması beklenir.

@pytest.mark.parametrize("degisen, hata_mesaji", [
    # Kullanıcı adı: 3–15 karakter
    pytest.param({"kullanici_adi": "ab"}, AD_HATASI, id="BVA-01"),
    pytest.param({"kullanici_adi": "abc"}, None, id="BVA-02"),
    pytest.param({"kullanici_adi": "abcd"}, None, id="BVA-03"),
    pytest.param({"kullanici_adi": "abcdefghijklmn"}, None, id="BVA-04"),
    pytest.param({"kullanici_adi": "abcdefghijklmno"}, None, id="BVA-05"),
    pytest.param({"kullanici_adi": "abcdefghijklmnop"}, AD_HATASI, id="BVA-06"),
    # Şifre: 8–20 karakter
    pytest.param({"sifre": "oyun123", "sifre_tekrar": "oyun123"}, SIFRE_HATASI, id="BVA-07"),
    pytest.param({"sifre": "oyun1234", "sifre_tekrar": "oyun1234"}, None, id="BVA-08"),
    pytest.param({"sifre": "oyun12345", "sifre_tekrar": "oyun12345"}, None, id="BVA-09"),
    pytest.param({"sifre": "oyun123456789012345", "sifre_tekrar": "oyun123456789012345"}, None, id="BVA-10"),
    pytest.param({"sifre": "oyun1234567890123456", "sifre_tekrar": "oyun1234567890123456"}, None, id="BVA-11"),
    pytest.param({"sifre": "oyun12345678901234567", "sifre_tekrar": "oyun12345678901234567"}, SIFRE_HATASI, id="BVA-12"),
    # Yaş: 13–99
    pytest.param({"yas": "12"}, YAS_HATASI, id="BVA-13"),
    pytest.param({"yas": "13"}, None, id="BVA-14"),
    pytest.param({"yas": "14"}, None, id="BVA-15"),
    pytest.param({"yas": "98"}, None, id="BVA-16"),
    pytest.param({"yas": "99"}, None, id="BVA-17"),
    pytest.param({"yas": "100"}, YAS_HATASI, id="BVA-18"),
])
def test_kayit_sinirlari(client, degisen, hata_mesaji):
    yanit = client.post("/kayit", data=kayit_verisi(**degisen))

    if hata_mesaji is None:
        assert yanit.status_code == 302, f"Kayıt başarılı olmalıydı, mesajlar: {mesajlar(yanit)}"
    else:
        assert yanit.status_code == 400
        assert hata_mesaji in mesajlar(yanit)


# ---------- Sepet: adet (tek seferde 1–5) ----------

@pytest.mark.parametrize("adet, hata_mesaji", [
    pytest.param("0", ADET_HATASI, id="BVA-19"),
    pytest.param("1", None, id="BVA-20"),
    pytest.param("2", None, id="BVA-21"),
    pytest.param("4", None, id="BVA-22"),
    pytest.param("5", None, id="BVA-23"),
    pytest.param("6", ADET_HATASI, id="BVA-24"),
])
def test_adet_sinirlari(girisli_client, adet, hata_mesaji):
    yanit = girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": adet})

    if hata_mesaji is None:
        assert yanit.status_code == 302
    else:
        assert yanit.status_code == 400
        assert hata_mesaji in mesajlar(yanit)


# ---------- Sepet: bir oyundan toplam en fazla 5 adet ----------

def test_bva25_sepette_4_varken_1_ekle(girisli_client):
    girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": "4"})
    yanit = girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": "1"})
    assert yanit.status_code == 302
    assert "3000 TL" in girisli_client.get("/sepet").text  # 5 x 600 TL


def test_bva26_sepette_5_varken_1_ekle(girisli_client):
    girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": "5"})
    yanit = girisli_client.post("/sepete-ekle", data={"oyun_id": "2", "adet": "1"})
    assert yanit.status_code == 400, "Sepette 5 adet varken 1 adet daha eklenebildi"
    assert "Bir oyundan en fazla 5 adet alınabilir." in mesajlar(yanit)