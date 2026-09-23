"""Template creativo e colorato delle slide del corso (Fabrizio Fiorucci)."""
import math, os, sys, itertools
# ---------------- palette ----------------
INK='#1B2A41'; BODY='#34465E'; SOFT='#5E6E82'; PAPER='#FFF8EE'; NAVY='#16324F'
CORAL='#E4572E'; SEA='#0B8A99'; SUN='#F4A300'; GREEN='#2E9E5B'; BLUE='#2F6FDB'; PURPLE='#7B5CD6'
CORAL_T='#FFE3D9'; SUN_T='#FFF0C9'; SEA_T='#D5F3F5'; GREEN_T='#DFF3E4'; BLUE_T='#E1EAFD'; LILAC_T='#ECE6FB'
DSOFT='#C9D6E3'; DACC='#FFC145'; BOAT='#FFFDF8'
ACC=CORAL; TEAL=SEA; CARD=SUN_T; TEALCARD=SEA_T
CH1='#008C9E'; CH2='#C0582C'
TINTS=[SUN_T,SEA_T,CORAL_T,GREEN_T,BLUE_T,LILAC_T]
HUES=[CORAL,SEA,PURPLE,BLUE,GREEN]
H="'Fredoka', 'Trebuchet MS', sans-serif"; B="'Nunito Sans', Arial, sans-serif"; HAND="'Caveat', 'Brush Script MT', cursive"
RADIUS=36
FACES={"fredoka":{"family":"Fredoka","href":"https://fonts.googleapis.com/css2?family=Fredoka:wght@400..700&display=swap"},
       "nunito-sans":{"family":"Nunito Sans","href":"https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400..900&display=swap"},
       "caveat":{"family":"Caveat","href":"https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap"}}

# ---------------- sfondo: forme morbide ----------------
def blob(cx,cy,r,seed=0,k=0.18,n=7):
    pts=[]
    for i in range(n):
        a=2*math.pi*i/n; rr=r*(1+k*math.sin(3*a+seed)+0.5*k*math.cos(5*a+seed*1.7))
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d=f'M{(pts[0][0]+pts[1][0])/2:.1f} {(pts[0][1]+pts[1][1])/2:.1f} '
    for i in range(n):
        p1=pts[(i+1)%n]; p2=pts[(i+2)%n]; d+=f'Q{p1[0]:.1f} {p1[1]:.1f} {(p1[0]+p2[0])/2:.1f} {(p1[1]+p2[1])/2:.1f} '
    return d+'Z'
def wavepath(y,amp,period,x0=-200,x1=2200):
    d=f'M{x0} {y} '; x=x0
    while x<x1: d+=f'q{period/4} {-amp} {period/2} 0 t{period/2} 0 '; x+=period
    return d+f'L{x1} 1080 L{x0} 1080 Z'
def backdrop(dark=False, variant=0):
    v=variant%4
    if dark:
        s=(f'<path d="{blob(1790,110,300,1.1)}" fill="#1F4466"/><path d="{blob(-40,1080,240,2.3)}" fill="#1F4466"/>'
           
           f'<path d="{wavepath(975,16,360)}" fill="#12A4B5" fill-opacity="0.25"/><path d="{wavepath(1015,14,300,-120)}" fill="#12A4B5" fill-opacity="0.35"/>')
    else:
        tr=[SUN_T,SEA_T,LILAC_T,CORAL_T][v]; bl=[SEA_T,CORAL_T,SUN_T,GREEN_T][v]
        s=(f'<path d="{blob(1830,90,270,1.3+v)}" fill="{tr}"/><path d="{blob(40,1010,230,0.7+v)}" fill="{bl}"/>'
           f'<circle cx="1848" cy="560" r="26" fill="{[CORAL,SEA,SUN,PURPLE][v]}" fill-opacity="0.18"/><circle cx="1878" cy="630" r="12" fill="{[SEA,SUN,CORAL,GREEN][v]}" fill-opacity="0.25"/>'
           f'<path d="{wavepath(1000,12,340)}" fill="#12A4B5" fill-opacity="0.10"/><path d="{wavepath(1036,10,280,-90)}" fill="#12A4B5" fill-opacity="0.14"/>')
    return f'<svg aria-label="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute; left:0px; top:0px; width:1920px; height:1080px">{s}</svg>'

