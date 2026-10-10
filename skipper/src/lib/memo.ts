/** Skipper memo: promemoria delle regole e dei codici da avere sempre a portata di mano. */

export interface Rule {
	title: string;
	text: string;
}

export const COLREG_PRECEDENZE: Rule[] = [
	{ title: 'Regola 5 — Vedetta', text: 'Mantenere sempre un’efficace vedetta visiva e uditiva, con tutti i mezzi disponibili, per valutare la situazione e il rischio di collisione.' },
	{ title: 'Regola 6 — Velocità di sicurezza', text: 'Navigare sempre a una velocità che permetta di evitare una collisione e di fermarsi nello spazio adeguato, tenendo conto di visibilità, traffico, manovrabilità, vento, mare e correnti.' },
	{ title: 'Regola 7 — Rischio di collisione', text: 'Se il rilevamento di una nave che si avvicina non cambia sensibilmente, il rischio di collisione esiste. Nel dubbio, si considera che esista.' },
	{ title: 'Regola 8 — Manovre per evitare la collisione', text: 'Manovre tempestive, ampie e ben visibili dall’altra nave. Evitare piccole variazioni successive di rotta o velocità.' },
	{ title: 'Regola 9 — Canali stretti', text: 'Navigare il più vicino possibile al limite esterno del canale alla propria dritta. Le barche sotto i 20 m e le barche a vela non devono ostacolare le navi che possono navigare solo nel canale.' },
	{ title: 'Regola 10 — Schemi di separazione del traffico', text: 'Seguire la corsia nel senso indicato; attraversare, se necessario, con prora il più possibile perpendicolare alla direzione del traffico. Le barche sotto i 20 m e a vela non devono ostacolare le navi che seguono la corsia.' },
	{ title: 'Regola 12 — Due barche a vela', text: 'Con mure diverse: la barca con mure a sinistra lascia libera la rotta a quella con mure a dritta. Con le stesse mure: la barca sopravvento lascia libera la rotta a quella sottovento. Se con mure a sinistra non riesci a capire le mure dell’altra barca sopravvento, lasciale libera la rotta.' },
	{ title: 'Regola 13 — Sorpasso', text: 'Chi sorpassa si tiene sempre discosto dalla nave sorpassata, qualunque sia il tipo delle due unità (anche una barca a vela che sorpassa una nave a motore).' },
	{ title: 'Regola 14 — Rotte opposte (a motore)', text: 'Due navi a motore con rotte opposte o quasi: entrambe accostano a dritta per passare sinistra contro sinistra.' },
	{ title: 'Regola 15 — Rotte incrociate (a motore)', text: 'Tra due navi a motore con rotte che si incrociano, lascia libera la rotta quella che vede l’altra alla propria dritta; se possibile evita di passarle di prora.' },
	{ title: 'Regole 16–17 — Chi manovra e chi mantiene', text: 'La nave che deve dare precedenza manovra presto e in modo deciso. L’altra mantiene rotta e velocità, ma deve manovrare da sola se capisce che l’altra non lo sta facendo, e deve farlo comunque se la collisione non è più evitabile con la sola manovra dell’altra.' },
	{ title: 'Regola 18 — Gerarchia delle precedenze', text: 'Dalla più privilegiata: nave che non governa → nave con manovrabilità limitata → nave condizionata dalla propria immersione → nave intenta alla pesca → nave a vela → nave a propulsione meccanica. Una barca a vela che naviga anche a motore è una nave a propulsione meccanica.' },
	{ title: 'Regola 19 — Visibilità ridotta', text: 'Velocità di sicurezza, macchine pronte a manovrare, segnali sonori. Se si rileva al radar un’altra nave: evitare di accostare a sinistra per una nave a proravia del traverso (salvo che si stia sorpassando) e di accostare verso una nave al traverso o a poppavia del traverso.' }
];

