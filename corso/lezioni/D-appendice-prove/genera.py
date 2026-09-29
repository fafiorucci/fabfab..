"""Appendice D: prove d'esame simulate in due parti. Parte 1: dieci prove entro 12 miglia (quiz di elementi di carteggio sulla 5/D, 20 quiz base, 5 quiz vela). Parte 2: dieci prove oltre 12 miglia (carteggio 4 esercizi, 20 quiz base, 5 quiz vela). Con la correzione."""
import os, sys, json, random, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/deck/project'
DATI=SP+'/rotta-giusta/site/dati'
C=json.load(open(DATI+'/carteggio.json'))
E12=json.load(open(DATI+'/carteggio_e12.json'))
QL=json.load(open(DATI+'/quiz.json'))
NP=10
rnd=random.Random(2026)

# ---------- quiz già usati nelle lezioni (per preferire domande nuove) ----------
cited=set()
for f in glob.glob('/home/user/fabfab../corso/lezioni/*/genera.py'):
    t=open(f).read()
    for m in re.finditer(r'(\d\.\d\.\d)-(\d+)((?:\s*(?:,|e)\s*-\d+)*)',t):
        cited.add(f'{m.group(1)}-{m.group(2)}'); cited.update(f'{m.group(1)}-{n}' for n in re.findall(r'-(\d+)',m.group(3)))
def ok(q,lim):
    return not q.get('osc') and not q.get('f') and q['x'] is not None and len(q['d'])+sum(len(r) for r in q['r'])<=lim
DIST=[('NAVIGAZIONE CARTOGRAFICA ED ELETTRONICA',4),('COLREG E SEGNALAMENTO MARITTIMO',2),('SICUREZZA DELLA NAVIGAZIONE',3),
      ('NORMATIVA DIPORTISTICA E AMBIENTALE',3),('MANOVRA E CONDOTTA',4),('TEORIA DELLO SCAFO',1),('METEOROLOGIA',2),('MOTORI',1)]
pools={}
for t,_ in DIST+[('VELA',0)]:
    lim=240 if t=='VELA' else 330
    qs=[q for q in QL if q['t']==t and ok(q,lim)]
    new=[q for q in qs if q['p'] not in cited]; old=[q for q in qs if q['p'] in cited]
    rnd.shuffle(new); rnd.shuffle(old); pools[t]=new+old
def take(t,n): out=pools[t][:n]; pools[t]=pools[t][n:]; return out

# ---------- carteggio: un esercizio per argomento, carte diverse ----------
cp={}
for x in C: cp.setdefault((x['carta'],x['argomento']),[]).append(x)
for v in cp.values(): rnd.shuffle(v)
def lesson(x):
    fam=x['famiglia']; a=fam.split('.')[2]; s=int(fam.split('.')[1])
    if x['carta']=='42/D': return 12 if a=='4' else 15
    return {'1':13 if s<=3 else 14,'2':11,'3':10,'4':12}[a]
PROVE=[]
for i in range(NP):
    if i in (4,9):   # due prove sulla carta 42/D
        es=[cp[('42/D','navigazione costiera')].pop(),cp[('42/D','correnti')].pop(),cp[('42/D','scarroccio')].pop(),cp[('42/D','correnti')].pop()]
    else:
        es=[cp[('5/D',a)].pop() for a in ('navigazione costiera','carburante','scarroccio','correnti')]
    base=[q for t,n in DIST for q in take(t,n)]
    es=sorted(es,key=lambda x:-len(x['testo'])); es=[es[0],es[3],es[1],es[2]]
    PROVE.append(dict(carta=es[0]['carta'],es=es,base=base,vela=take('VELA',5)))

# ---------- prove oltre 12 miglia: fissate in prove_oltre.json (quelle pubblicate), se presente ----------
PO=os.path.join(os.path.dirname(os.path.abspath(__file__)),'prove_oltre.json')
if os.path.exists(PO):
    CI={x['id']:x for x in C}; QI={q['p']:q for q in QL}
    PROVE=[dict(carta=d['carta'],es=[CI[i] for i in d['es']],base=[QI[p] for p in d['base']],vela=[QI[p] for p in d['vela']]) for d in json.load(open(PO))]
    used={q['p'] for P in PROVE for q in P['base']+P['vela']}
    for t in pools: pools[t]=[q for q in pools[t] if q['p'] not in used]

