import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez08/project'
GREY='#97A6B4'; SKY='#DDEFF7'; LRED='#E23B3B'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','La barca a vela':'sail','La randa':'sail','Le vele di prua':'sail','Gli armi':'sail',
 'La ferramenta di bordo':'anchor','Le andature':'compass','Il vento apparente':'wind','Come spinge la vela':'wind','Orziera o poggiera':'helm',
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

# ============ COVER + AGENDA ============
cover(8,'Vela: attrezzatura, teoria e manovre','Com\'è fatta una barca a vela, perché va controvento e come si manovra',
 'Lezione 8. Capitoli del programma della scuola: Vela (attrezzatura, teoria e manovre), All. A al DM 323/2021 punto 1c. All\'esame la prova di vela ha 5 quesiti Vero/Falso in più rispetto alla patente a motore: si supera con al massimo 1 errore. Banca ufficiale: 250 quiz (99 teoria, 86 attrezzatura, 65 manovre).')
blocks=[('0:00','40′','Barca, randa, vele di prua, armi, ferramenta · quiz 1',CORAL),('0:40','35′','Andature, vento apparente, portanza, equilibrio, regolazioni · quiz 2',SEA),('1:15','30′','Timone, virata e abbattuta, precedenze, issare e ridurre · quiz 3',PURPLE),('1:45','15′','Verifica finale',BLUE)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">5 V/F</p>'+p('quesiti di vela: al massimo 1 errore',26,INK,700)+p('250 quiz ufficiali, tutti Vero o Falso: attenzione alle parole «sempre», «esclusivamente», «solo».',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>chiamare per nome vele, manovre e ferramenta</li><li>riconoscere le andature e il vento apparente</li><li>spiegare perché la barca risale il vento</li><li>orzare, poggiare, virare e abbattere</li><li>applicare le precedenze tra barche a vela</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 08 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Tre verifiche intermedie da 4 quiz e una finale da 8, tutti dalla banca vela del DD 131/2022: 2.1.1 teoria della vela (99), 2.2.1 attrezzatura (86), 2.3.1 manovre (65). La lezione 9 riprende la vela in un ripasso.')

# ============ LA BARCA ============
s,P_=yacht(180,505,720)
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'+s+f'<rect x="0" y="505" width="1092" height="115" fill="{WATER}" fill-opacity="0.45"/>'+line(0,505,1092,505,SEA,3)
lbl=pill(X+P_['mx']+18,Y+14,110,'albero',NAVY)+pill(X+160,Y+170,150,'paterazzo',NAVY)+pill(X+690,Y+180,120,'strallo',NAVY)
lbl+=pill(X+P_['mx']+30,Y+P_['cro'][1]-18,120,'crocette',NAVY,22)+pill(X+P_['mx']+24,Y+372,100,'sartie',NAVY,22)
lbl+=pill(X+330,Y+300,100,'randa',CORAL)+pill(X+620,Y+310,100,'genoa',CORAL)+pill(X+250,Y+P_['by']+8,90,'boma',PURPLE,22)
lbl+=pill(X+660,Y+462,90,'scafo',SEA)+pill(X+650,Y+568,220,'bulbo zavorrato',SEA,22)+pill(X+80,Y+560,110,'timone',SEA,22)
txt=term('Scafo e bulbo','Lo scafo galleggia e porta tutto. Il bulbo zavorrato sotto la chiglia dà stabilità contro lo sbandamento.')+term('Manovre fisse','Strallo, paterazzo e sartie tengono su l\'albero; le crocette allargano le sartie e le mettono in tensione. In coperta si fissano alle lande.')+term('Manovre correnti','Drizze per issare, scotte per regolare, e poi vang, cunningham, tesabase: servono a manovrare le vele.')
sec('barca', head('Vela · l\'attrezzatura','La barca a vela')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Barca a vela armata a sloop di profilo con albero, boma, randa, genoa, strallo, paterazzo, sartie, crocette, scafo, bulbo e timone')+lbl,
 notes='Colori: blu manovre fisse, corallo vele, viola boma, verde acqua scafo. Quiz 2.1.1-1 e -2 (lo scafo), -3, -46, -47 (bulbo zavorrato e stabilità), 2.2.1-5, -6 (crocette), -69 (sartie), -77, -28, -29, -75 (manovre fisse e correnti), -42 (landa), -45 (trozza), -71 (vang), -52 e -53 (paterazzo: cazzandolo si smagrisce la randa), -1, -2, -3 (armo frazionato e sartie volanti), -72 (sartie e stralli non passano dentro l\'albero), -74 (l\'albero si regola sulle manovre fisse, non correnti).')

# ============ LA RANDA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
mx,top,bm,cl=300,50,500,880
b+=line(mx,20,mx,590,INK,10)+line(mx,bm,cl+40,bm,INK,9)
b+=f'<path d="M{mx+6} {top} L{mx+6} {bm-6} L{cl} {bm-6} Q{mx+330} {top+170} {mx+6} {top} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
def qb(k):
    P0=(cl,bm-6); P1=(mx+330,top+170); P2=(mx+6,top)
    return ((1-k)**2*P0[0]+2*(1-k)*k*P1[0]+k*k*P2[0], (1-k)**2*P0[1]+2*(1-k)*k*P1[1]+k*k*P2[1])
for k in (0.2,0.4,0.6,0.8):
    (x1,y1),(x2,y2)=qb(k-0.01),qb(k+0.01); tx,ty=x2-x1,y2-y1; n=math.hypot(tx,ty); nx,ny=-ty/n,tx/n
    if nx>0: nx,ny=-nx,-ny
    px,py=qb(k); b+=line(px+nx*8,py+ny*8,px+nx*(110 if k<0.7 else 80),py+ny*(110 if k<0.7 else 80),PURPLE,7)
b+=line(mx,bm,mx+110,590,INK,6)+f'<circle cx="{mx}" cy="{bm}" r="12" fill="{CORAL}"/>'
b+=f'<circle cx="{mx+6}" cy="{top}" r="14" fill="{CORAL}"/><circle cx="{mx+6}" cy="{bm-6}" r="14" fill="{CORAL}"/><circle cx="{cl}" cy="{bm-6}" r="14" fill="{CORAL}"/>'
b+=line(mx-12,20,mx-12,top,SEA,4)
lbl=pill(X+mx+30,Y+top-20,330,'angolo di penna · drizza',CORAL)+pill(X+40,Y+bm-80,240,'angolo di mura',CORAL)+pill(X+cl-240,Y+bm+30,330,'angolo di scotta · tesabase',CORAL)
lbl+=pill(X+mx+30,Y+300,340,'inferitura con la ralinga',PURPLE,22)+pill(X+640,Y+160,140,'balumina',PURPLE,22)+pill(X+520,Y+bm-50,90,'base',PURPLE,22)
lbl+=pill(X+700,Y+280,120,'stecche',PURPLE,22)+pill(X+130,Y+bm+10,140,'trozza',NAVY,22)+pill(X+mx+130,Y+560,90,'vang',NAVY,22)+lab(X+50,Y+160,220,'albero con la canaletta',NAVY,22,900)
txt=term('Tre angoli','Penna in alto, dove si aggancia la drizza; mura in basso a prua, vicino alla trozza che unisce boma e albero; scotta in basso a poppa, dove lavora il tesabase.')+term('Tre lati','Inferitura lungo l\'albero, con la ralinga che scorre nella canaletta; base lungo il boma; balumina, il lato libero.')+term('Stecche e vang','Le stecche nelle tasche della balumina tengono la forma della vela; il vang trattiene il boma verso il basso.')
sec('randa', head('Vela · l\'attrezzatura','La randa'), pinned=svgp(X,Y,W,Hh,b,'Randa inferita sull\'albero e sul boma con i tre angoli penna, mura e scotta, i tre lati inferitura, base e balumina, le stecche, la trozza e il vang')+lbl+pcol(txt),
 notes='Quiz 2.2.1-9 (la balumina non è il lato più corto), -10 (ralinga nella canaletta dell\'albero), -11 (base), -12 (angolo di scotta con il tesabase), -13 (penna) e -14 (mura), 2.1.1-43 e -44 (stecche: forma della vela), 2.2.1-16 (la randa è la vela principale, a poppavia dell\'albero), -45 (trozza), -71 (vang: regola la flessione dell\'albero e la superficie portante), -33 (cunningham: tensione della parte prodiera bassa), -79 (grillo della penna con perno di blocco), 2.3.1-14 (il punto di mura non è sulla varea del boma), -20 (drizza con moschettone impiombato), 2.1.1-85 (corda: la linea tra le estremità del profilo).')
X=700

# ============ VELE DI PRUA ============
def mini(head,rig='sloop',hc=SUN,main_c='#FFFFFF'):
    s,_=yacht(30,172,220,head,rig,main_c,hc,NAVY,2)
    return f'<rect x="0" y="0" width="320" height="200" fill="{SKY}"/>'+s+f'<rect x="0" y="172" width="320" height="28" fill="{WATER}" fill-opacity="0.45"/>'
VC=[('fiocco','Fiocco','Non si sovrappone alla randa. Con l\'autovirante la scotta va a una puleggia: in virata non si tocca.',SUN),
    ('genoa','Genoa','Più grande: oltrepassa l\'albero verso poppa, di solito per il 50% della distanza tra albero e mura.',CORAL),
    ('spi','Spinnaker','Simmetrico, per le andature portanti. Si porta con il tangone; il braccio regola la mura.',PURPLE),
    ('genn','Gennaker e code 0','Asimmetrici, senza tangone: il gennaker tra traverso e lasco, il code 0 con poco vento dalla bolina larga.',GREEN)]
cc=''.join(card(svgi(320,200,mini(k,hc=c),f'Barca con {t.lower()}',dw=330,dh=206,pan=False)+h3(t,32,c if c!=SUN else INK)+p(d,24),None,22,12) for k,t,d,c in VC)
sec('vele', head('Vela · l\'attrezzatura','Le vele di prua')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Set base dello sloop: randa e genoa. Del catamarano: randa, fiocco e gennaker. Con il cattivo tempo: la tormentina.',CORAL,34),
 notes='Quiz 2.2.1-15 (il fiocco non limita a 40-70°), -17, -18, -19, -20 (genoa e fiocco: sovrapposizione), -21 (lo spinnaker non è la vela principale né da bolina), -22 (gennaker 60-120°), -23 e -24 (code 0: poco vento, bolina larga-traverso; non è inferito), -49 e -50 (set di vele), -51 (garrocci), -64 e -65 (manovre dello spinnaker: il braccio regola la mura), -80 (la calza), -81 e -82 (fiocco autovirante), -46, -47, -48 (tessuti: dacron; il sole le degrada), 2.3.1-35 e -36 (strallare e quadrare il tangone).')

# ============ GLI ARMI ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
for i,(rg,hd) in enumerate((('sloop','genoa'),('cutter',''),('ketch','fiocco'))):
    s,_=yacht(28+i*355,490,320,hd,rg,'#FFFFFF',[CORAL,PURPLE,GREEN][i],NAVY,3); b+=s
b+=f'<rect x="0" y="490" width="1092" height="130" fill="{WATER}" fill-opacity="0.45"/>'+line(0,490,1092,490,SEA,3)
lbl=''.join(pill(X+28+i*355+70,Y+560,180,t,c,26,align='center') for i,(t,c) in enumerate((('sloop',CORAL),('cutter',PURPLE),('ketch',GREEN))))
txt=term('Sloop','Un albero e una sola vela di prua alla volta: l\'armo più diffuso.')+term('Cutter','Un albero e due vele di prua insieme.')+term('Ketch','Due alberi: la mezzana, più piccola, sta a proravia dell\'asse del timone.')+term('Armo frazionato','Lo strallo non arriva in testa d\'albero. Le sartie volanti aiutano a sostenerlo.')
sec('armi', head('Vela · l\'attrezzatura','Gli armi')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Tre barche a confronto: sloop con randa e genoa, cutter con due vele di prua, ketch con albero di maestra e di mezzana')+lbl,
 notes='Quiz 2.2.1-25 (sloop), -26 (cutter), -27 (ketch: mezzana a proravia dell\'asse del timone), -3 e -4 (armo frazionato: strallo non incappellato in testa d\'albero), -1 e -2 (sartie volanti), 2.1.1-72 (piano velico: numero di alberi e tipo di vele), -45 (il multiscafo ha maggiore stabilità di forma). Lo yawl, non in banca, ha la mezzana a poppavia del timone.')

# ============ FERRAMENTA ============
def ico(k):
    s=f'<rect x="0" y="0" width="150" height="120" rx="24" fill="{SEA_T}"/>'
    if k=='winch':
        s+=f'<circle cx="75" cy="60" r="40" fill="#C9D3DD" stroke="{NAVY}" stroke-width="4"/><circle cx="75" cy="60" r="22" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'+curved(75,60,32,-160,60,CORAL,5)
    elif k=='stopper':
        s+=f'<rect x="20" y="42" width="110" height="36" rx="12" fill="{NAVY}"/><path d="M50 42 L96 18" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/>'+line(0,60,150,60,SUN,8)
    elif k=='paranco':
        s+=f'<circle cx="75" cy="26" r="16" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><circle cx="75" cy="94" r="16" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'+''.join(line(x,26,x,94,SUN,4) for x in (62,72,82,90))+arrow(110,60,110,100,CORAL,4,12)
    elif k=='avvolgi':
        s+=line(40,110,110,10,NAVY,4)+f'<path d="M44 104 L108 14 L118 26 L56 110 Z" fill="{SUN}"/><ellipse cx="45" cy="108" rx="22" ry="9" fill="{CORAL}"/>'
    elif k=='lazy':
        s+=line(30,10,30,110,INK,6)+line(30,92,140,92,INK,6)+''.join(line(30,y,x,92,PURPLE,3) for y,x in ((30,90),(30,130),(55,70),(55,110)))+f'<path d="M34 80 Q80 70 136 86 L136 92 L34 92 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'
    elif k=='garrocci':
        s+=line(30,110,120,10,NAVY,4)+f'<path d="M36 112 L118 20 L90 112 Z" fill="{SUN}" fill-opacity="0.8"/>'+''.join(f'<circle cx="{30+t*90:.0f}" cy="{110-t*100:.0f}" r="7" fill="none" stroke="{CORAL}" stroke-width="4"/>' for t in (0.15,0.4,0.65,0.9))
    return s
FT=[('winch','Winch','Si avvolge sempre in senso orario, senza sovrapporre i giri. Il self-tailing trattiene la cima da solo.'),
    ('stopper','Stopper','Blocca una drizza o una scotta; la galloccia serve a darle volta.'),
    ('paranco','Paranco','Più carrucole: demoltiplica lo sforzo, come quello della scotta randa.'),
    ('avvolgi','Avvolgifiocco','Riduce la vela di prua arrotolandola, senza ammainarla.'),
    ('lazy','Lazy jack','Le sagole che raccolgono la randa sul boma quando la si ammaina.'),
    ('garrocci','Garrocci','Moschettoni che fissano fiocco e genoa allo strallo.')]
tiles=''.join(card(f'<div style="display:flex; gap:20px; align-items:start">{svgi(150,120,ico(k),"Disegno: "+t,dw=190,dh=152,pan=False)}<div style="display:flex; flex-direction:column; gap:6px">{h3(t,30)}{p(d,24)}</div></div>',None,24,0) for k,t,d in FT)
sec('ferramenta', head('Vela · l\'attrezzatura','La ferramenta di bordo')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:24px">{tiles}</div>'+note('E tre nodi: savoia in fondo alle scotte perché non si sfilino, margherita per accorciare, gassa d\'amante che non scorre.',PURPLE,34),
 notes='Quiz 2.2.1-35, -36, -76, -78 (winch: senso orario, maniglia oraria, self-tailing), -85 e -86 (stopper), -41 (galloccia), -30 (paranco), -37 (ferramenta di bordo), -39 (grilli: non riducono lo sforzo), -40 (carrello randa), -43 (golfare), -44 (varea del tangone), -61 e -60 (lazy jack), -62 (feeder dello strallo cavo), -70 (tornichetto), -73 (avvolgiranda), -83 e -84 (avvolgifiocco: oltre il 30% il profilo perde efficienza), -51 (garrocci), -67 (impiombatura), -68 (borosa). Nodi: -54, -55 (gassa d\'amante: tiene e non accorcia), -56 (nodo piano: non con cime di diametro diverso), -57 (savoia: impedisce che la cima si sfili), -58 (parlato per i parabordi), -59 (margherita: accorcia la cima); -38 (polipropilene: sagole galleggianti).')

quiz_slide('quiz1','Quiz 1 · L\'attrezzatura',['2.2.1-6','2.2.1-28','2.2.1-12','2.2.1-54'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['2.2.1-6','2.2.1-28','2.2.1-12','2.2.1-54'],True)

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
txt=term('Andatura','È la direzione della barca rispetto al vento reale: bolina circa 45°, traverso 90°, lasco circa 135°, poppa o fil di ruota 180°.')+term('Angolo morto','Il settore controvento dove le vele non portano: per risalire si bordeggia a zig-zag.')+term('Mure','Il lato da cui prende il vento: dritta o sinistra. L\'altro lato è sottovento.')
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
txt=term('Tre venti','Il reale soffia sul mare; quello di velocità nasce dal moto della barca, contrario alla rotta. La loro somma è l\'apparente: quello che senti e che gonfia le vele.')+term('Sempre più a prua','L\'apparente arriva sempre più da prua del reale. Di bolina è più forte del reale, in poppa più debole: in poppa sembra di andare piano.')+term('La raffica','Un rinforzo del reale sposta l\'apparente verso poppa: si può orzare e stringere di più.')
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
txt=term('Due centri','Centro velico (CV): dove si applica la spinta del vento sulle vele. Centro di deriva (CD): dove si applica la resistenza laterale dell\'opera viva.')+term('Tendenze','CV a proravia: la barca poggia. A poppavia: orza. Allineati, con il timone al centro: neutra. La randa spinge a orzare, il genoa a poggiare; l\'albero inclinato a poppa rende orziera.')+term('La scelta giusta','Leggermente orziera: più sicura e più efficiente. Troppo poggiera toglie effetto al timone.')
sec('equilibrio', head('Vela · la teoria','Orziera o poggiera')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Tre barche a confronto con il centro velico e il centro di deriva: poggiera con il centro velico a proravia, neutra con i centri allineati, orziera con il centro velico a poppavia')+lbl,
 notes='Quiz 2.1.1-29, -59, -60 (centro velico), -30, -61, -62, -67 (centro di deriva), -31, -32, -33, -63…-66 (tendenze: CV a proravia = poggiera, allineati = neutra), -34 e -66 (da cosa dipende la posizione del CV), -41, -42, -93, -94 (inclinazione dell\'albero), -97 (randa orziera, genoa poggiero), -87…-92 (pesi dell\'equipaggio, pesi a prua contro la tendenza poggiera, meglio leggermente orziera; troppo sbandata di bolina va più piano), 2.3.1-58 (ridurre la randa diminuisce la tendenza orziera).')

# ============ REGOLAZIONI ============
def prof(depth,c):
    return f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+arrow(20,30,100,60,GREY,6,18)+f'<path d="M60 130 Q180 {130-depth} 320 110" fill="none" stroke="{c}" stroke-width="12" stroke-linecap="round"/>'+dash(60,130,320,110,NAVY,2)
reef=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+line(150,10,150,165,INK,6)+line(150,140,320,140,INK,6)+f'<path d="M156 40 L156 134 L312 134 Q230 90 156 40 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M156 140 L312 140 L312 154 L156 154 Z" fill="{CORAL_T}" stroke="{CORAL}" stroke-width="3"/>'+''.join(f'<circle cx="{x}" cy="147" r="4" fill="{CORAL}"/>' for x in range(180,310,26))
RC=[(prof(80,SEA),'Poco vento: vela grassa','Più concava, più potente. Si lascano cunningham, tesabase e drizze; in poppa grasso massimo.',SEA_T),
    (prof(30,CORAL),'Vento forte: vela magra','Si cazzano cunningham, tesabase, drizza del genoa e paterazzo; il carrello del genoa va a poppa. In raffica: trasto sottovento o scotta randa lascata.',CORAL_T),
    (reef,'Ridurre in tempo','Se pensi di ridurre, è il momento. Terzaroli sulla randa, genoa avvolto: con la falchetta in acqua si va più piano, non più forte.',LILAC_T)]
cc=''.join(card(svgi(360,170,s,t,dw=484,dh=228,pan=False)+h3(t,32)+p(d,25),bg,28,12) for s,t,d,bg in RC)
sec('regolazioni', head('Vela · la teoria','Regolare le vele')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 2.1.1-95 (lascare drizza e base: vela grassa per il fil di ruota), -98 e -99 (col vento in aumento si cazzano cunningham, tesabase, drizza genoa; il carrello del genoa va a poppa, non a prua), -53 (paterazzo), -80 (smagrire), -91 (troppo sbandata di bolina va più piano), 2.3.1-52 e -53 (smagrire per ridurre lo sbandamento, non per aumentare la potenza), -55 (in raffica trasto sottovento o scotta lascata), -58, -59, -60 (quando ridurre), 2.2.1-83 (genoa avvolto oltre il 30%: profilo meno efficiente), 2.3.1-30 e -31 (terzaroli: si riduce la randa, non si cambia vela; i matafioni legano la parte ripiegata).')

quiz_slide('quiz2','Quiz 2 · La teoria della vela',['2.1.1-12','2.1.1-53','2.1.1-64','2.1.1-26'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['2.1.1-12','2.1.1-53','2.1.1-64','2.1.1-26'],True)

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
txt=term('Orzare e poggiare','Orzare: portare la prua verso il vento. Poggiare: allontanarla, lascando le vele. La barra va dalla parte opposta a dove vuoi andare.')+term('Aiutarsi con le vele','Lascare la randa aiuta a poggiare; cazzarla aiuta a orzare.')+term('Sventare','Mettere la prua al vento o mollare le scotte: le vele non portano più. Straorza e strapoggia sono gli scarti improvvisi causati da raffica o onda.')
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
txt=term('Cambiare mure','Si fa in due modi: con la virata (prua nel vento, per risalire) o con l\'abbattuta (poppa nel vento, nelle andature portanti).')+term('L\'abbattuta','Si cazza la randa al centro, si passa la poppa nel vento, poi si lasca sull\'altro bordo. Non alla massima velocità di bolina o al traverso.')+term('La strambata','È l\'abbattuta involontaria e incontrollata: il boma attraversa di colpo. Rischio al gran lasco e in poppa; si previene con la ritenuta del boma.')
sec('virata', head('Vela · le manovre','Virata e abbattuta')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Traiettorie viste dall\'alto: nella virata la barca risale il vento e passa con la prua nel vento; nell\'abbattuta scende col vento e passa con la poppa nel vento')+lbl,
 notes='Quiz 2.3.1-9 (abbattuta: la poppa attraversa il vento), -10, -11, -41 (a cosa non serve la virata), -12 (l\'abbattuta non si fa alla massima velocità di bolina o al traverso), -40 (virata e abbattuta: le manovre per cambiare mure), -57 (ritenuta del boma contro la strambata al granlasco e al giardinetto), -61, -62, -63 (strambata: abbattuta involontaria), 2.2.1-81 (con il fiocco autovirante in virata non si cazza la scotta). Comandi: «pronti a virare», «vira»; «pronti ad abbattere», «abbatti».')

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
txt=term('Mure diverse','Chi ha le mure a sinistra lascia la rotta a chi ha le mure a dritta, di solito poggiando e passandole di poppa.')+term('Stesse mure','Chi è sopravento si scosta da chi è sottovento.')+term('Nel dubbio','Con mure a sinistra e una barca sopravento di cui non capisci le mure: lascia libera la rotta. Non conta chi è più veloce.')
sec('precedenze', head('Vela · le manovre','Le precedenze a vela'), pinned=svgp(X,Y,W,Hh,b,'Due situazioni viste dall\'alto con il vento da nord: con mure diverse la barca con mure a sinistra poggia e passa di poppa; con le stesse mure la barca sopravento orza e si scosta da quella sottovento')+lbl+pcol(txt),
 notes='Quiz 2.3.1-5, -45, -46, -47, -48 (mure a dritta ha la precedenza), -7 e -44 (stesse mure: sottovento ha la precedenza, sopravento orza), -49 (nel dubbio lasciare libera la rotta), -6 e -43 (non conta la velocità). È la regola 12 del COLREG: il rapporto tra vela e motore è nella lezione 5. 2.3.1-64 (salvo ordinanze, in porto non si entra a vela).')
X=700

# ============ ISSARE, RIDURRE, FERMARSI ============
up=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+line(160,8,160,166,INK,6)+line(160,150,330,150,INK,6)+f'<path d="M166 70 L166 144 L300 144 Q230 110 166 70 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'+arrow(120,140,120,40,CORAL,6,18)+line(140,10,166,70,SEA,3)
roll=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+line(80,160,300,10,NAVY,4)+f'<path d="M90 160 L292 22 L300 34 L110 164 Z" fill="{SUN}"/><path d="M110 164 L300 34 L230 164 Z" fill="{SUN}" fill-opacity="0.35"/>'+curved(90,150,26,200,-20,CORAL,5)
panna=f'<rect x="0" y="0" width="360" height="170" fill="#F4FAFC"/>'+arrow(30,10,30,90,GREY,7,22)+f'<g transform="translate(200 90) rotate(-45)"><path d="M100 0 Q40 -20 -84 -16 L-100 -12 L-100 12 L-84 16 Q40 20 100 0 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M46 0 Q20 -26 -10 -30" fill="none" stroke="{SUN}" stroke-width="8" stroke-linecap="round"/><path d="M12 0 Q-30 22 -70 36" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/></g>'
IC=[(up,'Issare','Con la prua al vento, così le vele non si gonfiano. Drizza con moschettone alla penna; garrocci incocciati dalla mura verso la penna; scotte del fiocco con la gassa d\'amante.',SEA_T),
    (roll,'Ridurre','Terzaroli sulla randa, avvolgifiocco sulla vela di prua. Con il cattivo tempo: tormentina.',GREEN_T),
    (panna,'Fermarsi: la panna','Fiocco a collo, randa per la bolina larga, timone all\'orza: la barca resta quasi ferma. Si entra in porto a motore, salvo ordinanze.',LILAC_T)]
cc=''.join(card(svgi(360,170,s,t,dw=460,dh=217,pan=False)+h3(t,32)+p(d,25),bg,28,12) for s,t,d,bg in IC)
sec('issare', head('Vela · le manovre','Issare, ridurre, fermarsi')+f'<div style="display:flex; gap:24px">{cc}</div>',
 notes='Quiz 2.3.1-8 e -16 (tesata la drizza, la base si cazza poco per le andature larghe e molto per la bolina), -13 e -15 (armare la randa: niente borosa sulla mura, niente meolo), -17 (genoa e fiocco si armano allo stesso modo), -18 (la prima operazione è la mura, non la bugna), -19 (garrocci dalla mura verso la penna), -20 (moschettone impiombato alla drizza), -21 (scotte: non il parlato doppio), -22 (prua al vento), -23 e -24 (strallo cavo), -25, -26 (tormentina e fileggiare non servono a rallentare), -27 e -28 (panna), -29 (la cappa non è con l\'ancora galleggiante filata di poppa), -30 e -31 (terzaroli), -32 e -54 (messa a segno), -34, -64 (in porto non a vela salvo ordinanze).')

quiz_slide('quiz3','Quiz 3 · Le manovre',['2.3.1-4','2.3.1-47','2.3.1-62','2.3.1-65'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['2.3.1-4','2.3.1-47','2.3.1-62','2.3.1-65'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['2.1.1-24','2.2.1-81','2.3.1-28','2.1.1-97'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['2.1.1-24','2.2.1-81','2.3.1-28','2.1.1-97'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['2.1.1-94','2.2.1-19','2.3.1-9','2.2.1-60'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['2.1.1-94','2.2.1-19','2.3.1-9','2.2.1-60'],True)
closing(['Manovre fisse (strallo, sartie, paterazzo) reggono l\'albero; le correnti (drizze, scotte) manovrano le vele','Bolina 45°, traverso 90°, lasco 135°, poppa 180°; controvento c\'è l\'angolo morto','Il vento apparente è sempre più a prua del reale: di bolina più forte, in poppa più debole','CV a proravia del CD: poggiera; a poppavia: orziera. Meglio un po\' orziera','Mure a dritta ha la precedenza; con le stesse mure passa chi è sottovento'],
 'Prossima lezione · 09 · Emergenze, ripasso vela e correnti','A casa: i 250 quiz di vela, tutti Vero o Falso.')
write_deck(OUT,'Lezione 08 · Vela: attrezzatura, teoria e manovre',
 ['cover','agenda','barca','randa','vele','armi','ferramenta','quiz1','quiz1r','andature','apparente','portanza','equilibrio','regolazioni','quiz2','quiz2r',
  'barra','virata','precedenze','issare','quiz3','quiz3r','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Attrezzatura: barca, randa, vele, armi, ferramenta","start":"barca"},
  "s3":{"description":"Teoria: andature, vento apparente, portanza, equilibrio, regolazioni","start":"andature"},
  "s4":{"description":"Manovre: timone, virata e abbattuta, precedenze, issare e ridurre","start":"barra"},
  "s5":{"description":"Verifica finale","start":"finale1"}})
