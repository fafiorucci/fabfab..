"""Appendice F: schede del segnalamento marittimo AISM-IALA (Regione A), di giorno e di notte."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/deck/project'
GREY='#97A6B4'; NIGHT='#0F2238'; SIL='#2C4463'; SKY='#EAF4F7'; LAND='#F2E2B3'; LAND_S='#C9A96B'
LRED='#E23B3B'; LGREEN='#1FB35A'; LWHITE='#FFF7D6'; LYEL='#FFD84D'; MBLACK='#1B2330'; MYEL='#F2C230'; ORANGE='#F28C28'

ORDER=['cover','indice','sistema','luci','parole','quizA','quizAr',
       'sinistra','dritta','preferito','quizB','quizBr',
       'rosa','nord','est','sud','ovest','quizC','quizCr',
       'isolato','sicure','speciale','quizD','quizDr',
       'riepilogo','giorno','giornor','notte','notter','fluviale','chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
EB='Appendice F · Schede IALA'
LB.ICON_T.update({'Indice':'book','Il sistema AISM-IALA':'flag','Leggere una luce':'lighthouse','Le parole del segnalamento':'book',
 'Laterale di sinistra':'flag','Laterale di dritta':'flag','Il canale preferito':'flag','Le cardinali e l\'orologio':'compass',
 'Cardinale Nord':'compass','Cardinale Est':'compass','Cardinale Sud':'compass','Cardinale Ovest':'compass',
 'Pericolo isolato':'lighthouse','Acque sicure':'lighthouse','Segnale speciale':'lighthouse','Tutte le schede in una':'grid',
 'Di giorno: chi sono?':'star','Di giorno: le risposte':'check','Di notte: chi sono?':'star','Di notte: le risposte':'check','Navigazione fluviale':'map'})
X,Y,W,Hh=700,290,1092,620

# ---------- disegno dei segnali (in elevazione) ----------
UID=[0]
def cone(x,y,up,s=22,c=MBLACK):
    return f'<path d="M{x-s*0.6:.1f} {y+s/2:.1f} L{x+s*0.6:.1f} {y+s/2:.1f} L{x:.1f} {y-s/2:.1f} Z" fill="{c}"/>' if up else f'<path d="M{x-s*0.6:.1f} {y-s/2:.1f} L{x+s*0.6:.1f} {y-s/2:.1f} L{x:.1f} {y+s/2:.1f} Z" fill="{c}"/>'
SH={'can':80,'cone':92,'pillar':150,'spar':170,'sphere':78}
def shape_d(x,y,sh,s):
    if sh=='can': return f'M{x-34*s:.1f} {y:.1f} L{x+34*s:.1f} {y:.1f} L{x+34*s:.1f} {y-80*s:.1f} L{x-34*s:.1f} {y-80*s:.1f} Z'
    if sh=='cone': return f'M{x-44*s:.1f} {y:.1f} L{x+44*s:.1f} {y:.1f} L{x:.1f} {y-92*s:.1f} Z'
    if sh=='pillar': return (f'M{x-52*s:.1f} {y:.1f} L{x+52*s:.1f} {y:.1f} L{x+42*s:.1f} {y-30*s:.1f} L{x+18*s:.1f} {y-30*s:.1f} L{x+14*s:.1f} {y-150*s:.1f} '
                             f'L{x-14*s:.1f} {y-150*s:.1f} L{x-18*s:.1f} {y-30*s:.1f} L{x-42*s:.1f} {y-30*s:.1f} Z')
    if sh=='spar': return f'M{x-12*s:.1f} {y:.1f} L{x+12*s:.1f} {y:.1f} L{x+10*s:.1f} {y-170*s:.1f} L{x-10*s:.1f} {y-170*s:.1f} Z'
    if sh=='sphere': r=44*s; c=y-r+10*s; return f'M{x-r:.1f} {c:.1f} A{r:.1f} {r:.1f} 0 1 1 {x+r:.1f} {c:.1f} A{r:.1f} {r:.1f} 0 1 1 {x-r:.1f} {c:.1f} Z'
def buoy(x,y,sh,bands,top,s=1.0,vert=None,sil=None):
    """bands: colori dall'alto (fasce orizzontali); vert: colori a strisce verticali; top: miraglio [(tipo,param)]; sil: colore unico (notte)"""
    UID[0]+=1; cid=f'cb{UID[0]}'; h=SH[sh]*s; d=shape_d(x,y,sh,s); g=''
    if not sil: g+=f'<ellipse cx="{x}" cy="{y:.1f}" rx="{60*s:.1f}" ry="{9*s:.1f}" fill="{WATER}" fill-opacity="0.35"/>'
    g+=f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">'
    if sil: g+=f'<rect x="{x-60*s:.1f}" y="{y-h-2:.1f}" width="{120*s:.1f}" height="{h+4:.1f}" fill="{sil}"/>'
    elif vert:
        n=len(vert)*2; ww=110*s/n
        for i in range(n): g+=f'<rect x="{x-55*s+i*ww:.1f}" y="{y-h-2:.1f}" width="{ww+0.6:.1f}" height="{h+4:.1f}" fill="{vert[i%len(vert)]}"/>'
    else:
        bh=h/len(bands)
        for i,c in enumerate(bands): g+=f'<rect x="{x-60*s:.1f}" y="{y-h+i*bh-1:.1f}" width="{120*s:.1f}" height="{bh+2:.1f}" fill="{c}"/>'
    g+='</g>'
    if not sil: g+=f'<path d="{d}" fill="none" stroke="{NAVY}" stroke-width="{max(2,3*s):.1f}" stroke-linejoin="round"/>'
    ty=y-h
    if top:
        pc=sil or NAVY; g+=f'<path d="M{x} {ty:.1f} V{ty-26*s:.1f}" stroke="{pc}" stroke-width="{3*s:.1f}"/>'; ty-=40*s
        for kind,par in top:
            c=sil or (par if isinstance(par,str) and par.startswith('#') else MBLACK)
            if kind=='cu': g+=cone(x,ty,True,24*s,sil or par); ty-=28*s
            elif kind=='cd': g+=cone(x,ty,False,24*s,sil or par); ty-=28*s
            elif kind=='ball': g+=f'<circle cx="{x}" cy="{ty:.1f}" r="{12*s:.1f}" fill="{c}"/>'; ty-=28*s
            elif kind=='can': g+=f'<rect x="{x-11*s:.1f}" y="{ty-12*s:.1f}" width="{22*s:.1f}" height="{24*s:.1f}" fill="{c}"/>'; ty-=30*s
            elif kind=='x': g+=f'<path d="M{x-12*s:.1f} {ty-12*s:.1f} L{x+12*s:.1f} {ty+12*s:.1f} M{x+12*s:.1f} {ty-12*s:.1f} L{x-12*s:.1f} {ty+12*s:.1f}" stroke="{sil or MYEL}" stroke-width="{7*s:.1f}" stroke-linecap="round"/>'; ty-=30*s
    return g, ty
