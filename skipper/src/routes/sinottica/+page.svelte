<script lang="ts">
	import type { Feature, FeatureCollection, LineString, Point } from 'geojson';
	import { onDestroy, onMount } from 'svelte';
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import MapView from '#lib/components/MapView.svelte';
	import Locked from '#lib/components/Locked.svelte';
	import { fetchPressureGrids, gridForView, type BBox, type PressureSet } from '#lib/meteo/api.ts';
	import { LAYERS } from '#lib/meteo/layers.ts';
	import { modelById } from '#lib/meteo/models.ts';
	import { isobars } from '#lib/map/isobars.ts';
	import { isoDate } from '#lib/trip.ts';
	import { DEMO } from '#lib/demo.ts';

	/** Area delle carte: Atlantico orientale, Europa e Mediterraneo (come le carte Met Office/DWD). */
	const AREA: BBox = [-30, 25, 42, 66];
	/** Modelli globali, gli unici che coprono tutta l'area. Una sola richiesta li scarica tutti. */
	const SYN_MODELS = ['ecmwf_ifs025', 'gfs_seamless', 'icon_seamless', 'ukmo_seamless', 'meteofrance_seamless', 'gem_seamless', 'ecmwf_aifs025_single'];
	const MAX_COMPARE = 3;
	const PRIMARY = '#14202c';

	let data = $state.raw<PressureSet | null>(null);
	let error: string | null = $state(null);
	let selected: string[] = $state(['ecmwf_ifs025']);
	let step = $state(0);
	let playing = $state(false);
	let timer: ReturnType<typeof setInterval> | undefined;
	let base: 'light' | 'satellite' = $state('light');

	const grid = gridForView(AREA, 400);

	onMount(async () => {
		try {
			data = await fetchPressureGrids(DEMO ? ['ecmwf_ifs025'] : SYN_MODELS, grid, isoDate(new Date(Date.now() - 12 * 3600e3)), 6);
		} catch (e) {
			error = (e as Error).message;
		}
	});
	onDestroy(() => clearInterval(timer));

	/** Scadenze ogni 12 ore (00 e 12 UTC), dalla più recente già passata fino a +120 ore. */
	const steps = $derived.by(() => {
		if (!data) return [];
		const now = Date.now() / 1000;
		const out: number[] = [];
		data.times.forEach((t, i) => {
			const h = new Date(t * 1000).getUTCHours();
			if (h % 12 === 0 && t >= now - 12 * 3600) out.push(i);
		});
		return out.slice(0, 11);
	});
	const ti = $derived(steps[step] ?? -1);
	const t0 = $derived(data && steps.length ? data.times[steps[0]] : 0);

	const fc: FeatureCollection<LineString | Point> | null = $derived.by(() => {
		if (!data || ti < 0) return null;
		const N = grid.lats.length * grid.lons.length;
		const features: Feature<LineString | Point>[] = [];
		selected.forEach((m, k) => {
			const arr = data!.byModel[m];
			if (!arr) return;
			const f = isobars(grid, arr.subarray(ti * N, (ti + 1) * N), { step: 4 });
			for (const feat of f.features) {
				feat.properties = { ...feat.properties, color: k === 0 ? PRIMARY : modelById(m)?.color, secondary: k > 0 };
				features.push(feat);
			}
		});
		return { type: 'FeatureCollection', features };
	});

	const hasData = (m: string) => {
		if (!data || ti < 0) return false;
		const N = grid.lats.length * grid.lons.length;
		const arr = data.byModel[m];
		return !!arr && arr.subarray(ti * N, (ti + 1) * N).some((v) => !Number.isNaN(v));
	};

	function toggle(m: string) {
		if (selected.includes(m)) {
			if (selected.length > 1) selected = selected.filter((x) => x !== m);
		} else if (selected.length < MAX_COMPARE) selected = [...selected, m];
		else selected = [...selected.slice(1), m];
	}

	function play() {
		playing = !playing;
		clearInterval(timer);
		if (playing) timer = setInterval(() => (step = (step + 1) % Math.max(1, steps.length)), 1200);
	}

	const fmt = (i: number) => {
		const d = new Date(data!.times[i] * 1000);
		const day = d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', timeZone: 'UTC' });
		return `${day} ${String(d.getUTCHours()).padStart(2, '0')} UTC`;
	};
	const lead = (i: number) => Math.round((data!.times[i] - t0) / 3600);
</script>

