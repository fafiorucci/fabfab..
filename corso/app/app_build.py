import pymupdf, json, re, math, io, collections
from PIL import Image
import os
SP=os.environ.get('SP','/tmp/scratch')  # cartella di lavoro con rotta-giusta/ e app/
OUT=SP+'/app'
Q={q['p']:q for q in json.load(open(SP+'/rotta-giusta/site/dati/quiz.json')) if q.get('p')}
LEZ=[('L01','Lezione 01','Teoria dello scafo','/home/user/fabfab../corso/export/pdf/Lezione 01 - Teoria dello scafo.pdf'),
     ('L02','Lezione 02','Motori, elica e timone','/home/user/fabfab../corso/export/pdf/Lezione 02 - Motori, elica e timone.pdf')]
STOP=set('della delle dello degli nella nelle sono essere viene vengono quale quali come cosa ogni anche solo dove quando sulla sulle questo questa questi tutte tutti molto dalla dalle alla alle allo agli unità ecc oppure mentre perché però hanno avere'.split())
def toks(t):
    return [w[:6] for w in re.findall(r"[a-zàèéìòù]{4,}", t.lower()) if w not in STOP]
corso={'lezioni':[], 'quiz':{}}
for code,num,titolo,pdf in LEZ:
    d=pymupdf.open(pdf); pages=[]
    for i in range(d.page_count):
        t=' '.join(d[i].get_text().split())
        if i==0: k='cover'
        elif t.startswith(('CAPITOLO','ULTIMI 45 MINUTI')): k='chapter'
        elif t.startswith(('VERIFICA · QUIZ','RACCOLTA QUIZ')): k='quiz'
        elif t.startswith('VERIFICA · RISPOSTE'): k='answers'
        elif t.startswith('IN SINTESI'): k='closing'
        elif t.startswith('LEZIONE '): k='intro'
        else: k='theory'
        pages.append((i,k,t))
    # chapters
    caps=[{'titolo':'Introduzione','pagine':[],'quiz':[]}]
    for i,k,t in pages:
        if k=='chapter':
            m=re.match(r'CAPITOLO (\d+) (.*?) circa',t)
            tit=f'Capitolo {m.group(1)} · {m.group(2)}' if m else 'Raccolta quiz · ultimi 45 minuti'
            caps.append({'titolo':tit,'pagine':[i],'quiz':[]})
        elif k in ('cover','theory','closing','intro'):
            caps[-1]['pagine'].append(i)
        elif k=='quiz':
            m=re.search(r'(Quiz \d+ · .*?) Domanda 1',t); ids=re.findall(r'quiz (\d+\.\d+\.\d+-\d+)',t)
            caps[-1]['quiz'].append({'titolo':m.group(1) if m else 'Quiz','ids':ids,'raccolta':t.startswith('RACCOLTA')})
    # closing page into its own? keep in last chapter
    # images
    zoom=1280/d[0].rect.width
    for c in caps:
        for i in c['pagine']:
            pix=d[i].get_pixmap(matrix=pymupdf.Matrix(zoom,zoom))
            im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
            im.save(f'{OUT}/slides/{code}-{i+1:03d}.jpg','JPEG',quality=74,optimize=True,progressive=True)
    # idf over theory pages
    tp={i:toks(t) for i,k,t in pages if k in ('theory','closing')}
    df=collections.Counter(w for v in tp.values() for w in set(v)); N=len(tp)
    def best(qid,cand):
        q=Q[qid]; ws=set(toks(q['d']+' '+q['r'][q['x']]))
        sc=[(sum(math.log(N/df[w]) for w in ws if w in set(tp[i])),i) for i in cand if i in tp]
        sc.sort(reverse=True); return sc[0][1] if sc and sc[0][0]>0 else (cand[0] if cand else None)
    alltheory=[i for i in tp]
    for c in caps:
        for qs in c['quiz']:
            for qid in qs['ids']:
                cand=[i for i in c['pagine'] if i in tp] if not qs['raccolta'] else alltheory
                rv=best(qid,cand or alltheory)
                q=Q[qid]
                corso['quiz'][qid]={'d':q['d'].strip(),'r':[r.strip().rstrip(';,') for r in q['r']],'x':q['x'],'v':q.get('v',''),'t':q.get('t',''),'rivedi':[code,rv+1]}
    corso['lezioni'].append({'id':code,'num':num,'titolo':titolo,'capitoli':[{'titolo':c['titolo'],'pagine':[i+1 for i in c['pagine']],'quiz':c['quiz']} for c in caps]})
json.dump(corso,open(OUT+'/corso.json','w'),ensure_ascii=False,separators=(',',':'))
import os
print(len(os.listdir(OUT+'/slides')), sum(os.path.getsize(OUT+'/slides/'+f) for f in os.listdir(OUT+'/slides'))//1024,'KB', os.path.getsize(OUT+'/corso.json')//1024,'KB')
for L in corso['lezioni']:
    for c in L['capitoli']: print(L['id'],c['titolo'],c['pagine'],[ (q['titolo'],len(q['ids'])) for q in c['quiz']][:3])
