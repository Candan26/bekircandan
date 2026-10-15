/* ==========================================================
   AYARLAR – İletişim bilgileri tek yerden yönetilir.
   TODO: telefon ve facebook bilgisi Bekir Bey'den alınacak.
   ========================================================== */
const CONFIG = {
  phone: '',                 // örn. '905321234567' (başında + olmadan, ülke koduyla)
  phoneText: '',             // örn. '0532 123 45 67'
  whatsapp: '',              // boşsa phone kullanılır
  instagram: 'https://www.instagram.com/op.dr.banginbekircandan/',
  youtube: 'https://www.youtube.com/@DrBanginBekirCandan',
  facebook: '',              // örn. 'https://www.facebook.com/...'
  maps: 'https://www.google.com/maps/search/?api=1&query=Doruk+Nil%C3%BCfer+Hastanesi+Bursa',
};

const VIDEOS = [
  { yt: 'GiS1vCSuHQI', title: 'Bu kemik nasıl kırıldı?' },
  { yt: '5BBymSEmgYI', title: 'Paça çorbası kırığa iyi gelir mi?' },
  { yt: 'vbA018_amQ8', title: 'Bir ortopedist olarak ayakkabılarımı nasıl seçiyorum?' },
  { yt: '-EmWNt9BwXw', title: 'Kimlerin kalça protezine ihtiyacı olabilir?' },
  { yt: 'vuxBY3HXHDU', title: 'Kapalı omuz ameliyatı gerçekten ne demek?' },
  { yt: 'V35a5ydYrfI', title: 'Diz protezi defterini açıyoruz' },
  { yt: 'iZyHed7SrPg', title: 'Sen uzun yaşa, gerekirse protezi değiştiririz!' },
  { yt: 'vAEfcLsrosE', title: 'Sabah parmaklarınız kilitleniyorsa dikkat!' },
  { yt: 'Z2kDfnK2dRg', title: 'Basketbol tek başına boy uzatmaz!' },
  { yt: 'I3mTay0AAQg', title: 'Evde çıplak ayakla mı, terlikle mi yürümeli?' },
  { yt: 'PB6eedwPJAM', title: 'Başınız öne doğru eğikse bu video size göre' },
  { yt: 'FbrMaw7wSw4', title: 'Yastıksız uyumak boyun için daha mı sağlıklı?' },
  { yt: '9e_HfKzJB_c', title: 'Halı sahada sakatlanmaların asıl sebebi' },
  { src: 'assets/video/okul-cantasi.mp4', poster: 'assets/video/okul-cantasi.jpg', title: 'Okul çantası seçerken nelere dikkat etmeli?' },
  { src: 'assets/video/omuz-ameliyatlari.mp4', poster: 'assets/video/omuz-ameliyatlari.jpg', title: 'Omuz ameliyatları hakkında' },
];
const VIDEOS_INITIAL = 10;

const INFO = [
  { id: 'aliskanlik', title: '30 Yaşından Sonra 5 Alışkanlık', count: 6, from: 0 },
  { id: 'hareket', title: 'Bu 5 Hareketi Deneyin', count: 7, from: 0 },
  { id: 'kirik', title: 'Kırıkları Tanıyoruz', count: 5, from: 0 },
  { id: 'ayakkabi', title: 'Ayakkabınız Ne Anlatıyor?', count: 7, from: 0 },
  { id: 'durus', title: 'Masa Başı & Duruş', count: 5, from: 1 },
  { id: 'beslenme', title: 'Kemik Sağlığı & Beslenme', count: 3, from: 0 },
];

const GALLERY_COUNT = 16;

/* ---------- Yardımcılar ---------- */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const waNumber = () => (CONFIG.whatsapp || CONFIG.phone).replace(/\D/g, '');
const waLink = (text = '') => {
  const n = waNumber();
  const q = text ? `?text=${encodeURIComponent(text)}` : '';
  return n ? `https://wa.me/${n}${q}` : '#randevu';
};

