import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez02/project'
LB.ICON_T.update({'Le tipologie di eliche':'propeller','Fuoribordo, entrofuoribordo, entrobordo, idrogetto':'propeller','Il ciclo del diesel':'fuel','Inconvenienti del motore a scoppio':'cloud','Inconvenienti del motore diesel':'cloud','Destrorsa: effetto evolutivo':'propeller','Sinistrorsa: effetto evolutivo':'propeller','Effetto evolutivo e curva di evoluzione':'current','Timone a barra e timone a ruota':'helm','Cosa fa il timone':'helm','Tipi di timoni':'helm','Doppia linea d\'asse':'propeller','Ormeggi: elica e timone in manovra':'anchor','Fuoribordo: circuito aperto':'current','Entrobordo: circuito chiuso':'current','La lezione di oggi':'lifebuoy','Entrobordo, entrofuoribordo, fuoribordo, idrogetto':'propeller','Dal motore all\'elica':'propeller','S-DRIVE, IPS, POD e IDROGETTO':'propeller','Il ciclo a quattro tempi':'fuel',
 'Motore a benzina e motore diesel':'fuel','Il raffreddamento':'current','Benzina: miscela e scintilla':'fuel','Diesel: aria compressa e iniettori':'fuel','Fuoribordo: acqua di mare diretta':'current','Entrobordo: due circuiti e lo scambiatore':'current','Il motore ci parla: fumo e avviamento':'cloud','Il motore ci parla: in navigazione':'helm',
 'Carburante e manutenzione':'fuel','Quanto carburante imbarcare':'fuel','Autonomia e consumi':'chart','Mozzo, pale, passo e regresso':'propeller',
 'Elica destrorsa e sinistrorsa':'propeller','Spinta e velocità':'propeller','L\'effetto evolutivo dell\'elica':'current','Due motori, due eliche':'propeller','Il timone':'helm','Barra e ruota':'helm','Effetti combinati elica e timone':'anchor'})

# ============ FUNZIONI COMUNI ============
def nterm(n,t,d,c): return f'<div style="display:flex; gap:16px; align-items:start"><p style="flex:none; width:44px; font-family:{H}; font-size:26px; font-weight:700; line-height:44px; text-align:center; color:#FFFFFF; background:{c}; border-radius:22px">{n}</p><div style="display:flex; flex-direction:column; gap:2px">{p(t,26,INK,800,1.25)}{p(d,24,BODY,400,1.35)}</div></div>'
def tcol(x,items,extra=''): return f'<div style="position:absolute; left:{x}px; top:290px; width:532px; display:flex; flex-direction:column; gap:20px">{"".join(nterm(*i) for i in items)}{extra}</div>'
def tcol_inner(items): return f'<div style="display:flex; flex-direction:column; gap:16px">{"".join(nterm(*i) for i in items)}</div>'
FUEL=SUN; ELEC=PURPLE; GREY='#9AA5B1'; MIX='#9DB9F2'
MIR=lambda s,w: f'<g transform="translate({w} 0) scale(-1 1)">{s}</g>'
def legenda(items,c):
    li=''.join(f'<div style="display:flex; gap:12px; align-items:center"><p style="flex:none; width:36px; font-family:{H}; font-size:24px; font-weight:700; line-height:36px; text-align:center; color:#FFFFFF; background:{c}; border-radius:18px">{i+1}</p>{p(t,24,INK,700,1.2)}</div>' for i,t in enumerate(items))
    return f'<div style="display:flex; flex-direction:column; gap:4px">{li}</div>'
def boxn(title,body,c,bg):
    return f'<div style="display:flex; flex-direction:column; gap:4px; background:{bg}; border-left:10px solid {c}; border-radius:18px; padding:14px 20px">{p(title,26,c,800,1.2)}{p(body,24,BODY,400,1.35)}</div>'

# ============ COVER + AGENDA ============
cover(2,'Motori, elica e timone','Come funziona il motore, come spinge l\'elica, come governa il timone',
 'Lezione 2. Capitoli del programma della scuola: Motori ed Elica-Timone. All. A al DM 323/2021: materia 2 (motori, avarie, calcolo dell\'autonomia) e punto 1b (elica, timone). Ordine del manuale Il Frangente, cap. 1: motore e trasmissione, funzionamento, raffreddamento, irregolarità, elica, effetto evolutivo, timone, effetti combinati.')
blocks=[('0:00','25′','Cap. 1 · Il motore · verifica',CORAL),('0:25','15′','Cap. 2 · L\'elica · verifica',BLUE),('0:40','15′','Cap. 3 · Avarie e autonomia · verifica',PURPLE),('0:55','20′','Cap. 4 · Timone ed effetti combinati · verifica',SEA),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">1 + 1</p>'+p('domande su 20: una di Motori e una di Teoria dello scafo (elica e timone)',26,INK,700)+p('104 quiz ufficiali sui motori, di cui 27 sul calcolo dell\'autonomia; 50 su elica, timone e stabilità.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>riconoscere le installazioni del motore e la linea d\'asse</li><li>spiegare il ciclo a 4 tempi, benzina e diesel</li><li>capire cosa ti dice un motore che non va</li><li>calcolare carburante e autonomia con il 30% di riserva</li><li>prevedere l\'effetto dell\'elica e del timone</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 02 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro capitoli di teoria in 75 minuti, ognuno chiuso da una verifica da 2 quiz ufficiali (DD 131/2022): andare spediti sulle slide, il dettaglio è nelle note. Poi 45 minuti di raccolta quiz: 36 quiz ufficiali. Il capitolo dell\'Excel della scuola: motore marino, trasmissione, 4 tempi, diesel, raffreddamento EB/FB, inconvenienti; elica e timone.')

# ============ INSTALLAZIONI ============
def mini_hull(extra, stern_tall=False):
    s=f'<rect x="0" y="150" width="440" height="80" fill="{WATER}" fill-opacity="0.22"/>'+line(0,150,440,150,SEA,3)
    s+=f'<path d="M40 {96 if stern_tall else 108} L400 96 Q424 120 392 170 L96 176 L50 162 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
    s+=f'<path d="M47 150 L408 150 Q400 162 392 170 L96 176 L50 162 Z" fill="{CORAL}"/><path d="M46 144 L412 144" stroke="{BLUE}" stroke-width="6"/>'
    s+=f'<path d="M40 {96 if stern_tall else 108} L400 96 Q424 120 392 170 L96 176 L50 162 Z" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
    return s+extra
def prop_side(x,y,s=1,c=NAVY):
    return f'<ellipse cx="{x}" cy="{y-9*s}" rx="{5*s}" ry="{10*s}" fill="{c}"/><ellipse cx="{x}" cy="{y+9*s}" rx="{5*s}" ry="{10*s}" fill="{c}"/><circle cx="{x}" cy="{y}" r="{4*s}" fill="{SUN}"/>'
eng=lambda x,y,w=70,h=30,c=NAVY: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}"/><rect x="{x+8}" y="{y-8}" width="{w-16}" height="10" rx="3" fill="{SUN}"/>'
inst={
'entrobordo':mini_hull(eng(190,112)+line(196,134,110,190,'#7A8796',6)+prop_side(104,194)+f'<rect x="70" y="170" width="16" height="46" rx="4" fill="{NAVY}"/>'),
'entrofuoribordo':mini_hull(eng(60,112)+f'<path d="M58 126 L26 126 L22 200 L36 206 L40 132" fill="{SEA}" stroke="{NAVY}" stroke-width="3"/>'+prop_side(16,196)),
'fuoribordo':mini_hull(f'<rect x="6" y="54" width="40" height="46" rx="12" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><rect x="20" y="100" width="12" height="96" fill="{NAVY}"/><path d="M14 172 L40 172" stroke="{NAVY}" stroke-width="5"/>'+prop_side(12,196),True),
'idrogetto':mini_hull(eng(200,112)+f'<path d="M230 178 Q180 186 120 170 Q80 160 46 158" fill="none" stroke="{SEA}" stroke-width="12" stroke-linecap="round"/>'+''.join(line(40,158,6,150+i*6,'#FFFFFF',3) for i in range(3))+arrow(250,212,232,184,SEA,3)),
}
D={'fuoribordo':('Fuoribordo','Motore, trasmissione ed elica in un blocco sullo specchio di poppa. <b>Niente pala del timone</b>: il piede è propulsore e timone.'),
   'entrofuoribordo':('Entrofuoribordo','Motore <b>entro</b>bordo, organi di trasmissione <b>fuori</b>bordo nel <b>gruppo poppiero</b>. Niente pala del timone.'),
   'entrobordo':('Entrobordo','Motore dentro lo scafo, linea d\'asse ed elica. <b>C\'è la pala del timone</b>: l\'apparato propulsivo non è direzionabile.'),
   'idrogetto':('Idrogetto','Una pompa aspira l\'acqua e la spinge ad alta velocità da poppa; poco manovrabile al minimo.')}
cc=''.join(card(svgi(440,230,inst[k],f'Disegno di profilo: installazione {D[k][0].lower()}',dw=350,dh=183)+h3(D[k][0],30)+p(D[k][1],24),None,24,10) for k in D)
sec('installazioni', head('Il motore marino','Fuoribordo, entrofuoribordo, entrobordo, idrogetto')+f'<div style="display:flex; gap:24px">{cc}</div>'
 +note('Fuoribordo a gambo corto: carene piatte e plananti · a gambo lungo: carene a V, tonde e dislocanti. Il gambo va scelto sull\'altezza dello specchio di poppa.',PURPLE,32),
 notes='Quiz 1.2.1-12 (sistema propulsivo = motore + elica), 1.2.1-9 (entrofuoribordo), 1.2.1-45/46/47 (idrogetto: condotto di aspirazione, elica, condotto forzato, meccanismo di governo; difficile al minimo e con vento), 1.2.1-52/53/55/56 (IPS, pod, S-drive: sostituire la guarnizione del piedino alla scadenza).')

# ============ LINEA D'ASSE ============
X,Y,W,Hh=128,290,1092,620
b=f'<defs><clipPath id="la"><rect x="0" y="330" width="1092" height="400"/></clipPath></defs>'
hullp='M120 170 L1092 150 L1092 470 L120 360 Z'
b+=f'<rect x="0" y="330" width="1092" height="290" fill="{WATER}" fill-opacity="0.22"/>'
b+=f'<path d="{hullp}" fill="{BOAT}"/><path d="{hullp}" fill="{CORAL}" clip-path="url(#la)"/>'+line(0,330,1092,330,SEA,3)
b+=f'<path d="M120 170 L1092 150 M120 170 L120 360 L1092 470" fill="none" stroke="{NAVY}" stroke-width="5"/>'
b+=f'<rect x="640" y="250" width="230" height="120" rx="16" fill="{NAVY}"/>'+''.join(f'<rect x="{656+i*52}" y="226" width="40" height="28" rx="6" fill="{SUN}"/>' for i in range(4))
b+=f'<rect x="575" y="292" width="68" height="70" rx="10" fill="{SEA}"/>'
b+=line(578,338,210,454,'#7A8796',12)+f'<rect x="372" y="376" width="80" height="26" rx="8" fill="{PURPLE}" transform="rotate(-17.5 412 389)"/>'
b+=f'<rect x="524" y="332" width="34" height="40" rx="6" fill="{SUN}" stroke="{NAVY}" stroke-width="3" transform="rotate(-17.5 541 352)"/>'
b+=f'<rect x="461" y="342" width="50" height="52" rx="8" fill="#BFD3EE" stroke="{NAVY}" stroke-width="3" transform="rotate(-17.5 486 368)"/>'
b+=f'<rect x="444" y="360" width="14" height="36" rx="3" fill="{CORAL}" stroke="{NAVY}" stroke-width="2" transform="rotate(-17.5 451 378)"/>'
b+=f'<ellipse cx="200" cy="432" rx="12" ry="30" fill="{NAVY}"/><ellipse cx="200" cy="492" rx="12" ry="30" fill="{NAVY}"/><circle cx="202" cy="459" r="10" fill="{SUN}"/>'
b+=line(152,250,152,420,NAVY,6)+f'<path d="M140 400 L176 400 L176 520 Q160 530 140 520 Z" fill="{NAVY}"/>'
for (lx,ly,tx,ty) in [(760,120,755,222),(470,520,420,420),(280,570,215,500),(60,150,150,300)]: b+=arrow(lx,ly,tx,ty,INK,3)
b+=num(606,266,1,PURPLE)+num(548,300,2,PURPLE)+num(486,312,3,PURPLE)+num(380,344,4,PURPLE)
lbls=lab(X+690,Y+84,300,'Motore',INK)+lab(X+380,Y+524,260,'Asse portaelica',INK)+lab(X+250,Y+574,160,'Elica',INK)+lab(X+20,Y+110,170,'Timone',INK)
txt=f'<div style="position:absolute; left:1252px; top:290px; width:540px; display:flex; flex-direction:column; gap:20px">{p("<b>Linea d&#39;asse</b>: l&#39;insieme di organi meccanici che trasmettono il movimento dall&#39;albero motore all&#39;elica.",26,INK)}'+''.join(nterm(*i) for i in [
 (1,'Riduttore / invertitore','Sull&#39;albero motore: riduce i giri e dà avanti, folle, indietro. Il motore gira sempre nello stesso verso.',PURPLE),
 (2,'Giunto elastico','Collega il riduttore all&#39;asse e assorbe vibrazioni e piccoli disallineamenti.',PURPLE),
 (3,'Cuscinetto reggispinta','Trasmette allo scafo la spinta dell&#39;elica.',PURPLE),
 (4,'Astuccio con premistoppa','Dove l&#39;asse attraversa lo scafo: la premistoppa, o pressatrecce, non fa entrare l&#39;acqua.',PURPLE)])+'</div>'
sec('lineaasse', head('La linea d\'asse del motore entrobordo','Dal motore all\'elica')+txt, pinned=svgp(X,Y,W,Hh,b,'Spaccato di poppa: motore, albero motore con riduttore e invertitore, giunto elastico, cuscinetto reggispinta, astuccio con premistoppa, asse portaelica, elica e timone')+lbls,
 notes='Quiz 1.2.2-7 (linea d\'asse), 1.2.1-7 e -14 (invertitore: non si inverte la rotazione del motore), 1.2.1-42/43/44 (figure: astuccio, asse portaelica, invertitore/riduttore), 1.2.1-41 (paratia del vano motore). La premistoppa (o pressatrecce) stringe delle trecce attorno all\'asse: una goccia ogni tanto è normale e serve a lubrificarle; se entra un filo d\'acqua va stretta.')

X,Y,W,Hh=700,290,1092,620

# ============ TIPI DI TRASMISSIONE ============
def gear(x,y,r=7): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
def prop_front(x,y,s=1,c=NAVY):
    return prop_side(x,y,s,c)
def leg(x0,x1,ytop,ybot,w=16,c=SEA):
    return f'<path d="M{x0-w/2} {ytop} L{x0+w/2} {ytop} L{x1+w/2} {ybot} Q{x1} {ybot+10} {x1-w/2} {ybot} Z" fill="{c}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
