"""Soluzioni degli esercizi di carburante e autonomia (famiglie 5.1.2-5.4.2, carta 5/D)."""
import re, math
from geo import *
from es10 import Sol, deg, hm
def n1(v): return f'{v:.1f}'.replace('.',',')
def ll(g,m): return g+m/60

def fuel_range(r):
    v=[float(x.replace(',','.')) for x in re.findall(r'(\d+(?:,\d+)?)',r)]; return v[0],v[1]

class FSol(Sol):
    def check(s):
        a,b=fuel_range(s.ex['risposta_ufficiale']); return a-1e-6<=s.fuel<=b+1e-6

def traverso45(S, start, course, Lname, side, dt_min, Vp=None):
    """rilevamenti polari 45°-90° (side +1 dritta, -1 sinistra): punto al traverso e velocità"""
    L=S.xy(Lname); b90=course+side*90
    if Vp is not None:
        d=Vp*dt_min/60; B=add(L,u(b90),-d); V=Vp
    else:
        # proiezione del punto cospicuo sulla rotta
        v=u(course); w=sub(L,start); k=w[0]*v[0]+w[1]*v[1]; B=add(start,v,k); d=dist(L,B); V=d/(dt_min/60)
    P45=add(B,u(course),-d)
    return B,P45,d,V

def legs_fuel(S, legs, V, cons, ris=0.3):
    D=sum(dist(a,b) for a,b in legs); t=D/V; f=t*cons*(1+ris)
    S.D=D; S.t=t; S.fuel=f; S.res_txt=f'{n1(f)} litri'
    return D,t,f

def fuel_passi(D,V,t,cons,f,ris=0.3):
    return [f'Distanza totale {n1(D)} mg; a {n1(V)} kn servono {n1(D)} / {n1(V)} = {n1(t)} ore ({hm(t*60)}).',
            f'Carburante: {n1(t)} h × {n1(cons)} l/h = {n1(t*cons)} litri; più il {int(ris*100)}% di riserva: {n1(f)} litri.']

def draw_45(S,Lname,lab,P45,B,course,side,t1,t2):
    L=S.xy(Lname); S.pt(L,lab,'lm')
    S.line(P45,L,'ril',f'{t1} · ρ {"+" if side>0 else "−"}45°'); S.line(B,L,'ril2',f'{t2} · al traverso')
    S.pt(P45,t1,'ship')

SOLS=[]
def reg(f): SOLS.append(f); return f

@reg
def f5_1_2_1():
    S=FSol('5.1.2-1',lm("Capo d'Ortano"))
    C0=S.xy('Isola di Cerboli'); A=add(S.xy("Capo d'Ortano"),u(90),4.9); B=S.xy((ll(42,40),ll(10,30)))
    D,t,f=legs_fuel(S,[(C0,A),(A,B)],6,12)
    S.dati=[('Partenza','Isola Cerboli, Rv 180°, 6 kn'),('A',"Capo d'Ortano al traverso a 4,9 mg"),('B','42°40′N 010°30′E'),('Consumo','12 l/h')]
    S.passi=[f"Rotta 180° da Cerboli: Capo d'Ortano al traverso di dritta a 4,9 mg dà A (4,9 mg a est del capo).",f'Cerboli-A = {n1(dist(C0,A))} mg; A-B = {n1(dist(A,B))} mg.']+fuel_passi(D,6,t,12,f)
    S.pt(C0,'Cerboli','lm'); S.pt(S.xy("Capo d'Ortano"),"C. d'Ortano",'lm'); S.pt(A,'A','ship'); S.pt(B,'B','fix')
    S.line(C0,A,'rotta','180°'); S.line(A,B,'rotta',f'{deg(brg(A,B))} · {n1(dist(A,B))} mg'); S.line(S.xy("Capo d'Ortano"),A,'ril2','4,9 mg')
    return S

