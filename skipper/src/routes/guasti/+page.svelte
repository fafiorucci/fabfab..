<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import { persisted, shareText, uid } from '#lib/persist.svelte.ts';

	type Priority = 'bassa' | 'media' | 'alta' | 'critica';
	type Status = 'aperto' | 'in corso' | 'risolto';

	interface Fault {
		id: string;
		created: string;
		title: string;
		system: string;
		priority: Priority;
		status: Status;
		description: string;
		fix: string;
	}

	const SYSTEMS = ['Motore', 'Impianto elettrico', 'Vele e manovre', 'Timone', 'Scafo e coperta', 'Idraulica e WC', 'Elettronica e strumenti', 'Ancora e salpancore', 'Gommone / fuoribordo', 'Altro'];
	const PRIORITIES: Priority[] = ['bassa', 'media', 'alta', 'critica'];
	const STATUSES: Status[] = ['aperto', 'in corso', 'risolto'];

	const store = persisted<Fault[]>('guasti', []);
	const blank = () => ({ title: '', system: SYSTEMS[0], priority: 'media' as Priority, description: '' });
	let draft = $state(blank());
	let filter: Status | 'tutti' = $state('tutti');
	let toast: string | null = $state(null);

	const list = $derived(
		store.value
			.filter((f) => filter === 'tutti' || f.status === filter)
			.toSorted((a, b) => PRIORITIES.indexOf(b.priority) - PRIORITIES.indexOf(a.priority) || b.created.localeCompare(a.created))
	);
	const openCount = $derived(store.value.filter((f) => f.status !== 'risolto').length);

	function add(e: SubmitEvent) {
		e.preventDefault();
		if (!draft.title.trim()) return;
		store.value = [{ id: uid(), created: new Date().toISOString(), status: 'aperto', fix: '', ...draft }, ...store.value];
		draft = blank();
	}

	function remove(id: string) {
		if (confirm('Eliminare la segnalazione?')) store.value = store.value.filter((f) => f.id !== id);
	}

	async function share() {
		const lines = ['Guasti a bordo', ''];
		for (const f of list)
			lines.push(
				`• [${f.priority.toUpperCase()}] ${f.title} — ${f.system} (${f.status})`,
				...(f.description ? [`  ${f.description}`] : []),
				...(f.fix ? [`  Intervento: ${f.fix}`] : [])
			);
		const r = await shareText('Guasti a bordo', lines.join('\n'));
		if (r === 'copied') {
			toast = 'Elenco copiato negli appunti';
			setTimeout(() => (toast = null), 2500);
		}
	}

	const fmtDate = (iso: string) => new Date(iso).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
</script>

<ModuleShell title="Guasti">
	{#snippet actions()}
		<button class="ghost" onclick={share} disabled={!list.length}>Condividi</button>
	{/snippet}

	<h1 class="m-h1">Guasti</h1>
	<p class="m-lead">{openCount ? `${openCount} da risolvere` : 'Nessun guasto aperto'} · i dati restano su questo dispositivo.</p>

	<form class="m-card" onsubmit={add}>
		<h2>Nuova segnalazione</h2>
		<div class="m-grid">
			<label class="m-field m-wide"><span>Cosa non va</span><input bind:value={draft.title} placeholder="Es. pompa di sentina non parte" required /></label>
			<label class="m-field">
				<span>Impianto</span>
				<select bind:value={draft.system}>{#each SYSTEMS as s (s)}<option>{s}</option>{/each}</select>
			</label>
			<label class="m-field">
				<span>Priorità</span>
				<select bind:value={draft.priority}>{#each PRIORITIES as p (p)}<option>{p}</option>{/each}</select>
			</label>
			<label class="m-field m-wide"><span>Descrizione</span><textarea rows="2" bind:value={draft.description} placeholder="Quando è successo, cosa hai già provato…"></textarea></label>
		</div>
		<div class="m-actions"><button class="primary" type="submit">Aggiungi</button></div>
	</form>

	<div class="filters">
		{#each ['tutti', ...STATUSES] as s (s)}
			<button class="m-small-btn" class:on={filter === s} onclick={() => (filter = s as Status | 'tutti')}>{s}</button>
		{/each}
	</div>

	<div class="m-card">
		{#if !list.length}
			<p class="m-muted">Nessuna segnalazione.</p>
		{:else}
			<ul class="m-list">
				{#each list as f (f.id)}
					<li class="fault {f.priority}">
						<div class="head">
							<strong>{f.title}</strong>
							<span class="m-tag prio">{f.priority}</span>
						</div>
						<p class="m-muted">{f.system} · {fmtDate(f.created)}</p>
						{#if f.description}<p>{f.description}</p>{/if}
						<div class="m-grid">
							<label class="m-field">
								<span>Stato</span>
								<select bind:value={f.status}>{#each STATUSES as s (s)}<option>{s}</option>{/each}</select>
							</label>
							<label class="m-field"><span>Intervento / tecnico</span><input bind:value={f.fix} placeholder="Chi, cosa, quando" /></label>
						</div>
						<div class="m-actions"><button class="m-small-btn" onclick={() => remove(f.id)}>Elimina</button></div>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
	{#if toast}<p class="m-muted">{toast}</p>{/if}
</ModuleShell>

<style>
	.filters {
		display: flex;
		gap: 6px;
		margin-bottom: 10px;
	}
	.filters :global(.on) {
		background: var(--brand-2);
		color: #fff;
		border-color: var(--brand-2);
	}
	.head {
		display: flex;
		justify-content: space-between;
		gap: 8px;
		align-items: center;
	}
	.fault p {
		margin: 2px 0 6px;
	}
	.fault {
		border-left: 4px solid var(--p);
		padding-left: 10px !important;
	}
	.bassa {
		--p: var(--line-strong);
	}
	.media {
		--p: var(--caution);
	}
	.alta {
		--p: var(--accent);
	}
	.critica {
		--p: var(--nogo);
	}
	.prio {
		background: var(--p);
		color: #fff;
	}
</style>
