import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez05/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'; GREY='#97A6B4'; NIGHT='#0F2238'
LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Navigare in vista della costa':'lighthouse','Rilevamento vero e polare':'compass',
 'Dove sono rispetto al faro':'lighthouse','I luoghi di posizione':'map','Il punto nave costiero':'pencil','Il GPS':'map',
 'I fanali di navigazione':'lantern','Cosa vedo di notte':'lantern','Le barche a vela di notte':'sail','Segnali diurni e luci speciali':'flag',
 'Chi lascia la rotta a chi':'helm','C\'è rischio di collisione?':'compass','Due barche a motore':'helm','Due barche a vela':'sail',
 'Rilevamento polare':'compass','Due punti cospicui':'lighthouse','Un punto cospicuo: rilevamento e distanza':'lighthouse','Rilevamenti successivi':'pencil','I rilevamenti':'compass','Il punto nave: tutte le tecniche':'map'})
def chip(t,c,size=34): return f'<p style="font-family:{H}; font-size:{size}px; font-weight:700; color:#FFFFFF; background:{c}; padding:10px 24px; border-radius:40px">{t}</p>'
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
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
def sailtop(cx,cy,L,ang,side,fill='#FFFFFF',op=1):
    s=f'<path d="M{L*0.12:.0f} 0 Q{-L*0.1:.0f} {side*L*0.26:.0f} {-L*0.34:.0f} {side*L*0.2:.0f}" fill="none" stroke="{CORAL}" stroke-width="6" stroke-linecap="round"/>'
    return topboat(cx,cy,L,ang,fill,NAVY,4,op)+f'<g transform="translate({cx} {cy}) rotate({ang})" opacity="{op}">{s}<circle cx="{L*0.12:.0f}" cy="0" r="6" fill="{NAVY}"/></g>'
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(5,'COLREG e prevenzione degli abbordi','Chi è quella luce? Fanali e segnali diurni. Chi passa per primo? Precedenze e rischio di collisione. E poi segnali sonori, nebbia e porti',
 'Lezione 5. Segue la scaletta della scuola «Fanali» (obbligo, testa d\'albero, laterali, coronamento, vela, motore, cuscino d\'aria, draga, rimorchio, pesca, fonda, trucchetti di Ancorotto) e «Precedenze» (gerarchia, motore, vela, rischio di collisione, apparecchi e segnali sonori di manovra, sorpasso, nebbia e fonda, navigazione nei porti). Si apre con la slide sul COLREG e chiude con 24 casi di luci da riconoscere e la raccolta quiz.', title_size=88)
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','3′','Il COLREG',NAVY),('0:03','18′','Cap. 1 · I fanali',PURPLE),('0:21','17′','Cap. 2 · Navi particolari',CORAL),('0:38','13′','Cap. 3 · Precedenze',BLUE),('0:51','14′','Cap. 4 · Suoni e porti',SEA),('1:05','10′','Cap. 5 · Riconoscere le luci',SUN),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{max(int(d[:-1]),14)}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['colreg'],5,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>riconoscere un\'unità di notte dai fanali e di giorno dai segnali</li><li>sapere chi lascia libera la rotta e capire se c\'è rischio di collisione</li><li>usare i segnali sonori di manovra, di sorpasso e di nebbia</li><li>entrare e uscire dal porto</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 05 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='La slide sul COLREG e cinque capitoli di teoria in 75 minuti, i primi quattro chiusi da una verifica da 2 quiz ufficiali (DD 131/2022), il quinto di esercizi sulle luci. Poi 45 minuti di raccolta quiz: 36 quiz ufficiali. Banca: fanali e segnali diurni 67 (1.5.1), prevenire gli abbordi 60 (1.5.2), porti 21 (1.4.1). All. C: 2 quesiti di COLREG e segnalamento nella scheda da 20. Segue la scaletta della scuola «Fanali» e «Precedenze»; segnali sonori e porti erano nella lezione 6.')

# ============ IL COLREG ============
LB.ICON_T['Che cos\'è il COLREG']='helm'
def colreg_art():
    s=f'<rect x="0" y="0" width="520" height="600" rx="40" fill="{NIGHT}"/>'
    s+=''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#FFFFFF" opacity="0.6"/>' for x,y in ((40,40),(120,70),(470,50),(400,110),(70,150),(300,30),(480,170)))
    g=(260,190); R=130
    s+=f'<circle cx="{g[0]}" cy="{g[1]}" r="{R}" fill="#2A6FB0"/>'
    s+=f'<path d="M170 120 Q200 90 240 110 Q250 140 220 160 Q190 170 175 150 Z M280 90 Q330 80 350 120 Q340 160 300 150 Q270 130 280 90 Z M230 220 Q270 200 300 230 Q310 270 270 290 Q240 280 230 220 Z M330 200 Q360 190 370 220 Q350 250 330 230 Z" fill="#3FAE6B"/>'
    s+=f'<ellipse cx="{g[0]}" cy="{g[1]}" rx="{R}" ry="44" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/><ellipse cx="{g[0]}" cy="{g[1]}" rx="52" ry="{R}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/><line x1="{g[0]-R}" y1="{g[1]}" x2="{g[0]+R}" y2="{g[1]}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/>'
    s+=f'<path d="M120 300 Q260 380 400 300" fill="none" stroke="{SUN}" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/>'
    s+=f'<rect x="150" y="268" width="220" height="56" rx="28" fill="{CORAL}"/><text x="260" y="306" text-anchor="middle" font-family="Arial" font-size="30" font-weight="900" fill="#FFFFFF">COLREG 72</text>'
    parts=[('A','Generalità',SEA),('B','Governo e navigazione',BLUE),('C','Fanali e segnali',SUN),('D','Segnali sonori e luminosi',PURPLE),('E','Esenzioni',GREEN),('F','Verifica IMO',CORAL)]
    for i,(k,t,c) in enumerate(parts):
        y=356+i*38
        s+=f'<rect x="60" y="{y}" width="400" height="32" rx="10" fill="#FFFFFF" fill-opacity="0.08"/><rect x="60" y="{y}" width="40" height="32" rx="10" fill="{c}"/>'
        s+=f'<text x="80" y="{y+23}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">{k}</text><text x="116" y="{y+23}" font-family="Arial" font-size="20" font-weight="700" fill="#FFFFFF">{t}</text>'
    s+=f'<text x="260" y="590" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#FFFFFF" opacity="0.75">41 regole in 6 parti + 4 allegati</text>'
    return s
CQ=[('Che cos\'è','COLREG sta per <i>Collision Regulations</i>: la Convenzione di Londra del <b>1972</b> (IMO), in vigore dal <b>1977</b>. In italiano: <b>Regolamento internazionale per prevenire gli abbordi in mare</b>. Abbordo = collisione tra navi.',NAVY,BLUE_T),
    ('Perché è così importante','È la <b>lingua comune del mare</b>: in ogni paese le barche manovrano allo stesso modo e si riconoscono da luci, forme e suoni. Non basta però: vale sempre la buona pratica marinaresca e, per evitare un pericolo immediato, si può derogare.',CORAL,CORAL_T),
    ('Quando e dove si applica','<b>Sempre</b>, di giorno e di notte, in alto mare e in tutte le acque collegate navigabili dalle navi: anche sotto costa. Porti, fiumi e laghi possono avere <b>regole locali</b> (ordinanze), il più possibile conformi.',SEA,SEA_T),
    ('Chi lo deve rispettare','<b>Ogni nave</b>, cioè qualsiasi mezzo che galleggia e trasporta sull\'acqua: dalla petroliera al gommone, a vela, a motore o a remi, anche cuscini d\'aria e idrovolanti. Ne risponde chi ha il comando.',PURPLE,LILAC_T)]
cc=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:24px 26px; border-radius:28px">{tag(t,c)}{p(d,24,INK,500,1.38)}</div>' for t,d,c,bg in CQ)
sec('colreg', head('COLREG · le regole di tutti','Che cos\'è il COLREG')+f'<div style="display:flex; gap:32px; align-items:start">{svgi(520,600,colreg_art(),"Il globo con una rotta tratteggiata e la fascia COLREG 72; sotto le sei parti del regolamento: A generalità, B governo e navigazione, C fanali e segnali, D segnali sonori e luminosi, E esenzioni, F verifica IMO",dw=460,dh=531,pan=False)}<div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:18px">{cc}</div></div>',
 notes='Prima slide della lezione: tutta la lezione applica il COLREG. Convention on the International Regulations for Preventing Collisions at Sea, adottata a Londra il 20 ottobre 1972 dall\'IMO, in vigore dal 15 luglio 1977; in Italia resa esecutiva con la legge 27 dicembre 1977, n. 1085. Regola 1 (applicazione): alto mare e acque collegate navigabili; le regole locali di porti, rade, fiumi e laghi devono essere il più possibile conformi. Regola 2 (responsabilità): il rispetto delle regole non esonera dalla buona pratica marinaresca. Regola 3: «nave» è ogni tipo di galleggiante usato o utilizzabile come mezzo di trasporto sull\'acqua. Parte C: fanali e segnali (oggi capitolo 1); Parte B: precedenze e regole di rotta; Parte D: segnali sonori. Quiz 1.5.2-2 (la norma è il COLREG \'72), 1.5.1-62 (l\'elenco completo dei fanali è nel COLREG), 1.5.1-25 e -26. Trucchetto di Ancorotto: nei quiz sui fanali la risposta che cita il Regolamento per prevenire gli abbordi in mare (COLREG) è sempre quella giusta.')

# ================= DISEGNI COMUNI: LUCI E SEGNALI =================
LC={'W':LWHITE,'m':LWHITE,'R':LRED,'G':LGREEN,'Y':LYEL}
SIL='#2B4A6B'
def ball(x,y,r=16): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>'
def cone(x,y,down=True,h=30):
    return f'<path d="M{x-16} {y-h/2} L{x+16} {y-h/2} L{x} {y+h/2} Z" fill="{INK}"/>' if down else f'<path d="M{x-16} {y+h/2} L{x+16} {y+h/2} L{x} {y-h/2} Z" fill="{INK}"/>'