tr={
'sdrive':mini_hull(f'<path d="M262 172 L300 170 L292 222 L276 224 Z" fill="{NAVY}"/>'+eng(140,114)
    +leg(176,176,168,208,18)+gear(176,178,6)+gear(176,204,6)+line(176,140,176,172,'#7A8796',5)
    +f'<rect x="162" y="166" width="28" height="7" rx="3" fill="{PURPLE}"/>'+prop_side(158,204)),
'ips':mini_hull(eng(80,112)+leg(150,160,172,208,18)+prop_side(178,204)+prop_side(190,204,0.8,SEA)
    +arrow(212,206,262,206,CORAL,4,12)+line(120,134,150,172,'#7A8796',5)),
'pod':mini_hull(eng(80,112)+leg(160,160,172,206,18)+prop_side(142,202)+line(120,134,160,172,'#7A8796',5)
    +f'<path d="M126 218 A36 10 0 0 0 196 218" fill="none" stroke="{CORAL}" stroke-width="4" stroke-linecap="round"/>'+head_at(196,216,-80,CORAL,12)),
'getto':mini_hull(eng(210,112)
    +f'<path d="M262 176 Q230 170 190 166 L90 160 L48 156" fill="none" stroke="{SEA}" stroke-width="14" stroke-linecap="round"/>'
    +prop_side(130,162,0.8)+arrow(290,214,262,182,SEA,3,11)
    +f'<path d="M44 146 L30 150 L30 166 L44 168" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
    +''.join(line(26,152+i*6,4,146+i*9,'#FFFFFF',3) for i in range(3))),
}
TR={'sdrive':('S-DRIVE','Un <b>piedino</b> sotto lo scafo con <b>due ingranaggi conici</b> porta il moto all\'elica al posto della linea d\'asse. Tipico delle <b>barche a vela</b>. La <b>guarnizione</b> del piedino si sostituisce alla scadenza stampata nella gomma.'),
    'ips':('IPS','<i>Inboard Performance System</i>: <b>piede completamente immerso</b> e orientabile, con eliche <b>traenti</b>, rivolte <b>verso prua</b>, e controrotanti.'),
    'pod':('POD','<b>Corpo trasmissione in un piede immerso</b> che <b>ruota</b> e orienta la prua della barca: il piede fa anche da timone. L\'IPS è un tipo di pod.'),
    'getto':('IDROGETTO','Una <b>pompa</b> mossa dal motore aspira acqua e la spinge ad alta velocità <b>da poppa</b>. Parti: condotto di aspirazione, elica, condotto forzato, meccanismo di governo. <b>Difficile al minimo dei giri e con vento</b>.')}
ALT={'sdrive':'Disegno di profilo di barca a vela: motore, piedino S-drive con due ingranaggi conici, guarnizione e elica',
     'ips':'Disegno di profilo: piede IPS immerso con due eliche rivolte verso prua che tirano la barca',
     'pod':'Disegno di profilo: piede pod immerso che ruota su se stesso per orientare la barca',
     'getto':'Disegno di profilo: l\'acqua entra dal fondo, passa per la pompa ed esce a getto da poppa'}
