import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez08/project'
GREY='#97A6B4'; SKY='#DDEFF7'; LRED='#E23B3B'; ORANGE='#F28C28'; LAND='#F2E2B3'; LAND_S='#C9A96B'
LB.ICON_T.update({'La carta 5/D e i tre settori':'map','Le coordinate di un punto':'grid','La distanza':'dividers','Ora di arrivo o velocità':'compass','Il carburante da imbarcare':'fuel','Il metodo in cinque passi':'dividers','Gli errori che costano il quesito':'check','La prova di carteggio':'dividers','Il metodo per i 5 quesiti':'dividers','La traccia':'map','I 5 quesiti risolti':'map','La lezione di oggi':'lifebuoy','La vela in otto flash':'sail','La corrente':'current','Dalla prora alla rotta':'dividers',
 'Quale prora per la mia rotta':'compass','Trovare la corrente':'map','La falla':'hull','Incaglio e collisione':'hull','Incendio a bordo':'lifebuoy',
 'Uomo a mare':'lifebuoy','Abbandonare la barca':'lifebuoy','Il VHF di bordo':'lantern','Chiamare aiuto via radio':'lantern','Chi ci aiuta':'flag',
 'Il cattivo tempo':'wind','Alcol, droghe e farmaci':'check'})
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=24,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def pol(cx,cy,b,r): return (cx+r*math.sin(math.radians(b)), cy-r*math.cos(math.radians(b)))
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
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(8,'Quiz ed esercizi di carteggio di navigazione entro le 12 miglia','Dalla carta 5/D ai 5 quesiti: coordinate, distanza, tempo e carburante, fino alla prova d&#39;esame in 20 minuti',
 'Lezione 8, per tutti i percorsi: è l\'ultima lezione della patente entro 12 miglia a motore ed è tutta dedicata alla prova di carteggio entro 12 miglia (DM 323/2021 art. 6; elenco 4.1.1 del DD 131/2022, 50 esercizi sulla carta 5/D). Riprende gli strumenti e i calcoli delle lezioni 3, 4 e 5. Le emergenze sono nella lezione 6; la vela nella lezione 9, solo per chi fa la patente a vela; dalla 10 il carteggio oltre 12 miglia.', title_size=72)
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','10′','Cap. 1 · La prova e la carta 5/D',NAVY),('0:10','20′','Cap. 2 · Coordinate, distanza, tempo, carburante · 2 verifiche',SEA),('0:30','45′','Cap. 3 · Il metodo, quattro esercizi e la prova simulata',CORAL),('1:15','45′','Raccolta quiz: 36 quiz ufficiali',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['navigazione'],8,extra=' La prova di carteggio è a parte: 5 quesiti, almeno 4 giusti.')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>leggere le coordinate di un punto sulla carta 5/D</li><li>misurare una distanza con il compasso</li><li>calcolare ora di arrivo, velocità e carburante</li><li>evitare gli errori che costano un quesito</li><li>risolvere un esercizio ufficiale in 20 minuti</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 08 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Tre capitoli in 75 minuti: andare spediti sulla teoria per lasciare tempo agli esercizi; due verifiche da 2 quiz nel capitolo 2 e, negli ultimi 45 minuti, una raccolta di 36 quiz ufficiali di navigazione cartografica (1.7.1, 1.7.2, 1.7.4, 1.7.5, 1.7.7 del DD 131/2022). Esercizi: cinque esercizi ufficiali dell\'elenco 4.1.1, uno per ogni tipo: velocità data (4.1.1-1 e -19), orario di arrivo dato (4.1.1-35), mezz\'ora di moto (4.1.1-6) e la prova simulata a tempo (4.1.1-40). Ogni settore della carta compare almeno una volta.')


# ============ CARTEGGIO ENTRO 12 MIGLIA: STRUMENTI ============
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
import json as _json, re as _re
import geo, chart
E12={e['id']:e for e in _json.load(open(SP+'/rotta-giusta/site/dati/carteggio_e12.json'))}
CHARTBG='#FBF8EF'
def chart_html(S, x, y, w, h, solution, alt):
    body,labels,glabs,sbl,C=chart.render(S,w,h,solution)
    svg=f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px">{body}</svg>'
    html=''; last=-99
    for kind,v,t in glabs:
        if kind=='lat' and 30<v<h-40 and v-last>0:
            html+=lab(x+10,y+v-30,130,t,'#5E6E82',20,800)
    lastx=-999
    for kind,v,t in glabs:
        if kind=='lon' and 60<v<w-230 and v-lastx>150:
            html+=lab(x+v+6,y+h-34,140,t,'#5E6E82',20,800); lastx=v
    sx,sy,L,t=sbl; html+=lab(x+sx,y+sy,max(L,120),t,'#16324F',20,900)
    for lx,ly,lw,t,c,kind in chart.place_labels(labels,w,h,22):
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px">{t}</p>'
    return svg+html