# ---------------- icone ----------------
W='#FFFFFF'
S=f'stroke="{W}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"'
F=f'fill="{W}"'
def _prop(): return f'<circle cx="50" cy="50" r="9" {F}/>'+''.join(f'<ellipse cx="50" cy="25" rx="11" ry="20" {F} transform="rotate({a} 50 50)"/>' for a in (0,120,240))
ICONS={
 'hull':f'<path d="M10 55 L90 55 L78 75 L22 75 Z" {F}/><path d="M34 55 L34 38 L64 38 L72 55" {S}/><path d="M8 90 q10.5 -7 21 0 t21 0 t21 0 t21 0" {S}/>',
 'propeller':_prop(),
 'compass':f'<circle cx="50" cy="50" r="38" {S}/><polygon points="50,14 58,50 50,86 42,50" {F}/><polygon points="14,50 50,42 86,50 50,58" {F} fill-opacity="0.7"/>',
 'anchor':f'<circle cx="50" cy="15" r="7" {S}/><path d="M50 22 L50 86 M32 36 L68 36 M16 60 Q22 86 50 86 Q78 86 84 60 M10 66 L16 58 L24 66 M76 66 L84 58 L90 66" {S}/>',
 'lighthouse':f'<polygon points="40,36 60,36 68,90 32,90" {S}/><rect x="38" y="16" width="24" height="20" {S}/><path d="M34 62 L66 62 M22 20 L8 14 M22 30 L6 32 M78 20 L92 14 M78 30 L94 32" {S}/>',
 'lantern':f'<rect x="30" y="28" width="40" height="52" rx="8" {S}/><path d="M36 28 L42 14 L58 14 L64 28 M30 54 L70 54 M16 42 L4 38 M16 60 L4 64 M84 42 L96 38 M84 60 L96 64" {S}/>',
 'cloud':f'<path d="M26 62 Q10 62 12 50 Q14 38 28 40 Q32 22 52 24 Q70 26 72 42 Q88 42 88 52 Q88 62 76 62 Z" {S}/><path d="M18 78 L60 78 M38 92 L82 92" {S}/>',
 'sail':f'<path d="M50 8 L50 76" {S}/><path d="M45 14 L45 70 L12 70 Z" {F}/><path d="M56 22 L56 70 L86 70 Z" {F} fill-opacity="0.75"/><path d="M8 78 L92 78 L80 92 L20 92 Z" {F}/>',
 'lifebuoy':f'<circle cx="50" cy="50" r="30" fill="none" stroke="{W}" stroke-opacity="0.45" stroke-width="18"/><circle cx="50" cy="50" r="30" fill="none" stroke="{W}" stroke-width="18" stroke-dasharray="23.6 23.6" transform="rotate(-11 50 50)"/>',
 'dividers':f'<circle cx="50" cy="14" r="7" {S}/><path d="M46 21 L24 90 M54 21 L76 90 M33 60 L67 60" {S}/>',
 'fuel':f'<path d="M22 28 L64 28 L78 42 L78 90 L22 90 Z" {S}/><path d="M64 28 L64 14 L82 14" {S}/><rect x="34" y="46" width="30" height="26" rx="4" {S}/>',
 'wind':f'<path d="M8 36 L60 36 Q76 36 76 24 Q76 12 64 14 M8 56 L78 56 Q92 56 92 68 Q92 82 78 80 M8 76 L46 76" {S}/>',
 'current':f'<path d="M8 36 q10.5 -8 21 0 t21 0 t21 0 t21 0 M8 58 q10.5 -8 21 0 t21 0 t21 0 t21 0 M18 84 L80 84 M66 74 L80 84 L66 94" {S}/>',
 'map':f'<path d="M10 22 L36 12 L64 22 L90 12 L90 78 L64 88 L36 78 L10 88 Z M36 12 L36 78 M64 22 L64 88" {S}/><circle cx="76" cy="36" r="6" {F}/>',
 'book':f'<path d="M50 24 Q30 12 10 18 L10 82 Q30 76 50 88 Q70 76 90 82 L90 18 Q70 12 50 24 Z M50 24 L50 88" {S}/>',
 'check':f'<circle cx="50" cy="50" r="38" {S}/><path d="M30 52 L44 66 L72 36" {S}/>',
 'chart':f'<path d="M12 88 L90 88" {S}/><rect x="18" y="50" width="16" height="36" rx="3" {F}/><rect x="42" y="26" width="16" height="60" rx="3" {F}/><rect x="66" y="60" width="16" height="26" rx="3" {F}/>',
 'pencil':f'<path d="M20 80 L24 64 L68 20 L80 32 L36 76 Z M60 28 L72 40 M10 92 L90 92" {S}/>',
 'grid':''.join(f'<rect x="{12+x*28}" y="{22+y*30}" width="22" height="24" rx="6" {F}/>' for x in range(3) for y in range(2)),
 'flag':f'<path d="M24 10 L24 92" {S}/><path d="M28 14 L82 14 L70 32 L82 50 L28 50 Z" {F}/>',
 'helm':f'<circle cx="50" cy="50" r="26" {S}/><circle cx="50" cy="50" r="7" {F}/>'+''.join(f'<line x1="{50+7*math.cos(math.radians(a)):.1f}" y1="{50+7*math.sin(math.radians(a)):.1f}" x2="{50+42*math.cos(math.radians(a)):.1f}" y2="{50+42*math.sin(math.radians(a)):.1f}" {S}/>' for a in range(0,360,45)),
 'quiz':f'<rect x="16" y="12" width="68" height="80" rx="10" {S}/><path d="M30 34 L40 44 L56 26 M30 62 L70 62 M30 76 L60 76" {S}/>',
 'star':f'<polygon points="50,8 61,38 94,38 67,58 77,90 50,70 23,90 33,58 6,38 39,38" {F}/>',
}
def badge(icon, color=CORAL, size=104, alt=None):
    return (f'<svg aria-label="{alt or ""}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 104 104" width="104" height="104" style="width:{size}px; height:{size}px; flex:none">'
            f'<path d="{blob(52,52,47,1.0,0.07,8)}" fill="{color}"/>'
            f'<g transform="translate(22 22) scale(0.6)">{ICONS[icon]}</g></svg>')