export const COLREG_FANALI: Rule[] = [
	{ title: 'Nave a motore in navigazione (sotto 50 m)', text: 'Fanale di testa d’albero bianco (225°), fanali laterali rosso a sinistra e verde a dritta (112,5° ciascuno), fanale di poppa bianco (135°). Sotto i 12 m: possono bastare un bianco visibile tutto l’orizzonte e i fanali laterali.' },
	{ title: 'Barca a vela in navigazione', text: 'Fanali laterali e fanale di poppa. Sotto i 20 m possono essere riuniti in un unico fanale tricolore in testa d’albero. Quando naviga a motore accende anche il fanale di testa d’albero (e non usa il tricolore).' },
	{ title: 'Alla fonda', text: 'Un fanale bianco visibile tutto l’orizzonte a prora (oltre 50 m anche un secondo bianco più basso a poppa). Di giorno: un pallone nero a prora.' },
	{ title: 'Nave che non governa', text: 'Due fanali rossi visibili tutto l’orizzonte, uno sopra l’altro (più fanali laterali e di poppa se ha abbrivio). Di giorno: due palloni neri in verticale.' },
	{ title: 'Nave con manovrabilità limitata', text: 'Rosso – bianco – rosso, visibili tutto l’orizzonte, in verticale. Di giorno: pallone – rombo – pallone.' },
	{ title: 'Nave condizionata dalla propria immersione', text: 'Oltre ai fanali di navigazione, tre rossi in verticale visibili tutto l’orizzonte. Di giorno: un cilindro nero.' },
	{ title: 'Pesca a strascico', text: 'Verde sopra bianco, visibili tutto l’orizzonte (più laterali e di poppa se ha abbrivio). Di giorno: due coni neri uniti per i vertici.' },
	{ title: 'Pesca (non a strascico)', text: 'Rosso sopra bianco, visibili tutto l’orizzonte. Di giorno: due coni uniti per i vertici.' },
	{ title: 'Pilota in servizio', text: 'Bianco sopra rosso, visibili tutto l’orizzonte.' },
	{ title: 'Incagliata', text: 'Fanali di fonda più due rossi in verticale. Di giorno: tre palloni neri in verticale.' },
	{ title: 'Vela e motore insieme, di giorno', text: 'Un cono nero con il vertice in basso, a prora: segnala che la barca a vela sta usando anche il motore.' }
];

export const COLREG_SUONI: Rule[] = [
	{ title: '1 suono breve', text: 'Accosto a dritta.' },
	{ title: '2 suoni brevi', text: 'Accosto a sinistra.' },
	{ title: '3 suoni brevi', text: 'Le mie macchine vanno indietro.' },
	{ title: '5 o più suoni brevi e rapidi', text: 'Dubbio: non capisco le tue intenzioni o dubito che tu stia manovrando abbastanza.' },
	{ title: 'Sorpasso in canale stretto', text: '2 lunghi + 1 breve: intendo sorpassarti sulla tua dritta. 2 lunghi + 2 brevi: sulla tua sinistra. Consenso: lungo, breve, lungo, breve.' },
	{ title: 'Avvicinandosi a una curva', text: '1 suono lungo, a cui risponde con 1 lungo chi sta dall’altra parte.' },
	{ title: 'Visibilità ridotta — a motore con abbrivio', text: '1 suono lungo ogni 2 minuti al massimo.' },
	{ title: 'Visibilità ridotta — a motore senza abbrivio', text: '2 suoni lunghi ogni 2 minuti al massimo.' },
	{ title: 'Visibilità ridotta — vela, pesca, non governa, manovrabilità limitata', text: '1 lungo + 2 brevi ogni 2 minuti al massimo.' },
	{ title: 'Visibilità ridotta — alla fonda', text: 'Campana suonata rapidamente per circa 5 secondi ogni minuto (sotto i 12 m basta un altro segnale efficace).' }
];

export interface Mark {
	name: string;
	look: string;
	light: string;
	meaning: string;
}

