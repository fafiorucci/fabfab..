import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
from lezione_base import *
import lezione_base as LB
import geo, chart, es10
OUT=SP+'/lez10/project'
GREY='#97A6B4'; LRED='#E23B3B'; ORANGE='#F28C28'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Il kit del carteggio costiero':'dividers','Stesso punto, due rilevamenti':'lighthouse','Due punti, due ore diverse':'lighthouse',
 'Tre rilevamenti':'lighthouse','Passare al traverso':'compass','Intercettare una barca':'compass','La tabella di deviazione':'grid','I punti cospicui della carta 5/D':'map'})
def pcol(inner,w=532,gap=20,left=1260,top=290): return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def pol(cx,cy,b,r): return (cx+r*math.sin(math.radians(b)), cy-r*math.cos(math.radians(b)))
X,Y,W,Hh=700,290,1092,620

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
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px; white-space:nowrap">{t}</p>'
    return svg+html

# ============ COVER + AGENDA ============
cover(10,'Carteggio: navigazione costiera','Fare il punto nave con i rilevamenti, passare al traverso e intercettare: i 26 esercizi ufficiali della carta 5/D',
 'Lezione 10, la prima di carteggio. Esercizi ufficiali 5.1.3, 5.2.3, 5.3.3 e 5.4.3 dell\'Allegato A al DD 131/2022 (carta 5/D, settori A-D). All\'esame 4 esercizi indipendenti in 60 minuti, almeno 3 giusti. Le carte di questa lezione sono ridisegnate da dati OpenStreetMap per spiegare il tracciamento: all\'esame si lavora sulla carta 5/D dell\'IIM.')
