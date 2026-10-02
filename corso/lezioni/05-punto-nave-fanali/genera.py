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
cover(5,'COLREG e prevenzione degli abbordi','Chi è quella luce? Fanali e segnali diurni. Chi passa per primo? Rischio di collisione, precedenze e regole di rotta',
 'Lezione 5. Capitolo del programma della scuola: Prevenzione degli abbordi (fanali e precedenze). Aggiunta dall\'All. A: segnali diurni (materia 5). La navigazione costiera, il punto nave, i rilevamenti e il GPS sono passati nella lezione 4; segnali sonori e segnalamento IALA nella lezione 6.', title_size=88)
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','28′','Cap. 1 · Fanali di navigazione',PURPLE),('0:28','22′','Cap. 2 · Segnali diurni e precedenze',BLUE),('0:50','25′','Cap. 3 · Regole di rotta',SEA),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{max(int(d[:-1]),14)}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['colreg'],5,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>riconoscere una barca di notte dai fanali</li><li>leggere i segnali diurni e le luci speciali</li><li>capire se c\'è rischio di collisione</li><li>sapere chi lascia libera la rotta, a motore e a vela</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 05 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Tre capitoli di teoria in 75 minuti, ognuno chiuso da una verifica da 2 quiz ufficiali (DD 131/2022): c\'è tempo per far disegnare le luci alla lavagna e discutere i casi. Poi 45 minuti di raccolta quiz: 36 quiz ufficiali. Banca: fanali e segnali diurni 67 (1.5.1), prevenire gli abbordi 60 (1.5.2). All. C: 2 quesiti di COLREG e segnalamento nella scheda da 20. La navigazione costiera, il punto nave, i rilevamenti e il GPS sono nella lezione 4.')

# ============ IL COLREG ============
LB.ICON_T['Che cos\'è il COLREG']='helm'
def colreg_art():
    s=f'<rect x="0" y="0" width="520" height="600" rx="40" fill="{NIGHT}"/>'
    s+=''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#FFFFFF" opacity="0.6"/>' for x,y in ((40,40),(120,70),(470,50),(400,110),(70,150),(300,30),(480,170)))
    g=(260,190); R=130
    s+=f'<circle cx="{g[0]}" cy="{g[1]}" r="{R}" fill="#2A6FB0"/>'
    s+=f'<path d="M170 120 Q200 90 240 110 Q250 140 220 160 Q190 170 175 150 Z M280 90 Q330 80 350 120 Q340 160 300 150 Q270 130 280 90 Z M230 220 Q270 200 300 230 Q310 270 270 290 Q240 280 230 220 Z M330 200 Q360 190 370 220 Q350 250 330 230 Z" fill="#3FAE6B"/>'
    s+=f'<ellipse cx="{g[0]}" cy="{g[1]}" rx="{R}" ry="44" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/><ellipse cx="{g[0]}" cy="{g[1]}" rx="52" ry="{R}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/><line x1="{g[0]-R}" y1="{g[1]}" x2="{g[0]+R}" y2="{g[1]}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/>'
    s+=f'<path d="M120 300 Q260 380 400 300" fill="none" stroke="{SUN}" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/>'
    s+=f'<rect x="150" y="268" width="220" height="56" rx="28" fill="{CORAL}"/><text x="260" y="306" text-anchor="middle" font-family="Arial" font-size="30" font-weight="900" fill="#FFFFFF">COLREG 72</text>'
    parts=[('A','Generalità',SEA),('B','Governo e navigazione',BLUE),('C','Fanali e segnali',SUN),('D','Segnali sonori e luminosi',PURPLE),('E','Esenzioni',GREEN),('F','Verifica IMO',CORAL)]
    for i,(k,t,c) in enumerate(parts):
        y=356+i*38
        s+=f'<rect x="60" y="{y}" width="400" height="32" rx="10" fill="#FFFFFF" fill-opacity="0.08"/><rect x="60" y="{y}" width="40" height="32" rx="10" fill="{c}"/>'
        s+=f'<text x="80" y="{y+23}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">{k}</text><text x="116" y="{y+23}" font-family="Arial" font-size="20" font-weight="700" fill="#FFFFFF">{t}</text>'
    s+=f'<text x="260" y="590" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#FFFFFF" opacity="0.75">41 regole in 6 parti + 4 allegati</text>'
    return s
