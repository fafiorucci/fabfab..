"""Soluzioni degli esercizi di corrente (5.x.1) e di navigazione costiera sulla 42/D (5.5.3-5.8.3)."""
import re, math
from geo import *
from es10 import Sol, deg, hm, intercept, ipassi, draw_intercept, running_fix, draw_running
def n1(v): return f'{v:.1f}'.replace('.',',')
def ll(g,m): return g+m/60
def hhmm(h):
    h=h%24; H=int(h); M=int(round((h-H)*60))
    if M==60: H+=1; M=0
    return f'{H:02d}h{M:02d}m'
def vec(b,v): return (v*u(b)[0], v*u(b)[1])
def mag(v): return math.hypot(*v)
def ang(v): return norm(math.degrees(math.atan2(v[0],v[1])))

class CSol(Sol):
    kind='pos'; carta='5D'
    def check(s):
        r=s.ex['risposta_ufficiale'].replace('\n',' ')
        if s.kind=='pos': return super().check()
        nums=[float(x.replace(',','.')) for x in re.findall(r'(\d+(?:[,.]\d+)?)',r)]
        if s.kind in ('ora','tempo'):
            a=nums[0]+nums[1]/60; b=nums[2]+nums[3]/60; return a-1e-6<=s.val<=b+1e-6
        a,b=nums[0],nums[1]
        if s.kind=='dir':
            if a>b: return s.val>=a-0.5 or s.val<=b+0.5
            return a-0.5<=s.val<=b+0.5
        return a-0.05<=s.val<=b+0.05
    def done(s,val,txt): s.val=val; s.res_txt=txt; return s

# ---------- strumenti ----------
def ship_from(S,L,rilv,d):
    """la nave vede il punto L per rilv a d miglia"""
    return add(S.xy(L),u(rilv),-d)
def fix2(S,L1,r1,L2,r2): return cross_lines(S.xy(L1),r1,S.xy(L2),r2)
def pv_for(rv,vp,dc,vc):
    cp=vc*math.sin(math.radians(dc-rv)); a=math.degrees(math.asin(-cp/vp)); pv=norm(rv+a)
    ve=vp*math.cos(math.radians(a))+vc*math.cos(math.radians(dc-rv)); return pv,ve
def water_for(G,C):
    W=sub(G,C); return mag(W),ang(W)
def draw_tri(S,A,pv,vp,dc,vc,scale=1.0):
    """triangolo delle velocità in un'ora a partire da A"""
    P=add(A,vec(pv,vp*scale)); Q=add(P,vec(dc,vc*scale))
    S.line(A,P,'rotta_l',f'Pv {deg(pv)} · {n1(vp)} kn'); S.line(P,Q,'corr',f'corrente {deg(dc)} · {n1(vc)} kn')
    return Q
def lm_pt(S,n,sh): S.pt(S.xy(n),sh,'lm')

SOLS={13:[],14:[],15:[]}
def reg(les):
    def d(f): SOLS[les].append(f); return f
    return d

# ======================= LEZIONE 13: 5.1.1, 5.2.1, 5.3.1 =======================
@reg(13)
def c5_1_1_1():
    S=CSol('5.1.1-1',lm('Capo della Vita')); S.kind='vel'
    A=S.xy((ll(42,51),ll(10,16.9))); B=ship_from(S,'Capo della Vita',127,2.9); G=sub(B,A); G=(G[0]/0.5,G[1]/0.5); C=vec(180,2); vp,pv=water_for(G,C)
    S.passi=['B: il monumento si vede per 127° a 2,9 mg, quindi B è 2,9 mg per 307° dal monumento.',f'A-B = {n1(dist(A,B))} mg in 30 minuti: la velocità sul fondo deve essere {n1(mag(G))} kn per {deg(ang(G))}.',
             'Triangolo: dalla velocità sul fondo togli la corrente (180°, 2 kn): il vettore che resta è la velocità propria.',f'Vp = {n1(vp)} kn, con prora {deg(pv)}.']
    lm_pt(S,'Capo della Vita','Capo della Vita'); S.pt(A,'A','ship'); S.line(A,B,'rotta',f'Rv {deg(ang(G))}'); S.line(S.xy('Capo della Vita'),B,'ril2','2,9 mg')
    S.line(A,add(A,vec(pv,vp*0.5)),'rotta_l',f'Pv {deg(pv)}'); S.line(add(A,vec(pv,vp*0.5)),B,'corr','corrente in 30′'); S.fix(B,'B')
    return S.done(vp,f'Vp {n1(vp)} kn')

