<script lang="ts">
	import { LEVEL_LABEL, type DayVerdict } from '#lib/meteo/assess.ts';
	import { dayLabel } from '#lib/meteo/grid.ts';
	import { modelById } from '#lib/meteo/models.ts';
	import type { Limits } from '#lib/trip.ts';

	interface Props {
		verdicts: DayVerdict[];
		limits: Limits;
	}

	let { verdicts, limits }: Props = $props();
	const fmt = (x: number, d = 0) => (Number.isNaN(x) ? '—' : x.toFixed(d).replace('.', ','));
</script>

<div class="list">
	{#each verdicts as v (v.date)}
		<article class="day {v.level}">
			<header>
				<span class="dot" aria-hidden="true"></span>
				<strong>{dayLabel(v.date)}</strong>
				<span class="level">{LEVEL_LABEL[v.level]}</span>
			</header>
			<ul class="reasons">
				{#each v.reasons as r}<li>{r}</li>{/each}
			</ul>
			{#if v.models.length}
				<table>
					<thead><tr><th>Modello</th><th>Vento</th><th>Raffiche</th></tr></thead>
					<tbody>
						{#each v.models as m (m.model)}
							{@const info = modelById(m.model)}
							<tr>
								<td><span class="sw" style="background: {info?.color}"></span>{info?.label ?? m.model}</td>
								<td class:over={m.wind > limits.wind}>{fmt(m.wind)} kn</td>
								<td class:over={m.gust > limits.gust}>{fmt(m.gust)} kn</td>
							</tr>
						{/each}
						<tr class="wave">
							<td>Onda</td>
							<td colspan="2" class:over={v.wave > limits.wave}>{fmt(v.wave, 1)} m</td>
						</tr>
					</tbody>
				</table>
			{/if}
		</article>
	{/each}
	<p class="note">
		Valori al 90° percentile sui punti di mare della zona inquadrata, ore 7–20. Strumento di supporto: consulta sempre il bollettino ufficiale
		(<a href="https://www.meteoam.it/it/meteo-mare" target="_blank" rel="noopener">Meteomar</a>) prima di uscire.
	</p>
</div>

<style>
	.list {
		display: grid;
		gap: 10px;
	}
	.day {
		border: 1px solid var(--line);
		border-left: 6px solid var(--lvl);
		border-radius: 12px;
		padding: 10px 12px;
		background: var(--panel);
	}
	.go {
		--lvl: var(--go);
	}
	.caution {
		--lvl: var(--caution);
	}
	.nogo {
		--lvl: var(--nogo);
	}
	.nodata {
		--lvl: var(--muted);
	}
	header {
		display: flex;
		align-items: center;
		gap: 8px;
		text-transform: capitalize;
	}
	.dot {
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background: var(--lvl);
	}
	.level {
		margin-left: auto;
		font-weight: 700;
		color: var(--lvl);
		text-transform: none;
	}
	.reasons {
		margin: 6px 0;
		padding-left: 18px;
		font-size: 0.86rem;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.82rem;
		font-variant-numeric: tabular-nums;
	}
	th {
		text-align: left;
		color: var(--muted);
		font-weight: 600;
	}
	td,
	th {
		padding: 3px 4px;
		border-top: 1px solid var(--line);
	}
	td.over {
		color: var(--nogo);
		font-weight: 700;
	}
	.sw {
		display: inline-block;
		width: 8px;
		height: 8px;
		border-radius: 2px;
		margin-right: 6px;
	}
	.wave td {
		color: var(--muted);
	}
	.wave td.over {
		color: var(--nogo);
	}
	.note {
		font-size: 0.75rem;
		color: var(--muted);
		margin: 0;
	}
</style>
