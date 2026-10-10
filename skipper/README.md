# Skipper WebApp

Webapp di Onda Portante, a cura di Fabrizio Fiorucci. Valuta il meteo prima di un'uscita in mare: confronta più modelli sulla zona dell'uscita, mostra dove sono in disaccordo e dà un giudizio giorno per giorno (si esce / attenzione / meglio restare in porto) in base ai limiti della barca e dell'equipaggio. Comprende i moduli di bordo: check-in, safety plan, briefing, controlli motore, memo dello skipper.

Nato come **Skipper Meteo**. Lo studio completo è in [`../docs/studio-skipper-meteo.md`](../docs/studio-skipper-meteo.md).

## Moduli (versione 0.5.0)

Si scelgono dal menu nel logo. Il registro delle versioni è in [`CHANGELOG.md`](CHANGELOG.md).

- **Meteo**: confronto di 17 modelli sulla zona inquadrata (partenza predefinita: Fiumicino), semaforo per giorno, disaccordo tra modelli, valori nel punto toccato, isobare animate, report e link di invito.
- **Carte sinottiche**: isobare e centri di alta e bassa pressione su Europa e Mediterraneo ogni 12 ore, fino a 3 modelli sovrapposti; analisi ufficiale DWD e collegamenti a Met Office e Aeronautica Militare.
- **Rotta**: weather routing a isocrone con polari tipo o importate (.pol/.txt/.csv), rendimento e motore.
- **Check-in**: documenti, poi esterno e interno, con l'**High Five** (salpa ancora, sentine, batterie, motore, timoneria) in evidenza; verbale condivisibile. **Check-out** con la stessa struttura.
- **Safety plan**: pianta della barca (tipi di scafo o foto propria) su cui segnare batterie, serbatoi, prese a mare, estintori, pronto soccorso, attrezzi; condivisibile come immagine.
- **Briefing equipaggio**: vita di bordo e sicurezza, da spuntare e mandare all'equipaggio.
- **Controlli WOBBLE**: controlli giornalieri del motore con registro.
- **Skipper memo**: COLREG, IALA, bandiere e alfabeto, Beaufort e Douglas, VHF, MARPOL.
- **Guasti**: segnalazioni con impianto, priorità e stato.
- **Log book**: annotazioni con posizione GPS, esportazione CSV.
- **Contatti**: numeri di emergenza (1530, 112) e contatti personali.
- **Emergenze**: posizione GPS in gradi e primi, testo MAYDAY precompilato, procedure uomo a mare, incendio, via d'acqua, abbandono, PAN-PAN.

I dati dei moduli di bordo restano sul dispositivo (localStorage).

## Versione completa e demo

Il sito pubblico (GitHub Pages) contiene solo la **demo**: meteo su una zona di esempio, carte sinottiche e l'High Five del check-in; gli altri moduli si vedono ma sono bloccati. La **versione completa** per ora si usa in locale:

```sh
npm install
npm run dev         # versione completa su http://localhost:5173
npm run dev:demo    # come appare la demo
npm run check       # controllo dei tipi
npm test            # test unitari
npm run build       # sito statico completo in build/
npm run build:demo  # sito statico della demo in build/
```

Attenzione: il repository è pubblico, quindi il codice della versione completa è comunque leggibile da chiunque.

Per pubblicarlo in una sottocartella: `BASE_PATH=/nome-repo/skipper npm run build`.

## Pubblicazione

Il workflow `.github/workflows/pages.yml` controlla e compila l'app a ogni PR. A ogni push su `main` pubblica la **demo** su GitHub Pages: la pagina meteo semplice va alla radice del sito, Skipper va sotto `/skipper/`.
Una tantum, nelle impostazioni del repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Dati e limiti

- Dati: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0), gratuito per **uso non commerciale**, entro circa 10.000 chiamate al giorno per rete. Ogni punto della griglia conta come chiamata: un'uscita con area ±1° e 6 modelli usa circa 600 chiamate. I risultati restano in memoria per la sessione.
- La griglia è a 0,25° (circa 15 miglia): il dettaglio dei modelli locali (ICON-2I, AROME) è quindi solo in parte sfruttato. Il passo successivo è un backend che legge i GRIB a piena risoluzione.
- Strumento di supporto: non sostituisce il bollettino ufficiale né il giudizio dello skipper.
