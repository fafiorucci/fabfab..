<script lang="ts">
	import type { Snippet } from 'svelte';
	import { DEMO } from '#lib/demo.ts';

	/** Nella demo mostra il contenuto sfocato e non cliccabile; nella versione completa lo mostra normalmente. */
	let { children, label = 'Disponibile nella versione completa', compact = false }: { children: Snippet; label?: string; compact?: boolean } = $props();
</script>

{#if DEMO}
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
		inset: 0;
		margin: auto;
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
	.compact .badge {
		font-size: 0.75rem;
		padding: 4px 10px;
	}
</style>
