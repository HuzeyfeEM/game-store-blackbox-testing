# Hata Düzeltme Rehberi – Sunum İçin

Bu dosya, hataların **hocanın önünde canlı olarak** düzeltilmesi için hazırlandı.
Her hata için: kodun yeri, hatalı kod, düzeltilmiş kod, neden düzelttiğimiz, testi çalıştırma komutu ve sitede nasıl gösterileceği yazılıdır.

> **Satır numaraları** hatalı sürüme (`hatali-surum`) göredir. Düzeltme yaptıkça alttaki satırlar kayabilir.
> Kodu bulmak için VS Code'da **Ctrl + F** ile "Aranacak metin" kısmını ara veya **Ctrl + G** ile satıra git.

---

## Sunum öncesi hazırlık

1. Hatalı sürüme geç (sadece sunumdan önce, tek sefer):
   ```
   git checkout hatali-surum
   ```
2. Tüm testleri çalıştır, **7 başarısız** testi göster:
   ```
   py -m pytest tests -v
   ```
3. Siteyi ayrı bir terminalde çalıştır (düzeltmeler sırasında açık kalabilir, `debug=True` sayesinde kod değişince kendini yeniler):
   ```
   py app.py
   ```
4. Sitede denemeler için her zaman **gizli pencere** kullan (**Ctrl + Shift + N**).

---

## Her hata için çekilecek 6 fotoğraf

| No  | Dosya adı                    | Ne gösterir?                      | Durum    |
|-----|------------------------------|-----------------------------------|----------|
| 1   | `H-XX-1-hata.png`            | Sitede hatanın görünmesi          | ✅ Hazır |
| 2   | `H-XX-2-test-basarisiz.png`  | pytest çıktısı: FAILED            | ✅ Hazır |
| 3   | `H-XX-3-hatali-kod.png`      | VS Code'da hatalı kod satırı      | ⏳       |
| 4   | `H-XX-4-duzeltilmis-kod.png` | VS Code'da düzeltilmiş kod satırı | ⏳       |
| 5   | `H-XX-5-test-basarili.png`   | pytest çıktısı: PASSED            | ⏳       |
| 6   | `H-XX-6-sitede-duzeldi.png`  | Sitede doğru davranış             | ⏳       |

---

## H-01: Tam 8 karakterli şifre reddediliyor

- **Dosya / fonksiyon:** `app.py` → `kayit()` – **satır 50**
- **Aranacak metin:** `len(sifre) <= 8`
- **Hatalı kod:**
  ```python
  if len(sifre) <= 8 or len(sifre) > 20:
  ```
- **Düzeltilmiş kod:**
  ```python
  if len(sifre) < 8 or len(sifre) > 20:
  ```
- **Açıklama:** `<= 8` ifadesi 8'i de hatalı sayıyordu. Kurala göre 8 karakter **geçerli**. Sadece `=` işaretini sildik. Bu, Sınır Değer Analizi'nin yakaladığı tipik bir "sınırda bir kayma" hatasıdır.
- **Test komutu:**
  ```
  py -m pytest tests -v -k "BVA-08"
  ```
- **Sitede gösterme:** `/kayit` → `mehmet` / `mehmet@test.com` / şifre `oyun1234` (2 kez) / yaş `20` → **"Kayıt başarılı!"** mesajı görünmeli.

---

## H-02: Büyük/küçük harf farklı aynı e-posta ile ikinci kayıt yapılabiliyor

- **Dosya / fonksiyon:** `app.py` → `kayit()` – **satır 47**
- **Aranacak metin:** `k["email"] == email`
- **Hatalı kod:**
  ```python
  if k["email"] == email:
  ```
- **Düzeltilmiş kod:**
  ```python
  if k["email"].lower() == email.lower():
  ```
- **Açıklama:** E-posta adreslerinde büyük/küçük harf fark etmez (`ALI@test.com` = `ali@test.com`). `.lower()` iki adresi de küçük harfe çevirip öyle karşılaştırır.
- **Test komutu:**
  ```
  py -m pytest tests -v -k "EP-09"
  ```
- **Sitede gösterme:** Önce `ali` / `ali@test.com` ile kayıt ol. Sonra `veli` / `ALI@test.com` ile kayıt ol → **"Bu e-posta zaten kayıtlı."** mesajı görünmeli.

---

## H-03: Çıkış yapınca oturum kapanmıyor

