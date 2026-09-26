// Genera il menabò in PDF del ricettario a partire dai dati di index.html.
// Uso: node pdf/build-pdf.js  →  ricettario.pdf (formato 17×24 cm). Stampa l'elenco delle pagine che sforano.
const fs = require("fs");
const path = require("path");
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");
const { ICONS, iconFor, dishFor, iconSvg, dishSvg, ILL_CSS } = require("./illustrazioni");

const ROOT = path.resolve(__dirname, "..");
const src = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");

// I dati vivono nello script della pagina: si estrae il blocco tra l'helper degli ingredienti e l'archivio locale.
const start = src.indexOf("  const i = (q, u, nome)");
const end = src.indexOf("  // ---- Archivio locale");
const { BASE, CENE, TONI } = new Function(src.slice(start, end) + "\nreturn { BASE, CENE, TONI };")();

const LABELS = {
  farina: "Farina", burro: "Burro", zucchero: "Zucchero", uovo: "Uova", lievito: "Lievito", banana: "Banane",
  mela: "Mele", uvetta: "Uvetta", cedro: "Cedro candito", limone: "Limone", pane: "Pane", latte: "Latte",
  cannella: "Cannella", piccione: "Piccioni", lardo: "Lardo", cipolla: "Cipolle", aceto: "Aceto", alloro: "Alloro",
  chiodo: "Chiodi di garofano", ginepro: "Ginepro", salepepe: "Sale e pepe", brodo: "Brodo", mandorla: "Mandorle",
  liquore: "Liquore", vaniglia: "Zucchero vanigliato", incerto: "Parola da decifrare"
};

const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const nf = n => String(Math.round(n * 100) / 100).replace(".", ",");
const qty = g => {
  if (g.q == null) return "q.b.";
  if ((g.u === "g" || g.u === "ml") && g.q >= 1000) return `${nf(g.q / 1000)} ${g.u === "g" ? "kg" : "l"}`;
  return g.u ? `${nf(g.q)} ${g.u}` : nf(g.q);
};
const durata = min => { const h = Math.floor(min / 60), m = min % 60; return h ? (m ? `${h} h ${m} min` : `${h} h`) : `${m} min`; };
const two = n => String(n).padStart(2, "0");
// Ordine dei token nelle tavolozze: bg, surface, ink, muted, line, accento, accento tenue, secondo accento, secondo tenue.
const vars = key => {
  const [bg, surface, ink, muted, line, acc, accSoft, acc2, acc2Soft] = TONI[key].light;
  return `--bg:${bg};--surface:${surface};--ink:${ink};--muted:${muted};--line:${line};--acc:${acc};--acc-soft:${accSoft};--acc2:${acc2};--acc2-soft:${acc2Soft}`;
};
const palette = key => `<div class="palette">${TONI[key].sw.map(([n, c]) => `<span class="sw"><i style="background:${c}"></i>${esc(n)}</span>`).join("")}</div>`;
const foot = n => `<footer class="foot"><span>Ricettario di casa</span><span class="pn">${n}</span></footer>`;
const uniq = a => [...new Set(a)];
const recipeIcons = r => uniq(r.ingredienti.map(g => iconFor(g.nome)).filter(k => k !== "incerto"));

// ---- Impaginazione a pagine fisse: copertina, indice, dispensa, 3 pagine per capitolo, colophon ----
const chapters = [
  ...CENE.map(c => ({ kind: "cena", data: c, dish: c.id })),
  ...BASE.map(r => ({ kind: "ricetta", data: r, dish: r.id }))
];
let pageNo = 4;
chapters.forEach((ch, k) => { ch.n = k + 1; ch.page = pageNo; pageNo += 3; });
const colophonPage = pageNo;

