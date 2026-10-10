/** Versione dimostrativa pubblica: solo alcune parti sono attive, il resto è visibile ma bloccato. */
export const DEMO: boolean = typeof __DEMO__ === 'boolean' ? __DEMO__ : false;

/** Moduli utilizzabili nella demo. */
export const DEMO_MODULES = ['meteo', 'sinottica', 'checkin'];
