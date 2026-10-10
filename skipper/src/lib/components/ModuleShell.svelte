<script lang="ts">
	import type { Snippet } from 'svelte';
	import '../../app.css';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import ModuleMenu from './ModuleMenu.svelte';
	import Footer from './Footer.svelte';
	import Locked from './Locked.svelte';
	import { DEMO, DEMO_MODULES } from '#lib/demo.ts';
	import { MODULES } from '#lib/modules.ts';

	interface Props {
		title: string;
		actions?: Snippet;
		children: Snippet;
		/** Contenuto a piena larghezza (es. mappa) invece della colonna centrale */
		wide?: boolean;
	}

	let { title, actions, children, wide = false }: Props = $props();

	const here = $derived(page.url.pathname.replace(/(\.html)?\/?$/, ''));
	const module = $derived(MODULES.find((m) => resolve(m.path as '/').replace(/\/$/, '') === here));
	/** Nella demo i moduli non dimostrativi si vedono ma non si usano. */
	const locked = $derived(DEMO && !!module && !DEMO_MODULES.includes(module.id));
</script>

<svelte:head>
	<title>{title} · Skipper</title>
</svelte:head>

<div class="shell">
	<header class="top">
		<ModuleMenu />
		<div class="spacer"></div>
		{#if actions && !locked}<div class="actions">{@render actions()}</div>{/if}
	</header>
	<main class:wide>
		{#if locked}
			<Locked label="{module?.label} è disponibile nella versione completa">{@render children()}</Locked>
		{:else}
			{@render children()}
		{/if}
		{#if !wide}<Footer />{/if}
	</main>
</div>

<style>
	.shell {
		min-height: 100dvh;
		display: flex;
		flex-direction: column;
	}
	.top {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 14px;
		padding-top: max(8px, env(safe-area-inset-top));
		background: var(--brand);
		color: #fff;
		border-bottom: 3px solid var(--accent);
		position: sticky;
		top: 0;
		z-index: 20;
	}
	.spacer {
		flex: 1;
	}
	.actions {
		display: flex;
		gap: 6px;
	}
	.actions :global(.ghost) {
		color: #fff;
		border-color: rgba(255, 255, 255, 0.3);
	}
	main {
		width: min(860px, 100%);
		margin: 0 auto;
		padding: 16px 14px 32px;
	}
	main.wide {
		width: 100%;
		padding: 0;
		flex: 1;
		display: flex;
		flex-direction: column;
	}
</style>
