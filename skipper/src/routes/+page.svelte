<script lang="ts">
	import '../app.css';
	import { onDestroy, onMount } from 'svelte';
	import { replaceState } from '$app/navigation';
	import MapView, { type Base } from '#lib/components/MapView.svelte';
	import LineChart, { type Line } from '#lib/components/LineChart.svelte';
	import TripForm from '#lib/components/TripForm.svelte';
	import Verdicts from '#lib/components/Verdicts.svelte';
	import Footer from '#lib/components/Footer.svelte';
	import ModuleMenu from '#lib/components/ModuleMenu.svelte';
	import { BRAND } from '#lib/brand.ts';
	import {
		fetchAtmoGrids,
		fetchExtraGrid,
		type ExtraGrid,
		type Series,
		onRateWait,
		fetchMarineGrid,
		fetchPoint,
		fetchPointMarine,
		callsToday,
		DAILY_LIMIT,
		gridForView,
		gridCovers,
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
	import { areaSeries, cellsIn, dayLabel, frame, localParts, nCells, pick, sample, seaMask, spread, stats, timeIndex } from '#lib/meteo/grid.ts';
	import { LAYERS, cssGradient, type LayerId } from '#lib/meteo/layers.ts';
	import { MODELS, modelById } from '#lib/meteo/models.ts';
	import { arrow, cardinal, num, windName } from '#lib/meteo/format.ts';
	import { isobars } from '#lib/map/isobars.ts';
	import { decodeTrip, defaultTrip, inviteUrl, loadSavedTrip, saveTrip, type Trip } from '#lib/trip.ts';
	import { reportImage, reportText, shareReport } from '#lib/report.ts';

	// ----- Uscita -----
	let trip = $state<Trip | null>(null);
	let editing = $state(false);

	// ----- Dati -----
	let atmo: Record<string, AtmoGrid> = $state.raw({});
	let atmoErr: Record<string, string> = $state.raw({});
	let marine: MarineGrid | null = $state.raw(null);
	/** Pressione e pioggia del modello mostrato (scaricate solo con quei livelli attivi). */
	let extra: ExtraGrid | null = $state.raw(null);
	let gen = 0;
	let marineErr: string | null = $state(null);
	let loading = $state(0);
	/** Griglia dei dati: segue la zona inquadrata sulla mappa. */
	let grid = $state.raw<Grid | null>(null);
	let calls = $state(0);
	let rateWait: number | null = $state(null);
	onRateWait((s) => (rateWait = s));
	let viewTimer: ReturnType<typeof setTimeout> | undefined;

	// ----- Vista -----
	let layerId: LayerId = $state('wind');
	let modelId = $state(MODELS[0].id);
	let base: Base = $state('light');
	let seamarks = $state(true);
	let particlesOn = $state(true);
	let isobarsOn = $state(true);
	/** Menu della barra strumenti aperto. */
	let menu: 'layer' | 'model' | 'map' | null = $state(null);
	const toggleMenu = (m: 'layer' | 'model' | 'map') => (menu = menu === m ? null : m);
	let tab: 'verdict' | 'area' | 'point' | 'synoptic' = $state('verdict');
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
		extra = null;
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
			if (grid && gridCovers(grid, b)) return;
			const g = gridForView(b);
			grid = g;
			load($state.snapshot(trip) as Trip, g);
		}, 900); // si attende che la mappa sia ferma: zoom e spostamenti di fila non sprecano chiamate
	}

	async function load(t: Trip, g: Grid) {
		const my = ++gen;
		atmoErr = {};
		marineErr = null;
		const jobs: Promise<void>[] = [
			(async () => {
				try {
					const got = await fetchAtmoGrids(t, t.models, g);
					if (gen !== my) return;
					atmo = { ...atmo, ...got };
					const missing = t.models.filter((m) => !got[m]);
					atmoErr = Object.fromEntries(missing.map((m) => [m, 'nessun dato per questa zona o per queste date']));
					const first = Object.values(got)[0];
					if (first && ti < 0) ti = startIndex(first.times, first.utcOffset);
				} catch (e) {
					if (gen === my) atmoErr = Object.fromEntries(t.models.map((m) => [m, (e as Error).message]));
				}
			})()
		];
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

	const at = (g: Series) => timeIndex(g, now);

	const field = $derived.by(() => {
		if (!times.length) return null;
		if (layerId === 'wave') return marine ? { grid: marine.grid, values: frame(marine, 'wave', at(marine)) } : null;
		if (layerId === 'spread') {
			if (!grid || loadedModels.length < 2) return null;
			const frames = loadedModels.map((m) => frame(atmo[m], 'wind', at(atmo[m])));
			return { grid, values: spread(frames, nCells(grid)) };
		}
		if (layerId === 'pressure' || layerId === 'precip') return extra ? { grid: extra.grid, values: frame(extra, layerId, at(extra)) } : null;
		return mapModel ? { grid: mapModel.grid, values: frame(mapModel, layerId, at(mapModel)) } : null;
	});

	// Sinottica: isobare dalla pressione del modello mostrato, all'ora selezionata.
	const isobarFc = $derived.by(() => {
		if (!isobarsOn || !extra) return null;
		return isobars(extra.grid, frame(extra, 'pressure', at(extra)));
	});

	// Livelli Pressione/Pioggia e isobare: scarica la griglia extra per il modello mostrato quando serve.
	$effect(() => {
		if ((layerId !== 'pressure' && layerId !== 'precip' && !isobarsOn) || !trip || !grid) return;
		if (extra && extra.model === modelId && isCurrent(extra)) return;
		const t = $state.snapshot(trip) as Trip;
		const g = grid;
		const m = modelId;
		fetchExtraGrid(t, m, g)
			.then((d) => {
				if (grid === g && modelId === m) extra = d;
				calls = callsToday();
			})
			.catch((e) => flash(`Pressione/pioggia non disponibili: ${(e as Error).message}`));
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
		const [pd, pm] = await Promise.all([fetchPoint(t, lat, lon, t.models).catch(() => []), fetchPointMarine(t, lat, lon).catch(() => null)]);
		if (my !== pointGen) return;
		pointData = pd;
		pointMarine = pm && pm.wave.some((x) => !Number.isNaN(x)) ? pm : null;
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

	// ----- Valori nel punto toccato, all'ora selezionata -----
	interface PointRow {
		model: string;
		label: string;
		color: string;
		wind: number;
		dir: number;
		gust: number;
		precip: number;
		pressure: number;
	}

	/** Prima i valori interpolati dalla griglia (subito), poi quelli esatti del punto quando arrivano. */
	const pointNow = $derived.by(() => {
		if (!point || !now) return null;
		const { lat, lon } = point;
		let rows: PointRow[];
		if (pointData.length) {
			rows = pointData.map((p) => {
				const k = timeIndex(p, now);
				const info = modelById(p.model);
				return { model: p.model, label: info?.label ?? p.model, color: info?.color ?? '#888', wind: p.wind[k], dir: p.dir[k], gust: p.gust[k], precip: p.precip[k], pressure: p.pressure[k] };
			});
		} else {
			rows = loadedModels.map((m) => {
				const g = atmo[m];
				const k = at(g);
				const val = (v: 'wind' | 'gust' | 'precip' | 'pressure' | 'u' | 'v') => sample(g.grid, frame(g, v, k), lon, lat);
				const u = val('u');
				const v = val('v');
				const dir = (Math.atan2(-u, -v) * 180) / Math.PI;
				const info = modelById(m)!;
				return { model: m, label: info.label, color: info.color, wind: val('wind'), dir: (dir + 360) % 360, gust: val('gust'), precip: val('precip'), pressure: val('pressure') };
			});
		}
		let sea: { wave: number; waveDir: number; period: number; swell: number } | null = null;
		if (pointMarine) {
			const k = timeIndex(pointMarine, now);
			sea = { wave: pointMarine.wave[k], waveDir: pointMarine.waveDir[k], period: pointMarine.period[k], swell: pointMarine.swell[k] };
		} else if (marine && !pointLoading && !pointData.length) {
			const k = at(marine);
			const f = (v: 'wave' | 'waveDir' | 'wavePeriod' | 'swell') => sample(marine!.grid, frame(marine!, v, k), lon, lat);
			if (!Number.isNaN(f('wave'))) sea = { wave: f('wave'), waveDir: f('waveDir'), period: f('wavePeriod'), swell: f('swell') };
		}
		return { rows, sea, exact: pointData.length > 0 };
	});

	const popup = $derived.by(() => {
		if (!pointNow) return null;
		const lim = trip!.limits;
		const over = (x: number, l: number) => (x > l ? ' class="over"' : '');
		const rows = pointNow.rows
			.map(
				(r) =>
					`<tr><td><i style="background:${r.color}"></i>${r.label}</td><td${over(r.wind, lim.wind)}>${num(r.wind)} ${arrow(r.dir)} ${cardinal(r.dir)}</td><td${over(r.gust, lim.gust)}>${num(r.gust)}</td><td>${num(r.precip, 1)}</td><td>${num(r.pressure)}</td></tr>`
			)
			.join('');
		const sea = pointNow.sea
			? `<p class="sea"><b>Onda</b> <span${over(pointNow.sea.wave, lim.wave)}>${num(pointNow.sea.wave, 1)} m</span> ${arrow(pointNow.sea.waveDir)} ${cardinal(pointNow.sea.waveDir)} · periodo ${num(pointNow.sea.period, 1)} s · mare lungo ${num(pointNow.sea.swell, 1)} m</p>`
			: '<p class="sea muted">Onda: nessun dato (terraferma?)</p>';
		const dirs = pointNow.rows.map((r) => r.dir).filter(Number.isFinite);
		const name = dirs.length ? windName(dirs[0]) : '';
		// Riassunto per schermi piccoli: intervallo tra i modelli.
		const range = (xs: number[], d = 0) => {
			const v = xs.filter(Number.isFinite);
			if (!v.length) return '—';
			const lo = Math.min(...v);
			const hi = Math.max(...v);
			return lo.toFixed(d) === hi.toFixed(d) ? num(lo, d) : `${num(lo, d)}–${num(hi, d)}`;
		};
		const R = pointNow.rows;
		const compact = `<p><b>Vento</b> ${range(R.map((r) => r.wind))} kn ${dirs.length ? `${arrow(dirs[0])} ${cardinal(dirs[0])}` : ''} · <b>raffiche</b> ${range(R.map((r) => r.gust))} kn</p>
<p><b>Pioggia</b> ${range(R.map((r) => r.precip), 1)} mm · <b>pressione</b> ${range(R.map((r) => r.pressure))} hPa</p>
${pointNow.sea ? `<p><b>Onda</b> ${num(pointNow.sea.wave, 1)} m ${arrow(pointNow.sea.waveDir)} ${cardinal(pointNow.sea.waveDir)} · ${num(pointNow.sea.period, 1)} s</p>` : ''}
<p class="muted">${R.length} modelli · dettaglio sotto la mappa</p>`;
		return `<div class="pp"><p class="pp-h"><b>${timeLabel}</b>${name ? ` · ${name}` : ''}</p>
<div class="pp-full"><table><thead><tr><th>Modello</th><th>Vento kn (da)</th><th>Raff.</th><th>Pioggia mm</th><th>hPa</th></tr></thead><tbody>${rows}</tbody></table>${sea}</div>
<div class="pp-compact">${compact}</div></div>`;
	});
</script>

<svelte:head>
	<title>{trip && !editing ? `${trip.name} · Skipper Meteo` : 'Skipper Meteo'}</title>
</svelte:head>

<div class="app">
	<header class="top" class:has-trip={trip && !editing}>
		<ModuleMenu compact={!!trip && !editing} />
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
					{popup}
					isobars={isobarFc}
					onpick={(lat, lon) => (menu ? (menu = null) : pickPoint(lat, lon))}
					onclosepoint={() => (point = null)}
					onview={onView}
				/>

				<!-- Barra verticale compatta: ogni icona apre un piccolo menu a fianco. -->
				<div class="toolbar">
					<button class="tb" class:on={menu === 'layer'} onclick={() => toggleMenu('layer')} title="Livello: {layer.label}" aria-label="Livello">
						<svg viewBox="0 0 24 24"><path d="M12 3 2 8l10 5 10-5-10-5Zm-10 9 10 5 10-5M2 16l10 5 10-5" /></svg>
					</button>
					<button class="tb" class:on={menu === 'model'} onclick={() => toggleMenu('model')} title="Modello" aria-label="Modello">
						<svg viewBox="0 0 24 24"><path d="M4 19V5l8 8 8-8v14" /></svg>
					</button>
					<button class="tb" class:on={menu === 'map'} onclick={() => toggleMenu('map')} title="Mappa e sovrapposizioni" aria-label="Mappa">
						<svg viewBox="0 0 24 24"><path d="m3 6 6-2 6 2 6-2v14l-6 2-6-2-6 2V6Zm6-2v14m6-12v14" /></svg>
					</button>
					<button class="tb" onclick={() => mapView?.goHome()} title="Torna alla zona dell'uscita" aria-label="Zona dell'uscita">
						<svg viewBox="0 0 24 24"><path d="M3 11 12 4l9 7M5 10v10h14V10" /></svg>
					</button>

					{#if menu}
						<div class="flyout" role="menu">
							{#if menu === 'layer'}
								<p class="fl-h">Livello</p>
								{#each Object.values(LAYERS) as l (l.id)}
									<button class="fl-item" class:on={layerId === l.id} disabled={l.id === 'spread' && loadedModels.length < 2} onclick={() => ((layerId = l.id), (menu = null))}>
										<span class="sw" style="background: {cssGradient(l)}"></span>{l.label}
									</button>
								{/each}
							{:else if menu === 'model'}
								<p class="fl-h">Modello sulla mappa</p>
								{#if layerId === 'spread'}<p class="fl-note">Il livello "Disaccordo" usa tutti i modelli.</p>{/if}
								{#if layerId === 'wave'}<p class="fl-note">L'onda usa il miglior modello marino.</p>{/if}
								{#each trip.models as m (m)}
									<button class="fl-item" class:on={modelId === m} disabled={!atmo[m]} onclick={() => ((modelId = m), (menu = null))}>
										<i style="background: {modelById(m)?.color}"></i>{modelById(m)?.label ?? m}
										<small>{atmoErr[m] ? 'non disp.' : !atmo[m] ? '…' : `${modelById(m)?.km} km`}</small>
									</button>
								{/each}
							{:else if menu === 'map'}
								<p class="fl-h">Mappa</p>
								<div class="fl-seg">
									<button class:on={base === 'light'} onclick={() => (base = 'light')}>Chiara</button>
									<button class:on={base === 'satellite'} onclick={() => (base = 'satellite')}>Satellite</button>
								</div>
								<label class="fl-check"><input type="checkbox" bind:checked={isobarsOn} /> Isobare (sinottica)</label>
								<label class="fl-check"><input type="checkbox" bind:checked={particlesOn} /> Particelle del vento</label>
								<label class="fl-check"><input type="checkbox" bind:checked={seamarks} /> Segnali nautici</label>
							{/if}
						</div>
					{/if}
				</div>

				<div class="timeline">
					<button class="play" onclick={togglePlay} aria-label={playing ? 'Pausa' : 'Riproduci'}>{playing ? '❚❚' : '▶'}</button>
					<div class="tl-mid">
						<input type="range" min="0" max={Math.max(0, times.length - 1)} bind:value={ti} aria-label="Ora" />
						<div class="legend" title="{layer.label} ({layer.unit})">
							<span class="bar" style="background: {cssGradient(layer)}"></span>
							<span class="lim">{layer.stops[0][0]}–{layer.stops[layer.stops.length - 1][0]} {layer.unit}</span>
						</div>
					</div>
					<span class="when">{timeLabel}</span>
				</div>

				{#if rateWait}
					<div class="loading">Attendo il limite al minuto di Open-Meteo… {rateWait} s</div>
				{:else if loading > 0}
					<div class="loading">Carico i modelli…</div>
				{/if}
			</section>

			<aside class="panel">
				<nav class="tabs">
					<button class:on={tab === 'verdict'} onclick={() => (tab = 'verdict')}>Valutazione</button>
					<button class:on={tab === 'area'} onclick={() => (tab = 'area')}>Area</button>
					<button class:on={tab === 'point'} onclick={() => (tab = 'point')}>Punto</button>
					<button class:on={tab === 'synoptic'} onclick={() => (tab = 'synoptic')}>Sinottica</button>
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
				{:else if tab === 'synoptic'}
					<div class="syn">
						<h4>Isobare del modello sulla mappa</h4>
						<p class="small">
							Isobare ogni 2–4 hPa e centri di <b class="hi">A</b>lta e <b class="lo">B</b>assa pressione di {modelById(modelId)?.label}, all'ora della barra del tempo:
							premi ▶ per vedere i sistemi muoversi. Zooma indietro per la visione d'insieme.
						</p>
						<label class="fl-check"><input type="checkbox" bind:checked={isobarsOn} /> Mostra le isobare</label>
						<h4>Analisi al suolo ufficiale (DWD)</h4>
						<a href="https://www.dwd.de/DE/leistungen/hobbymet_wk_europa/hobbyeuropakarten.html" target="_blank" rel="noopener">
							<img class="chart-img" src="https://www.dwd.de/DWD/wetter/wv_spez/hobbymet/wetterkarten/bwk_bodendruck_na_ana.png" alt="Analisi della pressione al suolo, Nord Atlantico ed Europa" loading="lazy" />
						</a>
						<p class="small muted">Analisi più recente del Deutscher Wetterdienst (fronti e isobare). Fonte: DWD.</p>
						<h4>Carte e bollettini ufficiali</h4>
						<ul class="links">
							<li><a href="https://weather.metoffice.gov.uk/maps-and-charts/surface-pressure" target="_blank" rel="noopener">Met Office — analisi e previsioni al suolo fino a 5 giorni</a></li>
							<li><a href="https://www.dwd.de/DE/leistungen/hobbymet_wk_europa/hobbyeuropakarten.html" target="_blank" rel="noopener">DWD — carte del tempo per l'Europa</a></li>
							<li><a href="https://www.meteoam.it/it/meteo-mare" target="_blank" rel="noopener">Aeronautica Militare — bollettino del mare</a></li>
						</ul>
					</div>
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
						{#if popup}
							<div class="point-now">{@html popup}</div>
							<p class="muted small">{pointNow?.exact ? 'Valori nel punto' : 'Valori interpolati dalla griglia, in attesa dei dati esatti del punto'}. Sposta la barra del tempo per cambiare ora.</p>
						{/if}
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
						{#if pointData.length}
							<h4>Pioggia (mm/h)</h4>
							<LineChart
								times={pointData[0].times}
								utcOffset={pointData[0].utcOffset}
								lines={pointData.map((p) => ({ label: p.model, color: modelById(p.model)?.color ?? '#888', values: p.precip }))}
								unit="mm"
								cursor={ti}
								onseek={(i) => (ti = i)}
								height={110}
							/>
						{/if}
						{#if pointMarine}
							<h4>Onda significativa (linea) e mare lungo (tratteggio)</h4>
							<LineChart
								times={pointMarine.times}
								utcOffset={pointMarine.utcOffset}
								lines={[
									{ label: 'Onda', color: '#0f4c5c', values: pointMarine.wave },
									{ label: 'Mare lungo', color: '#5fc2d6', values: pointMarine.swell, dashed: true }
								]}
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
					Chiamate Open-Meteo oggi da questo dispositivo: ~{Math.round(calls).toLocaleString('it-IT')} / {DAILY_LIMIT.toLocaleString('it-IT')}
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
	/* Su schermi larghi l'app occupa esattamente lo schermo: mappa fissa, pannello che scorre. */
	@media (min-width: 901px) {
		.app:has(.layout) {
			height: 100dvh;
		}
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
		/* La riga resta alta quanto lo schermo: il pannello scorre, la mappa non si deforma. */
		grid-template-rows: minmax(0, 1fr);
		min-height: 0;
	}
	.mapcol {
		position: relative;
		min-height: 0;
	}
	.panel {
		min-height: 0;
		overflow-y: auto;
		padding: 12px 14px 24px;
		background: var(--bg);
		border-left: 1px solid var(--line);
		display: grid;
		align-content: start;
		gap: 10px;
	}

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
	.seg button.on {
		background: var(--brand-2);
		color: #fff;
	}

	/* Barra degli strumenti verticale, discreta. */
	.toolbar {
		position: absolute;
		z-index: 4;
		top: 10px;
		left: 10px;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.tb {
		width: 38px;
		height: 38px;
		display: grid;
		place-items: center;
		border: 0;
		border-radius: 10px;
		background: var(--panel);
		color: var(--text);
		box-shadow: var(--shadow);
		padding: 0;
	}
	.tb svg {
		width: 20px;
		height: 20px;
		fill: none;
		stroke: currentColor;
		stroke-width: 1.8;
		stroke-linejoin: round;
		stroke-linecap: round;
	}
	.tb.on {
		background: var(--brand-2);
		color: #fff;
	}
	.flyout {
		position: absolute;
		left: 46px;
		top: 0;
		min-width: 190px;
		max-height: 60vh;
		overflow-y: auto;
		background: var(--panel);
		border-radius: 12px;
		box-shadow: var(--shadow);
		padding: 6px;
		display: grid;
		gap: 2px;
	}
	.fl-h {
		margin: 2px 6px 4px;
		font-size: 0.7rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--muted);
	}
	.fl-note {
		margin: 0 6px 4px;
		font-size: 0.75rem;
		color: var(--muted);
	}
	.fl-item {
		display: flex;
		align-items: center;
		gap: 8px;
		border: 0;
		background: none;
		color: var(--text);
		padding: 7px 8px;
		border-radius: 8px;
		font-size: 0.85rem;
		text-align: left;
	}
	.fl-item small {
		margin-left: auto;
		color: var(--muted);
		font-size: 0.72rem;
	}
	.fl-item.on {
		background: var(--accent-soft);
		font-weight: 600;
	}
	.fl-item:disabled {
		opacity: 0.4;
	}
	.fl-item .sw {
		width: 22px;
		height: 8px;
		border-radius: 4px;
		margin: 0;
	}
	.fl-item i {
		width: 9px;
		height: 9px;
		border-radius: 2px;
	}
	.fl-seg {
		display: flex;
		gap: 4px;
		padding: 0 4px 4px;
	}
	.fl-seg button {
		flex: 1;
		border: 1px solid var(--line-strong);
		background: none;
		color: var(--text);
		border-radius: 8px;
		padding: 6px;
		font-size: 0.82rem;
	}
	.fl-seg button.on {
		background: var(--brand-2);
		border-color: var(--brand-2);
		color: #fff;
	}
	.fl-check {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 8px;
		font-size: 0.85rem;
	}

	/* Barra del tempo compatta: play, cursore con scala colori sotto, ora. */
	.timeline {
		position: absolute;
		z-index: 2;
		left: 10px;
		right: 10px;
		bottom: 28px;
		max-width: 640px;
		margin: 0 auto;
		background: color-mix(in srgb, var(--panel) 92%, transparent);
		border-radius: 22px;
		padding: 4px 12px 4px 4px;
		box-shadow: var(--shadow);
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.tl-mid {
		flex: 1;
		display: grid;
		gap: 1px;
		min-width: 0;
	}
	.tl-mid input {
		width: 100%;
		margin: 0;
		accent-color: var(--accent);
	}
	.legend {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.66rem;
		color: var(--muted);
	}
	.legend .bar {
		flex: 1;
		height: 4px;
		border-radius: 2px;
	}
	.play {
		flex: none;
		width: 32px;
		height: 32px;
		border-radius: 50%;
		border: 0;
		background: var(--accent);
		color: #fff;
		font-size: 0.75rem;
	}
	.when {
		flex: none;
		font-variant-numeric: tabular-nums;
		font-weight: 600;
		text-align: right;
		font-size: 0.8rem;
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
	.syn h4 {
		margin: 10px 0 4px;
	}
	.syn .hi {
		color: #2f6fdb;
	}
	.syn .lo {
		color: #d64545;
	}
	.chart-img {
		width: 100%;
		border-radius: 10px;
		display: block;
		background: var(--panel);
	}
	.links {
		margin: 0;
		padding-left: 18px;
		font-size: 0.85rem;
		display: grid;
		gap: 4px;
	}
	.point-now {
		background: var(--panel);
		border-radius: 10px;
		padding: 8px 10px;
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
		.timeline {
			left: 6px;
			right: 6px;
			bottom: 22px;
		}
		.when {
			font-size: 0.72rem;
		}
		.tb {
			width: 34px;
			height: 34px;
		}
	}
</style>
