import type { Feature, FeatureCollection, LineString, Point } from 'geojson';
import type { Grid } from '#lib/meteo/api.ts';
import { sample } from '#lib/meteo/grid.ts';

/** Fattore di infittimento prima di tracciare le linee: isobare morbide anche da una griglia rada. */
const UPSAMPLE = 5;

type Pt = [number, number];

/** Tratti di isolinea a livello `level` con il metodo "marching squares". */
function segments(xs: number[], ys: number[], f: (i: number, j: number) => number, level: number): [Pt, Pt][] {
	const out: [Pt, Pt][] = [];
	const lerp = (a: number, b: number, va: number, vb: number) => a + ((level - va) / (vb - va)) * (b - a);
	for (let j = 0; j < ys.length - 1; j++) {
		for (let i = 0; i < xs.length - 1; i++) {
			const v0 = f(i, j); // basso-sinistra
			const v1 = f(i + 1, j); // basso-destra
			const v2 = f(i + 1, j + 1); // alto-destra
			const v3 = f(i, j + 1); // alto-sinistra
			if ([v0, v1, v2, v3].some(Number.isNaN)) continue;
			const pts: Pt[] = [];
			if (v0 < level !== v1 < level) pts.push([lerp(xs[i], xs[i + 1], v0, v1), ys[j]]);
			if (v1 < level !== v2 < level) pts.push([xs[i + 1], lerp(ys[j], ys[j + 1], v1, v2)]);
			if (v2 < level !== v3 < level) pts.push([lerp(xs[i], xs[i + 1], v3, v2), ys[j + 1]]);
			if (v3 < level !== v0 < level) pts.push([xs[i], lerp(ys[j], ys[j + 1], v0, v3)]);
			if (pts.length === 2) out.push([pts[0], pts[1]]);
			else if (pts.length === 4) {
				out.push([pts[0], pts[1]]);
				out.push([pts[2], pts[3]]);
			}
		}
	}
	return out;
}

/** Unisce i tratti che si toccano in linee continue (servono per scriverci sopra il valore). */
function join(segs: [Pt, Pt][]): Pt[][] {
	const key = (p: Pt) => `${p[0].toFixed(5)},${p[1].toFixed(5)}`;
	const ends = new Map<string, number[]>();
	segs.forEach(([a, b], i) => {
		for (const p of [a, b]) {
			const k = key(p);
			if (!ends.has(k)) ends.set(k, []);
			ends.get(k)!.push(i);
		}
	});
	const used = new Uint8Array(segs.length);
	const lines: Pt[][] = [];
	const next = (p: Pt) => (ends.get(key(p)) ?? []).find((i) => !used[i]);
	for (let s = 0; s < segs.length; s++) {
		if (used[s]) continue;
		used[s] = 1;
		const line: Pt[] = [segs[s][0], segs[s][1]];
		for (const forward of [true, false]) {
			for (;;) {
				const tip = forward ? line[line.length - 1] : line[0];
				const n = next(tip);
				if (n === undefined) break;
				used[n] = 1;
				const [a, b] = segs[n];
				const other = key(a) === key(tip) ? b : a;
				if (forward) line.push(other);
				else line.unshift(other);
			}
		}
		lines.push(line);
	}
	return lines;
}

export interface IsobarOptions {
	/** Intervallo tra le isobare in hPa; se assente si sceglie in base all'escursione. */
	step?: number;
}

/** Isobare e centri di alta/bassa pressione dal campo di pressione su griglia. */
export function isobars(grid: Grid, pressure: ArrayLike<number>, opts: IsobarOptions = {}): FeatureCollection<LineString | Point> {
	const [w, s, e, n] = grid.bbox;
	const nx = (grid.lons.length - 1) * UPSAMPLE + 1;
	const ny = (grid.lats.length - 1) * UPSAMPLE + 1;
	const xs = Array.from({ length: nx }, (_, i) => w + ((e - w) * i) / (nx - 1));
	const ys = Array.from({ length: ny }, (_, j) => s + ((n - s) * j) / (ny - 1));
	const fine = new Float64Array(nx * ny);
	let lo = Infinity;
	let hi = -Infinity;
	for (let j = 0; j < ny; j++)
		for (let i = 0; i < nx; i++) {
			const v = sample(grid, pressure, xs[i], ys[j]);
			fine[j * nx + i] = v;
			if (!Number.isNaN(v)) {
				lo = Math.min(lo, v);
				hi = Math.max(hi, v);
			}
		}
	const features: Feature<LineString | Point>[] = [];
	if (!Number.isFinite(lo)) return { type: 'FeatureCollection', features };

	const step = opts.step ?? (hi - lo > 24 ? 4 : 2);
	const f = (i: number, j: number) => fine[j * nx + i];
	for (let level = Math.ceil(lo / step) * step; level <= hi; level += step) {
		for (const line of join(segments(xs, ys, f, level))) {
			if (line.length < 3) continue;
			features.push({ type: 'Feature', properties: { kind: 'isobar', p: level, major: level % 8 === 0 }, geometry: { type: 'LineString', coordinates: line } });
		}
	}

	// Centri: minimi e massimi locali sulla griglia originale (non sui bordi).
	const NX = grid.lons.length;
	const NY = grid.lats.length;
	for (let j = 1; j < NY - 1; j++)
		for (let i = 1; i < NX - 1; i++) {
			const v = pressure[j * NX + i];
			if (Number.isNaN(v)) continue;
			let isMin = true;
			let isMax = true;
			for (let dj = -1; dj <= 1; dj++)
				for (let di = -1; di <= 1; di++) {
					if (!di && !dj) continue;
					const u = pressure[(j + dj) * NX + i + di];
					if (Number.isNaN(u)) continue;
					if (u <= v) isMin = false;
					if (u >= v) isMax = false;
				}
			if (isMin || isMax)
				features.push({
					type: 'Feature',
					properties: { kind: isMin ? 'low' : 'high', label: `${isMin ? 'B' : 'A'}\n${Math.round(v)}` },
					geometry: { type: 'Point', coordinates: [grid.lons[i], grid.lats[j]] }
				});
		}
	return { type: 'FeatureCollection', features };
}
