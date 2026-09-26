import os, re, json, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import *
SP=os.path.dirname(os.path.abspath(__file__))
SRC=SP+'/read9/project'; OUT=SP+'/indice2/project'
os.makedirs(OUT+'/slides',exist_ok=True)
deck=json.load(open(SRC+'/deck.json'))
order=deck['order']
def src(i): return open(f'{SRC}/slides/{i}.html').read()
def notes_of(s):
    m=re.search(r'<aside>(.*?)</aside>',s,re.S); return m.group(1).strip() if m else ''
def section(i, n, inner, notes='', dark=False, gap=32, pinned=''):
    bg = NAVY if dark else PAPER; col = PAPER if dark else BODY
    return (f'<section id="{i}" data-transition="fade" style="background:{bg}; color:{col}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">\n{backdrop(dark,n)}\n{inner}\n{pinned}{footer(n,dark)}\n'
            + (f'<aside>{notes}</aside>\n' if notes else '') + '</section>\n')
HDR=re.compile(r'<div style="display:flex; flex-direction:column; gap:16px">\s*<p[^>]*>(.*?)</p>\s*<h2[^>]*>(.*?)</h2>\s*</div>',re.S)
def restyle(s):
    s=s.replace("'Libre Baskerville', Georgia, serif",H).replace("'Public Sans', Arial, sans-serif",B)
    s=re.sub(r'border-radius:\s*(16|24)px','border-radius:36px',s)
    accs=iter([CORAL,SEA,SUN,PURPLE,BLUE,GREEN]*20)
    s=re.sub(r'background:\s*#eae4d6;?',lambda m: f'background:#FFFFFF; border-left:12px solid {next(accs)}; {SHADOW};',s,flags=re.I)
    for a,b in [('#dce8e6',SEA_T),('#a8432a',CORAL),('#1f6f78',SEA),('#14212e',INK),('#3a4652',BODY),('#5c6874',SOFT)]:
        s=re.sub(a,b,s,flags=re.I)
    s=re.sub(r'(font-family:'+re.escape(H)+r';[^"]*?font-weight:)700',r'\g<1>600',s)
    return s
ICON={'fonti':'book','verifica':'check','l01':'hull','l02':'propeller','l03':'map','l04':'anchor','l05':'lantern','l06':'lighthouse','l07':'cloud','l08':'sail','l09':'lifebuoy',
      'l10':'dividers','l11':'fuel','l12':'wind','l13':'current','l14':'current','l15':'map'}
def transform(i,n):
    s=src(i); m=HDR.search(s); assert m, i
    eb, ti = m.group(1), m.group(2)
    color = TEAL if (i.startswith('l1') and i!='l1') or 'color:#1f6f78' in m.group(0).lower() else ACC
    k=s.lower().find('aria-label="logo fabrizio fiorucci"'); k=s.rfind('<svg',0,k)
    mid=restyle(s[m.end():k])
    return section(i,n,header(eb,ti,ICON[i],SEA if color==TEAL else None)+mid,notes_of(s))

out={}
# ---------- COVER ----------
ill=(f'<rect x="0" y="236" width="712" height="84" fill="#7FB8BF" fill-opacity="0.16"/>'
     +''.join(f'<path d="M{-40+j*30} {250+j*22} '+' '.join('q27 -9 54 0 t54 0' for _ in range(8))+f'" fill="none" stroke="#7FB8BF" stroke-opacity="{0.7-j*0.2}" stroke-width="4" stroke-linecap="round"/>' for j in range(3))
     +f'<path d="M560 214 L690 206 Q700 218 684 232 L570 236 Z" fill="{DSOFT}" fill-opacity="0.55"/><path d="M596 206 L650 203 L640 190 L604 191 Z" fill="{DSOFT}" fill-opacity="0.55"/>'
     +f'<path d="M250 222 L540 222 Q526 254 494 262 L290 262 Q264 254 250 222 Z" fill="{PAPER}"/>'
     +f'<path d="M398 222 L398 10" stroke="{PAPER}" stroke-width="6" stroke-linecap="round"/><path d="M392 22 L392 212 L262 212 Q320 110 392 22 Z" fill="{DACC}"/>'
     +f'<path d="M406 44 L406 212 L520 212 Q470 120 406 44 Z" fill="{PAPER}" fill-opacity="0.85"/><path d="M398 10 L430 18 L398 26 Z" fill="{DACC}"/>')
