import type { Trip } from '#lib/trip.ts';
import { addDays } from '#lib/trip.ts';

const FORECAST_URL = 'https://api.open-meteo.com/v1/forecast';
const MARINE_URL = 'https://marine-api.open-meteo.com/v1/marine';
const GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search';

/** Passi possibili della griglia, in gradi: si sceglie il più fine compatibile con il numero di punti. */
export const STEPS = [0.1, 0.125, 0.25, 0.5, 1, 2, 4] as const;
/**
 * Punti massimi per vista. Ogni punto conta come una chiamata Open-Meteo per modello:
 * Con 64 punti una zona nuova costa circa 180 chiamate (vento di 6 modelli + onda): 3 zone al minuto
 * entro il limite di 600/min e una cinquantina al giorno entro le 10.000. L'interpolazione rende il campo continuo.
 */
export const MAX_POINTS = 64;

/** Variabili scaricate per tutti i modelli sulla griglia: bastano per mappa, semaforo e confronto. */
export const WIND_VARS = ['wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m'] as const;
/** Variabili extra: sulla griglia solo per il modello mostrato e solo se il livello è attivo. */
export const EXTRA_VARS = ['pressure_msl', 'precipitation'] as const;
export const ATMO_VARS = [...WIND_VARS, ...EXTRA_VARS] as const;
export const MARINE_VARS = ['wave_height', 'wave_direction', 'wave_period', 'swell_wave_height'] as const;

export type AtmoVar = 'wind' | 'dir' | 'gust' | 'pressure' | 'precip' | 'u' | 'v';
export type MarineVar = 'wave' | 'waveDir' | 'wavePeriod' | 'swell';

export interface Grid {
	lats: number[]; // dal basso (sud) verso l'alto
	lons: number[];
	/** Riquadro [ovest, sud, est, nord] */
	bbox: [number, number, number, number];
}

export interface Series {
	/** Istanti in secondi UNIX (UTC) */
	times: number[];
	/** Offset del fuso orario della zona in secondi */
	utcOffset: number;
}

/** Dati su griglia: ogni variabile è un array [t * nCelle + cella], NaN dove mancante. */
export interface GridData<V extends string> extends Series {
	grid: Grid;
	values: Record<V, Float32Array>;
}

export type AtmoGrid = GridData<AtmoVar> & { model: string };
export type ExtraVar = 'pressure' | 'precip';
export type ExtraGrid = GridData<ExtraVar> & { model: string };
export type MarineGrid = GridData<MarineVar>;

export type BBox = [number, number, number, number];

function gridOn(bbox: BBox, step: number): Grid {
	// Bordi arrotondati ai multipli del passo, appena fuori dalla vista: tutti i punti servono.
	const w = Math.max(-180, Math.floor(bbox[0] / step) * step);
	const e = Math.min(180, Math.ceil(bbox[2] / step) * step);
	const s = Math.max(-80, Math.floor(bbox[1] / step) * step);
	const n = Math.min(80, Math.ceil(bbox[3] / step) * step);
	const range = (a: number, b: number) => {
		const out: number[] = [];
		for (let i = 0; a + i * step <= b + 1e-9; i++) out.push(+(a + i * step).toFixed(3));
		return out;
	};
	const lats = range(s, n);
	const lons = range(w, e);
	return { lats, lons, bbox: [lons[0], lats[0], lons[lons.length - 1], lats[lats.length - 1]] };
}

/** Griglia che copre (con un piccolo margine) la zona inquadrata [ovest, sud, est, nord]. */
export function gridForView(bbox: BBox, maxPoints = MAX_POINTS): Grid {
	let g = gridOn(bbox, STEPS[STEPS.length - 1]);
	for (const step of STEPS) {
		g = gridOn(bbox, step);
		if (g.lats.length * g.lons.length <= maxPoints) break;
	}
	return g;
}

export const gridStep = (g: Grid) => (g.lats.length > 1 ? g.lats[1] - g.lats[0] : STEPS[0]);

/**
 * La griglia già scaricata va ancora bene per la nuova vista? Sì se la contiene
 * e non è più grossolana di quella che si sceglierebbe per la vista (zoomando in avanti si infittisce).
 */
