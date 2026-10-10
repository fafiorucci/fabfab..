import { boatSpeed, type Polar } from './polars';

export interface LonLat {
	lon: number;
	lat: number;
}

/** Vento reale in un punto e istante: intensità (nodi) e direzione di provenienza (gradi). */
export type WindAt = (lon: number, lat: number, t: number) => { tws: number; twd: number } | null;
/** true se il punto è in mare navigabile. */
export type SeaAt = (lon: number, lat: number) => boolean;

export interface RouteOptions {
	start: LonLat;
	end: LonLat;
	/** Istante di partenza (secondi UNIX) */
	t0: number;
	/** Ore massime di navigazione considerate */
	maxHours: number;
	polar: Polar;
	/** Rendimento rispetto alla polare (0–1): equipaggio, carico, onda */
	efficiency: number;
	/** Motore quando a vela si andrebbe sotto `below` nodi */
	motor?: { below: number; speed: number } | null;
	wind: WindAt;
	sea: SeaAt;
	/** Passo temporale in ore */
	dt?: number;
	/** Passo delle prue provate, gradi */
	headingStep?: number;
	/** Ampiezza dei settori per sfoltire le isocrone, gradi */
	sectorDeg?: number;
	/** Distanza da partenza e arrivo entro cui non si controlla la costa (miglia): porti e rade */
	harbourNm?: number;
}

export interface RoutePoint extends LonLat {
	t: number;
	heading: number;
	tws: number;
	twd: number;
	twa: number;
	speed: number;
	motor: boolean;
}

export interface RouteResult {
	reached: boolean;
	points: RoutePoint[];
	/** Isocrone, una per passo temporale, come linee ordinate */
	isochrones: LonLat[][];
	distanceNm: number;
	hours: number;
	motorHours: number;
	reason?: string;
}

const RAD = Math.PI / 180;

/** Distanza in miglia (approssimazione locale, adeguata alle tratte costiere e di altura del Mediterraneo). */
export function distNm(a: LonLat, b: LonLat): number {
	const dLat = (b.lat - a.lat) * 60;
	const dLon = (b.lon - a.lon) * 60 * Math.cos(((a.lat + b.lat) / 2) * RAD);
	return Math.hypot(dLat, dLon);
}

/** Rilevamento vero da a verso b, gradi 0–360. */
export function bearing(a: LonLat, b: LonLat): number {
	const dLat = b.lat - a.lat;
	const dLon = (b.lon - a.lon) * Math.cos(((a.lat + b.lat) / 2) * RAD);
	return (Math.atan2(dLon, dLat) / RAD + 360) % 360;
}

function move(p: LonLat, heading: number, nm: number): LonLat {
	const lat = p.lat + (nm * Math.cos(heading * RAD)) / 60;
	const lon = p.lon + (nm * Math.sin(heading * RAD)) / (60 * Math.cos(((p.lat + lat) / 2) * RAD));
	return { lon, lat };
}

/** Angolo tra prua e direzione di provenienza del vento, 0–180. */
export function twaOf(heading: number, twd: number): number {
	return Math.abs(((heading - twd + 540) % 360) - 180);
}

interface Node extends RoutePoint {
	parent: Node | null;
}

/**
 * Rotta ottima con il metodo delle isocrone: a ogni passo si provano tutte le prue
 * da ogni punto del fronte e si tiene, per ogni settore di rilevamento dalla partenza,
 * il punto più lontano. Ci si ferma appena un punto può raggiungere l'arrivo.
 */
