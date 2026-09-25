"""Appendice D: dieci prove d'esame simulate (carteggio 4 esercizi, 20 quiz base, 5 quiz vela) con la correzione."""
import os, sys, json, random, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/deck/project'
DATI=SP+'/rotta-giusta/site/dati'
C=json.load(open(DATI+'/carteggio.json'))
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

ORDER=['cover','indice','regole','come']
for i in range(1,NP+1): ORDER+=[f'p{i}',f'p{i}c1',f'p{i}c2']+[f'p{i}b{k}' for k in range(1,6)]+[f'p{i}v',f'p{i}r']
ORDER+=['chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
HUE=[CORAL,SEA,PURPLE,BLUE,GREEN]
LB.ICON_T.update({'Indice':'book','Le regole dell\'esame':'flag','Come usare le prove':'check'})

# ============ COPERTINA ============
cover(0,'Prove d\'esame simulate','Dieci esami completi come il giorno della prova: 4 esercizi di carteggio, 20 quiz base e 5 quiz vela, con la correzione',
 'Appendice D al corso. Dieci prove costruite come l\'esame del DM 323/2021, art. 6: quiz dall\'elenco ufficiale del DD 131/2022 distribuiti per tema come nell\'All. C, esercizi di carteggio ufficiali. Ogni prova finisce con la slide di correzione.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice D · esercitazione'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
pid=lambda i: 'p'+str(i+1)
pp=lambda i,P: p('Prova '+str(i+1),30,INK,800,1.2)+p('Carta '+P['carta'],24,BODY,500,1.3)
cards=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:12px solid {HUE[i%5]}; border-radius:24px; padding:16px 22px">'
              f'<p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1; color:{HUE[i%5]}; width:60px">{i+1:02d}</p>'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:2px">{pp(i,P)}</div>'
              f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{HUE[i%5]}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(pid(i))}</p></div>' for i,P in enumerate(PROVE))
sec('indice', head('Appendice D · Prove d\'esame','Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px">{cards}</div>',
 notes='Le prove sono tutte diverse: nessun quiz e nessun esercizio si ripete da una prova all\'altra. Si preferiscono domande che non compaiono nelle verifiche delle lezioni. Le prove 5 e 10 usano la carta 42/D, le altre la 5/D.')

# ============ LE REGOLE ============
tile=lambda t,d,c: f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:26px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{squiggle(c,110)}{h3(t,34,c)}{d}</div>'
RG=[('1 · Carteggio','4 esercizi indipendenti, carta 5/D o 42/D','Almeno <b>3 su 4</b> corretti','60 minuti',CORAL),
    ('2 · Quiz base','20 domande, distribuite per tema','Al massimo <b>4 errori</b>','30 minuti',SEA),
    ('3 · Quiz vela','5 domande di vela','Al massimo <b>1 errore</b>','15 minuti',PURPLE)]
g=''.join(tile(t,p(a,26,BODY,400,1.35)+p(b,30,INK,700,1.3)+p('⏱ '+c,28,col,800,1.3),col) for t,a,b,c,col in RG)
sec('regole', head('Appendice D · Prove d\'esame','Le regole dell\'esame',CORAL)+f'<div style="display:flex; gap:24px; align-items:stretch">{g}</div>'
    +note('Il carteggio apre l\'esame ed è propedeutico. Quiz base e vela si fanno in un unico blocco da 45 minuti.',CORAL,36),
 notes='DM 10 agosto 2021 n. 323, art. 6. Carte 5/D e 42/D integre, consegnate all\'appello; si portano squadrette, compasso a punte fisse, matita e gomma. Nel quiz base la ripartizione per tema segue l\'All. C: navigazione 4, COLREG e segnalamento 2, sicurezza 3, normativa 3, manovra e condotta 4, teoria dello scafo 1, meteorologia 2, motori 1.')

# ============ COME USARLE ============
ST=[('Cronometro','Tempi veri: 60 minuti di carteggio, poi 45 per i quiz. Niente pause.',CORAL),
    ('Su carta','Scrivete le risposte su un foglio: lettera per i quiz, coordinate per il carteggio.',SEA),
    ('Correzione','L\'ultima slide di ogni prova dà le risposte ufficiali e dove trovare la soluzione.',PURPLE),
    ('Esito','Promossi se tutte e tre le soglie sono rispettate. Annotate gli errori per tema.',BLUE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:22px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{squiggle(c,110)}{h3(t,30,c)}{p(d,26,BODY,400,1.35)}</div>' for t,d,c in ST)
sec('come', head('Appendice D · Prove d\'esame','Come usare le prove',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{g}</div>'
    +note('Una prova a settimana nelle ultime cinque settimane, due nell\'ultima: all\'esame il tempo non sarà più un problema.',SEA,36),
 notes='Per il carteggio la risposta ufficiale è un intervallo (latitudine, longitudine, rotta o tempo): la risposta è corretta se cade dentro. Gli esercizi sono risolti passo per passo nelle lezioni 10-15 e nell\'Appendice A.')

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
for i,P in enumerate(PROVE,1):
    c=HUE[(i-1)%5]
    sec(f'p{i}', f'<p style="font-family:{HAND}; font-size:48px; font-weight:700; color:{DACC}">Esame simulato</p>'
        +f'<h2 style="font-family:{H}; font-size:120px; font-weight:700; line-height:1; color:#FFFFFF">Prova {i}</h2>{squiggle(DACC,330)}'
        +f'<div style="display:flex; gap:24px">'+''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#1F4266; border-radius:24px; padding:22px 28px">{p(a,26,DSOFT,700,1.3)}{p(b,34,"#FFFFFF",800,1.2)}</div>' for a,b in
          [('Carteggio · carta '+P['carta'],'4 esercizi · 60′'),('Quiz base','20 domande · 30′'),('Quiz vela','5 domande · 15′')])+'</div>',
        dark=True, gap=28, notes=f'Prova {i}. Distribuire la carta {P["carta"]} e far partire il cronometro. Correzione alla slide {N(f"p{i}r")}.')
    e=P['es']
    for k in (1,2):
        a,b=e[2*k-2],e[2*k-1]
        sec(f'p{i}c{k}', head(f'Prova {i} · carteggio · carta {P["carta"]}',f'Esercizi {2*k-1} e {2*k}',c)
            +f'<div style="display:flex; gap:24px; align-items:stretch">{ecard(2*k-1,a,c)}{ecard(2*k,b,c)}</div>',
            notes=f'Esercizi ufficiali {a["id"]} e {b["id"]} (DD 131/2022). Tempo totale per i 4 esercizi: 60 minuti.')
    for k in range(5):
        qs=P['base'][4*k:4*k+4]
        sec(f'p{i}b{k+1}', head(f'Prova {i} · quiz base · domande {4*k+1}–{4*k+4} di 20',f'Quiz base',c)
            +f'<div style="display:flex; gap:20px; align-items:stretch">{"".join(qcard(4*k+j+1,q,c) for j,q in enumerate(qs))}</div>',
            notes='Quiz '+', '.join(q['p'] for q in qs)+'. Una sola risposta esatta; segnare la lettera sul foglio.')
    sec(f'p{i}v', head(f'Prova {i} · quiz vela · 5 domande',f'Quiz vela',c)
        +f'<div style="display:flex; gap:18px; align-items:stretch">{"".join(qcard(j+1,q,c) for j,q in enumerate(P["vela"]))}</div>',
        notes='Quiz '+', '.join(q['p'] for q in P['vela'])+'. Al massimo un errore.')
    # correzione
    ec=''.join(f'<div style="display:flex; flex-direction:column; gap:4px; background:#FFFFFF; border-left:10px solid {c}; border-radius:18px; padding:12px 18px">'
               +p('<b>'+str(n)+'</b> · '+x['argomento']+' · '+x['id'],24,SOFT,700,1.3)+p(x['risposta_ufficiale'],24,INK,800,1.3)+p('Risolto nella lezione '+str(lesson(x)),24,c,700,1.3)+'</div>' for n,x in enumerate(e,1))
    cell=lambda n,q: f'<p style="font-size:26px; font-weight:800; color:{INK}; background:{SEA_T}; border-radius:12px; padding:6px 0px; text-align:center">{n} · {"abc"[q["x"]]}</p>'
    grid=f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px">{"".join(cell(n,q) for n,q in enumerate(P["base"],1))}</div>'
    vg=f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px">{"".join(cell(n,q).replace(SEA_T,LILAC_T) for n,q in enumerate(P["vela"],1))}</div>'
    right=(tag('Quiz base · max 4 errori',SEA)+grid+tag('Quiz vela · max 1 errore',PURPLE)+vg)
    sec(f'p{i}r', head(f'Prova {i} · correzione','Le risposte esatte',SEA)
        +f'<div style="display:flex; gap:32px"><div style="width:760px; display:flex; flex-direction:column; gap:10px">{tag("Carteggio · almeno 3 su 4",CORAL)}{ec}</div>'
         f'<div style="flex:1; display:flex; flex-direction:column; gap:12px">{right}</div></div>',
        notes='Risposte base: '+'; '.join(f'{n} {q["p"]} → {"abc"[q["x"]]}) {q["r"][q["x"]].strip()}' for n,q in enumerate(P['base'],1))
              +'. Vela: '+'; '.join(f'{n} {q["p"]} → {q["r"][q["x"]].strip()}' for n,q in enumerate(P['vela'],1))
              +'. Carteggio: la risposta ufficiale è un intervallo; è corretta se cade dentro.')

closing(['Tre prove, tre soglie: carteggio 3 su 4, quiz base 4 errori al massimo, vela 1 al massimo',
         'Il carteggio apre l\'esame: se non passa, la sessione finisce lì',
         'Il tempo si allena: fate le prove con il cronometro, non a pezzi',
         'Annotate gli errori per tema e ripassate la lezione corrispondente',
         'Portate carte integre, squadrette, compasso, matita morbida e gomma'],
 'Buon vento per l\'esame!','Appendice D · Prove d\'esame simulate')

write_deck(OUT,'Appendice D · Prove d\'esame simulate',ORDER,
 {"s1":{"description":"Copertina, indice, regole e metodo","start":"cover"},
  **{f"s{i+1}":{"description":f"Prova {i}: carteggio, quiz base, quiz vela e correzione","start":f"p{i}"} for i in range(1,NP+1)}})
json.dump([dict(carta=P['carta'],es=[x['id'] for x in P['es']],base=[q['p'] for q in P['base']],vela=[q['p'] for q in P['vela']]) for P in PROVE],
          open(SP+'/prove.json','w'),indent=1)
