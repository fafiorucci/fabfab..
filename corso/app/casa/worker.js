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
   - con MODO = "prova" (Worker «corsonautico-prova», senza Cloudflare Access e con i soli file della prova) si entra
     con il link personale …/?p=<codice> creato dall'istruttore: il codice resta in un cookie e vale fino alla scadenza.
   - account di prova per altre scuole (li crea l'istruttore, con scadenza): app con le lezioni 1-2 e area istruttore
     con allievi inventati; mai i dati veri. Scaduta la prova non si apre più niente. */
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

    if (p.startsWith('/api/')) {
      if (p.startsWith('/api/docente/') && !istruttore) return errore(403, 'Area riservata all’istruttore.');
      const h = new Headers(req.headers); h.set('x-email', email); h.set('x-ruolo', ruolo); h.set('x-origine', url.origin);
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

const linkProva = (env, e) => String(env.PROVA_URL || '').replace(/\/?$/, '/') + '?p=' + e.slice(5);

export class Corso extends DurableObject {
  async corso() { return (await this.env.ASSETS.fetch('https://corso/corso.json')).json(); }
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
      if (p === '/api/docente/allievi') {
        const elenco = allieviInventati(C, d.attive);
        if (a) elenco.unshift({ id: email, nome: a.nome + ' (tu)', creato: a.creato, ultimo: a.ultimo, stato: a.stato });
        return json({ allievi: elenco, indirizzi, attive: d.attive, prova: { scade: d.scade } });
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
      return json({ allievi: elenco, indirizzi, attive: await this.attive(),
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
