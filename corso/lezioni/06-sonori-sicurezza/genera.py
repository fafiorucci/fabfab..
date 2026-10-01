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
cover(6,'Segnali sonori, sicurezza ed emergenze','Fischi, nebbia e porti; le dotazioni del DM 133/2024, l&#39;incendio e le emergenze a bordo',
 'Lezione 6. Capitoli del programma della scuola: Segnali sonori, Sicurezza (dotazioni, mezzi di soccorso, incendio) ed emergenze (falla, incaglio, collisione, uomo a mare, abbandono, VHF, soccorso, tempo cattivo, 3). Aggiunte dall\'All. A: dotazioni obbligatorie secondo il DM 133/2024 (punto 3b), precauzioni all\'ingresso e all\'uscita dei porti (punto 4a), CIRM (3b), alcol e sostanze (3a). Fari e segnalamento AISM-IALA sono nella lezione 3. Gli ultimi 45 minuti sono una raccolta di quiz ufficiali.')
blocks=[('0:00','25′','Suoni, porti, dotazioni e soccorso',CORAL),('0:25','25′','Incendio, sinistri e abbandono',PURPLE),('0:50','25′','Radio, soccorso, meteo, alcol',BLUE),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">1 + 3</p>'+p('domande su 20: COLREG (segnali sonori), Sicurezza (dotazioni ed emergenze)',26,INK,700)+p('Più la manovra in porto, che rientra nelle 4 domande di Manovra e condotta.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>capire e usare i segnali sonori</li><li>entrare e uscire da un porto in sicurezza</li><li>preparare la barca con le dotazioni giuste</li><li>spegnere un incendio e recuperare un uomo a mare</li><li>lanciare un MAYDAY sul canale 16</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 06 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Tre capitoli di teoria in 75 minuti, ognuno con 2 quiz di verifica dopo ogni paragrafo: andare spediti sulle slide, il dettaglio è nelle note. Poi 45 minuti di raccolta quiz. Banca DD 131/2022: prevenire gli abbordi 60 (1.5.2, per i segnali sonori), porti 21 (1.4.1), incendio ed estintori 31 (1.3.1), dotazioni di sicurezza 48 (1.3.3, 14 oscurati), sinistri 36 (1.3.6), abbandono e soccorso 13 (1.3.7) più il CIRM (1.3.2.113), tempo cattivo 25 (1.3.8), radio 29 (1.3.9) più 1.3.5, alcol 12 (1.3.2). Attenzione: il DM 133/2024 ha riscritto l\'Allegato V del DM 146/2008; dove un quiz non oscurato diverge, all\'esame vale la risposta dell\'elenco ministeriale.')
X=700

chapter('cap1',1,'Segnali sonori, porti e dotazioni',['I segnali sonori di manovra','Nella nebbia','Entrare e uscire dal porto','Le dotazioni: salvarsi','Le dotazioni: navigare e comunicare','Chiedere soccorso'],CORAL,
 'Circa 25 minuti, compresi i 2 quiz di verifica dopo i porti e dopo i segnali di soccorso. Andare spediti. Quiz 1-5 nella raccolta finale.','circa 25 minuti · 6 argomenti',1,art=(ring_scene(),'Illustrazione: salvagente anulare con la sagola galleggiante'))
# ============ SEGNALI SONORI ============
def snd(seq):
    g=f'<rect x="0" y="0" width="260" height="60" rx="14" fill="{NIGHT}"/>'; x=18
    for s_ in seq:
        wdt=26 if s_=='.' else 80; g+=f'<rect x="{x}" y="20" width="{wdt}" height="20" rx="10" fill="{SUN}"/>'; x+=wdt+12
    return g
SS=[('.','Accosto a dritta',SEA),('..','Accosto a sinistra',SEA),('...','Macchine indietro',SEA),('--.','Voglio sorpassarti a dritta',PURPLE),('--..','Voglio sorpassarti a sinistra',PURPLE),('-','Curva cieca o uscita dal porto senza visibilità',CORAL),('.....','Non capisco le tue intenzioni: attenzione!',CORAL)]
cells=''.join(f'<div style="display:flex; gap:18px; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 18px; border-radius:20px; border-left:10px solid {c}">{svgi(260,60,snd(sq),"Sequenza di suoni",dw=260,dh=60,pan=False)}{p(t,26,INK,800,1.25)}</div>' for sq,t,c in SS)
legend=f'<div style="display:flex; gap:28px; align-items:center">{svgi(260,60,snd("."),"Suono breve",dw=130,dh=30,pan=False)}{p("breve: circa 1 secondo",24,INK,700)}{svgi(260,60,snd("-"),"Suono prolungato",dw=130,dh=30,pan=False)}{p("prolungato: da 4 a 6 secondi",24,INK,700)}</div>'
sec('sonori', head('COLREG · con il fischio','I segnali sonori di manovra')+legend+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px">{cells}</div>', gap=24,
 notes='Quiz 1.5.2-21 e -49 (1 breve = accosto a dritta), -23 e -28 (2 brevi = a sinistra), -22, -37, -48, -50 (sorpasso: 2 prolungati + 1 breve a dritta, + 2 brevi a sinistra), 1.4.1-15 e 1.5.3-116 (1 prolungato uscendo dal porto o in una curva cieca). I 3 brevi (macchine indietro) e i 5 brevi (dubbio) sono della regola 34 del COLREG. Apparecchi sonori: 1.5.2-13 e -51 (sotto i 12 m qualsiasi mezzo sonoro efficace), DM 133/2024 (fischio e campana per le unità oltre 12 m).')

# ============ NEBBIA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#DDE6EC"/><path d="M0 470 Q273 456 546 470 T1092 466 L1092 620 L0 620 Z" fill="{WATER}" fill-opacity="0.35"/>'
b+=profile(330,474,420,sup=True)
b+=''.join(f'<path d="M{700+r*0.2:.0f} {380-r:.0f} A{r} {r} 0 0 1 {700+r*0.2:.0f} {380+r*0.6:.0f}" fill="none" stroke="{SUN}" stroke-width="6" stroke-linecap="round" opacity="{1-r/260:.2f}"/>' for r in (60,110,160,210))
b+=''.join(f'<rect x="0" y="{y}" width="1092" height="{h}" fill="#FFFFFF" fill-opacity="0.45"/>' for y,h in ((60,60),(200,50),(390,70)))
lbl=lab(X+60,Y+40,400,'ogni 2 minuti al massimo',NAVY,26,900)
FG=[('-','A motore, con abbrivio'),('--','A motore, ferma senza abbrivio'),('-..','A vela'),]
fg=''.join(f'<div style="display:flex; gap:16px; align-items:center">{svgi(260,60,snd(sq),"Segnale da nebbia",dw=200,dh=46,pan=False)}{p(t,25,INK,800,1.25)}</div>' for sq,t in FG)
txt=fg+term('Alla fonda','Oltre i 20 m: rapidi colpi di campana per 5 secondi, almeno ogni minuto.')+term('Visibilità ridotta','Nebbia, pioggia, neve, fumo: velocità di sicurezza e fanali accesi.')
sec('nebbia', head('COLREG · visibilità ridotta','Nella nebbia')+col(txt,560,18), pinned=svgp(X,Y,W,Hh,b,'Barca nella nebbia che emette segnali sonori, con banchi di nebbia sul mare')+lbl,
 notes='Quiz 1.5.2-20 e -53 (motore con abbrivio: 1 prolungato ogni 2 minuti al massimo), -40 (motore fermo senza abbrivio: 2 prolungati), -52 (vela: 1 prolungato e 2 brevi), -35 (fonda oltre 20 m: campana per 5 secondi ogni minuto), -3 (visibilità ridotta), -10 (velocità di sicurezza), -12 (fanali accesi con visibilità ridotta), -14 (segnale di pericolo: suono continuo). Il quiz 1.5.2-36 sulla campana è oscurato.')

# ============ PORTO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
b+=f'<path d="M0 0 L1092 0 L1092 80 L0 80 Z" fill="{LAND}"/><path d="M180 80 L180 300 L460 300 L460 260 L220 260 L220 80 Z" fill="#C9C2B2" stroke="{NAVY}" stroke-width="3"/><path d="M900 80 L900 300 L632 300 L632 260 L860 260 L860 80 Z" fill="#C9C2B2" stroke="{NAVY}" stroke-width="3"/>'
b+=glow(460,280,LRED,8)+glow(632,280,LGREEN,8)
b+=topboat(546,200,110,90,'#FFFFFF',NAVY,4)+dpath('M546 260 L546 330',SEA,4)
b+=topboat(700,500,110,-100,'#FFFFFF',NAVY,4)
b+=f'<path d="M100 620 A480 420 0 0 1 992 620" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="12 8"/>'
lbl=lab(X+290,Y+310,160,'rosso',LRED,24,900,'right')+lab(X+650,Y+310,160,'verde',LGREEN,24,900)+lab(X+620,Y+110,220,'B esce: ha la precedenza',SEA,24,900)+lab(X+760,Y+470,260,'A entra: aspetta',NAVY,24,900)+lab(X+40,Y+420,300,'da qui, 500 m: rallenta',CORAL,24,900)
txt=term('Chi esce ha la precedenza','Di norma, salvo le ordinanze locali. Si lascia manovrare anche le navi grandi.')+term('Rallenta','Riduci la velocità a 500 m dall\'ingresso e non entrare a vela, salvo ordinanze locali.')+term('Nel canale','Tieniti sulla dritta. Uscendo senza visibilità: un suono prolungato e ascolta.')+term('Porto commerciale','Senza servizi per il diporto: avvisa l\'Autorità marittima.')
sec('porto', head('Condotta · i porti','Entrare e uscire dal porto'), pinned=svgp(X,Y,W,Hh,b,'Imboccatura di un porto vista dall\'alto: fanale rosso a sinistra e verde a dritta, la barca B che esce ha la precedenza, la barca A che entra aspetta fuori; arco dei 500 metri')+lbl+pcol(txt,532,20),
 notes='Quiz 1.4.1-4, -9, -17 (precedenza a chi esce; chi transita nei 500 m davanti all\'ingresso cede a chi entra ed esce), -6 (navi grandi), -10 (ridurre a 500 m), -12 (non si entra a vela), -19 (nel canale tenersi a dritta), -3 (porti con obbligo di tenere la dritta: ordinanze), -5 (porto commerciale: avvisare l\'Autorità marittima), -7, -8, -13, -14 (fanali dell\'imboccatura), -15 (1 prolungato uscendo), -16 (danni da moto ondoso), -20 (ormeggi in transito 72 ore), -21 (ormeggi per persone con disabilità), -1 (sanzione da 414 a 2.066 euro), -18 (ordinanze). I quiz -2 e -11 (3 nodi) sono oscurati: il limite lo fissa l\'ordinanza del porto.')
X=700


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
sec('dotazioni1', head('Sicurezza · DM 133/2024, Allegato V','Le dotazioni: salvarsi')+table(T1)+p('Mezzi collettivi e individuali per tutte le persone a bordo. Di notte, in solitario, il giubbotto si indossa sempre.',24,INK,700), gap=22,
 notes='Tabella dall\'Allegato V al DM 146/2008 come sostituito dal DM 17 settembre 2024 n. 133 (G.U. S.O. n. 35 del 21/09/2024, in vigore dal 21/10/2024). Colonne: senza limiti (qui «oltre 50»), entro 50, 12, 6, 3, 1 miglio, 300 m; esistono anche le acque interne. Entro 300 m nessuna dotazione obbligatoria in tabella. Tavole, derive, kitesurf, moto d\'acqua: dispositivo di galleggiamento da 50 N sempre indossato. Fuochi a mano sostituibili con dispositivo a LED SOLAS/MED. Quiz che divergono dalla nuova tabella e che all\'esame vanno risposti come nell\'elenco: 1.3.3-15 (entro 300 m salvagente e cinture), 1.3.3-12 (cinture oltre 300 m). Oscurati: 1.3.3-4, -6, -9, -11, -14, -23, -25, -26, -32, -33, -35, -36, -41, -42.')
sec('dotazioni2', head('Sicurezza · DM 133/2024, Allegato V','Le dotazioni: navigare e comunicare')+table(T2)+p('Bussola elettronica e cartografia elettronica conforme sono ammesse. Gli estintori seguono il manuale del proprietario (unità CE).',24,INK,700), gap=22,
 notes='Stessa tabella del DM 133/2024. Quiz coerenti: 1.3.3-1 e -40 (VHF oltre 6 miglia, cioè da «entro 12»), -22 e -34 (EPIRB oltre 50), -24 (riflettore radar oltre 12), -43 (binocolo oltre 12), -39 (entro 12 niente EPIRB), -30 (radar non obbligatorio), -5 (bussola e tabelle), 1.3.3-8 (fanali di notte oltre 1 miglio), 1.7.3-7 (GPS oltre 12), 1.7.5-71 (strumenti da carteggio oltre 12). Pronto soccorso: tabella D del decreto 1° ottobre 2015 (1.3.3-45…-47). Estintori: 1.3.1-29 e -30 (manuale del proprietario; per le unità non CE il regolamento), 1.3.3-2 (natante entro 6 miglia: almeno 1).')

# ============ SEGNALI DI SOCCORSO ============
def smoke():
    return f'<rect x="0" y="0" width="300" height="200" fill="#EAF4F7"/><rect x="0" y="150" width="300" height="50" fill="{WATER}" fill-opacity="0.35"/><rect x="130" y="130" width="40" height="30" rx="6" fill="{ORANGE}" stroke="{NAVY}" stroke-width="2"/>'+''.join(f'<circle cx="{150+dx}" cy="{110-i*22}" r="{20+i*6}" fill="{ORANGE}" fill-opacity="{0.55-i*0.1:.2f}"/>' for i,dx in enumerate((0,14,30,50)))
def handflare():
    return f'<rect x="0" y="0" width="300" height="200" fill="{NIGHT}"/><rect x="140" y="90" width="20" height="90" rx="6" fill="{CORAL}"/>'+glow(150,76,LRED,14)+''.join(f'<circle cx="{150+dx}" cy="{50-i*16}" r="{8+i*3}" fill="#AAB6C3" fill-opacity="0.3"/>' for i,dx in enumerate((0,-8,-4)))
def rocket():
    return f'<rect x="0" y="0" width="300" height="200" fill="{NIGHT}"/><path d="M110 60 Q150 20 190 60 Z" fill="#DDE6EC"/><path d="M110 60 L150 100 M190 60 L150 100 M150 60 L150 100" stroke="#DDE6EC" stroke-width="2"/>'+glow(150,108,LRED,12)+dpath('M60 200 Q80 120 130 90',"#6B7F95",3)
def epirb():
    return f'<rect x="0" y="0" width="300" height="200" fill="#EAF4F7"/><rect x="0" y="150" width="300" height="50" fill="{WATER}" fill-opacity="0.35"/><rect x="126" y="70" width="48" height="96" rx="16" fill="{MYEL}" stroke="{NAVY}" stroke-width="3"/><path d="M150 70 V20" stroke="{NAVY}" stroke-width="5"/>'+glow(150,84,LWHITE,6)+''.join(f'<path d="M{150+r} 20 A{r} {r} 0 0 0 {150+r} {20+r*0.01:.0f}" fill="none"/>' for r in ())+''.join(f'<path d="M{170+i*14} {30-i*6} q10 10 0 20" fill="none" stroke="{NAVY}" stroke-width="3"/>' for i in range(3))
SG=[(smoke(),'Boetta fumogena','Fumo arancione: è un segnale <b>diurno</b>.'),(handflare(),'Fuochi a mano','Luce rossa, visibili a circa <b>6 miglia</b>.'),
    (rocket(),'Razzi a paracadute','Luce rossa per meno di 1 minuto: <b>25 miglia</b> di notte, 7 di giorno.'),(epirb(),'EPIRB','Trasmette la posizione su 406 e 121,5 MHz. Obbligatorio oltre 50 miglia.')]
cc=''.join(card(svgi(300,200,s,f'Disegno: {t}',dw=300,dh=200,pan=False)+h3(t,28)+p(d,23),None,22,10) for s,t,d in SG)
sec('soccorso', head('Sicurezza · i segnali di soccorso','Chiedere soccorso')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Pirotecnici: scadenza di solito 4 anni. Controlla la data prima di uscire.',CORAL,36),
 notes='Quiz 1.3.3-3 e -20 (boetta fumogena arancione, segnale diurno), -16 (fuochi a mano 6 miglia), -17, -28, -29 (razzi: 25 miglia di notte, 7 di giorno, meno di 1 minuto), -21 (scadenza 4 anni), -22 e -34 (EPIRB oltre 50 miglia), -7 e -18 (quantità, coerenti con il DM 133/2024). Il riflettore radar (1.5.3-10, 1.3.3-24) rende la barca visibile ai radar. VHF e chiamate di soccorso più avanti in questa lezione.')


chapter('cap2',2,'Incendio e sinistri',['Il triangolo del fuoco','Classi di incendio ed estintori','Incendio a bordo','La falla','Incaglio e collisione','Uomo a mare','Abbandonare la barca'],PURPLE,
 'Circa 25 minuti, compresi i 2 quiz di verifica dopo l\'incendio e dopo l\'abbandono. Andare spediti. Quiz 6-9 nella raccolta finale.','circa 25 minuti · 7 argomenti',1,art=(fire_scene(),'Illustrazione: estintore accanto a una fiamma'))
# ============ TRIANGOLO DEL FUOCO ============
A=(546,70); B_=(236,560); C=(856,560)
b=f'<rect x="0" y="0" width="1092" height="620" fill="#FFF1E6"/>'
b+=f'<path d="M{A[0]} {A[1]} L{B_[0]} {B_[1]}" stroke="{CORAL}" stroke-width="22" stroke-linecap="round"/><path d="M{B_[0]} {B_[1]} L{C[0]} {C[1]}" stroke="{SUN}" stroke-width="22" stroke-linecap="round"/><path d="M{C[0]} {C[1]} L{A[0]} {A[1]}" stroke="{BLUE}" stroke-width="22" stroke-linecap="round"/>'
b+=f'<path d="M546 470 C470 430 480 350 530 300 C520 350 560 360 560 330 C590 380 640 400 610 460 C600 480 570 480 546 470 Z" fill="{ORANGE}"/><path d="M546 470 C510 450 515 410 540 380 C545 410 565 420 575 400 C590 430 580 470 546 470 Z" fill="{SUN}"/>'
lbl=lab(X+70,Y+280,260,'Combustibile',CORAL,30,900,'right')+lab(X+770,Y+280,300,'Comburente (ossigeno)',BLUE,30,900)+lab(X+396,Y+580,300,'Calore',SUN,30,900,'center')
txt=term('La combustione','Una reazione tra combustibile e comburente che produce calore. Servono tutti e tre i lati.')+term('Come si spegne','Togli un lato: raffreddamento (calore), soffocamento (ossigeno), separazione (combustibile).')+term('Prevenzione','Niente stracci unti nel vano motore, aera prima di avviare un motore a benzina. L\'aria che entra alimenta l\'incendio.')
sec('fuoco', head('Sicurezza · incendio','Il triangolo del fuoco')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Triangolo del fuoco con una fiamma al centro: lati combustibile, comburente e calore')+lbl,
 notes='Quiz 1.3.1-24 (triangolo: combustibile, comburente, calore), -27 (combustione), -31 (comburente), -25 e -26 (si spegne abbassando la temperatura o togliendo l\'ossigeno), -10 (l\'aria alimenta l\'incendio), -5 (stracci unti), -28 (temperatura di infiammabilità). Il ciclo di aerazione del vano motore a benzina è nella lezione 2.')

# ============ CLASSI ED ESTINTORI ============
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
ext=''.join(f'<div style="display:flex; justify-content:space-between; gap:10px; background:#FFFFFF; {SHADOW}; padding:8px 14px; border-radius:14px">{p(a,24,INK,800)}{p(b_,24,SEA,800)}</div>' for a,b_ in [('Polvere','tutte'),('CO2','B, C, E'),('Schiuma','A, B'),('Acqua','mai su D ed E')])
txt=f'<div style="display:flex; flex-direction:column; gap:10px">{cls}</div>'+ext+p('Getto alla base delle fiamme. Revisione se la lancetta è nel rosso o dopo l\'uso.',24,INK,700)
sec('estintori', head('Sicurezza · incendio','Classi di incendio ed estintori'), pinned=svgp(X,Y,W,Hh,b,'Estintore con etichetta 13B e il suo manometro con la lancetta nella zona verde')+lbl+pcol(txt,532,14),
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
txt=term('Fiamme sottovento','Manovra perché il fuoco resti sottovento: se è a poppa metti la prua al vento, se è a prua la poppa. Mai correre verso il porto: il vento alimenta il fuoco.')+term('Nel vano motore','Chiudi subito carburante e prese d\'aria. Estintore alla base della fiamma; a polvere sul quadro elettrico.')+term('Le persone prima','Primo ordine: giubbotti e lontano dal fuoco. In porto allontana la barca; se è grave prepara l\'abbandono.')
sec('incendio', head('Sicurezza · i sinistri','Incendio a bordo'), pinned=svgp(X,Y,W,Hh,b,'Due barche viste dall\'alto con il vento da nord: con il fuoco a poppa la barca mette la prua al vento; con il fuoco a prua mette la poppa al vento; in entrambi i casi fiamme e fumo vanno sottovento')+lbl+pcol(txt,532,20),
 notes='Estintori e classi di fuoco nella slide precedente. Quiz 1.3.6-11 (non accelerare verso il porto), -12 e -24 (chiudere carburante e vie d\'aria), -13, -18, -22, -25 (fiamme sottovento: fuoco a poppa prua al vento, fuoco a prua poppa al vento), -14 (base della fiamma), -15 (grave: preparare l\'abbandono), -16 (quadro elettrico: polvere), -17 (giubbotti e allontanarsi), -19 (in porto: allontanare l\'unità), -20 (ventilazione forzata prima di avviare un motore a benzina), -21 e -23 (raffreddamento e soffocamento), -26 e -27 (numero di estintori).')
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
lbl=pill(X+812,Y+318,300,'tampone dall\'esterno',ORANGE,22)+pill(X+800,Y+452,280,'pressione dell\'acqua',SEA,22)+pill(X+410,Y+440,220,'pompa di sentina',NAVY,22)
lbl+=pill(X+880,Y+140,190,'riserva di spinta',CORAL,22)+lab(X+620,Y+520,300,'acqua che entra',SEA,22,800)
txt=term('Perché è grave','Ogni litro che entra toglie riserva di spinta: il volume stagno sopra la linea di galleggiamento.')+term('Tappare','Il tampone va messo da fuori: la pressione dell\'acqua lo spinge contro lo scafo. Per una falla grande: tele cerate, materassi, cuscini.')+term('Rallentare ed esaurire','Falla a prua: ferma la barca, l\'avanzamento spinge dentro altra acqua. Se è piccola basta la pompa di sentina; se è irreparabile, MAYDAY.')
sec('falla', head('Sicurezza · i sinistri','La falla')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Sezione di uno scafo con una falla sotto la linea di galleggiamento: il tampone è applicato dall\'esterno e la pressione dell\'acqua lo spinge contro lo scafo; dentro, la pompa di sentina scarica l\'acqua fuori bordo')+lbl,
 notes='Quiz 1.3.6-1 (tamponare dall\'esterno), -9 (materiali ingombranti per falle grandi), -5 (falla a prua: arrestare il moto), -6 (falla lieve: pompa di sentina), -7 (riserva di spinta), 1.3.5-1 (falla irreparabile: MAYDAY e salvezza delle persone). Si può anche sbandare la barca sul lato opposto per portare la falla fuori dall\'acqua (e non sul lato della falla, come dice una risposta sbagliata della 1.3.6-1).')

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
    (collisione(),'Collisione','Se l\'urto è inevitabile: ferma il motore, metti indietro e accosta per attutire il colpo. Dopo: soccorri se serve e dai all\'altra unità i dati per identificarti.',CORAL_T)]
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
txt=term('Subito','Grida il lato e accosta da quello stesso lato: la poppa e le eliche si allontanano dal naufrago.')+term('Salvagente e occhi','Lancia l\'anulare vicino al naufrago e fai tenere a qualcuno il controllo visivo, senza mai staccarlo.')+term('L\'avvicinamento','Con prudenza, dopo aver perso velocità: motore in folle vicino alla persona. Col fuoribordo usa lo stacco di sicurezza.')
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
txt=term('Lo decide il comandante','Solo dopo aver provato tutto quello che l\'arte nautica consente. Prima fa indossare a tutti il giubbotto e controlla la zattera.')+term('La zattera','Si lega la sagola alla barca e poi si lancia: la sagola la apre e la tiene vicina. Sta in coperta, pronta: mai sottocoperta o in un gavone chiuso.')+term('Il grab bag','La sacca con le dotazioni della zattera, a portata di mano per portarla via.')
sec('abbandono', head('Sicurezza · l\'ultima scelta','Abbandonare la barca'), pinned=svgp(X,Y,W,Hh,b,'Barca inclinata che affonda, collegata con una sagola alla zattera di salvataggio arancione aperta in acqua; persone con i giubbotti e la sacca grab bag')+lbl+pcol(txt,532,20),
 notes='Quiz 1.3.7-1 e -13 (giubbotti a tutti, zattera equipaggiata), -2 (sagola fissata prima di lanciare), -3 e -4 (dove non tenere la zattera), -5 e -6 (grab bag), -11 (l\'abbandono lo ordina il comandante dopo aver accertato di persona che non c\'è altro da fare), 1.3.6-15 (incendio grave: preparare l\'abbandono). Zattera: obbligatoria senza limiti e fino a 50 miglia, costiera fino a 12 (DM 133/2024, slide delle dotazioni).')
