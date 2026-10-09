import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez06/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; GREY='#97A6B4'; NIGHT='#0F2238'
LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'; MBLACK='#1B2330'; MYEL='#F2C230'; ORANGE='#F28C28'
LB.ICON_T.update({'Raccolta quiz':'quiz','La prova di carteggio':'dividers','Il metodo per i 5 quesiti':'dividers','La traccia':'map','I 5 quesiti risolti':'map','La lezione di oggi':'lifebuoy','La vela in otto flash':'sail','La corrente':'current','Dalla prora alla rotta':'dividers',
 'Quale prora per la mia rotta':'compass','Trovare la corrente':'map','La falla':'hull','Incaglio e collisione':'hull','Incendio a bordo':'lifebuoy',
 'Uomo a mare':'lifebuoy','Abbandonare la barca':'lifebuoy','Il VHF di bordo':'lantern','Chiamare aiuto via radio':'lantern','Chi ci aiuta':'flag',
 'Il cattivo tempo':'wind','Alcol, droghe e farmaci':'check','La lezione di oggi':'lifebuoy','Fari e fanali: fin dove si vedono':'lighthouse','Riconoscere un faro':'lighthouse',
 'Entrare in porto: i segnali laterali':'flag','I segnali cardinali':'compass','Pericolo isolato, acque sicure, speciali':'flag',
 'I segnali sonori di manovra':'wind','Nella nebbia':'cloud','Entrare e uscire dal porto':'anchor',
 'Le dotazioni: salvarsi':'lifebuoy','Le dotazioni: navigare e comunicare':'compass','Chiedere soccorso':'flag',
 'Il triangolo del fuoco':'fuel','Classi di incendio ed estintori':'fuel'})
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def glow(x,y,c,r=9):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.6:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.6:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
def tower(x,y,s=1):
    g=f'<path d="M{x-14*s} {y} L{x-8*s} {y-90*s} L{x+8*s} {y-90*s} L{x+14*s} {y} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/><rect x="{x-9*s}" y="{y-66*s}" width="{18*s}" height="{12*s}" fill="{CORAL}"/><rect x="{x-11*s}" y="{y-34*s}" width="{22*s}" height="{12*s}" fill="{CORAL}"/>'
    return g+f'<rect x="{x-11*s}" y="{y-110*s}" width="{22*s}" height="{20*s}" rx="{4*s}" fill="{SUN}" stroke="{NAVY}" stroke-width="{2.5*s}"/>'
