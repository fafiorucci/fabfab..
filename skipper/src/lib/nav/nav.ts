/** Calcoli di navigazione sul globo (miglia nautiche, gradi veri) e file GPX. */

export interface LatLon {
	lat: number;
	lon: number;
}
export interface TrackPoint extends LatLon {
	/** Istante in ms */
	t: number;
	/** Velocità in nodi, se nota */
	sog?: number | null;
}
export interface Waypoint extends LatLon {
	name: string;
}

const R_NM = 3440.065; // raggio terrestre medio in miglia nautiche
const rad = (d: number) => (d * Math.PI) / 180;
const deg = (r: number) => (r * 180) / Math.PI;

/** Distanza ortodromica in miglia nautiche. */
export function distanceNm(a: LatLon, b: LatLon): number {
	const dLat = rad(b.lat - a.lat);
	const dLon = rad(b.lon - a.lon);
	const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLon / 2) ** 2;
	return 2 * R_NM * Math.asin(Math.min(1, Math.sqrt(h)));
}

/** Rilevamento iniziale vero da a verso b, 0–360°. */
export function bearing(a: LatLon, b: LatLon): number {
	const y = Math.sin(rad(b.lon - a.lon)) * Math.cos(rad(b.lat));
	const x = Math.cos(rad(a.lat)) * Math.sin(rad(b.lat)) - Math.sin(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.cos(rad(b.lon - a.lon));
	return (deg(Math.atan2(y, x)) + 360) % 360;
}

/**
 * Errore di fuori rotta (XTE) in miglia rispetto al tratto from→to:
 * positivo se la barca è a dritta della rotta, negativo se a sinistra.
 */
export function crossTrackNm(from: LatLon, to: LatLon, p: LatLon): number {
	const d13 = distanceNm(from, p) / R_NM;
	const t13 = rad(bearing(from, p));
	const t12 = rad(bearing(from, to));
	return Math.asin(Math.sin(d13) * Math.sin(t13 - t12)) * R_NM;
}

/** Lunghezza complessiva di una spezzata in miglia. */
export function pathNm(pts: LatLon[]): number {
	let d = 0;
	for (let i = 1; i < pts.length; i++) d += distanceNm(pts[i - 1], pts[i]);
	return d;
}

/** Differenza angolare con segno (−180…180) da a verso b. */
export const angleDiff = (a: number, b: number) => ((b - a + 540) % 360) - 180;

// ----- GPX -----

const esc = (s: string) => s.replace(/[<>&"']/g, (c) => `&#${c.charCodeAt(0)};`);
const fix = (n: number) => n.toFixed(6);

export function toGpx(opts: { name: string; track?: TrackPoint[]; route?: Waypoint[] }): string {
	const out = [
		'<?xml version="1.0" encoding="UTF-8"?>',
		'<gpx version="1.1" creator="Skipper WebApp — Onda Portante" xmlns="http://www.topografix.com/GPX/1/1">',
		`<metadata><name>${esc(opts.name)}</name><time>${new Date().toISOString()}</time></metadata>`
	];
	if (opts.route?.length) {
		out.push(`<rte><name>${esc(opts.name)} — rotta</name>`);
		for (const w of opts.route) out.push(`<rtept lat="${fix(w.lat)}" lon="${fix(w.lon)}"><name>${esc(w.name)}</name></rtept>`);
		out.push('</rte>');
	}
	if (opts.track?.length) {
		out.push(`<trk><name>${esc(opts.name)} — traccia</name><trkseg>`);
		for (const p of opts.track) out.push(`<trkpt lat="${fix(p.lat)}" lon="${fix(p.lon)}"><time>${new Date(p.t).toISOString()}</time></trkpt>`);
		out.push('</trkseg></trk>');
	}
	out.push('</gpx>');
	return out.join('\n');
}

/**
 * Legge un file GPX (Navionics, chartplotter, altre app): rotte, tracce e waypoint.
 * Restituisce i punti come rotta da seguire: prima la rotta, altrimenti i waypoint, altrimenti la traccia sfoltita.
 */
export function parseGpx(xml: string): { name: string; route: Waypoint[]; track: TrackPoint[] } {
	const doc = new DOMParser().parseFromString(xml, 'application/xml');
	if (doc.querySelector('parsererror')) throw new Error('File GPX non valido');
	const pt = (el: Element, i: number, prefix: string): Waypoint => ({
		lat: Number(el.getAttribute('lat')),
		lon: Number(el.getAttribute('lon')),
		name: el.querySelector('name')?.textContent?.trim() || `${prefix}${i + 1}`
	});
	const valid = (w: LatLon) => Number.isFinite(w.lat) && Number.isFinite(w.lon) && Math.abs(w.lat) <= 90 && Math.abs(w.lon) <= 180;
	const name = doc.querySelector('metadata > name, rte > name, trk > name')?.textContent?.trim() || 'Rotta importata';
	const rte = [...doc.querySelectorAll('rte > rtept')].map((e, i) => pt(e, i, 'WP')).filter(valid);
	const wpt = [...doc.querySelectorAll('gpx > wpt')].map((e, i) => pt(e, i, 'WP')).filter(valid);
	const track = [...doc.querySelectorAll('trkpt')]
		.map((e) => ({ lat: Number(e.getAttribute('lat')), lon: Number(e.getAttribute('lon')), t: Date.parse(e.querySelector('time')?.textContent ?? '') || 0 }))
		.filter(valid);
	let route = rte.length ? rte : wpt;
	if (!route.length && track.length) route = simplify(track, 0.2).map((p, i) => ({ lat: p.lat, lon: p.lon, name: `WP${i + 1}` }));
	return { name, route, track };
}

/** Sfoltisce una spezzata (Douglas-Peucker) con tolleranza in miglia. */
export function simplify<T extends LatLon>(pts: T[], tolNm: number): T[] {
	if (pts.length < 3) return pts.slice();
	let maxD = 0;
	let idx = 0;
	for (let i = 1; i < pts.length - 1; i++) {
		const d = Math.abs(crossTrackNm(pts[0], pts[pts.length - 1], pts[i]));
		if (d > maxD) {
			maxD = d;
			idx = i;
		}
	}
	if (maxD <= tolNm) return [pts[0], pts[pts.length - 1]];
	return [...simplify(pts.slice(0, idx + 1), tolNm).slice(0, -1), ...simplify(pts.slice(idx), tolNm)];
}