X=700


chapter('cap3',3,'Radio, soccorso, meteo, alcol',['Il VHF di bordo','Chiamare aiuto via radio','Chi ci aiuta','Il cattivo tempo','Alcol, droghe e farmaci'],BLUE,
 'Circa 25 minuti, compresi i 2 quiz di verifica finali del capitolo. Andare spediti. Quiz 10-12 nella raccolta finale.','circa 25 minuti · 5 argomenti',1,art=(radio_scene(),'Illustrazione: VHF portatile sul canale 16 che trasmette'))
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
txt=term('Canale 16','Soccorso e prima chiamata; poi ci si sposta su un altro canale. Tra barche: 6, 8, 72, 77. Vicino si usa la potenza ridotta di 1 watt.')+term('Portata','Onde in linea retta: tra barche 10-20 miglia, con le stazioni costiere circa 40.')+term('Chi può usarlo','Serve il certificato limitato di radiotelefonista. Il natante ha un indicativo di chiamata, imbarcazioni e navi il nominativo internazionale.')
sec('vhf', head('Sicurezza · la radio','Il VHF di bordo')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Apparato VHF sul canale 16 e un orologio con in rosso i minuti da 00 a 03 e da 30 a 33, riservati al silenzio radio')+lbl,
 notes='Quiz 1.3.9-1 (certificato limitato di radiotelefonista), -2 e -4 (indicativo di chiamata e nominativo internazionale), -3 (VHF fisso omologato), -5 (esonero dalle ispezioni ordinarie), -8 e -10 (canale 16, 156,8 MHz), -17 e -29 (silenzio ai minuti 00-03 e 30-33), -18 (il 16 solo per la prima chiamata), -21 (canali 6, 8, 72, 77), -22 (1 watt a distanza ravvicinata), -23 (responsabile il comandante), -24, -25, -26 (portata ottica: 10-20 miglia, circa 40 con le costiere), -27 (squelch), -28 (riflettore radar). Meteomar sul 68: lezione 7.')

