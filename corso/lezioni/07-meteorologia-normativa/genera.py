import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/lez07/project'
LAND='#F2E2B3'; LAND_S='#C9A96B'; GREY='#97A6B4'; NIGHT='#0F2238'; SKY='#DDEFF7'; LRED='#E23B3B'; ORANGE='#F28C28'; LYEL='#FFD84D'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Barometro e igrometro':'chart','Alta e bassa pressione':'cloud','I venti del Mediterraneo':'compass',
 'Quanto soffia: la scala Beaufort':'wind','Com\'è il vento':'wind','Le brezze':'wind','I fronti':'cloud','La carta sinottica':'map','Le nubi':'cloud',
 'Nebbia e foschia':'cloud','Le onde':'current','Lo stato del mare: la scala Douglas':'current','Maree e correnti':'current','Il bollettino Meteomar':'lantern',
 'Prevedere il tempo':'cloud','Natanti, imbarcazioni, navi':'hull','Marcatura CE e limiti di navigazione':'check','Linee di base e acque':'map',
 'La patente nautica':'book','I documenti di bordo':'book','Visite e certificato di sicurezza':'check','Locazione, noleggio, leasing':'book',
 'Il comandante e l\'autorità marittima':'flag','Sotto costa: le ordinanze':'map','Le sanzioni':'flag','Aree marine protette':'map',
 'Proteggere il mare':'current','Lo sci nautico':'helm','I subacquei':'flag','La pesca sportiva':'anchor'})
def pol(cx,cy,a,r): return (cx+r*math.sin(math.radians(a)), cy-r*math.cos(math.radians(a)))
def pcol(inner,w=532,gap=24,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def sterm(t,d,s=25): return f'<div style="display:flex; flex-direction:column; gap:4px">{p(t,s+2,INK,800,1.25)}{p(d,s,BODY,400,1.36)}</div>'
def lst(items,size=24,c='#34465E',gap=8,tagn='ul'): return f'<{tagn} style="font-size:{size}px; line-height:1.36; color:{c}; display:flex; flex-direction:column; gap:{gap}px">'+''.join(f'<li>{x}</li>' for x in items)+f'</{tagn}>'
def big(x,y,w,t,c,size=110,align='center'):
    return f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w}px; font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}; text-align:{align}">{t}</p>'
def cloudp(x,y,s=1,c='#FFFFFF',op=1):
    return f'<g transform="translate({x} {y}) scale({s})" opacity="{op}"><ellipse cx="0" cy="0" rx="46" ry="26" fill="{c}"/><circle cx="-26" cy="-8" r="22" fill="{c}"/><circle cx="10" cy="-22" r="28" fill="{c}"/><circle cx="36" cy="-4" r="20" fill="{c}"/></g>'
def tile(n,t,c,bg,size=64): return f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; padding:24px; border-radius:28px"><p style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,24,INK,600,1.35)}</div>'
def box(t,inner,c,bg): return f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:24px 28px; border-radius:28px; border-left:10px solid {c}">{tag(t,c)}{inner}</div>'
def table(head_,rows,widths,size=23):
    th=''.join(f'<th style="width:{w}; color:#FFFFFF; text-align:left; padding:10px 14px">{h}</th>' for h,w in zip(head_,widths))
    body=''.join(f'<tr style="background:{PAPER if k%2 else "#FFFFFF"}">'+''.join(f'<td style="padding:8px 14px; {"font-weight:800; color:"+INK if j==0 else ""}">{v}</td>' for j,v in enumerate(r))+'</tr>' for k,r in enumerate(rows))
    return f'<table style="width:100%; border-collapse:collapse; font-size:{size}px; line-height:1.3; color:{BODY}"><tr style="background:{NAVY}">{th}</tr>{body}</table>'
def chips(items):
    return '<div style="display:flex; gap:24px">'+''.join(f'<p style="font-size:24px; font-weight:800; color:{INK}; background:{bg}; padding:10px 18px; border-radius:18px">{t}</p>' for t,bg in items)+'</div>'
X,Y,W,Hh=700,290,1092,620

# ============ COVER + AGENDA ============
cover(7,'Meteorologia e Normativa','Leggere il cielo, il mare e i bollettini; conoscere unità, documenti, patente, autorità e regole del mare',
 'Lezione 7, rivista sulla scaletta della scuola. Meteorologia: barometro e igrometro, isobare e vento, il vento, le brezze, fronti, carte sinottiche, nebbia e foschia, nubi, mare e onde, maree, correnti, Meteomar e radio costiere, previsioni. Normativa: patenti, classificazione delle unità, documenti, marcatura CE e limiti, obblighi del comandante, aree marine protette, protezione dell\'ambiente, sci nautico, subacquei, pesca sportiva, locazione e noleggio, sanzioni. Dall\'All. A al DM 323/2021 anche visite e certificazioni (3b) e autorità marittima e ordinanze (8b). La meteo pesa 2 quesiti su 20, la normativa 3.', title_size=96)
import os as _os; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'esame.py')).read())
blocks=[('0:00','14′','Pressione e vento',CORAL),('0:14','10′','Fronti, nubi, nebbia',SEA),('0:24','12′','Mare e previsioni',PURPLE),('0:36','11′','Unità e patente',BLUE),
        ('0:47','9′','Documenti e noleggio',ORANGE),('0:56','10′','Comandante e regole',NAVY),('1:06','9′','Mare protetto',GREEN_S),('1:15','45′','Raccolta: 36 quiz',GREEN)]