def diamond(x,y): return f'<path d="M{x} {y-20} L{x+16} {y} L{x} {y+20} L{x-16} {y} Z" fill="{INK}"/>'
def cyl(x,y): return f'<rect x="{x-14}" y="{y-24}" width="28" height="48" rx="4" fill="{INK}"/><ellipse cx="{x}" cy="{y-24}" rx="14" ry="5" fill="#3B4A5E"/>'
def nview(view,cfg,w=260,h=200,sil=True):
    """Unità vista di notte da dritta, sinistra, prora o poppa. cfg: col (luci sull'albero dall'alto: m = testa d'albero,
    W/R/G/Y = visibili tutto intorno), mh2 (secondo testa d'albero più a poppavia e più alto), sd (laterali), st (coronamento),
    tw (giallo di rimorchio), gear (bianco verso le reti), drg ('dritta' o 'sinistra': lato ostruito della draga), kind (sagoma)."""
    s=f'<rect width="{w}" height="{h}" fill="{NIGHT}"/><rect y="{h-26}" width="{w}" height="26" fill="#17304C"/>'
    wl=h-26; cx=w/2; col=cfg.get('col',[]); kind=cfg.get('kind','ship')
    if view=='poppa': col=[c for c in col if c!='m']
    top=36 if len(col)<4 else 26; step=26 if len(col)<4 else 22
    L=[]
    if view in ('dritta','sinistra'):
        k=1 if view=='dritta' else -1
        if sil:
            if kind=='sail':
                s+=f'<path d="M{cx-80} {wl-22} L{cx+90} {wl-22} L{cx+70} {wl} L{cx-66} {wl} Z" fill="{SIL}"/><path d="M{cx} {wl-24} V{top-6}" stroke="{SIL}" stroke-width="5"/><path d="M{cx-6*k} {top+6} L{cx-6*k} {wl-30} L{cx-70*k} {wl-30} Z" fill="{SIL}" opacity="0.8"/>'
            else:
                s+=f'<path d="M{cx-100} {wl-26} L{cx+105} {wl-30} L{cx+85} {wl} L{cx-92} {wl} Z" fill="{SIL}"/><rect x="{cx-40}" y="{wl-58}" width="80" height="32" fill="{SIL}"/><path d="M{cx} {wl-58} V{top-8}" stroke="{SIL}" stroke-width="5"/>'
        for i,c in enumerate(col): L.append((cx,top+i*step,c))
        if cfg.get('mh2'): L.append((cx-60*k,top-8,'m'))
        if cfg.get('sd'): L.append((cx+70*k,wl-18,'G' if k==1 else 'R'))
        if cfg.get('gear'): L.append((cx+40*k,wl-56,'W'))
        if cfg.get('anc2'): L+= [(cx+70*k,top+4,'W'),(cx-80*k,wl-50,'W')]
        if cfg.get('drg'):
            near=('R' if cfg['drg']==view else 'G')
            L+= [(cx-30*k,wl-70,near),(cx-30*k,wl-46,near)]
    elif view=='prora':
        if sil:
            if kind=='sail':
                s+=f'<path d="M{cx-34} {wl-22} L{cx+34} {wl-22} L{cx+14} {wl} L{cx-14} {wl} Z" fill="{SIL}"/><path d="M{cx} {wl-24} V{top-6}" stroke="{SIL}" stroke-width="5"/><path d="M{cx-4} {top+8} L{cx-4} {wl-28} L{cx-30} {wl-28} Z M{cx+4} {top+12} L{cx+4} {wl-28} L{cx+26} {wl-28} Z" fill="{SIL}" opacity="0.8"/>'
            else:
                s+=f'<path d="M{cx-50} {wl-30} L{cx+50} {wl-30} L{cx+20} {wl} L{cx-20} {wl} Z" fill="{SIL}"/><rect x="{cx-34}" y="{wl-60}" width="68" height="30" fill="{SIL}"/><path d="M{cx} {wl-60} V{top-8}" stroke="{SIL}" stroke-width="5"/>'
        off=-26 if cfg.get('mh2') else 0
        if cfg.get('mh2'): L.append((cx,top+off,'m'))
        for i,c in enumerate(col): L.append((cx,top+i*step,c))
        if cfg.get('sd'): L+= [(cx-44,wl-20,'G'),(cx+44,wl-20,'R')]
        if cfg.get('drg'):
            gx=-1 if cfg['drg']=='dritta' else 1   # vista di prora: la dritta della draga è alla mia sinistra
            L+= [(cx+72*gx,wl-74,'R'),(cx+72*gx,wl-50,'R'),(cx-72*gx,wl-74,'G'),(cx-72*gx,wl-50,'G')]
    else:
        if sil:
            if kind=='sail':
                s+=f'<path d="M{cx-34} {wl-22} L{cx+34} {wl-22} L{cx+28} {wl} L{cx-28} {wl} Z" fill="{SIL}"/><path d="M{cx} {wl-24} V{top-6}" stroke="{SIL}" stroke-width="5"/>'
            else:
                s+=f'<path d="M{cx-52} {wl-30} L{cx+52} {wl-30} L{cx+44} {wl} L{cx-44} {wl} Z" fill="{SIL}"/><rect x="{cx-34}" y="{wl-60}" width="68" height="30" fill="{SIL}"/><path d="M{cx} {wl-60} V{top-8}" stroke="{SIL}" stroke-width="5"/>'
        for i,c in enumerate(col): L.append((cx,top+i*step,c))
        if cfg.get('st'): L.append((cx,wl-16,'W'))
        if cfg.get('tw'): L.append((cx,wl-40,'Y'))
        if cfg.get('drg'):
            gx=1 if cfg['drg']=='dritta' else -1   # vista di poppa: la dritta è alla mia destra
            L+= [(cx+72*gx,wl-74,'R'),(cx+72*gx,wl-50,'R'),(cx-72*gx,wl-74,'G'),(cx-72*gx,wl-50,'G')]
    s+=''.join(glow(x,y,LC[c],8) for x,y,c in L)
    return s
def dayview(shapes,w=260,h=260,kind='ship'):
    """Unità di giorno con i segnali sull'albero: lista di 'ball', 'cone_d', 'cone_u', 'dia', 'cyl' dall'alto."""
    s=f'<rect width="{w}" height="{h}" fill="#DDEFF7"/><rect y="{h-40}" width="{w}" height="40" fill="{WATER}" fill-opacity="0.5"/>'
    cx=w/2; wl=h-40
    if kind=='sail': s+=f'<path d="M{cx-70} {wl-18} L{cx+80} {wl-18} L{cx+62} {wl} L{cx-58} {wl} Z" fill="{NAVY}"/><path d="M{cx} {wl-20} V30" stroke="{NAVY}" stroke-width="5"/><path d="M{cx+6} 40 L{cx+6} {wl-26} L{cx+70} {wl-26} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'
    else: s+=f'<path d="M{cx-100} {wl-24} L{cx+105} {wl-28} L{cx+85} {wl} L{cx-92} {wl} Z" fill="{NAVY}"/><rect x="{cx-50}" y="{wl-54}" width="70" height="30" fill="{NAVY}"/><path d="M{cx-14} {wl-54} V24" stroke="{NAVY}" stroke-width="5"/>'
    x=cx-14 if kind!='sail' else cx-24; y=40
    for sh in shapes:
        if sh=='ball': s+=ball(x,y+4,15); y+=40
        elif sh=='cone_d': s+=cone(x,y+6,True); y+=38
        elif sh=='cone_u': s+=cone(x,y+6,False); y+=38
        elif sh=='dia': s+=diamond(x,y+8); y+=44
        elif sh=='cyl': s+=cyl(x,y+20); y+=56
        elif sh=='bicone': s+=cone(x,y+2,True,28)+cone(x,y+30,False,28); y+=60
    return s
def tile(svg,alt,cap,w=260,h=200,dw=None,dh=None,capc=INK):
    return f'<div style="display:flex; flex-direction:column; gap:6px; align-items:center">{svgi(w,h,svg,alt,dw=dw or w,dh=dh or h,pan=False)}<p style="font-size:22px; font-weight:800; color:{capc}; text-align:center; line-height:1.2">{cap}</p></div>'
def bigcol(cols,cap,w=220,h=260):
    s=f'<rect width="{w}" height="{h}" fill="{NIGHT}"/>'+''.join(glow(w/2,60+i*52,LC[c],16) for i,c in enumerate(cols))
    return s
def ship_slide(id_,eyebrow,title,big,day,views,txt,notes,trick=None,tc=CORAL):
    """big: (luci, didascalia); day: (forme, didascalia, kind) o None; views: lista di (vista, cfg, didascalia)."""
    r1=f'<div style="display:flex; flex-direction:column; gap:6px; align-items:center">{svgi(220,260,bigcol(big[0],big[1]),"Luci viste da lontano: "+big[1],dw=230,dh=272,pan=False)}<p style="font-size:22px; font-weight:800; color:{INK}; text-align:center; width:240px">{big[1]}</p></div>'
    if day: r1+=f'<div style="display:flex; flex-direction:column; gap:6px; align-items:center">{svgi(260,260,dayview(day[0],kind=day[2] if len(day)>2 else "ship"),"Di giorno: "+day[1],dw=272,dh=272,pan=False)}<p style="font-size:22px; font-weight:800; color:{INK}; text-align:center; width:272px">{day[1]}</p></div>'
    if trick: r1+=f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{SUN_T}; padding:22px; border-radius:26px; align-self:start">{tag("Il trucchetto",tc)}{note(trick,tc,32)}</div>'
    r2=''.join(tile(nview(v,c,h=270),f'Di notte, {cap}',cap,h=270,dw=266,dh=276) for v,c,cap in views)
    left=f'<div style="flex:1; display:flex; flex-direction:column; gap:16px"><div style="display:flex; gap:18px; align-items:start">{r1}</div><div style="display:flex; gap:12px; justify-content:space-between">{r2}</div></div>'
    sec(id_, head(eyebrow,title)+f'<div style="display:flex; gap:32px; align-items:start">{left}{col(txt,480,14)}</div>', notes=notes, gap=24)
def tterm(t,d): return f'<div style="display:flex; flex-direction:column; gap:2px">{p(t,26,INK,800,1.25)}{p(d,24,BODY,400,1.38)}</div>'

# ================= CAPITOLO 1 · I FANALI =================
LB.ICON_T.update({'Quando si accendono i fanali':'lantern','Il fanale di testa d\'albero':'lantern','I fanali laterali':'lantern','Il fanale di coronamento':'lantern',
 'Le unità a motore di notte':'lantern','Le unità a vela di notte':'sail','Le navi a cuscino d\'aria':'lantern','Rimorchiatore e rimorchiata':'anchor',
 'La pesca non a strascico':'flag','La pesca a strascico':'flag','Draga e manovrabilità limitata':'flag','Tre navi da riconoscere':'flag','La nave alla fonda':'anchor',
 'I trucchetti per ricordare':'star','La scala delle precedenze':'helm','Le precedenze tra unità a motore':'helm','Le precedenze tra unità a vela':'sail',
 'Il rischio di collisione':'compass','Gli apparecchi per i segnali sonori':'flag','I segnali sonori di manovra':'flag','I segnali sonori di sorpasso':'flag',
 'In navigazione con la nebbia':'cloud','Alla fonda con la nebbia':'cloud','Precedenze e navigazione nei porti':'lighthouse',
 'Riconosci le luci · 1':'quiz','Riconosci le luci · 2':'quiz','Riconosci le luci · 3':'quiz','Riconosci le luci · 4':'quiz'})

# ============ OBBLIGO DEI FANALI ============
X=700
b=f'<defs><linearGradient id="tram" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2E4F"/><stop offset="0.75" stop-color="#F28C28"/></linearGradient></defs>'
b+=f'<rect x="0" y="0" width="1092" height="300" rx="24" fill="url(#tram)"/><circle cx="880" cy="232" r="46" fill="{SUN}"/><rect x="0" y="230" width="1092" height="70" fill="#0F2238"/>'
b+=f'<path d="M0 150 Q80 170 140 220 L180 240 L0 240 Z" fill="#2F5D3A"/>'+arrow(200,200,560,200,'#FFFFFF',4,16)
b+=profile(560,246,260,sup=True)+glow(706,190,LWHITE,8)+glow(752,224,LGREEN,7)
b+=f'<rect x="0" y="320" width="1092" height="300" rx="24" fill="#BFE6F2"/><circle cx="120" cy="400" r="40" fill="{SUN}"/><rect x="0" y="540" width="1092" height="80" fill="{WATER}" fill-opacity="0.6"/>'
b+=f'<path d="M0 470 Q80 490 140 540 L0 540 Z" fill="#3FAE6B"/>'+arrow(200,510,620,510,NAVY,4,16)
b+=profile(620,556,260,sup=True)
b+=f'<g transform="translate(930 420) rotate(-20)"><rect x="-60" y="-16" width="100" height="32" rx="10" fill="{NAVY}"/><path d="M40 -22 L70 -30 L70 30 L40 22 Z" fill="#3B4A5E"/><path d="M70 -26 L150 -60 L150 60 L70 26 Z" fill="{SUN}" fill-opacity="0.45"/></g>'
lbl=(lab(X+200,Y+150,360,'oltre 1 miglio dalla costa',LWHITE,26,900)+lab(X+30,Y+20,700,'dal tramonto al sorgere del sole',LWHITE,28,900)
     +lab(X+200,Y+460,420,'di giorno, fino a 12 miglia',NAVY,26,900)+lab(X+860,Y+490,230,'torcia a luce bianca',NAVY,24,900,'center'))
txt=(term('Di notte','Dal tramonto al sorgere del sole. Per le unità da diporto l\'obbligo vale in navigazione oltre 1 miglio dalla costa.')
     +term('Con visibilità ridotta','Nebbia, bruma, neve, acquazzoni, tempeste di sabbia: i fanali si accendono anche di giorno.')
     +term('Niente altre luci','Di notte non si mostrano luci che si possano scambiare per i fanali. L\'elenco completo è nel COLREG.')
     +term('La torcia','Di giorno, fino a 12 miglia, basta una torcia a luce bianca a bordo. Per il quiz 1.5.1-6 la usa anche chi naviga di notte entro 3 miglia.'))
sec('obbligo', head('COLREG · i fanali','Quando si accendono i fanali')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'In alto, al tramonto, una barca oltre 1 miglio dalla costa con i fanali accesi; in basso, di giorno, una barca entro 12 miglia con a bordo una torcia a luce bianca')+lbl,
 notes='Quiz 1.5.1-23 e -56 (dal tramonto al sorgere del sole e con visibilità ridotta), -27 e 1.5.2-33 (diporto: oltre 1 miglio dalla costa), -26 e -35 (di notte si accendono i fanali regolamentari), 1.5.2-11 (nessun\'altra luce che si possa confondere), 1.5.2-12 (con visibilità ridotta anche di giorno), 1.5.2-3 (cos\'è la visibilità ridotta: nebbia, bruma, neve, piovaschi, tempeste di sabbia), 1.5.1-6 (entro 3 miglia, di notte: torcia di sicurezza a luce bianca), 1.5.1-62 (l\'elenco completo dei fanali è nel COLREG). La torcia di giorno entro 12 miglia segue il materiale della scuola.')

