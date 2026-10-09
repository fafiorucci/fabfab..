"""Appendice M: la portanza, dall'ala alla vela (quiz vela 2.1.1, 2.3.1). Disegni dal flusso calcolato in flow_lines.json."""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
FL=json.load(open(SP+'/flow_lines.json'))
ORDER=['cover','indice','controvento','forza','mano','newton','bernoulli','mito','quizA','quizAr',
       'viscosita','vortice','magnus','energia',
       'incidenza','stallo','fattori','ala','scomposizione','deriva','indotta','quizB','quizBr',
       'andature','filetti','posfiletti','grasso','fessura','autostrada','quizC','quizCr','web','chiusura']
EB='Appendice M · La portanza'
LB.ICON_T.update({'Indice':'book','Portanza e resistenza':'wind','La mano fuori dal finestrino':'wind','Deviare l\'aria: Newton':'wind',
 'Le pressioni: Bernoulli':'chart','Il mito del percorso più lungo':'star','L\'angolo di incidenza':'compass','Lo stallo':'wind',
 'Da cosa dipende la portanza':'chart','La vela è un\'ala':'sail','Propulsione e scarroccio':'sail','Anche la deriva è un\'ala':'hull',
 'Portanza e andature':'sail','I filetti':'flag','Grasso e magro':'sail','Fiocco e randa: la fessura':'sail','Vero o falso? Web e libri a confronto':'book',
 'Risalire il vento':'compass','Senza viscosità niente portanza':'wind','Il vortice di partenza':'wind','L\'effetto Magnus':'wind',
 'Il vento cede energia':'chart','Resistenza indotta e vortici':'wind','Dove mettere i filetti':'flag','Il cantiere in autostrada':'map'})
ROM='Laura Romanò, «La fisica in barca a vela», cap. 4 «La portanza»'
def fonte(par,extra=''):
    e=f'; {extra}' if extra else ''
    return f'<p style="font-size:20px; line-height:1.35; font-style:italic; color:{BODY}">Fonte: L. Romanò, <i>La fisica in barca a vela</i>, {par}{e}</p>'
FLOW='#6FB7C2'

# ---------------- disegni ----------------
def T(x,y,s,cx,cy): return cx+s*x, cy-s*y
def flow_lines(k,s,cx,cy,c=FLOW,w=3,op=1.0,skip=(),n=90):
    out=''
    for i,L in enumerate(FL[k]['lines']):
        if i in skip: continue
        pts=L['pts']; st=max(1,len(pts)//n)
        pp=pts[::st]+[pts[-1]]
        d='M'+' L'.join(f'{T(x,y,s,cx,cy)[0]:.1f} {T(x,y,s,cx,cy)[1]:.1f}' for x,y in pp)
        out+=f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round"/>'
    return out
def body(k,s,cx,cy,fill=NAVY,st=None,sw=0):
    pts=FL[k]['surface']
    d='M'+' L'.join(f'{T(p[0],p[1],s,cx,cy)[0]:.1f} {T(p[0],p[1],s,cx,cy)[1]:.1f}' for p in pts)+' Z'
    stroke=f' stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"' if st else ''
    return f'<path d="{d}" fill="{fill}"{stroke}/>'
def pressure(k,s,cx,cy,sc=34,cmax=2.2,step=2):
    out=''
    for p in FL[k]['surface'][::step]:
        x,y,cp,nx,ny=p
        if abs(cp)<0.08 or abs(cp)>3.5: continue
        cp=max(-cmax,min(cmax,cp)); L=sc*abs(cp)
        X0,Y0=T(x,y,s,cx,cy); ex,ey=nx,-ny
        if cp<0: out+=arrow(X0+ex*6,Y0+ey*6,X0+ex*(6+L),Y0+ey*(6+L),CORAL,3,10)
        else: out+=arrow(X0+ex*(6+L),Y0+ey*(6+L),X0+ex*6,Y0+ey*6,BLUE,3,10)
    return out
def wind(x,y,l=110,c=GREY,w=9): return arrow(x,y,x+l,y,c,w,28)
def lead(k):
    pts=FL[k]['surface']; p=min(pts,key=lambda q:q[0]); return p[0],p[1]
def trail(k):
    pts=FL[k]['surface']; p=max(pts,key=lambda q:q[0]); return p[0],p[1]

# ============ COVER E INDICE ============
cover_app('M','La portanza','Perché un\'ala vola e una vela spinge la barca controvento: pressioni, viscosità e vortici, incidenza e stallo, filetti e fessura tra fiocco e randa',
 'Appendice M al corso. La teoria della portanza spiegata passo per passo e applicata alla vela, con i quiz ufficiali di vela 2.1.1 e 2.3.1. Fonte principale: '+ROM+' (paragrafi 4.1–4.6), citata slide per slide. Confronto con le spiegazioni che circolano sul web (NASA, Arvel Gentry). Collegata alla lezione 8.')
index_slide(EB,[('Che cos\'è la portanza','Controvento, forza, Newton, Bernoulli e il mito del percorso più lungo',['controvento','forza','mano','newton','bernoulli','mito','quizA','quizAr'],CORAL),
 ('Come nasce la portanza','Viscosità, vortice di partenza, effetto Magnus, energia del vento',['viscosita','vortice','magnus','energia'],ORANGE),
 ('Da cosa dipende','Incidenza, stallo, velocità e superficie',['incidenza','stallo','fattori'],SEA),
 ('La vela è un\'ala','Pressioni, propulsione e scarroccio, deriva, resistenza indotta',['ala','scomposizione','deriva','indotta','quizB','quizBr'],PURPLE),
 ('In pratica','Andature, filetti, grasso, fessura e il cantiere in autostrada, web e libri',['andature','filetti','posfiletti','grasso','fessura','autostrada','quizC','quizCr','web'],BLUE)],ORDER,
 'Fonte: L. Romanò, «La fisica in barca a vela», cap. 4 · NASA · A. Gentry',
 'Appendice di approfondimento sulla portanza. Fonte principale: '+ROM+'. I disegni del flusso sono calcolati: linee di corrente e pressioni di un profilo alare in un fluido ideale (profilo di Joukowski con la condizione di Kutta), più il cilindro rotante per l\'effetto Magnus.')

# ============ CONTROVENTO (disegno a destra) ============
X=700
Ox,Oy=420,560
ang=[(27,500,CORAL,'27° · Luna Rossa'),(30,430,PURPLE,'30° · barche da regata'),(35,360,SEA,'35° · yacht da diporto'),(50,300,ORANGE,'50° · vascelli del \'700')]
def ray(t,L): return Ox+L*math.sin(math.radians(t)), Oy-L*math.cos(math.radians(t))
sx1,sy1=ray(-35,380); sx2,sy2=ray(35,380)
b=(f'<path d="M{Ox} {Oy} L{sx1:.0f} {sy1:.0f} A380 380 0 0 1 {sx2:.0f} {sy2:.0f} Z" fill="{CORAL}" fill-opacity="0.10"/>'
   +arrow(Ox,20,Ox,130,GREY,10,30))
lbl=lab(X+Ox+24,Y+40,200,'vento',INK,24,800)+lab(X+Ox-170,Y+Oy-280,200,'qui non si va',CORAL,24,900,'center')
for t,L,c,tx in ang:
    ex,ey=ray(t,L)
    b+=f'<path d="M{Ox} {Oy} L{ex:.0f} {ey:.0f}" stroke="{c}" stroke-width="6" stroke-linecap="round"/><circle cx="{ex:.0f}" cy="{ey:.0f}" r="11" fill="{c}"/>'
    lbl+=lab(X+ex+20,Y+ey-18,330,tx,c,24,900)
ex,ey=ray(-35,360)
b+=f'<path d="M{Ox} {Oy} L{ex:.0f} {ey:.0f}" stroke="{SEA}" stroke-width="6" stroke-dasharray="14 10" stroke-linecap="round"/>'
b+=(f'<g transform="translate({Ox} {Oy}) rotate(35)"><path d="M0 -54 Q20 -20 18 30 L-18 30 Q-20 -20 0 -54 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
    f'<path d="M0 -24 Q14 0 10 22" fill="none" stroke="{NAVY}" stroke-width="4"/></g>')
b+=(f'<path d="M{Ox-60} {Oy-86} A105 105 0 0 1 {Ox+60} {Oy-86}" fill="none" stroke="{NAVY}" stroke-width="3"/>')
lbl+=lab(X+20,Y+196,180,'sull\'altra mura',SEA,24,900,'right')
txt=(item(1,ORANGE,'Già nel \'700','I vascelli a vele quadre risalivano il vento fino a circa 50°.')
     +item(2,SEA,'Le vele di taglio','Uno yacht da diporto stringe a circa 35°, le barche da regata a 30°, Luna Rossa a 27°.')
     +item(3,PURPLE,'In fil di ruota','La forza del vento ha la stessa direzione del vento: spinge la resistenza.')
     +item(4,CORAL,'Nelle altre andature','Alla resistenza si somma la portanza, perpendicolare al vento: così si risale.')
     +fonte('cap. 4, introduzione'))
sec('controvento',head('Che cos\'è la portanza','Risalire il vento',ORANGE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Il vento arriva dall\'alto; da una barca partono raggi colorati che indicano quanto si stringe il vento: 50 gradi i vascelli del Settecento, 35 gli yacht, 30 le barche da regata, 27 Luna Rossa; il settore davanti al vento è ombreggiato: lì non si va')+lbl,
 notes='Da Laura Romanò, «La fisica in barca a vela», capitolo 4, introduzione: è una falsa credenza che i vascelli a vele quadre non potessero risalire il vento; già nel Settecento stringevano fino a circa 50 gradi. Oggi uno yacht da diporto stringe a circa 35 gradi, le barche da regata a 30, Luna Rossa a 27. Il capitolo si apre con una citazione dal «Gabbiano Jonathan Livingston»: «I gabbiani non vacillano, non stallano mai». In fil di ruota la forza aerodinamica ha la direzione del vento; nelle altre andature alla resistenza si somma vettorialmente la portanza, perpendicolare al vento. Il termine nasce in aeronautica, ma l\'origine della forza nelle vele è la stessa.')

# ============ FORZA (disegno a sinistra) ============
X=128
s,cx,cy=150,546,330
fx,fy=T(-0.95,0.12,s,cx,cy)
b=(flow_lines('profilo',s,cx,cy)+body('profilo',s,cx,cy)+wind(40,90)
   +arrow(fx,fy,fx,fy-250,CORAL,8,26)+arrow(fx,fy,fx+70,fy,PURPLE,8,22)
   +f'<path d="M{fx:.0f} {fy:.0f} L{fx+70:.0f} {fy-250:.0f}" stroke="{NAVY}" stroke-width="5" stroke-dasharray="12 9"/>'+arrow(fx+62,fy-222,fx+70,fy-250,NAVY,5,18))
lbl=(lab(X+50,Y+122,200,'vento',INK,24,800)+lab(X+fx-240,Y+fy-250,220,'portanza',CORAL,26,900,'right')+lab(X+fx+30,Y+fy+26,220,'resistenza',PURPLE,24,900)
     +lab(X+fx+90,Y+fy-270,260,'forza totale',NAVY,24,900))
txt=(item(1,CORAL,'Una sola forza','Il vento che scorre su un\'ala o su una vela produce una forza aerodinamica.')
     +item(2,SEA,'Portanza','La parte perpendicolare al vento: tiene in aria l\'aereo, spinge avanti la barca.')
     +item(3,PURPLE,'Resistenza','La parte parallela al vento: frena, e cresce con la turbolenza.')
     +item(4,BLUE,'Ala e vela','La fisica è la stessa: la vela è un\'ala messa in verticale.'))
sec('forza',head('Che cos\'è la portanza','Portanza e resistenza',CORAL),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con le linee di corrente calcolate: il vento arriva da sinistra; sul profilo la freccia rossa della portanza verso l\'alto, quella viola della resistenza verso destra e la forza totale tratteggiata')+lbl+pcol(txt,532,18),
 notes='Portanza e resistenza sono le due componenti della forza aerodinamica: la portanza è perpendicolare alla direzione del vento che arriva, la resistenza è parallela. Le linee di corrente sono calcolate per un profilo alare in un fluido ideale: si vede che l\'aria sale prima del profilo e scende dopo.')

