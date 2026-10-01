import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez03/project'
QUAY='#D9C9A8'; QUAY_T='#EADFC6'; LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; MAG='#C2185B'; SHALLOW='#CFE8F3'
SAND='#F3E3B8'; GREY='#97A6B4'; STEEL='#8E9BAA'; ROCK='#8C7B66'; NIGHT='#0F2238'; SKY='#DDEFF7'; GLOBE='#DFF1F8'; GRID='#8FB3C6'
LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'; MBLACK='#1B2330'; MYEL='#F2C230'; ORANGE='#F28C28'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Ormeggi e attracchi':'anchor','L\'elica e l\'ormeggio':'propeller','Le cime d\'ormeggio':'helm',
 'Ormeggio in andana':'anchor','Ormeggio all\'inglese':'anchor','Ormeggio con vento':'wind','Attracco a boa e gavitello':'lifebuoy',
 'Ancora e salpa-ancora':'anchor','Com\'è fatta un\'ancora':'anchor','Le ancore':'anchor','Regole per l\'ancoraggio':'anchor','Calumo, peso e tenuta':'anchor','Grippia e grippiale':'anchor',
 'Verifica dell\'ancoraggio':'compass','Tipi di ancoraggio':'anchor','Latitudine e longitudine':'map','I meridiani':'map','I paralleli':'map',
 'I circoli massimi':'map','La latitudine':'map','La longitudine':'map','Grado, primo, miglio e nodo':'dividers','Classificazione delle carte nautiche':'map',
 'Pubblicazioni e documenti nautici':'book','La 1111 INT 1':'book','I simboli delle carte nautiche':'map','Elenco dei fari e segnali da nebbia':'lighthouse',
 'Le caratteristiche dei fari':'lighthouse','Le portate dei fari':'lighthouse','Il sistema AISM-IALA':'flag','I segnali laterali':'flag',
 'Pericolo isolato':'flag','Acque sicure':'flag','Segnale speciale':'flag','I segnali cardinali':'compass','Navigazione fluviale':'current',
 'La carta di Mercatore':'map','Meridiani e paralleli sulla carta':'grid','Latitudini crescenti':'dividers','Isogonia e lossodromia':'compass',
 'Carta gnomonica e ortodromia':'map','Raccolta quiz':'quiz','Attracchi, ormeggi, ancoraggi':'anchor','Cartografia e segnalamento marittimo':'map'})

# ---------------- strumenti di disegno ----------------
def bollard(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{NAVY}"/><circle cx="{x}" cy="{y}" r="{r*0.4:.0f}" fill="{SUN}"/>'
def rope(d,c=NAVY,w=6):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="{max(1.5,w/3):.1f}" stroke-dasharray="3 6" stroke-linecap="round"/>'
def chain(d,c=NAVY,w=6): return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="10 5"/>'
def dot(n,c,s=44): return f'<p style="width:{s}px; height:{s}px; border-radius:{s//2}px; background:{c}; color:#FFFFFF; font-weight:900; font-size:{s//2}px; text-align:center; line-height:{s}px; flex:none">{n}</p>'
def item(n,c,t,d,ts=28,ds=24): return f'<div style="display:flex; gap:16px; align-items:start">{dot(n,c)}<div style="display:flex; flex-direction:column; gap:4px">{p(t,ts,INK,800,1.25)}{p(d,ds,BODY)}</div></div>'
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=24,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def glow(x,y,c,r=9):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.6:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.6:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
def windarrow(x1,y1,x2,y2): return arrow(x1,y1,x2,y2,GREY,9,28)
def cards(items,w,h,dw,dh,ts=28,ds=22,gap=20,pad=22):
    return f'<div style="display:flex; gap:{gap}px">'+''.join(card(svgi(w,h,s,alt,dw=dw,dh=dh)+h3(t,ts)+p(d,ds),None,pad,8) for s,t,d,alt in items)+'</div>'
X,Y,W,Hh=700,290,1092,620

def anchor_icon(x,y,s=1,c=NAVY):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round">'
            f'<circle cx="0" cy="-26" r="7"/><path d="M0 -19 V26 M-13 -9 H13 M-24 10 Q-20 28 0 26 Q20 28 24 10"/></g>')

# ---- globo visto dall'equatore ----
def globe(cx,cy,R,lats=(30,60),lons=(35,70),c=GRID,fill=GLOBE):
    s=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{fill}" stroke="{NAVY}" stroke-width="5"/>'
    for la in lats:
        for sg in (1,-1):
            yy=cy-sg*R*math.sin(math.radians(la)); hw=R*math.cos(math.radians(la)); s+=line(cx-hw,yy,cx+hw,yy,c,3)
    for lo in lons: s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{R*math.sin(math.radians(lo)):.1f}" ry="{R}" fill="none" stroke="{c}" stroke-width="3"/>'
    return s
# ---- globo visto dal polo Nord ----
def polar(cx,cy,R,step=15,c=GRID):
    s=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{GLOBE}" stroke="{NAVY}" stroke-width="5"/>'
    s+=''.join(f'<circle cx="{cx}" cy="{cy}" r="{R*k:.0f}" fill="none" stroke="{c}" stroke-width="2"/>' for k in (0.33,0.66))
    for a in range(0,360,step):
        x,y=pol(cx,cy,a,R); s+=line(cx,cy,x,y,c,2)
    return s+f'<circle cx="{cx}" cy="{cy}" r="8" fill="{NAVY}"/>'

# ---- carta di Mercatore ----
def merc_y(la,y0,k): return y0-k*math.log(math.tan(math.radians(45+la/2)))
def mercator(x0,y0,x1,y1,maxlat=70,step=10,dx=60,eq_c=CORAL):
    """reticolo di Mercatore tra x0..x1; equatore a metà altezza; restituisce svg e funzione y(lat)"""
    ym=(y0+y1)/2; k=(ym-y0)/math.log(math.tan(math.radians(45+maxlat/2)))
    yf=lambda la: ym-k*math.log(math.tan(math.radians(45+la/2))) if la>=0 else ym+k*math.log(math.tan(math.radians(45-la/2)))
    s=f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{CHART}" stroke="{NAVY}" stroke-width="3"/>'
    s+=''.join(line(x,y0,x,y1,GRID,2) for x in range(int(x0)+dx,int(x1),dx))
    for la in range(-maxlat,maxlat+1,step):
        s+=line(x0,yf(la),x1,yf(la),eq_c if la==0 else GRID,4 if la==0 else 2)
    return s,yf

# ============ COVER + AGENDA ============
cover(3,'Ormeggi, ancoraggi, carte e segnali','Dalla banchina alla rada, dal globo alla carta nautica: coordinate, fari e segnali AISM-IALA',
 'Lezione 3, due capitoli del programma della scuola: Attracchi, ormeggi e ancoraggi (All. A al DM 323/2021, punto 4b) e Cartografia e segnalamento marittimo (materia 7 e punto 5). Gli ultimi 45 minuti sono una raccolta di quiz ufficiali sui due capitoli. I primi calcoli (S = V × T, carburante), la rosa dei venti e gli strumenti del carteggio sono nella lezione 4.')
