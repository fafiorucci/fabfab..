"""Appendice K: il soccorso in mare (quiz 1.3.2, 1.3.5, 1.3.6, 1.3.7, 1.3.8, 1.3.9, 1.3.3, 1.8.1)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
ORDER=['cover','indice','chi','prime','quizA','quizAr',
       'falla','incendio','fuoco','collisione','uomoamare','quizB','quizBr',
       'segnali','chiamare','abbandono','quizC','quizCr',
       'prevenire','alcol','scenari','scenarir','chiusura']
EB='Appendice K · Il soccorso in mare'
LB.ICON_T.update({'Indice':'book','Chi coordina il soccorso':'lifebuoy','I primi minuti di un\'emergenza':'lifebuoy','La falla':'hull',
 'Incendio a bordo':'fuel','Quale estintore, dove':'fuel','Collisione e incaglio':'hull','Uomo a mare':'lifebuoy','I segnali di soccorso':'flag',
 'Chiamare aiuto':'lantern','Abbandonare la barca':'lifebuoy','Prevenire è soccorrere':'check','Alcol, droghe e farmaci':'check',
 'Esercitazione: che cosa fai?':'star','Esercitazione: le risposte':'check'})

cover_app('K','Il soccorso in mare','Chi coordina, i primi minuti, falla, incendio, collisione, uomo a mare, segnali, chiamata di soccorso, abbandono e prevenzione',
 'Appendice K al corso. Ripasso delle emergenze: quiz ufficiali 1.3.5-1.3.9 (sinistri, abbandono, soccorso, cattivo tempo, radio), 1.3.3 (segnali), 1.3.2 (alcol e droghe), 1.8.1 (obblighi del comandante). Collegata alle lezioni 6 e 9 e alle appendici E e H.')
index_slide(EB,[('Il sistema','Chi coordina, i primi minuti',['chi','prime','quizA','quizAr'],CORAL),
 ('Le emergenze','Falla, incendio, collisione, uomo a mare',['falla','incendio','fuoco','collisione','uomoamare','quizB','quizBr'],LRED),
 ('Chiedere aiuto','Segnali, radio, abbandono',['segnali','chiamare','abbandono','quizC','quizCr'],PURPLE),
 ('Prima e dopo','Prevenzione, alcol, esercitazione',['prevenire','alcol','scenari','scenarir'],SEA)],ORDER,
 'In ogni emergenza il primo ordine è sempre lo stesso: giubbotti a tutti.',
 'Appendice di ripasso delle emergenze. Per ogni situazione: che cosa fare subito, chi avvisare, come chiedere aiuto. Le procedure radio complete sono nell\'appendice H.')

sec('chi', head('Il sistema','Chi coordina il soccorso',CORAL)+grid([
 ('Soccorso marittimo','Tutte le attività per cercare e salvare la vita umana in mare.',CORAL),
 ('Chi coordina','Il Comando generale del Corpo delle Capitanerie di porto, con le Capitanerie sul territorio.',SEA),
 ('1530','Il numero di emergenza della Guardia Costiera, dal telefono.',LRED),
 ('Canale 16 e DSC','Dalla radio: MAYDAY, PAN PAN o il pulsante DISTRESS.',PURPLE),
 ('CIRM','Il Centro Internazionale Radio Medico: consigli medici per un infortunio grave a bordo.',BLUE),
 ('Anche tu','Devi soccorrere chi è in pericolo di vita, se non metti in pericolo la tua barca. In porto o vicino l\'Autorità marittima può chiamarti.',GREEN)],3,32,26),
 notes='Quiz 1.3.7-7 (soccorso marittimo), -8 (coordinamento: Comando generale delle Capitanerie di porto), -9 (unità in porto o nelle vicinanze), -10 e 1.8.1-7, -9 (obbligo di assistenza), 1.8.1-10 (omissione: reclusione fino a 2 anni), 1.3.8-25 (1530), 1.3.2.113 (CIRM), 1.3.9-8 e 1.3.8-7 (canale 16 e DSC).')

sec('prime', head('Il sistema','I primi minuti di un\'emergenza',CORAL)+steps([
 ('Persone','Giubbotti a tutti. Conta chi c\'è a bordo e chi è ferito.',LRED),
 ('Valuta','Che cosa succede e quanto è grave: si può risolvere a bordo?',ORANGE),
 ('Agisci','Pompa, estintore, manovra: la procedura per quel pericolo.',SEA),
 ('Chiama','Se il pericolo è grave: MAYDAY sul 16 o DSC; altrimenti PAN PAN.',PURPLE),
 ('Prepara','Zattera, grab bag, segnali: pronti se la situazione peggiora.',BLUE)],24)
 +note('Il comandante dà ordini chiari, uno alla volta.',CORAL,38),
 notes='Quiz 1.3.6-17 (primo ordine in caso di incendio: giubbotti e allontanarsi), -15 (incendio grave: preparare l\'abbandono), 1.3.7-1 e -13 (prima dell\'abbandono: giubbotti a tutti, zattera equipaggiata), 1.3.5-1 (falla irreparabile: MAYDAY), 1.3.9-13 (PAN PAN), 1.3.7-5 e -6 (grab bag).')

quiz_slide('quizA','Verifica · il sistema',['1.3.7-8','1.3.7-9','1.3.8-25'],False)
quiz_slide('quizAr','Verifica · il sistema',['1.3.7-8','1.3.7-9','1.3.8-25'],True)

# ============ FALLA ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{SKY}"/><rect x="0" y="250" width="1092" height="370" fill="{WATER}" fill-opacity="0.35"/>'+line(0,250,1092,250,SEA,3)
hull='M140 120 L952 120 Q940 360 546 470 Q152 360 140 120 Z'
b+=f'<path d="{hull}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/>'
b+=f'<path d="M230 330 Q546 380 860 330 Q800 420 546 460 Q292 420 230 330 Z" fill="{WATER}" fill-opacity="0.55"/>'
b+=f'<ellipse cx="780" cy="370" rx="16" ry="8" fill="{NAVY}" transform="rotate(-35 780 370)"/>'
b+=''.join(arrow(860-i*14,420+i*6,790-i*10,380+i*4,SEA,4,12) for i in range(3))
b+=f'<rect x="800" y="360" width="120" height="70" rx="16" fill="{ORANGE}" stroke="{NAVY}" stroke-width="4" transform="rotate(-35 860 395)"/>'
b+=f'<rect x="300" y="190" width="90" height="120" rx="12" fill="{STEEL}" stroke="{NAVY}" stroke-width="4"/>'+f'<path d="M345 310 V420" stroke="{NAVY}" stroke-width="6"/>'+arrow(390,220,470,160,SEA,5,16)
lbl=pill(X+830,Y+470,220,'tappo da fuori',ORANGE)+pill(X+200,Y+140,240,'pompa di sentina',NAVY)+lab(X+400,Y+380,220,'acqua in sentina',NAVY,24,900,'center')
txt=(item(1,SEA,'Falla piccola','Pompa di sentina, e cerca da dove entra.')
     +item(2,ORANGE,'Falla grande','Tampona dall\'esterno, con materiali ingombranti: tele cerate, materassi, cuscini. La pressione dell\'acqua tiene fermo il tappo.')
     +item(3,PURPLE,'Falla a prua','Ferma la barca: andando avanti entra più acqua.')
     +item(4,LRED,'Falla irreparabile','MAYDAY e salvezza delle persone. La falla toglie riserva di spinta: la barca può affondare.'))
sec('falla', head('Le emergenze','La falla',LRED), pinned=svgp(X,Y,W,Hh,b,'Sezione trasversale di uno scafo con una falla sotto la linea di galleggiamento: l\'acqua entra, un tappo arancione la chiude dall\'esterno e la pompa di sentina scarica fuori bordo')+lbl+pcol(txt,532,16),
 notes='Quiz 1.3.6-6 (falla lieve: pompa di sentina), -1 (tamponare dall\'esterno), -9 (falla grande: materiali ingombranti), -5 (falla a prua: fermare l\'unità), -7 (riduce la riserva di spinta), 1.3.5-1 (falla irreparabile: MAYDAY), 1.3.6-2 (incaglio volontario per non affondare).')
X=700

# ============ INCENDIO: manovra ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.12"/>'+line(546,110,546,600,'#C9D3DD',3)
b+=''.join(windarrow(x,10,80) for x in (516,576))
b+=topboat(270,330,300,-90,'#FFFFFF',NAVY,5)+flame(270,445,1.3)+''.join(f'<circle cx="{270+dx}" cy="{510+i*30}" r="{16+i*6}" fill="{GREY}" fill-opacity="{0.45-i*0.1:.2f}"/>' for i,dx in enumerate((0,8,-6)))
b+=topboat(820,300,300,90,'#FFFFFF',NAVY,5)+flame(820,415,1.3)+''.join(f'<circle cx="{820+dx}" cy="{480+i*30}" r="{16+i*6}" fill="{GREY}" fill-opacity="{0.45-i*0.1:.2f}"/>' for i,dx in enumerate((0,8,-6)))
lbl=pill(X+40,Y+24,400,'Fuoco a poppa: prua al vento',LRED)+pill(X+620,Y+24,420,'Fuoco a prua: poppa al vento',LRED)+lab(X+60,Y+582,440,'fiamme e fumo sottovento',NAVY,22,800,'center')+lab(X+600,Y+582,440,'lontano da chi è a bordo',NAVY,22,800,'center')
txt=(item(1,LRED,'Fiamme sottovento','Metti la barca in modo che il fuoco resti sottovento. Non correre verso il porto: il vento alimenta il fuoco.')
     +item(2,ORANGE,'Nel vano motore','Chiudi subito carburante e prese d\'aria.')
     +item(3,SEA,'In porto','Allontana la barca dalle altre e dal molo, mentre cerchi di spegnere.')
     +item(4,PURPLE,'Se è grave','Giubbotti a tutti, lontano dal fuoco, e prepara l\'abbandono.'))
sec('incendio', head('Le emergenze','Incendio a bordo',LRED)+col(txt,520,18), pinned=svgp(X,Y,W,Hh,b,'Due barche viste dall\'alto con il vento da nord: con il fuoco a poppa la barca mette la prua al vento; con il fuoco a prua mette la poppa al vento; fiamme e fumo vanno sottovento')+lbl,
 notes='Quiz 1.3.6-13, -18, -22, -25 (fiamme sottovento: fuoco a poppa prua al vento, a prua poppa al vento), -11 (non accelerare verso il porto), -12 e -24 (vano motore: chiudere carburante e vie d\'aria), -19 (in porto: allontanare l\'unità), -15 e -17 (grave: giubbotti, allontanarsi, preparare l\'abbandono), -20 (ventilazione del vano motore a benzina prima di avviare).')

sec('fuoco', head('Le emergenze','Quale estintore, dove',LRED)+table(['Che cosa brucia','Come si spegne'],[40,60],[
 ('Legno, tessuti, carta','Acqua: raffredda'),
 ('Carburante, liquidi','Soffocamento: polvere, schiuma, CO2'),
 ('Quadro elettrico','Estintore a polvere'),
 ('Apparato radio','CO2: raffredda senza danneggiare'),
 ('Fiamma alta','Il getto va alla base della fiamma'),
 ('Quanti estintori','Unità CE: lo dice il manuale del proprietario; non CE: 1 al posto di guida e 1 per locale')],LRED,28)
 +note('Il triangolo del fuoco: togli il combustibile, l\'aria o il calore.',LRED,36),
 notes='Quiz 1.3.6-21 (sostanze comuni: acqua), -23 (liquidi: soffocamento), -16 (quadro elettrico: polvere), 1.3.1-19 (radio: CO2), 1.3.6-14 (base della fiamma), -26 e -27 (numero e posizione degli estintori), 1.3.3-2 (natante entro 6 miglia: almeno 1). Classi di fuoco ed estintori: lezione 6.')

sec('collisione', head('Le emergenze','Collisione e incaglio',LRED)+grid([
 ('Stai per urtare','Ferma il motore, eventualmente indietro, e accosta: l\'urto sarà più leggero.',LRED),
 ('Dopo l\'urto','Soccorri le altre unità e le persone, se non metti in grave pericolo la tua.',ORANGE),
 ('I dati','Dai nei limiti del possibile i dati per identificare la tua barca: altrimenti da 1.032 a 6.197 euro.',PURPLE),
 ('L\'incaglio','Controlla falle e persone; valuta fondo, danno e manovra; aspetta l\'alta marea se serve.',SEA),
 ('Incaglio volontario','Portarsi sul basso apposta per non affondare per una falla o un incendio.',BLUE),
 ('La denuncia','Urto e incaglio sono eventi straordinari: denuncia entro 3 giorni dall\'arrivo in porto.',GREEN)],3,32,26),
 notes='Quiz 1.3.6-10 (fermare, indietro e accostare), 1.8.1-8 (urto: soccorrere), 1.3.7-12 e 1.8.1-4, -43 (dati di identificazione, sanzione), 1.3.6-3, -8 (disincaglio), -2 (incaglio volontario), -4 (causa: punto nave impreciso), 1.8.1-1, -108 (evento straordinario, denuncia entro 3 giorni).')

# ============ UOMO A MARE ============
X=128
b=f'<rect x="0" y="0" width="1092" height="620" fill="{WATER}" fill-opacity="0.14"/>'
cx_,cy_,R=520,280,170
b+=dpath(f'M{cx_-R} 600 L{cx_-R} {cy_}',NAVY,5,False)
path=f'M{cx_-R} {cy_} A{R} {R} 0 1 1 {cx_-R*math.cos(math.radians(40)):.1f} {cy_+R*math.sin(math.radians(40)):.1f}'
b+=dpath(path,CORAL,6)
b+=topboat(cx_-R,520,130,-90,'#FFFFFF',NAVY,4)+topboat(cx_+R,cy_,130,90,'#FFFFFF',NAVY,4)
px_,py_=cx_-R+70,cy_+60
b+=person(px_,py_,CORAL,1.2)+ring(px_+44,py_-6,18)
b+=f'<path d="M{cx_+R-20} {cy_-10} L{px_+20} {py_-10}" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="4 8"/>'
b+=num(cx_-R-40,420,1,NAVY,22)+num(cx_-R+20,cy_-60,2,CORAL,22)+num(px_+80,py_+40,3,ORANGE,22)+num(cx_+R+60,cy_-70,4,PURPLE,22)+num(cx_-40,cy_+R+10,5,SEA,22)
lbl=pill(X+30,Y+470,320,'«Uomo a mare a dritta!»',NAVY)+pill(X+40,Y+150,320,'accosta dallo stesso lato',CORAL)+pill(X+520,Y+368,240,'lancia l\'anulare',ORANGE)
lbl+=pill(X+790,Y+194,260,'occhi sempre su di lui',PURPLE)+pill(X+510,Y+448,300,'arriva piano, in folle',SEA)
txt=(item(1,NAVY,'Grida e premi MOB','Il lato della caduta; sul GPS il tasto MOB segna il punto.')
     +item(2,CORAL,'Accosta subito','Dallo stesso lato: l\'elica si allontana dalla persona.')
     +item(3,ORANGE,'Anulare e occhi','Lancia il salvagente vicino e non perdere mai il contatto visivo.')
     +item(4,SEA,'Arriva piano','Dopo aver perso velocità, motore in folle vicino alla persona.'))
sec('uomoamare', head('Le emergenze','Uomo a mare',LRED), pinned=svgp(X,Y,W,Hh,b,'Manovra di recupero vista dall\'alto: la barca accosta subito dal lato del naufrago, compie un giro e torna piano verso di lui; il salvagente anulare è vicino alla persona in acqua')+lbl+pcol(txt,532,18),
 notes='Quiz 1.3.6-28 (avvicinamento con prudenza dopo aver smaltito la velocità), -29 e -35 (anulare), -31, -33, -36 (accostare dallo stesso lato), -32 e -34 (controllo visivo), 1.7.3-1 e -10 (tasto MOB del GPS), 1.3.8-16 (stacco di sicurezza del fuoribordo). Manovra a vela: appendice E.')
X=700

quiz_slide('quizB','Verifica · le emergenze',['1.3.6-6','1.3.6-22','1.3.6-16'],False)
quiz_slide('quizBr','Verifica · le emergenze',['1.3.6-6','1.3.6-22','1.3.6-16'],True)

# ============ SEGNALI ============
b=f'<rect x="0" y="0" width="1092" height="620" fill="{NIGHT}"/>'
b+=f'<path d="M180 560 Q170 300 200 120" fill="none" stroke="{LRED}" stroke-width="4" stroke-dasharray="6 8"/>'+glow(200,110,LRED,16)+f'<path d="M200 126 L186 160 M200 126 L214 160" stroke="#FFFFFF" stroke-width="2"/><path d="M178 160 Q200 150 222 160" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
b+=f'<rect x="166" y="540" width="28" height="70" rx="8" fill="{LRED}" stroke="#FFFFFF" stroke-width="3"/>'
b+=f'<rect x="530" y="420" width="30" height="160" rx="8" fill="{LRED}" stroke="#FFFFFF" stroke-width="3"/>'+glow(545,390,LRED,22)
b+=f'<rect x="690" y="0" width="402" height="620" fill="{SKY}"/><rect x="690" y="470" width="402" height="150" fill="{WATER}" fill-opacity="0.5"/>'
b+=f'<rect x="860" y="440" width="50" height="50" rx="10" fill="{ORANGE}" stroke="{NAVY}" stroke-width="3"/>'+''.join(f'<circle cx="{885+dx}" cy="{400-i*60}" r="{26+i*14}" fill="{ORANGE}" fill-opacity="{0.8-i*0.15:.2f}"/>' for i,dx in enumerate((0,14,-10,20,-6)))
lbl=pill(X+60,Y+30,320,'razzo a paracadute',LRED)+pill(X+440,Y+300,240,'fuoco a mano',LRED)+pill(X+760,Y+30,280,'boetta fumogena',ORANGE)
lbl+=lab(X+240,Y+160,280,'almeno 300 m di quota · 25 miglia di notte, 7 di giorno · meno di 1 minuto',DSOFT,22,800)+lab(X+230,Y+500,280,'6 miglia · quando vedi le luci',DSOFT,22,800)+lab(X+720,Y+520,360,'di giorno · fumo arancione',NAVY,22,800,'center')
txt=(item(1,LRED,'Razzo a paracadute','Quando presumi che ci sia qualcuno: una nave, un aereo, la costa.')
     +item(2,LRED,'Fuoco a mano','Quando vedi le luci di una nave, di un aereo o della costa: indica dove sei.')
     +item(3,ORANGE,'Boetta fumogena','Il segnale di giorno: fumo arancione.')
     +item(4,NAVY,'Senza pirotecnici','Braccia allargate alzate e abbassate lentamente; un suono continuo con l\'apparecchio da nebbia.'))
sec('segnali', head('Chiedere aiuto','I segnali di soccorso',PURPLE)+col(txt,520,18), pinned=svgp(X,Y,W,Hh,b,'A sinistra, di notte, un razzo a paracadute a luce rossa alto nel cielo e un fuoco a mano acceso; a destra, di giorno, una boetta fumogena che fa fumo arancione sull\'acqua')+lbl,
 notes='Quiz 1.3.9-6 (razzi: se si presume la presenza di soccorritori), -9 (almeno 300 m), 1.3.3-17, -28, -29 (25 miglia di notte, 7 di giorno, meno di 1 minuto), 1.3.9-7 e 1.3.3-16 (fuochi a mano: se si vedono le luci; 6 miglia), 1.3.3-3 e -20 (boetta fumogena arancione, diurna), 1.3.8-24 (braccia), 1.5.2-14 (suono continuo), 1.3.3-21 (scadenza 4 anni), 1.8.2-52 (i segnali scaduti si riportano al rivenditore). Quantità a bordo: DM 133/2024, appendice G.')

sec('chiamare', head('Chiedere aiuto','Chiamare aiuto',PURPLE)+f'<div style="display:flex; gap:28px; align-items:start">'+script('MAYDAY · CANALE 16',[('MAYDAY MAYDAY MAYDAY','k'),('Qui … ×3 · nominativo','n'),('Posizione','m'),('Che cosa succede','m'),('Che aiuto serve','m'),('Quante persone · Passo','e')],760)
 +grid([('DSC','Il pulsante DISTRESS manda MMSI e posizione; poi il MAYDAY a voce sul 16.',PURPLE),('EPIRB','Oltre 50 miglia: il segnale via satellite.',LRED),('1530','Dal telefono, vicino alla costa.',SEA),('CIRM','Per un ferito grave: consigli medici a distanza.',BLUE)],2,30,24,16)+'</div>'
 +note('Chi sente un MAYDAY lo rilancia se nessuno risponde e, se può, va ad aiutare.',PURPLE,34),
 notes='Quiz 1.3.9-12, -14, -16, -19 (MAYDAY: tre volte, poi nominativo, posizione, tipo di pericolo), -8 (canale 16), 1.3.8-7 (DSC), 1.3.3-22 e -34 (EPIRB oltre 50 miglia), 1.3.8-25 (1530), 1.3.2.113 (CIRM), 1.3.9-11 (chi riceve rilancia e soccorre). Procedure complete: appendice H.')

sec('abbandono', head('Chiedere aiuto','Abbandonare la barca',PURPLE)+steps([
 ('Solo se serve','Lo ordina il comandante, dopo aver provato tutto ciò che l\'arte nautica consente.',LRED),
 ('Giubbotti','Tutti con il giubbotto indossato; MAYDAY lanciato.',ORANGE),
 ('La zattera','Controlla che sia equipaggiata. Lega la sagola alla barca, poi lanciala.',SEA),
 ('Grab bag','La sacca con le dotazioni, a portata di mano: va nella zattera.',PURPLE),
 ('Si sale','Direttamente nella zattera, possibilmente senza bagnarsi.',BLUE)],24)
 +note('La zattera sta in coperta, pronta: mai sottocoperta o in un gavone chiuso.',PURPLE,36),
 notes='Quiz 1.3.7-11 (l\'abbandono lo ordina il comandante dopo aver accertato che nulla può salvare l\'unità), -1 e -13 (giubbotti e zattera equipaggiata), -2 (sagola fissata alla barca prima di lanciarla), -3 e -4 (posizione della zattera), -5 e -6 (grab bag). «Si sale senza bagnarsi» è la regola pratica: la barca, finché galleggia, è il mezzo di salvataggio migliore.')

quiz_slide('quizC','Verifica · chiedere aiuto',['1.3.9-6','1.3.7-2','1.3.7-3'],False)
quiz_slide('quizCr','Verifica · chiedere aiuto',['1.3.9-6','1.3.7-2','1.3.7-3'],True)

sec('prevenire', head('Prima e dopo','Prevenire è soccorrere',SEA)+grid([
 ('Prima di partire','Meteo, dotazioni in ordine e non scadute, qualcuno a terra sa dove vai.',SEA),
 ('Il briefing','Mostra a tutti giubbotti, estintori, anulare, VHF e come si chiede aiuto.',CORAL),
 ('Il comandante','Controlla le dotazioni e sostituisce quelle rovinate; decide l\'equipaggio.',PURPLE),
 ('Da soli','In solitario: cintura di sicurezza e agganciati alla barca.',BLUE),
 ('Il fuoribordo','Stacco di sicurezza sempre collegato a chi guida.',LRED),
 ('Benzina','Ventila il vano motore prima di avviare.',ORANGE)],3,32,26),
 notes='Quiz 1.8.1-120 e -125 (il comandante verifica e sostituisce le dotazioni), -121 (equipaggio minimo), 1.3.8-22 (in solitario: cintura e agganciarsi), -16 (stacco di sicurezza), 1.3.6-20 (ventilazione forzata), 1.3.3-21 (segnali: scadenza 4 anni).')

sec('alcol', head('Prima e dopo','Alcol, droghe e farmaci',SEA)+table(['Caso','Conseguenza'],[46,54],[
 ('Comando in stato di ebbrezza','Da 2.755 a 15.000 euro secondo il tasso; patente sospesa da 3 a 24 mesi; licenza sospesa'),
 ('Ebbrezza con danno o pericolo per l\'ambiente','Patente sempre revocata'),
 ('Droghe o psicofarmaci','Da 2.755 a 11.017 euro; raddoppia in caso di sinistro'),
 ('Unità a noleggio, tasso tra 0,5 e 0,8 g/l','Sanzioni aumentate di un terzo'),
 ('Unità a noleggio, oltre 1,5 g/l','Patente sempre revocata'),
 ('Gli effetti','L\'alcol dura fino a 5 ore; con i sedativi è molto pericoloso')],SEA,26),
 notes='Quiz 1.3.2-2 e -3 (ebbrezza: sanzione e sospensione), -7 (sospensione della licenza), -1 e -5 (revoca per danno ambientale), -4 e -8 (droghe, raddoppio in caso di sinistro), -6 e -10 (noleggio), -9, -11, -12 (effetti di alcol e farmaci), 1.8.1-55 (sospensione della patente).')

SCN=[('1','Navigando a motore, dal vano motore a poppa esce fumo. Vento da prua, siete a 2 miglia dal porto.',LRED),
     ('2','Di notte, un membro dell\'equipaggio cade in mare dal lato sinistro. La barca va a 6 nodi.',PURPLE),
     ('3','Entra acqua da una presa a mare rotta. La pompa non riesce a svuotare.',SEA)]
g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:12px; background:#FFFFFF; border-top:12px solid {c}; border-radius:28px; padding:30px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(t,30,INK,600,1.4)}</div>' for n,t,c in SCN)
sec('scenari', head('Prima e dopo','Esercitazione: che cosa fai?',BLUE)+f'<div style="display:flex; gap:24px; align-items:stretch">{g}</div>'
    +note('Per ognuna: i primi tre ordini che dai, in ordine.',BLUE,38),
 notes='Si lavora a gruppi: ogni gruppo dice ad alta voce gli ordini del comandante. Poi si confronta con la slide delle risposte.')
A1=[('Giubbotti a tutti','k'),('Chiudi carburante e prese d\'aria','m'),('Fuoco a poppa: prua al vento','m'),('Estintore alla base della fiamma','m'),('Non correre verso il porto · PAN PAN o MAYDAY','e')]
A2=[('«Uomo a mare a sinistra!»','k'),('Accosta a sinistra · tasto MOB','m'),('Anulare con luce · uno lo indica','m'),('Torna piano, in folle vicino','m'),('Se lo perdi di vista: MAYDAY','e')]
A3=[('Giubbotti a tutti','k'),('Chiudi la presa a mare · tappo','m'),('Pompa a mano e sassola','m'),('Se l\'acqua sale: MAYDAY','m'),('Prepara zattera e grab bag','e')]
sec('scenarir', head('Prima e dopo','Esercitazione: le risposte',BLUE)+f'<div style="display:flex; gap:22px; align-items:stretch">{script("1 · INCENDIO",A1,None,"#7A1E1E")}{script("2 · UOMO A MARE",A2,None,"#3D2C7A")}{script("3 · FALLA",A3,None,"#0B4F58")}</div>',
 notes='1: 1.3.6-17, -12, -24, -22, -14, -11. 2: 1.3.6-31, -33, -35, -32, 1.7.3-1; di notte l\'anulare con la boetta luminosa. 3: 1.3.6-6, -1, -9, 1.3.5-1, 1.3.7-13. Le prese a mare hanno una valvola: chiuderla è la prima cosa; per questo si tengono a portata di mano tappi di legno della misura giusta.')

closing(['Primo ordine in ogni emergenza: giubbotti a tutti',
         'Falla: pompa, tappo da fuori, a prua ferma la barca; se è irreparabile MAYDAY',
         'Incendio: fiamme sottovento, chiudi carburante e aria, estintore alla base',
         'Razzo se presumi qualcuno, fuoco a mano se vedi le luci, fumo arancione di giorno',
         'La zattera si lega alla barca prima di lanciarla; l\'abbandono lo ordina il comandante'],
 'Buon vento, e che non serva mai!','Appendice K · Il soccorso in mare')
write_deck(OUT,'Appendice K · Il soccorso in mare',ORDER,
 {"s1":{"description":"Chi coordina e i primi minuti","start":"cover"},
  "s2":{"description":"Falla, incendio, collisione, uomo a mare","start":"falla"},
  "s3":{"description":"Segnali, chiamata di soccorso, abbandono","start":"segnali"},
  "s4":{"description":"Prevenzione, alcol, esercitazione","start":"prevenire"}})
