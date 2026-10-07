#!/usr/bin/env python3
"""Prepara l'app «da casa» di prova: installabile sul telefono e utilizzabile senza rete, ad accesso riservato.

  SP=<cartella di lavoro> python3 corso/app/casa/prepara_casa.py

Scrive $SP/casa/, da pubblicare su Cloudflare Pages (repository GitHub privato separato) protetto da
Cloudflare Access (email ammesse e codice via email):
- index.html             l'app degli allievi (riconosce «casa» in corso.json), con manifest e service worker;
- corso.json             una sola «lezione»: le 8 slide di «Rotta verso la patente» e la verifica con i
                         6 quiz ufficiali dei numeri d'oro (le slide del corso non vanno sul sito pubblico);
- slides/RV-NNN.jpg      le slide, con la filigrana;
- manifest.webmanifest, sw.js, icone;
- accesso.json           il file che l'app chiede a ogni apertura con la rete per sapere se l'accesso c'è ancora;
- entra/                 la pagina per rientrare con l'email (rimanda all'app);
- _headers               regole di Cloudflare (accesso.json e sw.js mai in cache);
- pubblico/logo.png      il logo per la pagina di accesso di Cloudflare Access: è l'unico file fuori dalla
                         protezione (in Access un'applicazione per il percorso /pubblico con regola «Bypass»).
I progressi passano dall'app dell'aula con «Porta a casa» e tornano con «Invia all'aula».
"""
import collections, io, json, math, os, re, shutil
import pymupdf
from PIL import Image

SP = os.environ.get('SP', '/tmp/scratch')
OUT = SP + '/casa'
QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
PDF = os.path.join(os.path.dirname(APP), 'export', 'pdf')
ROTTA = os.path.join(PDF, 'Rotta verso la patente - Il corso in sintesi.pdf')
FILIGRANA = 'Fabrizio Fiorucci · vietata la duplicazione'
AVVISO = 'La proprietà intellettuale di questo documento è di Fabrizio Fiorucci, ne sono proibite la divulgazione e la duplicazione'


def filigrana(page):
    font = pymupdf.Font('helv'); W, H = page.rect.width, page.rect.height
    size = W / 40; tw = font.text_length(FILIGRANA, fontsize=size); ang = math.degrees(math.atan2(H, W))
    sh = page.new_shape()
    sh.insert_text(pymupdf.Point(W / 2 - tw / 2, H / 2 + size / 3), FILIGRANA, fontsize=size, fontname='helv',
                   color=(0.5, 0.55, 0.6), fill_opacity=0.07, morph=(pymupdf.Point(W / 2, H / 2), pymupdf.Matrix(-ang)))
    sh.commit(overlay=True)
    fs = W / 120
    page.insert_text((W - font.text_length(AVVISO, fontsize=fs) - W * 0.02, H - H * 0.015), AVVISO,
                     fontsize=fs, fontname='helv', color=(0.37, 0.43, 0.51), fill_opacity=0.8)


shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/slides')

# slide di «Rotta verso la patente»
d = pymupdf.open(ROTTA)
testi = [' '.join(d[i].get_text().split()) for i in range(d.page_count)]
for i in range(d.page_count):
    filigrana(d[i])
    zoom = 1280 / d[i].rect.width
    im = Image.open(io.BytesIO(d[i].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes('png'))).convert('RGB')
    im.save(f'{OUT}/slides/RV-{i + 1:03d}.jpg', 'JPEG', quality=74, optimize=True, progressive=True)

# quiz: i numeri d'oro del corso completo, con la slide di Rotta più vicina per parole
C = json.load(open(SP + '/app/corso.json'))
ids = C['schede']['numeri_oro']
toks = lambda t: {w[:6] for w in re.findall(r'[a-zàèéìòù]{4,}', t.lower())}
tp = {i: toks(t) for i, t in enumerate(testi) if i > 0}
df = collections.Counter(w for v in tp.values() for w in v)
quiz = {}
for q in ids:
    Q = C['quiz'][q]; ws = toks(Q['d'] + ' ' + Q['r'][Q['x']])
    best = max(tp, key=lambda i: sum(math.log(len(tp) / df[w]) for w in ws if w in tp[i]))
    quiz[q] = {**Q, 'rivedi': ['RV', best + 1]}
