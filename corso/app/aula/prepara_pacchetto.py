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
for richiesto in ('corso.json', 'slides', 'fonts/fonts.css', 'vendor/qrcode.js'):
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
