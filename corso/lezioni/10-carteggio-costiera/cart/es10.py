"""Soluzioni degli esercizi di navigazione costiera (famiglie 5.1.3-5.4.3, carta 5/D)."""
import json, os, re, math
from geo import *
EX={e['id']:e for e in json.load(open(os.path.join(D,'..','..','..','..','..','..','home','user','fabfab..','corso','carteggio','esercizi-dd-131-2022.json')))} if False else None
EXF='/home/user/fabfab../corso/carteggio/esercizi-dd-131-2022.json'
EX={e['id']:e for e in json.load(open(EXF))}

def sgn(v): return f'{v:+g}°'.replace('+','+').replace('-','−')
def deg(v): return f'{norm(round(v)):03d}°'
def t2h(s):
    h,m=map(int,re.findall(r'\d+',s)[:2]); return h+m/60
def hm(mins): return f'{int(mins//60)}h{int(round(mins%60)):02d}m' if mins>=60 else f'{int(round(mins))} minuti'

def parse_range(r):
    """'Lat.42°49’,7N÷42°50’,3N Long.010°02’,0E÷010°02’,6E' → ((lat1,lat2),(lon1,lon2))"""
    r=r.replace("'",'’').replace(',','.')
    nums=re.findall(r'(\d+)°\s*(\d+)[’\']?\s*\.?(\d*)',r)
    vals=[int(g)+float(f"{m}.{d or 0}")/60 for g,m,d in nums]
    if len(vals)>=4: return (vals[0],vals[1]),(vals[2],vals[3])
    return None

class Sol:
    def __init__(s, id_, P0):
        s.id=id_; s.ex=EX[id_]; s.pl=Plane(*P0); s.passi=[]; s.dati=[]; s.pts=[]; s.lines=[]; s.res=None; s.res_txt=''; s.note=''
    def xy(s,name_or_ll):
        ll=lm(name_or_ll) if isinstance(name_or_ll,str) else name_or_ll
        return s.pl.xy(*ll)
    def ll(s,p): return s.pl.ll(*p)
    def pt(s,p,lab,kind='ship'): s.pts.append((s.ll(p),lab,kind))
    def line(s,a,b,kind,lab=''): s.lines.append((s.ll(a),s.ll(b),kind,lab))
    def fix(s,p,lab):
        s.res=s.ll(p); s.res_txt=f'{lat_s(s.res[0])} · {lon_s(s.res[1])}'; s.pt(p,lab,'fix')
    def check(s):
        rg=parse_range(s.ex['risposta_ufficiale'])
        if not rg or not s.res: return None
        (a,b),(c,d)=rg; lat,lon=s.res
        return (min(a,b)-1e-6<=lat<=max(a,b)+1e-6) and (min(c,d)-1e-6<=lon<=max(c,d)+1e-6)

def bear_line(S,Lxy,r,extra=1.0,kind='ril',lab=''):
    """disegna il rilevamento: dalla nave verso il punto cospicuo"""
    return None

# ---------- punto nave con due rilevamenti trasportati ----------
def running_fix(S, L1, r1, L2, r2, course, run):
    """L1 rilevato per r1 al tempo 1, L2 per r2 al tempo 2; tra i due la nave fa run miglia per course"""
    p1=S.xy(L1); p2=S.xy(L2)
    q=add(p1,u(course),run)            # punto cospicuo 1 trasportato
    F=cross_lines(p2,r2,q,r1)          # incrocio della seconda linea con la prima trasportata
    P1=sub(F,(u(course)[0]*run,u(course)[1]*run))  # posizione al primo rilevamento
    return F,P1,q

def draw_running(S,L1,n1,r1,L2,n2,r2,course,run,F,P1,q,t1,t2):
    p1=S.xy(L1); p2=S.xy(L2)
    S.pt(p1,n1,'lm')
    if n2!=n1: S.pt(p2,n2,'lm')
    S.line(add(P1,u(r1),-1.2),p1,'ril',f'{t1} · Rilv {deg(r1)}')
    S.line(F,p2,'ril2',f'{t2} · Rilv {deg(r2)}')
    S.line(add(q,u(r1),-dist(p1,P1)-1.2),add(q,u(r1),0.3),'trasp','primo rilevamento trasportato')
    S.line(P1,F,'rotta',f'{deg(course)} · {str(round(run,2)).replace(".",",")} mg')
    S.line(p1,q,'trasp_v','')
    S.pt(P1,t1,'ship')

def conv(pb=None, d=None, dev=None, V=None):
    v=V if V is not None else d+dev
    return v

SOLS=[]
def reg(f): SOLS.append(f); return f

def pb2pv_txt(pb,d,dv,label='Pb'):
    V=d+dv; return V, f'V = d + δ = {sgn(d)} {sgn(dv)} = {sgn(V)}', f'Pv = {label} + V = {deg(pb)} {sgn(V)} = {deg(pb+V)}'

