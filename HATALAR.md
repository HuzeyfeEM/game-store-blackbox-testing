# Hata Listesi – Mini Oyun Mağazası

Bu dosya projede bulunan bütün hataları tutar. Her yeni hata buraya eklenir.
Ekran görüntüleri `hata-fotograflari/` klasöründe saklanır. Her hata için 3 fotoğraf:
- `H-XX-1-hata.png`: sitede hatanın göründüğü ekran
- `H-XX-2-test-basarisiz.png`: pytest çıktısı, test kırmızı (FAILED)
- `H-XX-3-test-basarili.png`: düzeltmeden sonra pytest çıktısı, test yeşil (PASSED)

**Durum:** 🔴 Açık = düzeltilmedi, 🟢 Kapalı = düzeltildi ve test tekrar başarılı

| ID   | Kısa açıklama                                                       | Nasıl bulundu                           | Test tekniği         | Durum   |
|------|---------------------------------------------------------------------|-----------------------------------------|----------------------|---------|
| H-01 | Tam 8 karakterli şifre reddediliyor                                 | Bilerek eklendi                         | Sınır Değer Analizi  | 🔴 Açık |
| H-02 | Büyük/küçük harf farklı aynı e-posta ile ikinci kayıt yapılabiliyor | Bilerek eklendi                         | Eşdeğerlik Bölümleme | 🔴 Açık |
| H-03 | Çıkış yapınca oturum kapanmıyor                                     | Bilerek eklendi, manuel testte görüldü  | Durum Geçiş Testi    | 🔴 Açık |
| H-04 | Sepete tek tek eklenince bir oyundan 5'ten fazla alınabiliyor       | Manuel test sırasında tesadüfen bulundu | Sınır Değer Analizi  | 🔴 Açık |
| H-05 | Negatif adet girilince yanlış hata mesajı çıkıyor                   | pytest testi (EP-21) ile bulundu        | Eşdeğerlik Bölümleme | 🔴 Açık |

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
- **Ekran görüntüleri:** `H-01-1-hata.png`, `H-01-2-test-basarisiz.png`, `H-01-3-test-basarili.png`

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
- **Ekran görüntüleri:** `H-02-1-hata.png`, `H-02-2-test-basarisiz.png`, `H-02-3-test-basarili.png`

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
- **Ekran görüntüleri:** `H-03-1-hata.png`, `H-03-2-test-basarisiz.png`, `H-03-3-test-basarili.png`

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
- **Ekran görüntüleri:** `H-04-1-hata.png`, `H-04-2-test-basarisiz.png`, `H-04-3-test-basarili.png`

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
- **Ekran görüntüleri:** `H-05-1-hata.png`, `H-05-2-test-basarisiz.png`, `H-05-3-test-basarili.png`
