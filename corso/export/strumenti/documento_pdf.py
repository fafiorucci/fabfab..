#!/usr/bin/env python3
"""Impagina un documento Markdown in PDF A4 con la grafica delle slide del corso.

  python3 corso/export/strumenti/documento_pdf.py "corso/export/istruzioni/Linee guida dell'app del corso.md" \
      "corso/export/istruzioni/Linee guida dell'app del corso.pdf" [--etichetta "Linee guida · istruttore"]

Il Markdown comincia con «# Titolo», poi una riga con data e autore, poi il paragrafo di apertura; le sezioni sono «## …».
In copertina: riquadro blu notte con etichetta, titolo, onda gialla, apertura e il logo di Onda Portante Sailing.
Ogni pagina: fondo carta con macchia e onde come le slide, a piè di pagina il logo, la dicitura del corso, il numero
di pagina e l'avviso sulla proprietà intellettuale.
Requisiti: Playwright con Chromium in /opt/pw-browsers, python-markdown, pymupdf, Pillow; rete per i Google Fonts.
"""
import argparse, asyncio, base64, html, io, os, re, tempfile
import markdown, pymupdf
from PIL import Image
from playwright.async_api import async_playwright

QUI = os.path.dirname(os.path.abspath(__file__))
CORSO = os.path.dirname(os.path.dirname(QUI))
LOGO = os.path.join(CORSO, 'app', 'casa', 'logo-accesso.png')   # Onda Portante Sailing
DICITURA = 'Fabrizio Fiorucci · Patente nautica Vela/Motore entro le 12 miglia e senza limiti dalla costa'
AVVISO = ('La proprietà intellettuale di questo documento è di Fabrizio Fiorucci, '
          'ne sono proibite la divulgazione e la duplicazione.')
COLORI = ['#E4572E', '#0B8A99', '#7B5CD6', '#2F6FDB', '#2E9E5B']
CHROMIUM = '/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None