# ============ MANO (disegno a destra) ============
X=700
s,cx,cy=140,546,330
b=(flow_lines('lastra',s,cx,cy,w=3)+body('lastra',s,cx,cy,fill=SAND,st=NAVY,sw=14)
   +wind(40,90)+arrow(cx-20,cy-40,cx-20+60,cy-40-230,CORAL,8,26)
   +arrow(860,470,960,530,SEA,6,20))
lbl=(lab(X+50,Y+122,200,'vento',INK,24,800)+lab(X+cx+40,Y+cy-290,280,'spinta: su e indietro',CORAL,24,900)
     +lab(X+700,Y+548,330,'aria spinta verso il basso',SEA,24,900))
txt=(item(1,SEA,'Mano piatta','Nessuna spinta: l\'aria passa sopra e sotto allo stesso modo.')
     +item(2,CORAL,'Mano inclinata','La mano sale: l\'aria viene deviata verso il basso e spinge in su.')
     +item(3,PURPLE,'Troppo inclinata','La spinta verso l\'alto crolla e resta solo il freno: è lo stallo.')
     +item(4,BLUE,'La vela','Si regola allo stesso modo: l\'angolo giusto, né troppo né poco.'))
sec('mano',head('Che cos\'è la portanza','La mano fuori dal finestrino',SEA)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Una tavoletta inclinata di dieci gradi nel vento con le linee di corrente calcolate: l\'aria dietro scende e sulla tavoletta nasce una spinta verso l\'alto e un po\' indietro')+lbl,
 notes='L\'esperimento che tutti hanno fatto da bambini: la mano fuori dal finestrino dell\'auto in corsa. Il disegno è una lastra piana inclinata di 10 gradi, con il flusso calcolato: anche una superficie piatta produce portanza se è inclinata.')

# ============ NEWTON (disegno a sinistra) ============
X=128
s,cx,cy=150,546,330
b=(flow_lines('profilo',s,cx,cy)+body('profilo',s,cx,cy)+wind(40,90)
   +arrow(120,420,230,390,PURPLE,7,22)+arrow(880,440,1000,500,SEA,7,22)
   +arrow(cx-150,cy-30,cx-150,cy-230,CORAL,8,26)+arrow(cx+300,cy+80,cx+300,cy+230,NAVY,8,26))
lbl=(lab(X+60,Y+440,300,'l\'aria sale già prima',PURPLE,24,900)+lab(X+900,Y+410,180,'poi scende',SEA,24,900)
     +lab(X+cx-130,Y+cy-250,240,'reazione: portanza',CORAL,24,900)+lab(X+cx+300-240,Y+cy+200,220,'azione sull\'aria',NAVY,24,900,'right'))
txt=(item(1,NAVY,'Azione e reazione','L\'ala spinge l\'aria verso il basso; l\'aria spinge l\'ala verso l\'alto (terza legge di Newton).')
     +item(2,SEA,'Il flusso deviato','Dietro al profilo l\'aria scende: si chiama downwash.')
     +item(3,PURPLE,'Anche davanti','L\'aria sale prima di toccare il profilo: è l\'upwash. L\'ala si fa «sentire» in anticipo.')
     +item(4,CORAL,'F = m · a','La vela devia una grande massa d\'aria; ben regolata, riceve una forza perpendicolare alla corda.')
     +fonte('§4.3', 'NASA'))
sec('newton',head('Che cos\'è la portanza','Deviare l\'aria: Newton',PURPLE),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con le linee di corrente calcolate: davanti al profilo le linee salgono, dietro scendono; una freccia verso l\'alto sul profilo e una verso il basso sull\'aria')+lbl+pcol(txt,532,18),
 notes='La spiegazione «di Newton»: l\'ala cambia la direzione dell\'aria, quindi le imprime una forza verso il basso; per la terza legge l\'aria restituisce all\'ala una forza verso l\'alto. NASA Glenn Research Center, pagina «Bernoulli and Newton»: le due spiegazioni sono entrambe corrette e descrivono lo stesso fenomeno. Laura Romanò, «La fisica in barca a vela», paragrafo 4.3 «La vela come deflettore»: una forza nasce quando una massa è accelerata, F = m·a; se il vento entra con velocità V1 ed esce con V2, la forza sull\'aria dipende dalla massa d\'aria e dalla variazione di velocità. Di bolina o al traverso una grande massa d\'aria viene scaraventata lateralmente e la barca riceve una forza uguale e contraria; se la vela è simmetrica e ben regolata, la forza è perpendicolare alla corda.')

# ============ BERNOULLI (disegno a destra) ============
X=700
s,cx,cy=160,546,320
b=(flow_lines('profilo',s,cx,cy,op=0.45)+body('profilo',s,cx,cy)+pressure('profilo',s,cx,cy,sc=40)+wind(40,90))
lbl=(lab(X+cx-200,Y+100,420,'depressione (–): l\'aria corre',CORAL,26,900,'center')+lab(X+cx-200,Y+470,420,'sovrappressione (+): l\'aria rallenta',BLUE,26,900,'center')
     +lab(X+50,Y+122,200,'vento',INK,24,800))
txt=(item(1,CORAL,'Sopra: veloce','Sopra il profilo l\'aria accelera e la pressione scende: aspira.')
     +item(2,BLUE,'Sotto: più lenta','Sotto l\'aria rallenta e la pressione sale: spinge.')
     +item(3,SEA,'Bernoulli','Dove la velocità aumenta la pressione diminuisce, e viceversa.')
     +item(4,PURPLE,'Newton o Bernoulli?','Entrambi: sono due modi di descrivere la stessa forza (NASA).')
     +fonte('§4.1', 'NASA'))
sec('bernoulli',head('Che cos\'è la portanza','Le pressioni: Bernoulli',BLUE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con le frecce di pressione calcolate: sopra frecce rosse che escono dal profilo, la depressione più forte vicino al bordo d\'ingresso; sotto frecce blu che spingono verso il profilo')+lbl,
 notes='Le frecce sono il coefficiente di pressione calcolato sulla superficie del profilo. La depressione sul dorso è più grande della sovrappressione sul ventre e si concentra nella parte anteriore. NASA Glenn Research Center: «Both Bernoulli and Newton are correct». Laura Romanò, «La fisica in barca a vela», paragrafo 4.1: attorno a una randa isolata quasi tutte le linee di flusso che arrivano da sinistra passano sul lato sottovento; dove le linee sono fitte la velocità è alta e la pressione bassa. Le forze sui due lati si sommano in un\'unica forza applicata nel centro velico.')

# ============ MITO (disegno a sinistra) ============
X=128
s,cx,cy=150,546,330
def pick(k,sign):
    Ls=[L for L in FL[k]['lines'] if (L['lev']>0.05 if sign>0 else L['lev']<-0.05)]
    return min(Ls,key=lambda L:abs(L['lev']))
def at_x(L,x0):
    P=L['pts']; t=L['t']
    for i in range(len(P)-1):
        if P[i][0]<=x0<=P[i+1][0]:
            f=(x0-P[i][0])/max(1e-9,P[i+1][0]-P[i][0]); return t[i]+f*(t[i+1]-t[i])
    return None
def at_t(L,tt):
    P=L['pts']; t=L['t']
    for i in range(len(P)-1):
        if t[i]<=tt<=t[i+1]:
            f=(tt-t[i])/max(1e-9,t[i+1]-t[i]); return P[i][0]+f*(P[i+1][0]-P[i][0]),P[i][1]+f*(P[i+1][1]-P[i][1])
    return None
up,dn=pick('profilo',1),pick('profilo',-1)
t0u,t0d=at_x(up,-2.9),at_x(dn,-2.9)
dots=''; iso=''
for kk in range(0,9):
    tt=kk*0.7
    pu=at_t(up,t0u+tt); pd=at_t(dn,t0d+tt)
    if not pu or not pd: break
    U1=T(*pu,s,cx,cy); D1=T(*pd,s,cx,cy)
    iso+=f'<path d="M{U1[0]:.0f} {U1[1]:.0f} L{D1[0]:.0f} {D1[1]:.0f}" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 6"/>'
    dots+=f'<circle cx="{U1[0]:.0f}" cy="{U1[1]:.0f}" r="11" fill="{CORAL}" stroke="#FFFFFF" stroke-width="3"/><circle cx="{D1[0]:.0f}" cy="{D1[1]:.0f}" r="11" fill="{BLUE}" stroke="#FFFFFF" stroke-width="3"/>'
def one(L,c):
    pts=L['pts']; st=max(1,len(pts)//90); pp=pts[::st]
    return '<path d="M'+' L'.join(f'{T(x,y,s,cx,cy)[0]:.1f} {T(x,y,s,cx,cy)[1]:.1f}' for x,y in pp)+f'" fill="none" stroke="{c}" stroke-width="4"/>'
b=(flow_lines('profilo',s,cx,cy,op=0.35)+one(up,CORAL)+one(dn,BLUE)+body('profilo',s,cx,cy)+iso+dots+wind(40,90))
lbl=(lab(X+50,Y+122,200,'vento',INK,24,800)+lab(X+80,Y+520,940,'I pallini dello stesso istante sono uniti dal tratteggio: quello di sopra è già oltre il bordo d\'uscita.',INK,24,700))
txt=(item('✗',CORAL,'La teoria sbagliata','«Sopra il percorso è più lungo, l\'aria deve arrivare in fondo insieme a quella di sotto, quindi corre di più».')
     +item(1,SEA,'Non si rincontrano','L\'aria di sopra arriva prima: va molto più veloce di quanto dice quella teoria.')
     +item(2,PURPLE,'La prova','Profili simmetrici e volo rovescio portano; in galleria del vento il fumo sul dorso arriva molto prima.')
     +item(3,BLUE,'E la vela?','Una vela ha i due lati lunghi uguali, eppure produce portanza.')
     +fonte('§4.2', 'NASA'))
sec('mito',head('Che cos\'è la portanza','Il mito del percorso più lungo',CORAL),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con due linee di corrente evidenziate, una sopra in rosso e una sotto in blu; pallini segnano dove si trova l\'aria negli stessi istanti: il pallino di sopra arriva al bordo d\'uscita molto prima di quello di sotto')+lbl+pcol(txt,532,16),
 notes='NASA Glenn Research Center, «Incorrect Lift Theory»: la teoria del «tempo di transito uguale» o «percorso più lungo» è la spiegazione sbagliata più diffusa. «The actual velocity over the top of an airfoil is much faster than that predicted by the Longer Path theory and particles moving over the top arrive at the trailing edge before particles moving under the airfoil.» I pallini del disegno sono calcolati: posizioni dell\'aria a intervalli di tempo uguali lungo due linee di corrente. Laura Romanò, «La fisica in barca a vela», paragrafo 4.2 «Modelli non corretti»: la teoria dell\'uguale transito non ha fondamento fisico, non spiega il volo rovescio né i profili simmetrici; in galleria del vento il fumo mostra che il flusso sul dorso raggiunge il bordo d\'uscita molto prima di quello sul ventre.')

