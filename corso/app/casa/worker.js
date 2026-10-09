/* App del corso online: il server che sta davanti ai file del sito (Cloudflare Worker con file statici).
   Generato da prepara_casa.py (versione).

   - Chi entra lo decide Cloudflare Access (email ammesse e codice via email): qui si legge l'email dal
     token firmato che Access aggiunge a ogni richiesta (Cf-Access-Jwt-Assertion), verificandone firma,
     emittente, destinatario e scadenza.
   - /api/*  le stesse richieste del server dell'aula (server.py), ma l'allievo è riconosciuto dall'email:
             niente codice personale. I dati stanno in un Durable Object (archivio SQLite di Cloudflare).
   - /docente e /api/docente/*  solo per l'email dell'istruttore (variabile DOCENTE).
   - slide, schede e appendici delle lezioni ancora chiuse non si scaricano (come contenuto_aperto in server.py);
     le presentazioni solo per l'istruttore.
   - con MODO = "prova" (Worker «corso-nautico-prova», senza Cloudflare Access e con i soli file della prova) si entra
     con il link personale …/?p=<codice> creato dall'istruttore: il codice resta in un cookie e vale fino alla scadenza.
   - account di prova per altre scuole (li crea l'istruttore, con scadenza): app con le lezioni 1-2 e area istruttore
     con allievi inventati; mai i dati veri. Scaduta la prova non si apre più niente.
   - registro degli accessi degli allievi (per 90 giorni): per allievo e giorno quante volte apre l'app, slide, schede,
     appendici e quiz, da quali IP (con paese e città stimati da Cloudflare) e da quali dispositivi (codice casuale
     dell'app nel cookie corso_disp). Segnalazioni dei casi sospetti all'istruttore, anche per email se c'è il
     collegamento EMAIL (mittente EMAIL_DA); blocco dell'allievo, di un suo IP o di un suo dispositivo. */
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

/* ---------- registro degli accessi: chi, da dove, con cosa ---------- */
const GIORNI_REGISTRO = 90;          // poi i dati degli accessi si cancellano da soli
const SOGLIA_DISPOSITIVI = 3;        // più di 3 dispositivi in 7 giorni: segnalazione
const SOGLIA_KM = 300;               // due luoghi più lontani di così entro un'ora: segnalazione
const categoria = (p, metodo) => p === '/accesso.json' ? 'app' : /^\/slides\/L\d+-/.test(p) ? 'slide' : /^\/slides\/SR-/.test(p) ? 'scheda'
  : /^\/slides\/A[A-Z]-/.test(p) || p.startsWith('/appendici/') ? 'appendice' : null;
// «iPhone · Safari», «Windows · Chrome»…: abbastanza per riconoscere un dispositivo a colpo d'occhio
function dispositivo(ua) {
  ua = String(ua || '');
  const so = /iPhone/.test(ua) ? 'iPhone' : /iPad/.test(ua) ? 'iPad' : /Android/.test(ua) ? (/Mobile/.test(ua) ? 'Android' : 'tablet Android')
    : /Windows/.test(ua) ? 'Windows' : /Macintosh|Mac OS X/.test(ua) ? 'Mac' : /CrOS/.test(ua) ? 'Chromebook' : /Linux/.test(ua) ? 'Linux' : 'altro';
  const br = /Edg\//.test(ua) ? 'Edge' : /SamsungBrowser/.test(ua) ? 'Samsung Internet' : /Firefox|FxiOS/.test(ua) ? 'Firefox'
    : /Chrome|CriOS/.test(ua) ? 'Chrome' : /Safari/.test(ua) ? 'Safari' : 'browser';
  return so + ' · ' + br;
}
function visita(req, env, p) {
  const cf = req.cf || {}, prova = env.PROVA_EMAIL ? req.headers : null;   // in locale si può simulare IP e luogo
  const m = (req.headers.get('cookie') || '').match(/(?:^|;\s*)corso_disp=([a-z0-9]{8,40})/);
  return {
    cat: categoria(p, req.method),
    ip: String((prova && prova.get('x-prova-ip')) || req.headers.get('cf-connecting-ip') || '').slice(0, 45),
    paese: String((prova && prova.get('x-prova-paese')) || cf.country || '').slice(0, 2),
    citta: corto((prova && prova.get('x-prova-citta')) || cf.city || '', 40), regione: corto(cf.region || '', 40),
    lat: parseFloat((prova && prova.get('x-prova-lat')) || cf.latitude) || null, lon: parseFloat((prova && prova.get('x-prova-lon')) || cf.longitude) || null,
    disp: m ? m[1] : '', ua: dispositivo(req.headers.get('user-agent')),
  };
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
  m = p.match(/^\/slides\/A([A-Z])-\d+\.jpg$/);   // pagine delle appendici come immagini
  if (m) { const a = C.appendici.find(x => x.id === m[1]); return !a || a.lezioni.some(l => attive.includes(l)); }
  m = p.match(/^\/appendici\/([a-z])(?:\.html)?$/);   // anche senza «.html»
  if (m) { const a = C.appendici.find(x => x.file === 'appendici/' + m[1] + '.html'); return !a || a.lezioni.some(l => attive.includes(l)); }
  return true;
}