tl=''.join(f'<div style="flex:{max(int(d[:-1]),9)}; display:flex; flex-direction:column; gap:8px; border-top:10px solid {c}; padding:14px 10px 0px 0px"><p style="font-size:22px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:22px; line-height:1.25; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=esame_box(['meteo', 'normativa'],7,extra='')
left=card(tag('Dopo questa lezione sai',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>leggere barometro, carta del tempo e Meteomar</li><li>riconoscere venti, fronti, nubi e stato del mare</li><li>sapere che patente e che documenti servono</li><li>conoscere doveri del comandante e sanzioni</li><li>rispettare bagnanti, subacquei, sciatori e aree protette</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 07 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:12px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Sette capitoli di teoria in 75 minuti, ognuno chiuso da una verifica da 2 quiz ufficiali (DD 131/2022): andare spediti sulle slide, il dettaglio è nelle note. Poi 45 minuti di raccolta quiz: 36 quiz ufficiali. Banca: elementi di meteorologia 46 quiz (1.6.1), bollettini e previsioni 53 (1.6.2), venti 21 (1.6.3), leggi e regolamenti 125 (1.8.1), sci nautico, pesca, aree protette e ambiente 59 (1.8.2), visite e certificazioni 19 (1.3.4), più i quiz su costa, subacquei e pesca della sezione 1.4.2.')

# =====================================================================
# CAPITOLO 1 · PRESSIONE E VENTO
# =====================================================================
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
cx,cy,R=330,320,230
va=lambda v: -135+(v-960)/100*270
b+=f'<circle cx="{cx}" cy="{cy}" r="{R+26}" fill="#C9A96B"/><circle cx="{cx}" cy="{cy}" r="{R+10}" fill="#FFFDF8" stroke="{NAVY}" stroke-width="4"/>'
for v,c in ((960,CORAL),(995,SUN),(1030,SEA)):
    a0=va(v); a1=va(v+35 if v<1030 else 1060); p0=pol(cx,cy,a0,R-18); p1=pol(cx,cy,a1,R-18)
    b+=f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{R-18} {R-18} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{c}" stroke-width="22" stroke-opacity="0.55"/>'
for v in range(960,1061,5):
    o=pol(cx,cy,va(v),R-4); i=pol(cx,cy,va(v),R-(34 if v%20==0 else 22)); b+=line(o[0],o[1],i[0],i[1],NAVY,4 if v%20==0 else 2)
for v in range(960,1061,20):
    t=pol(cx,cy,va(v),R-62); b+=f'<text x="{t[0]:.0f}" y="{t[1]+9:.0f}" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700" fill="{NAVY}">{v}</text>'
n0=pol(cx,cy,va(1013.2),R-40); n1=pol(cx,cy,va(1013.2)+180,40)
b+=line(n1[0],n1[1],n0[0],n0[1],CORAL,8)+f'<circle cx="{cx}" cy="{cy}" r="16" fill="{NAVY}"/>'
b+=f'<text x="{cx}" y="{cy+95}" text-anchor="middle" font-family="Arial" font-size="26" font-weight="900" fill="{NAVY}">hPa</text>'
tx=820; b+=f'<rect x="{tx-90}" y="540" width="180" height="40" rx="10" fill="#8A97A6"/><rect x="{tx-20}" y="40" width="40" height="520" rx="20" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/><rect x="{tx-12}" y="120" width="24" height="440" rx="10" fill="#8A97A6"/>'
b+=dim(tx+60,120,tx+60,560,CORAL)
lbl=lab(X+tx-170,Y+40,140,'vuoto',SOFT,22,800,'right')+lab(X+tx+76,Y+300,200,'760 mm di mercurio',CORAL,24,900)+lab(X+tx-120,Y+585,240,'Torricelli',NAVY,22,900,'center')
lbl+=lab(X+60,Y+30,180,'brutto',CORAL,22,900,'center')+lab(X+250,Y+2,160,'variabile',SUN,22,900,'center')+lab(X+420,Y+30,180,'bello',SEA,22,900,'center')
txt=sterm('Barometro','Misura la pressione dell\'aria in hPa. Al livello del mare la media è 1013,2 hPa: sopra è alta, sotto è bassa.')+sterm('Il tubo di Torricelli','La pressione media regge una colonna di 760 mm di mercurio: 760 mm = 1013,2 hPa.')+sterm('Igrometro e anemometro','L\'igrometro misura l\'umidità relativa, in percentuale. L\'anemometro misura la velocità del vento.')+sterm('Conta la tendenza','Più del valore conta come cambia: se scende in fretta arriva brutto tempo.')
sec('strumenti', head('Meteorologia · gli strumenti','Barometro e igrometro')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Barometro aneroide con la lancetta su 1013 hPa e il tubo di Torricelli con 760 mm di mercurio')+lbl,
 notes='Materiale della scuola: barometro e igrometro. Quiz 1.6.1-34 e -35 (il barometro misura la pressione), -5 (hPa), 1.6.2-47 e 1.6.1-38 (1013,2 hPa normale; il codice 1.6.1-38 è doppio nella banca), -36 (igrometro: umidità relativa), -23 (anemometro: velocità del vento), -12 (conta la tendenza della pressione). Torricelli: 760 mm Hg = 1013,2 hPa = 1 atmosfera.')

b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
L=(330,320); Hp=(820,300)
b+=''.join(f'<ellipse cx="{L[0]}" cy="{L[1]}" rx="{40+i*42}" ry="{32+i*36}" fill="none" stroke="{BLUE}" stroke-width="3"/>' for i in range(6))
b+=''.join(f'<ellipse cx="{Hp[0]}" cy="{Hp[1]}" rx="{70+i*90}" ry="{56+i*80}" fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="10 8"/>' for i in range(3))
def windarr(c0,r,phis,ccw,inward,col_):
    s=''
    for ph in phis:
        f=math.radians(ph); px=c0[0]+r*math.cos(f); py=c0[1]+r*0.85*math.sin(f)
        tx_,ty_=(math.sin(f),-math.cos(f)) if ccw else (-math.sin(f),math.cos(f))
        ox,oy=(-math.cos(f),-math.sin(f)) if inward else (math.cos(f),math.sin(f))
        dx=tx_*0.9+ox*0.45; dy=ty_*0.9+oy*0.45; n=math.hypot(dx,dy); dx/=n; dy/=n
        s+=arrow(px-dx*35,py-dy*35,px+dx*35,py+dy*35,col_,6,18)
    return s
b+=windarr(L,190,range(0,360,45),True,True,NAVY)+windarr(Hp,190,range(20,360,60),False,False,SOFT)
lbl=big(X+L[0]-40,Y+L[1]-45,80,'B',BLUE,90)+big(X+Hp[0]-40,Y+Hp[1]-45,80,'A',CORAL,90)
lbl+=lab(X+L[0]-240,Y+560,480,'isobare fitte: vento forte',BLUE,24,900,'center')+lab(X+Hp[0]-210,Y+560,420,'isobare larghe: vento debole',CORAL,24,900,'center')
txt=term('Isobare','Linee che uniscono i punti con la stessa pressione.')+term('Gradiente barico','La differenza di pressione tra due zone: più le isobare sono vicine, più forte è il vento.')+term('Il giro del vento','Nel nostro emisfero il vento gira in senso antiorario attorno alla bassa (ciclone), entrando verso il centro; in senso orario attorno all\'alta.')+term('Perché soffia','Il vento nasce da differenze di temperatura e di pressione: l\'aria calda, più leggera, sale.')
sec('pressione', head('Meteorologia · isobare e vento','Alta e bassa pressione')+col(txt), pinned=svgp(X,Y,W,Hh,b,'Carta del tempo: una bassa pressione con isobare fitte e il vento che gira in senso antiorario verso il centro; un\'alta pressione con isobare larghe e il vento in senso orario verso l\'esterno')+lbl,
 notes='Quiz 1.6.1-6 (isobare), -19 (senso antiorario attorno alla bassa nel nostro emisfero), -20 e 1.6.2-53 (gradiente barico, isobare vicine = vento forte), -25 (il vento nasce da differenze di temperatura e pressione), -38 (l\'aria calda è più leggera), -8 (definizione di vento: spostamento quasi orizzontale, con direzione e velocità). Sulle carte italiane B = bassa, A = alta (in inglese L e H).')

X=128
cx,cy=546,320
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
for k,c in enumerate(['#FFE7A8','#CFEFF2','#FFD5C7','#E0D7FA']):
    a0,a1=k*90,(k+1)*90; p0=pol(cx,cy,a0,200); p1=pol(cx,cy,a1,200)
    b+=f'<path d="M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A200 200 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{c}"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="200" fill="none" stroke="{NAVY}" stroke-width="4"/>'
for a,t in ((45,'I'),(135,'II'),(225,'III'),(315,'IV')):
    q_=pol(cx,cy,a,150); b+=f'<text x="{q_[0]:.0f}" y="{q_[1]+12:.0f}" text-anchor="middle" font-family="Arial" font-size="34" font-weight="900" fill="{NAVY}" fill-opacity="0.4">{t}</text>'
for a in range(0,360,45):
    o=pol(cx,cy,a,196); i=pol(cx,cy,a,70); b+=arrow(o[0],o[1],i[0],i[1],NAVY if a%90==0 else SOFT,6,20)
b+=f'<circle cx="{cx}" cy="{cy}" r="16" fill="{SUN}"/>'
names=[(0,'Tramontana','N'),(45,'Grecale','NE'),(90,'Levante','E'),(135,'Scirocco','SE'),(180,'Ostro','S'),(225,'Libeccio','SW'),(270,'Ponente','W'),(315,'Maestrale','NW')]
lbl=''
for a,nm,d in names:
    x,y=pol(cx,cy,a,258 if a%180==0 else 290); lbl+=lab(X+x-110,Y+y-18,220,f'{nm} · {d}',NAVY if a%90==0 else PURPLE,24,900,'center')
txt=sterm('Il nome dice da dove viene','Lo Scirocco viene da Sud-Est (135°), il Ponente da Ovest (270°). Ostro e Mezzogiorno sono lo stesso vento.')+f'<div style="display:flex; flex-direction:column; gap:6px">{p("I quadranti",27,INK,800,1.25)}<div style="display:flex; gap:12px; align-items:baseline"><p style="width:56px; flex:none; font-family:{H}; font-size:28px; font-weight:700; color:{PURPLE}">I</p>{p("Tramontana, Grecale, Levante",24,BODY,600,1.3)}</div><div style="display:flex; gap:12px; align-items:baseline"><p style="width:56px; flex:none; font-family:{H}; font-size:28px; font-weight:700; color:{PURPLE}">II</p>{p("Levante, Scirocco, Mezzogiorno",24,BODY,600,1.3)}</div><div style="display:flex; gap:12px; align-items:baseline"><p style="width:56px; flex:none; font-family:{H}; font-size:28px; font-weight:700; color:{PURPLE}">III</p>{p("Mezzogiorno, Libeccio, Ponente",24,BODY,600,1.3)}</div><div style="display:flex; gap:12px; align-items:baseline"><p style="width:56px; flex:none; font-family:{H}; font-size:28px; font-weight:700; color:{PURPLE}">IV</p>{p("Ponente, Maestrale, Tramontana",24,BODY,600,1.3)}</div></div>'+sterm('Venti di traversia','Soffiano dal largo verso la costa: per una costa esposta a Sud-Est sono quelli del II quadrante. Lì non c\'è ridosso.')
sec('venti', head('Meteorologia · il vento','I venti del Mediterraneo'), pinned=svgp(X,Y,W,Hh,b,'Rosa dei venti con i quattro quadranti numerati e le frecce che arrivano da Tramontana, Grecale, Levante, Scirocco, Ostro, Libeccio, Ponente e Maestrale')+lbl+pcol(txt,gap=20),
 notes='Materiale della scuola: il vento. Quiz 1.6.3-1…-4 (venti dei quadranti), -5 (la rosa dei venti indica la direzione di provenienza), -6…-19 (singoli venti e gradi: Scirocco 135°, Ponente 270°, Ostro 180°, Maestrale da NW, Grecale da NE, Libeccio da SW), -15 (Ostro = Mezzogiorno), -20 (i venti intercardinali prendono il nome dalla provenienza). Il vento si indica «da», la corrente «verso» (lezione 4). Venti di traversia: il ridosso si cerca sottovento alla costa.')
X=700

BF=[(0,'calma','<1'),(1,'bava di vento','1-3'),(2,'brezza leggera','4-6'),(3,'brezza tesa','7-10'),(4,'vento moderato','11-16'),(5,'vento teso','17-21'),(6,'vento fresco','22-27'),(7,'vento forte','28-33'),(8,'burrasca','34-40'),(9,'burrasca forte','41-47'),(10,'tempesta','48-55'),(11,'fortunale','56-63'),(12,'uragano','64 e oltre')]
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
for f_ in range(13):
    nm=BF[f_][1]; kn=BF[f_][2]; x=128+x0+f_*bw-6; lbl+=lab(x,Y+448+(54 if f_%2 else 0),bw+12,f'{nm}<br>{kn} kn',INK,19,800,'center')
for cat,f_,c,t in (('D',4,GREEN,'onde 0,3 m'),('C',6,BLUE,'onde 2 m'),('B',8,PURPLE,'onde 4 m')):
    x=128+x0+(f_+1)*bw+6; lbl+=lab(x,Y+30,190,f'Cat. {cat} fino a forza {f_} · {t}',c,22,900)
bottom=f'<div style="position:absolute; left:128px; top:880px; width:1664px">'+chips([('Vento: scala Beaufort da 0 a 12',SEA_T),('Mare: scala Douglas da 0 a 9',BLUE_T),('La burrasca è una forza del vento',CORAL_T)])+'</div>'
sec('beaufort', head('Meteorologia · la forza del vento','Quanto soffia: la scala Beaufort'), pinned=svgp(128,Y,W2,H2,b,'Grafico a barre della scala Beaufort da 0 a 12 con nomi e nodi, e i limiti delle categorie di progettazione CE D, C e B')+lbl+bottom,
 notes='Nomi della scala come nel materiale della scuola (forza 8 burrasca, 9 burrasca forte, 10 tempesta, 11 fortunale, 12 uragano); la tabella dell\'Organizzazione meteorologica mondiale in italiano usa anche «burrasca moderata» per la 8 e «tempesta violenta» per la 11. Quiz 1.6.1-1 (scala Beaufort), -40 (vento 0-12, mare 0-9), 1.6.2-24 (burrasca = forza del vento), 1.8.1-116, -117, -119 (categorie di progettazione: B fino a forza 8 e onde 4 m, C forza 6 e onde 2 m, D forza 4 e onde 0,3 m, occasionalmente 0,5), 1.8.1-12 e -61 (i limiti delle unità CE dipendono da vento e onde).')

b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
def chart_(x,kind):
    s=f'<rect x="{x}" y="20" width="330" height="200" rx="18" fill="#FFFFFF" stroke="#DDE6EC" stroke-width="3"/>'+line(x+24,190,x+310,190,SOFT,3)+line(x+24,190,x+24,40,SOFT,3)
    if kind=='teso': d=f'M{x+30} 120 L{x+305} 120'
    elif kind=='raffiche':
        pts=[(x+30,130)]
        for k in range(5):
            bx=x+60+k*50; pts+=[(bx,130),(bx+8,62),(bx+16,130)]
        pts.append((x+305,130)); d='M'+' L'.join(f'{a} {c}' for a,c in pts)
    else:
        ys=[140,80,150,60,120,170,70,130,90,160,110]; d='M'+' L'.join(f'{x+30+k*27.5:.0f} {y}' for k,y in enumerate(ys))
    s+=f'<path d="{d}" fill="none" stroke="{CORAL if kind!="teso" else SEA}" stroke-width="6" stroke-linejoin="round"/>'
    return s
b+=chart_(20,'teso')+chart_(381,'raffiche')+chart_(742,'groppo')
mx=546
b+=f'<path d="M0 620 L250 620 L{mx} 330 L842 620 L1092 620 Z" fill="#B7A27A"/><path d="M{mx-70} 400 L{mx} 330 L{mx+70} 400 L{mx+35} 390 L{mx} 410 L{mx-30} 392 Z" fill="#FFFFFF"/>'
b+=f'<rect x="0" y="600" width="1092" height="20" fill="{WATER}" fill-opacity="0.5"/>'
b+=cloudp(mx-150,350,1.3,'#8A97A6')+''.join(f'<path d="M{mx-200+k*28} 380 l-10 30" stroke="{BLUE}" stroke-width="4"/>' for k in range(5))
b+=arrow(40,575,240,565,BLUE,7,22)+arrow(270,545,mx-40,345,BLUE,7,22)+arrow(mx+40,345,830,560,ORANGE,7,22)+arrow(860,580,1060,588,ORANGE,7,22)
lbl=lab(X+20,Y+232,330,'teso: costante','#FFFFFF',22,900,'center',bg=SEA)+lab(X+381,Y+232,330,'a raffiche: picchi brevi','#FFFFFF',22,900,'center',bg=CORAL)+lab(X+742,Y+232,330,'groppo: cambia tutto','#FFFFFF',22,900,'center',bg=CORAL)
lbl+=lab(X+20,Y+400,240,'Stau: l\'aria sale, si raffredda, nubi e pioggia',BLUE,22,900)+lab(X+830,Y+400,250,'Foehn: l\'aria scende, si scalda e asciuga',ORANGE,22,900)
txt=sterm('Teso','Direzione e velocità medie costanti per un certo tempo.',24)+sterm('A raffiche','Direzione costante, ma la velocità ha picchi di almeno 10 nodi sopra la media, che durano meno di un minuto.',24)+sterm('Groppo','Direzione e velocità cambiano in fretta: arriva con i temporali.',24)+sterm('Foehn','Vento che scende per forza lungo il versante sottovento di un rilievo, caldo e secco.',24)+sterm('Alisei','Venti permanenti tra i tropici, 13-18 nodi, più forti nei mesi freddi.',24)
sec('vento2', head('Meteorologia · il vento','Com\'è il vento')+col(txt,540,14), pinned=svgp(X,Y,W,Hh,b,'Tre grafici della velocità del vento nel tempo: teso, a raffiche, a groppo; sotto, una montagna con lo Stau sul versante sopravento e il Foehn su quello sottovento')+lbl,
 notes='Materiale della scuola: il vento 2. Quiz 1.6.2-36 (vento teso), -37 (raffiche: almeno 10 nodi oltre la media, meno di un minuto), -38 (Foehn: scende lungo il versante sottovento), 1.6.1-21 (alisei: permanenti, 13-18 nodi, più forti nei mesi freddi). Stau: sul versante sopravento l\'aria sale, si raffredda, condensa e piove; scendendo dall\'altra parte si riscalda ed è secca.')

def breeze(day):
    bg=SKY if day else '#23385A'; sea=WATER; s=f'<rect x="0" y="0" width="560" height="300" fill="{bg}"/>'
    s+=f'<rect x="0" y="220" width="300" height="80" fill="{sea}" fill-opacity="0.5"/><path d="M300 220 L560 200 L560 300 L300 300 Z" fill="{LAND}"/>'
    s+=(f'<circle cx="470" cy="60" r="34" fill="{SUN}"/>' if day else f'<circle cx="90" cy="60" r="28" fill="#F4F1DE"/><circle cx="104" cy="52" r="24" fill="#23385A"/>')
    if day: s+=arrow(120,190,420,180,NAVY,8,24)+dpath('M430 110 Q280 80 130 110',GREY,4)+arrow(420,150,440,110,GREY,4,14)
    else: s+=arrow(430,180,140,190,'#DDE6EC',6,20)+dpath('M140 110 Q280 90 420 110',GREY,4)
    return s
bc=card(svgi(560,300,breeze(True),'Di giorno la terra si scalda e la brezza soffia dal mare verso terra',dw=560,dh=300,pan=False)+h3('Di giorno: brezza di mare',30)+p('La terra si scalda <b>più in fretta</b> del mare: l\'aria sale sulla terra e dal mare arriva aria fresca. È la brezza più intensa.',25),None,24,10)
nc=card(svgi(560,300,breeze(False),'Di notte la terra si raffredda e la brezza soffia da terra verso il mare',dw=560,dh=300,pan=False)+h3('Di notte: brezza di terra',30)+p('La terra si raffredda <b>più in fretta</b> del mare: l\'aria scende da terra verso il mare. È più debole.',25),None,24,10)
sec('brezze', head('Meteorologia · il vento locale','Le brezze')+f'<div style="display:flex; gap:28px">{bc}{nc}</div>'+note('Nascono dalla differenza di temperatura tra terra e mare: servono giornate con forte escursione diurna (massima meno minima).',SEA,32),
 notes='Materiale della scuola: le brezze. Quiz 1.6.1-24, -26, -28, -37 (brezza di mare di giorno: la terra si scalda prima; nasce dalla diversa temperatura tra due zone), -27, -29, -31, -32, -33 (brezza di terra di notte: la terra si raffredda prima), -2 (la diurna è più intensa), -3 (escursione diurna). In estate la brezza di mare arriva a fine mattinata e cala al tramonto: attenzione al rientro.')

# =====================================================================
# CAPITOLO 2 · FRONTI, NUBI, NEBBIA
# =====================================================================
def section_front(cold):
    s=f'<rect x="0" y="0" width="600" height="260" fill="{SKY}"/><rect x="0" y="236" width="600" height="24" fill="{WATER}" fill-opacity="0.45"/>'
    if cold:
        s+=f'<path d="M0 236 L0 70 Q140 70 240 236 Z" fill="{BLUE}" fill-opacity="0.35"/><path d="M0 70 Q140 70 240 236" fill="none" stroke="{BLUE}" stroke-width="5"/>'
        s+=f'<path d="M230 225 L230 120 Q220 60 270 50 L380 40 Q410 50 360 70 Q320 80 320 120 L320 225 Z" fill="#6B7F95"/>'+cloudp(275,210,1.2,'#6B7F95')+f'<path d="M250 236 l-8 18 M282 236 l-8 18 M314 236 l-8 18" stroke="{BLUE}" stroke-width="3"/>'
        s+=arrow(40,170,160,170,BLUE,7,22)+arrow(400,170,460,110,ORANGE,5,16)
        s+=f'<text x="30" y="120" font-family="Arial" font-size="22" font-weight="900" fill="{BLUE}">fredda</text><text x="470" y="200" font-family="Arial" font-size="22" font-weight="900" fill="{ORANGE}">calda</text>'
    else:
        s+=f'<path d="M600 236 L600 60 Q300 120 80 236 Z" fill="{BLUE}" fill-opacity="0.25"/><path d="M80 236 Q300 120 600 60" fill="none" stroke="{LRED}" stroke-width="5"/>'
        s+=f'<rect x="200" y="140" width="200" height="30" rx="15" fill="#9AA8B6"/><rect x="330" y="96" width="180" height="22" rx="11" fill="#C3CDD6"/>'+''.join(f'<path d="M{440+k*44} 44 q20 -12 40 -2" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>' for k in range(3))
        s+=''.join(f'<path d="M{215+k*24} 180 l-5 12" stroke="{BLUE}" stroke-width="3"/>' for k in range(8))+arrow(20,120,170,95,ORANGE,7,22)
        s+=f'<text x="20" y="80" font-family="Arial" font-size="22" font-weight="900" fill="{ORANGE}">calda</text><text x="490" y="220" font-family="Arial" font-size="22" font-weight="900" fill="{BLUE}">fredda</text>'
    return s
fc=card(svgi(600,260,section_front(True),'Sezione di un fronte freddo: l\'aria fredda si incunea sotto la calda e la solleva in un cumulonembo',dw=600,dh=260,pan=False)+h3('Fronte freddo: veloce e violento',30)+lst(['l\'aria fredda si incunea sotto la calda e la spinge in alto','cumulonembi: rovesci, temporali, raffiche','pressione che <b>sale di colpo</b>; temperatura e umidità scendono','dopo: vento che ruota in senso orario, visibilità ottima'],23),None,24,10)
wc=card(svgi(600,260,section_front(False),'Sezione di un fronte caldo: l\'aria calda scivola sopra la fredda con nubi stratificate e pioggia leggera',dw=600,dh=260,pan=False)+h3('Fronte caldo: lento e stabile',30)+lst(['l\'aria calda scorre sopra la fredda','prima i cirri, poi nubi a strati sempre più basse','pressione che <b>cala</b> prima del fronte','piogge leggere e continue, visibilità scarsa'],23),None,24,10)
sec('fronti', head('Meteorologia · le masse d\'aria','I fronti')+f'<div style="display:flex; gap:28px">{fc}{wc}</div>',
 notes='Materiale della scuola: fronti (sezione verticale). Quiz 1.6.1-15 e 1.6.2-27 (fronte: superficie di contatto tra due masse d\'aria), 1.6.1-16 e 1.6.2-50 (fronte caldo, piogge leggere), 1.6.1-17, -41, 1.6.2-32, -49, -51 (fronte freddo: pressione in brusco aumento, cumulonembi, raffiche), 1.6.2-48 (prima del fronte caldo la pressione cala), 1.6.2-33 e -34 (aria instabile: rovesci a intermittenza, visibilità buona).')

def front(kind):
    s=f'<rect x="0" y="0" width="300" height="160" fill="#F4FAFC"/><path d="M20 110 Q150 60 280 100" fill="none" stroke="{ {"freddo":BLUE,"caldo":LRED,"occluso":PURPLE,"staz":NAVY}[kind] }" stroke-width="6"/>'
    pts=[(70,93),(130,82),(190,83),(245,91)]
    for i,(x,y) in enumerate(pts):
        if kind=='freddo': s+=f'<path d="M{x-14} {y+4} L{x+14} {y-4} L{x} {y-26} Z" fill="{BLUE}"/>'
        if kind=='caldo': s+=f'<path d="M{x-14} {y+4} A14 14 0 0 1 {x+14} {y-4} Z" fill="{LRED}"/>'
        if kind=='staz': s+=(f'<path d="M{x-14} {y+4} L{x+14} {y-4} L{x} {y-26} Z" fill="{BLUE}"/>' if i%2==0 else f'<path d="M{x-14} {y+4} A14 14 0 0 0 {x+14} {y-4} Z" fill="{LRED}"/>')
        if kind=='occluso': s+=(f'<path d="M{x-14} {y+4} L{x+14} {y-4} L{x} {y-26} Z" fill="{PURPLE}"/>' if i%2==0 else f'<path d="M{x-14} {y+4} A14 14 0 0 1 {x+14} {y-4} Z" fill="{PURPLE}"/>')
    return s
FR=[(front('freddo'),'Fronte freddo','Triangoli blu: aria fredda e veloce.'),
    (front('caldo'),'Fronte caldo','Semicerchi rossi: aria calda e lenta.'),
    (front('occluso'),'Fronte occluso','Triangoli e semicerchi dallo stesso lato: il freddo ha raggiunto il caldo.'),
    (front('staz'),'Fronte stazionario','Simboli alterni sui due lati: nessuno avanza, maltempo che dura.')]
cc=''.join(card(svgi(300,160,s,f'Simbolo del {t.lower()} sulla carta',dw=300,dh=160,pan=False)+h3(t,28)+p(d,23),None,22,10) for s,t,d in FR)
sec('sinottica', head('Meteorologia · leggere la carta','La carta sinottica')+f'<div style="display:flex; gap:20px">{cc}</div>'+chips([('Carte al suolo e carte in quota',SEA_T),('B bassa · A alta (in inglese L e H)',BLUE_T),('Fronte: linea che separa due masse d\'aria',CORAL_T)]),
 notes='Materiale della scuola: carte sinottiche e fronti. Quiz 1.6.2-9 (carte al suolo e in quota), 1.6.1-11 (occluso: sovrapposizione di un fronte freddo e di uno caldo), 1.6.1-18 e 1.6.2-35 (stazionario: nessuna massa avanza, stallo e maltempo), 1.6.2-27 (il fronte è una linea). I quiz 1.6.2-10…-13 chiedono di riconoscere i simboli in figura: sono fuori dalla raccolta perché hanno l\'immagine, ma all\'esame possono uscire.', gap=26)

X=128
ky=lambda km: 580-km*42
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="580" width="1092" height="40" fill="{WATER}" fill-opacity="0.45"/>'
for k0,k1,c_ in ((6,13,'#FFFFFF'),(2,6,'#EAF4F8'),(0,2,'#FFFFFF')): b+=f'<rect x="70" y="{max(ky(k1),20)}" width="600" height="{ky(k0)-max(ky(k1),20)}" fill="{c_}" fill-opacity="0.35"/>'
b+=line(70,20,70,580,NAVY,3)+''.join(line(62,ky(k),78,ky(k),NAVY,3)+f'<text x="54" y="{ky(k)+7}" text-anchor="end" font-family="Arial" font-size="20" font-weight="700" fill="{NAVY}">{k}</text>' for k in range(0,13,2))
b+=f'<text x="22" y="14" font-family="Arial" font-size="18" font-weight="900" fill="{NAVY}">km</text>'
b+=''.join(f'<path d="M70 {ky(k)} H670" stroke="{NAVY}" stroke-width="2" stroke-dasharray="8 8" stroke-opacity="0.45"/>' for k in (2,6))
def T(x,y,t,c=NAVY): return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial" font-size="21" font-weight="900" fill="{c}">{t}</text>'
b+=''.join(f'<text x="94" y="{ky(k)}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="900" fill="{SOFT}" transform="rotate(-90 94 {ky(k)})">{t}</text>' for k,t in ((9.5,'ALTE'),(4,'MEDIE'),(1,'BASSE')))
# alte
b+=''.join(f'<path d="M{x} {y} q30 -16 70 -5 q24 6 46 -8" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>' for x,y in ((110,ky(9.6)),(170,ky(9.0))))
b+=''.join(f'<circle cx="{330+i*22+(j%2)*11}" cy="{ky(8.6)+j*14}" r="7" fill="#FFFFFF"/>' for i in range(6) for j in range(3))
b+=f'<rect x="480" y="{ky(7.4)}" width="170" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.85"/>'
b+=T(190,ky(8.2),'cirri')+T(390,ky(7.4),'cirrocumuli')+T(565,ky(6.6),'cirrostrati')
# medie
b+=''.join(f'<ellipse cx="{130+i*30}" cy="{ky(4.6)+(i%2)*8}" rx="16" ry="10" fill="#F4F7F9"/>' for i in range(6))
b+=f'<rect x="330" y="{ky(4.4)}" width="320" height="30" rx="15" fill="#B9C6D2"/>'
b+=T(205,ky(3.6),'altocumuli')+T(490,ky(3.5),'altostrati')
# basse
b+=''.join(f'<ellipse cx="{120+i*34}" cy="{ky(1.4)}" rx="22" ry="13" fill="#C7D1DA"/>' for i in range(5))
b+=f'<rect x="300" y="{ky(0.8)}" width="150" height="18" rx="9" fill="#AEB9C4"/>'
b+=f'<rect x="480" y="{ky(1.9)}" width="170" height="52" rx="22" fill="#6B7F95"/>'+''.join(f'<path d="M{495+k*22} {ky(1.9)+56} l-8 22" stroke="{BLUE}" stroke-width="3"/>' for k in range(7))
b+=T(190,ky(0.65),'stratocumuli')+T(375,ky(0.25),'strati')+T(565,ky(2.15)-4,'nembostrati')
# sviluppo verticale
b+=cloudp(740,ky(1.3),1.0)+T(740,ky(0.3),'cumulo')
b+=f'<path d="M850 {ky(1)} L850 {ky(8)} Q850 {ky(11)} 880 {ky(11.6)} L1060 {ky(12.2)} Q1075 {ky(11.6)} 1020 {ky(11)} Q980 {ky(10.4)} 975 {ky(8)} L975 {ky(1)} Z" fill="#6B7F95"/>'+cloudp(912,ky(1.2),1.5,'#6B7F95')
b+=f'<path d="M920 {ky(6)} l-24 50 h20 l-20 50" fill="none" stroke="{SUN}" stroke-width="6" stroke-linejoin="round"/>'+''.join(f'<path d="M{870+k*26} {ky(0.5)} l-10 24" stroke="{BLUE}" stroke-width="4"/>' for k in range(4))
b+=T(912,ky(12.6),'cumulonembo')
lbl=''
txt=sterm('Alte · oltre 6 km circa','Cirri, cirrocumuli, cirrostrati, fatte di ghiaccio. Cirri isolati e pressione stabile o in salita: bel tempo; cirri che si addensano in cirrostrati e pressione che cala: peggiora.',23)+sterm('Medie · da 2 a 6 km','Altocumuli e altostrati: il velo grigio che spesso annuncia un fronte caldo.',23)+sterm('Basse · sotto i 2 km','Strati, stratocumuli e nembostrati: cielo coperto; dai nembostrati pioggia continua.',23)+sterm('A sviluppo verticale','Cumuli, di bel tempo se restano piccoli; cumulonembi, dalla base bassa fino a 12 km: rovesci, temporali, grandine. Più sono alti, più il temporale è violento.',23)
sec('nubi', head('Meteorologia · il cielo','Le nubi'), pinned=svgp(X,Y,W,Hh,b,'Le nubi disposte su una scala verticale da 0 a 12 km: alte (cirri, cirrocumuli, cirrostrati), medie (altocumuli, altostrati), basse (stratocumuli, strati, nembostrati), e a sviluppo verticale il cumulo e il cumulonembo che sale fino a 12 km')+lbl+pcol(txt,gap=16),
 notes='Materiale della scuola: nubi. Quiz 1.6.1-13 e 1.6.2-25 (cirri: bianchi, fibrosi, isolati; le nubi più alte), 1.6.2-4 (cirri che si addensano in cirrostrati, pressione che cala: peggioramento), 1.6.2-28 (cumuli: sviluppo verticale), 1.6.1-14, 1.6.2-26, -31 (cumulonembi, temporali; violenza in funzione dello sviluppo verticale). Le quote delle famiglie di nubi sono indicative (alle nostre latitudini l\'Organizzazione meteorologica mondiale dà: alte 5-13 km, medie 2-7 km, basse fino a 2 km).')
X=700

b=f'<rect x="0" y="0" width="1092" height="620" fill="#CFE3EC"/><rect x="0" y="420" width="1092" height="200" fill="#2C6E8F"/>'
b+=arrow(40,340,420,340,ORANGE,9,26)+f'<text x="50" y="318" font-family="Arial" font-size="24" font-weight="900" fill="{ORANGE}">aria calda e umida</text>'
b+=f'<text x="50" y="470" font-family="Arial" font-size="24" font-weight="900" fill="#FFFFFF">acqua fredda</text>'
b+=f'<g transform="translate(700 420)"><path d="M-80 0 L80 0 L60 30 L-60 30 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><rect x="-30" y="-40" width="50" height="40" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/></g>'
b+=''.join(f'<path d="M{790+k*24} {370-k*6} q16 20 0 40" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>' for k in range(3))
b+=''.join(f'<rect x="{450+k*20}" y="{250+k*12}" width="{640-k*20}" height="{170-k*12}" rx="40" fill="#FFFFFF" fill-opacity="0.32"/>' for k in range(5))
b+=f'<rect x="40" y="540" width="1012" height="40" rx="20" fill="#FFFFFF" fill-opacity="0.3"/><rect x="40" y="540" width="506" height="40" rx="20" fill="#FFFFFF" fill-opacity="0.85"/>'
lbl=lab(X+60,Y+543,480,'nebbia: meno di 1 km',NAVY,24,900,'center')+lab(X+560,Y+543,480,'foschia: oltre 1 km','#FFFFFF',24,900,'center')+lab(X+870,Y+330,200,'segnali sonori',NAVY,22,900)
txt=sterm('Il vapore acqueo','Condensando forma nubi nell\'aria, nebbia a contatto con il suolo o il mare, rugiada e brina sulle superfici.',24)+sterm('Nebbia o foschia','Riducono entrambe la visibilità: è nebbia sotto 1 km, foschia sopra.',24)+sterm('Nebbia da avvezione','Aria calda e umida che scorre su acqua più fredda, con vento debole: la nebbia tipica del mare.',24)+sterm('Se ti prende in mare','Velocità di sicurezza, segnali sonori, fanali accesi. Vicino a costa il colore dell\'acqua che cambia e il rumore dei frangenti avvisano del pericolo.',24)
sec('nebbia', head('Meteorologia · la visibilità','Nebbia e foschia')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Aria calda e umida che scorre su acqua fredda e forma un banco di nebbia attorno a una barca che emette segnali sonori; sotto, una barra della visibilità: nebbia sotto 1 km, foschia oltre')+lbl,
 notes='Materiale della scuola: nebbia e foschia. Quiz 1.6.1-4 (vapore acqueo: nubi, nebbie, rugiada, brina), -7 (nebbia: condensazione a contatto con suolo o specchi d\'acqua), 1.6.2-52 (nebbia sotto 1 km), 1.6.2-8 (segni della nebbia: aria calda e umida verso una zona più fredda, acqua molto più fredda dell\'aria, vento debole). Segnali sonori in nebbia: lezione 5.')

# =====================================================================
# CAPITOLO 3 · MARE E PREVISIONI
# =====================================================================
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
wave='M0 330 '+' '.join(f'L{x} {330-90*math.sin(2*math.pi*(x-40)/420):.1f}' for x in range(0,1093,12))
b+=f'<path d="{wave} L1092 620 L0 620 Z" fill="{WATER}" fill-opacity="0.45"/><path d="{wave}" fill="none" stroke="{SEA}" stroke-width="5"/>'
c1=40+105; c2=c1+420; tr=c1+210
b+=dim(c1,200,c2,200,NAVY)+dash(c1,240,c1,215,NAVY,2)+dash(c2,240,c2,215,NAVY,2)
b+=dim(tr+150,240,tr+150,420,CORAL)+dash(c1+420-60,240,tr+170,240,CORAL,2)+dash(tr-30,420,tr+170,420,CORAL,2)
b+=''.join(arrow(x,90,x+120,90,GREY,7,22) for x in (80,380,680))+dpath('M60 585 L1020 585',PURPLE,4)+arrow(900,585,1020,585,PURPLE,4,16)
lbl=lab(X+c1+60,Y+150,420,'lunghezza: da cresta a cresta',NAVY,24,900)+lab(X+tr+180,Y+435,400,'↕ altezza: dalla cresta al cavo','#FFFFFF',24,900,bg=f'linear-gradient(135deg,{CORAL},#FFB36B)')+lab(X+80,Y+120,260,'vento',SOFT,24,900)+lab(X+60,Y+505,660,'⟷ fetch: il tratto di mare libero su cui soffia il vento','#FFFFFF',24,900,bg=f'linear-gradient(135deg,{PURPLE},{BLUE})')
_f1=p('l\'onda è troppo ripida: l\'altezza supera 1/7 della lunghezza',22,BODY,500,1.3); _f2=p('la profondità è meno del doppio dell\'altezza. Vento contro corrente: onda ripida.',22,BODY,500,1.3)
txt=sterm('Da dove nasce','Il moto ondoso lo fa il vento: più forte, più a lungo, su un fetch più lungo, più grandi le onde. Oltre il fetch minimo l\'onda ha la sua altezza massima.',24)+f'<div style="display:flex; flex-direction:column; gap:8px; background:{CORAL_T}; padding:16px 20px; border-radius:22px">{p("Quando frange",26,INK,800,1.25)}<p style="font-family:{H}; font-size:34px; font-weight:700; line-height:1.15; color:{CORAL}">H ÷ L &gt; 1/7</p>{_f1}<p style="font-family:{H}; font-size:34px; font-weight:700; line-height:1.15; color:{CORAL}">fondale &lt; 2 × H</p>{_f2}</div>'+sterm('Mare vivo, lungo, vecchio','Vivo: il vento soffia sul posto. Lungo: onde arrivate da lontano. Vecchio o morto: resta dopo che il vento è calato.',24)
sec('onde', head('Meteorologia · il mare','Le onde')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Profilo di un\'onda con la lunghezza da cresta a cresta, l\'altezza dalla cresta al cavo, il vento e il fetch')+lbl,
 notes='Materiale della scuola: mare e onde. Quiz 1.6.1-9 (correnti, onde e maree), 1.6.2-39 (il vento provoca il moto ondoso), -40 (lunghezza), -41 (altezza), -29 (fetch minimo), -42 e -43 (quando frange), 1.6.1-30 (vento contro corrente: onda ripida), 1.6.2-44, -45, -46 (mare vivo, lungo, vecchio o morto). Le onde trasportano energia, non acqua: solo quando frangono l\'acqua viene portata in avanti.')

DG=[(0,'calmo','0'),(1,'quasi calmo','0-0,1'),(2,'poco mosso','0,1-0,5'),(3,'mosso','0,5-1,25'),(4,'molto mosso','1,25-2,5'),(5,'agitato','2,5-4'),(6,'molto agitato','4-6'),(7,'grosso','6-9'),(8,'molto grosso','9-14'),(9,'tempestoso','oltre 14')]
W2,H2=1664,540; x0=60; bw=(W2-120)/10
b=f'<rect x="0" y="0" width="{W2}" height="{H2}" fill="#F4FAFC"/>'
for f_,nm,hm in DG:
    h=24+f_*36; x=x0+f_*bw; c=lerp('#9ED8E0',BLUE,f_/6) if f_<=6 else lerp(BLUE,NAVY,(f_-6)/3)
    b+=f'<rect x="{x+10:.0f}" y="{380-h}" width="{bw-20:.0f}" height="{h}" rx="12" fill="{c}"/>'
lbl=''.join(lab(128+x0+f_*bw,Y+385,bw,str(f_),NAVY,32,900,'center') for f_,_,_ in DG)
lbl+=''.join(lab(128+x0+f_*bw,Y+430,bw,f'{nm}<br>{hm} m',INK,21,800,'center') for f_,nm,hm in DG)
bottom=f'<div style="position:absolute; left:128px; top:880px; width:1664px">'+chips([('Mare: scala Douglas da 0 a 9',BLUE_T),('Vento: scala Beaufort da 0 a 12',SEA_T),('Altezza delle onde in metri',CORAL_T)])+'</div>'
sec('douglas', head('Meteorologia · il mare','Lo stato del mare: la scala Douglas'), pinned=svgp(128,Y,W2,H2,b,'Grafico a barre della scala Douglas da 0 calmo a 9 tempestoso, con l\'altezza delle onde in metri')+lbl+bottom,
 notes='Materiale della scuola: mare e onde. Il grado 1 è «quasi calmo» (nel materiale c\'è un refuso, «quasi mosso»). Quiz 1.6.1-40 (vento da 0 a 12, mare da 0 a 9). Nel Meteomar lo stato del mare è dato con questi termini: «mosso», «molto mosso», «agitato». Altezze secondo la scala dell\'Organizzazione meteorologica mondiale.')

def tides(spring):
    s=f'<rect x="0" y="0" width="280" height="240" fill="{NIGHT}"/><circle cx="34" cy="120" r="26" fill="{SUN}"/>'+arrow(70,120,110,120,SUN,3,10)
    s+=f'<ellipse cx="160" cy="120" rx="{54 if spring else 42}" ry="{36 if spring else 42}" fill="{WATER}" fill-opacity="0.5"/><circle cx="160" cy="120" r="30" fill="{BLUE}"/>'
    s+=f'<circle cx="{250 if spring else 160}" cy="{120 if spring else 30}" r="14" fill="#F4F1DE"/>'
    s+=f'<text x="140" y="225" text-anchor="middle" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">{"sizigie" if spring else "quadratura"}</text>'
    return s
mc=card(f'<div style="display:flex; gap:16px">'+svgi(280,240,tides(True),'Sole, Terra e Luna allineati: marea sizigiale',dw=280,dh=240,pan=False)+svgi(280,240,tides(False),'Luna a 90 gradi dal Sole: marea di quadratura',dw=280,dh=240,pan=False)+'</div>'+h3('Le maree',30)+lst(['oscillazione del livello del mare per l\'attrazione di <b>Luna e Sole</b>','<b>sizigie</b> (Luna nuova e piena, allineate al Sole): maree più ampie','<b>quadratura</b> (primo e ultimo quarto): maree più deboli','l\'altezza di marea si misura dallo <b>zero idrografico</b> della carta'],23),None,24,10)
def rip():
    s=f'<rect x="0" y="0" width="576" height="240" fill="{WATER}" fill-opacity="0.35"/><rect x="0" y="200" width="576" height="40" fill="{LAND}"/>'
    s+=''.join(f'<path d="M0 {50+k*36} q36 -12 72 0 t72 0 t72 0 t72 0 t72 0 t72 0 t72 0 t72 0" fill="none" stroke="#FFFFFF" stroke-width="4"/>' for k in range(3))
    s+=f'<ellipse cx="130" cy="160" rx="110" ry="20" fill="{LAND}" fill-opacity="0.85"/><ellipse cx="446" cy="160" rx="110" ry="20" fill="{LAND}" fill-opacity="0.85"/>'
    s+=arrow(288,195,288,30,CORAL,9,26)+arrow(200,192,265,188,CORAL,4,12)+arrow(376,192,311,188,CORAL,4,12)
    return s
rc=card(svgi(576,240,rip(),'Corrente di ritorno: l\'acqua portata a riva dalle onde torna al largo nel varco tra due secche',dw=576,dh=240,pan=False)+h3('Le correnti',30)+lst(['<b>marina</b>: moto dell\'acqua non dovuto a onde o marea; in mare aperto e acque profonde, risente della rotazione terrestre','<b>di marea</b>: dovuta solo alla marea; in acque basse e negli stretti (Messina)','<b>risacca</b>: l\'onda di riflusso; tra due secche torna al largo con forza'],23),None,24,10)
sec('maree', head('Meteorologia · il mare','Maree e correnti')+f'<div style="display:flex; gap:28px">{mc}{rc}</div>',
 notes='Materiale della scuola: maree e correnti marine. Quiz 1.6.1-9 (correnti, onde e maree), -10 (maree: Sole e Luna), -22 (altezza di marea rispetto allo zero idrografico, chart datum), 1.6.1.97 (corrente di marea: codice scritto con il punto nella banca), -44 (acque basse e stretti), -42 e -43 (corrente marina), 1.3.8-20 (risacca). Nel Mediterraneo l\'acqua atlantica entra da Gibilterra e gira in senso antiorario lungo le coste; le maree sono piccole, salvo l\'alto Adriatico.')

X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
b+=f'<path d="M290 40 V0" stroke="{NAVY}" stroke-width="10"/><rect x="40" y="30" width="300" height="250" rx="34" fill="{NAVY}"/><rect x="70" y="60" width="240" height="110" rx="12" fill="#BFE6D9"/>'
b+=''.join(f'<rect x="{70+i*62}" y="200" width="52" height="50" rx="10" fill="#2B4A6B"/>' for i in range(4))
b+=''.join(f'<path d="M{360+i*26} {110-i*8} q18 26 0 52" fill="none" stroke="{SEA}" stroke-width="6" stroke-linecap="round"/>' for i in range(3))
T0=60; tw=(1032-T0)/36
b+=f'<rect x="{T0:.0f}" y="440" width="{12*tw-6:.0f}" height="64" rx="18" fill="#DDE6EC"/>'
for a,e,c in ((12,24,BLUE),(24,36,PURPLE)): b+=f'<rect x="{T0+a*tw:.0f}" y="440" width="{(e-a)*tw-6:.0f}" height="64" rx="18" fill="{c}"/>'
b+=''.join(line(T0+k*tw,520,T0+k*tw,540,NAVY,3) for k in (12,24,36))
b+=f'<rect x="{T0:.0f}" y="330" width="{36*tw-6:.0f}" height="70" rx="18" fill="{CORAL}"/>'
lbl=big(X+70,Y+85,240,'CH 68',NAVY,64)+lab(X+T0,Y+457,12*tw,'Situazione',NAVY,24,900,'center')+lab(X+T0+12*tw,Y+457,12*tw,'Previsione · 12 h','#FFFFFF',24,900,'center')+lab(X+T0+24*tw,Y+457,12*tw,'Tendenza · 12 h dopo','#FFFFFF',24,900,'center')
lbl+=''.join(lab(X+T0+k*tw-60,Y+545,120,t,NAVY,22,900,'center') for k,t in ((12,'12 UTC'),(24,'00 UTC'),(36,'12 UTC')))+lab(X+T0,Y+347,36*tw,'In testa gli avvisi: burrasca, tempesta, temporali · «Sécurité»','#FFFFFF',24,900,'center')
lbl+=lab(X+440,Y+60,620,'Il Meteomar dà, per ognuna delle 25 zone del Mediterraneo, vento, stato del mare e visibilità.',NAVY,26,900)
txt=sterm('Chi lo prepara','Il Centro nazionale di meteorologia e climatologia dell\'Aeronautica.',24)+sterm('Chi lo trasmette','Le stazioni radio costiere, di continuo sul canale VHF 68. Orari e canali sui «Radioservizi per la navigazione» dell\'Istituto Idrografico.',24)+sterm('Gli avvisi','Fenomeni pericolosi in corso, imminenti o previsti, preceduti da «Sécurité». Gli avvisi di burrasca hanno la precedenza assoluta.',24)+p('Radio costiere: Trieste, Ancona, San Benedetto del Tronto, Bari, Crotone, Augusta, Messina, Lampedusa, Mazara del Vallo, Palermo, Napoli, Civitavecchia, Livorno, Genova, Porto Torres, Cagliari.',21,SOFT,700,1.35)
sec('meteomar', head('Meteorologia · le previsioni','Il bollettino Meteomar'), pinned=svgp(X,Y,W,Hh,b,'VHF sul canale 68 e linea del tempo del Meteomar: in testa gli avvisi, poi situazione, previsione valida 12 ore dalle 12 UTC alle 00 UTC, tendenza nelle 12 ore successive')+lbl+pcol(txt,gap=16),
 notes='Materiale della scuola: Meteomar e stazioni radio costiere, bollettino Meteomar (la mappa delle 25 zone è nel volume: mostrarla). Quiz 1.6.2-1 (Centro nazionale di meteorologia e climatologia aeronautica), -2, -14, -15, -16 (avvisi, Sécurité, burrasca in corso o imminente), -21 (gale warning: precedenza assoluta), -17 (canale 68 di continuo), -18 (emesso alle 12 UTC, vale fino alle 00 UTC), -19 e -22 (tendenza: 12 ore successive alla validità), -20 (stazioni radio costiere), -23 (Radioservizi per la navigazione dell\'IIMM).')
X=700

pg=box('Peggiora',lst(['pressione che <b>cala in fretta</b>; temperatura e umidità salgono','cirri che si addensano in cirrostrati','nubi a grande sviluppo verticale','vento sostenuto già dal mattino','venti da Sud che rinforzano, cirri rossastri: pioggia'],25),CORAL,CORAL_T)
mg=box('Migliora',lst(['pressione <b>stabile o in salita</b>; temperatura e umidità scendono','sole rosso la sera con cielo chiaro','basi delle nubi che si alzano','vento che ruota in senso orario (da Est a Sud a Ovest)','venti freddi dal IV e I quadrante; orizzonte chiaro e calma'],25),SEA,SEA_T)
sec('previsioni', head('Meteorologia · i segni del tempo','Prevedere il tempo')+f'<div style="display:flex; gap:28px">{pg}{mg}</div>'+note('Il segno più utile a bordo è la tendenza del barometro: annotala ogni ora.',PURPLE,36),
 notes='Materiale della scuola: previsioni. Quiz 1.6.1-12 (tendenza della pressione), 1.6.2-4 e -7 (peggioramento), -6 (pioggia: cirri rossastri, calo della pressione, venti da Sud), -3 (bel tempo: pressione costante o in lenta salita, sole rosso la sera), -5 (miglioramento: basi delle nubi che salgono, vento che ruota in senso orario, pressione in rapido aumento), 1.6.2-30 (venti freddi dal IV e I quadrante: pressione in aumento), 1.6.1-39 (orizzonte chiaro e calma: bel tempo).', gap=28)

# =====================================================================
# CAPITOLO 4 · UNITÀ E PATENTE
# =====================================================================
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
sx=25; x0=46
for a,e,c in [(0,10,SEA),(10,24,PURPLE),(24,40,CORAL)]: b+=f'<rect x="{x0+a*sx}" y="470" width="{(e-a)*sx}" height="40" fill="{c}"/>'
b+=''.join(line(x0+m*sx,512,x0+m*sx,528,NAVY,3) for m in range(0,41,2))
b+=profile(x0+1*sx,420,8*sx)+profile(x0+10.5*sx,420,13*sx)+profile(x0+24.5*sx,420,15*sx,fly=True)
lbl=lab(X+x0,Y+530,60,'0',NAVY,24,900)+lab(X+x0+10*sx-30,Y+530,60,'10 m',NAVY,24,900,'center')+lab(X+x0+24*sx-30,Y+530,60,'24 m',NAVY,24,900,'center')
lbl+=lab(X+x0+10,Y+476,300,'natanti',('#FFFFFF'),24,900)+lab(X+x0+10*sx+10,Y+476,400,'imbarcazioni',('#FFFFFF'),24,900)+lab(X+x0+24*sx+10,Y+476,200,'navi',('#FFFFFF'),24,900)
lbl+=lab(X+40,Y+40,1000,'Si classificano per lunghezza fuori tutto',NAVY,28,900)
txt=sterm('Unità da diporto','Qualsiasi costruzione, di qualunque tipo e propulsione, per uso sportivo, ricreativo o commerciale.',24)+sterm('Natanti','Fino a 10 m: iscrizione facoltativa, niente licenza né bandiera. Se si iscrivono, seguono le regole delle imbarcazioni.',24)+sterm('Imbarcazioni','Oltre 10 e fino a 24 m: iscrizione all\'ATCN tramite uno STED e licenza obbligatorie; sigla di 4 lettere, 4 numeri e D; bandiera nazionale sempre.',24)+sterm('Navi da diporto','Oltre i 24 m: iscrizione e licenza obbligatorie.',24)
sec('unita', head('Normativa · la classificazione','Natanti, imbarcazioni, navi')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Righello delle lunghezze: fino a 10 metri i natanti, da 10 a 24 metri le imbarcazioni, oltre 24 metri le navi, con una barca per ogni fascia')+lbl,
 notes='Materiale della scuola: classificazione unità. Quiz 1.8.1-25 e -88 (unità e navigazione da diporto: uso lusorio o commerciale), -27 e -28 (uso commerciale: locazione, noleggio, assistenza ai subacquei, insegnamento), -29, -30, -34, -35 (Codice della nautica, regolamento, Codice della navigazione), -56 (lunghezza fuori tutto), -57 (motore di 9 m: natante), -113 (natante: non iscritto), -21 e -86 (natante iscritto: regime delle imbarcazioni), -13, -24, -77 (iscrizione all\'ATCN tramite qualsiasi STED), -26 (sigla), -23, -60, -63, -15 (bandiera), -17 (il nome non è obbligatorio), -103 (13 m: licenza).')

cats=[('A','Senza limiti','oltre forza 8 e onde oltre 4 m',CORAL,CORAL_T),('B','D\'altura','fino a forza 8 e onde di 4 m',PURPLE,LILAC_T),('C','Costiera','fino a forza 6 e onde di 2 m',BLUE,BLUE_T),('D','Acque protette','fino a forza 4 e onde di 0,3 m (a volte 0,5)',SEA,SEA_T)]
ct=''.join(f'<div style="flex:1; display:flex; gap:18px; align-items:center; background:{bg}; padding:20px 24px; border-radius:28px"><p style="font-family:{H}; font-size:84px; font-weight:700; line-height:1; color:{c}">{l}</p><div style="display:flex; flex-direction:column; gap:4px">{p(t,26,INK,800,1.2)}{p(d,22,INK,500,1.3)}</div></div>' for l,t,d,c,bg in cats)
one=box('Entro 1 miglio dalla costa',lst(['tender (battelli di servizio): entro 1 miglio dalla costa o dall\'unità madre','natanti a vela fino a 4 m² di vela, tavole a vela','pattini, jole, pedalò, mosconi, unità a remi','moto d\'acqua; oltre 1000 m dalla costa (500 m dalle coste a picco) può superare la velocità minima'],23),ORANGE,SUN_T)
rul=box('Da ricordare',lst(['marcatura CE: unità da 2,5 a 24 m messe in commercio dopo il 16 giugno 1998','i limiti CE dipendono da forza del vento e altezza significativa dell\'onda','natante CE: entro 12 miglia se omologato senza limiti, altrimenti entro 6','all\'estero solo se la categoria lo consente'],23),NAVY,BLUE_T)
sec('limiti', head('Normativa · fin dove si va','Marcatura CE e limiti di navigazione')+f'<div style="display:flex; gap:16px">{ct}</div><div style="display:flex; gap:24px">{one}{rul}</div>',
 notes='Materiale della scuola: marchio CE, limiti di navigazione. Quiz 1.8.1-69 (marcatura CE da 2,5 a 24 m dopo il 16/06/1998), -12 e -61 (limiti: onde e vento), -116, -117, -119 (categorie B, C, D), -124 (natante CE entro 12 miglia se omologato senza limiti), -64 (all\'estero se la categoria lo consente), -53 e 1.4.2-20…-24 (entro 1 miglio: remi, moto d\'acqua, tavole a vela, tender, vela fino a 4 m², pattini e pedalò), 1.8.1-93 (tender entro 1 miglio: solo i mezzi individuali), -102 (moto d\'acqua: giubbotto indossato e limiti di velocità locali), -122 (oltre la velocità minima solo oltre 1000 m dalla costa, 500 dalle coste a picco).', gap=26)

b=f'<rect x="0" y="0" width="1092" height="620" fill="#0E5C7A" fill-opacity="0.16"/><rect x="0" y="0" width="1092" height="150" fill="#0E5C7A" fill-opacity="0.22"/>'
b+=f'<path d="M0 620 L0 470 Q60 440 120 470 L180 430 Q230 400 260 420 L300 450 Q360 560 520 560 Q700 560 780 450 L830 410 Q880 390 930 430 L1000 450 Q1050 430 1092 450 L1092 620 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<path d="M260 420 L830 410" stroke="{CORAL}" stroke-width="6" stroke-dasharray="16 10"/>'
b+=f'<path d="M0 150 L1092 150" stroke="{NAVY}" stroke-width="4" stroke-dasharray="12 8"/>'+dim(1000,160,1000,405,NAVY)
lbl=lab(X+330,Y+470,400,'acque interne marittime',NAVY,24,900,'center')+lab(X+300,Y+370,500,'linea di base',CORAL,26,900,'center')
lbl+=lab(X+200,Y+250,520,'mare territoriale · 12 miglia',NAVY,28,900,'center')+lab(X+200,Y+60,520,'acque internazionali (alto mare)',NAVY,26,900,'center')
txt=sterm('Linee di base','Le linee che chiudono golfi e baie: da lì si misura il mare territoriale.')+sterm('Acque interne marittime','Il mare tra la costa e la linea di base.')+sterm('Mare territoriale','La fascia di 12 miglia oltre la linea di base. Oltre ci sono le acque internazionali.')+sterm('Navigazione interna','Quella su laghi, fiumi, canali e altre acque interne.')
sec('acque', head('Normativa · dove siamo','Linee di base e acque')+col(txt,540,20), pinned=svgp(X,Y,W,Hh,b,'Costa con un golfo chiuso dalla linea di base: dentro le acque interne marittime, fuori la fascia di 12 miglia del mare territoriale e poi le acque internazionali')+lbl,
 notes='Materiale della scuola: linee di base (carta con Pianosa e Montecristo). Quiz 1.8.1-14 (linee di base: limite interno da cui si misura il mare territoriale), -59 (acque interne marittime: tra la costa e la linea di base), -20 (navigazione interna: laghi, fiumi, canali). Le distanze della patente e delle dotazioni (6, 12 miglia) si misurano dalla costa, non dalla linea di base.')

tiles=f'<div style="display:flex; gap:18px">{tile("6 mg","Oltre le 6 miglia la patente serve sempre.",SEA,SEA_T)}{tile("30 kW","40,8 CV: oltre questa potenza serve sempre (1 kW = 1,36 CV).",CORAL,CORAL_T)}{tile("10 · 5","Anni di validità: 10 fino ai 60 anni, poi 5.",PURPLE,LILAC_T)}{tile("16 · 18","Senza patente: 16 anni per i natanti, 18 per le imbarcazioni.",BLUE,BLUE_T)}</div>'
cil=table(['Entro 6 miglia serve anche sotto i 30 kW se il motore supera','cm³'],[['2 tempi a carburazione','750'],['2 tempi a iniezione diretta','1000'],['4 tempi fuoribordo','1000'],['4 tempi entrobordo','1300']],['80%','20%'],23)
sem=box('E inoltre',lst(['sempre per la moto d\'acqua e per trainare lo sciatore','motore ausiliario: amovibile, su supporto proprio, fino al 20% del principale','con la patente entro 12 miglia si comanda anche un\'unità senza limiti, ma entro le 12 miglia','al timone può stare chi non ha la patente, se a bordo c\'è chi la ha e comanda'],22),CORAL,CORAL_T)
sec('patente', head('Normativa · l\'abilitazione','La patente nautica')+tiles+f'<div style="display:flex; gap:24px; align-items:start"><div style="flex:1">{cil}</div>{sem}</div>',
 notes='Materiale della scuola: patenti nautiche. Quiz 1.8.1-67, -70, -101 (oltre 40,8 CV; conta la potenza massima di esercizio), -111 (35 kW: sempre), -68 (29 kW e 750 cc entro 6 miglia: basta avere 18 anni), -94 (4 tempi entrobordo 1398 cc: serve), -106 (fuoribordo a iniezione diretta 1299 cc: serve), -110 (4 tempi fuoribordo 1098 cc: serve), -118 (natante con 4 tempi fuoribordo 998 cc: 16 anni), -91, -107, -123 (moto d\'acqua), 1.8.2-3, -8, -14 (sci nautico), -78 (vela senza motore entro 6 miglia: 18 anni), -87, -89, -112 (validità), -72 (motore ausiliario), -79 (patente entro 12 miglia e unità senza limiti), -114 (timoniere non abilitato). Il quiz 1.8.1-54 è oscurato. Fonte: Codice della nautica (D.Lgs. 171/2005), art. 39.', gap=26)

# =====================================================================
# CAPITOLO 5 · DOCUMENTI E NOLEGGIO
# =====================================================================
R_=[['Licenza di navigazione','—','sì: dati dell\'unità e del proprietario; rilasciata dall\'ATCN tramite lo STED; vale finché non cambiano le caratteristiche'],
   ['Certificato di sicurezza','—','sì: attesta la navigabilità; si rinnova con le visite periodiche'],
   ['Dichiarazione di potenza','sì','solo con motore fuoribordo'],
   ['Assicurazione RC','ogni motore, di qualsiasi potenza','ogni motore; anche i motori stranieri in acque italiane'],
   ['Certificato di omologazione e manuale del proprietario','natante CE: dice quante persone porta','—'],
   ['Atto di navigazione temporanea','—','al posto della licenza, per fiere ed eventi'],
   ['Contratto di locazione o noleggio','se l\'unità è a noleggio','in originale o copia conforme']]
sec('documenti', head('Normativa · a bordo','I documenti di bordo')+table(['Documento','Natante','Imbarcazione e nave'],R_,['28%','26%','46%'],25)+p('<b>STED</b> = Sportello telematico del diportista: l\'ufficio (Motorizzazione, Capitaneria o agenzia autorizzata) dove si iscrive l\'unità e si chiedono licenza e certificato. <b>ATCN</b> = Archivio telematico centrale delle unità da diporto, il registro nazionale online a cui lo STED è collegato.',24,INK,500)+p('In originale; tra porti italiani bastano le copie conformi. Le persone trasportabili di imbarcazioni e navi le fissa l\'organismo tecnico alla visita iniziale.',24,INK,700),
 notes='Materiale della scuola: documenti. Quiz 1.8.1-99 e -66 (licenza di navigazione), -48 e -100 (certificato di sicurezza), -49, -98, -115 (dichiarazione di potenza: natanti e imbarcazioni con fuoribordo), -31, -32, -33, -95 (assicurazione RC per ogni motore; escluse le unità a remi e a vela senza motore), -47 e -76 (originale o copia conforme tra porti nazionali), -50 (autorizzazione alla navigazione temporanea), -73 (manuale del proprietario), -105 (persone trasportabili del natante CE: certificato di omologazione), 1.3.4-6 (visita iniziale), -46 e -51 (contratti a bordo). Il quiz 1.8.1-22 (licenza RTF) è oscurato.', gap=24)

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
txt=term('Chi ha il certificato','Solo imbarcazioni e navi. I natanti no.')+term('Le visite','Iniziale (fissa anche le persone trasportabili), periodiche, e occasionali dopo danni o modifiche a scafo e motore.')+term('Chi le fa','Un organismo tecnico notificato; l\'esito si annota sul certificato, che si convalida presso uno STED. La licenza non si convalida.')
sec('visite', head('Normativa · la sicurezza dell\'unità','Visite e certificato di sicurezza'), pinned=svgp(X,Y,W,Hh,b,'Due linee del tempo: per le categorie A e B visite a 8, 13, 18, 23 anni; per le C e D a 10, 15, 20 anni')+lbl+pcol(txt),
 notes='Quiz 1.3.4-4 e -10 (solo imbarcazioni e navi), -14, -15, -17 (prima scadenza 8 anni per A e B, 10 per C e D), -8, -13, -16 (poi ogni 5 anni), -2, -7, -11 (visite occasionali), -3 (unità CE: periodiche e occasionali), -6 (visita iniziale: persone trasportabili), -12 (organismo tecnico), -18 (esito sul certificato), -1, -5, -9 (convalida del certificato presso gli STED), -19 (il certificato scade).')
X=700

lc=box('Locazione · senza equipaggio',lst(['paghi per avere la barca per un periodo, <b>senza riscatto</b>','il conduttore la comanda e ne risponde, secondo la licenza','basta la patente adatta alla navigazione'],24),BLUE,BLUE_T)
nc_=box('Noleggio · con equipaggio',lst(['paghi i servizi di chi ti porta con la sua barca','barca ed equipaggio restano dell\'armatore','anche solo una o più cabine','chi comanda deve avere un <b>titolo professionale</b> del diporto'],24),PURPLE,LILAC_T)
le=box('Leasing nautico',lst(['una banca o un intermediario finanzia e concede la barca dietro un canone','l\'utilizzatore ha in toto la responsabilità del comando e i rischi di perdita','risponde in solido delle sanzioni'],24),SEA,SEA_T)
strip=f'<div style="display:flex; gap:20px">'+''.join(f'<p style="flex:1; font-size:23px; line-height:1.35; font-weight:700; color:{INK}; background:{bg}; padding:14px 20px; border-radius:20px">{t}</p>' for t,bg in [('Noleggio occasionale: il proprietario, al massimo 42 giorni l\'anno, comunicando ogni contratto all\'Agenzia delle entrate e all\'Autorità marittima; non è attività professionale.',SUN_T),('Uso commerciale (locazione, noleggio, assistenza ai subacquei, insegnamento): risulta dalla licenza; il contratto sta a bordo in originale o copia conforme.',CORAL_T)])+'</div>'
sec('noleggio', head('Normativa · l\'uso commerciale','Locazione, noleggio, leasing')+f'<div style="display:flex; gap:22px">{lc}{nc_}{le}</div>'+strip,
 notes='Materiale della scuola: locazione, noleggio, leasing nautico. Quiz 1.8.1-27 e -28 (uso commerciale), -52 (risulta dalla licenza), -81 (locazione: godimento senza riscatto), -44 e -45 (il conduttore si assume responsabilità e rischi, secondo la licenza), -82 e -83 (noleggio: servizi di una persona; unità ed equipaggio restano all\'armatore), -85 (a cabina), -80 (comando con titolo professionale), -84 (noleggio occasionale: 42 giorni l\'anno, comunicazioni), -46 e -51 (contratto a bordo; il noleggio va scritto a pena di nullità), 1.8.1.38 (leasing: codice con il punto), -39, -40, -42 (utilizzatore), -36 (assistenza e traino con polizza e comunicazione alla Capitaneria).', gap=26)

# =====================================================================
# CAPITOLO 6 · COMANDANTE E REGOLE
# =====================================================================
lv=[('Ministero delle infrastrutture e dei trasporti',NAVY),('Comando generale delle Capitanerie di porto',BLUE),('Direzione marittima',PURPLE),('Capitaneria di porto · compartimento',SEA),('Ufficio circondariale marittimo · circondario',GREEN),('Uffici locali e delegazioni di spiaggia',CORAL)]
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/>'
for i,(t,c) in enumerate(lv):
    y=30+i*98; w=920-i*60; x=(1092-w)/2
    b+=f'<rect x="{x:.0f}" y="{y}" width="{w}" height="70" rx="35" fill="{c}"/>'
    if i<len(lv)-1: b+=arrow(546,y+70,546,y+96,SOFT,4,12)
lbl=''.join(lab(X+(1092-(920-i*60))/2,Y+30+i*98+18,920-i*60,t,'#FFFFFF',24,900,'center') for i,(t,c) in enumerate(lv))
txt=sterm('Il comandante','Dirige manovra e navigazione. Prima di partire controlla le dotazioni e decide l\'equipaggio minimo secondo meteo e distanza dai porti sicuri.',24)+sterm('Il soccorso','Deve accorrere e salvare chi è in pericolo, se non mette in grave pericolo la sua unità: chi non lo fa rischia fino a 2 anni di reclusione.',24)+sterm('Evento straordinario','Incaglio, falla, incendio, urto, uomo a mare, relitti: la denuncia la fa il comandante all\'Autorità marittima del porto di arrivo (all\'estero al Consolato), entro 3 giorni dall\'arrivo; se ci sono feriti, entro 24 ore.',24)
sec('autorita', head('Normativa · doveri e autorità','Il comandante e l\'autorità marittima')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Scala dell\'autorità marittima: Ministero, Comando generale delle Capitanerie, Direzione marittima, Capitaneria di porto, Ufficio circondariale, uffici locali')+lbl,
 notes='Materiale della scuola: obblighi e doveri del comandante. Quiz 1.8.1-3 (direzione della manovra), -120 e -125 (dotazioni), -121 (equipaggio minimo), -114 (timone a chi non ha la patente), -7, -8, -9, -10 (soccorso e sanzione penale), -1, -5, -65, -74, -92, -96, -108, -109 (evento straordinario: entro 3 giorni dall\'arrivo, all\'Autorità marittima o consolare), -2 (all\'estero: consolato), -16 e -58 (ritrovamenti in spiaggia e relitti: denuncia entro 3 giorni). Il termine di 24 ore con danni alle persone viene dal materiale della scuola; il quiz 1.8.1-96 parla di 3 giorni «nel caso non siano avvenute lesioni a persone».')

b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.3"/><rect x="0" y="550" width="1092" height="70" fill="{LAND}"/>'
yb=550; sc=1.5; yr=yb-200*sc; ytop=yb-250*sc
b+=f'<rect x="0" y="{yr:.0f}" width="1092" height="{yb-yr:.0f}" fill="#FFFFFF" fill-opacity="0.25"/>'
b+=''.join(f'<circle cx="{x}" cy="{yr:.0f}" r="10" fill="{LRED}" stroke="{NAVY}" stroke-width="2"/>' for x in range(30,1092,75))
for x in (700,800):
    b+=''.join(f'<circle cx="{x}" cy="{y:.0f}" r="9" fill="{LYEL}" stroke="{NAVY}" stroke-width="2"/>' for y in [yb-k*25*sc for k in range(1,11)])
    b+=f'<path d="M{x} {ytop-8:.0f} V{ytop-48:.0f}" stroke="{NAVY}" stroke-width="3"/><path d="M{x} {ytop-48:.0f} L{x+30} {ytop-40:.0f} L{x} {ytop-32:.0f} Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>'
b+=topboat(750,yb-110,70,-90,'#FFFFFF',NAVY,3)+arrow(750,yb-160,750,yb-205,NAVY,4,14)
b+=''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="{CORAL}"/>' for x,y in ((180,480),(260,500),(420,470),(520,505),(950,490)))
b+=topboat(330,110,90,0,'#FFFFFF',NAVY,3)
b+=dim(60,yr,60,yb,NAVY)+dim(1040,ytop,1040,yb,ORANGE)
lbl=lab(X+80,Y+yr+70,240,'200 m',NAVY,26,900)+lab(X+880,Y+ytop+230,140,'fino a 250 m',ORANGE,22,900,'right')+lab(X+100,Y+yr-46,560,'gavitelli rossi ogni 50 m: limite dei bagnanti',LRED,22,900)
lbl+=lab(X+830,Y+30,240,'corridoio di lancio: gavitelli gialli o arancioni, bandiere bianche',NAVY,20,900)+lab(X+40,Y+30,420,'oltre 200 m si naviga e si ancora',NAVY,22,900)
txt=sterm('Le ordinanze','Le emana il Capo del circondario marittimo: regolano spiagge, rade, porti, velocità e campi di gara.',24)+sterm('La fascia dei bagnanti','D\'estate, di norma, si naviga e si ancora oltre 200 m dalla spiaggia; il limite è segnato da gavitelli rossi ogni 50 m.',24)+sterm('I corridoi di lancio','Gavitelli gialli o arancioni perpendicolari alla costa fino a 250 m, bandiere bianche su quelli esterni: per partire e approdare con i natanti a motore, piano.',24)+sterm('In emergenza','Verso riva a remi o a lento moto, con rotta perpendicolare alla costa.',24)
sec('costa', head('Normativa · le regole locali','Sotto costa: le ordinanze')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Spiaggia vista dall\'alto con bagnanti, i gavitelli rossi a 200 metri, un corridoio di lancio di gavitelli gialli lungo 250 metri con bandiere bianche e una barca che esce piano')+lbl,
 notes='Materiale della scuola: ordinanze del Capo circondario per sottocosta e rade (disegno: campi di gara, rade, navigazione e ancoraggio oltre 200 m, corridoi di lancio). Quiz 1.8.1-18 e -19 (ordinanze), 1.4.2-4 (di massima 200 m), -5 (gavitelli rossi ogni 50 m), -6 e -7 (corridoi: gialli o arancioni fino a 250 m, bandiere bianche sugli esterni), -17 (corridoi per i natanti a motore), -11 (emergenza: a remi, perpendicolare), -13 (campi di gara: starne lontani), -25 (navigazione a motore interdetta nella fascia dei bagnanti), -10 (velocità oltre i limiti: da 414 a 2.066 euro). Il quiz 1.4.2-1 (10 nodi entro 1000 m) è oscurato: il limite preciso lo dà l\'ordinanza locale.')

