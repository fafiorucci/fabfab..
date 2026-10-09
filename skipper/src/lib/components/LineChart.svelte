<script lang="ts">
	import { dayLabel, localParts } from '#lib/meteo/grid.ts';

	export interface Line {
		label: string;
		color: string;
		values: number[];
		dashed?: boolean;
	}

	interface Props {
		times: number[];
		utcOffset: number;
		lines: Line[];
		unit: string;
		limit?: number;
		cursor?: number;
		height?: number;
		onseek?: (t: number) => void;
	}

	let { times, utcOffset, lines, unit, limit, cursor, height = 150, onseek }: Props = $props();

	// Larghezza reale del contenitore: testo e linee restano leggibili a ogni dimensione.
	let width = $state(360);
	const W = $derived(Math.max(240, width));
	const PAD = { l: 30, r: 8, t: 12, b: 22 };

	const all = $derived(lines.flatMap((l) => l.values).filter((v) => !Number.isNaN(v)));
	const yMax = $derived(Math.max(1, ...(limit ? [limit * 1.1] : []), ...all) * 1.08);
	const x = (i: number) => PAD.l + (i / Math.max(1, times.length - 1)) * (W - PAD.l - PAD.r);
	const y = (v: number) => PAD.t + (1 - v / yMax) * (height - PAD.t - PAD.b);

	function path(values: number[]) {
		let d = '';
		let pen = false;
		values.forEach((v, i) => {
			if (Number.isNaN(v)) {
				pen = false;
				return;
			}
			d += `${pen ? 'L' : 'M'}${x(i).toFixed(1)},${y(v).toFixed(1)}`;
			pen = true;
		});
		return d;
	}

	const ticks = $derived.by(() => {
		const step = yMax > 40 ? 10 : yMax > 15 ? 5 : yMax > 4 ? 1 : 0.5;
		const out: number[] = [];
		for (let v = 0; v <= yMax; v += step) out.push(v);
		return out;
	});

	const days = $derived(
		times
			.map((t, i) => ({ i, p: localParts(t, utcOffset) }))
			.filter(({ p }) => p.hour === 0)
			.map(({ i, p }) => ({ i, label: dayLabel(p.date) }))
	);

	function seek(e: PointerEvent) {
		if (!onseek || !times.length) return;
		const svg = e.currentTarget as SVGSVGElement;
		const r = svg.getBoundingClientRect();
		const px = ((e.clientX - r.left) / r.width) * W;
		const i = Math.round(((px - PAD.l) / (W - PAD.l - PAD.r)) * (times.length - 1));
		onseek(Math.max(0, Math.min(times.length - 1, i)));
	}
</script>

<div class="box" bind:clientWidth={width}>
<svg viewBox="0 0 {W} {height}" class="chart" role="img" aria-label="Grafico {unit}" onpointerdown={seek}>
	{#each ticks as t (t)}
		<line class="grid" x1={PAD.l} x2={W - PAD.r} y1={y(t)} y2={y(t)} />
		<text class="axis" x={PAD.l - 4} y={y(t) + 3} text-anchor="end">{t}</text>
	{/each}
	<text class="axis" x={PAD.l - 4} y={PAD.t - 1} text-anchor="end">{unit}</text>
	{#each days as d (d.i)}
		<line class="day" x1={x(d.i)} x2={x(d.i)} y1={PAD.t} y2={height - PAD.b} />
		<text class="axis" x={x(d.i) + 3} y={height - 6}>{d.label}</text>
	{/each}
	{#if limit}
		<line class="limit" x1={PAD.l} x2={W - PAD.r} y1={y(limit)} y2={y(limit)} />
		<text class="limit-label" x={W - PAD.r} y={y(limit) - 3} text-anchor="end">limite {limit}</text>
	{/if}
	{#each lines as l (l.label)}
		<path d={path(l.values)} stroke={l.color} class="line" class:dashed={l.dashed} />
	{/each}
	{#if cursor !== undefined && cursor >= 0}
		<line class="cursor" x1={x(cursor)} x2={x(cursor)} y1={PAD.t} y2={height - PAD.b} />
	{/if}
</svg>
</div>

<style>
	.box {
		width: 100%;
	}
	.chart {
		width: 100%;
		height: auto;
		display: block;
		touch-action: pan-y;
		cursor: pointer;
	}
	.grid {
		stroke: var(--line);
		stroke-width: 1;
	}
	.day {
		stroke: var(--line-strong);
		stroke-width: 1;
	}
	.axis {
		fill: var(--muted);
		font-size: 11px;
	}
	.line {
		fill: none;
		stroke-width: 2;
		stroke-linejoin: round;
	}
	.dashed {
		stroke-dasharray: 4 3;
		stroke-width: 1.4;
	}
	.limit {
		stroke: var(--nogo);
		stroke-dasharray: 6 4;
	}
	.limit-label {
		fill: var(--nogo);
		font-size: 10px;
	}
	.cursor {
		stroke: var(--accent);
		stroke-width: 2;
	}
</style>
