# Studio di progetto — Skipper Meteo (futura Skipper WebApp)

> Documento di lavoro da discutere insieme. Le sezioni marcate **[DA DECIDERE]** sono le scelte che servono per partire.

## 1. Obiettivo

Una webapp che accompagni lo skipper nella **decisione di uscire in mare**, dalla situazione sinottica fino al dettaglio locale. Non è solo "vedere il vento".

- **Input:** zona e porto di partenza (eventuale rotta o tappe), **data di uscita**, **numero di giorni**, barca e limiti personali (vento massimo, onda massima, esperienza dell'equipaggio).
- **Output:** per ogni giorno e fascia oraria un giudizio **Vai / Attenzione / Non uscire**, motivato e confrontato tra i modelli. Il giudizio si può condividere con l'equipaggio e si può esportare come report.
- **Il valore aggiunto rispetto a Windy:**
  1. Le **carte sinottiche** dei principali centri meteo sono integrate nello stesso flusso.
  2. I modelli sono **sovrapposti e confrontati** e mostrano l'**accordo o disaccordo sull'area inquadrata**: zoomi e vedi subito quanto sono concordi i modelli lì.
  3. Un **processo guidato** porta dalla sinottica al locale fino alla decisione.
  4. È **collaborativa**: più amici vedono la stessa uscita e valutano insieme gli scenari.
  5. In seguito, il **weather routing** con le polari della propria barca.

## 2. Il processo di valutazione (il cuore dell'app)

| Fase | Cosa si guarda | Fonti | Risultato |
|---|---|---|---|
| **1. Sinottica** (da -5 a 0 giorni) | Carte al suolo di analisi e previsione: alte e basse pressioni, fronti, gradienti | UK Met Office (analisi e previsione fino a T+120), DWD (Bodenanalyse e Vorhersage), Aeronautica Militare / meteoam | Situazione generale e "tipo di tempo" (es. maestrale in ingresso, bassa sul Tirreno) |
| **2. Modelli globali** | Vento, raffiche, pressione e precipitazioni sui giorni dell'uscita | ECMWF IFS e AIFS, GFS, ICON, ARPEGE, UKMO, GEM | Tendenza e prima valutazione di affidabilità |
| **3. Ensemble** | Dispersione dei membri (quanto il futuro è incerto) | ECMWF ENS, GEFS, ICON-EPS | Livello di confidenza per ogni giorno |
| **4. Modelli locali ad alta risoluzione** (0–72 h) | Effetti costieri, brezze, canalizzazioni | ICON-2I (ItaliaMeteo-ARPAE, ~2 km), AROME, ICON-D2 | Dettaglio su golfi, bocche e capi |
| **5. Mare** | Onda significativa, mare lungo (swell), periodo e direzione, correnti | ECMWF WAM, MeteoFrance MFWAM, DWD EWAM, Copernicus | Comfort e sicurezza: onda e periodo rispetto alla barca |
| **6. Bollettini ufficiali** | Bollettino del mare e avvisi | Aeronautica Militare (meteomar), NAVTEX | Controllo obbligatorio prima di decidere |
| **7. Decisione** | Sintesi con semaforo e voto dell'equipaggio | — | Report condivisibile |

Il semaforo nasce dal confronto tra i dati e i **limiti della barca e dell'equipaggio** impostati dall'utente. Non è mai un giudizio assoluto: l'app mostra sempre **perché** ha dato quel colore (es. "raffiche 32 kn secondo AROME, 3 modelli su 5 sopra il tuo limite").

## 3. Funzioni principali

### 3.1 Mappa animata
- Mappa reale con stile **chiaro** (vettoriale) e **satellite**, più l'overlay dei segnali nautici di **OpenSeaMap**.
- Una **barra del tempo** per animare ora per ora (play/pausa, velocità, salto al giorno).
- Layer come in Windy: vento con particelle animate, raffiche, pressione con isobare, onda e swell, periodo, correnti, precipitazioni, nuvolosità, temperatura, CAPE e temporali, visibilità.
- Le carte sinottiche si vedono a fianco, in un pannello sincronizzato con la stessa ora della mappa.

### 3.2 Confronto tra modelli (la funzione distintiva)
- **Mappa a schermo diviso o "a tendina"** tra due modelli.
- **Mappa del disaccordo:** la deviazione standard tra i modelli, calcolata su ogni cella, si colora sulla mappa. Le zone "rosse" sono quelle dove i modelli non sono d'accordo.
- **Pannello dell'area visibile:** quando zoomi, l'app calcola per l'area inquadrata il minimo, la media e il massimo di vento e onda per ogni modello. Sopra ci mette un grafico temporale con le curve di tutti i modelli e la fascia dell'ensemble.
- **Punto o tappa:** tocchi un punto e ottieni il meteogramma multi-modello (vento, raffiche, direzione, onda, periodo).

### 3.3 Collaborazione
- Ogni **uscita** è una "stanza" condivisa con un link di invito.
- In tempo reale: chi è online, la funzione **"segui la mia vista"** (gli altri vedono la tua stessa mappa e ora), commenti fissati su mappa e ora, voto sugli scenari.
- Lo skipper chiude la valutazione con una decisione registrata, che finisce poi nel log book.

### 3.4 Report e condivisione
- Un report in **PDF** o immagine con sinottica, tabella per giorno con semaforo, grafici multi-modello e mappe chiave.
- Condivisione con la **Web Share API**: sul telefono apre il menu nativo con WhatsApp, Mail, Telegram e **AirDrop** (iOS/macOS).
- In alternativa, un link alla stanza oppure un link di sola lettura al report.

### 3.5 Funzionamento in mare (fondamentale)
- La webapp si installa sulla schermata Home come **PWA**.
- Prima della partenza l'app **scarica in anticipo** i dati dei giorni di uscita sulla zona, così restano consultabili offline quando a bordo manca la rete.

### 3.6 Weather routing (fase successiva)
- Il calcolo usa il metodo delle **isocrone** e tiene conto di vento, correnti, penalità per onda, zone da evitare e costa.
- Si può calcolare la rotta con **ogni modello**, per vedere quanto cambia la rotta ottima al variare del modello.
- **Polari:**
  - polari ORC, dai certificati e dai dati pubblici;
  - libreria di polari standard per i modelli di serie più diffusi;
  - polari personalizzate, inserite a mano o importate da file (formati Expedition/qtVlm).
  - La disponibilità e la licenza dei dataset vanno verificate. Un database "di tutte le barche" completo e gratuito non esiste: va costruito progressivamente.
- **Riferimenti open source da studiare:** il plugin weather_routing di OpenCPN, VISIR-2 (accademico, focalizzato sul Mediterraneo) e la libreria Python `weatherrouting`.

## 4. Dati: fonti e vincoli

- **Open-Meteo** è la scelta per partire: un'unica API per decine di modelli (incluso **ICON-2I** a 2 km sul Sud Europa), oltre a marine API ed ensemble API.
  - L'uso gratuito è **solo non commerciale** e ha limiti giornalieri.
  - Per un uso commerciale c'è un abbonamento a partire da circa 29 $/mese (prezzo da verificare).
  - I dati sono rilasciati con licenza CC BY 4.0 e vanno attribuiti.
- **Campi su mappa:** Open-Meteo è pensato per i punti. Per le animazioni servono **griglie**, e ci sono due strade:
  - **Fase 1:** si campiona una griglia di punti sull'area dell'uscita (es. 0,1°) con chiamate multi-punto e si mette in cache. È semplice e adatta ad aree piccole.
  - **Fase 2:** un backend scarica i **GRIB** dai portali open data ufficiali (ECMWF open data, NOAA NOMADS, DWD opendata), li converte in **tile** per ora e per modello e li serve alla mappa. È scalabile ed è quello che fa Windy.
- **Carte sinottiche:**
  - Met Office e DWD pubblicano immagini con condizioni d'uso da rispettare. Va verificato se si possono incorporare o solo linkare. DWD open data è il più permissivo.
  - Alternativa: generare **le nostre carte sinottiche** (isobare e pressione) dai modelli, sempre disponibili e coerenti con la mappa.
- **Mappe base:**
  - stile chiaro: OpenFreeMap o MapTiler;
  - satellite: MapTiler Satellite (chiave gratuita entro certi limiti) oppure Esri World Imagery;
  - nautica: overlay di OpenSeaMap.

## 5. Architettura proposta

```
 ┌──────────── PWA (telefono / tablet / PC) ─────────────┐
 │ MapLibre GL + layer WebGL (particelle vento, campi)   │
 │ Timeline · Confronto modelli · Report · Offline cache │
 └──────────────┬───────────────────────┬────────────────┘
                │ REST/tiles            │ realtime
 ┌──────────────▼──────────┐   ┌────────▼──────────────────┐
 │ Data service (Python)   │   │ Supabase (o Firebase)     │
 │ GRIB → tile per ora     │   │ utenti, uscite, stanze,   │
 │ statistiche multi-mod.  │   │ commenti, voti, log book  │
 │ proxy/cache Open-Meteo  │   └───────────────────────────┘
 │ routing isocrone        │
 └─────────────────────────┘
```

- **Frontend:** TypeScript con SvelteKit o React (**[DA DECIDERE]**), MapLibre GL JS e una PWA con service worker.
- **Backend dati:** Python (xarray + cfgrib) per i GRIB, aggiornato a ogni nuova run dei modelli.
- **Collaborazione e account:** Supabase (Postgres, autenticazione e realtime), che ha un piano gratuito sufficiente per un gruppo di amici.
- **Hosting:** il frontend su GitHub Pages, Cloudflare Pages o Vercel; il backend dati su una piccola VM o un container.

## 6. Identità grafica

- Per l'impaginazione si prende spunto dal corso della patente nautica, ma con **un nome, una palette e dei componenti propri**, per non confondersi.
- **Proposta di palette:** blu notte e ottanio, con un accento **arancio** (il colore di soccorso). Il semaforo verde, ambra e rosso è riservato alle decisioni.
- **Tema scuro "notturno"** con luminosità ridotta, per l'uso in pozzetto di notte.
- **Pensata per il pollice:** comandi grandi, utilizzabili con una mano e anche con le mani bagnate.

## 7. Evoluzione: Skipper WebApp

Il modulo meteo diventa uno dei moduli di una suite per lo skipper:

| Modulo | Contenuto |
|---|---|
| **Meteo** | Tutto quanto descritto sopra |
| **Check-in / Check-out** | Checklist di presa e riconsegna della barca, foto dei danni, inventario, carburante e acqua |
| **Guasti** | Segnalazioni con foto, priorità, storico per barca, contatti dei tecnici |
| **Contatti** | Marina, charter, tecnici, guardia costiera locale, equipaggio |
| **Emergenze** | Procedure MAYDAY/PAN-PAN guidate, posizione GPS pronta da leggere, numeri utili (1530), schede uomo a mare e incendio |
| **Log book** | Diario di bordo con posizione, rotta, vento, mare e motore; le decisioni meteo vengono importate in automatico |
| **Equipaggio** | Ruoli, turni di guardia, documenti |

## 8. Roadmap

1. **MVP 1 (alcune settimane):**
   - creazione dell'uscita (zona, data, giorni, limiti);
   - mappa chiara e satellite con timeline oraria;
   - vento e onda da 3–4 modelli via Open-Meteo su griglia campionata;
   - meteogramma multi-modello sul punto;
   - semaforo per giorno;
   - report condivisibile con Web Share;
   - PWA.
2. **MVP 2:**
   - pannello delle carte sinottiche;
   - mappa del disaccordo e statistiche sull'area visibile;
   - ensemble;
   - stanze condivise in tempo reale con commenti e voti.
3. **V1:**
   - backend GRIB e tile (più modelli e aree più ampie);
   - modalità offline completa;
   - integrazione dei bollettini ufficiali.
4. **V2:** weather routing con le polari.
5. **Skipper WebApp:** check-in/out, guasti, contatti, emergenze, log book.

## 9. Avvertenze

- L'app è uno **strumento di supporto**: non sostituisce i bollettini ufficiali né il giudizio dello skipper. Lo dirà chiaramente in ogni report.
- Le licenze e le condizioni d'uso di ogni fonte (modelli, carte, mappe, polari) vanno verificate prima di un uso pubblico o commerciale.

## 10. Decisioni da prendere [DA DECIDERE]

1. **Uso:** privato o per amici (gratuito) oppure prodotto commerciale? Cambiano le licenze dei dati e i costi.
2. **Area geografica iniziale:** solo il Mediterraneo o le coste italiane? Su quest'area si sceglie quali modelli locali usare.
3. **Stack frontend:** SvelteKit o React.
4. **Account:** accesso con Google/Apple oppure semplice link di invito senza registrazione?
5. **Nome e marchio:** "Skipper Meteo" come modulo, "Skipper WebApp" come contenitore?
