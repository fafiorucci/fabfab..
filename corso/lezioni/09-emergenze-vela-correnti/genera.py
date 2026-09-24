import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez09/project'
GREY='#97A6B4'; SKY='#DDEFF7'; LRED='#E23B3B'; ORANGE='#F28C28'; LAND='#F2E2B3'; LAND_S='#C9A96B'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','La vela in otto flash':'sail','La corrente':'current','Dalla prora alla rotta':'dividers',
 'Quale prora per la mia rotta':'compass','Trovare la corrente':'map','La falla':'hull','Incaglio e collisione':'hull','Incendio a bordo':'lifebuoy',
 'Uomo a mare':'lifebuoy','Abbandonare la barca':'lifebuoy','Il VHF di bordo':'lantern','Chiamare aiuto via radio':'lantern','Chi ci aiuta':'flag',
 'Il cattivo tempo':'wind','Alcol, droghe e farmaci':'check'})
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=24,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def pol(cx,cy,b,r): return (cx+r*math.sin(math.radians(b)), cy-r*math.cos(math.radians(b)))
def windarrow(x,y,l=110,c=GREY): return arrow(x,y,x,y+l,c,8,26)
def grid(x0,y0,x1,y1,st,c='#DDE6EC'):
    s=''.join(line(x,y0,x,y1,c,2) for x in range(x0,x1+1,st))+''.join(line(x0,y,x1,y,c,2) for y in range(y0,y1+1,st))
    return s
