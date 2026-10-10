/**
 * Piante schematiche degli interni, disegnate per Skipper WebApp (non riproducono piante di cantiere).
 * Sistema di coordinate: viewBox 1000 × 400, prua a sinistra, poppa (pozzetto) a destra.
 */
export interface Room {
	label: string;
	x: number;
	y: number;
	w: number;
	h: number;
	kind?: 'cabin' | 'head' | 'saloon' | 'galley' | 'nav' | 'cockpit' | 'locker' | 'engine';
}

export interface BoatLayout {
	id: string;
	name: string;
	/** Profilo dello scafo (path SVG) */
	hull: string;
	rooms: Room[];
}

/** Scafo di monoscafo: prua a punta a sinistra, specchio di poppa a destra. */
const MONO = 'M 40 200 C 120 90, 300 40, 520 36 L 960 44 L 960 356 L 520 364 C 300 360, 120 310, 40 200 Z';
/** Due scafi di catamarano uniti dalla tuga. */
const CAT = 'M 40 92 C 120 40, 300 26, 520 24 L 960 28 L 960 156 L 520 160 C 300 158, 120 146, 40 92 Z M 40 308 C 120 254, 300 240, 520 240 L 960 244 L 960 372 L 520 376 C 300 374, 120 362, 40 308 Z';