@reg
def e5_1_3_1():
    S=Sol('5.1.3-1',lm('Faro di Punta Polveraia'))
    V=1; Pv=350+V; r1=75+V; r2=125+V; run=9*20/60
    S.dati=[('Pb','350°'),('d, δ','+1°, 0°'),('Vp','9 kn'),('Rilb','075° e 125° (Punta Polveraia)'),('Δt','20 minuti')]
    S.passi=[f'Variazione V = d + δ = +1°: Pv = 351°, Rilv₁ = 076°, Rilv₂ = 126°.',f'Cammino tra i due rilevamenti: 9 × 20/60 = {run:g} miglia per 351°.',
             'Traccia i due rilevamenti dal faro; trasporta il primo di 3 miglia per 351°.','Il punto nave è l\'incrocio del primo trasportato con il secondo.']
    F,P1,q=running_fix(S,'Faro di Punta Polveraia',r1,'Faro di Punta Polveraia',r2,Pv,run)
    draw_running(S,'Faro di Punta Polveraia','Punta Polveraia',r1,'Faro di Punta Polveraia','Punta Polveraia',r2,Pv,run,F,P1,q,'12h00m','12h20m')
    S.fix(F,'PN 12h20m'); return S

@reg
def e5_1_3_2():
    S=Sol('5.1.3-2',lm('Faro dello Scoglietto'))
    V=-4; Pv=86+V; r1=164+V; r2=194+V; run=5*18/60
    S.dati=[('Pb','086°'),('d, δ','−2°, −2°'),('Vp','5 kn'),('Rilb','164° e 194° (Scoglietto)'),('Δt','18 minuti')]
    S.passi=['V = −2° −2° = −4°: Pv = 082°, Rilv₁ = 160°, Rilv₂ = 190°.',f'Cammino: 5 × 18/60 = {run:g} miglia per 082°.','Trasporta il primo rilevamento di 1,5 miglia per 082° e incrocialo con il secondo.']
    F,P1,q=running_fix(S,'Faro dello Scoglietto',r1,'Faro dello Scoglietto',r2,Pv,run)
    draw_running(S,'Faro dello Scoglietto','Scoglietto',r1,'Faro dello Scoglietto','Scoglietto',r2,Pv,run,F,P1,q,'17h00m','17h18m')
    S.fix(F,'PN 17h18m'); return S

@reg
def e5_1_3_3():
    S=Sol('5.1.3-3',lm('Faro di Capo Poro'))
    V=-4; Pv=104+V; r=[46+V,9+V,321+V]; Vp=6
    S.dati=[('Pb','104°'),('V','−4°'),('Vp','6 kn'),('Rilb','046°, 009°, 321° (faro Fl 5s)'),('Ore','01h50m, 02h20m, 03h05m')]
    L='Faro di Capo Poro'; p=S.xy(L)
    runs=[Vp*75/60,Vp*45/60,0]
    qs=[add(p,u(Pv),k) for k in runs]
    F=cross_lines(qs[1],r[1],qs[2],r[2]); F2=cross_lines(qs[0],r[0],qs[2],r[2]); F=((F[0]+F2[0])/2,(F[1]+F2[1])/2)
    S.passi=['Il faro con un lampo ogni 5 s a sud dell\'Elba è Capo Poro (Fl 5s).','V = −4°: Pv = 100°, Rilv = 042°, 005°, 317°.',
             'Cammini fino alle 03h05m: 6 × 75/60 = 7,5 mg e 6 × 45/60 = 4,5 mg per 100°.','Trasporta il primo di 7,5 mg e il secondo di 4,5 mg: le tre linee si incontrano nel punto nave.']
    S.pt(p,'Capo Poro','lm')
    for i,(rr,k,t) in enumerate(zip(r,runs,['01h50m','02h20m','03h05m'])):
        P_i=sub(F,(u(Pv)[0]*k,u(Pv)[1]*k))
        S.line(add(P_i,u(rr),-1),p,'ril' if i<2 else 'ril2',f'{t} · Rilv {deg(rr)}')
        if k: S.line(add(qs[i],u(rr),-dist(p,P_i)-1),add(qs[i],u(rr),0.3),'trasp',''); S.pt(P_i,t,'ship')
    S.line(sub(F,(u(Pv)[0]*7.5,u(Pv)[1]*7.5)),F,'rotta','100° · 6 kn')
    S.fix(F,'PN 03h05m'); return S

@reg
def e5_1_3_4():
    S=Sol('5.1.3-4',lm('Punta Nera'))
    V=-5; Pv=355; r1=45+V; r2=100+V; run=6*30/60
    S.dati=[('Pv','355°'),('V','−5°'),('Vp','6 kn'),('Rilb','045° e 100° (Punta Nera)'),('Δt','30 minuti')]
    S.passi=['V = −5°: Rilv₁ = 040°, Rilv₂ = 095° (la Pv è già vera).',f'Cammino: 6 × 30/60 = {run:g} miglia per 355°.','Trasporta il primo rilevamento di 3 mg per 355° e incrocialo con il secondo.']
    F,P1,q=running_fix(S,'Punta Nera',r1,'Punta Nera',r2,Pv,run)
    draw_running(S,'Punta Nera','Punta Nera',r1,'Punta Nera','Punta Nera',r2,Pv,run,F,P1,q,'10h00m','10h30m')
    S.fix(F,'PN 10h30m'); return S