cov=src('cover')
out['cover']=(f'<section id="cover" data-transition="fade" style="background:{NAVY}; color:{PAPER}; font-family:{B}; padding:128px; display:flex; flex-direction:column; justify-content:space-between">\n{backdrop(True)}\n'
 f'{lockup(True,112)}\n<div style="display:flex; flex-direction:column; gap:16px">'
 f'<p style="font-family:{HAND}; font-size:48px; font-weight:700; line-height:1.1; color:{DACC}">Corso · Categoria A · Vela e motore</p>'
 f'<h1 style="font-family:{H}; font-size:88px; font-weight:600; line-height:1.1; color:{PAPER}">Patente nautica Vela/Motore<br>senza limiti dalla costa</h1>'
 f'{wave(DACC,330)}<p style="font-size:36px; line-height:1.4; color:{DSOFT}; width:1000px">Indice del corso: 15 lezioni da 2 ore, allineate al programma ministeriale</p></div>\n'
 f'<div style="display:flex; gap:24px">'+''.join(f'<p style="font-size:28px; color:{PAPER}; background:rgba(245,241,232,0.10); padding:10px 22px; border-radius:40px"><b>{a}</b> {b}</p>' for a,b in [('9','lezioni di teoria e vela'),('6','lezioni di carteggio'),('135','esercizi d\'esame')])+'</div>\n'
 f'<svg aria-label="Illustrazione: barca a vela e motoscafo sul mare con sole, nuvole e gabbiani" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 300" width="560" height="300" style="position:absolute; left:1232px; top:620px; width:560px; height:300px">{sea_scene(560,300)}</svg>\n'
 f'<aside>{notes_of(cov)}</aside>\n</section>\n')

# ---------- ESAME ----------
def station(icon,name,comp,pass_,time,color):
    return card(f'<div style="display:flex; gap:16px; align-items:center">{badge(icon,color,76)}<p style="font-family:{HAND}; font-size:36px; font-weight:700; color:{color}">{time}</p></div>'
                +h3(name,32)+p(comp,24)+f'<p style="font-size:24px; line-height:1.35; font-weight:700; color:{INK}; background:{PAPER}; padding:8px 14px; border-radius:14px">Per superarla: {pass_}</p>',CARD,28,14)
arr=lambda: f'<svg aria-label="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40" style="width:40px; height:40px; flex:none; align-self:center"><path d="M4 20 L30 20 M20 10 L32 20 L20 30" fill="none" stroke="{ACC}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
st=[('dividers','Prova di carteggio','4 esercizi su carta 5/D o 42/D','almeno 3 su 4','60 minuti',SEA),('quiz','Quiz base','20 quesiti, 3 risposte, una esatta','massimo 4 errori','30 minuti',CORAL),('sail','Quiz vela','5 quesiti a risposta singola','massimo 1 errore','15 minuti',PURPLE),('helm','Prova pratica','Manovre a motore e a vela','giudizio della commissione','altro giorno',BLUE)]
row=arr().join(station(*x) for x in st)
nts=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px">{note(a,ACC,34)}<p style="font-size:24px; line-height:1.4; color:{BODY}">{b}</p></div>' for a,b in [('Il carteggio apre l\'esame','ed è propedeutico al resto della prova scritta.'),('Carte 5/D e 42/D integre','senza segni: si consegnano alla commissione all\'appello.'),('Quiz base e vela insieme','in un blocco unico da 45 minuti; risposta omessa = errata.')])
out['esame']=('esame',header('Com\'è fatto l\'esame · DM 323/2021, artt. 3 e 6','Tre prove scritte, poi la pratica','check')+f'<div style="display:flex; gap:12px; align-items:stretch">{row}</div><div style="display:flex; gap:40px">{nts}</div>',notes_of(src('esame')))

# ---------- STRUTTURA ----------
L=[('Teoria dello scafo','hull'),('Motori, elica e timone','propeller'),('Ormeggi, cartografia e primi calcoli','map'),('Ancoraggio, prora e rotta','anchor'),('Punto nave e fanali','lantern'),('Segnalamento, segnali sonori e sicurezza','lighthouse'),('Meteorologia e normativa','cloud'),('Vela','sail'),('Emergenze, ripasso vela e correnti','lifebuoy'),
   ('Carteggio: navigazione costiera','dividers'),('Carteggio: carburante','fuel'),('Carteggio: scarroccio','wind'),('Carteggio: correnti I','current'),('Carteggio: correnti II','current'),('Carteggio: carta 42/D','map')]