TC={'sdrive':PURPLE,'ips':SEA,'pod':BLUE,'getto':CORAL}
cc=''.join(card(svgi(440,230,tr[k],ALT[k],dw=350,dh=183)+h3(TR[k][0],30,TC[k])+p(TR[k][1],24),None,24,10) for k in TR)
sec('trasmissioni', head('Tipi di trasmissione','S-DRIVE, IPS, POD e IDROGETTO')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 1.2.1-55 (S-drive: piedino con due ingranaggi conici, sulle barche a vela al posto della linea d\'asse), 1.2.1-56 (S-drive: sostituire la guarnizione del piedino secondo la scadenza stampata nella gomma, non «ogni 15 anni»), 1.2.1-52 (IPS: piede completamente immerso, eliche traenti rivolte verso prua), 1.2.1-54 (figura: riconoscere la trasmissione IPS), 1.2.1-53 (pod: piede immerso che ruotando orienta la prua), 1.2.1-45/46/47 (idrogetto: getto da poppa con pompa mossa da un motore convenzionale; condotto di aspirazione, elica, condotto forzato e meccanismo di governo; difficile al minimo e con vento). Nel disegno dell\'S-drive la striscia viola è la guarnizione tra piedino e scafo: se cede, entra acqua.')

# ============ QUATTRO TEMPI ============
def cyl(stage):
    s=f'<rect x="0" y="0" width="300" height="300" rx="30" fill="#FFFFFF"/>'
    top={'asp':170,'com':96,'sco':160,'sca':100}[stage]
    gas={'asp':BLUE_T,'com':'#9DB9F2','sco':'#FFD28A','sca':'#D3D8DF'}[stage]
    s+=f'<rect x="94" y="64" width="112" height="{top-64}" fill="{gas}"/>'
    s+=f'<path d="M90 60 L90 220 M210 60 L210 220 M90 60 L210 60" stroke="{NAVY}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    iv=12 if stage=='asp' else 0; ev=12 if stage=='sca' else 0
    s+=line(118,14,118,60+iv,NAVY,5)+f'<rect x="102" y="{58+iv}" width="32" height="7" rx="3" fill="{NAVY}"/>'
    s+=line(182,14,182,60+ev,NAVY,5)+f'<rect x="166" y="{58+ev}" width="32" height="7" rx="3" fill="{NAVY}"/>'
    s+=f'<rect x="143" y="28" width="14" height="34" rx="4" fill="{SUN}"/>'
    s+=f'<rect x="96" y="{top}" width="108" height="36" rx="6" fill="{CORAL}"/>'
    pin=(150,294) if top>140 else (150,238)
    s+=f'<circle cx="150" cy="266" r="28" fill="none" stroke="{NAVY}" stroke-width="5"/>'+line(150,top+30,pin[0],pin[1],NAVY,8)+f'<circle cx="{pin[0]}" cy="{pin[1]}" r="7" fill="{SUN}"/>'
    if stage=='asp': s+=arrow(40,20,108,76,BLUE,6,18)+arrow(150,130,150,160,CORAL,5,14)
    if stage=='com': s+=arrow(150,190,150,140,CORAL,5,14)
    if stage=='sco': s+=f'<polygon points="150,62 160,86 186,82 166,100 176,124 150,110 124,124 134,100 114,82 140,86" fill="{SUN}" stroke="{CORAL}" stroke-width="3"/>'+arrow(150,128,150,158,CORAL,6,16)
    if stage=='sca': s+=arrow(192,76,262,20,SOFT,6,18)+arrow(150,190,150,140,CORAL,5,14)
    return s
st=[('asp','1 · Aspirazione','Si apre la valvola di aspirazione, il pistone scende e aspira miscela o aria.'),('com','2 · Compressione','Con le <b>valvole chiuse</b> il pistone sale e comprime.'),('sco','3 · Scoppio','La benzina si accende e spinge il pistone in basso: è la fase utile.'),('sca','4 · Scarico','Si apre la valvola di scarico e il pistone spinge fuori i gas combusti.')]
cc=''.join(card(svgi(300,300,cyl(k),f'Cilindro nella fase di {t.split(" · ")[1].lower()}',dw=240,dh=240)+h3(t,30)+p(d,24),None,24,10) for k,t,d in st)
sec('quattrotempi', head('Motori endotermici','Il ciclo a quattro tempi')+f'<div style="display:flex; gap:24px">'+boxn('Sistema propulsivo delle unità a motore','<b>motore + elica</b>',CORAL,CORAL_T)+boxn('Locale macchine (apparato motore)','l\'ambiente di bordo con i motori principali e i sistemi ausiliari',SEA,SEA_T)+'</div>'+f'<div style="display:flex; gap:24px">{cc}</div>'+note('Ciclo completo = 4 corse del pistone e 2 giri dell\'albero motore · le valvole sono nella testa dei cilindri',CORAL,36),
 notes='Quiz 1.2.1-6 e -33 (aspirazione, compressione, scoppio, scarico), 1.2.1-16 e -17 (2 giri dell\'albero, 4 corse del pistone). Nel diesel si aspira solo aria e il gasolio viene iniettato alla fine della compressione.')

# ============ MOTORE A BENZINA E DIESEL: SCHEMA A 4 CILINDRI ============
def engine4(kind):
    d = kind=='diesel'
    W_='#DDE3EA'; PIST='#6F9BD8'
    s=f'<rect x="300" y="236" width="580" height="300" rx="26" fill="{W_}" stroke="{NAVY}" stroke-width="4"/>'
    cx=[390,530,670,810]; top=[300,340,300,340]
    gas=(['#FFB38A','#FFFFFF','#FFB38A','#FFB38A'] if d else ['#FFB38A','#FFB38A','#BFE8C4','#BFE8C4'])
    for i,x in enumerate(cx):
        s+=f'<rect x="{x-50}" y="256" width="100" height="{top[i]-256}" fill="{gas[i]}"/>'
        s+=f'<path d="M{x-54} 256 L{x-54} 440 M{x+54} 256 L{x+54} 440" stroke="{NAVY}" stroke-width="6"/>'
        s+=f'<rect x="{x-50}" y="{top[i]}" width="100" height="66" rx="8" fill="{PIST}" stroke="{NAVY}" stroke-width="3"/>'+''.join(line(x-50,top[i]+12+j*10,x+50,top[i]+12+j*10,NAVY,3) for j in range(3))
        s+=line(x,top[i]+56,x+(14 if i%2 else -14),492,NAVY,12)
    s+=f'<path d="M250 500 L360 500 L376 {492} L404 492 L420 500 L500 500 L516 520 L544 520 L560 500 L640 500 L656 520 L684 520 L700 500 L780 500 L796 492 L824 492 L840 500 L950 500" fill="none" stroke="{NAVY}" stroke-width="16" stroke-linejoin="round"/>'
    s+=f'<ellipse cx="250" cy="500" rx="16" ry="60" fill="{PIST}" stroke="{NAVY}" stroke-width="4"/><ellipse cx="950" cy="500" rx="12" ry="34" fill="{PIST}" stroke="{NAVY}" stroke-width="4"/>'
    s+=f'<path d="M944 468 L944 132 M956 532 L956 150" stroke="{NAVY}" stroke-width="5"/>'
    s+=f'<rect x="770" y="60" width="160" height="110" rx="40" fill="#BFD3EE" stroke="{NAVY}" stroke-width="4"/><ellipse cx="950" cy="140" rx="10" ry="26" fill="{PIST}" stroke="{NAVY}" stroke-width="3"/>'
    s+=f'<rect x="30" y="500" width="170" height="90" rx="10" fill="{NAVY}"/><rect x="56" y="486" width="30" height="16" rx="4" fill="{SUN}"/><rect x="144" y="486" width="30" height="16" rx="4" fill="{CORAL}"/>'
    s+=f'<rect x="196" y="556" width="70" height="44" rx="14" fill="#BFD3EE" stroke="{NAVY}" stroke-width="3"/><path d="M200 560 L200 540 L160 540 L160 502" fill="none" stroke="{ELEC}" stroke-width="4"/>'
    if not d:
        s+=f'<rect x="120" y="60" width="90" height="120" rx="16" fill="#BFD3EE" stroke="{NAVY}" stroke-width="4"/>'+''.join(line(124,76+j*14,206,76+j*14,NAVY,3) for j in range(7))
        s+=f'<path d="M160 486 L160 440 L90 440 L90 120 L120 120" fill="none" stroke="{ELEC}" stroke-width="4" stroke-linejoin="round"/><path d="M165 60 L165 30 L560 30 L560 110" fill="none" stroke="{ELEC}" stroke-width="4" stroke-linejoin="round"/>'
        s+=f'<rect x="520" y="110" width="80" height="60" rx="18" fill="#BFD3EE" stroke="{NAVY}" stroke-width="4"/>'
        for x in cx:
            s+=f'<path d="M560 150 Q{(560+x)/2} 190 {x} 214" fill="none" stroke="{ELEC}" stroke-width="3"/><rect x="{x-9}" y="212" width="18" height="44" rx="4" fill="{NAVY}"/><rect x="{x-6}" y="200" width="12" height="16" rx="3" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'
        n=[(115,540,1),(280,604,2),(165,200,3),(640,130,4),(430,222,5),(810,290,6),(470,330,7),(470,382,8),(850,40,9),(600,560,10)]
    else:
        s+=f'<rect x="440" y="110" width="320" height="60" rx="18" fill="#BFD3EE" stroke="{NAVY}" stroke-width="4"/>'+''.join(f'<rect x="{470+j*72}" y="98" width="20" height="14" rx="3" fill="{NAVY}"/>' for j in range(4))
        for j,x in enumerate(cx):
            s+=f'<path d="M{480+j*72} 100 Q{(480+j*72+x)/2} 70 {x} 196" fill="none" stroke="{FUEL}" stroke-width="4"/><rect x="{x-9}" y="196" width="18" height="60" rx="4" fill="{NAVY}"/>'
            s+=f'<path d="M{x-44} 204 L{x-26} 262" stroke="{SUN}" stroke-width="8" stroke-linecap="round"/><circle cx="{x-25}" cy="264" r="8" fill="{CORAL}" fill-opacity="0.7"/>'
        s+=f'<path d="M160 486 L160 440 L90 440 L90 204 L{cx[-1]-44} 204" fill="none" stroke="{ELEC}" stroke-width="4" stroke-linejoin="round"/>'
        n=[(115,540,1),(280,604,2),(600,70,3),(810,290,4),(470,330,5),(430,178,6),(470,382,7),(850,40,8),(600,560,9),(318,262,10)]
    s+=''.join(num(x,y,k,CORAL if not d else SEA,17) for x,y,k in n)
    return s
def legenda(items,c):
    li=''.join(f'<div style="display:flex; gap:12px; align-items:center"><p style="flex:none; width:36px; font-family:{H}; font-size:24px; font-weight:700; line-height:36px; text-align:center; color:#FFFFFF; background:{c}; border-radius:18px">{i+1}</p>{p(t,24,INK,700,1.2)}</div>' for i,t in enumerate(items))
    return f'<div style="display:flex; flex-direction:column; gap:4px">{li}</div>'
def boxn(title,body,c,bg):
    return f'<div style="display:flex; flex-direction:column; gap:4px; background:{bg}; border-left:10px solid {c}; border-radius:18px; padding:14px 20px">{p(title,26,c,800,1.2)}{p(body,24,BODY,400,1.35)}</div>'
# --- benzina: schema a destra ---
X,Y,W,Hh=700,290,1092,620
leg=legenda(['Batteria','Motorino di avviamento','Bobina','Sistema di accensione','Candela','Cilindro: miscela aria/benzina','Pistone','Fasce elastiche','Alternatore','Albero motore'],CORAL)
txt=f'<div style="position:absolute; left:128px; top:290px; width:540px; display:flex; flex-direction:column; gap:16px">{p("Impianto elettrico <b>complesso</b>",26,INK,800)}{leg}{boxn("Obbligo di aerazione","Vapori di benzina nel vano: <b>aerare prima di avviare</b>.",CORAL,CORAL_T)}</div>'
sec('benzina', head('Motore a scoppio · benzina','Benzina: miscela e scintilla')+txt, pinned=svgp(X,Y,W,Hh,engine4('benzina'),'Schema di un motore a benzina a quattro cilindri: batteria, motorino di avviamento, bobina, sistema di accensione con i cavi alle candele, cilindri con la miscela, pistoni con le fasce elastiche, albero motore, alternatore mosso dalla cinghia'),
 notes='Quiz 1.2.1-18 (il sistema di accensione esiste solo nei motori a scoppio), 1.2.1-2 e -3 (vapori di benzina: aerare il vano prima di avviare; l\'impianto di aerazione del vano di un entrobordo a benzina è obbligatorio). Impianto elettrico complesso: batteria e motorino di avviamento come nel diesel, in più bobina e sistema di accensione (spinterogeno o accensione elettronica) che mandano la scintilla alla candela del cilindro giusto. Nel disegno i cilindri arancio sono in scoppio, quelli verdi contengono miscela aria/benzina. Le fasce elastiche tengono la tenuta tra pistone e cilindro; l\'alternatore, mosso da una cinghia dall\'albero motore, ricarica la batteria. Il carburatore (oggi spesso l\'iniezione elettronica) prepara la miscela.')

# --- diesel: schema a sinistra ---
X,Y,W,Hh=128,290,1092,620
leg=legenda(['Batteria','Motorino di avviamento','Pompa di iniezione del gasolio','Cilindro: solo aria','Pistone','Iniettore','Fasce elastiche','Alternatore','Albero motore','Candelette a incandescenza'],SEA)
txt=f'<div style="position:absolute; left:1252px; top:290px; width:540px; display:flex; flex-direction:column; gap:16px">{p("Impianto elettrico <b>semplice</b>",26,INK,800)}{leg}{boxn("Aerazione consigliata","Punto di infiammabilità elevato: aerazione non obbligatoria.",SEA,SEA_T)}</div>'
sec('diesel', head('Motore diesel','Diesel: aria compressa e iniettori')+txt, pinned=svgp(X,Y,W,Hh,engine4('diesel'),'Schema di un motore diesel a quattro cilindri: batteria, motorino di avviamento, pompa di iniezione con i tubi agli iniettori, candelette a incandescenza, cilindri con sola aria, pistoni con fasce elastiche, albero motore, alternatore'),
 notes='Quiz 1.2.1-5 (aerazione forzata del vano diesel: non obbligatoria ma consigliata), -32 (gasolio: punto di infiammabilità più elevato), -49 (pompa di alimentazione, pompa di iniezione, iniettori), -48 (un iniettore per cilindro), -29 (l\'iniettore nebulizza il gasolio), -50 (candeletta a incandescenza nell\'iniezione indiretta), -15 (batteria essenziale per l\'avviamento), -1 (si spegne togliendo il gasolio alla pompa di iniezione). Impianto elettrico semplice: il diesel non ha bobina, sistema di accensione e candele; la batteria serve al motorino e alle candelette. Nel disegno i cilindri arancio sono in combustione, quello bianco è in aspirazione di aria.')

# ============ DIESEL 4 TEMPI ============
def cyld(stage):
    s=f'<rect x="0" y="0" width="300" height="300" rx="30" fill="#FFFFFF"/>'
    top={'asp':170,'com':96,'sco':160,'sca':100}[stage]
    gas={'asp':'#CFE3FB','com':'#F6B26B','sco':'#FFD28A','sca':'#D3D8DF'}[stage]
    s+=f'<rect x="94" y="64" width="112" height="{top-64}" fill="{gas}"/>'
    s+=f'<path d="M90 60 L90 220 M210 60 L210 220 M90 60 L210 60" stroke="{NAVY}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    iv=12 if stage=='asp' else 0; ev=12 if stage=='sca' else 0
    s+=line(118,14,118,60+iv,NAVY,5)+f'<rect x="102" y="{58+iv}" width="32" height="7" rx="3" fill="{NAVY}"/>'
    s+=line(182,14,182,60+ev,NAVY,5)+f'<rect x="166" y="{58+ev}" width="32" height="7" rx="3" fill="{NAVY}"/>'
    s+=f'<rect x="142" y="18" width="16" height="46" rx="4" fill="{NAVY}"/>'
    s+=f'<rect x="96" y="{top}" width="108" height="36" rx="6" fill="{CORAL}"/>'
    pin=(150,294) if top>140 else (150,238)
    s+=f'<circle cx="150" cy="266" r="28" fill="none" stroke="{NAVY}" stroke-width="5"/>'+line(150,top+30,pin[0],pin[1],NAVY,8)+f'<circle cx="{pin[0]}" cy="{pin[1]}" r="7" fill="{SUN}"/>'
    if stage=='asp': s+=arrow(40,20,108,76,BLUE,6,18)+arrow(150,130,150,160,CORAL,5,14)
    if stage=='com': s+=arrow(150,190,150,140,CORAL,5,14)
    if stage=='sco': s+=''.join(line(150,68,150+dx,110,SUN,4) for dx in (-34,-17,0,17,34))+f'<path d="M112 120 Q150 96 188 120" fill="none" stroke="{CORAL}" stroke-width="5"/>'+arrow(150,128,150,158,CORAL,6,16)
    if stage=='sca': s+=arrow(192,76,262,20,SOFT,6,18)+arrow(150,190,150,140,CORAL,5,14)
    return s
st=[('asp','1 · Aspirazione','Entra <b>solo aria</b>: il pistone scende.'),('com','2 · Compressione','Valvole chiuse: l&#39;aria compressa arriva a <b>700–800 °C</b>.'),('sco','3 · Espansione','L&#39;iniettore spruzza il gasolio, che <b>si accende da solo</b> e spinge il pistone.'),('sca','4 · Scarico','Il pistone spinge fuori i gas combusti.')]
cc=''.join(card(svgi(300,300,cyld(k),f'Cilindro diesel nella fase di {t.split(" · ")[1].lower()}',dw=300,dh=300)+h3(t,30)+p(d,24),None,24,10) for k,t,d in st)
sec('diesel4t', head('Motore diesel · 4 tempi','Il ciclo del diesel')+f'<div style="display:flex; gap:24px">{cc}</div>'+note('Ciclo completo = 2 giri dell&#39;albero motore · olio lubrificante ad alta viscosità e densità',SEA,38),
 notes='Quiz 1.2.1-35 (lubrificante per diesel: conta la viscosità o densità), -29 (l\'iniettore nebulizza il gasolio), 1.2.1-16 e -17 (2 giri dell\'albero, 4 corse del pistone). Differenze dal benzina: si aspira solo aria, la compressione è molto più forte e scalda l\'aria a 700–800 °C (valore della scheda della scuola: il valore esatto dipende dal motore), il gasolio iniettato si accende da solo senza candela. Per questo la terza fase si chiama espansione, non scoppio.')

# ============ BENZINA / DIESEL ============
plug=f'<rect x="0" y="0" width="260" height="160" rx="26" fill="#FFFFFF"/><rect x="100" y="16" width="60" height="40" rx="8" fill="{NAVY}"/><rect x="108" y="56" width="44" height="40" fill="#E9EEF3" stroke="{NAVY}" stroke-width="3"/><rect x="118" y="96" width="24" height="26" fill="#7A8796"/><path d="M130 122 L130 134 L144 134" fill="none" stroke="{NAVY}" stroke-width="5"/><polygon points="150,126 160,136 150,146 156,136" fill="{SUN}"/><polygon points="164,122 176,138 162,150" fill="{SUN}"/>'
inj=f'<rect x="0" y="0" width="260" height="160" rx="26" fill="#FFFFFF"/><rect x="110" y="10" width="40" height="70" rx="8" fill="{NAVY}"/><path d="M118 80 L142 80 L134 108 L126 108 Z" fill="#7A8796"/>'+''.join(line(130,110,130+dx,150,'#9DB9F2',4) for dx in (-40,-20,0,20,40))
cb=card(f'<div style="display:flex; gap:20px; align-items:center">{svgi(260,160,plug,"Candela di accensione con la scintilla",pan=False)}<div>{h3("Benzina",34)}{tag("motore a scoppio",CORAL)}</div></div>'
 +'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:8px"><li>La miscela si accende con la <b>candela</b>: il sistema di accensione esiste solo nei motori a scoppio.</li><li>Il pericolo principale: i <b>vapori di benzina</b> che si accumulano nel vano motore.</li><li>Prima di avviare un entrobordo a benzina: <b>aerare il vano motore</b>.</li></ul>',None,30,14)
cd=card(f'<div style="display:flex; gap:20px; align-items:center">{svgi(260,160,inj,"Iniettore che nebulizza il gasolio",pan=False)}<div>{h3("Diesel",34)}{tag("accensione per compressione",SEA)}</div></div>'
 +'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:8px"><li>Alimentazione: <b>pompa di alimentazione, pompa di iniezione, iniettori</b> (uno per cilindro) che nebulizzano il gasolio.</li><li>Iniezione indiretta: servono le <b>candelette</b>. La batteria è essenziale per l\'avviamento.</li><li>Si spegne togliendo il carburante alla pompa di iniezione. Gasolio: punto di infiammabilità più alto.</li></ul>',None,30,14)
sec('benzinadiesel', head('Due motori a confronto','Motore a benzina e motore diesel')+f'<div style="display:flex; gap:24px">{cb}{cd}</div>'+note('1 kW = 1,36 CV · aerazione forzata del vano diesel: consigliata, non obbligatoria',PURPLE,34),
 notes='Quiz 1.2.1-2, -3 (vapori, aerare il vano), -18 (accensione solo nei motori a scoppio), -29, -48, -49 (iniettori, alimentazione diesel), -50 (candelette), -15 (batteria), -1 (spegnimento diesel), -32 (infiammabilità), -5 (aerazione forzata diesel non obbligatoria), -30 (1 kW = 1,36 CV).')

# ============ RAFFREDDAMENTO: FUORIBORDO ============
X,Y,W,Hh=700,290,1092,620
b=f'<rect x="0" y="330" width="1092" height="290" fill="{WATER}" fill-opacity="0.22"/>'+line(0,330,1092,330,SEA,3)
b+=f'<path d="M1092 150 L800 166 L800 400 Q900 440 1092 450 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
b+=f'<rect x="720" y="150" width="80" height="44" rx="8" fill="{NAVY}"/>'
b+=f'<rect x="590" y="200" width="64" height="214" fill="#E9EEF3" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<rect x="510" y="54" width="220" height="156" rx="44" fill="#F3F6F9" stroke="{NAVY}" stroke-width="5"/><rect x="556" y="84" width="130" height="100" rx="14" fill="#DDE3EA"/>'
b+=''.join(f'<path d="M566 {100+i*22} q14 -8 28 0 t28 0 t28 0 t28 0" fill="none" stroke="{SEA}" stroke-width="4"/>' for i in range(4))
b+=f'<rect x="672" y="70" width="30" height="24" rx="5" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
b+=f'<rect x="530" y="412" width="190" height="12" rx="4" fill="{NAVY}"/>'
b+=f'<path d="M586 424 L660 424 L664 470 L700 486 Q704 520 660 522 L560 522 Q540 506 556 486 L582 470 Z" fill="#E9EEF3" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=''.join(f'<rect x="{600+i*12}" y="442" width="6" height="22" rx="3" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>' for i in range(4))
b+=prop_side(540,500,2.4)
b+=f'<path d="M622 440 L622 196" stroke="{SEA}" stroke-width="8"/>'+head_at(622,300,-90,SEA,16)+head_at(622,236,-90,SEA,16)
b+=f'<circle cx="622" cy="386" r="22" fill="#FFFFFF" stroke="{SEA}" stroke-width="5"/>'+''.join(line(622,386,622+16*math.cos(a),386+16*math.sin(a),SEA,3) for a in [0,1.05,2.1,3.14,4.19,5.24])
b+=f'<path d="M512 150 Q470 170 450 250 Q444 290 446 326" fill="none" stroke="{WATER}" stroke-width="7" stroke-linecap="round"/><path d="M512 158 Q480 180 466 250" fill="none" stroke="{WATER}" stroke-width="4" stroke-linecap="round" stroke-dasharray="8 8"/>'
b+=''.join(f'<circle cx="{470-i*34}" cy="{500+((-1)**i)*10}" r="{9-i}" fill="#FFFFFF" stroke="{SOFT}" stroke-width="2"/>' for i in range(5))
b+=num(750,444,1,SEA)+num(560,370,2,SEA)+num(420,150,3,SEA)
b+=f'<circle cx="180" cy="160" r="104" fill="#FFFFFF" stroke="{DSOFT}" stroke-width="3"/>'+''.join(f'<path d="M180 160 m-10 -26 Q{180-6} {160-86} {180+28} {160-92} Q{180+14} {160-60} 190 134 Z" fill="#2B2F36" transform="rotate({a} 180 160)"/>' for a in range(0,360,40))+f'<circle cx="180" cy="160" r="30" fill="{NAVY}"/><circle cx="180" cy="160" r="10" fill="{SUN}"/>'
lbls=lab(X+772,Y+430,220,'Prese d\'acqua',INK)+lab(X+670,Y+356,120,'Girante',SEA)+lab(X+40,Y+272,300,'Girante: pompa a depressione',INK)+lab(X+744,Y+26,170,'Termostato',INK)+lab(X+300,Y+190,130,'Spia',SEA,align='right')+lab(X+250,Y+540,300,'Acqua e gas di scarico escono dal mozzo',SOFT)
txt=tcol(128,[(1,'Prese d\'acqua sul piede','Aspirano l\'acqua di mare, che passa <b>direttamente</b> nel motore (circuito aperto) ed esce con lo scarico.',SEA),
 (2,'Girante','<b>Pompa a depressione</b> ad acqua, con palette di gomma: se gira a secco, con la presa fuori dall\'acqua, si rompe.',SEA),
 (3,'Spia','<b>Fuoriuscita costante di fiotti d\'acqua</b>: il raffreddamento funziona. Niente getto: spegnere.',GREEN),
 ('!','Surriscaldamento','Cause: prese ostruite, girante rotta, presa fuori dall\'acqua. Danni: <b>grippaggio</b>, testata e guarnizioni.',CORAL)])
sec('raffreddamento', head('L\'impianto di raffreddamento','Fuoribordo: circuito aperto')+txt, pinned=svgp(X,Y,W,Hh,b,'Motore fuoribordo di profilo: prese d\'acqua sul piede, girante nella gamba, condotti nel blocco motore con termostato, getto della spia e scarico dal mozzo dell\'elica')+lbls,
 notes='Quiz 1.2.1-37 (figura: le prese d\'acqua sul piede), -38 (figura: la spia, il getto che testimonia il corretto funzionamento del circuito), -4 (girante danneggiata se il motore gira con la presa fuori dall\'acqua), 1.2.2-11 e -26 (alghe o plastica sulla presa: surriscaldamento e arresto), -25 (surriscaldamento prolungato: grippaggio, danni alla testata e alle sue guarnizioni). Dopo l\'uso in mare, lavare il circuito con acqua dolce con l\'apposito attacco o le «cuffie».')

# ============ RAFFREDDAMENTO: ENTROBORDO ============
X,Y,W,Hh=128,290,1092,620
b=f'<rect x="0" y="530" width="1092" height="90" fill="{WATER}" fill-opacity="0.22"/><path d="M0 520 L1040 520 L1040 180" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/><rect x="1040" y="440" width="52" height="180" fill="{WATER}" fill-opacity="0.22"/>'
b+=f'<rect x="138" y="506" width="24" height="28" fill="{NAVY}"/><rect x="136" y="456" width="28" height="40" rx="6" fill="{NAVY}"/><rect x="164" y="466" width="48" height="10" rx="4" fill="{CORAL}"/>'
b+=f'<rect x="120" y="300" width="60" height="110" rx="12" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'+''.join(line(128,318+i*14,172,318+i*14,SOFT,2) for i in range(6))
b+=f'<path d="M150 456 L150 410 M150 300 L150 250 L212 250 M268 250 L300 250 L300 150 L330 150" fill="none" stroke="{SEA}" stroke-width="8" stroke-linejoin="round"/>'
b+=f'<circle cx="240" cy="250" r="30" fill="#FFFFFF" stroke="{SEA}" stroke-width="6"/>'+''.join(line(240,250,240+20*math.cos(a),250+20*math.sin(a),SEA,4) for a in [0,1.05,2.1,3.14,4.19,5.24])
b+=f'<rect x="330" y="112" width="220" height="72" rx="36" fill="{SUN_T}" stroke="{SUN}" stroke-width="5"/>'+''.join(line(350,132+i*16,530,132+i*16,SEA,3) for i in range(3))
b+=f'<rect x="420" y="80" width="40" height="34" rx="6" fill="{CORAL}"/><rect x="428" y="70" width="24" height="12" rx="3" fill="{NAVY}"/>'
b+=f'<path d="M540 118 L540 50 L880 50 L880 236" fill="none" stroke="{SEA}" stroke-width="8" stroke-linejoin="round"/>'
b+=f'<rect x="580" y="210" width="240" height="170" rx="20" fill="{NAVY}"/>'+''.join(f'<rect x="{596+i*56}" y="190" width="40" height="24" rx="6" fill="{SUN}"/>' for i in range(4))
b+=f'<path d="M550 164 L640 164 L640 212" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linejoin="round"/><rect x="626" y="176" width="28" height="22" rx="4" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
b+=f'<path d="M580 330 L470 330 M406 330 L380 330 L380 184" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linejoin="round"/><circle cx="438" cy="330" r="30" fill="#FFFFFF" stroke="{CORAL}" stroke-width="6"/>'+''.join(line(438,330,438+18*math.cos(a),330+18*math.sin(a),CORAL,4) for a in [0,1.57,3.14,4.71])
b+=f'<path d="M608 250 q20 -10 40 0 t40 0 t40 0 t40 0 t40 0 M608 300 q20 -10 40 0 t40 0 t40 0 t40 0 t40 0" fill="none" stroke="{CORAL}" stroke-width="5"/>'
b+=f'<path d="M820 260 L880 260" stroke="{GREY}" stroke-width="16" stroke-linecap="round"/><circle cx="880" cy="250" r="16" fill="{SEA}"/>'
b+=f'<path d="M880 266 L880 330" stroke="{GREY}" stroke-width="16"/><rect x="840" y="330" width="100" height="110" rx="22" fill="#DDE3EA" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M940 380 L1000 380 L1000 470 L1040 470" fill="none" stroke="{GREY}" stroke-width="14" stroke-linejoin="round"/>'+arrow(1044,470,1086,470,SEA,5,14)
b+=num(90,380,1,SEA)+num(310,70,2,SEA)+num(438,384,3,CORAL)
lbls=lab(X+220,Y+452,330,'Presa a mare: acqua fredda',INK)+lab(X+190,Y+324,110,'Filtro',INK)+lab(X+130,Y+118,160,'Pompa 1',SEA,align='right')+lab(X+398,Y+262,130,'Pompa 2',CORAL)+lab(X+860,Y+540,230,'Acqua calda in uscita',CORAL)+lab(X+384,Y+196,180,'Scambiatore',SUN)+lab(X+616,Y+320,190,'Motore','#FFFFFF')+lab(X+830,Y+448,150,'Marmitta',INK)
txt=tcol(1260,[(1,'Presa a mare e pompa 1','La girante aspira l\'acqua di mare fredda, attraverso valvola e filtro.',SEA),
 (2,'Scambiatore di calore','L\'acqua di mare raffredda il <b>liquido del circuito chiuso</b>, poi esce calda con lo scarico.',SEA),
 (3,'Circuito chiuso e pompa 2','<b>Liquido specifico</b>, rabboccabile con acqua dolce, nelle <b>intercapedini</b> di testa e monoblocco.',CORAL),
 ('!','Da controllare','Allo scarico <b>fiotti d\'acqua costanti</b>: tutto bene. <b>Presa a mare occlusa</b>: surriscaldamento.',CORAL)])
sec('raffreddamentoeb', head('L\'impianto di raffreddamento','Entrobordo: circuito chiuso')+txt, pinned=svgp(X,Y,W,Hh,b,'Schema del raffreddamento entrobordo: presa a mare con valvola, filtro, pompa con girante, scambiatore di calore con vaso di espansione, circuito chiuso del motore con termostato e pompa di circolazione, acqua di mare che esce con lo scarico attraverso la marmitta')+lbls,
 notes='Quiz 1.2.1-13 (lo scambiatore raffredda il fluido del circuito chiuso con l\'acqua di mare), -8 (causa più comune di surriscaldamento: presa a mare della pompa occlusa), 1.1.1-64 (passascafo). Nel disegno l\'azzurro è l\'acqua di mare (circuito aperto), l\'arancio il liquido di raffreddamento (circuito chiuso, con il termostato giallo sul motore e il tappo del vaso di espansione sullo scambiatore). Alcuni entrobordo piccoli hanno il raffreddamento diretto, come il fuoribordo. Dopo una lunga navigazione: lasciar raffreddare il motore e controllare il livello dell\'olio (1.2.1-36).')

quiz_slide('quiz1','Quiz 1 · Il motore',['1.2.1-6', '1.2.1-14'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.2.1-6', '1.2.1-14'],True)

# ============ INCONVENIENTI: MOTORE A SCOPPIO E DIESEL ============
def sym(t,cs,c):
    li=''.join(f'<li>{x}</li>' for x in cs)
    return f'<div style="display:flex; flex-direction:column; gap:2px">{p(t,25,c,800,1.25)}<ul style="font-size:24px; line-height:1.32; color:{BODY}; display:flex; flex-direction:column; gap:2px">{li}</ul></div>'
def colsym(items,c): return f'<div style="flex:1.15; display:flex; flex-direction:column; gap:18px">{"".join(sym(t,cs,c) for t,cs in items)}</div>'
face=(f'<rect x="0" y="0" width="220" height="190" rx="30" fill="none"/><circle cx="110" cy="110" r="70" fill="{SUN}" stroke="{CORAL}" stroke-width="4"/>'
 f'<path d="M48 70 Q110 10 172 70 L172 84 L48 84 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><path d="M104 46 L116 46 M110 40 L110 62" stroke="{NAVY}" stroke-width="3"/>'
 f'<circle cx="84" cy="110" r="17" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><circle cx="136" cy="110" r="17" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'+line(101,110,119,110,INK,5)
 +f'<circle cx="84" cy="112" r="6" fill="{INK}"/><path d="M128 112 Q136 104 144 112" fill="none" stroke="{INK}" stroke-width="4"/><path d="M84 144 Q110 166 136 144" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><rect x="102" y="150" width="16" height="12" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
def bubble(inner,c): return f'<div style="flex:0.9; display:flex; flex-direction:column; align-items:center; gap:10px">{svgi(220,190,face,"Il marinaio del corso con gli occhiali",pan=False)}<div style="display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border:4px solid {c}; border-radius:28px; padding:22px 26px">{inner}</div></div>'
cL=colsym([('Non si avvia e le luci del quadro si spengono',['Batteria scarica']),
  ('Non si avvia',['Carburatore sporco o ingolfato','Candele deteriorate','Invertitore con la marcia inserita']),
  ('Gira ma non parte',['Mancato afflusso di carburante']),
  ('Si ferma di colpo: in folle resta acceso, in marcia si spegne',['Asse portaelica o elica bloccati'])],CORAL)
cR=colsym([('Fumo azzurro',['Olio lubrificante nella camera di scoppio']),
  ('Fumo nero',['Carburante sporco','Filtri aria e carburante sporchi','Carburatore sporco','Cattiva combustione e carburazione']),
  ('Dopo una lunga navigazione',['Far raffreddare il motore, controllare e se serve rabboccare l&#39;olio'])],CORAL)
bb=bubble(p('I motori a <b>benzina</b> hanno:',26,INK)+'<ul style="font-size:26px; line-height:1.35; color:#1B2A41; font-weight:800"><li>carburatore</li><li>candele</li></ul>'+p('Perdono colpi e «sputacchiano» quando c&#39;è dello <b>sporco</b>.',26,INK),CORAL)
sec('avariescoppio', head('Irregolarità e piccole avarie','Inconvenienti del motore a scoppio')+f'<div style="display:flex; gap:32px">{cL}{bb}{cR}</div>',
 notes='Quiz 1.2.2-6 (non parte e le luci si spengono: batterie scariche), -14 (benzina non parte: carburante che non arriva, carburatore sporco o ingolfato, candele deteriorate), 1.2.2-1 (gira ma non parte: carburatore ingolfato; quesito oscurato), -4 e -5 (asse o elica bloccati), -9 (fumo azzurro: olio in camera di scoppio), -10 e -15 (fumo nero), 1.2.1-36 (dopo una lunga navigazione: olio a motore raffreddato), 1.2.2-12 (fuoribordo che non parte: leva in folle). Il fumo nero o grigio con pompa di iniezione e filtro aria è un quiz sul diesel (1.2.2-18): lo trovate nella slide degli inconvenienti del diesel.')
cL=colsym([('Gira ma non parte, o si spegne subito dopo l&#39;accensione',['Aria nella pompa di iniezione: <b>spurgare</b>','Aria nel circuito del carburante','Filtro del carburante intasato']),
  ('Si avvia con difficoltà',['Aria nel circuito: spurgare','Acqua nel carburante','Tubo di scarico ostruito','Tubi degli iniettori deformati o rotti']),
  ('Picchia in testa',['Iniettori starati'])],SEA)
cR=colsym([('Perde colpi e cala di giri',['Carburante sporco: alghe nel serbatoio, pulirlo periodicamente']),
  ('Acqua nel serbatoio',['Rabbocco con carburante scadente: filtro separatore']),
  ('Vibra troppo',['Supporti del motore rotti o allentati']),
  ('Fumo blu o bianco',['Filtro dell&#39;olio intasato, turbina di sovralimentazione']),
  ('Fumo nero o grigio',['Pompa di iniezione, filtro dell&#39;aria intasato'])],SEA)
bb=bubble(p('I <b>diesel</b> non hanno carburatore e candele. Hanno:',26,INK)+'<ul style="font-size:26px; line-height:1.35; color:#1B2A41; font-weight:800"><li>iniettori</li><li>candelette a incandescenza</li></ul>'+p('Il guaio più comune: <b>aria nel circuito di alimentazione</b>.',26,INK)+p('«Ottani» e «stop difettoso» nei quiz? <b>Risposta sbagliata!</b>',26,CORAL,700),SEA)
sec('avariediesel', head('Irregolarità e piccole avarie','Inconvenienti del motore diesel')+f'<div style="display:flex; gap:32px">{cL}{bb}{cR}</div>',
 notes='Quiz 1.2.2-3, -8, -16 (aria nel circuito o nella pompa di iniezione, filtro intasato), 1.2.1-10 (spurgare), 1.2.2-17 (avvio difficile: acqua nel carburante, scarico ostruito), -20 e -21 (tubi degli iniettori), -2 (picchia in testa: iniettori fuori taratura), 1.2.1-11 (perde colpi: carburante sporco), -57 e -58 (alghe e pulizia del serbatoio), 1.2.2-23 e -24 (acqua nel serbatoio, filtro separatore), -22 (vibrazioni: supporti), -19 (fumo blu o bianco), -18 (fumo nero o grigio). Nei quiz sul diesel le risposte con «numero di ottani», «comando di stop difettoso» o «carburatore» sono sempre sbagliate.')

# funzioni per le icone delle schede di manutenzione
def smoke(c,edge=None):
    e=f' stroke="{edge}" stroke-width="3"' if edge else ''
    return f'<rect x="0" y="0" width="100" height="100" rx="24" fill="#F4F7FA"/><rect x="10" y="66" width="30" height="16" rx="4" fill="#7A8796"/><circle cx="52" cy="58" r="14" fill="{c}"{e}/><circle cx="66" cy="40" r="18" fill="{c}"{e}/><circle cx="80" cy="22" r="14" fill="{c}"{e}/>'
def ico(kind):
    base=f'<rect x="0" y="0" width="100" height="100" rx="24" fill="#F4F7FA"/>'
    if kind=='key': return base+f'<circle cx="34" cy="50" r="16" fill="none" stroke="{NAVY}" stroke-width="7"/><path d="M50 50 L86 50 M76 50 L76 64 M86 50 L86 62" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/><path d="M66 18 L74 30 M80 14 L80 28 M92 22 L84 32" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>'
    if kind=='temp': return base+f'<rect x="42" y="14" width="16" height="54" rx="8" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="50" cy="76" r="14" fill="{CORAL}"/><rect x="46" y="30" width="8" height="46" fill="{CORAL}"/>'
    if kind=='vib': return base+f'<rect x="32" y="34" width="36" height="32" rx="6" fill="{NAVY}"/>'+''.join(f'<path d="M{x} 30 q6 10 0 20 t0 20" fill="none" stroke="{CORAL}" stroke-width="4"/>' for x in (18,82))
    if kind=='prop': return base+f'<g transform="translate(10 10) scale(0.8)"><circle cx="50" cy="50" r="9" fill="{NAVY}"/>'+''.join(f'<ellipse cx="50" cy="25" rx="11" ry="20" fill="{NAVY}" transform="rotate({a} 50 50)"/>' for a in (0,120,240))+f'</g><path d="M20 20 L80 80 M80 20 L20 80" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/>'
    if kind=='drop': return base+f'<path d="M50 14 Q76 50 72 64 Q66 86 50 86 Q34 86 28 64 Q24 50 50 14 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="4"/><circle cx="44" cy="62" r="5" fill="{NAVY}"/><circle cx="58" cy="70" r="4" fill="{NAVY}"/>'
    if kind=='bang': return base+f'<polygon points="50,12 58,36 84,30 66,50 84,70 58,64 50,88 42,64 16,70 34,50 16,30 42,36" fill="{SUN}" stroke="{CORAL}" stroke-width="4"/>'
    if kind=='batt': return base+f'<rect x="18" y="34" width="60" height="36" rx="6" fill="none" stroke="{NAVY}" stroke-width="6"/><rect x="78" y="44" width="8" height="16" fill="{NAVY}"/><rect x="24" y="40" width="10" height="24" fill="{CORAL}"/>'
    if kind=='air': return base+''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{SEA}" stroke-width="4"/>' for x,y,r in [(32,62,12),(58,40,16),(72,70,9)])
def av(icon, t, d):
    return card(f'<div style="display:flex; gap:20px; align-items:start">{svgi(100,100,icon,"",pan=False)}<div style="display:flex; flex-direction:column; gap:6px">{h3(t,28)}{p(d,24)}</div></div>',None,24,8)
# ============ MANUTENZIONE ============
m=av(ico('air'),'Spurgare','Eliminare tutta l\'aria dal circuito del gasolio prima di riavviare il diesel.')+av(ico('drop'),'Acqua nel serbatoio','Viene da un rabbocco con carburante di scarsa qualità: monta un filtro separatore.')+av(ico('drop'),'Alghe nel gasolio','Il gasolio favorisce le alghe: pulisci spesso il serbatoio e cambia i filtri.')
m+=av(ico('temp'),'Dopo una lunga navigazione','A motore raffreddato controlla il livello dell\'olio e rabbocca.')+av(ico('bang'),'Il buon lubrificante','Conta la viscosità, cioè la densità.')+av(ico('key'),'Fuoribordo che non parte','Controlla che la leva delle marce sia in folle.')
sec('manutenzione', head('Prevenire è meglio','Carburante e manutenzione')+f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px">{m}</div>',
 notes='Quiz 1.2.1-10 (spurgare), 1.2.2-23 e -24 (acqua nel serbatoio, filtro separatore), 1.2.1-57 e -58 (alghe nel gasolio), 1.2.1-36 (olio dopo lunga navigazione), -35 (viscosità), 1.2.2-12 (leva in folle).')

# ============ CARBURANTE ============
def chip(t,c): return f'<p style="font-family:{H}; font-size:36px; font-weight:700; color:#FFFFFF; background:{c}; padding:14px 26px; border-radius:40px">{t}</p>'
op=lambda t: f'<p style="font-family:{H}; font-size:44px; font-weight:700; color:{INK}">{t}</p>'
formula=f'<div style="display:flex; gap:18px; align-items:center; flex-wrap:wrap">{chip("tempo = miglia ÷ nodi",SEA)}{op("→")}{chip("litri = l/h × ore",PURPLE)}{op("+")}{chip("30% di riserva",CORAL)}</div>'
ex=card(note('Esempio · quiz 1.2.3-7',CORAL,38)+p('<b>180 miglia</b> a <b>30 nodi</b> con un consumo di <b>31 litri all\'ora</b>.',28,INK)
 +f'<div style="display:flex; gap:20px">'+''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{bg}; padding:20px; border-radius:24px">{p(a,24,SOFT,800)}<p style="font-family:{H}; font-size:48px; font-weight:700; color:{INK}">{b}</p>{p(c,24)}</div>' for a,b,c,bg in [('1 · tempo','6 ore','180 ÷ 30',SEA_T),('2 · consumo','186 litri','31 × 6',LILAC_T),('3 · con la riserva','≈ 242 litri','186 + 30%',CORAL_T)])+'</div>',None,30,16,flex='none')
sec('carburante', head('Calcolo dell\'autonomia','Quanto carburante imbarcare')+formula+ex+p('Il 30% in più copre vento, corrente e mare: è la buona regola marinara richiesta dai quiz.',26,BODY),
 notes='Quiz 1.2.3-1 (30%), 1.2.2-6 (motivo: vento e corrente), 1.2.2-8 e 1.2.3-5 (consumo orario × tempo), 1.2.3-7 (180 mg, 30 kn, 31 l/h → 242 l). Altri esempi ufficiali: 1.2.2-7 (150 mg, 25 kn, 40 l/h → 312 l), 1.2.3-9…-14 (per ore di moto), 1.2.3-15…-21 (sola riserva: es. 90 mg a 30 kn e 28 l/h → 3 h × 28 = 84 l, riserva 30% ≈ 25 l).')

# ============ AUTONOMIA ============
g=f'<rect x="0" y="0" width="420" height="300" rx="30" fill="#FFFFFF"/><path d="M60 230 A150 150 0 0 1 360 230" fill="none" stroke="#E6EAF0" stroke-width="34"/>'
g+=f'<path d="M60 230 A150 150 0 0 1 104 124" fill="none" stroke="{CORAL}" stroke-width="34"/><path d="M104 124 A150 150 0 0 1 210 80" fill="none" stroke="{SUN}" stroke-width="34"/><path d="M210 80 A150 150 0 0 1 360 230" fill="none" stroke="{GREEN}" stroke-width="34"/>'
g+=line(210,230,130,130,NAVY,8)+f'<circle cx="210" cy="230" r="16" fill="{NAVY}"/><text x="46" y="270" font-family="Arial" font-size="30" font-weight="700" fill="{CORAL}">R</text><text x="352" y="270" font-family="Arial" font-size="30" font-weight="700" fill="{GREEN}">P</text>'
e1=card(tag('Autonomia in tempo',SEA)+p('<b>30 litri</b> con un consumo di <b>20 l/h</b>: 90 minuti di moto. Tenendo la riserva del 30%, circa <b>69 minuti</b>.',26,INK),None,28,10)
e2=card(tag('Consumo dalla potenza',PURPLE)+p('Fuoribordo 2 tempi da <b>80 HP</b> che consuma 300 g per HP all\'ora: 24 kg/h. Con 0,75 kg per litro: <b>32 litri all\'ora</b>.',26,INK),None,28,10)
e3=card(tag('Cosa riduce l\'autonomia',CORAL)+p('Mare mosso (a pari velocità si fanno meno miglia), dislocamento complessivo, velocità di crociera. Il consumo dichiarato è quello alla potenza massima.',26,INK),None,28,10,flex='none')
sec('autonomia', head('Calcolo dell\'autonomia','Autonomia e consumi')+f'<div style="display:flex; gap:28px; align-items:start">{svgi(420,300,g,"Indicatore del carburante con la zona di riserva in rosso",pan=False)}<div style="flex:1; display:flex; flex-direction:column; gap:18px">{e1}{e2}</div></div>'+e3,
 notes='Quiz 1.2.3-6 (30 l, 20 l/h → 90 min, con il 30% circa 69 min), 1.2.3-2 (80 HP × 0,3 kg = 24 kg/h ÷ 0,75 = 32 l/h), 1.2.2-3 (autonomia dalla potenza e dal peso specifico), 1.2.3-3 (mare mosso), 1.2.2-28 e -29 (fattori), 1.2.2-5 (consumo a potenza massima).')

quiz_slide('quiz2','Quiz 3 · Avarie e autonomia',['1.2.2-9', '1.2.3-7'],False)
quiz_slide('quiz2r','Quiz 3 · Le risposte',['1.2.2-9', '1.2.3-7'],True)

# ============ ELICA ============
pf=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/><circle cx="140" cy="130" r="112" fill="none" stroke="{BLUE}" stroke-width="3"/><g transform="translate(140 130)">'+''.join(f'<path d="M0 0 Q-34 -40 -8 -104 Q30 -96 22 -22 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" transform="rotate({a})"/>' for a in (0,120,240))+f'<circle r="22" fill="{NAVY}"/><circle r="7" fill="{SUN}"/></g>'
pf+=f'<path d="M28 130 L252 130" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 6"/>'
pf+=f'<circle cx="318" cy="130" r="14" fill="{NAVY}"/><ellipse cx="362" cy="120" rx="46" ry="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3" transform="rotate(-6 318 130)"/><ellipse cx="362" cy="140" rx="46" ry="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3" transform="rotate(6 318 130)"/>'
def helix(x0,per,col,y0=178,amp=40):
    pts=' '.join(f'{x0+per*t/40:.1f},{y0-amp*math.sin(2*math.pi*t/40):.1f}' for t in range(41))
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="9 6"/>'
def blade(x,y,c): return f'<ellipse cx="{x}" cy="{y-18}" rx="7" ry="17" fill="{c}" stroke="{NAVY}" stroke-width="2"/><ellipse cx="{x}" cy="{y+18}" rx="7" ry="17" fill="{c}" stroke="{NAVY}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="5" fill="{NAVY}"/>'
tx=lambda x,y,t,c,a='middle': f'<text x="{x}" y="{y}" text-anchor="{a}" font-family="Arial" font-size="23" font-weight="700" fill="{c}">{t}</text>'
ph=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/>'
ph+=f'<path d="M50 126 L390 126 M50 230 L390 230" stroke="{DSOFT}" stroke-width="3"/><ellipse cx="50" cy="178" rx="16" ry="52" fill="#E1EAFD" stroke="{DSOFT}" stroke-width="3"/><ellipse cx="390" cy="178" rx="16" ry="52" fill="none" stroke="{DSOFT}" stroke-width="3"/>'
ph+=line(40,178,400,178,'#7A8796',6)
ph+=helix(60,300,BLUE)+helix(60,240,CORAL)
ph+=blade(60,178,SUN)+blade(300,178,CORAL)+blade(360,178,BLUE)
ph+=dim(60,44,360,44,BLUE)+tx(210,30,'passo teorico',BLUE)
ph+=dim(60,98,300,98,CORAL)+tx(180,84,'passo effettivo',CORAL)
ph+=dim(300,98,360,98,GREEN)+tx(372,84,'regresso',GREEN,'middle')
ph+=f'<path d="M300 104 L300 150 M360 50 L360 150" stroke="{SOFT}" stroke-width="2" stroke-dasharray="4 4"/>'
pc=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/><g transform="translate(200 130)">'+''.join(f'<path d="M0 0 Q-34 -40 -8 -104 Q30 -96 22 -22 Z" fill="{NAVY}" transform="rotate({a})"/>' for a in (20,140,260))+f'<circle r="20" fill="{SEA}"/></g>'+''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{SEA}" stroke-width="3"/>' for x,y,r in [(300,60,10),(330,100,7),(320,150,12),(350,190,8),(290,210,6),(110,60,8),(90,190,10)])
pb=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/><path d="M110 260 L110 120 Q110 40 210 14 Q310 40 310 120 L310 260 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="5"/>'
pb+=f'<rect x="110" y="96" width="200" height="30" fill="{DSOFT}" stroke="{NAVY}" stroke-width="3"/><g transform="translate(210 111)">'+''.join(f'<ellipse cx="0" cy="-8" rx="5" ry="9" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+'</g>'
pb+=arrow(116,111,24,111,SEA,6,18)+arrow(304,111,396,111,SEA,6,18)+f'<text x="210" y="220" text-anchor="middle" font-family="Arial" font-size="26" font-weight="700" fill="{SOFT}">prua ↑</text>'
e1=card(svgi(420,260,pf,'Elica a pale fisse vista da dietro, con il cerchio del diametro; a destra un&#39;elica a pale abbattibili chiusa',dw=350,dh=217)+h3('Mozzo, pale, diametro',30)+p('Pale fisse, orientabili o <b>abbattibili</b> (a destra, chiuse): scarso rendimento in marcia indietro.',24),None,24,10)
e2=card(svgi(420,260,ph,'Il percorso della punta della pala in un giro: il passo teorico in blu è più lungo del passo effettivo in rosso; la differenza, in verde, è il regresso',dw=350,dh=217)+h3('Passo e regresso',30)+p('In un giro l&#39;elica avanzerebbe del <b>passo teorico</b> (blu) se l&#39;acqua fosse solida; avanza del <b>passo effettivo</b> (rosso). La differenza è il <b>regresso</b> (verde): elevato a bassa velocità e con molti giri.',24),None,24,10)
e3=card(svgi(420,260,pc,'Elica circondata da bolle: la cavitazione',dw=350,dh=217)+h3('Cavitazione',30)+p('Elica fuori giri, <b>niente spinta</b>. Cause: <b>detriti sulle pale</b> (anche vibrazioni) o piede di lunghezza non corretta.',24),None,24,10)
e4=card(svgi(420,260,pb,'Prua vista dall&#39;alto con il tunnel trasversale dell&#39;elica di prua e le frecce della spinta verso dritta e sinistra',dw=350,dh=217)+h3('Elica di prua',30)+p('<b>Bow thruster</b>: un&#39;elica in un tunnel trasversale spinge la prua a dritta o a sinistra. Aiuta in manovra e all&#39;ormeggio.',24),None,24,10)
sec('elica', head('Elica: acciaio, alluminio, composito','Mozzo, pale, passo e regresso')+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}{e4}</div>',
 notes='Quiz 1.2.1-31 (mozzo e pale), -34 (materiali), 1.1.2-1 (pale abbattibili, minor rendimento indietro), -16 (passo teorico), -11 (regresso), -24 e 1.2.2-13 (cavitazione, lunghezza del piede), 1.2.2-27 (alghe o detriti sull\'elica: vibrazioni). Nel disegno del passo: in blu il passo teorico (un giro in «acqua solida»), in rosso il passo effettivo, in verde il regresso; le linee tratteggiate sono il percorso della punta della pala in un giro. Il regresso cresce quando la barca va piano e l\'elica gira forte, per esempio in partenza o con carena sporca. L\'elica di prua (bow thruster) non è nei quiz ma è ormai comune anche sulle barche da diporto.')

# ============ SPINTA E VELOCITÀ ============
X,Y,W,Hh=128,290,1092,370
b=f'<rect x="0" y="130" width="1092" height="55" fill="{WATER}" fill-opacity="0.22"/>'+line(0,130,1092,130,SEA,3)+f'<rect x="0" y="318" width="1092" height="52" fill="{WATER}" fill-opacity="0.22"/>'+line(0,318,1092,318,SEA,3)+line(0,185,1092,185,'#FFFFFF',6)
b+=f'<path d="M70 104 L340 104 Q362 106 350 128 Q326 168 250 170 L100 170 Q70 162 70 130 Z" fill="#F08A3C" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/><path d="M72 124 L352 124" stroke="{NAVY}" stroke-width="6"/>'
b+=f'<rect x="150" y="62" width="120" height="42" rx="6" fill="#F08A3C" stroke="{NAVY}" stroke-width="4"/><rect x="186" y="32" width="60" height="32" rx="4" fill="#F08A3C" stroke="{NAVY}" stroke-width="4"/><rect x="200" y="42" width="32" height="14" fill="#FFFFFF"/>'+line(216,32,216,6,NAVY,4)+line(204,16,228,16,NAVY,3)
b+=prop_side(64,150,2.3)+line(70,150,110,150,'#7A8796',6)
b+=f'<rect x="430" y="40" width="34" height="56" rx="10" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/><rect x="464" y="54" width="200" height="28" rx="4" fill="#C9D1DA" stroke="{NAVY}" stroke-width="3"/>'+''.join(line(470+i*10,54,478+i*10,82,NAVY,2) for i in range(19))
b+=f'<path d="M80 306 L400 292 Q380 282 330 276 L150 278 Q100 282 80 306 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/><path d="M150 288 L360 284" stroke="{SUN}" stroke-width="8"/><rect x="200" y="266" width="70" height="14" rx="6" fill="{NAVY}"/>'
b+=prop_side(70,318,1.1)+line(74,316,96,308,'#7A8796',4)
b+=f'<path d="M430 250 L464 238 L464 280 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/><rect x="464" y="248" width="200" height="22" rx="4" fill="#C9D1DA" stroke="{NAVY}" stroke-width="3"/>'+''.join(line(480+i*34,248,494+i*34,270,NAVY,3) for i in range(5))
lbls=lab(X+700,Y+30,380,'Rimorchiatore = spinta',INK,28,800)+lab(X+700,Y+72,380,'diametro grande, passo corto',CORAL,24,700)+lab(X+700,Y+220,380,'Offshore = velocità',INK,28,800)+lab(X+700,Y+262,380,'diametro piccolo, passo lungo',CORAL,24,700)
chip=lambda t,s,c: f'<div style="display:flex; flex-direction:column; align-items:center; gap:2px; background:#FFFFFF; border:3px solid {c}; border-radius:22px; padding:10px 18px"><p style="font-family:{H}; font-size:40px; font-weight:700; line-height:1.1; color:{c}">{t}</p><p style="font-size:24px; color:{BODY}">{s}</p></div>'
op=lambda t: f'<p style="font-family:{H}; font-size:44px; font-weight:700; color:{INK}">{t}</p>'
ctitle=p('<b>Velocità teorica = passo × giri dell\'elica</b>. Il regresso la riduce.',26,INK)
calc=f'<div style="position:absolute; left:128px; top:690px; width:1092px; display:flex; flex-direction:column; gap:14px; background:{SUN_T}; border-radius:28px; padding:22px 28px">{ctitle}<div style="display:flex; gap:14px; align-items:center">{chip("0,5 m","passo",PURPLE)}{op("×")}{chip("2.000","giri al minuto",PURPLE)}{op("=")}{chip("32 nodi","teorici",BLUE)}{op("−20%")}{chip("26 nodi","reali",CORAL)}</div></div>'
txt=tcol(1260,[(1,'La pala è un\'ala','Ruotando, ogni pala ha una faccia in pressione e una in depressione, come un\'ala: <b>spinge l\'acqua verso poppa</b>.',CORAL),
 (2,'La spinta','L\'acqua accelerata verso poppa spinge <b>per reazione</b> la barca in avanti. In retromarcia l\'elica rende meno.',CORAL),
 (3,'Rimorchiatore = spinta','Elica di <b>diametro grande e passo corto</b>, come una vite a passo fitto: barche pesanti e dislocanti.',CORAL),
 (4,'Offshore = velocità','Elica di <b>diametro piccolo e passo lungo</b>, come una vite a passo largo: barche plananti veloci.',CORAL)])
sec('spinta', head('L\'elica · come spinge','Spinta e velocità')+txt+calc, pinned=svgp(X,Y,W,Hh,b,'In alto un rimorchiatore con una grande elica e una vite a passo fitto; in basso un offshore con una piccola elica e una vite a passo largo')+lbls,
 notes='Quiz 1.1.2-17 (passo lungo e diametro piccolo: più velocità), 1.1.2-16 e -11 (passo teorico e regresso), 1.1.2-24 (cavitazione: oltre il limite dei giri si perde la spinta). Il conto: 0,5 m × 2.000 giri/min = 1.000 m al minuto = 60 km/h ≈ 32,4 nodi teorici; con il 20% di regresso ≈ 26 nodi reali. I giri sono quelli dell\'elica, cioè del motore divisi per il rapporto del riduttore. Il regresso dipende da carena, carico e mare: sulle barche veloci è intorno al 10–20%, sulle dislocanti anche di più.')

# ============ ROTAZIONE ============
def sternview(cw):
    s=f'<path d="M110 30 L450 30 C450 120 380 170 280 180 C180 170 110 120 110 30 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="5"/><path d="M118 110 Q280 190 442 110 L450 130 C400 176 340 186 280 186 C220 186 160 176 110 130 Z" fill="{CORAL}" fill-opacity="0.9"/>'
    s+=line(280,180,280,214,NAVY,8)+f'<g transform="translate(280 250)">'+''.join(f'<ellipse cx="0" cy="-26" rx="12" ry="26" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+f'<circle r="10" fill="{SUN}"/></g>'
    s+=curved(280,250,70,-150,-30,SEA if cw else CORAL,7) if cw else curved(280,250,70,-30,-150,CORAL,7)
    return s
r1=card(svgi(560,340,sternview(True),'Vista da poppa: elica che gira in senso orario',dw=560,dh=340)+h3('Destrorsa',32)+p('Guardando la poppa dall\'esterno, in <b>marcia avanti</b> gira in senso <b>orario</b>; in marcia indietro in senso antiorario.',25),None,26,10)
r2=card(svgi(560,340,sternview(False),'Vista da poppa: elica che gira in senso antiorario',dw=560,dh=340)+h3('Sinistrorsa',32)+p('Guardando la poppa dall\'esterno, in <b>marcia avanti</b> gira in senso <b>antiorario</b>.',25),None,26,10)

# ============ EFFETTO EVOLUTIVO (vista dall'alto) ============
def evo(reverse):
    s=''
    rot = 18 if reverse else -18
    s+=topboat(300,230,300,-90+rot,'#FFFFFF',NAVY,3,0.35,False)
    s+=topboat(300,230,300,-90,'#FFFFFF',NAVY,4)
    s+=f'<g transform="translate(300 392)">'+''.join(f'<ellipse cx="0" cy="-10" rx="6" ry="12" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+'</g>'
    if reverse:
        s+=curved(300,230,190,100,128,CORAL,7)+curved(300,230,190,-80,-52,SEA,7)+arrow(470,300,470,420,'#97A6B4',8,26)
    else:
        s+=curved(300,230,190,80,52,CORAL,7)+curved(300,230,190,-100,-128,SEA,7)+arrow(470,420,470,300,'#97A6B4',8,26)
    return s
v1=card(svgi(600,480,evo(False),'Vista dall\'alto, marcia avanti con elica destrorsa: la poppa va a dritta e la prua a sinistra',dw=560,dh=448)+h3('Marcia avanti · destrorsa',30)+p('Timone al centro: <b>la poppa va a dritta</b>, la prua a sinistra.',25),None,24,10)
v2=card(svgi(600,480,evo(True),'Vista dall\'alto, marcia indietro con elica destrorsa: la poppa va a sinistra',dw=560,dh=448)+h3('Marcia indietro · destrorsa',30)+p('<b>La poppa va a sinistra</b>, la prua a dritta. Con la sinistrorsa, tutto al contrario.',25),None,24,10)
v3=card(note('Da ricordare',PURPLE,40)+'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:12px"><li>L\'effetto è <b>massimo senza abbrivio e con la marcia inserita</b>.</li><li>Nasce dalla spinta laterale delle pale e dal flusso d\'acqua contro timone e carena.</li><li>Si compensa con il <b>timone</b>.</li><li>In marcia indietro è più forte: usalo in manovra.</li></ul>',None,30,12)
# ============ TIPOLOGIE DI ELICHE ============
BL='M0 0 Q-34 -40 -8 -104 Q30 -96 22 -22 Z'
def pr(cx,cy,sc,n,c=CORAL,off=0):
    return f'<g transform="translate({cx} {cy}) scale({sc})">'+''.join(f'<path d="{BL}" fill="{c}" stroke="{NAVY}" stroke-width="{4/sc:.1f}" transform="rotate({off+i*360/n})"/>' for i in range(n))+f'<circle r="20" fill="{NAVY}"/><circle r="7" fill="{SUN}"/></g>'
PB='<rect x="0" y="0" width="220" height="170" rx="24" fill="#FFFFFF"/>'
tp={
'fisso':PB+pr(110,88,0.72,3),
'abbatt':PB+f'<g opacity="0.35">'+pr(70,88,0.5,2,CORAL,90)+'</g>'+f'<circle cx="130" cy="88" r="12" fill="{NAVY}"/><ellipse cx="170" cy="78" rx="40" ry="8" fill="{SUN}" stroke="{NAVY}" stroke-width="3" transform="rotate(-6 130 88)"/><ellipse cx="170" cy="98" rx="40" ry="8" fill="{SUN}" stroke="{NAVY}" stroke-width="3" transform="rotate(6 130 88)"/>'+arrow(96,58,126,72,SOFT,3,10),
'orient':PB+pr(110,88,0.72,3,SEA)+curved(110,30,26,200,340,CORAL,5)+curved(66,118,24,40,180,CORAL,5),
'npale':PB+pr(40,88,0.34,2)+pr(110,88,0.34,3)+pr(180,88,0.34,4)+''.join(f'<text x="{x}" y="160" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700" fill="{INK}">{t}</text>' for x,t in ((40,'2'),(110,'3'),(180,'4'))),
'contro':PB+line(10,88,210,88,'#7A8796',8)+f'<g transform="translate(80 88)"><ellipse cx="0" cy="-26" rx="9" ry="24" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><ellipse cx="0" cy="26" rx="9" ry="24" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/></g><g transform="translate(130 88)"><ellipse cx="0" cy="-26" rx="9" ry="24" fill="{SEA}" stroke="{NAVY}" stroke-width="3"/><ellipse cx="0" cy="26" rx="9" ry="24" fill="{SEA}" stroke="{NAVY}" stroke-width="3"/></g>'+curved(80,88,58,-130,-50,CORAL,4)+curved(130,88,58,-50,-130,SEA,4),
'kort':PB+line(10,88,210,88,'#7A8796',8)+f'<g transform="translate(110 88)"><ellipse cx="0" cy="-28" rx="9" ry="26" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><ellipse cx="0" cy="28" rx="9" ry="26" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/></g><path d="M70 22 L150 32 L150 44 L70 40 Z M70 154 L150 144 L150 132 L70 136 Z" fill="{PURPLE}" stroke="{NAVY}" stroke-width="3"/>',
}
TT={'fisso':('A passo fisso','La più comune: pale fuse con il mozzo, robusta ed economica. Il passo non si cambia.'),
    'abbatt':('A pale abbattibili','Barche a vela: a motore spento le pale si chiudono e frenano meno. <b>Scarso rendimento in marcia indietro</b>.'),
    'orient':('A pale orientabili','Le pale ruotano sul mozzo: a vela si mettono «in bandiera»; sulle navi il <b>passo variabile</b> regola la spinta.'),
    'npale':('Numero di pale','2 pale: barche a vela, poca resistenza. 3: il compromesso più diffuso. 4-5: meno vibrazioni, più spinta.'),
    'contro':('Controrotanti','Due eliche sullo stesso asse che girano in versi opposti (IPS, duoprop): l&#39;effetto evolutivo si annulla.'),
    'kort':('Intubata (mantello Kort)','L&#39;elica gira dentro un anello: più spinta a bassa velocità. Rimorchiatori e pescherecci.')}
def tcard(k): return f'<div style="flex:1; display:flex; gap:20px; align-items:center; background:#FFFFFF; border-radius:24px; padding:16px 22px; {SHADOW}">{svgi(220,170,tp[k],"Disegno: elica "+TT[k][0].lower(),dw=176,dh=136,pan=False)}<div style="display:flex; flex-direction:column; gap:4px">{h3(TT[k][0],28)}{p(TT[k][1],24,BODY,400,1.32)}</div></div>'
rows=''.join(f'<div style="display:flex; gap:24px">{tcard(a)}{tcard(b)}</div>' for a,b in (('fisso','abbatt'),('orient','npale'),('contro','kort')))
sec('tipieliche', head('Elica: acciaio, alluminio, composito','Le tipologie di eliche')+rows, gap=22,
 notes='Quiz 1.1.2-1 (tra passo fisso, pale abbattibili e pale orientabili, il minor rendimento in marcia indietro è delle pale abbattibili), 1.2.1-34 (materiali), 1.2.1-52 (IPS: eliche traenti controrotanti). Pale orientabili: sulle barche a vela si parla di elica «feathering», che in navigazione a vela mette le pale in bandiera; sulle navi l\'elica a passo variabile cambia la spinta, e anche la marcia indietro, senza invertitore. Più pale significa spinta più regolare e meno vibrazioni, ma più resistenza quando l\'elica è ferma.')

# ============ ELICA DESTRORSA / SINISTRORSA: EFFETTO EVOLUTIVO ============
MIR=lambda s,w: f'<g transform="translate({w} 0) scale(-1 1)">{s}</g>'
def propicon(cx,cy,cw,c):
    s=f'<circle cx="{cx}" cy="{cy}" r="62" fill="#FFFFFF" stroke="{DSOFT}" stroke-width="3"/><g transform="translate({cx} {cy})">'+''.join(f'<ellipse cx="0" cy="-20" rx="10" ry="20" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+f'<circle r="8" fill="{SUN}"/></g>'
    s+=curved(cx,cy,46,-150,-30,c,5) if cw else curved(cx,cy,46,-30,-150,c,5)
    return s
def evo2(reverse,sx):
    b=evo(reverse)
    if sx: b=MIR(b,600)
    return b+propicon(96,96,(not reverse)^sx,BLUE if not reverse else CORAL)
def sailor(sx):
    s=f'<rect x="0" y="0" width="420" height="440" rx="30" fill="#FFFFFF"/>'
    s+=f'<path d="M130 400 L130 250 Q130 200 210 196 Q290 200 290 250 L290 400 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/><path d="M168 200 L210 250 L252 200" fill="none" stroke="{BLUE}" stroke-width="8"/>'
    s+=f'<circle cx="210" cy="140" r="56" fill="{SUN}" stroke="{CORAL}" stroke-width="4"/><path d="M150 106 Q210 54 270 106 L270 116 L150 116 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
    s+=f'<circle cx="190" cy="140" r="12" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><circle cx="230" cy="140" r="12" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><path d="M192 166 Q210 180 228 166" fill="none" stroke="{INK}" stroke-width="4"/>'
    s+=f'<path d="M120 310 L300 310" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/><path d="M210 310 L210 336" stroke="{CORAL}" stroke-width="10"/>'
    s+=f'<path d="M140 250 L120 306 M280 250 L300 306" stroke="{NAVY}" stroke-width="6"/><circle cx="120" cy="310" r="16" fill="{SUN}"/><circle cx="300" cy="310" r="16" fill="{SUN}"/>'
    s+=arrow(120,330,90,420,BLUE,8,24) if not sx else arrow(300,330,330,420,BLUE,8,24)
    return s
def elicaslide(sid,sx):
    nome='sinistrorsa' if sx else 'destrorsa'
    A=('antiorario','orario') if sx else ('orario','antiorario')
    ma=('prora a <b>dritta</b>, poppa a <b>sinistra</b>') if sx else ('prora a <b>sinistra</b>, poppa a <b>dritta</b>')
    mi=('poppa a <b>dritta</b>, prora a sinistra') if sx else ('poppa a <b>sinistra</b>, prora a dritta')
    c1=card(svgi(600,480,evo2(False,sx),f'Vista dall&#39;alto, marcia avanti con elica {nome}: {ma.replace("<b>","").replace("</b>","")}',dw=480,dh=384)+h3('Marcia avanti',30,BLUE)+p(f'Ruota in senso <b>{A[0]}</b>: {ma}.',25),None,24,10)
    c2=card(svgi(600,480,evo2(True,sx),f'Vista dall&#39;alto, marcia indietro con elica {nome}: {mi.replace("<b>","").replace("</b>","")}',dw=480,dh=384)+h3('Marcia indietro',30,CORAL)+p(f'Ruota in senso <b>{A[1]}</b>: {mi}.',25),None,24,10)
    mano='sinistra' if sx else 'destra'
    c3=card(svgi(420,440,sailor(sx),f'Marinaio alla barra: la mano {mano} spinge avanti',dw=400,dh=419,pan=False)+h3(f'Mano {mano} avanti',30,PURPLE)+p(f'Elica {nome} in marcia avanti: gira come la barra spinta dalla mano {mano}. Il verso si guarda da poppa, dall&#39;esterno.',24),None,24,10)
    return f'<div style="display:flex; gap:24px">{c1}{c2}{c3}</div>'

# ============ CURVA DI EVOLUZIONE ============
X,Y,W,Hh=128,290,1092,620
b=f'<path d="M480 610 C 480 380, 420 200, 90 150" fill="none" stroke="{SEA}" stroke-width="5" stroke-dasharray="14 10"/>'
for (x,y,a,o) in [(480,540,-90,0.35),(430,300,-118,0.6),(170,160,-170,1)]:
    b+=topboat(x,y,150,a,'#FFFFFF',NAVY,3,o,False)
b+=f'<g transform="translate(0 0)">'
PX,PY=760,380
b+=f'<g transform="rotate(-24 {PX} {PY})">'+topboat(PX,440,300,-90,'#FFFFFF',NAVY,3,0.3,False)+'</g>'+topboat(PX,440,300,-90,'#FFFFFF',NAVY,4)
b+='</g>'
b+=f'<circle cx="{PX}" cy="{PY}" r="11" fill="{CORAL}"/>'
b+=curved(PX,PY,90,-90,-114,BLUE,6)+curved(PX,PY,210,90,66,CORAL,7)
lbls=lab(X+60,Y+24,420,'Curva di evoluzione',SEA,26,800)+lab(X+830,Y+366,250,'Punto di rotazione verso prora',CORAL)+lab(X+800,Y+250,260,'Prora: arco piccolo',BLUE)+lab(X+880,Y+520,200,'Poppa: arco grande',CORAL)
txt=tcol(1252,[('!','Effetto evolutivo','Maggiore con il <b>motore entrobordo</b> e con la barca <b>senza abbrivio e marcia inserita</b>.',CORAL),
 (1,'Curva di evoluzione','La traiettoria che la barca descrive accostando a dritta o a sinistra.',SEA),
 (2,'Prora e poppa','In accostata la <b>poppa</b> descrive un arco di circonferenza <b>più grande</b> di quello della prora.',SEA),
 (3,'Asse di rotazione','La barca ruota attorno a un punto che si trova <b>verso prora</b>: la poppa «scoda» all&#39;esterno.',SEA)])
sec('evoluzione', head('Elica e manovra','Effetto evolutivo e curva di evoluzione')+txt, pinned=svgp(X,Y,W,Hh,b,'A sinistra la curva di evoluzione tracciata dalla barca che accosta; a destra una barca che ruota attorno a un punto vicino alla prora: la prora descrive un arco piccolo, la poppa un arco grande')+lbls,
 notes='Quiz 1.1.2-23 (effetto evolutivo massimo senza abbrivio e con marcia inserita), -19 (curva di evoluzione: traiettoria di chi accosta a dritta o a sinistra), -6 (asse di rotazione verso prua). L\'effetto evolutivo è più marcato con l\'entrobordo perché l\'elica è fissa e il timone è separato; con fuoribordo ed entrofuoribordo si orienta la spinta stessa.')

# ============ DOPPIA LINEA D'ASSE ============
def twincell(dx,sx):
    s=f'<rect x="0" y="0" width="360" height="200" rx="24" fill="#FFFFFF"/>'
    s+=topboat(180,100,150,-90,'#FFFFFF',NAVY,4)
    for x,st,cw in ((160,sx,False),(200,dx,True)):
        s+=f'<g transform="translate({x} 186)">'+''.join(f'<ellipse cx="0" cy="-7" rx="4" ry="8" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+'</g>'
        if st: s+=arrow(x+(-34 if x<180 else 34),150 if st>0 else 60,x+(-34 if x<180 else 34),60 if st>0 else 150,GREEN if st>0 else CORAL,5,14)
    turn=-(dx or 0)+(sx or 0); fwd=(dx or 0)+(sx or 0)
    if turn>0: s+=curved(180,100,82,-90,-50,PURPLE,6)
    elif turn<0: s+=curved(180,100,82,-90,-130,PURPLE,6)
    elif fwd>0: s+=arrow(180,24,180,4,PURPLE,6,14)
    elif fwd<0: s+=arrow(180,178,180,198,PURPLE,6,14)
    return s
def tc(dx,sx,cap,alt): return f'<div style="display:flex; flex-direction:column; align-items:center; gap:4px">{svgi(360,200,twincell(dx,sx),alt,dw=234,dh=130,pan=False)}{p(cap,24,INK,700,1.2)}</div>'
def colt(t,c,cells): return f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:12px 18px; {SHADOW}">{h3(t,30,c)}{"".join(cells)}</div>'
cA=colt('Marcia avanti',SEA,[tc(1,None,'Solo la destrorsa: prora a <b>sinistra</b>','Solo il motore di dritta avanti: la prora va a sinistra'),tc(None,1,'Solo la sinistrorsa: prora a <b>dritta</b>','Solo il motore di sinistra avanti: la prora va a dritta'),tc(1,1,'Entrambe: <b>moto rettilineo</b>','Due motori avanti: la barca va dritta')])
cI=colt('Marcia indietro',CORAL,[tc(-1,None,'Solo la destrorsa: prora a <b>dritta</b>','Solo il motore di dritta indietro: la prora va a dritta'),tc(None,-1,'Solo la sinistrorsa: prora a <b>sinistra</b>','Solo il motore di sinistra indietro: la prora va a sinistra'),tc(-1,-1,'Entrambe: <b>moto rettilineo</b>','Due motori indietro: la barca va dritta a marcia indietro')])
cR=colt('Rotazione sul posto',PURPLE,[tc(1,-1,'Sinistrorsa indietro, destrorsa avanti: prora a <b>sinistra</b>','Motore di sinistra indietro e di dritta avanti: la barca gira sul posto verso sinistra'),tc(-1,1,'Sinistrorsa avanti, destrorsa indietro: prora a <b>dritta</b>','Motore di sinistra avanti e di dritta indietro: la barca gira sul posto verso dritta'),p('Motori in versi opposti: la barca <b>gira quasi su se stessa</b>.',24,BODY)])
sec('bielica', head('Destrorsa a dritta · sinistrorsa a sinistra','Doppia linea d\'asse')+f'<div style="display:flex; gap:24px">{cA}{cI}{cR}</div>',
 notes='Quiz 1.1.2-5, -3, -26, -43 (destrorsa a dritta e sinistrorsa a sinistra, per compensare l\'effetto laterale delle pale), -42 (timoni accoppiati), -29 (solo motore di dritta in marcia indietro: prora a dritta). Frecce verdi: motore avanti; rosse: motore indietro; viola: dove va la prora.')

quiz_slide('quiz3','Quiz 2 · L\'elica',['1.1.2-7', '1.1.2-11'],False)
quiz_slide('quiz3r','Quiz 2 · Le risposte',['1.1.2-7', '1.1.2-11'],True)

# ============ TIMONE ============
def rud(comp):
    s=f'<rect x="0" y="0" width="420" height="300" rx="30" fill="#FFFFFF"/><rect x="0" y="0" width="420" height="80" fill="{BOAT}"/><path d="M0 80 L420 60" stroke="{NAVY}" stroke-width="6"/>'
    ax=250 if comp else 180
    s+=dash(ax,20,ax,280,INK,3)+line(ax,40,ax,110,NAVY,10)
    if comp: s+=f'<path d="M{ax-60} 110 L{ax+120} 110 L{ax+110} 262 L{ax-50} 262 Z" fill="{SEA}" stroke="{NAVY}" stroke-width="4"/><path d="M{ax-60} 110 L{ax} 110 L{ax} 262 L{ax-50} 262 Z" fill="{SUN}" fill-opacity="0.8"/>'
    else: s+=f'<path d="M{ax} 110 L{ax+170} 110 L{ax+160} 262 L{ax} 262 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/>'
    s+=f'<text x="40" y="200" font-family="Arial" font-size="26" font-weight="700" fill="{SOFT}">prua ←</text>'
    return s
# ============ BARRA E RUOTA ============
def steer(kind):
    s=''
    rot = -22 if kind=='ruota' else 22
    s+=topboat(300,230,300,-90+rot,'#FFFFFF',NAVY,3,0.35,False)+topboat(300,230,300,-90,'#FFFFFF',NAVY,4,1,False)
    if kind=='ruota':
        s+=f'<circle cx="300" cy="300" r="30" fill="none" stroke="{NAVY}" stroke-width="7"/>'+''.join(line(300,300,300+30*math.cos(math.radians(a)),300+30*math.sin(math.radians(a)),NAVY,4) for a in range(0,360,60))
        s+=curved(300,300,48,-40,-140,CORAL,6)+f'<path d="M300 380 L300 420 L282 432" stroke="{SEA}" stroke-width="10" stroke-linecap="round" fill="none"/>'
        s+=curved(300,230,190,-100,-128,SEA,7)
    else:
        s+=f'<path d="M300 380 L262 300" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/><path d="M300 380 L318 426" stroke="{SEA}" stroke-width="12" stroke-linecap="round"/>'
        s+=curved(300,230,190,-80,-52,SEA,7)
    return s
def stc(kind,mir,cap,alt):
    b=steer(kind); b=MIR(b,600) if mir else b
    return f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:6px; background:#FFFFFF; border-radius:24px; padding:14px; {SHADOW}">{svgi(600,440,b,alt,dw=300,dh=220)}{p(cap,26,INK,700,1.2)}</div>'
def rowhead(t,r,c,bg): return f'<div style="flex:1.1; display:flex; flex-direction:column; justify-content:center; gap:8px; background:{bg}; border-radius:24px; padding:22px">{h3(t,32,c)}{p(r,24,INK)}</div>'
r1=f'<div style="display:flex; gap:20px">{rowhead("Timone a barra","Pala e barra <b>in direzioni opposte</b>. Anche il <b>piede del fuoribordo</b> agisce da timone.",CORAL,CORAL_T)}'+stc('barra',True,'Barra a <b>dritta</b>: accosto a <b>sinistra</b>','Barra a dritta, pala a sinistra: la prua va a sinistra')+stc('barra',False,'Barra a <b>sinistra</b>: accosto a <b>dritta</b>','Barra a sinistra, pala a dritta: la prua va a dritta')+'</div>'
r2=f'<div style="display:flex; gap:20px">{rowhead("Timone a ruota","Pala e ruota <b>nella stessa direzione</b>.",SEA,SEA_T)}'+stc('ruota',False,'Ruota a <b>sinistra</b>: accosto a <b>sinistra</b>','Ruota girata a sinistra: la prua va a sinistra')+stc('ruota',True,'Ruota a <b>dritta</b>: accosto a <b>dritta</b>','Ruota girata a dritta: la prua va a dritta')+'</div>'
sec('barraruota', head('Governare la barca','Timone a barra e timone a ruota')+r1+r2, gap=24,
 notes='Quiz 1.1.2-32 e -14 (ruota a sinistra: prora a sinistra, poppa a dritta), -20 (barra in marcia indietro), -34 (fuoribordo: piede a dritta, poppa a sinistra). Il quiz 1.1.2-31 sulla barra è oscurato, ma il principio resta: barra a sinistra, prua a dritta. Tutto vale in marcia avanti; in marcia indietro l\'effetto si inverte ed è più debole.')

# ============ EFFETTI DEL TIMONE ============
X,Y,W,Hh=1000,290,792,620
b=f'<path d="M396 40 Q470 120 470 260 L470 520 Q470 560 430 560 L362 560 Q322 560 322 520 L322 260 Q322 120 396 40 Z" fill="#DCEBF7" stroke="{NAVY}" stroke-width="4"/>'
for x0 in (270,350,440,520):
    b+=f'<path d="M{x0} 90 L{x0} {470 if x0<400 else 500}" stroke="{BLUE}" stroke-width="4"/>'+head_at(x0,470 if x0<400 else 500,90,BLUE,14)
b+=''.join(f'<path d="M{x0} 420 Q{x0+10} 560 {x0+90} 600" fill="none" stroke="{BLUE}" stroke-width="4"/>' for x0 in (470,500))
b+=f'<path d="M410 560 L452 640" stroke="{NAVY}" stroke-width="18" stroke-linecap="round"/>'
b+=arrow(420,580,420,700,CORAL,6,18)+arrow(420,580,260,580,GREEN,6,18)+arrow(420,580,300,690,BLUE,6,18)
b+=f'<path d="M396 40 Q420 -10 470 -20" fill="none" stroke="{CORAL}" stroke-width="5"/>'+head_at(470,-20,-10,CORAL,16)
b=f'<g transform="translate(0 50) scale(1 0.8)">{b}</g>'
lbls=lab(X+470,Y+14,300,'Moto della barca',CORAL)+lab(X+30,Y+120,230,'Flusso dell&#39;acqua sotto lo scafo',BLUE)+lab(X+30,Y+530,230,'Sbandante: lieve deriva',GREEN)+lab(X+100,Y+470,200,'Direzionale',BLUE)+lab(X+440,Y+580,200,'Frenante',CORAL)+lab(X+500,Y+470,120,'Pala',NAVY)
txt=f'<div style="position:absolute; left:128px; top:290px; width:820px; display:flex; flex-direction:column; gap:22px">'+boxn('Effetto evolutivo dell&#39;elica','Nasce dalla <b>spinta delle pale</b> e dal <b>flusso dell&#39;acqua contro timone e carena</b>.',PURPLE,LILAC_T)+tcol_inner([
 (1,'Effetto direzionale','La pala devia l&#39;acqua: la poppa si sposta e la barca accosta.',BLUE),
 (2,'Effetto frenante','Il timone girato <b>riduce la velocità</b>.',CORAL),
 (3,'Effetto sbandante','<b>Spostamento laterale</b> sul lato opposto alla pala: una lieve deriva.',GREEN),
 (4,'Leggero appruamento','La prua si abbassa un poco.',SEA)])+boxn('Angolo utile','Massimo effetto con la pala a <b>30°–40°</b> dall&#39;asse longitudinale; oltre, frena soltanto.',SUN,SUN_T)+'</div>'
sec('effettitimone', head('Effetti combinati elica / timone','Cosa fa il timone')+txt, pinned=svgp(X,Y,W,Hh,b,'Scafo visto da sotto con il flusso dell&#39;acqua verso poppa e la pala del timone girata: frecce dell&#39;effetto direzionale, frenante e sbandante e curva del moto della barca')+lbls,
 notes='Quiz 1.1.2-8 (effetto evolutivo: spinta delle pale e flusso contro timone e carena), -18 (oltre all\'accostata il timone riduce la velocità, sposta lateralmente sul lato opposto alla pala e fa leggermente appruare), -13 (massimo effetto tra 30 e 40 gradi).')

# ============ TIPI DI TIMONI ============
def rud_ord():
    s=f'<rect x="0" y="0" width="560" height="440" rx="30" fill="#FFFFFF"/><path d="M380 30 L560 30" stroke="{NAVY}" stroke-width="5"/><rect x="372" y="60" width="18" height="360" fill="{GREEN}"/>'
    s+=f'<path d="M340 40 L340 360 Q300 420 200 410 Q150 400 150 330 L150 230 Q160 170 260 150 L340 130" fill="#A0703C" stroke="{NAVY}" stroke-width="4"/>'
    s+=line(346,14,346,380,NAVY,8)+f'<rect x="346" y="10" width="140" height="14" rx="6" fill="#A0703C" stroke="{NAVY}" stroke-width="3"/>'
    for y in (170,290):
        s+=f'<path d="M346 {y} L372 {y}" stroke="{NAVY}" stroke-width="10"/><path d="M362 {y-14} L380 {y-14} L380 {y+14} L362 {y+14}" fill="none" stroke="{CORAL}" stroke-width="5"/>'
    t=lambda x,y,w,a='start': f'<text x="{x}" y="{y}" text-anchor="{a}" font-family="Arial" font-size="24" font-weight="700" fill="{INK}">{w}</text>'
    s+=t(150,40,'anima / asse')+line(292,34,340,34,CORAL,2)+t(400,174,'femminelle')+t(170,110,'agugliotti','start')+t(400,330,'dritto')+t(400,358,'di poppa')+t(160,196,'spalla')+t(200,330,'pala')
    s+=line(300,104,344,166,CORAL,2)+line(300,104,344,286,CORAL,2)
    return s
def rud_semi():
    s=f'<rect x="0" y="0" width="420" height="300" rx="30" fill="#FFFFFF"/><rect x="0" y="0" width="420" height="80" fill="{BOAT}"/><path d="M0 80 L420 60" stroke="{NAVY}" stroke-width="6"/>'
    ax=210
    s+=f'<rect x="{ax-10}" y="58" width="20" height="30" fill="{SUN}"/>'+line(ax,20,ax,120,NAVY,10)
    s+=f'<path d="M{ax} 110 L{ax+130} 110 L{ax+120} 262 L{ax-60} 262 L{ax-60} 180 L{ax} 180 Z" fill="{SEA}" stroke="{NAVY}" stroke-width="4"/><path d="M{ax-60} 180 L{ax} 180 L{ax} 262 L{ax-60} 262 Z" fill="{SUN}" fill-opacity="0.8"/>'
    s+=f'<text x="{ax-24}" y="50" text-anchor="end" font-family="Arial" font-size="24" font-weight="700" fill="{INK}">losca</text><text x="40" y="200" font-family="Arial" font-size="24" font-weight="700" fill="{SOFT}">prua ←</text>'
    return s
def rud_twin():
    s=f'<rect x="0" y="0" width="420" height="300" rx="30" fill="#FFFFFF"/><path d="M40 60 Q210 40 380 60 Q360 160 210 170 Q60 160 40 60 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/><path d="M52 110 Q210 150 368 110 Q340 166 210 172 Q80 166 52 110 Z" fill="{CORAL}"/>'
    for x in (150,270):
        s+=line(x,160,x,200,NAVY,6)+f'<g transform="translate({x} 222)">'+''.join(f'<ellipse cx="0" cy="-14" rx="8" ry="15" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+'</g>'
        s+=f'<rect x="{x+34}" y="170" width="16" height="110" rx="4" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/>'
    return s
o1=card(svgi(560,440,rud_ord(),'Timone ordinario incernierato al dritto di poppa: pala, spalla, anima o asse, agugliotti e femminelle',dw=440,dh=346)+h3('Ordinario · incernierato esterno',30)+p('Tutta la pala a poppavia dell&#39;asse; gli <b>agugliotti</b> girano nelle <b>femminelle</b> del dritto di poppa.',24),None,24,10,1.35)
o2=card(svgi(420,300,rud(True),'Timone compensato: metà pala a proravia dell&#39;asse',dw=300,dh=214)+h3('Compensato',30)+p('Circa <b>50% della pala a proravia</b> e 50% a poppavia: meno sforzo su barra o ruota.',24),None,24,10)
o3=card(svgi(420,300,rud_semi(),'Timone semicompensato sospeso: l&#39;asse passa nella losca, solo la parte bassa della pala è a proravia',dw=300,dh=214)+h3('Semicompensato',30)+p('Timone <b>sospeso</b>, con l&#39;asse passante nella <b>losca</b>.',24),None,24,10)
o4=card(svgi(420,300,rud_twin(),'Poppa vista da dietro con due eliche e due timoni uguali',dw=300,dh=214)+h3('Accoppiati',30)+p('Due timoni <b>uguali e simmetrici</b> che agiscono in sintonia, sulle bieliche.',24),None,24,10)
sec('timone', head('Massimo 30°–40° di angolo della pala','Tipi di timoni')+f'<div style="display:flex; gap:24px">{o1}{o2}{o3}{o4}</div>',
 notes='Quiz 1.1.1-56 (pala), -33 (losca: apertura nella poppa per l\'asse del timone), 1.1.2-36 (ordinario: tutta la pala a poppavia dell\'anima), -9, -10, -27, -37 e 1.1.1-55, -57 (compensato: parte della pala a proravia dell\'asse, meno sforzo), -42 (timoni accoppiati), -13 (30-40 gradi). Agugliotti: perni fissati al timone; femminelle: anelli sul dritto di poppa in cui gli agugliotti girano.')


sec('elicadx2', head('Elica destrorsa','Destrorsa: effetto evolutivo')+elicaslide('elicadx2',False),
 notes='Quiz 1.1.2-7 (destrorsa: in marcia avanti gira in senso orario vista da poppa), -35 (in marcia indietro antiorario), -44 (marcia avanti, timone al centro: prua a sinistra, poppa a dritta), -2, -12, -30 (marcia indietro: poppa a sinistra, prora a dritta). Nel disegno la sagoma chiara è la barca dopo l\'accostata; la freccia grigia è il verso del moto. Il promemoria della mano: immagina di spingere avanti con la mano destra una barra orizzontale davanti a te: la barra gira come l\'elica destrorsa vista da poppa. Subito dopo, lo specchio: la sinistrorsa.')

sec('elicasx', head('Elica sinistrorsa','Sinistrorsa: effetto evolutivo')+elicaslide('elicasx',True),
 notes='Quiz 1.1.2-15 e -33 (sinistrorsa: in marcia avanti gira in senso antiorario vista da poppa), -45 e -39 (marcia avanti, timone al centro: prua a dritta, poppa a sinistra), -4, -25, -40 (marcia indietro: poppa a dritta). È tutto lo specchio della destrorsa. Promemoria: mano sinistra avanti.')

# ============ EFFETTI COMBINATI ELICA / TIMONE ============
def mini(n,rev,sx=False):
    s=topboat(85,110,130,-90,'#8FB3E0',NAVY,3)
    if n in (1,3,4): s+=f'<g transform="translate(85 150)">'+''.join(f'<ellipse cx="0" cy="-7" rx="4" ry="8" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+'</g>'
    if n in (2,3): s+=f'<path d="M85 172 L66 204" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/>'
    if n==4: s+=f'<path d="M85 172 L104 204" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/>'
    if not rev:
        if n==4: s+=curved(85,110,70,-90,-120,BLUE,4)+curved(85,110,70,-90,-60,CORAL,4)
        else: s+=curved(85,110,70,-90,-128 if n==3 else -118,BLUE if n==1 else CORAL if n==2 else PURPLE,5)
    else:
        if n==4: s+=curved(85,110,70,90,120,BLUE,4)+curved(85,110,70,90,60,CORAL,4)
        else: s+=curved(85,110,70,90,128 if n==3 else 118,BLUE if n==1 else CORAL if n==2 else PURPLE,5)
    if sx: s=MIR(s,170)
    return f'<rect x="0" y="0" width="170" height="210" rx="20" fill="#FFFFFF"/>'+s+f'<text x="85" y="100" text-anchor="middle" font-family="Arial" font-size="30" font-weight="700" fill="#FFFFFF">{n}</text>'
def minirow(rev,sx,alt): return ''.join(svgi(170,210,mini(n,rev,sx),f'{alt}, caso {n}',dw=146,dh=180,pan=False) for n in (1,2,3,4))
def half(t,rev,sx,cap,alt): return f'<div style="flex:1; display:flex; flex-direction:column; gap:6px"><div style="display:flex; gap:10px">{minirow(rev,sx,alt)}</div>{p("<b>"+t+"</b> · "+cap,24,INK,400,1.3)}</div>'
def band(t,c,bg,l,r): return f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; border-radius:24px; padding:10px 22px">{h3(t,28,c)}<div style="display:flex; gap:32px">{l}{r}</div></div>'
bd=band('Elica destrorsa',CORAL,CORAL_T,half('Marcia avanti',False,False,'elica ¹ e timone a sinistra ² → <b>prora a sinistra</b> ³; timone a dritta ⁴ compensa.','Elica destrorsa in marcia avanti'),half('Marcia indietro',True,False,'elica ¹ e timone a sinistra ² → <b>poppa a sinistra</b> ³; timone a dritta ⁴ compensa.','Elica destrorsa in marcia indietro'))
bs=band('Elica sinistrorsa',SEA,SEA_T,half('Marcia avanti',False,True,'elica ¹ e timone a dritta ² → <b>prora a dritta</b> ³; timone a sinistra ⁴ compensa.','Elica sinistrorsa in marcia avanti'),half('Marcia indietro',True,True,'elica ¹ e timone a dritta ² → <b>poppa a dritta</b> ³; timone a sinistra ⁴ compensa.','Elica sinistrorsa in marcia indietro'))
sec('elicatimone', head('Elica + timone','Effetti combinati elica e timone')+bd+bs, gap=20,
 notes='Quiz 1.1.2-44 e -45 (effetto dell\'elica in marcia avanti), -2, -12, -30, -4, -25, -40 (in marcia indietro), -28 (destrorsa in retromarcia: timone a dritta limita la poppa che va a sinistra), -41 (l\'effetto evolutivo si compensa con il timone). Caso 1: solo elica; 2: solo timone; 3: elica e timone insieme, l\'effetto si somma; 4: timone dalla parte opposta, l\'effetto si compensa e la barca va dritta. Frecce: blu = elica, rossa = timone, viola = somma.')

# ============ EFFETTI COMBINATI ============
def dock(kind):
    s=''
    if kind=='poppa':
        s+=f'<rect x="0" y="0" width="600" height="70" fill="#C9B79C"/>'+''.join(f'<rect x="{x}" y="70" width="18" height="14" fill="#8C7A5E"/>' for x in range(40,600,120))
        s+=topboat(330,250,260,86,'#FFFFFF',NAVY,4)+topboat(300,160,260,90,'#FFFFFF',NAVY,3,0.3,False)
        s+=dpath('M340 380 C 340 300, 330 240, 305 110',CORAL)+head_at(305,106,-100,CORAL)
    else:
        s+=f'<rect x="0" y="0" width="80" height="480" fill="#C9B79C"/>'+''.join(f'<rect x="80" y="{y}" width="14" height="18" fill="#8C7A5E"/>' for y in range(40,480,120))
        s+=topboat(230,250,260,-120,'#FFFFFF',NAVY,4)+topboat(170,240,260,-90,'#FFFFFF',NAVY,3,0.3,False)
        s+=curved(230,250,150,60,100,CORAL,7)
    return s
k1=card(svgi(600,480,dock('poppa'),'Vista dall\'alto: ormeggio di poppa alla banchina in retromarcia',dw=520,dh=416)+h3('Di poppa · elica sinistrorsa',30)+p('Si retrocede perpendicolari alla banchina <b>presentando il giardinetto di dritta</b>.',25),None,24,10)
k2=card(svgi(600,480,dock('inglese'),'Vista dall\'alto: ormeggio all\'inglese con banchina a sinistra',dw=520,dh=416)+h3('All\'inglese · elica destrorsa',30)+p('Banchina a sinistra: arrivo con il <b>mascone di sinistra</b>, poi marcia indietro. La poppa si avvicina e l\'abbrivio si ferma.',25),None,24,10)
k3=card(note('Trucchi di manovra',CORAL,40)+'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:12px"><li>Destrorsa in retromarcia: con il <b>timone a dritta</b> limito la poppa che va a sinistra.</li><li>Avaria al timone su una piccola barca: <b>remo in acqua a sinistra</b> per virare a sinistra.</li></ul>',None,30,12)
sec('combinati', head('Elica + timone','Ormeggi: elica e timone in manovra')+f'<div style="display:flex; gap:24px">{k1}{k2}{k3}</div>',
 notes='Quiz 1.1.2-21 (ormeggio di poppa con sinistrorsa), -22 (all\'inglese con destrorsa, banchina a sinistra), -28 (timone a dritta in retro con destrorsa), -38 (avaria al timone: remo a sinistra). Le prove pratiche dell\'All. D chiedono proprio gli effetti di timone ed elica in marcia avanti e indietro.')

quiz_slide('quiz4','Quiz 4 · Il timone',['1.1.2-10', '1.1.2-14'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.1.2-10', '1.1.2-14'],True)
exec(open('apertura.py').read())
chapter('cap1',1,'Il motore',['Benzina: miscela e scintilla','Il ciclo a quattro tempi','S-drive, IPS, POD e idrogetto','Dal motore all\'elica','Fuoribordo, entrofuoribordo, entrobordo','Inconvenienti del motore a scoppio','Raffreddamento a circuito aperto','Raffreddamento a circuito chiuso','Diesel: aria compressa e iniettori','Il ciclo del diesel','Benzina e diesel a confronto'],CORAL,
 'Circa 25 minuti, verifica da 2 quiz compresa: 11 slide, andare spediti e lasciare il dettaglio alle note.','circa 25 minuti · 11 argomenti',2)
chapter('cap2',2,'L\'elica',['Le tipologie di eliche','Effetto evolutivo e curva di evoluzione','Spinta e velocità','Mozzo, pale, passo e regresso'],BLUE,
 'Circa 15 minuti, verifica da 2 quiz compresa.','circa 15 minuti · 4 argomenti',1)
chapter('cap3',3,'Avarie, manutenzione e autonomia',['Inconvenienti del motore diesel','Carburante e manutenzione','Quanto carburante imbarcare','Autonomia e consumi'],PURPLE,
 'Circa 15 minuti, verifica da 2 quiz compresa.','circa 15 minuti · 4 argomenti',1,art=(fire_scene(),'Illustrazione: estintore accanto a una fiamma'))
chapter('cap4',4,'Timone ed effetti combinati',['Timone a barra e a ruota','Cosa fa il timone','Tipi di timoni','Doppia linea d\'asse','Destrorsa: effetto evolutivo','Sinistrorsa: effetto evolutivo','Effetti combinati elica e timone','Ormeggi: elica e timone in manovra'],SEA,
 'Circa 20 minuti, verifica da 2 quiz compresa.','circa 20 minuti · 8 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
QZ=[('q01','Quiz 1 · Benzina e diesel',['1.2.1-2','1.2.1-3','1.2.1-32']),('q02','Quiz 2 · Ciclo e accensione',['1.2.1-16','1.2.1-17','1.2.1-18']),
 ('q03','Quiz 3 · Trasmissioni e idrogetto',['1.2.1-9','1.2.1-45','1.2.1-47']),('q04','Quiz 4 · Il raffreddamento',['1.2.1-4','1.2.1-8','1.2.1-13']),
 ('q05','Quiz 5 · Il diesel',['1.2.1-1','1.2.1-15','1.2.1-49']),('q06','Quiz 6 · Avarie del motore',['1.2.2-10','1.2.2-15','1.2.2-17']),
 ('q07','Quiz 7 · Manutenzione e controlli',['1.2.1-36','1.2.1-50','1.2.2-12']),('q08','Quiz 8 · Autonomia e carburante',['1.2.2-2','1.2.2-29','1.2.3-12']),
 ('q09','Quiz 9 · Le eliche',['1.1.2-1','1.1.2-8','1.1.2-15']),('q10','Quiz 10 · Effetto evolutivo',['1.1.2-2','1.1.2-25','1.1.2-35']),
 ('q11','Quiz 11 · Il timone',['1.1.2-9','1.1.2-27','1.1.2-39']),('q12','Quiz 12 · Due eliche e manovre',['1.1.2-5','1.1.2-22','1.1.2-42'])]
raccolta(2,5,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Benzina o diesel?','Candele e carburatore sono della benzina, iniettori e candelette del diesel: guarda di che motore parla.'),
  ('Destra o sinistra','Destrorsa in retro: la poppa va a sinistra. Disegna l\'elica vista da poppa prima di rispondere.'),
  ('Attento ai numeri','Litri, ore, nodi e il 30% di riserva: rifai il conto sul foglio.')],
 ['Quiz 1-5 · il motore (15)','Quiz 6-8 · avarie, manutenzione, autonomia (9)','Quiz 9-12 · elica e timone (12)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Far rispondere ad alta voce con la lettera, poi chiedere perché le altre due sono sbagliate. Se il tempo stringe, lasciare per casa le slide 7 e 11.')
closing(['Motore + elica = sistema propulsivo; l\'invertitore cambia marcia, non il verso del motore','4 tempi: aspirazione, compressione, scoppio, scarico','Benzina: aerare il vano motore; diesel: niente aria nel circuito','Carburante = consumo orario × ore + 30%','Destrorsa in retro: la poppa va a sinistra; si compensa col timone'],
 'Prossima lezione · 03 · Ormeggi, cartografia e primi calcoli','A casa: i 104 quiz ufficiali di Motori e i 50 su elica, timone e stabilità.')
write_deck(OUT,'Lezione 02 · Motori, elica e timone',
 ['cover','agenda','cap1','benzina','quattrotempi','trasmissioni','lineaasse','installazioni','avariescoppio','raffreddamento','raffreddamentoeb','diesel','diesel4t','benzinadiesel','quiz1','quiz1r',
  'cap2','tipieliche','evoluzione','spinta','elica','quiz3','quiz3r',
  'cap3','avariediesel','manutenzione','carburante','autonomia','quiz2','quiz2r',
  'cap4','barraruota','effettitimone','timone','bielica','elicadx2','elicasx','elicatimone','combinati','quiz4','quiz4r',
  'capquiz','quiz']+[q+s for q,_,_ in QZ for s in ('','r')]+['chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Il motore: benzina, ciclo a 4 tempi, trasmissioni, linea d'asse, motore marino, avarie, raffreddamento, diesel","start":"cap1"},
  "s3":{"description":"L'elica: tipologie, effetto evolutivo, curva di evoluzione, spinta e velocità, passo e regresso","start":"cap2"},"s4":{"description":"Avarie del diesel, manutenzione e calcolo dell'autonomia","start":"cap3"},
  "s5":{"description":"Timone, doppia linea d'asse, effetti combinati elica e timone","start":"cap4"},"s6":{"description":"Raccolta quiz","start":"capquiz"}})
