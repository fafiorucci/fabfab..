"""Motore di disegno delle cime: curve 3D (x, y, z) proiettate sul piano, con sopra/sotto corretti agli incroci.
z positivo = verso chi guarda. Ogni cima è una spline di Catmull-Rom; i tratti che si sovrappongono a qualcosa
(un'altra cima, un oggetto) diventano pezzi disegnati in ordine di profondità."""
import math
NAVY='#16324F'
_uid=[0]
def uid(p='k'):
    _uid[0]+=1; return f'{p}{_uid[0]}'

def _sub(a,b): return tuple(x-y for x,y in zip(a,b))
def _add(a,b): return tuple(x+y for x,y in zip(a,b))
def _mul(a,k): return tuple(x*k for x in a)
def _lerp(a,b,t): return tuple(x+(y-x)*t for x,y in zip(a,b))

def catmull(P):
    n=len(P); segs=[]
    for i in range(n-1):
        p1,p2=P[i],P[i+1]
        p0=P[i-1] if i>0 else _sub(_mul(p1,2),p2)
        p3=P[i+2] if i+2<n else _sub(_mul(p2,2),p1)
        segs.append((p1,_add(p1,_mul(_sub(p2,p0),1/6)),_sub(p2,_mul(_sub(p3,p1),1/6)),p2))
    return segs

def bez(s,t):
    a=_lerp(s[0],s[1],t); b=_lerp(s[1],s[2],t); c=_lerp(s[2],s[3],t)
    d=_lerp(a,b,t); e=_lerp(b,c,t); return _lerp(d,e,t)

def split(s,t0,t1):
    """Sotto-curva di Bézier tra t0 e t1."""
    def left(s,t):
        a=_lerp(s[0],s[1],t); b=_lerp(s[1],s[2],t); c=_lerp(s[2],s[3],t); d=_lerp(a,b,t); e=_lerp(b,c,t); f=_lerp(d,e,t)
        return (s[0],a,d,f)
    def right(s,t):
        a=_lerp(s[0],s[1],t); b=_lerp(s[1],s[2],t); c=_lerp(s[2],s[3],t); d=_lerp(a,b,t); e=_lerp(b,c,t); f=_lerp(d,e,t)
        return (f,e,c,s[3])
    if t1<1: s=left(s,t1); t0=t0/t1 if t1>0 else 0
    if t0>0: s=right(s,t0)
    return s

def f1(v): return f'{v:.0f}' if abs(v-round(v))<0.05 else f'{v:.1f}'

class Rope:
    def __init__(s, pts, color, w=16, cap0=True, cap1=True, segs=None, hl=True, style='rope'):
        s.segs=segs if segs is not None else catmull([tuple(p) if len(p)==3 else (p[0],p[1],0) for p in pts])
        s.color=color; s.w=w; s.cap0=cap0; s.cap1=cap1; s.hl=hl; s.style=style
    def upto(s,k,cap1=True): return Rope(None,s.color,s.w,s.cap0,cap1,s.segs[:k],s.hl)
    def part(s,a,b): return Rope(None,s.color,s.w,False,False,s.segs[a:b],s.hl)
    def samples(s,step=3.0):
        out=[]
        for i,sg in enumerate(s.segs):
            L=sum(math.dist(sg[k][:2],sg[k+1][:2]) for k in range(3))
            m=max(4,int(L/step))
            for j in range(m): out.append((i,j/m))
        out.append((len(s.segs)-1,1.0))
        return out

class Obj:
    """Oggetto disegnato a una profondità; hit(x,y,m) dice se il punto (x,y) cade sull'oggetto (margine m)."""
    def __init__(s, svg, depth, hit): s.svg=svg; s.depth=depth; s.hit=hit