S_=[['Comando senza patente (mai presa, revocata, sospesa)','da 2.755 a 11.017 € e sospensione della licenza per 30 giorni'],
    ['Comando con patente scaduta','da 276 a 1.377 €, senza sospensione'],
    ['Esercizio abusivo di attività commerciali','da 2.755 a 11.017 €'],
    ['Velocità oltre i limiti','da 414 a 2.066 €'],
    ['Dopo un urto, non dare i dati della propria unità','da 1.032 a 6.197 €'],
    ['Comando in stato di ebbrezza','da 2.755 a 15.000 € secondo il tasso; sospensione della licenza'],
    ['Comando sotto effetto di droghe','da 2.755 a 11.017 €; doppia se c\'è un sinistro'],
    ['Omissione di soccorso','reclusione fino a 2 anni']]
pt=box('La patente',lst(['<b>sospesa</b> per gravi imperizie o imprudenze, ebbrezza o droghe (da 3 a 24 mesi)','<b>revocata</b> se mancano i requisiti fisici o morali, o con ebbrezza e danno ambientale','<b>negata</b> ai delinquenti abituali'],23),CORAL,CORAL_T)
_tab=table(['Violazione','Sanzione'],S_,['52%','48%'],23)
sec('sanzioni', head('Normativa · cosa si rischia','Le sanzioni')+f'<div style="display:flex; gap:24px; align-items:start"><div style="flex:1.7">{_tab}</div>{pt}</div>'+p('Usare l\'unità senza rispettare le norme sulla sicurezza della navigazione è un illecito amministrativo. Codice della nautica e Codice della navigazione valgono per il diporto ricreativo e commerciale.',23,INK,700),
 notes='Materiale della scuola: sanzioni. Quiz 1.8.1-6 e -90 (senza abilitazione: 2.755-11.017 euro e sospensione della licenza per 30 giorni), -71 e -75 (patente scaduta: niente sospensione, sanzione), -37 e -41 (esercizio abusivo; il -37 riporta 2.775, refuso della banca), 1.4.2-10 (velocità), 1.8.1-4 e -43 (urto: 1.032-6.197), -10 (omissione di soccorso), -11 (illecito amministrativo per la sicurezza della navigazione), -55 e -97 (sospensione), -104 (revoca), -62 (delinquente abituale). Alcol e droghe (1.3.2): la scuola riporta 15.017 euro come massimo per l\'ebbrezza, la banca (1.3.2-2) 15.000: all\'esame vale 15.000. Più un terzo sulle unità a noleggio con tasso tra 0,5 e 0,8 g/l; revoca sopra 1,5 g/l. Dettagli nella lezione 6.', gap=24)

