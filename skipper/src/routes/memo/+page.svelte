<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Locked from '#lib/components/Locked.svelte';
	import {
		BEAUFORT,
		COLREG_FANALI,
		COLREG_PRECEDENZE,
		COLREG_SUONI,
		DOUGLAS,
		FLAGS,
		IALA,
		LUCI_RITMI,
		MARPOL,
		NUMBERS,
		VHF,
		type Rule
	} from '#lib/memo.ts';

	const SECTIONS = [
		{ id: 'colreg', title: 'COLREG — regole di rotta', icon: '⚓' },
		{ id: 'iala', title: 'IALA — segnalamenti (regione A)', icon: '🚩' },
		{ id: 'bandiere', title: 'Bandiere e alfabeto', icon: '🏁' },
		{ id: 'meteo', title: 'Scale Beaufort e Douglas', icon: '🌊' },
		{ id: 'vhf', title: 'VHF e comunicazioni', icon: '📻' },
		{ id: 'marpol', title: 'MARPOL e ambiente', icon: '♻️' }
	] as const;

	let open: string | null = $state('colreg');
	let q = $state('');
	let missing: Record<string, boolean> = $state({});

	const match = (...s: string[]) => !q.trim() || s.some((x) => x.toLowerCase().includes(q.trim().toLowerCase()));
	const rules = (list: Rule[]) => list.filter((r) => match(r.title, r.text));
</script>

