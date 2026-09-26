import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez04/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; SAND='#F3E3B8'; GREY='#97A6B4'; STEEL='#8E9BAA'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Com\'è fatta un\'ancora':'anchor','I tipi di ancora':'anchor','Il calumo':'anchor',
 'La manovra di ancoraggio':'anchor','Alla ruota o afforcati':'anchor','Vicino alla spiaggia':'flag','Subacquei e piccoli natanti':'flag',
 'La bussola magnetica':'compass','Tre nord':'compass','Da bussola a vero e ritorno':'compass','Prora e rotta':'map',
 'Lo scarroccio':'wind','La deriva':'current','Vento «da», corrente «verso»':'wind'})
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def pcol(inner,w=532,gap=24): return f'<div style="position:absolute; left:1260px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def chip(t,c,size=34): return f'<p style="font-family:{H}; font-size:{size}px; font-weight:700; color:#FFFFFF; background:{c}; padding:10px 24px; border-radius:40px">{t}</p>'
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
X,Y,W,Hh=700,290,1092,620

def anchor_icon(x,y,s=1,c=NAVY):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round">'
            f'<circle cx="0" cy="-26" r="7"/><path d="M0 -19 V26 M-13 -9 H13 M-24 10 Q-20 28 0 26 Q20 28 24 10"/></g>')

# ============ COVER + AGENDA ============
cover(4,'Ancoraggio, prora e rotta','Dare fondo all\'ancora, navigare sottocosta, passare dalla bussola alla carta: scarroccio e deriva',
 'Lezione 4. Capitoli del programma della scuola: Attracchi, ormeggi e ancoraggi (ancoraggio) e Carteggio (prora e rotta, scarroccio, deriva, declinazione, deviazione). Aggiunta dall\'All. A: condotta sottocosta, limiti di velocità, balneazione e corridoi di lancio (punto 4a). Materia 7 per bussola e conversioni.')
