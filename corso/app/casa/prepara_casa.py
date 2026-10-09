#!/usr/bin/env python3
"""Prepara l'app online del corso: un solo indirizzo per gli allievi, a casa e in aula, con i progressi salvati
online e l'area istruttore. Installabile sul telefono e utilizzabile senza rete, ad accesso riservato.

  SP=<cartella di lavoro> python3 corso/app/casa/prepara_casa.py

Parte dal pacchetto dell'aula (corso/app/aula/www, rifatto da aula/prepara_pacchetto.py: slide, appendici,
caratteri in locale, presentazioni, area istruttore) e da corso/app/index.html.
Scrive $SP/casa/, il contenuto del repository privato «corso-nautico-prova», che Cloudflare pubblica a ogni push:
- wrangler.jsonc          configurazione del Worker «corsonautico-ondaportante» (file statici, Durable Object,
                          email dell'istruttore, team e applicazione di Cloudflare Access);
- src/worker.js           il server (da casa/worker.js): progressi degli allievi, area istruttore, lezioni aperte;
- public/                 i file del sito: index.html e corso.json (con «online»), slide di tutte le lezioni
                          (il Worker dà solo quelle delle lezioni aperte), appendici, presentazioni, docente.html,
                          manifest, sw.js, icone, accesso.json, entra/, _headers.
Il sito è protetto da Cloudflare Access (email ammesse e codice via email). Le lezioni si aprono dall'area
istruttore online (…/docente), senza ripubblicare. Il logo della pagina di accesso sta fuori dal sito protetto,
nel progetto Cloudflare Pages «onda-logo» (https://onda-logo.pages.dev/logo.png; l'immagine è logo-accesso.png).
"""
import json, os, re, shutil
from PIL import Image

SP = os.environ.get('SP', '/tmp/scratch')
OUT = SP + '/casa'
PUB = OUT + '/public'
QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
WWW = os.path.join(APP, 'aula', 'www')
WORKER = 'corsonautico-ondaportante'
WORKER_PROVA = 'corso-nautico-prova'                                          # sito delle prove, senza Cloudflare Access
PROVA_URL = 'https://corso-nautico-prova.fafiorucci.workers.dev/'
PROVA_LEZIONI, PROVA_SLIDE = ('L01', 'L02'), 3                               # come in worker.js
DOCENTE = 'fafiorucci@gmail.com'
TEAM = 'ondaportante'                                                         # <team>.cloudflareaccess.com
AUD = '492a093cc98e6ec93175617027cc6a35752c59b076b7ed02430ebff84ade1c01'      # applicazione Access del sito
# email delle segnalazioni di accessi sospetti: il mittente deve essere su un dominio attivato in Cloudflare Email Service
# (Email Routing) e DOCENTE un indirizzo verificato. Vuoto = niente email, le segnalazioni restano nell'area istruttore.
EMAIL_DA = ''

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(PUB)

# contenuti dal pacchetto dell'aula
for d in ('slides', 'appendici', 'fonts', 'vendor', 'presentazioni'):
    shutil.copytree(os.path.join(WWW, d), os.path.join(PUB, d))
for f in ('stile.css', 'grafica.js'):
    shutil.copy(os.path.join(WWW, f), os.path.join(PUB, f))