@reg
def e5_1_3_5():
    S=Sol('5.1.3-5',lm('Faro di Punta Polveraia'))
    V=-2; Pv=350; r1=52+V; r2=83+V; run=12.4*15/60
    S.dati=[('Rv','350° (Pv, nessuna deriva)'),('V','−2°'),('Vp','12,4 kn'),('Rilb','052° e 083° (Punta Polveraia)'),('Δt','15 minuti')]
    S.passi=['V = −2°: Rilv₁ = 050°, Rilv₂ = 081°. Senza vento né corrente la Rv coincide con la Pv.',f'Cammino: 12,4 × 15/60 = {run:.1f} miglia per 350°.','Trasporta il primo rilevamento di 3,1 mg per 350° e incrocialo con il secondo.']
    F,P1,q=running_fix(S,'Faro di Punta Polveraia',r1,'Faro di Punta Polveraia',r2,Pv,run)
    draw_running(S,'Faro di Punta Polveraia','Punta Polveraia',r1,'Faro di Punta Polveraia','Punta Polveraia',r2,Pv,run,F,P1,q,'13h45m','14h00m')
    S.pt(S.xy((42+40/60,10.0)),'A','ship')
    S.fix(F,'PN 14h00m'); return S

@reg
def e5_1_3_6():
    S=Sol('5.1.3-6',(42.85,10.1))
    A=S.xy((42.75,10+1.7/60)); B=S.xy((42+55/60,10.2)); vb=4; va=6; cb=240
    t=intercept(A,va,B,cb,vb); D_=add(B,u(cb),vb*t)
    S.dati=[('A (Vega)','42°45,0′N 010°01,7′E'),('Ve Vega','6 kn'),('B (Serenity)','42°55′N 010°12′E'),('Serenity','Rv 240°, 4 kn')]
    S.passi=ipassi('Serenity',cb,vb,va,brg(A,D_),t); draw_intercept(S,A,va,B,cb,vb,D_,'Vega','Serenity')
    S.pt(A,'A · Vega','ship'); S.pt(B,'B · Serenity','ship')
    S.line(B,D_,'rotta2','Serenity 240° · 4 kn'); S.line(A,D_,'rotta',f'Vega {deg(brg(A,D_))} · 6 kn')
    S.fix(D_,'D'); S.extra=('rotta di intercettazione',deg(brg(A,D_)),hm(t*60)); return S

def draw_intercept(S,A,va,B,cb,vb,D_,nA,nB):
    T=add(A,u(cb),vb); ab=brg(A,B); c=brg(A,D_); V_=add(A,u(c),va)
    S.line(A,T,'vett',f'{str(vb).replace(".",",")} kn'); S.line(T,add(V_,u(ab),0.6),'par','')
    S.line(A,V_,'vett2',f'{str(va).replace(".",",")} kn'); S.line(A,B,'rotta_l','')
def ipassi(nB,cb,vb,va,c,t,lettera='D'):
    vb_=str(vb).replace('.',','); va_=str(va).replace('.',',')
    return [f'Da B traccia la rotta di {nB} ({deg(cb)}) e congiungi A con B.',
            f'Da A disegna la velocità di {nB}: {vb_} mg per {deg(cb)} (1 ora).',
            f'Dalla punta traccia la parallela ad AB e tagliala da A con il compasso aperto di {va_} mg: la rotta di intercettazione è {deg(c)}.',
            f'Dove questa rotta taglia quella di {nB} c\'è {lettera}: incontro dopo {hm(t*60)}.']

def intercept(A,va,B,cb,vb):
    """tempo t tale che |B + vb t u(cb) - A| = va t"""
    w=sub(B,A); ub=u(cb)
    a=vb*vb-va*va; b=2*(w[0]*ub[0]+w[1]*ub[1])*vb; c=w[0]**2+w[1]**2
    if abs(a)<1e-9: return -c/b
    disc=b*b-4*a*c; ts=[(-b+math.sqrt(disc))/(2*a),(-b-math.sqrt(disc))/(2*a)]
    return min(t for t in ts if t>0)

