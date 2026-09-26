import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez07/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; GREY='#97A6B4'; NIGHT='#0F2238'; SKY='#DDEFF7'; LRED='#E23B3B'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Alta e bassa pressione':'cloud','Le brezze':'wind','I venti del Mediterraneo':'compass',
 'Quanto soffia: la scala Beaufort':'wind','I fronti':'cloud','Le nubi':'cloud','Le onde':'current','Bollettini e segni del tempo':'lighthouse',
 'Natanti, imbarcazioni, navi':'hull','I documenti di bordo':'book','La patente nautica':'book','Visite e certificato di sicurezza':'check',
 'Il comandante e l\'autorità marittima':'flag','Aree marine protette e ambiente':'map','Lo sci nautico':'helm'})
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def cloudp(x,y,s=1,c='#FFFFFF',op=1):
    return f'<g transform="translate({x} {y}) scale({s})" opacity="{op}"><ellipse cx="0" cy="0" rx="46" ry="26" fill="{c}"/><circle cx="-26" cy="-8" r="22" fill="{c}"/><circle cx="10" cy="-22" r="28" fill="{c}"/><circle cx="36" cy="-4" r="20" fill="{c}"/></g>'
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(7,'Meteorologia e normativa','Leggere il cielo e i bollettini; conoscere le regole, i documenti e le autorità del diporto',
 'Lezione 7. Capitoli del programma della scuola: Meteorologia e Normativa. Aggiunte dall\'All. A al DM 323/2021: visite e certificazioni (3b) e autorità marittima e ordinanze (8b). La meteo pesa 2 quesiti su 20, la normativa 3.')
blocks=[('0:00','30′','Pressione, brezze, venti, Beaufort · quiz 1',CORAL),('0:30','25′','Fronti, nubi, onde, bollettini · quiz 2',SEA),('0:55','25′','Unità, documenti, patente, visite · quiz 3',PURPLE),('1:20','25′','Autorità, ambiente, sci nautico · quiz 4',BLUE),('1:45','15′','Verifica finale',CORAL)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("All'esame")+f'<p style="font-family:{H}; font-size:88px; font-weight:700; line-height:1.05; color:{INK}">2 + 3</p>'+p('domande su 20: Meteorologia e Normativa',26,INK,700)+p('Oltre 400 quiz ufficiali in questi capitoli: qui i concetti, a casa l\'allenamento.',24))
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>leggere una carta del tempo e un bollettino</li><li>riconoscere venti, fronti e nubi</li><li>distinguere natanti, imbarcazioni e navi</li><li>sapere quali documenti tenere a bordo</li><li>conoscere doveri del comandante e autorità</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 07 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Quattro verifiche intermedie da 3 quiz e una finale da 6, tutti ufficiali (DD 131/2022). Banca: elementi di meteorologia 45 quiz (1.6.1), bollettini e previsioni 53 (1.6.2), venti 21 (1.6.3), leggi e regolamenti 124 (1.8.1), sci nautico, pesca, aree protette e ambiente 59 (1.8.2), visite e certificazioni 19 (1.3.4).')

# ============ PRESSIONE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
L=(330,320); Hp=(820,300)
b+=''.join(f'<ellipse cx="{L[0]}" cy="{L[1]}" rx="{40+i*42}" ry="{32+i*36}" fill="none" stroke="{BLUE}" stroke-width="3"/>' for i in range(6))
b+=''.join(f'<ellipse cx="{Hp[0]}" cy="{Hp[1]}" rx="{70+i*90}" ry="{56+i*80}" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="10 8"/>' for i in range(3))
def windarr(c0,r,phis,ccw,inward,col):
    s=''
    for ph in phis:
        f=math.radians(ph); px=c0[0]+r*math.cos(f); py=c0[1]+r*0.85*math.sin(f)
        tx,ty=(math.sin(f),-math.cos(f)) if ccw else (-math.sin(f),math.cos(f))
        ox,oy=(-math.cos(f),-math.sin(f)) if inward else (math.cos(f),math.sin(f))
        dx=tx*0.9+ox*0.45; dy=ty*0.9+oy*0.45; n=math.hypot(dx,dy); dx/=n; dy/=n
        s+=arrow(px-dx*35,py-dy*35,px+dx*35,py+dy*35,col,6,18)
    return s
b+=windarr(L,190,range(0,360,45),True,True,NAVY)+windarr(Hp,190,range(20,360,60),False,False,SOFT)
lbl=big(X+L[0]-40,Y+L[1]-45,80,'B',BLUE,90)+big(X+Hp[0]-40,Y+Hp[1]-45,80,'A',CORAL,90)
lbl+=lab(X+60,Y+560,480,'isobare fitte: vento forte',BLUE,24,900)+lab(X+640,Y+560,420,'isobare larghe: vento debole',CORAL,24,900)
txt=term('Pressione normale','1013,2 hPa al livello del mare: sopra è alta, sotto è bassa. Si misura con il barometro.')+term('Isobare','Linee di uguale pressione. Più sono vicine, più forte è il vento (gradiente barico).')+term('Il giro del vento','Nel nostro emisfero gira in senso antiorario attorno alla bassa, entrando verso il centro; in senso orario attorno all\'alta.')+term('Il segnale più utile','La tendenza della pressione: se scende in fretta arriva brutto tempo.')
sec('pressione', head('Meteorologia · la pressione','Alta e bassa pressione')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Carta del tempo: una bassa pressione con isobare fitte e il vento che gira in senso antiorario verso il centro; un\'alta pressione con isobare larghe e il vento in senso orario verso l\'esterno')+lbl,
 notes='Quiz 1.6.1-5 (hPa), 1.6.2-47 e 1.6.1-38 (1013,2 hPa), -6 (isobare), -34 e -35 (barometro), -19 (senso antiorario attorno alla bassa nel nostro emisfero), -20 e 1.6.2-53 (gradiente barico, isobare vicine = vento forte), -12 (tendenza della pressione), -25 (il vento nasce da differenze di temperatura e pressione), -38 (l\'aria calda è più leggera), -23 (anemometro), -36 (igrometro). Sulle carte italiane B = bassa, A = alta (in inglese L e H).')

