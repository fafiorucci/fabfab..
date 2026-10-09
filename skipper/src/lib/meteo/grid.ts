import type { Grid, GridData, Series } from './api';

export const nCells = (g: Grid) => g.lats.length * g.lons.length;

/** Indice orario più vicino all'istante richiesto (secondi UNIX). */
export function timeIndex(s: Series, t: number): number {
	const { times } = s;
	if (!times.length) return -1;
	if (t <= times[0]) return 0;
	if (t >= times[times.length - 1]) return times.length - 1;
	const step = times[1] - times[0];
	return Math.round((t - times[0]) / step);
}

/** Vista su un singolo istante di una variabile. */
export function frame<V extends string>(d: GridData<V>, key: V, t: number): Float32Array {
	const N = nCells(d.grid);
	return d.values[key].subarray(t * N, (t + 1) * N);
}

/** Interpolazione bilineare che ignora i nodi mancanti (es. terra per i dati marini). */
export function sample(g: Grid, f: ArrayLike<number>, lon: number, lat: number): number {
	const nx = g.lons.length;
	const ny = g.lats.length;
	const fx = ((lon - g.lons[0]) / (g.lons[nx - 1] - g.lons[0])) * (nx - 1);
	const fy = ((lat - g.lats[0]) / (g.lats[ny - 1] - g.lats[0])) * (ny - 1);
	if (!(fx >= 0 && fy >= 0 && fx <= nx - 1 && fy <= ny - 1)) return NaN;
	const x0 = Math.min(Math.floor(fx), nx - 2);
	const y0 = Math.min(Math.floor(fy), ny - 2);
	const ax = fx - x0;
	const ay = fy - y0;
	let sum = 0;
	let wsum = 0;
	const add = (x: number, y: number, w: number) => {
		const v = f[y * nx + x];
		if (w > 0 && !Number.isNaN(v)) {
			sum += v * w;
			wsum += w;
		}
	};
	add(x0, y0, (1 - ax) * (1 - ay));
	add(x0 + 1, y0, ax * (1 - ay));
	add(x0, y0 + 1, (1 - ax) * ay);
	add(x0 + 1, y0 + 1, ax * ay);
	return wsum > 0.05 ? sum / wsum : NaN;
}

/** Celle con dati marini validi = mare. */
export function seaMask(d: GridData<string> | null, key = 'wave'): Uint8Array | null {
	if (!d) return null;
	const N = nCells(d.grid);
	const arr = d.values[key];
	const mask = new Uint8Array(N);
	for (let i = 0; i < arr.length; i++) if (!Number.isNaN(arr[i])) mask[i % N] = 1;
	return mask.some(Boolean) ? mask : null;
}

/** Celle della griglia dentro un riquadro [ovest, sud, est, nord], opzionalmente solo mare. */
export function cellsIn(g: Grid, box: [number, number, number, number], mask?: Uint8Array | null): number[] {
	const out: number[] = [];
	const nx = g.lons.length;
	g.lats.forEach((lat, y) => {
		if (lat < box[1] || lat > box[3]) return;
		g.lons.forEach((lon, x) => {
			if (lon < box[0] || lon > box[2]) return;
			const i = y * nx + x;
			if (!mask || mask[i]) out.push(i);
		});
	});
	return out;
}

export interface Stats {
	min: number;
	mean: number;
	max: number;
	p90: number;
	n: number;
}

export function stats(values: Iterable<number>): Stats {
	const arr: number[] = [];
	for (const v of values) if (!Number.isNaN(v)) arr.push(v);
	if (!arr.length) return { min: NaN, mean: NaN, max: NaN, p90: NaN, n: 0 };
	arr.sort((a, b) => a - b);
	const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
	const p90 = arr[Math.min(arr.length - 1, Math.floor(arr.length * 0.9))];
	return { min: arr[0], mean, max: arr[arr.length - 1], p90, n: arr.length };
}

export function* pick(f: ArrayLike<number>, cells: number[]) {
	for (const c of cells) yield f[c];
}

/** Serie temporale di una statistica calcolata sulle celle indicate. */
export function areaSeries<V extends string>(d: GridData<V>, key: V, cells: number[], stat: keyof Stats = 'max'): number[] {
	return d.times.map((_, t) => stats(pick(frame(d, key, t), cells))[stat]);
}

/** Deviazione standard tra modelli, cella per cella: misura del disaccordo. */
export function spread(frames: ArrayLike<number>[], N: number): Float32Array {
	const out = new Float32Array(N).fill(NaN);
	for (let i = 0; i < N; i++) {
		let n = 0;
		let s = 0;
		let s2 = 0;
		for (const f of frames) {
			const v = f[i];
			if (Number.isNaN(v)) continue;
			n++;
			s += v;
			s2 += v * v;
		}
		if (n >= 2) out[i] = Math.sqrt(Math.max(0, s2 / n - (s / n) ** 2));
	}
	return out;
}

/** Giorno locale (YYYY-MM-DD) e ora locale di un istante, dato l'offset della zona. */
export function localParts(t: number, utcOffset: number) {
	const d = new Date((t + utcOffset) * 1000);
	return {
		date: d.toISOString().slice(0, 10),
		hour: d.getUTCHours(),
		label: d.toISOString().slice(11, 16)
	};
}

const WEEKDAYS = ['dom', 'lun', 'mar', 'mer', 'gio', 'ven', 'sab'];

export function dayLabel(date: string): string {
	const [y, m, d] = date.split('-').map(Number);
	const wd = WEEKDAYS[new Date(Date.UTC(y, m - 1, d)).getUTCDay()];
	return `${wd} ${d}/${m}`;
}
