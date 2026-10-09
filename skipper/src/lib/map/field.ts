import type { Feature, FeatureCollection } from 'geojson';
import type { Grid } from '#lib/meteo/api.ts';
import { sample } from '#lib/meteo/grid.ts';
import { colorAt, type LayerInfo } from '#lib/meteo/layers.ts';

const SIZE = 256;

const mercY = (lat: number) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));
const invMercY = (y: number) => (360 / Math.PI) * Math.atan(Math.exp(y)) - 90;

/**
 * Disegna il campo colorato con interpolazione bilineare.
 * Le righe sono campionate in coordinate Mercatore, così l'immagine combacia con la mappa.
 */
export function renderField(canvas: HTMLCanvasElement, grid: Grid, f: ArrayLike<number>, info: LayerInfo): string {
	canvas.width = SIZE;
	canvas.height = SIZE;
	const ctx = canvas.getContext('2d')!;
	const img = ctx.createImageData(SIZE, SIZE);
	const [w, s, e, n] = grid.bbox;
	const yTop = mercY(n);
	const yBot = mercY(s);
	for (let py = 0; py < SIZE; py++) {
		const lat = invMercY(yTop + ((yBot - yTop) * (py + 0.5)) / SIZE);
		for (let px = 0; px < SIZE; px++) {
			const lon = w + ((e - w) * (px + 0.5)) / SIZE;
			const c = colorAt(info, sample(grid, f, lon, lat));
			const o = (py * SIZE + px) * 4;
			img.data[o] = c[0];
			img.data[o + 1] = c[1];
			img.data[o + 2] = c[2];
			img.data[o + 3] = c[3];
		}
	}
	ctx.putImageData(img, 0, 0);
	return canvas.toDataURL();
}

export function bboxCorners(g: Grid): [[number, number], [number, number], [number, number], [number, number]] {
	const [w, s, e, n] = g.bbox;
	return [
		[w, n],
		[e, n],
		[e, s],
		[w, s]
	];
}

/** Frecce di direzione su ogni nodo della griglia (verso in cui va il vento o l'onda). */
export function arrowFeatures(grid: Grid, dirFrom: ArrayLike<number>, value: ArrayLike<number>): FeatureCollection {
	const features: Feature[] = [];
	const nx = grid.lons.length;
	grid.lats.forEach((lat, y) =>
		grid.lons.forEach((lon, x) => {
			const i = y * nx + x;
			const d = dirFrom[i];
			const v = value[i];
			if (Number.isNaN(d) || Number.isNaN(v)) return;
			features.push({
				type: 'Feature',
				geometry: { type: 'Point', coordinates: [lon, lat] },
				properties: { rot: (d + 180) % 360, v: Math.round(v * 10) / 10 }
			});
		})
	);
	return { type: 'FeatureCollection', features };
}

/** Icona freccia (SDF) per il layer simboli. */
export function arrowImage(): ImageData {
	const s = 48;
	const c = document.createElement('canvas');
	c.width = c.height = s;
	const ctx = c.getContext('2d')!;
	ctx.fillStyle = '#fff';
	ctx.beginPath();
	ctx.moveTo(s / 2, 4);
	ctx.lineTo(s / 2 + 11, 22);
	ctx.lineTo(s / 2 + 3.5, 20);
	ctx.lineTo(s / 2 + 3.5, s - 6);
	ctx.lineTo(s / 2 - 3.5, s - 6);
	ctx.lineTo(s / 2 - 3.5, 20);
	ctx.lineTo(s / 2 - 11, 22);
	ctx.closePath();
	ctx.fill();
	return ctx.getImageData(0, 0, s, s);
}
