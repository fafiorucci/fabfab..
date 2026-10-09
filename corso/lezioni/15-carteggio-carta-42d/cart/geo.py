"""Geometria del carteggio: coordinate, rilevamenti, punti nave, costa della carta 5/D."""
import json, math, os
D=os.path.dirname(os.path.abspath(__file__))

# ---------- conversioni ----------
def dm(v, pos='N', neg='S', w=2):
    s=pos if v>=0 else neg; v=abs(v); g=int(v); m=(v-g)*60
    if round(m,1)>=60: g+=1; m=0
    return f"{g:0{w}d}°{m:04.1f}′{s}".replace('.',',')
def lat_s(v): return dm(v,'N','S',2)
def lon_s(v): return dm(v,'E','W',3)
def parse_dm(g,m): return g+m/60
def norm(a): return a%360

# piano locale in miglia (x est, y nord), centrato su un riferimento
class Plane:
    def __init__(s, lat0, lon0): s.lat0=lat0; s.lon0=lon0; s.k=math.cos(math.radians(lat0))
    def xy(s, lat, lon): return ((lon-s.lon0)*60*s.k, (lat-s.lat0)*60)
    def ll(s, x, y): return (s.lat0+y/60, s.lon0+x/60/s.k)
def u(b): r=math.radians(b); return (math.sin(r), math.cos(r))
def add(a,b,k=1): return (a[0]+k*b[0], a[1]+k*b[1])
def sub(a,b): return (a[0]-b[0], a[1]-b[1])
def dist(a,b): return math.hypot(a[0]-b[0], a[1]-b[1])
def brg(a,b): return norm(math.degrees(math.atan2(b[0]-a[0], b[1]-a[1])))
def solve2(a,b,c):
    det=a[0]*b[1]-a[1]*b[0]; return ((c[0]*b[1]-c[1]*b[0])/det, (a[0]*c[1]-a[1]*c[0])/det)
def cross_lines(p1,b1,p2,b2):
    """intersezione della retta per p1 con direzione b1 e della retta per p2 con direzione b2"""
    s,t=solve2(u(b1), (-u(b2)[0],-u(b2)[1]), sub(p2,p1)); return add(p1,u(b1),s)

# ---------- tabella di deviazione (DD 131/2022) ----------
DEV={0:-2,5:-2,10:-2,15:-3,20:-3,25:-3,30:-3,35:-3,40:-3,45:-4,50:-4,55:-4,60:-4,65:-4,70:-4,75:-4,80:-5,85:-5,90:-5,95:-4,100:-3,105:-2,110:-2,115:-1,120:-1,125:0,
     130:1,135:2,140:2,145:2,150:2,155:2,160:3,165:3,170:3,175:3,180:3,185:4,190:4,195:4,200:4,205:5,210:5,215:5,220:5,225:5,230:4,235:4,240:3,245:3,250:2,255:2,
     260:1,265:0,270:-1,275:-1,280:-1,285:-2,290:-2,295:-2,300:-3,305:-3,310:-3,315:-3,320:-3,325:-2,330:-2,335:-2,340:-2,345:-2,350:-2,355:-2}
def dev_pm(pm):
    pm=norm(pm); a=int(pm//5)*5; b=(a+5)%360; f=(pm-a)/5
    return DEV[a]*(1-f)+DEV[b]*f

# ---------- punti cospicui (OpenStreetMap, © contributori OSM, ODbL) ----------
LM=json.load(open(os.path.join(D,'landmarks.json')))
def lm(name): return tuple(LM[name][:2])

# ---------- costa ----------
def coast_rings():
    cache=os.path.join(D,'coast_rings.json')
    if os.path.exists(cache): return json.load(open(cache))
    ways=json.load(open(os.path.join(D,'coast.json')))['elements']
    segs=[[ (g['lat'],g['lon']) for g in w['geometry']] for w in ways]
    ids=[(w['nodes'][0],w['nodes'][-1]) for w in ways]
    bystart={}
    for i,(a,b) in enumerate(ids): bystart.setdefault(a,[]).append(i)
    used=set(); rings=[]
    for i in range(len(segs)):
        if i in used: continue
        used.add(i); chain=list(segs[i]); start,end=ids[i]
        while end!=start:
            nxt=[j for j in bystart.get(end,[]) if j not in used]
            if not nxt: break
            j=nxt[0]; used.add(j); chain+=segs[j][1:]; end=ids[j][1]
        # prova ad allungare all'indietro
        byend={}
        rings.append({'closed':end==start,'pts':chain})
    json.dump(rings,open(cache,'w'))
    return rings