blocks=[('0:00','35′','Cap. 1 · Attracchi, ormeggi, ancoraggi',CORAL),('0:35','40′','Cap. 2 · Cartografia e segnalamento marittimo',SEA),('1:15','45′','Raccolta quiz: 18 sul cap. 1 e 18 sul cap. 2',PURPLE)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1.05; color:{INK}">4 + 4 + 2</p>'+p('domande su 20: Manovra e condotta, Navigazione cartografica, Segnalamento',26,INK,700)+p('E il carteggio, la prima prova, si fa sulla carta di Mercatore.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:24px; line-height:1.35; color:#34465E; display:grid; grid-template-columns:1fr 1fr; gap:8px 40px"><li>dare le cime giuste in banchina, anche con il vento</li><li>prendere un gavitello e ormeggiarti in andana</li><li>scegliere l\'ancora, dare fondo e verificare la tenuta</li><li>leggere latitudine e longitudine</li><li>scegliere la carta e riconoscerne i simboli</li><li>riconoscere un faro e i segnali AISM-IALA</li><li>spiegare la carta di Mercatore</li><li>navigare su un fiume</li></ul>',SEA_T,flex=2.2)
sec('agenda', head('Lezione 03 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Due capitoli di teoria e poi 45 minuti di quiz. Capitolo 1: 11 argomenti in circa 35 minuti. Capitolo 2: 26 argomenti in circa 40 minuti, quindi slide essenziali; se il tempo stringe si possono scorrere velocemente pubblicazioni, simboli e carta gnomonica. Banca DD 131/2022: ormeggio e disormeggio 49 quiz (1.4.4), ancoraggio 53 (1.4.3), coordinate 45 (1.7.1), carte e Mercatore 56 (1.7.2), pubblicazioni 8 (1.7.8), fanali e sistema IALA 120 (1.5.3).')

def chapter(id_,n,title,subs,c,notes):
    chips=''.join(f'<p style="font-size:26px; font-weight:800; color:#FFFFFF; background:rgba(255,255,255,0.10); padding:10px 18px; border-radius:18px">{t}</p>' for t in subs)
    sec(id_, header(f'Capitolo {n}',title,LB.ICON_T.get(title,'map'),c,True)+f'<div style="display:flex; flex-wrap:wrap; gap:12px; width:1600px">{chips}</div>', notes=notes, dark=True)

# ================= CAPITOLO 1 =================
chapter('cap1',1,'Attracchi, ormeggi, ancoraggi',['Ormeggi e attracchi','Cime d\'ormeggio','Sistemi di cime d\'attracco','Ormeggio con vento','Attracco a boa e gavitello','Ancora e salpa-ancora','Ancore','Regole per l\'ancoraggio','Grippia e grippiale','Verifica dell\'ancoraggio','Tipi di ancoraggio'],CORAL,
 'Circa 35 minuti. I quiz di questo capitolo sono nella raccolta finale (quiz 1-6).')

# ---- Ormeggi e attracchi: il vocabolario ----
b=f'<rect x="330" y="330" width="762" height="290" fill="{WATER}" fill-opacity="0.2"/>'+line(330,330,1092,330,SEA,3)
b+=f'<rect x="330" y="575" width="762" height="45" fill="{LAND}"/>'
b+=f'<path d="M0 230 L330 230 L330 620 L0 620 Z" fill="{QUAY}" stroke="{NAVY}" stroke-width="4"/><rect x="0" y="222" width="330" height="10" fill="{QUAY_T}"/>'
b+=f'<rect x="226" y="194" width="28" height="36" fill="{NAVY}"/><ellipse cx="240" cy="194" rx="24" ry="9" fill="{NAVY}"/>'
hull='M400 250 L740 250 Q730 420 570 440 Q410 420 400 250 Z'
b+=f'<rect x="490" y="200" width="160" height="52" rx="16" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'+line(570,200,570,20,NAVY,8)
b+=f'<path d="{hull}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/><path d="M403 330 L737 330 Q726 420 570 440 Q414 420 403 330 Z" fill="{CORAL}"/><path d="M402 318 L738 318" stroke="{BLUE}" stroke-width="8"/><path d="{hull}" fill="none" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M560 440 L580 440 L576 540 L564 540 Z" fill="{NAVY}"/>'
b+=line(408,250,408,200,NAVY,4)+line(732,250,732,200,NAVY,4)+line(408,204,732,204,NAVY,3)
b+=f'<rect x="336" y="262" width="58" height="92" rx="29" fill="{BLUE}" stroke="{NAVY}" stroke-width="3"/>'+line(365,262,408,206,NAVY,3)
b+=f'<path d="M412 250 L436 250 L432 242 L416 242 Z" fill="{NAVY}"/><path d="M710 250 L734 250 L730 242 L714 242 Z" fill="{NAVY}"/>'
b+=rope('M420 244 Q330 250 250 204',CORAL,7)
b+=arrow(150,140,222,196,INK,3)+arrow(360,130,330,232,INK,3)+arrow(250,300,334,306,INK,3)+arrow(820,244,740,246,INK,3)
lbl=lab(X+30,Y+100,200,'Bitta',INK)+lab(X+300,Y+88,300,'Cima d\'ormeggio',CORAL)+lab(X+30,Y+280,220,'Parabordo',INK)+lab(X+830,Y+224,220,'Galloccia',INK)+lab(X+40,Y+440,240,'BANCHINA',INK,26,900)
txt=term('Attracco','La manovra di avvicinamento a una banchina o a un galleggiante.')+term('Unità attraccata','È assicurata alla banchina con i cavi d\'ormeggio.')+term('Bitta e galloccia','La bitta è in banchina, la galloccia a bordo: lì si «dà volta» alle cime.')+term('Parabordi','Proteggono lo scafo; si legano a pulpiti e draglie con il nodo parlato.')
sec('attracco', head('Attracchi · il vocabolario','Ormeggi e attracchi')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione trasversale: barca a vela affiancata alla banchina, con parabordo tra scafo e banchina e cima dalla galloccia di bordo alla bitta di banchina')+lbl,
 notes='Quiz 1.4.4-30 (attracco = avvicinamento a banchina o galleggiante), -4 (attraccata = assicurata con i cavi d\'ormeggio), 1.4.4-21 (parlato per i parabordi a pulpiti e draglie). Mostrare in aula una galloccia e come si dà volta.')

# ---- L'elica e l'ormeggio ----
def quay_v(x=380,w=100,h=300): return f'<rect x="{x}" y="0" width="{w}" height="{h}" fill="{QUAY}"/>'+line(x,0,x,h,NAVY,5)
def prop_mark(x,y,cw=True,c=CORAL):
    a0,a1=(200,-20) if cw else (-20,200)
    return curved(x,y,26,a0,a1,c,5)
def inglese_dx():
    s=f'<rect x="0" y="0" width="80" height="300" fill="{QUAY}"/>'+line(80,0,80,300,NAVY,5)
    s+=''.join(bollard(62,y,8) for y in (60,240))
    s+=topboat(230,170,230,-112,'#FFFFFF',NAVY,4)
    s+=arrow(300,262,190,262,CORAL,6,20)+f'<text x="310" y="270" font-family="Arial" font-size="22" font-weight="700" fill="{CORAL}">retro</text>'
    s+=curved(262,230,52,40,150,SEA,5)
    return s
def poppa_giard():
    s=f'<rect x="0" y="0" width="480" height="70" fill="{QUAY}"/>'+line(0,70,480,70,NAVY,5)
    for x in (70,150,330,410): s+=topboat(x,150,150,90,'#FFFFFF',NAVY,3,0.4,False)
    s+=topboat(228,210,150,118,'#FFFFFF',NAVY,4)
    s+=arrow(276,132,286,92,CORAL,6,18)+f'<circle cx="260" cy="155" r="14" fill="none" stroke="{SEA}" stroke-width="5"/>'
    return s
def thruster():
    s=f'<rect x="380" y="0" width="100" height="300" fill="{QUAY}"/>'+line(380,0,380,300,NAVY,5)
    s+=topboat(250,150,250,-90,'#FFFFFF',NAVY,3,0.35,False)+topboat(320,150,250,-90,'#FFFFFF',NAVY,4)
    s+=f'<rect x="298" y="52" width="44" height="12" rx="6" fill="{CORAL}"/>'+arrow(270,58,300,58,CORAL,5,14)+arrow(342,58,372,58,CORAL,5,14)
    return s+arrow(190,230,262,230,SEA,6,20)
EL=[(inglese_dx(),'All\'inglese','Elica <b>destrorsa</b>: in retromarcia la poppa va a sinistra, quindi è facilitato l\'ormeggio con la banchina <b>a sinistra</b>. Sinistrorsa: a dritta.','Vista dall\'alto: barca con elica destrorsa che si accosta alla banchina sulla sua sinistra; in retromarcia la poppa si avvicina alla banchina'),
    (poppa_giard(),'Di poppa','Elica destrorsa: presenta al pontile il <b>giardinetto di sinistra</b>. Elica sinistrorsa: il giardinetto di <b>dritta</b>.','Vista dall\'alto: barca che entra di poppa tra due gruppi di barche ormeggiate, con la poppa inclinata verso il pontile'),
    (thruster(),'Elica di prua','Il <b>bow thruster</b> spinge la prua di lato: per ormeggiarti sul lato dritto accosta a dritta e trasla parallelo alla banchina.','Vista dall\'alto: la barca trasla verso la banchina a dritta grazie all\'elica di prua')]
sec('elica', head('Attracchi · la manovra','L\'elica e l\'ormeggio')+cards(EL,480,300,440,275,30,23,24,24)+note('In retromarcia l\'elica «tira» la poppa: sfruttalo, non combatterlo.',CORAL,36),
 notes='Quiz 1.4.4-31 (all\'inglese con elica destrorsa: banchina a sinistra, marcia indietro), -29 (di poppa con elica sinistrorsa: si presenta il giardinetto di dritta), -23 (bow thruster: accosto a dritta per traslare parallelo alla banchina), -32 (rotazione sul posto con elica e timone). Gli effetti evolutivi dell\'elica sono nella lezione 2.')

# ---- Cime d'ormeggio ----
def coil():
    s=''.join(f'<ellipse cx="160" cy="118" rx="{110-i*18}" ry="{62-i*10}" fill="none" stroke="{BLUE}" stroke-width="12"/>' for i in range(5))
    return s+rope('M270 118 Q300 170 250 205',BLUE,12)
def floating():
    s=f'<rect x="0" y="120" width="320" height="100" fill="{WATER}" fill-opacity="0.25"/>'+line(0,120,320,120,SEA,3)
    s+=rope('M10 60 Q60 40 90 116 Q140 128 190 116 Q220 110 236 118',SUN,10)
    s+=f'<circle cx="266" cy="118" r="34" fill="none" stroke="{CORAL}" stroke-width="18"/>'+''.join(f'<path d="M{266+34*math.cos(math.radians(a))-9:.0f} {118+34*math.sin(math.radians(a)):.0f} l18 0" stroke="#FFFFFF" stroke-width="18"/>' for a in (0,180))
    return s
def bowline():
    s=rope('M160 8 L160 78',CORAL,14)+rope('M146 100 C 70 150, 100 212, 160 212 C 220 212, 250 150, 174 100',CORAL,14)
    s+=f'<ellipse cx="160" cy="92" rx="30" ry="16" fill="none" stroke="{CORAL}" stroke-width="14"/><ellipse cx="160" cy="92" rx="30" ry="16" fill="none" stroke="{NAVY}" stroke-width="2"/>'
    return s+rope('M182 96 Q214 120 204 160',CORAL,12)
def clove():
    s=f'<rect x="0" y="44" width="320" height="20" rx="10" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/>'
    s+=''.join(f'<rect x="{x}" y="30" width="22" height="48" rx="11" fill="{PURPLE}" stroke="{NAVY}" stroke-width="3"/>' for x in (128,172))
    s+=f'<path d="M140 36 L184 72" stroke="{PURPLE}" stroke-width="14" stroke-linecap="round"/>'
    s+=rope('M160 78 L160 118',PURPLE,10)+f'<rect x="126" y="112" width="68" height="104" rx="34" fill="{BLUE}" stroke="{NAVY}" stroke-width="3"/>'
    return s
K=[(coil(),'Poliestere','Robusto e poco elastico: è la fibra delle <b>cime d\'ormeggio</b>.','Matassa di cima in poliestere'),
   (floating(),'Polipropilene','Galleggia: si usa solo per le <b>sagole galleggianti di salvataggio</b>.','Sagola gialla galleggiante collegata a un salvagente anulare'),
   (bowline(),'Gassa d\'amante','Un occhio che non scorre, di <b>grande tenuta</b>: adatto ai cavi d\'ormeggio.','Nodo gassa d\'amante con il suo occhio chiuso'),
   (clove(),'Nodo parlato','Due giri incrociati: per legare i <b>parabordi</b> a pulpiti e draglie.','Nodo parlato su una draglia che regge un parabordo')]
sec('cime', head('Ormeggi · il materiale','Le cime d\'ormeggio')+cards(K,320,220,330,227,30,24,22,24)+note('All\'esame pratico: gassa d\'amante, parlato, nodo di bitta e bozza (All. D).',PURPLE,36),
 notes='Quiz 1.4.4-19 (poliestere per gli ormeggi), -18 (polipropilene solo per sagole galleggianti di salvataggio), -20 (gassa d\'amante), -21 (parlato). L\'All. D al DM 323/2021 chiede di saper fare i nodi: tenere in aula spezzoni di cima e far provare a tutti. Tutti i nodi sono nell\'appendice C.')

# ---- Sistemi di cime: in andana ----
b=f'<rect x="0" y="0" width="1092" height="130" fill="{QUAY}"/>'+line(0,130,1092,130,NAVY,5)
b+=f'<path d="M40 598 L1052 598" stroke="{NAVY}" stroke-width="7" stroke-dasharray="12 7"/>'
for x in (330,762):
    b+=topboat(x,340,380,90,'#FFFFFF',NAVY,3,0.45,False)+rope(f'M{x} 528 L{x} 598',SOFT,4)
b+=rope('M455 124 Q470 420 546 598',SEA,4)
b+=topboat(546,340,380,90,'#FFFFFF',NAVY,4)
b+=rope('M515 168 L610 112',CORAL,7)+rope('M577 168 L482 112',CORAL,7)+rope('M546 528 L546 598',SEA,8)
b+=''.join(bollard(x,112) for x in (482,610))+bollard(455,118,9)
b+=f'<rect x="950" y="560" width="70" height="46" rx="6" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/>'
b+=num(640,150,1,CORAL,20)+num(430,300,2,SEA,20)+num(900,560,3,NAVY,20)+num(990,520,4,PURPLE,20)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+lab(X+620,Y+520,280,'catenaria sul fondo',NAVY,24,800)
txt=item(1,CORAL,'Cime di poppa incrociate','Con la risacca impediscono alla poppa di spostarsi di lato.')+item(2,SEA,'Trappa','Unisce la catenaria alla banchina: la si recupera e diventa l\'ormeggio di prua, verso il largo.')+item(3,NAVY,'Catenaria','La catena posata sul fondo, parallela alla banchina.')+item(4,PURPLE,'Corpo morto','Il blocco di cemento sul fondo a cui è fissata la catena.')
sec('andana', head('Sistemi di cime d\'attracco','Ormeggio in andana')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto: barca ormeggiata di poppa in un marina, con le cime di poppa incrociate e la trappa che dalla prua va alla catenaria sul fondo, ancorata ai corpi morti')+lbl,
 notes='Quiz 1.4.4-7 (cime di poppa incrociate con la risacca), -22 (trappa), -2 (corpo morto: blocco di cemento con un anello). Si ormeggia di poppa (o di prua) con la barca perpendicolare alla banchina, affiancata alle altre: è l\'ormeggio tipico dei nostri porti.')

# ---- Sistemi di cime: all'inglese ----
X=128
b=f'<rect x="0" y="0" width="1092" height="150" fill="{QUAY}"/>'+line(0,150,1092,150,NAVY,5)
b+=''.join(f'<rect x="{x}" y="152" width="44" height="22" rx="11" fill="{BLUE}"/>' for x in (380,524,680))
b+=topboat(546,275,600,0,'#FFFFFF',NAVY,4)
L=[('M790 238 L1000 128',NAVY),('M300 190 L90 128',NAVY),('M770 228 L600 128',CORAL),('M322 186 L490 128',CORAL),('M735 212 L740 128',SEA),('M350 182 L345 128',SEA)]
for d,c in L: b+=rope(d,c,7)
b+=rope('M872 246 L1040 128',PURPLE,5)+rope('M888 256 L1052 138',PURPLE,5)
b+=''.join(bollard(x,128) for x in (90,345,490,600,740,1000,1040))
for (n,x,y,c) in [(1,915,210,NAVY),(6,180,190,NAVY),(2,680,212,CORAL),(5,420,188,CORAL),(3,770,165,SEA),(4,315,158,SEA)]: b+=num(x,y,n,c,20)
b+=arrow(900,470,1000,470,NAVY,4,16)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+lab(X+780,Y+486,200,'prua',NAVY,24,800,'right')+lab(X+860,Y+300,200,'doppino',PURPLE,24,900)
txt=item('1·6',NAVY,'Prodiera e poppiera','Le cime di prua e di poppa.')+item('2·5',CORAL,'Spring','Da prua e da poppa si incrociano verso il centro barca: bloccano i movimenti avanti e indietro.')+item('3·4',SEA,'Traversini','Perpendicolari alla banchina: tengono la barca accostata.')+item('↺',PURPLE,'Doppino','Gira attorno alla bitta e torna a bordo con i due capi: si molla senza scendere a terra.')
sec('inglese', head('Sistemi di cime d\'attracco','Ormeggio all\'inglese'), pinned=pcol(txt+note('Spring e traversini insieme: l\'ormeggio più sicuro.',CORAL,34),540,20)+svgp(X,Y,W,Hh,b,'Vista dall\'alto di una barca ormeggiata di fianco: prodiera, poppiera, due spring incrociati verso il centro, due traversini perpendicolari alla banchina e un doppino a prua')+lbl,
 notes='Quiz 1.4.4-5 e -13 (spring: movimenti longitudinali), -6 (traversini: non far scostare), -8 (doppino), -10, -11, -12 (figure: senza spring la barca si muove lungo l\'asse longitudinale). Nel disegno i numeri sono colorati come le cime in legenda.')
X=700

# ---- Ormeggio con vento ----
b=f'<rect x="0" y="540" width="1092" height="80" fill="{QUAY}"/>'+line(0,540,1092,540,NAVY,5)
for x in (70,160,420,510):
    b+=topboat(x,430,190,-90,'#FFFFFF',NAVY,3,0.45,False)
b+=topboat(290,350,190,-90,'#FFFFFF',NAVY,4)+chain('M290 258 Q250 180 150 96',NAVY,5)+anchor_icon(140,80,0.8,CORAL)
b+=windarrow(40,30,130,110)+windarrow(560,30,650,110)
b+=line(620,20,620,600,'#C9D6DF',3)
b+=topboat(860,410,190,-90,'#FFFFFF',NAVY,4)+topboat(770,430,190,-90,'#FFFFFF',NAVY,3,0.45,False)+topboat(950,430,190,-90,'#FFFFFF',NAVY,3,0.45,False)
b+=rope('M846 500 L790 530',SEA,6)+rope('M874 500 L930 530',CORAL,6)+bollard(790,530,9)+bollard(930,530,9)
b+=num(770,480,'1',SEA,18)+num(952,480,'1',CORAL,18)
lbl=lab(X+30,Y+150,240,'vento',SOFT,24,900)+lab(X+170,Y+30,300,'ancora sopravento',CORAL,24,900)+lab(X+640,Y+180,440,'1ª in arrivo: la cima sopravento',SEA,24,900)+lab(X+640,Y+226,440,'1ª in partenza: la cima sottovento',CORAL,24,900)
txt=term('Senza trappe','Con vento al traverso del posto barca, fila l\'ancora leggermente sopravento rispetto al posto da occupare: la catena compensa lo scarroccio.')+term('In arrivo','Dai volta per prima alla cima di poppa sopravento: tiene la barca contro il vento.')+term('In partenza','Libera per prima la cima sottovento; quella sopravento per ultima.')
sec('vento', head('Ormeggi · con il vento','Ormeggio con vento')+col(txt), pinned=svgp(X,Y,W,Hh,b,'A sinistra una barca che entra di poppa tra le altre con il vento al traverso e l\'ancora filata sopravento; a destra la barca ormeggiata con la cima di poppa sopravento data per prima all\'arrivo e la sottovento liberata per prima alla partenza')+lbl,
 notes='Quiz 1.4.3-47 (vento forte, ormeggio di poppa: si dà fondo leggermente sopravento al posto barca), 1.4.4-14…-17 e -25…-28 (figure: quale cima dare o mollare per prima). La regola: la cima sopravento è quella che lavora, quindi si dà per prima e si molla per ultima.')

# ---- Attracco a boa e gavitello ----
X=128
b=f'<rect x="0" y="200" width="1092" height="420" fill="{WATER}" fill-opacity="0.2"/>'+line(0,200,1092,200,SEA,3)
b+=f'<path d="M0 560 Q270 540 546 562 T1092 552 L1092 620 L0 620 Z" fill="{LAND}"/>'
b+=f'<rect x="660" y="515" width="130" height="58" rx="8" fill="#9AA5B1" stroke="{NAVY}" stroke-width="4"/><circle cx="725" cy="508" r="10" fill="none" stroke="{NAVY}" stroke-width="5"/>'
b+=f'<path d="M725 498 Q690 400 700 320 Q708 250 722 222" fill="none" stroke="{NAVY}" stroke-width="9" stroke-dasharray="11 6"/>'
b+=f'<ellipse cx="724" cy="198" rx="40" ry="26" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/><rect x="684" y="190" width="80" height="12" fill="#FFFFFF"/>'
b+=profile(40,205,470)
b+=rope('M498 150 Q600 175 716 232',SEA,6)
for yy in (60,110): b+=arrow(1040,yy,900,yy,GREY,8,24)
lbl=lab(X+780,Y+130,200,'Gavitello',CORAL)+lab(X+470,Y+250,230,'Cima sotto il gavitello',SEA)+lab(X+740,Y+360,200,'Catena',NAVY)+lab(X+810,Y+470,240,'Corpo morto',INK)+lab(X+900,Y+136,160,'vento',SOFT,24,800)
txt=term('Come arrivare','A lento moto, con la prua al vento o alla corrente: il gavitello si raggiunge sottovento.')+term('Dove legarsi','Alla cima sotto il gavitello, non al gavitello.')+term('Corpo morto','Un blocco di cemento sul fondo con un anello: la catena sale fino al gavitello.')+term('Tra due boe','In sicurezza solo se una boa è a prua e l\'altra a poppa.')
sec('gavitello', head('Ormeggiarsi in rada','Attracco a boa e gavitello'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Sezione sotto il mare: corpo morto sul fondo, catena che sale al gavitello e barca che arriva con la prua al vento e si lega alla cima sotto il gavitello')+lbl,
 notes='Quiz 1.4.4-3 (avvicinamento a lento moto con prora al vento o alla corrente), -41 (sottovento al gavitello), -33 (ci si lega alla cima sotto il gavitello), -2 (corpo morto), -9 (due boe: una a proravia e una a poppavia). L\'ancora galleggiante (1.4.4-42, -44) serve a limitare l\'intraversamento: si vede con il cattivo tempo.')
X=700

# ---- Ancora e salpa-ancora ----
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="470" width="1092" height="150" fill="{WATER}" fill-opacity="0.35"/>'+line(0,470,1092,470,SEA,3)
b+=f'<path d="M40 200 L900 200 Q1010 200 1040 170 L1000 330 Q930 520 700 560 L40 560 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
b+=line(40,380,860,380,NAVY,3)+f'<rect x="120" y="390" width="200" height="160" fill="#E7EEF3"/>'
b+=''.join(f'<ellipse cx="{150+i*26}" cy="{530-(i%3)*10}" rx="16" ry="9" fill="none" stroke="{NAVY}" stroke-width="5"/>' for i in range(7))
b+=f'<rect x="200" y="150" width="120" height="52" rx="10" fill="#9AA5B1" stroke="{NAVY}" stroke-width="4"/><circle cx="340" cy="176" r="36" fill="#C7D0D9" stroke="{NAVY}" stroke-width="5"/><circle cx="340" cy="176" r="12" fill="{NAVY}"/>'
b+=''.join(f'<circle cx="{340+30*math.cos(math.radians(a)):.0f}" cy="{176+30*math.sin(math.radians(a)):.0f}" r="6" fill="{NAVY}"/>' for a in range(0,360,45))
b+=chain('M340 212 L340 380 Q330 440 200 500',NAVY,6)+chain('M376 150 L960 150',NAVY,6)
b+=f'<path d="M930 130 L1060 130 Q1080 150 1050 170 L960 176 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="4"/><circle cx="1040" cy="150" r="10" fill="{NAVY}"/>'
b+=chain('M1040 170 L1040 380',NAVY,6)+f'<g transform="translate(1040 430)">{anchor_icon(0,0,1.4,NAVY)}</g>'
b+=arrow(958,532,1010,462,INK,2.5,11)+arrow(1046,566,1041,474,INK,2.5,11)
for n,x,y,c in [(1,392,110,CORAL),(2,250,110,SEA),(3,640,110,NAVY),(4,1000,90,PURPLE)]: b+=num(x,y,n,c,20)
lbl=lab(X+130,Y+400,190,'pozzo catene',SOFT,22,800,'center')+lab(X+860,Y+528,100,'marra',CORAL,24,900,'right')+lab(X+968,Y+566,120,'diamante',CORAL,24,900,'center')
txt=item(1,CORAL,'Barbotin','Ruota sagomata con l\'impronta della catena.',26,22)+item(2,SEA,'Verricello salpa-ancora','Porta il barbotin e recupera la catena.',26,22)+item(3,NAVY,'Catena','A maglie ellittiche.',26,22)+item(4,PURPLE,'Musone','All\'estrema prua, con il passacatena: accoglie l\'ancora issata.',26,22)
txt+=p('<b>Marra</b>: il braccio che fa presa.',24,INK)+p('<b>Diamante</b>: la parte bassa al centro delle marre.',24,INK)+p('L\'ancora <b>fa testa</b> se tiene, <b>ara</b> se non tiene, <b>speda</b> se si solleva dal fondo.',24,INK)
sec('salpancora', head('Ancoraggi · a bordo','Ancora e salpa-ancora')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Sezione della prua: verricello salpa-ancora con il barbotin sul ponte, catena che scende nel pozzo catene e che corre verso il musone all\'estrema prua, dove è appesa l\'ancora')+lbl,
 notes='Quiz 1.4.3-10 (barbotin), -9 (maglie ellittiche), -16 e -25 (marre), -19 e -33 (diamante), -17 e -31 (fa testa), -24 (ara), -37 (speda). Le altre parti dell\'ancora ammiragliato (cicala, ceppo, fuso, patte) non sono chieste nei quiz.')

# ---- Nomenclatura dell'ancora ----
b=f'<circle cx="560" cy="80" r="28" fill="none" stroke="{NAVY}" stroke-width="12"/>'
b+=f'<rect x="400" y="128" width="320" height="24" rx="12" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/><circle cx="400" cy="140" r="16" fill="{NAVY}"/><circle cx="720" cy="140" r="16" fill="{NAVY}"/>'
b+=f'<rect x="546" y="104" width="28" height="410" rx="10" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M340 390 Q380 530 560 530 Q740 530 780 390" fill="none" stroke="{NAVY}" stroke-width="30" stroke-linecap="round"/><path d="M340 390 Q380 530 560 530 Q740 530 780 390" fill="none" stroke="{STEEL}" stroke-width="18" stroke-linecap="round"/>'
b+=f'<path d="M340 390 L290 330 L330 318 L372 370 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/><path d="M780 390 L830 330 L790 318 L748 370 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=f'<circle cx="560" cy="530" r="20" fill="{SUN}" stroke="{NAVY}" stroke-width="4"/>'
for i in range(9):
    t=i/8; x=596+t*420; y=74+t*t*160; a=math.degrees(math.atan2(2*t*160/420*1,1))
    if i%2==0: b+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="26" ry="14" fill="none" stroke="{NAVY}" stroke-width="7" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
    else: b+=f'<rect x="{x-26:.0f}" y="{y-4:.0f}" width="52" height="8" rx="4" fill="{NAVY}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
b+=arrow(420,60,528,76,INK,3)+arrow(300,190,398,150,INK,3)+arrow(700,300,580,300,INK,3)+arrow(200,420,330,392,INK,3)+arrow(240,300,300,332,INK,3)+arrow(760,580,584,536,INK,3)
lbl=lab(X+250,Y+40,170,'Cicala',INK,24,800,'right')+lab(X+130,Y+172,170,'Ceppo',INK,24,800,'right')+lab(X+712,Y+284,200,'Fuso',INK,24,800)+lab(X+40,Y+404,160,'Marra',CORAL,24,900,'right')+lab(X+60,Y+282,180,'Patta',CORAL,24,800,'right')+lab(X+770,Y+560,200,'Diamante',INK,24,900)+lab(X+800,Y+250,260,'catena: maglie ellittiche',NAVY,24,800)
txt=term('Cicala','L\'anello in cima al fuso dove si fissa la catena.')+term('Ceppo','La barra trasversale: fa girare l\'ancora sul fondo così che una marra si pianti.')+term('Fuso','L\'asta centrale che unisce cicala e marre.')+term('Marre e patte','I bracci che fanno presa sul fondo; le patte sono le loro estremità allargate.')+term('Diamante','La parte bassa al centro delle marre: qui si lega la grippia.')
sec('nomenclatura', head('Ancoraggi · le parti','Com\'è fatta un\'ancora')+col(txt,520,18), pinned=svgp(X,Y,W,Hh,b,'Ancora classica ammiragliato con cicala, ceppo, fuso, marre con le patte e diamante, e catena a maglie ellittiche')+lbl,
 notes='Nomenclatura generale sull\'ancora ammiragliato, la più chiara per imparare i nomi; a bordo si usano i tipi della slide seguente. Quiz 1.4.3-16 e -25 (marre), -19 e -33 (diamante), -26 (grippia legata al diamante), -9 (catena a maglie ellittiche).')

# ---- Le ancore ----
def a_shank(h=120): return f'<rect x="146" y="20" width="18" height="{h}" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
def ombrello():
    s=a_shank(130)+f'<circle cx="155" cy="140" r="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    for a in (-60,-25,25,60):
        x2=155+80*math.sin(math.radians(a)); s+=f'<path d="M155 140 L{x2:.0f} {140+60*math.cos(math.radians(a))-110:.0f}" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>'
    return s
def grappino():
    s=a_shank(120)
    for dx,op in ((-1,1),(1,1),(-0.45,0.6),(0.45,0.6)):
        s+=f'<path d="M155 140 Q{155+dx*60:.0f} 150 {155+dx*70:.0f} 100" fill="none" stroke="{NAVY}" stroke-opacity="{op}" stroke-width="10" stroke-linecap="round"/>'
    return s
def bruce():
    return (f'<path d="M150 20 L170 20 L175 120 Q175 150 150 158 L100 150 Q90 120 110 104 L140 130 L150 20 Z" fill="{STEEL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M150 158 L205 130 Q220 112 206 100 L176 124" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/><circle cx="160" cy="34" r="8" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/>')
def danforth():
    return (a_shank(140)+f'<rect x="80" y="150" width="150" height="14" rx="7" fill="{NAVY}"/><path d="M146 160 L96 70 L128 60 L150 150 Z M164 160 L214 70 L182 60 L160 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def cqr():
    return (f'<path d="M110 30 Q150 60 170 110" fill="none" stroke="{STEEL}" stroke-width="16" stroke-linecap="round"/><circle cx="108" cy="28" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M170 100 L100 150 L150 150 L170 170 L190 150 L240 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def mantus():
    return (f'<path d="M60 40 L200 120" stroke="{STEEL}" stroke-width="16" stroke-linecap="round"/><circle cx="58" cy="38" r="11" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M120 150 Q200 70 260 120 L250 160 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/><path d="M200 120 L250 160" stroke="{NAVY}" stroke-width="3"/>')
def ultra():
    return (f'<path d="M50 60 Q150 70 200 120" fill="none" stroke="{STEEL}" stroke-width="16" stroke-linecap="round"/><circle cx="48" cy="58" r="11" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M150 160 Q190 100 260 150 L260 166 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/><path d="M200 120 Q220 150 206 160" fill="none" stroke="{NAVY}" stroke-width="4"/>')
def rocna():
    return (a_shank(120)+f'<path d="M70 120 Q155 190 240 120 L240 140 Q155 205 70 140 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><path d="M80 122 Q155 40 230 122" fill="none" stroke="{NAVY}" stroke-width="7"/>')
def ammiragliato():
    return (f'<rect x="146" y="30" width="18" height="130" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<rect x="95" y="44" width="120" height="12" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M95 115 Q105 172 155 172 Q205 172 215 115" fill="none" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/><path d="M95 115 Q105 172 155 172 Q205 172 215 115" fill="none" stroke="{STEEL}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M95 118 L78 92 L98 86 L108 110 Z M215 118 L232 92 L212 86 L202 110 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def delta():
    return (f'<path d="M100 30 L170 110" stroke="{STEEL}" stroke-width="16" stroke-linecap="round"/><circle cx="98" cy="28" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M170 100 L100 150 L150 150 L170 170 L190 150 L240 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def cqr2(): return cqr()+f'<circle cx="170" cy="104" r="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
TUTTI='tutti i fondali: sabbia, fango, ghiaia, alghe'
AN=[(ammiragliato(),'Ammiragliato','La classica, con ceppo e due marre.','alghe, ghiaia e fondi duri; meno su sabbia e fango',SEA),
    (ombrello(),'Ombrello','Marre richiudibili: piccole unità e gonfiabili.','sabbia e fango, per soste brevi',SEA),
    (grappino(),'Grappino','Quattro marre fisse: solo piccole unità.','roccia e alghe, dove si incastra; soste brevi',SEA),
    (bruce(),'Bruce','Monoblocco con una marra ad ala, senza parti articolate.','sabbia, fango e ghiaia; meno sulle alghe',SEA),
    (danforth(),'Danforth','Due marre piatte articolate; il fuso rientra nell\'occhio di cubia.','sabbia e fango, ottima; non su roccia e alghe',SEA),
    (cqr2(),'CQR','A vomere d\'aratro, con il fuso snodato.',TUTTI,GREEN),
    (delta(),'Delta','A vomere d\'aratro, fuso fisso: si raddrizza da sola.',TUTTI,GREEN),
    (mantus(),'Mantus','Tenuta dinamica: marra a lama.',TUTTI,GREEN),
    (ultra(),'Ultra','Tenuta dinamica: marra concava zavorrata in punta.',TUTTI,GREEN),
    (rocna(),'Rocna','Marra concava con roll-bar: si posiziona sempre bene.',TUTTI,GREEN)]
grid_=''.join(card(svgi(310,190,s,f'Disegno dell\'ancora {t}',dw=170,dh=104)+h3(t,26)+p(d,20,BODY,400,1.25)+f'<p style="font-size:20px; line-height:1.25; font-weight:800; color:{c}">Fondale: {fd}</p>',None,14,4) for s,t,d,fd,c in AN)
sec('ancore', head('Ancoraggi · i modelli','Le ancore')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr 1fr; gap:14px">{grid_}</div>'+note('Sulla roccia nessuna ancora tiene sicura: si usa la grippia con il grippiale.',CORAL,32), gap=18,
 notes='Le dieci ancore più diffuse sulle unità da diporto. Quiz 1.4.3-6 (ombrello per battelli gonfiabili), -7 e -28 (grappino per piccole unità), -39 (Danforth ottima su sabbia e fango), -40 (CQR e Delta per tutti i fondali), -49 (Mantus e Ultra, tenuta dinamica, tutti i fondali), -52 (Rocna con roll-bar). Il quiz 1.4.3-8 sulla Bruce è oscurato. Le indicazioni sui fondali per ammiragliato, ombrello, grappino e Bruce sono di pratica marinara: la banca quiz non le chiede. Altri modelli (Spade, Fortress, Hall delle navi) non sono nei quiz.')

# ---- Regole per l'ancoraggio ----
b=''.join(arrow(x,30,x,110,GREY,8,24) for x in (140,540,940))
b+=f'<path d="M0 0 L1092 0 L1092 20 Q800 40 546 18 Q300 0 0 24 Z" fill="{LAND}"/>'
b+=dpath('M220 480 L220 330',CORAL,5)+topboat(220,300,180,-90,'#FFFFFF',NAVY,4)+anchor_icon(220,180,0.9,CORAL)+num(120,300,1,CORAL,22)
b+=topboat(560,440,180,-90,'#FFFFFF',NAVY,4)+f'<path d="M560 350 L560 190" stroke="{NAVY}" stroke-width="5" stroke-dasharray="10 6"/>'+anchor_icon(560,180,0.9,NAVY)+arrow(640,300,640,420,SEA,6,20)+num(460,440,'2·3',SEA,26)
b+=topboat(900,300,180,-90,'#FFFFFF',NAVY,4)+f'<path d="M900 210 L900 190" stroke="{NAVY}" stroke-width="6"/>'+anchor_icon(900,180,0.9,NAVY)+arrow(980,380,980,260,PURPLE,6,20)+num(800,300,5,PURPLE,22)
lbl=lab(X+60,Y+530,320,'Prua al vento, poco abbrivio: a barca ferma si fila',CORAL,22,800,'center')+lab(X+400,Y+530,320,'Marcia indietro: il calumo si distende e l\'ancora fa testa',SEA,22,800,'center')+lab(X+740,Y+530,320,'Per salpare: un po\' di marcia avanti',PURPLE,22,800,'center')+lab(X+460,Y+120,200,'vento',SOFT,24,800,'center')
txt=p('<b>Prima:</b> controlla divieti e situazione meteomarina locale.',24,INK)
txt+=item(1,CORAL,'Arriva piano, prua al vento','Con il minimo abbrivio; niente rocce né posidonia; misura il fondo con l\'ecoscandaglio.',24,21)
txt+=item(2,CORAL,'A scafo fermo fila','Con vento forte allenta il barbotin e fila in fretta.',24,21)
txt+=item(3,SEA,'Leggera marcia indietro','Distende il calumo, da 3 a 5 volte il fondale, e fa fare testa.',24,21)
txt+=item(4,BLUE,'Mai a murata in rada','Più barche affiancate sono troppo esposte al moto ondoso.',24,21)
txt+=item(5,PURPLE,'Per salpare','Un leggero colpo di marcia avanti toglie tensione alla catena.',24,21)
sec('regole', head('Ancoraggi · passo passo','Regole per l\'ancoraggio')+col(txt,560,14), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto in tre tempi: barca che arriva con la prua al vento e cala l\'ancora, poi arretra filando il calumo, infine per salpare avanza togliendo tensione alla catena')+lbl,
 notes='Quiz 1.4.3-2 (divieti e meteo), -12, -42, -43 (fasi della manovra: prua al vento, abbrivio esaurito, si fila e si indietreggia), -46 (vento forte: filare in fretta allentando il barbotin), -41 e -48 (più unità a murata in baia: sconsigliato), -51 (per salpare: marcia avanti), 1.4.4-47 (ecoscandaglio).')

# ---- Calumo, peso e tenuta ----
X=128
b=f'<rect x="0" y="140" width="1092" height="480" fill="{WATER}" fill-opacity="0.2"/>'+line(0,140,1092,140,SEA,3)
b+=f'<path d="M0 560 Q400 548 700 560 T1092 556 L1092 620 L0 620 Z" fill="{SAND}"/>'
b+=profile(60,146,320)
b+=f'<path d="M300 176 L250 520 L350 520 Z" fill="{SUN}" fill-opacity="0.22"/>'+''.join(f'<path d="M{300-k*14} {230+k*70} Q300 {244+k*70} {300+k*14} {230+k*70}" fill="none" stroke="{SUN}" stroke-width="3"/>' for k in range(4))
b+=f'<path d="M372 108 Q420 120 480 250 Q560 470 720 556 L860 560" fill="none" stroke="{NAVY}" stroke-width="7" stroke-dasharray="12 6"/>'
b+=f'<g transform="translate(900 546) rotate(-90)">{anchor_icon(0,0,1.1)}</g>'
b+=dim(1010,140,1010,556,INK)
lbl=lab(X+880,Y+320,200,'fondale',INK,26,900,bg='#FFFFFF')+lab(X+500,Y+330,220,'calumo',NAVY,26,900,bg='#FFFFFF')+lab(X+740,Y+480,340,'ancora: 1,5-2 kg per metro di scafo',CORAL,22,800)+lab(X+130,Y+320,200,'ecoscandaglio',SUN,22,900)
ex=''.join(f'<div style="display:flex; flex-direction:column; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 14px; border-radius:20px"><p style="font-size:22px; font-weight:800; color:{SOFT}; white-space:nowrap">fondo {a}</p><p style="font-family:{H}; font-size:38px; font-weight:700; color:{CORAL}">{c} m</p></div>' for a,c in [('5 m',15),('9 m',27),('16 m',48)])
txt=term('Calumo','La catena o cima filata per dare fondo all\'ancora: almeno 3 volte il fondale, da 3 a 5 secondo il vento e il mare.')+p('<b>Con mare calmo, almeno:</b>',24,INK)+f'<div style="display:flex; gap:12px">{ex}</div>'
txt+=term('La tenuta dipende','Dalla forma e dal peso dell\'ancora (barca di 10 m: 15-20 kg) e dalla lunghezza del calumo. L\'ancora deve restare orizzontale sul fondo.')
sec('calumo', head('Ancoraggi · la catena','Calumo, peso e tenuta'), pinned=pcol(txt,540,18)+svgp(X,Y,W,Hh,b,'Barca alla fonda: l\'ecoscandaglio misura il fondale, la catena scende dalla prua con una curva e resta distesa sul fondo, l\'ancora giace orizzontale; a destra la misura del fondale')+lbl,
 notes='Quiz 1.4.3-34 (calumo), -50 (minimo 3 volte il fondale), -3 e -32 (da 3 a 5 volte), -27, -29, -30 (16 m → 48 m, 9 m → 27 m, 5 m → 15 m), -1 (tenuta: peso e forma), -21 (10 m: 15-20 kg), -18 (ancora orizzontale). Il quiz 1.4.3-20 sul calumo è oscurato.')
X=700

# ---- Grippia e grippiale ----
b=f'<rect x="0" y="120" width="1092" height="500" fill="{WATER}" fill-opacity="0.22"/>'+line(0,120,1092,120,SEA,3)
b+=f'<path d="M0 560 Q200 540 360 556 L420 520 L470 540 L520 470 L600 500 L660 450 L720 520 L800 540 Q950 548 1092 552 L1092 620 L0 620 Z" fill="{ROCK}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
b+=profile(40,126,300)
b+=chain('M330 96 Q430 140 520 330 Q560 430 600 470',NAVY,6)
b+=f'<g transform="translate(622 470) rotate(-30)">{anchor_icon(0,0,1.2,NAVY)}</g>'
b+=f'<path d="M628 500 Q700 380 760 250 Q800 170 812 132" fill="none" stroke="{ORANGE}" stroke-width="5"/>'
b+=f'<path d="M792 132 L812 96 L832 132 L812 150 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/>'
b+=arrow(900,250,960,170,ORANGE,6,20)
lbl=lab(X+830,Y+60,200,'grippiale',ORANGE,26,900)+lab(X+740,Y+300,200,'grippia',ORANGE,26,900)+lab(X+520,Y+560,200,'fondo roccioso',INK,22,800)+lab(X+330,Y+300,220,'catena',NAVY,24,800)+lab(X+880,Y+280,210,'tirando, l\'ancora esce al contrario',ORANGE,22,800)
txt=term('Quando','Se si deve ancorare su fondali con scogli, relitti o rocce, dove l\'ancora può incastrarsi.')+term('La grippia','Una cima sottile: un capo è legato al diamante dell\'ancora, l\'altro al gavitello.')+term('Il grippiale','Il gavitello che galleggia sopra l\'ancora e segnala dove si trova.')+term('Il recupero','Se l\'ancora non si libera, si tira la grippia: l\'ancora viene su dal diamante, al contrario.')
sec('grippia', head('Ancoraggi · fondali difficili','Grippia e grippiale')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione del fondale roccioso: l\'ancora incastrata sotto uno scoglio, la catena verso la barca e la grippia arancione che dal diamante sale al grippiale in superficie')+lbl,
 notes='Quiz 1.4.3-13 (quando usare grippia e grippiale: fondale roccioso o con relitti), -14 (com\'è fatta la grippia), -26 (si lega al diamante per facilitare il recupero).')

# ---- Verifica dell'ancoraggio ----
def v_point():
    s=f'<path d="M430 0 L480 0 L480 300 L410 300 Q440 150 430 0 Z" fill="{SAND}" stroke="{LAND_S}" stroke-width="3"/>'
    for x,y in ((90,60),(210,40),(300,110),(120,200),(260,230)): s+=topboat(x,y,90,-45,'#FFFFFF',NAVY,3,0.5,False)
    for t,x,y,c in (('A',100,130,CORAL),('B',210,150,GREEN),('C',380,200,CORAL)):
        s+=f'<circle cx="{x}" cy="{y}" r="{60 if t=="B" else 12}" fill="{c}" fill-opacity="{0.12 if t=="B" else 1}" stroke="{c}" stroke-width="3"/>'+f'<text x="{x+16}" y="{y-14}" font-family="Arial" font-size="26" font-weight="900" fill="{c}">{t}</text>'
    return s+windarrow(20,20,70,70)
def v_current():
    s=''.join(topboat(x,y,90,-90,'#FFFFFF',NAVY,3) for x,y in ((100,100),(220,160),(340,90),(160,240),(300,240)))
    s+=windarrow(30,150,110,150)+''.join(arrow(430,y,430,y+70,SEA,6,20) for y in (60,180))
    s+=f'<text x="360" y="40" font-family="Arial" font-size="22" font-weight="800" fill="{SEA}">corrente</text><text x="10" y="200" font-family="Arial" font-size="22" font-weight="800" fill="{SOFT}">vento</text>'
    return s
def v_bearing():
    s=f'<path d="M0 0 L480 0 L480 60 Q360 90 240 50 Q120 20 0 70 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
    s+=f'<circle cx="70" cy="40" r="12" fill="{NAVY}"/><circle cx="410" cy="36" r="12" fill="{NAVY}"/>'
    s+=line(240,230,70,40,CORAL,4)+line(240,230,410,36,CORAL,4)+dash(300,250,70,40,PURPLE,3)+dash(300,250,410,36,PURPLE,3)
    s+=topboat(240,240,90,-90,'#FFFFFF',NAVY,3)+topboat(300,262,90,-90,'#FFFFFF',NAVY,3,0.5)
    return s
VR=[(v_point(),'Scegli il punto','Serve spazio per la ruota, lontano dalla spiaggia e dalle altre barche: qui la <b>B</b>.','Vista dall\'alto di una rada: barche alla fonda orientate al vento e tre punti candidati A, B e C; la B ha spazio per girare'),
    (v_current(),'Vento o corrente?','Con una corrente sostenuta le barche alla fonda non si orientano al vento: la prua va contro la corrente.','Vista dall\'alto: barche alla fonda con la prua verso nord, spinte da una corrente verso sud nonostante il vento da ovest'),
    (v_bearing(),'L\'ancora ara?','Rileva due punti a terra. Se il rilevamento <b>cambia</b>, l\'ancora sta arando.','Vista dall\'alto: due rilevamenti verso due punti cospicui a terra; nella seconda posizione le linee sono cambiate')]
sec('verifica', head('Ancoraggi · il controllo','Verifica dell\'ancoraggio')+cards(VR,480,300,440,275,30,23,24,24)+note('Controlla anche con il GPS: l\'allarme di ancoraggio avvisa se la barca si sposta.',SEA,34),
 notes='Quiz 1.4.3-45 (in figura, rada affollata: la barca B perché ha spazio per la ruota), -44 e -53 (altre figure), -15 (tenuta: rilevamenti successivi di punti cospicui o GPS), -4 (alla ruota serve spazio libero). Nel disegno di destra le linee tratteggiate sono i nuovi rilevamenti, diversi dai primi.')

# ---- Tipi di ancoraggio ----
def t_ruota():
    s=f'<circle cx="240" cy="160" r="120" fill="{SEA}" fill-opacity="0.08" stroke="{SEA}" stroke-width="3" stroke-dasharray="12 8"/>'+anchor_icon(240,160,0.8,NAVY)
    s+=dash(240,160,240,70,NAVY,4)+topboat(240,50,90,-90,'#FFFFFF',NAVY,4)+topboat(330,230,90,40,'#FFFFFF',NAVY,3,0.4,False)+topboat(140,240,90,140,'#FFFFFF',NAVY,3,0.4,False)
    return s
def t_pennello():
    s=anchor_icon(240,40,0.7,NAVY)+anchor_icon(240,120,0.7,CORAL)+line(240,58,240,100,CORAL,4)+line(240,140,240,210,NAVY,4)
    s+=topboat(240,250,90,90,'#FFFFFF',NAVY,4)+curved(240,250,70,200,240,SEA,4)+curved(240,250,70,-20,-60,SEA,4)
    return s
def t_afforcate():
    s=f'<ellipse cx="240" cy="170" rx="70" ry="120" fill="{PURPLE}" fill-opacity="0.08" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="12 8"/>'
    s+=anchor_icon(150,40,0.7,NAVY)+anchor_icon(330,40,0.7,NAVY)+line(240,210,154,64,NAVY,4)+line(240,210,326,64,NAVY,4)+topboat(240,250,90,90,'#FFFFFF',NAVY,4)
    return s
TA=[(t_ruota(),'Alla ruota','Una sola ancora filata da prua: la barca ruota di 360°. Verifica lo spazio; mai una seconda ancora da poppa.','Vista dall\'alto: barca alla ruota con il cerchio di rotazione attorno all\'ancora'),
    (t_pennello(),'Appennellate','Con il tempo critico: al diamante dell\'ancora principale si lega una seconda ancora, il pennello, con 4-6 m di catena.','Vista dall\'alto: due ancore in fila, la seconda legata al diamante della prima con uno spezzone di catena'),
    (t_afforcate(),'Afforcate','Due ancore con i calumi aperti a 45°: il campo di giro diventa un\'ellisse invece di un cerchio.','Vista dall\'alto: barca su due ancore con i calumi aperti a 45 gradi e il campo di giro ellittico')]
sec('tipi', head('Ancoraggi · una o due ancore','Tipi di ancoraggio')+cards(TA,480,300,440,275,30,23,24,24)+note('Nei fiumi: due ancore a 180°, nella direzione della corrente.',PURPLE,34),
 notes='Quiz 1.4.3-35 e -36 (alla ruota), -4 (spazio libero), -23 (non dare un\'ancora supplementare da poppa), -38 (appennellate), -22 (afforcata a 45°), -11 (campo di giro ellittico), -5 (nei fiumi due ancore a 180°).')

# ================= CAPITOLO 2 =================
chapter('cap2',2,'Cartografia e segnalamento marittimo',['Latitudine e longitudine','Meridiani','Paralleli','Circoli massimi','Latitudine','Longitudine','Grado, primo, miglio e nodo','Classificazione delle carte','Pubblicazioni e documenti','1111 INT 1','Simboli delle carte','Elenco dei fari','Caratteristiche dei fari','Portate dei fari','AISM-IALA','Laterali','Pericolo isolato','Acque sicure','Speciale','Cardinali','Navigazione fluviale','Mercatore','Meridiani e paralleli sulla carta','Latitudini crescenti','Isogonia e lossodromia','Carta gnomonica'],SEA,
 'Circa 40 minuti per 26 argomenti: una slide per argomento, da scorrere con ritmo. I quiz di questo capitolo sono nella raccolta finale (quiz 7-12).')

# ---- Latitudine e longitudine ----
cx,cy,R=546,320,270
b=globe(cx,cy,R,(30,60),(35,60))
b+=line(cx,cy-R,cx,cy+R,SEA,7)+line(cx-R,cy,cx+R,cy,CORAL,7)
b+=line(cx,cy,cx+135,cy,BLUE,12)+f'<path d="M{cx+135} {cy} A135 {R} 0 0 0 649 146" fill="none" stroke="{SUN}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<circle cx="649" cy="146" r="13" fill="{CORAL}" stroke="#FFFFFF" stroke-width="4"/><circle cx="{cx}" cy="{cy-R}" r="9" fill="{NAVY}"/><circle cx="{cx}" cy="{cy+R}" r="9" fill="{NAVY}"/>'
b+=arrow(400,92,538,140,INK,3)
lbl=lab(X+466,Y+8,160,'Polo Nord',NAVY,24,800,'center')+lab(X+466,Y+594,160,'Polo Sud',NAVY,24,800,'center')+lab(X+170,Y+60,240,'Greenwich',SEA,24,800,'right')
lbl+=lab(X+830,Y+296,200,'Equatore',CORAL,24,800)+lab(X+668,Y+104,60,'P',CORAL,28,900)
lbl+=lab(X+690,Y+210,160,'φ lat.',INK,26,900,bg=SUN_T)+lab(X+560,Y+334,160,'λ long.',BLUE,26,900,bg='#FFFFFF')
txt=term('Coordinate geografiche','La posizione di un punto si dà con due numeri: latitudine φ e longitudine λ.')+term('Il sistema di riferimento','I poli geografici, l\'equatore e il meridiano di Greenwich.')+term('Latitudine φ','Si legge lungo un meridiano, dall\'equatore.')+term('Longitudine λ','Si legge lungo l\'equatore, da Greenwich.')
sec('coordinate', head('Cartografia · le coordinate','Latitudine e longitudine')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Globo con equatore, meridiano di Greenwich, paralleli e meridiani; il punto P con la sua latitudine lungo il meridiano e la longitudine lungo l\'equatore')+lbl,
 notes='Quiz 1.7.1-7 e -21 (coordinate: latitudine e longitudine), -8 e -24 (equatore, meridiano di Greenwich, poli), -22 (λ longitudine), -25 (φ latitudine), -30 (servono entrambe). Le prossime slide scompongono il disegno: meridiani, paralleli, circoli massimi, poi latitudine e longitudine una alla volta.')

# ---- Meridiani ----
X=128
b=globe(270,320,250,(),(15,30,45,60,75))+line(270,70,270,570,CORAL,7)
b+=arrow(250,40,130,40,BLUE,5,18)+arrow(290,40,410,40,BLUE,5,18)
b+=polar(820,330,210,15)+line(820,330,820,540,CORAL,7)+dash(820,330,820,120,CORAL,4)
b+=arrow(560,330,610,330,GREEN,5,16)+arrow(1080,330,1030,330,GREEN,5,16)
b+=f'<path d="M{pol(820,330,260,235)[0]:.0f} {pol(820,330,260,235)[1]:.0f} A235 235 0 0 1 {pol(820,330,350,235)[0]:.0f} {pol(820,330,350,235)[1]:.0f}" fill="none" stroke="{BLUE}" stroke-width="4"/>'
lbl=lab(X+150,Y+54,110,'W',BLUE,26,900)+lab(X+330,Y+54,110,'E',BLUE,26,900)+lab(X+180,Y+584,180,'Greenwich 000°',CORAL,22,900,'center')
lbl+=lab(X+720,Y+550,200,'Greenwich 000°',CORAL,22,900,'center')+lab(X+700,Y+84,240,'antimeridiano 180°',CORAL,22,900,'center')+lab(X+540,Y+270,100,'090° W',GREEN,22,900)+lab(X+1000,Y+270,100,'090° E',GREEN,22,900)+lab(X+730,Y+24,200,'visto dal polo',SOFT,22,800,'center')
txt=term('Meridiani','Semicerchi che uniscono i poli, con direzione 000°-180°. Sono infiniti: sulla carta se ne traccia uno per grado, 180 a Est e 180 a Ovest.')+term('Greenwich','È il meridiano «zero», 000°: divide l\'emisfero Est da quello Ovest.')+term('Antimeridiano','Il 180°, opposto a Greenwich. Il 90° Est e il 90° Ovest stanno a metà strada.')+term('Stessa longitudine','Tutti i punti di un meridiano hanno la stessa longitudine.')
sec('meridiani', head('Cartografia · il reticolo','I meridiani'), pinned=pcol(txt,540,18)+svgp(X,Y,W,Hh,b,'A sinistra il globo con i meridiani e Greenwich al centro, emisfero Ovest a sinistra ed Est a destra; a destra il globo visto dal polo Nord con Greenwich 000, l\'antimeridiano 180 e i meridiani 090 Est e Ovest')+lbl,
 notes='Quiz 1.7.1-26 e -6 (semicircoli che uniscono i poli), -16 (sono infiniti), -39 (meridiano zero = Greenwich), -41 (il novantesimo meridiano sta a metà tra Greenwich e l\'antimeridiano), -33 (stessa longitudine lungo un meridiano), -44 (longitudine 0°: sul meridiano di Greenwich).')
X=700

# ---- Paralleli ----
cx,cy,R=380,320,270
b=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{GLOBE}" stroke="{NAVY}" stroke-width="5"/>'
for la in range(10,90,10):
    for sg in (1,-1):
        yy=cy-sg*R*math.sin(math.radians(la)); hw=R*math.cos(math.radians(la)); b+=line(cx-hw,yy,cx+hw,yy,BLUE,3)
b+=line(40,cy,760,cy,CORAL,8)+dash(cx,cy-R-30,cx,cy+R+30,LRED,3)
b+=arrow(900,300,900,120,BLUE,5,18)+arrow(900,340,900,520,BLUE,5,18)
lbl=''
for la in (0,20,40,60):
    for sg in ((1,-1) if la else (1,)):
        yy=cy-sg*R*math.sin(math.radians(la)); xx=cx+R*math.cos(math.radians(la))
        lbl+=lab(X+xx+10,Y+yy-16,80,f'{la}°',NAVY,22,900)
lbl+=lab(X+40,Y+cy-44,200,'Equatore 0°',CORAL,24,900)+lab(X+cx-20,Y+0,60,'N',NAVY,30,900)+lab(X+cx-16,Y+592,60,'S',NAVY,30,900)
lbl+=lab(X+820,Y+60,200,'Nord · emisfero boreale',BLUE,22,900,'center')+lab(X+820,Y+530,200,'Sud · emisfero australe',BLUE,22,900,'center')+lab(X+cx-250,Y+10,220,'asse terrestre',LRED,22,800,'right')
txt=term('Paralleli','Circoli minori paralleli all\'equatore e perpendicolari all\'asse di rotazione terrestre. Uno per grado: 90 a Nord e 90 a Sud.')+term('L\'equatore','Il parallelo «zero»: l\'unico circolo massimo. Divide l\'emisfero boreale da quello australe.')+term('Il 90° parallelo','Si riduce a un punto: il polo.')+term('Stessa latitudine','Tutti i punti di un parallelo hanno la stessa latitudine.')
sec('paralleli', head('Cartografia · il reticolo','I paralleli')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Globo con i paralleli ogni 10 gradi dall\'equatore ai poli, l\'asse terrestre tratteggiato e gli emisferi boreale e australe')+lbl,
 notes='Quiz 1.7.1-14 e -18 (paralleli: circoli minori paralleli all\'equatore e perpendicolari all\'asse), -29 e -43 (equatore, emisferi boreale e australe), -40 (il novantesimo parallelo si trova al polo), -32 (stessa latitudine lungo un parallelo), -45 (latitudine 0°: sull\'equatore).')

# ---- Circoli massimi ----
X=128
cx,cy,R=380,320,270
b=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{GLOBE}" stroke="{NAVY}" stroke-width="5"/>'
b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R*0.22:.0f}" fill="{CORAL}" fill-opacity="0.12" stroke="{CORAL}" stroke-width="8"/>'
b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{R*0.36:.0f}" ry="{R}" fill="none" stroke="{SEA}" stroke-width="8"/>'
yy=cy-R*0.77; b+=f'<ellipse cx="{cx}" cy="{yy:.0f}" rx="{R*0.64:.0f}" ry="{R*0.64*0.22:.0f}" fill="none" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="12 8"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="9" fill="{NAVY}"/><circle cx="{cx}" cy="{cy-R}" r="9" fill="{NAVY}"/><circle cx="{cx}" cy="{cy+R}" r="9" fill="{NAVY}"/>'
lbl=lab(X+680,Y+300,380,'Equatore: cerchio massimo',CORAL,24,900)+lab(X+660,Y+440,420,'Greenwich + antimeridiano: cerchio massimo',SEA,24,900)
lbl+=lab(X+640,Y+86,380,'Parallelo: circolo minore',PURPLE,24,900)+lab(X+cx-120,Y+cy+8,240,'centro della Terra',NAVY,20,800,'center')+lab(X+cx-80,Y-4,160,'Polo Nord',NAVY,22,800,'center')
txt=term('Circolo massimo','Un cerchio sulla sfera il cui piano passa per il centro della Terra: divide la sfera in due metà uguali.')+term('Quali sono','L\'equatore e ogni meridiano insieme al suo antimeridiano.')+term('I fondamentali','Equatore e meridiano di Greenwich: con i poli geografici permettono di leggere latitudine e longitudine.')+term('Circoli minori','I paralleli: il loro piano non passa per il centro.')
sec('circoli', head('Cartografia · il reticolo','I circoli massimi'), pinned=pcol(txt,540,20)+svgp(X,Y,W,Hh,b,'Globo con l\'equatore e il cerchio formato da Greenwich e dal suo antimeridiano, entrambi passanti per il centro della Terra, e un parallelo più piccolo tratteggiato')+lbl,
 notes='Quiz 1.7.1-13 (circoli massimi: equatore e meridiani con i rispettivi antimeridiani), -8 (cerchi fondamentali: equatore e Greenwich), -24 (poli, equatore e Greenwich), -29 (l\'equatore divide gli emisferi boreale e australe). Il circolo massimo tornerà con l\'ortodromia, la rotta più breve.')
