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

  const json = (dati, stato = 200) => new Response(JSON.stringify(dati), { status: stato, headers: { 'Content-Type': 'application/json' } });
  window.fetch = async (url, opt = {}) => {
    const u = typeof url === 'string' ? url : url.url;
    if (!/^api\//.test(u)) return orig(url, opt);
    await pronto;
    const b = opt.body ? JSON.parse(opt.body) : {};
    // indirizzo d'aula di esempio: il QR non porta da nessuna parte e l'indirizzo non si mostra
    const app = 'http://192.168.1.20:8000';
    switch (u) {
      case 'api/info': return json({ aula: true, versione: '0.1.0 · demo', attive: ATT });
      case 'api/docente/allievi': return json({ allievi, indirizzi: [app], attive: ATT });
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
    st.textContent = '.addr{display:none!important}';   // nessun indirizzo da aprire nella demo
    document.head.append(st);
    const d = document.createElement('div');
    d.style.cssText = 'background:#FFC145;color:#16324F;font:800 14px "Nunito Sans",Arial,sans-serif;padding:10px 16px;text-align:center';
    d.innerHTML = 'Area istruttore di esempio: allievi e risultati sono inventati, le modifiche non vengono salvate. <a href="./" style="color:#16324F">← Torna all’app</a>';
    document.body.prepend(d);
  });
})();
