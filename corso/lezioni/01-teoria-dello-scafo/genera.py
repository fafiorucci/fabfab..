import json, math, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SP=os.path.dirname(os.path.abspath(__file__))
OUT=SP+'/lez01/project'
Q={x['p']:x for x in json.load(open(SP+'/rotta-giusta/site/dati/quiz.json'))}

from template import *
RED='#D63B3B'; GREEN_S='#2E9E5B'; WATER='#12A4B5'
TITLE='Lezione 01 · Teoria dello scafo'


slides=[]
def sec(id, inner, notes='', dark=False, gap=32, pinned=''):
    n=len(slides)+1; bg = NAVY if dark else PAPER; col = PAPER if dark else BODY
    slides.append((id, f'<section id="{id}" data-transition="fade" style="background:{bg}; color:{col}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">\n{backdrop(dark,n)}\n{inner}\n{pinned}{footer(n,dark)}\n<aside>{notes}</aside>\n</section>\n'))
def lab(x,y,w,t,color=INK,size=24,weight=600,align='left',bg=None):
    b=f' background:{bg}; padding:2px 10px; border-radius:6px;' if bg else ''
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-size:{size}px; line-height:1.3; font-weight:{weight}; color:{color}; text-align:{align};{b}">{t}</p>'
def svgp(x,y,w,h,body,alt,pan=True):
    if pan: body=panel(w,h,body,wind=False)
    return f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px">{body}</svg>'
def svgi(w,h,body,alt,dw=None,dh=None):
    return f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="width:{dw or w}px; height:{dh or h}px">{body}</svg>'
def arrow(x1,y1,x2,y2,c=NAVY,w=3,hs=13):
    a=math.atan2(y2-y1,x2-x1); bx=x2-hs*math.cos(a); by=y2-hs*math.sin(a)
    p1=(bx+hs*0.5*math.sin(a), by-hs*0.5*math.cos(a)); p2=(bx-hs*0.5*math.sin(a), by+hs*0.5*math.cos(a))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>')
def dim(x1,y1,x2,y2,c=NAVY):
    return arrow((x1+x2)/2,(y1+y2)/2,x1,y1,c,2.5,12)+arrow((x1+x2)/2,(y1+y2)/2,x2,y2,c,2.5,12)
