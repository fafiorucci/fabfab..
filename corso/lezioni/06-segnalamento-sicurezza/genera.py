import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez06/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; GREY='#97A6B4'; NIGHT='#0F2238'
LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'; MBLACK='#1B2330'; MYEL='#F2C230'; ORANGE='#F28C28'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Fari e fanali: fin dove si vedono':'lighthouse','Riconoscere un faro':'lighthouse',
 'Entrare in porto: i segnali laterali':'flag','I segnali cardinali':'compass','Pericolo isolato, acque sicure, speciali':'flag',
 'I segnali sonori di manovra':'wind','Nella nebbia':'cloud','Entrare e uscire dal porto':'anchor',
 'Le dotazioni: salvarsi':'lifebuoy','Le dotazioni: navigare e comunicare':'compass','Chiedere soccorso':'flag',
 'Il triangolo del fuoco':'fuel','Classi di incendio ed estintori':'fuel'})
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def glow(x,y,c,r=9):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.6:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.6:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
def tower(x,y,s=1):
    g=f'<path d="M{x-14*s} {y} L{x-8*s} {y-90*s} L{x+8*s} {y-90*s} L{x+14*s} {y} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/><rect x="{x-9*s}" y="{y-66*s}" width="{18*s}" height="{12*s}" fill="{CORAL}"/><rect x="{x-11*s}" y="{y-34*s}" width="{22*s}" height="{12*s}" fill="{CORAL}"/>'
    return g+f'<rect x="{x-11*s}" y="{y-110*s}" width="{22*s}" height="{20*s}" rx="{4*s}" fill="{SUN}" stroke="{NAVY}" stroke-width="{2.5*s}"/>'
X,Y,W,Hh=700,290,1092,620

# ---- segnali IALA in elevazione ----
def cone(x,y,up,s=22,c=MBLACK):
    return f'<path d="M{x-s*0.6:.0f} {y+s/2:.0f} L{x+s*0.6:.0f} {y+s/2:.0f} L{x} {y-s/2:.0f} Z" fill="{c}"/>' if up else f'<path d="M{x-s*0.6:.0f} {y-s/2:.0f} L{x+s*0.6:.0f} {y-s/2:.0f} L{x} {y+s/2:.0f} Z" fill="{c}"/>'
def mark(x,y,bands,top,s=1):
    """bands: lista colori dall'alto; top: lista di (tipo,param)"""
    h=90*s; w=40*s; bh=h/len(bands); g=''
    g+=f'<ellipse cx="{x}" cy="{y}" rx="{w*0.9:.0f}" ry="{8*s:.0f}" fill="{WATER}" fill-opacity="0.35"/>'
    for i,c in enumerate(bands): g+=f'<rect x="{x-w/2:.0f}" y="{y-h+i*bh:.0f}" width="{w:.0f}" height="{bh+0.5:.0f}" fill="{c}"/>'
    g+=f'<rect x="{x-w/2:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="none" stroke="{NAVY}" stroke-width="2"/><path d="M{x} {y-h:.0f} V{y-h-30*s:.0f}" stroke="{NAVY}" stroke-width="{3*s}"/>'
    ty=y-h-44*s
    for kind,par in top:
        if kind=='cone': g+=cone(x,ty,par,22*s); ty-=26*s
        elif kind=='ball': g+=f'<circle cx="{x}" cy="{ty:.0f}" r="{11*s:.0f}" fill="{par}"/>'; ty-=26*s
        elif kind=='x': g+=f'<path d="M{x-11*s:.0f} {ty-11*s:.0f} L{x+11*s:.0f} {ty+11*s:.0f} M{x+11*s:.0f} {ty-11*s:.0f} L{x-11*s:.0f} {ty+11*s:.0f}" stroke="{MYEL}" stroke-width="{6*s:.0f}" stroke-linecap="round"/>'
    return g
CARD={'N':([MBLACK,MYEL],[('cone',True),('cone',True)]),'E':([MBLACK,MYEL,MBLACK],[('cone',False),('cone',True)]),
      'S':([MYEL,MBLACK],[('cone',False),('cone',False)]),'W':([MYEL,MBLACK,MYEL],[('cone',True),('cone',False)])}

# ============ COVER + AGENDA ============
cover(6,'Segnalamento, segnali sonori e sicurezza','Fari e boe IALA, fischi e nebbia, porti; le dotazioni del DM 133/2024 e come si spegne un incendio',
 'Lezione 6. Capitoli del programma della scuola: Cartografia e segnalamento (fari, IALA), Segnali sonori, Sicurezza parte 1 (dotazioni, mezzi di soccorso, incendio). Aggiunte dall\'All. A: dotazioni obbligatorie secondo il DM 133/2024 (punto 3b) e precauzioni all\'ingresso e all\'uscita dei porti (punto 4a). Emergenze, VHF e tempo cattivo nella lezione 9.')