/** Sistema IALA regione A (Europa, Africa, gran parte dell'Asia). */
export const IALA: Mark[] = [
	{ name: 'Laterale sinistra', look: 'Rossa, forma cilindrica (o miraglio cilindrico)', light: 'Rossa, qualsiasi ritmo', meaning: 'Entrando in porto (nel senso convenzionale del balisaggio) va lasciata a sinistra.' },
	{ name: 'Laterale dritta', look: 'Verde, forma conica (o miraglio conico con vertice in alto)', light: 'Verde, qualsiasi ritmo', meaning: 'Entrando in porto va lasciata a dritta.' },
	{ name: 'Canale preferito a dritta', look: 'Rossa con una fascia verde orizzontale', light: 'Rossa, lampi composti (2+1)', meaning: 'Biforcazione: il canale principale è a dritta.' },
	{ name: 'Canale preferito a sinistra', look: 'Verde con una fascia rossa orizzontale', light: 'Verde, lampi composti (2+1)', meaning: 'Biforcazione: il canale principale è a sinistra.' },
	{ name: 'Cardinale Nord', look: 'Due coni neri con i vertici in alto; nero sopra, giallo sotto', light: 'Bianca, scintillante continua (Q o VQ)', meaning: 'Le acque sicure sono a nord del segnale.' },
	{ name: 'Cardinale Est', look: 'Due coni uniti per le basi (vertici verso l’esterno); nero – giallo – nero', light: 'Bianca, 3 scintillii (Q(3) 10 s o VQ(3) 5 s)', meaning: 'Le acque sicure sono a est del segnale.' },
	{ name: 'Cardinale Sud', look: 'Due coni con i vertici in basso; giallo sopra, nero sotto', light: 'Bianca, 6 scintillii + 1 lampo lungo (Q(6)+LFl 15 s)', meaning: 'Le acque sicure sono a sud del segnale.' },
	{ name: 'Cardinale Ovest', look: 'Due coni uniti per i vertici; giallo – nero – giallo', light: 'Bianca, 9 scintillii (Q(9) 15 s o VQ(9) 10 s)', meaning: 'Le acque sicure sono a ovest del segnale.' },
	{ name: 'Pericolo isolato', look: 'Due sfere nere sovrapposte; nero con una o più fasce rosse', light: 'Bianca, 2 lampi (Fl(2))', meaning: 'Pericolo di estensione limitata con acque navigabili tutto intorno.' },
	{ name: 'Acque sicure', look: 'Una sfera rossa; strisce verticali bianche e rosse', light: 'Bianca, isofase, occulta, un lampo lungo ogni 10 s o Morse «A»', meaning: 'Acque navigabili tutto intorno: atterraggio, centro canale.' },
	{ name: 'Segnale speciale', look: 'Una croce gialla (a X); colore giallo', light: 'Gialla, ritmo diverso dagli altri segnali', meaning: 'Zone particolari: campi boe, cavi, esercitazioni, balneazione, condotte.' },
	{ name: 'Nuovo pericolo', look: 'Strisce verticali blu e gialle (in numero uguale); miraglio a croce gialla verticale', light: 'Alternata blu e gialla', meaning: 'Pericolo recente non ancora riportato sulle carte (es. relitto).' }
];

export const LUCI_RITMI: Rule[] = [
	{ title: 'F — Fissa', text: 'Luce continua.' },
	{ title: 'Fl — A lampi', text: 'Periodi di luce più brevi dei periodi di buio.' },
	{ title: 'LFl — A lampo lungo', text: 'Lampo di almeno 2 secondi.' },
	{ title: 'Oc — Intermittente (occulta)', text: 'Periodi di luce più lunghi di quelli di buio.' },
	{ title: 'Iso — Isofase', text: 'Luce e buio di uguale durata.' },
	{ title: 'Q / VQ — Scintillante / scintillante rapida', text: 'Circa 60 / 120 lampi al minuto.' },
	{ title: 'Al — Alternata', text: 'Colori che si alternano.' },
	{ title: 'Mo(A) — Morse', text: 'Luce che riproduce una lettera in codice Morse.' }
];

export const MARPOL: Rule[] = [
	{ title: 'Allegato I — Idrocarburi', text: 'Vietato scaricare in mare gasolio, olio e acque di sentina oleose. Le macchie in sentina si raccolgono con panni assorbenti da smaltire a terra. Chi vede o causa uno sversamento lo segnala alla Guardia Costiera.' },
	{ title: 'Allegato IV — Acque nere', text: 'Mai in porti, rade, ormeggi, zone di balneazione e aree marine protette: si usa il serbatoio e lo si svuota a terra. La regola MARPOL prevede lo scarico solo oltre 12 miglia dalla costa per le acque non trattate (3 miglia se triturate e disinfettate) con la barca in navigazione ad almeno 4 nodi. Valgono anche le ordinanze locali, spesso più restrittive.' },
	{ title: 'Allegato V — Rifiuti', text: 'Vietato gettare in mare plastica di ogni tipo, cime, reti, imballaggi, olio da cucina, mozziconi. Il Mediterraneo è «area speciale»: gli avanzi di cibo si possono scaricare solo oltre 12 miglia dalla costa più vicina con la barca in navigazione, ma la buona pratica a bordo è riportare tutto a terra, differenziato.' },
	{ title: 'Allegato VI — Emissioni', text: 'Riguarda le emissioni dei motori: per la barca da diporto conta usare carburante a norma e tenere il motore in ordine (fumo nero = manutenzione).' },
	{ title: 'Buone pratiche a bordo', text: 'Detersivi e creme il più possibile biodegradabili, rifiuti differenziati e portati a terra, mai ancorare sulla posidonia, rispettare le zone delle aree marine protette.' }
];

