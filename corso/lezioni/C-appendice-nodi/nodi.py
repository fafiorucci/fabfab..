"""I nodi marinari, passo per passo: ogni funzione restituisce 4 pannelli (svg, didascalia)."""
import math
from corde import *
PW,PH=536,226
QW,QH=258,524   # pannelli verticali (4 in fila)
CORAL='#E4572E'; SEA='#0B8A99'; SUN='#F4A300'; GREEN='#2E9E5B'; BLUE='#2F6FDB'; PURPLE='#7B5CD6'; INK='#1B2A41'
ROPE='#F2B134'; ROPE2='#3E8FD6'; ROPE3='#E4572E'
GREY='#97A6B4'; STEEL='#B9C6D2'; WOOD='#B98A55'

# ---------------- NODO SAVOIA ----------------
def savoia_pts():
    return [(600,112,0),(470,112,0),(412,112,1),(360,112,0),(298,113,-1),(268,114,0),(240,112,1),(205,104,0),
            (172,76,0),(178,36,0),(226,18,0),(278,28,0),(294,48,-1),(304,80,0),
            (298,113,1),(292,158,0),(322,190,0),(372,188,0),(404,150,0),(412,112,-1),(414,70,0),(392,34,0),(345,22,0),
            (297,50,1),(256,80,0),(240,112,-1),(232,150,0),(226,192,0)]
def savoia():
    R=Rope(savoia_pts(),ROPE,cap0=False)
    p1=render([R.upto(15),gd(R,15,20)])
    p2=render([R.upto(20),gd(R,20,27)])
    p3=render([R])+pull(470,86,0,NAVY,40)+pull(206,206,112,NAVY,20)
    # stretto, dietro un passacavo
    k=0.62; c=(290,105)
    P=[scale(*c,k)(p) for p in savoia_pts()[1:]]
    P=[(p[0]+40,p[1]+8,p[2]) for p in P]
    P=[(640,113,0),(560,113,0)]+P
    Rt=Rope(P,ROPE,cap0=False)
    fair=f'<rect x="452" y="84" width="34" height="58" rx="10" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/>'
    hole=Obj(fair,2,lambda x,y,m: 452-m<x<486+m and 84-m<y<142+m)
    base=f'<rect x="440" y="140" width="60" height="16" rx="4" fill="{GREY}" stroke="{NAVY}" stroke-width="3"/>'
    p4=render([Rt],[hole])+base+pull(560,113,0,SEA)
    return {'layout':'land','panels':[(p1,'Fai una volta: il corrente passa sopra il dormiente'),
            (p2,'Porta il corrente dietro al dormiente'),
            (p3,'Infila il corrente nella volta, dal davanti'),
            (p4,'Stringi: l\'otto non passa dal passacavo')]}

KNOTS={'savoia':savoia}

# ---------------- GASSA D'AMANTE ----------------
def gassa_design(r=52, legs=22, collar=94, wp_up=22, eye_w=(36,150), eye_bot=368, tail_end=310):
    """Disegno verticale (il dormiente scende dall'alto); poi si ruota di 90°."""
    cx,cy=110,172+r
    X=(110,172)
    def rim(th): return (cx-r*math.sin(math.radians(th)), cy-r*math.cos(math.radians(th)))
    xl,xr=110-legs,110+legs
    th_l=math.degrees(math.asin(legs/r)); th_r=360-th_l
    S=[(110,-190,0),(110,-60,0),(110,30,0),(110,collar,1),(110,collar+44,0),(X[0],X[1],-1)]
    ring=[]
    for th,z in [(th_l,-1),(60,0),(90,0),(120,0),(180-th_l,1),(180+th_l,1),(240,0),(270,0),(300,0),(th_r,-1)]:
        p=rim(th); ring.append((p[0],p[1],z))
    # la parte che va all'occhio
    wp=[(X[0],X[1],1),(xl,X[1]-wp_up,-1),(xl-26,X[1]-wp_up-2,0),(eye_w[0]+6,X[1]+2,0),(eye_w[0],X[1]+45,0),(eye_w[0],X[1]+100,0),
        (eye_w[0]+8,eye_bot-48,0),(eye_w[0]+34,eye_bot-12,0),(95,eye_bot,0)]
    yb=rim(180+th_l)[1]
    up=[(eye_w[1]-10,eye_bot-18,0),(eye_w[1]-4,(eye_bot+yb)/2+6,0),(xr+4,yb+26,0),(xr,yb,-1),(xr,cy,0),(xr,rim(th_r)[1],1),(xr+2,collar+40,0),(xr-6,collar+10,0),(110,collar,-1),
        (xl+6,collar+10,0),(xl,collar+34,0),(xl,X[1]-wp_up,1),(xl,rim(th_l)[1],1),(xl,cy,0),(xl,yb,-1),(xl-2,tail_end,0)]
    return S+ring+wp+up
