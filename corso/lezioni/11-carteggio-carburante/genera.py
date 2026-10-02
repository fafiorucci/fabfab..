import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
from lezione_base import *
import lezione_base as LB
import geo, chart, es10, es11
OUT=SP+'/lez11/project'
GREY='#97A6B4'; LRED='#E23B3B'; ORANGE='#F28C28'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Il conto del carburante':'fuel','Il doppio rilevamento 45°-90°':'lighthouse','La velocità dalla carta':'dividers',
 'Un punto da rilevamento e distanza':'lighthouse','Un esempio completo':'fuel','I punti cospicui di oggi':'map','La traccia':'map','Il tracciamento':'dividers'})
def pcol(inner,w=532,gap=20,left=1260,top=290): return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
X,Y,W,Hh=700,290,1092,620

def chart_html(S, x, y, w, h, solution, alt):
    body,labels,glabs,sbl,C=chart.render(S,w,h,solution)
    svg=f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px">{body}</svg>'
    html=''
    for kind,v,t in glabs:
        if kind=='lat' and 30<v<h-40: html+=lab(x+10,y+v-30,130,t,'#5E6E82',20,800)
    lastx=-999
    for kind,v,t in glabs:
        if kind=='lon' and 60<v<w-230 and v-lastx>150: html+=lab(x+v+6,y+h-34,140,t,'#5E6E82',20,800); lastx=v
    sx,sy,L,t=sbl; html+=lab(x+sx,y+sy,max(L,120),t,'#16324F',20,900)
    for lx,ly,lw,t,c,kind in chart.place_labels(labels,w,h,22):
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px; white-space:nowrap">{t}</p>'
    return svg+html

# ============ COVER + AGENDA ============
cover(11,'Carteggio: carburante e autonomia','Quanta nafta serve? Distanze sulla carta, velocità dal doppio rilevamento e il 30% di riserva: i 23 esercizi ufficiali della carta 5/D',
 'Lezione 11. Esercizi ufficiali 5.1.2, 5.2.2, 5.3.2 e 5.4.2 dell\'Allegato A al DD 131/2022 (carta 5/D). Tutti chiedono il carburante con la riserva: il 30% salvo diversa indicazione (quiz 1.2.3-1). Carte ridisegnate da OpenStreetMap per spiegare il tracciamento; all\'esame si lavora sulla carta 5/D.')