quiz_slide('quizA','Verifica · che cos\'è la portanza',['2.1.1-73','2.1.1-37','2.1.1-58'],False)
quiz_slide('quizAr','Verifica · che cos\'è la portanza',['2.1.1-73','2.1.1-37','2.1.1-58'],True)

# ============ VISCOSITÀ (disegno a destra) ============
X=700
ex0,ey0,erx,ery=300,330,92,118
def ell(t,off=0): return ex0+(erx+off)*math.cos(t), ey0+(ery+off)*math.sin(t)
xs=250; t0=math.pi+math.acos((ex0-xs)/(erx+9))  # punto d'impatto sul lato sinistro-alto
t0=2*math.pi-math.acos((xs-ex0)/(erx+9))
tt_=[t0-k*(t0-math.radians(80))/40 for k in range(41)]
stream=f'M{xs} 120 L{xs} {ell(t0,9)[1]:.0f} '+' '.join(f'L{ell(t,9)[0]:.0f} {ell(t,9)[1]:.0f}' for t in tt_)
exx,eyy=ell(math.radians(80),9)
stream+=f' L{exx+70:.0f} {eyy+40:.0f}'
tap=(f'<rect x="120" y="40" width="160" height="34" rx="10" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/>'
     f'<rect x="{xs-22}" y="66" width="44" height="54" rx="6" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/><rect x="170" y="20" width="44" height="24" rx="6" fill="{NAVY}"/>')
egg=f'<ellipse cx="{ex0}" cy="{ey0}" rx="{erx}" ry="{ery}" fill="#FFF3DC" stroke="{NAVY}" stroke-width="5"/>'
left=(tap+f'<path d="{stream}" fill="none" stroke="#5AA9E6" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.85"/>'
      +egg+arrow(ex0+50,ey0-10,ex0-40,ey0-10,CORAL,7,22))
s,cx,cy=78,820,300
clip='<defs><clipPath id="vsR"><rect x="590" y="30" width="490" height="560"/></clipPath></defs>'
right=(clip+'<g clip-path="url(#vsR)">'+flow_lines('vela',s,cx,cy,w=2.5)+'</g>'+body('vela',s,cx,cy,fill='none',st=NAVY,sw=8)
       +arrow(cx,cy-40,cx,cy-190,CORAL,8,24)+arrow(cx+175,cy+40,cx+245,cy+110,SEA,7,22)+wind(610,500,90))
b=left+f'<path d="M560 20 L560 600" stroke="{PANEL_W}" stroke-width="5"/>'+right
lbl=(lab(X+30,Y+530,520,'effetto Coandă: il getto segue l\'uovo',SEA,24,900)+lab(X+30,Y+570,520,'e l\'uovo è attirato verso il getto',CORAL,24,900)
     +lab(X+cx+20,Y+cy-200,250,'reazione sulla vela',CORAL,24,900)+lab(X+cx+50,Y+cy+128,210,'azione: aria deviata',SEA,24,900)
     +lab(X+610,Y+520,200,'vento',INK,24,800))
txt=(item(1,SEA,'L\'aria segue la vela','Sul lato sottovento l\'aria resta attaccata alla vela grazie alla viscosità.')
     +item(2,CORAL,'Fluido ideale: niente','Un corpo in un fluido senza viscosità non produce portanza.')
     +item(3,PURPLE,'L\'uovo sotto il rubinetto','Il getto si incurva e segue l\'uovo, se la curva non è troppo accentuata: è l\'effetto Coandă.')
     +item(4,BLUE,'Azione e reazione','La vela devia l\'aria (azione); l\'aria spinge la vela con una forza uguale e contraria.')
     +fonte('§4.3 «Viscosità»'))
sec('viscosita',head('Come nasce la portanza','Senza viscosità niente portanza',ORANGE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'A sinistra un rubinetto con un getto d\'acqua che tocca un uovo e ne segue la superficie curvandosi; una freccia mostra l\'uovo attirato verso il getto. A destra una vela vista dall\'alto con le linee del vento calcolate che la seguono e vengono deviate: la freccia dell\'aria deviata e quella della reazione sulla vela')+lbl,
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.3, «Generazione di portanza: viscosità». L\'aria segue la superficie della vela sul lato sottovento grazie alla viscosità: il primo strato di fluido resta fermo sulla superficie e le forze di attrazione tra le molecole fanno ruotare gli strati successivi. Un oggetto che si muove in un fluido ideale, senza viscosità, non produce portanza. L\'effetto Coandă: un fluido tende a seguire il contorno dell\'oggetto su cui incide, se la curvatura non è troppo accentuata; l\'esperimento dell\'uovo sotto il getto del rubinetto lo mostra. La forza che devia il fluido è l\'azione, la reazione è la forza uguale e contraria sulla vela. Esperimento da fare in aula: un cucchiaio tenuto per il manico sotto il getto viene attirato verso l\'acqua.')

# ============ VORTICE DI PARTENZA (disegno a sinistra) ============
X=128
def spiral(xc,yc,r0,turns,sign,c,w=4):
    pts=[]; n=60*turns
    for k in range(n+1):
        t=k/60*2*math.pi; r=r0*(1-0.8*k/n)
        pts.append((xc+r*math.cos(sign*t), yc+r*math.sin(sign*t)))
    d='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
    x1,y1=pts[1]; x0,y0=pts[0]
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'+head_at(x0,y0,math.degrees(math.atan2(y0-y1,x0-x1)),c,20)
s1,cx1=88,360
top=('<defs><clipPath id="vtA"><rect x="0" y="0" width="720" height="296"/></clipPath><clipPath id="vtB"><rect x="0" y="304" width="720" height="316"/></clipPath></defs>'
     +'<g clip-path="url(#vtA)">'+flow_lines('lastra_ideale',s1,cx1,150,w=2.5,n=45)+'</g>'+body('lastra_ideale',s1,cx1,150,fill=SAND,st=NAVY,sw=9))
tx_,ty_=T(*trail('lastra'),s1,cx1,462)
bot=('<g clip-path="url(#vtB)">'+flow_lines('lastra',s1,cx1,462,w=2.5,n=45)+'</g>'+body('lastra',s1,cx1,462,fill=SAND,st=NAVY,sw=9)
     +f'<ellipse cx="{cx1}" cy="462" rx="235" ry="92" fill="none" stroke="{CORAL}" stroke-width="5" stroke-dasharray="16 10"/>'
     +head_at(cx1+10,370,0,CORAL,24)+head_at(cx1-10,554,180,CORAL,24)
     +f'<path d="M{tx_:.0f} {ty_:.0f} C{tx_+120:.0f} {ty_+10:.0f} 780 480 850 470" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8"/>'
     +spiral(880,470,48,3,-1,PURPLE,5))
b=(top+bot+f'<path d="M0 300 L{W} 300" stroke="{PANEL_W}" stroke-width="4"/>'+wind(20,40,90)+wind(20,340,90))
lbl=(lab(X+740,Y+70,330,'fluido ideale: linee simmetriche, nessuna portanza',NAVY,24,900)
     +lab(X+740,Y+170,330,'l\'aria gira attorno al bordo d\'uscita',INK,24,700)
     +lab(X+610,Y+330,300,'circolazione attorno alla lastra',CORAL,24,900)
     +lab(X+760,Y+530,320,'vortice di partenza, nella scia',PURPLE,24,900,'center'))
txt=(item(1,NAVY,'Il paradosso','In un fluido ideale le linee sono simmetriche: nessuna portanza.')
     +item(2,PURPLE,'Il vortice di partenza','Con la viscosità, al bordo d\'uscita il flusso si stacca e nasce un vortice che resta nella scia.')
     +item(3,CORAL,'Helmholtz','Al vortice corrisponde una circolazione opposta attorno al profilo.')
     +item(4,SEA,'Si somma al vento','Sottovento l\'aria va più veloce (depressione), sopravvento più lenta (pressione).')
     +fonte('§4.3 «Lastra piana»'))
sec('vortice',head('Come nasce la portanza','Il vortice di partenza',PURPLE),pinned=svgp(X,Y,W,Hh,b,'Sopra: lastra inclinata in un fluido ideale, linee di corrente calcolate simmetriche che girano attorno al bordo d\'uscita: nessuna portanza. Sotto: la stessa lastra nel fluido reale, linee calcolate che lasciano pulito il bordo d\'uscita, una circolazione rossa in senso orario attorno alla lastra e un vortice viola antiorario lasciato nella scia')+lbl+pcol(txt,532,18),
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.3, analogia tra vela e lastra piana. Una vela o una lastra con un angolo di incidenza deviano le linee di flusso come la sfera che ruota. In un fluido ideale le linee sarebbero simmetriche e non ci sarebbe portanza: nel disegno in alto, calcolato senza circolazione, l\'aria gira attorno al bordo d\'uscita. Nel fluido reale, per la viscosità, al bordo d\'uscita il flusso si separa e si forma un primo vortice, il vortice di partenza, che resta nella scia. Per il teorema di Helmholtz sulla vorticità, a quel vortice corrisponde una circolazione in senso opposto attorno al profilo. La circolazione si somma al flusso: aumenta la velocità sottovento (depressione) e la riduce sopravvento (pressione). Il disegno in basso è calcolato con la condizione di Kutta: il flusso lascia pulito il bordo d\'uscita.')

# ============ MAGNUS (disegno a destra) ============
X=700
s,cx,cy=72,290,300
clip='<defs><clipPath id="mgL"><rect x="20" y="20" width="540" height="580"/></clipPath></defs>'
R_=72
left=(clip+'<g clip-path="url(#mgL)">'+flow_lines('cilindro',s,cx,cy,w=2.5)+'</g>'
      +f'<circle cx="{cx}" cy="{cy}" r="{R_}" fill="#FFF3DC" stroke="{NAVY}" stroke-width="5"/>'
      +f'<path d="M{cx-40} {cy-18} A44 44 0 1 1 {cx-10} {cy+42}" fill="none" stroke="{NAVY}" stroke-width="5"/>'+head_at(cx-12,cy+42,160,NAVY,18)
      +arrow(cx,cy-R_-10,cx,cy-R_-150,CORAL,8,24)+wind(30,560,90))
ship=(f'<path d="M0 400 '+' '.join('q27 -10 54 0 t54 0' for _ in range(5))+f'" fill="none" stroke="{SEA}" stroke-width="5" stroke-linecap="round" transform="translate(600 150)"/>'
      f'<path d="M610 470 L1070 470 L1035 535 L650 535 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/>'
      f'<rect x="960" y="430" width="70" height="40" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>')
