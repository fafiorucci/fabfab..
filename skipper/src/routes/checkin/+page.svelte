<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Checklist, { type Section } from '#lib/components/Checklist.svelte';

	const sections: Section[] = [
		{
			title: 'Documenti',
			items: [
				'Licenza di navigazione / documenti della barca',
				'Assicurazione in corso di validità',
				'Contratto di noleggio e cauzione',
				'Patente nautica dello skipper',
				'Lista equipaggio',
				'Elenco delle dotazioni di sicurezza'
			]
		},
		{
			title: 'Scafo e coperta',
			items: [
				'Scafo senza danni visibili (fotografato)',
				'Pulpiti, candelieri e draglie',
				'Winch e stopper funzionanti',
				'Ancora, catena e salpancore (provato)',
				'Gommone e fuoribordo',
				'Parabordi e cime d’ormeggio'
			]
		},
		{
			title: 'Vele e manovre',
			items: ['Randa e lazy bag', 'Genoa / fiocco e avvolgifiocco', 'Scotte e drizze', 'Vang, paterazzo e lazy jack']
		},
		{
			title: 'Motore',
			items: [
				'Livello olio',
				'Liquido di raffreddamento',
				'Cinghia',
				'Filtro acqua mare pulito',
				'Acqua di raffreddamento allo scarico all’avvio',
				'Contaore annotato',
				'Prova marcia avanti e indietro',
				'Elica di prua (se presente)'
			]
		},
		{
			title: 'Sicurezza',
			items: [
				'Giubbotti salvagente (numero e scadenze)',
				'Cinture di sicurezza e jackline',
				'Zattera autogonfiabile (revisione)',
				'Salvagente anulare e boetta luminosa',
				'Razzi e fumogeni (scadenze)',
				'Estintori (revisione)',
				'Cassetta di pronto soccorso',
				'VHF e prova radio',
				'EPIRB (se presente)',
				'Pompe di sentina manuale ed elettrica'
			]
		},
		{
			title: 'Impianti',
			items: [
				'Batterie servizi e motore cariche',
				'Luci di navigazione',
				'Strumenti: log, ecoscandaglio, vento',
				'GPS / plotter',
				'Pilota automatico',
				'Pompe acqua, WC e serbatoio acque nere',
				'Fornello e bombola del gas',
				'Frigo'
			]
		}
	];
</script>

<ModuleShell title="Check-in">
	<h1>Check-in — presa in consegna</h1>
	<p class="lead">Spunta ogni voce controllata. I dati restano su questo dispositivo; alla fine condividi il verbale.</p>
	<Checklist key="checkin" title="Check-in barca" {sections} />
</ModuleShell>

<style>
	h1 {
		margin: 0 0 4px;
		font-size: 1.3rem;
	}
	.lead {
		margin: 0 0 14px;
		color: var(--muted);
	}
</style>