# ============ BREZZE ============
def breeze(day):
    bg=SKY if day else '#23385A'; sea=WATER; s=f'<rect x="0" y="0" width="560" height="300" fill="{bg}"/>'
    s+=f'<rect x="0" y="220" width="300" height="80" fill="{sea}" fill-opacity="0.5"/><path d="M300 220 L560 200 L560 300 L300 300 Z" fill="{LAND}"/>'
    s+=(f'<circle cx="470" cy="60" r="34" fill="{SUN}"/>' if day else f'<circle cx="90" cy="60" r="28" fill="#F4F1DE"/><circle cx="104" cy="52" r="24" fill="#23385A"/>')
    if day: s+=arrow(120,190,420,180,NAVY,8,24)+dpath('M430 110 Q280 80 130 110',GREY,4)+arrow(420,150,440,110,GREY,4,14)
    else: s+=arrow(430,180,140,190,'#DDE6EC',6,20)+dpath('M140 110 Q280 90 420 110',GREY,4)
    return s
bc=card(svgi(560,300,breeze(True),'Di giorno la terra si scalda e la brezza soffia dal mare verso terra',dw=560,dh=300,pan=False)+h3('Di giorno: brezza di mare',30)+p('La terra si scalda <b>più in fretta</b> del mare: l\'aria sale sulla terra e dal mare arriva aria fresca. È la brezza più intensa.',25),None,24,10)
nc=card(svgi(560,300,breeze(False),'Di notte la terra si raffredda e la brezza soffia da terra verso il mare',dw=560,dh=300,pan=False)+h3('Di notte: brezza di terra',30)+p('La terra si raffredda <b>più in fretta</b> del mare: l\'aria scende da terra verso il mare. È più debole.',25),None,24,10)
sec('brezze', head('Meteorologia · il vento locale','Le brezze')+f'<div style="display:flex; gap:28px">{bc}{nc}</div>',
 notes='Quiz 1.6.1-24, -26, -28, -37 (brezza di mare di giorno: la terra si scalda prima), -27, -29, -31, -32, -33 (brezza di terra di notte: la terra si raffredda prima), -2 (la diurna è più intensa), -3 (escursione diurna). In estate la brezza di mare arriva a fine mattinata e cala al tramonto: attenzione al rientro.')

# ============ VENTI ============
X=128
cx,cy=546,320
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
for k,c in enumerate(['#FFE7A8','#CFEFF2','#FFD5C7','#E0D7FA']):
    a0,a1=k*90,(k+1)*90; p0=pol(cx,cy,a0,200); p1=pol(cx,cy,a1,200)
    b+=f'<path d="M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A200 200 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{c}"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="200" fill="none" stroke="{NAVY}" stroke-width="4"/>'
for a in range(0,360,45):
    o=pol(cx,cy,a,196); i=pol(cx,cy,a,70); b+=arrow(o[0],o[1],i[0],i[1],NAVY if a%90==0 else SOFT,6,20)
b+=f'<circle cx="{cx}" cy="{cy}" r="16" fill="{SUN}"/>'
names=[(0,'Tramontana','N'),(45,'Grecale','NE'),(90,'Levante','E'),(135,'Scirocco','SE'),(180,'Ostro','S'),(225,'Libeccio','SW'),(270,'Ponente','W'),(315,'Maestrale','NW')]
lbl=''
for a,nm,d in names:
    x,y=pol(cx,cy,a,258 if a%180==0 else 290); lbl+=lab(X+x-110,Y+y-18,220,f'{nm} · {d}',NAVY if a%90==0 else PURPLE,24,900,'center')
txt=term('Il nome dice da dove viene','Lo Scirocco viene da Sud-Est, cioè da 135°; il Ponente da Ovest, 270°.')+term('I quadranti','I: Tramontana, Grecale, Levante · II: Levante, Scirocco, Mezzogiorno · III: Mezzogiorno, Libeccio, Ponente · IV: Ponente, Maestrale, Tramontana.')+term('Ostro e Mezzogiorno','Sono lo stesso vento, da Sud.')
sec('venti', head('Meteorologia · i nomi','I venti del Mediterraneo'), pinned=svgp(X,Y,W,Hh,b,'Rosa dei venti con i quattro quadranti colorati e le frecce che arrivano da Tramontana, Grecale, Levante, Scirocco, Ostro, Libeccio, Ponente e Maestrale')+lbl+pcol(txt),
 notes='Quiz 1.6.3-1…-4 (venti dei quadranti), -5 (la rosa dei venti indica la direzione di provenienza), -6…-19 (singoli venti e gradi: Scirocco 135°, Ponente 270°, Ostro 180°, Maestrale da NW, Grecale da NE, Libeccio da SW), -15 (Ostro = Mezzogiorno), -20 (i venti intercardinali prendono il nome dalla provenienza). Ricordare: il vento si indica «da», la corrente «verso» (lezione 4).')
X=700