for rx_,top_ in [(720,230),(860,210)]:
    ship+=(f'<rect x="{rx_}" y="{top_}" width="56" height="{470-top_}" rx="8" fill="{SAND}" stroke="{NAVY}" stroke-width="5"/>'
           f'<ellipse cx="{rx_+28}" cy="{top_}" rx="44" ry="11" fill="{NAVY}"/>'
           f'<path d="M{rx_-14} {top_+70} Q{rx_+28} {top_+100} {rx_+70} {top_+70}" fill="none" stroke="{CORAL}" stroke-width="4"/>'+head_at(rx_+70,top_+70,-35,CORAL,16))
b=left+f'<path d="M580 20 L580 600" stroke="{PANEL_W}" stroke-width="5"/>'+ship
lbl=(lab(X+cx-260,Y+cy-R_-110,240,'portanza',CORAL,26,900,'right')
     +lab(X+30,Y+24,540,'sopra si sommano: veloce, bassa pressione',CORAL,24,900)
     +lab(X+30,Y+470,520,'sotto si sottraggono: lento, alta pressione',BLUE,24,900)
     +lab(X+640,Y+60,420,'la nave a rotori di Flettner',NAVY,26,900,'center')+lab(X+640,Y+550,420,'Buckau, anni \'20',INK,24,700,'center'))
txt=(item(1,CORAL,'Il tiro a effetto','Una palla lanciata con rotazione devia dalla traiettoria: c\'è portanza.')
     +item(2,SEA,'La rotazione trascina l\'aria','Sopra i flussi si sommano, sotto si sottraggono; i punti di ristagno si abbassano.')
     +item(3,PURPLE,'Rotori al posto delle vele','Anton Flettner montò due cilindri rotanti: la nave attraversò l\'Atlantico controvento.')
     +item(4,BLUE,'Il legame con la vela','Vela e lastra inclinata deviano l\'aria allo stesso modo: circolazione e portanza.')
     +fonte('§4.3 «L\'effetto Magnus»'))
sec('magnus',head('Come nasce la portanza','L\'effetto Magnus',BLUE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'A sinistra un cilindro che ruota in senso orario nel vento, con le linee di corrente calcolate: sopra sono fitte, sotto rade, e la freccia della portanza punta in alto. A destra una nave con due alti cilindri rotanti al posto delle vele, la nave a rotori di Flettner')+lbl,
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.3, «L\'effetto Magnus». Una palla lanciata con una rotazione devia dalla traiettoria rettilinea: è il tiro a effetto del calcio. La rotazione trascina per viscosità uno strato d\'aria; combinando traslazione e rotazione oraria, sopra i flussi si sommano (velocità alta, pressione bassa) e sotto si sottraggono (velocità bassa, pressione alta); i punti di ristagno si spostano verso il basso. Il disegno a sinistra è calcolato: cilindro con circolazione in un flusso uniforme. Anton Flettner sostituì le vele della nave Buckau con due rotori, cilindri verticali rotanti: la nave attraversò l\'Atlantico anche controvento, ma non risultò economicamente conveniente. Il libro indica il 1922; le fonti storiche datano la trasformazione della Buckau al 1924 e la traversata atlantica al 1926: per questo sulla slide c\'è «anni \'20».')

# ============ ENERGIA (disegno a sinistra) ============
X=128
k=30; Px,Py=640,330
AW=(-6,10); ca,sa=math.cos(math.radians(35)),math.sin(math.radians(35))
AW2=(AW[0]*ca-AW[1]*sa, AW[0]*sa+AW[1]*ca)      # ruotato di 35° verso poppa (schermo, y in basso)
TWo=(AW2[0]+6, AW2[1]); vout=math.hypot(*TWo)
Qx,Qy=Px-AW[0]*k,Py-AW[1]*k
E2=(Px+AW2[0]*k,Py+AW2[1]*k); T2=(Px+TWo[0]*k,Py+TWo[1]*k)
hull=(f'<path d="M{Px-230} {Py} Q{Px-210} {Py-60} {Px-30} {Py-66} Q{Px+150} {Py-60} {Px+250} {Py} Q{Px+150} {Py+60} {Px-30} {Py+66} Q{Px-210} {Py+60} {Px-230} {Py} Z" fill="#FFFFFF" fill-opacity="0.6" stroke="{NAVY}" stroke-opacity="0.35" stroke-width="4"/>')
sail=f'<path d="M{Px+40} {Py-6} Q{Px-10} {Py+30} {Px-80} {Py+44}" fill="none" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/><circle cx="{Px+40}" cy="{Py-6}" r="10" fill="{NAVY}"/>'
b=(hull+sail+arrow(Px+250,Py,Px+330,Py,NAVY,5,18)
   +arrow(Qx,Qy,Qx,Py,GREY,6,20)+arrow(Qx,Py,Px+6,Py,GREY,6,20)+arrow(Qx,Qy,Px+6,Py-10,SEA,8,24)
   +arrow(Px,Py,E2[0],E2[1],PURPLE,8,24)+arrow(Px,Py,T2[0],T2[1],CORAL,8,24)
   +f'<path d="M{T2[0]:.0f} {T2[1]:.0f} L{E2[0]:.0f} {E2[1]:.0f}" stroke="{GREY}" stroke-width="4" stroke-dasharray="8 8"/>')
# barre dell'energia
bx0,bw=750,300
b+=(f'<rect x="{bx0-20}" y="400" width="{bw+40}" height="210" rx="24" fill="#FFFFFF" fill-opacity="0.75"/>'
    f'<rect x="{bx0}" y="448" width="{bw}" height="32" rx="8" fill="{SEA}"/>'
    f'<rect x="{bx0}" y="528" width="{bw*0.49:.0f}" height="32" rx="8" fill="{CORAL}"/>'
    f'<rect x="{bx0+bw*0.49:.0f}" y="528" width="{bw*0.51:.0f}" height="32" rx="8" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>')
lbl=(lab(X+Qx+16,Y+Qy+110,230,'vento reale 10 nodi',INK,24,900)+lab(X+Px+60,Y+Py+8,120,'6 nodi',GREY,22,900)
     +lab(X+380,Y+150,310,'apparente ~12 nodi a 59°',SEA,24,900,'right')
     +lab(X+40,Y+492,340,'deviato di 35° dalla vela',PURPLE,24,900)
     +lab(X+400,Y+540,300,'reale in uscita ~7 nodi',CORAL,24,900)
     +lab(X+bx0,Y+410,bw,'energia del vento (∝ V²)',INK,22,900)+lab(X+bx0,Y+484,bw,'prima: 10 nodi = 100%',SEA,22,900)
     +lab(X+bx0,Y+564,bw,'dopo: 7 nodi ≈ 49%',CORAL,22,900)+lab(X+bx0+bw*0.49,Y+530,bw*0.51,'51% alla barca',CORAL,20,900,'center'))
txt=(item(1,SEA,'Energia e velocità','L\'energia del vento cresce con il quadrato della velocità.')
     +item(2,NAVY,'Al traverso','Barca a 6 nodi, vento reale di 10: apparente di circa 12 nodi a 59°.')
     +item(3,PURPLE,'La vela devia il vento','Rispetto all\'apparente la barca è come ferma: il flusso cambia solo direzione, qui di 35°.')
     +item(4,CORAL,'Il vento rallenta','Dietro la balumina il vento reale scende a circa 7 nodi: ha ceduto circa metà dell\'energia.')
     +fonte('§4.3 «Vento reale, apparente ed energia»'))
sec('energia',head('Come nasce la portanza','Il vento cede energia',CORAL),pinned=svgp(X,Y,W,Hh,b,'Barca vista dall\'alto al traverso verso destra. In alto a destra il triangolo dei venti: vento reale di 10 nodi dall\'alto, vento di velocità di 6 nodi, apparente di 12 nodi. Dalla vela esce l\'apparente deviato di 35 gradi e, tolto il moto della barca, il vento reale in uscita di circa 7 nodi. A destra due barre: l\'energia del vento reale passa dal 100 al 49 per cento')+lbl+pcol(txt,532,18),
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.3, «Vento reale, apparente ed energia». L\'energia di una massa d\'aria in moto è proporzionale al quadrato della velocità; se il vento cede energia alla barca, la sua velocità reale deve diminuire. Esempio del libro: traverso a 6 nodi con 10 nodi di vento reale; il vento apparente è di circa 12 nodi (11,7) a 59 gradi dalla prua. Rispetto al vento apparente la barca è come ferma su una banchina: il flusso cambia solo direzione. Se la vela lo devia di 35 gradi, all\'uscita dalla balumina il vento reale scende a circa 7 nodi (il calcolo con i vettori del disegno dà %.1f nodi): l\'energia passa da 10² a 7², cioè al 49 per cento, e il vento reale ha ceduto circa il 51 per cento della sua energia al moto della barca. Il disegno è costruito con questi vettori, in scala.' % vout)

# ============ INCIDENZA (disegno a destra) ============
X=700
ox,oy,gw,gh=150,470,760,330
def cl(a): return 0.105*a if a<=14 else (1.47-0.09*(a-14)*1.0 if a<=19 else 1.02+0.005*(a-19))
pts=[(ox+gw*a/24, oy-gh*cl(a)/1.6) for a in [i*0.25 for i in range(0,97)]]
curve='M'+' L'.join(f'{x:.0f} {y:.0f}' for x,y in pts)
def mini(xc,yc,ang,sc=34):
    ss=FL['profilo0']['surface']; ca,sa=math.cos(math.radians(ang)),math.sin(math.radians(ang))
    d='M'+' L'.join(f'{xc+sc*(p[0]*ca+p[1]*sa):.0f} {yc-sc*(-p[0]*sa+p[1]*ca):.0f}' for p in ss)+' Z'
    return f'<path d="{d}" fill="{NAVY}"/>'
sx=ox+gw*14/24; sy=oy-gh*cl(14)/1.6
b=(f'<path d="M{ox} {oy-gh-20} L{ox} {oy} L{ox+gw+30} {oy}" fill="none" stroke="{NAVY}" stroke-width="5"/>'
   +arrow(ox+gw,oy,ox+gw+40,oy,NAVY,5,16)+arrow(ox,oy-gh,ox,oy-gh-40,NAVY,5,16)
   +f'<rect x="{sx-40}" y="{oy-gh-10}" width="{ox+gw-sx+40}" height="{gh+10}" fill="{CORAL}" fill-opacity="0.10"/>'
   +f'<path d="{curve}" fill="none" stroke="{SEA}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
   +f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="14" fill="{CORAL}"/>'
   +mini(ox+gw*3/24,oy+80,3)+mini(ox+gw*10/24,oy+80,10)+mini(ox+gw*20/24,oy+80,20)
   +wind(ox+gw*3/24-150,oy+80,70,GREY,6))
lbl=(lab(X+ox+10,Y+oy-gh-60,300,'portanza',NAVY,24,900)+lab(X+ox+gw-360,Y+oy+14,380,'angolo di incidenza',NAVY,24,900,'right')
     +lab(X+sx+20,Y+oy-gh-50,340,'stallo: la portanza crolla',CORAL,24,900)+lab(X+ox+gw*7/24+10,Y+oy-120,260,'cresce con l\'angolo',SEA,24,900))
