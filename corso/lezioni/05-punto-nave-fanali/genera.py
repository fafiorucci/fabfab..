import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez05/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; GREY='#97A6B4'; NIGHT='#0F2238'
LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Navigare in vista della costa':'lighthouse','Rilevamento vero e polare':'compass',
 'Dove sono rispetto al faro':'lighthouse','I luoghi di posizione':'map','Il punto nave costiero':'pencil','Il GPS':'map',
 'I fanali di navigazione':'lantern','Cosa vedo di notte':'lantern','Le barche a vela di notte':'sail','Segnali diurni e luci speciali':'flag',
 'Chi lascia la rotta a chi':'helm','C\'è rischio di collisione?':'compass','Due barche a motore':'helm','Due barche a vela':'sail',
 'Rilevamento polare':'compass','Due punti cospicui':'lighthouse','Un punto cospicuo: rilevamento e distanza':'lighthouse','Rilevamenti successivi':'pencil','I rilevamenti':'compass','Il punto nave: tutte le tecniche':'map'})
def chip(t,c,size=34): return f'<p style="font-family:{H}; font-size:{size}px; font-weight:700; color:#FFFFFF; background:{c}; padding:10px 24px; border-radius:40px">{t}</p>'
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def sector(cx,cy,r,a0,a1,c,op=0.35):
    p0=pol(cx,cy,a0,r); p1=pol(cx,cy,a1,r); large=1 if (a1-a0)%360>180 else 0
    return f'<path d="M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{c}" fill-opacity="{op}" stroke="{c}" stroke-width="3"/>'
def tower(x,y,s=1,light=True):
    g=f'<path d="M{x-10*s} {y} L{x-6*s} {y-46*s} L{x+6*s} {y-46*s} L{x+10*s} {y} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/><rect x="{x-6*s}" y="{y-34*s}" width="{12*s}" height="{8*s}" fill="{CORAL}"/>'
    g+=f'<rect x="{x-8*s}" y="{y-58*s}" width="{16*s}" height="{12*s}" rx="{3*s}" fill="{SUN}" stroke="{NAVY}" stroke-width="{2.5*s}"/>'
    if light: g+=f'<circle cx="{x}" cy="{y-52*s}" r="{16*s}" fill="{SUN}" fill-opacity="0.3"/>'
    return g
def bell(x,y,s=1):
    return f'<path d="M{x-12*s} {y} L{x-12*s} {y-40*s} L{x} {y-56*s} L{x+12*s} {y-40*s} L{x+12*s} {y} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/><path d="M{x-5*s} {y-26*s} a{5*s} {6*s} 0 0 1 {10*s} 0 v{8*s} h{-10*s} Z" fill="{NAVY}"/>'
def glow(x,y,c,r=9):
    return f'<circle cx="{x}" cy="{y}" r="{r*2.6:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x}" cy="{y}" r="{r*1.6:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def sailtop(cx,cy,L,ang,side,fill='#FFFFFF',op=1):
    s=f'<path d="M{L*0.12:.0f} 0 Q{-L*0.1:.0f} {side*L*0.26:.0f} {-L*0.34:.0f} {side*L*0.2:.0f}" fill="none" stroke="{CORAL}" stroke-width="6" stroke-linecap="round"/>'
    return topboat(cx,cy,L,ang,fill,NAVY,4,op)+f'<g transform="translate({cx} {cy}) rotate({ang})" opacity="{op}">{s}<circle cx="{L*0.12:.0f}" cy="0" r="6" fill="{NAVY}"/></g>'
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(5,'Punto nave e fanali','Dove sono? Navigazione costiera, punto nave, rilevamenti e GPS. Chi è quella luce? Fanali, segnali diurni e precedenze',
 'Lezione 5. Capitoli del programma della scuola: Carteggio (navigazione costiera, punto nave 1 e 2, rilevamento polare, rilevamenti, GPS: la parte finale della scaletta «Carteggio · Navigazione», che nella lezione 4 arriva fino alla tabella delle deviazioni) e Prevenzione degli abbordi (fanali e precedenze). Aggiunta dall\'All. A: segnali diurni (materia 5). Segnali sonori e segnalamento IALA nella lezione 6.')
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','16′','Cap. 1 · Costiera e punto nave',CORAL),('0:16','18′','Cap. 2 · Rilevamenti e GPS',SUN),('0:34','16′','Cap. 3 · Fanali di navigazione',PURPLE),('0:50','12′','Cap. 4 · Segnali e precedenze',BLUE),('1:02','13′','Cap. 5 · Regole di rotta',SEA),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{max(int(d[:-1]),14)}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['navigazione', 'colreg'],5,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>fare il punto nave con due luoghi di posizione</li><li>usare tutti i rilevamenti: vero, bussola, polare, reciproco</li><li>usare il GPS con giudizio</li><li>riconoscere una barca di notte dai fanali</li><li>sapere chi lascia libera la rotta</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 05 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Cinque capitoli di teoria in 75 minuti, ognuno chiuso da una verifica da 2 quiz ufficiali (DD 131/2022): andare spediti sulle slide, il dettaglio è nelle note. Poi 45 minuti di raccolta quiz: 36 quiz ufficiali. Banca: navigazione costiera 49 quiz (1.7.6), navigazione elettronica 13 (1.7.3), fanali e segnali diurni 67 (1.5.1), prevenire gli abbordi 60 (1.5.2). All. C: 4 quesiti di navigazione e 2 di COLREG e segnalamento nella scheda da 20.')

# ============ COSTIERA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.18"/>'
b+=f'<path d="M0 0 L1092 0 L1092 150 Q980 190 880 150 Q760 110 640 170 Q520 230 400 160 Q280 100 160 150 Q80 180 0 140 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=tower(250,140,1.3)+bell(780,140,1.1)+f'<rect x="522" y="112" width="26" height="80" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><rect x="516" y="102" width="38" height="14" fill="{NAVY}"/>'
PN=(560,470)
b+=dash(250,90,PN[0]+(PN[0]-250)*0.3,PN[1]+(PN[1]-90)*0.3,SEA,4)+dash(780,100,PN[0]-(780-PN[0])*0.3,PN[1]+(PN[1]-100)*0.3,CORAL,4)
b+=topboat(PN[0]-40,PN[1]+70,120,-60,'#FFFFFF',NAVY,3,0.5,False)
b+=f'<circle cx="{PN[0]}" cy="{PN[1]}" r="16" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="{PN[0]}" cy="{PN[1]}" r="4" fill="{NAVY}"/>'
lbl=lab(X+150,Y+190,200,'Faro',NAVY,24,900,'center')+lab(X+690,Y+190,200,'Campanile',NAVY,24,900,'center')+lab(X+450,Y+200,220,'Torre',NAVY,24,900,'center')+lab(X+600,Y+450,260,'punto nave',NAVY,26,900,bg='#FFFFFF')
txt=(term('Navigazione costiera','Il punto nave si ricava da punti cospicui riconoscibili dal mare: fari, campanili, torri, capi.')
     +term('Cosa serve','Essere in vista della costa, carte a scala adeguata e pubblicazioni per riconoscerla; strumenti affidabili ed esperienza marinaresca.')
     +term('Punti cospicui','Ben visibili, entro 8-10 miglia. Strumenti da carteggio obbligatori oltre le 12 miglia.'))
sec('costiera', head('Carteggio · navigazione costiera','Navigare in vista della costa')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Costa con faro, torre e campanile; due rette di rilevamento partono da due punti cospicui e si incrociano nel punto nave della barca')+lbl,
 notes='Quiz 1.7.6-23 e -41 (navigazione costiera: punti cospicui, vista della costa), -3 e -4 (carte a scala adeguata e pubblicazioni), -7 (punti ben visibili entro 8-10 miglia), -45 (il campanile è un punto cospicuo), -5, -6, -49 (precisione e affidabilità), 1.7.5-71 (strumenti da carteggio obbligatori oltre 12 miglia). L\'esperienza conta: riconoscere un faro di giorno dalla forma e dai colori, di notte dalla caratteristica (lezione 3).')