blocks=[('0:00','30′','Fari e segnali IALA · quiz 1',CORAL),('0:30','25′','Segnali sonori, nebbia e porti · quiz 2',SEA),('0:55','25′','Dotazioni DM 133/2024 · quiz 3',PURPLE),('1:20','25′','Incendio ed estintori · quiz 4',BLUE),('1:45','15′','Verifica finale',CORAL)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">2 + 3</p>'+p('domande su 20: COLREG e segnalamento, Sicurezza',26,INK,700)+p('Più la manovra in porto, che rientra nelle 4 domande di Manovra e condotta.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>riconoscere un faro dalla sua caratteristica</li><li>leggere i segnali IALA laterali e cardinali</li><li>capire e usare i segnali sonori</li><li>preparare la barca con le dotazioni giuste</li><li>scegliere l\'estintore adatto</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 06 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie da 3 quiz e una finale da 6, tutti ufficiali (DD 131/2022). Banca: fanali luminosi e sistema IALA 120 quiz (1.5.3), prevenire gli abbordi 60 (1.5.2, per i segnali sonori), porti 21 (1.4.1), incendio ed estintori 31 (1.3.1), dotazioni di sicurezza 48 (1.3.3, 14 oscurati). Attenzione: il DM 133/2024 ha riscritto l\'Allegato V del DM 146/2008; dove un quiz non oscurato diverge, all\'esame vale la risposta dell\'elenco ministeriale.')

# ============ FARI: PORTATA ============
k=230/546**2
yc=lambda x: 380+k*(x-546)**2
tx=700; ty=yc(tx); m=2*k*(tx-546); L0=(120,ty+m*(120-tx))
ex=950; ey=ty+m*(ex-tx)
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EAF4F7"/>'
b+='<path d="M0 '+f'{yc(0):.0f}'+' '+' '.join(f'L{x} {yc(x):.1f}' for x in range(0,1093,26))+' L1092 620 L0 620 Z" fill="'+WATER+'" fill-opacity="0.4"/>'
b+=f'<path d="M40 {yc(40)+4:.0f} L40 {L0[1]+60} L200 {L0[1]+60} L220 {yc(220)+4:.0f} Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'+tower(120,L0[1]+62,0.8)
b+=dash(L0[0],L0[1],ex,ey,SUN,4)+glow(L0[0],L0[1],SUN,8)+f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="7" fill="{CORAL}"/>'
b+=profile(ex-70,yc(ex)+2,150,sup=True)+line(ex,yc(ex)-20,ex,ey,NAVY,4)+f'<circle cx="{ex}" cy="{ey:.0f}" r="8" fill="{NAVY}"/>'
lbl=lab(X+tx-120,Y+ty+24,240,'orizzonte',CORAL,24,900,'center')+lab(X+ex-100,Y+ey-60,200,'occhio',NAVY,24,900,'center')+lab(X+260,Y+60,420,'la luce passa radente alla curvatura',SUN,24,900)+lab(X+60,Y+int(L0[1])-100,200,'faro',NAVY,24,900)
txt=term('Faro e fanale','Si distinguono per la portata: i fari servono a riconoscere la costa, i fanali segnalano porti, moli e pericoli.')+term('Portata luminosa e nominale','Quanto lontano arriva la luce: dipende da intensità, visibilità dell\'aria e occhio. La nominale è quella con visibilità di 10 miglia: è quella scritta sulla carta.')+term('Portata geografica','Dipende dalla curvatura della Terra, dall\'altezza della luce e da quella dell\'occhio.')
sec('fari', head('Segnalamento · le portate','Fari e fanali: fin dove si vedono')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Faro su un promontorio: la luce passa radente alla curvatura del mare e raggiunge l\'occhio di chi sta sulla barca lontana, sopra l\'orizzonte')+lbl,
 notes='Quiz 1.5.3-29, -57, -61 (fari e fanali: la portata nominale li distingue), -1, -30, -39, -86 (portata luminosa), -2, -31, -63, -87 (portata nominale: atmosfera con visibilità meteorologica di 10 miglia), -79 (sulla carta è indicata la nominale), -3, -28, -88 (portata geografica: curvatura, altezza della luce, elevazione dell\'occhio).')

# ============ CARATTERISTICA ============
X=128
rows=[('F · fissa',[(0,12,LWHITE)]),('Lam · lampi',[(t,t+0.4,LWHITE) for t in (0,3,6,9)]),('Lam (2) · 2 lampi',[(t,t+0.4,LWHITE) for t0 in (0,6) for t in (t0,t0+1.2)]),
      ('Int · intermittente',[(t,t+2.2,LWHITE) for t in (0,3,6,9)]),('Iso · isofase',[(t,t+1.5,LWHITE) for t in (0,3,6,9)]),('Sc · scintillante',[(t/1.0,t/1.0+0.5,LWHITE) for t in range(12)]),
      ('Alt b.r.',[(t,t+1.5,LWHITE if i%2==0 else LRED) for i,t in enumerate((0,1.5,3,4.5,6,7.5,9,10.5))])]
x0,x1=300,1060; sx=(x1-x0)/12
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EAF4F7"/>'
for i,(nm,seg) in enumerate(rows):
    y=40+i*78; b+=f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="44" rx="8" fill="{NIGHT}"/>'
    b+=''.join(f'<rect x="{x0+a*sx:.0f}" y="{y+6}" width="{max(6,(e-a)*sx):.0f}" height="32" rx="6" fill="{c}"/>' for a,e,c in seg)
b+=f'<path d="M{x0} 590 H{x0+6*sx:.0f}" stroke="{CORAL}" stroke-width="4"/><path d="M{x0} 580 V600 M{x0+6*sx:.0f} 580 V600" stroke="{CORAL}" stroke-width="4"/>'
lbl=''.join(lab(X+20,Y+48+i*78,270,nm,NAVY,24,900) for i,(nm,_) in enumerate(rows))+lab(X+x0+20,Y+550,420,'periodo di Lam (2): 6 secondi',CORAL,22,900)
txt=term('La caratteristica','Tipo di luce, colore e periodo: di notte un faro si riconosce così.')+term('Il periodo','Il tempo in cui si ripete la sequenza di luci ed eclissi.')+term('Come si legge','«Lam (2) 12s 27m 20M»: 2 lampi ogni 12 secondi, luce a 27 m sul mare, portata 20 miglia. In inglese: Fl (2).')+term('Settore rosso','Si naviga, ma attenzione: segnala un pericolo.')
sec('caratteristica', head('Segnalamento · le luci','Riconoscere un faro'), pinned=svgp(X,Y,W,Hh,b,'Sette strisce notturne che mostrano nel tempo luce fissa, lampi, gruppi di due lampi, intermittente, isofase, scintillante e alternata bianca e rossa')+lbl+pcol(txt,532,20),
 notes='Quiz 1.5.3-56 e -77 (caratteristica), -47, -80, -81 (periodo: somma di luci ed eclissi, es. 0,5+1+0,5+2 = 4 s), -41, -48, -35, -34, -37, -45, -68 (lettura delle sigle), -7 e -92 (Sc = scintillante), -9 e -94 (Int = intermittente, a gruppi di eclissi), -38 (Iso: luce uguale all\'eclisse), -8, -75, -76, -93 (luce alternata), -85 (settore rosso), -60 (settori colorati), -78 (settore di visibilità in figura), -4 oscurato (fase). Il quiz 1.5.3-37 traduce Oc con «intermittente».')
