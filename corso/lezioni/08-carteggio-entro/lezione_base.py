"""Strumenti comuni per generare le lezioni (slide, disegni, quiz)."""
import json, math, os, sys, datetime, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import *
SP=os.path.dirname(os.path.abspath(__file__))
Q={x['p']:x for x in json.load(open(SP+'/rotta-giusta/site/dati/quiz.json'))}
RED='#D63B3B'; GREEN_S='#2E9E5B'; WATER='#12A4B5'
slides=[]
ICON_T={}
def sec(id, inner, notes='', dark=False, gap=32, pinned=''):
    n=len(slides)+1; bg = NAVY if dark else PAPER; col = '#FFFFFF' if dark else BODY
    slides.append((id, f'<section id="{id}" data-transition="fade" style="background:{bg}; color:{col}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">\n{backdrop(dark,n)}\n{inner}\n{pinned}{footer(n,dark)}\n<aside>{notes}</aside>\n</section>\n'))
def head(e,t,c=None):
    return header(e,t,'quiz' if t.startswith(('Quiz','Verifica')) else ICON_T.get(t,'lifebuoy'),c)
def lab(x,y,w,t,color=INK,size=24,weight=700,align='left',bg=None):
    b=f' background:{bg}; padding:2px 10px; border-radius:10px;' if bg else ''
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-size:{size}px; line-height:1.3; font-weight:{weight}; color:{color}; text-align:{align};{b}">{t}</p>'
def svgp(x,y,w,h,body,alt,pan=True):
    if pan: body=panel(w,h,body,wind=False)
    return f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px">{body}</svg>'
def svgi(w,h,body,alt,dw=None,dh=None,pan=True):
    if pan: body=panel(w,h,body,wind=False,waves=False)
    return f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="width:{dw or w}px; height:{dh or h}px; flex:none">{body}</svg>'
def arrow(x1,y1,x2,y2,c=NAVY,w=3,hs=13):
    a=math.atan2(y2-y1,x2-x1); bx=x2-hs*math.cos(a); by=y2-hs*math.sin(a)
    p1=(bx+hs*0.5*math.sin(a), by-hs*0.5*math.cos(a)); p2=(bx-hs*0.5*math.sin(a), by+hs*0.5*math.cos(a))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>')
def head_at(x,y,ang,c,hs=18):
    a=math.radians(ang); bx=x-hs*math.cos(a); by=y-hs*math.sin(a)
    return f'<polygon points="{x:.1f},{y:.1f} {bx+hs*0.55*math.sin(a):.1f},{by-hs*0.55*math.cos(a):.1f} {bx-hs*0.55*math.sin(a):.1f},{by+hs*0.55*math.cos(a):.1f}" fill="{c}"/>'
def dpath(d,c=CORAL,w=6,dashed=True):
    da=' stroke-dasharray="16 12"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{da}/>'
def dim(x1,y1,x2,y2,c=NAVY):
    return arrow((x1+x2)/2,(y1+y2)/2,x1,y1,c,2.5,12)+arrow((x1+x2)/2,(y1+y2)/2,x2,y2,c,2.5,12)
