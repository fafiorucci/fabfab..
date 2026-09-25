// Genera il menabò in PDF del ricettario a partire dai dati di index.html.
// Uso: node pdf/build-pdf.js  →  ricettario.pdf (formato 17×24 cm)
const fs = require("fs");
const path = require("path");
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");

const ROOT = path.resolve(__dirname, "..");
const src = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");

// I dati vivono nello script della pagina: si estrae il blocco tra l'helper degli ingredienti e l'archivio locale.
const start = src.indexOf("  const i = (q, u, nome)");
const end = src.indexOf("  // ---- Archivio locale");
const { BASE, CENE, TONI } = new Function(src.slice(start, end) + "\nreturn { BASE, CENE, TONI };")();

const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const nf = n => String(Math.round(n * 100) / 100).replace(".", ",");
const qty = g => {
  if (g.q == null) return "q.b.";
  if ((g.u === "g" || g.u === "ml") && g.q >= 1000) return `${nf(g.q / 1000)} ${g.u === "g" ? "kg" : "l"}`;
  return g.u ? `${nf(g.q)} ${g.u}` : nf(g.q);
};
const durata = min => { const h = Math.floor(min / 60), m = min % 60; return h ? (m ? `${h} h ${m} min` : `${h} h`) : `${m} min`; };
// Ordine dei token nelle tavolozze: bg, surface, ink, muted, line, accento, accento tenue, secondo accento, secondo tenue.
const vars = key => {
  const [bg, surface, ink, muted, line, acc, accSoft, acc2, acc2Soft] = TONI[key].light;
  return `--bg:${bg};--surface:${surface};--ink:${ink};--muted:${muted};--line:${line};--acc:${acc};--acc-soft:${accSoft};--acc2:${acc2};--acc2-soft:${acc2Soft}`;
};
const palette = key => `<div class="palette">${TONI[key].sw.map(([n, c]) => `<span class="sw"><i style="background:${c}"></i>${esc(n)}</span>`).join("")}</div>`;
const dots = key => `<span class="dots">${TONI[key].sw.map(([, c]) => `<i style="background:${c}"></i>`).join("")}</span>`;
const storia = paras => `
  <section class="storia">
    <div class="eyebrow">Nel suo tempo</div>
    ${paras.map(t => `<p>${esc(t)}</p>`).join("")}
  </section>`;
const foot = n => `<footer class="foot"><span>Ricettario di casa</span><span>${n}</span></footer>`;

// ---- Impaginazione a pagine fisse: copertina, indice, 2 pagine per capitolo, colophon ----
const chapters = [
  ...CENE.map(c => ({ kind: "cena", data: c })),
  ...BASE.map(r => ({ kind: "ricetta", data: r }))
];
let pageNo = 3;
chapters.forEach(ch => { ch.page = pageNo; pageNo += 2; });
const colophonPage = pageNo;

const cover = `
<section class="page cover">
  <div class="cover-in">
    <p class="kicker">1968 — 1998 · una villa, trent'anni di cene</p>
    <h1>Ricettario<br><em>di casa</em></h1>
    <p class="sub">Ricette scritte a mano sui taccuini, ricopiate nei quaderni, servite a tavole illustri.</p>
    <div class="cover-dots">${chapters.map(ch => dots(ch.data.tono)).join("")}</div>
    <p class="edition">Menabò di prova · settembre 2026</p>
  </div>
</section>`;

const indice = `
<section class="page plain">
  <div class="content">
    <p class="eyebrow">Indice</p>
    <h2 class="h-index">In queste pagine</h2>
    <ol class="toc">
      ${chapters.map((ch, k) => `
        <li>${dots(ch.data.tono)}
          <span class="toc-t">${esc(ch.data.titolo)}<small>${ch.kind === "cena" ? "Menu della cena" : esc(ch.data.categoria) + " · " + esc(ch.data.fonte)}</small></span>
          <span class="toc-p">${ch.page}</span></li>`).join("")}
      <li><span class="dots"></span><span class="toc-t">Nota al menabò<small>Fonti, illustrazioni, testi in bozza</small></span><span class="toc-p">${colophonPage}</span></li>
    </ol>
    <div class="howto">
      <p class="eyebrow">Come leggere questo libro</p>
      <p>Ogni capitolo si apre con i colori del suo piatto: una tavolozza pastello ricavata dagli ingredienti. Segue la ricetta, con il procedimento trascritto parola per parola dall'originale e le dosi ordinate per la cucina di oggi.</p>
    </div>
  </div>
  ${foot(2)}
</section>`;

