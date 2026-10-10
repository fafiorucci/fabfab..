const CARDINALS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO'];
const WINDS = ['Tramontana', 'Grecale', 'Levante', 'Scirocco', 'Ostro', 'Libeccio', 'Ponente', 'Maestrale'];

export const num = (x: number, d = 0) => (Number.isFinite(x) ? x.toFixed(d).replace('.', ',') : '—');

/** Punto cardinale (16 settori) di una direzione in gradi. */
export function cardinal(deg: number): string {
	return Number.isFinite(deg) ? CARDINALS[Math.round((((deg % 360) + 360) % 360) / 22.5) % 16] : '—';
}

/** Nome del vento della rosa dei venti per la direzione di provenienza. */
export function windName(deg: number): string {
	return Number.isFinite(deg) ? WINDS[Math.round((((deg % 360) + 360) % 360) / 45) % 8] : '';
}

/** Freccia che punta dove va il vento (o l'onda), data la direzione di provenienza. */
export function arrow(deg: number): string {
	if (!Number.isFinite(deg)) return '';
	const to = (deg + 180) % 360;
	return `<span class="dir-arrow" style="display:inline-block;transform:rotate(${to.toFixed(0)}deg)">↑</span>`;
}

/** Coordinate in gradi e primi decimali, come si leggono alla radio: 42° 48,61' N. */
export function toDM(value: number, pos: string, neg: string, degDigits: number): string {
	const hemi = value >= 0 ? pos : neg;
	const a = Math.abs(value);
	let d = Math.floor(a);
	let m = (a - d) * 60;
	if (m >= 59.995) {
		d += 1;
		m = 0;
	}
	return `${String(d).padStart(degDigits, '0')}° ${m.toFixed(2).replace('.', ',').padStart(5, '0')}' ${hemi}`;
}

export const latDM = (lat: number) => toDM(lat, 'N', 'S', 2);
export const lonDM = (lon: number) => toDM(lon, 'E', 'W', 3);
