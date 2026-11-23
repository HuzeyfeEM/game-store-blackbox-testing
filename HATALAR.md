# Hata Listesi – Mini Oyun Mağazası

Bu dosya projede bulunan bütün hataları tutar. Her yeni hata buraya eklenir.
Ekran görüntüleri `hata-fotograflari/` klasöründe saklanır. Her hata için 6 tür fotoğraf vardır (bazılarında a, b, c... diye birden fazla parça):
- `H-XX-1-hata.png`: sitede hatanın göründüğü ekran
- `H-XX-2-test-basarisiz.png`: pytest çıktısı, test kırmızı (FAILED)
- `H-XX-3-hatali-kod.png`: VS Code'da hatalı kod
- `H-XX-4-duzeltilmis-kod.png`: VS Code'da düzeltilmiş kod
- `H-XX-5-test-basarili.png`: düzeltmeden sonra pytest çıktısı, test yeşil (PASSED)
- `H-XX-6-sitede-duzeldi.png`: sitede doğru davranış

**Durum:** 🔴 Açık = düzeltilmedi, 🟢 Kapalı = düzeltildi ve test tekrar başarılı

| ID   | Kısa açıklama                                                       | Nasıl bulundu                           | Test tekniği         | Durum     |
|------|---------------------------------------------------------------------|-----------------------------------------|----------------------|-----------|
| H-01 | Tam 8 karakterli şifre reddediliyor                                 | Bilerek eklendi                         | Sınır Değer Analizi  | 🟢 Kapalı |
| H-02 | Büyük/küçük harf farklı aynı e-posta ile ikinci kayıt yapılabiliyor | Bilerek eklendi                         | Eşdeğerlik Bölümleme | 🟢 Kapalı |
| H-03 | Çıkış yapınca oturum kapanmıyor                                     | Bilerek eklendi, manuel testte görüldü  | Durum Geçiş Testi    | 🟢 Kapalı |
| H-04 | Sepete tek tek eklenince bir oyundan 5'ten fazla alınabiliyor       | Manuel test sırasında tesadüfen bulundu | Sınır Değer Analizi  | 🟢 Kapalı |
| H-05 | Negatif adet girilince yanlış hata mesajı çıkıyor                   | pytest testi (EP-21) ile bulundu        | Eşdeğerlik Bölümleme | 🟢 Kapalı |

---

## H-01: Tam 8 karakterli şifre reddediliyor

- **Yer:** `app.py` → `kayit()` fonksiyonu
- **Hatalı kod:** `if len(sifre) <= 8 or len(sifre) > 20:`
- **Doğru kod:** `if len(sifre) < 8 or len(sifre) > 20:`
- **Kural:** Şifre 8–20 karakter olmalı (8 dahil).
- **Oluşturma adımları:**
  1. `/kayit` sayfasını aç.
  2. Şifre ve şifre tekrar alanına tam 8 karakter yaz (örnek: `abcdefgh`).
  3. Diğer alanları geçerli doldur ve "Kayıt Ol"a bas.
- **Beklenen:** Kayıt başarılı olmalı.
- **Gerçekleşen:** "Şifre 8-20 karakter olmalıdır." hatası çıkıyor.
- **Yakalayan test(ler):** BVA-08
- **Ekran görüntüleri:** `H-01-1-hata.png`, `H-01-2-test-basarisiz.png`, `H-01-3-hatali-kod.png`, `H-01-4-duzeltilmis-kod.png`, `H-01-5-test-basarili.png`, `H-01-6a-sitede-form.png`, `H-01-6b-sitede-duzeldi.png`

## H-02: Büyük/küçük harf farklı aynı e-posta ile ikinci kayıt yapılabiliyor

- **Yer:** `app.py` → `kayit()` fonksiyonu
- **Hatalı kod:** `if k["email"] == email:`
- **Doğru kod:** `if k["email"].lower() == email.lower():`
- **Kural:** Bir e-posta adresiyle sadece bir hesap açılabilir. E-posta adreslerinde büyük/küçük harf fark etmez.
- **Oluşturma adımları:**
  1. `ali@test.com` ile kayıt ol.
  2. Başka bir kullanıcı adıyla `ALI@test.com` kullanarak tekrar kayıt ol.
- **Beklenen:** "Bu e-posta zaten kayıtlı." hatası çıkmalı.
- **Gerçekleşen:** İkinci kayıt başarılı oluyor.
- **Yakalayan test(ler):** EP-09
- **Ekran görüntüleri:** `H-02-1a-hata-form.png`, `H-02-1b-hata-sonuc.png`, `H-02-2-test-basarisiz.png`, `H-02-3-hatali-kod.png`, `H-02-4-duzeltilmis-kod.png`, `H-02-5-test-basarili.png`, `H-02-6a-ilk-kayit-ali.png`, `H-02-6b-sitede-duzeldi.png`

## H-03: Çıkış yapınca oturum kapanmıyor

