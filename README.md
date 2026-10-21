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
Siteyi üretir: `yayin: evet` (veya `onay: evet`) olan sayfalar `tedaviler/` altına yazılır; ana sayfadaki uzmanlık kartlarında bu sayfalara link ve "Tüm tedavi sayfaları" butonu çıkar; `sitemap.xml` ve `robots.txt` güncellenir. Yayında olmayan sayfalara verilen metin içi linkler otomatik olarak düz yazıya çevrilir. Eski `/onizleme/` linkleri yayındaki sayfalara yönlendirilir.

```bash
python tools/build.py --onizleme
```
Paylaşılabilir gizli önizleme (yeni taslaklar için): tüm sayfaları "TASLAK" etiketi ve `noindex` ile `onizleme/` altına üretir. Sitede bu sayfalara link yoktur ve sitemap'e girmezler; sadece linki bilenler görür (https://www.bekircandan.com/onizleme/). Metinler değişince yeniden çalıştırılmalı; tüm sayfalar onaylanınca `onizleme/` klasörü silinir.

**Yayın ve onay:** `yayin: evet` sayfayı sitede yayınlar. `onay` alanı hocanın metni okuyup onayladığını gösterir: hoca onaylayınca `onay: evet` yapılır ve `onay_tarihi: YYYY-AA-GG` satırı eklenir (sayfada "tıbbi içerik … tarafından incelenmiştir" notu bu tarihle çıkar). Ardından `python tools/build.py` çalıştırılıp commit edilir.

Alan adı bağlanınca `tools/build.py` içindeki `SITE_URL` güncellenip yeniden build alınmalıdır.

Analiz ve yapılacaklar listesi: [ANALIZ.md](ANALIZ.md)
