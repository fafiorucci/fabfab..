/* Area istruttore di esempio per la demo: sostituisce il server dell'aula con dati inventati,
   tenuti in memoria (si ripartono a ogni apertura). Caricato da docente.html prima del suo script. */
(function(){
  try { sessionStorage.setItem('corso-aula-pin', 'demo'); } catch (e) {}
  const orig = window.fetch.bind(window);
  let ATT = ['L01'], allievi = [];

  // allievi e risultati inventati, costruiti sui contenuti della demo
  const pronto = orig('corso.json').then(r => r.json()).then(C => {
    const L = C.lezioni[0], pagine = L.capitoli.flatMap(c => c.pagine), quiz = L.capitoli.flatMap(c => c.quiz.flatMap(s => s.ids));
    const tutti = [...quiz, ...C.schede.numeri_oro];
    const giorno = (n, h, m) => { const d = new Date(); d.setDate(d.getDate() + n); d.setHours(h, m, 0, 0); return d.toISOString().slice(0, 19); };
    const data = n => { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
    const persone = [
      ['Giulia', 'Ferri', '#E4572E', 'senza', 'entrambe', 21, 0.9, 0.95, 0],
      ['Marco', 'Bassi', '#0B8A99', 'entro', 'motore', 9, 0.7, 0.6, -1],
      ['Sara', 'Conti', '#7B5CD6', 'senza', 'vela', 35, 1, 0.85, 0],
      ['Luca', 'Moretti', '#2F6FDB', 'entro', 'motore', 9, 0.4, 0.5, -3],
      ['Elena', 'Galli', '#2E9E5B', '', '', null, 0.2, 0.7, -6],
      ['Paolo', 'Riva', '#F4A300', 'senza', 'motore', 48, 0.8, 0.4, -2],
    ];
    allievi = persone.map(([nome, cognome, colore, ambito, tipo, esame, vista, bravura, ultimo], i) => {
      const visti = { L01: pagine.slice(0, Math.round(pagine.length * vista)) };
      const risposte = {};
      tutti.slice(0, Math.round(tutti.length * vista)).forEach((q, k) => {
        const ok = ((k * 7 + i * 3) % 10) / 10 < bravura;
        risposte[q] = { ok, scelta: ok ? C.quiz[q].x : (C.quiz[q].x + 1) % C.quiz[q].r.length, ts: giorno(ultimo, 10, 0),
                        tentativi: ok && k % 4 === 0 ? 2 : 1, rivisto: !ok && k % 2 === 0 };
      });
      const profilo = { nome, cognome, colore };
      if (ambito) Object.assign(profilo, { ambito, tipo, esame: data(esame) });
      if (i % 2 === 0) profilo.email = nome.toLowerCase() + '@esempio.it';
      return { id: 'demo' + i, nome: nome + ' ' + cognome, creato: giorno(-20 + i, 9, 0), ultimo: giorno(ultimo, 9 + i, 12 * i % 60),
               stato: { visti, risposte, profilo, diario: {} } };
    });
  });

  // registro degli accessi di esempio (come nell'app online): giorni, IP con la città, dispositivi, segnalazioni e blocchi
  let SEGN = [], BLOCCHI = {};
  const GIORNI = {};   // id allievo → giorni, dal più recente
  const prima = minuti => new Date(Date.now() - minuti * 60e3).toISOString().slice(0, 19);   // sempre nel passato
  const quando = (n, h, m) => { const d = new Date(); d.setDate(d.getDate() + n); d.setHours(h, m, 0, 0); return d.toISOString().slice(0, 19); };
  const LUOGHI = ['Roma', 'Milano', 'Napoli', 'Torino', 'Firenze', 'Bologna'];
  const TIPI_DISP = ['iPhone · Safari', 'Android · Chrome', 'Windows · Chrome', 'Mac · Safari', 'iPad · Safari', 'Android · Samsung Internet'];
  const accessi = pronto.then(() => {
    allievi.forEach((a, i) => {
      const ip = `93.${40 + i}.${11 + 3 * i}.${20 + i}`, citta = LUOGHI[i % LUOGHI.length];
      const disp = [{ id: 'd' + i + 'a1b2c3', ua: TIPI_DISP[i % 6] }, { id: 'd' + i + 'e4f5g6', ua: TIPI_DISP[(i + 2) % 6] }];
      if (i === 0) disp.push({ id: 'd0h7i8j9', ua: 'Android · Chrome' }, { id: 'd0k1l2m3', ua: 'Windows · Chrome' });   // Giulia: 4 dispositivi
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
      if (i === 1) gg[0].ip.push({ ip: '151.20.33.7', luogo: 'Roma', n: 3, primo: prima(110), ultimo: prima(95) });   // Marco: Milano e Roma nella stessa ora
      if (i === 5) gg[0].ip.push({ ip: '88.12.4.90', luogo: 'Barcellona, Spagna', n: 2, primo: prima(200), ultimo: prima(185) });   // Paolo: dall'estero
      GIORNI[a.id] = gg;
    });
    const segn = (i, tipo, testo, minuti) => { const a = allievi[i], gg = GIORNI[a.id].slice(0, 7);
      const ip = new Map(), dd = new Map();
      for (const g of gg) { for (const x of g.ip) if (!ip.has(x.ip)) ip.set(x.ip, x); for (const x of g.disp) if (!dd.has(x.id)) dd.set(x.id, x); }
      return { id: 'esempio' + i, email: a.id, nome: a.nome, tipo, testo, creato: prima(minuti), stato: 'aperta',
               ip: [...ip.values()].map(x => ({ ip: x.ip, luogo: x.luogo, ultimo: x.ultimo, n: x.n })), disp: [...dd.values()] }; };
    SEGN = [segn(1, 'viaggio', 'Accessi da due luoghi lontani 477 km nella stessa ora: Milano e Roma', 90),
            segn(0, 'dispositivi', '4 dispositivi diversi negli ultimi 7 giorni', 25),
            segn(5, 'estero', 'Accesso dall’estero: Barcellona, Spagna', 180)];
  });
  const riassunto = (gg, n) => { const da = quando(-(n - 1), 0, 0).slice(0, 10), t = { n: {}, ip: new Set(), disp: new Set(), luoghi: new Set() };
    for (const g of gg.filter(g => g.data >= da)) { for (const [k, v] of Object.entries(g.n)) t.n[k] = (t.n[k] || 0) + v;
      g.ip.forEach(x => { t.ip.add(x.ip); t.luoghi.add(x.luogo); }); g.disp.forEach(x => t.disp.add(x.id)); }
    return { n: t.n, ip: t.ip.size, disp: t.disp.size, luoghi: [...t.luoghi] }; };
  const contatore = () => { const aperte = SEGN.filter(s => s.stato === 'aperta'); return { aperte: aperte.length, segnalati: [...new Set(aperte.map(s => s.email))] }; };

  const json = (dati, stato = 200) => new Response(JSON.stringify(dati), { status: stato, headers: { 'Content-Type': 'application/json' } });
  window.fetch = async (url, opt = {}) => {
    const u = typeof url === 'string' ? url : url.url;
    if (!/^api\//.test(u)) return orig(url, opt);
    await pronto; await accessi;
    const b = opt.body ? JSON.parse(opt.body) : {};
    // indirizzo d'aula di esempio: il QR non porta da nessuna parte e l'indirizzo non si mostra
    const app = 'http://192.168.1.20:8000';
    switch (u) {
      case 'api/info': return json({ aula: true, versione: '__VERSIONE__ · demo', attive: ATT });
      case 'api/docente/allievi': return json({ allievi, indirizzi: [app], attive: ATT, accessi: contatore() });
      case 'api/docente/accessi':
        return json({ email: false, giorni: 90, segnalazioni: SEGN.filter(s => s.stato === 'aperta').concat(SEGN.filter(s => s.stato !== 'aperta')),
          allievi: allievi.map(a => { const gg = GIORNI[a.id] || [];
            return { id: a.id, nome: a.nome, ultimo: gg[0] ? gg[0].ip.map(x => x.ultimo).sort().pop() : null, d7: riassunto(gg, 7), d30: riassunto(gg, 30), blocco: BLOCCHI[a.id] || null }; }) });
      case 'api/docente/accessi-allievo': return json({ giorni: GIORNI[b.id] || [], blocco: BLOCCHI[b.id] || null });
      case 'api/docente/segnalazione': { const s = SEGN.find(x => x.id === b.sid); if (s) s.stato = 'archiviata'; return json({ ok: true }); }
      case 'api/docente/blocca': case 'api/docente/sblocca': {
        const x = BLOCCHI[b.id] || { tutto: false, ip: {}, disp: {} }, ora = new Date().toISOString().slice(0, 19);
        if (u.endsWith('/blocca')) { if (b.tipo === 'tutto') x.tutto = ora; else x[b.tipo][b.valore] = ora; }
        else { if (b.tipo === 'tutto') x.tutto = false; else delete x[b.tipo][b.valore]; }
        BLOCCHI[b.id] = x.tutto || Object.keys(x.ip).length || Object.keys(x.disp).length ? x : null;
        const s = b.sid && SEGN.find(y => y.id === b.sid);
        if (s && u.endsWith('/blocca')) { s.stato = 'bloccata'; s.azione = b.tipo === 'tutto' ? 'allievo bloccato' : (b.tipo === 'ip' ? 'IP ' : 'dispositivo ') + b.valore + ' bloccato'; }
        return json({ ok: true, blocco: BLOCCHI[b.id] });
      }
      case 'api/docente/lezione':
        ATT = b.attiva ? [...new Set([...ATT, b.id])] : ATT.filter(x => x !== b.id);
        return json({ attive: ATT });
      case 'api/docente/codice': return json({ codice: String(1000 + Math.floor(Math.random() * 9000)) });
      case 'api/docente/azzera': {
        const a = allievi.find(x => x.id === b.id); if (a) a.stato = { visti: {}, risposte: {}, profilo: a.stato.profilo, diario: {} };
        return json({ ok: true });
      }
      case 'api/docente/elimina': allievi = allievi.filter(x => x.id !== b.id); return json({ ok: true });
    }
    return json({ errore: 'Non disponibile nella demo.' }, 404);
  };

  // presentazioni: niente nuove schede, le slide di esempio si sfogliano dentro la pagina
  addEventListener('click', e => {
    const a = e.target.closest && e.target.closest('a.pcard');
    if (!a) return;
    e.preventDefault();
    const ov = document.createElement('div');
    ov.style.cssText = 'position:fixed;inset:0;z-index:60;background:#0B1826;display:flex;flex-direction:column';
    const top = document.createElement('div');
    top.style.cssText = 'display:flex;align-items:center;gap:12px;padding:10px 16px;color:#fff;font:800 15px "Nunito Sans",Arial,sans-serif';
    top.innerHTML = '<span style="flex:1">Esempio di presentazione · frecce o clic a destra/sinistra per sfogliare</span>';
    const x = document.createElement('button');
    x.textContent = '✕ Chiudi'; x.style.cssText = 'font:inherit;color:#16324F;background:#FFC145;border:0;border-radius:999px;padding:8px 16px;cursor:pointer';
    const fr = document.createElement('iframe');
    fr.src = a.getAttribute('href'); fr.title = 'Esempio di presentazione';
    fr.style.cssText = 'flex:1;border:0;width:100%';
    const chiudi = () => { ov.remove(); removeEventListener('keydown', esc); };
    const esc = ev => { if (ev.key === 'Escape') chiudi(); };
    x.onclick = chiudi; addEventListener('keydown', esc);
    top.append(x); ov.append(top, fr); document.body.append(ov);
    fr.addEventListener('load', () => { try { fr.contentWindow.focus(); } catch (er) {} });
  }, true);

  // avviso in cima alla pagina
  addEventListener('DOMContentLoaded', () => {
    const st = document.createElement('style');
    st.textContent = '.qrbox .addr,.proj .addr,.prova-nuovo .addr,td .addr{display:none!important}';   // nessun indirizzo da aprire nella demo (gli IP degli accessi sì)
    document.head.append(st);
    const d = document.createElement('div');
    d.style.cssText = 'background:#FFC145;color:#16324F;font:800 14px "Nunito Sans",Arial,sans-serif;padding:10px 16px;text-align:center';
    d.innerHTML = 'Area istruttore di esempio: allievi e risultati sono inventati, le modifiche non vengono salvate. <a href="./" style="color:#16324F">← Torna all’app</a>';
    document.body.prepend(d);
  });
})();
