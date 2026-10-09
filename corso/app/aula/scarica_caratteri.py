#!/usr/bin/env python3
"""Scarica da Google Fonts i caratteri dell'app per l'uso senza internet: aula/www/fonts/ (fonts.css + woff2).

  python3 corso/app/aula/scarica_caratteri.py

Fredoka e Nunito Sans sono caratteri a peso variabile: un file per alfabeto copre tutti i pesi (la versione di prima
aveva Nunito Sans solo extra-grassetto, e in aula tutto il testo usciva in grassetto). Si tengono gli alfabeti latin e
latin-ext. Poi si rifanno il pacchetto (prepara_pacchetto.py), l'app online e la demo, che prendono i caratteri da qui.
"""
import os, re, urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(QUI, 'www', 'fonts')
URL = ('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
       '&family=Nunito+Sans:wght@400;600;700;800;900&family=Caveat:wght@700&display=swap')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
ALFABETI = ('latin-ext', 'latin')


def scarica(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30).read()


css = scarica(URL).decode()
facce = {}   # (famiglia, alfabeto) -> pesi, url, unicode-range
for alfabeto, blocco in re.findall(r'/\* ([\w-]+) \*/\s*@font-face\s*{([^}]*)}', css):
    if alfabeto not in ALFABETI:
        continue
    fam = re.search(r"font-family: '([^']+)'", blocco).group(1)
    peso = int(re.search(r'font-weight: (\d+)', blocco).group(1))
    url = re.search(r'url\(([^)]+)\)', blocco).group(1)
    rng = re.search(r'unicode-range: ([^;]+);', blocco).group(1)
    f = facce.setdefault((fam, alfabeto), {'pesi': [], 'url': url, 'rng': rng})
    assert f['url'] == url, f'{fam} {alfabeto}: un file per peso, non variabile'
    f['pesi'].append(peso)

os.makedirs(FONTS, exist_ok=True)
for f in os.listdir(FONTS):
    os.remove(os.path.join(FONTS, f))
righe = []
for (fam, alfabeto), f in facce.items():
    nome = f"{fam.replace(' ', '')}-{alfabeto}.woff2"
    open(os.path.join(FONTS, nome), 'wb').write(scarica(f['url']))
    pesi = f"{min(f['pesi'])} {max(f['pesi'])}" if len(f['pesi']) > 1 else str(f['pesi'][0])
    righe.append(f"@font-face {{\n  font-family: '{fam}';\n  font-style: normal;\n  font-weight: {pesi};\n"
                 f"  font-display: swap;\n  src: url({nome}) format('woff2');\n  unicode-range: {f['rng']};\n}}")
open(os.path.join(FONTS, 'fonts.css'), 'w', encoding='utf-8').write('\n'.join(righe) + '\n')
print(FONTS, len(facce), 'file:', ', '.join(f'{k[0]} {k[1]} {v["pesi"]}' for k, v in facce.items()))