# =====================================================================
# CAPITOLO 7 · MARE PROTETTO E ATTIVITÀ
# =====================================================================
X=128
cx,cy=546,320
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.25"/>'
for r,c in ((290,'#FFE9A6'),(200,'#FFC98A'),(115,'#F59A8A')): b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.35:.0f}" ry="{r}" fill="{c}" fill-opacity="0.8" stroke="{NAVY}" stroke-width="2" stroke-dasharray="8 6"/>'
b+=f'<path d="M{cx-60} {cy+10} Q{cx-50} {cy-50} {cx} {cy-40} Q{cx+70} {cy-50} {cx+64} {cy+14} Q{cx} {cy+50} {cx-60} {cy+10} Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=topboat(cx+300,cy+130,90,-120,'#FFFFFF',NAVY,3)
for a in (20,160,250,320):
    qx=cx+290*1.35*math.cos(math.radians(a)); qy=cy+290*math.sin(math.radians(a))
    b+=f'<path d="M{qx-12:.0f} {qy+10:.0f} L{qx+12:.0f} {qy+10:.0f} L{qx+6:.0f} {qy-14:.0f} L{qx-6:.0f} {qy-14:.0f} Z" fill="{LYEL}" stroke="{NAVY}" stroke-width="2"/><path d="M{qx-8:.0f} {qy-20:.0f} L{qx+8:.0f} {qy-36:.0f} M{qx-8:.0f} {qy-36:.0f} L{qx+8:.0f} {qy-20:.0f}" stroke="{NAVY}" stroke-width="4"/>'