CQ=[('Che cos\'è','COLREG sta per <i>Collision Regulations</i>: la Convenzione di Londra del <b>1972</b> (IMO), in vigore dal <b>1977</b>. In italiano: <b>Regolamento internazionale per prevenire gli abbordi in mare</b>. Abbordo = collisione tra navi.',NAVY,BLUE_T),
    ('Perché è così importante','È la <b>lingua comune del mare</b>: in ogni paese le barche manovrano allo stesso modo e si riconoscono da luci, forme e suoni. Non basta però: vale sempre la buona pratica marinaresca e, per evitare un pericolo immediato, si può derogare.',CORAL,CORAL_T),
    ('Quando e dove si applica','<b>Sempre</b>, di giorno e di notte, in alto mare e in tutte le acque collegate navigabili dalle navi: anche sotto costa. Porti, fiumi e laghi possono avere <b>regole locali</b> (ordinanze), il più possibile conformi.',SEA,SEA_T),
    ('Chi lo deve rispettare','<b>Ogni nave</b>, cioè qualsiasi mezzo che galleggia e trasporta sull\'acqua: dalla petroliera al gommone, a vela, a motore o a remi, anche cuscini d\'aria e idrovolanti. Ne risponde chi ha il comando.',PURPLE,LILAC_T)]
cc=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:24px 26px; border-radius:28px">{tag(t,c)}{p(d,24,INK,500,1.38)}</div>' for t,d,c,bg in CQ)
sec('colreg', head('COLREG · le regole di tutti','Che cos\'è il COLREG')+f'<div style="display:flex; gap:32px; align-items:start">{svgi(520,600,colreg_art(),"Il globo con una rotta tratteggiata e la fascia COLREG 72; sotto le sei parti del regolamento: A generalità, B governo e navigazione, C fanali e segnali, D segnali sonori e luminosi, E esenzioni, F verifica IMO",dw=460,dh=531,pan=False)}<div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:18px">{cc}</div></div>',
 notes='Prima slide della lezione: tutta la lezione applica il COLREG. Convention on the International Regulations for Preventing Collisions at Sea, adottata a Londra il 20 ottobre 1972 dall\'IMO, in vigore dal 15 luglio 1977; in Italia resa esecutiva con la legge 27 dicembre 1977, n. 1085. Regola 1 (applicazione): alto mare e acque collegate navigabili; le regole locali di porti, rade, fiumi e laghi devono essere il più possibile conformi. Regola 2 (responsabilità): il rispetto delle regole non esonera dalla buona pratica marinaresca. Regola 3: «nave» è ogni tipo di galleggiante usato o utilizzabile come mezzo di trasporto sull\'acqua. Parte C: fanali e segnali (oggi capitolo 1); Parte B: precedenze e regole di rotta; Parte D: segnali sonori. Quiz 1.5.2-2 (la norma è il COLREG \'72), 1.5.1-62 (l\'elenco completo dei fanali è nel COLREG), 1.5.1-25 e -26. Trucchetto di Ancorotto: nei quiz sui fanali la risposta che cita il Regolamento per prevenire gli abbordi in mare (COLREG) è sempre quella giusta.')

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

quiz_slide('quiz2','Quiz 1 · I fanali',['1.5.1-4', '1.5.1-39'],False)
quiz_slide('quiz2r','Quiz 1 · Le risposte',['1.5.1-4', '1.5.1-39'],True)

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

quiz_slide('quiz3','Quiz 2 · Segnali e precedenze',['1.5.1-10', '1.5.1-60'],False)
quiz_slide('quiz3r','Quiz 2 · Le risposte',['1.5.1-10', '1.5.1-60'],True)

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

quiz_slide('quiz4','Quiz 3 · Precedenze',['1.5.2-44', '1.5.2-6'],False)
quiz_slide('quiz4r','Quiz 3 · Le risposte',['1.5.2-44', '1.5.2-6'],True)
exec(open('apertura.py').read())
chapter('cap2',1,'Fanali di navigazione',['I fanali di navigazione','Cosa vedo di notte','Le barche a vela di notte'],PURPLE,
 'Circa 28 minuti, verifica da 2 quiz compresa: far disegnare i settori alla lavagna.','circa 28 minuti · 3 argomenti',1)
