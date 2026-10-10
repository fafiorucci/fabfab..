<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Checklist, { type Group } from '#lib/components/Checklist.svelte';

	const groups: Group[] = [
		{
			title: 'Prima di rientrare',
			ambiti: [
				{
					title: 'Rifornimenti e scarichi',
					items: ['Serbatoio carburante rifornito (e tanica di riserva piena)', 'Serbatoio acque nere svuotato (dove consentito)', 'Acqua dolce rabboccata, se richiesto dal charter']
				}
			]
		},
		{
			title: 'Esterno',
			intro: 'Come al check-in: prima fuori, poi dentro, da prua a poppa.',
			ambiti: [
				{
					title: 'Coperta e attrezzatura',
					items: [
						'Coperta lavata con acqua dolce',
						'Vele avvolte o piegate, lazy bag chiuso, coperture montate',
						'Scotte e drizze in chiaro, cime d’ormeggio e parabordi a posto',
						'Ancora e catena riposte, salpa ancora e magnetotermico spenti',
						'Maniglie dei winch, barra di emergenza e dotazioni di coperta presenti',
						'Tender sgonfiato o riconsegnato, fuoribordo con carburante e lavato'
					]
				}
			]
		},
		{
			title: 'Interno',
			ambiti: [
				{
					title: 'Interni e impianti',
					items: [
						'Interni puliti, frigo svuotato e spento',
						'Rifiuti portati a terra (differenziata)',
						'Prese a mare dei bagni chiuse',
						'Gas chiuso alla bombola',
						'Quadro: utenze spente, solo pompa di sentina in automatico',
						'Contaore motore annotato',
						'Inventario delle dotazioni completo (confronta con il check-in)'
					]
				}
			]
		},
		{
			title: 'Consegna',
			ambiti: [
				{
					title: 'Riconsegna al charter',
					items: [
						'Danni e guasti segnalati (modulo Guasti)',
						'Chiavi, documenti e dotazioni di bordo riconsegnati',
						'Verbale di riconsegna firmato',
						'Cauzione: sbloccata o concordata'
					]
				}
			]
		}
	];
</script>

<ModuleShell title="Check-out">
	<h1 class="m-h1">Check-out — riconsegna</h1>
	<p class="m-lead">Confronta con il verbale di check-in e segnala eventuali guasti dal modulo Guasti.</p>
	<Checklist key="checkout" title="Check-out barca" {groups} />
</ModuleShell>