X,Y,W,Hh=700,290,1092,620
SKY='#DDEFF7'
def pill(x,y,w,t,c,size=24,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def windarrow(x,y,l=110,c=GREY): return arrow(x,y,x,y+l,c,8,26)
def grid(x0,y0,x1,y1,st,c='#DDE6EC'):
    s=''.join(line(x,y0,x,y1,c,2) for x in range(x0,x1+1,st))+''.join(line(x0,y,x1,y,c,2) for y in range(y0,y1+1,st))
    return s
def dot(x,y,c=NAVY,r=12): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#FFFFFF" stroke-width="4"/>'
def flame(x,y,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 30 Q-26 10 -12 -22 Q-6 -8 0 -12 Q2 -34 16 -44 Q14 -20 24 -6 Q30 16 0 30 Z" fill="{ORANGE}"/><path d="M0 26 Q-12 12 -4 -6 Q2 4 6 -2 Q14 10 0 26 Z" fill="{SUN}"/></g>'
def person(x,y,c=CORAL,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-16" r="11" fill="#F2C9A0" stroke="{NAVY}" stroke-width="2"/><path d="M-14 -4 Q0 -10 14 -4 L12 16 L-12 16 Z" fill="{c}"/></g>'
def ring(x,y,r=22): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ORANGE}" stroke-width="{r*0.55:.0f}"/><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.55:.0f}" stroke-dasharray="{r*0.8:.0f} {r*0.8:.0f}"/>'

# ---- segnali IALA in elevazione ----
def cone(x,y,up,s=22,c=MBLACK):
    return f'<path d="M{x-s*0.6:.0f} {y+s/2:.0f} L{x+s*0.6:.0f} {y+s/2:.0f} L{x} {y-s/2:.0f} Z" fill="{c}"/>' if up else f'<path d="M{x-s*0.6:.0f} {y-s/2:.0f} L{x+s*0.6:.0f} {y-s/2:.0f} L{x} {y+s/2:.0f} Z" fill="{c}"/>'
def mark(x,y,bands,top,s=1):
    """bands: lista colori dall'alto; top: lista di (tipo,param)"""
    h=90*s; w=40*s; bh=h/len(bands); g=''
    g+=f'<ellipse cx="{x}" cy="{y}" rx="{w*0.9:.0f}" ry="{8*s:.0f}" fill="{WATER}" fill-opacity="0.35"/>'
    for i,c in enumerate(bands): g+=f'<rect x="{x-w/2:.0f}" y="{y-h+i*bh:.0f}" width="{w:.0f}" height="{bh+0.5:.0f}" fill="{c}"/>'
    g+=f'<rect x="{x-w/2:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="none" stroke="{NAVY}" stroke-width="2"/><path d="M{x} {y-h:.0f} V{y-h-30*s:.0f}" stroke="{NAVY}" stroke-width="{3*s}"/>'
    ty=y-h-44*s
    for kind,par in top:
        if kind=='cone': g+=cone(x,ty,par,22*s); ty-=26*s
        elif kind=='ball': g+=f'<circle cx="{x}" cy="{ty:.0f}" r="{11*s:.0f}" fill="{par}"/>'; ty-=26*s
        elif kind=='x': g+=f'<path d="M{x-11*s:.0f} {ty-11*s:.0f} L{x+11*s:.0f} {ty+11*s:.0f} M{x+11*s:.0f} {ty-11*s:.0f} L{x-11*s:.0f} {ty+11*s:.0f}" stroke="{MYEL}" stroke-width="{6*s:.0f}" stroke-linecap="round"/>'
    return g
CARD={'N':([MBLACK,MYEL],[('cone',True),('cone',True)]),'E':([MBLACK,MYEL,MBLACK],[('cone',False),('cone',True)]),
      'S':([MYEL,MBLACK],[('cone',False),('cone',False)]),'W':([MYEL,MBLACK,MYEL],[('cone',True),('cone',False)])}


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
cover(6,'La sicurezza e i suoi elementi nella navigazione','Le dotazioni e i segnali di soccorso, l&#39;incendio, i sinistri, la radio, il cattivo tempo',
 'Lezione 6. Capitoli del programma della scuola: Sicurezza (dotazioni, mezzi di soccorso, incendio) ed emergenze (falla, incaglio, collisione, uomo a mare, abbandono, VHF, soccorso, tempo cattivo, 3). Aggiunte dall\'All. A: dotazioni obbligatorie secondo il DM 133/2024 (punto 3b), CIRM (3b), alcol e sostanze (3a). Fari e segnalamento AISM-IALA sono nella lezione 3. Gli ultimi 45 minuti sono una raccolta di quiz ufficiali.', title_size=80)
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','20′','Dotazioni di sicurezza',CORAL),('0:20','15′','Incendio e falla',PURPLE),('0:35','12′','Sinistri e abbandono',ORANGE),('0:47','15′','Radio e soccorso',BLUE),('1:02','13′','Cattivo tempo e alcol',SEA),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['sicurezza'],6,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>preparare la barca con le dotazioni giuste</li><li>scegliere tra fuochi a mano e razzi</li><li>spegnere un incendio e recuperare un uomo a mare</li><li>lanciare un MAYDAY sul canale 16</li><li>affrontare il cattivo tempo</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 06 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Cinque capitoli di teoria in 75 minuti, ognuno chiuso da una verifica da 2 quiz ufficiali: andare spediti, il dettaglio è nelle note. Segue la scaletta della scuola (22 argomenti, dalla zattera all\'ancora galleggiante). Nelle dotazioni ogni scheda ha due riquadri: «Per i quiz» (la risposta dell\'elenco ufficiale) e «A bordo oggi» (DM 133/2024). Poi 45 minuti di raccolta quiz. Banca DD 131/2022: incendio ed estintori 31 (1.3.1), dotazioni 48 (1.3.3), sinistri 36 (1.3.6), abbandono e soccorso (1.3.7), cattivo tempo (1.3.8), radio (1.3.9), alcol 12 (1.3.2).')
X=700

chapter('cap1',1,'Le dotazioni di sicurezza',['La tabella: salvarsi','La tabella: navigare e comunicare','La zattera','Giubbotti e salvagente','La boetta fumogena','Fuochi a mano e razzi','Le scadenze','EPIRB e riflettore radar','Binocolo e pronto soccorso'],CORAL,
 'Circa 20 minuti, verifica da 2 quiz compresa. In ogni scheda il riquadro giallo dice cosa rispondere ai quiz, quello azzurro cosa chiede oggi il DM 133/2024.','circa 20 minuti · 9 argomenti',2,art=(ring_scene(),'Illustrazione: salvagente anulare con la sagola galleggiante'))
# ============ DOTAZIONI (tabelle) ============
COLS=['oltre 50','entro 50','entro 12','entro 6','entro 3','entro 1','300 m']
def table(rows,notes_col=None):
    th=''.join(f'<th style="width:9%; text-align:center; color:#FFFFFF">{c}</th>' for c in COLS)
    h=f'<tr style="background:{NAVY}"><th style="width:37%; color:#FFFFFF">Dotazione (miglia dalla costa)</th>'+th+'</tr>'
    body=''
    for k,(name,vals) in enumerate(rows):
        bg=f' style="background:{PAPER if k%2 else "#FFFFFF"}"'
        body+=f'<tr{bg}><td style="font-weight:700; color:{INK}{"; padding:8px 12px" if k==0 else ""}">{name}</td>'+''.join(f'<td style="text-align:center; font-weight:800; color:{SEA if v=="●" else CORAL}">{v}</td>' for v in vals)+'</tr>'
    return f'<table style="font-size:24px; color:{BODY}">{h}{body}</table>'
o='●'; n=''
T1=[('Zattera di salvataggio (tutti a bordo)',[o,o,n,n,n,n,n]),('Zattera costiera',[n,n,o,n,n,n,n]),
    ('Giubbotti 150 N con luce automatica',[o,o,o,n,n,n,n]),('Giubbotti 100 N',[n,n,n,o,o,o,n]),
    ('Salvagente anulare con cima',[o,o,o,o,o,n,n]),('Boetta luminosa per il salvagente',[o,o,o,o,n,n,n]),
    ('Boette fumogene',['2','2','2','2','1',n,n]),('Fuochi a mano a luce rossa',['3','2','2','2','2',n,n]),
    ('Razzi a paracadute a luce rossa',['3','2','2','2',n,n,n]),('Imbragature con safety line (vela)',['2','2','1',n,n,n,n])]
T2=[('Bussola e tabella deviazioni, orologio',[o,o,o,n,n,n,n]),('Tabella dei segnali COLREG',[o,o,o,n,n,n,n]),('Apparato VHF',[o,o,o,n,n,n,n]),
    ('Binocolo, barometro, carte, strumenti da carteggio',[o,o,n,n,n,n,n]),('GPS, scandaglio, riflettore radar, pronto soccorso',[o,o,n,n,n,n,n]),
    ('EPIRB (o telefono satellitare)',[o,n,n,n,n,n,n]),('Fanali regolamentari',[o,o,o,o,o,n,n]),('Fischio e campana (oltre 12 m)',[o,o,o,o,o,n,n]),
    ('Pallone nero di fonda (oltre 7 m)',[o,o,o,o,o,o,n]),('Pompa di sentina',[o,o,o,o,o,o,n])]
sec('dotazioni1', head('A bordo oggi · DM 133/2024, Allegato V','Le dotazioni: salvarsi')+table(T1)+p('Mezzi collettivi e individuali per tutte le persone a bordo. Di notte, in solitario, il giubbotto si indossa sempre.',24,INK,700), gap=22,
 notes='Tabella dall\'Allegato V al DM 146/2008 come sostituito dal DM 17 settembre 2024 n. 133 (G.U. S.O. n. 35 del 21/09/2024, in vigore dal 21/10/2024). Colonne: senza limiti (qui «oltre 50»), entro 50, 12, 6, 3, 1 miglio, 300 m; esistono anche le acque interne. Entro 300 m nessuna dotazione obbligatoria in tabella. Tavole, derive, kitesurf, moto d\'acqua: dispositivo di galleggiamento da 50 N sempre indossato. Fuochi a mano sostituibili con dispositivo a LED SOLAS/MED. Quiz che divergono dalla nuova tabella e che all\'esame vanno risposti come nell\'elenco: 1.3.3-15 (entro 300 m salvagente e cinture), 1.3.3-12 (cinture oltre 300 m). Oscurati: 1.3.3-4, -6, -9, -11, -14, -23, -25, -26, -32, -33, -35, -36, -41, -42.')
sec('dotazioni2', head('A bordo oggi · DM 133/2024, Allegato V','Le dotazioni: navigare e comunicare')+table(T2)+p('Bussola elettronica e cartografia elettronica conforme sono ammesse. Gli estintori seguono il manuale del proprietario (unità CE).',24,INK,700), gap=22,
 notes='Stessa tabella del DM 133/2024. Quiz coerenti: 1.3.3-1 e -40 (VHF oltre 6 miglia, cioè da «entro 12»), -22 e -34 (EPIRB oltre 50), -24 (riflettore radar oltre 12), -43 (binocolo oltre 12), -39 (entro 12 niente EPIRB), -30 (radar non obbligatorio), -5 (bussola e tabelle), 1.3.3-8 (fanali di notte oltre 1 miglio), 1.7.3-7 (GPS oltre 12), 1.7.5-71 (strumenti da carteggio oltre 12). Pronto soccorso: tabella D del decreto 1° ottobre 2015 (1.3.3-45…-47). Estintori: 1.3.1-29 e -30 (manuale del proprietario; per le unità non CE il regolamento), 1.3.3-2 (natante entro 6 miglia: almeno 1).')

# ============ SCHEDE DELLE DOTAZIONI: «Per i quiz» e «A bordo oggi» ============
LB.ICON_T.update({'La zattera di salvataggio':'lifebuoy','Giubbotti e salvagente anulare':'lifebuoy','La boetta fumogena':'flag','Fuochi a mano e razzi a paracadute':'flag',
 'Le scadenze dei mezzi di soccorso':'check','EPIRB e riflettore radar':'compass','Binocolo e pronto soccorso':'check','Le classi di incendio':'flag','Gli estintori':'flag',
 'La portata del VHF':'compass','Il soccorso in mare':'lifebuoy','Cattivo tempo: prepararsi':'cloud','Cattivo tempo: le onde':'wind','L\'ancora galleggiante':'anchor'})
def dual(q,o):
    bq=f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{SUN_T}; padding:18px 24px; border-radius:24px; border-left:10px solid {SUN}">{tag("Per i quiz",CORAL)}{p(q,23,INK,500,1.36)}</div>'
    bo=f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{SEA_T}; padding:18px 24px; border-radius:24px; border-left:10px solid {SEA}">{tag("A bordo oggi · DM 133/2024",SEA)}{p(o,23,INK,500,1.36)}</div>'
    return f'<div style="display:flex; gap:20px">{bq}{bo}</div>'
def dot_slide(id_,eyebrow,title,svg,alt,terms,q,o,notes,w=600,h=380):
    sec(id_, head(eyebrow,title)+f'<div style="display:flex; gap:36px; align-items:start">{svgi(w,h,svg,alt,dw=760,dh=int(760*h/w),pan=False)}<div style="flex:1; display:flex; flex-direction:column; gap:16px">{terms}</div></div>'+dual(q,o), notes=notes, gap=22)
def sterm(t,d): return f'<div style="display:flex; flex-direction:column; gap:4px">{p(t,28,INK,800,1.25)}{p(d,25,BODY,400,1.38)}</div>'
def raft(x,y,s=1,canopy=True):
    g=f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="40" rx="130" ry="34" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><ellipse cx="0" cy="30" rx="104" ry="22" fill="#F7B26A"/>'
    if canopy: g+=f'<path d="M-110 34 Q0 -110 110 34 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><path d="M-30 30 Q0 -20 30 30 Z" fill="{INK}"/>'
    else: g+=f'<path d="M-90 30 L-90 -10 M90 30 L90 -10" stroke="{NAVY}" stroke-width="4"/><path d="M-90 -10 Q0 10 90 -10" fill="none" stroke="{SUN}" stroke-width="4"/>'
    return g+'</g>'
# zattera
s=f'<rect width="600" height="380" fill="{SKY}"/><rect y="250" width="600" height="130" fill="{WATER}" fill-opacity="0.5"/>'+raft(150,220,0.95,False)+raft(450,220,0.95,True)
s+=f'<text x="150" y="330" text-anchor="middle" font-family="Arial" font-size="24" font-weight="900" fill="{NAVY}">costiera</text><text x="150" y="360" text-anchor="middle" font-family="Arial" font-size="20" font-weight="700" fill="{NAVY}">oltre 6, entro 12 miglia</text>'
s+=f'<text x="450" y="330" text-anchor="middle" font-family="Arial" font-size="24" font-weight="900" fill="{NAVY}">d\'altura</text><text x="450" y="360" text-anchor="middle" font-family="Arial" font-size="20" font-weight="700" fill="{NAVY}">oltre 12 miglia</text>'
dot_slide('zattera','Sicurezza · mezzo collettivo di salvataggio','La zattera di salvataggio',s,'Due zattere: a sinistra la costiera, aperta, per la navigazione tra 6 e 12 miglia; a destra quella d\'altura, con la tenda, oltre le 12 miglia',
 sterm('Per tutti','Deve accogliere tutte le persone imbarcate.')+sterm('Dove tenerla','In coperta, facile da raggiungere: mai sottocoperta né in un gavone chiuso.')+sterm('Il manuale','Per le unità CE i dati tecnici e di sicurezza sono nel manuale del proprietario.'),
 'Costiera oltre 6 ed entro 12 miglia; d\'altura (non costiera) oltre 12. Non va tenuta sottocoperta (1.3.7-3 e -4).',
 'Entro 12 miglia la zattera costiera; oltre 12, fino a 50 miglia e senza limiti, la zattera d\'altura. Entro 6 miglia non è richiesta.',
 'Quiz 1.3.7-3 e -4 (dove non tenerla), -1 e -13 (abbandono: zattera equipaggiata), 1.3.3-13 (entro 3 miglia nessun mezzo collettivo). Revisione periodica della zattera secondo il costruttore. Tabella dell\'Allegato V al DM 146/2008 come sostituito dal DM 133/2024.')
# giubbotti
s=f'<rect width="600" height="380" fill="#F4FAFC"/>'
s+=f'<g transform="translate(160 40)"><path d="M-70 20 Q-60 -10 -20 -10 L-10 60 L10 60 L20 -10 Q60 -10 70 20 L80 260 Q0 290 -80 260 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><rect x="-80" y="160" width="160" height="16" fill="{NAVY}"/><rect x="-60" y="90" width="20" height="60" fill="#DDE6EC"/><rect x="40" y="90" width="20" height="60" fill="#DDE6EC"/><circle cx="50" cy="40" r="10" fill="{SUN}"/></g>'
s+=f'<g transform="translate(430 170)">{ring(0,0,100)}<path d="M100 0 Q150 60 120 140 Q90 190 140 210" fill="none" stroke="{ORANGE}" stroke-width="6"/></g>'
s+=f'<text x="160" y="360" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">giubbotto · uno a testa</text><text x="430" y="360" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">anulare con sagola</text>'
dot_slide('giubbotti','Sicurezza · mezzi individuali di salvataggio','Giubbotti e salvagente anulare',s,'Un giubbotto di salvataggio arancione e un salvagente anulare con la sagola galleggiante',
 sterm('Il giubbotto','Uno per ogni persona a bordo. Conta chi è imbarcato, non il massimo di persone che la barca può portare: se è omologata per 8 ma a bordo siete in 4, servono 4 giubbotti.')+sterm('L\'anulare','Con una sagola in polipropilene: una cima galleggiante sottile, adatta al recupero.')+sterm('Nei fiumi','Giubbotti e anulare sono sempre obbligatori.'),
 'Una cintura per persona oltre 300 m dalla costa (1.3.3-12); con 4 persone a bordo su una barca omologata per 8 ne servono 4 (1.3.3-19). Salvagente anulare con cima anche entro 300 m (1.3.3-15).',
 'Giubbotti da 100 N oltre 300 m e fino a 6 miglia; oltre 6 miglia da 150 N con luce. Salvagente anulare con cima oltre 1 miglio; oltre 3 miglia anche con la boetta luminosa. In solitario e di notte il giubbotto si indossa.',
 'Il materiale della scuola segue la regola dei quiz (oltre 300 m e sempre nei fiumi). La tabella del DM 133/2024 è nella prima slide del capitolo. «Trasportabili» è il numero massimo di persone che l\'unità può portare, scritto nel certificato di omologazione o nella licenza (1.3.3-37). Quiz 1.3.3-12, -15, -19, -27 (numero in base alle persone imbarcate), -38 e -44 (tavole a vela e moto d\'acqua: mezzo individuale sempre indossato).')
# boetta
s=f'<rect width="600" height="380" fill="#DDEFF7"/><rect y="250" width="600" height="130" fill="{WATER}" fill-opacity="0.55"/>'
s+=''.join(f'<circle cx="{300+dx}" cy="{220-i*42}" r="{34+i*14}" fill="{ORANGE}" fill-opacity="{0.6-i*0.1:.2f}"/>' for i,dx in enumerate((0,40,90,150,220)))
s+=f'<rect x="270" y="226" width="60" height="46" rx="8" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/><rect x="284" y="214" width="32" height="16" rx="4" fill="{LRED}"/>'
dot_slide('boetta','Sicurezza · segnali di soccorso','La boetta fumogena',s,'Boetta galleggiante che emette una nube di fumo arancione sull\'acqua',
 sterm('Segnale diurno','Galleggia e fa fumo arancione per circa 3 minuti: di notte non si vede.')+sterm('Quando','Di giorno, quando si vede un aereo o una nave che può notarci.')+sterm('Il vento','Si lancia sottovento, perché il fumo non investa la barca.'),
 'È un segnale diurno, di colore arancione (1.3.3-3 e -20). Entro 12 miglia ne servono 2.',
 '2 boette oltre 3 miglia (anche senza limiti), 1 entro 3 miglia, nessuna entro 1 miglio.',
 'Quiz 1.3.3-3 e -20 (boetta arancione, segnale diurno), -21 (scadenza 4 anni). Durata indicata sull\'etichetta: 3 minuti.')
# fuochi e razzi
def curv(night,kind):
    bg=NIGHT if night else '#BFE6F2'
    s=f'<rect width="290" height="300" fill="{bg}"/><path d="M-60 300 Q145 150 350 300 Z" fill="#1D4E73"/>'
    s+=f'<g transform="translate(150 192)"><path d="M-14 0 L14 0 L8 10 L-8 10 Z" fill="#FFFFFF"/><path d="M0 0 V-24" stroke="#FFFFFF" stroke-width="2"/></g>'
    if kind=='fuoco': s+=glow(158,176,LRED,7)+f'<g transform="translate(230 196)"><rect x="-26" y="-8" width="52" height="10" fill="#DDE6EC"/></g>'+(glow(222,186,LWHITE,4) if night else '')
    else:
        s+=dpath('M152 168 Q170 60 210 40',LRED,3)+glow(210,44,LRED,9)+f'<path d="M198 30 Q210 14 222 30 Z" fill="#DDE6EC"/>'
        s+=f'<g transform="translate(270 250)"><rect x="-26" y="-8" width="52" height="10" fill="#DDE6EC"/></g>'
    return s
s=f'<rect width="600" height="380" fill="#FFFFFF"/><g transform="translate(0 0)">{curv(True,"fuoco")}</g><g transform="translate(310 0)">{curv(True,"razzo")}</g>'
s+=f'<text x="145" y="340" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">fuoco a mano</text><text x="145" y="368" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="{NAVY}">vedo le luci della nave</text>'
s+=f'<text x="455" y="340" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">razzo a paracadute</text><text x="455" y="368" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="{NAVY}">la nave è oltre l\'orizzonte</text>'
dot_slide('fuochirazzi','Sicurezza · segnali di soccorso','Fuochi a mano e razzi a paracadute',s,'A sinistra un fuoco a mano acceso mentre una nave è in vista; a destra un razzo a paracadute che sale in alto per farsi vedere da una nave oltre l\'orizzonte',
 sterm('Fuochi a mano','Luce rossa, visibili a circa 6 miglia. Si accendono quando si vedono bene le luci di una nave, di un aereo o della costa.')+sterm('Razzi a paracadute','Salgono a 300 m, restano accesi meno di 1 minuto: 7 miglia di giorno, 25 di notte. Si usano quando si presume che qualcuno ci sia, anche se non si vede.'),
 'Fuochi: 6 miglia (1.3.3-16), solo se le luci sono ben visibili (1.3.9-7); 2 a bordo (1.3.3-18). Razzi: 300 m (1.3.9-9), meno di 1 minuto, 7 e 25 miglia (1.3.3-28 e -29).',
 'Fuochi a mano: 3 oltre 50 miglia, 2 fino a 50; si possono sostituire con un dispositivo a LED omologato. Razzi: 3 oltre 50 miglia, 2 da 6 a 50; entro 3 miglia non servono.',
 'La differenza tra fuoco a mano (aiuto in vista) e razzo (aiuto presunto, oltre l\'orizzonte) è un classico dei quiz: 1.3.9-7. Quiz 1.3.3-16, -17, -18, -28, -29, 1.3.9-9. Si accendono sottovento, con il braccio teso, senza guardare la fiamma.')
# scadenze
s=f'<rect width="600" height="380" fill="#F4FAFC"/>'
s+=f'<g transform="translate(110 250)"><rect x="-40" y="-60" width="80" height="110" rx="10" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/><rect x="-22" y="-78" width="44" height="22" rx="6" fill="{LRED}"/></g>'
s+=f'<g transform="translate(300 250) rotate(-30)"><rect x="-22" y="-90" width="44" height="180" rx="12" fill="{LRED}" stroke="{NAVY}" stroke-width="3"/></g>'
s+=f'<g transform="translate(490 250) rotate(30)"><rect x="-16" y="-100" width="32" height="140" rx="6" fill="#C9D3DC" stroke="{NAVY}" stroke-width="3"/><rect x="-14" y="40" width="28" height="60" rx="6" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/></g>'
s+=f'<g transform="translate(300 65)"><rect x="-60" y="-40" width="120" height="90" rx="12" fill="#FFFFFF" stroke="{CORAL}" stroke-width="4"/><rect x="-60" y="-40" width="120" height="24" fill="{CORAL}"/><text x="0" y="36" text-anchor="middle" font-family="Arial" font-size="34" font-weight="900" fill="{CORAL}">4 anni</text></g>'
dot_slide('scadenze','Sicurezza · i mezzi di soccorso','Le scadenze dei mezzi di soccorso',s,'Boetta fumogena, razzo a paracadute e fuoco a mano con un calendario che indica 4 anni di scadenza',
 sterm('Le fasce di distanza','Le dotazioni cambiano con la navigazione: entro 3, 6, 12 e 50 miglia, e senza limiti.')+sterm('La scadenza','Boette, fuochi a mano e razzi durano di solito 4 anni: la data è sul prodotto.')+sterm('Gli scaduti','Si consegnano al rivenditore quando si comprano i nuovi: non si buttano e non si sparano.'),
 'Scadenza in genere ogni 4 anni (1.3.3-21). Le fasce: fino a 3, 6, 12, 50 miglia e senza limiti (1.3.3-31).',
 'Le stesse fasce dell\'Allegato V, più quella entro 1 miglio e i 300 m. Controlla le date prima di uscire: un pirotecnico scaduto non conta come dotazione.',
 'Quiz 1.3.3-21 (scadenza 4 anni), -31 (range di dotazioni). I pirotecnici scaduti si riconsegnano al rivenditore all\'atto della sostituzione.')
# EPIRB e riflettore
s=f'<rect width="600" height="380" fill="#EAF4F7"/><rect y="290" width="600" height="90" fill="{WATER}" fill-opacity="0.4"/>'
s+=f'<g transform="translate(150 200)"><rect x="-44" y="-90" width="88" height="170" rx="26" fill="{MYEL}" stroke="{NAVY}" stroke-width="4"/><path d="M0 -90 V-170" stroke="{NAVY}" stroke-width="6"/>{glow(0,-70,LWHITE,7)}</g>'
s+=''.join(f'<path d="M{190+i*20} {40-i*6} q14 20 0 40" fill="none" stroke="{NAVY}" stroke-width="4"/>' for i in range(3))
s+=f'<g transform="translate(430 180)"><path d="M0 -110 L80 0 L0 110 L-80 0 Z" fill="{LRED}" stroke="{NAVY}" stroke-width="4"/><path d="M0 -110 L20 0 L0 110 M-80 0 L20 0 L80 0" fill="none" stroke="{NAVY}" stroke-width="3"/></g>'
s+=f'<text x="150" y="335" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">EPIRB</text><text x="430" y="335" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">riflettore radar</text>'
dot_slide('epirb','Sicurezza · farsi trovare','EPIRB e riflettore radar',s,'A sinistra l\'EPIRB giallo con l\'antenna che trasmette; a destra il riflettore radar rosso a forma di ottaedro',
 sterm('EPIRB','Emergency Position Indicating Radio Beacon: trasmettitore di emergenza che invia la posizione su 406 e 121,5 MHz. È programmato con il codice MMSI della barca.')+sterm('Riflettore radar','Rinforza l\'eco radar: anche una barca piccola si vede e si riconosce da lontano.'),
 'EPIRB oltre 50 miglia (1.3.3-22 e -34); entro 12 non serve (1.3.3-39). Riflettore radar oltre 12 miglia (1.3.3-24, 1.3.9-28).',
 'Gli stessi limiti: EPIRB (o telefono satellitare) solo senza limiti, oltre 50 miglia; riflettore radar oltre 12. Il radar non è obbligatorio (1.3.3-30).',
 'Quiz 1.3.3-22, -34, -39 (EPIRB), -24 e 1.3.9-28 (riflettore radar), -30 (radar non obbligatorio). L\'EPIRB va registrato e programmato con l\'MMSI.')
# binocolo e pronto soccorso
s=f'<rect width="600" height="380" fill="#F4FAFC"/>'
s+=f'<g transform="translate(160 180)"><rect x="-90" y="-50" width="70" height="140" rx="30" fill="{INK}"/><rect x="20" y="-50" width="70" height="140" rx="30" fill="{INK}"/><rect x="-20" y="-20" width="40" height="40" fill="#3B4A5E"/><circle cx="-55" cy="90" r="26" fill="#5A7FA6"/><circle cx="55" cy="90" r="26" fill="#5A7FA6"/></g>'
s+=f'<g transform="translate(440 190)"><rect x="-100" y="-70" width="200" height="140" rx="20" fill="{LRED}" stroke="{NAVY}" stroke-width="4"/><rect x="-30" y="-96" width="60" height="30" rx="10" fill="none" stroke="{NAVY}" stroke-width="6"/><rect x="-14" y="-40" width="28" height="80" fill="#FFFFFF"/><rect x="-40" y="-14" width="80" height="28" fill="#FFFFFF"/></g>'
dot_slide('binocolo','Sicurezza · oltre le 12 miglia','Binocolo e pronto soccorso',s,'Un binocolo e una cassetta di pronto soccorso rossa con la croce bianca',
 sterm('Binocolo','Obbligatorio oltre 12 miglia, ma utile sempre: per riconoscere fari, boe e altre barche.')+sterm('Cassetta di pronto soccorso','Oltre 12 miglia. Il contenuto lo fissa il decreto del Ministero della Salute del 1° ottobre 2015: tabella D per il diporto, tabella A per il noleggio.'),
 'Binocolo oltre 12 miglia (1.3.3-43). Pronto soccorso: decreto 1° ottobre 2015, tabella D (1.3.3-45, -46, -47).',
 'Binocolo, barometro, carte e strumenti da carteggio oltre 12 miglia; GPS, scandaglio e pronto soccorso anche loro oltre 12.',
 'Quiz 1.3.3-43 (binocolo), -10, -45, -46, -47 (cassetta di pronto soccorso e tabella D). Il CIRM dà i consigli medici via radio: capitolo 4.')

chapter('cap2',2,'Incendio e falla',['Il triangolo del fuoco','Le classi di incendio','Gli estintori','Incendio a bordo','La falla'],PURPLE,
 'Circa 15 minuti, verifica da 2 quiz compresa.','circa 15 minuti · 5 argomenti',1,art=(fire_scene(),'Illustrazione: estintore accanto a una fiamma'))
# ============ TRIANGOLO DEL FUOCO ============
A=(546,70); B_=(236,560); C=(856,560)
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FFF1E6"/>'
b+=f'<path d="M{A[0]} {A[1]} L{B_[0]} {B_[1]}" stroke="{CORAL}" stroke-width="22" stroke-linecap="round"/><path d="M{B_[0]} {B_[1]} L{C[0]} {C[1]}" stroke="{SUN}" stroke-width="22" stroke-linecap="round"/><path d="M{C[0]} {C[1]} L{A[0]} {A[1]}" stroke="{BLUE}" stroke-width="22" stroke-linecap="round"/>'
b+=f'<path d="M546 470 C470 430 480 350 530 300 C520 350 560 360 560 330 C590 380 640 400 610 460 C600 480 570 480 546 470 Z" fill="{ORANGE}"/><path d="M546 470 C510 450 515 410 540 380 C545 410 565 420 575 400 C590 430 580 470 546 470 Z" fill="{SUN}"/>'
lbl=lab(X+70,Y+280,260,'Combustibile',CORAL,30,900,'right')+lab(X+770,Y+280,300,'Comburente (ossigeno)',BLUE,30,900)+lab(X+396,Y+580,300,'Calore',SUN,30,900,'center')
txt=term('La combustione','Una reazione tra combustibile e comburente che produce calore. Servono tutti e tre i lati.')+term('Come si spegne','Togli un lato: raffreddamento (calore), soffocamento (ossigeno), separazione (combustibile).')+term('Prevenzione','Niente stracci unti nel vano motore, aera prima di avviare un motore a benzina. L\'aria che entra alimenta l\'incendio.')
sec('fuoco', head('Sicurezza · incendio','Il triangolo del fuoco')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Triangolo del fuoco con una fiamma al centro: lati combustibile, comburente e calore')+lbl,
 notes='Quiz 1.3.1-24 (triangolo: combustibile, comburente, calore), -27 (combustione), -31 (comburente), -25 e -26 (si spegne abbassando la temperatura o togliendo l\'ossigeno), -10 (l\'aria alimenta l\'incendio), -5 (stracci unti), -28 (temperatura di infiammabilità). Il ciclo di aerazione del vano motore a benzina è nella lezione 2.')

# ============ CLASSI DI INCENDIO ============
def cico(k):
    s=f'<rect width="220" height="170" rx="20" fill="#FFF1E6"/>'
    if k=='A': s+=f'<path d="M50 140 L170 110 M60 110 L170 140" stroke="#8B5A2B" stroke-width="16" stroke-linecap="round"/>'+flame(110,110,0.9)
    elif k=='B': s+=f'<g transform="rotate(-15 110 100)"><rect x="70" y="60" width="80" height="96" rx="8" fill="#6B8E4E" stroke="{NAVY}" stroke-width="3"/><rect x="120" y="44" width="22" height="20" fill="#6B8E4E" stroke="{NAVY}" stroke-width="3"/></g>'+flame(70,70,0.6)
    elif k=='C': s+=f'<rect x="40" y="120" width="140" height="18" rx="6" fill="{BLUE}"/><rect x="70" y="102" width="80" height="20" rx="6" fill="#6B8BC7"/>'+''.join(flame(x,96,0.45) for x in (80,110,140))
    elif k=='D': s+=f'<circle cx="110" cy="105" r="40" fill="none" stroke="#8A97A6" stroke-width="22" stroke-dasharray="14 8"/>'+flame(140,60,0.55)
    else: s+=f'<rect x="30" y="118" width="70" height="14" rx="6" fill="{BLUE}"/><rect x="120" y="118" width="70" height="14" rx="6" fill="{BLUE}"/><path d="M120 30 L96 96 L116 96 L100 150 L140 80 L118 80 L136 30 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'+flame(110,120,0.5)
    return s
CL=[('A','Combustibili solidi','Legno, tessuti, carta. Polvere o schiuma; si raffredda con getti d\'acqua.',SEA),
    ('B','Liquidi infiammabili','Carburante, olio, vernici. Si soffoca: polvere, schiuma, CO2.',BLUE),
    ('C','Gas infiammabili','Bombola del gas di cucina. CO2 o polvere; prima chiudi il gas.',PURPLE),
    ('D','Metalli','Alluminio, magnesio. Polvere speciale per metalli: mai acqua, il CO2 non serve.',SOFT),
    ('E','Apparecchi elettrici','Quadri, radio, motorini sotto tensione. CO2 o polvere: mai acqua. Classe ancora nei quiz, non più nella norma europea.',CORAL)]
cc=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:#FFFFFF; {SHADOW}; padding:16px; border-radius:24px; border-top:10px solid {c}"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1; color:{c}">{k}</p>{svgi(220,170,cico(k),"Classe "+k+": "+t,dw=240,dh=185,pan=False)}{h3(t,26)}{p(d,22,INK,500,1.35)}</div>' for k,t,d,c in CL)
sec('classi', head('Sicurezza · incendio','Le classi di incendio')+f'<div style="display:flex; gap:14px">{cc}</div>'+dual('Polvere su tutte le classi (1.3.1-1); CO2 su liquidi, gas e apparecchi elettrici (1.3.1-13, -18); schiuma su A e B (1.3.1-2, -15); acqua pericolosa su metalli ed elettrico (1.3.1-8, -20).','Metalli (D): polvere speciale, il CO2 non serve, l\'acqua li fa esplodere. La norma europea EN 2 non ha più la classe E: un incendio elettrico si classifica per ciò che brucia e l\'estintore indica se si può usare sotto tensione. È nata la classe F, oli e grassi da cucina.'), gap=18,
 notes='La combustibilità dei liquidi dipende dalla temperatura di infiammabilità (1.3.1-28). Quiz 1.3.1-16, -9, -17, -14 (classi A solidi, B liquidi, C gas, E elettrico), -1 e -12 (polvere), -13, -18, -19, -6 (CO2), -2 e -15 (schiuma), -8 e -20 (acqua pericolosa). Classe E: la norma UNI EN 2 non la prevede più (non è stata «inglobata» nella B): gli incendi di apparecchi elettrici si classificano secondo il materiale che brucia, e sull\'etichetta l\'estintore indica se è utilizzabile su apparecchi sotto tensione (di solito fino a 1000 V). La stessa norma ha introdotto la classe F (oli e grassi da cucina). I quiz ufficiali usano ancora la classe E (1.3.1-14, -18, -20): all\'esame si risponde così. Correzione tecnica concordata: sui metalli il CO2 non è adatto (il materiale della scuola lo indica): all\'esame vale la risposta del quiz.')

# ============ ESTINTORI ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FFF1E6"/>'
b+=f'<rect x="240" y="170" width="170" height="380" rx="70" fill="{LRED}" stroke="{NAVY}" stroke-width="5"/><rect x="290" y="110" width="70" height="70" rx="10" fill="#6B7F95" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M360 130 L480 110 L490 124 L372 150 Z" fill="{NAVY}"/><path d="M300 150 Q180 150 170 260 L150 330" fill="none" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<rect x="260" y="260" width="130" height="150" rx="12" fill="#FFFFFF"/><circle cx="325" cy="120" r="1" fill="none"/>'
b+=f'<circle cx="700" cy="250" r="140" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/>'
b+=f'<path d="M580 250 A120 120 0 0 1 640 146" fill="none" stroke="{LRED}" stroke-width="22"/><path d="M640 146 A120 120 0 0 1 760 146" fill="none" stroke="{LGREEN}" stroke-width="22"/><path d="M760 146 A120 120 0 0 1 820 250" fill="none" stroke="{LRED}" stroke-width="22"/>'
b+=line(700,250,680,150,NAVY,8)+f'<circle cx="700" cy="250" r="12" fill="{NAVY}"/>'+dash(360,145,560,220,NAVY,3)
lbl=lab(X+262,Y+290,126,'13B',INK,44,900,'center')+lab(X+262,Y+350,126,'classe e capacità',SOFT,22,800,'center')+lab(X+560,Y+420,300,'manometro: lancetta nel verde',LGREEN,24,900,'center')
cls=''.join(f'<div style="display:flex; gap:12px; align-items:center"><p style="width:52px; height:52px; border-radius:26px; background:{c}; color:#FFFFFF; font-family:{H}; font-size:30px; font-weight:700; text-align:center; line-height:52px; flex:none">{k}</p>{p(t,24,INK,700,1.25)}</div>' for k,t,c in [('A','solidi',SEA),('B','liquidi infiammabili',BLUE),('C','gas',PURPLE),('D','metalli',SOFT),('E','apparecchi elettrici in tensione',CORAL)])
ext=''.join(f'<div style="display:flex; justify-content:space-between; gap:10px; background:#FFFFFF; {SHADOW}; padding:8px 14px; border-radius:14px">{p(a,24,INK,800)}{p(b_,24,SEA,800)}</div>' for a,b_ in [('Polvere','A, B, C, E'),('CO2','B, C, E'),('Schiuma','A, B'),('Metalli (D)','polvere speciale')])
txt=ext+term('Revisione','Solo se perde pressione (lancetta nel rosso) o dopo l\'uso; si sostituisce se è in cattivo stato. Getto sempre alla base delle fiamme.')+term('Quanti a bordo','Unità CE: numero e posto li dà il manuale del proprietario. Senza marchio CE: in base alla potenza del motore, uno al posto di guida e uno per locale. Natanti entro 6 miglia: almeno 1. Tutti omologati CE.')
sec('estintori', head('Sicurezza · incendio','Gli estintori'), pinned=svgp(X,Y,W,Hh,b,'Estintore con etichetta 13B e il suo manometro con la lancetta nella zona verde')+lbl+pcol(txt,532,12),
 notes='Quiz 1.3.1-16, -9, -17, -14 (classi A solidi, B liquidi, C gas, E elettrico), -1 e -12 (polvere: tutte le classi), -13, -18, -19, -6 (CO2 per liquidi, gas e apparecchi elettrici; VHF in fiamme: CO2), -2 e -15 (schiuma: A e B), -7 (getto alla base), -8 e -20 (acqua pericolosa su metalli e impianti elettrici), -11 (13B: classe e capacità estinguente), -21, -22, -23 (revisione e sostituzione), -4 (omologati CE). Il quiz 1.3.1-3 è oscurato: la CO2 nei locali chiusi toglie l\'ossigeno anche alle persone.')
X=700

X,Y,W,Hh=700,290,1092,620
# ============ INCENDIO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.12"/>'+line(546,110,546,600,'#C9D3DD',3)
b+=''.join(windarrow(x,10,80) for x in (516,576))
b+=topboat(270,330,300,-90,'#FFFFFF',NAVY,5)+flame(270,445,1.3)+''.join(f'<circle cx="{270+dx}" cy="{510+i*30}" r="{16+i*6}" fill="{GREY}" fill-opacity="{0.45-i*0.1:.2f}"/>' for i,dx in enumerate((0,8,-6)))
b+=topboat(820,300,300,90,'#FFFFFF',NAVY,5)+flame(820,415,1.3)+''.join(f'<circle cx="{820+dx}" cy="{480+i*30}" r="{16+i*6}" fill="{GREY}" fill-opacity="{0.45-i*0.1:.2f}"/>' for i,dx in enumerate((0,8,-6)))
b+=arrow(270,150,270,120,NAVY,5,16)+arrow(820,160,820,120,NAVY,5,16) if False else ''
lbl=pill(X+40,Y+24,400,'Fuoco a poppa: prua al vento',CORAL,22)+pill(X+620,Y+24,420,'Fuoco a prua: poppa al vento',CORAL,22)
lbl+=lab(X+60,Y+582,440,'il fumo va via da chi è a bordo',NAVY,22,800,'center')+lab(X+600,Y+582,440,'fiamme sempre sottovento',NAVY,22,800,'center')
txt=('<ol style="font-size:25px; line-height:1.36; color:#34465E; display:flex; flex-direction:column; gap:5px">'
 '<li><b>Giubbotti</b> a tutti.</li><li>Chiudi le <b>vie d\'aria</b> e la <b>valvola del carburante</b>.</li><li>Non aprire un locale in fiamme: l\'aria alimenta il fuoco.</li>'
 '<li>Metti le <b>fiamme sottovento</b>: fuoco a poppa, prua al vento; fuoco a prua, poppa al vento.</li><li>Estintore alla <b>base delle fiamme</b>.</li>'
 '<li>Allontanati dal porto, <b>non entrarci</b>.</li><li>Se è grave prepara l\'<b>abbandono</b>.</li><li>Prevenzione: niente <b>stracci unti</b> in sentina, possono incendiarsi da soli.</li></ol>')
sec('incendio', head('Sicurezza · i sinistri','Incendio a bordo'), pinned=svgp(X,Y,W,Hh,b,'Due barche viste dall\'alto con il vento da nord: con il fuoco a poppa la barca mette la prua al vento; con il fuoco a prua mette la poppa al vento; in entrambi i casi fiamme e fumo vanno sottovento')+lbl+pcol(txt,532,8),
 notes='La procedura in 8 punti del materiale della scuola. Quiz 1.3.6-11 (non accelerare verso il porto), -12 e -24 (chiudere carburante e vie d\'aria), -13, -18, -22, -25 (fiamme sottovento: fuoco a poppa prua al vento, fuoco a prua poppa al vento), -14 (base della fiamma), -15 (grave: preparare l\'abbandono), -16 (quadro elettrico: polvere), -17 (giubbotti e allontanarsi), -19 (in porto: allontanare l\'unità), -20 (ventilazione forzata prima di avviare un motore a benzina), -21 e -23 (raffreddamento e soffocamento), -26 e -27 (numero di estintori).')
X=700

X,Y,W,Hh=700,290,1092,620
# ============ FALLA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
wl=250
hull='M220 120 L220 260 Q230 470 546 500 Q862 470 872 260 L872 120 Z'
b+=f'<rect x="0" y="{wl}" width="1092" height="{620-wl}" fill="{WATER}" fill-opacity="0.5"/>'+line(0,wl,1092,wl,SEA,3)
b+=f'<path d="{hull}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/><rect x="226" y="330" width="640" height="150" fill="{WATER}" fill-opacity="0.25"/>'
b+=f'<path d="{hull}" fill="none" stroke="{NAVY}" stroke-width="6"/>'+line(220,120,872,120,NAVY,8)
hx,hy=820,400
b+=f'<ellipse cx="{hx+44}" cy="{hy}" rx="16" ry="40" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/>'
b+=''.join(arrow(1010,hy+dy,hx+70,hy+dy,SEA,5,16) for dy in (-30,0,30))
b+=f'<path d="M{hx-6} {hy} q-60 10 -90 50" fill="none" stroke="{WATER}" stroke-width="10" stroke-linecap="round" stroke-dasharray="4 10"/>'
b+=f'<rect x="330" y="420" width="70" height="46" rx="10" fill="{NAVY}"/><path d="M365 420 L365 180 Q365 150 330 150 L180 150 Q150 150 150 180 L150 240" fill="none" stroke="{GREY}" stroke-width="10"/>'+arrow(150,236,150,300,WATER,6,18)
b+=dim(960,120,960,wl,CORAL)
lbl=pill(X+812,Y+318,300,'tappo di fortuna, da fuori',ORANGE,22)+pill(X+800,Y+452,280,'pressione dell\'acqua',SEA,22)+pill(X+410,Y+440,220,'pompa di sentina',NAVY,22)
lbl+=pill(X+880,Y+140,190,'riserva di spinta',CORAL,22)+lab(X+620,Y+520,300,'acqua che entra',SEA,22,800)
txt=term('Perché è grave','Ogni litro che entra toglie riserva di spinta: il volume stagno sopra la linea di galleggiamento.')+term('Tappare','Il tampone va messo da fuori: la pressione dell\'acqua lo spinge contro lo scafo. Per una falla grande: tele cerate, materassi, cuscini.')+term('Rallentare ed esaurire','Falla a prua: ferma la barca. Pompe di sentina elettriche o manuali; se è irreparabile, MAYDAY.')
sec('falla', head('Sicurezza · i sinistri','La falla')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione di uno scafo con una falla sotto la linea di galleggiamento: il tampone è applicato dall\'esterno e la pressione dell\'acqua lo spinge contro lo scafo; dentro, la pompa di sentina scarica l\'acqua fuori bordo')+lbl,
 notes='Quiz 1.3.6-1 (tamponare dall\'esterno), -9 (materiali ingombranti per falle grandi), -5 (falla a prua: arrestare il moto), -6 (falla lieve: pompa di sentina), -7 (riserva di spinta), 1.3.5-1 (falla irreparabile: MAYDAY e salvezza delle persone). Si può anche sbandare la barca sul lato opposto per portare la falla fuori dall\'acqua (e non sul lato della falla, come dice una risposta sbagliata della 1.3.6-1).')