# ============ BEAUFORT ============
BF=[(0,'calma','<1'),(1,'bava di vento','1-3'),(2,'brezza leggera','4-6'),(3,'brezza tesa','7-10'),(4,'vento moderato','11-16'),(5,'vento teso','17-21'),(6,'vento fresco','22-27'),(7,'vento forte','28-33'),(8,'burrasca moderata','34-40'),(9,'burrasca forte','41-47'),(10,'tempesta','48-55'),(11,'tempesta violenta','56-63'),(12,'uragano','64 e oltre')]
W2,H2=1664,560; x0=60; bw=(W2-120)/13
def lerp(c1,c2,t):
    a=[int(c1[i:i+2],16) for i in (1,3,5)]; b_=[int(c2[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{int(a[k]+(b_[k]-a[k])*t):02X}' for k in range(3))
b=f'<rect x="0" y="0" width="{W2}" height="{H2}" fill="#F4FAFC"/>'
for f_,nm,kn in BF:
    h=30+f_*24; x=x0+f_*bw; c=lerp('#7CC6CF',CORAL,f_/12) if f_<=8 else lerp(CORAL,'#8E1B1B',(f_-8)/4)
    b+=f'<rect x="{x+8:.0f}" y="{400-h}" width="{bw-16:.0f}" height="{h}" rx="12" fill="{c}"/>'
for cat,f_,c in (('D',4,GREEN),('C',6,BLUE),('B',8,PURPLE)):
    x=x0+(f_+1)*bw-2; b+=f'<path d="M{x:.0f} 40 V410" stroke="{c}" stroke-width="4" stroke-dasharray="10 7"/>'
lbl=''.join(lab(128+x0+f_*bw,Y+405,bw,str(f_),NAVY,30,900,'center') for f_,_,_ in BF)
for f_ in (0,2,4,6,8,10,12):
    nm=BF[f_][1]; kn=BF[f_][2]; x=128+x0+f_*bw-40; lbl+=lab(x,Y+450,bw+80,f'{nm}<br>{kn} nodi',INK,22,800,'center')
for cat,f_,c,t in (('D',4,GREEN,'onde 0,3 m'),('C',6,BLUE,'onde 2 m'),('B',8,PURPLE,'onde 4 m')):
    x=128+x0+(f_+1)*bw+6; lbl+=lab(x,Y+30,190,f'Cat. {cat} fino a forza {f_} · {t}',c,22,900)
bottom=f'<div style="position:absolute; left:128px; top:870px; width:1664px; display:flex; gap:28px">'+''.join(f'<p style="font-size:24px; font-weight:800; color:{INK}; background:{bg}; padding:10px 18px; border-radius:18px">{t}</p>' for t,bg in [('Vento: scala Beaufort da 0 a 12',SEA_T),('Mare: scala Douglas da 0 a 9',BLUE_T),('La burrasca è una forza del vento',CORAL_T)])+'</div>'
sec('beaufort', head('Meteorologia · la forza del vento','Quanto soffia: la scala Beaufort'), pinned=svgp(128,Y,W2,H2,b,'Grafico a barre della scala Beaufort da 0 a 12, con i limiti delle categorie di progettazione CE D, C e B')+lbl+bottom,
 notes='Quiz 1.6.1-1 (scala Beaufort), -40 (vento 0-12, mare 0-9), 1.6.2-24 (burrasca = forza del vento), 1.8.1-116, -117, -119 (categorie di progettazione: B fino a forza 8 e onde 4 m, C forza 6 e onde 2 m, D forza 4 e onde 0,3 m, occasionalmente 0,5), 1.8.1-12 e -61 (i limiti delle unità CE dipendono da vento e onde). La categoria A va oltre la forza 8 e i 4 m. Nodi secondo la scala Beaufort dell\'Organizzazione meteorologica mondiale.')

quiz_slide('quiz1','Quiz 1 · Pressione e venti',['1.6.1-19','1.6.1-28','1.6.3-7'],False)
quiz_slide('quiz1r','Quiz 1 · Le risposte',['1.6.1-19','1.6.1-28','1.6.3-7'],True)

# ============ FRONTI ============
def front(kind):
    s=f'<rect x="0" y="0" width="300" height="160" fill="#F4FAFC"/><path d="M20 110 Q150 60 280 100" fill="none" stroke="{ {"freddo":BLUE,"caldo":LRED,"occluso":PURPLE,"staz":NAVY}[kind] }" stroke-width="6"/>'
    pts=[(70,93),(130,82),(190,83),(245,91)]
    for i,(x,y) in enumerate(pts):
        if kind=='freddo' or (kind=='staz' and i%2==0): s+=f'<path d="M{x-14} {y+4} L{x+14} {y-4} L{x} {y-26} Z" fill="{BLUE}"/>'
        if kind=='caldo' or (kind=='staz' and i%2==1): s+=f'<path d="M{x-14} {y+4} A14 14 0 0 1 {x+14} {y-4} Z" fill="{LRED}"/>'
        if kind=='occluso': s+=(f'<path d="M{x-14} {y+4} L{x+14} {y-4} L{x} {y-26} Z" fill="{PURPLE}"/>' if i%2==0 else f'<path d="M{x-14} {y+4} A14 14 0 0 1 {x+14} {y-4} Z" fill="{PURPLE}"/>')
    return s
FR=[(front('freddo'),'Fronte freddo','L\'aria fredda spinge sotto la calda: pressione che sale di colpo, cumulonembi, raffiche e temporali.'),
    (front('caldo'),'Fronte caldo','L\'aria calda scivola sulla fredda: prima i cirri, la pressione cala, piogge leggere e continue.'),
    (front('occluso'),'Fronte occluso','Il fronte freddo raggiunge il caldo e si sovrappone.'),
    (front('staz'),'Fronte stazionario','Nessuna delle due masse avanza: tempo brutto che dura.')]
cc=''.join(card(svgi(300,160,s,f'Simbolo del {t.lower()} sulla carta',dw=300,dh=160,pan=False)+h3(t,28)+p(d,23),None,22,10) for s,t,d in FR)
sec('fronti', head('Meteorologia · le masse d\'aria','I fronti')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Un fronte è la superficie di contatto tra due masse d\'aria diverse.',SEA,36),
 notes='Quiz 1.6.1-15 e 1.6.2-27 (fronte), -16 e 1.6.2-50 (fronte caldo, piogge leggere), -17, -41, 1.6.2-32, -49, -51 (fronte freddo: pressione in brusco aumento, cumulonembi, raffiche), -18 e 1.6.2-35 (stazionario), -11 (occluso), 1.6.2-48 (prima del fronte caldo la pressione cala), 1.6.2-10…-13 (simboli in figura), 1.6.2-9 (carte al suolo e in quota).')

# ============ NUBI ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="540" width="1092" height="80" fill="{WATER}" fill-opacity="0.45"/>'
b+=''.join(f'<path d="M{x} {y} q40 -20 90 -6 q30 8 60 -10" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>' for x,y in ((80,90),(260,70),(440,100)))
b+=f'<rect x="560" y="140" width="460" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.85"/>'
b+=cloudp(150,400,1.2)+cloudp(330,420,1.0)
b+=f'<path d="M700 520 L700 300 Q690 230 760 210 L960 190 Q1000 200 940 230 Q880 250 880 300 L880 520 Z" fill="#6B7F95"/>'+cloudp(790,500,1.6,'#6B7F95')+f'<path d="M740 530 l-14 40 M790 530 l-14 40 M840 530 l-14 40" stroke="{BLUE}" stroke-width="4"/>'
b+=f'<path d="M820 400 l-24 50 h20 l-20 50" fill="none" stroke="{SUN}" stroke-width="6" stroke-linejoin="round"/>'
b+=f'<rect x="0" y="505" width="520" height="40" fill="#FFFFFF" fill-opacity="0.75"/>'
lbl=lab(X+60,Y+120,300,'Cirri',NAVY,26,900)+lab(X+600,Y+100,380,'Cirrostrati',NAVY,26,900)+lab(X+120,Y+300,300,'Cumuli',NAVY,26,900)+lab(X+890,Y+300,200,'Cumulonembo',NAVY,26,900)+lab(X+40,Y+470,300,'Nebbia',NAVY,26,900)
txt=term('Cirri','Le nubi più alte, bianche e fibrose: bel tempo se la pressione è stabile. Se si addensano in cirrostrati e la pressione cala, peggiora.')+term('Cumuli e cumulonembi','Nubi a sviluppo verticale. Il cumulonembo porta rovesci, temporali e grandine: più è alto, più è violento.')+term('Nebbia e foschia','Vapore condensato vicino al mare: è nebbia se la visibilità scende sotto 1 km.')
sec('nubi', head('Meteorologia · il cielo','Le nubi'), pinned=svgp(X,Y,W,Hh,b,'Cielo con cirri in alto, un velo di cirrostrati, cumuli bassi, un cumulonembo scuro con fulmine e pioggia, e un banco di nebbia sul mare')+lbl+pcol(txt),
 notes='Quiz 1.6.1-13 e 1.6.2-25 (cirri), 1.6.2-4 e -7 (cirri che si addensano, pressione che cala: peggioramento), -14, 1.6.2-26, -28, -31 (cumuli e cumulonembi, temporali), -4 e -7 (vapore acqueo, nebbia), 1.6.2-52 (nebbia sotto 1 km), 1.6.2-33 e -34 (aria instabile: rovesci e buona visibilità), 1.6.2-3, -5, -6 (segni di miglioramento), -39 (orizzonte chiaro e calma: bel tempo).')
X=700

# ============ ONDE ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
wave='M0 330 '+' '.join(f'L{x} {330-90*math.sin(2*math.pi*(x-40)/420):.1f}' for x in range(0,1093,12))
b+=f'<path d="{wave} L1092 620 L0 620 Z" fill="{WATER}" fill-opacity="0.45"/><path d="{wave}" fill="none" stroke="{SEA}" stroke-width="5"/>'
c1=40+105; c2=c1+420; tr=c1+210
b+=dim(c1,200,c2,200,NAVY)+dash(c1,240,c1,215,NAVY,2)+dash(c2,240,c2,215,NAVY,2)
b+=dim(tr+150,240,tr+150,420,CORAL)+dash(c1+420-60,240,tr+170,240,CORAL,2)+dash(tr-30,420,tr+170,420,CORAL,2)
b+=''.join(arrow(x,90,x+120,90,GREY,7,22) for x in (80,380,680))+dpath('M60 585 L1020 585',PURPLE,4)+arrow(900,585,1020,585,PURPLE,4,16)
lbl=lab(X+c1+60,Y+150,420,'lunghezza: da cresta a cresta',NAVY,24,900)+lab(X+tr+180,Y+435,400,'↕ altezza: dalla cresta al cavo','#FFFFFF',24,900,bg=f'linear-gradient(135deg,{CORAL},#FFB36B)')+lab(X+80,Y+120,260,'vento',SOFT,24,900)+lab(X+60,Y+505,660,'⟷ fetch: il tratto di mare su cui soffia il vento','#FFFFFF',24,900,bg=f'linear-gradient(135deg,{PURPLE},{BLUE})')
txt=term('Da dove nasce','Il moto ondoso lo fa il vento: più forte, più a lungo, su un fetch più lungo, più grandi le onde.')+term('Quando frange','Se l\'onda è troppo ripida (altezza oltre 1/7 della lunghezza) o il fondale è meno del doppio dell\'altezza. Vento contro corrente: onda ripida.')+term('Mare vivo, lungo, morto','Vivo: vento sul posto. Lungo: onde arrivate da lontano. Morto: resta dopo che il vento è calato.')
sec('onde', head('Meteorologia · il mare','Le onde')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Profilo di un\'onda con la lunghezza da cresta a cresta, l\'altezza dalla cresta al cavo, il vento e il fetch')+lbl,
 notes='Quiz 1.6.2-39 (il vento provoca il moto ondoso), -40 (lunghezza), -41 (altezza), -29 (fetch minimo), -42 e -43 (quando frange), 1.6.1-30 (vento contro corrente: onda ripida), 1.6.2-44, -45, -46 (mare vivo, lungo, vecchio o morto), 1.6.1-9 (correnti, onde e maree), -10 e -22 (maree), -42, -43, -44 (correnti marine e di marea).')

# ============ METEOMAR ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
b+=f'<rect x="250" y="130" width="600" height="380" rx="46" fill="{NAVY}"/><path d="M780 130 V20" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
b+=f'<rect x="300" y="180" width="330" height="170" rx="16" fill="#BFE6D9"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#2B4A6B"/>' for x in range(680,820,30) for y in range(190,350,30))
b+=''.join(f'<rect x="{300+i*84}" y="390" width="66" height="60" rx="14" fill="#2B4A6B"/>' for i in range(4))+f'<rect x="636" y="390" width="160" height="60" rx="14" fill="{LRED}"/>'
b+=''.join(f'<path d="M{880+i*30} {110-i*10} q20 30 0 60" fill="none" stroke="{SEA}" stroke-width="6" stroke-linecap="round"/>' for i in range(3))
lbl=big(X+300,Y+205,330,'CH 68',NAVY,80)+lab(X+636,Y+402,160,'DISTRESS',('#FFFFFF'),22,900,'center')+lab(X+310,Y+300,310,'Meteomar continuo',NAVY,24,900,'center')
txt=term('Meteomar','Trasmesso di continuo sul canale VHF 68 dalle stazioni radio costiere. Quello delle 12 UTC vale fino alle 00 UTC; la «tendenza» guarda alle 12 ore dopo.')+term('Avvisi di burrasca','Burrasca o tempesta in corso o in arrivo: precedenza assoluta, preceduti da «Sécurité».')+term('Chi li fa','Il Centro nazionale di meteorologia e climatologia aeronautica. Orari e canali su «Radioservizi».')
sec('meteomar', head('Meteorologia · le previsioni','Bollettini e segni del tempo'), pinned=svgp(X,Y,W,Hh,b,'Apparato VHF acceso sul canale 68 che trasmette il bollettino Meteomar')+lbl+pcol(txt),
 notes='Quiz 1.6.2-1 (Centro nazionale di meteorologia e climatologia aeronautica), -2, -14, -15, -21 (avvisi e avvisi di burrasca, Sécurité, precedenza), -16 (contenuto del Meteomar), -17 (canale 68 di continuo), -18 (emesso alle 12 UTC, vale fino alle 00 UTC), -19 e -22 (tendenza: 12 ore successive), -20 (stazioni radio costiere), -23 (Radioservizi). Previsioni locali: -3…-8 (segni premonitori), 1.6.1-39, 1.6.2-30 (venti freddi da N: pressione in aumento), -36 e -37 (vento teso, a raffiche), -38 (foehn).')
