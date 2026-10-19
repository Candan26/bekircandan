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
- **Metinler / uzmanlık alanları**: `index.html`
- **Renkler / tasarım**: `assets/css/style.css` → `:root`

Analiz ve yapılacaklar listesi: [ANALIZ.md](ANALIZ.md)
