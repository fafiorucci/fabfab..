"""Indice del corso: slide «extra» con presentazione alla scuola e schede riassuntive; aggiorna prossimi e deck.json.
Lavora sulla copia scaricata del deck dell'indice in deck/project (accanto a questo file)."""
import os, sys, json
SP=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,SP)
from template import *
P=SP+'/deck/project'
def section(i, n, inner, notes='', dark=False, gap=32):
    bg = NAVY if dark else PAPER; col = PAPER if dark else BODY
    return (f'<section id="{i}" data-transition="fade" style="background:{bg}; color:{col}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">\n{backdrop(dark,n)}\n{inner}\n{footer(n,dark)}\n'
            + (f'<aside>{notes}</aside>\n' if notes else '') + '</section>\n')
X=[('flag',CORAL,'Presentazione alla scuola','7 slide','«Rotta verso la Patente Nautica da Diporto»: il corso in sintesi per la scuola nautica.',
    ['La struttura in tre tappe: teoria e vela, carteggio, verso l\'esame','Entro 12 miglia o senza limiti: prove e lezioni','Vela e motore o solo motore','Competenze, materiale e punti di forza'],'FxjVMj32rr5eymmibB5Eec'),
   ('book',SEA,'Schede riassuntive','31 slide','Addendum per lo studente: una o due pagine per ogni lezione, da stampare.',
    ['Le regole da memorizzare, lezione per lezione','I numeri che tornano nei quiz: distanze, velocità, dotazioni','Le formule del carteggio con gli esempi','I numeri d\'oro e due verifiche con quiz ufficiali'],'NEHjtWa3XgzS6NMc4K18vC')]
def card(ic,c,t,n,d,items,u):
    li=''.join(f'<li>{x}</li>' for x in items)
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:#FFFFFF; border-top:12px solid {c}; border-radius:32px; padding:32px 36px; {SHADOW}">'
            f'<div style="display:flex; align-items:center; gap:20px">{badge(ic,c,88)}<div style="flex:1; display:flex; flex-direction:column; gap:6px">{h3(t,40,c)}'
            f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; align-self:start">{n}</p></div></div>'
            f'<p style="font-size:28px; line-height:1.4; font-weight:700; color:{INK}">{d}</p>'
            f'<ul style="font-size:26px; line-height:1.4; color:{BODY}; display:flex; flex-direction:column; gap:8px">{li}</ul>'
            f'<p style="font-size:24px; font-weight:800; color:{c}"><a href="https://claude.ai/artifact/{u}"><span style="color:{c}">Apri il deck</span></a></p></div>')
inner=header('Per la scuola e per gli allievi','La presentazione del corso e le schede','star',PURPLE)+f'<div style="display:flex; gap:28px; align-items:stretch">{"".join(card(*x) for x in X)}</div>'
open(P+'/slides/extra.html','w').write(section('extra',26,inner,'Due materiali in più. La presentazione alla scuola nautica: https://claude.ai/artifact/FxjVMj32rr5eymmibB5Eec. Le schede riassuntive per lo studente: https://claude.ai/artifact/NEHjtWa3XgzS6NMc4K18vC.'))
f=P+'/slides/prossimi.html'; s=open(f).read()
R=[('border-radius:20px">26<','border-radius:20px">27<'),
   ('<li>A casa: le appendici per ripassare (B, C, F, G, H, I, J, K, L) e per esercitarsi (A, D)</li>','<li>A casa: le appendici per ripassare (B, C, F, G, H, I, J, K, L) e per esercitarsi (A, D), con le schede riassuntive</li>'),
   ('<li>Prima dell\'esame: le 10 prove simulate dell\'appendice D e la prova pratica dell\'appendice E</li></ul>','<li>Prima dell\'esame: le 10 prove simulate dell\'appendice D e la prova pratica dell\'appendice E</li><li>Per presentare il corso: la sintesi in 7 slide per la scuola nautica</li></ul>'),
   ('Riepilogo dei materiali pronti: 15 lezioni, 12 appendici A–L, 10 prove simulate, 135 esercizi di carteggio.','Riepilogo dei materiali pronti: 15 lezioni, 12 appendici A–L, 10 prove simulate, 135 esercizi di carteggio, le schede riassuntive e la presentazione alla scuola.')]
for a,b in R:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(f,'w').write(s)
d=json.load(open(P+'/deck.json'))
if 'extra' not in d['order']:
    k=d['order'].index('prossimi'); d['order'].insert(k,'extra')
d['sections']['s5']={'description':'Presentazione alla scuola e schede riassuntive per gli allievi','start':'extra'}
d['sections']['s6']={'description':'Riepilogo dei materiali del corso','start':'prossimi'}
json.dump(d,open(P+'/deck.json','w'),ensure_ascii=False,indent=1)
print(len(d['order']))
