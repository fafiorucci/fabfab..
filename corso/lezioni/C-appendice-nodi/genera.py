"""Appendice C: i nodi marinari, che cosa sono, a che cosa servono e come si fanno, passo per passo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
import template as TP
import nodi
from corde import uid
OUT=SP+'/deck/project'

# icona «nodo»: una cima che fa un otto
TP.ICONS['nodo']=(f'<path d="M14 72 C30 72 34 30 52 30 C70 30 72 56 56 62 C40 68 30 46 44 38 C58 30 78 40 86 26" {TP.S}/>'
                  f'<path d="M50 62 C58 74 70 80 86 78" {TP.S}/>')

ORDER=['cover','indice','parole','scelta','savoia','gassa','parlato','bozza','bitta','galloccia','mezzi','piano','bandiera','margherita',
       'cime','quiz1','quiz1r','quiz2','quiz2r','chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
TIT={'savoia':'Il nodo Savoia','gassa':'La gassa d\'amante','parlato':'Il nodo parlato','bozza':'Il nodo di bozza','bitta':'Dare volta alla bitta',
     'galloccia':'Dare volta alla galloccia','mezzi':'Volta tonda e due mezzi colli','piano':'Il nodo piano','bandiera':'Il nodo bandiera',
     'margherita':'Il nodo margherita'}
LB.ICON_T.update({'Indice':'book','Le parole dei nodi':'nodo','Quale nodo per quale lavoro':'helm','Le cime: materiali e cura':'anchor','Glossario':'book'})
LB.ICON_T.update({t:'nodo' for t in TIT.values()})

PANEL='#E4F3F1'
def nbadge(x,y,n,c):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:44px; height:44px; font-family:{H}; font-size:26px; line-height:44px; font-weight:700; color:#FFFFFF; background:{c}; border-radius:22px; text-align:center">{n}</p>'
def figure(K,x0,y0,c):
    """Quattro pannelli numerati: 2×2 orizzontali oppure 4 verticali in fila."""
    out=''
    if K['layout']=='land':
        W,Hd,Ht=536,226,300; pos=[(x0+(i%2)*(W+20),y0+(i//2)*(Ht+20)) for i in range(4)]
    else:
        W,Hd,Ht=258,524,620; pos=[(x0+i*(W+20),y0) for i in range(4)]
    for i,((body,cap),(x,y)) in enumerate(zip(K['panels'],pos)):
        cid=f'cl{uid()}'
        svg=(f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="{W}" height="{Hd}" rx="0"/></clipPath></defs>'
             f'<rect x="0" y="0" width="{W}" height="{Ht}" rx="26" fill="{PANEL}"/><g clip-path="url(#{cid})">{body}</g>')
        out+=(f'<svg aria-label="Passo {i+1}: {cap}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Ht}" width="{W}" height="{Ht}" '
              f'style="position:absolute; left:{x}px; top:{y}px; width:{W}px; height:{Ht}px">{svg}</svg>')
        out+=nbadge(x+12,y+12,i+1,c)
        out+=f'<p style="position:absolute; left:{x+18}px; top:{y+Hd+8}px; width:{W-32}px; font-size:24px; line-height:1.25; font-weight:700; color:{INK}">{cap}</p>'
    return out

def knot_slide(sid,c,what,use,tip,notes,side):
    K=nodi.KNOTS[sid]()
    txt=(tag('Che cos\'è',c)+p(what,26,BODY,400,1.4)+tag('A che cosa serve',c)+p(use,26,BODY,400,1.4)+squiggle(c,140)+note(tip,c,36))
    col=f'<div style="display:flex; flex-direction:column; gap:14px; width:520px">{txt}</div>'
    if side=='r':   # disegno a destra
        pinned=figure(K,700,290,c); body=col
    else:           # disegno a sinistra, testo a destra
        pinned=figure(K,128,290,c)+f'<div style="position:absolute; left:1272px; top:290px; width:520px; display:flex; flex-direction:column; gap:14px">{txt}</div>'
        body=''
    sec(sid, head(GRP[sid],TIT[sid],c)+body, pinned=pinned, notes=notes)
GRP={'savoia':'2 · Arresto e occhio','gassa':'2 · Arresto e occhio','parlato':'3 · Legare','bozza':'3 · Legare','bitta':'4 · Dare volta',
     'galloccia':'4 · Dare volta','mezzi':'4 · Dare volta','piano':'5 · Unire e accorciare','bandiera':'5 · Unire e accorciare','margherita':'5 · Unire e accorciare'}

# ============ COPERTINA ============
cover(0,'I nodi marinari','Che cosa sono, a che cosa servono e come si fanno: dieci nodi e volte, passo per passo, con un disegno per ogni passaggio',
 'Appendice C al corso. I nodi della prova pratica (All. D al DM 323/2021: gassa d\'amante, parlato, bitta, bozza) e quelli dei quiz 2.2.1 e 1.4.4, ognuno in quattro passaggi disegnati.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice C · studio'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
IDX=[('1','Le parole e la scelta','Corrente, dormiente, doppino, volta; quale nodo per quale lavoro',SEA,'parole'),
     ('2','Arresto e occhio','Nodo Savoia e gassa d\'amante',CORAL,'savoia'),
     ('3','Legare a una draglia, a una cima','Nodo parlato e nodo di bozza',PURPLE,'parlato'),
     ('4','Dare volta','Bitta, galloccia, volta tonda e due mezzi colli',BLUE,'bitta'),
     ('5','Unire e accorciare','Nodo piano, nodo bandiera, nodo margherita',GREEN,'piano'),
     ('6','Cime e ripasso','Materiali e cura delle cime, due verifiche con i quiz ufficiali',NAVY,'cime')]
cards=''.join(f'<div style="display:flex; align-items:center; gap:22px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:18px 24px"><p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:44px">{n}</p><div style="flex:1; display:flex; flex-direction:column; gap:2px">{p(t,30,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div><p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(s)}</p></div>' for n,t,d,c,s in IDX)
sec('indice', head('Appendice C · I nodi marinari','Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:18px">{cards}</div>'
    +note('All\'esame pratico si fanno gassa d\'amante, parlato, volta di bitta e nodo di bozza: portate uno spezzone di cima.',CORAL,34),
 notes='Ogni nodo ha una slide: a sinistra o a destra che cos\'è e a che cosa serve, dall\'altra parte quattro disegni numerati con i passaggi. La freccia tratteggiata mostra dove va il capo nel passaggio successivo. Riferimenti: DM 10 agosto 2021 n. 323, All. D (esercitazioni pratiche: nodi gassa d\'amante, parlato, bitta, bozza); quiz 2.2.1-54…-59, -67, -70; 1.4.4-8, -18…-21; 2.3.1-21.')

# ============ LE PAROLE ============
tile=lambda t,d,c: f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:22px 22px 24px 22px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{squiggle(c,110)}{h3(t,30,c)}{p(d,24,BODY,400,1.35)}</div>'
WD=[('Corrente','Il capo libero, quello che si muove per fare il nodo.',CORAL),('Dormiente','La parte che resta ferma e che prende il tiro.',SEA),
    ('Doppino','La cima piegata a U, senza incrociarla.',PURPLE),('Volta','Un giro in cui la cima incrocia sé stessa: un\'asola.',BLUE),
    ('Volta tonda','Un giro completo attorno a un palo o a un anello, e mezzo in più.',GREEN),('Mezzo collo','Un giro attorno a un oggetto o al dormiente, chiuso passando sotto sé stesso.',CORAL),
    ('Dare volta','Fissare una cima a una bitta o a una galloccia.',SEA),('Mollare','Liberare la cima; «in bando» se resta lenta.',PURPLE)]
g=''.join(tile(*x) for x in WD)
sec('parole', head('1 · Le parole e la scelta','Le parole dei nodi',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{g}</div>'
    +note('Un buon nodo si fa in fretta, tiene sotto tiro e si scioglie senza fatica anche dopo aver lavorato.',CORAL,36),
 notes='Nei passaggi disegnati il corrente è il capo con la punta arrotondata, il dormiente esce dal bordo del disegno. A bordo si dice cima, non corda; la sagola è una cima di piccolo diametro (quiz 1.1.1-40).')

# ============ LA SCELTA ============
SC=[('Fermare un capo','Nodo Savoia','savoia',CORAL),('Un occhio che non scorre','Gassa d\'amante','gassa',CORAL),
    ('Legare a draglia o palo','Nodo parlato','parlato',PURPLE),('Prendere il tiro di una cima','Nodo di bozza','bozza',PURPLE),
    ('Ormeggiare a bordo','Volta di bitta, galloccia','bitta',BLUE),('Legare a palo, anello, gavitello','Volta tonda e due mezzi colli','mezzi',BLUE),
    ('Unire cime uguali','Nodo piano','piano',GREEN),('Unire cime diverse','Nodo bandiera','bandiera',GREEN),
    ('Accorciare una cima','Nodo margherita','margherita',GREEN)]
rows=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:10px solid {c}; border-radius:20px; padding:14px 20px">'
             f'<div style="flex:1; display:flex; flex-direction:column; gap:2px">{p(a,24,SOFT,700,1.25)}{p(b,30,INK,800,1.2)}</div>'
             f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(s)}</p></div>' for a,b,s,c in SC)
sec('scelta', head('1 · Le parole e la scelta','Quale nodo per quale lavoro',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px">{rows}</div>',
 notes='Il colore del bordo indica il gruppo dell\'indice. Per unire cime di diametro diverso non si usa il nodo piano ma il bandiera (quiz 2.2.1-56); il tornichetto non unisce cime (2.2.1-70).')

# ============ I NODI ============
knot_slide('savoia',CORAL,'Un nodo d\'arresto: fa un ingrossamento a forma di otto in fondo alla cima.',
 'In fondo a scotte e drizze, perché non si sfilino da bozzelli e passacavi.','Si scioglie facilmente anche dopo aver lavorato.',
 'Quiz 2.2.1-57: la funzione del Savoia è impedire che l\'estremità di un cavo si sfili da un passacavo (vero). Si chiama anche nodo a otto. Farlo fare a tutti in aula: volta, dietro al dormiente, dentro la volta dal davanti.','r')
knot_slide('gassa',CORAL,'Un occhio fisso che non scorre e non si stringe: di grande tenuta, si scioglie anche dopo un forte tiro.',
 'Ormeggio su bitta o anello, scotte alla bugna del fiocco, una cima attorno al corpo per recuperare una persona.','Non accorcia la cima e non si scioglie da sola.',
 'Quiz 1.4.4-20 (grande tenuta, adatto ai cavi d\'ormeggio), 2.2.1-54 (non tende a sciogliersi: falso), -55 (non serve ad accorciare: falso), 2.3.1-21 (le scotte alla bugna si fissano con la gassa, non con il parlato doppio). È uno dei nodi della prova pratica (All. D). Filastrocca: il coniglio esce dal buco, gira attorno all\'albero e rientra nel buco.','l')
knot_slide('parlato',PURPLE,'Due giri attorno a una draglia o a un palo; i capi escono in versi opposti da sotto la diagonale.',
 'Per legare i parabordi a draglie e pulpiti e per fissare una cima a un palo.','Si regola in un attimo; sotto strappi può scorrere.',
 'Quiz 1.4.4-21 e 2.2.1-58: il parlato è utile per fissare i parabordi a pulpiti e draglie. È nella prova pratica (All. D). Si chiama anche nodo barcaiolo.','r')
knot_slide('bozza',PURPLE,'Un parlato con un giro in più dal lato del tiro: morde e non scorre lungo la cima tirata.',
 'Prendere il carico di una cima in tensione, per esempio per liberare una scotta incattivita sul winch.','Nella prova pratica: gassa, parlato, bitta e bozza.',
 'Il nodo di bozza è nella prova pratica (All. D al DM 323/2021). I due giri vanno dal lato verso cui si tira e passano sopra il dormiente; poi si chiude come un parlato dall\'altra parte.','l')
knot_slide('bitta',BLUE,'La volta di bitta: un giro completo sulla prima bitta, poi giri a otto tra le due.',
 'Dare volta alle cime d\'ormeggio a bordo; in banchina si infila una gassa sulla bitta oppure si passa un doppino.','Il doppino si molla da bordo, senza scendere in banchina.',
 'Quiz 1.1.1-18 (la bitta: bassa colonnetta con la testa a fungo), 1.4.4-8 (il doppino gira attorno alla bitta in banchina e torna a bordo, dove si fissano i due capi). La volta di bitta è nella prova pratica (All. D).','r')
knot_slide('galloccia',BLUE,'Volta tonda alla base, giri a otto sopra i corni e chiusura con una volta mezza.',
 'Dare volta a drizze, scotte e cime d\'ormeggio sulla galloccia.','Pochi giri: la cima deve potersi mollare subito.',
 'Quiz 1.1.1-17: la galloccia è un appiglio per rinviare o dare volta a una cima. La cima arriva dalla parte del corno lontano; la volta mezza finale si fa rovesciando il giro, così il capo passa sotto.','l')
knot_slide('mezzi',BLUE,'Una volta tonda attorno al palo o all\'anello, poi due mezzi colli sul dormiente.',
 'Ormeggiare a un palo, a un anello o a un gavitello; legare una cima a un oggetto.','La volta tonda regge il tiro, i mezzi colli lo fermano.',
 'I due mezzi colli, girati nello stesso verso, formano un parlato attorno al dormiente. Con il primo mezzo collo infilato sotto la volta tonda diventa il nodo d\'ancorotto, per legare la cima alla cicala dell\'ancora. Quiz 1.4.4-33: al gavitello ci si lega alla cima sotto il gavitello.','r')
knot_slide('piano',GREEN,'Due mezzi nodi incrociati in senso opposto: i due doppini si abbracciano.',
 'Unire due cime dello stesso diametro; chiudere i matafioni dei terzaroli.','Diametri diversi? Serve il nodo bandiera.',
 'Quiz 2.2.1-56: non è opportuno usare il nodo piano per unire cavi di diametro diverso (falso). Regola: sinistra sopra destra, poi destra sopra sinistra. Se si ripete lo stesso incrocio viene il nodo vaccaio, che scivola.','l')
knot_slide('bandiera',GREEN,'La cima sottile avvolge il doppino della grossa e passa sotto sé stessa.',
 'Unire due cime di diametro o materiale diverso; legare la bandiera alla sua drizza.','È la stessa struttura della gassa d\'amante.',
 'Il doppino si fa sempre nella cima più grossa. I due capi corti devono uscire dalla stessa parte del nodo. Collega al quiz 2.2.1-56 (per diametri diversi non il nodo piano).','r')
knot_slide('margherita',GREEN,'La cima piegata a Z e bloccata alle due estremità da un giro attorno al doppino.',
 'Accorciare una cima senza tagliarla, o escludere un tratto rovinato.','Tiene solo finché la cima resta in tiro.',
 'Quiz 2.2.1-59: il nodo margherita si usa per accorciare una cima (vero). Il tratto centrale della Z non lavora: se è rovinato, la cima tiene lo stesso.','l')

# ============ LE CIME ============
CM=[('Poliestere','Robusto e poco elastico: cime d\'ormeggio e manovre.',CORAL),('Polipropilene','Galleggia: solo per le sagole di salvataggio.',SEA),
    ('Sagola','Una cima di piccolo diametro.',PURPLE),('Acciaio','Sartie e stralli: cavi d\'acciaio o di fibra.',BLUE),
    ('Impiombatura','Intreccio dei trefoli: unisce due cavi o fa un occhio fisso.',GREEN),('Dugliare','Raccogliere la cima in spire ordinate, pronta a filare.',CORAL),
    ('Cima in chiaro','Senza nodi e senza volte: pronta per la manovra.',SEA),('Acqua dolce','A fine stagione, un lavaggio toglie il sale e l\'usura.',PURPLE)]
g=''.join(tile(*x) for x in CM)
sec('cime', head('6 · Cime e ripasso','Le cime: materiali e cura',NAVY)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{g}</div>',
 notes='Quiz 1.4.4-19 (poliestere per le cime d\'ormeggio), 1.4.4-18 e 2.2.1-38 (polipropilene solo per sagole galleggianti di salvataggio), 1.1.1-40 (sagola), 2.2.1-67 (impiombatura), 2.2.1-69 (sartie in acciaio o fibra).')

# ============ VERIFICHE ============
Q1=['2.2.1-57','1.4.4-20','2.2.1-55','1.4.4-21']; Q2=['2.2.1-56','2.2.1-59','2.3.1-21','1.4.4-8']
quiz_slide('quiz1','Verifica 1 · Arresto, occhio, parlato',Q1,False)
quiz_slide('quiz1r','Verifica 1 · Le risposte',Q1,True)
quiz_slide('quiz2','Verifica 2 · Unire, accorciare, ormeggiare',Q2,False)
quiz_slide('quiz2r','Verifica 2 · Le risposte',Q2,True)

closing(['Il Savoia ferma il capo in fondo a scotte e drizze: non si sfila dal passacavo',
         'La gassa d\'amante fa un occhio che non scorre e si scioglie anche dopo un forte tiro',
         'Parlato per i parabordi, bozza per prendere il tiro di una cima: nodi della prova pratica',
         'Bitta e galloccia: volta tonda, giri a otto e niente nodi strozzati',
         'Nodo piano per cime uguali, bandiera per cime diverse, margherita per accorciare'],
 'Ogni nodo si impara con le mani: una cima in tasca e dieci minuti al giorno','Appendice C · I nodi marinari')

write_deck(OUT,'Appendice C · I nodi marinari',ORDER,
 {"s1":{"description":"Copertina e indice","start":"cover"},"s2":{"description":"Le parole dei nodi e quale nodo scegliere","start":"parole"},
  "s3":{"description":"Arresto e occhio: Savoia e gassa d'amante","start":"savoia"},"s4":{"description":"Parlato e nodo di bozza","start":"parlato"},
  "s5":{"description":"Dare volta: bitta, galloccia, volta tonda e due mezzi colli","start":"bitta"},
  "s6":{"description":"Unire e accorciare: piano, bandiera, margherita","start":"piano"},"s7":{"description":"Le cime e le verifiche","start":"cime"}})