def mid_ll(r):
    r=r.replace('’','').replace("'",'').replace(' ','')
    v=[(int(g)+((float(a)+float(b))/2)/60) for g,a,b in _re.findall(r'(\d+)°\((\d+\.?\d*)÷(\d+\.?\d*)\)',r)]
    return v[0],v[1]
class Ex12:
    def __init__(s,id_,A,B):
        s.ex=E12[id_]; q={x['n']:x['risposta'] for x in s.ex['quesiti']}; s.q=q
        s.P=mid_ll(q[4]); s.Q=mid_ll(q[5]); s.pl=geo.Plane(*s.P)
        s.pts=[(s.P,'A · '+A,'lm'),(s.Q,'B · '+B,'lm')]; s.lines=[]; s.fix_below=False
        s.d=geo.dist(s.pl.xy(*s.P),s.pl.xy(*s.Q))
class Area:
    def __init__(s,pts):
        la=sum(p[0] for p,_ in pts)/len(pts); lo=sum(p[1] for p,_ in pts)/len(pts)
        s.pl=geo.Plane(la,lo); s.pts=[(p,t,'lm') for p,t in pts]; s.lines=[]; s.fix_below=False
def pretty(u):
    r=u.replace('’','').replace("'",'').replace(' ','')
    m=_re.findall(r'(\d+)°\((\d+\.?\d*)÷(\d+\.?\d*)\)',r)
    if len(m)==2:
        (g1,a1,b1),(g2,a2,b2)=m; f=lambda x: x.replace('.',',')
        return f'{g1}°{f(a1)}′÷{f(b1)}′ N<br>{g2}°{f(a2)}′÷{f(b2)}′ E'
    return u.replace('.',',').replace('lt,','litri').replace(' n',' nodi')
def fmt(v,n=1): return f'{v:.{n}f}'.replace('.',',')
def hhmm(h): h=h%24; H=int(h); M=int(round((h-H)*60)); H,M=(H+1,0) if M==60 else (H,M); return f'{H:02d}:{M:02d}'
def e12_slides(sid,id_,A,B,t0,V=None,t1=None,cons=10,col=SEA,eb=None,tnote=None,snote=''):
    S=Ex12(id_,A,B); ex=S.ex
    testo=' '.join(l for l in ex['testo'].split('\n') if not l.upper().startswith('SETTORE'))
    testo=_re.split(r'determinare',testo)[0].strip().rstrip(',')+', determinare i 5 quesiti.'
    sett=ex['testo'].split('\n')[0].title()
    lst=''.join(f'<li><b>{x["n"]}</b> · {x["etichetta"].replace("distanza / var.","distanza").replace("ora o velocità","ora di arrivo" if V else "velocità")}</li>' for x in ex['quesiti'])
    left=f'<div style="display:flex; flex-direction:column; gap:20px; width:700px">{p(testo,28,INK,500,1.42)}<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{col}; padding:6px 18px; border-radius:24px; width:max-content">{sett} · carta 5/D</p><ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px">{lst}</ul></div>'
    eb=eb or f'Esercizio {id_} · carteggio entro 12 miglia'
    sec(sid+'_t', head(eb,'La traccia',col)+left, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell&#39;esercizio {id_} con il punto di partenza e quello di arrivo'),
        notes=tnote or f'Esercizio ufficiale {id_} dell\'elenco 4.1.1 (DD 131/2022). In aula: gli allievi lo risolvono da soli sulla carta 5/D, poi si corregge con la slide successiva.')
    d=S.d
    if V:
        t=d/V; r2=('Ora di arrivo',f't = d ÷ V = {fmt(d)} ÷ {fmt(V)} = {fmt(t*60,0)} minuti; {t0} + {fmt(t*60,0)}′',hhmm(int(t0[:2])+int(t0[3:])/60+t))
    else:
        t=t1; Vv=d/t; r2=('Velocità',f'V = d ÷ t = {fmt(d)} ÷ {fmt(t,1)} h',f'{fmt(Vv)} nodi')
    fuel=cons*t*1.3
    lat=lambda ll: f'{geo.lat_s(ll[0])}<br>{geo.lon_s(ll[1])}'
    rows=[('1','Distanza','compasso sui due punti, poi sulla scala delle latitudini: 1′ = 1 miglio',f'{fmt(d)} M',S.q[1]),
          ('2',r2[0],r2[1],r2[2],S.q[2]),
          ('3','Carburante',f'{cons} l/h × {fmt(t,2)} h = {fmt(cons*t)} l, + 30% di riserva',f'{fmt(fuel)} litri',S.q[3]),
          ('4','Partenza','squadretta: latitudine sul bordo verticale, longitudine su quello orizzontale',lat(S.P),S.q[4]),
          ('5','Arrivo','come per la partenza',lat(S.Q),S.q[5])]
    tb='<table style="font-size:24px; color:#34465E"><tr><th style="width:5%">Q</th><th style="width:43%">Come</th><th style="width:24%">Risultato</th><th style="width:28%">Forchetta ufficiale</th></tr>'+''.join(f'<tr><td><b>{n}</b></td><td><b>{t_}</b>: {c}</td><td><b>{r}</b></td><td>{pretty(u)}</td></tr>' for n,t_,c,r,u in rows)+'</table>'
    S.lines=[(S.P,S.Q,'rotta',f'{fmt(d)} M')]
    sec(sid+'_s', head(eb.replace('· carteggio entro 12 miglia','· soluzione'),'I 5 quesiti risolti',col)+f'<div style="width:920px">{tb}</div>', pinned=chart_html(S,1080,290,712,620,True,f'Carta con la rotta dell&#39;esercizio {id_} da A a B e la distanza'),
        notes=f'Soluzione dell\'esercizio {id_}. Le coordinate e la distanza sono ricavate dal centro delle forchette ufficiali; all\'esame basta stare dentro la forchetta. Il carburante comprende il 30% di riserva, come nelle risposte ufficiali. {snote}')