- **Dosya / fonksiyon:** `app.py` → `cikis()` – **satır 177–179**
- **Aranacak metin:** `def cikis`
- **Hatalı kod:**
  ```python
  def cikis():
      flash("Başarıyla çıkış yaptınız.")
      return redirect(url_for("ana_sayfa"))
  ```
- **Düzeltilmiş kod:**
  ```python
  def cikis():
      session.clear()
      flash("Başarıyla çıkış yaptınız.")
      return redirect(url_for("ana_sayfa"))
  ```
- **Açıklama:** Fonksiyon sadece mesaj gösteriyordu, oturumdaki kullanıcıyı silmiyordu. `session.clear()` oturumdaki her şeyi (kullanıcı, sepet) siler. **Sıra önemli:** `session.clear()` mutlaka `flash(...)` satırından **önce** olmalı. Sonra olursa çıkış mesajı da silinir.
- **Test komutu** (3 test birden):
  ```
  py -m pytest tests -v -k "st10 or st11 or st12"
  ```
- **Sitede gösterme:** Giriş yap → "Çıkış Yap" → sağ üstte **"Giriş Yap / Kayıt Ol"** görünmeli. Sonra `/oyunlar` adresine git → giriş sayfasına yönlendirilmeli.

---

## H-04: Sepete tek tek eklenince bir oyundan 5'ten fazla alınabiliyor

- **Dosya / fonksiyon:** `app.py` → `sepete_ekle()` – **satır 137–138**
- **Aranacak metin:** `sepet = session.get("sepet", {})`
- **Hatalı kod:**
  ```python
  sepet = session.get("sepet", {})
  sepet[oyun_id] = sepet.get(oyun_id, 0) + int(adet)
  ```
- **Düzeltilmiş kod** (araya 3 satır eklenir):
  ```python
  sepet = session.get("sepet", {})
  if sepet.get(oyun_id, 0) + int(adet) > 5:
      flash("Bir oyundan en fazla 5 adet alınabilir.")
      return render_template("oyunlar.html", oyunlar=OYUNLAR, kullanici=session["kullanici"]), 400
  sepet[oyun_id] = sepet.get(oyun_id, 0) + int(adet)
  ```
- **Açıklama:** Kod sadece **o an girilen** adete bakıyordu. Artık **sepette zaten olan adet + yeni adet** toplamına bakıyor. Toplam 5'i geçerse ekleme yapılmıyor.
- **Test komutu:**
  ```
  py -m pytest tests -v -k "bva25 or bva26"
  ```
  (BVA-25 de çalıştırılır: tam 5 olunca hâlâ eklenebildiğini gösterir.)
- **Sitede gösterme:** Giriş yap → bir oyunu 5 adet ekle → aynı oyunu 1 adet daha ekle → **"Bir oyundan en fazla 5 adet alınabilir."** mesajı görünmeli, sepette 5 adet kalmalı.

---

## H-05: Negatif adet girilince yanlış hata mesajı çıkıyor

- **Dosya / fonksiyon:** `app.py` → `sepete_ekle()` – **satır 130**
- **Aranacak metin:** `adet.isdigit()`
- **Hatalı kod:**
  ```python
  if not adet.isdigit():
  ```
- **Düzeltilmiş kod:**
  ```python
  if not adet.lstrip("-").isdigit():
  ```
- **Açıklama:** `isdigit()` eksi işaretini (`-`) rakam saymaz. Bu yüzden `-2` "sayı değil" kabul ediliyordu. `lstrip("-")` baştaki eksi işaretini silip öyle kontrol eder. Böylece `-2` sayı kabul edilir ve bir sonraki kontrol (1–5 aralığı) doğru mesajı verir.
- **Test komutu:**
  ```
  py -m pytest tests -v -k "EP-21"
  ```
- **Sitede gösterme:** Giriş yap → adet alanına `-2` yaz → **"Adet 1 ile 5 arasında olmalıdır."** mesajı görünmeli.

---

## Son adım: Tüm testler

Bütün düzeltmelerden sonra:
```
py -m pytest tests -v
```
Beklenen sonuç: **62 passed, 0 failed** ✅
📸 `test-ciktilari/TUM-TESTLER-duzeltme-sonrasi.png`

Her düzeltmeden sonra commit önerisi:
```
git add .
git commit -m "H-01 duzeltildi: 8 karakterli sifre kabul ediliyor"
```