@reg
def f5_1_2_2():
    S=FSol('5.1.2-2',lm('Faro dello Scoglietto'))
    Pv=70; B,P45,d,V=traverso45(S,None,Pv,'Faro dello Scoglietto',+1,20,6); F=S.xy('Punta Falcone')
    D,t,f=legs_fuel(S,[(B,F)],6,10)
    S.passi=['V = +1°: Pv = 070°. Scoglietto a ρ +45° e poi +90°: la distanza al traverso è uguale al cammino tra i due rilevamenti.',
             f'Cammino in 20 minuti a 6 kn = 2 mg: A è 2 mg dal faro sul rilevamento 160°.',f'A - Punta Falcone = {n1(D)} mg.']+fuel_passi(D,6,t,10,f)
    draw_45(S,'Faro dello Scoglietto','Scoglietto',P45,B,Pv,1,'11h30m','11h50m'); S.pt(B,'A 11h50m','ship'); S.pt(F,'Punta Falcone','fix')
    S.line(P45,B,'rotta','070°'); S.line(B,F,'rotta2',f'{deg(brg(B,F))} · {n1(D)} mg'); return S

@reg
def f5_1_2_3():
    S=FSol('5.1.2-3',lm('Faro di Capo Poro'))
    A=S.xy((ll(42,44.2),ll(10,21.2))); Pv=247; B,P45,d,V=traverso45(S,A,Pv,'Faro di Capo Poro',+1,15,6); C=S.xy((ll(42,40),10.0))
    D,t,f=legs_fuel(S,[(A,B),(B,C)],6,4)
    S.passi=['Capo Poro a ρ +45° alle 12h00m e al traverso alle 12h15m: distanza al traverso = 6 × 15/60 = 1,5 mg.',f'B è 1,5 mg dal faro sul rilevamento {deg(Pv+90)}.',f'A-B = {n1(dist(A,B))} mg; B-C = {n1(dist(B,C))} mg.']+fuel_passi(D,6,t,4,f)
    draw_45(S,'Faro di Capo Poro','Capo Poro',P45,B,Pv,1,'12h00m','12h15m'); S.pt(A,'A','ship'); S.pt(B,'B','ship'); S.pt(C,'C','fix')
    S.line(A,B,'rotta','247°'); S.line(B,C,'rotta2',f'{deg(brg(B,C))} · {n1(dist(B,C))} mg'); return S

@reg
def f5_1_2_4():
    S=FSol('5.1.2-4',lm('Faro dello Scoglietto'))
    N=S.xy('Punta del Nasuto'); Pv=56; B,P45,d,V=traverso45(S,None,Pv,'Faro dello Scoglietto',+1,28,6); Sa=S.xy('Porticciolo di Salivoli')
    D,t,f=legs_fuel(S,[(N,B),(B,Sa)],6,10)
    S.passi=['V = −4°: Pv = 056°. Scoglietto a ρ +45° e +90°: 6 × 28/60 = 2,8 mg al traverso.',f'A è 2,8 mg dal fanale sul rilevamento 146°.',f'Nasuto-A = {n1(dist(N,B))} mg; A-Salivoli = {n1(dist(B,Sa))} mg.']+fuel_passi(D,6,t,10,f)
    draw_45(S,'Faro dello Scoglietto','Scoglietto',P45,B,Pv,1,'10h00m','10h28m'); S.pt(N,'Punta del Nasuto','lm'); S.pt(B,'A','ship'); S.pt(Sa,'Salivoli','fix')
    S.line(N,B,'rotta','056°'); S.line(B,Sa,'rotta2',f'{deg(brg(B,Sa))} · {n1(dist(B,Sa))} mg'); return S

@reg
def f5_1_2_5():
    S=FSol('5.1.2-5',lm('Isola Corbelli'))
    Fe=S.xy('Punta di Fetovaia'); Pv=105; B,P45,d,V=traverso45(S,None,Pv,'Isola Corbelli',-1,16,6); R=S.xy('Punta dei Ripalti')
    D,t,f=legs_fuel(S,[(Fe,B),(B,R)],6,12)
    S.passi=['Corbelli a ρ −45° e −90°: 6 × 16/60 = 1,6 mg al traverso.','A è 1,6 mg dall\'isolotto sul rilevamento 015°.',f'Fetovaia-A = {n1(dist(Fe,B))} mg; A-Ripalti = {n1(dist(B,R))} mg.']+fuel_passi(D,6,t,12,f)
    draw_45(S,'Isola Corbelli','Corbelli',P45,B,Pv,-1,'10h00m','10h16m'); S.pt(Fe,'Fetovaia','lm'); S.pt(B,'A','ship'); S.pt(R,'Punta dei Ripalti','fix')
    S.line(Fe,B,'rotta','105°'); S.line(B,R,'rotta2',f'{deg(brg(B,R))}'); return S