shutil.copy(os.path.join(APP, 'stemma.webp'), PUB + '/stemma.webp')
C = json.load(open(os.path.join(WWW, 'corso.json'), encoding='utf-8'))
C = {'casa': True, 'online': True, 'accesso': 'accesso.json', **C}
json.dump(C, open(PUB + '/corso.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# icone dallo stemma
stemma = Image.open(os.path.join(APP, 'stemma-originale.png')).convert('RGBA')
for n in (192, 512):
    stemma.resize((n, n), Image.LANCZOS).save(f'{PUB}/icona-{n}.png', optimize=True)
json.dump({'name': 'Corso Patente Nautica', 'short_name': 'Corso nautico', 'start_url': './', 'scope': './',
           'display': 'standalone', 'background_color': '#16324F', 'theme_color': '#16324F', 'lang': 'it',
           'icons': [{'src': 'icona-192.png', 'sizes': '192x192', 'type': 'image/png'},
                     {'src': 'icona-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'}]},
          open(PUB + '/manifest.webmanifest', 'w'), ensure_ascii=False, indent=1)

# app degli allievi: caratteri in locale (anche senza rete), manifest; il service worker lo registra l'app
h = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
versione = re.search(r"const VERSIONE='([^']+)'", h).group(1)
h = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', h)
h = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '<link rel="stylesheet" href="fonts/fonts.css">', h)
assert 'fonts.googleapis' not in h
h = ('<!doctype html>\n<html lang="it">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
     '<meta name="theme-color" content="#16324F">\n<link rel="manifest" href="manifest.webmanifest">\n'
     '<link rel="apple-touch-icon" href="icona-192.png">\n<meta name="apple-mobile-web-app-capable" content="yes">\n' + h)
open(PUB + '/index.html', 'w', encoding='utf-8').write(h)

# area istruttore: si entra con l'email dell'istruttore (lo controlla il Worker), niente PIN né codici personali
d = open(os.path.join(WWW, 'docente.html'), encoding='utf-8').read()
for vecchio, nuovo in (
        ("const PIN_KEY='corso-aula-pin';", "const PIN_KEY='corso-aula-pin';\ntry{ sessionStorage.setItem(PIN_KEY,'online'); }catch(e){}   // online entra l'email dell'istruttore"),
        ("'Gli allievi, sul wifi della scuola, inquadrano il QR o aprono:'", "'Gli allievi inquadrano il QR o aprono:'"),
        ("'Collegatevi al wifi della scuola, inquadrate il QR, scrivete nome e un codice di 4 cifre.'",
         "'Inquadrate il QR ed entrate con la vostra email: vi arriva un codice.'"),
        ("vPin(e.status===403?'PIN errato.':'Server non raggiungibile.')",
         "vPin(e.status===403?'Area riservata all’istruttore.':'Non riesco a collegarmi: controlla la connessione.')")):
    assert vecchio in d, vecchio
    d = d.replace(vecchio, nuovo, 1)
for vecchio, nuovo in (
        ('<span>QR aula</span>', '<span>QR</span>'),
        ('dargli un codice nuovo se l’ha dimenticato o azzerare', 'o azzerare'),
        ('«Nuovo codice personale» se l’ha dimenticato; ', ''),
        ('Si aprono solo da questo computer, non dai telefoni degli allievi.', 'Si aprono solo con l’email dell’istruttore, non dai telefoni degli allievi.')):
    assert vecchio in d, vecchio
    d = d.replace(vecchio, nuovo)
d, n = re.subn(r'const GUIDA=\[.*?\n\];', '''const GUIDA=[
  ['Come entrano gli allievi',['Aprono l’indirizzo del corso (QR o link) ed entrano con la loro email: arriva un codice da inserire. La prima volta scrivono il nome.','Le email ammesse si gestiscono in Cloudflare Zero Trust → Access → Applications → policy «Allievi».','Per togliere un allievo: togli la sua email dalla policy e revoca la sessione (Zero Trust → Users).']],
  ['Senza rete',['L’app funziona anche senza rete fino a 7 giorni: le risposte si salvano sul telefono e arrivano qui appena torna la connessione.']],
  ['Account di prova per altre scuole',['Scheda «Prove»: scrivi l’email e i giorni (5 di base) e crea l’account; poi aggiungi la stessa email alla policy «Allievi» su Cloudflare.','Chi prova vede l’app con le lezioni 1 e 2 e un’area istruttore con allievi inventati, mai i tuoi allievi. Alla scadenza non si apre più niente; «5 giorni da oggi» la prolunga, «Togli» la cancella.']],
  ['I dati',['Allievi e progressi sono salvati online sul servizio Cloudflare del corso. «Scarica il riepilogo (CSV)» ne fa una copia da aprire con Excel.']],
];''', d, count=1, flags=re.S)
assert n == 1
d, n = re.subn(r"el\('button',\{class:'btn sea',onclick:async\(\)=>\{try\{const j=await api\('docente/codice'.*?'Nuovo codice personale'\),\s*", '', d, flags=re.S)
assert n == 1
open(PUB + '/docente.html', 'w', encoding='utf-8').write(d)

# controllo dell'accesso: senza la sessione di Cloudflare Access la richiesta viene rimandata al login
json.dump({'ok': True}, open(PUB + '/accesso.json', 'w'))
os.makedirs(PUB + '/entra')
open(PUB + '/entra/index.html', 'w', encoding='utf-8').write(
    '<!doctype html>\n<html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    '<title>Corso Patente Nautica</title><body style="font-family:Arial,sans-serif;background:#16324F;color:#FFF8EE;padding:24px">'
    '<p>Accesso riuscito, apro il corso…</p><script>location.replace(\'../\')</script></body></html>\n')
open(PUB + '/_headers', 'w').write('/accesso.json\n  Cache-Control: no-store\n/sw.js\n  Cache-Control: no-cache\n'
                                   '/entra/*\n  Cache-Control: no-store\n/index.html\n  Cache-Control: no-cache\n')

# service worker: al primo avvio conserva app e caratteri; slide e appendici delle lezioni aperte le scarica l'app
file = sorted(os.path.relpath(os.path.join(r, f), PUB).replace(os.sep, '/') for r, _, fs in os.walk(PUB) for f in fs)
nucleo = [f for f in file if f in ('corso.json', 'manifest.webmanifest', 'icona-192.png', 'icona-512.png', 'stemma.webp')
          or f.startswith('fonts/')]
sw = open(os.path.join(QUI, 'sw.js'), encoding='utf-8').read()
sw = sw.replace('__VERSIONE__', versione).replace('__FILE__', json.dumps(['./'] + nucleo))
open(PUB + '/sw.js', 'w', encoding='utf-8').write(sw)

# server
os.makedirs(OUT + '/src')
open(OUT + '/src/worker.js', 'w', encoding='utf-8').write(
    open(os.path.join(QUI, 'worker.js'), encoding='utf-8').read().replace('__VERSIONE__', versione))
VAR_EMAIL = f', "EMAIL_DA": "{EMAIL_DA}"' if EMAIL_DA else ''
CON_EMAIL = f',\n  "send_email": [{{ "name": "EMAIL", "destination_address": "{DOCENTE}" }}]' if EMAIL_DA else ''
open(OUT + '/wrangler.jsonc', 'w', encoding='utf-8').write(f'''// Generato da corso/app/casa/prepara_casa.py: non modificare a mano.
{{
  "name": "{WORKER}",
  "main": "src/worker.js",
  "compatibility_date": "2025-09-01",
  "workers_dev": true,
  "preview_urls": false,
  "assets": {{
    "directory": "./public",
    "binding": "ASSETS",
    "run_worker_first": ["/api/*", "/accesso.json", "/corso.json", "/docente", "/docente/", "/docente.html", "/slides/*", "/appendici/*", "/presentazioni/*"]
  }},
  "durable_objects": {{ "bindings": [{{ "name": "CORSO", "class_name": "Corso" }}] }},
  "migrations": [{{ "tag": "v1", "new_sqlite_classes": ["Corso"] }}],
  "vars": {{ "DOCENTE": "{DOCENTE}", "TEAM": "{TEAM}", "AUD": "{AUD}", "PROVA_URL": "{PROVA_URL}"{VAR_EMAIL} }}{CON_EMAIL}
}}
''')

# sito delle prove: solo i file che servono alla prova (le prime slide delle lezioni 1 e 2, «Rotta verso la patente»);
# stesso server in MODO «prova», che usa l'archivio del sito del corso
PROVA = OUT + '/public-prova'
shutil.copytree(PUB, PROVA, ignore=shutil.ignore_patterns('slides', 'appendici', 'presentazioni'))
os.makedirs(PROVA + '/slides'); os.makedirs(PROVA + '/presentazioni')
for L in C['lezioni']:
    if L['id'] in PROVA_LEZIONI:
        for n in [x for c in L['capitoli'] for x in c['pagine']][:PROVA_SLIDE]:
            shutil.copy(f"{PUB}/slides/{L['id']}-{n:03d}.jpg", PROVA + '/slides/')
shutil.copy(PUB + '/presentazioni/rotta.html', PROVA + '/presentazioni/')
elenco = [x for x in json.load(open(PUB + '/presentazioni/elenco.json', encoding='utf-8')) if x['file'] == 'presentazioni/rotta.html']
json.dump(elenco, open(PROVA + '/presentazioni/elenco.json', 'w'), ensure_ascii=False, indent=1)
open(OUT + '/wrangler.prova.jsonc', 'w', encoding='utf-8').write(f'''// Generato da corso/app/casa/prepara_casa.py: non modificare a mano.
// Sito delle prove per altre scuole: senza Cloudflare Access, si entra con il link creato nell'area istruttore.
{{
  "name": "{WORKER_PROVA}",
  "main": "src/worker.js",
  "compatibility_date": "2025-09-01",
  "workers_dev": true,
  "preview_urls": false,
  "assets": {{ "directory": "./public-prova", "binding": "ASSETS", "run_worker_first": true }},
  "durable_objects": {{ "bindings": [{{ "name": "CORSO", "class_name": "Corso", "script_name": "{WORKER}" }}] }},
  "vars": {{ "MODO": "prova" }}
}}
''')
open(OUT + '/.gitignore', 'w').write('.wrangler/\nnode_modules/\n')   # file della prova in locale (wrangler dev)
tot = sum(os.path.getsize(os.path.join(PUB, f)) for f in file)
print(OUT, len(file), 'file,', tot // 1024, 'KB; nel service worker', len(nucleo) + 1, 'file; versione', versione)