# ============ MAYDAY ============
script=('<div style="display:flex; flex-direction:column; gap:10px; background:#16324F; padding:36px; border-radius:36px; width:820px">'
 +f'<p style="font-size:24px; font-weight:900; letter-spacing:1px; color:{DACC}">CANALE 16 · ALTA POTENZA</p>'
 +''.join(f'<p style="font-size:28px; line-height:1.35; color:{c}; font-weight:{w}">{t}</p>' for t,c,w in (
   ('MAYDAY MAYDAY MAYDAY','#FFFFFF',900),('Qui «Daphne», «Daphne», «Daphne»',DSOFT,700),('Nominativo IABC2',DSOFT,700),
   ('Posizione 42°45′ N 010°15′ E','#FFFFFF',800),('Falla a prua, stiamo affondando','#FFFFFF',800),('4 persone a bordo, abbandoniamo sulla zattera','#FFFFFF',800),('Passo','#9FB3C8',700)))+'</div>')
MC=[('MAYDAY','Soccorso: pericolo grave e imminente per persone o unità.',LRED,CORAL_T),('PAN PAN','Urgenza: sicurezza di unità o persona a rischio, ma non immediato.',SUN,SUN_T),('SÉCURITÉ','Sicurezza: avvisi di navigazione e di burrasca.',SEA,SEA_T)]
mc=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:{bg}; padding:22px 26px; border-radius:24px; border-left:10px solid {c}"><p style="font-family:{H}; font-size:36px; font-weight:700; line-height:1.05; color:{INK}">{t} ×3</p>{p(d,24,INK,600,1.35)}</div>' for t,d,c,bg in MC)
sec('mayday', head('Sicurezza · la radio','Chiamare aiuto via radio')+f'<div style="display:flex; gap:28px; align-items:start">{script}<div style="flex:1; display:flex; flex-direction:column; gap:18px">{mc}</div></div>'+note('Chi sente un MAYDAY non risponde a caso: lo rilancia e, se può, presta soccorso. Per zittire il canale: SILENCE MAYDAY (si pronuncia «seelonce»).',CORAL,32),
 notes='Esempio di messaggio con nome e nominativo inventati. Ordine delle informazioni come nel quiz 1.3.9-19: nominativo, posizione, tipo di pericolo. Quiz 1.3.9-12, -14, -16 (MAYDAY tre volte), -13 (PAN PAN), -15 (SÉCURITÉ), -11 (chi riceve rilancia e se possibile soccorre), -20 (SILENCE MAYDAY, pronunciato «seelonce»), 1.3.5-1 (falla irreparabile: MAYDAY), 1.3.8-7 (DSC: il tasto rosso invia in automatico il soccorso con la posizione), 1.3.9-6, -7, -9 (razzi e fuochi a mano: slide Chiedere soccorso).')