txt=(item(1,SEA,'L\'angolo di incidenza','Tra il vento apparente e la vela (o la corda del profilo).')
     +item(2,CORAL,'Più angolo, più portanza','Ad angoli piccoli cresce in modo lineare: angolo doppio, portanza doppia. Oltre un limite la vela stalla.')
     +item(3,PURPLE,'Troppo poco','Con angolo quasi nullo la vela non porta e fileggia.')
     +item(4,BLUE,'Per il quiz','La pressione del vento sulle vele dipende dall\'angolo di incidenza: vero.')
     +fonte('§4.3'))
sec('incidenza',head('Da cosa dipende','L\'angolo di incidenza',SEA)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Grafico qualitativo: la portanza cresce con l\'angolo di incidenza fino a un massimo, poi crolla nella zona dello stallo; sotto, tre profili a incidenza piccola, media e troppo grande')+lbl,
 notes='Grafico qualitativo, senza numeri: l\'angolo di stallo dipende dal profilo e, per una vela, dalla sua forma e dalla regolazione. Quiz 2.1.1-28 e 2.1.1-96 (definizione dell\'angolo di incidenza), 2.1.1-37 e -38 (la pressione del vento dipende dall\'angolo di incidenza). Laura Romanò, «La fisica in barca a vela», paragrafo 4.3: ad angoli piccoli la portanza cresce linearmente, raddoppiando l\'angolo raddoppia la portanza; superato l\'angolo critico il fluido si separa dalla superficie sottovento, la portanza cala drasticamente e la vela da deflettore diventa un ostacolo.')

# ============ STALLO (disegno a sinistra) ============
X=128
s1,cx1,cy1=105,420,150
top=('<defs><clipPath id="stA"><rect x="0" y="0" width="%d" height="296"/></clipPath></defs>' % W)+'<g clip-path="url(#stA)">'+flow_lines('profilo',s1,cx1,cy1,w=2.5)+body('profilo',s1,cx1,cy1)+'</g>'
def rot_body(xc,yc,sc,ang):
    ss=FL['profilo0']['surface']; ca,sa=math.cos(math.radians(ang)),math.sin(math.radians(ang))
    return 'M'+' L'.join(f'{xc+sc*(p[0]*ca+p[1]*sa):.0f} {yc-sc*(-p[0]*sa+p[1]*ca):.0f}' for p in ss)+' Z'
bot=''
for dd in ['M20 330 C300 328 700 340 1080 350','M20 362 C140 362 190 372 225 372 S 520 385 1080 400',
           'M20 470 C150 470 250 520 420 545 S 800 560 1080 565','M20 520 C200 522 400 570 700 580 S 950 585 1080 588','M20 575 C300 580 700 598 1080 600']:
    bot+=f'<path d="{dd}" fill="none" stroke="{FLOW}" stroke-width="2.5"/>'
for (vx,vy,r) in [(330,400,17),(420,418,22),(510,440,24),(600,462,24),(690,470,22)]:
    bot+=f'<path d="M{vx+r} {vy} A{r} {r} 0 1 0 {vx} {vy+r} A{r*0.6:.0f} {r*0.6:.0f} 0 1 0 {vx+r*0.3:.0f} {vy-r*0.2:.0f}" fill="none" stroke="{CORAL}" stroke-width="3.5"/>'
bot+=f'<path d="{rot_body(420,455,105,18)}" fill="{NAVY}"/>'
b=(f'<rect x="0" y="0" width="{W}" height="300" fill="#FFFFFF" fill-opacity="0.35"/>'+top+bot
   +f'<path d="M0 300 L{W} 300" stroke="{PANEL_W}" stroke-width="4"/>'+wind(20,40,90)+wind(20,340,90))
lbl=(lab(X+820,Y+110,250,'flusso attaccato: la vela porta',SEA,26,900)+lab(X+820,Y+400,250,'stallo: il flusso si stacca e fa vortici',CORAL,26,900)
     +lab(X+820,Y+510,250,'meno portanza, più resistenza',INK,24,700))
txt=(item(1,SEA,'Il flusso attaccato','L\'aria segue la curva del dorso fino al bordo d\'uscita.')
     +item(2,CORAL,'Il distacco','Verso il bordo d\'uscita la pressione risale; se risale troppo, l\'aria si stacca.')
     +item(3,PURPLE,'Da deflettore a ostacolo','Vortici sul dorso: la portanza crolla, la resistenza cresce.')
     +item(4,BLUE,'A bordo','Filetti sottovento che girano: lasca la vela o orza un poco.')
     +fonte('§4.3', 'A. Gentry'))
sec('stallo',head('Da cosa dipende','Lo stallo',CORAL),pinned=svgp(X,Y,W,Hh,b,'Sopra: profilo con il flusso attaccato che segue il dorso. Sotto: lo stesso profilo troppo inclinato, con il flusso che si stacca dal dorso e forma vortici rossi')+lbl+pcol(txt,532,18),
 notes='Il disegno in alto è calcolato; quello in basso è schematico, perché il distacco del flusso non si calcola con il fluido ideale. Arvel Gentry, «A Review of Modern Sail Theory»: il distacco è un effetto viscoso; quando la pressione aumenta troppo lungo la superficie (gradiente di pressione avverso) lo strato limite si stacca e il flusso diventa caotico e instabile.')

# ============ FATTORI ============
F=(f'<div style="display:flex; align-items:center; gap:30px; background:{NAVY}; border-radius:32px; padding:30px 40px">'
   f'<p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1.1; color:#FFFFFF; white-space:nowrap">Portanza = ½ · ρ · V² · S · C<span style="color:{DACC}">L</span></p>'
   f'<p style="font-size:28px; line-height:1.35; font-weight:700; color:{DSOFT}">La formula di ogni ala: non serve a fare conti, dice che cosa conta.</p></div>')
tl=tiles([('ρ · densità','L\'aria fredda e densa porta un po\' di più di quella calda. L\'acqua è circa 800 volte più densa.',SEA),
          ('V² · velocità','Il vento apparente conta al quadrato: vento doppio, forza quattro volte.',CORAL),
          ('S · superficie','Più tela, più forza: per questo con vento forte si prendono i terzaroli.',PURPLE),
          ('CL · forma e angolo','Il coefficiente di portanza: cresce con la concavità e l\'incidenza, fino allo stallo.',BLUE)],26)
sec('fattori',head('Da cosa dipende','Da cosa dipende la portanza',PURPLE)+F+tl
    +note('Vento da 10 a 20 nodi: sulle vele la forza non raddoppia, quadruplica.',CORAL,40),
 notes='Formula della portanza: L = ½ ρ V² S CL. La densità dell\'acqua di mare (circa 1025 kg/m³) è circa 800 volte quella dell\'aria (circa 1,2 kg/m³): per questo la deriva, pur piccola, riesce a opporsi alla forza delle vele. La stessa formula, con il coefficiente di resistenza, vale per la resistenza.',gap=30)

# ============ ALA (disegno a destra) ============
X=700
s,cx,cy=160,560,330
lx,ly=T(*lead('vela'),s,cx,cy); tx,ty=T(*trail('vela'),s,cx,cy)
b=(flow_lines('vela',s,cx,cy)+pressure('vela',s,cx,cy,sc=34)
   +body('vela',s,cx,cy,fill='none',st=NAVY,sw=9)
   +f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="14" fill="{NAVY}"/>'+wind(40,560,120))
lbl=(lab(X+50,Y+510,300,'vento apparente',INK,24,800)+lab(X+cx-240,Y+60,480,'sottovento: depressione (–)',CORAL,26,900,'center')
     +lab(X+cx-240,Y+420,480,'sopravvento: pressione (+)',BLUE,26,900,'center')+lab(X+lx-140,Y+ly+24,140,'albero',NAVY,24,900,'right')
     +lab(X+tx-60,Y+ty+22,160,'balumina',NAVY,24,900))
txt=(item(1,SEA,'Un\'ala verticale','La vela curva devia il vento apparente proprio come un\'ala.')
     +item(2,CORAL,'Sottovento','Il lato sottovento è in depressione: la vela viene aspirata.')
     +item(3,BLUE,'Sopravvento','Il lato sopravvento riceve la pressione del vento.')
     +item(4,PURPLE,'Davanti e sottovento','Linee più fitte all\'inferitura: lì la differenza di pressione è massima. Il lato sottovento lavora più di quello sopravvento.')
     +fonte('§4.1 e §4.3'))
sec('ala',head('La vela è un\'ala','La vela è un\'ala',PURPLE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Vela vista dall\'alto come un arco sottile dietro all\'albero, con le linee di corrente calcolate e le frecce di pressione: rosse di depressione sul lato sottovento, blu di pressione sul lato sopravvento')+lbl,
 notes='Il disegno è una vela sottile a forma di arco, con il flusso calcolato: si vedono le pressioni sui due lati. Quiz 2.1.1-58: «Si intende per lato sottovento la superficie sopravvento della vela che è sottoposta a una depressione» è FALSO: la depressione è sul lato sottovento. Laura Romanò, «La fisica in barca a vela», paragrafo 4.3: le linee di flusso sono più dense, cioè la velocità è maggiore, all\'inferitura che alla balumina; la differenza di pressione è massima vicino all\'inferitura; nelle andature strette la vela lavora di più sul lato sottovento (depressione) che su quello sopravvento (pressione).')

# ============ SCOMPOSIZIONE (disegno a sinistra) ============
X=128
bx,by=520,300
hull=(f'<path d="M{bx-260} {by} Q{bx-240} {by-70} {bx-40} {by-78} Q{bx+160} {by-70} {bx+280} {by} Q{bx+160} {by+70} {bx-40} {by+78} Q{bx-240} {by+70} {bx-260} {by} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/>')
mast=(bx+40,by)
sail=f'<path d="M{mast[0]} {mast[1]} Q{mast[0]-90} {mast[1]+40} {mast[0]-200} {mast[1]+46}" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/><circle cx="{mast[0]}" cy="{mast[1]}" r="12" fill="{NAVY}"/>'
a=math.radians(35); fxv,fyv=-math.cos(a),math.sin(a)      # direzione del vento apparente (verso cui va)
Lv=(math.sin(a),math.cos(a)); Dv=(fxv*0.25,fyv*0.25)
Rv=(Lv[0]+Dv[0],Lv[1]+Dv[1]); k=250
ox_,oy_=mast[0]-90,mast[1]+30
b=(hull+sail
   +arrow(ox_,oy_,ox_+k*Rv[0],oy_+k*Rv[1],NAVY,8,26)
   +arrow(ox_,oy_,ox_+k*Rv[0],oy_,GREEN,8,24)
   +arrow(ox_+k*Rv[0],oy_,ox_+k*Rv[0],oy_+k*Rv[1],CORAL,6,20)
   +f'<path d="M{ox_} {oy_} L{ox_} {oy_+k*Rv[1]:.0f} L{ox_+k*Rv[0]:.0f} {oy_+k*Rv[1]:.0f}" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8"/>'
   +arrow(930,60,930+120*fxv,60+120*fyv,GREY,9,26)+arrow(bx+300,by,bx+420,by,NAVY,5,18))
lbl=(lab(X+820,Y+140,240,'vento apparente',INK,24,800)+lab(X+bx+300,Y+by-50,200,'prua',NAVY,24,900)
     +lab(X+ox_+k*Rv[0]+20,Y+oy_-40,300,'propulsione',GREEN,26,900)+lab(X+ox_+k*Rv[0]+20,Y+oy_+130,300,'scarroccio',CORAL,26,900)
     +lab(X+ox_-270,Y+oy_+170,240,'forza totale',NAVY,26,900,'right'))
txt=(item(1,NAVY,'La forza totale','Nasce dal vento sulla vela: un po\' in avanti, molto di lato.')
     +item(2,GREEN,'Propulsione','Parallela all\'asse della barca: la fa avanzare.')
     +item(3,CORAL,'Scarroccio','Perpendicolare all\'asse: sbanda la barca e la spinge di lato.')
     +item(4,PURPLE,'Di bolina','La parte laterale è grande: servono bulbo e deriva per contrastarla.'))
sec('scomposizione',head('La vela è un\'ala','Propulsione e scarroccio',PURPLE),pinned=svgp(X,Y,W,Hh,b,'Barca vista dall\'alto che naviga di bolina verso destra, vento apparente dall\'alto a destra; dalla vela parte la forza totale, scomposta in una freccia verde di propulsione in avanti e una rossa di scarroccio verso sottovento')+lbl+pcol(txt,532,18),
 notes='Quiz 2.1.1-84 (propulsione e scarroccio hanno origine dalla forza risultante sulle vele: vero), 2.1.1-83 (la propulsione è parallela all\'asse longitudinale: vero), 2.1.1-39 (la forza di scarroccio è perpendicolare all\'asse: vero), 2.1.1-40 (propulsione perpendicolare: falso). Nel disegno la forza totale è portanza più resistenza, con vento apparente a 35 gradi dalla prua.')

# ============ DERIVA (disegno a destra) ============
X=700
s,cx,cy=150,546,330
kx,ky=T(-0.9,0.05,s,cx,cy)
b=(flow_lines('chiglia',s,cx,cy,c='#5AA9E6')+body('chiglia',s,cx,cy,fill='#3D4B5C')
   +arrow(kx,ky,kx,ky-210,GREEN,8,26)+arrow(kx+40,ky+40,kx+40,ky+200,CORAL,6,20)+arrow(40,90,150,90,'#5AA9E6',9,28))
lbl=(lab(X+50,Y+40,340,'acqua (con lo scarroccio)',INK,24,800)+lab(X+kx+20,Y+ky-230,380,'portanza della deriva',GREEN,26,900)
     +lab(X+kx+60,Y+ky+170,360,'spinta laterale delle vele',CORAL,24,900)+lab(X+700,Y+60,320,'sopravvento',NAVY,24,900)+lab(X+700,Y+540,320,'sottovento',NAVY,24,900))
txt=(item(1,SEA,'Un\'ala in acqua','Bulbo, deriva e timone sono profili simmetrici immersi.')
     +item(2,PURPLE,'Lo scarroccio serve','La barca scivola un poco di lato: l\'acqua arriva sulla deriva con un piccolo angolo.')
     +item(3,GREEN,'Nasce la portanza','Idrodinamica, verso sopravvento: si oppone alla spinta laterale delle vele.')
     +item(4,BLUE,'Poca superficie','L\'acqua è circa 800 volte più densa dell\'aria: basta una deriva piccola.'))
sec('deriva',head('La vela è un\'ala','Anche la deriva è un\'ala',SEA)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Sezione orizzontale della deriva, un profilo simmetrico, con le linee dell\'acqua calcolate che arrivano con un piccolo angolo di scarroccio; freccia verde della portanza verso sopravvento e freccia rossa della spinta laterale delle vele verso sottovento')+lbl,
 notes='Sezione orizzontale di una deriva: profilo simmetrico con 5 gradi di incidenza dovuti allo scarroccio, flusso calcolato. Il centro di deriva è il punto di applicazione della resistenza laterale (quiz 2.1.1-62: vero).')

