#!/usr/bin/env python3
"""Prepara la demo dell'app, da far vedere ad altre scuole: solo contenuti di esempio.

  SP=<cartella di lavoro> python3 corso/app/demo/prepara_demo.py

Parte dall'uscita completa di app_build.py ($SP/app) e scrive $SP/demo/:
- index.html     l'app degli allievi (riconosce la demo da «demo» in corso.json; progressi solo sul dispositivo);
- corso.json     le 15 lezioni con i titoli; aperta solo la lezione 1, con introduzione e capitolo 1;
                 appendici C ed E di esempio, scheda della lezione 1 e numeri d'oro;
- docente.html   l'area istruttore con allievi inventati (demo-dati.js al posto del server);
- presentazioni/ due presentazioni da proiettare di esempio.
Poi lo zip da aprire senza server (corso/export/app/Corso patente nautica - demo.zip): stessi file, con i dati
(corso.json, elenco delle presentazioni) dentro dati-locali.js e i caratteri in locale, così index.html si apre
con un doppio clic anche senza internet.
"""
import json, os, re, shutil, zipfile

SP = os.environ.get('SP', '/tmp/scratch')
SRC, OUT = SP + '/app', SP + '/demo'
QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
AULA = os.path.join(APP, 'aula')
HTML = os.path.join(os.path.dirname(APP), 'export', 'html')
APPENDICI_DEMO = ['C', 'E']
SLIDE_DEMO = 4             # appendici e presentazioni: solo le prime slide


def taglia(h, titolo):
    """Tiene le prime SLIDE_DEMO slide di un HTML esportato (il resto non viene pubblicato), toglie le note
    per l'istruttore e chiude con una slide «Nella versione completa»."""
    inizi = [m.start() for m in re.finditer(r'<div class="w"', h)]
    fine = h.index('<script>function fit()')
    tot = len(inizi)
    if tot > SLIDE_DEMO:
        ultima = ('<div class="w" id="s-demo"><div class="f"><section class="s" style="position:absolute;inset:0;display:flex;'
                  'flex-direction:column;align-items:center;justify-content:center;gap:40px;background:#16324F;color:#FFF8EE;'
                  'font-family:Fredoka,\'Trebuchet MS\',sans-serif;text-align:center">'
                  f'<p style="font-size:44px;color:#FFC145;font-weight:600">{titolo}</p>'
                  '<p style="font-size:92px;font-weight:700;line-height:1.1">Nella versione completa</p>'
                  f'<p style="font-size:48px;font-family:\'Nunito Sans\',Arial,sans-serif;font-weight:700">altre {tot - SLIDE_DEMO} slide</p>'
                  '</section></div></div>\n')
        h = h[:inizi[SLIDE_DEMO]] + ultima + h[fine:]
    h = re.sub(r'<details class="nt">.*?</details>', '', h, flags=re.S)
    return h, min(tot, SLIDE_DEMO), tot

CAPITOLI_DEMO = 2          # Introduzione + Capitolo 1
PAGINE_CAPITOLO_DEMO = 3   # del capitolo 1: le prime slide, più quella a cui rimanda la verifica
FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
        '&family=Nunito+Sans:wght@400;600;700;800;900&family=Caveat:wght@700&display=swap">')

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/slides'); os.makedirs(OUT + '/appendici'); os.makedirs(OUT + '/presentazioni'); os.makedirs(OUT + '/vendor')

C = json.load(open(SRC + '/corso.json'))
demo = {'demo': True, 'lezioni': [], 'appendici': [], 'schede': C['schede'], 'quiz': {}}
immagini = set()
for L in C['lezioni']:
    if L['id'] == 'L01':
        caps = [dict(c) for c in L['capitoli'][:CAPITOLI_DEMO]]
        resto = L['capitoli'][CAPITOLI_DEMO:]
        nq = sum(len(s['ids']) for c in resto for s in c['quiz'])
        rimandi = {C['quiz'][q]['rivedi'][1] for c in caps for s in c['quiz'] for q in s['ids']}
        for c in caps[1:]:
            c['pagine'] = sorted(set(c['pagine'][:PAGINE_CAPITOLO_DEMO]) | (rimandi & set(c['pagine'])))
        tutte = sum(len(c['pagine']) for c in L['capitoli'])
        mostrate = sum(len(c['pagine']) for c in caps)
        demo['lezioni'].append({**L, 'attiva': True, 'capitoli': caps, 'appendici': APPENDICI_DEMO,
                                'nota_demo': f'Demo: {mostrate} slide di esempio. Nella versione completa la lezione ha {tutte} slide, '
                                             f'altri {len(resto)} capitoli e {nq} quiz ufficiali.'})
        for c in caps:
            immagini |= {f'L01-{p:03d}.jpg' for p in c['pagine']}
            for s in c['quiz']:
                for q in s['ids']:
                    demo['quiz'][q] = C['quiz'][q]
        immagini |= {f'SR-{p:03d}.jpg' for p in L['scheda']}
    else:
        demo['lezioni'].append({**L, 'attiva': False, 'capitoli': [], 'appendici': []})
