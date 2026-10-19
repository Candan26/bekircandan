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
| Hakkında – zaman çizelgesi (1993, 1999, 2004...) | ✅ Özgeçmiş + zaman çizelgesi eklendi (yıllar isteğe bağlı) |
| Çalışma saatleri kutusu | ✅ Pzt–Cmt 09.00–18.00 (üst şerit, randevu, iletişim, alt bilgi) |
| Ameliyat örnekleri + videolar | ✅ Video bölümü (15 video). Ameliyathane galerisi mevzuat nedeniyle kaldırıldı |
| Online randevu formu | ✅ Form → WhatsApp'a hazır mesaj olarak gider (sunucu gerekmez) |
| İletişim + Google harita | ✅ İletişim kartları + Doruk Nilüfer Hastanesi haritası |
| Sabit WhatsApp butonu | ✅ WhatsApp + Ara butonu |
| Konu sayfaları (Diz protezi vb. ayrı sayfa) | 🔜 2. aşama (aşağıda) |

**Farklılaştırma:** Örnek site turkuaz/gri ve oldukça sade. Bizde Bekir Bey'in Instagram görsellerindeki **bordo + lacivert** kimlik kullanıldı (marka bütünlüğü), başlıklarda postlardaki kalın/dar font stili (Oswald), yumuşak animasyonlar, "Bilgi Köşesi" seri sekmeleri ve tam ekran görsel görüntüleyici eklendi.

## 3. Eksik bilgiler – Bekir Bey'den istenecek ❗
- [x] Telefon: Doruk randevu hattı 444 0 455 kullanılıyor
- [x] WhatsApp: +90 545 545 91 09 (Bekir abinin cep numarası; sitede yazı olarak görünmez, sadece WhatsApp butonları ve randevu formu kullanır)
- [x] Hakkımda için güncel fotoğraf geldi (Doruk logolu beyaz önlük); Doruk lobisi fotoğrafı iletişim bölümüne eklendi
- [ ] **Facebook** sayfa linki
- [x] **Özgeçmiş** geldi ve eklendi
- [ ] (İsteğe bağlı) Özgeçmişe yıllar: tıp mezuniyeti, uzmanlık, her kurumda çalışma yılları; varsa sertifika/kurslar
- [x] Çalışma saatleri: Pazar hariç her gün 09.00–18.00
- [x] E-posta: bbekircandan@hotmail.com (".com" uzantısı teyit edilecek)
- [x] Logo geldi; ikon kısmı menüde, alt bilgide ve favicon'da kullanılıyor (vektörel SVG hali gelirse daha keskin olur)
- [ ] Alan adı tercihi (ör. `bekircandan.com`, `drbekircandan.com`)

## 4. Dikkat: Sağlık tanıtım mevzuatı ⚠️
Notlardaki "Bursa'da en iyi benim", "Bursa'da layıkıyla yapan 4 kişiden biri" gibi **karşılaştırmalı üstünlük ifadeleri siteye konmadı.** Sağlık Bakanlığı'nın sağlık hizmetleri tanıtım/reklam düzenlemeleri ve Türk Tabipleri Birliği etik kuralları hekimlerin kendini diğerlerinden üstün gösteren ifadeler kullanmasını yasaklıyor; şikâyet/ceza riski var. Bunun yerine deneyimi anlatan nötr ifadeler kullanılabilir (ör. "omuz ve ayak bileği artroskopisinde yoğun deneyim").
Ayrıca alt bilgide "bilgilendirme amaçlıdır, tanı/tedavi yerine geçmez" uyarısı ve formda KVKK onayı eklendi.

