// Service worker: guarda o app (e a apostila) para abrir mesmo sem internet.
const C = 'estudos-v4-6';
const FILES = ['./', './index.html', './firebase-config.js', './vitrine.js', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-180.png', './favicon-32.png', './qyudev.png',
  './vendor/pdf.min.js', './vendor/pdf.worker.min.js', './apostila.pdf'];
self.addEventListener('install', e => { e.waitUntil(caches.open(C).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  // Bibliotecas do Firebase (versão fixa, nunca mudam): cache primeiro, para o app abrir offline.
  if (url.hostname === 'www.gstatic.com' && url.pathname.startsWith('/firebasejs/')) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(e.request, cp)); return res; })));
    return;
  }
  // Login e banco de dados (Google/Firebase) e outros sites: nunca passam pelo cache.
  if (url.origin !== location.origin) return;
  // A apostila e o leitor de PDF não mudam: cache primeiro.
  if (url.pathname.endsWith('apostila.pdf') || url.pathname.includes('/vendor/')) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(e.request, cp)); return res; })));
    return;
  }
  // O resto do app: rede primeiro (pega a versão nova), cache se estiver sem internet.
  e.respondWith(fetch(e.request).then(r => { const cp = r.clone(); caches.open(C).then(c => c.put(e.request, cp)); return r; }).catch(() => caches.match(e.request)));
});
