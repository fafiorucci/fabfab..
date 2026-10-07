#!/usr/bin/env python3
"""Prepara l'app «da casa»: installabile sul telefono e utilizzabile senza rete, ad accesso riservato.

  SP=<cartella di lavoro> python3 corso/app/casa/prepara_casa.py

Parte dall'uscita completa di app_build.py ($SP/app), come la web app: le 15 lezioni (aperte solo quelle con
«attiva» in corso.json, le altre si vedono oscurate), schede, numeri d'oro e appendici.
Scrive $SP/casa/, da pubblicare con Cloudflare (Worker con file statici collegato al repository GitHub privato
separato) protetto da Cloudflare Access (email ammesse e codice via email):
- index.html, corso.json  l'app degli allievi (riconosce «casa» in corso.json);
- slides/                 le slide delle lezioni aperte e le schede (già con la filigrana); appendici/;
- manifest.webmanifest, sw.js, icone;
- accesso.json            il file che l'app chiede a ogni apertura con la rete per sapere se l'accesso c'è ancora;
- entra/                  la pagina per rientrare con l'email (rimanda all'app);
- _headers                regole di Cloudflare (accesso.json e sw.js mai in cache);
- pubblico/logo.png       il logo per la pagina di accesso di Cloudflare Access: è l'unico file fuori dalla
                          protezione (in Access un'applicazione per il percorso /pubblico con regola «Bypass»).
I progressi passano dall'app dell'aula con «Porta a casa» e tornano con «Invia all'aula».
Quando si apre una nuova lezione (campo «attiva»), si rifà app_build.py e questo script e si pubblica.
"""
import json, os, re, shutil
from PIL import Image

SP = os.environ.get('SP', '/tmp/scratch')
SRC, OUT = SP + '/app', SP + '/casa'
QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/slides')

# contenuti: tutto corso.json; delle slide solo lezioni aperte e schede (le altre lezioni restano oscurate)
C = json.load(open(SRC + '/corso.json'))
aperte = {L['id'] for L in C['lezioni'] if L.get('attiva')}
for f in sorted(os.listdir(SRC + '/slides')):
    if f.split('-')[0] in aperte | {'SR'}:
        shutil.copy(f'{SRC}/slides/{f}', f'{OUT}/slides/{f}')
shutil.copytree(SRC + '/appendici', OUT + '/appendici')
C = {'casa': True, 'accesso': 'accesso.json', **C}
json.dump(C, open(OUT + '/corso.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# icone dallo stemma
stemma = Image.open(os.path.join(APP, 'stemma-originale.png')).convert('RGBA')
for n in (192, 512):
    stemma.resize((n, n), Image.LANCZOS).save(f'{OUT}/icona-{n}.png', optimize=True)
shutil.copy(os.path.join(APP, 'stemma.webp'), OUT + '/stemma.webp')
os.makedirs(OUT + '/pubblico')
Image.open(os.path.join(QUI, 'logo-accesso.png')).convert('RGBA').resize((256, 256), Image.LANCZOS).save(OUT + '/pubblico/logo.png', optimize=True)
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
