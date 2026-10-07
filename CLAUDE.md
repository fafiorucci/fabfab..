# Corso patente nautica · note per Claude

- Rispondere sempre in italiano.
- Le presentazioni sono artifact di tipo Slides (tabella degli URL in `corso/export/README.md`).
- Dicitura del corso, nel piè di pagina di ogni slide e in fondo alla copertina:
  «Fabrizio Fiorucci · Patente nautica Vela/Motore entro le 12 miglia e senza limiti dalla costa»
  (in copertina senza il nome). Vale per lezioni, appendici, schede, indice e presentazione della scuola.
- Lavorare sul branch `claude/corso-patente-nautica-indice-biov9q`: commit e push, niente PR.
- Lezioni 01-15: teoria in 75 minuti divisa in capitoli, ognuno aperto da una slide di apertura (`chapter()`);
  dopo ogni paragrafo una verifica da 2 quiz ufficiali (DD 131/2022) con la sua slide delle risposte
  (helper `intermedi.py` nella cartella della lezione).
  Nelle lezioni di carteggio 10-15 i capitoli sono le tecniche e i gruppi di esercizi, con la verifica in fondo
  a ogni capitolo (helper `schema_cart.py`).
- Ogni lezione chiude con gli ultimi 45 minuti di raccolta quiz ufficiali (12 slide da 3 quiz) sugli argomenti
  della lezione, ogni slide di quiz seguita dalla slide delle risposte, senza ripetere i quiz delle verifiche.

## Export obbligatorio dopo ogni modifica

Ogni volta che si modifica la struttura di un deck (slide aggiunte, tolte, spostate o cambiate)
o si crea un deck nuovo, dopo averlo pubblicato va rifatto l'export in `corso/export/`:

1. Scaricare il deck pubblicato con `Artifact` → `read`, `paths` = `project/deck.json`
   e poi tutte le `project/slides/<id>.html` elencate in `order`, con `out_dir` in una cartella
   di lavoro (es. `<scratchpad>/exp/L06`).
2. Eseguire `corso/export/strumenti/esporta.sh <cartella>`: scrive
   `corso/export/html/<titolo>.html`, `pdf/<titolo>.pdf`, `pptx/<titolo>.pptx`
   (nome = titolo del deck, con « · » → « - » e senza `/ : ?`).
3. Se il titolo è cambiato o il deck è nuovo, cancellare i file col vecchio nome e aggiornare l'elenco
   in `corso/export/README.md`, con i link di download diretto nella forma
   `[PPTX](pptx/<nome URL-encoded>.pptx?raw=true)` (idem PDF e HTML).
4. Rifare la versione protetta in `corso/export/pdf-protetti/` (filigrana, stampa e copia bloccate):
   `python3 corso/export/strumenti/proteggi.py pdf/<nome>.pdf pdf-protetti/<nome>.pdf <password>`
   oppure `PDF_OWNER_PW=… corso/export/strumenti/proteggi_tutti.sh`. La password del proprietario non è nel
   repository: chiederla a Fabrizio; se non la dà, segnalare che i PDF protetti non sono aggiornati.
5. Controllare a campione il PDF (pymupdf), poi commit e push insieme alle altre modifiche.

Requisiti dello script: Playwright + Chromium in `/opt/pw-browsers`, `python-pptx`, `Pillow`.
Il browser usa il proxy di `HTTPS_PROXY` per caricare i Google Fonts.

## App del corso

- Sorgenti in `corso/app/` (vedi `corso/app/README.md`). Ogni modifica all'app pubblicata aumenta la versione
  (`VERSIONE`/`RILASCIO` in `corso/app/index.html` e `VERSIONE` in `corso/app/aula/server.py`) e aggiunge una voce in
  `corso/app/VERSIONI.md`; poi si rifanno il pacchetto per l'aula (`aula/prepara_pacchetto.py`) e, se tocca la demo,
  `demo/prepara_demo.py`, e si ripubblicano gli artifact (app: PoYsNRcs6eKTS3DW7WdLv4, demo: TS7HycJgEtA3ugZTLMdsZm).
- App online (allievi a casa e in aula, area istruttore `/docente`): dopo il pacchetto per l'aula si rifà
  `casa/prepara_casa.py` e si copia `$SP/casa` nel repository `fafiorucci/corso-nautico-prova` (branch `main`, push:
  Cloudflare ripubblica da solo). Indirizzo `https://corsonautico-ondaportante.fafiorucci.workers.dev/`, protetto da
  Cloudflare Access; le lezioni si aprono dall'area istruttore. Dettagli in `corso/app/README.md`.