# ============ LUOGHI DI POSIZIONE ============
def lp_ret():
    return f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/>'+tower(70,90,0.9)+line(70,50,280,170,SEA,4)+f'<circle cx="70" cy="50" r="6" fill="{SEA}"/>'+topboat(210,130,60,30,'#FFFFFF',NAVY,3)
def lp_bat():
    s=f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/><path d="M0 0 L300 0 L300 34 Q220 54 150 38 Q70 22 0 44 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
    s+=f'<path d="M0 82 Q80 66 150 96 T300 84" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="4 6" opacity="0.6"/><path d="M0 122 Q80 104 150 128 T300 118" fill="none" stroke="{BLUE}" stroke-width="5" stroke-dasharray="12 7"/>'
    s+=dash(150,186,150,30,NAVY,3)+topboat(150,150,56,-90,'#FFFFFF',NAVY,3)
    return s
def lp_dist():
    return f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/>'+tower(150,110,0.9)+f'<circle cx="150" cy="80" r="80" fill="none" stroke="{CORAL}" stroke-width="4" stroke-dasharray="10 7"/>'+topboat(222,120,56,60,'#FFFFFF',NAVY,3)
def lp_cap():
    s=f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/><circle cx="150" cy="120" r="90" fill="none" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="10 7"/>'
    s+=tower(80,160,0.7)+tower(220,160,0.7)+line(150,30,80,124,PURPLE,3)+line(150,30,220,124,PURPLE,3)+f'<circle cx="150" cy="30" r="9" fill="{NAVY}"/>'
    return s
LP=[(lp_ret(),'Semiretta di rilevamento','Vedo il faro per 045°: sono sulla semiretta che parte dal faro verso 225°.'),
    (lp_bat(),'Batimetrica','L\'ecoscandaglio legge la profondità della linea: sono lì. Attraversala a 90° per riconoscerla.'),
    (lp_dist(),'Cerchio di egual distanza','Conosco la distanza da un punto: sono su un cerchio con il centro nel punto.'),
    (lp_cap(),'Cerchio capace','Vedo due punti sotto lo stesso angolo: sono su un arco di cerchio che passa per i due.')]
cc=''.join(card(svgi(300,190,s,f'Disegno: {t}',dw=300,dh=190)+h3(t,28)+p(d,24),None,22,10) for s,t,d in LP)
sec('luoghi', head('Carteggio · gli strumenti del punto','I luoghi di posizione')+p('<b>Luogo di posizione</b>: l\'insieme dei punti che godono della stessa proprietà, per esempio «da qui vedo il faro per 045°».',28,INK)+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Il punto nave vuole almeno due luoghi di posizione. La rosa dei venti non lo è!',CORAL,36),
 notes='Quiz 1.7.6-39 (definizione: insieme di punti con la stessa proprietà), -2 (rette di rilevamento, cerchi capaci, cerchi di uguale distanza, batimetriche), -38 (la rosa dei venti non lo è), -14 (cerchio capace), -46 (un solo luogo non basta). Semiretta e non retta: il faro si vede solo da una parte, quella da cui lo guardo. La batimetrica si usa con l\'ecoscandaglio, tagliandola perpendicolarmente per non confondere le linee vicine.')

# ============ PUNTO NAVE 1 · DUE PUNTI COSPICUI ============
def coast(w=440):
    return f'<rect x="0" y="0" width="{w}" height="250" fill="{CHART}"/><path d="M0 0 L{w} 0 L{w} 60 Q{w*0.75:.0f} 86 {w*0.5:.0f} 62 Q{w*0.25:.0f} 40 0 70 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
def pnmark(x,y): return f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="4" fill="{NAVY}"/>'
def ext(a,b_,k=1.25): return (a[0]+(b_[0]-a[0])*k, a[1]+(b_[1]-a[1])*k)
def pn_two():
    s=coast()+tower(90,60,0.8)+bell(340,64,0.8); P=(230,190)
    e1=ext((90,24),P); e2=ext((340,22),P)
    return s+line(90,24,*e1,SEA,4)+line(340,22,*e2,CORAL,4)+pnmark(*P)
def pn_allin():
    s=coast()+tower(70,62,0.7)+f'<rect x="124" y="46" width="16" height="40" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'+tower(360,60,0.8)
    P=(300,206); a=(70,40); e=ext(a,P,1.12)
    return s+line(*a,*e,PURPLE,4)+line(360,22,*ext((360,22),P,1.2),SEA,4)+pnmark(*P)
def pn_one():
    s=coast()+tower(70,62,0.7)+f'<rect x="124" y="46" width="16" height="40" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
    a=(70,40); e=ext(a,(300,206),1.25)
    s+=line(*a,*e,PURPLE,4)
    for t,op in ((0.55,0.35),(0.8,0.35),(1.05,0.35)):
        q=ext(a,(300,206),t); s+=topboat(q[0],q[1],56,36,'#FFFFFF',NAVY,3,op,False)
    return s
PN1=[(pn_two(),'Due semirette','Due punti rilevati nello stesso momento: le semirette si incrociano nel punto nave. Meglio se si tagliano quasi a 90°.'),
     (pn_allin(),'Semiretta e allineamento','Due punti uno dietro l\'altro (rilevamento uguale, o a 180°) più il rilevamento di un terzo punto.'),
     (pn_one(),'Un allineamento non basta','So solo di essere su quella linea: serve almeno un altro luogo di posizione.')]
cc=''.join(card(svgi(440,250,s,f'Disegno: {t}',dw=480,dh=273)+h3(t,30)+p(d,24),None,24,10) for s,t,d in PN1)
sec('pn1', head('Carteggio · punto nave 1','Due punti cospicui')+f'<div style="display:flex; gap:22px">{cc}</div>'+note('Punto nave = almeno 2 luoghi di posizione',CORAL,40),
 notes='Quiz 1.7.6-1 (intersezione di due o più luoghi di posizione), -46 (un solo luogo non basta), -11 e -32 (allineamento: rilevamenti uguali o a 180°), -48 (due torri allineate: serve un altro luogo di posizione), -12 (squadrette per tracciare i rilevamenti). All\'esame: «PN per due rilevamenti simultanei», per es. 5.2.3-2, 5.4.3-2, 5.6.3-1 (lì i rilevamenti sono tre: il terzo è la verifica). Prima di tracciare: Rilv = Rilb + V.')

# ============ PUNTO NAVE 2 · RILEVAMENTO E DISTANZA ============
X=128
F=(660,240); RD=190
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/><path d="M500 30 L1062 30 L1062 300 Q960 250 880 180 Q800 110 700 140 Q600 160 540 90 Q520 60 500 30 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<circle cx="{F[0]}" cy="{F[1]}" r="{RD}" fill="{CORAL}" fill-opacity="0.06" stroke="{CORAL}" stroke-width="4" stroke-dasharray="12 8"/>'
PN=pol(*F,225,RD); far=pol(*F,225,RD+170)
b+=line(*F,*far,SEA,5)+tower(F[0],F[1]+30,1.2)
b+=dim(F[0]+10,F[1]+10,*pol(*F,135,RD))
b+=pnmark(*PN)
lc=pol(*F,135,RD*0.55); lr=pol(*F,225,RD+170)
lbl=(lab(X+F[0]+40,Y+F[1]-20,120,'faro',NAVY,26,900)+lab(X+lc[0]+20,Y+lc[1]-10,200,'1,5 miglia',CORAL,28,900,bg='#FFFFFF')
     +lab(X+lr[0]+30,Y+lr[1]-10,300,'semiretta Rlv 045°',SEA,26,900)+lab(X+PN[0]+30,Y+PN[1]+6,120,'PN',NAVY,30,900)
     +lab(X+F[0]-170,Y+F[1]+RD+14,340,'cerchio di egual distanza',CORAL,24,900,'center'))
txt=(term('Un punto, due luoghi','Dallo stesso faro prendo rilevamento e distanza: la semiretta e il cerchio si tagliano nel punto nave.')
     +term('La distanza','Dal radar o da un\'altra misura: col compasso si traccia il cerchio, centro nel faro.')
     +term('Esempio','Vedo il faro per 045° a 1,5 miglia: sono a SW del faro, a 1,5 miglia.')
     +term('All\'esame','La tecnica più frequente: «PN per rilevamento e distanza», per es. 5.4.3-6.'))