const opener = (ch, n) => {
  const d = ch.data;
  const eyebrow = ch.kind === "cena"
    ? `Capitolo ${n} · Menu della cena · ${esc(d.quando)}`
    : `Capitolo ${n} · ${esc(d.categoria)} · ${esc(d.fonte)}`;
  return `
<section class="page opener" style="${vars(d.tono)}">
  <div class="content">
    ${d.immagini ? `<figure class="dish"><img src="../img/${d.id}-piatto.jpg" alt=""><figcaption>Illustrazione, non una foto della ricetta</figcaption></figure>` : ""}
    <p class="eyebrow">${eyebrow}</p>
    <h2>${esc(d.titolo)}</h2>
    <p class="claim">${esc(d.claim)}</p>
    <p class="quote">«${esc(d.citazione)}»</p>
    ${palette(d.tono)}
    ${storia(d.storia)}
  </div>
  ${foot(ch.page)}
</section>`;
};

const recipePage = ch => {
  const r = ch.data;
  const label = r.dosiLabel ? (r.dosi === 1 ? r.dosiLabel[0] : r.dosiLabel[1]) : (r.dosi === 1 ? "persona" : "persone");
  return `
<section class="page recipe" style="${vars(r.tono)}">
  <div class="content">
    <header class="mini"><span class="eyebrow">${esc(r.titolo)}</span>${dots(r.tono)}</header>
    <div class="meta">
      <div><span>Tempo stimato</span><b>${durata(r.tempo)}</b></div>
      <div><span>Dosi</span><b>${r.dosi} ${esc(label)}</b></div>
      <div><span>Difficoltà</span><b>${esc(r.difficolta)}</b></div>
    </div>
    <div class="cols">
      <section>
        <h3>Ingredienti</h3>
        ${r.immagini ? `<img class="ingr-img" src="../img/${r.id}-ingredienti.jpg" alt="">` : ""}
        <ul class="ingr">${r.ingredienti.map(g => `<li><span class="q${g.q == null ? " qb" : ""}">${esc(qty(g))}</span><span>${esc(g.nome)}</span></li>`).join("")}</ul>
      </section>
      <section>
        <h3>Procedimento</h3>
        <p class="hint">Trascritto fedelmente dall'originale.</p>
        <ol class="steps">${r.passi.map(p => `<li>${esc(p)}</li>`).join("")}</ol>
      </section>
    </div>
    ${r.riposo ? `<div class="note"><b>Da sapere:</b> oltre al tempo di preparazione servono ${esc(r.riposo)}.</div>` : ""}
    ${r.daVerificare ? `<div class="note check"><b>Da chiedere o verificare</b><ul>${r.daVerificare.map(t => `<li>${esc(t)}</li>`).join("")}</ul></div>` : ""}
  </div>
  ${foot(ch.page + 1)}
</section>`;
};

const menuPage = ch => {
  const c = ch.data;
  return `
<section class="page recipe" style="${vars(c.tono)}">
  <div class="content">
    <header class="mini"><span class="eyebrow">${esc(c.titolo)} · il menu</span>${dots(c.tono)}</header>
    <ol class="menu">
      ${c.portate.map(p => `<li><span class="portata">${esc(p.portata)}</span><div>${p.piatti.map(d => `
        <p class="piatto">${esc(d.nome)}${d.nota ? `<small>${esc(d.nota)}</small>` : ""}</p>`).join("")}</div></li>`).join("")}
    </ol>
    <div class="note check"><b>Da chiedere per ricostruire la serata</b><ul>${c.domande.map(q => `<li>${esc(q)}</li>`).join("")}</ul></div>
  </div>
  ${foot(ch.page + 1)}
</section>`;
};

