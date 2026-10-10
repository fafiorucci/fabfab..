<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import { normalize, PUBLIC_FORECAST, PUBLIC_MARINE, saveServer, server } from '#lib/meteo/dataserver.svelte.ts';
	import { MAIN_MODELS, modelById } from '#lib/meteo/models.ts';
	import { isoDate } from '#lib/trip.ts';

	let url = $state(server.url);
	let timeout = $state(server.timeout);
	let saved = $state(false);

	interface Probe {
		name: string;
		own: number | string | null;
		pub: number | string | null;
	}
	let probes: Probe[] = $state([]);
	let testing = $state(false);

	function save() {
		saveServer({ url, timeout });
		url = server.url;
		timeout = server.timeout;
		saved = true;
		setTimeout(() => (saved = false), 2000);
	}

	/** Tempo di una richiesta in ms, o il motivo dell'errore. */
	async function time(u: string, limit = 120): Promise<number | string> {
		const ctrl = new AbortController();
		const timer = setTimeout(() => ctrl.abort(), limit * 1000);
		const t0 = performance.now();
		try {
			const r = await fetch(u, { signal: ctrl.signal, cache: 'no-store' });
			const j = await r.json();
			if (!r.ok || j.error) return j.reason ?? `HTTP ${r.status}`;
			const h = (Array.isArray(j) ? j[0] : j).hourly as Record<string, (number | null)[]>;
			const vals = Object.entries(h).filter(([k]) => k !== 'time');
			if (!vals.length || vals.every(([, v]) => v.every((x) => x == null))) return 'nessun dato';
			return performance.now() - t0;
		} catch {
			return ctrl.signal.aborted ? `oltre ${limit} s` : 'non raggiungibile';
		} finally {
			clearTimeout(timer);
		}
	}

	/** Confronta il server proprio con quello pubblico sulle richieste tipiche dell'app. */
	async function test() {
		const own = normalize(url);
		testing = true;
		const day = isoDate(new Date());
		const grid = { lat: [] as number[], lon: [] as number[] };
		for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) {
			grid.lat.push(+(41 + i * 0.25).toFixed(2));
			grid.lon.push(+(11.25 + j * 0.25).toFixed(2));
		}
		const one = (m: string) =>
			`/v1/forecast?latitude=41.6&longitude=12&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&models=${m}&start_date=${day}&end_date=${day}`;
		const cases: [string, string, string][] = [
			...MAIN_MODELS.map((m) => [`Vento ${modelById(m)?.label ?? m}`, PUBLIC_FORECAST, one(m)] as [string, string, string]),
			[
				'Griglia 64 punti, 6 modelli, 3 giorni',
				PUBLIC_FORECAST,
				`/v1/forecast?latitude=${grid.lat}&longitude=${grid.lon}&hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m&models=${MAIN_MODELS}&forecast_days=3`
			],
			['Onda 64 punti', PUBLIC_MARINE, `/v1/marine?latitude=${grid.lat}&longitude=${grid.lon}&hourly=wave_height,wave_direction,wave_period&forecast_days=3`]
		];
		probes = cases.map(([name]) => ({ name, own: own ? null : '—', pub: null }));
		for (let i = 0; i < cases.length; i++) {
			const [, base, path] = cases[i];
			const [o, p] = await Promise.all([own ? time(own + path) : Promise.resolve('—'), time(base + path)]);
			probes[i] = { ...probes[i], own: o, pub: p };
		}
		testing = false;
	}

	const fmt = (v: number | string | null) => (v == null ? '…' : typeof v === 'number' ? `${(v / 1000).toFixed(2).replace('.', ',')} s` : v);
	const faster = (p: Probe) => typeof p.own === 'number' && typeof p.pub === 'number' && p.own < p.pub;
</script>

<ModuleShell title="Impostazioni">
	<h1 class="m-h1">Impostazioni</h1>

	<section class="m-card">
		<h2>Server dei dati meteo</h2>
		<p class="m-lead">
			Di base l'app usa <b>Open-Meteo pubblico</b> (gratuito, 10.000 chiamate al giorno per rete). Se hai un tuo server Open-Meteo, per esempio sul PC di
			casa, scrivi qui il suo indirizzo: le richieste andranno prima lì e, se non risponde entro il tempo indicato, l'app passa da sola al server
			pubblico.
		</p>
		<label class="f">
			<span>Indirizzo del tuo server (vuoto = solo Open-Meteo pubblico)</span>
			<input bind:value={url} placeholder="es. http://192.168.1.20:8080 oppure https://meteo.tuodominio.it" inputmode="url" autocomplete="off" />
		</label>
		<label class="f short">
			<span>Attesa massima prima di passare al pubblico (secondi)</span>
			<input type="number" min="5" max="300" bind:value={timeout} />
		</label>
		<p class="m-muted small">
			Dal telefono fuori casa serve un indirizzo <b>https</b> raggiungibile da internet (per esempio con Cloudflare Tunnel): un indirizzo come
			192.168.… funziona solo sulla rete di casa.
		</p>
		<div class="m-actions">
			<button class="ghost" onclick={test} disabled={testing}>{testing ? 'Prova in corso…' : 'Prova e confronta'}</button>
			<button class="primary" onclick={save}>{saved ? 'Salvato ✓' : 'Salva'}</button>
		</div>
	</section>

	{#if probes.length}
		<section class="m-card">
			<h2>Confronto dei tempi di risposta</h2>
			<table>
				<thead><tr><th>Richiesta</th><th>Tuo server</th><th>Pubblico</th></tr></thead>
				<tbody>
					{#each probes as p (p.name)}
						<tr>
							<td>{p.name}</td>
							<td class:best={faster(p)} class:bad={typeof p.own === 'string' && p.own !== '—'}>{fmt(p.own)}</td>
							<td class:best={typeof p.own === 'number' && typeof p.pub === 'number' && !faster(p)}>{fmt(p.pub)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<p class="m-muted small">
				La prima volta che il tuo server riceve una zona o un modello deve scaricarne i dati dall'archivio di Open-Meteo e può impiegare molto; dalla
				seconda volta risponde dalla sua memoria. Ripeti la prova per vedere i tempi a regime.
			</p>
		</section>
	{/if}
</ModuleShell>

<style>
	h2 {
		margin: 0 0 8px;
		font-size: 1.05rem;
	}
	.f {
		display: grid;
		gap: 4px;
		margin: 10px 0;
	}
	.f span {
		font-size: 0.85rem;
		color: var(--muted);
	}
	.f input {
		padding: 10px 12px;
		border: 1px solid var(--line-strong);
		border-radius: 10px;
		background: var(--bg);
		color: var(--text);
		font: inherit;
	}
	.f.short input {
		max-width: 120px;
	}
	.small {
		font-size: 0.85rem;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}
	th,
	td {
		text-align: left;
		padding: 6px;
		border-bottom: 1px solid var(--line);
	}
	td.best {
		color: var(--go);
		font-weight: 700;
	}
	td.bad {
		color: var(--nogo);
	}
</style>
