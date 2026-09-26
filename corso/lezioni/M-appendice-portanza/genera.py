"""Appendice M: la portanza, dall'ala alla vela (quiz vela 2.1.1, 2.3.1). Disegni dal flusso calcolato in flow_lines.json."""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
FL=json.load(open(SP+'/flow_lines.json'))
ORDER=['cover','indice','forza','mano','newton','bernoulli','mito','quizA','quizAr',
       'incidenza','stallo','fattori','ala','scomposizione','deriva','quizB','quizBr',
       'andature','filetti','grasso','fessura','quizC','quizCr','web','chiusura']
EB='Appendice M · La portanza'
LB.ICON_T.update({'Indice':'book','Portanza e resistenza':'wind','La mano fuori dal finestrino':'wind','Deviare l\'aria: Newton':'wind',
 'Le pressioni: Bernoulli':'chart','Il mito del percorso più lungo':'star','L\'angolo di incidenza':'compass','Lo stallo':'wind',
 'Da cosa dipende la portanza':'chart','La vela è un\'ala':'sail','Propulsione e scarroccio':'sail','Anche la deriva è un\'ala':'hull',
 'Portanza e andature':'sail','I filetti':'flag','Grasso e magro':'sail','Fiocco e randa: la fessura':'sail','Cosa si dice sul web':'book'})
FLOW='#6FB7C2'

# ---------------- disegni ----------------
def T(x,y,s,cx,cy): return cx+s*x, cy-s*y
def flow_lines(k,s,cx,cy,c=FLOW,w=3,op=1.0,skip=()):
    out=''
    for i,L in enumerate(FL[k]['lines']):
        if i in skip: continue
        pts=L['pts']; st=max(1,len(pts)//90)
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
cover_app('M','La portanza','Perché un\'ala vola e una vela spinge la barca controvento: pressioni, flusso deviato, incidenza, stallo, filetti e fessura tra fiocco e randa',
 'Appendice M al corso. La teoria della portanza spiegata passo per passo e applicata alla vela, con i quiz ufficiali di vela 2.1.1 e 2.3.1 e il confronto con le spiegazioni che circolano sul web (NASA, Arvel Gentry). Collegata alla lezione 8.')
index_slide(EB,[('Che cos\'è la portanza','Forza, Newton, Bernoulli e il mito del percorso più lungo',['forza','mano','newton','bernoulli','mito','quizA','quizAr'],CORAL),
 ('Da cosa dipende','Incidenza, stallo, velocità e superficie',['incidenza','stallo','fattori'],SEA),
 ('La vela è un\'ala','Pressioni, propulsione e scarroccio, la deriva',['ala','scomposizione','deriva','quizB','quizBr'],PURPLE),
 ('In pratica','Andature, filetti, grasso e fessura, cosa si dice sul web',['andature','filetti','grasso','fessura','quizC','quizCr','web'],BLUE)],ORDER,
 'Un\'ala e una vela funzionano allo stesso modo: deviano il vento.',
 'Appendice di approfondimento sulla portanza. I disegni del flusso sono calcolati: linee di corrente e pressioni di un profilo alare in un fluido ideale (profilo di Joukowski con la condizione di Kutta).')

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
     +item(4,CORAL,'Più aria devii','Più forte o più angolata è la deviazione, più grande è la portanza.'))
sec('newton',head('Che cos\'è la portanza','Deviare l\'aria: Newton',PURPLE),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con le linee di corrente calcolate: davanti al profilo le linee salgono, dietro scendono; una freccia verso l\'alto sul profilo e una verso il basso sull\'aria')+lbl+pcol(txt,532,18),
 notes='La spiegazione «di Newton»: l\'ala cambia la direzione dell\'aria, quindi le imprime una forza verso il basso; per la terza legge l\'aria restituisce all\'ala una forza verso l\'alto. NASA Glenn Research Center, pagina «Bernoulli and Newton»: le due spiegazioni sono entrambe corrette e descrivono lo stesso fenomeno.')

