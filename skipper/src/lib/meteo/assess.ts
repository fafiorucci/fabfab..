import type { AtmoGrid, MarineGrid } from './api';
import { frame, localParts, nCells, pick, stats } from './grid';
import { modelById } from './models';
import type { Limits } from '#lib/trip.ts';

export type Level = 'go' | 'caution' | 'nogo' | 'nodata';

export interface ModelDay {
	model: string;
	wind: number;
	gust: number;
	over: boolean;
}

export interface DayVerdict {
	date: string;
	level: Level;
	reasons: string[];
	models: ModelDay[];
	wave: number;
}

/** Ore di navigazione considerate (ora locale, estremi inclusi). */
export const DAY_HOURS: [number, number] = [7, 20];
/** Oltre questa quota del limite il giorno diventa "attenzione". */
export const CAUTION_RATIO = 0.85;

/** Ore (indici) di navigazione raggruppate per giorno locale. */
function hoursByDay(times: number[], utcOffset: number) {
	const days = new Map<string, number[]>();
	times.forEach((t, i) => {
		const p = localParts(t, utcOffset);
		if (p.hour < DAY_HOURS[0] || p.hour > DAY_HOURS[1]) return;
		if (!days.has(p.date)) days.set(p.date, []);
		days.get(p.date)!.push(i);
	});
	return days;
}

/** 90° percentile sulle celle e sulle ore del giorno: robusto rispetto a singoli picchi. */
function p90Over(d: AtmoGrid | MarineGrid, key: string, hours: number[], cells: number[]) {
	const vals: number[] = [];
	for (const t of hours) for (const v of pick(frame(d as never, key as never, t), cells)) vals.push(v);
	return stats(vals).p90;
}

const fmt = (x: number, d = 0) => x.toFixed(d).replace('.', ',');

/** Valuta i giorni sulle celle indicate (di norma: punti di mare nella zona inquadrata). */
export function assess(atmo: AtmoGrid[], marine: MarineGrid | null, limits: Limits, cells?: number[]): DayVerdict[] {
	const ref = atmo[0] ?? marine;
	if (!ref) return [];
	if (!cells) cells = [...Array(nCells(ref.grid)).keys()];
	const days = hoursByDay(ref.times, ref.utcOffset);

	return [...days.entries()].map(([date, hours]) => {
		const models: ModelDay[] = [];
		for (const g of atmo) {
			const wind = p90Over(g, 'wind', hours, cells);
			const gust = p90Over(g, 'gust', hours, cells);
			if (Number.isNaN(wind)) continue; // modello senza dati per quel giorno (fuori orizzonte)
			models.push({ model: g.model, wind, gust, over: wind > limits.wind || gust > limits.gust });
		}
		const wave = marine ? p90Over(marine, 'wave', hours, cells) : NaN;

		const reasons: string[] = [];
		const overs = models.filter((m) => m.over);
		const near = models.filter((m) => !m.over && (m.wind > limits.wind * CAUTION_RATIO || m.gust > limits.gust * CAUTION_RATIO));
		const waveOver = wave > limits.wave;
		const waveNear = !waveOver && wave > limits.wave * CAUTION_RATIO;

		let level: Level;
		if (!models.length) {
			level = 'nodata';
			reasons.push('Nessun modello copre questo giorno.');
		} else {
			if (overs.length) {
				const names = overs.map((m) => modelById(m.model)?.label ?? m.model).join(', ');
				const maxGust = Math.max(...overs.map((m) => m.gust));
				reasons.push(`${overs.length} modelli su ${models.length} oltre i tuoi limiti (${names}); raffiche fino a ${fmt(maxGust)} kn.`);
			}
			if (near.length) reasons.push(`${near.length} modelli vicini ai limiti di vento.`);
			if (waveOver) reasons.push(`Onda significativa ${fmt(wave, 1)} m oltre il limite di ${fmt(limits.wave, 1)} m.`);
			else if (waveNear) reasons.push(`Onda significativa ${fmt(wave, 1)} m, vicina al limite.`);

			if (overs.length * 2 >= models.length || waveOver) level = 'nogo';
			else if (overs.length || near.length || waveNear) level = 'caution';
			else {
				level = 'go';
				const maxWind = Math.max(...models.map((m) => m.wind));
				reasons.push(`Tutti i ${models.length} modelli entro i limiti (vento fino a ${fmt(maxWind)} kn).`);
			}
			if (models.length < atmo.length) reasons.push(`${atmo.length - models.length} modelli non arrivano a questo giorno.`);
		}
		return { date, level, reasons, models, wave };
	});
}

export const LEVEL_LABEL: Record<Level, string> = {
	go: 'Si esce',
	caution: 'Attenzione',
	nogo: 'Meglio restare in porto',
	nodata: 'Dati insufficienti'
};