b+=''.join(f'<circle cx="{cx-250+k*30}" cy="{cy+100}" r="7" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>' for k in range(5))
lbl=big(X+cx-30,Y+cy+40,60,'A',NAVY,60)+big(X+cx-30,Y+cy+130,60,'B',NAVY,60)+big(X+cx-30,Y+cy+215,60,'C',NAVY,60)+lab(X+cx-260,Y+cy+115,180,'campo boe',NAVY,20,900)
txt=sterm('Zone A, B, C (a volte D)','Delimitate con coordinate sulla carta allegata al decreto in Gazzetta Ufficiale; spesso segnalate con boe speciali gialle.',23)+sterm('A · riserva integrale','Niente navigazione né ancoraggio, salvo autorizzati.',23)+sterm('B e C','Nella B si va a remi e a vela; il motore e il resto li regolano decreto e regolamento. Nella C le regole sono più blande.',23)+sterm('Campi boe','Nelle zone B e C: lì non si ancora mai e il 15% degli ormeggi è per la vela.',23)+sterm('Chi controlla','Capitanerie e polizie degli enti locali. In un\'area non segnalata la sanzione è amministrativa.',23)
sec('amp', head('Normativa · rispetto del mare','Aree marine protette'), pinned=svgp(X,Y,W,Hh,b,'Isola al centro di un\'area marina protetta con la zona A più interna, la B e la C più esterna, boe gialle sul perimetro e un campo boe')+lbl+pcol(txt,gap=12),
 notes='Materiale della scuola: aree marine protette. Quiz 1.8.2-53 e -54 (zone A, B, C, a volte D, delimitate in carta e nel decreto), -49 e -55 (zona A: niente navigazione né ancoraggio), -50 e -57 (zona B: remi e vela; il resto secondo decreto e regolamento), -47 (campi boe nelle zone B e C), -48 (15% alla vela), -59 (nei campi boe niente ancoraggio), -45 (area non segnalata: sanzione amministrativa), -46 (sorveglianza). Boe perimetrali: segnali speciali gialli del sistema IALA (lezione 3).')
