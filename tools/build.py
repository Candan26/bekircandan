"""Tedavi sayfalarını content/tedaviler/*.md dosyalarından üretir.

Kullanım (website klasöründen):
  python tools/build.py             Site: `yayin: evet` veya `onay: evet` olan sayfaları üretir,
                                     ana sayfadaki tedavi listesini, sitemap.xml ve robots.txt'yi günceller.
  python tools/build.py --inceleme  Hoca onayı için: tüm sayfaları "TASLAK" etiketiyle _inceleme/site/
                                     altına üretir ve _inceleme/tedavi-sayfalari-inceleme.pdf hazırlar.
  python tools/build.py --onizleme  Paylaşılabilir gizli önizleme: tüm sayfaları "TASLAK" etiketi ve
                                     noindex ile onizleme/ altına üretir (sitede link yok, sitemap'te yok).

Ortak üst menü, alt bilgi ve ikonlar index.html'deki SHARED işaretleri arasından alınır.
"""
import datetime
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from string import Template

import markdown

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content' / 'tedaviler'
REVIEW = ROOT / '_inceleme'

# Alan adı bağlanınca burası değişecek (sonunda / olmadan)
SITE_URL = 'https://www.bekircandan.com'

DOCTOR = 'Op. Dr. Bangin Bekir Candan'
CATEGORIES = [
    # id, başlık, alt başlık, ikon
    ('protez', 'Artroplasti', 'Protez Ameliyatları', 's-knee'),
    ('artroskopi', 'Artroskopi', 'Kapalı – Kamerayla Cerrahi', 's-scope'),
    ('kirik', 'Kırık &amp; Travma Cerrahisi', '', 's-bone'),
    ('el', 'El Cerrahisi', '', 's-hand'),
    ('ayak', 'Ayak Cerrahisi', '', 's-foot'),
    ('eklem', 'Eklem Hastalıkları &amp; Çıkıklar', '', 's-hip'),
]
CAT = {c[0]: c for c in CATEGORIES}
FAQ_HEADING = 'Sık Sorulan Sorular'


# ---------------------------------------------------------------- okuma
TR = str.maketrans('çğıöşüÇĞİÖŞÜâîû', 'cgiosucgiosuaiu')


def slugify(value, separator='-'):
    value = value.translate(TR).lower()
    return re.sub(r'[^a-z0-9]+', separator, value).strip(separator)


def parse(path):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    if not m:
        sys.exit(f'{path.name}: başta --- ile ayrılmış bilgi bloğu yok')
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    for key in ('baslik', 'seo_baslik', 'aciklama', 'kategori', 'kisa_ad', 'sira', 'tur', 'onay'):
        if key not in meta:
            sys.exit(f'{path.name}: "{key}" alanı eksik')
    if meta['kategori'] not in CAT:
        sys.exit(f'{path.name}: bilinmeyen kategori "{meta["kategori"]}"')
    meta['slug'] = path.stem
    meta['sira'] = int(meta['sira'])
    # onay: hoca metni okudu (sayfada 'incelenmiştir' notu çıkar) · yayin: sayfa sitede yayında
    meta['onayli'] = meta['onay'].lower() in ('evet', 'yes', 'true')
    meta['yayin'] = meta.get('yayin', 'hayır').lower() in ('evet', 'yes', 'true')
    meta['ilgili'] = [s.strip() for s in meta.get('ilgili', '').split(',') if s.strip()]
    meta['body_md'] = m.group(2).strip()
    return meta


def render_body(md_text):
    md = markdown.Markdown(extensions=['toc', 'sane_lists'],
                           extension_configs={'toc': {'slugify': lambda v, sep: slugify(v, sep)}})
    body = md.convert(md_text)
    toc = [(t['id'], t['name']) for t in md.toc_tokens if t['level'] == 2]
    # "Sık Sorulan Sorular" altındaki ### soruları açılır-kapanır kutulara çevir
    m = re.search(r'<h2 id="[^"]*">' + FAQ_HEADING + r'</h2>', body)
    faq = []
    if m:
        head, rest = body[:m.end()], body[m.end():]
        nxt = re.search(r'<h2 ', rest)
        faq_html, tail = (rest[:nxt.start()], rest[nxt.start():]) if nxt else (rest, '')
        parts = re.split(r'<h3 id="[^"]*">(.*?)</h3>', faq_html)
        items = []
        for q, a in zip(parts[1::2], parts[2::2]):
            items.append(f'<details><summary>{q}</summary><div>{a.strip()}</div></details>')
            faq.append((html.unescape(re.sub('<[^>]+>', '', q)), html.unescape(re.sub('<[^>]+>', ' ', a)).strip()))
        body = head + '\n<div class="faq">' + '\n'.join(items) + '</div>\n' + tail
    return body, toc, faq


