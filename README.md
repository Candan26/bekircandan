# Op. Dr. Bangin Bekir Candan – Web Sitesi

Ortopedi ve Travmatoloji Uzmanı Op. Dr. Bangin Bekir Candan için tek sayfalık tanıtım sitesi (Doruk Nilüfer Hastanesi, Bursa).

## Yerelde çalıştırma
```bash
python -m http.server 5510
```
Ardından http://localhost:5510 adresini açın.

## Düzenleme
- **İletişim bilgileri** (telefon, WhatsApp, sosyal medya): `assets/js/main.js` → `CONFIG`
- **Videolar**: `assets/js/main.js` → `VIDEOS` (YouTube ID veya yerel mp4)
- **Bilgi Köşesi serileri**: `assets/js/main.js` → `INFO` + `assets/img/info/`
- **Metinler / uzmanlık alanları**: `index.html`
- **Renkler / tasarım**: `assets/css/style.css` → `:root`

Analiz ve yapılacaklar listesi: [ANALIZ.md](ANALIZ.md)