chapter('cap3',3,'Sinistri e abbandono',['Incaglio e collisione','Uomo a mare','Abbandonare la barca'],ORANGE,
 'Circa 12 minuti, verifica da 2 quiz compresa: sono gli argomenti più critici a bordo.','circa 12 minuti · 3 argomenti',1,art=(ring_scene(),'Illustrazione: salvagente anulare con la sagola galleggiante'))
# ============ INCAGLIO E COLLISIONE ============
def incaglio():
    s=f'<rect x="0" y="0" width="700" height="250" fill="{SKY}"/><rect x="0" y="120" width="700" height="130" fill="{WATER}" fill-opacity="0.45"/>'
    s+=f'<path d="M0 250 L0 220 Q180 200 300 170 Q380 150 460 190 Q560 225 700 215 L700 250 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
    s+=f'<g transform="rotate(-6 350 140)"><path d="M180 110 L520 100 Q510 150 470 162 L230 164 Q190 150 180 110 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><path d="M280 100 L420 96 L400 70 L300 72 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/></g>'
    s+=arrow(620,200,620,70,SEA,6,20)+f'<path d="M560 60 q20 -10 40 0 t40 0" fill="none" stroke="{SEA}" stroke-width="5"/>'
    return s
def collisione():
    s=f'<rect x="0" y="0" width="700" height="250" fill="{WATER}" fill-opacity="0.18"/>'
    s+=topboat(220,140,190,0,'#FFFFFF',NAVY,4)+topboat(470,150,190,200,'#FFFFFF',NAVY,4)
    s+=arrow(120,140,40,140,CORAL,6,18)+curved(220,140,120,-40,-100,CORAL,5)
    s+=f'<path d="M335 110 l12 -18 l6 20 l18 -10 l-8 20 l20 4 l-20 8" fill="none" stroke="{LRED}" stroke-width="5" stroke-linejoin="round"/>'
    return s
