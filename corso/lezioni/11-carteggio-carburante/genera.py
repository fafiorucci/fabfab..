import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
from lezione_base import *
import lezione_base as LB
import geo, chart, es10, es11
OUT=SP+'/lez11/project'
GREY='#97A6B4'; LRED='#E23B3B'; ORANGE='#F28C28'
LB.ICON_T.update({'Calcolo carburante e traverso':'fuel','Le famiglie d\'esame':'grid','Gli strumenti di base':'dividers','La lezione di oggi':'lifebuoy','Il conto del carburante':'fuel','Calcolo carburante e RilP 45°/90°':'lighthouse','RilP 45°/90° e velocità':'dividers',
 'Un punto da rilevamento e distanza':'lighthouse','Un esempio completo':'fuel','I punti cospicui di oggi':'map','La traccia':'map','Il tracciamento':'dividers'})
def pcol(inner,w=532,gap=20,left=1260,top=290): return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
X,Y,W,Hh=700,290,1092,620
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'famiglie.py')).read())

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
    for lx,ly,lw,t,c,kind in chart.place_labels(labels,w,h,22,[(sx-12,sy-8,max(L,120)+30,h-sy+8)]+[(4,v-32,150,32) for k_,v,_ in glabs if k_=='lat']+[(v,h-36,150,36) for k_,v,_ in glabs if k_=='lon'],C.segs,C.dots):
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px; white-space:nowrap">{t}</p>'
    return svg+html

# ============ COVER + AGENDA ============
cover(11,'Carteggio: carburante e autonomia','Quanta nafta serve? Distanze sulla carta, velocità dal doppio rilevamento e il 30% di riserva: i 23 esercizi ufficiali della carta 5/D',
 'Lezione 11. Esercizi ufficiali 5.1.2, 5.2.2, 5.3.2 e 5.4.2 dell\'Allegato A al DD 131/2022 (carta 5/D). Tutti chiedono il carburante con la riserva: il 30% salvo diversa indicazione (quiz 1.2.3-1). Carte ridisegnate da OpenStreetMap per spiegare il tracciamento; all\'esame si lavora sulla carta 5/D.')
