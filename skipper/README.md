# Skipper Meteo

Webapp per valutare il meteo prima di un'uscita in mare: confronta più modelli sulla zona dell'uscita, mostra dove sono in disaccordo e dà un giudizio giorno per giorno (si esce / attenzione / meglio restare in porto) in base ai limiti della barca e dell'equipaggio.

Primo modulo della futura **Skipper WebApp**. Lo studio completo è in [`../docs/studio-skipper-meteo.md`](../docs/studio-skipper-meteo.md).

## Cosa fa (MVP 1)

- **Uscita**: porto o zona (ricerca), data, giorni (1–7), ampiezza area, limiti di vento, raffiche e onda, modelli da confrontare.
- **Mappa reale** chiara (OpenFreeMap) o satellite (Esri), con segnali nautici OpenSeaMap.
- **Animazione oraria** con barra del tempo: vento con particelle, raffiche, onda, pressione, pioggia.
- **6 modelli**: ECMWF IFS, ICON, GFS, ARPEGE/AROME, UKMO, ICON-2I (2 km); onda dal miglior modello marino.
- **Disaccordo tra modelli**: mappa della deviazione standard del vento tra i modelli.
- **Area inquadrata**: zoomando, minimo, media e massimo per modello sulla zona visibile (solo mare) e curve orarie a confronto.
- **Punto**: tocchi la mappa e ottieni il meteogramma di tutti i modelli e l'onda.
- **Valutazione**: semaforo per giorno, con il motivo (90° percentile su mare aperto, ore 7–20).
- **Invita**: link con tutta l'uscita dentro, da mandare agli amici (nessun account).
- **Report**: immagine PNG con mappa e semafori, condivisa con il menu nativo (WhatsApp, Mail, AirDrop) o scaricata.
- **PWA**: si installa sulla schermata Home; i dati e le mappe già visti restano disponibili offline.

## Sviluppo

```sh
npm install
npm run dev       # http://localhost:5173
npm run check     # controllo dei tipi
npm test          # test unitari
npm run build     # sito statico in build/
```

Per pubblicarlo in una sottocartella (es. GitHub Pages): `BASE_PATH=/nome-repo npm run build`.

## Dati e limiti

- Dati: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0), gratuito per **uso non commerciale**, entro circa 10.000 chiamate al giorno per rete. Ogni punto della griglia conta come chiamata: un'uscita con area ±1° e 6 modelli usa circa 600 chiamate. I risultati restano in memoria per la sessione.
- La griglia è a 0,25° (circa 15 miglia): il dettaglio dei modelli locali (ICON-2I, AROME) è quindi solo in parte sfruttato. Il passo successivo è un backend che legge i GRIB a piena risoluzione.
- Strumento di supporto: non sostituisce il bollettino ufficiale né il giudizio dello skipper.
