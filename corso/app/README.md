# App del corso

Pubblicata come artifact: https://claude.ai/artifact/PoYsNRcs6eKTS3DW7WdLv4

- `index.html` · l'app (registrazione, percorso delle lezioni, visore slide, quiz uno per pagina, storico, rimando dall'errore alla slide). Il logo in alto a sinistra apre il menu a cassetto con lezioni (capitoli e verifiche) e materiali; sul tocco slide e quiz si sfogliano col dito.
- `app_build.py` · genera `corso.json` (15 lezioni con capitoli, quiz, scheda riassuntiva e appendici collegate), `slides/` (teoria delle lezioni, schede e pagine delle appendici `AX-NNN.jpg`, con filigrana; l'app mostra le appendici nel suo visore) e `appendici/` (HTML con il visore) dai file in `corso/export/`. Le lezioni aperte all'inizio sono in `ATTIVE`, l'abbinamento appendici-lezioni in `APPENDICI`.

Progressi per allievo nel `db` dell'artifact, in `data/users/<id>/profile` (privato per ogni allievo); senza `db` restano sul dispositivo.
Progetto completo: documento «Progetto: corso di patente nautica in app e in libro».

## Versione per l'aula (`aula/`)

Pacchetto per il PC dell'istruttore: gli allievi sul wifi della scuola aprono l'app e i progressi restano sul PC.

- `aula/server.py`: server con la sola libreria standard di Python. Registra gli allievi (nome + codice personale di 4-6 cifre), salva i progressi in `dati/allievi.json`, con un backup al giorno, e serve l'area istruttore `/docente`, protetta da PIN.
- `aula/docente.html`: area istruttore, con QR da proiettare, andamento di ogni allievo, quiz più sbagliati, nuovo codice, eliminazione ed export CSV.
- `aula/prepara_pacchetto.py`: rigenera `aula/www/` da `index.html` (caratteri in locale) e lo zip in `corso/export/app/`. Con `--python` include Python portatile per Windows, così non serve installarlo.
- L'app riconosce da sola dove gira: server dell'aula (`api/info`), artifact (archivio `db`) oppure solo il dispositivo.

## Lezioni aperte, schede e appendici

- Tutte le 15 lezioni sono nell'elenco; quelle chiuse si vedono bloccate. Online sono aperte quelle con `attiva` in `corso.json` (si pubblicano solo le loro immagini); in aula le apre l'istruttore (Area istruttore → Lezioni) e il server non fornisce slide e appendici delle lezioni chiuse.
- In cima a ogni lezione: la scheda riassuntiva e le appendici collegate. Menu «Materiali»: tutte le schede, i numeri d'oro con la loro verifica e le appendici A-M (si aprono con la prima lezione collegata).

## Profilo dell'allievo

Si apre toccando il proprio nome o avatar in alto: nome e cognome, colore dell'avatar, cambio del codice (in aula), patente (entro 12 miglia o senza limiti; motore, vela o entrambe), data d'esame, email e telefono, tema, testo più grande, obiettivo settimanale, scarica o cancella i propri dati. La patente segna come facoltative la lezione 9 (solo motore) e le lezioni 10-15 (entro le 12 miglia); la home mostra il conto alla rovescia e l'obiettivo della settimana (dal diario di studio: quiz e slide per giorno). L'istruttore vede patente, esame e contatti nella tabella della classe.

## Versione, aiuto e demo

- Versione corrente e regole di numerazione: `VERSIONI.md`.
- Aiuto: pulsante «?» in alto, nell'app e nell'area istruttore; mostra cosa si fa nella pagina aperta e le domande frequenti. La prima volta compare un suggerimento sotto il pulsante.
- Demo: `demo/prepara_demo.py` costruisce in `$SP/demo` una versione dimostrativa (lezione 1 fino al capitolo 1, scheda della lezione 1, numeri d'oro, appendici C ed E, area istruttore con allievi inventati da `demo/demo-dati.js`). Pubblicata come artifact separato. Lo stesso script scrive anche `corso/export/app/Corso patente nautica - demo.zip`, da aprire senza server: si scompatta e si fa doppio clic su `index.html` (dati in `dati-locali.js`, caratteri locali, funziona anche senza internet).

## App online (a casa e in aula)

Indirizzo per gli allievi: `https://corsonautico-ondaportante.fafiorucci.workers.dev/`; area istruttore: `…/docente` (solo con l'email dell'istruttore, `fafiorucci@gmail.com`).

- `casa/prepara_casa.py` costruisce in `$SP/casa` il contenuto del repository privato `corso-nautico-prova` (prima va rifatto `aula/prepara_pacchetto.py`, da cui prende slide, appendici, caratteri, presentazioni e area istruttore):
  `wrangler.jsonc` (Worker `corsonautico-ondaportante`), `src/worker.js` (da `casa/worker.js`) e `public/` (il sito). Cloudflare ripubblica da solo a ogni push su `main` (circa 20 secondi).
- Il server (`casa/worker.js`): riconosce chi entra dall'email nel token firmato di Cloudflare Access (verifica di firma, team `ondaportante`, applicazione e scadenza); risponde alle stesse richieste del server dell'aula (`/api/…`), ma senza codice personale; tiene allievi, progressi e lezioni aperte in un Durable Object (archivio SQLite di Cloudflare, piano gratuito); dà slide, schede e appendici solo delle lezioni aperte e le presentazioni solo all'istruttore.
- L'app (`index.html` con `online` in `corso.json`): la prima volta chiede solo il nome (e porta online i progressi già sul telefono); salva online a ogni risposta; senza rete continua sul telefono e invia appena torna la connessione; scarica subito slide, schede e appendici delle lezioni aperte per averle anche offline. Le lezioni si aprono dall'area istruttore (scheda «Lezioni»), senza ripubblicare.
- Accesso riservato: in Cloudflare Zero Trust l'applicazione Access del Worker ha l'accesso con codice via email (One-time PIN), la policy «Allievi» (Allow, Include → Emails) e sessione di 30 giorni. Anche l'email dell'istruttore deve essere nell'elenco. A ogni apertura con la rete l'app chiede `accesso.json`: se Access rimanda al login, toglie dal telefono slide e quiz e mostra «Accesso da rinnovare». Senza rete funziona per `GIORNI_OFFLINE` (7) giorni dall'ultimo controllo riuscito.
- Account di prova per altre scuole: scheda «Prove» dell'area istruttore (email, giorni, nota); l'email va aggiunta anche alla policy «Allievi». Il server li riconosce (`prova:<email>` nell'archivio): un `corso.json` ridotto (`corsoProva`: prime `PROVA_SLIDE` slide delle lezioni `PROVA_LEZIONI` con la prima verifica, niente schede né appendici), presentazioni `PROVA_PRESENTAZIONI` (solo «Rotta verso la patente»), area istruttore con allievi inventati (`allieviInventati`), esclusi dalla classe vera; scaduti, ogni richiesta ha risposta 403 e l'app si svuota.
- Prove con link (senza email): `wrangler.prova.jsonc` pubblica dallo stesso repository il Worker `corso-nautico-prova` (`https://corso-nautico-prova.fafiorucci.workers.dev/`, senza Cloudflare Access, cartella `public-prova/` con i soli file della prova), che usa l'archivio del Worker principale (`script_name`). Si entra con `?p=<codice>` creato nella scheda «Prove» (archivio: `prova:link:<codice>`); il codice resta nel cookie `corso_prova`. Su Cloudflare il secondo Worker ha come comando di pubblicazione `npx wrangler deploy -c wrangler.prova.jsonc`.
- Per togliere un allievo: togliere la sua email dalla policy «Allievi», poi in Zero Trust → Team & Resources → Users selezionarlo e fare Action → Revoke (chiude la sessione) e Action → Remove users (libera il posto: il piano gratuito ne ha 50; revocare da solo non lo libera); poi, se si vuole, «Elimina allievo» nell'area istruttore. In Settings → Admin controls «Remove inactive users from seats» libera da solo i posti di chi non entra da un periodo scelto (da 1 mese a 1 anno).
- Il logo della pagina di accesso (Zero Trust → Custom pages → Login page) è su un progetto Cloudflare Pages separato e pubblico, `https://onda-logo.pages.dev/logo.png` (immagine in `casa/logo-accesso.png`).
- Prova in locale: `npx wrangler dev --var PROVA_EMAIL:<email>` nella cartella `$SP/casa` (con `PROVA_EMAIL` il server non chiede il token di Access e accetta l'intestazione `x-prova-email`; in produzione non va mai impostata).
- Il server dell'aula resta come riserva (per esempio senza internet in aula) e per proiettare dal PC; il suo «Porta a casa» apre l'app online.
