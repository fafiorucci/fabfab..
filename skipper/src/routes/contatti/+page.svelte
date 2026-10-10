<script lang="ts">
	import ModuleShell from '#lib/components/ModuleShell.svelte';
	import { persisted, uid } from '#lib/persist.svelte.ts';

	interface Contact {
		id: string;
		name: string;
		role: string;
		phone: string;
		vhf: string;
		note: string;
	}

	/** Numeri di emergenza italiani: fissi, non modificabili. */
	const EMERGENCY = [
		{ name: 'Guardia Costiera — emergenze in mare', phone: '1530', vhf: '16', note: 'Numero blu, gratuito, attivo 24 ore su 24' },
		{ name: 'Numero unico di emergenza', phone: '112', vhf: '', note: 'Soccorso sanitario, Carabinieri, Vigili del Fuoco' },
	];
	const ROLES = ['Marina / porto', 'Charter', 'Tecnico motore', 'Velaio', 'Elettronica', 'Equipaggio', 'Altro'];

	const store = persisted<Contact[]>('contatti', []);
	const blank = () => ({ name: '', role: ROLES[0], phone: '', vhf: '', note: '' });
	let draft = $state(blank());

	function add(e: SubmitEvent) {
		e.preventDefault();
		if (!draft.name.trim()) return;
		store.value = [...store.value, { id: uid(), ...draft }].toSorted((a, b) => a.role.localeCompare(b.role) || a.name.localeCompare(b.name));
		draft = blank();
	}

	const tel = (p: string) => `tel:${p.replace(/[^\d+]/g, '')}`;
</script>

<ModuleShell title="Contatti">
	<h1 class="m-h1">Contatti</h1>
	<p class="m-lead">Tocca un numero per chiamare. In mare aperto il canale VHF 16 resta il primo mezzo per chiedere soccorso.</p>

	<section class="m-card sos">
		<h2>Emergenza</h2>
		<ul class="m-list">
			{#each EMERGENCY as c (c.phone)}
				<li>
					<div class="row">
						<div><strong>{c.name}</strong><p class="m-muted">{c.note}</p></div>
						<div class="calls">
							<a class="call" href={tel(c.phone)}>{c.phone}</a>
							{#if c.vhf}<span class="m-tag">VHF {c.vhf}</span>{/if}
						</div>
					</div>
				</li>
			{/each}
		</ul>
		<p class="m-muted">
			Assistenza medica a bordo: <a href="https://www.cirm.it/" target="_blank" rel="noopener">CIRM — Centro Internazionale Radio Medico</a> (verifica e salva qui sotto i
			suoi recapiti prima di partire).
		</p>
	</section>

	<section class="m-card">
		<h2>I miei contatti</h2>
		{#if !store.value.length}<p class="m-muted">Aggiungi marina, charter, tecnici ed equipaggio.</p>{/if}
		<ul class="m-list">
			{#each store.value as c (c.id)}
				<li>
					<div class="row">
						<div>
							<strong>{c.name}</strong> <span class="m-tag">{c.role}</span>
							{#if c.note}<p class="m-muted">{c.note}</p>{/if}
						</div>
						<div class="calls">
							{#if c.phone}<a class="call" href={tel(c.phone)}>{c.phone}</a>{/if}
							{#if c.vhf}<span class="m-tag">VHF {c.vhf}</span>{/if}
							<button class="m-small-btn" onclick={() => (store.value = store.value.filter((x) => x.id !== c.id))} aria-label="Elimina">✕</button>
						</div>
					</div>
				</li>
			{/each}
		</ul>
	</section>

	<form class="m-card" onsubmit={add}>
		<h2>Nuovo contatto</h2>
		<div class="m-grid">
			<label class="m-field"><span>Nome</span><input bind:value={draft.name} required /></label>
			<label class="m-field"><span>Ruolo</span><select bind:value={draft.role}>{#each ROLES as r (r)}<option>{r}</option>{/each}</select></label>
			<label class="m-field"><span>Telefono</span><input type="tel" bind:value={draft.phone} /></label>
			<label class="m-field"><span>Canale VHF</span><input bind:value={draft.vhf} placeholder="Es. 9" /></label>
			<label class="m-field m-wide"><span>Note</span><input bind:value={draft.note} /></label>
		</div>
		<div class="m-actions"><button class="primary" type="submit">Aggiungi</button></div>
	</form>
</ModuleShell>

<style>
	.row {
		display: flex;
		justify-content: space-between;
		gap: 10px;
		align-items: center;
	}
	.row p {
		margin: 2px 0 0;
	}
	.calls {
		display: flex;
		align-items: center;
		gap: 6px;
		flex-wrap: wrap;
		justify-content: flex-end;
	}
	.call {
		background: var(--go);
		color: #fff;
		text-decoration: none;
		padding: 6px 12px;
		border-radius: 18px;
		font-weight: 700;
		white-space: nowrap;
	}
	.sos {
		border: 2px solid var(--nogo);
	}
	.sos .call {
		background: var(--nogo);
	}
</style>