sec('pn2', head('Carteggio · punto nave 2','Un punto cospicuo: rilevamento e distanza'), pinned=pcol(txt,gap=18)+svgp(X,Y,W,Hh,b,'Faro sulla costa con il cerchio di egual distanza di 1,5 miglia e la semiretta di rilevamento per 045 gradi: si tagliano a Sud-Ovest del faro nel punto nave')+lbl,
 notes='Quiz 1.7.6-19 (servono un rilevamento e una distanza del punto cospicuo), -47 (con un solo punto cospicuo si può, se nota la distanza), -16 (5 miglia sul Rlv 180° del faro: sono a Nord, a 5 miglia), -21 (6 miglia sul Rlv SW: sono a NE). All\'esame «PN per rilevamento e distanza» compare in circa 30 esercizi, per es. 5.4.3-6, 5.4.3-8, 5.8.3-3, 5.1.1-1. Variante: allineamento e distanza (5.1.1-3).')

# ============ PUNTO NAVE 2 · RILEVAMENTI SUCCESSIVI ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/><path d="M30 30 L1062 30 L1062 120 Q800 170 546 110 Q300 60 30 130 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
F=(620,110); b+=tower(F[0],F[1]+20,1.2)
P1=(300,450); P2=(620,450)
b+=line(80,450,1000,450,NAVY,5)+arrow(900,450,1000,450,NAVY,5,20)
dx,dy=P1[0]-F[0],P1[1]-F[1]
b+=line(F[0],F[1],P1[0]+dx*0.25,P1[1]+dy*0.25,SEA,4)+dash(P2[0]-dx*0.9,P2[1]-dy*0.9,P2[0]+dx*0.25,P2[1]+dy*0.25,SEA,4)
b+=line(F[0],F[1],P2[0],P2[1]+110,CORAL,4)
b+=arrow(P1[0],P1[1]+40,P2[0],P2[1]+40,PURPLE,5,18)
b+=pnmark(*P2)
lbl=lab(X+130,Y+370,280,'1° rilevamento · 12:00',SEA,24,900)+lab(X+640,Y+300,280,'2° rilevamento · 12:20',CORAL,24,900)+lab(X+310,Y+500,360,'20′ a 9 nodi = 3 miglia',PURPLE,24,900,'center')
lbl+=lab(X+650,Y+180,330,'1° rilevamento trasportato',SEA,24,800)+lab(X+640,Y+410,200,'PN 12:20',NAVY,26,900,bg='#FFFFFF')+lab(X+860,Y+410,160,'Pv',NAVY,26,900)
txt=(term('Una sola mira, due volte','Rilevo lo stesso faro due volte: trasporto la prima semiretta lungo la rotta per le miglia percorse (M = V × Tᵐ : 60).')
     +term('Il punto','L\'incrocio della prima semiretta trasportata con la seconda è il punto nave dell\'ora del secondo rilevamento.')
     +term('All\'esame','Esercizi 5.x.3, come il 5.1.3-1: Rilb 075° alle 12:00, 125° alle 12:20, 9 nodi.'))
sec('puntonave', head('Carteggio · punto nave 2','Rilevamenti successivi'), pinned=svgp(X,Y,W,Hh,b,'Rilevamenti successivi dello stesso faro: la prima retta viene trasportata per le miglia percorse e incrocia la seconda nel punto nave')+lbl+pcol(txt),
 notes='Quiz 1.7.6-1 (intersezione di due o più luoghi di posizione), -12 e -13 (squadrette e compasso). Esercizi ufficiali «PN per rilevamenti successivi sulla stessa mira» (5.1.3-1…-5, 5.4.3-1, -5, 5.5.3-1): si convertono i rilevamenti bussola in veri (Rilv = Rilb + V), si tracciano le due semirette, si trasporta la prima parallelamente a sé stessa lungo la rotta per le miglia percorse; l\'incrocio con la seconda è il punto nave. Nel 5.1.3-1: 20′ a 9 nodi = 9 × 20 : 60 = 3 miglia. Si risolvono nella lezione 10.')
X=700

# ============ RILEVAMENTO POLARE ============
X=128
C=(546,330); RG=230
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<circle cx="{C[0]}" cy="{C[1]}" r="{RG}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
b+='<path d="'+' '.join(f'M{pol(*C,a,RG)[0]:.1f} {pol(*C,a,RG)[1]:.1f} L{pol(*C,a,RG-(20 if a%30==0 else 10))[0]:.1f} {pol(*C,a,RG-(20 if a%30==0 else 10))[1]:.1f}' for a in range(0,360,10))+f'" stroke="{NAVY}" stroke-width="3"/>'
for a in (90,270): b+=dash(*pol(*C,a,70),*pol(*C,a,RG-24),GREY,3)
b+=topboat(C[0],C[1],300,-90,'#FFFFFF',NAVY,4,0.85)
FO=pol(*C,300,RG+60); b+=line(*C,*pol(*C,300,RG+30),SEA,5)+tower(FO[0],FO[1]+10,1.0)
p0=pol(*C,0,120); p1=pol(*C,300,120); b+=f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A120 120 0 1 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-dasharray="10 7"/>'
q0=pol(*C,0,203); q1=pol(*C,300,203); b+=f'<path d="M{q0[0]:.1f} {q0[1]:.1f} A203 203 0 0 0 {q1[0]:.1f} {q1[1]:.1f}" fill="none" stroke="{CORAL}" stroke-width="7"/>'
lbl=''
for a,t1,t2 in ((0,'000°','0°'),(90,'090°','+90°'),(180,'180°','±180°'),(270,'270°','−90°')):
    o=pol(*C,a,RG+34); i=pol(*C,a,RG-50)
    lbl+=lab(X+o[0]-50,Y+o[1]-16,100,t1,NAVY,26,900,'center')+lab(X+i[0]-50,Y+i[1]-16,100,t2,CORAL,26,900,'center')
lc=pol(*C,330,215); ln=pol(*C,150,125)
lbl+=(lab(X+lc[0]-230,Y+lc[1]-70,250,'ρ −60° semicircolare',CORAL,26,900,'right',bg='#FFFFFF')+lab(X+ln[0]+10,Y+ln[1]-10,250,'ρ 300° circolare',NAVY,26,900,bg='#FFFFFF')
      +lab(X+FO[0]-150,Y+FO[1]+20,140,'faro',SEA,26,900,'right')+lab(X+C[0]+70,Y+C[1]+8,160,'traverso',SOFT,24,800)+lab(X+C[0]-230,Y+C[1]+8,160,'traverso',SOFT,24,800,'right'))
txt=(term('Rilevamento polare ρ','L\'angolo tra la prora (asse longitudinale) e l\'oggetto. Si misura con il grafometro.')
     +term('Grafometro circolare','Da 000° a 360° in senso orario dalla prora, sempre positivo: traverso a dritta 090°, a sinistra 270°.')
     +term('Grafometro semicircolare','Da 0° a 180°: + a dritta, − a sinistra. Traverso a sinistra −090°.')
     +term('Il traverso','ρ 90° e traverso coincidono sempre. Con vento o corrente accosti quando l\'oggetto è perpendicolare all\'asse della barca.'))
sec('rilevamento', head('Carteggio · dalla prora','Rilevamento polare'), pinned=svgp(X,Y,W,Hh,b,'Barca al centro del grafometro: fuori la scala circolare da 000 a 360 gradi dalla prora, dentro quella semicircolare con più a dritta e meno a sinistra; un faro a sinistra prora si legge 300 gradi oppure meno 60 gradi')+lbl+pcol(txt,gap=16),
 notes='Quiz 1.7.6-8 (angolo tra asse longitudinale e oggetto), -9 (circolare da 000° a 360° in senso orario dalla prora), -10 e -29 (semicircolare: positivo a dritta, negativo a sinistra), -17 (ρ 90° e traverso coincidono sempre), -33 (traverso = polare 90°), -18 (con scarroccio o deriva si accosta quando il punto è perpendicolare all\'asse longitudinale), -35 (grafometro). Nel disegno lo stesso faro si legge 300° sul grafometro circolare e −60° su quello semicircolare: con Pv 040° dà sempre Rilv 340°.')