def render(ropes, objs=(), guides=(), extra_top=''):
    items=[]; order=[0]
    def add(d,svg): order[0]+=1; items.append((d,order[0],svg))
    for o in objs: add(o.depth,o.svg)
    # campioni
    data=[]
    for r in ropes:
        smp=r.samples(); pts=[bez(r.segs[i],t) for i,t in smp]
        arc=[0.0]
        for k in range(1,len(pts)): arc.append(arc[-1]+math.dist(pts[k][:2],pts[k-1][:2]))
        data.append((r,smp,pts,arc))
    for ri,(r,smp,pts,arc) in enumerate(data):
        inv=[False]*len(pts)
        for k,p in enumerate(pts):
            for o in objs:
                if o.hit(p[0],p[1],r.w/2+2): inv[k]=True; break
            if inv[k]: continue
            for rj,(r2,smp2,pts2,arc2) in enumerate(data):
                thr=(r.w+r2.w)/2+4
                for m,q in enumerate(pts2):
                    if rj==ri and abs(arc2[m]-arc[k])<2.2*max(r.w,14)+thr: continue
                    if abs(q[0]-p[0])<thr and abs(q[1]-p[1])<thr and math.dist(q[:2],p[:2])<thr:
                        inv[k]=True; break
                if inv[k]: break
        # zone coinvolte
        zones=[]; k=0; n=len(pts)
        while k<n:
            if inv[k]:
                j=k
                while j+1<n and inv[j+1]: j+=1
                zones.append([k,j]); k=j+1
            else: k+=1
        mz=[]
        for z in zones:
            if mz and z[0]-mz[-1][1]<=2: mz[-1][1]=z[1]
            else: mz.append(z)
        zones=mz
        # suddivide le zone dove la profondità cambia (cima che gira attorno a un oggetto)
        DZ=5.0; sub=[]
        for a,b in zones:
            st=a; band=round(pts[a][2]/DZ)
            for k in range(a+1,b+1):
                bb=round(pts[k][2]/DZ)
                if bb!=band and k-st>=3:
                    sub.append([st,k-1,True]); st=k; band=bb
                elif bb!=band: band=bb
            sub.append([st,b,False])
        zones=sub
        bounds=[0]
        for q in range(len(zones)-1):
            if zones[q][2]: bounds.append(zones[q][1]+1)
            else: bounds.append((zones[q][1]+zones[q+1][0])//2)
        bounds.append(n-1)
        if not zones: depths=[sum(p[2] for p in pts)/n]
        else: depths=[sum(pts[k][2] for k in range(z[0],z[1]+1))/(z[1]-z[0]+1) for z in zones]
        for q in range(len(bounds)-1):
            a,b=bounds[q],bounds[q+1]
            if b<=a: continue
            d=path_between(r,smp[a],smp[b])
            pid=uid()
            if r.style=='guide':
                add(depths[q],f'<path id="{pid}" d="{d}" fill="none" stroke-linecap="round"/><use href="#{pid}" stroke="#FFFFFF" stroke-opacity="0.9" stroke-width="{r.w+7}"/><use href="#{pid}" stroke="{r.color}" stroke-width="{r.w}" stroke-dasharray="10 8"/>')
                continue
            lc='round'
            if (q==0 and not r.cap0) or (q==len(bounds)-2 and not r.cap1): lc='butt'
            svg=(f'<path id="{pid}" d="{d}" fill="none" stroke-linejoin="round"/>'
                 f'<use href="#{pid}" stroke="{NAVY}" stroke-width="{r.w+6}"/><use href="#{pid}" stroke="{r.color}" stroke-width="{r.w}" stroke-linecap="{lc}"/>'
                 +(f'<use href="#{pid}" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="{r.w*0.26:.1f}"/>' if r.hl else ''))
            cap=''
            if q==0 and r.cap0: cap+=_cap(pts[0],r)
            if q==len(bounds)-2 and r.cap1: cap+=_cap(pts[-1],r)
            add(depths[q],cap+svg)
    items.sort(key=lambda x:(x[0],x[1]))
    body=''.join(x[2] for x in items)
    for g in guides: body+=g
    for r in ropes:
        if r.style=='guide': body+=_head(r)
    return body+extra_top

def _head(r,head=17):
    e=r.segs[-1]; p=e[3]; q=bez(e,0.8)
    ang=math.atan2(p[1]-q[1],p[0]-q[0])
    hx,hy=p[0]+head*0.6*math.cos(ang),p[1]+head*0.6*math.sin(ang)
    bx,by=hx-head*math.cos(ang),hy-head*math.sin(ang)
    l=(bx+head*0.58*math.sin(ang),by-head*0.58*math.cos(ang)); rr=(bx-head*0.58*math.sin(ang),by+head*0.58*math.cos(ang))
    return f'<polygon points="{f1(hx)},{f1(hy)} {f1(l[0])},{f1(l[1])} {f1(rr[0])},{f1(rr[1])}" fill="{r.color}" stroke="#FFFFFF" stroke-width="2.5" stroke-linejoin="round"/>'

def gd(r,a,b,gap=22,c=NAVY):
    """Guida tratteggiata sul percorso futuro della cima r (segmenti a..b), staccata dal capo di gap px."""
    segs=list(r.segs[a:b])
    s0=segs[0]; L=sum(math.dist(s0[k][:2],s0[k+1][:2]) for k in range(3)); t0=min(0.6,gap/max(L,1))
    segs[0]=split(s0,t0,1.0)
    e=segs[-1]; L=sum(math.dist(e[k][:2],e[k+1][:2]) for k in range(3)); t1=max(0.4,1-10/max(L,1))
    segs[-1]=split(e,0.0,t1) if len(segs)>1 else split(segs[0],0.0,t1)
    return Rope(None,c,4,False,False,segs,False,'guide')

def _cap(p,r): return f'<circle cx="{f1(p[0])}" cy="{f1(p[1])}" r="{(r.w+6)/2}" fill="{NAVY}"/><circle cx="{f1(p[0])}" cy="{f1(p[1])}" r="{r.w/2}" fill="{r.color}"/>'

def path_between(r,sa,sb):
    (ia,ta),(ib,tb)=sa,sb
    parts=[]
    for i in range(ia,ib+1):
        t0=ta if i==ia else 0.0; t1=tb if i==ib else 1.0
        if t1-t0<1e-4: continue
        parts.append(split(r.segs[i],t0,t1))
    if not parts: parts=[split(r.segs[ia],ta,min(1,ta+0.01))]
    d=f'M{f1(parts[0][0][0])} {f1(parts[0][0][1])}'
    for s in parts: d+=f'C{f1(s[1][0])} {f1(s[1][1])} {f1(s[2][0])} {f1(s[2][1])} {f1(s[3][0])} {f1(s[3][1])}'
    return d

def guide(r,a,b,c=NAVY,w=4,head=16):
    """Freccia tratteggiata lungo il percorso futuro della cima (segmenti a..b)."""
    segs=r.segs[a:b]
    if not segs: return ''
    d=f'M{f1(segs[0][0][0])} {f1(segs[0][0][1])}'+''.join(f'C{f1(s[1][0])} {f1(s[1][1])} {f1(s[2][0])} {f1(s[2][1])} {f1(s[3][0])} {f1(s[3][1])}' for s in segs)
    e=segs[-1]; p=e[3]; q=bez(e,0.9)
    ang=math.atan2(p[1]-q[1],p[0]-q[0])
    hx,hy=p[0],p[1]
    bx,by=hx-head*math.cos(ang),hy-head*math.sin(ang)
    l=(bx+head*0.55*math.sin(ang),by-head*0.55*math.cos(ang)); rr=(bx-head*0.55*math.sin(ang),by+head*0.55*math.cos(ang))
    tri=f'{f1(hx)},{f1(hy)} {f1(l[0])},{f1(l[1])} {f1(rr[0])},{f1(rr[1])}'
    return (f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{w+6}" stroke-linecap="round" stroke-opacity="0.85"/>'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="10 8" stroke-linecap="round"/>'
            f'<polygon points="{tri}" fill="{c}" stroke="#FFFFFF" stroke-width="2"/>')

def pull(x,y,ang,c=NAVY,L=46,w=5):
    """Freccia piena di trazione nella direzione ang (gradi, 0 = destra)."""
    a=math.radians(ang); x2,y2=x+L*math.cos(a),y+L*math.sin(a); h=16
    bx,by=x2-h*math.cos(a),y2-h*math.sin(a)
    l=(bx+h*0.6*math.sin(a),by-h*0.6*math.cos(a)); r=(bx-h*0.6*math.sin(a),by+h*0.6*math.cos(a))
    return (f'<line x1="{f1(x)}" y1="{f1(y)}" x2="{f1(bx)}" y2="{f1(by)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{f1(x2)},{f1(y2)} {f1(l[0])},{f1(l[1])} {f1(r[0])},{f1(r[1])}" fill="{c}"/>')

def xf(pts, fn): return [fn(p) for p in pts]
def rot90(cx,cy):
    """Ruota di 90° (l'alto diventa destra): (x,y) -> (cx+(cy-y)... )"""
    return lambda p: (cx+(cy-p[1]), cy+(p[0]-cx), p[2])
def shift(dx,dy): return lambda p: (p[0]+dx,p[1]+dy,p[2])
def scale(cx,cy,k): return lambda p: (cx+(p[0]-cx)*k, cy+(p[1]-cy)*k, p[2])
def obl(kx,ky):
    """Proiezione obliqua: ciò che sta davanti (z>0) si sposta di (kx*z, ky*z)."""
    return lambda p: (p[0]+kx*p[2], p[1]+ky*p[2], p[2])