# ---------- prove entro 12 miglia: un esercizio ufficiale per settore, quiz nuovi ----------
sett={}
for x in E12:
    h=x['testo'].split('\n')[0].strip()
    if h.upper().startswith('SETTORE'): sett.setdefault(h.title(),[]).append(x)
for v in sett.values(): rnd.shuffle(v)
SK=sorted(sett)
PROVE12=[]
for i in range(NP):
    x=sett[SK[i%len(SK)]].pop()
    base=[q for t,n in DIST for q in take(t,n)]
    PROVE12.append(dict(es=x,sett=SK[i%len(SK)],base=base,vela=take('VELA',5)))
def qtext(x):
    t=x['testo']; head,_,rest=t.partition('\n')
    corpo=re.split(r'\s*quesito\s*1\s*:',rest)[0].strip()
    corpo=re.sub(r'[,;]?\s*(determinare|si determini|calcolare)\s*:?\s*$','.',corpo,flags=re.I).strip()
    qs=[re.sub(r'\s+',' ',q).strip() for _,q in re.findall(r'quesito\s*(\d)\s*:\s*(.+?)(?=\s*quesito\s*\d\s*:|$)',t,re.S)]
    return head.strip().title(),corpo,qs

ORDER=['cover','indice','regole','come','parte1']
for i in range(1,NP+1): ORDER+=[f'e{i}',f'e{i}c']+[f'e{i}b{k}' for k in range(1,6)]+[f'e{i}v',f'e{i}r']
ORDER+=['parte2']
for i in range(1,NP+1): ORDER+=[f'p{i}',f'p{i}c1',f'p{i}c2']+[f'p{i}b{k}' for k in range(1,6)]+[f'p{i}v',f'p{i}r']
ORDER+=['chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
HUE=[CORAL,SEA,PURPLE,BLUE,GREEN]
LB.ICON_T.update({'Indice':'book','Le regole dell\'esame':'flag','Come usare le prove':'check'})

# ============ COPERTINA ============
cover(0,'Prove d\'esame simulate','Venti esami completi, in due parti: dieci entro 12 miglia e dieci oltre 12 miglia, con la correzione',
 'Appendice D al corso, in due parti. Parte 1: dieci prove entro 12 miglia, con il quiz di elementi di carteggio sulla carta 5/D (un esercizio ufficiale, 5 quesiti), 20 quiz base e 5 quiz vela. Parte 2: dieci prove oltre 12 miglia, con la prova di carteggio di 4 esercizi, 20 quiz base e 5 quiz vela. Quiz ed esercizi dall\'elenco ufficiale del DD 131/2022, distribuiti come all\'esame (DM 323/2021, art. 6 e All. C). Ogni prova finisce con la slide di correzione.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice D · esercitazione'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
def part_card(n,t,d,ids,c):
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:14px; background:#FFFFFF; border-top:12px solid {c}; border-radius:28px; padding:30px 34px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
            f'<div style="display:flex; align-items:center; justify-content:space-between"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">Parte {n}</p>'
            f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(ids[0])}–{N(ids[1])}</p></div>'
            f'{h3(t,40,INK)}{d}</div>')
li=lambda xs: ''.join(p('· '+x,26,BODY,400,1.4) for x in xs)
P1=part_card(1,'Prove entro 12 miglia',li(['10 prove complete, dalla prova 1 alla 10','Quiz di elementi di carteggio: 1 esercizio ufficiale sulla carta 5/D, 5 quesiti, 20 minuti','20 quiz base e 5 quiz vela','Correzione alla fine di ogni prova']),['parte1','e10r'],SEA)
P2=part_card(2,'Prove oltre 12 miglia',li(['10 prove complete, dalla prova 1 alla 10','Prova di carteggio: 4 esercizi sulla carta 5/D o 42/D, 60 minuti','20 quiz base e 5 quiz vela','Correzione alla fine di ogni prova']),['parte2','p10r'],CORAL)
sec('indice', head('Appendice D · Prove d\'esame','Indice')+f'<div style="display:flex; gap:28px; align-items:stretch">{P1}{P2}</div>'
    +note('Chi prende la patente entro 12 miglia fa la parte 1; chi va oltre le 12 miglia fa la parte 2, e può usare la parte 1 per allenare quiz base e vela.',SEA,34),
 notes='L\'appendice è divisa in due parti, una per patente. Le prove sono tutte diverse: nessun quiz e nessun esercizio si ripete, né dentro una parte né tra le due parti. Si preferiscono domande che non compaiono nelle verifiche delle lezioni. Parte 1: gli esercizi entro 12 miglia sono i 50 dell\'elenco ufficiale (sigla 4.1.1), tutti sulla carta 5/D, divisi in tre settori. Parte 2: le prove 5 e 10 usano la carta 42/D, le altre la 5/D.')