X=700

# ---- Latitudine ----
cx,cy,R=560,320,270
b=globe(cx,cy,R,(20,40,60,80),(40,70))+line(cx-R,cy,cx+R,cy,CORAL,6)
phi=40; Px,Py=cx+R*math.cos(math.radians(phi)),cy-R*math.sin(math.radians(phi))
b+=f'<path d="M{cx} {cy} L{cx+R} {cy} A{R} {R} 0 0 0 {Px:.1f} {Py:.1f} Z" fill="{CORAL}" fill-opacity="0.25" stroke="{CORAL}" stroke-width="3"/>'
b+=line(cx-R*math.cos(math.radians(phi)),Py,Px,Py,SUN,6)+f'<path d="M{cx+R} {cy} A{R} {R} 0 0 0 {Px:.1f} {Py:.1f}" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<circle cx="{Px:.1f}" cy="{Py:.1f}" r="14" fill="{SUN}" stroke="{NAVY}" stroke-width="4"/>'
b+=line(120,cy-R,120,cy+R,NAVY,6)
for la in range(-90,91,10):
    yy=cy-R*math.sin(math.radians(la)); b+=line(120,yy,140 if la%30 else 156,yy,NAVY,3)
lbl=lab(X+cx+R*0.62,Y+cy-80,90,'φ',CORAL,44,900)+lab(X+Px+20,Y+Py-50,70,'P',NAVY,30,900)+lab(X+cx+R+10,Y+cy-16,160,'Equatore 0°',CORAL,22,900)
lbl+=''.join(lab(X+164,Y+cy-R*math.sin(math.radians(la))-16,110,t,NAVY,22,900) for la,t in ((90,'90° N'),(30,'30° N'),(0,'0°'),(-30,'30° S'),(-90,'90° S')))
txt=term('Latitudine φ','L\'arco di meridiano compreso tra l\'equatore e il parallelo del punto.')+term('Da 0° a 90°','Verso Nord o verso Sud. L\'equatore è il riferimento: 0°.')+term('Nord o Sud?','Se i valori crescono dal basso verso l\'alto siamo nell\'emisfero Nord.')+term('Un dato impossibile','95° di latitudine non esiste: il massimo è 90°, il polo.')
sec('latitudine', head('Cartografia · le coordinate','La latitudine')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Globo con l\'angolo di latitudine φ al centro della Terra, dall\'equatore al punto P lungo il meridiano, e a sinistra la scala da 90 gradi Sud a 90 gradi Nord')+lbl,
 notes='Quiz 1.7.1-2 (il grado di latitudine: distanza angolare tra equatore e parallelo), -3 (arco di meridiano dall\'equatore al parallelo del punto), -4 (da 0° a 90° Nord o Sud), -28 (l\'equatore è il riferimento), -42 (Nord se i valori crescono verso Nord), -31 (95° di latitudine è impossibile), -45 (0°: sull\'equatore).')

