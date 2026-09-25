"""Aggiorna l'indice del corso con le appendici A-L (slide appendici1, appendici2, prossimi, cover, deck.json).
Lavora sulla copia scaricata del deck dell'indice in deck/project (accanto a questo file)."""
import os, sys, json
SP=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,SP)
from template import *
def section(i, n, inner, notes='', dark=False, gap=32, pinned=''):
    bg = NAVY if dark else PAPER; col = PAPER if dark else BODY
    return (f'<section id="{i}" data-transition="fade" style="background:{bg}; color:{col}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">\n{backdrop(dark,n)}\n{inner}\n{pinned}{footer(n,dark)}\n'
            + (f'<aside>{notes}</aside>\n' if notes else '') + '</section>\n')
ORANGE='#F28C28'
P=SP+'/deck/project'
APP=[('A','I tre problemi della corrente',13,'Corrente nota, corrente da trovare, prora da tenere: il metodo passo per passo',CORAL,'1hFQPJ6uzwJTcUD3iL8kQr'),
     ('B','I nomi della barca a vela',26,'Scafo, attrezzatura, vele e manovre: ogni parte con il suo nome',SEA,'WNpiYhrUGGtCF1b8x3HwqV'),
     ('C','I nodi marinari',20,'I nodi del programma d\'esame, disegnati passo per passo',PURPLE,'SgD9AT2riGF8Qn3Y3nkBeE'),
     ('D',"Prove d'esame simulate",105,'Dieci prove complete: carteggio, quiz base e quiz vela, con soluzioni',BLUE,'Lc3nDQhbwaT9W7StE9dSjE'),
     ('E','La prova pratica',25,"Uscita in barca d'esame: manovre a motore e a vela, uomo a mare",GREEN,'Mzyami3LS4DrJEUr91yHVB'),
     ('F','Schede IALA',31,'Segnali laterali, cardinali, di pericolo isolato, acque sicure e speciali',ORANGE,'8r66WpwATcTvjUVVmMDkcF'),
     ('G','La normativa in tabelle',30,'Documenti, dotazioni, limiti, velocità e sanzioni a colpo d\'occhio',CORAL,'1rxQdsHj5KsKWbzfQywxYK'),
     ('H','La radio VHF',26,'Canali, procedure, Mayday, Pan Pan e Sécurité, DSC',SEA,'5Cb5LD8J7BgGSoBQfL3SLm'),
     ('I','Navigare sottocosta',22,'Allineamenti, rilevamenti, fari e fanali, rotte sicure vicino a terra',PURPLE,'CL3ifXqfGFmb7rLVtJCVTL'),
     ('J','I bollettini meteo',21,'Leggere il bollettino, scala Beaufort e Douglas, decidere se uscire',BLUE,'8DuhyYgsfK2SzSiiPjWWU7'),
     ('K','Il soccorso in mare',23,'Chiamate di emergenza, segnali di soccorso, dotazioni e abbandono',GREEN,'RnDo7TYXGz52N73sXndC26'),
     ('L',"L'ancoraggio",22,'Tipi di ancora, fondali, calumo, manovra di dar fondo e salpare',ORANGE,'5N8Yqin6vPAdayCKswo4Ug')]
