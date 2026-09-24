"""Soluzioni degli esercizi di scarroccio (famiglie 5.x.4, carte 5/D e 42/D)."""
import re, math
from geo import *
from es10 import Sol, deg, hm
def n1(v): return f'{v:.1f}'.replace('.',',')
def ll(g,m): return g+m/60
VENTI={'Tramontana':0,'Grecale':45,'Levante':90,'Scirocco':135,'Ostro':180,'Libeccio':225,'Ponente':270,'Maestrale':315}
def hhmm(h):
    h=h%24; H=int(h); M=int(round((h-H)*60))
    if M==60: H+=1; M=0
    return f'{H:02d}h{M:02d}m'
def sc_sign(course, wind):
    """+ se il vento arriva da sinistra (spinge a dritta), − se da dritta"""
    rel=(wind-course)%360
    return 1 if rel>180 else -1
def sgn(v): return f'+{v:g}°' if v>0 else f'−{abs(v):g}°'

class WSol(Sol):
    kind='pos'
    def check(s):
        r=s.ex['risposta_ufficiale']
        if s.kind=='pos': return super().check()
        nums=[float(x.replace(',','.')) for x in re.findall(r'(\d+(?:,\d+)?)',r)]
        if s.kind=='ora':
            a=nums[0]+nums[1]/60; b=nums[2]+nums[3]/60; return a-1e-6<=s.val<=b+1e-6
        a,b=nums[0],nums[1]; return a-0.5<=s.val<=b+0.5

def traverso_point(S, start, rv, Lname, pv, side):
    """punto della rotta rv (da start) in cui il punto cospicuo è al traverso della prora pv; side +1 dritta"""
    L=S.xy(Lname); b=norm(pv+side*90)
    return cross_lines(start,rv,L,b)
def side_of(S, start, rv, Lname):
    L=S.xy(Lname); v=u(rv); w=sub(L,start); cr=v[0]*w[1]-v[1]*w[0]
    return -1 if cr>0 else 1   # >0: a sinistra

SOLS=[]
def reg(f): SOLS.append(f); return f

def wind_txt(nome,sc,course,label='Rv'):
    return f'{nome} da {VENTI[nome]:03d}°: arriva da {"sinistra" if sc>0 else "dritta"} e spinge a {"dritta" if sc>0 else "sinistra"}, quindi Sc = {sgn(sc)}.'

@reg
def s5_1_4_1():
    S=WSol('5.1.4-1',lm('Faro dello Scoglietto')); S.kind='ora'
    A=S.xy("Capo Sant'Andrea"); C=S.xy('Capo della Vita'); rv=brg(A,C); Ve=dist(A,C)/2.5
    sc=10*sc_sign(rv,315); pv=rv-sc; side=side_of(S,A,rv,'Faro dello Scoglietto')
    T=traverso_point(S,A,rv,'Faro dello Scoglietto',pv,side); t=dist(A,T)/Ve
    S.val=10+t; S.res_txt=f'traverso alle {hhmm(S.val)}'
    S.passi=[f'Rv da Capo Sant\'Andrea a Capo della Vita: {deg(rv)}, {n1(dist(A,C))} mg in 2h30m: Ve = {n1(Ve)} kn.',wind_txt('Maestrale',sc,rv)+f' Pv = Rv − Sc = {deg(pv)}.',
             f'Il traverso si misura dalla prora: Scoglietto per Rilv = Pv {"+" if side>0 else "−"} 90° = {deg(pv+side*90)}. Dove questa linea taglia la rotta c\'è il punto.',f'{n1(dist(A,T))} mg a {n1(Ve)} kn = {hm(t*60)}: traverso alle {hhmm(S.val)}.']
    S.pt(A,"C. Sant'Andrea",'lm'); S.pt(C,'C. della Vita','lm'); S.pt(S.xy('Faro dello Scoglietto'),'Scoglietto','lm')
    S.line(A,C,'rotta',f'Rv {deg(rv)}'); S.line(A,add(A,u(pv),2.5),'rotta_l',''); S.line(T,S.xy('Faro dello Scoglietto'),'ril2',f'Rilv {deg(pv+side*90)}')
    S.fix(T,hhmm(S.val)); S.res_txt=f'traverso alle {hhmm(S.val)}'; return S