# ---------------------------------------------------------------- ortak parçalar
def shared(name):
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    m = re.search(rf'<!-- SHARED:{name}:START[^>]*-->\n(.*?)<!-- SHARED:{name}:END -->', src, re.S)
    return m.group(1)


def rebase(fragment, root):
    """Ana sayfadaki göreli linkleri alt sayfa derinliğine göre düzeltir."""
    # Sadece <a> linkleri (#bölüm ve tedaviler/ gibi göreli yollar); ikonlardaki <use href="#..."> aynı sayfada kalmalı
    fragment = re.sub(r'(<a\b[^>]*?\bhref=")(?!https?:|mailto:|tel:|/|\.\./)', lambda m: m.group(1) + root, fragment)
    return fragment.replace('src="assets/', f'src="{root}assets/')


def services_block(pages):
    out = ['      <div class="services">']
    for cid, title, sub, icon in CATEGORIES:
        items = sorted((p for p in pages if p['kategori'] == cid), key=lambda p: p['sira'])
        lis = ''.join(
            f'<li><a href="tedaviler/{p["slug"]}/">{html.escape(p["kisa_ad"])}</a></li>' if p['yayinda']
            else f'<li>{html.escape(p["kisa_ad"])}</li>'
            for p in items)
        small = f' <small>{sub}</small>' if sub else ''
        out.append(f'''        <article class="svc reveal">
          <div class="svc__icon"><svg><use href="#{icon}"/></svg></div>
          <h3>{title}{small}</h3>
          <ul>{lis}</ul>
        </article>''')
    out.append('      </div>')
    if any(p['yayinda'] for p in pages):
        out.append('      <div class="services__more reveal"><a href="tedaviler/" class="btn btn--ghost">Tüm tedavi sayfaları <svg><use href="#i-arrow"/></svg></a></div>')
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- şablonlar
HEAD = Template('''<!doctype html>
<html lang="tr" data-root="$root">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$title</title>
  <meta name="description" content="$description">
  $canonical_tag<meta name="theme-color" content="#1b2c55">
  <meta property="og:title" content="$title">
  <meta property="og:description" content="$description">
  <meta property="og:url" content="$canonical">
  <meta property="og:image" content="$site/assets/img/doctor/hero.webp">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="tr_TR">
  $robots<link rel="icon" href="${root}assets/img/brand/favicon-48.png" type="image/png">
  <link rel="apple-touch-icon" href="${root}assets/img/brand/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script>if (/[?&]renk=bordo\\b/.test(location.search)) document.documentElement.dataset.theme = 'bordo';</script>
  <link rel="stylesheet" href="${root}assets/css/style.css">
  <script type="application/ld+json">$jsonld</script>
</head>
<body>
''')

FOOT = Template('''$footer
<script src="${root}assets/js/main.js"></script>
</body>
</html>
''')

ARTICLE = Template('''<main id="top">
$draft
  <section class="page-hero">
    <div class="container">
      <nav class="crumbs" aria-label="Sayfa yolu"><a href="${root}">Ana Sayfa</a><span>›</span><a href="${tx}tedaviler/">Tedaviler</a><span>›</span><span>$cat</span></nav>
      <h1>$h1</h1>
      <p class="page-hero__lead">$lead</p>
      <div class="page-hero__meta">
        <img src="${root}assets/img/doctor/portre-sm.webp" alt="" width="48" height="48">
        <div><strong>$doctor</strong><span>Ortopedi ve Travmatoloji Uzmanı · Doruk Nilüfer Hastanesi, Bursa</span>$reviewed</div>
      </div>
    </div>
  </section>

  <div class="container article-grid">
    <article class="article">
$toc
$body
      <p class="article__note">Bu sayfadaki bilgiler genel bilgilendirme amaçlıdır; muayene, tanı ve tedavinin yerine geçmez. Size uygun tedavi, muayene ve gerekli tetkiklerden sonra hekiminiz tarafından belirlenir.</p>
    </article>

    <aside class="article-aside">
      <div class="aside-card aside-card--cta">
        <h2>Randevu</h2>
        <p>$doctor, Bursa Doruk Nilüfer Hastanesi'nde hastalarını kabul etmektedir.</p>
        <p class="aside-card__hours"><svg><use href="#i-clock"/></svg><span data-hours>Pazartesi – Cumartesi, 09.00 – 18.00</span></p>
        <a data-tel href="${root}#iletisim" class="btn btn--light btn--block"><svg><use href="#i-phone"/></svg> <span data-phone-text>Randevu Hattı</span></a>
        <a href="${root}#randevu" class="btn btn--outline-light btn--block">Online Randevu</a>
      </div>
$related
    </aside>
  </div>

  <section class="cta-band">
    <div class="container cta-band__inner">
      <div>
        <h2 class="h2">$h1 için muayene</h2>
        <p>Şikâyetlerinizi değerlendirmek ve size uygun tedavi seçeneklerini konuşmak için randevu alabilirsiniz.</p>
      </div>
      <div class="cta-band__actions">
        <a href="${root}#randevu" class="btn btn--primary btn--lg">Online Randevu <svg><use href="#i-arrow"/></svg></a>
        <a data-tel href="${root}#iletisim" class="btn btn--ghost btn--lg"><svg><use href="#i-phone"/></svg> <span data-phone-label>Randevu Hattı</span></a>
      </div>
    </div>
  </section>
</main>
''')

