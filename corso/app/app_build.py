"""Genera i contenuti dell'app del corso dai PDF esportati.

  SP=<cartella di lavoro con rotta-giusta/> python3 corso/app/app_build.py

Scrive in $SP/app/:
- corso.json   lezioni (capitoli, quiz, scheda riassuntiva, appendici collegate), appendici, quiz con le
               risposte e la slide da rivedere;
- slides/      le pagine di teoria delle 15 lezioni (LNN-NNN.jpg) e delle schede riassuntive (SR-NNN.jpg),
               con la filigrana;
- appendici/   le appendici A-M in HTML, con il visore per gli allievi; le loro pagine anche come immagini
               (slides/AX-NNN.jpg), che l'app mostra nel suo visore come le lezioni.
Le lezioni attive all'inizio sono in ATTIVE; poi le abilita l'istruttore (server d'aula) o una nuova
pubblicazione (app online).
"""
import pymupdf, json, re, math, io, collections, os, glob
from PIL import Image

SP = os.environ.get('SP', '/tmp/scratch')  # cartella di lavoro con rotta-giusta/
OUT = SP + '/app'
QUI = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(os.path.dirname(QUI), 'export')
PDF = os.path.join(EXPORT, 'pdf')
ATTIVE = ['L01', 'L02']

# Appendici e lezioni in cui servono (per argomento): l'appendice si apre con la prima lezione attiva
APPENDICI = {
    'A': ['L13', 'L14'], 'B': ['L09'], 'C': ['L03'], 'D': ['L08', 'L15'], 'E': ['L02', 'L03'],
    'F': ['L03'], 'G': ['L07'], 'H': ['L06'], 'I': ['L04'], 'J': ['L07'], 'K': ['L06'],
    'L': ['L03'], 'M': ['L09'],
}

Q = {q['p']: q for q in json.load(open(SP + '/rotta-giusta/site/dati/quiz.json')) if q.get('p')}
STOP = set('della delle dello degli nella nelle sono essere viene vengono quale quali come cosa ogni anche solo dove quando sulla sulle questo questa questi tutte tutti molto dalla dalle alla alle allo agli unità ecc oppure mentre perché però hanno avere'.split())

# Filigrana come nei PDF protetti (corso/export/strumenti/proteggi.py): diagonale leggera + avviso in basso
FILIGRANA = 'Fabrizio Fiorucci · vietata la duplicazione'
AVVISO = 'La proprietà intellettuale di questo documento è di Fabrizio Fiorucci, ne sono proibite la divulgazione e la duplicazione'


def filigrana(page):
    font = pymupdf.Font('helv'); W, H = page.rect.width, page.rect.height
    size = W / 40; tw = font.text_length(FILIGRANA, fontsize=size); ang = math.degrees(math.atan2(H, W))
    p0 = pymupdf.Point(W / 2, H / 2); sh = page.new_shape()
    sh.insert_text(pymupdf.Point(W / 2 - tw / 2, H / 2 + size / 3), FILIGRANA, fontsize=size, fontname='helv',
                   color=(0.5, 0.55, 0.6), fill_opacity=0.07, morph=(p0, pymupdf.Matrix(-ang)))
    sh.commit(overlay=True)
    fs = W / 120
    page.insert_text((W - font.text_length(AVVISO, fontsize=fs) - W * 0.02, H - H * 0.015), AVVISO,
                     fontsize=fs, fontname='helv', color=(0.37, 0.43, 0.51), fill_opacity=0.8)


def immagine(doc, i, nome):
    filigrana(doc[i])
    zoom = 1280 / doc[i].rect.width
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    im.save(f'{OUT}/slides/{nome}.jpg', 'JPEG', quality=74, optimize=True, progressive=True)


def testo(page):
    return ' '.join(page.get_text().split())


def toks(t):
    return [w[:6] for w in re.findall(r"[a-zàèéìòù]{4,}", t.lower()) if w not in STOP]