# ============ BERNOULLI (disegno a destra) ============
X=700
s,cx,cy=160,546,320
b=(flow_lines('profilo',s,cx,cy,op=0.45)+body('profilo',s,cx,cy)+pressure('profilo',s,cx,cy,sc=40)+wind(40,90))
lbl=(lab(X+cx-200,Y+100,420,'depressione (–): l\'aria corre',CORAL,26,900,'center')+lab(X+cx-200,Y+470,420,'sovrappressione (+): l\'aria rallenta',BLUE,26,900,'center')
     +lab(X+50,Y+122,200,'vento',INK,24,800))
txt=(item(1,CORAL,'Sopra: veloce','Sopra il profilo l\'aria accelera e la pressione scende: aspira.')
     +item(2,BLUE,'Sotto: più lenta','Sotto l\'aria rallenta e la pressione sale: spinge.')
     +item(3,SEA,'Bernoulli','Dove la velocità aumenta la pressione diminuisce, e viceversa.')
     +item(4,PURPLE,'Newton o Bernoulli?','Entrambi: sono due modi di descrivere la stessa forza (NASA).'))
sec('bernoulli',head('Che cos\'è la portanza','Le pressioni: Bernoulli',BLUE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con le frecce di pressione calcolate: sopra frecce rosse che escono dal profilo, la depressione più forte vicino al bordo d\'ingresso; sotto frecce blu che spingono verso il profilo')+lbl,
 notes='Le frecce sono il coefficiente di pressione calcolato sulla superficie del profilo. La depressione sul dorso è più grande della sovrappressione sul ventre e si concentra nella parte anteriore. NASA Glenn Research Center: «Both Bernoulli and Newton are correct».')

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
     +item(2,PURPLE,'La prova','Profili simmetrici e aerei in volo rovescio portano lo stesso.')
     +item(3,BLUE,'E la vela?','Una vela ha i due lati lunghi uguali, eppure produce portanza.'))
sec('mito',head('Che cos\'è la portanza','Il mito del percorso più lungo',CORAL),pinned=svgp(X,Y,W,Hh,b,'Profilo alare con due linee di corrente evidenziate, una sopra in rosso e una sotto in blu; pallini segnano dove si trova l\'aria negli stessi istanti: il pallino di sopra arriva al bordo d\'uscita molto prima di quello di sotto')+lbl+pcol(txt,532,16),
 notes='NASA Glenn Research Center, «Incorrect Lift Theory»: la teoria del «tempo di transito uguale» o «percorso più lungo» è la spiegazione sbagliata più diffusa. «The actual velocity over the top of an airfoil is much faster than that predicted by the Longer Path theory and particles moving over the top arrive at the trailing edge before particles moving under the airfoil.» I pallini del disegno sono calcolati: posizioni dell\'aria a intervalli di tempo uguali lungo due linee di corrente.')

quiz_slide('quizA','Verifica · che cos\'è la portanza',['2.1.1-73','2.1.1-37','2.1.1-58'],False)
quiz_slide('quizAr','Verifica · che cos\'è la portanza',['2.1.1-73','2.1.1-37','2.1.1-58'],True)

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
     +item(2,CORAL,'Più angolo, più portanza','Fino a un limite: oltre, il flusso si stacca e la vela stalla.')
     +item(3,PURPLE,'Troppo poco','Con angolo quasi nullo la vela non porta e fileggia.')
     +item(4,BLUE,'Per il quiz','La pressione del vento sulle vele dipende dall\'angolo di incidenza: vero.'))