X=700

# ============ I RILEVAMENTI ============
RT=[('Rilv','vero','dal Nord vero, sulla carta',NAVY,BLUE_T),('Rilm','magnetico','dal Nord magnetico',SEA,SEA_T),('Rilb','bussola','dal Nord bussola: lo leggi a bordo',CORAL,CORAL_T),('ρ','polare','dalla prora, col grafometro',PURPLE,LILAC_T),('±180°','reciproco','dal faro verso di me',GREEN,'#DDF3E4')]
cards=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:22px; border-radius:26px"><p style="font-family:{H}; font-size:46px; font-weight:700; line-height:1; color:{c}">{s}</p>{p(n,28,INK,800)}{p(d,24)}</div>' for s,n,d,c,bg in RT)
forms=f'<div style="display:flex; gap:14px; flex-wrap:wrap">{chip("Rilv = Rilb + V",CORAL,32)}{chip("Rilv = Rilm + d",SEA,32)}{chip("Rilv = Pv + ρ",PURPLE,32)}{chip("reciproco = Rilv ± 180°",GREEN,32)}</div>'
EXR=[('Esercizio 5.1.3-2','Rilb 164°, V −4°','Rilv 160°',CORAL),('Polare semicircolare','Pv 040°, ρ −60°','Rilv 340°',PURPLE),('Polare circolare','Pv 040°, ρ 300°','400° − 360° = 340°',PURPLE),('Reciproco','vedo il faro per 160°','dal faro sono a 340°',GREEN)]
exs=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:#FFFFFF; {SHADOW}; padding:20px; border-radius:24px">{tag(t,c)}{p(a,26,INK,700)}<p style="font-family:{H}; font-size:36px; font-weight:700; color:{c}">{r}</p></div>' for t,a,r,c in EXR)
sec('rilevamenti', head('Carteggio · tutte le opzioni','I rilevamenti')+f'<div style="display:flex; gap:16px">{cards}</div>'+forms+f'<div style="display:flex; gap:18px">{exs}</div>',
 notes='Riepilogo dei cinque modi di indicare la direzione di un punto cospicuo. Il rilevamento bussola si converte come la prora: Rilv = Rilb + V, con V = d + δ e δ letta per la prora della barca (non per il rilevamento). Il polare si somma alla prora vera: col grafometro semicircolare il segno fa da solo, con quello circolare si toglie 360° se si supera. Il reciproco serve per sapere dove sono rispetto al faro e per tracciare la semiretta dal faro. Quiz 1.7.6-24 (angolo di rilevamento dal Nord), -8 e -9 (polare), 1.7.4-34 (segni). Esercizio 5.1.3-2: Pb 086°, d 2°W, δ −2° → V −4°: Rilb 164° → Rilv 160°, Rilb 194° → Rilv 190°.')

# ============ DOVE SONO RISPETTO AL FARO ============
cx,cy=546,310
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/><circle cx="{cx}" cy="{cy}" r="230" fill="none" stroke="#D9D2BF" stroke-width="3" stroke-dasharray="6 8"/>'
b+=tower(cx,cy+30,1.3)
bp=pol(cx,cy,225,165); b+=topboat(bp[0],bp[1],110,-45,'#FFFFFF',NAVY,4)
b+=arrow(bp[0]+30,bp[1]-30,cx-40,cy+10,CORAL,6,24)
bp2=pol(cx,cy,0,190); b+=topboat(bp2[0],bp2[1],100,90,'#FFFFFF',NAVY,3,0.5,False)+arrow(bp2[0],bp2[1]+40,cx,cy-80,SEA,5,20)
lbl=''
for a,t in [(0,'N'),(90,'E'),(180,'S'),(270,'W'),(45,'NE'),(135,'SE'),(225,'SW'),(315,'NW')]:
    x,y=pol(cx,cy,a,272); lbl+=lab(X+x-40,Y+y-16,80,t,NAVY if a%90==0 else SOFT,26,900,'center')
lbl+=lab(X+bp[0]-330,Y+bp[1]+40,300,'sono a SW: lo rilevo per 045°',CORAL,24,900,bg='#FFFFFF')+lab(X+bp2[0]+40,Y+bp2[1]-10,280,'sono a N: lo rilevo per 180°',SEA,24,900,bg='#FFFFFF')
ex=''.join(f'<div style="display:flex; justify-content:space-between; gap:12px; background:#FFFFFF; {SHADOW}; padding:10px 16px; border-radius:16px">{p(a,25,INK,700)}{p(b_,25,SEA,900)}</div>' for a,b_ in [('Sono a Sud-Est','Rlv 315°'),('Sono sul Rlv 270°','sono a Est'),('Sono sul Rlv 157,5°','sono a NNW')])
txt=term('Il rilevamento reciproco','Il faro si rileva dalla parte opposta a quella in cui mi trovo: aggiungi o togli 180°.')+ex
sec('reciproco', head('Carteggio · il rilevamento reciproco','Dove sono rispetto al faro')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Faro al centro della rosa: una barca a Sud-Ovest lo rileva per 045°, una barca a Nord lo rileva per 180°')+lbl,
 notes='Quiz 1.7.6-15, -20, -22, -25, -30, -31, -36 (sono a … del faro: lo rilevo per …), -16, -21, -26, -27, -28, -34, -37, -40, -42, -43 (sono sul Rlv … del faro: mi trovo a …), -44 (faro a prora con Rv Ovest: lo rilevo per 270°). Il quiz 1.7.6-28 ha una formulazione ambigua («sono sul Rlv 225°… lo rilevo per Sud-Ovest»): risposta ministeriale b.')

# ============ IL PUNTO NAVE: TUTTE LE TECNICHE ============
def tk_bg(): return f'<rect x="0" y="0" width="300" height="140" fill="{CHART}"/><path d="M0 0 L300 0 L300 30 Q220 46 150 32 Q70 18 0 38 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="2"/>'
def tk_sim(): return tk_bg()+tower(70,36,0.6)+bell(230,38,0.6)+line(70,12,*ext((70,12),(150,110),1.2),SEA,3)+line(230,12,*ext((230,12),(150,110),1.2),CORAL,3)+pnmark(150,110)
def tk_dist(): return tk_bg()+f'<circle cx="150" cy="20" r="90" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>'+tower(150,36,0.6)+line(150,12,*pol(150,12,200,130),SEA,3)+pnmark(*pol(150,12,200,90))
def tk_all(): return tk_bg()+tower(60,40,0.5)+f'<rect x="96" y="22" width="12" height="28" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'+line(60,22,*ext((60,22),(220,116),1.15),PURPLE,3)+f'<circle cx="60" cy="22" r="110" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>'+pnmark(*ext((60,22),(220,116),0.58))
def tk_succ():
    s=tk_bg()+tower(150,36,0.6)+line(20,112,290,112,NAVY,3)
    return s+line(150,12,70,112,SEA,3)+dash(230,12,150,112,SEA,3)+line(150,12,175,140,CORAL,3)+arrow(70,128,150,128,PURPLE,3,10)+pnmark(150,112)
def tk_div():
    s=tk_bg()+tower(80,36,0.6)+bell(230,38,0.6)+line(20,112,290,112,NAVY,3)
    return s+line(80,12,60,112,SEA,3)+dash(160,12,140,112,SEA,3)+line(230,12,140,112,CORAL,3)+arrow(60,128,140,128,PURPLE,3,10)+pnmark(140,112)
def tk_pol():
    s=tk_bg()+tower(200,36,0.6)+line(20,112,290,112,NAVY,3)+topboat(120,112,40,0,'#FFFFFF',NAVY,2)
    return s+dash(120,112,200,32,SEA,3)+dash(200,112,200,32,CORAL,3)+pnmark(200,112)