// Copertina: una tappezzeria di ingredienti con il titolo al centro.
const coverKeys = Object.keys(ICONS).filter(k => k !== "incerto");
const coverTiles = Array.from({ length: 48 }, (_, k) => {
  const key = coverKeys[(k * 7) % coverKeys.length];
  const rot = ((k * 37) % 30) - 15;
  return `<div class="tile" style="rotate:${rot}deg">${iconSvg(key)}</div>`;
}).join("");
const cover = `
<section class="page cover">
  <div class="tiles">${coverTiles}</div>
  <div class="cover-card">
    <p class="kicker">1968 — 1998 · una villa, trent'anni di cene</p>
    <h1>Ricettario</h1>
    <p class="hand">di casa</p>
    <p class="sub">Ricette scritte a mano sui taccuini, ricopiate nei quaderni, servite a tavole illustri.</p>
    <p class="edition">Menabò di prova · 2026</p>
  </div>
</section>`;

const indice = `
<section class="page plain">
  <div class="content">
    <h2 class="big">Indice</h2>
    <ol class="toc">
      ${chapters.map(ch => `
        <li style="${vars(ch.data.tono)}">
          <span class="toc-ill">${dishSvg(ch.dish)}</span>
          <span class="toc-t"><em class="hand-n">${two(ch.n)}</em>${esc(ch.data.titolo)}<small>${ch.kind === "cena" ? "Menu della cena · " + esc(ch.data.quando) : esc(ch.data.categoria) + " · " + esc(ch.data.fonte)}</small></span>
          <span class="toc-p">${ch.page}</span>
        </li>`).join("")}
      <li class="toc-extra"><span class="toc-ill small">${iconSvg("farina")}</span><span class="toc-t">La dispensa<small>Tutti gli ingredienti, disegnati</small></span><span class="toc-p">3</span></li>
      <li class="toc-extra"><span class="toc-ill small">${iconSvg("incerto")}</span><span class="toc-t">Nota al menabò<small>Fonti, illustrazioni, testi in bozza</small></span><span class="toc-p">${colophonPage}</span></li>
    </ol>
  </div>
  ${foot(2)}
</section>`;

const dispensa = `
<section class="page plain">
  <div class="content">
    <h2 class="big">La dispensa</h2>
    <p class="lead">Tutti gli ingredienti di questo libro, disegnati uno per uno.</p>
    <div class="pantry">
      ${Object.keys(ICONS).map(k => `<figure>${iconSvg(k)}<figcaption>${LABELS[k]}</figcaption></figure>`).join("")}
    </div>
  </div>
  ${foot(3)}
</section>`;

const opener = ch => {
  const d = ch.data;
  const eyebrow = ch.kind === "cena" ? `Menu della cena · ${esc(d.quando)}` : `${esc(d.categoria)} · ${esc(d.fonte)}`;
  return `
<section class="page opener" style="${vars(d.tono)}">
  <div class="num">${two(ch.n)}</div>
  <svg class="blob" viewBox="0 0 200 160"><path d="M38 22 C70 -6 142 2 172 30 C198 54 196 104 170 128 C142 154 70 158 36 134 C6 112 8 46 38 22 Z"/></svg>
  <div class="hero-ill">${dishSvg(ch.dish)}</div>
  <div class="opener-text">
    <p class="eyebrow">Capitolo ${two(ch.n)} · ${eyebrow}</p>
    <h2>${esc(d.titolo)}</h2>
    <p class="hand quote">${esc(d.citazione)}</p>
    <p class="claim">${esc(d.claim)}</p>
    ${palette(d.tono)}
  </div>
  ${foot(ch.page)}
</section>`;
};