def dash(x1,y1,x2,y2,c=SOFT,w=2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-dasharray="8 6"/>'
def line(x1,y1,x2,y2,c=NAVY,w=2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
def term(t,d): return f'<div style="display:flex; flex-direction:column; gap:4px">{p(t,28,INK,800,1.3)}{p(d,26,BODY)}</div>'
def curved(cx,cy,r,a0,a1,c=CORAL,w=6):
    x0,y0=cx+r*math.cos(math.radians(a0)),cy+r*math.sin(math.radians(a0)); x1,y1=cx+r*math.cos(math.radians(a1)),cy+r*math.sin(math.radians(a1))
    sweep=1 if a1>a0 else 0; large=1 if abs(a1-a0)>180 else 0
    s=f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    tang=a1+(90 if sweep else -90)
    return s+head_at(x1+3*math.cos(math.radians(tang)),y1+3*math.sin(math.radians(tang)),tang,c,18)
def num(x,y,n,c=CORAL,r=18):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/><text x="{x}" y="{y+8}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{int(r*1.2)}" font-weight="700" fill="#FFFFFF">{n}</text>'
# ---- barca vista dall'alto (prua verso ang: 0=destra, -90=su) ----
def topboat(cx,cy,L,ang=-90,fill='#FFFFFF',st=NAVY,sw=4,op=1,cockpit=True):
    W=L*0.2
    d=f'M{L/2:.1f} 0 Q{L*0.2:.1f} {-W:.1f} {-L*0.42:.1f} {-W*0.82:.1f} L{-L/2:.1f} {-W*0.6:.1f} L{-L/2:.1f} {W*0.6:.1f} L{-L*0.42:.1f} {W*0.82:.1f} Q{L*0.2:.1f} {W:.1f} {L/2:.1f} 0 Z'
    g=f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    if cockpit: g+=f'<rect x="{-L*0.36:.1f}" y="{-W*0.45:.1f}" width="{L*0.3:.1f}" height="{W*0.9:.1f}" rx="{W*0.3:.1f}" fill="none" stroke="{st}" stroke-width="{sw*0.6:.1f}"/>'
    return f'<g transform="translate({cx} {cy}) rotate({ang})" opacity="{op}">{g}</g>'
# ---- barca di profilo (prua a destra) ----
def P(x0,wl,L,x,y): return (x0+x*L, wl+y*L)
def fmt(pt): return f'{pt[0]:.1f} {pt[1]:.1f}'
def profile(x0,wl,L,hull=BOAT,uw=CORAL,st=NAVY,sw=3,fly=False,deck2=False,sil=False,sup=True):
    f=lambda x,y: fmt(P(x0,wl,L,x,y))
    hullp=f'M{f(0,-0.09)} L{f(1.0,-0.13)} Q{f(1.01,-0.05)} {f(0.9,0.05)} L{f(0.12,0.06)} L{f(0.02,0.03)} Z'
    uwp=f'M{f(0.015,0)} L{f(0.943,0)} Q{f(0.924,0.028)} {f(0.9,0.05)} L{f(0.12,0.06)} L{f(0.02,0.03)} Z'
    supp=f'M{f(0.30,-0.102)} L{f(0.70,-0.118)} L{f(0.64,-0.19)} L{f(0.36,-0.19)} Z'
    if sil: return f'<path d="{hullp}" fill="{st}"/><path d="{supp}" fill="{st}"/>'
    s=f'<path d="{hullp}" fill="{hull}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    s+=f'<path d="{uwp}" fill="{uw}" fill-opacity="0.95"/><path d="M{f(0.02,-0.012)} L{f(0.955,-0.012)}" stroke="{BLUE}" stroke-width="{sw+4}"/>'
    s+=f'<path d="{hullp}" fill="none" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    if sup:
        s+=f'<path d="{supp}" fill="{hull}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
        for i in range(4):
            a=0.40+i*0.065; s+=f'<path d="M{f(a,-0.165)} L{f(a+0.045,-0.165)} L{f(a+0.045,-0.135)} L{f(a,-0.135)} Z" fill="{st}" fill-opacity="0.8"/>'
    return s
def water(w,y0,y1,op=0.16):
    return f'<rect x="0" y="{y0}" width="{w}" height="{y1-y0}" fill="{WATER}" fill-opacity="{op}"/>'+line(0,y0,w,y0,SEA,3)
# ---- quiz ----
def quiz_slide(id_, title, ps, reveal):
    cards=''
    for i,pp in enumerate(ps):
        x=Q[pp]; assert not x.get('osc'), pp; opts=''
        for j,o in enumerate(x['r']):
            o=o.strip().rstrip(';').rstrip(',')
            if reveal and j==x['x']:
                opts+=f'<div style="display:flex; gap:10px; align-items:start; background:{SEA_T}; padding:10px 12px; border-radius:14px; border:3px solid {SEA}"><x-icon name="CheckCircle" style="color:{SEA}; width:30px; height:30px"></x-icon><p style="font-size:24px; line-height:1.35; font-weight:800; color:{INK}">{"abc"[j]}) {o}</p></div>'
            else:
                c = SOFT if reveal else BODY
                opts+=f'<p style="font-size:24px; line-height:1.35; color:{c}; padding:10px 12px">{"abc"[j]}) {o}</p>'
        foot = f'<p style="font-size:24px; font-weight:800; color:{SEA}">Risposta esatta: {"abc"[x["x"]]}</p>' if reveal else ''
        cards+=card(f'<p style="font-size:24px; font-weight:800; color:{CORAL}">Domanda {i+1} · quiz {pp}</p><p style="font-size:26px; line-height:1.35; font-weight:800; color:{INK}">{x["d"].strip()}</p><div style="display:flex; flex-direction:column; gap:6px">{opts}</div>{foot}', None if not reveal else '#FFFFFF', 28, 14)
    e = 'Verifica · risposte esatte' if reveal else 'Verifica · quiz ufficiali DD 131/2022'
    notes = ('Risposte: ' + '; '.join(f'{pp} → {"abc"[Q[pp]["x"]]}) {Q[pp]["r"][Q[pp]["x"]].strip()}' for pp in ps)) if reveal else 'Leggere le domande, lasciare un minuto per rispondere, poi passare alla slide con le risposte esatte.'
    sec(id_, head(e, title, SEA if reveal else CORAL)+f'<div style="display:flex; gap:24px; align-items:stretch">{cards}</div>', notes=notes)
def cover(lesson_no, title, subtitle, notes):
    slides.append(('cover', f'''<section id="cover" data-transition="fade" style="background:{NAVY}; color:#FFFFFF; font-family:{B}; padding:128px; display:flex; flex-direction:column; justify-content:space-between">
{backdrop(True,0)}
{lockup(True,112)}
<div style="display:flex; flex-direction:column; gap:20px; width:840px">
<p style="font-family:{HAND}; font-size:48px; font-weight:700; line-height:1.1; color:{DACC}">Lezione {lesson_no:02d} · 2 ore</p>
<h1 style="font-family:{H}; font-size:104px; font-weight:700; line-height:1.05; color:#FFFFFF">{title}</h1>{squiggle(DACC,330)}
<p style="font-size:34px; line-height:1.4; color:{DSOFT}">{subtitle}</p>
</div>
<p style="font-size:24px; font-weight:600; color:{DSOFT}">Patente nautica Vela/Motore senza limiti dalla costa</p>
<svg aria-label="Illustrazione: barca a vela e motoscafo sul mare con sole, nuvole e gabbiani" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 792 450" width="792" height="450" style="position:absolute; left:1000px; top:470px; width:792px; height:450px">{sea_scene(792,450)}</svg>
<aside>{notes}</aside>
</section>
'''))
def closing(points, nxt, notes=''):
    ul=''.join(f'<li>{x}</li>' for x in points)
    n=len(slides)+1
    slides.append(('chiusura', f'''<section id="chiusura" data-transition="fade" style="background:{NAVY}; color:#FFFFFF; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:40px">
{backdrop(True,n)}
{header('In sintesi','Cinque cose da ricordare','flag',CORAL,True)}
<ol style="font-size:30px; line-height:1.45; color:{DSOFT}; display:flex; flex-direction:column; gap:14px; width:1500px">{ul}</ol>
<p style="font-family:{HAND}; font-size:44px; font-weight:700; color:{DACC}">{nxt}</p>
{footer(n,True)}
<aside>{notes}</aside>
</section>
'''))
def write_deck(out, title, order, sections):
    d=dict(slides); assert sorted(d)==sorted(order),(set(d)^set(order))
    os.makedirs(out+'/slides',exist_ok=True)
    for k,i in enumerate(order,1):
        h=re.sub(r'(border-radius:20px">)\d\d(</p>)', lambda m: f'{m.group(1)}{k:02d}{m.group(2)}', d[i])
        open(f'{out}/slides/{i}.html','w').write(h)
    deck={"v":4,"createdOnFiles":{"v":1,"at":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')},"title":title,"order":order,"cover":"cover","sections":sections,"faces":FACES,"designSystems":[]}
    json.dump(deck,open(out+'/deck.json','w'),ensure_ascii=False,indent=1)
    for i in order:
        h=open(f'{out}/slides/{i}.html').read()
        for m in re.finditer(r'<svg.*?</svg>',h,re.S):
            if len(m.group(0))>52000: print('BIG SVG',i,len(m.group(0)))
    print(len(order),'slides')
