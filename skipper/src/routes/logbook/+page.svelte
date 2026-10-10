<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import { persisted, shareText, uid } from '#lib/persist.svelte.ts';
	import { useGps } from '#lib/gps.svelte.ts';
	import { latDM, lonDM } from '#lib/meteo/format.ts';

	interface Entry {
		id: string;
		time: string;
		lat: number | null;
		lon: number | null;
		cog: string;
		sog: string;
		wind: string;
		sea: string;
		baro: string;
		engine: string;
		sails: string;
		note: string;
	}

	const store = persisted<Entry[]>('logbook', []);
	const gps = useGps();
	onMount(gps.start);
	onDestroy(gps.stop);

	const nowLocal = () => {
		const d = new Date();
		d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
		return d.toISOString().slice(0, 16);
	};
	const blank = (): Omit<Entry, 'id'> => ({ time: nowLocal(), lat: null, lon: null, cog: '', sog: '', wind: '', sea: '', baro: '', engine: '', sails: '', note: '' });
	let draft = $state(blank());
	let toast: string | null = $state(null);

	function useGpsNow() {
		if (!gps.pos) return;
		draft.lat = +gps.pos.lat.toFixed(5);
		draft.lon = +gps.pos.lon.toFixed(5);
		if (gps.pos.sog != null) draft.sog = gps.pos.sog.toFixed(1);
		if (gps.pos.cog != null) draft.cog = String(Math.round(gps.pos.cog));
	}

	function add(e: SubmitEvent) {
		e.preventDefault();
		store.value = [{ id: uid(), ...draft }, ...store.value].toSorted((a, b) => b.time.localeCompare(a.time));
		draft = blank();
	}

	const pos = (e: Entry) => (e.lat != null && e.lon != null ? `${latDM(e.lat)} ${lonDM(e.lon)}` : '');

	function csv(): string {
		const head = ['Data/ora', 'Latitudine', 'Longitudine', 'Rotta °', 'Velocità kn', 'Vento', 'Mare', 'Barometro hPa', 'Motore h', 'Vele', 'Note'];
		const q = (v: unknown) => `"${String(v ?? '').replace(/"/g, '""')}"`;
		const rows = store.value.toSorted((a, b) => a.time.localeCompare(b.time)).map((e) => [e.time.replace('T', ' '), e.lat ?? '', e.lon ?? '', e.cog, e.sog, e.wind, e.sea, e.baro, e.engine, e.sails, e.note].map(q).join(';'));
		return [head.map(q).join(';'), ...rows].join('\n');
	}

	function download() {
		const a = document.createElement('a');
		a.href = URL.createObjectURL(new Blob(['﻿' + csv()], { type: 'text/csv' }));
		a.download = `logbook-${nowLocal().slice(0, 10)}.csv`;
		a.click();
		setTimeout(() => URL.revokeObjectURL(a.href), 5000);
	}

	async function share() {
		const text = store.value
			.toSorted((a, b) => a.time.localeCompare(b.time))
			.map((e) => `${e.time.replace('T', ' ')} ${pos(e)} ${e.cog && `rotta ${e.cog}°`} ${e.sog && `${e.sog} kn`} ${e.wind && `vento ${e.wind}`} ${e.note}`.replace(/\s+/g, ' ').trim())
			.join('\n');
		const r = await shareText('Log book', `Log book\n\n${text}`);
		if (r === 'copied') {
			toast = 'Copiato negli appunti';
			setTimeout(() => (toast = null), 2500);
		}
	}
</script>

<ModuleShell title="Log book">
	{#snippet actions()}
		<button class="ghost" onclick={share} disabled={!store.value.length}>Condividi</button>
		<button class="ghost" onclick={download} disabled={!store.value.length}>CSV</button>
	{/snippet}

	<h1 class="m-h1">Log book</h1>
	<p class="m-lead">Giornale di bordo: annota posizione, rotta e condizioni a ogni cambio di guardia o evento.</p>

	<form class="m-card" onsubmit={add}>
		<h2>Nuova annotazione</h2>
		<div class="m-grid">
			<label class="m-field"><span>Data e ora</span><input type="datetime-local" bind:value={draft.time} required /></label>
			<div class="m-field">
				<span>Posizione</span>
				<button type="button" class="m-small-btn gpsbtn" onclick={useGpsNow} disabled={!gps.pos}>
					{draft.lat != null && draft.lon != null ? `${latDM(draft.lat)} ${lonDM(draft.lon)}` : gps.pos ? 'Usa GPS' : 'GPS…'}
				</button>
			</div>
			<label class="m-field"><span>Rotta °</span><input type="number" min="0" max="359" bind:value={draft.cog} /></label>
			<label class="m-field"><span>Velocità kn</span><input type="number" min="0" step="0.1" bind:value={draft.sog} /></label>
			<label class="m-field"><span>Vento</span><input bind:value={draft.wind} placeholder="Es. NW 15 kn" /></label>
			<label class="m-field"><span>Mare</span><input bind:value={draft.sea} placeholder="Es. poco mosso" /></label>
			<label class="m-field"><span>Barometro hPa</span><input type="number" step="0.1" bind:value={draft.baro} /></label>
			<label class="m-field"><span>Motore (ore)</span><input type="number" step="0.1" bind:value={draft.engine} /></label>
			<label class="m-field"><span>Vele</span><input bind:value={draft.sails} placeholder="Es. randa 1 mano + genoa" /></label>
			<label class="m-field m-wide"><span>Note ed eventi</span><textarea rows="2" bind:value={draft.note}></textarea></label>
		</div>
		<div class="m-actions"><button class="primary" type="submit">Annota</button></div>
	</form>

	<section class="m-card">
		<h2>Annotazioni ({store.value.length})</h2>
		{#if !store.value.length}<p class="m-muted">Nessuna annotazione.</p>{/if}
		<ul class="m-list">
			{#each store.value as e (e.id)}
				<li>
					<div class="head">
						<strong>{new Date(e.time).toLocaleString('it-IT', { weekday: 'short', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })}</strong>
						<button class="m-small-btn" onclick={() => confirm('Eliminare l’annotazione?') && (store.value = store.value.filter((x) => x.id !== e.id))} aria-label="Elimina">✕</button>
					</div>
					{#if pos(e)}<p class="mono">{pos(e)}</p>{/if}
					<p class="m-muted">
						{[e.cog && `rotta ${e.cog}°`, e.sog && `${e.sog} kn`, e.wind && `vento ${e.wind}`, e.sea && `mare ${e.sea}`, e.baro && `${e.baro} hPa`, e.engine && `motore ${e.engine} h`, e.sails].filter(Boolean).join(' · ')}
					</p>
					{#if e.note}<p>{e.note}</p>{/if}
				</li>
			{/each}
		</ul>
	</section>
	{#if toast}<p class="m-muted">{toast}</p>{/if}
</ModuleShell>

<style>
	.head {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	li p {
		margin: 2px 0;
	}
	.mono {
		font-variant-numeric: tabular-nums;
		font-weight: 600;
	}
	.gpsbtn {
		width: 100%;
		padding: 8px 10px;
		font-size: 0.85rem;
	}
</style>
