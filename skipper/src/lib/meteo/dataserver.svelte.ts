/**
 * Server dei dati meteo: Open-Meteo pubblico oppure un server Open-Meteo proprio (es. il PC di casa).
 * Con un server proprio le richieste vanno prima lì; se non risponde in tempo si ripiega sul pubblico.
 */
export const PUBLIC_FORECAST = 'https://api.open-meteo.com';
export const PUBLIC_MARINE = 'https://marine-api.open-meteo.com';

const KEY = 'skipper:server';

export interface ServerConfig {
	/** Indirizzo del server proprio, es. https://meteo.miodominio.it — vuoto = solo Open-Meteo pubblico */
	url: string;
	/** Secondi di attesa massima prima di ripiegare sul server pubblico */
	timeout: number;
}

function load(): ServerConfig {
	try {
		const v = JSON.parse(localStorage.getItem(KEY) ?? 'null');
		if (v && typeof v.url === 'string') return { url: v.url, timeout: Number(v.timeout) || 30 };
	} catch {
		/* storage non disponibile */
	}
	return { url: '', timeout: 30 };
}

export const server = $state<ServerConfig>(typeof localStorage === 'undefined' ? { url: '', timeout: 30 } : load());

export function saveServer(c: ServerConfig) {
	server.url = normalize(c.url);
	server.timeout = Math.min(300, Math.max(5, Math.round(c.timeout) || 30));
	try {
		localStorage.setItem(KEY, JSON.stringify(server));
	} catch {
		/* storage non disponibile */
	}
}

export const normalize = (u: string) => {
	const t = u.trim().replace(/\/+$/, '');
	if (!t) return '';
	return /^https?:\/\//i.test(t) ? t : `http://${t}`;
};

export type Source = 'proprio' | 'pubblico';

/** Ultima richiesta meteo: da dove è arrivata e quanto ha impiegato (per l'indicatore nell'app). */
export const lastFetch = $state<{ source: Source | null; ms: number; fallback: boolean; error: string | null }>({
	source: null,
	ms: 0,
	fallback: false,
	error: null
});

/** Se l'URL è una richiesta a Open-Meteo pubblico (previsioni o mare), lo riscrive verso il server proprio. */
export function toOwn(url: string): string | null {
	if (!server.url) return null;
	for (const base of [PUBLIC_FORECAST, PUBLIC_MARINE]) if (url.startsWith(base)) return server.url + url.slice(base.length);
	return null;
}