export const LAYOUTS: BoatLayout[] = [
	{
		id: 'mono-2c-1b',
		name: 'Monoscafo 30–36 piedi · 2 cabine, 1 bagno',
		hull: MONO,
		rooms: [
			{ label: 'Gavone di prua', x: 70, y: 160, w: 80, h: 80, kind: 'locker' },
			{ label: 'Cabina di prua', x: 155, y: 95, w: 175, h: 210, kind: 'cabin' },
			{ label: 'Bagno', x: 335, y: 60, w: 110, h: 110, kind: 'head' },
			{ label: 'Dinette', x: 335, y: 175, w: 250, h: 165, kind: 'saloon' },
			{ label: 'Cucina', x: 450, y: 60, w: 135, h: 110, kind: 'galley' },
			{ label: 'Carteggio', x: 590, y: 255, w: 110, h: 90, kind: 'nav' },
			{ label: 'Motore (sotto scala)', x: 590, y: 160, w: 110, h: 90, kind: 'engine' },
			{ label: 'Cabina di poppa', x: 590, y: 55, w: 160, h: 100, kind: 'cabin' },
			{ label: 'Gavone di poppa', x: 705, y: 255, w: 90, h: 90, kind: 'locker' },
			{ label: 'Pozzetto', x: 760, y: 60, w: 190, h: 280, kind: 'cockpit' }
		]
	},
	{
		id: 'mono-3c-1b',
		name: 'Monoscafo 36–40 piedi · 3 cabine, 1 bagno',
		hull: MONO,
		rooms: [
			{ label: 'Gavone di prua', x: 70, y: 160, w: 80, h: 80, kind: 'locker' },
			{ label: 'Cabina di prua', x: 155, y: 95, w: 175, h: 210, kind: 'cabin' },
			{ label: 'Bagno', x: 335, y: 255, w: 110, h: 95, kind: 'head' },
			{ label: 'Dinette', x: 335, y: 55, w: 250, h: 195, kind: 'saloon' },
			{ label: 'Cucina', x: 450, y: 255, w: 135, h: 95, kind: 'galley' },
			{ label: 'Carteggio', x: 590, y: 255, w: 90, h: 95, kind: 'nav' },
			{ label: 'Motore (sotto scala)', x: 590, y: 160, w: 90, h: 90, kind: 'engine' },
			{ label: 'Cabina di poppa sx', x: 590, y: 50, w: 170, h: 105, kind: 'cabin' },
			{ label: 'Cabina di poppa dx', x: 685, y: 250, w: 170, h: 100, kind: 'cabin' },
			{ label: 'Pozzetto', x: 765, y: 50, w: 185, h: 195, kind: 'cockpit' }
		]
	},
	{
		id: 'mono-3c-2b',
		name: 'Monoscafo 40–45 piedi · 3 cabine, 2 bagni',
		hull: MONO,
		rooms: [
			{ label: 'Gavone di prua', x: 70, y: 160, w: 80, h: 80, kind: 'locker' },
			{ label: 'Cabina armatoriale', x: 155, y: 90, w: 165, h: 220, kind: 'cabin' },
			{ label: 'Bagno di prua', x: 325, y: 50, w: 100, h: 110, kind: 'head' },
			{ label: 'Dinette', x: 325, y: 165, w: 270, h: 185, kind: 'saloon' },
			{ label: 'Cucina', x: 430, y: 50, w: 165, h: 110, kind: 'galley' },
			{ label: 'Bagno di poppa', x: 600, y: 50, w: 90, h: 100, kind: 'head' },
			{ label: 'Motore (sotto scala)', x: 600, y: 155, w: 90, h: 95, kind: 'engine' },
			{ label: 'Carteggio', x: 600, y: 255, w: 90, h: 95, kind: 'nav' },
			{ label: 'Cabina di poppa sx', x: 695, y: 48, w: 150, h: 120, kind: 'cabin' },
			{ label: 'Cabina di poppa dx', x: 695, y: 232, w: 150, h: 120, kind: 'cabin' },
			{ label: 'Pozzetto', x: 850, y: 48, w: 100, h: 304, kind: 'cockpit' }
		]
	},
	{
		id: 'mono-4c-2b',
		name: 'Monoscafo 45–50 piedi · 4 cabine, 2 bagni',
		hull: MONO,
		rooms: [
			{ label: 'Gavone di prua', x: 70, y: 165, w: 70, h: 70, kind: 'locker' },
			{ label: 'Cabina prua sx', x: 145, y: 95, w: 150, h: 102, kind: 'cabin' },
			{ label: 'Cabina prua dx', x: 145, y: 203, w: 150, h: 102, kind: 'cabin' },
			{ label: 'Bagno di prua', x: 300, y: 50, w: 100, h: 110, kind: 'head' },
			{ label: 'Dinette', x: 300, y: 165, w: 290, h: 185, kind: 'saloon' },
			{ label: 'Cucina', x: 405, y: 50, w: 185, h: 110, kind: 'galley' },
			{ label: 'Bagno di poppa', x: 595, y: 50, w: 90, h: 100, kind: 'head' },
			{ label: 'Motore (sotto scala)', x: 595, y: 155, w: 90, h: 95, kind: 'engine' },
			{ label: 'Carteggio', x: 595, y: 255, w: 90, h: 95, kind: 'nav' },
			{ label: 'Cabina di poppa sx', x: 690, y: 48, w: 150, h: 120, kind: 'cabin' },
			{ label: 'Cabina di poppa dx', x: 690, y: 232, w: 150, h: 120, kind: 'cabin' },
			{ label: 'Pozzetto', x: 845, y: 48, w: 105, h: 304, kind: 'cockpit' }
		]
	},
	{
		id: 'cat-4c-4b',
		name: 'Catamarano 40–45 piedi · 4 cabine, 4 bagni',
		hull: CAT,
		rooms: [
			{ label: 'Gavone prua sx', x: 80, y: 65, w: 70, h: 55, kind: 'locker' },
			{ label: 'Cabina prua sx', x: 155, y: 45, w: 170, h: 100, kind: 'cabin' },
			{ label: 'Bagno prua sx', x: 330, y: 40, w: 100, h: 105, kind: 'head' },
			{ label: 'Bagno poppa sx', x: 640, y: 35, w: 100, h: 110, kind: 'head' },
			{ label: 'Cabina poppa sx', x: 745, y: 35, w: 200, h: 110, kind: 'cabin' },
			{ label: 'Motore sx (gavone)', x: 870, y: 150, w: 75, h: 40, kind: 'engine' },
			{ label: 'Gavone prua dx', x: 80, y: 280, w: 70, h: 55, kind: 'locker' },
			{ label: 'Cabina prua dx', x: 155, y: 255, w: 170, h: 100, kind: 'cabin' },
			{ label: 'Bagno prua dx', x: 330, y: 255, w: 100, h: 105, kind: 'head' },
			{ label: 'Bagno poppa dx', x: 640, y: 255, w: 100, h: 110, kind: 'head' },
			{ label: 'Cabina poppa dx', x: 745, y: 255, w: 200, h: 110, kind: 'cabin' },
			{ label: 'Motore dx (gavone)', x: 870, y: 210, w: 75, h: 40, kind: 'engine' },
			{ label: 'Dinette e cucina (tuga)', x: 435, y: 150, w: 240, h: 100, kind: 'saloon' },
			{ label: 'Carteggio', x: 435, y: 105, w: 110, h: 42, kind: 'nav' },
			{ label: 'Pozzetto', x: 680, y: 150, w: 185, h: 100, kind: 'cockpit' }
		]
	}
];