/* ---------- İletişim bağlantıları ---------- */
$$('[data-tel]').forEach(a => { a.href = CONFIG.phone ? `tel:+${CONFIG.phone.replace(/\D/g, '')}` : '#iletisim'; });
$$('[data-phone-text]').forEach(el => { el.textContent = CONFIG.phoneText || 'Telefon (eklenecek)'; });
$$('[data-wa]').forEach(a => {
  a.href = waLink('Merhaba, randevu almak istiyorum.');
  if (!waNumber()) a.removeAttribute('target');
});
$$('[data-link]').forEach(a => {
  const url = CONFIG[a.dataset.link];
  if (url) a.href = url; else { a.href = '#iletisim'; a.removeAttribute('target'); }
});
$('#year').textContent = new Date().getFullYear();

/* ---------- Header + mobil menü ---------- */
const header = $('#header');
const burger = $('#burger');
const nav = $('#nav');
const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 10);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

burger.addEventListener('click', () => {
  const open = burger.getAttribute('aria-expanded') !== 'true';
  burger.setAttribute('aria-expanded', open);
  nav.classList.toggle('is-open', open);
});
$$('a', nav).forEach(a => a.addEventListener('click', () => {
  burger.setAttribute('aria-expanded', 'false');
  nav.classList.remove('is-open');
}));

// Aktif menü öğesi
const sections = $$('main section[id]');
const navLinks = $$('.nav a[href^="#"]:not(.btn)');
const spy = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    navLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === `#${e.target.id}`));
  });
}, { rootMargin: '-45% 0px -50% 0px' });
sections.forEach(s => spy.observe(s));

/* ---------- Videolar ---------- */
const videosEl = $('#videos');
function videoCard(v) {
  const el = document.createElement('div');
  el.className = 'vid reveal';
  const thumb = v.yt ? `https://i.ytimg.com/vi/${v.yt}/oardefault.jpg` : v.poster;
  el.innerHTML = `
    <button type="button" aria-label="${v.title} videosunu oynat">
      <img src="${thumb}" alt="" loading="lazy">
      <span class="vid__shade"></span>
      <span class="vid__play"><svg><use href="#i-play"/></svg></span>
      <span class="vid__title">${v.title}</span>
    </button>`;
  const img = $('img', el);
  if (v.yt) img.addEventListener('error', () => { img.src = `https://i.ytimg.com/vi/${v.yt}/hqdefault.jpg`; }, { once: true });
  $('button', el).addEventListener('click', () => {
    if (v.yt) {
      el.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${v.yt}?autoplay=1&rel=0&playsinline=1" title="${v.title}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
    } else {
      el.innerHTML = `<video src="${v.src}" poster="${v.poster}" controls autoplay playsinline></video>`;
    }
  });
  return el;
}
VIDEOS.forEach((v, i) => {
  const card = videoCard(v);
  if (i >= VIDEOS_INITIAL) card.hidden = true;
  videosEl.append(card);
});
if (VIDEOS.length > VIDEOS_INITIAL) {
  const more = document.createElement('button');
  more.className = 'btn btn--ghost videos__more';
  more.textContent = `Tüm videoları göster (${VIDEOS.length})`;
  more.addEventListener('click', () => { $$('.vid[hidden]', videosEl).forEach(c => { c.hidden = false; c.classList.add('is-in'); }); more.remove(); });
  videosEl.append(more);
}

/* ---------- Lightbox ---------- */
const lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap');
let lbItems = [], lbIndex = 0;
function lbShow(i) {
  lbIndex = (i + lbItems.length) % lbItems.length;
  const it = lbItems[lbIndex];
  lbImg.src = it.src; lbImg.alt = it.cap; lbCap.textContent = `${it.cap} · ${lbIndex + 1}/${lbItems.length}`;
}
function lbOpen(items, i) {
  lbItems = items; lbShow(i); lb.hidden = false; document.body.style.overflow = 'hidden';
  $('.lb__close', lb).focus();
}
function lbClose() { lb.hidden = true; document.body.style.overflow = ''; lbImg.removeAttribute('src'); }
$('.lb__close', lb).addEventListener('click', lbClose);
$('.lb__prev', lb).addEventListener('click', () => lbShow(lbIndex - 1));
$('.lb__next', lb).addEventListener('click', () => lbShow(lbIndex + 1));
lb.addEventListener('click', e => { if (e.target === lb) lbClose(); });
addEventListener('keydown', e => {
  if (lb.hidden) return;
  if (e.key === 'Escape') lbClose();
  if (e.key === 'ArrowLeft') lbShow(lbIndex - 1);
  if (e.key === 'ArrowRight') lbShow(lbIndex + 1);
});
// Mobilde kaydırma
let tx = null;
lb.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
lb.addEventListener('touchend', e => {
  if (tx === null) return;
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) lbShow(lbIndex + (dx < 0 ? 1 : -1));
  tx = null;
});