IC=[(incaglio(),'Incaglio','Nasce spesso da un punto nave impreciso sottocosta. Per disincagliare valuta fondale, danni e manovra; a volte basta attendere l\'alta marea. L\'incaglio volontario può evitare un naufragio per falla o incendio.',SEA_T),
    (collisione(),'Collisione','Se l\'urto è inevitabile: ferma il motore, metti indietro e accosta per attutire il colpo. Dopo: soccorri se serve e dai all\'altra unità i dati per identificarti. I danni da condotta irregolare si risarciscono anche senza urto, anche per il solo moto ondoso.',CORAL_T)]
cc=''.join(card(svgi(700,250,s,t,dw=752,dh=269,pan=False)+h3(t,34)+p(d,26),bg,32,12) for s,t,d,bg in IC)
sec('incaglio', head('Sicurezza · i sinistri','Incaglio e collisione')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 1.3.6-2 (incaglio volontario), -3 (fattori per il disincaglio), -4 (punto nave impreciso), -8 (alta marea), -10 (collisione: fermare, indietro e accostare), 1.3.7-12 (fornire i dati di identificazione, nei limiti del possibile), 1.8.1-4 e -43 (urto senza fornire i dati: sanzione, lezione 7), 1.8.1-1 e seguenti (evento straordinario: denuncia entro 3 giorni).')

# ============ UOMO A MARE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.14"/>'
cx_,cy_,R=520,280,170
b+=dpath(f'M{cx_-R} 600 L{cx_-R} {cy_}',NAVY,5,False)
path=f'M{cx_-R} {cy_} A{R} {R} 0 1 1 {cx_-R*math.cos(math.radians(40)):.1f} {cy_+R*math.sin(math.radians(40)):.1f}'
b+=dpath(path,CORAL,6)
b+=topboat(cx_-R,520,130,-90,'#FFFFFF',NAVY,4)+topboat(cx_+R,cy_,130,90,'#FFFFFF',NAVY,4)
px_,py_=cx_-R+70,cy_+60
b+=person(px_,py_,CORAL,1.2)+ring(px_+44,py_-6,18)
b+=f'<path d="M{cx_+R-20} {cy_-10} L{px_+20} {py_-10}" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="4 8"/>'
b+=num(cx_-R-40,420,1,NAVY,22)+num(cx_-R+20,cy_-60,2,CORAL,22)+num(px_+80,py_+40,3,ORANGE,22)+num(cx_+R+60,cy_-70,4,PURPLE,22)+num(cx_-40,cy_+R+10,5,SEA,22)
lbl=pill(X+40,Y+470,250,'«Uomo a mare a dritta!»',NAVY,22)+pill(X+40,Y+150,320,'accosta dallo stesso lato',CORAL,22)+pill(X+520,Y+368,240,'lancia il salvagente',ORANGE,22)
lbl+=pill(X+790,Y+194,260,'occhi sempre su di lui',PURPLE,22)+pill(X+510,Y+448,300,'arriva piano, in folle',SEA,22)
txt=term('Subito','Grida il lato e accosta da quello stesso lato: la poppa e le eliche si allontanano dal naufrago.')+term('Salvagente e occhi','Lancia l\'anulare vicino al naufrago e fai tenere a qualcuno il controllo visivo, senza mai staccarlo.')+term('L\'avvicinamento','Con prudenza, dopo aver perso velocità: motore in folle vicino alla persona. Col fuoribordo usa lo stacco di sicurezza.')+term('A motore e a vela','Il disegno mostra la manovra a motore. Per il recupero a vela vedi l\'appendice E, «La prova pratica».')
sec('uomoamare', head('Sicurezza · i sinistri','Uomo a mare')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Manovra di recupero vista dall\'alto: la barca che risale verso nord accosta subito a dritta dal lato del naufrago, compie un giro e torna piano verso di lui; il salvagente anulare è vicino alla persona in acqua')+lbl,
 notes='Quiz 1.3.6-28 (avvicinamento finale con prudenza, dopo aver smaltito la velocità), -29 e -35 (salvagente anulare verso il naufrago), -31, -33, -36 (accostare dallo stesso lato: eliche lontane), -32 e -34 (controllo visivo), 1.3.8-16 (stacco di sicurezza del fuoribordo). Il quiz 1.3.6-30 richiede la figura della banca (uomo caduto a prua lato dritto: manovra B). A vela: segnalare, lanciare l\'anulare, fermare la barca (panna) o accendere il motore controllando che non ci siano cime in acqua.')

