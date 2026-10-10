export interface ModelInfo {
	id: string;
	label: string;
	source: string;
	/** Risoluzione indicativa in km */
	km: number;
	/** Giorni di previsione disponibili (indicativi) */
	days: number;
	color: string;
	group: 'global' | 'regional';
	/** Tra i modelli selezionati di default */
	main?: boolean;
}

/**
 * Modelli atmosferici di Open-Meteo che coprono il Mediterraneo (identificativi verificati sull'API).
 * Esclusi perché senza dati in zona: GraphCast, BOM ACCESS, KMA, ICON-D2, MeteoSwiss.
 */
export const MODELS: ModelInfo[] = [
	// Globali
	{ id: 'ecmwf_ifs025', label: 'ECMWF IFS', source: 'ECMWF', km: 25, days: 15, color: '#2f80ed', group: 'global', main: true },
	{ id: 'ecmwf_ifs', label: 'ECMWF IFS 9 km', source: 'ECMWF', km: 9, days: 15, color: '#1b4f9c', group: 'global' },
	{ id: 'ecmwf_aifs025_single', label: 'ECMWF AIFS (IA)', source: 'ECMWF', km: 25, days: 15, color: '#56ccf2', group: 'global' },
	{ id: 'gfs_seamless', label: 'GFS', source: 'NOAA', km: 13, days: 16, color: '#eb5757', group: 'global', main: true },
	{ id: 'icon_seamless', label: 'ICON', source: 'DWD', km: 7, days: 7, color: '#27ae60', group: 'global', main: true },
	{ id: 'ukmo_seamless', label: 'UKMO', source: 'Met Office', km: 10, days: 7, color: '#f2994a', group: 'global', main: true },
	{ id: 'gem_seamless', label: 'GEM', source: 'Env. Canada', km: 15, days: 10, color: '#bb6bd9', group: 'global' },
	{ id: 'jma_seamless', label: 'JMA', source: 'JMA Giappone', km: 55, days: 11, color: '#828282', group: 'global' },
	{ id: 'cma_grapes_global', label: 'CMA GRAPES', source: 'CMA Cina', km: 15, days: 10, color: '#a0522d', group: 'global' },
	// Europei e locali ad alta risoluzione
	{ id: 'meteofrance_seamless', label: 'ARPEGE/AROME', source: 'Météo-France', km: 2, days: 4, color: '#9b51e0', group: 'regional', main: true },
	{ id: 'meteofrance_arpege_europe', label: 'ARPEGE Europa', source: 'Météo-France', km: 10, days: 4, color: '#7b3fb0', group: 'regional' },
	{ id: 'meteofrance_arome_france', label: 'AROME', source: 'Météo-France', km: 2.5, days: 2, color: '#c58af9', group: 'regional' },
	{ id: 'meteofrance_arome_france_hd', label: 'AROME HD', source: 'Météo-France', km: 1.5, days: 2, color: '#e0b3ff', group: 'regional' },
	{ id: 'icon_eu', label: 'ICON-EU', source: 'DWD', km: 7, days: 5, color: '#6fcf97', group: 'regional' },
	{ id: 'italia_meteo_arpae_icon_2i', label: 'ICON-2I', source: 'ItaliaMeteo-ARPAE', km: 2, days: 3, color: '#00a3a3', group: 'regional', main: true },
	{ id: 'dmi_harmonie_arome_europe', label: 'HARMONIE DMI', source: 'DMI Danimarca', km: 2, days: 2, color: '#d4a017', group: 'regional' },
	{ id: 'knmi_harmonie_arome_europe', label: 'HARMONIE KNMI', source: 'KNMI Olanda', km: 5.5, days: 2, color: '#e07b39', group: 'regional' }
];

export const MAIN_MODELS = MODELS.filter((m) => m.main).map((m) => m.id);

export const modelById = (id: string) => MODELS.find((m) => m.id === id);

/** Stima delle chiamate Open-Meteo per una zona nuova: vento (3 variabili) di ogni modello + onda. */
export function callsPerView(models: number, points = 64): number {
	return Math.round(points * Math.max(1, (3 * models) / 10) + points);
}