- **Yer:** `app.py` → `cikis()` fonksiyonu
- **Hatalı kod:** Fonksiyon `session` içindeki kullanıcıyı silmiyor.
- **Doğru kod:** `flash(...)` satırından önce `session.clear()` eklenmeli.
- **Kural:** Çıkış yapan kullanıcı korumalı sayfalara (`/oyunlar`, `/sepet`) girememeli.
- **Oluşturma adımları:**
  1. Giriş yap.
  2. "Çıkış Yap"a bas ("Başarıyla çıkış yaptınız." mesajı görünür).
  3. `/oyunlar` sayfasına git.
- **Beklenen:** Giriş sayfasına yönlendirilmeli.
- **Gerçekleşen:** Oyunlar sayfası açılıyor, menüde hâlâ kullanıcı adı görünüyor. Giriş sayfasına basınca eski hesaba otomatik giriş yapılıyor.
- **Yakalayan test(ler):** ST-10, ST-11, ST-12
- **Ekran görüntüleri:** `H-03-1a-giris-yapildi.png`, `H-03-1b-hata-cikis-sonrasi.png`, `H-03-2a-test-basarisiz-ST10.png`, `H-03-2b-test-basarisiz-ST11.png`, `H-03-2c-test-basarisiz-ST12.png`, `H-03-3-hatali-kod.png`, `H-03-4-duzeltilmis-kod.png`, `H-03-5-test-basarili.png`, `H-03-6a-giris-yapildi.png`, `H-03-6b-sitede-duzeldi-cikis.png`, `H-03-6c-adres-oyunlar.png`, `H-03-6d-girise-yonlendirildi.png`

## H-04: Sepete tek tek eklenince bir oyundan 5'ten fazla alınabiliyor

- **Yer:** `app.py` → `sepete_ekle()` fonksiyonu
- **Hatalı kod:** Sadece girilen adet kontrol ediliyor (1–5). Sepetteki mevcut adet hesaba katılmıyor.
- **Doğru kod:** Ekleme öncesinde `mevcut + yeni adet > 5` kontrolü yapılmalı.
- **Kural:** Sepette bir oyundan en fazla 5 adet olabilir.
- **Oluşturma adımları:**
  1. Giriş yap.
  2. Bir oyunu 5 adet sepete ekle.
  3. Aynı oyunu 1 adet daha ekle.
- **Beklenen:** "Bir oyundan en fazla 5 adet alınabilir." gibi bir hata çıkmalı.
- **Gerçekleşen:** Sepette 6 adet görünüyor.
- **Yakalayan test(ler):** BVA-26
- **Ekran görüntüleri:** `H-04-1a-sepette-5-adet.png`, `H-04-1b-hata-sepette-6-adet.png`, `H-04-2-test-basarisiz.png`, `H-04-3-hatali-kod.png`, `H-04-4-duzeltilmis-kod.png`, `H-04-5-test-basarili.png`, `H-04-6-sitede-duzeldi.png`

## H-05: Negatif adet girilince yanlış hata mesajı çıkıyor

- **Yer:** `app.py` → `sepete_ekle()` fonksiyonu
- **Hatalı kod:** `if not adet.isdigit():` — `isdigit()` eksi işaretini (`-`) rakam saymaz. Bu yüzden `-2` bir sayı olduğu hâlde "sayı değil" kabul ediliyor.
- **Doğru kod:** Önce sayıya çevirmeyi denemek (`int(adet)`), sonra 1–5 aralığını kontrol etmek. Örnek: `if not adet.lstrip("-").isdigit():`
- **Kural:** 1'den küçük bir sayı girilirse "Adet 1 ile 5 arasında olmalıdır." mesajı çıkmalı.
- **Oluşturma adımları:**
  1. Giriş yap.
  2. Oyunlar sayfasında bir oyunun adet alanına `-2` yaz.
  3. "Sepete Ekle" butonuna bas.
- **Beklenen:** 400, "Adet 1 ile 5 arasında olmalıdır."
- **Gerçekleşen:** 400, "Adet bir sayı olmalıdır." (Ürün sepete eklenmiyor, ama kullanıcıya yanlış bilgi veriliyor.)
- **Yakalayan test(ler):** EP-21
- **Ekran görüntüleri:** `H-05-1-hata.png`, `H-05-2-test-basarisiz.png`, `H-05-3-hatali-kod.png`, `H-05-4-duzeltilmis-kod.png`, `H-05-5-test-basarili.png`, `H-05-6-sitede-duzeldi.png`

---

## Düzeltme sonrası

Bütün hatalar düzeltildi ve **aynı testler yeniden çalıştırıldı.** Düzeltmeler için bkz. `DUZELTME_REHBERI.md`.

| Hata | Düzeltme                          | Tekrar çalıştırılan test(ler) | Sonuç     |
|------|-----------------------------------|-------------------------------|-----------|
| H-01 | `<= 8` → `< 8`                    | BVA-08                        | ✅ PASSED |
| H-02 | `.lower()` ile karşılaştırma      | EP-09                         | ✅ PASSED |
| H-03 | `cikis()` içine `session.clear()` | ST-10, ST-11, ST-12           | ✅ PASSED |
| H-04 | Sepetteki toplam adet kontrolü    | BVA-25, BVA-26                | ✅ PASSED |
| H-05 | `adet.lstrip("-").isdigit()`      | EP-21                         | ✅ PASSED |
