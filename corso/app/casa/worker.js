/* App del corso online: il server che sta davanti ai file del sito (Cloudflare Worker con file statici).
   Generato da prepara_casa.py (versione).

   - Chi entra lo decide Cloudflare Access (email ammesse e codice via email): qui si legge l'email dal
     token firmato che Access aggiunge a ogni richiesta (Cf-Access-Jwt-Assertion), verificandone firma,
     emittente, destinatario e scadenza.
   - /api/*  le stesse richieste del server dell'aula (server.py), ma l'allievo è riconosciuto dall'email:
             niente codice personale. I dati stanno in un Durable Object (archivio SQLite di Cloudflare).
   - /docente e /api/docente/*  solo per l'email dell'istruttore (variabile DOCENTE).
   - slide, schede e appendici delle lezioni ancora chiuse non si scaricano (come contenuto_aperto in server.py);
     le presentazioni solo per l'istruttore. */
import { DurableObject } from 'cloudflare:workers';

const VERSIONE = '__VERSIONE__';
const json = (dati, stato = 200) => new Response(JSON.stringify(dati), {
  status: stato, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } });
const errore = (stato, testo) => json({ errore: testo }, stato);
const pagina = (stato, testo) => new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
  + '<p style="font:18px sans-serif;padding:24px">' + testo + '</p>', { status: stato, headers: { 'Content-Type': 'text/html; charset=utf-8' } });

/* ---------- chi è: token di Cloudflare Access ---------- */
let CERTI = null, CERTI_TS = 0;
const b64u = s => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)), c => c.charCodeAt(0));
async function chiavi(env, forza) {
  if (!CERTI || forza || Date.now() - CERTI_TS > 3600e3) {
    const r = await fetch(`https://${env.TEAM}.cloudflareaccess.com/cdn-cgi/access/certs`);
    CERTI = (await r.json()).keys || []; CERTI_TS = Date.now();
  }
  return CERTI;
}
async function emailDa(req, env) {
  if (env.PROVA_EMAIL) return (req.headers.get('x-prova-email') || env.PROVA_EMAIL).toLowerCase();   // solo prova in locale
  let t = req.headers.get('cf-access-jwt-assertion');
  if (!t) { const m = (req.headers.get('cookie') || '').match(/(?:^|;\s*)CF_Authorization=([^;]+)/); t = m && m[1]; }
  if (!t) return null;
  try {
    const [h, p, s] = t.split('.');
    const testa = JSON.parse(new TextDecoder().decode(b64u(h))), dati = JSON.parse(new TextDecoder().decode(b64u(p)));
    let k = (await chiavi(env)).find(x => x.kid === testa.kid);
    if (!k) k = (await chiavi(env, true)).find(x => x.kid === testa.kid);
    if (!k || testa.alg !== 'RS256') return null;
    const chiave = await crypto.subtle.importKey('jwk', k, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
    const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', chiave, b64u(s), new TextEncoder().encode(h + '.' + p));
    const aud = [].concat(dati.aud || []);
    if (!ok || dati.iss !== `https://${env.TEAM}.cloudflareaccess.com` || !aud.includes(env.AUD) || !(dati.exp * 1000 > Date.now())) return null;
    return dati.email ? String(dati.email).toLowerCase() : null;
  } catch (e) { return null; }
}

/* ---------- lezioni aperte: slide, schede e appendici ---------- */
let CORSO = null;
async function corso(env, url) {
  if (!CORSO) CORSO = await (await env.ASSETS.fetch(new URL('/corso.json', url))).json();
  return CORSO;
}
async function aperto(p, attive, C) {
  let m = p.match(/^\/slides\/(L\d+)-\d+\.jpg$/);
  if (m) return attive.includes(m[1]);
  m = p.match(/^\/slides\/SR-(\d+)\.jpg$/);
  if (m) { const l = C.lezioni.find(x => (x.scheda || []).includes(+m[1])); return !l || attive.includes(l.id); }
  m = p.match(/^\/appendici\/([a-z])\.html$/);
  if (m) { const a = C.appendici.find(x => x.file === 'appendici/' + m[1] + '.html'); return !a || a.lezioni.some(l => attive.includes(l)); }
  return true;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), p = url.pathname;
    const email = await emailDa(req, env);
    if (!email) return p.startsWith('/api/') ? errore(401, 'Accesso non verificato: rientra con la tua email.') : pagina(401, 'Accesso non verificato: ricarica la pagina ed entra con la tua email.');
    const docente = email === String(env.DOCENTE || '').toLowerCase();
    const archivio = env.CORSO.get(env.CORSO.idFromName('corso'));

    if (p.startsWith('/api/')) {
      if (p.startsWith('/api/docente/') && !docente) return errore(403, 'Area riservata all’istruttore.');
      const h = new Headers(req.headers); h.set('x-email', email); h.set('x-origine', url.origin);
      return archivio.fetch(new Request(req.url, { method: req.method, headers: h, body: req.method === 'POST' ? await req.text() : undefined }));
    }
    if (p === '/docente' || p === '/docente/' || p === '/docente.html') {
      if (!docente) return pagina(403, 'Questa pagina è riservata all’istruttore.');
      return env.ASSETS.fetch(new URL('/docente.html', url));
    }
    if (p.startsWith('/presentazioni/') && !docente) return pagina(403, 'Le presentazioni si aprono dall’area istruttore.');
    if (!docente && (p.startsWith('/slides/') || p.startsWith('/appendici/'))) {
      const attive = await (await archivio.fetch(new Request(url.origin + '/interno/attive'))).json();
      if (!(await aperto(p, attive, await corso(env, url)))) return pagina(403, 'Questa lezione non è ancora aperta.');
    }
    return env.ASSETS.fetch(req);
  },
};