blocks=[('0:00','25′','Il conto, il 45°-90° e la velocità dalla carta',CORAL),('0:25','25′','Settore A · Elba (5 esercizi)',SEA),('0:50','20′','Settore B · Castiglione (5)',PURPLE),('1:10','25′','Settore C · Pianosa e Montecristo (7)',BLUE),('1:35','25′','Settore D · Giglio e Argentario (6)',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("La formula")+f'<p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1.1; color:{INK}">d ÷ V × c × 1,3</p>'+p('miglia diviso nodi, per litri all\'ora, più il 30% di riserva',26,INK,700))
left=card(tag('Leggi bene la traccia',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>da dove parte il conto: dalla partenza o dal punto nave?</li><li>fin dove arriva: destinazione, traverso, ritorno?</li><li>la velocità è data o va ricavata?</li><li>la riserva è del 30% o di un altro valore?</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 11 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Come nella lezione 10: per ogni esercizio una slide con la traccia e una con il tracciamento. Quasi tutti combinano un punto nave con il doppio rilevamento polare 45°-90° e il calcolo del carburante.')

# ============ IL CONTO ============
K=[('t = d ÷ V','Il tempo in ore: miglia diviso nodi. 16,2 mg a 6 kn = 2,7 ore.',CORAL,CORAL_T),
   ('c = t × consumo','Litri: ore per litri all\'ora. 2,7 h × 4 l/h = 10,8 litri.',SEA,SEA_T),
   ('× 1,3','La riserva del 30%, se la traccia non ne indica un\'altra. 10,8 × 1,3 = 14,0 litri.',PURPLE,LILAC_T),
   ('minuti ÷ 60','18 minuti = 0,3 ore; 25 minuti = 0,42 ore. Mai sommare ore e minuti come decimali.',BLUE,BLUE_T),
   ('Tutte le tratte','Somma le miglia di ogni tratto richiesto; andata e ritorno contano due volte.',GREEN,GREEN_T),
   ('Senza vento né corrente','La velocità sul fondo è la Vp e la rotta coincide con la prora.',ORANGE,SUN_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:28px; border-radius:28px"><p style="font-family:{H}; font-size:44px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in K)
sec('conto', head('Carteggio · il calcolo','Il conto del carburante')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:22px">{tiles}</div>',
 notes='Esempio del quiz 1.2.2-2: 10 mg a 5 kn = 2 ore; 2 × 50 = 100 litri; con il 30% = 130 litri. Esempio 5.1.2-3 (in questa lezione): 16,2 mg a 6 kn, 4 l/h: 14,0 litri con la riserva.')

# ============ 45-90 ============
def t4590(kind):
    b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/>'
    b+=f'<path d="M700 0 Q760 90 840 120 Q900 150 1092 150 L1092 0 Z" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/>'
    Lx,Ly=820,120
    b+=f'<circle cx="{Lx}" cy="{Ly}" r="13" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    yc=450; P45=(Lx-330,yc); P90=(Lx,yc)
    b+=line(60,yc,1040,yc,GREEN,5)+arrow(900,yc,1040,yc,GREEN,5,20)
    b+=line(P45[0],P45[1],Lx,Ly,NAVY,3)+line(P90[0],P90[1],Lx,Ly,CORAL,4)
    b+=f'<circle cx="{P45[0]}" cy="{yc}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="{P90[0]}" cy="{yc}" r="15" fill="none" stroke="{CORAL}" stroke-width="5"/>'
    b+=f'<path d="M{P45[0]+60} {yc} A60 60 0 0 0 {P45[0]+60*math.cos(math.radians(45)):.0f} {yc-60*math.sin(math.radians(45)):.0f}" fill="none" stroke="{PURPLE}" stroke-width="4"/><path d="M{Lx-30} {yc} L{Lx-30} {yc-30} L{Lx} {yc-30}" fill="none" stroke="{PURPLE}" stroke-width="3"/>'
    b+=line(P45[0],yc+40,P90[0],yc+40,PURPLE,3)+line(Lx+40,Ly,Lx+40,yc,PURPLE,3)
    if kind=='vel':
        b+=f'<circle cx="120" cy="{yc}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    L=[(P45[0]-110,yc-80,'ρ 45°',PURPLE),(P90[0]+24,yc+20,'ρ 90°: al traverso',CORAL),(P45[0]+80,yc+52,'cammino = Vp × t',PURPLE),(Lx+56,280,'distanza al traverso',PURPLE),(Lx-230,Ly-40,'faro',NAVY),(80,yc-50,'rotta',GREEN)]
    if kind=='vel': L=[(P45[0]-110,yc-80,'ρ 45°',PURPLE),(P90[0]+24,yc+20,'traverso: piede della perpendicolare',CORAL),(P45[0]+60,yc+52,'stessa lunghezza',PURPLE),(Lx+56,280,'la misuri col compasso',PURPLE),(Lx-230,Ly-40,'faro',NAVY),(90,yc+20,'A',INK)]
    return b,L
def tslide(id_,kind,title,txt,notes,left):
    b,L=t4590(kind); x=128 if left else 700
    lbl=''.join(pill(x+lx,Y+ly,440,t,c,22) for lx,ly,t,c in L)
    pinned=svgp(x,Y,W,Hh,b,title)+lbl
    if left: sec(id_,head('Carteggio · le tecniche',title),pinned=pinned+pcol(txt),notes=notes)
    else: sec(id_,head('Carteggio · le tecniche',title)+col(txt),pinned=pinned,notes=notes)
tslide('t4590','base','Il doppio rilevamento 45°-90°',
 term('Il trucco','Rilevi il faro a 45° dalla prora e poi al traverso (90°): il triangolo ha due angoli di 45°, è isoscele.')+term('La conseguenza','La distanza dal faro al traverso è uguale al cammino fatto tra i due rilevamenti: Vp × t.')+term('Il punto','Al traverso: dal faro, sul rilevamento vero (Pv ± 90°), riporta quella distanza.'),
 'Rilevamento polare ρ: + a dritta, − a sinistra. Rilv al traverso = Pv + ρ. Esempio 5.1.2-2: Pv 070°, Scoglietto a ρ +90° → Rilv 160°; in 20 minuti a 6 kn il cammino è 2 mg, quindi il punto nave è 2 mg dal faro sul 160°.',False)
tslide('tvel','vel','La velocità dalla carta',
 term('Quando la Vp non c\'è','Conosci il punto di partenza e la rotta: la barca sta su quella linea.')+term('Il traverso','Dal faro traccia la perpendicolare alla rotta: il piede è il punto al traverso. Misura la distanza faro-traverso.')+term('La velocità','Quella distanza è il cammino tra i due rilevamenti: V = distanza ÷ tempo. Poi il conto del carburante.'),
 'Esercizi 5.2.2-5, 5.3.2-3, -4, -5, -6, 5.4.2-2, -3, -4. La velocità ricavata va misurata con cura: 0,1 mg di differenza sulla distanza al traverso cambiano il carburante del 3-4%.',True)

# ============ RILEVAMENTO E DISTANZA ============
def rd():
    b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/><circle cx="700" cy="300" r="60" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/><circle cx="700" cy="300" r="12" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    b+=f'<circle cx="700" cy="300" r="250" fill="none" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="10 8"/>'
    B=(450,300); b+=line(B[0],B[1],700,300,CORAL,4)+arrow(560,300,690,300,CORAL,4,16)+f'<circle cx="{B[0]}" cy="{B[1]}" r="15" fill="none" stroke="{CORAL}" stroke-width="5"/>'
    A=(120,520); b+=arrow(A[0],A[1],B[0]-14,B[1]+10,GREEN,5,20)+f'<circle cx="{A[0]}" cy="{A[1]}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    L=[(500,250,'Rilv 090° del faro',CORAL),(760,460,'3,5 mg',PURPLE),(B[0]-120,B[1]-70,'B',CORAL),(A[0]-40,A[1]+20,'A',INK),(740,240,'faro',NAVY)]
    return b,L
b,L=rd()
sec('rildist', head('Carteggio · le tecniche','Un punto da rilevamento e distanza'), pinned=svgp(128,Y,W,Hh,b,'Il punto B è sul rilevamento vero del faro alla distanza data: si traccia il rilevamento dal faro al contrario e si prende la distanza con il compasso')+''.join(pill(128+lx,Y+ly,440,t,c,22) for lx,ly,t,c in L)+pcol(
 term('Il testo','«Distanza 3,5 miglia sul rilevamento vero 270° del faro»: dalla barca vedi il faro per 270°.')+term('Sulla carta','Dal faro traccia la direzione opposta (270° − 180° = 090°) e prendi la distanza con il compasso sulla scala delle latitudini.')+term('Attenzione','«A est del faro» e «il faro per 270°» sono la stessa cosa. Leggi sempre da chi a chi.')),
 notes='Esercizi 5.3.2-1 (Monte della Fortezza per Rilv 180° a 2,8 mg: il punto è a nord), 5.3.2-7 (Scoglio d\'Africa per Rilv 270° a 3,5 mg: il punto è a est), 5.4.2-1 (torre di Capo d\'Uomo per Rilv nord a 1 mg: il punto è a sud). Richiamo: quiz 1.7.6-16, -21, -26 della lezione 10.')

quiz_slide('quiz1','Quiz · Carburante e autonomia',['1.2.3-1','1.2.2-2','1.2.3-3'],False)
quiz_slide('quiz1r','Quiz · Le risposte',['1.2.3-1','1.2.2-2','1.2.3-3'],True)

# ============ MAPPA ============
M=es10.Sol('5.1.3-1',(42.62,10.55)); M.pts=[]; M.lines=[]
used={'Isola di Cerboli':'Cerboli',"Capo d'Ortano":"C. d'Ortano",'Punta Falcone':'P.ta Falcone','Punta del Nasuto':'P.ta del Nasuto','Porticciolo di Salivoli':'Salivoli','Punta di Fetovaia':'Fetovaia','Isola Corbelli':'Corbelli','Punta dei Ripalti':'P.ta dei Ripalti',
 'Faro dello Scoglietto':'Scoglietto','Faro di Capo Poro':'Capo Poro','Fanale di Carbonifera':'Carbonifera','Scoglio dello Sparviero':'Sparviero','Faro di Punta Ala':'Punta Ala','Fanali di Castiglione della Pescaia':'Castiglione',
 "Faro dell'Isola di Pianosa":'Pianosa','Punta Brigantina':'P.ta Brigantina','Punta del Libeccio':'P.ta del Libeccio',"Faro di Scoglio d'Africa":"Scoglio d'Africa",'Monte della Fortezza':'Montecristo',
 'Faro di Punta del Fenaio':'P.ta del Fenaio','Fanali del porto del Giglio':'Giglio Porto','Faro di Punta Lividonia':'P.ta Lividonia','Porto Santo Stefano':'P. S. Stefano','Porticciolo di Talamone':'Talamone','Faro di Formica Grande':'Formiche'}
for n,sh in used.items(): M.pts.append((geo.lm(n),sh,'lm'))
M.pts.append(((42.30,10.0),'','none')); M.pts.append(((42.97,11.2),'','none'))
sec('mappa', head('Carteggio · la carta','I punti cospicui di oggi'), pinned=chart_html(M,128,290,1664,620,True,'Carta schematica dall\'Elba all\'Argentario con i punti cospicui degli esercizi di carburante'),
 notes='Coste e punti da OpenStreetMap (© contributori OSM, ODbL). Alcuni punti (Punta del Nasuto, Punta dei Ripalti, il porticciolo di Salivoli) sono posizionati dal nome della località: sulla carta 5/D si usa il simbolo stampato.')

# ============ ESERCIZI ============
SETT={'5.1':('A','Elba',SEA),'5.2':('B','Castiglione e Punta Ala',PURPLE),'5.3':('C','Pianosa e Montecristo',BLUE),'5.4':('D','Giglio e Argentario',GREEN)}
order_ex=[]
def rng(r): return r.replace('\n',' ').replace('Carburante ','').replace('÷',' ÷ ')
for f in es11.SOLS:
    S=f(); sid='f'+S.id.replace('.','_').replace('-','_'); st=SETT[S.id[:3]]
    txt=S.ex['testo'].replace('\n',' ')
    fs=26 if len(txt)<520 else (24 if len(txt)<760 else 22)
    ask='il carburante necessario, compresa la riserva'
    left_col=f'<div style="display:flex; flex-direction:column; gap:20px; width:690px">{p(txt,fs,INK,500,1.45)}<p style="font-size:26px; font-weight:900; color:#FFFFFF; background:{st[2]}; padding:10px 20px; border-radius:18px">Da trovare: {ask}</p></div>'
    sec(sid+'_t', head(f'Esercizio {S.id} · settore {st[0]} · {st[1]}','La traccia',st[2])+left_col, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell\'esercizio {S.id}'),
        notes=f'Traccia ufficiale (Allegato A al DD 131/2022). Risposta ufficiale: {rng(S.ex["risposta_ufficiale"])}.')
    ol='<ol style="font-size:24px; line-height:1.38; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{x}</li>' for x in S.passi)+'</ol>'
    ok=S.check()
    extra='' if ok else f'<p style="font-size:22px; font-weight:600; color:{INK}">Scarto minimo: basta 0,1 mg in più o in meno sulla carta per rientrare.</p>'
    res=f'<div style="display:flex; flex-direction:column; gap:4px; background:{CORAL_T}; padding:16px 20px; border-radius:20px"><p style="font-size:30px; font-weight:900; color:{CORAL}">{S.res_txt}</p><p style="font-size:24px; font-weight:700; color:{INK}">Ufficiale: {rng(S.ex["risposta_ufficiale"])}</p>{extra}</div>'
    sec(sid+'_s', head(f'Esercizio {S.id} · soluzione','Il tracciamento',st[2]), pinned=chart_html(S,128,290,1092,620,True,f'Tracciamento dell\'esercizio {S.id}')+pcol(ol+res,532,14),
        notes='Soluzione: '+' '.join(S.passi)+f' Risultato: {S.res_txt}. Ufficiale: {rng(S.ex["risposta_ufficiale"])}.'+('' if ok else ' Il nostro calcolo, fatto con le coordinate OpenStreetMap, esce di poco dalla forchetta: la distanza al traverso o la posizione del punto di partenza misurate sulla carta 5/D la riportano dentro.'))
    order_ex+=[sid+'_t',sid+'_s']

closing(['Tempo = miglia ÷ nodi; carburante = tempo × consumo; poi +30%','Doppio rilevamento 45°-90°: distanza al traverso = cammino tra i due rilevamenti','Senza Vp: traverso = piede della perpendicolare, V = distanza ÷ tempo','«Il faro per 270° a 3,5 mg» vuol dire che sei 3,5 mg a est del faro','Somma tutte le tratte richieste, andata e ritorno comprese'],
 'Prossima lezione · 12 · Scarroccio','A casa: rifai sulla carta 5/D gli esercizi non svolti in aula.')
write_deck(OUT,'Lezione 11 · Carteggio: carburante e autonomia',
 ['cover','agenda','conto','t4590','tvel','rildist','quiz1','quiz1r','mappa']+order_ex+['chiusura'],
 {"s1":{"description":"Apertura, il conto e le tecniche","start":"cover"},"s2":{"description":"Settore A · Elba","start":"f5_1_2_1_t"},"s3":{"description":"Settore B · Castiglione e Punta Ala","start":"f5_2_2_1_t"},
  "s4":{"description":"Settore C · Pianosa e Montecristo","start":"f5_3_2_1_t"},"s5":{"description":"Settore D · Giglio e Argentario","start":"f5_4_2_1_t"}})
