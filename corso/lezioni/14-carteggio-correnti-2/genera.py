"""Lezioni 13, 14 e 15: le correnti (5/D) e la carta 42/D. Uso: python3 gen_corr.py 13|14|15"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
from lezione_base import *
import lezione_base as LB
import geo, chart, es10, escorr, json
LES=int(sys.argv[1]) if len(sys.argv)>1 else 14
OUT=SP+f'/lez{LES}/project'
GREY='#97A6B4'
LB.ICON_T.update({'La lezione di oggi':'lifebuoy','La corrente':'wind','Dallo stimato all\'osservato':'dividers','Il triangolo delle velocità':'current',
 'Quattro casi, quattro costruzioni':'dividers','Tempi e velocità':'compass','La carta 42/D':'map','Rilevamenti alla bussola':'compass','La traccia':'map','Il tracciamento':'dividers'})
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
    for lx,ly,lw,t,c,kind in chart.place_labels(labels,w,h,22,[(sx-12,sy-8,max(L,120)+30,h-sy+8)]):
        html+=f'<p style="position:absolute; left:{x+lx:.0f}px; top:{y+ly:.0f}px; width:max-content; max-width:{lw+20:.0f}px; font-size:22px; line-height:1.3; font-weight:900; color:#FFFFFF; text-align:left; background:{c}; padding:2px 10px; border-radius:10px; white-space:nowrap">{t}</p>'
    return svg+html

def P(a,A,d): return (A[0]+d*math.sin(math.radians(a)),A[1]-d*math.cos(math.radians(a)))
def seg(A,B,c,w=6,dash=''):
    da=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{A[0]:.0f}" y1="{A[1]:.0f}" x2="{B[0]:.0f}" y2="{B[1]:.0f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{da}/>'
def vecsvg(A,B,c,w=6): return seg(A,B,c,w)+arrow(A[0]+(B[0]-A[0])*0.8,A[1]+(B[1]-A[1])*0.8,B[0],B[1],c,w,22)
def dot(A,c=NAVY,r=12): return f'<circle cx="{A[0]:.0f}" cy="{A[1]:.0f}" r="{r}" fill="#FFFFFF" stroke="{c}" stroke-width="5"/>'
SEA_BG='<rect x="0" y="0" width="1092" height="620" fill="#E8F4F8"/>'

# ------------- figura: il triangolo delle velocità -------------
def trisvg():
    A=(170,500); Pv=P(35,A,440); Q=P(120,Pv,210)
    b=SEA_BG+''.join(f'<path d="M{40+i*230} {80+(i%2)*30} q40 -18 80 0 t80 0" fill="none" stroke="#9FD3E0" stroke-width="4"/>' for i in range(5))
    b+=vecsvg(A,Pv,NAVY)+vecsvg(Pv,Q,SEA)+vecsvg(A,Q,CORAL,7)+dot(A)
    b+=topboat(A[0]+10,A[1]-230,120,-55,'#FFFFFF',NAVY,4)
    return b,A,Pv,Q
tb,tA,tP,tQ=trisvg()
def tri_labels(x0,y0):
    return (pill(x0+tA[0]-40,y0+tA[1]+30,200,'A',NAVY)+pill(x0+20,y0+400,280,'Pv · Vp (motore)',NAVY)
            +pill(x0+(tP[0]+tQ[0])/2+30,y0+(tP[1]+tQ[1])/2-50,300,'Dc · Vc (corrente)',SEA)+pill(x0+(tA[0]+tQ[0])/2+60,y0+(tA[1]+tQ[1])/2+30,300,'Rv · Ve (sul fondo)',CORAL))

# ------------- figura: dallo stimato all'osservato -------------
def stsvg():
    A=(150,470); St=P(70,A,560); B=P(140,St,190)
    b=SEA_BG+'<path d="M760 620 Q820 520 930 540 Q1030 560 1092 500 L1092 620 Z" fill="#F3E6C4" stroke="#B89A5E" stroke-width="3"/>'
    b+=vecsvg(A,St,NAVY)+seg(A,B,CORAL,4,'12 8')+vecsvg(St,B,SEA,7)+dot(A)+dot(St,NAVY)+f'<circle cx="{B[0]:.0f}" cy="{B[1]:.0f}" r="16" fill="none" stroke="{CORAL}" stroke-width="6"/>'
    return b,A,St,B
sb,sA,sSt,sB=stsvg()

C=globals()
SOLS=[f() for f in escorr.SOLS[LES]]
LEZ={13:dict(title='Carteggio: le correnti (1)',sub='La corrente sposta la barca: dallo stimato all\'osservato e il triangolo delle velocità. I 21 esercizi ufficiali 5.1.1, 5.2.1 e 5.3.1 sulla carta 5/D',
             fam='5.1.1-5.3.1 (carta 5/D, 21 esercizi)',quiz=['1.7.7-24','1.7.7-25','1.7.7-27']),
     14:dict(title='Carteggio: le correnti (2)',sub='Prora da tenere, ora di arrivo, velocità della corrente: i 18 esercizi ufficiali 5.4.1 della carta 5/D (Giglio e Argentario)',
             fam='5.4.1 (carta 5/D, 18 esercizi)',quiz=['1.7.7-29','1.7.7-15','1.7.7-11']),
     15:dict(title='Carteggio sulla carta 42/D',sub='Bocche di Bonifacio, Maddalena, Asinara e golfo di Olbia: navigazione costiera e correnti. I 23 esercizi ufficiali della 42/D',
             fam='5.5.3-5.8.3 e 5.5.1-5.8.1 (carta 42/D, 23 esercizi)',quiz=['1.7.7-28','1.7.7-2','1.7.7-4'])}[LES]

cover(LES,LEZ['title'],LEZ['sub'],f'Lezione {LES}. Esercizi ufficiali {LEZ["fam"]} dell\'Allegato A al DD 131/2022. Carte ridisegnate da OpenStreetMap; all\'esame si lavora sulle carte dell\'IIM.')

# ============ AGENDA ============
if LES==13:
    blocks=[('0:00','25′','La corrente, lo stimato, il triangolo',CORAL),('0:25','25′','Settore A: Elba (6 esercizi)',SEA),('0:50','25′','Settore B: Punta Ala (5)',PURPLE),('1:15','30′','Settore C: Pianosa e Montecristo (10)',BLUE),('1:45','15′','Ripasso',GREEN)]
    rule=('La regola','Dc = verso dove va','La corrente si nomina con la direzione verso cui scorre: il contrario del vento')
    three=['la traccia dà la prora o la rotta?','conosco la corrente o la devo trovare?','quanto tempo è passato tra A e B?']
elif LES==14:
    blocks=[('0:00','20′','Ripasso: triangolo e tempi',CORAL),('0:20','30′','Esercizi 5.4.1-1…6',SEA),('0:50','30′','Esercizi 5.4.1-7…12',PURPLE),('1:20','30′','Esercizi 5.4.1-13…18',BLUE),('1:50','10′','Ripasso',GREEN)]
    rule=('La regola','t = d ÷ Ve','Il tempo di arrivo si calcola con la velocità sul fondo, non con quella del motore')
    three=['disegna sempre un\'ora di triangolo','Ve si misura sulla rotta, fino al punto d\'incontro','la velocità si legge sulla scala delle latitudini']
else:
    blocks=[('0:00','15′','La carta 42/D, rilevamenti bussola',CORAL),('0:15','45′','Navigazione costiera (10 esercizi)',SEA),('1:00','25′','Correnti: Bonifacio e Maddalena (5)',PURPLE),('1:25','25′','Correnti: Asinara e Olbia (8)',BLUE),('1:50','10′','Congedo',GREEN)]
    rule=('La regola','Rilv = Rilb + δ + d','Declinazione e deviazione: est positive, ovest negative')
    three=['prima trasforma i dati bussola in veri','poi traccia i rilevamenti dai fari','con la corrente, un\'ora di triangolo']
tl=''.join(f'<div style="flex:{int(d[:-1])}; display:flex; flex-direction:column; gap:10px; border-top:10px solid {c}; padding:16px 12px 0px 0px"><p style="font-size:24px; font-weight:800; color:{c}">{t} · {d}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{INK}">{x}</p></div>' for t,d,x,c in blocks)
right=card(tag(rule[0])+f'<p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1.1; color:{INK}">{rule[1]}</p>'+p(rule[2],26,INK,700))
left=card(tag('Tre domande, sempre',SEA)+'<ul style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:10px">'+''.join(f'<li>{x}</li>' for x in three)+'</ul>',SEA_T,flex=1.4)
sec('agenda', head(f'Lezione {LES} · 2 ore','La lezione di oggi')+f'<div style="display:flex; gap:14px">{tl}</div><div style="display:flex; gap:24px">{left}{right}</div>',
 notes='Come nelle lezioni 10-12: per ogni esercizio una slide con la traccia e una con il tracciamento, con il nostro risultato e la forchetta ufficiale.')

intro=['cover','agenda']
if LES in (13,14):
    sec('corrente', head('Carteggio · la corrente','Il triangolo delle velocità'), pinned=svgp(128,Y,W,Hh,tb,'Triangolo delle velocità: il vettore del motore più il vettore della corrente dà il moto sul fondo')+tri_labels(128,Y)+pcol(
     term('Il motore','Spinge la barca nell\'acqua lungo la prora vera Pv, alla velocità propulsiva Vp.')+term('La corrente','Sposta tutta l\'acqua, e la barca con lei, verso Dc alla velocità Vc.')+term('Sul fondo','La somma dei due vettori è la rotta vera Rv con la velocità effettiva Ve: è lì che la barca va davvero.')),
     notes='Quiz 1.7.7-24, -25, -27 (deriva e corrente). In carteggio si disegna un\'ora di moto: un vettore lungo Vp miglia per la prora, uno lungo Vc miglia per la corrente. La terza lato è Rv e Ve.')
    intro.append('corrente')
if LES==13:
    lbl=pill(X+sA[0]-30,Y+sA[1]+30,200,'A',NAVY)+pill(X+(sA[0]+sSt[0])/2-100,Y+(sA[1]+sSt[1])/2-80,320,'stimato: Pv · Vp · t',NAVY)+pill(X+sB[0]-120,Y+sB[1]+30,280,'B osservato',CORAL)+pill(X+(sSt[0]+sB[0])/2+40,Y+(sSt[1]+sB[1])/2-30,300,'corrente: Dc e Vc',SEA)
    sec('stimato', head('Carteggio · trovare la corrente','Dallo stimato all\'osservato')+col(
     term('1 · Lo stimato','Da A traccia la prora vera per Vp × t miglia: è dove saresti senza corrente.')+term('2 · L\'osservato','Con i rilevamenti trovi B, dove sei davvero.')+term('3 · La corrente','Dallo stimato a B: la direzione è Dc, la lunghezza divisa per il tempo è Vc.')),
     pinned=svgp(X,Y,W,Hh,sb,'Il punto stimato calcolato con prora e velocità e il punto osservato: il segmento che li unisce è la corrente')+lbl,
     notes='Esempio 5.1.1-2: stimato e osservato a Capo d\'Enfola; Dc 225°. Attenzione al verso: dallo stimato verso l\'osservato, non il contrario.')
    intro.append('stimato')
if LES in (13,14):
    T=[('Hai Pv e corrente','Somma i vettori: da A traccia la prora per Vp, dalla punta la corrente per Vc. Da A alla punta: Rv e Ve.',CORAL,CORAL_T),
       ('Vuoi andare in B','Traccia la rotta A-B. Da A traccia la corrente; dalla punta apri il compasso di Vp e taglia la rotta: quella direzione è la Pv.',SEA,SEA_T),
       ('Hai A e B','Stimato da A con Pv e Vp; osservato B. Dallo stimato a B: Dc e Vc.',PURPLE,LILAC_T),
       ('Tempo e arrivo','Ve si misura sulla rotta fino al punto d\'incontro. Tempo = distanza ÷ Ve, poi somma all\'ora di partenza.',BLUE,BLUE_T)]
    tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:16px; background:{bg}; padding:36px; border-radius:32px"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,28,INK,600,1.4)}</div>' for t,d,c,bg in T)
    sec('problemi', head('Carteggio · i quattro casi','Quattro casi, quattro costruzioni')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:28px">{tiles}</div>',
     notes='Ogni esercizio di corrente è uno di questi quattro casi o una loro combinazione (per esempio 5.4.1-2: prima la Pv per andare in B, poi l\'ora di arrivo con la Ve).')
    intro.append('problemi')
if LES==14:
    A=(250,540); rv=58; B=P(rv,A,860); Cc=P(300,A,200); vp=470
    ur=(math.sin(math.radians(rv)),-math.cos(math.radians(rv))); dx,dy=A[0]-Cc[0],A[1]-Cc[1]
    bq=dx*ur[0]+dy*ur[1]; tt=-bq+math.sqrt(bq*bq-(dx*dx+dy*dy-vp*vp)); E=(A[0]+tt*ur[0],A[1]+tt*ur[1])
    ae=math.degrees(math.atan2(E[0]-Cc[0],-(E[1]-Cc[1])))
    b=SEA_BG+seg(A,B,CORAL,4,'14 10')+vecsvg(A,Cc,SEA)+vecsvg(Cc,E,NAVY)+vecsvg(A,E,CORAL,8)+dot(A)
    b+=f'<path d="M{P(ae-14,Cc,vp)[0]:.0f} {P(ae-14,Cc,vp)[1]:.0f} A{vp} {vp} 0 0 1 {P(ae+14,Cc,vp)[0]:.0f} {P(ae+14,Cc,vp)[1]:.0f}" fill="none" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="8 8"/>'
    b+=f'<circle cx="{B[0]:.0f}" cy="{B[1]:.0f}" r="16" fill="none" stroke="{CORAL}" stroke-width="6"/>'
    b+=f'<circle cx="960" cy="470" r="80" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/><line x1="960" y1="470" x2="960" y2="410" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/><line x1="960" y1="470" x2="1005" y2="490" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/>'
    lbl=(pill(X+A[0]-20,Y+A[1]+26,100,'A',NAVY)+pill(X+B[0]-90,Y+B[1]+26,100,'B',CORAL)+pill(X+Cc[0]-60,Y+Cc[1]+40,260,'corrente 1 h',SEA)
         +pill(X+(Cc[0]+E[0])/2-60,Y+(Cc[1]+E[1])/2-80,220,'Vp · Pv',NAVY)+pill(X+(A[0]+E[0])/2+40,Y+(A[1]+E[1])/2+10,260,'Ve (1 ora)',CORAL)+pill(X+830,Y+570,260,'t = d ÷ Ve',NAVY))
    sec('tempi', head('Carteggio · i conti','Tempi e velocità')+col(
     term('Ora di arrivo','Ve dal triangolo, distanza A-B sulla carta: t = d ÷ Ve. Esempio 5.4.1-2: arrivo alle 11h08m.')+
     term('Velocità da tenere','Per arrivare a un\'ora data: Ve = d ÷ t. La Vp che serve è la distanza dal vertice della corrente al punto sulla rotta.')+
     term('Corrente dal fondo','Tra due punti noti la velocità sul fondo è AB ÷ t: togli il vettore del motore e resta la corrente.')),
     pinned=svgp(X,Y,W,Hh,b,'Triangolo delle velocità sulla rotta da A a B: la velocità effettiva si misura dal punto A al punto dove il compasso di Vp taglia la rotta')+lbl,
     notes='5.4.1-9 (Vp da tenere), 5.4.1-10 e -16 (velocità della corrente), 5.4.1-18 (Ve). Il tempo si converte sempre in ore e minuti: 0,38 h = 23 minuti.')
    intro.append('tempi')
if LES==15:
    M=es10.Sol('5.5.4-1',(41.12,9.25)); M.pts=[]; M.lines=[]; M.carta='42D'
    for n,sh in {'Faro di Cap de Feno':'Cap de Feno','Faro di Capo Testa':'Capo Testa','Faro delle Isolette Monaci':'Monaci','Faro di Capo Ferro':'Capo Ferro','Ex semaforo di Capo Figari':'Capo Figari','Faro di Punta Timone':'Tavolara','Punta li Canneddi':'P.ta li Canneddi'}.items():
        try: M.pts.append((geo.lm(n),sh,'lm'))
        except KeyError: print('manca',n)
    M.pts.append(((40.82,8.6),'','none')); M.pts.append(((41.5,9.85),'','none'))
    sec('carta42', head('Carteggio · la seconda carta','La carta 42/D'), pinned=chart_html(M,128,290,1664,620,True,'Carta schematica delle Bocche di Bonifacio e della Sardegna nord-orientale con i fari degli esercizi'),
     notes='La 42/D copre le Bocche di Bonifacio, la Gallura, il golfo dell\'Asinara e la Corsica meridionale. Coste da OpenStreetMap (© contributori OSM, ODbL). Settori: A Bonifacio e Cap de Feno, B Maddalena e Monaci, C golfo dell\'Asinara, D golfo di Olbia.')
    T=[('Dalla bussola al vero','Rilv = Rilb + δ + d, Pv = Pb + δ + d. Esempio 5.8.3-1: Pb 317°, δ +4°, d −6°: Pv 315°.',CORAL,CORAL_T),
       ('Punto con due fari','Traccia i due rilevamenti veri dai fari verso il mare: il punto nave è l\'incrocio.',SEA,SEA_T),
       ('Punto e trasporto','Un rilevamento, poi navighi per un tempo noto: trasporta la prima retta lungo la rotta e incrocia con la seconda.',PURPLE,LILAC_T),
       ('Con la corrente','Stesso triangolo della 5/D: un\'ora di motore più un\'ora di corrente. Lezioni 13 e 14.',BLUE,BLUE_T)]
    tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:16px; background:{bg}; padding:36px; border-radius:32px"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,28,INK,600,1.4)}</div>' for t,d,c,bg in T)
    sec('bussola42', head('Carteggio · ripasso','Rilevamenti alla bussola')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:28px">{tiles}</div>',
     notes='Richiamo delle lezioni 10 (navigazione costiera) e 13-14 (correnti). Sulla 42/D la declinazione cambia da esercizio a esercizio: si usa quella scritta nella traccia.')
    intro+=['carta42','bussola42']
quiz_slide('quiz1',f'Quiz · {"La deriva" if LES==13 else ("Corrente e velocità" if LES==14 else "Rotta e prora")}',LEZ['quiz'],False)
quiz_slide('quiz1r','Quiz · Le risposte',LEZ['quiz'],True)
intro+=['quiz1','quiz1r']

# ============ ESERCIZI ============
SETT={'5.1':('5/D · A','Elba',SEA),'5.2':('5/D · B','Castiglione e Punta Ala',PURPLE),'5.3':('5/D · C','Pianosa e Montecristo',BLUE),'5.4':('5/D · D','Giglio e Argentario',GREEN),
      '5.5':('42/D · A','Bonifacio',CORAL),'5.6':('42/D · B','La Maddalena e Monaci',PURPLE),'5.7':('42/D · C','Golfo dell\'Asinara',BLUE),'5.8':('42/D · D','Golfo di Olbia',GREEN)}
def rng(r): return r.replace('\n',' ').replace('Ora traverso: ','').replace('Ora del traverso ','').replace('Lat.','Lat ').replace('Long.','Long ').replace('÷',' ÷ ')
def ask(S):
    t=S.res_txt.split()[0]
    return {'Pv':'la prora vera da tenere','Dc':'la direzione della corrente','Vc':'la velocità della corrente','Vp':'la velocità propulsiva','Ve':'la velocità effettiva',
            'Rv':'la rotta vera','Pb':'la prora bussola','arrivo':'l\'ora di arrivo','traverso':'l\'ora del traverso'}.get(t,'il tempo di navigazione' if S.kind=='tempo' else 'le coordinate del punto nave')
order_ex=[]; first={}
for S in SOLS:
    sid='s'+S.id.replace('.','_').replace('-','_'); st=SETT[S.id[:3]]
    first.setdefault(S.id[:7],sid+'_t')
    txt=S.ex['testo'].replace('\n',' ')
    fs=26 if len(txt)<520 else (24 if len(txt)<700 else (22 if len(txt)<860 else 20))
    left_col=f'<div style="display:flex; flex-direction:column; gap:20px; width:690px">{p(txt,fs,INK,500,1.42)}<p style="font-size:26px; font-weight:900; color:#FFFFFF; background:{st[2]}; padding:10px 20px; border-radius:18px">Da trovare: {ask(S)}</p></div>'
    sec(sid+'_t', head(f'Esercizio {S.id} · carta {st[0]} · {st[1]}','La traccia',st[2])+left_col, pinned=chart_html(S,880,290,912,620,False,f'Carta della zona dell\'esercizio {S.id}'),
        notes=f'Traccia ufficiale (Allegato A al DD 131/2022). Risposta ufficiale: {rng(S.ex["risposta_ufficiale"])}.')
    ol='<ol style="font-size:23px; line-height:1.36; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{x}</li>' for x in S.passi)+'</ol>'
    ok=S.check()
    extra=f'<p style="font-size:21px; font-weight:600; color:{INK}">{S.note}</p>' if S.note else ('' if ok else f'<p style="font-size:21px; font-weight:600; color:{INK}">Il nostro calcolo esce di poco dalla forchetta: vedi le note.</p>')
    res=f'<div style="display:flex; flex-direction:column; gap:4px; background:{CORAL_T}; padding:16px 20px; border-radius:20px"><p style="font-size:28px; font-weight:900; color:{CORAL}">{S.res_txt}</p><p style="font-size:22px; font-weight:700; color:{INK}">Ufficiale: {rng(S.ex["risposta_ufficiale"])}</p>{extra}</div>'
    sec(sid+'_s', head(f'Esercizio {S.id} · soluzione','Il tracciamento',st[2]), pinned=chart_html(S,128,290,1092,620,True,f'Tracciamento dell\'esercizio {S.id}')+pcol(ol+res,532,14),
        notes='Soluzione: '+' '.join(S.passi)+f' Risultato: {S.res_txt}. Ufficiale: {rng(S.ex["risposta_ufficiale"])}.'+('' if ok else ' Scarto rispetto alla forchetta ufficiale: sulla carta IIM si usano i simboli stampati, le nostre posizioni vengono da OpenStreetMap.'))
    order_ex+=[sid+'_t',sid+'_s']

if LES==13:
    closing(['La corrente si nomina per dove va: Dc','Dallo stimato all\'osservato: direzione Dc, lunghezza ÷ tempo = Vc','Il triangolo si disegna per un\'ora: Vp, Vc e Ve in miglia','Per andare in B: corrente da A, compasso di Vp, taglia la rotta: Pv','Il tempo si calcola con la Ve, non con la Vp'],
     'Prossima lezione · 14 · Correnti (seconda parte)','A casa: rifai sulla carta gli esercizi non svolti in aula.')
    secs={"s1":{"description":"Apertura: la corrente e i casi","start":"cover"},"s2":{"description":"Settore A: Elba","start":first['5.1.1-1']},"s3":{"description":"Settore B: Punta Ala","start":first['5.2.1-1']},"s4":{"description":"Settore C: Pianosa e Montecristo","start":first['5.3.1-1']}}
elif LES==14:
    closing(['Un\'ora di triangolo: Vp per la prora, Vc per la corrente','Pv da tenere: la prora «contro» la corrente','Ve sulla rotta: t = d ÷ Ve','Vp da tenere: dal vertice della corrente al punto sulla rotta','Due punti noti e il tempo: togli il motore, resta la corrente'],
     'Prossima lezione · 15 · La carta 42/D','A casa: rifai sulla carta gli esercizi 5.4.1 non svolti in aula.')
    secs={"s1":{"description":"Apertura e ripasso","start":"cover"},"s2":{"description":"Esercizi 5.4.1-1…9","start":first['5.4.1-1']},"s3":{"description":"Esercizi 5.4.1-10…18","start":'s5_4_1_10_t'}}
else:
    closing(['Prima i dati bussola: Rilv = Rilb + δ + d','Il rilevamento si traccia dal faro verso il mare','Trasporto: sposta la prima retta lungo la rotta percorsa','Correnti: lo stesso triangolo, su qualunque carta','All\'esame: matita morbida, compasso, squadrette e calma'],
     'Fine del corso · Buon vento per l\'esame!','Ripassa gli esercizi delle lezioni 10-15 e le schede dei quiz.')
    secs={"s1":{"description":"Apertura e carta 42/D","start":"cover"},"s2":{"description":"Navigazione costiera sulla 42/D","start":first['5.5.3-1']},"s3":{"description":"Correnti sulla 42/D","start":first['5.5.1-1']}}
write_deck(OUT,f'Lezione {LES} · {LEZ["title"]}',intro+order_ex+['chiusura'],secs)
print('slide',len(intro)+len(order_ex)+1)
