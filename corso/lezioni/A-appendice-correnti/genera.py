"""Appendice A: i tre problemi della corrente (slide di studio)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'cart'))
from lezione_base import *
import lezione_base as LB
import geo, chart, es10, escorr, json
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


# ======================= APPENDICE A: I TRE PROBLEMI DELLA CORRENTE =======================
OUT=SP+'/appA/project'
LB.ICON_T.update({'Indice':'book','Tre regole per tutti i problemi':'check','Problema 1 · Conosco la prora':'compass','Problema 2 · Voglio arrivare in B':'dividers',
 'Problema 3 · Che corrente c\'è?':'current','Esempio svolto':'map','Riepilogo':'grid','Gli errori che costano l\'esercizio':'flag'})
cover(0,'I tre problemi della corrente','Appendice di studio: il triangolo delle velocità, come riconoscere il problema e come risolverlo, con tre esercizi ufficiali svolti',
 'Appendice A al corso. Riassume le lezioni 13, 14 e 15: problema diretto (rotta ed effettiva), problema inverso (prora da tenere e ora di arrivo), ricerca della corrente (dallo stimato all\'osservato).')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice A · studio'))

# ---- indice ----
IDX=[('1','Il triangolo delle velocità','Motore + corrente = moto effettivo; le tre regole',CORAL,'03'),
     ('2','Problema 1 · Conosco la prora','Trovo rotta vera ed effettiva. Esempio 5.3.1-7',SEA,'05'),
     ('3','Problema 2 · Voglio arrivare in B','Trovo la prora da tenere e l\'ora di arrivo. Esempio 5.4.1-2',PURPLE,'07'),
     ('4','Problema 3 · Che corrente c\'è?','Dallo stimato all\'osservato. Esempio 5.1.1-2',BLUE,'09'),
     ('5','Riepilogo ed errori tipici','La tabella dei tre problemi e sei errori da evitare',GREEN,'11')]
rows=''.join(f'<div style="display:flex; align-items:center; gap:28px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:18px 32px"><p style="font-family:{H}; font-size:56px; font-weight:700; line-height:1; color:{c}; width:60px">{n}</p><div style="flex:1; display:flex; flex-direction:column; gap:4px">{p(t,32,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div><p style="font-size:26px; font-weight:900; color:#FFFFFF; background:{c}; padding:6px 18px; border-radius:16px">slide {s}</p></div>' for n,t,d,c,s in IDX)
sec('indice', head('Appendice A · I tre problemi della corrente','Indice')+f'<div style="display:flex; flex-direction:column; gap:16px">{rows}</div>',
 notes='Ogni problema ha una slide di metodo e una con un esercizio ufficiale svolto sulla carta 5/D. Gli esercizi completi sono nelle lezioni 13, 14 e 15.')

# ---- triangolo ----
sec('triangolo', head('1 · La base','Il triangolo delle velocità'), pinned=svgp(128,Y,W,Hh,tb+dot(tP,NAVY,9)+dot(tQ,SEA,9),'Triangolo delle velocità: il vettore del motore più il vettore della corrente dà il moto sul fondo')+tri_labels(128,Y)+pill(128+tP[0]-80,Y+tP[1]-50,70,'P',NAVY,26,align='center')+pill(128+tQ[0]+22,Y+tQ[1]+8,70,'Q',SEA,26,align='center')+pcol(
 term('Motore: Pv · Vp','Dove la spinge l\'elica, nell\'acqua.')+term('Corrente: Dc · Vc','Dove l\'acqua trascina tutto, barca compresa.')+term('Sul fondo: Rv · Ve','La somma dei due vettori: dove la barca va davvero.')+
 f'<p style="font-family:{H}; font-size:44px; font-weight:700; color:{CORAL}">Ve = Vp + Vc</p>'+p('somma di vettori: direzioni e lunghezze',24,BODY,600)+''),
 notes='Tutti gli esercizi di corrente si risolvono con questo solo disegno: cambia soltanto quale lato è incognito. Problema 1: la rotta. Problema 2: la prora. Problema 3: la corrente.')

T=[('La corrente va','Dc indica dove scorre l\'acqua: Dc 180° = verso sud. Il vento, al contrario, si nomina da dove viene.',CORAL,CORAL_T),
   ('Un\'ora di moto','Il vettore del motore è lungo Vp miglia, quello della corrente Vc miglia: le lunghezze si leggono come nodi.',SEA,SEA_T),
   ('Prima i dati veri','Pv = Pb + δ + d, Rilv = Rilb + δ + d: est positivo, ovest negativo.',PURPLE,LILAC_T),
   ('Miglia in latitudine','Le distanze si misurano sulla scala delle latitudini, all\'altezza del disegno.',BLUE,BLUE_T)]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:16px; background:{bg}; padding:36px; border-radius:32px"><p style="font-family:{H}; font-size:48px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,28,INK,600,1.4)}</div>' for t,d,c,bg in T)
sec('regole', head('1 · La base','Tre regole per tutti i problemi'.replace('Tre','Quattro'))+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:28px">{tiles}</div>',
 notes='Da ricordare prima di aprire il compasso. L\'errore più frequente all\'esame è leggere la corrente come il vento.')
LB.ICON_T['Quattro regole per tutti i problemi']='check'

def method(id_,eb,title,dati,cerco,steps,check,fig,alt,lbl,left_fig,c,notes):
    body=(f'<div style="display:flex; gap:14px"><p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:6px 16px; border-radius:14px">Dati: {dati}</p></div>'
          f'<p style="font-size:24px; font-weight:900; color:{c}">Si cerca: {cerco}</p>'
          '<ol style="font-size:26px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
          +f'<p style="font-size:24px; line-height:1.35; font-weight:700; color:{INK}; background:{SUN}33; padding:12px 16px; border-radius:16px">Controllo a occhio: {check}</p>')
    if left_fig:
        sec(id_, head(eb,title,c), pinned=svgp(128,Y,W,Hh,fig,alt)+lbl(128)+pcol(body,532,16), notes=notes)
    else:
        sec(id_, head(eb,title,c)+col(body,532,16), pinned=svgp(X+160,Y,W-160,Hh,fig,alt)+lbl(X+160), notes=notes)

def fix_pts(S,sid):
    from geo import add, sub, dist, brg, u
    from escorr import ll
    from escorr import vec, pv_for, ship_from
    ren=lambda old,new: [S.pts.__setitem__(i,(q[0],new,q[2])) for i,q in enumerate(S.pts) if q[1]==old]
    if sid=='5.3.1-7':
        A=S.xy((ll(42,25),ll(10,14.6))); S.pt(add(A,vec(55,6)),'P','ship'); ren('1 ora','Q · 1 ora')
        S.passi=['Da A: 6 mg per 055° (moto proprio), punto P.','Da P: 1,5 mg verso nord (corrente), punto Q.','A→Q è la rotta vera: Rv = 045°, Ve 7,0 kn.']
    if sid=='5.4.1-2':
        A=S.xy((ll(42,23.2),ll(10,56.8))); B=ship_from(S,'Faro di Talamone',305,0.5); rv=brg(A,B); pv,ve=pv_for(rv,7,75,3)
        C=add(A,vec(75,3)); E=add(A,vec(rv,ve))
        S.lines=[l for l in S.lines if l[2] not in ('rotta_l','corr')]
        S.line(A,C,'corr','corrente 075° · 3 kn'); S.line(C,E,'stima','Pv 029° · 7 kn'); S.pt(C,'C','ship'); S.pt(E,'E · Ve 9,3','ship')
        S.passi=['B: Talamone per 305° a 0,5 mg (B è a SE del faro).','Rotta A-B 042°, 13,0 mg.','Da A la corrente 075° per 3 mg: punto C.','Compasso in C aperto di 7 mg: taglia la rotta in E. C→E: Pv 029°; A–E: Ve 9,3 kn.','Tempo 13,0 ÷ 9,3 = 1h23m: arrivo alle 11h08m.']
    if sid=='5.1.1-2':
        ren('stimato','S · stimato')
        S.passi=['A: Polveraia per 112° a 1,8 mg.','Stimato S alle 09h18m: 6,8 mg per 350° (48 minuti a 8,5 kn).','Osservato B da GPS.','S→B: Dc = 225°; Vc = 2,9 mg in 48′ = 3,6 kn.']
def example(id_,sid,eb,c,note):
    S=[f() for f in escorr.SOLS[13]+escorr.SOLS[14] if f.__name__=='c'+sid.replace('.','_').replace('-','_')][0]
    fix_pts(S,sid)
    txt=S.ex['testo'].replace('\n',' ')
    ol='<ol style="font-size:23px; line-height:1.36; color:#34465E; display:flex; flex-direction:column; gap:8px">'+''.join(f'<li>{x}</li>' for x in S.passi)+'</ol>'
    res=f'<div style="display:flex; flex-direction:column; gap:4px; background:{CORAL_T}; padding:16px 20px; border-radius:20px"><p style="font-size:28px; font-weight:900; color:{CORAL}">{S.res_txt}</p><p style="font-size:22px; font-weight:700; color:{INK}">Ufficiale: {S.ex["risposta_ufficiale"].replace(chr(10)," ").replace("÷"," ÷ ")}</p></div>'
    sec(id_, head(f'{eb} · esercizio {sid}','Esempio svolto',c), pinned=chart_html(S,128,290,1092,620,True,f'Tracciamento dell\'esercizio {sid}')+pcol(ol+res,532,14),
        notes=f'Traccia ufficiale: {txt} {note}')

# ---- problema 1 ----
A1=(140,520); P1=P(55,A1,600); Q1=P(0,P1,150)
f1=SEA_BG[:-2].replace('1092','932')+'/>'+vecsvg(A1,P1,NAVY)+vecsvg(P1,Q1,SEA)+vecsvg(A1,Q1,CORAL,8)+dot(A1)+dot(P1,NAVY,10)+dot(Q1,SEA,10)
f1+=topboat(P(55,A1,250)[0]-40,P(55,A1,250)[1]+70,120,-35,'#FFFFFF',NAVY,4)
l1=lambda x0: pill(x0+P1[0]+22,Y+P1[1]+6,70,'P',NAVY,26,align='center')+pill(x0+Q1[0]-94,Y+Q1[1]-6,70,'Q',SEA,26,align='center')+pill(x0+A1[0]-30,Y+A1[1]+30,100,'A',NAVY)+pill(x0+(A1[0]+P1[0])/2+40,Y+(A1[1]+P1[1])/2+30,300,'Pv 055° · 6 mg',NAVY)+pill(x0+P1[0]+24,Y+(P1[1]+Q1[1])/2-10,200,'N · 1,5 mg',SEA)+pill(x0+(A1[0]+Q1[0])/2-300,Y+(A1[1]+Q1[1])/2-60,300,'Rv 045° · 7,0 kn',CORAL)
method('p1','2 · Il problema diretto','Problema 1 · Conosco la prora','Pv, Vp, Dc, Vc','rotta vera Rv ed effettiva Ve',
 ['Da A traccia la Pv per Vp miglia: punto P.','Da P traccia la corrente, Dc per Vc miglia: punto Q.','A→Q è la Rv; la sua lunghezza in miglia è la Ve in nodi.','Posizione dopo t ore: Ve × t miglia sulla Rv.'],
 'la rotta sta tra la prora e la corrente, più vicina alla prora se Vp ≫ Vc.',f1,'Somma dei vettori: 6 miglia per 055° più 1,5 miglia verso nord danno la rotta vera 045° a 7 nodi',l1,False,SEA,
 'Problema diretto: si sommano i vettori, punta dopo punta. Esercizi ufficiali: 5.3.1-7 (Rv), 5.3.1-9 (Ve).')
example('p1e','5.3.1-7','2 · Problema 1',SEA,'Pv 055°, Vp 6 kn, corrente verso nord a 1,5 kn: Rv 045°, Ve 7,0 kn.')

# ---- problema 2 ----
A=(250,540); rv=58; B=P(rv,A,860); Cc=P(300,A,200); vp=470
ur=(math.sin(math.radians(rv)),-math.cos(math.radians(rv))); dx,dy=A[0]-Cc[0],A[1]-Cc[1]
bq=dx*ur[0]+dy*ur[1]; tt=-bq+math.sqrt(bq*bq-(dx*dx+dy*dy-vp*vp)); E=(A[0]+tt*ur[0],A[1]+tt*ur[1])
ae=math.degrees(math.atan2(E[0]-Cc[0],-(E[1]-Cc[1])))
f2=SEA_BG+seg(A,B,CORAL,4,'14 10')+vecsvg(A,Cc,SEA)+vecsvg(Cc,E,NAVY)+vecsvg(A,E,CORAL,8)+dot(A)+dot(Cc,SEA,10)+dot(E,NAVY,10)
f2+=f'<path d="M{P(ae-14,Cc,vp)[0]:.0f} {P(ae-14,Cc,vp)[1]:.0f} A{vp} {vp} 0 0 1 {P(ae+14,Cc,vp)[0]:.0f} {P(ae+14,Cc,vp)[1]:.0f}" fill="none" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="8 8"/>'
f2+=f'<circle cx="{B[0]:.0f}" cy="{B[1]:.0f}" r="16" fill="none" stroke="{CORAL}" stroke-width="6"/>'
l2=lambda x0: (pill(x0+Cc[0]-40,Y+Cc[1]-62,70,'C',SEA,26,align='center')+pill(x0+E[0]+26,Y+E[1]+14,70,'E',NAVY,26,align='center')+pill(x0+A[0]-20,Y+A[1]+26,100,'A',NAVY)+pill(x0+B[0]-90,Y+B[1]+26,100,'B',CORAL)+pill(x0+Cc[0]-60,Y+Cc[1]+40,260,'1 · corrente',SEA)
         +pill(x0+(Cc[0]+E[0])/2-60,Y+(Cc[1]+E[1])/2-80,260,'2 · compasso Vp → Pv',NAVY)+pill(x0+(A[0]+E[0])/2+40,Y+(A[1]+E[1])/2+10,220,'3 · Ve',CORAL))
method('p2','3 · Il problema inverso','Problema 2 · Voglio arrivare in B','A, B, Vp, Dc, Vc','prora vera Pv, Ve, ora di arrivo',
 ['Traccia la rotta A–B e misura la distanza d.','Da A traccia la corrente, Dc per Vc miglia: punto C.','Compasso in C aperto di Vp: taglia la rotta in E.','C→E è la Pv; A–E è la Ve.','Tempo t = d ÷ Ve; arrivo = partenza + t.'],
 'la prora «punta contro» la corrente, dalla parte opposta della rotta.',f2,'Problema inverso: la corrente parte da A, il compasso aperto di Vp dalla sua punta taglia la rotta verso B',l2,True,PURPLE,
 'Varianti: per arrivare a un\'ora data, Ve = d ÷ t e la Vp da tenere è la lunghezza C–E (5.4.1-9). Esercizi ufficiali: 5.3.1-10, 5.4.1-2, 5.4.1-11…14.')
example('p2e','5.4.1-2','3 · Problema 2',PURPLE,'Rotta A–B 042°, 13,0 mg; Pv 029°, Ve 9,3 kn; 1h23m, arrivo alle 11h08m.')

# ---- problema 3 ----
l3=lambda x0: pill(x0+sSt[0]+22,Y+sSt[1]-54,70,'S',NAVY,26,align='center')+pill(x0+sA[0]-30,Y+sA[1]+30,100,'A',NAVY)+pill(x0+(sA[0]+sSt[0])/2-120,Y+(sA[1]+sSt[1])/2-80,320,'1 · stimato S: Pv, Vp × t',NAVY)+pill(x0+sB[0]-160,Y+sB[1]+30,280,'2 · B osservato',CORAL)+pill(x0+(sSt[0]+sB[0])/2+30,Y+(sSt[1]+sB[1])/2-40,260,'3 · Dc e Vc',SEA)
sb3=sb.replace('width="1092"','width="932"')
method('p3','4 · Trovare la corrente','Problema 3 · Che corrente c\'è?','A, Pv, Vp, tempo t, punto osservato B','direzione Dc e velocità Vc della corrente',
 ['Da A traccia la Pv per Vp × t miglia: punto stimato S.','Trova il punto osservato B (rilevamenti o GPS).','S→B è la deriva: la direzione è la Dc.','Lunghezza S–B ÷ t = Vc.'],
 'sempre dallo stimato verso l\'osservato: al contrario la Dc sbaglia di 180°.',sb3,'Dal punto stimato al punto osservato: il segmento che li unisce è la corrente',l3,False,BLUE,
 'Con due punti noti e la rotta: la velocità sul fondo è A–B ÷ t; togli il vettore del motore e resta la corrente (5.4.1-10, 5.4.1-16). Esercizi ufficiali: 5.1.1-2, 5.2.1-5, 5.3.1-1.')
example('p3e','5.1.1-2','4 · Problema 3',BLUE,'Stimato 6,8 mg per 350° in 48 minuti; da S a B: Dc 225°, 2,9 mg, Vc 3,6 kn.')

# ---- riepilogo ----
R=[('1 · diretto','Pv, Vp, Dc, Vc','Rv, Ve','motore + corrente in fila; chiudi il triangolo','5.3.1-7, 5.3.1-9',SEA),
   ('2 · inverso','A, B, Vp, Dc, Vc','Pv, Ve, ora di arrivo','corrente da A, compasso di Vp sulla rotta','5.3.1-10, 5.4.1-2, da 5.4.1-11 a 5.4.1-14',PURPLE),
   ('3 · corrente','A, Pv, Vp, t, B','Dc, Vc','dallo stimato all\'osservato','5.1.1-2, 5.2.1-5, 5.3.1-1',BLUE)]
th=''.join(f'<th style="width:{w}%">{t}</th>' for t,w in (('Problema',14),('Conosco',18),('Cerco',16),('Costruzione',30),('Esercizi ufficiali',22)))
tr=''.join(f'<tr><td style="color:{c}; font-weight:800; padding:22px 14px">{a}</td><td>{b}</td><td style="font-weight:800">{cc}</td><td>{d}</td><td>{e}</td></tr>' for a,b,cc,d,e,c in R)
sec('riepilogo', head('5 · Riepilogo','Riepilogo',GREEN)+f'<table style="font-size:30px; line-height:1.4; color:{INK}; background:#FFFFFF; border-radius:24px; padding:24px"><tr>{th}</tr>{tr}</table>'
 +note('Stesso disegno, tre incognite diverse: prima di tracciare, chiediti quale lato manca.',GREEN,38),
 notes='Tabella da ricopiare sul quaderno. Gli esercizi citati sono svolti passo per passo nelle lezioni 13, 14 e 15.')

E6=[('Corrente come vento','Dc indica dove va l\'acqua, non da dove viene.'),('Vp al posto di Ve','Il tempo di arrivo si calcola con la velocità sul fondo.'),
    ('Compasso da A','Nel problema 2 il compasso si apre dalla punta della corrente.'),('Verso sbagliato','Nel problema 3 si misura dallo stimato all\'osservato.'),
    ('Minuti e decimali','48 minuti = 0,8 h; 0,38 h = 23 minuti.'),('Scala sbagliata','Le miglia si leggono sulla scala delle latitudini.')]
cols=[CORAL,SEA,PURPLE,BLUE,GREEN,CORAL]; bgs=[CORAL_T,SEA_T,LILAC_T,BLUE_T,SEA_T,CORAL_T]
tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:10px; background:{bgs[i]}; padding:44px 36px; border-radius:28px"><p style="font-family:{H}; font-size:44px; font-weight:700; line-height:1.05; color:{cols[i]}">{i+1} · {t}</p>{p(d,30,INK,600,1.4)}</div>' for i,(t,d) in enumerate(E6))
sec('errori', head('5 · Riepilogo','Gli errori che costano l\'esercizio',CORAL)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:32px">{tiles}</div>',
 notes='Sei errori visti più spesso negli esercizi di corrente. Prima di consegnare, ricontrolla questi sei punti.')

closing(['Un solo disegno: motore + corrente = moto effettivo','Problema 1: conosco la prora, sommo i vettori e trovo Rv e Ve','Problema 2: voglio arrivare in B, corrente da A e compasso di Vp: trovo la Pv','Problema 3: dallo stimato all\'osservato trovo Dc e Vc','Il tempo si calcola sempre con la Ve'],
 'Torna alle lezioni 13, 14 e 15 per tutti gli esercizi','Appendice A · I tre problemi della corrente')
write_deck(OUT,'Appendice A · I tre problemi della corrente',['cover','indice','triangolo','regole','p1','p1e','p2','p2e','p3','p3e','riepilogo','errori','chiusura'],
 {"s1":{"description":"Copertina e indice","start":"cover"},"s2":{"description":"Il triangolo delle velocità","start":"triangolo"},"s3":{"description":"Problema 1: rotta ed effettiva","start":"p1"},
  "s4":{"description":"Problema 2: prora da tenere e ora di arrivo","start":"p2"},"s5":{"description":"Problema 3: trovare la corrente","start":"p3"},"s6":{"description":"Riepilogo ed errori tipici","start":"riepilogo"}})
