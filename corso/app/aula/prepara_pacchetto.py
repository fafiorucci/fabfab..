#!/usr/bin/env python3
"""Prepara la cartella www/ del server d'aula e lo zip da scaricare.

  python3 corso/app/aula/prepara_pacchetto.py [--app <cartella con corso.json e slides/>]

- www/index.html  = corso/app/index.html con i caratteri in locale (funziona anche senza internet);
- www/stile.css, www/grafica.js = stile e disegni dell'app, riusati dall'area istruttore;
- corso.json e slides/ si prendono da --app (uscita di app_build.py) o restano quelli già in www/;
- con --python include Python portatile per Windows (python-3.12.x-embed-amd64.zip da python.org);
- lo zip va in corso/export/app/.
"""
import argparse
import json
import os
import re
import shutil
import stat
import zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
WWW = os.path.join(QUI, 'www')
EXPORT = os.path.join(os.path.dirname(APP), 'export', 'app')
NOME = 'Corso patente nautica - app aula'
CARTELLA_ZIP = 'Corso patente nautica - app aula'

ap = argparse.ArgumentParser()
ap.add_argument('--app', help='cartella con corso.json e slides/ prodotti da app_build.py')
ap.add_argument('--python', help='zip «Windows embeddable package (64-bit)» da python.org: va nella cartella python/ '
                'dello zip, così su Windows non serve installare nulla')
args = ap.parse_args()

os.makedirs(WWW, exist_ok=True)
if args.app:
    shutil.copy(os.path.join(args.app, 'corso.json'), os.path.join(WWW, 'corso.json'))
    shutil.rmtree(os.path.join(WWW, 'slides'), ignore_errors=True)
    shutil.copytree(os.path.join(args.app, 'slides'), os.path.join(WWW, 'slides'))
    shutil.rmtree(os.path.join(WWW, 'appendici'), ignore_errors=True)
    shutil.copytree(os.path.join(args.app, 'appendici'), os.path.join(WWW, 'appendici'))
for richiesto in ('corso.json', 'slides', 'appendici', 'fonts/fonts.css', 'vendor/qrcode.js'):
    if not os.path.exists(os.path.join(WWW, richiesto)):
        raise SystemExit(f'manca www/{richiesto}')

src = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()

# pagina degli allievi: documento completo, caratteri locali
pagina = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', src)
pagina = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>',
                '<link rel="stylesheet" href="fonts/fonts.css">', pagina)
assert 'fonts.googleapis' not in pagina
pagina = ('<!doctype html>\n<html lang="it">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + pagina)
open(os.path.join(WWW, 'index.html'), 'w', encoding='utf-8').write(pagina)

# stile e grafica condivisi con l'area istruttore
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
open(os.path.join(WWW, 'stile.css'), 'w', encoding='utf-8').write(css.strip() + '\n')
grafica = re.search(r'(const HUES=.*?)\ndocument\.getElementById\(\'logo-h\'\)', src, re.S).group(1)
el = re.search(r'^const el=.*$', src, re.M).group(0)
head = re.search(r'^function head\(.*?\n}\n', src, re.M | re.S).group(0)
open(os.path.join(WWW, 'grafica.js'), 'w', encoding='utf-8').write(
    '/* Generato da prepara_pacchetto.py a partire da corso/app/index.html */\n'
    + grafica + '\n' + el + '\n' + head)
shutil.copy(os.path.join(QUI, 'docente.html'), os.path.join(WWW, 'docente.html'))
shutil.copy(os.path.join(APP, 'stemma.webp'), os.path.join(WWW, 'stemma.webp'))

# appendici per gli allievi: caratteri locali, così funzionano anche senza internet
for f in os.listdir(os.path.join(WWW, 'appendici')):
    pa = os.path.join(WWW, 'appendici', f)
    h = open(pa, encoding='utf-8').read()
    if 'fonts.googleapis' in h:
        h = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '', h)
        h = h.replace('</head>', '<link rel="stylesheet" href="../fonts/fonts.css"></head>', 1)
        open(pa, 'w', encoding='utf-8').write(h)