# ============ ABBANDONO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="330" width="1092" height="290" fill="{WATER}" fill-opacity="0.5"/>'+line(0,330,1092,330,SEA,3)
b+=f'<g transform="rotate(12 330 330)"><path d="M90 250 L560 240 Q545 330 490 350 L150 352 Q100 330 90 250 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/><path d="M220 240 L420 236 L400 190 L240 192 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/></g>'
b+=f'<rect x="0" y="360" width="1092" height="260" fill="{WATER}" fill-opacity="0.35"/>'
b+=f'<path d="M520 300 Q640 330 740 390" fill="none" stroke="{SUN}" stroke-width="5" stroke-dasharray="10 8"/>'
b+=f'<ellipse cx="820" cy="420" rx="130" ry="36" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><path d="M720 410 Q820 290 920 410 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4"/><path d="M790 400 Q820 360 850 400 Z" fill="{INK}"/>'
b+=person(640,470,SUN,1.4)+person(700,500,SUN,1.4)
b+=f'<rect x="930" y="470" width="80" height="70" rx="14" fill="{NAVY}"/><rect x="956" y="456" width="28" height="18" rx="6" fill="none" stroke="{NAVY}" stroke-width="5"/>'
lbl=pill(X+500,Y+250,300,'sagola legata alla barca',SUN,22,INK)+pill(X+760,Y+300,200,'zattera',ORANGE,22)+pill(X+560,Y+560,220,'giubbotti a tutti',SEA,22)+pill(X+880,Y+560,160,'grab bag',NAVY,22)
lbl+=lab(X+40,Y+30,600,'Prima il MAYDAY, poi l\'abbandono',CORAL,30,900)
txt=term('Lo decide il comandante','Solo dopo aver tentato con ogni mezzo di salvare la barca. Prima i giubbotti a tutti; poi controlla le dotazioni della zattera.')+term('In zattera','Sale per primo un adulto in forze che aiuta gli altri, poi bambini e anziani; il comandante per ultimo.')+term('La zattera','Prima si lega la sagola alla barca, poi si lancia: la sagola la apre e la tiene vicina.')+term('Il grab bag','La sacca con le dotazioni della zattera, a portata di mano per portarla via.')
sec('abbandono', head('Sicurezza · l\'ultima scelta','Abbandonare la barca'), pinned=svgp(X,Y,W,Hh,b,'Barca inclinata che affonda, collegata con una sagola alla zattera di salvataggio arancione aperta in acqua; persone con i giubbotti e la sacca grab bag')+lbl+pcol(txt,532,12),
 notes='Quiz 1.3.7-1 e -13 (giubbotti a tutti, zattera equipaggiata), -2 (sagola fissata prima di lanciare), -3 e -4 (dove non tenere la zattera), -5 e -6 (grab bag), -11 (l\'abbandono lo ordina il comandante dopo aver accertato di persona che non c\'è altro da fare), 1.3.6-15 (incendio grave: preparare l\'abbandono). Zattera: obbligatoria senza limiti e fino a 50 miglia, costiera fino a 12 (DM 133/2024, slide delle dotazioni).')
