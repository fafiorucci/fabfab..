import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
from lezione_base import *
import lezione_base as LB
import geo, chart, es10, es12, json
OUT=SP+'/lez12/project'
GREY='#97A6B4'; LRED='#E23B3B'; ORANGE='#F28C28'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','Lo scarroccio':'wind','I venti della rosa':'compass','Il traverso si misura dalla prora':'lighthouse',
 'Dalla rotta alla prora e ritorno':'dividers','La carta 42/D':'map','La traccia':'map','Il tracciamento':'dividers'})
def pcol(inner,w=532,gap=20,left=1260,top=290): return f'<div style="position:absolute; left:{left}px; top:{top}px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=24: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF',align='left'):
    h=lab(x,y,w,t,tc,size,900,align,bg=c)
    return h if align=='center' else h.replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
X,Y,W,Hh=700,290,1092,620

R5=chart.rings(); R42=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart','coast42_rings.json')))
def chart_html(S, x, y, w, h, solution, alt):
    chart.RINGS=R42 if getattr(S,'carta','')=='42D' else R5
    body,labels,glabs,sbl,C=chart.render(S,w,h,solution)
    svg=f'<svg aria-label="{alt}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px">{body}</svg>'
    html=''
    for kind,v,t in glabs:
        if kind=='lat' and 30<v<h-40: html+=lab(x+10,y+v-30,130,t,'#5E6E82',20,800)
    lastx=-999
    for kind,v,t in glabs:
        if kind=='lon' and 60<v<w-230 and v-lastx>150: html+=lab(x+v+6,y+h-34,140,t,'#5E6E82',20,800); lastx=v
    sx,sy,L,t=sbl; html+=lab(x+sx,y+sy,max(L,120),t,'#16324F',20,900)
    for lx,ly,lw,t,c,kind in chart.place_labels(labels,w,h,22):
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px; white-space:nowrap">{t}</p>'
    return svg+html

# ============ COVER + AGENDA ============
cover(12,'Carteggio: lo scarroccio','Quando il vento ti spinge di lato: prora e rotta non coincidono più. I 24 esercizi ufficiali delle carte 5/D e 42/D',
 'Lezione 12. Esercizi ufficiali 5.1.4-5.4.4 (carta 5/D, 20 esercizi) e 5.5.4-5.8.4 (carta 42/D, 4 esercizi) dell\'Allegato A al DD 131/2022. Richiamo della lezione 4 (lo scarroccio e i nomi dei venti). Carte ridisegnate da OpenStreetMap; all\'esame si lavora sulle carte dell\'IIM.')