# ============ I FANALI DI NAVIGAZIONE (quadro) ============
X=128
cx,cy=546,320
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/>'
b+=sector(cx,cy,280,247.5,472.5,LWHITE,0.16)
b+=sector(cx,cy,210,0,112.5,LGREEN,0.4)+sector(cx,cy,210,247.5,360,LRED,0.4)+sector(cx,cy,210,112.5,247.5,LWHITE,0.3)
b+=topboat(cx,cy,190,-90,'#DCE6F0',NAVY,4)
b+=glow(cx,cy-40,LWHITE,7)+glow(cx+18,cy-10,LGREEN,6)+glow(cx-18,cy-10,LRED,6)+glow(cx,cy+92,LWHITE,6)
s_=pol(cx,cy,180,245); m=pol(cx,cy,0,300)
lbl=lab(X+m[0]-210,Y+14,420,'testa d\'albero · bianco · 225°',LWHITE,26,900,'center')+lab(X+836,Y+130,250,'verde · dritta · 112,5°',LGREEN,26,900)+lab(X+6,Y+130,254,'rosso · sinistra · 112,5°',LRED,26,900,'right')+lab(X+s_[0]-200,Y+s_[1]+14,400,'coronamento · bianco · 135°',LWHITE,26,900,'center')
txt=(term('Quattro fanali','Testa d\'albero e coronamento bianchi, laterali verde e rosso. Tutti hanno un settore fisso, misurato dalla prora.')
     +term('Tutto l\'orizzonte','225° + 135° = 360°: da qualsiasi direzione vedo almeno un bianco. I due laterali insieme fanno 225°, come la testa d\'albero.')
     +term('In abbrivio','Laterali e coronamento si accendono quando l\'unità si muove sull\'acqua, anche con l\'invertitore in folle o le vele sventate.'))
sec('fanali', head('COLREG · le luci','I fanali di navigazione'), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto di notte: settori di visibilità dei fanali, bianco di testa d\'albero verso prora, verde a dritta, rosso a sinistra, bianco di coronamento verso poppa',pan=False)+lbl+pcol(txt,532,22),
 notes='Quadro d\'insieme prima dei tre fanali uno per uno. Quiz 1.5.1-1 (motore < 50 m: testa d\'albero, laterali, coronamento), 1.5.2-38 (l\'abbrivio è il moto che resta quando si disinnesta l\'invertitore o si sventano le vele). Far disegnare alla lavagna la barca vista dall\'alto con i tre settori.')
X=700

# ============ TESTA D'ALBERO ============
cx,cy=290,330
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/>'+sector(cx,cy,250,247.5,472.5,LWHITE,0.3)
b+=dash(cx-260,cy,cx+260,cy,'#5B7896',2)+topboat(cx,cy,170,-90,'#DCE6F0',NAVY,4)+glow(cx,cy-40,LWHITE,8)
for a in (112.5,247.5): e=pol(cx,cy,a,250); b+=line(cx,cy,e[0],e[1],LWHITE,2)
b+=f'<rect x="600" y="0" width="492" height="620" fill="#15294A"/>'+f'<path d="M640 470 L1040 460 L1010 510 L660 510 Z" fill="{SIL}"/><rect x="760" y="420" width="140" height="40" fill="{SIL}"/><path d="M880 420 V260 M720 420 V180" stroke="{SIL}" stroke-width="6"/>'
b+=glow(880,256,LWHITE,10)+glow(720,176,LWHITE,10)+arrow(1000,560,1060,560,LWHITE,3,12)
lbl=(lab(X+cx-150,Y+40,300,'225° verso prora',LWHITE,28,900,'center')+lab(X+cx+90,Y+cy-50,200,'112,5° a dritta',LWHITE,22,800)+lab(X+cx-290,Y+cy-50,200,'112,5° a sinistra',LWHITE,22,800,'right')
     +lab(X+cx-270,Y+cy+110,540,'fino a 22,5° a poppavia del traverso',LWHITE,22,800,'center')
     +lab(X+620,Y+30,450,'oltre 50 m: due fanali',LWHITE,26,900,'center')+lab(X+620,Y+70,450,'il secondo più a poppavia e più alto',LWHITE,22,800,'center')+lab(X+930,Y+575,120,'prora',LWHITE,20,800))
txt=(term('Colore e settore','Bianco, 225° verso prora, centrato sull\'asse longitudinale.')
     +term('Chi lo mostra','Le unità a motore in navigazione, e la vela quando va anche a motore. La vela da sola non lo accende.')
     +term('Oltre i 50 m','Due fanali di testa d\'albero: il secondo più a poppavia e più in alto. Una nave di 280 m ne mostra 2.')
     +term('Portata','2 miglia sotto i 12 m, 3 miglia da 12 a 20 m, 5 miglia da 20 a 50 m, 6 miglia oltre.'))
sec('testa', head('COLREG · il fanale bianco a prora','Il fanale di testa d\'albero')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'A sinistra la barca vista dall\'alto con il settore bianco di 225 gradi verso prora; a destra una nave di oltre 50 metri vista di fianco con due fanali di testa d\'albero, quello a poppavia più alto',pan=False)+lbl,
 notes='Quiz 1.5.1-11 (bianco), -12 (il secondo fanale ha lo stesso settore di 225° verso prora), -38 e -66 (oltre 50 m: un bianco più alto e a poppavia), -29 (nave di 280 m: 2 fanali), -1, -37 e -65 (motore: testa d\'albero, laterali, coronamento). Portate dalla regola 22 del COLREG.')

# ============ LATERALI ============
X=128
cx,cy=300,330
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/>'
b+=sector(cx,cy,250,0,112.5,LGREEN,0.45)+sector(cx,cy,250,247.5,360,LRED,0.45)
b+=f'<path d="M{cx} {cy} m0 -1" />'+sector(cx,cy,120,112.5,360,'#5B7896',0.18)
b+=topboat(cx,cy,170,-90,'#DCE6F0',NAVY,4)+glow(cx+16,cy-10,LGREEN,7)+glow(cx-16,cy-10,LRED,7)
b+=f'<rect x="620" y="0" width="472" height="620" fill="#15294A"/>'+f'<path d="M770 470 L930 470 L890 530 L810 530 Z" fill="{SIL}"/><rect x="800" y="420" width="100" height="50" fill="{SIL}"/><path d="M850 420 V250" stroke="{SIL}" stroke-width="6"/>'
b+=glow(850,246,LWHITE,10)+glow(784,456,LGREEN,11)+glow(916,456,LRED,11)
lbl=(lab(X+cx+60,Y+60,240,'verde · dritta',LGREEN,26,900)+lab(X+cx-300,Y+60,240,'rosso · sinistra',LRED,26,900,'right')+lab(X+cx+40,Y+cy+40,240,'112,5° ciascuno',LWHITE,22,800)
     +lab(X+cx-130,Y+cy+130,260,'oscurato 247,5°',LWHITE,22,800,'center')
     +lab(X+640,Y+30,430,'la vedo di prora',LWHITE,26,900,'center')+lab(X+640,Y+70,430,'il suo verde è alla mia sinistra',LWHITE,22,800,'center'))
txt=(term('Colori e lati','Verde a dritta, rosso a sinistra: 112,5° ciascuno, dalla prora a 22,5° a poppavia del traverso.')
     +term('Insieme e al buio','Insieme fanno 225° verso prora. Ognuno resta oscurato per gli altri 247,5°.')
     +term('In abbrivio','Li mostra chi si muove sull\'acqua, anche col moto residuo. Alla fonda si spengono.')
     +term('Portata e combinati','1 miglio sotto i 12 m, 2 miglia da 12 a 50 m, 3 oltre. Sotto i 20 m possono stare in un unico fanale.'))
sec('laterali', head('COLREG · verde e rosso','I fanali laterali'), pinned=svgp(X,Y,W,Hh,b,'A sinistra la barca vista dall\'alto con il settore verde a dritta e quello rosso a sinistra, 112,5 gradi ciascuno; a destra la stessa barca vista di prora con il verde alla sinistra di chi guarda',pan=False)+lbl+pcol(txt,532,18),
 notes='Quiz 1.5.1-36 e -64 (verde a dritta, rosso a sinistra), -5 (112,5°), -30 (insieme 225° verso prora), -28 e 1.5.2-34 (portata 2 miglia per le unità da 12 a 50 m), 1.5.2-38 (abbrivio). Il disegno di prora anticipa la regola «vedo il rosso: cedo io».')
X=700

# ============ CORONAMENTO ============
cx,cy=300,250
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/>'+sector(cx,cy,300,112.5,247.5,LWHITE,0.3)
for a in (112.5,247.5): e=pol(cx,cy,a,300); b+=line(cx,cy,e[0],e[1],LWHITE,2)
b+=topboat(cx,cy,170,-90,'#DCE6F0',NAVY,4)+glow(cx,cy+84,LWHITE,8)+topboat(cx+20,cy+300,110,-90,'#DCE6F0',NAVY,3,0.8,False)
b+=f'<rect x="640" y="0" width="452" height="620" fill="#15294A"/>'+f'<path d="M780 470 L940 470 L930 520 L790 520 Z" fill="{SIL}"/><rect x="810" y="420" width="100" height="50" fill="{SIL}"/><path d="M860 420 V280" stroke="{SIL}" stroke-width="6"/>'+glow(860,496,LWHITE,11)
lbl=(lab(X+cx-150,Y+cy+150,300,'135° verso poppa',LWHITE,28,900,'center')+lab(X+cx+90,Y+cy+260,260,'chi raggiunge',LWHITE,22,800)
     +lab(X+660,Y+30,410,'la vedo di poppa',LWHITE,26,900,'center')+lab(X+660,Y+70,410,'solo il bianco basso',LWHITE,22,800,'center'))
txt=(term('Colore e settore','Bianco, 135° verso poppa, centrato sull\'asse: 67,5° per lato.')
     +term('Chi lo mostra','Tutte le unità in abbrivio, a motore e a vela, e anche chi è a rimorchio.')
     +term('Chi lo vede','Chi sta dietro, oltre 22,5° a poppavia del traverso: è la nave raggiungente e deve cedere.')
     +term('Portata','2 miglia sotto i 50 m, 3 miglia oltre.'))
sec('coronamento', head('COLREG · il bianco a poppa','Il fanale di coronamento')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'A sinistra la barca vista dall\'alto con il settore bianco di 135 gradi verso poppa e una seconda barca che la raggiunge da dietro; a destra la barca vista di poppa con il solo bianco basso',pan=False)+lbl,
 notes='Quiz 1.5.1-4 e -7 (135° verso poppa, centrato sull\'asse), -17 (bianco anche per l\'unità a rimorchio), 1.5.2-17, -45, -58 (la raggiungente sta nel settore del coronamento), 1.5.2-54 (vedo un bianco a prora: sto raggiungendo e cedo).')

# ============ UNITÀ A MOTORE ============
def mtop(two=False,comb=False,allround=False):
    s=f'<rect width="260" height="230" fill="{NIGHT}"/>'; cx,cy=130,130
    if allround: s+=f'<circle cx="{cx}" cy="{cy}" r="100" fill="{LWHITE}" fill-opacity="0.18" stroke="{LWHITE}" stroke-width="2"/>'
    else: s+=sector(cx,cy,100,247.5,472.5,LWHITE,0.25)+sector(cx,cy,80,112.5,247.5,LWHITE,0.18)
    s+=sector(cx,cy,64,0,112.5,LGREEN,0.5)+sector(cx,cy,64,247.5,360,LRED,0.5)+topboat(cx,cy,90,-90,'#DCE6F0',NAVY,3)
    if comb: s+=glow(cx-6,cy-30,LRED,5)+glow(cx+6,cy-30,LGREEN,5)
    else: s+=glow(cx-10,cy-6,LRED,5)+glow(cx+10,cy-6,LGREEN,5)
    s+=glow(cx,cy-18,LWHITE,6)+(glow(cx,cy+14,LWHITE,6) if two else '')
    return s
