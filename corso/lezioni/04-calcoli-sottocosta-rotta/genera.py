import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez04/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; SAND='#F3E3B8'; GREY='#97A6B4'; STEEL='#8E9BAA'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','La rosa dei venti':'compass','Gli strumenti del carteggio':'dividers','La navigazione stimata':'pencil','Spazio, velocità, tempo':'chart','Tre esempi svolti':'pencil','Il carburante sulla carta':'fuel','Raccolta quiz':'quiz','Com\'è fatta un\'ancora':'anchor','I tipi di ancora':'anchor','Il calumo':'anchor',
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
cover(4,'Primi calcoli, sottocosta, prora e rotta','Orientarsi e calcolare S = V × T, navigare vicino alla spiaggia, passare dalla bussola alla carta: scarroccio e deriva',
 'Lezione 4. Capitoli del programma della scuola: Carteggio (primi calcoli: navigazione stimata, miglia, velocità, carburante; prora e rotta, scarroccio, deriva, declinazione, deviazione). Aggiunta dall\'All. A: condotta sottocosta, limiti di velocità, balneazione e corridoi di lancio (punto 4a). Materia 7 per rosa dei venti, strumenti, bussola e conversioni. Gli ultimi 45 minuti sono una raccolta di quiz ufficiali. Attracchi, ormeggi e ancoraggi sono nella lezione 3.')
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','30′','Rosa, strumenti, stima, S = V × T, carburante',CORAL),('0:30','15′','Sottocosta e subacquei',SEA),('0:45','30′','Bussola, tre nord, prora e rotta, scarroccio e deriva',PURPLE),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['manovra', 'navigazione'],4,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>orientarti con la rosa dei venti e usare squadrette e compasso</li><li>risolvere S = V × T e calcolare il carburante</li><li>rispettare le regole vicino alla spiaggia</li><li>passare da prora bussola a prora vera e ritorno</li><li>distinguere prora e rotta, scarroccio e deriva</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 04 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Tre capitoli di teoria in 75 minuti, con 2 quiz di verifica dopo i calcoli, dopo il sottocosta, dopo le conversioni di bussola e alla fine: andare spediti sulle slide, il dettaglio è nelle note. Poi 45 minuti di raccolta quiz. Banca DD 131/2022: orientamento e bussola 49 quiz (1.7.4), navigazione stimata 71 (1.7.5), navigazione in prossimità della costa 32 (1.4.2), prora e rotta, scarroccio e deriva 30 (1.7.7).')
X=700

