<script lang="ts">
	import { MODELS } from '#lib/meteo/models.ts';
	import { searchPlaces, type Place } from '#lib/meteo/api.ts';
	import { MAX_DAYS, MAX_LEAD_DAYS, addDays, isoDate, validateTrip, type Trip } from '#lib/trip.ts';

	interface Props {
		trip: Trip;
		onsave: (t: Trip) => void;
		oncancel?: () => void;
	}

	let { trip, onsave, oncancel }: Props = $props();

	// svelte-ignore state_referenced_locally -- copia di lavoro, indipendente dall'originale
	let draft: Trip = $state(structuredClone($state.snapshot(trip)));
	let query = $state('');
	let results: Place[] = $state([]);
	let searching = $state(false);
	let error: string | null = $state(null);
	let timer: ReturnType<typeof setTimeout>;

	const today = isoDate(new Date());

	function onQuery() {
		clearTimeout(timer);
		const q = query.trim();
		if (q.length < 2) {
			results = [];
			return;
		}
		timer = setTimeout(async () => {
			searching = true;
			try {
				results = await searchPlaces(q);
			} catch (e) {
				error = (e as Error).message;
			} finally {
				searching = false;
			}
		}, 300);
	}

	function choose(p: Place) {
		draft.place = [p.name, p.admin1].filter(Boolean).join(', ');
		draft.lat = +p.latitude.toFixed(3);
		draft.lon = +p.longitude.toFixed(3);
		query = '';
		results = [];
	}

	function toggleModel(id: string) {
		draft.models = draft.models.includes(id) ? draft.models.filter((m) => m !== id) : [...draft.models, id];
	}

	function submit(e: SubmitEvent) {
		e.preventDefault();
		error = validateTrip(draft);
		if (!error) onsave($state.snapshot(draft));
	}
</script>

<form class="form" onsubmit={submit}>
	<h2>Pianifica l'uscita</h2>

	<label>
		<span>Nome</span>
		<input bind:value={draft.name} maxlength="60" placeholder="Es. Weekend all'Elba" />
	</label>

	<div class="field">
		<span>Porto o zona di partenza</span>
		<div class="place">
			<strong>{draft.place}</strong>
			<small>{draft.lat.toFixed(2)}°N {draft.lon.toFixed(2)}°E</small>
		</div>
		<input type="search" bind:value={query} oninput={onQuery} placeholder="Cerca un porto o una località…" aria-label="Cerca località" />
		{#if searching}<small class="muted">Ricerca…</small>{/if}
		{#if results.length}
			<ul class="results">
				{#each results as p (p.latitude + ',' + p.longitude)}
					<li><button type="button" onclick={() => choose(p)}>{p.name} <small>{[p.admin1, p.country].filter(Boolean).join(', ')}</small></button></li>
				{/each}
			</ul>
		{/if}
	</div>

	<div class="row">
		<label>
			<span>Data di uscita</span>
			<input type="date" bind:value={draft.date} min={today} max={addDays(today, MAX_LEAD_DAYS)} required />
		</label>
		<label>
			<span>Giorni</span>
			<input type="number" bind:value={draft.days} min="1" max={MAX_DAYS} required />
		</label>
	</div>

	<label>
		<span>Ampiezza area: ±{draft.radius}° (circa {Math.round(draft.radius * 60)} miglia)</span>
		<input type="range" bind:value={draft.radius} min="0.5" max="2" step="0.25" />
	</label>

	<fieldset>
		<legend>I tuoi limiti</legend>
		<div class="row three">
			<label><span>Vento max (kn)</span><input type="number" bind:value={draft.limits.wind} min="5" max="50" /></label>
			<label><span>Raffiche max (kn)</span><input type="number" bind:value={draft.limits.gust} min="5" max="60" /></label>
			<label><span>Onda max (m)</span><input type="number" bind:value={draft.limits.wave} min="0.3" max="6" step="0.1" /></label>
		</div>
	</fieldset>

	<fieldset>
		<legend>Modelli da confrontare</legend>
		<div class="models">
			{#each MODELS as m (m.id)}
				<label class="chip" style="--c: {m.color}">
					<input type="checkbox" checked={draft.models.includes(m.id)} onchange={() => toggleModel(m.id)} />
					<span>{m.label}</span>
					<small>{m.source} · {m.km} km · {m.days} gg</small>
				</label>
			{/each}
		</div>
	</fieldset>

	{#if error}<p class="error" role="alert">{error}</p>{/if}

	<div class="buttons">
		{#if oncancel}<button type="button" class="ghost" onclick={oncancel}>Annulla</button>{/if}
		<button type="submit" class="primary">Valuta il meteo</button>
	</div>
</form>

<style>
	.form {
		display: grid;
		gap: 14px;
	}
	h2 {
		margin: 0;
		font-size: 1.2rem;
	}
	label,
	.field {
		display: grid;
		gap: 4px;
	}
	label > span,
	.field > span,
	legend {
		font-size: 0.8rem;
		color: var(--muted);
		font-weight: 600;
	}
	input:not([type='checkbox']):not([type='range']) {
		width: 100%;
		padding: 10px 12px;
		border-radius: 10px;
		border: 1px solid var(--line-strong);
		background: var(--bg);
		color: var(--text);
		font-size: 1rem;
	}
	.place {
		display: flex;
		align-items: baseline;
		gap: 8px;
		flex-wrap: wrap;
	}
	.place small {
		color: var(--muted);
	}
	.results {
		list-style: none;
		margin: 0;
		padding: 4px;
		border: 1px solid var(--line-strong);
		border-radius: 10px;
		background: var(--panel);
	}
	.results button {
		width: 100%;
		text-align: left;
		padding: 8px 10px;
		border: 0;
		background: none;
		color: var(--text);
		border-radius: 8px;
		font-size: 0.95rem;
	}
	.results button:hover {
		background: var(--accent-soft);
	}
	.results small {
		color: var(--muted);
	}
	.row {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: 10px;
	}
	.row.three {
		grid-template-columns: repeat(3, 1fr);
		align-items: end;
	}
	fieldset {
		border: 1px solid var(--line);
		border-radius: 12px;
		padding: 10px 12px 12px;
		margin: 0;
	}
	.models {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		gap: 8px;
	}
	.chip {
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: center;
		gap: 0 8px;
		padding: 8px 10px;
		border: 1px solid var(--line-strong);
		border-left: 4px solid var(--c);
		border-radius: 10px;
		cursor: pointer;
	}
	.chip span {
		font-weight: 600;
	}
	.chip small {
		grid-column: 2;
		color: var(--muted);
		font-size: 0.72rem;
	}
	.error {
		color: var(--nogo);
		margin: 0;
	}
	.buttons {
		display: flex;
		justify-content: flex-end;
		gap: 8px;
	}
	.muted {
		color: var(--muted);
	}
</style>
