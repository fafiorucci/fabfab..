import type { Map as MlMap } from 'maplibre-gl';
import type { Grid } from '#lib/meteo/api.ts';
import { sample } from '#lib/meteo/grid.ts';

interface P {
	lon: number;
	lat: number;
	age: number;
}

/** Particelle di vento animate su un canvas sovrapposto alla mappa (stile Windy). */
export class Particles {
	private ctx: CanvasRenderingContext2D;
	private parts: P[] = [];
	private raf = 0;
	private u: ArrayLike<number> | null = null;
	private v: ArrayLike<number> | null = null;
	private grid: Grid | null = null;
	private running = false;

	constructor(
		private map: MlMap,
		private canvas: HTMLCanvasElement
	) {
		this.ctx = canvas.getContext('2d')!;
		const clear = () => this.clear();
		map.on('movestart', clear);
		map.on('resize', () => this.resize());
		this.resize();
	}

	resize() {
		const r = this.map.getContainer().getBoundingClientRect();
		const dpr = window.devicePixelRatio || 1;
		this.canvas.width = r.width * dpr;
		this.canvas.height = r.height * dpr;
		this.canvas.style.width = `${r.width}px`;
		this.canvas.style.height = `${r.height}px`;
		this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
	}

	setField(grid: Grid | null, u: ArrayLike<number> | null, v: ArrayLike<number> | null) {
		const reseed = this.grid !== grid;
		this.grid = grid;
		this.u = u;
		this.v = v;
		if (reseed) this.parts = [];
	}

	start() {
		if (this.running) return;
		this.running = true;
		const loop = () => {
			if (!this.running) return;
			if (!document.hidden) this.step();
			this.raf = requestAnimationFrame(loop);
		};
		loop();
	}

	stop() {
		this.running = false;
		cancelAnimationFrame(this.raf);
		this.clear();
	}

	clear() {
		this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
	}

	private spawn(): P {
		const g = this.grid!;
		const [w, s, e, n] = g.bbox;
		return { lon: w + Math.random() * (e - w), lat: s + Math.random() * (n - s), age: Math.floor(Math.random() * 80) };
	}

	private step() {
		const { ctx, map, grid, u, v } = this;
		const w = this.canvas.width;
		const h = this.canvas.height;
		ctx.save();
		ctx.setTransform(1, 0, 0, 1, 0, 0);
		ctx.globalCompositeOperation = 'destination-in';
		ctx.fillStyle = 'rgba(0,0,0,0.9)';
		ctx.fillRect(0, 0, w, h);
		ctx.restore();
		ctx.globalCompositeOperation = 'source-over';
		if (!grid || !u || !v || map.isMoving()) return;

		const target = Math.min(1500, Math.max(300, Math.round((w * h) / 2500)));
		while (this.parts.length < target) this.parts.push(this.spawn());

		// Spostamento in gradi per nodo per frame, costante a schermo a ogni zoom.
		const pxPerDeg = (512 * 2 ** map.getZoom()) / 360;
		const k = 0.1 / pxPerDeg;

		ctx.lineWidth = 1.2;
		ctx.strokeStyle = 'rgba(255,255,255,0.85)';
		ctx.beginPath();
		for (let i = 0; i < this.parts.length; i++) {
			const p = this.parts[i];
			const uu = sample(grid, u, p.lon, p.lat);
			const vv = sample(grid, v, p.lon, p.lat);
			if (Number.isNaN(uu) || Number.isNaN(vv) || p.age > 90) {
				this.parts[i] = this.spawn();
				continue;
			}
			const a = map.project([p.lon, p.lat]);
			p.lon += (uu * k) / Math.cos((p.lat * Math.PI) / 180);
			p.lat += vv * k;
			p.age++;
			const b = map.project([p.lon, p.lat]);
			ctx.moveTo(a.x, a.y);
			ctx.lineTo(b.x, b.y);
		}
		ctx.stroke();
	}
}