# ================= PRIMI CALCOLI (dalla vecchia lezione 3) =================
chapter('cap1',1,'Orientarsi e primi calcoli',['La rosa dei venti','Gli strumenti del carteggio','La navigazione stimata','Spazio, velocità, tempo','Tre esempi svolti','Il carburante sulla carta'],CORAL,
 'Circa 30 minuti, compresa una verifica da 2 quiz alla fine. Andare spediti. Altri quiz nella raccolta finale (quiz 1-5).','circa 30 minuti · 6 argomenti',1,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
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
chips=''.join(f'<p style="font-size:22px; font-weight:800; color:{INK}; background:{bg}; padding:8px 14px; border-radius:18px">{t}</p>' for t,bg in [('N · Tramontana',SUN_T),('NE · Grecale',SUN_T),('E · Levante',SEA_T),('SE · Scirocco',SEA_T),('S · Ostro',CORAL_T),('SW · Libeccio',CORAL_T),('W · Ponente',LILAC_T),('NW · Maestrale',LILAC_T)])
right=(term('Angoli da 000° a 360°','Si contano dal Nord in senso orario, sempre con tre cifre: 045°, 157°, 320°.')
      +term('Quattro quadranti','I NE 000-090 · II SE 090-180 · III SW 180-270 · IV NW 270-360. Esempio: 157° è nel II.')
      +term('Cardinali e intercardinali','N, E, S, W e NE, SE, SW, NW. Sulla carta il Nord è in alto.')
      +f'<div style="display:flex; flex-wrap:wrap; gap:10px">{chips}</div>')
sec('rosa', head('Orientarsi','La rosa dei venti')+f'<div style="width:920px; display:flex; flex-direction:column; gap:20px">{right}</div>', pinned=svgp(RX,Y,700,620,b,'Rosa dei venti con i quattro quadranti colorati, le direzioni cardinali e intercardinali e una freccia verso 157 gradi nel secondo quadrante')+lbl,
 notes='Quiz 1.7.4-1, -4, -5, -6, -7 (in quale quadrante: 157° II, 224° III, 320° IV, 038° I, 099° II), -2 e -3 (sulla carta: 048° in alto a destra, 167° in basso a destra, 301° in alto a sinistra, 249° in basso a sinistra), -8 (senso orario), -9, -10, -11 (cardinali e intercardinali). I nomi dei venti tornano in meteorologia (lezione 7) e nel Portolano. Bussola, declinazione e deviazione: più avanti in questa lezione.')

# ============ STRUMENTI ============
X=128
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
lbl=lab(X+120,Y+556,420,'Squadrette nautiche',SEA,26,900)+lab(X+900,Y+190,160,'Compasso a punte secche',NAVY,24,900)+lab(X+470,Y+40,300,'Matita morbida e gomma',INK,24,900)
txt=term('Squadrette nautiche','Usate in coppia come parallele: tracciano e misurano rotte e rilevamenti.')+term('Compasso a punte secche','Misura distanze e riporta coordinate.')+term('Come si misura','Apri il compasso sul tratto e riporta l\'apertura sulla scala delle latitudini, alla stessa latitudine.')+term('Obbligatori','A bordo oltre le 12 miglia dalla costa.')
sec('strumenti', head('Il carteggio','Gli strumenti del carteggio'), pinned=pcol(txt)+svgp(X,Y,W,Hh,b,'Su una carta nautica: due squadrette nautiche con goniometro usate come parallele, un compasso a punte secche, una matita e una gomma')+lbl,
 notes='Quiz 1.7.5-18 (squadrette e parallele), -19 (compasso: distanze e coordinate), 1.7.2-30 (compasso a punte secche per non rovinare la carta), 1.7.5-33 e -52 (distanza sulla scala delle latitudini, alla stessa latitudine), 1.7.2-37 (misura della distanza), -71 (strumenti obbligatori oltre 12 miglia). Portare in aula squadrette e compasso: da qui in poi ogni lezione ha un po\' di carteggio.')
X=700


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
lbl=lab(X+120,Y+500,240,'Partenza · 09:00',NAVY,24,800)+lab(X+290,Y+330,110,'10:00',NAVY,22,800)+lab(X+470,Y+210,110,'11:00',NAVY,22,800)+lab(X+400,Y+80,260,'12:00 · punto stimato',CORAL,24,900,'right')
lbl+=lab(X+850,Y+180,220,'posizione reale',SOFT,22,800)+lab(X+840,Y+540,220,'vento e corrente',SOFT,22,800)+lab(X+460,Y+400,240,'zona di incertezza',CORAL,22,800)
txt=term('Il punto stimato','Una posizione approssimata: si ricava da prora vera, velocità, punto di partenza e tempo trascorso.')+term('Gli strumenti','Bussola, solcometro e orologio. GPS e radar non danno un punto stimato.')+term('Perché si sbaglia','Scarroccio, deriva, declinazione, deviazione: l\'incertezza cresce col tempo.')
sec('stimata', head('Primi calcoli','La navigazione stimata')+col(txt+note('Insostituibile, ma da confermare con un punto nave.',CORAL,36)), pinned=svgp(X,Y,W,Hh,b,'Rotta stimata con i punti orari e cerchi di incertezza sempre più grandi; la posizione reale si allontana per effetto di vento e corrente')+lbl,
 notes='Quiz 1.7.5-9 e -28 (punto stimato), -30 (elementi: Pv, velocità, posizione iniziale, tempo), -23 (bussola, solcometro, orologio), -1 (GPS e radar non danno posizione stimata), -11 e -22 (cause di errore), -3 e -12 (zona di incertezza), -29 (insostituibile ma insufficiente), -36 (punto nave con almeno due luoghi di posizione: lezione 5), -2 e -10 (si risolve graficamente sulla carta di Mercatore).')

# ============ FORMULA ============
b=f'<path d="M280 40 L40 440 L520 440 Z" fill="{SUN_T}" stroke="{SUN}" stroke-width="10" stroke-linejoin="round"/>'+line(160,240,400,240,SUN,8)+line(280,240,280,440,SUN,8)
TX=128
lbl=big(TX+230,Y+110,100,'S',CORAL,120)+big(TX+110,Y+300,120,'V',SEA,120)+big(TX+330,Y+300,120,'T',PURPLE,120)+big(TX+250,Y+320,60,'×',INK,70)
def chip2(t,c,u): return f'<div style="display:flex; align-items:center; gap:18px"><p style="font-family:{H}; font-size:44px; font-weight:700; color:#FFFFFF; background:{c}; padding:10px 28px; border-radius:40px; flex:none">{t}</p>{p(u,26,INK,700)}</div>'
mins=''.join(f'<div style="display:flex; flex-direction:column; align-items:center; background:#FFFFFF; {SHADOW}; padding:10px 14px; border-radius:18px"><p style="font-family:{H}; font-size:30px; font-weight:700; color:{INK}">{a}</p><p style="font-size:22px; font-weight:800; color:{SEA}">{b_} h</p></div>' for a,b_ in [('6′','0,1'),('12′','0,2'),('15′','0,25'),('18′','0,3'),('20′','0,33'),('30′','0,5'),('45′','0,75')])
right=(chip2('S = V × T',CORAL,'spazio in <b>miglia</b>')+chip2('V = S ÷ T',SEA,'velocità in <b>nodi</b> (miglia all\'ora)')+chip2('T = S ÷ V',PURPLE,'tempo in <b>ore e decimi</b>')
       +p('<b>Minuti in ore:</b> dividi per 60. <b>Decimi in minuti:</b> moltiplica per 60 (0,4 h = 24′).',26,INK)+f'<div style="display:flex; gap:12px">{mins}</div>')
sec('formula', head('Primi calcoli','Spazio, velocità, tempo')+f'<div style="position:absolute; left:748px; top:290px; width:1044px; display:flex; flex-direction:column; gap:22px">{right}</div>', pinned=svgp(TX,Y,560,480,b,'Il triangolo S sopra, V e T sotto: coprendo una lettera restano le altre due')+lbl+note('Copri la lettera che cerchi!',CORAL,40).replace('<p style="','<p style="position:absolute; left:'+str(TX+40)+'px; top:790px; width:500px; ',1),
 notes='Quiz 1.7.5-13, -14, -25, -51 (nodo = un miglio all\'ora), -15, -16, -17 (le tre formule), -26 (miglio per le distanze), -35 (ricalcolare a ogni cambio di velocità), -54 (4,4 h = 4 h 24′). Il triangolo è un aiuto per la memoria: coprendo S restano V × T, coprendo V resta S ÷ T, coprendo T resta S ÷ V.')

# ============ ESEMPI ============
def ex(qid,prob,steps,res,c,bg):
    st=''.join(p(s,24,BODY) for s in steps)
    return card(note(f'Quiz {qid}',c,34)+p(prob,27,INK,800,1.3)+f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:22px">{st}</div>'+f'<p style="font-family:{H}; font-size:52px; font-weight:700; color:{c}">{res}</p>',None,28,14)
e1=ex('1.7.5-31','15 nodi per 45 minuti: quante miglia?',['45′ ÷ 60 = <b>0,75 h</b>','S = 15 × 0,75'],'11,25 miglia',CORAL,CORAL_T)
e2=ex('1.7.5-65','18 miglia a 7 nodi: quanto tempo?',['T = 18 ÷ 7 = <b>2,57 h</b>','0,57 × 60 ≈ <b>34′</b>'],'2 h 34′',SEA,SEA_T)
e3=ex('1.7.5-63','24,5 miglia in 3 h 30′: che velocità?',['3 h 30′ = <b>3,5 h</b>','V = 24,5 ÷ 3,5'],'7 nodi',PURPLE,LILAC_T)
sec('esempi', head('Primi calcoli','Tre esempi svolti')+f'<div style="display:flex; gap:24px">{e1}{e2}{e3}</div>'+note('Prima trasforma il tempo in ore e decimi, poi applica la formula.',BLUE,38),
 notes='Esempi dai quiz ufficiali: 1.7.5-31 (15 kn, 45′ → 11,25 mg), -65 (18 mg, 7 kn → 2 h 34′), -63 (3 h 30′, 24,5 mg → 7 kn; attenzione, nell\'elenco il numero 1.7.5-63 compare due volte). Altri da fare alla lavagna: -39 (9 kn, 45′ → 6,75), -41, -44 (19 kn, 9′ → 2,85), -57 (11,6 mg a 6 kn → 1 h 56′), -60 (6 kn, 2 h 45′ → 16,5), -64 (2 h 20′ a 12 kn → 28 mg).')

# ============ CARBURANTE SULLA CARTA ============
b=f'<rect x="0" y="0" width="440" height="300" fill="{CHART}"/>'
b+=f'<path d="M0 0 L180 0 Q150 60 90 80 Q40 110 0 100 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/><path d="M300 300 Q320 230 400 220 Q440 222 440 240 L440 300 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=line(90,130,360,200,NAVY,5)+f'<circle cx="90" cy="130" r="11" fill="{CORAL}"/><circle cx="360" cy="200" r="11" fill="{SEA}"/>'
b+=f'<path d="M216 40 L96 118 L104 122 L220 48 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="2"/><path d="M224 40 L356 186 L348 190 L218 48 Z" fill="#9AA5B1" stroke="{NAVY}" stroke-width="2"/><circle cx="220" cy="42" r="10" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
b+=f'<g transform="translate(40 190)"><rect x="0" y="12" width="70" height="86" rx="10" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><rect x="40" y="0" width="20" height="16" rx="3" fill="{NAVY}"/><path d="M12 30 L58 80 M58 30 L12 80" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="6"/></g>'
def chipc(t,c): return f'<p style="font-family:{H}; font-size:32px; font-weight:700; color:#FFFFFF; background:{c}; padding:12px 22px; border-radius:40px">{t}</p>'
op=lambda t: f'<p style="font-family:{H}; font-size:40px; font-weight:700; color:{INK}">{t}</p>'
formula=f'<div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap">{chipc("1 · miglia col compasso",BLUE)}{op("→")}{chipc("2 · T = S ÷ V",SEA)}{op("→")}{chipc("3 · litri = l/h × T",PURPLE)}{op("+")}{chipc("4 · 30% di riserva",CORAL)}</div>'
boxes=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{bg}; padding:18px; border-radius:24px">{p(a,22,SOFT,800)}<p style="font-family:{H}; font-size:44px; font-weight:700; color:{INK}">{b_}</p>{p(c,22)}</div>' for a,b_,c,bg in [('1 · da A a B','9 miglia','sulla scala delle latitudini',BLUE_T),('2 · tempo','1,5 h','9 ÷ 6 nodi',SEA_T),('3 · consumo','6 litri','4 l/h × 1,5',LILAC_T),('4 · con riserva','≈ 8 litri','6 + 30% = 7,8',CORAL_T)])
exm=card(note('Esempio · 6 nodi, motore da 4 l/h',CORAL,36)+f'<div style="display:flex; gap:14px">{boxes}</div>',None,28,14)
sec('carburante', head('Primi calcoli · verso il carteggio','Il carburante sulla carta')+formula+f'<div style="display:flex; gap:24px; align-items:stretch">{svgi(440,300,b,"Mini carta: rotta da A a B misurata con il compasso e una tanica di carburante",dw=440,dh=300)}{exm}</div>'
 +p('All\'esame di carteggio la soluzione è un intervallo: per l\'esercizio 5.1.2-3 (consumo 4 l/h) la risposta ufficiale è «13÷15 litri».',26,INK),
 notes='Anticipo della lezione 11 (23 esercizi di carburante, famiglie 5.x.2). Stessa regola dei quiz di motori (1.2.3-1: riserva del 30%). Nel carteggio le miglia si misurano sulla carta tra punti noti o calcolati; il tempo si ricava con T = S ÷ V. Tolleranza: le risposte ufficiali danno un intervallo, per es. 5.1.2-1 «29÷31 litri», 5.1.2-2 «19÷21 litri».')

chapter('cap2',2,'Navigare sottocosta',['Vicino alla spiaggia','Subacquei e piccoli natanti'],SEA,
 'Circa 15 minuti, compresa una verifica da 2 quiz. Quiz 6-7 nella raccolta finale.','circa 15 minuti · 2 argomenti',1)
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


chapter('cap3',3,'Bussola, prora e rotta',['La bussola magnetica','Tre nord','Da bussola a vero e ritorno','Prora e rotta','Lo scarroccio','La deriva','Vento «da», corrente «verso»'],PURPLE,
 'Circa 30 minuti, comprese 2 verifiche da 2 quiz (dopo le conversioni e alla fine). Andare spediti. Quiz 8-12 nella raccolta finale.','circa 30 minuti · 7 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
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

chapter('capquiz',4,'Raccolta quiz',['Rosa dei venti','Strumenti e distanze','Navigazione stimata','S = V × T','Tempo e velocità','Sottocosta','Subacquei','La bussola','Declinazione e deviazione','Tre nord','Prora e rotta','Scarroccio e deriva'],GREEN,
 'Inizio degli ultimi 45 minuti: 12 slide da 3 quiz ufficiali, ognuna seguita dalle risposte.','36 quiz ufficiali',2,'Ultimi 45 minuti','45′',art=(quiz_scene(),'Illustrazione: scheda di quiz con le risposte segnate e un cronometro sui 45 minuti'))
# ============ RACCOLTA QUIZ (45 minuti) ============
steps=[('1','Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.',CORAL,CORAL_T),
 ('2','Tempo in ore','Nei calcoli trasforma subito i minuti in ore e decimi: 45′ = 0,75 h, 24′ = 0,4 h.',SEA,SEA_T),
 ('3','Cerca lo scambio','Declinazione o deviazione, prora o rotta, vento «da» o corrente «verso»: il trabocchetto è lì.',PURPLE,LILAC_T),
 ('4','Attento ai numeri','Metri o miglia, 100 o 200 metri, 1 miglio dalla costa: controlla l\'unità di misura.',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,30,INK,800,1.2)}{p(d,24,INK,500,1.35)}</div>' for n,t,d,c,bg in steps)
exam=esame_box(['manovra', 'navigazione'],4,compact=True)
plan=card(tag("I 45 minuti",SEA)+'<ol style="font-size:24px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px"><li>Quiz 1-5 · rosa, strumenti, stima, S = V × T (15)</li><li>Quiz 6-7 · sottocosta e subacquei (6)</li><li>Quiz 8-12 · bussola, prora e rotta, scarroccio e deriva (15)</li></ol>',SEA_T,32,12)
sec('quiz', head('Lezione 04 · ultimi 45 minuti','Raccolta quiz')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div><div style="display:flex; gap:24px">{exam}{plan}</div>',
 notes='Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. I calcoli (quiz 4 e 5) si fanno alla lavagna. Se il tempo stringe, lasciare per casa le slide 7 e 10.', gap=28)
E='Raccolta quiz · DD 131/2022'
QZ=[('q01','Quiz 1 · Rosa dei venti',['1.7.4-1','1.7.4-8','1.7.4-11']),('q02','Quiz 2 · Strumenti e distanze',['1.7.5-18','1.7.5-33','1.7.5-71']),
    ('q03','Quiz 3 · Navigazione stimata',['1.7.5-1','1.7.5-30','1.7.5-11']),('q04','Quiz 4 · S = V × T',['1.7.5-27','1.7.5-39','1.7.5-24']),
    ('q05','Quiz 5 · Tempo e velocità',['1.7.5-56','1.7.5-62','1.7.5-54']),('q06','Quiz 6 · Sottocosta',['1.4.2-4','1.4.2-17','1.4.2-20']),
    ('q07','Quiz 7 · Subacquei',['1.4.2-2','1.4.2-15','1.4.2-19']),('q08','Quiz 8 · La bussola',['1.7.4-12','1.7.4-44','1.7.4-49']),
    ('q09','Quiz 9 · Declinazione e deviazione',['1.7.4-17','1.7.4-19','1.7.4-26']),('q10','Quiz 10 · Tre nord',['1.7.4-22','1.7.4-42','1.7.4-40']),
    ('q11','Quiz 11 · Prora e rotta',['1.7.7-1','1.7.7-4','1.7.7-6']),('q12','Quiz 12 · Scarroccio e deriva',['1.7.7-12','1.7.7-14','1.7.7-22'])]
for id_,t,ps in QZ:
    quiz_slide(id_,t,ps,False,E)
    quiz_slide(id_+'r',t+' · risposte',ps,True)
closing(['Angoli da 000° a 360° in senso orario; squadrette per le rotte, compasso per le distanze sulla scala delle latitudini','S = V × T con il tempo in ore e decimi; carburante + 30% di riserva','Entro 200 m dalle spiagge solo nei corridoi di lancio; 100 m dalle boe dei subacquei','Pv = Pb + deviazione + declinazione (Est +, Ovest −), e ritorno','Scarroccio dal vento, deriva dalla corrente: il vento «da», la corrente «verso»'],
 'Prossima lezione · 05 · Punto nave e fanali','A casa: i quiz 1.7.4 (bussola), 1.7.5 (navigazione stimata), 1.4.2 (costa) e 1.7.7 (prora e rotta).')
exec(open('intermedi.py').read())
intermedi([('carburante','v1','Verifica · Orientarsi e primi calcoli',['1.7.4-9','1.7.5-59']),
 ('subacquei','v2','Verifica · Sottocosta',['1.4.2-12','1.4.2-6']),
 ('conversioni','v3','Verifica · Bussola e tre nord',['1.7.4-21','1.7.4-38']),
 ('regole','v4','Verifica · Scarroccio e deriva',['1.7.7-26','1.7.7-27'])])
write_deck(OUT,'Lezione 04 · Primi calcoli, sottocosta, prora e rotta',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Rosa dei venti, strumenti, navigazione stimata, S = V × T e carburante","start":"cap1"},
  "s3":{"description":"Condotta sottocosta e subacquei","start":"cap2"},"s4":{"description":"Bussola, tre nord e conversioni","start":"cap3"},
  "s5":{"description":"Prora e rotta, scarroccio e deriva","start":"prorarotta"},"s6":{"description":"Raccolta quiz","start":"capquiz"}})