export const layoutById = (id: string) => LAYOUTS.find((l) => l.id === id);

export interface PlanItem {
	id: string;
	label: string;
	icon: string;
	group: 'sicurezza' | 'energia' | 'acqua' | 'motore' | 'bordo';
}

/** Elementi da localizzare: quello che serve trovare al volo in navigazione. */
export const PLAN_ITEMS: PlanItem[] = [
	{ id: 'giubbotti', label: 'Giubbotti salvagente', icon: '🦺', group: 'sicurezza' },
	{ id: 'cinture', label: 'Cinture di sicurezza / jackline', icon: '🪢', group: 'sicurezza' },
	{ id: 'estintore', label: 'Estintore', icon: '🧯', group: 'sicurezza' },
	{ id: 'soccorso', label: 'Cassetta pronto soccorso', icon: '⛑️', group: 'sicurezza' },
	{ id: 'razzi', label: 'Razzi, fuochi a mano e fumogeni', icon: '🎆', group: 'sicurezza' },
	{ id: 'epirb', label: 'EPIRB', icon: '📡', group: 'sicurezza' },
	{ id: 'zattera', label: 'Zattera di salvataggio', icon: '🛟', group: 'sicurezza' },
	{ id: 'tappi', label: 'Tappi conici (falle)', icon: '🔺', group: 'sicurezza' },
	{ id: 'torcia', label: 'Torcia e proiettore', icon: '🔦', group: 'sicurezza' },
	{ id: 'staccabatterie', label: 'Staccabatterie / switch generale', icon: '🔌', group: 'energia' },
	{ id: 'batterie', label: 'Batterie', icon: '🔋', group: 'energia' },
	{ id: 'quadro', label: 'Quadro elettrico', icon: '🎛️', group: 'energia' },
	{ id: 'salpancora-mt', label: 'Magnetotermico salpancora', icon: '⚓', group: 'energia' },
	{ id: 'gas', label: 'Rubinetto / bombola del gas', icon: '🔥', group: 'energia' },
	{ id: 'serbatoio-acqua', label: 'Serbatoio acqua', icon: '💧', group: 'acqua' },
	{ id: 'scambio', label: 'Scambio serbatoi acqua', icon: '🔀', group: 'acqua' },
	{ id: 'autoclave', label: 'Autoclave', icon: '🚰', group: 'acqua' },
	{ id: 'presa-wc', label: 'Prese a mare / chiusure bagni', icon: '🚽', group: 'acqua' },
	{ id: 'acque-nere', label: 'Serbatoio acque nere e valvola', icon: '🛢️', group: 'acqua' },
	{ id: 'pompa-sentina', label: 'Pompa di sentina (manuale/elettrica)', icon: '🪣', group: 'acqua' },
	{ id: 'serbatoio-gasolio', label: 'Serbatoio gasolio', icon: '⛽', group: 'motore' },
	{ id: 'taglia-nafta', label: 'Taglia-nafta', icon: '⛔', group: 'motore' },
	{ id: 'presa-motore', label: 'Presa a mare motore / filtro acqua', icon: '🌊', group: 'motore' },
	{ id: 'decantatore', label: 'Prefiltro decantatore', icon: '🧪', group: 'motore' },
	{ id: 'attrezzi', label: 'Cassetta attrezzi e ricambi', icon: '🧰', group: 'bordo' },
	{ id: 'timone-rispetto', label: 'Barra di emergenza', icon: '🛞', group: 'bordo' },
	{ id: 'vhf', label: 'VHF', icon: '📻', group: 'bordo' },
	{ id: 'documenti', label: 'Documenti di bordo', icon: '📁', group: 'bordo' }
];

export const GROUP_LABEL: Record<PlanItem['group'], string> = {
	sicurezza: 'Sicurezza',
	energia: 'Energia e gas',
	acqua: 'Acqua e scarichi',
	motore: 'Motore e carburante',
	bordo: 'Bordo'
};

export const itemById = (id: string) => PLAN_ITEMS.find((i) => i.id === id);