sec('incidenza',head('Da cosa dipende','L\'angolo di incidenza',SEA)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Grafico qualitativo: la portanza cresce con l\'angolo di incidenza fino a un massimo, poi crolla nella zona dello stallo; sotto, tre profili a incidenza piccola, media e troppo grande')+lbl,
 notes='Grafico qualitativo, senza numeri: l\'angolo di stallo dipende dal profilo e, per una vela, dalla sua forma e dalla regolazione. Quiz 2.1.1-28 e 2.1.1-96 (definizione dell\'angolo di incidenza), 2.1.1-37 e -38 (la pressione del vento dipende dall\'angolo di incidenza).')

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
     +item(3,PURPLE,'Cosa succede','Vortici sul dorso: la portanza crolla, la resistenza cresce.')
     +item(4,BLUE,'A bordo','Filetti sottovento che girano: lasca la vela o orza un poco.'))
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
     +item(4,PURPLE,'Davanti lavora di più','La depressione più forte è vicino all\'albero, verso l\'inferitura.'))
sec('ala',head('La vela è un\'ala','La vela è un\'ala',PURPLE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Vela vista dall\'alto come un arco sottile dietro all\'albero, con le linee di corrente calcolate e le frecce di pressione: rosse di depressione sul lato sottovento, blu di pressione sul lato sopravvento')+lbl,
 notes='Il disegno è una vela sottile a forma di arco, con il flusso calcolato: si vedono le pressioni sui due lati. Quiz 2.1.1-58: «Si intende per lato sottovento la superficie sopravvento della vela che è sottoposta a una depressione» è FALSO: la depressione è sul lato sottovento.')

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

quiz_slide('quizB','Verifica · la vela è un\'ala',['2.1.1-84','2.1.1-83','2.1.1-39'],False)
quiz_slide('quizBr','Verifica · la vela è un\'ala',['2.1.1-84','2.1.1-83','2.1.1-39'],True)

# ============ ANDATURE (disegno a sinistra) ============
X=128
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
     +item(4,BLUE,'Per questo','In poppa conta la superficie: spinnaker e gennaker grandi.'))
sec('andature',head('In pratica','Portanza e andature',BLUE),pinned=svgp(X,Y,W,Hh,b,'A sinistra una vela di bolina con il flusso attaccato che la segue su entrambi i lati; a destra una vela in poppa messa di traverso al vento, con il flusso che si stacca e vortici rossi dietro')+lbl+pcol(txt,532,18),
 notes='Nelle andature strette la vela lavora in portanza, con il flusso attaccato; in poppa la vela è perpendicolare al vento, completamente in stallo, e la spinta viene dalla resistenza. A sinistra flusso calcolato, a destra schema.')

# ============ FILETTI (disegno a destra) ============
X=700
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
     +item(2,BLUE,'Gira il sopravvento','Vela troppo lascata o prua troppo al vento: cazza o poggia.')
     +item(3,CORAL,'Gira il sottovento','Vela troppo cazzata: sottovento c\'è stallo. Lasca o orza.')
     +item(4,PURPLE,'Il trucco di Gentry','Una fila di filetti corti dall\'inferitura mostra quanto sei vicino allo stallo.'))
sec('filetti',head('In pratica','I filetti',GREEN)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Tre sezioni di vela viste dall\'alto con due filetti ciascuna, uno sottovento rosso e uno sopravvento verde: nella prima sono dritti, nella seconda gira quello sopravvento, nella terza gira quello sottovento',pan=True)+lbl,
 notes='I filetti (tell-tales) sono fili leggeri vicino all\'inferitura, su tutti e due i lati. Arvel Gentry racconta di aver messo 500 filetti sul fiocco e propone una fila di filetti corti a partire dall\'inferitura: così si vede non solo quando la vela è stallata ma anche quanto si è vicini, tra fileggiare e stallo.')

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
     +item(1,SEA,'Nella fessura','L\'aria rallenta e la pressione sale: la randa sottovento stalla meno.')
     +item(2,GREEN,'Il fiocco','Lavora nell\'upwash della randa: vede il vento più favorevole e fa stringere.')
     +item(3,PURPLE,'Troppo cazzato','Il fiocco chiude la fessura e la randa «sventa» all\'inferitura.'))