# ============ CHI CI AIUTA ============
def tile(n,t,c,bg,size=72): return f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:28px; border-radius:28px"><p style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,25,INK,600,1.35)}</div>'
tiles=f'<div style="display:flex; gap:22px">{tile("1530","Il numero di emergenza della Guardia Costiera, dal telefono.",CORAL,CORAL_T)}{tile("CIRM","Centro Internazionale Radio Medico: consigli medici a distanza per un infortunio grave a bordo.",SEA,SEA_T)}{tile("SAR","Il soccorso in mare lo coordina il Comando generale delle Capitanerie di porto.",PURPLE,LILAC_T)}</div>'
arms=f'<rect x="0" y="0" width="260" height="200" fill="#F4FAFC"/><circle cx="130" cy="70" r="20" fill="#F2C9A0" stroke="{NAVY}" stroke-width="3"/><path d="M104 96 L156 96 L150 176 L110 176 Z" fill="{CORAL}"/>'+line(104,100,40,60,NAVY,8)+line(156,100,220,60,NAVY,8)+dpath('M40 60 Q30 110 60 150',GREY,3)+dpath('M220 60 Q230 110 200 150',GREY,3)+arrow(40,120,54,150,GREY,3,10)+arrow(220,120,206,150,GREY,3,10)
dtxt=p("Se c'è gente in pericolo di vita devi prestare assistenza, se non metti a rischio la tua barca e chi è a bordo; in porto o vicino l'Autorità marittima può chiederti di partecipare al soccorso. Per farti notare: alza e abbassa lentamente le braccia allargate.",28)
dimg=svgi(260,200,arms,"Persona che alza e abbassa lentamente le braccia allargate",dw=260,dh=200,pan=False)
duty=card(f'<div style="display:flex; gap:28px; align-items:center">{dimg}<div style="display:flex; flex-direction:column; gap:10px">{h3("Aiutare e farsi vedere",34)}{dtxt}</div></div>',None,32,0,'none')
sec('soccorsomare', head('Sicurezza · il soccorso','Chi ci aiuta')+tiles+duty,
 notes='Quiz 1.3.8-25 (1530), 1.3.2.113 (CIRM, unico quiz della voce 3b), 1.3.7-7 (soccorso marittimo: ricerca e salvataggio della vita umana), -8 (coordinamento: Comando generale del Corpo delle Capitanerie di porto), -9 (l\'Autorità marittima può chiedere alle unità in porto o nelle vicinanze di partecipare), -10 (obbligo di assistenza senza rischio per sé), 1.8.1-7…-10 (sanzioni per omesso soccorso, lezione 7), 1.3.8-24 (braccia allargate, segnale di pericolo). Il CIRM risponde 24 ore su 24 via radio, telefono ed e-mail.')

