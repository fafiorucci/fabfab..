export type LayerId = 'wind' | 'gust' | 'wave' | 'pressure' | 'precip' | 'spread';

type Stop = [number, [number, number, number]];

export interface LayerInfo {
	id: LayerId;
	label: string;
	unit: string;
	decimals: number;
	stops: Stop[];
	/** Valori sotto questa soglia sono trasparenti */
	transparentBelow?: number;
}

const WIND: Stop[] = [
	[0, [98, 113, 183]],
	[5, [57, 153, 196]],
	[10, [76, 177, 107]],
	[15, [190, 196, 62]],
	[20, [232, 158, 52]],
	[25, [214, 80, 54]],
	[30, [178, 41, 98]],
	[40, [120, 38, 150]],
	[55, [60, 20, 80]]
];

export const LAYERS: Record<LayerId, LayerInfo> = {
	wind: { id: 'wind', label: 'Vento', unit: 'kn', decimals: 0, stops: WIND },
	gust: { id: 'gust', label: 'Raffiche', unit: 'kn', decimals: 0, stops: WIND },
	wave: {
		id: 'wave',
		label: 'Onda',
		unit: 'm',
		decimals: 1,
		stops: [
			[0, [70, 110, 190]],
			[0.5, [50, 160, 200]],
			[1, [80, 185, 120]],
			[1.5, [210, 200, 70]],
			[2.5, [230, 140, 50]],
			[4, [200, 50, 60]],
			[6, [120, 30, 120]]
		]
	},
	pressure: {
		id: 'pressure',
		label: 'Pressione',
		unit: 'hPa',
		decimals: 0,
		stops: [
			[985, [120, 40, 140]],
			[995, [60, 90, 190]],
			[1005, [70, 160, 200]],
			[1013, [140, 200, 140]],
			[1020, [230, 200, 90]],
			[1030, [220, 110, 60]]
		]
	},
	precip: {
		id: 'precip',
		label: 'Pioggia',
		unit: 'mm/h',
		decimals: 1,
		transparentBelow: 0.1,
		stops: [
			[0.1, [120, 190, 230]],
			[1, [60, 130, 220]],
			[3, [40, 80, 200]],
			[6, [150, 60, 200]],
			[12, [220, 50, 120]]
		]
	},
	spread: {
		id: 'spread',
		label: 'Disaccordo modelli',
		unit: 'kn',
		decimals: 1,
		stops: [
			[0, [60, 170, 110]],
			[2, [150, 200, 90]],
			[4, [235, 200, 60]],
			[6, [235, 130, 50]],
			[9, [210, 50, 60]],
			[13, [130, 30, 110]]
		]
	}
};

export function colorAt(info: LayerInfo, v: number): [number, number, number, number] {
	if (Number.isNaN(v) || (info.transparentBelow !== undefined && v < info.transparentBelow)) return [0, 0, 0, 0];
	const s = info.stops;
	if (v <= s[0][0]) return [...s[0][1], 255];
	for (let i = 1; i < s.length; i++) {
		if (v <= s[i][0]) {
			const [a, ca] = s[i - 1];
			const [b, cb] = s[i];
			const k = (v - a) / (b - a);
			return [ca[0] + (cb[0] - ca[0]) * k, ca[1] + (cb[1] - ca[1]) * k, ca[2] + (cb[2] - ca[2]) * k, 255];
		}
	}
	return [...s[s.length - 1][1], 255];
}

export function cssGradient(info: LayerInfo): string {
	const s = info.stops;
	const lo = s[0][0];
	const hi = s[s.length - 1][0];
	return `linear-gradient(90deg, ${s.map(([v, c]) => `rgb(${c.join(',')}) ${(((v - lo) / (hi - lo)) * 100).toFixed(1)}%`).join(', ')})`;
}
