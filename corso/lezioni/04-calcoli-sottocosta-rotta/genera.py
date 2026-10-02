import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez04/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; SAND='#F3E3B8'; GREY='#97A6B4'; STEEL='#8E9BAA'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','La rosa dei venti':'compass','Gli strumenti del carteggio':'dividers','La navigazione stimata':'pencil','Spazio, velocità, tempo':'chart','Tre esempi svolti':'pencil','Il carburante sulla carta':'fuel','Raccolta quiz':'quiz','Com\'è fatta un\'ancora':'anchor','I tipi di ancora':'anchor','Il calumo':'anchor',
 'La manovra di ancoraggio':'anchor','Alla ruota o afforcati':'anchor','Vicino alla spiaggia':'flag','Subacquei e piccoli natanti':'flag',
 'La bussola magnetica':'compass','Tre nord':'compass','Da bussola a vero e ritorno':'compass','Prora e rotta':'map',
 'Lo scarroccio':'wind','La deriva':'current','Vento «da», corrente «verso»':'wind',
 'Rotte e coordinate':'map','Misurare le miglia':'dividers','Miglia, velocità, tempo':'chart','Carburante e riserva':'fuel','Rotta vera e prora vera':'map',
 'Angoli di scarroccio e deriva':'wind','Moto proprio e moto effettivo':'current','La declinazione magnetica':'compass','La deviazione magnetica':'compass','La tabella delle deviazioni':'compass',
 'Navigare in vista della costa':'lighthouse','Rilevamento vero e polare':'compass',
 'Dove sono rispetto al faro':'lighthouse','I luoghi di posizione':'map','Il punto nave costiero':'pencil','Il GPS':'map',
 'I fanali di navigazione':'lantern','Cosa vedo di notte':'lantern','Le barche a vela di notte':'sail','Segnali diurni e luci speciali':'flag',
 'Chi lascia la rotta a chi':'helm','C\'è rischio di collisione?':'compass','Due barche a motore':'helm','Due barche a vela':'sail',
 'Rilevamento polare':'compass','Due punti cospicui':'lighthouse','Un punto cospicuo: rilevamento e distanza':'lighthouse','Rilevamenti successivi':'pencil','I rilevamenti':'compass','Il punto nave: tutte le tecniche':'map'})
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

def dot(n,c): return f'<p style="width:44px; height:44px; border-radius:22px; background:{c}; color:#FFFFFF; font-weight:900; font-size:22px; text-align:center; line-height:44px; flex:none">{n}</p>'

# ---- slide di apertura dei capitoli (stesse della lezione 03) ----
GRID='#8FB3C6'; CHART='#FBF8EF'; LAND='#F2E2B3'
if 'glow' not in globals():
    def glow(x,y,c,r=9):
        return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.6:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.6:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
def _panel(cid,body): return f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="500" height="220" rx="48"/></clipPath></defs><rect x="0" y="0" width="500" height="220" rx="48" fill="#FFFFFF" fill-opacity="0.06"/><g clip-path="url(#{cid})">{body}<path d="M-20 200 q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 L540 220 L-20 220 Z" fill="{WATER}"/></g>'
def compass_scene():
    s=f'<g transform="translate(250 105)"><circle r="82" fill="{CHART}" stroke="{DACC}" stroke-width="8"/>'
    s+=''.join(f'<path d="M0 -82 L0 -70" stroke="{NAVY}" stroke-width="3" transform="rotate({a_})"/>' for a_ in range(0,360,30))
    s+=f'<path d="M0 -66 L12 0 L0 66 L-12 0 Z" fill="{NAVY}"/><path d="M-66 0 L0 12 L66 0 L0 -12 Z" fill="{NAVY}" fill-opacity="0.55"/><path d="M0 -66 L12 0 L-12 0 Z" fill="{CORAL}"/><circle r="7" fill="{DACC}"/></g>'
    s+=f'<text x="250" y="20" text-anchor="middle" font-family="Arial" font-size="18" font-weight="900" fill="{DACC}">N</text>'
    s+=f'<path d="M60 150 L120 120" stroke="{CORAL}" stroke-width="4" stroke-dasharray="8 6"/><path d="M380 140 L450 110" stroke="{CORAL}" stroke-width="4" stroke-dasharray="8 6"/>'
    return _panel('chb',s)
def ring_scene():
    s=f'<g transform="translate(250 120)"><circle r="62" fill="none" stroke="{ORANGE if "ORANGE" in globals() else "#F28C28"}" stroke-width="30"/><circle r="62" fill="none" stroke="#FFFFFF" stroke-width="30" stroke-dasharray="32 33"/></g>'
    s+=f'<path d="M312 120 Q380 90 420 140 Q440 170 470 160" fill="none" stroke="{DACC}" stroke-width="6"/>'
    return _panel('chr',s)
def fire_scene():
    s=f'<g transform="translate(180 30)"><rect x="0" y="40" width="70" height="140" rx="22" fill="{CORAL}"/><rect x="20" y="16" width="30" height="28" rx="6" fill="{NAVY}"/><path d="M50 22 L96 8 L100 20 L56 32 Z" fill="{NAVY}"/><rect x="12" y="80" width="46" height="40" rx="6" fill="#FFFFFF"/></g>'
    s+=f'<g transform="translate(340 140) scale(1.6)"><path d="M0 30 Q-26 10 -12 -22 Q-6 -8 0 -12 Q2 -34 16 -44 Q14 -20 24 -6 Q30 16 0 30 Z" fill="#F28C28"/><path d="M0 26 Q-12 12 -4 -6 Q2 4 6 -2 Q14 10 0 26 Z" fill="{DACC}"/></g>'
    return _panel('chf',s)
def radio_scene():
    s=f'<g transform="translate(205 20)"><rect x="40" y="0" width="12" height="50" rx="5" fill="{NAVY}"/><rect x="10" y="40" width="80" height="150" rx="18" fill="#2A4A6B" stroke="{DACC}" stroke-width="4"/><rect x="24" y="58" width="52" height="34" rx="6" fill="{SEA}"/>'
    s+=f'<text x="50" y="82" text-anchor="middle" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">16</text>'+''.join(f'<circle cx="{30+(i%3)*20}" cy="{112+(i//3)*20}" r="6" fill="{DACC}"/>' for i in range(9))+'</g>'
    s+=''.join(f'<path d="M{330+k*22} {60-k*4} q14 30 0 60" fill="none" stroke="{DACC}" stroke-width="5" stroke-linecap="round" opacity="{1-k*0.25}"/>' for k in range(3))
    return _panel('chv',s)
def chart_scene():
    s=f'<defs><clipPath id="chc"><rect x="0" y="0" width="500" height="220" rx="48"/></clipPath></defs><rect x="0" y="0" width="500" height="220" rx="48" fill="#FFFFFF" fill-opacity="0.06"/><g clip-path="url(#chc)">'
    s+=f'<g transform="rotate(-6 150 120)"><rect x="40" y="40" width="230" height="150" rx="8" fill="{CHART}"/>'
    s+=''.join(line(40+i*46,40,40+i*46,190,GRID,1.5) for i in range(1,5))+''.join(line(40,40+j*37.5,270,40+j*37.5,GRID,1.5) for j in range(1,4))
    s+=f'<path d="M40 150 Q90 120 120 150 Q150 175 190 160 L270 170 L270 190 L40 190 Z" fill="{LAND}"/><path d="M70 70 L230 130" stroke="{CORAL}" stroke-width="4" stroke-dasharray="10 6"/><circle cx="70" cy="70" r="6" fill="{CORAL}"/><circle cx="230" cy="130" r="6" fill="{CORAL}"/>'
    s+=f'<g transform="translate(210 75)"><circle r="24" fill="none" stroke="{NAVY}" stroke-width="2"/><path d="M0 -26 L6 0 L0 26 L-6 0 Z" fill="{NAVY}"/><path d="M-26 0 L0 6 L26 0 L0 -6 Z" fill="{NAVY}" fill-opacity="0.6"/><path d="M0 -26 L6 0 L-6 0 Z" fill="{CORAL}"/></g></g>'
    s+=f'<path d="M330 220 L330 170 Q380 150 430 165 Q470 175 500 168 L500 220 Z" fill="#2A4A6B"/>'
    s+=f'<path d="M395 52 L515 10 L515 100 Z" fill="{DACC}" fill-opacity="0.35"/>'
    s+=f'<path d="M380 168 L386 70 L404 70 L410 168 Z" fill="#FFFFFF"/><rect x="384" y="94" width="22" height="12" fill="{CORAL}"/><rect x="382" y="128" width="26" height="12" fill="{CORAL}"/>'
    s+=f'<rect x="381" y="52" width="28" height="20" rx="4" fill="{DACC}"/><path d="M378 52 L395 38 L412 52 Z" fill="{CORAL}"/>{glow(395,62,DACC,7)}'
    s+=f'<path d="M-20 196 q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 L540 220 L-20 220 Z" fill="{WATER}"/></g>'
    return s
def quiz_scene():
    s=f'<defs><clipPath id="chq"><rect x="0" y="0" width="500" height="220" rx="48"/></clipPath></defs><rect x="0" y="0" width="500" height="220" rx="48" fill="#FFFFFF" fill-opacity="0.06"/><g clip-path="url(#chq)">'
    s+=f'<g transform="rotate(-5 160 110)"><rect x="60" y="22" width="200" height="190" rx="14" fill="{CHART}"/><rect x="125" y="12" width="70" height="24" rx="8" fill="{PURPLE}"/>'
    for i,(ok,yy) in enumerate(((1,62),(1,102),(0,142),(1,182))):
        s+=f'<rect x="84" y="{yy-14}" width="26" height="26" rx="6" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
        s+=(f'<path d="M89 {yy} l6 7 l12 -14" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' if ok else f'<path d="M90 {yy-8} l14 14 M104 {yy-8} l-14 14" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>')
        s+=f'<rect x="124" y="{yy-6}" width="{110-i*12}" height="10" rx="5" fill="{GRID}"/>'
    s+='</g>'
    s+=f'<g transform="translate(380 118)"><rect x="-10" y="-82" width="20" height="16" rx="4" fill="{DACC}"/><circle r="64" fill="#FFFFFF" stroke="{PURPLE}" stroke-width="10"/>'
    s+=f'<path d="M0 0 L0 -64 A64 64 0 1 1 -45.3 -45.3 Z" fill="{PURPLE}" fill-opacity="0.25"/><path d="M0 0 L0 -46" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/><path d="M0 0 L-30 -30" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/><circle r="7" fill="{NAVY}"/></g>'
    s+=f'<path d="M-20 200 q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 L540 220 L-20 220 Z" fill="{WATER}"/></g>'
    return s
_cid=[0]
def chapter(id_,n,title,subs,c,notes,dur='',cols=2,label=None,big=None,art=None):
    _cid[0]+=1
    rows=-(-len(subs)//cols); fs=30 if len(subs)<=12 else 22; bs=52 if len(subs)<=12 else 40
    items=''.join(f'<div style="display:flex; gap:14px; align-items:center"><p style="width:{bs}px; height:{bs}px; flex:none; border-radius:{bs//2}px; background:{c}; color:#FFFFFF; font-size:{bs*0.45:.0f}px; font-weight:900; text-align:center; line-height:{bs}px">{i}</p><p style="font-size:{fs}px; line-height:1.2; font-weight:700; color:#FFFFFF">{t}</p></div>' for i,t in enumerate(subs,1))
    left=(f'<div style="width:500px; flex:none; display:flex; flex-direction:column; gap:10px">'
          f'<p style="font-size:24px; font-weight:900; letter-spacing:2px; text-transform:uppercase; color:{c}">{label or "Capitolo"}</p>'
          f'<p style="font-family:{H}; font-size:{200 if big is None else 150}px; font-weight:700; line-height:0.9; color:{DACC}">{big or n}</p>'
          f'<h2 style="font-family:{H}; font-size:56px; font-weight:700; line-height:1.08; color:#FFFFFF">{title}</h2>{squiggle(c,220)}'
          f'<p style="font-size:26px; font-weight:700; color:{DSOFT}">{dur}</p>'
          f'<div style="flex:1"></div>'
          f'<svg aria-label="{art[1] if art else "Illustrazione: barca a vela sul mare"}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 220" width="500" height="220" style="width:500px; height:220px">{art[0] if art else sea_scene(500,220,True,True,"ch"+str(_cid[0]))}</svg></div>')
    right=f'<div style="flex:1; display:grid; grid-template-columns:repeat({cols},1fr); grid-template-rows:repeat({rows},auto); grid-auto-flow:column; gap:{24 if len(subs)<=12 else 16}px 32px; align-content:center; background:rgba(255,255,255,0.06); padding:36px; border-radius:32px">{items}</div>'
    sec(id_, f'<div style="display:flex; gap:56px; align-items:stretch; height:792px">{left}{right}</div>', notes=notes, dark=True, gap=0)



# ============ COVER + AGENDA ============
cover(4,'Carteggio e Navigazione: primi calcoli, sottocosta, prora e rotta','Orientarsi sulla carta, misurare le miglia e calcolare M = V × Tᵐ : 60 e il carburante; prora e rotta, scarroccio e deriva, declinazione e deviazione; punto nave, rilevamenti e GPS; la condotta sottocosta',
 'Lezione 4. Segue la scaletta della scuola «Carteggio · Navigazione»: rosa dei venti, rotte e quadranti, bussola, rotte e coordinate, navigazione stimata, misurazione e calcolo delle miglia, velocità, tempo, carburante, rotta vera e prora vera, scarroccio, deriva, angoli di scarroccio e deriva, moto proprio ed effettivo, declinazione, deviazione, tabella delle deviazioni, navigazione costiera, punto nave 1 e 2, rilevamento polare, rilevamenti, GPS: tutta la scaletta in una lezione. Aggiunta dall\'All. A: condotta sottocosta (punto 4a). Gli ultimi 45 minuti sono una raccolta di quiz ufficiali. Attracchi, ormeggi e ancoraggi sono nella lezione 3.', title_size=80)
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','11′','Rosa, bussola, coordinate',CORAL),('0:11','14′','Stima, miglia, tempo, carburante',SEA),('0:25','12′','Prora e rotta, scarroccio, deriva',PURPLE),('0:37','11′','Declinazione e deviazione',BLUE),('0:48','11′','Costiera e punto nave',GREEN),('0:59','11′','Rilevamenti e GPS',CORAL),('1:10','5′','Sotto­costa',SUN),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{max(int(d[:-1]),13)}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['manovra', 'navigazione'],4,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>orientarti con la rosa, leggere coordinate e rotte</li><li>calcolare miglia, tempi, velocità e carburante</li><li>passare da prora bussola a prora vera, con scarroccio e deriva</li><li>fare il punto nave con i rilevamenti e usare il GPS</li><li>rispettare le regole vicino alla spiaggia</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 04 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Sette capitoli di teoria in 75 minuti, nell\'ordine della scaletta della scuola «Carteggio · Navigazione», con una verifica da 2 quiz alla fine di ognuno: il programma è denso, andare spediti sulle slide, il dettaglio è nelle note. Poi 45 minuti di raccolta quiz. Banca DD 131/2022: orientamento e bussola 49 quiz (1.7.4), navigazione stimata 71 (1.7.5), navigazione costiera 49 (1.7.6), navigazione elettronica 13 (1.7.3), prora e rotta, scarroccio e deriva 30 (1.7.7), carburante 1.2.3, navigazione in prossimità della costa 32 (1.4.2).')
X=700

