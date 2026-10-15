/* ==========================================================
   Düzenlenebilir içerik (iletişim, videolar, bilgi serileri, galeri)
   kök dizindeki content.json dosyasından okunur.
   ========================================================== */

/* ---------- Yardımcılar ---------- */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
let CONTACT = {};
const waNumber = () => (CONTACT.whatsapp || CONTACT.phone || '').replace(/\D/g, '');
const waLink = (text = '') => {
  const n = waNumber();
  const q = text ? `?text=${encodeURIComponent(text)}` : '';
  return n ? `https://wa.me/${n}${q}` : '#randevu';
};
// YouTube linkinden (shorts, watch, youtu.be) ya da düz ID'den video ID'si çıkarır
const youtubeId = v => {
  const m = String(v || '').match(/(?:shorts\/|watch\?v=|youtu\.be\/|embed\/)([\w-]{11})/);
  return m ? m[1] : (/^[\w-]{11}$/.test(v) ? v : null);
};

/* ---------- İletişim bağlantıları ---------- */
function applyContact(c) {
  CONTACT = c || {};
  const phone = (CONTACT.phone || '').replace(/\D/g, '');
  $$('[data-tel]').forEach(a => { a.href = phone ? `tel:+${phone}` : '#iletisim'; });
  $$('[data-phone-text]').forEach(el => { el.textContent = CONTACT.phoneText || 'Telefon (eklenecek)'; });
  $$('[data-wa]').forEach(a => {
    a.href = waLink('Merhaba, randevu almak istiyorum.');
    if (waNumber()) a.target = '_blank'; else a.removeAttribute('target');
  });
  $$('[data-link]').forEach(a => {
    const url = CONTACT[a.dataset.link];
    if (url) { a.href = url; a.target = '_blank'; } else { a.href = '#iletisim'; a.removeAttribute('target'); }
  });
}
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

/* ---------- Scroll animasyonları ---------- */
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
}, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
const observeReveals = (root = document) => $$('.reveal:not(.is-in)', root).forEach(el => io.observe(el));

/* ---------- Videolar ---------- */
const videosEl = $('#videos');
function videoCard(v) {
  const el = document.createElement('div');
  el.className = 'vid reveal';
  const yt = youtubeId(v.youtube);
  const thumb = yt ? `https://i.ytimg.com/vi/${yt}/oardefault.jpg` : v.poster;
  el.innerHTML = `
    <button type="button" aria-label="${esc(v.title)} videosunu oynat">
      ${thumb ? `<img src="${esc(thumb)}" alt="" loading="lazy">` : ''}
      <span class="vid__shade"></span>
      <span class="vid__play"><svg><use href="#i-play"/></svg></span>
      <span class="vid__title">${esc(v.title)}</span>
    </button>`;
  const img = $('img', el);
  if (yt && img) img.addEventListener('error', () => { img.src = `https://i.ytimg.com/vi/${yt}/hqdefault.jpg`; }, { once: true });
  $('button', el).addEventListener('click', () => {
    if (yt) {
      el.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${yt}?autoplay=1&rel=0&playsinline=1" title="${esc(v.title)}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
    } else {
      el.innerHTML = `<video src="${esc(v.file)}" ${v.poster ? `poster="${esc(v.poster)}"` : ''} controls autoplay playsinline></video>`;
    }
  });
  return el;
}
function renderVideos(videos, initial = 10) {
  videosEl.innerHTML = '';
  const list = (videos || []).filter(v => youtubeId(v.youtube) || v.file);
  list.forEach((v, i) => {
    const card = videoCard(v);
    if (i >= initial) card.hidden = true;
    videosEl.append(card);
  });
  if (list.length > initial) {
    const more = document.createElement('button');
    more.className = 'btn btn--ghost videos__more';
    more.textContent = `Tüm videoları göster (${list.length})`;
    more.addEventListener('click', () => { $$('.vid[hidden]', videosEl).forEach(c => { c.hidden = false; c.classList.add('is-in'); }); more.remove(); });
    videosEl.append(more);
  }
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
function renderInfo(series, tab) {
  $$('.tab', tabsEl).forEach(t => t.setAttribute('aria-selected', t === tab));
  const items = series.images.map(im => ({ src: im.src, thumb: im.thumb || im.src, cap: series.title }));
  gridEl.innerHTML = '';
  items.forEach((it, i) => {
    const b = document.createElement('button');
    b.className = 'info-card';
    b.style.animationDelay = `${i * 50}ms`;
    b.setAttribute('aria-label', `${series.title} – görsel ${i + 1}`);
    b.innerHTML = `<img src="${esc(it.thumb)}" alt="${esc(series.title)} – ${i + 1}" loading="lazy" width="480" height="600">`;
    b.addEventListener('click', () => lbOpen(items, i));
    gridEl.append(b);
  });
}
function renderInfoTabs(seriesList) {
  tabsEl.innerHTML = '';
  const list = (seriesList || []).filter(s => s.images?.length);
  $('#bilgi').hidden = !list.length;
  list.forEach((s, i) => {
    const t = document.createElement('button');
    t.className = 'tab'; t.type = 'button'; t.role = 'tab'; t.textContent = s.title;
    t.addEventListener('click', () => renderInfo(s, t));
    tabsEl.append(t);
    if (i === 0) renderInfo(s, t);
  });
}

/* ---------- Galeri ---------- */
const galleryEl = $('#gallery');
function renderGallery(gallery) {
  galleryEl.innerHTML = '';
  const items = (gallery || []).map(g => ({ src: g.src, cap: g.caption || 'Galeri' }));
  $('#galeri').hidden = !items.length;
  items.forEach((it, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'reveal';
    b.setAttribute('aria-label', `Galeri görseli ${i + 1}`);
    b.innerHTML = `<img src="${esc(it.src)}" alt="${esc(it.cap)} ${i + 1}" loading="lazy">`;
    b.addEventListener('click', () => lbOpen(items, i));
    galleryEl.append(b);
  });
}

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
  if (!waNumber()) { msg.textContent = 'WhatsApp numarası henüz tanımlanmadı.'; return; }
  msg.textContent = 'WhatsApp açılıyor…';
  window.open(waLink(text), '_blank', 'noopener');
});
$$('input, textarea, select', form).forEach(f => f.addEventListener('input', () => f.classList.remove('is-invalid')));

/* ---------- İçeriği yükle ---------- */
applyContact({});
observeReveals();
fetch('content.json', { cache: 'no-cache' })
  .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(c => {
    applyContact(c.contact);
    renderVideos(c.videos, c.videosInitial || 10);
    renderInfoTabs(c.infoSeries);
    renderGallery(c.gallery);
    observeReveals();
  })
  .catch(err => console.error('content.json yüklenemedi:', err));