cells=''
for k,(t,ic) in enumerate(L):
    c = HUES[k%5] if k<9 else SEA; bg = TINTS[k%6] if k<9 else SEA_T
    cells+=(f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:{RADIUS}px">'
            f'<div style="display:flex; align-items:center; justify-content:space-between"><p style="font-family:{H}; font-size:40px; font-weight:600; color:{c}">{k+1:02d}</p>{badge(ic,c,52)}</div>'
            f'<p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{t}</p></div>')
out['struttura']=('struttura',header('30 ore · 9 di teoria e vela + 6 di carteggio','Le quindici lezioni','grid')+f'<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:16px">{cells}</div>',notes_of(src('struttura')))

# ---------- PESI (grafico a barre) ----------
rowsP=[('Navigazione cartografica ed elettronica',4,322,'03-05 · 09'),('Manovre e condotta',4,155,'03 · 04'),('Sicurezza della navigazione',3,215,'06 · 09'),('Normativa diportistica e ambientale',3,184,'07'),('COLREG e segnalamento marittimo',2,247,'05 · 06'),('Meteorologia',2,120,'07'),('Teoria dello scafo',1,125,'01 · 02'),('Motori',1,104,'02')]
def prow(t,e,n,l,vela=False):
    w=round(n/322*560); bg=f' background:{CARD}; border-radius:14px; padding:6px 12px;' if vela else ' padding:6px 12px;'
    return (f'<div style="display:flex; align-items:center; gap:24px;{bg} border-bottom:1px solid #D8D0BE">'
            f'<p style="width:540px; font-size:24px; line-height:1.3; font-weight:{800 if vela else 600}; color:{INK}">{t}</p>'
            f'<div style="flex:1; display:flex; align-items:center; gap:12px"><div style="width:{w}px; height:28px; background:{CH1}; border-radius:0px 4px 4px 0px"></div><p style="font-size:24px; font-weight:700; color:{INK}">{n}</p></div>'
            f'<p style="width:180px; font-size:24px; color:{BODY}"><b style="color:{INK}">{e}</b> {"quiz vela" if vela else "su 20"}</p>'
            f'<p style="width:150px; font-size:24px; color:{BODY}; text-align:right">{l}</p></div>')
hdrrow=(f'<div style="display:flex; gap:24px; padding:0px 12px"><p style="width:540px; font-size:24px; font-weight:800; color:{SOFT}">Tema (All. C, DM 323/2021)</p><p style="flex:1; font-size:24px; font-weight:800; color:{SOFT}">Quiz ufficiali nell\'elenco</p>'
        f'<p style="width:180px; font-size:24px; font-weight:800; color:{SOFT}">All\'esame</p><p style="width:150px; font-size:24px; font-weight:800; color:{SOFT}; text-align:right">Lezione</p></div>')
bars=hdrrow+''.join(prow(*r) for r in rowsP)+prow('Quiz vela · prova separata',5,250,'08 · 09',True)
out['pesi']=('pesi',header('Quiz base: 20 quesiti per tema','Il tempo di ogni lezione segue il peso d\'esame','chart')+f'<div style="display:flex; flex-direction:column; gap:4px">{bars}</div>'
 +p('<b>All\'esame</b>: domande del tema nella scheda d\'esame. <b>Quiz ufficiali</b>: domande del tema nell\'elenco del Ministero (DD 131/2022), da cui vengono estratte. Le barre sono lunghe in proporzione ai quiz ufficiali.',24,SOFT),notes_of(src('pesi')))

# ---------- CARTEGGIO (barre impilate) ----------
U=15.5
def seg(n,c,last):
    if n==0: return ''
    r='0px 4px 4px 0px' if last else '0px'
    return f'<div style="width:{round(n*U)}px; height:52px; background:{c}; border-radius:{r}; display:flex; align-items:center; justify-content:center"><p style="font-size:26px; font-weight:800; color:#FFFFFF">{n}</p></div>'
def krow(t,a,b,l):
    extra = f'<p style="font-size:24px; color:{SOFT}">solo 5/D</p>' if b==0 else ''
    return (f'<div style="display:flex; align-items:center; gap:24px; border-bottom:1px solid #D8D0BE; padding:8px 0px">'
            f'<p style="width:330px; font-size:26px; font-weight:700; color:{INK}">{t}</p>'
            f'<div style="flex:1; display:flex; align-items:center; gap:2px">{seg(a,CH1,b==0)}{seg(b,CH2,True)}<div style="width:14px"></div><p style="font-size:26px; font-weight:800; color:{INK}">{a+b}</p><div style="width:10px"></div>{extra}</div>'
            f'<p style="width:220px; font-size:24px; color:{BODY}; text-align:right">lez. {l}</p></div>')
