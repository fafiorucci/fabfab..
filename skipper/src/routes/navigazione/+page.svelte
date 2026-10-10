<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import type { Feature, FeatureCollection } from 'geojson';
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import MapView from '#lib/components/MapView.svelte';
	import { LAYERS } from '#lib/meteo/layers.ts';
	import { persisted, shareText, uid } from '#lib/persist.svelte.ts';
	import { latDM, lonDM, num } from '#lib/meteo/format.ts';
	import type { BBox } from '#lib/meteo/api.ts';
	import { angleDiff, bearing, crossTrackNm, distanceNm, parseGpx, pathNm, toGpx, type TrackPoint, type Waypoint } from '#lib/nav/nav.ts';

	interface NavState {
		name: string;
		route: Waypoint[];
		/** Indice del prossimo waypoint da raggiungere */
		active: number;
		track: TrackPoint[];
		recording: boolean;
		/** Raggio di arrivo al waypoint, in miglia */
		arrival: number;
	}
	const nav = persisted<NavState>('navigazione', { name: 'Navigazione', route: [], active: 0, track: [], recording: false, arrival: 0.1 });
	const s = $derived(nav.value);

	// ----- GPS -----
	interface Fix {
		lat: number;
		lon: number;
		acc: number;
		sog: number | null;
		cog: number | null;
		t: number;
	}
	let fix: Fix | null = $state(null);
	let prev: Fix | null = null;
	let gpsError: string | null = $state(null);
	let watch: number | null = null;
	let follow = $state(true);
	let planning = $state(false);
	let base: 'light' | 'satellite' = $state('light');
	let toast: string | null = $state(null);
	let fileInput: HTMLInputElement | undefined = $state();
	let map: MapView | undefined = $state();
	let wake: WakeLockSentinel | null = null;

	function flash(t: string) {
		toast = t;
		setTimeout(() => (toast = null), 2600);
	}

	function onFix(p: GeolocationPosition) {
		const f: Fix = {
			lat: p.coords.latitude,
			lon: p.coords.longitude,
			acc: p.coords.accuracy,
			sog: p.coords.speed != null && !Number.isNaN(p.coords.speed) ? p.coords.speed * 1.943844 : null,
			cog: p.coords.heading != null && !Number.isNaN(p.coords.heading) ? p.coords.heading : null,
			t: p.timestamp
		};
		// Su PC e alcuni telefoni velocità e rotta non arrivano dal GPS: si ricavano dagli ultimi due punti.
		if (prev && (f.sog == null || f.cog == null)) {
			const dt = (f.t - prev.t) / 3_600_000;
			const d = distanceNm(prev, f);
			// Oltre 60 nodi è un salto del GPS, non la velocità della barca: si scarta.
			if (dt > 0 && d > 0.003 && d / dt < 60) {
				f.sog ??= d / dt;
				f.cog ??= bearing(prev, f);
			} else {
				f.sog ??= prev.sog;
				f.cog ??= prev.cog;
			}
		}
		prev = f;
		fix = f;
		gpsError = null;
		record(f);
		advance(f);
		if (follow) map?.centerOn(f.lat, f.lon);
	}

	function startGps() {
		if (!('geolocation' in navigator)) return void (gpsError = 'GPS non disponibile su questo dispositivo.');
		watch = navigator.geolocation.watchPosition(onFix, (e) => {
			gpsError = e.code === e.PERMISSION_DENIED ? 'Permesso di posizione negato: abilitalo nelle impostazioni del browser.' : 'Posizione non disponibile: cerco il segnale…';
		}, { enableHighAccuracy: true, maximumAge: 2000, timeout: 30000 });
	}

	onMount(() => {
		startGps();
		if (s.recording) keepAwake();
		document.addEventListener('visibilitychange', onVisible);
	});
	onDestroy(() => {
		if (watch != null) navigator.geolocation.clearWatch(watch);
		wake?.release().catch(() => {});
		document.removeEventListener('visibilitychange', onVisible);
	});

	// ----- Traccia -----
	/** Aggiunge un punto alla traccia ogni ~10 m percorsi o ogni 30 s, scartando le posizioni imprecise. */
	function record(f: Fix) {
		if (!s.recording || f.acc > 60) return;
		const last = s.track.at(-1);
		if (last && distanceNm(last, f) < 0.005 && f.t - last.t < 30_000) return;
		nav.value.track.push({ lat: +f.lat.toFixed(6), lon: +f.lon.toFixed(6), t: f.t, sog: f.sog != null ? +f.sog.toFixed(1) : null });
	}

	async function keepAwake() {
		try {
			wake = (await navigator.wakeLock?.request('screen')) ?? null;
		} catch {
			wake = null;
		}
	}
	function onVisible() {
		if (document.visibilityState === 'visible' && s.recording) keepAwake();
	}

	function toggleRecording() {
		nav.value.recording = !s.recording;
		if (s.recording) {
			keepAwake();
			if (fix) record(fix);
			flash('Registrazione della traccia avviata');
		} else {
			wake?.release().catch(() => {});
			wake = null;
			flash('Registrazione in pausa');
		}
	}

	function clearTrack() {
		if (s.track.length && !confirm('Cancellare la traccia registrata?')) return;
		nav.value.track = [];
	}

	const trackStats = $derived.by(() => {
		const t = s.track;
		if (t.length < 2) return null;
		const nm = pathNm(t);
		const h = (t.at(-1)!.t - t[0].t) / 3_600_000;
		const max = Math.max(0, ...t.map((p) => p.sog ?? 0));
		return { nm, h, avg: h > 0 ? nm / h : 0, max };
	});

	// ----- Rotta pianificata -----
	const next = $derived(s.route[s.active] ?? null);
	const legFrom = $derived(s.active > 0 ? s.route[s.active - 1] : null);
	const toNext = $derived.by(() => {
		if (!fix || !next) return null;
		const dtw = distanceNm(fix, next);
		const brg = bearing(fix, next);
		const xte = legFrom ? crossTrackNm(legFrom, next, fix) : null;
		const sog = fix.sog ?? 0;
		const eta = sog > 0.5 ? new Date(Date.now() + (dtw / sog) * 3_600_000) : null;
		const remaining = dtw + pathNm(s.route.slice(s.active));
		return { dtw, brg, xte, eta, remaining };
	});

	/**
	 * Waypoint raggiunto: dentro il raggio di arrivo, oppure — come sui chartplotter — oltrepassato al traverso,
	 * cioè la barca è già avanti rispetto al tratto successivo e vicina al waypoint.
	 */
	function reached(f: Fix, i: number): boolean {
		const w = s.route[i];
		const d = distanceNm(f, w);
		if (d <= s.arrival) return true;
		const after = s.route[i + 1];
		if (!after) return false;
		const leg = distanceNm(w, after);
		return d < Math.max(0.3, Math.min(2, leg / 3)) && Math.abs(angleDiff(bearing(w, after), bearing(w, f))) < 80;
	}

	function advance(f: Fix) {
		const w = s.route[s.active];
		if (w && s.active < s.route.length && reached(f, s.active)) {
			nav.value.active = s.active + 1;
			flash(s.active < s.route.length ? `Raggiunto ${w.name}: prossimo ${s.route[s.active].name}` : `Raggiunto ${w.name}: arrivo!`);
			navigator.vibrate?.(200);
		}
	}

	function pick(lat: number, lon: number) {
		if (!planning) return;
		nav.value.route.push({ lat: +lat.toFixed(5), lon: +lon.toFixed(5), name: `WP${s.route.length + 1}` });
	}
	function removeWp(i: number) {
		nav.value.route.splice(i, 1);
		if (s.active > i) nav.value.active = s.active - 1;
		nav.value.active = Math.min(s.active, s.route.length);
	}
	function reverseRoute() {
		nav.value.route = s.route.toReversed();
		nav.value.active = 0;
	}
	function clearRoute() {
		if (s.route.length && !confirm('Cancellare la rotta pianificata?')) return;
		nav.value.route = [];
		nav.value.active = 0;
	}

	// ----- GPX (Navionics, chartplotter, altre app) -----
	async function importGpx(e: Event) {
		const input = e.currentTarget as HTMLInputElement;
		const f = input.files?.[0];
		input.value = '';
		if (!f) return;
		try {
			const g = parseGpx(await f.text());
			if (!g.route.length) throw new Error('Nel file non ci sono rotte, waypoint o tracce.');
			nav.value.route = g.route;
			nav.value.active = 0;
			nav.value.name = g.name;
			fitRoute();
			flash(`Importata «${g.name}»: ${g.route.length} waypoint`);
		} catch (err) {
			alert((err as Error).message);
		}
	}

	async function exportGpx(what: 'route' | 'track') {
		const name = `${s.name || 'Navigazione'} ${new Date().toLocaleDateString('it-IT')}`;
		const xml = toGpx({ name, route: what === 'route' ? s.route : undefined, track: what === 'track' ? s.track : undefined });
		const file = new File([xml], `${what === 'route' ? 'rotta' : 'traccia'}-${new Date().toISOString().slice(0, 10)}.gpx`, { type: 'application/gpx+xml' });
		if (navigator.canShare?.({ files: [file] })) {
			try {
				await navigator.share({ files: [file], title: name });
				return;
			} catch (err) {
				if ((err as Error).name === 'AbortError') return;
			}
		}
		const a = document.createElement('a');
		a.href = URL.createObjectURL(file);
		a.download = file.name;
		a.click();
		setTimeout(() => URL.revokeObjectURL(a.href), 2000);
	}

	function fitRoute() {
		const pts = [...s.route, ...(fix ? [fix] : [])];
		if (!pts.length) return;
		follow = false;
		const lats = pts.map((p) => p.lat);
		const lons = pts.map((p) => p.lon);
		map?.fitTo([Math.min(...lons), Math.min(...lats), Math.max(...lons), Math.max(...lats)]);
	}

	// ----- Log book e condivisione -----
	const logbook = persisted<Record<string, unknown>[]>('logbook', []);
	function toLogbook() {
		if (!fix) return;
		const d = new Date();
		d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
		logbook.value = [
			{
				id: uid(),
				time: d.toISOString().slice(0, 16),
				lat: +fix.lat.toFixed(5),
				lon: +fix.lon.toFixed(5),
				cog: fix.cog != null ? String(Math.round(fix.cog)) : '',
				sog: fix.sog != null ? fix.sog.toFixed(1) : '',
				wind: '',
				sea: '',
				baro: '',
				engine: '',
				sails: '',
				note: next ? `In navigazione verso ${next.name}` : 'Posizione da Navigazione'
			},
			...logbook.value
		];
		flash('Posizione annotata nel log book');
	}

	async function sharePosition() {
		if (!fix) return;
		const text = [
			`Posizione ${new Date(fix.t).toLocaleString('it-IT')}`,
			`${latDM(fix.lat)} ${lonDM(fix.lon)}`,
			fix.sog != null ? `Velocità ${num(fix.sog, 1)} kn, rotta ${fix.cog != null ? Math.round(fix.cog) + '°' : '—'}` : '',
			`https://www.openstreetmap.org/?mlat=${fix.lat.toFixed(5)}&mlon=${fix.lon.toFixed(5)}#map=12/${fix.lat.toFixed(4)}/${fix.lon.toFixed(4)}`
		].filter(Boolean);
		if ((await shareText('Posizione', text.join('\n'))) === 'copied') flash('Posizione copiata negli appunti');
	}

	// ----- Mappa -----
	const home: BBox = [11.6, 41.4, 12.8, 42.1]; // Fiumicino, finché non arriva il GPS
	const overlay: FeatureCollection = $derived.by(() => {
		const f: Feature[] = [];
		if (s.route.length > 1) f.push({ type: 'Feature', properties: { kind: 'plan' }, geometry: { type: 'LineString', coordinates: s.route.map((w) => [w.lon, w.lat]) } });
		if (s.track.length > 1) f.push({ type: 'Feature', properties: { kind: 'track' }, geometry: { type: 'LineString', coordinates: s.track.map((p) => [p.lon, p.lat]) } });
		if (fix && next) f.push({ type: 'Feature', properties: { kind: 'leg' }, geometry: { type: 'LineString', coordinates: [[fix.lon, fix.lat], [next.lon, next.lat]] } });
		s.route.forEach((w, i) =>
			f.push({ type: 'Feature', properties: { kind: 'wp', label: String(i + 1), active: i === s.active }, geometry: { type: 'Point', coordinates: [w.lon, w.lat] } })
		);
		if (fix)
			f.push({
				type: 'Feature',
				properties: fix.cog != null && (fix.sog ?? 0) > 0.3 ? { kind: 'boat', rot: fix.cog } : { kind: 'boat' },
				geometry: { type: 'Point', coordinates: [fix.lon, fix.lat] }
			});
		return { type: 'FeatureCollection', features: f };
	});

	const hhmm = (h: number) => `${Math.floor(h)} h ${String(Math.round((h % 1) * 60)).padStart(2, '0')} min`;
	const deg3 = (d: number) => String(Math.round(d) % 360).padStart(3, '0') + '°';