export function computeRoute(o: RouteOptions): RouteResult {
	const dt = o.dt ?? 1;
	const hStep = o.headingStep ?? 5;
	const sector = o.sectorDeg ?? 2;
	const harbour = o.harbourNm ?? 3;
	const direct = bearing(o.start, o.end);

	const seaOk = (a: LonLat, b: LonLat) => {
		for (const f of [0.34, 0.67, 1]) {
			const p = { lon: a.lon + (b.lon - a.lon) * f, lat: a.lat + (b.lat - a.lat) * f };
			if (distNm(p, o.start) < harbour || distNm(p, o.end) < harbour) continue;
			if (!o.sea(p.lon, p.lat)) return false;
		}
		return true;
	};

	const speedAt = (p: LonLat, heading: number, t: number) => {
		const w = o.wind(p.lon, p.lat, t);
		if (!w) return null;
		const twa = twaOf(heading, w.twd);
		let speed = boatSpeed(o.polar, twa, w.tws) * o.efficiency;
		let motor = false;
		if (o.motor && speed < o.motor.below) {
			speed = o.motor.speed;
			motor = true;
		}
		return { ...w, twa, speed, motor };
	};

	const startNode: Node = { ...o.start, t: o.t0, heading: direct, tws: 0, twd: 0, twa: 0, speed: 0, motor: false, parent: null };
	let front: Node[] = [startNode];
	const isochrones: LonLat[][] = [];
	const steps = Math.floor(o.maxHours / dt);

	for (let step = 0; step < steps; step++) {
		// 1. Si può arrivare entro questo passo da qualche punto del fronte?
		let best: Node | null = null;
		for (const p of front) {
			const h = bearing(p, o.end);
			const s = speedAt(p, h, p.t);
			if (!s || s.speed <= 0.1) continue;
			const d = distNm(p, o.end);
			if (d > s.speed * dt || !seaOk(p, o.end)) continue;
			const t = p.t + (d / s.speed) * 3600;
			if (!best || t < best.t) best = { ...o.end, t, heading: h, ...s, parent: p };
		}
		if (best) return finish(best, true, isochrones);

		// 2. Espansione del fronte.
		const buckets = new Map<number, Node>();
		for (const p of front) {
			for (let h = 0; h < 360; h += hStep) {
				const s = speedAt(p, h, p.t);
				if (!s || s.speed <= 0.1) continue;
				const q = move(p, h, s.speed * dt);
				if (!seaOk(p, q)) continue;
				const fromStart = bearing(o.start, q);
				// Non si esplora all'indietro rispetto alla direzione dell'arrivo.
				if (twaOf(fromStart, direct) > 110) continue;
				const key = Math.round(fromStart / sector);
				const node: Node = { ...q, t: p.t + dt * 3600, heading: h, ...s, parent: p };
				const prev = buckets.get(key);
				if (!prev || distNm(o.start, q) > distNm(o.start, prev)) buckets.set(key, node);
			}
		}
		if (!buckets.size) return finish(front[0], false, isochrones, 'Nessuna prua percorribile: vento assente, fuori dalla zona dei dati o costa di mezzo.');
		front = [...buckets.entries()].sort((a, b) => a[0] - b[0]).map(([, n]) => n);
		isochrones.push(front.map(({ lon, lat }) => ({ lon, lat })));
	}

	// Non raggiunto nel tempo disponibile: si mostra la rotta del punto più vicino all'arrivo.
	const closest = front.reduce((a, b) => (distNm(a, o.end) < distNm(b, o.end) ? a : b));
	return finish(closest, false, isochrones, `Arrivo non raggiunto entro ${o.maxHours} ore con i dati disponibili.`);
}

function finish(last: Node, reached: boolean, isochrones: LonLat[][], reason?: string): RouteResult {
	const pts: RoutePoint[] = [];
	for (let n: Node | null = last; n; n = n.parent) {
		const { parent: _p, ...rest } = n;
		pts.unshift(rest);
	}
	// Ogni punto porta la prua e il vento del tratto che vi arriva: li si sposta sul punto di partenza del tratto.
	const legs = pts.map((p, i) => (i < pts.length - 1 ? { ...p, heading: pts[i + 1].heading, tws: pts[i + 1].tws, twd: pts[i + 1].twd, twa: pts[i + 1].twa, speed: pts[i + 1].speed, motor: pts[i + 1].motor } : p));
	let distanceNm = 0;
	let motorHours = 0;
	for (let i = 1; i < legs.length; i++) {
		distanceNm += distNm(legs[i - 1], legs[i]);
		if (legs[i - 1].motor) motorHours += (legs[i].t - legs[i - 1].t) / 3600;
	}
	const hours = legs.length > 1 ? (legs[legs.length - 1].t - legs[0].t) / 3600 : 0;
	return { reached, points: legs, isochrones, distanceNm, hours, motorHours, reason };
}