TK=[(tk_sim(),'Due rilevamenti simultanei','Due punti cospicui nello stesso istante.','24 esercizi · 5.2.3-2, 5.6.3-1'),
    (tk_dist(),'Rilevamento e distanza','Semiretta e cerchio di egual distanza.','30 esercizi · 5.4.3-6, 5.8.3-3'),
    (tk_all(),'Allineamento e distanza','Due punti allineati e la distanza da uno.','2 esercizi · 5.1.1-3'),
    (tk_succ(),'Successivi, stessa mira','Trasporto la prima semiretta del cammino fatto.','9 esercizi · 5.1.3-1'),
    (tk_div(),'Successivi, mire diverse','Prima un punto, poi un altro: trasporto il primo.','10 esercizi · 5.2.3-1, 5.3.3-1'),
    (tk_pol(),'Polari e traverso','Rilv = Pv + ρ; a ρ 90° sono al traverso.','21 + 31 esercizi · 5.3.3-2, -4')]
cc=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#FFFFFF; {SHADOW}; padding:16px; border-radius:24px">{svgi(300,140,s,"Disegno: "+t,dw=300,dh=140)}{h3(t,28)}{p(d,24)}{p(e,24,SEA,800)}</div>' for s,t,d,e in TK)
sec('tecniche', head('Carteggio · tutte le opzioni','Il punto nave: tutte le tecniche')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px 22px">{cc}</div>',
 notes='Le tecniche del punto nave negli esercizi ufficiali di carteggio (DD 131/2022), con quante volte compaiono: due rilevamenti simultanei (24, per es. 5.2.3-2, 5.4.3-2, 5.6.3-1), rilevamento e distanza (30, 5.4.3-6, 5.4.3-8, 5.8.3-3), allineamento e distanza (2, 5.1.1-3, 5.4.1-13), rilevamenti successivi sulla stessa mira (9, 5.1.3-1…-5), su mire diverse (10, 5.2.3-1, 5.3.3-1, 5.3.3-5), rilevamenti polari successivi (21, 5.3.3-4, 5.3.3-6) e punto al traverso (31, 5.3.3-2, 5.3.3-3). In tutte prima si convertono i rilevamenti in veri. Il cerchio capace è un luogo di posizione ma negli esercizi non serve. Le tecniche si fanno sulla carta nelle lezioni 8 e 10.')

# ============ GPS ============
b=f'<rect x="210" y="40" width="680" height="540" rx="46" fill="{NAVY}"/><rect x="250" y="80" width="600" height="380" rx="18" fill="#DDF1F5"/>'
b+=f'<path d="M250 80 L850 80 L850 170 Q720 210 600 160 Q480 110 380 170 Q300 210 250 180 Z" fill="{LAND}"/>'
b+=f'<path d="M330 420 L520 300 L720 230" fill="none" stroke="{CORAL}" stroke-width="5" stroke-dasharray="12 8"/>'
for x,y in ((520,300),(720,230)): b+=f'<path d="M{x} {y} V{y-40} L{x+26} {y-30} L{x} {y-20}" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<path d="M700 184 h40 M700 184 v-16" stroke="{NAVY}" stroke-width="5"/><circle cx="742" cy="168" r="7" fill="{LGREEN}"/><circle cx="700" cy="160" r="7" fill="{LRED}"/>'
b+=topboat(330,420,70,-32,'#FFFFFF',NAVY,3)
b+=f'<rect x="290" y="490" width="160" height="60" rx="16" fill="{LRED}"/><rect x="480" y="490" width="120" height="60" rx="16" fill="#2B4A6B"/><rect x="630" y="490" width="120" height="60" rx="16" fill="#2B4A6B"/>'
b+=''.join(f'<g transform="translate({x} {y}) rotate(-30)"><rect x="-14" y="-8" width="28" height="16" rx="3" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/><rect x="-40" y="-6" width="22" height="12" fill="{BLUE}"/><rect x="18" y="-6" width="22" height="12" fill="{BLUE}"/></g>' for x,y in ((110,90),(990,120),(980,420)))
lbl=lab(X+290,Y+504,160,'MOB',('#FFFFFF'),28,900,'center')+lab(X+620,Y+250,220,'waypoint',NAVY,24,900)
txt=(term('Come funziona','Misura la distanza da più satelliti: dà il punto nave in ogni istante, con un errore di pochi metri.')
     +term('Cosa ti dice','Latitudine e longitudine, Rv e Ve sul fondo, rotta e distanza dal waypoint, fuori rotta, ETA e tempo di percorrenza, data e ora.')
     +term('I limiti','Non vede ostacoli né costa: controlla il percorso sulla carta. Waypoint del porto almeno 500 m fuori dai fanali.')
     +term('Obbligo e MOB','Obbligatorio oltre le 12 miglia, fisso o portatile a batterie alcaline. Il tasto MOB segna dove è caduto l\'uomo in mare.'))
sec('gps', head('Navigazione elettronica','Il GPS')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Schermo di un GPS cartografico con la costa, la rotta tratteggiata tra due waypoint, la barca e il tasto rosso MOB; intorno i satelliti',pan=True)+lbl,
 notes='Quiz 1.7.3-2 (distanza dai satelliti), -3 e -13 (informazioni: lat e long, rotta e distanza dal waypoint, fuori rotta, tempo stimato di arrivo), -5 (pochi metri), -6 (punto nave in ogni istante), -7 (obbligatorio oltre 12 miglia), -4 (apparati fissi e portatili), -8 (waypoint a 500 m dai fanali del porto), -11 (non tiene conto degli ostacoli), -12 (navigazione per waypoint), -1, -9, -10 (MOB). Le dotazioni oltre le 12 miglia: lezione 6. Il GPS non sostituisce la carta: il punto stimato e quello costiero restano indispensabili.')