for q in C['schede']['numeri_oro']:
    demo['quiz'][q] = {**C['quiz'][q], 'rivedi': ['SR', C['schede']['generali'][-1]]}
immagini |= {f'SR-{p:03d}.jpg' for p in C['schede']['generali']}
for a in C['appendici']:
    voce = {**a, 'aperta': a['id'] in APPENDICI_DEMO}
    voce.pop('pagine', None)   # nella demo le appendici sono le presentazioni HTML ridotte
    if a['id'] in APPENDICI_DEMO:
        h, n, tot = taglia(open(f"{SRC}/{a['file']}", encoding='utf-8').read(), f"Appendice {a['id']} · {a['titolo']}")
        open(f"{OUT}/{a['file']}", 'w', encoding='utf-8').write(h)
        voce['slide'] = n
    demo['appendici'].append(voce)
for f in sorted(immagini):
    shutil.copy(f'{SRC}/slides/{f}', f'{OUT}/slides/{f}')
json.dump(demo, open(OUT + '/corso.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# app degli allievi
h = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
h = h.replace('<title>Corso Patente Nautica</title>', '<title>Corso Nautico Demo</title>', 1)
open(OUT + '/index.html', 'w', encoding='utf-8').write(h)
shutil.copy(os.path.join(APP, 'stemma.webp'), OUT + '/stemma.webp')

# area istruttore di esempio
www = os.path.join(AULA, 'www')
for f in ('stile.css', 'grafica.js'):
    shutil.copy(os.path.join(www, f), os.path.join(OUT, f))
shutil.copy(os.path.join(www, 'vendor', 'qrcode.js'), OUT + '/vendor/qrcode.js')
versione = re.search(r"const VERSIONE='([^']+)'", h).group(1)   # la stessa dell'app
open(OUT + '/demo-dati.js', 'w', encoding='utf-8').write(
    open(os.path.join(QUI, 'demo-dati.js'), encoding='utf-8').read().replace('__VERSIONE__', versione))
d = open(os.path.join(AULA, 'docente.html'), encoding='utf-8').read()
d = d.replace('<link rel="stylesheet" href="fonts/fonts.css">', FONT, 1)
d = d.replace('<title>Area istruttore</title>', '<title>Area istruttore demo</title>', 1)
d = d.replace('<script src="vendor/qrcode.js"></script>', '<script src="vendor/qrcode.js"></script>\n<script src="demo-dati.js"></script>', 1)
d = d.replace("'Gli allievi, sul wifi della scuola, inquadrano il QR o aprono:'", "'Gli allievi, sul wifi della scuola, inquadrano il QR con il telefono.'", 1)
assert 'demo-dati.js' in d and 'fonts/fonts.css' not in d
open(OUT + '/docente.html', 'w', encoding='utf-8').write(d)

# presentazioni di esempio, con il proiettore
# nella demo le presentazioni si sfogliano dentro la pagina: niente link «← Elenco» né avvio a schermo intero
proiettore = open(os.path.join(AULA, 'proiettore.js'), encoding='utf-8').read()
proiettore = proiettore.replace("(allievo ? '<a href=\"../\" title=\"Torna al corso\">← Corso</a>' : '<a href=\"/docente\" title=\"Torna all’area istruttore\">← Elenco</a>')", "''")
proiettore = proiettore.replace("if (!allievo) document.body.append(start);", "")
assert '/docente' not in proiettore and 'document.body.append(start)' not in proiettore
elenco = []
for nome, gruppo, titolo, file in (('Rotta verso la patente - Il corso in sintesi', 'Il corso', 'Rotta verso la patente · il corso in sintesi', 'rotta'),
                                   ('Appendice C - I nodi marinari', 'Appendici', 'Appendice C · I nodi marinari', 'appendice-c')):
    p, n, tot = taglia(open(os.path.join(HTML, nome + '.html'), encoding='utf-8').read(), titolo)
    p = p.replace('</body>', '<script>' + proiettore + '</script></body>', 1)
    open(f'{OUT}/presentazioni/{file}.html', 'w', encoding='utf-8').write(p)
    elenco.append({'gruppo': gruppo, 'titolo': titolo, 'file': f'presentazioni/{file}.html', 'slide': n})
json.dump(elenco, open(OUT + '/presentazioni/elenco.json', 'w'), ensure_ascii=False, indent=1)

n = sum(len(fs) for _, _, fs in os.walk(OUT))
kb = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs) // 1024
print(OUT, n, 'file,', kb, 'KB;', len(immagini), 'immagini,', len(demo['quiz']), 'quiz')

# ---------- zip da aprire con un doppio clic su index.html (senza server, anche senza internet) ----------
# Aperta dal disco (file://) la pagina non può leggere i file con fetch: corso.json e l'elenco delle presentazioni
# vanno in dati-locali.js, caricato per primo, che risponde al loro posto. Caratteri dal pacchetto dell'aula.
EXPORT_APP = os.path.join(os.path.dirname(APP), 'export', 'app')
ZIP = os.path.join(EXPORT_APP, 'Corso patente nautica - demo.zip')
CARTELLA = 'Corso patente nautica - demo'
locali = {'corso.json': json.load(open(OUT + '/corso.json')), 'presentazioni/elenco.json': elenco}
dati_locali = ('/* Demo aperta dal disco: i dati che la pagina chiederebbe al server, già qui dentro. */\n(function(){\n'
               'const F=' + json.dumps(locali, ensure_ascii=False, separators=(',', ':')) + ';\n'
               'const orig=window.fetch?window.fetch.bind(window):null;\n'
               'window.fetch=function(url,opt){ const u=String(url&&url.url||url).split(/[?#]/)[0];\n'
               '  for(const k in F) if(u===k||u.endsWith(\'/\'+k)) return Promise.resolve(new Response(JSON.stringify(F[k]),{status:200,headers:{\'Content-Type\':\'application/json\'}}));\n'
               '  if(/^(\\.\\/)?api\\//.test(u)) return Promise.reject(new TypeError(\'demo senza server\'));\n'
               '  return orig?orig(url,opt):Promise.reject(new TypeError(\'fetch\')); };\n})();\n')
LEGGIMI = '''CORSO PATENTE NAUTICA · DEMO

Per aprire la demo: fai doppio clic su index.html (si apre nel browser: Chrome, Edge, Firefox o Safari).
Non serve internet e non serve installare niente.

- index.html     l'app degli allievi: ti registri con un nome qualsiasi e provi lezione 1, quiz, scheda e appendici.
                 I progressi restano solo su questo computer, nel browser.
- docente.html   l'area istruttore di esempio, con allievi inventati (si apre anche dall'app).

Tieni insieme tutti i file della cartella: se sposti index.html da sola, la demo non trova slide e dati.
Fabrizio Fiorucci · Patente nautica Vela/Motore entro le 12 miglia e senza limiti dalla costa
'''
FONT_LOCALE = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*|<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>')


def per_il_disco(nome, testo):
    # caratteri locali; i link «../» e «./» del web portano alla pagina, che dal disco va scritta per esteso
    if nome.endswith('.html'):
        su = '../' if '/' in nome else ''
        if 'fonts.googleapis' in testo:
            testo = FONT_LOCALE.sub('', testo)
            testo = testo.replace('</head>', f'<link rel="stylesheet" href="{su}fonts/fonts.css"></head>', 1) if '</head>' in testo \
                else testo.replace('<style>', f'<link rel="stylesheet" href="{su}fonts/fonts.css">\n<style>', 1)
            assert 'fonts.googleapis' not in testo and 'fonts/fonts.css' in testo, nome
        testo = testo.replace('href=\\"../\\"', 'href=\\"../index.html\\"').replace('href="../"', 'href="../index.html"')
    if nome == 'index.html':
        testo = testo.replace('<script>', '<script src="dati-locali.js"></script>\n<script>', 1)
    if nome == 'docente.html':
        testo = testo.replace('<script src="vendor/qrcode.js"></script>', '<script src="dati-locali.js"></script>\n<script src="vendor/qrcode.js"></script>', 1)
        assert testo.index('dati-locali.js') < testo.index('demo-dati.js')
    if nome == 'demo-dati.js':
        testo = testo.replace('<a href="./"', '<a href="index.html"')
    return testo


os.makedirs(EXPORT_APP, exist_ok=True)
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for r, _, fs in os.walk(OUT):
        for f in sorted(fs):
            pieno = os.path.join(r, f); nome = os.path.relpath(pieno, OUT).replace(os.sep, '/')
            if nome in locali: continue
            if nome.endswith(('.html', '.js')):
                z.writestr(f'{CARTELLA}/{nome}', per_il_disco(nome, open(pieno, encoding='utf-8').read()))
            else:
                z.write(pieno, f'{CARTELLA}/{nome}')
    z.writestr(f'{CARTELLA}/dati-locali.js', dati_locali)
    z.writestr(f'{CARTELLA}/LEGGIMI.txt', LEGGIMI)
    fonts = os.path.join(www, 'fonts')
    for f in sorted(os.listdir(fonts)):
        z.write(os.path.join(fonts, f), f'{CARTELLA}/fonts/{f}')
    nomi = z.namelist()
assert not any('fonts.googleapis' in z.open(n).read().decode('utf-8', 'ignore') for z in [zipfile.ZipFile(ZIP)] for n in nomi if n.endswith('.html'))
print(ZIP, len(nomi), 'file,', os.path.getsize(ZIP) // 1024, 'KB')
