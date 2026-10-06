#!/usr/bin/env python3
"""Prepara la demo dell'app, da far vedere ad altre scuole: solo contenuti di esempio.

  SP=<cartella di lavoro> python3 corso/app/demo/prepara_demo.py

Parte dall'uscita completa di app_build.py ($SP/app) e scrive $SP/demo/:
- index.html     l'app degli allievi (riconosce la demo da «demo» in corso.json; progressi solo sul dispositivo);
- corso.json     le 15 lezioni con i titoli; aperta solo la lezione 1, con introduzione e capitolo 1;
                 appendici C ed E di esempio, scheda della lezione 1 e numeri d'oro;
- docente.html   l'area istruttore con allievi inventati (demo-dati.js al posto del server);
- presentazioni/ due presentazioni da proiettare di esempio.
"""
import json, os, re, shutil

SP = os.environ.get('SP', '/tmp/scratch')
SRC, OUT = SP + '/app', SP + '/demo'
QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
AULA = os.path.join(APP, 'aula')
HTML = os.path.join(os.path.dirname(APP), 'export', 'html')
APPENDICI_DEMO = ['C', 'E']
CAPITOLI_DEMO = 2          # Introduzione + Capitolo 1
FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
        '&family=Nunito+Sans:wght@400;600;700;800;900&family=Caveat:wght@700&display=swap">')

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/slides'); os.makedirs(OUT + '/appendici'); os.makedirs(OUT + '/presentazioni'); os.makedirs(OUT + '/vendor')

C = json.load(open(SRC + '/corso.json'))
demo = {'demo': True, 'lezioni': [], 'appendici': [], 'schede': C['schede'], 'quiz': {}}
immagini = set()
for L in C['lezioni']:
    if L['id'] == 'L01':
        caps = L['capitoli'][:CAPITOLI_DEMO]
        resto = L['capitoli'][CAPITOLI_DEMO:]
        nq = sum(len(s['ids']) for c in resto for s in c['quiz'])
        demo['lezioni'].append({**L, 'attiva': True, 'capitoli': caps, 'appendici': APPENDICI_DEMO,
                                'nota_demo': f'Nella versione completa la lezione continua con altri {len(resto)} capitoli e {nq} quiz ufficiali.'})
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
    demo['appendici'].append({**a, 'aperta': a['id'] in APPENDICI_DEMO})
    if a['id'] in APPENDICI_DEMO:
        shutil.copy(f"{SRC}/{a['file']}", f"{OUT}/{a['file']}")
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
shutil.copy(os.path.join(QUI, 'demo-dati.js'), OUT + '/demo-dati.js')
d = open(os.path.join(AULA, 'docente.html'), encoding='utf-8').read()
d = d.replace('<link rel="stylesheet" href="fonts/fonts.css">', FONT, 1)
d = d.replace('<title>Area istruttore</title>', '<title>Area istruttore demo</title>', 1)
d = d.replace('<script src="vendor/qrcode.js"></script>', '<script src="vendor/qrcode.js"></script>\n<script src="demo-dati.js"></script>', 1)
assert 'demo-dati.js' in d and 'fonts/fonts.css' not in d
open(OUT + '/docente.html', 'w', encoding='utf-8').write(d)

# presentazioni di esempio, con il proiettore
proiettore = open(os.path.join(AULA, 'proiettore.js'), encoding='utf-8').read().replace('href="/docente"', 'href="../docente.html"')
elenco = []
for nome, gruppo, titolo, file in (('Rotta verso la patente - Il corso in sintesi', 'Il corso', 'Rotta verso la patente · il corso in sintesi', 'rotta'),
                                   ('Appendice C - I nodi marinari', 'Appendici', 'Appendice C · I nodi marinari', 'appendice-c')):
    p = open(os.path.join(HTML, nome + '.html'), encoding='utf-8').read()
    p = p.replace('</body>', '<script>' + proiettore + '</script></body>', 1)
    open(f'{OUT}/presentazioni/{file}.html', 'w', encoding='utf-8').write(p)
    elenco.append({'gruppo': gruppo, 'titolo': titolo, 'file': f'presentazioni/{file}.html', 'slide': p.count('<div class="w"')})
json.dump(elenco, open(OUT + '/presentazioni/elenco.json', 'w'), ensure_ascii=False, indent=1)

n = sum(len(fs) for _, _, fs in os.walk(OUT))
kb = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs) // 1024
print(OUT, n, 'file,', kb, 'KB;', len(immagini), 'immagini,', len(demo['quiz']), 'quiz')
