<script lang="ts">
	import { persisted, shareText, uid } from '#lib/persist.svelte.ts';
	import Locked from './Locked.svelte';
	import { DEMO } from '#lib/demo.ts';

	export interface Ambito {
		title: string;
		items: string[];
		/** Suggerimento didattico per lo skipper */
		tip?: string;
		/** Tra gli "High Five": se non funziona la barca non lascia l'ormeggio */
		high5?: boolean;
	}
	export interface Group {
		title: string;
		intro?: string;
		ambiti: Ambito[];
	}

	interface Props {
		/** Chiave di salvataggio sul dispositivo */
		key: string;
		title: string;
		groups: Group[];
		/** Mostra in cima il blocco High Five con l'avvertenza */
		highFive?: boolean;
	}

	let { key, title, groups, highFive = false }: Props = $props();

	interface Data {
		/** Identificativo della sessione nell'archivio (assente finché non la si salva) */
		id?: string;
		checked: Record<string, boolean>;
		notes: Record<string, string>;
		meta: { when: string; boat: string; place: string; fuel: string; water: string; engine: string; remarks: string };
	}
	const empty = (): Data => ({ checked: {}, notes: {}, meta: { when: '', boat: '', place: '', fuel: '', water: '', engine: '', remarks: '' } });
	// svelte-ignore state_referenced_locally -- la chiave non cambia durante la vita del componente
	const store = persisted<Data>(key, empty());
	const d = $derived(store.value);

	/** Chiave di una voce: l'ambito la distingue (es. "Motore" compare sia fuori sia dentro). */
	const k = (a: Ambito, item: string) => `${a.title}::${item}`;
	const all = $derived(groups.flatMap((g) => g.ambiti.flatMap((a) => a.items.map((i) => k(a, i)))));
	const done = $derived(all.filter((i) => d.checked[i]).length);
	const high5 = $derived(groups.flatMap((g) => g.ambiti.filter((a) => a.high5)));
	const doneIn = (a: Ambito) => a.items.filter((i) => d.checked[k(a, i)]).length;
	const anchor = (t: string) => 'a-' + t.toLowerCase().replace(/[^a-z0-9]+/g, '-');

	let openNote: string | null = $state(null);
	let openTip: string | null = $state(null);
	let toast: string | null = $state(null);

	// ----- Sessioni: archivio dei check-in/check-out salvati sul dispositivo -----
	interface Saved {
		id: string;
		savedAt: string;
		data: Data;
	}
	// svelte-ignore state_referenced_locally
	const archive = persisted<Saved[]>(`${key}:sessioni`, []);
	let showArchive = $state(false);
	let fileInput: HTMLInputElement | undefined = $state();

	const hasContent = (x: Data) =>
		Object.values(x.checked).some(Boolean) || Object.values(x.notes).some(Boolean) || Object.values(x.meta).some(Boolean);
	const doneOf = (x: Data) => all.filter((i) => x.checked[i]).length;
	const fmtWhen = (w: string) => (w ? new Date(w).toLocaleString('it-IT', { dateStyle: 'short', timeStyle: 'short' }) : '');
	const titleOf = (x: Data) => [x.meta.boat || 'Barca senza nome', x.meta.place, fmtWhen(x.meta.when)].filter(Boolean).join(' · ');
	const saved = $derived(d.id ? archive.value.find((x) => x.id === d.id) : undefined);
	/** Confronto indipendente dall'ordine delle chiavi e dalle voci vuote o tolte. */
	const sig = (x: Data) => {
		const pick = (o: Record<string, unknown>) =>
			Object.keys(o)
				.filter((k) => o[k] !== false && o[k] !== '' && o[k] != null)
				.sort()
				.map((k) => [k, o[k]]);
		return JSON.stringify([pick(x.checked), pick(x.notes), pick(x.meta)]);
	};
	const dirty = $derived(!saved || sig(saved.data) !== sig(d));

	function flash(t: string) {
		toast = t;
		setTimeout(() => (toast = null), 2500);
	}

	/** Salva (o aggiorna) la sessione corrente nell'archivio. */
	function saveSession(quiet = false) {
		if (!store.value.id) store.value.id = uid();
		if (!store.value.meta.when) store.value.meta.when = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
		const data = $state.snapshot(store.value) as Data;
		archive.value = [{ id: data.id!, savedAt: new Date().toISOString(), data }, ...archive.value.filter((x) => x.id !== data.id)];
		if (!quiet) flash('Sessione salvata nell’archivio');
	}

	/** Chiude la sessione corrente e ne apre una vuota. */
	function newSession() {
		if (hasContent(d) && dirty) {
			if (confirm('Salvare la sessione corrente nell’archivio prima di iniziarne una nuova?')) saveSession(true);
			else if (!confirm('Le modifiche non salvate andranno perse. Continuare?')) return;
		}
		store.value = empty();
		flash('Nuova sessione');
	}

	function openSession(x: Saved) {
		if (x.id === d.id && !dirty) return void (showArchive = false);
		if (hasContent(d) && dirty && confirm('La sessione aperta ha modifiche non salvate: salvarle prima di aprire l’altra?')) saveSession(true);
		store.value = $state.snapshot(x.data) as Data;
		showArchive = false;
		flash(`Aperta: ${titleOf(x.data)}`);
	}

	function duplicateSession(x: Saved) {
		const data = $state.snapshot(x.data) as Data;
		data.id = undefined;
		data.checked = {};
		data.meta = { ...data.meta, when: '', fuel: '', water: '', engine: '', remarks: '' };
		data.notes = {};
		if (hasContent(d) && dirty) saveSession(true);
		store.value = data;
		showArchive = false;
		flash('Nuova sessione con gli stessi dati della barca');
	}

	function deleteSession(x: Saved) {
		if (!confirm(`Eliminare la sessione «${titleOf(x.data)}»?`)) return;
		archive.value = archive.value.filter((y) => y.id !== x.id);
		if (d.id === x.id) store.value.id = undefined;
	}

	/** Esporta tutte le sessioni in un file, da conservare o da aprire su un altro dispositivo. */
	function exportFile() {
		if (dirty && hasContent(d)) saveSession(true);
		const blob = new Blob([JSON.stringify({ app: 'skipper', kind: key, title, exported: new Date().toISOString(), sessions: archive.value }, null, 1)], {
			type: 'application/json'
		});
		const a = document.createElement('a');
		a.href = URL.createObjectURL(blob);
		a.download = `${key}-sessioni-${new Date().toISOString().slice(0, 10)}.json`;
		a.click();
		setTimeout(() => URL.revokeObjectURL(a.href), 2000);
	}

	async function importFile(e: Event) {
		const f = (e.currentTarget as HTMLInputElement).files?.[0];
		if (!f) return;
		try {
			const j = JSON.parse(await f.text());
			if (j.app !== 'skipper' || !Array.isArray(j.sessions)) throw new Error();
			if (j.kind !== key && !confirm(`Il file contiene sessioni di «${j.title ?? j.kind}». Importarle comunque qui?`)) return;
			const incoming = (j.sessions as Saved[]).filter((x) => x?.id && x.data?.checked && x.data?.meta);
			const ids = new Set(incoming.map((x) => x.id));
			archive.value = [...incoming, ...archive.value.filter((x) => !ids.has(x.id))].sort((a, b) => b.savedAt.localeCompare(a.savedAt));
			showArchive = true;
			flash(`${incoming.length} sessioni importate`);
		} catch {
			alert('File non valido: scegli un file di sessioni esportato da Skipper.');
		} finally {
			(e.currentTarget as HTMLInputElement).value = '';
		}
	}

	async function share(x: Data = d) {
		const m = x.meta;
		const lines = [
			`${title} — ${m.boat || 'barca'}`,
			[m.when && `Data: ${m.when.replace('T', ' ')}`, m.place && `Luogo: ${m.place}`].filter(Boolean).join(' · '),
			[m.fuel && `Carburante ${m.fuel}%`, m.water && `Acqua ${m.water}%`, m.engine && `Contaore ${m.engine} h`].filter(Boolean).join(' · '),
			`Completate ${doneOf(x)}/${all.length} voci`
		].filter(Boolean);
		for (const g of groups) {
			lines.push('', `=== ${g.title.toUpperCase()} ===`);
			for (const a of g.ambiti) {
				lines.push(`■ ${a.title}${a.high5 ? ' (HIGH FIVE)' : ''}`);
				for (const i of a.items) lines.push(`${x.checked[k(a, i)] ? '✔' : '✘'} ${i}${x.notes[k(a, i)] ? ` — ${x.notes[k(a, i)]}` : ''}`);
			}
		}
		if (m.remarks) lines.push('', `Note e danni: ${m.remarks}`);
		const r = await shareText(title, lines.join('\n'));
		if (r === 'copied') flash('Testo copiato negli appunti');
	}