@reg
def s5_1_4_2():
    S=WSol('5.1.4-2',lm('Isola di Cerboli')); S.kind='ora'
    A=S.xy((ll(42,53.4),ll(10,6.6))); rv=90; sc=10; pv=rv-sc; side=side_of(S,A,rv,'Isola di Cerboli')
    T=traverso_point(S,A,rv,'Isola di Cerboli',pv,side); t=dist(A,T)/6
    S.val=7+20/60+t
    S.passi=['Rv 090°, Grecale da 045°: spinge a dritta, Sc = +10°: Pv = Rv − Sc = 080°.',f'Cerboli a {"dritta" if side>0 else "sinistra"}: al traverso lo si rileva per Pv {"+" if side>0 else "−"} 90° = {deg(pv+side*90)}.',
             f'Il punto al traverso è {n1(dist(A,T))} mg da A; a 6 kn servono {hm(t*60)}.',f'Traverso alle {hhmm(S.val)}.']
    S.pt(A,'A','ship'); S.pt(S.xy('Isola di Cerboli'),'Cerboli','lm'); S.line(A,T,'rotta','Rv 090°'); S.line(A,add(A,u(pv),3),'rotta_l','')
    S.line(T,S.xy('Isola di Cerboli'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,hhmm(S.val)); S.res_txt=f'traverso alle {hhmm(S.val)}'; return S

@reg
def s5_1_4_3():
    S=WSol('5.1.4-3',lm('Punta dei Ripalti'))
    A=S.xy((ll(42,41.5),ll(10,11.3))); pv=85; sc=8*sc_sign(pv,0); rv=pv+sc; side=side_of(S,A,rv,'Punta dei Ripalti')
    T=traverso_point(S,A,rv,'Punta dei Ripalti',pv,side)
    S.passi=[f'Pv 085°, Tramontana da nord: arriva da sinistra, Sc = {sgn(sc)}: Rv = Pv + Sc = {deg(rv)}.',f'Punta dei Ripalti a sinistra: al traverso la si rileva per Pv − 90° = {deg(pv-90)}.','Dove la linea del rilevamento taglia la rotta c\'è B.']
    S.pt(A,'A','ship'); S.pt(S.xy('Punta dei Ripalti'),'P.ta dei Ripalti','lm'); S.line(A,T,'rotta',f'Rv {deg(rv)}'); S.line(A,add(A,u(pv),4),'rotta_l','Pv 085°')
    S.line(T,S.xy('Punta dei Ripalti'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,'B'); return S

@reg
def s5_1_4_4():
    S=WSol('5.1.4-4',lm('Punta le Tombe'))
    A=S.xy((ll(42,39.6),ll(10,17.4))); pv=290; sc=5*sc_sign(pv,225); rv=pv+sc; side=side_of(S,A,rv,'Punta le Tombe')
    T=traverso_point(S,A,rv,'Punta le Tombe',pv,side)
    S.passi=[f'Pv 290°, Libeccio da 225°: arriva da sinistra, Sc = {sgn(sc)}: Rv = {deg(rv)}.',f'Punta le Tombe a dritta: al traverso per Pv + 90° = {deg(pv+90)}.','L\'incrocio con la rotta è B.']
    S.pt(A,'A','ship'); S.pt(S.xy('Punta le Tombe'),'P.ta le Tombe','lm'); S.line(A,T,'rotta',f'Rv {deg(rv)}'); S.line(A,add(A,u(pv),4),'rotta_l','Pv 290°')
    S.line(T,S.xy('Punta le Tombe'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,'B'); return S

@reg
def s5_1_4_5():
    S=WSol('5.1.4-5',lm('Punta dei Ripalti')); S.kind='ora'
    A=S.xy('Isola di Cerboli'); pv=190; sc=10*sc_sign(pv,315); rv=pv+sc; side=side_of(S,A,rv,'Punta dei Ripalti')
    T=traverso_point(S,A,rv,'Punta dei Ripalti',pv,side); t=dist(A,T)/6; S.val=10+t
    S.passi=[f'Pv 190°, Maestrale da 315°: arriva da dritta, Sc = {sgn(sc)}: Rv = {deg(rv)}.',f'Punta dei Ripalti a {"dritta" if side>0 else "sinistra"}: al traverso per {deg(pv+side*90)}.',f'Distanza da Cerboli al traverso: {n1(dist(A,T))} mg a 6 kn = {hm(t*60)}.',f'Traverso alle {hhmm(S.val)}.']
    S.pt(A,'Cerboli','lm'); S.pt(S.xy('Punta dei Ripalti'),'P.ta dei Ripalti','lm'); S.line(A,T,'rotta',f'Rv {deg(rv)}'); S.line(A,add(A,u(pv),4),'rotta_l','Pv 190°')
    S.line(T,S.xy('Punta dei Ripalti'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,hhmm(S.val)); S.res_txt=f'traverso alle {hhmm(S.val)}'; return S

@reg
def s5_2_4_1():
    S=WSol('5.2.4-1',lm('Faro di Punta Ala'))
    rv=25; sc=5*sc_sign(rv,315); pv=rv-sc; r1=pv+35; r2=pv+77
    F=cross_lines(S.xy('Punta Francese'),r1,S.xy('Faro di Punta Ala'),r2)
    S.passi=[f'Rv 025°, Maestrale da 315°: Sc = {sgn(sc)}, quindi Pv = Rv − Sc = {deg(pv)}.','I rilevamenti polari si contano dalla prora, non dalla rotta:',f'Punta Francese Rilv = {deg(pv)} + 35° = {deg(r1)}; Punta Ala Rilv = {deg(pv)} + 77° = {deg(r2)}.','I due rilevamenti contemporanei si incrociano nel punto nave.']
    for n,sh,r in (('Punta Francese','P.ta Francese',r1),('Faro di Punta Ala','Punta Ala',r2)):
        S.pt(S.xy(n),sh,'lm'); S.line(add(F,u(r),-1.5),S.xy(n),'ril' if r==r1 else 'ril2',f'Rilv {deg(r)}')
    S.line(add(F,u(rv),-2),add(F,u(rv),1),'rotta',f'Rv {deg(rv)}'); S.fix(F,'PN 10h00m'); return S

@reg
def s5_2_4_2():
    S=WSol('5.2.4-2',lm('Serbatoio di Marina di Grosseto'))
    A=S.xy('Scoglio dello Sparviero'); rv=140; sc=10*sc_sign(rv,225); pv=rv-sc; side=side_of(S,A,rv,'Serbatoio di Marina di Grosseto')
    T=traverso_point(S,A,rv,'Serbatoio di Marina di Grosseto',pv,side)
    S.passi=[f'Rv 140°, Libeccio da 225°: arriva da dritta, Sc = {sgn(sc)}: Pv = Rv − Sc = {deg(pv)}.',f'Serbatoio a {"dritta" if side>0 else "sinistra"}: al traverso per Pv {"+" if side>0 else "−"} 90° = {deg(pv+side*90)}.','L\'incrocio con la rotta 140° è A.']
    S.pt(A,'Sparviero','lm'); S.pt(S.xy('Serbatoio di Marina di Grosseto'),'Serbatoio','lm'); S.line(A,T,'rotta','Rv 140°'); S.line(A,add(A,u(pv),4),'rotta_l',f'Pv {deg(pv)}')
    S.line(T,S.xy('Serbatoio di Marina di Grosseto'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,'A'); return S

@reg
def s5_2_4_3():
    S=WSol('5.2.4-3',lm('Fanali di Castiglione della Pescaia'))
    A=S.xy((ll(42,40),ll(10,50))); rv=320; sc=10*sc_sign(rv,45); pv=rv-sc; side=side_of(S,A,rv,'Fanali di Castiglione della Pescaia')
    T=traverso_point(S,A,rv,'Fanali di Castiglione della Pescaia',pv,side)
    S.passi=[f'Rv 320°, Grecale da 045°: arriva da dritta, Sc = {sgn(sc)}: Pv = Rv − Sc = {deg(pv)}.',f'Fanali a dritta: al traverso per Pv + 90° = {deg(pv+90)}.','L\'incrocio con la rotta è B.']
    S.pt(A,'A','ship'); S.pt(S.xy('Fanali di Castiglione della Pescaia'),'Castiglione','lm'); S.line(A,T,'rotta','Rv 320°'); S.line(A,add(A,u(pv),3),'rotta_l',f'Pv {deg(pv)}')
    S.line(T,S.xy('Fanali di Castiglione della Pescaia'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,'B'); return S

@reg
def s5_2_4_4():
    S=WSol('5.2.4-4',lm('Fanali di Castiglione della Pescaia'))
    Lc=S.xy('Fanali di Castiglione della Pescaia'); A=add(Lc,u(320),-1); pv=253; sc=7*sc_sign(pv,225); rv=pv+sc; Ve=4; B=add(A,u(rv),Ve*2)
    S.passi=['A: il fanale è per Rilv 320° a 1 mg, quindi A è 1 mg per 140° dal fanale.',f'Pv 253°, Libeccio da 225°: arriva da sinistra, Sc = {sgn(sc)}: Rv = {deg(rv)}.','Ve = Vp − 1 = 4 kn; in 2 ore 8 mg per la Rv.']
    S.pt(Lc,'Castiglione','lm'); S.pt(A,'A 10h00m','ship'); S.line(Lc,A,'ril2','1 mg'); S.line(A,B,'rotta',f'Rv {deg(rv)} · 8 mg'); S.line(A,add(A,u(pv),8),'rotta_l',f'Pv 253°')
    S.fix(B,'B 12h00m'); return S

@reg
def s5_2_4_5():
    S=WSol('5.2.4-5',lm('Scoglio dello Sparviero')); S.kind='pv'
    A=S.xy((ll(42,41.7),ll(10,51.5))); B=add(S.xy('Scoglio dello Sparviero'),u(180),1); rv=brg(A,B); sc=5*sc_sign(rv,270); pv=rv-sc
    S.val=pv
    S.passi=['B: 1 mg a sud dello Sparviero.',f'Rv da A a B: {deg(rv)}.',f'Ponente da 270°: arriva da sinistra, Sc = {sgn(sc)}.',f'Pv = Rv − Sc = {deg(pv)}: la prora va tenuta più al vento della rotta.']
    S.pt(A,'A','ship'); S.pt(S.xy('Scoglio dello Sparviero'),'Sparviero','lm'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); S.line(A,add(A,u(pv),dist(A,B)),'rotta_l',f'Pv {deg(pv)}'); S.fix(B,'B'); S.res_txt=f'Pv {deg(pv)}'; return S

@reg
def s5_3_4_1():
    S=WSol('5.3.4-1',lm("Faro dell'Isola di Pianosa"))
    rv=150; sc=8*sc_sign(rv,270); pv=rv-sc; rl=pv+138; F=S.xy("Faro dell'Isola di Pianosa"); A=add(F,u(rl),-3.6)
    # limite della zona 2 di Montecristo: cerchio di 3 miglia dalla costa (vedi note)
    M=S.xy('Isola di Montecristo'); R=3+1.1
    v=u(rv); w=sub(A,M); bq=2*(w[0]*v[0]+w[1]*v[1]); cq=w[0]**2+w[1]**2-R*R; k=(-bq-math.sqrt(bq*bq-4*cq))/2; B=add(A,v,k)
    S.passi=[f'Rv 150°, Ponente da 270°: arriva da dritta, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Il faro è per ρ +138° dalla prora: Rilv = {deg(pv)} + 138° = {deg(rl)}; A è 3,6 mg dal faro sul rilevamento opposto.',
             'Da A traccia la Rv 150° fino al limite della zona 2 di Montecristo segnato sulla carta: lì c\'è B.']
    S.pt(F,'Pianosa','lm'); S.pt(A,'A 09h00m','ship'); S.pt(M,'Montecristo','lm'); S.line(F,A,'ril2','3,6 mg'); S.line(A,B,'rotta','Rv 150°'); S.fix(B,'B')
    S.note='Il limite della zona 2 è quello stampato sulla carta 5/D; qui lo approssimiamo con un cerchio attorno all\'isola.'; return S

@reg
def s5_3_4_2():
    S=WSol('5.3.4-2',lm('Isolotto della Scola'))
    rv=72; sc=2*sc_sign(rv,0); pv=rv-sc; r1=pv-119; r2=pv-77
    F=cross_lines(S.xy('Torre di Cala della Ruta'),r1,S.xy('Isolotto della Scola'),r2)
    S.passi=[f'Rv 072°, Tramontana da nord: arriva da sinistra, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Torre di Cala della Ruta: {deg(pv)} − 119° = {deg(r1)}; La Scola: {deg(pv)} − 77° = {deg(r2)}.','I due rilevamenti si incrociano nel punto nave.']
    for n,sh,r,k in (('Torre di Cala della Ruta','T. Cala della Ruta',r1,'ril'),('Isolotto della Scola','La Scola',r2,'ril2')):
        S.pt(S.xy(n),sh,'lm'); S.line(add(F,u(r),-1),S.xy(n),k,f'Rilv {deg(r)}')
    S.line(add(F,u(rv),-1.5),add(F,u(rv),1),'rotta','Rv 072°'); S.fix(F,'PN 10h00m'); return S

@reg
def s5_3_4_3():
    S=WSol('5.3.4-3',lm("Faro dell'Isola di Pianosa"))
    Af=S.xy("Faro di Scoglio d'Africa"); A=add(Af,u(90),-2.8); rv=25; sc=8*sc_sign(rv,90); pv=rv-sc; rl=pv-137
    B=cross_lines(A,rv,S.xy("Faro dell'Isola di Pianosa"),rl)
    S.passi=['A: Scoglio d\'Africa per Rilv 090° a 2,8 mg, quindi A è 2,8 mg a ovest del faro.',f'Rv 025°, Levante da 090°: arriva da dritta, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Faro di Pianosa per ρ −137°: Rilv = {deg(pv)} − 137° = {deg(rl)}.','Dove questo rilevamento taglia la rotta c\'è B.']
    S.pt(Af,"Scoglio d'Africa",'lm'); S.pt(A,'A','ship'); S.pt(S.xy("Faro dell'Isola di Pianosa"),'Pianosa','lm'); S.line(A,B,'rotta','Rv 025°'); S.line(B,S.xy("Faro dell'Isola di Pianosa"),'ril2',f'Rilv {deg(rl)}'); S.fix(B,'B'); return S

@reg
def s5_3_4_4():
    S=WSol('5.3.4-4',lm("Faro dell'Isola di Pianosa"))
    A=add(S.xy("Faro di Scoglio d'Africa"),u(315),1.5); rv=352; sc=8*sc_sign(rv,315); pv=rv-sc; side=side_of(S,A,rv,"Faro dell'Isola di Pianosa")
    T=traverso_point(S,A,rv,"Faro dell'Isola di Pianosa",pv,side)
    S.passi=['A: 1,5 mg a nord-ovest di Scoglio d\'Africa.',f'Rv 352°, Maestrale da 315°: arriva da sinistra, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Pianosa a dritta: al traverso per Pv + 90° = {deg(pv+90)}.','L\'incrocio con la rotta è B.']
    S.pt(S.xy("Faro di Scoglio d'Africa"),"Scoglio d'Africa",'lm'); S.pt(A,'A','ship'); S.pt(S.xy("Faro dell'Isola di Pianosa"),'Pianosa','lm')
    S.line(A,T,'rotta','Rv 352°'); S.line(T,S.xy("Faro dell'Isola di Pianosa"),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,'B'); return S

@reg
def s5_3_4_5():
    S=WSol('5.3.4-5',lm('Punta Brigantina')); S.kind='ora'
    A=add(S.xy("Faro di Scoglio d'Africa"),u(225),2); rv=20; sc=-6; pv=rv-sc; side=side_of(S,A,rv,'Punta Brigantina')
    T=traverso_point(S,A,rv,'Punta Brigantina',pv,side); t=dist(A,T)/18; S.val=8.5+t
    S.passi=['A: 2 mg a sud-ovest di Scoglio d\'Africa.',f'Scirocco, Sc = −6°: Pv = Rv − Sc = 020° + 6° = {deg(pv)}.',f'Punta Brigantina a {"dritta" if side>0 else "sinistra"}: al traverso per {deg(pv+side*90)}.',f'{n1(dist(A,T))} mg a 18 kn = {hm(t*60)}: B alle {hhmm(S.val)}.']
    S.pt(S.xy("Faro di Scoglio d'Africa"),"Scoglio d'Africa",'lm'); S.pt(A,'A 08h30m','ship'); S.pt(S.xy('Punta Brigantina'),'P.ta Brigantina','lm')
    S.line(A,T,'rotta','Rv 020°'); S.line(T,S.xy('Punta Brigantina'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,hhmm(S.val)); S.res_txt=f'B alle {hhmm(S.val)}'; return S

@reg
def s5_4_4_1():
    S=WSol('5.4.4-1',lm('Faro di Punta del Fenaio'))
    rv=313; sc=8*sc_sign(rv,0); pv=rv-sc; rl=pv-90; A=add(S.xy('Faro di Punta del Fenaio'),u(rl),-1.8)
    S.passi=[f'Rv 313°, Tramontana da nord: arriva da dritta, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Il faro è per ρ −90° dalla prora: Rilv = {deg(pv)} − 90° = {deg(rl)}.',f'A: 1,8 mg dal faro sul rilevamento opposto ({deg(rl+180)}).']
    S.pt(S.xy('Faro di Punta del Fenaio'),'P.ta del Fenaio','lm'); S.line(A,S.xy('Faro di Punta del Fenaio'),'ril2',f'Rilv {deg(rl)} · 1,8 mg'); S.line(add(A,u(rv),-1.5),add(A,u(rv),1.5),'rotta','Rv 313°'); S.fix(A,'A 09h00m'); return S

@reg
def s5_4_4_2():
    S=WSol('5.4.4-2',lm('Faro di Formica Grande'))
    rv=45; sc=5*sc_sign(rv,0); pv=rv-sc; rl=pv-90; A=add(S.xy('Faro di Formica Grande'),u(rl),-2)
    S.passi=[f'Rv 045°, Tramontana da nord: arriva da sinistra, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Traverso sinistro: Rilv = Pv − 90° = {deg(rl)}.',f'Punto nave: 2 mg dal faro sul rilevamento opposto ({deg(rl+180)}).']
    S.pt(S.xy('Faro di Formica Grande'),'Formica Grande','lm'); S.line(A,S.xy('Faro di Formica Grande'),'ril2',f'Rilv {deg(rl)} · 2 mg'); S.line(add(A,u(rv),-1.5),add(A,u(rv),1.5),'rotta','Rv 045°'); S.fix(A,'PN 09h00m'); return S

@reg
def s5_4_4_3():
    S=WSol('5.4.4-3',lm('Fanali del porto del Giglio')); S.kind='vp'
    A=S.xy((ll(42,21.1),ll(11,13.5))); G=S.xy('Fanali del porto del Giglio'); D_=dist(A,G); t=2.25; Ve=D_/t; Vp=Ve+1
    S.val=Vp; S.res_txt=f'Vp {n1(Vp)} kn'
    S.passi=[f'Da A ai fanali del Giglio: {n1(D_)} mg per {deg(brg(A,G))}.','Dalle 15h30m alle 17h45m: 2h15m = 2,25 ore.',f'Ve = {n1(D_)} / 2,25 = {n1(Ve)} kn. Il vento toglie 1 nodo: Vp = Ve + 1 = {n1(Vp)} kn.','Lo scarroccio di 7° cambia la prora da tenere, non la velocità.']
    S.pt(A,'A','ship'); S.pt(G,'Giglio Porto','lm'); S.line(A,G,'rotta',f'Rv {deg(brg(A,G))} · {n1(D_)} mg'); return S

@reg
def s5_4_4_4():
    S=WSol('5.4.4-4',lm('Faro di Punta Lividonia'))
    A=add(S.xy('Faro di Punta del Fenaio'),u(247.5),1.5); rv=60; sc=8; pv=rv-sc; rl=pv+45
    B=cross_lines(A,rv,S.xy('Faro di Punta Lividonia'),rl)
    S.passi=['A: 1,5 mg dal faro di Punta del Fenaio verso WSW (247,5°).',f'Maestrale, Sc = +8°: Pv = Rv − Sc = {deg(pv)}.',f'Punta Lividonia per ρ +45° dalla prora: Rilv = {deg(pv)} + 45° = {deg(rl)}.','Dove questo rilevamento taglia la rotta 060° c\'è B.']
    S.pt(S.xy('Faro di Punta del Fenaio'),'P.ta del Fenaio','lm'); S.pt(A,'A','ship'); S.pt(S.xy('Faro di Punta Lividonia'),'P.ta Lividonia','lm')
    S.line(A,B,'rotta','Rv 060°'); S.line(B,S.xy('Faro di Punta Lividonia'),'ril2',f'Rilv {deg(rl)}'); S.fix(B,'B'); return S

@reg
def s5_4_4_5():
    S=WSol('5.4.4-5',lm('Faro di Talamone'))
    A=add(S.xy('Faro di Formica Grande'),u(315),-1.5); rv=95; sc=5*sc_sign(rv,45); pv=rv-sc; side=side_of(S,A,rv,'Faro di Talamone')
    T=traverso_point(S,A,rv,'Faro di Talamone',pv,side)
    S.passi=['A: il faro di Formica Grande si vede per NW a 1,5 mg, quindi A è 1,5 mg a sud-est del faro.',f'Rv 095°, Grecale da 045°: arriva da sinistra, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Talamone a sinistra: al traverso per Pv − 90° = {deg(pv-90)}.','L\'incrocio con la rotta è B.']
    S.pt(S.xy('Faro di Formica Grande'),'Formica Grande','lm'); S.pt(A,'A','ship'); S.pt(S.xy('Faro di Talamone'),'Talamone','lm')
    S.line(A,T,'rotta','Rv 095°'); S.line(T,S.xy('Faro di Talamone'),'ril2',f'Rilv {deg(pv+side*90)}'); S.fix(T,'B'); return S

# ---------------- carta 42/D ----------------
@reg
def s5_5_4_1():
    S=WSol('5.5.4-1',lm('Porto di Bonifacio')); S.kind='pv'; S.carta='42D'
    A=S.xy((ll(41,15.3),ll(9,11.5))); B=S.xy('Porto di Bonifacio'); rv=brg(A,B); sc=10*sc_sign(rv,270); pv=rv-sc
    S.val=pv; S.res_txt=f'Pv {deg(pv)}'
    S.passi=[f'Rv da A al porto di Bonifacio: {deg(rv)}.',f'Ponente da 270°: arriva da sinistra, Sc = {sgn(sc)}.',f'Pv = Rv − Sc = {deg(pv)}.']
    S.pt(A,'A','ship'); S.pt(B,'Bonifacio','lm'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); S.line(A,add(A,u(pv),dist(A,B)*0.9),'rotta_l',f'Pv {deg(pv)}'); return S

@reg
def s5_6_4_1():
    S=WSol('5.6.4-1',lm('Faro delle Isolette Monaci')); S.carta='42D'
    L=S.xy('Faro delle Isolette Monaci'); A=add(L,u(190),-1); pv=50; sc=8*sc_sign(pv,180); rv=pv+sc; Ve=8; B=add(A,u(rv),Ve*100/60)
    S.passi=['A: il faro è per Rilv 190° a 1 mg, quindi A è 1 mg per 010° dal faro.',f'Pv 050°, Ostro da sud: arriva da dritta, Sc = {sgn(sc)}: Rv = {deg(rv)}.','Ve = Vp + 1 = 8 kn. Dalle 10h50m alle 12h30m: 1h40m, cioè 13,3 mg.']
    S.pt(L,'Isolette Monaci','lm'); S.pt(A,'A 10h50m','ship'); S.line(L,A,'ril2','1 mg'); S.line(A,B,'rotta',f'Rv {deg(rv)} · 13,3 mg'); S.fix(B,'B 12h30m'); return S

@reg
def s5_7_4_1():
    S=WSol('5.7.4-1',lm('Punta li Canneddi')); S.kind='ora'; S.carta='42D'
    A=S.xy((ll(40,56.7),ll(8,42.5))); rv=45; sc=6*sc_sign(rv,315); pv=rv-sc
    T=traverso_point(S,A,rv,'Punta li Canneddi',pv,1); t=dist(A,T)/5.5; S.val=11.25+t
    S.passi=[f'Rv 045°, Maestrale da 315°: arriva da sinistra, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Punta li Canneddi a dritta per ρ 90°: Rilv = Pv + 90° = {deg(pv+90)}.',f'Punto sulla rotta a {n1(dist(A,T))} mg da A; a 5,5 kn servono {hm(t*60)}.',f'Traverso alle {hhmm(S.val)}.']
    S.pt(A,'A 11h15m','ship'); S.pt(S.xy('Punta li Canneddi'),'P.ta li Canneddi','lm'); S.line(A,T,'rotta','Rv 045°'); S.line(T,S.xy('Punta li Canneddi'),'ril2',f'Rilv {deg(pv+90)}')
    S.fix(T,hhmm(S.val)); S.res_txt=f'traverso alle {hhmm(S.val)}'; return S

@reg
def s5_8_4_1():
    S=WSol('5.8.4-1',lm('Faro dello Scoglio Mortoriotto')); S.kind='ora'; S.carta='42D'
    Tv=S.xy('Faro di Punta Timone'); A=add(Tv,u(127),-1.8); rv=345; sc=10*sc_sign(rv,45); pv=rv-sc
    T=traverso_point(S,A,rv,'Faro dello Scoglio Mortoriotto',pv,-1); t=dist(A,T)/6.5; S.val=10+25/60+t
    S.passi=['A: il faro di Punta Timone è per Rilv 127° a 1,8 mg: A è 1,8 mg per 307° dal faro.',f'Rv 345°, Grecale da 045°: arriva da dritta, Sc = {sgn(sc)}: Pv = {deg(pv)}.',f'Mortoriotto per ρ −90°: Rilv = Pv − 90° = {deg(pv-90)}.',f'{n1(dist(A,T))} mg a 6,5 kn = {hm(t*60)}: traverso alle {hhmm(S.val)}.']
    S.pt(Tv,'P.ta Timone','lm'); S.pt(A,'A 10h25m','ship'); S.pt(S.xy('Faro dello Scoglio Mortoriotto'),'Mortoriotto','lm'); S.line(Tv,A,'ril','1,8 mg')
    S.line(A,T,'rotta','Rv 345°'); S.line(T,S.xy('Faro dello Scoglio Mortoriotto'),'ril2',f'Rilv {deg(pv-90)}'); S.fix(T,hhmm(S.val)); S.res_txt=f'traverso alle {hhmm(S.val)}'; return S

if __name__=='__main__':
    for fn in SOLS:
        S=fn(); print(S.id, S.res_txt, '| ufficiale', S.ex['risposta_ufficiale'].replace('\n',' '), '|', 'OK' if S.check() else 'FUORI')