{#snippet ruleList(title: string, list: Rule[])}
	{@const items = rules(list)}
	{#if items.length}
		<h3>{title}</h3>
		<dl class="rules">
			{#each items as r (r.title)}
				<dt>{r.title}</dt>
				<dd>{r.text}</dd>
			{/each}
		</dl>
	{/if}
{/snippet}

<ModuleShell title="Skipper memo">
	<h1 class="m-h1">Skipper memo</h1>
	<p class="m-lead">
		Promemoria rapido per lo skipper: regole di rotta, segnalamenti, bandiere, scale del vento e del mare, VHF e MARPOL. È un aiuto alla
		memoria, non sostituisce i testi ufficiali.
	</p>

	<Locked label="Skipper memo nella versione completa">
		<input class="search" type="search" placeholder="Cerca (es. «barca a vela», «cardinale», «Oscar»)" bind:value={q} />

		{#each SECTIONS as s (s.id)}
			<section class="sec" class:open={open === s.id || q.trim()}>
				<button class="sec-h" onclick={() => (open = open === s.id ? null : s.id)} aria-expanded={open === s.id}>
					<span>{s.icon}</span>{s.title}<span class="chev">{open === s.id || q.trim() ? '−' : '+'}</span>
				</button>
				{#if open === s.id || q.trim()}
					<div class="sec-b">
						{#if s.id === 'colreg'}
							{@render ruleList('Precedenze e manovre', COLREG_PRECEDENZE)}
							{@render ruleList('Fanali e segnali diurni', COLREG_FANALI)}
							{@render ruleList('Segnali sonori', COLREG_SUONI)}
						{:else if s.id === 'iala'}
							<div class="marks">
								{#each IALA.filter((m) => match(m.name, m.look, m.light, m.meaning)) as m (m.name)}
									<div class="mark">
										<b>{m.name}</b>
										<span><i>Aspetto:</i> {m.look}</span>
										<span><i>Luce:</i> {m.light}</span>
										<span>{m.meaning}</span>
									</div>
								{/each}
							</div>
							{@render ruleList('Ritmi delle luci', LUCI_RITMI)}
						{:else if s.id === 'bandiere'}
							<div class="flags">
								{#each FLAGS.filter((f) => match(f.letter, f.word, f.meaning)) as f (f.letter)}
									<div class="flag">
										{#if missing[f.letter]}
											<div class="ph">{f.letter}</div>
										{:else}
											<img
												src="./flags/{f.letter.toLowerCase()}.svg"
												alt="Bandiera {f.word}"
												width="56"
												height="56"
												loading="lazy"
												onerror={() => (missing[f.letter] = true)}
											/>
										{/if}
										<div>
											<b>{f.letter} — {f.word}</b>
											<span>{f.meaning}</span>
										</div>
									</div>
								{/each}
							</div>
							{#if match('numeri', ...NUMBERS.flat())}
								<h3>Numeri in radio</h3>
								<div class="nums">
									{#each NUMBERS as [n, w] (n)}<span><b>{n}</b> {w}</span>{/each}
								</div>
							{/if}
						{:else if s.id === 'meteo'}
							<h3>Beaufort — vento</h3>
							<table>
								<thead><tr><th>F</th><th>Nome</th><th>Nodi</th><th>Aspetto del mare</th></tr></thead>
								<tbody>
									{#each BEAUFORT.filter((b) => match(b.name, b.sea)) as b (b.f)}
										<tr><td><b>{b.f}</b></td><td>{b.name}</td><td class="nw">{b.kn}</td><td>{b.sea}</td></tr>
									{/each}
								</tbody>
							</table>
							<h3>Douglas — stato del mare</h3>
							<table>
								<thead><tr><th>D</th><th>Nome</th><th>Onda (m)</th></tr></thead>
								<tbody>
									{#each DOUGLAS.filter((d) => match(d.name)) as d (d.d)}
										<tr><td><b>{d.d}</b></td><td>{d.name}</td><td class="nw">{d.m}</td></tr>
									{/each}
								</tbody>
							</table>
						{:else if s.id === 'vhf'}
							{@render ruleList('VHF', VHF)}
						{:else}
							{@render ruleList('MARPOL 73/78', MARPOL)}
						{/if}
					</div>
				{/if}
			</section>
		{/each}
	</Locked>
</ModuleShell>

<style>
	.search {
		width: 100%;
		margin-bottom: 10px;
		padding: 10px 12px;
		border: 1px solid var(--line-strong);
		border-radius: 12px;
		background: var(--panel);
		color: var(--text);
		font: inherit;
	}
	.sec {
		background: var(--panel);
		border-radius: 12px;
		box-shadow: var(--shadow);
		margin-bottom: 8px;
		overflow: hidden;
	}
	.sec-h {
		width: 100%;
		display: flex;
		gap: 10px;
		align-items: center;
		border: 0;
		background: none;
		color: var(--text);
		font-weight: 700;
		font-size: 1rem;
		padding: 12px 14px;
		text-align: left;
	}
	.chev {
		margin-left: auto;
		color: var(--muted);
	}
	.sec-b {
		padding: 0 14px 14px;
	}
	h3 {
		font-size: 0.85rem;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: var(--brand-2);
		margin: 14px 0 6px;
	}
	.rules {
		margin: 0;
	}
	.rules dt {
		font-weight: 700;
		margin-top: 8px;
	}
	.rules dd {
		margin: 2px 0 0;
		line-height: 1.5;
	}
	.marks {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
		gap: 8px;
	}
	.mark {
		display: grid;
		gap: 3px;
		border: 1px solid var(--line);
		border-radius: 10px;
		padding: 8px 10px;
		font-size: 0.9rem;
	}
	.mark i {
		color: var(--muted);
		font-style: normal;
	}
	.flags {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
		gap: 8px;
	}
	.flag {
		display: flex;
		gap: 10px;
		align-items: center;
		font-size: 0.88rem;
	}
	.flag img,
	.ph {
		flex: none;
		width: 56px;
		height: 56px;
	}
	.ph {
		display: grid;
		place-items: center;
		border: 1px solid var(--line-strong);
		font-weight: 800;
		font-size: 1.4rem;
	}
	.flag div {
		display: grid;
	}
	.nums {
		display: flex;
		flex-wrap: wrap;
		gap: 6px 14px;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.88rem;
	}
	th,
	td {
		text-align: left;
		padding: 5px 6px;
		border-bottom: 1px solid var(--line);
		vertical-align: top;
	}
	.nw {
		white-space: nowrap;
	}
</style>