MT=[(mtop(allround=True,comb=True),'Sotto i 12 m','Al posto di testa d\'albero e coronamento può mostrare un solo bianco visibile tutto intorno, più i laterali. Sotto i 7 m e fino a 7 nodi basta il bianco.'),
    (mtop(comb=True),'Sotto i 20 m','Testa d\'albero, coronamento e laterali, che possono stare uniti in un unico fanale combinato.'),
    (mtop(),'Sotto i 50 m','Un testa d\'albero bianco di 225°, i due laterali, il coronamento.'),
    (mtop(two=True),'Da 50 m in su','Due testa d\'albero: il secondo più a poppavia e più alto del primo.')]
cc=''.join(card(svgi(260,230,s,f'Vista dall\'alto di notte: unità a motore {t.lower()}',dw=300,dh=265,pan=False)+h3(t,30)+p(d,22),None,20,8) for s,t,d in MT)
sec('motorenotte', head('COLREG · a motore','Le unità a motore di notte')+f'<div style="display:flex; gap:18px">{cc}</div>'+note('Di prora: il bianco e tutti e due i colori. Di fianco: il bianco e un colore. Di poppa: un bianco basso.',CORAL,32),
 notes='Quiz 1.5.1-1 (sotto i 50 m: testa d\'albero, laterali, coronamento), -37 e -65 (diporto di 45 m: tutti e tre i fanali), -38 e -66 (oltre 50 m: il secondo bianco più alto e a poppavia), -29 (280 m: 2 fanali di testa d\'albero), -3 (cuscino d\'aria in assetto dislocante: fanali del motore). Sotto i 12 m e sotto i 7 m: regola 23(d) del COLREG.')

# ============ UNITÀ A VELA ============
def vtop(kind):
    s=f'<rect width="260" height="230" fill="{NIGHT}"/>'; cx,cy=130,130
    if kind=='torcia':
        s+=topboat(cx,cy+10,80,-90,'#DCE6F0',NAVY,3)+f'<g transform="translate(150 80) rotate(-30)"><rect x="-40" y="-10" width="64" height="20" rx="6" fill="#DCE6F0"/><path d="M24 -14 L44 -18 L44 18 L24 14 Z" fill="#9AA5B1"/><path d="M44 -16 L110 -46 L110 46 L44 16 Z" fill="{LWHITE}" fill-opacity="0.35"/></g>'
        return s
    s+=sector(cx,cy,100,112.5,247.5,LWHITE,0.25)+sector(cx,cy,90,0,112.5,LGREEN,0.45)+sector(cx,cy,90,247.5,360,LRED,0.45)+topboat(cx,cy,90,-90,'#DCE6F0',NAVY,3)
    if kind=='tri': s+=f'<circle cx="{cx}" cy="{cy-8}" r="12" fill="none" stroke="{SUN}" stroke-width="3"/>'+glow(cx,cy-8,LWHITE,5)
    else: s+=glow(cx-10,cy-14,LRED,5)+glow(cx+10,cy-14,LGREEN,5)+glow(cx,cy+40,LWHITE,5)
    return s
def vfac():
    s=f'<rect width="260" height="230" fill="{NIGHT}"/><path d="M60 196 L210 196 L190 214 L76 214 Z" fill="{SIL}"/><path d="M130 196 V40" stroke="{SIL}" stroke-width="5"/><path d="M136 60 L136 190 L200 190 Z" fill="{SIL}" opacity="0.8"/>'
    return s+glow(130,38,LRED,9)+glow(130,64,LGREEN,9)+glow(200,190,LGREEN,7)
VT=[(vtop('torcia'),'Sotto i 7 m','Se può, laterali e coronamento; se no, una torcia a luce bianca pronta da mostrare.'),
    (vtop('tri'),'Da 7 a 20 m','Laterali e coronamento, anche riuniti in un unico fanale tricolore in testa d\'albero.'),
    (vtop('sep'),'Da 20 m in su','Laterali e coronamento separati: il tricolore non è ammesso.'),
    (vfac(),'Facoltativi','In testa d\'albero rosso sopra verde, visibili tutto intorno. Mai insieme al tricolore.')]
cc=''.join(card(svgi(260,230,s,f'Di notte: unità a vela, {t.lower()}',dw=300,dh=265,pan=False)+h3(t,30)+p(d,22),None,20,8) for s,t,d in VT)
_t='<b>A vela e a motore insieme</b>: di notte accende anche il testa d\'albero, di giorno mostra un cono con il vertice in basso. È una barca a motore e <b>perde il diritto di precedenza</b>.'
side=f'<div style="display:flex; gap:20px; align-items:center; background:{SUN_T}; padding:16px 24px; border-radius:26px">{svgi(60,60,cone(30,30,True,40),"Cono nero con il vertice in basso",dw=56,dh=56,pan=False)}{p(_t,24,INK,500,1.35)}</div>'
sec('velanotte', head('COLREG · a vela: niente testa d\'albero','Le unità a vela di notte')+f'<div style="display:flex; gap:18px">{cc}</div>'+side,
 notes='Quiz 1.5.1-39 e -67 (vela: laterali e coronamento), -61 (oltre 20 m: laterali e fanale di poppa), -15 (natanti a vela sotto i 7 m: torcia bianca), -40 (facoltativi rosso sopra verde, 360°), 1.5.1-9 e -55 (cono con il vertice in basso: vela e motore). Il tricolore è ammesso sotto i 20 m (regola 25(b)); i facoltativi non si accendono insieme al tricolore (regola 25(c)).')

# ============ COSA VEDO DI NOTTE ============
NV=[('prora',{'col':['m'],'sd':True},'Motore, di prora','Bianco in alto, verde e rosso: viene verso di me.'),('dritta',{'col':['m'],'sd':True},'Motore, dal lato dritto','Bianco e verde: la vedo di fianco, sulla sua dritta.'),
    ('poppa',{'col':['m'],'st':True},'Di poppa','Solo il bianco basso: la sto raggiungendo.'),('prora',{'sd':True,'kind':'sail'},'Vela, di prora','Verde e rosso senza bianco: è una barca a vela.')]
cc=''.join(card(svgi(260,240,nview(v,c,h=240),f'Di notte: {t}',dw=340,dh=314,pan=False)+h3(t,30)+p(d,24),None,22,10) for v,c,t,d in NV)
sec('cosavedo', head('COLREG · leggere le luci','Cosa vedo di notte')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Il verde di un\'altra barca è alla mia sinistra quando mi viene incontro!',CORAL,36),
 notes='Quiz 1.5.2-54 (un bianco a prora: sto raggiungendo un\'altra unità), 1.5.2-17 e -45 (raggiungente nel settore del coronamento), 1.5.2-46 (entrambe vedono testa d\'albero e laterali: rotte opposte, entrambe accostano a dritta), 1.5.2-41 (fiancate opposte). Nella prima figura il verde appare a sinistra di chi guarda perché la barca viene verso di noi.')
quiz_slide('v1','Verifica · I fanali',['1.5.1-5','1.5.1-39'],False,'Verifica del paragrafo · quiz ufficiali')
quiz_slide('v1r','Verifica · I fanali · risposte',['1.5.1-5','1.5.1-39'],True)

# ================= CAPITOLO 2 · NAVI PARTICOLARI =================
X=700
ship_slide('cuscino','COLREG · fanali speciali','Le navi a cuscino d\'aria',(['Y','m'],'giallo lampeggiante sopra il testa d\'albero'),None,
 [('dritta',{'col':['Y','m'],'sd':True},'lato dritto'),('prora',{'col':['Y','m'],'sd':True},'prora'),('sinistra',{'col':['Y','m'],'sd':True},'lato sinistro'),('poppa',{'col':['Y','m'],'st':True},'poppa')],
 tterm('Assetto non dislocante','Quando corre sollevata sul cuscino d\'aria: ai fanali della nave a motore aggiunge un giallo lampeggiante visibile tutto intorno.')
 +tterm('Assetto dislocante','Quando galleggia come una nave normale: solo i fanali della nave a motore.')
 +tterm('Di poppa','Il testa d\'albero non si vede: restano il giallo lampeggiante e il coronamento.'),
 'Quiz 1.5.1-34 (in assetto non dislocante: un giallo lampeggiante visibile tutto intorno in più), -3 (in assetto dislocante: i fanali della nave a propulsione meccanica). Regola 23(b) del COLREG.',
 trick='Il giallo lampeggia: va veloce, sollevata sull\'acqua.',tc=SUN)
X=128
ship_slide('rimorchio','COLREG · fanali speciali','Rimorchiatore e rimorchiata',(['m','m'],'rimorchiatore: due testa d\'albero in verticale'),(['dia'],'oltre 200 m: un rombo su tutte e due'),
 [('prora',{'col':['m','m'],'sd':True},'rimorchiatore, prora'),('poppa',{'col':['m','m'],'st':True,'tw':True},'rimorchiatore, poppa'),('dritta',{'sd':True},'rimorchiata, dritta'),('prora',{'col':['m','m','m'],'sd':True},'rimorchio oltre 200 m')],
 tterm('La rimorchiata','Solo laterali e coronamento: niente testa d\'albero.')
 +tterm('Il rimorchiatore','Due testa d\'albero in verticale, tre se il rimorchio supera 200 m. Sopra il coronamento un fanale giallo di rimorchio.')
 +tterm('La lunghezza del rimorchio','Si misura dalla poppa del rimorchiatore alla poppa della rimorchiata.')
 +tterm('Di giorno','Oltre 200 m un rombo nero su tutte e due le unità.'),
 'Quiz 1.5.1-24 (la rimorchiata mostra laterali e coronamento), -17 (il coronamento della rimorchiata è bianco), -18 e -20 (i fanali del rimorchiatore oltre 50 m: «sono riportati nel COLREG»). Regola 24 del COLREG: testa d\'albero doppio (triplo oltre 200 m), giallo di rimorchio sopra il coronamento, rombo oltre 200 m. Un rimorchio che non può deviare dalla rotta è una nave con manovrabilità limitata.',
 trick='Più fanali in verticale, più è lungo il rimorchio: due fino a 200 m, tre oltre.',tc=PURPLE)
X=700
ship_slide('pescanon','COLREG · la pesca','La pesca non a strascico',(['R','W'],'rosso sopra bianco, 360°'),(['bicone','cone_u'],'due coni uniti; reti oltre 150 m: un cono in su'),
 [('dritta',{'col':['R','W'],'sd':True,'gear':True},'lato dritto'),('prora',{'col':['R','W'],'sd':True},'prora'),('sinistra',{'col':['R','W'],'sd':True},'lato sinistro'),('poppa',{'col':['R','W'],'st':True},'poppa')],
 tterm('Di notte','Rosso sopra bianco, visibili tutto intorno. In abbrivio anche laterali e coronamento, mai il testa d\'albero.')
 +tterm('Reti oltre 150 m','Un bianco in più, tutto intorno, dalla parte delle reti; di giorno un cono con il vertice in alto.')
 +tterm('Di giorno','Due coni uniti per il vertice.')
 +tterm('Precedenza','Cede solo a chi non governa e alla manovrabilità limitata.'),
 'Quiz 1.5.1-32 (cono con il vertice in alto verso l\'attrezzo oltre 150 m), 1.5.1-13 e 1.5.2-24 (chi pesca cede a chi non governa e alla manovrabilità limitata). Le figure dei quiz 1.5.1-41, -48, -49, -50, -53 mostrano la pesca non a strascico. Regola 26(c).',
 trick='Reti in superficie: il pescatore ha il cappello ROSSO. Pericolo!',tc=CORAL)
X=128
ship_slide('strascico','COLREG · la pesca','La pesca a strascico',(['G','W'],'verde sopra bianco, 360°'),(['bicone'],'due coni uniti per il vertice'),
 [('dritta',{'col':['G','W'],'sd':True},'lato dritto'),('prora',{'col':['G','W'],'sd':True},'prora'),('sinistra',{'col':['G','W'],'sd':True,'mh2':True},'sinistro, oltre 50 m'),('poppa',{'col':['G','W'],'st':True},'poppa')],
 tterm('Di notte','Verde sopra bianco, visibili tutto intorno. In abbrivio anche laterali e coronamento.')
 +tterm('Oltre i 50 m','Anche un testa d\'albero, più a poppavia e più in alto del verde.')
 +tterm('Senza abbrivio','Solo verde sopra bianco.')
 +tterm('Di giorno','Due coni uniti per il vertice, come per l\'altra pesca.'),
 'Quiz 1.5.1-2 e -60 (di giorno: due coni uniti per il vertice), figure 1.5.1-33, -42, -52 (verde sopra bianco). Regola 26(b): sotto i 50 m il testa d\'albero a poppavia è facoltativo.',
 trick='Reti sul fondale: il pescatore ha il cappello VERDE, come le alghe sul fondo.',tc=GREEN)