/* ---------- Bilgi köşesi ---------- */
const tabsEl = $('#infoTabs'), gridEl = $('#infoGrid');
function renderInfo(series) {
  $$('.tab', tabsEl).forEach(t => t.setAttribute('aria-selected', t.dataset.id === series.id));
  const items = Array.from({ length: series.count }, (_, k) => {
    const n = k + series.from;
    return { src: `assets/img/info/${series.id}-${n}.webp`, thumb: `assets/img/info/${series.id}-${n}-sm.webp`, cap: series.title };
  });
  gridEl.innerHTML = '';
  items.forEach((it, i) => {
    const b = document.createElement('button');
    b.className = 'info-card';
    b.style.animationDelay = `${i * 50}ms`;
    b.setAttribute('aria-label', `${series.title} – görsel ${i + 1}`);
    b.innerHTML = `<img src="${it.thumb}" alt="${series.title} – ${i + 1}" loading="lazy" width="480" height="600">`;
    b.addEventListener('click', () => lbOpen(items, i));
    gridEl.append(b);
  });
}
INFO.forEach((s, i) => {
  const t = document.createElement('button');
  t.className = 'tab'; t.type = 'button'; t.role = 'tab'; t.dataset.id = s.id; t.textContent = s.title;
  t.addEventListener('click', () => renderInfo(s));
  tabsEl.append(t);
  if (i === 0) renderInfo(s);
});

/* ---------- Galeri ---------- */
const galleryEl = $('#gallery');
const galleryItems = Array.from({ length: GALLERY_COUNT }, (_, k) => ({
  src: `assets/img/gallery/g${String(k + 1).padStart(2, '0')}.webp`, cap: 'Ameliyathane',
}));
galleryItems.forEach((it, i) => {
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'reveal';
  b.setAttribute('aria-label', `Galeri görseli ${i + 1}`);
  b.innerHTML = `<img src="${it.src}" alt="Ameliyathaneden kare ${i + 1}" loading="lazy">`;
  b.addEventListener('click', () => lbOpen(galleryItems, i));
  galleryEl.append(b);
});

/* ---------- Randevu formu → WhatsApp ---------- */
const form = $('#apptForm'), msg = $('#formMsg');
form.addEventListener('submit', e => {
  e.preventDefault();
  let ok = true;
  $$('[required]', form).forEach(f => {
    const bad = f.type === 'checkbox' ? !f.checked : !f.value.trim();
    f.classList.toggle('is-invalid', bad);
    if (bad) ok = false;
  });
  if (!ok) { msg.textContent = 'Lütfen zorunlu alanları doldurun.'; return; }
  const d = Object.fromEntries(new FormData(form));
  const text = [
    'Merhaba, web sitesi üzerinden randevu talebi:',
    `Ad Soyad: ${d.ad}`,
    `Telefon: ${d.tel}`,
    `Konu: ${d.konu}`,
    d.gun ? `Tercih edilen gün: ${d.gun.split('-').reverse().join('.')}` : '',
    d.mesaj ? `Mesaj: ${d.mesaj}` : '',
  ].filter(Boolean).join('\n');
  if (!waNumber()) { msg.textContent = 'WhatsApp numarası henüz tanımlanmadı (CONFIG.phone).'; return; }
  msg.textContent = 'WhatsApp açılıyor…';
  window.open(waLink(text), '_blank', 'noopener');
});
$$('input, textarea, select', form).forEach(f => f.addEventListener('input', () => f.classList.remove('is-invalid')));

/* ---------- Scroll animasyonları ---------- */
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
}, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
$$('.reveal').forEach(el => io.observe(el));
