import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez03/project'
QUAY='#D9C9A8'; QUAY_T='#EADFC6'; LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; MAG='#C2185B'; SHALLOW='#CFE8F3'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Arrivare in banchina':'anchor','I cavi d\'ormeggio':'anchor','Ormeggio di poppa':'anchor',
 'Boe, gavitelli e corpi morti':'lifebuoy','Cime e nodi':'helm','Muoversi in porto e in rada':'helm','Latitudine e longitudine':'map',
 'Leggere le coordinate sulla carta':'grid','La carta di Mercatore':'map','Le carte e la loro scala':'map','Cosa c\'è sulla carta':'lighthouse',
 'Le pubblicazioni nautiche':'book','La rosa dei venti':'compass','Gli strumenti del carteggio':'dividers','La navigazione stimata':'pencil',
 'Spazio, velocità, tempo':'chart','Tre esempi svolti':'pencil','Il carburante sulla carta':'fuel'})

def bollard(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{NAVY}"/><circle cx="{x}" cy="{y}" r="{r*0.4:.0f}" fill="{SUN}"/>'
def rope(d,c=NAVY,w=6):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="{max(1.5,w/3):.1f}" stroke-dasharray="3 6" stroke-linecap="round"/>'
def dot(n,c): return f'<p style="width:44px; height:44px; border-radius:22px; background:{c}; color:#FFFFFF; font-weight:900; font-size:22px; text-align:center; line-height:44px; flex:none">{n}</p>'
def item(n,c,t,d): return f'<div style="display:flex; gap:16px; align-items:start">{dot(n,c)}<div style="display:flex; flex-direction:column; gap:4px">{p(t,28,INK,800,1.25)}{p(d,24,BODY)}</div></div>'
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x}px; top:{y}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(3,'Ormeggi, carte e primi calcoli','Dalla banchina alla carta nautica: cavi, coordinate, scale e la regola S = V × T',
 'Lezione 3. Capitoli del programma della scuola: Attracchi e ormeggi, Cartografia, primi elementi di carteggio (navigazione stimata, miglia, velocità, carburante). All. A al DM 323/2021: punto 4b (ormeggi) e materia 7 (navigazione cartografica). Ordine del manuale Il Frangente: manovre d\'ormeggio, poi coordinate geografiche, carta di Mercatore, pubblicazioni, rosa dei venti, strumenti, navigazione stimata.')