X=700


chapter('cap4',4,'Radio e soccorso',['Il VHF di bordo','La portata del VHF','Le chiamate via radio','Il soccorso in mare'],BLUE,
 'Circa 15 minuti, verifica da 2 quiz compresa.','circa 15 minuti · 4 argomenti',1,art=(radio_scene(),'Illustrazione: VHF portatile sul canale 16 che trasmette'))
# ============ VHF ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
b+=f'<rect x="40" y="170" width="460" height="300" rx="40" fill="{NAVY}"/><path d="M440 170 V50" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<rect x="80" y="210" width="250" height="140" rx="16" fill="#BFE6D9"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="#2B4A6B"/>' for x in range(370,470,26) for y in range(220,350,26))
b+=''.join(f'<rect x="{80+i*70}" y="385" width="56" height="50" rx="12" fill="#2B4A6B"/>' for i in range(3))+f'<rect x="300" y="385" width="160" height="50" rx="12" fill="{LRED}"/>'
cx_,cy_,R=820,320,200
b+=f'<circle cx="{cx_}" cy="{cy_}" r="{R}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="8"/>'
for a0 in (0,180):
    p0=pol(cx_,cy_,a0,R-8); p1=pol(cx_,cy_,a0+18,R-8)
    b+=f'<path d="M{cx_} {cy_} L{p0[0]:.1f} {p0[1]:.1f} A{R-8} {R-8} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{LRED}" fill-opacity="0.85"/>'
b+=''.join(line(*pol(cx_,cy_,a,R-8),*pol(cx_,cy_,a,R-(30 if a%90==0 else 20)),NAVY,5 if a%90==0 else 3) for a in range(0,360,30))
b+=line(cx_,cy_,*pol(cx_,cy_,0,R-50),NAVY,8)+line(cx_,cy_,*pol(cx_,cy_,9,R-30),CORAL,4)+f'<circle cx="{cx_}" cy="{cy_}" r="10" fill="{NAVY}"/>'
lbl=big(X+80,Y+232,250,'16',NAVY,96)+lab(X+300,Y+396,160,'DISTRESS','#FFFFFF',22,900,'center')+lab(X+60,Y+490,460,'Canale 16 · 156,8 MHz',NAVY,26,900,'center')
lbl+=pill(X+cx_+60,Y+cy_-R-10,210,'minuti 00-03',LRED,22)+pill(X+cx_-270,Y+cy_+R-40,210,'minuti 30-33',LRED,22)+lab(X+cx_-200,Y+cy_+R+20,400,'silenzio radio: solo soccorso',NAVY,22,800,'center')
txt=term('Canale 16','Soccorso e prima chiamata; poi ci si sposta su un altro canale. Tra barche: 6, 8, 72, 77. Vicino si usa la potenza ridotta di 1 watt.')+term('Chi può usarlo','Ne risponde il comandante. Serve il certificato limitato di radiotelefonista e la licenza RTF; se è omologato non ha ispezioni periodiche. Obbligatorio oltre 6 miglia.')+term('Il codice','Il natante ha un indicativo di chiamata; imbarcazioni e navi il nominativo internazionale, per le acque internazionali.')
sec('vhf', head('Sicurezza · la radio','Il VHF di bordo')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Apparato VHF sul canale 16 e un orologio con in rosso i minuti da 00 a 03 e da 30 a 33, riservati al silenzio radio')+lbl,
 notes='Quiz 1.3.9-1 (certificato limitato di radiotelefonista), -2 e -4 (indicativo di chiamata e nominativo internazionale), -3 (VHF fisso omologato), -5 (esonero dalle ispezioni ordinarie), -8 e -10 (canale 16, 156,8 MHz), -17 e -29 (silenzio ai minuti 00-03 e 30-33), -18 (il 16 solo per la prima chiamata), -21 (canali 6, 8, 72, 77), -22 (1 watt a distanza ravvicinata), -23 (responsabile il comandante), -24, -25, -26 (portata ottica: 10-20 miglia, circa 40 con le costiere), -27 (squelch), -28 (riflettore radar). Meteomar sul 68: lezione 7.')

# ============ PORTATA DEL VHF ============
X=128
b=f'<rect width="1092" height="620" fill="#BFE6F2"/><path d="M-200 700 Q546 250 1292 700 Z" fill="#1D4E73"/>'
b+=f'<g transform="translate(180 520) rotate(-22)"><path d="M-40 0 L40 0 L30 14 L-30 14 Z" fill="#FFFFFF"/><path d="M0 0 V-60" stroke="#FFFFFF" stroke-width="3"/></g>'
b+=f'<g transform="translate(470 405)"><path d="M-40 0 L40 0 L30 14 L-30 14 Z" fill="#FFFFFF"/><path d="M0 0 V-90" stroke="#FFFFFF" stroke-width="3"/><path d="M4 -86 L4 -10 L46 -10 Z" fill="#FFFFFF"/></g>'
b+=f'<g transform="translate(900 470) rotate(20)"><path d="M-30 0 L30 0 L18 -150 L-18 -150 Z" fill="none" stroke="#DDE6EC" stroke-width="4"/><path d="M-30 0 L18 -150 M30 0 L-18 -150" stroke="#DDE6EC" stroke-width="2"/></g><path d="M920 560 Q1000 520 1092 540 L1092 620 L860 620 Z" fill="#3FAE6B"/>'
b+=line(200,455,470,318,'#FFFFFF',4)+line(470,318,955,320,'#FFFFFF',4)
b+=''.join(f'<path d="M{975+k*16} {300-k*8} q10 16 0 32" fill="none" stroke="#FFFFFF" stroke-width="3"/>' for k in range(3))
lbl=lab(X+200,Y+330,280,'tra barche 10-20 miglia',NAVY,24,900)+lab(X+600,Y+270,300,'con la costiera 40 miglia',NAVY,24,900)+lab(X+40,Y+30,600,'le onde VHF vanno in linea retta: conta l\'altezza delle antenne',NAVY,24,900)
txt=(term('Portata','Tra due barche 10-20 miglia; con le stazioni costiere, che hanno antenne alte, circa 40.')
     +term('Potenza','Vicino, sotto costa e in porto si usa la potenza ridotta di 1 W; al largo quella piena.')
     +term('DSC','Il tasto rosso invia in automatico un segnale di soccorso, urgenza o sicurezza con la posizione a navi vicine, centri di soccorso e stazioni costiere.')
     +term('Squelch','Taglia il fruscio di fondo durante l\'ascolto.'))
sec('portata', head('Sicurezza · la radio','La portata del VHF'), pinned=svgp(X,Y,W,Hh,b,'La curvatura della Terra con due barche che si parlano via VHF a 10-20 miglia e una stazione radio costiera con l\'antenna alta raggiunta a 40 miglia',pan=False)+lbl+pcol(txt,532,16),
 notes='Quiz 1.3.9-22 (1 W a distanza ravvicinata), 1.3.8-7 (DSC: segnale automatico di soccorso, urgenza o sicurezza). La portata cresce con l\'altezza delle antenne perché le onde VHF viaggiano in linea retta. Lo squelch elimina il rumore quando nessuno trasmette.')
X=700

# ============ MAYDAY ============
script=('<div style="display:flex; flex-direction:column; gap:10px; background:#16324F; padding:36px; border-radius:36px; width:820px">'
 +f'<p style="font-size:24px; font-weight:900; letter-spacing:1px; color:{DACC}">CANALE 16 · ALTA POTENZA</p>'
 +''.join(f'<p style="font-size:28px; line-height:1.35; color:{c}; font-weight:{w}">{t}</p>' for t,c,w in (
   ('MAYDAY MAYDAY MAYDAY','#FFFFFF',900),('Qui «Daphne», «Daphne», «Daphne»',DSOFT,700),('Nominativo IABC2',DSOFT,700),
   ('Posizione 42°45′ N 010°15′ E','#FFFFFF',800),('Falla a prua, stiamo affondando','#FFFFFF',800),('4 persone a bordo, abbandoniamo sulla zattera','#FFFFFF',800),('Passo','#9FB3C8',700)))+'</div>')