</script>

{#snippet ambitoCard(a: Ambito)}
	<section class="card" id={anchor(a.title)} class:h5={a.high5}>
		<h3>
			<span>{a.title}{#if a.high5}<span class="h5tag">High Five</span>{/if}</span>
			<small>{doneIn(a)}/{a.items.length}</small>
		</h3>
		{#if a.tip}
			<button class="tip-btn" onclick={() => (openTip = openTip === a.title ? null : a.title)}>💡 Suggerimento didattico</button>
			{#if openTip === a.title}<p class="tip">{a.tip}</p>{/if}
		{/if}
		<ul>
			{#each a.items as item (item)}
				{@const id = k(a, item)}
				<li class:ok={d.checked[id]}>
					<label class="row">
						<input type="checkbox" bind:checked={d.checked[id]} />
						<span>{item}</span>
					</label>
					<button class="note-btn" class:has={!!d.notes[id]} onclick={() => (openNote = openNote === id ? null : id)} aria-label="Nota">✎</button>
					{#if openNote === id || d.notes[id]}
						<input class="note" placeholder="Nota (es. graffio a dritta, da sostituire…)" bind:value={d.notes[id]} />
					{/if}
				</li>
			{/each}
		</ul>
	</section>
{/snippet}

{#if highFive && high5.length}
	<section class="hf">
		<h2>High Five — da verificare subito</h2>
		<p>
			All'inizio del check-in verifica immediatamente salpa ancora, sentine, batterie, motore e timoneria.
			<b>Se uno di questi non è in perfetto stato di funzionamento, la barca non è titolata a lasciare l'ormeggio</b>: comunica subito il
			problema all'armatore perché venga riparato.
		</p>
		<div class="hf-list">
			{#each high5 as a (a.title)}
				<a href="#{anchor(a.title)}" class:ok={doneIn(a) === a.items.length}>
					<b>{a.title}</b><small>{doneIn(a)}/{a.items.length}</small>
				</a>
			{/each}
		</div>
		<details class="guide">
			<summary>Principi e linee guida</summary>
			<ul>
				<li>Fare il check-in il prima possibile e con metodo.</li>
				<li>Richiedere subito interventi o sostituzioni necessarie.</li>
				<li>Segnare malfunzionamenti o mancanze sulla checklist ufficiale prima di firmarla.</li>
				<li><b>Priorità:</b> prima gli High Five.</li>
				<li><b>Procedere per zone:</b> prima fuori, poi dentro, da prua a poppa.</li>
				<li><b>Guardare, poi trovare:</b> aprire tutto e guardare, poi spuntare la lista.</li>
			</ul>
		</details>
		{#if DEMO}
			{#each high5 as a (a.title)}{@render ambitoCard(a)}{/each}
		{/if}
	</section>
{/if}

<Locked label="Checklist completa, Safety plan e verbale nella versione completa">
	<section class="card session">
		<div class="s-head">
			<div class="s-title">
				<small>Sessione {d.id ? '' : 'nuova'}</small>
				<b>{hasContent(d) ? titleOf(d) : 'Nessun dato inserito'}</b>
				<span class="s-state" class:warn={dirty && hasContent(d)}>
					{#if saved && !dirty}Salvata il {fmtWhen(saved.savedAt)}{:else if hasContent(d)}Modifiche non salvate in archivio{:else}Compila e poi salva{/if}
				</span>
			</div>
			<div class="s-actions">
				<button class="primary small" onclick={() => saveSession()} disabled={!hasContent(d) || !dirty}>Salva</button>
				<button class="ghost small" onclick={newSession}>Nuova</button>
				<button class="ghost small" onclick={() => (showArchive = !showArchive)} aria-expanded={showArchive}>Archivio ({archive.value.length})</button>
			</div>
		</div>
		{#if showArchive}
			<div class="archive">
				{#if archive.value.length}
					<ul>
						{#each archive.value as x (x.id)}
							<li class:current={x.id === d.id}>
								<button class="s-open" onclick={() => openSession(x)}>
									<b>{titleOf(x.data)}</b>
									<small>{doneOf(x.data)}/{all.length} voci · salvata {fmtWhen(x.savedAt)}{x.id === d.id ? ' · aperta' : ''}</small>
								</button>
								<span class="s-row">
									<button class="ghost small" onclick={() => share(x.data)} title="Condividi il verbale">Verbale</button>
									<button class="ghost small" onclick={() => duplicateSession(x)} title="Nuova sessione con la stessa barca">Duplica</button>
									<button class="ghost small danger" onclick={() => deleteSession(x)} aria-label="Elimina">✕</button>
								</span>
							</li>
						{/each}
					</ul>
				{:else}
					<p class="m-muted">Nessuna sessione salvata. Premi «Salva» per conservare questo {title.toLowerCase()} e ritrovarlo qui.</p>
				{/if}
				<div class="s-file">
					<button class="ghost small" onclick={exportFile} disabled={!archive.value.length && !hasContent(d)}>Esporta file</button>
					<button class="ghost small" onclick={() => fileInput?.click()}>Importa file</button>
					<input bind:this={fileInput} type="file" accept="application/json,.json" hidden onchange={importFile} />
					<small>Il file serve come copia di sicurezza o per passare le sessioni su un altro dispositivo.</small>
				</div>
			</div>
		{/if}
	</section>

	<section class="card meta">
		<div class="grid">
			<label><span>Data e ora</span><input type="datetime-local" bind:value={d.meta.when} /></label>
			<label><span>Barca</span><input bind:value={d.meta.boat} placeholder="Nome / modello" /></label>
			<label><span>Luogo</span><input bind:value={d.meta.place} placeholder="Marina" /></label>
			<label><span>Carburante %</span><input type="number" min="0" max="100" bind:value={d.meta.fuel} /></label>
			<label><span>Acqua %</span><input type="number" min="0" max="100" bind:value={d.meta.water} /></label>
			<label><span>Contaore motore</span><input type="number" min="0" step="0.1" bind:value={d.meta.engine} /></label>
		</div>
		<div class="progress" aria-label="Avanzamento"><span style="width: {all.length ? (done / all.length) * 100 : 0}%"></span></div>
		<p class="count">{done} di {all.length} voci controllate</p>
	</section>

	{#each groups as g (g.title)}
		<h2 class="group">{g.title}</h2>
		{#if g.intro}<p class="intro">{g.intro}</p>{/if}
		{#each g.ambiti as a (a.title)}{@render ambitoCard(a)}{/each}
	{/each}

	<section class="card">
		<h3>Note e danni</h3>
		<textarea rows="4" bind:value={d.meta.remarks} placeholder="Descrivi eventuali danni o mancanze (consiglio: scatta anche delle foto)."></textarea>
	</section>

	<div class="bar">
		<button class="ghost" onclick={newSession}>Nuova sessione</button>
		<button class="ghost" onclick={() => saveSession()} disabled={!hasContent(d) || !dirty}>Salva sessione</button>
		<button class="primary" onclick={() => share()}>Condividi verbale</button>
	</div>
</Locked>
{#if toast}<p class="toast">{toast}</p>{/if}

<style>
	button.small {
		padding: 5px 10px;
		font-size: 0.82rem;
	}
	.session {
		border-left: 5px solid var(--brand-2);
	}
	.s-head {
		display: flex;
		gap: 10px;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
	}
	.s-title {
		display: grid;
		min-width: 0;
	}
	.s-title small {
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--muted);
	}
	.s-title b {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.s-state {
		font-size: 0.8rem;
		color: var(--go);
	}
	.s-state.warn {
		color: var(--caution);
	}
	.s-actions,
	.s-row,
	.s-file {
		display: flex;
		gap: 6px;
		flex-wrap: wrap;
		align-items: center;
	}
	.archive {
		margin-top: 10px;
		border-top: 1px solid var(--line);
		padding-top: 8px;
	}
	.archive ul {
		list-style: none;
		margin: 0 0 8px;
		padding: 0;
		display: grid;
		gap: 6px;
		max-height: 320px;
		overflow-y: auto;
	}
	.archive li {
		display: flex;
		gap: 8px;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		border: 1px solid var(--line);
		border-radius: 10px;
		padding: 6px 8px;
	}
	.archive li.current {
		border-color: var(--brand-2);
		background: var(--accent-soft);
	}
	.s-open {
		display: grid;
		text-align: left;
		border: 0;
		background: none;
		color: var(--text);
		padding: 0;
		flex: 1;
		min-width: 180px;
	}
	.s-open small,
	.s-file small {
		color: var(--muted);
		font-size: 0.75rem;
	}
	.danger {
		color: var(--nogo);
	}
	.card {
		background: var(--panel);
		border-radius: 14px;
		padding: 12px 14px;
		margin-bottom: 12px;
		box-shadow: var(--shadow);
		scroll-margin-top: 70px;
	}
	.card.h5 {
		border-left: 5px solid var(--accent);
	}
	h3 {
		margin: 0 0 6px;
		font-size: 1rem;
		display: flex;
		justify-content: space-between;
		gap: 8px;
	}
	h3 small {
		color: var(--muted);
		font-weight: 500;
	}
	.h5tag {
		margin-left: 8px;
		font-size: 0.65rem;
		font-weight: 800;
		text-transform: uppercase;
		background: var(--accent);
		color: #fff;
		padding: 2px 7px;
		border-radius: 10px;
		vertical-align: middle;
	}
	h2.group {
		margin: 18px 0 8px;
		font-size: 1.05rem;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--brand-2);
		border-bottom: 2px solid var(--brand-2);
		padding-bottom: 4px;
	}
	.intro {
		margin: -2px 0 10px;
		color: var(--muted);
		font-size: 0.88rem;
	}
	.hf {
		background: color-mix(in srgb, var(--accent) 10%, var(--panel));
		border: 2px solid var(--accent);
		border-radius: 16px;
		padding: 12px 14px;
		margin-bottom: 14px;
	}
	.hf h2 {
		margin: 0 0 4px;
		font-size: 1.05rem;
	}
	.hf p {
		margin: 0 0 8px;
		font-size: 0.9rem;
	}
	.hf-list {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}
	.hf-list a {
		display: grid;
		text-decoration: none;
		color: var(--text);
		background: var(--panel);
		border: 1px solid var(--line-strong);
		border-radius: 10px;
		padding: 6px 10px;
		font-size: 0.85rem;
	}
	.hf-list a.ok {
		border-color: var(--go);
		background: color-mix(in srgb, var(--go) 14%, var(--panel));
	}
	.hf-list small {
		color: var(--muted);
	}
	.guide {
		margin-top: 8px;
		font-size: 0.88rem;
	}
	.guide ul {
		margin: 6px 0 0;
		padding-left: 18px;
	}
	.tip-btn {
		border: 0;
		background: none;
		color: var(--brand-2);
		font-size: 0.8rem;
		padding: 0 0 4px;
	}
	.tip {
		margin: 0 0 6px;
		padding: 8px 10px;
		border-radius: 8px;
		background: color-mix(in srgb, var(--caution) 14%, transparent);
		font-size: 0.85rem;
		font-style: italic;
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