X=700

_sub='Avaria con rischio di perdere carburante o olio: il comandante avvisa senza indugio l\'Autorità marittima più vicina.'
tl_=f'<div style="display:flex; gap:18px">{tile("450 anni","Quanto può durare in mare un contenitore di plastica.",CORAL,CORAL_T)}{tile("5 kg","Di olio usato (il cambio di un fuoribordo da 115 CV) inquinano 1,5 campi da calcio. Vietato disperderlo.",SEA,SEA_T)}{tile("Subito",_sub,PURPLE,LILAC_T)}{tile("Al rivenditore","Razzi, fuochi e boette scaduti si riconsegnano quando si comprano i nuovi.",BLUE,BLUE_T,52)}</div>'
sec('ambiente', head('Normativa · l\'ambiente','Proteggere il mare')+tl_+box('E oltre le 12 miglia? I rifiuti non si gettano mai',lst(['<b>plastica</b>, anche reti e cime: vietata ovunque, a qualsiasi distanza','<b>vetro, alluminio e lattine, carta, stracci</b>: vietati anche al largo; le vecchie regole li permettevano oltre 12 miglia, dal 2013 non più','<b>avanzi di cibo</b>: nel Mediterraneo, area speciale, solo oltre 12 miglia dalla costa e in navigazione','olio, rifiuti e acque nere si portano a terra, nei contenitori e negli impianti del porto'],24),SEA,SEA_T),
 notes='Materiale della scuola: protezione dell\'ambiente marino. Quiz 1.8.2-58 (plastica: fino a 450 anni), -51 (5 kg di olio: una volta e mezzo un campo da calcio), -44 (sversamento di idrocarburi: informare senza indugio l\'autorità marittima più vicina), -52 (segnali scaduti al rivenditore). Rifiuti: convenzione MARPOL, allegato V, nel testo in vigore dal 1° gennaio 2013 (risoluzione MEPC.201(62)), che vale anche per le unità da diporto: divieto generale di scarico in mare; eccezione principale gli avanzi di cibo, che nel Mediterraneo (area speciale) si possono scaricare solo oltre 12 miglia dalla terra più vicina e con l\'unità in navigazione. Prima del 2013 vetro, metallo e carta erano ammessi oltre 12 miglia: molti manuali lo riportano ancora, ma non vale più. Nessun quiz della banca chiede questa distanza. Acque nere: ordinanze locali e regolamenti delle aree protette.', gap=30)

