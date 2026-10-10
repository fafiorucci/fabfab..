<script lang="ts">
	import { resolve } from '$app/paths';
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Locked from '#lib/components/Locked.svelte';
	import { persisted, shareText } from '#lib/persist.svelte.ts';
	import { SICUREZZA, VITA_DI_BORDO, type BriefingPoint } from '#lib/briefing.ts';
	import { BRAND } from '#lib/brand.ts';

	type Part = 'vita' | 'sicurezza';
	const PARTS: Record<Part, { title: string; points: BriefingPoint[] }> = {
		vita: { title: 'Briefing vita di bordo', points: VITA_DI_BORDO },
		sicurezza: { title: 'Briefing sicurezza', points: SICUREZZA }
	};

	const done = persisted<Record<string, boolean>>('briefing', {});
	let part: Part = $state('vita');
	let open: string | null = $state(null);
	let toast: string | null = $state(null);

	const cur = $derived(PARTS[part]);
	const count = (p: Part) => PARTS[p].points.filter((x) => done.value[`${p}:${x.title}`]).length;

	async function share(p: Part) {
		const text = [
			`${PARTS[p].title} — ${BRAND.org}`,
			'',
			...PARTS[p].points.flatMap((x, i) => [`${i + 1}. ${x.title.toUpperCase()}`, x.text, ''])
		].join('\n');
		const r = await shareText(PARTS[p].title, text);
		if (r === 'copied') {
			toast = 'Testo copiato negli appunti';
			setTimeout(() => (toast = null), 2500);
		}
	}
</script>

<ModuleShell title="Briefing equipaggio">
	<h1 class="m-h1">Briefing equipaggio</h1>
	<p class="m-lead">
		Da fare prima di lasciare l’ormeggio, con tutto l’equipaggio. Spunta ogni punto quando l’hai spiegato; puoi mandare il testo completo
		all’equipaggio già prima della partenza. Tieni aperto il <a href={resolve('/safety')}>safety plan</a> per mostrare dove si trova ogni cosa.
	</p>

	<div class="parts">
		{#each Object.entries(PARTS) as [id, p] (id)}
			<button class:on={part === id} onclick={() => (part = id as Part)}>
				{p.title.replace('Briefing ', '')}
				<small>{count(id as Part)}/{p.points.length}</small>
			</button>
		{/each}
	</div>

	<Locked label="Briefing completo nella versione completa">
		<ol class="points">
			{#each cur.points as x, i (x.title)}
				{@const id = `${part}:${x.title}`}
				<li class:ok={done.value[id]}>
					<div class="head">
						<input type="checkbox" bind:checked={done.value[id]} aria-label="Spiegato" />
						<button class="title" onclick={() => (open = open === id ? null : id)}>
							<span class="n">{i + 1}</span>{x.title}<span class="chev">{open === id ? '−' : '+'}</span>
						</button>
					</div>
					{#if open === id || open === 'all'}<p>{x.text}</p>{/if}
				</li>
			{/each}
		</ol>

		<div class="m-actions">
			<button class="ghost" onclick={() => confirm('Azzerare le spunte del briefing?') && (done.value = {})}>Azzera</button>
			<button class="ghost" onclick={() => (open = open ? null : 'all')}>{open === 'all' ? 'Chiudi tutto' : 'Apri tutto'}</button>
			<button class="primary" onclick={() => share(part)}>Manda all’equipaggio</button>
		</div>
	</Locked>
	{#if toast}<p class="m-muted">{toast}</p>{/if}
</ModuleShell>

<style>
	.parts {
		display: flex;
		gap: 6px;
		margin-bottom: 12px;
	}
	.parts button {
		flex: 1;
		border: 1px solid var(--line-strong);
		background: var(--panel);
		color: var(--text);
		border-radius: 12px;
		padding: 10px;
		font-weight: 700;
		display: grid;
	}
	.parts button.on {
		background: var(--brand-2);
		border-color: var(--brand-2);
		color: #fff;
	}
	.parts small {
		font-weight: 500;
		opacity: 0.8;
	}
	.points {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 8px;
	}
	.points li {
		background: var(--panel);
		border-radius: 12px;
		padding: 10px 12px;
		box-shadow: var(--shadow);
	}
	.points li.ok {
		border-left: 5px solid var(--go);
	}
	.head {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.head input {
		width: 22px;
		height: 22px;
		flex: none;
	}
	.title {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 10px;
		border: 0;
		background: none;
		color: var(--text);
		font-weight: 700;
		font-size: 0.95rem;
		text-align: left;
		padding: 0;
	}
	.n {
		flex: none;
		width: 24px;
		height: 24px;
		border-radius: 50%;
		background: var(--bg);
		display: grid;
		place-items: center;
		font-size: 0.75rem;
	}
	.chev {
		margin-left: auto;
		color: var(--muted);
	}
	.points p {
		margin: 8px 0 0 32px;
		line-height: 1.5;
	}
</style>