X=700

quiz_slide('quiz2','Quiz 2 · Fronti, nubi e bollettini',['1.6.2-17','1.6.1-41','1.6.2-31'],False)
quiz_slide('quiz2r','Quiz 2 · Le risposte',['1.6.2-17','1.6.1-41','1.6.2-31'],True)

# ============ UNITÀ ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
sx=25; x0=46
seg=[(0,10,SEA),(10,24,PURPLE),(24,40,CORAL)]
for a,e,c in seg: b+=f'<rect x="{x0+a*sx}" y="470" width="{(e-a)*sx}" height="40" fill="{c}"/>'
b+=''.join(line(x0+m*sx,512,x0+m*sx,528,NAVY,3) for m in range(0,41,2))
b+=profile(x0+1*sx,420,8*sx)+profile(x0+10.5*sx,420,13*sx)+profile(x0+24.5*sx,420,15*sx,fly=True)
lbl=lab(X+x0,Y+530,60,'0',NAVY,24,900)+lab(X+x0+10*sx-30,Y+530,60,'10 m',NAVY,24,900,'center')+lab(X+x0+24*sx-30,Y+530,60,'24 m',NAVY,24,900,'center')
lbl+=lab(X+x0+10,Y+476,300,'natanti',('#FFFFFF'),24,900)+lab(X+x0+10*sx+10,Y+476,400,'imbarcazioni',('#FFFFFF'),24,900)+lab(X+x0+24*sx+10,Y+476,200,'navi',('#FFFFFF'),24,900)
txt=term('Natanti','Fino a 10 m, non iscritti: niente licenza né bandiera. Se si iscrivono, seguono le regole delle imbarcazioni.')+term('Imbarcazioni','Da 10 a 24 m, iscritte all\'ATCN: sigla di 4 lettere, 4 numeri e la D. Espongono la bandiera nazionale.')+term('Navi da diporto','Oltre i 24 m.')+term('Marcatura CE','Unità da 2,5 a 24 m: il costruttore dichiara la categoria di progettazione.')
sec('unita', head('Normativa · la classificazione','Natanti, imbarcazioni, navi')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Righello delle lunghezze: fino a 10 metri i natanti, da 10 a 24 metri le imbarcazioni, oltre 24 metri le navi, con una barca per ogni fascia')+lbl,
 notes='Quiz 1.8.1-56 (classificazione per lunghezza fuori tutto), -57 (motore di 9 m: natante), -113 (natante: non iscritto), -21 e -86 (natante iscritto: regime delle imbarcazioni), -13, -24, -77 (iscrizione all\'ATCN tramite qualsiasi STED), -26 (sigla: 4 lettere, 4 numeri, D), -23, -60, -63 (bandiera: imbarcazioni e navi sì, natanti no), -15 (posizione della bandiera), -17 (il nome non è obbligatorio), -69 (marcatura CE da 2,5 a 24 m), -25, -88 (definizioni), -20 e -59 (navigazione e acque interne), -14 (linee di base).')