def dot(x,y,c=NAVY,r=12): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#FFFFFF" stroke-width="4"/>'
def flame(x,y,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 30 Q-26 10 -12 -22 Q-6 -8 0 -12 Q2 -34 16 -44 Q14 -20 24 -6 Q30 16 0 30 Z" fill="{ORANGE}"/><path d="M0 26 Q-12 12 -4 -6 Q2 4 6 -2 Q14 10 0 26 Z" fill="{SUN}"/></g>'
def person(x,y,c=CORAL,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-16" r="11" fill="#F2C9A0" stroke="{NAVY}" stroke-width="2"/><path d="M-14 -4 Q0 -10 14 -4 L12 16 L-12 16 Z" fill="{c}"/></g>'
def ring(x,y,r=22): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ORANGE}" stroke-width="{r*0.55:.0f}"/><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.55:.0f}" stroke-dasharray="{r*0.8:.0f} {r*0.8:.0f}"/>'
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(9,'Emergenze, ripasso vela e correnti','Ripassare la vela, risolvere il primo problema di corrente e sapere cosa fare quando le cose vanno storte',
 'Lezione 9. Capitoli del programma della scuola: Vela (ripasso, 1c), Carteggio (Pv, Vp, Rv, Ve e primo problema di corrente, 7), Sicurezza parte 2 (falla, incaglio, collisione, incendio, uomo a mare, abbandono, VHF, soccorso, tempo cattivo, 3). Aggiunte dall\'All. A al DM 323/2021: CIRM (3b) e alcol e sostanze (3a). È l\'ultima lezione di teoria: dalla 10 si passa al carteggio.')
blocks=[('0:00','20′','Ripasso vela · quiz 1',PURPLE),('0:20','30′','Corrente: prora, rotta e i tre problemi · quiz 2',SEA),('0:50','30′','Falla, incaglio, collisione, incendio, uomo a mare, abbandono · quiz 3',CORAL),('1:20','25′','VHF, soccorso, CIRM, cattivo tempo, alcol · quiz 4',BLUE),('1:45','15′','Verifica finale',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">2 + 5</p>'+p('domande su 20 di sicurezza, e i 5 quesiti di vela',26,INK,700)+p('Le correnti tornano negli esercizi di carteggio 5.x.1 (lezioni 13-15).',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>risolvere un problema di corrente sulla carta</li><li>tamponare una falla e gestire un incendio</li><li>recuperare un uomo a mare</li><li>lanciare un MAYDAY sul canale 16</li><li>prepararti al cattivo tempo</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 09 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie e una finale, tutti quiz ufficiali (DD 131/2022). Banca: sinistri 36 quiz (1.3.6), abbandono e soccorso 13 (1.3.7) più il CIRM (1.3.2.113), tempo cattivo 25 (1.3.8), radio 29 (1.3.9) più 1.3.5, alcol 12 (1.3.2), prora e rotta 30 (1.7.7), vela 250.')

# ============ RIPASSO VELA ============
RV=[('Andature','Bolina 45°, traverso 90°, lasco 135°, poppa 180°. Controvento: angolo morto.',CORAL,CORAL_T),
    ('Apparente','Sempre più a prua del reale; di bolina più forte, in poppa più debole.',SEA,SEA_T),
    ('Mure','Il lato da cui entra il vento. Mure a dritta: precedenza.',PURPLE,LILAC_T),
    ('Stesse mure','Chi è sopravento si scosta da chi è sottovento.',BLUE,BLUE_T),
    ('CV e CD','CV a proravia del CD: poggiera. A poppavia: orziera.',GREEN,GREEN_T),
    ('Virata e abbattuta','Prua nel vento, poppa nel vento. La strambata è l\'abbattuta involontaria.',CORAL,SUN_T),
    ('Fisse e correnti','Stralli e sartie reggono l\'albero; drizze e scotte manovrano le vele.',SEA,SEA_T),
    ('Ridurre','Se ci pensi, è il momento: terzaroli e genoa avvolto.',PURPLE,LILAC_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:44px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in RV)
sec('ripassovela', head('Vela · ripasso','La vela in otto flash')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div>'+note('Quiz di vela: tutti Vero o Falso. Diffida di «sempre», «solo», «esclusivamente».',PURPLE,36),
 notes='Ripasso della lezione 8 in forma di domande rapide: per ogni riquadro chiedere alla classe prima di scoprirlo. Riferimenti: 2.1.1-16…-24 e -50…-54 (andature), -8…-15 e -20…-23 (vento apparente), 2.3.1-5, -7, -44…-49 (precedenze), 2.1.1-29…-34, -64, -65 (CV e CD), 2.3.1-9, -40, -61…-63 (virata, abbattuta, strambata), 2.2.1-28, -29, -75, -77 (manovre fisse e correnti), 2.3.1-58…-60 (ridurre).')
quiz_slide('quiz1','Quiz 1 · Ripasso vela',['2.1.1-55','2.2.1-34','2.3.1-44','2.1.1-89'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['2.1.1-55','2.2.1-34','2.3.1-44','2.1.1-89'],True)

# ============ LA CORRENTE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.12"/>'
for x,y in ((250,80),(520,60),(800,90),(380,420),(700,440),(960,380)):
    b+=f'<path d="M{x} {y} q14 40 0 80 q-14 40 0 80" fill="none" stroke="{SEA}" stroke-width="5" stroke-opacity="0.45" stroke-linecap="round"/>'+head_at(x,y+160,90,SEA,18).replace('<polygon','<polygon fill-opacity="0.45"')
A=(120,250); ang=16; Lr=860
E=(A[0]+Lr*math.cos(math.radians(ang)), A[1]+Lr*math.sin(math.radians(ang)))
b+=dash(A[0],A[1],1000,A[1],NAVY,4)+arrow(A[0],A[1],E[0],E[1],CORAL,7,24)
b+=f'<path d="M{A[0]+220} {A[1]} A220 220 0 0 1 {A[0]+220*math.cos(math.radians(ang)):.1f} {A[1]+220*math.sin(math.radians(ang)):.1f}" fill="none" stroke="{PURPLE}" stroke-width="5"/>'
b+=topboat(A[0]+90,A[1],120,0,'#FFFFFF',NAVY,4)+dot(A[0],A[1])
lbl=pill(X+760,Y+A[1]-54,240,'prora vera Pv',NAVY,22)+pill(X+700,Y+E[1]-70,300,'rotta vera Rv',CORAL,22)+pill(X+A[0]+240,Y+A[1]+24,200,'deriva',PURPLE,22)
lbl+=pill(X+40,Y+520,420,'corrente: va verso Dc a Vc nodi',SEA,22)
txt=term('Corrente «verso»','La direzione della corrente Dc è quella verso cui va, al contrario del vento. Vc è la sua velocità in nodi.')+term('Tocca tutti allo stesso modo','La deriva non dipende dallo scafo: tutta l\'acqua si sposta, e la barca con lei.')+term('Il moto effettivo','Prora Pv e velocità propria Vp sono il moto sull\'acqua. Rotta Rv e velocità effettiva Ve sono il moto sul fondo: quello che vede il GPS.')
sec('corrente', head('Carteggio · la corrente','La corrente')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Barca con prora vera verso est e corrente verso sud: la rotta vera effettiva devia verso sud della prora, di un angolo chiamato deriva')+lbl,
 notes='Richiamo della lezione 4 (prorarotta, deriva, regole). Quiz 1.7.7-1, -2, -3 (rotta vera rispetto al fondo), -4 e -8 (prora), -11 e -15 (Vp dalle sole eliche), -13 e -17 (moto effettivo Rv e Ve, rispetto al fondo), -14, -24, -25, -27 (deriva dovuta alla corrente), -16 (non dipende dal tipo di scafo), -22 (la corrente 180 va verso sud), -29 (vento e corrente 180 con rotta nord), -30 (Pv = Rv solo con corrente di prora o di poppa).')

# ============ PRIMO PROBLEMA ============
X=128
k=120; A=(150,150); B=(A[0]+6*k,A[1]); C=(B[0],B[1]+2*k)
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FBFDFE"/>'+grid(30,30,1062,590,60)
b+=arrow(A[0],A[1],B[0]-6,B[1],NAVY,7,24)+arrow(B[0],B[1],C[0],C[1]-6,SEA,7,24)+arrow(A[0],A[1],C[0]-4,C[1]-2,CORAL,9,28)
a2=math.degrees(math.atan2(C[1]-A[1],C[0]-A[0]))
b+=f'<path d="M{A[0]+160} {A[1]} A160 160 0 0 1 {A[0]+160*math.cos(math.radians(a2)):.1f} {A[1]+160*math.sin(math.radians(a2)):.1f}" fill="none" stroke="{PURPLE}" stroke-width="5"/>'
b+=dot(*A)+dot(*B,SEA)+dot(*C,CORAL)
b+=line(60,560,180,560,NAVY,5)+line(60,550,60,570,NAVY,3)+line(180,550,180,570,NAVY,3)
lbl=pill(X+A[0]+170,Y+A[1]-60,420,'Pv 090° · Vp 6 kn: 6 miglia in 1 ora',NAVY,22)+pill(X+B[0]+24,Y+A[1]+90,200,'Dc 180° · Vc 2 kn',SEA,22)
lbl+=pill(X+300,Y+C[1]+10,380,'Rv 108° · Ve 6,3 kn',CORAL,26)+pill(X+A[0]+170,Y+A[1]+40,110,'18°',PURPLE,22)
lbl+=lab(X+A[0]-110,Y+A[1]-60,100,'A',NAVY,30,900,'right')+lab(X+B[0]+20,Y+B[1]-50,200,'stimato',SEA,24,900)+lab(X+C[0]+24,Y+C[1]-16,240,'effettivo',CORAL,24,900)+lab(X+56,Y+500,240,'1 miglio = 2 quadretti',NAVY,22,800)
txt=term('Il problema','Conosci prora e velocità propria (Pv, Vp) e la corrente (Dc, Vc). Dove vai davvero?')+'<ol style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>Da A traccia la Pv e prendi Vp miglia: punto stimato dopo 1 ora.</li><li>Da lì traccia la Dc e prendi Vc miglia.</li><li>Unisci A con l\'ultimo punto: la direzione è la Rv, la lunghezza in miglia è la Ve.</li></ol>'
sec('problema1', head('Carteggio · il primo problema','Dalla prora alla rotta'), pinned=svgp(X,Y,W,Hh,b,'Triangolo delle velocità su una quadrettatura: da A sei miglia verso est con la prora, poi due miglia verso sud con la corrente; la linea da A al punto finale è la rotta vera 108 gradi con velocità effettiva 6,3 nodi')+lbl+pcol(txt,532,20),
 notes='Esempio didattico, non preso dalla banca: Pv 090°, Vp 6 kn, Dc 180°, Vc 2 kn. Rv = 090° + arctan(2/6) ≈ 108°; Ve = √(36 + 4) ≈ 6,3 kn. Sulla carta si lavora con le miglia percorse in un\'ora (o nel tempo dato: tutto moltiplicato per lo stesso tempo) e si misura la Rv con le squadrette sulla rosa e la Ve con il compasso sulla scala delle latitudini. Esercizi ufficiali del tipo 5.x.1 nelle lezioni 13-15.')
X=700

# ============ SECONDO PROBLEMA ============
k=110; A=(130,190); D=(A[0],A[1]+2*k); r=6*k
ex=A[0]+math.sqrt(r*r-(D[1]-A[1])**2); E=(ex,A[1])
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FBFDFE"/>'+grid(20,20,1072,600,55)
b+=dash(A[0],A[1],1040,A[1],CORAL,4)+arrow(A[0],A[1],D[0],D[1]-6,SEA,7,24)+arrow(D[0],D[1],E[0]-4,E[1]+4,NAVY,7,24)
th0=math.degrees(math.atan2(E[1]-D[1],E[0]-D[0]))
b+=f'<path d="M{D[0]+r*math.cos(math.radians(th0-10)):.1f} {D[1]+r*math.sin(math.radians(th0-10)):.1f} A{r} {r} 0 0 1 {D[0]+r*math.cos(math.radians(th0+10)):.1f} {D[1]+r*math.sin(math.radians(th0+10)):.1f}" fill="none" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="10 8"/>'
b+=dot(*A)+dot(*D,SEA)+dot(*E,CORAL)
lbl=pill(X+A[0]+280,Y+A[1]-60,420,'Rv voluta 090°: la linea da seguire',CORAL,22)+pill(X+A[0]+24,Y+D[1]+14,200,'Dc 180° · Vc 2 kn',SEA,22)
lbl+=pill(X+430,Y+330,240,'Pv 071° · Vp 6',NAVY,24)+pill(X+E[0]-60,Y+A[1]+26,220,'Ve 5,7 kn',CORAL,24)+lab(X+A[0]-100,Y+A[1]-54,90,'A',NAVY,30,900,'right')
lbl+=lab(X+E[0]+20,Y+A[1]-120,300,'compasso aperto di Vp',PURPLE,22,800)
txt=term('Il problema inverso','Vuoi seguire una rotta: che prora tengo?')+'<ol style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>Da A traccia la Rv voluta.</li><li>Sempre da A traccia la corrente: Dc per Vc miglia.</li><li>Dalla punta apri il compasso di Vp e taglia la Rv.</li><li>Da quella punta al taglio: la Pv. Da A al taglio: la Ve.</li></ol>'+note('La prora punta un po\' verso la corrente.',SEA,34)
sec('problema2', head('Carteggio · il problema inverso','Quale prora per la mia rotta')+col(txt,520,16), pinned=svgp(X,Y,W,Hh,b,'Costruzione su quadrettatura: da A la corrente verso sud per 2 miglia, poi un arco di 6 miglia che taglia la rotta voluta verso est; la prora da tenere è 071 gradi e la velocità effettiva 5,7 nodi')+lbl,
 notes='Esempio didattico: Rv 090°, Vp 6 kn, Dc 180°, Vc 2 kn. La corrente è perpendicolare alla rotta: sin(correzione) = 2/6, correzione ≈ 19,5°, quindi Pv ≈ 070,5° ≈ 071°; Ve = 6 · cos 19,5° ≈ 5,7 kn. È il caso più frequente negli esercizi ufficiali: raggiungere un punto con la corrente presente, trovare Pv, Ve e il tempo (es. 5.1.1-1: Vp da impostare per arrivare in 30 minuti).')

# ============ TERZO PROBLEMA ============
X=128
k=90; A=(420,560); S=(A[0],A[1]-5*k); O=(S[0]+1.5*k*math.sin(math.radians(120))*1.0, S[1]-1.5*k*math.cos(math.radians(120)))
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FBFDFE"/>'+grid(15,20,1080,605,45)
b+=dash(A[0],A[1],S[0],S[1]+10,NAVY,4)+arrow(A[0],A[1]-14,S[0],S[1]+14,NAVY,5,18)+arrow(A[0],A[1],O[0]-4,O[1]+8,CORAL,7,24)+arrow(S[0],S[1],O[0]-8,O[1]-4,SEA,8,26)
b+=dot(*A)+dot(*S,NAVY)+dot(*O,CORAL)
b+=f'<circle cx="{O[0]:.1f}" cy="{O[1]:.1f}" r="34" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="6 6"/>'
lbl=pill(X+S[0]-330,Y+S[1]-20,300,'punto stimato: Pv e Vp',NAVY,22)+pill(X+O[0]+40,Y+O[1]+8,460,'punto osservato: GPS o rilevamenti',CORAL,22)
lbl+=pill(X+S[0]+70,Y+S[1]-70,330,'corrente: Dc 120° · Vc 1,5 kn',SEA,22)+pill(X+A[0]-270,Y+300,250,'Pv 000° · Vp 5 kn',NAVY,22)+lab(X+A[0]-80,Y+A[1]-10,60,'A',NAVY,30,900,'right')+lab(X+A[0]+110,Y+400,320,'rotta e velocità effettive',CORAL,22,800)
txt=term('Il terzo caso','Sai da dove sei partito, la prora e la velocità; dopo un certo tempo fai il punto e ti trovi altrove. La differenza è la corrente.')+term('Come si fa','Segna il punto stimato (Pv per Vp × tempo) e il punto osservato. Dallo stimato all\'osservato: la direzione è la Dc, la distanza diviso il tempo è la Vc.')+term('Esempio','Dopo 1 ora l\'osservato è 1,5 miglia per 120° dallo stimato: Dc 120°, Vc 1,5 kn. In 30 minuti sarebbe stata 3 kn.')
sec('trovacorrente', head('Carteggio · trovare la corrente','Trovare la corrente'), pinned=svgp(X,Y,W,Hh,b,'Da A la barca naviga verso nord per un\'ora: il punto stimato è 5 miglia a nord, il punto osservato 1,5 miglia più a sud-est; la freccia dallo stimato all\'osservato è la corrente')+lbl+pcol(txt,532,20),
 notes='Esempio didattico. È la famiglia di esercizi ufficiali in cui si chiede la direzione della corrente: 5.1.1-2 (Pv 350°, Vp 8,5 kn, punto osservato dopo 48 minuti: Dc 221°÷227°) e 5.1.1-4 (Pv 260°, Vp 6,5 kn, punto dopo 1h10m con due rilevamenti: Dc 027°÷033°). Attenzione al tempo: la distanza stimato-osservato si divide per il tempo trascorso in ore.')
X=700

quiz_slide('quiz2','Quiz 2 · Prora, rotta e corrente',['1.7.7-13','1.7.7-16','1.7.7-1'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.7.7-13','1.7.7-16','1.7.7-1'],True)

# ============ FALLA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
wl=250
hull='M220 120 L220 260 Q230 470 546 500 Q862 470 872 260 L872 120 Z'
b+=f'<rect x="0" y="{wl}" width="1092" height="{620-wl}" fill="{WATER}" fill-opacity="0.5"/>'+line(0,wl,1092,wl,SEA,3)
b+=f'<path d="{hull}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/><rect x="226" y="330" width="640" height="150" fill="{WATER}" fill-opacity="0.25"/>'
b+=f'<path d="{hull}" fill="none" stroke="{NAVY}" stroke-width="6"/>'+line(220,120,872,120,NAVY,8)
hx,hy=820,400
b+=f'<ellipse cx="{hx+44}" cy="{hy}" rx="16" ry="40" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/>'
b+=''.join(arrow(1010,hy+dy,hx+70,hy+dy,SEA,5,16) for dy in (-30,0,30))
b+=f'<path d="M{hx-6} {hy} q-60 10 -90 50" fill="none" stroke="{WATER}" stroke-width="10" stroke-linecap="round" stroke-dasharray="4 10"/>'
b+=f'<rect x="330" y="420" width="70" height="46" rx="10" fill="{NAVY}"/><path d="M365 420 L365 180 Q365 150 330 150 L180 150 Q150 150 150 180 L150 240" fill="none" stroke="{GREY}" stroke-width="10"/>'+arrow(150,236,150,300,WATER,6,18)
b+=dim(960,120,960,wl,CORAL)
lbl=pill(X+812,Y+318,300,'tampone dall\'esterno',ORANGE,22)+pill(X+800,Y+452,280,'pressione dell\'acqua',SEA,22)+pill(X+410,Y+440,220,'pompa di sentina',NAVY,22)
lbl+=pill(X+880,Y+140,190,'riserva di spinta',CORAL,22)+lab(X+620,Y+520,300,'acqua che entra',SEA,22,800)
txt=term('Perché è grave','Ogni litro che entra toglie riserva di spinta: il volume stagno sopra la linea di galleggiamento.')+term('Tappare','Il tampone va messo da fuori: la pressione dell\'acqua lo spinge contro lo scafo. Per una falla grande: tele cerate, materassi, cuscini.')+term('Rallentare ed esaurire','Falla a prua: ferma la barca, l\'avanzamento spinge dentro altra acqua. Se è piccola basta la pompa di sentina; se è irreparabile, MAYDAY.')
sec('falla', head('Sicurezza · i sinistri','La falla')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione di uno scafo con una falla sotto la linea di galleggiamento: il tampone è applicato dall\'esterno e la pressione dell\'acqua lo spinge contro lo scafo; dentro, la pompa di sentina scarica l\'acqua fuori bordo')+lbl,
 notes='Quiz 1.3.6-1 (tamponare dall\'esterno), -9 (materiali ingombranti per falle grandi), -5 (falla a prua: arrestare il moto), -6 (falla lieve: pompa di sentina), -7 (riserva di spinta), 1.3.5-1 (falla irreparabile: MAYDAY e salvezza delle persone). Si può anche sbandare la barca sul lato opposto per portare la falla fuori dall\'acqua (e non sul lato della falla, come dice una risposta sbagliata della 1.3.6-1).')

# ============ INCAGLIO E COLLISIONE ============
def incaglio():
    s=f'<rect x="0" y="0" width="700" height="250" fill="{SKY}"/><rect x="0" y="120" width="700" height="130" fill="{WATER}" fill-opacity="0.45"/>'
    s+=f'<path d="M0 250 L0 220 Q180 200 300 170 Q380 150 460 190 Q560 225 700 215 L700 250 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
    s+=f'<g transform="rotate(-6 350 140)"><path d="M180 110 L520 100 Q510 150 470 162 L230 164 Q190 150 180 110 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><path d="M280 100 L420 96 L400 70 L300 72 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/></g>'
    s+=arrow(620,200,620,70,SEA,6,20)+f'<path d="M560 60 q20 -10 40 0 t40 0" fill="none" stroke="{SEA}" stroke-width="5"/>'
    return s
def collisione():
    s=f'<rect x="0" y="0" width="700" height="250" fill="{WATER}" fill-opacity="0.18"/>'
    s+=topboat(220,140,190,0,'#FFFFFF',NAVY,4)+topboat(470,150,190,200,'#FFFFFF',NAVY,4)
    s+=arrow(120,140,40,140,CORAL,6,18)+curved(220,140,120,-40,-100,CORAL,5)
    s+=f'<path d="M335 110 l12 -18 l6 20 l18 -10 l-8 20 l20 4 l-20 8" fill="none" stroke="{LRED}" stroke-width="5" stroke-linejoin="round"/>'
    return s
IC=[(incaglio(),'Incaglio','Nasce spesso da un punto nave impreciso sottocosta. Per disincagliare valuta fondale, danni e manovra; a volte basta attendere l\'alta marea. L\'incaglio volontario può evitare un naufragio per falla o incendio.',SEA_T),
    (collisione(),'Collisione','Se l\'urto è inevitabile: ferma il motore, metti indietro e accosta per attutire il colpo. Dopo: soccorri se serve e dai all\'altra unità i dati per identificarti.',CORAL_T)]
cc=''.join(card(svgi(700,250,s,t,dw=752,dh=269,pan=False)+h3(t,34)+p(d,26),bg,32,12) for s,t,d,bg in IC)
sec('incaglio', head('Sicurezza · i sinistri','Incaglio e collisione')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 1.3.6-2 (incaglio volontario), -3 (fattori per il disincaglio), -4 (punto nave impreciso), -8 (alta marea), -10 (collisione: fermare, indietro e accostare), 1.3.7-12 (fornire i dati di identificazione, nei limiti del possibile), 1.8.1-4 e -43 (urto senza fornire i dati: sanzione, lezione 7), 1.8.1-1 e seguenti (evento straordinario: denuncia entro 3 giorni).')

# ============ INCENDIO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.12"/>'+line(546,110,546,600,'#C9D3DD',3)
b+=''.join(windarrow(x,10,80) for x in (516,576))
b+=topboat(270,330,300,-90,'#FFFFFF',NAVY,5)+flame(270,445,1.3)+''.join(f'<circle cx="{270+dx}" cy="{510+i*30}" r="{16+i*6}" fill="{GREY}" fill-opacity="{0.45-i*0.1:.2f}"/>' for i,dx in enumerate((0,8,-6)))
b+=topboat(820,300,300,90,'#FFFFFF',NAVY,5)+flame(820,415,1.3)+''.join(f'<circle cx="{820+dx}" cy="{480+i*30}" r="{16+i*6}" fill="{GREY}" fill-opacity="{0.45-i*0.1:.2f}"/>' for i,dx in enumerate((0,8,-6)))
b+=arrow(270,150,270,120,NAVY,5,16)+arrow(820,160,820,120,NAVY,5,16) if False else ''
lbl=pill(X+40,Y+24,400,'Fuoco a poppa: prua al vento',CORAL,22)+pill(X+620,Y+24,420,'Fuoco a prua: poppa al vento',CORAL,22)
lbl+=lab(X+60,Y+582,440,'il fumo va via da chi è a bordo',NAVY,22,800,'center')+lab(X+600,Y+582,440,'fiamme sempre sottovento',NAVY,22,800,'center')
txt=term('Fiamme sottovento','Manovra perché il fuoco resti sottovento: se è a poppa metti la prua al vento, se è a prua la poppa. Mai correre verso il porto: il vento alimenta il fuoco.')+term('Nel vano motore','Chiudi subito carburante e prese d\'aria. Estintore alla base della fiamma; a polvere sul quadro elettrico.')+term('Le persone prima','Primo ordine: giubbotti e lontano dal fuoco. In porto allontana la barca; se è grave prepara l\'abbandono.')
sec('incendio', head('Sicurezza · i sinistri','Incendio a bordo'), pinned=svgp(X,Y,W,Hh,b,'Due barche viste dall\'alto con il vento da nord: con il fuoco a poppa la barca mette la prua al vento; con il fuoco a prua mette la poppa al vento; in entrambi i casi fiamme e fumo vanno sottovento')+lbl+pcol(txt,532,20),
 notes='Estintori e classi di fuoco nella lezione 6. Quiz 1.3.6-11 (non accelerare verso il porto), -12 e -24 (chiudere carburante e vie d\'aria), -13, -18, -22, -25 (fiamme sottovento: fuoco a poppa prua al vento, fuoco a prua poppa al vento), -14 (base della fiamma), -15 (grave: preparare l\'abbandono), -16 (quadro elettrico: polvere), -17 (giubbotti e allontanarsi), -19 (in porto: allontanare l\'unità), -20 (ventilazione forzata prima di avviare un motore a benzina), -21 e -23 (raffreddamento e soffocamento), -26 e -27 (numero di estintori).')
X=700

# ============ UOMO A MARE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.14"/>'
cx_,cy_,R=520,280,170
b+=dpath(f'M{cx_-R} 600 L{cx_-R} {cy_}',NAVY,5,False)
path=f'M{cx_-R} {cy_} A{R} {R} 0 1 1 {cx_-R*math.cos(math.radians(40)):.1f} {cy_+R*math.sin(math.radians(40)):.1f}'
b+=dpath(path,CORAL,6)
b+=topboat(cx_-R,520,130,-90,'#FFFFFF',NAVY,4)+topboat(cx_+R,cy_,130,90,'#FFFFFF',NAVY,4)
px_,py_=cx_-R+70,cy_+60
b+=person(px_,py_,CORAL,1.2)+ring(px_+44,py_-6,18)
b+=f'<path d="M{cx_+R-20} {cy_-10} L{px_+20} {py_-10}" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="4 8"/>'
b+=num(cx_-R-40,420,1,NAVY,22)+num(cx_-R+20,cy_-60,2,CORAL,22)+num(px_+80,py_+40,3,ORANGE,22)+num(cx_+R+60,cy_-70,4,PURPLE,22)+num(cx_-40,cy_+R+10,5,SEA,22)
lbl=pill(X+40,Y+470,250,'«Uomo a mare a dritta!»',NAVY,22)+pill(X+40,Y+150,320,'accosta dallo stesso lato',CORAL,22)+pill(X+520,Y+368,240,'lancia il salvagente',ORANGE,22)
lbl+=pill(X+790,Y+194,260,'occhi sempre su di lui',PURPLE,22)+pill(X+510,Y+448,300,'arriva piano, in folle',SEA,22)
txt=term('Subito','Grida il lato e accosta da quello stesso lato: la poppa e le eliche si allontanano dal naufrago.')+term('Salvagente e occhi','Lancia l\'anulare vicino al naufrago e fai tenere a qualcuno il controllo visivo, senza mai staccarlo.')+term('L\'avvicinamento','Con prudenza, dopo aver perso velocità: motore in folle vicino alla persona. Col fuoribordo usa lo stacco di sicurezza.')
sec('uomoamare', head('Sicurezza · i sinistri','Uomo a mare')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Manovra di recupero vista dall\'alto: la barca che risale verso nord accosta subito a dritta dal lato del naufrago, compie un giro e torna piano verso di lui; il salvagente anulare è vicino alla persona in acqua')+lbl,
 notes='Quiz 1.3.6-28 (avvicinamento finale con prudenza, dopo aver smaltito la velocità), -29 e -35 (salvagente anulare verso il naufrago), -31, -33, -36 (accostare dallo stesso lato: eliche lontane), -32 e -34 (controllo visivo), 1.3.8-16 (stacco di sicurezza del fuoribordo). Il quiz 1.3.6-30 richiede la figura della banca (uomo caduto a prua lato dritto: manovra B). A vela: segnalare, lanciare l\'anulare, fermare la barca (panna) o accendere il motore controllando che non ci siano cime in acqua.')

# ============ ABBANDONO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="330" width="1092" height="290" fill="{WATER}" fill-opacity="0.5"/>'+line(0,330,1092,330,SEA,3)
b+=f'<g transform="rotate(12 330 330)"><path d="M90 250 L560 240 Q545 330 490 350 L150 352 Q100 330 90 250 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/><path d="M220 240 L420 236 L400 190 L240 192 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/></g>'
b+=f'<rect x="0" y="360" width="1092" height="260" fill="{WATER}" fill-opacity="0.35"/>'
b+=f'<path d="M520 300 Q640 330 740 390" fill="none" stroke="{SUN}" stroke-width="5" stroke-dasharray="10 8"/>'
b+=f'<ellipse cx="820" cy="420" rx="130" ry="36" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><path d="M720 410 Q820 290 920 410 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><path d="M790 400 Q820 360 850 400 Z" fill="{INK}"/>'
b+=person(640,470,SUN,1.4)+person(700,500,SUN,1.4)
b+=f'<rect x="930" y="470" width="80" height="70" rx="14" fill="{NAVY}"/><rect x="956" y="456" width="28" height="18" rx="6" fill="none" stroke="{NAVY}" stroke-width="5"/>'
lbl=pill(X+500,Y+250,300,'sagola legata alla barca',SUN,22,INK)+pill(X+760,Y+300,200,'zattera',ORANGE,22)+pill(X+560,Y+560,220,'giubbotti a tutti',SEA,22)+pill(X+880,Y+560,160,'grab bag',NAVY,22)
lbl+=lab(X+40,Y+30,600,'Prima il MAYDAY, poi l\'abbandono',CORAL,30,900)
txt=term('Lo decide il comandante','Solo dopo aver provato tutto quello che l\'arte nautica consente. Prima fa indossare a tutti il giubbotto e controlla la zattera.')+term('La zattera','Si lega la sagola alla barca e poi si lancia: la sagola la apre e la tiene vicina. Sta in coperta, pronta: mai sottocoperta o in un gavone chiuso.')+term('Il grab bag','La sacca con le dotazioni della zattera, a portata di mano per portarla via.')
sec('abbandono', head('Sicurezza · l\'ultima scelta','Abbandonare la barca'), pinned=svgp(X,Y,W,Hh,b,'Barca inclinata che affonda, collegata con una sagola alla zattera di salvataggio arancione aperta in acqua; persone con i giubbotti e la sacca grab bag')+lbl+pcol(txt,532,20),
 notes='Quiz 1.3.7-1 e -13 (giubbotti a tutti, zattera equipaggiata), -2 (sagola fissata prima di lanciare), -3 e -4 (dove non tenere la zattera), -5 e -6 (grab bag), -11 (l\'abbandono lo ordina il comandante dopo aver accertato di persona che non c\'è altro da fare), 1.3.6-15 (incendio grave: preparare l\'abbandono). Zattera: obbligatoria senza limiti e fino a 50 miglia, costiera fino a 12 (DM 133/2024, lezione 6).')
X=700

quiz_slide('quiz3','Quiz 3 · Sinistri e abbandono',['1.3.6-1','1.3.6-31','1.3.7-2'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.3.6-1','1.3.6-31','1.3.7-2'],True)

# ============ VHF ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
b+=f'<rect x="40" y="170" width="460" height="300" rx="40" fill="{NAVY}"/><path d="M440 170 V50" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<rect x="80" y="210" width="250" height="140" rx="16" fill="#BFE6D9"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="#2B4A6B"/>' for x in range(370,470,26) for y in range(220,350,26))
b+=''.join(f'<rect x="{80+i*70}" y="385" width="56" height="50" rx="12" fill="#2B4A6B"/>' for i in range(3))+f'<rect x="300" y="385" width="160" height="50" rx="12" fill="{LRED}"/>'
cx_,cy_,R=820,320,200
b+=f'<circle cx="{cx_}" cy="{cy_}" r="{R}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="8"/>'
for a0 in (0,180):
    p0=pol(cx_,cy_,a0,R-8); p1=pol(cx_,cy_,a0+18,R-8)
    b+=f'<path d="M{cx_} {cy_} L{p0[0]:.1f} {p0[1]:.1f} A{R-8} {R-8} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{LRED}" fill-opacity="0.85"/>'
b+=''.join(line(*pol(cx_,cy_,a,R-8),*pol(cx_,cy_,a,R-(30 if a%90==0 else 20)),NAVY,5 if a%90==0 else 3) for a in range(0,360,30))
b+=line(cx_,cy_,*pol(cx_,cy_,0,R-50),NAVY,8)+line(cx_,cy_,*pol(cx_,cy_,9,R-30),CORAL,4)+f'<circle cx="{cx_}" cy="{cy_}" r="10" fill="{NAVY}"/>'
lbl=big(X+80,Y+232,250,'16',NAVY,96)+lab(X+300,Y+396,160,'DISTRESS','#FFFFFF',22,900,'center')+lab(X+60,Y+490,460,'Canale 16 · 156,8 MHz',NAVY,26,900,'center')
lbl+=pill(X+cx_+60,Y+cy_-R-10,210,'minuti 00-03',LRED,22)+pill(X+cx_-270,Y+cy_+R-40,210,'minuti 30-33',LRED,22)+lab(X+cx_-200,Y+cy_+R+20,400,'silenzio radio: solo soccorso',NAVY,22,800,'center')
txt=term('Canale 16','Soccorso e prima chiamata; poi ci si sposta su un altro canale. Tra barche: 6, 8, 72, 77. Vicino si usa la potenza ridotta di 1 watt.')+term('Portata','Onde in linea retta: tra barche 10-20 miglia, con le stazioni costiere circa 40.')+term('Chi può usarlo','Serve il certificato limitato di radiotelefonista. Il natante ha un indicativo di chiamata, imbarcazioni e navi il nominativo internazionale.')
sec('vhf', head('Sicurezza · la radio','Il VHF di bordo')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Apparato VHF sul canale 16 e un orologio con in rosso i minuti da 00 a 03 e da 30 a 33, riservati al silenzio radio')+lbl,
 notes='Quiz 1.3.9-1 (certificato limitato di radiotelefonista), -2 e -4 (indicativo di chiamata e nominativo internazionale), -3 (VHF fisso omologato), -5 (esonero dalle ispezioni ordinarie), -8 e -10 (canale 16, 156,8 MHz), -17 e -29 (silenzio ai minuti 00-03 e 30-33), -18 (il 16 solo per la prima chiamata), -21 (canali 6, 8, 72, 77), -22 (1 watt a distanza ravvicinata), -23 (responsabile il comandante), -24, -25, -26 (portata ottica: 10-20 miglia, circa 40 con le costiere), -27 (squelch), -28 (riflettore radar). Meteomar sul 68: lezione 7.')

# ============ MAYDAY ============
script=('<div style="display:flex; flex-direction:column; gap:10px; background:#16324F; padding:36px; border-radius:36px; width:820px">'
 +f'<p style="font-size:24px; font-weight:900; letter-spacing:1px; color:{DACC}">CANALE 16 · ALTA POTENZA</p>'
 +''.join(f'<p style="font-size:28px; line-height:1.35; color:{c}; font-weight:{w}">{t}</p>' for t,c,w in (
   ('MAYDAY MAYDAY MAYDAY','#FFFFFF',900),('Qui «Daphne», «Daphne», «Daphne»',DSOFT,700),('Nominativo IABC2',DSOFT,700),
   ('Posizione 42°45′ N 010°15′ E','#FFFFFF',800),('Falla a prua, stiamo affondando','#FFFFFF',800),('4 persone a bordo, abbandoniamo sulla zattera','#FFFFFF',800),('Passo','#9FB3C8',700)))+'</div>')
MC=[('MAYDAY','Soccorso: pericolo grave e imminente per persone o unità.',LRED,CORAL_T),('PAN PAN','Urgenza: sicurezza di unità o persona a rischio, ma non immediato.',SUN,SUN_T),('SÉCURITÉ','Sicurezza: avvisi di navigazione e di burrasca.',SEA,SEA_T)]
mc=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:22px 26px; border-radius:24px; border-left:10px solid {c}"><p style="font-family:{H}; font-size:36px; font-weight:700; line-height:1.05; color:{INK}">{t} ×3</p>{p(d,24,INK,600,1.35)}</div>' for t,d,c,bg in MC)
sec('mayday', head('Sicurezza · la radio','Chiamare aiuto via radio')+f'<div style="display:flex; gap:28px; align-items:start">{script}<div style="flex:1; display:flex; flex-direction:column; gap:18px">{mc}</div></div>'+note('Chi sente un MAYDAY non risponde a caso: lo rilancia e, se può, presta soccorso. Per zittire il canale: SILENCE MAYDAY (si pronuncia «seelonce»).',CORAL,32),
 notes='Esempio di messaggio con nome e nominativo inventati. Ordine delle informazioni come nel quiz 1.3.9-19: nominativo, posizione, tipo di pericolo. Quiz 1.3.9-12, -14, -16 (MAYDAY tre volte), -13 (PAN PAN), -15 (SÉCURITÉ), -11 (chi riceve rilancia e se possibile soccorre), -20 (SILENCE MAYDAY, pronunciato «seelonce»), 1.3.5-1 (falla irreparabile: MAYDAY), 1.3.8-7 (DSC: il tasto rosso invia in automatico il soccorso con la posizione), 1.3.9-6, -7, -9 (razzi e fuochi a mano: lezione 6).')

# ============ CHI CI AIUTA ============
def tile(n,t,c,bg,size=72): return f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:28px; border-radius:28px"><p style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,25,INK,600,1.35)}</div>'
tiles=f'<div style="display:flex; gap:22px">{tile("1530","Il numero di emergenza della Guardia Costiera, dal telefono.",CORAL,CORAL_T)}{tile("CIRM","Centro Internazionale Radio Medico: consigli medici a distanza per un infortunio grave a bordo.",SEA,SEA_T)}{tile("SAR","Il soccorso in mare lo coordina il Comando generale delle Capitanerie di porto.",PURPLE,LILAC_T)}</div>'
arms=f'<rect x="0" y="0" width="260" height="200" fill="#F4FAFC"/><circle cx="130" cy="70" r="20" fill="#F2C9A0" stroke="{NAVY}" stroke-width="3"/><path d="M104 96 L156 96 L150 176 L110 176 Z" fill="{CORAL}"/>'+line(104,100,40,60,NAVY,8)+line(156,100,220,60,NAVY,8)+dpath('M40 60 Q30 110 60 150',GREY,3)+dpath('M220 60 Q230 110 200 150',GREY,3)+arrow(40,120,54,150,GREY,3,10)+arrow(220,120,206,150,GREY,3,10)
dtxt=p("Se c'è gente in pericolo di vita devi prestare assistenza, se non metti a rischio la tua barca e chi è a bordo; in porto o vicino l'Autorità marittima può chiederti di partecipare al soccorso. Per farti notare: alza e abbassa lentamente le braccia allargate.",28)
dimg=svgi(260,200,arms,"Persona che alza e abbassa lentamente le braccia allargate",dw=260,dh=200,pan=False)
duty=card(f'<div style="display:flex; gap:28px; align-items:center">{dimg}<div style="display:flex; flex-direction:column; gap:10px">{h3("Aiutare e farsi vedere",34)}{dtxt}</div></div>',None,32,0,'none')
sec('soccorso', head('Sicurezza · il soccorso','Chi ci aiuta')+tiles+duty,
 notes='Quiz 1.3.8-25 (1530), 1.3.2.113 (CIRM, unico quiz della voce 3b), 1.3.7-7 (soccorso marittimo: ricerca e salvataggio della vita umana), -8 (coordinamento: Comando generale del Corpo delle Capitanerie di porto), -9 (l\'Autorità marittima può chiedere alle unità in porto o nelle vicinanze di partecipare), -10 (obbligo di assistenza senza rischio per sé), 1.8.1-7…-10 (sanzioni per omesso soccorso, lezione 7), 1.3.8-24 (braccia allargate, segnale di pericolo). Il CIRM risponde 24 ore su 24 via radio, telefono ed e-mail.')

# ============ CATTIVO TEMPO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
for i in range(-4,9):
    x0=-200+i*110
    b+=f'<path d="M{x0} 700 q60 -40 110 -110 t110 -110 t110 -110 t110 -110 t110 -110 t110 -110 t110 -110" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-opacity="0.8"/>'
b+=arrow(60,40,170,150,NAVY,8,26)
b+=topboat(360,330,200,-100,'#FFFFFF',NAVY,5)
b+=topboat(800,330,200,-45,'#FFFFFF',NAVY,5)+line(720,250,880,410,LRED,10)+line(880,250,720,410,LRED,10)
lbl=pill(X+230,Y+460,380,'onde al mascone: alla cappa',GREEN,24)+pill(X+640,Y+460,380,'mai onde al traverso',LRED,24)+lab(X+180,Y+40,300,'onde e vento',NAVY,24,900)
txt=term('Prima che arrivi','Rizza tutto, chiudi oblò, osterigi e prese a mare (non quelle del motore), giubbotti addosso e cinture agganciate.')+term('Da terra o dal mare','Tempesta da terra: vai sottocosta, al ridosso. Dal mare: mettiti alla cappa, onde al mascone e motore quanto basta.')+term('Con le onde','Di prua: trim negativo, prua giù. Di poppa: trim positivo e meno velocità. L\'ancora galleggiante limita l\'intraversamento.')+term('Nebbia','Rallenta, accendi i fanali, fai i segnali; costa vicina: acqua che cambia colore, rumore di frangenti.')
sec('tempocattivo', head('Sicurezza · il mare formato','Il cattivo tempo'), pinned=svgp(X,Y,W,Hh,b,'Onde viste dall\'alto: una barca le prende al mascone, alla cappa, ed è la posizione giusta; un\'altra le prende al traverso ed è barrata in rosso')+lbl+pcol(txt,532,16),
 notes='Quiz 1.3.8-2 e -23 (preparare la barca; chiudere tutto tranne le prese a mare del motore), -3 (tempesta da terra: verso la costa), -4 e -19 (tempesta dal mare: alla cappa, al mascone), -5 (mare in poppa: ridurre), -8 (non al traverso), -9 (puntare leggermente la cresta), -1 e -10 (trim), -11…-14 (flaps; il -15 è oscurato), -16 (stacco di sicurezza), -17 e -6 (nebbia), -20 (risacca), -21 (ancora galleggiante; il -18 è oscurato), -22 (in solitario: cintura e agganciarsi), -24 (braccia per chiamare attenzione).')
X=700

# ============ ALCOL ============
T=[("2.755-15.000 €","la sanzione per chi conduce in stato di ebbrezza, secondo il tasso alcolemico",CORAL,CORAL_T),
   ("3-24 mesi","di sospensione della patente, sempre; revoca se c'è danno all'ambiente",PURPLE,LILAC_T),
   ("5 ore","quanto possono durare gli effetti dell'alcol",SEA,SEA_T),
   ("× 2","la sanzione per alterazione psicofisica, se c'è un sinistro",BLUE,BLUE_T)]
tiles='<div style="display:flex; gap:22px">'+''.join(tile(n,t,c,bg,44) for n,t,c,bg in T)+'</div>'
m1=p("Chi conduce dopo aver assunto stupefacenti o psicotropi: da 2.755 a 11.017 euro. I sedativi con l'alcol sono molto pericolosi: l'attenzione crolla.",27)
m2=p("Tasso tra 0,5 e 0,8 g/l: sanzioni aumentate di un terzo. Oltre 1,5 g/l: patente sempre revocata. Sospesa anche la licenza di navigazione.",27)
more=card(f'<div style="display:flex; gap:32px"><div style="flex:1; display:flex; flex-direction:column; gap:8px">{h3("Droghe e farmaci",32)}{m1}</div><div style="flex:1; display:flex; flex-direction:column; gap:8px">{h3("Unità a noleggio",32)}{m2}</div></div>',None,32,0,'none')
sec('alcol', head('Sicurezza · chi è al comando','Alcol, droghe e farmaci')+tiles+more,
 notes='Voce 3a dell\'All. A, 12 quiz (1.3.2). Quiz 1.3.2-2 (2.755-15.000 euro secondo il tasso), -3 (sospensione da 3 a 24 mesi), -1 e -5 (revoca con danno ambientale), -4 (stupefacenti: 2.755-11.017 euro), -8 (raddoppio in caso di sinistro), -6 e -10 (noleggio), -7 (sospensione della licenza di navigazione), -9 (effetti fino a 5 ore), -11 (sedativi e alcol), -12 (attenzione molto bassa). Le cifre sono quelle delle risposte della banca: il riferimento è l\'art. 53-bis del Codice della nautica.')

quiz_slide('quiz4','Quiz 4 · Radio, cattivo tempo, alcol',['1.3.9-17','1.3.8-3','1.3.2-9'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.3.9-17','1.3.8-3','1.3.2-9'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.3.9-8','1.3.6-13','1.7.7-17'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.3.9-8','1.3.6-13','1.7.7-17'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.3.2.113','1.3.8-8','1.3.9-13'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.3.2.113','1.3.8-8','1.3.9-13'],True)
closing(['Corrente: da A la Pv per Vp miglia, poi la Dc per Vc miglia; la congiungente è Rv e Ve','Falla: tampone da fuori; a prua ferma la barca','Incendio: fiamme sottovento, carburante chiuso, giubbotti a tutti','Uomo a mare: accosta dallo stesso lato, salvagente e occhi sempre su di lui','Canale 16: MAYDAY, PAN PAN, SÉCURITÉ, tre volte ciascuno'],
 'Prossima lezione · 10 · Carteggio: navigazione costiera','A casa: i quiz di sicurezza 1.3.2 e 1.3.5-1.3.9, e il ripasso di vela.')
write_deck(OUT,'Lezione 09 · Emergenze, ripasso vela e correnti',
 ['cover','agenda','ripassovela','quiz1','quiz1r','corrente','problema1','problema2','trovacorrente','quiz2','quiz2r',
  'falla','incaglio','incendio','uomoamare','abbandono','quiz3','quiz3r','vhf','mayday','soccorso','tempocattivo','alcol','quiz4','quiz4r',
  'finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e ripasso della vela","start":"cover"},"s2":{"description":"Correnti: prora e rotta, i tre problemi","start":"corrente"},
  "s3":{"description":"Sinistri: falla, incaglio, collisione, incendio, uomo a mare, abbandono","start":"falla"},
  "s4":{"description":"Radio, soccorso, CIRM, cattivo tempo, alcol","start":"vhf"},"s5":{"description":"Verifica finale","start":"finale1"}})
