# App del corso

Pubblicata come artifact: https://claude.ai/artifact/PoYsNRcs6eKTS3DW7WdLv4

- `index.html` · l'app (registrazione, percorso delle lezioni, visore slide, quiz a caselle, storico, rimando dall'errore alla slide).
- `app_build.py` · genera `corso.json` (15 lezioni con capitoli, quiz, scheda riassuntiva e appendici collegate), `slides/` (teoria delle lezioni e schede, con filigrana) e `appendici/` (HTML con il visore) dai file in `corso/export/`. Le lezioni aperte all'inizio sono in `ATTIVE`, l'abbinamento appendici-lezioni in `APPENDICI`.

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
