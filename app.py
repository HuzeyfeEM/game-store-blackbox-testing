import re
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "gizli-anahtar"

kullanicilar = {}

basarisiz_denemeler = {}

OYUNLAR = [
    {"id": 1, "ad": "Valorant Points 1000", "fiyat": 250},
    {"id": 2, "ad": "Minecraft", "fiyat": 600},
    {"id": 3, "ad": "FIFA 26", "fiyat": 1500},
]


@app.route("/")
def ana_sayfa():
    return render_template("ana_sayfa.html")


@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    if request.method == "POST":
        kullanici_adi = request.form.get("kullanici_adi", "").strip()
        email = request.form.get("email", "").strip()
        sifre = request.form.get("sifre", "")
        sifre_tekrar = request.form.get("sifre_tekrar", "")
        yas = request.form.get("yas", "").strip()

        if not kullanici_adi or not email or not sifre or not yas:
            flash("Tüm alanlar doldurulmalıdır.")
            return render_template("kayit.html"), 400

        hatalar = []

        if len(kullanici_adi) < 3 or len(kullanici_adi) > 15:
            hatalar.append("Kullanıcı adı 3-15 karakter olmalıdır.")
        elif kullanici_adi in kullanicilar:
            hatalar.append("Bu kullanıcı adı zaten alınmış.")

        if not re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$", email):
            hatalar.append("Geçerli bir e-posta adresi giriniz.")
        else:
            for k in kullanicilar.values():
                if k["email"].lower() == email.lower():    
                    hatalar.append("Bu e-posta zaten kayıtlı.")

        if len(sifre) < 8 or len(sifre) > 20:  
            hatalar.append("Şifre 8-20 karakter olmalıdır.")
        if sifre != sifre_tekrar:
            hatalar.append("Şifreler eşleşmiyor.")

        if not yas.isdigit():
            hatalar.append("Yaş bir sayı olmalıdır.")
        elif int(yas) < 13 or int(yas) > 99:
            hatalar.append("Yaş 13 ile 99 arasında olmalıdır.")

        if hatalar:
            for hata in hatalar:
                flash(hata)
            return render_template("kayit.html"), 400

        kullanicilar[kullanici_adi] = {"email": email, "sifre": sifre, "yas": int(yas)}
        flash("Kayıt başarılı! Giriş yapabilirsiniz.")
        return redirect(url_for("giris"))

    return render_template("kayit.html")

@app.route("/giris", methods=["GET", "POST"])
def giris():
    if "kullanici" in session:
        return redirect(url_for("oyunlar"))

    if request.method == "POST":
        kullanici_adi = request.form.get("kullanici_adi", "").strip()
        sifre = request.form.get("sifre", "")

        if not kullanici_adi or not sifre:
            flash("Kullanıcı adı ve şifre boş bırakılamaz.")
            return render_template("giris.html"), 400

        if basarisiz_denemeler.get(kullanici_adi, 0) >= 3:
            flash("Hesabınız kilitlendi. Çok fazla hatalı deneme yapıldı.")
            return render_template("giris.html"), 403

        kullanici = kullanicilar.get(kullanici_adi)
        if kullanici is None or kullanici["sifre"] != sifre:
            basarisiz_denemeler[kullanici_adi] = basarisiz_denemeler.get(kullanici_adi, 0) + 1
            flash("Kullanıcı adı veya şifre hatalı.")
            return render_template("giris.html"), 401

        basarisiz_denemeler[kullanici_adi] = 0
        session["kullanici"] = kullanici_adi
        flash(f"Giriş başarılı. Hoş geldin, {kullanici_adi}!")
        return redirect(url_for("oyunlar"))

    return render_template("giris.html")


@app.route("/oyunlar")
def oyunlar():
    if "kullanici" not in session:
        flash("Bu sayfayı görmek için giriş yapmalısınız.")
        return redirect(url_for("giris"))
    return render_template("oyunlar.html", oyunlar=OYUNLAR, kullanici=session["kullanici"])


@app.route("/sepete-ekle", methods=["POST"])
def sepete_ekle():
    if "kullanici" not in session:
        flash("Bu işlem için giriş yapmalısınız.")
        return redirect(url_for("giris"))

    oyun_id = request.form.get("oyun_id", "")
    adet = request.form.get("adet", "").strip()

    oyun = None
    for o in OYUNLAR:
        if str(o["id"]) == oyun_id:
            oyun = o
    if oyun is None:
        flash("Oyun bulunamadı.")
        return render_template("oyunlar.html", oyunlar=OYUNLAR, kullanici=session["kullanici"]), 404

    if not adet:
        flash("Adet boş bırakılamaz.")
        return render_template("oyunlar.html", oyunlar=OYUNLAR, kullanici=session["kullanici"]), 400
    if not adet.isdigit():
        flash("Adet bir sayı olmalıdır.")
        return render_template("oyunlar.html", oyunlar=OYUNLAR, kullanici=session["kullanici"]), 400
    if int(adet) < 1 or int(adet) > 5:
        flash("Adet 1 ile 5 arasında olmalıdır.")
        return render_template("oyunlar.html", oyunlar=OYUNLAR, kullanici=session["kullanici"]), 400

    sepet = session.get("sepet", {})
    sepet[oyun_id] = sepet.get(oyun_id, 0) + int(adet)
    session["sepet"] = sepet
    flash(f"{oyun['ad']} sepete eklendi ({adet} adet).")
    return redirect(url_for("sepet"))


@app.route("/sepet")
def sepet():
    if "kullanici" not in session:
        flash("Sepeti görmek için giriş yapmalısınız.")
        return redirect(url_for("giris"))

    urunler = []
    toplam = 0
    for oyun in OYUNLAR:
        adet = session.get("sepet", {}).get(str(oyun["id"]), 0)
        if adet > 0:
            ara_toplam = adet * oyun["fiyat"]
            urunler.append({"ad": oyun["ad"], "adet": adet, "ara_toplam": ara_toplam})
            toplam += ara_toplam

    return render_template("sepet.html", urunler=urunler, toplam=toplam)


@app.route("/satin-al", methods=["POST"])
def satin_al():
    if "kullanici" not in session:
        flash("Bu işlem için giriş yapmalısınız.")
        return redirect(url_for("giris"))

    if not session.get("sepet"):
        flash("Sepetiniz boş.")
        return redirect(url_for("sepet"))

    session["sepet"] = {}
    flash("Satın alma başarılı! Teşekkür ederiz.")
    return redirect(url_for("oyunlar"))

@app.route("/cikis")
def cikis():
    session.clear()  
    flash("Başarıyla çıkış yaptınız.")
    return redirect(url_for("ana_sayfa"))

if __name__ == "__main__":
    app.run(debug=True)
