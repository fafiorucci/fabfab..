"""Addendum: schede riassuntive per lo studente, una o due pagine per ogni lezione (regole da memorizzare e numeri dei quiz)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_common import *
OUT=SP+'/deck/project'
EB='Addendum · Schede riassuntive'

def rules(rs,cols=2,ts=28,ds=26,gap='28px 48px'):
    hues=[CORAL,SEA,PURPLE,BLUE,GREEN,ORANGE,SUN,CORAL]
    g=''.join(f'<div style="display:flex; gap:16px; align-items:start">{dot(i+1,hues[i%8])}<div style="display:flex; flex-direction:column; gap:4px">{p(t,ts,INK,800,1.25)}{p(d,ds,BODY,400,1.35)}</div></div>' for i,(t,d) in enumerate(rs))
    return f'<div style="display:grid; grid-template-columns:repeat({cols},1fr); gap:{gap}">{g}</div>'
def nums(ns,cols=4,size=64,ls=26,pad='24px 26px'):
    hues=[CORAL,SEA,PURPLE,BLUE,GREEN,ORANGE]
    g=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#FFFFFF; border-top:10px solid {hues[i%6]}; border-radius:24px; padding:{pad}; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:{size}px; font-weight:700; line-height:1; color:{hues[i%6]}">{n}</p>{p(d,ls,INK,700,1.3)}</div>' for i,(n,d) in enumerate(ns))
    return f'<div style="display:grid; grid-template-columns:repeat({cols},1fr); gap:18px">{g}</div>'
def formulas(fs):
    g=''.join(f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; background:{NAVY}; border-radius:24px; padding:16px 22px"><p style="font-family:{H}; font-size:36px; font-weight:700; line-height:1.1; color:{DACC}">{f}</p><p style="font-size:24px; line-height:1.3; font-weight:700; color:{DSOFT}">{d}</p></div>' for f,d in fs)
    return f'<div style="display:flex; gap:18px; align-items:stretch">{g}</div>'

ORDER=['cover','uso']
SCHEDE=[]  # (n, titolo, icona, colore, ids)
def scheda(n,title,icon,c,R,N=None,F=None,one=False,notes=''):
    eb=f'Scheda {n:02d} · {title}'
    if one or not N:
        inner=head_s(eb,'Regole e numeri da ricordare',icon,c)
        if F: inner+=formulas(F)
        inner+=rules(R,2,27,24,'22px 48px') if N else rules(R,2,31,28,'40px 56px')
        if N: inner+=nums(N,len(N),44,24,'16px 22px')
        sec(f's{n:02d}',inner,notes=notes,gap=28); ids=[f's{n:02d}']
    else:
        sec(f's{n:02d}a',head_s(eb+' · 1/2','Le regole da memorizzare',icon,c)+rules(R),notes=notes,gap=30)
        inner=head_s(eb+' · 2/2','I numeri che tornano nei quiz',icon,c)
        if F: inner+=formulas(F)
        inner+=nums(N)
        sec(f's{n:02d}b',inner,notes=notes,gap=26); ids=[f's{n:02d}a',f's{n:02d}b']
    ORDER.extend(ids); SCHEDE.append((n,title,icon,c,ids))
def head_s(e,t,icon,c): return header(e,t,icon,c)

cover_app('M','Schede riassuntive','Una o due pagine per ogni lezione: le regole da memorizzare e i numeri che tornano nei quiz, cioè distanze, velocità e dotazioni',
 'Addendum al corso: materiale per lo studente. Ogni scheda riassume una lezione. Da stampare (menu del deck: PDF) e tenere nel quaderno di studio.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Appendice M · studio','Addendum · materiale per lo studente'))

# ============ 01 ============
scheda(1,'Teoria dello scafo','hull',CORAL,[
 ('Natante, imbarcazione, nave','Conta la lunghezza dello scafo: natante fino a 10 m, imbarcazione oltre 10 e fino a 24 m, nave oltre 24 m.'),
 ('Opera viva e opera morta','Opera viva (carena): sotto la linea di galleggiamento. Opera morta: sopra, la parte emersa.'),
 ('Dislocamento, stazza, portata','Dislocamento = peso (quanto l\'acqua spostata). Stazza = volume, non peso. Portata = carico trasportabile.'),
 ('Lati e settori','Sinistra rosso, dritta verde. Masconi a prua, traversi al centro, giardinetti a poppa.'),
 ('Le carene','Carena tonda = dislocante, non plana. Fondo piatto o a V = planante. V profonda per il mare formato.'),
 ('Stabilità','G basso e carena larga: barca stabile. Pesi in alto e carichi liberi alzano G e la riducono.'),
 ('Assi','Rollio sul longitudinale, beccheggio sul trasversale, accostata sul verticale.'),
 ('Flaps e trim','Flaps: sempre due. Mare di prua abbassati, di poppa alzati. Trim negativo per entrare in planata, positivo alza la prua.')],
 [('10 m','natante: fino a'),('24 m','imbarcazione: fino a'),('> 24 m','nave da diporto'),('2','flaps, uno per lato')],one=True,
 notes='Scheda della lezione 1. Quiz 1.1.1 (teoria dello scafo) e 1.8.1 (classificazione delle unità).')

# ============ 02 ============
scheda(2,'Motori, elica e timone','propeller',SEA,[
 ('Invertitore','Dà avanti, folle e indietro: il motore gira sempre nello stesso verso.'),
 ('Quattro tempi','Aspirazione, compressione, scoppio, scarico. Solo lo scoppio è la fase utile.'),
 ('Benzina','Accensione a candela. Prima di avviare un entrobordo: aerare il vano motore (vapori).'),
 ('Diesel','Accensione per compressione, iniettori. Aria nel circuito = non parte: spurgare.'),
 ('Fumo','Nero: cattiva combustione. Azzurro: olio nella camera di scoppio.'),
 ('Surriscaldamento','Presa d\'acqua occlusa. Fuoribordo: se la spia non getta acqua, spegni.'),
 ('Effetto evolutivo','Destrorsa in marcia indietro: la poppa va a sinistra. Massimo senza abbrivio.'),
 ('Barra e ruota','Barra a sinistra: la prua va a dritta. Ruota a sinistra: la prua va a sinistra.')],
 [('4','corse del pistone per un ciclo'),('2','giri dell\'albero motore per un ciclo'),('1,36','CV in 1 kW'),('30%','riserva di carburante'),
  ('30-40°','angolo della pala: massimo effetto del timone'),('0,75','kg per litro di carburante'),('300 g','per HP all\'ora (2 tempi)'),('≈ 242 l','180 mg a 30 kn con 31 l/h, riserva compresa')],
 [('t = mg ÷ kn','tempo in ore'),('l = l/h × t','litri consumati'),('× 1,3','con la riserva del 30%')],
 notes='Scheda della lezione 2. Esempio del carburante: quiz 1.2.3-7. Consumo dalla potenza: 80 HP × 300 g = 24 kg/h, diviso 0,75 = 32 l/h.')

# ============ 03 ============
scheda(3,'Ormeggi, cartografia e primi calcoli','map',PURPLE,[
 ('Cavi d\'ormeggio','Spring contro i movimenti avanti e indietro; traversini contro lo scostamento dalla banchina.'),
 ('Ormeggio di poppa','Cime di poppa incrociate; a prua la trappa collegata alla catenaria.'),
 ('Gavitello','Si arriva a lento moto con la prua al vento o alla corrente; ci si lega alla cima sotto il gavitello.'),
 ('Nodi','Gassa d\'amante: occhio che non scorre. Parlato: per i parabordi.'),
 ('Coordinate','Latitudine da 0° a 90° N o S; longitudine da 0° a 180° E o W.'),
 ('Mercatore','Isogona: la lossodromia è una retta. Le distanze si misurano sulla scala delle latitudini, alla stessa latitudine.'),
 ('Scala','Scala più grande = denominatore più piccolo: 1:5.000 è più grande di 1:100.000.'),
 ('Rosa','Angoli da 000° a 360° da Nord in senso orario, sempre con tre cifre.')],
 [('1852 m','1 miglio = 1′ di latitudine'),('60 mg','in 1° di latitudine'),('90°','latitudine massima'),('180°','longitudine massima'),
  ('1:100.000','scala della carta 5/D'),('70°','oltre, Mercatore non si usa'),('12 mg','oltre: strumenti da carteggio obbligatori'),('0,1 h','= 6 minuti')],
 [('S = V × T','miglia = nodi × ore'),('min ÷ 60','minuti in ore'),('0,4 h = 24′','decimi × 60')],
 notes='Scheda della lezione 3. Esempi: 15 nodi per 45 minuti = 11,25 miglia (1.7.5-31); 18 miglia a 7 nodi = 2 h 34′ (1.7.5-65).')

# ============ 04 ============
scheda(4,'Ancoraggio, prora e rotta','anchor',BLUE,[
 ('Tipi di ancora','Danforth su sabbia e fango; CQR, Delta e Rocna su tutti i fondali; grappino e ombrello per piccole unità.'),
 ('Dare fondo','Prua al vento, cala a abbrivio finito, fila indietreggiando, controlla che faccia testa.'),
 ('Alla ruota','Una sola ancora: la barca gira di 360°. Afforcata: due ancore aperte di circa 45°.'),
 ('Vicino alla spiaggia','Oltre 200 m; corridoi di lancio a lento moto; in emergenza verso riva perpendicolari alla costa.'),
 ('Subacquei','Bandiera rossa con diagonale bianca o bandiera «A»: rallenta e passa lontano.'),
 ('Tre nord','Declinazione d (vero-magnetico), deviazione δ (magnetico-bussola), variazione V = d + δ.'),
 ('Scarroccio e deriva','Scarroccio dal vento, deriva dalla corrente. Vento «da», corrente «verso».'),
 ('Orzare','Per tenere la rotta con il vento: Pv = Rv − Sc, la prua va un po\' verso il vento.')],
 [('3-5 ×','il fondale: il calumo'),('15-20 kg','ancora per una barca di 10 m'),('200 m','dalla spiaggia: oltre si naviga e si ancora'),('50 m','gavitelli rossi uno ogni'),
  ('100 m','dal segnale del subacqueo'),('50 m','raggio dove c\'è il sub, dalla bandiera'),('300 m','visibilità della luce gialla della boa sub'),('1 mg','limite per moto d\'acqua, pedalò, vele fino a 4 m²')],
 [('V = d + δ','Est +, Ovest −'),('Pv = Pb + V','bussola → vero'),('Rv = Pv + Sc','vento da sinistra: Sc +')],
 notes='Scheda della lezione 4. Quiz 1.4.3 (ancoraggio), 1.4.2 (distanze), 1.7.3 (bussola).')

# ============ 05 ============
scheda(5,'Punto nave e fanali','lantern',GREEN,[
 ('Punto nave','Serve l\'incrocio di almeno due luoghi di posizione: con uno solo non si fa.'),
 ('Rilevamento polare','Rlv = Pv + ρ; ρ positivo a dritta, negativo a sinistra; al traverso ρ = 90°.'),
 ('Reciproco','Dove sono rispetto al faro: aggiungi o togli 180°. A SW del faro lo rilevo per 045°.'),
 ('Fanali','Di notte a motore: testa d\'albero bianco, verde a dritta, rosso a sinistra, coronamento.'),
 ('Vela di notte','Laterali e coronamento, niente testa d\'albero. A vela e motore insieme: sei a motore.'),
 ('Rischio di collisione','Rilevamento che non cambia e distanza che cala: manovra decisa e per tempo.'),
 ('Scala delle precedenze','Non governa, manovrabilità limitata, pesca, vela, motore. Chi raggiunge cede sempre.'),
 ('Regole di rotta','Motore: cede a chi viene da dritta, rotte opposte si accosta a dritta. Vela: mure a sinistra e sopravento cedono.')],
 [('225°','bianco di testa d\'albero'),('112,5°','ciascun fanale laterale'),('135°','bianco di coronamento'),('2 mg','portata dei laterali, unità 12-50 m'),
  ('50 m','oltre: secondo bianco di testa d\'albero'),('7 m','vela sotto: basta una torcia bianca'),('500 m','waypoint fuori dai fanali del porto'),('8-10 mg','distanza utile dei punti cospicui')],
 notes='Scheda della lezione 5. GPS obbligatorio oltre 12 miglia. Tricolore in testa d\'albero ammesso sotto i 20 m.')

# ============ 06 ============
scheda(6,'Segnalamento, segnali sonori e sicurezza','lighthouse',ORANGE,[
 ('Caratteristica','Un faro si riconosce da tipo di luce, colore e periodo: «Lam (2) 12s».'),
 ('Laterali (regione A)','Entrando in porto: rosso a sinistra (cilindro), verde a dritta (cono).'),
 ('Cardinali','Si passa dal lato del nome. Luci bianche: 3 lampi E, 6 + 1 lungo S, 9 W, continua N.'),
 ('Altri segnali','Pericolo isolato: 2 lampi bianchi. Acque sicure: isofase. Speciale: giallo.'),
 ('Fischio','1 breve accosto a dritta, 2 brevi a sinistra, 3 brevi macchine indietro, 5 brevi: non capisco.'),
 ('In porto','Chi esce ha la precedenza; nel canale tieni la dritta; non si entra a vela, salvo ordinanze.'),
 ('Fuoco','Triangolo: combustibile, comburente, calore. Si spegne togliendo un lato.'),
 ('Estintori','Polvere su tutto; CO2 su B, C, E; schiuma su A, B; acqua mai su D ed E.')],
 [('1 s','suono breve'),('4-6 s','suono prolungato'),('2 min','nella nebbia: un segnale almeno ogni'),('500 m','dall\'ingresso del porto: rallenta'),
  ('12 mg','oltre: zattera, binocolo, GPS, riflettore radar'),('50 mg','oltre: EPIRB, 3 fuochi e 3 razzi'),('25 mg','visibilità di notte dei razzi a paracadute'),('4 anni','scadenza dei pirotecnici')],
 notes='Scheda della lezione 6. Dotazioni: Allegato V del DM 146/2008 come sostituito dal DM 133/2024. VHF oltre 6 miglia. Fuochi a mano visibili a circa 6 miglia. EPIRB su 406 e 121,5 MHz.')

# ============ 07 ============
scheda(7,'Meteorologia e normativa','cloud',CORAL,[
 ('Pressione','Normale 1013 hPa. Se scende in fretta arriva brutto tempo. Isobare fitte = vento forte.'),
 ('Giro del vento','Nel nostro emisfero antiorario attorno alla bassa, orario attorno all\'alta.'),
 ('Brezze','Di giorno brezza di mare (la più forte), di notte brezza di terra.'),
 ('Fronti','Freddo: pressione che sale di colpo, cumulonembi e temporali. Caldo: cirri, pioggia continua.'),
 ('Documenti','Imbarcazioni: licenza e certificato di sicurezza. Ogni motore: assicurazione RC.'),
 ('Patente','Oltre 6 miglia sempre; entro 6 se il motore supera una soglia. Moto d\'acqua e sci nautico: sempre.'),
 ('Evento straordinario','Incaglio, urto, avaria grave: denuncia all\'Autorità marittima entro 3 giorni dall\'arrivo.'),
 ('Aree marine protette','Zona A: niente navigazione né ancoraggio. Zona B: remi e vela.')],
 [('1013 hPa','pressione normale'),('CH 68','Meteomar continuo'),('40,8 CV','30 kW: oltre, serve la patente'),('6 mg','oltre: patente sempre'),
  ('10 / 5','anni di validità, fino a / dopo i 60 anni'),('16 / 18','anni: natante / imbarcazione senza patente'),('3 giorni','per la denuncia di evento straordinario'),('12 m','cavo dello sci nautico, almeno')],
 notes='Scheda della lezione 7. Beaufort da 0 a 12, Douglas da 0 a 9. Nebbia: visibilità sotto 1 km. Visite: categorie A e B prima a 8 anni, C e D a 10, poi ogni 5. Senza patente: 2.755-11.017 euro.')

# ============ 08 ============
scheda(8,'Vela','sail',SEA,[
 ('Manovre fisse e correnti','Strallo, sartie, paterazzo reggono l\'albero; drizze e scotte manovrano le vele.'),
 ('La randa','Tre angoli: penna, mura, scotta. Tre lati: inferitura, base, balumina.'),
 ('Le andature','Bolina, traverso, lasco, poppa. Controvento l\'angolo morto: si bordeggia.'),
 ('Vento apparente','Sempre più a prua del reale; di bolina più forte, in poppa più debole.'),
 ('Orziera e poggiera','CV a proravia del CD: poggiera. A poppavia: orziera. Meglio un po\' orziera.'),
 ('Orzare e poggiare','Barra sottovento: orza. Barra sopravento: poggia.'),
 ('Virata e abbattuta','Virata: la prua passa nel vento. Abbattuta: la poppa. Strambata = abbattuta involontaria.'),
 ('Precedenze','Mure a sinistra cede a mure a dritta; con le stesse mure cede chi è sopravento.')],
 [('45°','bolina, dal vento reale'),('90°','traverso'),('135°','lasco'),('180°','poppa o fil di ruota'),
  ('50%','sovrapposizione tipica del genoa'),('1','vela di prua: sloop'),('2','vele di prua insieme: cutter'),('2','alberi: ketch, mezzana a proravia del timone')],
 notes='Scheda della lezione 8. Quiz di vela: tutti Vero o Falso. Winch: sempre in senso orario. Si riduce appena ci si pensa.')

# ============ 09 ============
scheda(9,'Emergenze, ripasso vela e correnti','lifebuoy',PURPLE,[
 ('Corrente','Si nomina per dove va (Dc). La deriva è uguale per tutti gli scafi.'),
 ('Falla','Tampone da fuori; falla a prua: ferma la barca. Irreparabile: MAYDAY.'),
 ('Incendio','Fiamme sottovento: fuoco a poppa prua al vento, a prua poppa al vento. Chiudi il carburante.'),
 ('Uomo a mare','Grida il lato e accosta da quel lato, salvagente e occhi sempre sul naufrago, arriva in folle.'),
 ('Abbandono','Lo decide il comandante: prima MAYDAY e giubbotti, sagola della zattera legata alla barca.'),
 ('Radio','MAYDAY pericolo grave e imminente, PAN PAN urgenza, SÉCURITÉ sicurezza: tre volte ciascuno.'),
 ('Cattivo tempo','Mai onde al traverso; dal mare alla cappa, onde al mascone.'),
 ('Alcol','Sospensione della patente sempre; revoca oltre 1,5 g/l con unità a noleggio.')],
 [('CH 16','156,8 MHz: soccorso e prima chiamata'),('1 W','potenza ridotta tra barche vicine'),('1530','Guardia Costiera dal telefono'),('00-03','e 30-33: minuti di silenzio radio sul 16'),
  ('10-20 mg','portata VHF tra barche'),('40 mg','portata VHF con le stazioni costiere'),('2.755 €','sanzione minima per ebbrezza'),('3-24 mesi','di sospensione della patente')],
 notes='Scheda della lezione 9. Canali tra barche: 6, 8, 72, 77. CIRM per i consigli medici. Soccorso: alza e abbassa lentamente le braccia allargate.')

# ============ 10-15 carteggio ============
scheda(10,'Carteggio: navigazione costiera','dividers',BLUE,[
 ('Prima tutto in vero','Converti prora e rilevamenti con V = d + δ; porta la declinazione all\'anno della traccia.'),
 ('Stesso faro due volte','Trasporta il primo rilevamento del cammino fatto (Pv, V × t): l\'incrocio col secondo è il punto.'),
 ('Tre rilevamenti','Devono incontrarsi quasi in un punto; un triangolo grande vuol dire un errore.'),
 ('Passare al traverso','Cerchio del raggio dato e tangente dal lato giusto: è la Pv; il punto di tangenza è il traverso.'),
 ('Tabella di deviazione','Entra con Pm = Pv − d, leggi δ, poi Pb = Pm − δ; tra due righe interpola.'),
 ('Intercettazione','Sua velocità da A, parallela ad AB, arco della tua velocità: trovi rotta e punto d\'incontro.')],
 F=[('V = d + δ','variazione'),('Rilv = Rilb + V','rilevamento vero'),('Rilv = Pv + ρ','dal polare'),('m = V × t','cammino')],
 notes='Scheda della lezione 10: esercizi 5.x.3 della carta 5/D.')
scheda(11,'Carteggio: carburante e autonomia','fuel',GREEN,[
 ('Tutte le tratte','Somma le miglia di ogni tratto richiesto; andata e ritorno contano due volte.'),
 ('Ore e minuti','Mai sommarli come decimali: 18 minuti = 0,3 h, 25 minuti = 0,42 h.'),
 ('Riserva','+30% se la traccia non ne indica un\'altra; la soluzione è un intervallo, per esempio 13÷15 litri.'),
 ('Doppio rilevamento 45°-90°','Distanza dal faro al traverso = cammino fatto tra i due rilevamenti.'),
 ('Senza la Vp','Traverso = piede della perpendicolare alla rotta dal faro; V = distanza ÷ tempo.'),
 ('Leggi da chi a chi','«Il faro per 270° a 3,5 mg» vuol dire che sei 3,5 mg a est del faro.')],
 F=[('t = d ÷ V','ore'),('c = t × l/h','litri'),('× 1,3','riserva 30%'),('min ÷ 60','in ore')],
 notes='Scheda della lezione 11: esercizi 5.x.2. Esempio: 16,2 mg a 6 kn = 2,7 h; × 4 l/h = 10,8 l; × 1,3 = 14,0 l.')
scheda(12,'Carteggio: scarroccio','wind',ORANGE,[
 ('Il segno','Vento da sinistra spinge a dritta: Sc positivo. Vento da dritta: Sc negativo.'),
 ('Hai la prora','Rv = Pv + Sc. Esempio 5.1.4-4: Pv 290°, Sc +5° → Rv 295°.'),
 ('Vuoi una rotta','Pv = Rv − Sc: la prora va più al vento. 5.5.4-1: Rv 345°, Sc +10° → Pv 335°.'),
 ('Il traverso','Si conta dalla prora (Pv ± 90°), ma il punto sta sulla rotta vera.'),
 ('I nomi dei venti','Il vento si chiama da dove viene: Maestrale da NW (315°) spinge verso SE.'),
 ('La velocità','Se la traccia lo dice il vento cambia anche la velocità: Ve = Vp ± variazione.')],
 F=[('Rv = Pv + Sc','dalla prora alla rotta'),('Pv = Rv − Sc','dalla rotta alla prora'),('Rilv = Pv + ρ','traverso: ρ = ±90°')],
 notes='Scheda della lezione 12: esercizi 5.x.4 su 5/D e 42/D.')
scheda(13,'Carteggio: correnti (prima parte)','current',CORAL,[
 ('Il triangolo','Un\'ora: da A la Pv per Vp miglia, dalla punta la Dc per Vc miglia; da A alla punta Rv e Ve.'),
 ('Trovare la corrente','Dallo stimato all\'osservato: la direzione è Dc, la lunghezza diviso il tempo è Vc.'),
 ('Andare in B','Traccia AB, da A la corrente, compasso aperto di Vp dalla punta: il taglio sulla rotta dà la Pv.'),
 ('Il tempo','Si calcola con la Ve sul fondo, non con la Vp: t = d ÷ Ve.'),
 ('Corrente «verso»','La corrente si nomina per dove va; il vento da dove viene.'),
 ('Deriva','Tocca tutti gli scafi allo stesso modo: si sposta tutta l\'acqua.')],
 F=[('Pv·Vp + Dc·Vc','= Rv·Ve'),('Vc = mg ÷ t','dallo stimato all\'osservato'),('t = d ÷ Ve','ora di arrivo')],
 notes='Scheda della lezione 13: esercizi 5.1.1, 5.2.1, 5.3.1.')
scheda(14,'Carteggio: correnti (seconda parte)','current',SEA,[
 ('Ora di arrivo','Ve dal triangolo, distanza A-B sulla carta: t = d ÷ Ve, poi somma all\'ora di partenza.'),
 ('Velocità da tenere','Per arrivare a un\'ora data: Ve = d ÷ t; la Vp è la distanza dal vertice della corrente al punto sulla rotta.'),
 ('Corrente dal fondo','Tra due punti noti: velocità sul fondo AB ÷ t; togli il vettore del motore e resta la corrente.'),
 ('Prora contro corrente','La Pv da tenere punta sempre un po\' verso la corrente.'),
 ('Per un\'ora','Il triangolo si disegna sempre per un\'ora: Vp, Vc e Ve in miglia.'),
 ('Controllo','Se la Ve è maggiore della Vp, la corrente ti aiuta; se è minore, ti frena.')],
 F=[('t = d ÷ Ve','quando arrivo'),('Ve = d ÷ t','quanto andare'),('AB ÷ t','velocità sul fondo')],
 notes='Scheda della lezione 14: esercizi 5.4.1. Esempio 5.4.1-2: arrivo alle 11h08m.')
scheda(15,'Carteggio: la carta 42/D','map',PURPLE,[
 ('Dati bussola','Rilv = Rilb + δ + d e Pv = Pb + δ + d. Esempio 5.8.3-1: Pb 317°, δ +4°, d −6° → Pv 315°.'),
 ('Tracciare','Il rilevamento si traccia dal faro verso il mare.'),
 ('Punto con due fari','L\'incrocio dei due rilevamenti veri è il punto nave.'),
 ('Trasporto','Sposta la prima retta lungo la rotta percorsa e incrocia con la seconda.'),
 ('Correnti','Lo stesso triangolo della 5/D, su qualunque carta.'),
 ('All\'esame','Matita morbida, compasso, squadrette e calma: distanze sempre sulla scala delle latitudini.')],
 F=[('Pv = Pb + δ + d','bussola → vero'),('Rilv = Rilb + δ + d','rilevamenti'),('1′ = 1 mg','scala delle latitudini')],
 notes='Scheda della lezione 15: esercizi 5.5-5.8 della carta 42/D (Bocche di Bonifacio).')

# ============ indice / uso ============
cards=''.join(f'<div style="display:flex; align-items:center; gap:14px; background:#FFFFFF; border-left:10px solid {c}; border-radius:20px; padding:12px 18px">'
              f'<p style="font-family:{H}; font-size:40px; font-weight:700; line-height:1; color:{c}; width:52px">{n:02d}</p>{p(t,24,INK,800,1.25)}</div>' for n,t,i,c,ids in SCHEDE)
uso=(head_s(EB,'Come usare le schede','book',SEA)
     +f'<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:14px">{cards}</div>'
     +note('Pagina 1: le regole da memorizzare. Pagina 2: i numeri che tornano nei quiz. Le schede di carteggio stanno in una pagina, con le formule in alto.',SEA,28))
sec('uso',uso,notes='Materiale per lo studente: una o due pagine per ogni lezione. Si stampano dal menu del deck (PDF). Consiglio: rileggere la scheda il giorno dopo la lezione e di nuovo la settimana prima dell\'esame.',gap=26)

# ============ numeri d'oro, quiz, chiusura ============
sec('numeri',head_s(EB,'I numeri d\'oro del corso','star',CORAL)+nums([
 ('200 m','dalla spiaggia'),('100 m','dal segnale del sub'),('500 m','dal porto: rallenta'),('1852 m','un miglio'),
 ('3-5 ×','il fondale: calumo'),('+30%','riserva carburante'),('CH 16','soccorso'),('CH 68','Meteomar'),
 ('6 mg','oltre: patente sempre'),('12 mg','oltre: zattera e radar'),('50 mg','oltre: EPIRB'),('40,8 CV','soglia di potenza')]),
 notes='Riepilogo dei numeri che tornano più spesso nei quiz base.',gap=26)
ORDER.append('numeri')
quiz_slide('quizA','Verifica dei numeri',['1.4.2-4','1.8.2-12','1.3.3-22'],False)
quiz_slide('quizAr','Verifica dei numeri',['1.4.2-4','1.8.2-12','1.3.3-22'],True)
quiz_slide('quizB','Verifica dei numeri',['1.4.1-10','1.3.3-24','1.8.1-89'],False)
quiz_slide('quizBr','Verifica dei numeri',['1.4.1-10','1.3.3-24','1.8.1-89'],True)
ORDER+=['quizA','quizAr','quizB','quizBr']
closing(['Rileggi la scheda il giorno dopo la lezione',
         'Copia a mano i numeri della pagina 2: si ricordano meglio',
         'Fai i quiz di quella lezione e segna gli errori sulla scheda',
         'Per il carteggio: le formule in alto, poi un esercizio svolto',
         'La settimana prima dell\'esame: ripassa solo le schede'],
 'Buono studio, e buon vento per l\'esame!','Addendum · come ripassare con le schede.')
ORDER.append('chiusura')
write_deck(OUT,'Addendum · Schede riassuntive',ORDER,
 {"s1":{"description":"Come usare le schede","start":"cover"},
  "s2":{"description":"Schede 01-09: teoria e vela","start":"s01"},
  "s3":{"description":"Schede 10-15: carteggio","start":"s10"},
  "s4":{"description":"I numeri d'oro e la verifica","start":"numeri"}})
print(len(ORDER))
