<script lang="ts">
	import type { Feature, FeatureCollection } from 'geojson';
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import MapView from '#lib/components/MapView.svelte';
	import { fetchAtmoGrids, fetchMarineGrid, gridForView, homeBox, type AtmoGrid, type BBox } from '#lib/meteo/api.ts';
	import { frame, localParts, sample, timeIndex, dayLabel } from '#lib/meteo/grid.ts';
	import { LAYERS } from '#lib/meteo/layers.ts';
	import { MODELS, modelById } from '#lib/meteo/models.ts';
	import { cardinal, latDM, lonDM, num } from '#lib/meteo/format.ts';
	import { MAX_LEAD_DAYS, addDays, defaultTrip, isoDate, loadSavedTrip, type Trip } from '#lib/trip.ts';
	import { persisted, shareText } from '#lib/persist.svelte.ts';
	import { BUILTIN_POLARS, parsePolar, type Polar } from '#lib/routing/polars.ts';
	import { computeRoute, distNm, type LonLat, type RouteResult } from '#lib/routing/router.ts';

	const RAD = Math.PI / 180;
	/** Punti massimi della griglia di routing: più fitta della mappa meteo, per seguire meglio la costa. */
	const ROUTE_POINTS = 220;
	const MAX_HOURS = 72;

	const trip: Trip = loadSavedTrip() ?? defaultTrip();
	const settings = persisted('rotta', {
		polarId: 'cruiser-38',
		efficiency: 85,
		motorOn: true,
		motorBelow: 3,
		motorSpeed: 6,
		model: 'ecmwf_ifs025'
	});
	const customPolars = persisted<Polar[]>('polari', []);
	const polars = $derived([...BUILTIN_POLARS, ...customPolars.value]);
	const polar = $derived(polars.find((p) => p.id === settings.value.polarId) ?? BUILTIN_POLARS[1]);

	let start: LonLat = $state({ lon: trip.lon, lat: trip.lat });
	let end = $state<LonLat | null>(null);
	let picking: 'start' | 'end' = $state('end');
	let depart = $state(`${trip.date}T08:00`);
	let busy = $state(false);
	let error: string | null = $state(null);
	let result = $state.raw<RouteResult | null>(null);
	let windGrid = $state.raw<AtmoGrid | null>(null);
	let base: 'light' | 'satellite' = $state('light');
	let importMsg: string | null = $state(null);

	const home: BBox = homeBox(trip);
	const today = isoDate(new Date());

	function pick(lat: number, lon: number) {
		if (picking === 'start') {
			start = { lat, lon };
			picking = 'end';
		} else end = { lat, lon };
		result = null;
	}

	async function onPolarFile(e: Event) {
		const file = (e.currentTarget as HTMLInputElement).files?.[0];
		if (!file) return;
		try {
			const p = parsePolar(await file.text(), file.name.replace(/\.[^.]+$/, ''));
			customPolars.value = [...customPolars.value, p];
			settings.value.polarId = p.id;
			importMsg = `Polare "${p.name}" importata: ${p.twa.length} angoli × ${p.tws.length} venti.`;
		} catch (err) {
			importMsg = `Impossibile leggere il file: ${(err as Error).message}`;
		}
	}

	async function compute() {
		if (!end) return;
		error = null;
		result = null;
		busy = true;
		try {
			const departDate = depart.slice(0, 10);
			if (departDate < today || departDate > addDays(today, MAX_LEAD_DAYS)) throw new Error(`La partenza deve essere entro ${MAX_LEAD_DAYS} giorni da oggi.`);
			const span = Math.max(Math.abs(end.lon - start.lon), Math.abs(end.lat - start.lat));
			const m = Math.max(0.4, span * 0.3);
			const box: BBox = [Math.min(start.lon, end.lon) - m, Math.min(start.lat, end.lat) - m, Math.max(start.lon, end.lon) + m, Math.max(start.lat, end.lat) + m];
			const grid = gridForView(box, ROUTE_POINTS);
			const window: Trip = { ...trip, date: departDate, days: 3 };
			const model = settings.value.model;
			const [atmo, marine] = await Promise.all([fetchAtmoGrids(window, [model], grid), fetchMarineGrid(window, grid).catch(() => null)]);
			const g = atmo[model];
			if (!g) throw new Error(`Il modello ${modelById(model)?.label ?? model} non ha dati per questa zona o queste date.`);
			windGrid = g;

			// L'ora di partenza è locale della zona.
			const [y, mo, d] = departDate.split('-').map(Number);
			const [hh, mm] = depart.slice(11, 16).split(':').map(Number);
			const t0 = Date.UTC(y, mo - 1, d, hh, mm) / 1000 - g.utcOffset;

			const N = g.grid.lats.length * g.grid.lons.length;
			const wind = (lon: number, lat: number, t: number) => {
				const x = (t - g.times[0]) / 3600;
				if (x < 0 || x > g.times.length - 1) return null;
				const i0 = Math.floor(x);
				const i1 = Math.min(g.times.length - 1, i0 + 1);
				const f = x - i0;
				const at = (key: 'u' | 'v', i: number) => sample(g.grid, frame(g, key, i), lon, lat);
				const u = at('u', i0) * (1 - f) + at('u', i1) * f;
				const v = at('v', i0) * (1 - f) + at('v', i1) * f;
				if (!Number.isFinite(u) || !Number.isFinite(v)) return null;
				return { tws: Math.hypot(u, v), twd: (Math.atan2(-u, -v) / RAD + 360) % 360 };
			};
			// Mare: celle con dati d'onda. Senza dati marini non si può evitare la costa.
			let sea = (_lon: number, _lat: number) => true;
			if (marine) {
				const mask = new Float32Array(N);
				for (let i = 0; i < marine.values.wave.length; i++) if (!Number.isNaN(marine.values.wave[i])) mask[i % N] = 1;
				sea = (lon, lat) => sample(marine.grid, mask, lon, lat) >= 0.5;
			} else error = 'Dati del mare non disponibili: la rotta non tiene conto della costa.';

			const hoursLeft = Math.floor((g.times[g.times.length - 1] - t0) / 3600);
			if (hoursLeft < 1) throw new Error('La partenza è oltre l’ultima ora di previsione disponibile.');
			// Il calcolo è sincrono: si lascia prima aggiornare l'interfaccia.
			await new Promise((r) => setTimeout(r, 30));
			result = computeRoute({
				start,
				end,
				t0,
				maxHours: Math.min(MAX_HOURS, hoursLeft),
				polar,
				efficiency: settings.value.efficiency / 100,
				motor: settings.value.motorOn ? { below: settings.value.motorBelow, speed: settings.value.motorSpeed } : null,
				wind,
				sea,
				dt: 1,
				headingStep: 5,
				sectorDeg: 2
			});
		} catch (e) {
			error = (e as Error).message;
		} finally {
			busy = false;
		}
	}

	const overlay: FeatureCollection = $derived.by(() => {
		const f: Feature[] = [];
		if (result) {
			for (const iso of result.isochrones) if (iso.length > 1) f.push({ type: 'Feature', properties: { kind: 'iso' }, geometry: { type: 'LineString', coordinates: iso.map((p) => [p.lon, p.lat]) } });
			const pts = result.points;
			for (let i = 1; i < pts.length; i++)
				f.push({ type: 'Feature', properties: { kind: 'route', motor: pts[i - 1].motor }, geometry: { type: 'LineString', coordinates: [[pts[i - 1].lon, pts[i - 1].lat], [pts[i].lon, pts[i].lat]] } });
			pts.forEach((p, i) => i > 0 && i < pts.length - 1 && i % 3 === 0 && f.push({ type: 'Feature', properties: { kind: 'step' }, geometry: { type: 'Point', coordinates: [p.lon, p.lat] } }));
		}
		f.push({ type: 'Feature', properties: { kind: 'start' }, geometry: { type: 'Point', coordinates: [start.lon, start.lat] } });
		if (end) f.push({ type: 'Feature', properties: { kind: 'end' }, geometry: { type: 'Point', coordinates: [end.lon, end.lat] } });
		return { type: 'FeatureCollection', features: f };
	});

	const departIndex = $derived(windGrid && result ? timeIndex(windGrid, result.points[0].t) : -1);
	const field = $derived(windGrid && departIndex >= 0 ? { grid: windGrid.grid, values: frame(windGrid, 'wind', departIndex) } : null);
	const windFrame = $derived(windGrid && departIndex >= 0 ? { grid: windGrid.grid, u: frame(windGrid, 'u', departIndex), v: frame(windGrid, 'v', departIndex) } : null);

	const off = $derived(windGrid?.utcOffset ?? 0);
	const when = (t: number) => {
		const p = localParts(t, off);
		return `${dayLabel(p.date)} ${p.label}`;
	};
	/** Mure: vento da dritta se arriva sul lato destro della prua. */
	const tack = (heading: number, twd: number) => ((twd - heading + 360) % 360 < 180 ? 'dritta' : 'sinistra');

	async function share() {
		if (!result) return;
		const r = result;
		const lines = [
			`Rotta ${polar.name} — modello ${modelById(settings.value.model)?.label}`,
			`Partenza ${when(r.points[0].t)} da ${latDM(start.lat)} ${lonDM(start.lon)}`,
			`${r.reached ? 'Arrivo' : 'Ultimo punto'} ${when(r.points[r.points.length - 1].t)} · ${num(r.distanceNm, 1)} mn in ${num(r.hours, 1)} h${r.motorHours ? ` (motore ${num(r.motorHours, 1)} h)` : ''}`,
			'',
			...r.points
				.slice(0, -1)
				.map((p) => `${when(p.t)}  prua ${Math.round(p.heading)}°  vento ${num(p.tws)} kn da ${cardinal(p.twd)}  ${p.motor ? 'motore' : `TWA ${Math.round(p.twa)}° mure a ${tack(p.heading, p.twd)}`}  ${num(p.speed, 1)} kn`),
			'',
			'Rotta indicativa calcolata sui dati del modello: verifica sempre sulla carta nautica.'
		];
		await shareText('Rotta', lines.join('\n'));
	}