</script>

<ModuleShell title="Navigazione" wide>
	<div class="layout">
		<section class="mapcol">
			<MapView
				bind:this={map}
				{home}
				field={null}
				layer={LAYERS.wind}
				arrows={null}
				wind={null}
				{base}
				seamarks={true}
				particles={false}
				point={null}
				isobars={null}
				{overlay}
				popup={null}
				onpick={pick}
			/>
			<div class="pickbar">
				<button class:on={follow} onclick={() => ((follow = !follow), follow && fix && map?.centerOn(fix.lat, fix.lon))}>◎ Segui</button>
				<button class:on={planning} onclick={() => (planning = !planning)}>＋ Waypoint</button>
				<button onclick={fitRoute} disabled={!s.route.length}>⤢ Rotta</button>
				<button onclick={() => (base = base === 'light' ? 'satellite' : 'light')}>{base === 'light' ? 'Satellite' : 'Mappa'}</button>
			</div>
			{#if planning}<div class="hint">Tocca la mappa per aggiungere i waypoint in ordine</div>{/if}
			<div class="hud">
				<div><small>SOG</small><b>{fix?.sog != null ? num(fix.sog, 1) : '—'}</b><i>kn</i></div>
				<div><small>COG</small><b>{fix?.cog != null ? deg3(fix.cog) : '—'}</b></div>
				{#if toNext}
					<div><small>BRG {next?.name}</small><b>{deg3(toNext.brg)}</b></div>
					<div><small>DTW</small><b>{num(toNext.dtw, toNext.dtw < 10 ? 2 : 1)}</b><i>NM</i></div>
				{/if}
			</div>
		</section>

		<aside class="panel">
			<h1 class="m-h1">Navigazione</h1>
			{#if gpsError}<p class="err">{gpsError}</p>{/if}

			<div class="m-card">
				<h2>Posizione</h2>
				{#if fix}
					<p class="pos">{latDM(fix.lat)}<br />{lonDM(fix.lon)}</p>
					<p class="m-muted small">Precisione ±{Math.round(fix.acc)} m · {new Date(fix.t).toLocaleTimeString('it-IT')}</p>
					<div class="m-actions">
						<button class="ghost small" onclick={toLogbook}>Annota nel log book</button>
						<button class="ghost small" onclick={sharePosition}>Condividi posizione</button>
					</div>
				{:else}
					<p class="m-muted">In attesa del segnale GPS…</p>
				{/if}
			</div>

			<div class="m-card">
				<h2>Rotta {s.route.length ? `· ${s.name}` : ''}</h2>
				{#if toNext && next}
					<div class="kpis">
						<div><small>Prossimo</small><b>{next.name}</b></div>
						<div><small>Rilevamento</small><b>{deg3(toNext.brg)}</b></div>
						<div><small>Distanza</small><b>{num(toNext.dtw, 2)} NM</b></div>
						<div><small>Arrivo stimato</small><b>{toNext.eta ? toNext.eta.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) : '—'}</b></div>
						{#if toNext.xte != null}
							<div class:warnk={Math.abs(toNext.xte) > 0.25}>
								<small>Fuori rotta</small><b>{num(Math.abs(toNext.xte), 2)} NM {toNext.xte > 0 ? 'a dritta' : 'a sinistra'}</b>
							</div>
						{/if}
						<div><small>Al termine</small><b>{num(toNext.remaining, 1)} NM</b></div>
					</div>
				{:else if s.route.length && s.active >= s.route.length}
					<p class="ok">Rotta completata ✓</p>
				{/if}
				{#if s.route.length}
					<ol class="wps">
						{#each s.route as w, i (i)}
							<li class:done={i < s.active} class:act={i === s.active}>
								<button class="wp-go" onclick={() => (nav.value.active = i)} title="Naviga verso questo waypoint">
									<span class="n">{i + 1}</span>{w.name}
									<small>{latDM(w.lat)} {lonDM(w.lon)}{i > 0 ? ` · ${num(distanceNm(s.route[i - 1], w), 1)} NM` : ''}</small>
								</button>
								<button class="x" onclick={() => removeWp(i)} aria-label="Elimina">✕</button>
							</li>
						{/each}
					</ol>
					<p class="m-muted small">Totale {num(pathNm(s.route), 1)} NM · arrivo al waypoint entro
						<input class="arr" type="number" min="0.02" max="1" step="0.01" bind:value={nav.value.arrival} /> NM
					</p>
				{:else}
					<p class="m-muted">Premi «＋ Waypoint» e tocca la mappa, oppure importa una rotta GPX (per esempio esportata da Navionics).</p>
				{/if}
				<div class="m-actions">
					<button class="ghost small" onclick={() => fileInput?.click()}>Importa GPX</button>
					<button class="ghost small" onclick={() => exportGpx('route')} disabled={!s.route.length}>Esporta rotta GPX</button>
					<button class="ghost small" onclick={reverseRoute} disabled={s.route.length < 2}>Inverti</button>
					<button class="ghost small" onclick={clearRoute} disabled={!s.route.length}>Cancella</button>
					<input bind:this={fileInput} type="file" accept=".gpx,application/gpx+xml,application/xml,text/xml" hidden onchange={importGpx} />
				</div>
			</div>

			<div class="m-card">
				<h2>Traccia</h2>
				{#if trackStats}
					<div class="kpis">
						<div><small>Percorse</small><b>{num(trackStats.nm, 1)} NM</b></div>
						<div><small>Tempo</small><b>{hhmm(trackStats.h)}</b></div>
						<div><small>Media</small><b>{num(trackStats.avg, 1)} kn</b></div>
						<div><small>Massima</small><b>{num(trackStats.max, 1)} kn</b></div>
					</div>
				{:else}
					<p class="m-muted">{s.recording ? 'Registrazione in corso: la traccia compare appena ti muovi.' : 'Avvia la registrazione per salvare il percorso.'}</p>
				{/if}
				<div class="m-actions">
					<button class={s.recording ? 'ghost' : 'primary'} onclick={toggleRecording}>{s.recording ? '❚❚ Pausa' : '● Registra'}</button>
					<button class="ghost small" onclick={() => exportGpx('track')} disabled={s.track.length < 2}>Esporta traccia GPX</button>
					<button class="ghost small" onclick={clearTrack} disabled={!s.track.length}>Cancella</button>
				</div>
				<p class="m-muted small">
					Durante la registrazione lo schermo resta acceso. Se blocchi il telefono o passi a un'altra app il browser può sospendere il GPS: la
					traccia riprende quando torni qui.
				</p>
			</div>

			<p class="m-muted small">
				Navionics: dall'app Boating esporta rotte o tracce come file GPX (Menu → Rotte/Tracce → Condividi) e importale qui; i file GPX esportati da qui
				si aprono in Navionics e nei chartplotter. Strumento di supporto: naviga sempre con la carta nautica e il GPS di bordo.
			</p>
		</aside>
	</div>
	{#if toast}<div class="toast" role="status">{toast}</div>{/if}
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
		right: 60px;
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		width: max-content;
		max-width: calc(100% - 70px);
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
	}
	.pickbar button.on {
		background: var(--brand-2);
		color: #fff;
	}
	.hint {
		position: absolute;
		z-index: 3;
		bottom: 40px;
		left: 10px;
		background: var(--accent);
		color: #fff;
		border-radius: 10px;
		padding: 6px 10px;
		font-size: 0.85rem;
	}
	.hud {
		position: absolute;
		z-index: 3;
		left: 10px;
		right: 60px;
		top: 58px;
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		pointer-events: none;
	}
	.hud div {
		background: rgba(11, 29, 44, 0.85);
		color: #fff;
		border-radius: 12px;
		padding: 6px 12px;
		display: grid;
		justify-items: center;
		min-width: 74px;
	}
	.hud small {
		font-size: 0.65rem;
		letter-spacing: 0.05em;
		opacity: 0.75;
		white-space: nowrap;
	}
	.hud b {
		font-size: 1.35rem;
		font-variant-numeric: tabular-nums;
		line-height: 1.1;
	}
	.hud i {
		font-style: normal;
		font-size: 0.7rem;
		opacity: 0.75;
	}
	h2 {
		margin: 0 0 8px;
		font-size: 1rem;
	}
	.pos {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
	}
	.small {
		font-size: 0.82rem;
	}
	button.small {
		padding: 5px 10px;
		font-size: 0.82rem;
	}
	.err {
		color: var(--nogo);
	}
	.ok {
		color: var(--go);
		font-weight: 700;
	}
	.kpis {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
		gap: 8px;
		margin-bottom: 10px;
	}
	.kpis div {
		background: var(--bg);
		border-radius: 10px;
		padding: 6px 8px;
		display: grid;
	}
	.kpis small {
		color: var(--muted);
		font-size: 0.72rem;
	}
	.kpis .warnk {
		background: var(--accent-soft);
	}
	.wps {
		list-style: none;
		margin: 0 0 6px;
		padding: 0;
		display: grid;
		gap: 4px;
		max-height: 260px;
		overflow-y: auto;
	}
	.wps li {
		display: flex;
		align-items: center;
		gap: 6px;
		border: 1px solid var(--line);
		border-radius: 10px;
		padding: 4px 6px;
	}
	.wps li.act {
		border-color: var(--nogo);
		background: var(--accent-soft);
	}
	.wps li.done {
		opacity: 0.55;
	}
	.wp-go {
		flex: 1;
		display: grid;
		grid-template-columns: auto 1fr;
		column-gap: 8px;
		text-align: left;
		border: 0;
		background: none;
		color: var(--text);
		padding: 2px;
		font-weight: 600;
	}
	.wp-go small {
		grid-column: 2;
		color: var(--muted);
		font-weight: 400;
		font-size: 0.75rem;
	}
	.n {
		grid-row: span 2;
		align-self: center;
		width: 22px;
		height: 22px;
		border-radius: 50%;
		background: var(--accent);
		color: #fff;
		display: grid;
		place-items: center;
		font-size: 0.75rem;
	}
	.x {
		border: 0;
		background: none;
		color: var(--muted);
	}
	.arr {
		width: 60px;
		padding: 2px 4px;
		border-radius: 6px;
		border: 1px solid var(--line-strong);
		background: var(--bg);
		color: var(--text);
	}
	.toast {
		position: fixed;
		left: 50%;
		bottom: 24px;
		transform: translateX(-50%);
		background: var(--brand);
		color: #fff;
		padding: 8px 14px;
		border-radius: 20px;
		z-index: 50;
		box-shadow: var(--shadow);
	}
	@media (max-width: 900px) {
		.layout {
			display: block;
			height: auto;
		}
		.mapcol {
			height: 60dvh;
		}
		.panel {
			border-left: 0;
		}
		.hud b {
			font-size: 1.1rem;
		}
		.hud div {
			min-width: 0;
			padding: 4px 8px;
		}
	}
</style>
