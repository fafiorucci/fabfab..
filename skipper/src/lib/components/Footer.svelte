<script lang="ts">
	import { BRAND } from '#lib/brand.ts';
	import { APP_VERSION } from '#lib/modules.ts';
</script>

<footer class="notes">
	<div class="org">
		{#if BRAND.logo}
			<img src={`./${BRAND.logo}`} alt={BRAND.org} />
		{:else}
			<span class="wordmark">{BRAND.org}</span>
		{/if}
		<span>{BRAND.app} — a cura di <b>{BRAND.author}</b></span>
	</div>

	<h2>Note e avvertenze</h2>
	<ul>
		<li>
			{BRAND.app} ha scopo esclusivamente informativo e di supporto alla pianificazione. Non sostituisce i bollettini ufficiali
			(<a href="https://www.meteoam.it/it/meteo-mare" target="_blank" rel="noopener">Meteomar – Aeronautica Militare</a>, avvisi
			della Guardia Costiera, NAVTEX) né il giudizio dello skipper, che resta l'unico responsabile della decisione di uscire in mare e
			della condotta della navigazione.
		</li>
		<li>
			Le previsioni dei modelli numerici sono stime: possono contenere errori e cambiare da un aggiornamento all'altro. Raffiche,
			effetti costieri, temporali e onda sottocosta possono differire anche di molto dai valori mostrati.
		</li>
		<li>
			Il semaforo è un aiuto calcolato in automatico sui limiti che hai impostato. Non tiene conto dello stato della barca,
			dell'equipaggio, dei ridossi né delle condizioni effettive in mare.
		</li>
		<li>L'autore declina ogni responsabilità per danni a persone o cose derivanti dall'uso dell'applicazione o dei dati che mostra.</li>
		<li>
			Fonti: dati <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> (CC BY 4.0) da modelli ECMWF, DWD,
			NOAA, Météo-France, Met Office e ItaliaMeteo-ARPAE. Mappe © OpenStreetMap, OpenFreeMap, Esri, OpenSeaMap.
		</li>
	</ul>
	<p class="copy">© {BRAND.year} {BRAND.author} · {BRAND.org} · versione {APP_VERSION}</p>
</footer>

<style>
	.notes {
		margin-top: 18px;
		padding-top: 14px;
		border-top: 1px solid var(--line-strong);
		font-size: 0.75rem;
		color: var(--muted);
		line-height: 1.45;
	}
	.org {
		display: flex;
		align-items: center;
		gap: 10px;
		flex-wrap: wrap;
		color: var(--text);
		font-size: 0.82rem;
	}
	.org img {
		height: 36px;
		width: auto;
	}
	.wordmark {
		font-weight: 800;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--brand-2);
		border: 2px solid currentColor;
		border-radius: 6px;
		padding: 2px 8px;
		font-size: 0.78rem;
	}
	@media (prefers-color-scheme: dark) {
		.wordmark {
			color: #5fc2d6;
		}
	}
	h2 {
		margin: 12px 0 4px;
		font-size: 0.8rem;
		color: var(--text);
	}
	ul {
		margin: 0;
		padding-left: 16px;
		display: grid;
		gap: 4px;
	}
	.copy {
		margin: 10px 0 0;
		font-weight: 600;
	}
</style>