export function gridCovers(g: Grid, view: BBox): boolean {
	const [w, s, e, n] = g.bbox;
	const inside = view[0] >= w - 1e-6 && view[1] >= s - 1e-6 && view[2] <= e + 1e-6 && view[3] <= n + 1e-6;
	return inside && gridStep(g) <= gridStep(gridForView(view)) + 1e-9;
}

export const gridKey = (g: Grid) => `${g.bbox.join(',')}:${g.lats.length}x${g.lons.length}`;

/** Zona iniziale dell'uscita attorno al porto. */
export function homeBox(trip: Pick<Trip, 'lat' | 'lon' | 'radius'>): BBox {
	const r = trip.radius;
	const rx = r / Math.cos((trip.lat * Math.PI) / 180);
	return [trip.lon - rx, trip.lat - r, trip.lon + rx, trip.lat + r];
}

export const cellCount = (g: Grid) => g.lats.length * g.lons.length;

function gridPoints(g: Grid) {
	const lat: number[] = [];
	const lon: number[] = [];
	for (const y of g.lats) for (const x of g.lons) {
		lat.push(y);
		lon.push(x);
	}
	return { lat, lon };
}

const cache = new Map<string, Promise<unknown>>();

// ----- Conteggio indicativo delle chiamate del giorno (per stare nel limite gratuito) -----
const BUDGET_KEY = 'skipper-meteo:calls';
export const DAILY_LIMIT = 10_000;

export function callsToday(): number {
	try {
		const v = JSON.parse(localStorage.getItem(BUDGET_KEY) ?? 'null');
		return v?.day === new Date().toDateString() ? v.n : 0;
	} catch {
		return 0;
	}
}

/**
 * Peso di una richiesta secondo Open-Meteo: ogni punto conta come una chiamata,
 * moltiplicata per ogni blocco di 10 variabili (le variabili di più modelli si sommano).
 */
export function callWeight(url: string): number {
	const q = new URL(url).searchParams;
	const points = q.get('latitude')?.split(',').length ?? 1;
	const vars = (q.get('hourly')?.split(',').length ?? 1) * (q.get('models')?.split(',').length ?? 1);
	return points * Math.max(1, vars / 10);
}

function countCalls(n: number) {
	try {
		localStorage.setItem(BUDGET_KEY, JSON.stringify({ day: new Date().toDateString(), n: callsToday() + n }));
	} catch {
		/* storage non disponibile */
	}
}

// ----- Regolatore: Open-Meteo gratuito accetta al massimo 600 chiamate al minuto -----
const PER_MINUTE = 540;
const WINDOW_MS = 60_000;
const recent: { t: number; n: number }[] = [];
let waitListener: ((seconds: number | null) => void) | null = null;

