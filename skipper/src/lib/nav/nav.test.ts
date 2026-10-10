import { describe, expect, it } from 'vitest';
import { angleDiff, bearing, crossTrackNm, distanceNm, pathNm, simplify } from './nav.ts';

describe('calcoli di navigazione', () => {
	it('un primo di latitudine è un miglio', () => {
		expect(distanceNm({ lat: 41, lon: 12 }, { lat: 41 + 1 / 60, lon: 12 })).toBeCloseTo(1, 2);
	});
	it('Fiumicino → Giannutri: distanza e rilevamento plausibili', () => {
		const a = { lat: 41.74, lon: 12.23 };
		const b = { lat: 42.25, lon: 11.1 };
		expect(distanceNm(a, b)).toBeGreaterThan(55);
		expect(distanceNm(a, b)).toBeLessThan(62);
		expect(bearing(a, b)).toBeGreaterThan(295);
		expect(bearing(a, b)).toBeLessThan(305);
	});
	it('rilevamenti cardinali', () => {
		const o = { lat: 0, lon: 0 };
		expect(bearing(o, { lat: 1, lon: 0 })).toBeCloseTo(0, 5);
		expect(bearing(o, { lat: 0, lon: 1 })).toBeCloseTo(90, 5);
		expect(bearing(o, { lat: -1, lon: 0 })).toBeCloseTo(180, 5);
		expect(bearing(o, { lat: 0, lon: -1 })).toBeCloseTo(270, 5);
	});
	it('fuori rotta: positivo a dritta, negativo a sinistra', () => {
		const from = { lat: 41, lon: 12 };
		const to = { lat: 42, lon: 12 }; // rotta verso nord
		expect(crossTrackNm(from, to, { lat: 41.5, lon: 12.02 })).toBeGreaterThan(0.8); // a est = a dritta
		expect(crossTrackNm(from, to, { lat: 41.5, lon: 11.98 })).toBeLessThan(-0.8);
		expect(Math.abs(crossTrackNm(from, to, { lat: 41.5, lon: 12 }))).toBeLessThan(1e-6);
	});
	it('differenza angolare con segno', () => {
		expect(angleDiff(350, 10)).toBe(20);
		expect(angleDiff(10, 350)).toBe(-20);
	});
	it('sfoltimento della traccia mantiene le svolte', () => {
		const line = Array.from({ length: 50 }, (_, i) => ({ lat: 41 + i * 0.01, lon: 12 }));
		const turn = Array.from({ length: 50 }, (_, i) => ({ lat: 41.49, lon: 12 + i * 0.01 }));
		const s = simplify([...line, ...turn], 0.05);
		expect(s.length).toBe(3);
		expect(pathNm(s)).toBeCloseTo(pathNm([...line, ...turn]), 0);
	});
});
