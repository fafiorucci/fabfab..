/* App online: tiene in memoria app, slide e quiz, così si apre e funziona anche senza rete.
   Generato da prepara_casa.py (versione e elenco dei file). Le slide delle lezioni aperte le scarica l'app
   (precarica) e qui si conservano man mano. */
const CACHE = 'corso-casa-__VERSIONE__';
const FILE = __FILE__;

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(k => Promise.all(k.filter(x => x.startsWith('corso-casa-') && x !== CACHE).map(x => caches.delete(x))))
    .then(() => self.clients.claim()));
});
// prima la copia conservata; se manca, la rete (e si conserva: per esempio i caratteri di Google)
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // sempre in rete, mai nella copia: controllo dell'accesso, pagina per rientrare, progressi (api),
  // area istruttore e presentazioni
  const u = new URL(e.request.url);
  if (u.origin === location.origin && (/\/(accesso\.json|entra\/?(index\.html)?)$/.test(u.pathname) ||
      /\/(api|presentazioni)\//.test(u.pathname) || /\/docente(\.html|\/)?$/.test(u.pathname))) return;
  // una risposta arrivata dopo un rimando (…/e.html → …/e) non si può dare a una pagina: se ne fa una copia pulita
  const pulita = r => r && r.redirected ? r.blob().then(b => new Response(b, {status: r.status, statusText: r.statusText, headers: r.headers})) : r;
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(pulita).then(c => c || fetch(e.request).then(r => {
    if (r && (r.ok || r.type === 'opaque')) { const copia = r.clone(); caches.open(CACHE).then(k => k.put(e.request, copia)); }
    return r;
  }).catch(() => e.request.mode === 'navigate' ? caches.match('./') : undefined)));
});