def gassa():
    T=shift(18,98)
    P=[T(p) for p in gassa_design()]
    R=Rope(P,ROPE,w=14,cap0=False)
    n=len(P)-1
    a=6+10+9+2
    p1=render([R.upto(a),gd(R,a,a+3)])
    p2=render([R.upto(a+7),gd(R,a+7,n)])
    p3=render([R])+pull(160,110,-90,NAVY,40)+pull(113,470,90,NAVY,36)
    Pt=[T(p) for p in gassa_design(r=36,legs=15,collar=128,wp_up=16,eye_w=(50,150),eye_bot=368,tail_end=276)]
    Rt=Rope(Pt,ROPE,w=14,cap0=False)
    p4=render([Rt])+pull(160,110,-90,SEA,40)+pull(118,470,90,SEA,36)
    return {'layout':'port','panels':[(p1,'Fai una volta sul dormiente, con il corrente sopra'),
            (p2,'Il corrente sale nella volta e gira dietro al dormiente'),
            (p3,'Ridiscende nella volta, accanto a sé stesso'),
            (p4,'Tira il dormiente: l\'occhio non scorre')]}
KNOTS['gassa']=gassa

# ---------------- strumenti comuni ----------------
def bar_w(x,ph,r,yb): a=math.radians(ph); return (x, yb+r*math.sin(a), r*math.cos(a))
def post_w(y,th,r,xc): a=math.radians(th); return (xc+r*math.sin(a), y, r*math.cos(a))
def tube_h(y,R=12,x0=-20,x1=560,fill=None):
    """Tubo orizzontale (draglia, pulpito) come oggetto a profondità 0."""
    fill=fill or STEEL
    svg=(f'<rect x="{x0}" y="{y-R}" width="{x1-x0}" height="{2*R}" rx="{R}" fill="{fill}" stroke="{NAVY}" stroke-width="4"/>'
         f'<line x1="{x0+10}" y1="{y-R*0.35:.1f}" x2="{x1-10}" y2="{y-R*0.35:.1f}" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="{max(2,R*0.3):.1f}" stroke-linecap="round"/>')
    return Obj(svg,0,lambda px,py,m: x0<px<x1 and abs(py-y)<R+m)
def post_v(x,R=16,y0=-20,y1=260,fill=None,top=None):
    fill=fill or WOOD
    cap=f'<ellipse cx="{x}" cy="{top}" rx="{R}" ry="{R*0.35:.1f}" fill="#D6B383" stroke="{NAVY}" stroke-width="4"/>' if top is not None else ''
    yt=top if top is not None else y0
    svg=(f'<rect x="{x-R}" y="{yt}" width="{2*R}" height="{y1-yt}" fill="{fill}" stroke="{NAVY}" stroke-width="4"/>'+cap+
         f'<line x1="{x-R*0.45:.1f}" y1="{yt+8}" x2="{x-R*0.45:.1f}" y2="{y1}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="{R*0.3:.1f}"/>')
    return Obj(svg,0,lambda px,py,m: abs(px-x)<R+m and yt-m<py<y1)
def fender(x,y,w=46,h=100,c=BLUE):
    return (f'<rect x="{x-w/2}" y="{y}" width="{w}" height="{h}" rx="{w/2}" fill="{c}" stroke="{NAVY}" stroke-width="4"/>'
            f'<rect x="{x-w/2+8}" y="{y+14}" width="{w*0.22:.0f}" height="{h-28}" rx="4" fill="#FFFFFF" fill-opacity="0.45"/>'
            f'<rect x="{x-9}" y="{y-8}" width="18" height="12" rx="4" fill="{NAVY}"/>')

