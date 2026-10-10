<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import Locked from '#lib/components/Locked.svelte';
	import { persisted, shareText, uid } from '#lib/persist.svelte.ts';

	/** Controlli giornalieri del motore prima dell'accensione (High Five — Motore). */
	const CHECKS = [
		{ id: 'V', word: 'Visivo', what: 'Analisi visiva del vano motore: pulizia, integrità della vernice, niente oggetti o stracci vicino a cinghie e pulegge.' },
		{ id: 'W', word: 'Water', what: 'Livello del liquido di raffreddamento (a motore freddo) e pulizia del filtro dell’acqua di mare; presa a mare aperta.' },
		{ id: 'O', word: 'Oil', what: 'Livello e colore dell’olio motore e dell’olio del saildrive/invertitore. Olio lattiginoso = acqua nell’olio: non accendere.' },
		{ id: 'B1', word: 'Belt', what: 'Stato e tensione della cinghia di trasmissione: niente crepe o sfilacciature, flessione di circa 1 cm sotto il pollice.' },
		{ id: 'B2', word: 'Bilge', what: 'Sentina del motore pulita e asciutta: acqua, olio o gasolio indicano una perdita da cercare.' },
		{ id: 'L', word: 'Leaks', what: 'Trafilamenti di liquidi, corrosione o calcare su raccordi, fascette, pompa dell’acqua e scambiatore.' },
		{ id: 'E', word: 'Exhaust', what: 'Dopo l’accensione: frequenza e portata dello scarico di fumi e acqua salata. Se l’acqua non esce, spegnere subito.' }
	];

	interface Check {
		id: string;
		when: string;
		hours: string;
		status: Record<string, 'ok' | 'ko' | ''>;
		note: string;
	}

	const nowLocal = () => {
		const d = new Date();
		d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
		return d.toISOString().slice(0, 16);
	};
	const blank = (): Omit<Check, 'id'> => ({ when: nowLocal(), hours: '', status: Object.fromEntries(CHECKS.map((c) => [c.id, ''])), note: '' });

	const log = persisted<Check[]>('wobble', []);
	let draft = $state(blank());
	let toast: string | null = $state(null);

	const complete = $derived(CHECKS.every((c) => draft.status[c.id]));
	const problems = $derived(CHECKS.filter((c) => draft.status[c.id] === 'ko'));

	function save() {
		log.value = [{ id: uid(), ...$state.snapshot(draft) }, ...log.value];
		draft = blank();
		toast = 'Controllo salvato nel registro';
		setTimeout(() => (toast = null), 2500);
	}

	const label = (c: Check) => CHECKS.filter((x) => c.status[x.id] === 'ko').map((x) => x.word).join(', ');

	async function share() {
		const lines = ['Registro controlli WOBBLE', ''];
		for (const c of log.value) lines.push(`${c.when.replace('T', ' ')} · ${c.hours ? `${c.hours} h · ` : ''}${label(c) ? `PROBLEMI: ${label(c)}` : 'tutto ok'}${c.note ? ` — ${c.note}` : ''}`);
		const r = await shareText('Controlli WOBBLE', lines.join('\n'));
		if (r === 'copied') {
			toast = 'Copiato negli appunti';
			setTimeout(() => (toast = null), 2500);
		}
	}
</script>