INDEX = Template('''<main id="top">
$draft
  <section class="page-hero">
    <div class="container">
      <nav class="crumbs" aria-label="Sayfa yolu"><a href="${root}">Ana Sayfa</a><span>›</span><span>Tedaviler</span></nav>
      <h1>Tedaviler</h1>
      <p class="page-hero__lead">$doctor'ın Bursa Doruk Nilüfer Hastanesi'nde uyguladığı ortopedik tedaviler ve ameliyatlar hakkında bilgilendirme sayfaları.</p>
    </div>
  </section>
  <div class="container tx">
$cats
  </div>
</main>
''')

DRAFT = '  <div class="draft-banner">TASLAK – Op. Dr. Bangin Bekir Candan\'ın onayı bekleniyor. Bu sayfa henüz yayında değil.</div>'


def canonical_tag(url, review):
    # Taslak/önizleme sayfaları noindex; henüz var olmayan canlı adrese canonical vermeyelim
    return '' if review else f'<link rel="canonical" href="{url}">\n  '


def jsonld(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def physician():
    return {
        '@type': 'Physician', 'name': DOCTOR, 'medicalSpecialty': 'Orthopedic',
        'url': SITE_URL + '/',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Konak Mah. Lefkoşe Cd. No:22',
                    'addressLocality': 'Nilüfer', 'addressRegion': 'Bursa', 'postalCode': '16110', 'addressCountry': 'TR'},
    }


# ---------------------------------------------------------------- üretim
INNER_LINK = re.compile(r'<a href="\.\./([a-z0-9-]+)/">(.*?)</a>')