# ---------------- NODO PARLATO ----------------
def clove(W,xs,r,k=1.0):
    """Parlato attorno a un asse orizzontale: W(x,ph,raggio). Restituisce giro A, diagonale, giro B, capo infilato."""
    A=[W(xs,40,r),W(xs-2*k,0,r),W(xs-8*k,-45,r),W(xs-14*k,-90,r),W(xs-20*k,-135,r),W(xs-26*k,-180,r),W(xs-32*k,-225,r),W(xs-38*k,-270,r),W(xs-44*k,-315,r)]
    D=[W(xs-30*k,22,r+6),W(xs-2*k,0,r+12),W(xs+22*k,-25,r+12),W(xs+42*k,-50,r+11),W(xs+58*k,-72,r+6),W(xs+70*k,-90,r)]
    B=[W(xs+74*k,-135,r),W(xs+77*k,-180,r),W(xs+80*k,-225,r),W(xs+82*k,-270,r),W(xs+84*k,-315,r)]
    T=[W(xs+78*k,15,r),W(xs+68*k,-25,r),W(xs+58*k,-55,r),W(xs+52*k,-84,r)]
    return A,D,B,T
def parlato_pts(xs=262,yb=100,r=20,k=1.0,S_len=250,tail_top=8):
    W=lambda x,ph,rr: bar_w(x,ph,rr,yb)
    S=[(xs,S_len,4),(xs,yb+90,6),(xs,yb+46,10)]
    A,D,B,T=clove(W,xs,r,k)
    T=T+[(xs+52*k,yb-r-26,6),(xs+54*k,max(tail_top+30,yb-r-60),3),(xs+56*k,tail_top,2)]
    return S+A+D+B+T, len(S)+len(A)-1, len(S)+len(A)+len(D)+len(B)-1
def parlato():
    P,a,b=parlato_pts(xs=236,yb=110,r=28,k=1.5)
    P=[obl(0.55,0.12)(p) for p in P]
    R=Rope(P,ROPE,w=16,cap0=False)
    bar=tube_h(110,R=10)
    p1=render([R.upto(a),gd(R,a,a+6)],[bar])
    p2=render([R.upto(b),gd(R,b,len(P)-1)],[bar])
    p3=render([R],[bar])+pull(206,196,90,NAVY,26)+pull(360,34,-90,NAVY,26)
    P4,_,_=parlato_pts(xs=300,yb=52,r=18,k=1.0,S_len=150,tail_top=4)
    P4=[obl(0.5,0.1)(p) for p in P4]
    R4=Rope(P4,ROPE,w=14,cap0=False)
    rail=tube_h(52,R=8)
    st=f'<rect x="92" y="36" width="16" height="200" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/>'
    p4=st+render([R4],[rail])+fender(300,146,50,90,BLUE)
    return {'layout':'land','panels':[(p1,'Passa il corrente attorno alla draglia, da davanti'),
            (p2,'Sali in diagonale sopra il dormiente e fai un secondo giro'),
            (p3,'Infila il corrente sotto la diagonale: i capi escono opposti'),
            (p4,'Tira i due capi: il parabordo resta appeso')]}
KNOTS['parlato']=parlato

# ---------------- VOLTA TONDA E DUE MEZZI COLLI ----------------
def mezzi_pts(xc=96,ys=104,rp=25.5,rs=18,xs=318):
    S=[(620,ys,0),(470,ys,0),(xs+120,ys,0),(xc+rp+60,ys+1,0)]
    turn=[post_w(ys+2+(th-90)/360*17,th,rp,xc) for th in range(90,811,45)]
    ex=[(xc+rp+26,ys+40,1),(xc+rp+110,ys+50,2),(xs-20,ys+48,3)]
    W=lambda x,ph,rr: bar_w(x,ph,rr,ys)
    A,D,B,T=clove(W,xs,rs,1.0)
    T=T+[(xs+52,ys-rs-24,5),(xs+62,ys-66,2),(xs+80,ys-84,0)]
    n0=len(S)+len(turn); n1=n0+len(ex)+len(A)+len(D)
    return S+turn+ex+A+D+B+T, n0-1, n1-1
