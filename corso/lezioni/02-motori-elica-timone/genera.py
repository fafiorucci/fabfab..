import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez02/project'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Entrobordo, entrofuoribordo, fuoribordo, idrogetto':'propeller','Dal motore all\'elica':'propeller','Il ciclo a quattro tempi':'fuel',
 'Motore a benzina e motore diesel':'fuel','Il raffreddamento':'current','Il motore ci parla: fumo e avviamento':'cloud','Il motore ci parla: in navigazione':'helm',
 'Carburante e manutenzione':'fuel','Quanto carburante imbarcare':'fuel','Autonomia e consumi':'chart','Mozzo, pale, passo e regresso':'propeller',
 'Elica destrorsa e sinistrorsa':'propeller','L\'effetto evolutivo dell\'elica':'current','Due motori, due eliche':'propeller','Il timone':'helm','Barra e ruota':'helm','Effetti combinati elica e timone':'anchor'})

# ============ COVER + AGENDA ============
cover(2,'Motori, elica e timone','Come funziona il motore, come spinge l\'elica, come governa il timone',
 'Lezione 2. Capitoli del programma della scuola: Motori ed Elica-Timone. All. A al DM 323/2021: materia 2 (motori, avarie, calcolo dell\'autonomia) e punto 1b (elica, timone). Ordine del manuale Il Frangente, cap. 1: motore e trasmissione, funzionamento, raffreddamento, irregolarità, elica, effetto evolutivo, timone, effetti combinati.')