X=700
ship_slide('draga','COLREG · fanali speciali','Draga e manovrabilità limitata',(['R','W','R'],'rosso, bianco, rosso: manovrabilità limitata'),(['ball','dia','ball'],'pallone, rombo, pallone'),
 [('prora',{'col':['m','R','W','R'],'sd':True},'manovrabilità limitata, prora'),('dritta',{'col':['m','R','W','R'],'sd':True},'manovrabilità limitata, dritta'),('prora',{'col':['R','W','R'],'drg':'sinistra'},'draga, prora'),('poppa',{'col':['R','W','R'],'drg':'sinistra'},'draga, poppa')],
 tterm('Manovrabilità limitata','Non può lasciare la rotta per il lavoro che fa: posa di cavi, rifornimento, sminamento, rimorchio che non può deviare.')
 +tterm('Di notte','Rosso, bianco, rosso in verticale; in abbrivio anche testa d\'albero, laterali e coronamento.')
 +tterm('La draga','È manovrabilità limitata. In più due rossi (di giorno due palloni) dal lato ostruito, due verdi (due rombi) da dove si passa.'),
 'Quiz 1.5.2-26 (la draga è una nave con manovrabilità limitata), 1.5.2-8 (la manovrabilità limitata cede a chi non governa), 1.5.1-21 (i segnali diurni della draga sono quelli del COLREG). Regola 27(b) e (d). Nelle figure la draga ha il lato ostruito a sinistra.',
 trick='R-B-R: rosso, bianco, rosso. Dalla draga si passa dal lato dei verdi: verde = via libera.',tc=PURPLE)

# ============ TRE NAVI DA RICONOSCERE ============
def tri(day,night,kind='ship'):
    return f'{svgi(260,260,dayview(day,kind=kind),"Di giorno",dw=210,dh=210,pan=False)}{svgi(260,260,nview(night[0],night[1],h=260),"Di notte",dw=270,dh=270,pan=False)}'
TR=[(['ball','ball'],('dritta',{'col':['R','R'],'sd':True}),'Nave che non governa','Per un guasto non può manovrare. Di giorno due palloni; di notte due rossi in verticale, tutto intorno; in abbrivio anche laterali e coronamento.',LRED),
    (['cyl'],('dritta',{'col':['m','R','R','R'],'sd':True}),'Condizionata dalla sua immersione','Nave a motore che per il pescaggio non può lasciare la rotta. Di giorno un cilindro; di notte i fanali del motore più tre rossi in verticale.',BLUE),
    ([],('prora',{'col':['W','R'],'sd':True}),'Nave pilota in servizio','Di notte bianco sopra rosso, tutto intorno; in abbrivio anche laterali e coronamento, alla fonda il fanale di fonda.',SEA)]
cc=''.join(card(f'<div style="display:flex; gap:10px; align-items:end">{tri(d,n)}</div>'+h3(t,30,c)+p(x,24),None,20,10) for d,n,t,x,c in TR)
sec('nongoverna', head('COLREG · fanali speciali','Tre navi da riconoscere')+f'<div style="display:flex; gap:18px">{cc}</div>'+note('Due rossi: non governa. Tre rossi: troppo pescaggio. Bianco su rosso: c\'è il pilota.',CORAL,32),
 notes='Quiz 1.5.1-16 (il motore lascia sempre libera la rotta a chi non governa), 1.5.1-25 (condizionata dall\'immersione oltre 50 m: i fanali e i segnali del COLREG), 1.5.1-46 (nave pilota: i fanali e i segnali del COLREG), 1.5.1-14 (il diporto non ha mai la precedenza sulle navi con luci speciali). Regole 27(a), 28 e 29. La nave pilota di giorno alza la bandiera H del Codice internazionale (bianca e rossa).')
X=128
ship_slide('fonda','COLREG · fanali speciali','La nave alla fonda',(['W'],'un bianco visibile tutto intorno'),(['ball'],'un pallone nero, da 7 m in su','sail'),
 [('dritta',{'col':['W'],'kind':'sail'},'vela alla fonda'),('prora',{'col':['W']},'motore alla fonda'),('poppa',{'col':['W']},'di poppa'),('sinistra',{'anc2':True},'oltre 50 m: due bianchi')],
 tterm('Sotto i 50 m','Un bianco visibile tutto intorno, dove si vede meglio.')
 +tterm('Da 50 m in su','Due bianchi: a prora più alto, a poppa più basso.')
 +tterm('Di giorno','Un pallone nero a prora, per tutte le unità da 7 m in su.')
 +tterm('Niente abbrivio','Laterali e coronamento spenti. I ponti si possono illuminare con i fanali di servizio.'),
 'Quiz 1.5.1-10 e -54 (di giorno: un pallone nero), -57 (figura: unità alla fonda sotto i 50 m), -31 (all\'ancora si possono accendere i fanali di servizio per illuminare i ponti). Regola 30 del COLREG.',
 trick='Un pallone solo: sono ferma, all\'ancora.',tc=SEA)

# ============ I TRUCCHETTI ============
TC=[('Ancorotto · i quiz sui fanali','Tra le tre risposte scegli quella che cita il <b>Regolamento per prevenire gli abbordi in mare</b> (COLREG): è sempre quella giusta.',NAVY,BLUE_T),
    ('Cappello rosso','Rosso sopra bianco: reti in superficie, <b>pericolo!</b> Pesca non a strascico.',CORAL,CORAL_T),
    ('Cappello verde','Verde sopra bianco: reti sul fondo, come <b>le alghe</b>. Pesca a strascico.',GREEN,GREEN_T),
    ('R-B-R','Rosso, bianco, rosso: <b>manovrabilità limitata</b>. La draga aggiunge i verdi dal lato dove si passa.',PURPLE,LILAC_T),
    ('Rosso su rosso','Due rossi in verticale: la nave <b>non governa</b>. In inglese: <i>red over red, the captain is dead</i>.',LRED,CORAL_T),
    ('Bianco su rosso','Bianco sopra rosso: c\'è il <b>pilota</b>. In inglese: <i>white over red, pilot ahead</i>.',SEA,SEA_T)]
cc=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px 30px; border-radius:30px">{tag(t,c)}{p(d,28,INK,500,1.4)}</div>' for t,d,c,bg in TC)
sec('trucchetti', head('COLREG · per l\'esame','I trucchetti per ricordare')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:24px">{cc}</div>',
 notes='Riepilogo dei trucchetti, con quelli di Ancorotto del materiale della scuola. Il primo vale per i quiz che chiedono i fanali di navi speciali: 1.5.1-18, -19, -20, -21, -25, -46, -62 e 1.5.2-2 hanno tutti come risposta giusta quella che cita il COLREG.')
quiz_slide('v2','Verifica · Navi particolari',['1.5.1-34','1.5.1-24'],False,'Verifica del paragrafo · quiz ufficiali')
quiz_slide('v2r','Verifica · Navi particolari · risposte',['1.5.1-34','1.5.1-24'],True)

# ================= CAPITOLO 3 · PRECEDENZE =================
GH=[(['ball','ball'],('dritta',{'col':['R','R']}),'Non governa',LRED,'ship'),
    (['ball','dia','ball'],('dritta',{'col':['m','R','W','R'],'sd':True}),'Manovrabilità limitata',PURPLE,'ship'),
    (['cyl'],('dritta',{'col':['m','R','R','R'],'sd':True}),'Condizionata dall\'immersione',BLUE,'ship'),
    (['bicone'],('dritta',{'col':['R','W'],'sd':True}),'Intenta alla pesca',SEA,'ship'),
    ([],('dritta',{'col':['R','G'],'sd':True,'kind':'sail'}),'A vela',GREEN,'sail'),
    ([],('dritta',{'col':['m'],'sd':True}),'A motore',CORAL,'ship')]
cc=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; align-items:center; background:#FFFFFF; {SHADOW}; padding:14px 10px; border-radius:24px; border-top:10px solid {c}"><p style="font-family:{H}; font-size:40px; font-weight:700; line-height:1; color:{c}">{i+1}°</p>{svgi(260,260,dayview(d,kind=k),"Di giorno: "+t,dw=200,dh=200,pan=False)}<p style="font-size:22px; font-weight:900; color:{INK}; text-align:center; line-height:1.15; height:52px">{t}</p>{svgi(260,200,nview(n[0],n[1]),"Di notte: "+t,dw=220,dh=170,pan=False)}</div>' for i,(d,n,t,c,k) in enumerate(GH))
rule=card(p('<b>Ognuno lascia libera la rotta a chi sta prima di lui</b>: il motore cede a tutti. La <b>raggiungente cede sempre</b>, chiunque sia. Nei canali e negli schemi di separazione del traffico la vela e le unità sotto i 20 m non intralciano le navi che possono navigare solo lì.',24,INK,500,1.38),SUN_T,20,6)
sec('gerarchia', head('COLREG · la scala','La scala delle precedenze')+f'<div style="display:flex; gap:12px">{cc}</div>'+rule, gap=18,
 notes='In ogni colonna il segnale di giorno sopra e le luci di notte sotto (vista di fianco, in abbrivio). Quiz 1.5.2-29 (il motore dà precedenza, nell\'ordine, a: non governa, manovrabilità limitata, pesca, vela), -8 (la manovrabilità limitata cede a chi non governa), 1.5.1-13 e 1.5.2-24 (la pesca cede a chi non governa e alla manovrabilità limitata), 1.5.1-16 (il motore cede sempre a chi non governa), 1.5.1-14 (il diporto non ha mai precedenza sulle navi con luci speciali), 1.5.2-19 (la raggiungente cede), 1.5.2-5 (schemi di separazione del traffico). La nave condizionata dalla sua immersione: regola 18(d), le altre evitano di intralciarla.')

# ============ PRECEDENZE A MOTORE ============
def m_opp():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'
    s+=topboat(130,180,70,-90,'#FFFFFF',NAVY,3)+topboat(170,40,70,90,'#FFFFFF',NAVY,3)
    s+=dpath('M130 140 Q130 110 170 90 L170 80',CORAL,4)+dpath('M170 80 Q170 110 130 130',SEA,4)
    return s
def m_cross():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'
    s+=topboat(110,180,70,-90,'#FFFFFF',NAVY,3)+topboat(200,90,70,180,'#FFFFFF',NAVY,3)+glow(198,101,LRED,6)
    s+=dpath('M110 145 Q112 128 160 128 Q262 128 272 36',CORAL,4)+dpath('M165 90 L20 90',GREY,3)
    return s
def m_over():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+sector(150,90,150,112.5,247.5,SUN,0.25)
    s+=topboat(150,70,70,-90,'#FFFFFF',NAVY,3)+topboat(150,190,70,-90,'#FFFFFF',NAVY,3)+dpath('M150 160 Q210 110 210 40',CORAL,4)
    return s
MM=[(m_cross(),'Rotte incrociate','Ha la precedenza chi viene da <b>dritta</b>. Chi vede l\'altra sulla propria dritta (ne vede il rosso) accosta a dritta e le passa di poppa.'),
    (m_opp(),'Rotte opposte','Si vedono testa d\'albero e tutti e due i laterali: <b>accostano entrambe a dritta</b> e si passano sulla sinistra.'),
    (m_over(),'Sorpasso','Chi raggiunge, cioè sta nei 135° del coronamento dell\'altra, <b>non ha mai</b> la precedenza; la raggiunta l\'ha <b>sempre</b>.')]