def build_article(p, pages, root, review, tx=None):
    """root: sitenin köküne göreli yol (assets, ana sayfa); tx: tedaviler/ klasörünün bulunduğu köke göreli yol."""
    tx = root if tx is None else tx
    body, toc, faq = render_body(p['body_md'])
    # Onaysız (yayında olmayan) sayfalara verilen metin içi linkler düz yazıya çevrilir
    live = {q['slug'] for q in pages if q['yayinda']}
    body = INNER_LINK.sub(lambda m: m.group(0) if m.group(1) in live else m.group(2), body)
    url = f'{SITE_URL}/tedaviler/{p["slug"]}/'
    cat = CAT[p['kategori']]
    toc_html = ''
    if len(toc) > 2:
        lis = ''.join(f'<li><a href="#{i}">{n}</a></li>' for i, n in toc)
        toc_html = f'      <nav class="toc" aria-label="Bu sayfada"><strong>Bu sayfada</strong><ol>{lis}</ol></nav>'
    visible = [q for q in pages if q['yayinda'] and q['slug'] != p['slug']]
    by_slug = {q['slug']: q for q in visible}
    rel = [by_slug[s] for s in p['ilgili'] if s in by_slug]
    rel += sorted((q for q in visible if q['kategori'] == p['kategori'] and q not in rel), key=lambda q: q['sira'])
    related = ''
    if rel:
        lis = ''.join(f'<li><a href="{tx}tedaviler/{q["slug"]}/">{html.escape(q["baslik"])}</a></li>' for q in rel[:8])
        related = f'      <div class="aside-card"><h2>İlgili sayfalar</h2><ul class="aside-links">{lis}</ul></div>'
    reviewed = ''
    page_ld = {'@type': 'MedicalWebPage', 'name': p['baslik'], 'description': p['aciklama'], 'url': url,
               'inLanguage': 'tr', 'about': {'@type': p['tur'], 'name': p['baslik']},
               'author': physician()}
    if p.get('onay_tarihi'):
        d = p['onay_tarihi']
        reviewed = f'<em class="reviewed">Tıbbi içerik {DOCTOR} tarafından incelenmiştir · {".".join(reversed(d.split("-")))}</em>'
        page_ld.update(lastReviewed=d, reviewedBy={'@type': 'Physician', 'name': DOCTOR})
    graph = [page_ld, {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Ana Sayfa', 'item': SITE_URL + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Tedaviler', 'item': SITE_URL + '/tedaviler/'},
        {'@type': 'ListItem', 'position': 3, 'name': p['baslik'], 'item': url}]}]
    if faq:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'\s+', ' ', a)}}
            for q, a in faq]})
    head = HEAD.substitute(root=root, title=html.escape(p['seo_baslik']), description=html.escape(p['aciklama']),
                           canonical=url, site=SITE_URL, robots='<meta name="robots" content="noindex">\n  ' if review else '',
                           canonical_tag=canonical_tag(url, review),
                           jsonld=jsonld({'@context': 'https://schema.org', '@graph': graph}))
    main = ARTICLE.substitute(root=root, tx=tx, draft=DRAFT if review else '', cat=cat[1], h1=html.escape(p['baslik']),
                              lead=html.escape(p['aciklama']), doctor=DOCTOR, reviewed=reviewed,
                              toc=toc_html, body=indent(body, 6), related=related)
    return head + rebase(shared('ICONS'), root) + rebase(shared('HEADER'), root) + main + \
        FOOT.substitute(root=root, footer=rebase(shared('FOOTER'), root))


def build_index(pages, root, review, tx=None):
    tx = root if tx is None else tx
    cats = []
    for cid, title, sub, icon in CATEGORIES:
        items = sorted((p for p in pages if p['kategori'] == cid and p['yayinda']), key=lambda p: p['sira'])
        if not items:
            continue
        cards = ''.join(f'''
        <a class="tx-card" href="{tx}tedaviler/{p["slug"]}/"><strong>{html.escape(p["baslik"])}</strong><span>{html.escape(p["aciklama"])}</span><svg><use href="#i-arrow"/></svg></a>'''
                        for p in items)
        cats.append(f'''    <section class="tx-cat">
      <h2><span class="svc__icon"><svg><use href="#{icon}"/></svg></span>{title}</h2>
      <div class="tx-grid">{cards}
      </div>
    </section>''')
    url = SITE_URL + '/tedaviler/'
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Tedaviler', 'url': url, 'inLanguage': 'tr'}
    head = HEAD.substitute(root=root, title=f'Tedaviler | {DOCTOR} – Bursa Ortopedi', site=SITE_URL,
                           description=html.escape(f'{DOCTOR} – Bursa Doruk Nilüfer Hastanesi: protez, artroskopi, kırık, el ve ayak cerrahisi tedavi sayfaları.'),
                           canonical=url, robots='<meta name="robots" content="noindex">\n  ' if review else '', jsonld=jsonld(ld),
                           canonical_tag=canonical_tag(url, review))
    main = INDEX.substitute(root=root, draft=DRAFT if review else '', doctor=DOCTOR, cats='\n'.join(cats))
    return head + rebase(shared('ICONS'), root) + rebase(shared('HEADER'), root) + main + \
        FOOT.substitute(root=root, footer=rebase(shared('FOOTER'), root))


def indent(text, n):
    pad = ' ' * n
    return '\n'.join(pad + line if line.strip() else line for line in text.splitlines())


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def check(pages):
    slugs = {p['slug'] for p in pages}
    for p in pages:
        for s in p['ilgili'] + re.findall(r'\]\(\.\./([a-z0-9-]+)/\)', p['body_md']):
            if s not in slugs:
                print(f'UYARI {p["slug"]}: bilinmeyen sayfa "{s}"')
        if len(p['seo_baslik']) > 65:
            print(f'UYARI {p["slug"]}: seo_baslik {len(p["seo_baslik"])} karakter (Google ~60 gösterir)')
        if not 70 <= len(p['aciklama']) <= 165:
            print(f'UYARI {p["slug"]}: aciklama {len(p["aciklama"])} karakter (önerilen 70–160)')