# ============ RESISTENZA INDOTTA (disegno a sinistra) ============
X=128
mx=640
sailp=f'<path d="M{mx} 70 L{mx} 440 L330 446 Q470 250 {mx} 70 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
rig=(f'<path d="M{mx} 50 L{mx} 478" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/><path d="M{mx} 444 L318 450" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>'
     f'<path d="M250 486 L800 486 L760 540 L300 540 Z" fill="{SAND}" stroke="{NAVY}" stroke-width="5"/>'
     f'<path d="M180 560 '+' '.join('q25 -10 50 0 t50 0' for _ in range(7))+f'" fill="none" stroke="{SEA}" stroke-width="5" stroke-linecap="round"/>')
def coil(x0,y0,x1,n,r,c):
    out=f'<path d="M{x0} {y0} L{x1} {y0}" stroke="{c}" stroke-width="2.5" stroke-dasharray="6 6"/>'
    for i in range(n):
        x=x0-(x0-x1)*i/(n-1); rr=r*(1-0.35*i/(n-1))
        out+=f'<ellipse cx="{x:.0f}" cy="{y0}" rx="{rr*0.45:.0f}" ry="{rr:.0f}" fill="none" stroke="{c}" stroke-width="4" stroke-opacity="{1-0.6*i/(n-1):.2f}"/>'
    return out
b=(rig+sailp+coil(mx-30,64,120,9,34,CORAL)+coil(300,448,90,5,26,CORAL)
   +f'<path d="M{mx+40} 110 C{mx+60} 40 {mx-10} 20 {mx-40} 44" fill="none" stroke="{BLUE}" stroke-width="5"/>'+head_at(mx-40,44,200,BLUE,18)
   +arrow(820,300,960,300,NAVY,6,22))
# riquadro: la portanza è perpendicolare al profilo, non al flusso
ix,iy=790,40
b+=(f'<rect x="{ix}" y="{iy}" width="280" height="210" rx="22" fill="#FFFFFF" fill-opacity="0.8"/>'
    +arrow(ix+20,iy+180,ix+110,iy+180,GREY,5,16)
    +arrow(ix+150,iy+180,ix+150,iy+40,GREEN,6,18)+arrow(ix+150,iy+180,ix+200,iy+180,CORAL,6,18)
    +arrow(ix+150,iy+180,ix+200,iy+44,NAVY,5,18))
lbl=(lab(X+ix+160,Y+iy+30,120,'forza',NAVY,20,900)+lab(X+ix+10,Y+iy+140,120,'flusso',GREY,20,900)+lab(X+ix+160,Y+iy+100,120,'portanza',GREEN,20,900)
     +lab(X+ix+140,Y+iy+186,140,'resistenza',CORAL,20,900)
     +lab(X+120,Y+100,380,'vortice di penna',CORAL,24,900)+lab(X+80,Y+380,300,'vortice sotto il boma',CORAL,24,900)
     +lab(X+mx+60,Y+120,160,'l\'aria scavalca',BLUE,22,900)+lab(X+830,Y+320,200,'rotta',NAVY,24,900))
txt=(item(1,BLUE,'La vela è finita','Sopravvento c\'è pressione, sottovento depressione: l\'aria scavalca la penna e passa sotto il boma.')
     +item(2,CORAL,'I vortici d\'estremità','Grandi vortici che si perdono nella scia, disperdendo energia.')
     +item(3,PURPLE,'Helmholtz, ancora','Compensano di continuo il vortice di partenza lasciato indietro.')
     +item(4,GREEN,'Di bolina','Gran parte della resistenza è indotta: è il prezzo della portanza.')
     +fonte('§4.6'))
sec('indotta',head('La vela è un\'ala','Resistenza indotta e vortici',CORAL),pinned=svgp(X,Y,W,Hh,b,'Barca a vela vista di fianco che naviga verso destra: dalla penna e da sotto il boma partono due vortici a spirale che restano indietro nella scia; una freccia blu mostra l\'aria che scavalca la penna. In un riquadro la forza sulla vela è inclinata all\'indietro e si scompone in portanza verso l\'alto e resistenza indotta')+lbl+pcol(txt,532,18),
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.6, «Resistenza indotta e vortici d\'estremità». Su una lastra reale la forza è perpendicolare al profilo e non al flusso indisturbato: ne nasce una componente parallela al moto, la resistenza indotta (riquadro in alto). La vela ha dimensioni finite: la differenza di pressione spinge l\'aria a scavalcare le estremità libere, sopra la penna e sotto il boma, e si formano vortici d\'estremità che si disperdono nella scia con forte dissipazione di energia. Per il teorema di Helmholtz sulla conservazione della vorticità, il vortice di partenza perso nella scia viene compensato di continuo dai vortici d\'estremità, a spese della velocità della barca. Nelle andature controvento la maggior parte della resistenza è indotta dalla portanza stessa. Disegno schematico.')

quiz_slide('quizB','Verifica · la vela è un\'ala',['2.1.1-84','2.1.1-83','2.1.1-39'],False)
quiz_slide('quizBr','Verifica · la vela è un\'ala',['2.1.1-84','2.1.1-83','2.1.1-39'],True)

# ============ ANDATURE (disegno a destra) ============
X=700
s2,cx2,cy2=78,280,300
left=flow_lines('vela',s2,cx2,cy2,w=2.5)+body('vela',s2,cx2,cy2,fill='none',st=NAVY,sw=7)+wind(20,470,90)
right=''
for yy in [120,170,220,380,430,480]:
    right+=f'<path d="M580 {yy} C680 {yy} 740 {yy+(40 if yy<300 else -40)*0} 800 {yy + (-30 if yy<300 else 30)} S 980 {yy+(-60 if yy<300 else 60)} 1080 {yy+(-70 if yy<300 else 70)}" fill="none" stroke="{FLOW}" stroke-width="2.5"/>'
right+=f'<path d="M800 150 Q760 300 800 450" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>'
for (vx,vy,r) in [(860,230,26),(880,300,32),(860,370,28),(940,260,24),(950,340,26)]:
    right+=f'<path d="M{vx+r} {vy} A{r} {r} 0 1 0 {vx} {vy+r} A{r*0.6:.0f} {r*0.6:.0f} 0 1 0 {vx+r*0.3:.0f} {vy-r*0.2:.0f}" fill="none" stroke="{CORAL}" stroke-width="3.5"/>'
right+=wind(590,560,90)+arrow(820,300,960,300,NAVY,8,24)
b=left+f'<path d="M546 20 L546 600" stroke="{PANEL_W}" stroke-width="5"/>'+right
lbl=(lab(X+40,Y+40,480,'bolina e traverso: portanza',SEA,26,900)+lab(X+590,Y+40,480,'poppa: resistenza',CORAL,26,900)
     +lab(X+40,Y+520,400,'flusso attaccato',INK,24,700)+lab(X+700,Y+520,360,'vela in stallo',INK,24,700))
txt=(item(1,SEA,'Bolina e traverso','La vela lavora come un\'ala: flusso attaccato, conta la portanza.')
     +item(2,PURPLE,'Lasco','Portanza e resistenza lavorano insieme.')
     +item(3,CORAL,'Poppa','La vela è di traverso al vento, in stallo: spinge la resistenza.')
     +item(4,BLUE,'Per questo','In poppa conta la superficie: spinnaker e gennaker grandi.')
     +fonte('cap. 4, introduzione'))