# ============ DOCUMENTI ============
def doc(c,icon):
    s=f'<rect x="0" y="0" width="300" height="190" fill="#F4FAFC"/><rect x="92" y="14" width="116" height="160" rx="10" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><rect x="92" y="14" width="116" height="34" rx="10" fill="{c}"/>'
    s+=''.join(f'<rect x="108" y="{62+i*18}" width="{84-(i%2)*24}" height="7" rx="3" fill="#C9D3DD"/>' for i in range(5))
    return s+f'<g transform="translate(196 150)">{icon}</g>'
stamp=lambda c: f'<circle r="26" fill="{c}" stroke="#FFFFFF" stroke-width="4"/><path d="M-11 0 l7 8 l15 -16" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
DC=[(doc(BLUE,stamp(BLUE)),'Licenza di navigazione','Per imbarcazioni e navi: riporta le caratteristiche. Vale finché non cambiano.'),
    (doc(GREEN,stamp(GREEN)),'Certificato di sicurezza','Imbarcazioni e navi: attesta la navigabilità. È quello che si convalida.'),
    (doc(PURPLE,stamp(PURPLE)),'Dichiarazione di potenza','Natanti e imbarcazioni con fuoribordo: le caratteristiche del motore.'),
    (doc(CORAL,stamp(CORAL)),'Assicurazione RC','Obbligatoria per ogni motore, anche fuoribordo e amovibile.')]
