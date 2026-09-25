"""Sintesi del corso per la scuola nautica: 5 slide con struttura, contenuti, materiali e punti di forza."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
ORDER=['cover','rotta','allievi','materiale','perche']
EB='Il corso per la vostra scuola'

# ============ COVER ============
cover(0,'Rotta verso la patente','Patente nautica Vela/Motore senza limiti dalla costa: un corso completo, pronto da usare in aula e in barca',
 'Presentazione del corso alla scuola nautica. In cinque slide: la struttura, cosa imparano gli allievi, il materiale pronto e i punti di forza.')
c=LB.slides[-1][1]
c=c.replace('Lezione 00 · 2 ore','Presentazione alla scuola nautica')
chip=lambda b,t: f'<p style="font-size:24px; color:#FFF8EE; background:rgba(245,241,232,0.10); padding:8px 16px; border-radius:40px"><b>{b}</b> {t}</p>'
chips=f'<div style="display:flex; gap:10px">{chip("30","ore")}{chip("15","lezioni")}{chip("12","appendici")}{chip("135","esercizi svolti")}{chip("1.000+","slide")}</div>'
k=c.index('</div>\n<p style="font-size:24px; font-weight:600'); c=c[:k]+chips+c[k:]
LB.slides[-1]=('cover',c)

# ============ LA ROTTA ============
W2,H2=1664,230
wp=[(277,140),(832,90),(1387,150),(1600,110)]
path=f'M40 170 C 150 150, 200 140, 277 140 S 640 60, 832 90 S 1200 190, 1387 150 S 1540 110, 1570 112'
g=(f'<path d="M0 205 '+' '.join('q26 -10 52 0 t52 0' for _ in range(16))+f'" fill="none" stroke="{SEA}" stroke-opacity="0.35" stroke-width="5" stroke-linecap="round"/>'
   f'<path d="{path}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-dasharray="14 12" stroke-linecap="round"/>')
cols=[CORAL,SEA,PURPLE]
for i,(x,y) in enumerate(wp[:3]):
    c_=cols[i]
    g+=f'<circle cx="{x}" cy="{y}" r="30" fill="{c_}"/><circle cx="{x}" cy="{y}" r="16" fill="#FFFFFF"/><circle cx="{x}" cy="{y}" r="8" fill="{c_}"/>'
# barca sul primo tratto
g+=(f'<g transform="translate(560 60)"><path d="M-46 22 L46 22 L34 40 L-34 40 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
    f'<path d="M-2 18 L-2 -62" stroke="{NAVY}" stroke-width="4"/><path d="M-6 -56 L-6 14 L-44 14 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M3 -48 L3 14 L36 14 Z" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/></g>')
# faro all'arrivo: l'esame
g+=tower(1600,190,1.35)+glow(1600,42,SUN,8)
lbls=(lab(128+277-120,290+H2-8,240,'Tappa 1',CORAL,24,900,'center')+lab(128+832-120,290+H2-8,240,'Tappa 2',SEA,24,900,'center')
      +lab(128+1387-120,290+H2-8,240,'Tappa 3',PURPLE,24,900,'center')+lab(128+1600-140,290+H2-8,280,'L\'esame',NAVY,24,900,'center'))
legs=[('Teoria e vela','Lezioni 1–9 · 18 ore','Scafo e motori, ormeggi e carte, ancoraggio, punto nave e fanali, segnalamento e sicurezza, meteo e normativa, vela ed emergenze.',CORAL),
      ('Carteggio','Lezioni 10–15 · 12 ore','Tutti i 135 esercizi d\'esame svolti passo per passo sulle carte 5/D e 42/D: costiera, carburante, scarroccio, correnti.',SEA),
      ('Verso l\'esame','12 appendici e schede','10 prove d\'esame simulate, la prova pratica in barca, ripasso mirato e schede riassuntive per lo studio a casa.',PURPLE)]
cards=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c_}; border-radius:28px; padding:28px 30px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
              f'{h3(t,38,c_)}<p style="font-size:24px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:{INK}">{s}</p>{p(d,28,BODY,400,1.4)}</div>' for t,s,d,c_ in legs)
sec('rotta',header(EB,'Il corso in una rotta: 30 ore, tre tappe','map',SEA)
    +f'<div style="height:{H2+40}px"></div>'+f'<div style="display:flex; gap:24px; align-items:stretch">{cards}</div>',
    pinned=svgp(128,272,W2,H2,g,'La rotta del corso: tre tappe segnate da boe, una barca a vela in navigazione e un faro all\'arrivo, l\'esame',pan=False)+lbls,
    notes='Il corso segue il programma d\'esame (DM 323/2021, Allegato A) in 15 lezioni da 2 ore. Prima la teoria e la vela, poi il carteggio con tutti gli esercizi ufficiali, infine il ripasso con le appendici, le prove simulate e le schede per gli allievi.',gap=32)

# ============ ALLIEVI ============
LEARN=[('hull','Conoscere la barca','Scafo, motori ed elica, timone, attrezzatura e vele: ogni parte con il suo nome e la sua funzione.',CORAL),
       ('compass','Navigare sicuri','Regole di rotta e precedenze, fanali, segnali sonori e segnalamento: sapere chi passa e dove.',SEA),
       ('dividers','Fare il carteggio','Punto nave, prora e rotta, carburante, scarroccio e correnti su carte 5/D e 42/D.',PURPLE),
       ('cloud','Leggere il tempo','Pressione, venti e brezze, fronti e nubi, onde e bollettini: decidere se e quando uscire.',BLUE),
       ('lifebuoy','Gestire l\'emergenza','Uomo a mare, falla, incendio, abbandono, radio VHF e MAYDAY: cosa fare, in quale ordine.',GREEN),
       ('helm','Comandare in barca','Manovre a motore e a vela, ormeggio e ancoraggio, nodi, documenti, dotazioni e responsabilità del comandante.',ORANGE)]
tiles_=''.join(f'<div style="display:flex; gap:20px; align-items:start; background:#FFFFFF; border-left:12px solid {c_}; border-radius:28px; padding:26px 28px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
               f'{badge(ic,c_,80)}<div style="display:flex; flex-direction:column; gap:8px">{h3(t,34,c_)}{p(d,25,BODY,400,1.4)}</div></div>' for ic,t,d,c_ in LEARN)
sec('allievi',header(EB,'Cosa sapranno fare gli allievi','star',CORAL)
    +f'<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:22px">{tiles_}</div>'
    +note('Non solo passare l\'esame: uscire in mare sapendo cosa fare.',CORAL,40),
    notes='Sei competenze, tutte legate ai temi d\'esame dell\'Allegato A al DM 323/2021 e alle esercitazioni pratiche dell\'Allegato D.',gap=30)

# ============ MATERIALE ============
hero=(f'<div style="width:560px; display:flex; flex-direction:column; gap:12px; background:{NAVY}; border-radius:36px; padding:44px 44px">'
      f'<p style="font-size:24px; font-weight:900; letter-spacing:2px; text-transform:uppercase; color:{DACC}">Tutto già pronto</p>'
      f'<p style="font-family:{H}; font-size:140px; font-weight:700; line-height:1; color:#FFFFFF">1.000+</p>'
      f'<p style="font-size:30px; line-height:1.35; font-weight:700; color:{DSOFT}">slide illustrate, pronte per l\'aula, con le note per l\'istruttore</p>'
      f'{squiggle(DACC,220)}'
      f'<p style="font-size:26px; line-height:1.4; color:{DSOFT}">Si proiettano così come sono, o si scaricano in PDF e PowerPoint.</p></div>')
MAT=[('15','lezioni da 2 ore','594 slide con disegni, schemi e quiz ufficiali con le risposte',CORAL),
     ('135','esercizi di carteggio','tutti svolti: traccia, soluzione e tracciamento sulla carta',SEA),
     ('12','appendici','364 slide: correnti, nomenclatura, nodi, IALA, normativa, VHF, costa, meteo, soccorso, ancoraggio',PURPLE),
     ('10','prove d\'esame simulate','complete di carteggio, quiz base e quiz vela, con le soluzioni',BLUE),
     ('1','prova pratica','le manovre in barca dell\'Allegato D, passo per passo',GREEN),
     ('15','schede per gli allievi','regole da memorizzare e numeri dei quiz, da stampare',ORANGE)]
mt=''.join(f'<div style="display:flex; align-items:center; gap:20px; background:#FFFFFF; border-left:12px solid {c_}; border-radius:24px; padding:12px 24px">'
           f'<p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c_}; width:104px; text-align:center">{n}</p>'
           f'<div style="flex:1; display:flex; flex-direction:column; gap:2px">{p(t,28,INK,800,1.2)}{p(d,24,BODY,400,1.3)}</div></div>' for n,t,d,c_ in MAT)
sec('materiale',header(EB,'Il materiale: un corso chiavi in mano','book',PURPLE)
    +f'<div style="display:flex; gap:32px; align-items:stretch">{hero}<div style="flex:1; display:flex; flex-direction:column; gap:12px">{mt}</div></div>',
    notes='Totale: 594 slide di lezione, 364 di appendici, 31 di schede riassuntive e 26 di indice del corso. Ogni deck si proietta dal browser e si scarica in PDF o PowerPoint.',gap=30)

# ============ PERCHÉ ============
WHY=[('Allineato all\'esame','Programma del DM 323/2021; quiz ed esercizi dall\'elenco ufficiale del DD 131/2022.'),
     ('Nessun esercizio lasciato indietro','135 esercizi di carteggio su 135, svolti e tracciati.'),
     ('Si impara guardando','Disegni originali in ogni lezione: barche, manovre, carte, luci e segnali.'),
     ('Verifica continua','Quiz ufficiali in ogni lezione, sempre seguiti dalla slide con le risposte.'),
     ('Aggiornato','Dotazioni di sicurezza secondo il DM 133/2024.'),
     ('Pronto per la scuola','Note per l\'istruttore, PDF e PowerPoint, schede da dare agli allievi.')]
wl=''.join(f'<div style="display:flex; gap:16px; align-items:start"><x-icon name="CheckCircle" style="color:{DACC}; width:40px; height:40px"></x-icon>'
           f'<div style="display:flex; flex-direction:column; gap:4px"><p style="font-size:30px; line-height:1.25; font-weight:800; color:#FFFFFF">{t}</p><p style="font-size:25px; line-height:1.35; color:{DSOFT}">{d}</p></div></div>' for t,d in WHY)
sig=(f'<div style="display:flex; align-items:center; gap:28px">{lockup(True,96)}'
     f'<p style="font-family:{HAND}; font-size:52px; font-weight:700; line-height:1.1; color:{DACC}">Pronti a salpare?</p></div>')
sec('perche',header(EB,'Perché scegliere questo corso','flag',CORAL,True)
    +f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:30px 60px">{wl}</div>'+sig,
    notes='Chiusura: il corso è tenuto da Fabrizio Fiorucci, skipper e istruttore di vela. Tutto il materiale è pronto e consultabile: indice del corso, lezioni, appendici e schede.',dark=True,gap=36)

write_deck(OUT,'Rotta verso la patente · Il corso in sintesi',ORDER,
 {"s1":{"description":"Presentazione del corso alla scuola nautica","start":"cover"},
  "s2":{"description":"Struttura, competenze, materiale e punti di forza","start":"rotta"}})
print('ok')
