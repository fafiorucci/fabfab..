/* Proiettore per le presentazioni esportate in HTML (corso/export/html).
   Una slide alla volta, adattata allo schermo. Avanti: → ↓ PagGiù Spazio Invio o clic a destra;
   indietro: ← ↑ PagSu o clic a sinistra; Inizio/Fine; F = schermo intero. Il telecomando del
   presentatore manda PagSu/PagGiù e funziona. Aggiunto da prepara_pacchetto.py.
   Con window.VISORE = "allievo" (appendici nell'app, da app_build.py): niente avvio a schermo intero,
   «Torna al corso», si sfoglia anche scorrendo col dito, filigrana leggera sopra le slide. */
(function(){
  const allievo = window.VISORE === 'allievo';
  const css = `
  body.pres{margin:0;background:#0B1826;overflow:hidden;height:100vh;display:flex;align-items:center;justify-content:center;cursor:default}
  body.pres header, body.pres .nt{display:none}
  body.pres .w{display:none;margin:0;border-radius:0;max-width:none;width:min(100vw,calc(100vh * 16 / 9))}
  body.pres .w.on{display:block}
  .pbar{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);display:flex;gap:6px;align-items:center;
        background:rgba(11,24,38,.86);color:#fff;border-radius:999px;padding:6px 8px;font:800 15px 'Nunito Sans',Arial,sans-serif;
        box-shadow:0 6px 20px rgba(0,0,0,.35);transition:opacity .3s;z-index:9}
  .pbar.off{opacity:0;pointer-events:none}
  .pbar button,.pbar a{white-space:nowrap;font:inherit;color:#fff;background:transparent;border:0;border-radius:999px;padding:6px 12px;cursor:pointer;text-decoration:none}
  .pbar button:hover,.pbar a:hover{background:rgba(255,255,255,.14)}
  .pbar .n{font-variant-numeric:tabular-nums;min-width:74px;text-align:center}
  .pstart{position:fixed;inset:0;display:grid;place-items:center;background:rgba(11,24,38,.55);z-index:10;cursor:pointer}
  .pmark{position:fixed;inset:0;pointer-events:none;z-index:8;display:grid;place-items:center;overflow:hidden}
  .pmark span{transform:rotate(-29deg);font:700 min(4.2vw,7.4vh) 'Nunito Sans',Arial,sans-serif;color:rgba(80,90,105,.10);white-space:nowrap}
  .pnote{position:fixed;left:12px;right:12px;top:6px;text-align:center;font:600 10px 'Nunito Sans',Arial,sans-serif;color:rgba(201,214,227,.75);pointer-events:none;z-index:8}
  .pstart div{background:#FFC145;color:#16324F;font:700 26px 'Fredoka','Trebuchet MS',sans-serif;padding:18px 30px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.4)}`;
  document.head.append(Object.assign(document.createElement('style'), {textContent: css}));
  document.body.classList.add('pres');

  const slides = [...document.querySelectorAll('.w')];
  if (!slides.length) return;
  let i = Math.min(Math.max((parseInt(location.hash.slice(1), 10) || 1) - 1, 0), slides.length - 1);

  const bar = document.createElement('div');
  bar.className = 'pbar';
  bar.innerHTML = (allievo ? '<a href="../" title="Torna al corso">← Corso</a>' : '<a href="/docente" title="Torna all’area istruttore">← Elenco</a>')
    + '<button data-d="-1" title="Indietro (←)">‹</button><span class="n"></span>'
    + '<button data-d="1" title="Avanti (→)">›</button>'
    + '<button data-fs title="Schermo intero (F)">⛶' + (allievo ? '' : ' Schermo intero') + '</button>';
  document.body.append(bar);
  if (allievo) {
    // torna alla pagina dell'app da cui si è arrivati, senza ricaricarla
    bar.querySelector('a').addEventListener('click', e => {
      try { if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) { e.preventDefault(); history.back(); } } catch (x) {}
    });
    const mark = document.createElement('div'); mark.className = 'pmark';
    mark.innerHTML = '<span>Fabrizio Fiorucci · vietata la duplicazione</span>';
    const nota = document.createElement('div'); nota.className = 'pnote';
    nota.textContent = 'La proprietà intellettuale di questo materiale è di Fabrizio Fiorucci, ne sono proibite la divulgazione e la duplicazione.';
    document.body.append(mark, nota);
  }
  const num = bar.querySelector('.n');

  function fit(){ const w = slides[i]; w.firstChild.style.transform = 'scale(' + (w.clientWidth / 1920) + ')'; }
  function show(n){
    i = Math.min(Math.max(n, 0), slides.length - 1);
    slides.forEach((w, k) => w.classList.toggle('on', k === i));
    fit();
    num.textContent = (i + 1) + ' / ' + slides.length;
    history.replaceState(null, '', '#' + (i + 1));
  }
  const inFs = () => document.fullscreenElement || document.webkitFullscreenElement;
  function fullscreen(){
    const d = document.documentElement, rq = d.requestFullscreen || d.webkitRequestFullscreen;
    const ex = document.exitFullscreen || document.webkitExitFullscreen;
    try { const r = inFs() ? ex.call(document) : rq.call(d); if (r && r.catch) r.catch(() => {}); } catch (e) {}
  }

  // all'apertura (solo in aula): un clic per passare a schermo intero (il browser lo consente solo dopo un gesto)
  const start = document.createElement('div');
  start.className = 'pstart';
  start.innerHTML = '<div>▶ Clic per proiettare a schermo intero</div>';
  start.addEventListener('click', e => { e.stopPropagation(); start.remove(); fullscreen(); wake(); });
  if (!allievo) document.body.append(start);

  // la barra sparisce quando il mouse sta fermo, così sullo schermo resta solo la slide
  let t = null;
  function wake(){ bar.classList.remove('off'); clearTimeout(t); t = setTimeout(() => bar.classList.add('off'), 2500); }
  addEventListener('mousemove', wake);

  bar.addEventListener('click', e => {
    e.stopPropagation();
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.fs !== undefined) fullscreen(); else show(i + Number(b.dataset.d));
  });
  addEventListener('click', e => {
    if (e.target.closest('.pbar,.pstart')) return;
    const f = e.clientX / innerWidth;
    if (allievo && f > 1 / 3 && f < 2 / 3) { wake(); return; }   // al centro: mostra solo i comandi
    show(f > 1 / 3 ? i + 1 : i - 1); wake();
  });
  let x0 = null;
  addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, {passive: true});
  addEventListener('touchend', e => {
    if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) { show(dx < 0 ? i + 1 : i - 1); wake(); }
  }, {passive: true});
  addEventListener('keydown', e => {
    const k = e.key;
    if (start.isConnected) { start.remove(); fullscreen(); wake(); }
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(k)) { show(i + 1); e.preventDefault(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { show(i - 1); e.preventDefault(); }
    else if (k === 'Home') show(0);
    else if (k === 'End') show(slides.length - 1);
    else if (k === 'f' || k === 'F') fullscreen();
  });
  addEventListener('resize', fit);


  show(i); wake();
})();