b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/><rect x="0" y="560" width="1092" height="60" fill="{LAND}"/>'
b+=topboat(760,220,170,180,'#FFFFFF',NAVY,4)+line(845,220,960,240,NAVY,3)
b+=dash(700,300,700,540,CORAL,4)
b+=f'<circle cx="980" cy="244" r="12" fill="{CORAL}"/><rect x="964" y="258" width="10" height="40" rx="4" fill="{NAVY}" transform="rotate(-10 969 278)"/><rect x="986" y="258" width="10" height="40" rx="4" fill="{NAVY}" transform="rotate(-10 991 278)"/>'
b+=dim(845,190,960,210,NAVY)+''.join(f'<path d="M{680-i*60} {200+i*10} q-30 10 -60 0" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>' for i in range(4))
b+=topboat(260,400,110,180,'#FFFFFF',SOFT,3)+f'<path d="M330 330 L560 280" stroke="{LRED}" stroke-width="6" stroke-linecap="round"/><path d="M340 280 L550 330" stroke="{LRED}" stroke-width="6" stroke-linecap="round"/>'
lbl=lab(X+790,Y+140,290,'cavo di almeno 12 m',NAVY,22,900)+lab(X+712,Y+430,370,'200 m dalla batimetrica di 1,60 m',CORAL,20,900)+lab(X+80,Y+460,480,'le altre unità: distanza maggiore del cavo, mai nella scia',SOFT,22,900)
txt=sterm('Chi c\'è a bordo','Il conduttore con la patente, sempre, anche su un natante, e un\'altra persona esperta nel nuoto. Qualsiasi unità, con invertitore e messa in folle.',23)+sterm('Cosa serve','Gancio di traino e specchietto convesso riconosciuti dalla Capitaneria, pronto soccorso anche entro 12 miglia, un salvagente per sciatore a portata di mano; lo sciatore indossa il giubbotto.',23)+sterm('Dove e quando','Di giorno, con mare calmo. Oltre 200 m dalla batimetrica di 1,60 m (100 m dalle coste a picco); partenza e rientro nei corridoi o perpendicolari alla costa a non più di 3 nodi. Al massimo 2 sciatori, cavo di 12 m.',23)
sec('scinautico', head('Normativa · lo sci nautico','Lo sci nautico')+col(txt,540,16), pinned=svgp(X,Y,W,Hh,b,'Barca che traina uno sciatore con un cavo di almeno 12 metri lontano dalla spiaggia, e un\'altra barca che non deve seguirne né tagliarne la scia')+lbl,
 notes='Materiale della scuola: sci nautico. Quiz 1.8.2-3, -8, -14 (patente), -4, -9, -26 (una persona esperta nel nuoto oltre al conduttore: in due non si può), -13 (qualsiasi unità), -21 (invertitore e messa in folle), -16, -18, -23 (gancio, specchietto convesso, riconosciuti dalla Capitaneria), -1, -2, -20, -22 (pronto soccorso anche entro 12 miglia, un salvagente per sciatore), -7 e -11 (di giorno, mare calmo), -10 e -6 (200 m dalla batimetrica di 1,60 m), -17 (100 m dalle coste a picco), -19 e -15 (partenza e rientro a 3 nodi, perpendicolari, lontano da bagnanti), -12 (cavo di 12 m), -24 (2 sciatori), -5 e -25 (le altre unità non seguono nella scia e stanno a una distanza maggiore del cavo).')