# ============ LE REGOLE ============
pd='padding:14px 20px; vertical-align:top; '
def rtable(cols,rows):
    th=''.join(f'<th style="{pd}width:{w}%; color:#FFFFFF; background:{c}; text-align:left">{t}</th>' for t,c,w in cols)
    body=''.join(f'<tr style="background:{"#FFFFFF" if k%2==0 else PAPER}">'+''.join(f'<td style="{pd}{"font-weight:800; " if j==0 else ""}color:{INK}">{v}</td>' for j,v in enumerate(r))+'</tr>' for k,r in enumerate(rows))
    return f'<table style="font-size:27px; line-height:1.35; color:{BODY}; width:1664px"><tr>{th}</tr>{body}</table>'
RR=[('1 · Carteggio','Quiz di elementi di carteggio: 1 esercizio sulla carta 5/D, <b>5 quesiti</b> · <b>20 minuti</b> · almeno <b>4 su 5</b>','Prova di carteggio: <b>4 esercizi</b> sulla carta 5/D o 42/D · <b>60 minuti</b> · almeno <b>3 su 4</b>'),
    ('2 · Quiz base','20 domande distribuite per tema · <b>30 minuti</b> · al massimo <b>4 errori</b>','uguale'),
    ('3 · Quiz vela','5 domande · <b>15 minuti</b> · al massimo <b>1 errore</b>','uguale')]
sec('regole', head('Appendice D · Prove d\'esame','Le regole dell\'esame',CORAL)
    +rtable([('Prova',NAVY,20),('Parte 1 · entro 12 miglia',SEA,40),('Parte 2 · oltre 12 miglia',CORAL,40)],RR)
    +note('Il carteggio apre l\'esame ed è propedeutico: se non lo superi, non prosegui con i quiz.',CORAL,36),
 notes='DM 10 agosto 2021 n. 323, art. 6. Entro 12 miglia: quiz di elementi di carteggio, 5 quesiti a risposta singola che formano la soluzione di un esercizio dell\'elenco (50 esercizi, carta 5/D), 20 minuti, almeno 4 risposte esatte. Oltre 12 miglia: prova di carteggio con 4 esercizi, 60 minuti, almeno 3 corretti. Quiz base e quiz vela sono uguali per le due patenti. Carte integre, consegnate all\'appello; si portano squadrette, compasso a punte fisse, matita e gomma. Nel quiz base la ripartizione per tema segue l\'All. C: navigazione 4, COLREG e segnalamento 2, sicurezza 3, normativa 3, manovra e condotta 4, teoria dello scafo 1, meteorologia 2, motori 1.')