def tipo(i, t):
    if i == 0: return 'cover'
    if t.startswith('VERIFICA · RISPOSTE'): return 'answers'
    if t.startswith(('VERIFICA DEL PARAGRAFO', 'VERIFICA DEL CAPITOLO', 'VERIFICA · QUIZ', 'RACCOLTA QUIZ')): return 'quiz'
    if re.match(r"(?:[A-ZÀ-Ú' ]+ · )?CAPITOLO \d+ ", t) or t.startswith('ULTIMI 45 MINUTI'): return 'chapter'
    if t.startswith('IN SINTESI'): return 'closing'
    if re.match(r'LEZIONE \d+ · 2 ORE', t): return 'intro'
    return 'theory'


def domanda(rec):
    return {'d': rec['d'].strip(), 'r': [r.strip().rstrip(';,') for r in rec['r']], 'x': rec['x'],
            'v': rec.get('v', ''), 't': rec.get('t', '')}


os.makedirs(OUT + '/slides', exist_ok=True)
for f in glob.glob(OUT + '/slides/*.jpg'):
    os.remove(f)
corso = {'lezioni': [], 'appendici': [], 'schede': {}, 'quiz': {}}

# ---------- schede riassuntive: «SCHEDA NN» va con la lezione NN ----------
sr = pymupdf.open(os.path.join(PDF, 'Addendum - Schede riassuntive.pdf'))
schede = collections.defaultdict(list)
generali, numeri_oro = [], []
for i in range(sr.page_count):
    t = testo(sr[i])
    m = re.match(r'SCHEDA (\d+)', t)
    if m:
        schede['L' + m.group(1)].append(i + 1)
    elif t.startswith('ADDENDUM · SCHEDE RIASSUNTIVE'):
        generali.append(i + 1)          # «Come usare le schede» e «I numeri d'oro del corso»
    elif t.startswith('VERIFICA · QUIZ'):
        numeri_oro += re.findall(r'quiz (\d+\.\d+\.\d+-\d+)', t)
for p in sorted(set(p for v in schede.values() for p in v) | set(generali)):
    immagine(sr, p - 1, f'SR-{p:03d}')
corso['schede'] = {'generali': generali, 'numeri_oro': numeri_oro}

