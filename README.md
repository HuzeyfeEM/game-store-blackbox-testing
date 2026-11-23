# Game Store – Black-Box Testing

Fırat Üniversitesi, **Yazılım Geçerleme ve Sınama** dersi grup projesi (Grup 28).

Flask ile yazılmış küçük bir oyun mağazası uygulaması (**Mini Oyun Mağazası**) ve bu uygulamanın **kara kutu test teknikleriyle** test edilmesi:

- Eşdeğerlik Bölümleme (24 test)
- Sınır Değer Analizi (26 test)
- Durum Geçiş Testi (12 test)

Testler **pytest** ile otomatikleştirildi. Testler 5 hata buldu, hatalar düzeltildi ve bütün testler tekrar çalıştırıldı.

| Sürüm (Git etiketi) | Sonuç               |
|---------------------|---------------------|
| `hatali-surum`      | 55 passed, 7 failed |
| `duzeltilmis-surum` | 62 passed           |

## Çalıştırma

```
py -m pip install -r requirements.txt
py app.py                 # site: http://127.0.0.1:5000
py -m pytest tests -v     # testler
```

## Belgeler

| Dosya                                   | İçerik                                               |
|-----------------------------------------|------------------------------------------------------|
| `anlatim/`                              | Projenin anlatımı ve sunum parçaları (buradan başla) |
| `TEST_SENARYOLARI.md`                   | 62 test senaryosu ve sonuçları                       |
| `HATALAR.md`                            | Bulunan 5 hatanın raporu                             |
| `DUZELTME_REHBERI.md`                   | Hataların nasıl düzeltildiği                         |
| `diyagramlar/`                          | Durum geçiş diyagramı                                |
| `hata-fotograflari/`, `test-ciktilari/` | Ekran görüntüleri                                    |
