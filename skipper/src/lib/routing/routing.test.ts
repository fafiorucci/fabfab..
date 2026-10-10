import { describe, expect, it } from 'vitest';
import { BUILTIN_POLARS, boatSpeed, parsePolar } from './polars';
import { bearing, computeRoute, distNm, twaOf } from './router';

const polar = BUILTIN_POLARS.find((p) => p.id === 'cruiser-38')!;
const T0 = 1_800_000_000;
const start = { lon: 10.0, lat: 42.0 };
const north = { lon: 10.0, lat: 42.5 }; // 30 miglia a nord
const constWind = (tws: number, twd: number) => () => ({ tws, twd });
const openSea = () => true;

describe('polari', () => {
	it('interpola tra i valori della tabella e annulla prua al vento', () => {
		expect(boatSpeed(polar, 90, 12)).toBeCloseTo(7.2);
		expect(boatSpeed(polar, 90, 13)).toBeCloseTo(7.3);
		expect(boatSpeed(polar, 0, 15)).toBe(0);
		expect(boatSpeed(polar, 25, 15)).toBe(0);
		expect(boatSpeed(polar, 90, 0)).toBe(0);
		expect(boatSpeed(polar, 90, 3)).toBeCloseTo(2.5); // metà del valore a 6 nodi
	});

	it('legge un file polare in formato tabella', () => {
		const p = parsePolar('TWA\\TWS\t6\t10\t16\n0\t0\t0\t0\n45\t4.0\t5.5\t6.2\n90\t5.0\t6.8\t7.6\n150\t3.8\t5.6\t7.1', 'Prova');
		expect(p.tws).toEqual([6, 10, 16]);
		expect(p.twa).toEqual([45, 90, 150]);
		expect(boatSpeed(p, 90, 10)).toBeCloseTo(6.8);
		expect(() => parsePolar('solo una riga', 'x')).toThrow();
	});
});

describe('geometria', () => {
	it('misura distanze, rilevamenti e angoli al vento', () => {
		expect(distNm(start, north)).toBeCloseTo(30, 1);
		expect(bearing(start, north)).toBeCloseTo(0, 5);
		expect(twaOf(0, 90)).toBe(90);
		expect(twaOf(350, 10)).toBe(20);
		expect(twaOf(180, 0)).toBe(180);
	});
});

describe('isocrone', () => {
	const base = { start, end: north, t0: T0, maxHours: 24, polar, efficiency: 1, sea: openSea };

	it('con vento al traverso va diretta, nel tempo atteso', () => {
		const r = computeRoute({ ...base, wind: constWind(12, 90) });
		expect(r.reached).toBe(true);
		const v = boatSpeed(polar, 90, 12);
		expect(r.hours).toBeGreaterThan((30 / v) * 0.97);
		expect(r.hours).toBeLessThan((30 / v) * 1.08);
		expect(r.distanceNm).toBeLessThan(31);
	});

	it('controvento bordeggia: percorre più strada della distanza diretta', () => {
		const r = computeRoute({ ...base, wind: constWind(12, 0) });
		expect(r.reached).toBe(true);
		expect(r.distanceNm).toBeGreaterThan(36);
		for (const p of r.points.slice(0, -1)) expect(p.twa).toBeGreaterThanOrEqual(38);
	});

	it('aggira un’isola sulla rotta diretta', () => {
		const island = (lon: number, lat: number) => !(Math.abs(lon - 10.0) < 0.08 && lat > 42.15 && lat < 42.3);
		const r = computeRoute({ ...base, wind: constWind(12, 90), sea: island });
		expect(r.reached).toBe(true);
		for (const p of r.points) expect(island(p.lon, p.lat)).toBe(true);
	});

	it('in calma piatta senza motore non arriva, col motore sì', () => {
		const calm = constWind(0.5, 0);
		expect(computeRoute({ ...base, maxHours: 10, wind: calm }).reached).toBe(false);
		const m = computeRoute({ ...base, maxHours: 10, wind: calm, motor: { below: 3, speed: 6 } });
		expect(m.reached).toBe(true);
		expect(m.hours).toBeCloseTo(5, 0);
		expect(m.motorHours).toBeGreaterThan(4.5);
	});
});