</script>

<ModuleShell title="Rotta" wide>
	<div class="layout">
		<section class="mapcol">
			<MapView
				{home}
				{field}
				layer={LAYERS.wind}
				arrows={null}
				wind={windFrame}
				{base}
				seamarks={true}
				particles={!!windFrame}
				point={null}
				isobars={null}
				{overlay}
				popup={null}
				onpick={pick}
			/>
			<div class="pickbar">
				<button class:on={picking === 'start'} onclick={() => (picking = 'start')}><i class="dot start"></i>Partenza</button>
				<button class:on={picking === 'end'} onclick={() => (picking = 'end')}><i class="dot end"></i>Arrivo</button>
				<button onclick={() => (base = base === 'light' ? 'satellite' : 'light')}>{base === 'light' ? 'Satellite' : 'Mappa'}</button>
			</div>
		</section>

		<aside class="panel">
			<h1 class="m-h1">Rotta</h1>
			<p class="m-muted">Tocca la mappa per scegliere {picking === 'start' ? 'la partenza' : 'l’arrivo'}.</p>

			<div class="m-card">
				<div class="m-grid">
					<div class="m-field">
						<span>Partenza</span>
						<p class="pt">{latDM(start.lat)}<br />{lonDM(start.lon)}</p>
					</div>
					<div class="m-field">
						<span>Arrivo</span>
						<p class="pt">{#if end}{latDM(end.lat)}<br />{lonDM(end.lon)}{:else}— tocca la mappa —{/if}</p>
					</div>
					{#if end}<p class="m-muted m-wide">Distanza diretta {num(distNm(start, end), 1)} mn</p>{/if}
					<label class="m-field m-wide"><span>Partenza (ora locale)</span><input type="datetime-local" bind:value={depart} min="{today}T00:00" /></label>
					<label class="m-field m-wide">
						<span>Barca (polare)</span>
						<select bind:value={settings.value.polarId}>
							<optgroup label="Polari tipo (indicative)">
								{#each BUILTIN_POLARS as p (p.id)}<option value={p.id}>{p.name}</option>{/each}
							</optgroup>
							{#if customPolars.value.length}
								<optgroup label="Importate">
									{#each customPolars.value as p (p.id)}<option value={p.id}>{p.name}</option>{/each}
								</optgroup>
							{/if}
						</select>
					</label>
					<label class="m-field m-wide">
						<span>Importa polare (.pol / .txt / .csv)</span>
						<input type="file" accept=".pol,.txt,.csv,.tsv" onchange={onPolarFile} />
					</label>
					{#if importMsg}<p class="m-muted m-wide">{importMsg}</p>{/if}
					<label class="m-field">
						<span>Rendimento {settings.value.efficiency}%</span>
						<input type="range" min="60" max="100" step="5" bind:value={settings.value.efficiency} />
					</label>
					<label class="m-field">
						<span>Modello meteo</span>
						<select bind:value={settings.value.model}>{#each MODELS as m (m.id)}<option value={m.id}>{m.label}</option>{/each}</select>
					</label>
					<div class="m-wide motor">
						<input type="checkbox" bind:checked={settings.value.motorOn} aria-label="Usa il motore" />
						<span>Motore sotto <input type="number" min="1" max="6" step="0.5" bind:value={settings.value.motorBelow} aria-label="Soglia motore" /> kn a vela, a
							<input type="number" min="3" max="12" step="0.5" bind:value={settings.value.motorSpeed} aria-label="Velocità a motore" /> kn</span>
					</div>
				</div>
				<div class="m-actions">
					<button class="primary" onclick={compute} disabled={!end || busy}>{busy ? 'Calcolo…' : 'Calcola rotta'}</button>
				</div>
				{#if error}<p class="err">{error}</p>{/if}
			</div>

			{#if result}
				{@const r = result}
				<div class="m-card">
					<h2>{r.reached ? 'Rotta ottima' : 'Rotta parziale'}</h2>
					{#if r.reason}<p class="err">{r.reason}</p>{/if}
					<div class="kpis">
						<div><span>{r.reached ? 'Arrivo' : 'Ultimo punto'}</span><b>{when(r.points[r.points.length - 1].t)}</b></div>
						<div><span>Durata</span><b>{num(r.hours, 1)} h</b></div>
						<div><span>Distanza</span><b>{num(r.distanceNm, 1)} mn</b></div>
						<div><span>Media</span><b>{num(r.hours ? r.distanceNm / r.hours : 0, 1)} kn</b></div>
						{#if r.motorHours}<div><span>Motore</span><b>{num(r.motorHours, 1)} h</b></div>{/if}
					</div>
					<table class="legs">
						<thead><tr><th>Ora</th><th>Prua</th><th>Vento</th><th>TWA</th><th>kn</th></tr></thead>
						<tbody>
							{#each r.points.slice(0, -1) as p (p.t)}
								<tr class:motor={p.motor}>
									<td>{when(p.t).split(' ').pop()}</td>
									<td>{Math.round(p.heading)}°</td>
									<td>{num(p.tws)} {cardinal(p.twd)}</td>
									<td>{p.motor ? 'motore' : `${Math.round(p.twa)}° ${tack(p.heading, p.twd) === 'dritta' ? 'Dr' : 'Sn'}`}</td>
									<td>{num(p.speed, 1)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					<div class="m-actions"><button class="ghost" onclick={share}>Condividi rotta</button></div>
				</div>
			{/if}

			<p class="m-muted note">
				Rotta indicativa: vento del modello {modelById(settings.value.model)?.label} su una griglia di circa 7–15 miglia, costa approssimata dai dati d'onda,
				polari tipo stimate. Verifica sempre sulla carta nautica e con i bollettini ufficiali.
			</p>
		</aside>
	</div>
</ModuleShell>

<style>
	.layout {
		flex: 1;
		display: grid;
		grid-template-columns: minmax(0, 1fr) 380px;
		grid-template-rows: minmax(0, 1fr);
		height: calc(100dvh - 58px);
	}
	.mapcol {
		position: relative;
		min-height: 0;
	}
	.panel {
		min-height: 0;
		overflow-y: auto;
		padding: 12px 14px 24px;
		border-left: 1px solid var(--line);
	}
	.pickbar {
		position: absolute;
		z-index: 3;
		top: 10px;
		left: 10px;
		display: flex;
		gap: 4px;
		background: var(--panel);
		border-radius: 12px;
		padding: 4px;
		box-shadow: var(--shadow);
	}
	.pickbar button {
		border: 0;
		background: none;
		color: var(--text);
		border-radius: 8px;
		padding: 6px 10px;
		font-size: 0.85rem;
		display: flex;
		align-items: center;
		gap: 6px;
	}
	.pickbar button.on {
		background: var(--brand-2);
		color: #fff;
	}
	.dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		border: 2px solid #fff;
	}
	.dot.start {
		background: #2e9d5b;
	}
	.dot.end {
		background: #d64545;
	}
	.pt {
		margin: 0;
		font-weight: 600;
		font-variant-numeric: tabular-nums;
	}
	.motor {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.85rem;
	}
	.motor input[type='number'] {
		width: 56px;
		padding: 4px;
		border-radius: 6px;
		border: 1px solid var(--line-strong);
		background: var(--bg);
		color: var(--text);
	}
	.err {
		color: var(--nogo);
		margin: 6px 0 0;
	}
	.kpis {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
		gap: 8px;
		margin-bottom: 10px;
	}
	.kpis div {
		background: var(--bg);
		border-radius: 10px;
		padding: 6px 8px;
		display: grid;
	}
	.kpis span {
		font-size: 0.7rem;
		color: var(--muted);
	}
	.legs {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.82rem;
		font-variant-numeric: tabular-nums;
	}
	.legs th {
		text-align: left;
		color: var(--muted);
		font-size: 0.72rem;
	}
	.legs td,
	.legs th {
		padding: 3px 4px;
		border-top: 1px solid var(--line);
	}
	.legs tr.motor td {
		color: var(--muted);
	}
	.note {
		font-size: 0.75rem;
	}
	@media (max-width: 900px) {
		.layout {
			display: block;
			height: auto;
		}
		.mapcol {
			height: 55dvh;
		}
		.panel {
			border-left: 0;
		}
	}
</style>
