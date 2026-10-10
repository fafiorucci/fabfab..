<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Checklist, { type Group } from '#lib/components/Checklist.svelte';
	import SafetyPlan from '#lib/components/SafetyPlan.svelte';
	import Locked from '#lib/components/Locked.svelte';

	/**
	 * Check-in tecnico: prima i documenti, poi fuori (coperta) e dentro (interni), da prua a poppa.
	 * Contenuti dal materiale "Check-in tecnico — Kit skipper" di Onda Portante.
	 */
	const groups: Group[] = [
		{
			title: 'Documenti',
			ambiti: [
				{
					title: 'Documenti di bordo e contratto',
					items: [
						'Licenza di navigazione / documenti della barca',
						'Assicurazione in corso di validità',
						'Contratto di noleggio, cauzione e checklist ufficiale del charter',
						'Patente nautica dello skipper',
						'Lista equipaggio',
						'Elenco e scadenze delle dotazioni di sicurezza'
					]
				}
			]
		},
		{
			title: 'Esterno',
			intro: 'Prima fuori, poi dentro: da prua a poppa.',
			ambiti: [
				{
					title: 'Stato generale',
					items: [
						'Opera morta, tuga, pulpiti, battagliola, falchetta, stralli e sartie: botte, crepe, delaminazione, ruggine notevole (fare foto e informare subito il charter/locatore)',
						'Alla prima occasione: botte o crepe all’opera viva (bulbo, timone ed elica)'
					],
					tip: 'Capiamo qual è la reale gravità dei problemi riscontrati. Cosa ci impedisce veramente di salpare? Cosa dobbiamo tenere monitorato?'
				},
				{
					title: 'Ancora principale e salpa ancora',
					high5: true,
					items: [
						'Analisi visiva: corrosione o calcare su catena e campana',
						'Ancora: stato, tipo e dimensione corretti',
						'Grillo / giunto girevole: stato e fascetta di sicurezza tra catena e fuso',
						'Dimensione della catena corretta rispetto al barbotin',
						'Verricello: funzionamento elettrico e frizione manuale',
						'Verricello: numero di giri motore minimo per il funzionamento',
						'Frizione del barbotin: calare 10 m di catena e salparla (è tutto ok?)',
						'Catena: metri disponibili, segna-catena (segnare ogni 10 m alla prima occasione) e rapporto tempo/metri di calumo in issata',
						'Sagolino di ancoraggio della catena a bordo, tra primo anello e golfare'
					],
					tip: 'Staccare magnetotermico o fusibile prima del check. Perché il verricello non gira? Quali possono essere le cause?'
				},
				{
					title: 'Luci',
					items: ['Luci di via: rosso/verde a prua, luce di motore (engine light) all’albero, coronamento a poppa', 'Deck light e luce di testa d’albero (la prima sera)']
				},
				{
					title: 'Albero e vele',
					items: [
						'Albero e boma: rettilineità',
						'Albero e boma: botte e ammaccature',
						'Tenuta della guarnizione al piede d’albero / coperta',
						'Sartie: tensionamento bilanciato',
						'Sartie: stato di arridatoi e crocette',
						'Genoa e randa: apertura e chiusura (circuito avvolgifiocco e avvolgiranda)',
						'Genoa e randa: usura, tagli e vecchie riparazioni',
						'Randa: stecche e borose',
						'Lazy bag e lazy jack',
						'Scotte e drizze: lunghezza e usura',
						'Bozzelli, carrelli e stopper: stato e usura'
					],
					tip: 'Staccare l’amantiglio o sfilare dallo stopper le borose e addugliarle all’albero. Salpereste così?…'
				},
				{
					title: 'Winch',
					items: ['Funzionamento e facilità di rotazione', 'Maniglie: almeno 2 + 1 di rispetto']
				},
				{
					title: 'Motore entrobordo',
					high5: true,
					items: [
						'Accensione e spegnimento',
						'Scarico acqua e fumi (frequenza e portata dello scarico)',
						'Leva: marcia avanti e indietro, acceleratore, folle',
						'Prova dell’effetto evolutivo',
						'Bow thruster (elica di prua)'
					],
					tip: 'Ricordiamo che l’elichetta del bow thruster si “mangia” quel che c’è vicino: in porto la si può distruggere con il capo dormiente della trappa o con il sagolino del tender…'
				},
				{
					title: 'Timoneria',
					high5: true,
					items: [
						'Fluidità e morbidezza d’uso, eventuale gioco',
						'Posizione del circuito: catene, cavi, frenelli e pulegge',
						'Pistone / braccio dell’autopilota: posizione e stato',
						'Accesso a frenelli e settore per eventuali interventi'
					],
					tip: 'Spiegare come si può ridurre il gioco, se eccessivo, agendo sugli arridatoi dei frenelli.'
				},
				{
					title: 'Timone di rispetto',
					items: ['Barra di emergenza (A PORTATA DI MANO)', 'Localizzazione del perno dell’asse del timone', 'Prova di funzionamento'],
					tip: 'Far provare a tutti per capire quanto è faticoso governare.'
				},
				{
					title: 'Strumenti di navigazione',
					items: [
						'Bussola',
						'GPS (se presente in pozzetto)',
						'Display con dati del log, stazione del vento ed ecoscandaglio (check con scandaglio a mano e taratura dello strumento)'
					],
					tip: 'Bussola: far vedere quanto un cellulare acceso e avvicinato può deviarla. Ecoscandaglio: da dove calcola la profondità? Fine del bulbo, livello dell’acqua? Capiamolo.'
				},
				{
					title: 'Cime e parabordi',
					items: ['Cime d’ormeggio: minimo 1 da 50 m, 2 da 20/25 m e 2 di varie lunghezze (più ce ne sono meglio è)', 'Parabordi: minimo 6']
				},
				{
					title: 'Dotazioni di sicurezza in coperta',
					items: [
						'Riflettore radar',
						'Salvagente anulare con cimino',
						'Boetta luminosa',
						'Pompa di sentina manuale (provarla)',
						'Estintore vicino alla plancia comandi'
					],
					tip: 'Nascondere una cosa e a fine check-in chiedere: cosa manca in pozzetto?'
				},
				{
					title: 'Zattera di salvataggio',
					items: ['Stato generale', 'Numero di passeggeri trasportabili', 'Data di scadenza della revisione', 'Sagolino di innesco libero (zattera sempre A PORTATA DI MANO)'],
					tip: 'Solleviamola e spostiamola per capirne il peso e come armarla correttamente in caso di utilizzo.'
				},
				{
					title: 'Altre dotazioni',
					items: [
						'Ancora e catena/cima di rispetto',
						'Bombola del gas (principale e di rispetto) e rubinetto',
						'Cavo elettrico di banchina (controllo adattatori)',
						'Tubo per l’acqua dolce',
						'Tanica da 20 L di gasolio (piena)',
						'Tanica da 5/10 L di carburante per il fuoribordo (piena)',
						'Tanica da 1 L di olio (se necessario)',
						'Lifeline, sassola, buiolo, spugna, ramazza'
					]
				},
				{
					title: 'Tender e fuoribordo',
					items: [
						'Tender: stato generale, graffi o vecchie riparazioni (gonfiato se possibile)',
						'Tender: remi e cimino galleggiante (minimo 10 m)',
						'Fuoribordo: livello carburante e olio',
						'Fuoribordo: elica (allineamento e spina di tenuta)',
						'Fuoribordo: chiavetta e kill-cord',
						'Fuoribordo: accensione e spegnimento con buiolo pieno d’acqua (circuito di raffreddamento)'
					],
					tip: 'Aprire la calotta e individuare insieme dove sono candela, vite del minimo, tubino di alimentazione, carburatore.'
				}
			]
		},
		{
			title: 'Interno',
			intro: 'Aprire tutto e guardare, poi spuntare la lista.',
			ambiti: [
				{
					title: 'Quadro elettrico',
					items: [
						'Indicatori di livello: carburante, acqua dolce e batterie',
						'Tutti gli switch del quadro: luci interne, strumenti di navigazione, VHF, pilota automatico, pompe di sentina e autoclave, presa 12 V…'
					],
					tip: 'Staccare il cavo di fase o il fusibile di un servizio dietro al quadro e far trovare/risolvere a loro il problema.'
				},
				{
					title: 'Batterie',
					high5: true,
					items: [
						'Coltelli (staccabatterie) e magnetotermico dell’ancora: dove sono',
						'Analisi visiva: pulite, asciutte, non ossidate o solfatate; livello del liquido',
						'Calcolo dell’amperaggio disponibile',
						'Test di tensione: staccare 220 V e tutte le utenze, misurare batteria servizi e batteria motore',
						'Confrontare la misura con il display del quadro elettrico',
						'A fine giornata, tutto staccato, ripetere il test: il voltaggio è variato?',
						'Alternatore e caricabatterie caricano le batterie'
					],
					tip: 'Staccare il cavo negativo (nero) dal caricabatterie prima del check. Perché sotto 220 V le batterie non si caricano?'
				},
				{
					title: 'Sentine',
					high5: true,
					items: [
						'Analisi visiva: integre, pulite, vuote',
						'Acqua in sentina? Dolce o salata? Individuare perdita o falla',
						'Pompa di sentina elettrica: posizione, check manuale e automatico (galleggiante)',
						'Prigionieri del bulbo: allentamenti, crepe o eccessiva ruggine',
						'Filtro della pompa di sentina manuale: posizione e pulizia'
					]
				},
				{
					title: 'Motore entrobordo (vano motore)',
					high5: true,
					items: [
						'Blocco motore e sentina: controllo visivo e pulizia, integrità della vernice',
						'WATER — liquido di raffreddamento e pulizia del filtro acqua mare',
						'OIL — livello e colore dell’olio motore e del saildrive (posizione dei tappi)',
						'BELT — stato e tensione della cinghia',
						'BILGE — pulizia della sentina motore',
						'LEAKS — trafilamenti di liquidi, corrosione o calcare',
						'EXHAUST — frequenza e portata dello scarico di fumi e acqua salata',
						'Presa a mare: posizione e funzionamento della valvola',
						'Girante: asciutta all’esterno',
						'Filtro aria: posizione e pulizia',
						'Prefiltro decantatore: posizione e pulizia',
						'Taglia-nafta: posizione e controllo',
						'Tiranteria: innesto di acceleratore e invertitore'
					]
				},
				{
					title: 'Impianto idraulico',
					items: [
						'Acque bianche: pressione dell’autoclave e posizione degli switch dei serbatoi',
						'Acque nere: scarico, prova dei WC e delle valvole',
						'Serbatoio acque nere (se presente): scarico e valvola'
					],
					tip: 'Cosa possiamo fare se si intasa il WC? Cosa può essere successo se rientra molta acqua dopo averlo svuotato e come risolviamo? E se perde acqua mentre azioniamo la pompa a mano?'
				},
				{
					title: 'Strumenti elettronici',
					items: ['GPS: carte dell’area di navigazione corrette, strumenti funzionanti', 'Stazione meteo, AIS e radar (se presenti)'],
					tip: 'Come controlliamo che il GPS ci rilevi nella giusta posizione? Siamo in porto: confrontiamo la posizione con il portolano. Almeno gradi e primi devono essere giusti.'
				},
				{
					title: 'VHF',
					items: ['Funzionamento: radio check con un’altra stazione', 'Se DSC: MMSI inserito, rilevamento automatico della posizione e procedura MAYDAY DSC'],
					tip: 'Durante il weekend far fare a ognuno una chiamata di urgenza o di emergenza (PAN-PAN o MAYDAY) in simulazione, senza trasmettere.'
				},
				{
					title: 'Dotazioni di sicurezza sotto coperta',
					items: [
						'Giubbotti salvagente: dove sono, numero (1 per imbarcato), tipo corretto (minimo 150 N), scadenza',
						'Cinture di sicurezza: dove sono, numero (in Italia non obbligatorie, consigliate almeno 4)',
						'Estintori: dove sono, validità, tipo, uso e numero (almeno 2 sotto coperta: 1 vicino alla sala macchine e 1 vicino al carteggio)',
						'Fuochi a mano, boette fumogene e razzi a paracadute: dove sono, scadenza, numero (almeno 2 per tipo vicino al carteggio)',
						'Orologio, barometro, binocolo, corno da nebbia',
						'Carte nautiche e portolani, strumenti da carteggio, bussola da rilevamento, tabella delle deviazioni',
						'Cassetta di pronto soccorso',
						'Torcia e proiettore',
						'GPS, VHF, EPIRB (oltre 50 miglia)'
					],
					tip: 'Quali e quante dotazioni deve avere la nostra barca? Da cosa dipende? Nel dubbio ci sono schede apposite, online e offline, da portarsi dietro… Oppure nascondere una cosa e a fine check-in chiedere: manca qualcosa?'
				},
				{
					title: 'Cassetta degli attrezzi',
					items: [
						'Attrezzi fondamentali: cacciaviti, pinze, chiavi a brugola…',
						'Ricambi per la manutenzione di base: coni in legno, filtri olio e carburante, girante, cinghia, lampadine, fusibili',
						'Set di riparazione delle vele',
						'Candela e chiave per il fuoribordo'
					]
				},
				{
					title: 'Cucina e gas',
					items: ['Fornello e forno: accensione e termocoppie', 'Valvola del gas e elettrovalvola (se presente)', 'Frigo', 'Oblò e osteriggi: apertura, chiusura e guarnizioni']
				}
			]
		}
	];
</script>

<ModuleShell title="Check-in">
	<h1 class="m-h1">Check-in tecnico</h1>
	<p class="m-lead">Prima gli High Five, poi per zone: documenti, esterno, interno. I dati restano su questo dispositivo; alla fine condividi il verbale.</p>
	<Checklist key="checkin" title="Check-in barca" {groups} highFive />

	<h2 class="sp-h">Safety plan</h2>
	<p class="m-lead">Segna sulla pianta dove si trovano le dotazioni: servono al volo in navigazione e nel briefing all’equipaggio.</p>
	<Locked label="Safety plan nella versione completa">
		<SafetyPlan />
	</Locked>
</ModuleShell>

<style>
	.sp-h {
		margin: 24px 0 4px;
		font-size: 1.05rem;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--brand-2);
		border-bottom: 2px solid var(--brand-2);
		padding-bottom: 4px;
	}
</style>