MC=[('MAYDAY','Soccorso: pericolo grave e imminente per persone o unità.',LRED,CORAL_T),('PAN PAN','Urgenza: sicurezza di unità o persona a rischio, ma non immediato.',SUN,SUN_T),('SÉCURITÉ','Sicurezza: avvisi di navigazione e di burrasca.',SEA,SEA_T)]
mc=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:22px 26px; border-radius:24px; border-left:10px solid {c}"><p style="font-family:{H}; font-size:36px; font-weight:700; line-height:1.05; color:{INK}">{t} ×3</p>{p(d,24,INK,600,1.35)}</div>' for t,d,c,bg in MC)
sec('mayday', head('Sicurezza · la radio','Le chiamate via radio')+f'<div style="display:flex; gap:28px; align-items:start">{script}<div style="flex:1; display:flex; flex-direction:column; gap:18px">{mc}</div></div>'+note('Chi sente un MAYDAY non risponde a caso: lo rilancia e, se può, presta soccorso. Per zittire il canale: SILENCE MAYDAY (si pronuncia «seelonce»).',CORAL,32),
 notes='Esempio di messaggio con nome e nominativo inventati. Ordine delle informazioni come nel quiz 1.3.9-19: nominativo, posizione, tipo di pericolo. Quiz 1.3.9-12, -14, -16 (MAYDAY tre volte), -13 (PAN PAN), -15 (SÉCURITÉ), -11 (chi riceve rilancia e se possibile soccorre), -20 (SILENCE MAYDAY, pronunciato «seelonce»), 1.3.5-1 (falla irreparabile: MAYDAY), 1.3.8-7 (DSC: il tasto rosso invia in automatico il soccorso con la posizione), 1.3.9-6, -7, -9 (razzi e fuochi a mano: slide Chiedere soccorso).')

# ============ CHI CI AIUTA ============
def tile(n,t,c,bg,size=72): return f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:28px; border-radius:28px"><p style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,25,INK,600,1.35)}</div>'
tiles=f'<div style="display:flex; gap:22px">{tile("1530","Il numero di emergenza della Guardia Costiera, dal telefono.",CORAL,CORAL_T)}{tile("CIRM","Centro Internazionale Radio Medico: consigli medici a distanza per un infortunio grave a bordo.",SEA,SEA_T)}{tile("SAR","Il soccorso in mare lo coordina il Comando generale delle Capitanerie di porto.",PURPLE,LILAC_T)}</div>'
arms=f'<rect x="0" y="0" width="260" height="200" fill="#F4FAFC"/><circle cx="130" cy="70" r="20" fill="#F2C9A0" stroke="{NAVY}" stroke-width="3"/><path d="M104 96 L156 96 L150 176 L110 176 Z" fill="{CORAL}"/>'+line(104,100,40,60,NAVY,8)+line(156,100,220,60,NAVY,8)+dpath('M40 60 Q30 110 60 150',GREY,3)+dpath('M220 60 Q230 110 200 150',GREY,3)+arrow(40,120,54,150,GREY,3,10)+arrow(220,120,206,150,GREY,3,10)
dtxt='<ul style="font-size:24px; line-height:1.36; color:#34465E; display:flex; flex-direction:column; gap:6px"><li>Chi è vicino presta assistenza quando può essere utile; a persone in pericolo di vita è <b>obbligatoria</b>, se non mette a rischio la propria barca e chi è a bordo.</li><li>Dopo un urto ogni comandante soccorre gli altri, se non corre un grave pericolo.</li><li>Chi non presta soccorso rischia la <b>reclusione fino a 2 anni</b>.</li><li>L\'Autorità marittima può ordinare a chi è in porto o vicino di partecipare.</li><li><b>Traino</b>: solo con polizza assicurativa e comunicazione alla Capitaneria.</li><li>Per farti notare: alza e abbassa lentamente le <b>braccia allargate</b>.</li></ul>'
dimg=svgi(260,200,arms,"Persona che alza e abbassa lentamente le braccia allargate",dw=260,dh=200,pan=False)
duty=card(f'<div style="display:flex; gap:28px; align-items:center">{dimg}<div style="display:flex; flex-direction:column; gap:10px">{h3("Gli obblighi del comandante",32)}{dtxt}</div></div>',None,32,0,'none')
sec('soccorsomare', head('Sicurezza · il soccorso','Il soccorso in mare')+tiles+duty,
 notes='Quiz 1.3.8-25 (1530), 1.3.2.113 (CIRM, unico quiz della voce 3b), 1.3.7-7 (soccorso marittimo: ricerca e salvataggio della vita umana), -8 (coordinamento: Comando generale del Corpo delle Capitanerie di porto), -9 (l\'Autorità marittima può chiedere alle unità in porto o nelle vicinanze di partecipare), -10 (obbligo di assistenza senza rischio per sé), 1.8.1-7…-10 (sanzioni per omesso soccorso, lezione 7), 1.3.8-24 (braccia allargate, segnale di pericolo). Il CIRM risponde 24 ore su 24 via radio, telefono ed e-mail.')