# ============ CATTIVO TEMPO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
for i in range(-4,9):
    x0=-200+i*110
    b+=f'<path d="M{x0} 700 q60 -40 110 -110 t110 -110 t110 -110 t110 -110 t110 -110 t110 -110 t110 -110" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-opacity="0.8"/>'
b+=arrow(60,40,170,150,NAVY,8,26)
b+=topboat(360,330,200,-100,'#FFFFFF',NAVY,5)
b+=topboat(800,330,200,-45,'#FFFFFF',NAVY,5)+line(720,250,880,410,LRED,10)+line(880,250,720,410,LRED,10)
lbl=pill(X+230,Y+460,380,'onde al mascone: alla cappa',GREEN,24)+pill(X+640,Y+460,380,'mai onde al traverso',LRED,24)+lab(X+180,Y+40,300,'onde e vento',NAVY,24,900)
txt=term('Prima che arrivi','Rizza tutto, chiudi oblò, osterigi e prese a mare (non quelle del motore), giubbotti addosso e cinture agganciate.')+term('Da terra o dal mare','Tempesta da terra: vai sottocosta, al ridosso. Dal mare: mettiti alla cappa, onde al mascone e motore quanto basta.')+term('Con le onde','Di prua: trim negativo, prua giù. Di poppa: trim positivo e meno velocità. L\'ancora galleggiante limita l\'intraversamento.')+term('Nebbia','Rallenta, accendi i fanali, fai i segnali; costa vicina: acqua che cambia colore, rumore di frangenti.')
sec('tempocattivo', head('Sicurezza · il mare formato','Il cattivo tempo'), pinned=svgp(X,Y,W,Hh,b,'Onde viste dall\'alto: una barca le prende al mascone, alla cappa, ed è la posizione giusta; un\'altra le prende al traverso ed è barrata in rosso')+lbl+pcol(txt,532,16),
 notes='Quiz 1.3.8-2 e -23 (preparare la barca; chiudere tutto tranne le prese a mare del motore), -3 (tempesta da terra: verso la costa), -4 e -19 (tempesta dal mare: alla cappa, al mascone), -5 (mare in poppa: ridurre), -8 (non al traverso), -9 (puntare leggermente la cresta), -1 e -10 (trim), -11…-14 (flaps; il -15 è oscurato), -16 (stacco di sicurezza), -17 e -6 (nebbia), -20 (risacca), -21 (ancora galleggiante; il -18 è oscurato), -22 (in solitario: cintura e agganciarsi), -24 (braccia per chiamare attenzione).')
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