cc=''.join(card(svgi(300,220,s,f'Vista dall\'alto: {t}',dw=330,dh=242)+h3(t,28)+p(d,22),None,20,8) for s,t,d in MM)
box=card('<ul style="font-size:23px; line-height:1.38; color:#34465E; display:flex; flex-direction:column; gap:4px"><li>Nel dubbio il pericolo si considera <b>esistente</b>.</li><li>La manovra per dare precedenza è <b>decisa, tempestiva ed evidente</b>.</li><li>Per evitare una collisione si manovra con <b>ampio margine di tempo</b>, rispettando le regole.</li><li>Cambi di rotta e velocità <b>ampi</b>, che l\'altro veda a vista o al radar.</li></ul>'+note('Vedo il suo rosso: cedo io.',CORAL,32),SUN_T,22,8,flex='none',extra='; width:470px')
sec('precmotore', head('COLREG · a motore: chi viene da dritta','Le precedenze tra unità a motore')+f'<div style="display:flex; gap:18px; align-items:stretch">{cc}{box}</div>',
 notes='Quiz 1.5.2-9, -39, -44 (rotte incrociate: ha precedenza chi viene da dritta; chi viene da sinistra accosta a dritta e passa di poppa), -1 e -46 (rotte opposte: entrambe a dritta), -41 (pericolo con fiancate opposte), -17, -19, -45, -54, -58 (raggiungente), -56 (nel dubbio il pericolo esiste), -57 (manovra decisa, tempestiva, evidente), -4 (cambi ampi ed evidenti, a vista o al radar), -43 (chi non ha la precedenza manovra). Il trucchetto: se dell\'altra vedo il rosso, lei è alla mia dritta e cedo io; se vedo il verde, mantengo rotta e velocità.')

# ============ PRECEDENZE A VELA ============
def v_mure():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+''.join(arrow(x,10,x,50,GREY,5,14) for x in (40,150,260))
    return s+sailtop(90,160,80,-45,1)+sailtop(220,160,80,-135,-1)+lab_svg(70,215,'A')+lab_svg(240,215,'B')
def v_stesse():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+''.join(arrow(x,10,x,50,GREY,5,14) for x in (40,150,260))
    return s+sailtop(110,110,80,-45,1)+sailtop(190,180,80,-45,1)+lab_svg(70,110,'A')+lab_svg(150,200,'B')
def v_opp():
    s=f'<rect x="0" y="0" width="300" height="220" fill="{CHART}"/>'+''.join(arrow(x,10,x,50,GREY,5,14) for x in (40,150,260))
    return s+sailtop(70,140,80,0,1)+sailtop(230,140,80,180,-1)+lab_svg(70,200,'A')+lab_svg(230,200,'B')
def lab_svg(x,y,t): return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial" font-size="22" font-weight="900" fill="{NAVY}">{t}</text>'
VV=[(v_mure(),'Mure diverse','Cede chi ha il vento a <b>sinistra</b> (mure a sinistra): qui A.'),
    (v_stesse(),'Stesse mure','Cede chi è <b>sopravento</b> a chi è sottovento: qui A.'),
    (v_opp(),'Rotte opposte','Mure diverse anche qui: cede chi ha le mure a sinistra, qui A.')]
cc=''.join(card(svgi(300,220,s,f'Vista dall\'alto con vento da Nord: {t}',dw=330,dh=242)+h3(t,28)+p(d,22),None,20,8) for s,t,d in VV)
side=card(svgi(260,260,dayview(['cone_d'],kind='sail'),'Barca a vela con un cono nero con il vertice in basso',dw=200,dh=200,pan=False)+p('Con il <b>cono con il vertice in basso</b> naviga a vela e a motore: è una barca a motore e <b>perde il diritto di precedenza</b>.',22,INK,500,1.35)+p('Il motore cede alla vela; la vela che raggiunge cede lo stesso.',22,INK,500,1.35),SUN_T,22,8,flex='none',extra='; width:460px')
sec('precvela', head('COLREG · a vela: conta il vento','Le precedenze tra unità a vela')+f'<div style="display:flex; gap:18px; align-items:stretch">{cc}{side}</div>',
 notes='Quiz 1.5.2-6, -15, -31, -32 (mure diverse: chi ha il vento a sinistra cede), -7, -16, -59 (stesse mure: sopravento cede a sottovento), 1.5.2-29 (motore cede alla vela), 1.5.1-9 e -55 (cono con il vertice in basso: vela e motore). Nei disegni il boma sta sottovento: se il boma è a dritta il vento arriva da sinistra (mure a sinistra).')

# ============ RISCHIO DI COLLISIONE ============
X=128
b=f'<rect x="20" y="20" width="520" height="580" rx="20" fill="#DDF1F7"/><rect x="552" y="20" width="520" height="580" rx="20" fill="#DDF1F7"/>'
P_=(280,110); A0=(450,560); B0=(110,560)
b+=f'<circle cx="{P_[0]}" cy="{P_[1]}" r="24" fill="none" stroke="{LRED}" stroke-width="4"/><path d="M{P_[0]-14} {P_[1]-14} L{P_[0]+14} {P_[1]+14} M{P_[0]+14} {P_[1]-14} L{P_[0]-14} {P_[1]+14}" stroke="{LRED}" stroke-width="4"/>'
b+=dpath(f'M{A0[0]} {A0[1]} L{P_[0]} {P_[1]}',BLUE,3)+dpath(f'M{B0[0]} {B0[1]} L{P_[0]} {P_[1]}',CORAL,3)
for i,t in enumerate((0,0.25,0.5)):
    a=(A0[0]+(P_[0]-A0[0])*t, A0[1]+(P_[1]-A0[1])*t); bb=(B0[0]+(P_[0]-B0[0])*t, B0[1]+(P_[1]-B0[1])*t)
    angA=math.degrees(math.atan2(P_[1]-A0[1],P_[0]-A0[0])); angB=math.degrees(math.atan2(P_[1]-B0[1],P_[0]-B0[0]))
    b+=dash(bb[0]+20,bb[1],a[0]-20,a[1],NAVY,2)+topboat(a[0],a[1],60,angA,'#FFFFFF',NAVY,3,0.45+0.25*i,False)+topboat(bb[0],bb[1],60,angB,'#FFFFFF',NAVY,3,0.45+0.25*i,False)
b+=dpath('M195 335 Q262 300 300 380 T 440 470',GREEN,4)
E1=(640,80); E2=(990,560); M_=((E1[0]+E2[0])/2,(E1[1]+E2[1])/2); ang=math.degrees(math.atan2(E2[1]-E1[1],E2[0]-E1[0]))
b+=dpath(f'M{E1[0]} {E1[1]} L{E2[0]} {E2[1]}',BLUE,3)+f'<circle cx="{M_[0]}" cy="{M_[1]}" r="22" fill="none" stroke="{LRED}" stroke-width="4"/>'
for t in (0.12,0.3): q=(E1[0]+(E2[0]-E1[0])*t,E1[1]+(E2[1]-E1[1])*t); b+=topboat(q[0],q[1],56,ang,'#FFFFFF',NAVY,3,0.5+t,False)
for t in (0.7,0.88): q=(E1[0]+(E2[0]-E1[0])*t,E1[1]+(E2[1]-E1[1])*t); b+=topboat(q[0],q[1],56,ang+180,'#FFFFFF',NAVY,3,1.3-t,False)
lbl=(lab(X+40,Y+30,480,'Rotte convergenti',NAVY,26,900,'center')+lab(X+572,Y+30,480,'Rotte opposte',NAVY,26,900,'center')
     +lab(X+310,Y+90,220,'punto di collisione',LRED,22,900)+lab(X+40,Y+590,120,'B',CORAL,28,900,'center')+lab(X+400,Y+590,120,'A',BLUE,28,900,'center')
     +lab(X+200,Y+470,330,'rilevamenti polari uguali',NAVY,22,800)+lab(X+60,Y+250,240,'B accosta a dritta',GREEN,22,900))
txt=(term('Il segnale d\'allarme','Rilevamento che non cambia e distanza che diminuisce: le due barche arrivano nello stesso punto nello stesso momento.')
     +term('Come accorgersene','Con rilevamenti polari successivi. Nel dubbio il pericolo esiste.')
     +term('Rotte convergenti','Cede chi vede l\'altra a dritta: B accosta a dritta e passa di poppa ad A.')
     +term('Rotte opposte','Accostano entrambe a dritta.'))
sec('rischio', head('COLREG · rischio di collisione','Il rischio di collisione'), pinned=svgp(X,Y,W,Hh,b,'A sinistra due barche su rotte convergenti: nei tre istanti la retta che le unisce resta parallela, cioè il rilevamento polare non cambia, e B accosta a dritta; a destra due barche su rotte opposte verso lo stesso punto')+lbl+pcol(txt,532,18),
 notes='Quiz 1.5.1-22, 1.5.2-18, -27, -30 (rilevamento costante e distanza che diminuisce), -42, -47, -55 (rilevamenti polari successivi e simultaneità di transito), -56 (nel dubbio il pericolo esiste), -43 (chi non ha la precedenza manovra), -10 (visibilità limitata: velocità di sicurezza).')
X=700
quiz_slide('v3','Verifica · Le precedenze',['1.5.2-29','1.5.2-6'],False,'Verifica del paragrafo · quiz ufficiali')
quiz_slide('v3r','Verifica · Le precedenze · risposte',['1.5.2-29','1.5.2-6'],True)

# ================= CAPITOLO 4 · SEGNALI SONORI E PORTI =================
def snd(seq,w=260):
    g=f'<rect x="0" y="0" width="{w}" height="60" rx="14" fill="{NIGHT}"/>'; x=18
    for s_ in seq:
        wdt=26 if s_=='.' else 70; g+=f'<rect x="{x}" y="20" width="{wdt}" height="20" rx="10" fill="{SUN}"/>'; x+=wdt+12
    return g
def sbar(seq,dw=200): return svgi(260,60,snd(seq),'Sequenza di suoni: '+seq.replace('.','breve ').replace('-','prolungato '),dw=dw,dh=dw*60/260,pan=False)
# ============ APPARECCHI ============
def ico(kind):
    s=f'<rect width="200" height="170" rx="20" fill="#DDF1F7"/>'
    if kind=='claxon': s+=f'<ellipse cx="100" cy="96" rx="58" ry="36" fill="#C9D3DC" stroke="{NAVY}" stroke-width="3"/>'+''.join(f'<path d="M{60+i*16} 84 Q100 70 {140-i*16} 84" fill="none" stroke="{NAVY}" stroke-width="2"/>' for i in range(3))
    elif kind=='tromba': s+=f'<rect x="120" y="60" width="40" height="90" rx="8" fill="{LRED}"/><path d="M126 60 L100 50 L40 30 L40 80 L100 62 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/>'
    elif kind=='corno': s+=f'<path d="M60 140 L140 30 L162 46 L72 146 Z" fill="#6FA8DC" stroke="{NAVY}" stroke-width="3"/><circle cx="151" cy="38" r="16" fill="#6FA8DC" stroke="{NAVY}" stroke-width="3"/>'
    elif kind=='fischio': s+=f'<rect x="40" y="90" width="30" height="50" fill="{NAVY}"/><path d="M70 96 L170 60 L170 140 L70 120 Z" fill="#E6EDF2" stroke="{NAVY}" stroke-width="3"/>'
    elif kind=='campana': s+=f'<path d="M70 130 Q70 60 100 50 Q130 60 130 130 L144 140 L56 140 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/><circle cx="100" cy="148" r="8" fill="{NAVY}"/><rect x="94" y="36" width="12" height="16" fill="{NAVY}"/>'
    else: s+=f'<circle cx="100" cy="96" r="56" fill="#D9B45A" stroke="{NAVY}" stroke-width="3"/><circle cx="100" cy="96" r="18" fill="#C49A3A"/><path d="M60 24 L100 40 L140 24" fill="none" stroke="{NAVY}" stroke-width="3"/>'
    return s
AP=[('claxon','Claxon elettrico'),('tromba','Tromba ad aria compressa'),('corno','Corno a fiato'),('fischio','Fischio · da 12 m'),('campana','Campana · da 20 m'),('gong','Gong · da 100 m')]
cc=''.join(tile(ico(k),t,t,w=200,h=170,dw=300,dh=255) for k,t in AP)
txt=(tterm('Sotto i 12 m','Nessun apparecchio prescritto, ma serve comunque un mezzo capace di un segnale sonoro efficace.')
     +tterm('Le navi','Da 12 m il fischio, da 20 m anche la campana, da 100 m anche il gong.')
     +tterm('Breve e prolungato','Breve: circa 1 secondo. Prolungato: da 4 a 6 secondi.')
     +tterm('Pericolo o soccorso','Un suono continuo con qualsiasi apparecchio da nebbia.'))
sec('apparecchi', head('COLREG · farsi sentire','Gli apparecchi per i segnali sonori')+f'<div style="display:flex; gap:32px; align-items:start"><div style="flex:1; display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px 18px">{cc}</div>{col(txt,470,16)}</div>', gap=24,
 notes='Quiz 1.5.2-13 e -51 (sotto i 12 m nessun obbligo di fischio e campana, ma un mezzo sonoro efficace), 1.5.2-14 (pericolo: suono continuo con un apparecchio da nebbia). Regola 33 del COLREG (fischio da 12 m, campana da 20 m, gong da 100 m) e regola 32 (breve circa 1 secondo, prolungato da 4 a 6 secondi). Per il diporto le dotazioni sono nel DM 133/2024.')