def png64(percorso, lato):
    im = Image.open(percorso).convert('RGBA'); im.thumbnail((lato, lato))
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def onda(colore, larghezza=120):
    return (f'<svg class="onda" width="{larghezza}" height="12" viewBox="0 0 {larghezza} 12"><path d="M2 6 '
            + ''.join(f'q{7.5} -6 15 0 t15 0 ' for _ in range(larghezza // 30))
            + f'" fill="none" stroke="{colore}" stroke-width="4" stroke-linecap="round"/></svg>')


def leggi(md):
    righe = md.strip().split('\n\n')
    titolo = re.sub(r'^#\s+', '', righe[0].strip())
    data, apertura, corpo = righe[1].strip(), righe[2].strip(), '\n\n'.join(righe[3:])
    return titolo, data, apertura, corpo


def corpo_html(corpo):
    h = markdown.markdown(corpo, extensions=['tables', 'sane_lists'])
    # ogni sezione: numero in una pastiglia colorata, titolo e onda come nelle slide
    n = 0

    def sezione(m):
        nonlocal n
        c = COLORI[n % len(COLORI)]; n += 1
        return (f'</section><section class="sez" style="--c:{c}"><div class="testa"><span class="num">{n:02d}</span>'
                f'<h2>{m.group(1)}</h2></div>{onda(c)}')
    h = re.sub(r'<h2>(.*?)</h2>', sezione, h)
    h = h.replace('<table>', '<div class="tab"><table>').replace('</table>', '</table></div>')
    return re.sub(r'^</section>', '', h) + '</section>'


PAGINA = """<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{titolo}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Nunito+Sans:wght@400;600;700;800;900&display=block">
<style>
@page {{ size: A4; margin: 15mm 17mm 27mm 17mm }}
:root {{ --ink:#1B2A41; --body:#34465E; --soft:#5E6E82; --line:#EDE5D6; --navy:#16324F; --sun:#FFC145; --coral:#E4572E; --sea:#0B8A99 }}
* {{ box-sizing: border-box }}
html, body {{ margin: 0; background: transparent; color: var(--body); font: 10.5pt/1.5 'Nunito Sans', Arial, sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.copertina {{ position: relative; background: var(--navy); color: #FFF8EE; border-radius: 22px; padding: 26px 30px 34px;
  display: grid; grid-template-columns: 1fr 150px; gap: 22px; align-items: center; overflow: hidden; margin-bottom: 14px }}
.copertina .etichetta {{ display: inline-block; background: var(--sun); color: var(--navy); font-weight: 900; font-size: 8.5pt;
  letter-spacing: .08em; text-transform: uppercase; border-radius: 20px; padding: 3px 12px }}
.copertina h1 {{ font-family: Fredoka, 'Trebuchet MS', sans-serif; font-weight: 700; font-size: 27pt; line-height: 1.08;
  margin: 12px 0 6px; color: #fff }}
.copertina p {{ margin: 10px 0 0; font-size: 11pt; color: #DCE6F0; font-weight: 600 }}
.copertina .data {{ font-size: 9pt; color: var(--sun); font-weight: 800; margin-top: 12px }}
.copertina img {{ width: 150px; height: 150px; border-radius: 50%; box-shadow: 0 6px 18px rgba(0,0,0,.35) }}
.copertina .onde {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px }}
.sez {{ margin-top: 20px }}
.testa {{ display: flex; align-items: center; gap: 10px; break-after: avoid }}
.num {{ flex: none; width: 30px; height: 30px; border-radius: 50%; background: var(--c); color: #fff; display: grid; place-items: center;
  font: 700 11pt Fredoka, sans-serif }}
h2 {{ font-family: Fredoka, 'Trebuchet MS', sans-serif; font-weight: 700; font-size: 16pt; color: var(--c); margin: 0; line-height: 1.15 }}
.onda {{ display: block; margin: 2px 0 6px 40px; break-after: avoid }}
p {{ margin: 6px 0 }}
.onda + p {{ break-after: avoid }}   /* il titolo della sezione non resta da solo in fondo alla pagina */
a {{ color: #0B6F7C; text-decoration: none; border-bottom: 1px solid #9CD3DA }}
strong {{ color: var(--ink) }}
ul, ol {{ margin: 6px 0; padding-left: 0; list-style: none }}
li {{ position: relative; padding-left: 26px; margin: 5px 0; break-inside: avoid }}
ul > li::before {{ content: ""; position: absolute; left: 8px; top: .55em; width: 7px; height: 7px; border-radius: 50%; background: var(--c) }}
ol {{ counter-reset: n }}
ol > li {{ counter-increment: n }}
ol > li::before {{ content: counter(n); position: absolute; left: 0; top: .1em; width: 18px; height: 18px; border-radius: 50%;
  background: var(--c); color: #fff; font: 700 8.5pt/18px Fredoka, sans-serif; text-align: center }}
.tab {{ background: #fff; border-radius: 14px; border-left: 6px solid var(--c); box-shadow: 0 3px 12px rgba(27,42,65,.08);
  margin: 8px 0; overflow: hidden }}
table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt }}
th {{ text-align: left; font-size: 7.5pt; letter-spacing: .07em; text-transform: uppercase; color: var(--c); font-weight: 900;
  padding: 8px 10px; border-bottom: 2px solid var(--line) }}
td {{ padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top }}
tr:last-child td {{ border-bottom: 0 }}
tr {{ break-inside: avoid }}
td:first-child {{ font-weight: 800; color: var(--ink) }}
</style></head><body>
<header class="copertina">
  <div><span class="etichetta">{etichetta}</span><h1>{titolo}</h1>{onda_gialla}<p>{apertura}</p><div class="data">{data}</div></div>
  <img src="{logo}" alt="Onda Portante Sailing">
  <svg class="onde" viewBox="0 0 600 22" preserveAspectRatio="none"><path d="M0 10 Q37 0 75 10 T150 10 T225 10 T300 10 T375 10 T450 10 T525 10 T600 10 V22 H0Z" fill="#12A4B5" fill-opacity=".45"/></svg>
</header>
{corpo}
</body></html>"""

# fondo di ogni pagina, come le slide: carta, macchia in alto a destra, puntini, onde in basso
FONDO = """<!doctype html><html><head><meta charset="utf-8"><style>@page{size:A4;margin:0} html,body{margin:0}
body{width:210mm;height:297mm;background:#FFF8EE;-webkit-print-color-adjust:exact;print-color-adjust:exact;position:relative;overflow:hidden}
svg{position:absolute;inset:0;width:210mm;height:297mm}</style></head><body>
<svg viewBox="0 0 210 297" preserveAspectRatio="none">
<path d="M150 -10 Q205 -18 222 22 Q236 60 200 72 Q170 82 156 58 Q140 30 150 -10Z" fill="#FFE3D9" fill-opacity=".75"/>
<circle cx="200" cy="96" r="3.2" fill="#ECE6FB"/><circle cx="194" cy="104" r="1.6" fill="#DFF3E4"/>
<path d="M-12 245 Q20 228 40 252 Q58 274 30 300 L-12 300Z" fill="#DFF3E4" fill-opacity=".8"/>
<path d="M0 284 Q13 279 26 284 T52 284 T78 284 T104 284 T130 284 T156 284 T182 284 T208 284 T234 284 V297 H0Z" fill="#12A4B5" fill-opacity=".14"/>
<path d="M0 289 Q15 284 30 289 T60 289 T90 289 T120 289 T150 289 T180 289 T210 289 V297 H0Z" fill="#12A4B5" fill-opacity=".18"/>
</svg></body></html>"""

PIEDE = """<style>*{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style>
<div style="width:100%;margin:0 17mm;font-family:Arial,sans-serif;color:#34465E">
 <div style="display:flex;align-items:center;gap:7px;font-size:8.5px;font-weight:600">
  <img src="{logo}" style="width:20px;height:20px;border-radius:50%">
  <span>{dicitura}</span>
  <span style="margin-left:auto;background:#E4572E;color:#fff;border-radius:9px;padding:1px 8px;font-weight:800;font-size:8.5px"><span class="pageNumber"></span></span>
 </div>
 <div style="font-size:6.8px;color:#5E6E82;margin-top:3px;padding-left:27px">{avviso}</div>
</div>"""


async def stampa(pagina_html, fondo_html, piede, pdf, fondo_pdf):
    async with async_playwright() as p:
        # caratteri da Google Fonts (dietro il proxy, se c'è): quelli locali dell'aula hanno Nunito Sans solo extra-grassetto
        proxy = {'proxy': {'server': os.environ['HTTPS_PROXY']}} if os.environ.get('HTTPS_PROXY') else {}
        b = await p.chromium.launch(args=['--ignore-certificate-errors'], **proxy, **({'executable_path': CHROMIUM} if CHROMIUM else {}))
        pg = await b.new_page()
        with tempfile.TemporaryDirectory() as t:
            for nome, testo, uscita, opz in (('d.html', pagina_html, pdf, dict(display_header_footer=True, header_template='<span></span>', footer_template=piede)),
                                             ('f.html', fondo_html, fondo_pdf, {})):
                f = os.path.join(t, nome); open(f, 'w', encoding='utf-8').write(testo)
                await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                await pg.pdf(path=uscita, format='A4', print_background=True, prefer_css_page_size=True, **opz)
        await b.close()


def main():
    a = argparse.ArgumentParser(); a.add_argument('md'); a.add_argument('pdf')
    a.add_argument('--etichetta', default='Linee guida · per l’istruttore')
    x = a.parse_args()
    titolo, data, apertura, corpo = leggi(open(x.md, encoding='utf-8').read())
    pagina = PAGINA.format(titolo=html.escape(titolo), etichetta=html.escape(x.etichetta),
                           onda_gialla=onda('#FFC145', 150), apertura=html.escape(apertura), data=html.escape(data),
                           logo=png64(LOGO, 360), corpo=corpo_html(corpo))
    piede = PIEDE.format(logo=png64(LOGO, 80), dicitura=html.escape(DICITURA),
                         avviso=html.escape(AVVISO))
    with tempfile.TemporaryDirectory() as t:
        contenuto, fondo = os.path.join(t, 'c.pdf'), os.path.join(t, 'f.pdf')
        asyncio.run(stampa(pagina, FONDO, piede, contenuto, fondo))
        doc, sotto = pymupdf.open(contenuto), pymupdf.open(fondo)
        for pag in doc:   # il fondo va sotto il testo: i link restano cliccabili
            pag.show_pdf_page(pag.rect, sotto, 0, overlay=False)
        doc.set_metadata({'title': titolo, 'author': 'Fabrizio Fiorucci', 'subject': x.etichetta, 'creator': '', 'producer': ''})
        doc.save(x.pdf, garbage=3, deflate=True)
        print(x.pdf, doc.page_count, 'pagine,', os.path.getsize(x.pdf) // 1024, 'KB')


if __name__ == '__main__':
    main()
