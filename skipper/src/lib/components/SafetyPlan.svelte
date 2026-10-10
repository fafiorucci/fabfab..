<script lang="ts">
	import { persisted, uid } from '#lib/persist.svelte.ts';
	import { GROUP_LABEL, LAYOUTS, PLAN_ITEMS, itemById, layoutById, type PlanItem } from '#lib/boat/layouts.ts';

	interface Marker {
		id: string;
		item: string;
		x: number;
		y: number;
		note: string;
	}
	interface Plan {
		layout: string;
		boatName: string;
		image: string | null;
		markers: Marker[];
	}

	const store = persisted<Plan>('safetyplan', { layout: 'mono-3c-2b', boatName: '', image: null, markers: [] });
	const plan = $derived(store.value);
	const layout = $derived(layoutById(plan.layout));

	const GROUP_COLOR: Record<PlanItem['group'], string> = {
		sicurezza: '#d64545',
		energia: '#e0a020',
		acqua: '#2f80ed',
		motore: '#6b7a8c',
		bordo: '#2e9d5b'
	};

	let armed: string | null = $state(null);
	let selected: string | null = $state(null);
	let highlight: string | null = $state(null);
	let svg: SVGSVGElement | undefined = $state();
	let drag: { id: string; moved: boolean } | null = null;
	let msg: string | null = $state(null);

	const groups = $derived(
		(Object.keys(GROUP_LABEL) as PlanItem['group'][]).map((g) => ({ g, items: PLAN_ITEMS.filter((i) => i.group === g) }))
	);
	const count = (item: string) => plan.markers.filter((m) => m.item === item).length;
	const selMarker = $derived(plan.markers.find((m) => m.id === selected) ?? null);

	function toPlan(e: PointerEvent): { x: number; y: number } {
		const pt = svg!.createSVGPoint();
		pt.x = e.clientX;
		pt.y = e.clientY;
		const p = pt.matrixTransform(svg!.getScreenCTM()!.inverse());
		return { x: Math.max(10, Math.min(990, p.x)), y: Math.max(10, Math.min(390, p.y)) };
	}

	function onPlanClick(e: PointerEvent) {
		if (!armed) {
			selected = null;
			return;
		}
		const { x, y } = toPlan(e);
		const m: Marker = { id: uid(), item: armed, x, y, note: '' };
		store.value.markers = [...plan.markers, m];
		selected = m.id;
		armed = null;
	}

	function onMarkerDown(e: PointerEvent, id: string) {
		e.stopPropagation();
		(e.currentTarget as Element).setPointerCapture(e.pointerId);
		drag = { id, moved: false };
	}
	function onMarkerMove(e: PointerEvent) {
		if (!drag) return;
		const m = plan.markers.find((x) => x.id === drag!.id);
		if (!m) return;
		const p = toPlan(e);
		if (Math.hypot(p.x - m.x, p.y - m.y) > 3) drag.moved = true;
		if (drag.moved) {
			m.x = p.x;
			m.y = p.y;
		}
	}
	function onMarkerUp(e: PointerEvent) {
		e.stopPropagation();
		if (drag && !drag.moved) selected = selected === drag.id ? null : drag.id;
		drag = null;
	}

	function remove(id: string) {
		store.value.markers = plan.markers.filter((m) => m.id !== id);
		selected = null;
	}

	function flash(item: string) {
		highlight = item;
		setTimeout(() => (highlight = highlight === item ? null : highlight), 2600);
	}

	/** Foto o pianta della propria barca, ridotta per stare nella memoria del dispositivo. */
	async function onImage(e: Event) {
		const file = (e.currentTarget as HTMLInputElement).files?.[0];
		if (!file) return;
		const url = URL.createObjectURL(file);
		const img = new Image();
		img.src = url;
		await img.decode();
		const scale = Math.min(1, 1400 / Math.max(img.width, img.height));
		const c = document.createElement('canvas');
		c.width = Math.round(img.width * scale);
		c.height = Math.round(img.height * scale);
		c.getContext('2d')!.drawImage(img, 0, 0, c.width, c.height);
		URL.revokeObjectURL(url);
		store.value.image = c.toDataURL('image/jpeg', 0.8);
		store.value.layout = 'custom';
	}

	/** Immagine PNG della pianta con la legenda, da mandare all'equipaggio. */
	async function share() {
		if (!svg) return;
		const W = 1600;
		const planH = 640;
		const used = PLAN_ITEMS.filter((i) => count(i.id));
		const rowH = 40;
		const H = 110 + planH + 40 + Math.ceil(used.length / 2) * rowH + 30;
		const c = document.createElement('canvas');
		c.width = W;
		c.height = H;
		const ctx = c.getContext('2d')!;
		ctx.fillStyle = '#f4f7fa';
		ctx.fillRect(0, 0, W, H);
		ctx.fillStyle = '#0b1d2c';
		ctx.fillRect(0, 0, W, 90);
		ctx.fillStyle = '#fff';
		ctx.font = '700 40px system-ui, sans-serif';
		ctx.fillText(`Safety plan${plan.boatName ? ` — ${plan.boatName}` : ''}`, 40, 60);
		const xml = new XMLSerializer().serializeToString(svg);
		const img = new Image();
		img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
		await img.decode();
		ctx.drawImage(img, 0, 110, W, planH);
		ctx.font = '26px system-ui, sans-serif';
		used.forEach((it, k) => {
			const x = 40 + (k % 2) * (W / 2);
			const y = 110 + planH + 50 + Math.floor(k / 2) * rowH;
			ctx.fillStyle = GROUP_COLOR[it.group];
			ctx.beginPath();
			ctx.arc(x + 14, y - 9, 14, 0, Math.PI * 2);
			ctx.fill();
			ctx.fillStyle = '#0f2233';
			ctx.fillText(`${it.icon} ${it.label}${count(it.id) > 1 ? ` (${count(it.id)})` : ''}`, x + 40, y);
		});
		const blob: Blob = await new Promise((r) => c.toBlob((b) => r(b!), 'image/png'));
		const file = new File([blob], 'safety-plan.png', { type: 'image/png' });
		const data = { title: 'Safety plan', text: 'Dove si trovano le dotazioni a bordo', files: [file] };
		if (navigator.canShare?.(data)) {
			try {
				await navigator.share(data);
				return;
			} catch (err) {
				if ((err as Error).name === 'AbortError') return;
			}
		}
		const a = document.createElement('a');
		a.href = URL.createObjectURL(blob);
		a.download = 'safety-plan.png';
		a.click();
		msg = 'Immagine scaricata';
		setTimeout(() => (msg = null), 2500);
	}