# ---- Longitudine ----
X=128
cx,cy,R=420,320,270
b=polar(cx,cy,R,15)
lam=50; Px,Py=pol(cx,cy,180-lam,R); Gx,Gy=pol(cx,cy,180,R)
b+=f'<path d="M{cx} {cy} L{Gx:.1f} {Gy:.1f} A{R} {R} 0 0 0 {Px:.1f} {Py:.1f} Z" fill="{BLUE}" fill-opacity="0.22" stroke="{BLUE}" stroke-width="3"/>'
b+=line(cx,cy,Gx,Gy,CORAL,7)+dash(cx,cy,cx,cy-R,CORAL,4)+line(cx,cy,Px,Py,BLUE,5)
b+=f'<path d="M{Gx:.1f} {Gy:.1f} A{R} {R} 0 0 0 {Px:.1f} {Py:.1f}" fill="none" stroke="{BLUE}" stroke-width="12" stroke-linecap="round"/><circle cx="{Px:.1f}" cy="{Py:.1f}" r="14" fill="{SUN}" stroke="{NAVY}" stroke-width="4"/>'
lbl=lab(X+cx-110,Y+cy+R+4,220,'Greenwich 000°',CORAL,22,900,'center')+lab(X+cx-110,Y+cy-R-34,220,'180°',CORAL,22,900,'center')
lbl+=lab(X+cx+R+14,Y+cy-16,140,'090° E',GREEN,22,900)+lab(X+cx-R-150,Y+cy-16,140,'090° W',GREEN,22,900,'right')+lab(X+cx+60,Y+cy+60,80,'λ',BLUE,44,900)+lab(X+Px+18,Y+Py,70,'P',NAVY,30,900)
lbl+=lab(X+800,Y+30,260,'visto dal polo Nord: il cerchio esterno è l\'equatore',SOFT,22,800)
txt=term('Longitudine λ','L\'arco di equatore compreso tra il meridiano di Greenwich e il meridiano del punto.')+term('Da 000° a 180°','Verso Est o verso Ovest (W).')+term('Stesso meridiano','Tutti i punti di un meridiano hanno la stessa longitudine.')+term('Longitudine 0°','Il punto sta sul meridiano di Greenwich.')
sec('longitudine', head('Cartografia · le coordinate','La longitudine'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Il globo visto dal polo Nord: l\'angolo di longitudine λ tra il meridiano di Greenwich e il meridiano del punto P, misurato lungo l\'equatore verso Est')+lbl,
 notes='Quiz 1.7.1-1 (grado di longitudine: distanza angolare tra due meridiani, 60 primi), -5 e -17 (da 0 a 180 gradi Est o Ovest), -12 e -36 (arco di equatore da Greenwich), -33 (stessa longitudine lungo un meridiano), -44 (0°: su Greenwich). Visto dal polo Nord, l\'Est è in senso antiorario partendo da Greenwich in basso.')