def mezzi():
    P,a,b=mezzi_pts()
    P=[obl(0.4,0.4)(p) for p in P]
    R=Rope(P,ROPE,w=16,cap0=False)
    post=post_v(96,R=16,top=14,y1=260)
    p1=render([R.upto(a),gd(R,a,a+4)],[post])
    p2=render([R.upto(b),gd(R,b,len(P)-1)],[post])
    p3=render([R],[post])
    water=f'<rect x="0" y="190" width="{PW}" height="40" fill="#12A4B5" fill-opacity="0.25"/><line x1="0" y1="190" x2="{PW}" y2="190" stroke="{SEA}" stroke-width="3"/>'
    p4=water+render([R],[post])+pull(468,76,0,SEA,44)
    return {'layout':'land','panels':[(p1,'Due giri attorno al palo: la volta tonda'),
            (p2,'Primo mezzo collo attorno al dormiente'),
            (p3,'Secondo mezzo collo, girato nello stesso verso'),
            (p4,'Tiene sotto tiro e si scioglie senza fatica')]}
KNOTS['mezzi']=mezzi
KNOTS['mezzi']=mezzi

# ---------------- NODO PIANO ----------------
def piano():
    Y=[(40,250,0),(140,222,0),(232,194,0),(268,178,1),(304,160,0),(268,142,-1),(232,124,0),(222,110,0),
       (232,96,0),(268,80,-1),(304,62,0),(268,44,1),(232,26,0),(222,4,0),(220,-20,0)]
    Bl=[(496,250,0),(396,222,0),(304,194,0),(268,178,-1),(232,160,0),(268,142,1),(304,124,0),(314,110,0),
        (304,96,0),(268,80,1),(232,62,0),(268,44,-1),(304,26,0),(314,4,0),(316,-20,0)]
    Ry=Rope(Y,ROPE,w=15,cap0=False,cap1=False); Rb=Rope(Bl,ROPE2,w=15,cap0=False,cap1=False)
    p1=render([Ry.upto(7,True),Rb.upto(7,True),gd(Rb,7,11)])
    p2=render([Ry,Rb])
    def bights(k=1.0):
        Yb=[(-30,206,0),(60,194,0),(150,166,0),(226,138,0),(268,128,-1),(320,126,0),(356,118,0),(366,102,0),(356,86,0),(320,78,0),(268,76,1),(226,66,0),(150,40,0),(60,16,0),(-30,4,0)]
        Bb=[(566,206,0),(476,194,0),(386,166,0),(310,138,0),(268,128,1),(216,126,0),(180,118,0),(170,102,0),(180,86,0),(216,78,0),(268,76,-1),(310,66,0),(386,40,0),(476,16,0),(566,4,0)]
        T=lambda p: (268+(p[0]-268)*k if abs(p[0]-268)<110 else p[0]+(-1 if p[0]<268 else 1)*110*(k-1), p[1], p[2])
        return [T(p) for p in Yb],[T(p) for p in Bb]
    Yb,Bb=bights()
    p3=render([Rope(Yb,ROPE,w=15,cap0=False,cap1=False),Rope(Bb,ROPE2,w=15,cap0=False,cap1=False)])
    Yt,Bt=bights(0.55)
    Yt=[(p[0],102+(p[1]-102)*0.8,p[2]) for p in Yt]; Bt=[(p[0],102+(p[1]-102)*0.8,p[2]) for p in Bt]
    p4=render([Rope(Yt,ROPE,w=15,cap0=False,cap1=False),Rope(Bt,ROPE2,w=15,cap0=False,cap1=False)])+pull(96,214,180,SEA,40)+pull(440,214,0,SEA,40)
    return {'layout':'land','panels':[(p1,'Sinistra sopra destra, e sotto: primo mezzo nodo'),
            (p2,'Destra sopra sinistra, e sotto: secondo mezzo nodo'),
            (p3,'Tira: i due doppini si abbracciano'),
            (p4,'Stretto: ogni capo esce accanto al suo dormiente')]}
