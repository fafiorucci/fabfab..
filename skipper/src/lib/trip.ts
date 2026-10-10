import { MAIN_MODELS, modelById } from './meteo/models';

export interface Limits {
	/** Vento medio massimo accettabile (nodi) */
	wind: number;
	/** Raffica massima accettabile (nodi) */
	gust: number;
	/** Onda significativa massima (metri) */
	wave: number;
}

export interface Trip {
	name: string;
	place: string;
	lat: number;
	lon: number;
	/** Data di uscita, YYYY-MM-DD (ora locale della zona) */
	date: string;
	days: number;
	/** Semi-ampiezza dell'area in gradi attorno al porto */
	radius: number;
	limits: Limits;
	models: string[];
}

export const MAX_DAYS = 7;
/** Orizzonte massimo dei modelli (Open-Meteo arriva a 16 giorni) */
export const MAX_LEAD_DAYS = 14;

export function isoDate(d: Date): string {
	const y = d.getFullYear();
	const m = String(d.getMonth() + 1).padStart(2, '0');
	const day = String(d.getDate()).padStart(2, '0');
	return `${y}-${m}-${day}`;
}

export function addDays(date: string, n: number): string {
	const [y, m, d] = date.split('-').map(Number);
	return isoDate(new Date(y, m - 1, d + n));
}

export function defaultTrip(): Trip {
	return {
		name: 'Uscita',
		place: 'Fiumicino, Lazio',
		lat: 41.771,
		lon: 12.217,
		date: addDays(isoDate(new Date()), 1),
		days: 2,
		radius: 1,
		limits: { wind: 20, gust: 28, wave: 1.5 },
		models: [...MAIN_MODELS]
	};
}

/** Controlla che i campi abbiano senso; restituisce un messaggio d'errore o null. */
export function validateTrip(t: Trip, today = isoDate(new Date())): string | null {
	if (!t.place.trim()) return 'Indica il porto o la zona di partenza.';
	if (!(t.lat >= 28 && t.lat <= 48 && t.lon >= -8 && t.lon <= 38)) return 'Per ora la zona deve essere nel Mediterraneo.';
	if (t.date < today) return 'La data di uscita è già passata.';
	if (t.date > addDays(today, MAX_LEAD_DAYS)) return `I modelli arrivano a ${MAX_LEAD_DAYS} giorni: scegli una data più vicina.`;
	if (!(t.days >= 1 && t.days <= MAX_DAYS)) return `La durata deve essere tra 1 e ${MAX_DAYS} giorni.`;
	if (!t.models.length) return 'Seleziona almeno un modello.';
	return null;
}

// ----- Link di invito: l'intera uscita viaggia nell'URL -----

function toBase64Url(s: string): string {
	const bytes = new TextEncoder().encode(s);
	let bin = '';
	bytes.forEach((b) => (bin += String.fromCharCode(b)));
	return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function fromBase64Url(s: string): string {
	const b64 = s.replace(/-/g, '+').replace(/_/g, '/');
	const bin = atob(b64 + '='.repeat((4 - (b64.length % 4)) % 4));
	return new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0)));
}

export function encodeTrip(t: Trip): string {
	return toBase64Url(JSON.stringify(t));
}

export function decodeTrip(s: string): Trip | null {
	try {
		const raw = JSON.parse(fromBase64Url(s));
		const base = defaultTrip();
		const t: Trip = {
			...base,
			...raw,
			limits: { ...base.limits, ...(raw.limits ?? {}) },
			models: Array.isArray(raw.models) ? raw.models.filter((m: unknown) => typeof m === 'string' && modelById(m)) : base.models
		};
		if (typeof t.lat !== 'number' || typeof t.lon !== 'number' || typeof t.date !== 'string') return null;
		return t;
	} catch {
		return null;
	}
}

export function inviteUrl(t: Trip, base: string): string {
	const u = new URL(base);
	u.search = '';
	u.hash = '';
	u.searchParams.set('u', encodeTrip(t));
	return u.toString();
}

const STORE_KEY = 'skipper-meteo:trip';

export function loadSavedTrip(): Trip | null {
	try {
		const s = localStorage.getItem(STORE_KEY);
		return s ? decodeTrip(s) : null;
	} catch {
		return null;
	}
}

export function saveTrip(t: Trip) {
	try {
		localStorage.setItem(STORE_KEY, encodeTrip(t));
	} catch {
		/* storage non disponibile */
	}
}