X=700

# ---- Grado, primo, miglio e nodo ----
bigp=lambda t,c,s=64: f'<p style="font-family:{H}; font-size:{s}px; font-weight:700; line-height:1.05; color:{c}">{t}</p>'
c1=card(tag('Sessagesimale',CORAL)+bigp('1° = 60′',CORAL)+bigp('1′ = 60″',CORAL,48)+p('Come le ore: 1 ora = 60 minuti, 1 minuto = 60 secondi. Il primo si divide anche in decimi: 42°46′,3.',24),CORAL_T,30,12)
c2=card(tag('Il miglio',SEA)+p('Terra sferica: un circolo massimo (equatore o due meridiani) è lungo 40.000 km.',24,INK)+p('40.000 km ÷ 360° = <b>111,1 km</b> per 1°<br>111,1 km ÷ 60′ = <b>1,852 km</b> per 1′',24)+bigp('1′ = 1 miglio = 1852 m',SEA,46),SEA_T,30,12)
c3=card(tag('Il nodo',PURPLE)+bigp('1 nodo',PURPLE)+p('= 1 miglio all\'ora. È una <b>velocità</b>, non una distanza: 6 nodi sono 6 miglia in un\'ora.',24),LILAC_T,30,12)
gl1=card(p("<b>Grado di latitudine</b>: distanza angolare tra due paralleli, 60′ = <b>60 miglia</b>.",26,INK),None,26)
gl2=card(p("<b>Grado di longitudine</b>: distanza angolare tra due meridiani, 60′ d'arco. In miglia vale 60 solo all'equatore.",26,INK),None,26)
bottom=f'<div style="display:flex; gap:24px">{gl1}{gl2}</div>'
sec('grado', head('Cartografia · le misure','Grado, primo, miglio e nodo')+f'<div style="display:flex; gap:24px; align-items:stretch">{c1}{c2}{c3}</div>'+bottom+note('Le distanze si misurano solo sulla scala delle latitudini.',CORAL,36), gap=26,
 notes='Quiz 1.7.1-9, -20, 1.7.5-20, -21, -50 (miglio = 1′ di latitudine = 1852 m), 1.7.1-11 (grado, primi, secondi), -2 (grado di latitudine), -1 (grado di longitudine: 60 primi d\'arco), 1.7.5-32 e -37 (1° = 60 miglia), 1.7.5-13, -14, -25, -51 (nodo = un miglio all\'ora). Attenzione: il primo di latitudine è il miglio; il nodo è una velocità.')

# ---- Classificazione delle carte ----
coast=[]
for i in range(60):
    t=2*math.pi*i/60; r=60+10*math.sin(3*t)+6*math.sin(7*t+1)+3*math.sin(13*t+2)
    coast.append((-58+r*math.cos(t), -40+r*math.sin(t)))
cpath='M'+' L'.join(f'{a:.2f} {b_:.2f}' for a,b_ in coast)+' Z'
isl='M20 -30 l6 -2 l4 5 l-5 4 Z M34 18 l3 -2 l3 3 l-4 3 Z'
FX,FY=coast[7]
moles=f'M{FX-1.4:.2f} {FY+0.9:.2f} l1.6 0.9 l0.15 -0.12 l-1.5 -0.9 Z M{FX+0.8:.2f} {FY-1.2:.2f} l0.25 1.9 l-0.15 0.02 l-0.2 -1.8 Z'
def zoom(z):
    return (f'<g transform="translate(150 95) scale({z}) translate({-FX:.2f} {-FY:.2f})"><path d="{cpath}" fill="{LAND}" stroke="{LAND_S}" stroke-width="2" vector-effect="non-scaling-stroke"/>'
            f'<path d="{isl}" fill="{LAND}" stroke="{LAND_S}" stroke-width="2" vector-effect="non-scaling-stroke"/><path d="{moles}" fill="#9AA5B1" stroke="{NAVY}" stroke-width="1.5" vector-effect="non-scaling-stroke"/></g>')
SC=[(1,'Generali','1:3.000.000 e meno','Pianificare rotte su grandi distanze. Non per la costiera.',CORAL),
    (2.6,'Di atterraggio','tra generali e costiere','Per avvicinarsi alla costa dal largo.',SUN),
    (7,'Costiere','1:100.000 · 1:50.000','La navigazione costiera. La 5/D è 1:100.000; 1:50.000 è costiera a grande scala.',SEA),
    (18,'Dei litorali','più grandi delle costiere','Porti, stretti e passaggi in dettaglio.',BLUE),
    (60,'Piani nautici','1:5.000 circa','Porti, rade, isolotti: banchine, ormeggi, fondali.',PURPLE)]
cc=''.join(card(svgi(300,190,zoom(z),f'Carta {t.lower()}: la stessa costa a ingrandimento crescente',dw=270,dh=171)+tag(s,c)+h3(t,30)+p(d,22),None,22,8) for z,t,s,d,c in SC)
sec('classificazione', head('Cartografia · le carte','Classificazione delle carte nautiche')+f'<div style="display:flex; gap:18px">{cc}</div>'
 +note('Piccola scala = denominatore grande (1:3.000.000). Grande scala = denominatore piccolo (1:20.000).',CORAL,36),
 notes='Quiz 1.7.2-5 e -17 (classificazione per scala: generali, di atterraggio, costiere, dei litorali, piani nautici), -6 e -21 (generali 1:3.000.000 e inferiore), -18 (generali per grandi distanze), -10 (la piccola scala non serve per la costiera), -7, -22, -35 (costiere, 1:100.000; 1:50.000 costiera a grande scala), -49 (litorali), -12, -13, -23 (piani nautici, 1:5.000), -25 (scala maggiore = denominatore minore). Il disegno mostra la stessa costa ingrandita: nel piano nautico compaiono i moli.')

# ---- Pubblicazioni ----
def book(c,icon):
    s=f'<rect x="70" y="18" width="170" height="200" rx="14" fill="{c}" stroke="{NAVY}" stroke-width="4"/><rect x="70" y="18" width="26" height="200" rx="8" fill="{NAVY}" fill-opacity="0.35"/>'
    s+=f'<rect x="110" y="40" width="112" height="16" rx="8" fill="#FFFFFF" fill-opacity="0.8"/><rect x="110" y="64" width="80" height="10" rx="5" fill="#FFFFFF" fill-opacity="0.6"/>'
    return s+f'<g transform="translate(166 150)">{icon}</g>'
ic_list=''.join(f'<rect x="-40" y="{-40+i*22}" width="80" height="10" rx="5" fill="#FFFFFF"/>' for i in range(4))
ic_warn=f'<path d="M0 -44 L46 36 L-46 36 Z" fill="#FFFFFF"/><rect x="-5" y="-18" width="10" height="32" rx="5" fill="{CORAL}"/><circle cx="0" cy="24" r="6" fill="{CORAL}"/>'
ic_coast=f'<path d="M-50 30 Q-30 -30 0 -10 Q20 -40 50 -20 L50 40 L-50 40 Z" fill="#FFFFFF"/>'+f'<path d="M-50 40 L50 40" stroke="{NAVY}" stroke-width="4"/>'
ic_light=f'<path d="M-12 40 L-7 -20 L7 -20 L12 40 Z" fill="#FFFFFF"/><rect x="-10" y="-34" width="20" height="14" rx="3" fill="{SUN}"/><path d="M12 -30 L44 -46 L44 -14 Z" fill="{SUN}" fill-opacity="0.9"/>'
PB=[(book(BLUE,ic_list),'Catalogo IIM','L\'elenco di tutte le carte e pubblicazioni dell\'Istituto Idrografico della Marina.'),
    (book(SEA,ic_coast),'Portolano','Le notizie per la navigazione costiera: costa, pericoli, aspetto dei fari, servizi portuali, boe.'),
    (book(PURPLE,ic_light),'Elenco dei Fari e Segnali da nebbia','Posizione, descrizione e caratteristiche dei segnali luminosi e sonori.'),
    (book(CORAL,ic_warn),'Avvisi ai Naviganti','Gli AA.NN. aggiornano carte e pubblicazioni; le correzioni si annotano a margine della carta.')]
cc=''.join(card(svgi(320,236,s,f'Copertina illustrata: {t}',dw=300,dh=221)+h3(t,28)+p(d,22),None,22,10) for s,t,d in PB)
sec('pubblicazioni', head('I documenti nautici','Pubblicazioni e documenti nautici')+f'<div style="display:flex; gap:20px">{cc}</div>'
 +p('<b>Ristampa</b>: nuova tiratura con le correzioni degli AA.NN. <b>Nuova edizione</b>: modifiche essenziali per la sicurezza, non riportabili con gli AA.NN. Le <b>carte didattiche</b> non sono aggiornate e non sono documenti ufficiali: non si carteggia in navigazione.',25,INK),
 notes='Quiz 1.7.8-1 (catalogo), -2 e -4 (aggiornamenti, Avvisi ai Naviganti), 1.7.2-3 (correzioni a margine della carta), -7 e -5 (Portolano), -6 (Elenco dei Fari), -8 (documenti nautici = carte e pubblicazioni), -3 e 1.7.2-36 (ristampa e nuova edizione), 1.7.2-26 (carte didattiche), 1.7.2-1 (l\'I.I.M.M. copre i mari italiani e il Mediterraneo).')

# ---- 1111 INT 1 ----
def light(x,y,s=1): return f'<path d="M{x} {y} Q{x+10*s} {y-30*s} {x+28*s} {y-44*s} Q{x+18*s} {y-18*s} {x} {y} Z" fill="{MAG}" fill-opacity="0.85"/><circle cx="{x}" cy="{y}" r="{5*s}" fill="{NAVY}"/>'
cp=[(0,150),(90,120),(180,160),(260,110),(350,90),(420,140),(500,120),(560,70),(640,90),(700,40),(760,60)]
cl='M'+' L'.join(f'{a} {b_}' for a,b_ in cp)
b=f'<rect x="0" y="0" width="760" height="620" fill="#FFFFFF"/>'
b+=f'<path d="{cl} L760 {cp[-1][1]+90} ' + ' '.join(f'L{a} {b_+90}' for a,b_ in reversed(cp)) + f' Z" fill="{SHALLOW}"/>'
b+=f'<path d="{cl} L760 0 L0 0 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=''.join(f'<path d="M'+' L'.join(f'{a} {b_+off}' for a,b_ in cp)+f'" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="10 7"/>' for off in (90,200,330))
b+=light(640,90,1.3)+f'<circle cx="300" cy="420" r="16" fill="none" stroke="{NAVY}" stroke-width="3"/><path d="M288 420 h24 M300 408 v24" stroke="{NAVY}" stroke-width="3"/>'
SX=128
lbl=''.join(lab(SX+x,Y+y,60,t,NAVY,24,700) for x,y,t in [(80,220,'3'),(440,250,'7'),(250,330,'12'),(640,380,'18'),(90,560,'25'),(520,500,'30'),(620,560,'34')])
lbl+=''.join(f'<p style="position:absolute; left:{SX+x}px; top:{Y+y}px; font-size:26px; font-style:italic; font-weight:700; color:{NAVY}">{t}</p>' for x,y,t in [(200,300,'r'),(560,250,'s'),(400,470,'f')])
lbl+=lab(SX+660,Y+60,90,'F',MAG,26,900)+lab(SX+330,Y+404,80,'PA',NAVY,24,900)
def leg(ic,t,d): return f'<div style="display:flex; gap:14px; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 16px; border-radius:22px">{ic}<div style="display:flex; flex-direction:column; gap:2px">{p(t,24,INK,800,1.2)}{p(d,22,BODY,400,1.3)}</div></div>'
ico=lambda body: f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" style="width:64px; height:64px; flex:none">{body}</svg>'
txtic=lambda t,c=NAVY,it=False: f'<p style="width:64px; flex:none; font-size:30px; font-weight:800; text-align:center; color:{c};{" font-style:italic;" if it else ""}">{t}</p>'
L6=[(ico(f'<path d="M4 40 Q20 24 32 34 T60 28" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 6"/>'),'Batimetriche o isobate','Linee che uniscono punti di uguale profondità.'),
    (txtic('12'),'Profondità','Gli scandagli, in metri.'),
    (txtic('f',NAVY,True),'Fondo fangoso','E «s» sabbia, «g» ghiaia…'),
    (txtic('r',NAVY,True),'Fondo roccioso','Attenzione all\'ancora!'),
    (ico(light(24,48,1.1)),'Segnali convenzionali','Fari e fanali; «F» = luce fissa.'),
    (txtic('PA'),'Posizione approssimativa','Vicino a un simbolo di posizione incerta.')]
grid=f'<div style="position:absolute; left:928px; top:290px; width:864px; display:grid; grid-template-columns:1fr 1fr; gap:14px">{"".join(leg(*x) for x in L6)}</div>'
sec('int1', head('Cartografia · la legenda','La 1111 INT 1')+grid+p('La 1111 INT 1 dell\'Istituto Idrografico è la legenda internazionale di simboli, abbreviazioni e termini delle carte nautiche.',24,INK).replace('<p style="','<p style="position:absolute; left:928px; top:830px; width:864px; ',1),
 pinned=svgp(SX,Y,760,620,b,'Carta nautica di fantasia con costa, isobate tratteggiate, scandagli, natura del fondo r, s, f, un faro con la lettera F e uno scoglio in posizione approssimativa PA'),
 notes='Quiz 1.7.2-8 e -48 (isobate: uguale profondità), -24 (profondità, elevazioni, segnali convenzionali), -15 e -29 (natura del fondo sulla carta), -38 (r = roccioso), -39 (f = fangoso), -32 (F = luce fissa), -44 (P.A. = posizione approssimativa). I numeri e le lettere sulla carta sono in corsivo. Far sfogliare la 1111 INT 1 in aula.')

# ---- Simboli delle carte ----
def sy(body): return body
def s_fonda(): return f'<g transform="translate(100 60)" fill="none" stroke="{MAG}" stroke-width="4" stroke-linecap="round"><circle cx="0" cy="-38" r="7"/><path d="M0 -31 V36 M-26 26 Q-18 42 0 36 Q18 42 26 26"/><circle cx="0" cy="4" r="18"/></g><text x="94" y="72" font-family="Arial" font-size="20" font-weight="700" fill="{MAG}">A</text>'
def s_minori(): return f'<g transform="translate(100 60)" fill="none" stroke="{MAG}" stroke-width="5" stroke-linecap="round"><circle cx="-8" cy="-30" r="10"/><path d="M-8 -20 V34 M-8 34 Q10 36 22 16 M-8 0 H6"/><path d="M22 16 l-10 2 M22 16 l2 -10"/></g>'
def s_relitto(): return f'<path d="M40 90 L160 90 L150 76 Q110 70 70 40 L90 20 L60 50 Q50 70 40 90 Z" fill="{NAVY}"/><circle cx="100" cy="92" r="6" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
def s_sommersi(): return f'<path d="M30 70 Q40 20 110 30 Q170 30 160 70 Q140 100 70 96 Q30 94 30 70 Z" fill="{SHALLOW}" stroke="{NAVY}" stroke-width="3" stroke-dasharray="4 6"/>'+''.join(f'<path d="M{x-9} {y} h18 M{x} {y-9} v18" stroke="{NAVY}" stroke-width="4"/>' for x,y in ((70,70),(100,50),(130,72)))
def s_affiorante(): return f'<rect x="40" y="10" width="120" height="100" fill="{SHALLOW}"/><path d="M100 26 V94 M66 60 H134" stroke="{NAVY}" stroke-width="8"/>'+''.join(f'<rect x="{x-9}" y="{y-9}" width="18" height="18" fill="{NAVY}"/>' for x,y in ((76,36),(124,36),(76,84),(124,84)))
def s_tss(): return f'<path d="M20 30 L180 10 M20 110 L180 90" stroke="{MAG}" stroke-width="3" stroke-dasharray="12 8"/><path d="M20 70 L180 50" stroke="{MAG}" stroke-opacity="0.45" stroke-width="16"/>'+arrow(150,34,60,46,MAG,3,14)+arrow(60,92,150,80,MAG,3,14)
def tdash(x0,y0,x1,y1):
    s=f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="{MAG}" stroke-width="4" stroke-dasharray="14 8"/>'
    s+=''.join(f'<path d="M{x} {y0} v10" stroke="{MAG}" stroke-width="4"/>' for x in range(x0+8,x1,22))
    return s