KNOTS['piano']=piano

# ---------------- NODO BANDIERA ----------------
def bandiera_ropes(tight=False):
    D=gassa_design(r=34,legs=15,collar=128,wp_up=16,eye_w=(50,150),eye_bot=368,tail_end=276) if tight else gassa_design()
    D=[(p[0]+18,p[1]+64,-p[2]) for p in D]      # specchio: la sottile entra da dietro e passa sotto sé stessa
    y=D[:6+10+6]
    up=D[6+10+9:]
    b=[(up[2][0]+10,up[2][1]+320,0),(up[2][0]+8,up[2][1]+150,0),(up[2][0]+6,up[2][1]+70,0)]+up[2:]
    return y,b
def bandiera():
    y,b=bandiera_ropes()
    Ry=Rope(y,ROPE3,w=11,cap0=False); Rb=Rope(b,ROPE2,w=20,cap0=False)
    p1=render([Ry.upto(2),Rb,gd(Ry,2,5)])
    p2=render([Ry.upto(16),Rb,gd(Ry,16,len(y)-1)])
    p3=render([Ry,Rb])
    yt,bt=bandiera_ropes(True)
    p4=render([Rope(yt,ROPE3,w=11,cap0=False),Rope(bt,ROPE2,w=20,cap0=False)])+pull(150,90,-90,SEA,36)+pull(186,470,90,SEA,34)
    return {'layout':'port','panels':[(p1,'Doppino nella grossa: la sottile passa sotto'),
            (p2,'La sottile gira attorno ai due rami del doppino'),
            (p3,'Infila il capo sotto sé stessa'),
            (p4,'Stringi: tiene anche tra cime diverse')]}
KNOTS['bandiera']=bandiera

# ---------------- NODO MARGHERITA ----------------
def margherita_pts(left=True,right=True,zr=26,yr=36):
    A=[(-30,62,0),(40,62,0),(100,64,0)]
    if left:
        cx,cy=158,137
        band=[(cx-4+8*(ph+60)/360, cy+yr*math.sin(math.radians(ph)), zr*math.cos(math.radians(ph))) for ph in range(-60,301,30)]
        A+=[(128,78,0)]+band+[(186,84,0),(220,64,0)]
    else: A+=[(170,62,0),(230,62,0)]
    A+=[(320,62,0),(410,62,0),(452,70,0),(470,87,0),(454,108,0),(410,112,0),(320,112,0),(230,112,0),(140,112,0),
        (96,116,0),(78,137,0),(96,158,0),(140,162,0),(230,162,0),(300,162,0)]
    if right:
        cx,cy=378,87
        band=[(cx-4+8*(60-ph)/360, cy+yr*math.sin(math.radians(ph)), zr*math.cos(math.radians(ph))) for ph in range(60,-301,-30)]
        A+=[(338,150,0)]+band+[(410,146,0),(446,162,0)]
    else: A+=[(380,162,0),(440,162,0)]
    A+=[(500,162,0),(580,162,0)]
    return [obl(0.5,0.1)(p) for p in A]
def margherita():
    p1=render([Rope(margherita_pts(False,False),ROPE,w=15,cap0=False,cap1=False)])
    p2=render([Rope(margherita_pts(True,False),ROPE,w=15,cap0=False,cap1=False)])
    p3=render([Rope(margherita_pts(True,True),ROPE,w=15,cap0=False,cap1=False)])
    p4=p3+pull(96,36,180,SEA,40)+pull(440,196,0,SEA,40)
    return {'layout':'land','panels':[(p1,'Piega la cima a Z: tre rami affiancati'),
            (p2,'Un giro del ramo di sopra stringe il doppino di sinistra'),
            (p3,'Lo stesso dall\'altra parte, con il ramo di sotto'),
            (p4,'La cima è più corta: tiene finché resta in tiro')]}
KNOTS['margherita']=margherita
KNOTS['piano']=piano