quiz_slide('quiz1','Quiz 1 · Navigazione costiera e punto nave',['1.7.6-1', '1.7.6-48'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.7.6-1', '1.7.6-48'],True)
quiz_slide('quiz1b','Quiz 2 · Rilevamenti e GPS',['1.7.6-20', '1.7.3-8'],False)
quiz_slide('quiz1br','Quiz 2 · Le risposte',['1.7.6-20', '1.7.3-8'],True)

# ============ FANALI ============
X=128
cx,cy=546,320
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/>'
b+=sector(cx,cy,280,247.5,472.5,LWHITE,0.16)
b+=sector(cx,cy,210,0,112.5,LGREEN,0.4)+sector(cx,cy,210,247.5,360,LRED,0.4)+sector(cx,cy,210,112.5,247.5,LWHITE,0.3)
b+=topboat(cx,cy,190,-90,'#DCE6F0',NAVY,4)
b+=glow(cx,cy-40,LWHITE,7)+glow(cx+18,cy-10,LGREEN,6)+glow(cx-18,cy-10,LRED,6)+glow(cx,cy+92,LWHITE,6)
g=pol(cx,cy,56,245); r=pol(cx,cy,304,245); s=pol(cx,cy,180,245); m=pol(cx,cy,0,300)
lbl=lab(X+m[0]-210,Y+14,420,'testa d\'albero · bianco · 225°',LWHITE,26,900,'center')+lab(X+836,Y+130,250,'verde · dritta · 112,5°',LGREEN,26,900)+lab(X+6,Y+130,254,'rosso · sinistra · 112,5°',LRED,26,900,'right')+lab(X+s[0]-200,Y+s[1]+14,400,'coronamento · bianco · 135°',LWHITE,26,900,'center')
txt=term('Quando','Dal tramonto al sorgere del sole e con visibilità ridotta. Per il diporto, di notte oltre 1 miglio dalla costa.')+term('I settori','I due laterali insieme fanno i 225° della testa d\'albero; con il coronamento si copre tutto l\'orizzonte.')+term('Portata','Laterali visibili a 2 miglia per le unità tra 12 e 50 m.')+term('Oltre i 50 m','Un secondo bianco di testa d\'albero, più alto e a poppavia.')
sec('fanali', head('COLREG · le luci','I fanali di navigazione'), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto di notte: settori di visibilità dei fanali, bianco di testa d\'albero verso prora, verde a dritta, rosso a sinistra, bianco di coronamento verso poppa',pan=False)+lbl+pcol(txt,532,20),
 notes='Quiz 1.5.1-1 (motore < 50 m: testa d\'albero, laterali, coronamento), -11 (testa d\'albero bianco), -36 e -64 (verde a dritta, rosso a sinistra), -5 e -30 (laterali 112,5° ciascuno, insieme 225°), -4 e -7 (coronamento 135° verso poppa), -12 e -38 (secondo fanale di testa d\'albero oltre 50 m), -29 (nave di 280 m: 2 fanali di testa d\'albero), -28 e 1.5.2-34 (portata 2 miglia), -23 e -56 (quando accenderli), -27 e 1.5.2-33 (diporto oltre 1 miglio dalla costa), -26 e -35 (fanali regolamentari), 1.5.2-11 (niente altre luci che si confondano). Il quiz 1.5.1-8 è oscurato.')
X=700

# ============ COSA VEDO DI NOTTE ============
def nightv(kind):
    s=f'<rect x="0" y="0" width="300" height="200" fill="{NIGHT}"/><path d="M0 150 Q75 142 150 150 T300 148 L300 200 L0 200 Z" fill="#17304C"/>'
    if kind=='prua':
        s+=f'<path d="M110 150 L150 108 L190 150 Z" fill="#23405F"/>'+glow(150,60,LWHITE)+glow(128,122,LGREEN)+glow(172,122,LRED)
    elif kind=='dritta':
        s+=f'<path d="M60 150 L240 150 L250 128 L70 132 Z" fill="#23405F"/>'+glow(190,60,LWHITE)+glow(220,124,LGREEN)
    elif kind=='poppa':
        s+=f'<path d="M110 150 L190 150 L186 124 L114 124 Z" fill="#23405F"/>'+glow(150,120,LWHITE)
    else:
        s+=f'<path d="M150 40 L150 130 L100 130 Z M156 50 L156 130 L196 130 Z" fill="#23405F"/><path d="M116 150 L150 132 L184 150 Z" fill="#23405F"/>'+glow(128,130,LGREEN)+glow(172,130,LRED)
    return s
NV=[('prua','Motore, di prua','Bianco in alto, verde e rosso: viene verso di me.'),('dritta','Motore, dal lato dritto','Bianco e verde: la vedo di fianco, sulla sua dritta.'),
    ('poppa','Di poppa','Solo il bianco di coronamento: la sto raggiungendo.'),('vela','Vela, di prua','Verde e rosso senza bianco: è una barca a vela.')]
cc=''.join(card(svgi(300,200,nightv(k),f'Di notte: {t}',dw=300,dh=200,pan=False)+h3(t,28)+p(d,23),None,22,10) for k,t,d in NV)
sec('cosavedo', head('COLREG · leggere le luci','Cosa vedo di notte')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Il verde di un\'altra barca è sulla mia sinistra quando mi viene incontro!',CORAL,36),
 notes='Quiz 1.5.1-43 e -44 (figure di unità a motore), -45, -47, -51 (figure di unità a vela), 1.5.2-54 (un bianco a prora: sto raggiungendo un\'altra unità), 1.5.2-17 e -45 (nave raggiungente nel settore del coronamento), 1.5.2-46 (entrambe vedono testa d\'albero e laterali: rotte opposte, entrambe accostano a dritta), 1.5.2-41 (fiancate opposte). Nella prima figura il verde appare a sinistra perché la barca ci viene incontro.')

# ============ VELA DI NOTTE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/><path d="M0 500 Q273 486 546 500 T1092 496 L1092 620 L0 620 Z" fill="#17304C"/>'
b+=f'<path d="M260 470 L820 470 L780 520 L320 520 Z" fill="#23405F" stroke="#3B5F84" stroke-width="3"/><path d="M540 470 V70" stroke="#3B5F84" stroke-width="8"/>'
b+=f'<path d="M530 90 L530 450 L330 450 Z" fill="#23405F"/><path d="M552 90 L552 450 L760 450 Z" fill="#1D3A58"/>'
b+=glow(540,62,LWHITE,9)+glow(528,58,LRED,5)+glow(552,58,LGREEN,5)
b+=glow(540,120,LRED,8)+glow(540,156,LGREEN,8)
b+=glow(790,478,LGREEN,8)+glow(290,478,LWHITE,8)
lbl=lab(X+580,Y+40,300,'tricolore in testa d\'albero (sotto i 20 m)',LWHITE,24,900)+lab(X+580,Y+120,340,'facoltativi: rosso sopra verde, 360°',LWHITE,24,800)+lab(X+800,Y+420,240,'laterali',LGREEN,24,900)+lab(X+160,Y+420,200,'coronamento',LWHITE,24,900,'right')
txt=term('La regola','A vela: fanali laterali e coronamento. Niente bianco di testa d\'albero.')+term('A vela e a motore','Conta come nave a motore: si accende anche il bianco di testa d\'albero. Di giorno: un cono con il vertice in basso.')+term('Le piccole','Natanti a vela sotto i 7 m: basta una torcia bianca. Entro 3 miglia una torcia di sicurezza a luce bianca.')
sec('velanotte', head('COLREG · la vela','Le barche a vela di notte')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Barca a vela di notte vista di fianco: laterale verde a prua, bianco di coronamento a poppa, tricolore o luci facoltative rossa sopra verde in cima all\'albero',pan=False)+lbl,
 notes='Quiz 1.5.1-39 e -67 (vela: laterali e coronamento), -61 (vela oltre 20 m: laterali e fanale di poppa), -40 (facoltativi rosso sopra verde, 360°), -58 e -59 (figure: vela sotto e sopra i 20 m, il tricolore è ammesso sotto i 20 m), -9 e -55 (cono con il vertice in basso: vela e motore insieme), -15 (natanti a vela sotto 7 m: torcia bianca), -6 (entro 3 miglia: torcia di sicurezza a luce bianca). Il tricolore non si usa insieme alle luci facoltative.')

quiz_slide('quiz2','Quiz 3 · I fanali',['1.5.1-4', '1.5.1-39'],False)
quiz_slide('quiz2r','Quiz 3 · Le risposte',['1.5.1-4', '1.5.1-39'],True)

# ============ SEGNALI DIURNI E LUCI SPECIALI ============
def ball(x,y,r=16): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>'
def cone(x,y,down=True,h=30):
    return f'<path d="M{x-16} {y-h/2} L{x+16} {y-h/2} L{x} {y+h/2} Z" fill="{INK}"/>' if down else f'<path d="M{x-16} {y+h/2} L{x+16} {y+h/2} L{x} {y-h/2} Z" fill="{INK}"/>'
def diamond(x,y): return f'<path d="M{x} {y-20} L{x+16} {y} L{x} {y+20} L{x-16} {y} Z" fill="{INK}"/>'
def sig(day,night):
    s=f'<rect x="0" y="0" width="160" height="180" fill="#EAF4F7"/><path d="M80 170 V10" stroke="{SOFT}" stroke-width="3"/>{day}'
    s+=f'<rect x="160" y="0" width="160" height="180" fill="{NIGHT}"/><path d="M240 170 V10" stroke="#2B4A6B" stroke-width="3"/>{night}'
    return s
SD=[(sig(ball(80,60),glow(240,60,LWHITE)),'Alla fonda','Un pallone nero · di notte un bianco visibile tutto intorno.'),
    (sig(cone(80,60,True),glow(240,50,LWHITE,7)+glow(222,110,LRED,6)+glow(258,110,LGREEN,6)),'Vela e motore insieme','Un cono con il vertice in basso · di notte i fanali da motore.'),
    (sig(cone(80,50,True)+cone(80,80,False),glow(240,50,LGREEN)+glow(240,95,LWHITE)),'Pesca a strascico','Due coni uniti per il vertice · di notte verde sopra bianco.'),
    (sig(cone(80,50,True)+cone(80,80,False),glow(240,50,LRED)+glow(240,95,LWHITE)),'Pesca non a strascico','Due coni uniti per il vertice · di notte rosso sopra bianco.'),
    (sig(ball(80,50)+ball(80,100),glow(240,50,LRED)+glow(240,100,LRED)),'Non governa','Due palloni in verticale · di notte due rossi.'),
    (sig(ball(80,40)+diamond(80,86)+ball(80,132),glow(240,40,LRED)+glow(240,86,LWHITE)+glow(240,132,LRED)),'Manovrabilità limitata','Pallone, rombo, pallone · di notte rosso, bianco, rosso.')]
