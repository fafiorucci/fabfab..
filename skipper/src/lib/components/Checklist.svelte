<script lang="ts">
	import { persisted, shareText } from '#lib/persist.svelte.ts';

	export interface Section {
		title: string;
		items: string[];
	}

	interface Props {
		/** Chiave di salvataggio sul dispositivo */
		key: string;
		title: string;
		sections: Section[];
	}

	let { key, title, sections }: Props = $props();

	interface Data {
		checked: Record<string, boolean>;
		notes: Record<string, string>;
		meta: { when: string; boat: string; place: string; fuel: string; water: string; engine: string; remarks: string };
	}
	const empty = (): Data => ({ checked: {}, notes: {}, meta: { when: '', boat: '', place: '', fuel: '', water: '', engine: '', remarks: '' } });
	// svelte-ignore state_referenced_locally -- la chiave non cambia durante la vita del componente
	const store = persisted<Data>(key, empty());
	const d = $derived(store.value);

	const all = $derived(sections.flatMap((s) => s.items));
	const done = $derived(all.filter((i) => d.checked[i]).length);
	let openNote: string | null = $state(null);
	let toast: string | null = $state(null);

	function reset() {
		if (confirm('Azzerare la checklist?')) store.value = empty();
	}

	async function share() {
		const m = d.meta;
		const lines = [
			`${title} — ${m.boat || 'barca'}`,
			[m.when && `Data: ${m.when.replace('T', ' ')}`, m.place && `Luogo: ${m.place}`].filter(Boolean).join(' · '),
			[m.fuel && `Carburante ${m.fuel}%`, m.water && `Acqua ${m.water}%`, m.engine && `Contaore ${m.engine} h`].filter(Boolean).join(' · '),
			`Completate ${done}/${all.length} voci`,
			''
		];
		for (const s of sections) {
			lines.push(`■ ${s.title}`);
			for (const i of s.items) lines.push(`${d.checked[i] ? '✔' : '✘'} ${i}${d.notes[i] ? ` — ${d.notes[i]}` : ''}`);
			lines.push('');
		}
		if (m.remarks) lines.push(`Note e danni: ${m.remarks}`);
		const r = await shareText(title, lines.filter((l, k) => l !== '' || k > 3).join('\n'));
		if (r === 'copied') flash('Testo copiato negli appunti');
	}

	function flash(t: string) {
		toast = t;
		setTimeout(() => (toast = null), 2500);
	}
</script>

<section class="card meta">
	<div class="grid">
		<label><span>Data e ora</span><input type="datetime-local" bind:value={d.meta.when} /></label>
		<label><span>Barca</span><input bind:value={d.meta.boat} placeholder="Nome / modello" /></label>
		<label><span>Luogo</span><input bind:value={d.meta.place} placeholder="Marina" /></label>
		<label><span>Carburante %</span><input type="number" min="0" max="100" bind:value={d.meta.fuel} /></label>
		<label><span>Acqua %</span><input type="number" min="0" max="100" bind:value={d.meta.water} /></label>
		<label><span>Contaore motore</span><input type="number" min="0" step="0.1" bind:value={d.meta.engine} /></label>
	</div>
	<div class="progress" aria-label="Avanzamento">
		<span style="width: {all.length ? (done / all.length) * 100 : 0}%"></span>
	</div>
	<p class="count">{done} di {all.length} voci controllate</p>
</section>

{#each sections as s (s.title)}
	<section class="card">
		<h2>{s.title} <small>{s.items.filter((i) => d.checked[i]).length}/{s.items.length}</small></h2>
		<ul>
			{#each s.items as item (item)}
				<li class:ok={d.checked[item]}>
					<label class="row">
						<input type="checkbox" bind:checked={d.checked[item]} />
						<span>{item}</span>
					</label>
					<button class="note-btn" class:has={!!d.notes[item]} onclick={() => (openNote = openNote === item ? null : item)} aria-label="Nota">✎</button>
					{#if openNote === item || d.notes[item]}
						<input class="note" placeholder="Nota (es. graffio a dritta, da sostituire…)" bind:value={d.notes[item]} />
					{/if}
				</li>
			{/each}
		</ul>
	</section>
{/each}

<section class="card">
	<h2>Note e danni</h2>
	<textarea rows="4" bind:value={d.meta.remarks} placeholder="Descrivi eventuali danni o mancanze (consiglio: scatta anche delle foto)."></textarea>
</section>

<div class="bar">
	<button class="ghost" onclick={reset}>Azzera</button>
	<button class="primary" onclick={share}>Condividi verbale</button>
</div>
{#if toast}<p class="toast">{toast}</p>{/if}

<style>
	.card {
		background: var(--panel);
		border-radius: 14px;
		padding: 12px 14px;
		margin-bottom: 12px;
		box-shadow: var(--shadow);
	}
	h2 {
		margin: 0 0 8px;
		font-size: 1rem;
		display: flex;
		justify-content: space-between;
	}
	h2 small {
		color: var(--muted);
		font-weight: 500;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
		gap: 10px;
	}
	label span {
		display: block;
		font-size: 0.75rem;
		color: var(--muted);
		font-weight: 600;
		margin-bottom: 2px;
	}
	input:not([type='checkbox']),
	textarea {
		width: 100%;
		padding: 8px 10px;
		border-radius: 8px;
		border: 1px solid var(--line-strong);
		background: var(--bg);
		color: var(--text);
		font: inherit;
	}
	.progress {
		margin-top: 12px;
		height: 8px;
		background: var(--bg);
		border-radius: 4px;
		overflow: hidden;
	}
	.progress span {
		display: block;
		height: 100%;
		background: var(--go);
		transition: width 0.2s;
	}
	.count {
		margin: 4px 0 0;
		font-size: 0.8rem;
		color: var(--muted);
	}
	ul {
		list-style: none;
		margin: 0;
		padding: 0;
	}
	li {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: center;
		gap: 4px 8px;
		padding: 6px 0;
		border-top: 1px solid var(--line);
	}
	li:first-child {
		border-top: 0;
	}
	.row {
		display: flex;
		align-items: center;
		gap: 10px;
		cursor: pointer;
	}
	.row input {
		width: 22px;
		height: 22px;
		flex: none;
	}
	li.ok .row span {
		color: var(--muted);
	}
	.note-btn {
		border: 0;
		background: none;
		color: var(--muted);
		font-size: 1rem;
		padding: 4px 8px;
	}
	.note-btn.has {
		color: var(--accent);
	}
	.note {
		grid-column: 1 / -1;
		font-size: 0.85rem;
	}
	.bar {
		position: sticky;
		bottom: 0;
		display: flex;
		justify-content: flex-end;
		gap: 8px;
		padding: 10px 0;
		background: linear-gradient(transparent, var(--bg) 30%);
	}
	.toast {
		text-align: center;
		color: var(--muted);
	}
</style>