def B(*a,**k): return buoy(*a,**k)[0]
# i segnali: (forma per la scheda, fasce, strisce verticali, miraglio, colore della luce)
TOP={'sx':[('can',LRED)],'dx':[('cu',LGREEN)],'N':[('cu',MBLACK),('cu',MBLACK)],'E':[('cd',MBLACK),('cu',MBLACK)],
     'S':[('cd',MBLACK),('cd',MBLACK)],'W':[('cu',MBLACK),('cd',MBLACK)],'iso':[('ball',MBLACK),('ball',MBLACK)],
     'safe':[('ball',LRED)],'spec':[('x',0)],'psx':[('can',LRED)],'pdx':[('cu',LGREEN)]}
BAND={'sx':[LRED],'dx':[LGREEN],'N':[MBLACK,MYEL],'E':[MBLACK,MYEL,MBLACK],'S':[MYEL,MBLACK],'W':[MYEL,MBLACK,MYEL],
      'iso':[MBLACK,LRED,MBLACK],'safe':None,'spec':[MYEL],'psx':[LRED,LGREEN,LRED],'pdx':[LGREEN,LRED,LGREEN]}
VERT={'safe':[LRED,'#FFFFFF']}
def mk(k,x,y,sh,s=1.0,sil=None): return buoy(x,y,sh,BAND[k],TOP[k],s,VERT.get(k),sil)

# ---------- luci ----------
def fl(ts,d=0.5): return [(t,t+d) for t in ts]
PAT={'sx':('Lam r 5s',15,fl([0,5,10]),LRED),'dx':('Lam v 5s',15,fl([0,5,10]),LGREEN),
     'N':('Sc · luce continua',12,fl(range(12),0.4),LWHITE),'E':('Sc (3) 10s',20,fl([0,1,2,10,11,12],0.4),LWHITE),
     'S':('Sc (6) + Lam lungo 15s',15,fl(range(6),0.4)+[(6,8)],LWHITE),'W':('Sc (9) 15s',15,fl(range(9),0.4),LWHITE),
     'iso':('Lam (2) 10s',20,fl([0,1.5,10,11.5]),LWHITE),'safe':('Iso 4s',16,[(0,2),(4,6),(8,10),(12,14)],LWHITE),
     'spec':('Lam (5) g 20s',20,fl([0,1.5,3,4.5,6]),LYEL),'psx':('Lam (2+1) r 10s',20,fl([0,1.2,3.6,10,11.2,13.6]),LRED),
     'pdx':('Lam (2+1) v 10s',20,fl([0,1.2,3.6,10,11.2,13.6]),LGREEN)}
def strip(x0,y0,w,k,h=40):
    _,T,segs,c=PAT[k]; sx=w/T
    return f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="8" fill="#060F1C"/>'+''.join(f'<rect x="{x0+a*sx:.1f}" y="{y0+5}" width="{max(5,(e-a)*sx):.1f}" height="{h-10}" rx="5" fill="{c}"/>' for a,e in segs)
def glow(x,y,c,r=9):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.8:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.7:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'

# ---------- testo ----------
def pcol(inner,w=532,gap=18,left=1260): return f'<div style="position:absolute; left:{left}px; top:290px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'
col=lambda inner,w=520,gap=18: f'<div style="display:flex; flex-direction:column; gap:{gap}px; width:{w}px">{inner}</div>'
def pill(x,y,w,t,c,size=22,tc='#FFFFFF'):
    return lab(x,y,w,t,tc,size,900,'left',bg=c).replace(f'width:{w}px;',f'width:max-content; max-width:{w}px;')
def idrow(k,v,c): return f'<div style="display:flex; flex-direction:column; gap:2px"><p style="font-size:24px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:{c}">{k}</p><p style="font-size:27px; line-height:1.3; font-weight:700; color:{INK}">{v}</p></div>'

