<script lang="ts">
	import '../app.css';
	import { onDestroy, onMount } from 'svelte';
	import { replaceState } from '$app/navigation';
	import MapView, { type Base } from '#lib/components/MapView.svelte';
	import LineChart, { type Line } from '#lib/components/LineChart.svelte';
	import TripForm from '#lib/components/TripForm.svelte';
	import Verdicts from '#lib/components/Verdicts.svelte';
	import Footer from '#lib/components/Footer.svelte';
	import { BRAND } from '#lib/brand.ts';
	import {
		fetchAtmoGrid,
		fetchMarineGrid,
		fetchPoint,
		fetchPointMarine,
		callsToday,
		DAILY_LIMIT,
		gridForView,
		gridKey,
		homeBox,
		type AtmoGrid,
		type BBox,
		type Grid,
		type MarineGrid,
		type PointMarine,
		type PointSeries
	} from '#lib/meteo/api.ts';
	import { assess } from '#lib/meteo/assess.ts';
	import { areaSeries, cellsIn, dayLabel, frame, localParts, nCells, pick, seaMask, spread, stats, timeIndex } from '#lib/meteo/grid.ts';
	import { LAYERS, cssGradient, type LayerId } from '#lib/meteo/layers.ts';
	import { MODELS, modelById } from '#lib/meteo/models.ts';
	import { decodeTrip, defaultTrip, inviteUrl, loadSavedTrip, saveTrip, type Trip } from '#lib/trip.ts';
	import { reportImage, reportText, shareReport } from '#lib/report.ts';

	// ----- Uscita -----
	let trip = $state<Trip | null>(null);
	let editing = $state(false);

	// ----- Dati -----
	let atmo: Record<string, AtmoGrid> = $state.raw({});
	let atmoErr: Record<string, string> = $state.raw({});
	let marine: MarineGrid | null = $state.raw(null);
	let gen = 0;
	let marineErr: string | null = $state(null);
	let loading = $state(0);
	/** Griglia dei dati: segue la zona inquadrata sulla mappa. */
	let grid = $state.raw<Grid | null>(null);
	let calls = $state(0);
	let viewTimer: ReturnType<typeof setTimeout> | undefined;

	// ----- Vista -----
	let layerId: LayerId = $state('wind');
	let modelId = $state(MODELS[0].id);
	let base: Base = $state('light');
	let seamarks = $state(true);
	let particlesOn = $state(true);
	let tab: 'verdict' | 'area' | 'point' = $state('verdict');
	let areaMetric: 'wind' | 'gust' | 'wave' = $state('wind');
	let view: [number, number, number, number] | null = $state(null);
	let ti = $state(0);
	let playing = $state(false);
	let playTimer: ReturnType<typeof setInterval> | undefined;
	let mapView: ReturnType<typeof MapView> | undefined = $state();
	let toast: string | null = $state(null);

	// ----- Punto -----
	let point: { lat: number; lon: number } | null = $state(null);
	let pointData: PointSeries[] = $state.raw([]);
	let pointMarine: PointMarine | null = $state.raw(null);
	let pointLoading = $state(false);
	let pointGen = 0;

	onMount(() => {
		const fromUrl = new URL(location.href).searchParams.get('u');
		const shared = fromUrl ? decodeTrip(fromUrl) : null;
		const t = shared ?? loadSavedTrip();
		if (t) setTrip(t, !!shared);
		else {
			trip = defaultTrip();
			editing = true;
		}
	});

	onDestroy(() => clearInterval(playTimer));

	function setTrip(t: Trip, fromInvite = false) {
		trip = t;
		editing = false;
		saveTrip(t);
		replaceState(inviteUrl(t, location.href), {});
		if (!t.models.includes(modelId)) modelId = t.models[0];
		point = null;
		pointData = [];
		pointMarine = null;
		// Nuova uscita: si riparte da zero; la mappa inquadra la zona e i dati arrivano con la vista.
		gen++;
		atmo = {};
		atmoErr = {};
		marine = null;
		marineErr = null;
		grid = null;
		ti = -1;
		calls = callsToday();
		if (fromInvite) flash(`Uscita condivisa: ${t.name}`);
	}

	/** La mappa si è fermata su una nuova zona: se serve, scarica la griglia corrispondente. */
	function onView(b: BBox) {
		view = b;
		clearTimeout(viewTimer);
		viewTimer = setTimeout(() => {
			if (!trip) return;
			const g = gridForView(b);
			if (grid && gridKey(g) === gridKey(grid)) return;
			grid = g;
			load($state.snapshot(trip) as Trip, g);
		}, 900); // si attende che la mappa sia ferma: zoom e spostamenti di fila non sprecano chiamate
	}

	async function load(t: Trip, g: Grid) {
		const my = ++gen;
		atmoErr = {};
		marineErr = null;
		// Il modello mostrato sulla mappa per primo, così il campo compare subito.
		const order = [modelId, ...t.models.filter((m) => m !== modelId)].filter((m) => t.models.includes(m));
		const jobs: Promise<void>[] = order.map(async (m) => {
			try {
				const d = await fetchAtmoGrid(t, m, g);
				if (gen !== my) return;
				atmo = { ...atmo, [m]: d };
				if (ti < 0) ti = startIndex(d.times, d.utcOffset);
			} catch (e) {
				if (gen === my) atmoErr = { ...atmoErr, [m]: (e as Error).message };
			}
		});
		jobs.push(
			(async () => {
				try {
					const d = await fetchMarineGrid(t, g);
					if (gen === my) marine = d;
				} catch (e) {
					if (gen === my) marineErr = (e as Error).message;
				}
			})()
		);
		loading = jobs.length;
		for (const j of jobs) j.finally(() => gen === my && loading--);
		await Promise.all(jobs);
		calls = callsToday();
		if (gen === my && ti < 0) ti = 0;
	}

	/** Prima ora utile: le 8 del mattino del giorno di uscita. */
	function startIndex(times: number[], off: number) {
		const i = times.findIndex((t) => localParts(t, off).hour === 8);
		return Math.max(0, i);
	}

	function flash(msg: string) {
		toast = msg;
		setTimeout(() => (toast = null), 3500);
	}

	// ----- Derivati -----
	/** Dati già allineati alla griglia corrente (gli altri sono della zona precedente, in attesa di aggiornamento). */
	const isCurrent = (d: { grid: Grid } | null | undefined) => !!d && !!grid && gridKey(d.grid) === gridKey(grid);
	const loadedModels = $derived(trip ? trip.models.filter((m) => isCurrent(atmo[m])) : []);
	const marineNow = $derived(isCurrent(marine) ? marine : null);
	const anyModel = $derived(trip ? trip.models.find((m) => atmo[m]) : undefined);
	const mapModel = $derived(atmo[modelId] ?? (anyModel ? atmo[anyModel] : null));
	const ref = $derived(mapModel ?? marine);
	const times = $derived(ref?.times ?? []);
	const utcOffset = $derived(ref?.utcOffset ?? 0);
	const now = $derived(times[Math.max(0, ti)] ?? 0);
	const mask = $derived(seaMask(marineNow));
	const layer = $derived(LAYERS[layerId]);
	const home = $derived(trip ? homeBox(trip) : null);

	const at = (g: AtmoGrid | MarineGrid) => timeIndex(g, now);

	const field = $derived.by(() => {
		if (!times.length) return null;
		if (layerId === 'wave') return marine ? { grid: marine.grid, values: frame(marine, 'wave', at(marine)) } : null;
		if (layerId === 'spread') {
			if (!grid || loadedModels.length < 2) return null;
			const frames = loadedModels.map((m) => frame(atmo[m], 'wind', at(atmo[m])));
			return { grid, values: spread(frames, nCells(grid)) };
		}
		return mapModel ? { grid: mapModel.grid, values: frame(mapModel, layerId, at(mapModel)) } : null;
	});

	const arrows = $derived.by(() => {
		if (layerId === 'wave') return marine ? { grid: marine.grid, dir: frame(marine, 'waveDir', at(marine)), value: frame(marine, 'wave', at(marine)) } : null;
		if (!mapModel) return null;
		const k = at(mapModel);
		return { grid: mapModel.grid, dir: frame(mapModel, 'dir', k), value: frame(mapModel, 'wind', k) };
	});

	const wind = $derived.by(() => {
		if (!mapModel || layerId === 'wave') return null;
		const k = at(mapModel);
		return { grid: mapModel.grid, u: frame(mapModel, 'u', k), v: frame(mapModel, 'v', k) };
	});

	// Celle della zona inquadrata: solo mare se c'è la maschera, altrimenti tutte.
	const areaCells = $derived.by(() => {
		if (!grid) return [];
		const box = view ?? grid.bbox;
		const sea = cellsIn(grid, box, mask);
		return sea.length ? sea : cellsIn(grid, box);
	});
	const areaIsSea = $derived(!!mask && !!grid && cellsIn(grid, view ?? grid.bbox, mask).length > 0);
	const gridStep = $derived(grid && grid.lats.length > 1 ? grid.lats[1] - grid.lats[0] : 0);

	const verdicts = $derived(trip ? assess(loadedModels.map((m) => atmo[m]), marineNow, trip.limits, areaCells) : []);

	const timeLabel = $derived.by(() => {
		if (!now) return '';
		const p = localParts(now, utcOffset);
		return `${dayLabel(p.date)} ${p.label}`;
	});

	const areaRows = $derived.by(() => {
		if (areaMetric === 'wave') {
			if (!marineNow) return [];
			return [{ id: 'marine', label: 'Onda (miglior modello)', color: '#0f4c5c', s: stats(pick(frame(marineNow, 'wave', at(marineNow)), areaCells)), series: areaSeries(marineNow, 'wave', areaCells, 'max') }];
		}
		const metric = areaMetric;
		return loadedModels.map((m) => {
			const g = atmo[m];
			const info = modelById(m)!;
			return {
				id: m,
				label: info.label,
				color: info.color,
				s: stats(pick(frame(g, metric, at(g)), areaCells)),
				series: areaSeries(g, metric, areaCells, 'max')
			};
		});
	});

	const areaSpread = $derived.by(() => {
		const means = areaRows.map((r) => r.s.mean).filter((v) => !Number.isNaN(v));
		if (means.length < 2) return null;
		return Math.max(...means) - Math.min(...means);
	});

	// ----- Azioni -----
	function togglePlay() {
		playing = !playing;
		clearInterval(playTimer);
		if (playing) playTimer = setInterval(() => (ti = (ti + 1) % Math.max(1, times.length)), 650);
	}

	async function pickPoint(lat: number, lon: number) {
		if (!trip) return;
		const t = $state.snapshot(trip) as Trip;
		const my = ++pointGen;
		point = { lat, lon };
		tab = 'point';
		pointLoading = true;
		pointData = [];
		pointMarine = null;
		const res = await Promise.allSettled(t.models.map((m) => fetchPoint(t, lat, lon, m)));
		const pm = await fetchPointMarine(t, lat, lon).catch(() => null);
		if (my !== pointGen) return;
		pointData = res.flatMap((r) => (r.status === 'fulfilled' ? [r.value] : []));
		pointMarine = pm;
		pointLoading = false;
	}

	async function invite() {
		if (!trip) return;
		const url = inviteUrl(trip, location.href);
		const data = { title: `Skipper Meteo — ${trip.name}`, text: `Valutiamo insieme il meteo per "${trip.name}"`, url };
		try {
			if (navigator.share) {
				await navigator.share(data);
				return;
			}
		} catch (e) {
			if ((e as Error).name === 'AbortError') return;
		}
		try {
			await navigator.clipboard.writeText(url);
			flash('Link di invito copiato');
		} catch {
			prompt('Copia il link di invito', url);
		}
	}

	let sharing = $state(false);
	async function report() {
		if (!trip || !verdicts.length) return;
		sharing = true;
		try {
			const link = inviteUrl(trip, location.href);
			const png = await reportImage(trip, verdicts, mapView?.snapshot() ?? null);
			const r = await shareReport(trip, reportText(trip, verdicts, link), png);
			if (r === 'downloaded') flash('Report scaricato come immagine');
		} finally {
			sharing = false;
		}
	}

	const pointLines = $derived.by(() => {
		const lines: Line[] = [];
		for (const p of pointData) {
			const info = modelById(p.model);
			lines.push({ label: info?.label ?? p.model, color: info?.color ?? '#888', values: p.wind });
		}
		return lines;
	});
	const pointGustLines = $derived(
		pointData.map((p) => ({ label: (modelById(p.model)?.label ?? p.model) + ' raffiche', color: modelById(p.model)?.color ?? '#888', values: p.gust, dashed: true }))
	);
	const fmt = (x: number, d = 0) => (Number.isNaN(x) ? '—' : x.toFixed(d).replace('.', ','));