# ---------------- GALLOCCIA (vista dall'alto) ----------------
def cleat_obj(cx=268,cy=110,L=118,h=11):
    horns=(f'<rect x="{cx-L}" y="{cy-h}" width="{2*L}" height="{2*h}" rx="{h}" fill="#C9D3DD" stroke="{NAVY}" stroke-width="4"/>'
           f'<line x1="{cx-L+12}" y1="{cy-4}" x2="{cx+L-12}" y2="{cy-4}" stroke="#FFFFFF" stroke-opacity="0.7" stroke-width="4" stroke-linecap="round"/>')
    base=f'<rect x="{cx-60}" y="{cy-21}" width="120" height="42" rx="12" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/>'
    return [Obj(base,3,lambda x,y,m: cx-60-m<x<cx+60+m and cy-21-m<y<cy+21+m),
            Obj(horns,15,lambda x,y,m: cx-L-m<x<cx+L+m and cy-h-m<y<cy+h+m)]
def galloccia_pts():
    P=[(-30,206,1),(70,184,1),(160,160,2),(250,148,3),(306,142,4),(334,130,5),
       (340,110,5),(334,90,5),(300,80,4),(268,76,3),(236,80,4),(204,90,5),
       (198,110,5),(206,132,6),
       (232,134,12),(252,124,26),(268,110,28),(288,96,26),(330,80,14),(352,88,6),
       (358,110,5),(352,134,6),
       (322,138,14),(292,126,32),(268,110,34),(244,94,32),(206,80,14),(184,88,6),
       (178,110,5),(186,134,6),(214,140,16),(236,128,30),(256,114,31),(276,98,30),(300,86,26),(326,78,20)]
    return P
def galloccia():
    P=[scale(268,110,1.3)(p) for p in galloccia_pts()]; objs=cleat_obj(L=154,h=14)
    R=Rope(P,ROPE,w=17,cap0=False)
    deck=f'<rect x="0" y="0" width="{PW}" height="{PH}" fill="#EFE3CF"/>'+''.join(f'<line x1="0" y1="{y}" x2="{PW}" y2="{y}" stroke="#D9C7A8" stroke-width="3"/>' for y in range(18,226,34))
    p1=deck+render([R.upto(13),gd(R,13,19)],objs)
    p2=deck+render([R.upto(21),gd(R,21,27)],objs)
    p3=deck+render([R.upto(27),gd(R,27,len(P)-1)],objs)
    p4=deck+render([R],objs)+pull(90,212,196,SEA,40)
    return {'layout':'land','panels':[(p1,'Dal corno lontano: un giro completo attorno alla base'),
            (p2,'Sali in diagonale sopra i corni e passa sotto il corno'),
            (p3,'Torna in diagonale: sopra la galloccia si forma una X'),
            (p4,'Chiudi con una volta mezza: il capo passa sotto')]}
KNOTS['galloccia']=galloccia

# ---------------- BITTA ----------------
def bitt_obj(cx,cy,R=22):
    svg=(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{R-8}" fill="#C9D3DD" stroke="{NAVY}" stroke-width="3"/>'
         f'<circle cx="{cx-4}" cy="{cy-4}" r="{R*0.25:.0f}" fill="#FFFFFF" fill-opacity="0.6"/>')
    return Obj(svg,40,lambda x,y,m: math.dist((x,y),(cx,cy))<R+m*0.3)
def around(cx,cy,R,a0,a1,z0,z1,step=30):
    n=max(2,int(abs(a1-a0)/step)); out=[]
    for i in range(n+1):
        a=math.radians(a0+(a1-a0)*i/n); z=z0+(z1-z0)*i/n
        out.append((cx+R*math.cos(a), cy+R*math.sin(a), z))
    return out