export interface Flag {
	letter: string;
	word: string;
	meaning: string;
}

/** Codice internazionale dei segnali: alfabeto fonetico e significato delle bandiere singole. */
export const FLAGS: Flag[] = [
	{ letter: 'A', word: 'Alfa', meaning: 'Ho un sommozzatore in immersione: tenetevi lontani e a bassa velocità.' },
	{ letter: 'B', word: 'Bravo', meaning: 'Sto caricando, scaricando o trasportando merci pericolose.' },
	{ letter: 'C', word: 'Charlie', meaning: 'Sì (affermativo).' },
	{ letter: 'D', word: 'Delta', meaning: 'Tenetevi lontani da me: manovro con difficoltà.' },
	{ letter: 'E', word: 'Echo', meaning: 'Accosto a dritta.' },
	{ letter: 'F', word: 'Foxtrot', meaning: 'Sono in avaria: comunicate con me.' },
	{ letter: 'G', word: 'Golf', meaning: 'Ho bisogno di un pilota. (Pescherecci: sto salpando le reti.)' },
	{ letter: 'H', word: 'Hotel', meaning: 'Ho un pilota a bordo.' },
	{ letter: 'I', word: 'India', meaning: 'Accosto a sinistra.' },
	{ letter: 'J', word: 'Juliett', meaning: 'Ho un incendio e merci pericolose a bordo: tenetevi ben lontani.' },
	{ letter: 'K', word: 'Kilo', meaning: 'Desidero comunicare con voi.' },
	{ letter: 'L', word: 'Lima', meaning: 'Fermate immediatamente la vostra nave.' },
	{ letter: 'M', word: 'Mike', meaning: 'La mia nave è ferma e senza abbrivio.' },
	{ letter: 'N', word: 'November', meaning: 'No (negativo).' },
	{ letter: 'O', word: 'Oscar', meaning: 'Uomo in mare.' },
	{ letter: 'P', word: 'Papa', meaning: 'In porto: tutti a bordo, la nave sta per partire. (Pescherecci in mare: le reti sono impigliate.)' },
	{ letter: 'Q', word: 'Quebec', meaning: 'La mia nave è indenne e chiedo libera pratica sanitaria.' },
	{ letter: 'R', word: 'Romeo', meaning: 'Nessun significato come bandiera singola.' },
	{ letter: 'S', word: 'Sierra', meaning: 'Le mie macchine vanno indietro.' },
	{ letter: 'T', word: 'Tango', meaning: 'Tenetevi lontani da me: sto pescando a coppia.' },
	{ letter: 'U', word: 'Uniform', meaning: 'State andando incontro a un pericolo.' },
	{ letter: 'V', word: 'Victor', meaning: 'Chiedo assistenza.' },
	{ letter: 'W', word: 'Whiskey', meaning: 'Chiedo assistenza medica.' },
	{ letter: 'X', word: 'X-ray', meaning: 'Sospendete ciò che state facendo e fate attenzione ai miei segnali.' },
	{ letter: 'Y', word: 'Yankee', meaning: 'Sto arando sull’ancora.' },
	{ letter: 'Z', word: 'Zulu', meaning: 'Ho bisogno di un rimorchiatore. (Pescherecci: sto calando le reti.)' }
];

/** Numeri come si pronunciano in radio secondo il Codice internazionale dei segnali. */
export const NUMBERS = [
	['0', 'Nadazero'],
	['1', 'Unaone'],
	['2', 'Bissotwo'],
	['3', 'Terrathree'],
	['4', 'Kartefour'],
	['5', 'Pantafive'],
	['6', 'Soxisix'],
	['7', 'Setteseven'],
	['8', 'Oktoeight'],
	['9', 'Novenine']
];

