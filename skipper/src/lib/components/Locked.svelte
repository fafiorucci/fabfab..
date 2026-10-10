<script lang="ts">
	import { getContext, setContext, type Snippet } from 'svelte';
	import { DEMO } from '#lib/demo.ts';

	/** Nella demo mostra il contenuto sfocato e non cliccabile; nella versione completa lo mostra normalmente. */
	let { children, label = 'Disponibile nella versione completa', compact = false }: { children: Snippet; label?: string; compact?: boolean } = $props();

	// Un blocco dentro un altro blocco non sfoca due volte.
	const nested = getContext<boolean>('locked') === true;
	if (DEMO) setContext('locked', true);
</script>

{#if DEMO && !nested}
	<div class="locked" class:compact>
		<div class="content" inert aria-hidden="true">{@render children()}</div>
		<div class="badge"><span aria-hidden="true">🔒</span> {label}</div>
	</div>
{:else}
	{@render children()}
{/if}

<style>
	.locked {
		position: relative;
		min-height: 80px;
	}
	.content {
		filter: blur(2.5px) grayscale(0.6);
		opacity: 0.55;
		pointer-events: none;
		user-select: none;
	}
	.badge {
		position: absolute;
		top: 24px;
		left: 0;
		right: 0;
		margin: 0 auto;
		height: max-content;
		width: max-content;
		max-width: 90%;
		background: var(--brand);
		color: #fff;
		padding: 8px 14px;
		border-radius: 20px;
		font-weight: 600;
		font-size: 0.85rem;
		box-shadow: var(--shadow);
		text-align: center;
	}
	.locked.compact {
		min-height: 0;
	}
	.compact .badge {
		top: 0;
		bottom: 0;
		margin: auto;
	}
	.compact .badge {
		white-space: nowrap;
		font-size: 0.75rem;
		padding: 4px 10px;
	}
</style>