def bitta_pts(eights=2):
    c1=(176,112); c2=(360,112)
    P=[(-30,214,2),(60,196,3),(120,168,4)]
    P+=around(*c1,34,140,-160,4,8)            # volta tonda (un giro e mezzo)
    P+=around(*c1,34,-160,-300,8,10)[1:]
    segs=[len(P)-1]
    z=12
    for k in range(eights):
        P+=[(268,112,z+4)]                     # attraversa al centro verso la seconda bitta
        P+=around(*c2,34+6*k,-150,150,z,z+2)
        P+=[(268,112,z+8)]
        P+=around(*c1,40+6*k,-30,-300+(0 if k<eights-1 else 60),z+2,z+4)
        segs.append(len(P)-1); z+=12
    P+=[(P[-1][0]+30,P[-1][1]+36,z),(P[-1][0]+44,P[-1][1]+70,z)]
    return P,segs
def bitta():
    objs=[bitt_obj(176,112),bitt_obj(360,112)]
    deck=f'<rect x="0" y="0" width="{PW}" height="{PH}" fill="#DCD6CC"/>'+''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{PH}" stroke="#C9C1B3" stroke-width="3"/>' for x in range(30,540,90))
    P,sg=bitta_pts()
    R=Rope(P,ROPE,w=15,cap0=False)
    p1=deck+render([R.upto(sg[0]),gd(R,sg[0],sg[0]+6)],objs)
    p2=deck+render([R.upto(sg[1]),gd(R,sg[1],sg[1]+6)],objs)
    p3=deck+render([R],objs)
    # doppino in banchina
    quay=f'<rect x="0" y="0" width="{PW}" height="150" fill="#DCD6CC"/><rect x="0" y="150" width="{PW}" height="76" fill="#12A4B5" fill-opacity="0.3"/><line x1="0" y1="150" x2="{PW}" y2="150" stroke="{NAVY}" stroke-width="4"/>'
    D=[(206,260,0),(214,170,1)]+around(268,72,34,180,360,2,2,20)+[(322,170,1),(330,260,0)]
    p4=quay+render([Rope(D,ROPE,w=15,cap0=False,cap1=False)],[bitt_obj(268,72,24)])
    return {'layout':'land','panels':[(p1,'Volta tonda sulla prima bitta'),
            (p2,'Poi giri a otto tra le due bitte'),
            (p3,'Un altro otto: tiene per attrito, si molla subito'),
            (p4,'In banchina, il doppino: si molla da bordo')]}
KNOTS['bitta']=bitta

# ---------------- NODO DI BOZZA ----------------
def bozza_pts(yb=112,r=21,x0=0):
    W=lambda x,ph,rr=r: bar_w(x+x0,ph,rr,yb)
    S=[(-40+x0,yb+30,8),(80+x0,yb+22,12),(180+x0,yb+18,12)]+[W(x,58) for x in (230,262)]
    T1=[W(268,20),W(266,-30),W(263,-90),W(260,-140),W(257,-190),W(254,-240),W(251,-275),W(248,-302,r+11)]
    T2=[W(246,20,r+4),W(244,-30),W(241,-90),W(238,-140),W(235,-190),W(232,-240),W(229,-275),W(226,-302,r+11)]
    D=[W(236,30,r+20),W(252,5,r+24),W(270,-24,r+24),W(288,-52,r+20),W(302,-76,r+8),W(310,-92)]
    T3=[W(313,-135),W(315,-180),W(317,-225),W(319,-270),W(321,-315)]
    TT=[W(314,15),W(305,-25),W(299,-57),W(296,-85),(297+x0,yb-r-26,6),(304+x0,yb-r-62,3),(314+x0,8,0)]
    n1=len(S)+len(T1)+len(T2)-1; n2=n1+len(D)+len(T3)
    return S+T1+T2+D+T3+TT, n1, n2