chapter('cap5',5,'Cattivo tempo e responsabilità',['Cattivo tempo: prepararsi','Cattivo tempo: le onde','L\'ancora galleggiante','Alcol, droghe e farmaci'],SEA,
 'Circa 13 minuti, verifica da 2 quiz compresa.','circa 13 minuti · 4 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
# ============ CATTIVO TEMPO 1 ============
X=128
b=f'<rect width="1092" height="620" fill="#C9D3DC"/>'
b+=f'<rect x="20" y="20" width="520" height="580" rx="20" fill="#DDEFF7"/><path d="M20 260 Q60 240 120 250 L160 300 L20 300 Z" fill="#8E9B6E"/><rect x="20" y="300" width="520" height="300" fill="{WATER}" fill-opacity="0.5"/>'
b+=arrow(60,200,300,200,LRED,6,18)+profile(280,320,200,sup=True)+f'<path d="M160 300 q30 -6 60 0 t60 0 t60 -8 t60 -14 t60 -20 t60 -26" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
b+=f'<rect x="552" y="20" width="520" height="580" rx="20" fill="#DDEFF7"/><path d="M552 420 Q700 220 812 300 Q920 380 1072 330 L1072 600 L552 600 Z" fill="{WATER}" fill-opacity="0.6"/>'
b+=f'<g transform="translate(800 280) rotate(-35)">{profile(-110,30,220,sup=True)}</g>'+curved(800,280,140,200,260,LRED,6)+f'<path d="M720 400 L880 560 M880 400 L720 560" stroke="{LRED}" stroke-width="10" opacity="0.8"/>'
lbl=lab(X+40,Y+40,480,'Tempesta da terra',NAVY,26,900,'center')+lab(X+40,Y+520,480,'verso la costa il mare è più calmo',NAVY,22,800,'center')+lab(X+572,Y+40,480,'Onde al traverso',NAVY,26,900,'center')+lab(X+572,Y+80,480,'la barca rischia di rovesciarsi',NAVY,22,800,'center')
txt=('<ul style="font-size:24px; line-height:1.38; color:#34465E; display:flex; flex-direction:column; gap:8px">'
     '<li><b>Rizza</b> tutti gli oggetti.</li><li>Chiudi osterigi, oblò, boccaporti e prese a mare: lascia aperta quella del <b>raffreddamento del motore</b>.</li>'
     '<li><b>Istruisci i passeggeri</b> su giubbotti e zattera; giubbotti addosso.</li><li><b>In solitario</b>: cintura di sicurezza agganciata alla life line.</li>'
     '<li>Tempesta da terra: avvicinati alla costa, al ridosso.</li><li>Mai prendere le onde <b>al traverso</b>.</li></ul>')
sec('tempo1', head('Sicurezza · il mare formato','Cattivo tempo: prepararsi'), pinned=svgp(X,Y,W,Hh,b,'A sinistra una barca che va verso la costa con la tempesta che arriva da terra e il mare più calmo vicino a riva; a destra una barca con le onde al traverso che rischia di rovesciarsi, barrata in rosso',pan=False)+lbl+pcol(txt,532,10),
 notes='Quiz 1.3.8-2 e -23 (preparare la barca: chiudere tutto tranne la presa a mare del raffreddamento del motore), -22 (in solitario cintura e assicurarsi al ponte), -3 (tempesta da terra: verso la costa), -8 (mai al traverso), -24 (per attirare l\'attenzione: braccia allargate su e giù).')
X=700

# ============ CATTIVO TEMPO 2 ============
def wave(kind):
    s=f'<rect width="320" height="200" fill="#DDEFF7"/><path d="M0 130 Q40 100 80 120 T160 120 T240 110 T320 120 L320 200 L0 200 Z" fill="{WATER}" fill-opacity="0.7"/>'
    if kind=='poppa': s+=arrow(20,80,140,80,LRED,5,14)+f'<g transform="translate(220 108) rotate(-6)">{profile(-70,10,140,sup=True)}</g>'+f'<path d="M150 116 L138 126" stroke="{LRED}" stroke-width="5"/>'
    else: s+=arrow(20,80,140,80,LRED,5,14)+f'<g transform="translate(220 108) rotate(8)">{profile(-70,10,140,sup=True)}</g>'+f'<path d="M154 102 L140 112" stroke="{LRED}" stroke-width="5"/>'
    return s
def cappa():
    s=f'<rect width="320" height="200" fill="#1D4E73"/>'+''.join(f'<path d="M{-40+i*60} 200 q30 -40 60 -80 t60 -80" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.5"/>' for i in range(8))
    s+=''.join(arrow(x,10,x,60,'#DDE6EC',4,12) for x in (60,140,220))+topboat(170,130,110,-60,'#FFFFFF',NAVY,3)
    s+=f'<path d="M220 160 Q260 120 300 140" fill="none" stroke="#9FD7E3" stroke-width="14" opacity="0.6"/>'
    return s
WV=[(wave('poppa'),'Onda da poppa','Riduci la velocità; <b>flaps alzati</b> e trim positivo, per tenere su la prua e non piantarla nell\'onda.'),
    (wave('prora'),'Onda da prora','Punta leggermente la cresta e scostati scendendo nel cavo; <b>flaps abbassati</b> e trim negativo, prua giù.'),
    (cappa(),'Alla cappa','Con la tempesta dal mare. Scarrocciando la barca lascia sopravento una scia calma, la <b>remora</b>, che smorza i frangenti.')]
cc=''.join(card(svgi(320,200,s,f'Disegno: {t}',dw=440,dh=275,pan=False)+h3(t,30)+p(d,24),None,22,10) for s,t,d in WV)
cappa_def=card(p('<b>Stare alla cappa</b> vuol dire smettere di navigare verso la meta e aspettare che passi il peggio: la barca resta quasi ferma, con onde e vento al mascone (circa 45° dalla prua), e il motore dà solo la spinta che serve per governare. A vela si sta alla cappa con poca tela, il fiocco a collo e la barra legata sottovento.',24,INK,500,1.4),SUN_T,20,6,flex='none')
sec('tempo2', head('Sicurezza · il mare formato','Cattivo tempo: le onde')+f'<div style="display:flex; gap:20px">{cc}</div>'+cappa_def,
 notes='Quiz 1.3.8-9 (puntare leggermente la cresta), -10 (onda di poppa: trim positivo), -1 (trim negativo: prua giù), -11 e -12 (flaps abbassati con mare contrario, alzati con mare di poppa), -13 e -14 (indicatore e regolazione dei flaps), -4 e -19 (alla cappa, al mascone), -5 (mare in poppa: ridurre la velocità). La remora è la scia calma che la barca lascia sopravento scarrocciando.')

# ============ ANCORA GALLEGGIANTE ============
X=128
b=f'<rect width="1092" height="620" fill="#DDEFF7"/><rect y="200" width="1092" height="420" fill="{WATER}" fill-opacity="0.45"/><path d="M0 120 Q60 140 90 200 L120 620 L0 620 Z" fill="#5E7D4E"/>'
b+=profile(420,206,220,sup=True)+line(650,190,940,200,ORANGE,4)+f'<path d="M940 186 L1000 170 L1000 230 L940 214 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/>'
b+=arrow(1060,110,900,110,LRED,6,18)+arrow(380,170,200,170,NAVY,5,16)
b+=f'<path d="M640 210 L640 540" stroke="{INK}" stroke-width="4" stroke-dasharray="6 6"/>'+f'<path d="M620 600 Q640 560 660 600" fill="none" stroke="{INK}" stroke-width="5"/><rect x="0" y="590" width="1092" height="30" fill="#2B4A6B"/>'
b+=f'<rect x="160" y="320" width="420" height="200" rx="20" fill="#FFFFFF" fill-opacity="0.85"/>'+topboat(470,430,110,0,'#FFFFFF',NAVY,3)+line(410,430,230,430,ORANGE,3)+f'<path d="M230 414 L190 430 L230 446 Z" fill="{ORANGE}"/>'+arrow(260,480,420,480,LRED,4,14)
lbl=lab(X+940,Y+70,140,'vento',LRED,24,900)+lab(X+180,Y+130,260,'scarroccio',NAVY,22,900)+lab(X+650,Y+380,260,'fondale troppo profondo per ancorare',INK,22,800)
lbl+=lab(X+180,Y+330,400,'in navigazione, filata da poppa',NAVY,22,900,'center')+lab(X+180,Y+490,400,'limita l\'intraversamento',NAVY,22,800,'center')
txt=(term('Che cos\'è','Un cono di tela che si fila in acqua con una cima: frena la barca ma non tocca il fondo.')
     +term('Alla deriva','Quando il fondale è troppo profondo per ancorare, rallenta lo scarroccio, soprattutto con una costa sottovento.')
     +term('In navigazione','Filata da poppa con il mare in poppa tiene la barca allineata alle onde e limita l\'intraversamento.'))
sec('ancora', head('Sicurezza · il mare formato','L\'ancora galleggiante'), pinned=svgp(X,Y,W,Hh,b,'Barca che scarroccia verso la costa con il vento: l\'ancora galleggiante filata sopravento la frena, perché il fondale è troppo profondo per l\'ancora normale; nel riquadro una barca in navigazione con l\'ancora galleggiante filata da poppa',pan=False)+lbl+pcol(txt,532,20),
 notes='Quiz 1.3.8-21 (limita l\'intraversamento), 1.3.8-18 (alla cappa è utile con una costa vicina sottovento: quiz oscurato). Il materiale della scuola mostra entrambi gli usi: alla deriva con fondali troppo profondi e in navigazione.')
X=700
# ============ ALCOL ============
T=[("2.755-15.000 €","la sanzione per chi conduce in stato di ebbrezza, secondo il tasso alcolemico",CORAL,CORAL_T),
   ("3-24 mesi","di sospensione della patente, sempre; revoca se c'è danno all'ambiente",PURPLE,LILAC_T),
   ("5 ore","quanto possono durare gli effetti dell'alcol",SEA,SEA_T),
   ("× 2","la sanzione per alterazione psicofisica, se c'è un sinistro",BLUE,BLUE_T)]
tiles='<div style="display:flex; gap:22px">'+''.join(tile(n,t,c,bg,44) for n,t,c,bg in T)+'</div>'
m1=p("Chi conduce dopo aver assunto stupefacenti o psicotropi: da 2.755 a 11.017 euro. I sedativi con l'alcol sono molto pericolosi: l'attenzione crolla.",27)
m2=p("Tasso tra 0,5 e 0,8 g/l: sanzioni aumentate di un terzo. Oltre 1,5 g/l: patente sempre revocata. Sospesa anche la licenza di navigazione.",27)
more=card(f'<div style="display:flex; gap:32px"><div style="flex:1; display:flex; flex-direction:column; gap:8px">{h3("Droghe e farmaci",32)}{m1}</div><div style="flex:1; display:flex; flex-direction:column; gap:8px">{h3("Unità a noleggio",32)}{m2}</div></div>',None,32,0,'none')
sec('alcol', head('Sicurezza · chi è al comando','Alcol, droghe e farmaci')+tiles+more,
 notes='Voce 3a dell\'All. A, 12 quiz (1.3.2). Quiz 1.3.2-2 (2.755-15.000 euro secondo il tasso), -3 (sospensione da 3 a 24 mesi), -1 e -5 (revoca con danno ambientale), -4 (stupefacenti: 2.755-11.017 euro), -8 (raddoppio in caso di sinistro), -6 e -10 (noleggio), -7 (sospensione della licenza di navigazione), -9 (effetti fino a 5 ore), -11 (sedativi e alcol), -12 (attenzione molto bassa). Le cifre sono quelle delle risposte della banca: il riferimento è l\'art. 53-bis del Codice della nautica.')


chapter('capquiz',6,'Raccolta quiz',['Dotazioni e distanze','Fuochi e razzi','Falla e incaglio','Le dotazioni','Segnali di soccorso','Il fuoco','Gli estintori','Incendio a bordo','Sinistri e abbandono','Radio e soccorso','Cattivo tempo','Alcol e farmaci'],GREEN,
 'Inizio degli ultimi 45 minuti: 12 slide da 3 quiz ufficiali, ognuna seguita dalle risposte.','36 quiz ufficiali',2,'Ultimi 45 minuti','45′',art=(quiz_scene(),'Illustrazione: scheda di quiz con le risposte segnate e un cronometro sui 45 minuti'))
# ============ RACCOLTA QUIZ (45 minuti) ============
steps=[('1','Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.',CORAL,CORAL_T),
 ('2','Conta le miglia','Le dotazioni cambiano con la distanza dalla costa: 300 m, 3, 6, 12, 50 miglia.',SEA,SEA_T),
 ('3','Cerca lo scambio','Sopravento o sottovento, polvere o CO2, MAYDAY o PAN PAN: il trabocchetto è lì.',PURPLE,LILAC_T),
 ('4','Attento ai numeri','Miglia dalla costa, minuti, metri, canali: controlla il numero e l\'unità.',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,30,INK,800,1.2)}{p(d,24,INK,500,1.35)}</div>' for n,t,d,c,bg in steps)
exam=esame_box(['sicurezza'],6,compact=True)
plan=card(tag("I 45 minuti",SEA)+'<ol style="font-size:24px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px"><li>Quiz 1-2 e 4-5 · dotazioni e segnali di soccorso (12)</li><li>Quiz 3 e 6-9 · falla, incendio, sinistri, abbandono (15)</li><li>Quiz 10-12 · radio, cattivo tempo, alcol (9)</li></ol>',SEA_T,32,12)
sec('quiz', head('Lezione 06 · ultimi 45 minuti','Raccolta quiz')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div><div style="display:flex; gap:24px">{exam}{plan}</div>',
 notes='Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Se il tempo stringe, lasciare per casa le slide 7 e 11.', gap=28)
E='Raccolta quiz · DD 131/2022'
QZ=[('q01','Quiz 1 · Dotazioni e distanze',['1.3.3-12','1.3.3-13','1.3.3-15']),('q02','Quiz 2 · Fuochi e razzi',['1.3.3-16','1.3.3-28','1.3.9-7']),
    ('q03','Quiz 3 · Falla e incaglio',['1.3.6-5','1.3.6-8','1.3.6-6']),('q04','Quiz 4 · Le dotazioni',['1.3.3-22','1.3.3-20','1.3.3-24']),
    ('q05','Quiz 5 · Segnali di soccorso',['1.3.3-17','1.3.3-43','1.3.9-6']),('q06','Quiz 6 · Il fuoco',['1.3.1-24','1.3.1-14','1.3.1-18']),
    ('q07','Quiz 7 · Gli estintori',['1.3.1-2','1.3.1-9','1.3.1-13']),('q08','Quiz 8 · Incendio a bordo',['1.3.6-13','1.3.6-14','1.3.6-11']),
    ('q09','Quiz 9 · Sinistri e abbandono',['1.3.6-1','1.3.6-31','1.3.7-2']),('q10','Quiz 10 · Radio e soccorso',['1.3.9-17','1.3.9-8','1.3.9-12']),
    ('q11','Quiz 11 · Cattivo tempo',['1.3.8-3','1.3.8-17','1.3.8-25']),('q12','Quiz 12 · Alcol e farmaci',['1.3.2-9','1.3.2-12','1.3.2-11'])]
for id_,t,ps in QZ:
    quiz_slide(id_,t,ps,False,E)
    quiz_slide(id_+'r',t+' · risposte',ps,True)
closing(['Zattera costiera tra 6 e 12 miglia, d\'altura oltre; binocolo e riflettore radar oltre 12, EPIRB oltre 50','Fuochi a mano se vedi chi ti aiuta, razzi a paracadute se lo presumi; i pirotecnici scadono in 4 anni','Incendio: CO2 per l\'elettrico, mai acqua; fiamme sottovento, carburante chiuso','Falla: tappo di fortuna da fuori e pompa di sentina; se è a prua ferma la barca','Uomo a mare: accosta dal suo lato; radio: MAYDAY, PAN PAN, SÉCURITÉ sul 16; cattivo tempo: mai onde al traverso'],
 'Prossima lezione · 07 · Meteorologia e Normativa','A casa: i quiz su dotazioni e incendio (1.3.1, 1.3.3) e su sinistri, radio e soccorso (1.3.2, 1.3.5-1.3.9).')
exec(open('intermedi.py').read())
intermedi([('binocolo','v1','Verifica · Le dotazioni',['1.3.3-34','1.3.3-3']),
 ('falla','v2','Verifica · Incendio e falla',['1.3.1-1','1.3.6-22']),
 ('abbandono','v3','Verifica · Sinistri e abbandono',['1.3.6-36','1.3.7-6']),
 ('soccorsomare','v4','Verifica · Radio e soccorso',['1.3.9-13','1.3.9-20']),
 ('alcol','v5','Verifica · Cattivo tempo e alcol',['1.3.8-8','1.3.8-21'])])
write_deck(OUT,'Lezione 06 · La sicurezza e i suoi elementi nella navigazione',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Dotazioni: tabelle, zattera, giubbotti, pirotecnici, EPIRB, binocolo e pronto soccorso","start":"cap1"},
  "s3":{"description":"Triangolo del fuoco, classi, estintori, incendio, falla","start":"cap2"},"s4":{"description":"Incaglio, collisione, uomo a mare, abbandono","start":"cap3"},
  "s5":{"description":"VHF, portata, chiamate, soccorso","start":"cap4"},"s6":{"description":"Cattivo tempo, ancora galleggiante, alcol","start":"cap5"},"s7":{"description":"Raccolta quiz","start":"capquiz"}})
