"""Disegni delle ancore (dalla lezione 4)."""
import math
from app_common import *
def anatomy():
    b=f'<circle cx="560" cy="80" r="28" fill="none" stroke="{NAVY}" stroke-width="12"/>'
    b+=f'<rect x="400" y="128" width="320" height="24" rx="12" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/><circle cx="400" cy="140" r="16" fill="{NAVY}"/><circle cx="720" cy="140" r="16" fill="{NAVY}"/>'
    b+=f'<rect x="546" y="104" width="28" height="410" rx="10" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/>'
    b+=f'<path d="M340 390 Q380 530 560 530 Q740 530 780 390" fill="none" stroke="{NAVY}" stroke-width="30" stroke-linecap="round"/><path d="M340 390 Q380 530 560 530 Q740 530 780 390" fill="none" stroke="{STEEL}" stroke-width="18" stroke-linecap="round"/>'
    b+=f'<path d="M340 390 L290 330 L330 318 L372 370 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/><path d="M780 390 L830 330 L790 318 L748 370 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
    b+=f'<circle cx="560" cy="530" r="20" fill="{SUN}" stroke="{NAVY}" stroke-width="4"/>'
    for i in range(9):
        t=i/8; x=596+t*420; y=74+t*t*160; a=math.degrees(math.atan2(2*t*160/420*1,1))
        if i%2==0: b+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="26" ry="14" fill="none" stroke="{NAVY}" stroke-width="7" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
        else: b+=f'<rect x="{x-26:.0f}" y="{y-4:.0f}" width="52" height="8" rx="4" fill="{NAVY}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
    return b
def danforth():
    return (f'<rect x="146" y="20" width="18" height="140" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<rect x="80" y="150" width="150" height="14" rx="7" fill="{NAVY}"/><path d="M146 160 L96 70 L128 60 L150 150 Z M164 160 L214 70 L182 60 L160 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def cqr():
    return (f'<path d="M150 22 Q190 60 170 110" fill="none" stroke="{STEEL}" stroke-width="16" stroke-linecap="round"/><circle cx="148" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M170 100 L100 150 L150 150 L170 170 L190 150 L240 150 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
def rocna():
    return (f'<rect x="146" y="20" width="18" height="120" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            f'<path d="M70 120 Q155 190 240 120 L240 140 Q155 205 70 140 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="3"/><path d="M80 122 Q155 40 230 122" fill="none" stroke="{NAVY}" stroke-width="7"/>')
def grappino():
    s=f'<rect x="146" y="20" width="18" height="120" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/>'
    for dx,op in ((-1,1),(1,1),(-0.45,0.6),(0.45,0.6)):
        s+=f'<path d="M155 140 Q{155+dx*60:.0f} 150 {155+dx*70:.0f} 100" fill="none" stroke="{NAVY}" stroke-opacity="{op}" stroke-width="10" stroke-linecap="round"/>'
    return s
def ombrello():
    s=f'<rect x="146" y="20" width="18" height="130" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="3"/><circle cx="155" cy="22" r="12" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="155" cy="140" r="9" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    for a in (-60,-25,25,60):
        x2,y2=155+80*math.sin(math.radians(a)),140-60*math.cos(math.radians(a))*-1
        s+=f'<path d="M155 140 L{x2:.0f} {y2-110:.0f}" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>'