corso = {
    'casa': True, 'accesso': 'accesso.json',
    'lezioni': [{'id': 'RV', 'num': 'Prova', 'titolo': 'Rotta verso la patente · il corso in sintesi', 'attiva': True,
                 'capitoli': [{'titolo': 'Il corso in sintesi', 'pagine': list(range(1, d.page_count + 1)),
                               'quiz': [{'titolo': 'Verifica · i numeri d’oro', 'ids': ids, 'raccolta': False}]}],
                 'scheda': [], 'appendici': []}],
    'appendici': [], 'schede': {'generali': [], 'numeri_oro': []}, 'quiz': quiz,
}
json.dump(corso, open(OUT + '/corso.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# icone dallo stemma
stemma = Image.open(os.path.join(APP, 'stemma-originale.png')).convert('RGBA')
for n in (192, 512):
    stemma.resize((n, n), Image.LANCZOS).save(f'{OUT}/icona-{n}.png', optimize=True)
shutil.copy(os.path.join(APP, 'stemma.webp'), OUT + '/stemma.webp')
os.makedirs(OUT + '/pubblico')
stemma.resize((256, 256), Image.LANCZOS).save(OUT + '/pubblico/logo.png', optimize=True)
json.dump({'name': 'Corso Patente Nautica · a casa', 'short_name': 'Corso nautico', 'start_url': './', 'scope': './',
           'display': 'standalone', 'background_color': '#16324F', 'theme_color': '#16324F', 'lang': 'it',
           'icons': [{'src': 'icona-192.png', 'sizes': '192x192', 'type': 'image/png'},
                     {'src': 'icona-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'}]},
          open(OUT + '/manifest.webmanifest', 'w'), ensure_ascii=False, indent=1)

# app: documento completo, manifest, service worker
h = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
versione = re.search(r"const VERSIONE='([^']+)'", h).group(1)
h = h.replace('<title>Corso Patente Nautica</title>', '<title>Corso nautico a casa</title>', 1)
h = ('<!doctype html>\n<html lang="it">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
     '<meta name="theme-color" content="#16324F">\n<link rel="manifest" href="manifest.webmanifest">\n'
     '<link rel="apple-touch-icon" href="icona-192.png">\n<meta name="apple-mobile-web-app-capable" content="yes">\n' + h)
open(OUT + '/index.html', 'w', encoding='utf-8').write(h)   # il service worker lo registra l'app dopo il controllo dell'accesso

# controllo dell'accesso: senza la sessione di Cloudflare Access la richiesta viene rimandata al login
json.dump({'ok': True}, open(OUT + '/accesso.json', 'w'))
os.makedirs(OUT + '/entra')
open(OUT + '/entra/index.html', 'w', encoding='utf-8').write(
    '<!doctype html>\n<html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    '<title>Corso nautico a casa</title><body style="font-family:Arial,sans-serif;background:#16324F;color:#FFF8EE;padding:24px">'
    '<p>Accesso riuscito, apro il corso…</p><script>location.replace(\'../\')</script></body></html>\n')
open(OUT + '/_headers', 'w').write('/accesso.json\n  Cache-Control: no-store\n/sw.js\n  Cache-Control: no-cache\n/entra/*\n  Cache-Control: no-store\n')

# service worker: conserva tutti i file al primo avvio, poi li serve anche senza rete
file = sorted(os.path.relpath(os.path.join(r, f), OUT).replace(os.sep, '/') for r, _, fs in os.walk(OUT) for f in fs)
file = [f for f in file if f not in ('index.html', 'accesso.json', '_headers', 'entra/index.html') and not f.startswith('pubblico/')]   # index è «./»
sw = open(os.path.join(QUI, 'sw.js'), encoding='utf-8').read()
sw = sw.replace('__VERSIONE__', versione).replace('__FILE__', json.dumps(['./'] + file))
open(OUT + '/sw.js', 'w', encoding='utf-8').write(sw)
print(OUT, len(file) + 1, 'file,', sum(os.path.getsize(os.path.join(OUT, f)) for f in file) // 1024, 'KB; versione', versione)