const storiaPage = ch => {
  const d = ch.data;
  const icons = ch.kind === "cena" ? ["alloro", "pane", "cipolla", "liquore"] : recipeIcons(d).slice(0, 5);
  const meta = ch.kind === "cena" ? "" : `
    <div class="meta">
      <div><span>Tempo stimato</span><b>${durata(d.tempo)}</b></div>
      <div><span>Dosi</span><b>${d.dosi} ${esc(d.dosiLabel ? (d.dosi === 1 ? d.dosiLabel[0] : d.dosiLabel[1]) : (d.dosi === 1 ? "persona" : "persone"))}</b></div>
      <div><span>Difficoltà</span><b>${esc(d.difficolta)}</b></div>
      ${d.riposo ? `<div><span>Da sapere</span><b>${esc(d.riposo)}</b></div>` : ""}
    </div>`;
  const domande = "";
  return `
<section class="page storia-page" style="${vars(d.tono)}">
  <aside class="rail">
    <span class="rail-t">Nel suo tempo</span>
    <div class="rail-icons">${icons.map(k => iconSvg(k)).join("")}</div>
  </aside>
  <div class="content with-rail">
    <p class="eyebrow">Capitolo ${two(ch.n)} · ${esc(d.titolo)}</p>
    <div class="storia">${d.storia.map(t => `<p>${esc(t)}</p>`).join("")}</div>
    <p class="draft">Testo di contesto in bozza, da verificare in redazione. I ricordi di chi cucinava si aggiungeranno dalle interviste.</p>
    ${meta}
    ${domande}
  </div>
  ${foot(ch.page + 1)}
</section>`;
};

const recipePage = ch => {
  const r = ch.data;
  return `
<section class="page recipe" style="${vars(r.tono)}">
  <div class="content">
    <header class="rhead">
      <span class="rhead-ill">${dishSvg(r.id)}</span>
      <div><p class="eyebrow">Capitolo ${two(ch.n)} · la ricetta</p><h3 class="rtitle">${esc(r.titolo)}</h3></div>
    </header>
    <h4>Ingredienti</h4>
    <div class="cards${r.ingredienti.length > 6 ? " three" : ""}">
      ${r.ingredienti.map(g => `<div class="card">${iconSvg(iconFor(g.nome))}<div><b class="${g.q == null ? "qb" : ""}">${esc(qty(g))}</b><span>${esc(g.nome)}</span></div></div>`).join("")}
    </div>
    <h4>Procedimento <small>trascritto fedelmente dall'originale</small></h4>
    <ol class="steps">${r.passi.map((p, k) => `<li><span class="hand-n">${k + 1}</span><p>${esc(p)}</p></li>`).join("")}</ol>
    ${r.daVerificare ? `<div class="note check"><b>Da chiedere o verificare</b><ul>${r.daVerificare.map(t => `<li>${esc(t)}</li>`).join("")}</ul></div>` : ""}
  </div>
  ${foot(ch.page + 2)}
</section>`;
};

const menuPage = ch => {
  const c = ch.data;
  const piatti = c.portate.flatMap(p => p.piatti.map(d => ({ ...d, portata: p.portata })));
  return `
<section class="page recipe" style="${vars(c.tono)}">
  <div class="content">
    <p class="eyebrow">Capitolo ${two(ch.n)} · ${esc(c.titolo)}</p>
    <h2 class="big menu-t">Il menu</h2>
    <div class="menu">
      ${piatti.map(d => `
        <div class="dish">
          <div class="dish-ill">${dishFor(d.nome) ? dishSvg(dishFor(d.nome)) : ""}</div>
          <p class="eyebrow">${esc(d.portata)}</p>
          <p class="dish-n">${esc(d.nome)}</p>
          ${d.nota ? `<p class="dish-note">${esc(d.nota)}</p>` : ""}
        </div>`).join("")}
    </div>
  </div>
  ${foot(ch.page + 2)}
</section>`;
};