@reg
def e5_2_3_1():
    S=Sol('5.2.3-1',lm('Scoglio dello Sparviero'))
    V=-1; Pv=281+V; r1=46+V; r2=351+V; run=12*30/60
    S.dati=[('Pb','281°'),('d, δ','+3°, −4°'),('Vp','12 kn'),('Rilb','046° fanali di Castiglione, 351° Sparviero'),('Δt','30 minuti')]
    S.passi=['V = +3° −4° = −1°: Pv = 280°, Rilv₁ = 045°, Rilv₂ = 350°.',f'Cammino: 12 × 30/60 = {run:g} miglia per 280°.','Trasporta di 6 mg il rilevamento dei fanali di Castiglione e incrocialo con quello dello Sparviero.']
    F,P1,q=running_fix(S,'Fanali di Castiglione della Pescaia',r1,'Scoglio dello Sparviero',r2,Pv,run)
    draw_running(S,'Fanali di Castiglione della Pescaia','Castiglione',r1,'Scoglio dello Sparviero','Sparviero',r2,Pv,run,F,P1,q,'11h00m','11h30m')
    S.fix(F,'PN 11h30m'); return S

@reg
def e5_2_3_2():
    S=Sol('5.2.3-2',lm('Faro di Punta Ala'))
    V=-4; Pv=315; r1=34+V; r2=74+V; run=6*30/60
    S.dati=[('Pv','315°'),('d, δ','−2°, −2°'),('Vp','6 kn'),('Rilb','034° e 074° (faro di Punta Ala)'),('Δt','30 minuti')]
    S.passi=['V = −4°: Rilv₁ = 030°, Rilv₂ = 070° (la Pv è già vera).',f'Cammino: 6 × 30/60 = {run:g} miglia per 315°.','Trasporta il primo rilevamento di 3 mg per 315° e incrocialo con il secondo.']
    F,P1,q=running_fix(S,'Faro di Punta Ala',r1,'Faro di Punta Ala',r2,Pv,run)
    draw_running(S,'Faro di Punta Ala','Punta Ala',r1,'Faro di Punta Ala','Punta Ala',r2,Pv,run,F,P1,q,'10h00m','10h30m')
    S.pt(S.xy((42+40/60,10+50/60)),'A','ship')
    S.fix(F,'PN 10h30m'); return S

@reg
def e5_2_3_3():
    S=Sol('5.2.3-3',lm('Scoglio dello Sparviero'))
    V=-1; Pv=271+V; r1=351+V; r2=21+V; run=6*34/60
    S.dati=[('Pb','271°'),('V','−1°'),('Vp','6 kn'),('Rilb','351° Passo Peroni, 021° Sparviero'),('Δt','34 minuti')]
    S.passi=['V = −1°: Pv = 270°, Rilv₁ = 350°, Rilv₂ = 020°.',f'Cammino: 6 × 34/60 = {run:.1f} miglia per 270°.','Trasporta di 3,4 mg il rilevamento di Passo Peroni e incrocialo con quello dello Sparviero.']
    F,P1,q=running_fix(S,'Poggio Peroni',r1,'Scoglio dello Sparviero',r2,Pv,run)
    draw_running(S,'Poggio Peroni','Passo Peroni',r1,'Scoglio dello Sparviero','Sparviero',r2,Pv,run,F,P1,q,'15h00m','15h34m')
    S.fix(F,'PN 15h34m'); return S

@reg
def e5_2_3_4():
    S=Sol('5.2.3-4',lm('Faro di Punta Ala'))
    d=1.5+5*0.1; V=d+1; Pv=197+V; r1=97+V; r2=147+V; run=9*10/60
    S.dati=[('Pb','197°'),('δ','+1°'),('d 2016','1°30′E, +6′/anno'),('Vp','9 kn'),('Rilb','097° Punta Martina, 147° Punta Ala'),('Δt','10 minuti')]
    S.passi=['Declinazione 2021: 1°30′ + 5 × 6′ = 2°00′E. V = +2° +1° = +3°.','Pv = 200°, Rilv₁ = 100°, Rilv₂ = 150°.',f'Cammino: 9 × 10/60 = {run:g} miglia per 200°.','Trasporta di 1,5 mg il rilevamento di Punta Martina e incrocialo con quello di Punta Ala.']
    F,P1,q=running_fix(S,'Punta Martina',r1,'Faro di Punta Ala',r2,Pv,run)
    draw_running(S,'Punta Martina','Punta Martina',r1,'Faro di Punta Ala','Punta Ala',r2,Pv,run,F,P1,q,'09h00m','09h10m')
    S.fix(F,'PN 09h10m'); return S

@reg
def e5_2_3_5():
    S=Sol('5.2.3-5',lm('Fanali di Castiglione della Pescaia'))
    Pv=130; r1=41; r2=80; run=6*20/60
    S.dati=[('Rv','130° da Scoglio dello Sparviero'),('Vp','6 kn'),('Rilv','041° fanali di Castiglione, 080° serbatoio di Marina di Grosseto'),('Δt','20 minuti')]
    S.passi=['Rilevamenti già veri: nessuna conversione.',f'Cammino: 6 × 20/60 = {run:g} miglia per 130°.','Trasporta di 2 mg il rilevamento di Castiglione e incrocialo con quello del serbatoio.']
    F,P1,q=running_fix(S,'Fanali di Castiglione della Pescaia',r1,'Serbatoio di Marina di Grosseto',r2,Pv,run)
    draw_running(S,'Fanali di Castiglione della Pescaia','Castiglione',r1,'Serbatoio di Marina di Grosseto','Serbatoio',r2,Pv,run,F,P1,q,'10h00m','10h20m')
    S.fix(F,'PN 10h20m'); return S