// account di prova: cosa vedono e per quanto
const PROVA_LEZIONI = ['L01', 'L02'];
const PROVA_SLIDE = 3;                       // delle lezioni 1 e 2 solo le prime slide
const PROVA_PRESENTAZIONI = ['rotta'];       // nell'area istruttore solo «Rotta verso la patente»
// il corso visto da un account di prova: lezioni 1 e 2 con le prime slide e la loro prima verifica (che rimanda a quelle
// slide), niente schede, numeri d'oro né appendici; le altre lezioni oscurate
function corsoProva(C) {
  const quiz = {};
  const lezioni = C.lezioni.map(l => {
    if (!PROVA_LEZIONI.includes(l.id)) return { ...l, attiva: false, capitoli: [], scheda: [], appendici: [] };
    const tutte = l.capitoli.flatMap(c => c.pagine), pagine = tutte.slice(0, PROVA_SLIDE);
    const verifica = l.capitoli.flatMap(c => c.quiz).find(v => !v.raccolta && v.ids.length) || { ids: [] };
    for (const q of verifica.ids) {
      const Q = C.quiz[q];
      quiz[q] = { ...Q, rivedi: Q.rivedi[0] === l.id && pagine.includes(Q.rivedi[1]) ? Q.rivedi : [l.id, pagine[pagine.length - 1]] };
    }
    const nq = l.capitoli.reduce((n, c) => n + c.quiz.reduce((m, v) => m + v.ids.length, 0), 0);
    return { ...l, attiva: true, scheda: [], appendici: [],
             capitoli: [{ titolo: 'Le prime slide', pagine, quiz: verifica.ids.length ? [{ titolo: 'Verifica di esempio', ids: verifica.ids, raccolta: false }] : [] }],
             nota_demo: `Account di prova: ${pagine.length} slide di esempio. Nella versione completa la lezione ha ${tutte.length} slide e ${nq} quiz ufficiali.` };
  });
  return { ...C, prova: true, lezioni, appendici: C.appendici.map(a => ({ ...a, aperta: false })), schede: { generali: [], numeri_oro: [] }, quiz };
}
const RUOLI = new Map();   // email → {ruolo, scade}, per un minuto, per non chiedere all'archivio a ogni slide
async function ruoloDi(archivio, email, origine) {
  const c = RUOLI.get(email);
  if (c && Date.now() - c.ts < 60e3) return c.r;
  const r = await (await archivio.fetch(new Request(origine + '/interno/ruolo', { headers: { 'x-email': email } }))).json();
  RUOLI.set(email, { r, ts: Date.now() });
  return r;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), p = url.pathname;
    const archivio = env.CORSO.get(env.CORSO.idFromName('corso'));
    const sitoProva = env.MODO === 'prova';
    let email;
    if (sitoProva) {
      // sito delle prove: si entra dal link personale (…/?p=<codice>), poi basta il cookie
      const dalLink = url.searchParams.get('p');
      if (dalLink) {
        const t = dalLink.toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 40);
        RUOLI.delete('link:' + t);
        const r = await ruoloDi(archivio, 'link:' + t, url.origin);
        if (r.ruolo !== 'prova') return pagina(403, r.ruolo === 'scaduta' ? 'Questo link di prova è scaduto. Per informazioni contatta Fabrizio Fiorucci.' : 'Questo link di prova non è valido.');
        return new Response(null, { status: 302, headers: { Location: '/', 'Set-Cookie': `corso_prova=${t}; Path=/; Max-Age=${60 * 86400}; HttpOnly; Secure; SameSite=Lax` } });
      }
      const m = (req.headers.get('cookie') || '').match(/(?:^|;\s*)corso_prova=([a-z0-9]+)/);
      if (!m) return p.startsWith('/api/') || p === '/accesso.json' ? errore(401, 'Apri il link di prova che ti è stato mandato.')
        : pagina(401, 'Per provare l’app del corso apri il link personale che ti è stato mandato.');
      email = 'link:' + m[1];
    } else {
      email = await emailDa(req, env);
      if (!email) return p.startsWith('/api/') ? errore(401, 'Accesso non verificato: rientra con la tua email.') : pagina(401, 'Accesso non verificato: ricarica la pagina ed entra con la tua email.');
    }
    const R = !sitoProva && email === String(env.DOCENTE || '').toLowerCase() ? { ruolo: 'docente' } : await ruoloDi(archivio, email, url.origin), ruolo = R.ruolo;
    if (sitoProva && ruolo !== 'prova' && ruolo !== 'scaduta') return pagina(403, 'Questo link di prova non è valido.');
    const prova = ruolo === 'prova', istruttore = ruolo === 'docente' || prova;
    if (ruolo === 'scaduta')
      return p.startsWith('/api/') || p === '/accesso.json' ? errore(403, 'Il periodo di prova è terminato.')
        : pagina(403, 'Il periodo di prova dell’app del corso è terminato. Grazie per averla provata! Per informazioni contatta Fabrizio Fiorucci.');

    // allievi veri: ogni accesso va nel registro e si controlla che non sia bloccato
    const allievo = ruolo === 'allievo' && !sitoProva, V = allievo ? visita(req, env, p) : null;
    if (p.startsWith('/api/')) {
      if (p.startsWith('/api/docente/') && !istruttore) return errore(403, 'Area riservata all’istruttore.');
      const h = new Headers(req.headers); h.set('x-email', email); h.set('x-ruolo', ruolo); h.set('x-origine', url.origin);
      h.delete('x-visita'); if (V) h.set('x-visita', encodeURIComponent(JSON.stringify(V)));   // le intestazioni vogliono solo ASCII
      return archivio.fetch(new Request(req.url, { method: req.method, headers: h, body: req.method === 'POST' ? await req.text() : undefined }));
    }
    if (p === '/docente' || p === '/docente/' || p === '/docente.html') {
      if (!istruttore) return pagina(403, 'Questa pagina è riservata all’istruttore.');
      return env.ASSETS.fetch(new URL('/docente.html', url));
    }
    if (p.startsWith('/presentazioni/')) {
      if (!istruttore) return pagina(403, 'Le presentazioni si aprono dall’area istruttore.');
      if (prova) {
        if (p === '/presentazioni/elenco.json') {
          const elenco = await (await env.ASSETS.fetch(new URL('/presentazioni/elenco.json', url))).json();
          return json(elenco.filter(x => PROVA_PRESENTAZIONI.some(n => x.file === 'presentazioni/' + n + '.html')));
        }
        // i file statici rispondono anche senza «.html» (…/rotta.html rimanda a …/rotta)
        if (!PROVA_PRESENTAZIONI.some(n => p.replace(/\.html$/, '') === '/presentazioni/' + n)) return pagina(403, 'Nella prova questa presentazione non è disponibile.');
      }
    }
    if (prova && p === '/corso.json') return json(corsoProva(await corso(env, url)));
    if (prova && (p.startsWith('/slides/') || p.startsWith('/appendici/'))) {
      const C = corsoProva(await corso(env, url)), m = p.match(/^\/slides\/(L\d+)-(\d+)\.jpg$/);
      const l = m && R.attive.includes(m[1]) && C.lezioni.find(x => x.id === m[1]);
      if (!l || !l.capitoli.some(c => c.pagine.includes(+m[2]))) return pagina(403, 'Nella prova questa slide non è disponibile.');
    } else if (allievo && (p === '/accesso.json' || p.startsWith('/slides/') || p.startsWith('/appendici/'))) {
      const r = await (await archivio.fetch(new Request(url.origin + '/interno/accesso', { method: 'POST',
        headers: { 'x-email': email, 'x-origine': url.origin }, body: JSON.stringify(V) }))).json();
      if (r.bloccato) return p === '/accesso.json' ? json({ ok: false, sospeso: true }, 403) : pagina(403, 'Accesso sospeso: rivolgiti all’istruttore.');
      if (p !== '/accesso.json' && !(await aperto(p, r.attive, await corso(env, url)))) return pagina(403, 'Questa lezione non è ancora aperta.');
    } else if (ruolo !== 'docente' && (p.startsWith('/slides/') || p.startsWith('/appendici/'))) {
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

// allievi inventati per l'area istruttore di prova (come demo/demo-dati.js), costruiti sulle lezioni 1-2
function allieviInventati(C, attive) {
  const quiz = C.lezioni.filter(l => attive.includes(l.id)).flatMap(l => l.capitoli.flatMap(c => c.quiz.flatMap(s => s.ids)));
  const pagine = Object.fromEntries(C.lezioni.filter(l => attive.includes(l.id)).map(l => [l.id, l.capitoli.flatMap(c => c.pagine)]));
  const giorno = (n, h, m) => { const d = new Date(); d.setDate(d.getDate() + n); d.setHours(h, m, 0, 0); return d.toISOString().slice(0, 19); };
  const data = n => { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
  return [['Giulia', 'Ferri', '#E4572E', 'senza', 'entrambe', 21, 0.9, 0.95, 0], ['Marco', 'Bassi', '#0B8A99', 'entro', 'motore', 9, 0.7, 0.6, -1],
          ['Sara', 'Conti', '#7B5CD6', 'senza', 'vela', 35, 1, 0.85, 0], ['Luca', 'Moretti', '#2F6FDB', 'entro', 'motore', 9, 0.4, 0.5, -3],
          ['Elena', 'Galli', '#2E9E5B', '', '', null, 0.2, 0.7, -6], ['Paolo', 'Riva', '#F4A300', 'senza', 'motore', 48, 0.8, 0.4, -2]]
    .map(([nome, cognome, colore, ambito, tipo, esame, vista, bravura, ultimo], i) => {
      const visti = Object.fromEntries(Object.entries(pagine).map(([l, pp]) => [l, pp.slice(0, Math.round(pp.length * vista))]));
      const risposte = {};
      quiz.slice(0, Math.round(quiz.length * vista)).forEach((q, k) => {
        const ok = ((k * 7 + i * 3) % 10) / 10 < bravura, Q = C.quiz[q];
        risposte[q] = { ok, scelta: ok ? Q.x : (Q.x + 1) % Q.r.length, ts: giorno(ultimo, 10, 0), tentativi: ok && k % 4 === 0 ? 2 : 1, rivisto: !ok && k % 2 === 0 };
      });
      const profilo = { nome, cognome, colore };
      if (ambito) Object.assign(profilo, { ambito, tipo, esame: data(esame) });
      return { id: 'esempio-' + i, nome: nome + ' ' + cognome + ' (esempio)', creato: giorno(-20 + i, 9, 0), ultimo: giorno(ultimo, 9 + i, (12 * i) % 60),
               stato: { visti, risposte, profilo, diario: {} } };
    });
}

// registro degli accessi inventato per l'area istruttore di prova (come demo/demo-dati.js): tre segnalazioni di esempio
function accessiInventati(allievi) {
  const prima = minuti => new Date(Date.now() - minuti * 60e3).toISOString().slice(0, 19);
  const LUOGHI = ['Roma', 'Milano', 'Napoli', 'Torino', 'Firenze', 'Bologna'];
  const TIPI = ['iPhone · Safari', 'Android · Chrome', 'Windows · Chrome', 'Mac · Safari', 'iPad · Safari', 'Android · Samsung Internet'];
  const giorni = {};
  allievi.forEach((a, i) => {
    const ip = `93.${40 + i}.${11 + 3 * i}.${20 + i}`, citta = LUOGHI[i % 6];
    const disp = [{ id: 'd' + i + 'a1b2c3', ua: TIPI[i % 6] }, { id: 'd' + i + 'e4f5g6', ua: TIPI[(i + 2) % 6] }];
    if (i === 0) disp.push({ id: 'd0h7i8j9', ua: 'Android · Chrome' }, { id: 'd0k1l2m3', ua: 'Windows · Chrome' });
    const gg = [];
    for (let d = 0; d < 21; d++) {
      if ((d + i) % 3 === 2) continue;
      const ora = prima(d * 1440 + 20 + 47 * i + (13 * d) % 90), usati = i === 0 && d < 5 ? disp : disp.slice(0, d % 4 === 0 ? 2 : 1);
      const g = { data: ora.slice(0, 10), n: { app: 1 + (d + i) % 3, slide: 6 + (5 * d + 3 * i) % 18, quiz: (d + i) % 4 === 0 ? 0 : 2 + (d * i) % 6 },
                  ip: [{ ip, luogo: citta, n: 4 + (d + i) % 9, primo: ora, ultimo: ora }],
                  disp: usati.map(x => ({ id: x.id, ua: x.ua, n: 2 + (d + i) % 5, ultimo: ora, ip })) };
      if ((d + i) % 5 === 0) g.n.appendice = 3; if ((d + i) % 4 === 1) g.n.scheda = 2;
      gg.push(g);
    }
    if (i === 1 && gg[0]) gg[0].ip.push({ ip: '151.20.33.7', luogo: 'Roma', n: 3, primo: prima(110), ultimo: prima(95) });
    if (i === 5 && gg[0]) gg[0].ip.push({ ip: '88.12.4.90', luogo: 'Barcellona, Spagna', n: 2, primo: prima(200), ultimo: prima(185) });
    giorni[a.id] = gg;
  });
  const segn = (i, tipo, testo, minuti) => { const a = allievi[i]; if (!a) return null;
    const ip = new Map(), dd = new Map();
    for (const g of giorni[a.id].slice(0, 7)) { for (const x of g.ip) if (!ip.has(x.ip)) ip.set(x.ip, x); for (const x of g.disp) if (!dd.has(x.id)) dd.set(x.id, x); }
    return { id: 'esempio' + i, email: a.id, nome: a.nome, tipo, testo, creato: prima(minuti), stato: 'aperta',
             ip: [...ip.values()].map(x => ({ ip: x.ip, luogo: x.luogo, ultimo: x.ultimo, n: x.n })), disp: [...dd.values()] }; };
  return { giorni, blocchi: {}, segn: [segn(1, 'viaggio', 'Accessi da due luoghi lontani 477 km nella stessa ora: Milano e Roma', 90),
    segn(0, 'dispositivi', '4 dispositivi diversi negli ultimi 7 giorni', 25), segn(5, 'estero', 'Accesso dall’estero: Barcellona, Spagna', 180)].filter(Boolean) };
}
function riassuntoInventato(gg, n) {
  const da = new Date(Date.now() - (n - 1) * 864e5).toISOString().slice(0, 10), t = { n: {}, ip: new Set(), disp: new Set(), luoghi: new Set() };
  for (const g of gg.filter(g => g.data >= da)) { for (const [k, v] of Object.entries(g.n)) t.n[k] = (t.n[k] || 0) + v;
    g.ip.forEach(x => { t.ip.add(x.ip); t.luoghi.add(x.luogo); }); g.disp.forEach(x => t.disp.add(x.id)); }
  return { n: t.n, ip: t.ip.size, disp: t.disp.size, luoghi: [...t.luoghi] };
}

const linkProva = (env, e) => String(env.PROVA_URL || '').replace(/\/?$/, '/') + '?p=' + e.slice(5);

const giornoISO = (n = 0) => new Date(Date.now() - n * 864e5).toISOString().slice(0, 10);
function km(a, b) {   // distanza sulla sfera, in km
  const r = Math.PI / 180, x = Math.sin((b.lat - a.lat) * r / 2) ** 2 + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin((b.lon - a.lon) * r / 2) ** 2;
  return 12742 * Math.asin(Math.sqrt(x));
}
const vuoto = () => ({ n: {}, ip: {}, disp: {} });
// somma un giorno di accessi a un altro (b dentro a); tiene i 40 IP e i 20 dispositivi più recenti
function somma(a, b) {
  for (const [k, v] of Object.entries(b.n)) a.n[k] = (a.n[k] || 0) + v;
  for (const t of ['ip', 'disp']) {
    for (const [k, v] of Object.entries(b[t])) {
      const x = a[t][k];
      if (!x) a[t][k] = { ...v };
      else { x.n += v.n; if (v.primo < x.primo) x.primo = v.primo; if (v.ultimo > x.ultimo) { x.ultimo = v.ultimo; if (v.ip) x.ip = v.ip; } }
    }
    const tieni = t === 'ip' ? 40 : 20, chiavi = Object.keys(a[t]);
    if (chiavi.length > tieni) for (const k of chiavi.sort((x, y) => a[t][y].ultimo.localeCompare(a[t][x].ultimo)).slice(tieni)) delete a[t][k];
  }
  return a;
}
const NOMI_PAESI = new Intl.DisplayNames(['it'], { type: 'region' });
const paese = c => { try { return c ? NOMI_PAESI.of(c) : ''; } catch (e) { return c; } };
const luogo = x => [x.citta, x.paese && x.paese !== 'IT' ? paese(x.paese) : ''].filter(Boolean).join(', ') || 'luogo sconosciuto';

export class Corso extends DurableObject {
  constructor(ctx, env) { super(ctx, env); this.coda = new Map(); this.toccati = new Set(); this.blocchi = null; }
  async corso() { return (await this.env.ASSETS.fetch('https://corso/corso.json')).json(); }

  /* ----- registro degli accessi: in memoria, poi nell'archivio ogni 20 secondi (un salvataggio per allievo e giorno) ----- */
  registra(email, v, quiz = 0) {
    const k = 'acc:' + giornoISO() + ':' + email, r = this.coda.get(k) || vuoto(), ora = adesso();
    if (v.cat) r.n[v.cat] = (r.n[v.cat] || 0) + 1;
    if (quiz) r.n.quiz = (r.n.quiz || 0) + quiz;
    if (v.ip) { const x = r.ip[v.ip] || (r.ip[v.ip] = { n: 0, paese: v.paese, citta: v.citta, regione: v.regione, lat: v.lat, lon: v.lon, primo: ora }); x.n++; x.ultimo = ora; }
    if (v.disp) { const x = r.disp[v.disp] || (r.disp[v.disp] = { n: 0, ua: v.ua, primo: ora }); x.n++; x.ultimo = ora; if (v.ip) x.ip = v.ip; }
    this.coda.set(k, r); this.toccati.add(email);
    if (!this.sveglia) { this.sveglia = true; this.ctx.storage.setAlarm(Date.now() + 20e3); }
  }
  async scarica() {
    const coda = this.coda, toccati = this.toccati; this.coda = new Map(); this.toccati = new Set();
    for (const [k, d] of coda) await this.ctx.storage.put(k, somma((await this.ctx.storage.get(k)) || vuoto(), d));
    for (const e of toccati) await this.controlla(e);
  }
  async alarm() {
    this.sveglia = false;
    await this.scarica();
    if (this.pulito !== giornoISO()) {   // una volta al giorno: via gli accessi e le segnalazioni più vecchi di 90 giorni
      this.pulito = giornoISO();
      const limite = giornoISO(GIORNI_REGISTRO), st = this.ctx.storage;
      const vecchi = [...(await st.list({ prefix: 'acc:', end: 'acc:' + limite })).keys()];
      for (const s of (await st.list({ prefix: 'segn:' })).values()) if (s.creato.slice(0, 10) < limite) vecchi.push('segn:' + s.id);
      for (let i = 0; i < vecchi.length; i += 128) await st.delete(vecchi.slice(i, i + 128));
    }
  }
  // gli ultimi 7 giorni di un allievo: casi sospetti
  async controlla(email) {
    const st = this.ctx.storage, chiavi = [...Array(7)].map((_, i) => 'acc:' + giornoISO(i) + ':' + email);
    const giorni = [...(await st.get(chiavi)).values()], tutti = giorni.reduce((a, g) => somma(a, g), vuoto());
    const ips = Object.entries(tutti.ip).map(([ip, x]) => ({ ip, ...x })).sort((a, b) => b.ultimo.localeCompare(a.ultimo));
    const disp = Object.entries(tutti.disp).map(([id, x]) => ({ id, ...x })).sort((a, b) => b.ultimo.localeCompare(a.ultimo));
    if (disp.length > SOGLIA_DISPOSITIVI)
      await this.segnala(email, 'dispositivi', disp.length + ' dispositivi diversi negli ultimi 7 giorni', ips, disp);
    for (const x of ips.filter(x => x.paese && x.paese !== 'IT'))
      await this.segnala(email, 'estero:' + x.paese, 'Accesso dall’estero: ' + luogo(x), ips, disp);
    const oggi = ips.filter(x => x.lat != null && x.lon != null && x.ultimo.slice(0, 10) === giornoISO());
    for (let i = 0; i < oggi.length; i++) for (let j = i + 1; j < oggi.length; j++) {
      const a = oggi[i], b = oggi[j], d = km(a, b);
      const distacco = Math.max(Date.parse(a.primo) - Date.parse(b.ultimo), Date.parse(b.primo) - Date.parse(a.ultimo), 0);
      if (d > SOGLIA_KM && distacco <= 3600e3)
        return this.segnala(email, 'viaggio', 'Accessi da due luoghi lontani ' + Math.round(d) + ' km nella stessa ora: ' + luogo(a) + ' e ' + luogo(b), ips, disp);
    }
  }
  // una segnalazione per tipo e allievo ogni 7 giorni
  async segnala(email, tipo, testo, ips, disp) {
    const st = this.ctx.storage, chiave = 'segnchiave:' + email + ':' + tipo, prima = await st.get(chiave);
    if (prima && Date.now() - prima < 7 * 864e5) return;
    await st.put(chiave, Date.now());
    const a = await st.get('allievo:' + email), id = [...crypto.getRandomValues(new Uint8Array(10))].map(x => (x % 36).toString(36)).join('');
    const s = { id, email, nome: a ? a.nome : email, tipo: tipo.split(':')[0], testo, creato: adesso(), stato: 'aperta',
                ip: ips.slice(0, 10).map(x => ({ ip: x.ip, luogo: luogo(x), ultimo: x.ultimo, n: x.n })),
                disp: disp.slice(0, 10).map(x => ({ id: x.id, ua: x.ua, ultimo: x.ultimo, n: x.n, ip: x.ip || '' })) };
    await this.avvisa(s);
    await st.put('segn:' + id, s);
  }
  // email all'istruttore con il link diretto alla segnalazione (se c'è il collegamento EMAIL e il mittente EMAIL_DA)
  async avvisa(s) {
    const env = this.env;
    if (!env.EMAIL || !env.EMAIL_DA || !env.DOCENTE) return;
    const link = (this.origine || await this.ctx.storage.get('origine') || '') + '/docente?segnalazione=' + s.id;
    const righe = ['Allievo: ' + s.nome + ' (' + s.email + ')', s.testo, '',
      'Ultimi IP: ' + s.ip.slice(0, 5).map(x => x.ip + ' (' + x.luogo + ')').join(', '),
      'Dispositivi: ' + s.disp.slice(0, 5).map(x => x.ua).join(', '), '',
      'Apri la segnalazione per bloccare l’allievo, un IP o un dispositivo, oppure archiviarla:', link];
    try {
      await env.EMAIL.send({ from: env.EMAIL_DA, to: env.DOCENTE, subject: 'App del corso: accesso sospetto di ' + s.nome, text: righe.join('\n'),
        html: '<p>' + righe.map(t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;')).join('<br>').replace(link.replace(/&/g, '&amp;'), '<a href="' + link + '">' + link + '</a>') + '</p>' });
      s.avviso = 'email inviata';
    } catch (e) { s.avviso = 'email non inviata: ' + String(e && (e.code || e.message) || e).slice(0, 120); }
  }
  /* ----- blocchi: tutto l'allievo, un suo IP o un suo dispositivo ----- */
  async blocchiTutti() {
    if (!this.blocchi) this.blocchi = new Map([...(await this.ctx.storage.list({ prefix: 'blocco:' }))].map(([k, v]) => [k.slice(7), v]));
    return this.blocchi;
  }
  async bloccato(email, v) {
    const b = (await this.blocchiTutti()).get(email);
    return !!(b && (b.tutto || (v && v.ip && b.ip[v.ip]) || (v && v.disp && b.disp[v.disp])));
  }
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
    const origine = req.headers.get('x-origine');
    if (origine && origine !== this.origine) { this.origine = origine; await this.ctx.storage.put('origine', origine); }
    if (p === '/interno/attive') return json(await this.attive());
    if (p === '/interno/accesso') {   // file statici degli allievi: registro e blocchi
      const v = JSON.parse(await req.text() || '{}');
      if (await this.bloccato(email, v)) return json({ bloccato: true });
      this.registra(email, v);
      return json({ attive: await this.attive() });
    }
    if (p === '/interno/ruolo') {
      const d = await this.ctx.storage.get('prova:' + email);
      if (!d) return json({ ruolo: 'allievo' });
      if (Date.now() > Date.parse(d.scade)) return json({ ruolo: 'scaduta' });
      return json({ ruolo: 'prova', scade: d.scade, attive: d.attive || PROVA_LEZIONI });
    }
    const ruolo = req.headers.get('x-ruolo');
    let dati = {};
    if (req.method === 'POST') { try { dati = JSON.parse(await req.text() || '{}'); } catch (e) { return errore(400, 'Richiesta non valida.'); } }
    const st = this.ctx.storage, chiave = 'allievo:' + email;
    const a = await st.get(chiave);

    // allievo: bloccato? Le risposte ai quiz nuove contano nel registro
    const V = ruolo === 'allievo' && req.headers.get('x-visita') ? JSON.parse(decodeURIComponent(req.headers.get('x-visita'))) : null;
    if (V) {
      if (await this.bloccato(email, V)) return json({ errore: 'Accesso sospeso: rivolgiti all’istruttore.', sospeso: true }, 403);
      let quiz = 0;
      if (p === '/api/progresso' && req.method === 'POST' && a && dati.risposte && typeof dati.risposte === 'object') {
        const prima = (a.stato && a.stato.risposte) || {};
        for (const [q, r] of Object.entries(dati.risposte)) if (r && (!prima[q] || prima[q].ts !== String(r.ts ?? '').slice(0, 32))) quiz++;
      }
      this.registra(email, V, Math.min(quiz, 500));
    }

    const d = ruolo === 'prova' ? await st.get('prova:' + email) : null;   // account di prova: lezioni e scadenza suoi
    if (p === '/api/info') return json({ aula: true, online: true, attive: d ? d.attive : await this.attive(), versione: VERSIONE,
                                        docente: ruolo === 'docente' || !!d, prova: d ? { scade: d.scade } : undefined });
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
    const indirizzi = [req.headers.get('x-origine') + '/'];
    if (d) {   // area istruttore di prova: allievi inventati più sé stesso come allievo; le lezioni 1-2 si aprono e chiudono solo per sé
      const C = corsoProva(await this.corso());
      // registro degli accessi inventato, uno per account di prova (in memoria: blocchi e archiviazioni si possono provare)
      if (!this.accProva) this.accProva = new Map();
      if (!this.accProva.has(email)) this.accProva.set(email, accessiInventati(allieviInventati(C, d.attive)));
      const R = this.accProva.get(email), aperte = R.segn.filter(s => s.stato === 'aperta');
      if (p === '/api/docente/allievi') {
        const elenco = allieviInventati(C, d.attive);
        if (a) elenco.unshift({ id: email, nome: a.nome + ' (tu)', creato: a.creato, ultimo: a.ultimo, stato: a.stato });
        return json({ allievi: elenco, indirizzi, attive: d.attive, prova: { scade: d.scade },
                      accessi: { aperte: aperte.length, segnalati: [...new Set(aperte.map(s => s.email))] } });
      }
      if (p === '/api/docente/accessi')
        return json({ email: false, giorni: GIORNI_REGISTRO, segnalazioni: aperte.concat(R.segn.filter(s => s.stato !== 'aperta')),
          allievi: allieviInventati(C, d.attive).map(x => { const gg = R.giorni[x.id] || [];
            return { id: x.id, nome: x.nome, ultimo: gg[0] ? gg[0].ip.map(y => y.ultimo).sort().pop() : null,
                     d7: riassuntoInventato(gg, 7), d30: riassuntoInventato(gg, 30), blocco: R.blocchi[x.id] || null }; }) });
      if (p === '/api/docente/accessi-allievo') return json({ giorni: R.giorni[String(dati.id || '')] || [], blocco: R.blocchi[String(dati.id || '')] || null });
      if (p === '/api/docente/segnalazione') { const s = R.segn.find(x => x.id === dati.sid); if (s) s.stato = 'archiviata'; return json({ ok: true }); }
      if (p === '/api/docente/blocca' || p === '/api/docente/sblocca') {
        const id = String(dati.id || ''), tipo = String(dati.tipo || ''), val = String(dati.valore || '');
        if (!R.giorni[id] || !['tutto', 'ip', 'disp'].includes(tipo)) return errore(400, 'Richiesta non valida.');
        const b = R.blocchi[id] || { tutto: false, ip: {}, disp: {} };
        if (p === '/api/docente/blocca') { if (tipo === 'tutto') b.tutto = adesso(); else b[tipo][val] = adesso(); }
        else { if (tipo === 'tutto') b.tutto = false; else delete b[tipo][val]; }
        R.blocchi[id] = b.tutto || Object.keys(b.ip).length || Object.keys(b.disp).length ? b : null;
        const s = dati.sid && R.segn.find(x => x.id === dati.sid);
        if (s && p === '/api/docente/blocca') { s.stato = 'bloccata'; s.azione = tipo === 'tutto' ? 'allievo bloccato' : (tipo === 'ip' ? 'IP ' : 'dispositivo ') + val + ' bloccato'; }
        return json({ ok: true, blocco: R.blocchi[id] });
      }
      if (p === '/api/docente/lezione') {
        const id = String(dati.id || '');
        if (!PROVA_LEZIONI.includes(id)) return errore(403, 'Nella prova si possono aprire e chiudere solo le lezioni 1 e 2.');
        const s = new Set(d.attive); dati.attiva ? s.add(id) : s.delete(id);
        d.attive = PROVA_LEZIONI.filter(x => s.has(x)); await st.put('prova:' + email, d);
        return json({ attive: d.attive });
      }
      if (String(dati.id || '').toLowerCase() !== email) return errore(403, 'Nella prova gli allievi di esempio non si modificano.');
    }
    if (p === '/api/docente/allievi') {
      const prove = await st.list({ prefix: 'prova:' }), escluse = new Set([...prove.values()].map(x => x.email));
      const elenco = [...(await st.list({ prefix: 'allievo:' })).values()]
        .filter(x => x.email !== String(this.env.DOCENTE || '').toLowerCase() && !escluse.has(x.email))   // l'istruttore e le prove non sono in classe
        .map(x => ({ id: x.email, nome: x.nome, creato: x.creato, ultimo: x.ultimo, stato: x.stato }));
      const aperte = [...(await st.list({ prefix: 'segn:' })).values()].filter(s => s.stato === 'aperta');
      return json({ allievi: elenco, indirizzi, attive: await this.attive(),
                    accessi: { aperte: aperte.length, segnalati: [...new Set(aperte.map(s => s.email))] },
                    prove: await Promise.all([...prove.values()].map(async x => ({ email: x.email, nota: x.nota || '', creato: x.creato, scade: x.scade,
                                                                                link: x.email.startsWith('link:') ? linkProva(this.env, x.email) : null,
                                                                                usata: !!(await st.get('allievo:' + x.email)) }))) });
    }
    // account di prova per altre scuole: solo l'istruttore vero
    if (p === '/api/docente/prova' && ruolo === 'docente') {
      // senza email: link personale per il sito delle prove (…/?p=<codice>), senza email né codice di Cloudflare
      let e = corto(dati.email, 80).toLowerCase(), giorni = Math.max(1, Math.min(parseInt(dati.giorni) || 5, 60));
      if (!e) e = 'link:' + [...crypto.getRandomValues(new Uint8Array(12))].map(x => (x % 36).toString(36)).join('');
      if (!/^link:[a-z0-9]{8,40}$/.test(e) && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e)) return errore(400, 'Scrivi un’email valida, oppure lasciala vuota per un link di prova.');
      if (e === String(this.env.DOCENTE || '').toLowerCase()) return errore(400, 'È l’email dell’istruttore.');
      if (await st.get('allievo:' + e) && !(await st.get('prova:' + e))) return errore(400, 'Questa email è di un allievo del corso.');
      const scade = new Date(Date.now() + giorni * 864e5).toISOString();
      const vecchia = await st.get('prova:' + e);
      await st.put('prova:' + e, { email: e, nota: corto(dati.nota, 60), creato: vecchia ? vecchia.creato : adesso(), scade, attive: vecchia ? vecchia.attive : PROVA_LEZIONI });
      return json({ ok: true, scade, link: e.startsWith('link:') ? linkProva(this.env, e) : null });
    }
    if (p === '/api/docente/prova-togli' && ruolo === 'docente') {
      const e = String(dati.email || '').toLowerCase();
      await st.delete('prova:' + e); await st.delete('allievo:' + e);
      return json({ ok: true });
    }
    if (p.startsWith('/api/docente/accessi') || ['/api/docente/blocca', '/api/docente/sblocca', '/api/docente/segnalazione'].includes(p)) {
      if (ruolo !== 'docente') return errore(403, 'Solo per l’istruttore.');
      await this.scarica();
      const blocchi = await this.blocchiTutti();
      if (p === '/api/docente/accessi') {
        const giorni = new Map();   // email → giorni (dal più recente)
        for (const [k, g] of await st.list({ prefix: 'acc:' })) { const [, data, e] = k.split(/:(\d{4}-\d{2}-\d{2}):/); (giorni.get(e) || giorni.set(e, []).get(e)).push({ data, ...g }); }
        const allievi = [...(await st.list({ prefix: 'allievo:' })).values()].filter(x => x.email !== String(this.env.DOCENTE || '').toLowerCase() && !x.email.startsWith('link:'));
        const riassunto = (gg, n) => { const da = giornoISO(n - 1), t = gg.filter(g => g.data >= da).reduce((a, g) => somma(a, g), vuoto());
          return { n: t.n, ip: Object.keys(t.ip).length, disp: Object.keys(t.disp).length,
                   luoghi: [...new Set(Object.values(t.ip).map(luogo))].slice(0, 6) }; };
        const segn = [...(await st.list({ prefix: 'segn:' })).values()].sort((a, b) => b.creato.localeCompare(a.creato));
        return json({
          email: !!(this.env.EMAIL && this.env.EMAIL_DA), giorni: GIORNI_REGISTRO,
          segnalazioni: segn.filter(s => s.stato === 'aperta').concat(segn.filter(s => s.stato !== 'aperta').slice(0, 30)),
          allievi: allievi.map(x => { const gg = (giorni.get(x.email) || []).sort((a, b) => b.data.localeCompare(a.data)), ult = gg[0];
            const ora = ult ? [...Object.values(ult.ip), ...Object.values(ult.disp)].map(y => y.ultimo).sort().pop() : null;
            return { id: x.email, nome: x.nome, ultimo: ora || null, d7: riassunto(gg, 7), d30: riassunto(gg, 30), blocco: blocchi.get(x.email) || null }; }),
        });
      }
      if (p === '/api/docente/accessi-allievo') {
        const e = String(dati.id || '').toLowerCase(), gg = [];
        for (const [k, g] of await st.list({ prefix: 'acc:' })) if (k.endsWith(':' + e)) gg.push({ data: k.slice(4, 14), n: g.n,
          ip: Object.entries(g.ip).map(([ip, x]) => ({ ip, luogo: luogo(x), n: x.n, primo: x.primo, ultimo: x.ultimo })),
          disp: Object.entries(g.disp).map(([id, x]) => ({ id, ua: x.ua, n: x.n, ultimo: x.ultimo, ip: x.ip || '' })) });
        return json({ giorni: gg.sort((a, b) => b.data.localeCompare(a.data)), blocco: blocchi.get(e) || null });
      }
      if (p === '/api/docente/segnalazione') {
        const s = await st.get('segn:' + String(dati.sid || ''));
        if (!s) return errore(404, 'Segnalazione non trovata.');
        s.stato = dati.stato === 'aperta' ? 'aperta' : 'archiviata'; s.chiusa = adesso(); await st.put('segn:' + s.id, s);
        return json({ ok: true });
      }
      // blocca / sblocca: tipo «tutto», «ip» (valore = indirizzo) o «disp» (valore = codice del dispositivo)
      const e = String(dati.id || '').toLowerCase(), tipo = String(dati.tipo || ''), val = String(dati.valore || '').slice(0, 45);
      if (!e || !['tutto', 'ip', 'disp'].includes(tipo) || (tipo !== 'tutto' && !val)) return errore(400, 'Richiesta non valida.');
      const b = blocchi.get(e) || { tutto: false, ip: {}, disp: {} };
      if (p === '/api/docente/blocca') { if (tipo === 'tutto') b.tutto = adesso(); else b[tipo][val] = adesso(); }
      else { if (tipo === 'tutto') b.tutto = false; else delete b[tipo][val]; }
      const resta = b.tutto || Object.keys(b.ip).length || Object.keys(b.disp).length;
      if (resta) { blocchi.set(e, b); await st.put('blocco:' + e, b); } else { blocchi.delete(e); await st.delete('blocco:' + e); }
      if (dati.sid && p === '/api/docente/blocca') {
        const s = await st.get('segn:' + String(dati.sid));
        if (s) { s.stato = 'bloccata'; s.chiusa = adesso(); s.azione = tipo === 'tutto' ? 'allievo bloccato' : (tipo === 'ip' ? 'IP ' : 'dispositivo ') + val + ' bloccato'; await st.put('segn:' + s.id, s); }
      }
      return json({ ok: true, blocco: resta ? b : null });
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
    if (p === '/api/docente/elimina') { await st.delete(k); await st.delete('blocco:' + b.email); if (this.blocchi) this.blocchi.delete(b.email); return json({ ok: true }); }
    return errore(404, 'Non trovato.');
  }
}
