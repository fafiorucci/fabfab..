"""Appendice L: l'ancoraggio (quiz 1.4.3, 1.4.2, 1.8.2, 1.5.2)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
from anc_draw import anatomy, danforth, cqr, rocna, grappino, ombrello
OUT=SP+'/deck/project'
ORDER=['cover','indice','parti','tipi','fondo','quizA','quizAr',
       'posto','calumo','manovra','tenuta','quizB','quizBr',
       'fonda','grippia','ventoforte','salpare','regole','quizC','quizCr','errori','chiusura']
EB='Appendice L · L\'ancoraggio'
LB.ICON_T.update({'Indice':'book','Com\'è fatta l\'ancora':'anchor','Quale ancora':'anchor','Il fondo giusto':'map',
 'Scegliere il posto':'map','Quanta catena':'anchor','Dare fondo, passo passo':'anchor','Tiene o ara?':'compass',
 'Modi di stare alla fonda':'anchor','La grippia':'anchor','Con vento forte':'wind','Salpare':'anchor',
 'Dove, e con quali segnali':'flag','Gli errori più comuni':'star'})

cover_app('L','L\'ancoraggio','Ancore e fondali, scegliere il posto, il calumo, la manovra, la tenuta, vento forte, grippia, salpare e regole',
 'Appendice L al corso. Ripasso dell\'ancoraggio: tutti i quiz ufficiali 1.4.3 (ancore e ancoraggio) e quelli collegati di 1.4.2 (distanze), 1.8.2 (aree marine protette), 1.5.2 (segnali alla fonda). Collegata alla lezione 4 e all\'appendice E.')
index_slide(EB,[('L\'ancora','Parti, tipi, fondali',['parti','tipi','fondo','quizA','quizAr'],CORAL),
 ('Dare fondo','Il posto, il calumo, la manovra, la tenuta',['posto','calumo','manovra','tenuta','quizB','quizBr'],SEA),
 ('Stare alla fonda','Ruota e afforcata, grippia, vento forte, salpare, regole',['fonda','grippia','ventoforte','salpare','regole','quizC','quizCr'],PURPLE),
 ('Per finire','Gli errori più comuni',['errori'],BLUE)],ORDER,
 'Un buon ancoraggio si decide prima di arrivare, sulla carta.',
 'Appendice di ripasso che raccoglie tutto l\'ancoraggio: dall\'attrezzatura alla scelta del posto, alla manovra, al controllo, fino alle regole e ai segnali.')

# ============ PARTI ============
X=128
b=anatomy()+arrow(420,60,528,76,INK,3)+arrow(300,190,398,150,INK,3)+arrow(700,300,580,300,INK,3)+arrow(200,420,330,392,INK,3)+arrow(240,300,300,332,INK,3)+arrow(760,580,584,536,INK,3)
lbl=lab(X+250,Y+40,170,'Cicala',INK,24,800,'right')+lab(X+130,Y+172,170,'Ceppo',INK,24,800,'right')+lab(X+712,Y+284,200,'Fuso',INK,24,800)+lab(X+40,Y+404,160,'Marra',CORAL,24,900,'right')+lab(X+60,Y+282,180,'Patta',CORAL,24,800,'right')+lab(X+770,Y+560,200,'Diamante',INK,24,900)+lab(X+800,Y+250,260,'catena: maglie ellittiche',NAVY,24,800)
txt=(item(1,CORAL,'Marre','I bracci che fanno presa sul fondo.')
     +item(2,SUN,'Diamante','La parte in basso, al centro delle marre: lì si lega la grippia.')
     +item(3,SEA,'Peso e forma','La tenuta dipende dal peso e in parte dalla forma. Barca di 10 m: 15–20 kg.')
     +item(4,PURPLE,'Barbotin','La ruota del verricello con l\'impronta della catena: non la fa slittare.'))
sec('parti', head('L\'ancora','Com\'è fatta l\'ancora',CORAL), pinned=svgp(X,Y,W,Hh,b,'Ancora classica con cicala, ceppo, fuso, marre con le patte e diamante, e catena a maglie ellittiche')+lbl+pcol(txt,532,18),
 notes='Quiz 1.4.3-16 e -25 (marre), -19 e -33 (diamante), -1 (tenuta: peso e forma), -21 (10 m: 15-20 kg), -9 (maglie ellittiche), -10 (barbotin), -18 (l\'ancora deve restare orizzontale sul fondo). Disegno dell\'ancora ammiragliato, come nella lezione 4.')
X=700

TP=[(danforth(),'Danforth','Sabbia e fango',CORAL),(cqr(),'CQR e Delta','Tutti i fondali',SEA),(rocna(),'Rocna, Mantus, Ultra','Tutti i fondali · roll-bar',PURPLE),
    (grappino(),'Grappino','Piccole unità',BLUE)]
cc=''.join(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:10px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:20px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)">{svgi(310,190,s,"Disegno ancora "+t,dw=270,dh=166)}{h3(t,30,c)}{p(d,26,INK,700,1.3)}</div>' for s,t,d,c in TP)
sec('tipi', head('L\'ancora','Quale ancora',CORAL)+f'<div style="display:flex; gap:18px; align-items:stretch">{cc}</div>'
    +table(['Ancora','Com\'è','Quando'],[22,44,34],[('Danforth','Due marre piatte e mobili','Ottima su sabbia e fango'),('CQR, Delta','A vomere d\'aratro','Tutti i fondali'),('Rocna','Una marra concava fissa e il roll-bar: non resta rovesciata','Tutti i fondali'),('Grappino','Quattro marre fisse, piccolo','Solo piccole unità'),('A ombrello','Marre richiudibili','Battelli gonfiabili')],CORAL,24),
 gap=24, notes='Quiz 1.4.3-39 (Danforth su sabbia e fango), -40 (CQR e Delta per tutti i fondali), -49 (Mantus e Ultra, tenuta dinamica), -52 (Rocna con roll-bar), -7 e -28 (grappino), -6 (ombrello per battelli gonfiabili). Il quiz 1.4.3-8 sulla Bruce è oscurato.')

sec('fondo', head('L\'ancora','Il fondo giusto',CORAL)+table(['Sulla carta','Fondo','Che cosa aspettarsi'],[18,22,60],[
 ('s','Sabbia','Buona tenuta per quasi tutte le ancore'),
 ('f','Fango','Buona tenuta, soprattutto con la Danforth'),
 ('r','Roccia','L\'ancora non entra o si incastra: usa la grippia, o scegli un altro posto'),
 ('—','Relitti, cavi, condotte','L\'ancora si incattivisce; e sui cavi segnalati non si ancora')],CORAL,28)
 +note('La natura del fondo si legge sulla carta nautica, accanto agli scandagli.',CORAL,36),
 notes='Quiz 1.7.2-15 e -29 (natura del fondo sulla carta), -38 (r roccia), -39 (f fango), 1.4.3-13 (fondale roccioso o con relitti: grippia e grippiale), 1.5.3-42 (i segnali speciali indicano cavi e condotte). La sigla s per la sabbia è quella delle carte italiane.')

quiz_slide('quizA','Verifica · l\'ancora',['1.4.3-19','1.4.3-39','1.4.3-21'],False)
quiz_slide('quizAr','Verifica · l\'ancora',['1.4.3-19','1.4.3-39','1.4.3-21'],True)

# ============ IL POSTO ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.22"/>'
b+=f'<path d="M0 0 L1092 0 L1092 260 Q980 180 860 150 Q700 110 560 150 Q400 200 300 330 Q220 440 0 470 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="4"/>'
b+=''.join(windarrow(x,y,90,GREY,40) for x,y in ((60,40),(180,20)))
for cx,cy,r in ((640,300,120),(880,360,120)):
    b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{SEA}" stroke-width="3" stroke-dasharray="10 8"/>'+anchor_icon(cx,cy,0.7,NAVY)+topboat(cx+60,cy+70,90,-130,'#FFFFFF',NAVY,3)
b+=topboat(470,300,90,-130,'#FFFFFF',NAVY,3,0.5,False)+f'<path d="M430 260 L510 340 M510 260 L430 340" stroke="{LRED}" stroke-width="7"/>'
b+=f'<circle cx="760" cy="520" r="120" fill="none" stroke="{GREEN}" stroke-width="5" stroke-dasharray="10 8"/>'+anchor_icon(760,520,0.8,GREEN)+topboat(820,590,90,-130,'#FFFFFF',GREEN,4)
lbl=pill(X+120,Y+130,260,'vento da terra: ridosso',NAVY)+pill(X+340,Y+360,300,'troppo vicino: no',LRED)+pill(X+620,Y+440,340,'qui: spazio per girare',GREEN)
txt=(item(1,SEA,'Riparo','Vento da terra: sottocosta il mare è calmo. Guarda il bollettino: se il vento gira?')
     +item(2,GREEN,'Spazio per la ruota','Tutta la barca deve poter girare attorno all\'ancora senza toccare le altre.')
     +item(3,CORAL,'Il fondale','Profondità giusta e fondo che tiene; niente cavi o relitti.')
     +item(4,PURPLE,'Niente divieti','Oltre 200 m dalle spiagge; non nella zona A delle aree protette né nei campi boe.'))
sec('posto', head('Dare fondo','Scegliere il posto',SEA)+col(txt,520,18), pinned=svgp(X,Y,W,Hh,b,'Rada vista dall\'alto con il vento da terra: due barche alla fonda con i loro cerchi di rotazione; una barca che vuole ancorarsi troppo vicina, barrata in rosso; il posto giusto più al largo con spazio per girare')+lbl,
 notes='Quiz 1.4.3-2 (divieti e meteo prima di dare fondo), -4 (alla ruota serve spazio libero), -45 (in una rada affollata: la barca con spazio per la ruota), -44 e -53 (figure), -41 e -48 (in baia più unità a murata: sconsigliato), 1.4.2-4 (ancorarsi oltre 200 m dalle spiagge), 1.8.2-49, -55, -59 (aree marine protette e campi boe), 1.3.8-3 (con vento da terra, il ridosso sotto costa).')

sec('calumo', head('Dare fondo','Quanta catena',SEA)+bignums([('3×','il minimo: tre volte il fondale',SEA),('3–5×','di più con vento e mare',PURPLE),('5 m → 15 m','con mare calmo',CORAL),('9 m → 27 m','con mare calmo',BLUE),('16 m → 48 m','con mare calmo',GREEN),('orizzontale','così deve restare l\'ancora sul fondo',ORANGE)],3)
 +note('Il calumo è la lunghezza di cima o catena filata: più è lungo, più l\'ancora tira in orizzontale.',SEA,34),
 gap=28, notes='Quiz 1.4.3-34 (calumo), -50 (minimo 3 volte), -3 e -32 (da 3 a 5 volte secondo il tempo), -27, -29, -30 (esempi: 16 → 48 m, 9 → 27 m, 5 → 15 m), -18 (ancora orizzontale). Il quiz -20 sul calumo è oscurato.')

sec('manovra', head('Dare fondo','Dare fondo, passo passo',SEA)+steps([
 ('Arriva','Piano, con la prua al vento o alla corrente, sul punto scelto.',CORAL),
 ('Fermati','Quando l\'abbrivio è finito, cala l\'ancora; un leggero colpo indietro.',SEA),
 ('Fila','Indietreggia piano filando catena fino al calumo giusto.',PURPLE),
 ('Fa testa','Un colpo di retro: se la catena si tende e resta ferma, l\'ancora ha fatto presa.',BLUE),
 ('Controlla','Prendi due rilevamenti a terra e segnali: li ripeterai.',GREEN)],24)
 +note('Mai calare l\'ancora con la barca che va avanti: la catena finisce sopra l\'ancora.',SEA,34),
 notes='Quiz 1.4.3-12 e -43 (prua al vento o alla corrente, a abbrivio esaurito si cala, leggero colpo indietro), -42 (indietreggiare filando il calumo), -17 e -31 (fa testa), -15 (controllo con rilevamenti successivi o punti nave). Manovra all\'esame pratico: appendice E.')

# ============ TENUTA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{CHART}"/><path d="M0 0 L1092 0 L1092 130 Q800 180 546 120 Q300 60 0 140 Z" fill="{LAND}" stroke="{LAND_S}" stroke-width="3"/>'
b+=tower(200,120,0.9)+church(900,140,0.9)
P=(560,430)
b+=dash(P[0],P[1],200,60,SEA,4)+dash(P[0],P[1],900,40,CORAL,4)
b+=f'<circle cx="{P[0]}" cy="{P[1]}" r="120" fill="{PURPLE}" fill-opacity="0.08" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="10 8"/>'
b+=anchor_icon(P[0],P[1]-40,0.7,NAVY)+topboat(P[0]+40,P[1]+60,110,110,'#FFFFFF',NAVY,4)
b+=topboat(P[0]+190,P[1]+100,110,110,'#FFFFFF',LRED,3,0.6,False)+arrow(P[0]+80,P[1]+80,P[0]+150,P[1]+100,LRED,5,16)
lbl=pill(X+250,Y+250,240,'Rlv faro 312°',SEA)+pill(X+700,Y+200,280,'Rlv campanile 048°',CORAL)+pill(X+60,Y+470,360,'allarme di ancoraggio del GPS',PURPLE)+lab(X+700,Y+560,360,'i rilevamenti cambiano: ara!',LRED,24,900)
txt=(item(1,SEA,'Rilevamenti','Appena ancorato scrivi due rilevamenti a terra. Ripetili: se cambiano, l\'ancora ara.')
     +item(2,PURPLE,'GPS','I punti nave successivi, o l\'allarme di ancoraggio, dicono se ti sposti.')
     +item(3,CORAL,'Le parole','Fa testa: ha preso. Ara: non tiene e striscia. Speda: si stacca dal fondo.')
     +item(4,LRED,'Se ara','Fila altra catena o salpa e ripeti la manovra.'))
sec('tenuta', head('Dare fondo','Tiene o ara?',SEA), pinned=svgp(X,Y,W,Hh,b,'Barca alla fonda con due rilevamenti a terra, uno al faro e uno al campanile, e il cerchio di allarme del GPS; una seconda posizione sottovento, fuori dal cerchio, mostra una barca che sta arando')+lbl+pcol(txt,532,18),
 notes='Quiz 1.4.3-15 (rilevamenti successivi di punti cospicui o punti nave successivi), -17 e -31 (fa testa), -24 (ara), -37 (speda). L\'allarme di ancoraggio è una funzione comune dei GPS e dei plotter: suona se la barca esce da un cerchio impostato. I rilevamenti nel disegno sono di esempio.')
X=700

quiz_slide('quizB','Verifica · dare fondo',['1.4.3-3','1.4.3-24','1.4.3-43'],False)
quiz_slide('quizBr','Verifica · dare fondo',['1.4.3-3','1.4.3-24','1.4.3-43'],True)

sec('fonda', head('Stare alla fonda','Modi di stare alla fonda',PURPLE)+table(['Modo','Come','Quando'],[22,44,34],[
 ('Alla ruota','Una sola ancora di prua: la barca gira di 360°','Dove c\'è spazio libero attorno'),
 ('Afforcata','Due ancore con i calumi aperti di circa 45°','Il campo di giro diventa un\'ellisse, più piccolo'),
 ('Appennellata','Una seconda ancora legata al diamante della prima con 4–6 m di catena','Per tenere meglio in condizioni difficili'),
 ('Nei fiumi','Due ancore a 180°, nella direzione della corrente','Con corrente che cambia verso'),
 ('Mai','Alla ruota, un\'ancora in più da poppa','La barca non gira più e prende il vento di traverso')],PURPLE,26),
 notes='Quiz 1.4.3-35 e -36 (alla ruota), -4 (spazio), -22 (afforcata a 45°), -11 (campo di giro ellittico), -38 (appennellate: pennello con 4-6 m di catena), -5 (nei fiumi), -23 (alla ruota non si dà ancora da poppa).')

# ============ GRIPPIA ============
b=f'<rect x="0" y="0" width="1092" height="160" fill="{SKY}"/><rect x="0" y="160" width="1092" height="460" fill="{WATER}" fill-opacity="0.2"/>'+line(0,160,1092,160,SEA,3)
b+=f'<path d="M0 560 Q200 540 360 560 L420 470 Q470 430 540 470 L600 560 Q800 548 1092 560 L1092 620 L0 620 Z" fill="#8C7B64" stroke="{NAVY}" stroke-width="3"/>'
b+=profile(40,160,300)
b+=f'<path d="M330 128 Q420 200 500 360 Q540 440 560 500" fill="none" stroke="{NAVY}" stroke-width="6" stroke-dasharray="3 5"/>'
b+=f'<g transform="translate(575 520) rotate(160)">{anchor_icon(0,0,1.3,NAVY)}</g>'
b+=f'<path d="M565 548 Q720 400 760 160" fill="none" stroke="{CORAL}" stroke-width="5"/>'+f'<ellipse cx="760" cy="156" rx="30" ry="18" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/>'
b+=arrow(820,300,780,180,CORAL,5,16)
lbl=pill(X+800,Y+100,240,'gavitello',ORANGE)+pill(X+680,Y+330,200,'grippia',CORAL)+lab(X+300,Y+584,500,'ancora incastrata sotto la roccia',INK,24,800,'center')
txt=(item(1,CORAL,'Che cos\'è','Una cima sottile legata al diamante dell\'ancora, con un gavitello in superficie.')
     +item(2,SEA,'Quando','Su fondali rocciosi o con relitti, dove l\'ancora può incastrarsi.')
     +item(3,PURPLE,'Come si usa','Se l\'ancora si incattivisce, tiri la grippia: l\'ancora esce al contrario, dal diamante.'))
sec('grippia', head('Stare alla fonda','La grippia',PURPLE)+col(txt,520,22), pinned=svgp(X,Y,W,Hh,b,'Sezione: la barca alla fonda, la catena che scende a un\'ancora incastrata sotto una roccia; dal diamante dell\'ancora sale una cima sottile, la grippia, fino a un gavitello arancione in superficie')+lbl,
 notes='Quiz 1.4.3-13 (grippia e grippiale su fondali rocciosi o con relitti), -14 (cima sottile legata al diamante, con un gavitello), -26 (serve a facilitare il recupero). Il gavitello segnala anche agli altri dove si trova l\'ancora.')

sec('ventoforte', head('Stare alla fonda','Con vento forte',PURPLE)+grid([
 ('Più catena','Fila fino a 5 volte il fondale; in fretta, allentando il barbotin.',PURPLE),
 ('Due ancore','Afforcati o appennellati tengono meglio in condizioni difficili.',SEA),
 ('Controlla spesso','Rilevamenti e GPS, anche di notte: qualcuno resta di guardia.',CORAL),
 ('Pronto a partire','Motore pronto, rotta di uscita decisa, se l\'ancora ara.',LRED),
 ('Con la poppa in banchina','Dai fondo leggermente sopravento al posto barca.',BLUE),
 ('Ridosso sbagliato','Se il vento gira e ti mette sottovento alla costa, salpa per tempo.',ORANGE)],3,32,26),
 notes='Quiz 1.4.3-46 (vento forte: filare velocemente allentando il barbotin), -32 (calumo da 3 a 5 volte secondo le condizioni), -11 e -38 (afforcata e appennellata), -47 (ormeggio di poppa con ancora: dare fondo sopravento al posto), 1.3.8-3 (tempesta da terra: ridosso). Costa sottovento: appendice I.')

sec('salpare', head('Stare alla fonda','Salpare',PURPLE)+steps([
 ('Avanti adagio','Vai verso l\'ancora mentre a prua si recupera la catena.',CORAL),
 ('A picco','Catena verticale: sei sopra l\'ancora.',SEA),
 ('Spedare','Un leggero colpo avanti toglie tensione e stacca l\'ancora.',PURPLE),
 ('Incattivita?','Girale attorno, o tira la grippia.',BLUE),
 ('A posto','Ancora nel musone e bloccata prima di navigare.',GREEN)],24)
 +note('Il verricello recupera, il motore aiuta: non si tira la catena con il motore.',PURPLE,36),
 notes='Quiz 1.4.3-51 (per salpare: leggero colpo avanti per togliere tensione), -37 (l\'ancora speda quando si stacca), -26 (grippia per il recupero), -10 (barbotin).')

sec('regole', head('Stare alla fonda','Dove, e con quali segnali',PURPLE)+table(['Regola','Che cosa dice'],[36,64],[
 ('Spiagge','Si ancora oltre 200 m dalla riva'),
 ('Aree marine protette','Zona A: niente ancoraggio; nei campi boe mai'),
 ('Canali e rotte','Non ancorare in un canale stretto'),
 ('Di giorno','Pallone nero a prua (unità oltre 7 m)'),
 ('Di notte','Fanale bianco visibile tutto intorno'),
 ('Nella nebbia, oltre 20 m','Campana rapida per 5 secondi, almeno ogni minuto')],PURPLE,28),
 notes='Quiz 1.4.2-4 (200 m), 1.8.2-49, -55, -59 (aree marine protette), 1.5.2-35 (alla fonda con nebbia, oltre 20 m: campana per 5 secondi a intervalli non superiori a un minuto). Il divieto di ancorare nei canali stretti è della regola 9 del COLREG; il pallone nero e il fanale bianco alla fonda della regola 30 (lezione 5); il pallone per le unità oltre 7 m è nella tabella del DM 133/2024.')

quiz_slide('quizC','Verifica · stare alla fonda',['1.4.3-22','1.4.3-26','1.4.3-51'],False)
quiz_slide('quizCr','Verifica · stare alla fonda',['1.4.3-22','1.4.3-26','1.4.3-51'],True)

sec('errori', head('Per finire','Gli errori più comuni',BLUE)+grid([
 ('Poca catena','Sotto 3 volte il fondale l\'ancora tira verso l\'alto e ara.',CORAL),
 ('Barca in moto','Calare con abbrivio avanti: la catena finisce sopra l\'ancora.',SEA),
 ('Troppo vicino','Il tuo cerchio tocca quello degli altri quando il vento gira.',PURPLE),
 ('Nessun controllo','Mai ancorare senza prendere rilevamenti o impostare l\'allarme.',BLUE),
 ('Fondo sbagliato','Roccia senza grippia, o posidonia e divieti ignorati.',GREEN),
 ('Il meteo','Il ridosso di oggi può diventare la costa sottovento di stanotte.',ORANGE)],3,32,26),
 notes='Riepilogo dei quiz 1.4.3 in forma di errori da evitare. La posidonia è una pianta marina protetta: in molte aree l\'ancoraggio sulle praterie è vietato dalle ordinanze o dai regolamenti delle aree protette.')

closing(['Danforth su sabbia e fango; CQR, Delta, Rocna e Mantus su tutti i fondali',
         'Prua al vento, a abbrivio finito si cala, poi si fila indietreggiando',
         'Calumo da 3 a 5 volte il fondale: con 9 m almeno 27 m',
         'Fa testa: tiene. Ara: non tiene. Controlla con i rilevamenti',
         'Grippia sui fondi rocciosi; per salpare un leggero colpo avanti'],
 'Buon vento, e buona fonda!','Appendice L · L\'ancoraggio')
write_deck(OUT,'Appendice L · L\'ancoraggio',ORDER,
 {"s1":{"description":"L'ancora: parti, tipi, fondali","start":"cover"},
  "s2":{"description":"Dare fondo: posto, calumo, manovra, tenuta","start":"posto"},
  "s3":{"description":"Stare alla fonda: modi, grippia, vento forte, salpare, regole","start":"fonda"},
  "s4":{"description":"Errori comuni e chiusura","start":"errori"}})