# ============ SEGNALI DI MANOVRA ============
def turn(kind):
    s=f'<rect width="300" height="200" fill="{CHART}"/>'+topboat(150,150,80,-90,'#FFFFFF',NAVY,3)
    if kind=='dx': s+=dpath('M150 108 Q150 60 240 50',CORAL,4)+head_at(240,50,0,CORAL)
    elif kind=='sx': s+=dpath('M150 108 Q150 60 60 50',CORAL,4)+head_at(60,50,180,CORAL)
    else: s+=dpath('M150 192 L150 196',CORAL,4)+arrow(150,190,150,198,CORAL,4,12)+arrow(150,110,150,40,'#B9C4CE',4,14)+arrow(110,190,110,196,CORAL,4,12)
    return s
def turn_back():
    return f'<rect width="300" height="200" fill="{CHART}"/>'+topboat(150,80,80,-90,'#FFFFFF',NAVY,3)+arrow(150,124,150,186,CORAL,5,16)
SM=[('.','Accosto a dritta',turn('dx')),('..','Accosto a sinistra',turn('sx')),('...','Macchine indietro',turn_back())]
cc=''.join(card(svgi(300,200,s,f'Vista dall\'alto: {t}',dw=420,dh=280)+sbar(q,280)+h3(t,32),None,20,12) for q,t,s in SM)
extra=''.join(f'<div style="flex:1; display:flex; gap:16px; align-items:center; background:#FFFFFF; {SHADOW}; padding:12px 18px; border-radius:20px; border-left:10px solid {c}">{sbar(q,170)}{p(t,24,INK,800,1.25)}</div>' for q,t,c in (('.....','Non capisco le tue intenzioni: attenzione!',CORAL),('-','Curva cieca o uscita dal porto senza visibilità',PURPLE)))
side=card(note('I soldatini in marcia: tutti brevi, un secondo ciascuno.',CORAL,30),SUN_T,18,6,flex='none',extra='; width:520px; justify-content:center')
sec('sonori', head('COLREG · con il fischio','I segnali sonori di manovra')+f'<div style="display:flex; gap:18px; align-items:stretch">{cc}</div><div style="display:flex; gap:18px; align-items:stretch">{extra}{side}</div>', gap=22,
 notes='Li usano le unità a motore in vista l\'una dell\'altra quando manovrano (regola 34). Quiz 1.5.2-21 e -49 (1 breve = accosto a dritta), -23 e -28 (2 brevi = a sinistra), 1.4.1-15 (uscendo dal porto senza visibilità: 1 prolungato e ascoltare). I 3 brevi (macchine indietro) e i 5 brevi (dubbio) sono della regola 34 del COLREG.')

# ============ SORPASSO ============
def canal(kind):
    s=f'<rect width="240" height="300" fill="#BFE6F2"/><path d="M0 0 L40 0 Q30 150 44 300 L0 300 Z M240 0 L200 0 Q212 150 196 300 L240 300 Z" fill="#9CCB86"/>'
    s+=topboat(120,110,60,-90,'#C69C6D',NAVY,3)+topboat(120,240,70,-90,'#FFFFFF',NAVY,3)
    if kind=='dx': s+=dpath('M120 200 Q170 160 160 60',CORAL,4)
    elif kind=='sx': s+=dpath('M120 200 Q70 160 80 60',CORAL,4)
    else: s+=''.join(f'<path d="M{150+k*14} {90-k*6} q12 20 0 40" fill="none" stroke="{SEA}" stroke-width="4" opacity="{1-k*0.3}"/>' for k in range(3))
    return s
_cv='Canale stretto visto dall\'alto: '
SO=[('--.','Voglio sorpassarti a dritta',canal('dx'),PURPLE),('--..','Voglio sorpassarti a sinistra',canal('sx'),PURPLE),('-.-.','Sei d\'accordo: puoi passare',canal('ok'),SEA)]
cc=''.join(card(f'<div style="display:flex; gap:18px; align-items:center">{svgi(240,300,s,_cv+t,dw=260,dh=325)}<div style="display:flex; flex-direction:column; gap:12px">{sbar(q,200)}{h3(t,28,c)}</div></div>',None,20,8) for q,t,s,c in SO)
txt=p('In un canale stretto chi vuole sorpassare <b>chiede il consenso</b>: 2 prolungati più 1 breve (a dritta) o 2 brevi (a sinistra). Chi è davanti risponde prolungato, breve, prolungato, breve; se non è d\'accordo o ha dubbi, 5 brevi.',25,INK,500,1.4)
sec('sorpasso', head('COLREG · nei canali stretti','I segnali sonori di sorpasso')+f'<div style="display:flex; flex-direction:column; gap:14px">{cc}</div>'.replace('flex-direction:column; gap:14px','gap:16px')+card(txt,SUN_T,22,6,flex='none'), gap=22,
 notes='Quiz 1.5.2-22 e -37 (2 prolungati e 2 brevi: sorpasso a sinistra), -48 (2 prolungati e 1 breve: a dritta), -50 (l\'intenzione di sorpassare si segnala con 2 prolungati, poi 1 o 2 brevi). Benestare e dubbio: regola 34(c) e (d) del COLREG.')

# ============ NEBBIA IN NAVIGAZIONE ============
def fog(kind):
    s=f'<rect width="300" height="220" fill="#C9D3DC"/><rect y="170" width="300" height="50" fill="{WATER}" fill-opacity="0.4"/>'
    s+=(profile(40,180,220,sup=True) if kind!='vela' else f'<path d="M70 166 L230 166 L210 186 L90 186 Z" fill="{NAVY}"/><path d="M150 166 V40" stroke="{NAVY}" stroke-width="5"/><path d="M156 50 L156 160 L222 160 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>')
    s+=''.join(f'<rect x="0" y="{y}" width="300" height="{h}" fill="#FFFFFF" fill-opacity="0.45"/>' for y,h in ((30,26),(110,22)))
    if kind=='ferma': s+=f'<path d="M20 200 h260" stroke="{CORAL}" stroke-width="4" stroke-dasharray="4 8"/>'
    return s
NB=[('-','fermo','A motore con abbrivio','1 prolungato.',),('--','ferma','A motore, ferma senza abbrivio','2 prolungati, a circa 2 secondi l\'uno dall\'altro.'),('-..','vela','A vela','1 prolungato e 2 brevi, di giorno e di notte. Lo stesso per chi non governa, ha manovrabilità limitata, pesca o rimorchia.')]
cc=''.join(card(svgi(300,220,fog(k),f'Nella nebbia: {t}',dw=430,dh=315)+sbar(q,280)+h3(t,30)+p(d,24),None,20,10) for q,k,t,d in NB)
side=card(p('<b>Ogni 2 minuti al massimo.</b> Rallenta alla <b>velocità di sicurezza</b> per le condizioni del momento, accendi i fanali, emetti i segnali e <b>ascolta</b>.',26,INK,500,1.4),SUN_T,20,6,flex='none')
sec('nebbia', head('COLREG · visibilità ridotta','In navigazione con la nebbia')+f'<div style="display:flex; gap:18px; align-items:stretch">{cc}</div>'+side, gap=20,
 notes='Quiz 1.5.2-20 e -53 (motore con abbrivio: 1 prolungato a intervalli non superiori a 2 minuti), -40 (motore ferma e senza abbrivio: 2 prolungati), -52 (vela: 1 prolungato e 2 brevi), -10 (velocità di sicurezza), 1.5.2-12 (fanali accesi anche di giorno con visibilità ridotta). Regola 35 del COLREG.')

# ============ FONDA CON LA NEBBIA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#C9D3DC"/><rect y="470" width="1092" height="150" fill="{WATER}" fill-opacity="0.4"/>'
b+=profile(250,480,560,sup=True)+f'<path d="M760 470 L860 610" stroke="{NAVY}" stroke-width="3" stroke-dasharray="6 6"/>'
b+=f'<g transform="translate(770 300)"><path d="M-30 60 Q-30 0 0 -10 Q30 0 30 60 L44 70 L-44 70 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/><rect x="-6" y="-26" width="12" height="18" fill="{NAVY}"/></g>'
b+=''.join(f'<path d="M{830+k*30} {320-k*10} q20 40 0 80" fill="none" stroke="{SUN}" stroke-width="6" stroke-linecap="round" opacity="{1-k*0.25}"/>' for k in range(3))
b+=''.join(f'<rect x="0" y="{y}" width="1092" height="{h}" fill="#FFFFFF" fill-opacity="0.45"/>' for y,h in ((60,60),(200,50),(400,60)))
lbl=lab(X+640,Y+200,420,'campana a prora · 5 secondi',NAVY,26,900)+lab(X+60,Y+40,500,'almeno una volta al minuto',NAVY,26,900)
txt=(term('Alla fonda, da 20 m','Rapidi colpi di campana a prora per 5 secondi, a intervalli non superiori a 1 minuto.')
     +term('Da 100 m','Anche il gong a poppa, subito dopo la campana.')
     +term('Sotto i 12 m','Un qualsiasi segnale sonoro efficace, almeno ogni 2 minuti.')
     +term('Pericolo o soccorso','Un suono continuo con qualsiasi apparecchio da nebbia.'))
sec('fondanebbia', head('COLREG · visibilità ridotta','Alla fonda con la nebbia'), pinned=svgp(X,Y,W,Hh,b,'Nave all\'ancora nella nebbia con la campana a prora che suona',pan=False)+lbl+pcol(txt,532,20),
 notes='Quiz 1.5.2-35 (alla fonda oltre 20 m con nebbia: rapidi suoni di campana per 5 secondi a intervalli non superiori a un minuto), 1.5.2-14 (pericolo: suono continuo). Regola 35(g) e (i) del COLREG. Il quiz 1.5.2-36 sulla campana è oscurato.')

# ============ PORTI ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
b+=f'<path d="M0 0 L1092 0 L1092 80 L0 80 Z" fill="{LAND}"/><path d="M180 80 L180 300 L460 300 L460 260 L220 260 L220 80 Z" fill="#C9C2B2" stroke="{NAVY}" stroke-width="3"/><path d="M900 80 L900 300 L632 300 L632 260 L860 260 L860 80 Z" fill="#C9C2B2" stroke="{NAVY}" stroke-width="3"/>'
b+=glow(460,280,LRED,8)+glow(632,280,LGREEN,8)
b+=topboat(546,200,110,90,'#FFFFFF',NAVY,4)+dpath('M546 260 L546 330',SEA,4)
b+=topboat(700,500,110,-100,'#FFFFFF',NAVY,4)+dpath('M690 445 Q660 380 600 330',NAVY,3)
b+=sailtop(260,500,80,-60,1,op=0.6)+f'<path d="M220 460 L300 540 M300 460 L220 540" stroke="{LRED}" stroke-width="6"/>'
b+=f'<path d="M100 620 A480 420 0 0 1 992 620" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="12 8"/>'
lbl=(lab(X+290,Y+310,160,'rosso',LRED,24,900,'right')+lab(X+650,Y+310,160,'verde',LGREEN,24,900)+lab(X+620,Y+110,240,'B esce: ha la precedenza',SEA,24,900)
     +lab(X+760,Y+470,300,'A entra: verso il verde',NAVY,24,900)+lab(X+40,Y+420,300,'500 m: rallenta e cedi',CORAL,24,900)+lab(X+120,Y+560,320,'a vela non si entra',LRED,22,900))
txt=(tterm('Entro 500 m dall\'imboccatura','Rallenta e dai precedenza a chi entra ed esce. In porto si va al massimo a 3 nodi e non si entra a vela.')
     +tterm('I fanali','Entrando ci si dirige verso il verde: verde a dritta, rosso a sinistra.')
     +tterm('Precedenza','A chi esce e alle navi più grandi, in entrata, in uscita e dentro il porto.')
     +tterm('Nei marina','Ormeggi in transito per 72 ore. Quelli per disabili, se liberi, si possono occupare ma vanno lasciati su richiesta fatta 24 ore prima.')
     +tterm('Porto commerciale','Senza servizi per il diporto: avvisa l\'Autorità marittima.'))
