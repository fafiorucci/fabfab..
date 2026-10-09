import { describe, expect, it } from 'vitest';
import { gridForView, gridKey, MAX_POINTS, type AtmoGrid, type Grid, type AtmoVar, type MarineGrid, type MarineVar } from './api';
import { assess } from './assess';
import { cellsIn, localParts, sample, spread, stats, timeIndex } from './grid';
import { decodeTrip, defaultTrip, encodeTrip, validateTrip } from '../trip';

const grid: Grid = {
	lats: [42.25, 42.5, 42.75, 43, 43.25],
	lons: [9.75, 10, 10.25, 10.5, 10.75],
	bbox: [9.75, 42.25, 10.75, 43.25]
};
const N = grid.lats.length * grid.lons.length;

/** 48 ore dal 2026-10-10 00:00 ora locale (UTC+2). */
const OFF = 7200;
const T0 = Date.UTC(2026, 9, 10) / 1000 - OFF;
const times = Array.from({ length: 48 }, (_, i) => T0 + i * 3600);

function atmo(model: string, wind: number, gust = wind * 1.3): AtmoGrid {
	const values = {} as Record<AtmoVar, Float32Array>;
	for (const k of ['wind', 'dir', 'gust', 'pressure', 'precip', 'u', 'v'] as AtmoVar[]) values[k] = new Float32Array(times.length * N).fill(0);
	values.wind.fill(wind);
	values.gust.fill(gust);
	return { model, grid, times, utcOffset: OFF, values };
}

function marine(wave: number): MarineGrid {
	const values = {} as Record<MarineVar, Float32Array>;
	for (const k of ['wave', 'waveDir', 'wavePeriod', 'swell'] as MarineVar[]) values[k] = new Float32Array(times.length * N).fill(wave);
	return { grid, times, utcOffset: OFF, values };
}

describe('griglia della vista', () => {
	it('copre tutta la zona inquadrata con un margine', () => {
		const view: [number, number, number, number] = [8.3, 41.1, 12.9, 44.2];
		const g = gridForView(view);
		expect(g.bbox[0]).toBeLessThan(view[0]);
		expect(g.bbox[1]).toBeLessThan(view[1]);
		expect(g.bbox[2]).toBeGreaterThan(view[2]);
		expect(g.bbox[3]).toBeGreaterThan(view[3]);
		expect(g.lats.length * g.lons.length).toBeLessThanOrEqual(MAX_POINTS);
	});

	it('si infittisce zoomando e resta entro il limite di punti', () => {
		const wide = gridForView([3, 36, 18, 45]); // mezzo Mediterraneo
		const close = gridForView([10.2, 42.7, 10.5, 42.9]); // un golfo
		const step = (g: Grid) => g.lats[1] - g.lats[0];
		expect(step(close)).toBeLessThan(step(wide));
		expect(step(close)).toBeCloseTo(0.1);
		for (const g of [wide, close]) expect(g.lats.length * g.lons.length).toBeLessThanOrEqual(MAX_POINTS);
	});

	it('riusa la stessa griglia per piccoli spostamenti', () => {
		const a = gridForView([9.2, 41.6, 11.3, 43.3]);
		const b = gridForView([9.25, 41.65, 11.35, 43.35]); // spostamento di ~3 miglia
		expect(gridKey(b)).toBe(gridKey(a));
	});
});

describe('griglia', () => {
	it('interpola linearmente e ignora i nodi mancanti', () => {
		const f = new Float32Array(N).map((_, i) => i % grid.lons.length); // cresce verso est
		expect(sample(grid, f, 10.125, 42.6)).toBeCloseTo(1.5);
		const g = Float32Array.from(f);
		g[1] = NaN;
		expect(sample(grid, g, 10.05, 42.25)).toBeCloseTo(2); // il nodo NaN è escluso, resta il vicino
		expect(sample(grid, g, 10, 42.25)).toBeNaN(); // sul nodo mancante non si inventa un valore
		expect(sample(grid, f, 5, 42.6)).toBeNaN(); // fuori griglia
	});

	it('seleziona le celle nel riquadro visibile', () => {
		expect(cellsIn(grid, [10.1, 42.6, 10.6, 43.1])).toHaveLength(4);
	});

	it('trova l’ora più vicina e le parti locali', () => {
		expect(timeIndex({ times, utcOffset: OFF }, T0 + 3 * 3600 + 1000)).toBe(3);
		expect(localParts(T0 + 8 * 3600, OFF)).toMatchObject({ date: '2026-10-10', hour: 8 });
	});

	it('calcola statistiche e disaccordo', () => {
		expect(stats([1, 2, 3, NaN])).toMatchObject({ min: 1, max: 3, mean: 2, n: 3 });
		const s = spread([new Float32Array([10, 5]), new Float32Array([20, 5]), new Float32Array([NaN, NaN])], 2);
		expect(s[0]).toBeCloseTo(5);
		expect(s[1]).toBeCloseTo(0);
	});
});

describe('valutazione', () => {
	const limits = { wind: 20, gust: 28, wave: 1.5 };

	it('via libera se tutti i modelli sono entro i limiti', () => {
		const v = assess([atmo('a', 10), atmo('b', 12)], marine(0.6), limits);
		expect(v.map((d) => d.date)).toEqual(['2026-10-10', '2026-10-11']);
		expect(v[0].level).toBe('go');
	});

	it('attenzione se un solo modello su tre supera i limiti', () => {
		const v = assess([atmo('a', 10), atmo('b', 12), atmo('c', 24)], marine(0.6), limits);
		expect(v[0].level).toBe('caution');
		expect(v[0].models.find((m) => m.model === 'c')?.over).toBe(true);
	});

	it('restare in porto se la maggioranza supera o l’onda è oltre il limite', () => {
		expect(assess([atmo('a', 25), atmo('b', 22)], marine(0.6), limits)[0].level).toBe('nogo');
		expect(assess([atmo('a', 10)], marine(2.2), limits)[0].level).toBe('nogo');
	});

	it('dati insufficienti se nessun modello copre il giorno', () => {
		const g = atmo('a', 10);
		g.values.wind.fill(NaN);
		expect(assess([g], null, limits)[0].level).toBe('nodata');
	});
});

describe('uscita', () => {
	it('il link di invito conserva tutti i dati, anche accenti', () => {
		const t = { ...defaultTrip(), name: 'Giro dell’Elba è bello', date: '2026-10-10' };
		expect(decodeTrip(encodeTrip(t))).toEqual(t);
		expect(decodeTrip('spazzatura')).toBeNull();
	});

	it('valida data e zona', () => {
		const t = { ...defaultTrip(), date: '2026-10-10' };
		expect(validateTrip(t, '2026-10-09')).toBeNull();
		expect(validateTrip({ ...t, date: '2026-10-01' }, '2026-10-09')).toMatch(/passata/);
		expect(validateTrip({ ...t, lat: 60 }, '2026-10-09')).toMatch(/Mediterraneo/);
	});
});