</script>

<section class="sp">
	<div class="head">
		<label class="m-field">
			<span>Tipo di barca</span>
			<select bind:value={store.value.layout}>
				{#each LAYOUTS as l (l.id)}<option value={l.id}>{l.name}</option>{/each}
				<option value="custom" disabled={!plan.image}>Pianta della mia barca (immagine caricata)</option>
			</select>
		</label>
		<label class="m-field">
			<span>Nome barca</span>
			<input bind:value={store.value.boatName} placeholder="Es. Dufour 460 «Aurora»" />
		</label>
		<label class="m-field">
			<span>Carica la pianta della tua barca</span>
			<input type="file" accept="image/*" onchange={onImage} />
		</label>
	</div>

	{#if armed}
		<p class="hint">Tocca la pianta dove si trova: <b>{itemById(armed)?.icon} {itemById(armed)?.label}</b> <button class="m-small-btn" onclick={() => (armed = null)}>Annulla</button></p>
	{:else}
		<p class="m-muted">Scegli un elemento qui sotto e poi tocca la pianta. Trascina un segnaposto per spostarlo, toccalo per aggiungere una nota.</p>
	{/if}

	<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
	<svg
		bind:this={svg}
		class="plan"
		class:arming={!!armed}
		viewBox="0 0 1000 400"
		role="img"
		aria-label="Pianta della barca con le dotazioni"
		onpointerup={(e) => !drag && onPlanClick(e)}
		onpointermove={onMarkerMove}
	>
		<rect x="0" y="0" width="1000" height="400" fill="#eaf2f8" />
		{#if plan.layout === 'custom' && plan.image}
			<image href={plan.image} x="0" y="0" width="1000" height="400" preserveAspectRatio="xMidYMid meet" />
		{:else if layout}
			<path d={layout.hull} fill="#ffffff" stroke="#0b1d2c" stroke-width="4" />
			{#each layout.rooms as r (r.label)}
				<rect x={r.x} y={r.y} width={r.w} height={r.h} rx="8" class="room {r.kind}" />
				<text x={r.x + r.w / 2} y={r.y + r.h / 2} class="room-label" text-anchor="middle" dominant-baseline="middle">{r.label}</text>
			{/each}
			<text x="60" y="390" class="bow">◀ PRUA</text>
			<text x="940" y="390" class="bow" text-anchor="end">POPPA ▶</text>
		{/if}
		{#each plan.markers as m (m.id)}
			{@const it = itemById(m.item)}
			{#if it}
				<g
					class="marker"
					class:sel={selected === m.id}
					class:pulse={highlight === m.item}
					transform="translate({m.x} {m.y})"
					onpointerdown={(e) => onMarkerDown(e, m.id)}
					onpointerup={onMarkerUp}
					role="button"
					tabindex="0"
					aria-label={it.label}
				>
					<circle r="21" fill={GROUP_COLOR[it.group]} stroke="#fff" stroke-width="4" />
					<text text-anchor="middle" dominant-baseline="central" font-size="22">{it.icon}</text>
					{#if selected === m.id || highlight === m.item}
						<text y="-32" text-anchor="middle" class="mlabel">{it.label}</text>
					{/if}
				</g>
			{/if}
		{/each}
	</svg>

	{#if selMarker}
		{@const it = itemById(selMarker.item)}
		<div class="m-card sel-card">
			<b>{it?.icon} {it?.label}</b>
			<input class="note" bind:value={selMarker.note} placeholder="Nota (es. sotto il materasso, gavone sx)" />
			<button class="m-small-btn" onclick={() => remove(selMarker.id)}>Elimina</button>
		</div>
	{/if}

	<div class="legend">
		{#each groups as { g, items } (g)}
			<div class="grp">
				<p class="grp-h" style="--c: {GROUP_COLOR[g]}">{GROUP_LABEL[g]}</p>
				<div class="chips">
					{#each items as it (it.id)}
						<div class="chip" class:armed={armed === it.id} class:done={count(it.id) > 0}>
							<button class="place" onclick={() => (armed = armed === it.id ? null : it.id)} title="Posiziona sulla pianta">{it.icon} {it.label}</button>
							{#if count(it.id)}
								<button class="find" onclick={() => flash(it.id)} title="Mostra sulla pianta">📍{count(it.id) > 1 ? count(it.id) : ''}</button>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		{/each}
	</div>

	{#if plan.markers.some((m) => m.note)}
		<div class="m-card">
			<h2>Note</h2>
			<ul class="notes">
				{#each plan.markers.filter((m) => m.note) as m (m.id)}<li><b>{itemById(m.item)?.label}:</b> {m.note}</li>{/each}
			</ul>
		</div>
	{/if}

	<div class="m-actions">
		<button class="ghost" onclick={() => confirm('Cancellare tutti i segnaposto?') && (store.value.markers = [])}>Azzera segnaposto</button>
		<button class="primary" onclick={share} disabled={!plan.markers.length}>Condividi pianta</button>
	</div>
	{#if msg}<p class="m-muted">{msg}</p>{/if}
</section>

<style>
	.head {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 10px;
		margin-bottom: 8px;
	}
	.hint {
		background: var(--accent-soft);
		padding: 8px 10px;
		border-radius: 10px;
		margin: 0 0 8px;
	}
	.plan {
		width: 100%;
		height: auto;
		display: block;
		border-radius: 14px;
		box-shadow: var(--shadow);
		touch-action: none;
		user-select: none;
	}
	.plan.arming {
		cursor: crosshair;
		outline: 3px solid var(--accent);
	}
	.room {
		fill: #f6f1e7;
		stroke: #b8a98d;
		stroke-width: 2;
	}
	.room.head {
		fill: #e3f0fb;
	}
	.room.cockpit {
		fill: #e9eef3;
	}
	.room.engine {
		fill: #e6e6e6;
	}
	.room.locker {
		fill: #efe8da;
	}
	.room-label {
		font: 600 15px system-ui, sans-serif;
		fill: #5b6b7d;
		pointer-events: none;
	}
	.bow {
		font: 700 14px system-ui, sans-serif;
		fill: #8a99a8;
	}
	.marker {
		cursor: grab;
	}
	.marker.sel circle {
		stroke: #0b1d2c;
	}
	.marker.pulse circle {
		animation: pulse 0.6s ease-in-out 4 alternate;
	}
	@keyframes pulse {
		to {
			r: 30;
		}
	}
	.mlabel {
		font: 700 16px system-ui, sans-serif;
		fill: #0b1d2c;
		paint-order: stroke;
		stroke: #fff;
		stroke-width: 5px;
	}
	.sel-card {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		margin-top: 8px;
	}
	.note {
		flex: 1;
		min-width: 180px;
		padding: 7px 10px;
		border-radius: 8px;
		border: 1px solid var(--line-strong);
		background: var(--bg);
		color: var(--text);
	}
	.legend {
		margin-top: 10px;
		display: grid;
		gap: 8px;
	}
	.grp-h {
		margin: 0 0 4px;
		font-size: 0.75rem;
		font-weight: 700;
		text-transform: uppercase;
		color: var(--c);
	}
	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}
	.chip {
		display: flex;
		border: 1px solid var(--line-strong);
		border-radius: 18px;
		overflow: hidden;
		background: var(--panel);
	}
	.chip.done {
		border-color: var(--go);
	}
	.chip.armed {
		border-color: var(--accent);
		box-shadow: 0 0 0 2px var(--accent);
	}
	.chip button {
		border: 0;
		background: none;
		color: var(--text);
		font-size: 0.82rem;
		padding: 5px 10px;
	}
	.chip .find {
		border-left: 1px solid var(--line);
		background: color-mix(in srgb, var(--go) 12%, transparent);
	}
	.notes {
		margin: 0;
		padding-left: 18px;
		font-size: 0.88rem;
	}
</style>
