# Versioni di Skipper Meteo / Skipper WebApp

La versione in uso si legge nel menu del logo e in fondo a ogni pagina.

## 0.6.0 — navigazione in tempo reale, sessioni, server meteo proprio
- Nuovo modulo **Navigazione**: posizione GPS del telefono o del PC sulla mappa nautica, velocità e rotta (SOG/COG), registrazione della traccia con schermo sempre acceso, rotta a waypoint (toccando la mappa o importando un file GPX, per esempio da Navionics) con rilevamento, distanza, arrivo stimato e fuori rotta verso il prossimo waypoint; passaggio automatico al waypoint successivo all'arrivo o al traverso; esportazione GPX di rotta e traccia (per Navionics e chartplotter); posizione nel log book e condivisione.
- **Check-in e check-out**: archivio delle sessioni sul dispositivo (salva, nuova, apri, duplica per la stessa barca, verbale di ogni sessione, esporta e importa file).
- Nuova pagina **Impostazioni**: server dei dati meteo. Con un server Open-Meteo proprio (cartella `server-meteo`, con Docker) l'app chiede prima a lui e, se non risponde entro il tempo impostato, passa da sola a Open-Meteo pubblico; prova e confronto dei tempi di risposta; indicatore della fonte dei dati nella pagina meteo.
- Menu dei moduli scorrevole.

## 0.5.2 — menu scorrevole
- Il menu dei moduli scorre con la sua barra verticale quando non entra nello schermo (telefono, finestre basse).

## 0.5.1 — aggiornamento automatico
- Le pagine si scaricano sempre fresche dal sito e, quando esce una nuova versione, l'app si ricarica da sola: niente più versione vecchia rimasta in memoria sul telefono o sul browser.
- Corretto il service worker, che non si installava (la pagina iniziale compariva due volte nella lista da salvare): ora l'app funziona davvero anche offline con le pagine e i dati già visti.

## 0.5.0 — carte sinottiche, check-in High Five, safety plan, briefing, memo, demo pubblica
- In fondo al menu: «Onda Portante · a cura di Fabrizio Fiorucci». Partenza predefinita: Fiumicino.
- Nuovo modulo **Carte sinottiche** (icona anche nella barra della mappa): isobare e centri A/B su Europa e Mediterraneo ogni 12 ore UTC dall'analisi fino a +5 giorni, animabili; confronto fino a 3 di 7 modelli sovrapposti; analisi DWD e collegamenti a Met Office e Aeronautica Militare.
- **Check-in** riorganizzato come da documentazione Onda Portante: Documenti, poi Esterno (prima fuori) e Interno (poi dentro); l'**High Five** (salpa ancora, sentine, batterie, motore, timoneria) in testa con l'avviso che senza uno di questi non si lascia l'ormeggio; principi e linee guida. Check-out con la stessa struttura.
- Nuovo modulo **Safety plan**: tipo di barca e pianta degli interni (o foto propria), su cui segnare batterie, serbatoi e scambio serbatoi, prese a mare dei bagni, estintori, pronto soccorso, attrezzi e altro; condivisibile come immagine.
- Nuovo modulo **Briefing equipaggio** in due parti, vita di bordo e sicurezza, esteso per i clienti; spunte e invio del testo all'equipaggio.
- Nuovo modulo **Controlli WOBBLE** per il motore, con registro giornaliero.
- Nuovo modulo **Skipper memo**: COLREG (precedenze, fanali, suoni), IALA regione A e ritmi delle luci, bandiere del Codice internazionale con alfabeto e numeri, Beaufort e Douglas, VHF, MARPOL; con ricerca. Sarà allineato al memorandum dello skipper.
- **Demo pubblica**: il sito su GitHub Pages mostra solo meteo sulla zona di esempio, carte sinottiche e l'High Five del check-in; gli altri moduli sono visibili ma bloccati. La versione completa si usa in locale.

## 0.4.0 — moduli di bordo, sinottica, weather routing
- Menu dei moduli nel logo: Meteo, Rotta, Check-in, Check-out, Guasti, Log book, Contatti, Emergenze.
- Mappa meteo più pulita: barra verticale di icone con menu a comparsa; barra del tempo compatta.
- Sinottica: isobare e centri di alta (A) e bassa (B) pressione del modello, animabili ora per ora; scheda con l'analisi ufficiale DWD e i collegamenti a Met Office e Aeronautica Militare.
- 17 modelli disponibili (globali ed europei ad alta risoluzione), con stima delle chiamate Open-Meteo.
- Rotta: weather routing a isocrone con polari tipo o importate, rendimento, motore sotto una soglia di velocità; tabella ora per ora condivisibile.
- Check-in e Check-out con checklist e verbale condivisibile; Guasti; Log book con GPS ed esportazione CSV; Contatti con i numeri di emergenza; Emergenze con posizione GPS, testo MAYDAY precompilato e procedure.
- Numero di versione visibile nell'app.

## 0.3.0 — valori nel punto e limiti di Open-Meteo
- Riquadro con tutti i valori del punto toccato (vento, raffiche, pioggia, pressione, onda, mare lungo) per ogni modello.
- Una sola richiesta per tutti i modelli, regolatore delle 600 chiamate al minuto e nuovo tentativo automatico.
- Logo di Onda Portante.

## 0.2.0 — meteo su tutta la mappa
- Il campo meteo, la valutazione e il confronto seguono la zona inquadrata.
- Particelle del vento più lente; note e disclaimer.

## 0.1.0 — prima versione
- Valutazione multi-modello con semaforo, mappa chiara/satellite animata, disaccordo tra modelli, report e link di invito.
