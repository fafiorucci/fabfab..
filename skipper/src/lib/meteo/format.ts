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
