<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import { persisted, shareText } from '#lib/persist.svelte.ts';
	import { useGps } from '#lib/gps.svelte.ts';
	import { latDM, lonDM } from '#lib/meteo/format.ts';

	const boat = persisted('barca', { name: '', callsign: '', mmsi: '', persons: '', description: '' });
	const gps = useGps();
	onMount(gps.start);
	onDestroy(gps.stop);

	let nature = $state('');
	let help = $state('');
	let open: string | null = $state('mayday');

	const position = $derived(gps.pos ? `${latDM(gps.pos.lat)}  ${lonDM(gps.pos.lon)}` : '— posizione non disponibile —');
	const b = $derived(boat.value);
	const name = $derived(b.name || '[nome barca]');
	const ids = $derived([b.callsign && `nominativo ${b.callsign}`, b.mmsi && `MMSI ${b.mmsi}`].filter(Boolean).join(', '));

	const mayday = $derived(
		[
			'MAYDAY, MAYDAY, MAYDAY',
			`qui è ${name}, ${name}, ${name}${ids ? `, ${ids}` : ''}`,
			`MAYDAY ${name}${ids ? `, ${ids}` : ''}`,
			`posizione ${position}`,
			nature || '[natura del pericolo: es. via d’acqua, incendio, uomo a mare]',
			help || '[assistenza richiesta]',
			`${b.persons || '[N]'} persone a bordo`,
			b.description || '[altre informazioni: descrizione della barca, zattera, EPIRB]',
			'OVER'
		].join('\n')
	);

	async function sharePosition() {
		if (!gps.pos) return;
		const { lat, lon } = gps.pos;
		await shareText('Posizione', `${name}: ${latDM(lat)} ${lonDM(lon)}\nhttps://www.openstreetmap.org/?mlat=${lat.toFixed(5)}&mlon=${lon.toFixed(5)}#map=12/${lat.toFixed(4)}/${lon.toFixed(4)}`);
	}

	const PROCEDURES: { id: string; title: string; steps: string[] }[] = [
		{
			id: 'mob',
			title: 'Uomo a mare',
			steps: [
				'Grida «UOMO A MARE!» e indica la persona con il braccio teso: qualcuno non deve mai perderla di vista.',
				'Lancia subito il salvagente anulare e la boetta luminosa (o il dan buoy).',
				'Premi il tasto MOB sul GPS/plotter per memorizzare il punto.',
				'Manovra di recupero (quick stop o virata e ritorno); avvicinati sopravvento a bassa velocità.',
				'A motore: elica in folle vicino alla persona, attenzione alle cime in acqua.',
				'Se non riesci a recuperarla subito o la perdi di vista: MAYDAY sul canale 16.'
			]
		},
		{
			id: 'fire',
			title: 'Incendio',
			steps: [
				'Allerta l’equipaggio e fai indossare i giubbotti salvagente.',
				'Chiudi carburante e gas; se è elettrico stacca le batterie.',
				'Usa l’estintore alla base delle fiamme; non aprire il vano motore se l’incendio è lì dentro.',
				'Governa per tenere il fuoco sottovento rispetto alle persone.',
				'Prepara zattera e borsa d’emergenza; se l’incendio non si spegne: MAYDAY.'
			]
		},
		{
			id: 'leak',
			title: 'Via d’acqua',
			steps: [
				'Giubbotti salvagente a tutti; avvia le pompe di sentina (elettrica e manuale).',
				'Cerca l’ingresso dell’acqua: prese a mare, premistoppa dell’asse, tubi, scarichi, timone.',
				'Chiudi le valvole e tappa con tappi conici, stracci o cuscini.',
				'Chiama PAN-PAN (o MAYDAY se l’acqua sale nonostante le pompe) e preparati all’abbandono.'
			]
		},
		{
			id: 'abandon',
			title: 'Abbandono della barca',
			steps: [
				'Solo come ultima soluzione: la barca, anche danneggiata, è più sicura della zattera finché galleggia.',
				'MAYDAY e attivazione dell’EPIRB.',
				'Giubbotti, abiti caldi, borsa d’emergenza (acqua, VHF portatile, razzi, documenti).',
				'Lancia la zattera tenendola legata alla barca; sali possibilmente senza bagnarti.',
				'Taglia la cima solo quando tutti sono a bordo della zattera.'
			]
		},
		{
			id: 'panpan',
			title: 'PAN-PAN (urgenza senza pericolo immediato)',
			steps: [
				'Per avaria seria, ferito non grave o barca senza governo non in pericolo imminente.',
				'Canale 16: «PAN-PAN, PAN-PAN, PAN-PAN — a tutte le stazioni (×3) — qui è [nome barca] (×3)», poi posizione, problema e assistenza richiesta.',
				'In alternativa telefona al 1530 (Guardia Costiera).'
			]
		}
	];