# ============ COME USARLE ============
ST=[('Cronometro','Tempi veri: 20 minuti di carteggio entro 12 miglia, 60 oltre; poi i quiz. Niente pause.',CORAL),
    ('Su carta','Scrivete le risposte su un foglio: lettera per i quiz, valori e coordinate per il carteggio.',SEA),
    ('Correzione','L\'ultima slide di ogni prova dà le risposte ufficiali e dove ripassare.',PURPLE),
    ('Esito','Promossi se tutte le soglie sono rispettate. Annotate gli errori per tema.',BLUE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:22px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{squiggle(c,110)}{h3(t,30,c)}{p(d,26,BODY,400,1.35)}</div>' for t,d,c in ST)
sec('come', head('Appendice D · Prove d\'esame','Come usare le prove',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{g}</div>'
    +note('Una prova a settimana nelle ultime cinque settimane, due nell\'ultima: all\'esame il tempo non sarà più un problema.',SEA,36),
 notes='Per il carteggio la risposta ufficiale è un intervallo (distanze, tempi, carburante, coordinate, rotte): la risposta è corretta se cade dentro. Gli esercizi oltre 12 miglia sono risolti passo per passo nelle lezioni 10-15 e nell\'Appendice A; quelli entro 12 miglia usano il metodo delle lezioni 03 e 04 (distanze, coordinate, tempo e velocità, carburante) e il lavoro sulla carta 5/D della lezione 10.')

# ============ DIVISORI DELLE PARTI ============
def divider(sid,n,t,sub,ids,c,info):
    cards=''.join(f'<div style="display:flex; align-items:center; gap:14px; background:#1F4266; border-radius:20px; padding:12px 18px">'
                  f'<p style="font-family:{H}; font-size:40px; font-weight:700; line-height:1; color:{DACC}; width:52px">{i:02d}</p>'
                  f'<div style="flex:1; display:flex; flex-direction:column; gap:2px">{p("Prova "+str(i),26,"#FFFFFF",800,1.2)}{p(info(i),24,DSOFT,500,1.3)}</div>'
                  f'<p style="font-size:24px; font-weight:900; color:{NAVY}; background:{DACC}; padding:2px 12px; border-radius:12px">{N(ids(i))}</p></div>' for i in range(1,NP+1))
    sec(sid, f'<p style="font-family:{HAND}; font-size:48px; font-weight:700; color:{DACC}">Parte {n}</p>'
        +f'<h2 style="font-family:{H}; font-size:96px; font-weight:700; line-height:1; color:#FFFFFF">{t}</h2>{squiggle(DACC,330)}'
        +p(sub,30,DSOFT,500,1.35)+f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:12px">{cards}</div>',
        dark=True, gap=24, notes=f'Parte {n}: {t.lower()}. {sub}')

# ============ LE PROVE ============
def qcard(n,q,c):
    opts=''.join(f'<p style="font-size:24px; line-height:1.3; color:{BODY}">{"abc"[j]}) {o.strip().rstrip(";").rstrip(",")}</p>' for j,o in enumerate(q['r']))
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-left:10px solid {c}; border-radius:24px; padding:22px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
            f'<p style="font-family:{H}; font-size:30px; font-weight:700; color:{c}">{n}</p>{p(q["d"].strip(),26,INK,700,1.3)}<div style="display:flex; flex-direction:column; gap:6px">{opts}</div></div>')
def ecard(n,x,c):
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-left:10px solid {c}; border-radius:24px; padding:26px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
            f'<p style="font-family:{H}; font-size:30px; font-weight:700; color:{c}">Esercizio {n} · {x["argomento"]}</p>'
            +''.join(p(r,24,INK,500,1.3) for r in paras(x['testo']))+'</div>')
def paras(t):
    out=[]
    for r in [r.strip() for r in t.split('\n') if r.strip()]:
        if out and not out[-1].endswith(('.',':',';',')')): out[-1]+=' '+r
        else: out.append(r)
    return out
# ============ PARTE 1 · ENTRO 12 MIGLIA ============
divider('parte1',1,'Prove entro 12 miglia','Quiz di elementi di carteggio sulla carta 5/D (20 minuti), 20 quiz base, 5 quiz vela.',lambda i:f'e{i}',SEA,lambda i:PROVE12[i-1]['sett'].replace('Settore ','settore '))
for i,P in enumerate(PROVE12,1):
    c=HUE[(i-1)%5]
    sec(f'e{i}', f'<p style="font-family:{HAND}; font-size:48px; font-weight:700; color:{DACC}">Esame simulato · entro 12 miglia</p>'
        +f'<h2 style="font-family:{H}; font-size:120px; font-weight:700; line-height:1; color:#FFFFFF">Prova {i}</h2>{squiggle(DACC,330)}'
        +f'<div style="display:flex; gap:24px">'+''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#1F4266; border-radius:24px; padding:22px 28px">{p(a,26,DSOFT,700,1.3)}{p(b,34,"#FFFFFF",800,1.2)}</div>' for a,b in
          [('Carteggio · carta 5/D','5 quesiti · 20′'),('Quiz base','20 domande · 30′'),('Quiz vela','5 domande · 15′')])+'</div>',
        dark=True, gap=28, notes=f'Parte 1, prova {i}, entro 12 miglia. Distribuire la carta 5/D e far partire il cronometro: 20 minuti per il carteggio. Correzione alla slide {N(f"e{i}r")}.')
    sett_,corpo,qs=qtext(P['es'])
    qb=''.join(f'<div style="display:flex; align-items:center; gap:16px; background:{PAPER}; border-radius:16px; padding:12px 18px"><p style="font-family:{H}; font-size:34px; font-weight:700; color:{c}; width:40px">{n}</p>{p(q[:1].upper()+q[1:],28,INK,700,1.3)}</div>' for n,q in enumerate(qs,1))
    sec(f'e{i}c', head(f'Prova {i} · entro 12 miglia · carteggio · carta 5/D',f'Quiz di elementi di carteggio',c)
        +f'<div style="display:flex; gap:28px; align-items:stretch">'
         f'<div style="flex:1.1; display:flex; flex-direction:column; gap:14px; background:#FFFFFF; border-left:10px solid {c}; border-radius:24px; padding:28px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
         f'{tag(sett_,c)}{p(corpo,30,INK,500,1.45)}</div>'
         f'<div style="flex:1; display:flex; flex-direction:column; gap:12px">{tag("Determinare",c)}{qb}</div></div>'
        +note('20 minuti · almeno 4 risposte esatte su 5 · usare la carta 5/D, squadrette e compasso.',c,32),
        notes=f'Esercizio ufficiale {P["es"]["id"]} (DD 131/2022, elenco entro 12 miglia). Ogni quesito ha una sola risposta esatta: la risposta ufficiale è un intervallo di valori.')
    for k in range(5):
        qs4=P['base'][4*k:4*k+4]
        sec(f'e{i}b{k+1}', head(f'Prova {i} · entro 12 miglia · quiz base · domande {4*k+1}–{4*k+4} di 20',f'Quiz base',c)
            +f'<div style="display:flex; gap:20px; align-items:stretch">{"".join(qcard(4*k+j+1,q,c) for j,q in enumerate(qs4))}</div>',
            notes='Quiz '+', '.join(q['p'] for q in qs4)+'. Una sola risposta esatta; segnare la lettera sul foglio.')
    sec(f'e{i}v', head(f'Prova {i} · entro 12 miglia · quiz vela · 5 domande',f'Quiz vela',c)
        +f'<div style="display:flex; gap:18px; align-items:stretch">{"".join(qcard(j+1,q,c) for j,q in enumerate(P["vela"]))}</div>',
        notes='Quiz '+', '.join(q['p'] for q in P['vela'])+'. Al massimo un errore. Solo per chi prende anche la vela.')
    ans=''.join(f'<div style="display:flex; gap:14px; align-items:start; background:#FFFFFF; border-left:10px solid {c}; border-radius:16px; padding:10px 16px">'
                f'<p style="font-family:{H}; font-size:30px; font-weight:700; color:{c}; width:28px">{q["n"]}</p><div style="display:flex; flex-direction:column; gap:2px">'
                +p(qs[q['n']-1][:1].upper()+qs[q['n']-1][1:],24,SOFT,700,1.25)+p(q['risposta'].replace('\n',' · '),24,INK,800,1.3)+'</div></div>' for q in P['es']['quesiti'])
    cell=lambda n,q: f'<p style="font-size:26px; font-weight:800; color:{INK}; background:{SEA_T}; border-radius:12px; padding:6px 0px; text-align:center">{n} · {"abc"[q["x"]]}</p>'
    grid=f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px">{"".join(cell(n,q) for n,q in enumerate(P["base"],1))}</div>'
    vg=f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px">{"".join(cell(n,q).replace(SEA_T,LILAC_T) for n,q in enumerate(P["vela"],1))}</div>'
    sec(f'e{i}r', head(f'Prova {i} · entro 12 miglia · correzione','Le risposte esatte',SEA)
        +f'<div style="display:flex; gap:32px"><div style="width:760px; display:flex; flex-direction:column; gap:8px">{tag("Carteggio · "+P["es"]["id"]+" · almeno 4 su 5",CORAL)}{ans}</div>'
         f'<div style="flex:1; display:flex; flex-direction:column; gap:12px">{tag("Quiz base · max 4 errori",SEA)}{grid}{tag("Quiz vela · max 1 errore",PURPLE)}{vg}</div></div>',
        notes='Carteggio '+P['es']['id']+': '+'; '.join(f'{q["n"]} {q["etichetta"]} → {q["risposta"].replace(chr(10)," ")}' for q in P['es']['quesiti'])
              +'. La risposta è corretta se cade nell\'intervallo ufficiale. Metodo: lezioni 03 e 04 (distanze, coordinate, tempo e velocità, carburante) e lezione 10 (la carta 5/D). Risposte base: '
              +'; '.join(f'{n} {q["p"]} → {"abc"[q["x"]]}) {q["r"][q["x"]].strip()}' for n,q in enumerate(P['base'],1))
              +'. Vela: '+'; '.join(f'{n} {q["p"]} → {q["r"][q["x"]].strip()}' for n,q in enumerate(P['vela'],1))+'.')

