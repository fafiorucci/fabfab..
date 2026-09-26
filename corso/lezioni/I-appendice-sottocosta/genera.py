"""Appendice I: navigare sottocosta (quiz 1.7.6, 1.7.2, 1.7.8, 1.7.3, 1.4.2, 1.3.6, 1.3.8)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
ORDER=['cover','indice','costa','carte','leggere','pubblicazioni','quizA','quizAr',
       'cospicui','rilevare','luoghi','pericoli','gps','quizB','quizBr',
       'vento','notte','regole','incaglio','quizC','quizCr','chiusura']
EB='Appendice I · Navigare sottocosta'
LB.ICON_T.update({'Indice':'book','Perché sottocosta è difficile':'map','Le carte giuste':'map','Che cosa dice la carta':'map',
 'Le pubblicazioni di bordo':'book','Riconoscere la costa':'lighthouse','Dove sono rispetto al faro':'compass',
 'I luoghi di posizione':'dividers','Stare lontani dai pericoli':'flag','Il GPS vicino alla costa':'compass',
 'Costa sopravento e sottovento':'wind','Di notte e nella nebbia':'lighthouse','Le regole vicino a riva':'flag','Se si tocca il fondo':'hull'})

cover_app('I','Navigare sottocosta','Carte e pubblicazioni, punti cospicui e rilevamenti, pericoli, GPS, vento, notte e regole vicino a riva',
 'Appendice I al corso. Ripasso della navigazione in vista della costa: quiz ufficiali 1.7.6 (navigazione costiera), 1.7.2 (carte), 1.7.8 (pubblicazioni), 1.7.3 (GPS), 1.4.2 (condotta vicino alla costa), 1.3.6 e 1.3.8 (incaglio, cattivo tempo). Collegata alle lezioni 3, 4, 5, 10 e alle appendici F e G.')
index_slide(EB,[('Preparare','Perché è difficile, carte, simboli, pubblicazioni',['costa','carte','leggere','pubblicazioni','quizA','quizAr'],CORAL),
 ('Sapere dove sei','Punti cospicui, rilevamenti, luoghi di posizione, pericoli, GPS',['cospicui','rilevare','luoghi','pericoli','gps','quizB','quizBr'],SEA),
 ('Il mare vicino a riva','Vento e costa, notte e nebbia, regole, incaglio',['vento','notte','regole','incaglio','quizC','quizCr'],PURPLE)],ORDER,
 'Sottocosta il pericolo non è il largo: è il fondo che sale.',
 'Appendice di ripasso per chi naviga in vista della costa, come si fa quasi sempre con la patente entro e oltre le 12 miglia. Le parti seguono l\'ordine di un\'uscita: si prepara, si naviga controllando la posizione, si gestiscono vento, notte e regole locali.')

# ============ PERCHÉ È DIFFICILE ============
sec('costa', head('Preparare','Perché sottocosta è difficile',CORAL)+tiles([
 ('I pericoli','Secche, scogli, bassi fondali: sono tutti vicino alla costa. Un punto nave impreciso qui porta all\'incaglio.',CORAL),
 ('Riconoscere','Tanti punti sulla costa, non sempre facili da identificare. Servono carte a scala adeguata e pubblicazioni.',SEA),
 ('Il principio','La navigazione è costiera quando il punto nave si fa con punti cospicui visibili dal mare: bisogna vedere la costa.',PURPLE),
 ('La precisione','Il punto costiero è preciso quanto gli strumenti, il metodo e l\'esperienza di chi lo fa.',BLUE)])
 +note('Sottocosta si naviga con gli occhi fuori e la carta sotto mano.',CORAL,36),
 notes='Quiz 1.7.6-5 (navigazione costiera impegnativa: punti cospicui non sempre riconoscibili), -3 e -4 (carte a scala adeguata e pubblicazioni), -23 e -41 (punto nave da elementi cospicui, in vista della costa), -6 e -49 (precisione e affidabilità), 1.3.6-4 (l\'incaglio può derivare da un punto nave impreciso vicino alla costa).')

sec('carte', head('Preparare','Le carte giuste',CORAL)+table(['Carta','Scala tipica','A che cosa serve'],[26,22,52],[
 ('Generale','1:3.000.000 e meno','Pianificare lunghe traversate'),
 ('Costiera','1:100.000','Navigare lungo la costa e avvicinarsi all\'atterraggio'),
 ('Costiera a grande scala','1:50.000','Condurre la navigazione costiera nei dettagli'),
 ('Dei litorali','Più grande della costiera','Zone di interesse: accessi, passaggi'),
 ('Piano nautico','1:5.000','Porti, rade, isolotti: banchine, ormeggi, fondali')],CORAL,28)
 +note('La scala più grande è quella con il denominatore più piccolo: 1:5.000 è più grande di 1:100.000.',CORAL,34),
 notes='Quiz 1.7.2-5 e -17 (classificazione per scala), -6 e -18 (carte generali), -7 e -22 (costiere 1:100.000), -35 (1:50.000, costiera a grande scala), -49 (litorali), -12, -13, -23 (piani nautici e pianetti, 1:5.000), -25 (scala maggiore = denominatore minore), -10 (la carta a piccola scala non serve per la costiera), -26 (sulle carte didattiche non si naviga), -14 (la gnomonica è per le traversate oceaniche). Il quiz 1.7.2-21 è oscurato.')

# ============ CHE COSA DICE LA CARTA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{CHART}"/>'
b+=f'<path d="M0 0 L1092 0 L1092 150 Q900 200 760 150 Q620 100 480 170 Q340 240 200 170 Q100 120 0 160 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
for d_,c,off in ((5,'#9CC9DA',60),(10,'#6FAFC6',150),(20,'#3C8FAE',280)):
    b+=f'<path d="M0 {160+off} Q100 {120+off} 200 {170+off} Q340 {240+off} 480 {170+off} Q620 {100+off} 760 {150+off} Q900 {200+off} 1092 {150+off}" fill="none" stroke="{c}" stroke-width="4" stroke-dasharray="14 8"/>'
b+=f'<path d="M0 160 Q100 120 200 170 Q340 240 480 170 Q620 100 760 150 Q900 200 1092 150 L1092 210 Q900 260 760 210 Q620 160 480 230 Q340 300 200 230 Q100 180 0 220 Z" fill="#CFE8F3" fill-opacity="0.8"/>'
b+=''.join(f'<path d="M{x-10} {y} l10 -10 l10 10 l-10 10 Z M{x-14} {y} h28 M{x} {y-14} v28" stroke="{NAVY}" stroke-width="3" fill="none"/>' for x,y in ((640,300),(668,318)))
b+=tower(880,190,0.9)
lbl=pill(X+30,Y+214,300,'batimetrica dei 5 m',SEA)+pill(X+30,Y+306,300,'batimetrica dei 10 m',SEA)+pill(X+30,Y+436,300,'batimetrica dei 20 m',SEA)
lbl+=lab(X+700,Y+300,200,'scogli',NAVY,24,900)+lab(X+180,Y+520,260,'r · roccia',NAVY,28,900)+lab(X+460,Y+520,260,'f · fango',NAVY,28,900)+lab(X+720,Y+520,300,'P.A. · pos. appross.',NAVY,28,900)
lbl+=lab(X+800,Y+60,260,'F · luce fissa',NAVY,24,900)+lab(X+560,Y+400,120,'12',NAVY,28,500,'center')+lab(X+330,Y+380,120,'7',NAVY,28,500,'center')
txt=(item(1,SEA,'Batimetriche','Linee di uguale profondità: anche una batimetrica è un luogo di posizione.')
     +item(2,CORAL,'Scandagli e fondo','I numeri sono le profondità; le lettere dicono il fondo: r roccia, f fango.')
     +item(3,PURPLE,'Sigle','P.A. posizione approssimativa; F luce fissa. Profilo della costa ed elevazioni.')
     +item(4,BLUE,'Aggiornamenti','Si riportano a margine della carta; carte vecchie o didattiche non valgono.'))
sec('leggere', head('Preparare','Che cosa dice la carta',CORAL), pinned=svgp(X,Y,W,Hh,b,'Stralcio di carta nautica con la costa, le batimetriche dei 5, 10 e 20 metri, i numeri degli scandagli, due simboli di scoglio, un faro e le sigle del fondale')+lbl+pcol(txt,532,18),
 notes='Quiz 1.7.2-8 e -48 (batimetriche e isobate: uguale profondità), 1.7.6-2 (la batimetrica è un luogo di posizione), 1.7.2-15 e -29 (natura del fondo sulla carta), -38 (r roccia), -39 (f fango), -44 (P.A.), -32 (F luce fissa), -24 (profondità, elevazioni, segni convenzionali), -3 (aggiornamenti a margine), -36 (nuova edizione), 1.7.8-3 (ristampa). Disegno schematico: non è una carta reale.')
X=700

sec('pubblicazioni', head('Preparare','Le pubblicazioni di bordo',CORAL)+table(['Pubblicazione','Che cosa ci trovi'],[32,68],[
 ('Portolano','Descrizione della costa, pericoli, fari, servizi dei porti, venti di traversìa'),
 ('Elenco dei fari e segnali da nebbia','Posizione e caratteristiche di tutti i segnali luminosi e sonori'),
 ('Avvisi ai naviganti','Le correzioni per aggiornare carte e pubblicazioni'),
 ('Radioservizi per la navigazione','Orari e canali delle stazioni radio e del Meteomar'),
 ('Catalogo I.I. 3001','L\'elenco di tutte le carte e pubblicazioni dell\'IIM')],CORAL,28)
 +note('Portolano: «venti di traversìa del II quadrante» vuol dire porto poco riparato da Levante, Scirocco e Ostro.',CORAL,32),
 notes='Quiz 1.7.8-7 (Portolano), -5 (venti di traversìa del secondo quadrante: Levante, Scirocco, Ostro), -6 (Elenco dei fari), -4 (Avvisi ai naviganti), -2 (aggiornamento), -1 (catalogo I.I. 3001), -8 (documenti nautici), 1.6.2-23 (Radioservizi), 1.7.2-1 (le carte IIM coprono i mari italiani e il Mediterraneo).')

quiz_slide('quizA','Verifica · carte e pubblicazioni',['1.7.2-25','1.7.8-7','1.7.2-48'],False)
quiz_slide('quizAr','Verifica · carte e pubblicazioni',['1.7.2-25','1.7.8-7','1.7.2-48'],True)

# ============ RICONOSCERE LA COSTA ============
b=f'<rect x="0" y="0" width="1092" height="380" fill="{SKY}"/><rect x="0" y="380" width="1092" height="240" fill="{WATER}" fill-opacity="0.35"/>'
b+=f'<path d="M0 380 L0 300 Q80 260 160 290 Q260 200 380 250 Q470 180 560 240 Q660 300 760 260 Q860 210 960 280 Q1030 320 1092 300 L1092 380 Z" fill="#B9C9A0" stroke="#7E946A" stroke-width="3"/>'
b+=f'<path d="M960 380 L960 300 L1092 280 L1092 380 Z" fill="#9FB08A"/>'
b+=tower(170,300,1.1)+church(560,250,1.0)+f'<rect x="380" y="206" width="30" height="50" fill="#D8C8A8" stroke="{NAVY}" stroke-width="3"/><path d="M372 206 h46" stroke="{NAVY}" stroke-width="5"/>'
b+=f'<path d="M900 240 L920 170 L940 240 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/><circle cx="920" cy="160" r="10" fill="{CORAL}"/>'
b+=profile(430,470,200)
lbl=pill(X+100,Y+120,160,'faro',CORAL)+pill(X+340,Y+150,160,'torre',SEA)+pill(X+520,Y+100,200,'campanile',PURPLE)+pill(X+860,Y+100,200,'antenna',BLUE)+pill(X+960,Y+320,120,'capo',NAVY)
lbl+=lab(X+60,Y+560,600,'punti ben visibili, entro 8–10 miglia',NAVY,24,900)
txt=(item(1,CORAL,'Punti cospicui','Faro, campanile, torre, capo, antenna: tutto ciò che si vede bene dal mare e che è segnato sulla carta.')
     +item(2,SEA,'Prima di partire','Scegli sulla carta i punti che userai e guarda nel Portolano come appaiono dal mare.')
     +item(3,PURPLE,'Controlla','Un punto sbagliato dà un punto nave sbagliato: confrontalo con la batimetrica e il GPS.'))
sec('cospicui', head('Sapere dove sei','Riconoscere la costa',SEA)+col(txt,520,22), pinned=svgp(X,Y,W,Hh,b,'Profilo della costa visto dal mare con un faro, una torre, un campanile, un\'antenna e un capo, e una barca in primo piano')+lbl,
 notes='Quiz 1.7.6-45 (il campanile è un punto cospicuo), -7 (punti ben visibili entro 8-10 miglia), -3 e -4 (carte e pubblicazioni per riconoscere la costa), 1.7.8-7 (il Portolano descrive l\'aspetto della costa e dei fari).')

sec('rilevare', head('Sapere dove sei','Dove sono rispetto al faro',SEA)+table(['Mi trovo…','…quindi rilevo il faro per','Ricorda'],[30,34,36],[
 ('a Nord','180°','Il rilevamento reciproco: ±180°'),
 ('a Nord-Est','225°','Sul Rlv 225° del faro sono a Nord-Est'),
 ('a Est','270°','Sul Rlv 270° sono a Est'),
 ('a Sud-Est','315°','Sul Rlv 135° sono a Nord-Ovest'),
 ('a Sud','360°','Sul Rlv 000° sono a Sud'),
 ('a Sud-Ovest','045°','Sul Rlv 045° sono a Sud-Ovest'),
 ('al traverso a dritta','polare 90°','Traverso = rilevamento polare 90°')],SEA,26),
 notes='Quiz 1.7.6-15, -20, -22, -25, -30, -31, -36 (sono a … del faro: lo rilevo per …), -16, -21, -26, -27, -28, -34, -37, -40, -42, -43 (sono sul Rlv … del faro: mi trovo a …), -17 e -33 (traverso = polare 90°), -8, -9, -10, -29 (rilevamento polare), -24 (rilevamento vero), -35 (grafometro), -44 (faro a prora con Rv Ovest: 270°). Regola: il rilevamento di un oggetto e la mia posizione rispetto a lui differiscono di 180°.')

sec('luoghi', head('Sapere dove sei','I luoghi di posizione',SEA)+table(['Luogo di posizione','Come lo ottieni','Con che cosa'],[28,44,28],[
 ('Retta di rilevamento','Rilevi un punto cospicuo','Bussola da rilevamento, grafometro'),
 ('Allineamento','Due punti uno dietro l\'altro: rilevamenti uguali o a 180°','Solo gli occhi'),
 ('Cerchio di distanza','Conosci la distanza da un punto','Radar, angolo verticale, tabelle'),
 ('Cerchio capace','Vedi due punti sotto lo stesso angolo','Differenza di due rilevamenti'),
 ('Batimetrica','Leggi il fondale','Ecoscandaglio')],SEA,28)
 +note('Il punto nave è l\'incrocio di almeno due luoghi. Con un rilevamento e una distanza dello stesso punto basta uno solo.',SEA,34),
 notes='Quiz 1.7.6-2 (i luoghi di posizione), -39 (definizione), -38 (la rosa dei venti non lo è), -1 e -46 (servono almeno due luoghi), -11 e -32 (allineamento), -14 (cerchio capace), -19 e -47 (rilevamento più distanza dallo stesso punto), -48 (due torri allineate: serve un altro luogo), -12 e -13 (squadrette e compasso). Punto nave per rilevamenti successivi: lezione 5 e lezione 10.')

# ============ PERICOLI ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{CHART}"/>'
b+=f'<path d="M0 0 L1092 0 L1092 110 Q880 150 700 120 Q520 90 360 140 Q200 190 0 150 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=f'<ellipse cx="460" cy="340" rx="95" ry="50" fill="#CFE8F3" stroke="#6FAFC6" stroke-width="3" stroke-dasharray="10 6"/>'
b+=''.join(f'<path d="M{x-12} {y} h24 M{x} {y-12} v24" stroke="{NAVY}" stroke-width="4"/>' for x,y in ((440,330),(480,350),(460,310)))
b+=tower(860,120,1.0)
b+=f'<path d="M860 40 L418 600 L1092 600 L1092 40 Z" fill="{GREEN}" fill-opacity="0.10"/>'+line(860,40,418,600,LRED,5)
b+=dpath('M520 600 Q720 520 1060 440',NAVY,5,False)+head_at(1060,440,-20,NAVY,20)
b+=topboat(640,560,110,-20,'#FFFFFF',NAVY,4)
b+=f'<path d="M0 230 Q200 270 360 220 Q520 170 700 200 Q880 230 1092 190" fill="none" stroke="#3C8FAE" stroke-width="4" stroke-dasharray="14 8"/>'
lbl=pill(X+380,Y+400,240,'secca · 2 m',NAVY)+pill(X+600,Y+170,300,'batimetrica dei 10 m',SEA)+pill(X+180,Y+470,330,'rilevamento limite 038°',LRED)
lbl+=lab(X+760,Y+330,320,'faro a meno di 038°: sei al sicuro',GREEN_S,24,800)+lab(X+880,Y+40,160,'faro',NAVY,24,900)
txt=(item(1,SEA,'Una batimetrica di sicurezza','Scegli la profondità sotto cui non scendere e controlla l\'ecoscandaglio.')
     +item(2,LRED,'Un rilevamento limite','Traccia sulla carta la retta dal faro che passa fuori dal pericolo: finché il rilevamento resta dal lato giusto, sei lontano.')
     +item(3,PURPLE,'Un allineamento','Due punti allineati indicano spesso il passaggio sicuro in un canale.')
     +item(4,NAVY,'Largo dai capi','Stai al largo di punte e secche: il margine è la tua sicurezza.'))
sec('pericoli', head('Sapere dove sei','Stare lontani dai pericoli',SEA), pinned=svgp(X,Y,W,Hh,b,'Stralcio di carta con una secca davanti alla costa, la batimetrica dei 10 metri e una retta rossa di rilevamento limite dal faro; la rotta della barca resta nel lato sicuro, oltre la secca')+lbl+pcol(txt,532,16),
 notes='Tecniche di uso comune nella navigazione costiera. Quiz collegati: 1.7.2-8 (batimetriche), 1.7.6-2 (la batimetrica è un luogo di posizione), 1.7.6-11 e -32 (allineamenti), 1.7.5-4 (criterio di sicurezza: tenersi lontani dai pericoli idrografici e meteorologici), 1.3.6-4 (incaglio per punto nave impreciso). Il rilevamento limite si misura con la bussola da rilevamento e si corregge con declinazione e deviazione come ogni altro rilevamento.')
X=700

sec('gps', head('Sapere dove sei','Il GPS vicino alla costa',SEA)+grid([
 ('Che cosa dà','Punto nave in ogni istante con un errore di pochi metri, rotta e velocità sul fondo, distanza e tempo al waypoint.',SEA),
 ('I waypoint','Mettili almeno 500 m fuori dai fanali del porto, con la rotta lontana da secche e ostacoli.',CORAL),
 ('Rotte spezzate','Molti GPS vanno dritti al waypoint e ignorano la costa: la rotta la spezzi tu, controllando la carta.',PURPLE),
 ('Il tasto MOB','Segna il punto di caduta dell\'uomo a mare e dà la rotta per tornarci. Verifica di saperlo usare.',LRED),
 ('Quando è obbligatorio','Oltre 12 miglia dalla costa. Sottocosta resta utilissimo.',BLUE),
 ('Non basta','Il GPS non vede gli scogli: occhi fuori, carta e scandaglio.',GREEN)],3,32,26),
 notes='Quiz 1.7.3-2, -3, -5, -6, -13 (che cosa dà il GPS: pochi metri di errore), -8 (waypoint almeno 500 m fuori dai fanali), -11 (rotte spezzate: il GPS non tiene conto degli ostacoli), -1, -9, -10 (MOB), -7 (obbligatorio oltre 12 miglia), -12 (navigazione per waypoint), -4 (fissi o portatili).')

quiz_slide('quizB','Verifica · sapere dove sei',['1.7.6-11','1.7.6-46','1.7.3-8'],False)
quiz_slide('quizBr','Verifica · sapere dove sei',['1.7.6-11','1.7.6-46','1.7.3-8'],True)

# ============ VENTO E COSTA ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.2"/>'
b+=f'<path d="M0 0 L380 0 Q420 160 360 300 Q300 460 380 620 L0 620 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=f'<path d="M1092 0 L900 0 Q860 200 940 330 Q1000 460 920 620 L1092 620 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=''.join(windarrow(x,y,110,GREY,0) for x,y in ((150,120),(150,300),(150,480),(560,200),(560,420)))
b+=f'<path d="M380 60 Q420 300 390 580 L480 580 Q500 300 470 60 Z" fill="#FFFFFF" fill-opacity="0.45"/>'
b+=topboat(430,330,110,-90,'#FFFFFF',NAVY,4)
for i in range(6): b+=f'<path d="M{800+(i%2)*20} {90+i*90} q30 -20 60 0 t60 0" fill="none" stroke="#FFFFFF" stroke-width="6"/>'
b+=topboat(800,330,110,-90,'#FFFFFF',NAVY,4)+line(740,270,860,390,LRED,8)+line(860,270,740,390,LRED,8)
lbl=pill(X+60,Y+30,280,'vento da terra',NAVY)+pill(X+380,Y+520,300,'ridosso: mare calmo',GREEN)+pill(X+640,Y+520,380,'costa sottovento: pericolo',LRED)
txt=(item(1,GREEN,'Sopravento: il ridosso','Vicino alla costa da cui arriva il vento il mare è calmo. Con una tempesta da terra, cerca il ridosso sotto costa.')
     +item(2,LRED,'Sottovento: lontano','Il vento e le onde ti spingono sugli scogli. Con la tempesta dal mare, stai al largo e mettiti alla cappa.')
     +item(3,PURPLE,'Onde che frangono','Sul basso fondale l\'onda frange quando il fondo è meno del doppio della sua altezza. Vicino ai moli c\'è la risacca.'))
sec('vento', head('Il mare vicino a riva','Costa sopravento e sottovento',PURPLE)+col(txt,520,22), pinned=svgp(X,Y,W,Hh,b,'Vento da sinistra a destra tra due coste: sotto la costa di sinistra, sopravento, la barca è al ridosso con mare calmo; vicino alla costa di destra, sottovento, le onde spingono la barca verso terra, barrata in rosso')+lbl,
 notes='Quiz 1.3.8-3 (tempesta da terra: verso la costa, dove il moto ondoso è attenuato), -4 e -19 (tempesta dal mare: alla cappa), 1.6.2-43 (l\'onda frange quando il fondale è meno del doppio dell\'altezza), -42 (o quando la ripidità supera 1/7), 1.3.8-20 (risacca: onde di riflusso), 1.3.8-18 e -21 (ancora galleggiante con costa sottovento vicina), 1.7.8-5 (venti di traversìa nel Portolano).')

sec('notte', head('Il mare vicino a riva','Di notte e nella nebbia',PURPLE)+grid([
 ('I fari','Si riconoscono dalla caratteristica: tipo, colore, periodo. Controlla sull\'Elenco dei fari.',CORAL),
 ('Settore rosso','Si naviga, ma segnala un pericolo: esci dal settore verso il bianco.',LRED),
 ('I fanali di bordo','Di notte si accendono sempre. Per navigare di notte oltre 1 miglio vanno tenuti a bordo come dotazione.',SEA),
 ('Nella nebbia','Rallenta, accendi i fanali, emetti i segnali sonori prescritti.',PURPLE),
 ('Costa vicina','L\'acqua che cambia colore e il rumore dei frangenti: sei troppo vicino.',BLUE),
 ('Fidati del fondo','Con poca visibilità l\'ecoscandaglio e la batimetrica sono il tuo luogo di posizione.',GREEN)],3,32,26),
 notes='Quiz 1.5.3-56 e -77 (caratteristica del faro), -85 (settore rosso), 1.7.8-6 (Elenco dei fari), 1.3.3-8 (fanali di notte oltre 1 miglio), 1.3.8-17 (visibilità scarsa: rallentare, fanali, segnali), -6 (nebbia: colore dell\'acqua e frangenti), 1.7.6-2 (batimetrica). Appendice F per le luci dei segnali.')

sec('regole', head('Il mare vicino a riva','Le regole vicino a riva',PURPLE)+table(['Regola','Distanza'],[52,48],[
 ('Circolare, sostare, ancorare','Oltre 200 m dalle spiagge'),
 ('Limite della balneazione','Gavitelli rossi ogni 50 m'),
 ('Corridoi di lancio','Gavitelli gialli o arancioni fino a 250 m'),
 ('Boa di un subacqueo','Almeno 100 m'),
 ('Remi, tavole a vela, moto d\'acqua, vele fino a 4 m²','Entro 1 miglio dalla costa'),
 ('Moto d\'acqua oltre la velocità minima','Oltre 1000 m (500 m dalle coste a picco)'),
 ('Velocità e zone vietate','Le decide l\'ordinanza della Capitaneria')],PURPLE,28),
 notes='Quiz 1.4.2-4, -5, -6, -7, -11, -17 (spiagge, balneazione, corridoi), -2, -12, -15 (subacquei), -20, -21, -23, -24, 1.8.1-53 (entro 1 miglio), 1.8.1-122 (moto d\'acqua), 1.4.2-3 e -25 (ordinanze, interdizioni), -10 (velocità: da 414 a 2.066 euro). Appendice G per tutte le tabelle normative.')

sec('incaglio', head('Il mare vicino a riva','Se si tocca il fondo',PURPLE)+steps([
 ('Ferma e guarda','Motore in folle. Tutti bene? Entra acqua? Controlla la sentina.',LRED),
 ('Valuta','Tipo di fondo, danno subito, manovra possibile per la barca e il luogo.',ORANGE),
 ('Disincaglia','Indietro con prudenza, alleggerisci, oppure aspetta l\'alta marea.',SEA),
 ('Se serve','Incaglio volontario: portarsi sul basso per non affondare per una falla.',PURPLE)])
 +note('Un incaglio si previene: punto nave preciso e margine dai bassi fondali.',PURPLE,36),
 notes='Quiz 1.3.6-3 (fattori per il disincaglio: fondale, avaria, manovra), -8 (attendere l\'alta marea), -2 (incaglio volontario per evitare il naufragio), -4 (causa frequente: punto nave impreciso vicino alla costa), 1.8.1-108 (l\'incaglio è un evento straordinario: denuncia entro 3 giorni). Nel Mediterraneo la marea è piccola: l\'alta marea aiuta poco, tranne in alcune zone come l\'Alto Adriatico.')

quiz_slide('quizC','Verifica · il mare vicino a riva',['1.7.8-5','1.6.2-43','1.3.8-6'],False)
quiz_slide('quizCr','Verifica · il mare vicino a riva',['1.7.8-5','1.6.2-43','1.3.8-6'],True)

closing(['Sottocosta servono carte a grande scala e il Portolano: 1:50.000 è più grande di 1:100.000',
         'Il punto nave è l\'incrocio di almeno due luoghi di posizione',
         'Sono a Nord del faro? Lo rilevo per 180°: il reciproco è ±180°',
         'Batimetrica, rilevamento limite e allineamenti tengono lontani i pericoli',
         'Costa sottovento: al largo. Costa sopravento: ridosso'],
 'Buon vento, e occhio al fondo!','Appendice I · Navigare sottocosta')
write_deck(OUT,'Appendice I · Navigare sottocosta',ORDER,
 {"s1":{"description":"Preparare: carte, simboli, pubblicazioni","start":"cover"},
  "s2":{"description":"Sapere dove sei: punti cospicui, rilevamenti, pericoli, GPS","start":"cospicui"},
  "s3":{"description":"Il mare vicino a riva: vento, notte, regole, incaglio","start":"vento"}})