chapter('capquiz',4,'Raccolta quiz',['Segnali sonori','Nebbia e porti','Entrare in porto','Le dotazioni','Segnali di soccorso','Il fuoco','Gli estintori','Incendio a bordo','Sinistri e abbandono','Radio e soccorso','Cattivo tempo','Alcol e farmaci'],GREEN,
 'Inizio degli ultimi 45 minuti: 12 slide da 3 quiz ufficiali, ognuna seguita dalle risposte.','36 quiz ufficiali',2,'Ultimi 45 minuti','45′',art=(quiz_scene(),'Illustrazione: scheda di quiz con le risposte segnate e un cronometro sui 45 minuti'))
# ============ RACCOLTA QUIZ (45 minuti) ============
steps=[('1','Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.',CORAL,CORAL_T),
 ('2','Conta i suoni','1 breve dritta, 2 brevi sinistra, 3 brevi indietro, 5 brevi dubbio: conta prima di rispondere.',SEA,SEA_T),
 ('3','Cerca lo scambio','Sopravento o sottovento, polvere o CO2, MAYDAY o PAN PAN: il trabocchetto è lì.',PURPLE,LILAC_T),
 ('4','Attento ai numeri','Miglia dalla costa, minuti, metri, canali: controlla il numero e l\'unità.',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,30,INK,800,1.2)}{p(d,24,INK,500,1.35)}</div>' for n,t,d,c,bg in steps)