# ---------- la scheda ----------
def scheda(sid,title,eyebrow,k,shapes,rows,trick,c,notes,left):
    X=128 if left else 700
    b=f'<rect x="0" y="0" width="700" height="620" fill="{SKY}"/><rect x="0" y="470" width="700" height="150" fill="{WATER}" fill-opacity="0.3"/>'+line(0,470,700,470,SEA,3)
    n=len(shapes); xs=[700*(i+0.5)/n for i in range(n)]
    for x,sh in zip(xs,shapes): b+=mk(k,x,470,sh,1.25 if n<3 else 1.1)[0]
    b+=f'<rect x="720" y="20" width="352" height="580" rx="22" fill="{NIGHT}"/>'
    g,ty=mk(k,896,400,shapes[0],1.0,SIL)
    b+=f'<rect x="740" y="400" width="312" height="3" fill="{SIL}"/>'+g+glow(896,ty+4,PAT[k][3],10)
    b+=strip(744,470,304,k)
    lbl=pill(X+20,Y+20,200,'di giorno',c)+pill(X+740,Y+36,200,'di notte',NAVY)
    names={'can':'boa cilindrica','cone':'boa conica','pillar':'boa a colonna','spar':'asta','sphere':'boa sferica'}
    lbl+=''.join(lab(X+x-110,Y+490,220,names[sh],NAVY,24,800,'center') for x,sh in zip(xs,shapes))
    lbl+=lab(X+734,Y+524,324,PAT[k][0],LYEL if PAT[k][3]==LYEL else '#FFFFFF',24,900,'center')
    alt=f'{title}: di giorno ' + ', '.join(names[s] for s in shapes) + ' con colori e miraglio della scheda; di notte la sua luce, ' + PAT[k][0]
    txt=''.join(idrow(a,v,c) for a,v in rows)+note(trick,c,34)
    body=svgp(X,Y,W,Hh,b,alt)+lbl
    if left: sec(sid, head(eyebrow,title,c), pinned=body+pcol(txt), notes=notes)
    else: sec(sid, head(eyebrow,title,c)+col(txt), pinned=body, notes=notes)

def mini(k,sh,s=0.62,w=150,h=190):
    g=f'<rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="{SKY}"/><rect x="0" y="{h-30}" width="{w}" height="30" fill="{WATER}" fill-opacity="0.3"/>'
    return svgi(w,h,g+mk(k,w/2,h-30,sh,s)[0],'Segnale in miniatura',pan=False)

# ============ COPERTINA ============
cover(0,'Schede IALA','Tutti i segnali del sistema AISM-IALA, uno per scheda: com\'è di giorno, come si riconosce di notte, come si passa',
 'Appendice F al corso. Schede di ripasso del segnalamento marittimo (Regione A), da usare con la lezione 6. Ogni segnale ha la sua scheda con forma, colori, miraglio, luce e significato; poi esercizi di riconoscimento e quiz ufficiali del gruppo 1.5.3.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice F · studio'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
IX=[('Le basi','Il sistema, le luci, le parole',['sistema','luci','parole','quizA','quizAr'],CORAL),
    ('Laterali','Sinistra, dritta, canale preferito',['sinistra','dritta','preferito','quizB','quizBr'],SEA),
    ('Cardinali','Nord, Est, Sud, Ovest',['rosa','nord','est','sud','ovest','quizC','quizCr'],PURPLE),
    ('Gli altri segnali','Pericolo isolato, acque sicure, speciale',['isolato','sicure','speciale','quizD','quizDr'],BLUE),
    ('Allenamento','Riepilogo, riconoscere di giorno e di notte',['riepilogo','giorno','giornor','notte','notter'],GREEN),
    ('Navigazione fluviale','I quiz sui fiumi',['fluviale'],ORANGE)]
cards=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:18px 24px">'
              f'<p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:64px">{i+1:02d}</p>'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:4px">{p(t,32,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div>'
              f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(ids[0])}{"–"+N(ids[-1]) if len(ids)>1 else ""}</p></div>' for i,(t,d,ids,c) in enumerate(IX))