def s_interdetta(): return f'<rect x="30" y="20" width="140" height="80" fill="{SHALLOW}"/>'+tdash(30,20,170,100)
def s_divieto(): return tdash(30,14,170,106)+f'<g transform="translate(100 62) scale(0.7)" fill="none" stroke="{MAG}" stroke-width="5" stroke-linecap="round"><circle cx="0" cy="-26" r="7"/><path d="M0 -19 V26 M-13 -9 H13 M-24 10 Q-20 28 0 26 Q20 28 24 10"/></g><path d="M74 36 L126 88" stroke="{MAG}" stroke-width="5"/>'
def s_cavo(): return f'<rect x="20" y="30" width="160" height="60" fill="{SHALLOW}"/><path d="M34 60 q10 -14 20 0 t20 0 M86 60 q10 -14 20 0 t20 0 M138 60 q10 -14 20 0" fill="none" stroke="{MAG}" stroke-width="4" stroke-dasharray="6 5"/>'
def s_condotta(): return line(20,60,180,60,MAG,4)+''.join(f'<circle cx="{x}" cy="60" r="8" fill="{MAG}"/>' for x in range(30,181,30))
SY=[(s_fonda(),'Punto di fonda'),(s_minori(),'Ancoraggio navi minori'),(s_relitto(),'Relitto emergente'),(s_sommersi(),'Scogli sommersi pericolosi'),(s_affiorante(),'Scoglio affiorante'),
    (s_tss(),'Schema di separazione del traffico'),(s_interdetta(),'Zona interdetta o regolamentata'),(s_divieto(),'Divieto di ancoraggio'),(s_cavo(),'Cavo sottomarino abbandonato'),(s_condotta(),'Condotta sottomarina')]
gs=''.join(card(svgi(200,120,s,f'Simbolo della carta nautica: {t}',dw=250,dh=150,pan=False)+p(t,23,INK,800,1.25),None,18,8) for s,t in SY)
sec('simboli', head('Cartografia · simboli','I simboli delle carte nautiche')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr 1fr; gap:18px">{gs}</div>'+note('In magenta le informazioni «aggiunte» dall\'uomo: fonde, divieti, cavi, condotte.',MAG,34),
 notes='Quiz 1.7.2-45, -51, -54 (punto di fonda, ancoraggio per navi minori, divieto di ancoraggio), -52 (relitto in parte emergente), -42 (scogli sommersi pericolosi), -41 (scoglio affiorante), -50 (schema di separazione del traffico), -40 (zona regolamentata), -43 (cavo abbandonato), -53 (condotta). Molti di questi quiz hanno la figura: a lezione far riconoscere il simbolo prima di leggere il nome.')

# ---- Elenco dei fari ----
X=128
rows=[('Fissa','F','F',[(0,12,LWHITE)]),('A lampi','Lam','Fl',[(t,t+0.4,LWHITE) for t in (0,3,6,9)]),('Scintillante','Sc','Q',[(t,t+0.5,LWHITE) for t in range(12)]),
      ('Intermittente','Int','Oc',[(t,t+2.2,LWHITE) for t in (0,3,6,9)]),('Alternata','Alt b.r.','Al W.R.',[(t,t+1.5,LWHITE if i%2==0 else LRED) for i,t in enumerate((0,1.5,3,4.5,6,7.5,9,10.5))]),
      ('Isofase','Iso','Iso',[(t,t+1.5,LWHITE) for t in (0,3,6,9)])]
x0,x1=440,1060; sx=(x1-x0)/12
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EAF4F7"/>'
for i,(nm,it,en,seg) in enumerate(rows):
    y=60+i*76; b+=f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="44" rx="8" fill="{NIGHT}"/>'
    b+=''.join(f'<rect x="{x0+a*sx:.0f}" y="{y+6}" width="{max(6,(e-a)*sx):.0f}" height="32" rx="6" fill="{c}"/>' for a,e,c in seg)
lbl=lab(X+30,Y+20,200,'tipo',SOFT,20,900)+lab(X+230,Y+20,90,'ITA',SOFT,20,900)+lab(X+330,Y+20,100,'ING',SOFT,20,900)
lbl+=''.join(lab(X+30,Y+66+i*76,200,nm,NAVY,24,900)+lab(X+230,Y+66+i*76,100,it,CORAL,24,900)+lab(X+330,Y+66+i*76,110,en,SEA,24,900) for i,(nm,it,en,_) in enumerate(rows))
cols=''.join(f'<p style="font-size:22px; font-weight:900; color:{tc}; background:{bg}; padding:6px 14px; border-radius:14px">{t}</p>' for t,bg,tc in (('rosso · r · R',LRED,'#FFFFFF'),('verde · v · G',LGREEN,'#FFFFFF'),('bianco · b · W','#FFFFFF',NAVY)))
lbl+=f'<div style="position:absolute; left:{X+30}px; top:{Y+540}px; display:flex; gap:12px; align-items:center">{cols}<p style="font-size:22px; font-weight:800; color:{INK}">se il colore non è indicato: bianco</p></div>'
txt=term('Cosa contiene','Ubicazione, descrizione e caratteristica dei segnali luminosi e dei segnali sonori da nebbia (nautofoni) delle coste del Mediterraneo.')+term('Caratteristica','Tipo di luce, periodo e colore: di notte un faro si riconosce così.')+term('Fase','Ogni singolo elemento del ciclo: un lampo, un\'eclisse.')+term('Periodo','Il tempo in cui si ripete la sequenza di lampi ed eclissi.')
sec('elencofari', head('Segnalamento · le luci','Elenco dei fari e segnali da nebbia'), pinned=pcol(txt,540,18)+svgp(X,Y,W,Hh,b,'Tabella dei tipi di luce con le sigle italiane e inglesi e le strisce notturne di luce fissa, a lampi, scintillante, intermittente, alternata bianca e rossa, isofase; sotto i colori rosso, verde e bianco')+lbl,
 notes='Quiz 1.7.8-6 (Elenco dei Fari), 1.5.3-56 e -77 (caratteristica), -47 (periodo), -7 e -92 (Sc = scintillante), -9 e -94 (Int = intermittente, a gruppi di eclissi), -38 (Iso: luce uguale all\'intervallo), -8 e -75 (luce alternata), -45 (Fl G 5s: 1 lampo verde ogni 5 secondi). La fase (1.5.3-4) è oscurata. Il quiz 1.5.3-37 traduce Oc con «intermittente».')

# ---- Caratteristiche dei fari ----
T=14; seq=[(0,1,1),(1,3,0),(3,4,1),(4,6,0),(6,7,1),(7,14,0)]
tw=1500; ts=tw/T
bar=f'<rect x="0" y="40" width="{tw}" height="60" rx="10" fill="{NIGHT}"/>'+''.join(f'<rect x="{a*ts:.0f}" y="48" width="{(e-a)*ts:.0f}" height="44" rx="6" fill="{LWHITE}"/>' for a,e,on in seq if on)
bar+=''.join(f'<text x="{(a+e)/2*ts:.0f}" y="130" text-anchor="middle" font-family="Arial" font-size="26" font-weight="{900 if on else 600}" fill="{CORAL if on else NAVY}">{e-a}</text>' for a,e,on in seq)
bar+=f'<path d="M0 150 H{tw}" stroke="{SEA}" stroke-width="4"/><path d="M0 140 V160 M{tw} 140 V160" stroke="{SEA}" stroke-width="4"/><text x="{tw/2}" y="30" text-anchor="middle" font-family="Arial" font-size="24" font-weight="900" fill="{NAVY}">Lam (3) 14s 63m 16M · 1-2-1-2-1-7 · periodo 14 secondi</text>'
EX=[('Fl (3) W 10s','3 lampi bianchi ogni 10 secondi.',LWHITE),('Lam (2) 12s 27m 17M','2 lampi bianchi in 12 s; luce a 27 m sul mare; portata nominale 17 miglia.',LWHITE),
    ('Oc (3) W 5s','Intermittente: 3 eclissi in 5 secondi, luce bianca.',LWHITE),('Int (2) 10s 26m 20M','2 intermittenze in 10 s; 26 m sul mare; 20 miglia.',LWHITE),
    ('Fl G 5s','1 lampo verde ogni 5 secondi.',LGREEN),('F r 18M','Luce fissa rossa, portata 18 miglia.',LRED)]
ex=''.join(f'<div style="display:flex; gap:14px; align-items:center; background:{NIGHT}; padding:16px 18px; border-radius:22px"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" style="width:48px; height:48px; flex:none">{glow(24,24,c,8)}</svg><div style="display:flex; flex-direction:column; gap:2px"><p style="font-family:{H}; font-size:28px; font-weight:700; color:#FFFFFF">{t}</p><p style="font-size:21px; line-height:1.3; color:{DSOFT}">{d}</p></div></div>' for t,d,c in EX)
sec('caratteristiche', head('Segnalamento · leggere una luce','Le caratteristiche dei fari')+f'<div style="display:flex; gap:24px; align-items:center">{svgi(1500,170,bar,"Striscia del faro di Forte Stella a Portoferraio: 3 lampi di 1 secondo separati da 2 secondi di buio e 7 secondi di buio finale, periodo 14 secondi",dw=1180,dh=134,pan=False)}{card(p("Forte Stella, Portoferraio. Sulla carta anche «F r 7M»: il <b>settore rosso</b> segnala condizioni di pericolo.",22,INK),CORAL_T,20,6)}</div>'
 +f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px">{ex}</div>', gap=26,
 notes='Esempio dall\'Elenco dei Fari: il faro di Forte Stella a Portoferraio, Lam (3) 14s 63m 16M: tre lampi di 1 secondo, eclissi di 2, 2 e 7 secondi, luce a 63 m, portata nominale 16 miglia. Quiz 1.5.3-41, -48, -35, -34, -37, -45, -68 (lettura delle sigle), -85 (settore rosso: pericolo), -60 (settori colorati). Leggere le sigle ad alta voce: tipo, gruppo, colore, periodo, altezza, portata.')

# ---- Portate dei fari ----
X=700
k=230/546**2
yc=lambda x: 380+k*(x-546)**2
tx=700; ty=yc(tx); m=2*k*(tx-546); L0=(120,ty+m*(120-tx))
ex_=950; ey=ty+m*(ex_-tx)
def tower(x,y,s=1):
    g=f'<path d="M{x-14*s} {y} L{x-8*s} {y-90*s} L{x+8*s} {y-90*s} L{x+14*s} {y} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/><rect x="{x-9*s}" y="{y-66*s}" width="{18*s}" height="{12*s}" fill="{CORAL}"/><rect x="{x-11*s}" y="{y-34*s}" width="{22*s}" height="{12*s}" fill="{CORAL}"/>'
    return g+f'<rect x="{x-11*s}" y="{y-110*s}" width="{22*s}" height="{20*s}" rx="{4*s}" fill="{SUN}" stroke="{NAVY}" stroke-width="{2.5*s}"/>'
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EAF4F7"/>'
b+='<path d="M0 '+f'{yc(0):.0f}'+' '+' '.join(f'L{x} {yc(x):.1f}' for x in range(0,1093,26))+' L1092 620 L0 620 Z" fill="'+WATER+'" fill-opacity="0.4"/>'
b+=f'<path d="M40 {yc(40)+4:.0f} L40 {L0[1]+60} L200 {L0[1]+60} L220 {yc(220)+4:.0f} Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'+tower(120,L0[1]+62,0.8)
b+=dash(L0[0],L0[1],ex_,ey,SUN,4)+glow(L0[0],L0[1],SUN,8)+f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="7" fill="{CORAL}"/>'
b+=profile(ex_-70,yc(ex_)+2,150,sup=True)+line(ex_,yc(ex_)-20,ex_,ey,NAVY,4)+f'<circle cx="{ex_}" cy="{ey:.0f}" r="8" fill="{NAVY}"/>'
lbl=lab(X+tx-120,Y+ty+24,240,'orizzonte',CORAL,24,900,'center')+lab(X+ex_-100,Y+ey-60,200,'occhio',NAVY,24,900,'center')+lab(X+260,Y+60,420,'la luce passa radente alla curvatura',SUN,24,900)+lab(X+60,Y+int(L0[1])-100,200,'faro',NAVY,24,900)
txt=term('Geografica','Dipende dalla curvatura della Terra, dall\'altezza della luce e dall\'elevazione dell\'occhio: più sei in alto, più lontano vedi.')+term('Luminosa','Dipende dall\'intensità della luce, dalla visibilità meteorologica (trasparenza dell\'aria) e dalla sensibilità dell\'occhio.')+term('Nominale','La portata luminosa con visibilità meteorologica di 10 miglia: è quella scritta sulle carte italiane.')+term('Faro e fanale','Si distinguono per la portata nominale: minore quella dei fanali.')
sec('portate', head('Segnalamento · fin dove si vede','Le portate dei fari')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Faro su un promontorio: la luce passa radente alla curvatura del mare e raggiunge l\'occhio di chi sta sulla barca lontana, sopra l\'orizzonte')+lbl,
 notes='Quiz 1.5.3-3, -28, -88 (portata geografica: curvatura, altezza della luce, elevazione dell\'occhio), -1, -30, -39, -86 (portata luminosa: intensità, visibilità meteorologica, occhio), -2, -31, -63, -87 (portata nominale: visibilità di 10 miglia), -79 (sulla carta è indicata la nominale), -29, -57, -61 (fari e fanali si distinguono per la portata nominale).')

# ---- segnali IALA ----
def cone(x,y,up,s=22,c=MBLACK):
    return f'<path d="M{x-s*0.6:.0f} {y+s/2:.0f} L{x+s*0.6:.0f} {y+s/2:.0f} L{x} {y-s/2:.0f} Z" fill="{c}"/>' if up else f'<path d="M{x-s*0.6:.0f} {y-s/2:.0f} L{x+s*0.6:.0f} {y-s/2:.0f} L{x} {y+s/2:.0f} Z" fill="{c}"/>'
def mark(x,y,bands,top,s=1,vstripes=None,op=1):
    h=90*s; w=40*s; g=f'<g opacity="{op}">'
    g+=f'<ellipse cx="{x}" cy="{y}" rx="{w*0.9:.0f}" ry="{8*s:.0f}" fill="{WATER}" fill-opacity="0.35"/>'
    if vstripes:
        n=len(vstripes)
        for i,c in enumerate(vstripes): g+=f'<rect x="{x-w/2+i*w/n:.1f}" y="{y-h:.0f}" width="{w/n+0.5:.1f}" height="{h:.0f}" fill="{c}"/>'
    else:
        bh=h/len(bands)
        for i,c in enumerate(bands): g+=f'<rect x="{x-w/2:.0f}" y="{y-h+i*bh:.0f}" width="{w:.0f}" height="{bh+0.5:.0f}" fill="{c}"/>'
    g+=f'<rect x="{x-w/2:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="none" stroke="{NAVY}" stroke-width="2"/><path d="M{x} {y-h:.0f} V{y-h-30*s:.0f}" stroke="{NAVY}" stroke-width="{3*s}"/>'
    ty=y-h-44*s
    for kind,par in top:
        if kind=='cone': g+=cone(x,ty,par,22*s); ty-=26*s
        elif kind=='ball': g+=f'<circle cx="{x}" cy="{ty:.0f}" r="{11*s:.0f}" fill="{par}"/>'; ty-=26*s
        elif kind=='x': g+=f'<path d="M{x-11*s:.0f} {ty-11*s:.0f} L{x+11*s:.0f} {ty+11*s:.0f} M{x+11*s:.0f} {ty-11*s:.0f} L{x-11*s:.0f} {ty+11*s:.0f}" stroke="{MYEL}" stroke-width="{6*s:.0f}" stroke-linecap="round"/>'
    return g+'</g>'
def spar(x,y,bands,top,s=1,vstripes=None,op=1):
    h=170*s; w=16*s; g=f'<g opacity="{op}">'
    if vstripes:
        for i,c in enumerate(vstripes): g+=f'<rect x="{x-w/2+i*w/len(vstripes):.1f}" y="{y-h:.0f}" width="{w/len(vstripes)+0.5:.1f}" height="{h:.0f}" fill="{c}"/>'
    else:
        bh=h/len(bands)
        for i,c in enumerate(bands): g+=f'<rect x="{x-w/2:.0f}" y="{y-h+i*bh:.0f}" width="{w:.0f}" height="{bh+0.5:.0f}" fill="{c}"/>'
    g+=f'<rect x="{x-w/2:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="none" stroke="{NAVY}" stroke-width="2"/>'
    ty=y-h-22*s
    for kind,par in top:
        if kind=='cone': g+=cone(x,ty,par,22*s); ty-=26*s
        elif kind=='ball': g+=f'<circle cx="{x}" cy="{ty:.0f}" r="{11*s:.0f}" fill="{par}"/>'; ty-=26*s
        elif kind=='x': g+=f'<path d="M{x-11*s:.0f} {ty-11*s:.0f} L{x+11*s:.0f} {ty+11*s:.0f} M{x+11*s:.0f} {ty-11*s:.0f} L{x-11*s:.0f} {ty+11*s:.0f}" stroke="{MYEL}" stroke-width="{6*s:.0f}" stroke-linecap="round"/>'
    return g+'</g>'