const colophon = `
<section class="page plain">
  <div class="content colophon">
    <p class="eyebrow">Nota al menabò</p>
    <h2 class="h-index">Come è fatto questo libro</h2>
    <p>Le ricette sono trascritte parola per parola dai taccuini, dai quaderni e dai fogli sciolti dell'archivio; accanto a ciascuna è indicato dove si trova l'originale. Le dosi sono state ordinate per la cucina di oggi, mentre tempi e difficoltà sono stime da verificare in cucina.</p>
    <p>I testi «Nel suo tempo» sono bozze di contesto storico e artistico, da verificare in redazione prima della stampa. I ricordi di chi ha cucinato in quella villa si aggiungeranno dalle interviste.</p>
    <p>Le illustrazioni ad acquerello sono state generate con Canva per immaginare i piatti: non sono fotografie delle ricette e verranno sostituite dalle fotografie dei piatti cucinati.</p>
    <p>Le tavolozze di ogni capitolo sono ricavate dai colori degli ingredienti.</p>
  </div>
  ${foot(colophonPage)}
</section>`;

const f = name => `url("fonts/${name}") format("truetype")`;
const html = `<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Ricettario di casa</title>
<style>
  @font-face { font-family: "Fraunces"; font-weight: 300; font-style: normal; src: ${f("Fraunces-300.ttf")}; }
  @font-face { font-family: "Fraunces"; font-weight: 400; font-style: normal; src: ${f("Fraunces-400.ttf")}; }
  @font-face { font-family: "Fraunces"; font-weight: 300; font-style: italic; src: ${f("Fraunces-300italic.ttf")}; }
  @font-face { font-family: "Fraunces"; font-weight: 400; font-style: italic; src: ${f("Fraunces-400italic.ttf")}; }
  @font-face { font-family: "Figtree"; font-weight: 400; src: ${f("Figtree-400.ttf")}; }
  @font-face { font-family: "Figtree"; font-weight: 600; src: ${f("Figtree-600.ttf")}; }
  @page { size: 170mm 240mm; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body { font: 9.5pt/1.5 "Figtree", sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact;
    --bg: #F6F3EF; --surface: #FFFDFB; --ink: #27231F; --muted: #6B635B; --line: #E6DFD6; --acc: #6A5577; --acc-soft: #EDE6F0; --acc2: #B9785C; --acc2-soft: #F6E6DC; }
  .page { width: 170mm; height: 240mm; position: relative; overflow: hidden; break-after: page; color: var(--ink); background: var(--surface); }
  .content { position: absolute; inset: 16mm 17mm 20mm; overflow: hidden; }
  .foot { position: absolute; left: 17mm; right: 17mm; bottom: 9mm; display: flex; justify-content: space-between; font-size: 7.5pt; color: var(--muted); letter-spacing: .06em; text-transform: uppercase; }
  .eyebrow { margin: 0; font-size: 7.5pt; font-weight: 600; text-transform: uppercase; letter-spacing: .14em; color: var(--acc); }
  .dots { display: inline-flex; flex: none; vertical-align: middle; }
  .dots i { width: 9px; height: 9px; border-radius: 50%; border: 1.2px solid var(--surface); margin-left: -3px; }
  .dots i:first-child { margin-left: 0; }

  /* Copertina */
  .cover { background:
      radial-gradient(60mm 60mm at 12% 14%, #F3DC7A88, transparent 70%),
      radial-gradient(70mm 70mm at 92% 22%, #E9A9A088, transparent 70%),
      radial-gradient(80mm 80mm at 18% 88%, #C5D3B099, transparent 70%),
      radial-gradient(70mm 70mm at 88% 84%, #9C98C477, transparent 70%),
      radial-gradient(60mm 60mm at 55% 55%, #E6D0B866, transparent 70%),
      #FBF8F3; }
  .cover-in { position: absolute; inset: 26mm 18mm 20mm; display: flex; flex-direction: column; }
  .kicker { margin: 0; font-size: 8pt; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: #6A5577; }
  .cover h1 { margin: 10mm 0 0; font: 300 64pt/.9 "Fraunces", serif; letter-spacing: -.03em; color: #27231F; }
  .cover h1 em { font-weight: 300; color: #8C3F4A; }
  .cover .sub { margin: 9mm 0 0; font: italic 300 14pt/1.35 "Fraunces", serif; max-width: 105mm; color: #4A433D; }
  .cover-dots { margin-top: auto; display: flex; gap: 7mm; }
  .cover-dots .dots i { width: 16px; height: 16px; margin-left: -5px; border-width: 2px; border-color: #FBF8F3; }
  .cover-dots .dots i:first-child { margin-left: 0; }
  .edition { margin: 6mm 0 0; font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; color: #6B635B; }

  /* Indice e colophon */
  .plain { background: #FBF8F3; }
  .h-index { font: 300 30pt/1 "Fraunces", serif; letter-spacing: -.02em; margin: 3mm 0 9mm; }
  .toc { list-style: none; margin: 0; padding: 0; }
  .toc li { display: grid; grid-template-columns: 14mm 1fr auto; align-items: baseline; gap: 3mm; padding: 3.2mm 0; border-bottom: 0.3mm solid #E6DFD6; }
  .toc-t { font: 400 14pt/1.2 "Fraunces", serif; }
  .toc-t small { display: block; font: 8pt/1.4 "Figtree", sans-serif; color: #6B635B; margin-top: 1mm; }
  .toc-p { font: 300 14pt "Fraunces", serif; font-variant-numeric: tabular-nums; }
  .howto { margin-top: 12mm; max-width: 110mm; }
  .howto p:last-child { margin: 2mm 0 0; font: 300 11pt/1.55 "Fraunces", serif; }
  .colophon p:not(.eyebrow) { font: 300 11pt/1.6 "Fraunces", serif; margin: 0 0 4mm; max-width: 118mm; }

  /* Apertura di capitolo: i toni del piatto */
  .opener { background: linear-gradient(160deg, var(--acc-soft) 0%, var(--bg) 55%, var(--acc2-soft) 100%); }
  .opener h2 { margin: 4mm 0 0; font: 300 40pt/.95 "Fraunces", serif; letter-spacing: -.025em; max-width: 92mm; }
  .claim { margin: 5mm 0 0; font-size: 10.5pt; font-weight: 600; max-width: 88mm; line-height: 1.4; }
  .quote { margin: 3mm 0 0; font: italic 300 14pt/1.3 "Fraunces", serif; color: var(--acc); max-width: 90mm; }
  .dish { float: right; margin: 0 0 4mm 5mm; width: 50mm; display: grid; gap: 1.5mm; justify-items: center; }
  .dish img { width: 50mm; border-radius: 5mm; border: 1.6mm solid var(--surface); box-shadow: 0 3mm 7mm rgba(0,0,0,.10); rotate: 2.5deg; }
  .dish figcaption { font-size: 6.5pt; color: var(--muted); }
  .palette { display: flex; flex-wrap: wrap; gap: 1.8mm; margin-top: 5mm; }
  .sw { display: inline-flex; align-items: center; gap: 1.8mm; padding: .8mm 2.6mm .8mm .8mm; border-radius: 99px; background: var(--surface); font-size: 7.5pt; font-weight: 600; }
  .sw i { width: 4.6mm; height: 4.6mm; border-radius: 50%; box-shadow: inset 0 0 0 .25mm rgba(0,0,0,.08); }
  .storia { clear: both; margin-top: 7mm; padding-top: 5mm; border-top: .3mm solid var(--line); }
  .storia p { margin: 2.5mm 0 0; font: 300 10pt/1.55 "Fraunces", serif; }
  .storia p:first-of-type::first-letter { float: left; font-size: 3.3em; line-height: .8; padding: 1mm 2mm 0 0; color: var(--acc); }

  /* Pagina ricetta */
  .recipe { background: var(--surface); }
  .mini { display: flex; justify-content: space-between; align-items: center; padding-bottom: 3mm; border-bottom: .3mm solid var(--line); }
  .meta { display: flex; gap: 2.5mm; margin: 4mm 0 5mm; }
  .meta div { background: var(--bg); border-radius: 4mm; padding: 2mm 4mm; display: grid; }
  .meta span { font-size: 6.5pt; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
  .meta b { font-weight: 600; font-size: 9.5pt; }
  .cols { display: grid; grid-template-columns: 52mm 1fr; gap: 7mm; }
  h3 { margin: 0 0 3mm; font: 400 16pt/1 "Fraunces", serif; }
  .ingr-img { width: 40mm; border-radius: 4mm; margin-bottom: 3mm; display: block; }
  .ingr { list-style: none; margin: 0; padding: 0; }
  .ingr li { display: grid; grid-template-columns: 17mm 1fr; gap: 2.5mm; padding: 1.1mm 0; border-bottom: .25mm dashed var(--line); font-size: 8.6pt; line-height: 1.35; }
  .q { text-align: right; font-weight: 600; color: var(--acc); font-variant-numeric: tabular-nums; }
  .q.qb { font-weight: 400; font-style: italic; color: var(--muted); }
  .hint { margin: -1.5mm 0 3mm; font-size: 7.5pt; color: var(--muted); }
  .steps { list-style: none; margin: 0; padding: 0; counter-reset: s; display: grid; gap: 3mm; }
  .steps li { counter-increment: s; display: grid; grid-template-columns: 7mm 1fr; gap: 2.5mm; font-size: 9.3pt; line-height: 1.5; }
  .steps li::before { content: counter(s); width: 6.5mm; height: 6.5mm; border-radius: 50%; display: grid; place-items: center; background: var(--acc2-soft); font: 400 9pt/1 "Fraunces", serif; }
  .note { margin-top: 3.5mm; background: var(--acc2-soft); border-radius: 4mm; padding: 3mm 4.5mm; font-size: 8.3pt; line-height: 1.45; }
  .note.check { background: var(--acc-soft); }
  .note ul { margin: 1.5mm 0 0; padding-left: 4mm; }

  /* Menu della cena */
  .menu { list-style: none; margin: 4mm 0 0; padding: 0; }
  .menu > li { display: grid; grid-template-columns: 26mm 1fr; gap: 4mm; padding: 2.6mm 0; border-bottom: .25mm dashed var(--line); }
  .portata { font-size: 7pt; font-weight: 600; text-transform: uppercase; letter-spacing: .12em; color: var(--acc); padding-top: 1.6mm; }
  .piatto { margin: 0; font: 400 13pt/1.2 "Fraunces", serif; }
  .piatto + .piatto { margin-top: 2mm; }
  .piatto small { display: block; font: 8pt/1.4 "Figtree", sans-serif; color: var(--muted); margin-top: .6mm; }
</style></head><body>
${cover}
${indice}
${chapters.map((ch, k) => opener(ch, k + 1) + (ch.kind === "cena" ? menuPage(ch) : recipePage(ch))).join("")}
${colophon}
</body></html>`;

(async () => {
  const out = path.join(__dirname, "libro.html");
  fs.writeFileSync(out, html);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + out);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  // Controllo: nessuna pagina deve tagliare il testo.
  const overflow = await page.$$eval(".page .content", els => els
    .map((el, k) => ({ page: k + 1, over: el.scrollHeight - el.clientHeight }))
    .filter(x => x.over > 1));
  const fontsOk = await page.evaluate(() => [...document.fonts].filter(f => f.status === "loaded").length);
  await page.pdf({ path: path.join(ROOT, "ricettario.pdf"), width: "170mm", height: "240mm", printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log(JSON.stringify({ pages: colophonPage, fontsLoaded: fontsOk, overflow }));
})();