cc=''.join(card(svgi(300,190,s,f'Documento: {t}',dw=300,dh=190,pan=False)+h3(t,28)+p(d,23),None,22,10) for s,t,d in DC)
sec('documenti', head('Normativa · a bordo','I documenti di bordo')+f'<div style="display:flex; gap:20px">{cc}</div>'+note('Natante CE: le persone trasportabili sono sul certificato di omologazione. Noleggio e locazione: il contratto sta a bordo.',PURPLE,34),
 notes='Quiz 1.8.1-99 e -66 (licenza di navigazione), -48 e -100 (certificato di sicurezza), -49, -98, -115 (dichiarazione di potenza: natanti e imbarcazioni con fuoribordo), -31, -32, -33, -95 (assicurazione RC per ogni motore), -47 e -76 (documenti in originale o copia), -50 (autorizzazione alla navigazione temporanea), -73 (manuale del proprietario), -105 e 1.3.3-37 (persone trasportabili: certificato di omologazione), -46 e -51 (contratti di locazione e noleggio a bordo), -81…-85 (locazione e noleggio), -103 (13 m: licenza di navigazione).')

# ============ PATENTE ============
def tile(n,t,c,bg): return f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{bg}; padding:24px; border-radius:28px"><p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,24,INK,700)}</div>'
tiles=f'<div style="display:flex; gap:20px">{tile("40,8 CV","Oltre questa potenza (30 kW), o sopra certe cilindrate, serve la patente anche entro 6 miglia.",CORAL,CORAL_T)}{tile("6 mg","Oltre le 6 miglia la patente serve sempre.",SEA,SEA_T)}{tile("10 anni","Validità fino ai 60 anni; poi 5 anni.",PURPLE,LILAC_T)}{tile("16 · 18","Senza patente: 16 anni per i natanti, 18 per le imbarcazioni.",BLUE,BLUE_T)}</div>'
rules=card(note('Sempre la patente',CORAL,36)+p('Moto d\'acqua, sci nautico, motore da 35 kW o più.',25,INK)+note('Sospensione e revoca',PURPLE,36)+p('Sospesa per ebbrezza o gravi imprudenze; revocata se mancano i requisiti morali o fisici. Senza patente: sanzione da 2.755 a 11.017 euro.',25,INK),None,28,10)
sec('patente', head('Normativa · l\'abilitazione','La patente nautica')+tiles+rules,
 notes='Quiz 1.8.1-67, -70, -101 (oltre 40,8 CV), -68 (29 kW e 750 cc entro 6 miglia: basta avere 18 anni), -94, -106, -110 (29 kW con cilindrate maggiori: serve), -111 (35 kW: sempre), -91, -107, -123 (moto d\'acqua: sempre), 1.8.2-3, -8, -14 (sci nautico), -78 (vela senza motore: 18 anni), -118 (natante entro 6 miglia: 16 anni), -87, -89, -112 (validità), -55, -97 (sospensione), -104 (revoca), -62 (delinquente abituale), -71 (ebbrezza fuori comando), -75 e -90 (patente scaduta o assente: sanzione), -114 (timoniere non abilitato con abilitato a bordo), -79 (patente entro 12 miglia), -72 (motore ausiliario fino al 20% del principale). Il quiz 1.8.1-54 è oscurato. Le soglie di cilindrata sono nel Codice della nautica (D.Lgs. 171/2005, art. 39).')

# ============ VISITE ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
yrs=24; sx=(1000-60)/yrs
def tline(y,first,c):
    s=f'<rect x="60" y="{y}" width="{sx*yrs:.0f}" height="16" rx="8" fill="#DDE6EC"/>'
    t=first; marks=[0]
    while t<=yrs: marks.append(t); t+=5
    for i in range(len(marks)-1):
        s+=f'<rect x="{60+marks[i]*sx:.0f}" y="{y}" width="{(marks[i+1]-marks[i])*sx-6:.0f}" height="16" rx="8" fill="{c}"/>'
    s+=''.join(f'<circle cx="{60+m*sx:.0f}" cy="{y+8}" r="16" fill="#FFFFFF" stroke="{c}" stroke-width="6"/>' for m in marks[1:])
    return s,marks
