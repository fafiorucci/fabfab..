import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez09/project'
GREY='#97A6B4'; SKY='#DDEFF7'; LRED='#E23B3B'
LB.ICON_T.update({'Esercitazione quiz vela':'quiz','La vela in otto flash':'sail','La lezione di oggi':'lifebuoy','La barca a vela':'sail','La randa':'sail','Le vele di prua':'sail','Gli armi':'sail',
 'La ferramenta di bordo':'anchor','Le andature':'compass','Il vento apparente':'wind','Come spinge la vela':'wind','Centro velico e centro di deriva':'helm',
 'Regolare le vele':'wind','Orzare e poggiare':'helm','Virata e abbattuta':'compass','Le precedenze a vela':'flag','Issare, ridurre, fermarsi':'sail'})
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=24,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
X,Y,W,Hh=700,290,1092,620

# ---- barca a vela di profilo (prua a destra) ----
def yacht(x0,wl,L,head='genoa',rig='sloop',main_c='#FFFFFF',head_c=SUN,st=NAVY,sw=3,rigging=True):
    u=lambda a: x0+a*L
    dk=wl-0.07*L; bowy=wl-0.085*L
    mxa=0.5 if rig=='ketch' else 0.45; mx=u(mxa); dm=dk-(bowy-dk)*0+(-0.0)*L
    mt=dm-0.6*L; by=dm-0.07*L
    pts={'mx':mx,'mt':mt,'dm':dm,'by':by,'wl':wl}
    s=''
    bp=(u(0.975),bowy)
    ft=mt+0.02*L
    if rigging: s+=line(mx,mt+0.01*L,u(0.015),dk,st,2.5)
    s+=line(mx,dm,mx,mt,INK,max(3,L*0.009))
    hd=(mx+0.004*L,mt+0.02*L); tk=(mx+0.004*L,by); cl=(mx-0.3*L,by)
    s+=f'<path d="M{hd[0]:.1f} {hd[1]:.1f} L{tk[0]:.1f} {tk[1]:.1f} L{cl[0]:.1f} {cl[1]:.1f} Q{mx-0.236*L:.1f} {mt+0.25*L:.1f} {hd[0]:.1f} {hd[1]:.1f} Z" fill="{main_c}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    pts.update(mhead=hd,mtack=tk,mclew=cl,mc=(mx-0.1*L,by-0.2*L))
    s+=line(mx,by,mx-0.31*L,by,INK,max(3,L*0.008))
    pt=lambda t,a=(mx,ft),b=bp: (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)
    if rig=='ketch':
        zx=u(0.2); zt=dm-0.36*L; zb=dm-0.05*L
        s+=line(zx,dm,zx,zt,INK,max(3,L*0.008))+f'<path d="M{zx:.1f} {zt+0.02*L:.1f} L{zx:.1f} {zb:.1f} L{u(0.04):.1f} {zb:.1f} Q{u(0.08):.1f} {zt+0.15*L:.1f} {zx:.1f} {zt+0.02*L:.1f} Z" fill="{main_c}" stroke="{st}" stroke-width="{sw}"/>'+line(zx,zb,u(0.035),zb,INK,max(3,L*0.007))
        pts['zx']=zx; pts['zt']=zt
    hs=''
    if head=='genoa':
        h=pt(0.06); t=pt(0.97); c=(mx-0.06*L,dm-0.025*L)
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} L{t[0]:.1f} {t[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Q{mx+0.03*L:.1f} {mt+0.3*L:.1f} {h[0]:.1f} {h[1]:.1f} Z"'
        pts['hc']=(mx+0.14*L,dm-0.14*L)
    elif head=='fiocco':
        h=pt(0.22); t=pt(0.97); c=(mx+0.1*L,dm-0.05*L)
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} L{t[0]:.1f} {t[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Q{mx+0.06*L:.1f} {mt+0.35*L:.1f} {h[0]:.1f} {h[1]:.1f} Z"'
        pts['hc']=(mx+0.2*L,dm-0.15*L)
    elif head=='spi':
        h=(mx+0.02*L,mt+0.03*L); c1=(u(1.1),dm-0.1*L); c2=(u(0.74),dm-0.1*L)
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} Q{u(1.22):.1f} {mt+0.18*L:.1f} {c1[0]:.1f} {c1[1]:.1f} Q{u(0.92):.1f} {dm-0.02*L:.1f} {c2[0]:.1f} {c2[1]:.1f} Q{u(0.58):.1f} {mt+0.25*L:.1f} {h[0]:.1f} {h[1]:.1f} Z"'
        s+=hs+f' fill="{head_c}" stroke="{st}" stroke-width="{sw}"/>'+line(mx,dm-0.1*L,c2[0],c2[1],INK,max(2.5,L*0.007)); hs=''
        pts['hc']=(u(0.9),mt+0.3*L)
    elif head=='genn':
        h=(mx+0.02*L,mt+0.04*L); tk2=(u(0.99),bowy-0.02*L); c=(u(0.72),dm-0.13*L)
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} Q{u(1.16):.1f} {mt+0.3*L:.1f} {tk2[0]:.1f} {tk2[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Q{u(0.66):.1f} {mt+0.3*L:.1f} {h[0]:.1f} {h[1]:.1f} Z"'
        pts['hc']=(u(0.85),mt+0.35*L)
    if rig=='cutter':
        # yankee alto e trinchetta interna
        h=pt(0.06); t=pt(0.97); c=(mx+0.24*L,dm-0.2*L)
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} L{t[0]:.1f} {t[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Q{mx+0.12*L:.1f} {mt+0.25*L:.1f} {h[0]:.1f} {h[1]:.1f} Z"'
        a2=(mx,mt+0.2*L); b2=(u(0.8),dm-0.005*L); p2=lambda t: (a2[0]+(b2[0]-a2[0])*t, a2[1]+(b2[1]-a2[1])*t)
        h2=p2(0.06); t2=p2(0.95); c2=(mx+0.06*L,dm-0.04*L)
        hs+=f' fill="{head_c}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'+line(a2[0],a2[1],b2[0],b2[1],st,2)
        hs+=f'<path d="M{h2[0]:.1f} {h2[1]:.1f} L{t2[0]:.1f} {t2[1]:.1f} L{c2[0]:.1f} {c2[1]:.1f} Z"'
    if hs: s+=hs+f' fill="{head_c}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    if rigging:
        s+=line(mx,ft,bp[0],bp[1],st,2.5)
        cy_=mt+0.28*L; s+=line(mx,cy_,mx+0.035*L,cy_,st,3)+line(mx,mt+0.02*L,mx+0.035*L,cy_,st,2)+line(mx+0.035*L,cy_,mx+0.02*L,dm,st,2)
        pts['cro']=(mx+0.035*L,cy_)
    pts['bp']=bp
    hull=f'M{u(0):.1f} {dk:.1f} L{u(1):.1f} {bowy:.1f} Q{u(0.97):.1f} {wl+0.01*L:.1f} {u(0.86):.1f} {wl+0.035*L:.1f} L{u(0.12):.1f} {wl+0.035*L:.1f} Q{u(0.03):.1f} {wl+0.03*L:.1f} {u(0.01):.1f} {wl:.1f} Z'
    kx=mx+0.05*L; kb=wl+0.035*L
    s+=f'<path d="M{kx-0.05*L:.1f} {kb:.1f} L{kx+0.06*L:.1f} {kb:.1f} L{kx+0.035*L:.1f} {kb+0.1*L:.1f} L{kx-0.035*L:.1f} {kb+0.1*L:.1f} Z" fill="{NAVY}"/><ellipse cx="{kx:.1f}" cy="{kb+0.105*L:.1f}" rx="{0.07*L:.1f}" ry="{0.018*L:.1f}" fill="{INK}"/>'
    rx_=u(0.1)
    s+=f'<path d="M{rx_-0.02*L:.1f} {kb-0.01*L:.1f} L{rx_+0.03*L:.1f} {kb-0.01*L:.1f} L{rx_+0.02*L:.1f} {kb+0.08*L:.1f} L{rx_-0.01*L:.1f} {kb+0.075*L:.1f} Z" fill="{CORAL}"/>'
    s+=f'<path d="{hull}" fill="#FFFFFF" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    s+=f'<path d="M{u(0.02):.1f} {dk+0.03*L:.1f} L{u(0.985):.1f} {bowy+0.03*L:.1f}" stroke="{CORAL}" stroke-width="{max(4,L*0.01):.1f}"/>'
    pts.update(kx=kx,kb=kb,rx=rx_,dk=dk,bowy=bowy)
    return s,pts

# ---- barca vista dall'alto con vele (heading in gradi da nord, lato 1 = vele a dritta) ----
def topsail(cx,cy,L,hd,sa,side,fill='#FFFFFF',st=NAVY,main=CORAL,jib=SUN):
    a=math.radians(sa)
    mxl=L*0.12; bl=L*0.46; jl=L*0.34
    ex=mxl-bl*math.cos(a); ey=side*bl*math.sin(a)
    jx=L*0.46-jl*math.cos(a*0.85); jy=side*jl*math.sin(a*0.85)
    cm=(mxl+ex)/2+side*0*1; g=f'<path d="M{L*0.46:.1f} 0 Q{(L*0.46+jx)/2+side*0:.1f} {jy*0.5+side*L*0.05:.1f} {jx:.1f} {jy:.1f}" fill="none" stroke="{jib}" stroke-width="{max(4,L*0.05):.1f}" stroke-linecap="round"/>'
    g+=f'<path d="M{mxl:.1f} 0 Q{(mxl+ex)/2:.1f} {ey*0.5+side*L*0.06:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="{main}" stroke-width="{max(5,L*0.06):.1f}" stroke-linecap="round"/>'
    return topboat(cx,cy,L,hd-90,fill,st,3,1,False)+f'<g transform="translate({cx} {cy}) rotate({hd-90})">{g}<circle cx="{mxl:.1f}" cy="0" r="{max(4,L*0.03):.1f}" fill="{INK}"/></g>'
def pol(cx,cy,b,r): return (cx+r*math.sin(math.radians(b)), cy-r*math.cos(math.radians(b)))
def windarrow(x,y,l=110,c=GREY): return arrow(x,y,x,y+l,c,8,26)

import nodi
ORANGE='#F28C28'; LAND='#F2E2B3'
LB.ICON_T.update({'Albero, boma e manovre fisse':'sail','Le manovre correnti':'sail','I nodi':'anchor','Le vele':'sail','Lati e angoli delle vele':'sail',
 'Il piano velico':'sail','Armare le vele':'sail','La stabilità':'hull','Terzaroli, panna e cappa':'sail','Regolare le vele':'wind'})
def box(t,inner,c,bg,flex=1): return f'<div style="flex:{flex}; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:24px 28px; border-radius:28px; border-left:10px solid {c}">{tag(t,c)}{inner}</div>'
def lst(items,size=24,gap=8): return f'<ul style="font-size:{size}px; line-height:1.36; color:#34465E; display:flex; flex-direction:column; gap:{gap}px">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def sterm(t,d,s=24): return f'<div style="display:flex; flex-direction:column; gap:4px">{p(t,s+3,INK,800,1.25)}{p(d,s,BODY,400,1.36)}</div>'

# ============ COVER + AGENDA ============
cover(9,'Vela','Com\'è fatta una barca a vela, perché va controvento e come si manovra',
 'Lezione 9, solo per chi fa la patente a vela: chi fa solo motore la salta. Rivista sulla scaletta della scuola (18 argomenti): ferramenta di bordo; albero, boma e manovre fisse; manovre correnti; vele; lati e angoli delle vele; armare le vele; stabilità e scarroccio; andature; poggiare e orzare; regolazione vele; virata e abbattuta; terzaroli e panna; vento apparente e reale; centro velico e centro di deriva; piano velico; vele di prora; nodi; precedenze. All. A al DM 323/2021, punto 1c. All\'esame la prova di vela ha 5 quesiti Vero/Falso in più rispetto alla patente a motore: si supera con al massimo 1 errore. Banca ufficiale: 250 quiz (99 teoria, 86 attrezzatura, 65 manovre).')
blocks=[('0:00','18′','Cap. 1 · L\'attrezzatura',CORAL),('0:18','16′','Cap. 2 · Le vele',SEA),('0:34','21′','Cap. 3 · La teoria',PURPLE),('0:55','20′','Cap. 4 · Le manovre',BLUE),('1:15','45′','Raccolta: 36 quiz vela',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
def esame_vela(compact=False):
    return card(tag("All'esame · prova di vela")+f'<div style="display:flex; gap:40px; align-items:end"><div>{p("quesiti",24,BODY,700)}<p style="font-family:{H}; font-size:{64 if compact else 80}px; font-weight:700; line-height:1; color:{INK}">5</p></div><div>{p("errori ammessi",24,BODY,700)}<p style="font-family:{H}; font-size:{64 if compact else 80}px; font-weight:700; line-height:1; color:{CORAL}">1</p></div><div>{p("tempo",24,BODY,700)}<p style="font-family:{H}; font-size:{64 if compact else 80}px; font-weight:700; line-height:1; color:{INK}">15′</p></div></div>'+p('Tutti Vero o Falso, dalla banca di 250 quiz: attenzione a «sempre», «esclusivamente», «solo». Si fa nello stesso blocco dei 20 quiz base.',24),None,30,14,1.5)
def esame_box(*a,**k): return esame_vela(True)
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:24px; line-height:1.35; color:#34465E; display:grid; grid-template-columns:1fr 1fr; gap:8px 40px"><li>chiamare per nome vele, manovre, ferramenta e nodi</li><li>armare e regolare le vele</li><li>riconoscere le andature e il vento apparente</li><li>spiegare perché la barca risale il vento e non si rovescia</li><li>orzare, poggiare, virare, abbattere, ridurre</li><li>applicare le precedenze tra barche a vela</li></ul>',SEA_T,flex=2.2)
sec('agenda', head('Lezione 09 · 2 ore · solo vela','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{esame_vela()}</div>',
 notes='Quattro capitoli di teoria in 75 minuti, ognuno aperto dalla sua slide e chiuso da una verifica da 2 quiz vela ufficiali (DD 131/2022): andare spediti, il dettaglio è nelle note. Poi 45 minuti di raccolta: 36 quiz vela, 12 slide da 3 con le risposte. Banca: 2.2.1 attrezzatura (86), 2.1.1 teoria della vela (99), 2.3.1 manovre (65). Le prove d\'esame complete con i 5 quiz vela sono nell\'appendice D.', gap=26)

# =====================================================================
# CAPITOLO 1 · L'ATTREZZATURA
# =====================================================================
s,P_=yacht(180,505,720)
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'+s+f'<rect x="0" y="505" width="1092" height="115" fill="{WATER}" fill-opacity="0.45"/>'+line(0,505,1092,505,SEA,3)
b+=f'<circle cx="{P_["mx"]:.0f}" cy="{P_["by"]:.0f}" r="9" fill="{CORAL}"/><rect x="{P_["mx"]+0.035*720-8:.0f}" y="{P_["dm"]-6:.0f}" width="16" height="10" fill="{CORAL}"/>'
lbl=pill(X+P_['mx']+18,Y+14,110,'albero',NAVY)+pill(X+250,Y+160,150,'paterazzo',NAVY)+pill(X+690,Y+180,120,'strallo',NAVY)
lbl+=pill(X+P_['mx']+30,Y+P_['cro'][1]-18,120,'crocette',NAVY,22)+pill(X+P_['mx']+24,Y+372,100,'sartie',NAVY,22)+pill(X+P_['mx']+40,Y+P_['dm']-50,90,'landa',CORAL,22)
lbl+=pill(X+330,Y+300,100,'randa',SOFT)+pill(X+620,Y+310,100,'genoa',SOFT)+pill(X+250,Y+P_['by']+8,90,'boma',PURPLE,22)+pill(X+P_['mx']-150,Y+P_['by']-46,100,'trozza',CORAL,22)
lbl+=pill(X+660,Y+462,90,'scafo',SEA)+pill(X+650,Y+568,220,'bulbo zavorrato',SEA,22)+pill(X+80,Y+560,110,'timone',SEA,22)
txt=sterm('Albero e boma','La trozza è lo snodo che unisce il boma all\'albero. La varea è l\'estremità esterna di un\'asta, come il tangone.')+sterm('Manovre fisse','Strallo, paterazzo e sartie sono cavi d\'acciaio che reggono l\'albero e non ci passano dentro. Le crocette allargano le sartie e le tensionano; in coperta si fissano alle lande e si regolano con gli arridatoi.')+sterm('Armo frazionato','Lo strallo non arriva in testa d\'albero: le sartie volanti controbilanciano lo sforzo. Con crocette acquartierate e paterazzo le volanti aiutano, ma non sono strutturali.')
sec('barca', head('Vela · l\'attrezzatura','Albero, boma e manovre fisse')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Barca a vela armata a sloop di profilo con albero, boma, trozza, strallo, paterazzo, sartie, crocette, lande, scafo, bulbo e timone')+lbl,
 notes='Materiale della scuola: albero, boma, manovre fisse. Colori: blu manovre fisse, corallo trozza e lande, viola boma, verde acqua scafo. Quiz 2.2.1-77 e -29 (stralli e sartie: manovre fisse), -69 (sartie in acciaio), -72 (non passano dentro l\'albero), -7 (le sartie non si regolano con il carrello), -6 e -5 (crocette: tensionano le sartie, non reggono le scotte; in realtà le allargano, ma al quiz vale la frase della scuola), -42 (landa), -45 (trozza), -44 (varea del tangone: non è l\'anello del mantiglio), -1, -2, -3, -4 (armo frazionato e sartie volanti; non c\'entrano i compartimenti dello scafo), -52 e -53 (paterazzo), -74 (l\'albero si regola sulle manovre fisse), 2.1.1-1 e -2 (scafo).')

X=128
s,P_=yacht(180,505,720)
L_=720; mx=P_['mx']; by=P_['by']; dm=P_['dm']
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'+s+f'<rect x="0" y="505" width="1092" height="115" fill="{WATER}" fill-opacity="0.45"/>'+line(0,505,1092,505,SEA,3)
be=mx-0.29*L_; dky=P_['dk']+0.004*L_
b+=line(mx-6,P_['mt']+20,mx-6,dm-6,CORAL,5)+line(mx+8,P_['mt']+30,mx+8,dm-6,CORAL,5)
b+=line(mx-4,dm-0.01*L_,mx-0.11*L_,by+3,PURPLE,6)
b+=line(be,by+6,be,dky,SUN,4)+f'<circle cx="{be:.0f}" cy="{by+16:.0f}" r="9" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><circle cx="{be:.0f}" cy="{dky-10:.0f}" r="9" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<rect x="{be-50:.0f}" y="{dky-6:.0f}" width="100" height="10" rx="5" fill="{NAVY}"/>'
b+=line(P_['mtack'][0],P_['mtack'][1]-10,P_['mtack'][0]-4,P_['mtack'][1]+20,GREEN,5)
b+=line(P_['mclew'][0],P_['mclew'][1],P_['mclew'][0]+30,P_['mclew'][1]+2,BLUE,6)
gc=(mx-0.06*L_,dm-0.025*L_); b+=line(gc[0],gc[1],mx-0.2*L_,P_['dk']+0.02*L_,SUN,4)
pr_=f'<rect x="30" y="30" width="210" height="200" rx="18" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="3"/>'+line(110,44,110,58,NAVY,4)+f'<circle cx="110" cy="74" r="18" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><circle cx="110" cy="176" r="18" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'+''.join(line(x,74,x,176,SUN,4) for x in (96,104,116,124))+line(110,194,110,212,NAVY,4)+line(124,176,170,214,SUN,4)+arrow(170,214,196,196,CORAL,4,12)
b+=pr_
lbl=lab(X+40,Y+236,200,'paranco 4:1: tiri 1/4',NAVY,20,900,'center')+pill(X+mx+20,Y+20,100,'drizze',CORAL,22)+pill(X+mx-110,Y+by-50,90,'vang',PURPLE,22)+pill(X+40,Y+by+22,250,'scotta e paranco',SUN,22,INK)
lbl+=pill(X+100,Y+dky+16,220,'carrello (trasto)',NAVY,22)+pill(X+mx+20,Y+by-24,150,'cunningham',GREEN,22)+pill(X+P_['mclew'][0]-70,Y+P_['mclew'][1]-56,140,'tesabase',BLUE,22)
lbl+=pill(X+340,Y+P_['dk']+34,200,'scotta del genoa',SUN,22,INK)
txt=sterm('Manovre correnti','Servono a manovrare le vele: drizze per issarle, scotte per regolarle, vang, cunningham e tesabase per la forma. Stralli e sartie non lo sono.')+sterm('Vang e cunningham','Il vang trattiene il boma, regola la flessione dell\'albero e la superficie portante della randa; non dipende dal paterazzo. Il cunningham è un paranco verticale che tesa la parte prodiera bassa della randa.')+sterm('Paranco e carrello','Il paranco di scotta demoltiplica lo sforzo: con 4 tratti di cima tiri un quarto della forza. Il carrello (trasto) sposta il punto di scotta; le scotte si danno volta sul paranco, non sul carrello.')
sec('correnti', head('Vela · l\'attrezzatura','Le manovre correnti'), pinned=svgp(X,Y,W,Hh,b,'Barca a vela di profilo con le manovre correnti colorate: drizze, vang, scotta e paranco della randa sul carrello, cunningham, tesabase e scotta del genoa')+lbl+pcol(txt,gap=18),
 notes='Materiale della scuola: manovre correnti. Quiz 2.2.1-75 (manovre correnti: scotte, drizze, vang, tesabase), -29 (stralli e sartie non lo sono), -33 (cunningham), -71 (vang), -52 (il paterazzo non regola il vang), -30 (paranco di scotta: demoltiplica lo sforzo), -40 (carrello randa: non serve a dare volta alle scotte), -12 (tesabase all\'angolo di scotta), 2.3.1-8 e -16 (drizza tesata, base più o meno cazzata secondo l\'andatura).')
X=700

def ico(k):
    s=f'<rect x="0" y="0" width="150" height="120" rx="24" fill="{SEA_T}"/>'
    if k=='winch':
        s+=f'<circle cx="75" cy="60" r="40" fill="#C9D3DD" stroke="{NAVY}" stroke-width="4"/><circle cx="75" cy="60" r="22" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'+curved(75,60,32,-160,60,CORAL,5)
    elif k=='stopper':
        s+=f'<rect x="20" y="42" width="110" height="36" rx="12" fill="{NAVY}"/><path d="M50 42 L96 18" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/>'+line(0,60,150,60,SUN,8)
    elif k=='galloccia':
        s+=f'<rect x="60" y="74" width="30" height="20" fill="{NAVY}"/><path d="M18 74 Q20 56 40 58 L110 58 Q130 56 132 74 Z" fill="#B98A55" stroke="{NAVY}" stroke-width="3"/>'+f'<path d="M30 66 C60 40 90 92 120 66" fill="none" stroke="{SUN}" stroke-width="7"/>'
    elif k=='golfare':
        s+=f'<rect x="30" y="80" width="90" height="16" rx="6" fill="{NAVY}"/><path d="M45 82 L45 50 Q45 22 75 22 Q105 22 105 50 L105 82" fill="none" stroke="#8A97A6" stroke-width="12"/>'
    elif k=='grillo':
        s+=f'<path d="M50 30 L50 70 Q50 104 75 104 Q100 104 100 70 L100 30" fill="none" stroke="#8A97A6" stroke-width="12"/><rect x="34" y="20" width="82" height="14" rx="7" fill="{NAVY}"/>'
    elif k=='arridatoio':
        s+=line(75,0,75,26,NAVY,5)+line(75,94,75,120,NAVY,5)+f'<rect x="60" y="26" width="30" height="68" rx="10" fill="none" stroke="#8A97A6" stroke-width="8"/>'+line(75,26,75,48,NAVY,7)+line(75,72,75,94,NAVY,7)
    return s
FT=[('galloccia','Galloccia','Ci si dà volta alle cime, per esempio a quelle di ormeggio. Non serve a fissare le draglie.'),
    ('golfare','Golfare','Anello fissato allo scafo a cui si attaccano paranchi e cime. Non è il carrello del boma.'),
    ('grillo','Grillo','Raccordo a U con perno che unisce manovre e catene. Non riduce lo sforzo.'),
    ('arridatoio','Arridatoio','Il tornichetto: doppia vite per tesare le sartie. Non unisce due cime.'),
    ('stopper','Stopper','Strozza e blocca una drizza o una scotta. Lo strozzascotte fa lo stesso sulle scotte.'),
    ('winch','Winch','La cima si avvolge sempre in senso orario, senza sovrapporre i giri; la maniglia in senso orario dà più trazione. Il self-tailing trattiene la cima da solo, non è elettrico.')]
tiles=''.join(card(f'<div style="display:flex; gap:20px; align-items:start">{svgi(150,120,ico(k),"Disegno: "+t,dw=170,dh=136,pan=False)}<div style="display:flex; flex-direction:column; gap:6px">{h3(t,30)}{p(d,23)}</div></div>',None,22,0) for k,t,d in FT)
sec('ferramenta', head('Vela · l\'attrezzatura','La ferramenta di bordo')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:22px">{tiles}</div>'+note('Ferramenta di bordo: strozzascotte, winch, arridatoi, gallocce e tutti gli attacchi metallici della coperta.',PURPLE,32),
 notes='Materiale della scuola: ferramenta di bordo. Quiz 2.2.1-37 (ferramenta: strozzascotte, winch, arridatoi, gallocce), -41 (galloccia: non per le draglie), -43 (golfare), -39 (grilli: non riducono lo sforzo), -70 (tornichetto: tesa le sartie, non unisce cime), -85 e -86 (stopper: blocca una drizza, non fissa il boma), -35 (il winch non è fatto di due bozzelli), -36 e -78 (senso orario), -76 (self-tailing: non elettronico).')

def knot(k,W_=300):
    K=nodi.KNOTS[k](); body,cap=K['panels'][-1]
    w,h=(nodi.PW,nodi.PH) if K['layout']=='land' else (nodi.QW,nodi.QH)
    return f'<svg aria-label="Nodo {k}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="width:{W_}px; height:{W_*h/w:.0f}px; flex:none; background:#E4F3F1; border-radius:20px">{body}</svg>'
NK=[('savoia','Nodo Savoia','Il nodo d\'arresto: impedisce che la cima si sfili da un passacavo o da un bozzello, per esempio in fondo alle scotte.',CORAL),
    ('piano','Nodo piano','Unisce due cime dello stesso diametro. Non si usa con cime di diametro diverso.',SEA),
    ('parlato','Nodo parlato','Lega i parabordi alle draglie. Il parlato doppio non serve per le scotte del fiocco: lì si usa la gassa.',PURPLE),
    ('margherita','Nodo margherita','Accorcia una cima senza tagliarla; tiene finché resta in tiro.',BLUE)]
gassa=card(knot('gassa',200)+h3('Gassa d\'amante',30,GREEN)+p('L\'occhio che non scorre e non si scioglie da solo. Non serve ad accorciare.',23),None,22,10,0.62)
grid_=''.join(card(f'<div style="display:flex; gap:18px; align-items:center">{knot(k,260)}<div style="display:flex; flex-direction:column; gap:6px">{h3(t,28,c)}{p(d,22)}</div></div>',None,18,0) for k,t,d,c in NK)
sec('nodi', head('Vela · l\'attrezzatura','I nodi')+f'<div style="display:flex; gap:22px">{gassa}<div style="flex:1; display:grid; grid-template-columns:1fr; gap:14px">{grid_}</div></div>'+note('Le sagole galleggianti di salvataggio sono in polipropilene. L\'impiombatura intreccia i legnoli di una cima per fare un occhio fisso.',PURPLE,30),
 notes='Materiale della scuola: nodi. Quiz 2.2.1-54 e -55 (gassa d\'amante: non si scioglie da sola, non accorcia), -56 (nodo piano: non con cime di diametro diverso), -57 (savoia), -58 (parlato per i parabordi), -59 (margherita: accorcia), 2.3.1-21 (le scotte del fiocco non si fissano con il parlato doppio), 2.2.1-67 (impiombatura), -38 (polipropilene). Come si fanno, passo per passo: appendice C.', gap=24)

# =====================================================================
# CAPITOLO 2 · LE VELE
# =====================================================================
def mini(head,rig='sloop',hc=SUN,main_c='#FFFFFF'):
    s,_=yacht(30,172,220,head,rig,main_c,hc,NAVY,2)
    return f'<rect x="0" y="0" width="320" height="200" fill="{SKY}"/>'+s+f'<rect x="0" y="172" width="320" height="28" fill="{WATER}" fill-opacity="0.45"/>'
fab=f'<rect x="0" y="0" width="320" height="200" fill="#F4FAFC"/>'+''.join(line(40+i*24,30,40+i*24,180,'#C9D3DD',6) for i in range(10))+''.join(line(30,40+i*24,270,40+i*24,'#DDE6EC',6) for i in range(6))+f'<circle cx="270" cy="50" r="30" fill="{SUN}"/>'+''.join(arrow(250-i*20,80+i*10,200-i*30,130+i*14,SUN,4,12) for i in range(2))
roll=f'<rect x="0" y="0" width="320" height="200" fill="#F4FAFC"/>'+line(80,190,260,10,NAVY,4)+f'<path d="M90 190 L252 22 L262 34 L110 194 Z" fill="{SUN}"/><path d="M110 194 L262 34 L200 194 Z" fill="{SUN}" fill-opacity="0.35"/>'+curved(90,180,26,200,-20,CORAL,5)
VB=[(mini('fiocco'),'Fiocco','La vela di prua che non si sovrappone alla randa. La randa è la vela principale, triangolare, a poppavia dell\'albero.'),
    (mini('genoa',hc=CORAL),'Genoa','Più grande: oltrepassa l\'albero verso poppa, di solito per il 50% della distanza tra albero e mura. Non è una vela da cattivo tempo.'),
    (fab,'Il tessuto','Deve resistere alla trazione; il sole prolungato lo degrada. Per la crociera si usa il dacron. Le stecche della randa ne conservano la forma.'),
    (roll,'Gli avvolgitori','L\'avvolgifiocco riduce la vela di prua senza ammainarla; l\'avvolgiranda la arrotola dentro l\'albero. Non sono gallocce né gavoni.')]
cc=''.join(card(svgi(320,200,s_,f'Disegno: {t}',dw=330,dh=206,pan=False)+h3(t,30)+p(d,23),None,22,10) for s_,t,d in VB)
sec('velebase', head('Vela · le vele','Le vele')+f'<div style="display:flex; gap:20px">{cc}</div>',
 notes='Materiale della scuola: vele. Quiz 2.2.1-16 (randa: vela principale, triangolare, a poppavia dell\'albero), -20 e -18 (il fiocco non si sovrappone, il genoa sì), -19 (genoa: 50% della distanza tra albero e mura, cioè un genoa al 150%), -17 (il genoa non è una vela ridotta da cattivo tempo), -84 (avvolgifiocco), -83 (ridotto oltre il 30% perde efficienza), -73 (avvolgiranda), -46 (resistenza alla trazione), -47 (dacron), -48 (sole), 2.1.1-43 e -44 (stecche: conservano la forma, non indicano il vento).')

X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
mx,top,bm,cl=200,50,500,700
b+=line(mx,20,mx,590,INK,10)+line(mx,bm,cl+30,bm,INK,9)
b+=f'<path d="M{mx+6} {top} L{mx+6} {bm-6} L{cl} {bm-6} Q{mx+270} {top+170} {mx+6} {top} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
def qb(k):
    P0=(cl,bm-6); P1=(mx+270,top+170); P2=(mx+6,top)
    return ((1-k)**2*P0[0]+2*(1-k)*k*P1[0]+k*k*P2[0], (1-k)**2*P0[1]+2*(1-k)*k*P1[1]+k*k*P2[1])
for k in (0.2,0.4,0.6,0.8):
    (x1,y1),(x2,y2)=qb(k-0.01),qb(k+0.01); tx,ty=x2-x1,y2-y1; n=math.hypot(tx,ty); nx,ny=-ty/n,tx/n
    if nx>0: nx,ny=-nx,-ny
    px,py=qb(k); b+=line(px+nx*8,py+ny*8,px+nx*(90 if k<0.7 else 64),py+ny*(90 if k<0.7 else 64),PURPLE,7)
b+=f'<circle cx="{mx+6}" cy="{top}" r="14" fill="{CORAL}"/><circle cx="{mx+6}" cy="{bm-6}" r="14" fill="{CORAL}"/><circle cx="{cl}" cy="{bm-6}" r="14" fill="{CORAL}"/>'
jx0,jy0,jx1,jy1=1040,60,1060,520
b+=line(820,540,jx0,jy0,NAVY,3)
b+=f'<path d="M{jx0-4} {jy0+20} L{jx1-40} {jy1-20} L{860} {jy1-30} Q{900} {280} {jx0-4} {jy0+20} Z" fill="{SUN_T}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=''.join(f'<circle cx="{jx0-4+(jx1-40-jx0+4)*t:.0f}" cy="{jy0+20+(jy1-40-jy0)*t:.0f}" r="7" fill="none" stroke="{CORAL}" stroke-width="4"/>' for t in (0.15,0.4,0.65,0.9))
b+=''.join(f'<circle cx="{x}" cy="{y}" r="12" fill="{CORAL}"/>' for x,y in ((jx0-4,jy0+20),(jx1-40,jy1-20),(860,jy1-30)))
b+=dash(860,560,1020,560,NAVY,3)+f'<path d="M860 600 Q930 560 1020 600" fill="none" stroke="{PURPLE}" stroke-width="6"/>'
lbl=pill(X+mx+30,Y+top-20,120,'penna',CORAL)+pill(X+30,Y+bm-80,130,'mura',CORAL)+pill(X+cl-200,Y+bm+30,280,'scotta (bugna)',CORAL)
lbl+=pill(X+mx+20,Y+300,200,'inferitura',PURPLE,22)+pill(X+500,Y+160,140,'balumina',PURPLE,22)+pill(X+420,Y+bm-50,90,'base',PURPLE,22)+pill(X+540,Y+250,180,'tasche stecche',PURPLE,22)
lbl+=lab(X+20,Y+160,170,'ralinga nella canaletta',NAVY,20,900)+pill(X+870,Y+20,200,'fiocco · garrocci',NAVY,22)+lab(X+780,Y+560,220,'corda',NAVY,20,900,'right')
txt=sterm('Tre angoli','Penna in alto, dove si aggancia la drizza; mura in basso a prua; scotta, o bugna, in basso a poppa, tra base e balumina, dove lavora il tesabase.')+sterm('Tre lati','Inferitura lungo l\'albero, con la ralinga nella canaletta; base lungo il boma; balumina, il lato libero, con le tasche delle stecche.')+sterm('Il fiocco','Stessi nomi. L\'inferitura si aggancia allo strallo con i garrocci.')+sterm('La corda','La linea che unisce le due estremità del profilo della vela.')
sec('lati', head('Vela · le vele','Lati e angoli delle vele'), pinned=svgp(X,Y,W,Hh,b,'Randa e fiocco con i tre angoli penna, mura e scotta, i tre lati inferitura, base e balumina, le stecche, i garrocci sullo strallo e la corda del profilo')+lbl+pcol(txt,gap=16),
 notes='Materiale della scuola: lati e angoli delle vele. Quiz 2.2.1-12 (angolo di scotta tra base e balumina), -13 e -14 (penna e mura: i falsi scambiano i lati), -9 (la balumina non è il lato più corto), -10 (ralinga nella canaletta dell\'albero), -11 (sulla base non ci sono le tasche delle stecche), 2.3.1-14 (il punto di mura non è sulla varea del boma), 2.2.1-51 (garrocci), 2.1.1-85 (corda).')
X=700

VC=[('fiocco','Fiocco','Non si sovrappone alla randa. Con l\'autovirante la scotta va a una puleggia sull\'albero: in virata non si tocca.',SUN),
    ('genoa','Genoa','Più grande: oltrepassa l\'albero verso poppa. Si riduce con l\'avvolgifiocco; con il cattivo tempo si issa la tormentina.',CORAL),
    ('spi','Spinnaker','Simmetrico, per le andature portanti, con il tangone; il braccio regola la mura. Si raccoglie nella calza.',PURPLE),
    ('genn','Gennaker e code 0','Asimmetrici, senza tangone: il gennaker tra traverso e lasco (60-120°), il code 0 con poco vento dalla bolina larga.',GREEN)]
cc=''.join(card(svgi(320,200,mini(k,hc=c),f'Barca con {t.lower()}',dw=330,dh=206,pan=False)+h3(t,32,c if c!=SUN else INK)+p(d,23),None,22,12) for k,t,d,c in VC)
sec('vele', head('Vela · le vele','Le vele di prua')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Set base dello sloop: randa e genoa. Del catamarano: randa, fiocco e gennaker.',CORAL,34),
 notes='Quiz 2.2.1-15 (il fiocco non limita a 40-70°), -21 (lo spinnaker non è la vela principale né da bolina), -22 (gennaker 60-120°), -23 e -24 (code 0: poco vento, bolina larga-traverso; non è inferito), -49 e -50 (set di vele), -64 e -65 (manovre dello spinnaker: il braccio regola la mura), -80 (la calza), -81 e -82 (fiocco autovirante), 2.3.1-35 e -36 (strallare e quadrare il tangone), -25 (la tormentina non serve a rallentare risalendo il vento).')

def catamaran(x0,wl,L,hc=BLUE):
    s=f'<path d="M{x0+L*0.03:.0f} {wl-0.06*L:.0f} L{x0+L*0.98:.0f} {wl-0.07*L:.0f} Q{x0+L*0.95:.0f} {wl+0.02*L:.0f} {x0+L*0.85:.0f} {wl+0.02*L:.0f} L{x0+L*0.08:.0f} {wl+0.02*L:.0f} Z" fill="#DDE6EC" stroke="{NAVY}" stroke-width="2" transform="translate({0.05*L:.0f} {-0.03*L:.0f})"/>'
    s+=f'<path d="M{x0:.0f} {wl-0.06*L:.0f} L{x0+L:.0f} {wl-0.07*L:.0f} Q{x0+L*0.96:.0f} {wl+0.02*L:.0f} {x0+L*0.86:.0f} {wl+0.025*L:.0f} L{x0+L*0.06:.0f} {wl+0.025*L:.0f} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
    s+=f'<rect x="{x0+L*0.3:.0f}" y="{wl-0.13*L:.0f}" width="{L*0.35:.0f}" height="{0.07*L:.0f}" rx="8" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
    mx_=x0+L*0.5; mt_=wl-0.8*L; md=wl-0.13*L
    s+=line(mx_,md,mx_,mt_,INK,4)+f'<path d="M{mx_-3:.0f} {mt_+8:.0f} L{mx_-3:.0f} {md-12:.0f} L{x0+L*0.12:.0f} {md-12:.0f} Q{x0+L*0.22:.0f} {mt_+0.3*L:.0f} {mx_-3:.0f} {mt_+8:.0f} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2.5"/>'
    s+=f'<path d="M{mx_+4:.0f} {mt_+0.12*L:.0f} L{x0+L*0.95:.0f} {wl-0.08*L:.0f} L{mx_+0.08*L:.0f} {md-8:.0f} Z" fill="{hc}" stroke="{NAVY}" stroke-width="2.5"/>'
    return s
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
for i,(rg,hd) in enumerate((('sloop','genoa'),('cutter',''),('ketch','fiocco'))):
    s,_=yacht(20+i*268,490,235,hd,rg,'#FFFFFF',[CORAL,PURPLE,GREEN][i],NAVY,3); b+=s
b+=catamaran(20+3*268,490,235)
b+=f'<rect x="0" y="490" width="1092" height="130" fill="{WATER}" fill-opacity="0.45"/>'+line(0,490,1092,490,SEA,3)
lbl=''.join(pill(X+20+i*268+40,Y+560,160,t,c,24,align='center') for i,(t,c) in enumerate((('sloop',CORAL),('cutter',PURPLE),('ketch',GREEN),('catamarano',BLUE))))
txt=sterm('Il piano velico','È l\'organizzazione delle vele come da progetto: lo caratterizzano il numero di alberi e il tipo di vele. Lo scafo è la struttura galleggiante e portante.')+sterm('Sloop e cutter','Un albero. Lo sloop porta una sola vela di prua alla volta (set base: randa e genoa); il cutter due fiocchi insieme.')+sterm('Ketch','Due alberi: la mezzana, più piccola, sta a proravia dell\'asse del timone.')+sterm('Catamarano','Un albero e due scafi; set di randa, fiocco e gennaker. Il multiscafo è più stabile.')
sec('armi', head('Vela · le vele','Il piano velico')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Quattro barche a confronto: sloop con randa e genoa, cutter con due vele di prua, ketch con albero di maestra e di mezzana, catamarano con due scafi')+lbl,
 notes='Materiale della scuola: piano velico. Quiz 2.1.1-72 (piano velico: numero di alberi e tipo di vele), 2.1.1-2 (scafo), 2.2.1-25 (sloop), -26 (cutter), -27 (ketch: mezzana a proravia dell\'asse del timone), -49 e -50 (set di vele del catamarano e dello sloop), 2.1.1-45 (il multiscafo ha maggiore stabilità: di forma; ma se si capovolge non si raddrizza da solo). Lo yawl, non in banca, ha la mezzana a poppavia del timone.')

up=f'<rect x="0" y="0" width="300" height="150" fill="#F4FAFC"/>'+line(130,8,130,146,INK,6)+line(130,132,280,132,INK,6)+f'<path d="M136 60 L136 126 L250 126 Q190 96 136 60 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'+arrow(96,130,96,40,CORAL,6,18)+line(112,10,136,60,SEA,3)+''.join(line(40+i*14,90,40+i*14+30,132,PURPLE,2) for i in range(3))
gar=f'<rect x="0" y="0" width="300" height="150" fill="#F4FAFC"/>'+line(40,146,250,8,NAVY,4)+f'<path d="M46 146 L244 18 L170 146 Z" fill="{SUN}" fill-opacity="0.8"/>'+''.join(f'<circle cx="{40+t*210:.0f}" cy="{146-t*138:.0f}" r="7" fill="none" stroke="{CORAL}" stroke-width="4"/>' for t in (0.15,0.4,0.65,0.9))+arrow(60,100,150,40,CORAL,4,12)
ra=box('La randa',svgi(300,150,up,'Randa issata con la drizza, la ralinga nella canaletta e i lazy jack',dw=420,dh=210,pan=False)+lst(['la drizza si aggancia alla penna con un moschettone impiombato; il grillo di penna ha il perno imperdibile, così non cade in mare','la ralinga scorre nella canaletta dell\'albero','i lazy jack sono le sagole che la raccolgono sul boma quando si ammaina'],23),CORAL,CORAL_T)
ge=box('Genoa e fiocco',svgi(300,150,gar,'Fiocco con i garrocci incocciati allo strallo dalla mura verso la penna',dw=420,dh=210,pan=False)+lst(['si armano allo stesso modo: stessa mura, stesso strallo','con i garrocci: prima la mura, poi i garrocci dalla mura verso la penna, infine le scotte alla bugna con la gassa d\'amante','con lo strallo cavo: l\'inferitura entra nella canaletta aiutata dal feeder; la doppia canaletta serve a cambiare vela'],23),SEA,SEA_T)
sv=f'<p style="font-size:24px; line-height:1.35; font-weight:700; color:{INK}; background:{SUN_T}; padding:14px 20px; border-radius:20px">Si issa con la prua al vento: la vela resta sventata e non si gonfia. Sventare vuol dire portare la prua al vento o mollare le scotte, così le vele non portano; non è mettere la poppa al vento.</p>'
sec('armare', head('Vela · le vele','Armare le vele')+f'<div style="display:flex; gap:24px">{ra}{ge}</div>'+sv,
 notes='Materiale della scuola: armare le vele. Quiz 2.3.1-20 (drizza con moschettone impiombato), 2.2.1-79 (grillo di penna con perno di blocco), 2.2.1-10 (ralinga), -60 e -61 (lazy jack: sagole per raccogliere la randa, non una drizza d\'emergenza), 2.3.1-13 e -15 (la randa non si arma con la borosa sulla mura né con la tavoletta nel meolo), -17 (genoa e fiocco si armano allo stesso modo), -18 (prima operazione: la mura, non la bugna), -19 (garrocci dalla mura verso la penna), -21 (scotte: non il parlato doppio), -22 (prua al vento), -23 e -24 e 2.2.1-62 (strallo cavo e feeder), 2.3.1-1, -2, -39 (sventare).', gap=24)

# =====================================================================
# CAPITOLO 3 · LA TEORIA
# =====================================================================
# ============ ANDATURE ============
X=128
cx,cy,R=546,330,190
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
a0,a1=-45,45
p0=pol(cx,cy,a0,300); p1=pol(cx,cy,a1,300)
b+=f'<path d="M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A300 300 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{LRED}" fill-opacity="0.15"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#C9D3DD" stroke-width="3" stroke-dasharray="10 8"/>'
b+=''.join(windarrow(x,4,60) for x in (cx-60,cx,cx+60))
for hd in (45,90,135,180,225,270,315):
    sa={45:12,90:45,135:65,180:85,225:65,270:45,315:12}[hd]; side=1 if hd<=180 else -1
    x,y=pol(cx,cy,hd,R); b+=topsail(x,y,130,hd,sa,side)
b+=f'<circle cx="{cx}" cy="{cy}" r="12" fill="{NAVY}"/>'
lbl=''
for hd,t,c,dx,dy in ((45,'bolina · 45°',CORAL,70,-40),(90,'traverso · 90°',SEA,80,-18),(135,'lasco · 135°',PURPLE,70,10),(180,'poppa · 180°',BLUE,50,20)):
    x,y=pol(cx,cy,hd,R); lbl+=pill(X+x+dx,Y+y+dy,220,t,c,22)
lbl+=pill(X+cx-100,Y+92,200,'angolo morto',LRED,22,align='center')+lab(X+cx-260,Y+14,160,'vento',SOFT,24,900,'right')
lbl+=pill(X+40,Y+560,230,'mure a dritta',NAVY,22)+pill(X+850,Y+560,230,'mure a sinistra',NAVY,22)
txt=term('Andatura','È la direzione della barca rispetto al vento, non la sua velocità: bolina circa 45°, traverso 90°, lasco circa 135°, poppa o fil di ruota 180°.')+term('Angolo morto','Il settore controvento dove le vele non portano: è il settore di bordeggio, non una zona dello scafo. Per risalire si bordeggia a zig-zag.')+term('Mure','Il lato da cui prende il vento: dritta o sinistra; l\'altro lato è sottovento. Non è il lato dove frangono le onde.')
sec('andature', head('Vela · la teoria','Le andature'), pinned=svgp(X,Y,W,Hh,b,'Rosa delle andature: vento da nord, angolo morto in rosso, barche di bolina, traverso, lasco e poppa con mure a dritta a sinistra del disegno e mure a sinistra a destra')+lbl+pcol(txt),
 notes='Quiz 2.1.1-6, -7, -49 (definizione di andatura: attenzione, -49 è Falso perché dice «direzione verso cui procede» senza riferirsi al vento reale come nella -6), -16…-19 e -50…-54 (angoli delle andature), -24, -25, -57 (settore di bordeggio o angolo morto), -68 e -69 (sopravento e sottovento), -70 (le mure non sono il lato dove frangono le onde), 2.3.1-50 (stringere oltre l\'angolo di bordeggio per rallentare), -51 (poggiando da bolina stretta a larga si accelera). Tra lasco e poppa: gran lasco e giardinetto.')
X=700

# ============ VENTO APPARENTE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'+line(546,40,546,580,'#C9D3DD',3)
def tri(ox,oy,hd,s_,R_=200):
    vr=(0,R_); h=math.radians(hd); vv=(-s_*math.sin(h), s_*math.cos(h)); va=(vr[0]+vv[0],vr[1]+vv[1])
    e=arrow(ox,oy,ox+vr[0],oy+vr[1],NAVY,7,22)+arrow(ox+vr[0],oy+vr[1],ox+va[0],oy+va[1],CORAL,7,22)+arrow(ox,oy,ox+va[0],oy+va[1],PURPLE,10,28)
    return e,va
e1,va1=tri(330,110,45,130); b+=e1+topsail(200,470,150,45,15,1)
b+=arrow(820,110,820,310,NAVY,7,22)+dash(820,310,880,310,SOFT,2)+arrow(880,310,880,200,CORAL,7,22)+dash(880,200,760,200,SOFT,2)+arrow(760,110,760,200,PURPLE,10,28)
b+=topsail(820,470,150,180,85,1)
lbl=pill(X+40,Y+30,420,'Di bolina: più forte, più a prua',PURPLE,24)+pill(X+586,Y+30,380,'In poppa: più debole',PURPLE,24)
lbl+=lab(X+340,Y+180,160,'reale',NAVY,24,900)+lab(X+300,Y+370,200,'di velocità',CORAL,24,900)+lab(X+130,Y+230,160,'apparente',PURPLE,26,900)
lbl+=lab(X+832,Y+120,160,'reale',NAVY,24,900)+lab(X+896,Y+236,200,'di velocità',CORAL,24,900)+lab(X+590,Y+136,160,'apparente',PURPLE,26,900,'right')
txt=term('Tre venti','Il reale soffia sul mare; quello di velocità nasce dal moto della barca, contrario alla rotta. La loro somma è l\'apparente: quello che senti e su cui si regolano le vele.')+term('Sempre più a prua','L\'apparente arriva sempre più da prua del reale. Di bolina è più forte del reale, in poppa più debole: in poppa sembra di andare piano.')+term('La raffica','Un rinforzo del reale sposta l\'apparente verso poppa: si può orzare e stringere di più.')
sec('apparente', head('Vela · la teoria','Il vento apparente')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Somma dei vettori: di bolina il vento reale più il vento di velocità dà un apparente più forte e più a prua; in poppa l\'apparente è più debole del reale')+lbl,
 notes='Quiz 2.1.1-8…-11 (a favore di vento l\'apparente è la differenza, controvento la somma), -12 e -13 (sempre più a proravia del reale), -14 e -15 (più forte quanto più si va verso il vento), -20…-23, -55, -56 (di bolina sembra di andare veloci, in poppa piano), -26 e -27 (la raffica porta l\'apparente verso poppa: si può orzare), -36 (la messa a segno delle vele dipende dall\'apparente), -74 (svergolamento: il vento reale aumenta con l\'altezza). Il vento di velocità ha la stessa intensità della velocità della barca e verso opposto.')

# ============ PORTANZA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
bx,byc=420,330; L=520
b+=topboat(bx,byc,L,-90,'#FFFFFF',NAVY,4,1,False)
mxp,myp=bx,byc-0.12*L
ex,ey=bx+62,byc+0.3*L
for k in range(-3,4):
    ox=260+k*95; oy=40
    b+=f'<path d="M{ox-40} {oy-60} L{ox+220} {oy+390}" fill="none" stroke="{SEA}" stroke-width="3" stroke-dasharray="14 10" stroke-opacity="0.5"/>'
b+=f'<path d="M{mxp} {myp} Q{mxp+75} {(myp+ey)/2:.0f} {ex} {ey:.0f}" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>'
b+=dash(mxp,myp,ex,ey,NAVY,3)
fc=(mxp+48,(myp+ey)/2-10)
F=(200,-115)
b+=arrow(fc[0],fc[1],fc[0]+F[0],fc[1]+F[1],PURPLE,9,28)+arrow(fc[0],fc[1],fc[0],fc[1]+F[1],GREEN,8,24)+arrow(fc[0],fc[1],fc[0]+F[0],fc[1],CORAL,8,24)
b+=dash(fc[0],fc[1]+F[1],fc[0]+F[0],fc[1]+F[1],SOFT,2)+dash(fc[0]+F[0],fc[1],fc[0]+F[0],fc[1]+F[1],SOFT,2)
b+=arrow(80,110,190,300,NAVY,8,26)
b+=''.join(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="46" font-weight="700" fill="{c}">{t}</text>' for x,y,t,c in ((350,380,'+',BLUE),(560,470,'−',LRED)))
lbl=lab(X+40,Y+30,300,'vento apparente',NAVY,24,900)+pill(X+fc[0]+F[0]+20,Y+fc[1]+F[1]-20,260,'forza della vela',PURPLE,24)
lbl+=pill(X+fc[0]-180,Y+fc[1]+F[1]-60,200,'propulsione',GREEN,24)+pill(X+fc[0]+F[0]+20,Y+fc[1]-16,200,'scarroccio',CORAL,24)
lbl+=lab(X+180,Y+420,200,'sopravento',BLUE,24,900)+lab(X+590,Y+470,380,'sottovento: depressione',LRED,24,900)+lab(X+600,Y+540,300,'corda della vela (tratteggio)',NAVY,22,800)
txt=term('Un\'ala','L\'aria scorre sui due lati della vela: sopravento spinge, sottovento si crea una depressione che la «aspira». È la portanza.')+term('Angolo di incidenza','Tra il vento apparente e la vela: decide quanta pressione la vela riceve.')+term('Due componenti','La forza si divide in propulsione, parallela all\'asse della barca, e scarroccio, perpendicolare. Bulbo e deriva si oppongono allo scarroccio.')
sec('portanza', head('Vela · la teoria','Come spinge la vela'), pinned=svgp(X,Y,W,Hh,b,'Barca vista dall\'alto di bolina: il vento apparente scorre sulla vela curva, sopravento pressione e sottovento depressione; la forza della vela si scompone in propulsione in avanti e scarroccio di lato')+lbl+pcol(txt),
 notes='Quiz 2.1.1-5 (la vela si orienta rispetto al flusso del vento), -28 e -96 (angolo di incidenza), -37 e -38 (la pressione dipende dall\'angolo di incidenza), -39, -40, -83, -84 (propulsione parallela all\'asse, scarroccio perpendicolare, entrambe dalla forza sulla vela), -78 (scarroccio), -58 (il lato sottovento è in depressione), -48 (la vela non si pone da sola a 45°), -73 (la portanza non è un peso), -85 (corda), -86 (la concavità non riduce la resistenza all\'avanzamento), -71 (grasso), -80 (smagrire), -35 e 2.3.1-33 (planata).')
X=700

X=700
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="380" width="1092" height="240" fill="{WATER}" fill-opacity="0.45"/>'+line(0,380,1092,380,SEA,3)
g=f'<path d="M-140 -30 L140 -30 Q130 40 60 62 L-60 62 Q-130 40 -140 -30 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
g+=line(0,-30,0,-330,INK,7)+f'<path d="M6 -320 Q40 -180 8 -40" fill="none" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/>'
g+=f'<rect x="-9" y="62" width="18" height="130" fill="{NAVY}"/><ellipse cx="0" cy="200" rx="46" ry="18" fill="{NAVY}"/>'
b+=f'<g transform="translate(546 380) rotate(20)">{g}</g>'
bx_=546-200*math.sin(math.radians(20)); by_=380+200*math.cos(math.radians(20))
b+=''.join(arrow(60,y,260,y,GREY,8,24) for y in (120,190,260))+arrow(bx_,by_,bx_,by_+50,PURPLE,7,20)+arrow(600,430,600,330,SEA,7,20)
b+=dpath('M820 250 Q790 110 660 90',GREEN,6,False)+arrow(690,88,640,92,GREEN,6,20)
lbl=lab(X+60,Y+70,220,'vento: fa sbandare',SOFT,22,900)+pill(X+bx_-260,Y+by_-10,200,'peso del bulbo',PURPLE,22)+pill(X+620,Y+300,250,'spinta dell\'acqua',SEA,22)+pill(X+700,Y+40,280,'coppia che raddrizza',GREEN,22)
txt=sterm('Il bulbo zavorrato','Il peso in fondo alla chiglia: quando la barca sbanda crea una coppia che la raddrizza. Dà stabilità e contrasta il vento; non serve ad andare più veloci.')+sterm('Lo sbandamento','Troppo sbandata la barca va più piano e diventa orziera. Il peso dell\'equipaggio sopravento aiuta; se la falchetta resta in acqua si riduce la vela.')+sterm('Il multiscafo','Sta dritto per la sua larghezza: è più stabile, ma se si capovolge non torna su. Si scuffia quando l\'albero va in acqua, anche fino a 180°.')
sec('stabilita', head('Vela · la teoria','La stabilità')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Sezione di una barca a vela sbandata dal vento: il peso del bulbo zavorrato tira in basso e la spinta dell\'acqua in alto, formando una coppia che la raddrizza')+lbl,
 notes='Materiale della scuola: stabilità e scarroccio. Quiz 2.1.1-3 e -46, -47 (il bulbo zavorrato dà stabilità e contrasta le azioni esterne; non serve alla velocità), -91 (troppo sbandata va più piano), -87…-90 (pesi dell\'equipaggio), -45 (multiscafo più stabile), -79 (scuffia), 2.3.1-60 (falchetta in acqua: ridurre). La scuola dice che la stabilità è assicurata dal bulbo: è la risposta del quiz. Conta anche la forma dello scafo: più largo, più stabile all\'inizio. Lo scarroccio e le forze sono nella slide precedente.')

# ============ EQUILIBRIO ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'; cvl=''
for i,(dx,t,c) in enumerate(((0.07,'poggiera',CORAL),(0,'neutra',SEA),(-0.07,'orziera',PURPLE))):
    x0=40+i*350; s,P2=yacht(x0,440,300,'genoa','sloop','#FFFFFF',SUN,NAVY,2.5); b+=s
    cdx=P2['kx']; cvx=cdx+dx*300*1.6; cvy=P2['dm']-0.22*300
    b+=dash(cvx,cvy,cvx,560,c,3)+dash(cdx,P2['kb']+10,cdx,560,NAVY,3)
    cvl+=pill(X+cvx-80,Y+cvy-17,60,'CV',c,20)+pill(X+cdx+18,Y+P2['kb']+30,60,'CD',NAVY,20)
    b+=f'<circle cx="{cvx:.1f}" cy="{cvy:.1f}" r="14" fill="{c}" stroke="#FFFFFF" stroke-width="4"/><circle cx="{cdx:.1f}" cy="{P2["kb"]+18:.1f}" r="12" fill="{NAVY}" stroke="#FFFFFF" stroke-width="4"/>'
b+=f'<rect x="0" y="440" width="1092" height="180" fill="{WATER}" fill-opacity="0.45"/>'+line(0,440,1092,440,SEA,3)
lbl=''.join(pill(X+40+i*350+70,Y+24,180,t,c,26,align='center') for i,(t,c) in enumerate((('poggiera',CORAL),('neutra',SEA),('orziera',PURPLE))))
lbl+=cvl+''.join(lab(X+40+i*350,Y+566,320,t,NAVY,22,800,'center') for i,t in enumerate(('CV a proravia del CD','CV sopra il CD','CV a poppavia del CD')))
txt=term('Due centri','Centro velico (CV): dove si applica la spinta del vento sulle vele. Centro di deriva (CD): dove si applica la resistenza laterale dell\'opera viva.')+term('Tendenze','CV a proravia: la barca poggia. A poppavia: orza. Allineati: neutra. La randa spinge a orzare, il fiocco a poggiare; albero inclinato a prua: poggiera, a poppa: orziera.')+term('La scelta giusta','Leggermente orziera: più sicura e veloce. Ridurre la randa toglie orziera; se è poggiera si spostano i pesi a prua, e il CD va avanti.')
sec('equilibrio', head('Vela · la teoria','Centro velico e centro di deriva')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Tre barche a confronto con il centro velico e il centro di deriva: poggiera con il centro velico a proravia, neutra con i centri allineati, orziera con il centro velico a poppavia')+lbl,
 notes='Materiale della scuola: centro velico e centro di deriva. Quiz 2.1.1-29, -59, -60 (centro velico), -30, -61, -62, -67 (centro di deriva), -31, -32, -33, -63…-66 (tendenze: CV a proravia = poggiera, allineati = neutra), -34 e -66 (da cosa dipende la posizione del CV), -41, -42, -93, -94 (inclinazione dell\'albero), -97 (randa orziera, genoa poggiero), -87…-92 (pesi dell\'equipaggio, pesi a prua contro la tendenza poggiera, meglio leggermente orziera; troppo sbandata di bolina va più piano), 2.3.1-58 (ridurre la randa diminuisce la tendenza orziera).')

def prof(depth,c):
    return f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+arrow(20,30,100,60,GREY,6,18)+f'<path d="M60 130 Q180 {130-depth} 320 110" fill="none" stroke="{c}" stroke-width="12" stroke-linecap="round"/>'+dash(60,130,320,110,NAVY,2)
twist=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+''.join(arrow(20,y,20+l,y,GREY,5,14) for y,l in ((30,150),(70,115),(110,85),(150,60)))+f'<path d="M250 10 L250 160 L330 160 Q300 80 250 10 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'+dash(250,40,310,20,CORAL,3)
RC=[(prof(30,CORAL),'Vento forte: smagrire','Meno concavità, meno potenza, meno sbandamento: si cazzano cunningham (o drizza randa), tesabase e drizza della vela di prua; il carrello del genoa va a poppa; in raffica il carrello randa va sottovento o si lasca la scotta; cazzando il paterazzo si smagrisce la parte centrale della randa.',CORAL_T),
    (prof(80,SEA),'Vento debole: ingrassare','Si lascano drizza e base: più concavità, più potenza; è la forma per il fil di ruota. Drizze e base più cazzate di bolina, più lasche nelle andature larghe.',SEA_T),
    (twist,'Di bolina e in alto','Stringendo il vento si rallenta; poggiando da bolina stretta a larga si accelera. Il vento cresce con l\'altezza: la parte alta della vela si svergola.',LILAC_T)]
cc=''.join(card(svgi(360,170,s_,t,dw=484,dh=228,pan=False)+h3(t,30)+p(d,23),bg,26,10) for s_,t,d,bg in RC)
sec('regolazioni', head('Vela · la teoria','Regolare le vele')+f'<div style="display:flex; gap:24px">{cc}</div>'+note('La pressione sulla vela dipende dall\'angolo di incidenza, tra il vento apparente e la vela.',PURPLE,32),
 notes='Materiale della scuola: regolazione vele. Quiz 2.1.1-37 e -96 (angolo di incidenza), -98 e 2.3.1-52 (vento in aumento: cunningham, tesabase, drizza genoa cazzati, punto di scotta del genoa arretrato), 2.3.1-53 (non si smagrisce per aumentare la potenza), -55 (raffica: carrello sottovento o scotta lascata), 2.2.1-53 (paterazzo), 2.1.1-95 (lascare drizza e base: grasso, fil di ruota), 2.3.1-8 e -16 (base più o meno cazzata secondo l\'andatura), -50 e -51 (stringere rallenta, poggiare da bolina stretta a larga accelera), 2.1.1-74 (svergolamento), -71 (il grasso non è la parte vicina alla drizza), -80 (smagrire).', gap=24)
# =====================================================================
# CAPITOLO 4 · LE MANOVRE
# =====================================================================
# ============ ORZARE E POGGIARE ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'+line(546,40,546,580,'#C9D3DD',3)
b+=''.join(arrow(20,y,120,y,GREY,7,22) for y in (200,330))
def tillerboat(cx,cy,sgn,c,label_turn):
    s=topsail(cx,cy,300,0,45,1)
    sx_,sy_=cx,cy+150
    tx,ty=sx_+sgn*60,sy_-100
    s+=line(sx_,sy_,tx,ty,INK,9)+f'<circle cx="{tx}" cy="{ty}" r="10" fill="{c}"/>'
    s+=arrow(tx,ty,tx+sgn*50,ty,c,5,16)
    s+=curved(cx,cy-120,70,-90-10,-90-10+sgn*(-1)*-70,c,6) if False else ''
    ang0=-100 if sgn<0 else -80; ang1=ang0+(60 if sgn<0 else -60)
    s+=curved(cx,cy-60,120,ang0,ang1,c,7)
    return s
b+=tillerboat(300,330,-1,CORAL,'')+tillerboat(800,330,1,PURPLE,'')
lbl=pill(X+100,Y+30,400,'Poggiare: barra sopravento',CORAL,24)+pill(X+600,Y+30,400,'Orzare: barra sottovento',PURPLE,24)
lbl+=lab(X+60,Y+560,440,'la prua si allontana dal vento',CORAL,22,800)+lab(X+590,Y+560,440,'la prua va verso il vento',PURPLE,22,800)+lab(X+10,Y+140,120,'vento',SOFT,22,900)
txt=term('Orzare e poggiare','Orzare: portare la prua verso il vento. Poggiare: allontanarla, lascando le vele. La barra va dalla parte opposta a dove vuoi andare.')+term('Aiutarsi con le vele','Lascare la randa aiuta a poggiare; cazzarla aiuta a orzare.')+term('Stringere il vento','Orzare il più possibile con le vele cazzate. Il contrario, poggiare, è allontanare la prua lascando le vele; orzare non vuol dire mettersi controvento.')
sec('barra', head('Vela · le manovre','Orzare e poggiare'), pinned=svgp(X,Y,W,Hh,b,'Due barche al traverso con il vento da sinistra: con la barra spinta sopravento la prua poggia, con la barra portata sottovento verso la randa la prua orza')+lbl+pcol(txt),
 notes='Quiz 2.3.1-3 e -4 (per poggiare barra sopravento, opposta alla randa), -42 (non con la barra al centro), -37 e -38 (poggiare e orzare), 2.1.1-81 e -82 (stringere il vento e poggiare), 2.3.1-65 (lascare la randa agevola la poggiata), -56 (per una poggiata rapida non basta lascare il fiocco), 2.3.1-1, -2, -39 (sventare), 2.1.1-75 e -76 (straorza e strapoggia), -79 (scuffia).')
X=700

# ============ VIRATA E ABBATTUTA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'+line(546,120,546,590,'#C9D3DD',3)
b+=''.join(windarrow(x,10,80) for x in (516,576))
b+=dpath('M120 590 L360 330 Q385 300 355 275 L120 90',CORAL,5)
b+=topsail(190,510,120,43,12,1)+topsail(190,160,120,317,12,-1)
b+=dpath('M640 110 L880 330 Q905 360 875 385 L650 590',PURPLE,5)
b+=topsail(720,180,120,137,70,1)+topsail(730,510,120,223,70,-1)
b+=f'<circle cx="372" cy="298" r="12" fill="{CORAL}"/><circle cx="893" cy="358" r="12" fill="{PURPLE}"/>'
lbl=pill(X+30,Y+24,440,'Virata: la prua passa nel vento',CORAL,22)+pill(X+620,Y+24,450,'Abbattuta: la poppa passa nel vento',PURPLE,22)
lbl+=lab(X+260,Y+510,220,'mure a sinistra',NAVY,22,800)+lab(X+260,Y+150,220,'mure a dritta',NAVY,22,800)+lab(X+790,Y+170,220,'mure a sinistra',NAVY,22,800)+lab(X+800,Y+500,220,'mure a dritta',NAVY,22,800)
txt=term('Cambiare mure','Si fa in due modi: con la virata (prua nel vento, per risalire) o con l\'abbattuta (poppa nel vento, nelle andature portanti).')+term('L\'abbattuta','Si cazza la randa al centro, si passa la poppa nel vento, poi si lasca sull\'altro bordo. Non alla massima velocità di bolina o al traverso.')+term('La strambata','L\'abbattuta involontaria e incontrollata: rischio al gran lasco e in poppa, si previene con la ritenuta del boma. Straorza e strapoggia: scarti improvvisi della prua per raffica od onda.')
sec('virata', head('Vela · le manovre','Virata e abbattuta')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Traiettorie viste dall\'alto: nella virata la barca risale il vento e passa con la prua nel vento; nell\'abbattuta scende col vento e passa con la poppa nel vento')+lbl,
 notes='Quiz 2.3.1-9 (abbattuta: la poppa attraversa il vento), -10, -11, -41 (a cosa non serve la virata), -12 (l\'abbattuta non si fa alla massima velocità di bolina o al traverso), -40 (virata e abbattuta: le manovre per cambiare mure), -57 (ritenuta del boma contro la strambata al granlasco e al giardinetto), -61, -62, -63 (strambata: abbattuta involontaria), 2.2.1-81 (con il fiocco autovirante in virata non si cazza la scotta). Straorza 2.1.1-75, strapoggia -76, scuffia -79; la virata non serve a evitare ostacoli né ad ammainare lo spi. Comandi: «pronti a virare», «vira»; «pronti ad abbattere», «abbatti».')

heel=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/><rect x="0" y="110" width="360" height="60" fill="{WATER}" fill-opacity="0.45"/><g transform="translate(180 110) rotate(35)"><path d="M-90 -6 L90 -6 Q80 24 40 30 L-40 30 Q-80 24 -90 -6 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>{line(0,-6,0,-140,INK,5)}<path d="M4 -130 L4 -12 L70 -12 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="2"/></g>'+''.join(f'<path d="M{20+i*60} 120 q15 -8 30 0" fill="none" stroke="#FFFFFF" stroke-width="3"/>' for i in range(6))
reef=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+line(150,10,150,165,INK,6)+line(150,140,320,140,INK,6)+f'<path d="M156 40 L156 134 L312 134 Q230 90 156 40 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M156 140 L312 140 L312 154 L156 154 Z" fill="{CORAL_T}" stroke="{CORAL}" stroke-width="3"/>'+''.join(f'<circle cx="{x}" cy="147" r="4" fill="{CORAL}"/>' for x in range(180,310,26))+line(312,134,330,140,PURPLE,4)
panna=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+arrow(30,10,30,90,GREY,7,22)+f'<g transform="translate(200 90) rotate(-45)"><path d="M100 0 Q40 -20 -84 -16 L-100 -12 L-100 12 L-84 16 Q40 20 100 0 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M46 0 Q20 -26 -10 -30" fill="none" stroke="{SUN}" stroke-width="8" stroke-linecap="round"/><path d="M12 0 Q-30 22 -70 36" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/></g>'
IC=[(heel,'Quando ridurre','Se cominci a chiederti se ridurre, è il momento. Con la falchetta stabilmente in acqua si va più piano, non più forte. Ridurre la randa toglie anche tendenza orziera.',GREEN_T),
    (reef,'I terzaroli','Si ammaina in parte la randa, si fissa la nuova mura e con la borosa la nuova bugna; i matafioni legano la parte ripiegata. Non si cambia vela: il matafione è una cima, non una randa o un fiocco di rispetto.',CORAL_T),
    (panna,'Panna e cappa','Panna: fiocco a collo, randa per la bolina larga, timone all\'orza: la barca resta quasi ferma. Cappa: con l\'ancora galleggiante filata da prua. Nessuna delle due serve ad andare più veloci.',LILAC_T)]
cc=''.join(card(svgi(360,170,s_,t,dw=484,dh=228,pan=False)+h3(t,30)+p(d,23),bg,26,10) for s_,t,d,bg in IC)
sec('terzaroli', head('Vela · le manovre','Terzaroli, panna e cappa')+f'<div style="display:flex; gap:24px">{cc}</div>'+note('Genoa avvolto oltre il 30%: il profilo perde efficienza. Con il cattivo tempo si issa la tormentina, che non serve a risalire il vento.',PURPLE,32),
 notes='Materiale della scuola: terzaroli e panna. Quiz 2.3.1-59 e -60 (quando ridurre), -58 (meno randa, meno orziera), -30 e -31 (terzaroli: non si abbassa il tangone, non si cambia randa; il matafione non è una vela), 2.2.1-68 (la borosa non è sullo strallo cavo), -34 (il tesabase non è sulla base del fiocco), 2.3.1-27 e -28 (panna: non per aumentare la velocità), -29 (cappa: ancora galleggiante da prua, non da poppa; vedi lezione 6), -25 e -26 (tormentina e fileggiare), 2.2.1-83 (genoa ridotto oltre il 30%).')
# ============ PRECEDENZE ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'+line(546,40,546,580,'#C9D3DD',3)
b+=''.join(windarrow(x,10,80) for x in (240,300,800,860))
b+=dpath('M150 470 L275 345 L410 210',GREY,3)+dpath('M420 470 L285 335 L150 200',GREY,3)
b+=dpath('M150 470 Q300 420 470 330',CORAL,5)
b+=topsail(150,470,120,45,12,1,main=CORAL)+topsail(420,470,120,315,12,-1,main=GREEN)
b+=dpath('M700 360 Q740 260 700 160',CORAL,5)
b+=topsail(700,360,120,45,12,1,main=CORAL)+topsail(850,480,120,45,12,1,main=GREEN)
lbl=pill(X+40,Y+120,460,'Mure diverse: le mure a dritta passano',NAVY,22)+pill(X+586,Y+120,480,'Stesse mure: sottovento passa',NAVY,22)
lbl+=pill(X+40,Y+540,250,'mure a sinistra: cede',CORAL,22)+pill(X+300,Y+540,230,'mure a dritta',GREEN,22)
lbl+=pill(X+770,Y+250,280,'sopravento: si scosta',CORAL,22)+pill(X+800,Y+540,200,'sottovento',GREEN,22)
txt=term('Mure diverse','Anche su rotte opposte: chi ha le mure a sinistra lascia la rotta a chi ha le mure a dritta, poggiando e passandole di poppa.')+term('Stesse mure','Chi è sopravento si scosta da chi è sottovento.')+term('Nel dubbio','Con mure a sinistra, se non capisci le mure dell\'altra: lascia libera la rotta. Salvo ordinanze, in porto non si entra a vela.')
sec('precedenze', head('Vela · le manovre','Le precedenze a vela'), pinned=svgp(X,Y,W,Hh,b,'Due situazioni viste dall\'alto con il vento da nord: con mure diverse la barca con mure a sinistra poggia e passa di poppa; con le stesse mure la barca sopravento orza e si scosta da quella sottovento')+lbl+pcol(txt),
 notes='Quiz 2.3.1-5, -45, -46, -47, -48 (mure a dritta ha la precedenza), -7 e -44 (stesse mure: sottovento ha la precedenza, sopravento orza), -49 (nel dubbio lasciare libera la rotta), -6 e -43 (non conta la velocità). È la regola 12 del COLREG: il rapporto tra vela e motore è nella lezione 5. 2.3.1-64 (salvo ordinanze, in porto non si entra a vela).')
X=700

# ============ RIPASSO VELA ============
RV=[('Andature','Bolina 45°, traverso 90°, lasco 135°, poppa 180°. Controvento: angolo morto.',CORAL,CORAL_T),
    ('Vento apparente','Sempre più a prua del reale; di bolina più forte, in poppa più debole.',SEA,SEA_T),
    ('Mure','Il lato da cui entra il vento. Mure a dritta: precedenza.',PURPLE,LILAC_T),
    ('Stesse mure','Chi è sopravento si scosta da chi è sottovento.',BLUE,BLUE_T),
    ('CV e CD','CV a proravia del CD: poggiera. A poppavia: orziera.',GREEN,GREEN_T),
    ('Virata e abbattuta','Prua nel vento, poppa nel vento. La strambata è l\'abbattuta involontaria.',CORAL,SUN_T),
    ('Fisse e correnti','Stralli e sartie reggono l\'albero; drizze e scotte manovrano le vele.',SEA,SEA_T),
    ('Ridurre','Se ci pensi, è il momento: terzaroli e genoa avvolto.',PURPLE,LILAC_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:44px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,26,INK,600,1.35)}</div>' for t,d,c,bg in RV)
sec('ripassovela', head('Vela · ripasso','La vela in otto flash')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div>'+note('Quiz di vela: tutti Vero o Falso. Diffida di «sempre», «solo», «esclusivamente».',PURPLE,36),
 notes='Ripasso della lezione in forma di domande rapide: per ogni riquadro chiedere alla classe prima di scoprirlo. Riferimenti: 2.1.1-16…-24 e -50…-54 (andature), -8…-15 e -20…-23 (vento apparente), 2.3.1-5, -7, -44…-49 (precedenze), 2.1.1-29…-34, -64, -65 (CV e CD), 2.3.1-9, -40, -61…-63 (virata, abbattuta, strambata), 2.2.1-28, -29, -75, -77 (manovre fisse e correnti), 2.3.1-58…-60 (ridurre).')
# =====================================================================
# APERTURE, VERIFICHE, RACCOLTA, CHIUSURA
# =====================================================================
exec(open('apertura.py').read())
FIRST={'cap1':'barca','cap2':'velebase','cap3':'andature','cap4':'barra'}
def chap(id_,n,title,subs,c,mins,art=None):
    chapter(id_,n,title,subs,c,f'Circa {mins} minuti, verifica da 2 quiz compresa: andare spediti, il dettaglio è nelle note.',f'circa {mins} minuti · {len(subs)} argomenti',1,art=art)
    new=slides.pop(); slides.insert([s_[0] for s_ in slides].index(FIRST[id_]),new)
chap('cap1',1,'L\'attrezzatura',['Albero, boma e manovre fisse','Le manovre correnti','La ferramenta di bordo','I nodi'],CORAL,18,art=(ring_scene(),'Illustrazione: salvagente anulare con la sagola galleggiante'))
chap('cap2',2,'Le vele',['Le vele','Lati e angoli delle vele','Le vele di prua','Il piano velico','Armare le vele'],SEA,16)
chap('cap3',3,'La teoria',['Le andature','Il vento apparente','Come spinge la vela','La stabilità','Centro velico e centro di deriva','Regolare le vele'],PURPLE,21,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata'))
chap('cap4',4,'Le manovre',['Orzare e poggiare','Virata e abbattuta','Terzaroli, panna e cappa','Le precedenze a vela','La vela in otto flash'],BLUE,20)
QZ=[('q01','Quiz 1 · Manovre fisse',['2.2.1-6','2.2.1-42','2.2.1-4']),('q02','Quiz 2 · Manovre correnti',['2.2.1-75','2.2.1-33','2.2.1-52']),
 ('q03','Quiz 3 · Ferramenta',['2.2.1-36','2.2.1-70','2.2.1-57']),('q04','Quiz 4 · Nodi e cime',['2.2.1-54','2.2.1-59','2.2.1-67']),
 ('q05','Quiz 5 · Le vele',['2.2.1-48','2.2.1-47','2.1.1-43']),('q06','Quiz 6 · Lati e vele di prua',['2.2.1-10','2.2.1-12','2.2.1-22']),
 ('q07','Quiz 7 · Piano velico e armo',['2.1.1-72','2.2.1-26','2.2.1-61']),('q08','Quiz 8 · Andature',['2.1.1-50','2.1.1-53','2.1.1-7']),
 ('q09','Quiz 9 · Apparente e forze',['2.1.1-22','2.1.1-39','2.1.1-3']),('q10','Quiz 10 · CV, CD e regolazioni',['2.1.1-42','2.1.1-97','2.3.1-52']),
 ('q11','Quiz 11 · Virata e terzaroli',['2.3.1-9','2.3.1-62','2.3.1-31']),('q12','Quiz 12 · Barra e precedenze',['2.3.1-3','2.3.1-7','2.3.1-48'])]
closing(['Manovre fisse (strallo, paterazzo, sartie) reggono l\'albero; le correnti (drizze, scotte, vang, cunningham) manovrano le vele','Vela: penna, mura, scotta; inferitura, base, balumina. Il genoa si sovrappone alla randa, il fiocco no','Bolina 45°, traverso 90°, lasco 135°, poppa 180°; il vento apparente è sempre più a prua del reale','CV a proravia del CD: poggiera; a poppavia: orziera. Vento forte: smagrire; se pensi di ridurre, riduci','Barra sopravento per poggiare; mure a dritta ha la precedenza, con le stesse mure passa chi è sottovento'],
 'Prossima lezione · 10 · Carteggio oltre 12 miglia: navigazione costiera','A casa: i 250 quiz di vela, tutti Vero o Falso, e le prove d\'esame dell\'appendice D con i loro 5 quiz vela.')
raccolta(9,5,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi fino in fondo','Il quesito cambia verso con una parola: «non», «solo», «sempre». Trovala prima di rispondere.'),
  ('Diffida degli assoluti','«Esclusivamente», «sempre», «mai» rendono falsa quasi ogni frase: in vela quasi nulla è assoluto.'),
  ('Cerca lo scambio','Il falso tipico scambia due parole vicine: sopravento e sottovento, orziera e poggiera, fisse e correnti, penna e mura.'),
  ('Un pezzo sbagliato','Se una parte della frase è sbagliata, tutta la frase è falsa: controlla ogni pezzo.')],
 ['Quiz 1-4 · attrezzatura e nodi (12)','Quiz 5-7 · vele e piano velico (9)','Quiz 8-12 · teoria e manovre (15)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz vela, tutti Vero o Falso, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Far rispondere ad alta voce, poi chiedere perché la frase è vera o falsa. Per la simulazione a tempo (5 quesiti, al massimo 1 errore) usare le prove dell\'appendice D.',esame=['vela'])
intermedi([('nodi','v1','Verifica · L\'attrezzatura',['2.2.1-77','2.2.1-35']),
 ('armare','v2','Verifica · Le vele',['2.2.1-18','2.3.1-19']),
 ('regolazioni','v3','Verifica · La teoria',['2.1.1-12','2.1.1-64']),
 ('ripassovela','v4','Verifica · Le manovre',['2.3.1-4','2.3.1-47'])])
write_deck(OUT,'Lezione 09 · Vela',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Albero e manovre fisse, manovre correnti, ferramenta, nodi","start":"cap1"},
  "s3":{"description":"Vele, lati e angoli, vele di prua, piano velico, armare le vele","start":"cap2"},
  "s4":{"description":"Andature, vento apparente, forze, stabilità, centro velico e di deriva, regolazioni","start":"cap3"},
  "s5":{"description":"Orzare e poggiare, virata e abbattuta, terzaroli e panna, precedenze, ripasso","start":"cap4"},
  "s6":{"description":"Raccolta quiz vela","start":"capquiz"}})
