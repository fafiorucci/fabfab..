export interface ModelInfo {
	id: string;
	label: string;
	source: string;
	/** Risoluzione indicativa in km */
	km: number;
	/** Giorni di previsione disponibili */
	days: number;
	color: string;
}

/** Modelli atmosferici richiesti a Open-Meteo (parametro `models`). */
export const MODELS: ModelInfo[] = [
	{ id: 'ecmwf_ifs025', label: 'ECMWF IFS', source: 'ECMWF', km: 25, days: 15, color: '#2f80ed' },
	{ id: 'icon_seamless', label: 'ICON', source: 'DWD', km: 7, days: 7, color: '#27ae60' },
	{ id: 'gfs_seamless', label: 'GFS', source: 'NOAA', km: 13, days: 16, color: '#eb5757' },
	{ id: 'meteofrance_seamless', label: 'ARPEGE/AROME', source: 'Météo-France', km: 2, days: 4, color: '#9b51e0' },
	{ id: 'ukmo_seamless', label: 'UKMO', source: 'Met Office', km: 10, days: 7, color: '#f2994a' },
	{ id: 'italia_meteo_arpae_icon_2i', label: 'ICON-2I', source: 'ItaliaMeteo-ARPAE', km: 2, days: 3, color: '#00a3a3' }
];

export const modelById = (id: string) => MODELS.find((m) => m.id === id);