blocks=[('0:00','20′','Il conto, il 45°-90° e la velocità dalla carta',CORAL),('0:20','15′','Settore A · Elba (5 esercizi)',SEA),('0:35','10′','Settore B · Castiglione (5)',PURPLE),('0:45','15′','Settore C · Pianosa (7)',BLUE),('1:00','15′','Settore D · Giglio (6)',GREEN),('1:15','45′','Raccolta quiz (36)',ORANGE)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("La formula")+f'<p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1.1; color:{INK}">d ÷ V × c × 1,3</p>'+p('miglia diviso nodi, per litri all\'ora, più il 30% di riserva',26,INK,700))
left=card(tag('Leggi bene la traccia',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>da dove parte il conto: dalla partenza o dal punto nave?</li><li>fin dove arriva: destinazione, traverso, ritorno?</li><li>la velocità è data o va ricavata?</li><li>la riserva è del 30% o di un altro valore?</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 11 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Cinque capitoli in 75 minuti, ognuno chiuso da una verifica da 2 quiz ufficiali; negli ultimi 45 minuti la raccolta di 36 quiz su autonomia, navigazione stimata e coordinate (1.2.3, 1.7.5, 1.7.1). Come nella lezione 10: per ogni esercizio una slide con la traccia e una con il tracciamento. Quasi tutti combinano un punto nave con il doppio rilevamento polare 45°-90° e il calcolo del carburante.')

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
tslide('t4590','base','Calcolo carburante e RilP 45°/90°',
 term('Il trucco','Rilevi il faro a 45° dalla prora e poi al traverso (90°): il triangolo ha due angoli di 45°, è isoscele.')+term('La conseguenza','La distanza dal faro al traverso è uguale al cammino fatto tra i due rilevamenti: Vp × t.')+term('Il punto','Al traverso: dal faro, sul rilevamento vero (Pv ± 90°), riporta quella distanza.'),
 'Rilevamento polare ρ: + a dritta, − a sinistra. Rilv al traverso = Pv + ρ. Esempio 5.1.2-2: Pv 070°, Scoglietto a ρ +90° → Rilv 160°; in 20 minuti a 6 kn il cammino è 2 mg, quindi il punto nave è 2 mg dal faro sul 160°.',False)
tslide('tvel','vel','RilP 45°/90° e velocità',
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


# ============ CARBURANTE E TRAVERSO ============
def travd():
    b='<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/><path d="M0 120 Q120 180 160 300 Q190 420 120 620 L0 620 Z" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/>'
    F=(150,330); R=(560,60); A=(560,330); B=(980,560)
    b+=f'<circle cx="{F[0]}" cy="{F[1]}" r="13" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    b+=arrow(R[0],R[1],A[0],A[1]-14,GREEN,6,20)+arrow(A[0],A[1],B[0],B[1],SEA,6,20)+dash(F[0],F[1],A[0],A[1],CORAL,4)
    b+=f'<path d="M{A[0]-26} {A[1]} L{A[0]-26} {A[1]-26} L{A[0]} {A[1]-26}" fill="none" stroke="{CORAL}" stroke-width="3"/>'
    b+=''.join(f'<circle cx="{q[0]}" cy="{q[1]}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>' for q in (R,B))+f'<circle cx="{A[0]}" cy="{A[1]}" r="15" fill="none" stroke="{CORAL}" stroke-width="5"/>'
    L=[(R[0]+20,R[1]-10,'partenza · Rv 180°',GREEN),(F[0]-40,F[1]+30,'faro',NAVY),(260,280,'4,9 mg · Rilv = Rv ± 90°',CORAL),(A[0]+26,A[1]-10,'A: al traverso',CORAL),(B[0]-140,B[1]-60,'B',SEA),(700,400,'seconda tratta',SEA)]
    return b,L
b,L=travd()
sec('trav', head('Carteggio · le tecniche','Calcolo carburante e traverso')+col(
 term('Quando','La traccia dice «si rileva il faro al traverso a 4,9 miglia» (5.1.2-1) o «fino al traverso del faro» (5.4.2-1).')+
 term('Il punto al traverso','Al traverso il faro è a 90° dalla prora: dal faro traccia la perpendicolare alla rotta. Dove la taglia c\'è il punto; se è data la distanza, la misuri col compasso dal faro.')+
 term('Il conto','Somma le tratte (partenza → traverso → arrivo), t = miglia ÷ V, litri = t × consumo × 1,3. 5.1.2-1: 3,5 + 8,2 = 11,8 mg a 6 kn, 12 l/h: 30,6 litri.')),
 pinned=svgp(X,Y,W,Hh,b,'La rotta passa al traverso del faro: il punto A è il piede della perpendicolare dal faro alla rotta')+''.join(pill(X+lx,Y+ly,440,t,c,22) for lx,ly,t,c in L),
 notes='Famiglia d\'esame «Calcolo carburante e traverso»: 5.1.2-1 (Cerboli, Rv 180°, Capo d\'Ortano al traverso di dritta a 4,9 mg: A è 4,9 mg a est del capo; ufficiale 29-31 litri) e 5.4.2-1 (da Capo d\'Uomo verso Giglio Porto a 20 kn, fino al traverso di Punta Lividonia: 5,0 mg, 21,0 litri; ufficiale 19,5-21,5).')

basi_slide('basi',[('Carburante','Litri = ore × consumo orario, più la riserva del 30% (× 1,3) se la traccia non dice altro.')])
famiglie_slide('famiglie',['Calcolo carburante','Calcolo carburante e traverso','Calcolo carburante e RilP 45°/90°','Calcolo carburante e RilP 45°/90° e velocità'],
 where={'Calcolo carburante':'Il conto · Rilevamento e distanza','Calcolo carburante e traverso':'Carburante e traverso','Calcolo carburante e RilP 45°/90°':'RilP 45°/90°','Calcolo carburante e RilP 45°/90° e velocità':'RilP 45°/90° e velocità'})

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
order_ex=[]; exs={}
def rng(r): return r.replace('\n',' ').replace('Carburante ','').replace('÷',' ÷ ')
for f in es11.SOLS:
    S=f(); sid='f'+S.id.replace('.','_').replace('-','_'); st=SETT[S.id[:3]]
    txt=S.ex['testo'].replace('\n',' ')
    fs=26 if len(txt)<520 else (24 if len(txt)<760 else 22)
    ask='il carburante necessario, compresa la riserva'
    fam=CAT[S.id]
    left_col=f'<div style="display:flex; flex-direction:column; gap:20px; width:690px"><p style="font-size:24px; font-weight:900; color:{st[2]}">Famiglia d\'esame · {fam}</p>{p(txt,fs,INK,500,1.45)}<p style="font-size:26px; font-weight:900; color:#FFFFFF; background:{st[2]}; padding:10px 20px; border-radius:18px">Da trovare: {ask}</p></div>'
    sec(sid+'_t', head(f'Esercizio {S.id} · settore {st[0]} · {st[1]}','La traccia',st[2])+left_col, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell\'esercizio {S.id}'),
        notes=f'Traccia ufficiale (Allegato A al DD 131/2022). Risposta ufficiale: {rng(S.ex["risposta_ufficiale"])}.')
    ol='<ol style="font-size:24px; line-height:1.38; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{x}</li>' for x in S.passi)+'</ol>'
    ok=S.check()
    extra='' if ok else f'<p style="font-size:22px; font-weight:600; color:{INK}">Scarto minimo: basta 0,1 mg in più o in meno sulla carta per rientrare.</p>'
    res=f'<div style="display:flex; flex-direction:column; gap:4px; background:{CORAL_T}; padding:16px 20px; border-radius:20px"><p style="font-size:30px; font-weight:900; color:{CORAL}">{S.res_txt}</p><p style="font-size:24px; font-weight:700; color:{INK}">Ufficiale: {rng(S.ex["risposta_ufficiale"])}</p>{extra}</div>'
    sec(sid+'_s', head(f'{S.id} · {fam}','Il tracciamento',st[2]), pinned=chart_html(S,128,290,1092,620,True,f'Tracciamento dell\'esercizio {S.id}')+pcol(ol+res,532,14),
        notes='Soluzione: '+' '.join(S.passi)+f' Risultato: {S.res_txt}. Ufficiale: {rng(S.ex["risposta_ufficiale"])}.'+('' if ok else ' Il nostro calcolo, fatto con le coordinate OpenStreetMap, esce di poco dalla forchetta: la distanza al traverso o la posizione del punto di partenza misurate sulla carta 5/D la riportano dentro.'))
    order_ex+=[sid+'_t',sid+'_s']; exs.setdefault(st[0],[]).append((S.id,sid+'_t',fam))

closing(['Tempo = miglia ÷ nodi; carburante = tempo × consumo; poi +30%','Doppio rilevamento 45°-90°: distanza al traverso = cammino tra i due rilevamenti','Senza Vp: traverso = piede della perpendicolare, V = distanza ÷ tempo','«Il faro per 270° a 3,5 mg» vuol dire che sei 3,5 mg a est del faro','Somma tutte le tratte richieste, andata e ritorno comprese'],
 'Prossima lezione · 12 · Scarroccio','A casa: rifai sulla carta 5/D gli esercizi non svolti in aula.')
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'apertura.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'esame.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'schema_cart.py')).read())
def sett(k,t,c,mins): return ('cap'+str('ABCD'.index(k)+2),t,[f'{e} · {fm}' for e,_,fm in exs[k]],c,mins,exs[k][0][1],(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
CAPS=[('cap1','Il conto e le tecniche',['Gli strumenti di base','Le famiglie d\'esame','Il conto del carburante','Calcolo carburante e RilP 45°/90°','RilP 45°/90° e velocità','Calcolo carburante e traverso','Un punto da rilevamento e distanza','I punti cospicui di oggi'],CORAL,20,'basi',(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata')),
 sett('A','Settore A · Elba',SEA,15),sett('B','Settore B · Castiglione e Punta Ala',PURPLE,10),sett('C','Settore C · Pianosa e Montecristo',BLUE,15),sett('D','Settore D · Giglio e Argentario',GREEN,15)]
VER=[['1.2.3-1', '1.2.3-2'], ['1.7.5-3', '1.7.5-4'], ['1.2.3-4', '1.2.3-5'], ['1.7.5-5', '1.7.5-8'], ['1.7.1-2', '1.7.1-6']]
RACC=[('1.2.3', ['1.2.3-3', '1.2.3-7', '1.2.3-18']), ('1.2.3', ['1.2.3-6', '1.2.3-9', '1.2.3-19']), ('1.7.5', ['1.7.5-9', '1.7.5-22', '1.7.5-32']), ('1.7.5', ['1.7.5-10', '1.7.5-23', '1.7.5-33']), ('1.7.5', ['1.7.5-11', '1.7.5-24', '1.7.5-34']), ('1.7.5', ['1.7.5-12', '1.7.5-25', '1.7.5-36']), ('1.7.5', ['1.7.5-13', '1.7.5-26', '1.7.5-37']), ('1.7.5', ['1.7.5-19', '1.7.5-28', '1.7.5-40']), ('1.7.5', ['1.7.5-21', '1.7.5-29', '1.7.5-50']), ('1.7.1', ['1.7.1-7', '1.7.1-11', '1.7.1-18']), ('1.7.1', ['1.7.1-8', '1.7.1-14', '1.7.1-19']), ('1.7.1', ['1.7.1-10', '1.7.1-17', '1.7.1-21'])]
order,secs=schema(11,['cover','agenda','basi','famiglie','conto','t4590','tvel','trav','rildist','mappa']+order_ex+['chiusura'],CAPS,VER,RACC,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Minuti in decimi','Trasforma i minuti in ore prima di moltiplicare: 15 minuti sono 0,25 ore, 35 minuti 0,58.'),
  ('La riserva','Carburante = ore × consumo, più il 30% di riserva se il quiz non dice altro: × 1,3.'),
  ('Un grado, 60 miglia','Un primo di latitudine è un miglio: un grado sono 60 miglia.')],
 ['Quiz 1-2 · autonomia e carburante (6)','Quiz 3-9 · spazio, tempo e velocità (21)','Quiz 10-12 · coordinate geografiche (9)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. I quiz di calcolo si risolvono alla lavagna con S = V × T. Se il tempo stringe, lasciare per casa le slide 11 e 12.',esame=('navigazione','motori'))
write_deck(OUT,'Lezione 11 · Carteggio: carburante e autonomia',order,secs)
