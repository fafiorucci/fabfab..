/**
 * Briefing pre-partenza per l'equipaggio, in due parti.
 * I primi nove punti di ogni parte sono quelli del briefing di Onda Portante; gli altri lo completano.
 */
export interface BriefingPoint {
	title: string;
	text: string;
}

export const VITA_DI_BORDO: BriefingPoint[] = [
	{
		title: 'Bagni: non buttare la carta nel WC',
		text: 'Nel WC va solo ciò che si è mangiato o bevuto: carta igienica, assorbenti, salviette e capelli vanno nel cestino. Prima dell’uso apri la valvola, poi pompa acqua di mare; dopo l’uso continua a pompare (10–15 colpi) finché il tubo è pulito e richiudi la valvola. In navigazione le valvole restano sempre chiuse. In porto e in rada non si scaricano acque nere: si usa il serbatoio o i servizi a terra. Se il WC si intasa, avvisa subito lo skipper: non insistere con la pompa.'
	},
	{
		title: 'L’acqua dolce è una risorsa limitata',
		text: 'I serbatoi bastano solo se tutti fanno attenzione. Doccia del marinaio: ti bagni, chiudi l’acqua, ti insaponi, ti sciacqui velocemente. I piatti si lavano prima con acqua di mare e si sciacquano con poca acqua dolce. Chiudi sempre bene i rubinetti: se senti l’autoclave che gira a lungo senza che nessuno usi l’acqua, avvisa lo skipper (serbatoio vuoto o perdita).'
	},
	{
		title: 'Energia: caricare i telefoni e spegnere le luci',
		text: 'Le batterie di bordo sono limitate e servono anzitutto a strumenti, luci di navigazione, frigo e pompe. Ricarica telefoni e dispositivi quando si naviga a motore o quando siamo collegati alla banchina. Spegni luci e ventilatori quando esci dalla cabina. Niente asciugacapelli o apparecchi a 220 V se non siamo collegati a terra. Apri il frigo il meno possibile.'
	},
	{
		title: 'Il quadro elettrico',
		text: 'Lo skipper ti mostra il quadro: lo staccabatterie generale, gli interruttori di luci interne, pompe, frigo e prese. Puoi usare luci e prese; non toccare gli interruttori di strumenti, luci di navigazione, pompe di sentina e VHF senza chiedere.'
	},
	{
		title: 'Oblò e osteriggi: in navigazione sempre chiusi',
		text: 'Impara ad aprirli e chiuderli bene. Prima di partire e ogni volta che si naviga devono essere chiusi: basta un’onda o uno spruzzo per bagnare cuscini e materassi. In coperta non camminare mai sugli osteriggi, aperti o chiusi.'
	},
	{
		title: 'Ordine e sistemazione delle cose',
		text: 'In barca lo spazio è poco e tutto si muove: borse morbide riposte nei gavoni, niente oggetti liberi su tavoli e cuccette prima di partire. Ognuno tiene in ordine la propria cabina; le cose comuni tornano sempre al loro posto, così si ritrovano anche al buio.'
	},
	{
		title: 'Fumo',
		text: 'Si fuma solo in coperta, sottovento, mai durante il rifornimento o vicino al gas. Le cicche non vanno mai in mare, nei bicchieri o nei piatti: usiamo una bottiglia di plastica con metà acqua come posacenere (la “bottiglia dello schifo”), così non si buca e non vola via. Attenzione a vele, cime e tender gonfiabili.'
	},
	{
		title: 'Pulizie, piatti e cucina',
		text: 'Finché funziona ci si organizza liberamente; se nascono lamentele si passa ai turni di corvée (cucina, piatti, pulizie). I rifiuti si differenziano a bordo e si portano a terra. Il gas si apre solo quando serve e si chiude subito dopo. In navigazione il fornello è basculante: pentole fermate con i fermi e mai riempite troppo.'
	},
	{
		title: 'Come ci si muove in barca',
		text: 'Scarpe con suola chiara antiscivolo o piedi nudi: niente ciabatte, niente calzini. Una mano per te e una per la barca: tieniti sempre a qualcosa. Muoviti sul lato sopravvento, lontano da boma, scotte e winch. Sotto coperta usa gli appigli, soprattutto con la barca sbandata.'
	},
	{
		title: 'Cabine, spazi comuni e silenzio',
		text: 'Le cabine si assegnano al primo giorno. Rispettiamo gli spazi degli altri e il silenzio la sera in rada: la voce sull’acqua arriva lontano, anche alle barche vicine.'
	},
	{
		title: 'Sole, idratazione e mal di mare',
		text: 'Cappello, occhiali e crema solare anche quando c’è vento; bevi spesso. Contro il mal di mare: stai all’aperto, guarda l’orizzonte, mangia leggero e asciutto, evita alcol la sera prima; se usi farmaci prendili prima di partire. Se non ti senti bene dillo subito allo skipper: non è una vergogna e c’è sempre un rimedio.'
	},
	{
		title: 'Bagni in mare',
		text: 'Solo quando lo dice lo skipper, a barca ferma e motore spento, con la scaletta abbassata. Mai da soli e mai lontano dalla barca; attenzione a tender e barche in transito. Dalla barca in movimento non ci si tuffa mai.'
	},
	{
		title: 'Il tender',
		text: 'Si usa con la kill-cord legata al polso, senza superare il numero di persone, piano in rada e nelle zone di balneazione (rispetta le ordinanze locali). Di sera porta una torcia. Al rientro il tender si lega corto e il fuoribordo si alza.'
	},
	{
		title: 'Rispetto dell’ambiente',
		text: 'Nelle aree marine protette valgono regole particolari: lo skipper le spiega prima di entrare. Non si ancora sulla posidonia, non si buttano rifiuti in mare (nemmeno quelli organici in rada), si usano saponi e creme il più possibile biodegradabili.'
	}
];