sec('porto', head('Condotta · salvo ordinanze locali','Precedenze e navigazione nei porti'), pinned=svgp(X,Y,W,Hh,b,'Imboccatura di un porto vista dall\'alto: fanale rosso a sinistra e verde a dritta di chi entra, la barca B che esce ha la precedenza, la barca A che entra si dirige verso il verde; arco dei 500 metri; una barca a vela barrata',pan=False)+lbl+pcol(txt,532,12),
 notes='Tutto vale salvo ordinanze locali dell\'Autorità marittima. Quiz 1.4.1-4, -9, -17 (precedenza a chi esce; chi transita nei 500 m davanti all\'ingresso cede a chi entra ed esce), -6 (navi di grandi dimensioni), -10 (ridurre a 500 m), -12 (non si entra a vela), -14 (verso il fanale verde), -7, -8, -13 (fanali e torrette dell\'imboccatura), -19 (nel canale tenersi a dritta), -3 (porti con obbligo di tenere la dritta: ordinanze), -5 (porto commerciale: avvisare l\'Autorità marittima), -15 (1 prolungato uscendo senza visibilità), -16 (danni da moto ondoso), -20 (ormeggi in transito 72 ore), -21 (ormeggi per disabili), 1.4.1-2 (velocità in porto, generalmente 3 nodi: quiz oscurato).')
X=700
quiz_slide('v4','Verifica · Segnali sonori e porti',['1.5.2-37','1.4.1-14'],False,'Verifica del paragrafo · quiz ufficiali')
quiz_slide('v4r','Verifica · Segnali sonori e porti · risposte',['1.5.2-37','1.4.1-14'],True)

# ================= CAPITOLO 5 · RICONOSCERE LE LUCI =================
EX=[[('prora',{'col':['m'],'sd':True},'Motore sotto i 50 m, di prora'),('dritta',{'col':['m'],'sd':True},'Motore sotto i 50 m, lato dritto'),('sinistra',{'col':['m'],'sd':True,'mh2':True},'Motore oltre 50 m, lato sinistro'),
     ('prora',{'sd':True,'kind':'sail'},'Vela, di prora'),('dritta',{'col':['R','G'],'sd':True,'kind':'sail'},'Vela con i facoltativi, lato dritto'),('poppa',{'st':True},'Di poppa: la sto raggiungendo')],
    [('prora',{'col':['G','W'],'sd':True},'Pesca a strascico in abbrivio, di prora'),('dritta',{'col':['G','W']},'Pesca a strascico senza abbrivio'),('sinistra',{'col':['R','W'],'sd':True},'Pesca non a strascico, lato sinistro'),
     ('dritta',{'col':['R','W'],'sd':True,'gear':True},'Non a strascico, reti oltre 150 m'),('prora',{'col':['m','m'],'sd':True},'Rimorchiatore, rimorchio fino a 200 m, di prora'),('poppa',{'col':['m','m'],'st':True,'tw':True},'Rimorchiatore, di poppa')],
    [('dritta',{'col':['R','R']},'Non governa, senza abbrivio'),('dritta',{'col':['R','R'],'sd':True},'Non governa con abbrivio, lato dritto'),('prora',{'col':['m','R','W','R'],'sd':True},'Manovrabilità limitata, di prora'),
     ('prora',{'col':['R','W','R'],'drg':'sinistra'},'Draga di prora: si passa dal lato dei verdi'),('dritta',{'col':['m','R','R','R'],'sd':True},'Condizionata dall\'immersione, lato dritto'),('prora',{'col':['W','R'],'sd':True},'Nave pilota in servizio, di prora')],
    [('dritta',{'col':['W'],'kind':'sail'},'Alla fonda, sotto i 50 m'),('sinistra',{'anc2':True},'Alla fonda, oltre 50 m'),('day',['cone_d'],'Vela e motore insieme','sail'),
     ('day',['bicone'],'Intenta alla pesca','ship'),('day',['ball','dia','ball'],'Manovrabilità limitata','ship'),('day',['cyl'],'Condizionata dall\'immersione','ship')]]
def extile(item,reveal,letter):
    if item[0]=='day':
        svg=dayview(item[1],kind=item[3]); w,h=260,260; dw,dh=277,277
    else:
        svg=nview(item[0],item[1],sil=reveal); w,h=260,200; dw,dh=360,277
    cap=f'<b>{letter}</b> · {item[2]}' if reveal else f'<b>{letter}</b>'
    return f'<div style="display:flex; flex-direction:column; gap:6px; align-items:center; background:#FFFFFF; {SHADOW}; padding:8px; border-radius:22px">{svgi(w,h,svg,("Soluzione: "+item[2]) if reveal else "Luci o segnale da riconoscere",dw=dw,dh=dh,pan=False)}<p style="font-size:22px; color:{INK}; text-align:center; line-height:1.2; min-height:{54 if reveal else 28}px">{cap}</p></div>'
for n,items in enumerate(EX,1):
    for reveal in (False,True):
        grid=''.join(extile(it,reveal,'ABCDEF'[i]) for i,it in enumerate(items))
        e='Riconosci le luci · soluzioni' if reveal else ('Di notte: che unità è e da che lato la vedo?' if n<4 else 'Di notte e di giorno: che unità è?')
        sec(f'luci{n}'+('r' if reveal else ''), head(e,f'Riconosci le luci · {n}',SEA if reveal else CORAL)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px 20px">{grid}</div>', gap=18,
            notes=('Soluzioni: '+'; '.join(f'{"ABCDEF"[i]} {it[2]}' for i,it in enumerate(items))) if reveal else 'Far rispondere a voce: che unità è, che cosa sta facendo, da che lato la vedo. Nelle soluzioni compare anche la sagoma.')

# ================= APERTURE DEI CAPITOLI =================
exec(open('apertura.py').read())
chapter('cap1',1,'I fanali',['Quando si accendono i fanali','I fanali di navigazione','Il fanale di testa d\'albero','I fanali laterali','Il fanale di coronamento','Le unità a motore di notte','Le unità a vela di notte','Cosa vedo di notte'],PURPLE,
 'Circa 18 minuti, verifica da 2 quiz compresa: far disegnare i settori alla lavagna.','circa 18 minuti · 8 argomenti',2)
chapter('cap2',2,'Navi particolari e segnali diurni',['Navi a cuscino d\'aria','Rimorchiatore e rimorchiata','Pesca non a strascico','Pesca a strascico','Draga e manovrabilità limitata','Non governa, immersione, pilota','La nave alla fonda','I trucchetti per ricordare'],CORAL,
 'Circa 17 minuti, verifica da 2 quiz compresa. Per ogni nave: luci da lontano, segnale di giorno, viste dai quattro lati e il trucchetto.','circa 17 minuti · 8 argomenti',2,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
chapter('cap3',3,'Precedenze e rischio di collisione',['La scala delle precedenze','Le precedenze tra unità a motore','Le precedenze tra unità a vela','Il rischio di collisione'],BLUE,
 'Circa 13 minuti, verifica da 2 quiz compresa: provare i casi con due modellini.','circa 13 minuti · 4 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
chapter('cap4',4,'Segnali sonori e porti',['Gli apparecchi sonori','I segnali di manovra','I segnali di sorpasso','In navigazione con la nebbia','Alla fonda con la nebbia','Precedenze nei porti'],SEA,
 'Circa 14 minuti, verifica da 2 quiz compresa. Far fare i segnali a voce: breve «tu», prolungato «tuuu».','circa 14 minuti · 6 argomenti',1,art=(radio_scene(),'Illustrazione: apparato radio con le onde sonore'))
chapter('cap5',5,'Riconoscere le luci',['Motore e vela','Pesca e rimorchio','Luci speciali','Fonda e segnali diurni'],SUN,
 'Circa 10 minuti: 4 esercizi da 6 casi con le soluzioni. Chi risponde dice che unità è e da che lato la vede.','circa 10 minuti · 24 casi',1,art=(quiz_scene(),'Illustrazione: scheda di quiz con le risposte segnate e un cronometro'))

# ================= RACCOLTA QUIZ =================
QZ=[('q01','Quiz 1 · Quando si accendono',['1.5.1-23','1.5.1-27','1.5.2-11']),('q02','Quiz 2 · I settori',['1.5.1-4','1.5.1-30','1.5.1-12']),
 ('q03','Quiz 3 · Motore di notte',['1.5.1-1','1.5.1-38','1.5.1-29']),('q04','Quiz 4 · Vela e piccole unità',['1.5.1-61','1.5.1-15','1.5.1-40']),
 ('q05','Quiz 5 · Navi particolari',['1.5.1-3','1.5.1-17','1.5.2-26']),('q06','Quiz 6 · Pesca e fonda',['1.5.1-2','1.5.1-32','1.5.1-10']),
 ('q07','Quiz 7 · Il trucchetto del COLREG',['1.5.1-62','1.5.1-25','1.5.2-2']),('q08','Quiz 8 · La scala delle precedenze',['1.5.1-13','1.5.2-8','1.5.1-14']),
 ('q09','Quiz 9 · A motore e chi raggiunge',['1.5.2-9','1.5.2-46','1.5.2-54']),('q10','Quiz 10 · Rischio e manovra',['1.5.2-18','1.5.2-56','1.5.2-57']),
 ('q11','Quiz 11 · Segnali sonori',['1.5.2-21','1.5.2-48','1.5.2-13']),('q12','Quiz 12 · Nebbia e porti',['1.5.2-52','1.5.2-35','1.4.1-17'])]
raccolta(5,6,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Cita il COLREG?','Nei quiz sui fanali di navi speciali la risposta giusta è quella che cita il Regolamento.'),
  ('Disegna la barca','Settori e precedenze: schizza la barca vista dall\'alto con 225°, 112,5° e 135°.'),
  ('Conta i suoni','Brevi per manovrare, prolungati per sorpassare e nella nebbia, ogni 2 minuti.')],
 ['Quiz 1-7 · fanali e navi particolari (21)','Quiz 8-10 · precedenze e rischio di collisione (9)','Quiz 11-12 · segnali sonori, nebbia e porti (6)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Far rispondere ad alta voce con la lettera, poi chiedere perché le altre due sono sbagliate. Se il tempo stringe, lasciare per casa le slide 4 e 7.',esame=['colreg'])
closing(['Fanali dal tramonto al sorgere del sole e con visibilità ridotta; per il diporto oltre 1 miglio dalla costa','Testa d\'albero 225°, laterali 112,5° (verde a dritta, rosso a sinistra), coronamento 135°',
  'Rosso su bianco pesca, verde su bianco strascico, R-B-R manovrabilità limitata, due rossi non governa','Cede chi vede l\'altra a dritta; la raggiungente cede sempre; a vela cedono mure a sinistra e sopravento',
  '1, 2, 3 brevi per manovrare; nella nebbia un prolungato ogni 2 minuti; in porto verso il verde e chi esce passa'],
 'Prossima lezione · 06 · La sicurezza e i suoi elementi nella navigazione','A casa: i 67 quiz su fanali e segnali diurni, i 60 sulle precedenze e i quiz 1.4.1 sui porti.')
write_deck(OUT,'Lezione 05 · COLREG e prevenzione degli abbordi',
 ['cover','agenda','colreg',
  'cap1','obbligo','fanali','testa','laterali','coronamento','motorenotte','velanotte','cosavedo','v1','v1r',
  'cap2','cuscino','rimorchio','pescanon','strascico','draga','nongoverna','fonda','trucchetti','v2','v2r',
  'cap3','gerarchia','precmotore','precvela','rischio','v3','v3r',
  'cap4','apparecchi','sonori','sorpasso','nebbia','fondanebbia','porto','v4','v4r',
  'cap5']+[f'luci{n}{s}' for n in range(1,5) for s in ('','r')]+['capquiz','quiz']+[q+s for q,_,_ in QZ for s in ('','r')]+['chiusura'],
 {"s1":{"description":"Apertura, obiettivi e il COLREG","start":"cover"},"s2":{"description":"I fanali: obbligo, testa d'albero, laterali, coronamento, motore e vela","start":"cap1"},
  "s3":{"description":"Navi particolari e segnali diurni, trucchetti","start":"cap2"},"s4":{"description":"Scala delle precedenze, regole a motore e a vela, rischio di collisione","start":"cap3"},
  "s5":{"description":"Apparecchi e segnali sonori, nebbia, porti","start":"cap4"},"s6":{"description":"Esercizi: riconoscere le luci","start":"cap5"},
  "s7":{"description":"Raccolta quiz","start":"capquiz"}})