def dash(x1,y1,x2,y2,c=SOFT):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="2" stroke-dasharray="8 6"/>'
def line(x1,y1,x2,y2,c=NAVY,w=2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
def term(t,d): return f'<div style="display:flex; flex-direction:column; gap:4px">{p(t,28,INK,700,1.3)}{p(d,26,BODY)}</div>'

ICON_T={'La lezione di oggi':'lifebuoy','Natanti, imbarcazioni e navi da diporto':'hull','Opera viva, opera morta e lunghezza':'hull','Baglio, bordo libero e pescaggio':'hull',
 'Prua, poppa, dritta e sinistra':'compass','Chiglia, ordinate, paratie e sovrastrutture':'hull','Sentina, pagliolo e boccaporto':'hull','La ferramenta di bordo':'anchor',
 'Passascafo, prese a mare e zinchi':'propeller','Dislocante, planante, semiplanante':'hull','Dislocamento, stazza e portata':'lifebuoy','Lo scafo in legno':'hull','Antivegetativa, zinchi e prese a mare':'propeller','Rollio, beccheggio e accostata':'compass',
 'Baricentro, centro di carena e metacentro':'sail','I flaps':'hull','Il trim del fuoribordo':'propeller'}
def head(e,t,c=None):
    return header(e,t,'quiz' if t.startswith(('Quiz','Verifica')) else ICON_T.get(t,'hull'),c)
# ---------- barca di profilo ----------
def P(x0,wl,L,x,y): return (x0+x*L, wl+y*L)
def fmt(pt): return f'{pt[0]:.1f} {pt[1]:.1f}'
def profile(x0,wl,L,hull=BOAT,uw=ACC,st=NAVY,sw=3,fly=False,deck2=False,sil=False):
    f=lambda x,y: fmt(P(x0,wl,L,x,y))
    hullp=f'M{f(0,-0.09)} L{f(1.0,-0.13)} Q{f(1.01,-0.05)} {f(0.9,0.05)} L{f(0.12,0.06)} L{f(0.02,0.03)} Z'
    uwp=f'M{f(0.015,0)} L{f(0.943,0)} Q{f(0.924,0.028)} {f(0.9,0.05)} L{f(0.12,0.06)} L{f(0.02,0.03)} Z'
    sup=f'M{f(0.30,-0.102)} L{f(0.70,-0.118)} L{f(0.64,-0.19)} L{f(0.36,-0.19)} Z'
    if sil:
        s=f'<path d="{hullp}" fill="{st}"/><path d="{sup}" fill="{st}"/>'
        if deck2: s+=f'<path d="M{f(0.40,-0.19)} L{f(0.60,-0.19)} L{f(0.57,-0.25)} L{f(0.44,-0.25)} Z" fill="{st}"/>'
        return s
    s=f'<path d="{hullp}" fill="{hull}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    s+=f'<path d="{uwp}" fill="{uw}" fill-opacity="0.95"/>'+f'<path d="M{f(0.02,-0.012)} L{f(0.955,-0.012)}" stroke="{BLUE}" stroke-width="{sw+4}"/>'
    s+=f'<path d="{hullp}" fill="none" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    s+=f'<path d="{sup}" fill="{hull}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    for i in range(4):
        a=0.40+i*0.065; s+=f'<path d="M{f(a,-0.165)} L{f(a+0.045,-0.165)} L{f(a+0.045,-0.135)} L{f(a,-0.135)} Z" fill="{st}" fill-opacity="0.8"/>'
    if fly:
        s+=f'<path d="M{f(0.40,-0.19)} L{f(0.58,-0.19)} L{f(0.58,-0.205)} L{f(0.40,-0.205)} Z" fill="{hull}" stroke="{st}" stroke-width="{sw}"/>'
        for a in (0.41,0.47,0.53,0.575): s+=line(*P(x0,wl,L,a,-0.205),*P(x0,wl,L,a,-0.235),st,2)
        s+=line(*P(x0,wl,L,0.41,-0.235),*P(x0,wl,L,0.575,-0.235),st,2)
    return s
def water(w,y0,y1,op=0.12):
    return f'<rect x="0" y="{y0}" width="{w}" height="{y1-y0}" fill="{WATER}" fill-opacity="{op}"/>'+line(0,y0,w,y0,TEAL,3)

# ---------- sezione trasversale ----------
def section_hull(cx=330, deck=170, half=230, keel=450, fin=540, wl=310, uw=True, cid='c'):
    xl,xr=cx-half,cx+half
    hp=f'M{xl} {deck} C {xl} {deck+160}, {cx-140} {keel-30}, {cx} {keel} C {cx+140} {keel-30}, {xr} {deck+160}, {xr} {deck} Z'
    s=f'<defs><clipPath id="{cid}"><rect x="0" y="{wl}" width="2000" height="1000"/></clipPath></defs>'
    s+=f'<path d="{hp}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
    if uw: s+=f'<path d="{hp}" fill="{ACC}" fill-opacity="0.85" clip-path="url(#{cid})"/>'
    s+=f'<path d="{hp}" fill="none" stroke="{NAVY}" stroke-width="4"/>'
    s+=f'<path d="M{cx-12} {keel-2} L{cx-8} {fin} L{cx+8} {fin} L{cx+12} {keel-2} Z" fill="{NAVY}"/>'
    return s

# =============== 1 COVER ===============
cover_boat = svgp(1000,470,792,450, sea_scene(792,450),pan=False,alt='Illustrazione: barca a vela e motoscafo sul mare con sole, nuvole e gabbiani')
slides.append(('cover', f'''<section id="cover" data-transition="fade" style="background:{NAVY}; color:{PAPER}; font-family:{B}; padding:128px; display:flex; flex-direction:column; justify-content:space-between">
{backdrop(True)}
{lockup(True,112)}
<div style="display:flex; flex-direction:column; gap:24px; width:820px">
<p style="font-family:{HAND}; font-size:48px; font-weight:700; line-height:1.1; color:{DACC}">Lezione 01 · 2 ore</p>
<h1 style="font-family:{H}; font-size:112px; font-weight:600; line-height:1.1; color:{PAPER}">Teoria dello scafo</h1>{wave(DACC,330)}
<p style="font-size:36px; line-height:1.4; color:{DSOFT}">Classificazione, nomenclatura, carene, assetto e stabilità</p>
</div>
<p style="font-size:24px; color:{DSOFT}">Patente nautica Vela/Motore senza limiti dalla costa</p>
{cover_boat}
<aside>Benvenuto al corso. Presentarsi, spiegare come è organizzato l'esame e che questa lezione copre la Teoria dello scafo (All. A al DM 323/2021, punti 1a e 1b).</aside>
</section>
'''))

# =============== 2 AGENDA ===============
blocks=[('0:00','15′','Classificazione e dimensioni',ACC),('0:15','30′','Pesi, carene e protezione · quiz 1',ACC),('0:45','30′','Parti, struttura e coperta · quiz 2',ACC),('1:15','25′','Assi, stabilità e assetto · quiz 3 e 4',ACC),('1:40','20′','Verifica finale',TEAL)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:8px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:700; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.35; font-weight:600; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:96px; font-weight:700; line-height:1.1; color:{INK}">1 / 20</p>'+p('domanda di Teoria dello scafo nella scheda del quiz base',26,INK,600)+p('125 quiz ufficiali sul tema: 75 di nomenclatura dello scafo, 50 su elica, timone e stabilità (elica e timone nella lezione 2).',24))
left=card(tag('Dopo questa lezione sai','#1F6F78')+'<ul style="font-size:26px; line-height:1.4; color:#3A4652; display:flex; flex-direction:column; gap:10px"><li>riconoscere natanti, imbarcazioni e navi</li><li>chiamare per nome ogni parte dello scafo</li><li>distinguere le carene e i movimenti della barca</li><li>spiegare stabilità, flaps e trim</li></ul>',TEALCARD,flex=1.4)
sec('agenda', head('Lezione 01 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:16px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Ordine degli argomenti come nel capitolo 1 del manuale Il Frangente (Teoria della nave): classificazione e caratteristiche, parti principali, attrezzatura di coperta, struttura in legno, assi, assetto, stabilità. Quattro verifiche intermedie da 3 quiz e una finale da 6: tutti quiz ufficiali del DD 131/2022, con la risposta esatta nella slide successiva.')

# =============== 3 CLASSIFICAZIONE ===============
def clscard(tagt, name, meters, Lpx, text, deck2=False, col=NAVY):
    wl=112; x0=(500-Lpx)/2
    body=f'<rect x="0" y="{wl}" width="500" height="38" fill="{WATER}" fill-opacity="0.12"/>'+line(0,wl,500,wl,TEAL,2)+profile(x0,wl,Lpx,sil=True,st=col,deck2=deck2)
    body+=line(x0,142,x0+Lpx,142,SOFT,2)+line(x0,134,x0,150,SOFT,2)+line(x0+Lpx,134,x0+Lpx,150,SOFT,2)
    return card(tag(tagt)+svgi(500,150,body,f'Sagoma di {name.lower()} di {meters} metri, in scala con le altre',dw=474,dh=142)+p(f'Esempio: {meters} m',24,SOFT)+h3(name)+p(text,24))
k=13
cards=clscard('fino a 10 m','Natante',8,8*k,'Non iscritto nei registri. Se iscritto a richiesta, segue le regole delle imbarcazioni.',col=CORAL)+clscard('oltre 10 m e fino a 24 m','Imbarcazione',18,18*k,'Iscritta nei registri delle imbarcazioni da diporto.',col=SEA)+clscard('oltre 24 m','Nave da diporto',34,34*k,'Iscritta nei registri delle navi da diporto.',True,col=PURPLE)
sec('classificazione', head('Classificazione · D.Lgs. 171/2005, art. 3','Natanti, imbarcazioni e navi da diporto')+f'<div style="display:flex; gap:24px">{cards}</div>'+p('Conta la <b>lunghezza dello scafo</b>. Per la forma: monocarena, catamarano (due scafi), battello pneumatico e RIB (chiglia rigida e tubolari).',26,BODY),
 notes='Codice della nautica, art. 3: unità da diporto con scafo fino a 10 m = natante; oltre 10 e fino a 24 m = imbarcazione; oltre 24 m = nave da diporto. Lunghezza misurata secondo le norme armonizzate (EN ISO 8666). Quiz: un\'unità di 9,90 m o di 7 m può essere iscritta, e allora subisce il regime giuridico delle imbarcazioni. Un natante è un\'unità non iscritta. Le sagome sono in scala tra loro.')

# =============== 4 PROFILO: opera viva/morta, LFT ===============
X,Y=128,300; W,Hh=1664,590
x0,wl,L=170,350,1280
b=water(W,wl,Hh,0.10)+profile(x0,wl,L,fly=True)
xs,xb=P(x0,wl,L,0,-0.09)[0], P(x0,wl,L,1.005,-0.1)[0]
b+=dash(xs,22,xs,wl-110)+dash(xb,22,xb,wl-170)+dim(xs,22,xb,22)
b+=arrow(330,150,400,240)+arrow(640,495,640,wl+45)+arrow(1560,wl+36,1560,wl+6,TEAL)
lbls=lab(X+640,Y+4,340,'Lunghezza fuori tutto',INK,24,700,'center',PAPER)+lab(X+130,Y+80,300,'Opera morta',INK,26,700)+lab(X+130,Y+112,300,'parte emersa',BODY,24,400)
lbls+=lab(X+360,Y+500,420,'Opera viva o carena',INK,26,700)+lab(X+360,Y+534,420,'parte immersa',BODY,24,400)
lbls+=lab(X+1440,Y+wl+40,220,'Linea di galleggiamento',TEAL,24,700)+lab(X+10,Y+wl-60,140,'Poppa',SOFT,24,700)+lab(X+1480,Y+wl-160,160,'Prua',SOFT,24,700)
sec('profilo', head('Nomenclatura · lo scafo di profilo','Opera viva, opera morta e lunghezza'), pinned=svgp(X,Y,W,Hh,b,'Profilo di un motoscafo: in rosso la carena immersa sotto la linea di galleggiamento, sopra l\'opera morta; quota della lunghezza fuori tutto')+lbls,
 notes='Scafo: la struttura che costituisce il guscio dell\'unità. Linea di galleggiamento: divide l\'opera viva (parte immersa, detta anche carena) dall\'opera morta (parte emersa). Lunghezza fuori tutto (LFT): la massima lunghezza, misurata tra le estremità prodiera e poppiera. Quiz 1.1.1-15, -16, -28, -37, -53 e 1.1.1-1.')

# =============== 5 SEZIONE: baglio, bordo libero, pescaggio ===============
X,Y,W,Hh=1000,290,792,620
b=f'<rect x="0" y="310" width="{W}" height="{Hh-310}" fill="{WATER}" fill-opacity="0.10"/>'+section_hull(cid='s5')+line(0,310,W,310,TEAL,3)
b+=f'<rect x="200" y="110" width="260" height="60" rx="10" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b+=dash(100,165,100,50)+dash(560,165,560,50)+dim(100,60,560,60)
b+=dash(565,170,660,170)+dash(345,540,660,540)+dim(640,170,640,310,INK)+dim(640,310,640,540,INK)
lbls=lab(X+180,Y+8,300,'Baglio massimo',INK,24,700,'center',PAPER)+lab(X+658,Y+205,134,'Bordo libero',INK,24,700)+lab(X+658,Y+400,134,'Pescaggio',INK,24,700)
txt=term('Baglio massimo','La larghezza massima dello scafo.')+term('Bordo libero','La distanza verticale tra la coperta e la linea di galleggiamento.')+term('Pescaggio','La distanza verticale tra la linea di galleggiamento e il punto più basso dello scafo.')+term('Sezione maestra','La sezione trasversale centrale, di solito la più larga. La sua ordinata è l\'ordinata maestra.')
sec('sezione', head('Nomenclatura · lo scafo in sezione','Baglio, bordo libero e pescaggio')+f'<div style="display:flex; flex-direction:column; gap:24px; width:800px">{txt}</div>', pinned=svgp(X,Y,W,Hh,b,'Sezione trasversale dello scafo con le quote di baglio massimo, bordo libero e pescaggio')+lbls,
 notes='Quiz 1.1.1-45 (baglio massimo = larghezza massima), 1.1.1-47 (bordo libero), 1.1.1-22 (pescaggio: dalla linea di galleggiamento al punto inferiore estremo dello scafo, non fino al fondo del mare), 1.1.1-48 e -23 (sezione e ordinata maestra). Caricando la barca aumenta il pescaggio e diminuisce il bordo libero.')

# =============== 6 PIANTA: orientamento ===============
X,Y,W,Hh=128,290,1664,610
hull=f'M330 165 L1080 150 Q1330 170 1450 305 Q1330 440 1080 460 L330 445 Q312 305 330 165 Z'
b=f'<path d="{hull}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M330 165 L1080 150 Q1330 170 1450 305" fill="none" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>'
b+=f'<path d="M330 445 L1080 460 Q1330 440 1450 305" fill="none" stroke="{GREEN_S}" stroke-width="10" stroke-linecap="round"/>'
b+=f'<rect x="620" y="235" width="460" height="140" rx="40" fill="{CARD}" stroke="{NAVY}" stroke-width="3"/>'+dash(290,305,1500,305)
for (x1,y1,x2,y2) in [(1420,60,1310,182),(1420,550,1310,428),(820,50,820,146),(820,560,820,464),(285,72,352,162),(285,545,352,448),(250,305,318,305)]:
    b+=arrow(x1,y1,x2,y2,INK,3)
lbls=lab(X+1430,Y+30,230,'Mascone di sinistra',RED,24,700)+lab(X+1430,Y+540,230,'Mascone di dritta',GREEN_S,24,700)
lbls+=lab(X+840,Y+20,300,'Traverso di sinistra',RED,24,700)+lab(X+840,Y+556,300,'Traverso di dritta',GREEN_S,24,700)
lbls+=lab(X+10,Y+20,260,'Giardinetto di sinistra',RED,24,700)+lab(X+10,Y+556,260,'Giardinetto di dritta',GREEN_S,24,700)
lbls+=lab(X+20,Y+240,220,'Specchio di poppa',INK,24,700,'right')+lab(X+1480,Y+286,170,'PRUA',INK,26,700)
lbls+=lab(X+380,Y+180,400,'Murata di sinistra',RED,24,700)+lab(X+380,Y+396,400,'Murata di dritta',GREEN_S,24,700)+lab(X+640,Y+268,420,'asse longitudinale',SOFT,24,700,'center')
sec('orientamento', head('Orientarsi a bordo · vista dall\'alto','Prua, poppa, dritta e sinistra'), pinned=svgp(X,Y,W,Hh,b,'Pianta di uno scafo con prua a destra: murata di sinistra in rosso, murata di dritta in verde, frecce su masconi, traversi e giardinetti')+lbls,
 notes='Guardando verso prua: dritta a destra, sinistra a sinistra. Colori come i fanali: rosso a sinistra, verde a dritta. Masconi: ai lati della prua; giardinetti: ai lati della poppa; traverso: a metà nave, perpendicolare all\'asse longitudinale. Murate: la parte esterna e laterale dello scafo (opera morta) da prua a poppa. Specchio di poppa: la porzione esterna e superiore della poppa. Nei quiz con figura (1.1.1-20, -21, -24, -25, -58, -60) la freccia indica proprio questi punti.')

# =============== QUIZ ===============
def quiz_slide(id_, title, ps, reveal):
    cards=''
    for i,pp in enumerate(ps):
        x=Q[pp]; opts=''
        for j,o in enumerate(x['r']):
            o=o.strip().rstrip(';')
            if reveal and j==x['x']:
                opts+=f'<div style="display:flex; gap:10px; align-items:start; background:{TEALCARD}; padding:10px 12px; border-radius:10px; border:2px solid {TEAL}"><x-icon name="CheckCircle" style="color:{TEAL}; width:30px; height:30px"></x-icon><p style="font-size:24px; line-height:1.35; font-weight:700; color:{INK}">{"abc"[j]}) {o}</p></div>'
            else:
                c = SOFT if reveal else BODY
                opts+=f'<p style="font-size:24px; line-height:1.35; color:{c}; padding:10px 12px">{"abc"[j]}) {o}</p>'
        foot = f'<p style="font-size:24px; font-weight:700; color:{TEAL}">Risposta esatta: {"abc"[x["x"]]}</p>' if reveal else ''
        cards+=card(f'<p style="font-size:24px; font-weight:700; color:{ACC}">Domanda {i+1} · quiz {pp}</p><p style="font-size:26px; line-height:1.35; font-weight:700; color:{INK}">{x["d"].strip()}</p><div style="display:flex; flex-direction:column; gap:6px">{opts}</div>{foot}', CARD if not reveal else '#FBF9F4', 28, 14)
    e = 'Verifica · risposte esatte' if reveal else 'Verifica · quiz ufficiali DD 131/2022'
    notes = ('Risposte: ' + '; '.join(f'{pp} → {"abc"[Q[pp]["x"]]}) {Q[pp]["r"][Q[pp]["x"]].strip()}' for pp in ps)) if reveal else 'Leggere le domande, lasciare un minuto per rispondere, poi passare alla slide con le risposte esatte.'
    sec(id_, head(e, title, TEAL if reveal else ACC)+f'<div style="display:flex; gap:24px; align-items:stretch">{cards}</div>', notes=notes)



# =============== 7 STRUTTURA ===============
X,Y,W,Hh=128,290,1664,610
x0,wl,L=200,430,1250
f=lambda x,y: P(x0,wl,L,x,y)
b=water(W,wl,Hh,0.08)+profile(x0,wl,L,fly=True)
def sheer(x): return -0.09-0.04*x
def bottom(x): return 0.06-0.01*(x-0.12)/0.78 if x>=0.12 else 0.03+0.03*(x-0.02)/0.10
for xx in [0.1,0.18,0.26,0.34,0.42,0.58,0.66,0.82]:
    b+=line(*f(xx,sheer(xx)+0.004),*f(xx,bottom(xx)-0.004),NAVY,1.5)
b+=line(*f(0.5,sheer(0.5)+0.004),*f(0.5,bottom(0.5)-0.004),'#E9A07F',9)
for xx in (0.30,0.75): b+=line(*f(xx,sheer(xx)+0.004),*f(xx,bottom(xx)-0.004),NAVY,8)
b+=f'<path d="M{fmt(f(0.12,0.056))} L{fmt(f(0.9,0.047))}" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
b+=f'<path d="M{fmt(f(0,-0.09))} L{fmt(f(1.0,-0.13))}" stroke="{TEAL}" stroke-width="6"/>'
tg=[((0.18,-0.097),(330,55),'Ponte di coperta'),((0.49,-0.235),(820,48),'Flying bridge'),((0.66,-0.16),(1110,60),'Tuga'),((0.012,-0.03),(185,300),'Specchio di poppa'),
    ((0.18,0.02),(420,560),'Ordinate'),((0.40,0.055),(640,560),'Chiglia'),((0.5,0.02),(880,560),'Ordinata maestra'),((0.75,0.02),(1200,560),'Paratie')]
for (pt,(lx,ly),_) in tg: b+=arrow(lx,ly,*f(*pt),INK,2.5)
lbls=lab(X+220,Y+10,240,'Ponte di coperta',INK,24,700)+lab(X+700,Y+4,260,'Flying bridge',INK,24,700)+lab(X+1060,Y+16,160,'Tuga',INK,24,700)+lab(X+0,Y+230,180,'Specchio di poppa',INK,24,700,'right')
lbls+=lab(X+360,Y+562,160,'Ordinate',INK,24,700)+lab(X+590,Y+562,140,'Chiglia',INK,24,700)+lab(X+780,Y+562,260,'Ordinata maestra',ACC,24,700)+lab(X+1150,Y+562,200,'Paratie',INK,24,700)
sec('struttura', head('Nomenclatura · la struttura','Chiglia, ordinate, paratie e sovrastrutture'), pinned=svgp(X,Y,W,Hh,b,'Spaccato longitudinale di uno scafo: chiglia sul fondo, ordinate verticali, ordinata maestra evidenziata al centro, due paratie, ponte di coperta, tuga e flying bridge')+lbls,
 notes='Chiglia: la trave longitudinale sul fondo, spina dorsale dello scafo. Ordinate: le costole trasversali; l\'ordinata maestra corrisponde alla sezione maestra. Paratie: strutture verticali che suddividono lo scafo in senso trasversale (quiz 1.1.1-13, -36). Ponte di coperta: il ponte continuo che chiude superiormente lo scafo. Sovrastruttura: ciò che si eleva sopra il ponte di coperta; la tuga è la sovrastruttura abitabile che non occupa tutta la larghezza. Flying bridge (fly): ponte superiore delle unità a motore, con la seconda timoneria. Dritto di poppa: la parte strutturale a cui si incardina il timone esterno; lo specchio di poppa è la parte della poppa sopra il dritto. Losca: l\'apertura nella poppa da cui passa l\'asse del timone.')


# =============== SCAFO IN LEGNO ===============
X,Y,W,Hh=128,290,792,620
WOOD='#9C6B3F'; WOOD2='#6E4A2A'
hp='M100 170 C 100 330, 190 420, 330 450 C 470 420, 560 330, 560 170'
b=f'<path d="{hp} Z" fill="{BOAT}"/><path d="{hp}" fill="none" stroke="{WOOD}" stroke-width="18" stroke-dasharray="46 5"/>'
b+=f'<path d="M122 176 C 122 318, 205 400, 330 428 C 455 400, 538 318, 538 176" fill="none" stroke="{WOOD2}" stroke-width="10"/>'
b+=f'<path d="M232 398 L428 398 L400 432 L260 432 Z" fill="{WOOD2}"/><rect x="306" y="440" width="48" height="52" rx="4" fill="{WOOD2}"/>'
b+=f'<rect x="96" y="176" width="468" height="16" fill="{WOOD2}"/>'+''.join(f'<rect x="{96+i*52}" y="160" width="48" height="14" fill="{WOOD}"/>' for i in range(9))
for (lx,ly,tx,ty) in [(610,40,450,165),(610,150,548,185),(610,270,556,262),(610,370,520,330),(610,470,420,414),(610,560,356,466)]: b+=arrow(lx,ly,tx,ty,INK,2.5)
lbls=lab(X+615,Y+22,177,'Ponte',INK,24,700)+lab(X+615,Y+132,177,'Bagli',INK,24,700)+lab(X+615,Y+252,177,'Fasciame',INK,24,700)+lab(X+615,Y+352,177,'Ordinate',INK,24,700)+lab(X+615,Y+452,177,'Madieri',INK,24,700)+lab(X+615,Y+542,177,'Chiglia',INK,24,700)
txt=term('Chiglia','La trave longitudinale sul fondo: prosegue a prua nella <b>ruota di prua</b> e a poppa nel <b>dritto di poppa</b>.')+term('Ordinate e madieri','Le costole trasversali dello scafo; i madieri le collegano alla chiglia sul fondo.')+term('Bagli','Le travi trasversali che reggono il ponte di coperta.')+term('Fasciame','Il rivestimento esterno di tavole fissato sulle ordinate.')
sec('legno', head('Nomenclatura · la costruzione','Lo scafo in legno')+f'<div style="position:absolute; left:968px; top:290px; width:824px; display:flex; flex-direction:column; gap:26px">{txt}</div>', pinned=svgp(X,Y,W,Hh,b,'Sezione di uno scafo in legno: chiglia sul fondo, madieri, ordinate, fasciame esterno, bagli e ponte di coperta')+lbls,
 notes='Nel manuale Il Frangente (cap. 1, «struttura dello scafo in legno») la costruzione tradizionale spiega i nomi usati anche per gli scafi moderni in vetroresina: chiglia, ordinate, madieri, bagli, fasciame, ruota di prua e dritto di poppa.')
X,Y,W,Hh=1000,290,792,620

# =============== 8 SOTTO COPERTA ===============
X,Y,W,Hh=1000,290,792,620
b=section_hull(uw=False,cid='s8')+line(0,310,W,310,TEAL,2)
b+=f'<path d="M222 402 Q330 470 438 402 Z" fill="{TEAL}" fill-opacity="0.35"/>'
b+=line(212,395,448,395,NAVY,10)
b+=f'<rect x="200" y="100" width="260" height="70" rx="10" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<rect x="290" y="84" width="80" height="16" fill="{NAVY}"/>'
for xx in (104,556): b+=line(xx,170,xx,95,NAVY,5)+f'<circle cx="{xx}" cy="100" r="7" fill="{ACC}"/><circle cx="{xx}" cy="135" r="7" fill="{ACC}"/>'
for (lx,ly,tx,ty) in [(610,50,375,90),(610,125,562,118),(610,200,548,172),(610,350,445,392),(610,460,380,425)]: b+=arrow(lx,ly,tx,ty,INK,2.5)
lbls=lab(X+615,Y+32,177,'Boccaporto',INK,24,700)+lab(X+615,Y+96,177,'Candelieri e draglie',INK,24,700)+lab(X+615,Y+184,177,'Coperta',INK,24,700)+lab(X+615,Y+334,177,'Pagliolo',INK,24,700)+lab(X+615,Y+444,177,'Sentina',TEAL,24,700)
txt=term('Sentina','Lo spazio tra il fondo interno dello scafo e il pagliolo: raccoglie acque sporche e residui liquidi.')+term('Pagliolo (pagliolato)','Il piano calpestabile e amovibile sotto coperta, il più basso.')+term('Gavoni','I vani ripostiglio di prua e di poppa.')+term('Locale macchine','Dove stanno i motori e gran parte degli impianti ausiliari.')+term('Boccaporto','L\'apertura nel ponte di coperta per il passaggio di persone e cose.')
sec('sottocoperta', head('Nomenclatura · sotto coperta','Sentina, pagliolo e boccaporto')+f'<div style="display:flex; flex-direction:column; gap:18px; width:820px">{txt}</div>', pinned=svgp(X,Y,W,Hh,b,'Sezione dello scafo: in basso la sentina con acqua, sopra il pagliolo, la tuga con il boccaporto e ai lati i candelieri con le draglie')+lbls,
 notes='Quiz 1.1.1-3 e -27 (sentina), -29, -46 e -51 (pagliolo, pagliolato), -19 (gavone), -9 (locale macchine), -42 (boccaporto). Le draglie sono i cavi tesi tra i candelieri: nel disegno in sezione se ne vedono le teste (punti rossi).')

# =============== 9 FERRAMENTA ===============
def fer(name, desc, body, alt):
    return card(svgi(240,100,body,alt,dw=240,dh=100)+h3(name,30)+p(desc,24),CARD,24,10)
deck=line(10,88,230,88,SOFT,4)
ic={
'Galloccia':(deck+f'<rect x="100" y="60" width="12" height="28" fill="{NAVY}"/><rect x="128" y="60" width="12" height="28" fill="{NAVY}"/><path d="M40 58 Q55 44 90 46 L150 46 Q185 44 200 58 Q185 62 150 60 L90 60 Q55 62 40 58 Z" fill="{NAVY}"/>','Galloccia: un appiglio a due corna fissato in coperta'),
'Bitta':(deck+f'<rect x="104" y="44" width="32" height="44" fill="{NAVY}"/><ellipse cx="120" cy="42" rx="34" ry="11" fill="{NAVY}"/>','Bitta: colonnetta con testa a fungo'),
'Battagliola':(deck+''.join(line(x,88,x,22,NAVY,5) for x in (30,90,150,210))+line(30,26,210,26,ACC,3)+line(30,56,210,56,ACC,3),'Battagliola: candelieri verticali uniti da due draglie'),
'Pulpito':(line(10,88,170,88,SOFT,4)+f'<path d="M170 88 Q205 88 222 60" fill="none" stroke="{SOFT}" stroke-width="4"/><path d="M40 30 L150 30 Q205 30 210 64" fill="none" stroke="{NAVY}" stroke-width="6"/>'+line(60,30,60,88,NAVY,5)+line(130,30,130,88,NAVY,5),'Pulpito: ringhiera in tubo all\'estremità di prua'),
'Musone':(f'<path d="M10 40 L170 40 Q200 40 210 60 L150 95 L10 95 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><rect x="170" y="28" width="44" height="18" rx="6" fill="{NAVY}"/><circle cx="212" cy="37" r="9" fill="{ACC}"/>'+line(220,40,232,92,SOFT,3),'Musone: blocco a prua estrema con il passacatena e il rullo per l\'ancora'),
'Ombrinale':(f'<path d="M10 50 L180 50 L180 95 L10 95 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><path d="M40 50 Q90 40 170 50" fill="{TEAL}" fill-opacity="0.35"/><rect x="176" y="56" width="10" height="12" fill="{NAVY}"/>'+arrow(186,62,226,84,TEAL,3),'Ombrinale: foro vicino alla murata da cui esce l\'acqua di coperta'),
}
D={'Galloccia':'Appiglio per dare volta a cavi d\'ormeggio, drizze e scotte.','Bitta':'Colonnetta bassa e robusta, a fungo, per catene e cavi d\'ormeggio.','Battagliola':'Draglie e candelieri: ringhiera per passare da poppa a prua.','Pulpito':'Protezione in tubo a estrema prua e poppa, dove si ancora la battagliola.','Musone':'Ferramenta a prua estrema che comprende il passacatena dell\'ancora.','Ombrinale':'Piccola apertura che fa defluire l\'acqua da coperta o pozzetto.'}
g=''.join(fer(n,D[n],*ic[n]) for n in D)
sec('ferramenta', head('Nomenclatura · in coperta','La ferramenta di bordo')+f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px">{g}</div>',
 notes='Quiz 1.1.1-17 (galloccia), -18 (bitta), -30, -31, -50 (battagliola, draglie, candelieri), -66 (pulpito), -63 (musone), -26 (ombrinale). Il pozzetto è la parte esterna dove sono le manovre e il timone (quiz -65). La sagola è una cima di piccolo diametro (-40).')

# =============== 10 SOTTO LA LINEA DI GALLEGGIAMENTO ===============
skin=f'<rect x="0" y="0" width="120" height="200" fill="{WATER}" fill-opacity="0.18"/><rect x="120" y="0" width="26" height="200" fill="{ACC}" fill-opacity="0.85"/>'
pas=skin+f'<rect x="96" y="80" width="24" height="40" fill="{NAVY}"/><rect x="146" y="88" width="120" height="24" fill="{SOFT}"/>'+''.join(line(160+i*14,88,166+i*14,112,NAVY,2) for i in range(7))+f'<rect x="146" y="76" width="18" height="48" fill="{NAVY}"/>'
pre=skin+f'<rect x="96" y="80" width="24" height="40" fill="{NAVY}"/><rect x="146" y="88" width="50" height="24" fill="{SOFT}"/><circle cx="222" cy="100" r="30" fill="{NAVY}"/><rect x="214" y="30" width="16" height="44" rx="6" fill="{ACC}"/><rect x="252" y="90" width="60" height="20" fill="{TEAL}" fill-opacity="0.8"/>'
zin=f'<rect x="0" y="0" width="320" height="200" fill="{WATER}" fill-opacity="0.12"/>'+line(0,100,230,100,SOFT,14)+f'<rect x="120" y="82" width="46" height="36" rx="8" fill="#9AA5AE" stroke="{NAVY}" stroke-width="3"/><ellipse cx="250" cy="100" rx="14" ry="70" fill="{NAVY}"/><ellipse cx="250" cy="100" rx="40" ry="12" fill="{NAVY}"/>'
ant=f'<rect x="0" y="0" width="320" height="200" fill="{WATER}" fill-opacity="0.12"/><path d="M0 60 Q160 150 320 60 L320 0 L0 0 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><path d="M0 60 Q160 150 320 60 L320 84 Q160 174 0 84 Z" fill="{ACC}"/><rect x="150" y="128" width="90" height="30" rx="12" fill="{NAVY}" transform="rotate(-18 195 143)"/><path d="M232 160 L262 196" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>'
cc=card(svgi(320,200,ant,'Rullo che stende la vernice antivegetativa rossa sull\'opera viva',dw=342,dh=214)+h3('Antivegetativa',30)+p('Vernice speciale per l\'opera viva: impedisce ad alghe e organismi marini di attaccarsi alla carena.',24),CARD,28)
cc+=card(svgi(320,200,pas,'Passascafo: raccordo filettato che attraversa lo spessore della carena',dw=342,dh=214)+h3('Passascafo',30)+p('La parte filettata che attraversa lo spessore della carena e si collega alla presa a mare.',24),CARD,28)
cc+=card(svgi(320,200,pre,'Presa a mare: valvola con leva montata sul passascafo, collegata al tubo',dw=342,dh=214)+h3('Presa a mare',30)+p('La valvola sul passascafo che permette di chiudere l\'ingresso dell\'acqua in barca.',24),CARD,28)
cc+=card(svgi(320,200,zin,'Zinco a collare montato sull\'asse dell\'elica',dw=342,dh=214)+h3('Zinchi',30)+p('Anodi sacrificali: si consumano al posto delle altre parti metalliche ed evitano le corrosioni galvaniche.',24),CARD,28)
sec('carena_imp', head('Protezione dello scafo e della carena','Antivegetativa, zinchi e prese a mare')+f'<div style="display:flex; gap:24px">{cc}</div>'+p('<b>Buona pratica:</b> controllare prese a mare e zinchi a ogni alaggio. Una presa a mare che perde è una falla.',26,BODY),
 notes='Il manuale Il Frangente tratta la protezione dello scafo e della carena insieme alle caratteristiche dell\'unità. Antivegetativa (antifouling): per questo nei disegni la carena è rossa. Quiz 1.1.1-64 (passascafo), -67 (prese a mare), -43 (zinchi: evitare le corrosioni galvaniche, non aumentare la zavorra).')

quiz_slide('quiz2','Quiz 2 · Parti dello scafo e coperta',['1.1.1-13','1.1.1-27','1.1.1-43'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.1.1-13','1.1.1-27','1.1.1-43'],True)

# =============== 11 CARENE ===============
def carena(kind):
    s=f'<rect x="0" y="80" width="480" height="120" fill="{WATER}" fill-opacity="0.12"/>'+line(0,80,480,80,TEAL,2)
    if kind=='disl':
        s+=f'<path d="M20 40 L140 40 C140 110 110 150 80 150 C50 150 20 110 20 40 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/>'
        s+=f'<path d="M190 50 L450 44 Q460 70 430 118 L220 122 L200 100 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/>'
        s+=f'<path d="M440 80 Q458 64 474 80" fill="none" stroke="{TEAL}" stroke-width="3"/><path d="M430 84 Q450 60 470 60" fill="none" stroke="{TEAL}" stroke-width="3"/>'
    elif kind=='plan':
        s+=f'<path d="M20 40 L140 40 L140 70 L80 92 L20 70 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/>'
        s+=f'<g transform="rotate(-6 320 80)"><path d="M190 52 L450 52 Q462 64 440 86 L200 90 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/></g>'
        s+=f'<path d="M180 92 Q140 96 110 90" fill="none" stroke="{TEAL}" stroke-width="3"/>'
    else:
        s+=f'<path d="M20 40 L140 40 C140 84 118 112 80 118 C42 112 20 84 20 40 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/>'
        s+=f'<g transform="rotate(-3 320 80)"><path d="M190 50 L450 48 Q462 66 438 100 L205 104 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/></g>'
    return s
cr=card(svgi(480,200,carena('disl'),'Carena dislocante: sezione tonda e scafo immerso che sposta l\'acqua',dw=474,dh=198)+h3('Dislocante',30)+p('Carena <b>tonda</b>: non plana, avanza spostando l\'acqua ai lati. Tipica di barche a vela e navette.',24),CARD,28)
cr+=card(svgi(480,200,carena('plan'),'Carena planante: sezione piatta o a V, scafo che scivola sull\'acqua con la prua alta',dw=474,dh=198)+h3('Planante',30)+p('Fondo <b>piatto o a V</b>: oltre una certa velocità si solleva e scivola sull\'acqua.',24),CARD,28)
cr+=card(svgi(480,200,carena('semi'),'Carena semiplanante: sezione intermedia e scafo poco sollevato',dw=474,dh=198)+h3('Semiplanante',30)+p('Via di mezzo: naviga dislocante a bassa velocità e plana in parte a velocità più alta.',24),CARD,28)
sec('carene', head('Le carene','Dislocante, planante, semiplanante')+f'<div style="display:flex; gap:24px">{cr}</div>'+card(p('<b>Per il quiz:</b> la carena dislocante è quella tonda, che non plana e sposta l\'acqua a destra e a sinistra. La carena a <b>V profonda</b> affronta meglio il moto ondoso molto formato.',26,INK),TEALCARD,24),
 notes='Quiz 1.1.1-52 e -71 (carena dislocante: tonda, non plana e sposta l\'acqua lateralmente); -68 (la V profonda affronta meglio il mare formato; la dislocante non è adatta alla planata; la carena piatta non è adatta al mare formato). Nota: il quiz 1.1.1-70 dà come esatta «tonda oppure a V profondo»: segnalarlo agli allievi.')

# =============== 12 DISLOCAMENTO ===============
X,Y,W,Hh=128,290,792,620
b=f'<rect x="0" y="310" width="{W}" height="{Hh-310}" fill="{WATER}" fill-opacity="0.10"/>'+section_hull(cid='s12')+line(0,310,W,310,TEAL,3)
b+=f'<rect x="200" y="110" width="260" height="60" rx="10" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b+=arrow(330,250,330,380,NAVY,6,22)+f'<circle cx="330" cy="250" r="14" fill="{NAVY}"/>'
b+=arrow(330,420,330,300,TEAL,6,22)+f'<circle cx="330" cy="420" r="14" fill="{TEAL}"/>'
lbls=lab(X+360,Y+200,300,'G · baricentro: qui agisce il <b>peso</b>',INK,24,600,'left',PAPER)+lab(X+360,Y+410,300,'C · centro di carena: qui agisce la <b>spinta</b>',TEAL,24,600,'left',PAPER)
txt=term('Dislocamento','Il <b>peso</b> dell\'unità: uguale al peso dell\'acqua spostata dalla carena (principio di Archimede).')+term('Stazza','Il <b>volume</b> interno dell\'unità, cioè la sua capacità. Non è un peso.')+term('Portata','Il <b>carico</b> che l\'unità può trasportare: persone, carburante, acqua, provviste.')+term('Equilibrio','Peso e spinta sono uguali e stanno sulla stessa verticale. Se carico la barca, cresce il pescaggio e cala il bordo libero.')
sec('dislocamento', head('Caratteristiche dell\'unità','Dislocamento, stazza e portata')+f'<div style="position:absolute; left:968px; top:290px; width:824px; display:flex; flex-direction:column; gap:28px">{txt}</div>', pinned=svgp(X,Y,W,Hh,b,'Sezione dello scafo con il baricentro G e la freccia del peso verso il basso, il centro di carena C e la freccia della spinta verso l\'alto')+lbls,
 notes='Nel manuale Il Frangente (cap. 1) lunghezza, dislocamento, stazza e portata sono le caratteristiche dell\'unità. Quiz 1.1.2-50: il peso della nave corrisponde al dislocamento, non alla portata né alla stazza (distrattori del quiz). La stazza si esprime in tonnellate di stazza (GT) ed è una misura di volume. Il centro di carena è il baricentro del volume immerso.')
X,Y,W,Hh=1000,290,792,620

# =============== 13 ASSI E MOVIMENTI ===============
def curved(cx,cy,r,a0,a1,c=ACC):
    x0,y0=cx+r*math.cos(math.radians(a0)),cy+r*math.sin(math.radians(a0)); x1,y1=cx+r*math.cos(math.radians(a1)),cy+r*math.sin(math.radians(a1))
    s=f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{c}" stroke-width="6"/>'
    t=math.radians(a1); tx,ty=-math.sin(t),math.cos(t)
    return s+f'<polygon points="{x1+tx*16:.1f},{y1+ty*16:.1f} {x1-tx*2+math.cos(t)*12:.1f},{y1-ty*2+math.sin(t)*12:.1f} {x1-tx*2-math.cos(t)*12:.1f},{y1-ty*2-math.sin(t)*12:.1f}" fill="{c}"/>'
roll=f'<path d="M140 90 L340 90 C340 170 290 210 240 214 C190 210 140 170 140 90 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><rect x="190" y="56" width="100" height="34" rx="8" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><circle cx="240" cy="140" r="10" fill="{NAVY}"/>'+curved(240,140,120,200,340)
pitch=profile(40,170,400)+dash(20,150,460,150)+curved(240,150,120,-150,-30)
yaw=f'<path d="M80 110 L330 105 Q420 112 460 150 Q420 188 330 195 L80 190 Q72 150 80 110 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><circle cx="260" cy="150" r="10" fill="{NAVY}"/>'+curved(260,150,110,-60,60)
ac=card(svgi(480,240,roll,'Vista da poppa: freccia curva attorno all\'asse longitudinale, il rollio',dw=474,dh=236)+tag('Asse longitudinale')+h3('Rollio',30)+p('Oscillazione da un lato all\'altro: la barca si inclina a dritta e a sinistra.',24),CARD,28)
ac+=card(svgi(480,240,pitch,'Vista di profilo: freccia curva attorno all\'asse trasversale, il beccheggio',dw=474,dh=236)+tag('Asse trasversale')+h3('Beccheggio',30)+p('La prua si immerge mentre la poppa si solleva, e viceversa.',24),CARD,28)
ac+=card(svgi(480,240,yaw,'Vista dall\'alto: freccia curva attorno all\'asse verticale, l\'accostata',dw=474,dh=236)+tag('Asse verticale')+h3('Accostata',30)+p('Rotazione attorno all\'asse verticale: la prua devia da un lato e la poppa dall\'altro.',24),CARD,28)
sec('assi', head('Assi e movimenti','Rollio, beccheggio e accostata')+f'<div style="display:flex; gap:24px">{ac}</div>'+p('<b>Assetto:</b> la posizione di equilibrio della barca nel piano longitudinale, prua–poppa.',26,BODY),
 notes='Quiz 1.1.1-69 (rollio: asse longitudinale), -34 (beccheggio: asse trasversale), 1.1.2-47, -48, -49 e -46 (assetto). L\'asse longitudinale passa per prua e poppa, parallelo alla chiglia (1.1.1-2). L\'accostata è detta anche imbardata.')

quiz_slide('quiz1','Quiz 1 · Dimensioni, pesi e carene',['1.1.1-1','1.1.2-50','1.1.1-52'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.1.1-1','1.1.2-50','1.1.1-52'],True)

# =============== 14 STABILITA ===============
def stab(heeled, cid):
    s=f'<rect x="0" y="300" width="660" height="220" fill="{WATER}" fill-opacity="0.10"/>'
    hp='M100 170 C 100 330, 190 420, 330 450 C 470 420, 560 330, 560 170 Z'
    grp=f'<path d="{hp}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/><path d="M318 448 L322 520 L338 520 L342 448 Z" fill="{NAVY}"/><rect x="200" y="110" width="260" height="60" rx="10" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'+dash(330,60,330,500,SOFT)
    if heeled:
        s+=f'<g transform="translate(-50 0) rotate(20 330 300)">{grp}</g>'
        G=(293.7,262.4); C=(342,378); M=(341,132)
        s+=line(0,300,660,300,TEAL,3)+dash(C[0],C[1],M[0],M[1],TEAL)
        s+=f'<path d="M140 250 A150 150 0 0 1 200 160" fill="none" stroke="{ACC}" stroke-width="6"/><polygon points="212,150 188,158 202,176" fill="{ACC}"/>'
    else:
        s+=grp+line(0,300,660,300,TEAL,3); G=(330,262); C=(330,380); M=(330,132)
    s+=arrow(G[0],G[1],G[0],G[1]+110,NAVY,5,20)+f'<circle cx="{G[0]}" cy="{G[1]}" r="12" fill="{NAVY}"/>'
    s+=arrow(C[0],C[1],C[0],C[1]-110,TEAL,5,20)+f'<circle cx="{C[0]}" cy="{C[1]}" r="12" fill="{TEAL}"/>'
    s+=f'<circle cx="{M[0]}" cy="{M[1]}" r="10" fill="{ACC}"/>'
    return s,G,C,M
X1,Y1=128,290; X2,Y2=1004,290
s1,G1,C1,M1=stab(False,'a'); s2,G2,C2,M2=stab(True,'b')
pin=svgp(X1,Y1,660,520,s1,'Barca dritta: baricentro G e centro di carena C sulla stessa verticale, metacentro M più in alto')+svgp(X2,Y2,660,520,s2,'Barca sbandata di 20 gradi: il centro di carena C si sposta verso il lato immerso, peso e spinta formano la coppia di raddrizzamento')
def gl(X,Y,G,C,M,right=True):
    dx=24
    return lab(X+G[0]+dx,Y+G[1]-18,60,'G',NAVY,26,700)+lab(X+C[0]+dx,Y+C[1]-18,60,'C',TEAL,26,700)+lab(X+M[0]+dx,Y+M[1]-18,60,'M',ACC,26,700)
pin+=gl(X1,Y1,G1,C1,M1)+gl(X2,Y2,G2,C2,M2)+lab(X1,Y1,600,'<b>Barca dritta</b>: peso e spinta sulla stessa verticale',INK,24,400)
pin+=lab(X2,Y2,660,'<b>Barca sbandata</b>: C si sposta sul lato immerso e nasce la <b>coppia di raddrizzamento</b>',INK,24,400)
strip=f'<div style="position:absolute; left:128px; top:820px; width:1664px; display:flex; gap:24px">'+card(p('<b>Stabilità di forma</b>: dipende dalla forma della carena; una carena larga resiste di più allo sbandamento.',24,INK),TEALCARD,20)+card(p('<b>Stabilità di peso</b>: dipende dal baricentro; pesi in basso, zavorra e bulbo la aumentano.',24,INK),TEALCARD,20)+card(p('<b>Attenzione</b>: pesi in alto e carichi liberi alzano G e riducono la stabilità.',24,INK),CARD,20)+'</div>'
sec('stabilita', head('Stabilità','Baricentro, centro di carena e metacentro'), pinned=pin+strip,
 notes='G: baricentro, dove agisce il peso. C: centro di carena, dove agisce la spinta. M: metacentro, il punto dove la verticale per C sbandato incontra l\'asse di simmetria. Finché M sta sopra G, peso e spinta formano una coppia che raddrizza la barca. Quiz 1.1.1-12: la coppia di stabilità di forma dipende dalla forma della carena. Nelle barche a vela la zavorra e il bulbo abbassano G (stabilità di peso).')

# =============== 15 FLAPS ===============
X,Y,W,Hh=1000,290,792,520
b=water(W,300,Hh,0.10)
x0,wl,L=220,300,520
b+=f'<g transform="rotate(-2 480 300)">{profile(x0,wl,L)}</g>'
tp=P(x0,wl,L,0.02,0.03)
b+=f'<path d="M{tp[0]-2:.1f} {tp[1]+2:.1f} L{tp[0]-58:.1f} {tp[1]+24:.1f}" stroke="{ACC}" stroke-width="10" stroke-linecap="round"/>'
b+=arrow(700,338,300,340,TEAL,3)+arrow(250,350,190,392,TEAL,3)
b+=arrow(210,250,210,160,NAVY,5,18)+arrow(760,120,760,210,NAVY,5,18)
st='<rect x="40" y="410" width="240" height="70" rx="10" fill="'+BOAT+'" stroke="'+NAVY+'" stroke-width="3"/><rect x="60" y="478" width="70" height="12" fill="'+ACC+'"/><rect x="190" y="478" width="70" height="12" fill="'+ACC+'"/>'
b+=st
lbls=lab(X+60,Y+110,260,'la poppa si alza',NAVY,24,700)+lab(X+560,Y+60,230,'la prua si abbassa',NAVY,24,700)+lab(X+300,Y+420,300,'Vista da poppa: due flaps',INK,24,700)+lab(X+40,Y+268,160,'Flap',ACC,24,700)
txt=term('Cosa sono','Appendici immerse montate sullo specchio di poppa: sempre due, una a dritta e una a sinistra.')+term('Come si usano','Si regolano anche in modo indipendente: correggono assetto longitudinale e trasversale. Indicatore a zero = flap orizzontale; valori negativi = flap verso il basso.')+term('Con il mare','Mare di prua: più o meno abbassati, contro la prua che si alza. Mare di poppa: alzati, contro l\'onda che solleva la poppa.')
sec('flaps', head('Assetto in navigazione','I flaps')+f'<div style="display:flex; flex-direction:column; gap:24px; width:820px">{txt}</div>', pinned=svgp(X,Y,W,Hh,b,'Profilo di un motoscafo con il flap abbassato a poppa: il flusso d\'acqua viene deviato verso il basso, la poppa si alza e la prua si abbassa; sotto, la vista da poppa con i due flaps')+lbls,
 notes='Quiz 1.1.1-73, -74, -75 e 1.3.8 (401-404): i flaps sono appendici immerse sullo specchio di poppa, sempre due, regolabili in modo indipendente; indicatore a zero = neutro; negativo = inclinati verso il basso. Con moto ondoso contrario: tenerli più o meno abbassati, secondo lo scafo, per contrastare la tendenza della carena ad alzare la prua. Con mare formato di poppa: tenerli alzati. Il quiz base-405 sul flap sinistro/destro è stato oscurato: non usarlo.')

# =============== 16 TRIM ===============
def trimsvg(ang, lift):
    s=f'<rect x="0" y="120" width="480" height="80" fill="{WATER}" fill-opacity="0.12"/>'+line(0,120,480,120,TEAL,2)
    boat=profile(90,120,340)
    tx,ty=P(90,120,340,0.01,-0.03)
    mot=f'<g transform="rotate({ang} {tx:.1f} {ty:.1f})"><rect x="{tx-34:.1f}" y="{ty-44:.1f}" width="34" height="36" rx="6" fill="{NAVY}"/><rect x="{tx-24:.1f}" y="{ty-8:.1f}" width="12" height="70" fill="{NAVY}"/><ellipse cx="{tx-18:.1f}" cy="{ty+64:.1f}" rx="6" ry="16" fill="{ACC}"/></g>'
    return f'<g transform="rotate({lift} 260 120)">{boat}</g>'+mot
tc=card(svgi(480,200,trimsvg(-12,4),'Trim negativo: piede del motore verso lo scafo, prua abbassata',dw=474,dh=198)+tag('Piede in basso')+h3('Trim negativo',30)+p('«Tutto basso»: più spinta iniziale per entrare in planata. Con mare formato abbassa la prua e attutisce gli impatti.',24),CARD,28)
tc+=card(svgi(480,200,trimsvg(0,0),'Trim neutro: gambo del motore in posizione intermedia, barca in assetto',dw=474,dh=198)+tag('Posizione intermedia')+h3('Trim neutro',30)+p('Il gambo sta nella posizione intermedia: l\'assetto normale di crociera.',24),CARD,28)
tc+=card(svgi(480,200,trimsvg(14,-5),'Trim positivo: piede del motore lontano dallo scafo, prua sollevata',dw=474,dh=198)+tag('Piede in alto')+h3('Trim positivo',30)+p('Alza la prua e riduce la superficie bagnata: più velocità con mare calmo. Se è eccessivo, la prua saltella.',24),CARD,28)
sec('trim', head('Assetto in navigazione','Il trim del fuoribordo')+p('Il trim è il <b>pistone idraulico</b> che cambia l\'angolo tra lo specchio di poppa e il gambo del motore fuoribordo.',26,INK)+f'<div style="display:flex; gap:24px">{tc}</div>',
 notes='Quiz 1.1.1-72 (definizione del trim), 1.4.4-39 (trim tutto basso = assetto tutto negativo, per la spinta iniziale verso la planata), base-391 (trim negativo abbassa la prua e attutisce gli impatti con mare formato), base-595 (il trim determina l\'innalzamento della prua).')

quiz_slide('quiz3','Quiz 3 · Assi e stabilità',['1.1.1-34','1.1.1-69','1.1.1-12'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.1.1-34','1.1.1-69','1.1.1-12'],True)
quiz_slide('quiz4','Quiz 4 · Assetto: flaps e trim',['1.1.1-73','1.4.4-39','1.1.2-46'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.1.1-73','1.4.4-39','1.1.2-46'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.1.1-45','1.1.1-17','1.1.1-22'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.1.1-45','1.1.1-17','1.1.1-22'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.1.1-68','1.1.1-63','1.1.1-47'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.1.1-68','1.1.1-63','1.1.1-47'],True)

# =============== CHIUSURA ===============
pts=['Natante fino a 10 m, imbarcazione fino a 24 m, nave oltre','Opera viva sotto la linea di galleggiamento, opera morta sopra','Rosso a sinistra, verde a dritta: masconi a prua, giardinetti a poppa','Carena tonda = dislocante; V profonda per il mare formato','G basso e carena larga = barca stabile; flaps e trim regolano l\'assetto']
ul=''.join(f'<li>{x}</li>' for x in pts)
n=len(slides)+1
slides.append(('chiusura', f'''<section id="chiusura" data-transition="fade" style="background:{NAVY}; color:{PAPER}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:40px">
{backdrop(True)}
{header('In sintesi','Cinque cose da ricordare','flag',ACC,True)}
<ol style="font-size:30px; line-height:1.45; color:{DSOFT}; display:flex; flex-direction:column; gap:14px; width:1500px">{ul}</ol>
<p style="font-size:28px; font-weight:700; color:{DACC}">Prossima lezione · 02 · Motori, elica e timone</p>
{footer(n,True)}
<aside>Assegnare a casa il ripasso dei 75 quiz ufficiali di nomenclatura dello scafo (1.1.1).</aside>
</section>
'''))

ORDER=['cover','agenda','classificazione','profilo','sezione','dislocamento','carene','carena_imp','quiz1','quiz1r','orientamento','struttura','legno','sottocoperta','ferramenta','quiz2','quiz2r','assi','stabilita','quiz3','quiz3r','flaps','trim','quiz4','quiz4r','finale1','finale1r','finale2','finale2r','chiusura']
import re as _re
d=dict(slides); assert sorted(d)==sorted(ORDER),(set(d)^set(ORDER))
slides=[(i,d[i]) for i in ORDER]
os.makedirs(OUT+'/slides',exist_ok=True)
for k,(id_,h) in enumerate(slides,1):
    h=_re.sub(r'(border-radius:20px">)\d\d(</p>)', lambda m: f'{m.group(1)}{k:02d}{m.group(2)}', h)
    open(f'{OUT}/slides/{id_}.html','w').write(h)
deck={"v":4,"createdOnFiles":{"v":1,"at":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')},"title":TITLE,"order":[i for i,_ in slides],"cover":"cover",
 "sections":{"s1":{"description":"Apertura e obiettivi della lezione","start":"cover"},
  "s2":{"description":"Classificazione e caratteristiche: dimensioni, pesi, carene e loro protezione","start":"classificazione"},
  "s3":{"description":"Parti dello scafo, struttura e attrezzatura di coperta","start":"orientamento"},
  "s4":{"description":"Assi, stabilità e assetto di navigazione","start":"assi"},
  "s5":{"description":"Verifica finale con i quiz ufficiali e sintesi","start":"finale1"}},
 "faces":FACES,"designSystems":[]}
json.dump(deck,open(OUT+'/deck.json','w'),ensure_ascii=False,indent=1)
print(len(slides)); print(json.dumps({f'project/slides/{i}.html':f'project/slides/{i}.html' for i,_ in slides}))
import re
for i,h in slides:
    for m in re.finditer(r'<svg.*?</svg>',h,re.S):
        if len(m.group(0))>52000: print('BIG SVG',i,len(m.group(0)))
    ne=len(re.findall(r'<(?!/)(?!aside)[a-z]',h))
    if ne>200: print('MANY',i,ne)