blocks=[('0:00','25′','Scarroccio, venti, traverso dalla prora',CORAL),('0:25','25′','5/D settori A e B (10 esercizi)',SEA),('0:50','25′','5/D settori C e D (10)',BLUE),('1:15','25′','Carta 42/D: Bocche e Gallura (4)',PURPLE),('1:40','20′','Ripasso e dubbi',GREEN)]
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag("La regola")+f'<p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1.1; color:{INK}">Rv = Pv + Sc</p>'+p('Sc positivo se il vento arriva da sinistra e spinge a dritta; negativo se arriva da dritta',26,INK,700))
left=card(tag('Tre domande, sempre',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px"><li>da che lato arriva il vento? (segno di Sc)</li><li>la traccia dà la prora o la rotta?</li><li>il rilevamento polare si conta dalla prora</li></ul>',SEA_T,flex=1.4)
sec('agenda', head('Lezione 12 · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Come nelle lezioni 10 e 11: per ogni esercizio una slide con la traccia e una con il tracciamento. Il punto chiave di oggi: la barca si muove sulla rotta, ma i rilevamenti polari e il traverso sono riferiti alla prora.')

# ============ VENTI ============
V=[('Tramontana','N · 000°'),('Grecale','NE · 045°'),('Levante','E · 090°'),('Scirocco','SE · 135°'),('Ostro','S · 180°'),('Libeccio','SW · 225°'),('Ponente','W · 270°'),('Maestrale','NW · 315°')]
cx,cy,R=546,310,200
b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/><circle cx="{cx}" cy="{cy}" r="{R+40}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="4"/>'
for i,(n,d) in enumerate(V):
    a=math.radians(i*45); x=cx+R*math.sin(a); y=cy-R*math.cos(a)
    b+=arrow(x,y,cx+60*math.sin(a),cy-60*math.cos(a),[CORAL,SEA,PURPLE,BLUE][i%4],5,18)
b+=f'<circle cx="{cx}" cy="{cy}" r="20" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
lbl=''
for i,(n,d) in enumerate(V):
    a=math.radians(i*45); x=cx+(R+95)*math.sin(a); y=cy-(R+95)*math.cos(a)
    lbl+=lab(128+x-110,Y+y-30,220,n,[CORAL,SEA,PURPLE,BLUE][i%4],26,900,'center')+lab(128+x-110,Y+y+4,220,d,'#5E6E82',22,800,'center')
sec('venti', head('Carteggio · i nomi dei venti','I venti della rosa'), pinned=svgp(128,Y,W,Hh,b,'Rosa dei venti con gli otto venti e le direzioni da cui soffiano')+lbl+pcol(
 term('Il vento viene da','Il nome dice da dove soffia: il Maestrale arriva da nord-ovest e spinge verso sud-est.')+term('Da che lato?','Confronta la direzione del vento con la rotta: se arriva dal lato sinistro della barca, la spinge a dritta.')+term('Attenzione alla corrente','La corrente, invece, si indica con la direzione verso cui va.')),
 notes='Richiamo della lezione 4 (vento «da», corrente «verso») e del quiz 1.7.7-22. Negli esercizi di oggi compaiono tutti gli otto venti.')

# ============ SCARROCCIO ============
def scsvg():
    b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/>'
    A=(160,500); pv=60; sc=12
    b+=''.join(arrow(60+i*140,40,60+i*140+90,130,GREY,6,20) for i in range(3))
    b+=line(A[0],A[1],A[0]+700*math.sin(math.radians(pv)),A[1]-700*math.cos(math.radians(pv)),NAVY,3)
    e=(A[0]+760*math.sin(math.radians(pv+sc)),A[1]-760*math.cos(math.radians(pv+sc)))
    b+=f'<line x1="{A[0]}" y1="{A[1]}" x2="{e[0]:.0f}" y2="{e[1]:.0f}" stroke="{CORAL}" stroke-width="6"/>'+arrow(e[0]-60*math.sin(math.radians(pv+sc)),e[1]+60*math.cos(math.radians(pv+sc)),e[0],e[1],CORAL,6,22)
    b+=topboat(A[0]+260*math.sin(math.radians(pv)),A[1]-260*math.cos(math.radians(pv))+30,150,pv-90,'#FFFFFF',NAVY,4)
    b+=f'<path d="M{A[0]+180*math.sin(math.radians(pv)):.0f} {A[1]-180*math.cos(math.radians(pv)):.0f} A180 180 0 0 1 {A[0]+180*math.sin(math.radians(pv+sc)):.0f} {A[1]-180*math.cos(math.radians(pv+sc)):.0f}" fill="none" stroke="{PURPLE}" stroke-width="5"/>'
    return b
lbl=pill(700+640,Y+150,240,'prora vera Pv',NAVY)+pill(700+820,Y+330,240,'rotta vera Rv',CORAL)+pill(700+330,Y+300,220,'scarroccio Sc',PURPLE)+pill(700+40,Y+150,140,'vento',GREY)
sec('scarroccio', head('Carteggio · il vento','Lo scarroccio')+col(term('Rv = Pv + Sc','La prora è dove punta la barca, la rotta è dove va davvero. La differenza è lo scarroccio.')+term('Il segno','Vento da sinistra: spinge a dritta, Sc positivo, la rotta sta a destra della prora. Vento da dritta: Sc negativo.')+term('La velocità','Se la traccia lo dice, il vento cambia anche la velocità: Ve = Vp ± la variazione.')),
 pinned=svgp(700,Y,W,Hh,scsvg(),'Barca con prora a 060° e vento da sinistra: la rotta vera è ruotata a destra della prora dello scarroccio')+lbl,
 notes='Quiz 1.7.7-12, -18, -19, -21, -23, -26 (scarroccio). Esempi dalla traccia: 5.1.4-3 (Pv 085°, Tramontana, Sc +8°, Rv 093°); 5.1.4-5 (Pv 190°, Maestrale da dritta, Sc −10°, Rv 180°).')

# ============ TRAVERSO DALLA PRORA ============
def trsvg():
    b=f'<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/><path d="M430 620 Q520 560 640 560 Q760 560 840 620 Z" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/>'
    L=(640,570); b+=f'<circle cx="{L[0]}" cy="{L[1]}" r="13" fill="{SUN}" stroke="{NAVY}" stroke-width="3"/>'
    A=(60,110); rv=100; pv=85
    ur=(math.sin(math.radians(rv)),-math.cos(math.radians(rv)))
    b+=line(A[0],A[1],A[0]+900*ur[0],A[1]+900*ur[1],CORAL,5)
    # punto dove L è a pv+90 (=175)
    ub=(math.sin(math.radians(pv+90)),-math.cos(math.radians(pv+90)))
    det=ur[0]*(-ub[1])-ur[1]*(-ub[0]); s=((L[0]-A[0])*(-ub[1])-(L[1]-A[1])*(-ub[0]))/det; T=(A[0]+ur[0]*s,A[1]+ur[1]*s)
    b+=line(T[0],T[1],L[0],L[1],PURPLE,4)
    # traverso sbagliato: perpendicolare alla rotta
    ub2=(math.sin(math.radians(rv+90)),-math.cos(math.radians(rv+90))); det=ur[0]*(-ub2[1])-ur[1]*(-ub2[0]); s2=((L[0]-A[0])*(-ub2[1])-(L[1]-A[1])*(-ub2[0]))/det; T2=(A[0]+ur[0]*s2,A[1]+ur[1]*s2)
    b+=f'<line x1="{T2[0]:.0f}" y1="{T2[1]:.0f}" x2="{L[0]}" y2="{L[1]}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
    b+=topboat(T[0],T[1],150,pv-90,'#FFFFFF',NAVY,4)+f'<circle cx="{T[0]:.0f}" cy="{T[1]:.0f}" r="15" fill="none" stroke="{CORAL}" stroke-width="5"/>'
    b+=line(T[0],T[1],T[0]+220*math.sin(math.radians(pv)),T[1]-220*math.cos(math.radians(pv)),NAVY,3)
    return b,T,T2
b,T,T2=trsvg()
lbl=pill(128+T[0]+170,Y+T[1]-120,240,'prora Pv',NAVY)+pill(128+900,Y+230,240,'rotta Rv',CORAL)+pill(128+T[0]-330,Y+T[1]+90,300,'traverso: Pv + 90°',PURPLE)+pill(128+T2[0]+50,Y+T2[1]+120,420,'non la perpendicolare alla rotta',GREY)
sec('traverso', head('Carteggio · il punto chiave','Il traverso si misura dalla prora'), pinned=svgp(128,Y,W,Hh,b,'La barca scarroccia: il faro è al traverso quando lo si rileva a 90° dalla prora, non a 90° dalla rotta')+lbl+pcol(
 term('La barca punta la prora','Il traverso e i rilevamenti polari sono angoli misurati a bordo, dalla prora: Rilv = Pv + ρ.')+term('Ma cammina sulla rotta','Il punto va cercato sulla Rv: dove il rilevamento Pv ± 90° del faro taglia la rotta.')+term('L\'errore tipico','Tracciare la perpendicolare alla rotta: con 10° di scarroccio il punto sbaglia di mezzo miglio o più.')),
 notes='Esercizi 5.1.4-1, -2, -3, -4, -5, 5.2.4-2, -3, 5.3.4-4, -5, 5.4.4-5, 5.7.4-1, 5.8.4-1 (traverso); 5.2.4-1, 5.3.4-2, -3, 5.4.4-1, -2, -4 (rilevamenti polari con scarroccio).')

# ============ DALLA ROTTA ALLA PRORA ============
C=[('Hai la prora','Rv = Pv + Sc. Esempio 5.1.4-4: Pv 290°, Libeccio da sinistra, Sc +5°: Rv 295°.',CORAL,CORAL_T),
   ('Hai la rotta','Pv = Rv − Sc. Esempio 5.2.4-2: Rv 140°, Libeccio da dritta, Sc −10°: Pv 150°.',SEA,SEA_T),
   ('Vuoi arrivare','Traccia la rotta verso la meta, poi Pv = Rv − Sc: la prora va tenuta più al vento. 5.5.4-1: Rv 345° verso Bonifacio, Ponente, Sc +10°: Pv 335°.',PURPLE,LILAC_T),
   ('La velocità','Ve = Vp ± variazione. 5.4.4-3: Ve = distanza ÷ tempo = 6 kn, Vp = Ve + 1 = 7 kn.',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:16px; background:{bg}; padding:40px; border-radius:32px"><p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,30,INK,600,1.4)}</div>' for t,d,c,bg in C)
sec('conti', head('Carteggio · i conti','Dalla rotta alla prora e ritorno')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:28px">{tiles}</div>',
 notes='Il segno di Sc si decide sempre rispetto alla direzione in cui la barca avanza. 5.2.4-5: Rv 309° verso il punto 1 mg a sud dello Sparviero, Ponente da sinistra, Sc +5°: Pv 304°.')

quiz_slide('quiz1','Quiz · Lo scarroccio',['1.7.7-19','1.7.7-21','1.7.7-26'],False)
quiz_slide('quiz1r','Quiz · Le risposte',['1.7.7-19','1.7.7-21','1.7.7-26'],True)

# ============ CARTA 42/D ============
M=es10.Sol('5.5.4-1',(41.12,9.25)); M.pts=[]; M.lines=[]; M.carta='42D'
for n,sh in {'Porto di Bonifacio':'Bonifacio','Faro delle Isolette Monaci':'Isolette Monaci','Punta li Canneddi':'P.ta li Canneddi','Faro di Punta Timone':'Tavolara','Faro dello Scoglio Mortoriotto':'Mortoriotto'}.items(): M.pts.append((geo.lm(n),sh,'lm'))
M.pts.append(((40.85,8.6),'','none')); M.pts.append(((41.45,9.85),'','none'))
sec('carta42', head('Carteggio · la seconda carta','La carta 42/D'), pinned=chart_html(M,128,290,1664,620,True,'Carta schematica delle Bocche di Bonifacio e della Sardegna nord-orientale con i punti degli esercizi'),
 notes='La 42/D copre le Bocche di Bonifacio, la Gallura e il golfo dell\'Asinara, con la Corsica meridionale. Coste da OpenStreetMap (© contributori OSM, ODbL). Negli esercizi di scarroccio della 42/D: Bonifacio, Isolette Monaci, Punta li Canneddi, Tavolara e Mortoriotto. Le altre famiglie della 42/D nella lezione 15.')

# ============ ESERCIZI ============
SETT={'5.1':('5/D · A','Elba',SEA),'5.2':('5/D · B','Castiglione e Punta Ala',PURPLE),'5.3':('5/D · C','Pianosa e Montecristo',BLUE),'5.4':('5/D · D','Giglio e Argentario',GREEN),
      '5.5':('42/D · A','Bonifacio',CORAL),'5.6':('42/D · B','La Maddalena e Monaci',CORAL),'5.7':('42/D · C','Golfo dell\'Asinara',CORAL),'5.8':('42/D · D','Golfo di Olbia',CORAL)}
order_ex=[]
def rng(r): return r.replace('\n',' ').replace('Ora traverso ','').replace('Ora del rilevamento: ','').replace('Lat.','Lat ').replace('Long.','Long ').replace('÷',' ÷ ')
ASK={'ora':'l\'ora del traverso','pv':'la prora vera da tenere','vp':'la velocità propria da impostare','pos':'le coordinate del punto nave'}
for f in es12.SOLS:
    S=f(); sid='s'+S.id.replace('.','_').replace('-','_'); st=SETT[S.id[:3]]
    txt=S.ex['testo'].replace('\n',' ')
    fs=26 if len(txt)<520 else (24 if len(txt)<760 else 22)
    left_col=f'<div style="display:flex; flex-direction:column; gap:20px; width:690px">{p(txt,fs,INK,500,1.45)}<p style="font-size:26px; font-weight:900; color:#FFFFFF; background:{st[2]}; padding:10px 20px; border-radius:18px">Da trovare: {ASK[S.kind]}</p></div>'
    sec(sid+'_t', head(f'Esercizio {S.id} · carta {st[0]} · {st[1]}','La traccia',st[2])+left_col, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell\'esercizio {S.id}'),
        notes=f'Traccia ufficiale (Allegato A al DD 131/2022). Risposta ufficiale: {rng(S.ex["risposta_ufficiale"])}.')
    ol='<ol style="font-size:24px; line-height:1.38; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{x}</li>' for x in S.passi)+'</ol>'
    ok=S.check()
    extra='' if ok else f'<p style="font-size:22px; font-weight:600; color:{INK}">{S.note or "Il nostro calcolo esce di poco dalla forchetta: vedi le note."}</p>'
    res=f'<div style="display:flex; flex-direction:column; gap:4px; background:{CORAL_T}; padding:16px 20px; border-radius:20px"><p style="font-size:28px; font-weight:900; color:{CORAL}">{S.res_txt}</p><p style="font-size:22px; font-weight:700; color:{INK}">Ufficiale: {rng(S.ex["risposta_ufficiale"])}</p>{extra}</div>'
    sec(sid+'_s', head(f'Esercizio {S.id} · soluzione','Il tracciamento',st[2]), pinned=chart_html(S,128,290,1092,620,True,f'Tracciamento dell\'esercizio {S.id}')+pcol(ol+res,532,14),
        notes='Soluzione: '+' '.join(S.passi)+f' Risultato: {S.res_txt}. Ufficiale: {rng(S.ex["risposta_ufficiale"])}.'+('' if ok else ' Scarto rispetto alla forchetta ufficiale dovuto alla posizione del punto cospicuo sulla carta: sulla 5/D si usa il simbolo stampato.'))
    order_ex+=[sid+'_t',sid+'_s']

closing(['Rv = Pv + Sc: vento da sinistra, Sc positivo','Il vento si chiama da dove viene; la corrente per dove va','Traverso e rilevamenti polari si contano dalla prora: Rilv = Pv + ρ','Il punto però sta sulla rotta vera','Per arrivare in un punto: Pv = Rv − Sc, prora più al vento'],
 'Prossima lezione · 13 · Correnti (prima parte)','A casa: rifai sulla carta gli esercizi non svolti in aula.')
write_deck(OUT,'Lezione 12 · Carteggio: lo scarroccio',
 ['cover','agenda','venti','scarroccio','traverso','conti','quiz1','quiz1r']+order_ex[:40]+['carta42']+order_ex[40:]+['chiusura'],
 {"s1":{"description":"Apertura, venti e regole dello scarroccio","start":"cover"},"s2":{"description":"Carta 5/D, settori A e B","start":"s5_1_4_1_t"},"s3":{"description":"Carta 5/D, settori C e D","start":"s5_3_4_1_t"},
  "s4":{"description":"Carta 42/D","start":"carta42"}})