cc=''.join(card(f'<div style="display:flex; gap:16px; align-items:center">{svgi(320,180,s,f"Segnale diurno e luci notturne: {t}",dw=240,dh=135,pan=False)}<div style="display:flex; flex-direction:column; gap:4px">{h3(t,26)}{p(d,22)}</div></div>',None,16,8) for s,t,d in SD)
sec('diurni', head('COLREG · forme e luci','Segnali diurni e luci speciali')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px">{cc}</div>',
 notes='Quiz 1.5.1-10 e -54 (alla fonda: pallone nero), -57 (figura: unità alla fonda sotto i 50 m), -9 e -55 (cono con il vertice in basso: vela e motore), -2 e -60 (strascico: due coni uniti per il vertice), -33, -42, -52 (strascico: verde sopra bianco), -41, -48, -49, -50, -53 (pesca non a strascico: rosso sopra bianco; attrezzi oltre 150 m: cono con il vertice in alto verso l\'attrezzo, -32), -21 e -25 (manovrabilità limitata, condizionata dalla propria immersione: cilindro e tre rossi), -19 (incagliata), -24 (rimorchiata), -3 e -34 (cuscino d\'aria), -46 (nave pilota), -18 e -20 (rimorchio), -62 (elenco completo nel COLREG).')

# ============ GERARCHIA ============
steps=[('Nave che non governa',LRED),('Manovrabilità limitata',PURPLE),('Intenta alla pesca',SEA),('A vela',BLUE),('A motore',CORAL)]
st=''.join(f'<div style="display:flex; gap:14px; align-items:center; padding:0px 0px 0px {k*60}px"><p style="font-family:{H}; font-size:36px; font-weight:700; color:#FFFFFF; background:{c}; padding:14px 30px; border-radius:40px; white-space:nowrap">{k+1} · {t}</p></div>' for k,(t,c) in enumerate(steps))
side=card(note('Regola generale',GREEN,38)+p('Ognuno lascia libera la rotta a chi sta <b>più in alto</b> nella scala. Il motore la lascia a tutti gli altri.',26,INK)+note('Attenzione',CORAL,38)+'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>La raggiungente lascia sempre libera la rotta.</li><li>Negli schemi di separazione del traffico la vela e le unità sotto i 20 m non intralciano le navi.</li><li>Di notte il diporto non ha mai la precedenza sulle navi con luci speciali.</li></ul>',None,30,12,flex='none',extra='; width:640px')
sec('gerarchia', head('COLREG · la scala delle precedenze','Chi lascia la rotta a chi')+f'<div style="display:flex; gap:40px; align-items:start"><div style="flex:1; display:flex; flex-direction:column; gap:14px">{st}</div>{side}</div>',
 notes='Quiz 1.5.2-29 (una unità a motore dà precedenza, nell\'ordine, a: nave che non governa, manovrabilità limitata, intenta alla pesca, vela), -8 (la manovrabilità limitata lascia libera la rotta a chi non governa), 1.5.1-13 e 1.5.2-24 (chi pesca la lascia a chi non governa e a chi ha manovrabilità limitata), 1.5.1-16 (il motore la lascia sempre a chi non governa), 1.5.2-26 (draga = manovrabilità limitata), 1.5.2-19 (raggiungente), 1.5.2-5 (schemi di separazione del traffico), 1.5.1-14 (di notte il diporto non ha mai precedenza su navi con luci speciali), 1.5.2-2 (COLREG 72). Nel COLREG c\'è anche la nave condizionata dalla propria immersione, tra la manovrabilità limitata e la pesca.')

quiz_slide('quiz3','Quiz 4 · Segnali e precedenze',['1.5.1-10', '1.5.1-60'],False)
quiz_slide('quiz3r','Quiz 4 · Le risposte',['1.5.1-10', '1.5.1-60'],True)

# ============ RISCHIO DI COLLISIONE ============
X=128
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
C=(760,160)
A=[(760,560),(760,440),(760,320)]; Bt=[(360,160),(480,160),(600,160)]
b+=dpath(f'M{A[0][0]} {A[0][1]+20} L{C[0]} {C[1]}',GREY,3)+dpath(f'M{Bt[0][0]-60} {Bt[0][1]} L{C[0]} {C[1]}',GREY,3)
for i,(a,bb) in enumerate(zip(A,Bt)):
    op=0.35+0.3*i; b+=line(a[0],a[1]-40,bb[0]+40,bb[1],[SEA,BLUE,CORAL][i],3)
    b+=topboat(a[0],a[1],90,-90,'#FFFFFF',NAVY,3,op,False)+topboat(bb[0],bb[1],90,0,'#FFFFFF',NAVY,3,op,False)
b+=f'<circle cx="{C[0]}" cy="{C[1]}" r="26" fill="{LRED}" fill-opacity="0.2" stroke="{LRED}" stroke-width="4"/>'
lbl=lab(X+C[0]+40,Y+C[1]-20,240,'punto di collisione',LRED,24,900)+lab(X+800,Y+460,240,'io',NAVY,26,900)+lab(X+300,Y+200,260,'l\'altra barca',NAVY,24,900)+lab(X+80,Y+380,420,'le rette di rilevamento restano parallele',INK,24,800)
txt=term('Il segnale d\'allarme','Il rilevamento dell\'altra barca non cambia e la distanza diminuisce: c\'è rischio di collisione.')+term('Come accorgersene','Con rilevamenti polari successivi. Nel dubbio, il pericolo si considera esistente.')+term('Come manovrare','In modo deciso, per tempo e ben evidente: un\'accostata ampia che l\'altro veda subito.')
sec('rischio', head('COLREG · rischio di collisione','C\'è rischio di collisione?'), pinned=svgp(X,Y,W,Hh,b,'Due barche su rotte che convergono: nei tre istanti successivi la retta che le congiunge resta parallela a se stessa, cioè il rilevamento non cambia')+lbl+pcol(txt),
 notes='Quiz 1.5.1-22, 1.5.2-18, -27, -30 (rilevamento costante e distanza che diminuisce), -42, -47, -55 (rilevamenti polari successivi), -56 (nel dubbio il pericolo esiste), -3 e -57 (manovra decisa, per tempo, con ampio margine), -4 (cambi di rotta e velocità ben evidenti), -43 (chi non ha diritto manovra), 1.4.4-40 (chi ha il diritto mantiene rotta e velocità), -10 (visibilità limitata: velocità di sicurezza).')
X=700

# ============ DUE BARCHE A MOTORE ============
def m_opp():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'
    s+=topboat(130,180,70,-90,'#FFFFFF',NAVY,3)+topboat(170,40,70,90,'#FFFFFF',NAVY,3)
    s+=dpath('M130 140 Q130 110 170 90 L170 80',CORAL,4)+dpath('M170 80 Q170 110 130 130',SEA,4)
    return s
def m_cross():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'
    s+=topboat(110,180,70,-90,'#FFFFFF',NAVY,3)+topboat(200,90,70,180,'#FFFFFF',NAVY,3)
    s+=dpath('M110 145 Q112 128 160 128 Q262 128 272 36',CORAL,4)+dpath('M165 90 L20 90',GREY,3)
    return s
def m_over():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+sector(150,90,150,112.5,247.5,SUN,0.25)
    s+=topboat(150,70,70,-90,'#FFFFFF',NAVY,3)+topboat(150,190,70,-90,'#FFFFFF',NAVY,3)+dpath('M150 160 Q210 110 210 40',CORAL,4)
    return s
MM=[(m_opp(),'Rotte opposte','Tutte e due accostano a dritta e si passano sulla sinistra.'),
    (m_cross(),'Rotte incrociate','Chi vede l\'altra sulla propria dritta le lascia libera la rotta e le passa di poppa. Ha la precedenza chi viene da dritta.'),
    (m_over(),'Sorpasso','Chi raggiunge, cioè arriva nel settore del coronamento dell\'altra, le lascia sempre libera la rotta.')]
