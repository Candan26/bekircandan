# Op. Dr. Bangin Bekir Candan – Web Sitesi Analiz & Yapılacaklar

## 1. Gelen materyal envanteri

| Kaynak | İçerik | Durum |
|---|---|---|
| `docs_material/*.zip` (13 adet) | 111 görsel → **94 benzersiz** (17 tekrar çıkarıldı) | ✅ incelendi |
| `docs_material/*.mp4` (14) + zip içi (2) | 16 dikey reels videosu (v01 ≈ v02 aynı içerik) | ✅ incelendi |
| `videos/v1.mp4` | Örnek sitenin (tanerbekmezci.com) ekran kaydı | ✅ referans |
| `screenshots/1-11.png` | Örnek sitenin ekran görüntüleri (anasayfa, hakkında, iletişim, randevu, menüler) | ✅ referans |
| `bekirCandanTxt.txt` | Notlar: YouTube kanalı, hastane, iletişim kalemleri, hizmet listesi | ✅ siteye işlendi |
| YouTube `@DrBanginBekirCandan` | 13 short video | ✅ siteye gömüldü |

### Görsellerin dağılımı
- **Doktor portreleri** (~35): ofis (Doruk logolu), beyaz önlük stüdyo, TV/basın röportajı, selfie'ler
- **Ameliyathane** (~20): artroskopi, ekip, ameliyat anı
- **Bilgilendirme görselleri / Instagram serileri** (~37), 6 seri:
  1. 30 yaşından sonra bırakmanız gereken 5 alışkanlık (6)
  2. Bu 5 basit hareketi deneyin (7)
  3. Kırıkları tanıyoruz (5)
  4. Ayakkabınız size ne anlatıyor? (7)
  5. Masa başı & duruş (5)
  6. Kemikleriniz tabağınızdaki seçimlerden etkileniyor (3)

### Videolar
- YouTube'da olanlar (13) → site **YouTube embed** kullanıyor (repo hafif kalır, izlenme kanala yazılır)
- YouTube'da **olmayanlar** → sıkıştırılıp siteye eklendi: *Okul çantası* (4 MB), *Omuz ameliyatları* (3.8 MB)

## 2. Örnek site (tanerbekmezci.com) analizi → bizdeki karşılığı

| Örnek sitede | Bizde |
|---|---|
| Üst bilgi şeridi (telefon, mail, sosyal) | ✅ Topbar: telefon, hastane, Instagram/YouTube/Facebook |
| Logo + yatay menü (alt menülü) | ✅ Sabit (sticky) menü + mobil hamburger menü |
| Büyük hero: doktor fotoğrafı + unvan + WhatsApp butonu | ✅ Hero: Doruk ofis fotoğrafı, unvan, uzmanlık etiketleri, Randevu + WhatsApp |
| "Uzman Hizmet" ikon kartları | ✅ 6 uzmanlık kartı (özel çizilmiş ikonlar) + üstte 4 hızlı kart |
| Hakkında – zaman çizelgesi (1993, 1999, 2004...) | ⚠️ Yapı hazır, **özgeçmiş bilgileri bekleniyor** |
| Çalışma saatleri kutusu | ❌ Bilgi yok (eklenecek) |
| Ameliyat örnekleri + videolar | ✅ Video bölümü (15 video) + ameliyathane galerisi |
| Online randevu formu | ✅ Form → WhatsApp'a hazır mesaj olarak gider (sunucu gerekmez) |
| İletişim + Google harita | ✅ İletişim kartları + Doruk Nilüfer Hastanesi haritası |
| Sabit WhatsApp butonu | ✅ WhatsApp + Ara butonu |
| Konu sayfaları (Diz protezi vb. ayrı sayfa) | 🔜 2. aşama (aşağıda) |

**Farklılaştırma:** Örnek site turkuaz/gri ve oldukça sade. Bizde Bekir Bey'in Instagram görsellerindeki **bordo + lacivert** kimlik kullanıldı (marka bütünlüğü), başlıklarda postlardaki kalın/dar font stili (Oswald), yumuşak animasyonlar, "Bilgi Köşesi" seri sekmeleri ve tam ekran görsel görüntüleyici eklendi.

## 3. Eksik bilgiler – Bekir Bey'den istenecek ❗
- [ ] **Telefon / WhatsApp numarası** (şu an "eklenecek" yazıyor; form da buna bağlı)
- [ ] **Facebook** sayfa linki
- [ ] **Özgeçmiş**: mezuniyet (okul/yıl), uzmanlık (kurum/yıl), önceki çalıştığı yerler, sertifika/kurslar, dernek üyelikleri
- [ ] Muayene / çalışma saatleri
- [ ] E-posta adresi (isteğe bağlı)
- [ ] Logo dosyası (postlarda görünen "Bangin Bekir Candan" logosu) – yüksek çözünürlüklü/PNG/SVG
- [ ] Alan adı tercihi (ör. `bekircandan.com`, `drbekircandan.com`)

## 4. Dikkat: Sağlık tanıtım mevzuatı ⚠️
Notlardaki "Bursa'da en iyi benim", "Bursa'da layıkıyla yapan 4 kişiden biri" gibi **karşılaştırmalı üstünlük ifadeleri siteye konmadı.** Sağlık Bakanlığı'nın sağlık hizmetleri tanıtım/reklam düzenlemeleri ve Türk Tabipleri Birliği etik kuralları hekimlerin kendini diğerlerinden üstün gösteren ifadeler kullanmasını yasaklıyor; şikâyet/ceza riski var. Bunun yerine deneyimi anlatan nötr ifadeler kullanılabilir (ör. "omuz ve ayak bileği artroskopisinde yoğun deneyim").
Ayrıca alt bilgide "bilgilendirme amaçlıdır, tanı/tedavi yerine geçmez" uyarısı ve formda KVKK onayı eklendi.

## 5. Yol haritası
**Aşama 1 – Base (şimdi)** ✅ Tek sayfa, tüm bölümler, mobil uyumlu, GitHub Pages'te yayın
**Aşama 2 – Feedback sonrası**
- [ ] Eksik bilgilerin eklenmesi (telefon, özgeçmiş, saatler)
- [ ] Her uzmanlık için ayrı detay sayfası (Diz protezi, Omuz artroskopisi, Halluks valgus... → SEO için kritik)
- [ ] Sık sorulan sorular (SSS) bölümü
- [ ] Hasta yorumları (mevzuata uygun şekilde, Google yorumları linki)
- [ ] Gerçek logo entegrasyonu
**Aşama 3 – Yayın**
- [ ] Alan adı + GitHub Pages bağlantısı (veya Netlify/Vercel)
- [ ] Google Business profili, Search Console, sitemap
- [ ] Randevu formunu e-postaya da düşürme (Formspree vb.)
- [ ] İngilizce dil seçeneği (istenirse)

## 6. Teknik
- Saf HTML/CSS/JS – derleme gerektirmez, GitHub Pages'te doğrudan çalışır
- Tüm iletişim bilgileri `assets/js/main.js` en üstündeki `CONFIG` bloğundan değiştirilir
- Video listesi `VIDEOS`, bilgi serileri `INFO` dizilerinden yönetilir
- Görseller WebP'ye çevrildi (toplam ~6.6 MB), sayfada lazy-load