@reg
def e5_3_3_1():
    S=Sol('5.3.3-1',lm('Punta Brigantina'))
    V=-3; Pv=265+V; r1=315+V; r2=350+V; run=5*36/60
    S.dati=[('Pb','265°'),('d, δ','−3°, 0°'),('Vp','5 kn'),('Rilb','315° Punta Brigantina, 350° Torre Cala della Ruta'),('Δt','36 minuti')]
    S.passi=['V = −3°: Pv = 262°, Rilv₁ = 312°, Rilv₂ = 347°.',f'Cammino: 5 × 36/60 = {run:g} miglia per 262°.','Trasporta di 3 mg il rilevamento di Punta Brigantina e incrocialo con quello della torre.']
    F,P1,q=running_fix(S,'Punta Brigantina',r1,'Torre di Cala della Ruta',r2,Pv,run)
    draw_running(S,'Punta Brigantina','P.ta Brigantina',r1,'Torre di Cala della Ruta','T. Cala della Ruta',r2,Pv,run,F,P1,q,'10h00m','10h36m')
    S.fix(F,'PN 10h36m'); return S

@reg
def e5_3_3_2():
    return traverso('5.3.3-2',(42+34.5/60,10+8.5/60),2.6,6,0+20/60+14*7/60,'dicembre 2008')
@reg
def e5_3_3_3():
    return traverso('5.3.3-3',(42+33/60,9+56/60),3.1,9,0+20/60+15*7/60,'novembre 2009')

def traverso(id_,A_ll,dd,Vp,d,quando):
    S=Sol(id_,lm("Faro di Scoglio d'Africa"))
    A=S.xy(A_ll); L=S.xy("Faro di Scoglio d'Africa")
    R=dist(A,L); b=brg(A,L); a=math.degrees(math.asin(dd/R))
    Pv=norm(b-a)   # scoglio a dritta: la rotta lo lascia sulla destra
    C=add(L,u(Pv-90),dd)
    Pm=Pv-d; dv=dev_pm(Pm); Pb=Pm-dv
    S.pt(A,'A','ship'); S.pt(L,"Scoglio d'Africa",'lm')
    S.line(A,add(C,u(Pv),2),'rotta',f'Pv {deg(Pv)}'); S.line(C,L,'ril2',f'{str(dd).replace(".",",")} mg al traverso')
    S.pt(C,'C','fix')
    S.res=('Pb',Pb); S.res_txt=f'Pb {deg(Pb)}'
    S.dati=[('A',f'{lat_s(A_ll[0])} {lon_s(A_ll[1])}'),('Traverso','a dritta di Scoglio d\'Africa a '+str(dd).replace('.',',')+' mg'),('d 1994','0°20′E, +7′/anno'),('Vp',f'{Vp} kn')]
    yrs=round((d-20/60)*60/7)
    S.passi=[f'Traccia il cerchio di {str(dd).replace(".",",")} mg attorno al faro e la tangente da A che lo lascia a dritta: Pv = {deg(Pv)}.',
             f'Declinazione {quando}: 0°20′ + {yrs} × 7′ = {int(d)}°{round((d-int(d))*60):02d}′E, cioè circa {round(d)}°E.',
             f'Pm = Pv − d = {deg(Pv)} − {round(d)}° = {deg(Pv-round(d))}. Dalla tabella: δ = {sgn(round(dev_pm(Pv-round(d))))}.',
             f'Pb = Pm − δ = {deg(Pv-round(d)-round(dev_pm(Pv-round(d))))}.']
    S.res=('Pb',Pv-round(d)-round(dev_pm(Pv-round(d)))); S.res_txt=f'Pb {deg(S.res[1])}'
    return S

@reg
def e5_3_3_4():
    S=Sol('5.3.3-4',lm("Faro dell'Isola di Pianosa"))
    Af=S.xy("Faro di Scoglio d'Africa"); A=add(Af,u(171),-6); B=S.xy((42+37.6/60,10+10/60)); Pv=brg(A,B)
    r1=Pv-45; r2=Pv-125; run=12*15/60
    F,P1,q=running_fix(S,"Faro dell'Isola di Pianosa",r1,"Faro dell'Isola di Pianosa",r2,Pv,run)
    S.dati=[('A','6 mg da Scoglio d\'Africa per Rilv 171°'),('B','42°37,6′N 010°10′E'),('Vp','12 kn'),('ρ','−045° e −125° (faro di Pianosa)'),('Δt','15 minuti')]
    S.passi=[f'A è 6 mg a sud (171°) di Scoglio d\'Africa. Da A a B: Pv = {deg(Pv)}.',f'Rilv = Pv + ρ: {deg(r1)} e {deg(r2)}.',f'Cammino: 12 × 15/60 = {run:g} miglia.','Trasporta il primo rilevamento di 3 mg e incrocialo con il secondo.']
    draw_running(S,"Faro dell'Isola di Pianosa",'Pianosa',r1,"Faro dell'Isola di Pianosa",'Pianosa',r2,Pv,run,F,P1,q,'10h00m','10h15m')
    S.pt(A,'A','ship'); S.pt(B,'B','ship'); S.pt(Af,"Scoglio d'Africa",'lm'); S.line(A,P1,'rotta','')
    S.fix(F,'PN 10h15m'); return S