chapter('cap3',2,'Segnali diurni e precedenze',['Segnali diurni e luci speciali','Chi lascia la rotta a chi'],BLUE,
 'Circa 22 minuti, verifica da 2 quiz compresa.','circa 22 minuti · 2 argomenti',1)
chapter('cap4',3,'Regole di rotta',['C\'è rischio di collisione?','Due barche a motore','Due barche a vela'],SEA,
 'Circa 25 minuti, verifica da 2 quiz compresa: provare i casi con due modellini.','circa 25 minuti · 3 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
QZ=[('q01','Quiz 1 · Quando si accendono',['1.5.1-23','1.5.1-56','1.5.1-27']),('q02','Quiz 2 · Colori e settori',['1.5.1-7','1.5.1-12','1.5.1-36']),
 ('q03','Quiz 3 · I fanali',['1.5.1-5','1.5.1-18','1.5.1-30']),('q04','Quiz 4 · Motore di notte',['1.5.1-1','1.5.1-17','1.5.1-38']),
 ('q05','Quiz 5 · Navi grandi e vela',['1.5.1-29','1.5.1-66','1.5.1-61']),('q06','Quiz 6 · Segnali diurni',['1.5.1-2','1.5.1-21','1.5.1-32']),
 ('q07','Quiz 7 · Luci speciali',['1.5.1-13','1.5.1-19','1.5.1-24']),('q08','Quiz 8 · Rischio di collisione',['1.5.2-3','1.5.2-18','1.5.2-41']),
 ('q09','Quiz 9 · Evitare la collisione',['1.5.2-4','1.5.2-43','1.5.2-55']),('q10','Quiz 10 · Precedenze a motore',['1.5.2-9','1.5.2-39','1.5.2-46']),
 ('q11','Quiz 11 · Chi raggiunge',['1.5.2-17','1.5.2-45','1.5.2-54']),('q12','Quiz 12 · Vela, raggiunta, gerarchia',['1.5.2-7','1.5.2-19','1.5.2-29'])]
raccolta(5,4,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Disegna la barca','Fanali e settori: schizza la barca vista dall\'alto con 225°, 112,5° e 135°.'),
  ('Chi è a dritta?','A motore lascia la rotta chi vede l\'altro sulla propria dritta; a vela conta il vento.'),
  ('Attento ai numeri','Gradi, miglia e lunghezze delle navi: 12 e 50 metri cambiano i fanali.')],
 ['Quiz 1-5 · fanali (15)','Quiz 6-7 · segnali diurni e luci speciali (6)','Quiz 8-12 · rischio di collisione e precedenze (15)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Far rispondere ad alta voce con la lettera, poi chiedere perché le altre due sono sbagliate. Se il tempo stringe, lasciare per casa le slide 5 e 11.',esame=['colreg'])
closing(['Fanali accesi dal tramonto al sorgere del sole e con visibilità ridotta','Un pallone nero: alla fonda; un cono a vertice in giù: vela con il motore acceso','Testa d\'albero 225°, laterali 112,5°, coronamento 135°','Rilevamento costante e distanza che cala: rischio di collisione','Motore: cede a chi viene da dritta; vela: mure a sinistra e sopravento cedono'],
 'Prossima lezione · 06 · La sicurezza e i suoi elementi nella navigazione','A casa: i 67 quiz su fanali e segnali diurni e i 60 sulle precedenze.')
write_deck(OUT,'Lezione 05 · COLREG e prevenzione degli abbordi',
 ['cover','agenda','colreg',
  'cap2','fanali','cosavedo','velanotte','quiz2','quiz2r','cap3','diurni','gerarchia','quiz3','quiz3r',
  'cap4','rischio','motore','vela','quiz4','quiz4r','capquiz','quiz']+[q+s for q,_,_ in QZ for s in ('','r')]+['chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Fanali di navigazione e barche a vela di notte","start":"cap2"},
  "s3":{"description":"Segnali diurni, luci speciali e scala delle precedenze","start":"cap3"},"s4":{"description":"Rischio di collisione e regole di rotta","start":"cap4"},
  "s5":{"description":"Raccolta quiz","start":"capquiz"}})
