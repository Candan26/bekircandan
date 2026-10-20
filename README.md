# Op. Dr. Bangin Bekir Candan – Web Sitesi

Ortopedi ve Travmatoloji Uzmanı Op. Dr. Bangin Bekir Candan için tek sayfalık tanıtım sitesi (Doruk Nilüfer Hastanesi, Bursa).

## Yerelde çalıştırma
```bash
python -m http.server 5510
```
Ardından http://localhost:5510 adresini açın.

## Düzenleme
- **İletişim, videolar, Bilgi Köşesi serileri**: kök dizindeki `content.json`
  (YouTube videoları için tam link yeterli: `https://www.youtube.com/shorts/...`)
- **Metinler**: `index.html` (uzmanlık kartları hariç, onlar aşağıdaki tedavi sayfalarından üretilir)
- **Renkler / tasarım**: `assets/css/style.css` → `:root`

## Tedavi sayfaları (SEO)
Her tedavinin metni `content/tedaviler/<sayfa-adi>.md` dosyasındadır. Sayfalar `tools/build.py` ile üretilir:

```bash
python tools/build.py --inceleme
```
Tüm sayfaları "TASLAK" etiketiyle `_inceleme/site/` altına üretir ve hoca onayı için `_inceleme/tedavi-sayfalari-inceleme.pdf` hazırlar (bu klasör git'e girmez).

```bash
python tools/build.py
```
Siteyi üretir: sadece `onay: evet` olan sayfalar `tedaviler/` altına yazılır; ana sayfadaki uzmanlık kartlarında bu sayfalara link verilir; `sitemap.xml` ve `robots.txt` güncellenir. Onaysız sayfalara verilen metin içi linkler otomatik olarak düz yazıya çevrilir.

```bash
python tools/build.py --onizleme
```
Paylaşılabilir gizli önizleme: tüm sayfaları "TASLAK" etiketi ve `noindex` ile `onizleme/` altına üretir. Sitede bu sayfalara link yoktur ve sitemap'e girmezler; sadece linki bilenler görür (https://candan26.github.io/bekircandan/onizleme/). Metinler değişince yeniden çalıştırılmalı; tüm sayfalar onaylanınca `onizleme/` klasörü silinir.

**Onay süreci:** Hoca bir sayfayı onaylayınca ilgili `.md` dosyasında `onay: evet` yapılır ve `onay_tarihi: YYYY-AA-GG` satırı eklenir (sayfada "tıbbi içerik … tarafından incelenmiştir" notu bu tarihle çıkar). Ardından `python tools/build.py` çalıştırılıp commit edilir.

Alan adı bağlanınca `tools/build.py` içindeki `SITE_URL` güncellenip yeniden build alınmalıdır.

Analiz ve yapılacaklar listesi: [ANALIZ.md](ANALIZ.md)