X=700

# ============ LATERALI ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
b+=f'<path d="M0 0 L420 0 L420 170 L390 170 L390 40 L0 40 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/><path d="M1092 0 L672 0 L672 170 L702 170 L702 40 L1092 40 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<rect x="385" y="150" width="40" height="40" rx="6" fill="{LRED}" stroke="{NAVY}" stroke-width="3"/><rect x="667" y="150" width="40" height="40" rx="6" fill="{LGREEN}" stroke="{NAVY}" stroke-width="3"/>'
b+=glow(405,140,LRED,7)+glow(687,140,LGREEN,7)
def can(x,y): return f'<rect x="{x-16}" y="{y-44}" width="32" height="40" rx="3" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/><rect x="{x-11}" y="{y-66}" width="22" height="18" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/>'
def cn(x,y): return f'<path d="M{x-18} {y-4} L{x+18} {y-4} L{x} {y-50} Z" fill="{LGREEN}" stroke="{NAVY}" stroke-width="2"/><path d="M{x-11} {y-54} L{x+11} {y-54} L{x} {y-76} Z" fill="{LGREEN}" stroke="{NAVY}" stroke-width="2"/>'
for yy in (330,480): b+=can(420,yy)+cn(672,yy)
b+=topboat(546,500,130,-90,'#FFFFFF',NAVY,4)+dpath('M546 430 L546 220',CORAL,5)+head_at(546,214,-90,CORAL)
lbl=lab(X+110,Y+300,280,'rosso a sinistra: cilindro',LRED,24,900,'right')+lab(X+710,Y+300,280,'verde a dritta: cono',LGREEN,24,900)+lab(X+390,Y+580,320,'entrando in porto',NAVY,24,900,'center')
txt=term('Regione A','In Europa: entrando in porto o risalendo un canale, il rosso sta a sinistra e il verde a dritta.')+term('Forme','A sinistra cilindri rossi; a dritta coni verdi, con la punta in alto.')+term('Di notte','I fanali del porto ripetono i colori: rosso sul molo di sinistra, verde su quello di dritta.')
sec('laterali', head('Segnalamento · sistema AISM-IALA','Entrare in porto: i segnali laterali')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto di una barca che entra in porto: boe rosse cilindriche a sinistra, boe verdi coniche a dritta, fanale rosso sul molo di sinistra e verde su quello di dritta')+lbl,
 notes='Quiz 1.5.3-32 (in Italia Sistema A, rosso a sinistra), -27 (segnale laterale), -43 (a sinistra entrando: rosso, cilindrico), -110 e -111 (figure), -44 (forma e colore del corpo o del miraglio), -49 (tipi di segnali IALA), -46 (regioni A e B differiscono solo nei laterali), 1.4.1-8 e -13 (imboccatura del porto: rosso a sinistra, verde a dritta). Navigazione fluviale: quiz 1.5.3-112…-120, da leggere sul manuale.')

# ============ CARDINALI ============
X=128
cx,cy=546,330
cx,cy=546,330
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/><circle cx="{cx}" cy="{cy}" r="180" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
b+=f'<path d="M{cx-50} {cy+20} Q{cx-40} {cy-30} {cx} {cy-26} Q{cx+50} {cy-40} {cx+56} {cy+14} Q{cx+10} {cy+36} {cx-50} {cy+20} Z" fill="#7A6A55" stroke="{NAVY}" stroke-width="3"/>'
pos={'N':(546,230),'E':(866,470),'S':(546,610),'W':(226,470)}
for kk,(px,py) in pos.items():
    bands,top=CARD[kk]; b+=mark(px,py,bands,top,1.05)
lbl=lab(X+590,Y+120,300,'N · luce continua',NAVY,24,900)+lab(X+910,Y+360,170,'E · 3 lampi',NAVY,24,900)+lab(X+590,Y+520,300,'S · 6 + 1 lungo',NAVY,24,900)+lab(X+30,Y+360,150,'W · 9 lampi',NAVY,24,900,'right')+lab(X+466,Y+366,160,'pericolo',INK,24,900,'center')
txt=term('Cosa dicono','Il lato su cui passare: si passa a Nord della cardinale Nord, perché il pericolo è a Sud.')+term('Colori e miragli','Nero e giallo. I due coni puntano verso le bande nere: in alto il Nord, in basso il Sud, base contro base l\'Est, punta contro punta l\'Ovest.')+term('Di notte','Luce bianca scintillante, come un orologio: 3 lampi Est, 6 Sud, 9 Ovest, continua Nord.')
sec('cardinali', head('Segnalamento · sistema AISM-IALA','I segnali cardinali'), pinned=svgp(X,Y,W,Hh,b,'Uno scoglio al centro e le quattro boe cardinali attorno: Nord nera sopra e gialla sotto con coni in alto; Est nera, gialla, nera con coni base contro base; Sud gialla sopra e nera sotto con coni in basso; Ovest gialla, nera, gialla con coni punta contro punta')+lbl+pcol(txt),
 notes='Quiz 1.5.3-36, -67 (cosa indicano), -51 (legati alla bussola, nero e giallo), -66 e -70 (miraglio Nord: vertici in alto; Sud: vertici in basso), -69 e -72 (Est: basi unite, passare a est), -71 e -73 (Ovest: vertici uniti, passare a ovest), -82, -83, -84 (9 scintillii: pericolo a est, passare a ovest; 3: passare a est; 6: passare a sud), -33, -52, -54, -55, -97, -103…-109 (figure).')
