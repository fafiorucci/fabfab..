<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import * as maplibregl from 'maplibre-gl';
	import { type GeoJSONSource, type ImageSource, type StyleSpecification } from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url';
	import type { BBox, Grid } from '#lib/meteo/api.ts';
	import type { LayerInfo } from '#lib/meteo/layers.ts';
	import { arrowFeatures, arrowImage, bboxCorners, renderField } from '#lib/map/field.ts';
	import { Particles } from '#lib/map/particles.ts';

	export type Base = 'light' | 'satellite';

	interface Props {
		/** Zona dell'uscita: inquadrata all'apertura e con il tasto "casa". */
		home: BBox | null;
		/** Ogni livello porta la propria griglia: durante il caricamento di una nuova zona resta visibile la precedente. */
		field: { grid: Grid; values: ArrayLike<number> } | null;
		layer: LayerInfo;
		arrows: { grid: Grid; dir: ArrayLike<number>; value: ArrayLike<number> } | null;
		wind: { grid: Grid; u: ArrayLike<number>; v: ArrayLike<number> } | null;
		base: Base;
		seamarks: boolean;
		particles: boolean;
		point: { lat: number; lon: number } | null;
		/** Contenuto HTML del riquadro con i valori nel punto toccato. */
		popup: string | null;
		onpick?: (lat: number, lon: number) => void;
		/** Il riquadro del punto è stato chiuso con la ×. */
		onclosepoint?: () => void;
		onview?: (bbox: BBox) => void;
	}

	let { home, field, layer, arrows, wind, base, seamarks, particles, point, popup, onpick, onclosepoint, onview }: Props = $props();

	let container: HTMLDivElement;
	let overlay: HTMLCanvasElement;
	let map: maplibregl.Map | undefined;
	let parts: Particles | undefined;
	let marker: maplibregl.Marker | undefined;
	let pop: maplibregl.Popup | undefined;
	let styleReady = $state(0);
	const fieldCanvas = document.createElement('canvas');
	const EMPTY_PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=';

	const LIGHT_STYLE = 'https://tiles.openfreemap.org/styles/positron';
	const SAT_STYLE: StyleSpecification = {
		version: 8,
		sources: {
			sat: {
				type: 'raster',
				tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
				tileSize: 256,
				maxzoom: 19,
				attribution: 'Immagini © Esri, Maxar, Earthstar Geographics'
			},
			ref: {
				type: 'raster',
				tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}'],
				tileSize: 256,
				maxzoom: 19
			}
		},
		layers: [
			{ id: 'sat', type: 'raster', source: 'sat' },
			{ id: 'ref', type: 'raster', source: 'ref' }
		]
	};

	function firstSymbolLayer(): string | undefined {
		return map!.getStyle().layers.find((l) => l.type === 'symbol')?.id;
	}

	function installOverlays() {
		const m = map!;
		const before = firstSymbolLayer();
		m.addSource('field', { type: 'image', url: EMPTY_PNG, coordinates: bboxCorners({ lats: [0, 0.1], lons: [0, 0.1], bbox: [0, 0, 0.1, 0.1] }) });
		m.addLayer({ id: 'field', type: 'raster', source: 'field', paint: { 'raster-opacity': 0.62, 'raster-fade-duration': 0, 'raster-resampling': 'linear' } }, before);
		m.addSource('seamarks', {
			type: 'raster',
			tiles: ['https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png'],
			tileSize: 256,
			attribution: 'Segnali © OpenSeaMap'
		});
		m.addLayer({ id: 'seamarks', type: 'raster', source: 'seamarks', minzoom: 8, layout: { visibility: seamarks ? 'visible' : 'none' } });
		if (!m.hasImage('arrow')) m.addImage('arrow', arrowImage(), { sdf: true });
		m.addSource('arrows', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
		m.addLayer({
			id: 'arrows',
			type: 'symbol',
			source: 'arrows',
			layout: {
				'icon-image': 'arrow',
				'icon-rotate': ['get', 'rot'],
				'icon-rotation-alignment': 'map',
				'icon-allow-overlap': true,
				'icon-size': ['interpolate', ['linear'], ['zoom'], 5, 0.3, 9, 0.55, 12, 0.7]
			},
			paint: { 'icon-color': '#0b1d2c', 'icon-halo-color': '#ffffff', 'icon-halo-width': 1.5, 'icon-opacity': 0.85 }
		});
		styleReady++;
	}

	// Con il bundling di Vite il worker va indicato esplicitamente.
	maplibregl.setWorkerUrl(workerUrl);

	onMount(() => {
		map = new maplibregl.Map({
			container,
			style: base === 'satellite' ? SAT_STYLE : LIGHT_STYLE,
			...(home ? { bounds: home, fitBoundsOptions: { padding: 24 } } : { center: [12.5, 40] as [number, number], zoom: 5 }),
			attributionControl: { compact: true },
			canvasContextAttributes: { preserveDrawingBuffer: true }
		});
		map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'top-right');
		map.addControl(new maplibregl.ScaleControl({ unit: 'nautical' }), 'bottom-left');
		map.on('style.load', installOverlays);
		map.on('click', (e) => onpick?.(e.lngLat.lat, e.lngLat.lng));
		const emitView = () => {
			const b = map!.getBounds();
			onview?.([b.getWest(), b.getSouth(), b.getEast(), b.getNorth()]);
		};
		map.on('moveend', emitView);
		map.once('load', emitView);
		parts = new Particles(map, overlay);
	});

	onDestroy(() => {
		parts?.stop();
		map?.remove();
	});

	// Cambio stile di base: le sorgenti personalizzate vengono reinstallate su 'style.load'.
	let currentBase: Base | undefined;
	$effect(() => {
		const b = base;
		if (!map) return;
		if (currentBase === undefined) {
			currentBase = b;
			return;
		}
		if (b === currentBase) return;
		currentBase = b;
		map.setStyle(b === 'satellite' ? SAT_STYLE : LIGHT_STYLE);
	});

	// Nuova uscita: inquadra la sua zona (la mappa poi segnala la vista e arrivano i dati).
	let homeKey = '';
	$effect(() => {
		const key = home?.join(',') ?? '';
		if (!map || !home || key === homeKey) return;
		const first = homeKey === '';
		homeKey = key;
		if (!first) goHome(0);
	});

	$effect(() => {
		if (!styleReady || !map) return;
		const src = map.getSource('field') as ImageSource;
		if (!field) {
			src.updateImage({ url: EMPTY_PNG });
			return;
		}
		src.updateImage({ url: renderField(fieldCanvas, field.grid, field.values, layer), coordinates: bboxCorners(field.grid) });
	});

	$effect(() => {
		if (!styleReady || !map) return;
		const fc = arrows ? arrowFeatures(arrows.grid, arrows.dir, arrows.value) : { type: 'FeatureCollection' as const, features: [] };
		(map.getSource('arrows') as GeoJSONSource).setData(fc);
		map.setPaintProperty('arrows', 'icon-color', base === 'satellite' ? '#ffffff' : '#0b1d2c');
		map.setPaintProperty('arrows', 'icon-halo-color', base === 'satellite' ? '#0b1d2c' : '#ffffff');
	});

	$effect(() => {
		if (!styleReady || !map) return;
		map.setLayoutProperty('seamarks', 'visibility', seamarks ? 'visible' : 'none');
	});

	$effect(() => {
		if (!parts) return;
		parts.setField(wind?.grid ?? null, wind?.u ?? null, wind?.v ?? null);
		if (particles && wind) parts.start();
		else parts.stop();
	});

	$effect(() => {
		if (!map) return;
		if (!point) {
			marker?.remove();
			marker = undefined;
			return;
		}
		if (!marker) marker = new maplibregl.Marker({ color: '#ff7a1a' });
		marker.setLngLat([point.lon, point.lat]).addTo(map);
	});

	$effect(() => {
		if (!map) return;
		if (!point || !popup) {
			pop?.remove();
			pop = undefined;
			return;
		}
		if (!pop) {
			pop = new maplibregl.Popup({ closeOnClick: false, closeButton: true, maxWidth: '340px', offset: 34, className: 'point-popup' });
			pop.on('close', () => {
				pop = undefined;
				onclosepoint?.();
			});
		}
		pop.setLngLat([point.lon, point.lat]).setHTML(popup);
		if (!pop.isOpen()) pop.addTo(map);
	});

	/** Istantanea PNG della mappa (per il report). */
	export function snapshot(): string | null {
		try {
			return map?.getCanvas().toDataURL('image/png') ?? null;
		} catch {
			return null;
		}
	}

	/** Torna alla zona dell'uscita. */
	export function goHome(duration = 600) {
		if (!map || !home) return;
		map.fitBounds([[home[0], home[1]], [home[2], home[3]]], { padding: 24, duration });
	}

	export function flyTo(lat: number, lon: number) {
		map?.flyTo({ center: [lon, lat], zoom: Math.max(map.getZoom(), 9) });
	}
</script>

<div class="wrap">
	<div class="map" bind:this={container}></div>
	<canvas class="particles" bind:this={overlay}></canvas>
</div>

<style>
	.wrap {
		position: relative;
		width: 100%;
		height: 100%;
	}
	.map {
		position: absolute;
		inset: 0;
	}
	.particles {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}
</style>