# presentazioni da proiettare dall'area istruttore: gli HTML esportati, con caratteri locali e il proiettore
HTML = os.path.join(os.path.dirname(APP), 'export', 'html')
PRES = os.path.join(WWW, 'presentazioni')
shutil.rmtree(PRES, ignore_errors=True)
os.makedirs(PRES)
proiettore = open(os.path.join(QUI, 'proiettore.js'), encoding='utf-8').read()
elenco = []
def gruppo(nome):
    if nome.startswith('Patente nautica'): return ('La scuola', 'Presentazione della scuola', 'scuola')
    if nome.startswith('Rotta verso'): return ('Il corso', 'Rotta verso la patente · il corso in sintesi', 'rotta')
    if nome.startswith('Addendum'): return ('Ripasso', 'Schede riassuntive', 'schede')
    m = re.match(r'Lezione (\d+) - (.*)', nome)
    if m: return ('Lezioni', f'Lezione {m.group(1)} · {m.group(2)}', 'lezione-' + m.group(1))
    m = re.match(r'Appendice ([A-Z]) - (.*)', nome)
    if m: return ('Appendici', f'Appendice {m.group(1)} · {m.group(2)}', 'appendice-' + m.group(1).lower())
    return None
for f in sorted(os.listdir(HTML)):
    g = gruppo(f[:-5]) if f.endswith('.html') else None
    if not g:
        continue
    h = open(os.path.join(HTML, f), encoding='utf-8').read()
    h = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '', h)
    h = h.replace('</head>', '<link rel="stylesheet" href="../fonts/fonts.css"></head>', 1)
    h = h.replace('</body>', '<script>' + proiettore + '</script></body>', 1)
    assert 'fonts.googleapis' not in h
    open(os.path.join(PRES, g[2] + '.html'), 'w', encoding='utf-8').write(h)
    elenco.append({'gruppo': g[0], 'titolo': g[1], 'file': 'presentazioni/' + g[2] + '.html',
                   'slide': h.count('<div class="w"')})
ordine = ['La scuola', 'Il corso', 'Lezioni', 'Ripasso', 'Appendici']
elenco.sort(key=lambda e: (ordine.index(e['gruppo']), e['titolo']))
json.dump(elenco, open(os.path.join(PRES, 'elenco.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# zip per l'istruttore
os.makedirs(EXPORT, exist_ok=True)
destinazione = os.path.join(EXPORT, NOME + '.zip')
eseguibili = {'Avvia (Mac).command', 'avvia-linux.sh', 'server.py'}
with zipfile.ZipFile(destinazione, 'w', zipfile.ZIP_DEFLATED) as z:
    for nome in ('LEGGIMI.txt', 'Avvia (Windows).bat', 'Avvia (Mac).command', 'avvia-linux.sh', 'server.py'):
        info = zipfile.ZipInfo(f'{CARTELLA_ZIP}/{nome}')
        info.compress_type = zipfile.ZIP_DEFLATED
        modo = 0o755 if nome in eseguibili else 0o644
        info.external_attr = (stat.S_IFREG | modo) << 16
        z.writestr(info, open(os.path.join(QUI, nome), 'rb').read())
    if args.python:
        with zipfile.ZipFile(args.python) as py:
            for voce in py.infolist():
                z.writestr(f'{CARTELLA_ZIP}/python/{voce.filename}', py.read(voce), zipfile.ZIP_DEFLATED)
    else:
        print('ATTENZIONE: zip senza Python portatile (--python): su Windows andrà installato Python.')
    for radice, _, files in os.walk(WWW):
        for f in sorted(files):
            pieno = os.path.join(radice, f)
            z.write(pieno, f'{CARTELLA_ZIP}/www/' + os.path.relpath(pieno, WWW).replace(os.sep, '/'))
print(destinazione, os.path.getsize(destinazione) // 1024, 'KB')