<ModuleShell title="Carte sinottiche" wide>
	<div class="layout">
		<section class="mapcol">
			<MapView
				home={AREA}
				field={null}
				layer={LAYERS.pressure}
				arrows={null}
				wind={null}
				{base}
				seamarks={false}
				particles={false}
				point={null}
				isobars={fc}
				popup={null}
			/>
			<div class="steps">
				<button class="play" onclick={play} aria-label={playing ? 'Pausa' : 'Riproduci'} disabled={!steps.length}>{playing ? '❚❚' : '▶'}</button>
				<div class="chips">
					{#each steps as s, k (s)}
						<button class:on={k === step} onclick={() => (step = k)}>{k === 0 ? 'Analisi' : `+${lead(s)}h`}</button>
					{/each}
				</div>
				{#if ti >= 0}<span class="when">{fmt(ti)}</span>{/if}
			</div>
		</section>

		<aside class="panel">
			<h1 class="m-h1">Carte sinottiche</h1>
			<p class="m-muted">
				Pressione al livello del mare con isobare ogni 4 hPa e centri di <b class="hi">A</b>lta e <b class="lo">B</b>assa pressione, ogni 12 ore fino a 5
				giorni. Sovrapponi più modelli per vedere dove concordano: dove le isobare coincidono la previsione è più affidabile.
			</p>
			{#if error}<p class="err">{error}</p>{:else if !data}<p class="m-muted">Carico la pressione dei modelli…</p>{/if}

			<div class="m-card">
				<h2>Modelli {DEMO ? '' : `(fino a ${MAX_COMPARE} sovrapposti)`}</h2>
				<ul class="models">
					{#each SYN_MODELS as m, k (m)}
						{@const sel = selected.indexOf(m)}
						{#if !DEMO || m === 'ecmwf_ifs025'}
							<li>
								<label class:off={!hasData(m)}>
									<input type="checkbox" checked={sel >= 0} onchange={() => toggle(m)} disabled={DEMO} />
									<i style="background: {sel === 0 ? PRIMARY : modelById(m)?.color}"></i>
									{modelById(m)?.label}
									<small>{sel === 0 ? 'principale, con valori e centri' : sel > 0 ? 'sovrapposto' : hasData(m) ? '' : 'nessun dato a questa scadenza'}</small>
								</label>
							</li>
						{/if}
					{/each}
				</ul>
				{#if DEMO}
					<Locked compact label="Confronto tra 7 modelli nella versione completa">
						<ul class="models">
							{#each SYN_MODELS.slice(1, 4) as m (m)}<li><label><input type="checkbox" /> <i style="background: {modelById(m)?.color}"></i>{modelById(m)?.label}</label></li>{/each}
						</ul>
					</Locked>
				{/if}
				<div class="m-actions">
					<button class="m-small-btn" onclick={() => (base = base === 'light' ? 'satellite' : 'light')}>{base === 'light' ? 'Satellite' : 'Mappa chiara'}</button>
				</div>
			</div>

			<div class="m-card">
				<h2>Carte ufficiali con i fronti</h2>
				<p class="m-muted">Le isobare dei modelli non mostrano i fronti: per quelli guarda le analisi dei servizi meteorologici.</p>
				<a href="https://www.dwd.de/DE/leistungen/hobbymet_wk_europa/hobbyeuropakarten.html" target="_blank" rel="noopener">
					<img class="chart-img" src="https://www.dwd.de/DWD/wetter/wv_spez/hobbymet/wetterkarten/bwk_bodendruck_na_ana.png" alt="Analisi al suolo DWD con fronti e isobare" loading="lazy" />
				</a>
				<p class="m-muted small">Analisi al suolo più recente del Deutscher Wetterdienst. Fonte: DWD.</p>
				<ul class="links">
					<li><a href="https://weather.metoffice.gov.uk/maps-and-charts/surface-pressure" target="_blank" rel="noopener">Met Office — carte al suolo con fronti, analisi e previsioni fino a 5 giorni</a></li>
					<li><a href="https://www.dwd.de/DE/leistungen/hobbymet_wk_europa/hobbyeuropakarten.html" target="_blank" rel="noopener">DWD — carte del tempo per l'Europa</a></li>
					<li><a href="https://www.meteoam.it/it/meteo-mare" target="_blank" rel="noopener">Aeronautica Militare — bollettino del mare</a></li>
				</ul>
			</div>
		</aside>
	</div>
</ModuleShell>

<style>
	.layout {
		flex: 1;
		display: grid;
		grid-template-columns: minmax(0, 1fr) 360px;
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
	.steps {
		position: absolute;
		z-index: 3;
		left: 10px;
		right: 10px;
		bottom: 26px;
		display: flex;
		align-items: center;
		gap: 8px;
		background: color-mix(in srgb, var(--panel) 92%, transparent);
		border-radius: 22px;
		padding: 4px 12px 4px 4px;
		box-shadow: var(--shadow);
		max-width: 760px;
		margin: 0 auto;
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
	.chips {
		flex: 1;
		display: flex;
		gap: 4px;
		overflow-x: auto;
		scrollbar-width: none;
	}
	.chips button {
		flex: none;
		border: 1px solid var(--line-strong);
		background: none;
		color: var(--text);
		border-radius: 14px;
		padding: 3px 9px;
		font-size: 0.78rem;
	}
	.chips button.on {
		background: var(--brand-2);
		border-color: var(--brand-2);
		color: #fff;
	}
	.when {
		flex: none;
		font-weight: 600;
		font-size: 0.8rem;
		text-transform: capitalize;
	}
	.models {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 4px;
	}
	.models label {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.9rem;
	}
	.models label.off {
		opacity: 0.55;
	}
	.models i {
		width: 18px;
		height: 3px;
		border-radius: 2px;
		flex: none;
	}
	.models small {
		margin-left: auto;
		color: var(--muted);
		font-size: 0.72rem;
	}
	.hi {
		color: #2f6fdb;
	}
	.lo {
		color: #d64545;
	}
	.err {
		color: var(--nogo);
	}
	.chart-img {
		width: 100%;
		border-radius: 10px;
		display: block;
	}
	.links {
		margin: 0;
		padding-left: 18px;
		font-size: 0.85rem;
		display: grid;
		gap: 4px;
	}
	.small {
		font-size: 0.75rem;
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
		.when {
			display: none;
		}
	}
</style>