def diver_buoy(night):
    s=f'<rect x="0" y="0" width="520" height="560" rx="24" fill="{NIGHT if night else SKY}"/><rect x="0" y="180" width="520" height="380" fill="{"#123B57" if night else "#7FC8D3"}"/>'
    s+=f'<path d="M200 160 V80" stroke="{"#DDE6EC" if night else NAVY}" stroke-width="4"/><circle cx="200" cy="182" r="24" fill="{LRED}" stroke="{NAVY}" stroke-width="3"/>'
    if night: s+=f'<circle cx="200" cy="72" r="44" fill="{LYEL}" fill-opacity="0.25"/><circle cx="200" cy="72" r="26" fill="{LYEL}" fill-opacity="0.5"/><circle cx="200" cy="72" r="13" fill="{LYEL}"/>'
    else: s+=f'<svg x="200" y="80" width="90" height="62"><rect width="90" height="62" fill="{LRED}"/><path d="M0 0 L90 62" stroke="#FFFFFF" stroke-width="14"/></svg><rect x="200" y="80" width="90" height="62" fill="none" stroke="{NAVY}" stroke-width="2"/>'
    s+=line(200,206,250,380,"#DDE6EC" if night else NAVY,2)
    s+=f'<g transform="translate(290 400) rotate(20)"><ellipse cx="0" cy="0" rx="40" ry="13" fill="{NAVY if not night else "#DDE6EC"}"/><circle cx="-44" cy="-2" r="11" fill="{NAVY if not night else "#DDE6EC"}"/><path d="M40 0 l30 -12 l0 24 z" fill="{SUN}"/></g>'
    s+=f'<circle cx="200" cy="182" r="165" fill="none" stroke="{"#DDE6EC" if night else NAVY}" stroke-width="3" stroke-dasharray="10 8"/>'
    return s
b=f'<rect x="0" y="0" width="1092" height="620" fill="#F4FAFC"/><g transform="translate(16 30)">{diver_buoy(False)}</g><g transform="translate(556 30)">{diver_buoy(True)}</g>'
lbl=lab(X+30,Y+40,170,'di giorno',NAVY,26,900)+lab(X+570,Y+40,170,'di notte','#FFFFFF',26,900)+lab(X+320,Y+520,200,'raggio 50 m',NAVY,22,900,'center',bg='#FFFFFF')
lbl+=lab(X+320,Y+110,220,'bandiera rossa con diagonale bianca',NAVY,20,900)+lab(X+860,Y+80,220,'luce gialla a lampi a 360°','#FFFFFF',20,900)
txt=sterm('Il segnale','Il subacqueo si segnala con un galleggiante e la bandiera rossa con diagonale bianca, visibile a 300 m; di notte una luce gialla a lampi, a giro d\'orizzonte, visibile a 300 m. Resta entro 50 m dal segnale.',24)+sterm('Con il mezzo d\'appoggio','La bandiera si issa sul mezzo. Le unità con un palombaro in immersione alzano la lettera A del Codice internazionale.',24)+sterm('Chi passa','Modera la velocità e resta ad almeno 100 m dal segnale.',24)
sec('sub', head('Normativa · chi è sott\'acqua','I subacquei')+col(txt,540,18), pinned=svgp(X,Y,W,Hh,b,'Di giorno un galleggiante rosso con la bandiera rossa a diagonale bianca e il subacqueo entro 50 metri; di notte lo stesso galleggiante con la luce gialla lampeggiante')+lbl,
 notes='Materiale della scuola: sub. Quiz 1.4.2-15 e -19 (entro 50 m dal segnale), 1.8.2-32 (bandiera visibile a 300 m), 1.4.2-16 e -9 (di notte luce gialla a lampi visibile a 300 m), 1.8.2-31 (con il mezzo d\'appoggio la bandiera sta sul mezzo), 1.4.2-8 (unità in attività subacquea: pallone rosso con la bandiera), -2 e -12 (le unità restano a 100 m e moderano la velocità). Il quiz 1.4.2-14 (lettera A: palombaro) ha la figura della bandiera.')

ps_=box('Pesca subacquea',lst(['solo dai <b>16 anni</b>, in apnea: mai bombole','solo di giorno, nessuna luce salvo la torcia','fucile carico solo in immersione','con il galleggiante e la bandiera','vietata a meno di <b>500 m</b> dalle spiagge frequentate, <b>100 m</b> da impianti fissi, reti da posta e navi ancorate fuori dai porti'],25),SEA,SEA_T)
pb_=box('Pesca dalla barca',lst(['solo per svago o gara: <b>vietato vendere</b> il pescato','al giorno al massimo <b>5 kg</b> (salvo un pesce singolo più pesante) e <b>1 cernia</b>; tonno rosso: 1 esemplare, finché resta la quota nazionale','canne fino a 3 ami, lenze morte, bolentini, correntine fino a 6 ami, lenze per cefalopodi; niente reti a circuizione','almeno <b>500 m</b> dalle unità in pesca professionale'],25),ORANGE,SUN_T)
sec('pesca', head('Normativa · il pescatore sportivo','La pesca sportiva')+f'<div style="display:flex; gap:24px">{ps_}{pb_}</div>'+note('Le gare di pesca le approva il Capo del compartimento marittimo con un\'ordinanza.',ORANGE,34),
 notes='Materiale della scuola: pesca sportiva. Quiz 1.8.2-27 (16 anni), -28 e -41 e 1.4.2-31 (niente apparecchi di respirazione), -29 (solo la torcia), -30 e 1.4.2-27 (vietata dal tramonto all\'alba), -33 (fucile armato solo in immersione), -34 e -35 e 1.4.2-30 (100 m da navi ancorate, impianti fissi, reti da posta), 1.4.2-26 (500 m dalle spiagge frequentate), 1.8.2-36 e -37 (solo ricreativa o agonistica, niente vendita), -38 (attrezzi), -40 (5 kg, 1 cernia), -42, -43, -56 (tonno rosso), -39 (gare: Capo del compartimento), 1.4.2-18 (si può pescare con un\'unità da diporto, entro limiti di cattura), -28 e -29 (niente reti a circuizione né pesca professionale), -32 (500 m dalla pesca professionale).', gap=26)

# =====================================================================
# APERTURE DEI CAPITOLI, CHIUSURA, RACCOLTA, VERIFICHE
# =====================================================================
exec(open('apertura.py').read())
FIRST={'cap1':'strumenti','cap2':'fronti','cap3':'onde','cap4':'unita','cap5':'documenti','cap6':'autorita','cap7':'amp'}
def chap(id_,n,title,subs,c,mins,art=None):
    mat='Meteorologia' if n<=3 else 'Normativa'
    chapter(id_,n,title,subs,c,f'Circa {mins} minuti, verifica da 2 quiz compresa: andare spediti, il dettaglio è nelle note. Capitolo {n} della parte di {mat.lower()}.',f'circa {mins} minuti · {len(subs)} argomenti',1,label=f'{mat} · capitolo',art=art)
    new=slides.pop(); slides.insert([s_[0] for s_ in slides].index(FIRST[id_]),new)
chap('cap1',1,'Pressione e vento',['Barometro e igrometro','Alta e bassa pressione','I venti del Mediterraneo','La scala Beaufort','Com\'è il vento','Le brezze'],CORAL,14,art=(compass_scene(),'Illustrazione: bussola con la rosa graduata'))
chap('cap2',2,'Fronti, nubi e nebbia',['I fronti','La carta sinottica','Le nubi','Nebbia e foschia'],SEA,10)
chap('cap3',3,'Mare e previsioni',['Le onde','La scala Douglas','Maree e correnti','Il bollettino Meteomar','Prevedere il tempo'],PURPLE,12,art=(radio_scene(),'Illustrazione: VHF portatile che riceve il bollettino'))
chap('cap4',4,'Unità e patente',['Natanti, imbarcazioni, navi','Marcatura CE e limiti','Linee di base e acque','La patente nautica'],BLUE,11)
chap('cap5',5,'Documenti e noleggio',['I documenti di bordo','Visite e certificato di sicurezza','Locazione, noleggio, leasing'],ORANGE,9,art=(chart_scene(),'Illustrazione: carta nautica con la rotta'))
chap('cap6',6,'Il comandante e le regole',['Il comandante e l\'autorità marittima','Sotto costa: le ordinanze','Le sanzioni'],CORAL,10,art=(ring_scene(),'Illustrazione: salvagente anulare con la sagola galleggiante'))
chap('cap7',7,'Mare protetto e attività',['Aree marine protette','Proteggere il mare','Lo sci nautico','I subacquei','La pesca sportiva'],SEA,9)
QZ=[('q01','Quiz 1 · Pressione e strumenti',['1.6.1-5','1.6.1-36','1.6.2-53']),('q02','Quiz 2 · Venti e brezze',['1.6.3-7','1.6.1-27','1.6.1-2']),
 ('q03','Quiz 3 · Com\'è il vento',['1.6.1-1','1.6.2-38','1.6.1-21']),('q04','Quiz 4 · I fronti',['1.6.1-17','1.6.2-35','1.6.2-48']),
 ('q05','Quiz 5 · Nubi e nebbia',['1.6.2-25','1.6.2-26','1.6.1-7']),('q06','Quiz 6 · Onde e stato del mare',['1.6.2-29','1.6.2-45','1.6.1-40']),
 ('q07','Quiz 7 · Maree, correnti, Meteomar',['1.6.1-44','1.6.2-17','1.6.2-21']),('q08','Quiz 8 · Prevedere il tempo',['1.6.2-4','1.6.2-5','1.6.1-12']),
 ('q09','Quiz 9 · Unità e limiti',['1.8.1-86','1.8.1-116','1.8.1-124']),('q10','Quiz 10 · La patente',['1.8.1-89','1.8.1-118','1.8.1-72']),
 ('q11','Quiz 11 · Documenti, noleggio, sanzioni',['1.8.1-98','1.8.1-84','1.8.1-90']),('q12','Quiz 12 · Sci nautico, sub e pesca',['1.8.2-12','1.4.2-15','1.8.2-40'])]
closing(['Pressione che cala in fretta: arriva brutto tempo; attorno alla bassa il vento gira in senso antiorario','Fronte freddo: pressione su di colpo, raffiche e temporali; è nebbia sotto 1 km di visibilità','Meteomar sul canale 68: previsione per 12 ore, tendenza per le 12 dopo; gli avvisi di burrasca hanno la precedenza','Patente oltre 6 miglia o 30 kW; natanti fino a 10 m, imbarcazioni fino a 24, poi navi','Evento straordinario: denuncia entro 3 giorni; sub: 100 m dal segnale; sci nautico oltre 200 m dalla batimetrica di 1,60 m'],
 'Prossima lezione · 08 · Quiz ed esercizi di carteggio di navigazione entro le 12 miglia','A casa: i 120 quiz di meteorologia (1.6) e i 184 di normativa e ambiente (1.8), più visite e certificati (1.3.4) e la sezione 1.4.2.')
raccolta(7,8,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,
 [('Leggi tutte e tre','Prima di scegliere leggi le tre risposte fino in fondo: spesso due si somigliano e cambia una parola.'),
  ('Da dove viene','Il vento si chiama con la direzione da cui soffia: Scirocco da SE, Libeccio da SW.'),
  ('Chi decide','Comandante, Capitaneria, STED, organismo tecnico: chiediti chi rilascia, chi controlla, chi sanziona.'),
  ('Attento ai numeri','hPa, metri, miglia, kW, anni, euro: controlla il numero e l\'unità.')],
 ['Quiz 1-8 · meteorologia (24)','Quiz 9-11 · unità, patente, documenti, sanzioni (9)','Quiz 12 · sci nautico, subacquei e pesca (3)'],
 'Ultimi 45 minuti della lezione. 12 slide da 3 quiz, ciascuna seguita dalle risposte: circa 3 minuti e mezzo per slide. Far rispondere ad alta voce con la lettera, poi chiedere perché le altre due sono sbagliate. Se il tempo stringe, lasciare per casa le slide 3 e 7.',esame=['meteo', 'normativa'])
intermedi([('brezze','v1','Verifica · Pressione e vento',['1.6.1-35','1.6.2-37']),
 ('nebbia','v2','Verifica · Fronti, nubi e nebbia',['1.6.2-49','1.6.2-52']),
 ('previsioni','v3','Verifica · Mare e previsioni',['1.6.2-43','1.6.2-19']),
 ('patente','v4','Verifica · Unità e patente',['1.8.1-59','1.8.1-110']),
 ('noleggio','v5','Verifica · Documenti e noleggio',['1.8.1-82','1.3.4-14']),
 ('sanzioni','v6','Verifica · Il comandante e le regole',['1.8.1-1','1.4.2-6']),
 ('pesca','v7','Verifica · Mare protetto e attività',['1.8.2-57','1.8.2-30'])])
write_deck(OUT,'Lezione 07 · Meteorologia e Normativa',[s_[0] for s_ in slides],
 {"s1":{"description":"Apertura e agenda","start":"cover"},"s2":{"description":"Barometro, pressione, venti, Beaufort, struttura del vento, brezze","start":"cap1"},
  "s3":{"description":"Fronti, carta sinottica, nubi, nebbia","start":"cap2"},"s4":{"description":"Onde, Douglas, maree e correnti, Meteomar, previsioni","start":"cap3"},
  "s5":{"description":"Unità, marcatura CE e limiti, acque, patente","start":"cap4"},"s6":{"description":"Documenti, visite, locazione e noleggio","start":"cap5"},
  "s7":{"description":"Comandante, ordinanze sotto costa, sanzioni","start":"cap6"},"s8":{"description":"Aree protette, ambiente, sci nautico, subacquei, pesca","start":"cap7"},
  "s9":{"description":"Raccolta quiz","start":"capquiz"}})