def squiggle(color=CORAL, w=180):
    return (f'<svg aria-label="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 18" width="{w}" height="18" style="width:{w}px; height:18px">'
            f'<path d="M5 9 ' + ' '.join('q11 -10 22 0 t22 0' for _ in range(w//44)) + f'" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/></svg>')
wave=squiggle
_hue=itertools.cycle(HUES)
def header(eyebrow, title, icon='lifebuoy', color=None, dark=False, size=64):
    c = color or next(_hue)
    tc = '#FFFFFF' if dark else c
    return (f'<div style="display:flex; gap:28px; align-items:center">{badge(icon,c)}'
            f'<div style="display:flex; flex-direction:column; gap:8px; align-items:start">'
            f'<p style="font-size:24px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:#FFFFFF; background:{c}; padding:4px 18px; border-radius:30px">{eyebrow}</p>'
            f'<h2 style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1.05; color:{tc}">{title}</h2></div></div>')

def logo(dark=False, style='', label='Logo Fabrizio Fiorucci'):
    ring,acc,wv = ('#FFF8EE','#FFC145','#7FD3DC') if dark else (NAVY,CORAL,SEA)
    ticks=''.join(f'<line x1="{100+78*math.cos(a):.1f}" y1="{100+78*math.sin(a):.1f}" x2="{100+86*math.cos(a):.1f}" y2="{100+86*math.sin(a):.1f}" stroke="{ring}" stroke-width="4" stroke-linecap="round"/>'
                  for a in [math.radians(d) for d in range(0,360,45) if d!=270])
    return (f'<svg aria-label="{label}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200" style="{style}">'
      f'<circle cx="100" cy="100" r="92" fill="none" stroke="{ring}" stroke-width="7"/>{ticks}'
      f'<path d="M100 16 L109 34 L91 34 Z" fill="{acc}"/><path d="M97 42 L97 132 L46 132 Q66 92 97 42 Z" fill="{ring}"/>'
      f'<path d="M104 54 L104 132 L148 132 Q128 96 104 54 Z" fill="{acc}"/><path d="M44 140 L156 140 Q148 156 126 158 L74 158 Q52 156 44 140 Z" fill="{ring}"/>'
      f'<path d="M50 173 Q62.5 165 75 173 T100 173 T125 173 T150 173" fill="none" stroke="{wv}" stroke-width="6" stroke-linecap="round"/></svg>')
def footer(n, dark=False):
    c = DSOFT if dark else SOFT
    return (logo(dark,'position:absolute; left:128px; bottom:56px; width:48px; height:48px')
      +f'<p style="position:absolute; left:192px; bottom:64px; width:1200px; font-size:24px; font-weight:600; color:{c}">Fabrizio Fiorucci · Patente nautica Vela/Motore senza limiti dalla costa</p>'
      +f'<p style="position:absolute; right:128px; bottom:58px; width:64px; font-family:{H}; font-size:26px; font-weight:700; color:#FFFFFF; background:{CORAL if not dark else SEA}; text-align:center; padding:2px 0px; border-radius:20px">{n:02d}</p>')
def lockup(dark=True, size=112):
    nc = '#FFFFFF' if dark else INK; sc = DACC if dark else CORAL
    return (f'<div style="display:flex; gap:28px; align-items:center">{logo(dark,f"width:{size}px; height:{size}px","Logo Fabrizio Fiorucci: sloop a vela dentro una bussola")}'
            f'<div style="display:flex; flex-direction:column; gap:0px"><p style="font-family:{H}; font-size:44px; font-weight:700; line-height:1.15; color:{nc}">Fabrizio Fiorucci</p>'
            f'<p style="font-family:{HAND}; font-size:38px; font-weight:700; line-height:1.1; color:{sc}">skipper e istruttore di vela</p></div></div>')
PANEL='#E4F3F1'; PANEL_W='#C9E6E2'; SHADOW='box-shadow:0px 10px 28px rgba(27,42,65,0.10)'
_acc=itertools.cycle([CORAL,SEA,SUN,PURPLE,BLUE,GREEN])
def card(inner,bg=None,pad=32,gap=12,flex=1,extra=''):
    if bg in (None,CARD):
        return (f'<div style="flex:{flex}; display:flex; flex-direction:column; gap:{gap}px; background:#FFFFFF; border-left:12px solid {next(_acc)}; '
                f'{SHADOW}; padding:{pad}px; border-radius:{RADIUS-8}px{extra}">{inner}</div>')
    return f'<div style="flex:{flex}; display:flex; flex-direction:column; gap:{gap}px; background:{bg}; padding:{pad}px; border-radius:{RADIUS}px{extra}">{inner}</div>'
_pid=itertools.count(1)
def panel(w,h,body,wind=True,waves=True):
    """Pannello illustrato: fondo verde mare arrotondato, onde e frecce del vento."""
    i=next(_pid); deco=''
    if waves:
        for (x,y) in [(0.07,0.2),(0.8,0.3),(0.1,0.86),(0.72,0.9)]:
            deco+=f'<path d="M{w*x:.0f} {h*y:.0f} q18 -10 36 0 t36 0 t36 0" fill="none" stroke="{PANEL_W}" stroke-width="5" stroke-linecap="round"/>'
    if wind:
        for (x,l) in [(0.5,70),(0.93,46)]:
            deco+=f'<path d="M{w*x:.0f} 26 L{w*x:.0f} {26+l}" stroke="#97A6B4" stroke-width="7" stroke-linecap="round"/><polygon points="{w*x-16:.0f},{20+l} {w*x+16:.0f},{20+l} {w*x:.0f},{44+l}" fill="#97A6B4"/>'
    return (f'<defs><clipPath id="pn{i}"><rect x="0" y="0" width="{w}" height="{h}" rx="40"/></clipPath></defs>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="40" fill="{PANEL}"/><g clip-path="url(#pn{i})">{deco}{body}</g>')
def h3(t,size=32,color=INK): return f'<h3 style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1.15; color:{color}">{t}</h3>'
def p(t,size=24,color=BODY,weight=400,lh=1.4): return f'<p style="font-size:{size}px; line-height:{lh}; color:{color}; font-weight:{weight}">{t}</p>'
def tag(t,c=CORAL): return f'<p style="font-size:24px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:{c}">{t}</p>'
def note(t,c=CORAL,size=34): return f'<p style="font-family:{HAND}; font-size:{size}px; font-weight:700; line-height:1.15; color:{c}">{t}</p>'

# ---------------- scena illustrata (copertine) ----------------
def cloud(x,y,s=1.0,fill='#FFFFFF',op=1):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}" fill-opacity="{op}"><ellipse cx="0" cy="0" rx="60" ry="30"/><ellipse cx="-40" cy="10" rx="40" ry="24"/>'
            f'<ellipse cx="45" cy="12" rx="44" ry="22"/><ellipse cx="5" cy="-18" rx="36" ry="28"/></g>')
def gull(x,y,s=1.0,c='#FFFFFF'):
    return f'<path d="M{x-18*s} {y} Q{x-9*s} {y-10*s} {x} {y} Q{x+9*s} {y-10*s} {x+18*s} {y}" fill="none" stroke="{c}" stroke-width="{4*s:.1f}" stroke-linecap="round"/>'
def sailboat(x,y,s=1.0,main='#FFFFFF',jib=None,hull='#FFFFFF',stripe=CORAL):
    jib=jib or SUN
    g=(f'<path d="M-130 0 L130 0 Q118 34 86 42 L-96 42 Q-122 34 -130 0 Z" fill="{hull}"/><path d="M-126 12 L126 12" stroke="{stripe}" stroke-width="9"/>'
       f'<path d="M-4 0 L-4 -250" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M-12 -236 L-12 -12 L-124 -12 Q-70 -110 -12 -236 Z" fill="{main}"/>'
       f'<path d="M6 -212 L6 -12 L112 -12 Q72 -110 6 -212 Z" fill="{jib}"/><path d="M-4 -250 L28 -242 L-4 -234 Z" fill="{CORAL}"/>')
    return f'<g transform="translate({x} {y}) scale({s})">{g}</g>'
def motorboat(x,y,s=1.0,hull='#FFFFFF',stripe=SEA):
    g=(f'<path d="M-120 0 L130 -8 Q138 18 108 34 L-110 36 Z" fill="{hull}"/><path d="M-116 16 L126 10" stroke="{stripe}" stroke-width="8"/>'
       f'<path d="M-50 -2 L60 -6 L36 -46 L-30 -46 Z" fill="{hull}"/><path d="M-20 -38 L28 -38 L40 -16 L-24 -14 Z" fill="{BLUE}" fill-opacity="0.8"/>')
    return f'<g transform="translate({x} {y}) scale({s})">{g}</g>'
def sea_scene(w, h, dark=True, sun=True, cid='scn'):
    s=''
    if sun: s+=f'<circle cx="{w*0.78:.0f}" cy="{h*0.26:.0f}" r="{h*0.16:.0f}" fill="{SUN if not dark else DACC}"/>'
    s+=cloud(w*0.2,h*0.2,0.9,'#FFFFFF',0.9 if not dark else 0.85)+cloud(w*0.62,h*0.12,0.6,'#FFFFFF',0.8)
    s+=gull(w*0.42,h*0.18,1.2)+gull(w*0.48,h*0.26,0.9)+gull(w*0.9,h*0.4,0.8)
    s+=motorboat(w*0.86,h*0.66,0.55)
    s+=sailboat(w*0.45,h*0.72,1.05)
    s+=f'<path d="{wavepath(h*0.74,14,160,-40,w+40).replace("1080",str(h))}" fill="#12A4B5"/>'
    s+=f'<path d="{wavepath(h*0.82,12,130,-80,w+40).replace("1080",str(h))}" fill="#0B8A99"/>'
    s+=f'<path d="{wavepath(h*0.9,10,110,-20,w+40).replace("1080",str(h))}" fill="#0A6F7B"/>'
    return f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="{w}" height="{h}" rx="48"/></clipPath></defs><rect x="0" y="0" width="{w}" height="{h}" rx="48" fill="#FFFFFF" fill-opacity="{0.06 if dark else 0.0}"/><g clip-path="url(#{cid})">{s}</g>'