def cardA(L,t,n,d,c,u):
    return (f'<div style="display:flex; align-items:center; gap:24px; background:#FFFFFF; border-left:12px solid {c}; border-radius:28px; padding:30px 28px; {SHADOW}">'
            f'<p style="width:96px; height:96px; border-radius:48px; background:{c}; color:#FFFFFF; font-family:{H}; font-size:60px; font-weight:700; line-height:96px; text-align:center; flex:none">{L}</p>'
            f'<div style="flex:1; display:flex; flex-direction:column; gap:6px">{h3(t,34,c)}<p style="font-size:26px; line-height:1.35; color:{BODY}">{d}</p></div>'
            f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap; flex:none">{n} slide</p></div>')
def notes(items): return ' '.join(f'Appendice {L}, {t}: https://claude.ai/artifact/{u}.' for L,t,n,d,c,u in items)
def appslide(sid,n,items,eb,title,icon):
    g=''.join(cardA(*a) for a in items)
    inner=header(eb,title,icon,SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:22px">{g}</div>'
    return section(sid,n,inner,'Le appendici si usano insieme alle lezioni, per ripassare e per esercitarsi. '+notes(items))
os.makedirs(P+'/slides',exist_ok=True)
open(P+'/slides/appendici1.html','w').write(appslide('appendici1',24,APP[:6],'Appendici A–F · ripasso ed esercitazione','Dodici appendici per studiare e allenarsi','book'))
open(P+'/slides/appendici2.html','w').write(appslide('appendici2',25,APP[6:],'Appendici G–L · ripasso ed esercitazione','Tabelle, radio, costa, meteo, soccorso, ancora','star'))
# prossimi -> materiali pronti
nums=[('15','lezioni da 2 ore: 9 di teoria e vela, 6 di carteggio',DACC),('12','appendici di ripasso ed esercitazione (A–L)','#7FD3DC'),
      ('10',"prove d'esame simulate complete, con soluzioni",'#FFB39C'),('135',"esercizi di carteggio del DD 131/2022, tutti svolti",'#B9F0C9')]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#1F4466; border-top:10px solid {c}; border-radius:28px; padding:28px 30px"><p style="font-family:{H}; font-size:96px; font-weight:700; line-height:1; color:{c}">{n}</p><p style="font-size:28px; line-height:1.35; font-weight:700; color:#FFFFFF">{d}</p></div>' for n,d,c in nums)
uso=('<ul style="font-size:28px; line-height:1.45; color:#C9D6E3; display:flex; flex-direction:column; gap:12px; width:1600px">'
     '<li>A lezione: le slide della lezione, con disegni, schemi e quiz ufficiali con le risposte</li>'
     '<li>A casa: le appendici per ripassare (B, C, F, G, H, I, J, K, L) e per esercitarsi (A, D)</li>'
     "<li>Prima dell'esame: le 10 prove simulate dell'appendice D e la prova pratica dell'appendice E</li></ul>")
inner=header('Materiali del corso',"Tutto pronto: dall'indice all'esame",'flag',None,True)+f'<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:22px">{g}</div>'+uso
open(P+'/slides/prossimi.html','w').write(section('prossimi',26,inner,'Riepilogo dei materiali pronti: 15 lezioni, 12 appendici A–L, 10 prove simulate, 135 esercizi di carteggio.',dark=True))
# cover
c=open(P+'/slides/cover.html').read()
chip='<p style="font-size:28px; color:#FFF8EE; background:rgba(245,241,232,0.10); padding:10px 22px; border-radius:40px"><b>135</b> esercizi d\'esame</p>'
assert chip in c
if '12</b> appendici' not in c:
    c=c.replace(chip,chip+chip.replace('<b>135</b> esercizi d\'esame','<b>12</b> appendici'))
    c=c.replace('<div style="display:flex; gap:24px"><p style="font-size:28px;','<div style="display:flex; gap:14px"><p style="font-size:28px;')
    c=c.replace('font-size:28px; color:#FFF8EE; background:rgba(245,241,232,0.10); padding:10px 22px','font-size:25px; color:#FFF8EE; background:rgba(245,241,232,0.10); padding:10px 18px')
    c=c.replace('Indice del corso: 15 lezioni da 2 ore, allineate al programma ministeriale','Indice del corso: 15 lezioni da 2 ore e 12 appendici, allineate al programma ministeriale')
open(P+'/slides/cover.html','w').write(c)
d=json.load(open(P+'/deck.json'))
o=[x for x in d['order'] if x not in('appendici1','appendici2')]
k=o.index('prossimi'); d['order']=o[:k]+['appendici1','appendici2']+o[k:]
d['sections']['s4']={'description':"Dodici appendici di ripasso ed esercitazione (A–L)",'start':'appendici1'}
d['sections']['s5']={'description':'Riepilogo dei materiali del corso','start':'prossimi'}
json.dump(d,open(P+'/deck.json','w'),ensure_ascii=False,indent=1)
print(len(d['order']))
