/** Moduli della Skipper WebApp, raggiungibili dal menu nel logo. */
export interface ModuleInfo {
	id: string;
	path: '/' | '/rotta' | '/checkin' | '/checkout' | '/guasti' | '/contatti' | '/emergenze' | '/logbook';
	label: string;
	icon: string;
	desc: string;
}

export const MODULES: ModuleInfo[] = [
	{ id: 'meteo', path: '/', label: 'Meteo', icon: '🌬️', desc: 'Valutazione multi-modello e sinottica' },
	{ id: 'rotta', path: '/rotta', label: 'Rotta', icon: '🧭', desc: 'Weather routing con le polari' },
	{ id: 'checkin', path: '/checkin', label: 'Check-in', icon: '📋', desc: 'Presa in consegna della barca' },
	{ id: 'checkout', path: '/checkout', label: 'Check-out', icon: '✅', desc: 'Riconsegna della barca' },
	{ id: 'guasti', path: '/guasti', label: 'Guasti', icon: '🔧', desc: 'Segnalazioni e stato delle riparazioni' },
	{ id: 'logbook', path: '/logbook', label: 'Log book', icon: '📓', desc: 'Giornale di bordo' },
	{ id: 'contatti', path: '/contatti', label: 'Contatti', icon: '📞', desc: 'Marina, tecnici, equipaggio, soccorso' },
	{ id: 'emergenze', path: '/emergenze', label: 'Emergenze', icon: '🆘', desc: 'MAYDAY, uomo a mare, incendio, falla' }
];

export const APP_VERSION: string = typeof __APP_VERSION__ === 'string' ? __APP_VERSION__ : 'dev';