<ModuleShell title="Controlli WOBBLE">
	<h1 class="m-h1">Controlli WOBBLE</h1>
	<p class="m-lead">Ogni mattina, a motore freddo, prima di accenderlo. Un controllo per lettera: <b>W</b>ater, <b>O</b>il, <b>B</b>elt, <b>B</b>ilge, <b>L</b>eaks, <b>E</b>xhaust.</p>

	<Locked label="Controlli WOBBLE nella versione completa">
		<section class="m-card">
			<div class="m-grid">
				<label class="m-field"><span>Data e ora</span><input type="datetime-local" bind:value={draft.when} /></label>
				<label class="m-field"><span>Ore motore</span><input type="number" step="0.1" min="0" bind:value={draft.hours} /></label>
			</div>
		</section>

		<ul class="checks">
			{#each CHECKS as c (c.id)}
				<li class={draft.status[c.id]}>
					<div class="letter">{c.word[0]}</div>
					<div class="body">
						<b>{c.word}</b>
						<p>{c.what}</p>
					</div>
					<div class="btns">
						<button class:on={draft.status[c.id] === 'ok'} class="okb" onclick={() => (draft.status[c.id] = 'ok')}>OK</button>
						<button class:on={draft.status[c.id] === 'ko'} class="kob" onclick={() => (draft.status[c.id] = 'ko')}>!</button>
					</div>
				</li>
			{/each}
		</ul>

		{#if problems.length}
			<p class="warn">Problemi su: {problems.map((p) => p.word).join(', ')}. Non partire finché lo skipper non ha valutato; se serve, apri una segnalazione nel modulo Guasti.</p>
		{/if}
		<label class="m-field"><span>Note</span><textarea rows="2" bind:value={draft.note}></textarea></label>
		<div class="m-actions">
			<button class="primary" onclick={save} disabled={!complete}>{complete ? 'Salva nel registro' : 'Completa tutti i controlli'}</button>
		</div>

		<section class="m-card log">
			<h2>Registro ({log.value.length})</h2>
			{#if !log.value.length}<p class="m-muted">Nessun controllo salvato.</p>{/if}
			<ul class="m-list">
				{#each log.value as c (c.id)}
					<li>
						<b>{new Date(c.when).toLocaleString('it-IT', { weekday: 'short', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })}</b>
						{#if c.hours}<span class="m-tag">{c.hours} h</span>{/if}
						<span class="res" class:bad={!!label(c)}>{label(c) ? `Problemi: ${label(c)}` : 'Tutto ok'}</span>
						{#if c.note}<p class="m-muted">{c.note}</p>{/if}
					</li>
				{/each}
			</ul>
			{#if log.value.length}<div class="m-actions"><button class="ghost" onclick={share}>Condividi registro</button></div>{/if}
		</section>
	</Locked>
	{#if toast}<p class="m-muted">{toast}</p>{/if}
</ModuleShell>

<style>
	.checks {
		list-style: none;
		margin: 0 0 10px;
		padding: 0;
		display: grid;
		gap: 8px;
	}
	.checks li {
		display: grid;
		grid-template-columns: 44px 1fr auto;
		gap: 10px;
		align-items: center;
		background: var(--panel);
		border-radius: 12px;
		padding: 10px;
		box-shadow: var(--shadow);
		border-left: 5px solid var(--line-strong);
	}
	.checks li.ok {
		border-left-color: var(--go);
	}
	.checks li.ko {
		border-left-color: var(--nogo);
	}
	.letter {
		width: 44px;
		height: 44px;
		border-radius: 10px;
		background: var(--brand-2);
		color: #fff;
		display: grid;
		place-items: center;
		font-size: 1.4rem;
		font-weight: 800;
	}
	.body p {
		margin: 2px 0 0;
		font-size: 0.85rem;
		color: var(--muted);
	}
	.btns {
		display: flex;
		gap: 4px;
	}
	.btns button {
		width: 44px;
		height: 38px;
		border-radius: 10px;
		border: 1px solid var(--line-strong);
		background: none;
		color: var(--text);
		font-weight: 800;
	}
	.okb.on {
		background: var(--go);
		border-color: var(--go);
		color: #fff;
	}
	.kob.on {
		background: var(--nogo);
		border-color: var(--nogo);
		color: #fff;
	}
	.warn {
		background: color-mix(in srgb, var(--nogo) 14%, transparent);
		padding: 8px 10px;
		border-radius: 10px;
	}
	.log {
		margin-top: 14px;
	}
	.res {
		margin-left: 6px;
		color: var(--go);
		font-weight: 600;
		font-size: 0.85rem;
	}
	.res.bad {
		color: var(--nogo);
	}
</style>
