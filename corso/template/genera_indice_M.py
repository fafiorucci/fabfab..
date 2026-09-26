"""Indice del corso: appendice M nella slide delle appendici (G–M), copertina, riepilogo e sezioni.
Lavora sulla copia scaricata del deck dell'indice in deck/project (accanto a questo file)."""
import os, sys, json
SP=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,SP)
from template import *
ORANGE='#F28C28'
P=SP+'/deck/project'
def section(i, n, inner, notes='', dark=False, gap=32):
    bg = NAVY if dark else PAPER; col = PAPER if dark else BODY
    return (f'<section id="{i}" data-transition="fade" style="background:{bg}; color:{col}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">\n{backdrop(dark,n)}\n{inner}\n{footer(n,dark)}\n'
            + (f'<aside>{notes}</aside>\n' if notes else '') + '</section>\n')
APP=[('G','La normativa in tabelle',30,'Documenti, dotazioni, limiti, velocità e sanzioni a colpo d\'occhio',CORAL,'1rxQdsHj5KsKWbzfQywxYK'),
     ('H','La radio VHF',26,'Canali, procedure, Mayday, Pan Pan e Sécurité, DSC',SEA,'5Cb5LD8J7BgGSoBQfL3SLm'),
     ('I','Navigare sottocosta',22,'Allineamenti, rilevamenti, fari e fanali, rotte sicure vicino a terra',PURPLE,'CL3ifXqfGFmb7rLVtJCVTL'),
     ('J','I bollettini meteo',21,'Leggere il bollettino, scala Beaufort e Douglas, decidere se uscire',BLUE,'8DuhyYgsfK2SzSiiPjWWU7'),
     ('K','Il soccorso in mare',23,'Chiamate di emergenza, segnali di soccorso, dotazioni e abbandono',GREEN,'RnDo7TYXGz52N73sXndC26'),
     ('L',"L'ancoraggio",22,'Tipi di ancora, fondali, calumo, manovra di dar fondo e salpare',ORANGE,'5N8Yqin6vPAdayCKswo4Ug'),
     ('M','La portanza',25,'Perché la vela spinge: pressioni, incidenza, stallo, filetti, fessura',CORAL,'Ap7Q1MUK6AqSZtf58LmStt')]
def cardA(L,t,n,d,c,u):
    return (f'<div style="display:flex; align-items:center; gap:20px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:16px 24px; {SHADOW}">'
            f'<p style="width:76px; height:76px; border-radius:38px; background:{c}; color:#FFFFFF; font-family:{H}; font-size:46px; font-weight:700; line-height:76px; text-align:center; flex:none">{L}</p>'
            f'<div style="flex:1; display:flex; flex-direction:column; gap:4px">{h3(t,32,c)}<p style="font-size:24px; line-height:1.3; color:{BODY}">{d}</p></div>'
            f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap; flex:none">{n} slide</p></div>')
notes='Le appendici si usano insieme alle lezioni, per ripassare e per esercitarsi. '+' '.join(f'Appendice {L}, {t}: https://claude.ai/artifact/{u}.' for L,t,n,d,c,u in APP)
inner=header('Appendici G–M · ripasso ed esercitazione','Sette appendici: dalle regole alla portanza','star',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px 22px">{"".join(cardA(*a) for a in APP)}</div>'
open(P+'/slides/appendici2.html','w').write(section('appendici2',25,inner,notes,gap=26))
def sub(f,pairs):
    s=open(f).read()
    for a,b in pairs:
        if b in s and a not in s: continue
        assert s.count(a)==1,(f,a); s=s.replace(a,b)
    open(f,'w').write(s)
sub(P+'/slides/appendici1.html',[('>Dodici appendici per studiare e allenarsi</h2>','>Sei appendici per studiare e allenarsi</h2>'),('>Tredici appendici per studiare e allenarsi</h2>','>Sei appendici per studiare e allenarsi</h2>')])
sub(P+'/slides/cover.html',[('15 lezioni da 2 ore e 12 appendici,','15 lezioni da 2 ore e 13 appendici,'),('<b>12</b> appendici','<b>13</b> appendici')])
sub(P+'/slides/prossimi.html',[('color:#7FD3DC">12</p>','color:#7FD3DC">13</p>'),('appendici di ripasso ed esercitazione (A–L)','appendici di ripasso ed esercitazione (A–M)'),
   ('ripassare (B, C, F, G, H, I, J, K, L) e','ripassare (B, C, F, G, H, I, J, K, L, M) e'),('12 appendici A–L,','13 appendici A–M,')])
d=json.load(open(P+'/deck.json'))
d['sections']['s4']['description']='Tredici appendici di ripasso ed esercitazione (A–M)'
json.dump(d,open(P+'/deck.json','w'),ensure_ascii=False,indent=1)
print('ok')
