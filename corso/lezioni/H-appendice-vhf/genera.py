"""Appendice H: la radio VHF di bordo (quiz 1.3.9, 1.6.2, 1.3.3, 1.3.7, 1.3.8 e procedure radio)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/deck/project'
GREY='#97A6B4'; LRED='#E23B3B'; ORANGE='#F28C28'; LAND='#F2E2B3'; LAND_S='#C9A96B'; LCD='#BFE6D9'; KEY='#2B4A6B'

ORDER=['cover','indice','apparato','titoli','canali','portata','silenzio','quizA','quizAr',
       'parlare','parole','alfabeto','livelli','mayday','panpan','ricevi','quizB','quizBr',
       'dsc','senzaradio','meteomar','quizC','quizCr','eser','eserr','chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
EB='Appendice H · La radio VHF'
LB.ICON_T.update({'Indice':'book','L\'apparato VHF':'lantern','Chi può usare la radio':'check','I canali da sapere':'lantern',
 'Fin dove arriva la voce':'wind','Il silenzio radio':'lantern','Una chiamata normale':'lantern','Le parole della radio':'book',
 'L\'alfabeto fonetico':'book','MAYDAY, PAN PAN, SÉCURITÉ':'flag','Il MAYDAY parola per parola':'lifebuoy',
 'Il PAN PAN e il SÉCURITÉ':'flag','Se senti un MAYDAY':'lifebuoy','Il DSC: il pulsante rosso':'lantern',
 'Chiedere aiuto in altri modi':'lifebuoy','Il Meteomar alla radio':'cloud','Esercitazione: quale chiamata?':'star','Esercitazione: le chiamate':'check'})
X,Y,W,Hh=700,290,1092,620

def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=20,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=20: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
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
def script(title,lines,w=None,bg=NAVY):
    ww=f' width:{w}px;' if w else ' flex:1;'
    out=f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:30px 34px; border-radius:32px;{ww}"><p style="font-size:24px; font-weight:900; letter-spacing:1px; color:{DACC}">{title}</p>'
    for t,kind in lines:
        c={'k':'#FFFFFF','n':DSOFT,'m':'#FFFFFF','e':'#9FB3C8'}[kind]; wgt={'k':900,'n':700,'m':800,'e':700}[kind]
        out+=f'<p style="font-size:28px; line-height:1.3; color:{c}; font-weight:{wgt}">{t}</p>'
    return out+'</div>'

# ============ COPERTINA ============
cover(0,'La radio VHF','Canali, portata, come si parla, l\'alfabeto fonetico, MAYDAY, PAN PAN e SÉCURITÉ, il DSC e il Meteomar',
 'Appendice H al corso. Ripasso della radio di bordo: i quiz ufficiali 1.3.9 (radiotelefonia), 1.6.2 (Meteomar), 1.3.3 (obbligo del VHF e dell\'EPIRB), 1.3.7 e 1.3.8 (soccorso, DSC), con le procedure radio di uso comune. I nomi delle barche e i nominativi negli esempi sono inventati.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice H · studio'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
IX=[('La radio a bordo','Apparato, titoli, canali, portata, silenzio',['apparato','titoli','canali','portata','silenzio','quizA','quizAr'],CORAL),
    ('Parlare alla radio','Chiamata normale, parole, alfabeto fonetico',['parlare','parole','alfabeto'],SEA),
    ('Soccorso, urgenza, sicurezza','MAYDAY, PAN PAN, SÉCURITÉ, chi ascolta',['livelli','mayday','panpan','ricevi','quizB','quizBr'],LRED),
    ('Il resto','DSC, EPIRB e segnali, Meteomar',['dsc','senzaradio','meteomar','quizC','quizCr'],PURPLE),
    ('Esercitazione','Tre situazioni, tre chiamate',['eser','eserr'],BLUE)]
cards=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:18px 24px">'
              f'<p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:64px">{i+1:02d}</p>'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:4px">{p(t,32,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div>'
              f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(ids[0])}–{N(ids[-1])}</p></div>' for i,(t,d,ids,c) in enumerate(IX))
sec('indice', head(EB,'Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:18px">{cards}</div>'
    +note('Da provare ad alta voce: la radio si impara parlando.',SEA,38),
 notes='Ripasso della radio, dalla lezione 9 e dalla lezione 7 (Meteomar). Consiglio per l\'aula: far leggere gli esempi ad alta voce, a coppie, uno fa la barca e l\'altro la stazione costiera.')

# ============ L'APPARATO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
b+=f'<rect x="40" y="150" width="740" height="330" rx="44" fill="{NAVY}"/><path d="M700 150 V40" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<rect x="80" y="190" width="330" height="170" rx="18" fill="{LCD}"/>'
b+=''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{KEY}"/>' for x in range(450,560,24) for y in range(200,350,24))
for i,t in enumerate(('16/9','H/L','SCAN')): b+=f'<rect x="{80+i*110}" y="390" width="96" height="56" rx="14" fill="{KEY}"/>'
b+=f'<circle cx="640" cy="230" r="42" fill="{KEY}" stroke="#FFFFFF" stroke-width="4"/><circle cx="640" cy="330" r="42" fill="{KEY}" stroke="#FFFFFF" stroke-width="4"/>'
b+=line(640,230,640,196,'#FFFFFF',6)+line(640,330,666,306,'#FFFFFF',6)
b+=f'<rect x="420" y="384" width="140" height="68" rx="12" fill="{LRED}"/><path d="M420 384 L560 384 L540 356 L440 356 Z" fill="#FFFFFF" fill-opacity="0.35" stroke="#FFFFFF" stroke-width="3"/>'
b+=f'<path d="M780 380 C860 380 840 500 900 500 C960 500 940 420 960 380" fill="none" stroke="{KEY}" stroke-width="10" stroke-linecap="round"/>'
b+=f'<rect x="920" y="180" width="110" height="210" rx="40" fill="{NAVY}"/><rect x="1024" y="240" width="18" height="80" rx="8" fill="{CORAL}"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{KEY}"/>' for x in (955,975,995) for y in (220,240,260))
NUMS=[(245,190,1,CORAL),(128,470,2,SEA),(238,470,3,SEA),(348,470,4,SEA),(490,470,5,LRED),(700,230,6,PURPLE),(700,330,7,PURPLE),(1060,280,8,CORAL)]
b+=''.join(num(x,y,n,c,20) for x,y,n,c in NUMS)
lbl=big(X+90,Y+200,310,'16',NAVY,110)+lab(X+80,Y+400,96,'16/9','#FFFFFF',22,900,'center')+lab(X+190,Y+400,96,'H/L','#FFFFFF',22,900,'center')+lab(X+300,Y+400,96,'SCAN','#FFFFFF',22,900,'center')
lbl+=lab(X+420,Y+404,140,'DISTRESS','#FFFFFF',22,900,'center')+lab(X+530,Y+216,60,'VOL',DSOFT,22,900,'right')+lab(X+530,Y+316,60,'SQL',DSOFT,22,900,'right')+lab(X+880,Y+140,200,'microfono',NAVY,24,900,'center')
txt=(item(1,CORAL,'Il canale','Sul display: lo cambi con la manopola o i tasti.')
     +item('2–4',SEA,'16/9, H/L, SCAN','Torna al 16; potenza alta o bassa (1 W); scansione dei canali.')
     +item(5,LRED,'DISTRESS','Il pulsante rosso del DSC, sotto uno sportellino.')
     +item('6–7',PURPLE,'Volume e squelch','Lo squelch toglie il fruscio di fondo.')
     +item(8,CORAL,'Il tasto del microfono','Premi per parlare, rilascia per ascoltare: o parli o senti.'))
sec('apparato', head('La radio a bordo','L\'apparato VHF'), pinned=svgp(X,Y,W,Hh,b,'Frontale di un VHF fisso con display sul canale 16, tasti 16/9, H/L e SCAN, pulsante rosso DISTRESS sotto lo sportellino, manopole di volume e squelch e microfono con il tasto laterale')+lbl+pcol(txt,532,16),
 notes='Quiz 1.3.9-27 (squelch: attenua il rumore di fondo), -22 (potenza ridotta di 1 watt a distanza ravvicinata), -3 (apparato fisso: basta che sia omologato), -5 (esonero dalle ispezioni ordinarie), 1.3.8-7 (DSC), 1.3.1-19 (principio d\'incendio alla radio: estintore a CO2). Un VHF fisso trasmette fino a 25 W; il portatile ha meno potenza e meno portata. Il VHF è in simplex: mentre si tiene premuto il tasto non si sente niente, quindi si parla corto e si dice «passo».')
X=700

# ============ TITOLI ============
sec('titoli', head('La radio a bordo','Chi può usare la radio',CORAL)+table(['Che cosa','Regola'],[34,66],[
  ('Il titolo','Certificato limitato di radiotelefonista per naviglio minore'),
  ('Natante','Usa il VHF con l\'indicativo di chiamata'),
  ('Imbarcazione e nave','Usano il VHF con il nominativo internazionale'),
  ('Apparato fisso','Basta che sia omologato; esonerato dalle ispezioni ordinarie'),
  ('Obbligo a bordo','Il VHF serve oltre le 6 miglia dalla costa'),
  ('Responsabile','Il comandante, per l\'uso corretto degli apparati')],CORAL,28)
  +note('Nominativo e MMSI si scrivono vicino alla radio: nel MAYDAY servono subito.',CORAL,36),
 notes='Quiz 1.3.9-1 (certificato limitato di radiotelefonista), -2 (indicativo di chiamata: natanti), -4 (nominativo internazionale: imbarcazioni e navi), -3 e -5 (omologazione, niente ispezioni ordinarie), 1.3.3-1 e -40 (VHF obbligatorio oltre 6 miglia), 1.3.9-23 (responsabilità del comandante). Il quiz 1.8.1-22 sulla licenza di esercizio (RTF) è oscurato. L\'MMSI è il numero di 9 cifre che identifica la stazione nelle chiamate digitali DSC e nell\'EPIRB.')

# ============ CANALI ============
CH=[('16','Soccorso, urgenza, sicurezza e prima chiamata · 156,8 MHz. Poi ci si sposta.',LRED),
    ('70','Solo digitale: le chiamate DSC. Non ci si parla.',PURPLE),
    ('68','Meteomar, trasmesso di continuo.',SEA),
    ('6 · 8 · 72 · 77','Tra barca e barca.',BLUE),
    ('13','Sicurezza della navigazione tra navi, da ponte a ponte.',GREEN),
    ('Gli altri','Porti e stazioni costiere: sul volume Radioservizi per la navigazione dell\'IIM.',ORANGE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:22px 26px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(d,26,INK,600,1.35)}</div>' for n,d,c in CH)
sec('canali', head('La radio a bordo','I canali da sapere',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px">{g}</div>',
 notes='Quiz 1.3.9-8 e -10 (canale 16, 156,8 MHz), -18 (il 16 solo per la prima chiamata), -21 (6, 8, 72, 77 tra barche), 1.6.2-17 (Meteomar sul 68 di continuo), -23 (orari e canali sui Radioservizi per la navigazione dell\'IIM), 1.3.8-7 (DSC). Il 70 e il 13 non sono nei quiz ma sono canali internazionali da conoscere: il 70 è riservato alle chiamate digitali, il 13 alle comunicazioni di sicurezza tra navi.')

# ============ PORTATA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EAF4F7"/>'
b+=f'<path d="M-100 700 Q546 330 1192 700 Z" fill="{WATER}" fill-opacity="0.45"/>'
b+=f'<path d="M0 560 Q60 470 140 470 L200 470 Q230 520 260 560 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=line(140,470,140,200,NAVY,6)+f'<circle cx="140" cy="196" r="10" fill="{CORAL}"/>'
b+=''.join(f'<path d="M{140+r*0.7:.0f} {196-r*0.7:.0f} A{r} {r} 0 0 1 {140+r:.0f} {196:.0f}" fill="none" stroke="{CORAL}" stroke-width="4" stroke-opacity="{0.9-i*0.25:.2f}"/>' for i,r in enumerate((30,55,80)))
b+=f'<g transform="rotate(-8 520 420)">'+profile(470,420,110)+line(520,380,520,330,NAVY,4)+'</g>'
b+=f'<g transform="rotate(10 900 470)">'+profile(850,470,110)+line(900,430,900,380,NAVY,4)+'</g>'
b+=dash(146,200,900,380,CORAL,4)+dash(522,332,902,382,SEA,4)
lbl=pill(X+30,Y+30,460,'stazione costiera: circa 40 miglia',CORAL)+pill(X+560,Y+250,360,'tra barche: 10–20 miglia',SEA)+lab(X+300,Y+30,560,'la curvatura della Terra ferma le onde',NAVY,24,800,'right')
txt=(item(1,CORAL,'In linea retta','Le onde VHF vanno come la luce: le antenne devono «vedersi» sopra l\'orizzonte.')
     +item(2,SEA,'Più alta, più lontano','L\'antenna in testa d\'albero arriva più lontano di un portatile in pozzetto.')
     +item(3,PURPLE,'La potenza','Alta 25 W per chiamare lontano; bassa 1 W quando l\'altro è vicino.'))
sec('portata', head('La radio a bordo','Fin dove arriva la voce')+col(txt), pinned=svgp(X,Y,W,Hh,b,'La superficie curva del mare con una stazione costiera su un promontorio e due barche: la stazione, con l\'antenna alta, raggiunge la barca più lontana; le due barche si parlano a distanza minore')+lbl,
 notes='Quiz 1.3.9-24 (le antenne devono stare sopra la linea dell\'orizzonte), -25 (tra unità 10-20 miglia), -26 (con le stazioni costiere circa 40 miglia), -22 (1 watt a distanza ravvicinata).')

# ============ SILENZIO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
cx_,cy_,R=546,320,250
b+=f'<circle cx="{cx_}" cy="{cy_}" r="{R}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="10"/>'
for a0 in (0,180):
    p0=pol(cx_,cy_,a0,R-10); p1=pol(cx_,cy_,a0+18,R-10)
    b+=f'<path d="M{cx_} {cy_} L{p0[0]:.1f} {p0[1]:.1f} A{R-10} {R-10} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{LRED}" fill-opacity="0.85"/>'
b+=''.join(line(*pol(cx_,cy_,a,R-10),*pol(cx_,cy_,a,R-(36 if a%90==0 else 22)),NAVY,6 if a%90==0 else 3) for a in range(0,360,30))
b+=line(cx_,cy_,*pol(cx_,cy_,0,R-70),NAVY,10)+line(cx_,cy_,*pol(cx_,cy_,9,R-40),CORAL,5)+f'<circle cx="{cx_}" cy="{cy_}" r="12" fill="{NAVY}"/>'
lbl=pill(X+cx_+70,Y+cy_-R-4,230,'minuti 00–03',LRED,24)+pill(X+cx_-310,Y+cy_+R-50,230,'minuti 30–33',LRED,24)
txt=(item(1,LRED,'Due volte l\'ora','Dal minuto 00 al 03 e dal 30 al 33 il canale 16 tace.')
     +item(2,SEA,'Solo soccorso','In quei minuti si trasmette solo per soccorso; tutti gli altri ascoltano.')
     +item(3,PURPLE,'Silenzio imposto','Durante un soccorso chi lo coordina ordina «SEELONCE MAYDAY»; quando finisce, «SEELONCE FEENEE».'))
sec('silenzio', head('La radio a bordo','Il silenzio radio',LRED), pinned=svgp(X,Y,W,Hh,b,'Quadrante d\'orologio con in rosso i minuti da 00 a 03 e da 30 a 33, riservati al silenzio radio sul canale 16')+lbl+pcol(txt),
 notes='Quiz 1.3.9-17 e -29 (silenzio nei primi 3 minuti dell\'ora e della mezz\'ora), -20 (si impone con SILENCE MAYDAY, pronunciato «seelonce»). «Seelonce feenee» è la formula internazionale che annuncia la fine del silenzio.')
X=700

quiz_slide('quizA','Verifica · la radio a bordo',['1.3.9-10','1.3.9-26','1.3.9-29'],False)
quiz_slide('quizAr','Verifica · la radio a bordo',['1.3.9-10','1.3.9-26','1.3.9-29'],True)

# ============ UNA CHIAMATA NORMALE ============
def bubble(who,t,c,right=False):
    al='flex-end' if right else 'flex-start'; bg='#FFFFFF' if right else c; tc=INK if right else '#FFFFFF'
    return f'<div style="display:flex; flex-direction:column; align-items:{al}; gap:4px">{p(who,24,SOFT,800,1.2)}<p style="font-size:28px; font-weight:700; line-height:1.3; color:{tc}; background:{bg}; border:3px solid {c}; border-radius:24px; padding:12px 24px; max-width:1100px">{t}</p></div>'
DLG=[('Daphne · canale 16','«Stella Maris, Stella Maris, qui Daphne, Daphne. Passo.»',False),
     ('Stella Maris · canale 16','«Daphne, qui Stella Maris. Passiamo al 72. Passo.»',True),
     ('Daphne · canale 16','«Al 72. Passo.»',False),
     ('Daphne · canale 72','«Stella Maris, qui Daphne. Arriviamo in rada tra un\'ora, ci teniamo un posto vicino a voi? Passo.»',False),
     ('Stella Maris · canale 72','«Ricevuto. Vi aspettiamo. Chiudo.»',True)]
sec('parlare', head('Parlare alla radio','Una chiamata normale',SEA)+f'<div style="display:flex; flex-direction:column; gap:10px">{"".join(bubble(w,t,SEA,r) for w,t,r in DLG)}</div>'
    +note('Sul 16 solo il contatto: il resto su un canale di lavoro.',SEA,36),
 notes='Quiz 1.3.9-18 (il 16 solo per la prima chiamata), -21 (6, 8, 72, 77 tra barche). Schema: nome di chi si chiama (fino a tre volte), «qui», il proprio nome, «passo». Si ascolta prima di trasmettere per non coprire altre comunicazioni. I nomi sono inventati.')

sec('parole', head('Parlare alla radio','Le parole della radio',SEA)+table(['Parola','Che cosa vuol dire'],[34,66],[
  ('Passo','Ho finito, ora parli tu'),
  ('Chiudo','La comunicazione è finita, non aspetto risposta'),
  ('Ricevuto','Ho capito il messaggio'),
  ('Ripeti','Non ho capito, ripeti'),
  ('Qui','Prima del proprio nome: «qui Daphne»'),
  ('SEELONCE MAYDAY','Silenzio: c\'è un soccorso in corso'),
  ('SEELONCE FEENEE','Il silenzio è finito, il canale torna libero'),
  ('MAYDAY RELAY','Rilancio il MAYDAY di un\'altra unità')],SEA,26),
 notes='Quiz 1.3.9-20 (SILENCE MAYDAY, pronunciato «seelonce»), -11 (chi riceve un soccorso lo rilancia). Le altre sono le parole di procedura di uso comune in italiano; in inglese «over» e «out». Mai «passo e chiudo» insieme: o si aspetta la risposta o si chiude.')

AL=[('A','Alfa'),('B','Bravo'),('C','Charlie'),('D','Delta'),('E','Echo'),('F','Foxtrot'),('G','Golf'),('H','Hotel'),('I','India'),('J','Juliett'),('K','Kilo'),('L','Lima'),('M','Mike'),
    ('N','November'),('O','Oscar'),('P','Papa'),('Q','Quebec'),('R','Romeo'),('S','Sierra'),('T','Tango'),('U','Uniform'),('V','Victor'),('W','Whiskey'),('X','X-ray'),('Y','Yankee'),('Z','Zulu')]
HU=[CORAL,SEA,PURPLE,BLUE,GREEN]
g=''.join(f'<div style="display:flex; align-items:center; gap:12px; background:#FFFFFF; border-left:8px solid {HU[i%5]}; border-radius:18px; padding:18px 18px"><p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{HU[i%5]}; width:44px">{l}</p>{p(w,30,INK,700,1.1)}</div>' for i,(l,w) in enumerate(AL))
sec('alfabeto', head('Parlare alla radio','L\'alfabeto fonetico',SEA)+f'<div style="display:grid; grid-template-columns:repeat(6,1fr); gap:12px">{g}</div>'
    +note('I numeri si dicono cifra per cifra: 42 → «quattro, due».',SEA,34),
 gap=24, notes='L\'alfabeto fonetico internazionale serve per compitare nomi, nominativi e posizioni senza equivoci: per esempio il nominativo IABC2 si dice «India Alfa Bravo Charlie Due». Il quiz 1.5.3-59 cita la lettera A (Alfa) in Morse per i segnali di acque sicure; la bandiera A (Alfa) indica un palombaro in immersione (1.4.2-14).')

# ============ MAYDAY, PAN PAN, SÉCURITÉ ============
LV=[('MAYDAY ×3','Soccorso','Pericolo grave e imminente per persone o unità: falla, incendio, uomo a mare',LRED,CORAL_T),
    ('PAN PAN ×3','Urgenza','Serve aiuto, ma il pericolo non è immediato: avaria al motore, ferito non grave',SUN,SUN_T),
    ('SÉCURITÉ ×3','Sicurezza','Avvisi per tutti: ostacolo alla deriva, burrasca in arrivo',SEA,SEA_T)]
g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; border-top:12px solid {c}; border-radius:28px; padding:30px"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1.05; color:{INK}">{k}</p>{tag(t,c if c!=SUN else "#9A6200")}{p(d,28,INK,600,1.4)}</div>' for k,t,d,c,bg in LV)
sec('livelli', head('Soccorso, urgenza, sicurezza','MAYDAY, PAN PAN, SÉCURITÉ',LRED)+f'<div style="display:flex; gap:24px; align-items:stretch">{g}</div>'
    +note('Tre volte la parola chiave, sempre: così nessuno può sbagliarsi.',LRED,36),
 notes='Quiz 1.3.9-12, -14, -16 (MAYDAY ripetuto tre volte), -13 (PAN PAN tre volte), -15 (SÉCURITÉ tre volte), 1.6.2-14 (gli avvisi di burrasca sono preceduti da SÉCURITÉ), 1.3.5-1 (falla irreparabile: MAYDAY). Tutte e tre si lanciano sul canale 16.')

MS=[('MAYDAY MAYDAY MAYDAY','k'),('Qui Daphne Daphne Daphne · nominativo IABC2','n'),('MAYDAY Daphne','k'),('Posizione 42°45′ N 010°15′ E','m'),
    ('Falla a prua, stiamo affondando','m'),('Chiediamo assistenza immediata','m'),('4 persone a bordo, saliamo sulla zattera','m'),('Passo','e')]
steps=[('1','Tre volte MAYDAY',LRED),('2','Chi sei: nome e nominativo',CORAL),('3','Dove sei: la posizione',PURPLE),('4','Che cosa succede',BLUE),('5','Che aiuto chiedi',SEA),('6','Quante persone, altre notizie',GREEN)]
st=''.join(f'<div style="display:flex; gap:14px; align-items:center">{dot(n,c)}{p(t,28,INK,800,1.25)}</div>' for n,t,c in steps)
sec('mayday', head('Soccorso, urgenza, sicurezza','Il MAYDAY parola per parola',LRED)+f'<div style="display:flex; gap:32px; align-items:start">{script("CANALE 16 · POTENZA ALTA",MS,860)}<div style="flex:1; display:flex; flex-direction:column; gap:16px">{st}</div></div>',
 notes='Esempio con nome, nominativo e posizione inventati. Quiz 1.3.9-19 (nell\'ordine: nominativo, posizione, tipo di pericolo), -12, -14, -16 (MAYDAY tre volte), -8 (canale 16). Si parla lentamente; se nessuno risponde si ripete a intervalli. Con un apparato DSC prima si preme il pulsante DISTRESS, poi si lancia il MAYDAY a voce sul 16.')

PP=[('PAN PAN PAN PAN PAN PAN','k'),('A tutte le stazioni, a tutte le stazioni, a tutte le stazioni','n'),('Qui Daphne Daphne Daphne · nominativo IABC2','n'),('Posizione 2 miglia a sud di Capo Ferro','m'),('Motore in avaria, scarrocciamo verso la costa','m'),('Chiediamo un rimorchio · Passo','e')]
SC=[('SÉCURITÉ SÉCURITÉ SÉCURITÉ','k'),('A tutte le stazioni, a tutte le stazioni, a tutte le stazioni','n'),('Qui Daphne Daphne Daphne','n'),('Tronco alla deriva in posizione 43°10′ N 010°05′ E','m'),('Pericolo per la navigazione','m'),('Chiudo','e')]
sec('panpan', head('Soccorso, urgenza, sicurezza','Il PAN PAN e il SÉCURITÉ',ORANGE)+f'<div style="display:flex; gap:28px; align-items:stretch">{script("URGENZA · CANALE 16",PP,None,"#5A3A00")}{script("SICUREZZA · CANALE 16",SC,None,"#0B4F58")}</div>',
 notes='Esempi inventati. Quiz 1.3.9-13 (PAN PAN tre volte), -15 (SÉCURITÉ tre volte), 1.6.2-14 e -21 (gli avvisi di burrasca: preceduti da SÉCURITÉ, con precedenza sugli altri messaggi meteo). Un avviso di sicurezza lungo si annuncia sul 16 e poi si legge su un canale di lavoro indicato nell\'annuncio.')

sec('ricevi', head('Soccorso, urgenza, sicurezza','Se senti un MAYDAY',LRED)+table(['Che cosa fare','Perché'],[42,58],[
  ('Ascolta e scrivi posizione e nome','Ti serviranno se devi rilanciare o intervenire'),
  ('Non occupare il canale 16','Deve rispondere la Guardia Costiera'),
  ('Se nessuno risponde, rilancia','MAYDAY RELAY ×3, poi il messaggio ricevuto'),
  ('Se puoi, vai ad aiutare','Il comandante deve prestare assistenza se non mette in pericolo la sua barca'),
  ('In porto o vicino','L\'Autorità marittima può chiederti di partecipare al soccorso')],LRED,28)
  +note('Non rispondere per curiosità: il canale serve a chi affonda.',LRED,36),
 notes='Quiz 1.3.9-11 (chi riceve rilancia e, se può, presta soccorso), 1.3.7-7 (soccorso marittimo), -8 (coordinamento: Comando generale delle Capitanerie di porto), -9 (unità in porto o vicine), -10 e 1.8.1-7…-10 (obbligo di assistenza e sanzioni). Il MAYDAY RELAY è la formula internazionale per ritrasmettere il soccorso di un\'altra unità.')

quiz_slide('quizB','Verifica · soccorso e procedure',['1.3.9-13','1.3.9-19','1.3.9-11'],False)
quiz_slide('quizBr','Verifica · soccorso e procedure',['1.3.9-13','1.3.9-19','1.3.9-11'],True)

# ============ DSC ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#EAF4F7"/><rect x="0" y="470" width="1092" height="150" fill="{WATER}" fill-opacity="0.4"/>'
b+=f'<path d="M760 470 L800 360 L1092 340 L1092 470 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'+line(930,350,930,120,NAVY,6)+f'<rect x="880" y="300" width="100" height="50" rx="8" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
b+=profile(80,470,230)+line(200,420,200,300,NAVY,5)+f'<circle cx="200" cy="296" r="9" fill="{LRED}"/>'
b+=profile(560,480,170)+line(650,440,650,360,NAVY,4)
for r in (60,110,160,210):
    b+=f'<path d="M{200+r*0.8:.0f} {296-r*0.6:.0f} A{r} {r} 0 0 1 {200+r*0.8:.0f} {296+r*0.6:.0f}" fill="none" stroke="{LRED}" stroke-width="5" stroke-opacity="{1-r/260:.2f}"/>'
b+=dash(210,290,650,360,PURPLE,4)+dash(210,290,930,130,PURPLE,4)
b+=f'<rect x="60" y="40" width="250" height="120" rx="20" fill="{NAVY}"/><rect x="110" y="72" width="150" height="60" rx="10" fill="{LRED}"/><path d="M110 72 L260 72 L240 48 L130 48 Z" fill="#FFFFFF" fill-opacity="0.35" stroke="#FFFFFF" stroke-width="3"/>'
lbl=lab(X+110,Y+86,150,'DISTRESS','#FFFFFF',22,900,'center')+pill(X+560,Y+300,240,'navi vicine',PURPLE)+pill(X+800,Y+60,280,'Guardia Costiera',PURPLE)+pill(X+330,Y+60,300,'canale 70 · MMSI + posizione',LRED)
txt=(item(1,LRED,'Apri lo sportellino e tieni premuto','Il pulsante DISTRESS per qualche secondo, finché la radio conferma.')
     +item(2,PURPLE,'Parte da solo','Sul canale 70: il tuo MMSI e la posizione del GPS, a navi e stazioni costiere.')
     +item(3,SEA,'Poi parla','La radio passa al 16: lancia il MAYDAY a voce e aspetta la risposta.'))
sec('dsc', head('Il resto','Il DSC: il pulsante rosso',PURPLE)+col(txt,520,22), pinned=svgp(X,Y,W,Hh,b,'Una barca in difficoltà preme il pulsante rosso DISTRESS: il segnale digitale sul canale 70 raggiunge una nave vicina e la stazione della Guardia Costiera a terra')+lbl,
 notes='Quiz 1.3.8-7 (DSC: invia automaticamente un segnale di soccorso, urgenza o sicurezza a navi vicine e centri di coordinamento). Il DSC funziona solo se la radio ha l\'MMSI programmato e il GPS collegato: senza GPS la posizione va inserita a mano. Con il DSC si fanno anche chiamate normali a una singola stazione.')

sec('senzaradio', head('Il resto','Chiedere aiuto in altri modi',PURPLE)+table(['Mezzo','Quando si usa'],[34,66],[
  ('EPIRB','Oltre 50 miglia è obbligatoria: via satellite manda il segnale di soccorso'),
  ('1530','Il numero di emergenza della Guardia Costiera, dal telefono'),
  ('CIRM','Centro Internazionale Radio Medico: un grave infortunio a bordo'),
  ('Razzo a paracadute','Se presumi una nave, un aereo o la costa: sale ad almeno 300 m'),
  ('Fuoco a mano','Se vedi le luci di una nave, di un aereo o della costa'),
  ('Boetta fumogena','Di giorno: fumo arancione'),
  ('Braccia','Alzale e abbassale lentamente, allargate')],PURPLE,26),
 notes='Quiz 1.3.3-22 e -34 (EPIRB oltre 50 miglia), 1.3.8-25 (1530), 1.3.2.113 (CIRM), 1.3.9-6 e -9 (razzi: se si presume la presenza di soccorritori; almeno 300 m), -7 (fuochi a mano: se si vedono le luci), 1.3.3-3 e -20 (boetta fumogena arancione, segnale diurno), 1.3.8-24 (braccia), 1.5.2-14 (anche un suono continuo con un apparecchio da nebbia è un segnale di pericolo). Il quiz 1.3.3-26 (EPIRB codificata con l\'MMSI) è oscurato.')

sec('meteomar', head('Il resto','Il Meteomar alla radio',SEA)+table(['Che cosa','Come funziona'],[32,68],[
  ('Dove si ascolta','Canale 68, trasmesso di continuo dalle stazioni radio costiere'),
  ('Chi lo prepara','Il Centro Nazionale di Meteorologia e Climatologia Aeronautica'),
  ('Che cosa contiene','Avvisi, situazione, previsione e tendenza per zona'),
  ('Validità','Emesso alle 12 UTC, vale fino alle 00 UTC del giorno dopo'),
  ('Tendenza','Vento e mare nelle 12 ore successive'),
  ('Avvisi di burrasca','Preceduti da SÉCURITÉ, con precedenza su tutto'),
  ('Orari e canali','Sul volume Radioservizi per la navigazione dell\'IIM')],SEA,26),
 notes='Quiz 1.6.2-17 (canale 68 di continuo), -20 (stazioni radio costiere), -1 (CNMCA), -16 (avvisi), -18 (validità), -19 e -22 (tendenza di 12 ore), -14 e -21 (avvisi di burrasca), -23 (Radioservizi per la navigazione). Il bollettino è letto in italiano e in inglese; la lezione 7 spiega le zone e la scala Beaufort.')

quiz_slide('quizC','Verifica · DSC, segnali, Meteomar',['1.3.3-34','1.6.2-17','1.3.9-7'],False)
quiz_slide('quizCr','Verifica · DSC, segnali, Meteomar',['1.3.3-34','1.6.2-17','1.3.9-7'],True)

# ============ ESERCITAZIONE ============
SCN=[('1','Siete in 3 a bordo, 5 miglia al largo. Una falla a poppa: l\'acqua sale e la pompa non basta.',LRED),
     ('2','Il motore si ferma a 2 miglia dalla costa. Il vento vi spinge piano verso gli scogli. Nessuno è ferito.',SUN),
     ('3','Navigando vedete un container che galleggia, semi affondato, in mezzo alla rotta dei traghetti.',SEA)]
g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:12px; background:#FFFFFF; border-top:12px solid {c}; border-radius:28px; padding:30px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1; color:{c if c!=SUN else "#9A6200"}">{n}</p>{p(t,30,INK,600,1.4)}</div>' for n,t,c in SCN)
sec('eser', head('Esercitazione','Esercitazione: quale chiamata?',BLUE)+f'<div style="display:flex; gap:24px; align-items:stretch">{g}</div>'
    +note('Per ognuna: quale parola chiave? Poi dite ad alta voce tutto il messaggio.',BLUE,36),
 notes='Si lavora a coppie: uno lancia la chiamata, l\'altro fa la Guardia Costiera e risponde. Inventare nome della barca, nominativo e posizione, e compitarli con l\'alfabeto fonetico.')
A1=[('MAYDAY ×3','k'),('Qui … ×3 · nominativo','n'),('Posizione · falla a poppa','m'),('3 persone · chiediamo aiuto','m'),('Passo','e')]
A2=[('PAN PAN ×3','k'),('A tutte le stazioni ×3','n'),('Qui … ×3 · posizione','n'),('Motore in avaria, scarrocciamo','m'),('Chiediamo rimorchio · Passo','e')]
A3=[('SÉCURITÉ ×3','k'),('A tutte le stazioni ×3','n'),('Qui … ×3','n'),('Container alla deriva in posizione …','m'),('Chiudo','e')]
sec('eserr', head('Esercitazione','Esercitazione: le chiamate',BLUE)+f'<div style="display:flex; gap:22px; align-items:stretch">{script("1 · SOCCORSO",A1,None,"#7A1E1E")}{script("2 · URGENZA",A2,None,"#5A3A00")}{script("3 · SICUREZZA",A3,None,"#0B4F58")}</div>',
 notes='1: la barca rischia di affondare, pericolo grave e imminente: MAYDAY (1.3.5-1). 2: serve aiuto ma nessuno è in pericolo immediato: PAN PAN; se gli scogli si avvicinano e non si riesce ad ancorare, diventa MAYDAY. 3: un pericolo per gli altri naviganti: SÉCURITÉ.')

closing(['Canale 16 · 156,8 MHz: soccorso e prima chiamata, poi si cambia canale',
         'Silenzio radio ai minuti 00–03 e 30–33',
         'MAYDAY, PAN PAN, SÉCURITÉ: sempre tre volte',
         'MAYDAY: chi sei, dove sei, che cosa succede, che aiuto serve, quanti siete',
         'Meteomar sul 68; EPIRB oltre 50 miglia; 1530 dal telefono'],
 'Buon vento, e passo!','Appendice H · La radio VHF')

write_deck(OUT,'Appendice H · La radio VHF',ORDER,
 {"s1":{"description":"Copertina, indice, apparato, titoli, canali, portata e silenzio","start":"cover"},
  "s2":{"description":"Parlare alla radio: chiamata, parole, alfabeto fonetico","start":"parlare"},
  "s3":{"description":"MAYDAY, PAN PAN, SÉCURITÉ e chi ascolta","start":"livelli"},
  "s4":{"description":"DSC, altri mezzi di soccorso, Meteomar","start":"dsc"},
  "s5":{"description":"Esercitazione e chiusura","start":"eser"}})
