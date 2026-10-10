<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Checklist, { type Section } from '#lib/components/Checklist.svelte';

	const sections: Section[] = [
		{
			title: 'Prima di rientrare',
			items: ['Serbatoio carburante rifornito', 'Serbatoio acque nere svuotato', 'Acqua dolce rabboccata (se richiesto)']
		},
		{
			title: 'Barca',
			items: [
				'Interni puliti e frigo svuotato',
				'Coperta lavata',
				'Vele piegate / avvolte e coperte',
				'Gommone e fuoribordo riconsegnati',
				'Inventario dotazioni completo',
				'Contaore motore annotato'
			]
		},
		{
			title: 'Consegna',
			items: [
				'Danni e guasti segnalati al charter',
				'Chiavi e documenti riconsegnati',
				'Verbale di riconsegna firmato',
				'Cauzione: sbloccata o concordata'
			]
		}
	];
</script>

<ModuleShell title="Check-out">
	<h1>Check-out — riconsegna</h1>
	<p class="lead">Confronta con il verbale di check-in e segnala eventuali guasti dal modulo Guasti.</p>
	<Checklist key="checkout" title="Check-out barca" {sections} />
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