# ---------- lezioni ----------
for pdf in sorted(glob.glob(os.path.join(PDF, 'Lezione *.pdf'))):
    m = re.match(r'Lezione (\d+) - (.*)\.pdf', os.path.basename(pdf))
    code, num, titolo = 'L' + m.group(1), 'Lezione ' + m.group(1), m.group(2)
    d = pymupdf.open(pdf)
    pages = [(i, tipo(i, testo(d[i])), testo(d[i])) for i in range(d.page_count)]
    caps = [{'titolo': 'Introduzione', 'pagine': [], 'quiz': []}]
    for i, k, t in pages:
        if k == 'chapter':
            mc = re.match(r"(?:[A-ZÀ-Ú' ]+ · )?CAPITOLO (\d+) (.*?) circa", t)
            caps.append({'titolo': f'Capitolo {mc.group(1)} · {mc.group(2)}' if mc else 'Raccolta quiz · ultimi 45 minuti',
                         'pagine': [i], 'quiz': []})
        elif k in ('cover', 'theory', 'closing', 'intro'):
            caps[-1]['pagine'].append(i)
        elif k == 'quiz':
            mt = re.search(r'((?:Quiz \d+|Verifica[^·]*) · .*?) Domanda 1', t)
            ids = re.findall(r'quiz (\d+\.\d+\.\d+-\d+)', t)
            caps[-1]['quiz'].append({'titolo': mt.group(1) if mt else 'Quiz', 'ids': ids, 'raccolta': t.startswith('RACCOLTA')})
    for c in caps:
        for i in c['pagine']:
            immagine(d, i, f'{code}-{i + 1:03d}')
    # slide da rivedere: la pagina di teoria più vicina alla domanda per parole (idf)
    tp = {i: toks(t) for i, k, t in pages if k in ('theory', 'closing')}
    df = collections.Counter(w for v in tp.values() for w in set(v)); N = len(tp)

    def best(qid, cand):
        q = Q[qid]; ws = set(toks(q['d'] + ' ' + q['r'][q['x']]))
        sc = [(sum(math.log(N / df[w]) for w in ws if w in set(tp[i])), i) for i in cand if i in tp]
        sc.sort(reverse=True)
        return sc[0][1] if sc and sc[0][0] > 0 else (cand[0] if cand else None)
    for c in caps:
        for qs in c['quiz']:
            for qid in qs['ids']:
                cand = [i for i in c['pagine'] if i in tp] if not qs['raccolta'] else list(tp)
                # un quiz presente in più lezioni rimanda alla prima, che si apre per prima
                corso['quiz'].setdefault(qid, {**domanda(Q[qid]), 'rivedi': [code, best(qid, cand or list(tp)) + 1]})
    corso['lezioni'].append({
        'id': code, 'num': num, 'titolo': titolo, 'attiva': code in ATTIVE,
        'capitoli': [{'titolo': c['titolo'], 'pagine': [i + 1 for i in c['pagine']], 'quiz': c['quiz']} for c in caps],
        'scheda': schede.get(code, []),
        'appendici': [a for a, ls in APPENDICI.items() if code in ls],
    })
    print(code, len(caps) - 1, 'capitoli,', sum(len(c['pagine']) for c in caps), 'slide,',
          sum(len(q['ids']) for c in caps for q in c['quiz']), 'quiz,', len(schede.get(code, [])), 'pagine di scheda')

# i quiz dei «numeri d'oro» rimandano alla loro lezione; se non c'è, alla pagina dei numeri d'oro
for q in numeri_oro:
    corso['quiz'].setdefault(q, {**domanda(Q[q]), 'rivedi': ['SR', generali[-1]]})

# ---------- appendici: gli HTML esportati con il visore per gli allievi ----------
os.makedirs(OUT + '/appendici', exist_ok=True)
for f in glob.glob(OUT + '/appendici/*.html'):
    os.remove(f)
visore = open(os.path.join(QUI, 'aula', 'proiettore.js'), encoding='utf-8').read()
for html in sorted(glob.glob(os.path.join(EXPORT, 'html', 'Appendice *.html'))):
    m = re.match(r'Appendice ([A-Z]) - (.*)\.html', os.path.basename(html))
    a, titolo = m.group(1), m.group(2)
    h = open(html, encoding='utf-8').read()
    h = h.replace('</body>', '<script>window.VISORE="allievo";' + visore + '</script></body>', 1)
    open(f'{OUT}/appendici/{a.lower()}.html', 'w', encoding='utf-8').write(h)
    # le stesse pagine come immagini (AX-NNN.jpg, con la filigrana): l'app le mostra nel visore delle slide
    doc = pymupdf.open(os.path.join(PDF, f'Appendice {a} - {titolo}.pdf'))
    for i in range(doc.page_count):
        immagine(doc, i, f'A{a}-{i + 1:03d}')
    corso['appendici'].append({'id': a, 'titolo': titolo, 'file': f'appendici/{a.lower()}.html',
                               'slide': h.count('<div class="w"'), 'pagine': doc.page_count, 'lezioni': APPENDICI[a]})

json.dump(corso, open(OUT + '/corso.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(os.listdir(OUT + '/slides')), 'immagini,', sum(os.path.getsize(OUT + '/slides/' + f) for f in os.listdir(OUT + '/slides')) // 1024, 'KB;',
      os.path.getsize(OUT + '/corso.json') // 1024, 'KB di corso.json;', len(corso['quiz']), 'quiz')
