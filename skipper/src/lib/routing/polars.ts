/**
 * Polari: velocità della barca (nodi) in funzione dell'angolo al vento reale (TWA, gradi)
 * e dell'intensità del vento reale (TWS, nodi).
 */
export interface Polar {
	id: string;
	name: string;
	/** Colonne: intensità del vento (nodi), crescenti */
	tws: number[];
	/** Righe: angoli al vento (gradi 0–180), crescenti */
	twa: number[];
	/** speeds[riga TWA][colonna TWS] */
	speeds: number[][];
	/** true se importata dall'utente */
	custom?: boolean;
}

const TWS = [6, 8, 10, 12, 14, 16, 20, 25];
const TWA = [40, 52, 60, 75, 90, 110, 120, 135, 150, 165, 180];

/** Base: crociera di circa 38 piedi (valori indicativi, ricavati da polari di barche di serie). */
const BASE = [
	[3.6, 4.6, 5.2, 5.6, 5.8, 5.9, 6.0, 5.9],
	[4.4, 5.4, 6.0, 6.4, 6.6, 6.7, 6.8, 6.7],
	[4.7, 5.7, 6.3, 6.7, 6.9, 7.0, 7.1, 7.1],
	[5.0, 6.0, 6.6, 7.0, 7.2, 7.4, 7.5, 7.6],
	[5.0, 6.1, 6.8, 7.2, 7.4, 7.6, 7.9, 8.1],
	[4.9, 6.0, 6.8, 7.2, 7.5, 7.8, 8.2, 8.6],
	[4.7, 5.8, 6.6, 7.1, 7.4, 7.7, 8.2, 8.8],
	[4.2, 5.3, 6.2, 6.8, 7.2, 7.5, 8.0, 8.7],
	[3.6, 4.6, 5.5, 6.2, 6.8, 7.2, 7.7, 8.3],
	[3.1, 4.1, 5.0, 5.7, 6.3, 6.8, 7.4, 8.0],
	[2.9, 3.8, 4.7, 5.4, 6.0, 6.5, 7.2, 7.8]
];

/** Ricava una polare tipo dalla base: fattore generale e correzioni per bolina e lasco. */
function derive(id: string, name: string, k: number, upwind = 1, reaching = 1, minTwa = 40): Polar {
	const speeds = BASE.map((row, i) => {
		const a = TWA[i];
		const f = k * (a < 70 ? upwind : a <= 135 ? reaching : 1);
		return row.map((v) => +(a < minTwa ? 0 : v * f).toFixed(2));
	});
	return { id, name, tws: TWS, twa: TWA, speeds };
}

export const BUILTIN_POLARS: Polar[] = [
	derive('cruiser-32', 'Crociera 30–34 piedi', 0.88),
	derive('cruiser-38', 'Crociera 36–40 piedi', 1),
	derive('cruiser-45', 'Crociera 42–46 piedi', 1.08),
	derive('cruiser-50', 'Crociera 50 piedi e oltre', 1.16),
	derive('performance-40', 'Performance / regata 40 piedi', 1.12, 1.06, 1.08),
	derive('catamaran-42', 'Catamarano da crociera 40–45 piedi', 1.05, 0.85, 1.22, 52)
];

/** Velocità della barca con interpolazione bilineare; 0 nella zona morta prua al vento. */
export function boatSpeed(p: Polar, twa: number, tws: number): number {
	twa = Math.min(180, Math.abs(twa));
	if (tws <= 0) return 0;
	// Sotto il primo angolo della tabella la barca non risale: si annulla fino a 2/3 di quell'angolo.
	const a0 = p.twa[0];
	if (twa < a0) {
		const dead = a0 * 0.75;
		if (twa <= dead) return 0;
		return boatSpeed(p, a0, tws) * ((twa - dead) / (a0 - dead));
	}
	const idx = (arr: number[], v: number) => {
		if (v <= arr[0]) return [0, 0, 0] as const;
		if (v >= arr[arr.length - 1]) return [arr.length - 1, arr.length - 1, 0] as const;
		let i = 0;
		while (arr[i + 1] < v) i++;
		return [i, i + 1, (v - arr[i]) / (arr[i + 1] - arr[i])] as const;
	};
	const [r0, r1, fr] = idx(p.twa, twa);
	// Sotto il primo vento della tabella si scala in proporzione verso zero.
	const scale = tws < p.tws[0] ? tws / p.tws[0] : 1;
	const [c0, c1, fc] = idx(p.tws, Math.max(tws, p.tws[0]));
	const v = (r: number, c: number) => p.speeds[r]?.[c] ?? 0;
	const top = v(r0, c0) * (1 - fc) + v(r0, c1) * fc;
	const bot = v(r1, c0) * (1 - fc) + v(r1, c1) * fc;
	return (top * (1 - fr) + bot * fr) * scale;
}

/**
 * Legge un file polare in forma di tabella: prima riga con le intensità del vento,
 * righe successive "angolo velocità velocità …". Separatori: tabulazione, punto e virgola, virgola o spazi.
 */
export function parsePolar(text: string, name: string): Polar {
	const rows = text
		.split(/\r?\n/)
		.map((l) => l.trim())
		.filter((l) => l && !l.startsWith('#'))
		.map((l) => l.split(/[\t;,]+|\s+/).filter(Boolean));
	if (rows.length < 3) throw new Error('File polare troppo corto.');
	const num = (s: string) => Number(s.replace(',', '.'));
	const header = rows[0].slice(1).map(num);
	if (!header.length || header.some((x) => !Number.isFinite(x))) throw new Error('Prima riga non valida: servono le intensità del vento (TWS).');
	const twa: number[] = [];
	const speeds: number[][] = [];
	for (const r of rows.slice(1)) {
		const a = num(r[0]);
		const vals = r.slice(1, header.length + 1).map(num);
		if (!Number.isFinite(a) || vals.some((x) => !Number.isFinite(x))) continue;
		if (a === 0) continue; // riga a 0° (tutti zero) non utile
		twa.push(a);
		speeds.push(vals.concat(Array(header.length - vals.length).fill(0)));
	}
	if (twa.length < 3) throw new Error('Servono almeno 3 righe di angoli con le velocità.');
	const order = twa.map((_, i) => i).sort((a, b) => twa[a] - twa[b]);
	return {
		id: `custom-${name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${Date.now().toString(36)}`,
		name,
		tws: header,
		twa: order.map((i) => twa[i]),
		speeds: order.map((i) => speeds[i]),
		custom: true
	};
}
