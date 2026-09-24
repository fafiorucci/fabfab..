"""Disegno della carta nautica schematica (costa OpenStreetMap) con il tracciamento di un esercizio."""
import math, json, os
from geo import *
NAVY='#16324F'; CORAL='#E4572E'; SEA='#0B8A99'; PURPLE='#7B5CD6'; GREEN='#2E9E5B'; SUN='#F4A300'; ORANGE='#F28C28'; GREY='#8A9BAD'; INK='#1B2A41'
SEA_BG='#E8F4F8'; LAND='#F3E6C4'; LAND_S='#B89A5E'; GRID='#B9CDD8'
RINGS=None
def rings():
    global RINGS
    if RINGS is None:
        RINGS=json.load(open(os.path.join(D,'coast_rings.json')))
        for r in RINGS:
            if not r['closed']:
                a=r['pts'][0]; b=r['pts'][-1]
                r['pts']=r['pts']+[(b[0],12.8),(43.4,12.8),(43.4,a[1])]
    return RINGS

def dp(pts,tol):
    if len(pts)<3: return pts
    keep=[False]*len(pts); keep[0]=keep[-1]=True; st=[(0,len(pts)-1)]
    while st:
        i,j=st.pop(); ax,ay=pts[i]; bx,by=pts[j]; dx,dy=bx-ax,by-ay; L=math.hypot(dx,dy) or 1e-9
        best=-1; bi=-1
        for k in range(i+1,j):
            d=abs((pts[k][0]-ax)*dy-(pts[k][1]-ay)*dx)/L
            if d>best: best=d; bi=k
        if best>tol: keep[bi]=True; st.append((i,bi)); st.append((bi,j))
    return [p for p,k in zip(pts,keep) if k]

class Chart:
    def __init__(s, S, W, H, pts_ll, pad=1.2, min_span=5):
        s.S=S; s.W=W; s.H=H; pl=S.pl
        xy=[pl.xy(*p) for p in pts_ll]
        x0=min(p[0] for p in xy)-pad; x1=max(p[0] for p in xy)+pad; y0=min(p[1] for p in xy)-pad; y1=max(p[1] for p in xy)+pad
        cx,cy=(x0+x1)/2,(y0+y1)/2; w=max(x1-x0,min_span); h=max(y1-y0,min_span*H/W)
        if w/h < W/H: w=h*W/H
        else: h=w*H/W
        s.x0=cx-w/2; s.y1=cy+h/2; s.sc=W/w; s.wm=w; s.hm=h
    def p(s,x,y): return ((x-s.x0)*s.sc, (s.y1-y)*s.sc)
    def pll(s,ll): return s.p(*s.S.pl.xy(*ll))
    def coast(s):
        out=[]; pl=s.S.pl; m=40
        for r in rings():
            pts=[s.p(*pl.xy(la,lo)) for la,lo in r['pts']]
            xs=[q[0] for q in pts]; ys=[q[1] for q in pts]
            if max(xs)<-m or min(xs)>s.W+m or max(ys)<-m or min(ys)>s.H+m: continue
            pts=[(min(max(x,-400),s.W+400),min(max(y,-400),s.H+400)) for x,y in pts]
            h_=len(pts)//2; q=dp(pts[:h_+1],1.1)[:-1]+dp(pts[h_:],1.1)
            if len(q)<3: continue
            out.append('M'+' L'.join(f'{x:.0f} {y:.0f}' for x,y in q)+' Z')
        return f'<path d="{" ".join(out)}" fill="{LAND}" stroke="{LAND_S}" stroke-width="2" stroke-linejoin="round"/>'
    def grid(s):
        pl=s.S.pl
        la0,lo0=pl.ll(s.x0,s.y1-s.hm); la1,lo1=pl.ll(s.x0+s.wm,s.y1)
        span=(la1-la0)*60; st=1 if span<9 else (2 if span<18 else 5)
        g=''; labs=[]
        m=math.ceil(la0*60/st)*st
        while m<=la1*60:
            y=s.pll((m/60,lo0))[1]; g+=f'<line x1="0" y1="{y:.1f}" x2="{s.W}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1.5"/>'
            labs.append(('lat',y,f"{int(m//60)}°{int(m%60):02d}′N")); m+=st
        m=math.ceil(lo0*60/st)*st
        while m<=lo1*60:
            x=s.pll((la0,m/60))[0]; g+=f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{s.H}" stroke="{GRID}" stroke-width="1.5"/>'
            labs.append(('lon',x,f"{int(m//60):03d}°{int(m%60):02d}′E")); m+=st
        return g,labs,st
    def scalebar(s):
        n=1 if s.sc>90 else (2 if s.sc>45 else 5)
        L=n*s.sc; x=s.W-L-30; y=s.H-30
        g=f'<rect x="{x-12:.0f}" y="{y-34:.0f}" width="{L+24:.0f}" height="52" rx="10" fill="#FFFFFF" fill-opacity="0.85"/>'
        g+=''.join(f'<rect x="{x+i*L/(2*n):.1f}" y="{y-6}" width="{L/(2*n):.1f}" height="10" fill="{NAVY if i%2==0 else "#FFFFFF"}" stroke="{NAVY}" stroke-width="1.5"/>' for i in range(2*n))
        return g,(x,y-36,L,f'{n} miglio' if n==1 else f'{n} miglia')

