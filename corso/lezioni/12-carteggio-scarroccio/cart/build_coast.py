"""Costruisce anelli chiusi di terra dalla linea di costa OSM tagliata su un rettangolo (terra a sinistra)."""
import json, sys
src, dst, lat0, lon0, lat1, lon1 = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:7])
ways=json.load(open(src))['elements']
starts={w['nodes'][0]:i for i,w in enumerate(ways)}; ends={w['nodes'][-1]:i for i,w in enumerate(ways)}
used=set(); chains=[]
def follow(i):
    ch=[(g['lon'],g['lat']) for g in ways[i]['geometry']]; used.add(i); first=ways[i]['nodes'][0]; last=ways[i]['nodes'][-1]
    while last!=first and last in starts and starts[last] not in used:
        j=starts[last]; used.add(j); ch+=[(g['lon'],g['lat']) for g in ways[j]['geometry']][1:]; last=ways[j]['nodes'][-1]
    return ch, last==first
for i,w in enumerate(ways):
    if w['nodes'][0] not in ends and i not in used: chains.append(follow(i))
for i in range(len(ways)):
    if i not in used: chains.append(follow(i))
X0,Y0,X1,Y1=lon0,lat0,lon1,lat1
def inside(p): return X0<=p[0]<=X1 and Y0<=p[1]<=Y1
def clip_seg(a,b):
    # Liang-Barsky
    t0,t1=0.0,1.0; dx=b[0]-a[0]; dy=b[1]-a[1]
    for p,q in ((-dx,a[0]-X0),(dx,X1-a[0]),(-dy,a[1]-Y0),(dy,Y1-a[1])):
        if p==0:
            if q<0: return None
        else:
            r=q/p
            if p<0: t0=max(t0,r)
            else: t1=min(t1,r)
    if t0>t1: return None
    return (a[0]+t0*dx,a[1]+t0*dy),(a[0]+t1*dx,a[1]+t1*dy),t0,t1
rings=[]; pieces=[]
for ch,closed in chains:
    if closed and all(inside(p) for p in ch): rings.append(ch); continue
    cur=None
    for a,b in zip(ch,ch[1:]):
        c=clip_seg(a,b)
        if c is None:
            if cur: pieces.append(cur); cur=None
            continue
        pa,pb,t0,t1=c
        if cur is None: cur=[pa]
        cur.append(pb)
        if t1<1: pieces.append(cur); cur=None
    if cur:
        if closed and pieces and pieces[-1] is not None: pass
        pieces.append(cur)
# unisci pezzi che non toccano il bordo (catene che finiscono dentro il rettangolo): scartali
def onb(p,e=1e-7): return abs(p[0]-X0)<e or abs(p[0]-X1)<e or abs(p[1]-Y0)<e or abs(p[1]-Y1)<e
pieces=[pc for pc in pieces if len(pc)>=2 and onb(pc[0]) and onb(pc[-1])]
W=X1-X0; H=Y1-Y0; P=2*(W+H)
def per(p):
    x,y=p
    if abs(y-Y0)<1e-7: return x-X0
    if abs(x-X1)<1e-7: return W+(y-Y0)
    if abs(y-Y1)<1e-7: return W+H+(X1-x)
    return 2*W+H+(Y1-y)
corners=[(0,(X0,Y0)),(W,(X1,Y0)),(W+H,(X1,Y1)),(2*W+H,(X0,Y1))]
left=set(range(len(pieces)))
while left:
    k=left.pop(); poly=list(pieces[k]); start=k
    while True:
        e=per(poly[-1])
        # prossimo ingresso in senso antiorario
        best=None
        for j in list(left)+[start]:
            s=per(pieces[j][0]); d=(s-e)%P
            if best is None or d<best[0]: best=(d,j)
        d,j=best
        # angoli attraversati
        for c,pt in sorted(corners,key=lambda c:(c[0]-e)%P):
            if 0<(c-e)%P<d: poly.append(pt)
        if j==start: break
        poly+=pieces[j]; left.discard(j)
    rings.append(poly)
out=[{'closed':True,'pts':[(y,x) for x,y in r]} for r in rings if len(r)>=3]
json.dump(out,open(dst,'w'))
print(len(out),'anelli;',len(pieces),'pezzi al bordo')