sec('andature',head('In pratica','Portanza e andature',BLUE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'A sinistra una vela di bolina con il flusso attaccato che la segue su entrambi i lati; a destra una vela in poppa messa di traverso al vento, con il flusso che si stacca e vortici rossi dietro')+lbl,
 notes='Nelle andature strette la vela lavora in portanza, con il flusso attaccato; in poppa la vela è perpendicolare al vento, completamente in stallo, e la spinta viene dalla resistenza. A sinistra flusso calcolato, a destra schema.')

# ============ FILETTI (disegno a sinistra) ============
X=128
def tt(x,y,wavy,c):
    if wavy: return f'<path d="M{x} {y} q12 -18 24 0 t24 0 t24 0" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
    return f'<path d="M{x} {y} L{x+72} {y+4}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
cols=[('Filetti dritti','regolata bene',False,False,GREEN),('Gira il sopravvento','cazza o poggia',True,False,BLUE),('Gira il sottovento','lasca o orza',False,True,CORAL)]
b=''
for i,(t,a_,wu,wd,c) in enumerate(cols):
    x0=40+i*350
    b+=f'<rect x="{x0}" y="60" width="320" height="440" rx="28" fill="#FFFFFF" fill-opacity="0.55"/>'
    b+=f'<path d="M{x0+40} 280 Q{x0+160} 210 {x0+290} 250" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/><circle cx="{x0+40}" cy="280" r="14" fill="{NAVY}"/>'
    b+=tt(x0+110,226,wd,CORAL)+tt(x0+110,290,wu,GREEN)
    b+=arrow(x0+10,380,x0+90,340,GREY,6,20)
lbl=''
for i,(t,a_,wu,wd,c) in enumerate(cols):
    x0=40+i*350
    lbl+=lab(X+x0+10,Y+70,300,t,c,26,900,'center')+lab(X+x0+10,Y+430,300,a_,INK,26,900,'center')
lbl+=lab(X+50,Y+520,1000,'rosso: filetto sottovento · verde: filetto sopravvento · freccia: vento apparente',INK,24,700)
txt=(item(1,GREEN,'Dritti tutti e due','Il flusso è attaccato su entrambi i lati: la vela porta al massimo.')
     +item(2,BLUE,'Gira il sopravvento','Angolo troppo piccolo, la vela fileggia: poggia o cazza.')
     +item(3,CORAL,'Gira il sottovento','Angolo troppo grande: sottovento c\'è stallo. Orza o lasca.')
     +item(4,PURPLE,'Barra e ruota','Barra: spostala verso il filetto che gira. Ruota: girala dalla parte opposta.')
     +fonte('§4.4', 'A. Gentry'))
sec('filetti',head('In pratica','I filetti',GREEN),pinned=svgp(X,Y,W,Hh,b,'Tre sezioni di vela viste dall\'alto con due filetti ciascuna, uno sottovento rosso e uno sopravvento verde: nella prima sono dritti, nella seconda gira quello sopravvento, nella terza gira quello sottovento',pan=True)+lbl+pcol(txt,532,18),
 notes='I filetti (tell-tales) sono fili leggeri vicino all\'inferitura, su tutti e due i lati. Arvel Gentry racconta di aver messo 500 filetti sul fiocco e propone una fila di filetti corti a partire dall\'inferitura: così si vede non solo quando la vela è stallata ma anche quanto si è vicini, tra fileggiare e stallo. Laura Romanò, «La fisica in barca a vela», paragrafo 4.4: angolo d\'attacco troppo piccolo, la vela fileggia, il flusso si separa sopravvento e il filetto sopravvento si muove in modo irregolare: poggiare o cazzare. Angolo corretto: i filetti all\'inferitura sono stesi. Angolo troppo grande, stallo: il flusso si separa sottovento e i filetti interni oscillano: orzare o lascare. Regola per il timoniere: con la barra si sposta la barra nella direzione in cui si orienta il segnavento che gira; con la ruota si gira nella direzione opposta.')

# ============ POSIZIONE DEI FILETTI (disegno a destra) ============
X=700
tack,head_,clew=(170,570),(420,40),(640,560)
jib=f'<path d="M{tack[0]} {tack[1]} L{head_[0]} {head_[1]} Q{600} {300} {clew[0]} {clew[1]} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
stay=f'<path d="M{tack[0]-20} {tack[1]+30} L{head_[0]+8} {head_[1]-30}" stroke="{NAVY}" stroke-width="3"/>'
tt9=''
for h in (0.18,0.44,0.7):
    Lx,Ly=tack[0]+(head_[0]-tack[0])*h, tack[1]+(head_[1]-tack[1])*h
    Rx,Ry=clew[0]+(head_[0]-clew[0])*h, clew[1]+(head_[1]-clew[1])*h
    for f_ in (0.15,0.5,0.82):
        x,y=Lx+(Rx-Lx)*f_, Ly+(Ry-Ly)*f_
        tt9+=f'<path d="M{x+4:.0f} {y+18:.0f} q10 -8 20 0 t20 0" fill="none" stroke="{CORAL}" stroke-width="5" stroke-linecap="round" stroke-dasharray="6 5"/>'
        tt9+=f'<path d="M{x:.0f} {y:.0f} q10 -8 20 0 t20 0" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linecap="round"/><circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{NAVY}"/>'
vane=(f'<path d="M{head_[0]} {head_[1]-30} L{head_[0]} {head_[1]-4}" stroke="{NAVY}" stroke-width="3"/>')
grad=''
for yy,L,c in [(120,300,CORAL),(300,220,ORANGE),(480,140,SUN)]:
    grad+=arrow(720,yy,720+L,yy,c,10,28)
grad+=f'<path d="M700 60 L700 540" stroke="{NAVY}" stroke-width="3" stroke-dasharray="8 8"/>'
b=jib+stay+tt9+vane+f'<path d="M680 20 L680 600" stroke="{PANEL_W}" stroke-width="5"/>'+grad
lbl=(lab(X+710,Y+150,340,'in alto più vento',CORAL,24,900)+lab(X+710,Y+330,340,'a metà',ORANGE,24,900)+lab(X+710,Y+510,340,'in basso meno vento',INK,24,900)
     +lab(X+30,Y+40,300,'3 altezze × 3 = 9 filetti',NAVY,24,900)+lab(X+30,Y+84,260,'verde: lato visibile',GREEN,22,900)+lab(X+30,Y+116,260,'rosso: l\'altro lato',CORAL,22,900))
txt=(item(1,NAVY,'Segnavento','Banderuola in testa d\'albero; fili di lana sulle sartie, utili con poco vento e mare formato.')
     +item(2,GREEN,'I tell tales','Fili di lana o nylon di circa 10 cm incollati sulla vela, sopravvento e sottovento.')
     +item(3,CORAL,'Almeno 3 altezze','Il vento cambia con l\'altezza e la vela è svergolata: ogni quota va letta da sola.')
     +item(4,PURPLE,'Ne bastano 9','Per leggere bene l\'angolo di incidenza su tutta la vela.')
     +fonte('§4.4'))
sec('posfiletti',head('In pratica','Dove mettere i filetti',GREEN)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Un fiocco visto di fianco con nove filetti su tre altezze e tre posizioni, verdi sul lato visibile e rossi tratteggiati sull\'altro lato; a destra tre frecce del vento, più lunga in alto e più corta in basso, per mostrare che il vento cresce con l\'altezza')+lbl,
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.4, «I segnavento ovvero i tell tales». Per vedere il vento: frecce o banderuole in testa d\'albero, molto affidabili in condizioni normali, e fili di lana sulle sartie, utili con vento debole o mare formato che fa rollare la barca. I tell tales sono piccoli fili di lana o nylon di circa 10 centimetri incollati sulla vela: mostrano se il flusso è parallelo alla superficie o se si separa. Vanno messi sia sopravvento sia sottovento, e almeno su tre altezze, perché il vento cambia con l\'altezza e la vela è svergolata; in tutto nove segnavento bastano per una diagnosi accurata dell\'angolo di incidenza. Nel disegno le tre posizioni su ogni altezza vanno dall\'inferitura alla balumina; i più importanti per la regolazione sono quelli vicino all\'inferitura.')

# ============ GRASSO (disegno a sinistra) ============
X=128
def sect(x0,depth,c):
    return (f'<path d="M{x0} 330 Q{x0+140} {330-2*depth} {x0+280} 330" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="{x0}" cy="330" r="13" fill="{NAVY}"/><path d="M{x0} 330 L{x0+280} 330" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8"/>'
            +arrow(x0+140,330,x0+140,330-depth+6,c,4,14))
b=sect(60,22,BLUE)+sect(410,38,SEA)+sect(760,58,CORAL)+wind(40,500,110)
lbl=(lab(X+40,Y+380,320,'magra',BLUE,28,900,'center')+lab(X+390,Y+380,320,'media',SEA,28,900,'center')+lab(X+740,Y+380,320,'grassa',CORAL,28,900,'center')
     +lab(X+40,Y+420,320,'vento forte',INK,24,700,'center')+lab(X+390,Y+420,320,'vento medio',INK,24,700,'center')+lab(X+740,Y+420,320,'vento leggero, onda',INK,24,700,'center')
     +lab(X+180,Y+60,760,'il grasso è la profondità della curva (freccia)',INK,24,700,'center'))
txt=(item(1,CORAL,'Vela grassa','Più concava: più portanza e più spinta, anche più resistenza.')
     +item(2,BLUE,'Vela magra','Più piatta: meno forza, meno sbandamento. Smagrire = ridurre la concavità.')
     +item(3,SEA,'Come si smagrisce','Cazza cunningham, tesabase e paterazzo, la drizza del genoa; carrello del genoa indietro.')
     +item(4,PURPLE,'Come si ingrassa','Lasca drizze, cunningham e tesabase: con poco vento e in poppa.'))
sec('grasso',head('In pratica','Grasso e magro',CORAL),pinned=svgp(X,Y,W,Hh,b,'Tre sezioni di vela viste dall\'alto: magra, media e grassa, con una freccia che indica la profondità della curva')+lbl+pcol(txt,532,18),
 notes='Quiz 2.1.1-80 (smagrire vuol dire ridurre la concavità: vero), 2.3.1-52 (per ridurre lo sbandamento si smagriscono le vele: vero), 2.3.1-53 (con vento debole si smagrisce: falso), 2.1.1-95 (lascare drizza e base della randa aumenta il grasso: vero), 2.1.1-86 (la concavità serve a diminuire la resistenza: falso).')

# ============ FESSURA (disegno a destra) ============
X=700
main=f'<path d="M500 330 Q740 240 1000 350" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/><circle cx="500" cy="330" r="14" fill="{NAVY}"/>'
jib=f'<path d="M180 360 Q360 230 600 230" fill="none" stroke="{PURPLE}" stroke-width="9" stroke-linecap="round"/><circle cx="180" cy="360" r="9" fill="{PURPLE}"/>'
fl=''
for d in ['M20 90 C300 80 600 90 1080 150','M20 190 C200 185 350 170 480 180 S 750 200 1080 250',
          'M20 380 C120 380 200 335 320 318 S 520 285 600 268 S 820 250 1080 300',
          'M20 440 C200 440 420 400 600 380 S 900 390 1080 420','M20 500 C300 505 700 470 1080 490','M20 570 C300 575 700 560 1080 570']:
    fl+=f'<path d="{d}" fill="none" stroke="{FLOW}" stroke-width="3"/>'