sec('fessura',head('In pratica','Fiocco e randa: la fessura',PURPLE)+col(txt,520,18),pinned=svgp(X,Y,W,Hh,b,'Fiocco e randa visti dall\'alto con le linee del vento: tra le due vele le linee si allargano perché l\'aria rallenta; davanti al fiocco il vento arriva più aperto; dietro al fiocco un flusso veloce')+lbl,
 notes='Arvel Gentry (1971, poi «A Review of Modern Sail Theory»): l\'effetto fessura non è un Venturi. Il fiocco devia sul suo lato sottovento gran parte dell\'aria che andrebbe nella fessura: quella che resta rallenta e la pressione nella fessura sale; il fiocco riduce le velocità sul lato sottovento della randa e quindi il rischio di distacco. La randa, a sua volta, crea upwash davanti al fiocco: il fiocco vede il vento più aperto e si può stringere di più. Disegno schematico.')

quiz_slide('quizC','Verifica · in pratica',['2.1.1-80','2.3.1-55','2.1.1-86'],False)
quiz_slide('quizCr','Verifica · in pratica',['2.1.1-80','2.3.1-55','2.1.1-86'],True)

# ============ WEB ============
rows=[('«L\'aria di sopra deve arrivare insieme a quella di sotto»','Falso: quella di sopra arriva prima','NASA Glenn · Incorrect Lift Theory'),
      ('«La portanza è solo Bernoulli» oppure «è solo Newton»','Falso: sono due descrizioni corrette','NASA Glenn · Bernoulli and Newton'),
      ('«Nella fessura il fiocco accelera l\'aria sulla randa»','Falso: nella fessura l\'aria rallenta','A. Gentry · Modern Sail Theory'),
      ('«La randa fa lavorare il fiocco con un vento più favorevole»','Vero: è l\'upwash della randa','A. Gentry · Modern Sail Theory'),
      ('«Filetto sottovento che gira: vela in stallo»','Vero: il flusso si è staccato','A. Gentry · Modern Sail Theory')]
sec('web',head('Cosa si dice sul web','Cosa si dice sul web',BLUE)+table(['Si legge…','Vero o falso?','Fonte'],[46,28,26],rows,BLUE,25)
    +note('Diffida delle spiegazioni troppo semplici: la vela ha i due lati lunghi uguali.',CORAL,38),
 notes='Fonti consultate: NASA Glenn Research Center, «Incorrect Lift Theory» (grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/wrong1.html) e «Bernoulli and Newton» (www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoulli-and-newton); Arvel Gentry, «A Review of Modern Sail Theory», con l\'effetto fessura e i filetti (copia su oceansailing.meder.hu). Il vecchio sito gentrysailing.com oggi reindirizza a un sito estraneo: non usarlo.',gap=28)

closing(['Portanza: la forza perpendicolare al vento; resistenza: quella parallela',
         'L\'ala e la vela deviano l\'aria: sottovento depressione, sopravvento pressione',
         'Più incidenza, più portanza, fino allo stallo: filetto sottovento che gira',
         'Forza totale = propulsione (lungo l\'asse) + scarroccio (di lato)',
         'Nella fessura l\'aria rallenta: il fiocco fa stringere, la randa stalla meno'],
 'Buon vento, e vele ben regolate!','Appendice M · La portanza')
write_deck(OUT,'Appendice M · La portanza',ORDER,
 {"s1":{"description":"Che cos'è la portanza: forza, Newton, Bernoulli, il mito del percorso più lungo","start":"cover"},
  "s2":{"description":"Da cosa dipende: incidenza, stallo, velocità e superficie","start":"incidenza"},
  "s3":{"description":"La vela è un'ala: pressioni, propulsione e scarroccio, la deriva","start":"ala"},
  "s4":{"description":"In pratica: andature, filetti, grasso, fessura e cosa si dice sul web","start":"andature"}})