/* ---------- archivio di allievi e progressi (un solo Durable Object per tutto il corso) ---------- */
const adesso = () => new Date().toISOString().slice(0, 19);
const corto = (v, n) => String(v ?? '').split(/\s+/).filter(Boolean).join(' ').slice(0, n);

// come stato_pulito in server.py: solo campi noti, valori ammessi, testi corti
function statoPulito(corpo) {
  const stato = { visti: {}, risposte: {} };
  const visti = corpo.visti || {}, risposte = corpo.risposte || {};
  if (typeof visti !== 'object' || typeof risposte !== 'object' || Array.isArray(visti) || Array.isArray(risposte)) throw new Error('formato');
  for (const [lez, pagine] of Object.entries(visti))
    if (lez.length <= 8 && Array.isArray(pagine))
      stato.visti[lez] = [...new Set(pagine.filter(x => Number.isInteger(x) && x > 0 && x < 1000))].sort((a, b) => a - b);
  for (const [q, r] of Object.entries(risposte))
    if (q.length <= 20 && r && typeof r === 'object')
      stato.risposte[q] = { ok: !!r.ok, scelta: Number.isInteger(r.scelta) ? r.scelta : null, ts: String(r.ts ?? '').slice(0, 32),
                            tentativi: Math.max(1, Math.min(parseInt(r.tentativi) || 1, 999)), rivisto: !!r.rivisto };
  const pr = corpo.profilo;
  if (pr && typeof pr === 'object') {
    const profilo = {};
    for (const [k, n] of [['nome', 40], ['cognome', 40], ['email', 80], ['telefono', 30], ['colore', 20]]) { const v = corto(pr[k], n); if (v) profilo[k] = v; }
    const scelte = { ambito: ['entro', 'senza'], tipo: ['motore', 'vela', 'entrambe'], tema: ['auto', 'chiaro', 'scuro'], testo: ['normale', 'grande'], obiettivo_tipo: ['quiz', 'giorni'] };
    for (const [k, ok] of Object.entries(scelte)) if (ok.includes(pr[k])) profilo[k] = pr[k];
    if (/^\d{4}-\d{2}-\d{2}$/.test(String(pr.esame || ''))) profilo.esame = pr.esame;
    if (Number.isInteger(pr.obiettivo_n) && pr.obiettivo_n > 0 && pr.obiettivo_n <= 500) profilo.obiettivo_n = pr.obiettivo_n;
    stato.profilo = profilo;
  }
  const di = corpo.diario;
  if (di && typeof di === 'object') {
    stato.diario = {};
    for (const g of Object.keys(di).filter(k => /^\d{4}-\d{2}-\d{2}$/.test(k)).sort().slice(-120))
      if (di[g] && typeof di[g] === 'object')
        stato.diario[g] = { q: Math.max(0, Math.min(parseInt(di[g].q) || 0, 9999)), s: Math.max(0, Math.min(parseInt(di[g].s) || 0, 9999)) };
  }
  return stato;
}