@reg
def f5_2_2_1():
    S=FSol('5.2.2-1',lm('Scoglio dello Sparviero'))
    C0=S.xy('Fanali di Castiglione della Pescaia'); Pv=270; B,P45,d,V=traverso45(S,None,Pv,'Scoglio dello Sparviero',+1,22,6); T=S.xy((ll(42,50),ll(10,37)))
    D,t,f=legs_fuel(S,[(C0,B),(B,T)],6,10)
    S.passi=['V = −1°: Pv = 270°. Sparviero a ρ +45° e +90°: 6 × 22/60 = 2,2 mg al traverso.','A è 2,2 mg a sud dello scoglio.',f'Castiglione-A = {n1(dist(C0,B))} mg; A-B = {n1(dist(B,T))} mg.']+fuel_passi(D,6,t,10,f)
    draw_45(S,'Scoglio dello Sparviero','Sparviero',P45,B,Pv,1,'09h00m','09h22m'); S.pt(C0,'Castiglione','lm'); S.pt(B,'A','ship'); S.pt(T,'B','fix')
    S.line(C0,B,'rotta','270°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

@reg
def f5_2_2_2():
    S=FSol('5.2.2-2',lm('Scoglio dello Sparviero'))
    C0=S.xy('Fanali di Castiglione della Pescaia'); Pv=270; B,P45,d,V=traverso45(S,None,Pv,'Scoglio dello Sparviero',+1,30,4.4); T=S.xy((ll(42,40),ll(10,50)))
    D,t,f=legs_fuel(S,[(C0,B),(B,T)],4.4,3.5)
    S.passi=['Sparviero a ρ +45° e al traverso: 4,4 × 30/60 = 2,2 mg al traverso.',f'Castiglione-traverso = {n1(dist(C0,B))} mg; traverso-destinazione = {n1(dist(B,T))} mg.']+fuel_passi(D,4.4,t,3.5,f)
    draw_45(S,'Scoglio dello Sparviero','Sparviero',P45,B,Pv,1,'13h00m','13h30m'); S.pt(C0,'Castiglione','lm'); S.pt(T,'arrivo','fix')
    S.line(C0,B,'rotta','270°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

@reg
def f5_2_2_3():
    S=FSol('5.2.2-3',lm('Faro di Punta Ala'))
    C0=S.xy('Fanale di Carbonifera'); Pv=180; B,P45,d,V=traverso45(S,None,Pv,'Faro di Punta Ala',-1,22,6); T=S.xy((ll(42,40),ll(10,40)))
    D,t,f=legs_fuel(S,[(C0,B),(B,T)],6,15)
    S.passi=['Punta Ala a ρ −45° e −90°: 6 × 22/60 = 2,2 mg al traverso, a ovest del faro.',f'Carbonifera-A = {n1(dist(C0,B))} mg; A-B = {n1(dist(B,T))} mg.']+fuel_passi(D,6,t,15,f)
    draw_45(S,'Faro di Punta Ala','Punta Ala',P45,B,Pv,-1,'08h00m','08h22m'); S.pt(C0,'Carbonifera','lm'); S.pt(B,'A','ship'); S.pt(T,'B','fix')
    S.line(C0,B,'rotta','180°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

@reg
def f5_2_2_4():
    S=FSol('5.2.2-4',lm('Scoglio dello Sparviero'))
    A=S.xy((ll(42,40),ll(10,55))); T=S.xy((ll(42,50),ll(10,37)))
    D,t,f=legs_fuel(S,[(A,T)],6,10)
    S.passi=[f'Rotta A-B: {deg(brg(A,T))}, {n1(D)} mg. I due rilevamenti dello Sparviero servono solo a verificare che non ci sono deriva né scarroccio.']+fuel_passi(D,6,t,10,f)
    S.pt(A,'A','ship'); S.pt(T,'B','fix'); S.pt(S.xy('Scoglio dello Sparviero'),'Sparviero','lm'); S.line(A,T,'rotta',f'{deg(brg(A,T))} · {n1(D)} mg'); return S

@reg
def f5_2_2_5():
    S=FSol('5.2.2-5',lm('Scoglio dello Sparviero'))
    A=S.xy((ll(42,38.8),ll(10,58.5))); Pv=302; B,P45,d,V=traverso45(S,A,Pv,'Scoglio dello Sparviero',+1,17)
    D,t,f=legs_fuel(S,[(A,B)],V,5)
    S.passi=['V = −3°: Pv = 302°. Il traverso B è il piede della perpendicolare dallo scoglio alla rotta.',f'Distanza al traverso {n1(d)} mg, percorsa in 17 minuti: V = {n1(d)} × 60/17 = {n1(V)} kn.',f'A-B = {n1(D)} mg.']+fuel_passi(D,V,t,5,f)
    draw_45(S,'Scoglio dello Sparviero','Sparviero',P45,B,Pv,1,'11h00m','11h17m'); S.pt(A,'A','ship'); S.pt(B,'B','fix'); S.line(A,B,'rotta','302°'); return S

@reg
def f5_3_2_1():
    S=FSol('5.3.2-1',lm('Monte della Fortezza'))
    A=add(S.xy("Faro di Scoglio d'Africa"),u(90),0.9); B=add(S.xy('Monte della Fortezza'),u(180),-2.8)
    D,t,f=legs_fuel(S,[(A,B)],5.5,38)
    S.passi=['A: 0,9 mg a est di Scoglio d\'Africa.','B: Monte della Fortezza per Rilv 180° a 2,8 mg, cioè 2,8 mg a nord della vetta.',f'A-B = {n1(D)} mg per {deg(brg(A,B))}.']+fuel_passi(D,5.5,t,38,f)
    S.pt(S.xy("Faro di Scoglio d'Africa"),"Scoglio d'Africa",'lm'); S.pt(S.xy('Monte della Fortezza'),'M. della Fortezza','lm'); S.pt(A,'A','ship'); S.pt(B,'B','fix')
    S.line(A,B,'rotta',f'{deg(brg(A,B))} · {n1(D)} mg'); S.line(B,S.xy('Monte della Fortezza'),'ril2','180° · 2,8 mg'); return S

@reg
def f5_3_2_2():
    S=FSol('5.3.2-2',lm("Faro di Scoglio d'Africa"))
    A=S.xy((ll(42,30),ll(10,30))); Pv=253; B,P45,d,V=traverso45(S,A,Pv,"Faro di Scoglio d'Africa",-1,27,6); C=S.xy((ll(42,30),10.0))
    D,t,f=legs_fuel(S,[(A,B),(B,C)],6,10)
    S.passi=["Scoglio d'Africa a ρ −45° e −90°: 6 × 27/60 = 2,7 mg al traverso.",'B è 2,7 mg dal faro sul rilevamento 163°.',f'A-B = {n1(dist(A,B))} mg; B-C = {n1(dist(B,C))} mg.']+fuel_passi(D,6,t,10,f)
    draw_45(S,"Faro di Scoglio d'Africa","Scoglio d'Africa",P45,B,Pv,-1,'10h00m','10h27m'); S.pt(A,'A','ship'); S.pt(B,'B','ship'); S.pt(C,'C','fix')
    S.line(A,B,'rotta','253°'); S.line(B,C,'rotta2',f'{deg(brg(B,C))}'); return S

@reg
def f5_3_2_3():
    S=FSol('5.3.2-3',lm('Punta Brigantina'))
    A=S.xy((ll(42,30),ll(10,30))); Pv=275; B,P45,d,V=traverso45(S,A,Pv,'Punta Brigantina',+1,25); Af=S.xy("Faro di Scoglio d'Africa")
    D,t,f=legs_fuel(S,[(A,B),(B,Af)],V,10)
    S.passi=['Il traverso B è il piede della perpendicolare da Punta Brigantina alla rotta 275°.',f'Distanza al traverso {n1(d)} mg in 25 minuti: V = {n1(V)} kn.',f"A-B = {n1(dist(A,B))} mg; B - Scoglio d'Africa = {n1(dist(B,Af))} mg per {deg(brg(B,Af))}."]+fuel_passi(D,V,t,10,f)
    draw_45(S,'Punta Brigantina','P.ta Brigantina',P45,B,Pv,1,'10h00m','10h25m'); S.pt(A,'A','ship'); S.pt(B,'B 10h25m','ship'); S.pt(Af,"Scoglio d'Africa",'fix')
    S.line(A,B,'rotta','275°'); S.line(B,Af,'rotta2',f'{deg(brg(B,Af))}'); return S

@reg
def f5_3_2_4():
    S=FSol('5.3.2-4',lm("Faro dell'Isola di Pianosa"))
    A=S.xy((ll(42,20),ll(10,9.2))); Pv=0; B,P45,d,V=traverso45(S,A,Pv,"Faro dell'Isola di Pianosa",-1,15); C=S.xy((ll(42,30),ll(10,20)))
    D,t,f=legs_fuel(S,[(A,B),(B,C)],V,6)
    S.passi=['Il traverso B è il punto della rotta 000° alla stessa latitudine del faro di Pianosa.',f'Distanza al traverso {n1(d)} mg in 15 minuti: V = {n1(V)} kn.',f'A-B = {n1(dist(A,B))} mg; B-C = {n1(dist(B,C))} mg.']+fuel_passi(D,V,t,6,f)
    draw_45(S,"Faro dell'Isola di Pianosa",'Pianosa',P45,B,Pv,-1,'22h00m','22h15m'); S.pt(A,'A','ship'); S.pt(B,'B','ship'); S.pt(C,'C','fix')
    S.line(A,B,'rotta','000°'); S.line(B,C,'rotta2',f'{deg(brg(B,C))}'); return S

@reg
def f5_3_2_5():
    S=FSol('5.3.2-5',lm("Faro dell'Isola di Pianosa"))
    A=S.xy((ll(42,30),10.0)); Pv=62; B,P45,d,V=traverso45(S,A,Pv,"Faro dell'Isola di Pianosa",-1,25); C=S.xy((ll(42,30),ll(10,20)))
    D,t,f=legs_fuel(S,[(A,B),(B,C)],V,6)
    S.passi=['Il traverso B è il piede della perpendicolare dal faro di Pianosa alla rotta 062°.',f'Distanza al traverso {n1(d)} mg in 25 minuti: V = {n1(V)} kn.',f'A-B = {n1(dist(A,B))} mg; B-C = {n1(dist(B,C))} mg.']+fuel_passi(D,V,t,6,f)
    draw_45(S,"Faro dell'Isola di Pianosa",'Pianosa',P45,B,Pv,-1,'09h00m','09h25m'); S.pt(A,'A','ship'); S.pt(B,'B 09h25m','ship'); S.pt(C,'C','fix')
    S.line(A,B,'rotta','062°'); S.line(B,C,'rotta2',f'{deg(brg(B,C))}'); return S

@reg
def f5_3_2_6():
    S=FSol('5.3.2-6',lm('Punta del Diavolo'))
    A=add(S.xy('Punta del Libeccio'),u(225),2.5); T=S.xy((ll(42,20),ll(10,30))); Pv=brg(A,T)
    B,P45,d,V=traverso45(S,A,Pv,'Punta del Diavolo',+1,38)
    D,t,f=legs_fuel(S,[(A,T)],V,10)
    S.passi=[f'A: 2,5 mg a SW di Punta del Libeccio. Rotta A-B: {deg(Pv)}, {n1(D)} mg.',f'Punta del Diavolo al traverso: piede della perpendicolare alla rotta, a {n1(d)} mg.',f'{n1(d)} mg in 38 minuti: V = {n1(V)} kn.']+fuel_passi(D,V,t,10,f)
    draw_45(S,'Punta del Diavolo','P.ta del Diavolo',P45,B,Pv,1,'09h00m','09h38m'); S.pt(S.xy('Punta del Libeccio'),'P.ta del Libeccio','lm'); S.pt(A,'A','ship'); S.pt(T,'B','fix')
    S.line(A,T,'rotta',f'{deg(Pv)}'); return S

@reg
def f5_3_2_7():
    S=FSol('5.3.2-7',lm("Faro di Scoglio d'Africa"))
    A=S.xy((ll(42,34.4),ll(9,58.5))); B=add(S.xy("Faro di Scoglio d'Africa"),u(270),-3.5)
    D,t,f=legs_fuel(S,[(A,B)],6,15)
    S.passi=["B: il faro di Scoglio d'Africa è per Rilv 270° a 3,5 mg, quindi B è 3,5 mg a est del faro.",f'A-B = {n1(D)} mg per {deg(brg(A,B))}.']+fuel_passi(D,6,t,15,f)
    S.pt(S.xy("Faro di Scoglio d'Africa"),"Scoglio d'Africa",'lm'); S.pt(A,'A','ship'); S.pt(B,'B','fix'); S.line(A,B,'rotta',f'{deg(brg(A,B))} · {n1(D)} mg'); S.line(B,S.xy("Faro di Scoglio d'Africa"),'ril2','270° · 3,5 mg')
    return S

@reg
def f5_4_2_1():
    S=FSol('5.4.2-1',lm('Faro di Punta Lividonia'))
    A=add(S.xy("Torre di Capo d'Uomo (Talamone)"),u(0),-1); G=S.xy('Fanali del porto del Giglio'); Pv=brg(A,G)
    B,P45,d,V=traverso45(S,A,Pv,'Faro di Punta Lividonia',-1,1)
    D,t,f=legs_fuel(S,[(A,B)],20,65)
    S.passi=[f"A: la torre di Capo d'Uomo è per Rilv nord a 1 mg, quindi A è 1 mg a sud della torre.",f'Rotta verso Giglio Porto: {deg(Pv)}. Il traverso di Punta Lividonia è il piede della perpendicolare dal faro.',f'A-traverso = {n1(D)} mg a 20 kn.']+fuel_passi(D,20,t,65,f)
    S.pt(S.xy("Torre di Capo d'Uomo (Talamone)"),"T. Capo d'Uomo",'lm'); S.pt(S.xy('Faro di Punta Lividonia'),'P.ta Lividonia','lm'); S.pt(A,'A','ship'); S.pt(B,'traverso','fix'); S.pt(G,'Giglio Porto','lm')
    S.line(A,G,'rotta_l',''); S.line(A,B,'rotta',f'{deg(Pv)} · {n1(D)} mg'); S.line(B,S.xy('Faro di Punta Lividonia'),'ril2','al traverso'); return S

@reg
def f5_4_2_2():
    S=FSol('5.4.2-2',lm('Faro di Formica Grande'))
    P=S.xy('Porto Santo Stefano'); Pv=320; B,P45,d,V=traverso45(S,P,Pv,'Faro di Formica Grande',-1,30)
    D,t,f=legs_fuel(S,[(P,B),(B,P)],V,4)
    S.passi=['Il traverso di Formica Grande è il piede della perpendicolare dal faro alla rotta 320°.',f'Distanza al traverso {n1(d)} mg in 30 minuti: V = {n1(V)} kn.',f'Andata e ritorno: 2 × {n1(dist(P,B))} = {n1(D)} mg.']+fuel_passi(D,V,t,4,f)
    draw_45(S,'Faro di Formica Grande','Formica Grande',P45,B,Pv,-1,'14h00m','14h30m'); S.pt(P,'P. S. Stefano','lm'); S.pt(B,'inversione','fix')
    S.line(P,B,'rotta','320° e ritorno'); return S

@reg
def f5_4_2_3():
    S=FSol('5.4.2-3',lm('Faro di Punta del Fenaio'))
    Li=S.xy('Faro di Punta Lividonia'); Pv=267; B,P45,d,V=traverso45(S,Li,Pv,'Faro di Punta del Fenaio',-1,30); T=S.xy('Porticciolo di Talamone')
    D,t,f=legs_fuel(S,[(Li,B),(B,T)],V,10)
    S.passi=['Punta del Fenaio è a sinistra della rotta 267°: il traverso A è il piede della perpendicolare dal faro.',f'Distanza al traverso {n1(d)} mg in 30 minuti: V = {n1(V)} kn.',f'Lividonia-A = {n1(dist(Li,B))} mg; A-Talamone = {n1(dist(B,T))} mg.']+fuel_passi(D,V,t,10,f)
    draw_45(S,'Faro di Punta del Fenaio','P.ta del Fenaio',P45,B,Pv,-1,'10h00m','10h30m'); S.pt(Li,'P.ta Lividonia','lm'); S.pt(B,'A','ship'); S.pt(T,'Talamone','fix')
    S.line(Li,B,'rotta','267°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

@reg
def f5_4_2_4():
    S=FSol('5.4.2-4',lm('Faro di Punta Lividonia'))
    G=S.xy('Fanali del porto del Giglio'); Pv=42; B,P45,d,V=traverso45(S,G,Pv,'Faro di Punta Lividonia',+1,30); T=S.xy('Formica Piccola')
    D,t,f=legs_fuel(S,[(G,B),(B,T)],V,12)
    S.passi=['Il traverso A è il piede della perpendicolare dal faro di Punta Lividonia alla rotta 042°.',f'Distanza al traverso {n1(d)} mg in 30 minuti: V = {n1(V)} kn.',f'Giglio-A = {n1(dist(G,B))} mg; A-Formica Piccola = {n1(dist(B,T))} mg.']+fuel_passi(D,V,t,12,f)
    draw_45(S,'Faro di Punta Lividonia','P.ta Lividonia',P45,B,Pv,1,'10h00m','10h30m'); S.pt(G,'Giglio Porto','lm'); S.pt(B,'A','ship'); S.pt(T,'Formica Piccola','fix')
    S.line(G,B,'rotta','042°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

@reg
def f5_4_2_5():
    S=FSol('5.4.2-5',lm('Faro di Punta del Fenaio'))
    A=S.xy((ll(42,25.7),ll(11,3.7))); Pv=267; B,P45,d,V=traverso45(S,A,Pv,'Faro di Punta del Fenaio',-1,30,4.2); T=S.xy('Faro di Formica Grande')
    D,t,f=legs_fuel(S,[(A,B),(B,T)],4.2,10)
    S.passi=['Fenaio a ρ −45° e −90°: 4,2 × 30/60 = 2,1 mg al traverso.','B è 2,1 mg dal faro sul rilevamento 177°.',f'A-B = {n1(dist(A,B))} mg; B-Formica Grande = {n1(dist(B,T))} mg.']+fuel_passi(D,4.2,t,10,f)
    draw_45(S,'Faro di Punta del Fenaio','P.ta del Fenaio',P45,B,Pv,-1,'16h30m','17h00m'); S.pt(A,'A','ship'); S.pt(B,'B','ship'); S.pt(T,'Formica Grande','fix')
    S.line(A,B,'rotta','267°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

@reg
def f5_4_2_6():
    S=FSol('5.4.2-6',lm('Faro di Punta del Fenaio'))
    A=S.xy((ll(42,20),ll(10,40))); Pv=61; B,P45,d,V=traverso45(S,A,Pv,'Faro di Punta del Fenaio',+1,30,3.6); T=S.xy('Faro di Formica Grande')
    D,t,f=legs_fuel(S,[(A,B),(B,T)],3.6,10)
    S.passi=['Fenaio a ρ +45° e +90°: 3,6 × 30/60 = 1,8 mg al traverso.','B è 1,8 mg dal faro sul rilevamento 151°.',f'A-B = {n1(dist(A,B))} mg; B-Formica Grande = {n1(dist(B,T))} mg.']+fuel_passi(D,3.6,t,10,f)
    draw_45(S,'Faro di Punta del Fenaio','P.ta del Fenaio',P45,B,Pv,1,'16h30m','17h00m'); S.pt(A,'A','ship'); S.pt(B,'B','ship'); S.pt(T,'Formica Grande','fix')
    S.line(A,B,'rotta','061°'); S.line(B,T,'rotta2',f'{deg(brg(B,T))}'); return S

if __name__=='__main__':
    for fn in SOLS:
        S=fn(); print(S.id, S.res_txt, f'(D {n1(S.D)} mg, t {n1(S.t)} h)', '| ufficiale', S.ex['risposta_ufficiale'], '|', 'OK' if S.check() else 'FUORI')