@reg(13)
def c5_1_1_2():
    S=CSol('5.1.1-2',lm('Faro di Punta Polveraia')); S.kind='dir'
    A=ship_from(S,'Faro di Punta Polveraia',112,1.8); t=48/60; St=add(A,vec(350,8.5*t)); B=S.xy((ll(42,53),10.0)); dc=brg(St,B)
    S.passi=['A: Polveraia per 112° a 1,8 mg, cioè 1,8 mg per 292° dal faro.',f'Punto stimato alle 09h18m: {n1(8.5*t)} mg per 350° (48 minuti a 8,5 kn).','La corrente va dal punto stimato al punto osservato B.',f'Dc = {deg(dc)}; Vc = {n1(dist(St,B))} mg in 48′ = {n1(dist(St,B)/t)} kn.']
    lm_pt(S,'Faro di Punta Polveraia','Punta Polveraia'); S.pt(A,'A 08h30m','ship'); S.line(A,St,'stima','350° · stimato'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.line(A,B,'rotta','moto effettivo'); S.fix(B,'B 09h18m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(13)
def c5_1_1_3():
    S=CSol('5.1.1-3',lm('Faro dello Scoglietto')); S.kind='tempo'
    Pf=S.xy('Faro di Portoferraio'); Sc=S.xy('Faro dello Scoglietto'); O=add(Sc,u(brg(Pf,Sc)),3); dc=45; vc=2.5/1.25; Sa=S.xy('Porticciolo di Salivoli')
    rv=brg(O,Sa); pv,ve=pv_for(rv,5,dc,vc); D_=dist(O,Sa); t=D_/ve
    S.passi=[f'Punto nave: sull\'allineamento Portoferraio-Scoglietto, 3 mg oltre lo Scoglietto.','Lo stimato è 2,5 mg a SW del calcolato: la corrente va verso NE (045°) e in 1h15m ha fatto 2,5 mg: Vc = 2 kn.',
             f'Rotta per Salivoli {deg(rv)}, {n1(D_)} mg. Con Vp 5 kn e la corrente: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Tempo = {n1(D_)} / {n1(ve)} = {hm(t*60)}.']
    lm_pt(S,'Faro di Portoferraio','Portoferraio'); lm_pt(S,'Faro dello Scoglietto','Scoglietto'); S.line(Pf,O,'rotta_l',''); S.pt(O,'punto nave','ship')
    S.line(add(O,u(225),2.5),O,'corr','045° · 2,5 mg'); S.line(O,Sa,'rotta',f'Rv {deg(rv)} · {n1(D_)} mg'); S.fix(Sa,'Salivoli')
    return S.done(t,f'{hm(t*60)}')

@reg(13)
def c5_1_1_4():
    S=CSol('5.1.1-4',lm('Faro di Capo Poro')); S.kind='dir'
    A=S.xy((ll(42,41),ll(10,28.4))); t=70/60; St=add(A,vec(260,6.5*t)); B=fix2(S,'Punta Morcone',35,'Faro di Capo Poro',310); dc=brg(St,B)
    S.passi=[f'Stimato alle 09h40m: {n1(6.5*t)} mg per 260° (1h10m a 6,5 kn).','Osservato B: Punta Morcone per 035° e Capo Poro per 310°.',f'Dallo stimato all\'osservato: Dc = {deg(dc)}, {n1(dist(St,B))} mg in 1h10m (Vc {n1(dist(St,B)/t)} kn).']
    S.pt(A,'A','ship'); lm_pt(S,'Punta Morcone','P.ta Morcone'); lm_pt(S,'Faro di Capo Poro','Capo Poro'); S.line(A,St,'stima','260°'); S.pt(St,'stimato','ship')
    S.line(B,S.xy('Punta Morcone'),'ril','035°'); S.line(B,S.xy('Faro di Capo Poro'),'ril','310°'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 09h40m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(13)
def c5_1_1_5():
    S=CSol('5.1.1-5',lm('Faro di Punta Polveraia')); S.kind='dir'
    A=S.xy((ll(42,50),10.0)); F=S.xy('Punta Falcone'); St=add(A,sub(F,A),1.5/3.5); B=fix2(S,'Traliccio di Monte Poppe',130,'Faro di Punta Polveraia',203); dc=brg(St,B)
    S.passi=[f'Da A a Punta Falcone: {n1(dist(A,F))} mg in 3h30m. Alle 09h30m (1h30m) lo stimato è ai 3/7 della rotta.','Osservato B: Monte Poppe per 130° e Polveraia per 203°.',f'Dallo stimato all\'osservato: Dc = {deg(dc)} ({n1(dist(St,B))} mg in 1h30m).']
    S.pt(A,'A 08h00m','ship'); S.pt(F,'P.ta Falcone','lm'); lm_pt(S,'Traliccio di Monte Poppe','M. Poppe'); lm_pt(S,'Faro di Punta Polveraia','Polveraia')
    S.line(A,F,'rotta_l',''); S.pt(St,'stimato','ship'); S.line(B,S.xy('Traliccio di Monte Poppe'),'ril','130°'); S.line(B,S.xy('Faro di Punta Polveraia'),'ril','203°'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 09h30m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(13)
def c5_1_1_6():
    S=CSol('5.1.1-6',lm('Punta di Fetovaia')); S.kind='ora'
    A=S.xy((ll(42,39),ll(10,12.7))); F=S.xy('Punta di Fetovaia'); rv=brg(A,F); pv,ve=pv_for(rv,4,270,2); t=dist(A,F)/ve
    S.passi=[f'Rotta per Fetovaia: {deg(rv)}, {n1(dist(A,F))} mg.',f'Triangolo con Vp 4 kn e corrente 270°/2 kn: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Tempo {n1(dist(A,F))} / {n1(ve)} = {hm(t*60)}: arrivo alle {hhmm(10+t)}.']
    S.pt(A,'A 10h00m','ship'); S.line(A,F,'rotta',f'Rv {deg(rv)}'); draw_tri(S,A,pv,4,270,2); S.fix(F,'Fetovaia')
    return S.done(10+t,f'arrivo {hhmm(10+t)}')

@reg(13)
def c5_2_1_1():
    S=CSol('5.2.1-1',lm('Scoglio dello Sparviero'))
    A=S.xy('Scoglio dello Sparviero'); B=add(add(A,vec(160,12)),vec(315,4))
    S.passi=['V = −3°: Pv = 160°.','In 2 ore: 12 mg per 160° (moto proprio) e 4 mg per 315° (corrente verso NW).','Il punto nave delle 11h00m è la punta del secondo vettore.']
    S.pt(A,'Sparviero','lm'); P=add(A,vec(160,12)); S.line(A,P,'stima','160° · 12 mg'); S.line(P,B,'corr','315° · 4 mg'); S.line(A,B,'rotta',f'Rv {deg(brg(A,B))}'); S.fix(B,'B 11h00m')
    return S

@reg(13)
def c5_2_1_2():
    S=CSol('5.2.1-2',lm('Fanali di Castiglione della Pescaia')); S.kind='ora'
    A=S.xy((ll(42,40),ll(10,40))); F=S.xy('Fanali di Castiglione della Pescaia'); rv=brg(A,F); pv,ve=pv_for(rv,6,59,2); t=dist(A,F)/ve
    S.passi=[f'Rotta per Castiglione: {deg(rv)}, {n1(dist(A,F))} mg.',f'Con Vp 6 kn e corrente 059°/2 kn: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Tempo {hm(t*60)}: arrivo alle {hhmm(10+t)}.']
    S.pt(A,'A 10h00m','ship'); S.line(A,F,'rotta',f'Rv {deg(rv)}'); draw_tri(S,A,pv,6,59,2); S.fix(F,'Castiglione')
    return S.done(10+t,f'arrivo {hhmm(10+t)}')

@reg(13)
def c5_2_1_3():
    S=CSol('5.2.1-3',lm('Fanale di Carbonifera')); S.kind='dir'
    A=S.xy((ll(42,44.9),ll(10,40))); T=S.xy('Fanale di Carbonifera'); G=sub(T,A); G=(G[0]/2,G[1]/2); vp,pv=water_for(G,vec(220,1.5)); pb=pv-2+3
    S.passi=[f'Da A alla Carbonifera: {n1(dist(A,T))} mg in 2 ore, sul fondo {n1(mag(G))} kn per {deg(ang(G))}.','Togli la corrente (220°, 1,5 kn): resta la velocità propria.',f'Pv = {deg(pv)} (Vp {n1(vp)} kn). V = +2° −3° = −1°: Pb = Pv − V = {deg(pb)}.']
    S.pt(A,'A','ship'); S.line(A,T,'rotta',f'Rv {deg(ang(G))}'); P=add(A,vec(pv,vp)); S.line(A,P,'rotta_l',f'Pv {deg(pv)}'); S.line(P,add(A,G),'corr','220° · 1,5 kn'); S.fix(T,'Carbonifera')
    return S.done(norm(pb),f'Pb {deg(pb)}')

@reg(13)
def c5_2_1_4():
    S=CSol('5.2.1-4',lm('Scoglio dello Sparviero')); S.kind='ora'
    A=add(S.xy('Serbatoio di Marina di Grosseto'),u(225),4); rv=302; pv,ve=pv_for(rv,8,90,2); L=S.xy('Scoglio dello Sparviero')
    side=1 if ((u(rv)[0]*(L[1]-A[1])-u(rv)[1]*(L[0]-A[0]))<0) else -1
    T=cross_lines(A,rv,L,pv+side*90); t=dist(A,T)/ve
    S.passi=['A: 4 mg a SW del serbatoio di Marina di Grosseto.',f'Rv 302°, Vp 8 kn, corrente verso est 2 kn: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Il traverso si misura dalla prora: Sparviero per {deg(pv+side*90)}; l\'incrocio con la rotta è a {n1(dist(A,T))} mg.',f'{hm(t*60)} dopo le 11h00m: traverso alle {hhmm(11+t)}.']
    lm_pt(S,'Serbatoio di Marina di Grosseto','Serbatoio'); lm_pt(S,'Scoglio dello Sparviero','Sparviero'); S.pt(A,'A 11h00m','ship'); S.line(A,T,'rotta','Rv 302°'); S.line(T,L,'ril2',f'{deg(pv+side*90)}'); S.fix(T,hhmm(11+t))
    return S.done(11+t,f'traverso alle {hhmm(11+t)}')

@reg(13)
def c5_2_1_5():
    S=CSol('5.2.1-5',lm('Faro di Punta Ala')); S.kind='dir'
    A=S.xy((ll(42,50),ll(10,38.5))); St=add(A,vec(141,9)); B=fix2(S,'Fanali di Castiglione della Pescaia',80,'Faro di Punta Ala',330); dc=brg(St,B)
    S.passi=['Stimato alle 11h30m: 9 mg per 141° (1h30m a 6 kn).','Osservato B: Castiglione per 080° e Punta Ala per 330°.',f'Dallo stimato all\'osservato: Dc = {deg(dc)} ({n1(dist(St,B))} mg in 1h30m).']
    S.pt(A,'A 10h00m','ship'); lm_pt(S,'Fanali di Castiglione della Pescaia','Castiglione'); lm_pt(S,'Faro di Punta Ala','Punta Ala'); S.line(A,St,'stima','141° · 9 mg'); S.pt(St,'stimato','ship')
    S.line(B,S.xy('Fanali di Castiglione della Pescaia'),'ril','080°'); S.line(B,S.xy('Faro di Punta Ala'),'ril','330°'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 11h30m')
    S.note='La deriva è breve (circa 1,9 mg): uno spostamento di pochi decimi di miglio del punto B cambia la Dc di qualche grado. La risposta ufficiale è 359°÷005°, noi troviamo 009°.'
    return S.done(dc,f'Dc {deg(dc)}')

@reg(13)
def c5_3_1_1():
    S=CSol('5.3.1-1',lm('Punta Brigantina')); S.kind='vel'
    A=fix2(S,'Punta Brigantina',22,'Torre di Cala della Ruta',323); St=add(A,vec(202,8)); B=S.xy((ll(42,24.1),10.0)); vc=dist(St,B)/0.5
    S.passi=['A: Punta Brigantina per 022° e torre di Cala della Ruta per 323°.','Stimato alle 13h12m: 8 mg per 202° (30 minuti a 16 kn).',f'Dallo stimato all\'osservato: {n1(dist(St,B))} mg in 30 minuti, Vc = {n1(vc)} kn (Dc {deg(brg(St,B))}).']
    lm_pt(S,'Punta Brigantina','P.ta Brigantina'); lm_pt(S,'Torre di Cala della Ruta','T. Cala della Ruta'); S.pt(A,'A 12h42m','ship'); S.line(A,St,'stima','202° · 8 mg'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'{n1(dist(St,B))} mg'); S.fix(B,'B 13h12m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(13)
def c5_3_1_2():
    S=CSol('5.3.1-2',lm('Punta Brigantina')); S.kind='dir'
    A=ship_from(S,"Faro di Scoglio d'Africa",225,3); Br=S.xy('Punta Brigantina'); pv=brg(A,Br); St=add(A,vec(pv,5)); B=ship_from(S,'Punta Brigantina',339,4.5); dc=brg(St,B)
    S.passi=["A: Scoglio d'Africa per SW a 3 mg, quindi A è 3 mg a NE del faro.",f'Prora verso Punta Brigantina: {deg(pv)}. Stimato alle 17h00m: 5 mg (50 minuti a 6 kn).','B: Brigantina per 339° a 4,5 mg.',f'Dallo stimato all\'osservato: Dc = {deg(dc)}.']
    lm_pt(S,"Faro di Scoglio d'Africa","Scoglio d'Africa"); lm_pt(S,'Punta Brigantina','P.ta Brigantina'); S.pt(A,'A 16h10m','ship'); S.line(A,St,'stima',f'{deg(pv)} · 5 mg'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.line(B,Br,'ril2','339° · 4,5 mg'); S.fix(B,'B 17h00m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(13)
def c5_3_1_3():
    S=CSol('5.3.1-3',lm("Faro di Scoglio d'Africa")); S.kind='dir'
    A=ship_from(S,"Faro di Scoglio d'Africa",310,3.3); t=102/60; St=add(A,vec(356,7*t)); B=S.xy((ll(42,32.9),ll(10,6))); dc=brg(St,B)
    S.passi=["A: Scoglio d'Africa per 310° a 3,3 mg (A è a SE del faro).",f'Dalle 23h40m alle 01h22m: 1h42m, cioè {n1(7*t)} mg per 356°.',f'Dallo stimato al GPS: Dc = {deg(dc)} ({n1(dist(St,B))} mg).']
    lm_pt(S,"Faro di Scoglio d'Africa","Scoglio d'Africa"); S.pt(A,'A 23h40m','ship'); S.line(A,St,'stima',f'356° · {n1(7*t)} mg'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 01h22m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(13)
def c5_3_1_4():
    S=CSol('5.3.1-4',lm("Faro di Scoglio d'Africa")); S.kind='vel'
    A=ship_from(S,"Faro di Scoglio d'Africa",238,3); t=130/60; St=add(A,vec(35,3.5*t)); B=S.xy((ll(42,31.5),ll(10,15.3))); vc=dist(St,B)/t
    S.passi=["A: Scoglio d'Africa per 238° a 3 mg (A è a NE del faro).",f'Dalle 00h20m alle 02h30m: 2h10m, {n1(3.5*t)} mg per 035°.',f'Dallo stimato al GPS: {n1(dist(St,B))} mg in 2h10m, Vc = {n1(vc)} kn.']
    lm_pt(S,"Faro di Scoglio d'Africa","Scoglio d'Africa"); S.pt(A,'A 00h20m','ship'); S.line(A,St,'stima','035°'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'{n1(dist(St,B))} mg'); S.fix(B,'B 02h30m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(13)
def c5_3_1_5():
    S=CSol('5.3.1-5',(42.53,10.36)); S.kind='vel'
    A=S.xy((ll(42,30),ll(10,18.5))); B=S.xy((ll(42,34.2),ll(10,25))); G=sub(B,A); G=(G[0]/0.5,G[1]/0.5); vp,pv=water_for(G,vec(0,4))
    S.passi=[f'A-B = {n1(dist(A,B))} mg in 30 minuti: sul fondo {n1(mag(G))} kn per {deg(ang(G))}.','Togli la corrente (nord, 4 kn): resta la velocità propria.',f'Vp = {n1(vp)} kn con prora {deg(pv)}.']
    S.pt(A,'A','ship'); S.line(A,B,'rotta',f'Rv {deg(ang(G))}'); P=add(A,vec(pv,vp*0.5)); S.line(A,P,'rotta_l',f'Pv {deg(pv)}'); S.line(P,B,'corr','nord · 2 mg'); S.fix(B,'B')
    return S.done(vp,f'Vp {n1(vp)} kn')

@reg(13)
def c5_3_1_6():
    S=CSol('5.3.1-6',(42.54,10.16)); S.kind='vel'
    A=S.xy((ll(42,33.4),ll(10,12.8))); vp,pv=water_for(vec(253,5),vec(190,1))
    S.passi=['Velocità sul fondo: 5 kn per 253°.','Togli la corrente (190°, 1 kn).',f'Vp = {n1(vp)} kn con prora {deg(pv)}.']
    S.pt(A,'A','ship'); E=add(A,vec(253,5)); S.line(A,E,'rotta','Rv 253° · 5 kn'); P=add(A,vec(pv,vp)); S.line(A,P,'rotta_l',f'Pv {deg(pv)}'); S.line(P,E,'corr','190° · 1 kn'); S.fix(E,'1 ora')
    return S.done(vp,f'Vp {n1(vp)} kn')

@reg(13)
def c5_3_1_7():
    S=CSol('5.3.1-7',(42.44,10.3)); S.kind='dir'
    A=S.xy((ll(42,25),ll(10,14.6))); E=add(add(A,vec(55,6)),vec(0,1.5)); rv=brg(A,E)
    S.passi=['In un\'ora: 6 mg per 055° (moto proprio) più 1,5 mg verso nord (corrente).',f'La congiungente A-punta è la rotta vera: Rv = {deg(rv)}, Ve {n1(dist(A,E))} kn.']
    S.pt(A,'A','ship'); draw_tri(S,A,55,6,0,1.5); S.line(A,E,'rotta',f'Rv {deg(rv)}'); S.fix(E,'1 ora')
    return S.done(rv,f'Rv {deg(rv)}')

@reg(13)
def c5_3_1_8():
    S=CSol('5.3.1-8',lm("Faro dell'Isola di Pianosa")); S.kind='vel'
    A=S.xy((ll(42,30),ll(10,20))); t=100/60; St=add(A,vec(263,6*t)); B=fix2(S,"Faro dell'Isola di Pianosa",345,"Faro di Scoglio d'Africa",210); vc=dist(St,B)/t
    S.passi=[f'Stimato alle 10h40m: {n1(6*t)} mg per 263° (1h40m a 6 kn).',"Osservato B: Pianosa per 345°, Scoglio d'Africa per 210°.",f'{n1(dist(St,B))} mg in 1h40m: Vc = {n1(vc)} kn.']
    S.pt(A,'A 09h00m','ship'); lm_pt(S,"Faro dell'Isola di Pianosa",'Pianosa'); lm_pt(S,"Faro di Scoglio d'Africa","Scoglio d'Africa"); S.line(A,St,'stima','263°'); S.pt(St,'stimato','ship')
    S.line(B,S.xy("Faro dell'Isola di Pianosa"),'ril','345°'); S.line(B,S.xy("Faro di Scoglio d'Africa"),'ril','210°'); S.line(St,B,'corr',f'{n1(dist(St,B))} mg'); S.fix(B,'B 10h40m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(13)
def c5_3_1_9():
    S=CSol('5.3.1-9',lm("Faro di Scoglio d'Africa")); S.kind='vel'
    A=S.xy("Faro di Scoglio d'Africa"); E=add(add(A,vec(14,11)),vec(140,2)); ve=dist(A,E)
    S.passi=['In un\'ora: 11 mg per 014° più 2 mg per 140°.',f'La somma dei vettori è la velocità effettiva: Ve = {n1(ve)} kn (Rv {deg(brg(A,E))}).']
    S.pt(A,"Scoglio d'Africa",'lm'); draw_tri(S,A,14,11,140,2); S.line(A,E,'rotta',f'Ve {n1(ve)} kn'); S.fix(E,'1 ora')
    return S.done(ve,f'Ve {n1(ve)} kn')

@reg(13)
def c5_3_1_10():
    S=CSol('5.3.1-10',lm("Faro dell'Isola di Pianosa")); S.kind='dir'
    A=add(S.xy("Faro dell'Isola di Pianosa"),vec(246,3.2)); B=S.xy((ll(42,23.3),ll(10,5.9))); rv=brg(A,B); pv,ve=pv_for(rv,4.8,280,1.5)
    S.passi=['A: 3,2 mg per 246° dal faro di Pianosa (A è a WSW del faro, come nella soluzione ufficiale).',f'Rotta A-B: {deg(rv)}.','Triangolo: da A la corrente (280°, 1,5 mg); dalla punta il compasso aperto di 4,8 mg taglia la rotta.',f'Pv = {deg(pv)}, Ve {n1(ve)} kn.']
    lm_pt(S,"Faro dell'Isola di Pianosa",'Pianosa'); S.pt(A,'A 13h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); C1=add(A,vec(280,1.5)); S.line(A,C1,'corr','280° · 1,5'); S.line(C1,add(A,vec(rv,ve)),'rotta_l',f'Pv {deg(pv)}'); S.fix(B,'B')
    return S.done(pv,f'Pv {deg(pv)}')

# ======================= LEZIONE 14: 5.4.1 =======================
@reg(14)
def c5_4_1_1():
    S=CSol('5.4.1-1',lm('Faro di Punta del Fenaio')); S.kind='dir'
    A=fix2(S,'Torre di Punta Avoltore',30,'Torre di Punta di Torre Ciana',321); B=add(S.xy('Faro di Punta del Fenaio'),u(0),3); G=sub(B,A); G=(G[0]/1.5,G[1]/1.5); vp,pv=water_for(G,vec(158,2))
    S.passi=['A: torre di Punta Avoltore per 030° e torre di Torre Ciana per 321°.','B: 3 mg a nord del faro di Punta del Fenaio.',f'Da A a B {n1(dist(A,B))} mg in 1h30m: sul fondo {n1(mag(G))} kn per {deg(ang(G))}.',f'Togli la corrente (158°, 2 kn): Pv = {deg(pv)}, Vp {n1(vp)} kn.']
    lm_pt(S,'Torre di Punta Avoltore','T. Avoltore'); lm_pt(S,'Torre di Punta di Torre Ciana','T. Ciana'); lm_pt(S,'Faro di Punta del Fenaio','P.ta del Fenaio')
    S.pt(A,'A 09h30m','ship'); S.line(A,B,'rotta',f'Rv {deg(ang(G))}'); P=add(A,vec(pv,vp)); S.line(A,P,'rotta_l',f'Pv {deg(pv)}'); S.line(P,add(A,G),'corr','158° · 2'); S.fix(B,'B 11h00m')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(14)
def c5_4_1_2():
    S=CSol('5.4.1-2',lm('Faro di Talamone')); S.kind='ora'
    A=S.xy((ll(42,23.2),ll(10,56.8))); B=ship_from(S,'Faro di Talamone',305,0.5); rv=brg(A,B); pv,ve=pv_for(rv,7,75,3); t=dist(A,B)/ve
    S.passi=['B: Talamone per 305° a 0,5 mg (B è a SE del faro).',f'Rotta A-B {deg(rv)}, {n1(dist(A,B))} mg.',f'Triangolo con Vp 7 e corrente 075°/3 kn: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Tempo {hm(t*60)}: arrivo alle {hhmm(9.75+t)}.']
    lm_pt(S,'Faro di Talamone','Talamone'); S.pt(A,'A 09h45m','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); draw_tri(S,A,pv,7,75,3); S.fix(B,'B')
    return S.done(9.75+t,f'arrivo {hhmm(9.75+t)}')

@reg(14)
def c5_4_1_3():
    S=CSol('5.4.1-3',lm('Faro di Punta Lividonia')); S.kind='vel'
    A=ship_from(S,'Faro di Punta Lividonia',180,2.2); St=add(A,vec(292,9)); B=S.xy((ll(42,32.4),ll(10,57))); vc=dist(St,B)/1.5
    S.passi=['A: Lividonia per sud a 2,2 mg, quindi A è 2,2 mg a nord del faro.','Stimato alle 13h00m: 9 mg per 292° (1h30m a 6 kn).',f'Dallo stimato al GPS: {n1(dist(St,B))} mg in 1h30m, Vc = {n1(vc)} kn.']
    lm_pt(S,'Faro di Punta Lividonia','P.ta Lividonia'); S.pt(A,'A 11h30m','ship'); S.line(A,St,'stima','292° · 9 mg'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'{n1(dist(St,B))} mg'); S.fix(B,'B 13h00m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(14)
def c5_4_1_4():
    S=CSol('5.4.1-4',lm('Faro di Punta del Fenaio')); S.kind='dir'
    C=fix2(S,'Faro di Punta del Fenaio',192,'Faro di Punta Lividonia',104); Fe=S.xy('Faro di Punta del Fenaio')
    # A sulla linea del rilevamento 119° del faro, alla batimetrica dei 200 m (vedi note)
    best=None
    for k in range(10,60):
        d=k/10; A=add(Fe,u(119),-d); rv=brg(A,C)
        if best is None or abs(rv-58)<abs(best[1]-58): best=(A,rv,d)
    A,rv,d=best
    S.passi=['Declinazione 2000: 0°30′ + 6 × 7′ = 1°12′E, circa +1°; δ = −4°: V = −3°.','C: Fenaio per Rilb 195° = Rilv 192°, Lividonia per Rilb 107° = Rilv 104°.',f'A: sul rilevamento 119° del Fenaio, alla batimetrica dei 200 m (circa {n1(d)} mg dal faro).',f'La rotta vera è la congiungente A-C: Rv {deg(rv)}.']
    lm_pt(S,'Faro di Punta del Fenaio','P.ta del Fenaio'); lm_pt(S,'Faro di Punta Lividonia','P.ta Lividonia'); S.pt(A,'A 19h40m','ship'); S.line(A,C,'rotta',f'Rv {deg(rv)}')
    S.line(C,Fe,'ril','192°'); S.line(C,S.xy('Faro di Punta Lividonia'),'ril','104°'); S.fix(C,'C 21h00m'); S.note='La batimetrica dei 200 m non è nei nostri dati: la distanza di A dal faro va letta sulla carta.'
    return S.done(rv,f'Rv {deg(rv)}')

@reg(14)
def c5_4_1_5():
    S=CSol('5.4.1-5',lm('Faro di Talamone')); S.kind='dir'
    A=fix2(S,'Faro di Talamone',47,'Faro di Punta Lividonia',152); t=72/60; St=add(A,vec(243,5*t)); B=S.xy((ll(42,26.2),ll(10,58.8))); dc=brg(St,B)
    S.passi=['A: Talamone per 047° e Lividonia per 152°.',f'Stimato alle 13h30m: {n1(5*t)} mg per 243° (1h12m a 5 kn).',f'Dallo stimato al GPS: Dc = {deg(dc)}.']
    lm_pt(S,'Faro di Talamone','Talamone'); lm_pt(S,'Faro di Punta Lividonia','P.ta Lividonia'); S.pt(A,'A 12h18m','ship'); S.line(A,St,'stima','243°'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 13h30m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(14)
def c5_4_1_6():
    S=CSol('5.4.1-6',lm('Faro di Formica Grande')); S.kind='ora'
    A=S.xy((ll(42,32.4),ll(10,57))); B=ship_from(S,'Faro di Formica Grande',90,4.6); rv=brg(A,B); pv,ve=pv_for(rv,6,48,2.2); t=dist(A,B)/ve
    S.passi=['B: Formica Grande per est a 4,6 mg, cioè 4,6 mg a ovest del faro.',f'Rotta A-B {deg(rv)}, {n1(dist(A,B))} mg.',f'Con Vp 6 e corrente 048°/2,2 kn: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Tempo {hm(t*60)}: arrivo alle {hhmm(13+t)}.']
    lm_pt(S,'Faro di Formica Grande','Formica Grande'); S.pt(A,'A 13h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); draw_tri(S,A,pv,6,48,2.2); S.fix(B,'B')
    return S.done(13+t,f'arrivo {hhmm(13+t)}')

@reg(14)
def c5_4_1_7():
    S=CSol('5.4.1-7',lm('Faro di Punta del Fenaio')); S.kind='ora'
    A=ship_from(S,'Faro di Formica Grande',124,2.4); B=ship_from(S,'Faro di Punta del Fenaio',153,1); rv=brg(A,B); pv,ve=pv_for(rv,10,48,2.2); t=dist(A,B)/ve
    S.passi=['A: Formica Grande per 124° a 2,4 mg; B: Fenaio per 153° a 1 mg.',f'Rotta A-B {deg(rv)}, {n1(dist(A,B))} mg.',f'Con Vp 10 e corrente 048°/2,2 kn: Pv {deg(pv)}, Ve {n1(ve)} kn.',f'Tempo {hm(t*60)}: arrivo alle {hhmm(12+t)}.']
    lm_pt(S,'Faro di Formica Grande','Formica Grande'); lm_pt(S,'Faro di Punta del Fenaio','P.ta del Fenaio'); S.pt(A,'A 12h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); draw_tri(S,A,pv,10,48,2.2); S.fix(B,'B')
    return S.done(12+t,f'arrivo {hhmm(12+t)}')

@reg(14)
def c5_4_1_8():
    S=CSol('5.4.1-8',lm('Faro di Formica Grande')); S.kind='dir'
    A=ship_from(S,'Faro di Formica Grande',333,2.1); E=add(add(A,vec(68,8)),vec(180,3.2)); rv=brg(A,E)
    S.passi=['A: Formica Grande per 333° a 2,1 mg.','In un\'ora: 8 mg per 068° più 3,2 mg verso sud.',f'Rv = {deg(rv)} (Ve {n1(dist(A,E))} kn). Gli altri dati della traccia non servono per la rotta.']
    lm_pt(S,'Faro di Formica Grande','Formica Grande'); S.pt(A,'A 16h45m','ship'); draw_tri(S,A,68,8,180,3.2); S.line(A,E,'rotta',f'Rv {deg(rv)}'); S.fix(E,'1 ora')
    return S.done(rv,f'Rv {deg(rv)}')

@reg(14)
def c5_4_1_9():
    S=CSol('5.4.1-9',lm('Porticciolo di Talamone')); S.kind='vel'
    A=S.xy((ll(42,25.5),ll(10,51.1))); Bs=S.xy((ll(42,26.6),ll(10,47.3))); C=((A[0]-Bs[0])/2,(A[1]-Bs[1])/2); T=S.xy('Porticciolo di Talamone')
    G=sub(T,A); G=(G[0]/3,G[1]/3); vp,pv=water_for(G,C)
    S.passi=[f'La corrente ha portato la barca dallo stimato al GPS in 2 ore: Dc {deg(ang(C))}, Vc {n1(mag(C))} kn.',f'Da A a Talamone: {n1(dist(A,T))} mg in 3 ore, sul fondo {n1(mag(G))} kn per {deg(ang(G))}.',f'Togli la corrente: Vp = {n1(vp)} kn (Pv {deg(pv)}).']
    S.pt(Bs,'stimato','ship'); S.line(Bs,A,'corr','2 ore'); S.pt(A,'A 12h00m','ship'); S.line(A,T,'rotta',f'Rv {deg(ang(G))}'); S.fix(T,'Talamone')
    return S.done(vp,f'Vp {n1(vp)} kn')

@reg(14)
def c5_4_1_10():
    S=CSol('5.4.1-10',lm('Faro di Punta del Fenaio')); S.kind='vel'
    A=fix2(S,'Faro di Talamone',53,'Faro di Punta Lividonia',150); St=add(A,vec(230,7.5)); B=ship_from(S,'Faro di Punta del Fenaio',200,3.5); vc=dist(St,B)/0.75
    S.passi=['A: Talamone per 053° e Lividonia per 150°.','Stimato dopo 45 minuti: 7,5 mg per 230°.','B: Fenaio a sinistra per ρ 30°: Rilv = 230° − 30° = 200°, a 3,5 mg.',f'Dallo stimato a B: {n1(dist(St,B))} mg in 45 minuti, Vc = {n1(vc)} kn.']
    lm_pt(S,'Faro di Talamone','Talamone'); lm_pt(S,'Faro di Punta Lividonia','P.ta Lividonia'); lm_pt(S,'Faro di Punta del Fenaio','P.ta del Fenaio'); S.pt(A,'A 10h00m','ship'); S.line(A,St,'stima','230° · 7,5 mg'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'{n1(dist(St,B))} mg'); S.line(B,S.xy('Faro di Punta del Fenaio'),'ril2','200° · 3,5 mg'); S.fix(B,'B 10h45m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(14)
def c5_4_1_11():
    S=CSol('5.4.1-11',(42.55,11.02)); S.kind='dir'
    A=S.xy((ll(42,30.6),ll(11,6.4))); pv,ve=pv_for(300,7.2,180,2)
    S.passi=['Rotta 300°, Vp 7,2 kn, corrente verso sud 2 kn.','Triangolo: da A la corrente (2 mg per 180°); dalla punta il compasso di 7,2 mg taglia la rotta.',f'Pv = {deg(pv)} (Ve {n1(ve)} kn): la prora va verso nord per compensare.']
    S.pt(A,'A 10h00m','ship'); E=add(A,vec(300,ve)); S.line(A,E,'rotta','Rv 300°'); C1=add(A,vec(180,2)); S.line(A,C1,'corr','180° · 2'); S.line(C1,E,'rotta_l',f'Pv {deg(pv)}')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(14)
def c5_4_1_12():
    S=CSol('5.4.1-12',(42.39,10.95)); S.kind='dir'
    A=S.xy((ll(42,24.3),ll(10,55.1))); B=S.xy((ll(42,21.6),ll(10,59.4))); rv=brg(A,B); pv,ve=pv_for(rv,7,0,1.5)
    S.passi=[f'Rotta A-B: {deg(rv)}.','Corrente verso nord 1,5 kn, Vp 7 kn.',f'Pv = {deg(pv)} (Ve {n1(ve)} kn).']
    S.pt(A,'A','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); C1=add(A,vec(0,1.5*0.5)); S.line(A,C1,'corr','nord'); S.line(C1,add(A,vec(rv,ve*0.5)),'rotta_l',f'Pv {deg(pv)}'); S.fix(B,'B')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(14)
def c5_4_1_13():
    S=CSol('5.4.1-13',lm('Faro di Formica Grande')); S.kind='dir'
    Cf=S.xy('Torre di Cala di Forno'); Fg=S.xy('Faro di Formica Grande'); A=cross_lines(Fg,brg(Cf,Fg),S.xy('Torre di Poggio Raso'),98)
    B=S.xy((ll(42,37.8),ll(10,50))); G=sub(B,A); G=(G[0]/1.5,G[1]/1.5); vp,pv=water_for(G,vec(145,1.5))
    S.passi=['A: sull\'allineamento torre di Cala di Forno - Formica Grande, dove Poggio Raso si vede per 098°.',f'A-B {n1(dist(A,B))} mg in 1h30m: sul fondo {n1(mag(G))} kn per {deg(ang(G))}.',f'Togli la corrente (145°, 1,5 kn): Pv = {deg(pv)} (Vp {n1(vp)} kn).']
    lm_pt(S,'Torre di Cala di Forno','T. Cala di Forno'); lm_pt(S,'Faro di Formica Grande','Formica Grande'); lm_pt(S,'Torre di Poggio Raso','Poggio Raso')
    S.line(Cf,A,'rotta_l',''); S.line(A,S.xy('Torre di Poggio Raso'),'ril','098°'); S.pt(A,'A 11h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(ang(G))}'); P=add(A,vec(pv,vp)); S.line(A,P,'rotta_l',f'Pv {deg(pv)}'); S.fix(B,'B 12h30m')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(14)
def c5_4_1_14():
    S=CSol('5.4.1-14',lm('Scoglio dello Sparviero')); S.kind='dir'
    A=ship_from(S,'Fanale rosso del porto di Piombino',243,0.4); B=S.xy((ll(42,49),ll(10,41.4))); G=sub(B,A); t=40/60; G=(G[0]/t,G[1]/t); vp,pv=water_for(G,vec(192,3))
    S.passi=['A: fanale rosso di Piombino per 243° a 0,4 mg.',f'A-B {n1(dist(A,B))} mg in 40 minuti: sul fondo {n1(mag(G))} kn per {deg(ang(G))}.',f'Togli la corrente (192°, 3 kn): Pv = {deg(pv)} (Vp {n1(vp)} kn).']
    lm_pt(S,'Fanale rosso del porto di Piombino','Piombino'); lm_pt(S,'Scoglio dello Sparviero','Sparviero'); S.pt(A,'A 10h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(ang(G))}'); P=add(A,vec(pv,vp*t)); S.line(A,P,'rotta_l',f'Pv {deg(pv)}'); S.line(P,B,'corr','192°'); S.fix(B,'B 10h40m')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(14)
def c5_4_1_15():
    S=CSol('5.4.1-15',lm('Faro di Formica Grande')); S.kind='dir'
    A=ship_from(S,'Scoglio dello Sparviero',0,3); t=66/60; St=add(A,vec(161,10*t)); B=ship_from(S,'Faro di Formica Grande',124,2.4); dc=brg(St,B)
    S.passi=['A: lo Sparviero si vede per nord a 3 mg, quindi A è 3 mg a sud.',f'Stimato alle 04h26m: {n1(10*t)} mg per 161° (1h06m a 10 kn).','Osservato: Formica Grande per 124° a 2,4 mg.',f'Dallo stimato all\'osservato: Dc = {deg(dc)}.']
    lm_pt(S,'Scoglio dello Sparviero','Sparviero'); lm_pt(S,'Faro di Formica Grande','Formica Grande'); S.pt(A,'A 03h20m','ship'); S.line(A,St,'stima','161°'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 04h26m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(14)
def c5_4_1_16():
    S=CSol('5.4.1-16',(42.38,10.02)); S.kind='vel'
    A=S.xy((ll(42,21),ll(9,57))); B=S.xy((ll(42,24),ll(10,5.1))); St=add(A,vec(76,7.1*0.75)); vc=dist(St,B)/0.75
    S.passi=[f'Stimato alle 18h45m: {n1(7.1*0.75)} mg per 076°.',f'Dallo stimato al GPS: {n1(dist(St,B))} mg in 45 minuti.',f'Vc = {n1(vc)} kn (Dc {deg(brg(St,B))}).']
    S.pt(A,'A 18h00m','ship'); S.line(A,St,'stima','076°'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'{n1(dist(St,B))} mg'); S.fix(B,'B 18h45m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(14)
def c5_4_1_17():
    S=CSol('5.4.1-17',lm('Faro di Punta del Fenaio')); S.kind='ora'
    A=S.xy((ll(42,22.3),ll(10,41.2))); E=add(add(A,vec(63,5)),vec(180,1.5)); rv=brg(A,E); ve=dist(A,E); B=cross_lines(A,rv,S.xy('Faro di Punta del Fenaio'),150); t=dist(A,B)/ve
    S.passi=[f'In un\'ora: 5 mg per 063° più 1,5 mg verso sud: Rv {deg(rv)}, Ve {n1(ve)} kn.','B: dove il Fenaio si vede per 150°, sulla rotta vera.',f'{n1(dist(A,B))} mg: {hm(t*60)}, arrivo alle {hhmm(18+t)}.']
    lm_pt(S,'Faro di Punta del Fenaio','P.ta del Fenaio'); S.pt(A,'A 18h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); S.line(B,S.xy('Faro di Punta del Fenaio'),'ril2','150°'); S.fix(B,hhmm(18+t))
    return S.done(18+t,f'arrivo {hhmm(18+t)}')

@reg(14)
def c5_4_1_18():
    S=CSol('5.4.1-18',lm('Monte della Fortezza')); S.kind='vel'
    A=ship_from(S,'Monte della Fortezza',160,3.9); E=add(add(A,vec(38,5)),vec(95,2)); ve=dist(A,E)
    S.passi=['A: Monte della Fortezza per 160° a 3,9 mg.','In un\'ora: 5 mg per 038° più 2 mg per 095°.',f'Ve = {n1(ve)} kn (Rv {deg(brg(A,E))}).']
    lm_pt(S,'Monte della Fortezza','Montecristo'); S.pt(A,'A 22h00m','ship'); draw_tri(S,A,38,5,95,2); S.line(A,E,'rotta',f'Ve {n1(ve)}'); S.fix(E,'1 ora')
    return S.done(ve,f'Ve {n1(ve)} kn')

# ======================= LEZIONE 15: carta 42/D =======================
def c42(S): S.carta='42D'; return S

@reg(15)
def c5_5_3_1():
    S=c42(CSol('5.5.3-1',lm('Cardinale sud Les Moines')))
    V=4; Pv=290; r1=350; r2=60; run=2
    F,P1,q=running_fix(S,'Cardinale sud Les Moines',r1,'Cardinale sud Les Moines',r2,Pv,run)
    S.passi=['V = +3° +1° = +4°: Pv = 290°, Rilv₁ = 350°, Rilv₂ = 060°.','Cammino: 6 × 20/60 = 2 mg per 290°.','Trasporta il primo rilevamento del segnale cardinale e incrocialo con il secondo.']
    draw_running(S,'Cardinale sud Les Moines','cardinale S',r1,'Cardinale sud Les Moines','cardinale S',r2,Pv,run,F,P1,q,'02h30m','02h50m'); lm_pt(S,'Faro di Cap de Feno','Cap de Feno')
    S.fix(F,'PN 02h50m'); return S

@reg(15)
def c5_5_3_2():
    S=c42(CSol('5.5.3-2',(41.33,9.05)))
    A=S.xy((ll(41,22.2),ll(8,57.5))); B=S.xy((ll(41,17.3),ll(9,6))); t=intercept(A,8,B,60,3.3); D_=add(B,u(60),3.3*t)
    S.passi=ipassi('Esperia',60,3.3,8,brg(A,D_),t); draw_intercept(S,A,8,B,60,3.3,D_,'Mizar','Esperia')
    S.pt(A,'A · Mizar','ship'); S.pt(B,'B · Esperia','ship'); S.line(A,D_,'rotta',f'{deg(brg(A,D_))} · 8 kn'); S.line(B,D_,'rotta2','Esperia 060°'); S.fix(D_,'D'); return S

@reg(15)
def c5_6_3_1():
    S=c42(CSol('5.6.3-1',lm('Faro di Lavezzi'))); S.kind='ora'
    d=0+5/60+16*7/60; Pm=180-round(d); dv=round(dev_pm(Pm)); V=round(d)+dv
    lines=[('Cardinale est Ecueil de Perduto',243+V),('Faro di Razzoli',195+V),('Torre di Santa Manza',286+V)]
    ps=[cross_lines(S.xy(a),ra,S.xy(b),rb) for (a,ra),(b,rb) in ((lines[0],lines[1]),(lines[0],lines[2]),(lines[1],lines[2]))]
    A=(sum(p[0] for p in ps)/3,sum(p[1] for p in ps)/3); L=S.xy('Faro di Lavezzi'); T=cross_lines(A,180,L,270); t=dist(A,T)/4
    S.passi=[f'Declinazione 2009: 0°05′ + 16 × 7′ = {int(d)}°{round((d-int(d))*60):02d}′E ≈ {round(d)}°E. Pm = {Pm:03d}°, dalla tabella δ = {dv:+d}°: V = {V:+d}°.',
             f'Rilv: Perduto {deg(243+V)}, Razzoli {deg(195+V)}, Santa Manza {deg(286+V)}: il loro incrocio è A.',f'Lavezzi al traverso di dritta con prora 180°: lo si vede per 270°, alla sua stessa latitudine.',f'{n1(dist(A,T))} mg a 4 kn = {hm(t*60)}: traverso alle {hhmm(11+50/60+t)}.']
    for n,r in lines: lm_pt(S,n,{'Cardinale est Ecueil de Perduto':'Perduto','Faro di Razzoli':'Razzoli','Torre di Santa Manza':'Santa Manza'}[n]); S.line(A,S.xy(n),'ril',deg(r))
    lm_pt(S,'Faro di Lavezzi','Lavezzi'); S.pt(A,'A 11h50m','ship'); S.line(A,T,'rotta','Pv 180°'); S.line(T,L,'ril2','270°'); S.fix(T,hhmm(11+50/60+t))
    return S.done(11+50/60+t,f'traverso alle {hhmm(11+50/60+t)}')

@reg(15)
def c5_6_3_2():
    S=c42(CSol('5.6.3-2',lm('Faro delle Isolette Monaci')))
    Pv=300; r1=235; r2=210; run=1.5
    F,P1,q=running_fix(S,'Faro delle Isolette Monaci',r1,'Faro delle Isolette Monaci',r2,Pv,run)
    S.passi=['V = +2° −2° = 0°: Pv 300°, Rilv 235° e 210°.','Cammino: 6 × 15/60 = 1,5 mg per 300°.','Trasporta il primo rilevamento e incrocialo con il secondo.']
    draw_running(S,'Faro delle Isolette Monaci','Isolette Monaci',r1,'Faro delle Isolette Monaci','Isolette Monaci',r2,Pv,run,F,P1,q,'1° ril.','2° ril.')
    S.fix(F,'PN'); return S

@reg(15)
def c5_6_3_3():
    S=c42(CSol('5.6.3-3',lm('Faro di Capo Ferro')))
    A=fix2(S,'Faro di Capo Ferro',135,'Meda della Secca di Tre Monti',246); A2=add(A,u(0),6); B=S.xy((ll(41,22.5),ll(9,23.5))); t=intercept(A2,9.9,B,225,2); D_=add(B,u(225),2*t)
    S.passi=['A: Capo Ferro per 135° e meda di Tre Monti per 246°. In 45 minuti a 8 kn verso nord: 6 mg, punto A′ delle 21h05m.']+[x.replace(' A ',' A′ ').replace('da A ','da A′ ').replace('Da A ','Da A′ ').replace('ad AB','ad A′B') for x in ipassi('Deneb',225,2,9.9,brg(A2,D_),t)]
    draw_intercept(S,A2,9.9,B,225,2,D_,'Altair','Deneb'); lm_pt(S,'Faro di Capo Ferro','Capo Ferro'); lm_pt(S,'Meda della Secca di Tre Monti','Tre Monti')
    S.pt(A,'A 20h20m','ship'); S.pt(A2,"A′ 21h05m",'ship'); S.pt(B,'B · Deneb','ship'); S.line(A,A2,'rotta','000° · 6 mg'); S.line(A2,D_,'rotta',f'{deg(brg(A2,D_))}'); S.line(B,D_,'rotta2','Deneb 225°'); S.fix(D_,'D'); S.pts.append(((41.10,9.40),'','none')); return S

@reg(15)
def c5_7_3_1():
    S=c42(CSol('5.7.3-1',lm('Campanile di Punta di li Francesi')))
    # il monte Russo è usato solo come direzione: lo posizioniamo sulla linea del rilevamento 240° dalla rada
    Pv=280; run=3; F0=S.xy((ll(41,10.1),ll(9,4.6))); P1=add(F0,u(Pv),-run); LM['Monte Russo']=S.ll(add(P1,u(240),1.2))
    F,P1,q=running_fix(S,'Monte Russo',240,'Campanile di Punta di li Francesi',210,Pv,run)
    S.passi=['V = −3° +2° = −1°: Pv 280°, Monte Russo per 240°, campanile per 210°.','Cammino: 18 × 10/60 = 3 mg per 280°.','Trasporta il rilevamento del monte e incrocialo con quello del campanile.']
    draw_running(S,'Monte Russo','M. Russo',240,'Campanile di Punta di li Francesi','campanile',210,Pv,run,F,P1,q,'12h00m','12h10m')
    S.fix(F,'PN 12h10m'); return S

@reg(15)
def c5_7_3_2():
    S=c42(CSol('5.7.3-2',(41.17,9.0)))
    A=S.xy((ll(41,8.5),ll(9,1.5))); B=S.xy((ll(41,12),ll(9,2.5))); t=intercept(A,3,B,280,2); D_=add(B,u(280),2*t)
    S.passi=ipassi('Denebola',280,2,3,brg(A,D_),t); draw_intercept(S,A,3,B,280,2,D_,'Enif','Denebola')
    S.pt(A,'A · Enif','ship'); S.pt(B,'B · Denebola','ship'); S.line(A,D_,'rotta',f'{deg(brg(A,D_))} · 3 kn'); S.line(B,D_,'rotta2','280° · 2 kn'); S.fix(D_,'D'); return S

@reg(15)
def c5_8_3_1():
    S=c42(CSol('5.8.3-1',lm('Faro di Punta Timone')))
    Pv=315; run=14*12/60
    F,P1,q=running_fix(S,'Faro di Punta Timone',270,'Faro della Bocca di Olbia',253,Pv,run)
    S.passi=['V = +4° −6° = −2°: Pv 315°, Punta Timone per 270°, Bocca di Olbia per 253°.',f'Cammino: 14 × 12/60 = {n1(run)} mg per 315°.','Trasporta il rilevamento di Punta Timone e incrocialo con quello della Bocca di Olbia: è il punto di accostata.']
    draw_running(S,'Faro di Punta Timone','P.ta Timone',270,'Faro della Bocca di Olbia','Bocca di Olbia',253,Pv,run,F,P1,q,'06h30m','06h42m')
    S.fix(F,'accostata'); return S

@reg(15)
def c5_8_3_2():
    S=c42(CSol('5.8.3-2',lm('Faro delle Isolette Monaci')))
    A=S.xy((ll(41,5.2),ll(9,48))); B=add(S.xy('Faro delle Isolette Monaci'),u(90),8); t=intercept(A,6.6,B,100,1.5); D_=add(B,u(100),1.5*t)
    S.passi=['B: 8 mg a levante (est) del faro delle Isole Monaci.']+ipassi('Schedar',100,1.5,6.6,brg(A,D_),t); draw_intercept(S,A,6.6,B,100,1.5,D_,'Alpheratz','Schedar')
    lm_pt(S,'Faro delle Isolette Monaci','Monaci'); S.pt(A,'A · Alpheratz','ship'); S.pt(B,'B · Schedar','ship'); S.line(A,D_,'rotta',f'{deg(brg(A,D_))}'); S.line(B,D_,'rotta2','100°'); S.fix(D_,'D'); return S

@reg(15)
def c5_8_3_3():
    S=c42(CSol('5.8.3-3',lm('Faro delle Isolette Monaci')))
    A=S.xy((ll(41,7.6),ll(9,39.1))); B=ship_from(S,'Faro delle Isolette Monaci',249,8); t=intercept(A,5,B,170,3.2); D_=add(B,u(170),3.2*t)
    S.passi=['B: il faro delle Monaci si vede per 249° a 8 mg, quindi B è 8 mg per 069° dal faro.']+ipassi('Spica',170,3.2,5,brg(A,D_),t); draw_intercept(S,A,5,B,170,3.2,D_,'Hamal','Spica')
    lm_pt(S,'Faro delle Isolette Monaci','Monaci'); S.pt(A,'A · Hamal','ship'); S.pt(B,'B · Spica','ship'); S.line(A,D_,'rotta',f'{deg(brg(A,D_))}'); S.line(B,D_,'rotta2','170°'); S.fix(D_,'D'); return S

@reg(15)
def c5_5_1_1():
    S=c42(CSol('5.5.1-1',lm('Faro di Cap de Feno'))); S.kind='dir'
    A=fix2(S,'Faro di Cap de Feno',335,'Faro di Cap Pertusato',32); pv,ve=pv_for(290,7,250,2.5)
    S.passi=['A: Cap de Feno per 335° e Cap Pertusato per 032°.','Rotta 290°, Vp 7 kn, corrente 250°/2,5 kn.',f'Triangolo: Pv = {deg(pv)} (Ve {n1(ve)} kn).']
    lm_pt(S,'Faro di Cap de Feno','Cap de Feno'); lm_pt(S,'Faro di Cap Pertusato','Pertusato'); S.pt(A,'A 20h20m','ship'); S.line(A,S.xy('Faro di Cap de Feno'),'ril','335°'); S.line(A,S.xy('Faro di Cap Pertusato'),'ril','032°')
    E=add(A,vec(290,ve)); S.line(A,E,'rotta','Rv 290°'); C1=add(A,vec(250,2.5)); S.line(A,C1,'corr','250° · 2,5'); S.line(C1,E,'rotta_l',f'Pv {deg(pv)}')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(15)
def c5_5_1_2():
    S=c42(CSol('5.5.1-2',lm('Faro di Capo Testa'))); S.kind='dir'
    Bp=S.xy((ll(41,15.7),ll(9,4.7))); P=S.xy('Porto di Punta la Madonnetta'); t=35/60; best=None
    for k in range(5,60):
        d=k/10; A=ship_from(S,'Faro di Capo Testa',67,d); C=sub(Bp,add(A,vec(44,7*t))); C=(C[0]/t,C[1]/t)
        G=sub(P,Bp); vp,pv=water_for(G,C)
        if best is None or abs(pv-34)<abs(best[0]-34): best=(pv,vp,A,C,d)
    pv,vp,A,C,d=best
    S.passi=[f'A: sul rilevamento 067° di Capo Testa, alla batimetrica dei 50 m (circa {n1(d)} mg dal faro).',f'Stimato alle 07h20m: {n1(7*t)} mg per 044°. Dallo stimato a B: corrente {deg(ang(C))}, {n1(mag(C))} kn.',
             f'Da B al porto di Punta la Madonnetta in 1 ora: {n1(dist(Bp,P))} mg per {deg(brg(Bp,P))}.',f'Togli la corrente: Pv = {deg(pv)} (Vp {n1(vp)} kn).']
    lm_pt(S,'Faro di Capo Testa','Capo Testa'); S.pt(A,'A 06h45m','ship'); St=add(A,vec(44,7*t)); S.line(A,St,'stima','044°'); S.line(St,Bp,'corr','corrente'); S.pt(Bp,'B 07h20m','ship'); S.line(Bp,P,'rotta','Rv'); S.fix(P,'Madonnetta')
    S.note='La batimetrica dei 50 m non è nei nostri dati: la distanza di A dal faro va letta sulla carta.'
    return S.done(pv,f'Pv {deg(pv)}')

@reg(15)
def c5_5_1_3():
    S=c42(CSol('5.5.1-3',lm('Faro di Cap de Feno'))); S.kind='dir'
    A=ship_from(S,'Faro di Cap de Feno',90,2); St=add(A,vec(175,6.6*1.5)); B=fix2(S,'Faro di Cap Pertusato',52,'Faro di Capo Testa',98); dc=brg(St,B)
    S.passi=['A: Cap de Feno per 090° a 2 mg, quindi A è 2 mg a ovest del faro.',f'Stimato alle 09h50m: {n1(6.6*1.5)} mg per 175°.','Osservato B: Pertusato per 052° e Capo Testa per 098°.',f'Dallo stimato all\'osservato: Dc = {deg(dc)}.']
    lm_pt(S,'Faro di Cap de Feno','Cap de Feno'); lm_pt(S,'Faro di Cap Pertusato','Pertusato'); lm_pt(S,'Faro di Capo Testa','Capo Testa'); S.pt(A,'A 08h20m','ship'); S.line(A,St,'stima','175°'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 09h50m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(15)
def c5_6_1_1():
    S=c42(CSol('5.6.1-1',lm('Faro delle Isolette Monaci'))); S.kind='dir'
    A=fix2(S,'Faro di Capo Ferro',247,'Faro delle Isolette Monaci',300); B=S.xy((ll(41,21.5),ll(9,26))); rv=brg(A,B); pv,ve=pv_for(rv,12,45,2.5)
    S.passi=['A: Capo Ferro per 247° e Isole Monaci per 300°.',f'Rotta A-B: {deg(rv)}.',f'Con Vp 12 e corrente 045°/2,5 kn: Pv = {deg(pv)} (Ve {n1(ve)} kn).']
    lm_pt(S,'Faro di Capo Ferro','Capo Ferro'); lm_pt(S,'Faro delle Isolette Monaci','Monaci'); S.pt(A,'A 15h00m','ship'); S.line(A,B,'rotta',f'Rv {deg(rv)}'); C1=add(A,vec(45,2.5*0.4)); S.line(A,C1,'corr','045°'); S.line(C1,add(A,vec(rv,ve*0.4)),'rotta_l',f'Pv {deg(pv)}'); S.fix(B,'B')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(15)
def c5_6_1_2():
    S=c42(CSol('5.6.1-2',lm('Faro delle Isolette Monaci'))); S.kind='dir'
    A=S.xy((ll(41,20),ll(9,30))); St=add(A,vec(137,10)); B=ship_from(S,'Faro delle Isolette Monaci',280,4); dc=brg(St,B)
    S.passi=['Stimato alle 22h00m: 10 mg per 137°.','Osservato: Monaci per 280° a 4 mg (B è a est del faro).',f'Dallo stimato all\'osservato: Dc = {deg(dc)} ({n1(dist(St,B))} kn).']
    lm_pt(S,'Faro delle Isolette Monaci','Monaci'); S.pt(A,'A 21h00m','ship'); S.line(A,St,'stima','137° · 10 mg'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 22h00m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(15)
def c5_7_1_1():
    S=c42(CSol('5.7.1-1',lm('Punta li Canneddi'))); S.kind='vel'
    A=ship_from(S,'Punta li Canneddi',115,1); St=add(A,vec(45,6.5)); B=S.xy((ll(41,7.4),ll(8,55.1))); vc=dist(St,B)
    S.passi=['A: Punta li Canneddi per 115° a 1 mg.','Stimato alle 13h00m: 6,5 mg per 045°.',f'Dallo stimato al GPS: {n1(vc)} mg in un\'ora, Vc = {n1(vc)} kn.']
    lm_pt(S,'Punta li Canneddi','P.ta li Canneddi'); S.pt(A,'A 12h00m','ship'); S.line(A,St,'stima','045°'); S.pt(St,'stimato','ship'); S.line(St,B,'corr',f'{n1(vc)} mg'); S.fix(B,'B 13h00m')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(15)
def c5_7_1_2():
    S=c42(CSol('5.7.1-2',(40.95,8.76))); S.kind='vel'
    A=S.xy((ll(40,54.9),ll(8,42.1))); E=add(add(A,vec(35,6)),vec(59,2)); ve=dist(A,E)
    S.passi=['In un\'ora: 6 mg per 035° più 2 mg per 059°.',f'Ve = {n1(ve)} kn (Rv {deg(brg(A,E))}).']
    S.pt(A,'A','ship'); draw_tri(S,A,35,6,59,2); S.line(A,E,'rotta',f'Ve {n1(ve)}'); S.fix(E,'1 ora')
    return S.done(ve,f'Ve {n1(ve)} kn')

@reg(15)
def c5_8_1_1():
    S=c42(CSol('5.8.1-1',lm('Ex semaforo di Capo Figari'))); S.kind='vel'
    A=fix2(S,'Ex semaforo di Capo Figari',288,'Faro di Punta Timone',216); B=ship_from(S,'Fanale delle Isole Nibani',235,2); t=100/60; G=sub(B,A); G=(G[0]/t,G[1]/t); vp,pv=water_for(G,vec(246,2.4))
    S.passi=['A: Capo Figari per 288° e Punta Timone per 216°.','B: il fanale delle Nibani per 235° a 2 mg.',f'A-B {n1(dist(A,B))} mg in 1h40m: sul fondo {n1(mag(G))} kn per {deg(ang(G))}.',f'Togli la corrente (246°, 2,4 kn): Vp = {n1(vp)} kn (Pv {deg(pv)}).']
    lm_pt(S,'Ex semaforo di Capo Figari','C. Figari'); lm_pt(S,'Faro di Punta Timone','P.ta Timone'); lm_pt(S,'Fanale delle Isole Nibani','Nibani'); S.pt(A,'A 14h20m','ship'); S.line(A,B,'rotta',f'Rv {deg(ang(G))}'); S.fix(B,'B 16h00m')
    return S.done(vp,f'Vp {n1(vp)} kn')

@reg(15)
def c5_8_1_2():
    S=c42(CSol('5.8.1-2',lm('Faro di Punta Timone'))); S.kind='dir'
    d=10/60+15*7/60; pb=348; pm=pb
    for _ in range(4): dv=dev_pm(pm); pm=pb+dv
    dv=round(dev_pm(pm)); pv=pb+dv+round(d); A=fix2(S,'Faro di Punta Timone',242+dv+round(d),'Faro di Figarolo',283+dv+round(d)); E=add(add(A,vec(pv,7)),vec(100,1.5)); rv=brg(A,E)
    S.passi=[f'Declinazione 2008: 0°10′ + 15 × 7′ = {int(d)}°{round((d-int(d))*60):02d}′E ≈ {round(d)}°E. Con Pb 348° la tabella dà δ = {dv:+d}°.',f'Pv = Pb + δ + d = {deg(pv)}.','In un\'ora: 7 mg per la Pv più 1,5 mg per 100°.',f'Rv = {deg(rv)}.']
    lm_pt(S,'Faro di Punta Timone','P.ta Timone'); lm_pt(S,'Faro di Figarolo','Figarolo'); S.pt(A,'A 05h30m','ship'); draw_tri(S,A,pv,7,100,1.5); S.line(A,E,'rotta',f'Rv {deg(rv)}'); S.fix(E,'1 ora')
    return S.done(rv,f'Rv {deg(rv)}')

@reg(15)
def c5_8_1_3():
    S=c42(CSol('5.8.1-3',lm('Faro di Capo Ferro'))); S.kind='dir'
    St=S.xy((ll(41,8.5),ll(9,37.6))); B=fix2(S,'Faro di Capo Ferro',281,'Faro di Punta Timone',173); dc=brg(St,B)
    S.passi=['Punto stimato A delle 20h20m: dato dalla traccia.','Punto osservato B: Capo Ferro per 281° e Punta Timone per 173°.',f'Dallo stimato all\'osservato: Dc = {deg(dc)} ({n1(dist(St,B))} mg in 1h20m).']
    lm_pt(S,'Faro di Capo Ferro','Capo Ferro'); lm_pt(S,'Faro di Punta Timone','P.ta Timone'); S.pt(St,'A stimato','ship'); S.line(B,S.xy('Faro di Capo Ferro'),'ril','281°'); S.line(B,S.xy('Faro di Punta Timone'),'ril','173°'); S.line(St,B,'corr',f'Dc {deg(dc)}'); S.fix(B,'B 20h20m')
    return S.done(dc,f'Dc {deg(dc)}')

@reg(15)
def c5_8_1_4():
    S=c42(CSol('5.8.1-4',lm('Fanale delle Isole Nibani'))); S.kind='dir'
    A=ship_from(S,'Ex semaforo di Capo Figari',250,4.3); N=S.xy('Fanale delle Isole Nibani'); R=dist(A,N); b=brg(A,N); a=math.degrees(math.asin(1/R)); rv=norm(b+a); pv,ve=pv_for(rv,6,180,2)
    S.passi=['A: Capo Figari per 250° a 4,3 mg (A è a ENE del semaforo).',f'Rotta tangente al cerchio di 1 mg attorno al fanale, lasciandolo a sinistra: Rv {deg(rv)}.',f'Con Vp 6 e corrente verso sud 2 kn: Pv = {deg(pv)} (Ve {n1(ve)} kn).']
    lm_pt(S,'Ex semaforo di Capo Figari','C. Figari'); lm_pt(S,'Fanale delle Isole Nibani','Nibani'); S.pt(A,'A 08h00m','ship'); T=add(A,u(rv),math.sqrt(R*R-1)); S.line(A,T,'rotta',f'Rv {deg(rv)}'); S.line(T,N,'ril2','1 mg'); S.fix(T,'B')
    return S.done(pv,f'Pv {deg(pv)}')

@reg(15)
def c5_8_1_5():
    S=c42(CSol('5.8.1-5',lm('Faro di Punta Timone'))); S.kind='vel'
    A=fix2(S,'Faro di Punta Timone',242,'Faro di Figarolo',283); B=S.xy((ll(40,57.5),ll(9,46.1))); vc=dist(A,B)
    S.passi=['Rilevamenti polari a sinistra con Pv 000°: Punta Timone 360° − 118° = 242°, Figarolo 360° − 77° = 283°: punto nave A.','Punto stimato B della stessa ora (dato dalla traccia).',f'In un\'ora la corrente ha spostato la barca da B ad A: {n1(vc)} mg, Vc = {n1(vc)} kn.']
    lm_pt(S,'Faro di Punta Timone','P.ta Timone'); lm_pt(S,'Faro di Figarolo','Figarolo'); S.pt(B,'B stimato','ship'); S.line(A,S.xy('Faro di Punta Timone'),'ril','242°'); S.line(A,S.xy('Faro di Figarolo'),'ril','283°'); S.line(B,A,'corr',f'{n1(vc)} mg'); S.fix(A,'A osservato')
    return S.done(vc,f'Vc {n1(vc)} kn')

@reg(15)
def c5_8_1_6():
    S=c42(CSol('5.8.1-6',lm('Faro dello Scoglio Mortoriotto'))); S.kind='dir'
    A=fix2(S,'Faro dello Scoglio Mortoriotto',317,'Ex semaforo di Capo Figari',196); pv,ve=pv_for(350,7.5,115,2.5)
    S.passi=['A: Mortoriotto per 317° e Capo Figari per 196°.','Rotta 350°, Vp 7,5 kn, corrente 115°/2,5 kn.',f'Pv = {deg(pv)} (Ve {n1(ve)} kn).']
    lm_pt(S,'Faro dello Scoglio Mortoriotto','Mortoriotto'); lm_pt(S,'Ex semaforo di Capo Figari','C. Figari'); S.pt(A,'A 07h00m','ship'); S.line(A,S.xy('Faro dello Scoglio Mortoriotto'),'ril','317°'); S.line(A,S.xy('Ex semaforo di Capo Figari'),'ril','196°')
    E=add(A,vec(350,ve)); S.line(A,E,'rotta','Rv 350°'); C1=add(A,vec(115,2.5)); S.line(A,C1,'corr','115° · 2,5'); S.line(C1,E,'rotta_l',f'Pv {deg(pv)}')
    return S.done(pv,f'Pv {deg(pv)}')

if __name__=='__main__':
    import sys
    for les in (13,14,15):
        ok=0
        for fn in SOLS[les]:
            S=fn(); c=S.check(); ok+=bool(c)
            print(les,S.id,S.res_txt,'| uff',S.ex['risposta_ufficiale'].replace('\n',' '),'|','OK' if c else 'FUORI')
        print('lezione',les,ok,'/',len(SOLS[les]))