</script>

<ModuleShell title="Emergenze">
	<h1 class="m-h1">Emergenze</h1>

	<section class="m-card pos">
		<p class="lbl">La tua posizione</p>
		<p class="coords">{position}</p>
		{#if gps.pos}
			<p class="m-muted">
				precisione ±{Math.round(gps.pos.acc)} m{gps.pos.sog != null ? ` · ${gps.pos.sog.toFixed(1).replace('.', ',')} kn` : ''}{gps.pos.cog != null ? ` · rotta ${Math.round(gps.pos.cog)}°` : ''}
			</p>
		{:else if gps.error}
			<p class="err">{gps.error}</p>
		{:else}
			<p class="m-muted">Ricerca del segnale GPS…</p>
		{/if}
		<div class="m-actions">
			<a class="sos-call" href="tel:1530">Chiama 1530</a>
			<a class="sos-call alt" href="tel:112">112</a>
			<button class="ghost" onclick={sharePosition} disabled={!gps.pos}>Invia posizione</button>
		</div>
	</section>

	<section class="m-card">
		<button class="acc" onclick={() => (open = open === 'mayday' ? null : 'mayday')}>
			<span>MAYDAY — pericolo grave e imminente</span><span>{open === 'mayday' ? '−' : '+'}</span>
		</button>
		{#if open === 'mayday'}
			<ol class="steps">
				<li>VHF su <b>canale 16</b>, alta potenza. Con DSC: tieni premuto il tasto rosso <b>DISTRESS</b> per 5 secondi, poi parla sul 16.</li>
				<li>Leggi il testo qui sotto lentamente, poi ascolta. Ripeti se nessuno risponde.</li>
			</ol>
			<div class="m-grid">
				<label class="m-field"><span>Natura del pericolo</span><input bind:value={nature} placeholder="Es. via d’acqua, incendio a bordo" /></label>
				<label class="m-field"><span>Assistenza richiesta</span><input bind:value={help} placeholder="Es. richiediamo assistenza immediata" /></label>
			</div>
			<pre class="script">{mayday}</pre>
		{/if}
	</section>

	{#each PROCEDURES as p (p.id)}
		<section class="m-card">
			<button class="acc" onclick={() => (open = open === p.id ? null : p.id)}>
				<span>{p.title}</span><span>{open === p.id ? '−' : '+'}</span>
			</button>
			{#if open === p.id}
				<ol class="steps">{#each p.steps as s (s)}<li>{s}</li>{/each}</ol>
			{/if}
		</section>
	{/each}

	<section class="m-card">
		<h2>Dati della barca (per il MAYDAY)</h2>
		<div class="m-grid">
			<label class="m-field"><span>Nome barca</span><input bind:value={boat.value.name} /></label>
			<label class="m-field"><span>Nominativo radio</span><input bind:value={boat.value.callsign} /></label>
			<label class="m-field"><span>MMSI</span><input bind:value={boat.value.mmsi} inputmode="numeric" /></label>
			<label class="m-field"><span>Persone a bordo</span><input type="number" min="1" bind:value={boat.value.persons} /></label>
			<label class="m-field m-wide"><span>Descrizione</span><input bind:value={boat.value.description} placeholder="Es. sloop 12 m scafo bianco, randa blu" /></label>
		</div>
	</section>

	<p class="m-muted">Procedure di riferimento: non sostituiscono la formazione né le istruzioni delle autorità.</p>
</ModuleShell>

<style>
	.pos {
		border: 2px solid var(--nogo);
		text-align: center;
	}
	.lbl {
		margin: 0;
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--muted);
	}
	.coords {
		margin: 4px 0;
		font-size: clamp(1.3rem, 6vw, 2rem);
		font-weight: 800;
		font-variant-numeric: tabular-nums;
	}
	.err {
		color: var(--nogo);
	}
	.pos .m-actions {
		justify-content: center;
	}
	.sos-call {
		background: var(--nogo);
		color: #fff;
		text-decoration: none;
		font-weight: 800;
		padding: 10px 18px;
		border-radius: 24px;
	}
	.sos-call.alt {
		background: var(--accent);
	}
	.acc {
		width: 100%;
		display: flex;
		justify-content: space-between;
		border: 0;
		background: none;
		color: var(--text);
		font-weight: 700;
		font-size: 1rem;
		padding: 2px 0;
		text-align: left;
	}
	.steps {
		margin: 8px 0;
		padding-left: 20px;
		display: grid;
		gap: 6px;
	}
	.script {
		white-space: pre-wrap;
		background: var(--bg);
		border-left: 4px solid var(--nogo);
		padding: 10px 12px;
		border-radius: 8px;
		font: 600 0.95rem/1.5 system-ui, sans-serif;
		margin: 10px 0 0;
	}
</style>