s1,m1=tline(190,8,PURPLE); s2,m2=tline(420,10,SEA); b+=s1+s2
lbl=lab(X+60,Y+120,700,'Categorie A e B: prima visita a 8 anni, poi ogni 5',PURPLE,26,900)+lab(X+60,Y+350,700,'Categorie C e D: prima visita a 10 anni, poi ogni 5',SEA,26,900)
lbl+=''.join(lab(X+60+m*sx-40,Y+222,80,str(m),PURPLE,24,900,'center') for m in m1[1:])+''.join(lab(X+60+m*sx-40,Y+452,80,str(m),SEA,24,900,'center') for m in m2[1:])
lbl+=lab(X+60,Y+540,600,'anni dall\'immatricolazione',SOFT,24,800)
txt=term('Chi ha il certificato','Solo imbarcazioni e navi. I natanti no.')+term('Le visite','Iniziale (stabilisce anche le persone trasportabili), periodiche, e occasionali dopo danni o modifiche a scafo e motore.')+term('Chi le fa','Un organismo tecnico notificato; l\'esito si annota sul certificato. Si convalida il certificato, non la licenza, presso uno STED.')
sec('visite', head('Normativa · la sicurezza dell\'unità','Visite e certificato di sicurezza'), pinned=svgp(X,Y,W,Hh,b,'Due linee del tempo: per le categorie A e B visite a 8, 13, 18, 23 anni; per le C e D a 10, 15, 20 anni')+lbl+pcol(txt),
 notes='Quiz 1.3.4-4 e -10 (solo imbarcazioni e navi), -14, -15, -17 (prima scadenza 8 anni per A e B, 10 per C e D), -8, -13, -16 (poi ogni 5 anni), -2, -7, -11 (visite occasionali), -3 (unità CE: periodiche e occasionali), -6 (visita iniziale: persone trasportabili), -12 (organismo tecnico), -18 (esito sul certificato), -1, -5, -9 (convalida del certificato presso gli STED), -19 (il certificato scade).')
X=700

quiz_slide('quiz3','Quiz 3 · Unità, patente e visite',['1.8.1-57','1.3.4-8','1.8.1-89'],False)
quiz_slide('quiz3r','Quiz 3 · Le risposte',['1.8.1-57','1.3.4-8','1.8.1-89'],True)

# ============ AUTORITÀ ============
lv=[('Ministero delle infrastrutture e dei trasporti',NAVY),('Comando generale delle Capitanerie di porto',BLUE),('Direzione marittima',PURPLE),('Capitaneria di porto · compartimento',SEA),('Ufficio circondariale marittimo · circondario',GREEN),('Uffici locali e delegazioni di spiaggia',CORAL)]
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
for i,(t,c) in enumerate(lv):
    y=30+i*98; w=920-i*60; x=(1092-w)/2
    b+=f'<rect x="{x:.0f}" y="{y}" width="{w}" height="70" rx="35" fill="{c}"/>'
    if i<len(lv)-1: b+=arrow(546,y+70,546,y+96,SOFT,4,12)
lbl=''.join(lab(X+(1092-(920-i*60))/2,Y+30+i*98+18,920-i*60,t,'#FFFFFF',24,900,'center') for i,(t,c) in enumerate(lv))
txt=term('Il comandante','Dirige manovra e navigazione ed è responsabile delle dotazioni. Deve soccorrere chi è in pericolo, se non mette a rischio la sua unità: chi non lo fa rischia fino a 2 anni di reclusione.')+term('Evento straordinario','Incaglio, urto, avaria grave: denuncia entro 3 giorni dall\'arrivo in porto all\'Autorità marittima; all\'estero al Consolato.')+term('Le ordinanze','Le emana il Capo del circondario: regolano rade, spiagge, porti e velocità.')
sec('autorita', head('Normativa · doveri e autorità','Il comandante e l\'autorità marittima')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Scala dell\'autorità marittima: Ministero, Comando generale delle Capitanerie, Direzione marittima, Capitaneria di porto, Ufficio circondariale, uffici locali')+lbl,
 notes='Quiz 1.8.1-3 (direzione della manovra al comandante), -120 e -125 (dotazioni), -121 (equipaggio minimo stabilito dal comandante), -7, -8, -9, -10 (soccorso e sanzione penale), -4 e -43 (urto senza fornire i dati: da 1.032 a 6.197 euro), -1, -5, -65, -74, -92, -96, -108, -109 (evento straordinario: entro 3 giorni, all\'Autorità marittima o consolare), -2 (all\'estero: consolato), -18 e -19 (ordinanze), 1.4.1-18 (Capo del circondario), -16 e -58 (ritrovamenti in spiaggia e relitti: denuncia entro 3 giorni), 1.8.2-44 (avaria con rischio di inquinamento: avvisare subito l\'autorità), 1.8.2-46 (sorveglianza delle aree marine protette). Il Corpo delle Capitanerie di porto dipende funzionalmente anche da altri ministeri (ambiente, pesca).')

# ============ AREE MARINE PROTETTE ============
X=128
cx,cy=546,320
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.25"/>'
for r,c in ((290,'#FFE9A6'),(200,'#FFC98A'),(115,'#F59A8A')): b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.35:.0f}" ry="{r}" fill="{c}" fill-opacity="0.8" stroke="{NAVY}" stroke-width="2" stroke-dasharray="8 6"/>'
b+=f'<path d="M{cx-60} {cy+10} Q{cx-50} {cy-50} {cx} {cy-40} Q{cx+70} {cy-50} {cx+64} {cy+14} Q{cx} {cy+50} {cx-60} {cy+10} Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=sailboat(cx+215,cy-90,0.6) if 'sailboat' in globals() else ''
b+=topboat(cx+300,cy+130,90,-120,'#FFFFFF',NAVY,3)
lbl=big(X+cx-30,Y+cy+40,60,'A',NAVY,60)+big(X+cx-30,Y+cy+130,60,'B',NAVY,60)+big(X+cx-30,Y+cy+215,60,'C',NAVY,60)
txt=term('Zona A','Riserva integrale: niente navigazione né ancoraggio.')+term('Zona B e C','Nella B si va a remi e a vela; il motore segue il regolamento dell\'area. Nei campi boe non si ancora e il 15% degli ormeggi è per la vela.')+term('Non inquinare','5 kg di olio usato inquinano un\'area enorme; la plastica dura fino a 450 anni. I razzi scaduti si riportano al rivenditore.')
sec('ambiente', head('Normativa · rispetto del mare','Aree marine protette e ambiente'), pinned=svgp(X,Y,W,Hh,b,'Isola al centro di un\'area marina protetta con la zona A più interna, la B e la C più esterna')+lbl+pcol(txt),
 notes='Quiz 1.8.2-53 e -54 (zone A, B, C, delimitate in carta), -49 e -55 (zona A: niente navigazione né ancoraggio), -50 e -57 (zona B: remi e vela; il resto secondo decreto e regolamento), -47 (ormeggi e campi boe), -48 (15% alla vela), -59 (nei campi boe niente ancoraggio), -45 (sanzione), -46 (sorveglianza), -51 (olio), -58 (plastica), -52 (segnali scaduti). Pesca sportiva: -36…-43 e 1.4.2 (lezione 4).')