/** Notifica quando l'app sta aspettando il limite al minuto (secondi di attesa, o null). */
export function onRateWait(fn: (seconds: number | null) => void) {
	waitListener = fn;
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function throttle(n: number) {
	for (;;) {
		const now = Date.now();
		while (recent.length && now - recent[0].t > WINDOW_MS) recent.shift();
		const used = recent.reduce((a, r) => a + r.n, 0);
		if (!recent.length || used + n <= PER_MINUTE) {
			recent.push({ t: now, n });
			waitListener?.(null);
			return;
		}
		const wait = recent[0].t + WINDOW_MS - now + 250;
		waitListener?.(Math.ceil(wait / 1000));
		await sleep(Math.min(wait, 5000));
	}
}

async function request(url: string): Promise<unknown> {
	const n = callWeight(url);
	await throttle(n);
	let res: Response;
	try {
		res = await fetch(url);
	} catch {
		throw new Error('Rete non disponibile: nessun dato in memoria per questa richiesta.');
	}
	countCalls(n);
	const body = await res.json().catch(() => null);
	if (!res.ok || (body && body.error)) {
		const reason: string = body?.reason ?? `HTTP ${res.status}`;
		if (/minutely/i.test(reason)) throw new RateError('minute');
		if (/hourly/i.test(reason)) throw new Error("Limite orario di Open-Meteo raggiunto per questa rete: riprova tra un po'.");
		if (/limit exceeded/i.test(reason)) throw new Error('Limite giornaliero di Open-Meteo raggiunto per questa rete: riprova domani.');
		throw new Error(reason);
	}
	return body;
}

class RateError extends Error {
	constructor(public kind: 'minute') {
		super('Limite al minuto di Open-Meteo raggiunto.');
	}
}

async function getJson(url: string): Promise<unknown> {
	const hit = cache.get(url);
	if (hit) return hit;
	const p = (async () => {
		try {
			return await request(url);
		} catch (e) {
			if (!(e instanceof RateError)) throw e;
			// Altre app sulla stessa rete possono aver consumato il minuto: si attende e si riprova una volta.
			waitListener?.(60);
			await sleep(61_000);
			try {
				return await request(url);
			} catch (e2) {
				if (e2 instanceof RateError) throw new Error('Open-Meteo è al limite di chiamate al minuto: aspetta un minuto e sposta di poco la mappa.');
				throw e2;
			}
		}
	})();
	cache.set(url, p);
	p.catch(() => cache.delete(url));
	return p;
}

function dateRange(trip: Pick<Trip, 'date' | 'days'>) {
	return { start_date: trip.date, end_date: addDays(trip.date, trip.days - 1) };
}

interface OmResponse {
	utc_offset_seconds: number;
	hourly: Record<string, (number | null)[]> & { time: number[] };
}

function asList(body: unknown): OmResponse[] {
	return Array.isArray(body) ? (body as OmResponse[]) : [body as OmResponse];
}

function toUV(speed: number, dirFrom: number): [number, number] {
	// Direzione meteorologica: da dove soffia. Il vettore punta dove va.
	const r = (dirFrom * Math.PI) / 180;
	return [-speed * Math.sin(r), -speed * Math.cos(r)];
}

/** Chiave di una variabile nella risposta: con più modelli Open-Meteo aggiunge il suffisso `_modello`. */
const key = (v: string, m: string, models: string[]) => (models.length > 1 ? `${v}_${m}` : v);

/** Tutti i modelli in un'unica richiesta: meno chiamate conteggiate e un solo viaggio in rete. */
export async function fetchAtmoGrids(trip: Trip, models: string[], grid: Grid): Promise<Record<string, AtmoGrid>> {
	const pts = gridPoints(grid);
	const params = new URLSearchParams({
		latitude: pts.lat.join(','),
		longitude: pts.lon.join(','),
		hourly: WIND_VARS.join(','),
		models: models.join(','),
		wind_speed_unit: 'kn',
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const list = asList(await getJson(`${FORECAST_URL}?${params}`));
	const times = list[0].hourly.time;
	const T = times.length;
	const N = list.length;
	const out: Record<string, AtmoGrid> = {};
	for (const m of models) {
		const v = {} as Record<AtmoVar, Float32Array>;
		for (const k of ['wind', 'dir', 'gust', 'pressure', 'precip', 'u', 'v'] as AtmoVar[]) v[k] = new Float32Array(T * N).fill(NaN);
		const col = (h: OmResponse['hourly'], name: string) => h[key(name, m, models)] ?? [];
		list.forEach((loc, c) => {
			const h = loc.hourly;
			const ws = col(h, 'wind_speed_10m');
			const wd = col(h, 'wind_direction_10m');
			const wg = col(h, 'wind_gusts_10m');
			for (let t = 0; t < T; t++) {
				const i = t * N + c;
				const s = ws[t];
				const d = wd[t];
				v.wind[i] = s ?? NaN;
				v.dir[i] = d ?? NaN;
				v.gust[i] = wg[t] ?? NaN;
				if (s != null && d != null) [v.u[i], v.v[i]] = toUV(s, d);
			}
		});
		// Un modello senza alcun dato (fuori area o fuori orizzonte) viene segnalato come non disponibile.
		if (v.wind.some((x) => !Number.isNaN(x))) out[m] = { model: m, grid, times, utcOffset: list[0].utc_offset_seconds, values: v };
	}
	return out;
}

/** Pressione e pioggia sulla griglia per un solo modello (livelli "Pressione" e "Pioggia"). */
export async function fetchExtraGrid(trip: Trip, model: string, grid: Grid): Promise<ExtraGrid> {
	const pts = gridPoints(grid);
	const params = new URLSearchParams({
		latitude: pts.lat.join(','),
		longitude: pts.lon.join(','),
		hourly: EXTRA_VARS.join(','),
		models: model,
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const list = asList(await getJson(`${FORECAST_URL}?${params}`));
	const times = list[0].hourly.time;
	const T = times.length;
	const N = list.length;
	const v = { pressure: new Float32Array(T * N).fill(NaN), precip: new Float32Array(T * N).fill(NaN) };
	list.forEach((loc, c) => {
		for (let t = 0; t < T; t++) {
			v.pressure[t * N + c] = loc.hourly.pressure_msl?.[t] ?? NaN;
			v.precip[t * N + c] = loc.hourly.precipitation?.[t] ?? NaN;
		}
	});
	return { model, grid, times, utcOffset: list[0].utc_offset_seconds, values: v };
}

export async function fetchMarineGrid(trip: Trip, grid: Grid): Promise<MarineGrid> {
	const pts = gridPoints(grid);
	const params = new URLSearchParams({
		latitude: pts.lat.join(','),
		longitude: pts.lon.join(','),
		hourly: MARINE_VARS.join(','),
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const list = asList(await getJson(`${MARINE_URL}?${params}`));
	const times = list[0].hourly.time;
	const T = times.length;
	const N = list.length;
	const v = {} as Record<MarineVar, Float32Array>;
	for (const k of ['wave', 'waveDir', 'wavePeriod', 'swell'] as MarineVar[]) v[k] = new Float32Array(T * N).fill(NaN);
	list.forEach((loc, c) => {
		const h = loc.hourly;
		for (let t = 0; t < T; t++) {
			const i = t * N + c;
			v.wave[i] = h.wave_height[t] ?? NaN;
			v.waveDir[i] = h.wave_direction[t] ?? NaN;
			v.wavePeriod[i] = h.wave_period[t] ?? NaN;
			v.swell[i] = h.swell_wave_height[t] ?? NaN;
		}
	});
	return { grid, times, utcOffset: list[0].utc_offset_seconds, values: v };
}

export interface PointSeries extends Series {
	model: string;
	wind: number[];
	gust: number[];
	dir: number[];
	precip: number[];
	pressure: number[];
}

/** Serie orarie in un punto per tutti i modelli, in un'unica richiesta. */
export async function fetchPoint(trip: Trip, lat: number, lon: number, models: string[]): Promise<PointSeries[]> {
	const params = new URLSearchParams({
		latitude: lat.toFixed(3),
		longitude: lon.toFixed(3),
		hourly: ATMO_VARS.join(','),
		models: models.join(','),
		wind_speed_unit: 'kn',
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const [r] = asList(await getJson(`${FORECAST_URL}?${params}`));
	const n = (a: (number | null)[] | undefined) => (a ?? r.hourly.time.map(() => null)).map((x) => x ?? NaN);
	return models
		.map((m) => ({
			model: m,
			times: r.hourly.time,
			utcOffset: r.utc_offset_seconds,
			wind: n(r.hourly[key('wind_speed_10m', m, models)]),
			gust: n(r.hourly[key('wind_gusts_10m', m, models)]),
			dir: n(r.hourly[key('wind_direction_10m', m, models)]),
			precip: n(r.hourly[key('precipitation', m, models)]),
			pressure: n(r.hourly[key('pressure_msl', m, models)])
		}))
		.filter((p) => p.wind.some((x) => !Number.isNaN(x)));
}

export interface PointMarine extends Series {
	wave: number[];
	waveDir: number[];
	period: number[];
	swell: number[];
}

export async function fetchPointMarine(trip: Trip, lat: number, lon: number): Promise<PointMarine> {
	const params = new URLSearchParams({
		latitude: lat.toFixed(3),
		longitude: lon.toFixed(3),
		hourly: MARINE_VARS.join(','),
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const [r] = asList(await getJson(`${MARINE_URL}?${params}`));
	const n = (a: (number | null)[]) => a.map((x) => x ?? NaN);
	return {
		times: r.hourly.time,
		utcOffset: r.utc_offset_seconds,
		wave: n(r.hourly.wave_height),
		waveDir: n(r.hourly.wave_direction),
		period: n(r.hourly.wave_period),
		swell: n(r.hourly.swell_wave_height)
	};
}

export interface Place {
	name: string;
	admin1?: string;
	country?: string;
	latitude: number;
	longitude: number;
}

export async function searchPlaces(q: string): Promise<Place[]> {
	const params = new URLSearchParams({ name: q, count: '8', language: 'it', format: 'json' });
	const body = (await getJson(`${GEO_URL}?${params}`)) as { results?: Place[] };
	return body.results ?? [];
}