leg=(f'<div style="display:flex; gap:40px; align-items:center"><div style="display:flex; gap:12px; align-items:center"><div style="width:28px; height:28px; background:{CH1}; border-radius:6px"></div><p style="font-size:24px; font-weight:700; color:{INK}">Carta 5/D · Elba, Pianosa, Giglio, Argentario</p></div>'
     f'<div style="display:flex; gap:12px; align-items:center"><div style="width:28px; height:28px; background:{CH2}; border-radius:6px"></div><p style="font-size:24px; font-weight:700; color:{INK}">Carta 42/D · Bocche di Bonifacio</p></div></div>')
kb=leg+'<div style="display:flex; flex-direction:column; gap:4px">'+krow('Correnti',39,13,'13 · 14 · 15')+krow('Navigazione costiera',26,10,'10 · 15')+krow('Scarroccio',20,4,'12')+krow('Carburante',23,0,'11')+'</div>'
kb+=f'<div style="display:flex; gap:24px; align-items:center"><p style="font-family:{H}; font-size:72px; font-weight:600; color:{INK}">135</p>{note("esercizi ufficiali: 108 sulla 5/D e 27 sulla 42/D, tutti svolti in aula",ACC,38)}</div>'
out['carteggio']=('carteggio',header('Lezioni 10-15 · DD 131/2022','I 135 esercizi di carteggio, tutti in aula','dividers',TEAL)+kb,notes_of(src('carteggio')))

# ---------- METODO ----------
steps=[('book','Traccia','Il testo ministeriale, parola per parola, con carta e settore.'),('pencil','Soluzione','Conversioni di prora, triangolo delle velocità, calcoli di tempo, spazio e consumo.'),('dividers','Tracciamento','La sequenza di linee e punti sulla carta 5/D o 42/D, con gli orari.'),('check','Verifica','Il confronto con la risposta ufficiale e il suo intervallo di tolleranza.')]
stc=''.join(card(f'<div style="display:flex; gap:14px; align-items:center">{badge(ic,TEAL,76)}<p style="font-family:{HAND}; font-size:56px; font-weight:700; color:{TEAL}">{k+1}.</p></div>'+h3(a,34)+p(b,24),TEALCARD,30,14) for k,(ic,a,b) in enumerate(steps))
out['metodo']=('metodo',header('Il metodo di ogni esercizio','Traccia, soluzione, tracciamento, verifica','pencil',TEAL)+f'<div style="display:flex; gap:24px">{stc}</div>'
 +card(note('Esempio 5.1.3-1',TEAL,36)+p('Pb 350°, d 1°E, Vp 9 kn, faro di Punta Polveraia a Rilb 075° alle 12h00 e 125° alle 12h20. Risposta ufficiale: Lat 42°49\',7-42°50\',3 N, Long 010°02\',0-010°02\',6 E.',24,INK),PAPER,24,6,flex='none',extra='; border:3px dashed #0B8A99'),notes_of(src('metodo')))

# ---------- PROSSIMI ----------
items=['Lezione 01 · Teoria dello scafo: pronta, 29 slide con disegni e quiz','Lezioni 02-09: slide con disegni, schemi e quiz ufficiali con risposte','Dispense 10-15: traccia, soluzione e tracciamento per tutti i 135 esercizi','Prova simulata finale: 4 esercizi di carteggio, quiz base e quiz vela']
ul=''.join(f'<li>{x}</li>' for x in items)
out['prossimi']=('prossimi',header('Prossimi passi','Dall\'indice ai materiali del corso','flag',ACC,True)+f'<ul style="font-size:30px; line-height:1.45; color:{DSOFT}; display:flex; flex-direction:column; gap:18px; width:1500px">{ul}</ul>','',True)

for n,i in enumerate(order,1):
    if i=='cover': html=out['cover']
    elif i in out:
        v=out[i]; html=section(i,n,v[1],v[2],dark=(len(v)>3 and v[3]))
    else: html=transform(i,n)
    open(f'{OUT}/slides/{i}.html','w').write(html)
deck['faces']=FACES
json.dump(deck,open(OUT+'/deck.json','w'),ensure_ascii=False,indent=1)
for i in order:
    h=open(f'{OUT}/slides/{i}.html').read()
    ne=len(re.findall(r'<(?!/)[a-z]',h)); 
    if ne>200: print('MANY',i,ne)
    if 'Libre Baskerville' in h or 'Public Sans' in h: print('OLDFONT',i)
print('ok',len(order))
