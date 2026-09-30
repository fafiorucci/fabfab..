# Corso patente nautica · note per Claude

- Rispondere sempre in italiano.
- Le presentazioni sono artifact di tipo Slides (tabella degli URL in `corso/export/README.md`).
- Lavorare sul branch `claude/corso-patente-nautica-indice-biov9q`: commit e push, niente PR.
- Ogni lezione chiude con gli ultimi 45 minuti di raccolta quiz ufficiali (DD 131/2022) sugli argomenti della lezione,
  ogni slide di quiz seguita dalla slide delle risposte; niente quiz intermedi durante la teoria.

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
4. Controllare a campione il PDF (pymupdf), poi commit e push insieme alle altre modifiche.

Requisiti dello script: Playwright + Chromium in `/opt/pw-browsers`, `python-pptx`, `Pillow`.
Il browser usa il proxy di `HTTPS_PROXY` per caricare i Google Fonts.