b=(fl+main+jib+wind(30,560,110)
   +arrow(110,405,165,378,GREEN,6,18)+arrow(625,222,745,212,CORAL,6,18)
   +f'<path d="M520 405 L595 285" stroke="{SEA}" stroke-width="3" stroke-dasharray="7 6"/><circle cx="598" cy="280" r="7" fill="{SEA}"/>')
lbl=(lab(X+40,Y+510,300,'vento apparente',INK,24,800)+lab(X+380,Y+410,330,'nella fessura l\'aria rallenta',SEA,24,900)
     +lab(X+650,Y+150,420,'uscita del fiocco: flusso veloce',CORAL,24,900)+lab(X+30,Y+420,300,'upwash: il fiocco stringe',GREEN,24,900)
     +lab(X+890,Y+370,160,'randa',NAVY,26,900)+lab(X+300,Y+200,160,'fiocco',PURPLE,26,900))
txt=(item('✗',CORAL,'Il mito del Venturi','«Il fiocco accelera l\'aria nella fessura e la soffia sulla randa»: falso.')
     +item(1,SEA,'Nel canale','Con il fiocco le linee di flusso nel canale passano da 3 a 1: l\'aria rallenta, la pressione sale.')
     +item(2,GREEN,'Il fiocco porta di più','Il suo punto di ristagno va sopravvento: nell\'upwash della randa vede un vento più favorevole.')
     +item(3,PURPLE,'La randa porta meno','Il ristagno si sposta verso l\'inferitura, ma stalla meno. Fiocco troppo cazzato: la randa sventa.')
     +fonte('§4.5', 'A. Gentry'))
sec('fessura',head('In pratica','Fiocco e randa: la fessura',PURPLE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Fiocco e randa visti dall\'alto con le linee del vento: tra le due vele le linee si allargano perché l\'aria rallenta; davanti al fiocco il vento arriva più aperto; dietro al fiocco un flusso veloce')+lbl,
 notes='Arvel Gentry (1971, poi «A Review of Modern Sail Theory»): l\'effetto fessura non è un Venturi. Il fiocco devia sul suo lato sottovento gran parte dell\'aria che andrebbe nella fessura: quella che resta rallenta e la pressione nella fessura sale; il fiocco riduce le velocità sul lato sottovento della randa e quindi il rischio di distacco. La randa, a sua volta, crea upwash davanti al fiocco: il fiocco vede il vento più aperto e si può stringere di più. Disegno schematico. Laura Romanò, «La fisica in barca a vela», paragrafo 4.5, «Interazione tra le vele»: confrontando la randa isolata con randa e fiocco, le linee di flusso nel canale diminuiscono, per esempio da 3 a 1; sulla randa il punto di ristagno si sposta verso l\'inferitura (porta meno); la linea di ristagno del fiocco si sposta molto sopravvento (la sua portanza aumenta); gran parte del flusso passa all\'esterno, sottovento al fiocco, e la zona tra le vele diventa una regione di alta pressione e di rallentamento. L\'effetto totale delle due vele non è una semplice somma.')

# ============ IL CANTIERE IN AUTOSTRADA (disegno a sinistra) ============
X=128
def car(x,y,c):
    return (f'<rect x="{x}" y="{y-22}" width="74" height="44" rx="12" fill="{c}" stroke="{NAVY}" stroke-width="3"/>'
            f'<rect x="{x+46}" y="{y-16}" width="16" height="32" rx="4" fill="#DCEBF5"/><rect x="{x+10}" y="{y-14}" width="12" height="28" rx="3" fill="#DCEBF5"/>')
def fast(x,y): return ''.join(f'<path d="M{x-14-10*i} {y-12+12*i} L{x-50-10*i} {y-12+12*i}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>' for i in range(3))
road=(f'<rect x="0" y="110" width="{W}" height="380" fill="#5B6573"/>'
      f'<path d="M0 116 L{W} 116 M0 484 L{W} 484" stroke="#FFFFFF" stroke-width="6"/>'
      f'<path d="M0 237 L{W} 237 M0 363 L{W} 363" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="36 28"/>')
work=f'<defs><pattern id="zz" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="14" height="28" fill="{ORANGE}"/><rect x="14" width="14" height="28" fill="#FFFFFF"/></pattern></defs>'
work+=f'<rect x="640" y="248" width="240" height="104" rx="10" fill="url(#zz)" stroke="{NAVY}" stroke-width="4"/>'
for cx_ in (600,560):
    work+=f'<path d="M{cx_} 322 L{cx_+12} 282 L{cx_+24} 322 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="2"/>'
cars=''.join(car(x,300,c) for x,c in [(150,CORAL),(240,BLUE),(330,PURPLE),(420,SEA),(505,SUN)])
for x,c in [(120,GREEN),(520,BLUE),(930,CORAL)]: cars+=fast(x,176)+car(x,176,c)
for x,c in [(260,SUN),(700,PURPLE),(990,SEA)]: cars+=fast(x,424)+car(x,424,c)
cars+=f'<path d="M500 280 C560 250 580 200 640 186" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="10 8"/>'+head_at(640,186,-15,'#FFFFFF',16)
cars+=f'<path d="M500 320 C560 350 580 400 640 414" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="10 8"/>'+head_at(640,414,15,'#FFFFFF',16)
b=road+work+cars
lbl=(lab(X+120,Y+54,520,'corsia libera: le auto accelerano',SEA,24,900)+lab(X+150,Y+238,420,'coda: rallentano',SUN,24,900,'left','rgba(27,42,65,0.75)')
     +lab(X+640,Y+54,420,'cantiere: il restringimento',ORANGE,24,900)
     +lab(X+30,Y+510,1040,'cantiere = fessura tra randa e fiocco: l\'aria rallenta e la pressione sale',CORAL,24,900)
     +lab(X+30,Y+556,1040,'corsie libere = sottovento al fiocco: l\'aria accelera e la pressione scende',SEA,24,900))
txt=(item('✗',CORAL,'Non è un Venturi','Tra randa e fiocco non c\'è un tubo chiuso: il canale è immerso nell\'aria libera.')
     +item(1,ORANGE,'Il canale frena','L\'aria sente il restringimento come una resistenza: dentro rallenta, la pressione sale.')
     +item(2,SEA,'La via più comoda','Il resto dell\'aria passa fuori, sottovento al fiocco, e accelera.')
     +item(3,PURPLE,'La portata','Si conserva nel sistema intero, non nello spazio tra le vele.')
     +fonte('§4.5 «Il paradosso del restringimento aperto»'))
sec('autostrada',head('In pratica','Il cantiere in autostrada',ORANGE),pinned=svgp(X,Y,W,Hh,b,'Autostrada a tre corsie vista dall\'alto: nella corsia centrale un cantiere con coni; prima del cantiere le auto sono in coda, alcune si spostano nelle corsie laterali dove corrono veloci. Sotto il paragone: il cantiere è la fessura tra le vele, le corsie libere sono l\'aria sottovento al fiocco',pan=False)+lbl+pcol(txt,532,18),
 notes='Da Laura Romanò, «La fisica in barca a vela», paragrafo 4.5, «Il paradosso del restringimento aperto». Perché l\'effetto Venturi non si applica tra le vele: il restringimento tra randa e fiocco non è un condotto isolato ma è immerso nell\'aria libera. L\'aria percepisce il canale stretto come una zona di maggiore resistenza e sceglie la via più conveniente: rallenta nel canale, dove la pressione aumenta, e accelera all\'esterno, dove la pressione diminuisce. L\'analogia del libro è il cantiere in autostrada: vicino a un restringimento per lavori le auto rallentano e fanno coda; se ci sono corsie libere, deviano lì e accelerano, come fa l\'aria attorno al fiocco. La costanza della portata vale per l\'intero sistema, non per il solo spazio tra le vele.')

quiz_slide('quizC','Verifica · in pratica',['2.1.1-80','2.3.1-55','2.1.1-86'],False)
quiz_slide('quizCr','Verifica · in pratica',['2.1.1-80','2.3.1-55','2.1.1-86'],True)

# ============ WEB ============
rows=[('«L\'aria di sopra deve arrivare insieme a quella di sotto»','Falso: quella di sopra arriva prima','NASA Glenn · Incorrect Lift Theory'),
      ('«La portanza è solo Bernoulli» oppure «è solo Newton»','Falso: sono due descrizioni corrette','NASA Glenn · Bernoulli and Newton'),
      ('«Tra randa e fiocco c\'è un tubo di Venturi»','Falso: il canale è aperto, l\'aria rallenta','L. Romanò §4.5 · A. Gentry'),
      ('«Basta un fluido ideale per spiegare la portanza»','Falso: senza viscosità niente portanza','L. Romanò §4.3'),
      ('«La randa fa lavorare il fiocco con un vento più favorevole»','Vero: è l\'upwash della randa','A. Gentry · Modern Sail Theory'),
      ('«Filetto sottovento che gira: vela in stallo»','Vero: il flusso si è staccato','L. Romanò §4.4 · A. Gentry')]
sec('web',head('In pratica','Vero o falso? Web e libri a confronto',BLUE)+table(['Si legge…','Vero o falso?','Fonte'],[46,28,26],rows,BLUE,25)
    +note('Diffida delle spiegazioni troppo semplici: la vela ha i due lati lunghi uguali.',CORAL,38),
 notes='Fonti: '+ROM+'; NASA Glenn Research Center, «Incorrect Lift Theory» (grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/wrong1.html) e «Bernoulli and Newton» (www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoulli-and-newton); Arvel Gentry, «A Review of Modern Sail Theory», con l\'effetto fessura e i filetti (copia su oceansailing.meder.hu). Il vecchio sito gentrysailing.com oggi reindirizza a un sito estraneo: non usarlo.',gap=28)

closing(['Portanza: la forza perpendicolare al vento; resistenza: quella parallela',
         'L\'ala e la vela deviano l\'aria grazie alla viscosità: sottovento depressione, sopravvento pressione',
         'Più incidenza, più portanza, fino allo stallo: filetto sottovento che gira',
         'Forza totale = propulsione (lungo l\'asse) + scarroccio (di lato)',
         'Nella fessura l\'aria rallenta: il fiocco porta di più, la randa stalla meno'],
 'Buon vento, e vele ben regolate!','Appendice M · La portanza. Fonte principale: '+ROM+'.')
write_deck(OUT,'Appendice M · La portanza',ORDER,
 {"s1":{"description":"Che cos'è la portanza: controvento, forza, Newton, Bernoulli, il mito del percorso più lungo","start":"cover"},
  "s2":{"description":"Come nasce la portanza (Romanò, cap. 4.3): viscosità, vortice di partenza, Magnus, energia","start":"viscosita"},
  "s3":{"description":"Da cosa dipende: incidenza, stallo, velocità e superficie","start":"incidenza"},
  "s4":{"description":"La vela è un'ala: pressioni, propulsione e scarroccio, deriva, resistenza indotta","start":"ala"},
  "s5":{"description":"In pratica: andature, filetti, grasso, fessura, il cantiere in autostrada, web e libri","start":"andature"}})
print('ok')