def bozza():
    P,a,b=bozza_pts()
    P=[obl(0.5,0.1)(scale(270,112,1.45)(p)) for p in P]
    R=Rope(P,ROPE,w=15,cap0=False)
    main=Rope([(-40,112,0),(200,112,0),(400,112,0),(600,112,0)],ROPE2,w=24,cap0=False,cap1=False)
    p1=render([main,R.upto(a),gd(R,a,a+6)])
    p2=render([main,R.upto(b),gd(R,b,len(P)-1)])
    p3=render([main,R])+pull(70,164,180,NAVY,40)
    P4,_,_=bozza_pts(x0=-50)
    P4=[obl(0.5,0.1)(scale(220,112,1.3)(p)) for p in P4]
    main4=Rope([(-40,112,0),(200,112,0),(400,112,0),(470,120,0),(480,150,0)],ROPE2,w=24,cap0=False,cap1=False)
    winch=(f'<circle cx="480" cy="170" r="44" fill="#C9D3DD" stroke="{NAVY}" stroke-width="4"/><circle cx="480" cy="170" r="24" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/>')
    p4=render([main4,Rope(P4,ROPE,w=15,cap0=False)])+winch+pull(60,164,180,SEA,40)
    return {'layout':'land','panels':[(p1,'Due giri sulla cima in tiro, sopra il proprio dormiente'),
            (p2,'Passa in diagonale sopra i giri e fai un giro dall\'altra parte'),
            (p3,'Chiudi come un parlato: il capo passa sotto la diagonale'),
            (p4,'Tira la bozza: il nodo morde e prende il carico')]}
KNOTS['bozza']=bozza

# ---------------- NODO D'ANCOROTTO ----------------
RING=(96,113,50)
def ancorotto_pts(rs=18):
    cx,cy,Rr=RING; xt=cx+Rr
    ys=113
    rp=lambda th: 15+15*max(0.0,math.cos(math.radians(th)))
    S=[(620,ys,0),(420,ys,0),(260,ys,0),(xt+44,ys,0)]
    turn=[post_w(ys-10+(th-90)/360*11,th,rp(th),xt) for th in range(90,811,45)]
    K=[(xt+30,ys+22,1),(xt+62,ys+18,-3),(xt+72,ys,-10),(xt+64,ys-24,-4),(xt+36,ys-34,4),(xt+14,ys-30,10)]
    U=[(xt+3,ys-18,16),(xt+2,ys-4,17),(xt+2,ys+10,17),(xt+4,ys+24,15),(xt+16,ys+40,8)]
    xs=256
    W=lambda x,ph,rr: bar_w(x,ph,rr,ys)
    H=[(xt+50,ys+46,4),(xs-18,ys+42,5)]+[W(xs,40,rs),W(xs+2,0,rs),W(xs+8,-45,rs),W(xs+14,-90,rs),W(xs+20,-135,rs),W(xs+26,-180,rs),W(xs+32,-225,rs),W(xs+38,-270,rs),W(xs+44,-315,rs)]
    H+=[W(xs+30,22,rs+6),W(xs+2,0,rs+12),W(xs-18,-30,rs+10),(xs-30,ys-rs-22,6),(xs-40,ys-60,2)]
    n1=len(S)+len(turn)-1; n2=n1+len(K)+len(U)
    return S+turn+K+U+H, n1, n2
def ancorotto():
    P,a,b=ancorotto_pts()
    P=[obl(0.4,0.4)(p) for p in P]
    R=Rope(P,ROPE,w=15,cap0=False)
    cx,cy,Rr=RING
    ring=Obj(f'<circle cx="{cx}" cy="{cy}" r="{Rr}" fill="none" stroke="{NAVY}" stroke-width="18"/><circle cx="{cx}" cy="{cy}" r="{Rr}" fill="none" stroke="{STEEL}" stroke-width="10"/>',0,
             lambda x,y,m: abs(math.dist((x,y),(cx,cy))-Rr)<9+m)
    shank=(f'<rect x="-10" y="{cy-15}" width="{cx-Rr+14}" height="30" rx="8" fill="{GREY}" stroke="{NAVY}" stroke-width="4"/>')
    p1=shank+render([R.upto(a),gd(R,a,a+6)],[ring])
    p2=shank+render([R.upto(b),gd(R,b,len(P)-1)],[ring])
    p3=shank+render([R],[ring])
    p4=p3+pull(470,84,0,SEA,44)
    return {'layout':'land','panels':[(p1,'Due giri nella cicala dell\'ancora'),
            (p2,'Il capo gira dietro al dormiente e passa sotto i due giri'),
            (p3,'Chiudi con un mezzo collo sul dormiente'),
            (p4,'Tiene sotto strappi e si scioglie a terra')]}
KNOTS['ancorotto']=ancorotto