cc=''.join(card(svgi(300,220,s,f'Vista dall\'alto: {t}',dw=420,dh=308)+h3(t,30)+p(d,24),None,24,10) for s,t,d in MM)
sec('motore', head('COLREG · le regole di rotta','Due barche a motore')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 1.5.2-1 e -46 (rotte opposte: entrambe a dritta), -9, -25, -39, -44 (rotte incrociate: chi vede l\'altra a dritta la lascia passare e passa di poppa; ha precedenza chi viene da dritta), -17, -19, -45, -54, -58 (raggiungente). Segnali sonori di manovra (1 breve = accosto a dritta, 2 brevi = a sinistra; sorpasso) nella lezione 6.')

# ============ DUE BARCHE A VELA ============
def v_mure():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+''.join(arrow(x,10,x,50,GREY,5,14) for x in (40,150,260))
    s+=sailtop(90,160,80,-45,1)+sailtop(220,160,80,-135,-1)
    return s
def v_stesse():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+''.join(arrow(x,10,x,50,GREY,5,14) for x in (40,150,260))
    s+=sailtop(110,110,80,-45,1)+sailtop(190,180,80,-45,1)
    return s
VV=[(v_mure(),'Mure diverse','Chi ha il vento a sinistra (mure a sinistra) lascia libera la rotta a chi ha il vento a dritta. Qui cede la barca di sinistra.'),
    (v_stesse(),'Stesse mure','Chi è sopravento lascia libera la rotta a chi è sottovento. Qui cede la barca più in alto.')]
cc=''.join(card(svgi(300,220,s,f'Vista dall\'alto con vento da Nord: {t}',dw=420,dh=308)+h3(t,30)+p(d,24),None,24,10) for s,t,d in VV)
side=card(note('Vela e motore',CORAL,38)+p('Il motore lascia libera la rotta alla vela, ma la vela che raggiunge cede lo stesso.',25,INK)+note('A vela e a motore',PURPLE,38)+p('Se il motore è acceso sei una barca a motore: valgono le regole del motore.',25,INK),None,30,12,flex='none',extra='; width:420px')
sec('vela', head('COLREG · le regole di rotta','Due barche a vela')+f'<div style="display:flex; gap:24px">{cc}{side}</div>',
 notes='Quiz 1.5.2-6, -15, -31, -32 (mure diverse: chi ha il vento a sinistra cede), -7, -16, -59 (stesse mure: sopravento cede a sottovento), 1.5.2-29 (motore cede alla vela). Nei disegni il boma sta sottovento: se il boma è a dritta il vento arriva da sinistra (mure a sinistra).')

quiz_slide('quiz4','Quiz 5 · Precedenze',['1.5.2-44', '1.5.2-6'],False)
quiz_slide('quiz4r','Quiz 5 · Le risposte',['1.5.2-44', '1.5.2-6'],True)
exec(open('apertura.py').read())
chapter('cap1',1,'Navigazione costiera e punto nave',['Navigare in vista della costa','I luoghi di posizione','Punto nave 1 · due punti cospicui','Punto nave 2 · rilevamento e distanza','Punto nave 2 · rilevamenti successivi'],CORAL,
 'Circa 16 minuti, verifica da 2 quiz compresa: andare spediti, il dettaglio è nelle note.','circa 16 minuti · 5 argomenti',1,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
chapter('caprl',2,'Rilevamenti e GPS',['Rilevamento polare','I rilevamenti: vero, bussola, polare','Dove sono rispetto al faro','Il punto nave: tutte le tecniche','Il GPS'],SUN,
 'Circa 18 minuti, verifica da 2 quiz compresa. È la parte finale della scaletta della scuola: tutti i rilevamenti e le tecniche del punto nave.','circa 18 minuti · 5 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
chapter('cap2',3,'Fanali di navigazione',['I fanali di navigazione','Cosa vedo di notte','Le barche a vela di notte'],PURPLE,
 'Circa 16 minuti, verifica da 2 quiz compresa.','circa 16 minuti · 3 argomenti',1)
chapter('cap3',4,'Segnali diurni e precedenze',['Segnali diurni e luci speciali','Chi lascia la rotta a chi'],BLUE,
 'Circa 12 minuti, verifica da 2 quiz compresa.','circa 12 minuti · 2 argomenti',1)
chapter('cap4',5,'Regole di rotta',['C\'è rischio di collisione?','Due barche a motore','Due barche a vela'],SEA,
 'Circa 13 minuti, verifica da 2 quiz compresa.','circa 13 minuti · 3 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
QZ=[('q01','Quiz 1 · Navigazione costiera',['1.7.6-3','1.7.6-9','1.7.6-23']),('q02','Quiz 2 · Rilevamento polare e traverso',['1.7.6-8','1.7.6-17','1.7.6-29']),
 ('q03','Quiz 3 · Luoghi di posizione',['1.7.6-2','1.7.6-14','1.7.6-38']),('q04','Quiz 4 · Il punto nave',['1.7.6-7','1.7.6-46','1.7.6-47']),
 ('q05','Quiz 5 · GPS',['1.7.3-1','1.7.3-5','1.7.3-9']),('q06','Quiz 6 · I fanali',['1.5.1-5','1.5.1-18','1.5.1-30']),
 ('q07','Quiz 7 · Motore di notte',['1.5.1-1','1.5.1-17','1.5.1-38']),('q08','Quiz 8 · Segnali diurni',['1.5.1-2','1.5.1-21','1.5.1-32']),
 ('q09','Quiz 9 · Luci speciali',['1.5.1-13','1.5.1-19','1.5.1-24']),('q10','Quiz 10 · Rischio di collisione',['1.5.2-3','1.5.2-18','1.5.2-41']),
 ('q11','Quiz 11 · Precedenze a motore',['1.5.2-9','1.5.2-39','1.5.2-46']),('q12','Quiz 12 · Vela, raggiunta, gerarchia',['1.5.2-7','1.5.2-19','1.5.2-29'])]
raccolta(5,6,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Disegna la barca','Fanali e settori: schizza la barca vista dall\'alto con 225°, 112,5° e 135°.'),
  ('Chi è a dritta?','A motore lascia la rotta chi vede l\'altro sulla propria dritta; a vela conta il vento.'),
  ('Attento ai numeri','Gradi, miglia e lunghezze delle navi: 12 e 50 metri cambiano i fanali.')],
 ['Quiz 1-5 · punto nave, rilevamenti e GPS (15)','Quiz 6-9 · fanali e segnali diurni (12)','Quiz 10-12 · rischio di collisione e precedenze (9)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Far rispondere ad alta voce con la lettera, poi chiedere perché le altre due sono sbagliate. Se il tempo stringe, lasciare per casa le slide 3 e 9.',esame=['navigazione', 'colreg'])
closing(['Punto nave: almeno due luoghi di posizione; Rilv = Rilb + V = Pv + ρ','Sono a SW del faro: lo rilevo per 045°, aggiungi o togli 180°','Testa d\'albero 225°, laterali 112,5°, coronamento 135°','Rilevamento costante e distanza che cala: rischio di collisione','Motore: cede a chi viene da dritta; vela: mure a sinistra e sopravento cedono'],
 'Prossima lezione · 06 · Segnalamento, segnali sonori e sicurezza','A casa: i 49 quiz di navigazione costiera, i 13 sul GPS, i 67 su fanali e segnali diurni e i 60 sulle precedenze.')
write_deck(OUT,'Lezione 05 · Punto nave e fanali',
 ['cover','agenda','cap1','costiera','luoghi','pn1','pn2','puntonave','quiz1','quiz1r','caprl','rilevamento','rilevamenti','reciproco','tecniche','gps','quiz1b','quiz1br',
  'cap2','fanali','cosavedo','velanotte','quiz2','quiz2r','cap3','diurni','gerarchia','quiz3','quiz3r',
  'cap4','rischio','motore','vela','quiz4','quiz4r','capquiz','quiz']+[q+s for q,_,_ in QZ for s in ('','r')]+['chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Navigazione costiera, luoghi di posizione, punto nave 1 e 2","start":"cap1"},
  "s3":{"description":"Rilevamento polare, tutti i rilevamenti, tecniche del punto nave, GPS","start":"caprl"},"s4":{"description":"Fanali di navigazione e barche a vela di notte","start":"cap2"},
  "s5":{"description":"Segnali diurni, luci speciali e scala delle precedenze","start":"cap3"},"s6":{"description":"Rischio di collisione e regole di rotta","start":"cap4"},
  "s7":{"description":"Raccolta quiz","start":"capquiz"}})
