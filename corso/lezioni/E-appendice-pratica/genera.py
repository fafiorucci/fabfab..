"""Appendice E: la prova pratica di manovra (All. A e All. D al DM 323/2021)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/deck/project'
GREY='#97A6B4'; ORANGE='#F28C28'; QUAY='#D9C9A8'; SEABED='#C9A96B'; SKY='#DDEFF7'

ORDER=['cover','indice','prova','prima','evolutivo','disormeggio','ormeggio','inglese','ancora','salpare','quiz1','quiz1r',
       'uomomotore','uomovela','andature','virata','bussola','cattivo','quiz2','quiz2r','nodi','dotazioni','errori','giorno','chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
EB='Appendice E · La prova pratica'
LB.ICON_T.update({'Indice':'book','Com\'è la prova pratica':'flag','Prima di mollare gli ormeggi':'check','Elica e timone in manovra':'propeller',
 'Disormeggio di poppa':'anchor','Ormeggio di poppa':'anchor','Ormeggio all\'inglese':'anchor','Ancoraggio a motore':'anchor','Salpare l\'ancora':'anchor',
 'Uomo a mare a motore':'lifebuoy','Uomo a mare a vela':'lifebuoy','Le andature':'sail','Virata e abbattuta a voce':'wind','Bussola e strumenti':'compass',
 'Arriva il cattivo tempo':'cloud','I quattro nodi della prova':'helm','Le dotazioni di sicurezza':'lifebuoy','Gli errori più comuni':'star','Il giorno della prova':'check'})

# ---------- strumenti ----------
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF'):
    return lab(x,y,w,t,tc,size,900,'left',bg=c).replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def bollard(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{NAVY}"/><circle cx="{x}" cy="{y}" r="{r*0.4:.0f}" fill="{SUN}"/>'
def rope(d,c=NAVY,w=6):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="{max(1.5,w/3):.1f}" stroke-dasharray="3 6" stroke-linecap="round"/>'
def dot(n,c): return f'<p style="width:44px; height:44px; border-radius:22px; background:{c}; color:#FFFFFF; font-weight:900; font-size:22px; text-align:center; line-height:44px; flex:none">{n}</p>'
def item(n,c,t,d): return f'<div style="display:flex; gap:16px; align-items:start">{dot(n,c)}<div style="display:flex; flex-direction:column; gap:4px">{p(t,28,INK,800,1.25)}{p(d,24,BODY)}</div></div>'
def windarrow(x,y,l=80,c=GREY,ang=90):
    a=math.radians(ang); return arrow(x,y,x+l*math.cos(a),y+l*math.sin(a),c,8,26)
def person(x,y,c=CORAL,s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-16" r="11" fill="#F2C9A0" stroke="{NAVY}" stroke-width="2"/><path d="M-14 -4 Q0 -10 14 -4 L12 16 L-12 16 Z" fill="{c}"/></g>'
def ring(x,y,r=22): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ORANGE}" stroke-width="{r*0.55:.0f}"/><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.55:.0f}" stroke-dasharray="{r*0.8:.0f} {r*0.8:.0f}"/>'
def wash(cx,cy,ang,n=3,c=SEA):
    a=math.radians(ang); s=''
    for i in range(n):
        d=26+i*22; x=cx+d*math.cos(a); y=cy+d*math.sin(a); r=10+i*5
        s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="3" stroke-opacity="{0.8-i*0.2:.1f}"/>'
    return s
def tile(t,d,c,pic=None):
    top=f'<div style="display:flex; justify-content:center; background:{PAPER}; border-radius:18px; padding:8px">{pic}</div>' if pic else squiggle(c,110)
    return f'<div style="flex:1; display:flex; flex-direction:column; gap:12px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:24px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{top}{h3(t,32,c)}{d}</div>'
pic=lambda body,alt: svgi(300,170,body,alt,dw=300,dh=170,pan=False)
# ---- pittogrammi ----
def rp(d,c=CORAL,w=12): return rope(d,c,w)
PIC={
 'gassa': rp('M40 130 L150 130 Q170 130 175 110 Q180 60 150 40 Q120 20 95 50 Q80 75 110 100 Q135 118 175 110')+rp('M175 110 L260 110',CORAL)+f'<circle cx="170" cy="112" r="16" fill="none" stroke="{NAVY}" stroke-width="5"/>',
 'parlato': line(20,40,280,40,GREY,8)+''.join(rope(f'M{x} 26 L{x+14} 56',SEA,11) for x in (120,142))+rope('M150 56 L150 90',SEA,8)+f'<rect x="118" y="90" width="64" height="74" rx="30" fill="{BLUE}" stroke="{NAVY}" stroke-width="4"/>',
 'bitta': f'<rect x="130" y="56" width="40" height="60" rx="8" fill="{NAVY}"/><rect x="60" y="72" width="180" height="28" rx="14" fill="{NAVY}"/>'+rp('M20 160 L96 104 Q60 80 96 64 L204 108 Q240 92 204 64 L96 108',PURPLE,10),
 'bozza': rope('M10 90 L290 90',NAVY,12)+''.join(rope(f'M{x} 60 L{x+18} 120',BLUE,9) for x in (100,124,148))+rope('M166 118 L260 150',BLUE,9)+arrow(270,90,295,90,CORAL,4,14),
 'anulare': ring(150,86,52)+rope('M202 86 Q250 100 280 150',ORANGE,6),
 'fuoco': f'<rect x="126" y="70" width="48" height="96" rx="10" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/><path d="M150 66 Q120 40 140 10 Q150 30 160 22 Q180 40 150 66 Z" fill="{SUN}"/><circle cx="110" cy="30" r="14" fill="{GREY}" fill-opacity="0.5"/><circle cx="90" cy="14" r="10" fill="{GREY}" fill-opacity="0.35"/>',
 'estintore': f'<rect x="120" y="50" width="60" height="112" rx="24" fill="{CORAL}" stroke="{NAVY}" stroke-width="4"/><rect x="138" y="28" width="24" height="24" fill="{NAVY}"/><path d="M162 36 L210 36 L230 60" fill="none" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/><rect x="132" y="90" width="36" height="30" rx="6" fill="#FFFFFF"/>',
 'kit': f'<rect x="80" y="50" width="140" height="100" rx="16" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/><path d="M130 50 L130 34 L170 34 L170 50" fill="none" stroke="{NAVY}" stroke-width="5"/><path d="M140 72 L160 72 L160 90 L178 90 L178 110 L160 110 L160 128 L140 128 L140 110 L122 110 L122 90 L140 90 Z" fill="{GREEN}"/>',
}
ul=lambda xs,size=24: f'<ul style="font-size:{size}px; line-height:1.35; color:{BODY}; display:flex; flex-direction:column; gap:6px">'+''.join(f'<li>{x}</li>' for x in xs)+'</ul>'
X,Y,W,Hh=700,290,1092,620

# ============ COPERTINA ============
cover(0,'La prova pratica','Le manovre dell\'esame a bordo: ormeggi, ancoraggio, uomo a mare, andature, strumenti e cattivo tempo',
 'Appendice E al corso. Segue il programma della prova pratica dell\'All. A al DM 323/2021 e il programma delle esercitazioni dell\'All. D. Serve a ripassare prima delle uscite in barca e prima della prova.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice E · studio'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
IX=[('Prima della prova','La prova e i controlli prima di partire',['prova','prima'],CORAL),
    ('Manovre in porto','Elica e timone, ormeggi, ancoraggio',['evolutivo','disormeggio','ormeggio','inglese','ancora','salpare','quiz1','quiz1r'],SEA),
    ('In mare','Uomo a mare, andature, virate, strumenti, cattivo tempo',['uomomotore','uomovela','andature','virata','bussola','cattivo','quiz2','quiz2r'],PURPLE),
    ('Il giorno della prova','Nodi, dotazioni, errori, checklist',['nodi','dotazioni','errori','giorno'],BLUE)]
cards=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:20px 24px">'
              f'<p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:64px">{i+1:02d}</p>'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:4px">{p(t,32,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div>'
              f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(ids[0])}–{N(ids[-1])}</p></div>' for i,(t,d,ids,c) in enumerate(IX))
sec('indice', head(EB,'Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:20px">{cards}</div>'
    +note('Ogni manovra rimanda alla lezione in cui l\'abbiamo studiata.',SEA,38),
 notes='L\'appendice ripassa la prova pratica. Si usa prima delle uscite con l\'istruttore: si legge la slide, poi si fa la manovra in barca. Le quattro parti seguono l\'ordine di un\'uscita: si prepara la barca, si esce dal porto, si naviga, si rientra.')

# ============ COM'È LA PROVA ============
RG=[('Chi è ammesso','Chi ha fatto <b>almeno 5 ore di manovre</b> con una scuola nautica, sul programma dell\'All. D. La scuola le certifica.',CORAL),
    ('Quando','In una <b>giornata diversa</b> dalla prova scritta, con una <b>commissione diversa</b>. Si fa a bordo, a motore e a vela.',SEA),
    ('Che cosa','Andature su tratti di almeno ¼ di miglio, uomo in mare, ormeggio e disormeggio, dotazioni, preparativi per il cattivo tempo.',PURPLE),
    ('Se va male','Si ripete <b>solo la pratica</b>, dopo almeno 30 giorni. Chi non è idoneo a vela può scegliere la patente a solo motore.',BLUE)]
g=''.join(tile(t,p(d,28,BODY,400,1.45),c) for t,d,c in RG)
sec('prova', head(EB,'Com\'è la prova pratica',CORAL)+f'<div style="display:flex; gap:22px; align-items:stretch">{g}</div>'
    +note('L\'esaminatore guarda soprattutto una cosa: che tu comandi la barca con calma e in sicurezza.',CORAL,36),
 notes='DM 10 agosto 2021 n. 323: art. 3 c. 1 (prova scritta e prova pratica di manovra in giornate diverse e con commissioni diverse; ammissione con almeno cinque ore di manovre attestate da una scuola nautica, sul programma dell\'All. D); art. 3 cc. 2 e 3 (si ripete una volta, dopo almeno 30 giorni; chi ha superato lo scritto ripete solo la pratica); art. 7 c. 6 (non idoneo nella pratica a vela: può optare per la patente solo motore). All. A, prova pratica: andature su tratti di almeno ¼ di miglio, uomo in mare, ormeggio e disormeggio, dotazioni, preparativi per il cattivo tempo. All. D: nodi, effetti di timone ed elica, bussola e strumentazione, ormeggio, disormeggio e simulazione di ancoraggio a motore, recupero di uomo in mare. Le modalità concrete (barca, ordine delle manovre) le decide la commissione.')

# ============ PRIMA DI MOLLARE ============
L1=['Se il motore è a benzina: <b>ventila il vano motore</b> prima di avviare','Carburante e olio: controlla i livelli','Avvia <b>in folle</b>, poi guarda lo scarico: deve uscire <b>acqua di raffreddamento</b>','Col fuoribordo: <b>stacco di sicurezza</b> al polso o al giubbotto']
L2=['<b>Bollettino meteo</b> letto prima di uscire','<b>Giubbotti</b> a bordo, uno per persona, e indossati se serve','Dotazioni al loro posto: anulare, estintori, VHF','<b>Parabordi e cime</b> pronti, equipaggio informato: chi fa cosa']
sec('prima', head(EB,'Prima di mollare gli ormeggi',SEA)
    +f'<div style="display:flex; gap:24px; align-items:stretch">{tile("Il motore",ul(L1,30),CORAL)}{tile("La barca e le persone",ul(L2,30),SEA)}</div>'
    +note('Dillo ad alta voce mentre controlli: l\'esaminatore deve sentire che sai cosa fai.',SEA,36),
 notes='Quiz 1.3.6-20 (ventilazione forzata prima dell\'avvio: ricambio completo dell\'aria), 1.3.8-16 (stacco di sicurezza del fuoribordo). Acqua di raffreddamento dallo scarico e avvio in folle: lezione dei motori. Bollettini meteo e VHF: lezioni di meteorologia e sicurezza.')

# ============ ELICA E TIMONE ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.12"/>'+line(546,40,546,590,'#C9D3DD',3)
for cx,rev in ((273,False),(819,True)):
    b+=topboat(cx,270,300,-90,'#FFFFFF',NAVY,5)
    sy=420
    b+=f'<ellipse cx="{cx}" cy="{sy+6}" rx="18" ry="8" fill="{NAVY}"/>'
    if not rev: b+=wash(cx,sy+6,90,3,SEA)+arrow(cx,110,cx,60,NAVY,6,20)+arrow(cx+20,sy-10,cx+140,sy-10,CORAL,10,30)
    else: b+=arrow(cx+130,200,cx+130,330,NAVY,6,20)+arrow(cx-20,sy-10,cx-140,sy-10,CORAL,10,30)
lbl=pill(X+40,Y+24,420,'Marcia avanti',NAVY,24)+pill(X+586,Y+24,420,'Marcia indietro',NAVY,24)
lbl+=lab(X+20,Y+510,500,'la poppa va a <b>dritta</b>',CORAL,30,800,'center')+lab(X+566,Y+510,500,'la poppa va a <b>sinistra</b>',CORAL,30,800,'center')
txt=term('Elica destrorsa','Vista da poppa gira in senso orario in marcia avanti. Spinge la poppa a dritta in avanti e a sinistra in retromarcia.')+term('Quando si sente di più','Da fermi e con poco abbrivio, quando il timone ancora non governa: proprio nelle manovre in porto.')+term('Il timone','Governa solo se l\'acqua gli scorre sopra. In retro la barca risponde tardi: usa colpi di motore brevi.')
sec('evolutivo', head('Manovre in porto · lezione 2','Elica e timone in manovra'), pinned=svgp(X,Y,W,Hh,b,'Due barche viste dall\'alto con elica destrorsa: in marcia avanti la poppa si sposta verso dritta, in marcia indietro verso sinistra')+lbl+pcol(txt,532,20),
 notes='Quiz 1.1.2-44 (elica destrorsa in marcia avanti: prua a sinistra, poppa a dritta), -45, -12, -30, -23, -41. In retromarcia l\'effetto è opposto e più forte, perché il timone è poco efficace. All\'esame si chiede di sfruttarlo: per esempio accostare più facilmente con la banchina sul lato sinistro, o compensarlo con il timone.')
X=700

# ============ DISORMEGGIO DI POPPA ============
b=f'<rect x="0" y="0" width="1092" height="130" fill="{QUAY}"/>'+line(0,130,1092,130,NAVY,5)
b+=f'<path d="M40 598 L1052 598" stroke="{NAVY}" stroke-width="7" stroke-dasharray="12 7"/>'
for x in (300,792):
    b+=topboat(x,330,360,90,'#FFFFFF',NAVY,3,0.45,False)
b+=topboat(546,330,360,90,'#FFFFFF',NAVY,4)
b+=rope('M515 160 L610 112',CORAL,7)+rope('M577 160 L482 112',CORAL,7)
b+=f'<path d="M546 510 Q600 560 620 598" fill="none" stroke="{SEA}" stroke-width="6" stroke-dasharray="4 10" stroke-linecap="round"/>'
b+=''.join(bollard(x,112) for x in (482,610))
b+=arrow(500,520,500,590,NAVY,8,24)
b+=num(660,560,1,SEA,22)+num(650,120,2,CORAL,22)+num(460,560,3,NAVY,22)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+pill(X+690,Y+520,300,'trappa che affonda',SEA,22)
txt=item(1,SEA,'Molla la trappa','Mollala da prua e lasciala affondare lungo la fiancata: deve arrivare sul fondo, lontano dall\'elica.')+item(2,CORAL,'Molla le cime di poppa','Prima quella sottovento, poi quella sopravento. Col doppino le recuperi da bordo.')+item(3,NAVY,'Esci diritto e piano','Avanti adagio, al centro del corridoio. Parabordi dentro solo quando sei fuori.')
sec('disormeggio', head('Manovre in porto · lezione 3','Disormeggio di poppa')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto: barca ormeggiata di poppa tra altre due barche; si molla prima la trappa di prua, che affonda, poi le cime di poppa incrociate, poi si esce avanti')+lbl,
 notes='Quiz 1.4.4-7, -22, -8 (ormeggio di poppa e trappa), -29 (doppino). Il rischio principale è la trappa nell\'elica: prima di ingranare si guarda che sia affondata. Con vento al traverso si molla per ultima la cima sopravento, così la poppa non va addosso al vicino sottovento.')

# ============ ORMEGGIO DI POPPA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="130" fill="{QUAY}"/>'+line(0,130,1092,130,NAVY,5)
for x in (300,792):
    b+=topboat(x,330,360,90,'#FFFFFF',NAVY,3,0.45,False)
b+=topboat(546,300,360,90,'#FFFFFF',NAVY,4)
b+=topboat(860,560,300,160,'#FFFFFF',NAVY,3,0.35,False)
b+=dpath('M820 540 Q620 520 560 470',CORAL,6)+head_at(560,470,-120,CORAL,18)
b+=rope('M577 130 L610 112',CORAL,7)+bollard(482,112)+bollard(610,112)
b+=''.join(f'<rect x="{x}" y="{y}" width="20" height="44" rx="10" fill="{BLUE}"/>' for x,y in ((486,180),(590,180),(486,300),(590,300)))
b+=windarrow(1060,250,100,GREY,180)
b+=num(840,470,1,NAVY,22)+num(700,560,2,CORAL,22)+num(646,120,3,CORAL,22)+num(546,520,4,SEA,22)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+lab(X+960,Y+270,120,'vento',GREY,24,800)
txt=item(1,NAVY,'Prepara prima','Parabordi su tutti e due i lati, cime di poppa pronte, mezzo marinaio a portata.')+item(2,CORAL,'Retro lenta','Allineati al posto e vai indietro piano. Correggi con brevi colpi di motore e ricorda l\'effetto dell\'elica.')+item(3,CORAL,'Prima la cima sopravento','A terra si dà volta prima alla cima di poppa sopravento: tiene la barca contro il vento.')+item(4,SEA,'Poi la trappa','Recuperala con il mezzo marinaio, portala a prua e mettila in tiro.')
sec('ormeggio', head('Manovre in porto · lezione 3','Ormeggio di poppa'), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto: la barca arriva in retromarcia nel posto tra due barche ormeggiate di poppa, con i parabordi fuori e la prima cima di poppa data sul lato sopravento')+lbl+pcol(txt,532,18),
 notes='Quiz 1.4.4-7, -22, -8, -14…-17 (ormeggi e cavi). In retromarcia con elica destrorsa la poppa tende a sinistra: si imposta la manovra per compensare, o per sfruttarlo. Mai scendere a terra saltando: si passa la cima a chi è in banchina, oppure si scende quando la barca è ferma e vicina. Con vento traverso la prima cima da dare è quella sopravento.')
X=700

# ============ ALL'INGLESE ============
b=f'<rect x="0" y="0" width="1092" height="150" fill="{QUAY}"/>'+line(0,150,1092,150,NAVY,5)
b+=topboat(330,420,320,-25,'#FFFFFF',NAVY,3,0.4,False)
b+=dpath('M180 490 Q420 360 560 260',CORAL,6)
b+=topboat(640,225,340,0,'#FFFFFF',NAVY,4)
b+=''.join(f'<rect x="{x}" y="152" width="44" height="22" rx="11" fill="{BLUE}"/>' for x in (540,640,740))
b+=rope('M790 212 L930 128',NAVY,7)+bollard(930,128)
b+=arrow(500,300,500,200,PURPLE,5,18)
b+=num(260,520,1,CORAL,22)+num(960,200,2,NAVY,22)+num(470,320,3,PURPLE,22)
lbl=lab(X+40,Y+40,300,'BANCHINA',INK,26,900)+pill(X+100,Y+560,420,'angolo di 20–30°, piano',CORAL,22)
txt=item(1,CORAL,'Avvicinati di sbieco','Con un angolo di 20–30° e pochissima velocità. Parabordi fuori sul lato della banchina.')+item(2,NAVY,'Prima la cima di prua','Appena la prua è vicina si passa la cima di prua o lo spring.')+item(3,PURPLE,'Colpo di retro','In folle, poi un breve colpo indietro: ferma la barca e avvicina la poppa. Con elica destrorsa è più facile con la banchina a sinistra.')
sec('inglese', head('Manovre in porto · lezione 3','Ormeggio all\'inglese')+col(txt,540,22), pinned=svgp(X,Y,W,Hh,b,'Vista dall\'alto: la barca si avvicina alla banchina con un angolo di circa 25 gradi, poi si affianca con la banchina sul lato sinistro; parabordi fuori e cima di prua alla bitta')+lbl,
 notes='Ormeggio all\'inglese, cioè di fianco: cime e spring nella lezione 3 (quiz 1.4.4-5, -6, -13). Con elica destrorsa, il colpo di retro sposta la poppa a sinistra: se la banchina è sulla sinistra la poppa si avvicina da sola. Con la banchina a dritta si arriva con un angolo più piccolo e si usa lo spring. Per disormeggiare di fianco: si molla tutto tranne lo spring di prua, si va avanti adagio col timone verso la banchina e la poppa si apre.')

# ============ ANCORAGGIO ============
X=128
b=f'<rect x="0" y="0" width="1092" height="190" fill="{SKY}"/><rect x="0" y="190" width="1092" height="430" fill="{WATER}" fill-opacity="0.18"/>'+line(0,190,1092,190,SEA,3)
b+=f'<path d="M0 540 Q300 525 600 545 T1092 535 L1092 620 L0 620 Z" fill="{SEABED}" fill-opacity="0.55"/>'
b+=profile(80,190,380)
bx,by=80+380*0.97,190-380*0.09
ax,ay=900,535
b+=f'<path d="M{bx:.0f} {by:.0f} Q560 250 640 470 Q680 540 {ax} {ay}" fill="none" stroke="{NAVY}" stroke-width="6" stroke-dasharray="3 5" stroke-linecap="round"/>'
b+=f'<g transform="translate({ax} {ay-8})"><path d="M0 -40 L0 8 M-26 -8 Q-24 14 0 14 Q24 14 26 -8" fill="none" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/><path d="M-16 -30 L16 -30" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/><circle cx="0" cy="-46" r="7" fill="none" stroke="{NAVY}" stroke-width="5"/></g>'
b+=dim(1040,190,1040,538,CORAL)
b+=''.join(arrow(1060-i*10,70+i*40,960-i*10,70+i*40,GREY,6,20) for i in range(2))
lbl=lab(X+920,Y+330,110,'fondale',CORAL,24,800,'right')+pill(X+520,Y+250,360,'calumo 3–5 volte il fondale',NAVY,22)+lab(X+880,Y+140,200,'vento',GREY,24,800)
txt=item(1,CORAL,'Prua al vento','Scegli il punto, controlla fondale e divieti. Arriva piano, con la prua al vento o alla corrente.')+item(2,SEA,'Dai fondo da fermo','Quando l\'abbrivio è finito dai fondo all\'ancora, poi vai indietro piano filando catena.')+item(3,PURPLE,'Fai presa','Con 3–5 volte il fondale filato dai un colpo di retro: se la catena si tende e resta ferma, l\'ancora ha fatto testa.')+item(4,NAVY,'Controlla','Prendi due rilevamenti su punti a terra e ripetili: se cambiano, l\'ancora ara.')
sec('ancora', head('Manovre in porto · lezione 4','Ancoraggio a motore'), pinned=svgp(X,Y,W,Hh,b,'Sezione laterale: barca a motore con la prua al vento, la catena scende in curva fino all\'ancora sul fondo; il calumo è da tre a cinque volte il fondale')+lbl+pcol(txt,532,16),
 notes='All. D: simulazione di ancoraggio a motore. Quiz 1.4.3-2 (divieti e meteo prima di dare fondo), -3 (da 3 a 5 volte il fondale), -12 (fasi dell\'ancoraggio: solo abbrivio, prua al vento o alla corrente, dar fondo, filare indietreggiando), -15 (tenuta con rilevamenti successivi), -17 e -31 (l\'ancora fa testa), -24 (l\'ancora ara), -42, -43, -46 (vento forte: filare catena). Distanza dalle spiagge: 1.4.2-4.')
X=700

# ============ SALPARE ============
def anc(x,y,s=0.8): return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -40 L0 8 M-26 -8 Q-24 14 0 14 Q24 14 26 -8" fill="none" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/><path d="M-16 -30 L16 -30" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/><circle cx="0" cy="-46" r="7" fill="none" stroke="{NAVY}" stroke-width="5"/></g>'
SB=f'<rect x="0" y="0" width="1664" height="80" fill="{SKY}"/><rect x="0" y="80" width="1664" height="170" fill="{WATER}" fill-opacity="0.18"/>'+line(0,80,1664,80,SEA,3)+f'<rect x="0" y="222" width="1664" height="28" fill="{SEABED}" fill-opacity="0.55"/>'
for i,(x0,chain,ax,ay) in enumerate(((120,'M{bx} {by} Q{mx} 150 {ax} 214',400,214),(700,'M{bx} {by} L{bx} 214',0,214),(1250,'M{bx} {by} L{bx} 190',0,190))):
    L=220; bx=x0+L*0.97; by=80-L*0.09
    ax=ax or bx
    SB+=profile(x0,80,L)+f'<path d="{chain.format(bx=round(bx),by=round(by),mx=round(bx+60),ax=ax)}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-dasharray="3 5" stroke-linecap="round"/>'+anc(ax,ay+6 if i<2 else ay,0.7)
    SB+=num(x0-40,40,i+1,(CORAL,SEA,PURPLE)[i],22)
SB+=arrow(360,40,460,40,CORAL,5,16)
ST=[('1','Avanti adagio','Vai verso l\'ancora con il motore, piano, mentre a prua si recupera la catena.',CORAL),
    ('2','A picco','Quando la catena è verticale sei sopra l\'ancora. Chi è a prua lo dice ad alta voce.',SEA),
    ('3','Spedare','Un leggero colpo avanti toglie tensione e stacca l\'ancora dal fondo. Poi si recupera tutta.',PURPLE),
    ('4','In posizione','Ancora a posto nel musone e bloccata. Solo allora si riprende la navigazione.',BLUE)]
g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:24px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1; color:{c}">{n}</p>{h3(t,32,c)}{p(d,26,BODY,400,1.4)}</div>' for n,t,d,c in ST)
sec('salpare', head('Manovre in porto · lezione 4','Salpare l\'ancora',SEA)+f'<div style="display:flex; gap:22px; align-items:stretch">{g}</div>'+svgi(1664,250,SB,'Tre barche di profilo: la prima avanza con la catena obliqua, la seconda è sopra l\'ancora con la catena verticale, la terza ha staccato l\'ancora dal fondo',pan=True)
    +note('Non tirare la catena con il motore: il verricello recupera, il motore aiuta.',SEA,36),
 notes='Quiz 1.4.3-51 (per salpare si dà un leggero colpo di marcia avanti per togliere tensione alla catena). Chi sta a prua comunica con i gesti o a voce: direzione della catena e «a picco». Se l\'ancora è incattivita si prova a girarle attorno o si usa il grippiale (1.4.3-13).')

# ============ VERIFICA 1 ============
quiz_slide('quiz1','Verifica · ancoraggio',['1.4.3-3','1.4.3-51','1.4.3-17'],False)
quiz_slide('quiz1r','Verifica · ancoraggio',['1.4.3-3','1.4.3-51','1.4.3-17'],True)

# ============ UOMO A MARE A MOTORE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.14"/>'
cx_,cy_,R=520,280,170
b+=dpath(f'M{cx_-R} 600 L{cx_-R} {cy_}',NAVY,5,False)
path=f'M{cx_-R} {cy_} A{R} {R} 0 1 1 {cx_-R*math.cos(math.radians(40)):.1f} {cy_+R*math.sin(math.radians(40)):.1f}'
b+=dpath(path,CORAL,6)
b+=topboat(cx_-R,520,130,-90,'#FFFFFF',NAVY,4)+topboat(cx_+R,cy_,130,90,'#FFFFFF',NAVY,4)
px_,py_=cx_-R+70,cy_+60
b+=person(px_,py_,CORAL,1.2)+ring(px_+44,py_-6,18)
b+=f'<path d="M{cx_+R-20} {cy_-10} L{px_+20} {py_-10}" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="4 8"/>'
b+=num(cx_-R-40,420,1,NAVY,22)+num(cx_-R+20,cy_-60,2,CORAL,22)+num(px_+80,py_+40,3,ORANGE,22)+num(cx_+R+60,cy_-70,4,PURPLE,22)+num(cx_-40,cy_+R+10,5,SEA,22)
lbl=pill(X+30,Y+470,320,'«Uomo a mare a dritta!»',NAVY)+pill(X+40,Y+150,320,'accosta dallo stesso lato',CORAL)+pill(X+520,Y+368,240,'lancia il salvagente',ORANGE)
lbl+=pill(X+790,Y+194,260,'occhi sempre su di lui',PURPLE)+pill(X+510,Y+448,300,'arriva piano, in folle',SEA)
txt=item(1,NAVY,'Grida il lato','«Uomo a mare a dritta!» Tutti devono sapere dove guardare.')+item(2,CORAL,'Accosta subito','Dallo stesso lato: la poppa e l\'elica si allontanano dalla persona.')+item(3,ORANGE,'Salvagente e occhi','Lancia l\'anulare. Una persona indica il naufrago col braccio e non lo perde mai di vista.')+item(4,SEA,'Arriva in folle','Piano, con la prua verso il naufrago e sopravento a lui. Vicino alla persona: motore in folle.')
sec('uomomotore', head('In mare · lezione 9','Uomo a mare a motore')+col(txt,520,20), pinned=svgp(X,Y,W,Hh,b,'Manovra di recupero vista dall\'alto: la barca accosta subito dal lato del naufrago, compie un giro e torna piano verso di lui; il salvagente anulare è vicino alla persona in acqua')+lbl,
 notes='All. A e All. D: recupero di uomo in mare. All\'esame il naufrago di solito si simula con un parabordo o un salvagente in acqua. Quiz 1.3.6-28 (avvicinamento con prudenza dopo aver smaltito la velocità), -29 e -35 (anulare), -31, -33, -36 (accostare dallo stesso lato), -32 e -34 (controllo visivo), 1.3.8-16 (stacco di sicurezza). Si arriva sopravento al naufrago così la barca scarroccia verso di lui, non sopra di lui con l\'elica.')

# ============ UOMO A MARE A VELA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.14"/>'
b+=''.join(windarrow(x,24,80) for x in (500,580))
mx,my=250,330
b+=dpath(f'M{mx} {my} L720 {my}',NAVY,6)
b+=dpath(f'M720 {my} Q860 {my} 850 250 Q830 180 740 220',PURPLE,6)
b+=dpath('M740 220 Q560 330 420 470 Q360 520 300 480',SEA,6)
b+=dpath(f'M300 480 Q270 440 {mx+30} {my+40}',CORAL,6)+head_at(mx+30,my+40,-110,CORAL,20)
b+=topboat(470,my,120,0,'#FFFFFF',NAVY,4)+topboat(560,395,120,135,'#FFFFFF',NAVY,4)
b+=person(mx,my,CORAL,1.2)+ring(mx-44,my-4,18)
b+=num(mx+80,my-60,1,NAVY,22)+num(900,220,2,PURPLE,22)+num(470,500,3,SEA,22)+num(220,480,4,CORAL,22)
lbl=lab(X+470,Y+110,200,'vento',GREY,24,800)+pill(X+300,Y+254,200,'al traverso',NAVY)+pill(X+780,Y+120,160,'virata',PURPLE)+pill(X+560,Y+470,200,'ritorno al lasco',SEA)+pill(X+40,Y+540,420,'arrivo di bolina, vele sventate',CORAL)
txt=item(1,NAVY,'Traverso','Grida, lancia l\'anulare, indica il naufrago. Porta la barca al traverso e allontanati di poche lunghezze.')+item(2,PURPLE,'Vira','Virata: ora il naufrago è sottovento a te.')+item(3,SEA,'Torna al lasco','Scendi verso un punto sottovento al naufrago, così l\'ultimo tratto sarà di bolina.')+item(4,CORAL,'Arriva di bolina','Lasca le scotte: le vele sventano e la barca rallenta fino a fermarsi accanto alla persona.')
sec('uomovela', head('In mare · lezione 9','Uomo a mare a vela'), pinned=svgp(X,Y,W,Hh,b,'Recupero a vela visto dall\'alto con il vento da nord: la barca va al traverso, vira, torna al lasco sotto il naufrago e risale di bolina lascando le vele fino a fermarsi accanto a lui')+lbl+pcol(txt,532,18),
 notes='È la manovra più insegnata nelle scuole; la commissione può accettare anche altre manovre corrette, per esempio fermarsi alla cappa o accendere il motore, dopo aver controllato che non ci siano cime in acqua (lezione 9). Il punto chiave è l\'ultimo tratto: di bolina si rallenta lascando le vele; al lasco o in poppa non si riesce a fermarsi. Il recupero si fa sul lato sottovento, dove il bordo è più basso.')
X=700

# ============ ANDATURE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.12"/>'
cx,cy,R=546,330,230
b+=f'<path d="M{cx} {cy} L{cx+R*math.sin(math.radians(-45)):.0f} {cy-R*math.cos(math.radians(-45)):.0f} A{R} {R} 0 0 1 {cx+R*math.sin(math.radians(45)):.0f} {cy-R*math.cos(math.radians(45)):.0f} Z" fill="{CORAL}" fill-opacity="0.14"/>'
b+=windarrow(cx,20,70)
AN=[(45,'bolina',CORAL),(90,'traverso',SEA),(135,'lasco',PURPLE),(180,'poppa',BLUE)]
for a,t,c in AN:
    for s in (1,-1):
        x=cx+R*math.sin(math.radians(a*s)); y=cy-R*math.cos(math.radians(a*s))
        if a==180 and s==-1: continue
        b+=line(cx,cy,x,y,'#C9D3DD',2)+topboat(x,y,110,a*s-90,'#FFFFFF',c,4)
b+=f'<circle cx="{cx}" cy="{cy}" r="10" fill="{NAVY}"/>'
lbl=pill(X+cx-90,Y+150,180,'angolo morto',CORAL)
for a,t,c in AN:
    x=cx+(R+80)*math.sin(math.radians(a)); y=cy-(R+50)*math.cos(math.radians(a))
    lbl+=pill(X+min(x,940),Y+y-16,160,t,c)
lbl+=pill(X+30,Y+560,400,'¼ di miglio ≈ 463 metri',NAVY,24)
txt=item('¼',NAVY,'Tratti di almeno ¼ di miglio','L\'esaminatore chiede un\'andatura: la tieni costante per un tratto di almeno 463 metri.')+item('⛵',SEA,'Vele regolate','Lasca finché la vela di prua fileggia, poi cazza appena: i filetti devono scorrere.')+item('↻',PURPLE,'Cambi d\'andatura','Orza e poggia dando gli ordini: chi regola le scotte segue il timone.')
sec('andature', head('In mare · lezione 8','Le andature')+col(txt,540,24), pinned=svgp(X,Y,W,Hh,b,'Rosa delle andature vista dall\'alto con il vento da nord: bolina, traverso, lasco su entrambe le mure e poppa; il settore di circa 45 gradi per lato attorno al vento è l\'angolo morto')+lbl,
 notes='All. A, prova pratica: andature su tratti di almeno un quarto di miglio. Un miglio nautico è 1852 m, quindi un quarto è circa 463 m. Si controlla l\'andatura con il segnavento in testa d\'albero e con i filetti sulle vele (lezione 8). A bolina si tiene la barca il più possibile vicina al vento senza far fileggiare il fiocco; in poppa attenzione alla strambata.')

# ============ VIRATA E ABBATTUTA A VOCE ============
def bubble(who,t,c,right=False):
    al='flex-end' if right else 'flex-start'; bg=c if not right else '#FFFFFF'; tc='#FFFFFF' if not right else INK
    return f'<div style="display:flex; flex-direction:column; align-items:{al}; gap:4px">{p(who,22,SOFT,800,1.2)}<p style="font-family:{H}; font-size:34px; font-weight:700; line-height:1.15; color:{tc}; background:{bg}; border:3px solid {c}; border-radius:24px; padding:10px 22px">{t}</p></div>'
def dialog(t,steps,c,act):
    return tile(t,''.join(bubble(w,s,c,r) for w,s,r in steps)+p(act,24,BODY,400,1.4),c)
V=dialog('Virata · la prua nel vento',[('timoniere','«Pronti a virare?»',False),('equipaggio','«Pronti!»',True),('timoniere','«Vira!»',False)],CORAL,
         'Il timoniere orza e la prua passa nel vento. Si molla la scotta del fiocco sul vecchio lato e si cazza sul nuovo.')
A=dialog('Abbattuta · la poppa nel vento',[('timoniere','«Pronti ad abbattere?»',False),('equipaggio','«Pronti!»',True),('timoniere','«Abbatti!»',False)],PURPLE,
         'Prima si cazza la randa al centro. Il timoniere poggia e la poppa passa nel vento; poi si lasca sul nuovo bordo.')
sec('virata', head('In mare · lezione 8','Virata e abbattuta a voce',PURPLE)+f'<div style="display:flex; gap:24px; align-items:stretch">{V}{A}</div>'
    +note('Aspetta il «Pronti!» prima di muovere il timone. E guarda sempre intorno prima di virare.',PURPLE,36),
 notes='Comandi e manovre dalla lezione 8, quiz 2.3.1-9, -10, -11, -12, -40, -41, -57, -61…-63. Nell\'abbattuta il boma attraversa il pozzetto: tutti a testa bassa. Con fiocco autovirante in virata la scotta non si tocca (2.2.1-81).')

# ============ BUSSOLA E STRUMENTI ============
cb=f'<circle cx="130" cy="130" r="112" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/>'
for a in range(0,360,30):
    r0=92 if a%90 else 80; x0=130+r0*math.sin(math.radians(a)); y0=130-r0*math.cos(math.radians(a)); x1=130+104*math.sin(math.radians(a)); y1=130-104*math.cos(math.radians(a))
    cb+=line(x0,y0,x1,y1,NAVY,4 if a%90==0 else 2)
cb+=''.join(f'<text x="{130+62*math.sin(math.radians(a)):.0f}" y="{140-62*math.cos(math.radians(a)):.0f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="{NAVY}">{t}</text>' for a,t in ((0,'N'),(90,'E'),(180,'S'),(270,'W')))
cb+=topboat(130,130,64,-90,CORAL,NAVY,3,1,False)+line(130,6,130,40,SEA,6)
IN=[('Bussola','Tieni la <b>prora bussola</b> che ti danno: guarda la linea di fede e correggi poco e subito. Ogni tanto guarda fuori.',CORAL),
    ('Ecoscandaglio','Dà il fondale sotto la chiglia. Prima di ancorare e in acque basse va sempre guardato.',SEA),
    ('GPS e plotter','Danno punto nave, velocità e rotta sul fondo. Servono anche per controllare che l\'ancora non ari.',PURPLE),
    ('Log e anemometro','Il log dà la velocità sull\'acqua; l\'anemometro il vento apparente.',BLUE)]
g=''.join(tile(t,p(d,27,BODY,400,1.45),c) for t,d,c in IN)
sec('bussola', head('In mare · lezioni 10–12','Bussola e strumenti',SEA)
    +f'<div style="display:flex; gap:28px; align-items:center">{svgi(260,260,cb,"Rosa della bussola con la linea di fede in alto",dw=340,dh=340,pan=False)}<div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:18px">{g}</div></div>',
 notes='All. D: bussola e strumentazione. All\'esame si può chiedere di tenere una prora bussola per un tratto e di leggere gli strumenti. La prora bussola non è la prora vera: tra le due ci sono declinazione e deviazione (lezioni 10–12). Con mare formato la rosa oscilla: si tiene la media, senza inseguire l\'ago.')

# ============ CATTIVO TEMPO ============
CT=[('Le persone','Giubbotti indossati. Chi sta in coperta usa la cintura e si aggancia alla barca.',CORAL),
    ('La barca','Chiudi oblò, boccaporti e prese a mare, tranne quella del motore. Rizza tutto quello che si muove.',SEA),
    ('Le vele','Riduci per tempo: terzaroli alla randa e fiocco ridotto, prima che il vento aumenti.',PURPLE),
    ('La velocità','Con mare grosso rallenta. Non prendere le onde al traverso.',BLUE),
    ('La rotta','Stai lontano da una costa sottovento. Se la burrasca viene da terra, vai sotto costa, dove il mare è più calmo.',GREEN),
    ('La radio','Ascolta gli avvisi di burrasca sul VHF. Tieni pronta la posizione.',ORANGE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:28px 28px">{h3(t,34,c)}{p(d,28,BODY,400,1.45)}</div>' for t,d,c in CT)
sec('cattivo', head('In mare · lezione 9','Arriva il cattivo tempo',BLUE)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px">{g}</div>',
 notes='All. A: preparativi per il cattivo tempo. Quiz 1.3.8-2 (rizzare gli oggetti, chiudere oblò e osterigi, istruire le persone sui mezzi di salvataggio), -23 (chiudere oblò, boccaporti e prese a mare tranne quella del motore), -22 (in solitario: cintura e assicurarsi al ponte), -5 e -8 (ridurre la velocità, onde non al traverso), -3 (tempesta da terra: verso la costa), -4 (tempesta dal mare: alla cappa), -18 e -21 (ancora galleggiante). Avvisi di burrasca: 1.6.2-14, -21. Terzaroli: lezione 8.')

# ============ VERIFICA 2 ============
quiz_slide('quiz2','Verifica · sicurezza in mare',['1.3.6-33','1.3.8-23','1.3.8-22'],False)
quiz_slide('quiz2r','Verifica · sicurezza in mare',['1.3.6-33','1.3.8-23','1.3.8-22'],True)

# ============ NODI ============
ND=[('Gassa d\'amante','Un occhio che non scorre e non si stringe. Per dar volta a una bitta, per il salvataggio.',CORAL),
    ('Nodo parlato','Lega i parabordi a draglie e pulpiti. Si regola in altezza facilmente.',SEA),
    ('Volta alla bitta','Dà volta a una cima su una bitta o una galloccia, e si molla in fretta.',PURPLE),
    ('Nodo di bozza','Tiene per poco una cima in tensione, per esempio per liberare un winch.',BLUE)]
KN=['gassa','parlato','bitta','bozza']
g=''.join(tile(t,p(d,26,BODY,400,1.4),c,pic(PIC[k],'Disegno: '+t)) for (t,d,c),k in zip(ND,KN))
sec('nodi', head('Il giorno della prova · appendice C','I quattro nodi della prova',CORAL)+f'<div style="display:flex; gap:22px; align-items:stretch">{g}</div>'
    +note('Fateli ad occhi chiusi: l\'esaminatore può chiederli in qualunque momento.',CORAL,36),
 notes='All. D: gassa d\'amante, parlato, bitta, bozza. Ognuno è disegnato passo per passo nell\'Appendice C. Allenarsi con una cima vera, anche sulle ginocchia o intorno a una gamba del tavolo. La gassa va fatta anche attorno a sé stessi, come per un salvataggio.')

# ============ DOTAZIONI ============
DT=[('Salvataggio','Giubbotti, salvagente anulare con cima, boetta luminosa, zattera se prevista.',CORAL),
    ('Segnalazione','Fuochi a mano, razzi, fumogeni, strumento per segnali sonori, fanali.',SEA),
    ('Antincendio','Estintori: dove sono, di che tipo, come si usano.',PURPLE),
    ('Il resto','Pompa di sentina e sassola, cassetta di pronto soccorso, VHF, documenti.',BLUE)]
KD=['anulare','fuoco','estintore','kit']
g=''.join(tile(t,p(d,26,BODY,400,1.4),c,pic(PIC[k],'Disegno: '+t)) for (t,d,c),k in zip(DT,KD))
sec('dotazioni', head('Il giorno della prova · lezione 6','Le dotazioni di sicurezza',SEA)+f'<div style="display:flex; gap:22px; align-items:stretch">{g}</div>'
    +note('Sapere dove sono conta quanto sapere cosa sono: prima di partire, apri i gavoni.',SEA,36),
 notes='All. A: dotazioni. L\'esaminatore può chiedere di indicarle a bordo e spiegare come si usano. Le dotazioni obbligatorie dipendono dalla distanza dalla costa: tabelle e quiz nella lezione 6. Si mostra il giubbotto indossato correttamente, con le cinghie chiuse e regolate.')

# ============ ERRORI ============
ER=[('Troppo gas','In porto il motore si usa a colpi brevi. Se la manovra non riesce, fermati e ricomincia.',CORAL),
    ('Cime in acqua','Una cima vicino all\'elica ferma il motore. Guardaci prima di ingranare.',SEA),
    ('Perdere il naufrago','Se nessuno lo indica, in un attimo non lo vedi più.',PURPLE),
    ('Ordini confusi','Comandi brevi, ad alta voce, prima della manovra. Aspetta la risposta.',BLUE),
    ('Parabordi dimenticati','Fuori prima di entrare in porto, dentro solo quando sei al largo.',GREEN),
    ('Solo strumenti','Guardare solo la bussola o il GPS e non guardare fuori, intorno alla barca.',ORANGE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:28px 28px">{h3(t,34,c)}{p(d,28,BODY,400,1.45)}</div>' for t,d,c in ER)
sec('errori', head('Il giorno della prova','Gli errori più comuni',CORAL)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px">{g}</div>',
 notes='Sono gli errori che gli istruttori vedono più spesso. Nessuno di questi fa perdere la prova da solo, se lo si riconosce e si corregge con calma. Quello che conta è la sicurezza: persone, barca, altre barche.')

# ============ IL GIORNO DELLA PROVA ============
GP=[('Cosa portare','Quello che dice la convocazione. Scarpe con suola chiara che non scivola, abiti comodi, cappello, occhiali da sole.',CORAL),
    ('A bordo','Presentati all\'equipaggio. Guarda la barca: motore, elica, dotazioni, cime.',SEA),
    ('Mentre manovri','Di\' ad alta voce cosa fai e perché. Guarda sempre intorno prima di muovere il timone.',PURPLE),
    ('Se sbagli','Fermati, rimetti la barca in sicurezza e ricomincia. L\'esaminatore giudica anche come correggi.',BLUE)]
g=''.join(tile(t,p(d,28,BODY,400,1.45),c) for t,d,c in GP)
sec('giorno', head('Il giorno della prova','Il giorno della prova',PURPLE)+f'<div style="display:flex; gap:22px; align-items:stretch">{g}</div>'
    +note('Calma, voce chiara e occhi fuori dalla barca: la prova è tutta qui.',PURPLE,38),
 notes='Documenti e orari sono nella convocazione della Capitaneria o della Motorizzazione: si seguono quelli. La prova è una conversazione a bordo: l\'esaminatore chiede una manovra, il candidato la esegue comandando l\'equipaggio.')

closing(['La prova è a bordo: ormeggi, ancoraggio, uomo a mare, andature, dotazioni e cattivo tempo',
         'In porto il motore si usa piano e a colpi brevi, sfruttando l\'effetto dell\'elica',
         'Uomo a mare: grida il lato, lancia l\'anulare, non perdere mai di vista il naufrago',
         'A vela si arriva sul naufrago di bolina, con le vele sventate',
         'Di\' ad alta voce cosa fai: comandare l\'equipaggio fa parte della prova'],
 'Buon vento per la prova pratica!','Appendice E · La prova pratica')

write_deck(OUT,'Appendice E · La prova pratica',ORDER,
 {"s1":{"description":"Copertina, indice, la prova e i controlli prima di partire","start":"cover"},
  "s2":{"description":"Manovre in porto: elica e timone, ormeggi, ancoraggio","start":"evolutivo"},
  "s3":{"description":"In mare: uomo a mare, andature, virate, strumenti, cattivo tempo","start":"uomomotore"},
  "s4":{"description":"Il giorno della prova: nodi, dotazioni, errori, checklist","start":"nodi"}})