# ============ LA PROVA ============
fmt_cards=[('1 esercizio','dall&#39;elenco ufficiale 4.1.1: 50 esercizi sulla carta 5/D, in tre settori',CORAL,CORAL_T),
           ('5 quesiti','distanza · ora di arrivo o velocità · carburante · coordinate di partenza · coordinate di arrivo',SEA,SEA_T),
           ('20 minuti','almeno 4 risposte giuste su 5, dentro la forchetta indicata dal Ministero',PURPLE,LILAC_T),
           ('Niente bussola','nessun rilevamento, deviazione o corrente: quelli sono per l&#39;oltre 12 miglia',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in fmt_cards)
sec('provaentro', head('Carteggio · entro 12 miglia','La prova di carteggio')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:22px">{tiles}</div>'+note('Porta: carta 5/D integra, due squadrette, compasso a punte secche, matita morbida, gomma, calcolatrice.',CORAL,36),
 notes='DM 323/2021, art. 6: per la patente entro 12 miglia la prova di carteggio è un quiz di elementi di carteggio con 5 quesiti a risposta singola su un esercizio dell\'elenco 4.1.1 del DD 131/2022; 20 minuti, superata con almeno 4 risposte giuste. È la prima prova dell\'esame ed è propedeutica ai quiz. Gli strumenti sono quelli della lezione 3.')

# ============ LA CARTA 5/D E I SETTORI ============
AR=Area([(geo.lm('Faro dello Scoglietto'),'Elba nord'),(geo.lm("Faro dell'Isola di Pianosa"),'Pianosa'),(geo.lm('Fanali del porto del Giglio'),'Giglio'),(geo.lm('Faro di Talamone'),'Talamone'),(geo.lm('Formica Piccola'),'Formiche')])
SETT=[('Nord Ovest orizzontale','16 esercizi, dal 4.1.1-1 al -16','Elba: tra i capi della costa nord (S. Andrea, Enfola, Scoglietto) e la costa sud (Fetovaia, Marina di Campo, Corbelli, Poro).',CORAL),
      ('Nord Ovest verticale','16 esercizi, dal -17 al -32','Tra Pianosa (Marchese, Grottone, Forano) e la costa ovest e nord dell&#39;Elba.',PURPLE),
      ('Sud Est','18 esercizi, dal -33 al -50','Giglio, Argentario (Lividonia, Torre Ciana, Capo d&#39;Uomo), Talamone e le Formiche di Grosseto.',SEA)]
sc=''.join(f'<div style="display:flex; flex-direction:column; gap:4px; border-left:10px solid {c}; padding-left:18px">{p(t,28,c,900,1.2)}{p(n,24,INK,800,1.2)}{p(d,24,BODY,400,1.35)}</div>' for t,n,d,c in SETT)
sec('carta5d', head('Carteggio · entro 12 miglia','La carta 5/D e i tre settori')+col(sc,640,26), pinned=chart_html(AR,880,290,912,620,False,'Carta della zona tra Elba, Pianosa, Giglio, Argentario e Formiche di Grosseto'),
 notes='La carta 5/D (dall\'Isola d\'Elba a Civitavecchia) è la stessa dell\'oltre 12 miglia. Gli esercizi 4.1.1 sono divisi in tre settori: Nord Ovest orizzontale (esercizi 1-16, Elba nord e sud), Nord Ovest verticale (17-32, Elba ovest e Pianosa), Sud Est (33-50, Giglio, Argentario, Talamone, Formiche). Il numero del settore in testa alla traccia dice dove guardare sulla carta. All\'esame la carta si porta integra: nessun segno o appunto.')

# ============ COORDINATE ============
def frame(x0,y0,x1,y1): return f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{CHARTBG}" stroke="{NAVY}" stroke-width="3"/>'
def vscale(x,y0,y1,pxm,n0,step=1):
    g=''; k=0; y=y1
    while y-pxm>=y0-0.1:
        g+=f'<rect x="{x}" y="{y-pxm:.1f}" width="26" height="{pxm:.1f}" fill="{NAVY if k%2==0 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="1.5"/>'
        for j in range(1,10): g+=line(x+26,y-pxm*j/10,x+(36 if j==5 else 32),y-pxm*j/10,NAVY,1.5)
        g+=f'<text x="{x-8}" y="{y-pxm+7:.1f}" text-anchor="end" font-family="Arial" font-size="20" font-weight="700" fill="{SOFT}">{n0+k+1}′</text>'
        y-=pxm; k+=1
    return g
def hscale(y,x0,x1,pxm,n0):
    g=''; k=0; x=x0
    while x+pxm<=x1+0.1:
        g+=f'<rect x="{x:.1f}" y="{y}" width="{pxm:.1f}" height="26" fill="{NAVY if k%2==0 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="1.5"/>'
        for j in range(1,10): g+=line(x+pxm*j/10,y,x+pxm*j/10,y-(10 if j==5 else 6),NAVY,1.5)
        g+=f'<text x="{x+pxm:.1f}" y="{y+50}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="700" fill="{SOFT}">{n0+k+1:02d}′</text>'
        x+=pxm; k+=1
    return g
def setsq(x,y,s,rot,c):
    return f'<g transform="translate({x} {y}) rotate({rot})"><path d="M0 0 L{s} 0 L0 {-s*0.62:.0f} Z" fill="{c}" fill-opacity="0.22" stroke="{c}" stroke-width="3"/><path d="M{s*0.18:.0f} {-s*0.1:.0f} L{s*0.4:.0f} {-s*0.1:.0f} L{s*0.18:.0f} {-s*0.24:.0f} Z" fill="{CHARTBG}" stroke="{c}" stroke-width="2"/></g>'
b=frame(120,20,1072,520)
b+=f'<path d="M150 20 Q260 80 360 60 Q470 40 540 110 Q610 170 720 120 Q800 80 900 20 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=vscale(94,20,520,100,46)+hscale(520,120,1072,136,5)
PX,PY=120+3.4*136,520-2.5*100
b+=dash(120,PY,PX,PY,CORAL,4)+dash(PX,PY,PX,520,BLUE,4)
b+=setsq(PX-4,PY+2,300,0,CORAL)+setsq(PX+2,PY,240,90,BLUE)
b+=f'<circle cx="{PX:.0f}" cy="{PY:.0f}" r="13" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/><circle cx="{PX:.0f}" cy="{PY:.0f}" r="4" fill="{NAVY}"/>'
lbl=(pill(X+140,Y+PY-60,300,'42°48′,5 N',CORAL,26)+pill(X+PX+14,Y+584,300,'010°08′,4 E',BLUE,26)+pill(X+PX+24,Y+PY-54,160,'P',NAVY,26)
     +lab(X+134,Y+150,300,'latitudine: bordo verticale',CORAL,22,900)+lab(X+700,Y+440,340,'longitudine: bordo orizzontale',BLUE,22,900))
txt=(term('Latitudine','Squadretta sul punto, parallela ai paralleli, fino al bordo destro o sinistro: si legge sulla scala verticale.')
     +term('Longitudine','Seconda squadretta perpendicolare, fino al bordo in alto o in basso: si legge sulla scala orizzontale.')
     +term('Come si scrive','Gradi, primi e decimi di primo: 42°48′,5 N · 010°08′,4 E. Sulla 5/D ogni primo è diviso in 10 parti.'))
sec('coordinate', head('Carteggio · quesiti 4 e 5','Le coordinate di un punto')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Bordo di una carta con la scala delle latitudini a sinistra e quella delle longitudini in basso: due squadrette portano il punto P sui due bordi')+lbl,
 notes='Quesiti 4 e 5 dell\'esercizio: coordinate di partenza e di arrivo. Il punto è il faro o il capo indicato dalla traccia, al centro del suo simbolo. Controlla la direzione in cui crescono i valori: la latitudine cresce verso Nord (in alto), la longitudine Est cresce verso destra (quiz 1.7.1-42). Le forchette ufficiali accettano di solito ±0,3′: 42°48′,5 va bene tra 48′,2 e 48′,8. Errore frequente: leggere un primo in più o in meno perché si parte dal tratto sbagliato della scala; contare sempre dal grado intero.')

# ============ DISTANZA ============
b=frame(90,40,1072,600)
b+=vscale(64,40,600,100,45)
b+=f'<rect x="90" y="8" width="982" height="26" fill="#EAF0F4" stroke="{SOFT}" stroke-width="1.5"/>'+''.join(line(90+k*98,8,90+k*98,34,SOFT,1.5) for k in range(11))
b+=line(460,4,700,40,LRED,6)+line(460,40,700,4,LRED,6)
AX,AY,BX,BY=340,470,770,280
b+=f'<line x1="{AX}" y1="{AY}" x2="{BX}" y2="{BY}" stroke="{NAVY}" stroke-width="4" stroke-dasharray="14 10"/>'
apx,apy=(AX+BX)/2-40,120
b+=f'<path d="M{apx} {apy} L{AX} {AY} M{apx} {apy} L{BX} {BY}" stroke="{SOFT}" stroke-width="7" stroke-linecap="round"/><circle cx="{apx}" cy="{apy}" r="14" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
for x_,y_ in ((AX,AY),(BX,BY)): b+=f'<circle cx="{x_}" cy="{y_}" r="11" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
L_=math.hypot(BX-AX,BY-AY); ym=(AY+BY)/2
b+=f'<path d="M104 {ym-L_/2:.0f} L126 {ym-L_/2:.0f} M115 {ym-L_/2:.0f} L115 {ym+L_/2:.0f} M104 {ym+L_/2:.0f} L126 {ym+L_/2:.0f}" stroke="{CORAL}" stroke-width="6" fill="none"/>'
b+=dash(126,ym,AX-20,ym,CORAL,3)
lbl=(pill(X+140,Y+ym-24,200,f'{fmt(L_/100)} miglia',CORAL,26)+pill(X+AX-40,Y+AY+22,60,'A',NAVY,26)+pill(X+BX+20,Y+BY-20,60,'B',NAVY,26)
     +lab(X+720,Y+44,360,'mai la scala delle longitudini',LRED,22,900))
txt=(term('Apri il compasso','Punte secche sui due punti, A e B, senza cambiare l&#39;apertura.')
     +term('Scala delle latitudini','Porta il compasso sul bordo verticale, all&#39;altezza della rotta: ogni primo è un miglio, ogni decimo un decimo di miglio.')
     +term('Se è troppo lungo','Apri il compasso a 1 o 2 miglia sulla scala e riportalo lungo la rotta contando i passi.'))
sec('distanza', head('Carteggio · quesito 1','La distanza')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Il compasso aperto tra A e B e la stessa apertura riportata sulla scala delle latitudini a sinistra; la scala delle longitudini in alto è barrata')+lbl,
 notes='Quiz 1.7.5-52 (la distanza si misura sulla scala delle latitudini, alla stessa latitudine della zona), 1.7.2-37 (con il compasso aperto pari alla distanza), 1.7.5-53 (4′,4 di latitudine = 4,4 miglia), 1.7.5-32 (in un grado 60 miglia). La scala delle longitudini non va mai usata: sulla carta di Mercatore un primo di longitudine è più corto di un miglio. Le forchette ufficiali sulla distanza sono di solito ±0,3 miglia.')

# ============ TEMPO E VELOCITÀ ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EEF5FB"/>'
b+=f'<path d="M270 80 L480 470 L60 470 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/><path d="M130 340 L410 340 M270 340 L270 470" stroke="{NAVY}" stroke-width="4"/>'
tx8=lambda x,y,t,c,s=64: f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial" font-size="{s}" font-weight="700" fill="{c}">{t}</text>'
b+=tx8(270,300,'d',CORAL)+tx8(190,440,'V',SEA)+tx8(350,440,'t',PURPLE)
cx,cy,r=800,280,190
b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/>'
b+=f'<path d="M{cx} {cy} L{cx} {cy-r} A{r} {r} 0 0 1 {cx+r} {cy} Z" fill="{SEA}" fill-opacity="0.35"/><path d="M{cx} {cy} L{cx+r} {cy} A{r} {r} 0 0 1 {cx} {cy+r} Z" fill="{SEA}" fill-opacity="0.2"/>'
for k in range(12):
    x1,y1=pol(cx,cy,k*30,r-8); x2,y2=pol(cx,cy,k*30,r-(26 if k%3==0 else 16)); b+=line(x1,y1,x2,y2,NAVY,4 if k%3==0 else 2)
b+=line(cx,cy,cx,cy-r+40,NAVY,6)+line(cx,cy,cx,cy+r-50,CORAL,8)+f'<circle cx="{cx}" cy="{cy}" r="10" fill="{NAVY}"/>'
lbl=(lab(X+60,Y+510,440,'copri la lettera che cerchi',INK,24,900,'center')+pill(X+cx+60,Y+cy-110,200,'15′ = 0,25 h',SEA,24)+pill(X+cx+50,Y+cy+60,200,'30′ = 0,5 h',SEA,24)
     +lab(X+cx-190,Y+cy+r+20,380,'minuti = ore decimali × 60',INK,24,900,'center'))
txt=(term('Tre formule, un triangolo','<b>d = V × t</b> · <b>t = d ÷ V</b> · <b>V = d ÷ t</b>. Miglia, nodi e ore.')
     +term('Ora di arrivo','t = 5,5 M ÷ 5,5 nodi = 1 h: partenza 09:00, arrivo 10:00.')
     +term('Velocità','3,2 M in 30 minuti: V = 3,2 ÷ 0,5 = 6,4 nodi.'))
sec('tempo', head('Carteggio · quesito 2','Ora di arrivo o velocità')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Il triangolo con d in alto e V e t in basso, e un orologio con il quarto d&#39;ora e la mezz&#39;ora evidenziati')+lbl,
 notes='Quiz 1.7.5-15, -16, -17 (V = S/T, S = V·T, T = S/V), -14 e -51 (il nodo è un miglio all\'ora), -24 (12 miglia in 2 ore: 6 nodi), -61 (9 nodi per 20 minuti: 3 miglia), -43 e -69 (miglia percorse in una frazione d\'ora). Conversioni: 6 minuti = 0,1 h, 12′ = 0,2 h, 20′ = 0,33 h, 40′ = 0,67 h, 45′ = 0,75 h. Mai sommare ore e minuti come decimali: 1,5 h sono 1 ora e 30 minuti, non 1 ora e 50. La forchetta sull\'ora è di solito ±3 minuti, sulla velocità ±0,6 nodi.')

# ============ CARBURANTE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F2FAF4"/>'
b+=f'<path d="M140 150 L300 150 L330 190 L330 520 L110 520 L110 190 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="5"/><rect x="170" y="110" width="60" height="44" rx="8" fill="{NAVY}"/><path d="M250 130 L300 130" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/><path d="M150 240 L290 470 M290 240 L150 470" stroke="#FFFFFF" stroke-width="8" stroke-opacity="0.5"/>'
bx,base=520,520; hb=300; hr=90
b+=f'<rect x="{bx}" y="{base-hb}" width="160" height="{hb}" rx="10" fill="{GREEN}"/><rect x="{bx}" y="{base-hb-hr}" width="160" height="{hr}" rx="10" fill="{SUN}"/>'
b+=f'<rect x="{bx+260}" y="{base-hb-hr}" width="160" height="{hb+hr}" rx="10" fill="{SEA}"/>'
b+=line(480,base,1060,base,NAVY,4)
lbl=(lab(X+bx,Y+base-hb/2-18,160,'10 l',  '#FFFFFF',34,900,'center')+lab(X+bx,Y+base-hb-hr/2-18,160,'+3 l','#16324F',30,900,'center')
     +lab(X+bx+260,Y+base-(hb+hr)/2-20,160,'13 l','#FFFFFF',40,900,'center')
     +lab(X+bx-20,Y+base+14,200,'consumo 1 h',GREEN,22,900,'center')+lab(X+bx-20,Y+base-hb-hr-40,200,'riserva 30%',SUN,22,900,'center')+lab(X+bx+240,Y+base+14,200,'da imbarcare',SEA,22,900,'center'))
txt=(term('La formula','<b>litri = consumo orario × ore di moto × 1,3</b>: il 30% in più è la riserva, come nelle risposte ufficiali.')
     +term('Le ore giuste','Sono quelle del quesito 2: t = d ÷ V, oppure il tempo dato dalla traccia (mezz&#39;ora, un&#39;ora).')
     +term('Esempi','10 l/h per 30 minuti: 5 l, con riserva 6,5 l. 15 l/h per 1 ora: 15 l, con riserva 19,5 l.'))
sec('carburante', head('Carteggio · quesito 3','Il carburante da imbarcare')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Una tanica e due colonne: 10 litri di consumo più 3 litri di riserva fanno 13 litri da imbarcare')+lbl,
 notes='Le risposte ufficiali del 4.1.1 comprendono sempre il 30% di riserva: per esempio esercizio 4.1.1-6, mezz\'ora a 10 l/h = 5 litri, risposta 6,5 litri; esercizio 4.1.1-24, un\'ora a 10 l/h, risposta 13 litri. Quando la traccia dà la velocità, il tempo è quello calcolato al quesito 2: un errore sulla distanza si porta dietro ora e carburante, per questo la distanza va misurata con cura. Attenzione al consumo: non è sempre 10 l/h (esercizio 4.1.1-19: 15 l/h).')

quiz_slide('quiz1','Quiz 1 · Coordinate e distanze',['1.7.1-42', '1.7.5-52'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.7.1-42', '1.7.5-52'],True)
quiz_slide('quiz2','Quiz 2 · Tempo e velocità',['1.7.5-43', '1.7.5-69'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.7.5-43', '1.7.5-69'],True)

# ============ IL METODO ============
M5=[(1,'Leggi e segna','Settore, partenza, arrivo, velocità o orari, consumo. Cerchia i due punti sulla carta.',NAVY),
    (2,'Coordinate','Quesiti 4 e 5 subito: sono indipendenti dagli altri.',BLUE),
    (3,'Distanza','Compasso sui punti, poi sulla <b>scala delle latitudini</b>: 1′ = 1 miglio.',SEA),
    (4,'Ora o velocità','<b>t = d ÷ V</b>, ora di arrivo = partenza + t. Oppure <b>V = d ÷ t</b>.',CORAL),
    (5,'Carburante','<b>consumo × ore × 1,3</b>. Poi ricontrolla i numeri con la calcolatrice.',PURPLE)]
rows=''.join(f'<div style="display:flex; gap:18px; align-items:start"><p style="flex:none; width:56px; font-family:{H}; font-size:32px; font-weight:700; line-height:56px; text-align:center; color:#FFFFFF; background:{c}; border-radius:28px">{n}</p><div style="display:flex; flex-direction:column; gap:4px">{h3(t,30,c)}{p(d,26,BODY,400,1.35)}</div></div>' for n,t,d,c in M5)
cheat=card(tag('Il tempo in 20 minuti',GREEN)+'<ul style="font-size:26px; line-height:1.45; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>2′ lettura e punti</li><li>6′ coordinate</li><li>4′ distanza</li><li>4′ ora o velocità e carburante</li><li>4′ controllo finale</li></ul>',GREEN_T,32,12,0.8)
sec('metodo12', head('Carteggio · entro 12 miglia','Il metodo in cinque passi')+f'<div style="display:flex; gap:32px"><div style="flex:1.3; display:flex; flex-direction:column; gap:20px">{rows}</div>{cheat}</div>',
 notes='L\'ordine consigliato parte dalle coordinate perché non dipendono da nessun calcolo: sono due risposte su cinque, e con la distanza fanno già tre. Ora e carburante dipendono dalla distanza: un errore lì ne produce tre. Le forchette ufficiali accettano di solito ±0,3 miglia sulla distanza, ±3 minuti sull\'ora, ±0,3′ sulle coordinate e qualche decimo di litro sul carburante.')

# ============ ERRORI TIPICI ============
ERR=[('Scala sbagliata','La distanza sulla scala delle longitudini: sempre troppo corta.',CORAL,CORAL_T),
     ('Primi e decimi','42°48′,5 non è 42°48′50″: il decimo è un decimo di primo.',BLUE,BLUE_T),
     ('Ore e minuti','0,75 h sono 45 minuti, non 75. Converti prima di sommare all&#39;ora di partenza.',PURPLE,LILAC_T),
     ('Riserva dimenticata','Senza il 30% il carburante esce dalla forchetta.',SUN,'#FFF0C9'),
     ('Punto sbagliato','Il faro, non il porto; il capo, non il paese. Centro del simbolo.',SEA,SEA_T),
     ('Grado sbagliato','Conta i primi dal grado intero, non dal tratto più vicino.',GREEN,GREEN_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:26px; border-radius:26px">{h3(t,32,c)}{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in ERR)
sec('errori', head('Carteggio · entro 12 miglia','Gli errori che costano il quesito')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:22px">{tiles}</div>'+note('Un errore sulla distanza ne porta con sé altri due: ora e carburante.',CORAL,36),
 notes='Gli errori più frequenti nelle correzioni. Il più grave è la scala: sulla carta di Mercatore un primo di longitudine è più corto di un miglio (a 42° circa 0,74 miglia), quindi chi misura in basso trova distanze troppo corte. Secondo: confondere i decimi di primo con i secondi. Terzo: le ore decimali. Per esercitarsi: tutti i 50 esercizi dell\'elenco 4.1.1 e le 10 prove simulate dell\'appendice D, parte 1.')

# ============ ESERCIZI ============
e12_slides('e1','4.1.1 - 1','Capo S. Andrea','Capo d&#39;Enfola','09:00',V=5.5,col=SEA,snote='Settore Nord Ovest orizzontale; velocità data, si cerca l\'ora di arrivo.')
e12_slides('e2','4.1.1 - 19','Punta del Marchese','Punta della Testa','10:00',V=8.1,cons=15,col=PURPLE,snote='Settore Nord Ovest verticale, da Pianosa all\'Elba. Attenzione al consumo di 15 l/h.')
e12_slides('e3','4.1.1 - 35','Talamone','Formica Piccola','08:00',t1=1.0,col=CORAL,snote='Settore Sud Est; è dato l\'orario di arrivo: il tempo è 1 ora e si cerca la velocità.')
e12_slides('e4','4.1.1 - 6','Marciana Marina','Capo d&#39;Enfola','10:00',t1=0.5,col=BLUE,snote='Mezz\'ora di navigazione: V = d ÷ 0,5, cioè la distanza per due; carburante 10 × 0,5 = 5 litri, più il 30%: 6,5 litri, come la risposta ufficiale.')
e12_slides('sim','4.1.1 - 40','Giglio Porto','Punta Lividonia','10:00',V=4.8,col=GREEN,eb='Prova simulata · 20 minuti · carteggio entro 12 miglia',
 tnote='Prova simulata come all\'esame: cronometro a 20 minuti, carta 5/D, squadrette, compasso e calcolatrice. Si risponde ai 5 quesiti su un foglio; superata con almeno 4 risposte dentro la forchetta. Esercizio 4.1.1-40, settore Sud Est.',
 snote='Più di 2 ore di moto: 9,6 ÷ 4,8 = 2 ore, arrivo alle 12:00; carburante 10 × 2 × 1,3 = 26 litri.')

exec(open('apertura.py').read())
chapter('cap1',1,'La prova e la carta 5/D',['La prova di carteggio','La carta 5/D e i tre settori'],CORAL,
 'Circa 10 minuti: solo l\'essenziale sulla prova e sulla carta.','circa 10 minuti · 2 argomenti',1,art=(chart_scene(),'Illustrazione: carta nautica con rotta e rosa dei venti e un faro acceso'))
chapter('cap2',2,'Coordinate, distanza, tempo e carburante',['Le coordinate di un punto','La distanza','Ora di arrivo o velocità','Il carburante da imbarcare'],SEA,
 'Circa 20 minuti, comprese due verifiche da 2 quiz.','circa 20 minuti · 4 argomenti',1,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata e una rotta tratteggiata'))
chapter('cap3',3,'Il metodo e gli esercizi',['Il metodo in cinque passi','Gli errori che costano il quesito','Esercizio 1: velocità data','Esercizio 2: velocità data','Esercizio 3: orario di arrivo','Esercizio 4: mezz\'ora di moto','Prova simulata a tempo'],PURPLE,
 'Circa 45 minuti: metodo, quattro esercizi ufficiali e la prova simulata. Se il tempo stringe, lasciare per casa uno dei quattro esercizi.','circa 45 minuti · 7 argomenti',1)
QZ=[('q01','Quiz 1 · Le coordinate',['1.7.1-1','1.7.1-15','1.7.1-30']),('q02','Quiz 2 · Meridiani e paralleli',['1.7.1-3','1.7.1-16','1.7.1-32']),
 ('q03','Quiz 3 · Miglio e nodo',['1.7.5-14','1.7.5-42','1.7.5-20']),('q04','Quiz 4 · La carta di Mercatore',['1.7.2-4','1.7.2-20','1.7.2-32']),
 ('q05','Quiz 5 · La scala delle carte',['1.7.2-5','1.7.2-22','1.7.2-35']),('q06','Quiz 6 · Fondali e simboli',['1.7.2-8','1.7.2-29','1.7.2-24']),
 ('q07','Quiz 7 · Spazio percorso',['1.7.5-16','1.7.5-41','1.7.5-47']),('q08','Quiz 8 · Tempo e velocità',['1.7.5-58','1.7.5-63','1.7.5-65']),
 ('q09','Quiz 9 · Le formule',['1.7.5-60','1.7.5-15','1.7.5-35']),('q10','Quiz 10 · Navigazione stimata',['1.7.5-2','1.7.5-7','1.7.5-17']),
 ('q11','Quiz 11 · Rotta e prora',['1.7.7-2','1.7.7-8','1.7.7-18']),('q12','Quiz 12 · La bussola',['1.7.4-14','1.7.4-27','1.7.4-35'])]
raccolta(8,4,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Minuti in decimi','Trasforma i minuti in ore e decimi prima di applicare S = V × T: 15 minuti sono 0,25 ore.'),
  ('Latitudine per le miglia','Un primo di latitudine è un miglio: le distanze si misurano sulla scala laterale.'),
  ('Attento ai numeri','Ore, minuti, miglia, nodi: controlla il numero e l\'unità prima di scegliere.')],
 ['Quiz 1-6 · coordinate, miglio e carte (18)','Quiz 7-10 · spazio, velocità, tempo (12)','Quiz 11-12 · rotta, prora e bussola (6)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. I quiz di calcolo si risolvono alla lavagna con S = V × T. Se il tempo stringe, lasciare per casa le slide 2 e 10.',esame=['navigazione'])
closing(['Coordinate: squadretta sul punto, latitudine sul bordo verticale, longitudine su quello orizzontale','Distanza: compasso e scala delle latitudini, 1′ = 1 miglio','t = d ÷ V, V = d ÷ t: converti i minuti prima di sommarli','Carburante: consumo × ore × 1,3','20 minuti, 4 risposte su 5: coordinate prima, poi distanza, ora e carburante'],
 'Prossima lezione · 09 · Vela (patente a vela) · per il motore entro 12 miglia: l\'esame','A casa: i 50 esercizi dell\'elenco 4.1.1 e le 10 prove entro 12 miglia dell\'appendice D, parte 1.')
write_deck(OUT,'Lezione 08 · Quiz ed esercizi di carteggio di navigazione entro le 12 miglia',
 ['cover','agenda','cap1','provaentro','carta5d','cap2','coordinate','distanza','quiz1','quiz1r','tempo','carburante','quiz2','quiz2r','cap3','metodo12','errori',
  'e1_t','e1_s','e2_t','e2_s','e3_t','e3_s','e4_t','e4_s','sim_t','sim_s','capquiz','quiz']+[q+s for q,_,_ in QZ for s in ('','r')]+['chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"La prova e la carta 5/D","start":"cap1"},
  "s3":{"description":"Coordinate, distanza, tempo e velocità, carburante","start":"cap2"},"s4":{"description":"Il metodo, gli errori tipici, quattro esercizi ufficiali e la prova simulata","start":"cap3"},
  "s5":{"description":"Raccolta quiz","start":"capquiz"}})