# ================= CAPITOLO 1 · ORIENTARSI =================
chapter('cap1',1,'Orientarsi sulla carta',['La rosa dei venti e i quadranti','La bussola magnetica','Gli strumenti del carteggio','Rotte e coordinate'],CORAL,
 'Circa 11 minuti, compresa una verifica da 2 quiz alla fine. Quiz 1-2 nella raccolta finale.','circa 11 minuti · 4 argomenti',1,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
# ============ ROSA DEI VENTI ============
rc,ry,RR=350,310,225
pt=lambda a,r: (rc+r*math.sin(math.radians(a)), ry-r*math.cos(math.radians(a)))
b=''
for k,c in enumerate(['#FFE7A8','#CFEFF2','#FFD5C7','#E0D7FA']):
    a0,a1=k*90,(k+1)*90; p0=pt(a0,RR); p1=pt(a1,RR)
    b+=f'<path d="M{rc} {ry} L{p0[0]:.1f} {p0[1]:.1f} A{RR} {RR} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{c}"/>'
b+=f'<circle cx="{rc}" cy="{ry}" r="{RR}" fill="none" stroke="{NAVY}" stroke-width="4"/>'
tk=' '.join(f'M{pt(a,RR)[0]:.1f} {pt(a,RR)[1]:.1f} L{pt(a,RR-(22 if a%30==0 else 11))[0]:.1f} {pt(a,RR-(22 if a%30==0 else 11))[1]:.1f}' for a in range(0,360,10))
b+=f'<path d="{tk}" stroke="{NAVY}" stroke-width="3"/>'
star=[]
for i in range(16):
    a=i*22.5; r=200 if i%4==0 else (130 if i%2==0 else 34); star.append(pt(a,r))
b+='<polygon points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in star)+f'" fill="{NAVY}" fill-opacity="0.88"/>'
b+=f'<circle cx="{rc}" cy="{ry}" r="12" fill="{SUN}"/>'
tip=pt(157,215); b+=arrow(rc,ry,tip[0],tip[1],CORAL,8,26)
RX=1092
lbl=''
for a,t in [(0,'N'),(45,'NE'),(90,'E'),(135,'SE'),(180,'S'),(225,'SW'),(270,'W'),(315,'NW')]:
    x,y=pt(a,262); lbl+=big(RX+x-50,Y+y-18,100,t,NAVY if a%90==0 else SOFT,34 if a%90==0 else 26)
for a,t,c in [(45,'I','#B77900'),(135,'II',SEA),(225,'III',CORAL),(315,'IV',PURPLE)]:
    x,y=pt(a,178); lbl+=big(RX+x-40,Y+y-24,80,t,c,44)
x,y=pt(157,215); lbl+=lab(RX+x+14,Y+y-10,120,'157°',CORAL,30,900,bg='#FFFFFF')
chips=''.join(f'<p style="font-size:24px; font-weight:800; color:{INK}; background:{bg}; padding:8px 14px; border-radius:18px">{t}</p>' for t,bg in [('N · Tramontana',SUN_T),('NE · Grecale',SUN_T),('E · Levante',SEA_T),('SE · Scirocco',SEA_T),('S · Ostro',CORAL_T),('SW · Libeccio',CORAL_T),('W · Ponente',LILAC_T),('NW · Maestrale',LILAC_T)])
right=(term('Angoli da 000° a 360°','Si contano dal Nord in senso orario, sempre con tre cifre: 045°, 157°, 320°.')
      +term('Rotte e quadranti','I NE 000-090 · II SE 090-180 · III SW 180-270 · IV NW 270-360. Una rotta di 157° è nel II quadrante: sulla carta va in basso a destra.')
      +term('Cardinali e intercardinali','N, E, S, W e NE, SE, SW, NW. Sulla carta il Nord è in alto.')
      +f'<div style="display:flex; flex-wrap:wrap; gap:10px">{chips}</div>')
sec('rosa', head('Orientarsi · rotte e quadranti','La rosa dei venti')+f'<div style="width:920px; display:flex; flex-direction:column; gap:20px">{right}</div>', pinned=svgp(RX,Y,700,620,b,'Rosa dei venti con i quattro quadranti colorati, le direzioni cardinali e intercardinali e una freccia verso 157 gradi nel secondo quadrante')+lbl,
 notes='Quiz 1.7.4-1, -4, -5, -6, -7 (in quale quadrante: 157° II, 224° III, 320° IV, 038° I, 099° II), -2 e -3 (sulla carta: 048° in alto a destra, 167° in basso a destra, 301° in alto a sinistra, 249° in basso a sinistra), -8 (senso orario), -9, -10, -11 (cardinali e intercardinali). I nomi dei venti tornano in meteorologia (lezione 7) e nel Portolano.')

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
sec('bussola', head('Orientarsi · lo strumento','La bussola magnetica'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Bussola vista dall\'alto dentro la sagoma della barca: la rosa è girata e la linea di fede, allineata alla prua, indica la prora')+lbl,
 notes='Quiz 1.7.4-14 e -29 (rosa ed equipaggio magnetico), -12, -30, -46 (gli aghi puntano al Nord bussola), -33 (rosa da 0 a 360 in senso orario dal Nb), -31, -41, -44, -45 (linea di fede parallela all\'asse longitudinale, sotto si legge la prora), -36 (mantiene la prora), -28 (liquido), -49 (sospensione cardanica), -15 (a cosa serve la bussola). Il quiz 1.7.4-13 è oscurato. Nel disegno la barca ha prora bussola di circa 035°. Perché la bussola non indica il Nord vero: declinazione e deviazione, capitolo 4.')

# ============ STRUMENTI ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=''.join(line(30,y,1062,y,'#E4DCC8',2) for y in (160,300,440))+''.join(line(x,30,x,590,'#E4DCC8',2) for x in (260,520,780))
def tri(dx,dy,rot,op):
    arc=' '.join(f'M{330+150*math.cos(math.radians(a)):.1f} {540-150*math.sin(math.radians(a)):.1f} L{330+(150-(16 if a%30==0 else 8))*math.cos(math.radians(a)):.1f} {540-(150-(16 if a%30==0 else 8))*math.sin(math.radians(a)):.1f}' for a in range(0,181,10))
    return (f'<g transform="translate({dx} {dy}) rotate({rot} 330 425)"><path d="M100 540 L560 540 L330 310 Z" fill="#BFE6EA" fill-opacity="{op}" stroke="{SEA}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M180 540 A150 150 0 0 1 480 540" fill="none" stroke="{NAVY}" stroke-width="3"/><path d="{arc}" stroke="{NAVY}" stroke-width="2"/></g>')
b+=tri(-20,20,0,0.75)+tri(70,-120,-14,0.55)
b+=f'<path d="M846 120 L760 520 L770 522 L852 128 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/><path d="M854 120 L940 520 L930 522 L848 128 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<rect x="836" y="70" width="28" height="44" rx="8" fill="{NAVY}"/><circle cx="850" cy="124" r="14" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
b+=dash(765,540,935,540,CORAL,3)
b+=f'<g transform="rotate(-28 640 150)"><rect x="560" y="138" width="190" height="24" rx="4" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/><path d="M750 138 L786 150 L750 162 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3"/><path d="M774 146 L786 150 L774 154 Z" fill="{NAVY}"/><rect x="530" y="138" width="30" height="24" rx="4" fill="{CORAL_T}" stroke="{NAVY}" stroke-width="3"/></g>'
X=128
lbl=lab(X+120,Y+556,420,'Squadrette nautiche',SEA,26,900)+lab(X+900,Y+190,160,'Compasso a punte secche',NAVY,24,900)+lab(X+470,Y+40,300,'Matita morbida e gomma',INK,24,900)
txt=term('Squadrette nautiche','Usate in coppia come parallele: tracciano rotte e rilevamenti e li portano al centro della rosa per leggerli.')+term('Compasso a punte secche','Misura le distanze e riporta le coordinate.')+term('Matita e gomma','Matita morbida, tratto leggero: la carta si usa e si cancella.')+term('Obbligatori','A bordo oltre le 12 miglia dalla costa.')
sec('strumenti', head('Orientarsi · il carteggio','Gli strumenti del carteggio'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Su una carta nautica: due squadrette nautiche con goniometro usate come parallele, un compasso a punte secche, una matita e una gomma')+lbl,
 notes='Quiz 1.7.5-18 (squadrette e parallele), -19 (compasso: distanze e coordinate), 1.7.2-30 (compasso a punte secche per non rovinare la carta), -71 (strumenti obbligatori oltre 12 miglia). Portare in aula squadrette e compasso: da qui in poi ogni lezione ha un po\' di carteggio.')
X=700

# ============ ROTTE E COORDINATE ============
PXL=30; PYL=40.4   # pixel per primo di longitudine e di latitudine (Mercatore a 42°)
def cxy(lat,lon): return (300+(lon-600)*PXL, 520-(lat-2530)*PYL)   # lat e lon in primi: 42°10′ = 2530′, 010°00′ = 600′
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<path d="M30 590 L30 380 Q90 400 120 470 Q150 540 260 590 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
for k in range(8): b+=f'<rect x="30" y="{60+k*62:.0f}" width="22" height="62" fill="{NAVY if k%2 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="2"/>'
for k in range(10): b+=f'<rect x="{60+k*100:.0f}" y="568" width="100" height="22" fill="{NAVY if k%2 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="2"/>'
for xx in (300,600,900): b+=line(xx,30,xx,568,GRID,2)
for yy in (520,318,116): b+=line(52,yy,1062,yy,GRID,2)
A=cxy(2531,598); Bq=cxy(2539,619)
RC=(720,420); RRo=78
b+=f'<circle cx="{RC[0]}" cy="{RC[1]}" r="{RRo}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
b+='<path d="'+' '.join(f'M{pol(*RC,a,RRo)[0]:.1f} {pol(*RC,a,RRo)[1]:.1f} L{pol(*RC,a,RRo-(14 if a%30==0 else 7))[0]:.1f} {pol(*RC,a,RRo-(14 if a%30==0 else 7))[1]:.1f}' for a in range(0,360,10))+f'" stroke="{NAVY}" stroke-width="2"/>'
b+=f'<path d="M{RC[0]} {RC[1]-60} L{RC[0]+8} {RC[1]} L{RC[0]} {RC[1]+60} L{RC[0]-8} {RC[1]} Z" fill="{NAVY}" fill-opacity="0.5"/>'
rv=math.degrees(math.atan2(Bq[0]-A[0],A[1]-Bq[1]))
e=pol(*RC,rv,RRo); b+=dash(RC[0],RC[1],e[0],e[1],CORAL,4)+f'<circle cx="{e[0]:.1f}" cy="{e[1]:.1f}" r="8" fill="{CORAL}"/>'
b+=arrow(A[0],A[1],Bq[0],Bq[1],CORAL,6,26)
for q in (A,Bq): b+=f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="11" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
m=((A[0]+Bq[0])/2,(A[1]+Bq[1])/2); b+=arrow(m[0]+40,m[1]+60,RC[0]-40,RC[1]-60,SEA,4,18)
lbl=(lab(X+A[0]-30,Y+A[1]+18,330,'A · 42°11′ N · 009°58′ E',NAVY,24,900,bg='#FFFFFF')+lab(X+Bq[0]-400,Y+Bq[1]-56,380,'B · 42°19′ N · 010°19′ E',NAVY,24,900,'right',bg='#FFFFFF')
     +lab(X+60,Y+500,110,'10′',NAVY,24,900)+lab(X+60,Y+298,110,'15′',NAVY,24,900)+lab(X+60,Y+96,140,'42°20′ N',NAVY,24,900)
     +lab(X+310,Y+40,160,'010° E',NAVY,24,900)+lab(X+610,Y+40,120,'10′',NAVY,24,900)+lab(X+910,Y+40,120,'20′',NAVY,24,900)
     +lab(X+e[0]+16,Y+e[1]-30,140,f'Rv {rv:03.0f}°',CORAL,28,900,bg='#FFFFFF')+lab(X+RC[0]-100,Y+RC[1]+RRo+6,200,'rosa della carta',SOFT,24,800,'center')+lab(X+m[0]-110,Y+m[1]+70,240,'squadrette',SEA,24,900))
txt=(term('Latitudine φ','Sulle scale verticali, ai lati della carta: da 0° a 90° N o S.')
     +term('Longitudine λ','Sulle scale orizzontali, in alto e in basso: da 0° a 180° E o W.')
     +term('Tracciare la rotta','Unisci partenza e arrivo; con le squadrette porta la direzione al centro della rosa e leggi Rv sul cerchio graduato.')
     +term('Rv 090° e Rv 180°','A 090° cambia solo la longitudine, a 180° solo la latitudine.'))
sec('coordinate', head('Orientarsi · sulla carta','Rotte e coordinate')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Carta nautica con le scale di latitudine e longitudine, due punti A e B con le loro coordinate, la rotta da A a B e la stessa direzione portata al centro della rosa della carta, dove si legge la rotta vera')+lbl,
 notes=f'Due punti con le coordinate: A 42°11′N 009°58′E, B 42°19′N 010°19′E. Dalla carta: Rv {rv:03.0f}° e circa 17,5 miglia (Δφ 8′, appartamento 21′ × cos 42° ≈ 15,6′). Le coordinate si riportano col compasso dalle scale ai lati e in basso. Quiz 1.7.5-19 (compasso per le coordinate), 1.7.7-6 e -7 (Rv 090 cambia solo la longitudine, Rv 180 solo la latitudine), -9 (la rotta si legge sulla rosa della carta), -5 (rotte opposte: 180°). Il carteggio vero e proprio si fa dalla lezione 8.')

# ================= CAPITOLO 2 · STIMA E CALCOLI =================
chapter('cap2',2,'Navigazione stimata e primi calcoli',['La navigazione stimata','Misurare le miglia','Miglia, velocità, tempo','Tre esempi svolti','Carburante e riserva'],SEA,
 'Circa 14 minuti, compresa una verifica da 2 quiz alla fine. Quiz 2-4 nella raccolta finale.','circa 14 minuti · 5 argomenti',1,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
# ============ NAVIGAZIONE STIMATA ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<path d="M30 500 Q120 470 170 520 Q200 590 30 590 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
DR=[(200,480),(390,370),(580,260),(770,150)]; RL=[(200,480),(410,400),(620,320),(830,240)]
b+=f'<path d="M{DR[0][0]} {DR[0][1]} L{DR[-1][0]} {DR[-1][1]}" stroke="{NAVY}" stroke-width="5"/>'
b+=dpath('M'+' L'.join(f'{a} {b_}' for a,b_ in RL),SOFT,4)
for i,(x,y) in enumerate(DR[1:],1):
    r=22+i*24; b+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CORAL}" fill-opacity="0.1" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>'
for x,y in DR: b+=f'<circle cx="{x}" cy="{y}" r="11" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><circle cx="{x}" cy="{y}" r="3" fill="{NAVY}"/>'
b+=topboat(860,236,90,-21,'#FFFFFF',NAVY,3)
for yy in (420,480): b+=arrow(880,yy,990,yy+40,'#97A6B4',7,22)
lbl=lab(X+120,Y+500,240,'Partenza · 09:00',NAVY,24,800)+lab(X+290,Y+330,110,'10:00',NAVY,24,800)+lab(X+470,Y+210,110,'11:00',NAVY,24,800)+lab(X+400,Y+80,260,'12:00 · punto stimato',CORAL,24,900,'right')
lbl+=lab(X+850,Y+180,220,'posizione reale',SOFT,24,800)+lab(X+840,Y+540,220,'vento e corrente',SOFT,24,800)+lab(X+460,Y+400,240,'zona di incertezza',CORAL,24,800)
txt=term('Il punto stimato','Una posizione approssimata: si ricava da prora vera, velocità, punto di partenza e tempo trascorso.')+term('Gli strumenti','Bussola, solcometro e orologio. GPS e radar non danno un punto stimato.')+term('Perché si sbaglia','Scarroccio, deriva, declinazione, deviazione: l\'incertezza cresce col tempo.')
sec('stimata', head('Primi calcoli','La navigazione stimata')+col(txt+note('Insostituibile, ma da confermare con un punto nave.',CORAL,36)), pinned=svgp(X,Y,W,Hh,b,'Rotta stimata con i punti orari e cerchi di incertezza sempre più grandi; la posizione reale si allontana per effetto di vento e corrente')+lbl,
 notes='Quiz 1.7.5-9 e -28 (punto stimato), -30 (elementi: Pv, velocità, posizione iniziale, tempo), -23 (bussola, solcometro, orologio), -1 (GPS e radar non danno posizione stimata), -11 e -22 (cause di errore), -3 e -12 (zona di incertezza), -29 (insostituibile ma insufficiente), -36 (punto nave con almeno due luoghi di posizione: capitolo 5), -2 e -10 (si risolve graficamente sulla carta di Mercatore).')

# ============ MISURARE LE MIGLIA ============
def divider(ax,ay,p1,p2,c='#9AA5B1'):
    s=''
    for qx,qy in (p1,p2):
        a=math.atan2(qy-ay,qx-ax); nx,ny=-math.sin(a)*5,math.cos(a)*5
        s+=f'<path d="M{ax+nx:.1f} {ay+ny:.1f} L{qx:.1f} {qy:.1f} L{ax-nx:.1f} {ay-ny:.1f} Z" fill="{c}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
    return s+f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="14" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
SX=960; Y0=550; PM=62.5   # scala delle latitudini: 62,5 px per primo
for k in range(8): b+=f'<rect x="{SX}" y="{Y0-(k+1)*PM:.1f}" width="34" height="{PM:.1f}" fill="{NAVY if k%2 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="2"/>'
b+='<path d="'+' '.join(f'M{SX-(14 if t%10==0 else 7)} {Y0-t*PM/10:.1f} L{SX} {Y0-t*PM/10:.1f}' for t in range(0,81))+f'" stroke="{NAVY}" stroke-width="2"/>'
b+=line(SX+34,40,SX+34,580,GRID,2)+line(SX,40,SX,580,NAVY,2)
A1=(170,480); B1=(500,254); L=math.dist(A1,B1)
b+=f'<path d="M80 300 Q160 250 140 160 Q120 80 200 50 L30 50 L30 300 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=line(*A1,*B1,CORAL,5)+''.join(f'<circle cx="{q[0]}" cy="{q[1]}" r="10" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>' for q in (A1,B1))
b+=divider(188,152,A1,B1)
y1=Y0-1.0*PM; y2=y1-L
b+=divider(790,(y1+y2)/2,(SX-2,y1),(SX-2,y2))
b+=f'<path d="M{SX-40} {y1:.1f} H{SX-60} V{y2:.1f} H{SX-40}" fill="none" stroke="{CORAL}" stroke-width="5"/>'
b+=f'<path d="M330 160 Q560 40 740 200" fill="none" stroke="{SEA}" stroke-width="5" stroke-dasharray="12 8"/>'+head_at(740,200,50,SEA,22)
lbl=''.join(lab(X+SX+40,Y+Y0-k*PM-16,80,f'{10+k}′',NAVY,24,900) for k in range(0,9,2))
lbl+=lab(X+A1[0]-20,Y+A1[1]+20,60,'A',NAVY,30,900)+lab(X+B1[0]+20,Y+B1[1]-10,60,'B',NAVY,30,900)
lbl+=lab(X+SX-560,Y+(y1+y2)/2+90,250,f'{L/PM:.1f}′ = {L/PM:.1f} miglia'.replace('.',','),CORAL,28,900,'right',bg='#FFFFFF')+lab(X+480,Y+70,300,'stessa apertura',SEA,26,900,'center')
lbl+=lab(X+870,Y+580,240,'scala delle latitudini',NAVY,24,900,'right')
mi=f'{L/PM:.1f}'.replace('.',',')
txt=(term('1 · Apri il compasso','Una punta sulla partenza, l\'altra sull\'arrivo. Non cambiare più l\'apertura.')
     +term('2 · Portalo sulla scala','La scala delle latitudini, ai lati della carta: indifferentemente a destra o a sinistra, all\'altezza del tratto misurato.')
     +term('3 · Leggi miglia e decimi','1′ di latitudine = 1 miglio = 1852 m. Ogni tacca piccola è 0,1 miglio.'))
sec('misura', head('Primi calcoli · il compasso','Misurare le miglia')+col(txt+note('Mai la scala delle longitudini!',CORAL,38),540,20), pinned=svgp(X,Y,W,Hh,b,'Il compasso a punte secche misura il tratto da A a B e, con la stessa apertura, viene riportato sulla scala delle latitudini a destra della carta, dove si leggono le miglia')+lbl,
 notes=f'Nel disegno il tratto AB misura {mi} miglia. Quiz 1.7.5-33 e -52 (distanza sulla scala delle latitudini, alla stessa latitudine), 1.7.2-37 (misura della distanza), 1.7.5-26 (il miglio è l\'unità delle distanze), 1.7.5-19 (compasso). Se il tratto è più lungo dell\'apertura comoda, si apre il compasso su un numero tondo (per es. 5 miglia) e lo si fa «camminare» lungo la rotta. Sulla carta di Mercatore la scala cresce verso i poli: per questo si misura all\'altezza del tratto.')

# ============ MIGLIA, VELOCITÀ, TEMPO ============
b=f'<path d="M280 30 L30 450 L530 450 Z" fill="{SUN_T}" stroke="{SUN}" stroke-width="10" stroke-linejoin="round"/>'
b+=f'<circle cx="280" cy="290" r="54" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/>'
TX=128
lbl=(big(TX+200,Y+90,160,'M',CORAL,120)+big(TX+60,Y+330,140,'V',SEA,100)+big(TX+340,Y+330,160,'Tᵐ',PURPLE,100)+big(TX+250,Y+350,60,'×',INK,70)
     +big(TX+230,Y+258,100,'60',NAVY,52)+big(TX+60,Y+170,80,':',INK,90)+big(TX+420,Y+170,80,':',INK,90))
def fcard(f,c,u,ex):
    return f'<div style="display:flex; align-items:center; gap:22px; background:#FFFFFF; {SHADOW}; padding:18px 24px; border-radius:26px"><p style="font-family:{H}; font-size:46px; font-weight:700; color:#FFFFFF; background:{c}; padding:10px 26px; border-radius:40px; flex:none">{f}</p><div style="display:flex; flex-direction:column; gap:2px">{p(u,26,INK,800)}{p(ex,24,BODY)}</div></div>'
right=(fcard('M = V × Tᵐ : 60',CORAL,'miglia','prima × poi :')+fcard('V = M : Tᵐ × 60',SEA,'nodi (miglia all\'ora)','prima : poi ×')+fcard('Tᵐ = M : V × 60',PURPLE,'tempo in minuti','prima : poi ×')
       +'<div style="display:flex; gap:12px; flex-wrap:wrap">'+''.join(f'<p style="font-size:26px; font-weight:800; color:{INK}; background:{LILAC_T}; padding:10px 18px; border-radius:18px">{t}</p>' for t in ('1 h = 60′','2 h 30′ = 150′','154′ = 2 h 34′'))+'</div>')
sec('formula', head('Primi calcoli · il triangolo','Miglia, velocità, tempo')+f'<div style="position:absolute; left:748px; top:290px; width:1044px; display:flex; flex-direction:column; gap:22px">{right}</div>', pinned=svgp(TX,Y,560,480,b,'Il triangolo con M in alto, V e T in minuti in basso uniti dal per, i due lati con il diviso e 60 al centro')+lbl+note('Se metti prima il «:» poi va il «×», e viceversa',CORAL,36).replace('<p style="','<p style="position:absolute; left:'+str(TX+10)+'px; top:790px; width:560px; ',1),
 notes='Metodo della scuola: il tempo sempre in minuti (Tᵐ) e il 60 al centro del triangolo. Si copre la lettera che si cerca: coprendo M resta V × Tᵐ, poi : 60; coprendo V resta M : Tᵐ, poi × 60; coprendo Tᵐ resta M : V, poi × 60. Il risultato in minuti si riporta in ore e minuti dividendo per 60 (154′ = 2 h 34′). Chi preferisce le ore e decimi usa M = V × T con T in ore: il risultato è lo stesso. Quiz 1.7.5-13, -14, -25, -51 (nodo = un miglio all\'ora), -15, -16, -17 (le tre formule), -26 (miglio per le distanze), -35 (ricalcolare a ogni cambio di velocità), -54 (4,4 h = 4 h 24′).')

# ============ ESEMPI ============
def ex(qid,prob,steps,res,c,bg):
    st=''.join(p(s,25,BODY) for s in steps)
    return card(note(f'Quiz {qid}',c,34)+p(prob,27,INK,800,1.3)+f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:22px">{st}</div>'+f'<p style="font-family:{H}; font-size:52px; font-weight:700; color:{c}">{res}</p>',None,28,14)
e1=ex('1.7.5-31','15 nodi per 45 minuti: quante miglia?',['M = V × Tᵐ : 60','15 × 45 = 675','675 : 60 = <b>11,25</b>'],'11,25 miglia',CORAL,CORAL_T)
e2=ex('1.7.5-65','18 miglia a 7 nodi: quanto tempo?',['Tᵐ = M : V × 60','18 : 7 × 60 ≈ <b>154′</b>','154′ = 2 h e 34′'],'2 h 34′',SEA,SEA_T)
e3=ex('1.7.5-63','24,5 miglia in 3 h 30′: che velocità?',['3 h 30′ = <b>210′</b>','V = M : Tᵐ × 60','24,5 : 210 × 60 = <b>7</b>'],'7 nodi',PURPLE,LILAC_T)
sec('esempi', head('Primi calcoli','Tre esempi svolti')+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}</div>'+note('Prima porta il tempo in minuti, poi applica la formula.',BLUE,38),
 notes='Esempi dai quiz ufficiali: 1.7.5-31 (15 kn, 45′ → 11,25 mg), -65 (18 mg, 7 kn → 2 h 34′), -63 (3 h 30′, 24,5 mg → 7 kn; attenzione, nell\'elenco il numero 1.7.5-63 compare due volte). Altri da fare alla lavagna: -39 (9 kn, 45′ → 6,75), -41, -57 (11,6 mg a 6 kn → 116′ = 1 h 56′), -60 (6 kn, 2 h 45′ = 165′ → 16,5), -64 (2 h 20′ = 140′ a 12 kn → 28 mg).')

# ============ CARBURANTE E RISERVA ============
def fbox(t,f,ex,c,bg):
    return f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:24px; border-radius:28px">{tag(t,c)}<p style="font-family:{H}; font-size:38px; font-weight:700; line-height:1.15; color:{INK}">{f}</p>{p(ex,24,BODY)}</div>'
row1=(fbox('Carburante totale','l/h × T × 1,3','consumo orario per il tempo in ore, più il 30% di riserva',CORAL,CORAL_T)
      +fbox('Sola riserva','l/h × T : 100 × 30','il 30% del consumo del viaggio',SEA,SEA_T)
      +fbox('Consumo dalla potenza','g/CV/h × CV : peso specifico','300 g × 80 CV : 750 g/l = <b>32 l/h</b> (quiz 1.2.3-2)',PURPLE,LILAC_T))
boxes=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{bg}; padding:16px; border-radius:22px">{p(a,24,SOFT,800)}<p style="font-family:{H}; font-size:40px; font-weight:700; color:{INK}">{b_}</p>{p(c,24)}</div>' for a,b_,c,bg in [('1 · tempo','3 h','90 : 30 × 60 = 180′',BLUE_T),('2 · consumo','84 litri','28 l/h × 3',LILAC_T),('3 · riserva','≈ 25 litri','84 : 100 × 30 = 25,2',SEA_T),('4 · totale','≈ 109 litri','84 × 1,3 = 109,2',CORAL_T)])
exm=card(note('Quiz 1.2.3-15 · 90 miglia a 30 nodi, consumo 28 l/h',CORAL,34)+f'<div style="display:flex; gap:14px">{boxes}</div>',None,26,12)
sec('carburante', head('Primi calcoli · prima di partire','Carburante e riserva')+f'<div style="display:flex; gap:20px">{row1}</div>'+exm
 +p('Il 30% copre vento e corrente contrari; mare mosso, dislocamento e velocità alta riducono l\'autonomia. All\'esame di carteggio la risposta è un intervallo (5.1.2-3: «13÷15 litri»).',25,INK),
 notes='Formule della scuola: carburante totale = consumo orario × tempo × 1,3; sola riserva = consumo orario × tempo : 100 × 30. Il tempo si ricava con Tᵐ = M : V × 60. Quiz 1.2.3-1 (riserva del 30%), -2 (consumo dalla potenza: 300 g/CV/h × 80 CV = 24 kg/h, : 0,75 kg/l = 32 l/h), -15, -16, -17 (sola riserva: 90 mg a 30 kn, 28 l/h → 25 litri; 84 mg a 21 kn → 4 h; 100 mg a 40 kn → 2,5 h). Esercizi di carteggio sul carburante: famiglie 5.x.2 (lezione 11), con le risposte ufficiali a intervallo, per es. 5.1.2-1 «29÷31 litri», 5.1.2-2 «19÷21 litri».')

# ================= CAPITOLO 3 · PRORA, ROTTA, VENTO E CORRENTE =================
chapter('cap3',3,'Prora e rotta, vento e corrente',['Rotta vera e prora vera','Lo scarroccio','La deriva','Angoli di scarroccio e deriva','Moto proprio e moto effettivo','Vento «da», corrente «verso»'],PURPLE,
 'Circa 12 minuti, compresa una verifica da 2 quiz alla fine. Quiz 5 nella raccolta finale.','circa 12 minuti · 6 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
# ============ ROTTA VERA E PRORA VERA
X=128
ox,oy=200,540
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<path d="M30 430 Q110 450 150 510 Q180 570 260 590 L30 590 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=arrow(ox,oy,ox,60,NAVY,5,22)
PVa,RVa=35,58
rv=pol(ox,oy,RVa,720); b+=dpath(f'M{ox} {oy} L{rv[0]:.0f} {rv[1]:.0f}',CORAL,6)+head_at(rv[0],rv[1],RVa-90,CORAL,24)
b+=curved(ox,oy,150,-90,PVa-90,NAVY,4)+curved(ox,oy,250,-90,RVa-90,CORAL,4)
for t in (0.3,0.6,0.88):
    bx,by=pol(ox,oy,RVa,720*t)
    b+=topboat(bx,by,110,PVa-90,'#FFFFFF',NAVY,3)
    tip=pol(bx,by,PVa,130); b+=arrow(*pol(bx,by,PVa,58),tip[0],tip[1],NAVY,5,18)
b+=''.join(arrow(x,y,x+90,y+55,GREY,7,22) for x,y in ((700,400),(800,460),(880,360)))
pa=pol(ox,oy,PVa/2,175); ra=pol(ox,oy,25,270)
lbl=(lab(X+ox-40,Y+20,80,'N',NAVY,30,900,'center')+lab(X+ox-250,Y+130,230,'meridiano geografico',NAVY,24,800,'right')
     +lab(X+pa[0]-10,Y+pa[1]-40,100,'Pv',NAVY,28,900)+lab(X+ra[0]-20,Y+ra[1]-50,200,'Rv · azimut',CORAL,28,900)
     +lab(X+rv[0]-20,Y+rv[1]+70,250,'percorso sul fondo',CORAL,24,900)+lab(X+800,Y+520,220,'vento e corrente',SOFT,24,800))
txt=(term('Rotta vera Rv','L\'angolo tra il Nord vero (meridiano geografico) e il percorso sul fondo, da 000° a 360° in senso orario: è un azimut.')
     +term('Prora vera Pv','L\'angolo tra il Nord vero e la linea di chiglia: dove punta la prua.')
     +term('Sulla carta','Si leggono sulla rosa della carta; due rotte opposte differiscono di 180°.')
     +term('Quando coincidono','Pv = Rv senza vento e corrente, o con vento e corrente esattamente di prora o di poppa.'))
sec('prorarotta', head('Carteggio · le parole','Rotta vera e prora vera'), pinned=pcol(txt,gap=18)+svgp(X,Y,W,Hh,b,'Una barca parte dalla costa tenendo sempre la stessa prora vera, frecce scure parallele, ma vento e corrente la spostano: il percorso sul fondo, la rotta vera, si apre a destra; gli angoli si contano dal meridiano geografico')+lbl,
 notes='Nel disegno la barca tiene sempre Pv 035° (le frecce scure sono parallele), ma il percorso sul fondo è Rv 058°. Quiz 1.7.7-4 e -8 (prora), -1, -2, -3 (rotta vera), -5 (rotte opposte 180°), -9 (si legge sulla rosa della carta), -30 (Pv = Rv solo con vento o corrente da prora o da poppa), -28 (vento in poppa: cambia la velocità, non la direzione). Il quiz 1.7.7-10 è oscurato.')
X=700

# ============ SCARROCCIO ============
ox,oy=520,560
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=''.join(arrow(80,y,220,y,GREY,8,24) for y in (160,260,360))
b+=arrow(ox,oy,ox,90,NAVY,7,26)
rv=pol(ox,oy,14,500); b+=dpath(f'M{ox} {oy} L{rv[0]:.0f} {rv[1]:.0f}',CORAL,6)
b+=curved(ox,oy,300,-90,-76,CORAL,5)
for k,(t) in enumerate((0.3,0.6)):
    x,y=ox+(rv[0]-ox)*t,oy+(rv[1]-oy)*t; b+=topboat(x,y,130,-90,'#FFFFFF',NAVY,3,0.9 if k else 0.5,k==1)
lbl=lab(X+60,Y+420,240,'vento da 270°',SOFT,26,900)+lab(X+ox-240,Y+80,220,'Pv 000°',NAVY,28,900,'right')+lab(X+rv[0]+10,Y+rv[1]+10,220,'Rv 014°',CORAL,28,900)+lab(X+ox+110,Y+200,260,'scarroccio +14°',CORAL,26,900,bg='#FFFFFF')
txt=(term('Cos\'è','Lo spostamento laterale dovuto al vento: l\'angolo tra prora e rotta.')
     +term('Il vento «viene»','Vento 180° viene da 180°, da Sud. Conta il vento apparente, che spinge sull\'opera morta.')
     +term('Da cosa dipende','Forza del vento, velocità e tipo di carena: più opera morta e meno opera viva, più scarroccio. Tocca tutte le barche.'))
sec('scarroccio', head('Carteggio · il vento','Lo scarroccio')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Barca con prora a Nord spinta da un vento da Ovest: la rotta vera piega a destra di 14 gradi')+lbl,
 notes='Quiz 1.7.7-12 e -26 (scarroccio dovuto al vento), -19 e -23 (da cosa dipende: meno opera viva e più superficie esposta, più scarroccio), -21 (tocca tutte le unità), -20 (vento apparente, somma vettoriale), -22 (vento 180 soffia verso Nord). Il segno: nella slide degli angoli.')

# ============ DERIVA
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<rect x="150" y="80" width="760" height="410" rx="40" fill="{WATER}" fill-opacity="0.22" stroke="{SEA}" stroke-width="4" stroke-dasharray="14 10"/>'
b+=''.join(f'<path d="M{x} {y} q18 -10 36 0 t36 0" fill="none" stroke="{SEA}" stroke-width="4" stroke-linecap="round" opacity="0.6"/>' for x,y in ((200,140),(420,470),(640,150),(780,440),(260,330)))
b+=f'<rect x="150" y="500" width="760" height="40" rx="20" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/>'+''.join(f'<circle cx="{x}" cy="520" r="14" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>' for x in range(190,900,90))
for (x,y,L,h) in ((260,200,150,0),(300,420,100,60),(470,300,80,300)):
    b+=topboat(x,y,L,h-90,'#FFFFFF',NAVY,3,0.3,False)+topboat(x+300,y,L,h-90,'#FFFFFF',NAVY,3)
    b+=arrow(x+60,y+50,x+250,y+50,SEA,6,22)
b+=arrow(940,300,1040,300,SEA,10,30)
lbl=lab(X+920,Y+200,150,'corrente<br>090°',SEA,26,900,'center')+lab(X+330,Y+548,420,'la massa d\'acqua si sposta',NAVY,24,900,'center')+lab(X+300,Y+32,480,'stesso spostamento per tutte',CORAL,26,900,'center')
txt=(term('Cos\'è','Lo spostamento dovuto alla corrente: l\'acqua si muove e porta con sé la barca.')
     +term('La corrente «va»','Corrente 180° va verso 180°, verso Sud. Si dà con direzione e velocità: Dc e Vc.')
     +term('Uguale per tutti','Come un nastro trasportatore: a parità di corrente la deriva non dipende dallo scafo.'))
sec('deriva', head('Carteggio · la corrente','La deriva')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Una massa d\'acqua, come un nastro trasportatore, si sposta verso Est e porta con sé tre barche diverse, con prore diverse, tutte dello stesso tratto')+lbl,
 notes='Quiz 1.7.7-14, -25, -27 (deriva dovuta alla corrente), -24 (moto dovuto alle correnti), -16 (non dipende dallo scafo: è indifferente), -22 (corrente 180 va verso Sud). Primo problema di corrente: lezione 9; esercizi 5.x.1 nelle lezioni 13-15.')

# ============ ANGOLI DI SCARROCCIO E DERIVA ============
def sd_diag(sign):
    s=f'<rect x="0" y="0" width="440" height="280" fill="{CHART}"/>'
    y0=140; s+=topboat(90,y0,100,0,'#FFFFFF',NAVY,3)+arrow(140,y0,420,y0,NAVY,5,20)
    e=(410,y0+90*sign); s+=dpath(f'M140 {y0} L{e[0]-12} {e[1]-4*sign}',CORAL,5)+head_at(e[0],e[1],math.degrees(math.atan2(e[1]-y0,e[0]-140)),CORAL,20)
    ys,ye=(20,90) if sign>0 else (260,190)
    s+=f'<circle cx="250" cy="{ys}" r="9" fill="{GREY}"/>'+arrow(250,ys,250,ye,GREY,7,22)
    s+=arrow(340,ys,340,ye,SEA,7,22)
    return s
def dcard(sign,t,sub):
    return card(svgi(440,280,sd_diag(sign),'Barca con prora 090: '+sub,dw=440,dh=280)+f'<p style="font-family:{H}; font-size:40px; font-weight:700; color:{CORAL}">{t}</p>'+p(sub,24,INK),None,22,8)
c1=dcard(1,'+ a dritta','Pv 090°: vento 000° (viene da N) e corrente 180° (va a S) spingono a destra.')
c2=dcard(-1,'− a sinistra','Pv 090°: vento 180° (viene da S) e corrente 360° (va a N) spingono a sinistra.')
defs=card(term('Angolo di scarroccio','Tra prora e rotta, per effetto del vento.')+term('Angolo di deriva','Tra prora e rotta, per effetto della corrente.')+p('Nei disegni: freccia grigia il vento, azzurra la corrente.',24,SOFT,700)+f'<div style="display:flex; gap:10px; flex-wrap:wrap">{chip("Rv = Pv + α",SEA,30)}{chip("Pv = Rv − α",CORAL,30)}</div>',SEA_T,26,14)
bx=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; background:{bg}; padding:16px 20px; border-radius:22px">{p(a,24,INK,800,1.25)}{p(b_,24)}</div>' for a,b_,bg in [('Rotta N, vento e corrente 180°','agevolata dallo scarroccio, contrastata dalla deriva',SUN_T),('Di prora o di poppa','cambia solo la velocità, non la direzione',BLUE_T),('Vento contro corrente','onda corta e ripida',CORAL_T)])
sec('angoli', head('Carteggio · il segno','Angoli di scarroccio e deriva')+f'<div style="display:flex; gap:22px; align-items:stretch">{defs}{c1}{c2}</div><div style="display:flex; gap:18px">{bx}</div>',
 notes='Il segno vale per tutti e due gli angoli: positivo se la barca va a dritta della prora, negativo se va a sinistra. Nel disegno la grigia è il vento (indicato da dove viene), l\'azzurra la corrente (indicata verso dove va). Quiz 1.7.7-18 (positivo a dritta, negativo a sinistra), -29 (rotta Nord con vento e corrente 180: agevolata dallo scarroccio, contrastata dalla deriva), -28 (vento di poppa: solo velocità), -30 (Pv = Rv solo con vento o corrente di prora o di poppa). Con vento contrario alla corrente il mare si fa corto e ripido (lezione 7). Le formule servono negli esercizi 5.x.4 (lezione 12).')

# ============ MOTO PROPRIO E MOTO EFFETTIVO
X=128
ox,oy=180,520
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
A=pol(ox,oy,40,560); Bp=(A[0]+230,A[1]+110)
b+=arrow(ox,oy,A[0],A[1],NAVY,7,26)+arrow(A[0],A[1],Bp[0],Bp[1],SEA,7,26)+dpath(f'M{ox} {oy} L{Bp[0]-14:.0f} {Bp[1]-8:.0f}',CORAL,6)+head_at(Bp[0],Bp[1],math.degrees(math.atan2(Bp[1]-oy,Bp[0]-ox)),CORAL,24)
b+=topboat(ox+60,oy-70,120,-50,'#FFFFFF',NAVY,4)
b+=''.join(f'<path d="M{x} {y} q18 -10 36 0 t36 0" fill="none" stroke="{SEA}" stroke-width="4" stroke-linecap="round"/>' for x,y in ((760,460),(820,510),(880,460)))
lbl=lab(X+30,Y+290,300,'moto proprio: Pv · Vp',NAVY,26,900,'right')+lab(X+A[0]+60,Y+A[1]-30,300,'corrente: Dc · Vc',SEA,26,900)+lab(X+560,Y+400,360,'moto effettivo: Rv · Ve',CORAL,26,900)
txt=(term('Moto proprio','Pv e Vp: dato dalle sole eliche (o dalle vele), rispetto all\'acqua.')
     +term('Moto effettivo','Rv e Ve: eliche più vento e corrente, rispetto al fondo del mare. È il percorso reale.')
     +term('Il triangolo','Moto proprio + moto della corrente = moto effettivo: sulla carta si sommano come vettori.'))
sec('moto', head('Carteggio · rispetto all\'acqua e al fondo','Moto proprio e moto effettivo'), pinned=pcol(txt+note('Si risolve sulla carta nelle lezioni 9, 13, 14 e 15.',SEA,34))+svgp(X,Y,W,Hh,b,'Triangolo delle velocità: prora e velocità propulsiva, poi il vettore della corrente, e la risultante che è la rotta e la velocità effettive')+lbl,
 notes='Quiz 1.7.7-11 e -15 (moto e velocità propri: sole eliche), -17 (Ve rispetto al fondo), -13 (moto effettivo: Rv e Ve), -24 (moto dovuto alle correnti), -20 (vento apparente, somma vettoriale). Primo problema di corrente: lezione 9; esercizi 5.x.1 nelle lezioni 13-15.')
X=700

# ============ VENTO DA, CORRENTE VERSO ============
def wind_cur():
    s=f'<rect x="0" y="0" width="460" height="300" fill="{CHART}"/>'
    s+=arrow(120,40,120,250,GREY,10,30)+f'<circle cx="120" cy="30" r="10" fill="{GREY}"/>'
    s+=arrow(340,40,340,250,SEA,10,30)
    return s
wc=card(svgi(460,300,wind_cur(),'A sinistra il vento che arriva da Nord e va verso Sud; a destra la corrente che va verso Sud',dw=440,dh=287)
        +p('<b>Vento 000°</b> (Tramontana) arriva da Nord e soffia verso Sud. <b>Corrente 180°</b> va verso Sud.',25,INK),None,26,12)
exx=card(note('Esercizio 5.1.4-2',CORAL,36)+p('Voglio <b>Rv = 090°</b> con un vento di <b>Grecale</b> che dà <b>Sc = +10°</b>. Che prora tengo?',27,INK,700)
        +f'<div style="display:flex; flex-direction:column; gap:6px; background:{CORAL_T}; padding:18px; border-radius:22px">{p("Pv = Rv − Sc",25)}{p("Pv = 090° − 10°",25)}</div>'
        +f'<p style="font-family:{H}; font-size:52px; font-weight:700; color:{CORAL}">Pv = 080°</p>'+p('Si «orza»: si mette la prua un po\' verso il vento.',24),None,28,12)
rules=card(note('Da ricordare',PURPLE,36)+'<ul style="font-size:25px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:12px"><li>Il vento si indica <b>da dove viene</b>, la corrente <b>verso dove va</b>.</li><li>Vento 180° e corrente 180°: il vento spinge verso Nord, la corrente verso Sud.</li><li>Per tenere la rotta si corregge la prora dalla parte opposta allo spostamento.</li></ul>',None,28,12)
sec('regole', head('Carteggio · attenzione ai versi','Vento «da», corrente «verso»')+f'<div style="display:flex; gap:24px">{wc}{exx}{rules}</div>',
 notes='Quiz 1.7.7-22 (vento 180 soffia verso nord, corrente 180 va verso sud), -29 (rotta Nord con vento e corrente 180: scarroccio favorevole, deriva contraria). Esempio dall\'esercizio ufficiale 5.1.4-2: Rv 090°, Grecale, Sc +10° → Pv 080°. Il Grecale da NE spinge la barca verso Sud, cioè a dritta rispetto a una prora a Est: per questo lo scarroccio è positivo.')

# ================= CAPITOLO 4 · DECLINAZIONE E DEVIAZIONE =================
chapter('cap4',4,'Declinazione e deviazione',['La declinazione magnetica','La deviazione magnetica','La tabella delle deviazioni','Da bussola a vero e ritorno'],BLUE,
 'Circa 11 minuti, compresa una verifica da 2 quiz alla fine. Quiz 6 nella raccolta finale.','circa 11 minuti · 4 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
def mini_n(cx,cy,ang,c2,l2,txt_c=None):
    s=arrow(cx,cy,cx,cy-190,NAVY,6,22)+arrow(cx,cy,*pol(cx,cy,ang,190),c2,6,22)
    p0=pol(cx,cy,0,120); p1=pol(cx,cy,ang,120)
    s+=f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A120 120 0 0 {1 if ang>0 else 0} {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{c2}" stroke-width="5"/>'
    return s
def mini_l(cx,ang,n2,c2): t_=pol(cx,300,ang,190); return lab(X+cx-40,Y+60,80,'N'+('v' if n2=='Nm' else 'm'),NAVY,26,900,'center')+lab(X+t_[0]-40,Y+60,80,n2,c2,26,900,'center')
def mini_c(t1,c1,s1,t2,c2,s2): return lab(X+680,Y+360,120,t1,c1,40,900,'center')+lab(X+920,Y+360,120,t2,c2,40,900,'center')+lab(X+640,Y+420,200,s1,INK,24,800,'center')+lab(X+880,Y+420,200,s2,INK,24,800,'center')
# ============ DECLINAZIONE ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
G=(320,330); GR=250
b+=f'<circle cx="{G[0]}" cy="{G[1]}" r="{GR}" fill="#DFF1F8" stroke="{NAVY}" stroke-width="4"/>'
b+=''.join(f'<ellipse cx="{G[0]}" cy="{G[1]}" rx="{rx}" ry="{GR}" fill="none" stroke="{GRID}" stroke-width="2"/>' for rx in (90,180))+line(G[0],G[1]-GR,G[0],G[1]+GR,GRID,2)
b+=f'<ellipse cx="{G[0]}" cy="{G[1]+40}" rx="{GR-6}" ry="60" fill="none" stroke="{GRID}" stroke-width="2"/>'
NV=(G[0],G[1]-GR); NM=(G[0]+70,G[1]-GR+42); OB=(G[0]-90,G[1]+150)
b+=f'<path d="M{OB[0]} {OB[1]} Q{OB[0]-40} {(OB[1]+NV[1])/2} {NV[0]} {NV[1]}" fill="none" stroke="{NAVY}" stroke-width="6"/>'
b+=f'<path d="M{OB[0]} {OB[1]} Q{OB[0]+10} {(OB[1]+NM[1])/2} {NM[0]} {NM[1]}" fill="none" stroke="{SEA}" stroke-width="6" stroke-dasharray="14 8"/>'
b+=f'<circle cx="{NV[0]}" cy="{NV[1]}" r="12" fill="{NAVY}"/><circle cx="{NM[0]}" cy="{NM[1]}" r="12" fill="{SEA}" stroke="#FFFFFF" stroke-width="3"/><circle cx="{OB[0]}" cy="{OB[1]}" r="12" fill="{CORAL}" stroke="#FFFFFF" stroke-width="3"/>'
b+=mini_n(740,300,22,SEA,'Nm')+mini_n(980,300,-22,SEA,'Nm')
b+=f'<rect x="630" y="340" width="440" height="2" fill="{GRID}"/>'
lbl=(lab(X+NV[0]-270,Y+NV[1]-44,240,'Nord geografico',NAVY,24,900,'right')+lab(X+NM[0]+30,Y+NM[1]-66,240,'Nord magnetico',SEA,24,900)
     +lab(X+OB[0]+22,Y+OB[1]-4,140,'tu sei qui',CORAL,24,900,bg='#FFFFFF')+lab(X+OB[0]-150,Y+OB[1]-190,140,'meridiano geografico',NAVY,24,800,'right',bg='#FFFFFF')+lab(X+OB[0]+90,Y+OB[1]-150,150,'meridiano magnetico',SEA,24,800,bg='#FFFFFF')
     +mini_c('d +',SEA,'Nm a Est di Nv','d −',CORAL,'Nm a Ovest di Nv')+mini_l(740,22,'Nm',SEA)+mini_l(980,-22,'Nm',SEA))
txt=(term('Cos\'è','L\'angolo tra meridiano geografico (Nv) e meridiano magnetico (Nm): nasce dal magnetismo terrestre.')
     +term('Valori e segno','Da 0° a 180° Est o Ovest: Est positiva, Ovest negativa.')
     +term('Dove si legge','Sulla rosa della carta, con l\'anno e la variazione annua: va aggiornata.')
     +term('Il Nord magnetico','Lo indica una bussola a terra, o su una barca senza ferri.'))
sec('declinazione', head('Bussola · il magnetismo terrestre','La declinazione magnetica')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Il globo con il polo Nord geografico e il polo Nord magnetico spostato: da dove sei partono il meridiano geografico e quello magnetico, e l\'angolo fra i due è la declinazione; a destra la declinazione positiva verso Est e negativa verso Ovest')+lbl,
 notes='Quiz 1.7.4-17 e -21 (declinazione tra Nv e Nm, meridiano geografico e magnetico), -18, -25, -32, -39 (magnetismo terrestre, varia con luogo e tempo), -22 (si legge sulla carta), -23 (tra 0 e 180 E o W), -34 (Est positiva, Ovest negativa). Aggiornare: sulla carta 5/D «0°20′E 1994 (7′E)»; nel 2008 sono 14 anni × 7′ = 98′ = 1°38′ in più, d = 1°58′E ≈ 2°E (esercizio 5.3.3-2).')

# ============ DEVIAZIONE ============
X=128
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+='<g transform="translate(90 0)">'+topboat(300,320,520,-90,'#FFFFFF',NAVY,4,1,False)
b+=f'<circle cx="300" cy="250" r="44" fill="#DFF1F8" stroke="{NAVY}" stroke-width="4"/><path d="M300 214 L308 250 L300 286 L292 250 Z" fill="{NAVY}"/><path d="M300 214 L308 250 L292 250 Z" fill="{CORAL}"/>'
b+=f'<rect x="258" y="400" width="84" height="70" rx="10" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><rect x="270" y="388" width="60" height="14" rx="4" fill="{NAVY}"/>'
b+=anchor_icon(300,128,1,NAVY)+''.join(f'<circle cx="{300+(k%2)*8-4}" cy="{160+k*10}" r="5" fill="none" stroke="{NAVY}" stroke-width="3"/>' for k in range(5))
b+=f'<rect x="220" y="300" width="40" height="30" rx="6" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'+f'<path d="M260 315 Q300 340 340 318 Q360 306 360 290" fill="none" stroke="{CORAL}" stroke-width="4"/>'
for r in (70,100): b+=f'<circle cx="300" cy="435" r="{r}" fill="none" stroke="{CORAL}" stroke-width="2" stroke-dasharray="6 8" opacity="0.7"/>'
b+='</g>'+mini_n(740,300,-22,CORAL,'Nb')+mini_n(980,300,22,CORAL,'Nb')
b+=f'<rect x="630" y="340" width="440" height="2" fill="{GRID}"/>'
lbl=(lab(X+40,Y+400,250,'motore:<br>ferri duri',NAVY,24,900,'right')+lab(X+440,Y+100,220,'catena:<br>ferri dolci',NAVY,24,900)+lab(X+40,Y+280,250,'strumenti e cavi:<br>campi elettrici',NAVY,24,900,'right')
     +lab(X+446,Y+232,160,'bussola',CORAL,24,900)
     +mini_c('δ −',CORAL,'Nb a Ovest di Nm','δ +',SEA,'Nb a Est di Nm')+mini_l(740,-22,'Nb',CORAL)+mini_l(980,22,'Nb',CORAL))
txt=(term('Cos\'è','L\'angolo tra Nord magnetico e Nord bussola, dovuto al magnetismo di bordo.')
     +term('Le cause','Ferri duri (magnetismo permanente), ferri dolci (magnetismo indotto), campi elettrici di cavi e strumenti.')
     +term('Il segno','Nb a Est di Nm: δ +. Nb a Ovest: δ −. Cambia con la prora.')
     +term('Variazione V','V = d + δ. Su legno o vetroresina senza ferri δ = 0 e V = d.'))
sec('deviazione', head('Bussola · il magnetismo di bordo','La deviazione magnetica'), pinned=pcol(txt,gap=18)+svgp(X,Y,W,Hh,b,'Barca vista dall\'alto con la bussola e intorno le masse che la disturbano: motore, catena dell\'ancora, strumenti e cavi; a destra il Nord bussola a Ovest del Nord magnetico, deviazione negativa, e a Est, deviazione positiva')+lbl,
 notes='Quiz 1.7.4-19 (deviazione tra Nm e Nb), -26 e -40 (ferri duri e dolci, magnetismo di bordo), -42 (varia con la prora), -38 (segno: Nb a Est positivo, a Ovest negativo), -35, -47, -48 (senza masse ferrose Nb = Nm). Tenere lontani dalla bussola telefoni, radio portatili, utensili e casse acustiche.')
X=700

# ============ TABELLA DELLE DEVIAZIONI ============
DEV={0:-2,15:-3,30:-3,45:-4,60:-4,75:-4,90:-5,105:-2,120:-1,135:2,150:2,165:3,180:3,195:4,210:5,225:5,240:3,255:2,270:-1,285:-2,300:-3,315:-3,330:-2,345:-2}
def dv(v): return ('+' if v>0 else ('−' if v<0 else ''))+f'{abs(v)}°'
tiles=''.join(f'<div style="display:flex; flex-direction:column; align-items:center; background:{"#FFFFFF" if v else SUN_T}; {SHADOW}; padding:6px 0px; border-radius:14px"><p style="font-size:24px; font-weight:800; color:{SOFT}">{k:03d}°</p><p style="font-family:{H}; font-size:30px; font-weight:700; color:{SEA if v>0 else (CORAL if v<0 else INK)}">{dv(v)}</p></div>' for k,v in DEV.items())
grid=f'<div style="position:absolute; left:700px; top:290px; width:1092px; display:grid; grid-template-columns:repeat(8,1fr); gap:10px">{tiles}</div>'
CW,CH=1092,300; x0,x1,ym,ys=90,1060,150,22
cb=f'<rect x="0" y="0" width="{CW}" height="{CH}" rx="24" fill="{CHART}"/>'+line(x0,ym,x1,ym,NAVY,3)+''.join(dash(x0+(x1-x0)*k/4,20,x0+(x1-x0)*k/4,280,GRID,2) for k in range(5))
cb+=''.join(line(x0,ym-v*ys,x1,ym-v*ys,'#E4DCC8',2) for v in (-4,4))
pts=list(DEV.items())+[(360,DEV[0])]
cb+='<polyline points="'+' '.join(f'{x0+(x1-x0)*k/360:.1f},{ym-v*ys:.1f}' for k,v in pts)+f'" fill="none" stroke="{PURPLE}" stroke-width="6" stroke-linejoin="round"/>'
cb+=''.join(f'<circle cx="{x0+(x1-x0)*k/360:.1f}" cy="{ym-v*ys:.1f}" r="7" fill="{PURPLE}"/>' for k,v in pts)
curve=svgp(700,610,CW,CH,cb,'Curva delle deviazioni residue: negativa fino a circa 125°, positiva fino a circa 265°, poi di nuovo negativa; massimo più 5 gradi verso 210, minimo meno 5 gradi a 090')
clbl=''.join(lab(700+x0+(x1-x0)*k/4-50,610+CH-40,100,f'{k*90:03d}°',NAVY,24,900,'center') for k in range(5) if k%4)+lab(700+6,610+ym-4*ys-16,80,'+4°',SEA,24,900)+lab(700+6,610+ym+4*ys-16,80,'−4°',CORAL,24,900)
txt=(term('Chi la fa','Il perito compensatore autorizzato dall\'Autorità marittima: compensa la bussola, poi con i giri di bussola annota le deviazioni residue.')
     +term('Quando serve','Con la bussola obbligatoria oltre le 6 miglia. Controllo con un allineamento o con la stella polare.')
     +term('Come si usa','Pm = Pv − d; con la Pm leggi δ; poi Pb = Pm − δ.'))
sec('tabella', head('Bussola · giri di bussola','La tabella delle deviazioni')+col(txt,540,18), pinned=grid+curve+clbl,
 notes='Valori ogni 15° della tabella di deviazione allegata agli esercizi ufficiali di carteggio (DD 131/2022, la stessa per le carte 5/D e 42/D; tabella completa ogni 5° nella lezione 10). Esempio dall\'esercizio 5.3.3-2: Pv 184°, d 2°E → Pm 182° → δ +3° → Pb 179°. Quiz 1.7.4-16 (perito compensatore autorizzato dall\'Autorità marittima), -20, -24, -27, -43 (tabella delle deviazioni residue dopo la compensazione e i giri di bussola), -37 (controllo: allineamento, stella polare). Tra due valori della tabella si interpola o si prende il più vicino.')

# ============ CONVERSIONI ============
formula=f'<div style="display:flex; gap:16px; align-items:center; flex-wrap:wrap">{chip("V = d + δ",PURPLE)}{chip("Pv = Pb + V",SEA)}{chip("Pb = Pv − V",CORAL)}{chip("Est + · Ovest −",NAVY)}</div>'
def exc(tagt,c,bg,rows,res):
    r=''.join(p(x,25,BODY) for x in rows)
    return card(note(tagt,c,34)+f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:22px">{r}</div>'+f'<p style="font-family:{H}; font-size:48px; font-weight:700; color:{c}">{res}</p>',None,28,14)
e1=exc('Esercizio 5.1.3-1',SEA,SEA_T,['Pb = 350°, d = 1° E, δ = 0°','V = +1°','Pv = 350° + 1°'],'Pv = 351°')
e2=exc('Esercizio 5.1.3-2',BLUE,BLUE_T,['Pb = 086°, d = 2° W, δ = −2°','V = −2° − 2° = −4°','Pv = 086° − 4°'],'Pv = 082°')
e3=exc('Al contrario',CORAL,CORAL_T,['Voglio Pv = 120°, V = +3°','Pb = Pv − V','Pb = 120° − 3°'],'Pb = 117°')
sec('conversioni', head('Bussola · il calcolo','Da bussola a vero e ritorno')+formula+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}</div>'+note('Stessa regola per i rilevamenti: Rilv = Rilb + V (lezione 5).',BLUE,38),
 notes='Esempi dagli esercizi ufficiali di carteggio (DD 131/2022): 5.1.3-1 (Pb 350°, d 1°E, δ 0° → Pv 351°) e 5.1.3-2 (Pb 086°, d 2°W, δ −2° → Pv 082°; lì anche Rilb 164° → Rilv 160°, Rilb 194° → Rilv 190°). Regola dei segni: Est positivo, Ovest negativo (quiz 1.7.4-34). In molti esercizi è data direttamente la variazione magnetica V (es. 5.1.2-2 e 5.1.3-3).')

# ================= CAPITOLO 5 · NAVIGAZIONE COSTIERA E PUNTO NAVE =================
LAND_S='#C9A96B'; NIGHT='#0F2238'; LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
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
X=700
chapter('cap5',5,'Navigazione costiera e punto nave',['Navigare in vista della costa','I luoghi di posizione','Punto nave 1 · due punti cospicui','Punto nave 2 · rilevamento e distanza','Punto nave 2 · rilevamenti successivi'],GREEN,
 'Circa 11 minuti, compresa una verifica da 2 quiz alla fine: andare spediti, il dettaglio è nelle note. Quiz 7-9 nella raccolta finale.','circa 11 minuti · 5 argomenti',1,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
# ============ COSTIERA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.18"/>'
b+=f'<path d="M0 0 L1092 0 L1092 150 Q980 190 880 150 Q760 110 640 170 Q520 230 400 160 Q280 100 160 150 Q80 180 0 140 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=tower(250,140,1.3)+bell(780,140,1.1)+f'<rect x="522" y="112" width="26" height="80" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><rect x="516" y="102" width="38" height="14" fill="{NAVY}"/>'
PN=(560,470)
b+=dash(250,90,PN[0]+(PN[0]-250)*0.3,PN[1]+(PN[1]-90)*0.3,SEA,4)+dash(780,100,PN[0]-(780-PN[0])*0.3,PN[1]+(PN[1]-100)*0.3,CORAL,4)
b+=topboat(PN[0]-40,PN[1]+70,120,-60,'#FFFFFF',NAVY,3,0.5,False)
b+=f'<circle cx="{PN[0]}" cy="{PN[1]}" r="16" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="{PN[0]}" cy="{PN[1]}" r="4" fill="{NAVY}"/>'
lbl=lab(X+150,Y+190,200,'Faro',NAVY,24,900,'center')+lab(X+690,Y+190,200,'Campanile',NAVY,24,900,'center')+lab(X+450,Y+200,220,'Torre',NAVY,24,900,'center')+lab(X+600,Y+450,260,'punto nave',NAVY,26,900,bg='#FFFFFF')
txt=(term('Navigazione costiera','Il punto nave si ricava da punti cospicui riconoscibili dal mare: fari, campanili, torri, capi.')
     +term('Cosa serve','Essere in vista della costa, carte a scala adeguata e pubblicazioni per riconoscerla; strumenti affidabili ed esperienza marinaresca.')
     +term('Punti cospicui','Ben visibili, entro 8-10 miglia. Strumenti da carteggio obbligatori oltre le 12 miglia.'))
sec('costiera', head('Carteggio · navigazione costiera','Navigare in vista della costa')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Costa con faro, torre e campanile; due rette di rilevamento partono da due punti cospicui e si incrociano nel punto nave della barca')+lbl,
 notes='Quiz 1.7.6-23 e -41 (navigazione costiera: punti cospicui, vista della costa), -3 e -4 (carte a scala adeguata e pubblicazioni), -7 (punti ben visibili entro 8-10 miglia), -45 (il campanile è un punto cospicuo), -5, -6, -49 (precisione e affidabilità), 1.7.5-71 (strumenti da carteggio obbligatori oltre 12 miglia). L\'esperienza conta: riconoscere un faro di giorno dalla forma e dai colori, di notte dalla caratteristica (lezione 3).')

# ============ LUOGHI DI POSIZIONE ============
def lp_ret():
    return f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/>'+tower(70,90,0.9)+line(70,50,280,170,SEA,4)+f'<circle cx="70" cy="50" r="6" fill="{SEA}"/>'+topboat(210,130,60,30,'#FFFFFF',NAVY,3)
def lp_bat():
    s=f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/><path d="M0 0 L300 0 L300 34 Q220 54 150 38 Q70 22 0 44 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
    s+=f'<path d="M0 82 Q80 66 150 96 T300 84" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="4 6" opacity="0.6"/><path d="M0 122 Q80 104 150 128 T300 118" fill="none" stroke="{BLUE}" stroke-width="5" stroke-dasharray="12 7"/>'
    s+=dash(150,186,150,30,NAVY,3)+topboat(150,150,56,-90,'#FFFFFF',NAVY,3)
    return s
def lp_dist():
    return f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/>'+tower(150,110,0.9)+f'<circle cx="150" cy="80" r="80" fill="none" stroke="{CORAL}" stroke-width="4" stroke-dasharray="10 7"/>'+topboat(222,120,56,60,'#FFFFFF',NAVY,3)
def lp_cap():
    s=f'<rect x="0" y="0" width="300" height="190" fill="{CHART}"/><circle cx="150" cy="120" r="90" fill="none" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="10 7"/>'
    s+=tower(80,160,0.7)+tower(220,160,0.7)+line(150,30,80,124,PURPLE,3)+line(150,30,220,124,PURPLE,3)+f'<circle cx="150" cy="30" r="9" fill="{NAVY}"/>'
    return s
LP=[(lp_ret(),'Semiretta di rilevamento','Vedo il faro per 045°: sono sulla semiretta che parte dal faro verso 225°.'),
    (lp_bat(),'Batimetrica','L\'ecoscandaglio legge la profondità della linea: sono lì. Attraversala a 90° per riconoscerla.'),
    (lp_dist(),'Cerchio di egual distanza','Conosco la distanza da un punto: sono su un cerchio con il centro nel punto.'),
    (lp_cap(),'Cerchio capace','Vedo due punti sotto lo stesso angolo: sono su un arco di cerchio che passa per i due.')]
cc=''.join(card(svgi(300,190,s,f'Disegno: {t}',dw=300,dh=190)+h3(t,28)+p(d,24),None,22,10) for s,t,d in LP)
sec('luoghi', head('Carteggio · gli strumenti del punto','I luoghi di posizione')+p('<b>Luogo di posizione</b>: l\'insieme dei punti che godono della stessa proprietà, per esempio «da qui vedo il faro per 045°».',28,INK)+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Il punto nave vuole almeno due luoghi di posizione. La rosa dei venti non lo è!',CORAL,36),
 notes='Quiz 1.7.6-39 (definizione: insieme di punti con la stessa proprietà), -2 (rette di rilevamento, cerchi capaci, cerchi di uguale distanza, batimetriche), -38 (la rosa dei venti non lo è), -14 (cerchio capace), -46 (un solo luogo non basta). Semiretta e non retta: il faro si vede solo da una parte, quella da cui lo guardo. La batimetrica si usa con l\'ecoscandaglio, tagliandola perpendicolarmente per non confondere le linee vicine.')

# ============ PUNTO NAVE 1 · DUE PUNTI COSPICUI ============
def coast(w=440):
    return f'<rect x="0" y="0" width="{w}" height="250" fill="{CHART}"/><path d="M0 0 L{w} 0 L{w} 60 Q{w*0.75:.0f} 86 {w*0.5:.0f} 62 Q{w*0.25:.0f} 40 0 70 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
def pnmark(x,y): return f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="4" fill="{NAVY}"/>'
def ext(a,b_,k=1.25): return (a[0]+(b_[0]-a[0])*k, a[1]+(b_[1]-a[1])*k)
def pn_two():
    s=coast()+tower(90,60,0.8)+bell(340,64,0.8); P=(230,190)
    e1=ext((90,24),P); e2=ext((340,22),P)
    return s+line(90,24,*e1,SEA,4)+line(340,22,*e2,CORAL,4)+pnmark(*P)
def pn_allin():
    s=coast()+tower(70,62,0.7)+f'<rect x="124" y="46" width="16" height="40" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'+tower(360,60,0.8)
    P=(300,206); a=(70,40); e=ext(a,P,1.12)
    return s+line(*a,*e,PURPLE,4)+line(360,22,*ext((360,22),P,1.2),SEA,4)+pnmark(*P)
def pn_one():
    s=coast()+tower(70,62,0.7)+f'<rect x="124" y="46" width="16" height="40" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
    a=(70,40); e=ext(a,(300,206),1.25)
    s+=line(*a,*e,PURPLE,4)
    for t,op in ((0.55,0.35),(0.8,0.35),(1.05,0.35)):
        q=ext(a,(300,206),t); s+=topboat(q[0],q[1],56,36,'#FFFFFF',NAVY,3,op,False)
    return s
PN1=[(pn_two(),'Due semirette','Due punti rilevati nello stesso momento: le semirette si incrociano nel punto nave. Meglio se si tagliano quasi a 90°.'),
     (pn_allin(),'Semiretta e allineamento','Due punti uno dietro l\'altro (rilevamento uguale, o a 180°) più il rilevamento di un terzo punto.'),
     (pn_one(),'Un allineamento non basta','So solo di essere su quella linea: serve almeno un altro luogo di posizione.')]
cc=''.join(card(svgi(440,250,s,f'Disegno: {t}',dw=480,dh=273)+h3(t,30)+p(d,24),None,24,10) for s,t,d in PN1)
sec('pn1', head('Carteggio · punto nave 1','Due punti cospicui')+f'<div style="display:flex; gap:22px">{cc}</div>'+note('Punto nave = almeno 2 luoghi di posizione',CORAL,40),
 notes='Quiz 1.7.6-1 (intersezione di due o più luoghi di posizione), -46 (un solo luogo non basta), -11 e -32 (allineamento: rilevamenti uguali o a 180°), -48 (due torri allineate: serve un altro luogo di posizione), -12 (squadrette per tracciare i rilevamenti). All\'esame: «PN per due rilevamenti simultanei», per es. 5.2.3-2, 5.4.3-2, 5.6.3-1 (lì i rilevamenti sono tre: il terzo è la verifica). Prima di tracciare: Rilv = Rilb + V.')

# ============ PUNTO NAVE 2 · RILEVAMENTO E DISTANZA ============
X=128
F=(660,240); RD=190
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/><path d="M500 30 L1062 30 L1062 300 Q960 250 880 180 Q800 110 700 140 Q600 160 540 90 Q520 60 500 30 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<circle cx="{F[0]}" cy="{F[1]}" r="{RD}" fill="{CORAL}" fill-opacity="0.06" stroke="{CORAL}" stroke-width="4" stroke-dasharray="12 8"/>'
PN=pol(*F,225,RD); far=pol(*F,225,RD+170)
b+=line(*F,*far,SEA,5)+tower(F[0],F[1]+30,1.2)
b+=dim(F[0]+10,F[1]+10,*pol(*F,135,RD))
b+=pnmark(*PN)
lc=pol(*F,135,RD*0.55); lr=pol(*F,225,RD+170)
lbl=(lab(X+F[0]+40,Y+F[1]-20,120,'faro',NAVY,26,900)+lab(X+lc[0]+20,Y+lc[1]-10,200,'1,5 miglia',CORAL,28,900,bg='#FFFFFF')
     +lab(X+lr[0]+30,Y+lr[1]-10,300,'semiretta Rlv 045°',SEA,26,900)+lab(X+PN[0]+30,Y+PN[1]+6,120,'PN',NAVY,30,900)
     +lab(X+F[0]-170,Y+F[1]+RD+14,340,'cerchio di egual distanza',CORAL,24,900,'center'))
txt=(term('Un punto, due luoghi','Dallo stesso faro prendo rilevamento e distanza: la semiretta e il cerchio si tagliano nel punto nave.')
     +term('La distanza','Dal radar o da un\'altra misura: col compasso si traccia il cerchio, centro nel faro.')
     +term('Esempio','Vedo il faro per 045° a 1,5 miglia: sono a SW del faro, a 1,5 miglia.')
     +term('All\'esame','La tecnica più frequente: «PN per rilevamento e distanza», per es. 5.4.3-6.'))
sec('pn2', head('Carteggio · punto nave 2','Un punto cospicuo: rilevamento e distanza'), pinned=pcol(txt,gap=18)+svgp(X,Y,W,Hh,b,'Faro sulla costa con il cerchio di egual distanza di 1,5 miglia e la semiretta di rilevamento per 045 gradi: si tagliano a Sud-Ovest del faro nel punto nave')+lbl,
 notes='Quiz 1.7.6-19 (servono un rilevamento e una distanza del punto cospicuo), -47 (con un solo punto cospicuo si può, se nota la distanza), -16 (5 miglia sul Rlv 180° del faro: sono a Nord, a 5 miglia), -21 (6 miglia sul Rlv SW: sono a NE). All\'esame «PN per rilevamento e distanza» compare in circa 30 esercizi, per es. 5.4.3-6, 5.4.3-8, 5.8.3-3, 5.1.1-1. Variante: allineamento e distanza (5.1.1-3).')

# ============ PUNTO NAVE 2 · RILEVAMENTI SUCCESSIVI ============
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/><path d="M30 30 L1062 30 L1062 120 Q800 170 546 110 Q300 60 30 130 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
F=(620,110); b+=tower(F[0],F[1]+20,1.2)
P1=(300,450); P2=(620,450)
b+=line(80,450,1000,450,NAVY,5)+arrow(900,450,1000,450,NAVY,5,20)
dx,dy=P1[0]-F[0],P1[1]-F[1]
b+=line(F[0],F[1],P1[0]+dx*0.25,P1[1]+dy*0.25,SEA,4)+dash(P2[0]-dx*0.9,P2[1]-dy*0.9,P2[0]+dx*0.25,P2[1]+dy*0.25,SEA,4)
b+=line(F[0],F[1],P2[0],P2[1]+110,CORAL,4)
b+=arrow(P1[0],P1[1]+40,P2[0],P2[1]+40,PURPLE,5,18)
b+=pnmark(*P2)
lbl=lab(X+130,Y+370,280,'1° rilevamento · 12:00',SEA,24,900)+lab(X+640,Y+300,280,'2° rilevamento · 12:20',CORAL,24,900)+lab(X+310,Y+500,360,'20′ a 9 nodi = 3 miglia',PURPLE,24,900,'center')
lbl+=lab(X+650,Y+180,330,'1° rilevamento trasportato',SEA,24,800)+lab(X+640,Y+410,200,'PN 12:20',NAVY,26,900,bg='#FFFFFF')+lab(X+860,Y+410,160,'Pv',NAVY,26,900)
txt=(term('Una sola mira, due volte','Rilevo lo stesso faro due volte: trasporto la prima semiretta lungo la rotta per le miglia percorse (M = V × Tᵐ : 60).')
     +term('Il punto','L\'incrocio della prima semiretta trasportata con la seconda è il punto nave dell\'ora del secondo rilevamento.')
     +term('All\'esame','Esercizi 5.x.3, come il 5.1.3-1: Rilb 075° alle 12:00, 125° alle 12:20, 9 nodi.'))
sec('puntonave', head('Carteggio · punto nave 2','Rilevamenti successivi'), pinned=svgp(X,Y,W,Hh,b,'Rilevamenti successivi dello stesso faro: la prima retta viene trasportata per le miglia percorse e incrocia la seconda nel punto nave')+lbl+pcol(txt),
 notes='Quiz 1.7.6-1 (intersezione di due o più luoghi di posizione), -12 e -13 (squadrette e compasso). Esercizi ufficiali «PN per rilevamenti successivi sulla stessa mira» (5.1.3-1…-5, 5.4.3-1, -5, 5.5.3-1): si convertono i rilevamenti bussola in veri (Rilv = Rilb + V), si tracciano le due semirette, si trasporta la prima parallelamente a sé stessa lungo la rotta per le miglia percorse; l\'incrocio con la seconda è il punto nave. Nel 5.1.3-1: 20′ a 9 nodi = 9 × 20 : 60 = 3 miglia. Si risolvono nella lezione 10.')
X=700

# ================= CAPITOLO 6 · RILEVAMENTI E GPS =================
chapter('cap6',6,'Rilevamenti e GPS',['Rilevamento polare','I rilevamenti: vero, bussola, polare','Dove sono rispetto al faro','Il punto nave: tutte le tecniche','Il GPS'],CORAL,
 'Circa 11 minuti, compresa una verifica da 2 quiz alla fine. È la parte finale della scaletta «Carteggio · Navigazione»: tutti i rilevamenti e le tecniche del punto nave. Quiz 10-11 nella raccolta finale.','circa 11 minuti · 5 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
# ============ RILEVAMENTO POLARE ============
X=128
C=(546,330); RG=230
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/>'
b+=f'<circle cx="{C[0]}" cy="{C[1]}" r="{RG}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
b+='<path d="'+' '.join(f'M{pol(*C,a,RG)[0]:.1f} {pol(*C,a,RG)[1]:.1f} L{pol(*C,a,RG-(20 if a%30==0 else 10))[0]:.1f} {pol(*C,a,RG-(20 if a%30==0 else 10))[1]:.1f}' for a in range(0,360,10))+f'" stroke="{NAVY}" stroke-width="3"/>'
for a in (90,270): b+=dash(*pol(*C,a,70),*pol(*C,a,RG-24),GREY,3)
b+=topboat(C[0],C[1],300,-90,'#FFFFFF',NAVY,4,0.85)
FO=pol(*C,300,RG+60); b+=line(*C,*pol(*C,300,RG+30),SEA,5)+tower(FO[0],FO[1]+10,1.0)
p0=pol(*C,0,120); p1=pol(*C,300,120); b+=f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A120 120 0 1 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-dasharray="10 7"/>'
q0=pol(*C,0,203); q1=pol(*C,300,203); b+=f'<path d="M{q0[0]:.1f} {q0[1]:.1f} A203 203 0 0 0 {q1[0]:.1f} {q1[1]:.1f}" fill="none" stroke="{CORAL}" stroke-width="7"/>'
lbl=''
for a,t1,t2 in ((0,'000°','0°'),(90,'090°','+90°'),(180,'180°','±180°'),(270,'270°','−90°')):
    o=pol(*C,a,RG+34); i=pol(*C,a,RG-50)
    lbl+=lab(X+o[0]-50,Y+o[1]-16,100,t1,NAVY,26,900,'center')+lab(X+i[0]-50,Y+i[1]-16,100,t2,CORAL,26,900,'center')
lc=pol(*C,330,215); ln=pol(*C,150,125)
lbl+=(lab(X+lc[0]-230,Y+lc[1]-70,250,'ρ −60° semicircolare',CORAL,26,900,'right',bg='#FFFFFF')+lab(X+ln[0]+10,Y+ln[1]-10,250,'ρ 300° circolare',NAVY,26,900,bg='#FFFFFF')
      +lab(X+FO[0]-150,Y+FO[1]+20,140,'faro',SEA,26,900,'right')+lab(X+C[0]+70,Y+C[1]+8,160,'traverso',SOFT,24,800)+lab(X+C[0]-230,Y+C[1]+8,160,'traverso',SOFT,24,800,'right'))
txt=(term('Rilevamento polare ρ','L\'angolo tra la prora (asse longitudinale) e l\'oggetto. Si misura con il grafometro.')
     +term('Grafometro circolare','Da 000° a 360° in senso orario dalla prora, sempre positivo: traverso a dritta 090°, a sinistra 270°.')
     +term('Grafometro semicircolare','Da 0° a 180°: + a dritta, − a sinistra. Traverso a sinistra −090°.')
     +term('Il traverso','ρ 90° e traverso coincidono sempre. Con vento o corrente accosti quando l\'oggetto è perpendicolare all\'asse della barca.'))
sec('rilevamento', head('Carteggio · dalla prora','Rilevamento polare'), pinned=svgp(X,Y,W,Hh,b,'Barca al centro del grafometro: fuori la scala circolare da 000 a 360 gradi dalla prora, dentro quella semicircolare con più a dritta e meno a sinistra; un faro a sinistra prora si legge 300 gradi oppure meno 60 gradi')+lbl+pcol(txt,gap=16),
 notes='Quiz 1.7.6-8 (angolo tra asse longitudinale e oggetto), -9 (circolare da 000° a 360° in senso orario dalla prora), -10 e -29 (semicircolare: positivo a dritta, negativo a sinistra), -17 (ρ 90° e traverso coincidono sempre), -33 (traverso = polare 90°), -18 (con scarroccio o deriva si accosta quando il punto è perpendicolare all\'asse longitudinale), -35 (grafometro). Nel disegno lo stesso faro si legge 300° sul grafometro circolare e −60° su quello semicircolare: con Pv 040° dà sempre Rilv 340°.')
X=700

# ============ I RILEVAMENTI ============
RT=[('Rilv','vero','dal Nord vero, sulla carta',NAVY,BLUE_T),('Rilm','magnetico','dal Nord magnetico',SEA,SEA_T),('Rilb','bussola','dal Nord bussola: lo leggi a bordo',CORAL,CORAL_T),('ρ','polare','dalla prora, col grafometro',PURPLE,LILAC_T),('±180°','reciproco','dal faro verso di me',GREEN,'#DDF3E4')]
cards=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:22px; border-radius:26px"><p style="font-family:{H}; font-size:46px; font-weight:700; line-height:1; color:{c}">{s}</p>{p(n,28,INK,800)}{p(d,24)}</div>' for s,n,d,c,bg in RT)
forms=f'<div style="display:flex; gap:14px; flex-wrap:wrap">{chip("Rilv = Rilb + V",CORAL,32)}{chip("Rilv = Rilm + d",SEA,32)}{chip("Rilv = Pv + ρ",PURPLE,32)}{chip("reciproco = Rilv ± 180°",GREEN,32)}</div>'
EXR=[('Esercizio 5.1.3-2','Rilb 164°, V −4°','Rilv 160°',CORAL),('Polare semicircolare','Pv 040°, ρ −60°','Rilv 340°',PURPLE),('Polare circolare','Pv 040°, ρ 300°','400° − 360° = 340°',PURPLE),('Reciproco','vedo il faro per 160°','dal faro sono a 340°',GREEN)]
exs=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:#FFFFFF; {SHADOW}; padding:20px; border-radius:24px">{tag(t,c)}{p(a,26,INK,700)}<p style="font-family:{H}; font-size:36px; font-weight:700; color:{c}">{r}</p></div>' for t,a,r,c in EXR)
sec('rilevamenti', head('Carteggio · tutte le opzioni','I rilevamenti')+f'<div style="display:flex; gap:16px">{cards}</div>'+forms+f'<div style="display:flex; gap:18px">{exs}</div>',
 notes='Riepilogo dei cinque modi di indicare la direzione di un punto cospicuo. Il rilevamento bussola si converte come la prora: Rilv = Rilb + V, con V = d + δ e δ letta per la prora della barca (non per il rilevamento). Il polare si somma alla prora vera: col grafometro semicircolare il segno fa da solo, con quello circolare si toglie 360° se si supera. Il reciproco serve per sapere dove sono rispetto al faro e per tracciare la semiretta dal faro. Quiz 1.7.6-24 (angolo di rilevamento dal Nord), -8 e -9 (polare), 1.7.4-34 (segni). Esercizio 5.1.3-2: Pb 086°, d 2°W, δ −2° → V −4°: Rilb 164° → Rilv 160°, Rilb 194° → Rilv 190°.')

# ============ DOVE SONO RISPETTO AL FARO ============
cx,cy=546,310
b=f'<rect x="30" y="30" width="1032" height="560" rx="20" fill="{CHART}"/><circle cx="{cx}" cy="{cy}" r="230" fill="none" stroke="#D9D2BF" stroke-width="3" stroke-dasharray="6 8"/>'
b+=tower(cx,cy+30,1.3)
bp=pol(cx,cy,225,165); b+=topboat(bp[0],bp[1],110,-45,'#FFFFFF',NAVY,4)
b+=arrow(bp[0]+30,bp[1]-30,cx-40,cy+10,CORAL,6,24)
bp2=pol(cx,cy,0,190); b+=topboat(bp2[0],bp2[1],100,90,'#FFFFFF',NAVY,3,0.5,False)+arrow(bp2[0],bp2[1]+40,cx,cy-80,SEA,5,20)
lbl=''
for a,t in [(0,'N'),(90,'E'),(180,'S'),(270,'W'),(45,'NE'),(135,'SE'),(225,'SW'),(315,'NW')]:
    x,y=pol(cx,cy,a,272); lbl+=lab(X+x-40,Y+y-16,80,t,NAVY if a%90==0 else SOFT,26,900,'center')
lbl+=lab(X+bp[0]-330,Y+bp[1]+40,300,'sono a SW: lo rilevo per 045°',CORAL,24,900,bg='#FFFFFF')+lab(X+bp2[0]+40,Y+bp2[1]-10,280,'sono a N: lo rilevo per 180°',SEA,24,900,bg='#FFFFFF')
ex=''.join(f'<div style="display:flex; justify-content:space-between; gap:12px; background:#FFFFFF; {SHADOW}; padding:10px 16px; border-radius:16px">{p(a,25,INK,700)}{p(b_,25,SEA,900)}</div>' for a,b_ in [('Sono a Sud-Est','Rlv 315°'),('Sono sul Rlv 270°','sono a Est'),('Sono sul Rlv 157,5°','sono a NNW')])
txt=term('Il rilevamento reciproco','Il faro si rileva dalla parte opposta a quella in cui mi trovo: aggiungi o togli 180°.')+ex
sec('reciproco', head('Carteggio · il rilevamento reciproco','Dove sono rispetto al faro')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Faro al centro della rosa: una barca a Sud-Ovest lo rileva per 045°, una barca a Nord lo rileva per 180°')+lbl,
 notes='Quiz 1.7.6-15, -20, -22, -25, -30, -31, -36 (sono a … del faro: lo rilevo per …), -16, -21, -26, -27, -28, -34, -37, -40, -42, -43 (sono sul Rlv … del faro: mi trovo a …), -44 (faro a prora con Rv Ovest: lo rilevo per 270°). Il quiz 1.7.6-28 ha una formulazione ambigua («sono sul Rlv 225°… lo rilevo per Sud-Ovest»): risposta ministeriale b.')

# ============ IL PUNTO NAVE: TUTTE LE TECNICHE ============
def tk_bg(): return f'<rect x="0" y="0" width="300" height="140" fill="{CHART}"/><path d="M0 0 L300 0 L300 30 Q220 46 150 32 Q70 18 0 38 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="2"/>'
def tk_sim(): return tk_bg()+tower(70,36,0.6)+bell(230,38,0.6)+line(70,12,*ext((70,12),(150,110),1.2),SEA,3)+line(230,12,*ext((230,12),(150,110),1.2),CORAL,3)+pnmark(150,110)
def tk_dist(): return tk_bg()+f'<circle cx="150" cy="20" r="90" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>'+tower(150,36,0.6)+line(150,12,*pol(150,12,200,130),SEA,3)+pnmark(*pol(150,12,200,90))
def tk_all(): return tk_bg()+tower(60,40,0.5)+f'<rect x="96" y="22" width="12" height="28" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'+line(60,22,*ext((60,22),(220,116),1.15),PURPLE,3)+f'<circle cx="60" cy="22" r="110" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="8 6"/>'+pnmark(*ext((60,22),(220,116),0.58))
def tk_succ():
    s=tk_bg()+tower(150,36,0.6)+line(20,112,290,112,NAVY,3)
    return s+line(150,12,70,112,SEA,3)+dash(230,12,150,112,SEA,3)+line(150,12,175,140,CORAL,3)+arrow(70,128,150,128,PURPLE,3,10)+pnmark(150,112)
def tk_div():
    s=tk_bg()+tower(80,36,0.6)+bell(230,38,0.6)+line(20,112,290,112,NAVY,3)
    return s+line(80,12,60,112,SEA,3)+dash(160,12,140,112,SEA,3)+line(230,12,140,112,CORAL,3)+arrow(60,128,140,128,PURPLE,3,10)+pnmark(140,112)
def tk_pol():
    s=tk_bg()+tower(200,36,0.6)+line(20,112,290,112,NAVY,3)+topboat(120,112,40,0,'#FFFFFF',NAVY,2)
    return s+dash(120,112,200,32,SEA,3)+dash(200,112,200,32,CORAL,3)+pnmark(200,112)
TK=[(tk_sim(),'Due rilevamenti simultanei','Due punti cospicui nello stesso istante.','24 esercizi · 5.2.3-2, 5.6.3-1'),
    (tk_dist(),'Rilevamento e distanza','Semiretta e cerchio di egual distanza.','30 esercizi · 5.4.3-6, 5.8.3-3'),
    (tk_all(),'Allineamento e distanza','Due punti allineati e la distanza da uno.','2 esercizi · 5.1.1-3'),
    (tk_succ(),'Successivi, stessa mira','Trasporto la prima semiretta del cammino fatto.','9 esercizi · 5.1.3-1'),
    (tk_div(),'Successivi, mire diverse','Prima un punto, poi un altro: trasporto il primo.','10 esercizi · 5.2.3-1, 5.3.3-1'),
    (tk_pol(),'Polari e traverso','Rilv = Pv + ρ; a ρ 90° sono al traverso.','21 + 31 esercizi · 5.3.3-2, -4')]
cc=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#FFFFFF; {SHADOW}; padding:16px; border-radius:24px">{svgi(300,140,s,"Disegno: "+t,dw=300,dh=140)}{h3(t,28)}{p(d,24)}{p(e,24,SEA,800)}</div>' for s,t,d,e in TK)
sec('tecniche', head('Carteggio · tutte le opzioni','Il punto nave: tutte le tecniche')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px 22px">{cc}</div>',
 notes='Le tecniche del punto nave negli esercizi ufficiali di carteggio (DD 131/2022), con quante volte compaiono: due rilevamenti simultanei (24, per es. 5.2.3-2, 5.4.3-2, 5.6.3-1), rilevamento e distanza (30, 5.4.3-6, 5.4.3-8, 5.8.3-3), allineamento e distanza (2, 5.1.1-3, 5.4.1-13), rilevamenti successivi sulla stessa mira (9, 5.1.3-1…-5), su mire diverse (10, 5.2.3-1, 5.3.3-1, 5.3.3-5), rilevamenti polari successivi (21, 5.3.3-4, 5.3.3-6) e punto al traverso (31, 5.3.3-2, 5.3.3-3). In tutte prima si convertono i rilevamenti in veri. Il cerchio capace è un luogo di posizione ma negli esercizi non serve. Le tecniche si fanno sulla carta nelle lezioni 8 e 10.')

# ============ GPS ============
b=f'<rect x="210" y="40" width="680" height="540" rx="46" fill="{NAVY}"/><rect x="250" y="80" width="600" height="380" rx="18" fill="#DDF1F5"/>'
b+=f'<path d="M250 80 L850 80 L850 170 Q720 210 600 160 Q480 110 380 170 Q300 210 250 180 Z" fill="{LAND}"/>'
b+=f'<path d="M330 420 L520 300 L720 230" fill="none" stroke="{CORAL}" stroke-width="5" stroke-dasharray="12 8"/>'
for x,y in ((520,300),(720,230)): b+=f'<path d="M{x} {y} V{y-40} L{x+26} {y-30} L{x} {y-20}" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<path d="M700 184 h40 M700 184 v-16" stroke="{NAVY}" stroke-width="5"/><circle cx="742" cy="168" r="7" fill="{LGREEN}"/><circle cx="700" cy="160" r="7" fill="{LRED}"/>'
b+=topboat(330,420,70,-32,'#FFFFFF',NAVY,3)
b+=f'<rect x="290" y="490" width="160" height="60" rx="16" fill="{LRED}"/><rect x="480" y="490" width="120" height="60" rx="16" fill="#2B4A6B"/><rect x="630" y="490" width="120" height="60" rx="16" fill="#2B4A6B"/>'
b+=''.join(f'<g transform="translate({x} {y}) rotate(-30)"><rect x="-14" y="-8" width="28" height="16" rx="3" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/><rect x="-40" y="-6" width="22" height="12" fill="{BLUE}"/><rect x="18" y="-6" width="22" height="12" fill="{BLUE}"/></g>' for x,y in ((110,90),(990,120),(980,420)))
lbl=lab(X+290,Y+504,160,'MOB',('#FFFFFF'),28,900,'center')+lab(X+620,Y+250,220,'waypoint',NAVY,24,900)
txt=(term('Come funziona','Misura la distanza da più satelliti: dà il punto nave in ogni istante, con un errore di pochi metri.')
     +term('Cosa ti dice','Latitudine e longitudine, Rv e Ve sul fondo, rotta e distanza dal waypoint, fuori rotta, ETA e tempo di percorrenza, data e ora.')
     +term('I limiti','Non vede ostacoli né costa: controlla il percorso sulla carta. Waypoint del porto almeno 500 m fuori dai fanali.')
     +term('Obbligo e MOB','Obbligatorio oltre le 12 miglia, fisso o portatile a batterie alcaline. Il tasto MOB segna dove è caduto l\'uomo in mare.'))
sec('gps', head('Navigazione elettronica','Il GPS')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Schermo di un GPS cartografico con la costa, la rotta tratteggiata tra due waypoint, la barca e il tasto rosso MOB; intorno i satelliti',pan=True)+lbl,
 notes='Quiz 1.7.3-2 (distanza dai satelliti), -3 e -13 (informazioni: lat e long, rotta e distanza dal waypoint, fuori rotta, tempo stimato di arrivo), -5 (pochi metri), -6 (punto nave in ogni istante), -7 (obbligatorio oltre 12 miglia), -4 (apparati fissi e portatili), -8 (waypoint a 500 m dai fanali del porto), -11 (non tiene conto degli ostacoli), -12 (navigazione per waypoint), -1, -9, -10 (MOB). Le dotazioni oltre le 12 miglia: lezione 6. Il GPS non sostituisce la carta: il punto stimato e quello costiero restano indispensabili.')

X=700

# ================= CAPITOLO 7 · SOTTOCOSTA =================
chapter('cap7',7,'Navigare sottocosta',['Vicino alla spiaggia','Subacquei e piccoli natanti'],SUN,
 'Circa 5 minuti, compresa una verifica da 2 quiz. Quiz 12 nella raccolta finale.','circa 5 minuti · 2 argomenti',1)
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
cc=''.join(card(svgi(300,190,s,f'Disegno: {t}',dw=300,dh=190)+h3(t,28)+p(d,24),None,22,10) for s,t,d in SB)
sec('subacquei', head('Condotta · chi c\'è in acqua','Subacquei e piccoli natanti')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Gara o manifestazione sulla rotta? Cambia percorso e stanne lontano.',PURPLE,36),
 notes='Quiz 1.4.2-15 (bandierina rossa con diagonale bianca, sub entro 50 m), -2 e -12 (almeno 100 m, moderando la velocità), -19 (sub a non più di 50 m dalla boa), -8 (unità di appoggio: pallone rosso con bandiera), -14 (bandiera A: palombaro), -9 e -16 (di notte luce gialla lampeggiante, visibile ad almeno 300 m), -20…-24 (entro 1 miglio), -13 (manifestazioni sportive). Pesca: -18 (sportiva consentita entro limiti di cattura), -26 (subacquea oltre 500 m dalle spiagge frequentate), -27 (mai di notte col fucile), -31 (mai con autorespiratori), -30 (100 m dagli impianti fissi), -32 (500 m dai pescatori professionali), -28 e -29 (niente reti a circuizione né pesca professionale).')

# ============ RACCOLTA QUIZ (45 minuti) ============
chapter('capquiz',8,'Raccolta quiz',['Rosa e bussola','Strumenti e stima','M = V × Tᵐ : 60','Carburante e riserva','Prora, rotta, scarroccio e deriva','Declinazione e deviazione','Navigazione costiera','Luoghi di posizione','Il punto nave','Rilevamento polare e traverso','GPS','Sottocosta e subacquei'],GREEN,
 'Inizio degli ultimi 45 minuti: 12 slide da 3 quiz ufficiali, ognuna seguita dalle risposte.','36 quiz ufficiali',2,'Ultimi 45 minuti','45′',art=(quiz_scene(),'Illustrazione: scheda di quiz con le risposte segnate e un cronometro sui 45 minuti'))
steps=[('1','Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.',CORAL,CORAL_T),
 ('2','Tempo in minuti','Nei calcoli porta il tempo in minuti e usa il 60: M = V × Tᵐ : 60. 2 h 30′ = 150′.',SEA,SEA_T),
 ('3','Cerca lo scambio','Declinazione o deviazione, prora o rotta, vento «da» o corrente «verso»: il trabocchetto è lì.',PURPLE,LILAC_T),
 ('4','Riserva o totale?','Nei quiz del carburante leggi cosa chiede: la sola riserva (30%) o tutto il carburante (× 1,3).',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,30,INK,800,1.2)}{p(d,24,INK,500,1.35)}</div>' for n,t,d,c,bg in steps)
exam=esame_box(['manovra', 'navigazione'],4,compact=True)
plan=card(tag("I 45 minuti",SEA)+'<ol style="font-size:24px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px"><li>Quiz 1-4 · rosa, bussola, stima, miglia, carburante (12)</li><li>Quiz 5-6 · prora e rotta, scarroccio e deriva, declinazione e deviazione (6)</li><li>Quiz 7-11 · costiera, punto nave, rilevamenti, GPS (15)</li><li>Quiz 12 · sottocosta e subacquei (3)</li></ol>',SEA_T,32,12)
sec('quiz', head('Lezione 04 · ultimi 45 minuti','Raccolta quiz')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div><div style="display:flex; gap:24px">{exam}{plan}</div>',
 notes='Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. I calcoli (quiz 3 e 4) si fanno alla lavagna con il triangolo M · V · Tᵐ. Se il tempo stringe, lasciare per casa le slide 8 e 12.', gap=28)
E='Raccolta quiz · DD 131/2022'
QZ=[('q01','Quiz 1 · Rosa e bussola',['1.7.4-1','1.7.4-11','1.7.4-12']),('q02','Quiz 2 · Strumenti e stima',['1.7.5-18','1.7.5-1','1.7.5-30']),
    ('q03','Quiz 3 · M = V × Tᵐ : 60',['1.7.5-27','1.7.5-39','1.7.5-56']),('q04','Quiz 4 · Carburante e riserva',['1.2.3-15','1.2.3-16','1.2.3-17']),
    ('q05','Quiz 5 · Prora, rotta, scarroccio e deriva',['1.7.7-1','1.7.7-12','1.7.7-22']),('q06','Quiz 6 · Declinazione e deviazione',['1.7.4-17','1.7.4-20','1.7.4-26']),
    ('q07','Quiz 7 · Navigazione costiera',['1.7.6-3','1.7.6-9','1.7.6-23']),('q08','Quiz 8 · Luoghi di posizione',['1.7.6-2','1.7.6-14','1.7.6-38']),
    ('q09','Quiz 9 · Il punto nave',['1.7.6-7','1.7.6-46','1.7.6-47']),('q10','Quiz 10 · Rilevamento polare e traverso',['1.7.6-8','1.7.6-17','1.7.6-29']),
    ('q11','Quiz 11 · GPS',['1.7.3-1','1.7.3-5','1.7.3-9']),('q12','Quiz 12 · Sottocosta e subacquei',['1.4.2-4','1.4.2-17','1.4.2-15'])]
for id_,t,ps in QZ:
    quiz_slide(id_,t,ps,False,E)
    quiz_slide(id_+'r',t+' · risposte',ps,True)
closing(['Angoli da 000° a 360° in senso orario; rotte con le squadrette sulla rosa della carta, miglia col compasso sulla scala delle latitudini','M = V × Tᵐ : 60 con il tempo in minuti; carburante × 1,3, sola riserva il 30%','Rv e Pv dal Nord vero; scarroccio dal vento («da»), deriva dalla corrente («verso»): + a dritta, − a sinistra','Pv = Pb + V con V = d + δ (Est +, Ovest −); δ dalla tabella delle deviazioni','Punto nave: almeno due luoghi di posizione; Rilv = Rilb + V = Pv + ρ','Entro 200 m dalle spiagge solo nei corridoi di lancio; 100 m dalle boe dei subacquei'],
 'Prossima lezione · 05 · COLREG e prevenzione degli abbordi','A casa: i quiz 1.7.4 (bussola), 1.7.5 (navigazione stimata), 1.7.6 (navigazione costiera), 1.7.3 (GPS), 1.7.7 (prora e rotta), 1.2.3 (carburante) e 1.4.2 (costa).')
exec(open('intermedi.py').read())
intermedi([('coordinate','v1','Verifica · Orientarsi sulla carta',['1.7.4-9','1.7.4-45']),
 ('carburante','v2','Verifica · Navigazione stimata e calcoli',['1.7.5-59','1.7.5-44']),
 ('regole','v3','Verifica · Prora e rotta, vento e corrente',['1.7.7-26','1.7.7-27']),
 ('conversioni','v4','Verifica · Declinazione e deviazione',['1.7.4-21','1.7.4-38']),
 ('puntonave','v5','Verifica · Navigazione costiera e punto nave',['1.7.6-1','1.7.6-48']),
 ('gps','v6','Verifica · Rilevamenti e GPS',['1.7.6-20','1.7.3-8']),
 ('subacquei','v7','Verifica · Sottocosta',['1.4.2-12','1.4.2-6'])])
write_deck(OUT,'Lezione 04 · Carteggio e Navigazione: primi calcoli, sottocosta, prora e rotta',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Rosa dei venti e quadranti, bussola, strumenti, rotte e coordinate","start":"cap1"},
  "s3":{"description":"Navigazione stimata, misura delle miglia, M = V × Tᵐ : 60, carburante e riserva","start":"cap2"},"s4":{"description":"Rotta e prora vera, scarroccio, deriva, angoli, moto proprio ed effettivo","start":"cap3"},
  "s5":{"description":"Declinazione, deviazione, tabella delle deviazioni e conversioni","start":"cap4"},"s6":{"description":"Navigazione costiera, luoghi di posizione, punto nave 1 e 2","start":"cap5"},
  "s7":{"description":"Rilevamento polare, tutti i rilevamenti, tecniche del punto nave, GPS","start":"cap6"},"s8":{"description":"Condotta sottocosta e subacquei","start":"cap7"},"s9":{"description":"Raccolta quiz","start":"capquiz"}})
