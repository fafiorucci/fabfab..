import type { Trip } from '#lib/trip.ts';
import { addDays } from '#lib/trip.ts';

const FORECAST_URL = 'https://api.open-meteo.com/v1/forecast';
const MARINE_URL = 'https://marine-api.open-meteo.com/v1/marine';
const GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search';

/** Passi possibili della griglia, in gradi: si sceglie il più fine compatibile con il numero di punti. */
export const STEPS = [0.1, 0.125, 0.25, 0.5, 1, 2, 4] as const;
/**
 * Punti massimi per vista. Ogni punto conta come una chiamata Open-Meteo per modello:
 * 64 punti × (6 modelli + onda) ≈ 450 chiamate per zona nuova, sul limite gratuito di 10.000 al giorno.
 * L'interpolazione bilineare rende comunque il campo continuo.
 */
export const MAX_POINTS = 64;

export const ATMO_VARS = ['wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m', 'pressure_msl', 'precipitation'] as const;
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
export type MarineGrid = GridData<MarineVar>;

export type BBox = [number, number, number, number];

function gridOn(bbox: BBox, step: number): Grid {
	// Bordi allineati ai multipli del passo: gli spostamenti più piccoli di un passo riusano la stessa griglia.
	const q = step;
	const w = Math.max(-180, Math.floor((bbox[0] - step) / q) * q);
	const e = Math.min(180, Math.ceil((bbox[2] + step) / q) * q);
	const s = Math.max(-80, Math.floor((bbox[1] - step) / q) * q);
	const n = Math.min(80, Math.ceil((bbox[3] + step) / q) * q);
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
export function gridForView(bbox: BBox): Grid {
	let g = gridOn(bbox, STEPS[STEPS.length - 1]);
	for (const step of STEPS) {
		g = gridOn(bbox, step);
		if (g.lats.length * g.lons.length <= MAX_POINTS) break;
	}
	return g;
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

function countCalls(url: string) {
	const lat = new URL(url).searchParams.get('latitude');
	const n = lat ? lat.split(',').length : 1;
	try {
		localStorage.setItem(BUDGET_KEY, JSON.stringify({ day: new Date().toDateString(), n: callsToday() + n }));
	} catch {
		/* storage non disponibile */
	}
}

async function getJson(url: string): Promise<unknown> {
	const hit = cache.get(url);
	if (hit) return hit;
	const p = (async () => {
		let res: Response;
		try {
			res = await fetch(url);
			countCalls(url);
		} catch {
			throw new Error('Rete non disponibile: nessun dato in memoria per questa richiesta.');
		}
		const body = await res.json().catch(() => null);
		if (!res.ok || (body && body.error)) {
			const reason: string = body?.reason ?? `HTTP ${res.status}`;
			if (/limit exceeded/i.test(reason)) throw new Error('Limite giornaliero di Open-Meteo raggiunto per questa rete. Riprova più tardi.');
			throw new Error(reason);
		}
		return body;
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

export async function fetchAtmoGrid(trip: Trip, model: string, grid: Grid): Promise<AtmoGrid> {
	const pts = gridPoints(grid);
	const params = new URLSearchParams({
		latitude: pts.lat.join(','),
		longitude: pts.lon.join(','),
		hourly: ATMO_VARS.join(','),
		models: model,
		wind_speed_unit: 'kn',
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const list = asList(await getJson(`${FORECAST_URL}?${params}`));
	const times = list[0].hourly.time;
	const T = times.length;
	const N = list.length;
	const v = {} as Record<AtmoVar, Float32Array>;
	for (const k of ['wind', 'dir', 'gust', 'pressure', 'precip', 'u', 'v'] as AtmoVar[]) v[k] = new Float32Array(T * N).fill(NaN);
	list.forEach((loc, c) => {
		const h = loc.hourly;
		for (let t = 0; t < T; t++) {
			const i = t * N + c;
			const s = h.wind_speed_10m[t];
			const d = h.wind_direction_10m[t];
			v.wind[i] = s ?? NaN;
			v.dir[i] = d ?? NaN;
			v.gust[i] = h.wind_gusts_10m[t] ?? NaN;
			v.pressure[i] = h.pressure_msl[t] ?? NaN;
			v.precip[i] = h.precipitation[t] ?? NaN;
			if (s != null && d != null) [v.u[i], v.v[i]] = toUV(s, d);
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
}

export async function fetchPoint(trip: Trip, lat: number, lon: number, model: string): Promise<PointSeries> {
	const params = new URLSearchParams({
		latitude: lat.toFixed(3),
		longitude: lon.toFixed(3),
		hourly: 'wind_speed_10m,wind_direction_10m,wind_gusts_10m',
		models: model,
		wind_speed_unit: 'kn',
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const [r] = asList(await getJson(`${FORECAST_URL}?${params}`));
	const n = (a: (number | null)[]) => a.map((x) => x ?? NaN);
	return {
		model,
		times: r.hourly.time,
		utcOffset: r.utc_offset_seconds,
		wind: n(r.hourly.wind_speed_10m),
		gust: n(r.hourly.wind_gusts_10m),
		dir: n(r.hourly.wind_direction_10m)
	};
}

export interface PointMarine extends Series {
	wave: number[];
	period: number[];
}

export async function fetchPointMarine(trip: Trip, lat: number, lon: number): Promise<PointMarine> {
	const params = new URLSearchParams({
		latitude: lat.toFixed(3),
		longitude: lon.toFixed(3),
		hourly: 'wave_height,wave_period',
		timezone: 'auto',
		timeformat: 'unixtime',
		...dateRange(trip)
	});
	const [r] = asList(await getJson(`${MARINE_URL}?${params}`));
	return {
		times: r.hourly.time,
		utcOffset: r.utc_offset_seconds,
		wave: r.hourly.wave_height.map((x) => x ?? NaN),
		period: r.hourly.wave_period.map((x) => x ?? NaN)
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
