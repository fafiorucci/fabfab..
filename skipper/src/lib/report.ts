import { LEVEL_LABEL, type DayVerdict } from './meteo/assess';
import { dayLabel } from './meteo/grid';
import { modelById } from './meteo/models';
import type { Trip } from './trip';
import { BRAND } from './brand';

const LEVEL_COLOR = { go: '#2e9d5b', caution: '#e0a020', nogo: '#d64545', nodata: '#8592a3' } as const;
const LEVEL_ICON = { go: '🟢', caution: '🟡', nogo: '🔴', nodata: '⚪' } as const;

const fmt = (x: number, d = 0) => (Number.isNaN(x) ? '—' : x.toFixed(d).replace('.', ','));

export function reportText(trip: Trip, verdicts: DayVerdict[], link: string): string {
	const lines = [
		`⛵ ${trip.name} — ${trip.place}`,
		`Limiti: vento ${trip.limits.wind} kn, raffiche ${trip.limits.gust} kn, onda ${fmt(trip.limits.wave, 1)} m`,
		''
	];
	for (const v of verdicts) {
		const maxWind = Math.max(...v.models.map((m) => m.wind));
		const maxGust = Math.max(...v.models.map((m) => m.gust));
		lines.push(
			`${LEVEL_ICON[v.level]} ${dayLabel(v.date)}: ${LEVEL_LABEL[v.level]}` +
				(v.models.length ? ` — vento fino a ${fmt(maxWind)} kn, raffiche ${fmt(maxGust)} kn, onda ${fmt(v.wave, 1)} m` : '')
		);
	}
	lines.push('', `Apri la valutazione: ${link}`, 'Strumento di supporto: verifica sempre il bollettino ufficiale.', `${BRAND.app} · ${BRAND.org} · a cura di ${BRAND.author}`);
	return lines.join('\n');
}

function loadImage(src: string): Promise<HTMLImageElement> {
	return new Promise((resolve, reject) => {
		const img = new Image();
		img.onload = () => resolve(img);
		img.onerror = reject;
		img.src = src;
	});
}

/** Report in formato immagine (PNG), pronto per WhatsApp, Mail o AirDrop. */
export async function reportImage(trip: Trip, verdicts: DayVerdict[], mapPng: string | null): Promise<Blob> {
	const W = 1080;
	const rowH = 132;
	const mapH = mapPng ? 600 : 0;
	const H = 220 + mapH + verdicts.length * rowH + 110;
	const c = document.createElement('canvas');
	c.width = W;
	c.height = H;
	const ctx = c.getContext('2d')!;
	const font = (size: number, weight = 400) => `${weight} ${size}px system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`;

	ctx.fillStyle = '#f4f7fa';
	ctx.fillRect(0, 0, W, H);
	ctx.fillStyle = '#0b1d2c';
	ctx.fillRect(0, 0, W, 180);
	ctx.fillStyle = '#ff7a1a';
	ctx.fillRect(0, 176, W, 4);
	ctx.fillStyle = '#ffffff';
	ctx.font = font(26, 600);
	ctx.fillText('SKIPPER METEO', 48, 56);
	ctx.textAlign = 'right';
	ctx.fillStyle = '#8fb4c8';
	ctx.font = font(22, 700);
	ctx.fillText(BRAND.org.toUpperCase(), W - 48, 56);
	ctx.textAlign = 'left';
	ctx.fillStyle = '#ffffff';
	ctx.font = font(44, 700);
	ctx.fillText(trip.name, 48, 112);
	ctx.font = font(26);
	ctx.fillStyle = '#b9cad8';
	ctx.fillText(`${trip.place} · limiti ${trip.limits.wind}/${trip.limits.gust} kn, ${fmt(trip.limits.wave, 1)} m`, 48, 152);

	let y = 210;
	if (mapPng) {
		try {
			const img = await loadImage(mapPng);
			const scale = Math.max(W / img.width, mapH / img.height);
			const sw = W / scale;
			const sh = mapH / scale;
			ctx.drawImage(img, (img.width - sw) / 2, (img.height - sh) / 2, sw, sh, 0, y - 10, W, mapH);
		} catch {
			/* mappa non disponibile */
		}
		y += mapH;
	}

	for (const v of verdicts) {
		ctx.fillStyle = '#ffffff';
		ctx.fillRect(32, y, W - 64, rowH - 16);
		ctx.fillStyle = LEVEL_COLOR[v.level];
		ctx.fillRect(32, y, 12, rowH - 16);
		ctx.fillStyle = '#0b1d2c';
		ctx.font = font(32, 700);
		ctx.fillText(dayLabel(v.date), 64, y + 44);
		ctx.fillStyle = LEVEL_COLOR[v.level];
		ctx.textAlign = 'right';
		ctx.fillText(LEVEL_LABEL[v.level], W - 56, y + 44);
		ctx.textAlign = 'left';
		ctx.fillStyle = '#44556a';
		ctx.font = font(23);
		const models = v.models.map((m) => `${modelById(m.model)?.label ?? m.model} ${fmt(m.wind)}/${fmt(m.gust)}`).join(' · ');
		ctx.fillText(models ? `Vento/raffiche kn: ${models}` : v.reasons[0] ?? '', 64, y + 82, W - 120);
		ctx.fillText(`Onda ${fmt(v.wave, 1)} m`, 64, y + 108);
		y += rowH;
	}

	ctx.fillStyle = '#6b7a8c';
	ctx.font = font(20);
	ctx.fillText('Dati Open-Meteo (CC BY 4.0). Strumento di supporto: verifica sempre il bollettino ufficiale.', 48, H - 62);
	ctx.fillStyle = '#0f4c5c';
	ctx.font = font(20, 600);
	ctx.fillText(`© ${BRAND.year} ${BRAND.author} · ${BRAND.org}`, 48, H - 32);
	return new Promise((resolve) => c.toBlob((b) => resolve(b!), 'image/png'));
}

/** Condivide con il menu nativo (WhatsApp, Mail, AirDrop…); se non disponibile scarica il file. */
export async function shareReport(trip: Trip, text: string, png: Blob): Promise<'shared' | 'downloaded' | 'cancelled'> {
	const name = `skipper-meteo-${trip.date}.png`;
	const file = new File([png], name, { type: 'image/png' });
	const data: ShareData = { title: `Skipper Meteo — ${trip.name}`, text, files: [file] };
	if (navigator.canShare?.(data)) {
		try {
			await navigator.share(data);
			return 'shared';
		} catch (e) {
			if ((e as Error).name === 'AbortError') return 'cancelled';
		}
	}
	const a = document.createElement('a');
	a.href = URL.createObjectURL(png);
	a.download = name;
	a.click();
	setTimeout(() => URL.revokeObjectURL(a.href), 10_000);
	return 'downloaded';
}
