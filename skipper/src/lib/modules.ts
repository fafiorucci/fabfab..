/** Moduli della Skipper WebApp, raggiungibili dal menu nel logo. */
export interface ModuleInfo {
	id: string;
	path: '/' | '/sinottica' | '/rotta' | '/briefing' | '/wobble' | '/memo' | '/safety' | '/checkin' | '/checkout' | '/guasti' | '/contatti' | '/emergenze' | '/logbook' | '/impostazioni' | '/navigazione';
	label: string;
	icon: string;
	desc: string;
}

export const MODULES: ModuleInfo[] = [
	{ id: 'meteo', path: '/', label: 'Meteo', icon: '🌬️', desc: 'Valutazione multi-modello e sinottica' },
	{ id: 'sinottica', path: '/sinottica', label: 'Carte sinottiche', icon: '🗺️', desc: 'Isobare dei modelli a confronto, carte ufficiali' },
	{ id: 'navigazione', path: '/navigazione', label: 'Navigazione', icon: '📡', desc: 'Posizione GPS, traccia e rotta in tempo reale' },
	{ id: 'rotta', path: '/rotta', label: 'Rotta', icon: '🧭', desc: 'Weather routing con le polari' },
	{ id: 'checkin', path: '/checkin', label: 'Check-in', icon: '📋', desc: 'Presa in consegna della barca' },
	{ id: 'safety', path: '/safety', label: 'Safety plan', icon: '📍', desc: 'Dove si trovano dotazioni e comandi a bordo' },
	{ id: 'briefing', path: '/briefing', label: 'Briefing equipaggio', icon: '🗣️', desc: 'Vita di bordo e sicurezza' },
	{ id: 'wobble', path: '/wobble', label: 'Controlli WOBBLE', icon: '⚙️', desc: 'Controlli giornalieri del motore' },
	{ id: 'checkout', path: '/checkout', label: 'Check-out', icon: '✅', desc: 'Riconsegna della barca' },
	{ id: 'guasti', path: '/guasti', label: 'Guasti', icon: '🔧', desc: 'Segnalazioni e stato delle riparazioni' },
	{ id: 'logbook', path: '/logbook', label: 'Log book', icon: '📓', desc: 'Giornale di bordo' },
	{ id: 'contatti', path: '/contatti', label: 'Contatti', icon: '📞', desc: 'Marina, tecnici, equipaggio, soccorso' },
	{ id: 'memo', path: '/memo', label: 'Skipper memo', icon: '📘', desc: 'COLREG, IALA, MARPOL, bandiere, scale' },
	{ id: 'emergenze', path: '/emergenze', label: 'Emergenze', icon: '🆘', desc: 'MAYDAY, uomo a mare, incendio, falla' },
	{ id: 'impostazioni', path: '/impostazioni', label: 'Impostazioni', icon: '🛠️', desc: 'Server dei dati meteo e confronto dei tempi' }
];

export const APP_VERSION: string = typeof __APP_VERSION__ === 'string' ? __APP_VERSION__ : 'dev';