sec('indice', head(EB,'Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:18px">{cards}</div>'
    +note('Ogni scheda ha la stessa forma: di giorno a sinistra, di notte a destra, la carta d\'identità accanto.',SEA,36),
 notes='Appendice di ripasso della lezione 6. Le schede seguono l\'ordine del sistema: laterali, cardinali, pericolo isolato, acque sicure, speciali. I quiz sono tutti ufficiali (DD 131/2022, gruppo 1.5.3, fanali luminosi e sistema IALA, 120 quesiti).')

# ============ IL SISTEMA ============
SY=[('sx','can','Laterali','Il lato del canale: rosso a sinistra, verde a dritta.',CORAL),
    ('N','pillar','Cardinali','Il lato del pericolo, con la bussola.',PURPLE),
    ('iso','pillar','Pericolo isolato','Un pericolo piccolo, proprio lì.',BLUE),
    ('safe','sphere','Acque sicure','Acqua navigabile tutto intorno.',SEA),
    ('spec','can','Speciali','Zone particolari: cavi, condotte, esercitazioni.',ORANGE)]
cc=''.join(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:20px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{mini(k,sh,0.8,200,210)}{h3(t,30,c)}<p style="font-size:24px; line-height:1.35; color:{BODY}; text-align:center">{d}</p></div>' for k,sh,t,d,c in SY)
ra1=p("<b>Regione A</b> · Europa, Africa, gran parte dell'Asia, Oceania",26,INK,400,1.35)
ra2=p("Entrando in porto: <b>rosso a sinistra</b>, verde a dritta. È il sistema del Mediterraneo.",26,BODY,400,1.35)
rb1=p("<b>Regione B</b> · Americhe, Giappone, Corea, Filippine",26,INK,400,1.35)
rb2=p("I colori dei laterali sono invertiti. Tutti gli altri segnali sono uguali.",26,BODY,400,1.35)
box=lambda bg,a,b_: f'<div style="flex:1; background:{bg}; border-radius:24px; padding:22px 26px; display:flex; flex-direction:column; gap:6px">{a}{b_}</div>'
AB=f'<div style="display:flex; gap:22px">{box(SEA_T,ra1,ra2)}{box(LILAC_T,rb1,rb2)}</div>'
sec('sistema', head(EB,'Il sistema AISM-IALA',CORAL)+f'<div style="display:flex; gap:18px; align-items:stretch">{cc}</div>'+AB,
 notes='Quiz 1.5.3-49 (i tipi: laterali, cardinali, pericolo isolato, acque sicure, speciali), -32 (nel Mediterraneo Sistema A, rosso a sinistra), -46 (tra le regioni A e B cambiano solo i laterali), -44 (di giorno il significato è dato da forma e colore della boa o del miraglio). Il sistema IALA prevede anche il segnale di nuovo pericolo, con bande verticali blu e gialle: non compare nei quiz.')

# ============ LEGGERE UNA LUCE ============
X=128
rows=[('F','fissa',[(0,12)],LWHITE),('Lam · Fl','a lampi',fl([0,3,6,9],0.4),LWHITE),('Lam (2) · Fl (2)','a gruppi',fl([0,1.2,6,7.2],0.4),LWHITE),
      ('Lam lungo · LFl','lampo lungo',[(0,2),(6,8)],LWHITE),('Int · Oc','intermittente',[(t,t+2.2) for t in (0,3,6,9)],LWHITE),
      ('Iso','isofase',[(t,t+1.5) for t in (0,3,6,9)],LWHITE),('Sc · Q','scintillante',fl(range(12),0.4),LWHITE),
      ('Alt b.r. · Al','alternata b. r.',[],None)]
x0,x1=470,1060; sx=(x1-x0)/12
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
for i,(a,d,segs,c) in enumerate(rows):
    y=24+i*72; b+=f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="44" rx="8" fill="{NIGHT}"/>'
    for j,(s0,e0) in enumerate(segs):
        b+=f'<rect x="{x0+s0*sx:.1f}" y="{y+6}" width="{max(6,(e0-s0)*sx):.1f}" height="32" rx="6" fill="{c}"/>'
    if c is None: b+=''.join(f'<rect x="{x0+j*1.5*sx:.1f}" y="{y+6}" width="{1.5*sx-4:.1f}" height="32" rx="6" fill="{LWHITE if j%2==0 else LRED}"/>' for j in range(8))
lbl=''.join(lab(X+16,Y+30+i*72,440,f'<b>{a}</b> · {d}',NAVY,24,500) for i,(a,d,_,_) in enumerate(rows))
txt=(idrow('La caratteristica','Tipo di luce, colore e periodo: di notte un faro si riconosce così.',CORAL)
     +idrow('Il periodo','Il tempo di un ciclo completo di luci e buio. «0,5 – 1 – 0,5 – 2» fa 4 secondi.',CORAL)
     +idrow('Come si legge','«Lam (2) 12s 27m 17M»: 2 lampi ogni 12 secondi, luce a 27 m sul mare, portata 17 miglia.',CORAL)
     +idrow('Il colore','Se non è scritto è bianca; r rossa, v verde, g gialla.',CORAL))
sec('luci', head('Le basi · lezione 6','Leggere una luce',CORAL), pinned=svgp(X,Y,W,Hh,b,'Otto strisce notturne che mostrano nel tempo luce fissa, a lampi, a gruppi di lampi, a lampo lungo, intermittente, isofase, scintillante e alternata bianca e rossa')+lbl+pcol(txt),
 notes='Sigle italiane dell\'Elenco fari e, dopo il punto, quelle inglesi delle carte internazionali. Quiz 1.5.3-56 e -77 (caratteristica), -47, -80, -81 (periodo: 0,5+1+0,5+2 = 4 s; 1,5+2+1,5+2 = 7 s), -41, -48, -35, -34, -45, -68 (lettura delle sigle), -7 e -92 (Sc = scintillante), -9 e -94 (Int = intermittente), -38 (Iso: luce uguale all\'eclisse), -8, -75, -76, -93 (alternata). Attenzione al quiz 1.5.3-37: traduce Oc con «intermittente».')
X=700

# ============ LE PAROLE ============
PW=[('Faro','Luce potente per riconoscere la costa. Si distingue dal fanale per la portata.',CORAL),
    ('Fanale','Luce più piccola: segnala entrate dei porti, moli, boe, pericoli.',SEA),
    ('Portata nominale','Quella con visibilità meteorologica di 10 miglia. È quella scritta sulla carta.',PURPLE),
    ('Portata geografica','Dipende dalla curvatura della Terra, dall\'altezza della luce e dell\'occhio.',BLUE),
    ('Meda','Costruzione o palo fisso sul fondo, che emerge dall\'acqua.',GREEN),
    ('Riflettore radar','Rende il segnale ben visibile sullo schermo radar.',ORANGE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:26px 28px">{h3(t,34,c)}{p(d,28,BODY,400,1.4)}</div>' for t,d,c in PW)
sec('parole', head('Le basi · lezione 6','Le parole del segnalamento',SEA)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px">{g}</div>'
    +note('Boa luminosa: un segnale luminoso galleggiante, ancorato al fondo.',SEA,36),
 notes='Quiz 1.5.3-29, -57, -61 (fari e fanali, la portata nominale li distingue), -2, -31, -63, -87 (portata nominale), -79 (sulla carta è indicata la nominale), -3, -28, -88 (portata geografica), -1, -30, -39, -86 (portata luminosa), -62 (meda), -10 e -95 (riflettore radar), -5, -6, -90, -91 (boe luminose), -58 (gavitelli: piccoli galleggianti per segnalazioni temporanee).')

quiz_slide('quizA','Verifica · luci e portate',['1.5.3-38','1.5.3-80','1.5.3-41'],False)
quiz_slide('quizAr','Verifica · luci e portate',['1.5.3-38','1.5.3-80','1.5.3-41'],True)

# ============ LATERALI ============
scheda('sinistra','Laterale di sinistra','Laterali · Regione A','sx',['can','pillar','spar'],
 [('Colore','Rosso'),('Forma','Cilindrica, a colonna o ad asta'),('Miraglio','Un cilindro rosso'),('Luce','Rossa, con qualunque ritmo tranne Lam (2+1)'),('Significato','Entrando in porto la lasci alla tua sinistra')],
 'Rosso a sinistra, come il fanale di via di sinistra.',LRED,
 'Quiz 1.5.3-27 (il laterale dice da che lato lasciarlo, secondo la direzione convenzionale), -43 (a sinistra entrando: rosso, cilindrico, miraglio cilindrico), -110 (figura), -32 (Regione A). La direzione convenzionale è quella di chi arriva dal mare verso il porto o risale un canale. Uscendo dal porto i lati si invertono: il rosso resta alla dritta.',True)
scheda('dritta','Laterale di dritta','Laterali · Regione A','dx',['cone','pillar','spar'],
 [('Colore','Verde'),('Forma','Conica, a colonna o ad asta'),('Miraglio','Un cono verde con la punta in alto'),('Luce','Verde, con qualunque ritmo tranne Lam (2+1)'),('Significato','Entrando in porto la lasci alla tua dritta')],
 'Verde a dritta, come il fanale di via di dritta.',GREEN_S,
 'Quiz 1.5.3-111 (figura: segnale di dritta entrando), 1.4.1-8 e -13 (imboccatura del porto: rosso a sinistra, verde a dritta). Sui moli i fanali ripetono i colori: rosso su quello di sinistra, verde su quello di dritta.',False)
# canale preferito: due segnali nella stessa scheda
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/>'
b+=f'<path d="M0 620 L0 380 Q300 360 420 250 L560 0 L1092 0 L1092 620 Z" fill="{WATER}" fill-opacity="0.25"/>'
b+=f'<path d="M0 0 L520 0 L400 210 Q300 320 0 330 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=f'<path d="M620 620 L700 440 Q760 330 1092 320 L1092 620 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=dpath('M300 600 Q420 520 520 400 Q700 380 1060 200',CORAL,6)+dpath('M520 400 Q600 260 720 60',SEA,5)
b+=B(640,330,'can',BAND['psx'],TOP['psx'],0.8)
b+=f'<rect x="760" y="470" width="300" height="130" rx="18" fill="{NIGHT}"/>'+strip(780,540,260,'psx')
b+=topboat(300,590,90,-60,'#FFFFFF',NAVY,4)
lbl=pill(X+860,Y+310,220,'canale principale',CORAL)+pill(X+740,Y+30,300,'canale secondario',SEA)+lab(X+780,Y+486,260,'Lam (2+1) r 10s',LWHITE,24,900,'center')+lab(X+680,Y+240,260,'rossa, fascia verde',NAVY,24,800)
txt=(idrow('Dove sono','Al bivio tra due canali, entrando dal mare',PURPLE)
     +idrow('Rossa con fascia verde','Cilindrica, luce rossa Lam (2+1). Il canale principale è a dritta: la lasci a sinistra',LRED)
     +idrow('Verde con fascia rossa','Conica, luce verde Lam (2+1). Il canale principale è a sinistra: la lasci a dritta',GREEN_S)
     +note('Conta il colore del corpo: comanda come un laterale normale.',PURPLE,34))
sec('preferito', head('Laterali · Regione A','Il canale preferito',PURPLE), pinned=svgp(X,Y,W,Hh,b,'Un canale che si divide in due: al bivio una boa cilindrica rossa con una fascia verde; il canale principale prosegue a dritta di chi entra, il secondario va a destra verso il mare aperto; di notte la luce rossa fa due lampi e poi uno')+lbl+pcol(txt),
 notes='Sono i laterali modificati del sistema IALA: servono dove un canale si divide. Il corpo e il miraglio sono quelli del laterale normale, con una larga fascia orizzontale dell\'altro colore; la luce è a gruppi composti di lampi (2+1). Non ci sono quiz specifici nel gruppo 1.5.3, ma il segnale si trova sulle carte nautiche.')
X=700

quiz_slide('quizB','Verifica · laterali',['1.5.3-43','1.5.3-46','1.5.3-27'],False)
quiz_slide('quizBr','Verifica · laterali',['1.5.3-43','1.5.3-46','1.5.3-27'],True)

# ============ LE CARDINALI E L'OROLOGIO ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.18"/>'
cx,cy,R=546,320,215
b+=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/>'
for h_ in range(12):
    a=math.radians(h_*30); b+=line(cx+(R-26)*math.sin(a),cy-(R-26)*math.cos(a),cx+(R-6)*math.sin(a),cy-(R-6)*math.cos(a),NAVY,6 if h_%3==0 else 3)
b+=f'<path d="M{cx-44} {cy+16} Q{cx-36} {cy-24} {cx} {cy-20} Q{cx+44} {cy-32} {cx+48} {cy+12} Q{cx+8} {cy+30} {cx-44} {cy+16} Z" fill="#7A6A55" stroke="{NAVY}" stroke-width="3"/>'
POS={'N':(0,'pillar'),'E':(90,'pillar'),'S':(180,'pillar'),'W':(270,'pillar')}
for kk,(a,sh) in POS.items():
    px=cx+(R-100)*math.sin(math.radians(a)); py=cy-(R-100)*math.cos(math.radians(a))+60
    b+=mk(kk,px,py,sh,0.55)[0]
lbl=lab(X+cx-150,Y+20,300,'12 · N · continua',NAVY,24,900,'center')+lab(X+cx+R+10,Y+cy-16,180,'3 · E',NAVY,26,900)+lab(X+cx-150,Y+cy+R+14,300,'6 · S · + lampo lungo',NAVY,24,900,'center')+lab(X+cx-R-190,Y+cy-16,180,'9 · W',NAVY,26,900,'right')
txt=(idrow('Cosa dicono','Dove passare: a Nord della cardinale Nord, perché il pericolo è a Sud',PURPLE)
     +idrow('Il miraglio','Due coni neri: le punte indicano dove sono le bande nere',PURPLE)
     +idrow('La luce','Bianca e scintillante. Conta i lampi come le ore: 3 a Est, 6 a Sud, 9 a Ovest, continua a Nord',PURPLE)
     +note('Il lampo lungo dopo i 6 non ti fa confondere il Sud con il 9 o il 3.',PURPLE,34))
sec('rosa', head('Cardinali','Le cardinali e l\'orologio',PURPLE)+col(txt), pinned=svgp(X,Y,W,Hh,b,'Un quadrante d\'orologio con uno scoglio al centro e le quattro cardinali: Nord alle 12, Est alle 3, Sud alle 6, Ovest alle 9, come il numero dei loro lampi')+lbl,
 notes='Quiz 1.5.3-36 e -67 (indicano il lato su cui transitare per evitare il pericolo), -51 (legati alla bussola, colori nero e giallo), -82, -83, -84 (9 scintillii: pericolo a est; 3: pericolo a ovest; 6: pericolo a nord). Scintillante (Q) = circa 60 lampi al minuto; scintillante rapida (VQ) = circa 120. Gli Est e gli Ovest possono avere periodi di 10 o 15 s (Q) o 5 e 10 s (VQ).')

scheda('nord','Cardinale Nord','Cardinali','N',['pillar','spar'],
 [('Colore','Nero sopra, giallo sotto'),('Forma','A colonna o ad asta'),('Miraglio','Due coni neri con le punte in alto'),('Luce','Bianca scintillante continua'),('Significato','Il pericolo è a Sud: passa a Nord')],
 'Le punte verso l\'alto: il nero è in alto, il Nord è in alto.',NAVY,
 'Quiz 1.5.3-66 (miraglio Nord: due coni con i vertici in alto), -33 (figura: passare a Nord, pericolo a Sud), -106 e -107 (figura: nero sopra il giallo; scintillante continua).',True)
scheda('est','Cardinale Est','Cardinali','E',['pillar','spar'],
 [('Colore','Nero, fascia gialla, nero'),('Forma','A colonna o ad asta'),('Miraglio','Due coni uniti per la base'),('Luce','Bianca, 3 scintillii: Sc (3) 10s'),('Significato','Il pericolo è a Ovest: passa a Est')],
 'Coni a rombo, 3 lampi: le 3 dell\'orologio sono a Est.',BLUE,
 'Quiz 1.5.3-69 e -72 (Est: coni uniti per le basi, passare a est), -83 (tre scintillii: pericolo a ovest, passare a est), -52 e -104 (figure).',False)
scheda('sud','Cardinale Sud','Cardinali','S',['pillar','spar'],
 [('Colore','Giallo sopra, nero sotto'),('Forma','A colonna o ad asta'),('Miraglio','Due coni neri con le punte in basso'),('Luce','Bianca, 6 scintillii e un lampo lungo'),('Significato','Il pericolo è a Nord: passa a Sud')],
 'Le punte verso il basso: il nero è in basso, il Sud è in basso.',CORAL,
 'Quiz 1.5.3-70 (miraglio Sud: vertici in basso), -84 (sei scintillii: pericolo a nord, passare a sud), -55, -108, -109 (figure: cardinale Sud, area navigabile a Sud).',True)
scheda('ovest','Cardinale Ovest','Cardinali','W',['pillar','spar'],
 [('Colore','Giallo, fascia nera, giallo'),('Forma','A colonna o ad asta'),('Miraglio','Due coni uniti per la punta'),('Luce','Bianca, 9 scintillii: Sc (9) 15s'),('Significato','Il pericolo è a Est: passa a Ovest')],
 'Coni a clessidra, 9 lampi: le 9 dell\'orologio sono a Ovest.',SEA,
 'Quiz 1.5.3-71 e -73 (Ovest: coni uniti per i vertici, passare a ovest), -82 (nove scintillii: pericolo a est, passare a ovest), -54 e -97 (figure).',False)

quiz_slide('quizC','Verifica · cardinali',['1.5.3-71','1.5.3-84','1.5.3-66'],False)
quiz_slide('quizCr','Verifica · cardinali',['1.5.3-71','1.5.3-84','1.5.3-66'],True)

# ============ GLI ALTRI ============
scheda('isolato','Pericolo isolato','Gli altri segnali','iso',['pillar','spar'],
 [('Colore','Nero con una o più bande rosse orizzontali'),('Forma','A colonna o ad asta'),('Miraglio','Due sfere nere'),('Luce','Bianca, a gruppi di 2 lampi'),('Significato','Un pericolo piccolo proprio lì sotto: gli giri attorno, stando largo')],
 'Due sfere, due lampi.',RED,
 'Quiz 1.5.3-15 e -40 (figure), -50 e -74 (nero con bande rosse, boa a fuso o asta), -16 (colore del corpo), -64 (luce bianca a lampi, pericolo isolato). L\'acqua intorno è navigabile, ma non si passa vicino.',True)
scheda('sicure','Acque sicure','Gli altri segnali','safe',['sphere','pillar','spar'],
 [('Colore','Strisce verticali rosse e bianche'),('Forma','Sferica, a colonna o ad asta'),('Miraglio','Una sfera rossa'),('Luce','Bianca: isofase, intermittente, lampo lungo ogni 10 s'),('Significato','Acqua navigabile tutto intorno: centro del canale o atterraggio')],
 'L\'unico a strisce verticali.',SEA,
 'Quiz 1.5.3-59 (luce bianca isofase, intermittente o a lampi lunghi: acque sicure), -65 (miraglio: una sfera rossa), -99 (figura). Può anche emettere la lettera A in Morse (punto-linea).',False)
scheda('speciale','Segnale speciale','Gli altri segnali','spec',['can','pillar','spar'],
 [('Colore','Giallo'),('Forma','Libera, purché non si confonda con altri segnali'),('Miraglio','Una X gialla'),('Luce','Gialla, con un ritmo diverso da quelli degli altri'),('Significato','Una zona particolare: cavi, condotte, esercitazioni, balneazione')],
 'Giallo e con la X: attenzione, qui c\'è qualcosa.',ORANGE,
 'Quiz 1.5.3-42 (zona speciale: cavi o condotte, esercitazioni), -53 (miraglio unico a X giallo), -12 (figura), -19, -22, -101 (corpo giallo), -20, -23 (5 lampi gialli ogni 20 s), -102 (un lampo giallo ogni 3 s). Tra le regioni A e B non cambiano (-46).',True)

quiz_slide('quizD','Verifica · gli altri segnali',['1.5.3-65','1.5.3-53','1.5.3-64'],False)
quiz_slide('quizDr','Verifica · gli altri segnali',['1.5.3-65','1.5.3-53','1.5.3-64'],True)

# ============ RIEPILOGO ============
RP=[('sx','can','Laterale di sinistra','Rossa · Lam r','Lasciala a sinistra entrando',LRED),
    ('dx','cone','Laterale di dritta','Verde · Lam v','Lasciala a dritta entrando',GREEN_S),
    ('iso','pillar','Pericolo isolato','Bianca · Lam (2)','Pericolo piccolo: girale attorno',RED),
    ('N','pillar','Cardinale Nord','Bianca · Sc continua','Passa a Nord',NAVY),
    ('E','pillar','Cardinale Est','Bianca · Sc (3)','Passa a Est',BLUE),
    ('safe','sphere','Acque sicure','Bianca · Iso','Navigabile tutto intorno',SEA),
    ('S','pillar','Cardinale Sud','Bianca · Sc (6) + lungo','Passa a Sud',CORAL),
    ('W','pillar','Cardinale Ovest','Bianca · Sc (9)','Passa a Ovest',SEA),
    ('spec','can','Speciale','Gialla','Zona particolare',ORANGE)]
g=''.join(f'<div style="display:flex; gap:16px; align-items:center; background:#FFFFFF; border-left:10px solid {c}; border-radius:20px; padding:10px 18px">{mini(k,sh,0.56,130,180)}'
          f'<div style="flex:1; display:flex; flex-direction:column; gap:2px">{p(t,28,INK,800,1.2)}{p(l,26,c,800,1.25)}{p(m,26,BODY,400,1.25)}</div></div>' for k,sh,t,l,m,c in RP)
sec('riepilogo', head('Allenamento','Tutte le schede in una',GREEN)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px">{g}</div>',
 notes='Da stampare o da tenere aperta durante il ripasso. Luce: il colore è quello del segnale per laterali e speciali; bianco per cardinali, pericolo isolato e acque sicure.')

# ============ DI GIORNO: CHI SONO? ============
GQ=[('E','pillar'),('sx','can'),('iso','spar'),('spec','pillar'),('S','spar'),('safe','sphere')]
GA=['Cardinale Est: passa a Est','Laterale di sinistra','Pericolo isolato','Speciale','Cardinale Sud: passa a Sud','Acque sicure']
def dayboard():
    b=f'<rect x="0" y="0" width="1664" height="500" fill="{SKY}"/><rect x="0" y="400" width="1664" height="100" fill="{WATER}" fill-opacity="0.3"/>'+line(0,400,1664,400,SEA,3)
    for i,(k,sh) in enumerate(GQ):
        x=1664*(i+0.5)/6; b+=mk(k,x,400,sh,1.15)[0]+num(x,460,i+1,NAVY,24)
    return b
sec('giorno', head('Allenamento · esercizio','Di giorno: chi sono?',GREEN)+svgi(1664,500,dayboard(),'Sei segnali numerati da 1 a 6 da riconoscere: boa a colonna nera con fascia gialla e coni base contro base; boa cilindrica rossa; asta nera con banda rossa e due sfere; boa a colonna gialla con X; asta gialla sopra e nera sotto con coni in basso; boa sferica a strisce verticali rosse e bianche con sfera rossa',pan=True)
    +note('Per ognuno: che segnale è, e da che parte passi?',GREEN,38),
 notes='Lasciare due minuti. Si guardano prima i colori, poi il miraglio: è il miraglio che distingue le cardinali tra loro.')
ans=''.join(f'<p style="flex:1; font-size:26px; line-height:1.25; font-weight:800; color:{INK}; text-align:center; background:{SEA_T}; border-radius:16px; padding:12px 8px">{i+1} · {a}</p>' for i,a in enumerate(GA))
sec('giornor', head('Allenamento · esercizio','Di giorno: le risposte',SEA)+svgi(1664,500,dayboard(),'Gli stessi sei segnali dell\'esercizio',pan=True)+f'<div style="display:flex; gap:12px; align-items:stretch">{ans}</div>',
 notes='1 Est (coni base contro base, nero-giallo-nero). 2 Laterale di sinistra (cilindro rosso). 3 Pericolo isolato (due sfere nere). 4 Speciale (giallo, X). 5 Sud (coni in basso, giallo sopra). 6 Acque sicure (strisce verticali, sfera rossa).')

# ============ DI NOTTE: CHI SONO? ============
NQ=['W','iso','safe','E','spec']
NA=['Cardinale Ovest','Pericolo isolato','Acque sicure','Cardinale Est','Speciale']
def nightboard():
    b=f'<rect x="0" y="0" width="1664" height="520" fill="{NIGHT}"/>'
    for i,k in enumerate(NQ): b+=num(60,52+i*100,i+1,CORAL,26)+strip(120,30+i*100,1500,k,48)
    return b
sec('notte', head('Allenamento · esercizio','Di notte: chi sono?',NAVY)+svgi(1664,520,nightboard(),'Cinque luci notturne numerate: nove scintillii bianchi poi buio; due lampi bianchi a gruppi; luce bianca isofase; tre scintillii bianchi; cinque lampi gialli',pan=False)
    +note('Conta i lampi e guarda il colore.',NAVY,38),
 notes='Ogni striscia mostra 15 o 20 secondi di luce. Contare i lampi di ogni gruppo e guardare il colore: il giallo è solo dei segnali speciali.')
na=''.join(f'<p style="flex:1; font-size:26px; line-height:1.25; font-weight:800; color:{INK}; text-align:center; background:{SEA_T}; border-radius:16px; padding:12px 8px">{i+1} · {a}<br><span style="color:{SEA}">{PAT[k][0]}</span></p>' for i,(k,a) in enumerate(zip(NQ,NA)))
sec('notter', head('Allenamento · esercizio','Di notte: le risposte',SEA)+svgi(1664,520,nightboard(),'Le stesse cinque luci dell\'esercizio',pan=False)+f'<div style="display:flex; gap:12px; align-items:stretch">{na}</div>',
 notes='1 Ovest: 9 scintillii. 2 Pericolo isolato: gruppi di 2 lampi. 3 Acque sicure: isofase. 4 Est: 3 scintillii. 5 Speciale: luce gialla.')

# ============ NAVIGAZIONE FLUVIALE ============
FV=[('Rotte opposte','Ha la precedenza chi naviga con la corrente a favore.',CORAL),
    ('Ponte con più arcate','Si passa sotto l\'arcata segnalata da un rombo giallo.',SEA),
    ('Boa bianca, controcorrente','Si passa a sinistra del segnale.',PURPLE),
    ('Curva a gomito','Un suono prolungato, poi si ascolta la risposta.',BLUE),
    ('A bordo','Tra le dotazioni: un faro anabbagliante orientabile.',GREEN),
    ('I cartelli in figura','Chiamata e rimando, prosecuzione: vanno visti sul manuale.',ORANGE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:26px 28px">{h3(t,34,c)}{p(d,28,BODY,400,1.4)}</div>' for t,d,c in FV)
sec('fluviale', head('Allenamento · i quiz sui fiumi','Navigazione fluviale',ORANGE)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px">{g}</div>'
    +note('Sono pochi quiz, ma all\'esame possono uscire.',ORANGE,36),
 notes='Quiz 1.5.3-113 (rotte opposte: precedenza a chi ha la corrente a favore), -114 (arcata con rombo giallo), -115 (controcorrente, boa bianca: passare a sinistra), -116 (curva a gomito: un suono prolungato e ascolto), -120 (faro anabbagliante orientabile). I quiz -112, -117, -118, -119 hanno una figura (segnali di chiamata e rimando e di prosecuzione): si studiano con le figure del manuale.')

closing(['Regione A: entrando in porto, rosso a sinistra e verde a dritta',
         'Cardinali: si passa dal lato del nome; i coni puntano verso il nero',
         'Di notte le cardinali sono un orologio: 3 Est, 6 Sud, 9 Ovest, continua Nord',
         'Pericolo isolato: due sfere e due lampi; acque sicure: strisce verticali e sfera rossa',
         'Tutto ciò che è giallo con la X è un segnale speciale'],
 'Buon vento, e occhi ai segnali!','Appendice F · Schede IALA')

write_deck(OUT,'Appendice F · Schede IALA',ORDER,
 {"s1":{"description":"Copertina, indice, sistema, luci e parole","start":"cover"},
  "s2":{"description":"Schede dei segnali laterali","start":"sinistra"},
  "s3":{"description":"Schede dei segnali cardinali","start":"rosa"},
  "s4":{"description":"Pericolo isolato, acque sicure, speciale","start":"isolato"},
  "s5":{"description":"Riepilogo ed esercizi di riconoscimento","start":"riepilogo"},
  "s6":{"description":"Navigazione fluviale e chiusura","start":"fluviale"}})