@reg
def e5_3_3_5():
    S=Sol('5.3.3-5',lm("Faro dell'Isola di Pianosa"))
    Pv=90; r1=30; r2=330; run=6*50/60
    S.dati=[('Rv','090°'),('Vp','6 kn'),('Rilv','030° Torre Cala della Ruta, 330° faro di Pianosa'),('Δt','50 minuti')]
    S.passi=['Rilevamenti già veri.',f'Cammino: 6 × 50/60 = {run:g} miglia per 090°.','Trasporta di 5 mg il rilevamento della torre e incrocialo con quello del faro.']
    F,P1,q=running_fix(S,'Torre di Cala della Ruta',r1,"Faro dell'Isola di Pianosa",r2,Pv,run)
    draw_running(S,'Torre di Cala della Ruta','T. Cala della Ruta',r1,"Faro dell'Isola di Pianosa",'Faro di Pianosa',r2,Pv,run,F,P1,q,'12h00m','12h50m')
    S.fix(F,'PN 12h50m'); return S

@reg
def e5_3_3_6():
    S=Sol('5.3.3-6',lm('Isolotto della Scola'))
    V=5; Pv=65+V; r1=Pv-118; r2=Pv-98; run=6*14/60
    S.dati=[('Pb','065°'),('d, δ','+1°, +4°'),('Vp','6 kn'),('ρ','−118° Torre Cala della Ruta, −098° Isola La Scola'),('Δt','14 minuti')]
    S.passi=[f'V = +1° +4° = +5°: Pv = 070°.',f'Rilv = Pv + ρ: 070° − 118° = {deg(r1)}; 070° − 98° = {deg(r2)}.',f'Cammino: 6 × 14/60 = {run:.1f} miglia per 070°.','Trasporta di 1,4 mg il rilevamento della torre e incrocialo con quello della Scola.']
    F,P1,q=running_fix(S,'Torre di Cala della Ruta',r1,'Isolotto della Scola',r2,Pv,run)
    draw_running(S,'Torre di Cala della Ruta','T. Cala della Ruta',r1,'Isolotto della Scola','La Scola',r2,Pv,run,F,P1,q,'10h00m','10h14m')
    S.fix(F,'PN 10h14m'); return S

@reg
def e5_3_3_7():
    S=Sol('5.3.3-7',lm('Punta Brigantina'))
    d=-(2.75+3*5/60); V=d+1; Pv=42+V; r1=277+V; r2=307+V; run=12*5/60
    S.dati=[('Pb','042°'),('δ','+1°'),('d 2018','2°45′W, 5′W/anno'),('Vp','12 kn'),('Rilb','277° Punta Brigantina, 307° Punta del Grottone'),('Δt','5 minuti')]
    S.passi=['Declinazione 2021: 2°45′ + 3 × 5′ = 3°00′W. V = −3° +1° = −2°.','Pv = 040°, Rilv₁ = 275°, Rilv₂ = 305°.',f'Cammino: 12 × 5/60 = {run:g} miglio per 040°.','Trasporta di 1 mg il rilevamento di Punta Brigantina e incrocialo con quello di Punta del Grottone.']
    F,P1,q=running_fix(S,'Punta Brigantina',r1,'Punta del Grottone',r2,Pv,run)
    draw_running(S,'Punta Brigantina','P.ta Brigantina',r1,'Punta del Grottone','P.ta del Grottone',r2,Pv,run,F,P1,q,'11h45m','11h50m')
    S.fix(F,'PN 11h50m'); return S