export const BEAUFORT = [
	{ f: 0, name: 'Calma', kn: '< 1', sea: 'Mare come uno specchio.' },
	{ f: 1, name: 'Bava di vento', kn: '1–3', sea: 'Piccole increspature senza creste.' },
	{ f: 2, name: 'Brezza leggera', kn: '4–6', sea: 'Onde corte, creste vitree che non si rompono.' },
	{ f: 3, name: 'Brezza tesa', kn: '7–10', sea: 'Creste che cominciano a rompersi, qualche pecorella.' },
	{ f: 4, name: 'Vento moderato', kn: '11–16', sea: 'Onde più lunghe, pecorelle frequenti.' },
	{ f: 5, name: 'Vento teso', kn: '17–21', sea: 'Onde moderate e allungate, molte pecorelle, qualche spruzzo.' },
	{ f: 6, name: 'Vento fresco', kn: '22–27', sea: 'Onde grandi, creste bianche estese, spruzzi.' },
	{ f: 7, name: 'Vento forte', kn: '28–33', sea: 'Il mare si ingrossa, schiuma in strisce nella direzione del vento.' },
	{ f: 8, name: 'Burrasca', kn: '34–40', sea: 'Onde alte e lunghe, creste che si frangono in spruzzi.' },
	{ f: 9, name: 'Burrasca forte', kn: '41–47', sea: 'Onde alte, dense strisce di schiuma, visibilità ridotta dagli spruzzi.' },
	{ f: 10, name: 'Tempesta', kn: '48–55', sea: 'Onde molto alte con creste ripiegate, mare bianco.' },
	{ f: 11, name: 'Tempesta violenta', kn: '56–63', sea: 'Onde eccezionalmente alte, mare coperto di schiuma.' },
	{ f: 12, name: 'Uragano', kn: '≥ 64', sea: 'Aria piena di schiuma e spruzzi, visibilità quasi nulla.' }
];

export const DOUGLAS = [
	{ d: 0, name: 'Calmo', m: '0' },
	{ d: 1, name: 'Quasi calmo', m: '0 – 0,1' },
	{ d: 2, name: 'Poco mosso', m: '0,1 – 0,5' },
	{ d: 3, name: 'Mosso', m: '0,5 – 1,25' },
	{ d: 4, name: 'Molto mosso', m: '1,25 – 2,5' },
	{ d: 5, name: 'Agitato', m: '2,5 – 4' },
	{ d: 6, name: 'Molto agitato', m: '4 – 6' },
	{ d: 7, name: 'Grosso', m: '6 – 9' },
	{ d: 8, name: 'Molto grosso', m: '9 – 14' },
	{ d: 9, name: 'Tempestoso', m: '> 14' }
];

export const VHF: Rule[] = [
	{ title: 'Canale 16', text: 'Soccorso, sicurezza e chiamata. Si ascolta sempre in navigazione; dopo il primo contatto ci si sposta su un canale di lavoro.' },
	{ title: 'MAYDAY', text: 'Pericolo grave e imminente per la barca o le persone. Precedenza assoluta su tutte le comunicazioni. Testo nel modulo Emergenze.' },
	{ title: 'PAN-PAN', text: 'Urgenza: situazione seria ma senza pericolo immediato (avaria, ferito non grave).' },
	{ title: 'SÉCURITÉ', text: 'Sicurezza della navigazione: avvisi meteo, pericoli, ostacoli.' },
	{ title: 'DSC — tasto DISTRESS', text: 'Tenuto premuto 5 secondi invia automaticamente l’allarme con MMSI e posizione (se il GPS è collegato); poi si parla sul 16.' },
	{ title: 'Canali utili', text: 'Canale 9 spesso usato da porti e marina per l’ormeggio; canali 6, 8, 72, 77 per le comunicazioni tra unità. I canali dei porti sono indicati sui portolani.' },
	{ title: 'Procedura di chiamata', text: 'Nome della stazione chiamata (fino a 3 volte), «qui è», nome della propria barca (fino a 3 volte), messaggio, «passo». Parlare lentamente, frasi brevi, attendere la risposta.' }
];