def load_pages(review):
    pages = [parse(f) for f in sorted(CONTENT.glob('*.md'))]
    check(pages)
    for p in pages:
        p['yayinda'] = review or p['onayli'] or p['yayin']
        p['onay_tarihi'] = p.get('onay_tarihi') if p['onayli'] else None
    return pages


def update_services(index_html, pages):
    block = services_block(pages)
    return re.sub(r'(<!-- SERVICES:START[^>]*-->\n).*?(      <!-- SERVICES:END -->)',
                  lambda m: m.group(1) + block + m.group(2), index_html, flags=re.S)


def build_site():
    pages = load_pages(review=False)
    live = [p for p in pages if p['yayinda']]
    out = ROOT / 'tedaviler'
    # Onayı kaldırılan sayfaları sil
    if out.exists():
        for d in out.iterdir():
            if d.is_dir() and d.name not in {p['slug'] for p in live}:
                shutil.rmtree(d)
    for p in live:
        write(out / p['slug'] / 'index.html', build_article(p, pages, '../../', review=False))
    if live:
        write(out / 'index.html', build_index(pages, '../', review=False))
    elif (out / 'index.html').exists():
        (out / 'index.html').unlink()
    index = ROOT / 'index.html'
    write(index, update_services(index.read_text(encoding='utf-8'), pages))
    today = datetime.date.today().isoformat()
    urls = [(SITE_URL + '/', today)]
    if live:
        urls.append((SITE_URL + '/tedaviler/', today))
    urls += [(f'{SITE_URL}/tedaviler/{p["slug"]}/', p.get('onay_tarihi') or today) for p in live]
    write(ROOT / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join(f'  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls) + '</urlset>\n')
    write(ROOT / 'robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    write_preview_redirects(live)
    print(f'Site: {len(live)}/{len(pages)} sayfa yayında; hoca onaylı: {sum(p["onayli"] for p in pages)}.')


def build_review():
    pages = load_pages(review=True)
    site = REVIEW / 'site'
    if site.exists():
        shutil.rmtree(site)
    shutil.copytree(ROOT / 'assets', site / 'assets')
    shutil.copy(ROOT / 'content.json', site / 'content.json')
    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    write(site / 'index.html', update_services(index, pages))
    for p in pages:
        write(site / 'tedaviler' / p['slug'] / 'index.html', build_article(p, pages, '../../', review=True))
    write(site / 'tedaviler' / 'index.html', build_index(pages, '../', review=True))
    pdf = build_review_pdf(pages)
    print(f'İnceleme: {len(pages)} sayfa → {site}\nPDF: {pdf}')


def redirect_html(target):
    return (f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0; url={target}">'
            f'<title>Yönlendiriliyor…</title><a href="{target}">{target}</a>\n')


def write_preview_redirects(live):
    """Daha önce paylaşılan /onizleme/ linkleri, yayına alınan sayfalara yönlensin."""
    out = ROOT / 'onizleme'
    if not out.exists():
        return
    shutil.rmtree(out)
    write(out / 'index.html', redirect_html(f'{SITE_URL}/tedaviler/' if live else f'{SITE_URL}/'))
    write(out / 'tedaviler' / 'index.html', redirect_html(f'{SITE_URL}/tedaviler/' if live else f'{SITE_URL}/'))
    for p in live:
        write(out / 'tedaviler' / p['slug'] / 'index.html', redirect_html(f'{SITE_URL}/tedaviler/{p["slug"]}/'))


def build_preview():
    """Linki bilenlerin görebileceği gizli önizleme: /onizleme/tedaviler/... (noindex, TASLAK etiketi)."""
    pages = load_pages(review=True)
    out = ROOT / 'onizleme'
    if out.exists():
        shutil.rmtree(out)
    for p in pages:
        write(out / 'tedaviler' / p['slug'] / 'index.html', build_article(p, pages, '../../../', review=True, tx='../../'))
    write(out / 'tedaviler' / 'index.html', build_index(pages, '../../', review=True, tx='../'))
    write(out / 'index.html', '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
          '<meta http-equiv="refresh" content="0; url=tedaviler/"><title>Önizleme</title><a href="tedaviler/">Tedaviler</a>\n')
    print(f'Önizleme: {len(pages)} sayfa → {out}')


def build_review_pdf(pages):
    ordered = sorted(pages, key=lambda p: ([c[0] for c in CATEGORIES].index(p['kategori']), p['sira']))
    toc, sections = [], []
    for n, p in enumerate(ordered, 1):
        body, _, _ = render_body(p['body_md'])
        body = body.replace('<div class="faq">', '<div>').replace('<details><summary>', '<h3>').replace('</summary><div>', '</h3>').replace('</div></details>', '')
        toc.append(f'<li><span>{n}.</span> {html.escape(p["baslik"])} <em>({CAT[p["kategori"]][1]})</em></li>')
        sections.append(f'''<section class="pg"><p class="no">Sayfa {n} / {len(ordered)} · {CAT[p["kategori"]][1]}</p>
<h1>{html.escape(p["baslik"])}</h1>
<div class="seo"><b>Google'da görünecek başlık:</b> {html.escape(p["seo_baslik"])}<br><b>Google açıklaması:</b> {html.escape(p["aciklama"])}</div>
{body}</section>''')
    doc = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Tedavi Sayfaları – İnceleme</title>
<style>
@page {{ size: A4; margin: 18mm 16mm; }}
body {{ font-family: "Segoe UI", Arial, sans-serif; color: #16213d; font-size: 10.5pt; line-height: 1.55; }}
h1 {{ color: #1b2c55; font-size: 19pt; margin: 4pt 0 8pt; }}
h2 {{ color: #067d6e; font-size: 13pt; margin: 14pt 0 4pt; }}
h3 {{ color: #1b2c55; font-size: 11pt; margin: 10pt 0 2pt; }}
p {{ margin: 0 0 6pt; }} ul {{ margin: 0 0 6pt; padding-left: 16pt; }}
.pg {{ break-before: page; }}
.no {{ color: #5d6782; font-size: 9pt; margin: 0; }}
.seo {{ background: #eef3fb; border-radius: 6pt; padding: 6pt 9pt; font-size: 9pt; color: #3c4663; margin-bottom: 8pt; }}
.cover h1 {{ font-size: 24pt; margin-top: 30pt; }}
.box {{ border: 1.5pt solid #067d6e; border-radius: 8pt; padding: 10pt 14pt; margin: 14pt 0; background: #e4f6f2; }}
ol.list {{ list-style: none; padding: 0; columns: 2; font-size: 10pt; }} ol.list li {{ margin-bottom: 3pt; }} ol.list span {{ display: inline-block; width: 18pt; font-weight: 700; }}
ol.list em {{ color: #5d6782; font-style: normal; font-size: 8.5pt; }}
</style></head><body>
<section class="cover">
<p class="no">{DOCTOR} · Web Sitesi</p>
<h1>Tedavi Sayfaları – İnceleme ve Onay</h1>
<div class="box"><b>Sayın Hocam,</b><br>Web sitesi için her tedaviye ayrı bir bilgilendirme sayfası hazırlandı. Bu sayfalar Google'da aranırken bulunmayı (SEO) ve reklam (Google Ads) yönlendirmelerini hedefliyor. Hiçbiri sizin onayınız olmadan yayına alınmayacak.<br><br>
<b>Lütfen kontrol edin:</b> tıbbi doğruluk, uygulamadığınız ya da farklı uyguladığınız yöntemler, eklemek istediğiniz bilgiler.<br>
<b>Geri dönüş:</b> düzeltmeleri <b>sayfa numarası</b> ile yazmanız yeterli (ör. "5. sayfa, iyileşme süresi 6 hafta değil 3 ay"). Sorunsuz olanlar için "1, 2, 4 onaylı" demeniz yeterli.</div>
<p>Metinler genel bilgilendirme amaçlıdır, karşılaştırma veya sonuç garantisi içermez (Sağlık Bakanlığı tanıtım kuralları).</p>
<h2>Sayfalar ({len(ordered)})</h2><ol class="list">{"".join(toc)}</ol>
</section>
{"".join(sections)}
</body></html>'''
    src = REVIEW / 'tedavi-sayfalari-inceleme.html'
    pdf = REVIEW / 'tedavi-sayfalari-inceleme.pdf'
    write(src, doc)
    for chrome in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                   r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'):
        if Path(chrome).exists():
            subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                            f'--print-to-pdf={pdf}', src.as_uri()], check=True, capture_output=True, timeout=180)
            return pdf
    print('Chrome/Edge bulunamadı; PDF yerine HTML hazırlandı.')
    return src


if __name__ == '__main__':
    if '--inceleme' in sys.argv:
        build_review()
    elif '--onizleme' in sys.argv:
        build_preview()
    else:
        build_site()