@reg
def e5_4_3_1():
    S=Sol('5.4.3-1',lm('Faro di Punta Lividonia'))
    Fe=S.xy('Faro di Punta del Fenaio'); Ta=S.xy('Faro di Talamone'); Pv=brg(Fe,Ta)
    V=4; r1=96+V; r2=131+V; run=6*20/60
    F,P1,q=running_fix(S,'Faro di Punta Lividonia',r1,'Faro di Punta Lividonia',r2,Pv,run)
    S.dati=[('Rotta','da Punta del Fenaio al faro di Talamone'),('d, δ','−1°, +5°'),('Vp','6 kn'),('Rilb','096° e 131° (faro di Punta Lividonia)'),('Δt','20 minuti')]
    S.passi=[f'Congiungi Punta del Fenaio con Talamone: Rv = Pv = {deg(Pv)}.','V = −1° +5° = +4°: Rilv₁ = 100°, Rilv₂ = 135°.',f'Cammino: 6 × 20/60 = {run:g} miglia.','Trasporta il primo rilevamento di 2 mg e incrocialo con il secondo.']
    draw_running(S,'Faro di Punta Lividonia','P.ta Lividonia',r1,'Faro di Punta Lividonia','P.ta Lividonia',r2,Pv,run,F,P1,q,'10h00m','10h20m')
    S.pt(Fe,'P.ta del Fenaio','lm'); S.pt(Ta,'Talamone','lm'); S.line(Fe,Ta,'rotta_l','')
    S.fix(F,'PN 10h20m'); return S

@reg
def e5_4_3_2():
    S=Sol('5.4.3-2',lm('Faro di Formica Grande'))
    V=2; Pv=349; r1=278+V; r2=243+V; run=6*20/60
    S.dati=[('Pv','349°'),('V','+2°'),('Vp','6 kn'),('Rilb','278° e 243° (Formica Grande)'),('Δt','20 minuti')]
    S.passi=['V = +2°: Rilv₁ = 280°, Rilv₂ = 245°.',f'Cammino: 6 × 20/60 = {run:g} miglia per 349°.','Trasporta il primo rilevamento di 2 mg e incrocialo con il secondo.']
    F,P1,q=running_fix(S,'Faro di Formica Grande',r1,'Faro di Formica Grande',r2,Pv,run)
    draw_running(S,'Faro di Formica Grande','Formica Grande',r1,'Faro di Formica Grande','Formica Grande',r2,Pv,run,F,P1,q,'10h00m','10h20m')
    S.fix(F,'PN 10h20m'); return S

@reg
def e5_4_3_3():
    S=Sol('5.4.3-3',lm('Scoglio Argentarola'))
    d=-(1.75+3*5/60); V=d+1; Pv=337+V; r1=36+V; r2=81+V; run=12*20/60
    S.dati=[('Pb','337°'),('δ','+1°'),('d 2018','1°45′W, 5′W/anno'),('Vp','12 kn'),('Rilb','036° Capo d\'Uomo, 081° Argentarola'),('Δt','20 minuti')]
    S.passi=['Declinazione 2021: 1°45′ + 3 × 5′ = 2°00′W. V = −2° +1° = −1°.','Pv = 336°, Rilv₁ = 035°, Rilv₂ = 080°.',f'Cammino: 12 × 20/60 = {run:g} miglia per 336°.','Trasporta di 4 mg il rilevamento di Capo d\'Uomo e incrocialo con quello dell\'Argentarola.']
    F,P1,q=running_fix(S,"Capo d'Uomo",r1,'Scoglio Argentarola',r2,Pv,run)
    draw_running(S,"Capo d'Uomo","Capo d'Uomo",r1,'Scoglio Argentarola','Argentarola',r2,Pv,run,F,P1,q,'10h00m','10h20m')
    S.fix(F,'PN 10h20m'); return S

@reg
def e5_4_3_4():
    S=Sol('5.4.3-4',lm('Faro di Punta Lividonia'))
    Pv=235; r1=120; r2=200; run=6*50/60
    S.dati=[('Rv','235° da Talamone'),('Vp','6 kn'),('Rilv','120° Punta Lividonia, 200° Punta del Fenaio'),('Δt','50 minuti')]
    S.passi=['Rilevamenti già veri.',f'Cammino: 6 × 50/60 = {run:g} miglia per 235°.','Trasporta di 5 mg il rilevamento di Punta Lividonia e incrocialo con quello di Punta del Fenaio.']
    F,P1,q=running_fix(S,'Faro di Punta Lividonia',r1,'Faro di Punta del Fenaio',r2,Pv,run)
    draw_running(S,'Faro di Punta Lividonia','P.ta Lividonia',r1,'Faro di Punta del Fenaio','P.ta del Fenaio',r2,Pv,run,F,P1,q,'20h00m','20h50m')
    S.fix(F,'PN 20h50m'); return S

@reg
def e5_4_3_5():
    S=Sol('5.4.3-5',lm('Faro di Formica Grande'))
    V=-5; Pv=230+V; r1=105+V; r2=70+V; run=6*23/60
    S.dati=[('Pb','230°'),('V','−5°'),('Vp','6 kn'),('Rilb','105° e 070° (Formica Grande)'),('Δt','23 minuti')]
    S.passi=['V = −5°: Pv = 225°, Rilv₁ = 100°, Rilv₂ = 065°.',f'Cammino: 6 × 23/60 = {run:.1f} miglia per 225°.','Trasporta il primo rilevamento di 2,3 mg e incrocialo con il secondo.']
    F,P1,q=running_fix(S,'Faro di Formica Grande',r1,'Faro di Formica Grande',r2,Pv,run)
    draw_running(S,'Faro di Formica Grande','Formica Grande',r1,'Faro di Formica Grande','Formica Grande',r2,Pv,run,F,P1,q,'16h00m','16h23m')
    S.fix(F,'PN 16h23m'); return S