const colophon = `
<section class="page plain">
  <div class="content colophon">
    <h2 class="big">Nota al menabò</h2>
    <p>Le ricette sono trascritte parola per parola dai taccuini, dai quaderni e dai fogli sciolti dell'archivio; accanto a ciascuna è indicato dove si trova l'originale. Le dosi sono ordinate per la cucina di oggi; tempi e difficoltà sono stime da verificare in cucina.</p>
    <p>I testi «Nel suo tempo» sono bozze di contesto storico e artistico, da verificare in redazione prima della stampa. I ricordi di chi ha cucinato in quella villa si aggiungeranno dalle interviste.</p>
    <p>Icone e disegni sono illustrazioni vettoriali realizzate per questo menabò: raccontano gli ingredienti e i piatti, ma non sostituiscono le fotografie dei piatti cucinati, che verranno scattate per l'edizione definitiva.</p>
    <p>Le tavolozze di ogni capitolo sono ricavate dai colori degli ingredienti. Caratteri: Fraunces, Figtree, Homemade Apple.</p>
    ${CENE.map(c => `<div class="note check"><b>Da chiedere ancora · ${esc(c.titolo)}</b><ul>${c.domande.map(q => `<li>${esc(q)}</li>`).join("")}</ul></div>`).join("")}
    <div class="colophon-icons">${["uovo", "farina", "burro", "mela", "mandorla", "alloro", "ginepro"].map(k => iconSvg(k)).join("")}</div>
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
  @font-face { font-family: "Homemade Apple"; font-weight: 400; src: ${f("HomemadeApple-400.ttf")}; }
  ${ILL_CSS}
  @page { size: 170mm 240mm; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body { font: 9.5pt/1.5 "Figtree", sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact;
    --bg: #F6F2EC; --surface: #FFFDF9; --ink: #2E2924; --muted: #6E655C; --line: #E6DED3; --acc: #6A5577; --acc-soft: #EDE6F0; --acc2: #B9785C; --acc2-soft: #F6E6DC; }
  .page { width: 170mm; height: 240mm; position: relative; overflow: hidden; break-after: page; color: var(--ink); background: var(--surface); }
  .content { position: absolute; inset: 16mm 17mm 20mm; overflow: hidden; }
  .foot { position: absolute; left: 17mm; right: 17mm; bottom: 9mm; display: flex; justify-content: space-between; align-items: baseline; font-size: 7pt; color: var(--muted); letter-spacing: .12em; text-transform: uppercase; }
  .foot .pn { font: 300 11pt "Fraunces", serif; letter-spacing: 0; color: var(--ink); }
  .eyebrow { margin: 0; font-size: 7pt; font-weight: 600; text-transform: uppercase; letter-spacing: .16em; color: var(--acc); }
  .hand { font-family: "Homemade Apple", cursive; }
  .hand-n { font: 400 normal 1em "Homemade Apple", cursive; color: var(--acc); }
  .big { margin: 0; font: 300 40pt/.95 "Fraunces", serif; letter-spacing: -.03em; }
  .lead { margin: 3mm 0 0; font: italic 300 12pt/1.4 "Fraunces", serif; color: var(--muted); }

  /* Copertina */
  .cover { background: #FBF6EE; }
  .tiles { position: absolute; inset: -6mm; display: grid; grid-template-columns: repeat(6, 1fr); grid-auto-rows: 31mm; place-items: center; }
  .tile { width: 17mm; }
  .cover-card { position: absolute; left: 19mm; right: 19mm; top: 58mm; padding: 13mm 12mm 11mm; background: #FFFDF9; border-radius: 9mm;
    box-shadow: 0 4mm 14mm rgba(60, 45, 30, .12); text-align: center; }
  .kicker { margin: 0; font-size: 7pt; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: #6A5577; }
  .cover h1 { margin: 7mm 0 0; font: 300 60pt/.9 "Fraunces", serif; letter-spacing: -.035em; color: #2E2924; }
  .cover .hand { margin: 1mm 0 0; font-size: 28pt; line-height: 1.3; color: #B04F66; rotate: -4deg; }
  .cover .sub { margin: 7mm auto 0; font: italic 300 12pt/1.4 "Fraunces", serif; max-width: 92mm; color: #5C534B; }
  .edition { margin: 8mm 0 0; font-size: 7pt; letter-spacing: .16em; text-transform: uppercase; color: #8A8076; }

  /* Pagine neutre */
  .plain { background: #FBF6EE; }
  .toc { list-style: none; margin: 7mm 0 0; padding: 0; }
  .toc li { display: grid; grid-template-columns: 27mm 1fr auto; align-items: center; gap: 4mm; padding: 1.6mm 3mm; margin-bottom: 2mm; border-radius: 5mm; background: var(--acc-soft); }
  .toc li.toc-extra { background: transparent; border: .3mm dashed #E0D6C8; }
  .toc-ill { width: 27mm; }
  .toc-ill.small { width: 10mm; justify-self: center; }
  .toc-t { font: 400 15pt/1.15 "Fraunces", serif; }
  .toc-t .hand-n { font-size: 10pt; margin-right: 3mm; }
  .toc-t small { display: block; font: 7.5pt/1.4 "Figtree", sans-serif; color: var(--muted); margin-top: 1mm; }
  .toc-p { font: 300 18pt "Fraunces", serif; padding-right: 2mm; }
  .pantry { margin-top: 8mm; display: grid; grid-template-columns: repeat(5, 1fr); gap: 4mm 3mm; }
  .pantry figure { margin: 0; display: grid; justify-items: center; gap: 1.5mm; }
  .pantry .ill { width: 17mm; }
  .pantry figcaption { font-size: 7.5pt; text-align: center; line-height: 1.25; }
  .colophon p { font: 300 10.5pt/1.6 "Fraunces", serif; margin: 5mm 0 0; max-width: 120mm; }
  .colophon-icons { display: flex; gap: 5mm; margin-top: 12mm; }
  .colophon-icons .ill { width: 13mm; }

  /* Apertura: il piatto a tutta pagina nei suoi colori */
  .opener { background: linear-gradient(165deg, var(--acc-soft) 0%, var(--bg) 52%, var(--acc2-soft) 100%); }
  .num { position: absolute; right: 12mm; top: 6mm; font: 300 130pt/1 "Fraunces", serif; color: transparent; -webkit-text-stroke: .35mm var(--acc); letter-spacing: -.04em; opacity: .55; }
  .blob { position: absolute; left: 14mm; top: 30mm; width: 142mm; }
  .blob path { fill: var(--surface); opacity: .75; }
  .hero-ill { position: absolute; left: 24mm; top: 36mm; width: 122mm; }
  .opener-text { position: absolute; left: 17mm; right: 17mm; bottom: 22mm; }
  .opener h2 { margin: 3mm 0 0; font: 300 42pt/.95 "Fraunces", serif; letter-spacing: -.03em; }
  .quote { margin: 3mm 0 0; font-size: 13pt; line-height: 1.6; color: var(--acc); }
  .claim { margin: 3mm 0 0; font-size: 10pt; font-weight: 600; max-width: 110mm; }
  .palette { display: flex; flex-wrap: wrap; gap: 1.8mm; margin-top: 5mm; }
  .sw { display: inline-flex; align-items: center; gap: 1.8mm; padding: .8mm 2.8mm .8mm .8mm; border-radius: 99px; background: var(--surface); font-size: 7pt; font-weight: 600; }
  .sw i { width: 4.6mm; height: 4.6mm; border-radius: 50%; box-shadow: inset 0 0 0 .25mm rgba(0,0,0,.08); }

  /* Nel suo tempo */
  .storia-page { background: var(--surface); }
  .rail { position: absolute; left: 0; top: 0; bottom: 0; width: 30mm; background: var(--acc-soft); display: flex; flex-direction: column; align-items: center; padding: 16mm 0 20mm; gap: 8mm; }
  .rail-t { writing-mode: vertical-rl; rotate: 180deg; font: italic 300 20pt "Fraunces", serif; color: var(--acc); }
  .rail-icons { display: grid; gap: 5mm; margin-top: auto; }
  .rail-icons .ill { width: 14mm; }
  .content.with-rail { left: 40mm; }
  .storia { margin-top: 6mm; }
  .storia p { margin: 0 0 3.2mm; font: 300 10.6pt/1.62 "Fraunces", serif; }
  .storia p:first-child::first-letter { float: left; font-size: 3.6em; line-height: .8; padding: 1mm 2mm 0 0; color: var(--acc); }
  .draft { margin: 2mm 0 0; font-size: 7pt; color: var(--muted); }
  .meta { display: flex; flex-wrap: wrap; gap: 2.5mm; margin-top: 7mm; }
  .meta div { background: var(--bg); border-radius: 4mm; padding: 2mm 4mm; display: grid; }
  .meta span { font-size: 6.5pt; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
  .meta b { font-weight: 600; font-size: 9pt; }
  .note { margin-top: 5mm; background: var(--acc2-soft); border-radius: 4mm; padding: 3mm 4.5mm; font-size: 8.2pt; line-height: 1.45; }
  .note.check { background: var(--acc-soft); }
  .note ul { margin: 1.5mm 0 0; padding-left: 4mm; }

  /* La ricetta */
  .recipe { background: var(--surface); }
  .rhead { display: grid; grid-template-columns: 36mm 1fr; gap: 5mm; align-items: center; padding-bottom: 4mm; border-bottom: .3mm solid var(--line); }
  .rtitle { margin: 1.5mm 0 0; font: 300 24pt/1 "Fraunces", serif; letter-spacing: -.02em; }
  h4 { margin: 5mm 0 3mm; font: 400 14pt/1 "Fraunces", serif; }
  h4 small { font: 7pt "Figtree", sans-serif; color: var(--muted); margin-left: 2mm; letter-spacing: .02em; }
  .cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 2.6mm; }
  .card { display: grid; grid-template-columns: 15mm 1fr; gap: 3mm; align-items: center; background: var(--bg); border-radius: 4mm; padding: 2mm 3mm 2mm 2mm; }
  .card b { display: block; font: 400 12pt/1.1 "Fraunces", serif; color: var(--acc); }
  .card b.qb { font-style: italic; color: var(--muted); }
  .card span { display: block; font-size: 8.6pt; line-height: 1.3; margin-top: .6mm; }
  .cards.three { grid-template-columns: repeat(3, 1fr); gap: 2.2mm; }
  .cards.three .card { grid-template-columns: 11mm 1fr; gap: 2mm; padding: 1.6mm 2.2mm 1.6mm 1.6mm; }
  .cards.three .card b { font-size: 10pt; }
  .cards.three .card span { font-size: 7.8pt; }
  .steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 3mm; }
  .steps li { display: grid; grid-template-columns: 9mm 1fr; gap: 2mm; align-items: start; }
  .steps .hand-n { font-size: 13pt; line-height: 1.2; }
  .steps p { margin: 0; font-size: 9.8pt; line-height: 1.55; }

  /* Il menu della cena */
  .menu-t { margin-top: 2mm; }
  .menu { margin-top: 6mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm 4mm; }
  .dish { background: var(--bg); border-radius: 4mm; padding: 2mm 3mm 3mm; }
  .dish-ill { height: 26mm; display: grid; place-items: center; }
  .dish-ill .ill { width: 32mm; }
  .dish-n { margin: 1mm 0 0; font: 400 11pt/1.15 "Fraunces", serif; }
  .dish-note { margin: 1mm 0 0; font-size: 6.8pt; line-height: 1.35; color: var(--muted); }
</style></head><body>
${cover}
${indice}
${dispensa}
${chapters.map(ch => opener(ch) + storiaPage(ch) + (ch.kind === "cena" ? menuPage(ch) : recipePage(ch))).join("")}
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
  const overflow = await page.$$eval(".page", pages => pages.map((p, k) => {
    const c = p.querySelector(".content, .opener-text");
    if (!c) return null;
    const over = c.classList.contains("opener-text")
      ? c.getBoundingClientRect().top - (p.querySelector(".hero-ill").getBoundingClientRect().bottom)
      : -(c.scrollHeight - c.clientHeight);
    return over < -1 ? { page: k + 1, over: Math.round(-over) } : null;
  }).filter(Boolean));
  await page.pdf({ path: path.join(ROOT, "ricettario.pdf"), width: "170mm", height: "240mm", printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log(JSON.stringify({ pages: colophonPage, overflow }));
})();