# ============ PARTE 2 · OLTRE 12 MIGLIA ============
divider('parte2',2,'Prove oltre 12 miglia','Prova di carteggio con 4 esercizi sulla carta 5/D o 42/D (60 minuti), 20 quiz base, 5 quiz vela.',lambda i:f'p{i}',CORAL,lambda i:'carta '+PROVE[i-1]['carta'])

for i,P in enumerate(PROVE,1):
    c=HUE[(i-1)%5]
    sec(f'p{i}', f'<p style="font-family:{HAND}; font-size:48px; font-weight:700; color:{DACC}">Esame simulato · oltre 12 miglia</p>'
        +f'<h2 style="font-family:{H}; font-size:120px; font-weight:700; line-height:1; color:#FFFFFF">Prova {i}</h2>{squiggle(DACC,330)}'
        +f'<div style="display:flex; gap:24px">'+''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#1F4266; border-radius:24px; padding:22px 28px">{p(a,26,DSOFT,700,1.3)}{p(b,34,"#FFFFFF",800,1.2)}</div>' for a,b in
          [('Carteggio · carta '+P['carta'],'4 esercizi · 60′'),('Quiz base','20 domande · 30′'),('Quiz vela','5 domande · 15′')])+'</div>',
        dark=True, gap=28, notes=f'Parte 2, prova {i}, oltre 12 miglia. Distribuire la carta {P["carta"]} e far partire il cronometro. Correzione alla slide {N(f"p{i}r")}.')
    e=P['es']
    for k in (1,2):
        a,b=e[2*k-2],e[2*k-1]
        sec(f'p{i}c{k}', head(f'Prova {i} · oltre 12 miglia · carteggio · carta {P["carta"]}',f'Esercizi {2*k-1} e {2*k}',c)
            +f'<div style="display:flex; gap:24px; align-items:stretch">{ecard(2*k-1,a,c)}{ecard(2*k,b,c)}</div>',
            notes=f'Esercizi ufficiali {a["id"]} e {b["id"]} (DD 131/2022). Tempo totale per i 4 esercizi: 60 minuti.')
    for k in range(5):
        qs=P['base'][4*k:4*k+4]
        sec(f'p{i}b{k+1}', head(f'Prova {i} · oltre 12 miglia · quiz base · domande {4*k+1}–{4*k+4} di 20',f'Quiz base',c)
            +f'<div style="display:flex; gap:20px; align-items:stretch">{"".join(qcard(4*k+j+1,q,c) for j,q in enumerate(qs))}</div>',
            notes='Quiz '+', '.join(q['p'] for q in qs)+'. Una sola risposta esatta; segnare la lettera sul foglio.')
    sec(f'p{i}v', head(f'Prova {i} · oltre 12 miglia · quiz vela · 5 domande',f'Quiz vela',c)
        +f'<div style="display:flex; gap:18px; align-items:stretch">{"".join(qcard(j+1,q,c) for j,q in enumerate(P["vela"]))}</div>',
        notes='Quiz '+', '.join(q['p'] for q in P['vela'])+'. Al massimo un errore.')
    # correzione
    ec=''.join(f'<div style="display:flex; flex-direction:column; gap:4px; background:#FFFFFF; border-left:10px solid {c}; border-radius:18px; padding:12px 18px">'
               +p('<b>'+str(n)+'</b> · '+x['argomento']+' · '+x['id'],24,SOFT,700,1.3)+p(x['risposta_ufficiale'],24,INK,800,1.3)+p('Risolto nella lezione '+str(lesson(x)),24,c,700,1.3)+'</div>' for n,x in enumerate(e,1))
    cell=lambda n,q: f'<p style="font-size:26px; font-weight:800; color:{INK}; background:{SEA_T}; border-radius:12px; padding:6px 0px; text-align:center">{n} · {"abc"[q["x"]]}</p>'
    grid=f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px">{"".join(cell(n,q) for n,q in enumerate(P["base"],1))}</div>'
    vg=f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px">{"".join(cell(n,q).replace(SEA_T,LILAC_T) for n,q in enumerate(P["vela"],1))}</div>'
    right=(tag('Quiz base · max 4 errori',SEA)+grid+tag('Quiz vela · max 1 errore',PURPLE)+vg)
    sec(f'p{i}r', head(f'Prova {i} · oltre 12 miglia · correzione','Le risposte esatte',SEA)
        +f'<div style="display:flex; gap:32px"><div style="width:760px; display:flex; flex-direction:column; gap:10px">{tag("Carteggio · almeno 3 su 4",CORAL)}{ec}</div>'
         f'<div style="flex:1; display:flex; flex-direction:column; gap:12px">{right}</div></div>',
        notes='Risposte base: '+'; '.join(f'{n} {q["p"]} → {"abc"[q["x"]]}) {q["r"][q["x"]].strip()}' for n,q in enumerate(P['base'],1))
              +'. Vela: '+'; '.join(f'{n} {q["p"]} → {q["r"][q["x"]].strip()}' for n,q in enumerate(P['vela'],1))
              +'. Carteggio: la risposta ufficiale è un intervallo; è corretta se cade dentro.')