blocks=[('0:00','20′','L\'ancora: parti, tipi, calumo',CORAL),('0:20','20′','Manovra, ruota · quiz 1',SEA),('0:40','20′','Sottocosta e subacquei · quiz 2',PURPLE),('1:00','25′','Bussola e tre nord · quiz 3',BLUE),('1:25','20′','Prora, rotta, scarroccio, deriva · quiz 4',GREEN),('1:45','15′','Verifica finale',CORAL)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">4 + 4</p>'+p('domande su 20: Manovra e condotta, Navigazione cartografica',26,INK,700)+p('Nel carteggio: conversioni bussola-vero in quasi ogni esercizio e 24 esercizi di scarroccio (lezione 12).',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>riconoscere le ancore e filare il calumo giusto</li><li>dare fondo, controllare la tenuta e salpare</li><li>rispettare le regole vicino alla spiaggia</li><li>passare da prora bussola a prora vera e ritorno</li><li>distinguere prora e rotta, scarroccio e deriva</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 04 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie da 3 quiz e una finale da 6, tutti ufficiali (DD 131/2022). Banca: ancoraggio 53 quiz (1.4.3), navigazione in prossimità della costa 32 (1.4.2), bussola e orientamento 49 (1.7.4), prora e rotta, scarroccio e deriva 30 (1.7.7).')

# ============ L'ANCORA ============
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
txt=term('Marre e diamante','I bracci che fanno presa sono le marre; al centro, in basso, c\'è il diamante.')+term('La tenuta','Dipende dal peso e, in parte, dalla forma. Barca di 10 m: ancora di 15-20 kg.')+term('Sul fondo','L\'ancora deve restare orizzontale anche quando la barca tira sul calumo.')+term('Il barbotin','La ruota del verricello salpancore con l\'impronta della catena: non la fa slittare.')
sec('ancora', head('Ancoraggio · le parti','Com\'è fatta un\'ancora')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Ancora classica con cicala, ceppo, fuso, marre con le patte e diamante, e catena a maglie ellittiche')+lbl,
 notes='Quiz 1.4.3-16 e -25 (marre), -19 e -33 (diamante), -1 (tenuta: peso e forma), -21 (10 m: 15-20 kg), -18 (ancora orizzontale sul fondo), -9 (maglie ellittiche), -10 (barbotin). Il disegno è un\'ancora ammiragliato, la più chiara per imparare i nomi; a bordo si usano i tipi della slide seguente.')

# ============ TIPI DI ANCORA ============
def danforth():
    return (f'<rect x="146" y="20" width="18" height="140" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<rect x="80" y="150" width="150" height="14" rx="7" fill="{NAVY}"/><path d="M146 160 L96 70 L128 60 L150 150 Z M164 160 L214 70 L182 60 L160 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def cqr():
    return (f'<path d="M150 22 Q190 60 170 110" fill="none" stroke="{STEEL}" stroke-width="16" stroke-linecap="round"/><circle cx="148" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M170 100 L100 150 L150 150 L170 170 L190 150 L240 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def rocna():
    return (f'<rect x="146" y="20" width="18" height="120" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M70 120 Q155 190 240 120 L240 140 Q155 205 70 140 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><path d="M80 122 Q155 40 230 122" fill="none" stroke="{NAVY}" stroke-width="7"/>')
def grappino():
    s=f'<rect x="146" y="20" width="18" height="120" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
    for dx,op in ((-1,1),(1,1),(-0.45,0.6),(0.45,0.6)):
        s+=f'<path d="M155 140 Q{155+dx*60:.0f} 150 {155+dx*70:.0f} 100" fill="none" stroke="{NAVY}" stroke-opacity="{op}" stroke-width="10" stroke-linecap="round"/>'
    return s
def ombrello():
    s=f'<rect x="146" y="20" width="18" height="130" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="155" cy="140" r="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    for a in (-60,-25,25,60):
        x2,y2=155+80*math.sin(math.radians(a)),140-60*math.cos(math.radians(a))*-1
        s+=f'<path d="M155 140 L{x2:.0f} {y2-110:.0f}" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>'
    return s
TP=[(danforth(),'Danforth','Due marre piatte e mobili: ottima su <b>sabbia e fango</b>.'),
    (cqr(),'CQR e Delta','A vomere d\'aratro: vanno bene <b>su tutti i fondali</b>.'),
    (rocna(),'Rocna, Mantus, Ultra','Marra concava; la Rocna ha il roll-bar. Tenuta dinamica, <b>tutti i fondali</b>.'),
    (grappino(),'Grappino','Piccola, quattro marre fisse: per <b>piccole unità</b> e soste brevi.'),
    (ombrello(),'A ombrello','Marre richiudibili: per <b>gonfiabili</b> e piccole unità.')]
cc=''.join(card(svgi(310,190,s,f'Disegno dell\'ancora {t}',dw=270,dh=166)+h3(t,28)+p(d,23),None,22,8) for s,t,d in TP)
sec('tipi', head('Ancoraggio · i modelli','I tipi di ancora')+f'<div style="display:flex; gap:18px">{cc}</div>'+note('Scegli l\'ancora in base al fondo: la carta nautica te lo dice (r, f, s).',SEA,38),
 notes='Quiz 1.4.3-39 (Danforth su sabbia e fango), -40 (CQR e Delta per tutti i fondali), -49 (Mantus e Ultra, tenuta dinamica), -52 (Rocna con roll-bar), -7 e -28 (grappino), -6 (ombrello per battelli gonfiabili). Il quiz 1.4.3-8 sulla Bruce è oscurato.')

# ============ CALUMO
X=128
b=f'<rect x="0" y="140" width="1092" height="480" fill="{WATER}" fill-opacity="0.2"/>'+line(0,140,1092,140,SEA,3)
b+=f'<path d="M0 560 Q400 548 700 560 T1092 556 L1092 620 L0 620 Z" fill="{SAND}"/>'
b+=profile(60,146,320)
b+=f'<path d="M372 108 Q420 120 480 250 Q560 470 720 556 L860 560" fill="none" stroke="{NAVY}" stroke-width="7" stroke-dasharray="12 6"/>'
b+=f'<g transform="translate(900 546) rotate(-90)">{anchor_icon(0,0,1.1)}</g>'
b+=dim(1010,140,1010,556,INK)
lbl=lab(X+880,Y+320,200,'fondale',INK,26,900,bg='#FFFFFF')+lab(X+500,Y+330,220,'calumo',NAVY,26,900,bg='#FFFFFF')+lab(X+780,Y+480,300,'ancora orizzontale',CORAL,24,800)
ex=''.join(f'<div style="display:flex; flex-direction:column; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 14px; border-radius:20px"><p style="font-size:24px; font-weight:800; color:{SOFT}; white-space:nowrap">fondo {a}</p><p style="font-family:{H}; font-size:40px; font-weight:700; color:{CORAL}">{c} m</p></div>' for a,c in [('5 m',15),('9 m',27),('16 m',48)])
txt=term('Calumo','La lunghezza di catena o cima filata per dare fondo all\'ancora.')+term('Quanto filarne','Almeno 3 volte il fondale; da 3 a 5 volte secondo il vento e il mare.')+p('<b>Con mare calmo, almeno:</b>',26,INK)+f'<div style="display:flex; gap:12px">{ex}</div>'
sec('calumo', head('Ancoraggio · la catena','Il calumo'), pinned=pcol(txt,540,20)+svgp(X,Y,W,Hh,b,'Barca alla fonda: la catena scende dalla prua con una curva e resta distesa sul fondo, l\'ancora giace orizzontale; a destra la misura del fondale')+lbl,
 notes='Quiz 1.4.3-34 (calumo), -50 (minimo 3 volte il fondale), -3 e -32 (da 3 a 5 volte), -27, -29, -30 (16 m → 48 m, 9 m → 27 m, 5 m → 15 m). Il tratto di catena sul fondo tiene l\'ancora orizzontale e fa lavorare le marre. Il quiz 1.4.3-20 sul calumo è oscurato: vale la definizione di -34.')
X=700

# ============ MANOVRA ============
b=''.join(arrow(x,30,x,110,GREY,8,24) for x in (140,540,940))
b+=f'<path d="M0 0 L1092 0 L1092 20 Q800 40 546 18 Q300 0 0 24 Z" fill="{LAND}"/>'
b+=dpath('M220 480 L220 330',CORAL,5)+topboat(220,300,180,-90,'#FFFFFF',NAVY,4)+anchor_icon(220,180,0.9,CORAL)+num(120,300,1,CORAL,22)
b+=topboat(560,440,180,-90,'#FFFFFF',NAVY,4)+f'<path d="M560 350 L560 190" stroke="{NAVY}" stroke-width="5" stroke-dasharray="10 6"/>'+anchor_icon(560,180,0.9,NAVY)+arrow(640,300,640,420,SEA,6,20)+num(460,440,2,SEA,22)
b+=topboat(900,440,180,-90,'#FFFFFF',NAVY,4)+f'<path d="M900 350 L900 190" stroke="{NAVY}" stroke-width="6"/>'+anchor_icon(900,180,0.9,NAVY)+num(800,440,3,PURPLE,22)
b+=dash(900,440,1060,90,PURPLE,3)+dash(900,440,760,70,PURPLE,3)+f'<path d="M1050 70 l12 24 h-24 Z M750 50 l12 24 h-24 Z" fill="{PURPLE}"/>'
lbl=lab(X+90,Y+530,300,'Prua al vento: cala a abbrivio finito',CORAL,24,800,'center')+lab(X+420,Y+530,300,'Fila il calumo indietreggiando',SEA,24,800,'center')+lab(X+760,Y+530,300,'Fa testa? Controlla con i rilevamenti',PURPLE,24,800,'center')+lab(X+460,Y+120,200,'vento',SOFT,24,800,'center')
txt=term('Prima di dare fondo','Controlla divieti e previsioni del tempo.')+term('Fa testa · ara','L\'ancora fa testa quando ha preso il fondo; se non tiene «ara» o «speda».')+term('Per salpare','Un leggero colpo di marcia avanti toglie tensione alla catena.')+term('Vento forte, poi di poppa in banchina','Dai fondo leggermente sopravento al posto barca.')
sec('manovra', head('Ancoraggio · passo passo','La manovra di ancoraggio')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto in tre tempi: barca che arriva con la prua al vento e cala l\'ancora, poi fila il calumo indietreggiando, infine controlla la tenuta con due rilevamenti a terra')+lbl,
 notes='Quiz 1.4.3-12 e -43 (prua al vento, a abbrivio esaurito si cala), -42 (si indietreggia filando il calumo), -15 (controllo della tenuta con rilevamenti successivi di punti cospicui o con il GPS), -17 e -31 (fa testa), -24 (ara), -37 (speda), -2 (divieti e meteo), -51 (salpare), -46 (vento forte: filare in fretta allentando il barbotin), -47 (fondo sopravento al posto barca), -44, -45, -53 (figure).')

# ============ RUOTA
X=128
b=f'<circle cx="290" cy="330" r="220" fill="{SEA}" fill-opacity="0.08" stroke="{SEA}" stroke-width="3" stroke-dasharray="12 8"/>'+anchor_icon(290,330,1,NAVY)
b+=dash(290,330,290,160,NAVY,4)+topboat(290,120,150,-90,'#FFFFFF',NAVY,4)+topboat(450,440,150,40,'#FFFFFF',NAVY,3,0.45,False)+topboat(150,470,150,140,'#FFFFFF',NAVY,3,0.45,False)
b+=f'<ellipse cx="820" cy="300" rx="120" ry="200" fill="{PURPLE}" fill-opacity="0.08" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="12 8"/>'
b+=anchor_icon(720,500,0.9,NAVY)+anchor_icon(920,500,0.9,NAVY)+line(820,260,724,480,NAVY,4)+line(820,260,916,480,NAVY,4)+topboat(820,180,150,-90,'#FFFFFF',NAVY,4)
lbl=lab(X+140,Y+566,300,'Alla ruota: gira di 360°',SEA,24,900,'center')+lab(X+660,Y+566,320,'Afforcata: campo di giro ellittico',PURPLE,24,900,'center')
txt=term('Alla ruota','Una sola ancora di prua: la barca gira di 360° e serve spazio libero attorno. Mai un\'ancora di poppa in più.')+term('Afforcata','Due ancore con i calumi aperti di circa 45°: il giro diventa un\'ellisse.')+term('La grippia','Una cima sottile legata al diamante, con un gavitello: aiuta a recuperare l\'ancora sui fondali rocciosi.')
sec('ruota', head('Ancoraggio · stare alla fonda','Alla ruota o afforcati'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Vista dall\'alto: a sinistra una barca alla ruota con il cerchio di rotazione; a destra una barca afforcata su due ancore con il campo di giro ellittico')+lbl,
 notes='Quiz 1.4.3-35 e -36 (alla ruota), -4 (serve spazio libero), -23 (non dare ancora di poppa), -22 (afforcata a 45°), -11 (campo di giro ellittico), -5 (nei fiumi due ancore a 180° nella direzione della corrente), -38 (ancore appennellate), -13, -14, -26 (grippia e grippiale), -41 e -48 (in baia più unità a murata: sconsigliato).')
X=700

quiz_slide('quiz1','Quiz 1 · Ancoraggio',['1.4.3-27','1.4.3-17','1.4.3-26'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.4.3-27','1.4.3-17','1.4.3-26'],True)

# ============ SOTTOCOSTA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/><path d="M0 520 Q300 500 546 520 T1092 512 L1092 620 L0 620 Z" fill="{SAND}"/>'+f'<path d="M0 520 Q300 500 546 520 T1092 512" fill="none" stroke="{LAND_S}" stroke-width="4"/>'
b+=''.join(f'<circle cx="{x}" cy="290" r="10" fill="{RED}" stroke="{NAVY}" stroke-width="2"/>' for x in range(40,1092,90) if not 660<x<860)
for yy in range(300,500,50):
    for xx in (700,820): b+=f'<circle cx="{xx}" cy="{yy}" r="10" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
b+=''.join(f'<circle cx="{xx}" cy="250" r="10" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/><path d="M{xx} 250 V206 L{xx+30} 216 L{xx} 226" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>' for xx in (700,820))
b+=topboat(760,400,120,90,'#FFFFFF',NAVY,4)
b+=''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{CORAL}"/>' for x,y in ((200,450),(260,470),(420,430),(500,470),(950,450)))
b+=f'<circle cx="260" cy="130" r="110" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="10 8"/><circle cx="260" cy="130" r="55" fill="{RED}" fill-opacity="0.1"/>'
b+=f'<circle cx="260" cy="130" r="10" fill="{RED}"/><path d="M260 130 V86" stroke="{NAVY}" stroke-width="3"/><rect x="260" y="86" width="44" height="30" fill="{RED}"/><path d="M260 116 L304 86" stroke="#FFFFFF" stroke-width="6"/>'
b+=dim(1040,290,1040,516,INK)
lbl=lab(X+20,Y+560,300,'battigia',INK,24,800)+lab(X+880,Y+380,160,'200 m',INK,26,900,bg='#FFFFFF')+lab(X+20,Y+312,420,'gavitelli rossi ogni 50 m',RED,24,900)+lab(X+620,Y+150,340,'corridoio di lancio',INK,24,900,'center')+lab(X+390,Y+100,300,'subacqueo: stai ad almeno 100 m',RED,24,900)
txt=term('I 200 metri','Di massima si naviga, si sosta e si ancora oltre 200 m dalle spiagge. Il limite è segnato da gavitelli rossi ogni 50 m.')+term('Corridoi di lancio','Gavitelli gialli o arancioni perpendicolari alla costa, bandiere bianche su quelli esterni: per partire e arrivare a motore, a lento moto.')+term('Emergenza','Se devi raggiungere la riva: a lento moto, con i remi, perpendicolare alla costa.')
sec('costa', head('Condotta · la stagione balneare','Vicino alla spiaggia')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto di una spiaggia: fascia dei 200 metri segnata da gavitelli rossi, corridoio di lancio con gavitelli gialli e bandiere bianche, barca che entra piano, bagnanti e boa di un subacqueo con la distanza di rispetto')+lbl,
 notes='Quiz 1.4.2-4 (200 m), -5 (gavitelli rossi ogni 50 m), -6 e -7 (corridoi: gavitelli gialli o arancioni, bandiere bianche sugli esterni), -17 (a cosa servono i corridoi), -11 (emergenza: remi, perpendicolare alla riva), -25 (navigazione a motore interdetta nella fascia riservata alla balneazione), -10 (sanzione da 414 a 2.066 euro per i limiti di velocità). I limiti di velocità e le distanze li fissa l\'ordinanza balneare della Capitaneria: leggerla prima di uscire. I quiz 1.4.2-1 e -3 sono oscurati.')

# ============ SUBACQUEI E 1 MIGLIO ============
def flag_sub():
    return f'<rect x="0" y="0" width="300" height="190" fill="{WATER}" fill-opacity="0.2"/><path d="M120 170 V30" stroke="{NAVY}" stroke-width="6"/><rect x="120" y="30" width="130" height="86" fill="{RED}" stroke="{NAVY}" stroke-width="3"/><path d="M120 116 L250 30" stroke="#FFFFFF" stroke-width="16"/><ellipse cx="120" cy="170" rx="44" ry="16" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/>'
def flag_alfa():
    return f'<rect x="0" y="0" width="300" height="190" fill="{WATER}" fill-opacity="0.2"/><path d="M70 176 V20" stroke="{NAVY}" stroke-width="6"/><rect x="70" y="30" width="80" height="110" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M150 30 L250 30 L200 85 L250 140 L150 140 Z" fill="{BLUE}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
def night():
    return f'<rect x="0" y="0" width="300" height="190" fill="{NAVY}"/><circle cx="150" cy="80" r="60" fill="{SUN}" fill-opacity="0.18"/><circle cx="150" cy="80" r="30" fill="{SUN}" fill-opacity="0.35"/><circle cx="150" cy="80" r="14" fill="{SUN}"/><path d="M150 94 V150" stroke="#FFFFFF" stroke-width="4"/><ellipse cx="150" cy="156" rx="40" ry="14" fill="{CORAL}"/>'
def mile():
    s=f'<rect x="0" y="0" width="300" height="190" fill="{WATER}" fill-opacity="0.2"/><path d="M0 160 Q150 150 300 162 L300 190 L0 190 Z" fill="{SAND}"/>'
    s+=dash(0,50,300,50,CORAL,4)+dim(270,56,270,152,INK)
    s+=f'<ellipse cx="80" cy="110" rx="26" ry="9" fill="{CORAL}" stroke="{NAVY}" stroke-width="2"/><path d="M150 124 L150 76 L178 118 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/><rect x="132" y="120" width="40" height="8" rx="4" fill="{SUN}"/><rect x="200" y="100" width="40" height="18" rx="9" fill="{SEA}" stroke="{NAVY}" stroke-width="2"/>'
    return s
SB=[(flag_sub(),'Bandiera del subacqueo','Rossa con diagonale bianca: c\'è un sub <b>entro 50 m</b>. Rallenta e passa ad <b>almeno 100 m</b>.'),
    (flag_alfa(),'Bandiera «A» (Alfa)','Codice internazionale dei segnali: l\'unità ha un <b>palombaro in immersione</b>.'),
    (night(),'Di notte','La boa del sub mostra una luce <b>gialla lampeggiante</b>, visibile a 360° e ad almeno 300 m.'),
    (mile(),'Entro 1 miglio','Moto d\'acqua, tavole a vela, pedalò e jole, vele fino a 4 m², tender (dalla costa o dalla barca madre).')]
cc=''.join(card(svgi(300,190,s,f'Disegno: {t}',dw=300,dh=190)+h3(t,28)+p(d,23),None,22,10) for s,t,d in SB)
sec('subacquei', head('Condotta · chi c\'è in acqua','Subacquei e piccoli natanti')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Gara o manifestazione sulla rotta? Cambia percorso e stanne lontano.',PURPLE,36),
 notes='Quiz 1.4.2-15 (bandierina rossa con diagonale bianca, sub entro 50 m), -2 e -12 (almeno 100 m, moderando la velocità), -19 (sub a non più di 50 m dalla boa), -8 (unità di appoggio: pallone rosso con bandiera), -14 (bandiera A: palombaro), -9 e -16 (di notte luce gialla lampeggiante, visibile ad almeno 300 m), -20…-24 (entro 1 miglio), -13 (manifestazioni sportive). Pesca: -18 (sportiva consentita entro limiti di cattura), -26 (subacquea oltre 500 m dalle spiagge frequentate), -27 (mai di notte col fucile), -31 (mai con autorespiratori), -30 (100 m dagli impianti fissi), -32 (500 m dai pescatori professionali), -28 e -29 (niente reti a circuizione né pesca professionale).')

quiz_slide('quiz2','Quiz 2 · Sottocosta',['1.4.2-4','1.4.2-2','1.4.2-6'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.4.2-4','1.4.2-2','1.4.2-6'],True)

# ============ BUSSOLA
X=128
cx,cy=546,320
b=topboat(cx,cy,560,-90,'#FFFFFF',NAVY,3,0.35,False)
b+=f'<circle cx="{cx}" cy="{cy}" r="230" fill="none" stroke="{STEEL}" stroke-width="10"/><circle cx="{cx}" cy="{cy}" r="206" fill="none" stroke="{STEEL}" stroke-width="8"/>'
b+=f'<rect x="{cx-240}" y="{cy-10}" width="24" height="20" rx="4" fill="{NAVY}"/><rect x="{cx+216}" y="{cy-10}" width="24" height="20" rx="4" fill="{NAVY}"/><rect x="{cx-10}" y="{cy-216}" width="20" height="20" rx="4" fill="{NAVY}"/><rect x="{cx-10}" y="{cy+196}" width="20" height="20" rx="4" fill="{NAVY}"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="186" fill="#DFF1F8" stroke="{NAVY}" stroke-width="5"/>'
rot=-35
tk=' '.join(f'M{pol(cx,cy,a+rot,168)[0]:.1f} {pol(cx,cy,a+rot,168)[1]:.1f} L{pol(cx,cy,a+rot,168-(20 if a%30==0 else 10))[0]:.1f} {pol(cx,cy,a+rot,168-(20 if a%30==0 else 10))[1]:.1f}' for a in range(0,360,10))
b+=f'<circle cx="{cx}" cy="{cy}" r="168" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="{tk}" stroke="{NAVY}" stroke-width="3"/>'
n1=pol(cx,cy,rot,130); s1=pol(cx,cy,rot+180,130); e1=pol(cx,cy,rot+90,26); w1=pol(cx,cy,rot-90,26)
b+=f'<polygon points="{n1[0]:.1f},{n1[1]:.1f} {e1[0]:.1f},{e1[1]:.1f} {s1[0]:.1f},{s1[1]:.1f} {w1[0]:.1f},{w1[1]:.1f}" fill="{NAVY}" fill-opacity="0.85"/>'
b+=f'<path d="M{n1[0]:.1f} {n1[1]:.1f} L{e1[0]:.1f} {e1[1]:.1f} L{cx} {cy} L{w1[0]:.1f} {w1[1]:.1f} Z" fill="{CORAL}"/>'
b+=line(cx,cy-190,cx,cy-150,CORAL,8)+f'<circle cx="{cx}" cy="{cy}" r="8" fill="{SUN}"/>'
b+=arrow(820,80,cx+6,cy-176,INK,3)+arrow(900,300,cx+200,cy,INK,3)+arrow(250,560,cx-120,cy+130,INK,3)+arrow(160,120,cx-226,cy-40,INK,3)
nl=pol(cx,cy,rot,150)
lbl=lab(X+830,Y+56,240,'Linea di fede',CORAL,24,900)+lab(X+910,Y+280,180,'Mortaio con liquido',INK,24,800)+lab(X+100,Y+564,300,'Rosa graduata',INK,24,800)+lab(X+30,Y+60,260,'Sospensione cardanica',INK,24,800)+lab(X+nl[0]-20,Y+nl[1]-8,40,'N',CORAL,26,900,'center')
txt=term('La rosa','Un galleggiante con sotto gli aghi magnetici e il quadrante da 0° a 360°: gli aghi puntano al Nord bussola.')+term('La linea di fede','Parallela all\'asse della barca, indica la prora: la prora si legge sotto la linea di fede.')+term('Liquido e cardano','Il liquido smorza colpi e vibrazioni; la sospensione cardanica tiene la bussola orizzontale.')
sec('bussola', head('Bussola · lo strumento','La bussola magnetica'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Bussola vista dall\'alto dentro la sagoma della barca: la rosa è girata e la linea di fede, allineata alla prua, indica la prora')+lbl,
 notes='Quiz 1.7.4-14 e -29 (rosa ed equipaggio magnetico), -12, -30, -46 (gli aghi puntano al Nord bussola), -33 (rosa da 0 a 360 in senso orario dal Nb), -31, -41, -44, -45 (linea di fede parallela all\'asse longitudinale, sotto si legge la prora), -36 (mantiene la prora), -28 (liquido), -49 (sospensione cardanica), -15 (a cosa serve la bussola). Il quiz 1.7.4-13 è oscurato. Nel disegno la barca ha prora bussola di circa 035°.')
X=700

# ============ TRE NORD ============
ox,oy=546,580
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
def arc(r,a0,a1,c,w=5):
    p0=pol(ox,oy,a0,r); p1=pol(ox,oy,a1,r)
    return f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
for a,c,w in ((0,NAVY,7),(12,SEA,7),(28,CORAL,7)):
    tip=pol(ox,oy,a,470); b+=arrow(ox,oy,tip[0],tip[1],c,w,26)
b+=arc(340,0,12,SEA,6)+arc(420,12,28,CORAL,6)+arc(230,0,28,PURPLE,6)
t0=pol(ox,oy,0,470); t1=pol(ox,oy,12,470); t2=pol(ox,oy,28,470)
ld=pol(ox,oy,6,380); lde=pol(ox,oy,20,460); lv=pol(ox,oy,14,200)
lbl=lab(X+t0[0]-230,Y+t0[1]-10,210,'Nv · Nord vero',NAVY,24,900,'right')+lab(X+t1[0]-70,Y+t1[1]-50,220,'Nm · magnetico',SEA,24,900)+lab(X+t2[0]+24,Y+t2[1]-6,240,'Nb · bussola',CORAL,24,900)
lbl+=lab(X+ld[0]-20,Y+ld[1]-20,40,'d',SEA,32,900,'center')+lab(X+lde[0]-10,Y+lde[1]-24,40,'δ',CORAL,32,900,'center')+lab(X+lv[0]+30,Y+lv[1]-20,150,'V = d + δ',PURPLE,24,900,bg='#FFFFFF')
txt=term('Declinazione d','Tra Nord vero e Nord magnetico. Dipende dal magnetismo terrestre, cambia con il luogo e con gli anni: si legge sulla carta.')+term('Deviazione δ','Tra Nord magnetico e Nord bussola. Nasce dai ferri e dagli apparati di bordo e cambia con la prora: si legge sulla tabella delle deviazioni residue.')+term('Variazione V','La somma d + δ. Su una barca senza masse ferrose è uguale alla declinazione.')
sec('trenord', head('Bussola · declinazione e deviazione','Tre nord')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Tre frecce da uno stesso punto: Nord vero, Nord magnetico spostato della declinazione, Nord bussola spostato ancora della deviazione')+lbl,
 notes='Quiz 1.7.4-17 e -21 (declinazione tra Nv e Nm), -19 (deviazione tra Nm e Nb), -18, -25, -32, -39 (declinazione: magnetismo terrestre, varia con luogo e tempo), -22 (si legge sulla carta), -23 (tra 0 e 180 E o W), -34 (Est positiva, Ovest negativa), -26 e -40 (deviazione: ferri duri e dolci, magnetismo di bordo), -42 (varia con la prora), -20, -24, -27, -43 (tabella delle deviazioni residue dopo i giri di bussola), -16 (li fa il perito compensatore), -37 (controllo: allineamenti, stella polare), -38 (segno della deviazione), -35, -47, -48 (senza masse ferrose Nb = Nm). Sulla carta 5/D la declinazione è riportata sulla rosa con l\'anno e la variazione annua.')

# ============ CONVERSIONI ============
formula=f'<div style="display:flex; gap:16px; align-items:center; flex-wrap:wrap">{chip("V = d + δ",PURPLE)}{chip("Pv = Pb + V",SEA)}{chip("Pb = Pv − V",CORAL)}{chip("Est + · Ovest −",NAVY)}</div>'
def exc(tagt,c,bg,rows,res):
    r=''.join(p(x,25,BODY) for x in rows)
    return card(note(tagt,c,34)+f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:22px">{r}</div>'+f'<p style="font-family:{H}; font-size:48px; font-weight:700; color:{c}">{res}</p>',None,28,14)
e1=exc('Esercizio 5.1.3-1',SEA,SEA_T,['Pb = 350°, d = 1° E, δ = 0°','V = +1°','Pv = 350° + 1°'],'Pv = 351°')
e2=exc('Esercizio 5.1.3-2',BLUE,BLUE_T,['Pb = 086°, d = 2° W, δ = −2°','V = −2° − 2° = −4°','Pv = 086° − 4°'],'Pv = 082°')
e3=exc('Al contrario',CORAL,CORAL_T,['Voglio Pv = 120°, V = +3°','Pb = Pv − V','Pb = 120° − 3°'],'Pb = 117°')
sec('conversioni', head('Bussola · il calcolo','Da bussola a vero e ritorno')+formula+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}</div>'+note('Stessa regola per i rilevamenti: Rilv = Rilb + V.',BLUE,38),
 notes='Esempi dagli esercizi ufficiali di carteggio (DD 131/2022): 5.1.3-1 (Pb 350°, d 1°E, δ 0° → Pv 351°) e 5.1.3-2 (Pb 086°, d 2°W, δ −2° → Pv 082°; lì anche Rilb 164° → Rilv 160°, Rilb 194° → Rilv 190°). Regola dei segni: Est positivo, Ovest negativo (quiz 1.7.4-34). In molti esercizi è data direttamente la variazione magnetica V (es. 5.1.2-2 e 5.1.3-3).')

quiz_slide('quiz3','Quiz 3 · Bussola',['1.7.4-17','1.7.4-42','1.7.4-26'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.7.4-17','1.7.4-42','1.7.4-26'],True)

# ============ PRORA E ROTTA
X=128
ox,oy=260,540
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=arrow(ox,oy,ox,70,NAVY,5,22)
pv=pol(ox,oy,40,520); rv=pol(ox,oy,55,560)
b+=arrow(ox,oy,pv[0],pv[1],NAVY,7,26)+dpath(f'M{ox} {oy} L{rv[0]:.0f} {rv[1]:.0f}',CORAL,6)
b+=curved(ox,oy,160,-90,-50,NAVY,4)+curved(ox,oy,230,-90,-35,CORAL,4)
b+=topboat(ox+150*math.sin(math.radians(40)),oy-150*math.cos(math.radians(40)),140,-50,'#FFFFFF',NAVY,4)
b+=''.join(arrow(x,y,x+90,y+60,GREY,7,22) for x,y in ((760,90),(860,170)))
lbl=lab(X+ox-40,Y+40,80,'N',NAVY,30,900,'center')+lab(X+pv[0]-240,Y+pv[1]-20,230,'Pv · prora vera',NAVY,26,900,'right')+lab(X+rv[0]+10,Y+rv[1]+30,300,'Rv · rotta vera',CORAL,26,900)+lab(X+880,Y+50,200,'vento e corrente',SOFT,22,800)
txt=term('Prora','La direzione della chiglia rispetto al Nord, da 0° a 360° in senso orario.')+term('Rotta vera Rv','Il percorso reale rispetto al fondo del mare. Due rotte opposte differiscono di 180°.')+term('Vp e Ve','Vp: velocità data dalle sole eliche. Ve: velocità effettiva rispetto al fondo.')+term('Quando coincidono','Pv = Rv solo se vento e corrente arrivano esattamente da prua o da poppa.')
sec('prorarotta', head('Carteggio · le parole','Prora e rotta'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Dallo stesso punto: la prora vera, dove punta la barca, e la rotta vera, spostata da vento e corrente')+lbl,
 notes='Quiz 1.7.7-4 e -8 (prora), -1, -2, -3 (rotta vera), -5 (rotte opposte 180°), -9 (si legge sulla rosa della carta), -11 e -15 (Vp dalle sole eliche), -17 (Ve rispetto al fondo), -13 (moto effettivo: Rv e Ve), -30 (Pv = Rv solo con vento o corrente da prora o da poppa), -28 (vento in poppa: cambia la velocità, non la direzione), -6 e -7 (Rv 090 cambia la longitudine, Rv 180 la latitudine). Il quiz 1.7.7-10 è oscurato.')
X=700

# ============ SCARROCCIO ============
ox,oy=520,560
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=''.join(arrow(80,y,220,y,GREY,8,24) for y in (160,260,360))
b+=arrow(ox,oy,ox,90,NAVY,7,26)
rv=pol(ox,oy,14,500); b+=dpath(f'M{ox} {oy} L{rv[0]:.0f} {rv[1]:.0f}',CORAL,6)
b+=curved(ox,oy,300,-90,-76,CORAL,5)
for k,(t) in enumerate((0.3,0.6)):
    x=ox+(rv[0]-ox)*t; y=oy+(rv[1]-oy)*t; b+=topboat(x,y,130,-90,'#FFFFFF',NAVY,3,0.9 if k else 0.5,k==1)
lbl=lab(X+60,Y+420,220,'vento da W',SOFT,26,900)+lab(X+ox-240,Y+80,220,'Pv 000°',NAVY,28,900,'right')+lab(X+rv[0]+10,Y+rv[1]+10,220,'Rv 014°',CORAL,28,900)+lab(X+ox+20,Y+200,260,'scarroccio +14°',CORAL,26,900,bg='#FFFFFF')
txt=term('Cos\'è','L\'angolo tra prora e rotta dovuto al vento.')+term('Il segno','Positivo se la barca scarroccia a dritta (vento da sinistra), negativo se va a sinistra.')+term('Da cosa dipende','Forza del vento, velocità, superficie esposta: più opera morta e meno opera viva, più scarroccio. Tocca tutte le barche.')+f'<div style="display:flex; gap:12px">{chip("Rv = Pv + Sc",SEA,30)}{chip("Pv = Rv − Sc",CORAL,30)}</div>'
sec('scarroccio', head('Carteggio · il vento','Lo scarroccio')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Barca con prora a Nord spinta da un vento da Ovest: la rotta vera piega a destra di 14 gradi')+lbl,
 notes='Quiz 1.7.7-12 e -26 (scarroccio dovuto al vento), -18 (positivo a dritta, negativo a sinistra), -19 e -23 (da cosa dipende: meno opera viva e più superficie esposta, più scarroccio), -21 (tocca tutte le unità). Le formule servono negli esercizi 5.x.4 (lezione 12).')

# ============ DERIVA
X=128
ox,oy=180,520
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
A=pol(ox,oy,40,560); Bp=(A[0]+230,A[1]+110)
b+=arrow(ox,oy,A[0],A[1],NAVY,7,26)+arrow(A[0],A[1],Bp[0],Bp[1],SEA,7,26)+dpath(f'M{ox} {oy} L{Bp[0]-14:.0f} {Bp[1]-8:.0f}',CORAL,6)+head_at(Bp[0],Bp[1],math.degrees(math.atan2(Bp[1]-oy,Bp[0]-ox)),CORAL,24)
b+=topboat(ox+60,oy-70,120,-50,'#FFFFFF',NAVY,4)
b+=''.join(f'<path d="M{x} {y} q18 -10 36 0 t36 0" fill="none" stroke="{SEA}" stroke-width="4" stroke-linecap="round"/>' for x,y in ((760,460),(820,510),(880,460)))
lbl=lab(X+30,Y+290,300,'Pv · Vp: il motore',NAVY,26,900,'right')+lab(X+A[0]+60,Y+A[1]-30,300,'corrente: Dc · Vc',SEA,26,900)+lab(X+560,Y+400,320,'Rv · Ve: sul fondo',CORAL,26,900)
txt=term('Cos\'è','L\'effetto della corrente sul moto della barca: l\'angolo di deriva è tra prora e rotta.')+term('Uguale per tutti','A parità di corrente la deriva non dipende dal tipo di scafo.')+term('Il triangolo','Moto propulsivo + moto della corrente = moto effettivo. Sulla carta si disegna come un triangolo di vettori.')
sec('deriva', head('Carteggio · la corrente','La deriva'), pinned=pcol(txt+note('Si risolve sulla carta nelle lezioni 9, 13, 14 e 15.',SEA,34))+svgp(X,Y,W,Hh,b,'Triangolo delle velocità: prora e velocità propulsiva, poi il vettore della corrente, e la risultante che è la rotta e la velocità effettive')+lbl,
 notes='Quiz 1.7.7-14, -25, -27 (deriva dovuta alla corrente), -24 (moto dovuto alle correnti), -16 (non dipende dallo scafo), -13 (moto effettivo Rv e Ve), -20 (vento apparente, somma vettoriale). Primo problema di corrente: lezione 9; esercizi 5.x.1 nelle lezioni 13-15.')
X=700

# ============ VENTO DA, CORRENTE VERSO ============
def wind_cur():
    s=f'<rect x="0" y="0" width="460" height="300" fill="{CHART}"/>'
    s+=arrow(120,40,120,250,GREY,10,30)+f'<circle cx="120" cy="30" r="10" fill="{GREY}"/>'
    s+=arrow(340,40,340,250,SEA,10,30)
    return s
wc=card(svgi(460,300,wind_cur(),'A sinistra il vento che arriva da Nord e va verso Sud; a destra la corrente che va verso Sud',dw=440,dh=287)
        +p('<b>Vento 000°</b> (Tramontana) arriva da Nord e soffia verso Sud. <b>Corrente 180°</b> va verso Sud.',25,INK),None,26,12)
ex=card(note('Esercizio 5.1.4-2',CORAL,36)+p('Voglio <b>Rv = 090°</b> con un vento di <b>Grecale</b> che dà <b>Sc = +10°</b>. Che prora tengo?',27,INK,700)
        +f'<div style="display:flex; flex-direction:column; gap:6px; background:{CORAL_T}; padding:18px; border-radius:22px">{p("Pv = Rv − Sc",25)}{p("Pv = 090° − 10°",25)}</div>'
        +f'<p style="font-family:{H}; font-size:52px; font-weight:700; color:{CORAL}">Pv = 080°</p>'+p('Si «orza»: si mette la prua un po\' verso il vento.',24),None,28,12)
rules=card(note('Da ricordare',PURPLE,36)+'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:12px"><li>Il vento si indica <b>da dove viene</b>, la corrente <b>verso dove va</b>.</li><li>Vento 180° e corrente 180°: il vento spinge verso Nord, la corrente verso Sud.</li><li>Rotta Nord con vento e corrente 180°: lo scarroccio aiuta, la deriva frena.</li></ul>',None,28,12)
sec('regole', head('Carteggio · attenzione ai versi','Vento «da», corrente «verso»')+f'<div style="display:flex; gap:24px">{wc}{ex}{rules}</div>',
 notes='Quiz 1.7.7-22 (vento 180 soffia verso nord, corrente 180 va verso sud), -29 (rotta Nord con vento e corrente 180: scarroccio favorevole, deriva contraria). Esempio dall\'esercizio ufficiale 5.1.4-2: Rv 090°, Grecale, Sc +10° → Pv 080°. Il Grecale da NE spinge la barca verso Sud, cioè a dritta rispetto a una prora a Est: per questo lo scarroccio è positivo.')

quiz_slide('quiz4','Quiz 4 · Prora, rotta, scarroccio',['1.7.7-12','1.7.7-22','1.7.7-18'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.7.7-12','1.7.7-22','1.7.7-18'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.4.3-24','1.4.2-15','1.7.4-19'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.4.3-24','1.4.2-15','1.7.4-19'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.7.7-14','1.7.7-30','1.4.3-51'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.7.7-14','1.7.7-30','1.4.3-51'],True)
closing(['Calumo: almeno 3 volte il fondale, da 3 a 5 con vento e mare','Prua al vento, cala a abbrivio finito, fila indietreggiando, controlla che faccia testa','Spiagge: oltre 200 m; corridoi di lancio a lento moto; sub a 100 m','V = d + δ; Pv = Pb + V; Est positivo, Ovest negativo','Scarroccio dal vento, deriva dalla corrente: il vento viene «da», la corrente va «verso»'],
 'Prossima lezione · 05 · Punto nave e fanali','A casa: i 53 quiz di ancoraggio, i 32 sulla navigazione costiera, i 49 sulla bussola e i 30 su prora e rotta.')
write_deck(OUT,'Lezione 04 · Ancoraggio, prora e rotta',
 ['cover','agenda','ancora','tipi','calumo','manovra','ruota','quiz1','quiz1r','costa','subacquei','quiz2','quiz2r',
  'bussola','trenord','conversioni','quiz3','quiz3r','prorarotta','scarroccio','deriva','regole','quiz4','quiz4r','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"L'ancoraggio: ancore, calumo, manovra, ruota e afforcamento","start":"ancora"},
  "s3":{"description":"Navigare vicino alla costa: balneazione, corridoi, subacquei","start":"costa"},"s4":{"description":"Bussola, declinazione, deviazione e conversioni","start":"bussola"},
  "s5":{"description":"Prora, rotta, scarroccio e deriva, verifica finale","start":"prorarotta"}})
