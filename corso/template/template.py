"""Template informale delle slide del corso (Fabrizio Fiorucci)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bg import backdrop

NAVY='#10263A'; PAPER='#F5F1E8'; CARD='#EAE4D6'; ACC='#A8432A'; TEAL='#1F6F78'; TEALCARD='#DCE8E6'
INK='#14212E'; BODY='#3A4652'; SOFT='#5C6874'; DSOFT='#B9C7D2'; DACC='#E9A07F'; BOAT='#FBF9F4'
CH1='#008C9E'; CH2='#C0582C'   # coppia validata per i grafici (5/D, 42/D)
H="'Fredoka', 'Trebuchet MS', sans-serif"; B="'Nunito Sans', Arial, sans-serif"; HAND="'Caveat', 'Brush Script MT', cursive"
RADIUS=24
FACES={"fredoka":{"family":"Fredoka","href":"https://fonts.googleapis.com/css2?family=Fredoka:wght@400..700&display=swap"},
       "nunito-sans":{"family":"Nunito Sans","href":"https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400..800&display=swap"},
       "caveat":{"family":"Caveat","href":"https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap"}}

W='#FFF7EC'
S=f'stroke="{W}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"'
F=f'fill="{W}"'
def _prop():
    return f'<circle cx="50" cy="50" r="9" {F}/>'+''.join(f'<ellipse cx="50" cy="25" rx="11" ry="20" {F} transform="rotate({a} 50 50)"/>' for a in (0,120,240))
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
}
def badge(icon, color=ACC, size=104, alt=None):
    alt = alt if alt is not None else ''
    return (f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 104 104" width="104" height="104" style="width:{size}px; height:{size}px">'
            f'<circle cx="52" cy="52" r="50" fill="{color}"/>'+(f'<circle cx="52" cy="52" r="43" fill="none" stroke="{W}" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="3 6"/>' if size>=76 else '')+
            f'<g transform="translate(22 22) scale(0.6)">{ICONS[icon]}</g></svg>')
def wave(color=ACC, w=220):
    return (f'<svg aria-label="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 16" width="{w}" height="16" style="width:{w}px; height:16px">'
            f'<path d="M4 8 ' + ' '.join('q13.5 -8 27 0 t27 0' for _ in range(w//54)) + f'" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/></svg>')
def header(eyebrow, title, icon='lifebuoy', color=ACC, dark=False, size=60):
    ec = DACC if dark and color==ACC else ('#7FC8D2' if dark else color)
    tc = PAPER if dark else INK
    return (f'<div style="display:flex; gap:28px; align-items:center">{badge(icon,color)}'
            f'<div style="display:flex; flex-direction:column; gap:2px">'
            f'<p style="font-family:{HAND}; font-size:42px; font-weight:700; line-height:1.1; color:{ec}">{eyebrow}</p>'
            f'<h2 style="font-family:{H}; font-size:{size}px; font-weight:600; line-height:1.1; color:{tc}">{title}</h2>'
            f'{wave(ec)}</div></div>')

def logo(dark=False, style='', label='Logo Fabrizio Fiorucci'):
    ring,acc,wv = ('#F5F1E8','#E9A07F','#7FB8BF') if dark else (NAVY,ACC,TEAL)
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
      +f'<p style="position:absolute; left:192px; bottom:64px; width:1200px; font-size:24px; color:{c}">Fabrizio Fiorucci · Patente nautica Vela/Motore senza limiti dalla costa</p>'
      +f'<p style="position:absolute; right:128px; bottom:64px; width:200px; font-size:24px; font-weight:700; color:{c}; text-align:right">{n:02d}</p>')
def lockup(dark=True, size=112):
    nc = PAPER if dark else INK; sc = DACC if dark else ACC
    return (f'<div style="display:flex; gap:28px; align-items:center">{logo(dark,f"width:{size}px; height:{size}px","Logo Fabrizio Fiorucci: sloop a vela dentro una bussola")}'
            f'<div style="display:flex; flex-direction:column; gap:0px"><p style="font-family:{H}; font-size:44px; font-weight:600; line-height:1.15; color:{nc}">Fabrizio Fiorucci</p>'
            f'<p style="font-family:{HAND}; font-size:36px; font-weight:700; line-height:1.1; color:{sc}">skipper e istruttore di vela</p></div></div>')
def card(inner,bg=CARD,pad=32,gap=12,flex=1,extra=''):
    return f'<div style="flex:{flex}; display:flex; flex-direction:column; gap:{gap}px; background:{bg}; padding:{pad}px; border-radius:{RADIUS}px{extra}">{inner}</div>'
def h3(t,size=32,color=INK): return f'<h3 style="font-family:{H}; font-size:{size}px; font-weight:600; line-height:1.2; color:{color}">{t}</h3>'
def p(t,size=24,color=BODY,weight=400,lh=1.4): return f'<p style="font-size:{size}px; line-height:{lh}; color:{color}; font-weight:{weight}">{t}</p>'
def tag(t,c=ACC): return f'<p style="font-size:24px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:{c}">{t}</p>'
def note(t,c=ACC,size=32): return f'<p style="font-family:{HAND}; font-size:{size}px; font-weight:700; line-height:1.15; color:{c}">{t}</p>'