@reg
def e5_4_3_6():
    S=Sol('5.4.3-6',lm('Faro di Punta del Fenaio'))
    Fe=S.xy('Faro di Punta del Fenaio'); A=add(Fe,u(95),-2.5); A2=add(A,u(340),9)
    B=S.xy((42+32.5/60,10+57.5/60)); t=intercept(A2,9,B,52,1.6); D_=add(B,u(52),1.6*t)
    S.dati=[('A','2,5 mg dal faro di Punta del Fenaio per Rilv 095°, 14h50m'),('Rigel','Rv 340°, 9 kn'),('B (Dubhe, 15h50m)','42°32,5′N 010°57,5′E, Rv 052°, 1,6 kn')]
    S.passi=['A: 2,5 mg dal faro sul rilevamento 095° (il faro è a est). In un\'ora Rigel fa 9 mg per 340°: punto A′ delle 15h50m.']+[x.replace(' A ',' A′ ').replace('da A ','da A′ ').replace('Da A ','Da A′ ').replace('ad AB','ad A′B') for x in ipassi('Dubhe',52,1.6,9,brg(A2,D_),t)]
    draw_intercept(S,A2,9,B,52,1.6,D_,'Rigel','Dubhe')
    S.pt(Fe,'P.ta del Fenaio','lm'); S.pt(A,'A 14h50m','ship'); S.pt(A2,'A′ 15h50m','ship'); S.pt(B,'B · Dubhe','ship')
    S.line(A,A2,'rotta','340° · 9 mg'); S.line(A2,D_,'rotta',f'{deg(brg(A2,D_))}'); S.line(B,D_,'rotta2','Dubhe 052°'); S.line(Fe,A,'ril2','095° · 2,5 mg')
    S.fix(D_,'D'); return S

@reg
def e5_4_3_7():
    S=Sol('5.4.3-7',(42.45,11.05))
    A=S.xy((42+23/60,10+58/60)); B=S.xy((42+31.5/60,11+8/60)); t=intercept(A,4,B,221,1.5); D_=add(B,u(221),1.5*t)
    S.dati=[('A (Daphne, 09h30m)','42°23,0′N 010°58,0′E, 4 kn'),('B (Sophia)','42°31,5′N 011°08,0′E, Rv 221°, 1,5 kn')]
    S.passi=ipassi('Sophia',221,1.5,4,brg(A,D_),t,'C'); draw_intercept(S,A,4,B,221,1.5,D_,'Daphne','Sophia')
    S.pt(A,'A · Daphne','ship'); S.pt(B,'B · Sophia','ship'); S.line(A,D_,'rotta',f'{deg(brg(A,D_))} · 4 kn'); S.line(B,D_,'rotta2','Sophia 221° · 1,5 kn')
    S.fix(D_,'C'); return S

@reg
def e5_4_3_8():
    S=Sol('5.4.3-8',lm('Faro di Punta Lividonia'))
    Li=S.xy('Faro di Punta Lividonia'); A2=add(Li,u(146),-3.1); B=S.xy((42.6,10+53/60)); t=intercept(A2,7,B,105,2.5); D_=add(B,u(105),2.5*t)
    S.dati=[('A′ (14h20m)','3,1 mg dal faro di Punta Lividonia per Rilv 146°'),('Mistral','7 kn dopo la chiamata'),('B (Ghibli)','42°36,0′N 010°53,0′E, Rv 105°, 2,5 kn')]
    S.passi=['A′: 3,1 mg dal faro di Punta Lividonia sul rilevamento 146°. Il tratto dal Giglio serve solo al racconto.']+[x.replace(' A ',' A′ ').replace('da A ','da A′ ').replace('Da A ','Da A′ ').replace('ad AB','ad A′B') for x in ipassi('Ghibli',105,2.5,7,brg(A2,D_),t)]
    draw_intercept(S,A2,7,B,105,2.5,D_,'Mistral','Ghibli')
    S.pt(Li,'P.ta Lividonia','lm'); S.pt(A2,'A′ 14h20m','ship'); S.pt(B,'B · Ghibli','ship')
    S.line(Li,A2,'ril2','146° · 3,1 mg'); S.line(A2,D_,'rotta',f'{deg(brg(A2,D_))} · 7 kn'); S.line(B,D_,'rotta2','Ghibli 105°')
    S.fix(D_,'D'); return S

if __name__=='__main__':
    for f in SOLS:
        S=f()
        if S is None: print(f.__name__,'--- da fare'); continue
        ok=S.check()
        print(S.id, S.res_txt, '| ufficiale:', S.ex['risposta_ufficiale'].replace('\n',' '), '|', 'OK' if ok else ('??' if ok is None else 'FUORI'))