X=700

# ============ ALTRI SEGNALI ============
def scene(inner,light):
    return f'<rect x="0" y="0" width="300" height="220" fill="#EAF4F7"/><rect x="0" y="180" width="300" height="40" fill="{WATER}" fill-opacity="0.35"/>{inner}<rect x="210" y="20" width="76" height="76" rx="14" fill="{NIGHT}"/>{light}'
iso=scene(mark(120,190,[MBLACK,LRED,MBLACK],[('ball',MBLACK),('ball',MBLACK)],1.1),glow(248,58,LWHITE,7))
def sw():
    g=f'<ellipse cx="120" cy="190" rx="36" ry="8" fill="{WATER}" fill-opacity="0.35"/>'
    for i in range(4): g+=f'<rect x="{100+i*10}" y="91" width="10" height="99" fill="{LRED if i%2==0 else "#FFFFFF"}"/>'
    g+=f'<rect x="100" y="91" width="40" height="99" fill="none" stroke="{NAVY}" stroke-width="2"/><path d="M120 91 V58" stroke="{NAVY}" stroke-width="3"/><circle cx="120" cy="44" r="12" fill="{LRED}"/>'
    return g
safe=scene(sw(),glow(248,58,LWHITE,7))
spec=scene(mark(120,190,[MYEL],[('x',0)],1.1),glow(248,58,LYEL,7))
AS=[(iso,'Pericolo isolato','Nero con bande rosse, due sfere nere. Luce bianca a gruppi di 2 lampi. Il pericolo è piccolo: gli si passa attorno.'),
    (safe,'Acque sicure','Strisce verticali rosse e bianche, una sfera rossa. Luce bianca isofase, intermittente o a lampo lungo. Acqua navigabile tutto intorno.'),
    (spec,'Speciale','Giallo, con la croce gialla a X. Luce gialla. Zone particolari: cavi, condotte, esercitazioni, balneazione.')]