def can(x,y,s=1,op=1): return f'<g opacity="{op}" transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="32" ry="8" fill="{WATER}" fill-opacity="0.35"/><rect x="-18" y="-80" width="36" height="78" rx="3" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/><path d="M0 -80 V-100" stroke="{NAVY}" stroke-width="3"/><rect x="-11" y="-122" width="22" height="22" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/></g>'
def cn(x,y,s=1,op=1): return f'<g opacity="{op}" transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="32" ry="8" fill="{WATER}" fill-opacity="0.35"/><path d="M-22 -2 L22 -2 L6 -80 L-6 -80 Z" fill="{LGREEN}" stroke="{NAVY}" stroke-width="2"/><path d="M0 -80 V-100" stroke="{NAVY}" stroke-width="3"/><path d="M-12 -100 L12 -100 L0 -124 Z" fill="{LGREEN}" stroke="{NAVY}" stroke-width="2"/></g>'
CARD_={'N':([MBLACK,MYEL],[('cone',True),('cone',True)]),'E':([MBLACK,MYEL,MBLACK],[('cone',False),('cone',True)]),
      'S':([MYEL,MBLACK],[('cone',False),('cone',False)]),'W':([MYEL,MBLACK,MYEL],[('cone',True),('cone',False)])}
RW=[LRED,'#FFFFFF',LRED,'#FFFFFF']

# ---- Il sistema AISM-IALA ----
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="470" width="1092" height="150" fill="{WATER}" fill-opacity="0.35"/>'+line(0,470,1092,470,SEA,3)
b+=can(80,480,1.3)+cn(170,480,1.3)
b+=mark(330,480,[MBLACK,LRED,MBLACK],[('ball',MBLACK),('ball',MBLACK)],1.3)
b+=mark(520,480,None,[('ball',LRED)],1.3,RW)
b+=mark(710,480,[MYEL],[('x',0)],1.3)
b+=mark(920,480,CARD_['N'][0],CARD_['N'][1],1.3)
for n,x in ((1,125),(2,330),(3,520),(4,710),(5,920)): b+=num(x,540,n,[CORAL,NAVY,SEA,SUN,PURPLE][n-1],22)
lbl=''.join(lab(X+x-100,Y+575,200,t,INK,22,900,'center') for x,t in ((125,'laterali'),(330,'pericolo isolato'),(520,'acque sicure'),(710,'speciale'),(920,'cardinali')))
txt=term('Cinque tipi','Laterali, pericolo isolato, acque sicure, speciali e cardinali: si riconoscono per forma e colore della struttura e del miraglio.')+term('Fanali','Segnalano porti, boe, pericoli, canali e piattaforme; hanno portata nominale minore dei fari.')
txt+=p('<b>Mede</b>: strutture fisse ancorate al fondo che emergono. <b>Boe</b> e <b>boe luminose</b>: galleggianti vincolati al fondo. <b>Gavitelli</b>: piccoli galleggianti per segnalazioni temporanee.',23,INK)
txt+=p('Con la nebbia: <b>campane</b> azionate dalle onde, <b>riflettori radar</b> passivi, <b>racon</b> (risponditore radar).',23,INK)
sec('iala', head('Segnalamento · il sistema','Il sistema AISM-IALA'), pinned=pcol(txt,540,18)+svgp(X,Y,W,Hh,b,'I cinque tipi di segnali AISM-IALA in fila: laterali rosso cilindrico e verde conico, pericolo isolato nero e rosso con due sfere, acque sicure a strisce verticali bianche e rosse con sfera rossa, speciale giallo con la X, cardinale Nord nero e giallo con due coni')+lbl,
 notes='Quiz 1.5.3-49 (i tipi di segnali AISM-IALA), -44 (codifica diurna: forma e colore della boa o del miraglio), -29 (fanali), -61 (faro e fanale differiscono per la portata nominale), -62 (meda), -5, -6, -90, -91 (boe luminose), -58 (gavitelli), -10 e -95 (riflettore radar). Una slide per ciascun tipo nelle pagine seguenti.')

# ---- Laterali ----
X=700
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
b+=f'<path d="M0 0 L420 0 L420 170 L390 170 L390 40 L0 40 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/><path d="M1092 0 L672 0 L672 170 L702 170 L702 40 L1092 40 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<rect x="385" y="150" width="40" height="40" rx="6" fill="{LRED}" stroke="{NAVY}" stroke-width="3"/><rect x="667" y="150" width="40" height="40" rx="6" fill="{LGREEN}" stroke="{NAVY}" stroke-width="3"/>'
b+=glow(405,140,LRED,7)+glow(687,140,LGREEN,7)
def can2(x,y): return f'<rect x="{x-16}" y="{y-44}" width="32" height="40" rx="3" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/><rect x="{x-11}" y="{y-66}" width="22" height="18" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/>'
def cn2(x,y): return f'<path d="M{x-18} {y-4} L{x+18} {y-4} L{x} {y-50} Z" fill="{LGREEN}" stroke="{NAVY}" stroke-width="2"/><path d="M{x-11} {y-54} L{x+11} {y-54} L{x} {y-76} Z" fill="{LGREEN}" stroke="{NAVY}" stroke-width="2"/>'
for yy in (330,480): b+=can2(420,yy)+cn2(672,yy)
b+=topboat(546,500,130,-90,'#FFFFFF',NAVY,4)+dpath('M546 430 L546 220',CORAL,5)+head_at(546,214,-90,CORAL)
lbl=lab(X+110,Y+300,280,'rosso a sinistra: cilindro',LRED,24,900,'right')+lab(X+710,Y+300,280,'verde a dritta: cono',LGREEN,24,900)+lab(X+390,Y+580,320,'entrando in porto',NAVY,24,900,'center')
txt=term('Cosa dicono','Da quale lato della barca va lasciato il segnale, secondo il senso convenzionale: entrando in porto o risalendo un canale.')+term('Regione A','Europa, Asia continentale, Africa, Australia: entrando, rosso a sinistra (cilindro) e verde a dritta (cono). Uscendo, il contrario.')+term('Regione B','America, Corea, Giappone, Filippine: i colori sono invertiti.')+term('Di notte','Luci rosse e verdi con periodi diversi; i fanali dei moli ripetono i colori.')
sec('laterali', head('Segnalamento · AISM-IALA 1','I segnali laterali')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto di una barca che entra in porto: boe rosse cilindriche a sinistra, boe verdi coniche a dritta, fanale rosso sul molo di sinistra e verde su quello di dritta')+lbl,
 notes='Quiz 1.5.3-32 (in Italia Sistema A, rosso a sinistra), -27 (segnale laterale), -43 (a sinistra entrando: rosso, cilindrico), -110 e -111 (figure), -46 (regioni A e B differiscono solo nei laterali), 1.4.1-8 e -13 (imboccatura del porto: rosso a sinistra, verde a dritta).')

# ---- una slide per segnale: giorno e notte ----
def lightbar(x0,y0,w,segs,T=12,c=LWHITE):
    s=f'<rect x="{x0}" y="{y0}" width="{w}" height="40" rx="8" fill="{NIGHT}" stroke="#FFFFFF" stroke-opacity="0.3"/>'
    return s+''.join(f'<rect x="{x0+a*w/T:.0f}" y="{y0+5}" width="{max(5,(e-a)*w/T):.0f}" height="30" rx="5" fill="{c}"/>' for a,e in segs)
def markslide(id_,n,title,dayfn,glowc,segs,barc,txt,alt,notes,barlabel):
    X_=128
    b=f'<rect x="0" y="0" width="546" height="620" fill="{SKY}"/><rect x="0" y="470" width="546" height="150" fill="{WATER}" fill-opacity="0.35"/>'+line(0,470,546,470,SEA,3)
    b+=f'<rect x="546" y="0" width="546" height="620" fill="{NIGHT}"/><rect x="546" y="470" width="546" height="150" fill="#16324F"/>'
    b+=dayfn(1)+f'<g transform="translate(546 0)">{dayfn(0.22)}</g>'
    b+=glow(546+170,480-90*1.6-30*1.6-4,glowc,11)+glow(546+390,480-170*1.5-4,glowc,9)
    b+=lightbar(596,540,446,segs,12,barc)
    lb=lab(X_+30,Y+20,200,'GIORNO',NAVY,24,900)+lab(X_+576,Y+20,200,'NOTTE',DACC,24,900)+lab(X_+596,Y+500,446,barlabel,'#FFFFFF',22,900)
    sec(id_, head(f'Segnalamento · AISM-IALA {n}',title), pinned=pcol(txt,540,20)+svgp(X_,Y,W,Hh,b,alt,pan=False)+lb, notes=notes)
iso_day=lambda op: mark(170,480,[MBLACK,LRED,MBLACK],[('ball',MBLACK),('ball',MBLACK)],1.6,op=op)+spar(390,480,[MBLACK,LRED,MBLACK,LRED,MBLACK],[('ball',MBLACK),('ball',MBLACK)],1.5,op=op)
markslide('isolato',2,'Pericolo isolato',iso_day,LWHITE,[(0,0.5),(1.5,2),(10,10.5),(11.5,12)],LWHITE,
 term('Giorno','Supporto nero con una o più bande orizzontali rosse; miraglio: due sfere nere sovrapposte.')+term('Notte','Luce bianca a gruppi di 2 lampi, Fl (2): la luce dura meno dell\'eclisse. I due lampi ricordano le due sfere.')+term('Cosa dice','Un pericolo piccolo, con acqua navigabile tutto intorno: gli si passa attorno, a distanza.'),
 'Di giorno una boa e un\'asta nere con bande rosse orizzontali e due sfere nere; di notte gli stessi segnali al buio con la luce bianca a gruppi di due lampi',
 'Quiz 1.5.3-15, -40, -50, -74 (pericolo isolato: nero con bande rosse), -64 (luce bianca a lampi, durata della luce inferiore all\'eclisse, gruppi di 2).','Fl (2) · 2 lampi bianchi, poi buio')
sw_day=lambda op: mark(170,480,None,[('ball',LRED)],1.6,RW,op=op)+spar(390,480,None,[('ball',LRED)],1.5,[LRED,'#FFFFFF',LRED],op=op)
markslide('acquesicure',3,'Acque sicure',sw_day,LWHITE,[(0,2),(4,6),(8,10)],LWHITE,
 term('Giorno','Supporto bianco con una o più bande verticali rosse; miraglio: una sfera rossa.')+term('Notte','Luce bianca isofase, intermittente, a lampo lungo, oppure la lettera «A» in Morse.')+term('Cosa dice','Acqua navigabile tutto intorno: spesso segna l\'inizio di un canale o l\'atterraggio a un porto.'),
 'Di giorno una boa e un\'asta a strisce verticali bianche e rosse con la sfera rossa; di notte la luce bianca isofase',
 'Quiz 1.5.3-59, -65, -99 (acque sicure: luce bianca isofase, intermittente o a lampo lungo; sfera rossa).','Iso · luce e buio di uguale durata')
sp_day=lambda op: mark(170,480,[MYEL],[('x',0)],1.6,op=op)+spar(390,480,[MYEL],[('x',0)],1.5,op=op)
markslide('speciale',4,'Segnale speciale',sp_day,LYEL,[(0,0.6),(4,4.6),(8,8.6)],LYEL,
 term('Giorno','Supporto giallo; miraglio: una «X» gialla.')+term('Notte','Luce gialla, di qualsiasi ritmo purché non si confonda con gli altri segnali.')+term('Cosa dice','Zone particolari: cavi e condotte, esercitazioni, campi boe, limiti delle zone di balneazione.'),
 'Di giorno una boa e un\'asta gialle con la X gialla; di notte la luce gialla',
 'Quiz 1.5.3-12, -42, -53, -100, -101, -102 (speciali: gialli, miraglio a X gialla, luce gialla).','Luce gialla · ritmo variabile')

# ---- Cardinali ----
X=128
cx,cy=546,330
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/><circle cx="{cx}" cy="{cy}" r="180" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
b+=f'<path d="M{cx-50} {cy+20} Q{cx-40} {cy-30} {cx} {cy-26} Q{cx+50} {cy-40} {cx+56} {cy+14} Q{cx+10} {cy+36} {cx-50} {cy+20} Z" fill="#7A6A55" stroke="{NAVY}" stroke-width="3"/>'
pos={'N':(546,230),'E':(866,470),'S':(546,610),'W':(226,470)}
for kk,(px,py) in pos.items():
    bands,top=CARD_[kk]; b+=mark(px,py,bands,top,1.05)
lbl=lab(X+590,Y+120,300,'N · luce continua',NAVY,24,900)+lab(X+910,Y+360,170,'E · 3 lampi',NAVY,24,900)+lab(X+590,Y+520,300,'S · 6 + 1 lungo',NAVY,24,900)+lab(X+30,Y+360,150,'W · 9 lampi',NAVY,24,900,'right')+lab(X+466,Y+366,160,'pericolo',INK,24,900,'center')
txt=term('Cosa dicono','Con la bussola: il lato su cui passare. Si passa a Nord della cardinale Nord, perché il pericolo è a Sud.')+term('Colori e miragli','Nero e giallo. I coni puntano verso le bande nere: in alto il Nord, in basso il Sud, base contro base l\'Est, punta contro punta l\'Ovest.')+term('Di notte','Luce bianca scintillante, come un orologio: 3 lampi Est (ore 3), 6 Sud (ore 6), 9 Ovest (ore 9), continua Nord (ore 12).')
sec('cardinali', head('Segnalamento · AISM-IALA 5','I segnali cardinali'), pinned=svgp(X,Y,W,Hh,b,'Uno scoglio al centro e le quattro boe cardinali attorno: Nord nera sopra e gialla sotto con coni in alto; Est nera, gialla, nera con coni base contro base; Sud gialla sopra e nera sotto con coni in basso; Ovest gialla, nera, gialla con coni punta contro punta')+lbl+pcol(txt),
 notes='Quiz 1.5.3-36, -67 (cosa indicano), -51 (legati alla bussola, nero e giallo), -66 e -70 (miraglio Nord: vertici in alto; Sud: vertici in basso), -69 e -72 (Est: basi unite, passare a est), -71 e -73 (Ovest: vertici uniti, passare a ovest), -82, -83, -84 (9 scintillii: pericolo a est, passare a ovest; 3: passare a est; 6: passare a sud), -33, -52, -54, -55, -97, -103…-109 (figure).')
X=700

# ---- Navigazione fluviale ----
def rsign(split):
    s=f'<rect x="0" y="120" width="220" height="40" fill="{WATER}" fill-opacity="0.4"/><path d="M0 140 L70 110 L220 118 L220 160 L0 160 Z" fill="{ROCK}" fill-opacity="0.7"/>'
    s+=line(110,50,110,140,NAVY,6)
    d=[(110,0),(160,50),(110,100),(60,50)]
    s+=f'<path d="M110 0 L160 50 L110 100 L60 50 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
    half={'basso':'M60 50 L160 50 L110 100 Z','alto':'M60 50 L160 50 L110 0 Z','sinistra':'M110 0 L110 100 L60 50 Z','destra':'M110 0 L110 100 L160 50 Z'}[split]
    return s+f'<path d="{half}" fill="{LRED}" stroke="{NAVY}" stroke-width="3"/>'
FS=[(rsign('basso'),'Prosecuzione','Prosegui lungo la sponda del segnale fino al prossimo avviso.'),(rsign('alto'),'Chiamata e rimando','Dirigi verso la sponda del segnale e poi abbandonala subito.'),
    (rsign('sinistra'),'Chiamata (destra)','Sulla sponda destra: dirigi verso la sponda del segnale.'),(rsign('destra'),'Chiamata (sinistra)','Sulla sponda sinistra: dirigi verso la sponda del segnale.')]
fs=''.join(card(svgi(220,160,s,f'Segnale fluviale: {t}',dw=190,dh=138,pan=False)+h3(t,24)+p(d,20,BODY,400,1.3),None,16,6) for s,t,d in FS)
def bridge():
    s=f'<rect x="0" y="150" width="440" height="50" fill="{WATER}" fill-opacity="0.4"/><rect x="0" y="20" width="440" height="30" fill="#9AA5B1"/>'
    s+=''.join(f'<rect x="{x}" y="50" width="22" height="120" fill="#9AA5B1"/>' for x in (40,160,260,380))
    s+=f'<path d="M210 30 L226 14 L242 30 L226 46 Z" fill="{MYEL}" stroke="{NAVY}" stroke-width="2"/>'+topboat(226,160,90,-90,'#FFFFFF',NAVY,3)
    return s
rules=('<ul style="font-size:22px; line-height:1.35; color:#34465E; display:flex; flex-direction:column; gap:6px">'
 '<li>A bordo un <b>faro anabbagliante orientabile</b> a luce bianca.</li><li>Rotte opposte: precedenza a chi ha la <b>corrente a favore</b>.</li>'
 '<li>Curva a gomito: <b>1 suono prolungato</b>, poi ascolta la risposta.</li><li>Controcorrente, una <b>boa bianca</b> si lascia a sinistra.</li><li>Ancoraggio: <b>due ancore a 180°</b>, nella direzione della corrente.</li></ul>')
bcard=card(svgi(440,200,bridge(),"Ponte a più arcate con il rombo giallo sopra l'arcata da usare e una barca che vi passa sotto",dw=330,dh=150,pan=False)+p("<b>Ponti</b>: si passa sotto l'arcata segnata dal <b>rombo giallo</b>.",22,INK),None,18,6)
sec('fluviale', head('Segnalamento · acque interne','Navigazione fluviale')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:16px">{fs}</div>'
 +f'<div style="display:flex; gap:20px; align-items:stretch">{bcard}{card(rules,SEA_T,20,6,1.6)}</div>', gap=20,
 notes='Quiz 1.5.3-112 (chiamata e rimando), -117 e -118 (chiamata: sponda destra o sinistra), -119 (prosecuzione), -113 (rotte opposte: precedenza a chi ha la corrente a favore), -114 (rombo giallo sull\'arcata), -115 (controcorrente, boa bianca: si passa a sinistra), -116 (curva a gomito: 1 suono prolungato e ascolto), -120 (faro anabbagliante orientabile), 1.4.3-5 (ancoraggio con due ancore a 180°), 1.8.1-20 (navigazione interna: laghi, fiumi, canali). I segnali -112, -117, -118, -119 sono in figura.')

# ---- Mercatore 1: la proiezione ----
b=f'<rect x="250" y="60" width="560" height="520" fill="{SEA}" fill-opacity="0.10"/>'+line(250,60,250,580,SEA,4)+line(810,60,810,580,SEA,4)
b+=f'<ellipse cx="530" cy="60" rx="280" ry="36" fill="none" stroke="{SEA}" stroke-width="4"/><ellipse cx="530" cy="580" rx="280" ry="36" fill="none" stroke="{SEA}" stroke-dasharray="10 8" stroke-width="4"/>'
b+=globe(530,320,280,(30,60),(35,70))+line(250,320,810,320,CORAL,6)
for la in (25,45):
    y1=320-280*math.tan(math.radians(la)); gy=320-280*math.sin(math.radians(la)); gx=530+280*math.cos(math.radians(la))
    b+=dash(530,320,810,y1,SUN,3)+f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="7" fill="{SUN}"/><circle cx="810" cy="{y1:.0f}" r="9" fill="{CORAL}"/>'
