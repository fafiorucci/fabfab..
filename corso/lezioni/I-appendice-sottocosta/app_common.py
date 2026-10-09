"""Strumenti comuni per le appendici I, J, K, L (schede, tabelle, indice, disegni ricorrenti)."""
import math
from lezione_base import *
import lezione_base as LB

GREY='#97A6B4'; LRED='#E23B3B'; ORANGE='#F28C28'; LAND='#F2E2B3'; LAND_S='#C9A96B'; CHART='#FBF8EF'
SKY='#EAF4F7'; NIGHT='#0F2238'; STEEL='#8E9BAA'; SAND='#F3E3B8'; LWHITE='#FFF7D6'
X,Y,W,Hh=700,290,1092,620

def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=20,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
def col(inner,w=520,gap=20): return f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF'):
    return lab(x,y,w,t,tc,size,900,'left',bg=c).replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def dot(n,c): return f'<p style="width:44px; height:44px; border-radius:22px; background:{c}; color:#FFFFFF; font-weight:900; font-size:22px; text-align:center; line-height:44px; flex:none">{n}</p>'
def item(n,c,t,d): return f'<div style="display:flex; gap:16px; align-items:start">{dot(n,c)}<div style="display:flex; flex-direction:column; gap:4px">{p(t,28,INK,800,1.25)}{p(d,24,BODY)}</div></div>'
def table(head_cells,widths,rows,c=NAVY,size=26):
    pd='padding:12px 18px; '
    th=''.join(f'<th style="{pd}width:{w}%; color:#FFFFFF; text-align:left">{h}</th>' for h,w in zip(head_cells,widths))
    body=''
    for k,r in enumerate(rows):
        bg='#FFFFFF' if k%2==0 else PAPER
        body+=f'<tr style="background:{bg}">'+''.join(f'<td style="{pd}font-weight:800; color:{c}">{v}</td>' if j==0 else f'<td style="{pd}color:{INK}">{v}</td>' for j,v in enumerate(r))+'</tr>'
    return f'<table style="font-size:{size}px; line-height:1.3; color:{BODY}"><tr style="background:{c}">{th}</tr>{body}</table>'
HU=[CORAL,SEA,PURPLE,BLUE,GREEN,ORANGE]
def grid(cards,cols=3,tsize=34,dsize=28,gap=20):
    g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:26px 28px">{h3(t,tsize,c)}{p(d,dsize,BODY,400,1.4)}</div>' for t,d,c in cards)
    return f'<div style="display:grid; grid-template-columns:repeat({cols},1fr); gap:{gap}px">{g}</div>'
def tiles(cards,dsize=28):
    g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:26px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{squiggle(c,110)}{h3(t,32,c)}{p(d,dsize,BODY,400,1.4)}</div>' for t,d,c in cards)
    return f'<div style="display:flex; gap:22px; align-items:stretch">{g}</div>'
def steps(cards,dsize=26):
    g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:24px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{i+1}</p>{h3(t,30,c)}{p(d,dsize,BODY,400,1.4)}</div>' for i,(t,d,c) in enumerate(cards))
    return f'<div style="display:flex; gap:20px; align-items:stretch">{g}</div>'
def bignums(cards,cols=3):
    g=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:24px 26px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(d,26,INK,700,1.3)}</div>' for n,d,c in cards)
    return f'<div style="display:grid; grid-template-columns:repeat({cols},1fr); gap:18px">{g}</div>'
def script(title,lines,w=None,bg=NAVY):
    ww=f' width:{w}px;' if w else ' flex:1;'
    out=f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:30px 34px; border-radius:32px;{ww}"><p style="font-size:24px; font-weight:900; letter-spacing:1px; color:{DACC}">{title}</p>'
    for t,kind in lines:
        c={'k':'#FFFFFF','n':DSOFT,'m':'#FFFFFF','e':'#9FB3C8'}[kind]; wgt={'k':900,'n':700,'m':800,'e':700}[kind]
        out+=f'<p style="font-size:28px; line-height:1.3; color:{c}; font-weight:{wgt}">{t}</p>'
    return out+'</div>'
def index_slide(EB,IX,ORDER,foot,notes):
    N=lambda sid: f'{ORDER.index(sid)+1:02d}'
    cards=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:18px 24px">'
                  f'<p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:64px">{i+1:02d}</p>'
                  f'<div style="flex:1; display:flex; flex-direction:column; gap:4px">{p(t,32,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div>'
                  f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(ids[0])}{"–"+N(ids[-1]) if len(ids)>1 else ""}</p></div>' for i,(t,d,ids,c) in enumerate(IX))
    sec('indice', head(EB,'Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:18px">{cards}</div>'+note(foot,SEA,36), notes=notes)
def cover_app(letter,title,sub,notes):
    cover(0,title,sub,notes)
    LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore',f'Appendice {letter} · studio'))
    assert 'vele spiegate' in LB.slides[-1][1]

# ---- disegni ricorrenti ----
def tower(x,y,s=1):
    g=f'<path d="M{x-14*s} {y} L{x-8*s} {y-90*s} L{x+8*s} {y-90*s} L{x+14*s} {y} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/><rect x="{x-9*s}" y="{y-66*s}" width="{18*s}" height="{12*s}" fill="{CORAL}"/><rect x="{x-11*s}" y="{y-34*s}" width="{22*s}" height="{12*s}" fill="{CORAL}"/>'
    return g+f'<rect x="{x-11*s}" y="{y-110*s}" width="{22*s}" height="{20*s}" rx="{4*s}" fill="{SUN}" stroke="{NAVY}" stroke-width="{2.5*s}"/>'
def church(x,y,s=1):
    return (f'<rect x="{x-12*s}" y="{y-90*s}" width="{24*s}" height="{90*s}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="{3*s}"/>'
            f'<path d="M{x-16*s} {y-90*s} L{x} {y-124*s} L{x+16*s} {y-90*s} Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="{3*s}"/><rect x="{x-5*s}" y="{y-76*s}" width="{10*s}" height="{14*s}" fill="{NAVY}"/>')
def anchor_icon(x,y,s=1,c=NAVY):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round">'
            f'<circle cx="0" cy="-26" r="7"/><path d="M0 -19 V26 M-13 -9 H13 M-24 10 Q-20 28 0 26 Q20 28 24 10"/></g>')
def glow(x,y,c,r=9):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.8:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.7:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
def windarrow(x,y,l=80,c=GREY,ang=90):
    a=math.radians(ang); return arrow(x,y,x+l*math.cos(a),y+l*math.sin(a),c,8,26)
def person(x,y,c=CORAL,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-16" r="11" fill="#F2C9A0" stroke="{NAVY}" stroke-width="2"/><path d="M-14 -4 Q0 -10 14 -4 L12 16 L-12 16 Z" fill="{c}"/></g>'
def ring(x,y,r=22): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ORANGE}" stroke-width="{r*0.55:.0f}"/><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.55:.0f}" stroke-dasharray="{r*0.8:.0f} {r*0.8:.0f}"/>'
def flame(x,y,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 30 Q-26 10 -12 -22 Q-6 -8 0 -12 Q2 -34 16 -44 Q14 -20 24 -6 Q30 16 0 30 Z" fill="{ORANGE}"/><path d="M0 26 Q-12 12 -4 -6 Q2 4 6 -2 Q14 10 0 26 Z" fill="{SUN}"/></g>'