</script>

<svelte:head>
	<title>{trip && !editing ? `${trip.name} · Skipper Meteo` : 'Skipper Meteo'}</title>
</svelte:head>

<div class="app">
	<header class="top" class:has-trip={trip && !editing}>
		<div class="brand">
			<svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true"><path d="M16 3 L16 24 L6 24 Z" fill="#ff7a1a" /><path d="M18 7 L18 24 L26 24 Z" fill="#fff" opacity=".9" /><path d="M4 26 Q16 31 28 26" stroke="#5fc2d6" stroke-width="2.5" fill="none" /></svg>
			<span>Skipper <b>Meteo</b> <small class="org">{BRAND.org}</small></span>
		</div>
		{#if trip && !editing}
			<button class="trip" onclick={() => (editing = true)} title="Modifica uscita">
				<strong>{trip.name}</strong>
				<small>{trip.place} · {dayLabel(trip.date)} · {trip.days} gg</small>
			</button>
			<div class="actions">
				<button class="ghost small" onclick={invite}>Invita</button>
				<button class="primary small" onclick={report} disabled={sharing || !verdicts.length}>{sharing ? '…' : 'Report'}</button>
			</div>
		{/if}
	</header>

	{#if editing && trip}
		<div class="sheet">
			<div class="sheet-card">
				<TripForm {trip} onsave={(t) => setTrip(t)} oncancel={loadedModels.length || marine ? () => (editing = false) : undefined} />
				<Footer />
			</div>
		</div>
	{/if}

	{#if trip && !editing}
		<main class="layout">
			<section class="mapcol">
				<MapView
					bind:this={mapView}
					{home}
					{field}
					{layer}
					{arrows}
					{wind}
					{base}
					{seamarks}
					particles={particlesOn}
					{point}
					onpick={pickPoint}
					onview={onView}
				/>

				<div class="ctrl layers">
					{#each Object.values(LAYERS) as l (l.id)}
						<button class:on={layerId === l.id} onclick={() => (layerId = l.id)} disabled={l.id === 'spread' && loadedModels.length < 2}>{l.label}</button>
					{/each}
				</div>

				<div class="ctrl models">
					{#if layerId === 'spread'}
						<span class="hint">Deviazione tra {loadedModels.length} modelli</span>
					{:else if layerId === 'wave'}
						<span class="hint">Onda: miglior modello disponibile</span>
					{:else}
						<select bind:value={modelId} aria-label="Modello sulla mappa">
							{#each trip.models as m (m)}
								<option value={m} disabled={!atmo[m]}>{modelById(m)?.label ?? m}{atmoErr[m] ? ' (non disp.)' : !atmo[m] ? ' …' : ''}</option>
							{/each}
						</select>
					{/if}
				</div>

				<div class="ctrl basemap">
					<button class:on={base === 'light'} onclick={() => (base = 'light')}>Mappa</button>
					<button class:on={base === 'satellite'} onclick={() => (base = 'satellite')}>Satellite</button>
					<button class:on={seamarks} onclick={() => (seamarks = !seamarks)} title="Segnali nautici OpenSeaMap">⚓</button>
					<button class:on={particlesOn} onclick={() => (particlesOn = !particlesOn)} title="Particelle del vento">〰</button>
					<button onclick={() => mapView?.goHome()} title="Torna alla zona dell'uscita">⌂</button>
				</div>

				<div class="timeline">
					<div class="legend">
						<span>{layer.label} ({layer.unit})</span>
						<span class="bar" style="background: {cssGradient(layer)}"></span>
						<span class="lim">{layer.stops[0][0]}–{layer.stops[layer.stops.length - 1][0]}</span>
					</div>
					<div class="tl-row">
						<button class="play" onclick={togglePlay} aria-label={playing ? 'Pausa' : 'Riproduci'}>{playing ? '❚❚' : '▶'}</button>
						<input type="range" min="0" max={Math.max(0, times.length - 1)} bind:value={ti} aria-label="Ora" />
						<span class="when">{timeLabel}</span>
					</div>
				</div>

				{#if loading > 0}<div class="loading">Carico i modelli… ({loading})</div>{/if}
			</section>

			<aside class="panel">
				<nav class="tabs">
					<button class:on={tab === 'verdict'} onclick={() => (tab = 'verdict')}>Valutazione</button>
					<button class:on={tab === 'area'} onclick={() => (tab = 'area')}>Area inquadrata</button>
					<button class:on={tab === 'point'} onclick={() => (tab = 'point')}>Punto</button>
				</nav>

				{#if Object.keys(atmoErr).length || marineErr}
					<details class="errors">
						<summary>Alcuni dati non sono disponibili</summary>
						<ul>
							{#each Object.entries(atmoErr) as [m, e] (m)}<li><b>{modelById(m)?.label ?? m}</b>: {e}</li>{/each}
							{#if marineErr}<li><b>Onda</b>: {marineErr}</li>{/if}
						</ul>
					</details>
				{/if}

				{#if tab === 'verdict'}
					<p class="muted small">
						Valutazione della <b>zona inquadrata</b> sulla mappa ({areaIsSea ? `${areaCells.length} punti di mare` : `${areaCells.length} punti`}, passo {fmt(gridStep, 2)}°).
						Sposta o zooma la mappa per valutare un altro tratto; ⌂ riporta alla zona dell'uscita.
					</p>
					{#if verdicts.length}
						<Verdicts {verdicts} limits={trip.limits} />
					{:else if loading}
						<p class="muted">Sto confrontando i modelli…</p>
					{:else}
						<p class="muted">Nessun dato disponibile per la valutazione.</p>
					{/if}
				{:else if tab === 'area'}
					<div class="seg">
						<button class:on={areaMetric === 'wind'} onclick={() => (areaMetric = 'wind')}>Vento</button>
						<button class:on={areaMetric === 'gust'} onclick={() => (areaMetric = 'gust')}>Raffiche</button>
						<button class:on={areaMetric === 'wave'} onclick={() => (areaMetric = 'wave')}>Onda</button>
					</div>
					<p class="muted small">
						Zona inquadrata · {areaCells.length} punti {areaIsSea ? 'di mare' : ''} · {timeLabel}.
						Zooma o sposta la mappa per confrontare i modelli su un tratto preciso.
					</p>
					{#if areaSpread !== null}
						<p class="spread" class:hi={areaSpread > 5}>
							Differenza tra i modelli (media dell'area): <b>{fmt(areaSpread, 1)} kn</b>
							{areaSpread > 5 ? '— modelli in disaccordo, previsione incerta' : areaSpread > 2.5 ? '— accordo discreto' : '— modelli concordi'}
						</p>
					{/if}
					<table class="area">
						<thead><tr><th>Modello</th><th>Min</th><th>Media</th><th>Max</th></tr></thead>
						<tbody>
							{#each areaRows as r (r.id)}
								<tr>
									<td><span class="sw" style="background: {r.color}"></span>{r.label}</td>
									<td>{fmt(r.s.min, areaMetric === 'wave' ? 1 : 0)}</td>
									<td>{fmt(r.s.mean, areaMetric === 'wave' ? 1 : 0)}</td>
									<td><b>{fmt(r.s.max, areaMetric === 'wave' ? 1 : 0)}</b></td>
								</tr>
							{/each}
						</tbody>
					</table>
					<h4>Massimo nell'area, ora per ora</h4>
					<LineChart
						{times}
						{utcOffset}
						lines={areaRows.map((r) => ({ label: r.label, color: r.color, values: r.series }))}
						unit={areaMetric === 'wave' ? 'm' : 'kn'}
						limit={areaMetric === 'wave' ? trip.limits.wave : areaMetric === 'gust' ? trip.limits.gust : trip.limits.wind}
						cursor={ti}
						onseek={(i) => (ti = i)}
					/>
				{:else}
					{#if !point}
						<p class="muted">Tocca un punto sulla mappa per vedere il meteogramma di tutti i modelli in quel punto.</p>
					{:else}
						<p class="small">
							<b>{point.lat.toFixed(3)}°N {point.lon.toFixed(3)}°E</b>
							<button class="link" onclick={() => (point = null)}>rimuovi</button>
						</p>
						{#if pointLoading}<p class="muted">Carico…</p>{/if}
						{#if pointData.length}
							<h4>Vento medio (linee) e raffiche (tratteggio)</h4>
							<LineChart
								times={pointData[0].times}
								utcOffset={pointData[0].utcOffset}
								lines={[...pointLines, ...pointGustLines]}
								unit="kn"
								limit={trip.limits.wind}
								cursor={ti}
								onseek={(i) => (ti = i)}
								height={180}
							/>
							<div class="keys">
								{#each pointData as p (p.model)}<span><i style="background: {modelById(p.model)?.color}"></i>{modelById(p.model)?.label}</span>{/each}
							</div>
						{/if}
						{#if pointMarine}
							<h4>Onda significativa</h4>
							<LineChart
								times={pointMarine.times}
								utcOffset={pointMarine.utcOffset}
								lines={[{ label: 'Onda', color: '#0f4c5c', values: pointMarine.wave }]}
								unit="m"
								limit={trip.limits.wave}
								cursor={ti}
								onseek={(i) => (ti = i)}
								height={120}
							/>
						{:else if !pointLoading}
							<p class="muted small">Nessun dato d'onda in questo punto (terraferma?).</p>
						{/if}
					{/if}
				{/if}
				<p class="budget" class:warn={calls > DAILY_LIMIT * 0.8}>
					Chiamate Open-Meteo oggi da questo dispositivo: ~{calls.toLocaleString('it-IT')} / {DAILY_LIMIT.toLocaleString('it-IT')}
				</p>
				<Footer />
			</aside>
		</main>
	{/if}

	{#if toast}<div class="toast" role="status">{toast}</div>{/if}
</div>

<style>
	.app {
		min-height: 100dvh;
		display: flex;
		flex-direction: column;
	}
	.top {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 8px 14px;
		padding-top: max(8px, env(safe-area-inset-top));
		background: var(--brand);
		color: #fff;
		border-bottom: 3px solid var(--accent);
	}
	.brand {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 1.05rem;
		white-space: nowrap;
	}
	.brand b {
		color: var(--accent);
	}
	.brand .org {
		display: block;
		font-size: 0.62rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #8fb4c8;
		line-height: 1;
	}
	.trip {
		min-width: 0;
		flex: 1;
		display: grid;
		text-align: left;
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.12);
		color: #fff;
		border-radius: 10px;
		padding: 4px 10px;
	}
	.trip strong,
	.trip small {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.trip small {
		color: #b9cad8;
	}
	.actions {
		display: flex;
		gap: 6px;
	}
	.small {
		font-size: 0.85rem;
	}
	.top .ghost {
		color: #fff;
		border-color: rgba(255, 255, 255, 0.3);
	}
	button.small {
		padding: 7px 12px;
	}

	.sheet {
		flex: 1;
		display: grid;
		place-items: start center;
		padding: 16px;
	}
	.sheet-card {
		width: min(640px, 100%);
		background: var(--panel);
		border-radius: 16px;
		padding: 18px;
		box-shadow: var(--shadow);
	}

	.layout {
		flex: 1;
		display: grid;
		grid-template-columns: minmax(0, 1fr) 400px;
		min-height: 0;
		height: calc(100dvh - 58px);
	}
	.mapcol {
		position: relative;
		min-height: 0;
	}
	.panel {
		overflow-y: auto;
		padding: 12px 14px 24px;
		background: var(--bg);
		border-left: 1px solid var(--line);
		display: grid;
		align-content: start;
		gap: 10px;
	}

	.ctrl {
		position: absolute;
		z-index: 2;
		display: flex;
		gap: 4px;
		background: var(--panel);
		border-radius: 12px;
		padding: 4px;
		box-shadow: var(--shadow);
	}
	.ctrl button,
	.seg button,
	.tabs button {
		border: 0;
		background: none;
		color: var(--text);
		padding: 6px 10px;
		border-radius: 8px;
		font-size: 0.85rem;
		white-space: nowrap;
	}
	.ctrl button.on,
	.seg button.on {
		background: var(--brand-2);
		color: #fff;
	}
	.ctrl button:disabled {
		opacity: 0.4;
	}
	.layers {
		top: 10px;
		left: 10px;
		right: 60px;
		width: max-content;
		max-width: calc(100% - 70px);
		overflow-x: auto;
	}
	.models {
		top: 58px;
		left: 10px;
	}
	.models select {
		border: 0;
		background: none;
		color: var(--text);
		font: inherit;
		font-size: 0.85rem;
		padding: 4px 6px;
	}
	.hint {
		font-size: 0.8rem;
		padding: 4px 8px;
		color: var(--muted);
	}
	.basemap {
		top: 104px;
		left: 10px;
	}
	.timeline {
		position: absolute;
		z-index: 2;
		left: 10px;
		right: 10px;
		bottom: 30px;
		background: var(--panel);
		border-radius: 12px;
		padding: 8px 10px;
		box-shadow: var(--shadow);
		display: grid;
		gap: 4px;
	}
	.legend {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.75rem;
		color: var(--muted);
	}
	.legend .bar {
		flex: 1;
		height: 8px;
		border-radius: 4px;
	}
	.tl-row {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.tl-row input {
		flex: 1;
		accent-color: var(--accent);
	}
	.play {
		width: 38px;
		height: 38px;
		border-radius: 50%;
		border: 0;
		background: var(--accent);
		color: #fff;
		font-size: 0.9rem;
	}
	.when {
		font-variant-numeric: tabular-nums;
		font-weight: 600;
		min-width: 110px;
		text-align: right;
		font-size: 0.9rem;
		text-transform: capitalize;
	}
	.loading {
		position: absolute;
		z-index: 3;
		top: 10px;
		left: 50%;
		transform: translate(-50%, 50px);
		background: var(--brand);
		color: #fff;
		padding: 6px 12px;
		border-radius: 20px;
		font-size: 0.8rem;
	}

	.tabs {
		display: flex;
		gap: 4px;
		background: var(--panel);
		border-radius: 12px;
		padding: 4px;
		position: sticky;
		top: 0;
		z-index: 1;
		box-shadow: var(--shadow);
	}
	.tabs button {
		flex: 1;
	}
	.tabs button.on {
		background: var(--accent);
		color: #fff;
		font-weight: 600;
	}
	.seg {
		display: flex;
		gap: 4px;
	}
	.seg button {
		border: 1px solid var(--line-strong);
	}
	.muted {
		color: var(--muted);
	}
	h4 {
		margin: 6px 0 0;
		font-size: 0.85rem;
		color: var(--muted);
	}
	.spread {
		margin: 0;
		padding: 8px 10px;
		border-radius: 10px;
		background: color-mix(in srgb, var(--go) 14%, transparent);
		font-size: 0.85rem;
	}
	.spread.hi {
		background: color-mix(in srgb, var(--nogo) 16%, transparent);
	}
	table.area {
		width: 100%;
		border-collapse: collapse;
		font-variant-numeric: tabular-nums;
		font-size: 0.88rem;
		background: var(--panel);
		border-radius: 10px;
		overflow: hidden;
	}
	.area th {
		text-align: left;
		color: var(--muted);
		font-weight: 600;
		font-size: 0.78rem;
	}
	.area td,
	.area th {
		padding: 6px 8px;
		border-top: 1px solid var(--line);
	}
	.sw,
	.keys i {
		display: inline-block;
		width: 9px;
		height: 9px;
		border-radius: 2px;
		margin-right: 6px;
	}
	.keys {
		display: flex;
		flex-wrap: wrap;
		gap: 4px 12px;
		font-size: 0.8rem;
	}
	.link {
		border: 0;
		background: none;
		color: var(--accent);
		text-decoration: underline;
		padding: 0 4px;
	}
	.errors {
		font-size: 0.82rem;
		background: color-mix(in srgb, var(--caution) 14%, transparent);
		border-radius: 10px;
		padding: 6px 10px;
	}
	.errors ul {
		margin: 6px 0 0;
		padding-left: 18px;
	}
	.budget {
		margin: 8px 0 0;
		font-size: 0.72rem;
		color: var(--muted);
	}
	.budget.warn {
		color: var(--nogo);
	}
	.toast {
		position: fixed;
		left: 50%;
		bottom: 24px;
		transform: translateX(-50%);
		background: var(--brand);
		color: #fff;
		padding: 10px 16px;
		border-radius: 12px;
		box-shadow: var(--shadow);
		z-index: 20;
	}

	@media (max-width: 900px) {
		.layout {
			display: block;
			height: auto;
		}
		.mapcol {
			height: 62dvh;
		}
		.panel {
			border-left: 0;
		}
		.has-trip .brand span {
			display: none;
		}
		.when {
			min-width: 0;
			font-size: 0.8rem;
		}
	}
</style>