blocks=[('0:00','15′','In banchina: i cavi d\'ormeggio',CORAL),('0:15','25′','Poppa, boe, nodi · quiz 1',SEA),('0:40','25′','Coordinate e carte · quiz 2',PURPLE),('1:05','15′','Rosa e strumenti · quiz 3',BLUE),('1:20','25′','Stima, S = V × T · quiz 4',GREEN),('1:45','15′','Verifica finale',CORAL)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">4 + 4</p>'+p('domande su 20: Manovra e condotta, Navigazione cartografica',26,INK,700)+p('E il carteggio, la prima prova, si fa proprio sulla carta di Mercatore con compasso e squadrette.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>dare i cavi giusti in banchina, di fianco e di poppa</li><li>prendere un gavitello e fare gassa e parlato</li><li>leggere latitudine e longitudine sulla carta</li><li>scegliere la carta e riconoscerne i simboli</li><li>risolvere S = V × T e calcolare il carburante</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 03 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie da 3 quiz e una finale da 6, tutti ufficiali (DD 131/2022). All. C al DM 323/2021: 4 quesiti di Manovra e condotta e 4 di Navigazione cartografica ed elettronica nella scheda da 20. Banca: ormeggio e disormeggio 49 quiz; coordinate 45; carte e Mercatore 56; orientamento e bussola 49; navigazione stimata 71; pubblicazioni 8. Bussola, declinazione e deviazione: lezione 4.')

# ============ ARRIVARE IN BANCHINA (sezione) ============
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
sec('attracco', head('Ormeggi · il vocabolario','Arrivare in banchina')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione trasversale: barca a vela affiancata alla banchina, con parabordo tra scafo e banchina e cima dalla galloccia di bordo alla bitta di banchina')+lbl,
 notes='Quiz 1.4.4-30 (attracco = avvicinamento a banchina o galleggiante), -4 (attraccata = assicurata con i cavi d\'ormeggio), 1.4.4-21 (parlato per i parabordi a pulpiti e draglie). Mostrare in aula una galloccia e come si dà volta.')

# ============ CAVI ALL'INGLESE (dall'alto) ============
b=f'<rect x="0" y="0" width="1092" height="150" fill="{QUAY}"/>'+line(0,150,1092,150,NAVY,5)
b+=''.join(f'<rect x="{x}" y="152" width="44" height="22" rx="11" fill="{BLUE}"/>' for x in (380,524,680))
b+=topboat(546,275,600,0,'#FFFFFF',NAVY,4)
L=[('M790 238 L1000 128',NAVY),('M300 190 L90 128',NAVY),('M770 228 L600 128',CORAL),('M322 186 L490 128',CORAL),('M735 212 L740 128',SEA),('M350 182 L345 128',SEA)]
for d,c in L: b+=rope(d,c,7)
b+=''.join(bollard(x,128) for x in (90,345,490,600,740,1000))
for (n,x,y,c) in [(1,915,210,NAVY),(6,180,190,NAVY),(2,680,212,CORAL),(5,420,188,CORAL),(3,770,165,SEA),(4,315,158,SEA)]: b+=num(x,y,n,c,20)
b+=arrow(900,470,1000,470,NAVY,4,16)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+lab(X+780,Y+486,200,'prua',NAVY,24,800,'right')
txt=item('1·6',NAVY,'Prodiera e poppiera','Le cime di prua e di poppa: tengono la barca al suo posto.')+item('2·5',CORAL,'Spring','Da prua o da poppa corrono verso il centro barca: bloccano i movimenti avanti e indietro.')+item('3·4',SEA,'Traversini','Perpendicolari alla banchina: non fanno scostare la barca.')
sec('cavi', head('Ormeggio all\'inglese · di fianco','I cavi d\'ormeggio')+col(txt+note('Senza spring la barca scorre lungo la banchina!',CORAL,38),540,28), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto di una barca ormeggiata di fianco: prodiera, poppiera, due spring incrociati verso il centro e due traversini perpendicolari alla banchina')+lbl,
 notes='Quiz 1.4.4-5 (spring: movimenti longitudinali), -13 (definizione di spring), -6 (traversini: non far scostare), -10, -11, -12 (figure: senza spring la barca si muove lungo l\'asse longitudinale). Nel disegno i numeri sono colorati come le cime in legenda.')

# ============ ORMEGGIO DI POPPA ============
b=f'<rect x="0" y="0" width="1092" height="130" fill="{QUAY}"/>'+line(0,130,1092,130,NAVY,5)
b+=f'<path d="M40 598 L1052 598" stroke="{NAVY}" stroke-width="7" stroke-dasharray="12 7"/>'
for x in (330,762):
    b+=topboat(x,340,380,90,'#FFFFFF',NAVY,3,0.45,False)+rope(f'M{x} 528 L{x} 598',SOFT,4)
b+=rope('M455 124 Q470 420 546 598',SEA,4)
b+=topboat(546,340,380,90,'#FFFFFF',NAVY,4)
b+=rope('M515 168 L610 112',CORAL,7)+rope('M577 168 L482 112',CORAL,7)+rope('M546 528 L546 598',SEA,8)
b+=''.join(bollard(x,112) for x in (482,610))+bollard(455,118,9)
b+=num(640,150,1,CORAL,20)+num(430,300,2,SEA,20)+num(990,560,3,NAVY,20)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+lab(X+640,Y+520,300,'catenaria sul fondo',NAVY,24,800)
txt=item(1,CORAL,'Cime di poppa incrociate','Con la risacca impediscono alla poppa di spostarsi di lato.')+item(2,SEA,'Trappa','Nei marina unisce la catenaria alla banchina: la si recupera e diventa l\'ormeggio di prua, verso il largo.')+item(3,NAVY,'Catenaria','La catena posata sul fondo, parallela alla banchina.')+item('↺',PURPLE,'Doppino','Una cima fatta girare attorno alla bitta, con i due capi a bordo: si molla senza scendere a terra.')
sec('poppa', head('Ormeggio di poppa · «alla mediterranea»','Ormeggio di poppa')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto: barca ormeggiata di poppa in un marina, con le cime di poppa incrociate e la trappa che dalla prua va alla catenaria sul fondo')+lbl,
 notes='Quiz 1.4.4-7 (cime di poppa incrociate con la risacca), -22 (trappa), -8 (doppino). Manovra: lezione 2, effetti combinati (elica sinistrorsa: si retrocede presentando il giardinetto di dritta, quiz 1.4.4-29). I quiz 1.4.4-14…-17 e -25…-28 chiedono quale cima dare o mollare per prima e da che posizione partire guardando una figura: si allenano sulle figure del manuale.')

# ============ BOE E GAVITELLI ============
b=f'<rect x="0" y="200" width="1092" height="420" fill="{WATER}" fill-opacity="0.2"/>'+line(0,200,1092,200,SEA,3)
b+=f'<path d="M0 560 Q270 540 546 562 T1092 552 L1092 620 L0 620 Z" fill="{LAND}"/>'
b+=f'<rect x="660" y="515" width="130" height="58" rx="8" fill="#9AA5B1" stroke="{NAVY}" stroke-width="4"/><circle cx="725" cy="508" r="10" fill="none" stroke="{NAVY}" stroke-width="5"/>'
b+=f'<path d="M725 498 Q690 400 700 320 Q708 250 722 222" fill="none" stroke="{NAVY}" stroke-width="9" stroke-dasharray="11 6"/>'
b+=f'<ellipse cx="724" cy="198" rx="40" ry="26" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/><rect x="684" y="190" width="80" height="12" fill="#FFFFFF"/>'
b+=profile(40,205,470)
b+=rope('M498 150 Q600 175 716 232',SEA,6)
for yy in (60,110): b+=arrow(1040,yy,900,yy,'#97A6B4',8,24)
lbl=lab(X+780,Y+130,200,'Gavitello',CORAL)+lab(X+470,Y+250,230,'Cima sotto il gavitello',SEA)+lab(X+740,Y+360,200,'Catena',NAVY)+lab(X+810,Y+470,240,'Corpo morto',INK)+lab(X+900,Y+136,160,'vento',SOFT,24,800)
txt=term('Corpo morto','Un blocco di cemento sul fondo con un anello: la catena sale fino al gavitello.')+term('Come arrivare','A lento moto, con la prora al vento o alla corrente: ci si presenta sottovento al gavitello.')+term('Dove legarsi','Alla cima sotto il gavitello, non al gavitello.')+term('Ormeggio a due boe','Solo se una boa è a proravia e l\'altra a poppavia.')
sec('boe', head('Ormeggiarsi in rada','Boe, gavitelli e corpi morti')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione sotto il mare: corpo morto sul fondo, catena che sale al gavitello e barca che arriva con la prua al vento e si lega alla cima sotto il gavitello')+lbl,
 notes='Quiz 1.4.4-2 (corpo morto), -3 (avvicinamento a lento moto con prora al vento o alla corrente), -41 (sottovento al gavitello), -33 (ci si lega alla cima sotto il gavitello), -9 (due boe: una a proravia e una a poppavia). Il quiz 1.4.4-43 sull\'ancora galleggiante è oscurato; l\'ancora galleggiante (1.4.4-42, -44) si vede nella lezione 4.')

# ============ CIME E NODI ============
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
cc=''.join(card(svgi(320,220,s,alt,dw=330,dh=227)+h3(t,30)+p(d,24),None,24,10) for s,t,d,alt in K)
sec('nodi', head('Il materiale','Cime e nodi')+f'<div style="display:flex; gap:22px">{cc}</div>'+note('All\'esame pratico: gassa d\'amante, parlato, nodo di bitta e bozza (All. D).',PURPLE,36),
 notes='Quiz 1.4.4-19 (poliestere per gli ormeggi), -18 (polipropilene solo per sagole galleggianti di salvataggio), -20 (gassa d\'amante), -21 (parlato). L\'All. D al DM 323/2021 chiede di saper fare i nodi: tenere in aula spezzoni di cima e far provare a tutti.')

# ============ PORTO E RADA ============
def thruster():
    s=f'<rect x="380" y="0" width="100" height="300" fill="{QUAY}"/>'+line(380,0,380,300,NAVY,5)
    s+=topboat(250,150,250,-90,'#FFFFFF',NAVY,3,0.35,False)+topboat(320,150,250,-90,'#FFFFFF',NAVY,4)
    s+=f'<rect x="298" y="52" width="44" height="12" rx="6" fill="{CORAL}"/>'+arrow(270,58,300,58,CORAL,5,14)+arrow(342,58,372,58,CORAL,5,14)
    return s+arrow(190,230,262,230,SEA,6,20)
def rada():
    s=''
    for x,y,a in ((90,90,-60),(250,70,-70),(390,110,-55)):
        s+=topboat(x,y,110,a,'#FFFFFF',NAVY,3)+dash(x+30*math.cos(math.radians(a)),y+30*math.sin(math.radians(a)),x+85*math.cos(math.radians(a)),y+85*math.sin(math.radians(a)),NAVY,3)
    s+=topboat(240,225,150,0,'#FFFFFF',NAVY,4)
    s+=f'<path d="M165 225 L95 205 M165 225 L95 245" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
    return s
def logscan():
    s=f'<rect x="0" y="120" width="480" height="180" fill="{WATER}" fill-opacity="0.22"/>'+line(0,120,480,120,SEA,3)
    s+=f'<path d="M0 285 Q240 262 480 285 L480 300 L0 300 Z" fill="{LAND}"/>'
    s+=profile(60,126,360,sup=True)
    s+=f'<path d="M270 172 L230 282 L310 282 Z" fill="{SUN}" fill-opacity="0.35"/><rect x="262" y="160" width="16" height="14" rx="4" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
    s+=f'<circle cx="190" cy="176" r="10" fill="{PURPLE}" stroke="{NAVY}" stroke-width="2"/>'
    return s
P3=[(thruster(),'Elica di prua (bow thruster)','Per ormeggiarti sul <b>lato dritto</b>: accosta a dritta e usa l\'elica di prua per traslare parallelo alla banchina.','Vista dall\'alto: la barca trasla verso la banchina a dritta grazie all\'elica di prua'),
    (rada(),'In rada','Procedi <b>piano</b>, anche mettendo e togliendo la marcia: la tua onda disturba e mette in pericolo le barche alla fonda.','Vista dall\'alto: barche alla fonda e una barca che attraversa la rada lentamente'),
    (logscan(),'Solcometro ed ecoscandaglio','Il <b>solcometro</b> (log) dà velocità e miglia percorse, ma con la corrente non è attendibile. L\'<b>ecoscandaglio</b> misura il fondale.','Barca di profilo con il sensore del solcometro e il cono dell\'ecoscandaglio verso il fondo')]
cc=''.join(card(svgi(480,300,s,alt,dw=440,dh=275)+h3(t,30)+p(d,24),None,24,10) for s,t,d,alt in P3)
sec('porto', head('Manovra e condotta','Muoversi in porto e in rada')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 1.4.4-23 (bow thruster: accosto a dritta per traslare parallelo alla banchina), -35 e -37 (in rada: velocità contenuta, attenzione all\'onda), -24 e -46 (solcometro: velocità e cammino), -48 (non attendibile con corrente), -47 (ecoscandaglio). Il solcometro servirà subito per S = V × T.')

quiz_slide('quiz1','Quiz 1 · Ormeggi',['1.4.4-5','1.4.4-7','1.4.4-3'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.4.4-5','1.4.4-7','1.4.4-3'],True)

# ============ COORDINATE ============
cx,cy,R=546,320,270
b=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#DFF1F8" stroke="{NAVY}" stroke-width="5"/>'
for lat in (30,60):
    for sg in (1,-1):
        yy=cy-sg*R*math.sin(math.radians(lat)); hw=R*math.cos(math.radians(lat)); b+=line(cx-hw,yy,cx+hw,yy,'#8FB3C6',3)
for rx in (135,234): b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{R}" fill="none" stroke="#8FB3C6" stroke-width="3"/>'
b+=line(cx,cy-R,cx,cy+R,SEA,7)+line(cx-R,cy,cx+R,cy,CORAL,7)
b+=line(cx,cy,cx+135,cy,BLUE,12)+f'<path d="M{cx+135} {cy} A135 {R} 0 0 0 649 146" fill="none" stroke="{SUN}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<circle cx="649" cy="146" r="13" fill="{CORAL}" stroke="#FFFFFF" stroke-width="4"/><circle cx="{cx}" cy="{cy-R}" r="9" fill="{NAVY}"/><circle cx="{cx}" cy="{cy+R}" r="9" fill="{NAVY}"/>'
b+=arrow(400,92,538,140,INK,3)+arrow(880,200,770,220,INK,3)
lbl=lab(X+466,Y+8,160,'Polo Nord',NAVY,24,800,'center')+lab(X+466,Y+594,160,'Polo Sud',NAVY,24,800,'center')+lab(X+170,Y+60,240,'Greenwich',SEA,24,800,'right')
lbl+=lab(X+830,Y+296,200,'Equatore',CORAL,24,800)+lab(X+890,Y+180,200,'Parallelo',SOFT,24,800)+lab(X+668,Y+104,60,'P',CORAL,28,900)
lbl+=lab(X+690,Y+210,160,'φ lat.',INK,26,900,bg=SUN_T)+lab(X+560,Y+334,160,'λ long.',BLUE,26,900,bg='#FFFFFF')
txt=term('Latitudine φ','Arco di meridiano dall\'equatore al punto: da 0° a 90° Nord o Sud.')+term('Longitudine λ','Arco di equatore da Greenwich al meridiano del punto: da 0° a 180° Est o Ovest.')+term('Paralleli','Circoli minori paralleli all\'equatore: stessa latitudine.')+term('Meridiani','Semicircoli da polo a polo: stessa longitudine.')
sec('coordinate', head('Cartografia · le coordinate','Latitudine e longitudine')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Globo con equatore, meridiano di Greenwich, paralleli e meridiani; il punto P con la sua latitudine lungo il meridiano e la longitudine lungo l\'equatore')+lbl,
 notes='Quiz 1.7.1-2, -3, -4, -35 (latitudine), -1, -5, -12, -17, -36 (longitudine), -6, -26, -33 (meridiani), -14, -18, -32 (paralleli), -8, -15, -24 (equatore e Greenwich), -22 e -25 (λ e φ), -31 (95° di latitudine è impossibile), -30 (servono entrambe le coordinate).')

# ============ LEGGERE LE COORDINATE ============
b=f'<rect x="60" y="40" width="972" height="540" fill="{CHART}" stroke="{NAVY}" stroke-width="4"/>'
bw=[];wh=[]
for i in range(10):
    y0=60+i*50; (bw if i%2==0 else wh).append(f'M60 {y0} h18 v50 h-18 Z M1014 {y0} h18 v50 h-18 Z')
for i in range(18):
    x0=80+i*52; (bw if i%2==0 else wh).append(f'M{x0} 40 v18 h52 v-18 Z M{x0} 562 v18 h52 v-18 Z')
b+=f'<path d="{" ".join(bw)}" fill="{NAVY}"/><path d="{" ".join(wh)}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.5"/>'
b+=f'<path d="M120 480 Q170 380 260 400 Q330 330 400 380 Q430 450 360 500 Q260 540 160 520 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<path d="M760 70 Q840 160 930 120 Q1000 150 1012 70 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=dash(600,300,78,300,CORAL,3)+dash(600,300,600,562,BLUE,3)+f'<circle cx="600" cy="300" r="14" fill="{CORAL}" stroke="#FFFFFF" stroke-width="4"/>'
b+=f'<path d="M100 60 L130 60 M100 110 L130 110" stroke="{SUN}" stroke-width="4"/>'
lbl=lab(X+86,Y+62,260,'42°50′ N',NAVY,22,800)+lab(X+84,Y+506,260,'42°41′ N',NAVY,22,800)+lab(X+84,Y+586,200,'010°10′ E',NAVY,22,800)+lab(X+836,Y+586,200,'010°27′ E',NAVY,22,800,'right')
lbl+=lab(X+300,Y+74,260,'1′ = 1 miglio',SUN,24,900,bg='#FFFFFF')+lab(X+630,Y+250,380,'P · 42°46′,0 N · 010°19′,5 E',CORAL,26,900,bg='#FFFFFF')
lbl+=lab(X+120,Y+256,300,'latitudine: ai lati',CORAL,22,800)+lab(X+612,Y+470,300,'longitudine: in alto e in basso',BLUE,22,800)
txt=term('Gradi, primi, decimi','1° = 60′; il primo si divide in decimi: 42°46′,3 N.')+term('Il miglio','1′ di latitudine = 1 miglio = 1852 m. Quindi 1° = 60 miglia.')+term('Rotte e coordinate','Con Rv 090° o 270° la latitudine non cambia; con Rv 000° o 180° non cambia la longitudine.')
sec('leggere', head('Cartografia · sulla carta','Leggere le coordinate sulla carta')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Riquadro di carta nautica con le scale graduate ai bordi: la latitudine del punto P si legge sulla scala laterale, la longitudine su quella in basso')+lbl,
 notes='Quiz 1.7.1-9, -20, 1.7.5-20, -21, -50 (miglio = 1′ di latitudine = 1852 m), 1.7.5-32 e -37 (1° = 60 miglia; 180 miglia = 3°), -53 (4′,4 = 4,4 miglia), 1.7.1-11 (grado, primi, secondi), -27 (longitudine in alto e in basso), -34 (Rv 090: latitudine invariata), -23 (Rv 180: longitudine invariata). In aula: far leggere le coordinate di un faro sulla 5/D.')

# ============ MERCATORE ============
b=f'<rect x="80" y="90" width="340" height="480" fill="{SEA}" fill-opacity="0.12"/>'+line(80,90,80,570,SEA,4)+line(420,90,420,570,SEA,4)
b+=f'<ellipse cx="250" cy="90" rx="170" ry="26" fill="none" stroke="{SEA}" stroke-width="4"/><ellipse cx="250" cy="570" rx="170" ry="26" fill="none" stroke="{SEA}" stroke-width="4"/>'
b+=f'<circle cx="250" cy="330" r="150" fill="#DFF1F8" stroke="{NAVY}" stroke-width="4"/>'+line(100,330,400,330,CORAL,4)
for lat in (20,45):
    y1=330-170*math.tan(math.radians(lat)); b+=dash(250,330,420,y1,CORAL,3)+f'<circle cx="{420}" cy="{y1:.0f}" r="7" fill="{CORAL}"/>'
b+=f'<circle cx="250" cy="330" r="7" fill="{NAVY}"/>'
k=500/math.log(math.tan(math.radians(80)))
yy=lambda la: 560-k*math.log(math.tan(math.radians(45+la/2)))
b+=f'<rect x="520" y="50" width="540" height="520" fill="{CHART}" stroke="{NAVY}" stroke-width="3"/>'
b+=''.join(line(x,50,x,570,'#8FB3C6',2) for x in range(580,1060,60))
b+=''.join(line(520,yy(la),1060,yy(la),CORAL if la==0 else '#8FB3C6',4 if la==0 else 2) for la in range(0,80,10))
b+=dpath('M560 540 Q650 120 1030 110',NAVY,4)+line(560,540,1030,110,CORAL,7)
lbl=lab(X+80,Y+14,340,'Proiezione su un cilindro',SEA,24,800,'center')+lab(X+530,Y+10,520,'Paralleli sempre più distanti',INK,24,800,'center')
lbl+=lab(X+800,Y+300,260,'Lossodromia: una retta',CORAL,24,900,bg='#FFFFFF')+lab(X+600,Y+150,200,'Ortodromia',NAVY,24,900,bg='#FFFFFF')+lab(X+440,Y+546,90,'0°',CORAL,22,800,'right')+lab(X+440,Y+58,90,'70°',SOFT,22,800,'right')
txt=term('Isogona','Conserva gli angoli: la rotta a angolo costante (lossodromia) è una retta.')+term('Meridiani e paralleli','Rette perpendicolari. I paralleli si allontanano verso i poli: la scala delle latitudini cresce.')+term('I limiti','Non si usa oltre i 70°; i poli non si possono rappresentare.')+term('Ortodromia','L\'arco di circolo massimo, il più breve: si pianifica sulla carta gnomonica.')
sec('mercatore', head('Cartografia · la proiezione','La carta di Mercatore')+col(txt), pinned=svgp(X,Y,W,Hh,b,'A sinistra il globo proiettato su un cilindro dal centro della Terra; a destra la carta di Mercatore con i paralleli sempre più distanti, la lossodromia retta e l\'ortodromia curva')+lbl,
 notes='Quiz 1.7.2-4, -9, -19, -33 (reticolato), -2 (la scala delle latitudini aumenta con la latitudine), -11 e -16 (isogonia), -31, -46, -47 (lossodromia retta), -34 e -27 (oltre 70°, poli), -28 (punto di proiezione al centro della Terra: è la risposta ministeriale; la costruzione reale è matematica), -14, -55, -56 (gnomonica e ortodromia), -20 (i primi di longitudine sono uguali).')

# ============ SCALE ============
import random
rnd=random.Random(7)
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
SC=[(1,'Generali','1:3.000.000 e meno','Grandi traversate e pianificazione di lunghe rotte.',CORAL),
    (2.6,'Di atterraggio','tra generali e costiere','Per avvicinarsi alla costa dal largo.',SUN),
    (7,'Costiere','1:100.000 · 1:50.000','Per la navigazione costiera. La 5/D è in scala 1:100.000.',SEA),
    (18,'Dei litorali','più grandi delle costiere','Tratti di costa in dettaglio.',BLUE),
    (60,'Piani nautici','1:5.000 circa','Porti, rade, isolotti: banchine e punti d\'ormeggio.',PURPLE)]
cc=''.join(card(svgi(300,190,zoom(z),f'Carta {t.lower()}: la stessa costa a ingrandimento crescente',dw=270,dh=171)+tag(s,c)+h3(t,30)+p(d,23),None,22,8) for z,t,s,d,c in SC)
sec('scale', head('Cartografia · le carte','Le carte e la loro scala')+f'<div style="display:flex; gap:18px">{cc}</div>'
 +f'<div style="display:flex; gap:40px; align-items:center">{note("Scala più grande = denominatore più piccolo: 1:5.000 è più grande di 1:100.000",CORAL,38)}</div>'
 +p('Le carte 5/D e 42/D dell\'esame sono <b>didattiche</b>: non sono aggiornate e non valgono per navigare.',26,INK),
 notes='Quiz 1.7.2-5 e -17 (classificazione per scala), -6 (generali 1:3.000.000 e inferiore), -18 (generali per grandi distanze), -7, -22, -35 (costiere, 1:100.000, 1:50.000 costiera a grande scala), -49 (litorali), -12, -13, -23 (piani nautici e pianetti, 1:5.000), -10 (la piccola scala non serve per la costiera), -25 (scala maggiore = denominatore minore), -26 (carte didattiche). Il disegno mostra la stessa costa ingrandita: nel piano nautico compaiono i moli.')

# ============ SIMBOLI ============
def awash(x,y,s=1): return f'<path d="M{x-12*s} {y} h{24*s} M{x} {y-12*s} v{24*s} M{x-8*s} {y-8*s} l{16*s} {16*s} M{x-8*s} {y+8*s} l{16*s} {-16*s}" stroke="{NAVY}" stroke-width="{3*s}" stroke-linecap="round"/>'
def sub(x,y,s=1): return f'<circle cx="{x}" cy="{y}" r="{18*s}" fill="{SHALLOW}" stroke="{NAVY}" stroke-width="{2.5*s}" stroke-dasharray="2 4"/><path d="M{x-10*s} {y} h{20*s} M{x} {y-10*s} v{20*s}" stroke="{NAVY}" stroke-width="{3*s}"/>'
def wreck(x,y,s=1): return f'<path d="M{x-24*s} {y} L{x+24*s} {y} L{x+15*s} {y+10*s} L{x-15*s} {y+10*s} Z" fill="{NAVY}"/><path d="M{x-4*s} {y} l{-8*s} {-16*s} M{x+8*s} {y} l{6*s} {-14*s}" stroke="{NAVY}" stroke-width="{3*s}"/>'
def anch(x,y,s=1,c=MAG): return f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="3.5" stroke-linecap="round"><circle cx="0" cy="-16" r="5"/><path d="M0 -11 V16 M-9 -5 H9 M-15 6 Q-12 18 0 16 Q12 18 15 6"/></g>'
def noanch(x,y,s=1): return anch(x,y,s)+f'<path d="M{x-18*s} {y-18*s} L{x+18*s} {y+18*s}" stroke="{MAG}" stroke-width="{4*s}" stroke-linecap="round"/>'
def light(x,y,s=1): return f'<path d="M{x} {y} Q{x+10*s} {y-30*s} {x+28*s} {y-44*s} Q{x+18*s} {y-18*s} {x} {y} Z" fill="{MAG}" fill-opacity="0.85"/><circle cx="{x}" cy="{y}" r="{5*s}" fill="{NAVY}"/>'
cp=[(0,150),(90,120),(180,160),(260,110),(350,90),(420,140),(500,120),(560,70),(640,90),(700,40),(760,60)]
cl='M'+' L'.join(f'{a} {b_}' for a,b_ in cp)
b=f'<rect x="0" y="0" width="760" height="620" fill="#FFFFFF"/>'
b+=f'<path d="{cl} L760 {cp[-1][1]+90} ' + ' '.join(f'L{a} {b_+90}' for a,b_ in reversed(cp)) + f' Z" fill="{SHALLOW}"/>'
b+=f'<path d="{cl} L760 0 L0 0 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=''.join(f'<path d="M'+' L'.join(f'{a} {b_+off}' for a,b_ in cp)+f'" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="10 7"/>' for off in (90,200))
b+=light(640,90,1.3)+awash(300,230)+sub(520,350)+wreck(170,470)+anch(620,520,1.2)+noanch(360,540,1.2)
lbl=''.join(lab(128+x,Y+y,60,t,NAVY,24,700) for x,y,t in [(80,220,'3'),(440,250,'7'),(250,360,'12'),(640,380,'18'),(90,560,'25'),(520,470,'30')])
lbl+=''.join(f'<p style="position:absolute; left:{128+x}px; top:{Y+y}px; font-size:26px; font-style:italic; font-weight:700; color:{NAVY}">{t}</p>' for x,y,t in [(200,300,'r'),(560,250,'s'),(400,420,'f')])
lbl+=lab(128+660,Y+60,90,'F',MAG,26,900)
def leg(ic,t,d): return f'<div style="display:flex; gap:14px; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 16px; border-radius:22px">{ic}<div style="display:flex; flex-direction:column; gap:2px">{p(t,24,INK,800,1.2)}{p(d,22,BODY,400,1.3)}</div></div>'
ico=lambda body: f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" style="width:64px; height:64px; flex:none">{body}</svg>'
txtic=lambda t,c=NAVY,it=False: f'<p style="width:64px; flex:none; font-size:30px; font-weight:800; text-align:center; color:{c};{" font-style:italic;" if it else ""}">{t}</p>'
L8=[(ico(f'<path d="M4 40 Q20 24 32 34 T60 28" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 6"/>'),'Isobate','Linee batimetriche: uguale profondità.'),
    (txtic('12'),'Scandagli','Profondità in metri.'),
    (txtic('r f s',NAVY,True),'Natura del fondo','r roccia · f fango · s sabbia.'),
    (ico(awash(32,32,1.4)),'Scoglio affiorante','Emerge con la bassa marea.'),
    (ico(sub(32,32,1.4)),'Scogli sommersi','Pericolosi per la navigazione.'),
    (ico(wreck(32,40,1.1)),'Relitto','Qui in parte emergente.'),
    (ico(anch(20,34,0.9)+noanch(46,34,0.9)),'Fonda · divieto','Ancoraggio, ancoraggio vietato.'),
    (ico(light(24,48,1.1)),'Luce · «F»','F = luce fissa; P.A. = posizione approssimata.')]
grid=f'<div style="margin-left:792px; display:grid; grid-template-columns:1fr 1fr; gap:14px">{"".join(leg(*x) for x in L8)}</div>'
sec('simboli', head('Cartografia · simboli','Cosa c\'è sulla carta')+grid, pinned=svgp(128,Y,760,620,b,'Carta nautica di fantasia con costa, isobate tratteggiate, scandagli, natura del fondo, scoglio affiorante, scogli sommersi, relitto, zona di fonda e di divieto e un faro')+lbl, gap=24,
 notes='Quiz 1.7.2-8, -48 (isobate), -24 (profondità, elevazioni, segnali), -15, -29 (natura del fondo), -38 (r = roccioso), -39 (f = fangoso), -41 (scoglio affiorante), -42 (scogli sommersi), -52 (relitto in parte emergente), -45, -51, -54 (ancoraggio, divieto, punto di fonda), -32 (F = luce fissa), -44 (P.A.). Altri simboli in figura: -40 (zona regolamentata), -43 (cavo abbandonato), -50 (schema di separazione del traffico), -53 (condotta). I numeri e le lettere sulla carta sono in corsivo.')

# ============ PUBBLICAZIONI ============
def book(c,icon):
    s=f'<rect x="70" y="18" width="170" height="200" rx="14" fill="{c}" stroke="{NAVY}" stroke-width="4"/><rect x="70" y="18" width="26" height="200" rx="8" fill="{NAVY}" fill-opacity="0.35"/>'
    s+=f'<rect x="110" y="40" width="112" height="16" rx="8" fill="#FFFFFF" fill-opacity="0.8"/><rect x="110" y="64" width="80" height="10" rx="5" fill="#FFFFFF" fill-opacity="0.6"/>'
    return s+f'<g transform="translate(166 150)">{icon}</g>'
ic_list=''.join(f'<rect x="-40" y="{-40+i*22}" width="80" height="10" rx="5" fill="#FFFFFF"/>' for i in range(4))
ic_warn=f'<path d="M0 -44 L46 36 L-46 36 Z" fill="#FFFFFF"/><rect x="-5" y="-18" width="10" height="32" rx="5" fill="{CORAL}"/><circle cx="0" cy="24" r="6" fill="{CORAL}"/>'
ic_coast=f'<path d="M-50 30 Q-30 -30 0 -10 Q20 -40 50 -20 L50 40 L-50 40 Z" fill="#FFFFFF"/>'+f'<path d="M-50 40 L50 40" stroke="{NAVY}" stroke-width="4"/>'
ic_light=f'<path d="M-12 40 L-7 -20 L7 -20 L12 40 Z" fill="#FFFFFF"/><rect x="-10" y="-34" width="20" height="14" rx="3" fill="{SUN}"/><path d="M12 -30 L44 -46 L44 -14 Z" fill="{SUN}" fill-opacity="0.9"/>'
PB=[(book(BLUE,ic_list),'Catalogo I.I. 3001','L\'elenco di tutte le carte e pubblicazioni dell\'Istituto Idrografico della Marina.'),
    (book(CORAL,ic_warn),'Avvisi ai Naviganti','Aggiornano carte e pubblicazioni; le correzioni si annotano a margine della carta.'),
    (book(SEA,ic_coast),'Portolano','Descrive coste, pericoli e porti. «Traversìa del 2° quadrante»: porto esposto a Levante, Scirocco e Ostro.'),
    (book(PURPLE,ic_light),'Elenco dei Fari e Segnali da nebbia','Posizione, descrizione e caratteristiche dei segnali luminosi e sonori.')]
cc=''.join(card(svgi(320,236,s,f'Copertina illustrata: {t}',dw=300,dh=221)+h3(t,28)+p(d,23),None,22,10) for s,t,d in PB)
sec('pubblicazioni', head('I documenti nautici','Le pubblicazioni nautiche')+f'<div style="display:flex; gap:20px">{cc}</div>'
 +note('Nuova edizione: modifiche essenziali per la sicurezza. Ristampa: nessuna nuova correzione.',SEA,36),
 notes='Quiz 1.7.8-1 (catalogo I.I. 3001), -2 e -4 (aggiornamenti, Avvisi ai Naviganti), 1.7.2-3 (aggiornamenti a margine della carta), -7 e -5 (Portolano, venti di traversia), -6 (Elenco dei Fari), -8 (documenti nautici), -3 e 1.7.2-36 (ristampa e nuova edizione), 1.7.2-1 (l\'I.I.M.M. copre i mari italiani e il Mediterraneo).')

quiz_slide('quiz2','Quiz 2 · Coordinate e carte',['1.7.1-5','1.7.2-2','1.7.2-25'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.7.1-5','1.7.2-2','1.7.2-25'],True)

# ============ ROSA DEI VENTI ============
rc,ry,RR=350,310,225
pt=lambda a,r: (rc+r*math.sin(math.radians(a)), ry-r*math.cos(math.radians(a)))
b=''
for k,c in enumerate(['#FFE7A8','#CFEFF2','#FFD5C7','#E0D7FA']):
    a0,a1=k*90,(k+1)*90; p0=pt(a0,RR); p1=pt(a1,RR)
    b+=f'<path d="M{rc} {ry} L{p0[0]:.1f} {p0[1]:.1f} A{RR} {RR} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{c}"/>'
b+=f'<circle cx="{rc}" cy="{ry}" r="{RR}" fill="none" stroke="{NAVY}" stroke-width="4"/>'
tk=' '.join(f'M{pt(a,RR)[0]:.1f} {pt(a,RR)[1]:.1f} L{pt(a,RR-(22 if a%30==0 else 11))[0]:.1f} {pt(a,RR-(22 if a%30==0 else 11))[1]:.1f}' for a in range(0,360,10))
b+=f'<path d="{tk}" stroke="{NAVY}" stroke-width="3"/>'
star=[]
for i in range(16):
    a=i*22.5; r=200 if i%4==0 else (130 if i%2==0 else 34); star.append(pt(a,r))
b+='<polygon points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in star)+f'" fill="{NAVY}" fill-opacity="0.88"/>'
b+=f'<circle cx="{rc}" cy="{ry}" r="12" fill="{SUN}"/>'
tip=pt(157,215); b+=arrow(rc,ry,tip[0],tip[1],CORAL,8,26)
lbl=''
for a,t in [(0,'N'),(45,'NE'),(90,'E'),(135,'SE'),(180,'S'),(225,'SW'),(270,'W'),(315,'NW')]:
    x,y=pt(a,262); lbl+=big(128+x-50,Y+y-18,100,t,NAVY if a%90==0 else SOFT,34 if a%90==0 else 26)
for a,t,c in [(45,'I','#B77900'),(135,'II',SEA),(225,'III',CORAL),(315,'IV',PURPLE)]:
    x,y=pt(a,178); lbl+=big(128+x-40,Y+y-24,80,t,c,44)
x,y=pt(157,215); lbl+=lab(128+x+14,Y+y-10,120,'157°',CORAL,30,900,bg='#FFFFFF')
chips=''.join(f'<p style="font-size:22px; font-weight:800; color:{INK}; background:{bg}; padding:8px 14px; border-radius:18px">{t}</p>' for t,bg in [('N · Tramontana',SUN_T),('NE · Grecale',SUN_T),('E · Levante',SEA_T),('SE · Scirocco',SEA_T),('S · Ostro',CORAL_T),('SW · Libeccio',CORAL_T),('W · Ponente',LILAC_T),('NW · Maestrale',LILAC_T)])
right=(term('Angoli da 000° a 360°','Si contano dal Nord in senso orario, sempre con tre cifre: 045°, 157°, 320°.')
      +term('Quattro quadranti','I NE 000-090 · II SE 090-180 · III SW 180-270 · IV NW 270-360. Esempio: 157° è nel II.')
      +term('Cardinali e intercardinali','N, E, S, W e NE, SE, SW, NW. Sulla carta il Nord è in alto.')
      +f'<div style="display:flex; flex-wrap:wrap; gap:10px">{chips}</div>')
sec('rosa', head('Orientarsi','La rosa dei venti')+f'<div style="margin-left:760px; display:flex; flex-direction:column; gap:20px">{right}</div>', pinned=svgp(128,Y,700,620,b,'Rosa dei venti con i quattro quadranti colorati, le direzioni cardinali e intercardinali e una freccia verso 157 gradi nel secondo quadrante')+lbl,
 notes='Quiz 1.7.4-1, -4, -5, -6, -7 (in quale quadrante: 157° II, 224° III, 320° IV, 038° I, 099° II), -2 e -3 (sulla carta: 048° in alto a destra, 167° in basso a destra, 301° in alto a sinistra, 249° in basso a sinistra), -8 (senso orario), -9, -10, -11 (cardinali e intercardinali). I nomi dei venti tornano in meteorologia (lezione 7) e nel Portolano. Bussola, declinazione e deviazione: lezione 4.')

# ============ STRUMENTI ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=''.join(line(30,y,1062,y,'#E4DCC8',2) for y in (160,300,440))+''.join(line(x,30,x,590,'#E4DCC8',2) for x in (260,520,780))
def tri(dx,dy,rot,op):
    arc=' '.join(f'M{330+150*math.cos(math.radians(a)):.1f} {540-150*math.sin(math.radians(a)):.1f} L{330+(150-(16 if a%30==0 else 8))*math.cos(math.radians(a)):.1f} {540-(150-(16 if a%30==0 else 8))*math.sin(math.radians(a)):.1f}' for a in range(0,181,10))
    return (f'<g transform="translate({dx} {dy}) rotate({rot} 330 425)"><path d="M100 540 L560 540 L330 310 Z" fill="#BFE6EA" fill-opacity="{op}" stroke="{SEA}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M180 540 A150 150 0 0 1 480 540" fill="none" stroke="{NAVY}" stroke-width="3"/><path d="{arc}" stroke="{NAVY}" stroke-width="2"/></g>')
b+=tri(-20,20,0,0.75)+tri(70,-120,-14,0.55)
b+=f'<path d="M846 120 L760 520 L770 522 L852 128 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/><path d="M854 120 L940 520 L930 522 L848 128 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<rect x="836" y="70" width="28" height="44" rx="8" fill="{NAVY}"/><circle cx="850" cy="124" r="14" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
b+=dash(765,540,935,540,CORAL,3)
b+=f'<g transform="rotate(-28 640 150)"><rect x="560" y="138" width="190" height="24" rx="4" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/><path d="M750 138 L786 150 L750 162 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><path d="M774 146 L786 150 L774 154 Z" fill="{NAVY}"/><rect x="530" y="138" width="30" height="24" rx="4" fill="{CORAL_T}" stroke="{NAVY}" stroke-width="3"/></g>'
lbl=lab(X+120,Y+556,420,'Squadrette nautiche',SEA,26,900)+lab(X+900,Y+190,160,'Compasso a punte secche',NAVY,24,900)+lab(X+470,Y+40,300,'Matita morbida e gomma',INK,24,900)
txt=term('Squadrette nautiche','Usate in coppia come parallele: tracciano e misurano rotte e rilevamenti.')+term('Compasso a punte secche','Misura distanze e riporta coordinate.')+term('Come si misura','Apri il compasso sul tratto e riporta l\'apertura sulla scala delle latitudini, alla stessa latitudine.')+term('Obbligatori','A bordo oltre le 12 miglia dalla costa.')
sec('strumenti', head('Il carteggio','Gli strumenti del carteggio')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Su una carta nautica: due squadrette nautiche con goniometro usate come parallele, un compasso a punte secche, una matita e una gomma')+lbl,
 notes='Quiz 1.7.5-18 (squadrette e parallele), -19 (compasso: distanze e coordinate), 1.7.2-30 (compasso a punte secche per non rovinare la carta), 1.7.5-33 e -52 (distanza sulla scala delle latitudini, alla stessa latitudine), 1.7.2-37 (misura della distanza), -71 (strumenti obbligatori oltre 12 miglia). Portare in aula squadrette e compasso: da qui in poi ogni lezione ha un po\' di carteggio.')

quiz_slide('quiz3','Quiz 3 · Orientarsi e misurare',['1.7.4-1','1.7.4-8','1.7.5-33'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.7.4-1','1.7.4-8','1.7.5-33'],True)

# ============ NAVIGAZIONE STIMATA ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<path d="M30 500 Q120 470 170 520 Q200 590 30 590 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
DR=[(200,480),(390,370),(580,260),(770,150)]; RL=[(200,480),(410,400),(620,320),(830,240)]
b+=f'<path d="M{DR[0][0]} {DR[0][1]} L{DR[-1][0]} {DR[-1][1]}" stroke="{NAVY}" stroke-width="5"/>'
b+=dpath('M'+' L'.join(f'{a} {b_}' for a,b_ in RL),SOFT,4)
for i,(x,y) in enumerate(DR[1:],1):
    r=22+i*24; b+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CORAL}" fill-opacity="0.1" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>'
for x,y in DR: b+=f'<circle cx="{x}" cy="{y}" r="11" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><circle cx="{x}" cy="{y}" r="3" fill="{NAVY}"/>'
b+=topboat(860,236,90,-21,'#FFFFFF',NAVY,3)
for yy in (420,480): b+=arrow(880,yy,990,yy+40,'#97A6B4',7,22)
lbl=lab(X+120,Y+500,240,'Partenza · 09:00',NAVY,24,800)+lab(X+290,Y+330,110,'10:00',NAVY,22,800)+lab(X+470,Y+210,110,'11:00',NAVY,22,800)+lab(X+400,Y+80,260,'12:00 · punto stimato',CORAL,24,900,'right')
lbl+=lab(X+850,Y+180,220,'posizione reale',SOFT,22,800)+lab(X+840,Y+540,220,'vento e corrente',SOFT,22,800)+lab(X+460,Y+400,240,'zona di incertezza',CORAL,22,800)
txt=term('Il punto stimato','Una posizione approssimata: si ricava da prora vera, velocità, punto di partenza e tempo trascorso.')+term('Gli strumenti','Bussola, solcometro e orologio. GPS e radar non danno un punto stimato.')+term('Perché si sbaglia','Scarroccio, deriva, declinazione, deviazione: l\'incertezza cresce col tempo.')
sec('stimata', head('Primi calcoli','La navigazione stimata')+col(txt+note('Insostituibile, ma da confermare con un punto nave.',CORAL,36)), pinned=svgp(X,Y,W,Hh,b,'Rotta stimata con i punti orari e cerchi di incertezza sempre più grandi; la posizione reale si allontana per effetto di vento e corrente')+lbl,
 notes='Quiz 1.7.5-9 e -28 (punto stimato), -30 (elementi: Pv, velocità, posizione iniziale, tempo), -23 (bussola, solcometro, orologio), -1 (GPS e radar non danno posizione stimata), -11 e -22 (cause di errore), -3 e -12 (zona di incertezza), -29 (insostituibile ma insufficiente), -36 (punto nave con almeno due luoghi di posizione: lezione 5), -2 e -10 (si risolve graficamente sulla carta di Mercatore).')

# ============ FORMULA ============
b=f'<path d="M280 40 L40 440 L520 440 Z" fill="{SUN_T}" stroke="{SUN}" stroke-width="10" stroke-linejoin="round"/>'+line(160,240,400,240,SUN,8)+line(280,240,280,440,SUN,8)
lbl=big(128+230,Y+110,100,'S',CORAL,120)+big(128+110,Y+300,120,'V',SEA,120)+big(128+330,Y+300,120,'T',PURPLE,120)+big(128+250,Y+320,60,'×',INK,70)
def chip2(t,c,u): return f'<div style="display:flex; align-items:center; gap:18px"><p style="font-family:{H}; font-size:44px; font-weight:700; color:#FFFFFF; background:{c}; padding:10px 28px; border-radius:40px; flex:none">{t}</p>{p(u,26,INK,700)}</div>'
mins=''.join(f'<div style="display:flex; flex-direction:column; align-items:center; background:#FFFFFF; {SHADOW}; padding:10px 14px; border-radius:18px"><p style="font-family:{H}; font-size:30px; font-weight:700; color:{INK}">{a}</p><p style="font-size:22px; font-weight:800; color:{SEA}">{b_} h</p></div>' for a,b_ in [('6′','0,1'),('12′','0,2'),('15′','0,25'),('18′','0,3'),('20′','0,33'),('30′','0,5'),('45′','0,75')])
right=(chip2('S = V × T',CORAL,'spazio in <b>miglia</b>')+chip2('V = S ÷ T',SEA,'velocità in <b>nodi</b> (miglia all\'ora)')+chip2('T = S ÷ V',PURPLE,'tempo in <b>ore e decimi</b>')
       +p('<b>Minuti in ore:</b> dividi per 60. <b>Decimi in minuti:</b> moltiplica per 60 (0,4 h = 24′).',26,INK)+f'<div style="display:flex; gap:12px">{mins}</div>')
sec('formula', head('Primi calcoli','Spazio, velocità, tempo')+f'<div style="margin-left:640px; display:flex; flex-direction:column; gap:22px">{right}</div>', pinned=svgp(128,Y,560,480,b,'Il triangolo S sopra, V e T sotto: coprendo una lettera restano le altre due')+lbl+note('Copri la lettera che cerchi!',CORAL,40).replace('<p style="','<p style="position:absolute; left:160px; top:790px; width:500px; ',1),
 notes='Quiz 1.7.5-13, -14, -25, -51 (nodo = un miglio all\'ora), -15, -16, -17 (le tre formule), -26 (miglio per le distanze), -35 (ricalcolare a ogni cambio di velocità), -54 (4,4 h = 4 h 24′). Il triangolo è un aiuto per la memoria: coprendo S restano V × T, coprendo V resta S ÷ T, coprendo T resta S ÷ V.')

# ============ ESEMPI ============
def ex(qid,prob,steps,res,c,bg):
    st=''.join(p(s,24,BODY) for s in steps)
    return card(note(f'Quiz {qid}',c,34)+p(prob,27,INK,800,1.3)+f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:22px">{st}</div>'+f'<p style="font-family:{H}; font-size:52px; font-weight:700; color:{c}">{res}</p>',None,28,14)
e1=ex('1.7.5-31','15 nodi per 45 minuti: quante miglia?',['45′ ÷ 60 = <b>0,75 h</b>','S = 15 × 0,75'],'11,25 miglia',CORAL,CORAL_T)
e2=ex('1.7.5-65','18 miglia a 7 nodi: quanto tempo?',['T = 18 ÷ 7 = <b>2,57 h</b>','0,57 × 60 ≈ <b>34′</b>'],'2 h 34′',SEA,SEA_T)
e3=ex('1.7.5-63','24,5 miglia in 3 h 30′: che velocità?',['3 h 30′ = <b>3,5 h</b>','V = 24,5 ÷ 3,5'],'7 nodi',PURPLE,LILAC_T)
sec('esempi', head('Primi calcoli','Tre esempi svolti')+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}</div>'+note('Prima trasforma il tempo in ore e decimi, poi applica la formula.',BLUE,38),
 notes='Esempi dai quiz ufficiali: 1.7.5-31 (15 kn, 45′ → 11,25 mg), -65 (18 mg, 7 kn → 2 h 34′), -63 (3 h 30′, 24,5 mg → 7 kn; attenzione, nell\'elenco il numero 1.7.5-63 compare due volte). Altri da fare alla lavagna: -39 (9 kn, 45′ → 6,75), -41, -44 (19 kn, 9′ → 2,85), -57 (11,6 mg a 6 kn → 1 h 56′), -60 (6 kn, 2 h 45′ → 16,5), -64 (2 h 20′ a 12 kn → 28 mg).')

# ============ CARBURANTE SULLA CARTA ============
b=f'<rect x="0" y="0" width="440" height="300" fill="{CHART}"/>'
b+=f'<path d="M0 0 L180 0 Q150 60 90 80 Q40 110 0 100 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/><path d="M300 300 Q320 230 400 220 Q440 222 440 240 L440 300 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=line(90,130,360,200,NAVY,5)+f'<circle cx="90" cy="130" r="11" fill="{CORAL}"/><circle cx="360" cy="200" r="11" fill="{SEA}"/>'
b+=f'<path d="M216 40 L96 118 L104 122 L220 48 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="2"/><path d="M224 40 L356 186 L348 190 L218 48 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="2"/><circle cx="220" cy="42" r="10" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
b+=f'<g transform="translate(40 190)"><rect x="0" y="12" width="70" height="86" rx="10" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><rect x="40" y="0" width="20" height="16" rx="3" fill="{NAVY}"/><path d="M12 30 L58 80 M58 30 L12 80" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="6"/></g>'
def chip(t,c): return f'<p style="font-family:{H}; font-size:32px; font-weight:700; color:#FFFFFF; background:{c}; padding:12px 22px; border-radius:40px">{t}</p>'
op=lambda t: f'<p style="font-family:{H}; font-size:40px; font-weight:700; color:{INK}">{t}</p>'
formula=f'<div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap">{chip("1 · miglia col compasso",BLUE)}{op("→")}{chip("2 · T = S ÷ V",SEA)}{op("→")}{chip("3 · litri = l/h × T",PURPLE)}{op("+")}{chip("4 · 30% di riserva",CORAL)}</div>'
boxes=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:24px">{p(a,22,SOFT,800)}<p style="font-family:{H}; font-size:44px; font-weight:700; color:{INK}">{b_}</p>{p(c,22)}</div>' for a,b_,c,bg in [('1 · da A a B','9 miglia','sulla scala delle latitudini',BLUE_T),('2 · tempo','1,5 h','9 ÷ 6 nodi',SEA_T),('3 · consumo','6 litri','4 l/h × 1,5',LILAC_T),('4 · con riserva','≈ 8 litri','6 + 30% = 7,8',CORAL_T)])
exm=card(note('Esempio · 6 nodi, motore da 4 l/h',CORAL,36)+f'<div style="display:flex; gap:14px">{boxes}</div>',None,28,14)
sec('carburante', head('Primi calcoli · verso il carteggio','Il carburante sulla carta')+formula+f'<div style="display:flex; gap:24px; align-items:stretch">{svgi(440,300,b,"Mini carta: rotta da A a B misurata con il compasso e una tanica di carburante",dw=440,dh=300)}{exm}</div>'
 +p('All\'esame di carteggio la soluzione è un intervallo: per l\'esercizio 5.1.2-3 (consumo 4 l/h) la risposta ufficiale è «13÷15 litri».',26,INK),
 notes='Anticipo della lezione 11 (23 esercizi di carburante, famiglie 5.x.2). Stessa regola dei quiz di motori (1.2.3-1: riserva del 30%). Nel carteggio le miglia si misurano sulla carta tra punti noti o calcolati; il tempo si ricava con T = S ÷ V. Tolleranza: le risposte ufficiali danno un intervallo, per es. 5.1.2-1 «29÷31 litri», 5.1.2-2 «19÷21 litri».')

quiz_slide('quiz4','Quiz 4 · S = V × T',['1.7.5-27','1.7.5-56','1.7.5-62'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.7.5-27','1.7.5-56','1.7.5-62'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.4.4-6','1.7.1-34','1.7.2-48'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.4.4-6','1.7.1-34','1.7.2-48'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.7.8-4','1.7.5-54','1.7.5-39'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.7.8-4','1.7.5-54','1.7.5-39'],True)
closing(['Spring contro i movimenti avanti e indietro, traversini contro lo scostamento dalla banchina','Latitudine 0-90° N/S, longitudine 0-180° E/W; 1′ di latitudine = 1 miglio = 1852 m','Mercatore: isogona, lossodromia retta, distanze sulla scala delle latitudini alla stessa latitudine','Scala più grande = denominatore più piccolo','S = V × T con il tempo in ore e decimi; carburante + 30%'],
 'Prossima lezione · 04 · Ancoraggio, prora e rotta','A casa: i 49 quiz di ormeggio, i 45 sulle coordinate, i 56 sulle carte e i calcoli di navigazione stimata (1.7.5).')
write_deck(OUT,'Lezione 03 · Ormeggi, carte e primi calcoli',
 ['cover','agenda','attracco','cavi','poppa','boe','nodi','porto','quiz1','quiz1r','coordinate','leggere','mercatore','scale','simboli','pubblicazioni','quiz2','quiz2r',
  'rosa','strumenti','quiz3','quiz3r','stimata','formula','esempi','carburante','quiz4','quiz4r','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Ormeggi: banchina, cavi, poppa, boe, nodi, porto e rada","start":"attracco"},
  "s3":{"description":"Cartografia: coordinate, Mercatore, scale, simboli, pubblicazioni","start":"coordinate"},"s4":{"description":"Rosa dei venti e strumenti del carteggio","start":"rosa"},
  "s5":{"description":"Navigazione stimata, S = V × T, carburante e verifica finale","start":"stimata"}})
