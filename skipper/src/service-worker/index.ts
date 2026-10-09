
import { self as sw } from '$app/service-worker';
import { assets, immutable, prerendered } from '$app/manifest';
import { version } from '$app/env';

/** Percorso di base dell'app (es. /nome-repo/ su GitHub Pages), ricavato dallo scope del worker. */
const scope = sw.registration.scope;
const abs = (p: string) => new URL(p.replace(/^\//, ''), scope).href;

const SHELL = `shell-${version}`;
const DATA = 'meteo-data-v1';
const TILES = 'map-tiles-v1';
const MAX_TILES = 3000;

const ASSETS = [...immutable, ...assets, ...prerendered].map((f) => abs(f.path)).concat(scope);

sw.addEventListener('install', (event) => {
	event.waitUntil(caches.open(SHELL).then((c) => c.addAll(ASSETS)).then(() => sw.skipWaiting()));
});

sw.addEventListener('activate', (event) => {
	event.waitUntil(
		caches
			.keys()
			.then((keys) => Promise.all(keys.filter((k) => k.startsWith('shell-') && k !== SHELL).map((k) => caches.delete(k))))
			.then(() => sw.clients.claim())
	);
});

const isData = (u: URL) => u.hostname.endsWith('open-meteo.com');
const isTile = (u: URL) =>
	/(openfreemap\.org|arcgisonline\.com|openseamap\.org)$/.test(u.hostname) || u.pathname.endsWith('.pbf') || u.pathname.endsWith('.png');

/** Dati meteo: prima la rete (dati freschi), in mare senza rete l'ultima copia salvata. */
async function networkFirst(req: Request, cacheName: string) {
	const cache = await caches.open(cacheName);
	try {
		const res = await fetch(req);
		if (res.ok) cache.put(req, res.clone());
		return res;
	} catch {
		const hit = await cache.match(req);
		if (hit) return hit;
		throw new Error('offline');
	}
}

let trimming = false;
async function trimTiles() {
	if (trimming) return;
	trimming = true;
	const cache = await caches.open(TILES);
	const keys = await cache.keys();
	for (const k of keys.slice(0, Math.max(0, keys.length - MAX_TILES))) await cache.delete(k);
	trimming = false;
}

/** Tile delle mappe: dalla cache se presenti, così la mappa già vista resta disponibile offline. */
async function cacheFirst(req: Request) {
	const cache = await caches.open(TILES);
	const hit = await cache.match(req);
	if (hit) return hit;
	const res = await fetch(req);
	if (res.ok || res.type === 'opaque') {
		cache.put(req, res.clone());
		if (Math.random() < 0.02) trimTiles();
	}
	return res;
}

sw.addEventListener('fetch', (event) => {
	const req = event.request;
	if (req.method !== 'GET') return;
	const url = new URL(req.url);

	if (isData(url)) {
		event.respondWith(networkFirst(req, DATA));
		return;
	}
	if (url.origin !== location.origin) {
		if (isTile(url)) event.respondWith(cacheFirst(req));
		return;
	}
	if (req.mode === 'navigate') {
		event.respondWith(fetch(req).catch(async () => (await caches.match(scope)) ?? Response.error()));
		return;
	}
	event.respondWith(caches.match(req).then((hit) => hit ?? fetch(req)));
});
