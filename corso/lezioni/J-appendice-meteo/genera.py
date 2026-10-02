"""Appendice J: i bollettini meteo e i segni del tempo (quiz 1.6.2, 1.6.1, 1.8.1)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
ORDER=['cover','indice','fonti','meteomar','esempio','orari','quizA','quizAr',
       'beaufort','douglas','vento','onde','quizB','quizBr',
       'barometro','cielo','fronti','decidere','quizC','quizCr','chiusura']
EB='Appendice J · I bollettini meteo'
LB.ICON_T.update({'Indice':'book','Dove si trovano le previsioni':'cloud','Com\'è fatto il Meteomar':'cloud','Un Meteomar da leggere':'cloud',
 'UTC e ora italiana':'check','La forza del vento':'wind','Lo stato del mare':'wind','Come soffia il vento':'wind','Le onde del bollettino':'wind',
 'Leggere il barometro':'chart','I segni del cielo':'cloud','I fronti in arrivo':'cloud','Uscire o restare in porto?':'flag'})

cover_app('J','I bollettini meteo','Dove si trovano, come si leggono, le scale del vento e del mare, il barometro, il cielo e la decisione di uscire',
 'Appendice J al corso. Ripasso della meteorologia pratica: quiz ufficiali 1.6.2 (bollettini, segni del tempo, fronti, onde), 1.6.1 (scale), 1.8.1 (categorie di progettazione). Collegata alla lezione 7 e all\'appendice H (Meteomar via radio).')
index_slide(EB,[('Il bollettino','Fonti, Meteomar, un esempio, UTC',['fonti','meteomar','esempio','orari','quizA','quizAr'],CORAL),
 ('Vento e mare','Beaufort, Douglas, raffiche, onde',['beaufort','douglas','vento','onde','quizB','quizBr'],SEA),
 ('Il tempo che cambia','Barometro, cielo, fronti, la decisione',['barometro','cielo','fronti','decidere','quizC','quizCr'],PURPLE)],ORDER,
 'Si ascolta prima di partire, e si riascolta in navigazione.',
 'Appendice di ripasso per usare davvero il bollettino: sapere dove trovarlo, leggerlo, tradurre forza del vento e stato del mare, e confrontarlo con quello che si vede.')

sec('fonti', head('Il bollettino','Dove si trovano le previsioni',CORAL)+table(['Fonte','Che cosa è'],[34,66],[
 ('Chi le prepara','Il Centro Nazionale di Meteorologia e Climatologia Aeronautica'),
 ('Meteomar','Il bollettino per il mare, sul canale VHF 68 di continuo, dalle stazioni radio costiere'),
 ('Avvisi di burrasca','Burrasca o tempesta in corso o imminente: via radio, preceduti da SÉCURITÉ, con precedenza su tutto'),
 ('Radioservizi per la navigazione','Il volume dell\'IIM con orari e canali dei bollettini'),
 ('Carte meteorologiche','Al suolo (isobare e fronti) e in quota')],CORAL,28)
 +note('La burrasca è una forza del vento, non un generico «brutto tempo».',CORAL,36),
 notes='Quiz 1.6.2-1 (CNMCA), -17 e -20 (Meteomar sul 68 dalle stazioni costiere), -2, -14, -15, -21 (avvisi), -23 (Radioservizi), -9 (carte al suolo e in quota), -24 (burrasca: termine della forza del vento). Il Meteomar si trova anche sui siti ufficiali e viene letto in italiano e in inglese.')

# ============ COM'È FATTO: la linea del tempo ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
x0,x1=70,1030; hx=lambda h: x0+(x1-x0)*h/24
b+=f'<rect x="{hx(0):.0f}" y="250" width="{hx(12)-hx(0):.0f}" height="100" rx="16" fill="{SEA}"/>'
b+=f'<rect x="{hx(12):.0f}" y="250" width="{hx(24)-hx(12):.0f}" height="100" rx="16" fill="{PURPLE}"/>'
for h,t in ((0,'12 UTC'),(12,'00 UTC'),(24,'12 UTC')):
    b+=line(hx(h),220,hx(h),380,NAVY,4)
b+=f'<circle cx="{hx(0):.0f}" cy="160" r="30" fill="{CORAL}"/>'+arrow(hx(0),192,hx(0),246,CORAL,5,16)
b+=f'<rect x="60" y="440" width="960" height="130" rx="20" fill="#FFFFFF" stroke="#DDE6EC" stroke-width="3"/>'
lbl=lab(X+hx(0)-70,Y+390,140,'oggi 12 UTC',NAVY,24,900,'center')+lab(X+hx(12)-70,Y+390,140,'00 UTC',NAVY,24,900,'center')+lab(X+hx(24)-190,Y+390,200,'domani 12 UTC',NAVY,24,900,'right')
lbl+=lab(X+hx(0)+20,Y+280,420,'PREVISIONE · validità',LWHITE,28,900)+lab(X+hx(12)+20,Y+280,420,'TENDENZA · 12 ore dopo','#FFFFFF',28,900)+lab(X+hx(0)+50,Y+140,300,'emissione',CORAL,26,900)
lbl+=''.join(pill(X+80+i*240,Y+490,230,t,c,24) for i,(t,c) in enumerate((('1 · Avvisi',LRED),('2 · Situazione',ORANGE),('3 · Previsione',SEA),('4 · Tendenza',PURPLE))))+lab(X+80,Y+452,700,'Le parti del bollettino, in ordine:',INK,24,800)
txt=(item(1,LRED,'Avvisi','Prima di tutto: burrasche e temporali in corso o previsti.')
     +item(2,SEA,'Situazione e previsione','Dove sono alte e basse pressioni; per ogni zona vento (direzione e forza) e stato del mare.')
     +item(3,PURPLE,'Tendenza','Vento e mare nelle 12 ore dopo la fine della validità.'))
sec('meteomar', head('Il bollettino','Com\'è fatto il Meteomar',CORAL), pinned=svgp(X,Y,W,Hh,b,'Linea del tempo: il bollettino emesso alle 12 UTC di oggi vale fino alle 00 UTC di domani; la tendenza copre le 12 ore successive, fino alle 12 UTC di domani; sotto le quattro parti del bollettino')+lbl+pcol(txt,532,22),
 notes='Quiz 1.6.2-16 (il Meteomar contiene avvisi in corso o previsti), -18 (emesso alle 12 UTC, vale fino alle 00 UTC di domani), -19 e -22 (tendenza del mare e del vento nelle 12 ore successive alla validità).')
X=700

ES=[('AVVISI: burrasca forte da maestrale, forza 8, su Mar di Sardegna','k'),('SITUAZIONE: bassa pressione sul Golfo di Genova in approfondimento','n'),
    ('MAR LIGURE: vento da ovest forza 5, in rinforzo a 6 · mare molto mosso','m'),('MAR DI SARDEGNA: maestrale forza 7, localmente 8 · mare agitato','m'),
    ('TENDENZA: maestrale in attenuazione · mare in diminuzione','e')]
key=[('Avviso','Qui, in Sardegna, non si esce',LRED),('Situazione','La causa: una bassa pressione',ORANGE),('Vento','Da dove e quanto: Beaufort',SEA),('Mare','Stato del mare: Douglas',BLUE),('Tendenza','Come cambierà dopo',PURPLE)]
kk=''.join(f'<div style="display:flex; gap:14px; align-items:center">{dot(i+1,c)}<div style="display:flex; flex-direction:column">{p(t,28,INK,800,1.2)}{p(d,24,BODY,400,1.3)}</div></div>' for i,(t,d,c) in enumerate(key))
sec('esempio', head('Il bollettino','Un Meteomar da leggere',CORAL)+f'<div style="display:flex; gap:32px; align-items:start">{script("ESEMPIO · CANALE 68",ES,900)}<div style="flex:1; display:flex; flex-direction:column; gap:16px">{kk}</div></div>',
 notes='Esempio inventato per esercitarsi: le zone esistono, i dati no. Si legge così: prima gli avvisi, poi la zona in cui si naviga e quelle vicine da cui arriva il vento. Un\'imbarcazione di categoria C è progettata per vento fino a forza 6 e onde fino a 2 m (1.8.1-117): con forza 7-8 si resta in porto.')

sec('orari', head('Il bollettino','UTC e ora italiana',CORAL)+bignums([
 ('UTC','Il tempo universale: tutti i bollettini lo usano.',CORAL),
 ('+1','Ora solare, d\'inverno: 12 UTC sono le 13.',SEA),
 ('+2','Ora legale, d\'estate: 12 UTC sono le 14.',PURPLE)])
 +table(['Nel bollettino','In inverno','In estate'],[40,30,30],[('00 UTC','01:00','02:00'),('06 UTC','07:00','08:00'),('12 UTC','13:00','14:00'),('18 UTC','19:00','20:00')],CORAL,28),
 gap=28, notes='La conversione è la regola generale del tempo universale coordinato. Serve per capire fino a quando vale il bollettino (1.6.2-18): un Meteomar delle 12 UTC valido fino alle 00 UTC d\'estate vale fino alle 2 di notte, ora italiana.')

quiz_slide('quizA','Verifica · il bollettino',['1.6.2-17','1.6.2-18','1.6.2-21'],False)
quiz_slide('quizAr','Verifica · il bollettino',['1.6.2-17','1.6.2-18','1.6.2-21'],True)

BF=[(0,'Calma','meno di 1'),(1,'Bava di vento','1–3'),(2,'Brezza leggera','4–6'),(3,'Brezza tesa','7–10'),(4,'Vento moderato','11–16'),(5,'Vento teso','17–21'),(6,'Vento fresco','22–27'),
    (7,'Vento forte','28–33'),(8,'Burrasca moderata','34–40'),(9,'Burrasca forte','41–47'),(10,'Tempesta','48–55'),(11,'Tempesta violenta','56–63'),(12,'Uragano','64 e oltre')]
def bfcell(f,t,k):
    c=GREEN if f<=4 else (BLUE if f<=6 else (ORANGE if f<=8 else LRED))
    return f'<div style="display:flex; align-items:center; gap:12px; background:#FFFFFF; border-left:10px solid {c}; border-radius:16px; padding:16px 16px"><p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:64px">{f}</p><div style="display:flex; flex-direction:column">{p(t,28,INK,800,1.15)}{p(k+" nodi",26,BODY,500,1.2)}</div></div>'
NODO=p("1 nodo = 1 miglio all'ora = 1,852 km/h",24,INK,700)
sec('beaufort', head('Vento e mare','La forza del vento',SEA)+f'<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px">{"".join(bfcell(*r) for r in BF)}<div style="display:flex; flex-direction:column; justify-content:center; gap:6px; background:{SEA_T}; border-radius:16px; padding:12px 16px">{p("<b>Scala Beaufort</b> · 0–12",26,INK)}{p("Categoria D fino a 4 · C fino a 6 · B fino a 8",24,INK)}</div><div style="display:flex; flex-direction:column; justify-content:center; background:{LILAC_T}; border-radius:16px; padding:12px 16px">{NODO}</div><div></div></div>',
 gap=24, notes='Quiz 1.6.1-1 (scala Beaufort), -40 (vento 0-12, mare 0-9), 1.6.2-24 (burrasca = forza del vento), 1.8.1-116, -117, -119 (categorie di progettazione B, C, D). Nodi secondo la scala dell\'Organizzazione meteorologica mondiale, come nella lezione 7.')

DG=[(0,'Calmo','0 m'),(1,'Quasi calmo','fino a 0,1 m'),(2,'Poco mosso','0,1–0,5 m'),(3,'Mosso','0,5–1,25 m'),(4,'Molto mosso','1,25–2,5 m'),
    (5,'Agitato','2,5–4 m'),(6,'Molto agitato','4–6 m'),(7,'Grosso','6–9 m'),(8,'Molto grosso','9–14 m'),(9,'Tempestoso','oltre 14 m')]
def dgcell(f,t,k):
    c=GREEN if f<=3 else (BLUE if f<=4 else (ORANGE if f<=6 else LRED))
    return f'<div style="display:flex; align-items:center; gap:12px; background:#FFFFFF; border-left:10px solid {c}; border-radius:18px; padding:26px 18px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}; width:56px">{f}</p><div style="display:flex; flex-direction:column; gap:4px">{p(t,30,INK,800,1.15)}{p("onde "+k,26,BODY,500,1.2)}</div></div>'
sec('douglas', head('Vento e mare','Lo stato del mare',SEA)+f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:14px">{"".join(dgcell(*r) for r in DG)}</div>'
    +note('Nel bollettino: «mare molto mosso» vuol dire onde fino a 2,5 m. Categoria C: fino a 2 m.',SEA,34),
 gap=28, notes='Scala Douglas del mare, da 0 a 9 (quiz 1.6.1-40); le altezze sono quelle dell\'onda significativa secondo l\'Organizzazione meteorologica mondiale. Categorie di progettazione: D fino a 0,3 m (occasionalmente 0,5), C fino a 2 m, B fino a 4 m (1.8.1-116, -117, -119).')

sec('vento', head('Vento e mare','Come soffia il vento',SEA)+grid([
 ('Teso','Direzione e velocità media restano costanti per un certo tempo.',SEA),
 ('A raffiche','La direzione resta, ma arrivano picchi di almeno 10 nodi sopra la media, per meno di un minuto.',LRED),
 ('Isobare fitte','Più le isobare sono vicine, più il vento è forte.',PURPLE),
 ('1013,2 hPa','La pressione media al livello del mare.',BLUE),
 ('Foehn','Vento che scende lungo il versante sottovento di una montagna: caldo e secco.',ORANGE),
 ('Le brezze','Di giorno dal mare, di notte da terra: la terra si scalda e si raffredda prima del mare.',GREEN)],3,32,26),
 notes='Quiz 1.6.2-36 (vento teso), -37 (raffiche), -53 (gradiente barico), -47 (1013,2 hPa), -38 (Foehn), 1.6.1-24 (brezza di mare). Nel bollettino «raffiche» vuol dire che il vento reale può superare di molto quello medio indicato.')

sec('onde', head('Vento e mare','Le onde del bollettino',SEA)+table(['Parola','Che cosa vuol dire'],[30,70],[
 ('Mare vivo','Onde fatte dal vento che soffia qui, adesso'),
 ('Mare lungo','Onde arrivate da lontano, dove c\'è un mare vivo'),
 ('Mare vecchio','Onde che restano quando il vento che le ha fatte è finito'),
 ('Fetch','Il tratto di mare libero su cui soffia il vento: più è lungo, più le onde crescono'),
 ('Altezza e lunghezza','Dal cavo alla cresta; da una cresta all\'altra'),
 ('Onda che frange','Ripidità oltre 1/7, o fondale meno del doppio dell\'altezza')],SEA,28),
 notes='Quiz 1.6.2-39 (il moto ondoso lo provoca il vento), -44 (mare vivo), -45 (mare lungo), -46 (mare vecchio o morto), -29 (fetch), -40 e -41 (lunghezza e altezza), -42 e -43 (quando l\'onda frange). Un mare lungo può arrivare anche con il bollettino che dà vento debole: guarda anche la zona da cui viene.')

quiz_slide('quizB','Verifica · vento e mare',['1.6.1-40','1.6.2-37','1.6.2-45'],False)
quiz_slide('quizBr','Verifica · vento e mare',['1.6.1-40','1.6.2-37','1.6.2-45'],True)

# ============ BAROMETRO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
for i in range(7): b+=line(60,80+i*70,1060,80+i*70,'#DDE6EC',2)
b+=line(60,290,1060,290,NAVY,3)+''.join(line(60+i*125,70,60+i*125,500,'#DDE6EC',2) for i in range(9))
pts=[(60,250),(185,245),(310,248),(380,300),(450,380),(520,430),(560,438),(600,330),(640,260),(700,230),(820,220),(940,212),(1060,205)]
b+=f'<path d="M{pts[0][0]} {pts[0][1]} '+' '.join(f'L{x} {y}' for x,y in pts[1:])+f'" fill="none" stroke="{CORAL}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
b+=num(200,210,1,GREEN,22)+num(440,450,2,LRED,22)+num(610,260,3,PURPLE,22)+num(900,170,4,SEA,22)
lbl=lab(X+10,Y+276,50,'1013',NAVY,22,900,'right')+lab(X+60,Y+520,1000,'giorni e ore →',SOFT,24,800,'center')+lab(X+70,Y+20,300,'pressione (hPa)',SOFT,24,800)
txt=(item(1,GREEN,'Stabile o sale piano','Il bel tempo dura, soprattutto se la sera il sole è rosso e il cielo chiaro.')
     +item(2,LRED,'Cala in fretta','Arriva brutto tempo: un fronte caldo, una bassa pressione, vento in rinforzo.')
     +item(3,PURPLE,'Sale di colpo','Passa un fronte freddo: raffiche, rovesci, poi il cielo si apre.')
     +item(4,SEA,'Venti del I e IV quadrante','Aria fredda da Nord: la pressione sale.'))
sec('barometro', head('Il tempo che cambia','Leggere il barometro',PURPLE), pinned=svgp(X,Y,W,Hh,b,'Grafico della pressione nel tempo: prima stabile, poi un calo rapido fino al minimo, poi una risalita brusca e infine una salita lenta e stabile')+lbl+pcol(txt,532,18),
 notes='Quiz 1.6.2-3 (bel tempo: pressione costante o in lenta salita, sole rosso la sera), -4 e -7 (peggioramento: brusca caduta della pressione), -48 (prima di un fronte caldo la pressione cade), -49 e -32 (salita brusca: fronte freddo, raffiche), -5 (miglioramento: rapido aumento della pressione), -30 (venti freddi del IV e I quadrante: la pressione aumenta). Conta più la tendenza del valore: guardare il barometro ogni poche ore.')
X=700

sec('cielo', head('Il tempo che cambia','I segni del cielo',PURPLE)+table(['Che cosa vedi','Che cosa aspettarti'],[56,44],[
 ('Pressione stabile, sole rosso la sera, cielo chiaro','Il bel tempo continua'),
 ('Cirri che si addensano in cirrostrati, pressione in calo, vento già al mattino','Peggioramento'),
 ('Nubi che si alzano, vento che gira da Est a Sud e a Ovest, pressione in salita','Miglioramento'),
 ('Cirri rossastri, nubi fitte, pressione in calo, vento da Sud in rinforzo','Pioggia'),
 ('Aria calda e umida su acqua fredda, vento debole','Nebbia (visibilità sotto 1 km)'),
 ('Cumulonembi: nubi alte a sviluppo verticale','Temporale, raffiche, rovesci')],PURPLE,26),
 notes='Quiz 1.6.2-3, -4, -5, -6, -8 (segni premonitori), -25 (cirri: bel tempo se la pressione è stabile o sale), -28 e -31 (cumuli e cumulonembi), -26 (la violenza di un temporale dipende dallo sviluppo verticale), -52 (nebbia sotto 1 km, foschia sopra), -33 e -34 (aria instabile: rovesci, buona visibilità).')

sec('fronti', head('Il tempo che cambia','I fronti in arrivo',PURPLE)+table(['Fronte','Prima','Al passaggio'],[20,36,44],[
 ('Caldo','La pressione cade rapidamente; nubi sempre più basse','Piogge leggere e continue'),
 ('Freddo','Vento da Sud, pressione in calo','Cumulonembi, rovesci, temporali, raffiche; poi la pressione sale di colpo'),
 ('Stazionario','—','Stallo: maltempo che dura'),
 ('Occluso','Il freddo ha raggiunto il caldo','Tempo perturbato, come un misto dei due')],PURPLE,28)
 +note('Un fronte è la superficie di contatto tra due masse d\'aria diverse.',PURPLE,36),
 notes='Quiz 1.6.2-27 (definizione di fronte), -48 e -50 (fronte caldo), -32, -49, -51 (fronte freddo), -35 (fronte stazionario), -10…-13 (figure dei fronti sulle carte). La descrizione del fronte occluso è quella di base della lezione 7.')

sec('decidere', head('Il tempo che cambia','Uscire o restare in porto?',PURPLE)+steps([
 ('Ascolta','Il Meteomar sul 68 o sui siti ufficiali: prima gli avvisi.',CORAL),
 ('Confronta','Forza del vento e stato del mare con la categoria della barca e con l\'esperienza di chi è a bordo.',SEA),
 ('Guarda fuori','Barometro, cielo, vento: confermano il bollettino?',PURPLE),
 ('Pianifica','Un ridosso lungo la rotta, un porto di rifugio, l\'ora di rientro.',BLUE),
 ('Riascolta','In navigazione: il tempo cambia, anche il piano.',GREEN)],24)
 +note('Nel dubbio si resta in porto: il mare aspetta.',PURPLE,38),
 notes='Categorie di progettazione CE: D fino a forza 4 e onde 0,3 m, C fino a forza 6 e 2 m, B fino a forza 8 e 4 m (1.8.1-116, -117, -119); sono limiti di progetto, non obiettivi. Quiz 1.4.3-2 (prima di ancorare: meteo e divieti), 1.3.8-2 (brusco peggioramento: preparare la barca), 1.7.5-4 (criterio di sicurezza: stare lontani dai pericoli meteorologici).')

quiz_slide('quizC','Verifica · il tempo che cambia',['1.6.2-49','1.6.2-7','1.6.2-52'],False)
quiz_slide('quizCr','Verifica · il tempo che cambia',['1.6.2-49','1.6.2-7','1.6.2-52'],True)

closing(['Meteomar sul canale 68; gli avvisi di burrasca arrivano con SÉCURITÉ',
         'Emesso alle 12 UTC vale fino alle 00 UTC; poi 12 ore di tendenza',
         'Vento: Beaufort 0–12. Mare: Douglas 0–9',
         'Pressione che cala in fretta: peggiora. Sale di colpo: fronte freddo',
         'Categoria della barca ed esperienza decidono se si esce'],
 'Buon vento, e buon tempo!','Appendice J · I bollettini meteo')
write_deck(OUT,'Appendice J · I bollettini meteo',ORDER,
 {"s1":{"description":"Il bollettino: fonti, Meteomar, esempio, UTC","start":"cover"},
  "s2":{"description":"Vento e mare: Beaufort, Douglas, raffiche, onde","start":"beaufort"},
  "s3":{"description":"Barometro, cielo, fronti e la decisione di uscire","start":"barometro"}})