def arrowhead(x1,y1,x2,y2,c,hs=16):
    a=math.atan2(y2-y1,x2-x1); bx=x2-hs*math.cos(a); by=y2-hs*math.sin(a)
    return f'<polygon points="{x2:.1f},{y2:.1f} {bx+hs*0.45*math.sin(a):.1f},{by-hs*0.45*math.cos(a):.1f} {bx-hs*0.45*math.sin(a):.1f},{by+hs*0.45*math.cos(a):.1f}" fill="{c}"/>'
ST={'ril':(NAVY,3,'',False),'ril2':(CORAL,4,'',False),'trasp':(PURPLE,3.5,'14 9',False),'trasp_v':(GREY,2,'6 6',True),'rotta':(GREEN,5,'',True),
    'rotta2':(ORANGE,4,'12 8',True),'rotta_l':(GREY,2,'8 8',False),'vett':(ORANGE,4,'',True),'vett2':(GREEN,3,'8 6',True),'par':(PURPLE,2.5,'10 8',False)}
LABC={'ril':NAVY,'ril2':CORAL,'trasp':PURPLE,'rotta':GREEN,'rotta2':ORANGE,'vett':ORANGE,'vett2':GREEN,'lm':NAVY,'ship':'#34465E','fix':CORAL}

_CID=0
def render(S, W, H, solution=True, keep=None):
    """ritorna (corpo svg, etichette[(x,y,testo,colore,kind)]) — coordinate nel pannello"""
    geo_pts=[p for p,_,_ in S.pts]+[a for a,_,_,_ in S.lines]+[b for _,b,_,_ in S.lines]
    if not solution: geo_pts=[p for p,_,k in S.pts]+[a for a,_,_,_ in S.lines]+[b for _,b,_,_ in S.lines]
    C=Chart(S,W,H,geo_pts)
    global _CID; _CID+=1; cid=f'cc{_CID}'
    body=f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="{W}" height="{H}" rx="36"/></clipPath></defs><g clip-path="url(#{cid})"><rect x="0" y="0" width="{W}" height="{H}" fill="{SEA_BG}"/>'
    g,glabs,st=C.grid(); body+=g+C.coast()
    labels=[]
    if solution:
        for a,b,kind,lab in S.lines:
            c,w,dash,arr=ST[kind]; (x1,y1),(x2,y2)=C.pll(a),C.pll(b)
            da=f' stroke-dasharray="{dash}"' if dash else ''
            body+=f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{da} stroke-linecap="round"/>'
            if arr: body+=arrowhead(x1,y1,x2,y2,c,16 if w>=4 else 12)
            if lab: labels.append(((x1+x2)/2,(y1+y2)/2,lab,LABC.get(kind,NAVY),'line',(x1,y1,x2,y2)))
    for ll,lab,kind in S.pts:
        if kind=='none' or (not solution and kind=='fix'): continue
        x,y=C.pll(ll)
        if kind=='lm': body+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{NAVY}"/>'
        elif kind=='fix': body+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="none" stroke="{CORAL}" stroke-width="5"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{CORAL}"/>'
        elif solution or (lab.startswith(('A','B')) and '′' not in lab): body+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
        else: continue
        labels.append((x,y,lab,LABC[kind],kind,None))
    sb,sbl=C.scalebar(); body+=sb+'</g>'
    return body,labels,glabs,sbl,C

def place_labels(labels, W, H, size=22):
    """posiziona le etichette evitando sovrapposizioni; ritorna [(x,y,w,testo,colore,pill)]"""
    boxes=[]; out=[]
    def ok(b):
        if b[0]<6 or b[1]<6 or b[0]+b[2]>W-6 or b[1]+b[3]>H-6: return False
        return all(b[0]+b[2]<o[0] or o[0]+o[2]<b[0] or b[1]+b[3]<o[1] or o[1]+o[3]<b[1] for o in boxes)
    # prima i punti (fix, lm, ship) poi le linee
    order=sorted(labels,key=lambda l:{'fix':0,'lm':1,'ship':2,'line':3}[l[4]])
    for x,y,t,c,kind,seg in order:
        w=int(0.56*size*len(t))+24; h=size*1.3+6
        if kind=='line':
            x1,y1,x2,y2=seg; cands=[]
            for f in (0.5,0.35,0.65,0.25,0.75,0.15,0.85):
                px,py=x1+(x2-x1)*f,y1+(y2-y1)*f
                cands+= [(px-w/2,py-h-8),(px-w/2,py+8),(px+10,py-h/2),(px-w-10,py-h/2)]
        else:
            r=20 if kind=='fix' else 16
            cands=[(x+r,y-h-4),(x+r,y+4),(x-w-r,y-h-4),(x-w-r,y+4),(x-w/2,y-h-r),(x-w/2,y+r),(x+r,y-h/2),(x-w-r,y-h/2)]
        for cx,cy in cands:
            b=(cx,cy,w,h)
            if ok(b): boxes.append(b); out.append((cx,cy,w,t,c,kind)); break
        else:
            cx,cy=cands[0]; cx=min(max(cx,8),W-w-8); cy=min(max(cy,8),H-h-8); boxes.append((cx,cy,w,h)); out.append((cx,cy,w,t,c,kind))
    return out
