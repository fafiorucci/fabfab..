"""Appendice B: la nomenclatura completa della barca a vela (slide di studio con disegni)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/appB/project'
GREY='#97A6B4'; ORANGE='#F28C28'; SKY='#DDEFF7'; AF='#C8553D'; WOOD='#A0703F'; SEAB='#E8F4F8'
X,Y,W,Hh=700,290,1092,620
def pcol(inner,w=532,gap=20,left=1260,top=290): return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=22: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'

# ---------- etichette con linea di richiamo ----------
def tagp(x,y,t,c,align='l',size=22):
    h=size*1.3+4
    pos=f'left:{x:.0f}px' if align=='l' else (f'right:{1920-x:.0f}px' if align=='r' else f'left:{x:.0f}px; transform:translateX(-50%)')
    return (f'<p style="position:absolute; {pos}; top:{y-h/2:.0f}px; width:max-content; font-size:{size}px; line-height:1.3; font-weight:900; '
            f'color:#FFFFFF; background:{c}; padding:2px 10px; border-radius:10px; white-space:nowrap">{t}</p>')
class Fig:
    def __init__(s,x0,y0,w,h): s.x0,s.y0,s.w,s.h=x0,y0,w,h; s.svg=''; s.html=''
    def lead(s,part,at,t,c=NAVY,align='l',size=22):
        (px,py),(lx,ly)=part,at
        s.svg+=f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{c}" stroke-width="2.5"/><circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{c}" stroke="#FFFFFF" stroke-width="2"/>'
        s.html+=tagp(s.x0+lx,s.y0+ly,t,c,align,size)
    def tag(s,at,t,c=NAVY,align='l',size=22): s.html+=tagp(s.x0+at[0],s.y0+at[1],t,c,align,size)
    def out(s,body,alt): return svgp(s.x0,s.y0,s.w,s.h,body+s.svg,alt)+s.html

def qbez(P0,P1,P2,t): return ((1-t)**2*P0[0]+2*(1-t)*t*P1[0]+t*t*P2[0], (1-t)**2*P0[1]+2*(1-t)*t*P1[1]+t*t*P2[1])
def qy(P,x):
    lo,hi=0.0,1.0
    for _ in range(40):
        m=(lo+hi)/2
        if qbez(*P,m)[0]<x: lo=m
        else: hi=m
    return qbez(*P,lo)[1]
def water(w,h,y0,op=0.35): return f'<rect x="0" y="{y0}" width="{w}" height="{h-y0}" fill="{WATER}" fill-opacity="{op}"/>'+line(0,y0,w,y0,SEA,3)
_cp=[0]
def clip_below(d,y,w,fill):
    _cp[0]+=1; cid=f'bcp{_cp[0]}'
    return f'<defs><clipPath id="{cid}"><rect x="0" y="{y}" width="{w}" height="2000"/></clipPath></defs><path d="{d}" fill="{fill}" clip-path="url(#{cid})"/>'

ORDER=['cover','indice','scafo','pianta','sotto','direzioni','coperta','ferramenta','albero','fisse','randa','genoa','vele','corr_randa','corr_prua',
       'armi','cime','verbi','quiz1','quiz1r','quiz2','quiz2r','gloss1','gloss2','gloss3','chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
LB.ICON_T.update({'Indice':'book','Lo scafo di profilo':'hull','Lo scafo in pianta e in sezione':'hull','Sotto coperta':'hull','Le direzioni a bordo':'compass',
 'La coperta vista dall\'alto':'map','La ferramenta di coperta':'anchor','L\'albero visto da prua':'sail','Le manovre fisse':'sail','La randa: angoli e lati':'sail',
 'Il genoa: angoli e lati':'sail','Le vele di bordo':'sail','Le manovre correnti della randa':'wind','Genoa e spinnaker: le manovre':'wind','Gli armi':'sail',
 'Cime e nodi':'anchor','Le parole delle manovre':'helm','Glossario':'book'})

# ---- barca di profilo (dalla lezione 8) ----
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
    if rig=='yawl':
        zx=u(0.045); zt=dm-0.3*L; zb=dm-0.05*L
        s+=line(zx,dm,zx,zt,INK,max(3,L*0.008))+f'<path d="M{zx:.1f} {zt+0.02*L:.1f} L{zx:.1f} {zb:.1f} L{u(-0.1):.1f} {zb:.1f} Q{u(-0.06):.1f} {zt+0.13*L:.1f} {zx:.1f} {zt+0.02*L:.1f} Z" fill="{main_c}" stroke="{st}" stroke-width="{sw}"/>'+line(zx,zb,u(-0.105),zb,INK,max(3,L*0.007))+line(u(0.0),dk+0.005*L,u(-0.1),dk+0.012*L,INK,max(2,L*0.006))
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
    elif head=='torm':
        h=pt(0.5); t=pt(0.97); c=(mx+0.2*L,dm-0.05*L)
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} L{t[0]:.1f} {t[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Z"'
    elif head=='code0':
        h=(mx+0.01*L,mt+0.03*L); tk2=(u(1.05),bowy-0.005*L); c=(mx+0.02*L,dm-0.07*L)
        s+=line(u(0.99),bowy,u(1.06),bowy-0.004*L,INK,max(2.5,L*0.008))
        hs=f'<path d="M{h[0]:.1f} {h[1]:.1f} Q{u(0.9):.1f} {mt+0.3*L:.1f} {tk2[0]:.1f} {tk2[1]:.1f} L{c[0]:.1f} {c[1]:.1f} Q{mx+0.09*L:.1f} {mt+0.3*L:.1f} {h[0]:.1f} {h[1]:.1f} Z"'
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


# ============ COPERTINA ============
cover(0,'I nomi della barca a vela','La nomenclatura completa per lo studio: scafo, coperta, alberatura, vele, manovre e ferramenta, con un disegno per ogni gruppo di nomi',
 'Appendice B al corso. Raccoglie la nomenclatura della barca a vela: i termini dei quiz ufficiali 1.1.1 (scafo) e 2.2.1 (attrezzatura della vela) del DD 131/2022, con un disegno per ogni gruppo di nomi, due verifiche e un glossario dalla A alla Z.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice B · studio'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
IDX=[('1','Lo scafo','Profilo, pianta e sezione, sotto coperta, direzioni a bordo',SEA,'scafo'),
     ('2','La coperta','La coperta vista dall\'alto e la ferramenta',BLUE,'coperta'),
     ('3','Alberatura e manovre fisse','Albero, crocette, sartie, stralli e paterazzo',PURPLE,'albero'),
     ('4','Le vele','Angoli e lati di randa e genoa, le vele di bordo',CORAL,'randa'),
     ('5','Le manovre correnti','Drizze, scotte, vang, amantiglio, braccio e tangone',GREEN,'corr_randa'),
     ('6','Armi, cime e parole','Sloop, cutter, ketch, yawl; cime, nodi e verbi di bordo',NAVY,'armi'),
     ('7','Ripasso','Due verifiche con i quiz ufficiali e il glossario dalla A alla Z',CORAL,'quiz1')]
cards=''.join(f'<div style="display:flex; align-items:center; gap:22px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:14px 24px"><p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:44px">{n}</p><div style="flex:1; display:flex; flex-direction:column; gap:2px">{p(t,30,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div><p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(s)}</p></div>' for n,t,d,c,s in IDX)
sec('indice', head('Appendice B · La nomenclatura della barca a vela','Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px">{cards}</div>',
 notes='Ogni gruppo di nomi ha un disegno con le etichette; le definizioni sono nelle note e nel glossario finale. I termini seguono i quiz ufficiali: 1.1.1 per lo scafo, 2.2.1 per l\'attrezzatura della vela.')

# ============ 1 · LO SCAFO DI PROFILO ============
F=Fig(128,290,1664,620); PW=1664
SH=((300,236),(760,262),(1300,208)); sy=lambda x: qy(SH,x); WLY=330
hull='M300 236 Q760 262 1300 208 Q1272 300 1210 330 Q1170 358 1080 364 L400 360 Q345 354 330 330 Z'
b=f'<rect x="0" y="0" width="{PW}" height="620" fill="{SKY}"/>'+water(PW,620,WLY)
xs=list(range(420,1260,100)); tops=[(x,sy(x)-34) for x in xs]
b+=''.join(line(x,sy(x),x,t,GREY,3) for x,t in tops)
b+=f'<polyline points="{" ".join(f"{x},{t:.1f}" for x,t in tops)}" fill="none" stroke="{GREY}" stroke-width="2.5"/><polyline points="{" ".join(f"{x},{t+17:.1f}" for x,t in tops)}" fill="none" stroke="{GREY}" stroke-width="2"/>'
b+=f'<path d="M1250 {sy(1250):.1f} L1256 176 L1296 172 L1299 {sy(1299):.1f}" fill="none" stroke="{GREY}" stroke-width="4"/><path d="M306 {sy(306):.1f} L306 198 L356 196 L360 {sy(360):.1f}" fill="none" stroke="{GREY}" stroke-width="4"/>'
b+=f'<path d="M690 358 L800 358 L782 510 L712 510 Z" fill="{NAVY}"/><ellipse cx="748" cy="516" rx="86" ry="21" fill="{INK}"/>'
b+=f'<path d="M372 356 L430 356 L424 478 L396 488 L374 474 Z" fill="{NAVY}"/>'
b+=f'<path d="{hull}" fill="{BOAT}"/>'+clip_below(hull,WLY,PW,AF)+f'<path d="{hull}" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=f'<path d="M318 250 Q760 276 1292 222" fill="none" stroke="{SEA}" stroke-width="6"/>'
t1,t2=620,960
b+=f'<path d="M{t1} {sy(t1):.1f} L{t1+34} {sy(t1)-28:.1f} L{t2-12} {sy(t2)-26:.1f} L{t2} {sy(t2):.1f} Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
b+=''.join(f'<ellipse cx="{x}" cy="{sy(x)-13:.1f}" rx="16" ry="6" fill="{SEA}"/>' for x in (700,770,840,910))
b+=line(0,WLY,PW,WLY,SEA,3)+dash(392,296,392,358,NAVY,3)
b+=dash(300,236,300,124,SOFT,2)+dash(1300,208,1300,124,SOFT,2)+dim(300,140,1300,140,NAVY)
dby=sy(1120); b+=dim(1120,dby,1120,WLY,PURPLE)
b+=line(834,537,912,537,PURPLE,2.5)+dim(900,WLY,900,537,PURPLE)
F.tag((800,140),'lunghezza fuori tutto',NAVY,'c')
F.tag((1134,(dby+WLY)/2),'bordo libero',PURPLE,'l'); F.tag((914,440),'pescaggio',PURPLE,'l')
F.tag((1330,214),'prua',CORAL,'l'); F.tag((272,236),'poppa',CORAL,'r')
F.lead((1272,272),(1344,272),'dritto di prua',NAVY,'l')
F.lead((316,288),(250,300),'specchio di poppa',NAVY,'r')
F.lead((560,292),(560,190),'opera morta · murata',NAVY,'c')
F.lead((560,346),(560,430),'opera viva (carena)',AF,'c')
F.tag((1648,WLY),'linea di galleggiamento',SEA,'r')
F.lead((725,505),(650,565),'chiglia e bulbo zavorrato',NAVY,'r')
F.lead((412,440),(330,470),'timone compensato',NAVY,'r')
F.lead((392,358),(340,405),'losca',NAVY,'r')
F.lead((830,sy(830)-16),(830,190),'tuga',NAVY,'c')
sec('scafo', head('1 · Lo scafo','Lo scafo di profilo',SEA), pinned=F.out(b,'Barca a vela di profilo senza vele: prua e dritto di prua, poppa e specchio di poppa, opera morta con la murata, opera viva rossa sotto la linea di galleggiamento, tuga, chiglia con bulbo zavorrato, timone compensato con la losca, e le misure lunghezza fuori tutto, bordo libero e pescaggio'),
 notes='Opera viva (carena) sotto la linea di galleggiamento, opera morta sopra: le murate sono la parte laterale esterna dell\'opera morta. Bordo libero: distanza verticale tra coperta e linea di galleggiamento. Pescaggio: dalla linea di galleggiamento al punto più basso dello scafo, qui il bulbo. Lunghezza fuori tutto: tra le estremità di prua e di poppa. Lo specchio di poppa è la parte della poppa sopra il dritto di poppa, a cui si incardina il timone quando è esterno. La losca è l\'apertura da cui passa l\'asse del timone; il timone è compensato quando una parte della pala è a proravia dell\'asse. Il bulbo zavorrato dà stabilità contro lo sbandamento. Quiz 1.1.1-1, -4, -10, -11, -14, -15, -16, -22, -28, -33, -35, -37, -39, -47, -53, -55, -56, -57; 2.1.1-2, -3.')

# ============ 1 · PIANTA E SEZIONE ============
F1=Fig(128,290,800,620)
out='M745 310 Q652 172 380 168 L170 186 Q116 192 112 250 L112 370 Q116 428 170 434 L380 452 Q652 448 745 310 Z'
b1=f'<rect x="0" y="0" width="800" height="620" fill="{SEAB}"/>'+f'<path d="{out}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b1+=f'<rect x="300" y="245" width="270" height="130" rx="30" fill="#F2EEE6" stroke="{NAVY}" stroke-width="3"/><rect x="140" y="236" width="130" height="148" rx="22" fill="#E6EEF2" stroke="{NAVY}" stroke-width="3"/>'
b1+=f'<circle cx="540" cy="310" r="10" fill="{INK}"/>'
b1+=dash(380,110,380,505,SEA,3)+f'<line x1="70" y1="310" x2="775" y2="310" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="14 8"/>'+dim(380,170,380,450,CORAL)
F1.tag((380,98),'sezione maestra',SEA,'c'); F1.lead((640,310),(640,282),'asse longitudinale',PURPLE,'c')
F1.tag((394,400),'baglio massimo',CORAL,'l')
F1.lead((575,184),(575,136),'murata di sinistra',NAVY,'c'); F1.lead((575,437),(575,490),'murata di dritta',NAVY,'c')
F1.tag((757,310),'prua',CORAL,'l'); F1.tag((102,310),'poppa',CORAL,'r')
F2=Fig(992,290,800,620)
sec_d='M170 190 Q175 300 240 335 Q300 352 360 354 L440 354 Q500 352 560 335 Q625 300 630 190 Q400 176 170 190 Z'
b2=f'<rect x="0" y="0" width="800" height="620" fill="{SKY}"/>'+water(800,620,270)
b2+=f'<path d="M372 350 L428 350 L420 480 L380 480 Z" fill="{NAVY}"/><ellipse cx="400" cy="492" rx="36" ry="26" fill="{INK}"/>'
b2+=f'<path d="{sec_d}" fill="{BOAT}"/>'
_cp[0]+=1; cid=f'bcp{_cp[0]}'
b2+=f'<defs><clipPath id="{cid}"><path d="{sec_d}"/></clipPath></defs><rect x="0" y="300" width="800" height="80" fill="{SEA_T}" clip-path="url(#{cid})"/><rect x="0" y="338" width="800" height="40" fill="#9FC9D6" clip-path="url(#{cid})"/>'
b2+=f'<path d="{sec_d}" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>'
_cp[0]+=1; cid2=f'bcp{_cp[0]}'
b2+=f'<defs><clipPath id="{cid2}"><rect x="0" y="270" width="800" height="400"/></clipPath></defs><path d="{sec_d}" fill="none" stroke="{AF}" stroke-width="9" clip-path="url(#{cid2})"/>'
b2+=line(222,300,578,300,WOOD,8)+f'<path d="M270 184 L286 132 L514 132 L530 184" fill="{BOAT}" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
b2+=line(0,270,800,270,SEA,3)
F2.tag((400,40),'sezione maestra · vista da poppa',SEA,'c')
F2.lead((400,138),(400,92),'tuga',NAVY,'c'); F2.lead((212,186),(130,122),'ponte di coperta',NAVY,'c')
F2.lead((630,230),(680,230),'murata',NAVY,'l'); F2.lead((176,240),(160,240),'opera morta',NAVY,'r')
F2.lead((250,330),(215,372),'opera viva',AF,'r'); F2.lead((520,300),(660,318),'pagliolo',WOOD,'l')
F2.lead((440,344),(660,370),'sentina',SEA,'l'); F2.lead((412,470),(520,500),'chiglia e bulbo',NAVY,'l')
sec('pianta', head('1 · Lo scafo','Lo scafo in pianta e in sezione',SEA),
 pinned=F1.out(b1,'Scafo visto dall\'alto con prua a destra: asse longitudinale tratteggiato da prua a poppa, baglio massimo nel punto più largo, murata di sinistra in alto e murata di dritta in basso, sezione maestra')
       +F2.out(b2,'Sezione maestra vista da poppa: tuga e ponte di coperta in alto, murate ai lati, opera morta sopra e opera viva sotto la linea di galleggiamento, pagliolo e sotto la sentina, chiglia e bulbo'),
 notes='Asse longitudinale: passa per prua e poppa, parallelo alla chiglia. Baglio massimo: la larghezza massima dello scafo, nella sezione maestra (la sezione trasversale centrale, di norma la più larga; l\'ordinata maestra è quella che le corrisponde). Guardando verso prua la murata di dritta è a destra, quella di sinistra a sinistra. Ponte di coperta: chiude lo scafo in alto; la tuga è la sovrastruttura abitabile che non occupa tutta la larghezza. Pagliolo: piano calpestabile amovibile sotto coperta (l\'insieme è il pagliolato); la sentina è lo spazio tra il fondo interno dello scafo e il pagliolo, dove si raccolgono acque sporche e residui. Quiz 1.1.1-2, -3, -5, -23, -27, -29, -38, -39, -45, -46, -48, -49, -51, -59, -60.')

# ============ 1 · SOTTO COPERTA ============
F=Fig(128,290,1664,620)
SH2=((280,196),(760,222),(1320,170)); s2=lambda x: qy(SH2,x); WL2=300
h2='M280 196 Q760 222 1320 170 Q1290 262 1225 300 Q1180 352 1080 380 L430 378 Q352 368 315 300 Z'
b=f'<rect x="0" y="0" width="{PW}" height="620" fill="{SKY}"/>'+water(PW,620,WL2,0.3)
b+=f'<path d="M700 376 L800 376 L786 500 L716 500 Z" fill="{NAVY}"/><ellipse cx="750" cy="506" rx="80" ry="18" fill="{INK}"/>'
b+=f'<path d="M362 370 L420 370 L414 480 L386 490 L364 476 Z" fill="{NAVY}"/>'
b+=line(600,376,600,428,INK,10)+f'<ellipse cx="600" cy="414" rx="10" ry="6" fill="{SUN}"/>'+f'<path d="M600 432 L585 422 L585 442 Z M600 432 L615 422 L615 442 Z" fill="{INK}"/>'
b+=f'<path d="{h2}" fill="#FFFDF8"/>'
_cp[0]+=1; cid=f'bcp{_cp[0]}'
b+=f'<defs><clipPath id="{cid}"><path d="{h2}"/></clipPath></defs><rect x="0" y="335" width="{PW}" height="60" fill="{SEA_T}" clip-path="url(#{cid})"/><rect x="0" y="366" width="{PW}" height="30" fill="#9FC9D6" clip-path="url(#{cid})"/>'
b+=f'<rect x="340" y="255" width="150" height="110" fill="#EFE7DA" clip-path="url(#{cid})"/>'
b+=f'<rect x="520" y="292" width="110" height="52" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="3"/>'
b+=line(440,335,1150,335,WOOD,7)
for x,top in ((500,250),(900,s2(900)),(1150,s2(1150))): b+=line(x,top,x,376 if x<1100 else 350,NAVY,6)
b+=line(330,s2(330),340,250,NAVY,5)+line(340,250,550,250,NAVY,5)+line(550,250,560,s2(560),NAVY,5)
b+=f'<path d="M280 196 Q760 222 1320 170" fill="none" stroke="{NAVY}" stroke-width="7"/>'
b+=f'<path d="M600 {s2(600):.1f} L630 {s2(600)-38:.1f} L950 {s2(950)-36:.1f} L965 {s2(965):.1f}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=''.join(f'<ellipse cx="{x}" cy="{s2(x)-18:.1f}" rx="15" ry="6" fill="{SEA}"/>' for x in (720,790,860))
b+=f'<rect x="604" y="{s2(604)-6:.1f}" width="46" height="12" fill="#FFFDF8"/>'
b+=''.join(line(606+i*9,s2(606)+i*25+10,646+i*9,s2(606)+i*25+10,WOOD,5) for i in range(5))+line(604,s2(604)+6,648,335,WOOD,4)
b+=f'<rect x="1030" y="{s2(1050)-14:.1f}" width="60" height="14" rx="4" fill="{SEA}"/>'
b+=line(860,378,860,352,INK,5)+line(846,352,874,352,CORAL,6)
b+=''.join(f'<circle cx="{1180+(i%4)*14}" cy="{330-(i//4)*10}" r="6" fill="none" stroke="{INK}" stroke-width="3"/>' for i in range(10))
b+=dash(380,250,380,372,NAVY,3)
b+=f'<path d="{h2}" fill="none" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/>'
_cp[0]+=1; cid2=f'bcp{_cp[0]}'
b+=f'<defs><clipPath id="{cid2}"><rect x="0" y="{WL2}" width="{PW}" height="400"/></clipPath></defs><path d="{h2}" fill="none" stroke="{AF}" stroke-width="7" clip-path="url(#{cid2})"/>'
b+=line(0,WL2,PW,WL2,SEA,3)
TOP=110
F.lead((445,250),(430,TOP),'pozzetto',NAVY,'c'); F.lead((627,s2(627)+12),(600,TOP),'boccaporto',WOOD,'c')
F.lead((780,s2(780)-36),(760,TOP),'tuga',NAVY,'c'); F.lead((900,262),(880,TOP),'paratie',NAVY,'c')
F.lead((1060,s2(1050)-10),(1060,TOP),'osteriggio',SEA,'c'); F.lead((1240,s2(1240)),(1265,TOP),'ponte di coperta',NAVY,'c')
F.lead((420,300),(260,300),'gavone di poppa',NAVY,'r'); F.lead((380,372),(330,412),'losca',NAVY,'r')
F.lead((575,318),(520,560),'locale motore',INK,'c'); F.lead((600,414),(560,470),'zinco',SUN,'r')
F.lead((860,356),(930,560),'presa a mare e passascafo',CORAL,'l')
F.lead((1040,335),(1080,470),'pagliolato',WOOD,'l'); F.lead((1120,370),(1300,420),'sentina',SEA,'l')
F.lead((1200,300),(1380,250),'gavone di prua',NAVY,'l')
sec('sotto', head('1 · Lo scafo','Sotto coperta',SEA), pinned=F.out(b,'Sezione longitudinale di una barca a vela: pozzetto, boccaporto con la scaletta, tuga, osteriggio, ponte di coperta; sotto, le paratie verticali, il pagliolato con la sentina, il gavone di poppa sotto il pozzetto, il locale motore con il piede poppiero e lo zinco, la presa a mare con il passascafo, la losca del timone e il gavone di prua con la catena'),
 notes='Paratie: strutture verticali che suddividono internamente lo scafo in senso trasversale. Pagliolato: il pavimento interno, il piano di calpestio più basso, fatto di paglioli amovibili; sotto c\'è la sentina, che raccoglie le acque sporche e i residui liquidi. Gavone: vano ripostiglio di prua o di poppa. Boccaporto: apertura nel ponte di coperta per il passaggio di persone o cose; osteriggio: apertura sulla coperta per luce e aria. Locale motore: dove sono il motore e gran parte degli impianti. Passascafo: parte filettata che attraversa la carena; la presa a mare è la valvola collegata che chiude l\'ingresso dell\'acqua. Zinchi: anodi che evitano la corrosione galvanica. Quiz 1.1.1-3, -9, -13, -19, -27, -29, -36, -42, -43, -46, -51, -64, -65, -67.')

# ============ 1 · LE DIREZIONI A BORDO ============
F=Fig(X,Y,W,Hh); cx,cy=546,322
b=f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="{SEAB}"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="252" fill="none" stroke="#C9E6E2" stroke-width="3" stroke-dasharray="6 10"/>'
b+=dash(cx-150,cy,cx+150,cy,PURPLE,3)+topboat(cx,cy,300,-90,BOAT,NAVY,4)
DIRS=[(0,'prua',CORAL,'c'),(45,'mascone di dritta',SEA,'l'),(90,'traverso di dritta',SEA,'l'),(135,'giardinetto di dritta',SEA,'l'),
      (180,'poppa',CORAL,'c'),(225,'giardinetto di sinistra',PURPLE,'r'),(270,'traverso di sinistra',PURPLE,'r'),(315,'mascone di sinistra',PURPLE,'r')]
for a,t,c,al in DIRS:
    ra=math.radians(a); s_,c_=math.sin(ra),math.cos(ra)
    rin=178 if a in (0,180) else (78 if a in (90,270) else 118)
    b+=arrow(cx+242*s_,cy-242*c_,cx+rin*s_,cy-rin*c_,c,6,22)
    lx,ly=cx+262*s_,cy-262*c_
    if a==0: ly=cy-286
    if a==180: ly=cy+286
    F.tag((lx,ly),t,c,al)
F.tag((cx+60,cy-28),'a proravia',NAVY,'l',20); F.tag((cx+60,cy+28),'a poppavia',NAVY,'l',20)
txt=(term('Dalla prua in giro','Mascone a 45° dalla prua, traverso a 90°, giardinetto a 135°: a dritta e a sinistra. Le murate sono i due fianchi.')
     +term('Proravia e poppavia','Ciò che sta davanti a un riferimento è a proravia, ciò che sta dietro è a poppavia.')
     +term('Sopravvento e sottovento','Il lato da cui arriva il vento è sopravvento, l\'altro sottovento.')
     +term('Rollio e beccheggio','Rollio: oscillazione attorno all\'asse longitudinale. Beccheggio: attorno all\'asse trasversale.'))
sec('direzioni', head('1 · Lo scafo','Le direzioni a bordo',SEA)+col(txt), pinned=F.out(b,'Barca vista dall\'alto con la prua in alto e otto frecce verso lo scafo: prua, mascone, traverso e giardinetto di dritta a destra, poppa in basso, giardinetto, traverso e mascone di sinistra a sinistra; una linea al traverso divide ciò che sta a proravia da ciò che sta a poppavia'),
 notes='Guardando verso prua, la dritta è a destra e la sinistra a sinistra. Il giardinetto è la parte terminale dello scafo vicino alla poppa, a dritta e a sinistra; il mascone la parte prodiera. Quiz 1.1.1-20, -21, -24, -25, -41, -58 (con figura: le frecce verso lo scafo), -34 (beccheggio: asse trasversale), -69 (rollio: asse longitudinale). Mure a dritta: il vento arriva da dritta.')

# ============ 2 · LA COPERTA VISTA DALL'ALTO ============
def nbadge(x,y,n,c): return f'<p style="position:absolute; left:{x-19:.0f}px; top:{y-19:.0f}px; width:38px; height:38px; font-size:22px; line-height:38px; font-weight:900; color:#FFFFFF; background:{c}; border-radius:19px; text-align:center">{n}</p>'
x0c,y0c=128,290
TOPQ=((520,168),(930,175),(1040,310))
def ytop(x):
    if x<=150: return 188
    if x<=520: return 182-(x-150)/370*14
    return qy(TOPQ,x)
ybot=lambda x: 620-ytop(x)
out='M1040 310 Q930 175 520 168 L150 182 Q64 188 60 240 L60 380 Q64 432 150 438 L520 452 Q930 445 1040 310 Z'
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SEAB}"/>'
b+=f'<path d="{out}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=f'<path d="{out}" fill="none" stroke="#B89A5E" stroke-width="3" transform="translate(550 310) scale(0.972 0.945) translate(-550 -310)"/>'
b+=f'<rect x="95" y="218" width="235" height="184" rx="22" fill="#E6EEF2" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<circle cx="150" cy="310" r="40" fill="none" stroke="{INK}" stroke-width="6"/>'+''.join(line(150,310,150+40*math.cos(math.radians(a)),310+40*math.sin(math.radians(a)),INK,3) for a in (0,60,120,180,240,300))+f'<circle cx="150" cy="310" r="8" fill="{INK}"/>'
b+=line(290,226,290,394,NAVY,6)+f'<rect x="281" y="298" width="18" height="24" rx="4" fill="{CORAL}"/>'
b+=f'<circle cx="104" cy="226" r="5" fill="{INK}"/><circle cx="104" cy="394" r="5" fill="{INK}"/>'
b+=''.join(f'<circle cx="300" cy="{y}" r="14" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/>' for y in (200,420))
b+=f'<rect x="345" y="222" width="355" height="176" rx="44" fill="#F2EEE6" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<rect x="350" y="288" width="50" height="44" rx="6" fill="#D8CBB5" stroke="{NAVY}" stroke-width="2"/>'
b+=''.join(f'<circle cx="372" cy="{y}" r="11" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/><rect x="392" y="{y-6}" width="40" height="12" rx="3" fill="{NAVY}"/>' for y in (246,374))
b+=''.join(f'<rect x="520" y="{y}" width="36" height="36" rx="6" fill="{SEA_T}" stroke="{SEA}" stroke-width="3"/>' for y in (245,339))
for x in (440,500,560):
    pass
b+=line(430,ytop(430)+22,560,ytop(560)+22,SOFT,5)+line(430,ybot(430)-22,560,ybot(560)-22,SOFT,5)
b+=f'<rect x="490" y="{ytop(500)+16:.1f}" width="20" height="12" rx="3" fill="{CORAL}"/><rect x="490" y="{ybot(500)-28:.1f}" width="20" height="12" rx="3" fill="{CORAL}"/>'
b+=line(670,310,660,ytop(660)+10,NAVY,2.5)+line(670,310,660,ybot(660)-10,NAVY,2.5)+line(670,310,1030,310,NAVY,2.5)
b+=f'<rect x="652" y="{ytop(660)+5:.1f}" width="16" height="10" fill="{INK}"/><rect x="652" y="{ybot(660)-15:.1f}" width="16" height="10" fill="{INK}"/>'
b+=f'<circle cx="670" cy="310" r="13" fill="{INK}"/>'
cx_=[200,340,480,620,760,880]
b+=''.join(f'<circle cx="{x}" cy="{ytop(x)+8:.1f}" r="5" fill="{GREY}"/><circle cx="{x}" cy="{ybot(x)-8:.1f}" r="5" fill="{GREY}"/>' for x in cx_)
b+=f'<polyline points="160,{ytop(160)+8:.1f} {" ".join(f"{x},{ytop(x)+8:.1f}" for x in cx_)}" fill="none" stroke="{GREY}" stroke-width="2.5"/><polyline points="160,{ybot(160)-8:.1f} {" ".join(f"{x},{ybot(x)-8:.1f}" for x in cx_)}" fill="none" stroke="{GREY}" stroke-width="2.5"/>'
b+=f'<path d="M160 190 L68 198 L66 422 L160 430" fill="none" stroke="{GREY}" stroke-width="6" stroke-linejoin="round"/><path d="M880 {ytop(880)+8:.1f} Q990 250 1016 310 Q990 370 880 {ybot(880)-8:.1f}" fill="none" stroke="{GREY}" stroke-width="6"/>'
b+=f'<rect x="790" y="288" width="50" height="44" rx="6" fill="{SEA_T}" stroke="{SEA}" stroke-width="3"/><rect x="930" y="295" width="36" height="30" rx="5" fill="#E6EEF2" stroke="{NAVY}" stroke-width="2"/>'
b+=f'<rect x="1036" y="302" width="26" height="16" rx="4" fill="{INK}"/><circle cx="1056" cy="310" r="6" fill="{GREY}"/>'
b+=''.join(f'<rect x="{x-15}" y="{y-4}" width="30" height="8" rx="4" fill="{INK}"/>' for x,y in ((925,ytop(925)+20),(925,ybot(925)-20),(185,ytop(185)+22),(185,ybot(185)-22)))
C_=[CORAL,SEA,PURPLE,BLUE,GREEN]
ITEMS=[('pulpito di prua',(962,236)),('musone e rullo dell\'ancora',(1058,276)),('gavone dell\'ancora',(948,310)),('osteriggio',(815,310)),
 ('strallo di prua',(750,310)),('albero',(640,310)),('sartie e lande',(690,246)),('candelieri e draglie: la battagliola',(760,ytop(760)-26)),
 ('rotaia e carrello del genoa',(540,ybot(540)-6)),('tuga',(610,390)),('winch e stopper di tuga',(452,246)),('boccaporto (tambucio<span style="color:#E4572E"><b>*</b></span>)',(375,310)),
 ('winch del genoa',(300,158)),('trasto: il carrello della randa',(290,360)),('timone a ruota',(150,252)),('pozzetto',(232,380)),
 ('ombrinali',(120,400)),('pulpito di poppa',(96,162)),('specchio di poppa',(34,310)),('gallocce d\'ormeggio',(925,ytop(925)-18))]
F=Fig(x0c,y0c,1092,620)
for i,(t,(x,y)) in enumerate(ITEMS,1): F.html+=nbadge(x0c+x,y0c+y,i,C_[(i-1)%5])
leg=''.join(f'<p style="font-size:24px; line-height:1.19; color:{INK}; font-weight:600"><span style="color:{C_[(i-1)%5]}"><b>{i}</b></span>  {t}</p>' for i,(t,_) in enumerate(ITEMS,1))
TAMB=('<p style="position:absolute; left:128px; top:922px; width:1664px; font-size:24px; line-height:1.25; color:#5E6E82"><span style="color:#E4572E"><b>*</b></span> <b>Tambucio</b> (<a href="https://www.treccani.it/vocabolario/tambucio/">tambúcio o tambùccio</a>): il piccolo casotto o la struttura scorrevole, spesso in legno o plexiglass, posta sopra il ponte; con la sua porta o lo scorrevole chiude l\'accesso sottocoperta e protegge gli interni da acqua e intemperie.</p>')
sec('coperta', head('2 · La coperta','La coperta vista dall\'alto',BLUE), pinned=TAMB+F.out(b,'Barca a vela vista dall\'alto con la prua a destra e venti particolari numerati: dal pulpito di prua con il musone e il gavone dell\'ancora, all\'albero con strallo, sartie e lande, alla tuga con osteriggi, winch, stopper e boccaporto, fino al pozzetto con trasto, timone a ruota, ombrinali, pulpito e specchio di poppa')+pcol(leg,532,0),
 notes='Battagliola: l\'insieme di draglie e candelieri che protegge il camminamento tra poppa e prua; i candelieri sono gli elementi verticali. Pulpito: protezione in tubo a estrema prua e a estrema poppa, a cui si ancorano le draglie. Musone: la ferramenta a prua estrema che comprende passacatena e rullo dell\'ancora. Gavone: vano ripostiglio. Ombrinali: piccole aperture che fanno defluire l\'acqua dalla coperta e dal pozzetto. Pozzetto: la parte esterna con le manovre e il timone. Galloccia: appiglio per dare volta a una cima. Lande: piastre in coperta a cui si fissano sartie e stralli. Trasto: il carrello della randa, su cui scorre il punto di scotta (non serve a dare volta alle scotte). Quiz 1.1.1-17, -26, -30, -31, -39, -42, -50, -63, -65, -66; 2.2.1-40, -41, -42.')

# ============ 2 · LA FERRAMENTA ============
def ico(k):
    s=f'<rect x="0" y="0" width="150" height="120" rx="24" fill="{SEA_T}"/>'
    R=lambda x1,y1,x2,y2,w=8: line(x1,y1,x2,y2,SUN,w)
    if k=='winch':
        s+=f'<circle cx="75" cy="60" r="40" fill="#C9D3DD" stroke="{NAVY}" stroke-width="4"/><circle cx="75" cy="60" r="22" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'+curved(75,60,32,-160,60,CORAL,5)
    elif k=='stopper':
        s+=f'<rect x="20" y="42" width="110" height="36" rx="12" fill="{NAVY}"/><path d="M50 42 L96 18" stroke="{CORAL}" stroke-width="10" stroke-linecap="round"/>'+R(0,60,150,60)
    elif k=='strozza':
        s+=R(0,60,150,60)+''.join(f'<circle cx="75" cy="{cy}" r="20" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/>'+''.join(line(75+20*math.cos(math.radians(a)),cy+20*math.sin(math.radians(a)),75+27*math.cos(math.radians(a)),cy+27*math.sin(math.radians(a)),NAVY,3) for a in range(0,360,30)) for cy in (31,89))
    elif k=='galloccia':
        s+=f'<rect x="60" y="66" width="30" height="30" fill="{NAVY}"/><path d="M18 60 Q75 46 132 60 L132 70 Q75 60 18 70 Z" fill="{NAVY}"/>'+f'<path d="M40 92 L110 50 M40 50 L110 92" stroke="{SUN}" stroke-width="7" stroke-linecap="round"/>'
    elif k=='bitta':
        s+=f'<ellipse cx="75" cy="104" rx="42" ry="8" fill="{NAVY}"/><rect x="58" y="44" width="34" height="60" fill="{NAVY}"/><ellipse cx="75" cy="42" rx="28" ry="11" fill="{INK}"/>'+f'<path d="M20 80 Q75 96 130 80" fill="none" stroke="{SUN}" stroke-width="7"/><path d="M20 66 Q75 50 130 66" fill="none" stroke="{SUN}" stroke-width="7"/>'
    elif k=='bozzello':
        s+=f'<path d="M75 8 L75 22" stroke="{NAVY}" stroke-width="6"/><rect x="48" y="22" width="54" height="80" rx="27" fill="{NAVY}"/><circle cx="75" cy="58" r="20" fill="#FFFFFF" stroke="{GREY}" stroke-width="4"/>'+f'<path d="M55 120 L55 58 A20 20 0 0 1 95 58 L95 120" fill="none" stroke="{SUN}" stroke-width="7"/>'
    elif k=='grillo':
        s+=f'<path d="M50 30 L50 70 A25 25 0 0 0 100 70 L100 30" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'+line(36,30,114,30,CORAL,9)+f'<circle cx="118" cy="30" r="9" fill="{CORAL}"/>'
    elif k=='golfare':
        s+=f'<rect x="30" y="86" width="90" height="16" rx="6" fill="{NAVY}"/><circle cx="75" cy="56" r="24" fill="none" stroke="{NAVY}" stroke-width="10"/>'+line(75,80,75,88,NAVY,10)
    elif k=='arridatoio':
        s+=line(75,0,75,28,GREY,4)+f'<rect x="64" y="28" width="22" height="50" rx="6" fill="none" stroke="{NAVY}" stroke-width="6"/>'+line(75,78,75,96,NAVY,6)+f'<rect x="45" y="96" width="60" height="16" rx="4" fill="{CORAL}"/><circle cx="58" cy="104" r="3" fill="#FFFFFF"/><circle cx="92" cy="104" r="3" fill="#FFFFFF"/>'
    return s
FT=[('winch','Winch','Verricello per cazzare scotte e drizze: la cima si avvolge sempre in senso orario. Il self-tailing la trattiene da solo.'),
    ('stopper','Stopper','Blocca una drizza o una scotta e libera il winch.'),
    ('strozza','Strozzascotte','Due camme dentate trattengono la cima; si libera tirandola verso l\'alto.'),
    ('galloccia','Galloccia','Appiglio per dare volta a una cima: ormeggio, drizza o scotta.'),
    ('bitta','Bitta','Colonnetta bassa e robusta con la testa a fungo, per i cavi d\'ormeggio.'),
    ('bozzello','Bozzello','Carrucola che rinvia una cima; più bozzelli fanno un paranco.'),
    ('grillo','Grillo','Chiusura a U con perno: unisce ferramenta e manovre, non riduce lo sforzo.'),
    ('golfare','Golfare','Anello fissato in coperta per agganciare bozzelli e rinvii.'),
    ('arridatoio','Arridatoio e landa','L\'arridatoio tende sartie e stralli; la landa è la piastra in coperta che li tiene.')]
tiles=''.join(card(f'<div style="display:flex; gap:18px; align-items:start">{svgi(150,120,ico(k),"Disegno: "+t,dw=150,dh=120,pan=False)}<div style="display:flex; flex-direction:column; gap:4px">{h3(t,28)}{p(d,24,BODY,400,1.3)}</div></div>',None,20,0) for k,t,d in FT)
sec('ferramenta', head('2 · La coperta','La ferramenta di coperta',BLUE)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px">{tiles}</div>',
 notes='La ferramenta di bordo è l\'insieme di strozzascotte, winch, arridatoi, gallocce e simili. Quiz 2.2.1-35, -36, -37, -76, -78 (winch), -85, -86 (stopper), -41 (la galloccia non fissa le draglie), -39 (i grilli non riducono lo sforzo), -79 (grillo della penna con perno di blocco), -43 (golfare), -42 (landa), -30 (paranco), 1.1.1-17 (galloccia), -18 (bitta).')

# ============ 3 · L'ALBERO VISTO DA PRUA ============
F=Fig(128,Y,W,Hh); mx=546; top=64; cro=250; dk=468
b=f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="{SKY}"/>'+water(W,Hh,540)
sec_d='M360 468 Q362 520 400 548 Q470 576 546 578 Q622 576 692 548 Q730 520 732 468 Q546 456 360 468 Z'
b+=f'<path d="{sec_d}" fill="{BOAT}" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>'
b+=dash(mx,dk,mx,574,NAVY,4)
b+=f'<rect x="{mx-9}" y="{top}" width="18" height="{dk-top}" rx="4" fill="{INK}"/><rect x="{mx-16}" y="{dk-8}" width="32" height="12" rx="3" fill="{NAVY}"/>'
b+=f'<rect x="{mx-14}" y="{top-8}" width="28" height="12" rx="3" fill="{NAVY}"/>'+line(mx,top-8,mx,top-44,NAVY,3)+f'<path d="M{mx} {top-44} L{mx+34} {top-38} L{mx} {top-32} Z" fill="{CORAL}"/>'+line(mx+10,top-8,mx+10,top-54,GREY,2)+f'<circle cx="{mx-12}" cy="{top-14}" r="6" fill="{SUN}"/>'
b+=line(mx-118,cro,mx+118,cro,NAVY,7)
L1,L2=(392,dk),(700,dk); l1,l2=(420,dk),(672,dk)
for side in (-1,1):
    tip=(mx+side*118,cro); la=L2 if side>0 else L1; lb=l2 if side>0 else l1
    b+=line(mx,top+4,tip[0],tip[1],NAVY,3)+line(tip[0],tip[1],la[0],la[1]-30,NAVY,3)
    b+=line(mx,cro+8,lb[0],lb[1]-30,PURPLE,3)
    for (xx,yy) in (la,lb):
        b+=f'<rect x="{xx-5}" y="{yy-30}" width="10" height="24" rx="4" fill="{SOFT}"/><rect x="{xx-9}" y="{yy-8}" width="18" height="10" fill="{CORAL}"/>'
F.lead((mx,top-2),(640,40),'testa d\'albero',NAVY,'l')
F.lead((mx+80,cro),(760,210),'crocette',NAVY,'l')
F.lead((470,150),(330,150),'sartie alte',NAVY,'r')
F.lead((470,360),(330,360),'sartie basse',PURPLE,'r')
F.lead((L2[0],L2[1]-18),(760,430),'arridatoio',SOFT,'l'); F.lead((L2[0],L2[1]-3),(760,492),'landa',CORAL,'l')
F.lead((mx,dk-2),(330,500),'piede d\'albero',NAVY,'r')
F.lead((mx,560),(330,570),'albero passante',NAVY,'r')
F.lead((mx,400),(330,430),'albero',INK,'r')
txt=(term('Albero e testa d\'albero','In testa: segnavento, luci di via e di fonda, antenna del VHF. Dentro l\'albero passano le drizze, non le manovre fisse.')
     +term('Crocette','Allargano l\'angolo delle sartie e le mettono in tensione.')
     +term('Sartie','Cavi d\'acciaio o di fibra che sostengono l\'albero di lato. In coperta l\'arridatoio le tende e la landa le tiene.')
     +term('Piede d\'albero','Appoggiato in coperta oppure passante, con il piede sulla chiglia.'))
sec('albero', head('3 · Alberatura e manovre fisse','L\'albero visto da prua',PURPLE), pinned=F.out(b,'Albero visto da prua sopra la sezione dello scafo: testa d\'albero con segnavento, luci e antenna; crocette a metà altezza; sartie alte dalla testa d\'albero alle estremità delle crocette e giù in coperta; sartie basse sotto le crocette; arridatoi e lande in coperta; piede d\'albero, con l\'albero che può proseguire fino alla chiglia')+pcol(txt),
 notes='Quiz 2.2.1-5 e -6 (le crocette tensionano le sartie, non trattengono le scotte), -69 (sartie: cavi che sostengono l\'albero), -72 (sartie e stralli non passano dentro l\'albero), -42 (landa), -7 (le sartie non si regolano con il carrello della scotta), -74 (l\'albero si regola sulle manovre fisse, non sulle correnti), -37 (arridatoi).')

# ============ 3 · LE MANOVRE FISSE ============
F=Fig(X,Y,W,Hh)
SH3=((150,440),(520,458),(960,420)); s3=lambda x: qy(SH3,x); wl=486
b=f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="{SKY}"/>'+water(W,Hh,wl)
h3_='M150 440 Q520 458 960 420 Q942 470 900 486 Q870 506 800 512 L260 510 Q200 504 176 486 Z'
b+=f'<path d="M520 508 L590 508 L580 580 L530 580 Z" fill="{NAVY}"/><ellipse cx="556" cy="584" rx="54" ry="13" fill="{INK}"/><path d="M226 506 L262 506 L258 572 L232 578 Z" fill="{NAVY}"/>'
b+=f'<path d="{h3_}" fill="{BOAT}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
mx3=560; mt=36; fz=mt+62; dk3=s3(mx3)
b+=f'<rect x="{mx3-6}" y="{mt}" width="12" height="{dk3-mt}" rx="3" fill="{INK}"/>'+line(mx3,dk3-70,300,dk3-70,INK,8)
b+=line(mx3,fz,948,s3(948)-4,CORAL,4)+line(mx3,mt+4,162,s3(162)-4,CORAL,4)
b+=line(mx3,mt+6,mx3+26,260,NAVY,3)+line(mx3+26,260,mx3+14,dk3,NAVY,3)+line(mx3,268,mx3-20,dk3,PURPLE,3)+line(mx3,260,mx3+30,260,NAVY,6)
b+=f'<path d="M{mx3} {fz} L260 {s3(260):.1f}" stroke="{SEA}" stroke-width="3" stroke-dasharray="12 8" fill="none"/>'
b+=f'<rect x="{mx3+8}" y="{dk3-6:.1f}" width="12" height="8" fill="{CORAL}"/><rect x="{mx3-26}" y="{dk3-6:.1f}" width="12" height="8" fill="{CORAL}"/>'
F.lead((760,(fz+s3(948))/2+10),(860,230),'strallo di prua',CORAL,'l')
F.lead((360,250),(250,170),'paterazzo',CORAL,'r')
F.lead((mx3+18,200),(700,140),'sartie alte',NAVY,'l')
F.lead((mx3+29,260),(700,300),'crocette',NAVY,'l')
F.lead((550,380),(640,410),'sartie basse',PURPLE,'l')
F.lead((400,s3(400)-80),(300,300),'volanti',SEA,'r')
F.lead((mx3,fz),(620,70),'armo frazionato',CORAL,'l')
F.lead((380,dk3-70),(360,390),'boma',INK,'r')
txt=(term('Manovre fisse','Tengono su l\'albero e non si toccano durante la navigazione: stralli, paterazzo e sartie.')
     +term('Strallo e paterazzo','Lo strallo di prua tiene l\'albero verso prua, il paterazzo verso poppa. Cazzando il paterazzo si smagrisce la randa.')
     +term('Armo in testa o frazionato','Nell\'armo frazionato lo strallo non arriva in testa d\'albero. Le volanti aiutano a sostenerlo.'))
sec('fisse', head('3 · Alberatura e manovre fisse','Le manovre fisse',PURPLE)+col(txt), pinned=F.out(b,'Barca a vela di profilo senza vele, con armo frazionato: strallo di prua attaccato sotto la testa d\'albero, paterazzo dalla testa d\'albero alla poppa, sartie alte con le crocette, sartie basse, volanti tratteggiate verso poppa, boma e albero'),
 notes='Stralli e sartie sono manovre fisse; drizze e scotte sono correnti. Armo frazionato: lo strallo non è incappellato in testa d\'albero. Le sartie volanti sostengono l\'albero controbilanciando lo sforzo sullo strallo; con crocette acquartierate e paterazzo possono dare supporto senza essere strutturali. Il paterazzo non serve a regolare il vang. Quiz 2.2.1-1, -2, -3, -4, -28, -29, -52, -53, -77.')

# ============ 4 · LA RANDA ============
F=Fig(128,Y,W,Hh)
H_,T_,C_=(336,48),(336,494),(900,494); LC=(650,210)
lq=lambda k: qbez(C_,LC,H_,k)
def lq_y(y):
    lo,hi=0.0,1.0
    for _ in range(40):
        m=(lo+hi)/2
        if lq(m)[1]>y: lo=m
        else: hi=m
    return lq(lo)
b=f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="#F4FAFC"/>'+line(150,585,1000,585,GREY,4)
b+=line(330,16,330,590,INK,12)+line(330,500,940,500,INK,10)
b+=f'<path d="M{H_[0]} {H_[1]} L{T_[0]} {T_[1]} L{C_[0]} {C_[1]} Q{LC[0]} {LC[1]} {H_[0]} {H_[1]} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
for k in (0.2,0.4,0.6,0.8):
    (x1,y1),(x2,y2)=lq(k-0.01),lq(k+0.01); tx,ty=x2-x1,y2-y1; n=math.hypot(tx,ty); nx,ny=-ty/n,tx/n
    if nx>0: nx,ny=-nx,-ny
    px,py=lq(k); b+=line(px+nx*8,py+ny*8,px+nx*(110 if k<0.7 else 80),py+ny*(110 if k<0.7 else 80),PURPLE,7)
xl,yl=lq_y(420)
b+=''.join(f'<circle cx="{x}" cy="420" r="4" fill="{SEA}"/>'+line(x,424,x,436,SEA,2) for x in range(372,int(xl)-20,34))
b+=f'<circle cx="340" cy="420" r="7" fill="none" stroke="{SEA}" stroke-width="3"/><circle cx="{xl-6:.1f}" cy="420" r="7" fill="none" stroke="{SEA}" stroke-width="3"/>'
b+=f'<path d="M{xl-6:.1f} 427 L{xl-6:.1f} 512 L360 512" fill="none" stroke="{GREEN}" stroke-width="4"/>'
b+=line(340,468,346,585,GREEN,3)+f'<circle cx="340" cy="466" r="6" fill="none" stroke="{GREEN}" stroke-width="3"/>'
b+=line(339,48,339,494,SEA,6)+f'<rect x="336" y="36" width="34" height="26" rx="6" fill="{CORAL_T}" stroke="{NAVY}" stroke-width="3"/>'
b+=f'<circle cx="330" cy="500" r="13" fill="{NAVY}"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="13" fill="{CORAL}"/>' for x,y in (H_,T_,C_))
F.lead((352,48),(430,34),'angolo di penna e tavoletta',CORAL,'l')
F.lead(T_,(300,470),'angolo di mura',CORAL,'r'); F.lead(C_,(760,548),'angolo di scotta · tesabase',CORAL,'l')
F.lead((339,250),(300,250),'inferitura e ralinga',SEA,'r'); F.lead(lq(0.5),(720,190),'balumina',PURPLE,'l')
F.tag((560,548),'base',PURPLE,'c'); F.lead((650,300),(790,300),'stecche',PURPLE,'l')
F.lead((560,420),(790,390),'terzaroli e matafioni',SEA,'l'); F.lead((xl-6,470),(790,460),'borosa',GREEN,'l')
F.lead((343,520),(300,540),'cunningham',GREEN,'r'); F.lead((330,500),(300,596),'trozza',NAVY,'r')
txt=(term('Tre angoli','Penna in alto, con la tavoletta e la drizza; mura in basso a prua, vicino alla trozza; scotta in basso a poppa, dove lavora il tesabase.')
     +term('Tre lati','Inferitura lungo l\'albero, con la ralinga che scorre nella canaletta; base lungo il boma; balumina libera, con le stecche.')
     +term('Terzaroli','Per ridurre la randa si prende una mano di terzaroli: la borosa tira giù la vela, i matafioni raccolgono il tessuto.'))
sec('randa', head('4 · Le vele','La randa: angoli e lati',CORAL), pinned=F.out(b,'Randa inferita su albero e boma: angolo di penna con la tavoletta, angolo di mura vicino alla trozza, angolo di scotta con il tesabase; inferitura con la ralinga, base e balumina con le stecche; una mano di terzaroli con i matafioni e la borosa; il cunningham sopra la mura')+pcol(txt),
 notes='Quiz 2.2.1-9 (la balumina non è il lato più corto), -10 (ralinga nella canaletta dell\'albero), -11 (la base non è il lato con le stecche), -12 (angolo di scotta tra base e balumina, con il tesabase), -13 (penna: in alto, con la drizza), -14 (mura: in basso a prua), -16 (la randa è la vela principale, a poppavia dell\'albero), -33 (cunningham), -45 (trozza), -66 (il matafione non è un fiocco), -68 (la borosa non fa parte dello strallo cavo), -79 (grillo della penna con perno di blocco); 2.1.1-43 e -44 (stecche: forma della vela).')

# ============ 4 · IL GENOA ============
F=Fig(X,Y,W,Hh)
FS=((406,40),(1040,556)); fs=lambda t: (FS[0][0]+(FS[1][0]-FS[0][0])*t, FS[0][1]+(FS[1][1]-FS[0][1])*t)
Hg,Tg,Cg=fs(0.04),fs(0.95),(250,528); LG,FG=(290,280),(640,580)
b=f'<rect x="0" y="0" width="{W}" height="{Hh}" fill="{SKY}"/>'
b+=f'<path d="M20 560 L1070 560 L1050 620 L40 620 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M394 50 L394 470 L90 470 Q250 200 394 50 Z" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'+line(394,470,86,470,GREY,6)
b+=line(400,16,400,560,INK,12)+line(*FS[0],*FS[1],NAVY,3)
sail=f'M{Hg[0]:.1f} {Hg[1]:.1f} L{Tg[0]:.1f} {Tg[1]:.1f} Q{FG[0]} {FG[1]} {Cg[0]} {Cg[1]} Q{LG[0]} {LG[1]} {Hg[0]:.1f} {Hg[1]:.1f} Z'
b+=f'<path d="{sail}" fill="#FFE08A" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=f'<path d="M{Tg[0]:.1f} {Tg[1]:.1f} Q{FG[0]} {FG[1]} {Cg[0]} {Cg[1]} Q{LG[0]} {LG[1]} {Hg[0]:.1f} {Hg[1]:.1f}" fill="none" stroke="{SEA}" stroke-width="12" stroke-opacity="0.55"/>'
b+=f'<rect x="996" y="528" width="26" height="30" rx="5" fill="{INK}"/>'+line(996,568,620,568,GREEN,4)
b+=line(160,556,240,556,NAVY,6)+f'<rect x="185" y="548" width="20" height="14" rx="3" fill="{CORAL}"/>'+f'<polyline points="{Cg[0]},{Cg[1]} 195,552 80,540" fill="none" stroke="{ORANGE}" stroke-width="4"/>'+f'<circle cx="72" cy="540" r="15" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/>'
b+=dim(250,400,400,400,CORAL)+''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{CORAL}"/>' for x,y in (Hg,Tg,Cg))
F.lead(Hg,(470,40),'angolo di penna',CORAL,'l'); F.lead(fs(0.5),(800,250),'inferitura sullo strallo',NAVY,'l')
F.lead(Tg,(985,470),'angolo di mura',CORAL,'r'); F.lead(Cg,(238,480),'angolo di scotta',CORAL,'r')
F.tag((242,400),'sovrapposizione',CORAL,'r'); F.lead(qbez(Cg,LG,Hg,0.5),(238,300),'balumina',NAVY,'r')
F.lead(qbez(Tg,FG,Cg,0.5),(640,512),'base',NAVY,'c'); F.lead(qbez(Cg,LG,Hg,0.7),(238,170),'fascia anti UV',SEA,'r')
F.tag((170,230),'randa',GREY,'c')
F.lead((1008,545),(985,600),'avvolgifiocco',INK,'r'); F.lead((700,568),(620,600),'cima d\'avvolgimento',GREEN,'c')
F.lead((195,556),(90,600),'scotta e carrello',ORANGE,'l')
txt=(term('Tre angoli, come la randa','Penna in alto sulla drizza, mura in basso sullo strallo (sul tamburo dell\'avvolgifiocco), scotta dove lavorano le scotte.')
     +term('Tre lati','Inferitura lungo lo strallo: con i garrocci, oppure nella canaletta dello strallo cavo, dove entra con il feeder. Poi base e balumina.')
     +term('Genoa o fiocco','Il genoa oltrepassa l\'albero di circa metà della distanza tra albero e mura. Il fiocco non si sovrappone alla randa.'))
sec('genoa', head('4 · Le vele','Il genoa: angoli e lati',CORAL)+col(txt), pinned=F.out(b,'Genoa inferito sullo strallo di prua con i tre angoli penna, mura sul tamburo dell\'avvolgifiocco e scotta; i lati inferitura, base e balumina con la fascia anti UV; la sovrapposizione oltre l\'albero sulla randa tratteggiata; la scotta sul carrello della rotaia fino al winch e la cima d\'avvolgimento'),
 notes='Quiz 2.2.1-17, -18, -19, -20 (genoa e fiocco: sovrapposizione del 50%), -51 (garrocci), -62 (feeder dello strallo cavo), -63 (il tesabase non è del fiocco), -81 e -82 (fiocco autovirante: la scotta va a una puleggia, in virata non si tocca), -83 (oltre il 30% di riduzione il genoa avvolto perde efficienza), -84 (avvolgifiocco), -48 (il sole degrada le vele: da qui la fascia anti UV).')

# ============ 4 · LE VELE DI BORDO ============
def mini(head,rig='sloop',hc=SUN,main_c='#FFFFFF'):
    s,_=yacht(30,172,220,head,rig,main_c,hc,NAVY,2)
    return f'<rect x="0" y="0" width="320" height="200" fill="{SKY}"/>'+s+f'<rect x="0" y="172" width="320" height="28" fill="{WATER}" fill-opacity="0.45"/>'
VC=[('fiocco','Fiocco','Vela di prua che non si sovrappone alla randa. Con l\'autovirante la scotta va a una puleggia.',SUN),
    ('genoa','Genoa','Più grande del fiocco: supera l\'albero verso poppa. Si riduce con l\'avvolgifiocco.',CORAL),
    ('torm','Tormentina','Piccola e robusta: la vela di prua per il cattivo tempo.',BLUE),
    ('spi','Spinnaker','Simmetrico, per le andature portanti, con il tangone. Il braccio ne regola la mura.',PURPLE),
    ('genn','Gennaker','Asimmetrico e senza tangone: tra il traverso e il lasco, 60°–120° dal vento.',GREEN),
    ('code0','Code 0','Asimmetrico e piatto, non inferito: con poco vento, tra bolina larga e traverso.',SEA)]
cc=''.join(card(f'<div style="display:flex; gap:20px; align-items:center">{svgi(320,200,mini(k,hc=c),"Barca con "+t.lower(),dw=264,dh=165,pan=False)}<div style="display:flex; flex-direction:column; gap:4px">{h3(t,30,c if c!=SUN else INK)}{p(d,24,BODY,400,1.3)}</div></div>',None,16,0) for k,t,d,c in VC)
sec('vele', head('4 · Le vele','Le vele di bordo',CORAL)+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px">{cc}</div>',
 notes='La randa è la vela principale, a poppavia dell\'albero. Set di vele: sloop con randa e genoa; catamarano con randa, fiocco e gennaker. Vele leggere: la calza raccoglie spinnaker e gennaker prima di ammainarli. Tessuti: il dacron è il più diffuso per la crociera; il sole prolungato ne degrada la resistenza. Quiz 2.2.1-15, -16, -17, -20, -21, -22, -23, -24, -46, -47, -48, -49, -50, -80.')

# ============ 5 · LE MANOVRE CORRENTI DELLA RANDA ============
F=Fig(128,290,1664,620)
Hm,Tm,Cm=(1048,44),(1048,434),(430,434); LM_=(700,200)
b=f'<rect x="0" y="0" width="{PW}" height="620" fill="{SKY}"/>'
b+=f'<path d="M100 556 L1560 548 Q1540 590 1500 606 L180 612 Q130 600 100 556 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b+=f'<path d="M{Hm[0]} {Hm[1]} L{Tm[0]} {Tm[1]} L{Cm[0]} {Cm[1]} Q{LM_[0]} {LM_[1]} {Hm[0]} {Hm[1]} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b+=line(1040,24,1040,556,INK,14)+line(1040,440,420,440,INK,12)
b+=''.join(line(1040,230,x,440,GREY,2) for x in (620,780,920))
b+=f'<path d="M1040 50 L426 436" stroke="{GREEN}" stroke-width="3" stroke-dasharray="12 8" fill="none"/>'
b+=f'<path d="M1034 40 L1034 528 L1022 552 L870 552" fill="none" stroke="{GREEN}" stroke-width="4" stroke-dasharray="0" />'+f'<circle cx="852" cy="544" r="15" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/><rect x="880" y="540" width="40" height="12" rx="3" fill="{NAVY}"/>'
b+=line(930,446,1034,540,ORANGE,8)
b+=line(500,556,620,556,NAVY,7)+f'<rect x="548" y="546" width="24" height="14" rx="3" fill="{CORAL}"/>'+f'<circle cx="560" cy="456" r="11" fill="{NAVY}"/><circle cx="560" cy="536" r="11" fill="{NAVY}"/>'+''.join(line(x,456,x,536,ORANGE,3) for x in (553,558,563,568))
b+=f'<polyline points="{Cm[0]},{Cm[1]-4} 520,430" fill="none" stroke="{GREEN}" stroke-width="4"/><circle cx="522" cy="430" r="6" fill="{NAVY}"/>'
b+=line(1052,410,1046,540,GREEN,3)+f'<circle cx="1050" cy="408" r="6" fill="none" stroke="{GREEN}" stroke-width="3"/>'
b+=f'<path d="M541 344 L541 452" stroke="{GREEN}" stroke-width="4" fill="none"/><circle cx="541" cy="344" r="7" fill="none" stroke="{GREEN}" stroke-width="3"/>'
b+=f'<circle cx="1040" cy="440" r="13" fill="{NAVY}"/>'
F.lead((1034,150),(1110,120),'drizza della randa',GREEN,'l'); F.lead((1040,230),(1110,250),'lazy jack',GREY,'l')
F.lead((1052,420),(1110,380),'cunningham',GREEN,'l'); F.lead((1040,440),(1110,440),'trozza',NAVY,'l'); F.lead((985,494),(1110,500),'vang',ORANGE,'l')
F.lead((600,328),(400,280),'amantiglio',GREEN,'r'); F.lead((541,400),(400,340),'borosa',GREEN,'r')
F.lead((470,432),(400,400),'tesabase',GREEN,'r'); F.lead((560,500),(400,480),'scotta della randa e paranco',ORANGE,'r')
F.lead((520,556),(400,560),'trasto e carrello',NAVY,'r'); F.lead((860,548),(860,592),'stopper e winch',NAVY,'c')
F.tag((1150,592),'verde: regolazioni · arancio: scotta e vang',NAVY,'l',20)
sec('corr_randa', head('5 · Le manovre correnti','Le manovre correnti della randa',GREEN), pinned=F.out(b,'Randa armata vista di lato con le manovre correnti: la drizza scende dentro l\'albero fino a stopper e winch; l\'amantiglio dalla testa d\'albero all\'estremità del boma; il vang dal boma al piede d\'albero; la scotta con il paranco sul carrello del trasto; tesabase, cunningham, borosa e lazy jack'),
 notes='Le manovre correnti servono a manovrare le vele: drizze, scotte, vang, tesabase e le altre. La drizza issa la randa; la scotta la regola, con il paranco che demoltiplica lo sforzo e il carrello del trasto che sposta il punto di scotta. Il vang trattiene il boma verso il basso e regola flessione dell\'albero e superficie portante. L\'amantiglio sostiene il boma. Il tesabase tende la base, il cunningham la parte prodiera bassa. La borosa cala la vela nella mano di terzaroli. I lazy jack raccolgono la randa in ammainata. Quiz 2.2.1-28, -29, -30, -33, -40, -60, -61, -71, -73, -75.')

# ============ 5 · GENOA E SPINNAKER ============
F1=Fig(128,290,800,620)
FS2=((266,36),(740,536)); f2=lambda t: (FS2[0][0]+(FS2[1][0]-FS2[0][0])*t, FS2[0][1]+(FS2[1][1]-FS2[0][1])*t)
Hg,Tg,Cg=f2(0.05),f2(0.95),(170,512)
b1=f'<rect x="0" y="0" width="800" height="620" fill="{SKY}"/>'+f'<path d="M10 540 L790 540 L770 610 L30 610 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b1+=line(260,16,260,540,INK,12)+line(*FS2[0],*FS2[1],NAVY,3)
b1+=f'<path d="M{Hg[0]:.1f} {Hg[1]:.1f} L{Tg[0]:.1f} {Tg[1]:.1f} Q470 560 {Cg[0]} {Cg[1]} Q200 270 {Hg[0]:.1f} {Hg[1]:.1f} Z" fill="#FFE08A" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b1+=f'<path d="M262 40 L{Hg[0]:.1f} {Hg[1]:.1f}" stroke="{GREEN}" stroke-width="4"/><path d="M254 44 L254 526 L240 548 L110 548" fill="none" stroke="{GREEN}" stroke-width="4" stroke-dasharray="12 7"/>'
b1+=f'<rect x="704" y="511" width="26" height="30" rx="5" fill="{INK}"/>'+line(704,552,330,552,GREEN,4)
b1+=line(80,538,160,538,NAVY,6)+f'<rect x="110" y="530" width="20" height="14" rx="3" fill="{CORAL}"/><polyline points="{Cg[0]},{Cg[1]} 120,534 58,522" fill="none" stroke="{ORANGE}" stroke-width="4"/><circle cx="50" cy="522" r="14" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/>'
F1.tag((400,40),'genoa',CORAL,'c')
F1.lead((262,120),(360,120),'drizza del genoa',GREEN,'l'); F1.lead((716,520),(790,380),'avvolgifiocco',INK,'r')
F1.lead((520,552),(520,598),'cima d\'avvolgimento',GREEN,'c'); F1.lead((120,536),(14,598),'scotta, rotaia e carrello',ORANGE,'l')
F2=Fig(992,290,800,620)
b2=f'<rect x="0" y="0" width="800" height="620" fill="{SKY}"/>'+f'<path d="M10 540 L790 540 L770 610 L30 610 Z" fill="{BOAT}" stroke="{NAVY}" stroke-width="4"/>'
b2+=line(240,16,240,540,INK,12)
spi='M250 40 Q700 40 640 330 Q640 450 560 472 Q380 300 250 40 Z'
b2+=f'<path d="{spi}" fill="#D9CCF5" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
b2+=line(240,330,640,330,INK,8)+f'<circle cx="640" cy="330" r="9" fill="{CORAL}"/>'
b2+=line(240,170,632,326,GREEN,3)+line(560,334,540,540,GREEN,3)
b2+=line(640,334,90,530,ORANGE,4)+line(560,472,60,520,ORANGE,4)+f'<circle cx="54" cy="522" r="14" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/>'
F2.tag((620,40),'spinnaker',PURPLE,'c')
F2.lead((246,42),(230,40),'drizza dello spi',GREEN,'r'); F2.lead((400,330),(400,365),'tangone',INK,'c')
F2.lead((436,247),(230,200),'amantiglio',GREEN,'r'); F2.lead((548,440),(600,500),'caricabasso',GREEN,'l')
F2.lead((640,330),(660,290),'varea',CORAL,'l'); F2.lead((300,469),(230,420),'braccio',ORANGE,'r'); F2.lead((260,500),(230,500),'scotta',ORANGE,'r')
sec('corr_prua', head('5 · Le manovre correnti','Genoa e spinnaker: le manovre',GREEN),
 pinned=F1.out(b1,'Genoa armato: la drizza scende dentro l\'albero, l\'avvolgifiocco alla mura con la cima d\'avvolgimento verso poppa, la scotta passa dal carrello sulla rotaia al winch')
       +F2.out(b2,'Spinnaker armato: drizza in testa d\'albero, tangone dall\'albero alla mura con l\'amantiglio sopra e il caricabasso sotto, varea all\'estremità del tangone; il braccio parte dalla mura sul tangone, la scotta dall\'altro angolo, entrambi verso poppa'),
 notes='Genoa: drizza per issarlo, scotte (quella che lavora è sottovento) che passano dal carrello sulla rotaia, avvolgifiocco con la sua cima per ridurlo senza ammainarlo. Spinnaker: drizza, scotta, braccio (regola la mura, cioè l\'angolo sul tangone), tangone con amantiglio (lo sostiene) e caricabasso (lo tiene giù); la varea è l\'estremità del tangone. Le manovre dello spinnaker non sono «scotta, spring, vang, borosa e meolo». Quiz 2.2.1-34 (il tangone non porta la base della randa), -44 (la varea non è l\'anello del mantiglio), -64, -65, -80, -84; 2.3.1-35 e -36 (strallare e quadrare il tangone).')

# ============ 6 · GLI ARMI ============
def mini2(head,rig,hc,main_c='#FFFFFF'):
    s,_=yacht(40,172,210,head,rig,main_c,hc,NAVY,2)
    return f'<rect x="0" y="0" width="320" height="200" fill="{SKY}"/>'+s+f'<rect x="0" y="172" width="320" height="28" fill="{WATER}" fill-opacity="0.45"/>'
AR=[('genoa','sloop','Sloop','Un albero e una sola vela di prua alla volta: l\'armo più diffuso. Set base: randa e genoa.',CORAL),
    ('','cutter','Cutter','Un albero e due vele di prua insieme, su due stralli.',PURPLE),
    ('fiocco','ketch','Ketch','Due alberi: la mezzana, più bassa, sta a proravia dell\'asse del timone.',GREEN),
    ('fiocco','yawl','Yawl','Due alberi, ma la piccola mezzana sta a poppavia dell\'asse del timone.',BLUE)]
cc=''.join(card(f'<div style="display:flex; gap:22px; align-items:center">{svgi(320,200,mini2(hd,rg,c),f"Barca armata {t.lower()}",dw=352,dh=220,pan=False)}<div style="display:flex; flex-direction:column; gap:6px">{h3(t,34,c)}{p(d,26,BODY,400,1.35)}</div></div>',None,18,0) for hd,rg,t,d,c in AR)
sec('armi', head('6 · Armi, cime e parole','Gli armi',NAVY)+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:18px">{cc}</div>'
    +note('E il catamarano: due scafi e grande stabilità di forma. Set di vele: randa, fiocco e gennaker.',CORAL,34),
 notes='Piano velico: numero di alberi e tipo di vele. Armo in testa o frazionato: vedi le manovre fisse. Quiz 2.2.1-25 (sloop), -26 (cutter), -27 (ketch: mezzana a proravia dell\'asse del timone), -49 e -50 (set di vele), 1.1.1-54 (catamarano: due scafi); 2.1.1-45 (il multiscafo ha maggiore stabilità di forma). Lo yawl non è in banca: ha la mezzana a poppavia del timone.')

# ============ 6 · CIME E NODI ============
CN=[('Cima','Qualunque cavo tessile di bordo: drizze, scotte, ormeggi.',CORAL),('Sagola','Una cima di piccolo diametro.',SEA),
    ('Cavo','Di fibra o d\'acciaio: d\'acciaio sono sartie e stralli.',PURPLE),('Impiombatura','Intreccio dei trefoli: unisce due cavi o fa un occhio fisso.',BLUE),
    ('Polipropilene','Galleggia: si usa solo per le sagole di salvataggio.',GREEN),
    ('Gassa d\'amante','Fa un occhio che non scorre e non si scioglie.',CORAL),('Savoia','In fondo alle scotte: non le fa sfilare dal passacavo.',SEA),
    ('Parlato','Lega i parabordi alle draglie.',PURPLE),('Margherita','Accorcia una cima senza tagliarla.',BLUE),('Nodo piano','Unisce due cime dello stesso diametro.',GREEN)]
tile=lambda t,d,c: f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:22px 22px 24px 22px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{squiggle(c,110)}{h3(t,30,c)}{p(d,24,BODY,400,1.35)}</div>'
row=lambda items: f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr 1fr; gap:18px">{"".join(tile(*x) for x in items)}</div>'
sec('cime', head('6 · Armi, cime e parole','Cime e nodi',NAVY)+tag('Le cime',SEA)+row(CN[:5])+tag('I nodi',CORAL)+row(CN[5:]),
 notes='A bordo si dice cima, non corda. Quiz 1.1.1-40 (sagola), 2.2.1-38 (polipropilene), -67 (impiombatura), -54 e -55 (gassa d\'amante: tiene, non si scioglie, non accorcia), -56 (nodo piano: non per cime di diametro diverso), -57 (savoia), -58 (parlato per i parabordi), -59 (margherita), -69 (sartie in acciaio o fibra), -70 (il tornichetto non unisce due cime).')

# ============ 6 · LE PAROLE DELLE MANOVRE ============
VB=[('Issare · ammainare','Alzare una vela con la drizza; abbassarla.',CORAL),('Cazzare · lascare','Tirare una cima per tendere la vela; allentarla.',SEA),
    ('Dare volta · mollare','Fissare una cima alla galloccia; liberarla.',PURPLE),('Orzare · poggiare','Portare la prua verso il vento; allontanarla dal vento.',BLUE),
    ('Virare · abbattere','Cambiare mure passando con la prua nel vento; con la poppa.',GREEN),('Terzarolare','Ridurre la randa prendendo una mano di terzaroli.',CORAL),
    ('Sventare','Prua al vento o scotte mollate: le vele non portano più.',SEA),('Strallare · quadrare','Portare il tangone verso lo strallo; verso poppa.',PURPLE)]
g=''.join(tile(t,d,c) for t,d,c in VB)
sec('verbi', head('6 · Armi, cime e parole','Le parole delle manovre',NAVY)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{g}</div>'
    +note('Mure a dritta: il vento arriva da dritta. Sopravvento il lato del vento, sottovento l\'altro.',CORAL,34),
 notes='Quiz 2.3.1-1 e -2 (sventare: prua al vento o scotte mollate, non poppa al vento), -3 (per poggiare la barra va sopravento, dalla parte opposta alla randa), -35 e -36 (strallare: il tangone verso lo strallo; quadrare è il contrario). Orzare, poggiare, virata e abbattuta sono spiegati nella lezione 8.')

# ============ 7 · RIPASSO ============
quiz_slide('quiz1','Verifica 1 · Lo scafo e la coperta',['1.1.1-14','1.1.1-33','1.1.1-50','1.1.1-63'],False)
quiz_slide('quiz1r','Verifica 1 · Le risposte',['1.1.1-14','1.1.1-33','1.1.1-50','1.1.1-63'],True)
quiz_slide('quiz2','Verifica 2 · Attrezzatura e vele',['2.2.1-42','2.2.1-45','2.2.1-65','2.2.1-44'],False)
quiz_slide('quiz2r','Verifica 2 · Le risposte',['2.2.1-42','2.2.1-45','2.2.1-65','2.2.1-44'],True)

GL=[('Albero','l\'asta verticale che porta le vele'),('Amantiglio','sostiene dall\'alto il boma o il tangone'),('Angolo di mura','l\'angolo basso e prodiero della vela'),
('Angolo di penna','l\'angolo in alto, con la drizza'),('Angolo di scotta','l\'angolo basso e poppiero, con la scotta'),('Arridatoio','tende sartie e stralli sulle lande'),
('Asse longitudinale','da prua a poppa, parallelo alla chiglia'),('Avvolgifiocco','riduce la vela di prua arrotolandola'),('Baglio massimo','la larghezza massima dello scafo'),
('Balumina','il lato libero della vela, verso poppa'),('Base','il lato inferiore della vela'),('Battagliola','draglie e candelieri lungo il camminamento'),
('Bitta','colonnetta con la testa a fungo per l\'ormeggio'),('Boccaporto','apertura in coperta per scendere sotto'),('Boma','l\'asta orizzontale della base della randa'),
('Bordo libero','dalla coperta alla linea di galleggiamento'),('Borosa','cala la vela nella mano di terzaroli'),('Bozzello','carrucola che rinvia una cima'),
('Braccio','regola la mura dello spinnaker'),('Bulbo','la zavorra in fondo alla chiglia'),('Candelieri','i montanti verticali della battagliola'),
('Carena','l\'opera viva'),('Crocette','allargano e tendono le sartie'),('Cunningham','tende la parte bassa prodiera della randa'),
('Draglie','i cavi tesi tra i candelieri'),('Dritto di prua','la struttura dell\'estrema prua'),('Drizza','la cima che issa una vela'),
('Galloccia','appiglio per dare volta a una cima'),('Gavone','vano ripostiglio di prua o di poppa'),('Genoa','vela di prua che oltrepassa l\'albero'),
('Giardinetto','a 135° dalla prua, a dritta e a sinistra'),('Grillo','chiusura a U con il perno'),('Inferitura','il lato della vela su albero o strallo'),
('Landa','la piastra in coperta di sartie e stralli'),('Lazy jack','sagole che raccolgono la randa sul boma'),('Losca','il foro dell\'asse del timone'),
('Mascone','a 45° dalla prua, a dritta e a sinistra'),('Matafioni','cordini che legano la vela terzarolata'),('Murata','il fianco dello scafo sopra l\'acqua'),
('Musone','ferramenta di prua con passacatena e rullo'),('Ombrinale','foro di scarico dell\'acqua in coperta'),('Opera morta','la parte emersa dello scafo'),
('Opera viva','la parte immersa: la carena'),('Osteriggio','apertura in coperta per luce e aria'),('Pagliolato','il pavimento interno, fatto di paglioli'),
('Paratia','parete verticale interna dello scafo'),('Paterazzo','tiene l\'albero verso poppa'),('Pescaggio','dal galleggiamento al punto più basso'),
('Pozzetto','la zona esterna con timone e manovre'),('Pulpito','protezione in tubo a prua e a poppa'),('Ralinga','il cavo cucito nell\'inferitura'),
('Randa','la vela principale, a poppavia dell\'albero'),('Sartie','sostengono l\'albero di lato'),('Scotta','la cima che regola la vela'),
('Sentina','lo spazio tra il fondo e il pagliolato'),('Specchio di poppa','la poppa sopra il dritto di poppa'),('Stecche','listelli nelle tasche della balumina'),
('Stopper','blocca drizze e scotte'),('Strallo','tiene l\'albero verso prua'),('Tangone','asta che porta fuori la mura dello spi'),
('Terzaroli','riducono la randa: si cala una mano'),('Tesabase','tende la base della randa sul boma'),('Timone','la pala che governa la barca'),
('Trasto','la rotaia del carrello della randa'),('Trozza','lo snodo tra boma e albero'),('Tuga','sovrastruttura abitabile sopra la coperta'),
('Vang','trattiene il boma verso il basso'),('Varea','l\'estremità del boma o del tangone'),('Volanti','sartie mobili che reggono l\'albero a poppa'),
('Winch','verricello per cazzare le cime'),('Zinco','anodo contro la corrosione galvanica'),('Traverso','a 90° dalla prua')]
GL=sorted(GL,key=lambda x: x[0].lower())
GC=[CORAL,SEA,PURPLE,BLUE,GREEN]
for i,sid in enumerate(('gloss1','gloss2','gloss3')):
    part=GL[i*24:(i+1)*24]
    colh=lambda items: '<div style="display:flex; flex-direction:column; gap:10px">'+''.join(f'<p style="font-size:27px; line-height:1.3; color:{BODY}"><span style="color:{GC[(i*24+j)%5]}"><b>{t}</b></span> · {d}</p>' for j,(t,d) in enumerate(items))+'</div>'
    rng=f'{part[0][0][0]}–{part[-1][0][0]}'
    sec(sid, head(f'7 · Ripasso · glossario {i+1} di 3 · {rng}','Glossario',CORAL)+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:48px">{colh(part[:12])}{colh(part[12:])}</div>',
        notes='Definizioni brevi, in ordine alfabetico; i disegni delle slide precedenti mostrano dove si trova ogni parte. '+' '.join(f'{t}: {d}.' for t,d in part))

closing(['Opera viva sotto la linea di galleggiamento, opera morta sopra: le murate sono i fianchi',
         'Dalla prua: mascone a 45°, traverso a 90°, giardinetto a 135°, a dritta e a sinistra',
         'Manovre fisse (stralli, sartie, paterazzo) tengono l\'albero; le correnti (drizze, scotte, vang) manovrano le vele',
         'Ogni vela ha tre angoli, penna, mura e scotta, e tre lati, inferitura, base e balumina',
         'In barca si dice cima, galloccia, winch: il nome giusto rende la manovra più sicura'],
 'Per teoria e manovre della vela: lezioni 8 e 9','Appendice B · I nomi della barca a vela')

# ---- anteprima parziale ----
if os.environ.get('PARTIAL'):
    d=dict(LB.slides); write_deck(OUT,'Appendice B',[i for i in ORDER if i in d],{"s1":{"description":"x","start":"cover"}})

if not os.environ.get('PARTIAL'):
    write_deck(OUT,'Appendice B · I nomi della barca a vela',ORDER,
     {"s1":{"description":"Copertina e indice","start":"cover"},"s2":{"description":"Lo scafo: profilo, pianta e sezione, sotto coperta, direzioni","start":"scafo"},
      "s3":{"description":"La coperta e la ferramenta","start":"coperta"},"s4":{"description":"Alberatura e manovre fisse","start":"albero"},
      "s5":{"description":"Le vele: randa, genoa e vele di bordo","start":"randa"},"s6":{"description":"Le manovre correnti","start":"corr_randa"},
      "s7":{"description":"Armi, cime e nodi, parole delle manovre","start":"armi"},"s8":{"description":"Verifiche e glossario","start":"quiz1"}})