exam=card(tag("All'esame · la prova a quiz")+f'<div style="display:flex; gap:48px; align-items:end"><div>{p("domande",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{INK}">20</p></div><div>{p("errori ammessi",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{CORAL}">4</p></div><div>{p("tempo",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{INK}">30′</p></div></div>'+p('Il quiz base d\'esame: 20 domande della banca ufficiale, una sola risposta esatta su tre. Vela: altre 5 domande, 1 errore.',24),None,32,16)
plan=card(tag("I 45 minuti",SEA)+'<ol style="font-size:24px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px"><li>Quiz 1-3 · suoni, nebbia, porti (9)</li><li>Quiz 4-5 · dotazioni e soccorso (6)</li><li>Quiz 6-9 · incendio, sinistri, abbandono (12)</li><li>Quiz 10-12 · radio, cattivo tempo, alcol (9)</li></ol>',SEA_T,32,12)
sec('quiz', head('Lezione 06 · ultimi 45 minuti','Raccolta quiz')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div><div style="display:flex; gap:24px">{exam}{plan}</div>',
 notes='Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Se il tempo stringe, lasciare per casa le slide 7 e 11.', gap=28)
E='Raccolta quiz · DD 131/2022'
QZ=[('q01','Quiz 1 · Segnali sonori',['1.5.2-21','1.5.2-23','1.5.2-22']),('q02','Quiz 2 · Nebbia e porti',['1.4.1-15','1.4.1-13','1.5.2-52']),
    ('q03','Quiz 3 · Entrare in porto',['1.4.1-8','1.4.1-10','1.4.1-12']),('q04','Quiz 4 · Le dotazioni',['1.3.3-22','1.3.3-20','1.3.3-24']),
    ('q05','Quiz 5 · Segnali di soccorso',['1.3.3-17','1.3.3-43','1.3.9-6']),('q06','Quiz 6 · Il fuoco',['1.3.1-24','1.3.1-14','1.3.1-18']),
    ('q07','Quiz 7 · Gli estintori',['1.3.1-2','1.3.1-9','1.3.1-13']),('q08','Quiz 8 · Incendio a bordo',['1.3.6-13','1.3.6-14','1.3.6-11']),
    ('q09','Quiz 9 · Sinistri e abbandono',['1.3.6-1','1.3.6-31','1.3.7-2']),('q10','Quiz 10 · Radio e soccorso',['1.3.9-17','1.3.9-8','1.3.9-12']),
    ('q11','Quiz 11 · Cattivo tempo',['1.3.8-3','1.3.8-17','1.3.8-25']),('q12','Quiz 12 · Alcol e farmaci',['1.3.2-9','1.3.2-12','1.3.2-11'])]
