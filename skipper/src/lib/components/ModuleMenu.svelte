<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { BRAND } from '#lib/brand.ts';
	import { APP_VERSION, MODULES } from '#lib/modules.ts';
	import { DEMO, DEMO_MODULES } from '#lib/demo.ts';

	/** Su schermi piccoli mostra solo il logo (l'intestazione ha altri comandi). */
	let { compact = false }: { compact?: boolean } = $props();
	let open = $state(false);
	const href = (p: string) => resolve(p as '/');
	const here = $derived(page.url.pathname.replace(/\/$/, ''));
	const current = $derived(MODULES.find((m) => href(m.path).replace(/\/$/, '') === here) ?? MODULES[0]);

	function onkey(e: KeyboardEvent) {
		if (e.key === 'Escape') open = false;
	}
</script>

<svelte:window onkeydown={onkey} />

<div class="mm" class:compact>
	<button class="logo-btn" onclick={() => (open = !open)} aria-expanded={open} aria-haspopup="menu" title="Moduli di {BRAND.app}">
		<img src="./{BRAND.logo}" alt={BRAND.org} width="34" height="34" />
		<span class="name">Skipper <b>{current.label}</b><small>{BRAND.org}</small></span>
		<svg class="caret" viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4.5 3 3 3-3" /></svg>
	</button>

	{#if open}
		<button class="scrim" aria-label="Chiudi menu" onclick={() => (open = false)}></button>
		<div class="menu" role="menu">
			<p class="menu-h">Skipper WebApp{#if DEMO}<span class="demo">Demo</span>{/if}</p>
			{#each MODULES as m (m.id)}
				{#if DEMO && !DEMO_MODULES.includes(m.id)}
					<span role="menuitem" class="off" aria-disabled="true" title="Disponibile nella versione completa">
						<span class="ic" aria-hidden="true">{m.icon}</span>
						<span><b>{m.label}</b><small>Versione completa</small></span>
						<span class="lock" aria-hidden="true">🔒</span>
					</span>
				{:else}
					<a role="menuitem" href={href(m.path)} class:on={m.id === current.id} onclick={() => (open = false)}>
						<span class="ic" aria-hidden="true">{m.icon}</span>
						<span><b>{m.label}</b><small>{m.desc}</small></span>
					</a>
				{/if}
			{/each}
			<p class="ver"><b>{BRAND.org}</b> · a cura di {BRAND.author}<br />Versione {APP_VERSION}{DEMO ? ' · demo' : ''}</p>
		</div>
	{/if}
</div>

<style>
	.mm {
		position: relative;
	}
	.logo-btn {
		display: flex;
		align-items: center;
		gap: 8px;
		border: 0;
		background: none;
		color: #fff;
		padding: 2px 4px;
		border-radius: 10px;
	}
	.logo-btn:hover {
		background: rgba(255, 255, 255, 0.08);
	}
	.logo-btn img {
		width: 34px;
		height: 34px;
		flex: none;
	}
	.name {
		display: grid;
		text-align: left;
		font-size: 1.02rem;
		white-space: nowrap;
		line-height: 1.1;
	}
	.name b {
		color: var(--accent);
	}
	.name small {
		font-size: 0.6rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #8fb4c8;
	}
	.caret {
		width: 12px;
		height: 12px;
		fill: none;
		stroke: #8fb4c8;
		stroke-width: 1.6;
	}
	.scrim {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.25);
		border: 0;
		z-index: 30;
	}
	.menu {
		position: absolute;
		top: calc(100% + 8px);
		left: 0;
		z-index: 31;
		width: min(320px, calc(100vw - 20px));
		background: var(--panel);
		color: var(--text);
		border-radius: 14px;
		box-shadow: var(--shadow);
		padding: 6px;
		display: grid;
		gap: 2px;
		/* Su schermi bassi il menu scorre con la sua barra verticale */
		max-height: calc(100dvh - 76px - env(safe-area-inset-top) - env(safe-area-inset-bottom));
		overflow-y: auto;
		overscroll-behavior: contain;
		-webkit-overflow-scrolling: touch;
		scrollbar-width: thin;
		scrollbar-color: var(--line-strong) transparent;
	}
	.menu::-webkit-scrollbar {
		width: 8px;
	}
	.menu::-webkit-scrollbar-thumb {
		background: var(--line-strong);
		border-radius: 8px;
	}
	.menu::-webkit-scrollbar-track {
		background: transparent;
		margin: 10px 0;
	}
	.menu-h {
		margin: 4px 8px 6px;
		font-size: 0.7rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--muted);
	}
	.menu a,
	.menu .off {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px;
		border-radius: 10px;
		color: var(--text);
		text-decoration: none;
	}
	.menu a:hover {
		background: var(--accent-soft);
	}
	.menu a.on {
		background: var(--accent-soft);
		box-shadow: inset 3px 0 0 var(--accent);
	}
	.menu a span:last-child,
	.off > span:nth-child(2) {
		display: grid;
	}
	.off {
		opacity: 0.45;
		cursor: not-allowed;
	}
	.lock {
		margin-left: auto;
		font-size: 0.8rem;
	}
	.demo {
		margin-left: 6px;
		background: var(--accent);
		color: #fff;
		border-radius: 6px;
		padding: 1px 6px;
	}
	.menu small {
		color: var(--muted);
		font-size: 0.75rem;
	}
	.ic {
		width: 30px;
		text-align: center;
		font-size: 1.25rem;
	}
	.ver {
		margin: 6px 8px 2px;
		font-size: 0.7rem;
		color: var(--muted);
		border-top: 1px solid var(--line);
		padding-top: 6px;
	}
	@media (max-width: 900px) {
		.name {
			font-size: 0.9rem;
		}
		.compact .name {
			display: none;
		}
	}
</style>