blocks=[('0:00','25′','Il kit e le cinque tecniche',CORAL),('0:25','25′','Settore A · Elba (6 esercizi)',SEA),('0:50','20′','Settore B · Castiglione e Punta Ala (5)',PURPLE),('1:10','25′','Settore C · Pianosa (7)',BLUE),('1:35','25′','Settore D · Giglio e Argentario (8)',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">3 su 4</p>'+p('esercizi giusti in 60 minuti',26,INK,700)+p('Il risultato va dato entro la forchetta ufficiale: di solito ±0,3′ in latitudine e longitudine.',24))
left=card(tag('Cosa porti al tavolo',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>carta 5/D integra</li><li>squadrette nautiche e compasso a punte secche</li><li>matita morbida e gomma</li><li>calcolatrice non programmabile</li><li>la tabella di deviazione, se la traccia la cita</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 10 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='In aula si svolgono alla lavagna un esercizio per tecnica e gli altri si danno come lavoro a coppie; le slide della soluzione servono per la correzione e per il ripasso a casa. Per ogni esercizio: una slide con la traccia (e la carta senza soluzione) e una con il tracciamento.')

# ============ KIT ============
K=[('V = d + δ','Variazione: declinazione più deviazione, con il segno (Est +, Ovest −).',CORAL,CORAL_T),
   ('Rilv = Rilb + V','Da bussola a vero; per la prora: Pv = Pb + V. All\'indietro: Pb = Pv − V.',SEA,SEA_T),
   ('Rilv = Pv + ρ','Rilevamento polare: ρ è negativo a sinistra, positivo a dritta.',PURPLE,LILAC_T),
   ('d + anni × variazione','La declinazione della carta va portata all\'anno della traccia.',BLUE,BLUE_T),
   ('m = V × t','Miglia = nodi × ore. 20 minuti sono 1/3 d\'ora, 18 minuti 0,3.',GREEN,GREEN_T),
   ('Senza vento né corrente','Rv = Pv e Ve = Vp: la barca va dove punta la prora.',ORANGE,SUN_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:28px; border-radius:28px"><p style="font-family:{H}; font-size:44px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in K)
sec('kit', head('Carteggio · prima di tracciare','Il kit del carteggio costiero')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:22px">{tiles}</div>',
 notes='Tutte le conversioni degli esercizi di oggi. Esempi: 5.1.3-2 (d −2°, δ −2°: V −4°), 5.2.3-4 (declinazione 2016 1°30′E più 5 anni × 6′ = 2°00′E), 5.3.3-4 e 5.3.3-6 (rilevamenti polari), 5.3.3-2 e 5.3.3-3 (tabella di deviazione: si entra con la prora magnetica Pm = Pv − d). Richiami: bussola e conversioni nella lezione 4, rilevamenti nella lezione 5.')

# ============ TECNICHE (schemi) ============
def tech_svg(kind):
    b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/>'
    Lx,Ly=820,120
    b+=f'<path d="M760 0 Q850 60 900 150 Q960 220 1092 240 L1092 0 Z" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/>'
    b+=f'<circle cx="{Lx}" cy="{Ly}" r="13" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    if kind=='stesso':
        P1=(250,520); run=(230,-150); P2=(P1[0]+run[0],P1[1]+run[1]); Q=(Lx+run[0],Ly+run[1])
        b+=line(P1[0]-40,P1[1]+22,Lx,Ly,NAVY,3)+line(P2[0]-60,P2[1]+70,Lx,Ly,CORAL,4)
        b+=dash(Lx,Ly,Q[0],Q[1],GREY,2)+arrow(Lx,Ly,Q[0],Q[1],GREY,2,12)
        dx,dy=Lx-P1[0],Ly-P1[1]; b+=f'<line x1="{Q[0]-dx*1.15:.0f}" y1="{Q[1]-dy*1.15:.0f}" x2="{Q[0]+dx*0.1:.0f}" y2="{Q[1]+dy*0.1:.0f}" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="14 9"/>'
        b+=arrow(P1[0],P1[1],P2[0],P2[1],GREEN,6,20)+f'<circle cx="{P2[0]}" cy="{P2[1]}" r="16" fill="none" stroke="{CORAL}" stroke-width="5"/>'+f'<circle cx="{P1[0]}" cy="{P1[1]}" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
        L=[(P1[0]-120,P1[1]+10,'ore 1',INK),(Lx-260,Ly-50,'faro',NAVY),(330,470,'cammino: Pv, V × t',GREEN),(Q[0]-420,Q[1]+120,'primo rilevamento trasportato',PURPLE),(P2[0]+26,P2[1]-40,'punto nave, ore 2',CORAL)]
    elif kind=='diversi':
        L2=(980,380); b+=f'<path d="M1092 300 Q1000 330 960 400 Q940 480 1092 520 Z" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/><circle cx="{L2[0]}" cy="{L2[1]}" r="13" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
        P1=(250,520); run=(280,-120); P2=(P1[0]+run[0],P1[1]+run[1]); Q=(Lx+run[0],Ly+run[1])
        b+=line(P1[0]-40,P1[1]+22,Lx,Ly,NAVY,3)+line(P2[0]-80,P2[1]+10,L2[0],L2[1],CORAL,4)
        dx,dy=Lx-P1[0],Ly-P1[1]; b+=f'<line x1="{Q[0]-dx*1.1:.0f}" y1="{Q[1]-dy*1.1:.0f}" x2="{Q[0]+dx*0.05:.0f}" y2="{Q[1]+dy*0.05:.0f}" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="14 9"/>'
        b+=dash(Lx,Ly,Q[0],Q[1],GREY,2)+arrow(P1[0],P1[1],P2[0],P2[1],GREEN,6,20)+f'<circle cx="{P2[0]}" cy="{P2[1]}" r="16" fill="none" stroke="{CORAL}" stroke-width="5"/><circle cx="{P1[0]}" cy="{P1[1]}" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
        L=[(P1[0]-120,P1[1]+10,'ore 1',INK),(Lx+26,Ly+14,'punto 1',NAVY),(L2[0]-160,L2[1]+30,'punto 2',CORAL),(330,500,'cammino',GREEN),(Q[0]-470,Q[1]+60,'rilevamento 1 trasportato',PURPLE),(P2[0]-40,P2[1]-70,'punto nave',CORAL)]
    elif kind=='tre':
        P=[(160,540),(380,400),(620,250)]
        for i,(q,c) in enumerate(zip(P,(NAVY,PURPLE,CORAL))):
            b+=line(q[0]-50*(i+1)*0.4,q[1]+30,Lx,Ly,c,3 if i<2 else 4)
        b+=arrow(P[0][0],P[0][1],P[2][0],P[2][1],GREEN,6,20)+''.join(f'<circle cx="{q[0]}" cy="{q[1]}" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>' for q in P[:2])+f'<circle cx="{P[2][0]}" cy="{P[2][1]}" r="16" fill="none" stroke="{CORAL}" stroke-width="5"/>'
        L=[(P[0][0]-60,P[0][1]+20,'ore 1',INK),(P[1][0]-120,P[1][1]+10,'ore 2',INK),(P[2][0]-190,P[2][1]-60,'ore 3: punto nave',CORAL),(Lx-240,Ly-50,'faro',NAVY)]
    elif kind=='traverso':
        L0=(700,330); R=150; A=(150,80)
        b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/><circle cx="{L0[0]}" cy="{L0[1]}" r="{R}" fill="none" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="10 8"/><circle cx="{L0[0]}" cy="{L0[1]}" r="18" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/><circle cx="{L0[0]}" cy="{L0[1]}" r="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
        dx,dy=L0[0]-A[0],L0[1]-A[1]; d=math.hypot(dx,dy); a=math.asin(R/d); th=math.atan2(dy,dx)+a
        T=(L0[0]+R*math.sin(th),L0[1]-R*math.cos(th))
        e=(A[0]+math.cos(th)*820,A[1]+math.sin(th)*820)
        b+=arrow(A[0],A[1],e[0],e[1],GREEN,6,22)+line(L0[0],L0[1],T[0],T[1],CORAL,4)+f'<circle cx="{A[0]}" cy="{A[1]}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="{T[0]:.0f}" cy="{T[1]:.0f}" r="12" fill="none" stroke="{CORAL}" stroke-width="5"/>'
        L=[(A[0]-60,A[1]-60,'A',INK),(T[0]+24,T[1]-20,'C: al traverso',CORAL),(L0[0]+40,L0[1]+R+14,'cerchio del raggio dato',PURPLE),(L0[0]+30,L0[1]-30,'faro a dritta',NAVY)]
    else:  # intercetta
        A=(180,480); B=(820,160); cb=225; vb=150; va=300
        ub=(math.sin(math.radians(cb)),-math.cos(math.radians(cb)))
        T=(A[0]+ub[0]*vb,A[1]+ub[1]*vb)
        ab=((B[0]-A[0]),(B[1]-A[1])); n=math.hypot(*ab); ab=(ab[0]/n,ab[1]/n)
        # V = T + k ab with |V-A|=va
        wx,wy=T[0]-A[0],T[1]-A[1]; bb=2*(wx*ab[0]+wy*ab[1]); cc=wx*wx+wy*wy-va*va; k=(-bb+math.sqrt(bb*bb-4*cc))/2
        V=(T[0]+k*ab[0],T[1]+k*ab[1]); dv=((V[0]-A[0])/va,(V[1]-A[1])/va)
        # intersezione rotta A dv con rotta B ub
        det=dv[0]*(-ub[1])-dv[1]*(-ub[0]); s=((B[0]-A[0])*(-ub[1])-(B[1]-A[1])*(-ub[0]))/det; Dp=(A[0]+dv[0]*s,A[1]+dv[1]*s)
        b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/>'
        b+=dash(A[0],A[1],B[0],B[1],GREY,2)+arrow(B[0],B[1],Dp[0],Dp[1],ORANGE,4,16)+arrow(A[0],A[1],T[0],T[1],ORANGE,5,16)+dash(T[0],T[1],V[0]+ab[0]*60,V[1]+ab[1]*60,PURPLE,3)
        b+=arrow(A[0],A[1],Dp[0],Dp[1],GREEN,6,22)+f'<circle cx="{A[0]}" cy="{A[1]}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="{B[0]}" cy="{B[1]}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="{Dp[0]:.0f}" cy="{Dp[1]:.0f}" r="16" fill="none" stroke="{CORAL}" stroke-width="5"/>'
        b+=f'<path d="M{A[0]+va*math.cos(math.atan2(dv[1],dv[0])-0.25):.0f} {A[1]+va*math.sin(math.atan2(dv[1],dv[0])-0.25):.0f} A{va} {va} 0 0 1 {A[0]+va*math.cos(math.atan2(dv[1],dv[0])+0.25):.0f} {A[1]+va*math.sin(math.atan2(dv[1],dv[0])+0.25):.0f}" fill="none" stroke="{GREEN}" stroke-width="3" stroke-dasharray="6 6"/>'
        L=[(A[0]-60,A[1]+14,'A',INK),(B[0]+16,B[1]-40,'B',INK),(T[0]-250,T[1]+4,'sua velocità',ORANGE),(Dp[0]+24,Dp[1]-12,'D: incontro',CORAL),(V[0]+30,V[1]-60,'parallela ad AB',PURPLE),(A[0]+140,A[1]-40,'rotta di intercettazione',GREEN)]
    return b,L
def tech_slide(id_,kind,title,txt,notes,left):
    b,L=tech_svg(kind); x=128 if left else 700
    lbl=''.join(pill(x+lx,Y+ly,420,t,c,22) for lx,ly,t,c in L)
    pinned=svgp(x,Y,W,Hh,b,title)+lbl
    if left: sec(id_,head('Carteggio · le tecniche',title),pinned=pinned+pcol(txt),notes=notes)
    else: sec(id_,head('Carteggio · le tecniche',title)+col(txt),pinned=pinned,notes=notes)
tech_slide('t_stesso','stesso','Stesso punto, due rilevamenti',
 term('Quando','Un solo punto cospicuo, rilevato due volte a distanza di tempo, con prora e velocità note.')+term('Come','Traccia i due rilevamenti veri dal faro. Porta il primo avanti del cammino fatto (Pv, V × t) spostandolo parallelo a sé stesso.')+term('Il punto','Il primo trasportato incrocia il secondo: è il punto nave all\'ora del secondo rilevamento.'),
 'È il «rilevamento trasportato» o punto nave con rilevamenti successivi sulla stessa mira: 5.1.3-1, -2, -4, -5, 5.2.3-2, 5.3.3-4, 5.4.3-1, -2, -5. Il trasporto si fa spostando il faro del cammino e tracciando da lì la parallela al primo rilevamento.',False)
tech_slide('t_diversi','diversi','Due punti, due ore diverse',
 term('Quando','Due punti cospicui diversi, rilevati in due momenti: non c\'è un incrocio immediato.')+term('Come','Il primo rilevamento si trasporta del cammino fatto fino al secondo, esattamente come prima.')+term('Il punto','L\'incrocio con il rilevamento del secondo punto è il punto nave.'),
 'Esercizi 5.2.3-1, -3, -4, -5, 5.3.3-1, -5, -6, -7, 5.4.3-3, -4. Se i rilevamenti fossero contemporanei (lezione 5) basterebbe incrociarli.',True)
tech_slide('t_tre','tre','Tre rilevamenti',
 term('Quando','Lo stesso faro rilevato tre volte: 5.1.3-3, di notte, riconoscendo il faro dalla caratteristica.')+term('Come','Trasporta il primo e il secondo rilevamento del cammino fatto fino all\'ora del terzo.')+term('La verifica','Le tre linee devono incontrarsi quasi in un punto: se formano un triangolo grande, c\'è un errore.'),
 'Nel 5.1.3-3 il faro che emette un lampo ogni 5 secondi a sud dell\'Elba è Capo Poro (Fl 5s). Cammini: 7,5 e 4,5 miglia.',False)
tech_slide('t_traverso','traverso','Passare al traverso',
 term('Quando','Vuoi passare a una certa distanza da un faro, lasciandolo a dritta o a sinistra.')+term('Come','Cerchio del raggio dato attorno al faro e tangente da A dal lato giusto: è la Pv. Il punto di tangenza C è il traverso.')+term('La prora bussola','Pm = Pv − d; con la Pm entra nella tabella e trovi δ; Pb = Pm − δ.'),
 'Esercizi 5.3.3-2 e 5.3.3-3 con Scoglio d\'Africa. Faro a dritta: la rotta lo lascia sulla destra, quindi è ruotata a sinistra rispetto al rilevamento diretto del faro.',True)
tech_slide('t_intercetta','intercetta','Intercettare una barca',
 term('Quando','Una barca chiede aiuto e si muove: devi scegliere la rotta che la incontra.')+term('Triangolo delle velocità','Da A disegna la sua velocità (1 ora). Dalla punta la parallela ad AB; il compasso aperto della tua velocità, puntato in A, la taglia.')+term('Il punto D','La direzione da A al taglio è la rotta da tenere; dove incrocia la rotta dell\'altra barca c\'è D.'),
 'Esercizi 5.1.3-6, 5.4.3-6, -7, -8. Il metodo mantiene costante il rilevamento dell\'altra barca: se il rilevamento non cambia e la distanza cala, ci si incontra.',False)

# ============ TABELLA DI DEVIAZIONE ============
rows=[(pm,geo.DEV[pm]) for pm in range(120,205,5)]
half=(len(rows)+1)//2
def cell(v,b=False): return f'<td style="font-weight:{800 if b else 500}">{v}</td>'
trs=''.join('<tr>'+cell(f'{a[0]:03d}°',True)+cell(f'{a[1]:+d}°'.replace('+0','0'))+cell(f'{geo.norm(a[0]-a[1]):03d}°')+(cell(f'{c[0]:03d}°',True)+cell(f'{c[1]:+d}°')+cell(f'{geo.norm(c[0]-c[1]):03d}°') if c else '<td></td><td></td><td></td>')+'</tr>' for a,c in zip(rows[:half],rows[half:]+[None]))
tab=f'<table style="font-size:26px; color:{INK}; width:760px"><tr><th style="width:16%">Pm</th><th style="width:16%">δ</th><th style="width:18%">Pb</th><th style="width:16%">Pm</th><th style="width:16%">δ</th><th style="width:18%">Pb</th></tr>{trs}</table>'
side=card(tag('Come si usa')+p('Si entra con la <b>prora magnetica</b> Pm = Pv − d e si legge δ; poi Pb = Pm − δ.',26,INK)+p('Tra due righe si interpola: Pm 182° sta tra +3° e +4°, si prende +3°.',24)+note('5.3.3-2: Pv 184°, d 2°E → Pm 182° → δ +3° → Pb 179°',CORAL,32),None,32,14)
sec('deviazione', head('Carteggio · DD 131/2022','La tabella di deviazione')+f'<div style="display:flex; gap:32px; align-items:start">{tab}{side}</div>',
 notes='Estratto (Pm da 120° a 200°) della tabella di deviazione allegata agli esercizi ufficiali, la stessa per le carte 5/D e 42/D. Tabella completa nel sito del corso e nell\'allegato del decreto. Serve quando la traccia dice «è necessario utilizzare la tabella delle deviazioni allegata».')

quiz_slide('quiz1','Quiz · Navigazione costiera',['1.7.6-31','1.7.6-47','1.7.6-12'],False)
quiz_slide('quiz1r','Quiz · Le risposte',['1.7.6-31','1.7.6-47','1.7.6-12'],True)

# ============ MAPPA GENERALE ============
class Dummy: pass
M=es10.Sol('5.1.3-1',(42.62,10.55)); M.pts=[]; M.lines=[]
used=['Faro di Punta Polveraia','Faro dello Scoglietto','Faro di Capo Poro','Punta Nera','Scoglio dello Sparviero','Faro di Punta Ala','Fanali di Castiglione della Pescaia','Punta Martina','Serbatoio di Marina di Grosseto',
      "Faro dell'Isola di Pianosa",'Punta Brigantina','Torre di Cala della Ruta',"Faro di Scoglio d'Africa",'Faro di Punta del Fenaio','Faro di Formica Grande','Faro di Punta Lividonia','Faro di Talamone',"Capo d'Uomo"]
short={'Faro di Punta Polveraia':'Punta Polveraia','Faro dello Scoglietto':'Scoglietto','Faro di Capo Poro':'Capo Poro','Faro di Punta Ala':'Punta Ala','Fanali di Castiglione della Pescaia':'Castiglione','Serbatoio di Marina di Grosseto':'Serbatoio M. Grosseto',
       "Faro dell'Isola di Pianosa":'Pianosa','Torre di Cala della Ruta':'T. Cala della Ruta',"Faro di Scoglio d'Africa":"Scoglio d'Africa",'Faro di Punta del Fenaio':'P.ta del Fenaio','Faro di Formica Grande':'Formica Grande','Faro di Punta Lividonia':'P.ta Lividonia','Faro di Talamone':'Talamone','Scoglio dello Sparviero':'Sparviero','Punta Brigantina':'P.ta Brigantina'}
for n in used: M.pts.append((geo.lm(n),short.get(n,n),'lm'))
M.pts.append(((42.30,10.0),'','none')); M.pts.append(((42.93,11.2),'','none'))
sec('mappa', head('Carteggio · la carta','I punti cospicui della carta 5/D'), pinned=chart_html(M,128,290,1664,620,True,'Carta schematica dall\'Elba all\'Argentario con i punti cospicui usati negli esercizi di oggi'),
 notes='Coste da OpenStreetMap (© contributori OpenStreetMap, ODbL). Settore A: Elba; B: da Follonica a Marina di Grosseto; C: Pianosa e Scoglio d\'Africa; D: Formiche, Giglio, Argentario e Talamone. Punta Nera (ovest Elba) e Torre Cala della Ruta (Pianosa) sono state posizionate risolvendo al contrario gli esercizi ufficiali che le usano.')

# ============ ESERCIZI ============
SETT={'5.1':('A','Elba',SEA),'5.2':('B','Castiglione e Punta Ala',PURPLE),'5.3':('C','Pianosa',BLUE),'5.4':('D','Giglio e Argentario',GREEN)}
order_ex=[]
def rng(r): return r.replace('\n',' ').replace('Lat.','Lat ').replace('Long.','Long ').replace('÷',' ÷ ')
for f in es10.SOLS:
    S=f(); sid='e'+S.id.replace('.','_').replace('-','_')
    st=SETT[S.id[:3]]
    txt=S.ex['testo'].replace('\n',' ').replace('PER LA RISOLUZIONE DEL QUESITO E\' NECESSARIO UTILIZZARE LA TABELLA DELLE DEVIAZIONI ALLEGATA','(Serve la tabella di deviazione.)')
    fs=26 if len(txt)<520 else (24 if len(txt)<760 else 22)
    ask=txt.split('Determinare')[-1].strip().rstrip('.') if 'Determinare' in txt else 'il risultato'
    left_col=f'<div style="display:flex; flex-direction:column; gap:20px; width:690px">{p(txt,fs,INK,500,1.45)}<p style="font-size:26px; font-weight:900; color:#FFFFFF; background:{st[2]}; padding:10px 20px; border-radius:18px">Da trovare: {ask}</p></div>'
    sec(sid+'_t', head(f'Esercizio {S.id} · settore {st[0]} · {st[1]}','La traccia',st[2])+left_col, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell\'esercizio {S.id} con i punti cospicui'),
        notes=f'Traccia ufficiale (Allegato A al DD 131/2022). Risposta ufficiale: {rng(S.ex["risposta_ufficiale"])}. Lasciare 8-10 minuti per il tracciamento, poi passare alla soluzione.')
    ol='<ol style="font-size:24px; line-height:1.38; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{x}</li>' for x in S.passi)+'</ol>'
    res=f'<div style="display:flex; flex-direction:column; gap:4px; background:{CORAL_T}; padding:16px 20px; border-radius:20px"><p style="font-size:26px; font-weight:900; color:{CORAL}">{S.res_txt}</p><p style="font-size:22px; font-weight:700; color:{INK}">Ufficiale: {rng(S.ex["risposta_ufficiale"])}</p></div>'
    sec(sid+'_s', head(f'Esercizio {S.id} · soluzione','Il tracciamento',st[2]), pinned=chart_html(S,128,290,1092,620,True,f'Tracciamento dell\'esercizio {S.id}')+pcol(ol+res,532,16),
        notes='Soluzione: '+' '.join(S.passi)+f' Risultato: {S.res_txt}. Ufficiale: {rng(S.ex["risposta_ufficiale"])}. Calcolo verificato con le coordinate OpenStreetMap dei punti cospicui; sulla carta 5/D il tracciamento a matita dà lo stesso risultato entro la forchetta.')
    order_ex+=[sid+'_t',sid+'_s']

closing(['Prima di tracciare converti tutto in vero: V = d + δ, e aggiorna la declinazione','Rilevamento trasportato: sposta il faro del cammino e ritraccia il primo rilevamento','Tre rilevamenti: devono incontrarsi quasi in un punto','Traverso: cerchio e tangente dal lato giusto; poi Pm, tabella, Pb','Intercettazione: sua velocità da A, parallela ad AB, arco della tua velocità'],
 'Prossima lezione · 11 · Carburante e autonomia','A casa: rifai sulla carta 5/D gli esercizi non svolti in aula.')
write_deck(OUT,'Lezione 10 · Carteggio: navigazione costiera',
 ['cover','agenda','kit','t_stesso','t_diversi','t_tre','t_traverso','t_intercetta','deviazione','quiz1','quiz1r','mappa']+order_ex+['chiusura'],
 {"s1":{"description":"Apertura, kit e tecniche","start":"cover"},"s2":{"description":"Settore A · Elba","start":"e5_1_3_1_t"},"s3":{"description":"Settore B · Castiglione e Punta Ala","start":"e5_2_3_1_t"},
  "s4":{"description":"Settore C · Pianosa","start":"e5_3_3_1_t"},"s5":{"description":"Settore D · Giglio e Argentario","start":"e5_4_3_1_t"}})