cc=''.join(card(svgi(300,220,s,f'Segnale di {t.lower()} di giorno e la sua luce di notte',dw=330,dh=242)+h3(t,30)+p(d,24),None,24,10) for s,t,d in AS)
sec('altri', head('Segnalamento · sistema AISM-IALA','Pericolo isolato, acque sicure, speciali')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 1.5.3-15, -40, -50, -74 (pericolo isolato: nero con bande rosse), -64 (luce bianca a lampi, gruppi di 2), -59, -65, -99 (acque sicure: luce bianca isofase, intermittente o a lampo lungo; sfera rossa), -12, -42, -53, -100, -101, -102 (speciali: gialli, X gialla, luce gialla), -5, -6, -90, -91 (boe luminose), -62 (meda), -58 (gavitelli), -10 e -95 (riflettore radar).')

quiz_slide('quiz1','Quiz 1 · Fari e segnali',['1.5.3-32','1.5.3-82','1.5.3-50'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.5.3-32','1.5.3-82','1.5.3-50'],True)

# ============ SEGNALI SONORI ============
def snd(seq):
    g=f'<rect x="0" y="0" width="260" height="60" rx="14" fill="{NIGHT}"/>'; x=18
    for s_ in seq:
        wdt=26 if s_=='.' else 80; g+=f'<rect x="{x}" y="20" width="{wdt}" height="20" rx="10" fill="{SUN}"/>'; x+=wdt+12
    return g
SS=[('.','Accosto a dritta',SEA),('..','Accosto a sinistra',SEA),('...','Macchine indietro',SEA),('--.','Voglio sorpassarti a dritta',PURPLE),('--..','Voglio sorpassarti a sinistra',PURPLE),('-','Curva cieca o uscita dal porto senza visibilità',CORAL),('.....','Non capisco le tue intenzioni: attenzione!',CORAL)]
cells=''.join(f'<div style="display:flex; gap:18px; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 18px; border-radius:20px; border-left:10px solid {c}">{svgi(260,60,snd(sq),"Sequenza di suoni",dw=260,dh=60,pan=False)}{p(t,26,INK,800,1.25)}</div>' for sq,t,c in SS)
legend=f'<div style="display:flex; gap:28px; align-items:center">{svgi(260,60,snd("."),"Suono breve",dw=130,dh=30,pan=False)}{p("breve: circa 1 secondo",24,INK,700)}{svgi(260,60,snd("-"),"Suono prolungato",dw=130,dh=30,pan=False)}{p("prolungato: da 4 a 6 secondi",24,INK,700)}</div>'
sec('sonori', head('COLREG · con il fischio','I segnali sonori di manovra')+legend+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px">{cells}</div>', gap=24,
 notes='Quiz 1.5.2-21 e -49 (1 breve = accosto a dritta), -23 e -28 (2 brevi = a sinistra), -22, -37, -48, -50 (sorpasso: 2 prolungati + 1 breve a dritta, + 2 brevi a sinistra), 1.4.1-15 e 1.5.3-116 (1 prolungato uscendo dal porto o in una curva cieca). I 3 brevi (macchine indietro) e i 5 brevi (dubbio) sono della regola 34 del COLREG. Apparecchi sonori: 1.5.2-13 e -51 (sotto i 12 m qualsiasi mezzo sonoro efficace), DM 133/2024 (fischio e campana per le unità oltre 12 m).')

# ============ NEBBIA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#DDE6EC"/><path d="M0 470 Q273 456 546 470 T1092 466 L1092 620 L0 620 Z" fill="{WATER}" fill-opacity="0.35"/>'
b+=profile(330,474,420,sup=True)
b+=''.join(f'<path d="M{700+r*0.2:.0f} {380-r:.0f} A{r} {r} 0 0 1 {700+r*0.2:.0f} {380+r*0.6:.0f}" fill="none" stroke="{SUN}" stroke-width="6" stroke-linecap="round" opacity="{1-r/260:.2f}"/>' for r in (60,110,160,210))
b+=''.join(f'<rect x="0" y="{y}" width="1092" height="{h}" fill="#FFFFFF" fill-opacity="0.45"/>' for y,h in ((60,60),(200,50),(390,70)))
lbl=lab(X+60,Y+40,400,'ogni 2 minuti al massimo',NAVY,26,900)
FG=[('-','A motore, con abbrivio'),('--','A motore, ferma senza abbrivio'),('-..','A vela'),]
fg=''.join(f'<div style="display:flex; gap:16px; align-items:center">{svgi(260,60,snd(sq),"Segnale da nebbia",dw=200,dh=46,pan=False)}{p(t,25,INK,800,1.25)}</div>' for sq,t in FG)
txt=fg+term('Alla fonda','Oltre i 20 m: rapidi colpi di campana per 5 secondi, almeno ogni minuto.')+term('Visibilità ridotta','Nebbia, pioggia, neve, fumo: velocità di sicurezza e fanali accesi.')
sec('nebbia', head('COLREG · visibilità ridotta','Nella nebbia')+col(txt,560,18), pinned=svgp(X,Y,W,Hh,b,'Barca nella nebbia che emette segnali sonori, con banchi di nebbia sul mare')+lbl,
 notes='Quiz 1.5.2-20 e -53 (motore con abbrivio: 1 prolungato ogni 2 minuti al massimo), -40 (motore fermo senza abbrivio: 2 prolungati), -52 (vela: 1 prolungato e 2 brevi), -35 (fonda oltre 20 m: campana per 5 secondi ogni minuto), -3 (visibilità ridotta), -10 (velocità di sicurezza), -12 (fanali accesi con visibilità ridotta), -14 (segnale di pericolo: suono continuo). Il quiz 1.5.2-36 sulla campana è oscurato.')

# ============ PORTO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
b+=f'<path d="M0 0 L1092 0 L1092 80 L0 80 Z" fill="{LAND}"/><path d="M180 80 L180 300 L460 300 L460 260 L220 260 L220 80 Z" fill="#C9C2B2" stroke="{NAVY}" stroke-width="3"/><path d="M900 80 L900 300 L632 300 L632 260 L860 260 L860 80 Z" fill="#C9C2B2" stroke="{NAVY}" stroke-width="3"/>'
b+=glow(460,280,LRED,8)+glow(632,280,LGREEN,8)
b+=topboat(546,200,110,90,'#FFFFFF',NAVY,4)+dpath('M546 260 L546 330',SEA,4)
b+=topboat(700,500,110,-100,'#FFFFFF',NAVY,4)
b+=f'<path d="M100 620 A480 420 0 0 1 992 620" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="12 8"/>'
lbl=lab(X+290,Y+310,160,'rosso',LRED,24,900,'right')+lab(X+650,Y+310,160,'verde',LGREEN,24,900)+lab(X+620,Y+110,220,'B esce: ha la precedenza',SEA,24,900)+lab(X+760,Y+470,260,'A entra: aspetta',NAVY,24,900)+lab(X+40,Y+420,300,'da qui, 500 m: rallenta',CORAL,24,900)
txt=term('Chi esce ha la precedenza','Di norma, salvo le ordinanze locali. Si lascia manovrare anche le navi grandi.')+term('Rallenta','Riduci la velocità a 500 m dall\'ingresso e non entrare a vela, salvo ordinanze locali.')+term('Nel canale','Tieniti sulla dritta. Uscendo senza visibilità: un suono prolungato e ascolta.')+term('Porto commerciale','Senza servizi per il diporto: avvisa l\'Autorità marittima.')
sec('porto', head('Condotta · i porti','Entrare e uscire dal porto'), pinned=svgp(X,Y,W,Hh,b,'Imboccatura di un porto vista dall\'alto: fanale rosso a sinistra e verde a dritta, la barca B che esce ha la precedenza, la barca A che entra aspetta fuori; arco dei 500 metri')+lbl+pcol(txt,532,20),
 notes='Quiz 1.4.1-4, -9, -17 (precedenza a chi esce; chi transita nei 500 m davanti all\'ingresso cede a chi entra ed esce), -6 (navi grandi), -10 (ridurre a 500 m), -12 (non si entra a vela), -19 (nel canale tenersi a dritta), -3 (porti con obbligo di tenere la dritta: ordinanze), -5 (porto commerciale: avvisare l\'Autorità marittima), -7, -8, -13, -14 (fanali dell\'imboccatura), -15 (1 prolungato uscendo), -16 (danni da moto ondoso), -20 (ormeggi in transito 72 ore), -21 (ormeggi per persone con disabilità), -1 (sanzione da 414 a 2.066 euro), -18 (ordinanze). I quiz -2 e -11 (3 nodi) sono oscurati: il limite lo fissa l\'ordinanza del porto.')
X=700

quiz_slide('quiz2','Quiz 2 · Suoni e porti',['1.5.2-21','1.4.1-13','1.5.2-52'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.5.2-21','1.4.1-13','1.5.2-52'],True)

# ============ DOTAZIONI (tabelle) ============
COLS=['oltre 50','entro 50','entro 12','entro 6','entro 3','entro 1','300 m']
def table(rows,notes_col=None):
    th=''.join(f'<th style="width:9%; text-align:center; color:#FFFFFF">{c}</th>' for c in COLS)
    h=f'<tr style="background:{NAVY}"><th style="width:37%; color:#FFFFFF">Dotazione (miglia dalla costa)</th>'+th+'</tr>'
    body=''
    for k,(name,vals) in enumerate(rows):
        bg=f' style="background:{PAPER if k%2 else "#FFFFFF"}"'
        body+=f'<tr{bg}><td style="font-weight:700; color:{INK}{"; padding:8px 12px" if k==0 else ""}">{name}</td>'+''.join(f'<td style="text-align:center; font-weight:800; color:{SEA if v=="●" else CORAL}">{v}</td>' for v in vals)+'</tr>'
    return f'<table style="font-size:24px; color:{BODY}">{h}{body}</table>'
o='●'; n=''
T1=[('Zattera di salvataggio (tutti a bordo)',[o,o,n,n,n,n,n]),('Zattera costiera',[n,n,o,n,n,n,n]),
    ('Giubbotti 150 N con luce automatica',[o,o,o,n,n,n,n]),('Giubbotti 100 N',[n,n,n,o,o,o,n]),
    ('Salvagente anulare con cima',[o,o,o,o,o,n,n]),('Boetta luminosa per il salvagente',[o,o,o,o,n,n,n]),
    ('Boette fumogene',['2','2','2','2','1',n,n]),('Fuochi a mano a luce rossa',['3','2','2','2','2',n,n]),
    ('Razzi a paracadute a luce rossa',['3','2','2','2',n,n,n]),('Imbragature con safety line (vela)',['2','2','1',n,n,n,n])]
T2=[('Bussola e tabella deviazioni, orologio',[o,o,o,n,n,n,n]),('Tabella dei segnali COLREG',[o,o,o,n,n,n,n]),('Apparato VHF',[o,o,o,n,n,n,n]),
    ('Binocolo, barometro, carte, strumenti da carteggio',[o,o,n,n,n,n,n]),('GPS, scandaglio, riflettore radar, pronto soccorso',[o,o,n,n,n,n,n]),
    ('EPIRB (o telefono satellitare)',[o,n,n,n,n,n,n]),('Fanali regolamentari',[o,o,o,o,o,n,n]),('Fischio e campana (oltre 12 m)',[o,o,o,o,o,n,n]),
    ('Pallone nero di fonda (oltre 7 m)',[o,o,o,o,o,o,n]),('Pompa di sentina',[o,o,o,o,o,o,n])]
sec('dotazioni1', head('Sicurezza · DM 133/2024, Allegato V','Le dotazioni: salvarsi')+table(T1)+p('Mezzi collettivi e individuali per tutte le persone a bordo. Di notte, in solitario, il giubbotto si indossa sempre.',24,INK,700), gap=22,
 notes='Tabella dall\'Allegato V al DM 146/2008 come sostituito dal DM 17 settembre 2024 n. 133 (G.U. S.O. n. 35 del 21/09/2024, in vigore dal 21/10/2024). Colonne: senza limiti (qui «oltre 50»), entro 50, 12, 6, 3, 1 miglio, 300 m; esistono anche le acque interne. Entro 300 m nessuna dotazione obbligatoria in tabella. Tavole, derive, kitesurf, moto d\'acqua: dispositivo di galleggiamento da 50 N sempre indossato. Fuochi a mano sostituibili con dispositivo a LED SOLAS/MED. Quiz che divergono dalla nuova tabella e che all\'esame vanno risposti come nell\'elenco: 1.3.3-15 (entro 300 m salvagente e cinture), 1.3.3-12 (cinture oltre 300 m). Oscurati: 1.3.3-4, -6, -9, -11, -14, -23, -25, -26, -32, -33, -35, -36, -41, -42.')
sec('dotazioni2', head('Sicurezza · DM 133/2024, Allegato V','Le dotazioni: navigare e comunicare')+table(T2)+p('Bussola elettronica e cartografia elettronica conforme sono ammesse. Gli estintori seguono il manuale del proprietario (unità CE).',24,INK,700), gap=22,
 notes='Stessa tabella del DM 133/2024. Quiz coerenti: 1.3.3-1 e -40 (VHF oltre 6 miglia, cioè da «entro 12»), -22 e -34 (EPIRB oltre 50), -24 (riflettore radar oltre 12), -43 (binocolo oltre 12), -39 (entro 12 niente EPIRB), -30 (radar non obbligatorio), -5 (bussola e tabelle), 1.3.3-8 (fanali di notte oltre 1 miglio), 1.7.3-7 (GPS oltre 12), 1.7.5-71 (strumenti da carteggio oltre 12). Pronto soccorso: tabella D del decreto 1° ottobre 2015 (1.3.3-45…-47). Estintori: 1.3.1-29 e -30 (manuale del proprietario; per le unità non CE il regolamento), 1.3.3-2 (natante entro 6 miglia: almeno 1).')

# ============ SEGNALI DI SOCCORSO ============
def smoke():
    return f'<rect x="0" y="0" width="300" height="200" fill="#EAF4F7"/><rect x="0" y="150" width="300" height="50" fill="{WATER}" fill-opacity="0.35"/><rect x="130" y="130" width="40" height="30" rx="6" fill="{ORANGE}" stroke="{NAVY}" stroke-width="2"/>'+''.join(f'<circle cx="{150+dx}" cy="{110-i*22}" r="{20+i*6}" fill="{ORANGE}" fill-opacity="{0.55-i*0.1:.2f}"/>' for i,dx in enumerate((0,14,30,50)))
def handflare():
    return f'<rect x="0" y="0" width="300" height="200" fill="{NIGHT}"/><rect x="140" y="90" width="20" height="90" rx="6" fill="{CORAL}"/>'+glow(150,76,LRED,14)+''.join(f'<circle cx="{150+dx}" cy="{50-i*16}" r="{8+i*3}" fill="#AAB6C3" fill-opacity="0.3"/>' for i,dx in enumerate((0,-8,-4)))
def rocket():
    return f'<rect x="0" y="0" width="300" height="200" fill="{NIGHT}"/><path d="M110 60 Q150 20 190 60 Z" fill="#DDE6EC"/><path d="M110 60 L150 100 M190 60 L150 100 M150 60 L150 100" stroke="#DDE6EC" stroke-width="2"/>'+glow(150,108,LRED,12)+dpath('M60 200 Q80 120 130 90',"#6B7F95",3)
def epirb():
    return f'<rect x="0" y="0" width="300" height="200" fill="#EAF4F7"/><rect x="0" y="150" width="300" height="50" fill="{WATER}" fill-opacity="0.35"/><rect x="126" y="70" width="48" height="96" rx="16" fill="{MYEL}" stroke="{NAVY}" stroke-width="3"/><path d="M150 70 V20" stroke="{NAVY}" stroke-width="5"/>'+glow(150,84,LWHITE,6)+''.join(f'<path d="M{150+r} 20 A{r} {r} 0 0 0 {150+r} {20+r*0.01:.0f}" fill="none"/>' for r in ())+''.join(f'<path d="M{170+i*14} {30-i*6} q10 10 0 20" fill="none" stroke="{NAVY}" stroke-width="3"/>' for i in range(3))
SG=[(smoke(),'Boetta fumogena','Fumo arancione: è un segnale <b>diurno</b>.'),(handflare(),'Fuochi a mano','Luce rossa, visibili a circa <b>6 miglia</b>.'),
    (rocket(),'Razzi a paracadute','Luce rossa per meno di 1 minuto: <b>25 miglia</b> di notte, 7 di giorno.'),(epirb(),'EPIRB','Trasmette la posizione su 406 e 121,5 MHz. Obbligatorio oltre 50 miglia.')]
cc=''.join(card(svgi(300,200,s,f'Disegno: {t}',dw=300,dh=200,pan=False)+h3(t,28)+p(d,23),None,22,10) for s,t,d in SG)
sec('soccorso', head('Sicurezza · i segnali di soccorso','Chiedere soccorso')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Pirotecnici: scadenza di solito 4 anni. Controlla la data prima di uscire.',CORAL,36),
 notes='Quiz 1.3.3-3 e -20 (boetta fumogena arancione, segnale diurno), -16 (fuochi a mano 6 miglia), -17, -28, -29 (razzi: 25 miglia di notte, 7 di giorno, meno di 1 minuto), -21 (scadenza 4 anni), -22 e -34 (EPIRB oltre 50 miglia), -7 e -18 (quantità, coerenti con il DM 133/2024). Il riflettore radar (1.5.3-10, 1.3.3-24) rende la barca visibile ai radar. VHF e chiamate di soccorso nella lezione 9.')

quiz_slide('quiz3','Quiz 3 · Dotazioni e soccorso',['1.3.3-22','1.3.3-20','1.3.3-17'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.3.3-22','1.3.3-20','1.3.3-17'],True)

# ============ TRIANGOLO DEL FUOCO ============
A=(546,70); B_=(236,560); C=(856,560)
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FFF1E6"/>'
b+=f'<path d="M{A[0]} {A[1]} L{B_[0]} {B_[1]}" stroke="{CORAL}" stroke-width="22" stroke-linecap="round"/><path d="M{B_[0]} {B_[1]} L{C[0]} {C[1]}" stroke="{SUN}" stroke-width="22" stroke-linecap="round"/><path d="M{C[0]} {C[1]} L{A[0]} {A[1]}" stroke="{BLUE}" stroke-width="22" stroke-linecap="round"/>'
b+=f'<path d="M546 470 C470 430 480 350 530 300 C520 350 560 360 560 330 C590 380 640 400 610 460 C600 480 570 480 546 470 Z" fill="{ORANGE}"/><path d="M546 470 C510 450 515 410 540 380 C545 410 565 420 575 400 C590 430 580 470 546 470 Z" fill="{SUN}"/>'
lbl=lab(X+70,Y+280,260,'Combustibile',CORAL,30,900,'right')+lab(X+770,Y+280,300,'Comburente (ossigeno)',BLUE,30,900)+lab(X+396,Y+580,300,'Calore',SUN,30,900,'center')
txt=term('La combustione','Una reazione tra combustibile e comburente che produce calore. Servono tutti e tre i lati.')+term('Come si spegne','Togli un lato: raffreddamento (calore), soffocamento (ossigeno), separazione (combustibile).')+term('Prevenzione','Niente stracci unti nel vano motore, aera prima di avviare un motore a benzina. L\'aria che entra alimenta l\'incendio.')
sec('fuoco', head('Sicurezza · incendio','Il triangolo del fuoco')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Triangolo del fuoco con una fiamma al centro: lati combustibile, comburente e calore')+lbl,
 notes='Quiz 1.3.1-24 (triangolo: combustibile, comburente, calore), -27 (combustione), -31 (comburente), -25 e -26 (si spegne abbassando la temperatura o togliendo l\'ossigeno), -10 (l\'aria alimenta l\'incendio), -5 (stracci unti), -28 (temperatura di infiammabilità). Il ciclo di aerazione del vano motore a benzina è nella lezione 2.')

# ============ CLASSI ED ESTINTORI ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FFF1E6"/>'
b+=f'<rect x="240" y="170" width="170" height="380" rx="70" fill="{LRED}" stroke="{NAVY}" stroke-width="5"/><rect x="290" y="110" width="70" height="70" rx="10" fill="#6B7F95" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M360 130 L480 110 L490 124 L372 150 Z" fill="{NAVY}"/><path d="M300 150 Q180 150 170 260 L150 330" fill="none" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<rect x="260" y="260" width="130" height="150" rx="12" fill="#FFFFFF"/><circle cx="325" cy="120" r="1" fill="none"/>'
b+=f'<circle cx="700" cy="250" r="140" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/>'
b+=f'<path d="M580 250 A120 120 0 0 1 640 146" fill="none" stroke="{LRED}" stroke-width="22"/><path d="M640 146 A120 120 0 0 1 760 146" fill="none" stroke="{LGREEN}" stroke-width="22"/><path d="M760 146 A120 120 0 0 1 820 250" fill="none" stroke="{LRED}" stroke-width="22"/>'
b+=line(700,250,680,150,NAVY,8)+f'<circle cx="700" cy="250" r="12" fill="{NAVY}"/>'+dash(360,145,560,220,NAVY,3)
lbl=lab(X+262,Y+290,126,'13B',INK,44,900,'center')+lab(X+262,Y+350,126,'classe e capacità',SOFT,22,800,'center')+lab(X+560,Y+420,300,'manometro: lancetta nel verde',LGREEN,24,900,'center')
cls=''.join(f'<div style="display:flex; gap:12px; align-items:center"><p style="width:52px; height:52px; border-radius:26px; background:{c}; color:#FFFFFF; font-family:{H}; font-size:30px; font-weight:700; text-align:center; line-height:52px; flex:none">{k}</p>{p(t,24,INK,700,1.25)}</div>' for k,t,c in [('A','solidi',SEA),('B','liquidi infiammabili',BLUE),('C','gas',PURPLE),('D','metalli',SOFT),('E','apparecchi elettrici in tensione',CORAL)])
ext=''.join(f'<div style="display:flex; justify-content:space-between; gap:10px; background:#FFFFFF; {SHADOW}; padding:8px 14px; border-radius:14px">{p(a,24,INK,800)}{p(b_,24,SEA,800)}</div>' for a,b_ in [('Polvere','tutte'),('CO2','B, C, E'),('Schiuma','A, B'),('Acqua','mai su D ed E')])
txt=f'<div style="display:flex; flex-direction:column; gap:10px">{cls}</div>'+ext+p('Getto alla base delle fiamme. Revisione se la lancetta è nel rosso o dopo l\'uso.',24,INK,700)
sec('estintori', head('Sicurezza · incendio','Classi di incendio ed estintori'), pinned=svgp(X,Y,W,Hh,b,'Estintore con etichetta 13B e il suo manometro con la lancetta nella zona verde')+lbl+pcol(txt,532,14),
 notes='Quiz 1.3.1-16, -9, -17, -14 (classi A solidi, B liquidi, C gas, E elettrico), -1 e -12 (polvere: tutte le classi), -13, -18, -19, -6 (CO2 per liquidi, gas e apparecchi elettrici; VHF in fiamme: CO2), -2 e -15 (schiuma: A e B), -7 (getto alla base), -8 e -20 (acqua pericolosa su metalli e impianti elettrici), -11 (13B: classe e capacità estinguente), -21, -22, -23 (revisione e sostituzione), -4 (omologati CE). Il quiz 1.3.1-3 è oscurato: la CO2 nei locali chiusi toglie l\'ossigeno anche alle persone.')
X=700

quiz_slide('quiz4','Quiz 4 · Incendio',['1.3.1-24','1.3.1-14','1.3.1-18'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.3.1-24','1.3.1-14','1.3.1-18'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.5.3-66','1.4.1-10','1.3.3-24'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.5.3-66','1.4.1-10','1.3.3-24'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.5.2-35','1.3.1-2','1.3.3-43'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.5.2-35','1.3.1-2','1.3.3-43'],True)
closing(['Un faro si riconosce dalla caratteristica: tipo, colore, periodo','Entrando in porto: rosso a sinistra, verde a dritta; le cardinali dicono dove passare','1 breve a dritta, 2 brevi a sinistra; nella nebbia 1 prolungato ogni 2 minuti','Oltre 12 miglia: zattera, binocolo, GPS, riflettore radar; oltre 50: EPIRB','Triangolo del fuoco; CO2 per l\'elettrico, mai acqua'],
 'Prossima lezione · 07 · Meteorologia e normativa','A casa: i 120 quiz su fari e IALA, i 21 sui porti, i 48 sulle dotazioni e i 31 sull\'incendio.')
write_deck(OUT,'Lezione 06 · Segnalamento, segnali sonori e sicurezza',
 ['cover','agenda','fari','caratteristica','laterali','cardinali','altri','quiz1','quiz1r','sonori','nebbia','porto','quiz2','quiz2r',
  'dotazioni1','dotazioni2','soccorso','quiz3','quiz3r','fuoco','estintori','quiz4','quiz4r','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Fari e segnalamento AISM-IALA","start":"fari"},
  "s3":{"description":"Segnali sonori, nebbia e porti","start":"sonori"},"s4":{"description":"Dotazioni di sicurezza DM 133/2024 e segnali di soccorso","start":"dotazioni1"},
  "s5":{"description":"Incendio ed estintori, verifica finale","start":"fuoco"}})