b+=glow(530,320,SUN,12)
lbl=lab(X+830,Y+300,240,'cilindro tangente all\'equatore',SEA,22,900)+lab(X+400,Y+340,260,'punto di proiezione al centro',SUN,22,900)
txt=term('Gerardo Mercatore','Gerhard Kremer, cartografo fiammingo (1512-1594), inventò la carta che usiamo in mare.')+term('L\'idea','Il reticolo terrestre si proietta su un cilindro di carta tangente all\'equatore, poi il cilindro si srotola.')+term('Il punto di proiezione','È al centro della Terra.')+note('È la carta del carteggio d\'esame: la 5/D e la 42/D.',CORAL,34)
sec('mercatore1', head('Cartografia · la proiezione','La carta di Mercatore')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Il globo dentro un cilindro tangente all\'equatore: dal centro della Terra i raggi proiettano i paralleli sul cilindro, sempre più distanti verso i poli')+lbl,
 notes='Quiz 1.7.2-28 (il punto di proiezione è al centro della Terra: è la risposta ministeriale; in realtà la costruzione di Mercatore è matematica, con le latitudini crescenti, ma all\'esame si risponde così). Il disegno mostra il principio: i paralleli si allontanano verso i poli.')

# ---- Mercatore 2: il reticolo ----
X=128
g,yf=mercator(60,40,1030,600,70,10,60)
b=g+f'<path d="M548 {yf(0):.0f} h-26 v-26" fill="none" stroke="{CORAL}" stroke-width="4"/>'+f'<rect x="60" y="0" width="970" height="40" fill="{CORAL}" fill-opacity="0.12"/><rect x="60" y="600" width="970" height="20" fill="{CORAL}" fill-opacity="0.12"/>'
lbl=''.join(lab(X+1036,Y+yf(la)-14,60,f'{abs(la)}°',NAVY,20,900) for la in (-60,-30,0,30,60))+lab(X+300,Y+6,500,'oltre 70° la carta non si usa',CORAL,22,900,'center')+lab(X+570,Y+yf(0)-50,120,'90°',CORAL,22,900)
txt=term('Meridiani','Rette parallele, perpendicolari all\'equatore ed equidistanti tra loro.')+term('Paralleli','Rette parallele ma non equidistanti: la distanza cresce dall\'equatore verso i poli.')+term('Angoli','Meridiani e paralleli si incrociano sempre a 90°.')+term('I limiti','I poli non si possono rappresentare: vicino ai poli il primo diventerebbe infinito. Non si usa oltre i 70° di latitudine.')
sec('mercatore2', head('Cartografia · Mercatore','Meridiani e paralleli sulla carta'), pinned=pcol(txt,540,20)+svgp(X,Y,W,Hh,b,'Reticolo della carta di Mercatore: meridiani verticali equidistanti, paralleli orizzontali sempre più distanti verso l\'alto e il basso, fino a 70 gradi')+lbl,
 notes='Quiz 1.7.2-9 (meridiani rette perpendicolari all\'equatore ed equidistanti), -19 e -4 (paralleli non equidistanti), -33 (angoli di 90°), -34 (non utilizzabile oltre i 70°), -27 (poli non rappresentati).')
X=700

# ---- Latitudini crescenti ----
x0c,x1c,ytop,ybot=140,940,40,560
kk=(ybot-ytop)/math.log(math.tan(math.radians(45+70/2)))
yf=lambda la: ybot-kk*math.log(math.tan(math.radians(45+la/2)))
b=f'<rect x="{x0c}" y="{ytop}" width="{x1c-x0c}" height="{ybot-ytop}" fill="{CHART}" stroke="{NAVY}" stroke-width="3"/>'
b+=''.join(line(x,ytop,x,ybot,GRID,2) for x in range(x0c+80,x1c,80))+''.join(line(x0c,yf(la),x1c,yf(la),CORAL if la==0 else GRID,4 if la==0 else 2) for la in range(0,71,10))
for i,la in enumerate(range(0,70,10)):
    for xs in (100,948): b+=f'<rect x="{xs}" y="{yf(la+10):.1f}" width="30" height="{yf(la)-yf(la+10):.1f}" fill="{NAVY if i%2==0 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="2"/>'
for i,x in enumerate(range(x0c,x1c,80)):
    b+=f'<rect x="{x}" y="570" width="80" height="22" fill="{BLUE if i%2==0 else "#FFFFFF"}" stroke="{BLUE}" stroke-width="2"/>'
for la,c,xx in ((0,SEA,990),(50,CORAL,990)):
    y0_,y1_=yf(la),yf(la+10); b+=f'<path d="M{xx} {y0_:.0f} L{xx+24} {y0_:.0f} L{xx+24} {y1_:.0f} L{xx} {y1_:.0f}" fill="none" stroke="{c}" stroke-width="6"/>'
lbl=lab(X+600,Y+yf(5)-16,330,'0°-10°: 600 miglia',SEA,22,900,'right')+lab(X+600,Y+yf(55)-16,330,'50°-60°: 600 miglia, tratto più lungo',CORAL,22,900,'right')
lbl+=''.join(lab(X+46,Y+yf(la)-14,50,f'{la}°',NAVY,20,900,'right') for la in (0,30,50,60,70))+lab(X+x0c,Y+596,x1c-x0c,'scala delle longitudini (in alto e in basso): primi tutti uguali',BLUE,22,900,'center')
txt=term('La scala delle latitudini','Ai lati della carta: è la scala delle distanze. Il primo si allunga con la latitudine: si misura sempre alla stessa latitudine del tratto.')+term('La scala delle longitudini','In alto e in basso: i primi sono tutti uguali e valgono 1 miglio solo all\'equatore. Non si usa per le distanze.')+note('Compasso sul tratto, poi sulla scala laterale, all\'altezza del tratto.',CORAL,32)
sec('crescenti', head('Cartografia · Mercatore','Latitudini crescenti')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Carta di Mercatore con la scala delle latitudini ai lati, fatta di tratti sempre più lunghi verso i poli, e la scala delle longitudini in alto e in basso con tratti uguali')+lbl,
 notes='Quiz 1.7.2-2 (la scala delle latitudini non è costante e aumenta con la latitudine), -20 (i primi di longitudine sono uguali tra loro), 1.7.1-27 (la longitudine si legge in alto e in basso), 1.7.5-33 e -52 (distanza sulla scala delle latitudini, alla stessa latitudine), 1.7.2-37 (misura della distanza). Esempio sulla 5/D: il tratto tra due punti si riporta sulla scala laterale alla stessa altezza.')

# ---- Isogonia e lossodromia ----
X=128
cx,cy,R=250,320,230
b=globe(cx,cy,R,(30,60),(30,60,90))+line(cx-R,cy,cx+R,cy,CORAL,4)
pts=[]
for i in range(0,71,2):
    la=math.radians(i); lo=math.radians(-60)+math.log(math.tan(math.pi/4+la/2))
    if lo<math.radians(88): pts.append((cx+R*math.cos(la)*math.sin(lo), cy-R*math.sin(la)))
b+=f'<path d="M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+f'" fill="none" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/>'
g,yf=mercator(540,40,1060,600,70,10,52)
b+=g
xA,yA=580,yf(-10); xB,yB=1020,yf(55)
b+=line(xA,yA,xB,yB,CORAL,7)
ang=math.degrees(math.atan2(xB-xA,yA-yB))
for x in range(592,1020,104):
    t=(x-xA)/(xB-xA); y=yA+t*(yB-yA); b+=line(x,y-40,x,y+10,GREEN,4)+f'<path d="M{x} {y-30:.1f} A30 30 0 0 1 {x+30*math.sin(math.radians(ang)):.1f} {y-30*math.cos(math.radians(ang)):.1f}" fill="none" stroke="{SUN}" stroke-width="4"/>'
lbl=lab(X+60,Y+24,380,'sulla sfera: una curva verso il polo',CORAL,22,900,'center')+lab(X+540,Y+4,520,'su Mercatore: una retta',CORAL,22,900,'center')
txt=term('Isogonia','La carta di Mercatore conserva gli angoli della realtà: anche la rotta è isogona.')+term('Lossodromia','La rotta che taglia tutti i meridiani con lo stesso angolo: è quella che si segue con la bussola.')+term('Sulla sfera e sulla carta','Sulla sfera è una curva che si avvolge verso il polo; Mercatore la rettifica in una retta.')+term('Il prezzo','Non è il percorso più breve: quello è l\'ortodromia.')
sec('lossodromia', head('Cartografia · Mercatore','Isogonia e lossodromia'), pinned=pcol(txt,540,20)+svgp(X,Y,W,Hh,b,'A sinistra il globo con la lossodromia che si avvolge verso il polo tagliando i meridiani con angolo costante; a destra la stessa rotta sulla carta di Mercatore, una retta che forma lo stesso angolo con ogni meridiano')+lbl,
 notes='Quiz 1.7.2-11 e -16 (isogonia: la carta mantiene gli angoli della realtà), -31, -46, -47 (Mercatore rende rettilinee le rotte lossodromiche, ad angolo costante). La lossodromia è la rotta più semplice da tenere: la prora non cambia.')
X=700

# ---- Carta gnomonica ----
cx,cy,R=210,360,180
b=globe(cx,cy,R,(30,60),(40,70))+line(cx-R,cy,cx+R,cy,BLUE,4)
tx_,ty_=pol(cx,cy,-45,R); nx,ny=math.cos(math.radians(-135)),math.sin(math.radians(-135))
b+=line(tx_-160*ny,ty_+160*nx,tx_+160*ny,ty_-160*nx,CORAL,6)
for a in (-75,-60,-30,-15):
    gx,gy=pol(cx,cy,a,R); d=R/math.cos(math.radians(a+45)); px_,py_=pol(cx,cy,a,d)
    b+=dash(cx,cy,px_,py_,SUN,3)+f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="6" fill="{SUN}"/>'
b+=glow(cx,cy,SUN,10)
gx0,gy0,gw,gh=470,90,590,420
b+=f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="{CHART}" stroke="{NAVY}" stroke-width="3"/>'
px0,py0=gx0+gw/2,gy0-700
b+=f'<clipPath id="gc"><rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}"/></clipPath><g clip-path="url(#gc)">'
for i in range(-4,5):
    b+=line(px0,py0,px0+i*190,gy0+gh+40,GRID,2)
b+=''.join(f'<circle cx="{px0}" cy="{py0}" r="{r}" fill="none" stroke="{GRID}" stroke-width="2"/>' for r in range(780,1200,80))
b+=f'<path d="M500 250 Q765 520 1030 280" fill="none" stroke="{CORAL}" stroke-width="7"/>'+line(500,250,1030,280,BLUE,7)+'</g>'
b+=f'<circle cx="500" cy="250" r="11" fill="{GREEN}"/><circle cx="1030" cy="280" r="11" fill="{GREEN}"/>'
lbl=lab(X+40,Y+50,380,'piano tangente in un punto',CORAL,22,900)+lab(X+620,Y+206,380,'ortodromia · 6277 miglia',BLUE,22,900,bg='#FFFFFF')+lab(X+620,Y+440,380,'lossodromia · 7606 miglia',CORAL,22,900,bg='#FFFFFF')
txt=term('Carte gnomoniche','Proiezioni centrali di una parte della Terra su un piano tangente in un punto.')+term('Ortodromia','L\'arco di circolo massimo: il percorso più breve tra due punti. Taglia i meridiani con angoli sempre diversi; sulla gnomonica è una retta.')+term('A cosa serve','A pianificare le traversate oceaniche; poi la rotta si riporta a tratti sulla carta di Mercatore. Non serve per la navigazione costiera.')
sec('gnomonica', head('Cartografia · per gli oceani','Carta gnomonica e ortodromia')+col(txt), pinned=svgp(X,Y,W,Hh,b,'A sinistra il globo con il piano tangente e i raggi di proiezione dal centro; a destra la carta gnomonica con i meridiani convergenti: l\'ortodromia è una retta più corta, la lossodromia una curva più lunga')+lbl,
 notes='Quiz 1.7.2-14 (la gnomonica serve a pianificare una traversata oceanica, non la costiera), -55 e -56 (ortodromia, circolo massimo). Esempio del disegno: tra due porti oceanici l\'ortodromia misura 6277 miglia, la lossodromia 7606.')

# ================= RACCOLTA QUIZ (45 minuti) =================
steps=[('1','Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.',CORAL,CORAL_T),
 ('2','Escludi le assurde','Di solito una risposta è palesemente sbagliata: toglila e ragiona sulle altre due.',SEA,SEA_T),
 ('3','Cerca lo scambio','Sopravento o sottovento, Nord o Sud, latitudine o longitudine, destrorsa o sinistrorsa: il trabocchetto è lì.',PURPLE,LILAC_T),
 ('4','Attento ai numeri','Metri o miglia, 3 o 5 volte il fondale, 1:50.000 o 1:5.000: controlla l\'unità di misura.',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,30,INK,800,1.2)}{p(d,24,INK,500,1.35)}</div>' for n,t,d,c,bg in steps)
exam=card(tag("La prova a quiz")+f'<div style="display:flex; gap:48px; align-items:end"><div>{p("quesiti",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{INK}">20</p></div><div>{p("errori ammessi",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{CORAL}">4</p></div><div>{p("tempo",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{INK}">30′</p></div></div>'+p('Tre risposte, una sola esatta. Oggi 36 quiz ufficiali della banca del DD 131/2022 sui due capitoli.',24),None,32,16)
plan=card(tag("I 45 minuti",SEA)+'<ol style="font-size:24px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px"><li>Quiz 1-6 · attracchi, ormeggi, ancoraggi (18)</li><li>Quiz 7-12 · cartografia e segnalamento (18)</li><li>Un minuto a domanda, poi la slide delle risposte e il perché</li></ol>',SEA_T,32,12)
sec('quiz', head('Lezione 03 · ultimi 45 minuti','Raccolta quiz')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div><div style="display:flex; gap:24px">{exam}{plan}</div>',
 notes='Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide, spiegazione compresa. Far rispondere ad alta voce con la lettera, poi chiedere perché le altre due sono sbagliate. Se il tempo stringe, saltare le slide 5 e 11 e lasciarle per casa.', gap=28)
E1='Raccolta quiz · capitolo 1 · DD 131/2022'; E2='Raccolta quiz · capitolo 2 · DD 131/2022'
QZ=[('q01','Quiz 1 · Ormeggi e attracchi',['1.4.4-4','1.4.4-5','1.4.4-6'],E1),('q02','Quiz 2 · Cime e sistemi d\'ormeggio',['1.4.4-8','1.4.4-22','1.4.4-20'],E1),
    ('q03','Quiz 3 · Gavitello e vento',['1.4.4-41','1.4.4-33','1.4.3-47'],E1),('q04','Quiz 4 · Ancora e ancore',['1.4.3-17','1.4.3-10','1.4.3-39'],E1),
    ('q05','Quiz 5 · Calumo, grippia, verifica',['1.4.3-27','1.4.3-26','1.4.3-15'],E1),('q06','Quiz 6 · Tipi di ancoraggio',['1.4.3-22','1.4.3-38','1.4.3-23'],E1),
    ('q07','Quiz 7 · Latitudine e longitudine',['1.7.1-4','1.7.1-5','1.7.1-13'],E2),('q08','Quiz 8 · Gradi, miglia, reticolo',['1.7.1-20','1.7.1-40','1.7.1-41'],E2),
    ('q09','Quiz 9 · Carte e pubblicazioni',['1.7.2-6','1.7.2-25','1.7.8-4'],E2),('q10','Quiz 10 · Simboli e fari',['1.7.2-39','1.7.2-44','1.5.3-45'],E2),
    ('q11','Quiz 11 · AISM-IALA',['1.5.3-32','1.5.3-64','1.5.3-82'],E2),('q12','Quiz 12 · Mercatore e fiumi',['1.7.2-2','1.7.2-31','1.5.3-114'],E2)]
for id_,t,ps,e in QZ:
    quiz_slide(id_,t,ps,False,e)
    quiz_slide(id_+'r',t+' · risposte',ps,True)

closing(['Spring contro i movimenti avanti e indietro, traversini contro lo scostamento; in andana la trappa diventa l\'ormeggio di prua','Con il vento: ancora sopravento; in arrivo si dà per prima la cima sopravento, in partenza si molla per prima la sottovento','Calumo da 3 a 5 volte il fondale; se il rilevamento cambia, l\'ancora ara','Latitudine 0-90° N/S, longitudine 0-180° E/W; 1′ di latitudine = 1 miglio = 1852 m, sulla scala laterale','Entrando in porto rosso a sinistra; cardinali: i coni puntano al nero, i lampi come un orologio'],
 'Prossima lezione · 04 · Primi calcoli, sottocosta, prora e rotta','A casa: i quiz 1.4.4 (ormeggio), 1.4.3 (ancoraggio), 1.7.1 (coordinate), 1.7.2 (carte) e 1.5.3 (fanali e IALA).')
write_deck(OUT,'Lezione 03 · Ormeggi, ancoraggi, carte e segnali',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Capitolo 1 · Attracchi e ormeggi","start":"cap1"},
  "s3":{"description":"Capitolo 1 · Ancore e ancoraggi","start":"salpancora"},"s4":{"description":"Capitolo 2 · Coordinate e misure","start":"cap2"},
  "s5":{"description":"Capitolo 2 · Carte, pubblicazioni e simboli","start":"classificazione"},"s6":{"description":"Capitolo 2 · Fari e segnalamento AISM-IALA","start":"elencofari"},
  "s7":{"description":"Capitolo 2 · Navigazione fluviale e carta di Mercatore","start":"fluviale"},"s8":{"description":"Raccolta quiz: capitolo 1","start":"quiz"},
  "s9":{"description":"Raccolta quiz: capitolo 2","start":"q07"}})