closing(['Entro 12 miglia: carteggio 4 quesiti su 5 in 20 minuti; oltre: 3 esercizi su 4 in 60 minuti',
         'Quiz base (max 4 errori) e quiz vela (max 1) sono uguali per le due patenti',
         'Il tempo si allena: fate le prove con il cronometro, non a pezzi',
         'Annotate gli errori per tema e ripassate la lezione corrispondente',
         'Il carteggio apre l\'esame: portate carte integre, squadrette, compasso, matita e gomma'],
 'Buon vento per l\'esame!','Appendice D · Prove d\'esame simulate')

write_deck(OUT,'Appendice D · Prove d\'esame simulate',ORDER,
 {"s1":{"description":"Copertina, indice, regole e metodo","start":"cover"},
  "s2":{"description":"Parte 1: dieci prove entro 12 miglia, con il quiz di elementi di carteggio sulla carta 5/D","start":"parte1"},
  **{f"s{i+2}":{"description":f"Entro 12 miglia · prova {i}: carteggio, quiz base, quiz vela e correzione","start":f"e{i}"} for i in range(1,NP+1)},
  "s13":{"description":"Parte 2: dieci prove oltre 12 miglia, con la prova di carteggio di 4 esercizi","start":"parte2"},
  **{f"s{i+13}":{"description":f"Oltre 12 miglia · prova {i}: carteggio, quiz base, quiz vela e correzione","start":f"p{i}"} for i in range(1,NP+1)}})
json.dump([dict(carta=P['carta'],es=[x['id'] for x in P['es']],base=[q['p'] for q in P['base']],vela=[q['p'] for q in P['vela']]) for P in PROVE],
          open(SP+'/appD/prove.json','w'),indent=1)
json.dump([dict(es=P['es']['id'],base=[q['p'] for q in P['base']],vela=[q['p'] for q in P['vela']]) for P in PROVE12],open(SP+'/appD/prove_entro.json','w'),indent=1)