X=700

# ============ SCI NAUTICO ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/><rect x="0" y="560" width="1092" height="60" fill="{LAND}"/>'
b+=topboat(760,220,170,180,'#FFFFFF',NAVY,4)+line(845,220,960,240,NAVY,3)
b+=dash(700,300,700,540,CORAL,4)
b+=f'<circle cx="980" cy="244" r="12" fill="{CORAL}"/><rect x="964" y="258" width="10" height="40" rx="4" fill="{NAVY}" transform="rotate(-10 969 278)"/><rect x="986" y="258" width="10" height="40" rx="4" fill="{NAVY}" transform="rotate(-10 991 278)"/>'
b+=dim(845,190,960,210,NAVY)+''.join(f'<path d="M{680-i*60} {200+i*10} q-30 10 -60 0" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>' for i in range(4))
lbl=lab(X+830,Y+140,220,'cavo di almeno 12 m',NAVY,24,900)+lab(X+716,Y+400,300,'200 m dalla spiaggia',CORAL,24,900)+lab(X+260,Y+110,400,'a bordo: chi guida e un esperto nuotatore',NAVY,22,800)
txt=term('Chi e quando','Patente sempre, anche con un natante. A bordo un\'altra persona esperta nel nuoto. Solo di giorno, con mare calmo.')+term('Dove','Oltre 200 m dalla spiaggia (100 m dalle coste a picco), lontano da bagnanti e barche. Partenza e rientro perpendicolari alla costa, al massimo a 3 nodi.')+term('Come','Cavo di almeno 12 m, al massimo 2 sciatori, specchietto convesso, gancio di traino, un salvagente per sciatore e pronto soccorso.')
sec('scinautico', head('Normativa · lo sci nautico','Lo sci nautico')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Barca che traina uno sciatore con un cavo di almeno 12 metri, lontano dalla spiaggia')+lbl,
 notes='Quiz 1.8.2-3, -8, -14 (patente), -4, -9, -26 (una persona esperta nel nuoto oltre al conduttore), -7 e -11 (di giorno, tempo favorevole, mare calmo), -10 e -17 (200 m dalla batimetrica di 1,60 m; 100 m dalle coste a picco), -6 e -19 (partenza e rientro a 3 nodi, perpendicolari alla costa), -12 (cavo di 12 m), -24 (2 sciatori), -23 (specchietto convesso), -16, -18, -21 (gancio, specchietto, invertitore e messa in folle), -20 e -1, -2, -22 (salvagente per sciatore e pronto soccorso), -5 e -25 (distanze dalle altre unità), -15 (partenza lontano da bagnanti), 1.8.1-122 (moto d\'acqua: oltre 1000 m dalla costa, 500 dalle coste a picco).')

quiz_slide('quiz4','Quiz 4 · Autorità, ambiente, sci nautico',['1.8.1-58','1.8.2-49','1.8.2-12'],False)
quiz_slide('quiz4r','Quiz 4 · Le risposte',['1.8.1-58','1.8.2-49','1.8.2-12'],True)
quiz_slide('finale1','Verifica finale · 1 di 2',['1.6.1-5','1.6.3-9','1.8.1-60'],False)
quiz_slide('finale1r','Verifica finale · 1 di 2 · risposte',['1.6.1-5','1.6.3-9','1.8.1-60'],True)
quiz_slide('finale2','Verifica finale · 2 di 2',['1.3.4-10','1.8.2-9','1.6.2-44'],False)
quiz_slide('finale2r','Verifica finale · 2 di 2 · risposte',['1.3.4-10','1.8.2-9','1.6.2-44'],True)
closing(['Pressione che cala in fretta: arriva brutto tempo; attorno alla bassa il vento gira in senso antiorario','Di giorno brezza di mare, di notte brezza di terra','Meteomar sul canale 68; gli avvisi di burrasca hanno la precedenza','Natanti fino a 10 m, imbarcazioni fino a 24, poi navi','Evento straordinario: denuncia entro 3 giorni all\'Autorità marittima'],
 'Prossima lezione · 08 · Vela','A casa: i 119 quiz di meteorologia e i 202 di normativa e ambiente.')
write_deck(OUT,'Lezione 07 · Meteorologia e normativa',
 ['cover','agenda','pressione','brezze','venti','beaufort','quiz1','quiz1r','fronti','nubi','onde','meteomar','quiz2','quiz2r',
  'unita','documenti','patente','visite','quiz3','quiz3r','autorita','ambiente','scinautico','quiz4','quiz4r','finale1','finale1r','finale2','finale2r','chiusura'],
 {"s1":{"description":"Apertura e obiettivi","start":"cover"},"s2":{"description":"Pressione, brezze, venti e scala Beaufort","start":"pressione"},
  "s3":{"description":"Fronti, nubi, onde e bollettini","start":"fronti"},"s4":{"description":"Unità, documenti, patente e visite","start":"unita"},
  "s5":{"description":"Autorità marittima, ambiente e sci nautico, verifica finale","start":"autorita"}})