blocks=[('0:00','15′','Installazioni e linea d\'asse',CORAL),('0:15','25′','Motore, raffreddamento · quiz 1',SEA),('0:40','25′','Avarie, manutenzione, autonomia · quiz 2',PURPLE),('1:05','20′','Elica ed effetto evolutivo · quiz 3',BLUE),('1:25','20′','Timone e manovre · quiz 4',GREEN),('1:45','15′','Verifica finale',CORAL)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">1 + 1</p>'+p('domande su 20: una di Motori e una di Teoria dello scafo (elica e timone)',26,INK,700)+p('104 quiz ufficiali sui motori, di cui 27 sul calcolo dell\'autonomia; 50 su elica, timone e stabilità.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>riconoscere le installazioni del motore e la linea d\'asse</li><li>spiegare il ciclo a 4 tempi, benzina e diesel</li><li>capire cosa ti dice un motore che non va</li><li>calcolare carburante e autonomia con il 30% di riserva</li><li>prevedere l\'effetto dell\'elica e del timone</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 02 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie da 3 quiz e una finale da 6, tutti ufficiali (DD 131/2022). Il capitolo dell\'Excel della scuola: motore marino, trasmissione, 4 tempi, diesel, raffreddamento EB/FB, inconvenienti; elica e timone.')

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
D={'entrobordo':('Entrobordo','Motore dentro lo scafo; la linea d\'asse porta il moto all\'elica, il timone governa.'),
   'entrofuoribordo':('Entrofuoribordo','Motore dentro, trasmissione riunita in un piede (gruppo poppiero) applicato alla poppa.'),
   'fuoribordo':('Fuoribordo','Motore, trasmissione ed elica in un unico blocco sullo specchio di poppa; si governa ruotandolo.'),
   'idrogetto':('Idrogetto','Una pompa aspira l\'acqua e la spinge ad alta velocità da poppa; poco manovrabile al minimo.')}
cc=''.join(card(svgi(440,230,inst[k],f'Disegno di profilo: installazione {D[k][0].lower()}',dw=350,dh=183)+h3(D[k][0],30)+p(D[k][1],24),None,24,10) for k in D)
sec('installazioni', head('Il sistema propulsivo · motore + elica','Entrobordo, entrofuoribordo, fuoribordo, idrogetto')+f'<div style="display:flex; gap:24px">{cc}</div>'
 +note('Sulle barche a vela spesso c\'è la S-drive: un piedino con due ingranaggi conici al posto della linea d\'asse. Pod e IPS: piedi immersi e orientabili, con eliche traenti.',PURPLE,32),
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
b+=line(578,338,210,454,'#7A8796',12)+f'<rect x="372" y="376" width="80" height="26" rx="8" fill="{PURPLE}" transform="rotate(17.5 412 389)"/>'
b+=f'<ellipse cx="200" cy="432" rx="12" ry="30" fill="{NAVY}"/><ellipse cx="200" cy="492" rx="12" ry="30" fill="{NAVY}"/><circle cx="202" cy="459" r="10" fill="{SUN}"/>'
b+=line(152,250,152,420,NAVY,6)+f'<path d="M140 400 L176 400 L176 520 Q160 530 140 520 Z" fill="{NAVY}"/>'
for (lx,ly,tx,ty) in [(760,120,755,222),(560,200,600,288),(470,520,420,420),(330,300,405,378),(280,570,215,500),(60,150,150,300)]: b+=arrow(lx,ly,tx,ty,INK,3)
lbls=lab(X+690,Y+84,300,'Motore',INK)+lab(X+440,Y+160,260,'Invertitore / riduttore',SEA)+lab(X+380,Y+524,260,'Asse portaelica',INK)+lab(X+220,Y+262,220,'Astuccio',PURPLE)+lab(X+250,Y+574,160,'Elica',INK)+lab(X+20,Y+110,170,'Timone',INK)
txt=term('Linea d\'asse','L\'insieme di organi meccanici che trasmette il movimento dal motore all\'elica.')+term('Invertitore','Dà marcia avanti, folle e marcia indietro: il motore gira sempre nello stesso verso.')+term('Riduttore','Riduce i giri che arrivano all\'elica.')+term('Astuccio','Il tubo in cui l\'asse portaelica attraversa lo scafo, a tenuta d\'acqua.')
sec('lineaasse', head('Motore entrobordo · trasmissione','Dal motore all\'elica')+f'<div style="position:absolute; left:1260px; top:290px; width:532px; display:flex; flex-direction:column; gap:24px">{txt}</div>', pinned=svgp(X,Y,W,Hh,b,'Spaccato di poppa: motore, invertitore e riduttore, asse portaelica che esce dallo scafo attraverso l\'astuccio, elica e timone')+lbls,
 notes='Quiz 1.2.2-7 (linea d\'asse), 1.2.1-7 e -14 (invertitore: non si inverte la rotazione del motore), 1.2.1-42/43/44 (figure: astuccio, asse portaelica, invertitore/riduttore), 1.2.1-41 (paratia del vano motore).')
X,Y,W,Hh=700,290,1092,620

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
st=[('asp','1 · Aspirazione','Si apre la valvola di aspirazione, il pistone scende e aspira miscela o aria.'),('com','2 · Compressione','Valvole chiuse: il pistone sale e comprime.'),('sco','3 · Scoppio','La combustione spinge il pistone verso il basso: è la fase utile.'),('sca','4 · Scarico','Si apre la valvola di scarico e il pistone spinge fuori i gas combusti.')]
cc=''.join(card(svgi(300,300,cyl(k),f'Cilindro nella fase di {t.split(" · ")[1].lower()}',dw=300,dh=300)+h3(t,30)+p(d,24),None,24,10) for k,t,d in st)
sec('quattrotempi', head('Come funziona il motore','Il ciclo a quattro tempi')+f'<div style="display:flex; gap:24px">{cc}</div>'+note('Un ciclo completo = 4 corse del pistone e 2 giri dell\'albero motore.',CORAL,40),
 notes='Quiz 1.2.1-6 e -33 (aspirazione, compressione, scoppio, scarico), 1.2.1-16 e -17 (2 giri dell\'albero, 4 corse del pistone). Nel diesel si aspira solo aria e il gasolio viene iniettato alla fine della compressione.')

# ============ BENZINA / DIESEL ============
plug=f'<rect x="0" y="0" width="260" height="160" rx="26" fill="#FFFFFF"/><rect x="100" y="16" width="60" height="40" rx="8" fill="{NAVY}"/><rect x="108" y="56" width="44" height="40" fill="#E9EEF3" stroke="{NAVY}" stroke-width="3"/><rect x="118" y="96" width="24" height="26" fill="#7A8796"/><path d="M130 122 L130 134 L144 134" fill="none" stroke="{NAVY}" stroke-width="5"/><polygon points="150,126 160,136 150,146 156,136" fill="{SUN}"/><polygon points="164,122 176,138 162,150" fill="{SUN}"/>'
inj=f'<rect x="0" y="0" width="260" height="160" rx="26" fill="#FFFFFF"/><rect x="110" y="10" width="40" height="70" rx="8" fill="{NAVY}"/><path d="M118 80 L142 80 L134 108 L126 108 Z" fill="#7A8796"/>'+''.join(line(130,110,130+dx,150,'#9DB9F2',4) for dx in (-40,-20,0,20,40))
cb=card(f'<div style="display:flex; gap:20px; align-items:center">{svgi(260,160,plug,"Candela di accensione con la scintilla",pan=False)}<div>{h3("Benzina",34)}{tag("motore a scoppio",CORAL)}</div></div>'
 +'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:8px"><li>La miscela si accende con la <b>candela</b>: il sistema di accensione esiste solo nei motori a scoppio.</li><li>Il pericolo principale: i <b>vapori di benzina</b> che si accumulano nel vano motore.</li><li>Prima di avviare un entrobordo a benzina: <b>aerare il vano motore</b>.</li></ul>',None,30,14)
cd=card(f'<div style="display:flex; gap:20px; align-items:center">{svgi(260,160,inj,"Iniettore che nebulizza il gasolio",pan=False)}<div>{h3("Diesel",34)}{tag("accensione per compressione",SEA)}</div></div>'
 +'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:8px"><li>Alimentazione: <b>pompa di alimentazione, pompa di iniezione, iniettori</b> (uno per cilindro) che nebulizzano il gasolio.</li><li>Iniezione indiretta: servono le <b>candelette</b>. La batteria è essenziale per l\'avviamento.</li><li>Si spegne togliendo il carburante alla pompa di iniezione. Gasolio: punto di infiammabilità più alto.</li></ul>',None,30,14)
sec('benzinadiesel', head('Due motori a confronto','Motore a benzina e motore diesel')+f'<div style="display:flex; gap:24px">{cb}{cd}</div>'+note('1 kW = 1,36 CV · aerazione forzata del vano diesel: consigliata, non obbligatoria',PURPLE,34),
 notes='Quiz 1.2.1-2, -3 (vapori, aerare il vano), -18 (accensione solo nei motori a scoppio), -29, -48, -49 (iniettori, alimentazione diesel), -50 (candelette), -15 (batteria), -1 (spegnimento diesel), -32 (infiammabilità), -5 (aerazione forzata diesel non obbligatoria), -30 (1 kW = 1,36 CV).')

# ============ RAFFREDDAMENTO ============
fb=f'<rect x="0" y="170" width="764" height="130" fill="{WATER}" fill-opacity="0.22"/>'+line(0,170,764,170,SEA,3)
fb+=f'<path d="M470 60 L470 190 L640 170 L640 70 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
fb+=f'<rect x="300" y="26" width="130" height="86" rx="26" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/><rect x="340" y="112" width="44" height="100" fill="{NAVY}"/><path d="M330 212 L396 212 L390 250 L336 250 Z" fill="{NAVY}"/><path d="M320 200 L406 200" stroke="{NAVY}" stroke-width="6"/>'
fb+=f'<ellipse cx="316" cy="226" rx="8" ry="22" fill="{NAVY}"/><circle cx="318" cy="228" r="6" fill="{SUN}"/>'+''.join(line(346+i*8,222,346+i*8,240,'#FFFFFF',3) for i in range(5))
fb+=arrow(280,280,344,236,SEA,4,16)+arrow(440,282,380,238,SEA,4,16)+f'<path d="M430 96 Q470 100 486 136" fill="none" stroke="{WATER}" stroke-width="7" stroke-linecap="round"/>'
fb+=num(250,272,1,SEA)+num(516,120,2,CORAL)
eb=f'<rect x="0" y="210" width="764" height="90" fill="{WATER}" fill-opacity="0.22"/>'+line(0,210,764,210,SEA,3)
eb+=f'<rect x="420" y="40" width="200" height="110" rx="18" fill="{NAVY}"/><rect x="200" y="60" width="150" height="70" rx="14" fill="{SUN_T}" stroke="{SUN}" stroke-width="5"/>'+''.join(f'<path d="M214 {76+i*14} q16 -8 32 0 t32 0 t32 0 t32 0" fill="none" stroke="{SUN}" stroke-width="3"/>' for i in range(3))
eb+=f'<path d="M420 80 L350 80 M350 110 L420 110" stroke="{CORAL}" stroke-width="8"/>'
eb+=f'<circle cx="120" cy="170" r="30" fill="#FFFFFF" stroke="{SEA}" stroke-width="6"/>'+''.join(line(120,170,120+20*math.cos(a),170+20*math.sin(a),SEA,4) for a in [0,1.05,2.1,3.14,4.19,5.24])
eb+=f'<path d="M120 250 L120 200 M120 140 L120 95 L200 95" fill="none" stroke="{SEA}" stroke-width="8"/><path d="M275 130 L275 180 L700 180 L700 250" fill="none" stroke="{SEA}" stroke-width="8"/>'
eb+=f'<rect x="100" y="250" width="40" height="22" rx="6" fill="{NAVY}"/>'+arrow(120,292,120,262,SEA,4,14)+arrow(700,236,700,280,SEA,4,14)
eb+=num(80,262,1,SEA)+num(80,170,2,SEA)+num(275,40,3,SUN)+num(740,236,4,SEA)
cf=card(svgi(764,300,fb,'Motore fuoribordo con le prese d\'acqua sul piede e il getto della spia di raffreddamento',dw=764,dh=300)+h3('Fuoribordo',30)+p('<b>1</b> prese d\'acqua sul piede · <b>2</b> la <b>spia</b>: il getto conferma che il circuito funziona. Mai far girare il motore con la presa fuori dall\'acqua: si danneggia la girante.',24),None,24,10)
ce=card(svgi(764,300,eb,'Schema del raffreddamento entrobordo: presa a mare, pompa con girante, scambiatore di calore, scarico',dw=764,dh=300)+h3('Entrobordo',30)+p('<b>1</b> presa a mare · <b>2</b> pompa con girante · <b>3</b> scambiatore: l\'acqua di mare raffredda il liquido del circuito chiuso del motore · <b>4</b> scarico.',24),None,24,10)
sec('raffreddamento', head('Il motore va raffreddato','Il raffreddamento')+f'<div style="display:flex; gap:24px">{cf}{ce}</div>',
 notes='Quiz 1.2.1-4 (girante danneggiata se la presa è fuori dall\'acqua), -13 (scambiatore di calore), -37 e -38 (figure: prese d\'acqua e spia), -8 (causa più comune di surriscaldamento: presa a mare occlusa), 1.2.2-11 (alghe e plastica sulla presa del fuoribordo).')

quiz_slide('quiz1','Quiz 1 · Il motore',['1.2.1-6','1.2.1-14','1.2.1-13'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.2.1-6','1.2.1-14','1.2.1-13'],True)

# ============ AVARIE ============
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
a1=av(smoke('#2B2F36'),'Fumo nero','Benzina: cattiva combustione, carburazione difettosa. Diesel: pompa di iniezione, filtro aria intasato.')+av(smoke('#7FB3E6'),'Fumo azzurro','Olio lubrificante entrato nella camera di scoppio.')+av(smoke('#FFFFFF','#9DB9F2'),'Diesel: fumo blu o bianco','Filtro dell\'olio intasato, turbina di sovralimentazione difettosa.')
a1+=av(ico('key'),'Benzina: gira ma non parte','Manca carburante, carburatore sporco o ingolfato, candele deteriorate.')+av(ico('air'),'Diesel: gira ma non parte','Aria nel circuito del carburante, filtro del carburante intasato.')+av(ico('air'),'Diesel: si spegne subito','Aria nella pompa di iniezione.')
sec('avarie1', head('Irregolarità e piccole avarie','Il motore ci parla: fumo e avviamento')+f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px">{a1}</div>',
 notes='Quiz 1.2.2-10 e -15 (fumo nero), -9 (fumo azzurro), -18 e -19 (fumi diesel), -14 (benzina non parte), -16 (diesel gira ma non si avvia), -8 (diesel si spegne subito), -17 (si avvia difficilmente: acqua nel carburante, scarico ostruito), -20 e -21 (accensione irregolare). Attenzione: 1.2.2-1 e 1.2.2-3 sono oscurati.')
a2=av(ico('temp'),'Surriscaldamento','Presa d\'acqua occlusa da alghe o plastica. Se dura: grippaggio, testata e guarnizioni danneggiate.')+av(ico('vib'),'Vibrazioni','Supporti del motore allentati o rotti; alghe o detriti sull\'elica.')+av(ico('prop'),'In folle va, in marcia si ferma','L\'elica è bloccata; se si ferma di colpo, l\'asse si è bloccato con l\'invertitore ingranato.')
a2+=av(ico('drop'),'Perde colpi e cala di giri','Carburante sporco nel serbatoio.')+av(ico('bang'),'Picchia in testa','Iniettori fuori taratura.')+av(ico('batt'),'Non parte e le luci si spengono','Batterie completamente scariche.')
sec('avarie2', head('Irregolarità e piccole avarie','Il motore ci parla: in navigazione')+f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px">{a2}</div>',
 notes='Quiz 1.2.2-11, -25, -26 (surriscaldamento), -22 e -27 (vibrazioni), -4 e -5 (elica o asse bloccati), 1.2.1-11 (perde colpi: carburante sporco), 1.2.2-2 (picchia in testa), -6 (batterie scariche), -12 (fuoribordo non parte: leva in folle).')

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

quiz_slide('quiz2','Quiz 2 · Avarie e autonomia',['1.2.2-9','1.2.2-5','1.2.3-7'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.2.2-9','1.2.2-5','1.2.3-7'],True)

# ============ ELICA ============
pf=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/><g transform="translate(210 130)">'+''.join(f'<path d="M0 0 Q-34 -40 -8 -104 Q30 -96 22 -22 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" transform="rotate({a})"/>' for a in (0,120,240))+f'<circle r="24" fill="{NAVY}"/><circle r="8" fill="{SUN}"/></g>'
pf+=arrow(346,60,236,120,INK,3)+arrow(80,220,150,172,INK,3)
ph=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/>'+line(30,190,400,190,'#7A8796',8)
ph+=f'<path d="M40 190 C 80 60, 140 60, 170 130 S 250 250, 300 130" fill="none" stroke="{PURPLE}" stroke-width="5" stroke-dasharray="12 8"/>'
ph+=dim(40,226,380,226,INK)+dim(40,244,300,244,CORAL)
pc=f'<rect x="0" y="0" width="420" height="260" rx="30" fill="#FFFFFF"/><g transform="translate(200 130)">'+''.join(f'<path d="M0 0 Q-34 -40 -8 -104 Q30 -96 22 -22 Z" fill="{NAVY}" transform="rotate({a})"/>' for a in (20,140,260))+f'<circle r="20" fill="{SEA}"/></g>'+''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{SEA}" stroke-width="3"/>' for x,y,r in [(300,60,10),(330,100,7),(320,150,12),(350,190,8),(290,210,6),(110,60,8),(90,190,10)])
e1=card(svgi(420,260,pf,'Elica vista da dietro: mozzo al centro e tre pale',dw=440,dh=272)+h3('Mozzo e pale',30)+p('Alluminio, acciaio inox o composito. A passo fisso, a pale abbattibili (il minor rendimento in marcia indietro) o a pale orientabili.',24),None,24,10)
e2=card(svgi(420,260,ph,'Percorso dell\'elica in un giro: il passo teorico è più lungo dell\'avanzamento reale, la differenza è il regresso',dw=440,dh=272)+h3('Passo e regresso',30)+p('<b>Passo teorico</b>: quanto l\'elica avanzerebbe in un giro se l\'acqua fosse solida. <b>Regresso</b>: la differenza con l\'avanzamento reale. Passo lungo e diametro piccolo: più velocità.',24),None,24,10)
e3=card(svgi(420,260,pc,'Elica circondata da bolle: la cavitazione',dw=440,dh=272)+h3('Cavitazione',30)+p('L\'elica supera il limite dei giri e perde spinta. Sul fuoribordo può dipendere da un piede non adatto all\'altezza dello specchio di poppa.',24),None,24,10)
sec('elica', head('L\'elica','Mozzo, pale, passo e regresso')+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}</div>',
 notes='Quiz 1.2.1-31 (mozzo e pale), -34 (materiali), 1.1.2-1 (pale abbattibili, minor rendimento indietro), -16 (passo teorico), -11 (regresso), -17 (passo lungo e diametro piccolo = più velocità), -24 e 1.2.2-13 (cavitazione). Nel disegno centrale: freccia blu = passo teorico, freccia rossa = avanzamento reale.')

# ============ ROTAZIONE ============
def sternview(cw):
    s=f'<path d="M110 30 L450 30 C450 120 380 170 280 180 C180 170 110 120 110 30 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="5"/><path d="M118 110 Q280 190 442 110 L450 130 C400 176 340 186 280 186 C220 186 160 176 110 130 Z" fill="{CORAL}" fill-opacity="0.9"/>'
    s+=line(280,180,280,214,NAVY,8)+f'<g transform="translate(280 250)">'+''.join(f'<ellipse cx="0" cy="-26" rx="12" ry="26" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+f'<circle r="10" fill="{SUN}"/></g>'
    s+=curved(280,250,70,-150,-30,SEA if cw else CORAL,7) if cw else curved(280,250,70,-30,-150,CORAL,7)
    return s
r1=card(svgi(560,340,sternview(True),'Vista da poppa: elica che gira in senso orario',dw=560,dh=340)+h3('Destrorsa',32)+p('Guardando la poppa dall\'esterno, in <b>marcia avanti</b> gira in senso <b>orario</b>; in marcia indietro in senso antiorario.',25),None,26,10)
r2=card(svgi(560,340,sternview(False),'Vista da poppa: elica che gira in senso antiorario',dw=560,dh=340)+h3('Sinistrorsa',32)+p('Guardando la poppa dall\'esterno, in <b>marcia avanti</b> gira in senso <b>antiorario</b>.',25),None,26,10)
sec('rotazione', head('L\'elica · il verso di rotazione','Elica destrorsa e sinistrorsa')+f'<div style="display:flex; gap:24px">{r1}{r2}</div>',
 notes='Quiz 1.1.2-7 (destrorsa: senso orario in marcia avanti vista da poppa), -15 e -33 (sinistrorsa: antiorario), -35 (destrorsa in marcia indietro: antiorario).')

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
sec('evolutivo', head('Elica e manovra','L\'effetto evolutivo dell\'elica')+f'<div style="display:flex; gap:24px">{v1}{v2}{v3}</div>',
 notes='Quiz 1.1.2-44 e -45 (marcia avanti: destrorsa prua a sinistra/poppa a dritta; sinistrorsa il contrario), -2, -12, -30 (destrorsa in retromarcia: poppa a sinistra), -4, -25, -40 (sinistrorsa in retromarcia: poppa a dritta), -39, -23 (massimo senza abbrivio), -8 (flusso contro timone e carena), -41 (si compensa col timone). Nel disegno la sagoma chiara è la barca dopo l\'accostata; freccia grigia = verso del moto.')

# ============ BIELICA ============
def twin(man):
    s=''
    if man: s+=topboat(300,230,300,-90+22,'#FFFFFF',NAVY,3,0.35,False)
    s+=topboat(300,230,300,-90,'#FFFFFF',NAVY,4)
    for x,cw in ((270,False),(330,True)):
        s+=f'<g transform="translate({x} 392)">'+''.join(f'<ellipse cx="0" cy="-9" rx="5" ry="11" fill="{NAVY}" transform="rotate({a})"/>' for a in (0,120,240))+'</g>'
    if not man:
        s+=curved(330,400,34,200,340,SEA,5)+curved(270,400,34,340,200,CORAL,5)
    else:
        s+=arrow(330,400,330,468,CORAL,7,22)+curved(300,230,190,-80,-52,SEA,7)
    return s
t1=card(svgi(600,480,twin(False),'Vista dall\'alto di una bielica: elica destrorsa a dritta, sinistrorsa a sinistra',dw=520,dh=416)+h3('Eliche controrotanti',30)+p('Di norma <b>destrorsa a dritta</b> e <b>sinistrorsa a sinistra</b>: gli effetti laterali si compensano. Spesso con <b>timoni accoppiati</b>.',25),None,24,10)
t2=card(svgi(600,480,twin(True),'Solo il motore di dritta in marcia indietro: la prua accosta a dritta',dw=520,dh=416)+h3('Una marcia avanti, una indietro',30)+p('Solo il motore di <b>dritta in marcia indietro</b>: la <b>prora accosta a dritta</b>. Con i due motori in versi opposti la barca gira quasi su se stessa.',25),None,24,10)
sec('bielica', head('Elica e manovra','Due motori, due eliche')+f'<div style="display:flex; gap:24px">{t1}{t2}</div>',
 notes='Quiz 1.1.2-5, -3, -26, -43 (destrorsa a dritta, sinistrorsa a sinistra, per compensare l\'effetto laterale), -42 (timoni accoppiati), -29 (solo motore di dritta indietro: prora a dritta).')

quiz_slide('quiz3','Quiz 3 · L\'elica',['1.1.2-7','1.1.2-11','1.1.2-12'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.1.2-7','1.1.2-11','1.1.2-12'],True)

# ============ TIMONE ============
def rud(comp):
    s=f'<rect x="0" y="0" width="420" height="300" rx="30" fill="#FFFFFF"/><rect x="0" y="0" width="420" height="80" fill="{BOAT}"/><path d="M0 80 L420 60" stroke="{NAVY}" stroke-width="6"/>'
    ax=250 if comp else 180
    s+=dash(ax,20,ax,280,INK,3)+line(ax,40,ax,110,NAVY,10)
    if comp: s+=f'<path d="M{ax-60} 110 L{ax+120} 110 L{ax+110} 262 L{ax-50} 262 Z" fill="{SEA}" stroke="{NAVY}" stroke-width="4"/><path d="M{ax-60} 110 L{ax} 110 L{ax} 262 L{ax-50} 262 Z" fill="{SUN}" fill-opacity="0.8"/>'
    else: s+=f'<path d="M{ax} 110 L{ax+170} 110 L{ax+160} 262 L{ax} 262 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/>'
    s+=f'<text x="40" y="200" font-family="Arial" font-size="26" font-weight="700" fill="{SOFT}">prua ←</text>'
    return s
u1=card(svgi(420,300,rud(False),'Timone ordinario: tutta la pala sta a poppavia dell\'asse',dw=420,dh=300)+h3('Ordinario',30)+p('Tutta la <b>pala</b> sta a poppavia dell\'asse.',25),None,24,10)
u2=card(svgi(420,300,rud(True),'Timone compensato: una parte della pala, in giallo, sta a proravia dell\'asse',dw=420,dh=300)+h3('Compensato',30)+p('Una parte della pala è <b>a proravia dell\'asse</b>: serve meno forza su barra o ruota.',25),None,24,10)
u3=card(note('Cosa fa il timone',GREEN,40)+'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:12px"><li>Parti: <b>pala</b>, <b>asse</b>, e la <b>losca</b> da cui l\'asse entra nello scafo.</li><li>Massimo effetto con la pala a <b>30-40 gradi</b>.</li><li>Oltre all\'accostata: riduce la velocità, sposta la barca sul lato opposto alla pala, la fa leggermente appruare.</li></ul>',None,30,12)
sec('timone', head('Governare la barca','Il timone')+f'<div style="display:flex; gap:24px">{u1}{u2}{u3}</div>',
 notes='Quiz 1.1.1-56 (pala), -33 (losca), 1.1.2-36 (ordinario), -9, -10, -27, -37 e 1.1.1-55, -57 (compensato), 1.1.2-13 (30-40 gradi), -18 (effetti secondari del timone).')

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
w1=card(svgi(600,480,steer('ruota'),'Vista dall\'alto: ruota girata a sinistra, la prua va a sinistra',dw=520,dh=416)+h3('Ruota',30)+p('Giro la ruota <b>a sinistra</b>: la <b>prua va a sinistra</b> e la poppa a dritta.',25),None,24,10)
w2=card(svgi(600,480,steer('barra'),'Vista dall\'alto: barra spostata a sinistra, pala a dritta, la prua va a dritta',dw=520,dh=416)+h3('Barra',30)+p('Sposto la barra <b>a sinistra</b>: la pala va a dritta e la <b>prua va a dritta</b>. In marcia indietro, barra a dritta: poppa a sinistra.',25),None,24,10)
w3=card(note('E il fuoribordo?',BLUE,40)+p('Si governa ruotando il piede: <b>piede a dritta</b> in marcia avanti, <b>la poppa va a sinistra</b>.',26,INK)+note('Punto di rotazione',BLUE,40)+p('In marcia avanti la barca ruota attorno a un punto spostato <b>verso prua</b>: la poppa «scoda» all\'esterno della curva di evoluzione.',26,INK),None,30,12)
sec('barraruota', head('Governare la barca','Barra e ruota')+f'<div style="display:flex; gap:24px">{w1}{w2}{w3}</div>',
 notes='Quiz 1.1.2-32 e -14 (ruota a sinistra: prora a sinistra, poppa a dritta), -20 (barra in marcia indietro), -34 (fuoribordo: piede a dritta, poppa a sinistra), -6 (punto di rotazione verso prua), -19 (curva di evoluzione). Il quiz 1.1.2-31 sulla barra è oscurato, ma il principio resta.')

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
sec('combinati', head('Elica + timone','Effetti combinati elica e timone')+f'<div style="display:flex; gap:24px">{k1}{k2}{k3}</div>',
 notes='Quiz 1.1.2-21 (ormeggio di poppa con sinistrorsa), -22 (all\'inglese con destrorsa, banchina a sinistra), -28 (timone a dritta in retro con destrorsa), -38 (avaria al timone: remo a sinistra). Le prove pratiche dell\'All. D chiedono proprio gli effetti di timone ed elica in marcia avanti e indietro.')

quiz_slide('quiz4','Quiz 4 · Il timone',['1.1.2-10','1.1.2-14','1.1.2-29'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.1.2-10','1.1.2-14','1.1.2-29'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.2.1-9','1.2.1-4','1.2.1-3'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.2.1-9','1.2.1-4','1.2.1-3'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.2.3-6','1.1.2-23','1.1.2-13'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.2.3-6','1.1.2-23','1.1.2-13'],True)
closing(['Motore + elica = sistema propulsivo; l\'invertitore cambia marcia, non il verso del motore','4 tempi: aspirazione, compressione, scoppio, scarico','Benzina: aerare il vano motore; diesel: niente aria nel circuito','Carburante = consumo orario × ore + 30%','Destrorsa in retro: la poppa va a sinistra; si compensa col timone'],
 'Prossima lezione · 03 · Ormeggi, cartografia e primi calcoli','A casa: i 104 quiz ufficiali di Motori e i 50 su elica, timone e stabilità.')
write_deck(OUT,'Lezione 02 · Motori, elica e timone',
 ['cover','agenda','installazioni','lineaasse','quattrotempi','benzinadiesel','raffreddamento','quiz1','quiz1r','avarie1','avarie2','manutenzione','carburante','autonomia','quiz2','quiz2r',
  'elica','rotazione','evolutivo','bielica','quiz3','quiz3r','timone','barraruota','combinati','quiz4','quiz4r','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Il motore: installazioni, trasmissione, funzionamento e raffreddamento","start":"installazioni"},
  "s3":{"description":"Avarie, manutenzione e calcolo dell'autonomia","start":"avarie1"},"s4":{"description":"Elica: passo, rotazione, effetto evolutivo, bielica","start":"elica"},
  "s5":{"description":"Timone ed effetti combinati, verifica finale","start":"timone"}})
