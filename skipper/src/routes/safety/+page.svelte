<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import SafetyPlan from '#lib/components/SafetyPlan.svelte';
	import Locked from '#lib/components/Locked.svelte';
</script>

<ModuleShell title="Safety plan">
	<h1 class="m-h1">Safety plan</h1>
	<p class="m-lead">Dove si trovano dotazioni, comandi e chiusure a bordo. Tocca una voce con 📍 per vederla lampeggiare sulla pianta.</p>
	<Locked label="Safety plan nella versione completa">
		<SafetyPlan />
	</Locked>
</ModuleShell>
