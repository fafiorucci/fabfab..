# Skipper Meteo

Webapp per valutare il meteo prima di un'uscita in mare: confronta più modelli sulla zona dell'uscita, mostra dove sono in disaccordo e dà un giudizio giorno per giorno (si esce / attenzione / meglio restare in porto) in base ai limiti della barca e dell'equipaggio.

Primo modulo della futura **Skipper WebApp**. Lo studio completo è in [`../docs/studio-skipper-meteo.md`](../docs/studio-skipper-meteo.md).

## Moduli (versione 0.4.0)

Si scelgono dal menu nel logo. Il registro delle versioni è in [`CHANGELOG.md`](CHANGELOG.md).

- **Meteo**: confronto di 17 modelli sulla zona inquadrata, semaforo per giorno, disaccordo tra modelli, valori nel punto toccato, sinottica con isobare animate e analisi ufficiale DWD, report e link di invito.
- **Rotta**: weather routing a isocrone con polari tipo o importate (.pol/.txt/.csv), rendimento e motore.
- **Check-in / Check-out**: checklist con note e verbale condivisibile.
- **Guasti**: segnalazioni con impianto, priorità e stato.
- **Log book**: annotazioni con posizione GPS, esportazione CSV.
- **Contatti**: numeri di emergenza (1530, 112) e contatti personali.
- **Emergenze**: posizione GPS in gradi e primi, testo MAYDAY precompilato, procedure uomo a mare, incendio, via d'acqua, abbandono, PAN-PAN.

I dati dei moduli di bordo restano sul dispositivo (localStorage).

## Sviluppo

```sh
npm install
npm run dev       # http://localhost:5173
npm run check     # controllo dei tipi
npm test          # test unitari
npm run build     # sito statico in build/
```

Per pubblicarlo in una sottocartella: `BASE_PATH=/nome-repo/skipper npm run build`.

## Pubblicazione

Il workflow `.github/workflows/pages.yml` controlla e compila l'app a ogni PR. A ogni push su `main` la pubblica su GitHub Pages: la pagina meteo semplice va alla radice del sito, Skipper Meteo va sotto `/skipper/`.
Una tantum, nelle impostazioni del repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Dati e limiti

- Dati: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0), gratuito per **uso non commerciale**, entro circa 10.000 chiamate al giorno per rete. Ogni punto della griglia conta come chiamata: un'uscita con area ±1° e 6 modelli usa circa 600 chiamate. I risultati restano in memoria per la sessione.
- La griglia è a 0,25° (circa 15 miglia): il dettaglio dei modelli locali (ICON-2I, AROME) è quindi solo in parte sfruttato. Il passo successivo è un backend che legge i GRIB a piena risoluzione.
- Strumento di supporto: non sostituisce il bollettino ufficiale né il giudizio dello skipper.