## 5. Feedback turları
**1. tur – Kübra Hanım (sosyal medya), 19.10.2026**
- [x] Ameliyathane galerisi tamamen kaldırıldı (mevzuat). Fotoğraflar repodan da silindi
- [x] Hero'daki hareketli kart yüzü kapatıyordu → fotoğrafın orta hizasına alındı
- [x] Hero'daki tekrar eden "Bursa · Doruk Nilüfer Hastanesi" satırı kaldırıldı (konum kartı zaten gösteriyor)
- [x] "Doruk Çağrı Merkezi" butonu yerine telefon alanında "Doruk Randevu Hattı · 444 0 455"
- [x] Hakkımda fotoğrafı güncellendi (20.10.2026)
- [x] SEO içerikleri: 26 tedavi sayfası yazıldı (`content/tedaviler/`), sayfa üretici `tools/build.py` hazır
- [ ] **Hoca onayı:** `_inceleme/tedavi-sayfalari-inceleme.pdf` gönderilecek; onaylanan sayfalar `onay: evet` yapılıp yayına alınacak. Çalışma `seo-sayfalar` dalında, onaya kadar GitHub'a gönderilmiyor
- [ ] Yayın sonrası: Google Search Console'a sitemap gönderimi (alan adı bağlandıktan sonra), Google Ads açılış sayfaları olarak tedavi sayfalarının kullanılması

## 6. Yol haritası
**Aşama 1 – Base (şimdi)** ✅ Tek sayfa, tüm bölümler, mobil uyumlu, GitHub Pages'te yayın
**Aşama 2 – Feedback sonrası**
- [ ] Eksik bilgilerin eklenmesi (telefon/WhatsApp, Facebook)
- [x] Her uzmanlık için ayrı detay sayfası (26 sayfa, hoca onayı bekliyor)
- [ ] Sık sorulan sorular (SSS) bölümü
- [ ] Hasta yorumları (mevzuata uygun şekilde, Google yorumları linki)
- [x] Logo entegrasyonu
- [ ] Renk kararı: site logodaki turkuaza geçirildi; eski bordo `?renk=bordo` ile görülebilir. Bekir abinin seçimine göre biri kalıcı olacak (karşılaştırma kodu sonra kaldırılır)
**Aşama 3 – Admin paneli (Cloudflare kararı verildi, feedback sonrasında yapılacak)**
Amaç: sosyal medya uzmanı GitHub'a girmeden video ve görselleri kendisi güncelleyebilsin.
- [x] İçerik `content.json`'a taşındı (videolar, bilgi serileri, iletişim)
- [ ] Çağrı: ücretsiz Cloudflare hesabı açıp GitHub (Candan26) bağlantısını yapacak
- [ ] Siteyi Cloudflare Pages'e taşı (GitHub'a her push'ta otomatik yayın); istenirse repo private
- [ ] `/admin` sayfası: Türkçe, mobil uyumlu, kullanıcı adı + şifre ile giriş
- [ ] Sunucu fonksiyonu (Pages Functions): şifre kontrolü + oturum çerezi; GitHub anahtarı sadece Cloudflare'de gizli değişken olarak durur
- [ ] Videolar: YouTube linki yapıştır → ekle / sil / sırala
- [ ] Bilgi Köşesi: seri ekle / sil, seriye görsel yükle (otomatik küçültme + WebP)
- [ ] "Yayınla" → değişiklik repoya commit edilir, site 1–2 dk'da güncellenir (her değişiklik geri alınabilir)
- [ ] İsteğe bağlı: iletişim bilgileri ve çalışma saatleri de panelden düzenlensin

**Aşama 4 – Yayın**
- [ ] Alan adı bağlantısı (Cloudflare DNS)
- [ ] Google Business profili, Search Console, sitemap
- [ ] Randevu formunu e-postaya da düşürme (Formspree vb.)
- [ ] İngilizce dil seçeneği (istenirse)

## 7. Teknik
- Saf HTML/CSS/JS – derleme gerektirmez, GitHub Pages'te doğrudan çalışır
- Düzenlenebilir tüm içerik (iletişim, videolar, bilgi serileri) `content.json` dosyasında; admin paneli bu dosyayı güncelleyecek
- Görseller WebP'ye çevrildi (toplam ~6.6 MB), sayfada lazy-load