export const SICUREZZA: BriefingPoint[] = [
	{
		title: 'Chi non sa nuotare lo dica',
		text: 'Chi non sa nuotare, o nuota male, lo dice subito allo skipper: per tutta la navigazione indosserà il giubbotto salvagente in coperta. Non è una regola contro qualcuno: in mare cadere è facile e risalire a bordo è difficile.'
	},
	{
		title: 'Reggersi sempre',
		text: 'Una mano per te e una per la barca. Con mare formato muoviti basso, accucciato. Non sederti sulla battagliola e non usare le draglie come schienale.'
	},
	{
		title: 'Il pozzetto è la parte più sicura',
		text: 'In navigazione si sta in pozzetto. A prua si va solo se serve e se lo chiede lo skipper; con mare formato e di notte si va agganciati con la cintura alla jackline.'
	},
	{
		title: 'Autopilota: inserire e disinserire',
		text: 'Lo skipper ti mostra come si inserisce (Auto) e come si disinserisce (Standby) per riprendere subito il timone a mano. Anche con l’autopilota qualcuno resta sempre di guardia e guarda fuori.'
	},
	{
		title: 'Invertitore: avanti, folle, indietro',
		text: 'La leva comanda marcia e motore insieme. Passa sempre dal folle e aspetta un secondo prima di cambiare marcia: si protegge l’invertitore e la manovra resta controllabile.'
	},
	{
		title: 'Accendere e spegnere il motore',
		text: 'Impara la sequenza di accensione e di spegnimento. Dopo l’accensione controlla che esca acqua dallo scarico: se non esce, spegni e avvisa lo skipper.'
	},
	{
		title: 'Dare gas in folle',
		text: 'Per scaldare il motore o caricare le batterie si accelera in folle: lo skipper ti mostra come disinnestare la marcia dalla leva (pulsante o leva tirata) prima di dare gas.'
	},
	{
		title: 'VHF: canale 16 e chiamata di soccorso',
		text: 'Il VHF è sempre sul canale 16, il canale di emergenza. Per chiedere aiuto: alta potenza, premi il tasto per parlare, di’ lentamente MAYDAY tre volte, il nome della barca, la posizione (dal GPS o dall’app), cosa succede e quante persone ci sono a bordo. Con il DSC: tieni premuto il tasto rosso DISTRESS per 5 secondi. In alternativa telefona al 1530 (Guardia Costiera).'
	},
	{
		title: 'Giubbotti salvagente e cinture',
		text: 'Lo skipper ti mostra dove sono e come si indossano: regolati aderenti, con il cinghiale sotto le gambe. Gli autogonfiabili si aprono a contatto con l’acqua o tirando la maniglia. Si indossano quando lo dice lo skipper: di notte, con mare formato, da soli in coperta, e sempre per chi non sa nuotare.'
	},
	{
		title: 'Uomo a mare',
		text: 'Chi vede cadere qualcuno grida «UOMO A MARE!», lo indica con il braccio e non lo perde mai di vista. Si lancia subito il salvagente anulare e la boetta, si preme MOB sul GPS e si chiama lo skipper. Non tuffarti per salvarlo: le persone in acqua diventerebbero due.'
	},
	{
		title: 'Incendio e gas',
		text: 'Sai dove sono gli estintori (vedi il safety plan). Se senti odore di gas: chiudi la bombola, apri oblò e osteriggi, niente fiamme né interruttori, avvisa lo skipper. In caso di fuoco avvisa tutti, chiudi gas e carburante e usa l’estintore alla base delle fiamme.'
	},
	{
		title: 'Via d’acqua',
		text: 'Se vedi acqua sui paglioli avvisa subito lo skipper. Lui ti mostra dove sono le pompe di sentina, la pompa manuale con la sua leva e i tappi conici.'
	},
	{
		title: 'Zattera e abbandono della barca',
		text: 'La zattera si usa solo su ordine dello skipper e come ultima soluzione. Sapere dove si trova, chi la lancia e cosa portare: borsa d’emergenza, acqua, VHF portatile, telefono in busta stagna, documenti.'
	},
	{
		title: 'Pronto soccorso e salute',
		text: 'La cassetta di pronto soccorso è indicata nel safety plan. Allergie, patologie e farmaci che prendi: comunicali allo skipper, anche in privato. Sono informazioni che in caso di emergenza servono subito.'
	},
	{
		title: 'Durante le manovre',
		text: 'Mani lontane da winch, bozzelli, stopper e catena dell’ancora. Attento al boma, soprattutto in abbattuta: abbassa la testa quando lo skipper avvisa. Non stare in piedi sulle cime e fai solo ciò che ti viene chiesto, rispondendo «ok» quando hai capito.'
	},
	{
		title: 'Se lo skipper non può agire',
		text: 'Se lo skipper si fa male o cade in mare: metti il motore in folle o fermalo, sventa o arrotola le vele, chiama aiuto con il VHF (MAYDAY sul 16 o tasto DISTRESS) o con il 1530, leggi la posizione dal GPS o dalla sezione Emergenze dell’app.'
	}
];
