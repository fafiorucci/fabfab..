"""Sintesi del corso per la scuola nautica: 5 slide con struttura, contenuti, materiali e punti di forza."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
ORDER=['cover','rotta','percorsi','velamotore','allievi','materiale','perche']
EB='Il corso per la vostra scuola'

# ============ COVER ============
cover(0,'Rotta verso la Patente Nautica da Diporto','Un corso completo, pronto da usare in aula e in barca',
 'Presentazione del corso alla scuola nautica. In sette slide: la struttura, i percorsi entro 12 miglia o senza limiti, vela e motore o solo motore, cosa imparano gli allievi, il materiale pronto e i punti di forza.')
c=LB.slides[-1][1]
c=c.replace('Lezione 00 · 2 ore','Il corso in sintesi')
t0=f'<h1 style="font-family:{H}; font-size:104px; font-weight:700; line-height:1.05; color:#FFFFFF">Rotta verso la Patente Nautica da Diporto</h1>'
assert t0 in c
c=c.replace(t0,f'<div style="display:flex; flex-direction:column; gap:4px"><p style="font-family:{H}; font-size:52px; font-weight:600; line-height:1.1; color:{DSOFT}">Rotta verso la</p>'
            f'<h1 style="font-family:{H}; font-size:84px; font-weight:700; line-height:1.02; color:#FFFFFF">Patente Nautica<br>da Diporto</h1></div>')
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
lbls=(lab(128+277-120,884,240,'Tappa 1',CORAL,24,900,'center')+lab(128+832-120,884,240,'Tappa 2',SEA,24,900,'center')
      +lab(128+1387-120,884,240,'Tappa 3',PURPLE,24,900,'center')+lab(128+1600-140,884,280,'L\'esame',NAVY,24,900,'center'))
legs=[('Teoria e vela','Lezioni 1–9 · 18 ore','Scafo e motori, ormeggi e carte, ancoraggio, punto nave e fanali, segnalamento e sicurezza, meteo e normativa, vela ed emergenze.',CORAL),
      ('Carteggio','Lezioni 10–15 · 12 ore','Tutti i 135 esercizi d\'esame svolti passo per passo sulle carte 5/D e 42/D: costiera, carburante, scarroccio, correnti.',SEA),
      ('Verso l\'esame','12 appendici e schede','10 prove d\'esame simulate, la prova pratica in barca, ripasso mirato e schede riassuntive per lo studio a casa.',PURPLE)]
cards=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c_}; border-radius:28px; padding:28px 30px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
              f'{h3(t,38,c_)}<p style="font-size:24px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:{INK}">{s}</p>{p(d,28,BODY,400,1.4)}</div>' for t,s,d,c_ in legs)
sec('rotta',header(EB,'Il corso in una rotta: 30 ore, tre tappe','map',SEA)
    +f'<div style="display:flex; gap:24px; align-items:stretch">{cards}</div>',
    pinned=svgp(128,660,W2,H2,g,'La rotta del corso: tre tappe segnate da boe, una barca a vela in navigazione e un faro all\'arrivo, l\'esame',pan=False)+lbls,
    notes='Il corso segue il programma d\'esame (DM 323/2021, Allegato A) in 15 lezioni da 2 ore. Prima la teoria e la vela, poi il carteggio con tutti gli esercizi ufficiali, infine il ripasso con le appendici, le prove simulate e le schede per gli allievi.',gap=32)


# ============ PERCORSI: 12 MIGLIA O SENZA LIMITI ============
def sailboat(x,y,s,sail):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-46 22 L46 22 L34 40 L-34 40 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
            f'<path d="M-2 18 L-2 -62" stroke="{NAVY}" stroke-width="4"/><path d="M-6 -56 L-6 14 L-44 14 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><path d="M3 -48 L3 14 L36 14 Z" fill="{sail}" stroke="{NAVY}" stroke-width="3"/></g>')
W3,H3=1664,120
d=(f'<path d="M0 96 '+' '.join('q26 -9 52 0 t52 0' for _ in range(16))+f'" fill="none" stroke="{SEA}" stroke-opacity="0.4" stroke-width="5" stroke-linecap="round"/>'
   f'<path d="M0 120 L0 30 Q60 22 110 48 Q150 70 170 120 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
   +tower(70,60,0.5)+glow(70,6,SUN,5)
   +f'<path d="M760 4 L760 116" stroke="{NAVY}" stroke-width="4" stroke-dasharray="12 10"/>'
   +sailboat(430,58,0.8,SEA)+sailboat(1250,58,0.8,CORAL)
   +arrow(1330,74,1600,74,CORAL,4,16))
lbl3=(lab(128+780,262,300,'12 miglia dalla costa',NAVY,24,900)+lab(128+1360,262,300,'senza limiti',CORAL,24,900))
def route(title,sub,rows,aula,c_):
    tb=table(['Prova','Quesiti','Tempo','Errori'],[44,20,16,20],rows,c_,24)
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:12px; background:#FFFFFF; border-top:10px solid {c_}; border-radius:28px; padding:24px 28px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
            f'<div style="display:flex; align-items:center; gap:16px">{h3(title,38,c_)}<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c_}; padding:4px 14px; border-radius:14px">{sub}</p></div>'
            f'{tb}{p(aula,25,BODY,400,1.35)}</div>')
R12=route('Entro 12 miglia','Lezioni 1–9 · 18 ore',[('Quiz di carteggio','5','15′','max 1'),('Quiz base','20','30′','max 4'),('Quiz vela (solo vela)','5','15′','max 1')],
          '<b>In aula</b>: teoria, vela ed elementi di carteggio. Prova pratica in mare o in lago.',SEA)
RSL=route('Senza limiti','Lezioni 1–15 · 30 ore',[('Prova di carteggio','4 esercizi','60′','max 1'),('Quiz base','20','30′','max 4'),('Quiz vela (solo vela)','5','15′','max 1')],
          '<b>In più</b>: tutto il carteggio su 5/D e 42/D, 135 esercizi svolti e 10 prove simulate. Prova pratica in mare.',CORAL)
banner=(f'<div style="display:flex; align-items:center; gap:18px; background:{NAVY}; border-radius:24px; padding:16px 28px">'
        f'<p style="font-family:{HAND}; font-size:40px; font-weight:700; line-height:1; color:{DACC}; white-space:nowrap">Hai già la 12 miglia?</p>'
        f'<p style="font-size:26px; line-height:1.3; font-weight:700; color:#FFFFFF">Niente quiz base: solo carteggio (e quiz vela per la vela), con le lezioni 10–15.</p></div>')
sec('percorsi',header(EB,'Due patenti, due rotte','compass',BLUE)+svgi(W3,H3,d,'Dalla costa al largo: una barca naviga entro la linea delle 12 miglia, un\'altra la supera verso il mare aperto',pan=False)
    +f'<div style="display:flex; gap:24px; align-items:stretch">{R12}{RSL}</div>'+banner,
    pinned=lbl3,
    notes='Prove d\'esame secondo l\'art. 6 del DM 323/2021 (tabella riportata nel manuale dei quiz). Entro 12 miglia: 5 quiz su elementi di carteggio in 15 minuti con al massimo 1 errore, 20 quiz base in 30 minuti con al massimo 4 errori, per la vela 5 quiz vela in 15 minuti con al massimo 1 errore. Senza limiti: prova di carteggio con 4 esercizi in 60 minuti con al massimo 1 errore, quiz base solo per chi non ha già la patente entro 12 miglia, quiz vela per la vela. Prova pratica: entro 12 miglia in mare, in lago o in specchi acquei adeguati; senza limiti in mare.',gap=22)


# ============ VELA E MOTORE O SOLO MOTORE ============
def motorboat(x,y,s):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-120 0 L130 -8 Q138 18 108 34 L-110 36 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
            f'<path d="M-116 16 L126 10" stroke="{ORANGE}" stroke-width="8"/><path d="M-50 -2 L60 -6 L36 -46 L-30 -46 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
            f'<path d="M-20 -38 L28 -38 L40 -16 L-24 -14 Z" fill="{BLUE}" fill-opacity="0.8"/></g>')
W4,H4=1664,120
wake=lambda x: ''.join(f'<path d="M{x-150-j*40} {88+j*8} q20 -8 40 0" fill="none" stroke="{SEA}" stroke-width="4" stroke-linecap="round" stroke-opacity="{0.7-j*0.2}"/>' for j in range(3))
d4=(f'<path d="M0 100 '+' '.join('q26 -9 52 0 t52 0' for _ in range(16))+f'" fill="none" stroke="{SEA}" stroke-opacity="0.4" stroke-width="5" stroke-linecap="round"/>'
    +wake(420)+motorboat(420,70,0.62)+sailboat(1240,58,0.8,SEA)+motorboat(1450,74,0.36))
lbl4=(lab(128+560,268,300,'solo motore',ORANGE,24,900)+lab(128+1520,268,200,'vela e motore',SEA,24,900))
def rowsbox(title,sub,rows,c_):
    g=''.join(f'<p style="font-size:28px; line-height:1.3; font-weight:900; color:{c_}">{a}</p><p style="font-size:28px; line-height:1.35; color:{BODY}">{b}</p>' for a,b in rows)
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:22px; background:#FFFFFF; border-top:10px solid {c_}; border-radius:28px; padding:30px 32px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">'
            f'<div style="display:flex; align-items:center; gap:16px">{h3(title,38,c_)}<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c_}; padding:4px 14px; border-radius:14px">{sub}</p></div>'
            f'<div style="display:grid; grid-template-columns:150px 1fr; gap:22px 18px">{g}</div></div>')
MOT=rowsbox('Solo motore','abilita alle unità a motore',[
    ('Esame','Carteggio e quiz base. Niente quiz vela.'),
    ('Pratica','Manovre a motore: ormeggio e disormeggio, uomo a mare, nodi, strumenti.'),
    ('In aula','Tutte le lezioni tranne la 8 sulla vela: 2 ore in meno.')],ORANGE)
VEL=rowsbox('Vela e motore','abilita a vela, motore e mista',[
    ('Esame','In più 5 quiz vela: 15′, al massimo 1 errore.'),
    ('Pratica','Andature e manovre a vela, più tutto il programma a motore, con l\'istruttore di vela a bordo.'),
    ('In aula','Tutte le 15 lezioni, con la lezione 8 sulla vela e l\'appendice B sui nomi della barca a vela.')],SEA)
banner4=(f'<div style="display:flex; align-items:center; gap:18px; background:{NAVY}; border-radius:24px; padding:16px 28px">'
         f'<p style="font-family:{HAND}; font-size:40px; font-weight:700; line-height:1; color:{DACC}; white-space:nowrap">E se la vela non va?</p>'
         f'<p style="font-size:26px; line-height:1.3; font-weight:700; color:#FFFFFF">Chi non è idoneo alla prova a vela può optare per la patente a solo motore, con le manovre a motore.</p></div>')
sec('velamotore',header(EB,'Vela e motore, o solo motore','sail',SEA)+svgi(W4,H4,d4,'Un motoscafo con la sua scia e, più avanti, una barca a vela con un piccolo motoscafo',pan=False)
    +f'<div style="display:flex; gap:24px; align-items:stretch">{MOT}{VEL}</div>'+banner4,
    pinned=lbl4,
    notes='DM 323/2021, art. 6 e prova pratica (tabella e programma riportati nel manuale dei quiz). Solo motore: carteggio (quiz di carteggio entro 12 miglia, prova di carteggio senza limiti) e quiz base; prova pratica con le manovre a motore dell\'Allegato D. Vela e motore: in più 5 quiz vela in 15 minuti con al massimo 1 errore; la prova pratica su unità a vela include anche il programma a motore e a bordo c\'è l\'istruttore professionale di vela. Chi non è idoneo nella pratica a vela può optare per la patente a solo motore effettuando le manovre a motore; l\'opzione si annota nel verbale. Vale sia per la patente entro 12 miglia sia per quella senza limiti.',gap=22)

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
      f'<p style="font-family:{HAND}; font-size:46px; font-weight:700; line-height:1.1; color:{DACC}">Si accende il proiettore, e si salpa.</p></div>')
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
sig=f'<p style="font-family:{HAND}; font-size:64px; font-weight:700; line-height:1.1; color:{DACC}">Pronti a salpare?</p>'
sec('perche',header(EB,'Perché scegliere questo corso','flag',CORAL,True)
    +f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:30px 60px">{wl}</div>'+sig,
    notes='Chiusura: il corso è tenuto da Fabrizio Fiorucci, skipper e istruttore di vela. Tutto il materiale è pronto e consultabile: indice del corso, lezioni, appendici e schede.',dark=True,gap=36)

write_deck(OUT,'Rotta verso la patente · Il corso in sintesi',ORDER,
 {"s1":{"description":"Presentazione del corso alla scuola nautica","start":"cover"},
  "s2":{"description":"Struttura, competenze, materiale e punti di forza","start":"rotta"}})
print('ok')
