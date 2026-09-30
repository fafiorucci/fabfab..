import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez08/project'
GREY='#97A6B4'; SKY='#DDEFF7'; LRED='#E23B3B'; ORANGE='#F28C28'; LAND='#F2E2B3'; LAND_S='#C9A96B'
LB.ICON_T.update({'La prova di carteggio':'dividers','Il metodo per i 5 quesiti':'dividers','La traccia':'map','I 5 quesiti risolti':'map','La lezione di oggi':'lifebuoy','La vela in otto flash':'sail','La corrente':'current','Dalla prora alla rotta':'dividers',
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
cover(8,'Emergenze e carteggio entro 12 miglia','Sapere cosa fare quando le cose vanno storte e risolvere in 20 minuti la prova di carteggio entro 12 miglia',
 'Lezione 8, per tutti i percorsi: è l\'ultima lezione della patente entro 12 miglia a motore. Capitoli: Sicurezza parte 2 (falla, incaglio, collisione, incendio, uomo a mare, abbandono, VHF, soccorso, tempo cattivo, 3) e la prova di carteggio entro 12 miglia (elenco 4.1.1 del DD 131/2022). Aggiunte dall\'All. A al DM 323/2021: CIRM (3b) e alcol e sostanze (3a). La vela è nella lezione 9, solo per chi fa la patente a vela; dalla 10 il carteggio oltre 12 miglia.')
blocks=[('0:00','30′','Falla, incaglio, collisione, incendio, uomo a mare, abbandono · quiz 1',CORAL),('0:30','30′','VHF, soccorso, CIRM, cattivo tempo, alcol · quiz 2',BLUE),('1:00','45′','Carteggio entro 12 miglia: il metodo e due esercizi ufficiali',SEA),('1:45','15′','Verifica finale',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">2 + 5</p>'+p('domande su 20 di sicurezza, e i 5 quesiti del carteggio entro 12 miglia',26,INK,700)+p('Carteggio entro 12: 20 minuti, almeno 4 risposte giuste su 5.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>tamponare una falla e gestire un incendio</li><li>recuperare un uomo a mare</li><li>lanciare un MAYDAY sul canale 16</li><li>prepararti al cattivo tempo</li><li>risolvere in 20 minuti l&#39;esercizio di carteggio entro 12 miglia</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 08 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie e una finale, tutti quiz ufficiali (DD 131/2022). Banca: sinistri 36 quiz (1.3.6), abbandono e soccorso 13 (1.3.7) più il CIRM (1.3.2.113), tempo cattivo 25 (1.3.8), radio 29 (1.3.9) più 1.3.5, alcol 12 (1.3.2), prora e rotta 30 (1.7.7), vela 250.')

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

quiz_slide('quiz1','Quiz 1 · Sinistri e abbandono',['1.3.6-1','1.3.6-31','1.3.7-2'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.3.6-1','1.3.6-31','1.3.7-2'],True)

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

quiz_slide('quiz2','Quiz 2 · Radio, cattivo tempo, alcol',['1.3.9-17','1.3.8-3','1.3.2-9'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.3.9-17','1.3.8-3','1.3.2-9'],True)

# ============ CARTEGGIO ENTRO 12 MIGLIA ============
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
import json as _json, re as _re
import geo, chart
E12={e['id']:e for e in _json.load(open(SP+'/rotta-giusta/site/dati/carteggio_e12.json'))}
def chart_html(S, x, y, w, h, solution, alt):
    body,labels,glabs,sbl,C=chart.render(S,w,h,solution)
    svg=f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px">{body}</svg>'
    html=''; last=-99
    for kind,v,t in glabs:
        if kind=='lat' and 30<v<h-40 and v-last>0:
            html+=lab(x+10,y+v-30,130,t,'#5E6E82',20,800)
    lastx=-999
    for kind,v,t in glabs:
        if kind=='lon' and 60<v<w-230 and v-lastx>150:
            html+=lab(x+v+6,y+h-34,140,t,'#5E6E82',20,800); lastx=v
    sx,sy,L,t=sbl; html+=lab(x+sx,y+sy,max(L,120),t,'#16324F',20,900)
    for lx,ly,lw,t,c,kind in chart.place_labels(labels,w,h,22):
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px">{t}</p>'
    return svg+html
def mid_ll(r):
    r=r.replace('’','').replace("'",'').replace(' ','')
    v=[(int(g)+((float(a)+float(b))/2)/60) for g,a,b in _re.findall(r'(\d+)°\((\d+\.?\d*)÷(\d+\.?\d*)\)',r)]
    return v[0],v[1]
class Ex12:
    def __init__(s,id_,A,B):
        s.ex=E12[id_]; q={x['n']:x['risposta'] for x in s.ex['quesiti']}; s.q=q
        s.P=mid_ll(q[4]); s.Q=mid_ll(q[5]); s.pl=geo.Plane(*s.P)
        s.pts=[(s.P,'A · '+A,'lm'),(s.Q,'B · '+B,'lm')]; s.lines=[]; s.fix_below=False
        s.d=geo.dist(s.pl.xy(*s.P),s.pl.xy(*s.Q))
def pretty(u):
    r=u.replace('’','').replace("'",'').replace(' ','')
    m=_re.findall(r'(\d+)°\((\d+\.?\d*)÷(\d+\.?\d*)\)',r)
    if len(m)==2:
        (g1,a1,b1),(g2,a2,b2)=m; f=lambda x: x.replace('.',',')
        return f'{g1}°{f(a1)}′÷{f(b1)}′ N<br>{g2}°{f(a2)}′÷{f(b2)}′ E'
    return u.replace('.',',').replace('lt,','litri').replace(' n',' nodi')
def fmt(v,n=1): return f'{v:.{n}f}'.replace('.',',')
def hhmm(h): h=h%24; H=int(h); M=int(round((h-H)*60)); H,M=(H+1,0) if M==60 else (H,M); return f'{H:02d}:{M:02d}'
def tr(t): return t.replace('.',',')
def e12_slides(sid,id_,A,B,t0,V=None,t1=None,cons=10,col=SEA):
    S=Ex12(id_,A,B); ex=S.ex
    testo=' '.join(l for l in ex['testo'].split('\n') if not l.upper().startswith('SETTORE'))
    testo=_re.split(r'determinare',testo)[0].strip().rstrip(',')+', determinare i 5 quesiti.'
    sett=ex['testo'].split('\n')[0].title()
    lst=''.join(f'<li><b>{x["n"]}</b> · {x["etichetta"].replace("distanza / var.","distanza").replace("ora o velocità","ora di arrivo" if V else "velocità")}</li>' for x in ex['quesiti'])
    left=f'<div style="display:flex; flex-direction:column; gap:20px; width:700px">{p(testo,28,INK,500,1.42)}<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{col}; padding:6px 18px; border-radius:24px; width:max-content">{sett} · carta 5/D</p><ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px">{lst}</ul></div>'
    sec(sid+'_t', head(f'Esercizio {id_} · carteggio entro 12 miglia','La traccia',col)+left, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell&#39;esercizio {id_} con il punto di partenza e quello di arrivo'),
        notes=f'Esercizio ufficiale {id_} dell\'elenco 4.1.1 (DD 131/2022). In aula: 20 minuti, come all\'esame; poi si corregge con la slide successiva.')
    d=S.d
    if V:
        t=d/V; r2=('Ora di arrivo',f't = d ÷ V = {fmt(d)} ÷ {fmt(V)} = {fmt(t*60,0)} minuti; {t0} + {fmt(t*60,0)}′',hhmm(int(t0[:2])+int(t0[3:])/60+t))
    else:
        t=t1; Vv=d/t; r2=('Velocità',f'V = d ÷ t = {fmt(d)} ÷ {fmt(t,1)} h',f'{fmt(Vv)} nodi')
    fuel=cons*t*1.3
    lat=lambda ll: f'{geo.lat_s(ll[0])}<br>{geo.lon_s(ll[1])}'
    rows=[('1','Distanza','compasso sui due punti, poi sulla scala delle latitudini: 1′ = 1 miglio',f'{fmt(d)} M',S.q[1]),
          ('2',r2[0],r2[1],r2[2],S.q[2]),
          ('3','Carburante',f'{cons} l/h × {fmt(t,2)} h = {fmt(cons*t)} l, + 30% di riserva',f'{fmt(fuel)} litri',S.q[3]),
          ('4','Partenza','squadretta: latitudine sul bordo verticale, longitudine su quello orizzontale',lat(S.P),S.q[4]),
          ('5','Arrivo','come per la partenza',lat(S.Q),S.q[5])]
    tb='<table style="font-size:24px; color:#34465E"><tr><th style="width:6%">Q</th><th style="width:44%">Come</th><th style="width:22%">Risultato</th><th style="width:28%">Forchetta ufficiale</th></tr>'+''.join(f'<tr><td><b>{n}</b></td><td><b>{t_}</b>: {c}</td><td><b>{r}</b></td><td>{pretty(u)}</td></tr>' for n,t_,c,r,u in rows)+'</table>'
    S.lines=[(S.P,S.Q,'rotta',f'{fmt(d)} M')]
    sec(sid+'_s', head(f'Esercizio {id_} · soluzione','I 5 quesiti risolti',col)+f'<div style="width:920px">{tb}</div>', pinned=chart_html(S,1080,290,712,620,True,f'Carta con la rotta dell&#39;esercizio {id_} da A a B e la distanza'),
        notes=f'Soluzione dell\'esercizio {id_}. Le coordinate e la distanza sono ricavate dal centro delle forchette ufficiali; all\'esame basta stare dentro la forchetta. Il carburante comprende il 30% di riserva, come nelle risposte ufficiali (per esempio 1 ora × 10 l/h = 10 litri, più 30% = 13 litri).')

# --- la prova e il metodo ---
fmt_cards=[('1 esercizio','dall&#39;elenco ufficiale 4.1.1: 50 esercizi sulla carta 5/D, in tre settori',CORAL,CORAL_T),
           ('5 quesiti','distanza · ora di arrivo o velocità · carburante · coordinate di partenza · coordinate di arrivo',SEA,SEA_T),
           ('20 minuti','almeno 4 risposte giuste su 5, dentro la forchetta indicata dal Ministero',PURPLE,LILAC_T),
           ('Niente bussola','nessun rilevamento, deviazione o corrente: quelli sono per l&#39;oltre 12 miglia',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in fmt_cards)
sec('provaentro', head('Carteggio · entro 12 miglia','La prova di carteggio')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:22px">{tiles}</div>'+note('Porta: carta 5/D integra, due squadrette, compasso a punte secche, matita morbida, gomma, calcolatrice.',CORAL,36),
 notes='DM 323/2021, art. 6: per la patente entro 12 miglia la prova di carteggio è un quiz di elementi di carteggio con 5 quesiti a risposta singola su un esercizio dell\'elenco 4.1.1 del DD 131/2022; 20 minuti, superata con almeno 4 risposte giuste. Gli strumenti si spiegano nella lezione 3.')
M5=[(1,'Distanza','Apri il compasso tra partenza e arrivo e riportalo sulla <b>scala delle latitudini</b> all&#39;altezza della rotta: 1′ = 1 miglio.',SEA),
    (2,'Ora di arrivo o velocità','<b>t = d ÷ V</b> in ore; ora di arrivo = partenza + t. Se ti danno l&#39;ora di arrivo: <b>V = d ÷ t</b>.',CORAL),
    (3,'Carburante','<b>consumo orario × ore di moto</b>, più il <b>30%</b> di riserva.',PURPLE),
    (4,'Coordinate','Squadretta sul punto: la <b>latitudine</b> si legge sul bordo verticale, la <b>longitudine</b> su quello orizzontale.',BLUE)]
rows=''.join(f'<div style="display:flex; gap:18px; align-items:start"><p style="flex:none; width:56px; font-family:{H}; font-size:32px; font-weight:700; line-height:56px; text-align:center; color:#FFFFFF; background:{c}; border-radius:28px">{n}</p><div style="display:flex; flex-direction:column; gap:4px">{h3(t,32,c)}{p(d,26,BODY,400,1.4)}</div></div>' for n,t,d,c in M5)
cheat=card(tag('Conti veloci',GREEN)+'<ul style="font-size:26px; line-height:1.45; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>30 minuti = 0,5 h · 20 minuti = 0,33 h · 15 minuti = 0,25 h</li><li>6 M a 12 nodi = 30 minuti</li><li>1 h × 10 l/h = 10 l → con riserva <b>13 l</b></li><li>Gradi e primi: 42°48′,5 N · 010°08′,4 E</li></ul>',GREEN_T,32,12,0.9)
sec('metodo12', head('Carteggio · entro 12 miglia','Il metodo per i 5 quesiti')+f'<div style="display:flex; gap:32px"><div style="flex:1.2; display:flex; flex-direction:column; gap:26px">{rows}</div>{cheat}</div>',
 notes='Ripresa delle formule della lezione 3: miglia = nodi × ore, tempo = miglia ÷ nodi, velocità = miglia ÷ ore; carburante con il 30% in più. Le forchette ufficiali accettano di solito ±0,3 miglia sulla distanza, ±3 minuti sull\'ora e ±0,3′ sulle coordinate.')
e12_slides('e1','4.1.1 - 1','Capo S. Andrea','Capo d&#39;Enfola','09:00',V=5.5,col=SEA)
e12_slides('e2','4.1.1 - 35','Talamone','Formica Piccola','08:00',t1=1.0,col=PURPLE)

quiz_slide('finale1','Verifica finale · 1 di 2',['1.3.9-8','1.3.6-13','1.7.5-33'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.3.9-8','1.3.6-13','1.7.5-33'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.3.2.113','1.3.8-8','1.3.9-13'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.3.2.113','1.3.8-8','1.3.9-13'],True)
closing(['Falla: tampone da fuori; a prua ferma la barca','Incendio: fiamme sottovento, carburante chiuso, giubbotti a tutti','Uomo a mare: accosta dallo stesso lato, salvagente e occhi sempre su di lui','Canale 16: MAYDAY, PAN PAN, SÉCURITÉ, tre volte ciascuno','Carteggio entro 12: distanza sulla scala delle latitudini, t = d ÷ V, carburante + 30%, coordinate dai bordi'],
 'Prossima lezione · 09 · Vela (patente a vela) · per il motore entro 12 miglia: l\'esame','A casa: i quiz di sicurezza 1.3.2 e 1.3.5-1.3.9 e i 50 esercizi entro 12 miglia (appendice D, parte 1).')
write_deck(OUT,'Lezione 08 · Emergenze e carteggio entro 12 miglia',
 ['cover','agenda','falla','incaglio','incendio','uomoamare','abbandono','quiz1','quiz1r','vhf','mayday','soccorso','tempocattivo','alcol','quiz2','quiz2r',
  'provaentro','metodo12','e1_t','e1_s','e2_t','e2_s','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Sinistri: falla, incaglio, collisione, incendio, uomo a mare, abbandono","start":"falla"},
  "s3":{"description":"Radio, soccorso, CIRM, cattivo tempo, alcol","start":"vhf"},"s4":{"description":"Carteggio entro 12 miglia: la prova, il metodo, due esercizi ufficiali","start":"provaentro"},
  "s5":{"description":"Verifica finale","start":"finale1"}})