for id_,t,ps in QZ:
    quiz_slide(id_,t,ps,False,E)
    quiz_slide(id_+'r',t+' · risposte',ps,True)
closing(['1 breve a dritta, 2 brevi a sinistra, 3 brevi macchine indietro; nella nebbia 1 prolungato ogni 2 minuti','In porto rosso a sinistra e verde a dritta; velocità ridotta già a 500 m dall\'imboccatura','Oltre 12 miglia: zattera, binocolo, GPS, riflettore radar; oltre 50: EPIRB','Incendio: CO2 per l\'elettrico, mai acqua; fiamme sottovento, carburante chiuso','Uomo a mare: accosta dal suo lato; canale 16: MAYDAY, PAN PAN, SÉCURITÉ; 1530 per le emergenze'],
 'Prossima lezione · 07 · Meteorologia e normativa','A casa: i quiz su suoni e porti (1.5.2, 1.4.1), dotazioni e incendio (1.3.1, 1.3.3) e su sinistri, radio e soccorso (1.3.2, 1.3.5-1.3.9).')
exec(open('intermedi.py').read())
intermedi([('porto','v1','Verifica · Suoni, nebbia e porti',['1.5.2-49','1.4.1-14']),
 ('soccorso','v2','Verifica · Dotazioni e soccorso',['1.3.3-34','1.3.3-3']),
 ('incendio','v3','Verifica · Incendio',['1.3.1-1','1.3.6-22']),
 ('abbandono','v4','Verifica · Sinistri e abbandono',['1.3.6-36','1.3.7-6']),
 ('alcol','v5','Verifica · Radio, meteo, alcol',['1.3.9-13','1.3.8-8'])])
write_deck(OUT,'Lezione 06 · Segnali sonori, sicurezza ed emergenze',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Segnali sonori, porti, dotazioni DM 133/2024 e segnali di soccorso","start":"cap1"},
  "s3":{"description":"Incendio, falla, incaglio, collisione, uomo a mare, abbandono","start":"cap2"},
  "s4":{"description":"Radio, soccorso, CIRM, cattivo tempo, alcol","start":"cap3"},
  "s5":{"description":"Raccolta quiz","start":"capquiz"}})