export class Corso extends DurableObject {
  async attive() {
    let a = await this.ctx.storage.get('attive');
    if (!a) {
      const C = await (await this.env.ASSETS.fetch('https://corso/corso.json')).json();
      a = C.lezioni.filter(l => l.attiva).map(l => l.id);
      await this.ctx.storage.put('attive', a);
    }
    return a;
  }
  async fetch(req) {
    const p = new URL(req.url).pathname, email = req.headers.get('x-email');
    if (p === '/interno/attive') return json(await this.attive());
    let dati = {};
    if (req.method === 'POST') { try { dati = JSON.parse(await req.text() || '{}'); } catch (e) { return errore(400, 'Richiesta non valida.'); } }
    const st = this.ctx.storage, chiave = 'allievo:' + email;
    const a = await st.get(chiave);

    if (p === '/api/info') return json({ aula: true, online: true, attive: await this.attive(), versione: VERSIONE,
                                        docente: email === String(this.env.DOCENTE || '').toLowerCase() });
    if (p === '/api/progresso' && req.method === 'GET') {
      if (!a) return errore(401, 'Primo accesso: scrivi il tuo nome.');
      return json({ nome: a.nome, stato: a.stato, giro: a.giro || 0, creato: a.creato });
    }
    if (p === '/api/accedi') {
      const nome = corto(dati.nome, 60);
      if (!nome) return errore(400, 'Scrivi il tuo nome.');
      let b = a;
      if (!b) { b = { email, nome, creato: adesso(), ultimo: adesso(), giro: 0, stato: { visti: {}, risposte: {}, profilo: { email } } }; await st.put(chiave, b); }
      return json({ token: 'online', nome: b.nome, stato: b.stato, giro: b.giro || 0 });
    }
    if (p === '/api/progresso') {
      if (!a) return errore(401, 'Primo accesso: scrivi il tuo nome.');
      // «giro» cambia quando l'istruttore azzera: un telefono rimasto indietro non rimette i vecchi dati
      if (String(dati.giro ?? 0) !== String(a.giro || 0)) return json({ errore: 'Progressi azzerati dall’istruttore.', stato: a.stato, giro: a.giro || 0 }, 409);
      try { a.stato = statoPulito(dati); } catch (e) { return errore(400, 'Richiesta non valida.'); }
      const pr = a.stato.profilo || {}, nuovo = [pr.nome, pr.cognome].filter(Boolean).join(' ');
      if (nuovo) a.nome = nuovo;
      a.ultimo = adesso(); await st.put(chiave, a);
      return json({ ok: true });
    }
    if (p === '/api/cancella') { await st.delete(chiave); return json({ ok: true }); }
    if (p === '/api/codice') return errore(400, 'Online non serve un codice: entri con la tua email.');

    // area istruttore (il Worker ha già controllato l'email)
    if (p === '/api/docente/allievi') {
      const elenco = [...(await st.list({ prefix: 'allievo:' })).values()]
        .filter(x => x.email !== String(this.env.DOCENTE || '').toLowerCase())   // l'istruttore che prova l'app non è in classe
        .map(x => ({ id: x.email, nome: x.nome, creato: x.creato, ultimo: x.ultimo, stato: x.stato }));
      return json({ allievi: elenco, indirizzi: [req.headers.get('x-origine') + '/'], attive: await this.attive() });
    }
    if (p === '/api/docente/lezione') {
      const C = await (await this.env.ASSETS.fetch('https://corso/corso.json')).json();
      const id = String(dati.id || '');
      if (!C.lezioni.some(l => l.id === id)) return errore(404, 'Lezione non trovata.');
      const s = new Set(await this.attive()); dati.attiva ? s.add(id) : s.delete(id);
      const nuove = C.lezioni.filter(l => s.has(l.id)).map(l => l.id);
      await st.put('attive', nuove);
      return json({ attive: nuove });
    }
    const k = 'allievo:' + String(dati.id || '').toLowerCase(), b = await st.get(k);
    if (p.startsWith('/api/docente/') && !b) return errore(404, 'Allievo non trovato.');
    if (p === '/api/docente/codice') return errore(400, 'Online gli allievi entrano con la loro email: non serve un codice.');
    if (p === '/api/docente/azzera') {
      b.stato = { visti: {}, risposte: {}, profilo: b.stato.profilo || {}, diario: {} }; b.giro = (b.giro || 0) + 1;
      await st.put(k, b); return json({ ok: true });
    }
    if (p === '/api/docente/elimina') { await st.delete(k); return json({ ok: true }); }
    return errore(404, 'Non trovato.');
  }
}
